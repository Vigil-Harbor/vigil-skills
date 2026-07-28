# VHS-6 — spec-cycle: upstream staleness check before spec work begins

**Status:** Backlog · **Priority:** Medium · **Assignee:** Devin
**Created:** 2026-05-09 · **Plane:** VHS-6
**Origin:** Direct cost observation from a CAL-54 dogfooding run on 2026-05-08. `/spec-cycle` ran 4 rounds × 3 reviewers (12 agent invocations) and `/ship-spec` set up a worktree before the first `git log` call inside the implementation worktree surfaced that `upstream/main` had already migrated `writeUsageCostCache` to `replaceFileAtomic` from `@openclaw/fs-safe` (commit `1997ac449d`). The check that would have caught this — "does upstream already touch these files for this reason?" — is one `git fetch` plus two `git log` calls, sub-second. Goal is to insert that check at the front of `/spec-cycle` so wasted spec/impl effort on already-fixed-upstream work fails fast.

## Problem

`skills/spec-cycle/SKILL.md` Phase 0 (`:19–32`) walks through five preflight steps — brief resolution, brief existence check, `CLAUDE.md` read for test/wiki config, Plane reachability ping, and `states.json` namespace lookup — then proceeds directly to Phase 1 (spec authorship). None of those steps look at the *upstream* git history of the repo being patched. For forks of an active upstream (the only relevant case in Vigil-Harbor today is CAL, a fork of Claude Code's agent SDK / CLI repo), the omission means:

- A reviewer agent grep against the local fork's `HEAD` confirms the broken code path is still present, agreeing with the brief's framing of the bug.
- All three reviewer lenses converge on a green spec because the fix described in the brief *is* a valid fix against `HEAD`.
- `/ship-spec` then implements it, runs tests, and only at PR time does the user notice the upstream divergence (or — worse — the PR merges and silently re-introduces a now-superseded approach).

The CAL-54 incident is the canonical case: 4 rounds × 3 reviewers + worktree spinup, all wasted, because nobody looked at `upstream/main`'s last 90 days of commits touching `src/infra/session-cost-usage.ts`. The check itself is mechanical — `git fetch upstream`, two `git log` queries with inferred search terms, an `HEAD..upstream/<default-branch>` rev-list count — and the false-positive cost is one user-confirmation prompt.

## Why it matters

- **Wasted-work asymmetry.** A false negative (the check misses a real upstream fix) is no worse than today: the user proceeds normally, eventually catches it at PR-review or merge time. A true positive saves 4 rounds × 3 reviewers (≈12 agent invocations) plus a worktree spin-up — empirically observed on CAL-54. The asymmetry favors adding the check even at moderate false-positive rates.
- **Fork hygiene is a structural concern.** CAL is the only repo in Vigil-Harbor that pulls from an active upstream today, but the workflow is designed to be portable (see `vigil-skills/docs/customizing.md`). Bolting the check into Phase 0 — gated cleanly behind "upstream remote exists" — costs zero on non-fork repos and accrues value as the workflow gets adopted on more forks.
- **Bounded blast radius.** Markdown-only edit to one file (`skills/spec-cycle/SKILL.md`) plus a sync.py push. No new tools, no new dependencies, no runtime state. Same blast-radius profile as VHS-3, VHS-4. A single-section revert undoes it cleanly if the check turns out to be more friction than help.
- **Fail-fast aligns with the wiki's skepticism rule.** The wiki (`vigil-harbor-wiki/CLAUDE.md` § "Skepticism rule") tells agents not to treat user-volunteered framing as truth. A brief framing the bug as "EPERM in writeUsageCostCache, fix with retry-loop" is exactly the kind of user framing that needs verification — and an upstream-history grep is a cheap, mechanical verifier that doesn't depend on human judgment.

## Scope (verified against current code, 2026-05-09 main)

| Section in `skills/spec-cycle/SKILL.md` | Current behavior | Replacement |
|---|---|---|
| Phase 0 preflight (`:19–32`) | Five steps: brief resolution, existence check, CLAUDE.md read, Plane ping, `states.json` namespace lookup. No git operations. | Insert a new step (placement TBD by spec author — see scope wrinkle below) that runs the upstream staleness check. Steps 1–3 stay structurally identical; the new step lands between the CLAUDE.md read and Phase 1 entry. Renumber downstream steps if inserted before existing step 4 / 5. |
| Phase 0 closing line (`:32`) | `Print a one-line preflight summary, then continue.` | Augment the preflight summary to include either `upstream: clean` / `upstream: skipped (no remote)` / `upstream: N stale commits — user proceeded` so the gating mechanism is observable in the run log. |
| `## Tool-use notes` (`:205–211`) | Lists Read/Edit/Write, Bash for `git log`, Agent calls, `memory_search`. | Already covers `Bash for git log`. Extend the line to call out `git fetch upstream` (ref-update side effect) and `git rev-list HEAD..upstream/<default-branch> --count` so the reviewer agents are not surprised by network/ref-update activity in Phase 0. |
| `## Failure modes to watch for` (`:213–219`) | Five bullets covering stale spec read, reviewer status drift, severity inflation, ticket-not-in-cache, wiki path mismatch. | Add two bullets: (a) **Upstream remote missing or unreachable** — skip silently, do not block Phase 1; (b) **Search-term extraction false negative** — note that the heuristic is best-effort and that a missed upstream commit means the user pays today's wasted-rounds cost, no worse. |

**Preserved (NOT changed):**

- Phases 1–3 (spec authorship, review loop, drift-check HARD STOP). The new check lives entirely inside Phase 0; no downstream phase changes are required.
- The Plane reachability ping (`:29`). Independent dependency; warn-and-proceed semantics unchanged.
- The `states.json` namespace lookup (`:30`). Independent dependency; serves Phase 1 + reviewer agents.
- `/ship-spec`'s own preflight. The ship-spec skill has its own Phase 0 (separate file); this brief deliberately scopes to spec-cycle only. Dual-staging the check in ship-spec is out of scope (see Out of scope §1).
- Reviewer agent prompts and STATUS-line parsing (Phase 2). Reviewer behavior is unchanged.

**Possible scope wrinkle to confirm before kickoff:**

- **Exact insert position.** The Plane ticket suggests labeling the new step `3b`, which reads as splitting current step 3 (CLAUDE.md read). The cleaner alternatives:
  - **(A) Insert as new step 4**, renumbering current steps 4 (Plane ping) → 5 and 5 (`states.json`) → 6. Pro: clean numbering. Con: every reference to "Phase 0 step 5" elsewhere needs an audit (currently none in-tree; verified via `grep -r "Phase 0 step" skills/ agents/`).
  - **(B) Insert as new step 6**, after `states.json`. Pro: zero renumbering. Con: cosmetically the staleness check has nothing to do with namespace resolution and shouldn't trail it.
  - **(C) Genuinely split step 3 into 3a (CLAUDE.md read) + 3b (staleness check)**, as the ticket literally suggests. Pro: matches ticket wording. Con: visually awkward; step 3 is one logical action and 3a/3b implies they're related.
  - Recommend **(A)** — the renumber audit is one grep and the result places the check in the natural ordering position (after we know the project but before we hit external systems).
- **Default-branch detection.** `git log upstream/<default-branch>` needs to resolve `<default-branch>`. Cheapest approach: `git symbolic-ref --short refs/remotes/upstream/HEAD` (returns `upstream/main` or `upstream/master`). If that errors, fall back to trying `main` then `master`. Spec author pins the exact command sequence; do not hardcode `main` blindly.
- **Brief-text vs. ticket-text as search-term source.** The ticket title and description live in two places: the brief on disk (already in scope as `<TICKET-ID>.brief.md`) and the Plane work-item record (fetched in Phase 1 via `memory_search`). Phase 0 runs *before* Phase 1's Plane fetch. The brief is the authoritative source of truth for Phase 0 search-term extraction. Spec author confirms the parser only reads the brief, not the cached Plane record (which may not be available pre-Phase-1).

## Decisions carried forward

1. **Upstream-only — no comparable cross-fork or upstream-of-upstream check.** The check uses the `upstream` remote as the canonical "what does the source repo think" signal. Other remotes (`origin`, named feature forks, etc.) are ignored. If a project later needs to check a different remote name, that's a config addition; v1 hardcodes `upstream`.
2. **Skip silently when no upstream remote exists.** `git remote get-url upstream` (or equivalent) is the gate. Empty / nonexistent / errored → log `upstream: skipped (no remote)` in the preflight summary and proceed. Vigil-Harbor's own repos will hit this branch; CAL is the lone fork today.
3. **Search-term extraction is heuristic and best-effort.** Priority order, per the ticket: explicit file paths in the brief description, then function/error names mentioned in the brief, then ticket-title words. Grep commit messages *and* paths so refactors that moved files are still caught (the CAL-54 case literally was a function migration to a different module). Spec author picks regex patterns; do not over-engineer.
4. **90-day window is the v1 default; tunable via environment variable.** `git log --since="90 days ago"` covers typical release cadence on most upstreams without flooding output with ancient history. Make the window overridable (e.g., `SPEC_CYCLE_UPSTREAM_WINDOW=180`) so projects with slower release cadence can widen it. Default stays 90.
5. **Halt on stdin prompt — do not auto-proceed.** When commits are found AND the fork is behind upstream, print the warning and prompt `Proceed anyway? [y/N]` on stdin. This is a new halt pattern in Phase 0 (current Phase 0 only halts on brief-missing). Acceptable because the halt is interactive and short — no idle-context bloat. Spec author confirms the prompt is wired through the same stdin path used for the existing brief-not-found halt.
6. **`git fetch upstream` is permitted — it's a local ref update, not a working-tree write.** The skill description (`/spec-cycle` is read-only re: spec authorship; only writes to `docs/specs/TODO/`) is preserved: `git fetch` updates `.git/refs/remotes/upstream/*` but does not touch the working tree or the user's branches. Document explicitly so reviewer agents and `/ship-spec` consumers don't flag it as a mutation.
7. **Search runs in parallel where possible.** The two `git log` calls (paths-based + grep-based) are independent. Run them in parallel via background-and-wait shell idiom or via two Bash tool calls in one round-trip. Sub-second total wall-clock target.

## Approach

1. **Phase 0 step insertion.** Add the new step at position 4 (per scope-wrinkle recommendation A), renumbering current steps 4 and 5 to 5 and 6. Step 4 body, expanded from the ticket's pseudo-code:
   ```
   4. Upstream staleness check.
      a. Detect upstream remote:
           git remote get-url upstream  (capture exit code)
         If exit ≠ 0: log "upstream: skipped (no remote)" and continue to step 5.
      b. Resolve default branch:
           git symbolic-ref --short refs/remotes/upstream/HEAD
         Fallback chain on error: try main, then master, then warn-and-skip.
      c. Refresh upstream refs:
           git fetch upstream 2>/dev/null
         Network failure here is non-fatal — proceed using whatever upstream/* refs are already local. Log it in the preflight summary.
      d. Extract search terms from <TICKET-ID>.brief.md:
           - explicit file paths (regex over `[A-Za-z0-9_./-]+\.(ts|js|py|md|...)`)
           - function names (heuristic: words in `code` spans / fenced blocks)
           - error strings (heuristic: ALL-CAPS_WITH_UNDERSCORES or quoted-error-string patterns)
           - fallback: ticket-title words
         Spec author pins extraction regex; recommend keeping it small.
      e. Run two parallel git log queries:
           git log upstream/<branch> --since="${SPEC_CYCLE_UPSTREAM_WINDOW:-90 days ago}" \
               --oneline -- <inferred-paths>
           git log upstream/<branch> --since="${SPEC_CYCLE_UPSTREAM_WINDOW:-90 days ago}" \
               --oneline --grep="<primary-search-term>"
         Union the results, dedupe by SHA.
      f. Behind-upstream check:
           git rev-list HEAD..upstream/<branch> --count
         If 0: fork is at-or-ahead of upstream; even relevant commits are unlikely to mean "already fixed." Log "upstream: clean (at HEAD)" and continue.
      g. If commits found AND behind-count > 0:
           ⚠️  UPSTREAM STALENESS: <N> recent upstream commits touch files relevant to this brief.
               Review before investing in a spec:
                 <SHA>  <subject>
                 ...
               Proceed anyway? [y/N]
         Halt for stdin. On 'y' / 'Y': log "upstream: N stale commits — user proceeded" and continue. On 'n' / 'N' / EOF: halt with exit message "Spec-cycle aborted: upstream staleness — re-evaluate brief or update fork."
      h. If no commits found: log "upstream: clean (no relevant commits)" and continue.
   ```
2. **Preflight summary line update.** Phase 0's closing line (`:32`) currently says `Print a one-line preflight summary, then continue.` Augment to include the upstream-check result token (`clean` / `skipped` / `N stale — user proceeded`).
3. **Tool-use notes update.** Existing line `Bash for git log (read-only) and mkdir for review subdirs` (`:208`) becomes `Bash for git fetch upstream (ref update only), git log / git remote / git rev-list / git symbolic-ref (read-only), and mkdir for review subdirs.`
4. **Failure modes additions.** Append two bullets to `## Failure modes to watch for` (`:213–219`):
   - `Upstream remote missing or unreachable. Skip silently — vigil-harbor's own repos will hit this branch by design. CAL is the lone fork today.`
   - `Search-term extraction false negative. The heuristic is best-effort. A missed upstream commit means the user pays the pre-VHS-6 wasted-rounds cost; no worse.`
5. **Validation harness.** Run `/spec-cycle` against three test briefs:
   - **Brief A — no upstream remote** (any vigil-harbor repo, e.g., the MCP server): confirm step 4 prints `upstream: skipped (no remote)` and Phase 1 starts within ≤1s of step 3 completion.
   - **Brief B — fork with upstream, irrelevant ticket** (CAL with a brief that mentions files untouched by recent upstream commits): confirm step 4 prints `upstream: clean (no relevant commits)` and proceeds.
   - **Brief C — fork with upstream, relevant upstream commits exist** (CAL with a synthetic brief mirroring CAL-54's framing): confirm step 4 surfaces the `replaceFileAtomic` migration commit, halts on stdin, and exits cleanly when the user types `n`.
   Pin the actual log output for each in the spec's Test plan.

## Acceptance criteria

- A new Phase 0 step exists in `skills/spec-cycle/SKILL.md` between the CLAUDE.md read and Phase 1 entry, implementing all eight sub-steps a–h above.
- `git remote get-url upstream` failure (no upstream remote) results in a single `upstream: skipped (no remote)` log line; Phase 1 starts within ≤1s of step 3 completion.
- On a fork with an upstream remote and zero relevant commits in the configured window, the preflight summary's upstream token is `clean (no relevant commits)` (or `clean (at HEAD)` if the fork is at/ahead of upstream); Phase 1 proceeds.
- On a fork with an upstream remote AND relevant commits AND the fork is behind upstream, the skill prints the warning block (commit list with hashes + subjects), halts on stdin, and respects the user's `[y/N]` answer:
  - `y`: continues to Phase 1, with `upstream: N stale — user proceeded` in the preflight summary.
  - `n` / `N` / EOF: exits with code ≠ 0 and the message `Spec-cycle aborted: upstream staleness — re-evaluate brief or update fork.`
- The `SPEC_CYCLE_UPSTREAM_WINDOW` env var, when set to a value `git log --since=` accepts (e.g., `180 days ago`), is honored. When unset, the default `90 days ago` is used.
- Phase 0 closing line includes the upstream token (`clean | skipped | N stale — user proceeded`) so the gating mechanism is observable in the run log.
- `## Tool-use notes` lists `git fetch upstream`, `git remote`, `git log`, `git rev-list`, `git symbolic-ref` explicitly so reviewer agents do not flag them as undocumented mutations.
- `## Failure modes to watch for` includes the two new bullets (no-upstream-remote, search-term-false-negative).
- `python sync.py status` after the edit shows the SKILL.md change cleanly diffed; `python sync.py push` followed by `git diff` shows byte-for-byte parity in `~/.claude/skills/spec-cycle/spec-cycle.md` (note: installed file is `.md`, repo file is `SKILL.md` — sync.py handles the rename).
- Validation harness Brief A / B / C all behave as described in Approach §5; spec's Test plan cites actual run log output (not synthetic).
- A re-run of `/spec-cycle` on the same brief produces the same upstream-check result (idempotency: `git fetch` is a no-op if refs are already up-to-date; user prompt re-fires only if the staleness window includes new commits).

## Out of scope

- Mirroring the same check into `/ship-spec` Phase 0. The pipeline is split (`/spec-cycle` → session boundary → `/ship-spec`); catching staleness at spec-cycle is the dominant savings. ship-spec dual-staging is a separate brief if it's wanted later.
- Custom remote names (e.g., `origin-upstream`, `nexus`, named feature-fork remotes). v1 hardcodes the literal `upstream` remote name.
- Cross-fork comparison (checking sibling forks, not the canonical upstream). Out of scope; the canonical upstream is the only authoritative "is this already fixed" source.
- Reading `.coderabbit.yaml`, `.github/CODEOWNERS`, or any non-git config to bias search terms. Pure git-history-grep heuristic in v1.
- Inferring whether an upstream commit is *the* fix for the ticket (semantic match). The check surfaces commits that *might* be related; the user does the semantic eval. Trying to LLM-classify the diff would be a much larger change with unclear win.
- Detecting upstream branches other than the default branch (release branches, hotfix branches). v1 only checks `upstream/<default-branch>`.
- Adding the staleness signal to reviewer agents' input context. Phase 0 is upstream of reviewer dispatch; the halt/prompt happens before any reviewer runs. If staleness is detected and user proceeds, reviewers don't need to know — Phase 0 already gated.
- Backfilling the check on briefs already in `docs/specs/TODO/` that were spec-cycled before this lands. Cosmetic; not worth the cycles.
- Caching upstream refs across `/spec-cycle` invocations. Each run does its own `git fetch upstream`; sub-second cost on a warm clone, no caching needed.

## Risks / decisions

1. **CAL-only signal value today.** The only repo in Vigil-Harbor with an active `upstream` remote is CAL. Every other vigil-harbor repo will hit the no-remote skip-silently branch. The check accrues value as the workflow gets adopted on more forks (`docs/customizing.md` users), but v1's value is concentrated in CAL workflows. Acceptable — the cost on non-fork repos is one `git remote get-url` call (sub-millisecond).
2. **`git fetch upstream` network cost on slow links.** A slow upstream-fetch could add 5–30s to every Phase 0 run on CAL. Mitigation: `2>/dev/null` already swallows transient failures; consider whether to add a 5s timeout via `git -c http.lowSpeedTime=5 fetch upstream`. Spec author decides whether to wire the timeout in v1 or accept the rare outlier.
3. **Default-branch detection edge cases.** A repo where `upstream/HEAD` is unset (older clones, manual remote setup) will fall through to the `main`-then-`master` fallback. If the upstream uses neither — e.g., `dev`, `trunk`, `develop` — the check skips that fork until the spec author manually fixes the symbolic ref or until v2 adds explicit config. Acceptable for v1; document in failure modes.
4. **Search-term extraction over-fires on broad briefs.** A brief that mentions a common word (`error`, `cache`, `state`) could match dozens of upstream commits in 90 days, producing a noisy warning. Mitigations: (a) prioritize file paths and function names over title words; (b) cap output at, say, 20 commits with `git log -n 20`; (c) the user can answer `y` to proceed — false-positive cost is low. Spec author picks the cap.
5. **Search-term extraction under-fires on indirect rewrites.** The CAL-54 fix renamed the function (`writeUsageCostCache` → `replaceFileAtomic`). Path-based search would catch it (the file `src/infra/session-cost-usage.ts` was edited); commit-message grep on `writeUsageCostCache` might miss it if the upstream commit subject says only `migrate to fs-safe`. The dual path-search + grep-search design is the mitigation; spec author confirms both fire on the CAL-54 reproduction.
6. **Stdin halt is a new pattern in Phase 0.** Current Phase 0 halts only on brief-not-found (a hard error, not interactive). The `[y/N]` prompt mid-Phase-0 is a UX departure. Confirm the skill runner's stdin path supports interactive prompts in non-TTY contexts (e.g., piped input, automated test harness). Recommend: if stdin is not a TTY, treat as `n` (abort) and tell the user to re-run interactively. Spec author pins the non-TTY behavior.
7. **User confirmation as a soft gate.** A rushed user can `y`-through every staleness warning, defeating the purpose. Mitigation: print the upstream commit list inline so the user has to *see* what they're proceeding past. The skill cannot enforce careful reading; that's user discipline. Acceptable.
8. **Interaction with `--no-prompt` or batch modes.** If `/spec-cycle` is invoked from a CI-style automation that wants no interactive prompts, the staleness halt will block it. v1 punts on a `--force-skip-staleness` flag — automations should set `SPEC_CYCLE_UPSTREAM_WINDOW=0d` or similar to make the window vacuous (verify `git log --since="0 days ago"` returns nothing recent enough to trigger). Spec author either wires an explicit flag or documents the env-var workaround.
9. **`git rev-list HEAD..upstream/<branch>` cost on diverged forks.** On a fork with thousands of commits behind upstream, the rev-list `--count` could be slow. v1 uses `--count` (which is fast — it doesn't enumerate); acceptable. If profiling later shows it as a hot spot, switch to `git merge-base --is-ancestor` (faster but only gives a boolean, not a count).
10. **`states.json` ordering question.** The current Phase 0 step 5 (`states.json` lookup) feeds Phase 1's namespace argument. Inserting the staleness check at position 4 means it runs *before* the namespace is resolved, but the staleness check doesn't need namespaces — it operates purely on git. Confirmed safe. If a future change makes the staleness check namespace-aware (e.g., per-project upstream config), revisit ordering.

## References

- Plane: VHS-6
- Skill: `skills/spec-cycle/SKILL.md` (current implementation, 219 lines)
- Trigger incident: CAL-54 (fix EPERM on usage-cost-cache atomic rename) — discovered upstream `1997ac449d` migrated `writeUsageCostCache` to `replaceFileAtomic` from `@openclaw/fs-safe`. The 90-day path-based `git log` against `src/infra/session-cost-usage.ts` would have surfaced this in preflight.
- Workflow context: `vigil-skills/CLAUDE.md` § "Workflow: spec-cycle → ship-spec"
- Related preflight precedent: `skills/spec-cycle/SKILL.md:29` (Plane reachability ping — warn-and-proceed on outage) and `skills/ship-spec/SKILL.md:39` (mirror preflight in ship-spec) — both establish the "cheap dependency check, log the result, do not block on failure" pattern that step 4 should follow.
- Skepticism rule: `vigil-harbor-wiki/CLAUDE.md` § "Skepticism rule (for any agent making claims)" — the staleness check mechanizes "do not treat user-volunteered framing as truth" for the upstream-divergence case.
- Sibling brief / spec (preserved-step-numbering pattern): `docs/specs/TODO/VHS-4.brief.md`, `docs/specs/TODO/VHS-4.spec.md`
- Customizing doc (consumers in non-CAL forks): `docs/customizing.md`
- Current call sites verified 2026-05-09 via `Read skills/spec-cycle/SKILL.md`
