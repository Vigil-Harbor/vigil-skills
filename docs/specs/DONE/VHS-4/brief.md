# VHS-4 — /review-pr: fast path for trivial PRs, evaluate review status via CI check not comment polling

**Status:** Backlog · **Priority:** Medium · **Assignee:** Devin
**Created:** 2026-05-08 · **Plane:** VHS-4
**Origin:** Two related issues from agent-execution feedback during the 2026-05-08 dogfooding pass on `/review-pr`. The skill's incremental-review wait loop is the longest unbroken stretch of dead time in a typical run; both findings target it. Goal is to (a) skip the wait entirely on trivial PRs where the wait's value is near zero, and (b) for the cases where we *do* wait, gate on a signal that's actually authoritative.

## Problem

`skills/review-pr/SKILL.md` Step 6 runs the same six-substep ceremony (6a wait → 6b triage → 6c per-thread reply → 6d poll for resolution + verdict → 6e report) regardless of PR size or finding count. Two issues with that:

1. **Unconditional wait on trivial PRs has near-zero expected value.** Step 6a (`:146–174`) and 6b (`:176–195`) wait up to 5 minutes for CodeRabbit's incremental review of the new commit, then triage any new findings. Empirically, on PRs where the original review surfaced ≤2 findings and all were fix-categorized, CodeRabbit's incremental review of the resulting one-or-two-line fix almost never surfaces new actionable findings — yet the skill blocks for the full polling window every time. For a PR with 1 finding and 1 fix, that's 30s–5min of latency for a check that essentially always returns "no new findings." The 6b loop's 3-round cap protects against pathological cases; it doesn't avoid the latency on the trivial case.

2. **"Review is done" signal is the wrong granularity.** Step 6a's polling query (`:165–169`) is:
   ```bash
   gh api repos/<OWNER>/<REPO>/pulls/<N>/reviews \
     --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.submitted_at > "'"$PUSH_TIME"'")] | length'
   ```
   This treats "a review object exists with `submitted_at > PUSH_TIME`" as proof the incremental review is complete. But the review object lands when the GitHub Reviews API record is created — the walkthrough comment and inline comments are not guaranteed to be posted atomically with the review submission. The skill can race: detect a new review, fetch comments via `pulls/<N>/comments` filtered to `pull_request_review_id`, get an empty or partial set, and conclude "no new actionable findings" while CodeRabbit is still posting. The authoritative "review is done" signal is the CodeRabbit GitHub Check (`gh pr checks <N>`) transitioning through `pending → in_progress → completed`. CodeRabbit publishes a status check per review pass; that check's `completed` state is the moment all walkthrough + inline output has been written.

Both issues live entirely in Step 6 of one SKILL.md. No new tools, no new dependencies, no runtime state — same blast-radius profile as VHS-3.

## Why it matters

- **Latency is the dominant UX cost of `/review-pr` today.** A trivial PR (1–2 findings, 1 fix, no incremental findings) currently spends ~30s on triage and fix work, then 30s–5min in the 6a wait, then ~30s on resolution polling. The wait is the largest single cost and the one most often spent waiting for "nothing happened." Skipping it on the trivial case turns a 2–6min skill into a sub-minute one without changing semantics.
- **A wrong completion signal masquerades as a correct one.** The reviews-API poll usually works because CodeRabbit usually finishes posting comments fast enough. When it doesn't — under CodeRabbit load, large PRs, or pre-merge-check evaluation — the skill silently undercounts findings, posts replies on stale data, and reports "no new findings" while the walkthrough is still being written. The fix is mechanical (gate on `gh pr checks <N>`) but it's load-bearing for correctness in the edge case where the wait actually matters.
- **Bounded blast radius, easy revert.** Both changes are markdown edits inside one SKILL.md. The fast path is gated by a clearly-bounded predicate (≤2 fix-categorized findings, all fix-categorized). The CI-check signal is a drop-in replacement for the existing reviews-API poll with an explicit fallback when no CodeRabbit check is registered. Either change can be reverted with a single-section revert.

## Scope (verified against current code, 2026-05-09 main)

| Section in `skills/review-pr/SKILL.md` | Current behavior | Replacement |
|---|---|---|
| Step 6 preamble (`:142–144`) | Describes per-thread replies + auto-approval gate. No mention of fast path. | Add a one-paragraph fast-path predicate: "If round 1's triage produced ≤2 findings AND all were fix-categorized AND step 5 succeeded, skip 6a/6b after the first push and proceed directly to 6d." Document the rationale and the exit criterion. |
| Step 6a (`:146–174`) | Pre-push verdict short-circuit, then polls `pulls/<N>/reviews` every 30s for up to 5min (extendable to 10min) for a review submitted after `PUSH_TIME`. | Replace the reviews-API poll with `gh pr checks <N>` gating on the CodeRabbit check transitioning to `completed`. After the check completes, fetch the latest review (one query) to capture its ID for use in 6b. Keep the pre-push `APPROVED` short-circuit and the "no CodeRabbit check is running" warn-and-proceed branch. Adjust polling cadence as appropriate for the check-status signal (likely faster than 30s — the check transitions are cheap to query). |
| Step 6b (`:176–195`) | Triage new findings from incremental review, looped up to 3 fix-push-review cycles. | Skip entirely on the fast path. Otherwise unchanged. The 3-round cap stays. |
| Step 6c–6e (`:197–300`) | Per-thread replies, GraphQL polling for `isResolved`, verdict polling, final report. | Unchanged structurally. Step 6e report adds two new lines: (a) `Fast path: yes / no` indicating whether 6a/6b were skipped, (b) `Review completion signal: ci-check / reviews-api-fallback / pre-existing-approval` to make the gating mechanism observable. |
| Edge cases section (`:302–321`) | Documents existing branches. | Add three entries: (i) fast-path triggered, no incremental review observed; (ii) fast-path triggered, manual `/review-pr` re-run later if needed; (iii) CodeRabbit GitHub Check missing or stuck — fall back to reviews-API poll with a 1-minute compatibility timeout, then warn-and-proceed. |

**Preserved (NOT changed):**

- Steps 1–5 (input parsing, repo detection, finding fetch, triage, fix-and-test, commit-and-push). The fast path predicate is evaluated at the *end* of Step 5 / start of Step 6, using the round-1 triage results already in scope.
- The `request_changes_workflow` warning in Step 1b. Auto-approval semantics depend on it regardless of how 6a is gated.
- The pre-push verdict short-circuit at the top of 6a (`:152–161`). If CodeRabbit's last verdict is `APPROVED` and `submitted_at > PUSH_TIME` *before* we enter the new CI-check gate, we still skip 6a/6b. The fast path and the pre-push short-circuit are independent gates that compose.
- Per-thread reply mechanism in Step 6c (the VHS-3 design). The fast path doesn't change replies — it just means the reply happens immediately after Step 5 instead of after Step 6b.
- The 3-round fix-push-review cap in Step 6b. The fast path skips 6b, so the cap is irrelevant on that branch; on the non-fast-path branch the cap is unchanged.
- All of Step 6d Phase 1 (thread-resolution polling) and Phase 2 (verdict polling). The CI-check change is upstream of these.

**Possible scope wrinkle to confirm before kickoff:**

- The exact `gh pr checks <N>` JSON shape and the CodeRabbit check's `name` field. Spec author should run `gh pr checks <N> --json name,state,startedAt,completedAt` on a real PR with CodeRabbit configured and pin the exact filter (likely `select(.name | test("CodeRabbit"; "i"))` or similar). The wiki documents the GitHub Checks integration (`tools/coderabbit/tools/github-checks.md`) but doesn't pin the exact check name — empirical confirmation needed.
- Whether CodeRabbit registers a check at all on PRs where it skipped review (e.g., draft PR, paused review, no diff). The "no check is running" branch must handle that explicitly — see Risks §3.

## Decisions carried forward

1. **Fast-path predicate is conservative: ≤2 findings AND all fix-categorized.** Tighter than "≤2 findings" because a PR with 1 fix-categorized + 1 skip is a different shape — the skip needs to live in 6e's report, and the user may want to re-run if CodeRabbit re-surfaces it. Looser than "1 finding" because the empirical observation in the ticket is "1 finding, 1 fix" but the predicate should cover trivially-similar 2-finding cases. Spec author may tighten to ≤1 if they prefer.
2. **Fast path applies only to round 1.** If a non-fast-path run reaches Step 6b, applies fixes, and pushes again, do NOT re-evaluate the fast path on round 2. The skill is already in the multi-round branch by then; bailing out via fast path mid-loop adds complexity for no benefit.
3. **CI-check signal is the primary; reviews-API is the documented fallback.** If `gh pr checks <N>` returns empty or shows no CodeRabbit-named check after a 1-minute compatibility window, fall back to the existing reviews-API poll. This protects against (a) repos where CodeRabbit's check name has drifted from the wiki's reference, (b) future CodeRabbit changes, (c) GHE/GitLab/Bitbucket variants that the SKILL.md may eventually cover. Report which signal was used in 6e.
4. **Polling cadence adjustments stay conservative.** Initial implementation: keep 30s/5min for the CI-check gate (matches existing reviews-API cadence). The check-status query is cheaper than a reviews-API list, so the spec author may tighten to 15s/3min, but that's a tuning decision — not load-bearing for correctness.
5. **Fast path doesn't change reporting structure.** Step 6e still produces the same fields. Two additions: `Fast path: yes/no` and `Review completion signal: ci-check / reviews-api-fallback / pre-existing-approval`. This makes the new gating mechanism observable in the report without restructuring it.
6. **Manual re-run is the safety valve for the fast path.** If a fast-path run misses an incremental finding (which is exactly the rare case the fast path tolerates), the user can re-run `/review-pr` on the same PR. The skill's existing "fetch latest review" logic (Step 2) will pick up the missed incremental review naturally. Document this in the report's `Fast path: yes` line: `Fast path used — re-run /review-pr if CodeRabbit posts new findings`.

## Approach

1. **Step 6 preamble update.** Add the fast-path predicate definition near the top of Step 6, before 6a. Predicate: `round1_finding_count <= 2 AND all_round1_findings_categorized_as_fix AND step5_pushed_successfully`.
2. **Insert fast-path branch at start of 6a.** Before the pre-push verdict short-circuit, evaluate the predicate. If true: log `Fast path triggered — skipping incremental review wait`, set the report flag, and jump directly to 6d (which has its own skip-Phase-2-if-no-fixes logic that compounds correctly). The pre-push short-circuit and CI-check gate are skipped on the fast path.
3. **6a CI-check gate (replaces reviews-API poll).** Pseudo-flow:
   ```bash
   # Capture push time as before
   HEAD_SHA=$(git rev-parse HEAD)
   PUSH_TIME=$(gh api repos/<O>/<R>/commits/$HEAD_SHA --jq '.commit.committer.date')

   # Pre-push APPROVED short-circuit (unchanged)
   # ...

   # New: gate on CodeRabbit's CI check completing
   # Poll gh pr checks <N>, look for the CodeRabbit check, wait for state == "completed"
   # (or whatever the exact gh pr checks JSON state is — pin in spec)
   gh pr checks <N> --json name,state \
     --jq '.[] | select(.name | test("CodeRabbit"; "i")) | .state'
   ```
   Poll every 30s, up to 5min. On `completed`, fetch the latest review for its ID (one query) and proceed to 6b's triage logic. On timeout with no completed CodeRabbit check, fall back to the existing reviews-API poll for 1min, then warn-and-proceed.
4. **6e report additions.** Two new lines:
   - `Fast path: yes` (with the re-run nudge) or `no`.
   - `Review completion signal: ci-check` / `reviews-api-fallback` / `pre-existing-approval`. The third value is set when the pre-push verdict short-circuit fires.
5. **Edge cases append.** Three new entries (specifics in Scope table above).
6. **Validation harness.** Run the modified `/review-pr` against:
   - A trivial PR with 1 finding and 1 fix → confirm fast-path triggers, total runtime drops by 1–5min, report shows `Fast path: yes`.
   - A non-trivial PR with 3+ findings or a mixed fix/skip set → confirm fast-path does NOT trigger, CI-check gate fires correctly, report shows `Fast path: no` and `Review completion signal: ci-check`.
   - A PR where CodeRabbit's check is missing (e.g., draft, or paused) → confirm fallback to reviews-API poll, report shows `reviews-api-fallback`.
   Pin the exact `gh pr checks` JSON shape and CodeRabbit check name in the spec's Test plan.

## Acceptance criteria

- The fast-path predicate is documented in Step 6's preamble with explicit predicate variables (round-1 finding count, fix-categorization, step-5 success).
- A real `/review-pr` run on a 1-finding, 1-fix PR completes in < 90s end-to-end (fix + push + thread reply + 6d polling) — i.e., no 30s–5min wait for an incremental review.
- A real `/review-pr` run on a 3+ finding PR (or any non-fast-path case) gates on `gh pr checks <N>` showing the CodeRabbit check `completed`, then fetches comments. The report's `Review completion signal` field reads `ci-check`.
- A real `/review-pr` run on a PR where `gh pr checks <N>` returns no CodeRabbit-named check (within the 1-min compatibility window) falls back to the existing reviews-API poll. The report's `Review completion signal` field reads `reviews-api-fallback`.
- The pre-push `APPROVED` short-circuit still fires when the latest verdict is `APPROVED` with `submitted_at > PUSH_TIME` *before* either gate is evaluated. Report's `Review completion signal` reads `pre-existing-approval` in that case.
- `grep -n 'pulls/<N>/reviews' skills/review-pr/SKILL.md` shows the reviews-API call only inside the fallback branch and the existing pre-push short-circuit — never as the primary gate.
- Per-thread replies (VHS-3 design) still post correctly on the fast path: replies fire immediately after Step 5's push, against the round-1 fix-categorized findings, with `HEAD_SHORT_SHA` from that push.
- The 3-round fix-push-review cap in Step 6b still works on the non-fast-path branch (no regression).
- `python sync.py status` shows the SKILL.md edit cleanly diffed; `python sync.py push` produces a byte-for-byte match in `~/.claude/skills/review-pr/SKILL.md`.
- Step 6e report includes both new fields (`Fast path:` and `Review completion signal:`) on every run.

## Out of scope

- Tightening the fast-path predicate beyond ≤2 fix-only findings. If empirical observation later shows the predicate should be ≤1 or ≤3, that's a one-line tuning patch — not part of v1.
- Replacing the GraphQL thread-resolution poll in Step 6d with a check-status signal. Thread resolution is a CodeRabbit-internal state, not a CI check; the GraphQL approach is correct for that step.
- Adding new MCP tools or wrapping `gh pr checks` behind a helper. Direct `gh pr checks` invocation matches existing skill style.
- Cross-platform CI-check support (GitLab, Bitbucket, Azure DevOps). The skill is GitHub-only today; adding other platforms is a separate brief.
- Skipping the verdict poll in Step 6d Phase 2 on the fast path. Phase 2 is gated by `request_changes_workflow` and "all threads resolved" — both still need to be checked. Fast path only skips 6a/6b.
- Detecting whether the resulting fix is actually a no-op (e.g., the user's fix matches what CodeRabbit suggested verbatim, so no incremental review will trigger). That's a heuristic-on-heuristic; not worth the complexity.
- Backfilling old PRs that were resolved under the old (slower) flow. Cosmetic-only; not worth the cycles.

## Risks / decisions

1. **CodeRabbit check name drift.** The skill must filter `gh pr checks` output by the CodeRabbit check's `name`. If CodeRabbit renames its check (e.g., `CodeRabbit` → `CodeRabbit AI` → `coderabbitai`), the filter breaks. Decision: case-insensitive substring match on `coderabbit` (`select(.name | test("coderabbit"; "i"))`). Spec author confirms exact form during validation harness.
2. **CodeRabbit not registering a check at all.** On draft PRs, paused reviews, or repos where the GitHub Checks integration is disabled, no CodeRabbit check appears in `gh pr checks` output. The 1-minute compatibility timeout (Decision §3 above) handles this — fall back to reviews-API poll. Spec author should explicitly test this branch (a draft PR is the cheapest repro).
3. **Stuck or failing CodeRabbit checks.** Rare but possible: the CodeRabbit check enters `failed` or `stuck`. The skill should treat `failed` as terminal (proceed without finding new comments — CodeRabbit didn't review) and report it in 6e. `stuck` is harder; the 5-min polling timeout will eventually fire and the skill falls back. Acceptable for v1.
4. **Race between commit push and check registration.** When the skill polls `gh pr checks` immediately after pushing, the CodeRabbit check may not yet be registered. The first 1–2 polls may see no check, then it appears and starts. The 1-minute compatibility window must be measured from "started polling" not "first failed poll" — otherwise we may falsely fall back when the check just hasn't registered yet. Implementation note: only fall back if the CodeRabbit check is *still* missing after the compatibility window elapses, not if it's missing on the first poll.
5. **Fast path interaction with the pre-push `APPROVED` short-circuit.** Both gates can fire on round 1; their compositions need to be unambiguous. Decision: fast-path check runs *before* the pre-push short-circuit (Step 6a top). If fast path triggers, we don't even read the latest verdict — we just go to 6d. If fast path doesn't trigger, the pre-push short-circuit runs as today, then the CI-check gate runs if the short-circuit doesn't fire. This ordering means a trivial PR with a pre-existing `APPROVED` verdict still goes through the fast path (correct: the user already saw "approved," and 6d will confirm threads are resolved before reporting).
6. **Fast path masking real findings.** The whole premise is "trivial PRs almost never surface new findings on incremental review." If that empirical assumption is wrong on the user's repos, the fast path will silently miss findings. Mitigations: (a) Decision §6 — manual re-run is the documented safety valve, (b) Step 6e report explicitly says `Fast path used — re-run /review-pr if CodeRabbit posts new findings`, (c) the predicate is conservative (≤2 fix-only). Spec author should run the validation harness on real trivial PRs and pin the false-negative rate.
7. **Reviews-API fallback hides regressions.** If the CI-check gate is broken in some way that causes it to silently always fall back, the skill behavior reverts to today's. Mitigation: Step 6e reports the signal used. If users see `reviews-api-fallback` consistently when they expect `ci-check`, the regression is observable. Add a one-line operator note to the skill's edge cases section.
8. **Polling-cadence interaction with the 3-round cap.** If 6a polling is faster (15s) but each round still incurs the polling overhead, the worst-case 3-round latency on the non-fast-path branch is `3 × 5min = 15min`. Today's worst case is the same. Not a regression, but a reminder that the fast path is the optimization for trivial PRs; non-trivial PRs still incur the wait.

## References

- Plane: VHS-4
- Skill: `skills/review-pr/SKILL.md` (current implementation, ~322 lines)
- Predecessor brief / spec (per-thread replies, related Step 6 changes): `docs/specs/TODO/VHS-3.brief.md`, `docs/specs/TODO/VHS-3.spec.md`
- CodeRabbit GitHub Checks integration (mirrored): `vigil-harbor-wiki/tools/coderabbit/tools/github-checks.md` — describes the checks integration but does not pin the exact check `name` field; spec author verifies via `gh pr checks` on a real PR
- CodeRabbit auto-incremental review configuration (mirrored): `vigil-harbor-wiki/tools/coderabbit/configuration/auto-review.md` § `auto_incremental_review` — confirms incremental reviews fire on every push by default, which is the latency this brief addresses
- CodeRabbit `request_changes_workflow` semantics: `vigil-harbor-wiki/tools/coderabbit/reference/glossary.md:70`
- Status check terminology cross-platform: `vigil-harbor-wiki/tools/coderabbit/reference/glossary.md:100` § "Status Check"
- Workflow context: `vigil-skills/CLAUDE.md` § "/review-pr"
- GitHub CLI — `gh pr checks` JSON output (verify exact JSON shape and CodeRabbit check name in spec)
- Current call sites verified 2026-05-09 via `Read skills/review-pr/SKILL.md`
