# VHS-6 — spec-cycle: upstream staleness check before spec work begins

## Goal

Insert an upstream-staleness check into `/spec-cycle` Phase 0 that detects when a fork's upstream has already addressed the brief's concern — before wasting 12+ agent invocations on spec authoring and review. The check runs `git fetch upstream`, extracts search terms from the brief, greps recent upstream commits by path and message, and halts with a user prompt if relevant upstream activity is found on a fork that's behind upstream. On repos without an `upstream` remote, it skips silently at near-zero cost.

## Scope

| File | Change |
|------|--------|
| `skills/spec-cycle/SKILL.md` | Phase 0: insert new step 4 (upstream staleness check), renumber steps 4→5 and 5→6. Update closing line, Tool-use notes, Failure modes. |

**Preserved (NOT changed):**

- Phases 1–3 (spec authorship, review loop, drift-check HARD STOP). The new check lives entirely inside Phase 0.
- Phase 0 steps 1–3 (brief resolution, existence check, CLAUDE.md read). Structurally identical.
- Phase 0 steps 4–5 (Plane ping, `states.json` lookup) — renumbered to 5–6, content unchanged.
- `/ship-spec`'s own Phase 0 (separate file, separate skill). Not touched.
- Reviewer agent prompts and STATUS-line parsing (Phase 2). Unchanged.
- YAML frontmatter.

## Decisions

### D1: Insert position — new step 4, renumber 4→5 and 5→6

Insert the staleness check as Phase 0 step 4, between the CLAUDE.md read (step 3) and the Plane ping (now step 5). Renumber current steps 4 (Plane ping) → 5 and 5 (`states.json` lookup) → 6.

**Why:** Brief scope-wrinkle recommendation (A). Clean numbering, one-grep audit of downstream references (verified: `grep -r "Phase 0 step" skills/ agents/` returns zero hits outside the skill definition itself; step numbers only appear inside spec-cycle's SKILL.md and in the spec-cycle entry loaded into conversation context, which will be updated in the same edit). The staleness check is logically positioned after "we know the project" (step 3) but before "we check external systems" (Plane, states.json).

**How to apply:** Renumber in the Phase 0 body. Update all step-number references in the Tool-use notes and Failure modes sections. The spec-cycle skill preamble loaded into conversation context references "step 5" for namespace — update to "step 6".

### D2: Upstream-only — hardcode `upstream` remote name

The check uses the literal `upstream` remote. Other remotes (`origin`, named feature forks) are ignored. If a project needs a different remote name, that's a config addition for a future version.

**Why:** Brief Decision §1. CAL is the lone fork today; every other vigil-harbor repo hits the skip branch.

### D3: Skip silently when no upstream remote exists

`git remote get-url upstream` is the gate. Exit ≠ 0 → log `upstream: skipped (no remote)` in the preflight summary and proceed to step 5.

**Why:** Brief Decision §2. Non-fork repos (vigil-harbor's own repos) pay only one sub-millisecond `git remote` call.

### D4: Search-term extraction — heuristic, prioritized, best-effort

Extract search terms from the brief in priority order:
1. **Explicit file paths**: regex `[A-Za-z0-9_./+-]+\.[a-z]{1,4}` that looks like a source-file path — must contain `/` or end with a known code extension (`.ts`, `.js`, `.py`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`, `.sh`, `.go`, `.rs`).
2. **Code identifiers**: words inside backtick spans or fenced code blocks matching `[A-Za-z_][A-Za-z0-9_]{3,}` (camelCase, snake_case, PascalCase — ≥4 chars, avoids noise).
3. **Fallback — ticket-title words**: non-stopword tokens ≥4 characters from the brief's `# ...` heading. Used only if priorities 1 and 2 yield nothing.

For the path-based `git log`, use the top 5 paths (or all if ≤5). For the grep-based `git log`, use the top 3 identifiers joined with `|` in a single `--grep` pattern (with `--extended-regexp` for portable ERE alternation).

**Why:** Brief Decision §3. The priority order ensures file-path searches (most precise) fire first, with progressively broader fallbacks. The CAL-54 case would be caught by path search (`src/infra/session-cost-usage.ts`) even though the commit message used the new name.

**How to apply:** The extraction runs once in step 4d, before the git log queries in step 4e.

### D5: 90-day default window, tunable via `SPEC_CYCLE_UPSTREAM_WINDOW`

`git log --since=` uses `${SPEC_CYCLE_UPSTREAM_WINDOW:-90 days ago}`. The env var accepts any value `git log --since=` accepts (e.g., `180 days ago`, `2026-01-01`).

**Why:** Brief Decision §4. 90 days covers typical release cadence without flooding output.

### D6: Halt on staleness — conversational prompt, not tool call

When the check finds relevant upstream commits AND the fork is behind upstream, present the warning block with commit list and prompt the user conversationally (same pattern as ship-spec's Phase 3 test-gate halt — numbered options, wait for response). The "stdin" metaphor from the brief maps to the LLM's standard interactive pause, not a literal `read` or a specific tool invocation. On non-interactive invocations (if such a path exists), treat as abort.

**Why:** Brief Decisions §5 and §6 (Risk §6). The halt is a UX departure from current Phase 0 (which only halts on brief-not-found), but the cost of false-proceeding (wasted spec rounds) justifies it.

### D7: `git fetch upstream` is permitted — ref update, not working-tree write

`git fetch upstream` updates `.git/refs/remotes/upstream/*` but does not touch the working tree or user branches. This is consistent with the spec-cycle "no working-tree writes" contract. Document explicitly so reviewer agents don't flag it.

**Why:** Brief Decision §6.

### D8: Parallel git log queries, capped output

The two `git log` calls (paths-based and grep-based) are independent and run in parallel via two Bash tool calls in one message when both tiers produce search terms. When only one tier has results, only that query runs. Each is capped at `git log -n 20` to avoid noisy output on broad search terms. Grep uses `--extended-regexp` for portable ERE alternation (`|` instead of BRE `\|`).

**Why:** Brief Decision §7 and Risk §4. Sub-second total wall-clock target; cap prevents the warning block from being unusably long.

## Design

### Phase 0 step 4: Upstream staleness check

Insert after step 3 (CLAUDE.md read), before step 5 (Plane ping, formerly step 4). The step has seven sub-steps:

```markdown
4. Upstream staleness check.

   a. **Detect upstream remote:**
      ```bash
      git remote get-url upstream 2>/dev/null
      ```
      If exit ≠ 0: log `upstream: skipped (no remote)` and continue to step 5.

   b. **Resolve default branch:**
      ```bash
      git symbolic-ref refs/remotes/upstream/HEAD 2>/dev/null | sed 's|^refs/remotes/upstream/||'
      ```
      Returns the bare branch name (`main`, `master`, etc.) — the `sed` strip is required because the long-form output is `refs/remotes/upstream/main`. This matches ship-spec's Phase 0 step 5 pattern for `origin/HEAD`. If this errors or returns empty, try `main` then `master` as literal fallbacks (check existence with `git rev-parse --verify upstream/main` / `upstream/master`). Capture the result as `<default-branch>`. If none resolve, log `upstream: skipped (cannot resolve default branch)` and continue to step 5.

   c. **Refresh upstream refs:**
      ```bash
      timeout 30 git fetch upstream 2>/dev/null
      ```
      Network failure is non-fatal — proceed using whatever `upstream/*` refs are already local. The 30-second timeout bounds wall-clock cost on unresponsive remotes. Log `upstream: fetch failed (proceeding with available refs)` if exit ≠ 0; do not halt.

   d. **Extract search terms from `<TICKET-ID>.brief.md`:**
      Read the brief and extract:
      - **File paths** (priority 1): tokens matching `[A-Za-z0-9_./+-]+\.[a-z]{1,4}` that contain `/` or end with a known code extension (`.ts`, `.js`, `.py`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`, `.sh`, `.go`, `.rs`). Take the top 5.
      - **Code identifiers** (priority 2): words inside backtick spans or fenced code blocks that match `[A-Za-z_][A-Za-z0-9_]{3,}` (camelCase, snake_case, PascalCase — ≥4 chars, avoids noise). Take the top 3.
      - **Title words** (priority 3, fallback): non-stopword tokens ≥4 characters from the brief's `# ...` heading. Used only if priorities 1 and 2 yield nothing.

      If no search terms can be extracted at all, log `upstream: skipped (no search terms extracted)` and continue to step 5.

   e. **Run git log queries (parallel when both tiers have results):**
      ```bash
      # Paths-based (only if file paths were extracted in 4d):
      git log upstream/<default-branch> --since="${SPEC_CYCLE_UPSTREAM_WINDOW:-90 days ago}" \
          --oneline -n 20 -- <path1> <path2> ...

      # Grep-based (only if code identifiers or title words were extracted in 4d):
      git log upstream/<default-branch> --since="${SPEC_CYCLE_UPSTREAM_WINDOW:-90 days ago}" \
          --oneline -n 20 --extended-regexp --grep="<term1>|<term2>|<term3>"
      ```
      If both tiers produced search terms, run both via two Bash tool calls in a single message (parallel). If only one tier produced terms, run that query alone. Union the results, deduplicate by SHA prefix.

      If all queries return empty: log `upstream: clean (no relevant commits)` and continue to step 5.

   f. **Behind-upstream check:**
      ```bash
      git rev-list HEAD..upstream/<default-branch> --count
      ```
      If count is 0: the fork is at or ahead of upstream. Even if relevant commits exist, they're already incorporated. Log `upstream: clean (at HEAD)` and continue to step 5.

   g. **Halt on staleness:** If commits were found (step 4e) AND behind-count > 0 (step 4f), present the findings to the user and ask whether to proceed — standard conversational prompting, same pattern as ship-spec's Phase 3 test-gate halt:

      ```text
      UPSTREAM STALENESS: <N> recent upstream commits touch files/terms relevant to this brief.
      Review before investing in a spec:
        <SHA>  <subject>
        ...

      The fork is <M> commits behind upstream/<default-branch>.

      What would you like to do?
      1. Proceed anyway
      2. Abort — re-evaluate brief or update fork
      ```

      Wait for the user's response.

      - On `Proceed`: log `upstream: N stale commits — user proceeded` and continue to step 5.
      - On `Abort`: halt with message `Spec-cycle aborted: upstream staleness — re-evaluate brief or update fork.`
```

### Phase 0 closing line update

Current line 32: `Print a one-line preflight summary, then continue.`

Change to: `Print a one-line preflight summary — including the upstream check result token (clean / skipped / N stale — user proceeded) — then continue.`

### Step renumbering

All references to Phase 0 step numbers in the SKILL.md body:
- Current step 4 (Plane ping) → step 5. References: line 29 body text.
- Current step 5 (`states.json` lookup) → step 6. References: line 30 body text, line 38 ("namespace from step 5" → "namespace from step 6"), line 77 ("namespace from preflight step 5" → "namespace from preflight step 6").

### Tool-use notes update

Current line 208: `Bash for git log (read-only) and mkdir for review subdirs.`

Change to: `Bash for git fetch upstream (ref update only, bounded by timeout), git log / git remote / git rev-list / git symbolic-ref / sed (read-only), and mkdir for review subdirs.`

### Failure modes additions

Append two bullets after line 219:

- **Upstream remote missing or unreachable.** Skip silently — vigil-harbor's own repos will hit this branch by design. CAL is the lone fork today. Cost: one sub-millisecond `git remote get-url` call.
- **Search-term extraction false negative.** The heuristic is best-effort. A missed upstream commit means the user pays the pre-VHS-6 wasted-rounds cost; no worse than today.

## Test plan

### Static verification

1. **Step numbering correct.**
   ```bash
   grep -n "^[0-9]\." skills/spec-cycle/SKILL.md | head -20
   ```
   Expected: steps 1, 2, 3, 4, 5, 6 in Phase 0. Step 4 is the upstream staleness check; step 5 is the Plane ping; step 6 is `states.json`.

2. **Step 6 namespace references updated.**
   ```bash
   grep -n "step [0-9]" skills/spec-cycle/SKILL.md
   ```
   Expected: no references to "step 5" for namespace resolution — all updated to "step 6".

3. **Upstream-related git commands documented in Tool-use notes.**
   ```bash
   grep -n "git fetch\|git remote\|git rev-list\|git symbolic-ref" skills/spec-cycle/SKILL.md
   ```
   Expected: matches in step 4 body AND in Tool-use notes section.

4. **Failure modes has two new bullets.**
   ```bash
   grep -c "Upstream remote\|Search-term extraction false" skills/spec-cycle/SKILL.md
   ```
   Expected: 2.

5. **Sync check.**
   ```bash
   python sync.py status
   ```
   Expected: `skills/spec-cycle/SKILL.md` shows as differing.

### Empirical validation

6. **No-upstream repo (vigil-skills itself).** Run the modified skill's Phase 0 logic against this repo. Confirm `upstream: skipped (no remote)` appears in preflight summary and Phase 1 starts within ≤1s of step 3 completion.

7. **Fork with upstream, irrelevant ticket.** If a CAL checkout with `upstream` remote is available, run with a brief mentioning files/functions untouched in upstream's last 90 days. Confirm `upstream: clean (no relevant commits)`.

8. **Fork with upstream, relevant commits.** Run with a brief mirroring CAL-54 framing (mentions `src/infra/session-cost-usage.ts` or `writeUsageCostCache`). Confirm the staleness warning surfaces the `replaceFileAtomic` migration commit and the user is prompted.

## Test command

```bash
python sync.py status && grep -c "upstream" skills/spec-cycle/SKILL.md && grep -c "git fetch" skills/spec-cycle/SKILL.md && grep -c "SPEC_CYCLE_UPSTREAM_WINDOW" skills/spec-cycle/SKILL.md
```

This repo has no executable test suite. The combined command verifies: (1) SKILL.md syncs cleanly, (2) upstream check is present, (3) git fetch documented, (4) env var for window is wired. Empirical validation (real runs) is described above.

## Done when

1. Phase 0 has a new step 4 implementing sub-steps a–g (upstream remote detection, default-branch resolution, ref refresh, search-term extraction, parallel git log, behind-count check, user prompt on staleness) with clean/skip logging at each early-exit branch.
2. Current Phase 0 steps 4–5 are renumbered to 5–6; all internal references updated.
3. `git remote get-url upstream` failure results in `upstream: skipped (no remote)` log line; Phase 1 starts within ≤1s of step 3 completion.
4. On a fork with upstream and zero relevant commits, upstream token is `clean (no relevant commits)` or `clean (at HEAD)`.
5. On a fork with relevant commits AND behind-count > 0, the skill presents the warning (commit list + behind count) conversationally and waits for the user's response (`Proceed` → continues, `Abort` → halts).
6. `SPEC_CYCLE_UPSTREAM_WINDOW` env var is honored when set; defaults to `90 days ago`.
7. Phase 0 closing line includes the upstream token in the preflight summary.
8. Tool-use notes lists `git fetch upstream`, `git remote`, `git log`, `git rev-list`, `git symbolic-ref`.
9. Failure modes includes two new bullets (no-upstream-remote, search-term-false-negative).
10. `python sync.py status` shows the SKILL.md change cleanly diffed.
11. Search-term extraction prioritizes file paths > code identifiers > title words, with output capped at 20 commits per query.
12. Empirical validation (tests 6–8) produces verifiable log output: `upstream: skipped (no remote)` on vigil-skills, `upstream: clean` on irrelevant-ticket fork, staleness warning + user prompt on CAL-54-style fork.

## Out of scope

1. Mirroring the staleness check into `/ship-spec` Phase 0. Catching it at spec-cycle is the dominant savings; dual-staging is a separate brief.
2. Custom remote names (e.g., `origin-upstream`, `nexus`). v1 hardcodes `upstream`.
3. Cross-fork comparison (sibling forks, not the canonical upstream).
4. Reading `.coderabbit.yaml`, `.github/CODEOWNERS`, or non-git config to bias search terms.
5. Semantic inference of whether an upstream commit is *the* fix (LLM-classifying the diff). The check surfaces *possibly* related commits; the user does the semantic eval.
6. Detecting upstream branches other than the default branch (release, hotfix). v1 only checks `upstream/<default-branch>`.
7. Adding the staleness signal to reviewer agents' input context. Phase 0 gates before any reviewer runs.
8. Backfilling the check on briefs already in `docs/specs/TODO/` that were spec-cycled before this lands.
9. Caching upstream refs across invocations. Each run does its own `git fetch upstream`; sub-second on warm clone.

## Deferred (P2+)

- **Windows path separators in brief content.** The file-path regex uses `/` as separator. Briefs authored on Windows may contain `\`. Since `git log -- <path>` uses `/` internally, this is likely benign, but edge cases exist. (edge-cases R1/F-6)
- **Step 4f flow diagram.** Step 4f (behind-count) implicitly depends on 4e finding commits — the text says "If count is 0 ... continue to step 5" which is correct, but a reader might wonder when 4f runs vs. when 4e's early-exit fires. Current text is accurate; a flow diagram would be clearer but is not worth the complexity for a skill instruction. (edge-cases R1/F-8)
