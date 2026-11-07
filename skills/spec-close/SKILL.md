---
name: spec-close
description: Close a shipped spec in one pass — reconcile it against the shipped code, harvest wiki entries sized to the brief's tier, archive its artifacts from TODO/ to DONE/, and prepend a close entry to the wiki's log.md. Also archives tickets that have artifacts but no spec. Run after /spec-land.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: true
  services: [issue-tracker?, vcs-host?]
---

```
/spec-close <spec-path | TICKET-ID | docs/specs/TODO/<TICKET-ID>/> [--report-only | --partial]
```

`--report-only` and `--partial` together halt with `Usage: --report-only and --partial are mutually exclusive — pick one.`

Nothing changes before the Phase 4 confirmation except the reconciliation report.

## Phase 0 — Preflight

- **Resolve.** `project_root` is the repo root (the directory holding `docs/specs/`); run every command from it. Take the ticket id from the argument: the `.spec.md` stem, the `DONE/<ID>/` directory name, the `TODO/<ID>/` folder name, or the id itself. Uppercase it. `project_prefix` is the part before the first hyphen. The spec is `docs/specs/TODO/<ID>.spec.md`, else `docs/specs/DONE/<ID>/spec.md`.
  - A spec exists: the spec flow (Phases 1–5).
  - No spec, but a `docs/specs/TODO/<ID>.*` entry, a `docs/specs/TODO/<ID>/` folder, or an existing `docs/specs/DONE/<ID>/`: the archive-only close (Phase 2A).
  - Nothing found: halt with `nothing to close for <ID> under docs/specs/`.
- **Wiki.** Read `wiki_root` and `project_slug` from the project's `CLAUDE.md` or `AGENTS.md`. If a path with a username segment does not exist, retry it with the current user's name. A missing wiki is a warning; Phase 1 handles it.
- **Origin.** Run `timeout 30 git fetch origin`, then `git rev-list --count HEAD..origin/<branch>` (the default branch when the current one has no origin counterpart). When behind, print one line: `origin: local <branch> is <N> commits behind origin/<cmp> — reconciliation reads the working tree; never updated here.` Any git failure prints `origin: skipped (<reason>)`. Never update the tree.

Print one preflight line: ticket, flow (spec | archive-only), flags, wiki, origin.

## Phase 1 — Mode

Spec flow only. The archive-only close skips this phase whatever the ticket's state. First match wins:

1. `--report-only` → report only. No tracker read; the report's Plane line reads `not checked (--report-only)`.
2. `--partial`, or no tracker config → partial-close. No tracker config means the installed `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/ship-spec/states.json` is missing, unreadable, or has no `project_prefix` key.
3. The ticket's state group is `completed` or `cancelled`, and the wiki exists → full-close.
4. Anything else → print why, then the partial-or-abort prompt: `1. Partial-close  2. Abort`. This covers another group, a read with no group, Plane unreachable or ticket not found, and a missing wiki for a full close.

Read the ticket with the issue tracker's retrieve-by-identifier capability (e.g., `mcp__claude_ai_Plane__workitem` with `action: retrieve_by_identifier`, `workitem_identifier: "<TICKET-ID>"`, `fields: "name,state,completed_at"` and `expand: "state"` in Claude Code, or the equivalent in your host; load the tool first if your host defers tool schemas). `state.group` is the gate. A failed read prints `ticket: could not read <TICKET-ID> from the issue tracker (<error>). Usually a login problem: re-authenticate the tracker connection.` and takes rule 4.

Never gate on `completed_at`: some states that are not done still set it. It is only a ship-date source.

Partial-close skips Phases 2 and 3. With no wiki it archives only and prints `wiki not found — skipping log.md entry; archive only`.

## Phase 2 — Reconcile (full-close and report-only)

- **Merge.** In `<wiki_root>/log.md`, find the headings that contain `merge | <PREFIX> — <TICKET-ID> PR #`. spec-land writes one per landed PR. The PR number follows `PR #` up to the `:`. The SHA is that entry's `Landed: <sha>` body line; an entry without one gives only its PR number. Several entries: read each and combine them. With no wiki or no entry, run `git log --all --oneline -i -E --grep="<TICKET-ID>([^0-9]|$)" -- .` (the suffix keeps `VHS-1` off `VHS-11`). Nothing found: ask `Could not find merge commit for <TICKET-ID>. Enter PR number or commit SHA:`.
- **Diff.** For each SHA, read the first-parent diff: `git diff --stat <SHA>^1 <SHA>`, then `git diff <SHA>^1 <SHA>`. That is the change for a squash commit and for a two-parent merge commit, where `git show` prints no diff. If `<SHA>^1` does not resolve, the clone lacks the commit: say so and ask the operator to fetch. With only a PR number, run `gh pr view <N> --json files,additions,deletions` and `gh pr diff <N>`. If `gh` is absent or either command fails, stop and ask for the merge SHA. Over 500 diff lines: summarize by file, and read the paths the spec's decisions name.
- **Brief.** `<ID>.brief.md` beside a TODO spec, `brief.md` beside a DONE spec. Its acceptance criteria are reconciliation targets. Its `## Tier` `**Level:**` line drives Phase 3.
- **Walk.** Read the code; do not infer.
  - Scope: each spec file in the diff, dropped, or unexpected.
  - Decisions: Confirmed, Drifted, or Unverifiable.
  - Done-when criteria: Met, Unmet, or Unverifiable, each with evidence.
  - Test plan: does each test exist?
- **Report.** Write `<ID>.reconciliation.md` beside the spec (`reconciliation.md` beside a DONE spec). Overwrite an old one.

```markdown
# Reconciliation Report: <TICKET-ID>

> Date: YYYY-MM-DD
> Spec: <spec path>
> Merge: <PR number(s) and SHA(s)>
> Plane state: <state_name> (group: <group>)

## Summary
<1-2 sentences.>

## Scope
| Spec file | In diff? | Notes |
|---|---|---|

Unexpected files in diff (not in spec):
- `path` — <what it does>

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|

## Test Plan
| Test | Exists? | Location |
|---|---|---|

## Wiki-ready
<one line per entry worth writing, or `none`>

RECONCILED: <yes|no> DRIFT: <n>
```

`RECONCILED: yes` needs zero Unmet. `DRIFT` counts Drifted + Dropped + Unexpected. Report-only ends here: print the report path and `Re-run /spec-close <spec-path> without --report-only to complete the close.` On `RECONCILED: no`, ask `Spec has unmet acceptance criteria. Continue anyway? [y/N]` and halt on N.

## Phase 2A — Archive-only close

For a ticket with artifacts but no spec. There is no reconciliation, no harvest and no mode-gate read. `--report-only` stops with `nothing to reconcile: <ID> has no spec`. `--partial` is accepted and changes nothing.

Phase 4 shows the archive plan and the log entry. Phase 5 runs the archive and the log write. The log heading is `## [<date>] close | <PREFIX> — <ID>: <title> (archive only, no spec)`. `<title>` is the brief's `# ` heading when a brief exists. Otherwise it is the ticket name from a tracker read when one succeeds, else `<ID> artifacts`. The body is one sentence naming what was archived.

A ticket already in `DONE/<ID>/`, with nothing left in `TODO/`, only gets the log line; the guard keeps it to one. With no wiki, it archives only and prints the skipped-log notice.

## Phase 3 — Harvest (full-close only)

- **Duplicates.** Run `grep -rlw "<TICKET-ID>"` over `decisions/`, `comprehension/` and `projects/<slug>/state.md`, and show the hits. Do not propose a kind of entry the wiki already has for this ticket unless the operator asks. A state.md hit counts only when it sits under What's Shipped; a hit under What's Active or What's Next is the entry to move to What's Shipped. spec-close never edits the filemap; spec-land owns it.
- **Weight.** Brief tier `small`: a state.md entry and the log line only. Any other tier, or no tier:
  - a decision page only when the spec chose between real options;
  - a comprehension page only for a new module, data flow or integration.

  Follow the wiki's SCHEMA.md templates.
- **state.md.** A What's Shipped entry has three parts:
  - the evidence-triple heading `(<ID>, <ship-date>, commit <sha>)`;
  - the `Verification: <file>:<line> -- '<excerpt>'` line, taken from the report;
  - 1–2 sentences and links.

  The ship date is `completed_at`, else the merge commit's date, else today with a warning. With incomplete evidence, skip the state.md edit and say so. Replace the `> Last updated:` line with one line, `> Last updated: <today> (<ID> <short note>)`. Never keep or extend a `Prior:` chain.

## Phase 4 — Confirm

One checkpoint covers every change after the report. Run the archive block (Phase 5) with `--dry-run` added after the ticket id, and paste its output, or its `archive NOT run` line, into the plan verbatim:

```text
=== CLOSE PLAN: <TICKET-ID> ===
Mode: <full-close | partial-close | archive-only>
Reconciliation: <RECONCILED: yes|no, DRIFT: n | skipped>
Wiki: <available | not found — log.md entry omitted>

Wiki entries to create:
  1. decisions/YYYY-MM-DD-<slug>.md — "<title>"
     <3-line preview>

State.md update:
  File: projects/<project>/state.md
  <What's Shipped entry and the new Last updated line>

Archive (dry run):
  <archive_spec.py --dry-run output>

Log.md entry (prepended):
  ## [<date>] close | <PREFIX> — <TICKET-ID>: <title>
  <body>

Proceed? [y/N]
```

On `N`, stop: nothing changes after the report.

## Phase 5 — Execute

1. **Wiki** (full-close only). Write the approved pages, then the state.md edit.
2. **Archive.** Run this block and show its output:

   ```bash
   ARCHIVE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-close/scripts/archive_spec.py"
   command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
   cd "<project_root>"
   if test -f "$ARCHIVE"; then "$PY" "$ARCHIVE" <TICKET-ID> < /dev/null; else echo "archive NOT run: archive_spec.py not found at $ARCHIVE — install with 'python sync.py install'"; fi
   ```

   The script moves `TODO/<ID>.*` to `DONE/<ID>/` with the prefix stripped, then the children of a `TODO/<ID>/` folder. It skips sources already gone and never moves onto an existing path. It stages tracked moves, and untracked ones only when git does not ignore the destination. It prints one `staged:` line per staged path, `staged: none`, or `nothing to archive` (nothing new staged). Exit 0 is all done, and 1 is some item skipped or failed. Exit 2 is a usage error.

   On exit 0, continue. On any other exit, or `archive NOT run`, the archive is incomplete: skip the log write, report `Archive: incomplete` with the script's problem lines, and tell the operator to clear each one and re-run `/spec-close <TICKET-ID>`. To clear a `destination exists` line, move or remove the existing path. To clear `moved, NOT staged`, run `git add` on that path. The re-run archives what is left and writes the log line.
3. **Log** (skipped when there is no wiki). Prepend the entry with `prepend_log_entry.py`; it places the entry above the newest dated one, checks the guard, and writes atomically.
   - Spec-flow heading: `## [<date>] close | <PREFIX> — <TICKET-ID>: <spec title> (archived from TODO/)`, with a 1–2 sentence body.
   - Guard: `close | <PREFIX> — <TICKET-ID>:`. The `close |` keeps it apart from spec-land's merge lines. The colon keeps `VHS-1` from matching `VHS-11`.
   - `<date>` is today in UTC, or the newest date already heading `log.md` when that is later; the script refuses an entry older than the newest one.

   ```bash
   SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-close/scripts/prepend_log_entry.py"
   LOGPATH="<wiki_root>/log.md"
   command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
   if test -f "$SCRIPT"; then
   if "$PY" "$SCRIPT" "$LOGPATH" --guard 'close | <PREFIX> — <TICKET-ID>:' <<'PREPEND_LOG_ENTRY_EOF'
   ## [<date>] close | <PREFIX> — <TICKET-ID>: <title>

   <body>
   PREPEND_LOG_ENTRY_EOF
   then rc=0; else rc=$?; fi
   echo "prepend_log_entry_exit=$rc"
   else echo "log.md NOT written: prepend_log_entry.py not found at $SCRIPT — install with 'python sync.py install'"; fi
   ```

   Single-quote the guard. Double-quote both paths. Keep the `PREPEND_LOG_ENTRY_EOF` delimiter. Branch on the echoed integer, not on the harness's pass or fail:

   | Exit | Report |
   |---|---|
   | 0 | `Prepended: log.md` on `prepend_log_entry_outcome=prepended`; on `=fresh` or `=created`, the script's stderr notice verbatim |
   | 1 | `log.md: entry already present — skipped` |
   | other | `log.md NOT written: <stderr>` |

   A failed log write never stops the close. To recover, re-run `/spec-close <TICKET-ID>`.
4. **Never commit.**

```text
=== CLOSE COMPLETE: <TICKET-ID> ===

Target repo (<project_root>):
  Reconciliation: docs/specs/DONE/<TICKET-ID>/reconciliation.md
  Archived: TODO/<TICKET-ID>.* → DONE/<TICKET-ID>/
  Staged: <each path from the script's staged: lines>
  Status: uncommitted — review with `git diff --stat` then commit.

Wiki (<wiki_root>):
  Created: decisions/YYYY-MM-DD-<slug>.md
  Updated: projects/<project>/state.md
  <the log.md report line>
  Status: uncommitted.

Suggested commits:
  (in target repo)  git commit -m "close(<ticket-lower>): archive spec to DONE/"
  (in wiki)         git add <each wiki file this run wrote> && git commit -m "close(<ticket-lower>): wiki harvest from <TICKET-ID>"
```

The archive paths are already staged, so the target-repo suggestion is a plain `git commit` with no `git add` and no pathspec. Print it only when the script printed at least one `staged: <path>` line. On `staged: none` or `nothing to archive`, drop that line and print `Nothing was staged in the target repo by this run.` Name in the wiki suggestion only the files this run wrote; `log.md` only when the script wrote it. Never `git add docs/specs/` or `git add -A`. Omit the reconciliation line when no report exists.

## Re-runs

- **Interrupted execute.** Re-run with the DONE path or the ticket id. The archive script skips what already moved, and the guard skips the log line.
- **Partial, then full.** The later full close's guard matches the partial's `close |` line, so there is no second log line, by design.
- Keep the em dash in the guard: a tool that turns it into `-` breaks the match.

## Tool-use notes

- File read and write: the report, the wiki pages, and the state.md edit. `log.md` changes only through `prepend_log_entry.py`.
- Shell with git; `archive_spec.py` and `prepend_log_entry.py` run through the resolved interpreter.
- `gh`, optional (`vcs-host?`): only for a PR-number-only diff.
- The issue tracker's ticket read (`issue-tracker?`).
- Never commit, push, or open a PR.
