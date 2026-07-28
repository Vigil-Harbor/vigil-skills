# Conventions Review -- round 1

## Closure of round 0 findings
N/A -- round 1.

## Findings

### F-1: Scope omits spec-reconcile and spec-retire
**Severity:** P1
**Where:** spec.md:9-17
**Convention violated:** Brief Done-when #1 intent (host-agnostic tool references across all skills). VHS-8/VHS-9 added these files after the brief was written.
**Evidence:** spec-reconcile has 3 Plane MCP + 2 memory_search + 1 states.json path. spec-retire has 2 Plane MCP + 1 states.json path.
**Suggested fix:** Add both to scope with specific replacement counts.

### F-2: Test plan grep audit misses `mcp__claude_ai_Plane__` pattern
**Severity:** P2
**Where:** spec.md:117-118
**Convention violated:** Internal consistency
**Evidence:** Grep checks `mcp__plane__` and `mcp__claude_ai_Vigil_Harbor_MCP_Server__` but not `mcp__claude_ai_Plane__` (used by spec-reconcile/spec-retire).
**Suggested fix:** Add third grep pattern or use broad `mcp__(plane|claude_ai_)` regex.

### F-3: Line number references off-by-one for ship-spec
**Severity:** P4
**Where:** spec.md:65, 67
**Convention violated:** Internal consistency
**Evidence:** "Line 38" is actually line 39; "Line 258" is actually line 256.
**Suggested fix:** Correct or replace with step identifiers.

### F-4: Scope table incomplete for ship-spec
**Severity:** P2
**Where:** spec.md:14
**Convention violated:** Scope/design agreement
**Evidence:** Scope table says ship-spec changes are MCP tool names + states.json path, but Design section 4 adds the N/A escape hatch to ship-spec.
**Suggested fix:** Update scope table row to include N/A escape hatch.

### F-5: Silent spec additions beyond the brief
**Severity:** P2
**Where:** spec.md:88-108
**Convention violated:** Brief authorization / silent addition check
**Evidence:** "Proceed directly to Phase 4 (commit)" locks skip-target to a phase number; `## Deferred (P2+)` section name is new commitment; rename workflow recommendation is new.
**Suggested fix:** Use phase name instead of number; flag others for human drift-check.

### F-6: Capability-description pattern and `__` namespacing convention
**Severity:** P3
**Where:** spec.md:29-35
**Convention violated:** Wiki decision on `__` namespacing
**Evidence:** Example names strip namespace entirely (`list_projects` instead of `mcp__plane__list_projects`).
**Suggested fix:** Keep full Claude Code tool name as example for grepability.

## Summary
P0: 0 | P1: 1 | P2: 3 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=3 P3=2 P4=1