# Conventions Review — round 3

Grounding performed: spec and brief read fresh from disk; `AGENTS.md` (tracked project instructions) and the machine-local `CLAUDE.md` pointer; `skills/ship-spec/SKILL.md` (whole file); `docs/customizing.md` heading map and `:51`–`:60`; `skills/spec-cycle/SKILL.md:441`, `:459` (the `## Deferred (P2+)` rule); `skills/spec-close/SKILL.md:340` (companion rule); tracked `tests/` listing (5 test files, 20 fixture files); `git log` on the seven touched paths (newest commit still 1bd3f29, VHS-45, so round-2 anchors stand); wiki `projects/vigil-skills/state.md` and `filemap.md` (no `architecture.md` exists for this project); wiki `decisions/` listing re-scanned — no entry newer than round 2 overlaps (the one new vigil-skills entry, `2026-10-08-vhs-45-spec-tickets-files-blockers-first-no-resume.md`, concerns `/spec-tickets`, which this spec leaves alone). The three round-2 reports were read. Ticket lookup skipped per orchestrator note (ACL); the brief is the ticket text. `scale_lens` is off and no `scalability.md` exists in round-2.

Deferred-findings block: the spec has no `## Deferred — follow-up required` section, so there are no `D-<n>` rows, no preamble, and no ceiling to check. Its `## Deferred (P2+)` section (spec.md:276–285) is the advisory list `skills/spec-cycle/SKILL.md:459` describes, under that exact heading, and holds no P0/P1.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Override at the second halt has no defined outcome, and its printed text says "commit" while the tests are red | CLOSED (reworked) | spec § Decision 9, line 120: "There is no second review halt and Decision 8's block is not printed again"; a red loop "ends red like any other red loop: Phase 3's own halt block applies"; "Nothing is committed until the tests are green." Checklist row at line 244 matches. Decision 8's option 2 ("commit with each finding above recorded as overridden", line 108) is now reachable only at the one stop before any test re-run, where its text is true. No other site still refers to a second stop (lines 98, 182, 200, 240 checked). The direction change is deliberate and stated, and it moves the spec closer to brief Decision 15 ("the same halt menu"). Manifest claim and its 2-site recount verified. |
| correctness | F-2 (P2) | Review record cannot count an unresolved Blocks finding; two header fields have no value on a skip | PARTIAL | (a) closed: line 136 carries `<un> unresolved`. (b) closed: line 147 omits `Mode` and `Compared against` on a skipped run. (c) open: `overridden by operator` still takes no reason (line 144), and is not listed in § Deferred (P2+). See F-1 below. |
| correctness | F-3 (P3) | Scope row for `docs/customizing.md` omits the second edit | CLOSED | spec § Scope, line 14: "`## Spec & brief layout` gains the review file's path." |
| correctness | F-4 (P3) | Four round-1 P3/P4 items neither folded nor listed | DEFERRED | § Deferred (P2+), line 285 names correctness/R1/F-7, F-8, edge-cases/R1/F-13, conventions/R1/F-11. The `mode: inline` nit is closed at line 147. |
| edge-cases | F-1 (P2) | "Override" at the second stop has no stated outcome | CLOSED | Same rework as correctness F-1: the second stop no longer exists (line 120). |
| edge-cases | F-2 (P3) | Unusable Blocks finding has no stated group tag or count | CLOSED | § Decision 10, line 147: "An unusable finding labelled as a blocker is tagged `Blocks` and counted there." |
| edge-cases | F-3 (P3) | Halt option 1 marks every listed finding as fixed by operator | DEFERRED | § Deferred (P2+), line 285 (edge-cases/R2/F-3) |
| conventions | F-1 (P2) | Second halt reuses Decision 8's menu | CLOSED | Same rework (line 120). |
| conventions | F-2 (P2) | Review-record residue neither folded nor listed | CLOSED | Line 136 (`<un> unresolved`); line 147 (skipped-run omissions; "A `vetoed` finding counts as recorded"; "`Mode:` is the only spelling"). Item (e), reasons in two places, is now an explicit cross-reference at line 120 ("a reason allowed here in addition to Decision 8's list"). The one remaining record item is correctness F-2(c), filed as F-1 below. |
| conventions | F-3 (P3) | Review-command resolution reads two files; docs and test-command fallback describe one | PARTIAL | Unchanged at lines 34 and 206; not listed. P3, no disposition required. See F-3 below. |
| conventions | F-4 (P3) | Scope row for `docs/customizing.md` | CLOSED | Line 14. The hardcoded-paths sentence at `docs/customizing.md:60` is still not named; see F-5 below (P4). |
| conventions | F-5 (P3) | Spec-level additions, informational | CLOSED | No action was required. |
| conventions | F-6 (P4) | Four round-1 P3/P4 items unlisted | DEFERRED | § Deferred (P2+), line 285 |

No finding is REOPENED. The manifest line verifies: reworked, both named sites carry it.

## Findings

### F-1: Decision 9 records an override "with the reason", but the disposition list gives `overridden by operator` no reason slot
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9 (line 120) against § Decision 10 (line 144); § Deferred (P2+) (lines 278–285)
**Convention violated:** `skills/spec-cycle/SKILL.md:459`: "For P2 findings, either fix or list them in a `## Deferred (P2+)` section". Also the spec's own template as the single definition of the record's values.
**Evidence:** Line 120: "the finding is recorded as `overridden by operator` with the reason `fix broke <test>`". Line 144 lists `overridden by operator` bare, while `vetoed: <reason>` and `recorded: <reason>` carry a suffix. The implementer has two sources for one value. This is the open part (c) of correctness/R2/F-2, made visible by this round's rework; it is not in the Deferred list. An override at Decision 8's stop likewise loses why the finding was unresolved (for example the veto reason).
**Suggested fix:** In Decision 10's template change `overridden by operator` to `overridden by operator: <reason>` and add after line 147's last sentence: "The reason is why the finding was unresolved, or `fix broke <test>` under Decision 9." Or add one Deferred (P2+) line naming correctness/R2/F-2(c).

### F-2: The Design does not say which skill text carries Decision 9's hold rule and the added halt line
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9 (line 120) against § Design `skills/ship-spec/SKILL.md` (lines 183, 188) and § Scope (line 11)
**Convention violated:** Scope table and Design as the complete list of edits per file (the same convention round-2 F-4 applied to `docs/customizing.md`).
**Evidence:** Decision 9 now changes how Phase 3 behaves on re-entry: a Blocks fix is not undone, and "Phase 3's own halt block applies, with one added line naming the finding whose fix is being held." Phase 3's loop text says "identify the smallest blocking failure … fix it" (`skills/ship-spec/SKILL.md:108`–`:109`) and its halt block is a fixed literal (`:116`–`:127`). The Design lists one Phase 3 edit, the `N/A` sentence in the intro (line 188), and step 7 says only "Re-run the tests when Decision 9 says so" (line 183). The Scope row (line 11) names Phases 0, 3b, 4, 5 and 7 and not Phase 3 at all. An implementer can place the rule in Phase 3b step 7 or edit Phase 3's block; both work, and the two give different diffs to check against the Scope table.
**Suggested fix:** Extend Design step 7 to: "Re-run the tests when Decision 9 says so. This step states the hold rule for Blocks fixes, the revert rule for Fix-or-record fixes, and the one line added to Phase 3's halt block on this path; Phase 3's own loop and halt-block text are not edited." Add "Phase 3 intro: one sentence on `N/A`." to the Scope row for `skills/ship-spec/SKILL.md`.

### F-3: Review-command resolution reads two files; `docs/customizing.md` and the test-command fallback still describe one
**Severity:** P3
**Where:** spec § Decision 2 item 2 (line 34); § Design `docs/customizing.md` (line 206)
**Convention violated:** None broken. Carried from conventions/R2/F-3, unchanged and unlisted.
**Evidence:** The new doc section lands under `## What to put in your CLAUDE.md` (`docs/customizing.md:5`). The Design paragraph does not say the section may also sit in `AGENTS.md`, or that `CLAUDE.md` wins when both declare one. The test command still falls back to `CLAUDE.md` only (`skills/ship-spec/SKILL.md:21`).
**Suggested fix:** Add to the `docs/customizing.md` Design paragraph: "It states that the section is read from `CLAUDE.md` first and `AGENTS.md` second, and that this is wider than the test-command fallback, which reads `CLAUDE.md` only."

### F-4: Spec-level additions made this round, listed for the human drift check
**Severity:** P3
**Where:** spec § Decision 9 (line 120)
**Convention violated:** None. Class (c) items, each with its reason in the text.
**Evidence:** (1) Phase 3's halt block gains one line on the re-entry path; brief Decision 15 says "the same halt menu", and the options are unchanged. (2) A Blocks finding can become `overridden by operator` through Phase 3's manual-debug option, without passing Decision 8's three-option block; brief Decision 6 describes the override only at the review stop. The operator still makes the call and nothing commits on red, so brief Decisions 6 and 15 both hold. (3) A gate-applied Blocks fix is held inside the test loop; the brief is silent on this and the rule serves "A blocker never passes silently."
**Suggested fix:** None required.

### F-5: Two small text residues
**Severity:** P4
**Where:** spec § Deferred (P2+) (line 279); § Design `docs/customizing.md` (line 206)
**Convention violated:** None.
**Evidence:** (a) Line 279 says "the halt blocks print the findings". After the rework, a halt in the re-entered loop prints Phase 3's block with one line naming the held finding, not the findings. (b) `docs/customizing.md:60` ("the skills hardcode the spec/reviews/test-output paths today") will name three paths when there are four.
**Suggested fix:** Line 279: "Decision 8's block prints the findings and Phase 3's block names the held one". Add "and to the hardcoded-paths sentence" to the Design paragraph at line 206.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 2 | P4: 1

STATUS: GREEN
