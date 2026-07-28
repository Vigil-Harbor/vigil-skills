# Correctness Review -- round 2

## Closure of round 1 findings

- **R1/F-1 (P0) — Test plan grep scope mismatch:** CLOSED. Spec now narrows grep to specific in-scope file paths (lines 139-151) and all three MCP prefix patterns are covered by the regex.
- **R1/F-2 (P1) — Stale line anchor ship-spec line 38→39:** CLOSED. Spec line 65 now says "line 39" with step identifier.
- **R1/F-3 (P1) — Stale line anchor ship-spec line 258→256:** CLOSED. Spec line 73 now says "line 256" with section identifier.
- **R1/F-4 (P2) — N/A escape hatch placement:** CLOSED. Spec Design section 4 now places the escape hatch between step 4.1 and 4.2 with exact parsing rule.
- **R1/F-5 (P3) — Ticket not cached in MCP memory:** CLOSED. No spec change needed (grounding note).
- **R1/F-6 (P3) — spec-reconcile and spec-retire scope:** CLOSED. Both added to scope table and Design section with specific replacement counts. Decision 4 documents rationale.

## Findings

### F-1: spec-reconcile scope table count inconsistency
**Severity:** P2
**Where:** spec.md:15
**Claim:** Scope table says "Replace 4 hardcoded MCP tool names (2 Plane, 2 memory)"
**Why this is worth noting:** Design section 1 lists 6 occurrences for spec-reconcile: line 15 has 2 Plane tools on one long line, line 25 has 1 memory_search, line 103 has 1 memory_search, line 104 has 2 Plane tools. That's 4 Plane + 2 memory = 6 occurrences. The scope table says 4. However, the "(2 Plane, 2 memory)" breakdown in the scope table accounts for 2 distinct tool names (list_states, retrieve_work_item_by_identifier) and 2 memory_search references — it's counting distinct tools, not occurrences. The design section lists all 6 occurrences correctly.
**Suggested fix:** Clarify scope table to say "6 occurrences" or note it counts distinct tool names.

### F-2: Capability description wording not verified against actual file content
**Severity:** P3
**Where:** spec.md:56-60
**Claim:** Template pattern uses "call the <server-name> server's <capability> capability"
**Why this is worth noting:** The actual replacement text hasn't been tested for readability in context. Minor — the template is clear enough.
**Suggested fix:** None needed; implementer will adapt phrasing to context.

### F-3: Test command uses `&&` which is Unix-specific
**Severity:** P4
**Where:** spec.md:157-158
**Claim:** `python sync.py install --dry-run && python sync.py install`
**Why this is worth noting:** On Windows PowerShell, `&&` is not available in PS 5.1. However, sync.py is run from the repo root where bash is typically available, and the test command is meant to be run in the tool's shell environment.
**Suggested fix:** Minor — could use `; if ($?) {` pattern for PS 5.1 but not critical since bash is available.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 1

STATUS: GREEN P0=0 P1=0 P2=1 P3=1 P4=1
