#!/usr/bin/env python3
"""Word ceilings and phrase pins for spec-tickets and the workflow reference (VHS-99).

Stdlib unittest. Reads files under the repo root the way
tests/test_review_pr_skill.py does.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "spec-tickets" / "SKILL.md"
REFERENCE = REPO_ROOT / "docs" / "spec-workflow-reference.md"
SPEC_CYCLE = REPO_ROOT / "skills" / "spec-cycle" / "SKILL.md"
README = REPO_ROOT / "README.md"

REQUIRES = (
    "requires:\n"
    "  shell: optional\n"
    "  filesystem: [read, write]\n"
    "  services: [issue-tracker?]"
)

PRESENT = (
    "verdict_marker.py",
    "--no-fingerprint",
    "SPEC VERDICT: red",
    "one piece — run /ship-spec",
    "NOT FILED:",
    "FILED: <PARENT-ID>",
    "STOPPED: <PARENT-ID>",
    "Storage: halt via",
    "<PARENT-ID>.ticket-",
    "Reading:",
    # Regression for VHS-99: the duplicate guard's stop line stays phrase-pinned.
    "already has children",
)

ABSENT = (
    "## Failure modes",
    "never does",
    "Approve and file",
    "does not file headless",
    "override",
    "## Phase 4",
)

POINTERS = (
    "skills/spec-brief/SKILL.md",
    "skills/spec-cycle/SKILL.md",
    "skills/spec-tickets/SKILL.md",
    "skills/ship-spec/SKILL.md",
    "skills/spec-land/SKILL.md",
    "skills/spec-close/SKILL.md",
)


def read(path):
    return path.read_text(encoding="utf-8")


class TestSpecTicketsSkill(unittest.TestCase):

    def test_skill_word_budget(self):
        # Regression for VHS-99: spec-tickets stays under the 1,900-word ceiling.
        self.assertLessEqual(len(read(SKILL).split()), 1900)

    def test_contract_phrases_present(self):
        text = read(SKILL)
        for phrase in PRESENT:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_removed_machinery_absent(self):
        text = read(SKILL)
        for phrase in ABSENT:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)

    def test_requires_block(self):
        text = read(SKILL)
        start = text.index("requires:\n")
        end = text.index("\n---", start)
        self.assertEqual(text[start:end], REQUIRES)


class TestReferenceDoc(unittest.TestCase):

    def test_reference_word_budget(self):
        # Regression for VHS-99: the workflow reference stays under 1,500 words.
        self.assertLessEqual(len(read(REFERENCE).split()), 1500)

    def test_skill_pointers(self):
        text = read(REFERENCE)
        for phrase in POINTERS:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


class TestNextAndReadme(unittest.TestCase):

    def test_spec_cycle_next_commands(self):
        text = read(SPEC_CYCLE)
        self.assertIn("/spec-tickets docs/specs/TODO/<TICKET-ID>.spec.md", text)
        self.assertIn("/ship-spec docs/specs/TODO/<TICKET-ID>.spec.md", text)

    def test_readme_lists_spec_land(self):
        self.assertIn("`/spec-land", read(README))


if __name__ == "__main__":
    unittest.main()
