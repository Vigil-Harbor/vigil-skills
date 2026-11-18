#!/usr/bin/env python3
"""Tests for design-loop's score_gate.py.

Stdlib unittest. The script is loaded by file path, the same way
tests/test_verdict_marker.py loads verdict_marker.py. Reviews are written to
a temp dir.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "design-loop"
SCRIPT = SKILL_DIR / "scripts" / "score_gate.py"


def load_script(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = load_script(SCRIPT, "design_loop_score_gate")


def category(name: str, score, concerns=None) -> dict:
    return {"category": name, "score": score, "rationale": "r", "concerns": concerns or []}


def review(*surfaces: tuple[str, list[dict]]) -> dict:
    return {
        "surfaces": [{"surface": name, "categories": cats} for name, cats in surfaces],
        "overall_notes": "",
    }


THREE = ["design", "usability", "conventions"]


def scores(d: int, u: int, c: int) -> list[dict]:
    return [category("design", d), category("usability", u), category("conventions", c)]


class GateTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def run_gate(self, payload, *args: str, raw: str | None = None, bom: bool = False):
        path = self.dir / "review.json"
        text = raw if raw is not None else json.dumps(payload)
        path.write_text(text, encoding="utf-8-sig" if bom else "utf-8")
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gate.main([str(path), *args])
        return code, out.getvalue(), err.getvalue()


class TestVerdict(GateTestCase):
    def test_passes_when_every_category_reaches_the_target(self):
        code, out, _ = self.run_gate(review(("list", scores(9, 8, 8)), ("drawer", scores(8, 8, 10))))
        self.assertEqual(code, gate.EXIT_PASS)
        self.assertIn("GATE: PASS (target 8)", out)
        self.assertIn("LOWEST: 8 (list / usability)", out)

    def test_fails_when_one_category_on_one_surface_is_short(self):
        code, out, _ = self.run_gate(review(("list", scores(9, 8, 9)), ("drawer", scores(9, 7, 9))))
        self.assertEqual(code, gate.EXIT_FAIL)
        self.assertIn("GATE: FAIL (target 8)", out)
        self.assertIn("LOWEST: 7 (drawer / usability)", out)
        # the short score is marked in the table
        self.assertIn("usability 7 <", out)

    def test_target_is_adjustable(self):
        payload = review(("list", scores(7, 7, 7)))
        self.assertEqual(self.run_gate(payload, "--target", "7")[0], gate.EXIT_PASS)
        self.assertEqual(self.run_gate(payload, "--target", "8")[0], gate.EXIT_FAIL)

    def test_custom_categories_are_gated_too(self):
        payload = review(("list", [category("clarity", 9), category("speed", 6)]))
        code, out, _ = self.run_gate(payload, "--categories", "clarity,speed")
        self.assertEqual(code, gate.EXIT_FAIL)
        self.assertIn("LOWEST: 6 (list / speed)", out)

    def test_a_byte_order_mark_is_accepted(self):
        code, _, _ = self.run_gate(review(("list", scores(8, 8, 8))), bom=True)
        self.assertEqual(code, gate.EXIT_PASS)


class TestVoid(GateTestCase):
    def assert_void(self, payload=None, *args: str, raw: str | None = None, says: str = ""):
        code, out, err = self.run_gate(payload, *args, raw=raw)
        self.assertEqual(code, gate.EXIT_VOID)
        self.assertEqual(out, "")
        self.assertIn("VOID:", err)
        if says:
            self.assertIn(says, err)

    def test_an_empty_file_is_void_not_a_pass(self):
        # A reviewer that was stopped mid-run leaves an empty output file.
        self.assert_void(raw="", says="did not finish")

    def test_not_json_is_void(self):
        self.assert_void(raw="{not json", says="not JSON")

    def test_no_surfaces_is_void(self):
        self.assert_void({"surfaces": [], "overall_notes": ""}, says="non-empty list")

    def test_a_surface_with_no_categories_is_void(self):
        self.assert_void(review(("list", [])), says="non-empty list")

    def test_a_missing_required_category_is_void(self):
        # Leaving a category out must not pass the gate.
        payload = review(("list", [category("design", 9), category("conventions", 9)]))
        self.assert_void(payload, "--categories", ",".join(THREE), says="usability")

    def test_required_categories_match_without_regard_to_case(self):
        payload = review(("list", [category("Design", 9), category("Usability", 9), category("Conventions", 9)]))
        code, _, _ = self.run_gate(payload, "--categories", ",".join(THREE))
        self.assertEqual(code, gate.EXIT_PASS)

    def test_scores_outside_one_to_ten_are_void(self):
        for bad in (0, 11, -3):
            with self.subTest(score=bad):
                self.assert_void(review(("list", scores(9, bad, 9))), says="1 to 10")

    def test_non_integer_scores_are_void(self):
        # True is an int in Python; it must not read as a score of 1.
        for bad in (True, 8.5, "8", None):
            with self.subTest(score=bad):
                self.assert_void(review(("list", scores(9, bad, 9))), says="1 to 10")

    def test_a_duplicated_surface_or_category_is_void(self):
        self.assert_void(review(("list", scores(9, 9, 9)), ("list", scores(9, 9, 9))), says="appears twice")
        twice = review(("list", [category("design", 9), category("design", 3)]))
        self.assert_void(twice, says="appears twice")

    def test_a_bad_target_is_void(self):
        self.assert_void(review(("list", scores(9, 9, 9))), "--target", "11", says="--target")

    def test_a_missing_file_is_void(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gate.main([str(self.dir / "nope.json")])
        self.assertEqual(code, gate.EXIT_VOID)
        self.assertIn("cannot read", err.getvalue())


class TestConcerns(GateTestCase):
    def test_concerns_print_most_severe_first(self):
        concerns = [
            {"severity": "low", "where": "footer", "problem": "tight", "suggestion": "loosen"},
            {"severity": "high", "where": "save", "problem": "claims success", "suggestion": "say unknown"},
        ]
        payload = review(("drawer", [category("design", 9), category("usability", 6, concerns), category("conventions", 9)]))
        code, out, _ = self.run_gate(payload, "--concerns")
        self.assertEqual(code, gate.EXIT_FAIL)
        self.assertIn("[drawer / usability] 6", out)
        self.assertLess(out.index("(high) save"), out.index("(low) footer"))

    def test_concerns_are_left_out_unless_asked_for(self):
        concerns = [{"severity": "high", "where": "save", "problem": "p", "suggestion": "s"}]
        payload = review(("drawer", [category("design", 9, concerns)]))
        _, out, _ = self.run_gate(payload)
        self.assertNotIn("(high)", out)


class TestBundle(unittest.TestCase):
    """The schema the skill hands the reviewer and the gate must agree."""

    def test_schema_is_json_and_names_the_fields_the_gate_reads(self):
        schema = json.loads((SKILL_DIR / "reference" / "score-schema.json").read_text(encoding="utf-8"))
        surface = schema["properties"]["surfaces"]["items"]
        self.assertEqual(surface["required"], ["surface", "categories"])
        cat = surface["properties"]["categories"]["items"]
        self.assertEqual(cat["required"], ["category", "score", "rationale", "concerns"])
        self.assertEqual((cat["properties"]["score"]["minimum"], cat["properties"]["score"]["maximum"]), (1, 10))

    def test_a_review_shaped_like_the_schema_passes_through_the_gate(self):
        payload = review(("list", scores(8, 8, 8)))
        self.assertEqual(len(gate.read_review(payload, THREE)), 1)


if __name__ == "__main__":
    unittest.main()
