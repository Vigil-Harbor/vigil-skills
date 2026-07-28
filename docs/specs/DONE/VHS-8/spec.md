# VHS-8 — /spec-reconcile + /spec-retire: post-convention spec retirement pipeline

## Goal

Ship two new user-invocable skills (`/spec-reconcile` and `/spec-retire`) that complete the spec lifecycle: after `/ship-spec` merges a PR, `/spec-reconcile` diffs the spec against shipped code, and `/spec-retire` decomposes the spec into wiki entries and archives the artifacts. Together they drain the 22-spec backlog identified in the spec migration manifest, plus handle the partial-retire case (DYN-34/34b pattern). No changes to existing skills.

## Scope

**New files:**
- `skills/spec-reconcile/SKILL.md` — full skill definition (YAML frontmatter + phased body)
- `skills/spec-retire/SKILL.md` — full skill definition (YAML frontmatter + phased body)

**Modified files:**
- `CLAUDE.md` — extend the "Workflow: spec-cycle -> ship-spec" subsection to document the full lifecycle

**Not changed:**
- `skills/ship-spec/SKILL.md`, `skills/spec-cycle/SKILL.md`, `skills/review-pr/SKILL.md` — untouched
- `skills/ship-spec/states.json` — already maps MCP, DYN, VHS, ADA; no additions
- `sync.py` — already mirrors `skills/` subtree; new dirs are auto-discovered
- `agents/*.md` — reviewer agents are for spec-cycle's review loop, not these skills

## Decisions

### Decision 1 — Two skills, not one

Reconcile is read-only: it reads the spec, reads the code, and produces a report. Zero side effects — safe to run speculatively on any closed spec. Retire is mutating: it moves files, writes wiki entries, updates `state.md`, and appends `log.md`. Different blast radii warrant separate invocations with a user checkpoint between them.

Pipeline: `/spec-reconcile <spec>` -> user reviews report -> `/spec-retire <spec>`.

### Decision 2 — Plane state resolution via `list_states` + `group` matching

Both skills need to know whether a ticket is done. The manifest flagged 8 distinct "done" UUIDs across 4 projects, some of which are actually "PR Review" (resolved by `states.json`). Hardcoding UUIDs is brittle.

Approach: call `mcp__claude_ai_Plane__list_states(project_id)` at runtime. Accept any state where `group == "completed"` as terminal for full-retire. For partial-retire detection, any non-completed group (including `"started"`) signals the parent ticket is still active.

### Decision 3 — Reconciliation report is on disk, not stdout

The reconciliation report is the contract between the two skills. Writing it to `docs/specs/TODO/<TICKET-ID>.reconciliation.md` (alongside the spec) makes it:
- Auditable: the user can review it before running retire
- Persistent: retire can read it without re-doing the analysis
- Archivable: it moves to `DONE/` with the rest of the artifacts

The report ends with a machine-readable status line: `RECONCILED: <yes|no> DRIFT: <n>` where `<n>` is the count of drifted items. Retire reads this line to gate execution.

### Decision 4 — Partial-retire is auto-detected, `--partial` is an override

The brief mentions `--partial` as a flag. Auto-detection via Plane state group is more robust (no user error). Design:
- Default behavior: check Plane state. If `group != "completed"` and `group != "cancelled"`, enter partial-retire mode automatically.
- `--partial` flag: force partial-retire regardless of Plane state (for cases where auto-detection isn't appropriate).
- No `--force` flag. The brief doesn't specify one, and forcing full-retire on a non-completed ticket is high risk (wiki writes + state.md edits with incomplete evidence). If the user needs full-retire on a non-completed ticket, they should close the ticket in Plane first.

### Decision 5 — Archive to `DONE/<TICKET-ID>/` with mkdir-if-needed

model-adapter already uses `docs/specs/DONE/<TICKET>/spec.md`. Adopt this across all projects. The skill creates `DONE/<TICKET-ID>/` if it doesn't exist, then moves all artifacts:
- `<TICKET-ID>.spec.md` -> `DONE/<TICKET-ID>/spec.md`
- `<TICKET-ID>.brief.md` -> `DONE/<TICKET-ID>/brief.md`
- `<TICKET-ID>.reconciliation.md` -> `DONE/<TICKET-ID>/reconciliation.md`
- `<TICKET-ID>.reviews/` -> `DONE/<TICKET-ID>/reviews/`
- Any other companions (`*.test-output.txt`, `*.curation-protocol.md`, etc.) -> `DONE/<TICKET-ID>/`

Git operations: `git mv` for tracked files, plain `mv` + `git add` for untracked.

### Decision 6 — Duplicate detection is grep-based, not semantic

Before proposing wiki entries, search the wiki for existing coverage:
1. `grep -r "<TICKET-ID>" <wiki_root>/decisions/ <wiki_root>/comprehension/` — exact ticket match
2. `grep -ri "<slug-keywords>" <wiki_root>/decisions/` — key-term match from spec title

If matches found, list them to the user with file paths and one-line context. User decides: skip (entry already exists), merge (augment existing entry), or proceed (create new despite overlap). This is deterministic, fast, and doesn't require embedding search.

### Decision 7 — Wiki entry proposals are staged in-context, not on disk

Retire proposes wiki entries in its output (printed to conversation). The user reviews the proposals, then the skill writes approved entries to disk. This avoids creating draft files that might get accidentally committed or confused with real entries.

The exception: `state.md` updates are presented as diffs (old line -> new line) with the evidence triple already populated. The user approves, then the skill applies the edit.

### Decision 8 — `log.md` append format

Follow the existing convention observed in `log.md`:
```
## [YYYY-MM-DD] retire | <PROJECT> — <TICKET-ID>: <spec title> (archived from TODO/)

<1-3 sentences: what the spec covered, reconciliation status, wiki entries created.>
```

The `retire` action tag distinguishes retirement entries from `feat`/`fix`/`refactor` entries.

## Design

### `/spec-reconcile` — `skills/spec-reconcile/SKILL.md`

Invoked as: `/spec-reconcile <spec-path>` (e.g., `/spec-reconcile docs/specs/TODO/ADA-17.spec.md`).

YAML frontmatter:
```yaml
---
name: spec-reconcile
description: Diff a closed spec against shipped code. Produces a reconciliation report confirming implementation matches spec intent, or flags drift. Read-only — never edits code or spec files. Pair with /spec-retire to archive reconciled specs into the wiki.
user_invocable: true
---
```

#### Phase 0 — Preflight

1. Resolve `<spec-path>`. Expected shapes: `docs/specs/TODO/<TICKET-ID>.spec.md` or `docs/specs/DONE/<TICKET-ID>/spec.md`. Extract `ticket_id` (uppercase): from TODO paths, the filename stem before `.spec.md`; from DONE paths, the parent directory name. Derive `project_prefix` (portion before the first hyphen, e.g., `ADA` from `ADA-17`) and `issue_number` (portion after, e.g., `17`). Set `project_root` to the repo root (the directory containing `CLAUDE.md`).
2. Confirm the spec exists. Halt if not.
3. Read `<project_root>/CLAUDE.md`. Identify the wiki path (resolve username-bearing paths per spec-cycle convention).
4. Read `~/.claude/skills/ship-spec/states.json`. Look up ticket prefix to get `project_id` and `namespace`. If prefix not found, warn and default `namespace` to `"plane"`.
5. Verify Plane ticket state. Call `mcp__claude_ai_Plane__list_states(project_id)` to get the state map. Then look up the ticket via `mcp__claude_ai_Plane__retrieve_work_item_by_identifier(project_identifier, issue_number)`. Check whether the ticket's state falls in a `group == "completed"` or `group == "cancelled"` state. If not: halt with `Ticket <TICKET-ID> is not in a completed state (current: <state_name>). Reconciliation requires a completed ticket. Close the ticket in Plane or verify the correct spec path.` This matches the brief's "warn-and-halt" requirement — reconciliation targets shipped work, so a non-completed ticket signals the wrong spec or premature invocation.

Print a one-line preflight summary, then continue.

#### Phase 1 — Gather shipped state

Goal: identify what code actually shipped for this ticket.

1. **Find the merge commit(s).** Three strategies, tried in order:
   a. `git log --all --oneline --grep="<TICKET-ID>" -- .` — matches commit messages containing the ticket ID.
   b. Look up the Plane ticket via `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` with `tags: ["plane_work_item", "<TICKET-ID>"]`, `namespace` from preflight. Parse the description for PR references (`PR #N`, `#N`, `github.com/…/pull/N`).
   c. If neither yields results, prompt the user: `Could not find merge commit for <TICKET-ID>. Enter PR number or commit SHA:`

2. **Read the shipped diff.** For each identified PR/commit:
   - `gh pr view <N> --json files,additions,deletions` for file-level diff stat.
   - `gh pr diff <N>` (or `git show <SHA>`) for the full diff content. If the diff is large (>500 lines), summarize by file rather than reading every line.

3. **Read the spec's companion brief** at `docs/specs/TODO/<TICKET-ID>.brief.md` (if it exists). The brief's acceptance criteria are the primary reconciliation targets.

#### Phase 2 — Reconcile

Walk the spec section by section:

1. **Scope (files changed).** Compare the spec's "Scope" or "Edit" section against the PR's actual diff stat. For each file the spec says to change: confirm it appears in the diff. For each file in the diff that the spec doesn't mention: flag as "Added (not in spec)." For each file the spec mentions but the diff doesn't touch: flag as "Dropped."

2. **Decisions.** For each `### Decision` in the spec: read the relevant code (using the file paths from the diff) and confirm the decision is reflected. Use grep/file reads, not inference. Mark each as: Confirmed (code matches), Drifted (code diverges — describe how), or Unverifiable (decision is about behavior/performance, not structure).

3. **Acceptance criteria.** For each "Done when" bullet in the spec (or "Acceptance" in the brief): produce a grep or file-read that confirms the criterion is met. Mark as: Met (with evidence), Unmet (with explanation), or Unverifiable.

4. **Test plan.** Check whether the tests described in the spec's "Test plan" section exist in the codebase. Grep for test file names, function names, or describe blocks.

#### Phase 3 — Report

Write the reconciliation report alongside the spec. If the spec is at `docs/specs/TODO/<TICKET-ID>.spec.md`, write to `docs/specs/TODO/<TICKET-ID>.reconciliation.md`. If the spec is at `docs/specs/DONE/<TICKET-ID>/spec.md`, write to `docs/specs/DONE/<TICKET-ID>/reconciliation.md`.

Report format:

```markdown
# Reconciliation Report: <TICKET-ID>

> Date: YYYY-MM-DD
> Spec: docs/specs/TODO/<TICKET-ID>.spec.md
> Merge: <PR number or commit SHA>
> Plane state: <state_name> (group: <group>)

## Summary
<1-2 sentences: overall reconciliation status.>

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `path/to/file.ts` | Yes | As specified |
| `path/to/other.ts` | No | Dropped — <reason> |

Unexpected files in diff (not in spec):
- `path/to/surprise.ts` — <what it does>

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | <title> | Confirmed | `file:line` — '<excerpt>' |
| 2 | <title> | Drifted | <explanation> |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | <criterion> | Met | `file:line` — '<excerpt>' |
| 2 | <criterion> | Unmet | <explanation> |

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| <test description> | Yes | `path/to/test.ts:line` |

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- <Decision N>: <why it's wiki-worthy — non-obvious, reusable, or constraining>
- <Comprehension>: <what changed and why, for the comprehension layer>

RECONCILED: <yes|no> DRIFT: <n>
```

The `RECONCILED: yes` status requires: all acceptance criteria Met or Unverifiable, zero Unmet. Drifted decisions alone don't block — drift is informational. `DRIFT: <n>` counts Drifted + Dropped + Unexpected items.

Tool-use notes for spec-reconcile:
- Read, Grep for code verification. `gh pr view` / `gh pr diff` for PR data.
- `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` for Plane ticket lookup.
- `mcp__claude_ai_Plane__list_states` and `mcp__claude_ai_Plane__retrieve_work_item_by_identifier` for state verification.
- Bash for `git log --grep` (read-only).
- Write for the reconciliation report.
- This skill is read-only. It must never edit code files, spec files, or wiki files.

Failure modes for spec-reconcile:
- **Merge commit not found.** Fall back to user prompt. Common for tickets where commit messages don't include the ticket ID (older conventions).
- **Large diffs.** PRs with >500 lines of diff: summarize by file, don't try to read every line. Focus grep on the specific code paths the spec's decisions describe.
- **Plane ticket not in MCP memory.** Warn and proceed using only git log + brief. The brief is the local source of truth for acceptance criteria.
- **Cross-repo specs.** The skill runs in the target repo (where the spec lives). Wiki path comes from that repo's CLAUDE.md. No cross-repo file access needed during reconciliation.

---

### `/spec-retire` — `skills/spec-retire/SKILL.md`

Invoked as: `/spec-retire <spec-path>` or `/spec-retire <spec-path> --partial`.

YAML frontmatter:
```yaml
---
name: spec-retire
description: Decompose a reconciled spec into wiki entries (decisions, comprehension, state.md updates), archive the spec and companions to DONE/, and append to wiki log.md. Checks Plane state to gate full-retire vs. partial-retire. Run /spec-reconcile first. Pair with /spec-cycle and /ship-spec for the full spec lifecycle.
user_invocable: true
---
```

#### Phase 0 — Preflight

1. Resolve `<spec-path>`. Extract `ticket_id`, `project_prefix`, `issue_number`, and `project_root` using the same parsing rules as spec-reconcile Phase 0 step 1.
2. Confirm the spec exists. Halt if not.
3. Confirm the reconciliation report exists alongside the spec (same directory, `<TICKET-ID>.reconciliation.md` or `reconciliation.md`). If not: halt with `Reconciliation report not found. Run /spec-reconcile docs/specs/TODO/<TICKET-ID>.spec.md first.`
4. Read the reconciliation report's last non-blank line. Parse `RECONCILED: <yes|no> DRIFT: <n>`. If `RECONCILED: no`, warn: `Spec has unmet acceptance criteria. Review the reconciliation report before proceeding. Continue anyway? [y/N]`. Halt on N.
5. Read `<project_root>/CLAUDE.md`. Identify the wiki path. Confirm the wiki directory exists.
6. Read `~/.claude/skills/ship-spec/states.json`. Look up ticket prefix.
7. Check for `--partial` flag in invocation args. If present, force partial-retire regardless of Plane state.

Print a one-line preflight summary, then continue.

#### Phase 1 — Plane state gate

1. Call `mcp__claude_ai_Plane__list_states(project_id)` to get the full state map with groups.
2. Look up the ticket via `mcp__claude_ai_Plane__retrieve_work_item_by_identifier(project_identifier, issue_number)`.
3. Match the ticket's `state` UUID against the state map to determine the group.
4. Determine mode:
   - `group == "completed"` or `group == "cancelled"` -> **full-retire**.
   - `--partial` flag was set -> **partial-retire** (regardless of state).
   - Any other group -> **partial-retire** (auto-detected). Print: `Ticket <TICKET-ID> is in state "<state_name>" (group: <group>). Entering partial-retire mode: archiving spec artifacts only, skipping wiki decomposition.`

#### Phase 2 — Analysis

##### 2a. Duplicate detection

Search the wiki for existing entries related to this ticket:

```bash
grep -rl "<TICKET-ID>" <wiki_root>/decisions/ <wiki_root>/comprehension/
grep -rli "<key-terms>" <wiki_root>/decisions/ <wiki_root>/comprehension/
```

Where `<key-terms>` are 2-3 distinctive words from the spec's Goal section (not common words like "fix" or "update").

If matches found, read each matched file's title and first paragraph. Present to user:
```
Pre-existing wiki entries found:
  1. decisions/2026-05-06-dyn-34-score-calibration-pipeline.md — "Decision: DYN-34a score calibration pipeline"
  2. comprehension/2026-05-06-dyn-34b-ui-calibration-overlay.md — "Comprehension: DYN-34b calibration UI overlay"

These may already cover some or all of the spec's content.
Duplicates will be excluded from wiki proposals below.
```

Track matched ticket IDs and decision titles as an exclusion list for Phase 2b.

##### 2b. Wiki decomposition (full-retire only)

Skip entirely for partial-retire. For full-retire:

1. Read the reconciliation report's "Wiki-ready" section and the spec's "Decisions" sections.
2. For each decision worth extracting (non-trivial, reusable, or constraining — skip implementation-detail decisions like "use `git mv` not `mv`"):
   - Check against the duplicate exclusion list. Skip if covered.
   - Draft a wiki decision entry following SCHEMA.md's standard or multi-judgment format. Include: Context (from spec's Goal), Options Considered (from spec's Decision rationale), Decision (what was chosen), Consequences, Related links.
3. If the spec describes a significant architectural change (new module, new data flow, new integration):
   - Draft a comprehension entry following SCHEMA.md's template. Include: What Changed, Why, What Would Break, Files Touched, Judgment Calls.
4. For `state.md` updates:
   - If the ticket was in "What's Next" or "What's Active", propose moving it to "What's Shipped" with the evidence triple:
     ```
     ### <Title> (<TICKET-ID>, <ship-date>, commit <merge-sha>)
     Verification: <file>:<line> -- '<excerpt>'.
     ```
   - The ship date: try `completed_at` from the Plane ticket first; if null, fall back to the merge commit date from `git log --format=%ci <merge-sha>`, then to today's date as last resort (with a warning). The merge SHA comes from the reconciliation report. The verification line comes from the reconciliation report's acceptance criteria evidence.

##### 2c. Compile proposals

Collect all proposed actions into a single summary:
- Wiki decisions to create (with filenames and content previews)
- Wiki comprehension entries to create
- `state.md` edits (as diffs)
- Files to archive (list of `TODO/` -> `DONE/` moves)
- `log.md` entry (full text)

For partial-retire, this section contains only the archive list and log.md entry.

#### Phase 3 — User confirmation

Present the compiled proposals:
```
=== RETIREMENT PLAN: <TICKET-ID> ===
Mode: <full-retire | partial-retire>

Wiki entries to create:
  1. decisions/YYYY-MM-DD-<slug>.md — "<title>"
     <3-line preview>
  2. comprehension/YYYY-MM-DD-<slug>.md — "<title>"
     <3-line preview>

State.md update:
  File: projects/<project>/state.md
  Move "<Title>" from What's Active → What's Shipped
  Evidence: (<TICKET-ID>, YYYY-MM-DD, commit <SHA>)

Archive (TODO/ → DONE/<TICKET-ID>/):
  - <TICKET-ID>.spec.md
  - <TICKET-ID>.brief.md
  - <TICKET-ID>.reconciliation.md
  - <TICKET-ID>.reviews/ (N files)

Log.md append:
  ## [YYYY-MM-DD] retire | <PROJECT> — <TICKET-ID>: <title>
  <summary>

Proceed? [y/N]
```

Halt for user confirmation. On `N`: exit without changes. On `y`: continue to Phase 4.

#### Phase 4 — Execute

All file operations happen here, after user approval.

1. **Wiki entries** (full-retire only). Write each approved decision/comprehension file to `<wiki_root>/decisions/` or `<wiki_root>/comprehension/`.

2. **State.md update** (full-retire only). Apply the approved `state.md` edit. The edit must include the evidence triple — if the evidence is incomplete (no merge SHA, no verification grep), skip the `state.md` edit and warn: `state.md update skipped: incomplete evidence triple. Run /wiki-state-update manually.`

3. **Archive.** In the target repo:
   ```bash
   mkdir -p docs/specs/DONE/<TICKET-ID>
   git mv docs/specs/TODO/<TICKET-ID>.spec.md docs/specs/DONE/<TICKET-ID>/spec.md
   ```
   Repeat for brief, reconciliation report, reviews directory, and any companions. For untracked files (not yet committed), use `mv` + `git add` instead of `git mv`.

4. **Log.md.** Append the approved entry to `<wiki_root>/log.md`. Idempotency: `grep -F "<TICKET-ID>" <wiki_root>/log.md` first; skip if already present.

5. **Do not commit.** The skill writes to two separate repos (target repo for archive, wiki repo for entries). Neither is committed — the user controls commit timing.

Print at the end:
```
=== RETIREMENT COMPLETE: <TICKET-ID> ===

Target repo (<project_root>):
  Archived: TODO/<TICKET-ID>.* → DONE/<TICKET-ID>/
  Status: uncommitted — review with `git diff --stat` then commit.

Wiki (<wiki_root>):
  Created: decisions/YYYY-MM-DD-<slug>.md
  Created: comprehension/YYYY-MM-DD-<slug>.md
  Updated: projects/<project>/state.md
  Appended: log.md
  Status: uncommitted — review with `git diff --stat` then commit.

Suggested commits:
  (in target repo)  git add docs/specs/ && git commit -m "retire(<ticket-lower>): archive spec to DONE/"
  (in wiki)         git add -A && git commit -m "retire(<ticket-lower>): wiki harvest from <TICKET-ID>"
```

Tool-use notes for spec-retire:
- Read, Grep for duplicate detection and evidence extraction.
- Write for wiki entries and log.md.
- Edit for state.md updates (surgical line replacement).
- Bash for `git mv`, `mkdir -p`, `grep -F` (idempotency check), `git status`.
- `mcp__claude_ai_Plane__list_states` and `mcp__claude_ai_Plane__retrieve_work_item_by_identifier` for state gate.
- This skill mutates files in both the target repo and the wiki repo. All mutations happen in Phase 4, after user confirmation in Phase 3.

Failure modes for spec-retire:
- **Reconciliation report missing.** Hard halt at preflight. The user must run `/spec-reconcile` first.
- **Reconciliation report says `RECONCILED: no`.** Soft halt with user override. Some specs may have unmet criteria that are acceptable (e.g., descoped items). The user decides.
- **Plane ticket not found.** Warn and proceed. Default to partial-retire if the ticket can't be looked up — this is the safer path (archive only, no wiki writes or state.md edits). The user can re-run once Plane is available to get full-retire with wiki decomposition.
- **Wiki path not found.** Halt. The wiki is required for retirement — without it, there's nowhere to write entries. The user must configure the wiki path in their repo's CLAUDE.md.
- **`state.md` evidence incomplete.** Skip the `state.md` update, warn, and suggest `/wiki-state-update` as a follow-up. Don't block the rest of the retirement.
- **Untracked spec files.** Some spec artifacts may not be committed yet (e.g., VHS-1 through VHS-6 are untracked per `git status`). Use `mv` + `git add` instead of `git mv` for untracked files. Detect via `git ls-files --error-unmatch <file> 2>/dev/null`.
- **Cross-repo commit discipline.** The skill writes to two repos but commits to neither. Print explicit commit suggestions for both repos. The user controls when and how to commit.

---

### CLAUDE.md changes

**Heading rename:** Change `### Workflow: spec-cycle -> ship-spec` to `### Workflow: spec lifecycle`. The pipeline is now 4 skills, not 2.

**Intro paragraph:** Replace "The two main skills form a split pipeline designed to avoid token-cap pressure:" with "Four skills form the spec lifecycle. The authoring/impl pair runs in separate sessions to avoid token-cap pressure; the post-merge pair runs after code ships:"

**Extend numbered list:** Add after the existing ship-spec entry:

```markdown
3. **`/spec-reconcile <spec-path>`** — After ship-spec's PR merges, reconcile the spec against shipped code. Produces a reconciliation report (`<TICKET-ID>.reconciliation.md`) confirming what matched, what drifted, and what's worth extracting to the wiki. Read-only — no mutations.

4. **`/spec-retire <spec-path> [--partial]`** — Consumes the reconciliation report. Proposes wiki entries (decisions, comprehension, state.md updates), archives spec artifacts from `TODO/` to `DONE/<TICKET-ID>/`, and appends to wiki `log.md`. Auto-detects partial-retire when the Plane ticket isn't completed. All mutations require user confirmation before execution.
```

**File layout section:** Add to the `### File layout` bullet list:
```markdown
- `skills/spec-reconcile/SKILL.md` — Reconciliation skill. Installed to `~/.claude/skills/spec-reconcile/SKILL.md`.
- `skills/spec-retire/SKILL.md` — Retirement skill. Installed to `~/.claude/skills/spec-retire/SKILL.md`.
```

## Test plan

This is a markdown-only repo with no automated test suite. Validation:

1. **Structural.** `python sync.py install --dry-run --verbose` discovers and would install both new skills without error.
2. **Frontmatter.** Both SKILL.md files have valid YAML frontmatter with `name`, `description`, and `user_invocable: true`.
3. **Internal consistency.** Each skill's phases reference the correct tools, the phase ordering is logical (no forward-references to unresolved state), and tool-use notes list every tool the phases use.
4. **CLAUDE.md accuracy.** The updated workflow section matches the actual skill definitions (names, invocation syntax, behavior descriptions).

## Test command

```bash
python sync.py install --dry-run --verbose
```

This verifies the new skill directories are discoverable by sync.py and would install cleanly alongside existing skills. It does not modify `~/.claude/`.

## Done when

1. `skills/spec-reconcile/SKILL.md` exists with valid YAML frontmatter and Phases 0-3 covering: preflight (spec resolution, states.json, Plane state check), context gathering (merge commit discovery, PR diff reading), reconciliation (scope/decisions/criteria/tests comparison), and report output with `RECONCILED: <yes|no> DRIFT: <n>` status line.
2. `skills/spec-retire/SKILL.md` exists with valid YAML frontmatter and Phases 0-4 covering: preflight (reconciliation report gate, states.json, `--partial` flag), analysis (Plane state gate, duplicate detection, wiki decomposition), user confirmation (compiled proposal presentation with halt), and execution (wiki writes, archive, log.md append, suggested commits).
3. `/spec-retire` distinguishes full-retire from partial-retire via Plane state group and `--partial` flag per Decision 4.
4. `/spec-retire` scans wiki `decisions/` and `comprehension/` for pre-existing entries by ticket ID and key-term grep before proposing new entries per Decision 6.
5. `/spec-retire` archives spec + companions from `TODO/` to `DONE/<TICKET-ID>/` using `git mv` for tracked files and `mv` + `git add` for untracked files per Decision 5.
6. `/spec-retire` appends to wiki `log.md` with the `retire` action tag per Decision 8, with idempotency check.
7. `/spec-retire` produces `state.md` update proposals with the evidence triple (Plane-ID, date, commit-hash, verification grep) per wiki convention, and skips the update (with warning) if evidence is incomplete.
8. `CLAUDE.md` documents the full spec lifecycle (spec-cycle -> ship-spec -> spec-reconcile -> spec-retire) in the workflow subsection and lists both skills in the file layout.
9. `python sync.py install --dry-run --verbose` discovers both new skill directories.

## Out of scope

- **Retiring legacy flat specs (manifest Section B).** ~65 pre-convention specs need a different flow without Plane linkage. Separate ticket.
- **Batch execution across all 22 specs.** VHS-8 builds the tools; the manifest's sequenced waves are separate invocations per spec.
- **Modifying `/ship-spec` or `/spec-cycle`.** The pipeline is additive — new skills, no changes to existing ones.
- **Wiki schema changes.** Both skills follow existing wiki conventions (`decisions/`, `comprehension/`, `log.md`, `state.md`). No new directory structures.
- **CAL-49 orphan handling.** The Plane 404 case needs manual investigation (manifest step 6).
- **Review-loop agents.** `/spec-reconcile` is single-pass, not multi-round. No subagent dispatch.
- **Non-spec docs triage (manifest Section E).** Different lifecycle, different tools.
- **Auto-commit.** Neither skill commits. The user controls commit timing across both repos.

## Deferred (P2+)

- **Reconciliation report format versioning** (conventions R1/F-5): Adding a `Format: reconciliation-v1` line is reasonable but not blocking for v1 delivery. Can add if the format changes.
- **`retire` action tag not in SCHEMA.md** (conventions R1/F-6): The tag is additive and follows the existing pattern. If wiki maintainers want it formalized, a SCHEMA.md update can follow.
- **`git mv --force` for retry safety** (edge-cases R1/F-5): If DONE/ has partial contents from an interrupted run, `git mv` may fail. Mitigated by `mkdir -p` idempotency; the skill can detect existing destination files and warn rather than blindly overwriting.
- **False-positive duplicate detection** (edge-cases R1/F-8): `grep -rl "<TICKET-ID>"` may match references sections. Accepted trade-off — false positives produce a warning the user can dismiss; false negatives (missing duplicates) are worse.
- **VHS-1 caching tension** (conventions R1/F-2): The brief explicitly says to use runtime `list_states`. `states.json` provides project_id and namespace lookups (static config); `list_states` provides group membership (could drift if states are reconfigured). Both are needed. No contradiction — they serve different purposes.
