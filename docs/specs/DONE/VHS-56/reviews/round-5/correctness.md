# Correctness Review — round 5

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | DEFERRED | Spec lines 312 and 316 preserve the canonical-ticket grounding limitation. This invocation still has no network access; the brief supplies the documented narrowed contract. |
| edge-cases | F-1 | Canonical-ticket grounding remains unavailable | DEFERRED | Spec line 316 explicitly retains this advisory process limitation. |
| conventions | F-1 | Keep resolutions without Q identifiers outside the Grill summary grammar | CLOSED | Spec line 239 retains Q-less resolutions in the candidate and seed, outside the summary’s Settled section. Q-linked reopens use the existing Open frontier shape at `skills/grilling/SKILL.md:143`. |
| conventions | F-2 | Explicit spec additions need the operator’s drift-check attention | CLOSED | Spec lines 31–39 retain the explicit addition labels and their rationale. These positions remain available for the orchestrator’s final drift checklist. |

All three predecessor reports have parseable green STATUS lines and no P0/P1 findings. The empty closure manifest is complete. Scalability is off. The hand-saved cross-model directories were not treated as predecessor rounds.

## Findings

### F-1: Compare family and provider identities at the same level

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** docs/specs/TODO/VHS-56.spec.md:92
**Claim:** “Its own provider/vendor statement counts as its family … Compare trimmed, case-insensitive family values with the author’s self-reported family.”
**Why this is wrong:** The accepted identity evidence includes both family names and provider names, but the comparison does not explicitly require matching kinds of identity. A reviewer’s provider label and the author’s model-family label can differ while identifying the same family. String inequality alone then fails to establish the different-family requirement carried by the brief’s Decision 2 and its prohibition on a same-model fallback. A careful implementation can resolve this correctly, so this is a clarification rather than a shipping blocker.
**Suggested fix:** Require like-for-like comparison: compare declared family names with the author’s family, or a declared provider with the author’s self-reported provider. When comparable identity evidence cannot be established, treat identity as unknown and the mechanism as ineligible. This needs no vendor lookup table.

### F-2: ticket not cached

**Severity:** P3
**Where:** docs/specs/TODO/VHS-56.spec.md:316
**Claim:** “Canonical-ticket grounding remains unavailable under this invocation’s declared network outage.”
**Why this is wrong:** Independent canonical-ticket verification cannot be completed under the dispatch’s explicit no-network constraint. This is a review-environment limitation, not an implementation defect. The live brief’s Origin documents the operator-approved split into VHS-56, VHS-66 and VHS-67 and identifies itself as the narrowed contract.
**Suggested fix:** Preserve the limitation in the review record and verify the canonical ticket when authorized access becomes available. No speculative scope change is warranted.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

I obtained and read the installed correctness reviewer role in full. I freshly read the live spec, brief, project instructions, all three round-4 reports, the round-5 ledger, and both snapshot bodies for every supplied changed heading and deletion. The live spec and round-5 snapshot have matching SHA-256 hashes.

Source grounding verified the cited spec-brief flow, grilling input/resume/output contracts, portability capability vocabulary, downstream brief parser, public summaries and relevant wiki decisions. Current anchors resolve. The deleted strict-report section is replaced by the lenient contract; removing Post-green polish does not remove its Q-less serialization correction.

The explicit consistency walk checked held-candidate preservation, settled-target precedence, fixed finding caps, report transport and lenient reading, identity checks, retry/cycle bounds, irreversible acceptance conditions, tier and Scale routes, outcome counts, resume metadata, exact-preview writes and phase renumbering. The brief’s acceptance criteria remain covered.

The ground-truth ledger contains the required round-5 no-runtime-claims declaration and has no claim rows or omission boundary. No structured `## Deferred — follow-up required` section exists.

Touched-file history includes recent commits `5f640d0` (2026-10-11) and `33b9215` (2026-10-13); verification used current files. No files or git state were changed.

STATUS: GREEN
