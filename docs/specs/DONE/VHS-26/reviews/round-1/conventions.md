# Conventions Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: Author-pinned enforcement choices need explicit provenance labels
**Severity:** P3  
**Where:** spec.md:40; spec.md:59; spec.md:87  
**Convention violated:** Silent-addition audit, category (c): spec-level additions with rationale should remain visible for the human drift-check.  
**Evidence:** The brief’s `## Risks / decisions` delegates the ledger filename and incomplete-artifact behavior, sample size and severities, and review checklist to the spec author. The spec reasonably pins these as `ground-truth-ledger.md`, warn-and-dispatch without baseline incompleteness, a deterministic five-row maximum, and P0/P1 enforcement, with rationale.  
**Suggested fix:** Label Decisions 4, 5, and 8 as author-pinned resolutions of the corresponding brief risk items so the Phase 3 drift-check can confirm those choices directly. No design change is required.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
