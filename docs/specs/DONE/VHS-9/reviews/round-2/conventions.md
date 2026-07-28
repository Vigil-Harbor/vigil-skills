# Conventions Review — VHS-9 Round 2

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | R1/F-1 | Unicode checkmarks/crosses | CLOSED | Now `[found]`/`[missing]` |
| conventions | R1/F-2 | Notice text | CLOSED | Corrected |
| conventions | R1/F-3 | log.md in 2b coverage model | CLOSED | Excluded with rationale |
| conventions | R1/F-4 | `[skip/edit]` prompt | CLOSED | Now `[y/N]` |
| conventions | R1/F-5 | Four-category model beyond brief | CLOSED | Three-category with rationale |
| conventions | R1/F-6 | Wiki-ready heading tolerance | CLOSED | Scoped to exact heading |
| conventions | R1/F-7 | `2>/dev/null` Windows | CLOSED | Consistent with existing |

## Findings

### F-1 (P2): Phase 4 guard change presented as "unchanged"
Same root issue as correctness/edge-cases P1. Narrowing the guard IS a change.

### F-2 (P4): Code block annotation inside user-facing prompt
`[or "n/a" if not applicable]` inside code block.

### F-3 (P3): "Older spec-reconcile version" forward-looking for brand-new skill

### F-4 (P2): Stage 1 Wiki-ready parsing is underspecified / contradicts Decision 1

### F-5 (P3): Three-category conditional applicability is a spec-level addition (c)

STATUS: GREEN
