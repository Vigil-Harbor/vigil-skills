# AGENTS.md

Project instructions for any AI agent working in the **vigil-skills** repo. Harness-neutral by intent — written for Claude Code, Hermes, or any agent that reads an `AGENTS.md`. Machine-local paths and personal tips live in a gitignored `CLAUDE.md` (or your harness's local config) that points here.

## What this repo is

Cross-machine agent skills and subagents. Not an application — no build step, no dependencies beyond Python 3.8+ stdlib; a stdlib `unittest` suite lives under `tests/` (run `python -m unittest discover -s tests -p 'test_*.py'`). The repo is a source-of-truth mirror for files that get installed into your agent's config dir (for Claude Code: `~/.claude/skills/` and `~/.claude/agents/`).

## Sync commands

```bash
python sync.py install          # repo → ~/.claude/ (daily driver after git pull)
python sync.py push             # ~/.claude/ → repo (commit back in-place edits)
python sync.py status           # diff between repo and ~/.claude/
```

Flags: `--dry-run`, `--verbose`, `--prune` (install only), `--claude-dir <path>`.

## Architecture

### Workflow: spec lifecycle

Six skills form the spec lifecycle; the third is optional. The interview stage is separate so the brief — the artifact every reviewer treats as authority — is settled before review context is spent; the authoring/impl pair runs in separate sessions to avoid token-cap pressure; the post-merge close runs after code ships:

1. **`/spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`** — Produces the brief: resolves the ticket, grounds against the repo and wiki, runs the bounded interview, and writes `docs/specs/TODO/<TICKET-ID>.brief.md`. Reads tickets; never creates or transitions them.

2. **`/spec-cycle <brief-path> [--attest "<reason>" | --full]`** — Authors a spec from a brief and runs the parallel review until green or `round_cap` passes complete, then halts with a drift-check checklist. The green NEXT recommends `/spec-tickets` when the spec splits, else `/ship-spec`.

3. **`/spec-tickets <spec-path>`** *(optional)* — Invoking it files the pieces after its draft checks pass: blocked-by relations where the tracker has them, a `Blocked by` section where it does not, one local file per piece when no tracker is connected. A one-piece spec files nothing, and existing pieces stop a re-run.

4. **`/ship-spec <spec-path>`** — Reads the spec's verdict marker in preflight (green passes, red halts, anything else warns and continues with an unchecked PR-body line), then implements in an isolated git worktree through the test gate, an optional review gate, commit, PR, and the issue-tracker update. The primary working tree is never touched, except a copy of an ignored test-output or review artifact into `docs/specs/TODO/`; git does not track that copy.

5. **`/spec-land <PR-number | PR-URL | spec-path>`** — After the PR is merged and before spec-close, confirm the landed code, move the Plane ticket, write the wiki merge line and filemap delta, then remove the worktree and branch and run the post-land command. Never merges and never commits.

6. **`/spec-close <spec-path> [--report-only | --partial]`** (the argument may also be a ticket id or a `docs/specs/TODO/<TICKET-ID>/` folder) — After `/spec-land`, reconcile the spec against shipped code, propose wiki entries sized to the brief's tier, archive artifacts from `TODO/` to `DONE/<TICKET-ID>/`, and prepend a `close |` entry to the wiki's `log.md`. A ticket with artifacts but no spec gets an archive-only close.

**Stakes tier.** The operator sets a tier in `/spec-brief`, and ceremony follows it. `tweak` stops in spec-brief with nothing written. `small` is the three standing lenses, `round_cap` 2, and `/ship-spec` skips the review gate while keeping the test gate. `big` is today's behaviour and is what an absent tier means. spec-brief offers the doubt pass at every tier when a reviewer is eligible and requires it for `irreversible`. `irreversible` is `big` plus the tier on every reviewer prompt plus a review gate that stops instead of committing when the review did not run; spec-brief requires a doubt pass, halts before the interview when no reviewer is eligible, and never skips a failed dispatch. Scale stays its own `## Scale` declaration and never follows from the tier.

### Parallel review agents

`spec-cycle` dispatches read-only reviewer subagents **in parallel** (single message — three by default, plus an optional fourth when the brief declares scale):

| Agent | Lens | Key concern |
|-------|------|-------------|
| `spec-reviewer-correctness` | Does it solve the brief? | Nonexistent references, unmet acceptance criteria, internal contradictions, ground-truth ledger samples |
| `spec-reviewer-edge-cases` | What breaks it? | Empty inputs, concurrency, external-system failures, observability gaps |
| `spec-reviewer-conventions` | Does it follow the repo? | AGENTS.md / CLAUDE.md rules, wiki decisions, stale prior-spec mechanisms, premature abstractions, duplicate code |
| `spec-reviewer-scalability` | Does it hold at N×? *(optional — dispatched only when the brief declares scale)* | Batching, algorithmic complexity, unbounded accumulation, per-instance state collision, uncapped fan-out, cost/token budget |

Each agent emits a `STATUS: GREEN` or `STATUS: RED P0=<n> P1=<n> ...` last line. The orchestrator parses this to gate the loop.

### /review-pr

Standalone skill for triaging CodeRabbit review comments. Reads findings, verifies against current code, fixes real issues, pushes, posts per-thread commit-hash replies (`Resolved in <sha>`), conditionally waits for CodeRabbit's incremental re-review, and polls for auto-approval. Inline findings that are not fixes are skip, with a reason, or defer, and each gets a per-thread reply. Body findings, which have no thread, are listed in one PR comment per round; threads that stay unresolved are left open for CodeRabbit and the user to handle naturally. Checks `.coderabbit.yaml` for `request_changes_workflow: true` to determine whether auto-approval is expected.

**Review cadence for this repository.** Before another corrective push:

1. Collect every current inline thread and body finding, including Follow-up Comments and later pages. Record the reviewed head, each finding's source, its current-code evidence, and its disposition. Distinguish demonstrated blockers, valid nonblocking improvements, duplicates or misreads, and optional wording. A reviewer label alone does not establish impact; retain the skill's Critical/Major rules and verify disputed claims.
2. Batch the corrections locally. Trace each changed rule through its consumers and neighboring branches; use an existing behavioral replay pack when available, plus the required tests and lint. Record the exact candidate and validation limits. Reopen checks only for changed behavior, invalidated evidence, or a newly demonstrated gap.
3. Publish the validated batch once when authorized. Reply with the actual pushed commit; never claim an unpushed fix is resolved remotely. Prefer automatic review for that head. Before any manual request, check whether review is already queued, running, or complete. At most one authorized manual request per batch is appropriate when automatic review does not cover it; do not escalate a rejected request to full review or resume without separate authorization.
4. Do not retry requests when the service is paused, allowance is exhausted, a request is rejected, or the skill's bounded wait expires. Report the head, outstanding findings, verdict and service state. A stale verdict or successful check is not current-head approval. Report allowance notices with their observation time; do not infer a live balance or reset time.
5. A new demonstrated blocker requires local diagnosis of its related rules and a newly validated batch before another push. Give nonblocking suggestions an evidence-based fix, skip, or tracked defer disposition; optional wording alone does not justify repeated review requests. Stopping a review loop does not clear unresolved blockers or waive required checks. Keep `request_changes_workflow` enabled, leave configuration changes to a separate decision, and merge only with explicit user authorization.

### /key-rotation

Process guide for a credential-exposure response. The operator performs every provider action. The record lives in the target project and is gitignored by the preflight script. The optional project section is documented in `docs/customizing.md`.

### File layout

- `skills/<name>/SKILL.md` — Skill definitions (YAML frontmatter + markdown body). Installed to `~/.claude/skills/<name>/SKILL.md`.
- `agents/<name>.md` — Subagent definitions. Installed to `~/.claude/agents/<name>.md`.
- `skills/ship-spec/states.json` — Committed map of project identifiers to state UUIDs and review-state IDs. Synced alongside SKILL.md by `sync.py`.
- Bundled scripts: `skills/spec-cycle/scripts/verdict_marker.py`, `skills/spec-land/scripts/land_check.py`, `skills/spec-close/scripts/archive_spec.py` and `prepend_log_entry.py`, `skills/spec-brief/scripts/check_premises.py`, `skills/session-handoff/scripts/`, `skills/key-rotation/scripts/prepare_record.py`, `skills/hermes-kanban-awareness/scripts/read_board.py`.
- `reference/` folders — templates and schemas a skill reads beside its script.
- `sync.py` — Bidirectional file sync. Stdlib only, cross-platform via `pathlib`.
- `lint.py` — Portability lint for skills (`python lint.py --strict` to gate).
- `tests/` — Stdlib `unittest` suite.
- `docs/customizing.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, and `docs/spec-workflow-reference.md` — project setup, the portability contract, authoring discipline, and the lifecycle overview.

## Superseded vendor skills

Remove a retired copy by hand with a targeted delete, never `python sync.py install --prune`, which deletes third-party skills.

- `agentcraft-handoff` (VHS-28, replaced by `session-handoff`, delete the vendor copy by hand).
- `grilling` / `grill-me` (VHS-32, superseded by overwrite; rename an upstream copy to keep it).
- `bloat-check` (VHS-46, retired; ship-spec's review gate carries its veto; delete by hand).
- `talaria` (2026-10-11, retired; delete by hand).

## Plan & Spec Reviews

- Always verify load-bearing claims against the actual codebase, wiki, and current file state before critiquing — never review from memory or stale buffers.
- Re-read files at the start of each new review pass; the user iterates plans frequently and stale context produces false-positive findings that require retraction.
- Deliver findings as severity-ranked lists (critical/high/medium/low) with specific `file:line` references.

## Conventions

- Skills use `name`, `description`, `user_invocable`; agents use `name`, `description`.
- Reviewer agents are **read-only** — they must never edit files or mutate git state.
- Severity scale is shared across all reviewers (the three default lenses plus the optional scalability lens): P0/P1 block shipping — except that a finding the author routed, under the scope ceiling, to a well-formed row in the spec's `## Deferred — follow-up required` section is not re-filed by the reviewers and so never enters the gate — a malformed row, a duplicate section, a routing-changing scope error, or an undischarged in-scope P0 or P1 row, including a grill row the ceiling classifies as in-scope, is still filed as a P0; P2+ do not. Reserve P0/P1 for genuinely load-bearing issues. Those definitions do not change with tier.
- `sync.py` mirrors only the `skills/` and `agents/` subtrees (defined in `SUBTREES`). Adding a new top-level subtree requires updating that tuple.
- Specs, briefs, and reviews live in the **target project** at `docs/specs/TODO/<TICKET-ID>.*`, not in this repo.
- A brief may carry an optional `## Scale` section to turn on the scalability reviewer: `**Factor:** yes` plus a `**Target:**` line (the target N the design must hold at — requests/sec, records, tenants, $/op, etc.) enables the lens; `**Factor:** no` (or `none` / `n/a`) records scale as an explicit non-factor. Absent the section, the lens stays off and the loop runs the three default lenses unchanged. The full grammar is spec-cycle's Phase 0 Scale step (`skills/spec-cycle/SKILL.md`). A brief may carry an optional `## Tier` section (`**Level:**` `small`, `big`, or `irreversible`); an absent tier is `big`.
- `CLAUDE.md` is gitignored (it holds machine-local absolute paths). Anything that must ship in a PR — including "referenced from project guidance" pointers — belongs in a **tracked** file (`AGENTS.md`, `README.md`, or `docs/`), not `CLAUDE.md`.

## Post-merge wiki update

After a PR merges, run `/spec-land` from the target repo. It writes the merge log line and the filemap delta.

For the fallback, run `/wiki-after-merge <commit-sha>` **from the wiki directory**. It prepends to `log.md`. That command remains the fallback for comprehension stubs, state.md header notes, sibling Plane tickets, and merges outside the lifecycle. Idempotent — safe to re-run for the same SHA. Manual edits are fine for trivial single-file fixes; the skill handles everything else.

State.md edits require an evidence triple (Plane ID, date, commit hash) — the wiki's pre-commit hook enforces this. See the wiki's `CLAUDE.md` § "Editing state.md safely" for field rules per section.

## Git Hygiene

- Before committing, audit staged paths for stale skill copies, backup files, and large binaries; add to `.gitignore` rather than committing.
- After context compaction or long sessions, verify no orphaned cron jobs or background tasks were left running.

## External dependencies (runtime, not build)

- **Plane connector** — ticket reads and state updates, live. Skills warn and proceed when a read fails; `wiki-state-update` refuses instead, and `/spec-tickets` halts when a connected tracker cannot read the parent or its children.
- **`gh` CLI** — PR creation, CodeRabbit thread management. Must be authenticated.
- **CodeRabbit** — configured on target repos for `/review-pr`.

## Machine-local config

Absolute paths specific to your machine — your installed-config dir and the `vigil-harbor-wiki` checkout location (the latter is what the skills' preflight resolves as `wiki_root`) — live in your local, gitignored `CLAUDE.md`, which points here for everything else.

## Wiki

Slug: vigil-skills
Log: on
Filemap: on

The wiki path stays in gitignored `CLAUDE.md`. This section does not copy it.

## Post-land command

python sync.py install
