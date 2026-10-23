#!/usr/bin/env python3
"""Preflight a gitignored credential-rotation record.

Usage:
    prepare_record.py --project-root <dir> [--record-path <path>] [--choose <path> [--reuse-only] | --new | --reuse-only] [--template <path>]
    prepare_record.py --project-root <dir> [--record-path <path>] --status
    prepare_record.py --project-root <dir> [--record-path <path>] --list-names [--file <project-relative>]...
    prepare_record.py --project-root <dir> [--record-path <path>] --match-names --names-file <project-relative>
    prepare_record.py --project-root <dir> --hash-name <name> --file <project-relative>
    prepare_record.py --project-root <dir> --hash-names --names-file <project-relative> --file <project-relative>

Stdlib only. Python 3.8. The read-only name, match, and hash modes are not
implemented in this copy; each of those flags exits 1.
"""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

MAX_STEM_ATTEMPTS = 9
DATE_TOKEN = "YYYY-MM-DD"
CLOSE_MARK = b"Sign-off (close):"
CLOSED_WORD = b"closed:"
ASCII_WS = b" \t\v\f\r"
DEFAULT_RECORD = ".key-rotation/record-YYYY-MM-DD.md"
GIT_TIMEOUT_SECONDS = 30


class Stop(Exception):
    """A prepare_record failure. stderr is the full block to write."""

    def __init__(self, stderr, code=1):
        self.stderr = stderr
        self.code = code


class Check(object):
    def __init__(self, satisfied, q_exit, source, pattern):
        self.satisfied = satisfied
        self.q_exit = q_exit
        self.source = source
        self.pattern = pattern


class Published(object):
    def __init__(self):
        self.wrote = False
        self.previous = b""
        self.new = b""


def stop(reason):
    raise Stop("prepare_record: {}\n".format(reason))


def stop_block(header, paths, advisories):
    lines = [header]
    lines.extend(paths)
    lines.extend(advisories)
    raise Stop("\n".join(lines) + "\n")


def real_path(path):
    return os.path.realpath(os.path.abspath(str(path)))


def same_path(left, right):
    return os.path.normcase(real_path(left)) == os.path.normcase(real_path(right))


def is_inside(child, root):
    child_n = os.path.normcase(real_path(child))
    root_n = os.path.normcase(real_path(root))
    if child_n == root_n:
        return False
    prefix = root_n if root_n.endswith(os.sep) else root_n + os.sep
    return child_n.startswith(prefix)


def project_relative(root, path):
    rel = os.path.relpath(real_path(path), real_path(root))
    return Path(rel).as_posix()


def absolute_text(path):
    return os.path.abspath(real_path(path))


def split_lines(data):
    lines = []
    start = 0
    i = 0
    length = len(data)
    while i < length:
        if data[i:i + 2] == b"\r\n":
            lines.append(data[start:i])
            i += 2
            start = i
        elif data[i:i + 1] in (b"\n", b"\r"):
            lines.append(data[start:i])
            i += 1
            start = i
        else:
            i += 1
    if start < length:
        lines.append(data[start:])
    return lines


def line_is_close_mark(line):
    return line.lstrip(ASCII_WS).startswith(CLOSE_MARK)


def line_is_closed(line):
    """Closed only when the value starts with closed: and evidence follows."""
    body = line.lstrip(ASCII_WS)
    if not body.startswith(CLOSE_MARK):
        return False
    rest = body[len(CLOSE_MARK):].strip(ASCII_WS)
    if len(rest) < len(CLOSED_WORD):
        return False
    if rest[:len(CLOSED_WORD)].lower() != CLOSED_WORD:
        return False
    return rest[len(CLOSED_WORD):].strip(ASCII_WS) != b""


def classify(data):
    """Return 'open', 'closed', or None when the bytes are not a record."""
    found = False
    all_closed = True
    for line in split_lines(data):
        if not line_is_close_mark(line):
            continue
        found = True
        if not line_is_closed(line):
            all_closed = False
    if not found:
        return None
    if all_closed:
        return "closed"
    return "open"


def is_temp_entry(path):
    name = path.name
    if name.endswith(".tmp") or name.startswith(".key-rotation."):
        return True
    if not name.endswith(".md"):
        return False
    try:
        st = os.lstat(str(path))
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and st.st_size == 0


def read_regular(path):
    """Return (data, unreadable). A non-regular file is neither."""
    try:
        st = os.lstat(str(path))
    except OSError:
        return None, True
    if not stat.S_ISREG(st.st_mode):
        return None, False
    if st.st_size == 0:
        return b"", False
    try:
        with open(str(path), "rb") as handle:
            return handle.read(), False
    except OSError:
        return None, True


def is_record_file(path):
    if is_temp_entry(path):
        return False
    data, unreadable = read_regular(path)
    if unreadable or data is None:
        return False
    return classify(data) is not None


def parent_is_records_and_temps(parent):
    if not parent.exists():
        return True
    if not parent.is_dir():
        return False
    try:
        entries = list(parent.iterdir())
    except OSError:
        return False
    for entry in entries:
        if is_temp_entry(entry):
            continue
        if is_record_file(entry):
            continue
        return False
    return True


def run_git(root, args):
    try:
        proc = subprocess.run(
            ["git"] + list(args),
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None, b"", b""
    return proc.returncode, proc.stdout, proc.stderr


def git_or_stop(root, args, rel):
    code, out, err = run_git(root, args)
    if code is None:
        stop("not a git work tree")
    return code, out, err


def parse_check_ignore_v(stdout):
    text = stdout.splitlines()
    if not text:
        return b"", b""
    line = text[-1]
    if b"\t" not in line:
        return b"", b""
    left, _pathname = line.split(b"\t", 1)
    # source:linenum:pattern — the line number is the last numeric field.
    parts = left.split(b":")
    if len(parts) < 3:
        return b"", b""
    for index in range(len(parts) - 1, 0, -1):
        if parts[index].isdigit():
            source = b":".join(parts[:index])
            pattern = b":".join(parts[index + 1:])
            return source, pattern
    return b"", b""


def source_is_worktree_gitignore(source, root):
    if not source:
        return False
    try:
        text = source.decode("utf-8", "surrogateescape")
    except UnicodeError:
        return False
    if os.path.isabs(text):
        candidate = text
    else:
        candidate = os.path.join(str(root), text)
    gitignore = os.path.join(str(root), ".gitignore")
    try:
        return os.path.normcase(real_path(candidate)) == os.path.normcase(real_path(gitignore))
    except OSError:
        return False


def check_ignore(root, operand, no_index):
    """Decide with -q. Read -v only after -q says the path is ignored.

    -v alone is not the decision: a negated pattern can make -v exit 0
    while -q reports the path is not ignored.
    """
    q_args = ["check-ignore", "-q"]
    if no_index:
        q_args.append("--no-index")
    q_args.extend(["--", operand])
    q_code, _q_out, _q_err = git_or_stop(root, q_args, operand)
    if q_code not in (0, 1):
        stop("not a git work tree {} {}".format(operand, q_code))
    if q_code == 1:
        return Check(False, 1, None, None)
    v_args = ["check-ignore", "-v"]
    if no_index:
        v_args.append("--no-index")
    v_args.extend(["--", operand])
    v_code, v_out, _v_err = git_or_stop(root, v_args, operand)
    if v_code != 0:
        stop("not a git work tree {} {}".format(operand, v_code))
    source, pattern = parse_check_ignore_v(v_out)
    satisfied = (
        source_is_worktree_gitignore(source, root)
        and not pattern.startswith(b"!")
    )
    return Check(satisfied, 0, source, pattern)


def ignore_checks(root, parent_rel, file_rel):
    parent_operand = parent_rel if parent_rel.endswith("/") else parent_rel + "/"
    parent_check = check_ignore(root, parent_operand, False)
    file_check = check_ignore(root, file_rel, True)
    return parent_check, file_check


def tracked_state(root, file_rel):
    """Return 'tracked', 'untracked', or stop when git cannot answer."""
    code, _out, _err = git_or_stop(
        root, ["ls-files", "--error-unmatch", "--", file_rel], file_rel)
    if code == 0:
        return "tracked"
    if code == 1:
        return "untracked"
    stop("not a git work tree {} {}".format(file_rel, code))
    return "untracked"


def gitignore_bytes(root):
    path = root / ".gitignore"
    if not path.exists():
        return b"", None
    if not path.is_file():
        stop("write failed")
    try:
        return path.read_bytes(), path.stat().st_mode & 0o777
    except OSError:
        stop("write failed")
    return b"", None


def line_present(data, pattern):
    target = pattern.encode("utf-8")
    return target in data.split(b"\n")


def prepare_ignore_bytes(existing, pattern, checks):
    """Return new bytes, or None when nothing should be written."""
    unsatisfied = [item for item in checks if not item.satisfied]
    if not unsatisfied:
        return None
    because_q1 = any(item.q_exit == 1 for item in unsatisfied)
    because_other = any(item.q_exit == 0 for item in unsatisfied)
    if because_q1:
        append = True
    elif because_other and not line_present(existing, pattern):
        append = True
    else:
        append = False
    if not append:
        return None
    line = pattern.encode("utf-8") + b"\n"
    if existing and not existing.endswith(b"\n"):
        return existing + b"\n" + line
    return existing + line


def unlink_quiet(path):
    try:
        os.unlink(str(path))
    except OSError:
        pass


def publish_bytes(root, baseline, new_bytes):
    """Compare-and-swap .gitignore. Return None, or an error reason."""
    path = root / ".gitignore"
    for _attempt in range(3):
        temp_path = None
        try:
            if path.is_file():
                current = path.read_bytes()
                mode = path.stat().st_mode & 0o777
            elif path.exists():
                return "gitignore changed"
            else:
                current = b""
                mode = 0o644
            if current != baseline:
                continue
            fd, temp_name = tempfile.mkstemp(prefix=".key-rotation.", dir=str(root))
            temp_path = Path(temp_name)
            # Close before replace: on Windows an open source handle blocks it.
            with os.fdopen(fd, "wb") as handle:
                handle.write(new_bytes)
                handle.flush()
                os.fsync(handle.fileno())
            # mkstemp is 0600; replace would carry that onto the shared file.
            os.chmod(str(temp_path), mode)
            if path.is_file():
                again = path.read_bytes()
            elif path.exists():
                unlink_quiet(temp_path)
                temp_path = None
                continue
            else:
                again = b""
            if again != current or again != baseline:
                unlink_quiet(temp_path)
                temp_path = None
                continue
            os.replace(str(temp_path), str(path))
            temp_path = None
            return None
        except OSError:
            if temp_path is not None:
                unlink_quiet(temp_path)
            return "write failed"
    return "gitignore changed"


def rollback_gitignore(root, state):
    if not state.wrote:
        return
    path = root / ".gitignore"
    try:
        current = path.read_bytes() if path.is_file() else b""
    except OSError:
        return
    if current != state.new:
        return
    publish_bytes(root, state.new, state.previous)


def recheck_ignore(root, parent_rel, file_rel, state):
    parent_check, file_check = ignore_checks(root, parent_rel, file_rel)
    if parent_check.satisfied and file_check.satisfied:
        return
    rollback_gitignore(root, state)
    stop("ignore check failed")


def validate_pattern(parent_rel):
    pattern = parent_rel + "/"
    if (
        "\n" in pattern
        or "\r" in pattern
        or pattern.startswith("#")
        or pattern.startswith("!")
        or any(ch in pattern for ch in "*?[")
    ):
        stop("ignore pattern rejected")
    return pattern


def create_parent(parent):
    if parent.is_dir():
        return
    if parent.exists():
        stop("write failed")
    try:
        os.mkdir(str(parent), 0o700)
    except FileExistsError:
        if not parent.is_dir():
            stop("write failed")
    except OSError:
        stop("write failed")
    if os.name == "posix":
        try:
            os.chmod(str(parent), 0o700)
        except OSError:
            stop("write failed")


def ensure_ignore(root, target, state):
    """Steps 5 to 9 for the chosen file. state remembers a publish for rollback."""
    parent = target.parent
    if same_path(parent, root) or not is_inside(parent, root):
        stop("ignore pattern rejected")
    parent_rel = project_relative(root, parent)
    if parent_rel in ("", "."):
        stop("ignore pattern rejected")
    pattern = validate_pattern(parent_rel)
    create_parent(parent)
    file_rel = project_relative(root, target)
    if tracked_state(root, file_rel) == "tracked":
        stop("record is tracked")
    parent_check, file_check = ignore_checks(root, parent_rel, file_rel)
    checks = (parent_check, file_check)
    if parent_check.satisfied and file_check.satisfied:
        recheck_ignore(root, parent_rel, file_rel, state)
        return state
    if not parent_is_records_and_temps(parent):
        stop("parent is not a record directory")
    existing, _mode = gitignore_bytes(root)
    new_bytes = prepare_ignore_bytes(existing, pattern, checks)
    if new_bytes is None:
        stop("ignore check failed")
    reason = publish_bytes(root, existing, new_bytes)
    if reason:
        stop(reason)
    state.wrote = True
    state.previous = existing
    state.new = new_bytes
    recheck_ignore(root, parent_rel, file_rel, state)
    return state


def search_dirs(root, parent):
    found = []
    seen = set()
    for candidate in (root / ".key-rotation", parent):
        if not candidate.is_dir():
            continue
        key = os.path.normcase(real_path(candidate))
        if key in seen:
            continue
        seen.add(key)
        found.append(candidate)
    return found


def search_records(root, parent):
    """Return (open, closed, advisories, unreadable relative paths)."""
    opens = []
    closed = []
    advisories = []
    unreadable = []
    seen = set()
    for directory in search_dirs(root, parent):
        try:
            entries = list(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if is_temp_entry(entry):
                continue
            if not entry.name.endswith(".md"):
                continue
            key = os.path.normcase(real_path(entry))
            if key in seen:
                continue
            seen.add(key)
            data, failed = read_regular(entry)
            if failed:
                rel = project_relative(root, entry)
                unreadable.append(rel)
                advisories.append("prepare_record: skipped unreadable {}".format(rel))
                continue
            if data is None:
                continue
            kind = classify(data)
            if kind == "open":
                opens.append(entry)
            elif kind == "closed":
                closed.append(entry)
    opens.sort(key=lambda item: project_relative(root, item))
    closed.sort(key=lambda item: project_relative(root, item))
    return opens, closed, advisories, unreadable


def rels_of(root, paths):
    return [project_relative(root, item) for item in paths]


def stem_names(resolved):
    stem = resolved.name[:-3]
    suffixes = [""] + ["-{}".format(n) for n in range(2, MAX_STEM_ATTEMPTS + 1)]
    return ["{}{}.md".format(stem, suffix) for suffix in suffixes]


def claim_path(target):
    return target.parent / (target.name + ".tmp")


def existing_blocks_stem(target):
    """A real file blocks the stem. A zero-byte .md is a crash leftover."""
    if not os.path.lexists(str(target)):
        return False
    try:
        st = os.lstat(str(target))
    except OSError:
        return True
    if stat.S_ISREG(st.st_mode) and st.st_size == 0:
        return False
    return True


def next_available(resolved, after=None):
    """The next free stem. A zero-byte claim with no .md is removed and reused."""
    passed = after is None
    for name in stem_names(resolved):
        if not passed:
            if name == after:
                passed = True
            continue
        target = resolved.parent / name
        claim = claim_path(target)
        if existing_blocks_stem(target):
            continue
        if os.path.lexists(str(claim)):
            try:
                cst = os.lstat(str(claim))
            except OSError:
                continue
            target_absent = not os.path.lexists(str(target))
            reclaim = (
                stat.S_ISREG(cst.st_mode)
                and cst.st_size == 0
                and target_absent
            )
            if not reclaim:
                continue
            try:
                os.unlink(str(claim))
            except OSError:
                continue
        return target
    return None


def remove_zero_byte_target(target):
    try:
        st = os.lstat(str(target))
    except OSError:
        return
    if stat.S_ISREG(st.st_mode) and st.st_size == 0:
        unlink_quiet(target)


def try_exclusive(path):
    """Create path with O_EXCL. Return True when this process owns it."""
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return False
    except OSError:
        stop("write failed")
    os.close(fd)
    return True


def load_template(template_arg, today):
    if template_arg:
        path = Path(template_arg)
    else:
        path = Path(__file__).resolve().parent.parent / "reference" / "record-template.md"
    if not path.is_file():
        stop("template missing {}".format(path))
    try:
        data = path.read_bytes()
    except OSError:
        stop("template missing {}".format(path))
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if b"{{date}}" not in data:
        stop("template missing {}".format(path))
    return data.replace(b"{{date}}", today.encode("ascii"))


def write_record(root, target, claim, body, state):
    parent_rel = project_relative(root, target.parent)
    file_rel = project_relative(root, target)
    fd, temp_name = tempfile.mkstemp(
        prefix=".key-rotation.", suffix=".md.tmp", dir=str(target.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        recheck_ignore(root, parent_rel, file_rel, state)
        os.replace(str(temp_path), str(target))
        temp_path = None
    except Stop:
        if temp_path is not None:
            unlink_quiet(temp_path)
        unlink_quiet(target)
        unlink_quiet(claim)
        raise
    except OSError:
        if temp_path is not None:
            unlink_quiet(temp_path)
        unlink_quiet(target)
        unlink_quiet(claim)
        stop("write failed")
    unlink_quiet(claim)


def emit(advisories):
    for line in advisories:
        sys.stderr.write(line + "\n")


def finish_reuse(root, target, advisories, state):
    ensure_ignore(root, target, state)
    emit(advisories)
    sys.stdout.write("reused: {}\n".format(absolute_text(target)))
    return 0


def finish_create(root, resolved, body, advisories):
    state = Published()
    target = next_available(resolved, None)
    while target is not None:
        ensure_ignore(root, target, state)
        claim = claim_path(target)
        remove_zero_byte_target(target)
        if not try_exclusive(claim):
            target = next_available(resolved, target.name)
            continue
        if not try_exclusive(target):
            unlink_quiet(claim)
            target = next_available(resolved, target.name)
            continue
        write_record(root, target, claim, body, state)
        emit(advisories)
        sys.stdout.write("created: {}\n".format(absolute_text(target)))
        return 0
    stop("write failed")


def resolve_user_path(root, raw):
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    return Path(real_path(path))


def validate_record_path(root, raw, today):
    """Return the resolved record path. Reject before any search or create."""
    pure = Path(raw)
    parent_text = pure.parent.as_posix()
    name = pure.name
    if DATE_TOKEN in parent_text or not name.endswith(".md"):
        stop("record path rejected")
    name = name.replace(DATE_TOKEN, today)
    if pure.is_absolute():
        candidate = Path(pure.parent) / name
    else:
        candidate = root / pure.parent / name
    resolved = Path(real_path(candidate))
    if not is_inside(resolved, root):
        stop("path is outside the project {}".format(raw))
    if resolved.is_dir():
        stop("record path rejected")
    return resolved


def find_match(records, chosen):
    for record in records:
        if same_path(record, chosen):
            return record
    return None


def run_status(root, resolved):
    opens, _closed, advisories, _unreadable = search_records(root, resolved.parent)
    emit(advisories)
    for record in opens:
        sys.stdout.write(absolute_text(record) + "\n")
    return 0


def chosen_rel_text(root, choose_path, raw):
    if is_inside(choose_path, root):
        return project_relative(root, choose_path)
    return raw


def run_create_or_reuse(args, root, resolved, today):
    opens, closed, advisories, unreadable = search_records(root, resolved.parent)
    choose_path = None
    match = None
    if args.choose is not None:
        choose_path = resolve_user_path(root, args.choose)
        match = find_match(opens, choose_path)
    if unreadable and not args.new and match is None:
        lines = list(advisories)
        lines.append("prepare_record: record unreadable {}".format(unreadable[0]))
        raise Stop("\n".join(lines) + "\n")
    if args.choose is not None:
        if match is None:
            stop_block(
                "prepare_record: chosen record not open {}".format(
                    chosen_rel_text(root, choose_path, args.choose)),
                rels_of(root, opens),
                advisories,
            )
        return finish_reuse(root, match, advisories, Published())
    if not args.new:
        if len(opens) == 1:
            return finish_reuse(root, opens[0], advisories, Published())
        if len(opens) > 1:
            stop_block(
                "prepare_record: multiple open records",
                rels_of(root, opens),
                advisories,
            )
        if args.reuse_only:
            stop_block(
                "prepare_record: no open record",
                rels_of(root, closed),
                advisories,
            )
    body = load_template(args.template, today)
    return finish_create(root, resolved, body, advisories)


def build_parser():
    parser = argparse.ArgumentParser(prog="prepare_record.py")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--record-path", default=None)
    parser.add_argument("--template", default=None)
    parser.add_argument("--reuse-only", action="store_true")
    parser.add_argument("--status", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--choose", default=None)
    group.add_argument("--new", action="store_true")
    # Declared for the next run. Behavior is a hard failure until then.
    parser.add_argument("--list-names", action="store_true")
    parser.add_argument("--match-names", action="store_true")
    parser.add_argument("--hash-name", default=None)
    parser.add_argument("--hash-names", action="store_true")
    parser.add_argument("--file", action="append", default=None)
    parser.add_argument("--names-file", default=None)
    return parser


def readonly_requested(args):
    return bool(
        args.list_names
        or args.match_names
        or args.hash_names
        or args.hash_name is not None
        or args.names_file is not None
        or args.file
    )


def execute(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.new and args.reuse_only:
        parser.error("--new and --reuse-only are mutually exclusive")
    if readonly_requested(args):
        sys.stderr.write("prepare_record: not implemented\n")
        return 1
    if args.project_root is None or args.project_root.strip() == "":
        stop("path is outside the project")
    root = Path(real_path(args.project_root))
    if not root.is_dir():
        stop("not a git work tree")
    today = date.today().isoformat()
    raw = args.record_path if args.record_path is not None else DEFAULT_RECORD
    resolved = validate_record_path(root, raw, today)
    if args.status:
        return run_status(root, resolved)
    return run_create_or_reuse(args, root, resolved, today)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass
    try:
        return execute(sys.argv[1:] if argv is None else argv)
    except Stop as exc:
        sys.stderr.write(exc.stderr)
        return exc.code
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        sys.stderr.write("prepare_record: write failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
