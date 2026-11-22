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
        # Regression for VHS-115: no growth past the 2026-11-22 count. The VHS-90 target is about 2,900.
        self.assertLessEqual(len(read(SKILL).split()), 3666)

    def test_contract_phrases_present(self):
        text = read(SKILL)
        for phrase in ("--build-only", "--from-review",
                       "if the review did not run, stop instead of committing",
                       "verdict_marker.py", "land_check.py",
                       "## Done when", "## Test plan",
                       "Test command:", "Validation:", "git hash-object"):
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

    def test_unattended_phrases(self):
        # Regression for VHS-115: the flag, the fixed answer, the recorded stop, the operator box.
        text = read(SKILL)
        for phrase in ("--from-review <worktree-path>] [--unattended]",
                       "`--unattended` goes with any mode and makes the run that host",
                       "Any halt or stop short of the mode's end, except a usage halt, is then a recorded stop",
                       "UNATTENDED STOP: <TICKET-ID> · ship-spec · <reason>",
                       "never under `--build-only`",
                       "if unsure, ask; with `--unattended`, use `chore`",
                       "Flagged, a step the spec's own words give to the operator",
                       "is left undone and is no stop: Phase 5 lists every such step as `- [ ] Operator: <step>`",
                       "A flagged `--build-only` also prints those lines, and its `--from-review` command with `--unattended`",
                       "never give the operator a step on your own judgment",
                       "each `- [ ] Operator: <step>` line, and always `- [ ] Post-merge verification`",
                       "else add at that section's end each `- [ ] Operator:` line it lacks"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_unflagged_prompts_kept(self):
        # Regression for VHS-115: without the flag every prompt and halt reads as it did.
        text = read(SKILL)
        for phrase in ("A host that cannot wait prints the prompt and stops.",
                       "it does not take a numbered option whose text does one of those",
                       "A host that cannot wait prints this halt, keeps the worktree and the branch, and does not take option 3.",
                       "A host that cannot wait takes 3.",
                       "Halt if the directory exists, or the branch exists locally",
                       "3. Abandon — stop here; the worktree is kept"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
