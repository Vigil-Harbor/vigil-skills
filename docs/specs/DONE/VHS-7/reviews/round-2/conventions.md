# Conventions Review -- round 2

## Closure of round 1 findings

- **R1/F-1 (P1) — Scope omits spec-reconcile and spec-retire:** CLOSED. Both files added to scope table with specific replacement counts. Decision 4 documents rationale for expanding beyond original brief scope.
- **R1/F-2 (P2) — Test plan grep audit misses `mcp__claude_ai_Plane__` pattern:** CLOSED. Regex now covers all three prefix patterns.
- **R1/F-3 (P4) — Line number references off-by-one for ship-spec:** CLOSED. Corrected with step identifiers added.
- **R1/F-4 (P2) — Scope table incomplete for ship-spec:** CLOSED. Scope table updated to include N/A escape hatch.
- **R1/F-5 (P2) — Silent spec additions beyond the brief:** CLOSED. Decision 4 explicitly documents the scope expansion rationale.
- **R1/F-6 (P3) — Capability-description pattern and `__` namespacing convention:** CLOSED. Full Claude Code tool names now kept as examples.

## Findings

### F-1: Scope table replacement counts use "tool names" ambiguously
**Severity:** P2
**Where:** spec.md:13-16
**Convention violated:** Internal consistency between scope table and design section
**Evidence:** Scope table uses "N hardcoded MCP tool names" which could mean distinct tool names or total occurrences. spec-reconcile says "4" but design lists 6 occurrences. spec-retire says "3" but design lists 4 occurrences. The distinction matters for implementer verification.
**Suggested fix:** Use "N occurrences" consistently, or clarify what the count means.

### F-2: Decision 4 rationale is well-structured
**Severity:** P3
**Where:** spec.md:48-49
**Convention violated:** None — this is a positive observation
**Evidence:** Decision 4 clearly documents why scope expanded beyond the brief, citing VHS-8/VHS-9 as the source. Good precedent for future specs.
**Suggested fix:** None needed.

### F-3: Test plan step 4 spot-check is manual
**Severity:** P3
**Where:** spec.md:152
**Convention violated:** Test plan completeness
**Evidence:** Step 4 says "Read each changed file end-to-end" which is a manual review step, not automatable. Acceptable for a doc-only change.
**Suggested fix:** None needed; manual review is appropriate for documentation changes.

### F-4: Brief's "Done when" #6 maps to test command
**Severity:** P3
**Where:** spec.md:168
**Convention violated:** Done-when / test-plan alignment
**Evidence:** Brief done-when #6 says "`sync.py install` still works after all edits." The test command covers this. Good alignment.
**Suggested fix:** None needed.

### F-5: `## Deferred (P2+)` section name introduced by spec-cycle
**Severity:** P4
**Where:** spec.md (not yet present — will appear if P2+ findings are deferred)
**Convention violated:** None currently — noting for consistency
**Evidence:** The spec-cycle skill references `## Deferred (P2+)` as a section name. This spec doesn't currently have one since no P2s are being deferred.
**Suggested fix:** None needed.

### F-6: Windows path uses backslash in parenthetical
**Severity:** P4
**Where:** spec.md:109
**Convention violated:** Markdown rendering
**Evidence:** `%USERPROFILE%\.claude\` — the backslashes render fine in raw markdown but could be escaped in some renderers. Minor.
**Suggested fix:** None needed; raw markdown is the consumption format.

### F-7: Spec doesn't mention CLAUDE.md conventions section
**Severity:** P4
**Where:** spec.md:22-23
**Convention violated:** Wiki/CLAUDE.md sync
**Evidence:** The CLAUDE.md "External dependencies" section mentions MCP tools by category but not by name. No update needed there since it uses capability descriptions already.
**Suggested fix:** None needed.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 3

STATUS: GREEN P0=0 P1=0 P2=1 P3=3 P4=3
