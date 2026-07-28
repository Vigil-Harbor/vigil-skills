# Correctness Review — VHS-9 Round 2

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | R1/F-1 | Phase 0 notice text factually incorrect | CLOSED | Decision 4 + line 55 corrected |
| correctness | R1/F-2 | `<project_slug>` undefined | CLOSED | `--include="state.md"` wildcard |
| correctness | R1/F-3 | Contradictory Phase 2c language | CLOSED | Lines 116, 140 aligned |
| correctness | R1/F-4 | VHS-9 not in MCP memory | CLOSED | Informational |
| correctness | R1/F-5 | Redundant greps | CLOSED | Intentional, documented |

## Findings

### F-1 (P1): Phase 4 idempotency guard change is undeclared scope
The spec references `grep -F "retire | <PROJECT> — <TICKET-ID>"` but claims Phase 4 is "unchanged." Current SKILL.md line 138 uses `grep -F "<TICKET-ID>"`. This is a behavioral change.
**Suggested fix:** Declare in scope, add Decision 5, update integration section.

### F-2 (P2): Brief AC 1 lists four categories; spec reduces to three without explicit mapping
Decision 2 provides rationale but no explicit note acknowledging the deviation from brief AC 1.

### F-3 (P3): VHS-9 Plane ticket not in MCP memory cache

### F-4 (P3): Code block annotation `[or "n/a" if not applicable]` would render to user

STATUS: RED P0=0 P1=1 P2=1 P3=2 P4=0
