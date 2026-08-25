#!/usr/bin/env python3
"""Tests for the session-handoff skill (VHS-28).

Stdlib unittest. Run directly: `python tests/test_session_handoff.py`.
Resolves the repo root and all paths from __file__ (never cwd) so it works
regardless of the working directory ship-spec runs it from.

The skill's scripts are loaded by file path so they can stay portable scripts
without package boilerplate, matching tests/test_talaria_bridge.py.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime as real_datetime
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import lint  # noqa: E402

SKILL_DIR = REPO_ROOT / "skills" / "session-handoff"
SCRIPTS_DIR = SKILL_DIR / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "session-handoff"


def load_script(path: Path, module_name: str):
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load script at {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_sections():
    return load_script(SCRIPTS_DIR / "_sections.py", "session_handoff_sections_under_test")


def load_creator():
    return load_script(SCRIPTS_DIR / "create_handoff.py", "session_handoff_create_under_test")


def load_validator():
    return load_script(SCRIPTS_DIR / "validate_handoff.py", "session_handoff_validate_under_test")


@contextlib.contextmanager
def pushd(path: Path):
    """Pin the process CWD for the duration, then restore it.

    Every path here resolves from __file__, never cwd, so the suite passes from
    any working directory - but one test needs the CWD to sit inside a
    repository to prove anything, and it must not leak that to its neighbours.
    """
    previous = Path.cwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(str(previous))


def run_main(module, argv: list[str]):
    """Call main(argv) and capture its streams. Exit codes are asserted on the
    returned int, never via SystemExit."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = module.main(argv)
    return code, out.getvalue(), err.getvalue()


def headings_of(sections, text: str) -> list[str]:
    """Every ATX heading title, in document order.

    Deliberately reaches for the module's private matcher: the point of this
    helper is to observe exactly what the one shared matcher sees.
    """
    return [m.group(2).strip() for m in sections._HEADING_RE.finditer(text)]


def matched_names(sections) -> list[str]:
    return [name for _, name, cls in sections.TEMPLATE_SECTIONS
            if cls in ("required", "recommended")]


def fill_markers(sections, text: str) -> str:
    return sections.TODO_MARKER_RE.sub("written by the author", text)


def git_env() -> dict:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def init_repo(path: Path, subject: str = "init") -> None:
    """A one-commit repository, with signing and hooks kept out of the way."""
    env = git_env()

    def git(*args):
        subprocess.run(["git"] + list(args), cwd=str(path), env=env,
                       check=True, capture_output=True)

    git("init", "-q")
    git("symbolic-ref", "HEAD", "refs/heads/main")
    git("config", "user.email", "vhs28@example.invalid")
    git("config", "user.name", "VHS-28 Test")
    git("config", "commit.gpgsign", "false")
    (path / "README.md").write_text("seed\n", encoding="utf-8", newline="\n")
    git("add", "README.md")
    git("commit", "-q", "--no-verify", "-m", subject)


def minimal_document(extra: str = "") -> str:
    """The smallest document that satisfies every required section."""
    return (
        "# Handoff: minimal\n\n"
        "## Current State Summary\n\nthe work stands here\n\n"
        "## Immediate Next Steps\n\n1. do the next thing\n\n"
        "## Important Context\n\nthe thing that would otherwise be missed\n"
        + extra
    )


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.addCleanup(self._tmp.cleanup)

    def write(self, name: str, text: str, encoding: str = "utf-8") -> Path:
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding=encoding, newline="")
        return path

    def handoffs_dir(self, project: Path | None = None) -> Path:
        return (project or self.tmp) / ".claude" / "handoffs"


# --- 1. Heading matcher: the filed bug ---------------------------------------

class TestHeadingMatcher(unittest.TestCase):
    def setUp(self):
        self.S = load_sections()

    def norm(self, text: str) -> str:
        return self.S.normalize(text.encode("utf-8"))

    def test_level3_section_is_found(self):
        # Regression for VHS-28: the vendor patterns capped at `##`, so no `###`
        # section could ever be seen and every nested handoff reported missing.
        text = self.norm("# Doc\n\n### Current State Summary\n\nreal content\n")
        self.assertTrue(self.S.has_section(text, "Current State Summary"))

    def test_absent_section_reports_missing(self):
        # Regression for VHS-28: depth-blindness must not become name-blindness.
        text = self.norm("# Doc\n\n## Something Else\n\ncontent\n")
        self.assertFalse(self.S.has_section(text, "Current State Summary"))

    def test_same_name_matches_at_every_depth(self):
        for depth in range(1, 7):
            with self.subTest(depth=depth):
                text = self.norm("#" * depth + " Important Context\n")
                self.assertTrue(self.S.has_section(text, "Important Context"))

    def test_seven_hashes_is_not_a_heading(self):
        text = self.norm("####### Important Context\n")
        self.assertFalse(self.S.has_section(text, "Important Context"))

    def test_missing_separator_is_not_a_heading(self):
        for line in ("#Important Context", "##Important Context"):
            with self.subTest(line=line):
                self.assertFalse(self.S.has_section(self.norm(line + "\n"),
                                                    "Important Context"))

    def test_indent_boundary(self):
        self.assertTrue(self.S.has_section(self.norm("   ## Important Context\n"),
                                           "Important Context"))
        self.assertFalse(self.S.has_section(self.norm("    ## Important Context\n"),
                                            "Important Context"))

    def test_closing_run_is_stripped(self):
        text = self.norm("## Important Context ##\n")
        self.assertTrue(self.S.has_section(text, "Important Context"))

    def test_name_comparison_is_case_insensitive(self):
        text = self.norm("## iMPORTANT cONTEXT\n")
        self.assertTrue(self.S.has_section(text, "Important Context"))

    def test_prefix_name_does_not_collide(self):
        # Comparison is by name, never by interpolating the name into a regex -
        # which is what created the vendor's substring-collision failure.
        text = self.norm("## Important Context Notes\n")
        self.assertFalse(self.S.has_section(text, "Important Context"))
        both = self.norm("## Important Context Notes\n\n### Important Context\n")
        self.assertTrue(self.S.has_section(both, "Important Context"))

    def test_first_heading_title(self):
        self.assertEqual(self.S.first_heading_title(self.norm("## Two\n\n# One\n")), "One")
        self.assertIsNone(self.S.first_heading_title(self.norm("## Only Two\n")))
        self.assertIsNone(self.S.first_heading_title(self.norm("# \n")))

    def test_derived_name_tables(self):
        self.assertEqual(
            self.S.REQUIRED_SECTIONS,
            ("Current State Summary", "Immediate Next Steps", "Important Context"),
        )
        self.assertEqual(len(self.S.RECOMMENDED_SECTIONS), 6)


# --- 2. Template round-trip --------------------------------------------------

class TestTemplateRoundTrip(TempDirCase):
    def setUp(self):
        super().setUp()
        self.S = load_sections()
        self.C = load_creator()
        self.V = load_validator()

    def scaffold(self, slug: str = "round-trip") -> Path:
        code, out, err = run_main(self.C, [slug, "--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        return Path(out.strip())

    def test_scaffold_headings_match_the_class_column_in_order(self):
        text = self.S.normalize(self.scaffold().read_bytes())
        expected = matched_names(self.S)
        wanted = set(expected)
        found = [h for h in headings_of(self.S, text) if h in wanted]
        self.assertEqual(found, expected)

    def test_scaffold_has_exactly_one_marker_per_matched_section(self):
        text = self.S.normalize(self.scaffold().read_bytes())
        for name in matched_names(self.S):
            with self.subTest(name=name):
                self.assertEqual(text.count(self.S.todo_marker(name)), 1)
        # The per-name assertion above is what makes this non-vacuous: a bare
        # count cannot tell nine right sections from nine markers in one.
        self.assertEqual(len(self.S.TODO_MARKER_RE.findall(text)), 9)

    def test_files_modified_marker_sits_outside_the_generated_table(self):
        text = self.S.normalize(self.scaffold().read_bytes())
        marker = self.S.todo_marker("Files Modified")
        lines = text.split("\n")
        self.assertIn(marker, lines)
        for line in lines:
            if line.startswith("|"):
                self.assertIsNone(self.S.TODO_MARKER_RE.search(line))

    def test_filled_scaffold_validates_ready(self):
        path = self.scaffold()
        path.write_text(fill_markers(self.S, path.read_text(encoding="utf-8")),
                        encoding="utf-8", newline="\n")
        text = self.S.normalize(path.read_bytes())
        self.assertEqual([n for n in self.S.REQUIRED_SECTIONS
                          if not self.S.has_section(text, n)], [])
        code, out, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, out)
        self.assertIn("VERDICT: READY", out)

    def test_unfilled_scaffold_is_not_ready(self):
        code, out, _ = run_main(self.V, [str(self.scaffold())])
        self.assertEqual(code, 1)
        self.assertIn("VERDICT: NEEDS WORK", out)


# --- 3. Legacy-corpus compatibility, both shapes -----------------------------

class TestLegacyCorpus(unittest.TestCase):
    def setUp(self):
        self.S = load_sections()
        self.V = load_validator()

    def test_both_on_disk_shapes_validate(self):
        # Regression for VHS-28: `legacy-nested.md` is the shape the capped
        # pattern could not see. Both are authored fixtures, not copies.
        for name in ("legacy-flat.md", "legacy-nested.md"):
            with self.subTest(fixture=name):
                path = FIXTURES / name
                text = self.S.normalize(path.read_bytes())
                missing = [n for n in self.S.REQUIRED_SECTIONS
                           if not self.S.has_section(text, n)]
                self.assertEqual(missing, [])
                code, out, _ = run_main(self.V, [str(path)])
                self.assertEqual(code, 0, out)
                self.assertIn("VERDICT: READY", out)


# --- 4. Verdict / exit matrix ------------------------------------------------

class TestVerdictMatrix(TempDirCase):
    def setUp(self):
        super().setUp()
        self.S = load_sections()
        self.V = load_validator()

    def verdict(self, text: str, name: str = "doc.md"):
        path = self.write(name, text)
        code, out, _ = run_main(self.V, [str(path)])
        return code, out

    def test_clean_document_is_ready(self):
        code, out = self.verdict(minimal_document())
        self.assertEqual(code, 0)
        self.assertIn("VERDICT: READY", out)

    def test_unfilled_placeholder_is_needs_work(self):
        code, out = self.verdict(minimal_document(
            "\n" + self.S.todo_marker("Potential Gotchas") + "\n"))
        self.assertEqual(code, 1)
        self.assertIn("VERDICT: NEEDS WORK", out)

    def test_absent_required_heading_is_needs_work(self):
        text = minimal_document().replace("## Important Context", "## Other Notes")
        code, out = self.verdict(text)
        self.assertEqual(code, 1)
        self.assertIn("MISSING: Important Context", out)

    def test_env_style_assignment_blocks(self):
        code, out = self.verdict(minimal_document(
            "\nAPI_KEY=AKIAIOSFODNN7EXAMPLE\n"))
        self.assertEqual(code, 2)
        self.assertIn("VERDICT: BLOCKED", out)
        self.assertIn("generic assignment (api_key)", out)

    def test_branded_prefix_blocks(self):
        code, out = self.verdict(minimal_document(
            "\nthe key was sk-ant-api03-AAAABBBBCCCCDDDDEEEEFFFF in the log\n"))
        self.assertEqual(code, 2)
        self.assertIn("VERDICT: BLOCKED", out)

    def test_secrets_outrank_placeholders(self):
        code, out = self.verdict(minimal_document(
            "\n" + self.S.todo_marker("Important Context") +
            "\nAPI_KEY=AKIAIOSFODNN7EXAMPLE\n"))
        self.assertEqual(code, 2)
        self.assertIn("VERDICT: BLOCKED", out)
        # No short-circuit: the placeholder is still reported.
        self.assertIn("Placeholders remaining:", out)
        self.assertIn("[TODO: Important Context", out)

    def test_prose_near_miss_does_not_block(self):
        code, out = self.verdict(minimal_document(
            "\nThe auth token is refreshed by the loader.\n"
            "Rotation policy - token: rotated-nightly\n"))
        self.assertEqual(code, 0, out)

    def test_short_generic_value_is_fully_masked(self):
        # D6: first-4/last-4 on an 8-character value reproduces it in full, so
        # at 12 or fewer the excerpt names the pattern and the length instead.
        # (A literal "no character of the value appears" assertion is not
        # writable - the pattern name and the word "chars" share letters with
        # any value - so the value and both 4-character halves are pinned.)
        value = "Zq7-Xv9w"
        code, out = self.verdict(minimal_document("\npassword=" + value + "\n"))
        self.assertEqual(code, 2)
        self.assertIn("8 chars, fully masked", out)
        self.assertNotIn(value, out)
        self.assertNotIn(value[:4], out)
        self.assertNotIn(value[-4:], out)

    def test_long_value_keeps_only_its_ends(self):
        value = "AKIAIOSFODNN7EXAMPLE"
        code, out = self.verdict(minimal_document("\nclient_secret=" + value + "\n"))
        self.assertEqual(code, 2)
        self.assertIn(value[:4] + "*" * (len(value) - 8) + value[-4:], out)
        self.assertNotIn(value, out)

    def test_missing_file_and_no_argument_are_usage_errors(self):
        code, out, err = run_main(self.V, [str(self.tmp / "nope.md")])
        self.assertEqual(code, 3)
        self.assertNotIn("VERDICT", out)
        self.assertTrue(err.strip())
        code, out, err = run_main(self.V, [])
        self.assertEqual(code, 3)
        self.assertNotIn("VERDICT", out)
        self.assertTrue(err.strip())


# --- 5. Accepted limits (D0), pinned as decisions -----------------------------

class TestAcceptedLimits(TempDirCase):
    def setUp(self):
        super().setUp()
        self.S = load_sections()
        self.V = load_validator()

    def test_placeholder_inside_a_fence_still_trips(self):
        # Documented limit: the validator does not parse markdown, so a quoted
        # marker is still a marker. Clearable by rewording.
        path = self.write("doc.md", minimal_document(
            "\n```\n[TODO: quoted from another handoff]\n```\n"))
        code, out, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 1)
        self.assertIn("VERDICT: NEEDS WORK", out)

    def test_heading_inside_a_fence_satisfies_presence(self):
        # Documented limit: a false pass, never a false fail.
        text = minimal_document().replace("## Current State Summary",
                                          "## Renamed Summary")
        text += "\n```\n# Current State Summary\n```\n"
        path = self.write("doc.md", text)
        code, out, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, out)

    def test_quoted_handoff_headings_satisfy_presence(self):
        quoted = ("```\n## Current State Summary\n## Immediate Next Steps\n"
                  "## Important Context\n```\n")
        path = self.write("doc.md", "# Quoting another handoff\n\n" + quoted)
        code, out, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, out)


# --- 6. Encoding --------------------------------------------------------------

class TestEncoding(TempDirCase):
    def setUp(self):
        super().setUp()
        self.S = load_sections()
        self.C = load_creator()
        self.V = load_validator()

    def test_scaffold_is_lf_not_crlf(self):
        # Without newline="\n" on the write, every scaffold would be CRLF and
        # the skill would fail to validate its own output.
        code, out, err = run_main(self.C, ["lf-check", "--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        self.assertNotIn(b"\r", Path(out.strip()).read_bytes())

    def test_non_ascii_commit_subject_writes(self):
        project = self.tmp / "repo"
        project.mkdir()
        init_repo(project, subject="\U0001F389 celebrate the parser")
        code, out, err = run_main(self.C, ["emoji", "--project-path", str(project)])
        self.assertEqual(code, 0, err)
        text = Path(out.strip()).read_text(encoding="utf-8")
        self.assertIn("\U0001F389 celebrate the parser", text)

    def test_crlf_document_validates_with_zero_missing(self):
        # Regression for VHS-28: under re.MULTILINE a stray \r is absorbed into
        # the title group, so every required section of a CRLF document reports
        # missing - the ticket's headline symptom.
        path = self.tmp / "crlf.md"
        path.write_bytes(minimal_document().replace("\n", "\r\n").encode("utf-8"))
        text = self.S.normalize(path.read_bytes())
        self.assertEqual([n for n in self.S.REQUIRED_SECTIONS
                          if not self.S.has_section(text, n)], [])
        code, out, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, out)

    def test_bom_document_validates(self):
        path = self.tmp / "bom.md"
        path.write_bytes(b"\xef\xbb\xbf" + minimal_document().encode("utf-8"))
        code, out, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, out)


# --- 7. Scaffold robustness ---------------------------------------------------

class TestScaffoldRobustness(TempDirCase):
    def setUp(self):
        super().setUp()
        self.S = load_sections()
        self.C = load_creator()
        self.V = load_validator()

    def test_git_failure_placeholders_are_not_markers(self):
        # A direct unit assertion, needing no repository: a git placeholder
        # written in the marker shape would make every CREATE outside a repo
        # permanently un-READY, with nothing for the author to replace.
        for placeholder in (self.C.NOT_A_REPO, self.C.NO_COMMITS,
                            self.C.GIT_UNAVAILABLE):
            with self.subTest(placeholder=placeholder):
                self.assertIsNone(self.S.TODO_MARKER_RE.search(placeholder))
                self.assertTrue(placeholder.startswith("_"))
                self.assertTrue(placeholder.endswith("_"))

    def test_outside_a_repository_states_the_case_and_still_reaches_ready(self):
        # The process CWD is pinned *inside* a repository while the target
        # project is outside one, so the not-a-repo placeholder can only come
        # from the cwd= plumbing. Without it, git would answer about the
        # repository the caller happens to be standing in - which succeeds, and
        # so fails silently, filling the field RESUME trusts most with the
        # wrong branch and the wrong commits.
        with pushd(REPO_ROOT):
            self.assertTrue((Path.cwd() / ".git").exists(),
                            "CWD must sit inside a repository for this to prove anything")
            code, out, err = run_main(self.C, ["orphan", "--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        path = Path(out.strip())
        text = path.read_text(encoding="utf-8")
        self.assertIn(self.C.NOT_A_REPO, text)
        path.write_text(fill_markers(self.S, text), encoding="utf-8", newline="\n")
        code, report, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, report)

    def test_creates_the_handoffs_directory(self):
        self.assertFalse(self.handoffs_dir().exists())
        code, out, err = run_main(self.C, ["fresh", "--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        self.assertTrue(self.handoffs_dir().is_dir())

    def test_slug_sanitizing_and_cap(self):
        self.assertEqual(self.C.sanitize_slug("Fix The  Thing!!"), "fix-the-thing")
        self.assertEqual(self.C.sanitize_slug("---"), "handoff")
        self.assertEqual(self.C.sanitize_slug(""), "handoff")
        self.assertEqual(len(self.C.sanitize_slug("x" * 300)), self.C.MAX_SLUG_CHARS)

    def test_long_slug_still_writes_a_valid_file(self):
        code, out, err = run_main(self.C, ["a" * 300, "--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        path = Path(out.strip())
        self.assertTrue(path.is_file())
        # stem is YYYY-MM-DD-HHMMSS-<slug>, so the slug is the fifth field.
        self.assertLessEqual(len(path.stem.split("-", 4)[-1]), self.C.MAX_SLUG_CHARS)

    def test_continues_from_not_found_writes_nothing(self):
        code, out, err = run_main(self.C, [
            "chained", "--project-path", str(self.tmp),
            "--continues-from", "no-such-handoff.md"])
        self.assertNotEqual(code, 0)
        self.assertIn("does not exist", err)
        self.assertEqual(list(self.handoffs_dir().glob("*")) if
                         self.handoffs_dir().exists() else [], [])

    def test_continues_from_escape_writes_nothing(self):
        outside = self.write("elsewhere.md", "# Elsewhere\n")
        code, out, err = run_main(self.C, [
            "chained", "--project-path", str(self.tmp),
            "--continues-from", str(outside)])
        self.assertNotEqual(code, 0)
        self.assertIn("must name a file in", err)
        self.assertEqual(list(self.handoffs_dir().glob("*")) if
                         self.handoffs_dir().exists() else [], [])

    def test_failed_render_leaves_the_directory_untouched(self):
        handoffs = self.handoffs_dir()
        handoffs.mkdir(parents=True)
        before = sorted(p.name for p in handoffs.iterdir())
        with mock.patch.object(self.C.os, "replace", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                run_main(self.C, ["doomed", "--project-path", str(self.tmp)])
        self.assertEqual(sorted(p.name for p in handoffs.iterdir()), before)

    def test_successful_create_leaves_no_claim_behind(self):
        code, out, err = run_main(self.C, ["tidy", "--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        self.assertEqual(list(self.handoffs_dir().glob("*.tmp")), [])

    def test_collision_appends_a_suffix_with_the_claim_still_present(self):
        handoffs = self.handoffs_dir()
        handoffs.mkdir(parents=True)
        stem = "2026-01-02-030405-dup"
        (handoffs / (stem + ".md")).write_text("existing\n", encoding="utf-8")
        (handoffs / (stem + ".md.tmp")).write_text("", encoding="utf-8")
        target, claim = self.C.claim_stem(handoffs, stem)
        self.assertEqual(target.name, stem + "-2.md")
        self.assertEqual(claim.name, stem + "-2.md.tmp")

    def test_collision_appends_a_suffix_with_the_claim_removed(self):
        # The case that fails if only FileExistsError on the .tmp is tested:
        # the claim is a reservation for `<stem>.md`, not the document itself.
        handoffs = self.handoffs_dir()
        handoffs.mkdir(parents=True)
        stem = "2026-01-02-030405-dup"
        (handoffs / (stem + ".md")).write_text("existing\n", encoding="utf-8")
        target, claim = self.C.claim_stem(handoffs, stem)
        self.assertEqual(target.name, stem + "-2.md")

    def test_same_second_collision_does_not_clobber(self):
        frozen = real_datetime(2026, 1, 2, 3, 4, 5)
        with mock.patch.object(self.C, "datetime") as clock:
            clock.now.return_value = frozen
            code, first, err = run_main(self.C, ["dup", "--project-path", str(self.tmp)])
            self.assertEqual(code, 0, err)
            code, second, err = run_main(self.C, ["dup", "--project-path", str(self.tmp)])
            self.assertEqual(code, 0, err)
        first_path, second_path = Path(first.strip()), Path(second.strip())
        self.assertNotEqual(first_path, second_path)
        self.assertTrue(second_path.name.endswith("-2.md"))
        self.assertIn("# Handoff: dup", first_path.read_text(encoding="utf-8"))
        self.assertEqual(list(self.handoffs_dir().glob("*.tmp")), [])

    def test_todo_shaped_commit_subject_is_neutralized(self):
        project = self.tmp / "repo"
        project.mkdir()
        init_repo(project, subject="[TODO] wire up X")
        code, out, err = run_main(self.C, ["neutral", "--project-path", str(project)])
        self.assertEqual(code, 0, err)
        path = Path(out.strip())
        text = path.read_text(encoding="utf-8")
        self.assertIn("&#91;TODO] wire up X", text)
        path.write_text(fill_markers(self.S, text), encoding="utf-8", newline="\n")
        code, report, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, report)

    def test_todo_shaped_predecessor_title_is_neutralized(self):
        handoffs = self.handoffs_dir()
        handoffs.mkdir(parents=True)
        prior = handoffs / "2026-01-01-000000-prior.md"
        prior.write_text("# [TODO] finish the migration\n", encoding="utf-8", newline="\n")
        code, out, err = run_main(self.C, [
            "after", "--project-path", str(self.tmp),
            "--continues-from", prior.name])
        self.assertEqual(code, 0, err)
        path = Path(out.strip())
        text = path.read_text(encoding="utf-8")
        self.assertIn("&#91;TODO] finish the migration", text)
        path.write_text(fill_markers(self.S, text), encoding="utf-8", newline="\n")
        code, report, _ = run_main(self.V, [str(path)])
        self.assertEqual(code, 0, report)


# --- 8. Chain round-trip ------------------------------------------------------

class TestChain(TempDirCase):
    def setUp(self):
        super().setUp()
        self.S = load_sections()
        self.C = load_creator()

    def create(self, *argv) -> Path:
        code, out, err = run_main(self.C, list(argv) + ["--project-path", str(self.tmp)])
        self.assertEqual(code, 0, err)
        return Path(out.strip())

    def chain_block(self, path: Path) -> list[str]:
        lines = path.read_text(encoding="utf-8").split("\n")
        start = next(i for i, line in enumerate(lines)
                     if line.startswith("- **Continues from**"))
        return lines[start:start + 2]

    def test_fresh_start_line(self):
        block = self.chain_block(self.create("solo"))
        self.assertEqual(block[0], "- **Continues from**: None (fresh start)")

    def test_chain_round_trip(self):
        first = self.create("first-leg")
        second = self.create("second-leg", "--continues-from", first.name)
        block = self.chain_block(second)
        self.assertEqual(
            block[0], "- **Continues from**: [{0}](./{0})".format(first.name))
        self.assertEqual(block[1], "  - Previous title: Handoff: first leg")
        href = re.search(r"\]\(\./([^)]+)\)", block[0]).group(1)
        self.assertTrue((self.handoffs_dir() / href).is_file())
        self.assertEqual((self.handoffs_dir() / href).resolve(), first.resolve())

    def test_hostile_predecessor_title_is_truncated_then_escaped(self):
        handoffs = self.handoffs_dir()
        handoffs.mkdir(parents=True)
        prior = handoffs / "2026-01-01-000000-hostile.md"
        title = "pipes | and `backticks` " + "x" * 200
        prior.write_text("# " + title + "\n", encoding="utf-8", newline="\n")
        block = self.chain_block(self.create("after", "--continues-from", prior.name))
        shown = block[1].split("Previous title: ", 1)[1]
        self.assertIn("|", shown)               # bullets are not table cells
        self.assertIn("\\`", shown)             # backticks are escaped
        self.assertTrue(shown.endswith("…"))
        self.assertLessEqual(len(shown.replace("\\", "")),
                             self.C.MAX_PREVIOUS_TITLE_CHARS)

    def test_predecessor_without_a_usable_h1_falls_back_to_the_filename(self):
        handoffs = self.handoffs_dir()
        handoffs.mkdir(parents=True)
        cases = {"2026-01-01-000000-none.md": "## Only Level Two\n",
                 "2026-01-01-000000-empty.md": "# \n\n## Body\n"}
        for name, body in cases.items():
            with self.subTest(name=name):
                (handoffs / name).write_text(body, encoding="utf-8", newline="\n")
                block = self.chain_block(
                    self.create("after-" + name[:10], "--continues-from", name))
                self.assertEqual(block[1], "  - Previous title: " + name)


# --- 9. Session-id validation (the shape SKILL.md declares) -------------------

class TestSessionIdShape(unittest.TestCase):
    """The UUID gate is agent-executed prose, so what ships is the declared
    pattern. This pins that pattern's behavior rather than aspiration."""

    def setUp(self):
        body = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        found = re.search(r"\^\[0-9a-fA-F\]\{8\}[^`\n]*\$", body)
        self.assertIsNotNone(found, "SKILL.md must declare the session-id pattern")
        self.pattern = re.compile(found.group(0))
        self.body = body

    def test_full_match_is_declared(self):
        # `$` also matches before a trailing newline, so "<uuid>\n" from a shell
        # substitution would reach the filesystem lookup.
        self.assertIn("full", self.body.lower())

    def test_canonical_id_is_accepted(self):
        self.assertIsNotNone(
            self.pattern.fullmatch("3f2504e0-4f89-11d3-9a0c-0305e82c3301"))

    def test_malformed_traversal_and_trailing_newline_are_rejected(self):
        for bad in ("not-a-uuid",
                    "../../etc/passwd",
                    "3f2504e0-4f89-11d3-9a0c-0305e82c33",
                    "3f2504e0-4f89-11d3-9a0c-0305e82c3301/../secrets",
                    "3f2504e0-4f89-11d3-9a0c-0305e82c3301\n"):
            with self.subTest(bad=bad):
                self.assertIsNone(self.pattern.fullmatch(bad))


# --- 10/11. Lint and inventory -----------------------------------------------

class TestSkillLint(unittest.TestCase):
    def test_skill_lints_clean(self):
        # `lint.py --strict` exits non-zero only on ERRORs, so the console
        # command cannot check the WARN half; assert programmatically.
        findings = lint.lint_path(SKILL_DIR / "SKILL.md")
        self.assertEqual([f for f in findings if f[0] == lint.ERROR], [])
        self.assertEqual([f for f in findings if f[0] == lint.WARN], [])

    def test_skill_ships_in_the_inventory(self):
        shipped = {p.parent.name for p in (REPO_ROOT / "skills").glob("*/SKILL.md")}
        self.assertIn("session-handoff", shipped)


if __name__ == "__main__":
    unittest.main()
