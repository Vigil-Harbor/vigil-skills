# Edge-Cases Review — round 6

## Closure of round 5 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Compare family and provider identities at the same level | CLOSED | `docs/specs/TODO/VHS-56.spec.md:92` requires like-for-like identity comparison and treats a missing comparable pair as unknown and ineligible. |
| correctness | F-2 | ticket not cached | DEFERRED | Spec `:312` retains the grounding limitation. This invocation prohibits network access; the brief’s Origin supplies the narrowed contract. |
| edge-cases | F-1 | Canonical-ticket grounding remains unavailable | DEFERRED | Spec `:312` retains this process limitation; canonical-ticket access remains unavailable. |
| conventions | F-1 | Label retained operator resolutions as constraints rather than established facts | CLOSED | Spec `:239` passes Q-less resolutions as labelled operator-settled constraints, preserves empirical verification status, and forbids promoting them into established facts. Test plan item 14 at `:281` mirrors the correction. |
| conventions | F-2 | Updated spec additions need the operator’s drift-check attention | DEFERRED | Spec `:316` retains the advisory for the final human drift checklist; the addition labels and rationale remain at `:31`–`:39`. |

All three predecessor reports are green and contain no P0/P1 findings, so the empty closure manifest is complete. Scalability is off. The hand-saved cross-model reports were not treated as numbered predecessors.

## Findings

### F-1: Canonical-ticket grounding remains unavailable
**Severity:** P2
**Where:** docs/specs/TODO/VHS-56.spec.md:312
**Edge case:** This invocation prohibits network access and declares Plane and shared memory unreachable.
**What happens:** The canonical ticket cannot be independently verified. Review proceeds using the fresh brief, whose Origin documents the operator-approved split and identifies itself as the narrowed contract.
**Why the spec misses it:** This is a review-environment limitation, not an implementation defect. The mandatory ticket-grounding step is blocked by the dispatch constraint.
**Suggested fix:** Preserve this limitation in the review record and verify the canonical ticket when authorized access becomes available. No speculative scope change is warranted.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

I read the full installed reviewer definition, fresh live spec and brief, project instructions, proposed implementation files, relevant source contracts and cited wiki decision. The live spec and round-6 snapshot have matching SHA-256 hashes. I read both snapshot bodies for every supplied changed heading and only the round-5 standing reviewer reports as closure inputs.

New critique stayed within the supplied exclusive heading bodies. Required closure, vanished-reference and deferred-section checks were also performed. Source anchors resolve. No structured `## Deferred — follow-up required` section is present.

The scoped checks covered missing or incomparable identities, identity drift, read-only eligibility, unavailable mechanisms, resume conflicts, preserved candidate state, tier changes, partial review disclosure and malformed operator replies. Q-less constraints retain their authority without entering the established-facts mapping. The test matrix covers the relevant failure paths. No blocking edge was found.

Persistence checklist for the new `## Doubt pass` metadata:

- **Atomicity — CHECKED:** Spec `:243` retains the complete-brief temporary-sibling rename at `skills/spec-brief/SKILL.md:218`.
- **Size bound — FLAGGED, previously deferred:** Spec `:313` retains the optional bound on free-text skip reasons. Raw reviewer reports are excluded from persisted metadata.
- **Idempotency — CHECKED:** Spec `:243` requires exactly one outcome block and preserves the existing artifact-collision confirmation.
- **Read-side mode filtering — CHECKED:** Decision 4 defines audit metadata with no downstream gate; no separate execution-mode records are introduced.
- **Schema compatibility — CHECKED:** The downstream brief parser reads its existing named sections; the outcome block is optional for existing briefs.
- **Concurrent writes — CHECKED:** The retained writer documents unsupported simultaneous same-ticket runs and last-writer-wins behavior at `skills/spec-brief/SKILL.md:220`.

External failure axes include ticket services, reviewer mechanisms and model runtimes, repository/wiki reads, operator responses and final filesystem writes. No files or git state were mutated.

STATUS: GREEN
