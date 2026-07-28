# Edge-Cases Review -- round 2

## Closure of round 1 findings

- **R1/F-1 (P1) — Stale line-number anchor ship-spec line 38→39:** CLOSED. Corrected in spec.
- **R1/F-2 (P1) — Stale line-number anchor ship-spec line 258→256:** CLOSED. Corrected in spec.
- **R1/F-3 (P1) — Missing scope spec-reconcile:** CLOSED. Added to scope table and Design section with specific line references.
- **R1/F-4 (P1) — Missing scope spec-retire:** CLOSED. Added to scope table and Design section with specific line references.
- **R1/F-5 (P2) — Missing scope docs/customizing.md:** CLOSED. Added to scope table and Design section.
- **R1/F-6 (P2) — N/A test command parsing ambiguity:** CLOSED. Spec now defines exact parsing: strip code fences, trim whitespace, match case-insensitive `N/A`.
- **R1/F-7 (P2) — "Proceed directly to Phase 4" ambiguity:** CLOSED. Spec now says "Phase 2 (implementation) still runs normally, then proceed directly to Phase 4."
- **R1/F-8 (P3) — Synthetic ticket ID rename orphaned artifacts:** CLOSED. Spec now mentions renaming all `<TICKET-ID>.*` artifacts (brief, spec, reviews directory, test output).

## Findings

### F-1: spec-reconcile replacement count disagrees with actual occurrences
**Severity:** P1
**Where:** spec.md:15 (scope table)
**Edge case:** Scope table says "Replace 4 hardcoded MCP tool names (2 Plane, 2 memory)" but Design section 1 enumerates 6 occurrences across 5 lines: line 15 (2 Plane on one line), line 25 (1 memory), line 103 (1 memory), line 104 (2 Plane). An implementer following the scope table may stop at 4 replacements and miss 2.
**What happens:** 2 hardcoded MCP tool names survive un-replaced; grep audit catches them but the scope table is misleading.
**Suggested fix:** Change scope table to "Replace 6 hardcoded MCP tool name occurrences (4 Plane, 2 memory)" to match the design section.

### F-2: spec-reconcile scope table missing states.json mention
**Severity:** P2
**Where:** spec.md:15
**Edge case:** Design section 2 lists spec-reconcile line 14 as a states.json path reference, but the scope table row for spec-reconcile doesn't mention "add Windows path note for `states.json`" like the other skill rows do.
**What happens:** Implementer follows scope table, misses the states.json path update for spec-reconcile.
**Suggested fix:** Add "; add Windows path note for `states.json`" to the spec-reconcile scope table row.

### F-3: spec-retire replacement count ambiguity
**Severity:** P2
**Where:** spec.md:16
**Edge case:** Scope table says "Replace 3 hardcoded MCP tool names (all Plane)" but Design section lists line 30 (1), line 31 (1), and line 251 (2 on one line) = 4 occurrences. The scope table counts 3 distinct lines, not occurrences.
**What happens:** Minor confusion for implementer; grep audit catches any misses.
**Suggested fix:** Change to "Replace 4 hardcoded MCP tool name occurrences (all Plane)" or "Replace hardcoded MCP tool names across 3 lines (all Plane)".

### F-4: Test command doesn't execute grep audit
**Severity:** P2
**Where:** spec.md:156-158
**Edge case:** Test plan step 3 defines a grep audit that should return zero results. But the test command is only `python sync.py install --dry-run && python sync.py install`. The grep audit is described but not automated in the test command.
**What happens:** sync.py install succeeds but hardcoded tool names could survive if grep isn't run manually.
**Suggested fix:** Either add the grep to the test command or note that step 3 is a manual verification step.

### F-5: Test command `&&` is not PowerShell 5.1 compatible
**Severity:** P3
**Where:** spec.md:157
**Edge case:** `&&` pipeline chain operator is not available in Windows PowerShell 5.1. Since VHS-7 is about cross-platform compatibility, the test command itself should work cross-platform.
**What happens:** Test command fails on PS 5.1 with a parser error.
**Suggested fix:** Use `python sync.py install --dry-run; if ($LASTEXITCODE -eq 0) { python sync.py install }` for PS or note that bash is the expected shell.

### F-6: Round-trip degradation if MCP memory server is down
**Severity:** P3
**Where:** spec.md:39-40 (Decision 2)
**Edge case:** The capability description says "if available" for memory_search. If memory is down during spec-cycle, the reviewer agents also call memory_search in their grounding step. All three reviewers would get zero context from memory simultaneously.
**What happens:** Reviewers proceed using brief alone — this is the documented fallback. No spec change needed, just noting the blast radius.
**Suggested fix:** None needed; fallback is correct.

### F-7: Capability description example names could become stale
**Severity:** P4
**Where:** spec.md:29-37
**Edge case:** If Claude Code renames its MCP tools (e.g., namespace change), the example names in capability descriptions become stale. But they're just examples, not dependencies.
**What happens:** Examples become inaccurate but the capability description still conveys intent.
**Suggested fix:** None needed; acceptable staleness risk for documentation.

## Summary
P0: 0 | P1: 1 | P2: 3 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=3 P3=2 P4=1
