# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Terminal red revisions bypass the immutable ground-truth ledger | CLOSED | Spec lines 79, 148, 234, 258, and 270 add checked immutable terminal addenda for final-red and grill revisions, restore pre-edit bytes on gate failure, and cover the behavior in tests and Done-when item 1. |
| correctness | F-2 | The no-Python flow skips the ledger it promises to preserve | CLOSED | Spec line 222 now skips only checker step 3 and explicitly retains ledger preparation and finalization; line 258 adds the corresponding contract regression. |
| correctness | F-3 | Ticket not cached | PARTIAL | The ticket/shared-memory service remains unavailable, so this review again used the brief as degraded authority. See F-3. |
| correctness | F-4 | Touched review machinery changed within the freshness window | CLOSED | The round-3 baseline is current HEAD `fc20f94026c3b06ca130a1822e157e80bcde533e`; fresh reads confirm the cited anchors still resolve in `skills/spec-cycle/SKILL.md` and `sync.py`. |
| edge-cases | F-1 | Deleted headings have no valid coverage representation | PARTIAL | Lines 50, 61–63, 115, 156, 255, and 270 add removed-heading tombstones for ordinary unique headings, but a deletion or rename of one duplicate heading still has no valid representation because the tombstone must name a heading absent from the current spec. See F-1. |
| edge-cases | F-2 | Unavailable-Python flow skips the ledger it must dispatch | CLOSED | Spec lines 132 and 222 require preparation, finalization, and correctness dispatch of the ledger when Python is unavailable; line 258 pins that path. |
| edge-cases | F-3 | Checker-driven spec edits leave expected coverage stale | CLOSED | Spec line 124 requires recomputing the predecessor diff and expected coverage against the same saved predecessor, rebuilding the temp ledger, and then retrying; line 257 adds the regression. |
| edge-cases | F-4 | Ticket lookup remains unavailable | PARTIAL | The supplied environment still has no ticket/shared-memory access. Review proceeded from the brief as required. See F-3. |
| conventions | F-1 | No-Python path skips the required ledger preparation | CLOSED | Spec line 222 now explicitly skips only step 3 and preserves steps 2 and 6; line 258 covers finalization and dispatch. |
| conventions | F-2 | Review-driven operational additions need drift-check visibility | PARTIAL | The operational contracts remain rationalized in Decisions 4, 5, and 7, but the spec still has no explicit drift-check note grouping them for operator acceptance. |
| conventions | F-3 | Ticket cache remains inaccessible | PARTIAL | Ticket grounding remains unavailable; the brief’s recorded tracker read remains the degraded authority. See F-3. |

## Findings

### F-1: Duplicate-heading deletion still has no valid tombstone
**Severity:** P0  
**Where:** spec.md:61-63; spec.md:115  
**Edge case:** A revision deletes or renames one heading while an identically worded heading remains elsewhere in the current spec. The live changed-regions algorithm explicitly supports duplicate headings by pairing the nth identical full heading stack (`skills/spec-cycle/SKILL.md:480`).  
**What happens:** Expected coverage must include the deleted heading as `§ <heading> (removed)`, but the checker must reject that tombstone because a heading with the same text still exists in the current spec. Omitting it fails exact expected-coverage comparison. No ledger can pass, so reviewer dispatch is blocked on a valid spec edit. Current-side coverage and `Spec locations` are also unable to distinguish the duplicate sections.  
**Why the spec misses it:** Tombstone identity is only the leaf heading text, while the source diff’s identity is the full heading stack plus occurrence order. The round-2 fix handles unique deleted headings but discards the identity needed for duplicates.  
**Suggested fix:** Give coverage and `Spec locations` an unambiguous identity derived from the changed-regions algorithm, such as the full heading stack plus occurrence ordinal. Validate tombstone absence for that identity rather than global absence of the leaf text, and add duplicate-heading deletion and rename regressions.

### F-2: Terminal gate failures emit a false dispatch message
**Severity:** P2  
**Pre-ship recommended:** yes  
**Where:** spec.md:79; spec.md:124-132  
**Edge case:** The checker repeats a diagnostic or times out while validating a final-pass or post-grill terminal addendum.  
**What happens:** The spec restores the pre-edit bytes and halts using Decision 7’s message, which says `no reviewer dispatched; marker unchanged`. In this path the final-round reviewers already ran, reports and synthesis already exist, and the marker remains pending. The operator is told an incorrect execution history and is not told that terminal edits were rolled back.  
**Why the spec misses it:** Decision 7’s diagnostics were designed for the pre-dispatch gate and are reused verbatim after dispatch without terminal-path context.  
**Suggested fix:** Define terminal-specific repeated-failure and timeout messages naming the addendum kind/path, cumulative round, successful rollback, already-persisted reviewer reports, and resulting marker state. Pin both messages in the orchestrator-contract tests.

### F-3: Ticket lookup remains unavailable
**Severity:** P3  
**Where:** brief.md:90  
**Edge case:** The ticket/shared-memory service and network are unavailable during review.  
**What happens:** Current Plane ticket contents cannot be independently verified; this pass relies on the brief as degraded authority.  
**Why the spec misses it:** This is an environmental grounding limitation, not a design defect.  
**Suggested fix:** Re-run ticket grounding when the service is available if the canonical ticket may have changed.

## Summary

Persistence checks covered atomic finalization, size bounds, retry behavior, read-side use, schema lifetime, and the explicitly unsupported same-spec concurrency case. The blocking issue is the persisted ledger’s inability to identify a removed duplicate heading.

P0: 1 | P1: 0 | P2: 1 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=0 P2=1 P3=1 P4=0
