# Correctness Review -- round 1

## Findings

### F-1: Multi-round SHA capture gap -- only Step 5 captures SHA, rounds 2/3 push from Step 6b without capture
**Severity:** P1
**Where:** spec.md:66-74 (Step 5 design) and spec.md:82 (Step 6c "from this round")
**Claim:** "After the push succeeds (line ~119), add: `HEAD_SHORT_SHA=$(git rev-parse --short HEAD)`" and D5: "The mapping is `{ all fix-findings from round N -> HEAD SHA after push N }`"
**Why this is wrong:** The spec captures SHA only in Step 5 (the first push). But the 6a/6b loop can produce up to 3 fix-push-review cycles. Rounds 2 and 3 commit and push from within Step 6b (SKILL.md line 168: "apply fixes, run tests, commit, push, then loop back to 6a"), not from Step 5. The spec never instructs SHA capture inside the 6b loop. Step 6c then runs once after all rounds, but only has `HEAD_SHORT_SHA` from Step 5 -- findings fixed in rounds 2/3 would either get the wrong SHA or no reply. D5 correctly states the per-round mapping intent but the design section does not implement it.
**Suggested fix:** Either (a) add SHA capture to Step 6b's commit-push path and accumulate a list of `(comment_id, sha)` pairs across rounds, posting all replies in Step 6c; or (b) restructure to post per-thread replies immediately after each push (inside the loop at 6b, before looping back to 6a), which also avoids the need to accumulate state across rounds.

### F-2: Fallback `@coderabbitai resolve` contradicts Plane ticket acceptance criterion
**Severity:** P1
**Where:** spec.md:32-35 (D3) and spec.md:113-121 (Step 6d Phase 1 fallback)
**Claim:** D3: "the fallback fires only when fix-categorized threads fail to auto-resolve within the polling window" and posts `@coderabbitai resolve`
**Why this is wrong:** The user's stated intent (quoted in D4) is to "let the reviewer run through its natural process of actually gating approval, not forcing." Auto-firing `@coderabbitai resolve` as a fallback contradicts this by force-resolving threads (including skipped ones) when fix-threads are slow to auto-resolve. The brief's Decision §3 introduces the fallback as a hedge, but the user explicitly authorized departing from the brief on this point: "Feel free to quote me if it's a brief-drift issue."
**Suggested fix:** Remove the automated fallback. When fix-threads don't auto-resolve within the polling window, report the unresolved thread paths and offer the manual command. Let the user decide whether to force-resolve.

### F-3: "Stale CHANGES_REQUESTED with no findings" edge case dropped
**Severity:** P1
**Where:** spec.md:147-158 (Edge cases table)
**Claim:** The spec lists 8 edge cases but omits the current "Stale CHANGES_REQUESTED with no findings" edge case.
**Why this is wrong:** SKILL.md line 258 currently has: "Stale CHANGES_REQUESTED with no findings: post resolve and wait for auto-approval -- CodeRabbit may be blocking from a previous review round whose threads were never resolved." This is a real scenario (leftover threads from a prior `/review-pr` run or manual CodeRabbit review). The spec's new behavior would change this: without `@coderabbitai resolve` as the primary mechanism, a stale CHANGES_REQUESTED with no current findings would never get resolved. The spec needs to decide what happens here.
**Suggested fix:** Add an entry to the edge cases table specifying the new behavior: prior-round threads stay open, report shows them, user manually resolves.

### F-4: Step 6d Phase 2 entry condition change contradicts brief's "Unchanged" scope
**Severity:** P2
**Where:** spec.md:123-131 (Step 6d Phase 2) and spec.md:18 (Preserved section)
**Claim:** Spec line 18: "Step 6d Phase 2 (verdict polling logic) -- the polling mechanics are unchanged; only the conditions for entering Phase 2 change." But the brief says Phase 2 is "Unchanged."
**Why this is wrong:** The brief's scope table explicitly says "Step 6d Phase 2: Unchanged." The spec adds entry conditions that skip Phase 2 when skipped threads are open. This is a scope expansion beyond the brief.
**Suggested fix:** Note the scope addition and justify why it's necessary.

### F-5: "All skips/duplicates" behavior diverges from brief's Risk 4 assumption
**Severity:** P2
**Where:** spec.md:48-58 (D6)
**Claim:** D6 says go directly to report. Brief's Risk 4 assumed fallback would fire for all-skips.
**Suggested fix:** Add a note in D6 acknowledging the divergence and justifying the choice.

### F-6: Step 6c "from this round" is ambiguous in multi-round context
**Severity:** P2
**Where:** spec.md:82
**Suggested fix:** Clarify to "from all rounds" or restructure to post replies per-round inside the 6b loop.

### F-7: Brief's Risk 3 (comment-ID stability across incremental reviews) not addressed
**Severity:** P2
**Where:** spec.md (absent)
**Suggested fix:** Add a design note specifying that incremental-review findings (from Step 6b) use the comment IDs from the incremental review fetch, not the original Step 2 fetch.

## Summary
P0: 0 | P1: 3 | P2: 4 | P3: 0 | P4: 0

STATUS: RED P0=0 P1=3 P2=4 P3=0 P4=0
