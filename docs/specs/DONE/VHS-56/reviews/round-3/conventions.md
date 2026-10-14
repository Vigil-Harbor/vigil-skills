# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Recovery requires two successful cycles even when the second is forbidden | CLOSED | `docs/specs/TODO/VHS-56.spec.md:157` and `:211` now require successful completion of only the dispatches Decision 2 requires. An unchanged restarted cycle 1 explicitly completes the pass; Test plan item 4 covers both restart branches. |
| correctness | F-2 | Ticket-only derivation anchor exists only in the ledger | CLOSED | Spec line 174 now carries `skills/spec-brief/SKILL.md:184`; the live source supports the ticket-only derivation claim. |
| correctness | F-3 | Atomic-write anchor exists only in the ledger | CLOSED | Spec line 215 now carries `skills/spec-brief/SKILL.md:218`; the live source defines the temporary-sibling write and rename. |
| correctness | F-4 | General invalidation wording should exempt tier-only changes | CLOSED | Spec line 213 explicitly exempts tier-only changes and directs them to the preceding paragraph. |
| correctness | F-5 | ticket not cached | DEFERRED | Spec line 278 retains the canonical-ticket verification limitation. The brief explicitly identifies itself as the narrowed contract and explains that the tracker text predates the split. |
| edge-cases | F-1 | Restart requires a second cycle that the cycle rule can forbid | CLOSED | Spec lines 157 and 211 preserve Decision 2’s conditional cycle-2 rule during recovery; Test plan item 4 requires the same behavior. |
| edge-cases | F-2 | Ticket grounding remains blocked by namespace permissions | DEFERRED | Spec line 278 preserves the review-environment limitation; no speculative implementation change is claimed. |
| conventions | F-1 | Recovery wording implies an unconditional second cycle | CLOSED | Spec lines 157 and 211 explicitly permit completion after an unchanged restarted cycle 1 and require cycle 2 only after a draft change. |

## Findings

No findings.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 0 | P4: 0

The spec preserves operator ownership of settled decisions, live verification before folding reviewer facts, the existing filesystem-mutation boundary, and the portable capability vocabulary. Its design choices resolve the brief’s stated open questions without expanding the implementation scope.

Current source anchors resolve. No `## Deferred — follow-up required` section is present. The wiki architecture page is absent; grounding used the available state, filemap, relevant decisions, and live source files.

STATUS: GREEN
