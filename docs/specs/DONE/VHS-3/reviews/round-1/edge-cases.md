# Edge-Cases Review -- round 1

## Findings

### F-1: Multi-round fix loop -- per-thread replies posted once at end, but SHA maps to only the last push
**Severity:** P1
**Where:** spec.md:66-94 (Step 5 + Step 6c design)
**Edge case:** Multiple fix-push-review rounds (up to 3 per the 6b cap)
**What happens:** Step 6c fires once after the loop. HEAD_SHORT_SHA contains only the last push's SHA. Findings fixed in round 1 get replied with the round 3 SHA -- the wrong commit.
**Suggested fix:** Post per-thread replies inside the 6a/6b loop after each push, or accumulate {comment_id, sha} tuples across rounds.

### F-2: `unresolved_count <= skip_count` success condition is unsound -- thread count != finding count
**Severity:** P1
**Where:** spec.md:96-109 (Step 6d Phase 1)
**Edge case:** Multiple findings per thread, pre-existing unresolved threads from prior rounds
**What happens:** The 1:1 mapping between findings and threads doesn't hold. Pre-existing unresolved threads inflate unresolved_count, triggering false fallback.
**Suggested fix:** Track fix-thread IDs and poll for those specific threads, or use delta-based counting.

### F-3: `already-fixed` category is unaccounted -- no reply, no skip count, breaks the arithmetic
**Severity:** P1
**Where:** spec.md:50, 94, 106
**Edge case:** Findings categorized as `already-fixed` are neither fix nor skip/duplicate
**What happens:** Their threads remain open but aren't counted in skip_count, causing unresolved_count to exceed skip_count and triggering fallback spuriously.
**Suggested fix:** Include `already-fixed` in the non-fix category alongside skip/duplicate.

### F-4: Spec contradicts the Plane ticket acceptance criterion on `@coderabbitai resolve`
**Severity:** P1
**Where:** spec.md:33-36 (D3), spec.md:113-121 (fallback)
**Edge case:** Fallback fires `@coderabbitai resolve` but user wants natural process
**Suggested fix:** Remove automated fallback; report unresolved threads instead and offer manual command.

### F-5: The "Stale CHANGES_REQUESTED with no findings" edge case is dropped without a replacement
**Severity:** P2
**Where:** spec.md:147-158 (Edge cases table)
**Suggested fix:** Add explicit edge case entry.

### F-6: Per-thread reply may target the wrong comment ID in multi-round scenarios
**Severity:** P2
**Where:** spec.md:82-90 (Step 6c)
**Edge case:** CodeRabbit's incremental review creates new threads on same location
**Suggested fix:** Specify that round-N replies use round-N comment IDs from the incremental review fetch.

### F-7: Nitpick findings (review-body-level, not inline comments) have no comment ID
**Severity:** P2
**Where:** spec.md:82-90 (Step 6c), current SKILL.md line 71
**Edge case:** A nitpick from the review body summary categorized as `fix` has no comment_id
**Suggested fix:** Guard: skip reply for findings with no comment ID, note in report.

### F-8: Phase 2 entry condition creates a dead path when fallback fires but re-poll still shows unresolved threads
**Severity:** P2
**Where:** spec.md:119-131 (Step 6d fallback + Phase 2 entry)
**Suggested fix:** Add report template for fallback-failure case.

### F-9: Spec does not update the Step 6 header prose that references `@coderabbitai resolve`
**Severity:** P2
**Where:** spec.md:10-11 (Scope table), current SKILL.md line 125
**Suggested fix:** Add Step 6 header to scope table.

### F-10: Rate limiting on the reply API for edge-case round sizes
**Severity:** P3
**Where:** spec.md:157
**Suggested fix:** Add retry-once on 429/Retry-After header.

### F-11: Test plan has no coverage for the multi-round SHA mapping edge case
**Severity:** P3
**Where:** spec.md:160-211
**Suggested fix:** Add multi-round test scenario.

## Summary
P0: 0 | P1: 4 | P2: 5 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=4 P2=5 P3=2 P4=0
