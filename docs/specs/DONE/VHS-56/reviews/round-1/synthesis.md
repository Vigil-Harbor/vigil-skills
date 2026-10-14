# Synthesis — round 1

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P0) "Cycle-2 failure has conflicting irreversible outcomes" — sites: 3 — separate successful cap completion from dispatch failure and enforce the irreversible gate across tier changes.
- correctness/F-2 (P1) "Adding a decision under no-grill leaves the previous review valid" — sites: 2 — invalidate and rerun the doubt pass after the existing `--no-grill` decision-addition branch.
- edge-cases/F-1 (P1) "A partially failed pass can become valid for an irreversible brief" — sites: 3 — same failure-state root as correctness/F-1.
- edge-cases/F-2 (P1) "Adding a decision under `--no-grill` retains a stale doubt result" — sites: 2 — same Confirm invalidation root as correctness/F-2.
- conventions/F-1 (P0) "A failed second cycle can become an irreversible completion" — sites: 3 — same failure-state root as correctness/F-1.

## Consider
(none)

## Noted
- correctness/F-3 (P2) "ground-truth ledger omits runtime claims" — advisory ledger coverage; hold the missing rows for round 2.
- correctness/F-4 (P3) "ticket not cached" — shared-memory permission degradation; no speculative spec edit.
- edge-cases/F-3 (P2) "Ticket grounding was blocked by namespace permissions" — environment limitation; no spec edit.
- edge-cases/F-4 (P3) "The persisted operator skip reason has no size bound" — optional bounded-audit improvement.
- conventions/F-2 (P2) "Confirm invalidation omits the existing no-grill decision-addition path" — duplicate of the blocking correctness/edge finding and folded with it.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Cycle-2 dispatch failure can satisfy irreversible after a tier change | correctness/F-1; edge-cases/F-1; conventions/F-1 | correctness; edge-cases; conventions | P0; P1; P0 | Act on |
| `--no-grill` Add a decision retains stale doubt result | correctness/F-2; edge-cases/F-2; conventions/F-2 | correctness; edge-cases; conventions | P1; P1; P2 | mixed: correctness/F-2 Act on; edge-cases/F-2 Act on; conventions/F-2 Noted |
| Ground-truth ledger coverage | correctness/F-3 | correctness | P2 | Noted |
| Ticket/shared-memory access degradation | correctness/F-4; edge-cases/F-3 | correctness; edge-cases | P3; P2 | Noted |
| Operator skip-reason size | edge-cases/F-4 | edge-cases | P3 | Noted |
