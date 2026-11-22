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
AGENTS_MD = REPO_ROOT / "AGENTS.md"
SHIP_SPEC = REPO_ROOT / "skills" / "ship-spec" / "SKILL.md"
CUSTOMIZING = REPO_ROOT / "docs" / "customizing.md"

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
    "one piece — nothing filed",
    "NOT FILED:",
    "FILED: <PARENT-ID>",
    "STOPPED: <PARENT-ID>",
    "Storage: halt via",
    "<PARENT-ID>.ticket-",
    "Reading:",
    # Regression for VHS-99: the duplicate guard's stop line stays phrase-pinned.
    "already has children",
    # Regression for VHS-115: the flag and the flagged outcome of the one prompt.
    "then an optional `--unattended`",
    "The name minus `.spec.md` is `<PARENT-ID>`",
    "Usage: /spec-tickets docs/specs/TODO/<TICKET-ID>.spec.md [--unattended]",
    "`--unattended` means nobody will answer: the integration pick stops before filing",
    "every heading-check, red-verdict, `Storage: halt`, `NOT FILED` and `STOPPED` exit, is then a recorded stop",
    "UNATTENDED STOP: <PARENT-ID> · spec-tickets · <reason>",
    # Regression for VHS-115: a run that files is unchanged.
    "Invoking it is the authorization to file.",
    "one blocked-by relation per edge",
    "Next: /ship-spec docs/specs/TODO/<PARENT-ID>.spec.md",
    # Regression for VHS-54: free words, the one-piece Next line and the chain.
    "later non-flag words are the operator's line",
    "and the Report's `Next:` line, file nothing, and end as its **Chain** says",
    "when the verdict read `green` and `/ship-spec` Phase 0 step 7 resolves a builder, start the `Next:` command by `/spec-cycle`'s **Chain** rule",
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
        # Regression for VHS-115: no growth past the 2026-11-22 count.
        self.assertLessEqual(len(read(SKILL).split()), 1714)

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


class TestUnattended(unittest.TestCase):

    def test_stop_line_shape_shared(self):
        # Regression for VHS-115: one stop line and one comment rule in all three skills.
        for path, name in ((SPEC_CYCLE, "spec-cycle"), (SKILL, "spec-tickets"),
                           (SHIP_SPEC, "ship-spec")):
            text = read(path)
            for phrase in ("UNATTENDED STOP: <",
                           " · {} · <reason>".format(name),
                           "when exactly one connected issue tracker resolves the id",
                           "a failed comment prints `stop comment NOT posted: <error>`",
                           "then print the `UNATTENDED STOP` line last"):
                with self.subTest(skill=name, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_docs_carry_flag(self):
        # Regression for VHS-115: every usage line names the flag.
        usage = ('/spec-cycle <brief-path> [--attest "<reason>" | [--full] [--unattended]]',
                 "/ship-spec <spec-path> [--build-only | --from-review <worktree-path>] [--unattended]")
        for path in (AGENTS_MD, README):
            text = read(path)
            for phrase in usage + ("/spec-tickets <spec-path> [--unattended]",):
                with self.subTest(doc=path.name, phrase=phrase):
                    self.assertIn(phrase, text)
        text = read(REFERENCE)
        for phrase in usage + ("/spec-tickets docs/specs/TODO/<TICKET-ID>.spec.md [--unattended]",
                               "UNATTENDED STOP: <ticket> · <skill> · <reason>"):
            with self.subTest(doc=REFERENCE.name, phrase=phrase):
                self.assertIn(phrase, text)


class TestChain(unittest.TestCase):

    def test_next_line_rule_shared(self):
        # Regression for VHS-54: every stop in all three skills ends on a Next line,
        # and the stop line VHS-115 pins stays last.
        for path in (SPEC_CYCLE, SKILL, SHIP_SPEC):
            text = read(path)
            for phrase in ("Every stop ends on one `Next:` line, a command or a question, "
                           "printed before a recorded stop's line.",
                           "then print the `UNATTENDED STOP` line last"):
                with self.subTest(skill=path.parent.name, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_docs_carry_executors(self):
        # Regression for VHS-54: the setting, its removal and the boundary are documented.
        for path, phrases in (
                (CUSTOMIZING, ("## Executors", "two roles, `build` and `gate`",
                               "or remove the key", "restores the earlier behaviour",
                               "nothing falls back to the session")),
                (AGENTS_MD, ("**Executors.**",
                             "Removing the key restores the stage-by-stage stops")),
                (README, ("**Executors.**",
                          "remove the key to get the stage-by-stage stops back")),
                (REFERENCE, ("`executors` in `states.json` names a builder and a gate",
                             "Context boundary between review and implementation",
                             "never implements it",
                             "Every stop ends on one `Next:` line"))):
            text = read(path)
            for phrase in phrases:
                with self.subTest(doc=path.name, phrase=phrase):
                    self.assertIn(phrase, text)
        text = read(REFERENCE)
        for phrase in ("Neither command runs from spec-cycle", "Session boundary between"):
            with self.subTest(doc=REFERENCE.name, absent=phrase):
                self.assertNotIn(phrase, text)

    def test_skills_name_no_executor(self):
        # Regression for VHS-54: executor names live in states.json, never in a skill.
        for path in (SPEC_CYCLE, SKILL, SHIP_SPEC):
            text = read(path).lower()
            for name in ("grok", "codex", "gpt-"):
                with self.subTest(skill=path.parent.name, name=name):
                    self.assertNotIn(name, text)


if __name__ == "__main__":
    unittest.main()
