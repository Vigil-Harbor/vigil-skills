# VHS-11 Spec — spec-cycle: 4 enhancements surfaced by the PET-86 run

**Ticket:** VHS-11 · **Brief:** `docs/specs/TODO/VHS-11.brief.md` · **Status:** v3 — green at round 2, post-green polish applied (see § Post-green polish)
**Spec class:** documentation-only (markdown edits to one skill file, three agent files, one doc; no code ships)

## Goal

Harden `/spec-cycle`'s convergence signal and smooth three friction points observed in the PET-86 end-to-end run. One markdown-only change adds: (1) an origin-sync check in Phase 0 so reviewers don't cold-read a stale local tree and burn findings on merged-but-unpulled code; (2) a sanctioned, bounded post-green polish step so reviewer-recommended P2 clarifications can be folded in without undocumented discretion; (3) tolerant brief-path resolution (alternate directories, descriptive-suffix filenames) with `docs/specs/TODO/` stated as canonical for spec artifacts; (4) an author-stated closure-manifest block in round-N>1 reviewer prompts so CLOSED/REOPENED verdicts verify the author's claims instead of inferring intent from a spec diff. Items 1 and 4 protect the trustworthiness of the review gate; items 2 and 3 are flow-text fixes.

## Scope

### Files to change

| File | Change |
|---|---|
| `skills/spec-cycle/SKILL.md` | Insert origin-sync check as Phase 0 step 5 (after step 4, `:96`); renumber current steps 5–6 → 6–7 and update the two step-number cross-references (`:107` "step 6" → "step 7", `:147` "step 6" → "step 7"); add origin token to the preflight summary line (`:101`); add post-green polish step 2g between the gate and Phase 3, with cross-references from 2d (`:172–174`) and 2e (`:181`); rewrite Phase 0 step 1 (`:23`) for brief-path tolerance + canonical-artifact statement; change 2b `brief_path` (`:144`) to the resolved path; add the round-N>1 closure-manifest block to the 2b prompt (`:142–152`); extend `## Tool-use notes` (`:277–283`) and `## Failure modes to watch for` (`:285–293`) |
| `agents/spec-reviewer-correctness.md` | Two edits: (1) optional `**Pre-ship recommended:**` line in the findings template (after `**Severity:**`, `:146`) + one defining sentence after the template's closing fence (`:160`); (2) one `closure_manifest` line in the orchestrator-inputs block (after `round_number`, `:16`) |
| `agents/spec-reviewer-edge-cases.md` | Same two edits (template `:141`, closing fence `:156`, inputs block `:16`) |
| `agents/spec-reviewer-conventions.md` | Same two edits (template `:135`, closing fence `:149`, inputs block `:18`) |
| `docs/customizing.md` | § "Spec & brief layout" (`:51–60`): note that the brief location/filename is tolerant on input (alternate directories, `<TICKET-ID>-slug.md` names) while spec artifacts stay canonical at `docs/specs/TODO/` (§ D3) |

### New files

None.

### Files to leave alone

- `skills/ship-spec/SKILL.md`, `skills/spec-reconcile/SKILL.md`, `skills/spec-retire/SKILL.md`, `skills/review-pr/SKILL.md` — untouched (brief Out-of-scope).
- `sync.py`, `skills/ship-spec/states.json` — untouched.
- The agents' step-7 closure-verification logic and closure-table format — untouched (item 4 feeds them better input only; the new `closure_manifest` input line documents what arrives, it does not change how step 7 verifies).
- `skills/spec-cycle/SKILL.md` Phase 3 brief-section parsing rules (`:264–273`) — already has a per-missing-header fallback; the brief's scope table carries no change here.
- The upstream staleness check (step 4, VHS-6), green-gate formula, round cap, round-4 FROZEN/REWRITE protocol — all preserved verbatim.

Edits land in the repo copies; `python sync.py install` propagates `skills/` and `agents/` to `~/.claude/` (`docs/customizing.md` is outside the synced subtrees). The repo is the source of truth (per CLAUDE.md).

## Decisions

### Decision 1 — Never auto-pull (brief §Decisions 1)

The origin check warns and *offers* a `--ff-only` update; the user confirms before any mutation. If histories have diverged (fast-forward impossible), the skill warns and proceeds — no merge, no rebase, no stash, ever, and no update is even offered. If a user-confirmed ff merge is aborted by git (e.g., uncommitted local changes would be overwritten), the skill prints git's error and proceeds on the stale tree — it never retries with a different strategy. When the comparison falls back to the default branch (current branch has no origin counterpart), no update is offered at all — the check is informational, because fast-forwarding a topic branch onto another branch's history is a surprising mutation no warning text fully inoculates. The design (D1 step 5e) encodes all four paths explicitly.

### Decision 2 — Origin check mirrors the VHS-6 pattern (brief §Decisions 2)

Same idiom as step 4: silent skip when the remote is absent, bounded-timeout fetch with non-fatal network failure, result token in the preflight summary. One deliberate ordering deviation: the fetch (5b) precedes branch resolution (5c), because a counterpart branch fetched for the first time must exist as a remote-tracking ref before `git rev-parse --verify origin/<branch>` can see it. Step 4's b/c ordering is unchanged (out of scope).

### Decision 3 — Post-green polish is bounded and gate-preserving (brief §Decisions 3)

Step 2g runs once, after the gate breaks green, before Phase 3. Three guardrails stated in the step text: only P2s a reviewer explicitly tagged pre-ship-recommended; clarifications only (no behavior reversals, no new scope); no re-review round — the green verdict stands and the polish step cannot reopen the loop. 2g also performs the green-round carry-forward of untouched P2s into `## Deferred (P2+)` (the round that goes green never runs 2e, so no earlier step has written them — see D2).

### Decision 4 — `docs/specs/TODO/` stays canonical for spec artifacts (brief §Decisions 4)

Step 1's rewrite tolerates alternate brief locations on input but never promotes them: the spec, reviews directory, and downstream ship-spec outputs always land in `docs/specs/TODO/`, and the step says so in one explicit sentence. Out-of-tree briefs are never moved or renamed by this skill; in-tree briefs remain subject to step 2's existing local-only-ticket rename flow (unchanged), which renames `<TICKET-ID>.*` artifacts under `docs/specs/TODO/` once a real Plane ID exists.

### Decision 5 — Closure manifest is author-stated intent, additive to agent self-service (brief §Decisions 5)

The 2b prompt block carries the author's one-line disposition for each round-(N−1) P0/P1 finding, and the agents' orchestrator-inputs blocks gain a matching `closure_manifest` line so the input is part of the documented contract (mirroring how `namespace` landed on both sides in VHS-1). The agents' step-7 disk-read closure verification is untouched; agents now verify the author's claim against the spec instead of inferring intent from a diff. P0/P1 only, one line each — bounded prompt growth (~10 lines observed on PET-86).

### Decision 6 — All four items ship as one markdown-only change (brief §Decisions 6)

Five files, all markdown, no new tools or runtime state. Each item is a section-level edit, so a per-item revert is a section-level revert. Same blast-radius class as VHS-6/VHS-7.

## Design

### D1 — Origin-sync check (SKILL.md Phase 0, new step 5)

Insert the following as step 5, immediately after step 4's closing line (`:96`). Current steps 5 (plane-proxy) and 6 (states.json) become 6 and 7. The "continue to step 5" lines inside step 4 (all six occurrences: 4a/4b/4d/4e/4f/4g — `SKILL.md:36, 42, 56, 70, 76, 95`) need **no text change** — the next step after 4 is still 5; only its content changed. Two cross-references must be updated: Phase 1's "`namespace` from step 6" (`:107`) → "step 7", and the 2b prompt's "resolved from preflight step 6" (`:147`) → "step 7".

New step text:

````markdown
5. Origin sync check. Sibling of step 4 — same skip-silently / warn-and-prompt
   idiom, applied to the local-branch-vs-origin axis. Reviewers cold-read the
   local tree, so a merged-but-unpulled change is a false-positive generator
   that pollutes the convergence signal. This step contains the skill's lone
   git-level mutation of existing tracked files, and it is strictly opt-in.
   Catch-all: any git command failure inside this step not handled by an
   explicit branch below → log `origin: skipped (git error)` and continue to
   step 6; never halt on this step's account.

   a. **Detect origin remote:**
      ```bash
      git remote get-url origin 2>/dev/null
      ```
      If exit ≠ 0: log `origin: skipped (no remote)` and continue to step 6.

   b. **Refresh origin refs:**
      ```bash
      timeout 30 git fetch origin 2>/dev/null
      ```
      Ref update only — never touches the working tree. Network failure is
      non-fatal: log `origin: fetch failed (proceeding with available refs)`
      if exit ≠ 0 and continue with whatever `origin/*` refs are already
      local. (Fetch runs before branch resolution — unlike step 4's b/c
      order — so a counterpart branch fetched for the first time is visible
      to the existence check in 5c.)

   c. **Resolve branches:**
      ```bash
      git symbolic-ref --short -q HEAD
      ```
      - Empty output (detached HEAD): log `origin: skipped (detached HEAD)`
        and continue to step 6.
      - Otherwise capture the output as `<branch>` (the current branch),
        then bind the comparison branch `<cmp>`:
        - If `git rev-parse --verify -q origin/<branch>` succeeds:
          `<cmp>` = `<branch>` — a **counterpart comparison**.
        - Otherwise fall back to the default branch: `git symbolic-ref
          refs/remotes/origin/HEAD 2>/dev/null | sed 's|^refs/remotes/origin/||'`;
          on error or empty output try `main` then `master` as literals
          (existence via `git rev-parse --verify origin/main` /
          `origin/master`) — the same fallback chain as step 4b. Set `<cmp>`
          to the first that resolves — a **fallback comparison**. If none
          resolve: log `origin: skipped (no comparison branch)` and continue
          to step 6.

   d. **Behind count:**
      ```bash
      git rev-list --count HEAD..origin/<cmp>
      ```
      If 0: log `origin: in-sync` and continue to step 6. (A local branch
      that is *ahead* of `origin/<cmp>` with no incoming commits also
      counts 0 — in-sync for staleness purposes.)

   e. **Warn; offer a fast-forward only for a counterpart comparison:**

      - **Fallback comparison (`<cmp>` ≠ `<branch>`) — informational only.**
        Warn: `local <branch> has no origin counterpart; the local tree is
        <N> commits behind origin/<cmp> — reviewers may cold-read stale
        files.` Log `origin: behind-N (informational — no counterpart)` and
        continue to step 6. No update is offered: fast-forwarding `<branch>`
        onto `origin/<cmp>`'s tip would move a topic branch onto another
        branch's history — a mutation outside this step's mandate.

      - **Counterpart comparison (`<cmp>` = `<branch>`):** check feasibility:
        ```bash
        git merge-base --is-ancestor HEAD origin/<branch>
        ```
        - **Exit 0 — HEAD is an ancestor; fast-forward is possible.** Prompt:

          ```text
          ORIGIN SYNC: local <branch> is <N> commits behind origin/<branch>.
          Reviewers cold-read the local tree; merged-but-unpulled changes
          generate false-positive findings.

          What would you like to do?
          1. Fast-forward update now (git merge --ff-only origin/<branch>)
          2. Proceed on the stale tree
          ```

          Wait for the user's response.
          - On update: run `git merge --ff-only origin/<branch>`. On
            success, log `origin: behind-N (updated)`, then re-validate the
            preflight reads the update may have staled: re-confirm the brief
            exists at the resolved path (step 2) and re-read CLAUDE.md
            (step 3); if `docs/specs/TODO/<TICKET-ID>.spec.md` arrived with
            the update, halt and ask before Phase 1 would overwrite it. If
            git aborts the merge (e.g., uncommitted local changes would be
            overwritten), print git's error verbatim, log `origin: behind-N
            (update failed — proceeded)`, and continue on the stale tree —
            never retry with merge, rebase, or stash.
          - On proceed: log `origin: behind-N (user proceeded)`.
        - **Exit 1 — histories have diverged; fast-forward is impossible.**
          Do not offer an update. Warn:
          `local <branch> and origin/<branch> have diverged (<N> behind);
          fast-forward impossible — proceeding on the local tree.`
          Log `origin: behind-N (diverged — proceeded)` and continue. No
          merge, no rebase, ever.
        - **Exit > 1 — git error** (bad ref, shallow-clone history boundary):
          handled by the step-level catch-all — log `origin: skipped (git
          error)` and continue to step 6.
````

**Preflight summary line** (`:101`) gains the origin token alongside the upstream token:

```markdown
Print a one-line preflight summary — including the upstream check result
token (clean / skipped / N stale — user proceeded) and the origin check
result token (in-sync / behind-N (updated) / behind-N (user proceeded) /
behind-N (update failed — proceeded) / behind-N (diverged — proceeded) /
behind-N (informational — no counterpart) / skipped (<reason>)) — then
continue.
```

Rationale for seven tokens where the brief's Done-when lists four (`in-sync | behind-N (updated) | behind-N (user proceeded) | skipped`): the brief's own Decision 1 mandates distinct no-update outcomes (user-declined, diverged, ff-aborted) that a four-token list cannot express without misreporting user intent in the audit line, and the fallback-comparison path (brief Risk §6, delegated to this spec) adds an informational outcome with no prompt at all. This is a token-vocabulary clarification, not a behavior change; Decision 1's never-auto-pull semantics are identical across all of them.

### D2 — Post-green polish step (SKILL.md, new § 2g)

Append after 2f, before Phase 3:

````markdown
### 2g. Post-green polish (bounded)

Runs exactly once, immediately after the gate breaks green (2d) and before
Phase 3. This is not a review round and cannot reopen the loop — the green
verdict stands regardless of what happens here. Note: the round that goes
green never runs 2e, so the final round's P2s exist only in the persisted
reports; this step performs their carry-forward bookkeeping. If a
`## Post-green polish` section already exists in the spec, treat 2g as
already-run: reconcile (merge/dedup) rather than append.

1. Collect candidates: P2 findings carrying the explicit
   `**Pre-ship recommended:** yes` marker (see the reviewer output
   contracts) from **all rounds'** persisted reports — not only the final
   round's. Skip any already addressed by an earlier revision; merge
   duplicates across lenses. Fallback for reports without the marker: a P2
   whose prose explicitly recommends folding the change in before
   /ship-spec.
2. If there are no candidates: print `post-green polish: none tagged`,
   record any remaining final-round P2s in `## Deferred (P2+)` (creating
   the section if absent), and proceed to Phase 3.
3. Apply each candidate only if it is a clarification — wording, file:line
   anchors, examples, error-message text, checklist rows. Hard limits: no
   behavior reversals, no new scope, no edits to the spec's Decisions,
   Out-of-scope, or Done-when sections (Done-when may gain parenthetical
   annotations only, never reworded criteria). A candidate that exceeds
   these limits is recorded
   in `## Deferred (P2+)` (creating the section or entry if absent) with a
   one-line reason.
4. Record each folded P2 in a `## Post-green polish` section at the end of
   the spec: one line each — finding ID and what changed. If the finding
   already has an entry in `## Deferred (P2+)`, remove that entry. Record
   every remaining untouched final-round P2 in `## Deferred (P2+)`.
5. No re-review round runs after polish.
````

Cross-references added:
- **2d** (`:172`): after "break the loop. Spec is green at round N." append "Run the post-green polish step (2g) before Phase 3."
- **2d advisory sentence** (`:174`): after "...do not prevent the spec from going green." append "On the green round, the carry into `## Deferred (P2+)` is performed by the post-green polish step (2g); P2s tagged `Pre-ship recommended` by a reviewer are 2g candidates."
- **2e P2 bullet** (`:181`): append "P2s carrying a reviewer's `Pre-ship recommended` tag become 2g candidates once the spec goes green."

### D3 — Brief-path resolution (SKILL.md Phase 0, step 1 rewrite)

Replace step 1 (`:23`) with:

````markdown
1. Resolve `<brief-path>` from the user's invocation and normalize it to a
   project_root-relative path with forward slashes (this normalized form is
   what later phases — including the 2b reviewer prompts — carry). The
   canonical shape is `docs/specs/TODO/<TICKET-ID>.brief.md`, but two
   alternates are tolerated on input:
   - **Alternate directories** — the brief may live anywhere in the repo
     (e.g., `docs/briefs/`).
   - **Descriptive-suffix filenames** — `<TICKET-ID>-some-slug.md`.

   If the resolved path is not under `project_root`, halt and ask the user
   to either move the brief into the repo or confirm proceeding; on
   confirm, carry the absolute path instead of the normalized relative
   form (reviewer access to out-of-root paths is host-dependent).

   Extract `ticket_id` with an anchored prefix match on the filename:
   `^[A-Z][A-Z0-9]*-[0-9]+` (e.g., `PROJ-86-fix-API-33-regression.md` →
   `PROJ-86`; anchoring disambiguates embedded ID-shaped tokens, and the
   `[A-Z0-9]*` tail admits digit-bearing project prefixes like `WEB3-12`).
   If the filename has no match, ask the user for the ticket ID before
   continuing.

   `project_root` is the cwd (the directory containing `CLAUDE.md`).

   **Canonical artifact location:** regardless of where the brief lives,
   every spec-cycle artifact — `<TICKET-ID>.spec.md`, the
   `<TICKET-ID>.reviews/` tree, and downstream ship-spec outputs — lands
   in `docs/specs/TODO/`. A brief outside that directory stays where it
   is: tolerated on input, never moved or promoted. If brief and spec end
   up in different trees, that is a documented consequence of the brief's
   location, not an accident.
````

Step 2's local-only-ticket-ID paragraph is unchanged; its rename flow targets `<TICKET-ID>.*` artifacts under `docs/specs/TODO/` and continues to make sense with an out-of-tree brief (an out-of-tree brief is not under `docs/specs/TODO/` and is therefore untouched by it).

**`docs/customizing.md` § "Spec & brief layout"** (`:51–60`): change the briefs bullet to read "Briefs at `docs/specs/TODO/<TICKET-ID>.brief.md` (loose: just enough to get started; canonical location — alternate directories and `<TICKET-ID>-slug.md` filenames are tolerated on input, and spec artifacts still land in `docs/specs/TODO/`)", leave the other three bullets untouched, and adjust the section's closing sentence (`:60`) to "Adjust the layout in your fork if needed; the skills hardcode the spec/reviews/test-output paths today (brief location is tolerant on input per the bullet above)."

### D4 — 2b prompt: resolved brief_path + closure-manifest block

Three edits:

1. SKILL.md 2b `brief_path` line (`:144`) becomes:
   ```
   - `brief_path: <the brief path resolved and normalized in Phase 0 step 1 — project_root-relative, forward slashes — not the canonical template>`
   ```

2. SKILL.md: after the per-agent prompt-content list (below the conventions-reviewer extras, `:152`), add:

````markdown
For rounds N > 1, each agent's prompt must additionally include a
closure-manifest block — the author's stated disposition of every
round-(N−1) P0/P1 finding, one line each:

```text
closure_manifest (round <N-1> → <N>):
  - <lens>/<finding-id> (P<sev>) "<title>" — <how addressed, with spec § anchor>
  - correctness/F-2 (P1) "stale anchor in § Design" — fixed: re-anchored to SKILL.md:142
```

P0/P1 findings only (P2 dispositions are visible in the spec's edits or
its `## Deferred (P2+)` section). A synthetic missing-STATUS P0 (per
`## Failure modes`) appears as
`<lens>/STATUS (P0) "missing STATUS line" — <disposition, e.g. report
regenerated in round N>` so the manifest always reconciles with the prior
round's gate arithmetic. This block complements — does not replace — the
reviewers' step-7 disk-read closure verification: the agents verify the
author's claims against the current spec instead of inferring intent from
a spec diff. Build it from the revision work you just did in 2e.
````

3. Each agent file: add one line to the orchestrator-inputs block ("The orchestrator passes these in your prompt:"), directly after the `round_number` line (`correctness.md:16`, `edge-cases.md:16`, `conventions.md:18`), identical wording in all three:
   ```markdown
   - `closure_manifest` — author-stated disposition of each round-(N−1) P0/P1 finding (present only when `round_number` ≥ 2); verify these claims against the spec in step 7
   ```
   This documents the input contract (mirroring how `namespace` landed on both sides in VHS-1) without changing step-7 logic or the closure-table format.

### D5 — `Pre-ship recommended` marker (three agent files)

In each agent's `# Output contract` findings template, insert one line directly after the `**Severity:**` line (identical in all three files; anchors: `agents/spec-reviewer-correctness.md:146`, `agents/spec-reviewer-edge-cases.md:141`, `agents/spec-reviewer-conventions.md:135`):

```markdown
**Pre-ship recommended:** yes
```

And one defining sentence placed **immediately after the template's closing code fence, before the "The last non-blank line MUST be exactly one of" paragraph** (i.e., after `correctness.md:160`, `edge-cases.md:156`, `conventions.md:149`):

```markdown
The `**Pre-ship recommended:**` line is optional and only meaningful on P2
findings: emit it (value `yes`) when you recommend the orchestrator fold
this clarification into the spec during spec-cycle's post-green polish
step (2g) before /ship-spec; omit the line otherwise.
```

The STATUS-line contract, severity definitions, closure-table format, and step-7 logic are untouched.

### D6 — Tool-use notes and failure modes (SKILL.md)

`## Tool-use notes` (`:280`) — extend the Bash bullet:

```markdown
- Bash for `git fetch upstream` / `git fetch origin` (ref updates only,
  bounded by timeout), `git log` / `git remote` / `git rev-list` /
  `git rev-parse` / `git symbolic-ref` / `git merge-base --is-ancestor` /
  `sed` (read-only), `mkdir` for review subdirs, and — the lone git-level
  mutation of existing tracked files in this skill —
  `git merge --ff-only origin/<branch>`, run only after explicit user
  confirmation in Phase 0 step 5e.
```

`## Failure modes to watch for` (`:293`) — add two bullets:

```markdown
- **Origin remote missing or unreachable.** Skip silently (token
  `origin: skipped (no remote)`); fetch failure is non-fatal and proceeds
  with available refs; any other git failure in step 5 not handled by an
  explicit 5e branch (the ff-abort keeps its own token) maps to
  `origin: skipped (git error)`. Same posture as the upstream check.
- **Diverged local branch.** Fast-forward is impossible — warn and proceed;
  never merge or rebase. Likewise, a user-confirmed ff update that git
  aborts (uncommitted changes in the way) proceeds on the stale tree after
  printing git's error. In both cases reviewers may still produce
  stale-tree false positives; the warning names the cause, which is the
  bulk of the value.
```

## Test plan

Documentation-only spec — review checklist (per the VHS-7 convention). A reviewer verifies:

1. **Origin check structure.** New step 5 has sub-steps a–e mirroring the VHS-6 idiom (detect → fetch → resolve → count → prompt); every exit path logs a token (including the step-level `git error` catch-all); the only mutation is the user-confirmed `git merge --ff-only` on a counterpart comparison; the fallback comparison is informational-only; diverged and ff-aborted paths never retry with merge/rebase/stash; the on-update branch re-validates the brief, CLAUDE.md, and the spec output path.
2. **Renumbering integrity.** Steps 5–6 are now 6–7; grep `skills/spec-cycle/SKILL.md` for `step 5`, `step 6`, `step 7` and confirm every reference points at the intended step (step-4 sub-steps' six "continue to step 5" lines now land on the origin check by design; `:107` and `:147` say "step 7").
3. **Preflight summary** lists both the upstream and the seven-token origin vocabularies.
4. **Post-green polish.** § 2g exists with the three guardrails verbatim (tagged-P2s-only; clarifications-only with hard limits; no re-review); candidates are collected from all rounds' reports; 2g performs the green-round Deferred carry-forward; 2d and 2e cross-reference it; the `## Post-green polish` spec-section mechanic is described.
5. **Agent-file consistency.** All three agent files carry (a) the identical `**Pre-ship recommended:**` template line inside the findings template, (b) the identical defining sentence after the template's closing fence (not inside it), and (c) the identical `closure_manifest` line in the orchestrator-inputs block; STATUS contract, severity definitions, and step-7 sections are byte-identical to before.
6. **Brief-path resolution.** Step 1 names both tolerances, pins the anchored regex `^[A-Z][A-Z0-9]*-[0-9]+`, includes the two-ID-token disambiguation example (`PROJ-86-fix-API-33-regression.md` → `PROJ-86`), defines path normalization (project_root-relative, forward slashes) and the out-of-root halt-and-ask, and states the canonical-artifact-location rule; `docs/customizing.md` § "Spec & brief layout" reflects the tolerance, including its closing sentence.
7. **2b prompt.** `brief_path` is the resolved-and-normalized path; the closure-manifest block is mandated for rounds N > 1, P0/P1-only, with the stated format including the synthetic missing-STATUS notation.
8. **Sync round-trip.** `python sync.py status` shows exactly the four edited files under the synced subtrees (`docs/customizing.md` is repo-only); after `python sync.py install`, `python sync.py push` round-trips byte-for-byte (no diff).
9. **Dry-run transcript.** In a scratch repo with a deliberately stale local branch (clone, then `git reset --hard HEAD~2`), walk step 5 manually and capture transcripts for all three mutation-adjacent paths: (a) ff-success — behind-N warning, prompt, successful `--ff-only` update; (b) diverged — add a local commit after the reset, verify the diverged warning and that no update is offered; (c) ff-abort — dirty a tracked file the incoming commits touch, confirm the update, verify git's abort is printed verbatim and the skill proceeds without retry. Attach the transcripts as the PR's test-output artifact (ship-spec audit trail).

## Test command

N/A

## Done when

1. Phase 0 contains an origin-sync check after the upstream block — `git fetch origin` (bounded timeout, non-fatal) + `git rev-list --count HEAD..origin/<cmp>`; a counterpart comparison with behind-count > 0 produces a warning and an explicit user choice (ff-only update / proceed); no `origin` remote → silent skip with summary token. (§ D1) (User choice on counterpart comparisons with fast-forward feasible only — fallback comparisons are informational and diverged branches are warn-only per Decision 1, narrowing the brief's unconditional bullet 1; brief Risk §6 delegated this path.)
2. The preflight summary line includes an origin token (seven-token vocabulary per § D1 rationale, superseding the brief's four-token list). (§ D1)
3. A post-green polish step exists between the gate and Phase 3 with the three guardrails stated explicitly; 2d/2e `## Deferred (P2+)` language cross-references it. (§ D2)
4. Reviewer findings format supports an explicit pre-ship-recommended marker on P2s, and the polish step keys off it. (§ D5, § D2 step 1)
5. Phase 0 step 1 documents alternate brief directories and descriptive-suffix filenames; ticket-id extraction is pinned to `^[A-Z][A-Z0-9]*-[0-9]+` (digit-tolerant superset of the brief's `^[A-Z]+-[0-9]+`); canonical artifact location is stated. (§ D3)
6. The 2b prompt passes the resolved `brief_path` and, for rounds N > 1, includes the mandated closure-manifest block. (§ D4)
7. `## Tool-use notes` and `## Failure modes` cover the new git operations and the two new failure modes. (§ D6)
8. `python sync.py status` shows the edits cleanly; `python sync.py push` round-trips byte-for-byte. (§ Test plan 8)
9. A dry-run transcript shows the origin check firing, the user prompt, and the ff-only path — plus the diverged and ff-abort paths — pinned via Test-plan item 9 and attached at ship time. (§ Test plan 9)

## Out of scope

- Mirroring the origin-sync check into `/ship-spec` Phase 0 (it works in an isolated worktree cut from a fresh ref).
- Auto-pull, merge, or rebase of any kind — no working-tree mutation without explicit confirmation.
- Custom remote names beyond the literal `origin` and `upstream`.
- Rewriting the reviewer agents' step-7 closure logic or closure-table format.
- Changing the green-gate formula, severity scale, or round cap.
- A general brief-discovery search (globbing for candidate briefs) — only the two named layout tolerances.
- Normalizing or moving existing briefs already on disk in any repo.
- LLM classification of origin-commit relevance — behind-count is the only signal; relevance heuristics stay in the upstream check.

## Deferred (P2+)

- **conventions/R1/F-5** (P3) — token-vocabulary expansion is a spec-level addition with rationale; no spec edit needed beyond the Done-when 2 annotation (done). The Phase 3 drift-check row for brief Done-when bullet 2 will note the expanded vocabulary at render time.
- **conventions/R1/F-6** (P3) — fetch-before-resolve ordering deviation is flagged with rationale in Decision 2 (category (c), informational); no further action.

## Post-green polish (round 2)

Spec went green at round 2 (all three lenses `STATUS: GREEN`, total P0+P1 = 0). The round-2 reports carried 8 distinct P3/P4 clarifications with concrete suggested fixes; all were folded in as clarifications per the PET-86 precedent this spec's own § D2 formalizes (the running skill version predates the `Pre-ship recommended` marker, so the prose-recommendation fallback applies). No Decisions, Out-of-scope fences, or Done-when criteria were reworded — Done-when 1 gained a parenthetical annotation only.

- **correctness/R2/F-1 + conventions/R2/F-3** — D3's customizing.md instruction now also updates the section's closing sentence (`:60`) and restores the "loose: just enough to get started" parenthetical.
- **correctness/R2/F-2 + edge-cases/R2/F-3 + conventions/R2/F-2** — Done-when 1 annotated: user choice on counterpart comparisons with ff feasible only; fallback informational, diverged warn-only, per Decision 1.
- **edge-cases/R2/F-1** — 2g step-3 hard limits extended to protect Done-when (parenthetical annotations only).
- **edge-cases/R2/F-2** — D3 step 1 defines the out-of-root brief path: halt-and-ask, absolute path on confirm.
- **edge-cases/R2/F-4** — D6 failure-modes bullet 1 qualified: catch-all excludes tokens owned by explicit 5e branches (ff-abort).
- **edge-cases/R2/F-5** — 2g intro gains a re-entry rule: existing `## Post-green polish` section → reconcile, don't append.
- **conventions/R2/F-1** — D3's regex example genericized to `PROJ-86-fix-API-33-regression.md` → `PROJ-86` (public repo; internal ticket IDs stay out of skill text); Test-plan item 6 updated to match.
- **conventions/R2/F-4** — D4's P0/P1-only rationale reworded: P2 dispositions are visible in the spec's edits or its Deferred section.
