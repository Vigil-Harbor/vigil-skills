# Synthesis — round 1

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P0) "Reader state `changed` never selects a candidate round" — sites: 3 — § Decisions; § Mode; § Scenarios
- correctness/F-2 (P1) "Green-round `spec.copy.md` is taken before post-green polish" — sites: 4 — § Decisions; § Artifacts; § Two counters; § Scenarios
- correctness/F-3 (P1) "Output-contract closure line stays on the round-1 rule" — sites: 1 — § Delta contract
- edge-cases/F-1 (P0) "Ledger coverage is a substring test, so a dropped shorter id is invisible" — sites: 2 — § Delta contract; § Scenarios
- edge-cases/F-2 (P1) "House-style `path:line` citations never count as code drift, so scenario 10 no-ops" — sites: 2 — § Changed regions; § Scenarios
- edge-cases/F-3 (P1) "Any edit marks every ancestor section changed, so a delta pass may explore the whole spec" — sites: 2 — § Changed regions; § Delta contract
- edge-cases/F-4 (P1) "A git error suppresses the no-op, then an empty delta may go green and replace the baseline" — sites: 5 — § Decisions; § Mode; § No-op; § Two counters; § Scenarios

## Consider
(none)

## Noted
- conventions/F-1 (P2) "Output-contract closure line is not an edit site" — same root as correctness/F-3
- conventions/F-2 (P2) "Correctness anchor replacement leaves the old P1 rule in place"
- conventions/F-3 (P2) "Decision 7 omits the Follow-up filter § Mode applies"
- conventions/F-4 (P2) "Single-counter write-points and closure prose are not named as edit sites"
- conventions/F-5 (P3) "Invocation syntax is specified once and copied in three places"
- conventions/F-6 (P3) "Mode row 9 is a spec-level addition to the brief's mode list"
- conventions/F-7 (P3) "§ 2b's sample disposition still cites a skill line"
- edge-cases/F-5 (P2) "A review marker whose round is not a positive integer falls through to delta"
- edge-cases/F-6 (P2) "baseline.commit and ledger.md treat a Windows newline as a corrupt artifact"
- edge-cases/F-7 (P2) "The no-op can report green for a red marker when reports are missing or headings do not parse"
- edge-cases/F-8 (P2) "Only the immediate next round directory is reserved, so a later pass can overwrite an existing round"
- correctness/F-4 (P3) "Ticket not cached"

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Marker fields, not reader state `changed`, select the candidate round | correctness/F-1 | correctness | P0 | Act on |
| Green-round baseline must be the post-polish spec | correctness/F-2 | correctness | P1 | Act on |
| Closure section follows the manifest, not `round_number ≥ 2` | correctness/F-3, conventions/F-1 | correctness, conventions | P1, P2 | mixed: correctness/F-3 Act on, conventions/F-1 Noted |
| Ledger id match needs a token boundary | edge-cases/F-1 | edge-cases | P0 | Act on |
| Path citations must strip a trailing line locator | edge-cases/F-2 | edge-cases | P1 | Act on |
| Changed sections are exclusive bodies, not ancestor spans | edge-cases/F-3 | edge-cases | P1 | Act on |
| Code-drift failure must not no-op or go green on an empty delta | edge-cases/F-4 | edge-cases | P1 | Act on |
| Anchor rule must replace every stale-anchor P1 sentence | conventions/F-2 | conventions | P2 | Noted |
| Brief compare and Decision 7 use one filter | conventions/F-3 | conventions | P2 | Noted |
| Write points, failure mode, and reference prose name the two counters | conventions/F-4 | conventions | P2 | Noted |
| Both skill copies of the usage line are edit sites | conventions/F-5 | conventions | P3 | Noted |
| Occupied-directory row is carried on Decision 14 | conventions/F-6 | conventions | P3 | Noted |
| § 2b sample must not cite a skill line | conventions/F-7 | conventions | P3 | Noted |
| Non-integer `round` is full, not delta | edge-cases/F-5 | edge-cases | P2 | Noted |
| Commit and ledger reads accept CRLF | edge-cases/F-6 | edge-cases | P2 | Noted |
| A red marker and a missing report are not a no-op | edge-cases/F-7 | edge-cases | P2 | Noted |
| The whole round span must be free | edge-cases/F-8 | edge-cases | P2 | Noted |
| Ticket mirror was not read | correctness/F-4 | correctness | P3 | Noted |
