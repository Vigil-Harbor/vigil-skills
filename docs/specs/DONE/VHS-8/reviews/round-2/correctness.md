# Correctness Review — VHS-8 Round 2

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | R1/F-1 | `--force` flag declared but not in phases | CLOSED | Decision 4 line 50: "No `--force` flag" with rationale |
| correctness | R1/F-2 | spec-reconcile warn-and-proceed vs brief's warn-and-halt | CLOSED | Phase 0 step 5 line 109: now halts matching brief |
| correctness | R1/F-3 | Reconciliation filename mismatch | CLOSED | All references now `.reconciliation.md` |
| correctness | R1/F-4 | CLAUDE.md stale heading and intro | CLOSED | Lines 391-394: heading rename + intro rewrite specified |
| correctness | R1/F-5 | `completed_at` not guaranteed | CLOSED | Line 285: 3-tier fallback chain |
| correctness | R1/F-6 | Reconciliation report path assumes TODO/ | CLOSED | Line 142: explicit branch for both paths |
| correctness | R1/F-7 | Stream-of-consciousness in Phase 4 | CLOSED | Clean prose, no "Wait -- actually" |
| correctness | R1/F-8 | ship-spec comparison claim | CLOSED | No inaccurate comparison remains |
| correctness | R1/F-9 | Missing "Invoked as:" convention | CLOSED | Lines 92, 211 |
| correctness | R1/F-10 | Ticket ID parsing rule not specified | CLOSED | Line 105: full parsing rule |

## Findings

### F-1 (P2): Brief companion path hardcoded to TODO/ in spec-reconcile Phase 1

Phase 1 step 3 says "Read the spec's companion brief at `docs/specs/TODO/<TICKET-ID>.brief.md`" but Phase 0 accepts DONE/ paths. If input is a DONE/ spec, the brief path should adapt.

### F-2 (P2): spec-retire allows partial-retire on backlog/unstarted tickets

Brief says "reject if not completed/started respectively." Tickets in `backlog` or `unstarted` groups should halt, not auto-enter partial-retire. Only `started` group should trigger partial-retire.

### F-3 (P2): Reconciliation status-line format diverges from brief without Decision

Brief suggests `RECONCILED: true/false, DRIFT_COUNT: N`. Spec uses `yes/no` and `DRIFT: n`. The format is self-consistent but the departure should be noted in Decision 3.

STATUS: GREEN
