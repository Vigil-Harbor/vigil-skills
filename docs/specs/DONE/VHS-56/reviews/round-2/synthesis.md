# Synthesis — round 2

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P1) "Recovery requires two successful cycles even when the second is forbidden" — sites: 3 — require every dispatch called for by the conditional cycle rule to succeed; allow a clean restarted cycle 1 to complete the irreversible pass.
- edge-cases/F-1 (P0) "Restart requires a second cycle that the cycle rule can forbid" — sites: 3 — same restart-state root as correctness/F-1.

## Consider
(none)

## Noted
- correctness/F-2 (P2) "Ticket-only derivation anchor exists only in the ledger" — pre-ship recommended; add the sentence-local source anchor.
- correctness/F-3 (P2) "Atomic-write anchor exists only in the ledger" — pre-ship recommended; add the sentence-local source anchor.
- correctness/F-4 (P2) "General invalidation wording should exempt tier-only changes" — pre-ship recommended; make the existing tier-only exception explicit.
- correctness/F-5 (P3) "ticket not cached" — shared-memory permission degradation already recorded; no speculative scope edit.
- edge-cases/F-2 (P2) "Ticket grounding remains blocked by namespace permissions" — same environment limitation as correctness/F-5.
- conventions/F-1 (P2) "Recovery wording implies an unconditional second cycle" — pre-ship recommended duplicate of the blocking restart finding and folded with it.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Restarted irreversible pass conflicts with the conditional cycle-2 rule | correctness/F-1; edge-cases/F-1; conventions/F-1 | correctness; edge-cases; conventions | P1; P0; P2 | mixed: correctness/F-1 Act on; edge-cases/F-1 Act on; conventions/F-1 Noted |
| Sentence-local runtime anchors | correctness/F-2; correctness/F-3 | correctness | P2; P2 | Noted |
| Tier-only invalidation exception | correctness/F-4 | correctness | P2 | Noted |
| Ticket/shared-memory access degradation | correctness/F-5; edge-cases/F-2 | correctness; edge-cases | P3; P2 | Noted |
