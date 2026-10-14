# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Recovery requires two successful cycles even when the second is forbidden | CLOSED | `docs/specs/TODO/VHS-56.spec.md:157` and `:211` explicitly allow an unchanged restarted cycle 1 to complete the pass; cycle 2 is required only after a draft change. Test plan item 4 covers both branches. |
| correctness | F-2 | Ticket-only derivation anchor exists only in the ledger | CLOSED | Spec line 174 now cites `skills/spec-brief/SKILL.md:184`; the live source supports the claim. |
| correctness | F-3 | Atomic-write anchor exists only in the ledger | CLOSED | Spec line 215 now cites `skills/spec-brief/SKILL.md:218`; the live source defines the temporary-sibling rename. |
| correctness | F-4 | General invalidation wording should exempt tier-only changes | CLOSED | Spec line 213 explicitly routes tier-only changes through the preceding paragraph. |
| correctness | F-5 | ticket not cached | DEFERRED | Spec line 278 preserves the grounding limitation. The fresh lookup again returned access denied; see F-1 below. |
| edge-cases | F-1 | Restart requires a second cycle that the cycle rule can forbid | CLOSED | Spec lines 157 and 211 require every dispatch called for by Decision 2 to succeed, without imposing an unconditional second dispatch. Test plan item 4 includes an unchanged restarted cycle 1. |
| edge-cases | F-2 | Ticket grounding remains blocked by namespace permissions | DEFERRED | Spec line 278 retains the limitation; this review independently reproduced it. |
| conventions | F-1 | Recovery wording implies an unconditional second cycle | CLOSED | Spec lines 157 and 211 distinguish the one-cycle and two-cycle recovery paths explicitly. |

## Findings

### F-1: Ticket grounding remains blocked by namespace permissions
**Severity:** P2  
**Where:** docs/specs/TODO/VHS-56.spec.md:278  
**Edge case:** The required canonical-ticket lookup targets namespace `skills`, tags `plane_work_item` and `VHS-56`, and source system `plane`.  
**What happens:** Shared memory returns `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. The review therefore uses the supplied brief and its explicit scope split as the contract.  
**Why the spec misses it:** This is an existing review-environment limitation, already recorded in the spec, rather than an implementation defect.  
**Suggested fix:** Preserve the limitation in the review record and independently verify the ticket when an authorized read becomes available. No speculative scope change is needed.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

The restart inconsistency is closed. The full review covered empty and malformed reviewer output, count mismatches, unavailable model metadata, source-verification failures, operator interruption, conditional cycle dispatch, partial completion, tier changes, Confirm revisions, and final file I/O. No additional blocking failure path was found.

Persistence checklist for the new `## Doubt pass` metadata:

- **Atomicity — CHECKED:** Spec line 215 retains the full-brief atomic write defined at `skills/spec-brief/SKILL.md:218`.
- **Size bound — FLAGGED, previously deferred:** Spec line 279 retains round-1 edge-cases/F-4 concerning the operator’s unbounded skip reason. It remains an optional audit-size improvement.
- **Idempotency — CHECKED:** Existing artifact-collision confirmation protects retries; the metadata occupies one section within the brief.
- **Read-side mode filtering — CHECKED:** Decision 4 makes the section inert; no production/dev selection mechanism is introduced.
- **Schema-version compatibility — CHECKED:** Downstream skills do not consume the new metadata, so older briefs remain usable.
- **Concurrent writes — CHECKED:** `skills/spec-brief/SKILL.md:220` explicitly documents last-writer-wins and excludes simultaneous same-ticket runs from the supported flow.

No `## Deferred — follow-up required` section or structured deferred rows are present. The ordinary `## Deferred (P2+)` section contains advisory follow-ups only.

STATUS: GREEN
