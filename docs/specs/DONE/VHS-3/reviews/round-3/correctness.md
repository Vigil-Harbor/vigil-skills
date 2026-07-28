# Correctness Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Scope table lists 6a/6b as "preserved" but design requires modifications | CLOSED | Spec v3 line 11: scope table lists "Step 6a (forward-reference update), Step 6b (forward-reference update + reply injection)" |
| correctness | F-2 | Done-when #12 references "test output file" not defined | CLOSED | Spec v3 line 272: output path specified as `docs/specs/TODO/VHS-3.test-output.txt` |
| correctness | F-3 | Line reference "125-126" slightly imprecise | CLOSED | Spec v3 line 98: reference corrected to "line 125" |

## Findings

### F-1: Line 176 forward reference to 6c not covered
**Severity:** P1
**Where:** spec.md:86, SKILL.md:176
**Issue:** Design § Steps 6a/6b lists three edits (lines 129, 168, 169-174) but SKILL.md line 176 also says "proceed to 6c" — the no-new-findings exit path in 6b.
**Suggested fix:** Add a 4th item to the edit list for line 176.

### F-2: D6 wording uses "Skip" which implies the step doesn't execute
**Severity:** P3
**Where:** spec.md:55-57
**Suggested fix:** Reword "Skip Step 6d" → "Step 6d short-circuits" for consistency with the rest of the spec's language.

## Summary
P0: 0 | P1: 1 | P2: 0 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=0 P3=1 P4=0
