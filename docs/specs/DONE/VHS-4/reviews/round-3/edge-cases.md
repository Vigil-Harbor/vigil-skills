# Edge-Cases Review -- round 3

## Closure table (round 2 findings)

| Finding | Status | Evidence |
|---------|--------|----------|
| R2/F-1: jq filter returns SUCCESS for empty array | CLOSED | spec:146 now has `if length == 0 then "NONE"` guard |
| R2/F-2: FAILURE path REVIEW_SIGNAL mismatch | CLOSED | spec:160 now reads `ci-check (FAILURE)` |
| R2/F-3: jq maps non-standard states to SUCCESS | CLOSED | spec:146 uses `all(. == "SUCCESS") then "SUCCESS" else "FAILURE"` |
| R2/F-4: REVIEW_SIGNAL not set on 10-minute PENDING timeout | CLOSED | spec:174 sets `REVIEW_SIGNAL=ci-check (timeout)` |

## Findings

### F-1: Zero-finding path composition with fast-path predicate
**Severity:** P3
**Where:** spec.md:29-31, 126-128
**Edge case:** Zero findings from round 1 — "no fixes were pushed" gate at line 126 fires before fast-path is evaluated. Correct behavior, documentation gap only.
**Suggested fix:** Optionally add one-line note to edge cases.

### F-2: reviews-API fallback sets REVIEW_SIGNAL before review is detected
**Severity:** P2
**Where:** spec.md:162
**Edge case:** `REVIEW_SIGNAL=reviews-api-fallback` is set at fallback entry, not after review detection. Timeout and success produce the same signal. Compare with CI-check path which distinguishes success/failure/timeout.
**Suggested fix:** Add `reviews-api-fallback (timeout)` signal for the fallback timeout case.

### F-3: Re-entry guard FIRST_POLL_TIME not reset on round 2+ re-entry
**Severity:** P2
**Where:** spec.md:176
**Edge case:** If FIRST_POLL_TIME is not reset on re-entry from 6b, the "remaining time" calculation yields near-zero, making the fallback effectively a no-op.
**Suggested fix:** Add note: "Reset FIRST_POLL_TIME at the start of each re-entry to 6a from 6b."

### F-4: PUSH_TIME is conversational state but not documented as such
**Severity:** P2
**Where:** spec.md:133-135, 166
**Edge case:** FIRST_POLL_TIME is documented as conversational state (line 151) but PUSH_TIME is not. Separate Bash calls referencing $PUSH_TIME would get empty string.
**Suggested fix:** Add clarification parallel to the FIRST_POLL_TIME note.

### F-5: PENDING transition missed due to polling granularity
**Severity:** P3
**Where:** spec.md:96, 176
**Edge case:** If CodeRabbit completes in under 15s, SUCCESS → PENDING → SUCCESS between polls. Guard waits full 1-minute, then falls back. Graceful degradation.
**Suggested fix:** No change required — optionally note the possibility.

### F-6: ISO timestamp comparison assumes same format
**Severity:** P3
**Where:** spec.md:137-140
**Edge case:** Lexicographic ISO comparison correct as long as both use Z suffix. Theoretical if GitHub returns +00:00 offset.
**Suggested fix:** No change required — existing SKILL.md has same pattern.

### F-7: `gh pr checks` field name may differ across gh CLI versions
**Severity:** P2
**Where:** spec.md:145-146
**Edge case:** Older/newer gh versions may use `conclusion`+`status` instead of `state`. Null values would route to FAILURE via conservative catch-all.
**Suggested fix:** Add defensive jq fallback: `.state // .conclusion // "UNKNOWN"`, or pin gh CLI version.

STATUS: GREEN
