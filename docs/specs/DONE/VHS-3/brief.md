# VHS-3 — /review-pr: per-thread "Resolved in &lt;hash&gt;" replies, drop bulk @coderabbitai resolve

**Status:** Backlog · **Priority:** Medium · **Assignee:** Devin
**Created:** 2026-05-08 · **Plane:** VHS-3
**Origin:** Style adjustment to the working `/review-pr` flow. The CodeRabbit back-and-forth is genuine and the auto-approval gate works, but the closing move is a bulk `@coderabbitai resolve` PR comment that collapses per-finding history and short-circuits CodeRabbit's normal closure path. Goal is to replace it with per-thread commit-hash replies and let CodeRabbit's standard mechanisms close threads.

## Problem

`skills/review-pr/SKILL.md` Step 6c currently posts a single PR comment — `@coderabbitai resolve` — after all incremental review rounds have been triaged. This is documented behavior in CodeRabbit (`vigil-harbor-wiki/tools/coderabbit/reference/review-commands.md:234`, `guides/commands.md:66`) and works reliably: it marks every CodeRabbit comment as resolved in one shot, the GitHub thread `isResolved` flips, and `request_changes_workflow: true` flips the verdict to `APPROVED`. The skill then polls and reports success.

Two style problems with this:

1. **Audit trail collapse.** Every closed thread shows the same trailing "Resolved by @coderabbitai" event. There is no per-thread record of *which commit* addressed *which finding*. Future reviewers (and `git blame`-curious humans) have to reconstruct the mapping by reading the commit diff against the comment locations. With one bundled commit per round this is feasible but tedious; with multiple commits across an extended review cycle it gets noisy.

2. **Premature force-close.** `@coderabbitai resolve` is documented in CodeRabbit's own guide with a prominent warning: "Make sure you've actually addressed the feedback before using this command" (`reference/review-commands.md:252`). The skill *does* address findings before posting it, but the bulk resolve still bypasses CodeRabbit's normal per-thread closure semantics — which would otherwise let the user's repo-side configuration (currently on "chill" review mode) be the single point of nit-volume control.

## Why it matters

- **Per-thread provenance is cheap and load-bearing later.** Posting `Resolved in fc701f2` on each fixed thread costs one HTTP call per finding (typical round: 3–8 findings). The audit value compounds: when a CodeRabbit finding turns out to be valid in retrospect, you can grep the thread for the resolving commit instead of reverse-engineering it from review-time and push-time correlation.
- **Decouples skill style from CodeRabbit config.** The user's stated intent is to make CodeRabbit's `.coderabbit.yaml` (review mode, profile, path filters) the *only* knob for nit volume. Skill-side `@coderabbitai resolve` is a hidden second knob — it suppresses noise by force-closing threads regardless of what CodeRabbit would do under its current config. Removing it makes the feedback loop honest: if CodeRabbit produces too many nits after this change, the fix is config-side, not skill-side.
- **Bounded blast radius.** This is markdown-only inside one SKILL.md file. No new tools, no new dependencies, no runtime state change. Easy to revert if the empirical "does CodeRabbit auto-resolve on commit-hash reply?" question (see Risks §1) comes back as "no."

## Scope (verified against current code, 2026-05-08 main)

| Section in `skills/review-pr/SKILL.md` | Current behavior | Replacement |
|---|---|---|
| Step 5 (Commit and push), `:108–121` | Stages and pushes a single bundled commit. Does not capture the resulting SHA for downstream use. | Capture the post-push HEAD SHA (short form via `git rev-parse --short HEAD`). Pass it through to Step 6c along with the list of `fix`-categorized findings from this round. |
| Step 6c (Post resolve), `:179–184` | Single `gh pr comment <N> --body "@coderabbitai resolve"` PR comment. | Loop over each `fix`-categorized finding from this round; for each, post an inline reply on the originating review-comment thread referencing the resolving commit. Body is `Resolved in <short-sha>` (or one of an acceptable variant set — see Decisions §1). |
| Step 6d Phase 1 (Poll for thread resolution), `:188–217` | GraphQL polling for `isResolved` across all CodeRabbit threads, every 15s up to 2min. | Keep the polling logic. Closure semantics change from "explicit resolve command" to "CodeRabbit auto-closes on commit reference" (assumed — see Risks §1). May need to extend the timeout if auto-closure is slower or doesn't happen at all. |
| Step 6d Phase 2 (Wait for verdict), `:222–235` | Polls for `APPROVED` verdict after threads resolve. | Unchanged. Auto-approval still depends on `request_changes_workflow: true` AND all threads resolved AND pre-merge checks passing. |
| Step 6e (Report), `:239–247` | Reports fixed/skipped/duplicates/round count/thread status/verdict. | Add the resolving commit SHA to the "Fixed" line. Optionally enumerate per-finding `(comment-id, sha)` mapping in verbose mode. |

**Preserved (NOT changed):**

- Step 1–4 (input parsing, repo detection, finding fetch, triage, fix-and-test). The triage rules and severity table are unaffected.
- Step 6a/6b (wait for incremental review, triage new findings). The fix-push-review loop and the 3-round cap stay as-is.
- The `request_changes_workflow` warning in Step 1b. Auto-approval semantics depend on it, regardless of resolve mechanism.
- The "all skips/duplicates" branch that skips push and goes straight to resolve. Under the new flow, "all skips/duplicates" means *no* per-thread replies are posted (because no findings were `fix`-categorized) — the thread polling will need to either short-circuit immediately (no pending closures) or fall back to the bulk resolve (see Decisions §3).

**Possible scope wrinkle to confirm before kickoff:**

- The GitHub REST endpoint `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies` posts a reply to a review-comment thread, threading correctly under the original CodeRabbit comment. Confirm `gh api` shape (likely `gh api -X POST repos/<OWNER>/<REPO>/pulls/<N>/comments/<COMMENT_ID>/replies -f body="Resolved in <sha>"`). The `comment_id` comes from the inline-comment fetch in Step 2 (`:51–54`) — already in scope, no new API surface needed.

## Decisions carried forward

1. **Reply phrasing is a small bounded set, not free-form.** Acceptable bodies: `Resolved in <short-sha>`, `Fixed in <short-sha>`, `Fixed, <short-sha>`, `Addressed in <short-sha>`. Pick one and use it consistently within a run; rotating across the set is fine across runs but not within. The user's stated examples were `Resolved in fc701f2` and `Fixed, 2a72316`. Spec author picks the canonical default; recommend `Resolved in <short-sha>` for consistency with CodeRabbit's own "resolved" language.
2. **Short SHA, not full.** Seven-character form via `git rev-parse --short HEAD`. Matches GitHub's display convention and CodeRabbit walkthrough comments.
3. **Fallback to bulk resolve only on polling timeout, not by default.** If after the polling window (Step 6d Phase 1) some threads are still unresolved, the skill posts `@coderabbitai resolve` as a last-resort cleanup and re-polls once. This protects against the documented-but-untested assumption in Risks §1. The fallback fires the bulk command, then re-evaluates — it does *not* loop indefinitely.
4. **Skipped findings get no reply.** Don't post "Skipped because over-engineering" on threads — the final report enumerates skips and reasons. CodeRabbit's own dedup/closure logic (or the user's manual review of skipped threads) handles them. This preserves the human-readable thread for any finding the user disagrees with the skip on.
5. **One commit per round, mapped to all findings from that round.** The current Step 5 already bundles all fixes from one round into a single commit. Don't change that — the mapping is `{ all fix-findings from round N → HEAD SHA after push N }`. If a future change splits commits per finding, the SHA capture point and reply payload change accordingly, but that's out of scope here.

## Approach

1. **Step 5 instrumentation.** After the push succeeds, capture `HEAD_SHORT_SHA=$(git rev-parse --short HEAD)` and the list of comment IDs from the `fix`-categorized findings of this round. Hold both in the skill's working state for Step 6c.
2. **Step 6c rewrite.** Replace the single `gh pr comment` call with a loop:
   ```bash
   for COMMENT_ID in "${FIX_COMMENT_IDS[@]}"; do
     gh api -X POST \
       repos/<OWNER>/<REPO>/pulls/<N>/comments/$COMMENT_ID/replies \
       -f body="Resolved in $HEAD_SHORT_SHA"
   done
   ```
   Spec author decides whether to surface per-call failures inline or batch them into the final report. Recommend: log each failure but don't abort the loop; report the count of failed replies in Step 6e.
3. **Step 6d Phase 1 polling.** Keep the GraphQL query unchanged. Adjust the timeout if empirical testing (see Validation harness below) shows CodeRabbit takes longer to auto-close on hash references than on the explicit command. Initial guess: same 2-minute window; revisit after first real run.
4. **Step 6d fallback branch.** If the polling window ends with unresolved threads, the skill currently warns and lists paths. Modify to: (a) post `@coderabbitai resolve` as a last-resort cleanup, (b) re-poll for 60s, (c) on still-unresolved, fall through to the existing warn-and-list behavior. Document the fallback in the report.
5. **Step 6e reporting.** Add `Resolving commit: <short-sha>` to the report. If the fallback fired, note `Bulk resolve fallback: posted (N threads still required it)`.
6. **Validation harness.** Run `/review-pr` against a real test PR with at least one CodeRabbit finding intentionally left for fixing. Observe whether per-thread hash replies cause CodeRabbit to mark the thread `isResolved` without the bulk command. Cite the result in the spec's Test plan and pin the empirical answer to Risks §1 before merge. The MCP-server repo or a throwaway PR against any vigil-harbor repo is fine; pick one with `request_changes_workflow: true` already configured.

## Acceptance criteria

- `grep -n '@coderabbitai resolve' skills/review-pr/SKILL.md` shows the string only inside the fallback branch (Step 6d) and in explanatory prose, never as the *primary* closure mechanism in Step 6c.
- A real `/review-pr` run on a PR with N≥2 fix-categorized CodeRabbit findings results in N inline replies on the originating threads, each containing the resolving short SHA, observable via `gh api repos/<O>/<R>/pulls/<N>/comments`.
- Threads end up `isResolved: true` in the GraphQL query at the end of the run, with or without the fallback firing.
- The skill's final report (Step 6e) includes the resolving commit SHA on the "Fixed" line.
- If the fallback fires, the report explicitly says so — no silent degradation back to the old behavior.
- `python sync.py status` shows the SKILL.md edit cleanly diffed; `python sync.py push` then `git diff` shows the same SKILL.md byte-for-byte in `~/.claude/skills/review-pr/SKILL.md`.
- The skill still works end-to-end on the "all findings are skips/duplicates" branch (no fixes pushed → no per-thread replies posted → polling either short-circuits or falls back to bulk resolve cleanly).
- No regression on the existing `request_changes_workflow` warning, the infrastructure-error re-trigger branch (Step 2), or the 3-round fix-push-review cap (Step 6b).

## Out of scope

- Tuning `.coderabbit.yaml` (review mode, profile, path filters). The user's intent is explicitly to *not* tune the skill side and instead let CodeRabbit's own config govern noise. That config work is separate.
- Changing the severity triage table in Step 3 (Critical / Major / Minor / Nitpick handling).
- Splitting one bundled commit per round into multiple per-finding commits. The mapping `{round N fixes → one SHA}` is the explicit design.
- Adding a new MCP tool or wrapping `gh api` behind a helper. Direct `gh api` calls match the existing skill style.
- Modifying `request_changes_workflow` Phase 2 polling logic in Step 6d.
- Backfilling per-thread replies on PRs that were already resolved by the old bulk command. Cosmetic-only; not worth the cycles.
- Changing reviewer-comment fetch in Step 2 (already returns the comment IDs we need).

## Risks / decisions

1. **Undocumented assumption: does CodeRabbit auto-resolve a thread on hash-only reply?** CodeRabbit's docs (`vigil-harbor-wiki/tools/coderabbit/guides/commands.md`, `reference/review-commands.md`) document `@coderabbitai resolve` and per-comment commands but say *nothing* about auto-closure on commit-hash mention. Empirical observation in a test PR is required before this design is load-bearing. Decision §3 hedges: if hash replies don't auto-close, the fallback bulk-resolve fires and the skill still terminates cleanly. Spec author must run the validation harness (Approach §6) and pin the answer in the spec — do not ship without it.
2. **Per-comment-reply API permissions.** `gh api -X POST .../comments/{id}/replies` requires the same auth `gh pr comment` already uses (PR write). No new permission surface, but worth confirming on a real run that the existing `gh` auth works for the replies endpoint.
3. **Comment-ID stability across incremental reviews.** When CodeRabbit posts an incremental review (Step 6a/6b), it may reuse the original comment thread or create a new one. The skill's per-thread-reply logic must reply on the *current* unresolved thread for each finding, not the original. Spec author should verify by examining the inline-comment payload for `in_reply_to_id` chains and reply on the leaf, not the root. Likely a one-line filter; flag if anything more involved.
4. **"All findings skipped" race.** If round 1 produces only skips/duplicates, no commit gets pushed, so there's no SHA to reply with. Current skill goes straight to bulk resolve. Decision §3 fallback handles this — no per-thread replies, polling immediately falls through to bulk resolve. Confirm in the spec that this branch is explicit and tested.
5. **Reply-rate concerns.** GitHub's secondary rate limit on review-comment replies is generous but not infinite. A pathological round with 30+ findings could hit it. Realistic round size is 3–8; not a concern for v1, but worth noting. If it becomes one, batch via GraphQL `addPullRequestReviewThreadReply` instead of N REST calls.
6. **CodeRabbit verdict timing.** Phase 2 (verdict polling) currently expects the verdict flip to follow thread resolution by ~20–60s. If hash-reply auto-closure is slower than explicit-resolve, the cumulative wait may exceed the 3-minute Phase 2 window. Spec author should re-evaluate the Phase 2 timeout after the validation harness run.
7. **No "ignore" semantics for skipped findings.** The current bulk resolve closes *every* thread including skipped ones. The new flow only closes fix-threads via reply. Skipped-thread closure relies on either: (a) CodeRabbit's own duplicate detection in the next incremental review, (b) the fallback bulk resolve firing because of unresolved skipped threads, or (c) the user manually resolving them. Decision §3 (fallback) covers (b); the spec should make the trade-off explicit and pick a default.

## References

- Plane: VHS-3
- Skill: `skills/review-pr/SKILL.md` (current implementation, ~258 lines)
- CodeRabbit command reference (mirrored): `vigil-harbor-wiki/tools/coderabbit/reference/review-commands.md` § "@coderabbitai resolve" (`:234`)
- CodeRabbit guide on managing reviews (mirrored): `vigil-harbor-wiki/tools/coderabbit/guides/commands.md` § "Resolve comments" (`:66`)
- CodeRabbit `request_changes_workflow` semantics: `vigil-harbor-wiki/tools/coderabbit/reference/configuration.md:43`, `reference/glossary.md:70`
- CodeRabbit pre-merge checks (relevant for Phase 2): `vigil-harbor-wiki/tools/coderabbit/pr-reviews/pre-merge-checks.md`
- Workflow context: `vigil-skills/CLAUDE.md` § "/review-pr"
- GitHub REST API — Create a reply for a review comment: `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies` (verify exact `gh api` invocation in spec)
- Current call sites verified 2026-05-08 via `Read skills/review-pr/SKILL.md`
