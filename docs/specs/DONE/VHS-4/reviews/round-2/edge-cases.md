# Edge-Cases Review -- round 2

## Closure table (round 1 findings)

| Finding | Status | Evidence |
|---------|--------|----------|
| R1/F-1: Stale SUCCESS on round 2+ re-entry | CLOSED | spec:92-98 adds D8 stale-check guard with PENDING transition requirement |
| R1/F-2: step5_push_succeeded tautological | CLOSED | spec:31 notes defense-in-depth + zero-finding vacuous-truth guard |
| R1/F-3: jq filter returns multiple lines | CLOSED | spec:146 aggregates with conservative rule: any PENDING → PENDING |
| R1/F-4: FIRST_POLL_TIME undefined | CLOSED | spec:151 notes conversational state tracked by LLM |
| R1/F-5: Pre-push APPROVED short-circuit skips 6d | CLOSED | spec:140 explicitly notes this is preserved behavior |
| R1/F-6: 10-minute extension doesn't check reviews-API | CLOSED | spec:174 adds parallel reviews-API check during extension |
| R1/F-7: Zero-finding edge case | CLOSED | spec:31 notes this in D1 |
| R1/F-8: Done-when inconsistent variable name | CLOSED | spec:276 now uses correct variable names |
| R1/F-9: No test for multi-round CI-check | CLOSED | spec:261-262 adds Test 11 for round 2+ check handling |

## Findings

### F-1: jq filter returns `SUCCESS` for empty array, making "no check found" fallback unreachable
**Severity:** P1
**Where:** spec.md:146
**Edge case:** When `gh pr checks` returns no CodeRabbit-named checks, the `select` produces an empty array `[]`. Then `any(. == "PENDING")` on `[]` is `false`, `any(. == "FAILURE")` on `[]` is `false`, so the `else` branch returns `"SUCCESS"`. The skill proceeds as if CodeRabbit completed successfully. The "No CodeRabbit check found after 1 minute" fallback (line 162) is unreachable because the filter never returns a value distinguishable from "check found and succeeded."
**Suggested fix:** Add an empty-array guard at the start of the jq pipeline: `if length == 0 then "NONE" elif any(. == "PENDING") then "PENDING" elif any(. == "FAILURE") then "FAILURE" else "SUCCESS" end`. Then add a `NONE` outcome to the poll logic: treat `NONE` as "no check found" and apply the 1-minute compatibility window.

### F-2: FAILURE path sets `REVIEW_SIGNAL=ci-check` instead of `ci-check (FAILURE)`
**Severity:** P2
**Where:** spec.md:160
**Suggested fix:** Same as correctness F-1 — change to `REVIEW_SIGNAL=ci-check (FAILURE)`.

### F-3: jq filter maps non-standard states (CANCELLED, ERROR, STALE, STARTUP_FAILURE) to SUCCESS
**Severity:** P2
**Where:** spec.md:146
**Edge case:** GitHub checks can have states beyond SUCCESS/FAILURE/PENDING — e.g., CANCELLED, ERROR, STALE, STARTUP_FAILURE. The current `else "SUCCESS"` branch catches all of these as if the check completed successfully.
**Suggested fix:** Invert the logic: `if length == 0 then "NONE" elif any(. == "PENDING") then "PENDING" elif all(. == "SUCCESS") then "SUCCESS" else "FAILURE" end`. This treats any non-SUCCESS, non-PENDING state as FAILURE — conservative and safe.

### F-4: REVIEW_SIGNAL not set on 10-minute PENDING timeout path
**Severity:** P2
**Where:** spec.md:174
**Edge case:** The "still pending after 10 minutes, warn-and-proceed to 6d" path does not set REVIEW_SIGNAL. The 6e report template requires a value for `Review completion signal:`. This path should set something.
**Suggested fix:** Set `REVIEW_SIGNAL=ci-check (timeout)` on this path, and add `ci-check (timeout)` to D6's enumeration and the 6e template.

STATUS: RED P0=0 P1=1 P2=3 P3=0 P4=0
