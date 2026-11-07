#!/usr/bin/env python3
"""Archive a ticket's spec artifacts from docs/specs/TODO/ to docs/specs/DONE/<ID>/.

Usage: archive_spec.py <TICKET-ID> [--dry-run]

Run with cwd at the project root (the directory holding docs/specs/). Collects
every TODO/<ID>.* entry (prefix stripped) and, when TODO/<ID>/ is a folder, its
direct children. Per item: never move onto an existing path; classify the source
(tracked / with untracked files / untracked) and the destination (ignored or
not) just before the move; git mv or a filesystem move; git add only a
destination that is not ignored. Prints one line per item, then the staged
paths. Exit 0 all moved or nothing to do, 1 some item skipped or failed,
2 usage or environment error. Stdlib only.
"""

import os
import re
import subprocess
import sys

USAGE = "usage: archive_spec.py <TICKET-ID> [--dry-run]"
TICKET_RE = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")
TODO = "docs/specs/TODO"
DONE = "docs/specs/DONE"


class Usage(Exception):
    pass


def git(*args):
    # Literal pathspecs keep `*`, `?` and `[` in artifact names from matching
    # siblings. check-ignore rejects that magic and takes a plain path anyway.
    env = dict(os.environ)
    if args[0] != "check-ignore":
        env["GIT_LITERAL_PATHSPECS"] = "1"
    proc = subprocess.run(["git"] + list(args), env=env, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", "replace").strip()


def collect(ticket):
    """(source, destination) pairs: TODO/<ID>.* first, then TODO/<ID>/ children."""
    items = []
    if not os.path.isdir(TODO):
        return items
    prefix = ticket + "."
    for name in sorted(os.listdir(TODO)):
        if name.startswith(prefix) and len(name) > len(prefix):
            items.append((TODO + "/" + name, DONE + "/" + ticket + "/" + name[len(prefix):]))
    folder = TODO + "/" + ticket
    if os.path.isdir(folder):
        for name in sorted(os.listdir(folder)):
            items.append((folder + "/" + name, DONE + "/" + ticket + "/" + name))
    return items


def classify(source, destination):
    """Return (state, ignored) or raise RuntimeError naming the failing command."""
    code, out, _ = git("ls-files", "-z", "--", source)
    if code != 0:
        raise RuntimeError("git ls-files exit {}".format(code))
    tracked = bool(out.strip(b"\0"))
    code, out, _ = git("ls-files", "-z", "--others", "--exclude-standard", "--", source)
    if code != 0:
        raise RuntimeError("git ls-files --others exit {}".format(code))
    untracked = bool(out.strip(b"\0"))
    code, _, _ = git("check-ignore", "-q", "--", destination)
    if code not in (0, 1):
        raise RuntimeError("git check-ignore exit {}".format(code))
    ignored = code == 0
    if tracked:
        return ("tracked, with untracked files" if untracked else "tracked"), ignored
    return ("untracked, destination ignored" if ignored
            else "untracked, destination not ignored"), ignored


def move(source, destination, state, ignored):
    """Do one move. Return (result text, staged?, ok?)."""
    if state.startswith("tracked"):
        code, _, err = git("mv", "--", source, destination)
        if code != 0:
            return "NOT moved ({})".format(err or "git mv exit {}".format(code)), False, False
        if state == "tracked":
            return "moved", True, True
        if ignored:
            return "moved (untracked files local only)", True, True
        code, _, err = git("add", "--", destination)
        if code != 0:
            return "partially archived ({})".format(err or "git add exit {}".format(code)), True, False
        return "moved", True, True
    try:
        os.rename(source, destination)
    except OSError as exc:
        return "NOT moved ({})".format(exc), False, False
    if ignored:
        return "moved (local only)", False, True
    code, _, err = git("add", "--", destination)
    if code != 0:
        return "moved, NOT staged ({})".format(err or "git add exit {}".format(code)), False, False
    return "moved", True, True


def run(ticket, dry_run):
    code, out, _ = git("rev-parse", "--is-inside-work-tree")
    if code != 0 or out.strip() != b"true":
        raise Usage("archive: not inside a git work tree")
    if not os.path.isdir("docs/specs"):
        raise Usage("archive: no docs/specs/ under {}".format(os.getcwd()))

    items = collect(ticket)
    if not items:
        print("archive: nothing to archive for {}".format(ticket))
        return 0

    claimed = set()
    staged = []
    problems = 0
    for source, destination in items:
        head = "archive: {} -> {} - ".format(source, destination)
        key = os.path.normcase(os.path.normpath(destination))
        if key in claimed or os.path.lexists(destination):
            print(head + ("destination exists: would skip" if dry_run else "destination exists: skipped"))
            problems += 1
            continue
        try:
            state, ignored = classify(source, destination)
        except RuntimeError as exc:
            print(head + "error: {}".format(exc))
            problems += 1
            continue
        claimed.add(key)
        if dry_run:
            print(head + state + ": would move")
            continue
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        result, was_staged, ok = move(source, destination, state, ignored)
        print(head + state + ": " + result)
        if was_staged:
            staged.append(destination)
        if not ok:
            problems += 1

    folder = TODO + "/" + ticket
    if not dry_run and os.path.isdir(folder):
        try:
            os.rmdir(folder)
        except OSError:
            pass

    if dry_run:
        print("staged: (dry run)")
    elif staged:
        for path in staged:
            print("staged: " + path)
    else:
        print("staged: none")
    return 1 if problems else 0


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = [a for a in argv if a != "--dry-run"]
    dry_run = len(args) != len(argv)
    try:
        if len(args) != 1 or not TICKET_RE.match(args[0]) or argv.count("--dry-run") > 1:
            raise Usage(USAGE)
        return run(args[0], dry_run)
    except Usage as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - any surprise is exit 2, never a traceback
        print("archive: error: {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
