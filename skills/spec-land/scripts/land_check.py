#!/usr/bin/env python3
"""Classify a spec-land marker, patch-id decision, or path overlap.

Usage:
    land_check.py parse
    land_check.py decide --parents N --pr-commits N --recorded ID --single ID [--range ID]
    land_check.py overlap

parse reads a PR comment body on stdin.
    0  one line: head=<40> base=<40> patch-id=<40> review=<token>
    1  not a marker (stdout empty). A crash must not use this code.
    2  the body is a marker and it is malformed

decide prints exactly "match single", "match range", or "mismatch".
    0  match
    1  mismatch
    2  parents < 1, pr-commits < 1, or a bad hex id

overlap reads two newline-delimited path lists separated by a line that is
exactly "--".
    0  stdout "clear"
    1  the shared paths, sorted, one per line

main() decodes stdin as strict UTF-8. Any other failure exits 3, so exit 1
stays the documented outcome. SystemExit and KeyboardInterrupt propagate:
argparse usage errors stay exit 2.

Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys

_OPEN = "<!-- vigil-spec-land"
_CLOSE = "-->"
_HEX_ID = re.compile(r"^[0-9a-f]{40}$")
_REVIEW_TOKENS = frozenset(("passed", "skipped", "inconclusive", "not-run"))
_ID_LABELS = ("head", "base", "patch-id")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="land_check.py")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("parse")
    decide = sub.add_parser("decide")
    decide.add_argument("--parents", type=int, required=True)
    decide.add_argument("--pr-commits", type=int, required=True)
    decide.add_argument("--recorded", required=True)
    decide.add_argument("--single", required=True)
    decide.add_argument("--range", dest="range_id", default=None)
    sub.add_parser("overlap")
    return parser


def _body_lines(text: str) -> list[str]:
    # Decision 10: one optional CR before each LF. A lone CR is not a break.
    lines = []
    for line in text.split("\n"):
        if line.endswith("\r"):
            line = line[:-1]
        lines.append(line)
    return lines


def _parse_marker(text: str) -> tuple[int, str]:
    # One leading U+FEFF, then one surrounding whitespace run. strip() does
    # not remove U+FEFF, so the BOM has to come off first (Decision 10).
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.strip()
    if not text.startswith(_OPEN):
        return 1, ""
    lines = _body_lines(text)
    if len(lines) != 6 or lines[0] != _OPEN or lines[5] != _CLOSE:
        return 2, ""
    values = []
    for label, line in zip(_ID_LABELS, lines[1:4]):
        prefix = label + ": "
        if not line.startswith(prefix) or _HEX_ID.fullmatch(line[len(prefix):]) is None:
            return 2, ""
        values.append(line[len(prefix):])
    review_prefix = "review: "
    if not lines[4].startswith(review_prefix):
        return 2, ""
    review = lines[4][len(review_prefix):]
    if review not in _REVIEW_TOKENS:
        return 2, ""
    head, base, patch = values
    return 0, f"head={head} base={base} patch-id={patch} review={review}"


def _bad_id(value: str | None) -> bool:
    return value is None or _HEX_ID.fullmatch(value) is None


def _decide(parents: int, pr_commits: int, recorded: str, single: str,
            range_id: str | None) -> tuple[int, str]:
    if parents < 1 or pr_commits < 1 or _bad_id(recorded) or _bad_id(single):
        return 2, ""
    if range_id is not None and _bad_id(range_id):
        return 2, ""
    # Decision 3: two or more parents, and a one-commit PR, compare single only.
    # The range argument is not a candidate on either arm.
    if parents >= 2 or pr_commits == 1:
        if single == recorded:
            return 0, "match single"
        return 1, "mismatch"
    if single == recorded:
        return 0, "match single"
    if range_id is not None and range_id == recorded:
        return 0, "match range"
    return 1, "mismatch"


def _overlap(text: str) -> tuple[int, list[str]]:
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    try:
        split_at = lines.index("--")
    except ValueError:
        # shortcut: missing "--" exits 2, upgrade when Decision 16 names this input
        return 2, []
    shared = sorted(set(lines[:split_at]).intersection(lines[split_at + 1:]))
    if not shared:
        return 0, []
    return 1, shared


def _run(argv: list[str]) -> int:
    args = _parser().parse_args(argv)
    text = sys.stdin.buffer.read().decode("utf-8")
    if args.command == "parse":
        code, line = _parse_marker(text)
        if code == 2:
            print("malformed marker", file=sys.stderr)
        elif line:
            print(line)
        return code
    if args.command == "decide":
        code, line = _decide(
            args.parents, args.pr_commits, args.recorded, args.single, args.range_id)
        if code == 2:
            print("bad arguments", file=sys.stderr)
        elif line:
            print(line)
        return code
    code, paths = _overlap(text)
    if code == 0:
        print("clear")
    elif code == 1:
        for path in paths:
            print(path)
    else:
        print("overlap input has no -- separator", file=sys.stderr)
    return code


def main(argv: list[str]) -> int:
    # Windows stdout is cp1252 when piped. The precedent reconfigures before
    # any write so a later message cannot escape as a crash (exit 1).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass
    try:
        return _run(argv)
    except (KeyboardInterrupt, SystemExit):
        # argparse raises SystemExit(0) for --help and SystemExit(2) for a
        # usage error. Turning those into 3 would hide a bad invocation.
        raise
    except BaseException as exc:  # noqa: BLE001 - exit 1 is a documented outcome
        sys.stderr.write(
            "unexpected failure: {}: {}\n".format(type(exc).__name__, exc))
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
