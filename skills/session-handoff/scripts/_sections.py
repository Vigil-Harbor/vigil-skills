#!/usr/bin/env python3
"""Shared section vocabulary, heading matcher and placeholder marker.

VHS-28 D3/D4: one heading matcher, one marker pattern and one section table,
declared here and imported by both entry points by file path. The bug this
skill was filed for was a heading pattern built in three places that diverged
on depth and separator, so nothing below is restated anywhere else.

Public surface: TEMPLATE_SECTIONS, REQUIRED_SECTIONS, RECOMMENDED_SECTIONS,
TODO_MARKER_RE, normalize(), has_section(), first_heading_title(),
todo_marker(). `_HEADING_RE` is private to this module.
"""

from __future__ import annotations

import re

# --- Section vocabulary (D4) -------------------------------------------------
# (depth, name, cls). `cls` drives behavior; `depth` drives rendering only.
# `name` is None where nothing matches or validates the heading, leaving the
# renderer free to title it (D1).
TEMPLATE_SECTIONS = (
    (1, None, "title"),
    (2, "Session Metadata", "container"),
    (3, "Recent Commits", "generated"),
    (2, "Current State Summary", "required"),
    (2, None, "container"),
    (3, "Architecture Overview", "recommended"),
    (3, "Critical Files", "recommended"),
    (2, None, "container"),
    (3, "Files Modified", "recommended"),
    (3, "Decisions Made", "recommended"),
    (2, "Pending Work", "container"),
    (3, "Immediate Next Steps", "required"),
    (2, None, "container"),
    (3, "Important Context", "required"),
    (3, "Assumptions Made", "recommended"),
    (3, "Potential Gotchas", "recommended"),
    (2, "Handoff Chain", "chain"),
)

# Derived from the class column, never written out a second time.
REQUIRED_SECTIONS = tuple(n for _, n, c in TEMPLATE_SECTIONS if c == "required")
RECOMMENDED_SECTIONS = tuple(n for _, n, c in TEMPLATE_SECTIONS if c == "recommended")

# Public: create_handoff.py renders through todo_marker() and neutralizes
# foreign runs with this object; validate_handoff.py scans with it. One
# matcher, one module.
TODO_MARKER_RE = re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)

_GUIDANCE = {
    "Current State Summary": "what is the state of this work right now?",
    "Architecture Overview": "how do the moving parts fit together?",
    "Critical Files": "which files must the next session read first?",
    "Files Modified": "why did each of these change?",
    "Decisions Made": "what was decided, and what was rejected?",
    "Immediate Next Steps": "what is the very next action, in order?",
    "Important Context": "what would the next session get wrong without this?",
    "Assumptions Made": "what is assumed but not verified?",
    "Potential Gotchas": "what is likely to bite the next session?",
}
_DEFAULT_GUIDANCE = "fill this in before handing off"

# --- The one heading matcher (D3) --------------------------------------------
# Depths 1-6; 0-3 leading spaces (4+ is an indented code block); a space or tab
# after the hashes is mandatory, so `#hashtag` and `##Foo` are not headings; an
# optional ATX closing run is stripped from the captured title. Setext headings
# are deliberately not recognized. No `\r` appears here because normalize()
# guarantees none can reach it.
_HEADING_RE = re.compile(
    r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$",
    re.MULTILINE,
)


def normalize(raw: bytes) -> str:
    r"""Decode utf-8 with errors='replace', strip a leading BOM, and fold
    \r\n and lone \r to \n. Every other function here takes this output.

    Raw string deliberately: this docstring *documents* the escapes, so it
    must not contain them - in a module whose thesis is that a stray \r
    breaks matching, shipping one inside its own normalizer would be poor.
    """
    text = raw.decode("utf-8", errors="replace")
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def has_section(normalized: str, name: str) -> bool:
    """True if any ATX heading at ANY depth 1-6 has this title.

    Lookup is BY NAME ONLY; depth never participates. Measured across the five
    documents in one project's `.claude/handoffs/`, three are fully flattened to
    `##` and two use `##`/`###` - so a lookup keyed on (depth, name) would
    report two required sections `missing` on 60% of that corpus, which is a
    depth bug, i.e. precisely the defect VHS-28 was filed for.
    """
    wanted = name.strip().casefold()
    for match in _HEADING_RE.finditer(normalized):
        if match.group(2).strip().casefold() == wanted:
            return True
    return False


def first_heading_title(normalized: str) -> str | None:
    """The first depth-1 heading's title, or None.

    None covers BOTH "no depth-1 heading" and "the heading is empty" - `# `
    alone is a heading and its title group captures '', so the empty title is
    normalized to None here rather than leaving callers to discover that '' is
    not None. Public so create_handoff.py never touches `_HEADING_RE` itself.
    """
    for match in _HEADING_RE.finditer(normalized):
        if len(match.group(1)) == 1:
            title = match.group(2).strip()
            return title or None
    return None


def todo_marker(name: str) -> str:
    """The `[TODO: ...]` text for a section. `TODO_MARKER_RE` matches exactly
    what this emits - one producer, one matcher, one module.

    The section name appears verbatim, which is what makes
    `todo_marker(name) in text` a valid way to locate one section's marker.
    """
    guidance = _GUIDANCE.get(name, _DEFAULT_GUIDANCE)
    return "[TODO: {} \u2014 {}]".format(name, guidance)
