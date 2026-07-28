# Edge-Cases Review -- round 1

## Findings

### F-1: CI-check gate on round 2+ re-entry sees stale SUCCESS from prior round
**Severity:** P1
**Where:** spec.md:139-159 and spec.md:170
**Edge case:** 6b loops back to 6a after a round-2 push. The CodeRabbit CI check from round 1 still shows SUCCESS. The new check for round 2 has not yet registered. The CI-check gate immediately declares the incremental review complete using the stale SUCCESS.
**Suggested fix:** Add a temporal guard: after 6b pushes and loops back, wait for the check to transition through PENDING (indicating new run started) before gating on SUCCESS. If it never transitions within the 1-minute window, fall back to reviews-API.

### F-2: Fast-path predicate `step5_push_succeeded` is tautological given the other two conditions
**Severity:** P4
**Suggested fix:** Add parenthetical to D1 noting this is defense-in-depth + guards the zero-finding vacuous-truth case.

### F-3: jq filter returns multiple lines when multiple CodeRabbit checks exist
**Severity:** P2
**Where:** spec.md:135-137
**Suggested fix:** Aggregate with a conservative rule: if any check is PENDING, treat as PENDING.

### F-4: FIRST_POLL_TIME is undefined -- no mechanism to capture wall clock persistently
**Severity:** P2
**Where:** spec.md:139, 150
**Suggested fix:** Add note that FIRST_POLL_TIME is conversational state (LLM tracks it), not a shell variable.

### F-5: Pre-push APPROVED short-circuit skips 6d but fast path goes to 6d -- observability gap
**Severity:** P2
**Suggested fix:** Add note that this is preserved from current SKILL.md behavior.

### F-6: 10-minute extension for PENDING check doesn't also check reviews-API
**Severity:** P3

### F-7: Zero-finding edge case -- step5_push_succeeded guards vacuous truth
**Severity:** P3
**Suggested fix:** Note in D1 that this guards the zero-finding vacuous-truth case.

### F-8: Done-when criterion 1 uses inconsistent variable name
**Severity:** P4

### F-9: No test for multi-round CI-check interaction
**Severity:** P2
**Suggested fix:** Add test 11 for multi-round runs verifying the CI-check gate correctly distinguishes round-1 vs round-2 checks.

STATUS: RED P0=0 P1=1 P2=4 P3=2 P4=2
