#!/usr/bin/env python3
"""Commit this ticket's wiki log entries and named files in one local commit.

Usage:
    commit_wiki.py <wiki-root> --ticket <TICKET-ID> [--file <path>]...

The commit is built in a private index from HEAD, so the working tree and the
real index stay untouched until the commit has succeeded. A failure prints
`wiki commit: not made - <reason>` and a retry line, and leaves the wiki as it
was. The script never pushes, stashes, resets, checks out, or prompts.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TICKET_RE = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")
HEADING_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] ")
DROPPED_ENV = {
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE", "GIT_PREFIX",
}
IN_PROGRESS = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD")


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


def _retry(root: str, ticket: str, files: list) -> str:
    parts = [
        '"{}"'.format(_forward(sys.executable)),
        '"{}"'.format(_forward(os.path.abspath(__file__))),
        '"{}"'.format(_forward(root)),
        "--ticket", ticket,
    ]
    for path in files:
        parts.append("--file")
        parts.append('"{}"'.format(_forward(path)))
    return "To retry: " + " ".join(parts)


def _not_made(root: str, ticket: str, files: list, reason: str) -> None:
    print("wiki commit: not made - {}".format(reason))
    print(_retry(root, ticket, files))


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


def _parse_log(data: bytes):
    """Return (preamble bytes, blocks). A block is heading, raw bytes, line texts."""
    data.decode("utf-8")
    spans = _line_spans(data)
    texts = []
    heading_at = []
    for index, (left, right, _) in enumerate(spans):
        text = data[left:right].decode("utf-8")
        if index == 0 and text.startswith("\ufeff"):
            text = text[1:]
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
        heading = texts[start]
        if heading.startswith("\ufeff"):
            heading = heading[1:]
        blocks.append((heading, raw, texts[start:end]))
    return preamble, blocks


def _is_ours(heading: str, head_headings: set, ticket: str) -> bool:
    if heading in head_headings:
        return False
    prefix = ticket.split("-", 1)[0]
    merge = "] merge | {} \u2014 {} PR #".format(prefix, ticket)
    close = "] close | {} \u2014 {}:".format(prefix, ticket)
    return merge in heading or close in heading


def _encode_lines(lines: list, newline: bytes) -> bytes:
    return b"".join(line.encode("utf-8") + newline for line in lines)


def _with_blank_line(text: bytes, newline: bytes) -> bytes:
    if not text.endswith(newline):
        text += newline
    if not text.endswith(newline + newline):
        text += newline
    return text


def _compose(head_bytes: bytes, work_bytes: bytes, ticket: str):
    """Return (composed bytes, entry count), or (None, 0) when log.md stays out."""
    try:
        head_preamble, head_blocks = _parse_log(head_bytes)
        _, work_blocks = _parse_log(work_bytes)
    except UnicodeDecodeError as exc:
        raise NotMade("log.md is not UTF-8") from exc
    headings = {block[0] for block in head_blocks}
    first = {}
    for index, block in enumerate(head_blocks):
        first.setdefault(block[0], index)
    newline = b"\r\n" if b"\r\n" in head_bytes else b"\n"
    before = {index: [] for index in range(len(head_blocks))}
    pending = []
    for heading, _, lines in work_blocks:
        if _is_ours(heading, headings, ticket):
            pending.append(_encode_lines(lines, newline))
        elif heading in first:
            before[first[heading]].extend(pending)
            pending = []
    if not any(before.values()) and not pending:
        return None, 0
    count = sum(len(parts) for parts in before.values()) + len(pending)
    pieces = [head_preamble]
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


def _refresh_message(root: str, short: str, detail: str, paths: list) -> str:
    shown = " ".join(paths)
    return (
        'wiki commit: {} - made, but the wiki index was not refreshed ({}): '
        'run git -C "{}" reset -q -- {}'
    ).format(short, detail or "git failed", _forward(root), shown)


def _commit(root: str, ticket: str, file_args: list) -> int:
    env = _base_env()
    if not os.path.isdir(root):
        raise NotMade("{} is not the top of a git work tree".format(root))
    prefix = _git(root, ["rev-parse", "--show-prefix"], env)
    if prefix.returncode != 0 or prefix.stdout.strip():
        raise NotMade("{} is not the top of a git work tree".format(root))
    head_ref = _git(root, ["symbolic-ref", "-q", "HEAD"], env)
    if head_ref.returncode != 0:
        raise NotMade("the wiki is on a detached HEAD")
    current = _git(root, ["rev-parse", "-q", "--verify", "HEAD"], env)
    if current.returncode != 0 or not current.stdout.strip():
        raise NotMade("the wiki has no commit yet")
    base = current.stdout.decode().strip()
    for name in IN_PROGRESS:
        found = _git(root, ["rev-parse", "-q", "--verify", name], env)
        if found.returncode == 0 and found.stdout.strip():
            raise NotMade("the wiki has a merge, cherry-pick or revert in progress")
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
    composed = None
    count = 0
    log_path = os.path.join(root, "log.md")
    if os.path.isfile(log_path):
        blob = _git(root, ["cat-file", "blob", "HEAD:log.md"], env)
        if blob.returncode == 0:
            with open(log_path, "rb") as handle:
                work_bytes = handle.read()
            composed, count = _compose(blob.stdout, work_bytes, ticket)
    index_dir = tempfile.mkdtemp(prefix="commit-wiki-")
    try:
        private = dict(env)
        private["GIT_INDEX_FILE"] = os.path.join(index_dir, "index")
        _require(_git(root, ["read-tree", "HEAD"], private), "git read-tree failed")
        real_paths = []
        shown = []
        if composed is not None:
            hashed = _require(
                _git(root, ["hash-object", "-w", "--stdin"], private, composed),
                "git hash-object failed")
            blob_id = hashed.stdout.decode().strip()
            mode_line = _require(
                _git(root, ["ls-tree", "HEAD", "--", "log.md"], private),
                "git ls-tree failed")
            mode = mode_line.stdout.decode().split()[0]
            _require(_git(
                root, ["update-index", "--cacheinfo", "{},{},log.md".format(mode, blob_id)],
                private), "git update-index failed")
            real_paths.append("log.md")
            shown.append("log.md ({} entries)".format(count))
        if files:
            adding = dict(private)
            adding["GIT_LITERAL_PATHSPECS"] = "1"
            _require(_git(root, ["add", "--", *files], adding), "git add failed")
            real_paths.extend(files)
            shown.extend(files)
        quiet = _git(root, ["diff", "--cached", "--quiet"], private)
        if quiet.returncode == 0:
            print("wiki commit: nothing to commit")
            return 0
        if quiet.returncode != 1:
            raise NotMade(_collapse(quiet.stderr + quiet.stdout) or "git diff failed")
        again = _require(_git(root, ["rev-parse", "HEAD"], private), "git rev-parse failed")
        if again.stdout.decode().strip() != base:
            raise NotMade("the wiki's HEAD moved during the commit")
        message = "close({}): wiki harvest from {}".format(ticket.lower(), ticket)
        committed = _git(root, ["commit", "-q", "-m", message], private)
        if committed.returncode != 0:
            raise NotMade(_collapse(committed.stderr + committed.stdout) or "git commit failed")
        short = _git(root, ["rev-parse", "--short", "HEAD"], env)
        short_id = short.stdout.decode().strip() if short.returncode == 0 else "unknown"
        listed = _git(root, ["ls-tree", "-z", "HEAD", "--", *real_paths], env)
        if listed.returncode != 0:
            print(_refresh_message(root, short_id, _collapse(listed.stderr + listed.stdout), real_paths))
            return 1
        updated = _git(root, ["update-index", "-z", "--index-info"], env, listed.stdout)
        if updated.returncode != 0:
            print(_refresh_message(root, short_id, _collapse(updated.stderr + updated.stdout), real_paths))
            return 1
        if short.returncode != 0:
            raise NotMade(_collapse(short.stderr + short.stdout) or "git rev-parse failed")
        print("wiki commit: {} - {}".format(short_id, ", ".join(shown)))
        return 0
    finally:
        shutil.rmtree(index_dir, ignore_errors=True)


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
