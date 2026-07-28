# Edge-Cases Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | R2/F-1 | spec-reconcile replacement count 4 vs 6 | CLOSED | spec line 15 now says "Replace 6 hardcoded MCP tool name occurrences (4 Plane, 2 memory)" -- verified against source: line 15 (2 Plane), line 25 (1 memory), line 103 (1 memory), line 104 (2 Plane) = 6 total |
| edge-cases | R2/F-2 | spec-reconcile missing states.json mention | CLOSED | spec line 15 now includes "; add Windows path note for `states.json`" |
| edge-cases | R2/F-3 | spec-retire replacement count ambiguity | CLOSED | spec line 16 now says "Replace 4 hardcoded MCP tool name occurrences across 3 lines (all Plane)" -- verified: lines 30(1), 31(1), 251(2) = 4 occurrences on 3 lines |
| edge-cases | R2/F-4 | Test command doesn't execute grep audit | CLOSED | P2 advisory; grep audit is a manual verification step in test plan; acceptable for doc-only change |
| edge-cases | R2/F-5 | Test command && not PS 5.1 compatible | CLOSED | P3 advisory; bash is the expected shell for test commands |
| edge-cases | R2/F-6 | Round-trip degradation if MCP memory down | CLOSED | P3 informational; fallback is correct |
| edge-cases | R2/F-7 | Capability description example names staleness | CLOSED | P4; acceptable risk |
| All R1 findings | | | CLOSED | Confirmed closed in R2 closure table |

## Findings

### F-1: ship-spec scope row says "4 hardcoded MCP tool names" -- phrasing inconsistent with sibling rows
**Severity:** P3
**Where:** spec.md:14
**Edge case:** spec-reconcile row says "6 occurrences" and spec-retire says "4 occurrences across 3 lines", but ship-spec row says "4 hardcoded MCP tool names" without "occurrences" qualifier. Count is coincidentally correct either way (4 distinct occurrences of 3 distinct tool names + 1 wildcard). No functional impact since Design section 1 enumerates all 4 explicitly.
**What happens:** Terminology inconsistency only. Implementer would find all 4 regardless.
**Suggested fix:** Change to "Replace 4 hardcoded MCP tool name occurrences" for consistency.

### F-2: N/A escape hatch + synthetic ticket ID interaction through ship-spec Phase 6
**Severity:** P3
**Where:** spec.md:125, 131
**Edge case:** A doc-only spec with N/A test command AND a synthetic ticket ID would hit ship-spec Phase 6 (Plane update) which tries to call `mcp__plane__update_work_item`. Existing ship-spec Phase 0 step 8 warn-and-skip behavior already handles Plane unreachability, and Phase 6 has graceful degradation. No crash.
**What happens:** Graceful degradation via existing failure modes. No spec change strictly needed.
**Suggested fix:** Optionally add a cross-reference sentence, but existing failure paths cover it.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 0

STATUS: GREEN
