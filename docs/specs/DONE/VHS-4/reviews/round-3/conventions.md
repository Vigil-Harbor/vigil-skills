# Conventions Review -- round 3

## Closure table (round 2 findings)

| Finding | Status | Evidence |
|---------|--------|----------|
| R2/F-1: D6 enumeration should stay in sync | CLOSED | D6 line 79 now includes all six signal values including ci-check (timeout) |
| R2/F-2: Edge cases section length — table format | CLOSED | Informational; prose format fine for v1 |

## Findings

### F-1: D7 and D8 are spec-level additions with rationale
**Severity:** P3
**Where:** spec.md:85-99
**Note:** D7 derived from brief Risk 3, D8 is a spec-level race condition discovery. Both carry explicit rationale. Category (c) — spec-level additions. No change needed; flagging for human drift-check.

### F-2: Brief Decision 5 enumerates three signal values; spec D6 enumerates six
**Severity:** P3
**Where:** spec.md:79 vs brief.md:58
**Note:** Three additions (ci-check (FAILURE), ci-check (timeout), fast-path) are necessary consequences of D7, timeout path, and D1. Category (c) — spec-level extension of brief decision.

STATUS: GREEN
