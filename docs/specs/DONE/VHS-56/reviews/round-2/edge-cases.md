# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Cycle-2 failure has conflicting irreversible outcomes | CLOSED | Spec lines 155–157 explicitly halt irreversible failures and restrict partial completion to small/big. |
| correctness | F-2 | Adding a decision under no-grill leaves the previous review valid | CLOSED | Spec line 213 invalidates the result and restarts Phase 3 after a no-grill addition; line 246 tests this path. |
| correctness | F-3 | ground-truth ledger omits runtime claims | CLOSED | Round-2 ground-truth ledger includes Design 2’s ticket-only derivation and Design 6’s atomic write, supported by current skill lines 184 and 218. |
| correctness | F-4 | ticket not cached | DEFERRED | Spec line 278 records the grounding limitation; the current lookup again returned access denied. See F-2 below. |
| edge-cases | F-1 | A partially failed pass can become valid for an irreversible brief | CLOSED | Spec lines 157 and 211 prohibit reusing partial completion and require a restart. The restart introduces the distinct inconsistency in F-1 below. |
| edge-cases | F-2 | Adding a decision under `--no-grill` retains a stale doubt result | CLOSED | Spec line 213 explicitly clears the previous outcome, re-renders, and restarts under the current tier policy. |
| edge-cases | F-3 | Ticket grounding was blocked by namespace permissions | DEFERRED | Spec line 278 preserves the limitation; permissions remain unchanged. See F-2 below. |
| edge-cases | F-4 | The persisted operator skip reason has no size bound | DEFERRED | Spec line 279 explicitly retains this optional improvement; line 116 still imposes only non-empty validation. |
| conventions | F-1 | A failed second cycle can become an irreversible completion | CLOSED | Spec lines 155–157 and 211 distinguish failed completion and prevent its reuse for irreversible. |
| conventions | F-2 | Confirm invalidation omits the existing no-grill decision-addition path | CLOSED | Spec line 213 covers the existing branch at `skills/spec-brief/SKILL.md:184`; test-plan line 246 includes it. |

## Findings

### F-1: Restart requires a second cycle that the cycle rule can forbid
**Severity:** P0
**Where:** docs/specs/TODO/VHS-56.spec.md:157; docs/specs/TODO/VHS-56.spec.md:39; docs/specs/TODO/VHS-56.spec.md:211
**Edge case:** A big run changes the draft in cycle 1, fails cycle 2, and upgrades to irreversible. The required fresh restart reviews the already-reconciled draft and returns no actionable findings in its new cycle 1.
**What happens:** Decision 12 requires “both cycles” to complete successfully before continuing. Decision 2 permits cycle 2 only when cycle 1 changes the draft, and Test plan item 5 reiterates that condition. The unchanged restart therefore must either dispatch a forbidden second cycle or halt despite successfully completing every required review.
**Why the spec misses it:** The failure repair correctly prevents reuse of partial completion, but ties recovery to two successful cycles rather than successful completion of the conditional one-or-two-cycle pass. Design 6’s “both required dispatches” wording repeats the ambiguity.
**Suggested fix:** Require every dispatch called for by Decision 2 to complete successfully after the restart. Explicitly allow a clean, unchanged restarted cycle 1 to satisfy irreversible; require successful cycle 2 only when the restarted cycle 1 changes the draft. Add this recovery branch to the test matrix.

### F-2: Ticket grounding remains blocked by namespace permissions
**Severity:** P2
**Where:** docs/specs/TODO/VHS-56.spec.md:278
**Edge case:** The mandatory canonical-ticket lookup uses namespace `skills`, tags `plane_work_item` and `VHS-56`, and source system `plane`.
**What happens:** Shared memory returns `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. This review consequently uses the supplied brief as its ticket-contract authority.
**Why the spec misses it:** This is a review-environment limitation already recorded in the spec, not an implementation defect. The brief explicitly explains that the tracker text predates its scope split.
**Suggested fix:** Preserve the grounding limitation in the review record. No speculative implementation or scope change is needed; independently verify the ticket when an authorized read is available.

## Summary

P0: 1 | P1: 0 | P2: 1 | P3: 0 | P4: 0

Persistence checklist for the new `## Doubt pass` metadata:

- **Atomicity — CHECKED:** Design 6 retains the full-brief temporary-file rename defined at `skills/spec-brief/SKILL.md:218`.
- **Size bound — FLAGGED:** Round-1 edge-cases/F-4 remains explicitly deferred at spec line 279. The operator skip reason is unbounded; other outcome fields have fixed cardinality.
- **Idempotency — CHECKED:** Existing artifact-collision confirmation protects retries; metadata remains within the single brief.
- **Read-side mode filtering — CHECKED:** Decision 4 makes the metadata inert and introduces no production/dev record selection.
- **Schema-version compatibility — CHECKED:** Downstream skills do not consume this section, so older briefs without it remain supported.
- **Concurrent writes — CHECKED:** The inherited write contract documents last-writer-wins and excludes concurrent same-ticket runs at `skills/spec-brief/SKILL.md:220`.

No `## Deferred — follow-up required` section or structured deferred rows are present. The ordinary `## Deferred (P2+)` section records the two advisory follow-ups. External failure axes checked include host metadata, reviewer dispatch and parsing, operator waiting, source availability, ticket retrieval, and final file I/O.

STATUS: RED P0=1 P1=0 P2=1 P3=0 P4=0
