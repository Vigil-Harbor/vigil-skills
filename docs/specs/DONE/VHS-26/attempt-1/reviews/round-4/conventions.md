# Conventions Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Terminal addenda cannot always be “checked” | CLOSED | Spec lines 79, 267, and 279 consistently distinguish checker-validated addenda when Python is available from explicitly unvalidated addenda under the unavailable-Python exception. |
| correctness | F-2 | Ticket grounding remains unavailable | PARTIAL | Ticket, shared-memory, and network access remain unavailable; brief line 90 is still the degraded authority. See F-2. |
| correctness | F-3 | Touched review surfaces changed within the last seven days | PARTIAL | HEAD remains `fc20f94`; `fad52c7`, `f64bebe`, and `d3730b1` changed the relevant lifecycle surfaces on 2026-10-12/13. Fresh reads confirm the cited anchors still resolve. See F-3. |
| correctness | F-4 | Review-introduced operational contracts remain implicit in the drift check | PARTIAL | The grouped drift-check note remains absent, and round 4 adds canonical duplicate-section identities and terminal-specific failure messages to the review-introduced contracts. See F-1. |
| edge-cases | F-1 | Duplicate-heading deletion still has no valid tombstone | CLOSED | Spec lines 50–63 define full heading-stack plus occurrence identities on each referenced side; lines 115 and 264 require matching parser validation and duplicate/deletion/rename regressions. |
| edge-cases | F-2 | Terminal gate failures emit a false dispatch message | CLOSED | Spec lines 134–141 define terminal-only messages that report preserved round reports, rollback success or failure, cumulative round, and the actual pending/red marker state; line 267 pins them in tests. |
| edge-cases | F-3 | Ticket lookup remains unavailable | PARTIAL | External ticket grounding remains unavailable; review proceeded from the brief as directed. See F-2. |
| conventions | F-1 | Review-introduced contracts still need drift-check visibility | PARTIAL | The additions remain reasoned category-(c) decisions, but no grouped operator-facing drift-check entry was added. See F-1. |
| conventions | F-2 | Ticket source remains unavailable | PARTIAL | The brief’s same-day tracker record remains the only available authority. See F-2. |
| conventions | F-3 | Review surfaces remain inside the freshness window | PARTIAL | Same-day lifecycle commits remain within seven days, although every inspected symbol and anchor resolves at `fc20f94`. See F-3. |

## Findings

### F-1: Review-introduced contracts remain outside the drift checklist
**Severity:** P3  
**Where:** spec.md:61–63, spec.md:75–79, spec.md:98, spec.md:124–141, spec.md:247  
**Convention violated:** Silent-additions classification; these are category-(c) spec-level additions with rationale  
**Evidence:** The spec reasonably adds canonical full-stack identities, terminal addenda, stale-temp cleanup, resource limits, stable retry ownership, subprocess timeouts, terminal-specific rollback messages, and the post-green runtime-claim prohibition. The live Phase 3 checklist at `skills/spec-cycle/SKILL.md:988-1007` surfaces only brief decisions, Done-when criteria, Out-of-scope fences, and scale, so these beyond-brief contracts are not presented for explicit operator acceptance.  
**Suggested fix:** Add one concise Phase 3 drift-check entry grouping the review-introduced operational contracts, including the round-4 identity and terminal-message additions.

### F-2: Ticket source remains unavailable
**Severity:** P3  
**Where:** brief.md:90  
**Convention violated:** Ticket-grounding fallback  
**Evidence:** Ticket, shared-memory, and network access are unavailable for this pass. The brief records a direct tracker read dated 2026-10-13 and therefore remains the degraded authority.  
**Suggested fix:** Re-run ticket grounding before implementation if the canonical ticket may have changed.

### F-3: Review surfaces remain inside the freshness window
**Severity:** P3  
**Where:** spec § Scope  
**Convention violated:** Fresh grounding for recently changed lifecycle contracts  
**Evidence:** Read-only history shows `fad52c7` and `f64bebe` on 2026-10-13 and `d3730b1` on 2026-10-12 touching `/spec-cycle`, reviewer contracts, workflow documentation, or AGENTS.md. Fresh inspection at HEAD `fc20f94` confirms the cited `sync.py` and `skills/spec-cycle/SKILL.md` symbols still resolve.  
**Suggested fix:** Immediately before implementation, re-check artifact ordering, terminal-addendum insertion points, duplicate-heading identity derivation, reviewer inputs, and divergence handling.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 3 | P4: 0

STATUS: GREEN
