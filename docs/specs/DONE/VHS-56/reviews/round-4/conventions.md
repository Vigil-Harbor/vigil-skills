# Conventions Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:310` preserves the limitation. Network and ticket-cache access are unavailable in this review session; the brief’s Origin explicitly establishes the narrowed contract. |
| edge-cases | F-1 | Ticket grounding remains blocked by namespace permissions | DEFERRED | `docs/specs/TODO/VHS-56.spec.md:310` and `:312` retain the process limitation. Independent ticket verification remains unavailable; no speculative scope change is warranted. |

The round-3 conventions report contained no findings. The closure manifest contains no predecessor P0/P1 dispositions.

## Findings

### F-1: Keep resolutions without Q identifiers outside the Grill summary grammar
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** docs/specs/TODO/VHS-56.spec.md:238
**Convention violated:** The shared `grilling` hand-off associates every Settled decision with its originating question; callers preserve that contract.
**Evidence:** Design 6 requires ticket decisions and replacement acceptance statements without a Q identifier to be “included as labelled amended Settled items,” while prohibiting invented Q numbers. The live primitive defines `prior_summary` as an earlier Grill summary at `skills/grilling/SKILL.md:21`, rebuilds its decision tree under the resume contract at `:23`, and requires `(Q<n>)` on every Settled output item at `:140`. The wiki’s `decisions/2026-09-07-vhs-33-the-hand-off-carries-ids-and-a-hollow-brief-is-a-success.md:55` explicitly states: “Every Settled line is `(Q<n>)`; the question is the only parent.” The preservation goal is sound, but the proposed representation extends the shared grammar while claiming to use its existing contract.
**Suggested fix:** Amend genuine Q-linked items within `prior_summary`. Keep resolutions without Q identifiers in the authoritative candidate and supply them as separately labelled operator constraints in the existing `seed` context, outside the Grill summary’s Settled section. State how those constraints survive the returned summary and how an explicit revised decision may reopen them. Preserve the unchanged summary grammar and resume counters.

### F-2: Explicit spec additions need the operator’s drift-check attention
**Severity:** P3
**Where:** docs/specs/TODO/VHS-56.spec.md:31
**Convention violated:** The conventions review contract requires explicitly justified spec-level additions to be surfaced as P3 for the human drift check.
**Evidence:** The brief’s Scope and Risks / decisions authorize the doubt pass and leave its mechanics open. The spec explicitly identifies additional positions at lines 33–39: full-candidate preview; completed-pass records and cumulative counts; explicit Abort choices; deterministic read-only eligibility, report validation and retries; furthest-completed-state handling; early irreversible eligibility checks and preserved upgrade work; and candidate retention with amended resume context. These additions have stated rationale. Decision 12 at line 177 also expressly replaces the earlier recovery rule rather than silently preserving it.
**Suggested fix:** Retain these addition labels and include the seven positions in the final drift checklist, particularly completed at-cap outcomes retained through tier-only upgrades. No design change is requested.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

Fresh grounding covered the live spec, brief, CLAUDE.md, AGENTS.md, available wiki state and filemap, relevant decisions, current skill contracts and source anchors. The wiki has no `architecture.md`. Canonical-ticket verification was unavailable under the session’s network constraint, so the review used the brief’s explicitly narrowed contract.

New critique was limited to the supplied delta regions. Deleted sections were checked in round 3’s `spec.copy.md`; their replacements retain the relevant tier and dispatch behavior. No dead source references or structured `## Deferred — follow-up required` section were found. No files or git state were changed.

STATUS: GREEN
