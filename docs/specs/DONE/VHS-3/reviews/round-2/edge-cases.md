# Edge-Cases Review -- round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Multi-round SHA mapping | CLOSED | Spec v2 lines 82, 92: replies post after each push |
| edge-cases | F-2 | Thread≠finding counting unsound | CLOSED | Spec v2 lines 114-120: polling purely observational, no counting condition |
| edge-cases | F-3 | already-fixed unaccounted | CLOSED | Spec v2 D4 (line 39): explicitly grouped with skip/duplicate |
| edge-cases | F-4 | Fallback contradicts user intent | CLOSED | Spec v2 D3 (line 31): automated fallback removed |
| edge-cases | F-5 | Stale CHANGES_REQUESTED dropped | CLOSED | Spec v2 edge cases table line 166 |
| edge-cases | F-6 | Comment-ID stability | CLOSED | Spec v2 line 104: each round uses own comment IDs |
| edge-cases | F-7 | Nitpick body findings no comment ID | CLOSED | Spec v2 line 106: guard for body-level findings |
| edge-cases | F-8 | Fallback-failure report gap | CLOSED | Moot — fallback removed |
| edge-cases | F-9 | Step 6 header prose | CLOSED | Spec v2 lines 84-88: Step 6 header in scope |
| edge-cases | F-10 | Rate limiting | CLOSED | Spec v2 line 108: 429 retry-once |
| edge-cases | F-11 | Multi-round test coverage | CLOSED | Spec v2 lines 220-223: multi-round test scenario added |

## Findings

### F-1: Stale forward references to Step 6c from 6a, 6b, and edge cases
**Severity:** P1
**Where:** spec.md:17, SKILL.md lines 129, 169, 176, 252
**Edge case:** 6c folded inline but "skip to 6c" / "proceed to 6c" references in 6a/6b remain
**Suggested fix:** Add 6a/6b to scope table; add design subsection for forward-reference updates.

### F-2: Step 6b lacks explicit reply-posting insertion point
**Severity:** P2
**Where:** spec.md:92
**Suggested fix:** Add "Step 6b: Reply injection point" subsection to Design.

### F-3: Edge cases section merge strategy unspecified
**Severity:** P2
**Where:** spec.md:161-176
**Suggested fix:** Add merge note before the table.

### F-4: Reply-before-incremental-review confusing thread sequence
**Severity:** P3
**Where:** spec.md:82, 175
**Suggested fix:** Add cosmetic-only note to edge case entry.

### F-5: Phase 1 short-circuit scope should cover all rounds, not just current
**Severity:** P3
**Where:** spec.md:122
**Suggested fix:** Clarify short-circuit applies only when no fix-findings across ALL rounds.

### F-6: 3-round cap warning still references "resolve threads"
**Severity:** P3
**Where:** SKILL.md line 173
**Suggested fix:** Update cap warning text in 6b design note.

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 3 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=3 P4=0
