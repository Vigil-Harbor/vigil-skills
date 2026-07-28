# Conventions Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | 6b reply-posting location implicit rather than explicit | CLOSED | Spec v3 line 90: item 2 explicitly describes reply injection after 6b push |
| conventions | F-2 | Scope "NOT changed" labeling nit | CLOSED | Spec v3 line 14: reworded to "Preserved (NOT changed)" with clarifying sub-bullets |

## Findings

### F-1: Edge cases table "Current behavior" column retains prose about `@coderabbitai resolve`
**Severity:** P3
**Where:** spec.md:177-191
**Suggested fix:** Acceptable — the "Current behavior" column documenting the old behavior is intentional for the diff context. No action needed.

### F-2: Done-when numbering has "9" and "9b" — not sequential
**Severity:** P4
**Where:** spec.md:269
**Suggested fix:** Renumber to sequential 9, 10, 11... This is cosmetic only.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 1

STATUS: GREEN
