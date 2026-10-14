# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Terminal red revisions bypass the immutable ground-truth ledger | CLOSED | Spec § Decision 4, line 79 adds immutable `ground-truth.after-revision.md` and `ground-truth.after-grill-<G>.md` artifacts before terminal completion; §§ Decision 9 and Revision and synthesis integration, lines 148 and 234, carry the rule through final and grill revisions. |
| correctness | F-2 | The no-Python flow skips the ledger it promises to preserve | CLOSED | Spec § Pre-dispatch flow, line 222 now skips checker step 3 while retaining ledger preparation and finalization in steps 2 and 6; Test plan line 258 pins that path. |
| correctness | F-3 | Ticket not cached | CLOSED | Round 2 correctly followed the degraded-authority path. Ticket/shared memory remains unavailable and is reported anew as F-2. |
| correctness | F-4 | Touched review machinery changed within the freshness window | CLOSED | All live anchors were reread at `fc20f94`; the continuing freshness condition is reported anew as F-3. |
| edge-cases | F-1 | Deleted headings have no valid coverage representation | CLOSED | Spec § Decision 3, lines 50–63 defines removed-heading tombstones and rename pairs; § Decision 6 line 115 validates current versus removed entries; Test plan line 255 covers deletion and rename. |
| edge-cases | F-2 | Unavailable-Python flow skips the ledger it must dispatch | CLOSED | Spec § Pre-dispatch flow, line 222 explicitly preserves preparation and finalization while skipping only checker execution. |
| edge-cases | F-3 | Checker-driven spec edits leave expected coverage stale | CLOSED | Spec § Decision 7, line 124 requires recomputing the predecessor diff and expected coverage, then rebuilding the temporary ledger after a checker-driven spec edit; Test plan line 257 covers the unchanged-to-changed retry. |
| edge-cases | F-4 | Ticket lookup remains unavailable | CLOSED | Round 2 correctly degraded to the brief. The current independent grounding limitation is reported once as F-2. |
| conventions | F-1 | No-Python path skips the required ledger preparation | CLOSED | Spec § Pre-dispatch flow, line 222 now says the no-Python path skips step 3, not ledger preparation in step 2. |
| conventions | F-2 | Review-driven operational additions need drift-check visibility | PARTIAL | The operational additions remain explicit and reasoned in Decisions 4, 5, 7 and Revision and synthesis integration, but the requested drift-check note grouping them as review-introduced contracts is still absent. See F-4. |
| conventions | F-3 | Ticket cache remains inaccessible | CLOSED | Round 2 correctly used the brief’s same-day tracker record as degraded authority. Current unavailability is reported once as F-2. |

## Findings

### F-1: Terminal addenda cannot always be “checked”
**Severity:** P0  
**Where:** spec.md:79, spec.md:258, spec.md:270  
**Claim:** Terminal revisions finalize a “checked immutable addendum,” and tests require final-red and grill edits to “finalize checked immutable addenda or restore pre-edit bytes on gate failure.”  
**Why this is wrong:** Decision 4 explicitly says that when Python is unavailable, the terminal addendum is written without running `check_spec.py` (line 79), matching brief Decision 14 (`brief.copy.md:50`). That path neither produces a checked addendum nor restores the edit as a gate failure, contradicting both the Test plan contract at line 258 and Done-when item 1 at line 270. An implementer cannot satisfy those statements and the required no-Python continuation simultaneously.  
**Suggested fix:** Qualify the terminal contract consistently: the addendum is checker-validated when Python is available and persisted unvalidated under the explicit unavailable-Python exception. Update Test plan item 9 and Done-when item 1, and add a regression that the terminal no-Python path writes the addendum without claiming validation.

### F-2: Ticket grounding remains unavailable
**Severity:** P3  
**Where:** brief.md:90  
**Claim:** The brief records Plane VHS-26 as the canonical ticket source and states that it has no acceptance criteria.  
**Why this is wrong:** Ticket/shared-memory/network access is unavailable for this pass, so the current ticket description and acceptance criteria could not be independently verified. Review proceeded from the brief as required.  
**Suggested fix:** Re-run ticket grounding before implementation if the canonical ticket may have changed.

### F-3: Touched review surfaces changed within the last seven days
**Severity:** P3  
**Where:** spec § Scope  
**Claim:** The implementation will modify `/spec-cycle`, two reviewer definitions, workflow documentation, README, and AGENTS.md.  
**Why this is wrong:** Read-only history shows same-day changes on these surfaces: `fad52c7` and `f64bebe` on 2026-10-13, plus `d3730b1` on 2026-10-12. Fresh reads confirm the cited symbols and anchors still resolve at HEAD `fc20f94`, so this is a freshness warning rather than a demonstrated design defect.  
**Suggested fix:** Re-run anchor and integration checks immediately before implementation, especially artifact ordering, terminal addenda, delta coverage, and divergence handling.

### F-4: Review-introduced operational contracts remain implicit in the drift check
**Severity:** P3  
**Where:** spec §§ Decision 4, Decision 5, Decision 7, Revision and synthesis integration  
**Claim:** Stale-temp pruning, resource caps, subprocess timeouts, and the post-green runtime-claim prohibition are explicit spec Decisions.  
**Why this is wrong:** These additions remain reasonable and documented, but the round-2 conventions finding requested a grouped note identifying them as review-introduced operational contracts for operator acceptance. The current Phase 3 drift check enumerates brief decisions, criteria, and fences, so these additions are not surfaced there as additions beyond the brief.  
**Suggested fix:** Add a short drift-check note grouping the review-introduced operational contracts.

## Summary

P0: 1 | P1: 0 | P2: 0 | P3: 3 | P4: 0

STATUS: RED P0=1 P1=0 P2=0 P3=3 P4=0
