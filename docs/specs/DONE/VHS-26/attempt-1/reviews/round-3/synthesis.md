# Synthesis — round 3

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P0) "Terminal addenda cannot always be ‘checked’" — sites: 3 — qualify terminal validation consistently for the explicit unavailable-Python exception and pin that path.
- edge-cases/F-1 (P0) "Duplicate-heading deletion still has no valid tombstone" — sites: 5 — replace leaf-only references with canonical full-stack-plus-occurrence identities for coverage and spec locations.
- edge-cases/F-2 (P2, Pre-ship recommended) "Terminal gate failures emit a false dispatch message" — sites: 3 — define terminal-specific repeated-failure and timeout messages that report preserved reviews and rollback state.

## Consider
(none)

## Noted
- correctness/F-2 (P3) "Ticket grounding remains unavailable" — expected degraded-path environment; the brief remains the local authority.
- correctness/F-3 (P3) "Touched review surfaces changed within the last seven days" — implementation must re-read current review machinery and anchors.
- correctness/F-4 (P3) "Review-introduced operational contracts remain implicit in the drift check" — group all review-introduced contracts in the Phase 3 checklist.
- edge-cases/F-3 (P3) "Ticket lookup remains unavailable" — duplicate environmental note for correctness/F-2.
- conventions/F-1 (P3) "Review-introduced contracts still need drift-check visibility" — same Phase 3 checklist note as correctness/F-4.
- conventions/F-2 (P3) "Ticket source remains unavailable" — duplicate environmental note for correctness/F-2.
- conventions/F-3 (P3) "Review surfaces remain inside the freshness window" — duplicate freshness note for correctness/F-3.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Terminal validation wording contradicts the no-Python exception | correctness/F-1 | correctness | P0 | Act on |
| Leaf-only heading references cannot identify duplicate deletion | edge-cases/F-1 | edge-cases | P0 | Act on |
| Pre-dispatch failure messages are false on terminal paths | edge-cases/F-2 | edge-cases | P2 | Act on |
| Ticket service unavailable | correctness/F-2; edge-cases/F-3; conventions/F-2 | correctness; edge-cases; conventions | P3; P3; P3 | Noted |
| Recently changed target surfaces | correctness/F-3; conventions/F-3 | correctness; conventions | P3; P3 | Noted |
| Review-introduced contracts need operator visibility | correctness/F-4; conventions/F-1 | correctness; conventions | P3; P3 | Noted |
