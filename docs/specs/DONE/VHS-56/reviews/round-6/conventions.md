# Conventions Review — round 6

## Closure of round 5 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Compare family and provider identities at the same level | CLOSED | `docs/specs/TODO/VHS-56.spec.md:92` explicitly compares family with family or provider with provider; absent comparable evidence means unknown identity and ineligibility. |
| correctness | F-2 | ticket not cached | DEFERRED | Spec `:312` retains the canonical-ticket grounding limitation. Network access remains prohibited; the fresh brief’s Origin identifies the narrowed contract. |
| edge-cases | F-1 | Canonical-ticket grounding remains unavailable | DEFERRED | Spec `:312` preserves the process limitation without speculative scope changes. |
| conventions | F-1 | Label retained operator resolutions as constraints rather than established facts | CLOSED | Spec `:239` places kept Q-less resolutions in the problem-statement portion of `seed`, explicitly labels them operator-settled constraints, and preserves empirical verification status. Test plan item 14 at `:281` mirrors the distinction. |
| conventions | F-2 | Updated spec additions need the operator’s drift-check attention | DEFERRED | Spec `:316` retains the advisory for the final human drift checklist. It requests no design change. |

The empty closure manifest matches the predecessor’s absence of P0/P1 findings. Closure inputs were the three standing round-5 reviewer reports; scalability is off. The hand-saved cross-model directories were not treated as numbered predecessor rounds.

## Findings

### F-1: Canonical-ticket grounding remains unavailable

**Severity:** P3  
**Where:** docs/specs/TODO/VHS-56.spec.md:312  
**Convention violated:** Canonical-ticket grounding is degraded; project guidance permits proceeding from the brief when ticket services are unavailable.  
**Evidence:** This invocation explicitly prohibits network access and declares Plane and shared memory unreachable. `AGENTS.md:126` documents ticket reads through shared memory and warn-and-proceed degradation. The freshly read brief’s Origin states that the operator split the original ticket into VHS-56, VHS-66 and VHS-67 and that the brief is the narrowed contract. Independent verification of the current canonical ticket therefore remains unavailable. This is a review-environment limitation, not an implementation defect.  
**Suggested fix:** Preserve the limitation in the review record and verify the canonical ticket when authorized access becomes available. No speculative spec or scope edit is warranted.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

I read the complete installed conventions reviewer definition and freshly read the live spec, brief, CLAUDE.md and AGENTS.md. Grounding covered wiki state, filemap, relevant decisions and live source contracts. The wiki’s `architecture.md` is absent.

The live spec matches the round-6 snapshot byte-for-byte, including at the final check. I read the round-5 exclusive bodies for all four supplied changed headings. New critique stayed within those bodies; closure, deferred-section and vanished-reference checks ran as required.

The revised seed handoff agrees with the live primitive’s separation of operator decisions from sourced grounding facts and with VHS-36’s prohibition on promoting operator claims into established facts. Family/provider comparison preserves the brief’s different-family requirement without adding a vendor lookup table. Current source anchors resolve. No structured `## Deferred — follow-up required` section is present.

No files or git state were mutated.

STATUS: GREEN
