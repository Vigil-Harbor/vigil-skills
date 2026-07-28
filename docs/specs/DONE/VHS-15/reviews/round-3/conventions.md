# Conventions Review — round 3

## Closure of round 2 findings

All round-2 findings CLOSED (correctness/F-1 P1 + folded P2/P3/P4). The AGENTS.md:66 SSOT fold is appropriate (single-clause correction in a section already being edited; verified agents carry only `name`+`description`), not scope creep. No REOPENED items.

## Findings

### F-1: AGENTS.md:68 "all three reviewers" is a stale count in the Conventions section being edited — Scope names line 68 but §6 has no row
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope line 24 vs. § Design §6 table; target `AGENTS.md:68`
**Convention violated:** the spec's own reconciliation contract (Done-when 6 / Decision 9) and the item-12 grep gate.
**Evidence:** `AGENTS.md:68` reads "Severity scale is shared across all three reviewers". Scope line 24 names line 68 as an AGENTS.md edit, but §6 has no reconciliation row, so a §6-faithful implementation leaves it and the item-12 grep flags it. Pure count reconciliation ("all three reviewers" → "all reviewers"), clear of Decision 5's rubric/gate-formula fence (severity scale unchanged).
**Suggested fix:** Add a §6 row: `AGENTS.md:68` "shared across all three reviewers" → "shared across all reviewers (the three default lenses plus the optional scalability lens)".

### F-2: SKILL.md:270 "three Agent tool calls" is a count residual inside the 2b block with no §6 row
**Severity:** P3
**Where:** spec § Design §3 step 2b vs. § Design §6 table; target `skills/spec-cycle/SKILL.md:270`
**Evidence:** `SKILL.md:270` ("Single message, three Agent tool calls") matches `three (agent)`. §3 step 2b rewrites the dispatch block holistically but the literal "three Agent tool calls" prose isn't tabulated. The spec flags item 12 as "a locator … pair with an eyeball pass," so it'd be caught — but naming it removes ambiguity.
**Suggested fix:** Add a §6 row for `SKILL.md:270` ("three Agent tool calls" → "the reviewer Agent tool calls (three, or four when scale is declared)"), or note the line-270 reword in §3 step 2b.

## Decision-classification re-audit
No new (d) silent additions in the round-2→3 edits. The near-miss tripwire, deliberate-off escape, scale_lens collapse clause, and AGENTS.md:66 SSOT row are all (a) authorized implementations of round-2 findings. The two (c) items (README, portability-contract) remain correctly flagged.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

STATUS: GREEN
