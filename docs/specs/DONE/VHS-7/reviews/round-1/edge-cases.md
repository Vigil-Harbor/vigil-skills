# Edge-Cases Review -- round 1

## Closure of round 0 findings
N/A -- round 1

## Findings

### F-1: Stale line-number anchor for ship-spec `mcp__plane__list_projects`
**Severity:** P1
**Where:** spec.md:64
**Edge case:** Spec references "Line 38" but actual is line 39.
**What happens:** Implementer edits wrong line; `mcp__plane__list_projects` survives un-replaced.
**Why the spec misses it:** Line numbers shifted across edits.
**Suggested fix:** Change "Line 38" to "Line 39" or use step identifiers.

### F-2: Stale line-number anchor for ship-spec `mcp__plane__*` wildcard
**Severity:** P1
**Where:** spec.md:67
**Edge case:** Spec references "Line 258" but actual is line 256.
**What happens:** Implementer targets wrong line.
**Suggested fix:** Change "Line 258" to "Line 256".

### F-3: Missing scope -- `spec-reconcile/SKILL.md` has hardcoded MCP tool names
**Severity:** P1
**Where:** spec.md:9
**Edge case:** Test plan grep covers all of `skills/` but spec-reconcile is out of scope; grep would fail.
**What happens:** Test plan contradicts scope -- grep audit fails even after all VHS-7 changes.
**Suggested fix:** Expand scope to include spec-reconcile or narrow grep.

### F-4: Missing scope -- `spec-retire/SKILL.md` has hardcoded MCP tool names
**Severity:** P1
**Where:** spec.md:9
**Edge case:** Same as F-3 but for spec-retire. Uses `mcp__claude_ai_Plane__` prefix not caught by existing grep patterns.
**What happens:** Hardcoded tool names survive completely undetected.
**Suggested fix:** Add to scope and add `mcp__claude_ai_Plane__` grep pattern.

### F-5: Missing scope -- `docs/customizing.md` has hardcoded MCP tool name
**Severity:** P2
**Where:** spec.md:23
**Edge case:** Spec says customizing.md has "no MCP tool names" but it has `mcp__plane__list_states` on line 66.
**What happens:** User-facing doc retains hardcoded tool name.
**Suggested fix:** Add to scope or correct "Files to leave alone" claim.

### F-6: ship-spec `N/A` test command parsing ambiguity
**Severity:** P2
**Where:** spec.md:100-102
**Edge case:** Spec says "only `N/A` (case-insensitive, trimmed)" but doesn't define parsing for code fences or trailing text.
**What happens:** Ambiguous whether `N/A - documentation only` triggers the escape hatch.
**Suggested fix:** Define exact parsing rule: strip markdown code fences, trim whitespace, match `/^N\/A$/i`.

### F-7: ship-spec `N/A` skip "proceed directly to Phase 4" is ambiguous
**Severity:** P2
**Where:** spec.md:102
**Edge case:** "Proceed directly to Phase 4 (commit)" could skip Phase 2 (implementation) too.
**What happens:** Implementer might skip Phase 2, leaving worktree unchanged.
**Suggested fix:** Change to "Skip Phase 3 (test gate) only; Phase 2 still runs."

### F-8: Synthetic ticket ID rename -- orphaned review artifacts
**Severity:** P3
**Where:** spec.md:106-108
**Edge case:** Only mentions renaming the brief file, not the spec/reviews/test-output.
**What happens:** ship-spec looks for spec under new ID and doesn't find it.
**Suggested fix:** Expand to mention renaming all `<TICKET-ID>.*` artifacts.

## Summary
P0: 0 | P1: 4 | P2: 3 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=4 P2=3 P3=1 P4=0