#!/usr/bin/env python3
"""Scaffold a session handoff document.

Usage:
    create_handoff.py [slug] [--continues-from FILE] [--project-path PATH]

Writes `<project-path>/.claude/handoffs/YYYY-MM-DD-HHMMSS-<slug>.md`, pre-filled
with git metadata and a `[TODO: ...]` marker in every section the author must
write. Prints the resulting path. Stdlib only.

The section table, the marker text and the marker pattern all come from
`_sections.py` and are never restated here (VHS-28 D4).
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

GIT_TIMEOUT_SECONDS = 10
MAX_FILE_ROWS = 10
MAX_SLUG_CHARS = 60
MAX_PREVIOUS_TITLE_CHARS = 80
MAX_STEM_ATTEMPTS = 9

# Diagnostics, not author work: plain italic prose, deliberately *not* the
# marker shape. A git placeholder written as a `[TODO: ...]` would make every
# CREATE outside a repository permanently un-READY, with nothing to replace.
NOT_A_REPO = "_not a git repository_"
NO_COMMITS = "_no commits yet_"
GIT_UNAVAILABLE = "_git unavailable or timed out_"

# Titles for the rows `_sections` leaves anonymous. Nothing matches or
# validates these, so they are this script's own constants (D1/D4).
ANONYMOUS_CONTAINER_TITLES = (
    "Codebase Orientation",
    "Work Completed",
    "Context and Risks",
)


def _load_sections():
    """Load the shared section module by file path (D4).

    No `sys.path` mutation: sync.py mirrors these files into the operator's
    harness dir, where a module-level insert would run in their process.
    """
    path = Path(__file__).resolve().with_name("_sections.py")
    spec = importlib.util.spec_from_file_location("_session_handoff_sections", path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load _sections.py from {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["_session_handoff_sections"] = module
    spec.loader.exec_module(module)
    return module


S = _load_sections()


# --- Text safety -------------------------------------------------------------

def neutralize_todo(text: str) -> str:
    """Rewrite the opening bracket of any `[TODO...]`-shaped run as `&#91;`.

    A commit subject like `[TODO] wire up X` is a real convention, and left
    alone it would trip the whole-document marker scan on a fully written
    handoff - unclearable, because the author cannot edit generated content.

    The entity is load-bearing; a backslash escape does not work. Against a
    backslash-escaped run the marker pattern still matches from index 1, so it
    would render correctly and still trip the gate.
    """
    return S.TODO_MARKER_RE.sub(lambda m: "&#91;" + m.group(0)[1:], text)


def safe_inline(text: str) -> str:
    """Escape a value bound for prose or a bullet, then neutralize markers."""
    return neutralize_todo(text.replace("`", "\\`"))


def safe_cell(text: str) -> str:
    """Escape a value bound for a table cell, then neutralize markers."""
    return neutralize_todo(text.replace("|", "\\|").replace("`", "\\`"))


# --- Git metadata ------------------------------------------------------------

def _scrubbed_env() -> dict:
    """Every inherited GIT_* variable removed, so `cwd` alone decides the repo.

    Scrubbing only GIT_DIR/GIT_WORK_TREE is not enough: git resolves all of
    them ahead of discovery, and a hook exports the lot - with GIT_INDEX_FILE
    still set, `git status` reads the *other* repository's index.
    """
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def _run_git(args: list[str], cwd: Path) -> tuple[bool, str, str | None]:
    """Run one git command. Returns (ok, stdout, reason).

    reason is None on success, "unavailable" when git could not run or timed
    out (a timeout is treated exactly like a non-zero exit), "failed"
    otherwise.
    """
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            env=_scrubbed_env(),
            capture_output=True,
            timeout=GIT_TIMEOUT_SECONDS,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.SubprocessError):
        return (False, "", "unavailable")
    if proc.returncode != 0:
        return (False, proc.stdout or "", "failed")
    return (True, proc.stdout or "", None)


def _parse_porcelain_z(payload: str) -> list[tuple[str, str]]:
    """Parse `git status --porcelain -z` into (status, path) rows.

    Rename/copy records carry a second NUL-separated source path; it is
    consumed so it never renders as a row of its own.
    """
    fields = payload.split("\0")
    rows: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        record = fields[index]
        index += 1
        if len(record) < 4:
            continue
        status = record[:2]
        path = record[3:]
        if "R" in status or "C" in status:
            index += 1  # the source path of a rename/copy
        rows.append((status.strip() or "??", path))
    return rows


def _render_file_table(rows: list[tuple[str, str]]) -> str:
    if not rows:
        return "_no modified or staged files_"
    lines = ["| Status | File |", "|--------|------|"]
    for status, path in rows[:MAX_FILE_ROWS]:
        lines.append("| {} | {} |".format(safe_cell(status), safe_cell(path)))
    if len(rows) > MAX_FILE_ROWS:
        lines.append("")
        lines.append("… and {} more".format(len(rows) - MAX_FILE_ROWS))
    return "\n".join(lines)


def collect_git_metadata(project_path: Path) -> dict:
    """Branch, last 5 commits and modified+staged files, or a stated failure."""
    ok, _, reason = _run_git(["rev-parse", "--is-inside-work-tree"], project_path)
    if not ok:
        placeholder = GIT_UNAVAILABLE if reason == "unavailable" else NOT_A_REPO
        return {"branch": placeholder, "commits": placeholder, "files": placeholder}

    ok, out, reason = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], project_path)
    if ok and out.strip():
        branch = safe_inline(out.strip())
    elif reason == "unavailable":
        branch = GIT_UNAVAILABLE
    else:
        branch = NO_COMMITS

    ok, out, reason = _run_git(["log", "-5", "--format=%h %s"], project_path)
    if ok and out.strip():
        commits = "\n".join(
            "- " + safe_inline(line.strip())
            for line in out.splitlines() if line.strip()
        )
    elif reason == "unavailable":
        commits = GIT_UNAVAILABLE
    else:
        commits = NO_COMMITS

    ok, out, reason = _run_git(
        ["-c", "core.quotepath=false", "status", "--porcelain", "-z"], project_path
    )
    if not ok:
        files = GIT_UNAVAILABLE if reason == "unavailable" else NO_COMMITS
    else:
        files = _render_file_table(_parse_porcelain_z(out))

    return {"branch": branch, "commits": commits, "files": files}


# --- Slug / paths ------------------------------------------------------------

def sanitize_slug(raw: str) -> str:
    """Sanitize to [a-z0-9-], collapse runs, strip edges, cap at 60 characters,
    and only *then* default to `handoff` if what is left is empty."""
    text = re.sub(r"[^a-z0-9-]+", "-", (raw or "").strip().lower())
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:MAX_SLUG_CHARS].strip("-") or "handoff"


def _same_path(left: Path, right: Path) -> bool:
    if os.name == "nt":
        return os.path.normcase(str(left)) == os.path.normcase(str(right))
    return str(left) == str(right)


def resolve_predecessor(argument: str, handoffs_dir: Path) -> tuple[Path | None, str]:
    """Resolve --continues-from against the handoffs directory.

    Returns (path, "") on success, or (None, message). A path that escapes the
    directory, or names a file that does not exist, is a hard error - checked
    before any name is claimed, so "no document written" holds.
    """
    base = handoffs_dir.resolve()
    raw = Path(argument).expanduser()
    candidate = (raw if raw.is_absolute() else base / raw).resolve()
    if not _same_path(candidate.parent, base):
        return (None, "--continues-from must name a file in {}; got {}".format(
            base, candidate))
    if not candidate.is_file():
        return (None, "--continues-from names a file that does not exist: {}".format(
            candidate))
    return (candidate, "")


def chain_lines(predecessor: Path | None) -> list[str]:
    """The pinned two-line chain block, or the fresh-start line."""
    if predecessor is None:
        return ["- **Continues from**: None (fresh start)"]
    filename = predecessor.name
    try:
        title = S.first_heading_title(S.normalize(predecessor.read_bytes()))
    except OSError:
        title = None
    if title is None:
        shown = filename
    else:
        # Truncate first (ellipsis included), escape after: escaping first can
        # cut an escape pair at the boundary, and the escaped form may exceed
        # 80 because the 80 bounds the title, not the rendered line.
        if len(title) > MAX_PREVIOUS_TITLE_CHARS:
            title = title[: MAX_PREVIOUS_TITLE_CHARS - 1] + "…"
        shown = safe_inline(title)
    return [
        "- **Continues from**: [{0}](./{0})".format(filename),
        "  - Previous title: {}".format(shown),
    ]


# --- Rendering ---------------------------------------------------------------

def render_document(slug: str, meta: dict, chain: list[str], created: str,
                    project_path: Path) -> str:
    """Render the whole document by walking TEMPLATE_SECTIONS in order."""
    anonymous = iter(ANONYMOUS_CONTAINER_TITLES)
    metadata_block = "\n".join([
        "- **Created**: {}".format(created),
        "- **Project**: {}".format(safe_inline(str(project_path))),
        "- **Branch**: {}".format(meta["branch"]),
    ])
    parts: list[str] = []
    for depth, name, cls in S.TEMPLATE_SECTIONS:
        if cls == "title":
            heading = "Handoff: " + slug.replace("-", " ")
        elif name is None:
            heading = next(anonymous)
        else:
            heading = name
        parts.append("#" * depth + " " + heading)
        parts.append("")

        if name == "Session Metadata":
            body = metadata_block
        elif cls == "generated":
            body = meta["commits"]
        elif name == "Files Modified":
            # One marker, on a line beneath the generated table - never inside
            # a cell, so the section's count stays one however many rows git
            # emits.
            body = meta["files"] + "\n\n" + S.todo_marker(name)
        elif cls in ("required", "recommended"):
            body = S.todo_marker(name)
        elif cls == "chain":
            body = "\n".join(chain)
        else:
            body = ""

        if body:
            parts.append(body)
            parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


# --- Atomic write ------------------------------------------------------------

def claim_stem(handoffs_dir: Path, stem: str):
    """Reserve `<stem>.md` by exclusively creating `<stem>.md.tmp`.

    A stem is taken if the claim raises FileExistsError *or* `<stem>.md`
    already exists - both must be tested, or the replace below silently
    clobbers a handoff whose claim was already cleaned up. On a taken stem,
    append -2 ... -9 to the timestamp-and-slug stem, never after `.md`.
    """
    suffixes = [""] + ["-{}".format(n) for n in range(2, MAX_STEM_ATTEMPTS + 1)]
    for suffix in suffixes:
        target = handoffs_dir / "{}{}.md".format(stem, suffix)
        claim = handoffs_dir / "{}{}.md.tmp".format(stem, suffix)
        if target.exists():
            continue
        try:
            with open(claim, "xb"):
                pass
        except FileExistsError:
            continue
        return (target, claim)
    return (None, None)


def write_atomically(handoffs_dir: Path, target: Path, claim: Path, text: str) -> None:
    """Render to a dot-prefixed temp, fsync, close, replace, drop the claim."""
    fd, temp_name = tempfile.mkstemp(
        prefix=".session-handoff.", suffix=".md.tmp", dir=str(handoffs_dir)
    )
    temp_path = Path(temp_name)
    try:
        # Close the descriptor before renaming: on Windows an open *source*
        # handle blocks os.replace exactly as an open target handle does.
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temp_path), str(target))
    except BaseException:
        temp_path.unlink(missing_ok=True)
        claim.unlink(missing_ok=True)
        raise
    # The claim is a name reservation, never the document; leaving it behind
    # litters a permanent zero-byte `<stem>.md.tmp` beside every handoff.
    claim.unlink(missing_ok=True)


# --- Entry point -------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="create_handoff.py",
        description="Scaffold a session handoff document.",
    )
    parser.add_argument("slug", nargs="?", default="",
                        help="short task slug; sanitized to [a-z0-9-]")
    parser.add_argument("--continues-from", default=None, metavar="FILE",
                        help="a prior handoff in the same handoffs directory")
    parser.add_argument("--project-path", default=None, metavar="PATH",
                        help="project root (default: the current directory)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(sys.argv[1:] if argv is None else argv)

    # 1. Validate everything before claiming a name.
    project_path = Path(args.project_path or Path.cwd()).expanduser()
    try:
        project_path = project_path.resolve()
    except OSError as exc:
        print("cannot resolve --project-path: {}".format(exc), file=sys.stderr)
        return 1
    if not project_path.is_dir():
        print("--project-path is not an existing directory: {}".format(project_path),
              file=sys.stderr)
        return 1

    slug = sanitize_slug(args.slug)
    handoffs_dir = project_path / ".claude" / "handoffs"

    predecessor = None
    if args.continues_from is not None:
        predecessor, message = resolve_predecessor(args.continues_from, handoffs_dir)
        if predecessor is None:
            print(message, file=sys.stderr)
            return 1

    try:
        handoffs_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print("cannot create handoffs directory {}: {}".format(handoffs_dir, exc),
              file=sys.stderr)
        return 1

    # 2. Claim the stem, before the git subprocesses run.
    now = datetime.now()
    stem = "{}-{}".format(now.strftime("%Y-%m-%d-%H%M%S"), slug)
    target, claim = claim_stem(handoffs_dir, stem)
    if target is None or claim is None:
        print("could not claim a filename for {} in {} (tried {} variants)".format(
            stem, handoffs_dir, MAX_STEM_ATTEMPTS), file=sys.stderr)
        return 1

    # 3. Render and replace; on any failure between the claim and the
    #    successful replace, leave the directory as it was found.
    try:
        meta = collect_git_metadata(project_path)
        document = render_document(
            slug, meta, chain_lines(predecessor),
            now.strftime("%Y-%m-%d %H:%M:%S"), project_path,
        )
        write_atomically(handoffs_dir, target, claim, document)
    except BaseException:
        claim.unlink(missing_ok=True)
        raise

    print(str(target))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
