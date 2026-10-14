# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | CLOSED | The round-1 finding required no spec change and explicitly permitted proceeding from the brief; the current review again used that documented degraded path. |
| correctness | F-2 | Recently changed implementation surfaces | CLOSED | The cited symbols still resolve in the live files, and the spec retains explicit implementation-time reinspection and diff checks in § Test plan, lines 150–157. |
| edge-cases | F-1 | Later full passes cannot distinguish new claims from untouched claims | CLOSED | Spec § Decision 4, lines 49–59, adds review-visible `Coverage:` provenance; § Decision 8, lines 100–106, defines its omission check against closure evidence and edits encountered during the reviewer’s ordinary read. |
| edge-cases | F-2 | Post-green polish bypasses author grounding | DEFERRED | Spec § Deferred — follow-up required, lines 189–202, contains well-formed row D-1 with three existing propagation sites. Its stated region, `skills/spec-cycle/SKILL.md` §2g Post-green polish, is absent from the brief’s Scope table, so the out-of-scope routing is valid. |
| edge-cases | F-3 | An empty ledger silently satisfies the only enforcement path | CLOSED | Spec § Decision 8, line 100, makes zero-length and contentless ledgers P0; § Test plan, line 153, includes those cases. |
| conventions | F-1 | Author-pinned enforcement choices need explicit provenance labels | PARTIAL | Decisions 4, 5, and 8 still give rationale for the pinned filename/artifact behavior, sample, severities, and checklist, but do not identify them as author-pinned resolutions of brief § Risks / decisions items 2–5. |

## Findings

### F-1: Author-pinned enforcement choices still lack explicit provenance labels
**Severity:** P3  
**Where:** spec.md:40; spec.md:61; spec.md:89; spec.md:146  
**Convention violated:** Silent-addition audit, category (c): spec-level additions with rationale must remain visible for the human drift-check.  
**Evidence:** Brief § Risks / decisions delegates the ledger filename and incomplete-artifact behavior, spot-check size and severities, and review checklist to the spec author. The spec pins those choices in Decisions 4, 5, and 8 and § Test plan, with rationale, but still does not label them as author-pinned resolutions.  
**Suggested fix:** Label Decisions 4, 5, and 8 and the manual checklist as the author-pinned resolutions of brief § Risks / decisions items 2–5. No design change is required.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
