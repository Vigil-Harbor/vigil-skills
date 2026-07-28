# Conventions Review — VHS-9 Round 4

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | R3/F-1 | Stage 1 grep matches outside Wiki-ready | CLOSED | sed-scoped |
| conventions | R3/F-2 | --include flag unprecedented | CLOSED | Acceptable — grep builtin |
| conventions | R3/F-3 | Tool-use notes not in amended structure | CLOSED | Informational |
| conventions | R3/F-4 | Three-category model drift-check | CLOSED | Acknowledged |
| conventions | R3/F-5 | PROJECT resolution unspecified | CLOSED | Added to spec |

## Findings

### F-1 (P3): Tool-use notes section not updated for new commands
Spec's "Amended SKILL.md structure" section doesn't mention updating the Tool-use notes section at the end of SKILL.md to reflect new commands (sed, grep -c). Minor omission — implementer will naturally add them.

### F-2 (P4): Partial-coverage prompt is informational (no user choice)
The partial-coverage branch prints "Deriving proposals for missing categories only." without a y/N prompt. This is intentional (brief doesn't require user confirmation for partial) but differs from the full-coverage branch's interactive prompt.

STATUS: GREEN
