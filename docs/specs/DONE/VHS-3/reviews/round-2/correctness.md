# Correctness Review -- round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Multi-round SHA capture gap | CLOSED | Spec v2 lines 17, 82, 92: replies post inside loop after each push |
| correctness | F-2 | Fallback contradicts user intent | CLOSED | Spec v2 D3 (line 33): automated fallback removed, report-only with user-quote rationale |
| correctness | F-3 | Stale CHANGES_REQUESTED edge case | CLOSED | Spec v2 edge cases table line 166 |
| correctness | F-4 | Phase 2 scope addition | CLOSED | Spec v2 D8 (line 69): explicit brief departure |
| correctness | F-5 | All-skips divergence from Risk 4 | CLOSED | Spec v2 D6 (line 52): explicit brief departure |
| correctness | F-6 | "from this round" ambiguous | CLOSED | Spec v2 lines 92-93: placement clarified |
| correctness | F-7 | Comment-ID stability not addressed | CLOSED | Spec v2 line 104: each round uses own comment IDs |

## Findings

### F-1: Scope table lists 6a/6b as "preserved" but design requires modifications
**Severity:** P2
**Where:** spec.md:14-17
**Suggested fix:** Move 6a/6b forward-reference updates into scope table.

### F-2: Done-when #12 references "test output file" not defined
**Severity:** P3
**Where:** spec.md:257
**Suggested fix:** Specify output location.

### F-3: Line reference "125-126" slightly imprecise
**Severity:** P4
**Where:** spec.md:86
**Suggested fix:** Change to "line 125" or drop line reference.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 1

STATUS: GREEN
