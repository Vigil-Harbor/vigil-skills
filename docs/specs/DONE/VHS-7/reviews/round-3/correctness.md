# Correctness Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | spec-reconcile scope table count inconsistency | CLOSED | spec.md line 15 now reads "Replace 6 hardcoded MCP tool name occurrences (4 Plane, 2 memory)" -- verified against actual file: 4 Plane occurrences (lines 15x2, 104x2) + 2 memory occurrences (lines 25, 103) = 6 |
| correctness | F-2 | Capability description wording not verified | CLOSED | P3 advisory, no spec change needed |
| correctness | F-3 | Test command `&&` is Unix-specific | CLOSED | P4 nit, no spec change needed |
| edge-cases | F-1 | spec-reconcile replacement count disagrees with occurrences | CLOSED | spec.md line 15 now says "Replace 6 hardcoded MCP tool name occurrences (4 Plane, 2 memory)" -- matches actual count |
| edge-cases | F-2 | spec-reconcile missing states.json mention | CLOSED | spec.md line 15 now includes "; add Windows path note for `states.json`" |
| edge-cases | F-3 | spec-retire replacement count ambiguity | CLOSED | spec.md line 16 now says "Replace 4 hardcoded MCP tool name occurrences across 3 lines (all Plane)" -- verified: lines 30(1), 31(1), 251(2) = 4 occurrences across 3 lines |
| edge-cases | F-4 | Test command doesn't execute grep audit | CLOSED | P2 advisory; the grep is described in the test plan as a manual verification step, acceptable for doc-only change |
| edge-cases | F-5 | Test command `&&` not PS 5.1 compatible | CLOSED | P3 advisory; bash is the expected shell environment |
| edge-cases | F-6 | Round-trip degradation if MCP memory server is down | CLOSED | P3 informational; fallback is correct as documented |
| edge-cases | F-7 | Capability description example names could become stale | CLOSED | P4 nit; acceptable staleness risk |
| conventions | F-1 | Scope table replacement counts use "tool names" ambiguously | CLOSED | Both spec-reconcile (line 15) and spec-retire (line 16) now use "occurrences" phrasing |
| conventions | F-2 through F-7 | Various P3/P4 observations | CLOSED | No spec changes needed |

## Findings

### F-1: Ticket VHS-7 not cached in MCP memory
**Severity:** P3
**Where:** N/A (grounding step)
**Claim:** N/A
**Why this is worth noting:** `memory_search` for VHS-7 in `vhs` namespace returned zero results. Consistent with rounds 1 and 2. Proceeding using the brief alone.
**Suggested fix:** No spec change needed. Cache the VHS-7 ticket when convenient.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
