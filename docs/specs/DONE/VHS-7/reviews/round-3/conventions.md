# Conventions Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | R2/F-1 | Scope table replacement counts ambiguous | CLOSED | spec lines 15-16 now use "occurrences" consistently for spec-reconcile and spec-retire |
| conventions | R2/F-2 | Decision 4 rationale well-structured | CLOSED | P3 positive observation; no change needed |
| conventions | R2/F-3 | Test plan step 4 spot-check is manual | CLOSED | P3; acceptable for doc-only change |
| conventions | R2/F-4 | Brief Done-when #6 maps to test command | CLOSED | P3 positive observation |
| conventions | R2/F-5 | Deferred (P2+) section name | CLOSED | P4; not applicable to this spec |
| conventions | R2/F-6 | Windows path backslash rendering | CLOSED | P4; raw markdown is consumption format |
| conventions | R2/F-7 | CLAUDE.md conventions section | CLOSED | P4; CLAUDE.md already uses capability descriptions |
| All R1 findings | | | CLOSED | Confirmed closed in R2 closure table |

## Findings

### F-1: Test command code fence missing `bash` language hint
**Severity:** P4
**Where:** spec.md:156
**Convention violated:** Repo-internal spec convention for test command blocks
**Evidence:** All other VHS specs use ` ```bash ` for their Test command code fence. VHS-7 uses bare ` ``` `.
**Suggested fix:** Change ` ``` ` to ` ```bash `.

### F-2: Test command `&&` and missing grep audit
**Severity:** P3
**Where:** spec.md:157
**Convention violated:** Cross-platform consistency (the spec's own goal) and test-plan/test-command alignment
**Evidence:** `&&` unavailable in PS 5.1; grep audit (test plan step 3) not in test command. Since ship-spec runs in bash and this is doc-only, not load-bearing. A spec about cross-platform compatibility having a platform-specific test command is a self-consistency gap but not blocking.
**Suggested fix:** Note test command expects bash (matching ` ```bash ` convention from F-1), or append grep audit.

### F-3: Decision 4 scope expansion -- correctly documented (c)-class addition
**Severity:** P3
**Where:** spec.md:48-49
**Convention violated:** None -- flagged for drift-check visibility per conventions-review protocol
**Evidence:** Brief's Done-when #1 covers only spec-cycle, ship-spec, and reviewer agents. Decision 4 expands to spec-reconcile, spec-retire, and customizing.md with explicit rationale. Category (c) spec-level addition.
**Suggested fix:** None needed. Flagging for drift-check.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 1

STATUS: GREEN
