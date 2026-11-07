#!/usr/bin/env python3
"""Classify a spec-land marker, patch-id decision, or path overlap; read and
post the SHA marker on a PR.

Usage:
    land_check.py parse
    land_check.py decide --parents N --pr-commits N --recorded ID --single ID [--range ID]
    land_check.py overlap
    land_check.py latest <N>
    land_check.py post <N> --review <passed|skipped|inconclusive|not-run> [--no-push]
    land_check.py preflight [<PR-number | PR-URL | spec-path>] [--ticket ID]
    land_check.py wiki --state FILE
    land_check.py cleanup --state FILE

parse reads a PR comment body on stdin.
    0  one line: head=<40> base=<40> patch-id=<40> review=<token>
    1  not a marker (stdout empty). A crash must not use this code.
    2  the body is a marker and it is malformed

decide prints exactly "match single", "match range", or "mismatch".
    0  match
    1  mismatch
    2  parents < 1, pr-commits < 1, or a bad hex id

overlap reads two newline-delimited path lists separated by a line that is
exactly "--".
    0  stdout "clear"
    1  the shared paths, sorted, one per line

latest reads the PR's issue comments with gh api --paginate --slurp and finds
the latest marker: greatest created_at, ties to the greatest id.
    0  one line: id=<id> head=<40> base=<40> patch-id=<40> review=<token>
    1  exactly "no marker" (a successful full read found none)
    2  "malformed marker id=<id>", then the raw body
    4  the comment read failed (gh error, bad JSON or array shape, a field
       missing or of the wrong type, a marker created_at with no timezone)

post checks the PR head, base and patch-id, reads the latest marker, and posts
a new marker with gh pr comment, retrying a failed post once. Run it from the
PR's checkout. The first stdout line is the status line.
    0  "SHA marker: posted (head <head>, review <token>)", or
       "SHA marker: already current (head <head>)" when the head matches and the new token does not outrank the recorded one
    1  "SHA marker: NOT posted (<reason>)", then the body when it was built

preflight <PR-number | PR-URL | spec-path> [--ticket ID] does spec-land's
read-only checks: PR selection, MERGED state, one fetch window, the marker
read, head/patch-id/base-drift verification, ticket id, test-plan checklist,
states.json target, wiki path / Slug / post-land command, worktrees and
default branch. A mismatch or malformed marker is a warning, not a halt.
    0  the confirmation block, then one line spec_land_state=<JSON>
    1  "HALT: <reason>" (not merged, failed PR or comment read, failed fetch,
       wrong-repository URL, no unique PR, a failed git command)
    4  "NEEDS TICKET: ..." - rerun with --ticket ID
It writes nothing. The caller saves the JSON after the operator agrees.

wiki --state FILE writes the merge log line through the installed
prepend_log_entry.py and applies the filemap D/R/A edits.
cleanup --state FILE removes a clean worktree, deletes the local branch (-D
only after a SHA match with the tip at the PR head) and the remote branch
(leased on the PR head), fast-forwards a clean default-branch main checkout,
and then runs the post-land command when main holds the landed commit.
Both print one outcome line per action and exit 1 when any action failed.

Only parse, decide and overlap read stdin; main() decodes it as strict UTF-8.
latest, post, preflight, wiki and cleanup never read stdin. Any other failure exits 3, so exit 1
stays the documented outcome. SystemExit and KeyboardInterrupt propagate:
argparse usage errors stay exit 2.

Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

_OPEN = "<!-- vigil-spec-land"
_CLOSE = "-->"
_HEX_ID = re.compile(r"^[0-9a-f]{40}$")
_REVIEW_TOKENS = frozenset(("passed", "skipped", "inconclusive", "not-run"))
# Low to high. A same-head post replaces the marker only when the new token outranks the recorded one.
_REVIEW_RANK = {"not-run": 0, "skipped": 1, "inconclusive": 2, "passed": 3}
_ID_LABELS = ("head", "base", "patch-id")
_CMD_TIMEOUT = 120
# A credential prompt must fail, not wait on a terminal nobody is watching.
_CHILD_ENV = {"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never",
              "GH_PROMPT_DISABLED": "1"}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="land_check.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("parse")
    decide = sub.add_parser("decide")
    decide.add_argument("--parents", type=int, required=True)
    decide.add_argument("--pr-commits", type=int, required=True)
    decide.add_argument("--recorded", required=True)
    decide.add_argument("--single", required=True)
    decide.add_argument("--range", dest="range_id", default=None)
    sub.add_parser("overlap")
    latest = sub.add_parser("latest")
    latest.add_argument("number", type=int)
    post = sub.add_parser("post")
    post.add_argument("number", type=int)
    post.add_argument("--review", required=True, choices=sorted(_REVIEW_TOKENS))
    post.add_argument("--no-push", action="store_true")
    preflight = sub.add_parser("preflight")
    preflight.add_argument("target", nargs="?")
    preflight.add_argument("--ticket")
    for name in ("wiki", "cleanup"):
        sub.add_parser(name).add_argument("--state", required=True)
    return parser


def _body_lines(text: str) -> list[str]:
    # Decision 10: one optional CR before each LF. A lone CR is not a break.
    lines = []
    for line in text.split("\n"):
        if line.endswith("\r"):
            line = line[:-1]
        lines.append(line)
    return lines


def _strip_marker(text: str) -> str:
    # One leading U+FEFF, then one surrounding whitespace run. strip() does
    # not remove U+FEFF, so the BOM has to come off first (Decision 10).
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.strip()


def _parse_marker(text: str) -> tuple[int, str]:
    text = _strip_marker(text)
    if not text.startswith(_OPEN):
        return 1, ""
    lines = _body_lines(text)
    if len(lines) != 6 or lines[0] != _OPEN or lines[5] != _CLOSE:
        return 2, ""
    values = []
    for label, line in zip(_ID_LABELS, lines[1:4]):
        prefix = label + ": "
        if not line.startswith(prefix) or _HEX_ID.fullmatch(line[len(prefix):]) is None:
            return 2, ""
        values.append(line[len(prefix):])
    review_prefix = "review: "
    if not lines[4].startswith(review_prefix):
        return 2, ""
    review = lines[4][len(review_prefix):]
    if review not in _REVIEW_TOKENS:
        return 2, ""
    head, base, patch = values
    return 0, f"head={head} base={base} patch-id={patch} review={review}"


def _bad_id(value: str | None) -> bool:
    return value is None or _HEX_ID.fullmatch(value) is None


def _decide(parents: int, pr_commits: int, recorded: str, single: str,
            range_id: str | None) -> tuple[int, str]:
    if parents < 1 or pr_commits < 1 or _bad_id(recorded) or _bad_id(single):
        return 2, ""
    if range_id is not None and _bad_id(range_id):
        return 2, ""
    # Decision 3: two or more parents, and a one-commit PR, compare single only.
    # The range argument is not a candidate on either arm.
    if parents >= 2 or pr_commits == 1:
        if single == recorded:
            return 0, "match single"
        return 1, "mismatch"
    if single == recorded:
        return 0, "match single"
    if range_id is not None and range_id == recorded:
        return 0, "match range"
    return 1, "mismatch"


def _overlap(text: str) -> tuple[int, list[str]]:
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    try:
        split_at = lines.index("--")
    except ValueError:
        # shortcut: missing "--" exits 2, upgrade when Decision 16 names this input
        return 2, []
    # A blank line is not a path, so trailing newlines in pasted git output never count as shared.
    shared = sorted(set(filter(None, lines[:split_at])).intersection(filter(None, lines[split_at + 1:])))
    if not shared:
        return 0, []
    return 1, shared


def _cmd(argv: list[str], input: bytes | None = None) -> tuple[int, bytes, bytes]:
    # Bytes in and out: Windows' locale decoder is cp1252, and git diff output
    # must reach git patch-id unchanged (read_board.py:181-183 precedent).
    kwargs = {"input": input} if input is not None else {"stdin": subprocess.DEVNULL}
    try:
        proc = subprocess.run(
            argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=_CMD_TIMEOUT, env={**os.environ, **_CHILD_ENV}, **kwargs)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, b"", str(exc).encode("utf-8", "replace")
    return proc.returncode, proc.stdout, proc.stderr


def _sleep(seconds: float) -> None:
    time.sleep(seconds)


def _comments_argv(number: int) -> list[str]:
    # gh fills {owner} and {repo} from the working directory's repository.
    # No --jq: gh rejects --slurp combined with --jq.
    return ["gh", "api", "--paginate", "--slurp",
            "repos/{{owner}}/{{repo}}/issues/{}/comments".format(number)]


class _ReadFailed(Exception):
    pass


def _timestamp(value: str) -> datetime.datetime:
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        when = datetime.datetime.fromisoformat(text)
    except ValueError:
        raise _ReadFailed("created_at does not parse: {!r}".format(value)) from None
    if when.tzinfo is None:
        raise _ReadFailed("created_at has no timezone: {!r}".format(value))
    return when


def _read_latest(number: int) -> tuple[int, str, str | None] | None:
    """None when there is no marker; else (id, raw body, parse line or None).

    Raises _ReadFailed. A failed or truncated read is never an absent marker.
    """
    code, out, err = _cmd(_comments_argv(number))
    if code != 0:
        raise _ReadFailed("gh api exited {}: {}".format(
            code, err.decode("utf-8", "replace").strip()))
    try:
        pages = json.loads(out.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _ReadFailed("comment JSON: {}".format(exc)) from None
    if not isinstance(pages, list) or not all(isinstance(page, list) for page in pages):
        raise _ReadFailed("comment JSON is not an array of pages")
    best = None
    for page in pages:
        for comment in page:
            if not isinstance(comment, dict):
                raise _ReadFailed("a comment is not an object")
            cid, body, created = (comment.get("id"), comment.get("body"),
                                  comment.get("created_at"))
            # bool is an int subclass; a true id is not an id.
            if not isinstance(cid, int) or isinstance(cid, bool) \
                    or not isinstance(body, str) or not isinstance(created, str):
                raise _ReadFailed("a comment lacks an integer id, a string body "
                                  "or a string created_at")
            if not _strip_marker(body).startswith(_OPEN):
                continue
            key = (_timestamp(created), cid)
            if best is None or key > best[0]:
                best = (key, cid, body)
    if best is None:
        return None
    _, cid, body = best
    code, line = _parse_marker(body)
    return cid, body, line if code == 0 else None


def _safe(text: str) -> str:
    # A lone surrogate from JSON must not crash the print under strict UTF-8.
    return text.encode("utf-8", "backslashreplace").decode("utf-8")


def _latest(number: int) -> int:
    try:
        found = _read_latest(number)
    except _ReadFailed as exc:
        print("comment read failed: {}".format(exc), file=sys.stderr)
        return 4
    if found is None:
        print("no marker")
        return 1
    cid, body, line = found
    if line is None:
        print("malformed marker id={}".format(cid))
        print(_safe(body))
        return 2
    print("id={} {}".format(cid, line))
    return 0


def _pr_ids(number: int) -> tuple[str, str] | None:
    code, out, err = _cmd(["gh", "pr", "view", str(number), "--json", "headRefOid,baseRefOid"])
    if code != 0:
        sys.stderr.write(err.decode("utf-8", "replace"))
        return None
    try:
        data = json.loads(out.decode("utf-8"))
        head, base = data["headRefOid"], data["baseRefOid"]
    except (UnicodeDecodeError, ValueError, TypeError, KeyError):
        return None
    if _bad_id(head) or _bad_id(base):
        return None
    return head, base


def _patch_id(base: str, head: str) -> str | None:
    code, diff, err = _cmd(["git", "diff", "{}...{}".format(base, head)])
    if code != 0:
        sys.stderr.write(err.decode("utf-8", "replace"))
        return None
    code, out, err = _cmd(["git", "patch-id", "--stable"], input=diff)
    if code != 0:
        sys.stderr.write(err.decode("utf-8", "replace"))
        return None
    try:
        lines = out.decode("ascii").splitlines()
    except UnicodeDecodeError:
        return None
    if len(lines) != 1:
        return None
    fields = lines[0].split()
    if not fields or _bad_id(fields[0]):
        return None
    return fields[0]


def _valid_head_line(body: str) -> str | None:
    lines = _body_lines(_strip_marker(body))
    if len(lines) < 2 or not lines[1].startswith("head: "):
        return None
    value = lines[1][len("head: "):]
    return None if _bad_id(value) else value


def _recorded_review(line: str) -> str:
    for field in line.split():
        if field.startswith("review="):
            return field[len("review="):]
    return ""


def _post(number: int, review: str, no_push: bool) -> int:
    def refuse(reason: str, body: str | None = None) -> int:
        print("SHA marker: NOT posted ({})".format(reason))
        if body is not None:
            sys.stdout.write(body)
        return 1

    ids = _pr_ids(number)
    if ids is None:
        return refuse("gh pr view failed")
    remote, base = ids
    code, out, _ = _cmd(["git", "rev-parse", "HEAD"])
    first = out.decode("ascii", "replace").strip().split("\n")[0].strip() if code == 0 else ""
    if not first or _bad_id(first):
        # No re-read: a local head that is not an id will not start matching.
        return refuse("head mismatch {} != {}".format(first or "none", remote))
    if first != remote:
        # GitHub can lag in updating a PR's head right after a push.
        _sleep(5)
        ids = _pr_ids(number)
        if ids is None:
            return refuse("gh pr view failed")
        remote, base = ids
        if first != remote:
            return refuse("head mismatch {} != {}".format(first, remote))
    head = first

    if _cmd(["git", "cat-file", "-e", base])[0] != 0:
        _cmd(["git", "fetch", "origin"])
        if _cmd(["git", "cat-file", "-e", base])[0] != 0:
            return refuse("base object missing")
    patch = _patch_id(base, head)
    if patch is None:
        return refuse("bad patch-id")
    body = "\n".join((_OPEN, "head: " + head, "base: " + base,
                      "patch-id: " + patch, "review: " + review, _CLOSE)) + "\n"

    try:
        latest = _read_latest(number)
    except _ReadFailed as exc:
        print("comment read failed: {}".format(exc), file=sys.stderr)
        return refuse("comment read failed", body)
    if latest is not None:
        cid, raw, line = latest
        if line is not None:
            if line.split()[0] == "head=" + head:
                recorded = _recorded_review(line)
                if _REVIEW_RANK[review] <= _REVIEW_RANK.get(recorded, -1):
                    print("SHA marker: already current (head {})".format(head))
                    return 0
        else:
            print("latest marker id={} (malformed):".format(cid), file=sys.stderr)
            print(_safe(raw), file=sys.stderr)
            if no_push and _valid_head_line(raw) is None:
                return refuse("latest marker has no valid head (no-push)", body)

    fd, path = tempfile.mkstemp(prefix="vigil-spec-land-", suffix=".md")
    try:
        # Close before gh runs: Windows will not share an open write handle.
        with os.fdopen(fd, "wb") as handle:
            handle.write(body.encode("utf-8"))
        argv = ["gh", "pr", "comment", str(number), "--body-file", path]
        posted = False
        for _ in range(2):
            code, _, err = _cmd(argv)
            if code == 0:
                posted = True
                break
            sys.stderr.write(err.decode("utf-8", "replace"))
    finally:
        try:
            os.remove(path)
        except OSError as exc:
            print("warning: temp body file not removed: {}".format(exc), file=sys.stderr)
    if not posted:
        return refuse("gh pr comment failed twice", body)
    print("SHA marker: posted (head {}, review {})".format(head, review))
    return 0


# --- VHS-97: preflight, wiki, cleanup -------------------------------------

_TICKET = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")
_TICKET_PREFIX = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+")
_UNANCHORED = re.compile(r"(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9]*-[0-9]+")
# A path runs to whitespace, a quote, a backtick or a bracket. Backslashes stay.
_ABS_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|~/|/)[^\s`'" + '"' + r"<>|()]*")
_LOG_DATE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\]", re.MULTILINE)
_HEADING = re.compile(r"^#{1,6} ")
_STATE_VERSION = 1
_STATE_PREFIX = "spec_land_state="
# gh pr list pages internally up to --limit; this is past any real ticket.
_SEARCH_LIMIT = "10000"
_PMC = "Post-merge Checklists"
_POST_LAND_TIMEOUT = 900


class _Halt(Exception):
    pass


class _NeedTicket(Exception):
    def __init__(self, number: int, candidates: list[str]) -> None:
        super().__init__(number, candidates)
        self.number = number
        self.candidates = candidates


def _text(data: bytes) -> str:
    return data.decode("utf-8", "replace")


def _must(argv: list[str], what: str, input: bytes | None = None) -> str:
    code, out, err = _cmd(argv, input)
    if code != 0:
        detail = _text(err).strip() or _text(out).strip()
        raise _Halt("{} failed (exit {}): {}".format(what, code, detail))
    return _text(out)


def _json(argv: list[str], what: str):
    raw = _must(argv, what)
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise _Halt("{}: bad JSON: {}".format(what, exc)) from None


def _norm_path(value: str) -> str:
    """Accept C:/, C:\\ and /c/ forms. On Windows /c/ becomes C:/."""
    text = value.strip()
    if text == "~" or text.startswith("~/"):
        text = os.path.expanduser(text)
    text = text.replace("\\", "/")
    if os.name == "nt":
        match = re.match(r"^/([A-Za-z])(/.*)?$", text)
        if match:
            text = match.group(1).upper() + ":" + (match.group(2) or "/")
    return text


def _config_dir() -> str:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        return _norm_path(env)
    return _norm_path(os.path.join(os.path.expanduser("~"), ".claude"))


def _unanchored(text) -> str | None:
    match = _UNANCHORED.search(text) if isinstance(text, str) else None
    return match.group(0).upper() if match else None


def _repo() -> str:
    data = _json(["gh", "repo", "view", "--json", "owner,name"], "gh repo view")
    try:
        return "{}/{}".format(data["owner"]["login"], data["name"])
    except (TypeError, KeyError):
        raise _Halt("gh repo view: no owner or name") from None


def _select(arg: str | None, repo: str) -> tuple[int, str | None]:
    """The PR number, and the ticket id when the argument is a spec path."""
    if arg is None:
        data = _json(["gh", "pr", "view", "--json", "number"], "gh pr view")
        return int(data["number"]), None
    if re.fullmatch(r"[0-9]+", arg):
        return int(arg), None
    if "/pull/" in arg:
        match = re.search(r"([^/]+)/([^/]+)/pull/([0-9]+)", arg)
        if not match or "{}/{}".format(match.group(1), match.group(2)).lower() != repo.lower():
            raise _Halt("PR URL is not for {}: {}".format(repo, arg))
        return int(match.group(3)), None
    name = _norm_path(arg).rsplit("/", 1)[-1]
    match = _TICKET_PREFIX.match(name)
    if not match:
        raise _Halt("spec path has no ticket id prefix: {}".format(arg))
    ticket = match.group(0)
    code, out, _ = _cmd(["gh", "pr", "view", "--json", "number,headRefName,title"])
    if code == 0:
        try:
            current = json.loads(_text(out))
        except ValueError:
            current = None
        if isinstance(current, dict) and ticket in (
                _unanchored(current.get("headRefName")), _unanchored(current.get("title"))):
            return int(current["number"]), ticket
    rows = _json(["gh", "pr", "list", "--state", "merged", "--search", ticket,
                  "--json", "number,title,headRefName", "--limit", _SEARCH_LIMIT],
                 "gh pr list")
    kept = [row["number"] for row in rows if isinstance(row, dict) and ticket in (
        _unanchored(row.get("headRefName")), _unanchored(row.get("title")))]
    if len(kept) != 1:
        listed = ", ".join("#{}".format(n) for n in kept) or "none"
        raise _Halt("{} merged PRs match {} ({}) - pass the PR number".format(
            len(kept), ticket, listed))
    return int(kept[0]), ticket


def _diff_patch_id(base: str, tip: str) -> str:
    diff = _cmd(["git", "diff", base, tip])
    if diff[0] != 0:
        raise _Halt("git diff {} {} failed: {}".format(base, tip, _text(diff[2]).strip()))
    code, out, err = _cmd(["git", "patch-id", "--stable"], input=diff[1])
    lines = _text(out).splitlines() if code == 0 else []
    fields = lines[0].split() if len(lines) == 1 else []
    if not fields or _bad_id(fields[0]):
        raise _Halt("git patch-id for {} {} gave no single id: {}".format(
            base, tip, _text(err).strip()))
    return fields[0]


def _verify(number: int, pr_head: str, landed: str, commits: int) -> dict:
    """Marker read and SHA checks. A mismatch is a warning, never a halt."""
    result = {"status": "skipped", "kind": None, "review": None, "warnings": [],
              "drift": [], "diff_base": landed + "^1"}
    try:
        found = _read_latest(number)
    except _ReadFailed as exc:
        raise _Halt("comment read failed: {}".format(exc)) from None
    if found is None:
        return result
    cid, _, line = found
    if line is None:
        result["status"] = "warning"
        result["warnings"].append("marker id={} is malformed; not compared".format(cid))
        return result
    fields = dict(field.split("=", 1) for field in line.split())
    head, base, recorded = fields["head"], fields["base"], fields["patch-id"]
    result["review"] = fields["review"]
    if head != pr_head:
        result["status"] = "warning"
        result["warnings"].append("PR head {} != recorded head {}".format(pr_head, head))
        return result
    single = _diff_patch_id(landed + "^1", landed)
    parents = len(_must(["git", "rev-list", "--parents", "-n", "1", landed],
                        "git rev-list --parents").split()) - 1
    range_id = None
    if parents == 1 and commits > 1 and single != recorded:
        range_id = _diff_patch_id("{}~{}".format(landed, commits), landed)
    code, kind = _decide(parents, commits, recorded, single, range_id)
    if code != 0:
        result["status"] = "warning"
        result["warnings"].append("patch-id mismatch: recorded {}, single {}, range {}".format(
            recorded, single, range_id or "n/a"))
        return result
    merge_base = "{}~{}".format(landed, commits) if kind == "match range" else landed + "^1"
    for oid in (base, head, landed):
        _must(["git", "cat-file", "-e", oid], "git cat-file -e {}".format(oid))
    _must(["git", "merge-base", "--is-ancestor", base, merge_base],
          "git merge-base --is-ancestor {} {}".format(base, merge_base))
    walked = _must(["git", "rev-list", "--reverse", "{}..{}".format(base, merge_base)],
                   "git rev-list").split()
    pr_paths = {p.replace("\\", "/") for p in _must(
        ["git", "diff", "--name-only", "{}...{}".format(base, head)],
        "git diff --name-only").splitlines() if p}
    touching = []
    subjects = []
    for sha in walked:
        paths = {p.replace("\\", "/") for p in _must(
            ["git", "diff-tree", "--first-parent", "-m", "--no-commit-id", "--name-only", "-r", sha],
            "git diff-tree {}".format(sha)).splitlines() if p}
        subject = _must(["git", "log", "-1", "--format=%s", sha], "git log").strip()
        subjects.append("{} {}".format(sha[:12], subject))
        shared = sorted(paths & pr_paths)
        if shared:
            touching.append("{} {} touches {}".format(sha[:12], subject, ", ".join(shared)))
    if touching:
        result["status"] = "warning"
        result["warnings"].append("base moved and these commits touch PR files: " + "; ".join(touching))
        return result
    result["status"] = "match"
    result["kind"] = kind
    result["drift"] = subjects
    result["diff_base"] = merge_base
    return result


def _checklist(body) -> list[str]:
    lines = []
    inside = False
    for line in (body if isinstance(body, str) else "").split("\n"):
        if line.endswith("\r"):
            line = line[:-1]
        if not inside:
            inside = line == "## Test plan"
            continue
        if line.startswith("## "):
            break
        if re.match(r"^\s*[-*] \[ \]\s+\S", line) and "Spec verdict:" not in line \
                and "Review gate:" not in line:
            lines.append(line)
    return lines


def _plane(ticket: str, number: int, unchecked: list[str]) -> dict:
    prefix = ticket.split("-", 1)[0]
    digest = hashlib.sha256("\n".join(unchecked).encode("utf-8")).hexdigest()
    plane = {"prefix": prefix, "target": "Done", "state_id": None, "project_id": None,
             "comment": None, "problem": None, "states": []}
    path = os.path.join(_config_dir(), "skills", "ship-spec", "states.json")
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        data = None
        plane["problem"] = "states.json unreadable at {}: {}".format(path, exc)
    entry = data.get(prefix) if isinstance(data, dict) else None
    if data is not None and not isinstance(entry, dict):
        plane["problem"] = "no states.json entry for prefix {}".format(prefix)
    states = entry.get("states") if isinstance(entry, dict) else None
    groups = entry.get("state_groups") if isinstance(entry, dict) else None
    states = states if isinstance(states, dict) else {}
    groups = groups if isinstance(groups, dict) else {}
    if unchecked and _PMC in states and _PMC in groups:
        plane["target"] = _PMC
    plane["states"] = sorted(states)
    plane["state_id"] = states.get(plane["target"])
    plane["project_id"] = entry.get("project_id") if isinstance(entry, dict) else None
    if not plane["problem"] and not plane["state_id"]:
        plane["problem"] = "state {} not in states.json for {}".format(plane["target"], prefix)
    if plane["target"] == _PMC:
        plane["comment"] = "Post-merge checklists for PR #{}:\n{}\nspec-land:checklist PR #{} {}".format(
            number, "\n".join(unchecked), number, digest)
    return plane


def _section(text: str, heading: str) -> list[str] | None:
    """Lines under the first exact heading, up to the next markdown heading."""
    body = None
    for line in text.splitlines():
        if _HEADING.match(line):
            if body is not None:
                break
            if line.strip() == heading:
                body = []
            continue
        if body is not None:
            body.append(line)
    return body


def _existing_dir(candidate: str) -> str | None:
    path = _norm_path(candidate.rstrip(".,;:"))
    if os.path.isdir(path):
        return path
    user = os.environ.get("USERNAME") or os.environ.get("USER")
    match = re.match(r"^(.*?/(?:Users|home)/)[^/]+(/.*)?$", path)
    if user and match:
        swapped = match.group(1) + user + (match.group(2) or "")
        if os.path.isdir(swapped):
            return swapped
    return None


def _wiki_path(text: str) -> str | None:
    wiki_lines = set(_section(text, "## Wiki") or [])
    for line in text.splitlines():
        # Any line that names the wiki, or any line under ## Wiki (such as Path:).
        if "wiki" not in line.lower() and line not in wiki_lines:
            continue
        for match in _ABS_PATH.finditer(line):
            # A path may hold spaces: try the longest run of words first.
            seg = re.split(r"[`'\"<>|()]", line[match.start():])[0]
            for end in reversed([word.end() for word in re.finditer(r"\S+", seg)]):
                found = _existing_dir(seg[:end])
                if found:
                    return found
    return None


def _instructions(landed: str, main: str) -> dict:
    sources = []
    if _cmd(["git", "cat-file", "-e", landed + ":CLAUDE.md"])[0] == 0:
        sources.append(("CLAUDE.md", _must(["git", "show", landed + ":CLAUDE.md"], "git show CLAUDE.md")))
    else:
        local = os.path.join(main, "CLAUDE.md")
        if os.path.isfile(local):
            with open(local, encoding="utf-8", errors="replace") as handle:
                sources.append(("CLAUDE.md (main checkout)", handle.read()))
    if _cmd(["git", "cat-file", "-e", landed + ":AGENTS.md"])[0] == 0:
        sources.append(("AGENTS.md", _must(["git", "show", landed + ":AGENTS.md"], "git show AGENTS.md")))
    held = {"wiki": None, "wiki_source": None, "slug": None, "slug_source": None,
            "command": None, "command_source": None, "command_warning": None}
    for name, text in sources:
        if held["wiki"] is None:
            found = _wiki_path(text)
            if found:
                held["wiki"], held["wiki_source"] = found, name
        if held["slug"] is None:
            for line in _section(text, "## Wiki") or []:
                if line.strip().startswith("Slug:"):
                    value = line.strip()[len("Slug:"):].strip()
                    if value:
                        held["slug"], held["slug_source"] = value, name
                    break
        if held["command_source"] is None:
            body = _section(text, "## Post-land command")
            if body is not None:
                held["command_source"] = name
                lines = [l.strip() for l in body
                         if l.strip() and not l.strip().startswith(("```", "~~~"))]
                if len(lines) == 1:
                    held["command"] = lines[0]
                else:
                    held["command_warning"] = "{} ## Post-land command has {} non-blank lines - skipped".format(
                        name, len(lines))
    return held


def _worktrees(main: str | None = None) -> list[dict]:
    argv = ["git"] + (["-C", main] if main else []) + ["worktree", "list", "--porcelain"]
    records = []
    for line in _must(argv, "git worktree list").splitlines():
        if line.startswith("worktree "):
            records.append({"path": _norm_path(line[len("worktree "):]), "branch": None})
        elif line.startswith("branch ") and records:
            records[-1]["branch"] = line[len("branch "):]
    if not records:
        raise _Halt("git worktree list returned no records")
    return records


def _default_branch(main: str) -> str | None:
    code, out, _ = _cmd(["git", "-C", main, "symbolic-ref", "refs/remotes/origin/HEAD"])
    if code == 0 and _text(out).strip():
        return _text(out).strip().rsplit("refs/remotes/origin/", 1)[-1]
    code, out, _ = _cmd(["git", "-C", main, "remote", "show", "origin"])
    if code == 0:
        match = re.search(r"HEAD branch: (\S+)", _text(out))
        if match:
            return match.group(1)
    return None


def _ticket(spec_id, ticket_arg, branch, title, number) -> tuple[str, str, str | None]:
    branch_id, title_id = _unanchored(branch), _unanchored(title)
    if spec_id:
        other = {i for i in (branch_id, title_id) if i and i != spec_id}
        note = "PR branch or title names {}".format(", ".join(sorted(other))) if other else None
        return spec_id, "spec path", note
    if ticket_arg:
        value = ticket_arg.strip().upper()
        if not _TICKET.match(value):
            raise _Halt("--ticket {} is not a ticket id".format(ticket_arg))
        return value, "operator", None
    if branch_id and title_id and branch_id != title_id:
        raise _NeedTicket(number, [branch_id, title_id])
    if branch_id and title_id:
        return branch_id, "branch and title", None
    if branch_id or title_id:
        return branch_id or title_id, "branch" if branch_id else "title", None
    raise _NeedTicket(number, [])


def _preflight_state(arg: str | None, ticket_arg: str | None) -> dict:
    repo = _repo()
    number, spec_id = _select(arg, repo)
    pr = _json(["gh", "pr", "view", str(number), "--json",
                "state,mergeCommit,mergedAt,baseRefOid,headRefOid,headRefName,body,commits,title,url"],
               "gh pr view {}".format(number))
    if pr.get("state") != "MERGED":
        raise _Halt("PR #{} is {}, not MERGED. spec-land does not merge.".format(number, pr.get("state")))
    landed = (pr.get("mergeCommit") or {}).get("oid")
    if _bad_id(landed):
        raise _Halt("PR #{} has no landed commit id".format(number))
    commits = len(pr["commits"]) if isinstance(pr.get("commits"), list) else 0
    ticket, source, note = _ticket(spec_id, ticket_arg, pr.get("headRefName"), pr.get("title"), number)
    _must(["git", "fetch", "origin"], "git fetch origin")
    _must(["git", "fetch", "origin", "pull/{}/head".format(number)], "git fetch origin pull/{}/head".format(number))
    verification = _verify(number, pr.get("headRefOid"), landed, commits)
    records = _worktrees()
    main = records[0]["path"]
    branch = pr.get("headRefName") or ""
    linked = [r["path"] for r in records[1:] if r["branch"] == "refs/heads/" + branch]
    unchecked = _checklist(pr.get("body"))
    held = _instructions(landed, main)
    default = _default_branch(main)
    if not default:
        fast_forward = "skipped (default branch unknown)"
    elif records[0]["branch"] != "refs/heads/" + default:
        fast_forward = "skipped (main checkout is on {}, not {})".format(
            (records[0]["branch"] or "a detached HEAD").replace("refs/heads/", ""), default)
    elif _cmd(["git", "-C", main, "status", "--porcelain"])[1].strip():
        fast_forward = "skipped (main checkout has uncommitted changes)"
    else:
        fast_forward = "will run"
    return {
        "version": _STATE_VERSION, "repo": repo, "main": main,
        "pr": {"number": number, "url": pr.get("url"), "title": pr.get("title") or "",
               "merged_at": pr.get("mergedAt"), "head": pr.get("headRefOid"),
               "base": pr.get("baseRefOid"), "landed": landed, "branch": branch,
               "commits": commits},
        "ticket": ticket, "ticket_source": source, "ticket_note": note,
        "spec_path": arg if spec_id else None,
        "verification": verification,
        "checklist": unchecked,
        "plane": _plane(ticket, number, unchecked),
        "wiki": {"path": held["wiki"], "source": held["wiki_source"],
                 "slug": held["slug"], "slug_source": held["slug_source"]},
        "post_land": {"command": held["command"], "source": held["command_source"],
                      "warning": held["command_warning"]},
        "worktrees": linked, "default_branch": default, "fast_forward": fast_forward,
    }


def _confirmation(state: dict) -> str:
    pr, v, plane, wiki, post = (state["pr"], state["verification"], state["plane"],
                                state["wiki"], state["post_land"])
    rows = ["PR: #{} {}".format(pr["number"], pr["url"]),
            "State: MERGED at {}".format(pr["merged_at"]),
            "Ticket: {} ({})".format(state["ticket"], state["ticket_source"])]
    if state["ticket_note"]:
        rows.append("Ticket note: " + state["ticket_note"])
    if v["status"] == "match":
        rows.append("SHA: match ({}) review={}".format(v["kind"], v["review"]))
    elif v["status"] == "skipped":
        rows.append("SHA: no marker - verification skipped")
    else:
        rows.append("SHA: WARNING" + (" review={}".format(v["review"]) if v["review"] else ""))
        rows.extend("  - " + w for w in v["warnings"])
    rows.append("A match means the landed code is the recorded code, not that it was reviewed.")
    if v["drift"]:
        rows.append("Base drift (clear of PR files): " + "; ".join(v["drift"]))
    diff = "Filemap diff: {} {}".format(v["diff_base"], pr["landed"])
    if v["status"] != "match" and pr["commits"] > 1:
        diff += " (landed first parent; may omit earlier rebased commits)"
    rows.append(diff)
    if plane["problem"]:
        rows.append("Plane: manual - {} (target {})".format(plane["problem"], plane["target"]))
    else:
        rows.append("Plane: {} ({})".format(plane["target"], plane["state_id"]))
    rows.append("Unchecked:")
    rows.extend(state["checklist"] or ["  none"])
    if plane["comment"]:
        rows.append("Checklist comment:")
        rows.extend("  " + line for line in plane["comment"].split("\n"))
    if wiki["path"]:
        rows.append("Wiki: {} from {}; log on; filemap {}".format(
            wiki["path"], wiki["source"],
            "on (slug {} from {})".format(wiki["slug"], wiki["slug_source"]) if wiki["slug"] else "off (no slug)"))
    else:
        rows.append("Wiki: none configured")
    if post["command"]:
        rows.append("Post-land command: {} from {}".format(post["command"], post["source"]))
    else:
        rows.append("Post-land command: " + (post["warning"] or "none declared"))
    rows.append("Worktree: " + (", ".join(state["worktrees"]) or "no worktree"))
    rows.append("Branch: {} (local and remote)".format(pr["branch"]))
    rows.append("Fast-forward: " + state["fast_forward"])
    if v["status"] == "warning":
        rows.append("Reply land anyway to land {} despite the warnings above.".format(state["ticket"]))
    else:
        rows.append("Reply yes to land {}.".format(state["ticket"]))
    return "\n".join(rows)


def _preflight(arg: str | None, ticket_arg: str | None) -> int:
    try:
        state = _preflight_state(arg, ticket_arg)
    except _NeedTicket as exc:
        print("NEEDS TICKET: PR #{} - candidates: {}".format(
            exc.number, ", ".join(exc.candidates) or "none"))
        print("Ask the operator for the id, then run: land_check.py preflight {} --ticket <ID>".format(exc.number))
        return 4
    except _Halt as exc:
        print("HALT: {}".format(exc))
        return 1
    print(_confirmation(state))
    print(_STATE_PREFIX + json.dumps(state, ensure_ascii=True, separators=(",", ":")))
    return 0


_STATE_KEYS = ("main", "pr", "ticket", "verification", "wiki", "post_land",
               "default_branch", "plane", "checklist")


def _load_state(path: str) -> dict:
    try:
        with open(_norm_path(path), encoding="utf-8") as handle:
            text = handle.read().strip()
    except OSError as exc:
        raise _Halt("state file: {}".format(exc)) from None
    if text.startswith(_STATE_PREFIX):
        text = text[len(_STATE_PREFIX):]
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise _Halt("state file is not JSON: {}".format(exc)) from None
    if not isinstance(data, dict) or data.get("version") != _STATE_VERSION:
        raise _Halt("state file is not version {}".format(_STATE_VERSION))
    missing = [key for key in _STATE_KEYS if key not in data]
    if missing:
        raise _Halt("state file lacks {}".format(", ".join(missing)))
    return data


def _log_date(log_path: str) -> str:
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    try:
        with open(log_path, encoding="utf-8", errors="replace") as handle:
            match = _LOG_DATE.search(handle.read())
    except OSError:
        return today
    return max(today, match.group(1)) if match else today


def _write_log(state: dict) -> bool:
    pr = state["pr"]
    log = state["wiki"]["path"] + "/log.md"
    script = os.path.join(_config_dir(), "skills", "spec-close", "scripts", "prepend_log_entry.py")
    if not os.path.isfile(script):
        print("log.md: NOT written (prepend_log_entry.py not found at {} - run python sync.py install)".format(script))
        return False
    prefix = state["ticket"].split("-", 1)[0]
    guard = "merge | {} \u2014 {} PR #{}:".format(prefix, state["ticket"], pr["number"])
    title = " ".join(pr["title"].split()) or state["ticket"]
    entry = "## [{}] {} {} (`{}`)\n\nMerged at: {}\nLanded: {}\n".format(
        _log_date(log), guard, title, pr["landed"][:12], pr["merged_at"], pr["landed"])
    code, out, err = _cmd([sys.executable, script, log, "--guard", guard], input=entry.encode("utf-8"))
    outcome = next((line.split("=", 1)[1] for line in _text(out).splitlines()
                    if line.startswith("prepend_log_entry_outcome=")), None)
    if code == 0:
        print("log.md: {}".format(outcome or "written"))
        return True
    if code == 1:
        print("log.md: entry already present - skipped")
        return True
    print("log.md: NOT written (prepend_log_entry.py exit {}): {}".format(code, _text(err).strip()))
    return False


def _filemap_rows(lines: list[str], rows: list[str], number: int) -> tuple[list[str], list[str]]:
    def find(path):
        heading = "### `{}`".format(path)
        for index, line in enumerate(lines):
            if line.rstrip("\r\n") == heading:
                return index
        return None

    notes = []
    for row in rows:
        parts = row.split("\t")
        status = parts[0][:1]
        if status == "D" and len(parts) >= 2:
            start = find(parts[1])
            if start is None:
                notes.append("D {}: no heading - skipped".format(parts[1]))
                continue
            end = start + 1
            while end < len(lines) and not _HEADING.match(lines[end]):
                end += 1
            del lines[start:end]
            notes.append("D {}: section removed".format(parts[1]))
        elif status == "R" and len(parts) >= 3:
            old, new = find(parts[1]), find(parts[2])
            if old is not None and new is None:
                ending = lines[old][len(lines[old].rstrip("\r\n")):]
                lines[old] = "### `{}`{}".format(parts[2], ending or "\n")
                notes.append("R {} -> {}: renamed".format(parts[1], parts[2]))
            else:
                notes.append("R {} -> {}: skipped".format(parts[1], parts[2]))
        elif status == "A" and len(parts) >= 2:
            if find(parts[1]) is not None:
                continue
            leaf = parts[1].rsplit("/", 1)[-1]
            is_test = re.fullmatch(r"test_.*\.py|.*\.test\.(ts|js)", leaf) is not None
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"
            lines.extend(["\n", "### `{}`\n".format(parts[1]),
                          "- **Purpose:** {} PR #{}.\n".format(
                              "Test added in" if is_test else "Added in", number)])
            notes.append("A {}: stub added".format(parts[1]))
        elif status == "M":
            notes.append("M {}: not filemap-relevant".format(parts[-1]))
        else:
            notes.append("{}: not edited".format(row))
    return lines, notes


def _write_filemap(state: dict) -> bool:
    wiki, pr = state["wiki"], state["pr"]
    if not wiki.get("slug"):
        print("filemap: off (no slug)")
        return True
    path = "{}/projects/{}/filemap.md".format(wiki["path"], wiki["slug"])
    if not os.path.isfile(path):
        print("filemap: missing file {} - skipped".format(path))
        return True
    # -z: git leaves unusual pathnames unquoted, NUL-separated.
    code, out, err = _cmd(["git", "-C", state["main"], "diff", "--name-status", "-z",
                           state["verification"]["diff_base"], pr["landed"]])
    if code != 0:
        print("filemap: NOT written (git diff --name-status failed: {})".format(_text(err).strip()))
        return False
    with open(path, encoding="utf-8", newline="") as handle:
        before = handle.read()
    fields, rows, index = _text(out).split("\0"), [], 0
    while index < len(fields) and fields[index]:
        width = 3 if fields[index][:1] in "RC" else 2
        rows.append("\t".join(fields[index:index + width]))
        index += width
    lines, notes = _filemap_rows(before.splitlines(keepends=True), rows, pr["number"])
    for note in notes:
        print("filemap: " + note)
    after = "".join(lines)
    if after == before:
        print("filemap: unchanged")
        return True
    fd, temp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".filemap-", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
        handle.write(after)
    os.replace(temp, path)
    print("filemap: written")
    return True


def _wiki(state_path: str) -> int:
    try:
        state = _load_state(state_path)
    except _Halt as exc:
        print("HALT: {}".format(exc))
        return 1
    if not state["wiki"].get("path"):
        print("wiki: none configured")
        return 0
    ok = _write_log(state)
    ok = _write_filemap(state) and ok
    return 0 if ok else 1


def _shell(command: str, cwd: str) -> int:
    sys.stdout.flush()
    try:
        return subprocess.run(command, shell=True, cwd=cwd, stdin=subprocess.DEVNULL,
                              timeout=_POST_LAND_TIMEOUT, env={**os.environ, **_CHILD_ENV}).returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("post-land command: could not run: {}".format(exc))
        return 127


def _cleanup(state_path: str) -> int:
    try:
        state = _load_state(state_path)
    except _Halt as exc:
        print("HALT: {}".format(exc))
        return 1
    main, pr, default = state["main"], state["pr"], state["default_branch"]
    branch, head, ref = pr["branch"], pr["head"], "refs/heads/" + pr["branch"]
    matched = state["verification"]["status"] == "match"
    failed = False

    def git(*args):
        return _cmd(["git", "-C", main, *args])

    try:
        records = _worktrees(main)
    except _Halt as exc:
        print("worktree: NOT inspected ({}) - branches kept".format(exc))
        records, failed = [], True
    deletable = bool(records) and bool(branch)
    if branch and branch == default:
        print("branches: kept ({} is the default branch)".format(branch))
        deletable = False
    linked = [r["path"] for r in records[1:] if r["branch"] == ref]
    in_main = bool(records) and records[0]["branch"] == ref
    if len(linked) > 1:
        print("worktree: {} linked checkouts kept, with their branches: {}".format(len(linked), ", ".join(linked)))
        deletable = False
    elif linked:
        code, out, err = _cmd(["git", "-C", linked[0], "status", "--porcelain"])
        if code != 0:
            print("worktree: NOT inspected ({}) - kept with its branches".format(_text(err).strip()))
            deletable, failed = False, True
        elif out.strip():
            print("worktree: dirty - kept, with its local and remote branch: {}".format(linked[0]))
            deletable = False
        else:
            code, _, err = git("worktree", "remove", linked[0])
            if code != 0:
                print("worktree: NOT removed ({}) - branches kept".format(_text(err).strip()))
                deletable, failed = False, True
            else:
                print("worktree: removed {}".format(linked[0]))
    elif records:
        print("worktree: no worktree")

    if deletable and in_main:
        print("local branch: kept (checked out in the main checkout)")
    elif deletable:
        code, out, err = git("rev-parse", "--verify", "-q", ref)
        tip = _text(out).strip()
        if code != 0 and not tip and not err.strip():
            print("local branch: already gone")
        elif code != 0 or _bad_id(tip):
            print("local branch: kept (rev-parse failed: {})".format(_text(err).strip()))
            failed = True
        else:
            code, out, err = git("rev-list", "--count", "{}..{}".format(head, tip))
            count = _text(out).strip()
            if code != 0 or not count.isdigit():
                print("local branch: kept (rev-list failed: {})".format(_text(err).strip()))
                failed = True
            elif int(count) > 0:
                print("local branch: kept ({} commits not in the PR head)".format(count))
            elif git("branch", "-d", branch)[0] == 0:
                print("local branch: deleted")
            elif matched and tip == head:
                code, _, err = git("branch", "-D", branch)
                if code == 0:
                    print("local branch: deleted (-D; squash or rebase, tip matched the recorded head)")
                else:
                    print("local branch: NOT deleted ({})".format(_text(err).strip()))
                    failed = True
            else:
                print("local branch: kept (git branch -d refused; -D needs a SHA match)")

    if deletable:
        code, out, err = git("ls-remote", "--heads", "origin", branch)
        tips = [line.split()[0] for line in _text(out).splitlines()
                if line.split() and line.split()[-1] == ref]
        if code != 0:
            print("remote branch: lookup failed - skipped ({})".format(_text(err).strip()))
            failed = True
        elif not tips:
            print("remote branch: already deleted")
        elif tips[0] != head:
            print("remote branch: skipped (tip {} is not the PR head)".format(tips[0]))
        else:
            code, _, err = git("push", "--force-with-lease={}:{}".format(ref, head), "origin", "--delete", branch)
            if code == 0:
                print("remote branch: deleted")
            else:
                print("remote branch: skipped (lease rejected or push failed: {})".format(_text(err).strip()))

    contains = False
    main_ref = records[0]["branch"] if records else None
    if not default:
        print("fast-forward: skipped (default branch unknown)")
    elif main_ref != "refs/heads/" + default:
        print("fast-forward: skipped (main checkout is not on {})".format(default))
    else:
        code, out, err = git("status", "--porcelain")
        if code != 0:
            print("fast-forward: skipped (git status failed: {})".format(_text(err).strip()))
            failed = True
        elif out.strip():
            print("fast-forward: skipped (main checkout has uncommitted changes)")
        else:
            code, _, err = git("merge", "--ff-only", "origin/" + default)
            if code != 0:
                print("fast-forward: failed ({})".format(_text(err).strip()))
                failed = True
            elif git("merge-base", "--is-ancestor", pr["landed"], "HEAD")[0] == 0:
                print("fast-forward: done")
                contains = True
            else:
                print("fast-forward: done, but the main checkout does not contain the landed commit")
    command = state["post_land"].get("command")
    if not command:
        print("post-land command: none declared")
    elif not contains:
        print("post-land command: skipped (main checkout does not hold the landed commit)")
    else:
        code = _shell(command, main)
        print("post-land command: exit {}".format(code))
        failed = failed or code != 0
    return 1 if failed else 0


def _run(argv: list[str]) -> int:
    args = _parser().parse_args(argv)
    # latest, post, preflight, wiki and cleanup return before the stdin read:
    # they must not block on a terminal, and their callers pass no input.
    if args.command == "latest":
        return _latest(args.number)
    if args.command == "post":
        return _post(args.number, args.review, args.no_push)
    if args.command == "preflight":
        return _preflight(args.target, args.ticket)
    if args.command == "wiki":
        return _wiki(args.state)
    if args.command == "cleanup":
        return _cleanup(args.state)
    text = sys.stdin.buffer.read().decode("utf-8")
    if args.command == "parse":
        code, line = _parse_marker(text)
        if code == 2:
            print("malformed marker", file=sys.stderr)
        elif line:
            print(line)
        return code
    if args.command == "decide":
        code, line = _decide(
            args.parents, args.pr_commits, args.recorded, args.single, args.range_id)
        if code == 2:
            print("bad arguments", file=sys.stderr)
        elif line:
            print(line)
        return code
    code, paths = _overlap(text)
    if code == 0:
        print("clear")
    elif code == 1:
        for path in paths:
            print(path)
    else:
        print("overlap input has no -- separator", file=sys.stderr)
    return code


def main(argv: list[str]) -> int:
    # Windows stdout is cp1252 when piped. The precedent reconfigures before
    # any write so a later message cannot escape as a crash (exit 1).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass
    try:
        return _run(argv)
    except (KeyboardInterrupt, SystemExit):
        # argparse raises SystemExit(0) for --help and SystemExit(2) for a
        # usage error. Turning those into 3 would hide a bad invocation.
        raise
    except BaseException as exc:  # noqa: BLE001 - exit 1 is a documented outcome
        sys.stderr.write(
            "unexpected failure: {}: {}\n".format(type(exc).__name__, exc))
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
