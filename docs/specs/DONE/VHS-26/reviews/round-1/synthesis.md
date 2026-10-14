# Synthesis — round 1

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- edge-cases/F-1 (P1) "Later full passes cannot distinguish new claims from untouched claims" — sites: 4 — define human-visible coverage provenance without coupling to changed-regions computation.
- edge-cases/F-3 (P1) "An empty ledger silently satisfies the only enforcement path" — sites: 3 — classify an empty/contentless evidence file as missing and test that case.

## Consider
- edge-cases/F-2 (P1) "Post-green polish bypasses author grounding" — post-green polish is outside the brief's scoped Phase 1/§2e/round-artifact surfaces; record as a follow-up.

## Noted
- correctness/F-1 (P3) "ticket not cached" — degraded-path context; no spec edit required.
- correctness/F-2 (P3) "Recently changed implementation surfaces" — implementation-time drift reminder already represented by fresh reads and the delta-block check.
- conventions/F-1 (P3) "Author-pinned enforcement choices need explicit provenance labels" — optional clarity; the Decisions already supply rationale.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Later-round omission provenance | edge-cases/F-1 | edge-cases | P1 | Act on |
| Post-green unreviewed edits | edge-cases/F-2 | edge-cases | P1 | Consider |
| Empty evidence artifact | edge-cases/F-3 | edge-cases | P1 | Act on |
| Degraded ticket lookup | correctness/F-1 | correctness | P3 | Noted |
| Recent contract churn | correctness/F-2 | correctness | P3 | Noted |
| Author-pinned decision labels | conventions/F-1 | conventions | P3 | Noted |
