#!/usr/bin/env python3
"""Commit this ticket's wiki log entries and named files in one local commit.

Usage:
    commit_wiki.py <wiki-root> --ticket <TICKET-ID> [--file <path>]...

The commit is built in a private index from HEAD. The branch moves only by a
compare-and-swap from that HEAD, so a concurrent commit is left untouched.
The working tree stays untouched. The real index is refreshed only after the
commit, and only for paths that are still unstaged. A commit that is not made
prints `wiki commit: not made - <reason>` and a retry line. The script never
pushes, stashes, resets, checks out, or prompts.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

TICKET_RE = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")
HEADING_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] ")
# Action and ticket are the fields after the date. The title is not searched.
_ENTRY_RE = re.compile(
    r"^## \[\d{4}-\d{2}-\d{2}\] (merge|close) \| "
    r"([A-Z][A-Z0-9]*) \u2014 ([A-Z][A-Z0-9]*-[0-9]+)"
    r"( PR #([0-9]+))?(?=:)"
)
_BOM = b"\xef\xbb\xbf"
_REGULAR_MODES = (b"100644", b"100755")
DROPPED_ENV = {
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE", "GIT_PREFIX",
}
IN_PROGRESS = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD")
SEQUENCER_DIRS = ("sequencer", "rebase-merge", "rebase-apply")


class NotMade(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _reconfigure() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass


def _base_env() -> dict:
    env = {key: value for key, value in os.environ.items() if key not in DROPPED_ENV}
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_LITERAL_PATHSPECS"] = "1"
    return env


def _collapse(data: bytes) -> str:
    return " ".join(data.decode("utf-8", "replace").split())


def _git(root: str, args: list, env: dict, input_bytes: bytes | None = None):
    try:
        return subprocess.run(
            ["git", "-C", root, *args],
            env=env,
            input=input_bytes,
            stdin=None if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        raise NotMade("git timed out") from exc
    except FileNotFoundError as exc:
        raise NotMade("git is not on PATH") from exc
    except OSError as exc:
        raise NotMade("git failed: {}".format(exc)) from exc


def _require(proc, what: str):
    if proc.returncode != 0:
        detail = _collapse(proc.stderr + proc.stdout) or what
        raise NotMade(detail)
    return proc


def _forward(path: str) -> str:
    return path.replace("\\", "/")


def _quote_arg(text: str) -> str:
    escaped = (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("$", "\\$")
        .replace("`", "\\`")
    )
    return '"{}"'.format(escaped)


def _retry(root: str, ticket: str, files: list) -> str:
    parts = [
        _quote_arg(_forward(sys.executable)),
        _quote_arg(_forward(os.path.abspath(__file__))),
        _quote_arg(_forward(root)),
        "--ticket", ticket,
    ]
    for path in files:
        parts.append("--file")
        parts.append(_quote_arg(_forward(path)))
    return "To retry: " + " ".join(parts)


def _not_made(root: str, ticket: str, files: list, reason: str) -> None:
    print("wiki commit: not made - {}".format(reason))
    print(_retry(root, ticket, files))


def _refresh_message(root: str, short: str, detail: str, paths: list) -> str:
    shown = " ".join(_quote_arg(":(literal)" + _forward(path)) for path in paths)
    return (
        'wiki commit: {} - made, but the wiki index was not refreshed ({}): '
        'run git -C {} reset -q -- {}'
    ).format(short, detail or "git failed", _quote_arg(_forward(root)), shown)


def _line_spans(data: bytes) -> list:
    spans = []
    start = 0
    index = 0
    size = len(data)
    while index < size:
        if data.startswith(b"\r\n", index):
            spans.append((start, index, index + 2))
            index += 2
            start = index
        elif data[index:index + 1] in (b"\n", b"\r"):
            spans.append((start, index, index + 1))
            index += 1
            start = index
        else:
            index += 1
    if start < size or not spans:
        spans.append((start, size, size))
    return spans


def _split_bom(data: bytes):
    if data.startswith(_BOM):
        return _BOM, data[len(_BOM):]
    return b"", data


def _parse_log(data: bytes):
    """Return (preamble bytes, blocks). A block is heading, raw bytes, line texts."""
    spans = _line_spans(data)
    texts = []
    heading_at = []
    for index, (left, right, _) in enumerate(spans):
        text = data[left:right].decode("utf-8")
        texts.append(text)
        if HEADING_RE.match(text):
            heading_at.append(index)
    if not heading_at:
        return data, []
    preamble = data[:spans[heading_at[0]][0]]
    blocks = []
    for number, start in enumerate(heading_at):
        end = heading_at[number + 1] if number + 1 < len(heading_at) else len(spans)
        raw = data[spans[start][0]:spans[end - 1][2]]
        blocks.append((texts[start], raw, texts[start:end]))
    return preamble, blocks


def _lifecycle(heading: str):
    """Identity of a merge or close heading, or None.

    A merge's identity includes its pull request number. The title is ignored,
    so a changed title is the same entry.
    """
    match = _ENTRY_RE.match(heading)
    if match is None:
        return None
    action, prefix, ticket, pr = match.group(1), match.group(2), match.group(3), match.group(5)
    if prefix != ticket.split("-", 1)[0]:
        return None
    if action == "merge":
        if not pr:
            return None
        return ("merge", ticket, pr)
    if pr:
        return None
    return ("close", ticket, "")


def _is_ours(heading: str, seen: set, ticket: str) -> bool:
    ident = _lifecycle(heading)
    if ident is None or ident in seen or ident[1] != ticket:
        return False
    return True


def _encode_lines(lines: list, newline: bytes) -> bytes:
    return b"".join(line.encode("utf-8") + newline for line in lines)


def _with_blank_line(text: bytes, newline: bytes) -> bytes:
    body = text[len(_BOM):] if text.startswith(_BOM) else text
    if not body:
        return text
    if not text.endswith(newline):
        text += newline
    if not text.endswith(newline + newline):
        text += newline
    return text


def _compose(head_bytes: bytes, work_bytes: bytes, ticket: str):
    """Return (composed bytes, entry count), or (None, 0) when log.md stays out."""
    bom, head_body = _split_bom(head_bytes)
    _, work_body = _split_bom(work_bytes)
    try:
        head_preamble, head_blocks = _parse_log(head_body)
        _, work_blocks = _parse_log(work_body)
    except UnicodeDecodeError as exc:
        raise NotMade("log.md is not UTF-8") from exc
    seen = set()
    for block in head_blocks:
        ident = _lifecycle(block[0])
        if ident is not None:
            seen.add(ident)
    first = {}
    for index, block in enumerate(head_blocks):
        first.setdefault(block[0], index)
    newline = b"\r\n" if b"\r\n" in head_body else b"\n"
    before = {index: [] for index in range(len(head_blocks))}
    pending = []
    for heading, _, lines in work_blocks:
        if _is_ours(heading, seen, ticket):
            pending.append(_encode_lines(lines, newline))
        elif heading in first:
            before[first[heading]].extend(pending)
            pending = []
    if not any(before.values()) and not pending:
        return None, 0
    count = sum(len(parts) for parts in before.values()) + len(pending)
    pieces = [bom, head_preamble]
    for index, block in enumerate(head_blocks):
        pieces.extend(before[index])
        pieces.append(block[1])
    composed = b"".join(pieces)
    if pending:
        composed = _with_blank_line(composed, newline) + b"".join(pending)
    return composed, count


def _normalize(root: str, raw: str, root_real: str) -> str | None:
    text = _forward(raw)
    full = text if os.path.isabs(text) else os.path.join(root, text)
    try:
        resolved = os.path.realpath(full)
    except OSError as exc:
        raise NotMade("{} is not a file inside the wiki".format(text)) from exc
    root_real = os.path.realpath(root_real)
    if os.path.normcase(resolved) == os.path.normcase(os.path.join(root_real, "log.md")):
        return None
    root_key = os.path.normcase(os.path.abspath(root_real))
    file_key = os.path.normcase(os.path.abspath(resolved))
    try:
        inside = os.path.commonpath([root_key, file_key]) == root_key
    except ValueError:
        inside = False
    if not inside or not os.path.isfile(resolved) or os.path.islink(resolved):
        raise NotMade("{} is not a file inside the wiki".format(text))
    relative = os.path.relpath(resolved, root_real)
    return _forward(relative)


def _entry_id(data: bytes):
    """Return (mode, object id) for one exact index or tree entry."""
    records = [record for record in data.split(b"\0") if record]
    if not records:
        return None
    if len(records) != 1:
        return ("multiple", data)
    head, _, _path = records[0].partition(b"\t")
    parts = head.split()
    blob = None
    for part in parts[1:]:
        if len(part) >= 40 and all(chr(c) in "0123456789abcdef" for c in part.lower()):
            blob = part
            break
    if not parts or blob is None:
        return ("bad", data)
    return (parts[0], blob)


def _exact_path_changed(root: str, env: dict, base: str, path: str) -> bool:
    index = _require(
        _git(root, ["ls-files", "-s", "-z", "--", path], env), "git ls-files failed")
    head = _require(
        _git(root, ["ls-tree", "-z", base, "--", path], env), "git ls-tree failed")
    return _entry_id(index.stdout) != _entry_id(head.stdout)


def _changed_paths(root: str, env: dict, base: str, tree: str) -> list:
    diff = _require(_git(root, [
        "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "--no-renames",
        base, tree,
    ], env), "git diff-tree failed")
    paths = []
    for record in diff.stdout.split(b"\0"):
        if record:
            paths.append(record.decode("utf-8", "replace"))
    return paths


def _blob_at(root: str, env: dict, tree: str, path: str):
    listed = _require(_git(root, ["ls-tree", "-z", tree, "--", path], env), "git ls-tree failed")
    found = _entry_id(listed.stdout)
    if found is None or found[0] in ("multiple", "bad"):
        return None
    return found[1]


def _refuse_in_progress(root: str, env: dict) -> None:
    for name in IN_PROGRESS:
        found = _git(root, ["rev-parse", "-q", "--verify", name], env)
        if found.returncode == 0 and found.stdout.strip():
            raise NotMade("the wiki has a merge, cherry-pick or revert in progress")
    unmerged = _require(_git(root, ["ls-files", "-u"], env), "git ls-files failed")
    if unmerged.stdout.strip():
        raise NotMade("the wiki index has unmerged entries")
    git_dir = _require(
        _git(root, ["rev-parse", "--absolute-git-dir"], env), "git rev-parse failed")
    directory = git_dir.stdout.decode("utf-8", "replace").strip()
    for name in SEQUENCER_DIRS:
        if os.path.isdir(os.path.join(directory, name)):
            raise NotMade("the wiki has a sequencer or rebase in progress")


def _read_log(root: str, env: dict, ticket: str):
    """Return (composed, count, blob prelude) or (None, 0, None) when log stays out."""
    log_path = os.path.join(root, "log.md")
    if not os.path.lexists(log_path):
        return None, 0
    if os.path.islink(log_path):
        raise NotMade("log.md is not a regular file")
    try:
        info = os.lstat(log_path)
    except OSError as exc:
        raise NotMade("log.md is not a regular file") from exc
    if not stat.S_ISREG(info.st_mode):
        raise NotMade("log.md is not a regular file")
    listed = _require(_git(root, ["ls-tree", "-z", "HEAD", "--", "log.md"], env),
                      "could not read HEAD's log.md")
    found = _entry_id(listed.stdout)
    if found is None:
        head_bytes = b""
    elif found[0] in ("multiple", "bad") or found[0] not in _REGULAR_MODES:
        raise NotMade("HEAD's log.md is not a regular file")
    else:
        blob = _git(root, ["cat-file", "blob", "HEAD:log.md"], env)
        if blob.returncode != 0:
            raise NotMade(
                _collapse(blob.stderr + blob.stdout) or "could not read HEAD's log.md")
        head_bytes = blob.stdout
    try:
        with open(log_path, "rb") as handle:
            work_bytes = handle.read()
    except OSError as exc:
        raise NotMade("log.md is not a regular file") from exc
    return _compose(head_bytes, work_bytes, ticket)


def _log_mode(root: str, env: dict) -> str:
    listed = _require(
        _git(root, ["ls-tree", "-z", "HEAD", "--", "log.md"], env), "git ls-tree failed")
    found = _entry_id(listed.stdout)
    if found is None:
        return "100644"
    if found[0] in _REGULAR_MODES:
        return found[0].decode("ascii")
    raise NotMade("HEAD's log.md is not a regular file")


def _run_pre_commit(root: str, env: dict) -> None:
    hook = _git(root, ["hook", "run", "--ignore-missing", "pre-commit"], env)
    if hook.returncode == 0:
        return
    detail = _collapse(hook.stderr + hook.stdout)
    lowered = detail.lower()
    if hook.returncode == 129 or "not a git command" in lowered or "unknown option" in lowered:
        raise NotMade("git is too old to run the pre-commit hook")
    raise NotMade(detail or "pre-commit hook failed")


def _build(root: str, ticket: str, file_args: list):
    """Check the wiki and build the candidate tree. Does not publish it.

    Returns None when there is nothing to commit, otherwise a dict the caller
    can publish. Tests move the branch between this and `_publish`.
    """
    env = _base_env()
    if not os.path.isdir(root):
        raise NotMade("{} is not the top of a git work tree".format(root))
    prefix = _git(root, ["rev-parse", "--show-prefix"], env)
    if prefix.returncode != 0 or prefix.stdout.strip():
        raise NotMade("{} is not the top of a git work tree".format(root))
    head_ref = _git(root, ["symbolic-ref", "-q", "HEAD"], env)
    if head_ref.returncode != 0:
        raise NotMade("the wiki is on a detached HEAD")
    branch = head_ref.stdout.decode().strip()
    current = _git(root, ["rev-parse", "-q", "--verify", "HEAD"], env)
    if current.returncode != 0 or not current.stdout.strip():
        raise NotMade("the wiki has no commit yet")
    base = current.stdout.decode().strip()
    _refuse_in_progress(root, env)
    files = []
    seen = set()
    root_real = os.path.realpath(root)
    for raw in file_args:
        relative = _normalize(root, raw, root_real)
        if relative is None or relative in seen:
            continue
        seen.add(relative)
        files.append(relative)
    staged = _git(root, ["diff", "--cached", "--quiet", "--", "log.md", *files], env)
    if staged.returncode == 1:
        names = _git(root, ["diff", "--cached", "--name-only", "--", "log.md", *files], env)
        if names.returncode != 0:
            raise NotMade(_collapse(names.stderr + names.stdout) or "git diff failed")
        listed = [line for line in names.stdout.decode("utf-8", "replace").splitlines() if line]
        raise NotMade("already staged in the wiki: {}".format(", ".join(listed)))
    if staged.returncode != 0:
        raise NotMade(_collapse(staged.stderr + staged.stdout) or "git diff failed")
    composed, count = _read_log(root, env, ticket)
    index_dir = None
    try:
        index_dir = tempfile.mkdtemp(prefix="commit-wiki-")
        private = dict(env)
        private["GIT_INDEX_FILE"] = os.path.join(index_dir, "index")
        _require(_git(root, ["read-tree", "HEAD"], private), "git read-tree failed")
        composed_blob = None
        if composed is not None:
            hashed = _require(
                _git(root, ["hash-object", "-w", "--stdin"], private, composed),
                "git hash-object failed")
            composed_blob = hashed.stdout.decode().strip().encode("ascii")
            mode = _log_mode(root, private)
            _require(_git(
                root,
                ["update-index", "--add", "--cacheinfo",
                 "{},{},log.md".format(mode, composed_blob.decode("ascii"))],
                private), "git update-index failed")
        if files:
            _require(_git(root, ["add", "--", *files], private), "git add failed")
        quiet = _git(root, ["diff", "--cached", "--quiet"], private)
        if quiet.returncode == 0:
            return None
        if quiet.returncode != 1:
            raise NotMade(_collapse(quiet.stderr + quiet.stdout) or "git diff failed")
        allowed = []
        shown = []
        if composed is not None:
            allowed.append("log.md")
            shown.append("log.md ({} entries)".format(count))
        for path in files:
            if _exact_path_changed(root, private, base, path):
                allowed.append(path)
                shown.append(path)
        _run_pre_commit(root, private)
        tree = _require(_git(root, ["write-tree"], private), "git write-tree failed")
        tree_id = tree.stdout.decode().strip()
        actual = _changed_paths(root, private, base, tree_id)
        if set(actual) != set(allowed):
            names = sorted(set(actual) - set(allowed)) or sorted(set(allowed) - set(actual))
            raise NotMade("unexpected path: {}".format(", ".join(names)))
        if composed_blob is not None and _blob_at(root, private, tree_id, "log.md") != composed_blob:
            raise NotMade("unexpected path: log.md")
        return {
            "base": base,
            "branch": branch,
            "tree": tree_id,
            "paths": allowed,
            "shown": shown,
            "message": "close({}): wiki harvest from {}".format(ticket.lower(), ticket),
        }
    finally:
        if index_dir:
            shutil.rmtree(index_dir, ignore_errors=True)


def _report_published(root: str, env: dict, new_commit: str, candidate: dict) -> int:
    short = _git(root, ["rev-parse", "--short", new_commit], env)
    problems = []
    if short.returncode != 0 or not short.stdout.decode().strip():
        short_id = new_commit
        detail = "could not read the short hash"
        extra = _collapse(short.stderr + short.stdout)
        if extra:
            detail = detail + ": " + extra
        problems.append(detail)
    else:
        short_id = short.stdout.decode().strip()
    skipped = []
    # Compare with the parent, not the new HEAD. A clean index still matches the
    # parent; a path staged after the early check does not.
    base = candidate["base"]
    for path in candidate["paths"]:
        staged = _git(root, ["diff", "--cached", "--quiet", base, "--", path], env)
        if staged.returncode == 1:
            problems.append("index not refreshed for {}".format(path))
            skipped.append(path)
            continue
        if staged.returncode != 0:
            detail = _collapse(staged.stderr + staged.stdout) or "git diff failed"
            problems.append("index not refreshed for {}: {}".format(path, detail))
            skipped.append(path)
            continue
        listed = _git(root, ["ls-tree", "-z", new_commit, "--", path], env)
        if listed.returncode != 0 or not listed.stdout:
            detail = _collapse(listed.stderr + listed.stdout) or "git ls-tree failed"
            problems.append("index not refreshed for {}: {}".format(path, detail))
            skipped.append(path)
            continue
        updated = _git(root, ["update-index", "-z", "--index-info"], env, listed.stdout)
        if updated.returncode != 0:
            detail = _collapse(updated.stderr + updated.stdout) or "git update-index failed"
            problems.append("index not refreshed for {}: {}".format(path, detail))
            skipped.append(path)
    if problems:
        if skipped:
            print(_refresh_message(root, short_id, "; ".join(problems), skipped))
        else:
            print("wiki commit: {} - made, but {}".format(short_id, "; ".join(problems)))
        return 1
    print("wiki commit: {} - {}".format(short_id, ", ".join(candidate["shown"])))
    return 0


def _publish(root: str, ticket: str, candidate: dict) -> int:
    """Create the commit and move the branch only if it still points at base."""
    env = _base_env()
    committed = _git(
        root,
        ["commit-tree", candidate["tree"], "-p", candidate["base"], "-m", candidate["message"]],
        env)
    if committed.returncode != 0 or not committed.stdout.strip():
        raise NotMade(_collapse(committed.stderr + committed.stdout) or "git commit-tree failed")
    new_commit = committed.stdout.decode().strip()
    updated = _git(
        root, ["update-ref", candidate["branch"], new_commit, candidate["base"]], env)
    if updated.returncode != 0:
        raise NotMade(
            _collapse(updated.stderr + updated.stdout) or "the wiki's HEAD moved during the commit")
    try:
        return _report_published(root, env, new_commit, candidate)
    except NotMade as exc:
        print("wiki commit: {} - made, but {}".format(new_commit, exc.reason))
        return 1


def _commit(root: str, ticket: str, file_args: list) -> int:
    candidate = _build(root, ticket, file_args)
    if candidate is None:
        print("wiki commit: nothing to commit")
        return 0
    return _publish(root, ticket, candidate)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="commit_wiki.py")
    parser.add_argument("wiki_root")
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--file", action="append", default=[])
    return parser


def main(argv: list | None = None) -> int:
    _reconfigure()
    if argv is None:
        argv = sys.argv[1:]
    parser = _parser()
    try:
        args = parser.parse_args(argv)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # noqa: BLE001 - one not-made line for every other failure
        print("wiki commit: not made - unexpected failure: {}: {}".format(type(exc).__name__, exc))
        return 1
    if not TICKET_RE.fullmatch(args.ticket):
        parser.error("--ticket must match ^[A-Z][A-Z0-9]*-[0-9]+$")
    try:
        return _commit(args.wiki_root, args.ticket, list(args.file))
    except NotMade as exc:
        _not_made(args.wiki_root, args.ticket, list(args.file), exc.reason)
        return 1
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # noqa: BLE001 - one not-made line for every other failure
        _not_made(
            args.wiki_root, args.ticket, list(args.file),
            "unexpected failure: {}: {}".format(type(exc).__name__, exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
