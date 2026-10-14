# Synthesis — round 4

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P0) "Explicit coverage cannot represent the before-first-heading region" — sites: 5 — add a canonical pre-heading identity variant, align BOM normalization, and test insert/change/delete behavior.
- correctness/F-2 (P0) "The orchestrator cannot observe the retry identity it must compare" — sites: 4 — emit a stable hashed owner token in every diagnostic and compare that observable token across checker processes.
- correctness/F-3 (P2, Pre-ship recommended) "Terminal messages still cannot always report the actual marker state" — sites: 2 — render the complete marker-reader result rather than restricting state to pending/red.
- edge-cases/F-1 (P0) "Before-first-heading changes have no ledger identity" — sites: 5 — same composed pre-heading identity and BOM-normalization fix as correctness/F-1.

## Consider
(none)

## Noted
- correctness/F-4 (P3) "Ticket grounding remains unavailable" — expected degraded-path environment; the brief remains the local authority.
- correctness/F-5 (P3) "Touched workflow surfaces remain inside the freshness window" — implementation must re-read current review machinery and anchors.
- correctness/F-6 (P3) "Review-introduced contracts still lack grouped drift-check visibility" — surface all review-introduced contracts in the operator drift check.
- edge-cases/F-2 (P3) "Ticket lookup remains unavailable" — duplicate environmental note for correctness/F-4.
- edge-cases/F-3 (P3) "Review-introduced contracts remain absent from the drift check" — duplicate drift note for correctness/F-6.
- edge-cases/F-4 (P3) "Recently changed integration surfaces require implementation-time rereading" — duplicate freshness note for correctness/F-5.
- conventions/F-1 (P3) "Review-introduced contracts remain outside the drift checklist" — duplicate drift note for correctness/F-6.
- conventions/F-2 (P3) "Ticket source remains unavailable" — duplicate environmental note for correctness/F-4.
- conventions/F-3 (P3) "Review surfaces remain inside the freshness window" — duplicate freshness note for correctness/F-5.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Before-first-heading region has no canonical ledger identity | correctness/F-1; edge-cases/F-1 | correctness; edge-cases | P0; P0 | Act on |
| Retry owner cannot cross the checker process boundary | correctness/F-2 | correctness | P0 | Act on |
| Terminal marker-state rendering is incomplete | correctness/F-3 | correctness | P2 | Act on |
| Ticket service unavailable | correctness/F-4; edge-cases/F-2; conventions/F-2 | correctness; edge-cases; conventions | P3; P3; P3 | Noted |
| Recently changed target surfaces | correctness/F-5; edge-cases/F-4; conventions/F-3 | correctness; edge-cases; conventions | P3; P3; P3 | Noted |
| Review-introduced contracts need operator visibility | correctness/F-6; edge-cases/F-3; conventions/F-1 | correctness; edge-cases; conventions | P3; P3; P3 | Noted |
