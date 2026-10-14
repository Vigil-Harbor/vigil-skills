# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Terminal red revisions bypass the immutable ground-truth ledger | CLOSED | Spec § Decision 4, lines 79–80 adds checked immutable terminal addenda for final-pass and grill revisions; §§ Decision 9, Revision and synthesis integration, Test plan, and Done when propagate the contract. |
| correctness | F-2 | The no-Python flow skips the ledger it promises to preserve | CLOSED | Spec § Pre-dispatch flow, line 222 now skips checker step 3 while retaining ledger preparation and finalization; Test plan line 258 pins the behavior. |
| correctness | F-3 | Ticket not cached | PARTIAL | The ticket/shared-memory service remains unavailable; this pass again used brief lines 54–71 as degraded authority. See F-2. |
| correctness | F-4 | Touched review machinery changed within the freshness window | PARTIAL | Fresh reads confirm the cited symbols still resolve at baseline `fc20f94`, but `fad52c7`, `f64bebe`, and `d3730b1` changed the same review surfaces on 2026-10-12/13. See F-3. |
| edge-cases | F-1 | Deleted headings have no valid coverage representation | CLOSED | Spec § Decision 3, lines 50–63 defines `(removed)` tombstones and rename pairs; § Decision 6 line 115 splits checker/orchestrator ownership; Test plan line 255 covers deletion and rename. |
| edge-cases | F-2 | Unavailable-Python flow skips the ledger it must dispatch | CLOSED | Spec § Pre-dispatch flow line 222 retains steps 2 and 6 while skipping only checker step 3; Test plan line 258 requires finalization and dispatch on that path. |
| edge-cases | F-3 | Checker-driven spec edits leave expected coverage stale | CLOSED | Spec § Decision 7, line 124 requires recomputing the predecessor diff and rebuilding the temporary ledger after a checker-driven spec edit; Test plan line 257 pins the regression. |
| edge-cases | F-4 | Ticket lookup remains unavailable | PARTIAL | The external ticket source is still unavailable; review proceeded from the brief as required. See F-2. |
| conventions | F-1 | No-Python path skips the required ledger preparation | CLOSED | Spec § Pre-dispatch flow line 222 explicitly skips step 3, not step 2, and retains ledger finalization in step 6. |
| conventions | F-2 | Review-driven operational additions need drift-check visibility | PARTIAL | The earlier caps, cleanup, timeout, and post-green contracts remain, and round 3 adds terminal addenda, removed-heading tombstones, and retry-time coverage rebuilding. They are reasoned category-(c) additions but still lack a grouped drift-check note. See F-1. |
| conventions | F-3 | Ticket cache remains inaccessible | PARTIAL | Ticket/shared-memory/network access remains unavailable; the brief records the same-day tracker result at line 90. See F-2. |

## Findings

### F-1: Review-introduced contracts still need drift-check visibility
**Severity:** P3  
**Where:** spec.md:61–79, spec.md:124, spec.md:238  
**Convention violated:** Silent-additions classification; these are category-(c) spec-level additions with rationale  
**Evidence:** Beyond the brief’s carried-forward decisions, the candidate now specifies removed-heading tombstones, final-red/grill terminal ledger addenda, stale-temp cleanup, size and timeout bounds, retry-time coverage rebuilding, and a post-green runtime-claim prohibition. The additions are justified and fit the live workflow, but the conventions lens requires category-(c) additions to be surfaced for the human drift check.  
**Suggested fix:** Add one concise drift-check note grouping these review-introduced operational contracts so the operator explicitly accepts them before implementation.

### F-2: Ticket source remains unavailable
**Severity:** P3  
**Where:** brief.md:90  
**Convention violated:** Ticket-grounding fallback  
**Evidence:** Ticket/shared-memory/network access is unavailable for this review. The brief records a direct tracker read dated 2026-10-13 and states that the ticket has no acceptance criteria, so it remains the degraded authority.  
**Suggested fix:** Re-run ticket grounding before implementation if the canonical ticket may have changed.

### F-3: Review surfaces remain inside the freshness window
**Severity:** P3  
**Where:** spec § Scope  
**Convention violated:** Fresh grounding for recently changed lifecycle contracts  
**Evidence:** Read-only history shows `fad52c7` and `f64bebe` on 2026-10-13 and `d3730b1` on 2026-10-12 touching `/spec-cycle`, reviewer contracts, workflow documentation, or AGENTS.md. The candidate’s live anchors currently resolve at HEAD `fc20f94`, including `sync.py:30`, `sync.py:48-57`, and `skills/spec-cycle/SKILL.md:378`, `:380`, `:388`, `:503-513`, and `:698`.  
**Suggested fix:** Re-run the artifact-ordering, dispatch-input, terminal-revision, delta-coverage, and divergence checks immediately before implementation.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 3 | P4: 0

STATUS: GREEN
