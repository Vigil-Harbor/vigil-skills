# VHS-5 — Fix review-pr skill bugs found during VHS-3 review run

## Goal

Fix three bugs in `skills/review-pr/SKILL.md` surfaced by exercising `/review-pr` against the VHS-3 PR: a P0 GraphQL author-login filter that silently returns zero CodeRabbit threads, a P1 invalid `gh pr diff --stat` invocation that errors on every run, and a P2 documented-but-unenforced polling cadence at all three Phase 6 polling locations (6a, 6d-Phase 1, 6d-Phase 2). All edits are localized to a single file; no restructuring, no new behavior. After merge + `python sync.py push`, the next `/review-pr` run produces a credible Phase 6 verdict instead of a wrong-but-plausible "all threads resolved" answer.

This is a v2 spec. v1 was authored against pre-VHS-4 main and reviewed twice; both reviews are preserved under `docs/specs/TODO/VHS-5.reviews/v1/`. The `/ship-spec` run against v1 halted at Phase 2 because VHS-4 had independently restructured Phase 6a of the SKILL.md (introducing a `FAST_PATH` predicate and `FIRST_POLL_TIME` wall-clock tracking), making v1's full "Location A" cadence rewrite stale. v2 originally dropped Location A entirely; it was tightened on 2026-05-13 (pre-`/ship-spec`, post-drift-check) to re-add a single inline parenthetical at SKILL.md:185 — substantially lighter than v1's full-paragraph rewrite, but enough to satisfy the brief's literal "6a cadence text" requirement. See Decision 3 for the rationale on why a parenthetical is the right shape (vs. a full rewrite).

## Scope

**Edit:**
- `skills/review-pr/SKILL.md` — four localized edits: P0 jq filter (line 284), P1 `gh pr diff` invocation (line 40), P2 cadence-honesty parenthetical at Phase 6a (line 185, ~30-word inline addition), P2 cadence rewrites at the two Phase 6d locations (lines 295/297 and 322).

**Do not touch:**
- Any other file in the repo (no test infra exists; brief explicitly out-of-scopes spec-cycle / ship-spec / reviewer agents / sync.py / states.json).
- Phase 6a's logic, structure, or signal-source (lines 156–214). VHS-4 already restructured this phase with a `FAST_PATH` predicate and `FIRST_POLL_TIME` total-polling bound; this spec adds only an inline cadence-honesty parenthetical at line 185. No new sub-phases, no logic moves, no signal changes — see Decision 3.
- The structure of Phase 6 elsewhere (no new sub-phases, no logic moves, no new error branches in 6d).
- `~/.claude/skills/review-pr/` — that's mirrored post-merge via `python sync.py push`, a workflow step the spec author does not own.

## Decisions

### Decision 1 — P0 GraphQL filter: use `"coderabbitai"` only, drop the suffix check

The current jq filter at SKILL.md line 284 (post-VHS-4 line numbers) is:

```
select(.comments.nodes[0].author.login == "coderabbitai[bot]")
```

This filter is applied **to GraphQL response data**, where `author.login` is `coderabbitai` (no `[bot]` suffix). GitHub's REST API uses the suffixed form; GraphQL does not. The filter matches nothing under GraphQL, so the merged threads array is always empty and the skill concludes "all CodeRabbit threads resolved" regardless of actual state.

**Fix:** change the literal to `"coderabbitai"`. Do **not** accept both forms via an `or` clause. Adding `or "coderabbitai[bot]"` would add a clause that can never match the GraphQL surface this jq runs against, and the spurious second clause would mislead future readers into thinking the suffix is a real-world possibility at this call site. Single source of truth; match what GraphQL actually returns.

The brief permits either approach; picking the simpler one keeps the contract obvious.

### Decision 2 — P1 `gh pr diff` replacement: `--name-only`

Line 40 calls `gh pr diff <N> --stat`. `--stat` is not a valid flag — the call errors on every run. The intent is "show file/line scope to contextualize triage."

**Fix:** replace with `gh pr diff <N> --name-only`. Rationale:

- Zero external dependencies (`diffstat` is not ubiquitous on Windows, where this skill runs).
- Lower output volume — triage only needs *which* files changed, not exact `+/-` counts per file. The unified diff is already available downstream if line-level context is needed.
- Matches the "scope-awareness" intent of the comment ("contextualize findings and triage outside-diff comments") — the file list is sufficient for that.

### Decision 3 — P2 polling cadence: full rewrite at Phase 6d, lighter parenthetical at Phase 6a

The brief identifies three polling locations (Phase 6a, Phase 6d-Phase 1, Phase 6d-Phase 2) that all claimed wall-clock cadences ("every 30/15/20 seconds, up to 5/2/3 minutes"). VHS-4 (merged after the brief was authored) independently restructured Phase 6a:

- Phase 6a now has a `FAST_PATH` predicate that skips the polling loop entirely on trivial PRs (≤2 fix-only findings).
- When not in fast-path, Phase 6a tracks `FIRST_POLL_TIME` as LLM conversational state, which bounds total polling (5 minutes, extending to 10 minutes if the check is still pending).
- VHS-4's substantive contribution was switching the completion *signal* (CI check status vs reviews-API polling). The cadence text on line 185 ("every 15 seconds") was not relabeled by VHS-4 and remains misleading on its own terms — both the inter-poll claim and FIRST_POLL_TIME's total-duration claim share the same harness limitation (the LLM tracks wall-clock as conversational state; back-to-back Bash calls advance it only by network round-trip latency).

**Fix:** apply cadence-honesty wording to all three locations, with shape calibrated to each:

- **Phase 6a (line 185)** — add a single inline parenthetical immediately after "every 15 seconds" acknowledging that intervals are aspirational and pointing the reader to FIRST_POLL_TIME as the bounding mechanism. The surrounding text already documents FIRST_POLL_TIME, so the parenthetical only needs to (a) acknowledge the aspirational cadence and (b) cross-reference the actual bound. No restructuring; no logic change.
- **Phase 6d-Phase 1 (line 295)** and **Phase 6d-Phase 2 (line 322)** — full rewrite to "up to N polling attempts; the attempt count governs total polling, not wall-clock duration. Intervals are aspirational because the agent harness fires Bash tool calls back-to-back." Phase 6d has no FIRST_POLL_TIME analogue, so attempt count is the governing limit and warrants a fuller explanation.

Do **not** add `sleep N &&` prefixes anywhere. Rationale for "doc, not enforce": zero behavior change (a sleep would slow every `/review-pr` run by minutes per polling phase even when unnecessary), cheaper to maintain, honest about what the harness actually does.

Why the asymmetric treatment (parenthetical at 6a vs. full rewrite at 6d) is the right shape:

- Phase 6a already carries the structural machinery a reader needs (FIRST_POLL_TIME, CI check signal). The parenthetical leans on that surrounding context — adding a full "up to N attempts" rewrite would either (i) duplicate FIRST_POLL_TIME's role, or (ii) replace it, both of which would conflict with VHS-4.
- Phase 6d has no equivalent machinery. The fuller "attempt count governs total polling" framing is load-bearing — without it, the rewrite would just delete the misleading cadence claim without telling the reader what the actual bound is.

Attempt counts derived from the 6d wording (8 attempts for 6d-Phase 1; 9 attempts for 6d-Phase 2) are preserved verbatim. Only the cadence claim is reframed.

### Decision 4 — No broader skill restructuring

The brief explicitly fences against Phase 6 redesigns. Each edit above fits inside an existing paragraph or code fence — the P0 jq literal change, the P1 flag swap, the Phase 6a inline parenthetical, and the two Phase 6d sentence rewrites. No new phases, no new sections, no new error-handling cases. If a reader diffs the spec change, the entire scope is four contiguous edit ranges (counting the two adjacent edits at Location B / lines 295 and 297 as a single range; five if counted separately).

### Decision 5 — Acknowledge VHS-4's partial overlap explicitly

The brief, authored before VHS-4 merged, called out three Phase 6 cadence sites. After VHS-4 restructured Phase 6a, all three remain in scope but with different shapes: the two Phase 6d locations get full rewrites (no FIRST_POLL_TIME analogue exists there); Phase 6a gets a lighter parenthetical that leans on VHS-4's FIRST_POLL_TIME machinery rather than duplicating it. The spec records this explicitly in Decision 3 so a future reader understands why the three edits are not symmetric. This is not a brief deviation — the brief permits the spec author to verify the underlying code and adjust shape when reality has shifted.

## Design

### P0 edit (SKILL.md line 284)

Current:

```
}' --jq '.data.repository.pullRequest.reviewThreads | {hasNextPage: .pageInfo.hasNextPage, endCursor: .pageInfo.endCursor, threads: [.nodes[] | select(.comments.nodes[0].author.login == "coderabbitai[bot]")]}'
```

New:

```
}' --jq '.data.repository.pullRequest.reviewThreads | {hasNextPage: .pageInfo.hasNextPage, endCursor: .pageInfo.endCursor, threads: [.nodes[] | select(.comments.nodes[0].author.login == "coderabbitai")]}'
```

Single-character delta: drop `[bot]` from the jq string literal. Add a one-line clarifying note immediately above the code fence describing why the GraphQL form differs from REST elsewhere in the skill, so the next reader does not "fix" it back. Comment text:

> Note: GitHub's GraphQL API returns `coderabbitai` for the bot login (no `[bot]` suffix). The REST API used elsewhere in this skill returns `coderabbitai[bot]`. The jq filter below runs against GraphQL data, so it uses the unsuffixed form.

### P1 edit (SKILL.md line 40)

Current:

```bash
# Get the PR's diff scope — helps contextualize findings and triage outside-diff comments
gh pr diff <N> --stat
```

New:

```bash
# Get the PR's diff scope (file list) — helps contextualize findings and triage outside-diff comments
gh pr diff <N> --name-only
```

Comment updated to "(file list)" so a future reader is not surprised the output lacks `+/-` counts.

### P2 edits (three locations — Phase 6a parenthetical + two Phase 6d rewrites)

**Location A — Phase 6a (line 185).** Current:

> Poll by making **individual Bash tool calls** every 15 seconds. Note the wall-clock time at first poll as `FIRST_POLL_TIME` — this is conversational state tracked by the LLM across tool calls, not a persistent shell variable (individual Bash calls do not share state). Reset `FIRST_POLL_TIME` at the start of each re-entry to 6a from 6b (timeouts are per-round, not cumulative). Outcomes:

New:

> Poll by making **individual Bash tool calls** every 15 seconds (intervals are aspirational because the agent harness fires Bash tool calls back-to-back; `FIRST_POLL_TIME` is what bounds total polling, not the per-poll wait). Note the wall-clock time at first poll as `FIRST_POLL_TIME` — this is conversational state tracked by the LLM across tool calls, not a persistent shell variable (individual Bash calls do not share state). Reset `FIRST_POLL_TIME` at the start of each re-entry to 6a from 6b (timeouts are per-round, not cumulative). Outcomes:

The parenthetical (~30 words) is the only new content; the rest of the paragraph is verbatim from the existing line. No code change, no logic change, no signal-source change.

**Location B — Phase 6d Phase 1 (line 295).** Current:

> Poll by making **individual Bash tool calls** (not a sleep loop — sleep loops are blocked in this environment). Check every 15 seconds, up to 2 minutes. After each poll, observe how many CodeRabbit threads are resolved and how many are still unresolved. The skill does not attempt to correlate unresolved thread counts against finding counts — it simply observes and reports.

New:

> Poll by making **individual Bash tool calls** (not a sleep loop — sleep loops are blocked in this environment). Make up to 8 polling attempts; the attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back. After each poll, observe how many CodeRabbit threads are resolved and how many are still unresolved. The skill does not attempt to correlate unresolved thread counts against finding counts — it simply observes and reports.

The "after the 2-minute polling window" sentence in the same section (line 297) also needs aligning. Current:

> If after the 2-minute polling window some threads are still unresolved, report the unresolved thread file paths and the manual resolve command:

New:

> If after exhausting the polling attempts some threads are still unresolved, report the unresolved thread file paths and the manual resolve command:

**Location C — Phase 6d Phase 2 (line 322).** Current:

> Poll by making **individual Bash tool calls** every 20 seconds, up to 3 minutes. CodeRabbit's `request_changes_workflow` auto-approval fires after threads are resolved AND pre-merge checks pass.

New:

> Poll by making **individual Bash tool calls**; make up to 9 polling attempts. The attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back. CodeRabbit's `request_changes_workflow` auto-approval fires after threads are resolved AND pre-merge checks pass.

The `CHANGES_REQUESTED after timeout` outcome wording (line 326) is left untouched: "timeout" still describes the user-visible outcome (attempts exhausted) accurately enough at the outcomes-list level.

### Cross-edit consistency

The two Phase 6d rewrites use the identical phrase **"The attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back."** Repeating it verbatim is intentional: each polling section reads as a self-contained spec for that phase, so future readers don't have to remember a global qualifier from another section. Two copies × ~20 words is well below the threshold at which the `spec-reviewer-conventions` prompt flags "premature abstraction" ("three similar lines is better than a premature abstraction").

The Phase 6a parenthetical uses a deliberately *different* phrasing than the 6d rewrites — "intervals are aspirational" appears in all three (so a single grep anchor catches all of them in the Test command), but 6a's parenthetical also names `FIRST_POLL_TIME` because the surrounding paragraph defines it. The 6d locations have no FIRST_POLL_TIME analogue, so attempt count appears in their phrasing instead. The asymmetry is intentional and matches the asymmetry of the underlying mechanisms (see Decision 3).

## Test plan

This repo has no executable test suite (`CLAUDE.md`: "no build step, no test suite, no dependencies beyond Python 3.8+ stdlib"). Verification is structural (greps on the edited file) + manual (paste-and-run against a live PR post-merge).

**Structural (via Test command below):**
1. `grep -c '"coderabbitai")' skills/review-pr/SKILL.md` returns at least 1 — the new GraphQL filter is present (positive presence of the P0 fix; more resilient than an absolute count of the suffixed form, which could shift if an unrelated commit adds or removes a REST literal elsewhere in the skill).
2. `grep -c -- '--stat' skills/review-pr/SKILL.md` returns 0 — the invalid flag is gone (P1).
3. `grep -c -- '--name-only' skills/review-pr/SKILL.md` returns at least 1 — the replacement is present (P1).
4. `grep -c "intervals are aspirational" skills/review-pr/SKILL.md` returns at least 3 — the cadence-honesty wording landed in all three locations (Phase 6a parenthetical + both Phase 6d rewrites) (P2). `-ge "3"` (not `= "3"`) keeps the assertion resilient against future unrelated edits.
5. `grep -c "2-minute polling window" skills/review-pr/SKILL.md` returns 0 — the secondary rewrite in Location B (line 297 wording) also landed. Without this check, the implementer could miss the secondary edit and the structural gate would still pass.
6. `grep -c "bounds total polling, not the per-poll wait" skills/review-pr/SKILL.md` returns at least 1 — the Phase 6a parenthetical specifically names FIRST_POLL_TIME as the bounding mechanism, not just a generic "aspirational" claim. Without this check, an implementer could land "intervals are aspirational" at line 185 without the FIRST_POLL_TIME cross-reference and the broader `intervals are aspirational` count check would still pass at >=3 — but the parenthetical would be misleading (the reader would conclude there's no bound, when in fact FIRST_POLL_TIME is the bound). The grep pattern deliberately excludes `FIRST_POLL_TIME` itself because SKILL.md wraps that identifier in backticks (markdown inline code), and a single-quoted shell pattern containing a backtick would interact badly with bash command substitution. The "bounds total polling, not the per-poll wait" suffix is unique to the Location A parenthetical and locks in the substance of the edit, not just its presence.

**Note on `python sync.py status`:** intentionally omitted from the Test command. `sync.py status` prints drift information but does not exit non-zero, so chaining it with `&&` would be decorative — the chain proceeds regardless. The repo's working tree also carries pre-existing drift (peon-ping `dst-only` entries; `ship-spec/states.json` if locally re-installed) that is unrelated to this spec and would clutter the report at every Test command run. Mirror cleanliness is gated separately by Done-when #5 (a manual post-`python sync.py push` check, not a Test command clause).

**Manual (post-merge, against any live CodeRabbit PR):**
1. Paste the GraphQL `reviewThreads` query (Phase 6d) into `gh api graphql -f query='...'` against any PR that has CodeRabbit comments. Confirm `threads` is non-empty. Confirms P0 fix end-to-end.
2. Run `gh pr diff <N> --name-only` against any PR. Confirm exit 0 and a list of file paths. Confirms P1 fix.
3. Cosmetic: read Phase 6d in the installed SKILL.md and confirm the cadence wording reads naturally and no longer claims wall-clock seconds-based pacing. Confirms P2 fix.

No regression tests are added because no test infra exists. The structural greps are the closest available proxy.

## Test command

```bash
test "$(grep -c '"coderabbitai")' skills/review-pr/SKILL.md)" -ge "1" && test "$(grep -c -- '--stat' skills/review-pr/SKILL.md)" = "0" && test "$(grep -c -- '--name-only' skills/review-pr/SKILL.md)" -ge "1" && test "$(grep -c 'intervals are aspirational' skills/review-pr/SKILL.md)" -ge "3" && test "$(grep -c '2-minute polling window' skills/review-pr/SKILL.md)" = "0" && test "$(grep -c 'every 20 seconds, up to 3 minutes' skills/review-pr/SKILL.md)" = "0" && test "$(grep -c 'bounds total polling, not the per-poll wait' skills/review-pr/SKILL.md)" -ge "1"
```

This command verifies: (1) the new GraphQL filter `"coderabbitai")` is present (P0 landed); (2) no `--stat` remains in any gh command (P1 landed); (3) `--name-only` is present (P1 replacement landed); (4) the P2 cadence-honesty wording appears in at least all three locations (Phase 6a parenthetical + both Phase 6d rewrites); (5) the secondary "2-minute polling window" phrase in Location B has been replaced; (6) Location C's old "every 20 seconds, up to 3 minutes" phrase has been replaced (symmetric coverage with assertion 5 — both Phase 6d cadence rewrites have explicit absence checks against their pre-edit phrasing); (7) Phase 6a's parenthetical specifically cross-references FIRST_POLL_TIME, locking in substance not just presence (see § Test plan structural check #6). Empirical validation per the manual steps above.

Run via Bash tool (not PowerShell) — the brief's repo uses bash for all `gh`/`git` invocations per the SKILL.md shell note, and `grep -c` is the available count primitive on this machine via the Bash tool's git-bash. If an assertion fails, the `&&` chain returns the failing clause's exit code; re-run individual clauses to identify which check fired.

## Done when

1. Phase 6d GraphQL query returns the expected CodeRabbit threads when pasted into `gh api graphql` against a PR that has any (the merged threads array is non-empty). Maps to brief Done-when #1.
2. Step 1 `gh pr diff <N> --name-only` invocation runs without error and outputs a file list. Maps to brief Done-when #2.
3. All three Phase 6 polling locations have cadence-honesty wording: Phase 6d-Phase 1 and Phase 6d-Phase 2 carry full rewrites framing intervals as aspirational with attempt count as the governing limit; Phase 6a (line 185) carries an inline parenthetical acknowledging the cadence is aspirational and naming `FIRST_POLL_TIME` as the actual bound. Maps to brief Done-when #3 (literal coverage at all three locations).
4. The only file changed is `skills/review-pr/SKILL.md`. `git diff --name-only <merge-base>..HEAD` on the implementation branch lists exactly that path. (`/ship-spec` cuts an isolated worktree from main, so the merge-base ref at implementation time is main's tip.) Maps to brief Done-when #4.
5. After `python sync.py push` (run by the human or by `/ship-spec`'s post-merge step, not by the Test command), `python sync.py status` shows no remaining `differ` entry for `skills/review-pr/SKILL.md`. This is a post-push manual check, deliberately outside the structural Test command — see § Test plan note. Maps to brief Done-when #5.
6. The Test command above exits 0.

## Out of scope

- Any change to `/spec-cycle`, `/ship-spec`, or any reviewer subagent (per brief).
- Any change to `sync.py`, `states.json`, or files outside `skills/review-pr/` (per brief).
- Phase 6 restructuring, new triage logic, new error-handling branches (per brief Decision 4).
- Any edit to Phase 6a's logic, structure, or signal-source — VHS-4 already addressed those concerns. This spec's only Phase 6a edit is a single inline parenthetical at line 185 (Decision 3 / Location A); the surrounding paragraph and the FAST_PATH / FIRST_POLL_TIME / CI-check-signal machinery are preserved verbatim.
- Adding a test suite or test infrastructure — the repo's "no test suite" stance is intentional (per `CLAUDE.md`).
- Wiki updates beyond what `/wiki-after-merge` produces post-merge (per brief).
- Renaming or reformatting CodeRabbit-related identifiers elsewhere in the skill (REST jq filters still match `"coderabbitai[bot]"` — that is correct for REST and is explicitly preserved).

## References

- Plane: VHS-5 (`401bddd2-6d35-48e4-9c4e-e6d4fbec819d`)
- Brief: `docs/specs/TODO/VHS-5.brief.md`
- v1 reviews (preserved for audit): `docs/specs/TODO/VHS-5.reviews/v1/round-{1,2}/`
- Skill source: `skills/review-pr/SKILL.md` at main HEAD `19d2d98` (lines 40, 185, 284, 295, 297, 322)
- Related prior merges: PR #6 (VHS-4) — restructured Phase 6a with FAST_PATH and FIRST_POLL_TIME; PR #7 (VHS-6) — added upstream-staleness check to spec-cycle Phase 0 (which, if installed, would have flagged v1's stale anchors before review)
- Origin: bugs surfaced during VHS-3 `/review-pr` dry run
