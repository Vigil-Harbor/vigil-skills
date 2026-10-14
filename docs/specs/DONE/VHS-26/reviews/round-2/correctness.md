# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | PARTIAL | Shared memory remains unavailable; review again proceeded from the brief. Re-filed below as current F-1. |
| correctness | F-2 | Recently changed implementation surfaces | CLOSED | Fresh reads confirm the cited symbols still resolve at `skills/spec-cycle/SKILL.md:384`, `:444`, `:462`, `:511`, and `:706`; both reviewer headings and the documentation anchors also remain live. Recent commits are surfaced by this closure row. |
| edge-cases | F-1 | Later full passes cannot distinguish new claims from untouched claims | CLOSED | `Coverage:` now declares `full spec (new)`, edited headings, or `none`; Decision 8 bounds omission checking to that declaration and checks it against closure/current-spec evidence without invoking changed-regions machinery (`spec.md:49-59`, `spec.md:99-106`, `spec.md:136`). |
| edge-cases | F-2 | Post-green polish bypasses author grounding | DEFERRED | D-1 is well-formed, has the required preamble and seven fields, names three existing propagation sites, and records the root as out of scope under the brief’s absent §2g scope row (`spec.md:189-202`). |
| edge-cases | F-3 | An empty ledger silently satisfies the only enforcement path | CLOSED | Decision 8 now treats zero-length, missing-coverage, and contentless ledgers as the same P0 as a missing ledger; the manual checklist covers these cases (`spec.md:99-104`, `spec.md:153`). |
| conventions | F-1 | Author-pinned enforcement choices need explicit provenance labels | PARTIAL | Decisions 4, 5, and 8 retain their rationale, but still do not explicitly identify themselves as author-pinned resolutions of brief Risks / decisions items 2–5 (`spec.md:40-71`, `spec.md:89-106`). Re-filed below as current F-2. |

## Findings

### F-1: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec is authored from the VHS-26 brief and ticket context.
**Why this is wrong:** The MCP shared-memory service remains unavailable, so the canonical Plane ticket could not be retrieved. Per the reviewer contract, this pass proceeded from `docs/specs/TODO/VHS-26.brief.md`.
**Suggested fix:** No spec change is required unless the live ticket later conflicts with the brief; recheck it when shared memory becomes available.

### F-2: Author-pinned enforcement choices still lack explicit provenance labels
**Severity:** P3
**Where:** spec § Decision 4; spec § Decision 5; spec § Decision 8
**Claim:** The spec pins the ledger filename and shape, warn-and-dispatch behavior, sample size, and finding severities with rationale.
**Why this is wrong:** Those are valid spec-level choices delegated by brief Risks / decisions items 2–5, but the Decisions still do not explicitly label that provenance. The design remains correct; the omission only weakens the later human drift-check.
**Suggested fix:** Label Decisions 4, 5, and 8 as author-pinned resolutions of the corresponding brief risk items.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 0

STATUS: GREEN
