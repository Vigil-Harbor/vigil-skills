# Correctness Review — VHS-9 Round 3

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | R2/F-1 | Phase 4 guard undeclared scope | CLOSED | Decision 5 + scope updated |
| correctness | R2/F-2 | Brief AC 1 deviation unacknowledged | CLOSED | Lines 92-93 deviation note |
| correctness | R2/F-3 | VHS-9 not in MCP memory | CLOSED | Informational |
| correctness | R2/F-4 | Code block annotation | CLOSED | Removed |

## Findings

### F-1 (P1): Stage 1 `grep -c "Decision"` always returns > 0 — matches Decisions section header/table
The grep runs against the entire file. Every reconciliation report has a `## Decisions` section. Decisions category is always classified as applicable regardless of Wiki-ready content.
**Suggested fix:** Scope grep to Wiki-ready section using `sed`.

### F-2 (P2): Brief AC 2 prompt format `[skip/edit]` → `[y/N]` deviation unacknowledged

### F-3 (P3): VHS-9 Plane ticket not in MCP memory cache

STATUS: RED P0=0 P1=1 P2=1 P3=1 P4=0
