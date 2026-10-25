#!/usr/bin/env python3
"""Parse a brief's ## Premises section and the Decision citations that rest on it.

Stdlib only. Reads one brief path and never writes it. Exit 0 is silence.
Exit 1 is a data or gate failure. Exit 2 is usage, an unreadable path, or
an unexpected error. See the VHS-67 spec, Parser and exits.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LEVELS = ("said", "pointed", "walked", "ran", "reproduced")
BELOW_RAN = ("said", "pointed", "walked")
KNOWN_FIELDS = ("Level", "Source", "Defeats ticket", "Override")
PREMISES_TITLE = "## Premises"
DECISIONS_TITLE = "## Decisions carried forward"
NO_PREMISES = "_(no premises)_"
NO_DECISIONS = "_(none settled — see Risks / decisions)_"

ITEM_RE = re.compile(r"^(\d+)\.\s+\*\*P(\d+)\.\*\*(.*)$")
FIELD_RE = re.compile(r"^\*\*([A-Za-z][A-Za-z0-9 ]*):(\*\*)(.*)$")
HEADING_RE = re.compile(r"^#{1,2} ")
DECISION_RE = re.compile(r"^(\d+)\.\s")
NUMBERED_RE = re.compile(r"^\d+\.\s")
REST_PART_RE = re.compile(
    r"^P(\d+) \((said|pointed|walked|ran|reproduced)\)$"
)
PATH_LINE_RE = re.compile(r"\S+:\d+")


class Unreadable(Exception):
    """The path is a directory, missing, unreadable, or not UTF-8."""


def _strip3(line):
    i = 0
    while i < len(line) and i < 3 and line[i] == " ":
        i += 1
    return line[i:]


def _fence_marker(line):
    """Return (char, length) when line opens or closes a fence, else None.

    A marker is three or more backticks or tildes at the start of the line
    after at most three spaces. A line prefixed '> ' is not a marker.
    """
    if line.startswith("> "):
        return None
    rest = _strip3(line)
    if not rest:
        return None
    ch = rest[0]
    if ch not in "`~":
        return None
    n = 0
    while n < len(rest) and rest[n] == ch:
        n += 1
    if n >= 3:
        return (ch, n)
    return None


def _scan_fences(lines):
    in_fence = []
    open_fence = None
    for line in lines:
        marker = _fence_marker(line)
        if open_fence is None:
            if marker is not None:
                open_fence = marker
                in_fence.append(True)
            else:
                in_fence.append(False)
        else:
            in_fence.append(True)
            if (
                marker is not None
                and marker[0] == open_fence[0]
                and marker[1] >= open_fence[1]
            ):
                open_fence = None
    return in_fence, open_fence is not None


def _is_heading_12(line):
    if line.startswith("> "):
        return False
    return HEADING_RE.match(_strip3(line)) is not None


def _heading_indexes(lines, in_fence, title):
    found = []
    for i, line in enumerate(lines):
        if in_fence[i] or line.startswith("> "):
            continue
        if _strip3(line).rstrip(" ") == title:
            found.append(i)
    return found


def _section_end(lines, in_fence, start):
    for i in range(start + 1, len(lines)):
        if in_fence[i] or lines[i].startswith("> "):
            continue
        if _is_heading_12(lines[i]):
            return i
    return len(lines)


def _item_start(line):
    if line.startswith("> "):
        return None
    match = ITEM_RE.match(_strip3(line))
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2)), match.group(3)


def _field(line):
    if line.startswith("> "):
        return None
    match = FIELD_RE.match(_strip3(line))
    if match is None:
        return None
    return match.group(1), match.group(3)


def _numbered_loose(line):
    """True when a non-item line has the shape that must not continue a field."""
    return NUMBERED_RE.match(line.lstrip()) is not None


def _emit(problems, code, detail):
    if detail:
        problems.append("premise: {} {}".format(code, detail))
    else:
        problems.append("premise: {}".format(code))


def _check_item(item, position, problems):
    for code, detail in item["scan"]:
        _emit(problems, code, detail)

    claim = " ".join(item["claim"]).strip()
    p_label = "P{}".format(item["p_n"])
    if claim == "":
        _emit(problems, "claim-missing", p_label)
    if item["list_n"] != position or item["p_n"] != position:
        _emit(problems, "item-id", "P{}".format(item["list_n"]))

    fields = item["fields"]
    level = None
    if "Level" not in fields:
        _emit(problems, "level-missing", p_label)
    else:
        level = fields["Level"].strip()
        if level not in LEVELS:
            _emit(problems, "level-invalid", p_label)
            level = None

    flag = None
    if "Defeats ticket" not in fields:
        _emit(problems, "flag-missing", p_label)
    else:
        flag = fields["Defeats ticket"].strip()
        if flag not in ("yes", "no"):
            _emit(problems, "flag-invalid", p_label)
            flag = None

    if "Source" not in fields or fields["Source"].strip() == "":
        _emit(problems, "source-missing", p_label)
    elif level is not None:
        source = fields["Source"].strip()
        bad = False
        if level in ("pointed", "walked") and PATH_LINE_RE.search(source) is None:
            bad = True
        elif level in ("ran", "reproduced") and "source: run:" not in source:
            bad = True
        if bad:
            _emit(problems, "source-invalid", p_label)

    override_empty = False
    has_override = False
    if "Override" in fields:
        if fields["Override"].strip() == "":
            override_empty = True
            _emit(problems, "override-empty", p_label)
        else:
            has_override = True

    if (
        flag == "yes"
        and level in BELOW_RAN
        and not override_empty
        and not has_override
    ):
        _emit(problems, "below-ran", p_label)

    item["level"] = fields["Level"].strip() if "Level" in fields else None


def _parse_items(lines, in_fence, start, end, problems):
    """Return ('marker', None), ('empty', None), ('mixed', None), or ('items', list)."""
    nonblank = []
    for i in range(start + 1, end):
        if in_fence[i]:
            continue
        if lines[i].strip() == "":
            continue
        nonblank.append(i)

    marker_at = None
    other = False
    item_indexes = []
    for i in nonblank:
        if lines[i].strip() == NO_PREMISES:
            if marker_at is None:
                marker_at = i
            else:
                other = True
            continue
        other = True
        if _item_start(lines[i]) is not None:
            item_indexes.append(i)

    if marker_at is not None and other:
        return "mixed", None
    if marker_at is not None:
        return "marker", None
    if not item_indexes:
        return "empty", None

    items = []
    for pos, idx in enumerate(item_indexes):
        list_n, p_n, rest = _item_start(lines[idx])
        item = {
            "list_n": list_n,
            "p_n": p_n,
            "claim": [rest],
            "fields": {},
            "scan": [],
            "level": None,
        }
        next_idx = item_indexes[pos + 1] if pos + 1 < len(item_indexes) else end
        seen_field = False
        latest = None
        for j in range(idx + 1, next_idx):
            if in_fence[j]:
                continue
            raw = lines[j]
            if raw.strip() == "":
                continue
            if _item_start(raw) is not None:
                break
            parsed = _field(raw)
            if parsed is not None:
                label, value = parsed
                seen_field = True
                if label not in KNOWN_FIELDS:
                    item["scan"].append(("field-unknown", "P{} {}".format(p_n, label)))
                    latest = ["sink", []]
                elif label in item["fields"]:
                    item["scan"].append(("field-duplicate", "P{} {}".format(p_n, label)))
                    latest = ["sink", []]
                else:
                    item["fields"][label] = value.strip()
                    latest = ["known", label]
                continue
            if seen_field and _numbered_loose(raw):
                item["scan"].append(("item-unparsed", str(j + 1)))
                continue
            text = raw.strip()
            if not seen_field:
                item["claim"].append(text)
            elif latest is not None and latest[0] == "known":
                item["fields"][latest[1]] = (
                    item["fields"][latest[1]] + " " + text
                ).strip()
        items.append(item)

    for position, item in enumerate(items, start=1):
        _check_item(item, position, problems)
    return "items", items


def _parse_rests(value):
    value = value.strip()
    if value == "none":
        return "none", []
    parts = value.split("; ")
    parsed = []
    seen = set()
    for part in parts:
        match = REST_PART_RE.match(part)
        if match is None:
            return "invalid", []
        pid = int(match.group(1))
        if pid in seen:
            return "invalid", []
        seen.add(pid)
        parsed.append((pid, match.group(2)))
    if not parsed:
        return "invalid", []
    return "ok", parsed


def _check_decisions(lines, in_fence, problems, items):
    headings = _heading_indexes(lines, in_fence, DECISIONS_TITLE)
    if not headings:
        return
    if len(headings) >= 2:
        _emit(problems, "decision-section", "")
        return

    start = headings[0]
    end = _section_end(lines, in_fence, start)
    content = []
    for i in range(start + 1, end):
        if in_fence[i]:
            continue
        if lines[i].strip() == "":
            continue
        content.append(i)
    if len(content) == 1 and lines[content[0]].strip() == NO_DECISIONS:
        return

    starts = []
    for i in content:
        line = lines[i]
        if line.startswith("> ") or line[:1] in (" ", "\t"):
            continue
        match = DECISION_RE.match(line)
        if match is None:
            continue
        starts.append((i, int(match.group(1))))

    levels = {}
    if items:
        for item in items:
            if item["p_n"] not in levels:
                levels[item["p_n"]] = item["level"]

    for pos, (idx, number) in enumerate(starts, start=1):
        if number != pos:
            _emit(problems, "decision-id", str(number))
        next_idx = starts[pos][0] if pos < len(starts) else end
        # pos is 1-based; the next start lives at index pos in `starts` when
        # another item follows. `pos < len(starts)` is that test.
        rests = []
        below = []
        for j in range(idx, next_idx):
            if j >= end or in_fence[j] or lines[j].startswith("> "):
                continue
            text = lines[j].strip()
            if text.startswith("**Rests on:**"):
                rests.append(text[len("**Rests on:**"):].strip())
            elif text.startswith("**Below ran:**"):
                below.append(text)
        n_label = str(number)
        if not rests:
            _emit(problems, "rests-on-missing", n_label)
            continue
        if len(rests) >= 2:
            _emit(problems, "rests-on-duplicate", n_label)
            continue
        status, cites = _parse_rests(rests[0])
        if status == "invalid":
            _emit(problems, "rests-on-invalid", n_label)
            continue
        if status == "ok":
            for pid, cited in cites:
                if pid not in levels:
                    _emit(problems, "rests-on-unknown", "{} P{}".format(n_label, pid))
                elif cited != levels[pid]:
                    _emit(problems, "rests-on-level", "{} P{}".format(n_label, pid))
        ran_cited = status == "none" or any(
            level in ("ran", "reproduced") for _, level in cites
        )
        all_below = status == "ok" and cites and all(
            level in BELOW_RAN for _, level in cites
        )
        if ran_cited:
            if below:
                _emit(problems, "below-ran-line", n_label)
        elif all_below:
            if any(text != "**Below ran:** yes" for text in below) or not any(
                text == "**Below ran:** yes" for text in below
            ):
                _emit(problems, "below-ran-line", n_label)


def _split_lines(text):
    lines = text.split("\n")
    return [line[:-1] if line.endswith("\r") else line for line in lines]


def _read(path):
    file_path = Path(path)
    if file_path.is_dir():
        raise Unreadable()
    try:
        data = file_path.read_bytes()
    except OSError:
        raise Unreadable()
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise Unreadable()
    return _split_lines(text)


def _run(argv):
    problems = []
    if len(argv) != 1:
        _emit(problems, "usage", "")
        return 2, problems
    try:
        lines = _read(argv[0])
    except Unreadable:
        _emit(problems, "unreadable", "")
        return 2, problems

    in_fence, fence_open = _scan_fences(lines)
    if fence_open:
        _emit(problems, "fence-open", "")
        return 1, problems

    headings = _heading_indexes(lines, in_fence, PREMISES_TITLE)
    if not headings:
        _emit(problems, "section-absent", "")
        return 1, problems
    if len(headings) >= 2:
        _emit(problems, "section-duplicate", "")
        return 1, problems

    end = _section_end(lines, in_fence, headings[0])
    kind, items = _parse_items(lines, in_fence, headings[0], end, problems)
    if kind == "mixed":
        _emit(problems, "marker-and-items", "")
        return 1, problems
    if kind == "empty":
        _emit(problems, "section-empty", "")
        return 1, problems

    _check_decisions(lines, in_fence, problems, items)
    if problems:
        return 1, problems
    return 0, problems


def _reconfigure():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass


def main(argv):
    """Return 0, 1, or 2. Problems go to stderr. Stdout stays empty."""
    _reconfigure()
    try:
        code, problems = _run(argv)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as exc:  # noqa: BLE001 - exit 2 names the exception class
        sys.stderr.write("premise: error {}\n".format(type(exc).__name__))
        return 2
    if problems:
        sys.stderr.write("\n".join(problems) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
