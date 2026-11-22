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
                       "Generated with [Claude Code]", "place_artifact",
                       # Regression for VHS-54: the HEAD check is not a gate-only, clean-only rule.
                       "Its clean result means it did run only when"):
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
                       "if unsure, ask, or with `--unattended` use `chore`",
                       "Flagged, a step the spec's own words give to the operator",
                       "is left undone and is no stop: Phase 5 lists every such step as `- [ ] Operator: <step>`",
                       "A flagged `--build-only` also prints those lines, and its `--from-review` command with `--unattended`",
                       "never give the operator a step on your own judgment",
                       "each `- [ ] Operator: <step>` line, and always `- [ ] Post-merge verification`",
                       "else, flagged, append there each `- [ ] Operator:` line it lacks",
                       "warn, naming both, and continue; flagged, halt",
                       "skips go to Phase 4 only with no unresolved Blocks finding"):
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


    def test_executor_phrases(self):
        # Regression for VHS-54: the executors read, the hand-off, the gate and the always-review rule.
        text = read(SKILL)
        for phrase in ("Its `executors` name `build` and `gate`: for each, the prefix entry's value, else the top-level one",
                       "Anything but a non-empty string, and a name for this session, is none",
                       "can replace either for this run",
                       "No builder is used. After Phase 3 is green",
                       "with the host's delegation tool, or the executor's command-line tool when the host has none",
                       "write only in the worktree, by absolute path; never change directory; delete no temporary files; leave operator steps undone; commit by naming each path; no push, PR, tracker write or `/ship-spec`; stop after the final commit",
                       "the first two sentences above, the guardrails step 3 read, this chain's `FILED` report when `/spec-tickets` filed",
                       "report what was built, what was not, and what the next step needs",
                       "or reports spec work unbuilt, operator steps aside, halts the run, naming it",
                       # Regression for VHS-54: missing builder work is never a test fix; the red gate halts on it.
                       "is red: halt on missing builder work; otherwise make one smallest fix and retry",
                       "A run that a **Chain** started halts unless the verdict is `green` and a builder resolved.",
                       "Never build in the session or pick another executor.",
                       "- `small`, unless builder-built: print",
                       "A builder-built diff (this run's builder, or `--from-review` with a builder set) follows `irreversible` on every tier. So does `big` with a gate executor. Missing builder work found by tests or review is unresolved Blocks.",
                       "With a gate executor, it stands in for the command throughout this phase: hand it that prompt, without the command, as Phase 2 hands off",
                       "still runs once as above, without `Test command:`, as a bloat check",
                       "its findings join the gate's but never count as the review running",
                       "its absence or failure is neither a skip nor a stop",
                       # Regression for VHS-54: a review of a builder's commit, or by a gate, counts only for the HEAD under review.
                       "For builder-built or gate-executor reviews, the prompt asks the report to confirm it inspected the committed range through the expected `HEAD`; otherwise the review did not run.",
                       # Regression for VHS-54: with no executors the two diagnostics read as they did.
                       "Review follows the spec tier. On tier mismatch, print both tiers and that rule, explaining implicit `big` when applicable. Preserve the marker.",
                       "Keep the worktree. Print the case and any configured gate.",
                       "Before any review starts and after the last returns, record outside both checkouts `git rev-parse HEAD`, `git status --porcelain=v1 -uall -z`",
                       "Include `origin/<default-branch>...HEAD`.",
                       "Executors: build <name | session | prebuilt> · gate <name | session | skipped>",
                       "`prebuilt` for a resumed build of unknown builder, `skipped` when no review ran",
                       "that `Executors:` line",
                       "Next: /ship-spec <spec-path> --from-review <worktree-path>",
                       "End on `Next: /review-pr`, in the worktree."):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
