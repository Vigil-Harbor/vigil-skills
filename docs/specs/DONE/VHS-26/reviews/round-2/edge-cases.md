# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | CLOSED | The declared offline environment requires the documented brief-only degraded path; no spec defect remains. |
| correctness | F-2 | Recently changed implementation surfaces | CLOSED | Fresh reads confirm every cited surface still resolves: `skills/spec-cycle/SKILL.md:384`, `:444`, `:511`, `:706`; `agents/spec-reviewer-correctness.md:90`; `agents/spec-reviewer-conventions.md:103`; `docs/spec-workflow-reference.md:43`; `README.md:10`. |
| edge-cases | F-1 | Later full passes cannot distinguish new claims from untouched claims | CLOSED | spec lines 49-59 add the human-readable `Coverage:` boundary; lines 101-106 define its cross-check against closure evidence without backfilling untouched sections; lines 134-136 carry that rule into the correctness-agent design. |
| edge-cases | F-2 | Post-green polish bypasses author grounding | DEFERRED | D-1 at spec lines 193-202 is well-formed, names three existing propagation sites, and carries the explicit `out-of-scope` token; the ceiling therefore permits the undischarged P1 row. |
| edge-cases | F-3 | An empty ledger silently satisfies the only enforcement path | CLOSED | spec lines 99-100 classify zero-length and contentless ledgers as the same P0 as a missing ledger; the manual checklist covers the case at line 153. |
| conventions | F-1 | Author-pinned enforcement choices need explicit provenance labels | PARTIAL | Decisions 4, 5, and 8 remain explicit and reasoned, but none is labeled as an author-pinned resolution of the brief’s corresponding risk item. |

## Findings

### F-1: Author-pinned enforcement choices remain implicit
**Severity:** P3
**Where:** spec.md:40-71; spec.md:89-106  
**Edge case:** During the Phase 3 drift-check, the operator must distinguish choices carried by the brief from choices the spec author pinned under the brief’s `## Risks / decisions`.  
**What happens:** The design remains understandable and functional, but the provenance of the filename/failure semantics and correctness-enforcement choices is not immediately visible as author-pinned.  
**Why the spec misses it:** Decisions 4, 5, and 8 explain their rationale but do not label themselves as resolutions of brief risk items 2 and 3.  
**Suggested fix:** Add a short “author-pinned from brief risk item” note to Decisions 4, 5, and 8 without changing their behavior.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
