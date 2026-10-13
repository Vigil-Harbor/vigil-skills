# Synthesis — round 3

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P1) "The replacement resolver no longer places `spec.md:<line>` locators, so the reviewers' canonical `Where` form falls to every-heading" — sites: 4 — in-scope (brief Scope row `### Changed regions`; brief Decision 7 "every cited line"); fold at Decision 8, § Open-finding resolver, the `:492` replacement, and § Scenarios.

## Consider
(none)

## Noted
- edge-cases/F-1 (P2, pre-ship recommended) colon-form locator — same root as correctness/F-1.
- edge-cases/F-2 (P3) empty heading phrase matches arm 2.
- edge-cases/F-3 (P3) raw-line validation precedes the archive drop.
- edge-cases/F-4 (P3) ticket grounding unavailable.
- correctness/F-2 (P3) ticket not cached.
- correctness/F-3 (P4) "direct child" wording.
- conventions/F-1 (P3) `.attempt-<n>/` layout undefined in tracked files.
- conventions/F-2 (P3) ticket grounding unavailable.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| `:492` replacement — colon-form line locator unrecognised | correctness/F-1, edge-cases/F-1 | correctness, edge-cases | P1, P2 | mixed: correctness/F-1 Act on; edge-cases/F-1 Noted |
| ticket grounding unavailable (memory server 502) | correctness/F-2, edge-cases/F-4, conventions/F-2 | all three | P3 | Noted |
