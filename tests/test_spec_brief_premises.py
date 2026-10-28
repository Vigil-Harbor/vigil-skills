#!/usr/bin/env python3
"""Tests for spec-brief's check_premises.py (VHS-67, VHS-93).

Stdlib unittest. The script is loaded by file path, the same way
tests/test_spec_land.py loads land_check.py, so an import does not exit.
Subprocess cases run the script as a process and check the entry point.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "spec-brief" / "scripts" / "check_premises.py"
SKILL = REPO_ROOT / "skills" / "spec-brief" / "SKILL.md"

CODE_RE = re.compile(r"^premise: (\S+)", re.M)

RUN_RECORD = 'source: run: "python -m app.job"; exit: 0; excerpt: "wrote ledger"'
READ_SOURCE = "vendor/sdk.py:12"


def load_script(path, module_name):
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load script at {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def codes(err):
    return CODE_RE.findall(err)


def premise(pid, claim, level, source, override=None):
    lines = [
        "{}. **P{}.** {}".format(pid, pid, claim),
        "   **Level:** {}".format(level),
        "   **Source:** {}".format(source),
    ]
    if override is not None:
        lines.append("   **Override:** {}".format(override))
    return "\n".join(lines)


def brief_with(*blocks):
    return "\n".join(blocks) + "\n"


def sole_marker_brief():
    return brief_with(
        "## Decisions carried forward",
        "",
        "1. Keep the clock.",
        "",
        "## Premises",
        "",
        "_(no premises)_",
    )


class CheckPremisesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script(SCRIPT, "check_premises_vhs67")

    def run_bytes(self, raw):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_bytes(raw)
            before = path.read_bytes()
            out = __import__("io").StringIO()
            err = __import__("io").StringIO()
            from contextlib import redirect_stderr, redirect_stdout
            with redirect_stdout(out), redirect_stderr(err):
                code = self.mod.main([str(path)])
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(out.getvalue(), "")
            stderr = err.getvalue()
            if code == 0:
                self.assertEqual(stderr, "")
            return code, stderr

    def run_text(self, text, newline="\n", bom=False):
        body = text.replace("\n", newline)
        raw = body.encode("utf-8")
        if bom:
            raw = b"\xef\xbb\xbf" + raw
        return self.run_bytes(raw)

    def test_section_absent(self):
        code, err = self.run_text("# Brief\n\n## Done when\n\n- ships\n")
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["section-absent"])

    def test_sole_marker(self):
        code, err = self.run_text(sole_marker_brief())
        self.assertEqual(code, 0)
        self.assertEqual(err, "")

    # Regression for VHS-93: Decisions carry no Rests on line, and the script no longer reads them.
    def test_decisions_without_rests_on_pass(self):
        text = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock. The ticket says so.",
            "",
            "2. Drop the cache.",
            "",
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 0, err)

    # Regression for VHS-93: an unchecked premise needs the operator's reason.
    def test_unchecked_without_override(self):
        for source in ("none", "operator says the job writes first"):
            with self.subTest(source=source):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The job writes the ledger before it returns.", "unchecked", source),
                )
                code, err = self.run_text(text)
                self.assertEqual(code, 1)
                self.assertEqual(codes(err), ["unchecked"])

    def test_unchecked_with_override(self):
        text = brief_with(
            "## Premises",
            "",
            premise(
                1,
                "The job writes the ledger before it returns.",
                "unchecked",
                "none",
                override="operator accepts the vendor's documented behavior for this brief",
            ),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 0, err)

    # Regression for VHS-93: read and ran pass without an override.
    def test_read_and_ran_without_override(self):
        for level, source in (("read", READ_SOURCE), ("ran", RUN_RECORD)):
            with self.subTest(level=level):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The ledger file appears after the job command.", level, source),
                )
                code, err = self.run_text(text)
                self.assertEqual(code, 0, err)

    def test_level_missing_and_invalid(self):
        missing = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Source:** none",
        )
        code, err = self.run_text(missing)
        self.assertEqual(code, 1)
        self.assertIn("level-missing", codes(err))

        # Regression for VHS-93: the old five-level names are no longer levels.
        for level in ("said", "pointed", "walked", "reproduced", "Ran"):
            with self.subTest(level=level):
                invalid = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The vendor SDK injects the clock.", level, RUN_RECORD),
                )
                code, err = self.run_text(invalid)
                self.assertEqual(code, 1)
                self.assertEqual(codes(err), ["level-invalid"])

    # Regression for VHS-93: the dropped fields are unknown fields now.
    def test_dropped_fields_are_unknown(self):
        for line in ("   **Defeats ticket:** yes", "   **Kind:** text"):
            with self.subTest(line=line):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
                    line,
                )
                code, err = self.run_text(text)
                self.assertEqual(code, 1)
                self.assertEqual(codes(err), ["field-unknown"])

    def test_override_whitespace_only(self):
        for level, source in (("read", READ_SOURCE), ("unchecked", "none")):
            with self.subTest(level=level):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The vendor SDK injects the clock.", level, source, override="  "),
                )
                code, err = self.run_text(text)
                self.assertEqual(code, 1)
                self.assertEqual(codes(err), ["override-empty"])

    def test_item_id_gap(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "First claim.", "read", READ_SOURCE),
            "",
            "3. **P3.** Third claim.",
            "   **Level:** read",
            "   **Source:** vendor/sdk.py:30",
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("item-id", codes(err))

    def test_claim_missing(self):
        text = brief_with(
            "## Premises",
            "",
            "1. **P1.**",
            "   **Level:** read",
            "   **Source:** vendor/sdk.py:12",
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("claim-missing", codes(err))

    def test_fenced_item_is_section_empty(self):
        text = brief_with(
            "## Premises",
            "",
            "```",
            premise(1, "Hidden claim.", "read", READ_SOURCE),
            "```",
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["section-empty"])

    def test_unclosed_fence_hides_later_item(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
            "",
            "```",
            premise(2, "The job writes the ledger before it returns.", "unchecked", "none"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["fence-open"])

    def test_item_after_next_heading_is_not_a_premise(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
            "",
            "## Done when",
            "",
            premise(2, "The job writes the ledger before it returns.", "unchecked", "none"),
        )
        code, _err = self.run_text(text)
        self.assertEqual(code, 0)

    def test_bom_sole_marker(self):
        code, err = self.run_text(sole_marker_brief(), bom=True)
        self.assertEqual(code, 0)
        self.assertEqual(err, "")

    def test_section_duplicate(self):
        text = brief_with(
            "## Premises",
            "",
            "_(no premises)_",
            "",
            "## Done when",
            "",
            "- ships",
            "",
            "## Premises",
            "",
            premise(1, "The job writes the ledger before it returns.", "unchecked", "none"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["section-duplicate"])

    def test_field_unknown_and_duplicate(self):
        unknown = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Level:** read",
            "   **Source:** vendor/sdk.py:12",
            "   **Defeats:** yes",
        )
        code, err = self.run_text(unknown)
        self.assertEqual(code, 1)
        self.assertIn("field-unknown", codes(err))

        duplicate = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Level:** read",
            "   **Level:** ran",
            "   **Source:** vendor/sdk.py:12",
        )
        code, err = self.run_text(duplicate)
        self.assertEqual(code, 1)
        self.assertIn("field-duplicate", codes(err))

    def test_source_shapes(self):
        read = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", "no line here"),
        )
        code, err = self.run_text(read)
        self.assertEqual(code, 1)
        self.assertIn("source-invalid", codes(err))

        ran = brief_with(
            "## Premises",
            "",
            premise(1, "The ledger file appears after the job command.", "ran", READ_SOURCE),
        )
        code, err = self.run_text(ran)
        self.assertEqual(code, 1)
        self.assertIn("source-invalid", codes(err))

        for source in ("none", "operator says so"):
            with self.subTest(source=source):
                unchecked = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The vendor SDK injects the clock.", "unchecked", source, override="accepted"),
                )
                code, err = self.run_text(unchecked)
                self.assertEqual(code, 0, err)

    def test_item_unparsed_not_a_well_formed_next_item(self):
        bad = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
            "2. **P2** claim",
        )
        code, err = self.run_text(bad)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

        also = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
            "2. P2. claim",
        )
        code, err = self.run_text(also)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

        good = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "read", READ_SOURCE),
            "",
            premise(2, "The job writes the ledger before it returns.", "ran", RUN_RECORD),
        )
        code, _err = self.run_text(good)
        self.assertEqual(code, 0)

    def test_numbered_line_after_a_field_is_item_unparsed(self):
        text = "\n".join([
            "## Premises",
            "",
            "1. **P1.** The job writes the ledger before it returns.",
            "   **Level:** read",
            "   **Source:** skills/app/SKILL.md:10",
            "   2. skills/app/SKILL.md:40 opens the write.",
            "   **Override:** operator accepts the file for this brief",
            "",
        ])
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

    def test_deeply_indented_item_after_a_field_is_item_unparsed(self):
        text = "\n".join([
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "unchecked", "none", "fine"),
            "      2. **P2.** Hidden defeating claim.",
            "   **Level:** unchecked",
            "   **Source:** none",
            "",
        ])
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

    def test_unexpected_exception_exits_2(self):
        from unittest import mock

        with mock.patch.object(self.mod, "_run", side_effect=RuntimeError("boom")):
            code, err = self.run_text(sole_marker_brief())
        self.assertEqual(code, 2)
        self.assertIn("premise: error RuntimeError", err)

    def test_unreadable_paths(self):
        code, err = self.run_text_missing()
        self.assertEqual(code, 2)
        self.assertEqual(codes(err), ["unreadable"])

        code, err = self.run_bytes(b"\xff\xfe not utf-8 \x80")
        self.assertEqual(code, 2)
        self.assertEqual(codes(err), ["unreadable"])

        with tempfile.TemporaryDirectory() as directory:
            out = __import__("io").StringIO()
            err = __import__("io").StringIO()
            from contextlib import redirect_stderr, redirect_stdout
            with redirect_stdout(out), redirect_stderr(err):
                code = self.mod.main([directory])
            self.assertEqual(code, 2)
            self.assertEqual(out.getvalue(), "")
            self.assertEqual(codes(err.getvalue()), ["unreadable"])

    def run_text_missing(self):
        out = __import__("io").StringIO()
        err = __import__("io").StringIO()
        from contextlib import redirect_stderr, redirect_stdout
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "no-such-brief.md")
            with redirect_stdout(out), redirect_stderr(err):
                code = self.mod.main([missing])
        self.assertEqual(out.getvalue(), "")
        return code, err.getvalue()

    def test_quoted_heading_does_not_end_premises(self):
        text = brief_with(
            "## Premises",
            "",
            "> ## Done when",
            "",
            premise(1, "The job writes the ledger before it returns.", "unchecked", "none"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["unchecked"])

    def test_marker_and_items_only(self):
        text = brief_with(
            "## Premises",
            "",
            "_(no premises)_",
            "",
            premise(1, "The job writes the ledger before it returns.", "unchecked", "none"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["marker-and-items"])

    def test_crlf_and_lf(self):
        text = sole_marker_brief()
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                code, err = self.run_text(text, newline=newline)
                self.assertEqual(code, 0)
                self.assertEqual(err, "")

    def test_usage_arity(self):
        from contextlib import redirect_stderr, redirect_stdout
        for argv in ([], ["a", "b"]):
            with self.subTest(argv=argv):
                out = __import__("io").StringIO()
                err = __import__("io").StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    code = self.mod.main(argv)
                self.assertEqual(code, 2)
                self.assertEqual(out.getvalue(), "")
                self.assertEqual(codes(err.getvalue()), ["usage"])

    def test_em_dash_claim_emits_data_code(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The ledger — the real one — is written before return.", "unchecked", "none"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["unchecked"])
        self.assertNotIn("error", codes(err))

    def test_subprocess_entry_point(self):
        defeating = brief_with(
            "## Premises",
            "",
            premise(1, "The job writes the ledger before it returns.", "unchecked", "none"),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_bytes(defeating.encode("utf-8"))
            before = path.read_bytes()
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertEqual(proc.stdout, b"")
            self.assertIn(b"premise: unchecked", proc.stderr)
            self.assertEqual(path.read_bytes(), before)

            path.write_bytes(sole_marker_brief().encode("utf-8"))
            before = path.read_bytes()
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(proc.stdout, b"")
            self.assertEqual(proc.stderr, b"")
            self.assertEqual(path.read_bytes(), before)

    def test_skill_contains_the_gate_contract(self):
        text = SKILL.read_text(encoding="utf-8")
        for needle in (
            "check_premises.py",
            "## Premises",
            "_(no premises)_",
            "tier needs an operator — stopping",
            "premise gate: check_premises.py did not run",
            "writing without the check",
            "Write blocked",
            "A premise at ran with no matching run record in this invocation's Grill summary is demoted.",
            "Write the temp from the candidate after override lines are on the items.",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)

    # Regression for VHS-93: the removed premise model must not drift back in.
    def test_skill_drops_the_old_premise_model(self):
        text = SKILL.read_text(encoding="utf-8")
        for needle in (
            "reproduced",
            "**Rests on:**",
            "**Below ran:**",
            "**Kind:**",
            "Defeats ticket",
            "notice_armed",
            "Tweak surfaces",
        ):
            with self.subTest(needle=needle):
                self.assertNotIn(needle, text)

    # Regression for VHS-93: anti-regrowth tripwire for the VHS-90 simplification epic.
    def test_skill_word_budget(self):
        words = len(SKILL.read_text(encoding="utf-8").split())
        self.assertLessEqual(words, 5800)


if __name__ == "__main__":
    unittest.main()
