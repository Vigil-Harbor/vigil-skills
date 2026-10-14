# Conventions Review — round 5

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:312`, `:314`, and `:317` retain the grounding limitation. This invocation explicitly makes Plane/shared memory unavailable; the brief’s Origin supplies the narrowed contract. |
| edge-cases | F-1 | Canonical-ticket grounding remains unavailable | DEFERRED | Spec line 316 preserves this advisory process limitation. No speculative scope change was made. |
| conventions | F-1 | Keep resolutions without Q identifiers outside the Grill summary grammar | CLOSED | Spec line 239 keeps Q-less resolutions in the candidate and `seed`, outside the summary’s Settled section. Genuine Q-linked items use the existing summary grammar and resume counters. |
| conventions | F-2 | Explicit spec additions need the operator’s drift-check attention | CLOSED | Spec lines 31–39 retain explicit addition labels and rationale. Decision 12 still explains completed-record retention across tier changes at line 178. The updated additions are surfaced below for the human drift check. |

The empty closure manifest matches the predecessor’s absence of P0/P1 findings. Only round-4 reviewer reports were used as closure inputs; scalability is off.

## Findings

### F-1: Label retained operator resolutions as constraints rather than established facts

**Severity:** P2  
**Pre-ship recommended:** yes  
**Where:** docs/specs/TODO/VHS-56.spec.md:239; Test plan item 14 at line 281  
**Convention violated:** The shared interview separates operator decisions from established grounding facts; established facts carry source evidence.  
**Evidence:** Design 6 now passes kept Q-less resolutions “written as established facts,” and the test plan calls this an “established-fact seed.” The live primitive defines `seed` as the problem statement and established grounding facts at `skills/grilling/SKILL.md:18`, gives established facts a `source: <path:line>` at `:148`, and prohibits recording operator claims as established facts at `:159`. The caller maps established facts into References and Scope at `skills/spec-brief/SKILL.md:229`–`:230`. A retained operator decision or replacement acceptance statement has authority as a constraint, but its empirical premises need not have been verified: Decision 8 deliberately permits keeping a decision after unavailable evidence. Calling the entire resolution an established fact blurs that existing distinction.  
**Suggested fix:** Say that Q-less resolutions enter the problem/contract portion of `seed` as explicitly labelled operator-settled constraints. Preserve their authority against automatic re-decision while stating that empirical claims within them retain their verification status and are not promoted into `Facts established` without source evidence. Mirror that terminology in Test plan item 14. Keep the candidate retention, unchanged summary grammar, and returned-conflict prompt.

### F-2: Updated spec additions need the operator’s drift-check attention

**Severity:** P3  
**Where:** docs/specs/TODO/VHS-56.spec.md:31; Decisions 5, 11 and 12 at lines 92, 143 and 173  
**Convention violated:** The conventions review contract requires explicitly justified spec-level additions to be surfaced for the human drift check.  
**Evidence:** The brief authorizes the cross-model pass and leaves its mechanics open. The changed spec explicitly identifies additional positions and now chooses configured/documented model defaults with operator tie-breaking, a content-free identity probe and per-dispatch identity checks, lenient report reading with a fixed seven-finding cap, and an irreversible option to accept reconciled cycle 1 after cycle-2 retry exhaustion. These choices are explained and preserve the brief’s requirement that a cross-model cycle completed, but they materially determine the resulting workflow.  
**Suggested fix:** Include these updated choices in the final drift checklist alongside the existing seven addition groups, particularly the irreversible `Accept cycle 1` outcome and the distinction between readable findings and report-schema compliance. No design change is requested.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

I read the installed conventions reviewer role in full and read both round-4 and round-5 snapshot exclusive bodies for every supplied changed region, including the deleted machine-checkable Decision 11 and Post-green polish section. The current spec matches the round-5 snapshot byte-for-byte.

Fresh grounding covered the spec, brief, CLAUDE.md, AGENTS.md, wiki state and filemap, relevant wiki decisions, and live source contracts. The wiki’s `architecture.md` is absent. Canonical-ticket verification remains unavailable under the declared network restriction, so this review uses the brief’s explicitly narrowed contract.

New critique stayed within the supplied delta scope. Source anchors resolve, and cited implementation files have no diff from the supplied baseline. No structured `## Deferred — follow-up required` section is present. No files or git state were mutated.

STATUS: GREEN
