# Correctness Review -- round 1

## Closure of round 0 findings
N/A -- round 1

## Findings

### F-1: Test plan grep for memory_search would not return zero results
**Severity:** P0
**Where:** spec.md:118
**Claim:** "`grep -r "mcp__claude_ai_Vigil_Harbor_MCP_Server__" skills/ agents/` should return zero results."
**Why this is wrong:** `skills/spec-reconcile/SKILL.md` lines 25 and 103 contain `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`. This file is explicitly out of scope for VHS-7 (it does not appear in the "Files to change" table at spec lines 9-17). After all VHS-7 changes are applied, the grep would still return 2 matches from spec-reconcile. The spec's test plan (step 3) is internally inconsistent with its scope.
**Suggested fix:** Narrow the grep to the in-scope files only, or expand scope to include spec-reconcile and spec-retire.

### F-2: Stale line anchor -- ship-spec line 38 vs actual line 39
**Severity:** P1
**Where:** spec.md:64
**Claim:** "Line 38 (`mcp__plane__list_projects`): Replace with capability description for Plane project listing."
**Why this is wrong:** In `skills/ship-spec/SKILL.md`, `mcp__plane__list_projects` appears on line 39, not line 38.
**Suggested fix:** Change "Line 38" to "Line 39" or use step identifiers instead of line numbers.

### F-3: Stale line anchor -- ship-spec line 258 vs actual line 256
**Severity:** P1
**Where:** spec.md:67
**Claim:** "Line 258 (`mcp__plane__*`)"
**Why this is wrong:** In `skills/ship-spec/SKILL.md`, the `mcp__plane__*` wildcard reference appears on line 256, not line 258.
**Suggested fix:** Change "Line 258" to "Line 256" or use section identifiers.

### F-4: N/A escape hatch placement creates ambiguous control flow in ship-spec
**Severity:** P2
**Where:** spec.md:100-102
**Claim:** "Also add a corresponding note in `ship-spec/SKILL.md` Phase 0 step 4, after the 'Fail loud' block"
**Why this is wrong:** Placement after step 4.3 but semantically intercepts step 4.1's "use verbatim" behavior. An LLM reading step 4.1 would see "use verbatim" before encountering the N/A exception.
**Suggested fix:** Place between step 4.1 and step 4.2 instead.

### F-5: Ticket not cached in MCP memory
**Severity:** P3
**Where:** N/A (grounding step)
**Claim:** N/A
**Why this is wrong:** `memory_search` for VHS-7 in `vhs` namespace returned zero results.
**Suggested fix:** No spec change needed.

### F-6: spec-reconcile and spec-retire also have hardcoded MCP tool names
**Severity:** P3
**Where:** spec.md:19-23 (Files to leave alone)
**Claim:** Does not mention spec-reconcile or spec-retire.
**Why this is wrong:** Both files contain hardcoded MCP tool names (`mcp__claude_ai_Plane__*`, `mcp__claude_ai_Vigil_Harbor_MCP_Server__*`).
**Suggested fix:** Add to scope or explicitly list in "Files to leave alone" with rationale.

## Summary
P0: 1 | P1: 2 | P2: 1 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=2 P2=1 P3=2 P4=0