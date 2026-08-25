#!/usr/bin/env python3
"""Prepend a close entry to the wiki's newest-first `log.md`.

Usage:
    prepend_log_entry.py <log-path> --guard 'close | <PROJECT> — <TICKET-ID>:'

The entry text arrives on **stdin** (close entries are multi-paragraph prose, so
a CLI argument is the wrong carrier). The script owns the write: it locates the
insertion anchor, refuses shapes the anchor cannot describe, guards against
duplicates, and lands the bytes through a temp file plus `os.replace`.

The anchor is line-anchored on a real date::

    ENTRY_RE = ^## \\[\\d{4}-\\d{2}-\\d{2}\\]<space>   (re.MULTILINE)

which is what keeps it off `log.md`'s own header sentence -- ``Format: `## [YYYY-MM-DD]
action | description` `` -- where a naive ``text.index("## [")`` matches mid-sentence
and splices the entry into the middle of the header. All three narrowings (line
start, real digits, trailing space) would have to fail at once for that sentence
to be selected.

`ENTRY_RE` has two jobs: it finds the anchor on read, and it validates the
entry's own heading on write. A narrow anchor is only safe if the entries this
script writes are guaranteed to match it -- otherwise the *next* run's anchor
skips this entry and inserts underneath it, silently leaving newest-first
contract one run later.

Outcomes (stdout carries `prepend_log_entry_outcome=<outcome>`):

    prepended  the entry was inserted above the newest dated entry
    fresh      no dated entry existed; the entry was placed at end of file
    created    `log.md` did not exist; it now holds this entry alone

Exit codes -- exactly three, and 1 is reserved:

    0  entry written (see the outcome token for which of the three)
    1  ONLY: the guard string is already present; nothing written
    2  everything else: input validation, an unmatched anchor in a populated
       file, a concurrent change, any I/O failure, any unexpected exception

The reservation of 1 is a hard requirement: CPython exits 1 on an uncaught
exception, so an unguarded `PermissionError` would be reported to the operator
as "entry already present -- skipped" over a `log.md` that was never written.

Stdlib only. No markdown parsing: one line-anchored regex search over the file
text, deliberately (a fenced example entry in the header would be selected; the
live header has no fence, and fence masking is the first step toward a markdown
parser inside a skill script).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

# The insertion anchor. Line-anchored (`^` under re.M) on a *real* date, with a
# mandatory trailing space -- three exclusions, each load-bearing against the
# header's own `Format: ## [YYYY-MM-DD] action | description` sentence.
ENTRY_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] ", re.M)

# Evidence that a file has entry-shaped headings the anchor could not describe:
# a hand-edited `### [...]`, a short date `## [2026-8-5]`, a missing space after
# the `]`. Their presence turns "no anchor" from fresh-wiki into a refusal.
HEADINGISH_RE = re.compile(r"^#{2,6} *\[", re.M)

BOM = "﻿"

HEREDOC_HINT = (
    "pipe the entry in on stdin, e.g.:\n"
    "  \"$PY\" \"$SCRIPT\" \"$LOGPATH\" --guard 'close | PROJECT — TICKET:' "
    "<<'PREPEND_LOG_ENTRY_EOF'\n"
    "  ## [YYYY-MM-DD] close | PROJECT — TICKET: title\n"
    "  ...\n"
    "  PREPEND_LOG_ENTRY_EOF"
)


class AnchorMissing(Exception):
    """A populated file whose headings the anchor cannot describe (D7 refusal).

    Carries the evidence the operator needs to hand-fix the file: how many
    heading-like lines were seen, and where the first one is.
    """

    def __init__(self, count: int, line_number: int, line_text: str) -> None:
        super().__init__("no line-anchored dated entry found")
        self.count = count
        self.line_number = line_number
        self.line_text = line_text

    def message(self) -> str:
        return (
            "no line-anchored dated entry found, but {} heading-like line(s) "
            "present — first is line {}: {} — refusing to write".format(
                self.count, self.line_number, self.line_text
            )
        )


def normalize_entry(raw: bytes) -> str:
    r"""Decode strict UTF-8, fold \r\n and lone \r to \n, strip a BOM, strip.

    Strict, deliberately: the two in-repo precedents (`_sections.normalize`,
    `lint._read_lines`) decode with errors='replace', which is right for
    *inspecting* a file. This entry lands permanently in the wiki's operations
    log, so a mojibake'd entry is refused rather than silently written with
    U+FFFD in it. The resulting UnicodeDecodeError reaches main()'s guard as a
    clean exit 2.

    A BOM is not whitespace, so `.strip()` would leave it in place and the
    entry's first line would be `﻿## [...]`, which ENTRY_RE cannot match.
    Stripping it is the right fix for a recoverable input.
    """
    text = raw.decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith(BOM):
        text = text[1:]
    return text.strip()


def splice(existing, entry):
    """Return (new_text, outcome). `existing` is None when log.md is absent.

    A leading BOM on `existing` is detached before matching and re-attached to
    the result: every offset, separator and degenerate-emptiness decision is
    made in the stripped coordinates, so the BOM neither moves the anchor (both
    patterns are `^`-anchored, and a BOM immediately preceding an entry heading
    would defeat them on that line only, silently) nor counts as preceding
    content (`'\\ufeff'` is not whitespace, so `.strip()` keeps it and the
    degenerate no-leading-separator rule would never fire).

    outcome is one of: "prepended", "fresh", "created".
    Raises AnchorMissing when existing has heading-like lines but no dated entry.
    """
    if existing is None:
        return entry + "\n", "created"

    bom = ""
    text = existing
    if text.startswith(BOM):
        bom = BOM
        text = text[1:]

    match = ENTRY_RE.search(text)
    if match is not None:
        head = text[: match.start()].rstrip()
        tail = text[match.start():]
        # No leading separator when nothing precedes the anchor: without this a
        # touched log.md, or a second close against the file the missing-file
        # outcome created, would open with two blank lines.
        if head:
            return bom + head + "\n\n" + entry + "\n\n" + tail, "prepended"
        return bom + entry + "\n\n" + tail, "prepended"

    headingish = list(HEADINGISH_RE.finditer(text))
    if headingish:
        first = headingish[0]
        line_number = text.count("\n", 0, first.start()) + 1
        line_end = text.find("\n", first.start())
        line_text = (text[first.start():] if line_end == -1
                     else text[first.start():line_end]).strip()
        raise AnchorMissing(len(headingish), line_number, line_text)

    body = text.rstrip()
    if body:
        return bom + body + "\n\n" + entry + "\n", "fresh"
    return bom + entry + "\n", "fresh"


def _current_umask() -> int:
    """Read the umask without leaving it changed.

    The stdlib has no getter -- `os.umask()` is a setter returning the prior
    value -- so set-and-restore. This script is single-threaded, so the window
    is safe.
    """
    previous = os.umask(0)
    os.umask(previous)
    return previous


def write_atomically(path: Path, text: str, baseline, mode: int) -> bool:
    """Render to a dot-prefixed temp, fsync, close, re-check, replace.

    Returns False when the target changed under us between the read and the
    replace; True on success. `baseline` is (st_mtime_ns, st_size) from the read
    handle, or None when the file did not exist.

    Reuses the shape of `skills/session-handoff/scripts/create_handoff.py`
    `write_atomically()`. Deliberately a second implementation: skills install
    independently under `<config-dir>/skills/<name>/` and share no importable
    module, and that signature is welded to its claim-file reservation protocol.

    The dot prefix is load-bearing, not cosmetic: the wiki's `.gitignore`
    carries `.*.tmp`, and SKILL.md tells the operator to commit the wiki with
    `git add -A`, so an undotted leak would be staged and committed.
    """
    fd, temp_name = tempfile.mkstemp(
        prefix=".prepend-log-entry.", suffix=".md.tmp", dir=str(path.parent)
    )
    temp_path = Path(temp_name)
    try:
        # Close the descriptor before renaming: on Windows an open *source*
        # handle blocks os.replace exactly as an open target handle does.
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp creates at 0600 by design, and os.replace would carry that
        # onto log.md -- silently making the wiki's operations log owner-only.
        # Git does not track non-exec mode bits, so it would never show in a
        # diff or survive a clone.
        os.chmod(str(temp_path), mode)

        # The last thing before the swap. This closes the window this script
        # opens; it is detection, not locking.
        if baseline is None:
            if os.path.exists(str(path)):
                return False
        else:
            try:
                current = os.stat(str(path))
            except FileNotFoundError:
                return False
            if (current.st_mtime_ns, current.st_size) != baseline:
                return False

        os.replace(str(temp_path), str(path))
        return True
    finally:
        # try/finally, not except/BaseException: the stat-mismatch abort above
        # is a plain return, so exception-only cleanup would leak on the one
        # path most likely to leak.
        temp_path.unlink(missing_ok=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prepend_log_entry.py",
        description="Prepend a close entry to the wiki's newest-first log.md.",
    )
    parser.add_argument("path", metavar="LOG_PATH",
                        help="path to the wiki's log.md")
    parser.add_argument("--guard", required=True, metavar="LITERAL",
                        help="idempotency literal, e.g. "
                             "'close | PROJECT — TICKET:'")
    return parser


def _run(argv, context) -> int:
    args = _parser().parse_args(argv)
    path = Path(args.path).resolve()
    guard = args.guard
    # Published for main()'s catch-all: every failure message names the
    # resolved absolute path and the --guard literal, because /spec-close
    # surfaces stderr verbatim and nothing else -- "log.md changed under us"
    # read months later in a transcript with no path is not debuggable.
    context["path"] = path
    context["guard"] = guard

    def fail(message: str) -> int:
        sys.stderr.write("{} (guard: {}): {}\n".format(path, guard, message))
        return 2

    # 1. No stdin attached. Without this the script blocks on read() until an
    #    EOF that never arrives, hanging the close for the harness's full Bash
    #    timeout with Phase 5 step 3's archive moves already applied. "Empty
    #    stdin" (a pipe that closed with zero bytes) and "no stdin" (no pipe at
    #    all) are different conditions and are checked separately.
    #    Platform note: on Windows `NUL` is a character device and isatty()
    #    returns True for it, so `< /dev/null` reaches this branch there and the
    #    empty-entry branch on POSIX.
    if sys.stdin is None or sys.stdin.isatty():
        return fail("no entry on stdin — " + HEREDOC_HINT)

    # 2. Empty entry, after decode / newline-fold / BOM-strip / strip.
    entry = normalize_entry(sys.stdin.buffer.read())
    if not entry:
        return fail("empty entry on stdin — " + HEREDOC_HINT)

    first_line = entry.split("\n", 1)[0]

    # 3. Guard shape. Both failures would otherwise land on exit 1 -- the
    #    silent-loss code -- so they are validated rather than trusted.
    if not guard.strip():
        return fail("--guard is empty")
    if not guard.endswith(":"):
        return fail(
            "guard must end with ':' — the trailing colon is what keeps "
            "closing TICKET-1 after TICKET-11 from false-matching"
        )
    # The colon check catches a *truncated* guard but is blind to an
    # *unsubstituted* one: the literal template ends with ':' and does appear in
    # the first line of an entry built from the same template, so both other
    # checks pass and a literal-placeholder entry lands permanently at
    # position 1.
    if "<" in guard or ">" in guard:
        return fail("guard still contains an unresolved placeholder: "
                    "{}".format(guard))
    # Close entries routinely quote sibling tickets in body prose, so a
    # whole-text check would pass on a guard describing a different entry.
    if guard not in first_line:
        return fail("guard not found in the entry's first line: "
                    "{}".format(first_line))

    # 4. Entry heading shape -- the write-side mirror of the read-side refusal.
    #    An entry the *next* run's anchor cannot find lands at the top, exits 0,
    #    and then gets the newer entry inserted underneath it: this ticket's own
    #    bug, one run later, with no refusal to prompt a re-sort.
    if ENTRY_RE.match(entry) is None:
        return fail(
            "entry heading does not match the log format "
            "'## [YYYY-MM-DD] …' — refusing to write an entry the anchor "
            "cannot find: {}".format(first_line)
        )

    # 5. Read. newline="" -- *not* the default newline=None, whose
    #    universal-newline translation silently converts every \r\n to \n in
    #    memory, so the LF write would then re-terminate the whole file.
    baseline = None
    mode = None
    existing = None
    if path.exists():
        with open(str(path), encoding="utf-8", newline="") as handle:
            existing = handle.read()
            # fstat on the handle, not stat on the path: if another writer lands
            # its own os.replace while our read() is in flight, POSIX rename
            # swaps the inode and a post-read stat(path) would describe the
            # *new* file. That baseline would match at re-check and we would
            # replace the file with a splice of stale content.
            info = os.fstat(handle.fileno())
        baseline = (info.st_mtime_ns, info.st_size)
        mode = info.st_mode & 0o777
    else:
        mode = 0o666 & ~_current_umask()

    # 6. Idempotency. Literal substring, never a regex -- the guard contains
    #    `|`, which a regex would read as alternation. Whole-text, exactly as
    #    the retired `grep -F` searched every line.
    if existing is not None and guard in existing:
        sys.stderr.write(
            "entry already present in {} (guard: {}) — skipped\n".format(
                path, guard)
        )
        return 1

    try:
        new_text, outcome = splice(existing, entry)
    except AnchorMissing as exc:
        return fail(exc.message())

    if not write_atomically(path, new_text, baseline, mode):
        sys.stderr.write(
            "{} changed under us between read and replace (guard: {}) "
            "— re-run\n".format(path, guard)
        )
        return 2

    if outcome == "fresh":
        sys.stderr.write(
            "{}: no dated entry found — entry placed at end of file\n".format(path)
        )
    elif outcome == "created":
        sys.stderr.write(
            "{} did not exist — created with this entry alone; "
            "no header synthesized\n".format(path)
        )

    # After the successful replace, so a failed write never leaves a
    # `=prepended` token beside an exit 2.
    print("prepend_log_entry_outcome={}".format(outcome))
    return 0


def main(argv) -> int:
    # Best-effort, and outside the failure semantics: reconfigure is a
    # TextIOWrapper method, and main() may be called in-process with sys.stdout
    # replaced by an io.StringIO. Left unguarded that AttributeError would be
    # caught below and returned as 2 -- the exact value most tests assert as
    # their failure signal, so a test could pass having never reached the code
    # it exists to exercise.
    #
    # It is needed at all because Python's stdout encoding on Windows is
    # locale-derived (cp1252 with errors='surrogateescape' when piped), and
    # every message here echoes the --guard literal, which carries an em dash by
    # construction. PEP 686's UTF-8 default lands in 3.15, not 3.14.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass

    context = {}
    try:
        return _run(argv, context)
    except (KeyboardInterrupt, SystemExit):
        # argparse raises SystemExit(0) for --help and SystemExit(2) for a usage
        # error, each already carrying its own output. Swallowing them would
        # make --help print help, then an error, then exit 2.
        raise
    except BaseException as exc:  # noqa: BLE001 - 1 is reserved; see module docstring
        detail = "unexpected failure: {}: {}".format(type(exc).__name__, exc)
        if "path" in context:
            detail = "{} (guard: {}): {}".format(
                context["path"], context["guard"], detail)
        # One carve-out: a failure raised before argparse completes has neither
        # value available and emits the exception alone.
        sys.stderr.write(detail + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
