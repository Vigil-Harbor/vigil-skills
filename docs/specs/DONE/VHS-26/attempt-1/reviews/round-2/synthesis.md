# Synthesis — round 2

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P0) "Terminal red revisions bypass the immutable ground-truth ledger" — sites: 6 — add an immutable, checked terminal ledger addendum for final-red and grill revisions before their result is accepted.
- correctness/F-2 (P0) "The no-Python flow skips the ledger it promises to preserve" — sites: 3 — correct the flow to skip checker step 3 while retaining ledger preparation/finalization.
- edge-cases/F-1 (P0) "Deleted headings have no valid coverage representation" — sites: 5 — add removed-heading tombstones to explicit coverage and validate current versus removed entries appropriately.
- edge-cases/F-2 (P0) "Unavailable-Python flow skips the ledger it must dispatch" — sites: 3 — same composed step-number fix as correctness/F-2.
- edge-cases/F-3 (P1) "Checker-driven spec edits leave expected coverage stale" — sites: 4 — re-derive coverage and rebuild the temp ledger after a checker-driven spec edit.
- conventions/F-1 (P0) "No-Python path skips the required ledger preparation" — sites: 3 — same composed step-number fix as correctness/F-2.

## Consider
(none)

## Noted
- correctness/F-3 (P3) "Ticket not cached" — expected degraded-path environment; the brief remains the local authority.
- correctness/F-4 (P3) "Touched review machinery changed within the freshness window" — implementation must re-read current review machinery and anchors.
- edge-cases/F-4 (P3) "Ticket lookup remains unavailable" — duplicate environmental note for correctness/F-3.
- conventions/F-2 (P3) "Review-driven operational additions need drift-check visibility" — surface stale-temp pruning, size/output caps, subprocess timeouts, and the post-green runtime restriction in the Phase 3 drift check.
- conventions/F-3 (P3) "Ticket cache remains inaccessible" — duplicate environmental note for correctness/F-3.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| No-Python wording skips the required ledger preparation | correctness/F-2; edge-cases/F-2; conventions/F-1 | correctness; edge-cases; conventions | P0; P0; P0 | Act on |
| Terminal patch paths have no author-grounding artifact | correctness/F-1 | correctness | P0 | Act on |
| Deleted/renamed headings cannot be represented in coverage | edge-cases/F-1 | edge-cases | P0 | Act on |
| Checker-driven spec edits leave coverage and ledger stale | edge-cases/F-3 | edge-cases | P1 | Act on |
| Ticket service unavailable | correctness/F-3; edge-cases/F-4; conventions/F-3 | correctness; edge-cases; conventions | P3; P3; P3 | Noted |
| Recently changed target surfaces | correctness/F-4 | correctness | P3 | Noted |
| Review-introduced operational contracts need operator visibility | conventions/F-2 | conventions | P3 | Noted |
