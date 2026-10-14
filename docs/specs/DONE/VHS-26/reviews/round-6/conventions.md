# Conventions Review — round 6

Mode: delta. Round 6 is green from the conventions lens: no P0 or P1, two P3 and two P4.

Grounding notes:
- The repo's tracked conventions live in `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\AGENTS.md`; `CLAUDE.md` only points there.
- The wiki has no `architecture.md` for this project; `state.md` and `filemap.md` exist.
- Decisions read for overlap: `2026-10-13-vhs-27-delta-scoped-review-passes.md`, `2026-10-13-vhs-60-delta-scope-resolver-and-full-pass-recovery.md`, `2026-08-09-review-round-artifacts-are-immutable.md`, `2026-10-12-vhs-43-in-scope-p1-always-folds.md`.
- Every `file:line` citation inside the changed regions resolves at the current files: `skills/spec-cycle/SKILL.md:390`, `:578-579`, `:594-601`, `:715`, `:757`, and `agents/spec-reviewer-correctness.md:109`. No anchor drift.

## Closure of round 5 findings

The closure manifest is empty because round 5 closed green with no P0/P1. The table covers the round-5 P2–P4 findings against the current spec.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P2) | First-match order puts the unsupported-anchor P1 ahead of Anchor drift | CLOSED | spec.md:133-138: rules reordered (`Anchor: none`, unreadable out-of-root, row-only P2, Anchor drift, unsupported P1); rule 5 now requires "file and symbol resolve" |
| correctness | F-2 (P3) | Preamble lists the Decision 6 phrase while Apply-findings says "no manifest vocabulary" | CLOSED | spec.md:172 "adds one process phrase and no section-naming form" |
| correctness | F-3 (P3) | Illustrative block does not show the new-spec line | CLOSED | spec.md:71 states where the line sits; the block itself is unchanged |
| correctness | F-4 (P3) | Ticket not cached | N/A (process) | Recurs this round, see F-2 below |
| edge-cases | F-1 (P2) | First-match order misgrades three row states | CLOSED | spec.md:134-138; Test plan spec.md:200 names each grade |
| edge-cases | F-2 (P3) | Phase 1 told to "build" the file before a round directory exists | CLOSED | spec.md:156 "hold the rows … written at dispatch (Decision 5), not during Phase 1" |
| edge-cases | F-3 (P3) | Sample P1 outside `changed_regions` has no filing permission | CLOSED | spec.md:140 "filed against the section the row names, on a full or a delta pass" |
| edge-cases | F-4 (P3) | Ticket lookup blocked | N/A (process) | Recurs this round, see F-2 below |
| conventions | F-1 (P3) | Unsupported-anchor rule precedes Anchor drift | CLOSED | spec.md:137-138; matches VHS-27 decision 9 and `agents/spec-reviewer-correctness.md:109` |
| conventions | F-2 (P3) | Closure route for other lenses rests on unedited text | CLOSED | spec.md:110 "The path stands in for the `§` anchor: a reviewer closes the finding by checking that the file exists with content" |
| conventions | F-3 (P3) | Spec-level additions not all listed in the preamble | CLOSED | spec.md:32 adds the no-anchor P2 and the `changed_regions` rule; rationale reworded at spec.md:136 |
| conventions | F-4 (P4) | Green-round sentence sits in the §2e block | CLOSED | spec.md:112 "(by the existing 2g carry-forward, which this ticket does not edit)" |

Deferred-findings block: the preamble is present, there is one section, and row D-1 is well-formed. All seven fields are present, the `Suggested fix` is blockquoted, and its three propagation sites all exist. Its `Scope` token is `out-of-scope`, and the stated region (`skills/spec-cycle/SKILL.md` §2g) has no row in the brief's Scope table, so the ceiling does not apply. No routing violation.

Deleted `## Deferred (P2+)`: its only entry (correctness/R5/F-1 with edge-cases/R5/F-1) asked for the Decision 8 grading reorder. The current rule order is the order that entry suggested, so the removal drops nothing unresolved.

## Findings

### F-1: Spec-level additions in this revision, for the human drift check
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (spec.md:128, :136, :140); spec § Decisions (spec.md:32)
**Convention violated:** Silent-addition audit, category (c): additions with rationale stay visible to the drift check.
**Evidence:**
- **Filing rule on a delta pass.** The new sentence at spec.md:140 gives the Ground-truth check its own filing permission outside `changed_regions`. The byte-identical `# Delta scope` block (`agents/spec-reviewer-correctness.md:90-98`) names only a P0 as fileable outside the changed regions. The addition is consistent with VHS-27 decision 7 ("grounding and process failures … run everywhere at their existing severities"). The preamble covers the read ("the row sample is not limited by `changed_regions`") but not the filing sentence.
- **No-anchor P2.** A sampled sentence with no anchor is advisory (rule 3). It is now listed in the preamble and permitted by brief Risks item 3. It softens brief Decision 1 ("needs a `file:line` anchor") at enforcement time.
- Neither item contradicts a brief fence: no parser, no computed inventory, no edit to `# Delta scope`.

**Suggested fix:** Optional. Extend the preamble bullet at spec.md:32 to read "…the row sample is not limited by `changed_regions`, and its findings are filed on a delta pass".

### F-2: Ticket lookup denied
**Severity:** P3
**Where:** grounding (process)
**Convention violated:** None; this records a degraded grounding step.
**Evidence:** `memory_search` with tags `[plane_work_item, VHS-26]` in namespace `skills` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The review proceeded on the brief, which says the ticket carries no acceptance criteria.
**Suggested fix:** None for the spec.

### F-3: Two small wording gaps in the changed Decision 8 and Test plan text
**Severity:** P4
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (spec.md:134, :138, :140); spec § Test plan (spec.md:200)
**Convention violated:** Clarity; one name for one thing.
**Evidence:**
- Rules 1 and 5 file "against the spec section that holds the claim", while the closing sentence at spec.md:140 says "against the section the row names". These differ when the row's `Spec section` is wrong.
- The Test plan list now gives an expected grade for most cases, but "a sentence with no anchor", "a row whose anchor differs from a correct spec sentence" and "a row whose sentence is not in the spec" carry none. All three are P2 under rule 3.

**Suggested fix:** Use one phrase for the filing section, for example "the section that holds the claim, or the section the row names when the sentence is not in the spec". Add "(P2)" to the three ungraded Test plan cases.

### F-4: The Decision 8 fold leaves no trace in the spec
**Severity:** P4
**Where:** spec § Deferred (P2+) (deleted; body at `docs/specs/TODO/VHS-26.reviews/round-5/spec.copy.md:253-255`)
**Convention violated:** Loose analogy to 2g step 4 (`skills/spec-cycle/SKILL.md:965-969`), which records a folded P2 in `## Post-green polish` when it removes the `## Deferred (P2+)` entry.
**Evidence:** The entry said "Not folded in polish: the list is in Decision 8." The fold was then made by hand outside 2g, and the section was deleted. 2g does not govern a hand fold that is followed by a re-review, and the round-5 reports keep the record, so nothing is lost.
**Suggested fix:** None required.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 2

STATUS: GREEN
