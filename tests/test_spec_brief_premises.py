#!/usr/bin/env python3
"""Tests for spec-brief's check_premises.py (VHS-67).

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


def premise(pid, claim, level, source, flag, override=None):
    lines = [
        "{}. **P{}.** {}".format(pid, pid, claim),
        "   **Level:** {}".format(level),
        "   **Source:** {}".format(source),
        "   **Defeats ticket:** {}".format(flag),
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
        "   **Rests on:** none",
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

    def test_sole_marker_and_rests_on_none(self):
        code, err = self.run_text(sole_marker_brief())
        self.assertEqual(code, 0)
        self.assertEqual(err, "")

    def test_defeating_below_ran_without_override(self):
        for level, source in (
            ("said", "none"),
            ("pointed", "vendor/sdk.py:12"),
            ("walked", "1. skills/app/SKILL.md:10 opens the job."),
        ):
            with self.subTest(level=level):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The job writes the ledger before it returns.", level, source, "yes"),
                )
                code, err = self.run_text(text)
                self.assertEqual(code, 1)
                self.assertEqual(codes(err), ["below-ran"])

    def test_defeating_below_ran_with_override(self):
        for level, source in (
            ("said", "none"),
            ("pointed", "vendor/sdk.py:12"),
            ("walked", "1. skills/app/SKILL.md:10 opens the job."),
        ):
            with self.subTest(level=level):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(
                        1,
                        "The job writes the ledger before it returns.",
                        level,
                        source,
                        "yes",
                        override="operator accepts the trace for this brief",
                    ),
                )
                code, _err = self.run_text(text)
                self.assertEqual(code, 0)

    def test_defeating_ran_and_reproduced_without_override(self):
        for level in ("ran", "reproduced"):
            with self.subTest(level=level):
                text = brief_with(
                    "## Premises",
                    "",
                    premise(1, "The ledger file appears after the job command.", level, RUN_RECORD, "yes"),
                )
                code, _err = self.run_text(text)
                self.assertEqual(code, 0)

    def test_non_defeating_said_without_override(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
        )
        code, _err = self.run_text(text)
        self.assertEqual(code, 0)

    def test_level_missing_and_invalid(self):
        missing = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Source:** none",
            "   **Defeats ticket:** no",
        )
        code, err = self.run_text(missing)
        self.assertEqual(code, 1)
        self.assertIn("level-missing", codes(err))

        invalid = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "Ran", "none", "no"),
        )
        code, err = self.run_text(invalid)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["level-invalid"])

    def test_flag_missing_and_invalid(self):
        missing = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Level:** said",
            "   **Source:** none",
        )
        code, err = self.run_text(missing)
        self.assertEqual(code, 1)
        self.assertIn("flag-missing", codes(err))

        invalid = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "true"),
        )
        code, err = self.run_text(invalid)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["flag-invalid"])

    def test_override_whitespace_only(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "pointed", "vendor/sdk.py:12", "yes", override="   "),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["override-empty"])

    def test_item_id_gap(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "First claim.", "said", "none", "no"),
            "",
            "3. **P3.** Third claim.",
            "   **Level:** said",
            "   **Source:** none",
            "   **Defeats ticket:** no",
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("item-id", codes(err))

    def test_claim_missing(self):
        text = brief_with(
            "## Premises",
            "",
            "1. **P1.**",
            "   **Level:** said",
            "   **Source:** none",
            "   **Defeats ticket:** no",
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("claim-missing", codes(err))

    def test_fenced_item_is_section_empty(self):
        text = brief_with(
            "## Premises",
            "",
            "```",
            premise(1, "Hidden claim.", "said", "none", "no"),
            "```",
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["section-empty"])

    def test_unclosed_fence_hides_later_item(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
            "",
            "```",
            premise(2, "The job writes the ledger before it returns.", "said", "none", "yes"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["fence-open"])

    def test_defeating_item_after_next_heading_is_not_a_premise(self):
        text = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
            "",
            "## Done when",
            "",
            premise(2, "The job writes the ledger before it returns.", "said", "none", "yes"),
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
            premise(1, "The job writes the ledger before it returns.", "said", "none", "yes"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["section-duplicate"])

    def test_field_unknown_and_duplicate(self):
        unknown = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Level:** said",
            "   **Source:** none",
            "   **Defeats:** yes",
        )
        code, err = self.run_text(unknown)
        self.assertEqual(code, 1)
        self.assertIn("field-unknown", codes(err))

        duplicate = brief_with(
            "## Premises",
            "",
            "1. **P1.** The vendor SDK injects the clock.",
            "   **Level:** said",
            "   **Level:** pointed",
            "   **Source:** none",
            "   **Defeats ticket:** no",
        )
        code, err = self.run_text(duplicate)
        self.assertEqual(code, 1)
        self.assertIn("field-duplicate", codes(err))

    def test_source_shapes(self):
        pointed = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "pointed", "no line here", "no"),
        )
        code, err = self.run_text(pointed)
        self.assertEqual(code, 1)
        self.assertIn("source-invalid", codes(err))

        ran = brief_with(
            "## Premises",
            "",
            premise(1, "The ledger file appears after the job command.", "ran", "vendor/sdk.py:12", "yes"),
        )
        code, err = self.run_text(ran)
        self.assertEqual(code, 1)
        self.assertIn("source-invalid", codes(err))

        said = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
        )
        code, _err = self.run_text(said)
        self.assertEqual(code, 0)

    def test_rests_on_checks(self):
        mismatch = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock.",
            "   **Rests on:** P1 (pointed)",
            "   **Below ran:** yes",
            "",
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
        )
        code, err = self.run_text(mismatch)
        self.assertEqual(code, 1)
        self.assertIn("rests-on-level", codes(err))

        unknown = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock.",
            "   **Rests on:** P9 (said)",
            "   **Below ran:** yes",
            "",
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
        )
        code, err = self.run_text(unknown)
        self.assertEqual(code, 1)
        self.assertIn("rests-on-unknown", codes(err))

        missing = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock. The ticket says so.",
            "",
            "## Premises",
            "",
            "_(no premises)_",
        )
        code, err = self.run_text(missing)
        self.assertEqual(code, 1)
        self.assertIn("rests-on-missing", codes(err))

        duplicate = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock.",
            "   **Rests on:** none",
            "   **Rests on:** P1 (said)",
            "   **Below ran:** yes",
            "",
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
        )
        code, err = self.run_text(duplicate)
        self.assertEqual(code, 1)
        self.assertIn("rests-on-duplicate", codes(err))
        self.assertNotIn("below-ran-line", codes(err))

        no_line = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock.",
            "   **Rests on:** P1 (said)",
            "",
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
        )
        code, err = self.run_text(no_line)
        self.assertEqual(code, 1)
        self.assertIn("below-ran-line", codes(err))

        line_on_ran = brief_with(
            "## Decisions carried forward",
            "",
            "1. Keep the clock.",
            "   **Rests on:** P1 (ran)",
            "   **Below ran:** yes",
            "",
            "## Premises",
            "",
            premise(1, "The ledger file appears after the job command.", "ran", RUN_RECORD, "yes"),
        )
        code, err = self.run_text(line_on_ran)
        self.assertEqual(code, 1)
        self.assertIn("below-ran-line", codes(err))

    def test_below_ran_line_is_per_decision(self):
        ok = brief_with(
            "## Decisions carried forward",
            "",
            "1. Walked decision.",
            "   **Rests on:** P1 (walked)",
            "   **Below ran:** yes",
            "",
            "2. Ran decision.",
            "   **Rests on:** P2 (ran)",
            "",
            "## Premises",
            "",
            premise(1, "The job writes the ledger before it returns.", "walked", "skills/app/SKILL.md:10", "no"),
            "",
            premise(2, "The ledger file appears after the job command.", "ran", RUN_RECORD, "yes"),
        )
        code, _err = self.run_text(ok)
        self.assertEqual(code, 0)

        swapped = brief_with(
            "## Decisions carried forward",
            "",
            "1. Walked decision.",
            "   **Rests on:** P1 (walked)",
            "",
            "2. Ran decision.",
            "   **Rests on:** P2 (ran)",
            "   **Below ran:** yes",
            "",
            "## Premises",
            "",
            premise(1, "The job writes the ledger before it returns.", "walked", "skills/app/SKILL.md:10", "no"),
            "",
            premise(2, "The ledger file appears after the job command.", "ran", RUN_RECORD, "yes"),
        )
        code, err = self.run_text(swapped)
        self.assertEqual(code, 1)
        self.assertIn("below-ran-line", codes(err))

    def test_item_unparsed_not_a_well_formed_next_item(self):
        bad = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
            "2. **P2** claim",
        )
        code, err = self.run_text(bad)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

        also = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
            "2. P2. claim",
        )
        code, err = self.run_text(also)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

        good = brief_with(
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "no"),
            "",
            premise(2, "The job writes the ledger before it returns.", "said", "none", "no"),
        )
        code, _err = self.run_text(good)
        self.assertEqual(code, 0)

    def test_walked_step_on_its_own_line_is_item_unparsed(self):
        text = "\n".join([
            "## Premises",
            "",
            "1. **P1.** The job writes the ledger before it returns.",
            "   **Level:** walked",
            "   **Source:** 1. skills/app/SKILL.md:10 opens the job.",
            "   2. skills/app/SKILL.md:40 opens the write.",
            "   **Defeats ticket:** yes",
            "   **Override:** operator accepts the trace for this brief",
            "",
        ])
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertIn("item-unparsed", codes(err))

    def test_deeply_indented_item_after_a_field_is_item_unparsed(self):
        text = "\n".join([
            "## Premises",
            "",
            premise(1, "The vendor SDK injects the clock.", "said", "none", "yes", "fine"),
            "    2. **P2.** Hidden defeating claim.",
            "    **Level:** said",
            "    **Source:** none",
            "    **Defeats ticket:** yes",
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

    def test_fenced_and_quoted_rests_on_do_not_count(self):
        text = "\n".join([
            "## Decisions carried forward",
            "",
            "1. **Keep.** The rationale.",
            "```",
            "   **Rests on:** none",
            "```",
            "   **Rests on:** none",
            "> **Rests on:** P9 (said)",
            "",
            "## Premises",
            "",
            "_(no premises)_",
            "",
        ])
        code, err = self.run_text(text)
        self.assertEqual(code, 0, err)

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
            premise(1, "The job writes the ledger before it returns.", "said", "none", "yes"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["below-ran"])

    def test_indented_and_fenced_decision_lines_are_not_items(self):
        text = "\n".join([
            "## Decisions carried forward",
            "",
            "1. **Keep.** The rationale.",
            "   1. a substep",
            "   **Rests on:** none",
            "```",
            "2. **Other.**",
            "```",
            "",
            "## Premises",
            "",
            "_(no premises)_",
            "",
        ])
        code, err = self.run_text(text)
        self.assertEqual(code, 0, err)
        self.assertNotIn("decision-id", codes(err))
        self.assertNotIn("rests-on-missing", codes(err))

    def test_marker_and_items_only(self):
        text = brief_with(
            "## Premises",
            "",
            "_(no premises)_",
            "",
            premise(1, "The job writes the ledger before it returns.", "said", "none", "yes"),
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
            premise(1, "The ledger — the real one — is written before return.", "said", "none", "yes"),
        )
        code, err = self.run_text(text)
        self.assertEqual(code, 1)
        self.assertEqual(codes(err), ["below-ran"])
        self.assertNotIn("error", codes(err))

    def test_subprocess_entry_point(self):
        defeating = brief_with(
            "## Premises",
            "",
            premise(1, "The job writes the ledger before it returns.", "said", "none", "yes"),
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
            self.assertIn(b"premise: below-ran", proc.stderr)
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
            "**Rests on:**",
            "premises need an operator — stopping",
            "premise gate: check_premises.py did not run",
            "Write blocked",
            "When the first premise is added, delete _(no premises)_ in that same edit.",
            "A premise at ran or reproduced with no matching hand-off line is demoted.",
            "Write the temp from the candidate after flag replies and override lines are on the items.",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
