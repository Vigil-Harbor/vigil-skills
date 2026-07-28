# Edge-Cases Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Stale forward references to Step 6c from 6a, 6b, and edge cases | CLOSED | Spec v3 lines 86-94: Design § Steps 6a/6b with explicit edit items for lines 129, 168, 169-174 |
| edge-cases | F-2 | Step 6b lacks explicit reply-posting insertion point | CLOSED | Spec v3 line 90: item 2 specifies reply injection after 6b push |
| edge-cases | F-3 | Edge cases section merge strategy unspecified | CLOSED | Spec v3 line 175: merge note before the table |
| edge-cases | F-4 | Reply-before-incremental-review confusing thread sequence | CLOSED | Spec v3: acknowledged as cosmetically confusing but functionally correct in edge cases table line 189 |
| edge-cases | F-5 | Phase 1 short-circuit scope should cover all rounds, not just current | CLOSED | Spec v3 line 134: "across ALL rounds of this run" |
| edge-cases | F-6 | 3-round cap warning still references "resolve threads" | CLOSED | Spec v3 line 92: cap warning updated to "check thread resolution status" |

## Findings

### F-1: Line 176 forward reference to 6c not listed
**Severity:** P1
**Where:** spec.md:86, SKILL.md:176
**Edge case:** 6b no-new-findings exit says "proceed to 6c" — same root issue as correctness F-1
**Suggested fix:** Add 4th edit item for SKILL.md line 176.

### F-2: D6 wording inconsistency — "Skip" vs short-circuit
**Severity:** P3
**Where:** spec.md:55-57
**Suggested fix:** Reword to "Step 6d short-circuits" for consistency.

### F-3: Test plan lacks explicit verification of D6 short-circuit path
**Severity:** P3
**Where:** spec.md:239-243
**Suggested fix:** Test plan § "All non-fix" path already covers this — add explicit mention of short-circuit steps.

## Summary
P0: 0 | P1: 1 | P2: 0 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=1 P2=0 P3=2 P4=0
