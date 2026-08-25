#!/usr/bin/env python3
"""Tests for spec-close's log.md prepend script (VHS-29).

Stdlib unittest. Run directly: `python tests/test_spec_close_log.py`.
Resolves the repo root and all paths from __file__ (never cwd) so it works
regardless of the working directory ship-spec runs it from.

The skill's script is loaded by file path so it can stay a portable script
without package boilerplate, matching tests/test_session_handoff.py.

Every mutating case copies its fixture into a per-test TemporaryDirectory and
operates on the copy — the checked-in fixtures are read-only inputs. Without
this, run 1 mutates log-with-entries.md in the working tree and run 2's
idempotency case exits 1 where it expects 0, with /ship-spec green on the first
pass and a corrupted fixture in the PR.

Division of labour: unit cases drive splice() directly; process-level cases that
need no interposition go through subprocess with the script's real argv; cases
that must act *between* the script's read and its write drive main() in-process,
because subprocess gives no seam.

Exit 2 is the catch-all for validation, I/O, refusal and concurrency, so every
exit-2 case additionally asserts its distinguishing stderr text — a case
asserting only the code can pass having never reached the code it exercises.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import lint  # noqa: E402

SKILL_DIR = REPO_ROOT / "skills" / "spec-close"
SKILL_MD = SKILL_DIR / "SKILL.md"
SCRIPT = SKILL_DIR / "scripts" / "prepend_log_entry.py"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
PORTABLE_DOC = REPO_ROOT / "docs" / "authoring-portable-skills.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "spec-close"

BOM = "﻿"
GUARD = "close | VHS — VHS-29:"
HEADING = "## [2026-08-25] close | VHS — VHS-29: /spec-close prepends its entry"
BODY = (
    "`abc1234` (PR #99). Closed via `/spec-close`. The close entry carries an em\n"
    "dash — and a `|` pipe — in its body, the way real entries do."
)
ENTRY = HEADING + "\n\n" + BODY

# The header's own format sentence, verbatim from the fixtures. A naive
# `text.index("## [")` matches *inside* this line.
FORMAT_SENTENCE = (
    "Append-only record of wiki operations. "
    "Format: `## [YYYY-MM-DD] action | description`"
)


def load_script(path: Path, module_name: str):
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load script at {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_prepender():
    return load_script(SCRIPT, "spec_close_prepend_under_test")


class StdinStub:
    """A stand-in for sys.stdin exposing both halves the script needs.

    Both are required. The precedent helper (tests/test_session_handoff.py
    run_main) leaves sys.stdin alone, which under `python -m unittest` in a
    terminal is a tty — so the no-stdin guard would fire and *every* in-process
    call would exit 2 before reaching the code under test. And io.StringIO has
    no `.buffer`, which the strict-UTF-8 stdin read requires, so a naive fake
    raises AttributeError into the catch-all and also exits 2. Both give a
    green-looking "exit 2" for the wrong reason.
    """

    def __init__(self, data: bytes, isatty: bool = False) -> None:
        self.buffer = io.BytesIO(data)
        self._isatty = isatty

    def isatty(self) -> bool:
        return self._isatty


def run_main(module, argv, entry: bytes = b"", isatty: bool = False):
    """Call main(argv) in-process and capture its streams.

    Exit codes are asserted on the returned int, never via SystemExit.
    """
    out, err = io.StringIO(), io.StringIO()
    stub = StdinStub(entry, isatty)
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
            mock.patch.object(sys, "stdin", stub):
        code = module.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def run_cli(argv, entry: bytes = b""):
    """Run the script as a real subprocess with the real interpreter."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)] + list(argv),
        input=entry, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return (proc.returncode,
            proc.stdout.decode("utf-8"),
            proc.stderr.decode("utf-8"))


def run_cli_devnull(argv):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)] + list(argv),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return (proc.returncode,
            proc.stdout.decode("utf-8"),
            proc.stderr.decode("utf-8"))


def read(path: Path) -> str:
    with open(str(path), encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path: Path, text: str) -> Path:
    """Write with explicit newline translation.

    Path.write_text() only grew a `newline` parameter in 3.10 and AGENTS.md
    declares a Python 3.8 floor, so go through open(), which has always had one.
    """
    with open(str(path), "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def header_of(text: str) -> str:
    """Every byte from `# Wiki Log` through the blockquote's last line."""
    start = text.index("# Wiki Log")
    end = text.index("entries dated **2026-08-01 and later**.") + len(
        "entries dated **2026-08-01 and later**.")
    return text[start:end]


def temps_in(directory: Path):
    return [p.name for p in directory.iterdir()
            if p.name.startswith(".prepend-log-entry.")]


class PrependCase(unittest.TestCase):
    """Base: a private temp dir plus a freshly loaded copy of the script."""

    def setUp(self):
        self.module = load_prepender()
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def copy_fixture(self, name: str, as_name: str = "log.md") -> Path:
        target = self.tmp / as_name
        shutil.copyfile(str(FIXTURES / name), str(target))
        return target


class TestHeaderCorruption(PrependCase):
    """Case: header corruption — the regression this ticket exists for."""

    def test_naive_index_would_split_the_header(self):
        # Regression for VHS-29: the fixture *is* the test. Prove the naive
        # anchor lands inside the format sentence before proving ours does not.
        # From `# Wiki Log` onward: the live log.md starts there, while the
        # fixture carries a provenance comment above it that no real file has.
        original = read(FIXTURES / "log-with-entries.md")
        live_shape = original[original.index("# Wiki Log"):]
        naive = live_shape.index("## [")
        self.assertIn(FORMAT_SENTENCE[:40], live_shape[max(0, naive - 60):naive + 60],
                      "the naive anchor should land inside the format sentence")
        self.assertLess(naive, live_shape.index("\n## ["),
                        "the naive anchor should precede the first real entry")

    def test_prepends_above_the_newest_entry_and_leaves_the_header_intact(self):
        # Regression for VHS-29: prepend, and do not touch the header.
        target = self.copy_fixture("log-with-entries.md")
        original = read(target)

        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)

        result = read(target)
        self.assertEqual(header_of(result), header_of(original),
                         "the header must be byte-identical after the write")
        self.assertLess(result.index(HEADING), result.index("## [2026-08-24]"),
                        "the new entry must sit above the previously-newest one")
        self.assertLess(result.index(FORMAT_SENTENCE), result.index(HEADING),
                        "the new entry must sit below the header")
        self.assertNotIn(FORMAT_SENTENCE[:30] + "\n", result[:result.index(HEADING)]
                         .replace(FORMAT_SENTENCE, "SENTENCE"),
                         "the format sentence must not have been split")
        self.assertIn(FORMAT_SENTENCE, result)


class TestAnchor(PrependCase):
    """Case: anchor unit test."""

    def test_entry_re_ignores_the_format_sentence(self):
        # Regression for VHS-29: three narrowings, each load-bearing.
        module = self.module
        self.assertIsNone(module.ENTRY_RE.search(FORMAT_SENTENCE))
        self.assertIsNone(module.HEADINGISH_RE.search(FORMAT_SENTENCE))
        match = module.ENTRY_RE.search(HEADING)
        self.assertIsNotNone(match)
        self.assertEqual(match.start(), 0)

    def test_entry_re_rejects_each_narrowing(self):
        module = self.module
        for bad in ("### [2026-08-25] x",       # depth
                    "## [2026-8-5] x",          # short date
                    "## [2026-08-25]x",         # no space after ]
                    "## [2026-08-25]\tx",       # tab, not space
                    " ## [2026-08-25] x"):      # indented, so not at ^
            self.assertIsNone(module.ENTRY_RE.match(bad), bad)


class TestReadSideRefusal(PrependCase):
    """Case: read-side refusal — a populated file the anchor misses."""

    def test_h3_entries_refuse(self):
        # Regression for VHS-29: a silent bottom-append here IS the bug.
        target = self.copy_fixture("log-h3-entries.md")
        original = read(target)
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("no line-anchored dated entry found", err)
        self.assertIn("heading-like line(s) present", err)
        self.assertIn("refusing to write", err)
        self.assertIn(str(target), err)
        self.assertIn(GUARD, err)
        self.assertEqual(read(target), original, "nothing may be written")
        self.assertEqual(out, "")

    def test_heading_like_line_above_the_anchor_refuses(self):
        # Regression for VHS-29: a dated entry is not enough on its own. An
        # operator hand-demotes the newest entry to `### [...]` over older `##`
        # ones; the anchor then finds the OLDER entry and a plain prepend files
        # the new entry underneath something newer — exit 0, "Prepended:"
        # reported, file silently out of newest-first contract.
        target = self.copy_fixture("log-with-entries.md")
        text = read(target).replace(
            "## [2026-08-24] merge", "### [2026-08-26] merge")
        write(target, text)
        original = read(target)

        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("sit above the newest line-anchored dated entry", err)
        self.assertIn("refusing to write", err)
        self.assertIn("### [2026-08-26]", err)
        self.assertIn(str(target), err)
        self.assertEqual(read(target), original, "nothing may be written")
        self.assertEqual(out, "")

    def test_the_two_refusals_report_distinct_reasons(self):
        # The no-anchor message must not be reused for the above-anchor case:
        # "no line-anchored dated entry found" would be false there, and the
        # operator would go looking for the wrong defect.
        code, _out, err = run_cli(
            [str(self.copy_fixture("log-h3-entries.md")), "--guard", GUARD],
            ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("no line-anchored dated entry found", err)
        self.assertNotIn("sit above", err)

    def test_normal_shape_still_prepends(self):
        # The guard against over-refusing: the live log.md header carries no
        # heading-like line at all, so the ordinary path must be untouched.
        target = self.copy_fixture("log-with-entries.md")
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)

    def test_short_date_entries_refuse(self):
        target = write(self.tmp / "log.md",
                       "# Wiki Log\n\n" + FORMAT_SENTENCE
                       + "\n\n## [2026-8-5] merge | VHS — VHS-1: short date\n\nb\n")
        original = read(target)
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("1 heading-like line(s) present", err)
        self.assertIn("## [2026-8-5]", err)
        self.assertEqual(read(target), original)


class TestWriteSideHeadingValidation(PrependCase):
    """Case: write-side heading validation — the mirror of the read-side rule."""

    def test_malformed_entry_headings_are_refused(self):
        # Regression for VHS-29: an entry the NEXT run's anchor cannot find
        # lands at the top, exits 0, and gets the newer entry inserted
        # underneath it — this ticket's bug, one run later.
        rest = " close | VHS — VHS-29: title\n\nbody"
        for heading in ("## [2026-8-5]" + rest,
                        "### [2026-08-25]" + rest,
                        "## [2026-08-25]close | VHS — VHS-29: title\n\nbody",
                        "## [2026-08-25]\tclose | VHS — VHS-29: title\n\nbody"):
            with self.subTest(heading=heading.split("\n")[0]):
                target = self.copy_fixture("log-with-entries.md")
                original = read(target)
                code, _out, err = run_cli([str(target), "--guard", GUARD],
                                          heading.encode("utf-8"))
                self.assertEqual(code, 2, err)
                self.assertIn("entry heading does not match the log format", err)
                self.assertEqual(read(target), original)

    def test_well_formed_entry_passes(self):
        target = self.copy_fixture("log-with-entries.md")
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)


class TestDateOrdering(PrependCase):
    """Case: newest-first ordering — the rule the anchor alone cannot enforce.

    `TestReadSideRefusal` covers headings ENTRY_RE *cannot* read. These cover
    the heading it reads perfectly and would still file the new entry
    underneath: a well-formed entry at the anchor carrying a newer date. Same
    end state as this ticket's bug — exit 0, "Prepended:" reported, file out of
    newest-first contract with nothing to prompt a re-sort — so it gets the same
    refusal.
    """

    def top_dated(self, date_text: str) -> Path:
        """log-with-entries.md with its newest entry re-dated."""
        target = self.copy_fixture("log-with-entries.md")
        write(target, read(target).replace("## [2026-08-24] merge",
                                           "## [{}] merge".format(date_text)))
        return target

    def test_older_entry_above_a_newer_one_refuses(self):
        # The entry is dated 2026-08-25; the file's newest is 2026-08-26. Both
        # headings are well formed, so every check that exists before this one
        # passes and the plain prepend files the older entry on top.
        target = self.top_dated("2026-08-26")
        original = read(target)

        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("entry dated 2026-08-25 is older", err)
        self.assertIn("dated 2026-08-26", err)
        self.assertIn("refusing to write above it", err)
        self.assertIn(str(target), err)
        self.assertIn(GUARD, err)
        self.assertEqual(read(target), original, "nothing may be written")
        self.assertEqual(out, "")

    def test_same_day_entry_still_prepends(self):
        # The guard against over-refusing: several closes land on one day, and
        # newest-first puts the most recent of them on top. Only a *strictly*
        # older entry is a contract break.
        target = self.top_dated("2026-08-25")
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)
        result = read(target)
        self.assertLess(result.index(HEADING), result.index("## [2026-08-25] merge"))

    def test_impossible_entry_date_is_refused(self):
        # ENTRY_RE's \d{2} fields constrain width, not range, so these clear the
        # heading-shape check above and would land permanently in the wiki's
        # operations log on a day that does not exist.
        for bad in ("2026-13-45", "2026-02-30", "2026-00-10"):
            with self.subTest(date=bad):
                target = self.copy_fixture("log-with-entries.md")
                original = read(target)
                entry = ENTRY.replace("2026-08-25", bad)
                code, out, err = run_cli([str(target), "--guard", GUARD],
                                         entry.encode("utf-8"))
                self.assertEqual(code, 2, err)
                self.assertIn("entry heading date is not a real calendar day", err)
                self.assertEqual(read(target), original)
                self.assertEqual(out, "")

    def test_impossible_anchor_date_is_refused(self):
        # The read-side mirror. There is no ordering to check the entry against,
        # and a guess would file it above a heading nobody can order — so the
        # operator is told to fix the file rather than handed a silent write.
        target = self.top_dated("2026-02-30")
        original = read(target)

        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("the newest dated entry carries a date that is not a "
                      "real calendar day", err)
        self.assertIn("## [2026-02-30] merge", err)
        self.assertEqual(read(target), original)
        self.assertEqual(out, "")

    def test_the_ordering_refusals_report_distinct_reasons(self):
        # Exit 2 is the catch-all, so an operator reading only the code cannot
        # tell "your entry is backdated" from "your log.md is corrupt at the
        # top" — the two need different fixes.
        _c1, _o1, backdated = run_cli(
            [str(self.top_dated("2026-08-26")), "--guard", GUARD],
            ENTRY.encode("utf-8"))
        _c2, _o2, corrupt = run_cli(
            [str(self.top_dated("2026-02-30")), "--guard", GUARD],
            ENTRY.encode("utf-8"))
        self.assertIn("is older than the newest entry", backdated)
        self.assertNotIn("is not a real calendar day", backdated)
        self.assertIn("is not a real calendar day", corrupt)
        self.assertNotIn("is older than the newest entry", corrupt)


class TestFreshWiki(PrependCase):
    """Case: fresh wiki — header present, zero dated entries."""

    def test_entry_lands_after_the_header(self):
        target = self.copy_fixture("log-fresh.md")
        original = read(target)
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=fresh", out)
        self.assertIn("no dated entry found", err)
        self.assertIn(str(target), err,
                      "the notice must carry the resolved path — it is what "
                      "the completion output surfaces instead of `Prepended:`")

        result = read(target)
        self.assertEqual(header_of(result), header_of(original))
        self.assertLess(result.index(FORMAT_SENTENCE), result.index(HEADING))
        self.assertTrue(result.endswith(BODY + "\n"))


class TestMissingFile(PrependCase):
    """Case: missing file."""

    def test_file_is_created_with_the_entry_alone(self):
        target = self.tmp / "log.md"
        self.assertFalse(target.exists())
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=created", out)
        self.assertIn("did not exist", err)
        self.assertIn("no header synthesized", err)
        self.assertIn(str(target), err)
        # The honest minimum: a header would have to assert the rotation
        # boundary and name log-archive.md, neither of which the script knows.
        self.assertEqual(read(target), ENTRY + "\n")


class TestIdempotency(PrependCase):
    """Case: idempotency."""

    def test_second_run_skips_and_changes_nothing(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        after_first = read(target)

        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 1, err)
        self.assertIn("entry already present", err)
        self.assertIn("skipped", err)
        self.assertIn(str(target), err)
        self.assertIn(GUARD, err)
        self.assertEqual(out, "")
        self.assertEqual(read(target), after_first)
        self.assertEqual(after_first.count(GUARD), 1)


class TestGuardPrecision(PrependCase):
    """Case: guard precision — the trailing colon is load-bearing."""

    def test_ticket_11_does_not_suppress_ticket_1(self):
        # Regression for VHS-29: without the trailing colon, closing VHS-1
        # after VHS-11 false-matches and silently skips the entry.
        target = self.copy_fixture("log-with-entries.md")
        text = read(target).replace(
            "## [2026-08-24] merge | VHS — VHS-28:",
            "## [2026-08-24] close | VHS — VHS-11:")
        write(target, text)

        entry = ("## [2026-08-26] close | VHS — VHS-1: the one-digit sibling"
                 "\n\nbody")
        code, out, err = run_cli([str(target), "--guard", "close | VHS — VHS-1:"],
                                 entry.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)
        self.assertIn("close | VHS — VHS-1:", read(target))

    def test_exact_match_does_suppress(self):
        target = self.copy_fixture("log-with-entries.md")
        entry = ("## [2026-08-26] close | VHS — VHS-27: repeat\n\nbody")
        code, _out, err = run_cli(
            [str(target), "--guard", "close | VHS — VHS-27:"],
            entry.encode("utf-8"))
        self.assertEqual(code, 1, err)
        self.assertIn("entry already present", err)


class TestGuardShape(PrependCase):
    """Case: guard shape — all three failures exit 2, never 1."""

    def test_guard_without_trailing_colon(self):
        target = self.copy_fixture("log-with-entries.md")
        original = read(target)
        code, _out, err = run_cli([str(target), "--guard", "close | VHS — VHS-29"],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("guard must end with ':'", err)
        self.assertEqual(read(target), original)

    def test_guard_present_only_in_the_body(self):
        # Close entries routinely quote sibling tickets in body prose, so a
        # whole-text check would pass on a guard describing a different entry.
        target = self.copy_fixture("log-with-entries.md")
        entry = ("## [2026-08-26] close | VHS — VHS-30: a different ticket\n\n"
                 "Body prose that mentions close | VHS — VHS-29: in passing.")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  entry.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("guard not found in the entry's first line", err)

    def test_wholly_unsubstituted_guard_names_the_placeholder(self):
        # Regression for VHS-29: the template guard ends with ':' AND appears in
        # the first line of an entry built from the same template, so the other
        # two checks both pass and a literal-placeholder entry would land
        # permanently at position 1 of the wiki's log.
        target = self.copy_fixture("log-with-entries.md")
        original = read(target)
        template_guard = "close | <PROJECT> — <TICKET-ID>:"
        entry = ("## [2026-08-25] " + template_guard + " <title>\n\n<body>")
        code, _out, err = run_cli([str(target), "--guard", template_guard],
                                  entry.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("unresolved placeholder", err)
        self.assertNotIn("guard must end with", err)
        self.assertNotIn("first line", err)
        self.assertEqual(read(target), original)


class TestStdin(PrependCase):
    """Case: no stdin."""

    def test_devnull_is_refused(self):
        # On Windows NUL is a character device and isatty() returns True for it,
        # so /dev/null reaches the no-stdin branch there and the empty-entry
        # branch on POSIX. Assert the union.
        target = self.copy_fixture("log-with-entries.md")
        original = read(target)
        code, _out, err = run_cli_devnull([str(target), "--guard", GUARD])
        self.assertEqual(code, 2, err)
        self.assertTrue("no entry on stdin" in err or "empty entry on stdin" in err,
                        err)
        self.assertEqual(read(target), original)

    def test_tty_stdin_names_the_heredoc(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_main(
            self.module, [str(target), "--guard", GUARD],
            ENTRY.encode("utf-8"), isatty=True)
        self.assertEqual(code, 2, err)
        self.assertIn("no entry on stdin", err)
        self.assertIn("PREPEND_LOG_ENTRY_EOF", err)

    def test_whitespace_only_entry_is_refused(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_cli([str(target), "--guard", GUARD], b"  \n\n \n")
        self.assertEqual(code, 2, err)
        self.assertIn("empty entry on stdin", err)


class TestExitOneIsReserved(PrependCase):
    """Case: exit 1 is reserved — an I/O failure must never read as a skip."""

    def test_directory_target_exits_two(self):
        # Via subprocess, so the real interpreter's uncaught-exception status is
        # what is measured: CPython exits 1 on an uncaught exception, which
        # would be reported to the operator as "already present — skipped".
        # Portable: PermissionError on Windows, IsADirectoryError on POSIX.
        directory = self.tmp / "log.md"
        directory.mkdir()
        code, out, err = run_cli([str(directory), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertNotIn("already present", err)
        self.assertNotIn("skipped", err)
        self.assertIn("unexpected failure", err)
        self.assertIn(str(directory), err)
        self.assertIn(GUARD, err)
        self.assertEqual(out, "")

    @unittest.skipIf(os.name == "nt", "POSIX directory permissions")
    def test_read_only_parent_directory_exits_two(self):
        # A read-only *target file* would not do: os.replace is governed by the
        # parent directory's permissions on POSIX, so chmod 0444 log.md succeeds
        # there and the assertion would hold only on Windows.
        if os.geteuid() == 0:  # pragma: no cover - root ignores the mode bits
            self.skipTest("running as root")
        nested = self.tmp / "wiki"
        nested.mkdir()
        target = nested / "log.md"
        shutil.copyfile(str(FIXTURES / "log-with-entries.md"), str(target))
        original = read(target)
        os.chmod(str(nested), 0o500)
        self.addCleanup(os.chmod, str(nested), 0o700)
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertNotIn("already present", err)
        self.assertEqual(read(target), original)


class TestAtomicWrite(PrependCase):
    """Case: atomic write and temp hygiene."""

    def test_no_temp_survives_a_successful_run(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertEqual(temps_in(self.tmp), [])

    def test_mid_write_failure_leaves_the_original_and_no_temp(self):
        target = self.copy_fixture("log-with-entries.md")
        original = read(target)
        seen = []

        def boom(fd):
            seen.extend(p.name for p in self.tmp.iterdir())
            raise OSError("simulated ENOSPC")

        with mock.patch.object(self.module.os, "fsync", boom):
            code, out, err = run_main(self.module, [str(target), "--guard", GUARD],
                                      ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("unexpected failure", err)
        self.assertEqual(read(target), original,
                         "a plain open(path, 'w') would have truncated here")
        self.assertEqual(out, "")
        self.assertEqual(temps_in(self.tmp), [])
        # The dot prefix is load-bearing: the wiki's .gitignore carries `.*.tmp`
        # and SKILL.md tells the operator to commit the wiki with `git add -A`.
        self.assertTrue(
            any(name.startswith(".prepend-log-entry.") and name.endswith(".md.tmp")
                for name in seen),
            "expected a dot-prefixed temp during the write, saw {}".format(seen))


class TestConcurrentChange(PrependCase):
    """Case: concurrent change detected."""

    def test_change_between_read_and_replace_is_refused(self):
        target = self.copy_fixture("log-with-entries.md")
        real_splice = self.module.splice

        def mutate_then_splice(existing, entry):
            write(target, read(target) + "\n## [2026-08-26] merge | VHS — VHS-99:"
                                         " another writer landed\n\nbody\n")
            return real_splice(existing, entry)

        with mock.patch.object(self.module, "splice", mutate_then_splice):
            code, out, err = run_main(self.module, [str(target), "--guard", GUARD],
                                      ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("changed under us between read and replace", err)
        self.assertIn(str(target), err)
        self.assertIn(GUARD, err)
        self.assertIn("VHS-99", read(target), "the other writer's entry survives")
        self.assertNotIn(HEADING, read(target))
        self.assertEqual(out, "")
        # The mismatch abort is a plain return, so exception-only cleanup would
        # leak here.
        self.assertEqual(temps_in(self.tmp), [])

    def test_file_appearing_under_a_missing_file_run_is_refused(self):
        target = self.tmp / "log.md"
        real_splice = self.module.splice

        def create_then_splice(existing, entry):
            write(target, "## [2026-08-26] merge | VHS — VHS-99: bootstrapped\n")
            return real_splice(existing, entry)

        with mock.patch.object(self.module, "splice", create_then_splice):
            code, _out, err = run_main(self.module, [str(target), "--guard", GUARD],
                                       ENTRY.encode("utf-8"))
        self.assertEqual(code, 2, err)
        self.assertIn("changed under us between read and replace", err)
        self.assertIn("VHS-99", read(target))
        self.assertEqual(temps_in(self.tmp), [])


@unittest.skipIf(os.name == "nt", "POSIX mode bits")
class TestMode(PrependCase):
    """Case: mode — mkstemp creates at 0600 and os.replace would carry it over."""

    def test_existing_mode_is_preserved(self):
        target = self.copy_fixture("log-with-entries.md")
        os.chmod(str(target), 0o644)
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertEqual(stat.S_IMODE(os.stat(str(target)).st_mode), 0o644,
                         "git does not track non-exec mode bits, so a silent "
                         "0600 would never show in a diff")

    def test_created_mode_matches_a_plain_open(self):
        previous = os.umask(0)
        os.umask(previous)
        expected = 0o666 & ~previous

        target = self.tmp / "log.md"
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertEqual(stat.S_IMODE(os.stat(str(target)).st_mode), expected)


class TestBom(PrependCase):
    """Case: BOM on the existing file."""

    def test_bom_before_a_header_survives_and_the_entry_lands_first(self):
        target = self.copy_fixture("log-with-entries.md")
        write(target, BOM + read(target))
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)
        result = read(target)
        self.assertTrue(result.startswith(BOM), "the BOM must survive")
        self.assertLess(result.index(HEADING), result.index("## [2026-08-24]"))

    def test_bom_immediately_before_an_entry_heading(self):
        # Without detaching the BOM, `^` fails on that one line: a two-entry
        # headerless file anchors on entry 2 and splices into second place, and
        # a one-entry file takes the fresh-wiki row and lands at the END of a
        # file that demonstrably has an entry. Both silent.
        target = write(self.tmp / "log.md",
                       BOM + "## [2026-08-20] merge | VHS — VHS-27: only entry"
                             "\n\nbody\n")
        code, out, err = run_cli([str(target), "--guard", GUARD],
                                 ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out,
                      "must not take the fresh-wiki row")
        result = read(target)
        self.assertTrue(result.startswith(BOM + HEADING),
                        "expected <BOM><entry> with no separator, got "
                        "{!r}".format(result[:60]))
        self.assertLess(result.index(HEADING), result.index("## [2026-08-20]"))

    def test_bom_with_two_headerless_entries(self):
        target = write(self.tmp / "log.md",
                       BOM
                       + "## [2026-08-20] merge | VHS — VHS-27: first\n\nbody\n\n"
                       + "## [2026-08-19] merge | VHS — VHS-26: second\n\nbody\n")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        result = read(target)
        self.assertLess(result.index(HEADING), result.index("## [2026-08-20]"),
                        "must not splice into second place")


class TestEmDashRoundTrip(PrependCase):
    """Case: em dash + BOM round-trip."""

    def test_em_dash_survives_and_the_guard_still_matches(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  (BOM + ENTRY).encode("utf-8"))
        self.assertEqual(code, 0, err)

        result = read(target)
        self.assertNotIn(BOM, result, "the entry's BOM is stripped, not written")
        first_line = result[result.index(HEADING):].split("\n", 1)[0]
        self.assertTrue(first_line.startswith("## "), first_line)
        self.assertIn(GUARD, result)
        # Scoped to the entry this run wrote: the fixture's provenance comment
        # above the header legitimately contains `--`, and this assertion is
        # about the guard's em dash surviving, not the whole file's punctuation.
        entry_region = result[result.index(HEADING):result.index(BODY) + len(BODY)]
        self.assertIn("—", entry_region)
        self.assertNotIn("--", entry_region)

        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 1,
                         "the em dash must survive the round trip: "
                         + err)


class TestNewlines(PrependCase):
    """Case: newlines, all three directions."""

    def test_lf_file_stays_lf(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertEqual(read(target).count("\r"), 0)

    def test_crlf_entry_on_stdin_produces_no_cr(self):
        target = self.copy_fixture("log-with-entries.md")
        crlf_entry = ENTRY.replace("\n", "\r\n").encode("utf-8")
        code, _out, err = run_cli([str(target), "--guard", GUARD], crlf_entry)
        self.assertEqual(code, 0, err)
        self.assertEqual(read(target).count("\r"), 0)

    def test_crlf_target_keeps_crlf_except_the_boundary_line(self):
        # CRLF is constructed in-test, never checked in: root .gitattributes is
        # `*.md text eol=lf`, so a CRLF fixture cannot survive its own commit.
        target = write(self.tmp / "log.md",
                       read(FIXTURES / "log-with-entries.md").replace("\n", "\r\n"))
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)

        result = read(target)
        self.assertIn("> **Newest first.**", result)
        self.assertGreater(result.count("\r\n"), 5,
                           "untouched lines keep their CRLF")
        # The one bounded exception: the separator rule right-strips the text
        # above the insertion point and re-emits "\n\n", so that single boundary
        # line's terminator becomes LF. Pinned rather than waved away.
        boundary = "entries dated **2026-08-01 and later**."
        self.assertIn(boundary + "\n\n" + HEADING, result)
        self.assertNotIn(boundary + "\r\n", result)
        self.assertIn("out of contract — re-sort rather than leaving it.\r\n", result)

    def test_stderr_comes_back_as_utf8_with_lf(self):
        target = self.copy_fixture("log-with-entries.md")
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(target), "--guard", GUARD],
            input=ENTRY.encode("utf-8"),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(target), "--guard", GUARD],
            input=ENTRY.encode("utf-8"),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.returncode, 1)
        # Decodes strictly, carries the em dash, and is not CRLF-terminated.
        text = proc.stderr.decode("utf-8")
        self.assertIn(GUARD, text)
        self.assertNotIn(b"\r\n", proc.stderr)


class TestWhitespaceDiscipline(PrependCase):
    """Case: whitespace discipline."""

    def test_one_blank_line_on_each_side_in_the_normal_outcome(self):
        target = self.copy_fixture("log-with-entries.md")
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        result = read(target)
        self.assertIn("entries dated **2026-08-01 and later**.\n\n" + HEADING,
                      result)
        self.assertIn(BODY + "\n\n## [2026-08-24]", result)

    def test_no_leading_separator_when_nothing_precedes_the_anchor(self):
        new_text, outcome = self.module.splice(
            "## [2026-08-20] merge | VHS — VHS-27: only entry\n\nbody\n", ENTRY)
        self.assertEqual(outcome, "prepended")
        self.assertTrue(new_text.startswith(HEADING), repr(new_text[:40]))

    def test_no_leading_separator_on_an_empty_file(self):
        new_text, outcome = self.module.splice("", ENTRY)
        self.assertEqual(outcome, "fresh")
        self.assertEqual(new_text, ENTRY + "\n")

    def test_fresh_and_created_end_in_exactly_one_newline(self):
        created, outcome = self.module.splice(None, ENTRY)
        self.assertEqual(outcome, "created")
        self.assertTrue(created.endswith(BODY + "\n"))
        self.assertFalse(created.endswith("\n\n"))

        fresh, outcome = self.module.splice("# Wiki Log\n\nheader only.\n", ENTRY)
        self.assertEqual(outcome, "fresh")
        self.assertTrue(fresh.endswith(BODY + "\n"))
        self.assertFalse(fresh.endswith("\n\n"))

    def test_normal_outcome_leaves_a_missing_trailing_newline_alone(self):
        # The normal outcome splices at the top and touches nothing after the
        # anchor. Enforcing a one-newline tail here would mean rewriting bytes
        # the script did not author.
        target = self.copy_fixture("log-no-trailing-newline.md")
        original = read(target)
        self.assertFalse(original.endswith("\n"))
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)
        result = read(target)
        self.assertFalse(result.endswith("\n"), "the tail must be byte-identical")
        self.assertTrue(result.endswith(original[-80:]))

    def test_second_close_against_a_created_file(self):
        target = self.tmp / "log.md"
        code, _out, err = run_cli([str(target), "--guard", GUARD],
                                  ENTRY.encode("utf-8"))
        self.assertEqual(code, 0, err)

        second_heading = "## [2026-08-26] close | VHS — VHS-30: the next close"
        second = second_heading + "\n\nbody"
        code, out, err = run_cli([str(target), "--guard", "close | VHS — VHS-30:"],
                                 second.encode("utf-8"))
        self.assertEqual(code, 0, err)
        self.assertIn("prepend_log_entry_outcome=prepended", out)
        result = read(target)
        self.assertTrue(result.startswith(second_heading),
                        "a created file must not gain a leading blank line")

    def test_second_close_against_a_bom_prefixed_created_file(self):
        # The case that distinguishes deciding emptiness in stripped coordinates
        # from deciding it in the original text: '﻿' is not whitespace, so
        # in original coordinates the preceding text is non-empty and the result
        # would open with a spurious blank line.
        new_text, outcome = self.module.splice(BOM + ENTRY + "\n", ENTRY.replace(
            "VHS-29", "VHS-30"))
        self.assertEqual(outcome, "prepended")
        self.assertTrue(new_text.startswith(BOM + "## ["),
                        repr(new_text[:40]))


class TestNoStaleWording(unittest.TestCase):
    """Case: no stale wording survives."""

    def test_skill_md_has_no_append_or_grep_f(self):
        # A permanent tripwire: the word "append" is deliberately absent from
        # the four outcomes and the Phase 5 prose that transcribes them, and no
        # shell grep performs the log guard any more.
        text = SKILL_MD.read_text(encoding="utf-8")
        appends = [line for line in text.splitlines()
                   if re.search(r"append", line, re.I)]
        self.assertEqual(appends, [], "stale append wording in SKILL.md")
        greps = [line for line in text.splitlines() if "grep -F" in line]
        self.assertEqual(greps, [], "stale grep -F guard wording in SKILL.md")

    def test_agents_md_bullets_read_correctly(self):
        # Content, not a blanket count: AGENTS.md is a living cross-skill doc
        # that may legitimately use the word later, and a repo-wide ban asserted
        # from a spec-close-named suite would fail pointing at the wrong
        # subsystem. Located by substring, never by line index.
        lines = AGENTS_MD.read_text(encoding="utf-8").splitlines()

        close_bullet = [ln for ln in lines if "`/spec-close <spec-path>" in ln]
        self.assertEqual(len(close_bullet), 1, close_bullet)
        self.assertIn("prepend", close_bullet[0].lower())
        self.assertNotIn("append", close_bullet[0].lower())

        after_merge = [ln for ln in lines
                       if "run `/wiki-after-merge <commit-sha>`" in ln]
        self.assertEqual(len(after_merge), 1, after_merge)
        self.assertIn("prepend", after_merge[0].lower())
        self.assertNotIn("append", after_merge[0].lower())

    def test_missing_requires_backlog_no_longer_names_spec_close(self):
        text = PORTABLE_DOC.read_text(encoding="utf-8")
        backlog = [ln for ln in text.splitlines()
                   if "have no `requires:` block" in ln]
        self.assertEqual(len(backlog), 1, backlog)
        self.assertNotIn("`spec-close`", backlog[0])
        self.assertIn("`ship-spec`", backlog[0])
        self.assertIn("`review-pr`", backlog[0])


class TestInvocationString(PrependCase):
    """Case: invocation string — the only case that sees the shell layer.

    Every other process-level case hands subprocess a Python-built argv, which
    never exercises the quoting, the heredoc delimiter, or the exit capture.
    """

    def setUp(self):
        super().setUp()
        # Resolve bash once and invoke it by ABSOLUTE path. On Windows,
        # subprocess's PATH search finds System32\bash.exe — the WSL launcher —
        # which runs a Linux bash that cannot see `C:/...` at all, while
        # shutil.which() finds Git Bash. Spawning "bash" by name would silently
        # run the wrong one and report every path as missing.
        self.bash = shutil.which("bash")
        if self.bash is None:
            self.skipTest("bash not available")
        # A config dir laid out the way `python sync.py install` writes it, so
        # the documented ${CLAUDE_CONFIG_DIR:-$HOME/.claude} expansion resolves.
        self.config_dir = self.tmp / "config"
        scripts = self.config_dir / "skills" / "spec-close" / "scripts"
        scripts.mkdir(parents=True)
        shutil.copyfile(str(SCRIPT), str(scripts / SCRIPT.name))

        self.env = dict(os.environ)
        # Forward slashes deliberately: Python accepts them on Windows, and a
        # backslash path inside double quotes is consumed as escapes by bash.
        self.env["CLAUDE_CONFIG_DIR"] = str(self.config_dir).replace("\\", "/")

        probe = self._bash(
            "command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1"
            " && PY=python3 || PY=python\n"
            '"$PY" -c "print(1)"\n')
        if probe.returncode != 0:
            self.skipTest("no usable python on the bash PATH")

    def _bash(self, script: str):
        path = self.tmp / "invoke.sh"
        with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
            handle.write(script)
        return subprocess.run(
            [self.bash, str(path).replace("\\", "/")],
            env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def _invocation(self, log_path: Path, guard: str, heading: str) -> str:
        # SKILL.md's documented form, verbatim in structure: the variable
        # indirection, both quotings, the delimiter, and the exit capture.
        # `set -e` is present deliberately — a bare `python …; echo "$?"` loses
        # the value on exactly the two paths where it matters.
        # Substitution is by sentinel replace, never str.format: the documented
        # form contains `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`, whose braces
        # format() would read as a field and reject.
        template = (
            "set -e\n"
            'SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}'
            '/skills/spec-close/scripts/prepend_log_entry.py"\n'
            'LOGPATH="@LOGPATH@"\n'
            "command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1"
            " && PY=python3 || PY=python\n"
            'test -f "$SCRIPT" || { echo "not found at $SCRIPT"; exit 9; }\n'
            "if \"$PY\" \"$SCRIPT\" \"$LOGPATH\" --guard '@GUARD@' "
            "<<'PREPEND_LOG_ENTRY_EOF'\n"
            "@HEADING@\n"
            "\n"
            "Body prose with an em dash — and a `|` pipe.\n"
            "PREPEND_LOG_ENTRY_EOF\n"
            "then rc=0; else rc=$?; fi\n"
            'echo "prepend_log_entry_exit=$rc"\n'
        )
        return (template
                .replace("@LOGPATH@", str(log_path).replace("\\", "/"))
                .replace("@GUARD@", guard)
                .replace("@HEADING@", heading))

    def test_documented_form_lands_the_entry(self):
        target = self.copy_fixture("log-with-entries.md")
        proc = self._bash(self._invocation(target, GUARD, HEADING))
        stdout = proc.stdout.decode("utf-8")
        self.assertIn("prepend_log_entry_exit=0", stdout,
                      proc.stderr.decode("utf-8"))
        self.assertIn("prepend_log_entry_outcome=prepended", stdout)

        result = read(target)
        self.assertIn(HEADING, result)
        # A tilde-rendered path fails this; so does an unquoted guard (bash
        # would split ` | ` into a pipeline); so does a body line equal to the
        # delimiter.
        self.assertIn(GUARD, result, "the guard must survive with its em dash "
                                     "and pipe intact")
        self.assertLess(result.index(HEADING), result.index("## [2026-08-24]"))

    def test_failing_run_reports_a_nonzero_exit_token(self):
        # The assertion that would have caught `$?`-after-`fi`, which is always
        # 0 because both branches of the if end in an assignment — so a refusal,
        # a skip and a PermissionError would all report success forever.
        target = self.copy_fixture("log-with-entries.md")
        original = read(target)
        template_guard = "close | <PROJECT> — <TICKET-ID>:"
        proc = self._bash(self._invocation(
            target, template_guard,
            "## [2026-08-25] " + template_guard + " <title>"))
        stdout = proc.stdout.decode("utf-8")
        match = re.search(r"prepend_log_entry_exit=(\d+)", stdout)
        self.assertIsNotNone(match, stdout + proc.stderr.decode("utf-8"))
        self.assertNotEqual(match.group(1), "0", stdout)
        self.assertEqual(read(target), original)


class TestSkillDeclaration(unittest.TestCase):
    """Cases: `requires:` matches the body, and lint."""

    def test_requires_block_matches_the_tool_use_notes(self):
        # lint.py validates the vocabulary but never under-declaration, so the
        # fuller block lints identically to a thin one. Pin it against the body.
        text = SKILL_MD.read_text(encoding="utf-8")
        block = text.split("---", 2)[1]
        self.assertIn("requires:", block)
        declared = set(re.findall(r"^  ([a-z]+):", block, re.M))
        self.assertEqual(declared, {"shell", "filesystem", "network", "services"})
        self.assertNotIn("subagents", block)
        self.assertIn("filesystem: [read, write]", block)
        self.assertIn("network: true", block)
        self.assertIn("shell: true", block)
        self.assertIn("issue-tracker?", block)
        self.assertIn("shared-memory?", block)

    def test_lint_is_clean_including_warns(self):
        # `lint.py --strict` exits on ERROR only — WARNs never affect its exit
        # status, so the command line alone cannot enforce zero-WARN.
        findings = lint.lint_path(SKILL_MD)
        errors = [f for f in findings if f[0] == lint.ERROR]
        warns = [f for f in findings if f[0] == lint.WARN]
        self.assertEqual(errors, [], "unexpected ERROR(s): {}".format(errors))
        self.assertEqual(warns, [], "unexpected WARN(s): {}".format(warns))


if __name__ == "__main__":
    unittest.main(verbosity=2)
