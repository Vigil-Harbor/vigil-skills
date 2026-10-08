# Edge-Cases Review — round 3

Grounding notes: spec and brief read fresh from disk; machine-local `CLAUDE.md` (pointer file) and `skills/ship-spec/SKILL.md` (whole file, including Phase 3's halt block at `:114`–`:129`) re-read; all three round-2 reports read. The ticket lookup was skipped as instructed (ACL on namespace `skills`); the brief stands in for the ticket. `scale_lens` is off and no `scalability.md` exists in round-2. The spec has no `## Deferred — follow-up required` section, so there are no D-rows, no preamble and no ceiling to check. Its `## Deferred (P2+)` list (spec.md:276–285) is the advisory list; items in it are acknowledged and not re-filed.

## Closure of round 2 findings

"ACK" means the item is listed in the spec's `## Deferred (P2+)` section. "OPEN" means a P3/P4 that was neither folded nor listed; it has no gate effect.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Override at the second halt has no defined outcome, and its printed text says "commit" while the tests are red | CLOSED | Deliberate direction change with rationale. spec § Decision 9, line 120: the second halt is gone ("There is no second review halt and Decision 8's block is not printed again"); a red loop "ends red like any other red loop: Phase 3's own halt block applies"; "Nothing is committed until the tests are green." Checklist row at line 244 reworded to match. Both manifest sites verified. Decision 8's "stop once" (line 98) is now true, and option 2's "commit" wording (line 108) is only ever printed before the test re-run, where step 7 still stands between it and the commit. Phase 3's halt block (`skills/ship-spec/SKILL.md:114`–`:129`) has no option that commits. |
| correctness | F-2 (P2) | Review record cannot count an unresolved Blocks finding; two header fields have no value on a skip | PARTIAL (P2) | Folded: `<un> unresolved` in the `Blocks:` line (line 136); `Mode` and `Compared against` omitted on a skip (line 147). Remaining: part (c), `overridden by operator` takes no reason in the template (line 144), and Decision 9 now requires one (`fix broke <test>`). Carried as F-2 below. |
| correctness | F-3 (P3) | Scope row for `docs/customizing.md` omits the second edit | CLOSED | spec § Scope, line 14: "`## Spec & brief layout` gains the review file's path." |
| correctness | F-4 (P3) | Four round-1 P3/P4 items neither folded nor listed | ACK | § Deferred (P2+), line 285 lists them; the `mode: inline` nit is folded at line 147 |
| edge-cases | F-1 (P2) | "Override" at the second stop has no stated outcome for the fix or the tests | CLOSED | Same rework as correctness F-1; the second stop no longer exists (line 120) |
| edge-cases | F-2 (P3) | Unusable Blocks finding has no stated group tag or count | CLOSED | § Decision 10, line 147: "An unusable finding labelled as a blocker is tagged `Blocks` and counted there." |
| edge-cases | F-3 (P3) | Halt option 1 marks every listed finding as fixed by operator | ACK | § Deferred (P2+), line 285 |
| conventions | F-1 (P2) | Second halt reuses Decision 8's menu | CLOSED | Same rework; line 120 |
| conventions | F-2 (P2) | Review-record residue neither folded nor listed | CLOSED | Line 136 (`<un>`), line 147 (skip omissions, vetoed counts as recorded, `Mode:` spelling). Part (e), record reasons in two places, is left with an explicit cross-reference at line 120 ("a reason allowed here in addition to Decision 8's list"), which is enough. |
| conventions | F-3 (P3) | Review command read from two files; `docs/customizing.md` Design still describes one | OPEN (P3) | § Design `docs/customizing.md`, line 206 unchanged; not in § Deferred (P2+) |
| conventions | F-4 (P3) | Scope row for `docs/customizing.md` | CLOSED | Line 14 |
| conventions | F-5 (P3) | Spec-level additions listed for the drift check | CLOSED | No action was required; item (4), the second operator stop, is removed by the rework |
| conventions | F-6 (P4) | Four round-1 P3/P4 items unchanged and unlisted | ACK | § Deferred (P2+), line 285 |

Manifest verdict: correctness/F-1 "reworked" is verified. The direction change is deliberate and stated, both named sites carry it, and no REOPENED item results. No finding is REOPENED.

## Findings

Walked for the rework: every exit of the re-entered loop (green; red then Phase 3 option 1, 2 or 3), with a gate-applied Blocks fix, with an operator hand fix, with a reverted Fix-or-record fix, with an `N/A` test command, and with an override at the first halt and no fix applied. None commits on red, and none drops a blocking finding without an operator in the path. The findings below are record-accuracy gaps.

### F-1: An operator's hand fix is not covered by the "not undone" rule
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9, line 120, against § Decision 8, line 112
**Edge case:** Partial failure after halt option 1. The operator fixes a Blocks finding by hand and resumes; the finding is recorded `fixed by operator`; step 7 re-enters the Phase 3 loop; the operator's change is what turns a test red.
**What happens:** Line 120 protects "a fix the gate applied for a Blocks finding". A hand fix is not one the gate applied, so the sentence does not cover it, and the added halt line ("naming the finding whose fix is being held") is not required for it either. Phase 3's loop says "identify the smallest blocking failure ... fix it" (`skills/ship-spec/SKILL.md:108`–`:109`), and the smallest change may be to take the operator's edit back out. The record would then say `fixed by operator` for a tree that no longer holds the fix. The sentence "The dispositions in the review file describe the tree that is committed" would lead a careful agent to correct the record or stop, and an agent is unlikely to revert an operator's edit, so this does not gate. The rule is one clause short of saying so.
**Why the spec misses it:** The protection was written in round 1 for gate-applied fixes, before option 1's resume path was routed through step 7.
**Suggested fix:** In Decision 9, line 120, change "a fix the gate applied for a Blocks finding is not undone to get the tests green" to "a fix for a Blocks finding, whether the gate applied it or the operator made it by hand, is not undone to get the tests green".

### F-2: `overridden by operator` has a reason in Decision 9 and no place for one in the template
**Severity:** P3
**Where:** spec § Decision 9, line 120; § Decision 10, line 144
**Edge case:** The operator removes a held Blocks fix from Phase 3's manual-debug option.
**What happens:** Decision 9 says the finding is recorded "as `overridden by operator` with the reason `fix broke <test>`". The Disposition line offers `overridden by operator` with no suffix, while `vetoed` and `recorded` carry `: <reason>`. The agent either drops the reason or invents the form. This is also what remains of correctness/R2/F-2 part (c). Nothing is lost that the PR line does not also count.
**Suggested fix:** In the template at line 144 write `overridden by operator[: <reason>]`, and add to line 147: "An override at Decision 8's halt carries the reason the finding was unresolved; an override under Decision 9 carries `fix broke <test>`."

### F-3: The held-fix line and the override are worded for one finding and for removal "by hand"
**Severity:** P3
**Where:** spec § Decision 9, line 120
**Edge case:** (a) The gate applied fixes for several Blocks findings and the loop stays red. (b) At Phase 3's halt the operator tells the agent to take the fix out instead of doing it personally.
**What happens:** (a) "one added line naming the finding whose fix is being held" is singular; the agent often cannot tell which fix broke the test, so it must name all of them or guess. (b) "If the operator removes that fix by hand" does not cover an instruction to the agent. Decision 8 says a Blocks finding "is never declined by the agent", so a literal agent could refuse the instruction; a careful one treats it as the operator's override. Both resolve with the operator present.
**Suggested fix:** Change to "with one added line naming each Blocks finding whose fix is being held", and "If the operator removes that fix, or tells the agent to remove it, from Phase 3's halt, the finding is recorded as `overridden by operator`".

### F-4: A red loop held by a Blocks fix spends all five iterations before the halt
**Severity:** P4
**Where:** spec § Decision 9, line 120
**Edge case:** The only cause of the red tests is the held Blocks fix.
**What happens:** Round 2's "stop the loop without spending the remaining iterations" went out with the second halt. The loop now runs five iterations in which the one change that would turn the tests green is forbidden, so the agent's remaining moves are edits elsewhere, test files included. Phase 3 has the same exposure today, and the halt still arrives; this costs time and invites a weakened test.
**Suggested fix:** Optional sentence in Decision 9: "When the agent judges that only undoing a held fix would turn the tests green, it goes to Phase 3's halt block without spending the remaining iterations."

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 1

STATUS: GREEN
