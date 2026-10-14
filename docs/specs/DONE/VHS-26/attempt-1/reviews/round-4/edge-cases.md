# Edge-Cases Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Terminal addenda cannot always be “checked” | CLOSED | Spec lines 79, 267, and 279 consistently distinguish checker-validated addenda from the unavailable-Python exception. |
| correctness | F-2 | Ticket grounding remains unavailable | PARTIAL | Ticket/shared-memory/network access remains unavailable; review used brief line 90 as degraded authority. See F-2. |
| correctness | F-3 | Touched review surfaces changed within the last seven days | PARTIAL | Baseline remains `fc20f94`; recent commits `fad52c7`, `f64bebe`, and `d3730b1` still place these surfaces inside the freshness window. Fresh reads found no current anchor drift. See F-4. |
| correctness | F-4 | Review-introduced operational contracts remain implicit in the drift check | PARTIAL | The spec still lacks the requested grouped drift-check note. See F-3. |
| edge-cases | F-1 | Duplicate-heading deletion still has no valid tombstone | NEW | Full-stack-plus-occurrence identities fix duplicate headings at spec lines 61–63 and 115, but the live algorithm also emits `(before first heading)`, which the non-empty heading-stack grammar cannot encode. See F-1. |
| edge-cases | F-2 | Terminal gate failures emit a false dispatch message | CLOSED | Spec lines 134–141 define terminal-specific repeated-failure and timeout messages naming preserved reports, rollback outcome, round, and actual marker state; line 267 pins them in tests. |
| edge-cases | F-3 | Ticket lookup remains unavailable | PARTIAL | The external ticket source remains unavailable. See F-2. |
| conventions | F-1 | Review-introduced contracts still need drift-check visibility | PARTIAL | No grouped operator-facing drift-check note was added. See F-3. |
| conventions | F-2 | Ticket source remains unavailable | PARTIAL | The brief remains the degraded authority. See F-2. |
| conventions | F-3 | Review surfaces remain inside the freshness window | PARTIAL | The same recent commits remain within seven days; live anchors currently resolve. See F-4. |

## Findings

### F-1: Before-first-heading changes have no ledger identity
**Severity:** P0  
**Where:** spec.md:61-63, spec.md:115; `skills/spec-cycle/SKILL.md:480`  
**Edge case:** A valid spec gains, changes, or removes bytes before its first Markdown heading—for example an HTML comment or UTF-8 BOM.  
**What happens:** The live changed-regions algorithm emits `(before first heading)`, so `expected_ground_truth_coverage` must contain that identity. The ledger grammar permits only JSON identities with a non-empty heading `stack`, and the checker requires them to resolve through its heading scan. The author cannot encode the expected set: an invented identity fails checker validation, while omitting it or using `no spec sections` fails the correctness comparison. A valid revision therefore cannot pass the author gate. BOM handling can additionally make the orchestrator and checker derive different heading stacks if only the checker strips it.  
**Why the spec misses it:** Decision 3 claims to represent the exact identity set from the existing algorithm, but defines identities only for headings. Test-plan item 6 covers duplicate/deleted/renamed headings, not the algorithm’s special pre-heading region or consistent BOM normalization.  
**Suggested fix:** Define a canonical identity for `(before first heading)` and accept it in coverage and `Spec locations`, or explicitly exclude that region from both expected coverage and runtime-claim placement. Normalize an optional BOM identically before both heading scans. Add insert/change/delete pre-heading and BOM regressions.

### F-2: Ticket lookup remains unavailable
**Severity:** P3  
**Where:** brief.md:90  
**Edge case:** Ticket/shared-memory/network access is unavailable during the final review pass.  
**What happens:** Current Plane contents and acceptance criteria cannot be independently verified; this review relies on the brief’s recorded tracker read.  
**Why the spec misses it:** This is an environmental grounding limitation, not a design defect.  
**Suggested fix:** Re-run ticket grounding before implementation if the canonical ticket may have changed.

### F-3: Review-introduced contracts remain absent from the drift check
**Severity:** P3  
**Where:** spec § Decision 4; § Decision 5; § Decision 7; § Revision and synthesis integration  
**Edge case:** The operator reaches the Phase 3 hard stop after reviewers introduced tombstones, terminal addenda, stale-temp cleanup, resource bounds, rollback messages, and post-green restrictions beyond the brief.  
**What happens:** Those additions are not grouped for explicit operator acceptance, so the drift check can pass without surfacing the accumulated operational expansion.  
**Why the spec misses it:** The requested grouped drift-check note remains absent.  
**Suggested fix:** Add one concise drift-check item enumerating the review-introduced operational contracts.

### F-4: Recently changed integration surfaces require implementation-time rereading
**Severity:** P3  
**Where:** spec § Scope  
**Edge case:** Implementation starts after further changes land on the recently modified spec-cycle and reviewer surfaces.  
**What happens:** Artifact ordering, delta coverage, terminal revision, or divergence assumptions could become stale. Current reads show no drift, but the surfaces remain inside the freshness window.  
**Why the spec misses it:** This is a timing risk rather than a current contradiction.  
**Suggested fix:** Re-read the named integration points immediately before implementation.

## Summary

Persistence checks: atomic ledger/addendum finalization, bounds, retry behavior, current-round read isolation, immutable schema lifetime, and unsupported same-spec concurrency are specified. F-1 flags the remaining persisted-ledger identity state that cannot be represented.

P0: 1 | P1: 0 | P2: 0 | P3: 3 | P4: 0

STATUS: RED P0=1 P1=0 P2=0 P3=3 P4=0
