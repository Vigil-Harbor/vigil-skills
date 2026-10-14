# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: Later full passes cannot distinguish new claims from untouched claims
**Severity:** P1  
**Where:** spec.md:55-57; spec.md:95-102  
**Edge case:** A full round after round 1 revises only part of the spec, and a newly authored runtime-behavior claim is omitted from that round’s ledger while older, untouched runtime claims remain elsewhere in the spec.  
**What happens:** The correctness reviewer has no defined provenance for deciding which unlisted claims were authored or revised for this dispatch. Treating every unlisted claim as an omission falsely blocks untouched claims and violates the no-backfill rule; checking only listed rows silently misses the newly omitted claim.  
**Why the spec misses it:** Full-mode prompts do not carry `changed_regions`, the closure manifest does not record P2 edits or exact changed claims, and the spec expressly forbids a computed expected-coverage inventory. Nevertheless, Decision 8 requires the reviewer to file P1 for an authored-or-revised claim with no row without defining how that state is observable.  
**Suggested fix:** Pin a review-visible provenance rule that lets correctness identify the claims eligible for omission checking on later full rounds, or explicitly route this omission-enforcement requirement to the excluded VHS-61 machinery rather than claiming it is enforceable here. Do not widen this ticket into the excluded changed-regions/ledger coupling.

### F-2: Post-green polish bypasses author grounding
**Severity:** P1  
**Where:** spec.md:69; spec.md:71-81; spec.md:122-126  
**Edge case:** A green round contains a pre-ship-recommended P2 that supplies a changed `file:line` anchor, error-message assertion, or other factual runtime wording, and post-green polish applies it.  
**What happens:** Reviewer-supplied facts can be embedded after the last review without a fresh live-source verification or consumer re-read; the polished bytes are then fingerprinted as green and can proceed to `/ship-spec`. This recreates the failure mode the brief requires every revision to prevent.  
**Why the spec misses it:** Decision 6 explicitly applies the verify–compose–edit–re-read operation to ordinary revision, delta pass 2, and final FROZEN/REWRITE, but not to the existing post-green polish path at `skills/spec-cycle/SKILL.md:939-970`. Decision 5 correctly forbids a ledger/addendum for polish, but that fence does not forbid live verification before the polish edit.  
**Suggested fix:** Require post-green polish to live-verify any factual claim or anchor it applies, compose overlapping candidates, and re-read affected consumers, while preserving the brief’s explicit rule that polish produces no ledger/addendum and no new review round.

### F-3: An empty ledger silently satisfies the only enforcement path
**Severity:** P1  
**Where:** spec.md:55; spec.md:63-67; spec.md:95-102  
**Edge case:** `ground-truth-ledger.md` exists and is readable but is zero-length or contains neither a recognizable claim row nor the exact no-runtime-claims line.  
**What happens:** The “missing or unreadable” P0 does not apply, there are no rows to sample, and—when the reviewed changes genuinely contain no runtime claims—the omission check finds nothing. The round can go green without the explicit no-claims evidence required by Decision 4 and Done when item 1.  
**Why the spec misses it:** Decision 8 defines missing/unreadable files, contradicted no-claims declarations, sampled rows, dead anchors, unsupported anchors, and uncovered runtime claims, but gives no result for a readable ledger with no usable content. The test plan likewise exercises a missing ledger but not an empty or contentless one.  
**Suggested fix:** In the correctness-agent contract, treat a readable ledger containing neither at least one human-recognizable row nor the exact no-claims declaration as `ground-truth ledger missing` (P0), and add that case to the manual checklist. This remains a human-review rule, not the excluded machine-checked grammar.

## Summary

P0: 0 | P1: 3 | P2: 0 | P3: 0 | P4: 0

STATUS: RED P0=0 P1=3 P2=0 P3=0 P4=0
