# Synthesis — round 3

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P0) "Delta pass 1 after a red halt carries a closure manifest, so the omission boundary is not empty on a re-run" — sites: 6 — in-scope (brief Scope rows for the skill and the correctness agent); the boundary must not depend on the closure manifest
- edge-cases/F-1 (P0) "Delta pass 1 after a red halt has a closure manifest, so the omission boundary fires where the spec says it must not" — sites: 6 — same root as correctness/F-1
- correctness/F-2 (P1) "An evidence-only ground-truth fix puts a section in the omission boundary with rows for only the named claims" — sites: 5 — in-scope; the carried-rows disposition is the cause
- edge-cases/F-2 (P1) "An evidence-only fix carries rows for the named claims only, but its disposition puts the whole section in the omission boundary — the loop cannot close" — sites: 5 — same root as correctness/F-2

## Consider
(none)

## Noted
- correctness/F-3 (P3) "Decisions preamble maps to brief decisions but still does not mark the author-pinned choices"
- correctness/F-4 (P3) "ticket not cached"
- correctness/F-5 (P4) "Done-when item 6 and § Test command quote the unittest pattern differently"
- edge-cases/F-3 (P2) "A ground-truth finding on the final allowed pass gets a `fixed:` disposition for rows that are never written"
- edge-cases/F-4 (P2) "\"Section\" is not defined the same way for the author's rows and the reviewer's boundary"
- edge-cases/F-5 (P2) "Closure rule cannot be met when the fix removes or rewrites the named claim"
- edge-cases/F-6 (P3) "Held rows have no durable home between authoring and dispatch"
- edge-cases/F-7 (P3) "\"Check at most five rows\" conflicts with \"also check every row a predecessor finding named\""
- edge-cases/F-8 (P3) "Ticket lookup blocked"
- conventions/F-1 (P2) "New `fixed: ground-truth rows carried` disposition is not reconciled with the existing manifest vocabulary, the recount trigger, or the other lenses' closure check"
- conventions/F-2 (P2) "`Anchor: none` relaxes brief Decision 1 but is presented as carried from the brief"
- conventions/F-3 (P2) "Decision 3 uses the bare word \"ledger\" that Decision 4 forbids in the same revision"
- conventions/F-4 (P3) "Spec-level additions in this revision, for the human drift check"

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Omission boundary read from the closure manifest (§ Decision 8, § Decision 4, § Test plan) | correctness/F-1, edge-cases/F-1 | correctness, edge-cases | P0, P0 | Act on |
| Carried-rows disposition for an evidence-only fix (§ Decision 6 step 6, § Decision 8) | correctness/F-2, edge-cases/F-2, edge-cases/F-3, edge-cases/F-5, edge-cases/F-7, conventions/F-1 | correctness, edge-cases, conventions | P1, P1, P2, P2, P3, P2 | mixed: correctness/F-2 Act on; edge-cases/F-2 Act on; edge-cases/F-3 Noted; edge-cases/F-5 Noted; edge-cases/F-7 Noted; conventions/F-1 Noted |
| Author-pinned choices and additions not labelled (§ Decisions) | correctness/F-3, conventions/F-2, conventions/F-4 | correctness, conventions | P3, P2, P3 | Noted |
