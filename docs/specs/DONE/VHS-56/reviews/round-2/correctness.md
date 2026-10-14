# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Cycle-2 failure has conflicting irreversible outcomes | CLOSED | `spec.md:155–157` restricts partial completion to small/big and excludes it from irreversible reuse; `spec.md:211` restarts on upgrade. The restart introduces a separate cycle-count conflict reported below. |
| correctness | F-2 | Adding a decision under no-grill leaves the previous review valid | CLOSED | `spec.md:213` explicitly invalidates the result, re-renders, and restarts Phase 3 after the no-grill addition. |
| correctness | F-3 | ground-truth ledger omits runtime claims | CLOSED | Round-2 ledger includes the ticket-only derivation and atomic-write claims. Their missing sentence-local anchors are reported below. |
| correctness | F-4 | ticket not cached | DEFERRED | `spec.md:278` records the advisory limitation; this round's lookup still returns access denied. |
| edge-cases | F-1 | A partially failed pass can become valid for an irreversible brief | CLOSED | `spec.md:157,211` distinguishes partial completion and forbids its reuse on upgrade. |
| edge-cases | F-2 | Adding a decision under `--no-grill` retains a stale doubt result | CLOSED | `spec.md:213` covers this exact branch; Test plan item 8 includes it. |
| edge-cases | F-3 | Ticket grounding was blocked by namespace permissions | DEFERRED | `spec.md:278` preserves the limitation; independent ticket verification remains unavailable. |
| edge-cases | F-4 | The persisted operator skip reason has no size bound | DEFERRED | `spec.md:279` explicitly leaves this optional audit-size improvement for later. |
| conventions | F-1 | A failed second cycle can become an irreversible completion | CLOSED | `spec.md:155–157,211` excludes failed dispatches from irreversible completion. |
| conventions | F-2 | Confirm invalidation omits the existing no-grill decision-addition path | CLOSED | `spec.md:213` now names the existing branch and its restart behavior. |

## Findings

### F-1: Recovery requires two successful cycles even when the second is forbidden
**Severity:** P1
**Where:** docs/specs/TODO/VHS-56.spec.md:157
**Claim:** “restart Phase 3 at cycle 1; if both cycles do not complete successfully, stop and write nothing.”
**Why this is wrong:** Decision 2 at `spec.md:39` permits cycle 2 only when the new cycle 1 changes the candidate. Consider a big run whose second dispatch fails, followed by an upgrade to irreversible: the restarted cycle 1 returns no findings, so no second dispatch is permitted. Decision 12 nevertheless requires both cycles to succeed, and Design 6 at `spec.md:211` repeats “both required dispatches.” The restart therefore either halts despite a successful clean review or dispatches an unchanged candidate contrary to the cycle rule. The original unsafe reuse is fixed, but recovery is now inconsistent with the normal completion condition.
**Suggested fix:** Require every dispatch attempted in the restarted pass to succeed. Explicitly allow completion after an unchanged cycle 1; require cycle 2 only if that restarted cycle 1 changes the draft. Apply this wording in Decision 12, Design 6, and the restart test case.

### F-2: Ticket-only derivation anchor exists only in the ledger
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** docs/specs/TODO/VHS-56.spec.md:174
**Claim:** “Under `--no-grill`, it uses the existing ticket-only decision derivation.”
**Why this is wrong:** Ground-truth ledger row 1 gives `skills/spec-brief/SKILL.md:184`, and the freshly opened source supports the claim. However, the spec sentence carries no anchor. Ground-truth grading rule 3 treats an anchor supplied only by the ledger as an advisory defect.
**Suggested fix:** Append `skills/spec-brief/SKILL.md:184` to the spec sentence.

### F-3: Atomic-write anchor exists only in the ledger
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** docs/specs/TODO/VHS-56.spec.md:215
**Claim:** “Phase 5 … keeps the existing atomic write.”
**Why this is wrong:** Ground-truth ledger row 4 anchors this claim at `skills/spec-brief/SKILL.md:218`, which supports it. The spec sentence itself has no anchor, triggering ground-truth grading rule 3.
**Suggested fix:** Append `skills/spec-brief/SKILL.md:218` to this sentence.

### F-4: General invalidation wording should exempt tier-only changes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** docs/specs/TODO/VHS-56.spec.md:213
**Claim:** “Every Confirm action that changes candidate brief content invalidates the prior doubt result.”
**Why this is wrong:** The preceding paragraph explicitly preserves a successfully completed pass across tier changes (`spec.md:211`). A tier change also changes candidate content because the candidate contains the final `## Tier` section (`spec.md:174`; `skills/spec-brief/SKILL.md:202,208–216`). The specific tier rule makes the intended behavior recoverable, but the general sentence obscures that exception.
**Suggested fix:** Say that substantive candidate edits invalidate the result, with tier-only changes governed by the preceding paragraph.

### F-5: ticket not cached
**Severity:** P3
**Where:** spec § Done when
**Claim:** The spec implements the narrowed VHS-56 contract.
**Why this is wrong:** Canonical ticket verification remains unavailable. The required shared-memory lookup with namespace `skills`, tags `plane_work_item` and `VHS-56`, and source system `plane` returned `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. This review therefore uses the brief and its explicit scope split.
**Suggested fix:** Verify the canonical ticket when authorized access becomes available; make no speculative scope change.

## Summary

P0: 0 | P1: 1 | P2: 3 | P3: 1 | P4: 0

All four ground-truth rows were checked against freshly opened sources. Their claims are supported; two sentence-local anchors are missing. The closure manifest covers every predecessor P0/P1 finding. No `## Deferred — follow-up required` section is present.

The cross-section walk covered dispatch eligibility, cycle transitions, report parsing, outcome records, tier changes, and Confirm mutations. It found the restart conflict above; the original failure-reuse and no-grill invalidation defects are closed.

Touched files changed within seven days, including `5f640d0` on October 11 and `33b9215` on October 13. Review used the current on-disk versions.

STATUS: RED P0=0 P1=1 P2=3 P3=1 P4=0
