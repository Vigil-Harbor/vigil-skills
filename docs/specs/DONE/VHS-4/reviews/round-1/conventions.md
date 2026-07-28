# Conventions Review -- round 1

## Findings

### F-1: Polling cadence changed from 30s to 15s without explicit acknowledgment
**Severity:** P3
**Suggested fix:** Add note referencing brief Decision 4's authorization.

### F-2: REVIEW_SIGNAL variable style inconsistent with SKILL.md prose convention
**Severity:** P3
**Suggested fix:** Either define it in the preamble alongside FAST_PATH, or replace with prose directives.

### F-3: CLAUDE.md description needs update for fast-path behavior
**Severity:** P2
**Where:** spec.md:12
**Evidence:** CLAUDE.md line 45 says "waits for CodeRabbit's incremental re-review" but VHS-4 sometimes skips the wait. VHS-3 precedent: update CLAUDE.md when behavioral surface changes.
**Suggested fix:** Add CLAUDE.md to scope table with a wording update.

### F-4: `fast-path-skipped` naming is confusing -- reads as "fast path was skipped"
**Severity:** P2
**Where:** spec.md:178, 181
**Suggested fix:** Rename to `fast-path` (parallel to `ci-check`) or `signal-skipped`.

### F-5: D6 enumeration omits `ci-check (FAILURE)`
**Severity:** P4

### F-6: Brief Decision 4 says "keep 30s/5min" but spec preserves 10min extension without noting it
**Severity:** P3

### F-7: PENDING as third check state not flagged as a decision
**Severity:** P3

STATUS: GREEN
