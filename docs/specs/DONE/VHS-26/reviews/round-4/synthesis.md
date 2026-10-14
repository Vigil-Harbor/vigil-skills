# Synthesis — round 4

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
(none)

## Consider
(none)

## Noted
- correctness/F-1 (P2) "The row-named omission boundary narrows brief Decision 7's third trigger, and a new spec whose ground-truth ledger holds only the no-claims line draws no ground-truth finding"
- correctness/F-2 (P2) "Closing `ground-truth ledger missing` is pinned for the correctness agent only, but the spec says every lens can already apply it"
- correctness/F-3 (P2) "Grading order is ambiguous for a dead anchor that appears only in the row"
- correctness/F-4 (P3) "ticket not cached"
- correctness/F-5 (P3) "After a failed first write, a new spec's Phase 1 rows are dropped although the author still holds them; preamble count nit"
- edge-cases/F-1 (P2) "The omission P2 is tagged `Pre-ship recommended`, which makes it a 2g candidate that 2g has no legal way to act on"
- edge-cases/F-2 (P2) "The other lenses have no rule for closing `ground-truth ledger missing`, although the spec says every lens can already apply one"
- edge-cases/F-3 (P3) "\"The row sample opens code anchors, not spec sections\" no longer matches the Sample and Grading bullets"
- edge-cases/F-4 (P3) "Three row and closure states have no grading rule"
- edge-cases/F-5 (P3) "A no-claims line on a newly authored spec passes every check"
- edge-cases/F-6 (P3) "Ticket lookup blocked"
- conventions/F-1 (P2) "The omission finding is tagged `Pre-ship recommended`, which the repo defines as a spec-text fold in 2g"
- conventions/F-2 (P2) "The missing-file disposition carries no anchor a lens without the path can verify (residual of round-3 conventions F-1)"
- conventions/F-3 (P2) "The preamble says Decision 8 \"carries brief Decision 7\" and lists three additions, but Decision 8 now narrows that brief decision"
- conventions/F-4 (P3) "Spec-level additions in this revision, for the human drift check"

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Missing-file disposition not verifiable by a lens without the path (§ Decision 6 step 6, § Correctness reviewer changes) | correctness/F-2, edge-cases/F-2, conventions/F-2 | correctness, edge-cases, conventions | P2, P2, P2 | Noted |
| Omission finding tagged `Pre-ship recommended` (§ Decision 8, § Decision 6) | edge-cases/F-1, conventions/F-1 | edge-cases, conventions | P2, P2 | Noted |
| Decision 8 narrows brief Decision 7 and the preamble does not say so (§ Decisions, § Decision 8) | correctness/F-1, conventions/F-3, conventions/F-4, edge-cases/F-5 | correctness, conventions, edge-cases | P2, P2, P3, P3 | Noted |
