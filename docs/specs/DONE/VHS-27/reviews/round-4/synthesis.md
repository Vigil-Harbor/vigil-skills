# Synthesis — round 4

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P1) "A STATUS-only open set still lets a red marker go green" — sites: 7 — valid, in scope (brief Decision 11; spec Scope row `skills/spec-cycle/SKILL.md`). Fold: a `<lens>/STATUS` line is a full pass, `mode: full (open findings unreadable)`, before the pending write.
- edge-cases/F-1 (P1) "A suffixed `§` phrase suppresses the line and names no heading" — sites: 5 — valid, in scope (brief Decision 15; spec Scope row `skills/spec-cycle/SKILL.md`). Fold: split Where on `;`, match a heading by equality or longest prefix, and use the line when the phrase matches nothing.

## Consider
(none)

## Noted
- correctness/F-2 (P2) "Out of scope still says a delta pass uses the routing rules unchanged" — carve-out: delta pass 2 keeps a recount fold and does not revert, as Decision 8 states
- correctness/F-3 (P2) "Grill row templates still record `round_cap` on a delta halt" — `Deferred in: round <C> (grill)` and `Scope: operator — round-<C> grill`
- correctness/F-4 (P3) "ticket not cached" — no further spec change; round 4 re-filed the existing § Deferred (P2+) note
- edge-cases/F-2 (P2) "An untracked brief is code drift, so the clean no-op never fires" — drop the brief path, the spec path, and paths under that ticket's reviews directory before the citation tests
- edge-cases/F-3 (P3) "ticket not cached" — same note, no further spec change
- conventions/F-1 (P3) "ticket not cached" — same note, no further spec change

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| A STATUS-only open set dispatches delta and can replace a red marker with green | correctness/F-1 | correctness | P1 | Act on |
| A suffixed § phrase matches no heading and drops the line | edge-cases/F-1 | edge-cases | P1 | Act on |
| Out of scope says routing is unchanged on delta pass 2 | correctness/F-2 | correctness | P2 | Noted |
| Grill row templates still record round_cap | correctness/F-3 | correctness | P2 | Noted |
| An untracked brief or spec is code drift, so the no-op never fires | edge-cases/F-2 | edge-cases | P2 | Noted |
| Ticket not cached | correctness/F-4, edge-cases/F-3, conventions/F-1 | correctness, edge-cases, conventions | P3, P3, P3 | Noted |

adjustment: correctness/F-1 — Act on → Act on — recount: 7 sites, fold kept. Where lands on § No-op, § Dispatch, § Delta contract, § Two counters, and § Scenarios, already named on earlier fixed lines. Round equals round_cap, so the recount does not revert. Fold kept.
adjustment: edge-cases/F-1 — Act on → Act on — recount: 5 sites, fold kept. Where lands on § Changed regions, § Decisions, and § Scenarios, already named on earlier fixed lines. Round equals round_cap, so the recount does not revert. Fold kept.
adjustment: edge-cases/R3/F-1 — Act on → Act on — recount: 5 sites, fold kept. Round 4 correctness/F-1 lands on § No-op and § Scenarios. In-scope, round equals round_cap, fold kept.
adjustment: edge-cases/R3/F-2 — Act on → Act on — recount: 5 sites, fold kept. Round 4 correctness/F-1 lands on § Dispatch and round 4 edge-cases/F-1 lands on § Changed regions. In-scope, fold kept.
adjustment: edge-cases/R2/F-1 — Act on → Act on — recount: 7 sites, fold kept. Round 4 correctness/F-1 lands on § Two counters and § Scenarios. In-scope, fold kept.
adjustment: edge-cases/R1/F-2 — Act on → Act on — recount: 4 sites, fold kept. Round 4 edge-cases/F-1 lands on § Changed regions and § Scenarios. In-scope, fold kept.
adjustment: edge-cases/R1/F-3 — Act on → Act on — recount: 5 sites, fold kept. Round 4 correctness/F-1 lands on § Dispatch and § Delta contract. In-scope, fold kept.
adjustment: edge-cases/R1/F-4 — Act on → Act on — recount: 9 sites, fold kept. Round 4 correctness/F-1 lands on § No-op, § Two counters, and § Scenarios. In-scope, fold kept.
adjustment: correctness/R1/F-1 — Act on → Act on — recount: 3 sites, fold kept. Round 4 edge-cases/F-1 lands on § Decisions and both new findings land on § Scenarios. In-scope, fold kept.
