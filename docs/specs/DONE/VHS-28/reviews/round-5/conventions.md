# Conventions Review — round 5 (delta-scoped)

## Closure of round 4 findings

Scoped to my own lens per the delta brief; the other lenses verify theirs.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | § Deferred quoted brief text that does not exist | CLOSED | spec.md:412-414 now quotes brief:44 **verbatim** (byte-checked against the brief), names the dropped third distinction and the `incomplete` verdict, cites brief:42's terminator scan and brief:29's `score` (both verified at those lines), and quotes brief:86's § Open questions verbatim. Done-when softened at spec.md:389 / 392 / 393; D12 now "one of two places" (spec.md:270) |
| conventions | F-2 | stale cross-reference "Test item 4's round-trip" | CLOSED | spec.md:196 reads "Test item 2's round-trip"; item 2 is the template round-trip (spec.md:358) |
| conventions | F-3 | PEP 585 annotations without `from __future__` on a 3.8 floor | CLOSED | New § Module conventions (spec.md:306-308). All six precedents verified to carry the import (`lint.py:36`, `sync.py:20`, `talaria_bridge.py:10`, `talaria_read.py:4`, `talaria_watch.py:4`, `read_board.py:30`); `AGENTS.md:7` states "Python 3.8+ stdlib"; the precedent signature is exact at `talaria_bridge.py:1070`, `talaria_read.py:289`, `talaria_watch.py:738` |
| conventions | F-4 | `_sections` private name across the module boundary | PARTIAL | `first_heading_title()` is public (spec.md:136-138) and `_HEADING_RE` is contained — but the same patch created a new instance of the same root with `TODO_MARKER_RE` (F-2 below) |
| conventions | F-5 | D0's parser rejection cited D1 | CLOSED | spec.md:17 now cites `decisions/2026-06-15-vhs-19-fork-and-own-converter.md`; the quoted sentence is verbatim at that file's line 14, and `docs/portability-contract.md` §3 is the capability-declaration section as claimed |

Incidental anchor repairs also verified: `lint.py:63-73` (`_read_lines` spans exactly 63–73) and `AGENTS.md:7` (carries the "for Claude Code: `~/.claude/skills/`" phrasing).

## Findings

### F-1: New marker rule contradicts `RECOMMENDED_SECTIONS` on `Files Modified` — and makes test item 2's new assertion unsatisfiable
**Severity:** P0
**Where:** spec.md:330 vs. spec.md:180 + spec.md:190; consequence at spec.md:358
**Convention violated:** internal consistency — the schema table is the single source of truth for section classes (D4)
**Evidence:** spec.md:330 (new in v5): "markers go into … **every name in `REQUIRED_SECTIONS ∪ RECOMMENDED_SECTIONS`** … `Session Metadata`, `Recent Commits`, **`Files Modified`** and `Handoff Chain` are generated or fixed-format and **never** carry one." But the table classes `Files Modified` as **recommended** (spec.md:180) and spec.md:190 defines `RECOMMENDED_SECTIONS` = "the six marked recommended", which includes it. So `Files Modified` is simultaneously required to carry a marker and forbidden from carrying one. The other three excluded names check out (container / generated / fixed-format, none in either set) — `Files Modified` is the sole offender.
This is load-bearing rather than cosmetic: test item 2's new assertion (spec.md:358) — "a fresh scaffold contains **exactly one `[TODO: …]` per `REQUIRED ∪ RECOMMENDED` name and none anywhere else**" — cannot pass under either reading. If `Files Modified` is git-generated (as § `create_handoff.py` says: "modified + staged files"), the count is one short; if it carries a marker, spec.md:330's exclusion is wrong and every CREATE ships a `NEEDS WORK` placeholder inside auto-generated content. Both halves of the contradiction are new `+` lines in this patch.
**Suggested fix:** Reclassify the table row to `| ### | Files Modified | generated |` (spec.md:180), drop it from `RECOMMENDED_SECTIONS`, and change spec.md:190's "the six marked recommended" to "the five marked recommended". That keeps spec.md:330's exclusion list correct as written and makes item 2's count assertion well-formed. (The alternative — leaving it recommended and giving it a marker — conflicts with the git-metadata rendering and with D6's new "marker in a recommended section is `NEEDS WORK`" rule at spec.md:224.)

### F-2: `TODO_MARKER_RE` is declared private, then consumed across the module boundary — the round-4 F-4 shape, re-created
**Severity:** P2
**Where:** spec.md:143, spec.md:147, spec.md:149, spec.md:345
**Convention violated:** PEP 8 leading-underscore convention, and the spec's own enumerated public surface (D3)
**Evidence:** spec.md:143 (new): "`normalize`, `has_section`, `first_heading_title` and the name tables are the module's whole public surface; `_HEADING_RE` and **`TODO_MARKER_RE` stay private to it**", echoed at spec.md:147 ("the **private** `_HEADING_RE` and `TODO_MARKER_RE`"). But spec.md:149 says "`validate_handoff.py` scans with **the same object**", and spec.md:345 names it directly: "no `TODO_MARKER_RE` match anywhere in the document". A name with no leading underscore that a second module imports is public by convention; calling it private is the exact defect round-4 F-4 raised for `_HEADING_RE`, which this patch otherwise closed by promoting `first_heading_title()`.
Related, same root: spec.md:149 introduces an unnamed fourth callable ("`create_handoff.py` renders markers **through a helper from this module**") three lines after D3 commits to "exactly three callables" (spec.md:132).
**Suggested fix:** At spec.md:143/147, move `TODO_MARKER_RE` into the public list (it is a deliberately shared constant — that is the whole point of spec.md:149) and leave only `_HEADING_RE` private. Name the marker helper and update D3's count: "exactly four callables — `normalize()`, `has_section()`, `first_heading_title()`, `todo_marker(name) -> str` — plus `TODO_MARKER_RE` and the name tables."

### F-3: Temp-file naming drops the repo's dot-prefix precedent
**Severity:** P4
**Where:** spec.md:327 (collision step 3)
**Convention violated:** the repo's four-instance atomic-write shape
**Evidence:** Every existing instance dot-prefixes the temp so it sorts and globs out of the way: `tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)` (`talaria_bridge.py:420`, `talaria_watch.py:123`, `talaria_watch.py:140`) and `prefix=".talaria-read."` (`talaria_read.py:174`). The spec specifies `mkstemp(dir=<handoffs dir>, suffix=".md.tmp")` with no prefix, so mkstemp's default yields a visible `tmpXXXXXXXX.md.tmp` in the operator's handoffs directory.
**Suggested fix:** `tempfile.mkstemp(prefix=".session-handoff.", suffix=".md.tmp", dir=<handoffs dir>)`. (Harmless either way — RESUME's `*.md` listing and `*.tmp` ignore both behave correctly — so this is conformance, not a bug.)

### F-4: The claim step opens a text-mode file with no encoding, against the spec's own absolute rule
**Severity:** P4
**Where:** spec.md:326 (collision step 2)
**Convention violated:** § Encoding discipline, spec.md:311
**Evidence:** spec.md:311 states without qualification: "**All file I/O is explicitly UTF-8**", justified by the measured `cp1252` default on the operator machine. Step 2 specifies `with open(path, "x"): pass` — text mode, no `encoding=`. Nothing is written through the handle, so no encoding is exercised, but an implementer applying spec.md:311 literally has to guess whether this is an exception.
**Suggested fix:** Write it as `with open(path, "xb"): pass` (binary makes the absence of an encoding self-evidently correct), or add `encoding="utf-8"` for uniformity.

### F-5: "the four container rows" does not match the table
**Severity:** P4
**Where:** spec.md:358, against the table at spec.md:169-186 and the sentence at spec.md:192
**Convention violated:** the table is the source of truth for row counts
**Evidence:** spec.md:192 (new) says "the title row and **the container rows** carry `None`". The table has five container-class rows — `Session Metadata`, three anonymous `*(container)*` rows, and `Pending Work` — or three if only the anonymous ones are meant. spec.md:358 (new) says "the title row and the **four** container rows". Neither reading yields four. The subsequence assertion itself is robust to the count (it filters on `if name`), so this is explanatory text only.
**Suggested fix:** Change "the four container rows" to "the five container rows" at spec.md:358, matching spec.md:192's reading that all container-class rows carry `None` and are rendered from `create_handoff.py`'s constants.

## Summary
P0: 1 | P1: 0 | P2: 1 | P3: 0 | P4: 3

STATUS: RED P0=1 P1=0 P2=1 P3=0 P4=3
