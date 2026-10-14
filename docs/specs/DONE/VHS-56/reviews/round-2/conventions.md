# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Cycle-2 failure has conflicting irreversible outcomes | CLOSED | Spec § Decision 12, lines 155–157, explicitly halts irreversible runs on either dispatch failure and restricts partial completion to small/big. Design 6, line 211, excludes partial completion from reuse after an upgrade. |
| correctness | F-2 | Adding a decision under no-grill leaves the previous review valid | CLOSED | Spec § Design 6, line 213, explicitly clears the result after a no-grill decision addition and restarts Phase 3; Test plan item 8 covers this branch. |
| correctness | F-3 | ground-truth ledger omits runtime claims | CLOSED | `round-2/ground-truth-ledger.md` includes the ticket-only derivation and atomic-write claims, naming Design 2 and Design 6 and the live anchors at `skills/spec-brief/SKILL.md:184` and `:218`. |
| correctness | F-4 | ticket not cached | DEFERRED | Spec § Deferred (P2+), line 278, records the namespace-permission limitation and continued reliance on the explicitly narrowed brief. Independent ticket verification remains outstanding. |
| edge-cases | F-1 | A partially failed pass can become valid for an irreversible brief | CLOSED | Spec § Decision 12, line 157, introduces `dispatch_failed: true`; Design 6, line 211, discards the partial result on upgrade and restarts the pass. |
| edge-cases | F-2 | Adding a decision under `--no-grill` retains a stale doubt result | CLOSED | Spec § Design 6, line 213, re-renders the appended decision and restarts Phase 3 without reusing reviewer output. |
| edge-cases | F-3 | Ticket grounding was blocked by namespace permissions | DEFERRED | Spec § Deferred (P2+), line 278, preserves the review-environment limitation; no implementation change is claimed. |
| edge-cases | F-4 | The persisted operator skip reason has no size bound | DEFERRED | Spec § Deferred (P2+), line 279, explicitly retains this optional audit-size improvement as deferred. |
| conventions | F-1 | A failed second cycle can become an irreversible completion | CLOSED | Spec § Decision 12, lines 155–157, and Design 6, line 211, distinguish successful completion from cycle-2 failure and prohibit using the latter for irreversible. |
| conventions | F-2 | Confirm invalidation omits the existing no-grill decision-addition path | CLOSED | Spec § Design 6, line 213, now explicitly covers the existing branch at `skills/spec-brief/SKILL.md:184`; Test plan item 8 mirrors it. |

## Findings

### F-1: Recovery wording implies an unconditional second cycle
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** docs/specs/TODO/VHS-56.spec.md:157; spec § 6. Renumber Confirm and Write and make the outcome visible
**Convention violated:** The spec's bounded-review rule should have one consistent condition for dispatching cycle 2.
**Evidence:** Decision 2, line 39, allows cycle 2 only when cycle 1 changes the candidate and explicitly ends an unchanged review after cycle 1. The upgrade recovery at line 157 instead says “if both cycles do not complete successfully, stop and write nothing”; Design 6 calls them “both required dispatches.” A restarted cycle 1 can return no findings, leaving no permitted second dispatch. The wording does not clearly distinguish failure of a required dispatch from a second dispatch that was never required.
**Suggested fix:** Say that every dispatch required by Decision 2 must complete successfully, and explicitly preserve its conditional cycle-2 rule on restart. Add a test case where a big pass suffers cycle-2 failure, upgrades to irreversible, and the restarted cycle 1 completes without changing the draft.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

The prior blocking findings are closed. The spec preserves the existing mutation boundary, portable capability vocabulary, operator ownership of decisions, and live verification of reviewer facts.

STATUS: GREEN
