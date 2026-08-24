# Fed board snapshot schema

`read_board.py` accepts a board snapshot in any of three shapes. You produce the canonical
one on a machine that has Hermes:

```console
hermes kanban list --json --archived > board.json
```

Then read it anywhere:

```console
python scripts/read_board.py ./board.json --as <profile>
```

## Accepted shapes

The reader auto-detects which of these it was given:

1. **Top-level array** (what `hermes kanban list --json` emits):
   ```json
   [ { "id": "t_aaa", "title": "...", "assignee": "gibson", "status": "ready" } ]
   ```
2. **Object with a `tasks` array**:
   ```json
   { "tasks": [ { "id": "t_aaa", "...": "..." } ] }
   ```
3. **Dashboard `/board` shape** - what `GET /api/plugins/kanban/board` returns: `columns`
   is a **list** of `{name, tasks}` objects (the wrapper keys `tenants`, `assignees`,
   `latest_event_id`, `now` are ignored):
   ```json
   { "columns": [ { "name": "todo", "tasks": [ { "id": "t_aaa" } ] },
                  { "name": "running", "tasks": [] } ] }
   ```
   A status-keyed dict (`{ "columns": { "todo": [ ... ] } }`) is also accepted for
   convenience.

Any task object missing an `id` is skipped (with a note on stderr).

## Fields the reader uses

Only these fields drive the ownership lens and collision check. Extra fields are ignored,
so a partial snapshot is fine as long as these are present where they apply.

| Field            | Meaning                                                             |
|------------------|---------------------------------------------------------------------|
| `id`             | Task id (required). Short hex like `t_9f2a`.                         |
| `title`          | Display title.                                                      |
| `assignee`       | Owning Hermes profile, or `null`/absent when unclaimed.             |
| `status`         | Column: `triage`, `todo`, `scheduled`, `ready`, `running`, `blocked`, `review`, `done`, `archived`. |
| `priority`       | Integer tiebreaker (higher first).                                  |
| `tenant`         | Optional namespace.                                                 |
| `branch_name`    | Git branch, if any. Drives collision detection.                     |
| `workspace_path` | Working dir, if any. Drives collision detection.                    |
| `created_at` / `started_at` / `completed_at` | Unix timestamps (informational).        |

## Ownership lanes

The reader derives a lane per task from `assignee` + `status` against your `--as` identity:

- `MINE` - `assignee` equals your identity.
- `OTHERS` - `assignee` set and not you (do not touch the `running` ones).
- `UNCLAIMED` - no `assignee` and status is `triage` / `todo` / `ready` (free to claim).
- `UNOWNED` - no `assignee` but status is active and not claimable (`scheduled` / `running` /
  `review`, or unknown). Anomalous; not advertised as free.
- `BLOCKED` - status `blocked`.
- `DONE` - status `done` or `archived`.

A **collision** is two or more non-finished tasks that share a `branch_name` or
`workspace_path` across different owners.

## Minimal example

```json
[
  { "id": "t_aaa", "title": "Wire OAuth refresh", "assignee": null, "status": "todo" },
  { "id": "t_bbb", "title": "Draft release notes", "assignee": "gibson", "status": "ready" },
  { "id": "t_ccc", "title": "Rebuild search index", "assignee": "serenade-worker",
    "status": "running", "branch_name": "feat/search" }
]
```

Read with `--as gibson`, this yields: `t_bbb` MINE, `t_aaa` UNCLAIMED (free to claim),
`t_ccc` OTHERS (do not touch, it is running).
