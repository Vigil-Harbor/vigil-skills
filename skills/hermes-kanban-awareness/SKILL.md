---
name: hermes-kanban-awareness
description: Make this session aware of the Hermes collaboration kanban so it does not
  overlap with other agents' owned tasks. Reads the live board (hermes kanban CLI, or
  the local SQLite DB) or a fed snapshot, reports ownership (mine / others / unclaimed /
  blocked) plus branch/workspace collisions, and drives claim, assign, comment, complete,
  and block. Use when working alongside Hermes agents that share a kanban board, or when
  handed a board JSON to coordinate against.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
---

# /hermes-kanban-awareness

Hermes runs a shared **kanban board** as its multi-agent coordination primitive: every
task carries an `assignee` (the owning Hermes profile) and a `status` column, so a fleet
of workers divides labour without colliding. A Claude Code session is not on that board by
default, so it can start work a Hermes worker already owns. This skill pulls the board in,
shows who owns what, and keeps this session in its lane. With the user's go-ahead it can
also act on the board (claim, comment, complete, block).

Read the board first, **act second**. Treat assigned tasks as taken.

## Input parsing

The argument is optional. Forms:

- `/hermes-kanban-awareness` -> live read of the current board.
- `/hermes-kanban-awareness ./board.json` -> read a fed snapshot file (overrides live).
- `/hermes-kanban-awareness --board <slug>` -> a specific named board.
- `/hermes-kanban-awareness --as <profile>` -> declare this session's identity on the board.
- `--mine`, `--status <col>`, `--assignee <profile>`, `--archived` -> narrow the view.

**Identity (who am I on the board?).** Ownership classification needs to know which
assignee is "me". Resolution order: the `--as <profile>` argument, then `$HERMES_PROFILE_NAME`
or `$HERMES_PROFILE` in the environment (the same vars the Hermes CLI's own `--mine` uses),
else **observer** mode (no task is "mine"; every assigned task is treated as someone else's,
and you claim nothing as yours). If the user has not said who they are and no env identity is
set, ask once, or proceed as observer and say so.

## Step 1 - Acquire the board

Run the bundled reader. It is live-first: it prefers `hermes kanban list --json`, falls
back to the local SQLite DB the CLI would read, and accepts a fed JSON snapshot. It never
writes to the board.

```console
python ${CLAUDE_SKILL_DIR}/scripts/read_board.py --as <profile>
```

Useful variants:

```console
# A specific board, including finished/archived cards
python ${CLAUDE_SKILL_DIR}/scripts/read_board.py --board <slug> --archived --as <profile>

# Machine JSON (columns + ownership lens + collisions) to reason over precisely
python ${CLAUDE_SKILL_DIR}/scripts/read_board.py --as <profile> --json

# Read a fed snapshot (a board exported elsewhere)
python ${CLAUDE_SKILL_DIR}/scripts/read_board.py ./board.json --as <profile>

# Force the offline path (skip the CLI, read SQLite directly)
python ${CLAUDE_SKILL_DIR}/scripts/read_board.py --no-cli --as <profile>
```

The digest header names the **source** (`cli`, `sqlite`, or `fed`) and, for the SQLite
path, the exact DB file it resolved, so a stale or wrong-board read is visible at a glance.

## Step 2 - Read the ownership lens

The reader tags every task into one lane. This is the "no overlap" map:

- **MINE** - `assignee` equals your identity. Yours to act on.
- **OTHERS** - `assignee` is set and is not you. Someone else's lane. If it is also
  `running`, treat it as actively held.
- **UNCLAIMED** - no assignee and status is `triage` / `todo` / `ready`. Free to claim.
- **UNOWNED** - no assignee but the status is active and not claimable (`scheduled` /
  `running` / `review`, or an unknown column). Anomalous (likely mid-handoff or orphaned).
  Do NOT treat as free; raise it with the user rather than grabbing it.
- **BLOCKED** - parked waiting on input. If it is yours, it may be your unblock to do.
- **DONE** - `done` or `archived`. History only.

It also reports **collisions**: non-finished tasks that share a `branch_name` or
`workspace_path` across different owners. A collision is a direct overlap warning, surface
it loudly.

## Step 3 - Stay-in-your-lane contract

Before doing work that maps to a task on the board:

- If the matching task is **OTHERS** and `running`, do not touch it. Tell the user it is
  owned by `<assignee>` and ask before proceeding.
- If it is **UNCLAIMED**, claim it first (Step 4) so siblings see it is taken, then work.
- If your planned files, branch, or workspace match a **collision** entry, stop and flag
  the conflict with the other owner's task id.
- If nothing on the board matches your work, say so. Awareness includes "this is not
  tracked here."

## Step 4 - Acting on the board (full write)

All writes go through the `hermes kanban` CLI against the local DB (no dashboard or token
needed). Use the same `--board <slug>` you read from if it was not the default.

```console
# Take durable ownership of a free task (records assignee so no sibling grabs it)
hermes kanban assign <task_id> <profile>

# Take a short execution lock (TTL) while actively working it
hermes kanban claim <task_id>

# Leave a progress note other agents and the user can see
hermes kanban comment <task_id> "Refactored auth; tests green on feat/auth"

# Mark finished with a result summary
hermes kanban complete <task_id> --result "Shipped in PR #142"

# Park it (also recorded as a comment)
hermes kanban block <task_id> "Waiting on API key from ops"

# Record a dependency (parent must clear before child is ready)
hermes kanban link <parent_id> <child_id>
```

**Guardrails.**
- Confirm with the user before `complete` or `block`, and before `assign`-ing a task that
  is currently someone else's.
- Never reassign or complete another agent's `running` task. If you must intervene,
  `comment` to coordinate and ask the user first.
- After a write, re-run Step 1 to confirm the board reflects it.

## Feeding the board

When the live Hermes install is not on this machine (a session on another box, or you were
simply handed the board), feed a snapshot.

**Consume a snapshot** the user provides:

```console
# From a file
python ${CLAUDE_SKILL_DIR}/scripts/read_board.py ./board.json --as <profile>
```

If the user pastes board JSON into the chat, save it to the session scratchpad and read
that file (saving the paste is why this skill declares `filesystem: [write]`), or pipe it
on stdin with `--fed -`. Accepted shapes are a top-level task array, `{"tasks": [...]}`, or
`{"columns": [...]}` (the dashboard `/board` shape, a list of `{name, tasks}` objects). See
`reference/board-schema.md` for the schema and a minimal example.

**Produce a snapshot** to hand to another machine or session:

```console
hermes kanban list --json --archived > board.json
```

Note: a fed snapshot is read-only context. The write verbs in Step 4 act on a live local
board, not on a fed file.

## Fallbacks and troubleshooting

- **`hermes` not on PATH** - the reader falls back to SQLite automatically. Force it with
  `--no-cli`. Override the Hermes home with `--home <dir>` or `$HERMES_HOME`.
- **No DB found** - the board is not on this machine. Switch to fed mode (produce a
  snapshot on the Hermes box, read it here).
- **Multiple boards** - list them with `hermes kanban boards list --json`; the reader honors
  the on-disk current-board pointer, so the SQLite fallback reads the same board the CLI
  would. Pass `--board <slug>` to target another.
- **Empty active board** - normal when all work is finished. Add `--archived` to see history.

## Tool-use notes

Non-operative reference for the surfaces this skill touches:

- `hermes kanban` CLI: `list`/`ls`, `show`, `boards list`, and the write verbs `assign`,
  `claim`, `comment`, `complete`, `block`, `link` (all read/write the local DB directly).
- SQLite (read-only) at the resolved Hermes board DB, e.g. `<root>/kanban.db` or
  `<root>/kanban/boards/<slug>/kanban.db`. `<root>` is `$HERMES_HOME` with any
  `profiles/<name>` suffix stripped (profiles share one board), else the platform default
  (`%LOCALAPPDATA%\hermes` on Windows, `~/.hermes` on POSIX). The bundled
  `scripts/read_board.py` resolves this the way Hermes does and is the only thing that opens it.
- Optional: the dashboard REST route `GET /api/plugins/kanban/board` on `:9119` exposes the
  same data but requires the dashboard session bearer token; this skill does not use it.
