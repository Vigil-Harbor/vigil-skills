# Edge-Cases Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:310` and `:312` retain the review-environment limitation. This dispatch explicitly declares ticket/shared-memory access unavailable; the brief supplies the narrowed contract. |
| edge-cases | F-1 | Ticket grounding remains blocked by namespace permissions | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:310` retains the limitation. Canonical-ticket verification remains unavailable under this dispatch’s network constraint. |
| conventions | — | No round-3 findings | CLOSED | The predecessor conventions report contains no findings. |

The predecessor has no open P0/P1 findings. The empty closure manifest matches its reports. Scalability is off; no scalability report was used.

## Findings

### F-1: Canonical-ticket grounding remains unavailable
**Severity:** P2
**Where:** docs/specs/TODO/VHS-56.spec.md:310
**Edge case:** This review session explicitly has no network access; Plane and shared memory are unavailable.
**What happens:** The canonical ticket cannot be independently verified. Review proceeds using the live brief, whose Origin explicitly documents the operator-approved split and identifies itself as the narrowed contract.
**Why the spec misses it:** This is a review-environment limitation already recorded in the spec, rather than an implementation defect. No network lookup was attempted under the dispatch constraint.
**Suggested fix:** Preserve this limitation in the review record and verify the canonical ticket when authorized access becomes available. No speculative spec or scope change is warranted.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

Fresh grounding covered the spec, brief, project instructions, proposed implementation files, cited control-flow anchors, all three predecessor reports, and the four deleted heading bodies in the predecessor snapshot. Current source anchors resolve. No `## Deferred — follow-up required` section or structured deferred rows are present.

Within the declared delta scope, the review checked empty, malformed, truncated and excessive reviewer reports; missing model or mode evidence; unavailable and stalled dispatches; retry exhaustion; incomplete contradiction answers; overlapping replacements; retained-candidate revisions; tier transitions; and cycle-2 partial failure. No blocking failure path was found. The removal of the previous recovery rule is deliberate and explained in Decision 12.

Persistence checklist for `## Doubt pass` metadata:

- **Atomicity — CHECKED:** Spec line 242 preserves the full-brief temporary-sibling rename defined at `skills/spec-brief/SKILL.md:218`.
- **Size bound — FLAGGED, previously deferred:** Spec line 311 retains the optional bound on free-text skip reasons. Finding counts are bounded by `question_cap`, and raw reports are excluded from persisted metadata.
- **Idempotency — CHECKED:** Spec line 242 requires exactly one outcome block and preserves the existing artifact-collision confirmation.
- **Read-side mode filtering — CHECKED:** Decision 4 declares the metadata inert; no additional read-side mode is introduced.
- **Schema compatibility — CHECKED:** No downstream gate consumes the new outcome record, so older briefs remain usable.
- **Concurrent writes — CHECKED:** The retained write mechanism explicitly documents unsupported simultaneous same-ticket runs and last-writer-wins behavior at `skills/spec-brief/SKILL.md:220`.

External failure axes are the optional ticket services, selected reviewer mechanism/model runtime, repository/wiki reads, operator responses, and final filesystem write. The revised contract distinguishes dispatch failure, unavailable evidence, explicit skip and abort while preserving the existing mutation boundary.

STATUS: GREEN
