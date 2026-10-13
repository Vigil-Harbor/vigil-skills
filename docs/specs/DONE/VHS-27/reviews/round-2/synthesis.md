# Synthesis — round 2

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- edge-cases/F-1 (P1) "A renamed cited file never becomes a changed path, so the no-op sticks" — sites: 7 — valid, in scope (brief Decision 5 and the spec-cycle skill row). Fold the snapshot SHA, `--no-renames`, `core.quotePath=false`, and a non-path line as a code-drift failure.

## Consider
(none)

## Noted
- correctness/F-1 (P2) "Workflow reference still describes one round counter outside the named edit sites" — name the remaining single-counter paragraphs in § Docs
- correctness/F-2 (P3) "Ticket not cached" — no spec change; already recorded under § Deferred (P2+)
- edge-cases/F-2 (P2) "Two headings with the same line can hide an edit" — pair by ancestor stack, in order
- edge-cases/F-3 (P2) "A red marker whose P0/P1 headings do not parse can be replaced with green" — empty delta must not write green over a red marker
- conventions/F-1 (P2) "Grill paths in `### 2f-i` are not an edit site" — name that heading in § Stop screens
- conventions/F-2 (P2) "Three workflow-reference sentences still treat `round_cap` as the cumulative round" — same root as correctness/F-1
- conventions/F-3 (P2) "New git commands are not added to `## Tool-use notes`" — name that heading in § Docs
- conventions/F-4 (P3) "Changed-region headings do not reuse the skill's heading boundary" — use `^#{1,6}\s` per line

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Rename and quoted path dropped from code drift | edge-cases/F-1 | edge-cases | P1 | Act on |
| Workflow reference still uses one round counter | correctness/F-1, conventions/F-2 | correctness, conventions | P2, P2 | Noted |
| Grill directory not named at `### 2f-i` | conventions/F-1 | conventions | P2 | Noted |
| Code-drift git commands absent from tool-use notes | conventions/F-3 | conventions | P2 | Noted |
| Heading grammar differs from the skill | conventions/F-4 | conventions | P3 | Noted |
| Duplicate heading lines hide an edit | edge-cases/F-2 | edge-cases | P2 | Noted |
| Empty delta can replace a red marker with green | edge-cases/F-3 | edge-cases | P2 | Noted |
| Ticket not cached | correctness/F-2 | correctness | P3 | Noted |

adjustment: edge-cases/R1/F-2 — Act on → Act on — recount: 4 sites, fold kept. Round 2's P1 lands on § Changed regions, which was already on the round-1 site list.
adjustment: edge-cases/R1/F-3 — Act on → Act on — recount: 5 sites, fold kept. Same section, in-scope, fold kept.
adjustment: edge-cases/R1/F-4 — Act on → Act on — recount: 9 sites, fold kept. Same section, in-scope, fold kept.
