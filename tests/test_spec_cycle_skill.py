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
        # Regression for VHS-115: no growth past the 2026-11-22 count. The VHS-90 target is about 6,300.
        self.assertLessEqual(len(read(SKILL).split()), 7066)

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

    def test_unattended_phrases(self):
        # Regression for VHS-115: the flag, the recorded stop and the Splits line.
        text = read(SKILL)
        for phrase in ('[--attest "<reason>" | [--full] [--unattended]]',
                       "`--unattended` means nobody will answer: the run is a host that cannot wait",
                       "every prompt is a stop",
                       "the 2f halt prints its block and takes no option",
                       "except a usage halt and the unchanged-green stop",
                       "UNATTENDED STOP: <TICKET-ID> · spec-cycle · <reason>",
                       "when exactly one connected issue tracker resolves the id",
                       "stop comment NOT posted: <error>",
                       "then print the `UNATTENDED STOP` line last",
                       "each is exclusive with `--attest`",
                       "or output that is not one JSON object with a valid `state` is `unreadable`",
                       "a `red`, `pending` or `unreadable` state is a recorded stop here:",
                       "an unattended run does not resume a halted or unfinished review",
                       "Splits: <yes — <the pieces in a few words> | no>",
                       "The `Splits:` line then names the pieces in a few words",
                       "with `Splits: no`"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_unflagged_prompts_kept(self):
        # Regression for VHS-115: without the flag every prompt reads as it did.
        text = read(SKILL)
        for phrase in ("with no match, ask for it",
                       "A host that cannot wait keeps the prompt's own stop.",
                       "marker left pending",
                       "4. Grill the remaining findings.",
                       "Wait for the operator.",
                       "attestation requires an operator — nothing written",
                       "`full` when `--full` is given; when the marker is missing, unreadable, `pending`"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_stale_marker_actions_absent(self):
        # Regression for VHS-115: the marker list names states, not confirms.
        text = read(SKILL)
        for phrase in ("— Confirm", "Every confirm stops", "canonical copy", "`Why:` line"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


    def test_chain_phrases(self):
        # Regression for VHS-54: the Next line, the chain start and its stops. The chain starts
        # only on the spec ship-spec will read, and never forwards the operator's line.
        text = read(SKILL)
        for phrase in ("Splits: <yes — <the pieces in a few words> | no>\nNext: <recommended command>",
                       "**Chain.** When the green marker was written, `/ship-spec` Phase 0 step 7 resolves a builder, and this spec is the file `/ship-spec` will read (the same absolute path under its primary checkout)",
                       "start the `Next:` command with `--unattended` alone, in this session",
                       "Never forward the operator's line",
                       "this session acts on it and carries any executor it names, which replaces that role for this run",
                       "Chain: started <command> — build <name>, gate <name | session>",
                       "Start nothing when it says to hold or is unclear, or the host cannot start it",
                       "With no builder, the operator starts `Next:` in a fresh session."):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        for phrase in ("neither command runs from here", "then the operator's line",
                       "When ready, run:", "## Failure modes"):
            with self.subTest(absent=phrase):
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
