# Conventions Review — round 2

## Closure of round 1 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Irreversible reinstates a rejected VHS-46 halt and drops its review-file record | CLOSED | spec § Decision 8 line 61 names the VHS-46 decision and limits the supersession to `irreversible`; § ship-spec Phase 3b lines 244 and 256 keep the skipped-form review file and amend `:432-433` |
| conventions | F-2 | Basis-line template does not generate the normative examples | CLOSED | spec § Decision 14 lines 105–113: three comma-separated slots, singular counts, four normative examples; pipe sketch gone |
| conventions | F-3 | Tweak-surfaces "then" reads as first-wins | CLOSED | spec § Decision 14 Extension lines 102–103: both files when present, union, not the review-command order, body to the next `^#{1,6}` heading |
| conventions | F-4 | Workflow-reference cap and gate sentences stay literal | CLOSED | spec § Docs line 270 rewrites `:84-86`, `:246`, `:66`, `:27`, `:102`, and the `:187` irreversible exception |
| conventions | F-5 | A near-miss Tier heading halts; Scale's near-miss only warns | CLOSED | spec § spec-cycle brief parse step 1 line 174: stricter than Scale on purpose, and only when no strict heading matched |
| conventions | F-6 | Decision 14 pins past Risk 2 | CLOSED | spec § Decision 14 lines 86, 89, and 103 each labeled "spec pin beyond Risk 2" |
| conventions | F-7 | README still states a fixed 4-pass loop | CLOSED | spec § Scope line 24: `README.md:10` stays the big-tier maximum and is not updated |
| correctness | F-1 | Looser Tier heading rule halts every valid `## Tier` section | CLOSED | spec § spec-cycle brief parse step 1 line 174: looser rule only when no strict `^#{1,6}\s+tier\s*$` match; a second strict heading warns and is not a near-miss |
| correctness | F-2 | Malformed-brief halt runs before the re-run pin | CLOSED | spec § spec-cycle lines 168–172 apply the pin before the brief parse can halt; § Done when line 298 states the same partition |
| correctness | F-3 | A non-bare `**Tier:**` line is read as absent and becomes `big` | CLOSED | spec § reader rule lines 180–181: case-insensitive label; empty, trailing note, or stuck punctuation halts; absence is no label line |
| correctness | F-4 | Irreversible "re-run /ship-spec" cannot resume the worktree it just created | DEFERRED | D-1 lines 320–329 is well-formed (preamble present, seven fields, blockquoted fix, two sites that exist, Scope `in-scope` matches brief Scope row `skills/ship-spec/SKILL.md`, P1 so the ceiling does not apply) |
| correctness | F-5 | Post-cap Confirm still offers only options 1 and 3 | CLOSED | spec § spec-brief Confirm line 154: post-cap menu is options 1, 3, and 4; a bad re-ask reprints and does not discard the interview |
| correctness | F-6 | Tweak-floor match mode and basis line are not pinned tightly enough | CLOSED | spec § Decision 14 lines 92–106: segment-or-filename equality, `config.py` excluded, union, basis grammar matches the examples |
| correctness | F-7 | `round_cap` rewrite leaves literal cap-of-4 sentences in force | CLOSED | spec substitution table line 203 adds `:672`; lines 213–214 keep grilling's literal 3; § Docs line 270 and § AGENTS.md line 272 cover the leftover cap sentences including `AGENTS.md:25` |
| correctness | F-8 | Ship-spec's other copies of the gate contract stay unconditional | CLOSED | spec § ship-spec lines 234, 241, and 256: canonical table stays fingerprint-only, `N/A` skip unchanged, `:432-433` gain the irreversible exception |
| correctness | F-9 | ticket not cached | CLOSED | spec § Deferred (P2+) line 314 records no spec change; `memory_search` on namespace `skills` still returns access denied for this agent; the brief remains the record |
| edge-cases | F-1 | Malformed-brief halt and the re-run pin cannot both be true | CLOSED | same partition as correctness F-2: spec lines 168–172 and Done when line 298 |
| edge-cases | F-2 | A near-miss `**Tier:**` line is read as absent `big` | CLOSED | spec § reader rule lines 180–181, applied to attest, the re-run pin, and ship-spec |
| edge-cases | F-3 | A clean irreversible review is specified as the failed halt | DEFERRED | D-2 lines 331–340 is well-formed (same preamble and field checks as D-1; Scope `in-scope` matches the brief's ship-spec Phase 3b row; P1) |
| edge-cases | F-4 | Irreversible re-run stops on the leftover worktree | CLOSED | spec § ship-spec halt text lines 249–251 name the worktree and branch and say a re-run does not resume Phase 3b by itself |
| edge-cases | F-5 | Failure-mode bullets still say a failed review never halts | CLOSED | spec § ship-spec line 256 |
| edge-cases | F-6 | At `round_cap = 2`, FROZEN ignores the round that reviewed the revision | CLOSED | spec substitution table line 202: current round forces REWRITE |
| edge-cases | F-7 | `round_cap = 2` leaves the grill-apply rules and the grilling cap bound to the wrong 4 | CLOSED | spec lines 203 and 213: line 672 follows `round < round_cap`; line 646 passes the literal 3 as the interview cap |
| edge-cases | F-8 | Quoted multi-word surface signals do not match a "whole word" check | CLOSED | spec § Decision 14 lines 92–93 and worked example 4 line 113 |
| edge-cases | F-9 | `small` plus `Test command: N/A` drops both gates, and the spec says Phase 3 still runs | CLOSED | spec § ship-spec line 241: `small` does not skip Phase 3; the existing `N/A` skip still applies |
| edge-cases | F-10 | A fenced `**Level:**` line in the brief becomes the tier | CLOSED | spec § spec-cycle brief parse step 2 line 175: unfenced Level line only; a fenced example does not set `round_cap` |
| edge-cases | F-11 | Confirming a tier mismatch ships the absent-line tier, not the marker | PARTIAL | confirm sentence is at spec § ship-spec line 232; the attest rewrite is explicitly not folded (§ Deferred (P2+) line 313; early return stays at line 221). P2, recorded on purpose |
| edge-cases | F-12 | Plane ticket body was not readable | CLOSED | spec § Deferred (P2+) line 314; finding asked for no spec change. Lookup this round was access denied again |

## Findings

### F-1: Workflow reference still puts the seed gate inside the interview `--no-grill` skips
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Docs and AGENTS.md (spec.md:270); `docs/spec-workflow-reference.md:11` and `:17`
**Convention violated:** Same-file reconciliation. `decisions/2026-06-16-vhs-15-optional-scalability-lens.md` kept this reference from carrying a heading that contradicted the body. The spec's doc edit is a closed line list and does not include the spec-brief paragraphs that the hoist falsifies.
**Evidence:** The reference says "`--no-grill` skips the interview but not the confirmation step" (`:11`) and, under Phase 2 — Interview, "A seed that states no problem is gated first" (`:17`). The spec hoists that gate so "Skipped entirely under `--no-grill`" no longer covers it (spec § spec-brief, lines 118–119) and runs it in every mode before the tier question (§ Done when). The rewrite list at spec line 270 names the loop-cap sentences and `:187` only.
**Suggested fix:** Add `:11` and `:17` to that list: the seed gate runs before the tier gate in every mode, including `--no-grill`, and is not part of the interview that flag skips. At `:21`, name `## Tier` on every brief Phase 4 writes.

### F-2: customizing.md still says a skipped review never blocks, with no leave-alone note
**Severity:** P3
**Where:** spec § Scope, leave-alone list (spec.md:25); `docs/customizing.md:40`
**Convention violated:** The README leave-alone note (round-1 conventions F-7, now at spec line 24) records a tracked sentence that stays at the big-tier maximum. `docs/customizing.md` is left alone with no such note, and it states the VHS-46 rule Decision 8 supersedes for `irreversible`.
**Evidence:** `docs/customizing.md:40`: "A declared command that is not available on the host, or that fails, is also skipped and never blocks the commit." Spec Decision 8 (line 61) supersedes that rule for `irreversible` only. The brief's scope table does not list this file.
**Suggested fix:** One phrase in the leave-alone list: `docs/customizing.md:40` stays today's skip for `big` and an absent tier and is not updated for the irreversible halt. Do not open that file beyond that clause.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

STATUS: GREEN
