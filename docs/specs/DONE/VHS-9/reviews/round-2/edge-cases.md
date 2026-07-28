# Edge-Cases Review — VHS-9 Round 2

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | R1/F-1 | `<project_slug>` undefined | CLOSED | `--include="state.md"` wildcard |
| edge-cases | R1/F-2 | log.md retirement entry ambiguity | PARTIAL | log.md excluded from coverage model but Phase 4 guard "unchanged" claim contradicts |
| edge-cases | R1/F-3 | grep on non-existent directory | CLOSED | Per-command stdout classification |
| edge-cases | R1/F-4 | Phase 0 notice text | CLOSED | Corrected |
| edge-cases | R1/F-5 | Partial-coverage scoping | CLOSED | Inputs always read clarification |
| edge-cases | R1/F-6 | Comprehension "Always" applicability | CLOSED | Made conditional |
| edge-cases | R1/F-7 | Redundant greps | CLOSED | Intentional |

## Findings

### F-1 (P1): Phase 4 log.md idempotency guard is NOT retirement-specific
Same as correctness R2/F-1. Spec claims "unchanged" but references a guard pattern that doesn't exist in current SKILL.md.

### F-2 (P2): Semicolon-separated greps produce interleaved stdout
No delimiter between commands' outputs. Agent cannot reliably classify per-category.
**Suggested fix:** Add echo delimiters between commands.

### F-3 (P2): Stage 1 Wiki-ready parsing is LLM analysis, contradicting Decision 1
Determining applicability requires reading and interpreting free-form prose.
**Suggested fix:** Use grep-based markers or acknowledge as lightweight read step.

### F-4 (P3): `[y/N]` defaults to No — user must actively opt in to optimization

### F-5 (P3): `--include="state.md"` flag position after path may not be portable

STATUS: RED P0=0 P1=1 P2=2 P3=2 P4=0
