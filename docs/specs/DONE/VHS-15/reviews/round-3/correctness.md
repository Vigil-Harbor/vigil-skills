# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Broadened grep flags reconciled :9/:3/:17/:25 | CLOSED | §6 forms reworded to "three default lenses"/"three by default"/"independent AI agents (three by default…)"; item 12 reframed as zero-match locator (spec:234). Empirically all reconciled forms dodge the alternation. |
| correctness | F-2 (P3) | `:357–368` clips block | CLOSED | All four refs → `SKILL.md:357–371`. |
| correctness | F-3 (P3) | preflight-summary "ending" wording | CLOSED | §3 step 8 now "after the origin token and before '— then continue'". |
| edge-cases | F-1 (P2) | near-miss heading silent drop | CLOSED | §2 rule 1 near-miss tripwire. |
| edge-cases | F-2 (P2) | deliberate-off escape | CLOSED | §3 step 8 escape clause. |
| conventions | F-1 (P4) | AGENTS.md:66 SSOT | CLOSED | §6 :66 row + Scope line 24. |
| conventions | F-2 (P3) | scale_lens collapse | CLOSED | §3 step 2b collapse clause. |
| conventions | F-3 (P3) | decision-classification | CLOSED | Recorded in Deferred. |

All eight round-2 findings verify closed. No REOPENED/PARTIAL.

## Findings

### F-1: Checklist item 12's "grep returns zero" pass-bar is unreachable — §6 omits two surviving count-residuals (AGENTS.md:68, SKILL.md:270)
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan item 12 vs. § Design §6 table; Scope line 24
**Claim:** Item 12 — "Pass = the grep returns zero after a faithful §6 implementation."
**Why this is wrong:** Two count-residuals match the locator but have no §6 row: `AGENTS.md:68` ("shared across all three reviewers" → `three (reviewer)`) — Scope line 24 names line 68 but §6 has no row — and `SKILL.md:270` ("three Agent tool calls" → `three (agent)`), implicitly rewritten by §3 step 2b but not tabulated. A §6-faithful implementation leaves both, contradicting "returns zero."
**Suggested fix:** Add §6 rows for `AGENTS.md:68` ("shared across all three reviewers" → "shared across all reviewers …") and `SKILL.md:270` ("three Agent tool calls" → "the reviewer Agent tool calls (three, or four when scale is on)"); both are pure count reconciliations (Decision 5's rubric untouched).

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

STATUS: GREEN
