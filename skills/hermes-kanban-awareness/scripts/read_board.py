#!/usr/bin/env python3
"""read_board.py - read the Hermes collaboration kanban and classify ownership.

Source resolution is live-first, in this order:

  1. ``hermes kanban list --json``   (CLI on PATH; reads the local DB itself)
  2. read-only SQLite at the Hermes board DB the CLI would read
  3. a fed JSON snapshot (positional path, ``--fed FILE``, or ``-`` for stdin)

A fed snapshot, when given explicitly, always wins (it is how you coordinate
against a board that lives on another machine). Otherwise the script prefers the
CLI and falls back to SQLite, so it keeps working when ``hermes`` is not on PATH.

Output is a human ownership digest (default) or machine JSON (``--json``),
grouping the board by status column and tagging each task against an identity:

  MINE       assignee == identity
  OTHERS     assignee set and != identity   (do not touch the running ones)
  UNCLAIMED  no assignee and status in {triage, todo, ready}   (free to claim)
  UNOWNED    no assignee but status is active and not claimable (scheduled /
             running / review / unknown) - anomalous, NOT advertised as free
  BLOCKED    status == blocked
  DONE       status in {done, archived}

Stdlib only. Read-only: this script never mutates the board. All writes
(claim/assign/comment/complete/block) go through the ``hermes kanban`` CLI,
driven from the SKILL.md steps.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

# Mirror plugin_api.BOARD_COLUMNS (+ archived). Order is the display order.
COLUMNS = ["triage", "todo", "scheduled", "ready", "running", "blocked", "review", "done"]
ARCHIVED = "archived"
CLAIMABLE_STATUSES = {"triage", "todo", "ready"}
TERMINAL_STATUSES = {"done", "archived"}

# Fields we normalize across all three sources. SQLite older than these columns'
# migrations is handled by selecting only the columns that actually exist.
FIELDS = [
    "id", "title", "assignee", "status", "priority", "tenant",
    "workspace_path", "branch_name", "created_by", "created_at",
    "started_at", "completed_at", "session_id",
]

LANE_TO_LENS = {
    "MINE": "mine", "OTHERS": "others", "UNCLAIMED": "unclaimed",
    "UNOWNED": "unowned", "BLOCKED": "blocked", "DONE": "done",
}


def _status(task: dict) -> str:
    """Status as a lowercase string. Fed JSON is untyped, so coerce defensively
    (a non-string status must not crash the whole digest)."""
    return str(task.get("status") or "").lower()


def resolve_identity(args: argparse.Namespace) -> str | None:
    """Who is this session on the board? --as wins, else the same env vars the
    Hermes CLI's own _profile_author() reads, else observer (no task is mine)."""
    if args.identity:
        return args.identity
    for env in ("HERMES_PROFILE_NAME", "HERMES_PROFILE"):
        val = os.environ.get(env)
        if val:
            return val
    return None


# --------------------------------------------------------------------------
# Board location (faithful to hermes_constants.get_default_hermes_root +
# kanban_db.kanban_db_path so the SQLite fallback reads the SAME DB the CLI does)
# --------------------------------------------------------------------------

def _native_default_home() -> Path:
    """Platform-native Hermes home: %LOCALAPPDATA%\\hermes on Windows, ~/.hermes
    on POSIX. Mirrors hermes_constants._get_platform_default_hermes_home."""
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA", "").strip()
        base = Path(local) if local else Path.home() / "AppData" / "Local"
        return base / "hermes"
    return Path.home() / ".hermes"


def resolve_home(args: argparse.Namespace) -> Path:
    """The kanban umbrella root <root>. HERMES_KANBAN_HOME pins it directly;
    otherwise mirror get_default_hermes_root: a HERMES_HOME of
    ``<root>/profiles/<name>`` resolves back to ``<root>`` (profiles share one
    board), and an unset HERMES_HOME falls to the platform-native default."""
    if args.home:
        return Path(args.home).expanduser()
    pinned = os.environ.get("HERMES_KANBAN_HOME")
    if pinned:
        return Path(pinned).expanduser()
    native = _native_default_home()
    env = os.environ.get("HERMES_HOME")
    if not env:
        return native
    env_path = Path(env).expanduser()
    # Under the native default (standard install or ~/.hermes/profiles/<name>):
    # the root is the native home, never the per-profile dir.
    try:
        env_path.relative_to(native)
        return native
    except ValueError:
        pass
    # Custom HERMES_HOME outside the native tree (Docker etc.). Strip a
    # trailing profiles/<name> if present; otherwise HERMES_HOME is the root.
    if env_path.parent.name == "profiles":
        return env_path.parent.parent
    return env_path


def _board_db(home: Path, slug: str | None) -> Path:
    """Default board is the shared kanban.db; named boards nest under boards/."""
    if not slug or slug == "default":
        return home / "kanban.db"
    return home / "kanban" / "boards" / slug / "kanban.db"


def resolve_db(home: Path, board: str | None) -> Path:
    """Resolve the DB file the way Hermes' kanban_db_path does.

    Order: HERMES_KANBAN_DB (direct file pin, wins over everything, as the
    dispatcher injects it into workers) -> explicit --board flag ->
    HERMES_KANBAN_BOARD env slug -> the on-disk ``<root>/kanban/current``
    pointer (only if that board actually exists, else the default) -> the
    default shared board.
    """
    direct = os.environ.get("HERMES_KANBAN_DB")
    if direct:
        return Path(direct).expanduser()
    if board:
        return _board_db(home, board)
    slug = os.environ.get("HERMES_KANBAN_BOARD")
    if not slug:
        pointer = home / "kanban" / "current"
        if pointer.exists():
            try:
                slug = pointer.read_text(encoding="utf-8").strip() or None
            except OSError:
                slug = None
        # A stale pointer to a deleted board: Hermes falls back to default,
        # so do the same rather than resolving a path that does not exist.
        if slug and not _board_db(home, slug).exists():
            slug = None
    return _board_db(home, slug)


# --------------------------------------------------------------------------
# Source readers
# --------------------------------------------------------------------------

def read_cli(args: argparse.Namespace) -> list[dict] | None:
    """Try the hermes CLI. Return task dicts, or None to fall through."""
    if args.no_cli:
        return None
    hermes = shutil.which(args.hermes_bin)
    if not hermes:
        return None
    cmd = [hermes, "kanban"]
    if args.board:
        cmd += ["--board", args.board]
    cmd += ["list", "--json"]
    if args.archived:
        cmd += ["--archived"]
    if args.assignee:
        cmd += ["--assignee", args.assignee]
    if args.status:
        cmd += ["--status", args.status]
    try:
        # Capture bytes, not text: the CLI emits UTF-8 and Windows' locale
        # decoder (cp1252) chokes on it, which would silently null stdout.
        proc = subprocess.run(cmd, capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"note: hermes CLI failed ({exc}); falling back to SQLite", file=sys.stderr)
        return None
    out = (proc.stdout or b"").decode("utf-8", "replace")
    err = (proc.stderr or b"").decode("utf-8", "replace")
    if proc.returncode != 0:
        msg = err.strip().splitlines()[-1:] or [""]
        print(f"note: hermes CLI exited {proc.returncode} ({msg[0]}); "
              "falling back to SQLite", file=sys.stderr)
        return None
    try:
        return normalize(json.loads(out))
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"note: hermes CLI output not JSON ({exc}); falling back to SQLite",
              file=sys.stderr)
        return None


def read_sqlite(args: argparse.Namespace) -> list[dict]:
    home = resolve_home(args)
    db = resolve_db(home, args.board)
    args._resolved_db = str(db)  # surfaced in the header/JSON for transparency
    if not db.exists():
        raise SystemExit(
            f"error: no kanban DB at {db}. The Hermes board is not on this "
            "machine.\nHand me a snapshot instead: produce it on the Hermes box "
            "with `hermes kanban list --json > board.json`, then run with "
            "`--fed board.json` (or pipe it on stdin)."
        )
    uri = f"file:{db.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        conn.row_factory = sqlite3.Row
        # Select only columns that exist: older boards predate some migrations
        # (branch_name, session_id, ...) and we open read-only without migrating.
        present = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
        if not present:
            raise SystemExit(
                f"error: {db} has no 'tasks' table (not a kanban DB, or empty/"
                "corrupt). Use `--fed <snapshot.json>` instead."
            )
        cols = [c for c in FIELDS if c in present]
        sql = f"SELECT {', '.join(cols)} FROM tasks"
        where: list[str] = []
        params: list = []
        if not args.archived and (args.status or "").lower() != ARCHIVED:
            where.append("status != ?")
            params.append(ARCHIVED)
        if args.assignee:
            where.append("assignee = ?")
            params.append(args.assignee)
        if args.status:
            where.append("status = ?")
            params.append(args.status.lower())
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY priority DESC, created_at ASC"
        rows = []
        for row in conn.execute(sql, params):
            d = dict(row)
            for c in FIELDS:  # fill any columns the old schema lacked
                d.setdefault(c, None)
            rows.append(d)
        return rows
    except sqlite3.OperationalError as exc:
        raise SystemExit(
            f"error: could not read kanban DB at {db}: {exc}\n"
            "It may be an incompatible schema or locked by a writer. "
            "Use `--fed <snapshot.json>` instead."
        )
    finally:
        conn.close()


def read_fed(source: str) -> list[dict]:
    if source == "-":
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
    else:
        path = Path(source).expanduser()
        if not path.exists():
            raise SystemExit(f"error: fed snapshot not found: {path}")
        raw = path.read_text(encoding="utf-8")
    try:
        return normalize(json.loads(raw))
    except (json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"error: fed snapshot is not valid board JSON: {exc}")


def normalize(payload) -> list[dict]:
    """Accept a top-level array, {tasks:[...]}, or the dashboard /board shape
    where ``columns`` is either a list of {name, tasks} objects (what the real
    REST route returns) or a dict of status -> task list."""
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict) and isinstance(payload.get("tasks"), list):
        rows = payload["tasks"]
    elif isinstance(payload, dict) and isinstance(payload.get("columns"), list):
        rows = [t for col in payload["columns"] if isinstance(col, dict)
                for t in (col.get("tasks") or [])]
    elif isinstance(payload, dict) and isinstance(payload.get("columns"), dict):
        rows = [t for col in payload["columns"].values() if isinstance(col, list) for t in col]
    else:
        raise ValueError("expected a JSON array, {tasks:[...]}, or {columns:...}")
    out = []
    skipped = 0
    for r in rows:
        if not isinstance(r, dict) or not r.get("id"):
            skipped += 1
            continue
        out.append({k: r.get(k) for k in FIELDS})
    if skipped:
        plural = "y" if skipped == 1 else "ies"
        print(f"note: skipped {skipped} malformed task entr{plural} "
              "(not an object, or missing id)", file=sys.stderr)
    return out


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------

def classify(task: dict, identity: str | None) -> str:
    status = _status(task)
    assignee = task.get("assignee")
    if status in TERMINAL_STATUSES:
        return "DONE"
    if status == "blocked":
        return "BLOCKED"
    if assignee:
        return "MINE" if identity and assignee == identity else "OTHERS"
    if status in CLAIMABLE_STATUSES:
        return "UNCLAIMED"
    # Unassigned but in an active, non-claimable column (scheduled/running/
    # review/unknown). Anomalous - do NOT advertise as free to claim.
    return "UNOWNED"


def find_collisions(tasks: list[dict]) -> list[dict]:
    """Non-terminal tasks that share a branch or workspace. Any shared
    branch/workspace among >1 live task is a contention signal, including two
    unassigned tasks on the same branch (both claimable -> same work)."""
    collisions = []
    for field, label in (("branch_name", "branch"), ("workspace_path", "workspace")):
        groups: dict[str, list[dict]] = {}
        for t in tasks:
            if _status(t) in TERMINAL_STATUSES:
                continue
            key = t.get(field)
            if key:
                groups.setdefault(str(key), []).append(t)
        for key, group in groups.items():
            if len(group) > 1:
                collisions.append({
                    "key": f"{label}:{key}",
                    "tasks": [{"id": t.get("id"), "assignee": t.get("assignee")} for t in group],
                })
    return collisions


def build_result(tasks: list[dict], identity: str | None, source: str,
                 board: str | None, source_detail: str | None = None) -> dict:
    columns: dict[str, list[dict]] = {}
    lens: dict[str, list[str]] = {v: [] for v in LANE_TO_LENS.values()}
    for t in tasks:
        lane = classify(t, identity)
        row = dict(t)
        row["lane"] = lane
        key = _status(t) or "unknown"
        columns.setdefault(key, []).append(row)
        lens[LANE_TO_LENS[lane]].append(t.get("id"))
    # Known columns first (canonical order), then archived, then any
    # present-but-unknown status so a counted task can never be hidden.
    order = list(COLUMNS)
    if ARCHIVED in columns:
        order.append(ARCHIVED)
    for key in columns:
        if key not in order:
            order.append(key)
    return {
        "source": source,
        "source_detail": source_detail,
        "board": board or "default",
        "identity": identity,
        "column_order": order,
        "columns": columns,
        "lens": lens,
        "counts": {k: len(v) for k, v in lens.items()},
        "collisions": find_collisions(tasks),
    }


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

LANE_TAG = {
    "MINE": "MINE",
    "OTHERS": "OTHERS - do not touch if running",
    "UNCLAIMED": "FREE to claim",
    "UNOWNED": "unowned (active, no assignee; not free to claim)",
    "BLOCKED": "blocked",
    "DONE": "done",
}


def _trim(text, width):
    text = str(text or "").replace("\n", " ").strip()
    return text if len(text) <= width else text[: width - 1] + "."


def render_digest(result: dict) -> str:
    ident = result["identity"] or "(observer: no task is yours; claim nothing as MINE)"
    src = result["source"]
    if result.get("source_detail"):
        src = f"{src}: {result['source_detail']}"
    lines = [
        f"Hermes kanban: board '{result['board']}'  (source: {src})  "
        f"identity: {ident}",
        "",
    ]
    columns = result["columns"]
    if not any(columns.values()):
        lines.append("(board is empty)")
        return "\n".join(lines)
    for col in result["column_order"]:
        rows = columns.get(col) or []
        if not rows:
            continue
        lines.append(f"{col.upper()}  ({len(rows)})")
        for t in rows:
            assignee = t.get("assignee") or "unassigned"
            lines.append(
                f"  {_trim(t.get('id'), 10):<10} {_trim(t.get('title'), 42):<42} "
                f"{_trim(assignee, 18):<18} {LANE_TAG[t['lane']]}"
            )
    c = result["counts"]
    summary = (f"Ownership: {c['mine']} mine, {c['others']} others, "
               f"{c['unclaimed']} unclaimed, {c['blocked']} blocked, {c['done']} done")
    if c["unowned"]:
        summary += f", {c['unowned']} unowned"
    lines += ["", summary]
    if result["collisions"]:
        lines.append("Collisions (same branch/workspace, live tasks):")
        for col in result["collisions"]:
            who = ", ".join(f"{t['id']}({t['assignee'] or 'unassigned'})" for t in col["tasks"])
            lines.append(f"  {col['key']}: {who}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def parse_args(argv) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Read the Hermes kanban and classify task ownership.")
    p.add_argument("fed", nargs="?", default=None,
                   help="Fed board snapshot: a JSON file path, or '-' for stdin. "
                        "When given, overrides the live board.")
    p.add_argument("--fed", dest="fed_flag", default=None,
                   help="Same as the positional fed argument (explicit form).")
    p.add_argument("--as", dest="identity", default=None,
                   help="This session's identity (Hermes profile) on the board.")
    p.add_argument("--mine", action="store_true",
                   help="Show only tasks owned by your identity (needs --as or env identity).")
    p.add_argument("--board", default=None, help="Board slug (omit for the current board).")
    p.add_argument("--assignee", default=None, help="Filter to one assignee.")
    p.add_argument("--status", default=None, help="Filter to one status column.")
    p.add_argument("--archived", action="store_true", help="Include archived tasks.")
    p.add_argument("--no-cli", action="store_true",
                   help="Skip the hermes CLI; read SQLite (or fed) directly.")
    p.add_argument("--home", default=None,
                   help="Override the Hermes umbrella root (else $HERMES_HOME / platform default).")
    p.add_argument("--hermes-bin", default="hermes", help="hermes executable name.")
    p.add_argument("--json", dest="as_json", action="store_true",
                   help="Emit machine JSON instead of the human digest.")
    return p.parse_args(argv)


def main(argv=None) -> int:
    # Board content is UTF-8; force UTF-8 output so a Windows cp1252 console
    # cannot raise UnicodeEncodeError on a task title.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    args = parse_args(argv if argv is not None else sys.argv[1:])
    args._resolved_db = None
    fed_source = args.fed_flag or args.fed
    identity = resolve_identity(args)
    if args.mine and not identity:
        raise SystemExit("error: --mine needs an identity; pass --as <profile> "
                         "(or set $HERMES_PROFILE).")

    if fed_source:
        tasks, source = read_fed(fed_source), "fed"
        source_detail = None if fed_source == "-" else fed_source
    else:
        tasks = read_cli(args)
        if tasks is not None:
            source, source_detail = "cli", None
        else:
            tasks, source = read_sqlite(args), "sqlite"
            source_detail = args._resolved_db

    # Post-hoc filters. The archived exclusion must yield to an explicit
    # --status archived (or --archived), else that query returns a false empty.
    if not args.archived and (args.status or "").lower() != ARCHIVED:
        tasks = [t for t in tasks if _status(t) != ARCHIVED]
    if args.assignee:
        tasks = [t for t in tasks if t.get("assignee") == args.assignee]
    if args.status:
        tasks = [t for t in tasks if _status(t) == args.status.lower()]
    if args.mine:
        tasks = [t for t in tasks if classify(t, identity) == "MINE"]

    result = build_result(tasks, identity, source, args.board, source_detail)
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_digest(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
