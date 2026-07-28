# VHS-3 — /review-pr: per-thread "Resolved in <hash>" replies, drop bulk @coderabbitai resolve

## Goal

Replace the single-shot `@coderabbitai resolve` PR comment in `/review-pr` Step 6c with per-thread inline replies on each fix-categorized finding, each containing the resolving commit SHA. Skipped-finding threads stay open for CodeRabbit and the user to handle naturally. Bulk `@coderabbitai resolve` is removed from the skill's automated flow entirely — the user can post it manually if needed, but the skill never force-resolves. The skill's thread-closure mechanism stops being a hidden second knob for nit volume — `.coderabbit.yaml` (profile, path filters, review mode) becomes the single point of control.

## Scope

| File | Change |
|------|--------|
| `skills/review-pr/SKILL.md` | Step 5, Step 6 header, Step 6a (forward-reference update), Step 6b (forward-reference update + reply injection), Step 6c (full rewrite), Step 6d, Step 6e, edge cases |
| `CLAUDE.md` | Update /review-pr description (line ~45): "resolves threads via `@coderabbitai resolve`" → "resolves threads via per-thread commit-hash replies" |

**Preserved (NOT changed):**

- Steps 1–4 (input parsing, repo detection, CodeRabbit config check, finding fetch, triage, fix-and-test). Severity table, triage rules, test discovery unchanged.
- Step 6a/6b loop structure (wait for incremental review, triage new findings, 3-round cap) — unchanged. Forward references and post-push behavior within 6a/6b are updated (see Design § Steps 6a/6b).
- `request_changes_workflow` warning in Step 1b.
- YAML frontmatter.

## Decisions

### D1: Reply phrasing — `Resolved in <short-sha>`

Use `Resolved in <short-sha>` as the canonical per-thread reply body. Matches CodeRabbit's own "resolved" language and the user's example (`Resolved in fc701f2`). The brief's acceptable set (`Fixed in`, `Fixed,`, `Addressed in`) are alternates for future variability across runs, but v1 uses one phrase consistently.

### D2: Short SHA, not full

Seven-character form via `git rev-parse --short HEAD`. Matches GitHub's display convention and CodeRabbit walkthrough comments.

### D3: No automated fallback — report-only on unresolved threads

**Brief departure.** The brief's Decision §3 says "fallback to bulk resolve on polling timeout." This spec removes the automated fallback entirely. When fix-threads don't auto-resolve within the polling window, the skill reports the unresolved thread paths and offers the manual command (`gh pr comment <N> --body "@coderabbitai resolve"`) — it does not auto-fire it.

Rationale (user quote, 2026-05-08): "I want to specifically try to let the reviewer run through its natural process of actually gating approval, not forcing. It's on 'chill', shouldn't be too hard. Then later we can tune coderabbitai on a harder set that's actually geared for our operation, not just generic."

If empirical validation (D7) shows hash replies never auto-resolve threads, the next step is to evaluate `resolveReviewThread` GraphQL mutation as a surgical middle layer (see Out of scope §8) — not to fall back to the blunt `@coderabbitai resolve`.

### D4: Skipped/duplicate/already-fixed findings — no reply, threads left open

No reply is posted on non-fix finding threads (skip, duplicate, or already-fixed). These threads remain open, which means:
- CodeRabbit's verdict stays `CHANGES_REQUESTED` until the user manually resolves them (or re-runs `/review-pr` with different triage decisions, or posts `@coderabbitai resolve` by hand).
- This is the desired behavior: CodeRabbit acts as a genuine gate, not a rubber stamp.
- This is a behavioral change from the current skill, which bulk-resolves all threads including skips.
- `already-fixed` is explicitly grouped with skip/duplicate throughout the spec. The current SKILL.md has four categories (fix, skip, duplicate, already-fixed) — three of those are non-fix.

### D5: One commit per round, mapped to all fix-findings from that round

No change from the current skill. All fixes from one round are bundled into a single commit. The mapping is `{ all fix-findings from round N → HEAD SHA after push N }`. Per-thread replies are posted immediately after each push (not batched at the end), so each finding's reply contains the correct SHA for the round it was fixed in.

### D6: "All skips/duplicates/already-fixed" branch — report only, no resolution

When all findings are categorized as non-fix:
- No fixes → no push → no SHA → no per-thread replies.
- Steps 6a/6b short-circuit (no incremental review to wait for).
- Step 6c short-circuits (no fix-findings to reply on).
- Step 6d short-circuits (no fix-threads to poll; no verdict expected with open threads).
- Go directly to Step 6e report.

**Brief departure.** The brief's Risk §4 assumed the fallback would fire for all-skips. This spec instead short-circuits to report-only because: no fix-threads = nothing to wait for; skipped threads are intentionally open per D3.

This is a behavioral change: the current skill posts `@coderabbitai resolve` in this case. The new behavior leaves threads open and reports them.

### D7: Empirical validation required before merge

The brief's Risks §1 identifies an undocumented assumption: does posting a commit-hash reply on a CodeRabbit thread cause CodeRabbit (or GitHub) to auto-resolve that thread? The answer must be pinned empirically during implementation via a test PR run (see Test plan § Empirical validation). D3's report-only design means the skill terminates cleanly regardless of the answer — but the primary value proposition (per-thread replies as the closure mechanism) depends on auto-resolution working.

### D8: Phase 2 entry condition — scope addition beyond brief

**Brief departure.** The brief's scope table says "Step 6d Phase 2: Unchanged." This spec adds entry conditions that skip Phase 2 when non-fix threads are open (because APPROVED verdict won't come with unresolved threads). The polling mechanics themselves are unchanged — only the decision to enter Phase 2 changes. This is a necessary consequence of D4 (skipped threads stay open).

## Design

### Step 5: Capture resolving commit SHA

After the push succeeds (line ~119), add:

```bash
HEAD_SHORT_SHA=$(git rev-parse --short HEAD)
```

Immediately post per-thread replies for all fix-categorized findings from **this round** (see Step 6c for the reply mechanism). Then continue to Step 6a.

### Steps 6a/6b: Forward-reference updates + reply injection

The 6a/6b loop structure is unchanged, but four edits are needed:

1. **6a skip target (line 129).** Change "skip to 6c" → "skip to 6d" (the all-non-fix branch no longer has a standalone 6c resolve step to skip to; it proceeds to polling or directly to 6e per D6).

2. **6b reply injection (line 168).** After the 6b push ("apply fixes, run tests, commit, push"), insert the same SHA-capture + reply-posting sequence described in Step 5: capture `HEAD_SHORT_SHA=$(git rev-parse --short HEAD)`, then post per-thread replies for this round's fix-categorized findings using the Step 6c mechanism. Then loop back to 6a.

3. **6b cap-reached flow (lines 169–174).** Change "proceed to 6c" → "proceed to 6d." Update the warning message from "Proceeding to resolve threads" to "Proceeding to check thread resolution status" (replies for the final round were already posted after the push).

4. **6b no-new-findings exit (line 176).** Change "proceed to 6c" → "proceed to 6d." This is the branch where the incremental review returns only duplicates/already-fixed findings — no new fixes needed, proceed to polling.

### Step 6 header: Reframe around per-thread replies

Replace the current header prose (SKILL.md line 125, which frames Step 6 around `@coderabbitai resolve`) with prose that frames it around per-thread commit-hash replies. The new framing:

Per-thread `Resolved in <sha>` replies on fix-categorized finding threads are the primary closure mechanism. Threads for non-fix findings (skip/duplicate/already-fixed) are left open for CodeRabbit and the user to handle naturally. Auto-approval (`APPROVED` verdict) requires all threads resolved AND `request_changes_workflow: true` AND pre-merge checks passing.

### Step 6c: Per-thread commit-hash replies (full rewrite)

**Placement change:** Step 6c is no longer a standalone post-loop step. Per-thread replies are posted immediately after each push — both after Step 5's initial push and after each Step 6b fix-push cycle. This ensures each reply contains the correct SHA for the round that fixed the finding.

**Reply mechanism:**

For each fix-categorized finding from the current round, post an inline reply on the originating review-comment thread:

```bash
gh api -X POST \
  repos/<OWNER>/<REPO>/pulls/<N>/comments/<COMMENT_ID>/replies \
  -f body="Resolved in <HEAD_SHORT_SHA>"
```

Where `<COMMENT_ID>` is the review-comment ID from the finding's triage. For findings from Step 3 (initial triage), the comment ID comes from Step 2's inline-comment fetch. For findings from Step 6b (incremental review triage), the comment ID comes from the incremental review's comment fetch (filtered to the new review ID). Each round uses its own comment IDs — the skill does not attempt to match incremental-review findings back to original-round comment IDs.

**Guard for body-level findings:** If a fix-categorized finding has no associated comment ID (e.g., a review-body-level nitpick that was categorized as fix), skip the reply for that finding. Note the skip in the Step 6e report: `Reply skipped: finding has no inline comment ID (review-body-level)`.

**Error handling:** If a reply call fails (404 = comment deleted, 403 = permission issue, 422 = thread locked, 429 = rate limited), log the failure and continue. Do not abort the loop. On 429 with a `Retry-After` header, wait the indicated duration and retry once. Failed reply count is reported in Step 6e.

**If no findings were fix-categorized** (all non-fix, no push), no replies are posted.

### Step 6d Phase 1: Thread resolution polling (simplified)

The GraphQL polling query is unchanged. The evaluation is now purely observational (no automated fallback to gate).

After each poll, observe:
- How many CodeRabbit threads are resolved
- How many are still unresolved

The skill does not attempt to correlate unresolved thread counts against finding counts. It simply observes and reports.

**Short-circuit:** If no fix-categorized findings exist across ALL rounds of this run (not just the current round), skip Phase 1 entirely — no fix-threads to wait for. If prior rounds had fix-categorized findings, poll to observe their resolution status even if the current round had no fixes.

**Timeout:** If after the 2-minute polling window some threads are still unresolved, report the unresolved thread file paths and the manual resolve command:

```text
N CodeRabbit threads still unresolved after 2min:
  - <path1>
  - <path2>
To force-resolve all threads: gh pr comment <N> --body "@coderabbitai resolve"
```

Do not auto-fire the command.

### Step 6d Phase 2: Verdict polling (entry condition changed)

The polling mechanics (every 20s, up to 3min, checking latest CodeRabbit review `.state`) are unchanged. The entry condition changes:

**Enter Phase 2 only if ALL CodeRabbit threads are resolved.** This means:
- If all threads resolved (all findings were fix-categorized and all fix-threads resolved) → enter Phase 2
- If any threads unresolved (non-fix threads open, or fix-threads stuck) → **skip Phase 2**; report that `CHANGES_REQUESTED` is expected while threads remain open
- If `request_changes_workflow` is not enabled (per Step 1b) → skip Phase 2 as before

### Step 6e: Report (enhanced)

```text
Review round complete for PR #<N>:
- Fixed: X findings in commit <short-sha> (list them)
  [If multi-round: "Round 1: A findings in <sha1>; Round 2: B findings in <sha2>"]
- Skipped: Y findings (list with reasons) — threads left open
- Already fixed: Z findings (list them) — threads left open
- Duplicates: W
- Incremental review rounds: M
- Reply failures: F (list comment IDs and error codes, if any)
- Reply skipped: G (body-level findings with no inline comment ID, if any)
- Thread status: X resolved via reply / Y left open (non-fix)
  [If fix-threads unresolved: "N fix-threads still unresolved — to force-resolve: gh pr comment <N> --body '@coderabbitai resolve'"]
- CodeRabbit verdict: APPROVED / CHANGES_REQUESTED (expected — N threads open) / not polled (request_changes_workflow disabled)
```

### Edge cases: Updates

Update the existing edge cases section. Replace the bullets for "All findings are skips/duplicates" and "Stale CHANGES_REQUESTED with no findings" with their new-behavior entries below. Add all other rows as new entries. Preserve existing edge cases not covered by this table (No new comments, CodeRabbit review pending, CI failing, Branch protection, Incremental review loop, CodeRabbit timeout/down).

| Edge case | Current behavior | New behavior |
|-----------|------------------|--------------|
| All findings are non-fix (skip/duplicate/already-fixed) | Post `@coderabbitai resolve`, poll for APPROVED | No push, no replies, no resolution — report only, threads stay open |
| Stale CHANGES_REQUESTED with no new findings | Post `@coderabbitai resolve`, clear stale threads | No new findings → no triage → report "no findings but N prior-round threads still open" with manual resolve command |
| Fix-threads don't auto-resolve on hash reply | N/A (not attempted) | Report unresolved threads + manual resolve command. No automated fallback |
| Reply API call fails (404/403/422) | N/A | Log failure, continue loop, report count in 6e |
| Reply API rate-limited (429) | N/A | Wait `Retry-After` duration, retry once. If still 429, log and continue |
| Mixed fix+non-fix findings, all fix-threads resolve | N/A | Skip Phase 2 (non-fix threads open → no APPROVED expected), report non-fix threads |
| All fix, no non-fix, threads resolve | Current bulk resolve + APPROVED | Per-thread replies, poll, Phase 2 → APPROVED |
| Multi-round fix-push-review | Bulk resolve at end covers all rounds | Per-thread replies posted after each push with correct per-round SHA |
| Comment deleted between triage and reply | N/A | 404 from reply API — logged, counted, non-fatal |
| Body-level nitpick categorized as fix | N/A | Reply skipped (no comment ID), noted in report |
| Incremental review creates new thread on same location | N/A | Round-N replies use round-N comment IDs from the incremental review fetch. If the new thread is on the same file:line as a prior round's "Resolved" reply, both coexist — cosmetically confusing but functionally correct |
| Rate limit on reply API (pathological 30+ findings) | N/A | 429 retry handles transient limits; if persistent, cap at available budget and report |

## Test plan

### Static verification

1. **Grep check — `@coderabbitai resolve` removed from automated flow.**
   ```bash
   grep -n "@coderabbitai resolve" skills/review-pr/SKILL.md
   ```
   Expected: matches only in explanatory prose (Step 6 header context, edge cases table "Current behavior" column) and in the manual-command suggestion within the report template. Zero matches in any automated step.

2. **Grep check — per-thread reply present.**
   ```bash
   grep -n "comments.*replies" skills/review-pr/SKILL.md
   ```
   Expected: at least one match showing the `gh api -X POST .../comments/<COMMENT_ID>/replies` pattern.

3. **Grep check — SHA capture present.**
   ```bash
   grep -n "rev-parse --short HEAD" skills/review-pr/SKILL.md
   ```
   Expected: at least one match in the post-push flow (Step 5 and/or Step 6b context).

4. **Sync check.**
   ```bash
   python sync.py status
   ```
   Expected: clean diff between repo and `~/.claude/` after `sync.py install`.

5. **CLAUDE.md updated.**
   ```bash
   grep -n "per-thread" CLAUDE.md
   ```
   Expected: at least one match in the /review-pr description.

### Empirical validation (during implementation, before merge)

6. **Hash-reply auto-resolution test.** Run `/review-pr` against a real PR in a repo with `request_changes_workflow: true` and at least 2 CodeRabbit findings. Verify:
   - Per-thread replies appear under each fix-categorized finding
   - Observe whether threads flip to `isResolved: true` after hash reply (pin the empirical answer)
   - Report includes the resolving commit SHA
   - If threads don't auto-resolve, verify the report shows unresolved paths + manual command

7. **Multi-round SHA mapping test.** Run `/review-pr` on a PR where the initial review has findings fixed in round 1, and the incremental review introduces at least one new finding fixed in round 2. Verify:
   - Round-1 findings get replies with SHA-A
   - Round-2 findings get replies with SHA-B
   - Report lists both rounds with their respective SHAs

8. **"All non-fix" path.** Run `/review-pr` on a PR where all findings are skipped. Verify:
   - No push occurs
   - No per-thread replies posted
   - Threads remain open
   - Report correctly shows all findings as skipped with "threads left open"

9. **No regression.** Verify:
   - `request_changes_workflow` warning still appears when config is absent
   - Infrastructure-error re-trigger branch (Step 2) unchanged
   - 3-round fix-push-review cap (Step 6b) unchanged

## Test command

```bash
python sync.py status && grep -c "@coderabbitai resolve" skills/review-pr/SKILL.md && grep -c "comments.*replies" skills/review-pr/SKILL.md
```

This repo has no executable test suite. The combined command verifies: (1) SKILL.md syncs cleanly, (2) `@coderabbitai resolve` occurrence count (expected: small, prose-only), (3) per-thread reply pattern is present. Empirical validation (real PR run) is described in the test plan above.

## Done when

1. `@coderabbitai resolve` appears in `skills/review-pr/SKILL.md` only in explanatory prose and the manual-command suggestion in the report template — never in any automated step.
2. Per-thread replies are posted immediately after each push (Step 5 and Step 6b) using `gh api -X POST .../comments/<COMMENT_ID>/replies -f body="Resolved in <short-sha>"`, with the correct per-round SHA.
3. Step 5 captures `HEAD_SHORT_SHA` via `git rev-parse --short HEAD` after push.
4. Step 6d Phase 1 polling is purely observational — reports unresolved threads with manual resolve command, no automated fallback.
5. Step 6d Phase 2 entry condition gates on ALL threads resolved (skips Phase 2 when non-fix threads are open).
6. Step 6e report includes: per-round resolving commit SHAs on "Fixed" lines, non-fix findings with "threads left open", reply failures/skips, manual resolve command if threads unresolved, and CodeRabbit verdict status.
7. "All non-fix" branch short-circuits to report without posting per-thread replies.
8. Edge cases section updated with all new behaviors (stale CHANGES_REQUESTED, reply failures, body-level findings, multi-round SHAs, rate limiting).
9. Step 6 header prose reframed around per-thread replies.
9b. Step 6a/6b forward references updated: "skip to 6c" → "skip to 6d", "proceed to 6c" → "proceed to 6d", cap warning updated. 6b reply-injection point explicit.
10. `CLAUDE.md` /review-pr description updated to reflect per-thread replies.
11. `python sync.py status` shows clean diff after install.
12. Empirical validation pinned: hash-reply auto-resolution behavior documented in `docs/specs/TODO/VHS-3.test-output.txt` (yes/no + observed timing).
13. No regression on `request_changes_workflow` warning, infrastructure-error re-trigger, or 3-round cap.

## Out of scope

1. Tuning `.coderabbit.yaml` (review mode, profile, path filters) — config is the user's knob, not the skill's.
2. Changing the severity triage table in Step 3.
3. Splitting one bundled commit per round into multiple per-finding commits.
4. Adding a new MCP tool or wrapping `gh api` behind a helper.
5. Modifying `request_changes_workflow` Phase 2 polling timing.
6. Backfilling per-thread replies on PRs already resolved by the old bulk command.
7. Changing the reviewer-comment fetch in Step 2 (already returns comment IDs).
8. Using `resolveReviewThread` GraphQL mutation as a surgical middle fallback — noted as a potential next step if empirical validation shows hash replies don't auto-resolve threads, but not in v1.
9. `@coderabbitai autofix` integration.
