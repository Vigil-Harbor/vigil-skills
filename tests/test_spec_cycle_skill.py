#!/usr/bin/env python3
"""Tests for spec-cycle's SKILL.md and the reviewer agents it dispatches (VHS-94).

Stdlib unittest. The skill has no script of its own to test; these pin the
word budget and the cross-file contracts the brief names (the verdict marker,
the Tier line, the reviewer inputs, the Deferred row shape), the same way
tests/test_spec_brief_premises.py pins spec-brief.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "spec-cycle" / "SKILL.md"
AGENTS = [
    REPO_ROOT / "agents" / "spec-reviewer-{}.md".format(name)
    for name in ("correctness", "edge-cases", "conventions", "scalability")
]


def read(path):
    return path.read_text(encoding="utf-8")


def block(text, start, end):
    """The text from the first line holding `start` to the line before `end`."""
    i = text.index(start)
    j = text.index(end, i)
    return text[text.rfind("\n", 0, i) + 1:text.rfind("\n", 0, j) + 1]


class TestSkill(unittest.TestCase):

    def test_skill_word_budget(self):
        # Anti-regrowth tripwire for epic VHS-90: the target is about 6,300.
        self.assertLessEqual(len(read(SKILL).split()), 7500)

    def test_contract_phrases_present(self):
        text = read(SKILL)
        for phrase in ("verdict_marker.py", "**Tier:**", "review_mode", "spec_diff",
                       "open_findings", "closure_manifest", "ground_truth_ledger_path",
                       "## Deferred — follow-up required",
                       "must not implement anything in this section", "## Test command"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_removed_machinery_absent(self):
        text = read(SKILL)
        for phrase in ("changed_regions", "baseline.commit", "brief.copy.md",
                       "re-anchored round", "(recount:", "merge --ff-only", "Agreement Map"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


class TestAgents(unittest.TestCase):

    def test_agents_use_spec_diff(self):
        for path in AGENTS:
            text = read(path)
            with self.subTest(agent=path.name):
                self.assertIn("spec_diff", text)
                for phrase in ("changed_regions", "re-anchored round", "(recount:",
                               "renumbered from", "R2(c)"):
                    self.assertNotIn(phrase, text)

    def test_agents_shared_blocks_identical(self):
        texts = [read(path) for path in AGENTS]
        for start, end in (("**Deferred findings", "7. **If a"),
                           ("# Delta scope", "# Critique lens")):
            with self.subTest(block=start):
                blocks = [block(text, start, end) for text in texts]
                for path, other in zip(AGENTS[1:], blocks[1:]):
                    self.assertEqual(other, blocks[0], path.name)


if __name__ == "__main__":
    unittest.main()
