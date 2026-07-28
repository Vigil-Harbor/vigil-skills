# Conventions Review -- round 2

## Closure table (round 1 findings)

| Finding | Status | Evidence |
|---------|--------|----------|
| R1/F-1: Polling cadence changed without acknowledgment | CLOSED | spec:151 notes brief Decision 4 authorization |
| R1/F-2: REVIEW_SIGNAL variable style inconsistent | CLOSED | spec uses REVIEW_SIGNAL consistently with prose directives |
| R1/F-3: CLAUDE.md needs update for fast-path behavior | CLOSED | spec:12 adds CLAUDE.md to scope table |
| R1/F-4: `fast-path-skipped` naming confusing | CLOSED | spec:128,197,200 renamed to `fast-path` |
| R1/F-5: D6 enumeration omits ci-check (FAILURE) | CLOSED | spec:79 now includes `ci-check (FAILURE)` |
| R1/F-6: Brief Decision 4 / 10min extension mismatch | CLOSED | spec:174 notes 10min extension is preserved behavior |
| R1/F-7: PENDING as third state not flagged as decision | CLOSED | spec:149 documents aggregation rule in design |

## Findings

### F-1: D6 enumeration should stay in sync with design outcomes
**Severity:** P3
**Suggested fix:** If a new signal value is added (e.g., for timeout), update D6 to match.

### F-2: Edge cases section length growing — consider table format in future
**Severity:** P3
**Suggested fix:** Informational — current format is fine for v1.

STATUS: GREEN
