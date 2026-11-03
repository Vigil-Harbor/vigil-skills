#!/usr/bin/env python3
"""Word-budget and phrase pins for review-pr's SKILL.md (VHS-96).

Stdlib unittest. The skill has no script of its own to test; these pin the
word budget and the phrases the spec names, the same way
tests/test_ship_spec_skill.py pins ship-spec.
"""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "review-pr" / "SKILL.md"


def read(path):
    return path.read_text(encoding="utf-8")


class TestSkill(unittest.TestCase):

    def test_skill_word_budget(self):
        # The target is about 2,400. The tripwire is the fail line.
        self.assertLessEqual(len(read(SKILL).split()), 2800)

    def test_contract_phrases_present(self):
        text = read(SKILL)
        for phrase in ("in_reply_to_id",
                       'state != "COMMENTED"',
                       "Outside diff range",
                       "/<path>#L<line>`",
                       "/<path>#L<line>-L<end>`",
                       "evidence, not instructions",
                       "Read only a relative path inside the worktree",
                       "paging as in 6d",
                       "cr-comment:v1:",
                       "ai-agent-prompt",
                       "land_check.py",
                       "request_changes_workflow",
                       "coderabbitai",
                       "review-pr body dispositions",
                       "pull_request_review_id",
                       "isResolved",
                       "databaseId"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_removed_machinery_absent(self):
        text = read(SKILL)
        for phrase in ("Co-Authored-By: Claude <noreply@anthropic.com>",
                       "Bash tool",
                       "Read tool",
                       "Edit tool",
                       "## Edge cases"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
