# VHS-4 — /review-pr: fast path for trivial PRs, CI-check gate for review completion

## Goal

Add two optimizations to `/review-pr` Step 6, both targeting the incremental-review wait loop. First, a fast path that skips the wait entirely on trivial PRs (≤2 fix-only findings from round 1) where the incremental review almost never surfaces new findings. Second, replace the reviews-API poll in Step 6a with a `gh pr checks` gate on CodeRabbit's own status check, which is the authoritative "review is done" signal — the current reviews-API poll can race with incomplete comment posting.

## Scope

| File | Change |
|------|--------|
| `skills/review-pr/SKILL.md` | Step 6 preamble, Step 6a, Step 6e report template, edge cases section |
| `CLAUDE.md` | Update /review-pr description (line ~45): add "conditionally" before "waits for CodeRabbit's incremental re-review" to reflect the fast-path skip |

**Preserved (NOT changed):**

- Steps 1–5 (input parsing, repo detection, finding fetch, triage, fix-and-test, commit-and-push, per-thread replies). The fast-path predicate is evaluated at the boundary of Step 5 → Step 6, using triage results already in scope.
- Step 6b (triage new findings from incremental review, 3-round cap). Unchanged on the non-fast-path branch; skipped on the fast-path branch.
- Step 6c (per-thread reply mechanism). Unchanged — replies fire after each push regardless of fast path.
- Step 6d (thread-resolution polling, verdict polling). Unchanged structurally. Fast path proceeds directly to 6d after Step 5's push + replies.
- Step 6e structure. Two new fields added; existing fields unchanged.
- `request_changes_workflow` warning (Step 1b).
- YAML frontmatter.

## Decisions

### D1: Fast-path predicate — ≤2 findings AND all fix-categorized AND step 5 pushed

The predicate is: `round1_finding_count <= 2 AND all_round1_findings_fix_categorized AND step5_push_succeeded`. This is conservative by design:
- "≤2" covers the empirical sweet spot (1–2 finding trivial PRs) without being so loose that it masks real issues.
- "all fix-categorized" excludes PRs with skips — those have open threads that the user may want CodeRabbit to re-evaluate.
- "step 5 pushed" guards two cases: (a) if no push happened (all non-fix), 6a already short-circuits via the existing "no fixes were pushed" branch, and (b) the degenerate zero-finding case where `all_fix_categorized` is vacuously true but no push occurred.

**Why:** Brief Decision §1. The predicate is tight enough that false negatives (missing a real incremental finding) are rare, and the safety valve (re-run `/review-pr`) is zero-cost.

**How to apply:** Evaluate at the top of Step 6a, before any other gate.

### D2: Fast path applies only to round 1

If the skill enters the 6b multi-round loop, it is by definition not trivial. Re-evaluating the fast path mid-loop adds complexity for no benefit.

**Why:** Brief Decision §2.

**How to apply:** The fast-path predicate references "round 1" explicitly. Step 6b's loop-back-to-6a path does not re-check the predicate.

### D3: CI-check gate is primary, reviews-API is fallback

Replace the reviews-API poll (`pulls/<N>/reviews` filtered by `submitted_at > PUSH_TIME`) with `gh pr checks <N> --json name,state` gating on the CodeRabbit check transitioning to a terminal state (`SUCCESS` or `FAILURE`). After the check completes, fetch the latest review for its ID (one query) to hand off to 6b.

If no CodeRabbit-named check appears within a 1-minute compatibility window (measured from first poll, not first miss), fall back to the existing reviews-API poll for the remainder of the 5-minute window. This protects against repos where CodeRabbit's check isn't registered (draft PRs, paused reviews, disabled integration).

**Why:** Brief §Problem item 2. The reviews-API poll can race with incomplete comment posting. The CodeRabbit status check is the authoritative "all output has been written" signal.

**How to apply:** Replace the poll body in Step 6a. Keep the pre-push `APPROVED` short-circuit above it.

### D4: Check name filter — case-insensitive match on "coderabbit"

Empirically confirmed: `gh pr checks <N> --json name,state` returns `{"name": "CodeRabbit", "state": "SUCCESS"}` on this repo. The filter uses case-insensitive match (`test("coderabbit"; "i")`) to handle potential name variations across CodeRabbit versions.

**Why:** Brief Risk §1. Pin the filter based on empirical observation, but make it resilient to capitalization drift.

**How to apply:** jq filter in the 6a poll command.

### D5: Composition order — fast path → pre-push short-circuit → CI-check gate → reviews-API fallback

Four stages compose at the top of Step 6a:

1. **Fast path** (D1): if true, skip 6a/6b entirely → proceed to 6d.
2. **Pre-push `APPROVED` short-circuit** (existing): if latest verdict is `APPROVED` with `submitted_at > PUSH_TIME`, skip 6a/6b → proceed to 6e.
3. **CI-check gate** (D3): poll `gh pr checks` for CodeRabbit completion.
4. **Reviews-API fallback** (D3): if no CodeRabbit check found within 1 minute, fall back to existing `pulls/<N>/reviews` poll. This is not independent of stage 3 — it activates only when the CI-check gate finds no check.

The fast path is first because it avoids the PUSH_TIME capture and verdict fetch entirely. Stages 1 and 2 are independent of each other and of stages 3–4.

**Why:** Brief Decision §5.

### D6: Report observability — two new fields in Step 6e

- `Fast path: yes — re-run /review-pr if CodeRabbit posts new findings` or `Fast path: no`
- `Review completion signal: ci-check / ci-check (FAILURE) / ci-check (timeout) / reviews-api-fallback / pre-existing-approval / fast-path`

These make the new gating mechanism observable without restructuring the report.

**Why:** Brief Decision §5.

### D7: CodeRabbit check `FAILURE` is terminal

If the CodeRabbit check completes with state `FAILURE`, treat it as terminal: CodeRabbit encountered an error and did not post findings. Proceed to 6d without entering 6b. Report `Review completion signal: ci-check (FAILURE)`.

**Why:** Brief Risk §3. `FAILURE` is rare but shouldn't block the skill indefinitely.

### D8: Stale-check guard on round 2+ re-entry

When Step 6b loops back to 6a after a round-2 push, the CodeRabbit CI check from round 1 still shows `SUCCESS`. The new check for round 2 has not yet registered. Without a guard, the CI-check gate would immediately declare the incremental review complete using the stale `SUCCESS`.

Fix: on re-entry to 6a from 6b, the CI-check gate must first observe the check transition away from `SUCCESS` (i.e., to `PENDING`, indicating the new run started) before gating on the next `SUCCESS`. If the check does not transition away from `SUCCESS` within the 1-minute compatibility window, fall back to reviews-API poll (the temporal filter `submitted_at > PUSH_TIME` naturally handles staleness).

**Why:** The existing reviews-API poll avoided this via `submitted_at > PUSH_TIME`. The CI-check gate has no analogous temporal filter — `gh pr checks` returns current state, not history.

**How to apply:** The 6a design section includes a "Re-entry from 6b" note with the transition guard.

## Design

### Step 6 preamble: Add fast-path predicate

Insert after the existing preamble paragraph (line 142–144), before Step 6a:

```markdown
**Fast-path predicate (evaluated once, after Step 5):**

```
FAST_PATH = (round1_finding_count <= 2
             AND every round-1 finding is categorized as "fix"
             AND step 5 pushed successfully)
```

If `FAST_PATH` is true, skip Steps 6a and 6b entirely — proceed directly to Step 6d. Log: `Fast path triggered — skipping incremental review wait (≤2 fix-only findings)`. The rationale: on trivial PRs (1–2 fix-only findings), CodeRabbit's incremental review of the resulting small fix almost never surfaces new actionable findings. The 30s–5min wait in 6a has near-zero expected value. If CodeRabbit does post new findings, re-running `/review-pr` on the same PR picks them up naturally.
```

### Step 6a: Replace reviews-API poll with CI-check gate

Replace the entire 6a section (lines 146–173 of the current SKILL.md) with the following structure. The pre-push `APPROVED` short-circuit and "no fixes were pushed" branch are preserved.

```markdown
### 6a. Wait for CodeRabbit's incremental review (only if fixes were pushed)

If no fixes were pushed (all skips/duplicates/already-fixed), skip to 6d.

**If FAST_PATH is true**, set `REVIEW_SIGNAL=fast-path` and skip to 6d. (Per-thread replies were already posted in Step 5.)

**Otherwise, capture push time and check for pre-existing approval:**

```bash
HEAD_SHA=$(git rev-parse HEAD)
PUSH_TIME=$(gh api repos/<OWNER>/<REPO>/commits/$HEAD_SHA --jq '.commit.committer.date')

gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]")] | sort_by(.submitted_at) | last | {state, submitted_at}'
```

If the latest verdict's `state` is `APPROVED` **and its `submitted_at` is after `PUSH_TIME`**, skip 6a/6b and go straight to 6e. Set `REVIEW_SIGNAL=pre-existing-approval`. (This skips 6d — the existing behavior, preserved from the current SKILL.md; `APPROVED` implies threads are resolved or will be imminently.) A pre-push `APPROVED` verdict must not short-circuit: the incoming incremental review may flip it back to `CHANGES_REQUESTED`.

**Otherwise, gate on CodeRabbit's CI check completing:**

```bash
gh pr checks <N> --json name,state \
  --jq '[.[] | select(.name | test("coderabbit"; "i")) | .state] | if length == 0 then "NONE" elif any(. == "PENDING") then "PENDING" elif all(. == "SUCCESS") then "SUCCESS" else "FAILURE" end'
```

The jq aggregation handles four cases: if no CodeRabbit-named checks exist, return `NONE` (triggers the "no check found" fallback); if any is `PENDING`, treat the overall state as `PENDING`; if all are `SUCCESS`, treat as `SUCCESS`; otherwise `FAILURE` (catches `FAILURE`, `CANCELLED`, `ERROR`, `STALE`, and any other non-standard GitHub check state — conservative and safe).

Poll by making **individual Bash tool calls** every 15 seconds (brief Decision 4 authorizes tightening from 30s since check-status queries are cheaper than reviews-API lists). Note the wall-clock time at first poll as `FIRST_POLL_TIME` — this is conversational state tracked by the LLM across tool calls, not a persistent shell variable (individual Bash calls do not share state). Outcomes:

- **CodeRabbit check returns `SUCCESS`:** set `REVIEW_SIGNAL=ci-check`. Fetch the latest CodeRabbit review to capture its `id` for Step 6b:
  ```bash
  gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
    --jq '[.[] | select(.user.login == "coderabbitai[bot]")] | sort_by(.submitted_at) | last | .id'
  ```
  Proceed to 6b.

- **CodeRabbit check returns `FAILURE`:** set `REVIEW_SIGNAL=ci-check (FAILURE)`. CodeRabbit errored — no incremental findings expected. Proceed to 6d (skip 6b).

- **CodeRabbit check returns `NONE` (no check found):** Track how long since `FIRST_POLL_TIME`. Early `NONE` results are expected (push-to-check registration race). After 1 minute of continuous `NONE`, fall back to reviews-API poll for the remaining time (up to 5 minutes total from first poll). Set `REVIEW_SIGNAL=reviews-api-fallback`.
  ```bash
  # Detection query (returns count):
  gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
    --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.submitted_at > "'"$PUSH_TIME"'")] | length'

  # Once count > 0, capture the review ID:
  gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
    --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.submitted_at > "'"$PUSH_TIME"'")] | last | .id'
  ```
  When a new review is detected, capture its `id` for Step 6b. If timeout with no new review, proceed to 6d — CodeRabbit may have decided the diff didn't warrant a re-review.

- **CodeRabbit check found but still `PENDING` after 5 minutes:** extend to 10 minutes total (preserved from current 6a behavior). During the extension, also check the reviews-API as a parallel signal — if a new review is detected via reviews-API while the check is still `PENDING`, use the review and proceed to 6b (set `REVIEW_SIGNAL=reviews-api-fallback`). If still pending after 10 minutes, set `REVIEW_SIGNAL=ci-check (timeout)`, warn-and-proceed to 6d.

**Re-entry from 6b (round 2+ guard):** When 6b loops back to 6a after a subsequent push, the CodeRabbit CI check from the prior round still shows `SUCCESS`. Before gating on `SUCCESS`, the skill must first observe the check transition to `PENDING` (indicating the new review run started). If the check does not transition away from `SUCCESS` within 1 minute, fall back to reviews-API poll (whose `submitted_at > PUSH_TIME` filter naturally handles staleness).

When a new review is detected (via either signal), capture its `id` for use in Step 6b.
```

### Step 6b: Fast-path skip note

No structural change to Step 6b. Add a one-line note at the top:

```markdown
(Skipped entirely when FAST_PATH is true — proceed to 6d.)
```

The 6b loop's internal loop-back-to-6a does NOT re-evaluate the fast-path predicate. Once the skill is in the 6b loop, it stays on the non-fast-path branch.

### Step 6e: Two new report fields

Add after the existing `CodeRabbit verdict:` line:

```text
- Fast path: yes — re-run /review-pr if CodeRabbit posts new findings / no
- Review completion signal: ci-check / ci-check (FAILURE) / ci-check (timeout) / reviews-api-fallback / pre-existing-approval / fast-path
```

`fast-path` is the value when `FAST_PATH` is true (the review-completion gate was bypassed). Named parallel to `ci-check` — describes the mechanism, not what was skipped.

### Edge cases: Eight new entries

Append to the existing edge cases section:

```markdown
- **Fast path triggered, no incremental review observed**: expected behavior — the fast path intentionally skips 6a/6b. If CodeRabbit posts new findings after the run, re-run `/review-pr` to pick them up.
- **Fast path triggered but CodeRabbit posts new findings before 6d completes**: 6d's thread-resolution polling may observe unresolved threads from the new findings. The report will show them as unresolved with the manual resolve command. Re-run `/review-pr` to triage.
- **CodeRabbit check missing or stuck — fallback to reviews-API**: if `gh pr checks <N>` returns no CodeRabbit-named check within 1 minute of first poll, fall back to reviews-API poll. Report shows `Review completion signal: reviews-api-fallback`. Common causes: draft PR, paused review, CodeRabbit Checks integration disabled.
- **CodeRabbit check `FAILURE`**: CodeRabbit encountered an error and did not post findings. Proceed to 6d (skip 6b). Report shows `Review completion signal: ci-check (FAILURE)`.
- **CodeRabbit check stuck `PENDING` for 10 minutes**: the PENDING extension window expires. Set `REVIEW_SIGNAL=ci-check (timeout)`, warn, proceed to 6d. Report shows the timeout signal for observability.
- **Race between push and check registration**: the CodeRabbit check may not appear on the first 1–2 polls after push. The 1-minute compatibility window is measured from first poll, not first miss — early misses do not trigger fallback.
- **Reviews-API fallback hides CI-check regression**: if `reviews-api-fallback` appears consistently when `ci-check` is expected, the CI-check filter may be broken. Report makes this observable.
- **Stale CI check on round 2+ re-entry**: after 6b pushes and loops back to 6a, the round-1 CodeRabbit check still shows `SUCCESS`. The re-entry guard waits for `PENDING` before gating on the next `SUCCESS`. If the check never transitions (CodeRabbit skipped re-review), the 1-minute window expires and the skill falls back to reviews-API.
```

## Test plan

### Static verification

1. **Fast-path predicate present.**
   ```bash
   grep -n "FAST_PATH" skills/review-pr/SKILL.md
   ```
   Expected: matches in Step 6 preamble (predicate definition), Step 6a (evaluation), Step 6b (skip note).

2. **CI-check gate present.**
   ```bash
   grep -n 'gh pr checks' skills/review-pr/SKILL.md
   ```
   Expected: matches in Step 1 (existing), Step 6a (new CI-check gate).

3. **Reviews-API poll only in fallback + pre-push short-circuit.**
   ```bash
   grep -n 'pulls.*reviews' skills/review-pr/SKILL.md
   ```
   Expected: Step 2 (finding fetch — unchanged), Step 6a pre-push short-circuit (unchanged), Step 6a CI-check SUCCESS branch (review-ID fetch — new), Step 6a fallback branch (new), Step 6d Phase 2 (unchanged). NOT in the primary 6a gate.

4. **Report fields present.**
   ```bash
   grep -n 'Fast path:\|Review completion signal:' skills/review-pr/SKILL.md
   ```
   Expected: both in the 6e report template.

5. **Sync check.**
   ```bash
   python sync.py status
   ```
   Expected: `skills/review-pr/SKILL.md` shows as differing (repo ahead of installed). After `python sync.py install`, clean.

### Empirical validation

6. **Trivial PR — fast path fires.** Run `/review-pr` on a PR with 1–2 findings, all fix-categorized. Confirm: fast path triggers, no 6a/6b wait, total runtime <90s, report shows `Fast path: yes` and `Review completion signal: fast-path`.

7. **Non-trivial PR — CI-check gate fires.** Run `/review-pr` on a PR with 3+ findings or mixed fix/skip. Confirm: fast path does NOT trigger, 6a gates on `gh pr checks` showing `SUCCESS`, report shows `Fast path: no` and `Review completion signal: ci-check`.

8. **No CodeRabbit check — fallback fires.** Run `/review-pr` on a draft PR or a repo where CodeRabbit skips review. Confirm: 1-minute timeout, fallback to reviews-API poll, report shows `Review completion signal: reviews-api-fallback`.

9. **Pre-push APPROVED short-circuit.** If available, test a PR where CodeRabbit has already approved after the push (rare timing). Confirm: report shows `Review completion signal: pre-existing-approval`.

10. **No regression.** Per-thread replies (VHS-3) still fire correctly. 3-round cap in 6b still works. `request_changes_workflow` warning unchanged. Infrastructure-error re-trigger (Step 2) unchanged.

11. **Multi-round non-trivial PR — CI-check gate handles round-2 correctly.** Run `/review-pr` on a PR where round 1 produces fixes AND the incremental review produces new fix-worthy findings. Confirm: after round-2 push, 6a correctly waits for the NEW CodeRabbit check (observes transition through `PENDING`) before proceeding to 6b round 2 — does not short-circuit on stale round-1 `SUCCESS`.

12. **CLAUDE.md updated.** `grep "conditionally" CLAUDE.md` matches the /review-pr description.

## Test command

```bash
python sync.py status && grep -c "FAST_PATH" skills/review-pr/SKILL.md && grep -c "gh pr checks" skills/review-pr/SKILL.md && grep -c "Review completion signal:" skills/review-pr/SKILL.md
```

This repo has no executable test suite. The combined command verifies: (1) SKILL.md syncs cleanly, (2) FAST_PATH references present, (3) `gh pr checks` gate present, (4) new report field present. Empirical validation (real PR runs) is described above.

## Done when

1. Step 6 preamble defines the fast-path predicate with explicit variables (`round1_finding_count`, `all_round1_findings_fix_categorized`, `step5_push_succeeded`).
2. Step 6a evaluates the fast-path predicate before any other gate; when true, skips to 6d.
3. Step 6a's primary wait gate is `gh pr checks <N> --json name,state` filtered case-insensitively for `coderabbit`, polling every 15s.
4. Step 6a falls back to reviews-API poll if no CodeRabbit check appears within 1 minute of first poll.
5. The pre-push `APPROVED` short-circuit is preserved, runs after fast-path check and before CI-check gate.
6. Step 6b notes it is skipped on the fast path; its internal loop-back does not re-evaluate the fast-path predicate.
7. Step 6e report includes `Fast path: yes/no` and `Review completion signal: ci-check / ci-check (FAILURE) / ci-check (timeout) / reviews-api-fallback / pre-existing-approval / fast-path`.
8. Edge cases section includes entries for: fast-path triggered, CodeRabbit check missing/fallback, CodeRabbit check FAILURE, PENDING timeout, push-to-check registration race, fallback regression observability.
9. `grep -n 'pulls.*reviews' skills/review-pr/SKILL.md` shows the reviews-API call only in: Step 2 (finding fetch), Step 6a pre-push short-circuit, Step 6a CI-check SUCCESS branch (review-ID fetch), Step 6a fallback branch, Step 6d Phase 2 verdict polling — never as the primary 6a gate.
10. `python sync.py status` shows clean diff after install.
11. Per-thread replies (VHS-3) still fire correctly on the fast path (replies post after Step 5, before 6d).
12. The 3-round fix-push-review cap in Step 6b still works on the non-fast-path branch.
13. Step 6a includes a re-entry guard for round 2+: wait for CI check to transition through `PENDING` before gating on `SUCCESS`, with fallback to reviews-API if the check doesn't transition within 1 minute.
14. `CLAUDE.md` /review-pr description updated to reflect conditional wait behavior.
15. The CI-check jq filter aggregates multiple CodeRabbit-named checks conservatively (any `PENDING` → overall `PENDING`).

## Out of scope

1. Tightening or loosening the fast-path predicate beyond ≤2 fix-only — tuning patch, not v1.
2. Replacing the GraphQL thread-resolution poll in Step 6d with a check-status signal — thread resolution is CodeRabbit-internal state, not a CI check.
3. Adding new MCP tools or wrapping `gh pr checks` behind a helper — direct CLI matches skill style.
4. Cross-platform CI-check support (GitLab, Bitbucket) — GitHub-only today.
5. Skipping Step 6d verdict poll on the fast path — Phase 2 entry still requires "all threads resolved" check.
6. Detecting no-op fixes (fix matches CodeRabbit suggestion verbatim) — heuristic-on-heuristic.
7. Backfilling old PRs resolved under the slower flow.
8. Changing polling cadence in Step 6d (thread-resolution or verdict polling) — those are downstream of the 6a change and work fine as-is.

## Deferred (P2+)

- **reviews-API fallback signal doesn't distinguish success from timeout** (edge-cases R3/F-2): `REVIEW_SIGNAL=reviews-api-fallback` is set at fallback entry regardless of outcome. Could add `reviews-api-fallback (timeout)` for parity with CI-check path.
- **FIRST_POLL_TIME not documented as reset on re-entry** (edge-cases R3/F-3): On round 2+ re-entry from 6b, FIRST_POLL_TIME should be reset so the timeout window is per-round. Currently implicit.
- **PUSH_TIME not documented as conversational state** (edge-cases R3/F-4): FIRST_POLL_TIME has an explicit note (line 151); PUSH_TIME should have the same clarification.
- **gh CLI `state` field may differ across versions** (edge-cases R3/F-7): Older/newer `gh` versions may use `conclusion`+`status` instead of `state`. Conservative `else FAILURE` catch-all handles it safely.
