---
name: review-pr
description: Triage and fix CodeRabbit review comments on a PR. Verifies findings against current code, fixes real issues, pushes, posts per-thread commit-hash replies, waits for CodeRabbit's incremental re-review, and polls for auto-approval.
user_invocable: true
---

# /review-pr — CodeRabbit review round handler

Process one round of CodeRabbit review findings on a GitHub PR. Triage by severity, fix real issues, push, resolve threads.

**Shell note:** All `gh api`, `git`, and `gh pr` commands use bash syntax (single quotes, `$()` expansion). Use the **Bash tool** for these commands, not PowerShell.

## Input parsing

Parse the argument into a PR number:

- `/review-pr 8` → PR #8
- `/review-pr https://github.com/.../pull/8` → extract #8 from URL
- `/review-pr` (no arg) → detect from current branch: `gh pr view --json number --jq .number`

## Step 1: Detect repo, resolve working directory, and check state

```bash
# Get owner/repo
gh repo view --json owner,name --jq '.owner.login + "/" + .name'

# Resolve the PR's head branch and find the right working directory
PR_BRANCH=$(gh pr view <N> --json headRefName --jq .headRefName)
# Exact-match the branch against worktree list (porcelain column: path + HEAD + branch)
WORKTREE_PATH=$(git worktree list --porcelain | awk -v b="$PR_BRANCH" '
  /^worktree /{ wt=$2 }
  /^branch /{ if ($2 == "refs/heads/" b) print wt }
')
```

If `WORKTREE_PATH` is non-empty, use it as the working directory for all subsequent steps (file reads, edits, git operations). If the branch is the current branch in the primary tree (`git branch --show-current` matches `$PR_BRANCH`), use the primary tree. If the branch isn't checked out anywhere, check it out before proceeding.

```bash
# Get the PR's diff scope (file list) — helps contextualize findings and triage outside-diff comments
gh pr diff <N> --name-only

# Check if CodeRabbit review is still pending
gh pr checks <N>
```

If CodeRabbit shows "Review in progress" or "pending", tell the user to wait and stop.

### 1b. Check CodeRabbit config

Read `.coderabbit.yaml` from the repo root. Confirm `reviews.request_changes_workflow: true`. This is what enables CodeRabbit to auto-approve after all threads are resolved and pre-merge checks pass.

If the file is missing or `request_changes_workflow` is not `true`, warn:
```text
⚠ request_changes_workflow is not enabled in .coderabbit.yaml.
CodeRabbit will not auto-approve after thread resolution.
Thread resolution will still work but the review verdict must be changed manually.
```

Proceed regardless — the skill still works for thread cleanup without auto-approval.

## Step 2: Fetch CodeRabbit review comments

```bash
# Get all reviews — find the latest coderabbitai[bot] VERDICT review.
# `select(.state != "COMMENTED")` is load-bearing: CodeRabbit posts an
# empty-bodied COMMENTED review for every reply it makes on a thread, so an
# unfiltered `last` returns an acknowledgement rather than the verdict.
gh api repos/{owner}/{repo}/pulls/<N>/reviews \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.state != "COMMENTED")] | sort_by(.submitted_at) | last | {id, state, submitted_at, body}'

# Get inline comments from CodeRabbit — findings only.
# `in_reply_to_id == null` excludes CodeRabbit's own "✅ Review thread resolved"
# replies, which are authored by the same bot and would otherwise be triaged as
# if they were findings.
gh api repos/{owner}/{repo}/pulls/<N>/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.in_reply_to_id == null)]'
```

If the latest review body contains infrastructure errors — look for `"Failed to clone"`, `"🔥 Problems"`, or `"Please run the @coderabbitai full review"` — then post `@coderabbitai full review` as a PR comment to re-trigger the review, report "CodeRabbit hit an infrastructure error — re-triggered full review", and stop.

If the latest review state is `APPROVED` and there are no unresolved comments, report "Nothing to review — PR is approved" and stop.

If there are no CodeRabbit reviews at all, report "No CodeRabbit reviews found" and stop.

## Step 3: Triage each finding

CodeRabbit tags findings with severity labels. Parse them from the comment body:

| Severity | Pattern in body | Default action |
|----------|----------------|----------------|
| Critical | `_🔴 Critical_` | **Always fix** |
| Major | `_🟠 Major_` | Fix unless already addressed in current code |
| Minor | `_🟡 Minor_` | Fix if trivial and correct; skip if over-engineering |
| Nitpick | `🧹 Nitpick` (appears in review body summary, not inline) | Skip unless trivially correct |

For EACH finding:

1. **Parse** the severity label and the file path + line number from the comment
2. **Read** the actual file at the referenced line using the Read tool
3. **Verify** whether the finding applies to the current code (it may already be fixed in a later commit)
4. **Categorize**:
   - `fix` — genuinely wrong code, security issue, real bug, applies to current code
   - `duplicate` — same finding repeated from a prior review round
   - `skip` — over-engineering suggestion, style preference, already fixed, or the reviewer misread the code
   - `already-fixed` — finding was valid but a subsequent commit already addressed it

Record the categorization and reason for each finding.

### Important triage rules

- **Outside-diff comments**: findings on code not changed by this PR. Fix only if genuinely wrong.
- **Duplicate comments**: CodeRabbit marks these in a "Duplicate comments" section in the review body. Always skip.
- **Nitpick sections**: CodeRabbit groups these in a "Nitpick comments" section in the review body. Default to skip.
- When in doubt about whether to fix, **read the code first** — never skip without verifying.

## Step 4: Fix and test

For all findings categorized as `fix`:

1. Apply the code fix using Edit tool
2. After all fixes are applied, run the project's test suite. Use the same test-command resolution as `/ship-spec` Phase 0 step 4: spec `## Test command` first, then `CLAUDE.md` "Build & Run" section. If no test command found: warn but proceed — review-pr is fixing review comments, not authoring new features, so skipping tests is less critical than in ship-spec
3. If tests fail, fix the test failure before continuing
4. If no findings were categorized as `fix`, skip this step entirely

## Step 5: Commit and push

Only if fixes were made:

1. Stage only the changed files by name (never use `git add -A` or `git add .`)
2. Write a descriptive commit message summarizing what was fixed and what was skipped:
   ```
   fix: <summary of fixes>

   Fixed: <list of what was fixed>
   Skipped: <list of what was skipped with brief reasons>

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
3. Push to the PR branch
4. Capture the resolving commit SHA and post per-thread replies:
   ```bash
   HEAD_SHORT_SHA=$(git rev-parse --short HEAD)
   ```
   For each fix-categorized finding from this round, post an inline reply on the originating review-comment thread (see Step 6c for the reply mechanism and error handling). Then post non-fix replies for all skip/duplicate/already-fixed findings from this round (see Step 6c). Then continue to Step 6a.

**Note:** Pushing triggers CodeRabbit's auto-incremental review of the new commit. Step 6 waits for it before attempting thread resolution.

## Step 6: Wait for re-review, verify thread resolution, poll for approval

Per-thread replies are the primary closure mechanism for all findings. Fix-categorized findings get `Resolved in <sha>` replies. Non-fix findings (skip/duplicate/already-fixed) get a reply stating the categorization and reasoning — this creates a record and lets CodeRabbit resolve threads naturally without force-resolving. Auto-approval (`APPROVED` verdict) requires all threads resolved AND `request_changes_workflow: true` AND pre-merge checks passing. The skill never posts `@coderabbitai resolve` — if threads don't auto-resolve on reply, the report offers the manual command.

**Fast-path predicate (evaluated once, after Step 5):**

```
FAST_PATH = (round1_finding_count <= 2
             AND every round-1 finding is categorized as "fix"
             AND step 5 pushed successfully)
```

If `FAST_PATH` is true, skip Steps 6a and 6b entirely — proceed directly to Step 6d. Log: `Fast path triggered — skipping incremental review wait (≤2 fix-only findings)`. The rationale: on trivial PRs (1–2 fix-only findings), CodeRabbit's incremental review of the resulting small fix almost never surfaces new actionable findings. The 30s–5min wait in 6a has near-zero expected value. If CodeRabbit does post new findings, re-running `/review-pr` on the same PR picks them up naturally.

### 6a. Wait for CodeRabbit's incremental review (only if fixes were pushed)

If no fixes were pushed (all skips/duplicates/already-fixed), skip to 6d.

**If FAST_PATH is true**, set `REVIEW_SIGNAL=fast-path` and skip to 6d. (Per-thread replies were already posted in Step 5.)

**Otherwise, capture push time and check for pre-existing approval:**

```bash
HEAD_SHA=$(git rev-parse HEAD)
PUSH_TIME=$(gh api repos/<OWNER>/<REPO>/commits/$HEAD_SHA --jq '.commit.committer.date')

gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.state != "COMMENTED")] | sort_by(.submitted_at) | last | {id, state, submitted_at}'
```

Capture that review's `id` as `PREV_REVIEW_ID` — the new-findings predicate below is relative to it.

`PUSH_TIME` and `PREV_REVIEW_ID` are conversational state — the LLM captures their values from the Bash output and substitutes them literally into subsequent Bash commands. Individual Bash tool calls do not share shell variables.

If the latest verdict's `state` is `APPROVED` **and its `submitted_at` is after `PUSH_TIME`**, skip 6a/6b and go straight to 6e. Set `REVIEW_SIGNAL=pre-existing-approval`. (This skips 6d — the existing behavior, preserved from the current SKILL.md; `APPROVED` implies threads are resolved or will be imminently.) A pre-push `APPROVED` verdict must not short-circuit: the incoming incremental review may flip it back to `CHANGES_REQUESTED`.

**Otherwise, poll for new findings directly. This is the primary signal.**

> **Why not gate on the CI check.** The `CodeRabbit` check is an unreliable completion signal and must never be the thing that blocks progress. Observed on Vigil-Harbor/petland PR #51 across two consecutive rounds: the check reported `pass / Review completed` before the first push, then went `PENDING` after each push and **stayed `PENDING` indefinitely** — through a full review being posted, five threads being replied to and resolved, and a second review carrying a genuine new finding. Gating on `SUCCESS` there burns the entire 10-minute PENDING budget and then reports a timeout, on a PR where the findings had been available for minutes. Poll the findings themselves; treat the check as advisory colour only.

```bash
# New FINDINGS since the last round. Two filters, both load-bearing:
#   pull_request_review_id > PREV_REVIEW_ID  — belongs to a newer review
#   in_reply_to_id == null                   — is a finding, not CodeRabbit's
#                                              own "✅ Review thread resolved"
#                                              acknowledgement of your reply
gh api repos/<OWNER>/<REPO>/pulls/<N>/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.pull_request_review_id > <PREV_REVIEW_ID>) | select(.in_reply_to_id == null)] | length'
```

**Do not use `select(.submitted_at > PUSH_TIME)` on the reviews endpoint as the detection query.** CodeRabbit posts an empty-bodied `COMMENTED` review for each thread reply it makes, so within ~40 seconds of posting replies that query returns a non-zero count of reviews that contain no findings at all. Taking `last | .id` off it hands Step 6b an acknowledgement review, whose comment list is empty, and the round concludes "no new findings" while a real finding is still inbound. That is a false negative on the one thing this step exists to catch.

Poll by making **individual Bash tool calls**. Make up to 10 attempts (intervals are aspirational — the agent harness fires Bash tool calls back-to-back, so the attempt count is what bounds polling, not wall-clock). Outcomes:

- **Count > 0:** new findings exist. Capture their review id and proceed to 6b. Set `REVIEW_SIGNAL=new-findings`.
- **Count stays 0 for all attempts:** proceed to 6d, but set `REVIEW_SIGNAL=inconclusive` — see the honesty rule in 6e. CodeRabbit may have had nothing to add, or may simply not have finished.
- **A verdict review lands (`state != "COMMENTED"`, `submitted_at > PUSH_TIME`) with count 0:** CodeRabbit finished and found nothing. Set `REVIEW_SIGNAL=verdict-landed` and proceed to 6d. This is the only *positive* "nothing new" signal available; check for it alongside the count.

**Advisory only — CodeRabbit's CI check:**

```bash
gh pr checks <N> --json name,state \
  --jq '[.[] | select(.name | test("coderabbit"; "i")) | .state] | if length == 0 then "NONE" elif any(. == "PENDING") then "PENDING" elif all(. == "SUCCESS") then "SUCCESS" else "FAILURE" end'
```

Fold this into the same Bash calls as the findings poll, for observability only. `FAILURE` is the one state worth acting on: CodeRabbit errored, so no incremental findings are coming and polling further is pointless — proceed to 6d immediately with `REVIEW_SIGNAL=ci-check (FAILURE)`. `SUCCESS` corroborates a count of 0. `PENDING` and `NONE` mean nothing either way and must not extend polling.

**Re-entry from 6b (round 2+ guard):** the findings predicate handles this for free — advance `PREV_REVIEW_ID` to the review just triaged before looping back, and `pull_request_review_id > PREV_REVIEW_ID` cannot re-match the prior round. No check-transition dance is needed.

### 6b. Triage new findings from incremental review

(Skipped entirely when FAST_PATH is true — proceed to 6d.)

Fetch the new findings in full, using the same two filters that detected them in 6a — newer than `PREV_REVIEW_ID`, and not a reply. Filtering on a single `pull_request_review_id` is too narrow: CodeRabbit sometimes splits one round's findings across more than one review id, and the `>` comparison catches them all.

```bash
gh api repos/<OWNER>/<REPO>/pulls/<N>/comments \
  --jq '.[] | select(.user.login == "coderabbitai[bot]") | select(.pull_request_review_id > <PREV_REVIEW_ID>) | select(.in_reply_to_id == null) | "=== ID:\(.id) \(.path):\(.line // .original_line)\n\(.body)"'
```

Without `in_reply_to_id == null` this returns CodeRabbit's own `✅ Review thread resolved` acknowledgements — same bot login, higher review id — and they get triaged as if they were findings.

If the new review has NEW findings not present in the original review:

- Triage using Step 3 logic
- If any are categorized as `fix`: apply fixes, run tests, commit, push, capture `HEAD_SHORT_SHA=$(git rev-parse --short HEAD)`, post per-thread replies for this round's fix-categorized findings (same mechanism as Step 6c), then loop back to 6a
- **Cap at 3 fix-push-review cycles.** After 3 rounds, warn the user and proceed to 6d:
  ```text
  3 fix-push-review cycles completed. Remaining findings:
    - <list>
  Proceeding to check thread resolution status. Re-run /review-pr if needed.
  ```

If the incremental review has no new actionable findings (or only duplicates/already-fixed), proceed to 6d.

### 6c. Per-thread replies (mechanism)

Step 6c is not a standalone post-loop step — per-thread replies are posted immediately after each push (Step 5 and each Step 6b fix-push cycle). Fix replies are posted first (they reference the push SHA), then non-fix replies. If no fixes were pushed (all non-fix), non-fix replies are still posted after Step 3 triage completes.

**Fix reply mechanism:**

For each fix-categorized finding from the current round, post an inline reply on the originating review-comment thread:

```bash
gh api -X POST \
  repos/<OWNER>/<REPO>/pulls/<N>/comments/<COMMENT_ID>/replies \
  -f body="Resolved in <HEAD_SHORT_SHA>"
```

**Non-fix reply mechanism:**

For each non-fix finding (skip/duplicate/already-fixed) from the current round, post an inline reply with the categorization and reasoning:

```bash
gh api -X POST \
  repos/<OWNER>/<REPO>/pulls/<N>/comments/<COMMENT_ID>/replies \
  -f body="<REPLY_BODY>"
```

Reply body templates by category:

- **skip**: `Skipped — <reason from triage>` (e.g., "Skipped — style preference; current pattern is consistent with the rest of the codebase", "Skipped — suggestion would over-engineer a straightforward path")
- **duplicate**: `Duplicate of earlier finding — no action taken.`
- **already-fixed**: `Already addressed in a prior commit — no action needed.`

Keep reasoning concise (1–2 sentences). The goal is a record of the judgment call, not a debate.

**Comment ID sourcing:** `<COMMENT_ID>` is the review-comment ID from the finding's triage. For findings from Step 3 (initial triage), the comment ID comes from Step 2's inline-comment fetch. For findings from Step 6b (incremental review triage), the comment ID comes from the incremental review's comment fetch (filtered to the new review ID). Each round uses its own comment IDs.

**Guard for body-level findings:** If a finding has no associated comment ID (e.g., a review-body-level nitpick), skip the reply for that finding. Note the skip in the Step 6e report: `Reply skipped: finding has no inline comment ID (review-body-level)`.

**Error handling:** If a reply call fails (404 = comment deleted, 403 = permission issue, 422 = thread locked, 429 = rate limited), log the failure and continue. Do not abort the loop. On 429 with a `Retry-After` header, wait the indicated duration and retry once. Failed reply count is reported in Step 6e.

### 6d. Poll for thread resolution + approval

**Short-circuit:** If no fix-categorized findings exist across ALL rounds of this run (not just the current round), skip Phase 1 entirely — no fix-threads to wait for. If prior rounds had fix-categorized findings, poll to observe their resolution status even if the current round had no fixes.

**Phase 1 — Observe thread resolution status.**

> Note: GitHub's GraphQL API returns `coderabbitai` for the bot login (no `[bot]` suffix). The REST API used elsewhere in this skill returns `coderabbitai[bot]`. The jq filter below runs against GraphQL data, so it uses the unsuffixed form.

```bash
gh api graphql -f query='query {
  repository(owner:"<OWNER>", name:"<REPO>") {
    pullRequest(number:<N>) {
      reviewThreads(first:100) {
        pageInfo { hasNextPage endCursor }
        nodes {
          isResolved
          path
          comments(first:1) {
            nodes { author { login } }
          }
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads | {hasNextPage: .pageInfo.hasNextPage, endCursor: .pageInfo.endCursor, threads: [.nodes[] | select(.comments.nodes[0].author.login == "coderabbitai")]}'
```

If `hasNextPage` is true, repeat with `reviewThreads(first:100, after:"<endCursor>")` and merge the `threads` arrays until `hasNextPage` is false. Then evaluate the merged set:

```bash
# On the merged threads array:
# all_resolved if every thread's .isResolved is true
# otherwise: unresolved_threads: <comma-separated .path values of unresolved threads>
```

Poll by making **individual Bash tool calls** (not a sleep loop — sleep loops are blocked in this environment). Make up to 8 polling attempts; the attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back. After each poll, observe how many CodeRabbit threads are resolved and how many are still unresolved. The skill does not attempt to correlate unresolved thread counts against finding counts — it simply observes and reports.

If after exhausting the polling attempts some threads are still unresolved, report the unresolved thread file paths and the manual resolve command:

```text
N CodeRabbit threads still unresolved after 8 polling attempts:
  - <path1>
  - <path2>
To force-resolve all threads: gh pr comment <N> --body "@coderabbitai resolve"
```

Do not auto-fire the command.

**Phase 2 — Wait for review verdict to update.**

**Enter Phase 2 only if ALL CodeRabbit threads are resolved.** This means:
- If all threads resolved (fix-threads via SHA reply, non-fix threads via reasoning reply) → enter Phase 2
- If any threads unresolved (reply didn't trigger resolution, or threads stuck) → **skip Phase 2**; report that `CHANGES_REQUESTED` is expected while threads remain open
- If `request_changes_workflow` is not enabled (per Step 1b) → skip Phase 2 as before

Once entered, poll for the review verdict:

```bash
# select(.state != "COMMENTED") again — an unfiltered `last` returns one of
# CodeRabbit's empty reply-acknowledgement reviews and reads as a verdict.
gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.state != "COMMENTED")] | sort_by(.submitted_at) | last | .state'
```

Poll by making **individual Bash tool calls**; make up to 9 polling attempts. The attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back. CodeRabbit's `request_changes_workflow` auto-approval fires after threads are resolved AND pre-merge checks pass.

Outcomes:
- `APPROVED`: success — CodeRabbit has lifted the reviewer block.
- `CHANGES_REQUESTED` after timeout: **the common case, and usually benign.** The verdict lags thread resolution by minutes; observed on PR #51 staying `CHANGES_REQUESTED` through nine polls in each of two rounds with every thread resolved and every other check green, then lifting on its own afterwards. Report it as a stale verdict expected to clear, not as a problem: "All threads resolved; the verdict lags and should flip on its own. If it hasn't after a few minutes, check the CodeRabbit walkthrough comment for a failing pre-merge check." Do not fire `@coderabbitai resolve` for this — the threads are already resolved and it fixes nothing.

### 6e. Report

```text
Review round complete for PR #<N>:
- Fixed: X findings in commit <short-sha> (list them)
  [If multi-round: "Round 1: A findings in <sha1>; Round 2: B findings in <sha2>"]
- Skipped: Y findings (list with reasons) — replied with reasoning
- Already fixed: Z findings (list them) — replied
- Duplicates: W
- Incremental review rounds: M
- Reply failures: F (list comment IDs and error codes, if any)
- Reply skipped: G (body-level findings with no inline comment ID, if any)
- Thread status: X resolved / Y unresolved
  [If threads unresolved: "N threads still unresolved — to force-resolve: gh pr comment <N> --body '@coderabbitai resolve'"]
- CodeRabbit verdict: APPROVED / CHANGES_REQUESTED (expected — N threads open) / CHANGES_REQUESTED (stale — all threads resolved, verdict lags) / not polled (request_changes_workflow disabled)
- Fast path: yes — re-run /review-pr if CodeRabbit posts new findings / no
- Review completion signal: new-findings / verdict-landed / inconclusive / ci-check (FAILURE) / pre-existing-approval / fast-path
```

**Honesty rule on `inconclusive`.** Say "no new findings" only on `verdict-landed` — a post-push review whose `state != "COMMENTED"` actually arrived and carried none. On `inconclusive` (polling exhausted with a count of 0 and no verdict review), the accurate line is:

```text
- Incremental review: inconclusive — polling ended before CodeRabbit posted a
  verdict for <sha>. Re-run /review-pr to pick up anything that lands after this.
```

This distinction is not pedantry. On PR #51 round 1, polling ended reporting "no new findings"; a `CHANGES_REQUESTED` review carrying a real Major-adjacent finding landed about three minutes later and was caught only because the user pasted it in. A round that ends `inconclusive` is a round that is not finished.

## Edge cases

- **No new comments**: report "Nothing to review" and exit
- **All findings are non-fix (skip/duplicate/already-fixed)**: no push, but replies are posted with reasoning for each inline finding (body-level findings without a comment ID are skipped per the guard in 6c)
- **CodeRabbit review pending**: "Review in progress — wait and retry"
- **CI failing from unrelated issue**: warn user but still process review findings (the review may contain the fix)
- **Branch protection blocks push**: report the error, don't retry
- **Incremental review loop**: cap at 3 fix-push-review cycles to prevent infinite loops
- **CodeRabbit timeout/down**: if polls consistently timeout with no CodeRabbit activity, report and stop
- **Stale CHANGES_REQUESTED with all threads resolved**: the normal end state of a successful round. The verdict trails thread resolution by minutes. Report it as stale-and-expected; do not fire `@coderabbitai resolve` (there is nothing left to resolve) and do not diagnose it as a failing pre-merge check unless the checks actually show one
- **Stale CHANGES_REQUESTED with threads still open**: no new findings → no triage → report "no findings but N prior-round threads still unresolved" with manual resolve command (`gh pr comment <N> --body "@coderabbitai resolve"`)
- **Fix-threads don't auto-resolve on hash reply**: report unresolved threads + manual resolve command. No automated fallback
- **Reply API call fails (404/403/422)**: log failure, continue loop, report count in 6e
- **Reply API rate-limited (429)**: wait `Retry-After` duration, retry once. If still 429, log and continue
- **Mixed fix+non-fix findings, all threads resolve**: all threads replied to (fix with SHA, non-fix with reasoning), poll, Phase 2 → APPROVED
- **All fix, no non-fix, threads resolve**: per-thread replies, poll, Phase 2 → APPROVED
- **Multi-round fix-push-review**: per-thread replies posted after each push with correct per-round SHA
- **Comment deleted between triage and reply**: 404 from reply API — logged, counted, non-fatal
- **Body-level nitpick categorized as fix**: reply skipped (no comment ID), noted in report
- **Incremental review creates new thread on same location**: round-N replies use round-N comment IDs from the incremental review fetch. If the new thread is on the same file:line as a prior round's "Resolved" reply, both coexist — cosmetically confusing but functionally correct
- **Rate limit on reply API (pathological 30+ findings)**: 429 retry handles transient limits; if persistent, cap at available budget and report
- **Fast path triggered, no incremental review observed**: expected behavior — the fast path intentionally skips 6a/6b. If CodeRabbit posts new findings after the run, re-run `/review-pr` to pick them up.
- **Fast path triggered but CodeRabbit posts new findings before 6d completes**: 6d's thread-resolution polling may observe unresolved threads from the new findings. The report will show them as unresolved with the manual resolve command. Re-run `/review-pr` to triage.
- **CodeRabbit check stuck `PENDING` indefinitely**: common, and harmless now that the check is advisory. Observed on Vigil-Harbor/petland PR #51 for the full duration of two rounds while reviews, replies, and thread resolutions all landed normally. Never extend polling on it.
- **CodeRabbit check `FAILURE`**: CodeRabbit errored and posted no findings. The one check state worth acting on — proceed to 6d (skip 6b), `REVIEW_SIGNAL=ci-check (FAILURE)`.
- **Empty `COMMENTED` reviews flood the reviews endpoint**: CodeRabbit posts one per thread reply, so a run that answers five threads adds five bodiless reviews within a minute. Any query that takes `last` off an unfiltered review list — verdict checks especially — returns one of these instead of the real verdict. Always `select(.state != "COMMENTED")`.
- **CodeRabbit replies look like findings**: its `✅ Review thread resolved` acknowledgements are inline comments from `coderabbitai[bot]` carrying a *newer* `pull_request_review_id` than the findings they answer. Only `in_reply_to_id == null` separates them.
- **Polling ends before the incremental review lands**: report `inconclusive`, never "no new findings" — see the honesty rule in 6e. Re-running `/review-pr` is the remedy and costs one round.
