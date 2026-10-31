#!/usr/bin/env python3
"""Word-budget and phrase pins for ship-spec's SKILL.md (VHS-95).

Stdlib unittest. The skill has no script of its own to test; these pin the
word budget and the phrases the spec names, the same way
tests/test_spec_cycle_skill.py pins spec-cycle.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "ship-spec" / "SKILL.md"


def read(path):
    return path.read_text(encoding="utf-8")


class TestSkill(unittest.TestCase):

    def test_skill_word_budget(self):
        # Anti-regrowth tripwire for epic VHS-90: the target is about 2,900.
        self.assertLessEqual(len(read(SKILL).split()), 3500)

    def test_contract_phrases_present(self):
        text = read(SKILL)
        for phrase in ("--build-only", "--from-review",
                       "if the review did not run, stop instead of committing",
                       "verdict_marker.py", "land_check.py",
                       "## Done when", "## Test plan"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_removed_machinery_absent(self):
        text = read(SKILL)
        for phrase in ("## Failure modes",
                       "Co-Authored-By: Claude <noreply@anthropic.com>",
                       "plane-proxy", "Halted passes",
                       "Generated with [Claude Code]", "place_artifact"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
