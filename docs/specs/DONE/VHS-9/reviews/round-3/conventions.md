# Conventions Review — VHS-9 Round 3

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | R2/F-1 | Phase 4 guard "unchanged" | CLOSED | Decision 5 |
| conventions | R2/F-2 | Code block annotation | CLOSED | Removed |
| conventions | R2/F-3 | "Older version" wording | CLOSED | Reworded |
| conventions | R2/F-4 | Stage 1 contradicts Decision 1 | PARTIAL | grep-c approach fixes contract but patterns over-match |
| conventions | R2/F-5 | Three-category addition | CLOSED | Acknowledged |

## Findings

### F-1 (P2): Stage 1 grep patterns match outside Wiki-ready section
Same root as correctness R3/F-1. The grep runs file-wide; "Decision" appears in Decisions table.
**Suggested fix:** Scope grep to Wiki-ready section via `sed`.

### F-2 (P3): `--include` flag unprecedented in skills

### F-3 (P3): Tool-use notes section not mentioned in amended structure

### F-4 (P3): Three-category model is spec-level addition (c) — surfaced for drift-check

### F-5 (P2): `<PROJECT>` resolution unspecified for Phase 4 guard

STATUS: GREEN
