#!/usr/bin/env python3
"""Classify a spec-land marker, patch-id decision, or path overlap; read and
post the SHA marker on a PR.

Usage:
    land_check.py parse
    land_check.py decide --parents N --pr-commits N --recorded ID --single ID [--range ID]
    land_check.py overlap
    land_check.py latest <N>
    land_check.py post <N> --review <passed|skipped|inconclusive|not-run> [--no-push]

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
       "SHA marker: already current (head <head>)"
    1  "SHA marker: NOT posted (<reason>)", then the body when it was built

Only parse, decide and overlap read stdin; main() decodes it as strict UTF-8.
latest and post never read stdin. Any other failure exits 3, so exit 1
stays the documented outcome. SystemExit and KeyboardInterrupt propagate:
argparse usage errors stay exit 2.

Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime
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


def _run(argv: list[str]) -> int:
    args = _parser().parse_args(argv)
    # latest and post return before the stdin read: they must not block on a
    # terminal, and their callers pass no input.
    if args.command == "latest":
        return _latest(args.number)
    if args.command == "post":
        return _post(args.number, args.review, args.no_push)
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
