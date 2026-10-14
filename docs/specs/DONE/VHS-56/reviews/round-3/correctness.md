# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Recovery requires two successful cycles even when the second is forbidden | CLOSED | `docs/specs/TODO/VHS-56.spec.md:157` permits completion after an unchanged restarted cycle 1 and requires cycle 2 only after a draft change. Design 6 at line 211 and Test plan item 4 at line 242 agree. |
| correctness | F-2 | Ticket-only derivation anchor exists only in the ledger | CLOSED | Spec line 174 now cites `skills/spec-brief/SKILL.md:184`; the source supports the claim. |
| correctness | F-3 | Atomic-write anchor exists only in the ledger | CLOSED | Spec line 215 now cites `skills/spec-brief/SKILL.md:218`; the source supports the claim. |
| correctness | F-4 | General invalidation wording should exempt tier-only changes | CLOSED | Spec line 213 explicitly exempts tier-only changes from substantive-edit invalidation and refers them to the preceding paragraph. |
| correctness | F-5 | ticket not cached | DEFERRED | Spec line 278 preserves the grounding limitation. This round’s required lookup again returned access denied; see F-1 below. |
| edge-cases | F-1 | Restart requires a second cycle that the cycle rule can forbid | CLOSED | Spec lines 157, 211, and 242 consistently apply Decision 2’s conditional second-cycle rule to recovery. |
| edge-cases | F-2 | Ticket grounding remains blocked by namespace permissions | DEFERRED | Spec line 278 records this environment limitation; canonical-ticket access remains unavailable. |
| conventions | F-1 | Recovery wording implies an unconditional second cycle | CLOSED | Spec lines 157 and 211 remove the unconditional requirement; line 242 explicitly tests an unchanged restarted cycle 1. |

## Findings

### F-1: ticket not cached
**Severity:** P3
**Where:** docs/specs/TODO/VHS-56.spec.md:278
**Claim:** “Canonical ticket verification was unavailable because shared memory denied the `skills` namespace.”
**Why this is wrong:** Independent canonical-ticket verification remains unavailable. This round’s required search using namespace `skills`, tags `plane_work_item` and `VHS-56`, and source system `plane` returned `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. This is a review-environment limitation, not an implementation defect. The review therefore uses the brief and its explicitly documented scope split.
**Suggested fix:** Preserve the limitation in the review record and verify the canonical ticket when authorized access becomes available. No speculative scope change is warranted.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

The closure manifest covers both predecessor P0/P1 findings. All four ground-truth ledger rows were checked against freshly opened anchors and their spec sentences; the claims are supported and sentence-local anchors are present. No `## Deferred — follow-up required` section is present.

The cross-section consistency walk covered reviewer eligibility, dispatch payload and report parsing, conditional cycle transitions, persisted outcomes, tier changes, Confirm invalidation, and final emission. No blocking disagreement remains. The brief’s acceptance criteria map to the decisions, design, and test matrix.

Touched files changed within seven days, including `5f640d0` on October 11 and `33b9215` on October 13. Grounding used their current on-disk versions.

STATUS: GREEN
