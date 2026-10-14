# Edge-Cases Review — round 5

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:312` and `:316` retain the grounding limitation. Canonical-ticket access remains unavailable; the brief supplies the narrowed contract. |
| edge-cases | F-1 | Canonical-ticket grounding remains unavailable | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:316` explicitly records this process limitation. |
| conventions | F-1 | Keep resolutions without Q identifiers outside the Grill summary grammar | CLOSED | Spec `:239` keeps Q-less resolutions in the candidate and existing seed context; genuine Q-linked items alone amend `prior_summary`. Spec `:241` checks returned decisions for conflicts before updating the candidate. |
| conventions | F-2 | Explicit spec additions need the operator’s drift-check attention | DEFERRED | Spec `:31`–`:39` retains the addition labels and their rationale for the final operator drift check. No design correction was requested. |

The predecessor contains no P0/P1 findings, so the empty closure manifest is complete. Scalability is off. Neither separately saved cross-model directory was treated as a predecessor.

## Findings

### F-1: Canonical-ticket grounding remains unavailable
**Severity:** P2
**Where:** docs/specs/TODO/VHS-56.spec.md:316
**Edge case:** This invocation prohibits network access and declares Plane and shared memory unreachable.
**What happens:** The canonical ticket cannot be independently verified. Review proceeds using the fresh brief, whose Origin documents the operator-approved split and identifies itself as the narrowed contract.
**Why the spec misses it:** This is an existing review-environment limitation, rather than an implementation defect. The required ticket lookup is blocked by the dispatch constraint.
**Suggested fix:** Preserve the limitation in the review record and verify the canonical ticket when authorized access becomes available. No speculative scope change is warranted.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

I read the installed reviewer role in full through a filesystem read. I read the fresh spec, brief, CLAUDE.md, proposed implementation files, relevant source contracts and cited wiki decision. I also read both round-4 and round-5 snapshot bodies for every supplied changed heading, including the deleted report-contract and post-green-polish bodies. The live spec and round-5 snapshot have identical SHA-256 hashes.

New critique stayed within the supplied exclusive heading bodies. Required closure, vanished-reference and deferred-section checks were also performed. Current source anchors resolve; no structured `## Deferred — follow-up required` section is present.

The changed contract handles empty and unreadable returns, readable malformed findings, duplicate identifiers, excessive reports, missing or mismatched reviewer identity, unavailable evidence, dispatch errors, timeout disclosure, retry exhaustion and cycle-2 partial completion. Operator reconciliation retains valid answers, rejects unknown or conflicting replies, preserves candidate edits through resume, and keeps tier changes under the existing tier gate. No blocking failure path was found.

Persistence checklist for the new `## Doubt pass` metadata:

- **Atomicity — CHECKED:** Spec `:243` preserves the complete-brief temporary-sibling rename at `skills/spec-brief/SKILL.md:218`.
- **Size bound — FLAGGED, previously deferred:** Spec `:313` retains the optional bound on free-text skip reasons. Retained finding bodies are capped at seven per cycle; raw reports are excluded from persisted metadata.
- **Idempotency — CHECKED:** Spec `:243` requires exactly one outcome block and preserves the existing artifact-collision confirmation.
- **Read-side mode filtering — CHECKED:** Decision 4 declares audit metadata with no downstream gate; no separate execution-mode records are introduced.
- **Schema compatibility — CHECKED:** No downstream reader requires the new outcome section, so existing briefs remain usable.
- **Concurrent writes — CHECKED:** The retained writer explicitly documents unsupported simultaneous same-ticket runs and last-writer-wins behavior at `skills/spec-brief/SKILL.md:220`.

External failure axes include ticket services, reviewer mechanisms and model runtimes, repository/wiki reads, operator responses and final filesystem writes. The spec distinguishes these failures while preserving the existing mutation boundary. No files or git state were mutated.

STATUS: GREEN
