# Synthesis — round 3

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- edge-cases/F-1 (P1) "A late full upgrade keeps the two-directory delta start" — sites: 5 — valid, in scope (brief Decision 8; spec Scope row `skills/spec-cycle/SKILL.md`). Fold: discard the delta start and recompute the full span before creating a directory.
- edge-cases/F-2 (P1) "A line-only Where is placed in the spec after the revision, so the open section drops out" — sites: 5 — valid, in scope (brief Decision 15; spec Scope row `skills/spec-cycle/SKILL.md`). Fold: resolve a line-only Where in the predecessor copy, then map it by stack pairing.

## Consider
(none)

## Noted
- correctness/F-1 (P2) "A green marker with a non-empty delta has no classified exit" — name the green non-empty exit after the no-op steps
- correctness/F-2 (P2) "The empty-pair Done-when sentence covers only the green no-op" — parenthetical: scenario 2 is the green no-op; scenario 15 is the red full pass
- correctness/F-3 (P3) "ticket not cached" — no spec change; already recorded under § Deferred (P2+)
- edge-cases/F-3 (P2) "Code-drift commands have no deadline, so a hung git never becomes the failure token" — `git --no-pager` and `timeout 30`
- conventions/F-1 (P2) "Ledger sample still teaches the old header while mode requires the word `next`" — sample header becomes `round <N-1> → next`
- conventions/F-2 (P2) "The workflow-reference edit list never states the delta mode" — Skill 1 states the two-pass re-run, the clean no-op, and `--full`
- conventions/F-3 (P3) "Delta pass 2 keeps an out-of-scope recount fold" — Decision 8 records the final-round recount rule

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| A full upgrade after row 11 still starts at candidate+1, and a green non-empty delta has no no-op exit | edge-cases/F-1, correctness/F-1 | edge-cases, correctness | P1, P2 | mixed: edge-cases/F-1 Act on, correctness/F-1 Noted |
| A line-only Where is resolved in the current spec | edge-cases/F-2 | edge-cases | P1 | Act on |
| Done-when empty pair names only the green no-op | correctness/F-2 | correctness | P2 | Noted |
| Code-drift git commands can hang | edge-cases/F-3 | edge-cases | P2 | Noted |
| Ledger sample header is still `→ <N>` | conventions/F-1 | conventions | P2 | Noted |
| Workflow reference does not state delta mode | conventions/F-2 | conventions | P2 | Noted |
| Delta pass 2 recount may not revert | conventions/F-3 | conventions | P3 | Noted |
| Ticket not cached | correctness/F-3 | correctness | P3 | Noted |

adjustment: edge-cases/R2/F-1 — Act on → Act on — recount: 7 sites, fold kept. Round 3 edge-cases/F-1 lands on § Mode and round 3 edge-cases/F-2 lands on § Changed regions. Both sections are already on the round-2 site list. In-scope, fold kept.
adjustment: edge-cases/R1/F-2 — Act on → Act on — recount: 4 sites, fold kept. Round 3 edge-cases/F-2 lands on § Changed regions, already on the site list.
adjustment: edge-cases/R1/F-3 — Act on → Act on — recount: 5 sites, fold kept. Same section, in-scope, fold kept.
adjustment: edge-cases/R1/F-4 — Act on → Act on — recount: 9 sites, fold kept. Round 3 edge-cases/F-1 lands on § No-op and § Mode, both already on the site list.
adjustment: correctness/R1/F-1 — Act on → Act on — recount: 3 sites, fold kept. Round 3 edge-cases/F-1 lands on § Mode, already on the site list.
