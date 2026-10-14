# Conventions Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: A failed second cycle can become an irreversible completion
**Severity:** P0
**Where:** spec.md:209; spec § Decision 12 — Failure posture follows tier and never silently substitutes same-model review
**Convention violated:** The spec's irreversible failure rule and the established rule that stricter tiers halt on failed review.
**Evidence:** Decision 12 (`spec.md:155`) says an irreversible dispatch failure stops without writing, but labels a cycle-2 failure `completed at cap` for the permissive tiers. Design 6 (`spec.md:209`) then declares that “a prior completed pass remains valid” when changing to irreversible, without excluding that failure outcome. Thus a big run can fail cycle 2, change tier, and write an irreversible brief without satisfying the failure rule. Test-plan item 4 explicitly requires no write when an irreversible dispatch fails. The live precedent in `skills/ship-spec/SKILL.md:199` likewise makes failed review a halt for irreversible.
**Suggested fix:** Distinguish a successfully completed capped pass from a failed second dispatch in carried state. Explicitly exclude the failed-dispatch outcome from reuse on an upgrade to irreversible, and specify the recovery or halt behavior. Clarify that Decision 12's partial-completion recording applies only to small/big, and add the failed-cycle-2 → irreversible transition to the test matrix.

### F-2: Confirm invalidation omits the existing no-grill decision-addition path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:209
**Convention violated:** Preserve and reconcile every existing Confirm branch when changing its review flow.
**Evidence:** `skills/spec-brief/SKILL.md:184` changes Confirm option 2 under `--no-grill` to “Add a decision (state it) — appended to Decisions carried forward.” Design 6 preserves the existing menu but invalidates the prior doubt result only when “Revising an interview answer”; it re-enters Phase 3 after a resumed interview. The no-grill addition has neither an interview answer nor a resumed interview, although it changes the candidate for the same reason that motivates the stated invalidation rule.
**Suggested fix:** State that adding a decision under `--no-grill` invalidates the prior doubt result and re-enters Phase 3 using the updated candidate, with the current tier policy. Add that transition to test-plan item 8.

## Summary

P0: 1 | P1: 0 | P2: 1 | P3: 0 | P4: 0

STATUS: RED P0=1 P1=0 P2=1 P3=0 P4=0
