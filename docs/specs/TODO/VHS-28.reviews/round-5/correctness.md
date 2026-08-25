# Correctness Review — round 5 (delta)

Scope: the 17 hunks in `docs/specs/TODO/VHS-28.reviews/round-5/v4-to-v5.diff` and the sections they land in. Unchanged regions were not re-litigated.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | § Deferred quotes a phrase absent from the brief; "Mapped 1:1" hides the narrowing | **CLOSED** | spec:412-414 quotes brief:44 verbatim (byte-checked against `VHS-28.brief.md:44`), names the dropped third distinction + the `incomplete` verdict, records brief:42's terminator scan and brief:29's `score` as superseded, and cites brief:86's § Open questions verbatim; spec:389 now "Mapped … #2 and #3 are narrowed by D0"; spec:391/392 relabelled "(brief #2/#3, narrowed)"; D12 spec:270 "one of two places" |
| correctness | F-2 (P1) | `TEMPLATE_SECTIONS` cannot render the scaffold; test 2's equality unsatisfiable | **CLOSED** | spec:172 adds the `#` title row; spec:192 settles the `None`-name question and narrows the single-source claim to named rows; spec:194 pins the title format with no `--title`; spec:358 restated as a **subsequence** |
| correctness | F-3 (P1) | `[TODO: …]` emission rule unspecified | **PARTIAL** | spec:149 declares `TODO_MARKER_RE`; spec:330 pins REQUIRED ∪ RECOMMENDED and the git-placeholder prohibition; spec:18 "every **authored** section"; spec:358/363 add the assertions. **But spec:351 still reads "every section carrying a `[TODO: …]` marker"** — the exact line this finding and edge-cases/F-3 both asked to amend. See F-2 below |
| correctness | F-4 (P2) | Accepted-limits list omits the two holes D0 opens | **CLOSED** | spec:26, spec:27 |
| correctness | F-5 (P2) | Public surface stated two ways; normalizer unnamed | **PARTIAL → new variant** | `normalize()` (spec:124) and `first_heading_title()` (spec:138) are now named. But the new closed-surface sentences (spec:121, 143, 147) contradict the new marker-helper / `TODO_MARKER_RE` call sites (spec:149, 330, 345). See F-1 below |
| correctness | F-6 (P3) | `Previous title` fallback | **CLOSED** | spec:338 "If it returns `None` … emit the filename … never fail the create"; test item 8 asserts it |
| correctness | F-7 (P3) | Two imprecise anchors | **CLOSED** | Verified on disk: `AGENTS.md:7` is the "for Claude Code: `~/.claude/skills/`" sentence; `lint.py:63` is `def _read_lines` |
| correctness | F-8 (P4) | `slug` positional vs optional | **CLOSED** | spec:277 now `[slug]` with "(slug omitted or empty → `handoff`)" |
| edge-cases | F-1 (P0) | No document title → `Previous title` has no source | **CLOSED** | spec:172, 194; test item 8 rewritten to chain from an authored H1 |
| edge-cases | F-2 (P1) | Zero-byte claim file stranded | **CLOSED** | spec:324-328 four-step ordering, `try/finally` spanning claim→replace; test item 7 asserts byte-identical directory after a forced failure |
| edge-cases | F-3 (P2) | Marker pattern defined nowhere | **PARTIAL** | Same residue as correctness/F-3: its fix explicitly said "Amend spec.md:323 to 'every *authored* section'" — that line (now spec:351) is untouched |
| edge-cases | F-4 (P2) | Completeness fails open | **CLOSED** | spec:26-27 |
| edge-cases | F-5 (P2) | Recommended-TODO asymmetry | **CLOSED** | spec:224 records the rule and the incentive it creates |
| edge-cases | F-6 (P2) | Bare-path chain rule follows a disclaimed link | **CLOSED** | spec:299 adds the `None` / `new thread` guard with the corpus shape quoted |
| edge-cases | F-7 (P2) | Drift roll-up phrase | **CLOSED** | § Deferred, as correctness/F-1 |
| edge-cases | F-8 (P3) | Accepted limit understated | **CLOSED** | spec:25 rewritten ("A handoff that quotes another handoff will hit this") |
| edge-cases | F-9 (P3) | `GIT_DIR`/`GIT_WORK_TREE` | **CLOSED** | spec:321 |
| conventions | F-1 (P2) | § Deferred drift entry | **CLOSED** | § Deferred |
| conventions | F-2 (P2) | "Test item 4's round-trip" | **CLOSED** | spec:198 now "Test item 2's round-trip" |
| conventions | F-3 (P2) | Missing `from __future__ import annotations` | **CLOSED** | New § Module conventions (spec:307). All precedents verified: `lint.py:36`, `sync.py:20`, `talaria_read.py:4`, `talaria_watch.py:4`, `talaria_bridge.py:10`, `read_board.py:30`; AGENTS.md:7 does declare "Python 3.8+ stdlib"; `def main(argv: list[str] | None = None) -> int` confirmed at `talaria_bridge.py:1070`, `talaria_read.py:289`, `talaria_watch.py:738` |
| conventions | F-4 (P3) | Private name across the module boundary | **PARTIAL → new variant** | `first_heading_title` added as the fix asked; but the patch extended "private" to `TODO_MARKER_RE`, which two modules must share. See F-1 |
| conventions | F-5 (P4) | Cite the wiki decision, not D1 | **CLOSED** | spec:14 quotes `decisions/2026-06-15-vhs-19-fork-and-own-converter.md:14` verbatim — verified |

**No reintroduced closed defects.** I checked every new line against the round-1→4 closures in the three lenses' reports: the collision rewrite still forbids the `os.replace` clobber, the RESUME addition is a narrowing (not a reversal) of the round-3 no-href branch, and D6's new paragraph is consistent with the verdict table. The one new corpus claim — spec:27's "All 23 documents in the on-disk corpus carry zero `[TODO:` markers" — I re-measured: 23 `*/.claude/handoffs/*.md` under `C:/Users/zioni/Documents/Vigil-Harbor/`, zero `[TODO` hits. Exact.

## Findings

### F-1: The patch declares `_sections.py`'s public surface closed at three callables and `TODO_MARKER_RE` private, while three other new lines require a fourth public callable and cross-module use of that regex

**Severity:** P1
**Where:** spec.md:121, spec.md:143, spec.md:147 vs spec.md:149, spec.md:330, spec.md:345 (all six lines are new in v5)

**Claim:**
- spec:121 — "`_sections.py` exposes **exactly three callables**"
- spec:143 — "`normalize`, `has_section`, `first_heading_title` and the name tables are the module's whole public surface; `_HEADING_RE` and **`TODO_MARKER_RE` stay private to it**."
- spec:147 — "declares … **the private** `_HEADING_RE` and `TODO_MARKER_RE`"
- spec:149 — "`create_handoff.py` **renders markers through a helper from this module** and `validate_handoff.py` **scans with the same object**."
- spec:330 — "rendered through `_sections`' helper"
- spec:345 — "no **`TODO_MARKER_RE`** match anywhere in the document"

**Why this is wrong:** Two mutually exclusive statements about the same module, both introduced by this patch:

1. **The fourth callable.** spec:149 and spec:330 require `create_handoff.py` to call a marker-rendering helper *on `_sections`*. spec:121's "exactly three" and spec:143's "whole public surface" say no such callable exists — and the helper is never named or given a signature anywhere, which is the same defect round-4 F-5 filed against the then-unnamed normalizer, relocated onto the marker.
2. **The "private" regex is consumed by both entry points.** spec:149 says `validate_handoff.py` "scans with the same object" and spec:345 names `TODO_MARKER_RE` directly as validate's scan predicate. A name declared private to `_sections` cannot be that object. conventions/F-4 (round 4) flagged exactly this pattern for `_HEADING_RE` and its accepted fix was to keep `_HEADING_RE` private *by adding a public callable* — the patch applied the "private" half to `TODO_MARKER_RE` without the public-callable half.

This is not cosmetic. An implementer who follows D3's closed surface writes `_TODO_MARKER_RE` inside `_sections.py`, and `validate_handoff.py` then either reaches into a private name or re-declares the pattern — the second option recreating "one matcher, two places, diverging" on the single token D0 made the *entire* completeness gate. That is the defect VHS-28 was filed for.

Secondary, same root: spec:319 still says create_handoff "**Imports `TEMPLATE_SECTIONS` from `_sections`**", but v5's spec:338 now also has it calling `_sections.first_heading_title(normalize(...))` and spec:330 the marker helper — three more names than that sentence admits.

**Suggested fix:** In D3, change "exactly three callables" → "four public callables" and add the helper next to `first_heading_title`, e.g. `def todo_marker(name: str) -> str:` ("the `[TODO: …]` text for a section; `TODO_MARKER_RE` matches exactly what this emits"). Amend spec:143 to "`normalize`, `has_section`, `first_heading_title`, `todo_marker`, `TODO_MARKER_RE` and the name tables are the module's whole public surface; `_HEADING_RE` stays private to it", and drop "the private" from `TODO_MARKER_RE` at spec:147. Amend spec:319 to "Imports `TEMPLATE_SECTIONS`, `normalize`, `first_heading_title` and `todo_marker` from `_sections` by file path (D4)".

---

### F-2: The `reference/handoff-template.md` line still says markers go in "every section" — the exact sentence correctness/F-3 and edge-cases/F-3 both asked to amend, now in direct contradiction with the new spec:330

**Severity:** P1
**Where:** spec.md:351 (untouched by the patch) vs spec.md:330 and spec.md:18 (both new)

**Claim:** spec:351 — "The annotated section structure with per-section guidance, depths matching `TEMPLATE_SECTIONS`, **every section carrying a `[TODO: …]` marker** (which is what completeness now rests on)."

**Why this is wrong:** spec:330 now states the opposite in the same document: markers go into "**exactly** the author-filled sections — every name in `REQUIRED_SECTIONS ∪ RECOMMENDED_SECTIONS` … one per section and **nowhere else**", and names `Session Metadata`, `Recent Commits`, `Files Modified` and `Handoff Chain` as sections that "**never** carry one." spec:18 was amended to "every **authored** section"; spec:351 was not.

The patch fixed D0's copy of the phrase and left the § `reference/handoff-template.md` copy, so the round-4 finding is PARTIAL rather than closed on both lenses (edge-cases/F-3's suggested fix names this line explicitly: "Amend spec.md:323 to 'every *authored* section'" — v4's :323 is v5's :351).

It has a functional path, not just a documentation one. spec:351 requires the template's "depths matching `TEMPLATE_SECTIONS`", so the template is a section-for-section mirror of the scaffold; an implementer authoring `create_handoff.py`'s rendering constants against that template emits markers under `Recent Commits` and `Handoff Chain`, which breaks two new assertions at once — test item 2's "none anywhere else" (spec:358) and test item 7's "the not-a-repo scaffold, with its markers replaced, validates `READY`" (spec:363) — and reintroduces the permanently-un-`READY` scaffold that spec:330's own last sentence exists to prevent.

**Suggested fix:** spec:351 → "…depths matching `TEMPLATE_SECTIONS`, **every authored section** (`REQUIRED ∪ RECOMMENDED`, per § `create_handoff.py`) carrying a `[TODO: …]` marker and the generated/fixed-format sections carrying none."

---

### F-3: Test item 8's "authored fixture" is a third fixture the test-plan preamble and § New files both say does not exist

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:364 (new) vs spec.md:355 and spec.md:50-58

**Claim:** spec:364 — "The escaping case chains from an **authored fixture** whose H1 contains `|`, backticks and 200 characters."

**Why this is wrong:** spec:355 says "Cases are generated in temp dirs **except the two fixtures**", and § New files (spec:57-58) lists exactly two: `tests/fixtures/session-handoff/legacy-flat.md` and `legacy-nested.md`. The spec uses "authored fixture" in precisely that tracked sense at spec:359 ("both **authored, not copied**"), so spec:364 reads as a third tracked file that no section creates. The alternative reading — a file the test writes into the temp handoffs dir — is the one that actually works with spec:332's rule that `--continues-from` must resolve inside `<project-path>/.claude/handoffs/`, but then "fixture" is the wrong word for it. Either reading is implementable; the two sections disagree on which.

**Suggested fix:** spec:364 → "The escaping case chains from a predecessor the test **writes into the temp handoffs directory** with an H1 containing `|`, backticks and 200 characters (not a tracked fixture — a *generated* document cannot carry such a title, since D4 derives it from the sanitized 60-char slug)."

---

### F-4: D4 attributes `first_heading_title` to D5; it is declared in D3

**Severity:** P3
**Where:** spec.md:194 (new)

**Claim:** spec:194 — "(**D5's** `first_heading_title` reads exactly this line)."

**Why this is wrong:** `first_heading_title` is declared in D3's code block at spec:138-140. D5 (spec:200-207) is session transfer — it does not mention the function. The patch's own D3 docstring already cross-references correctly ("Public so `create_handoff.py` never touches `_HEADING_RE` itself (D4)"), so this is an isolated slip in a new line.

**Suggested fix:** "D5's" → "D3's".

---

### F-5: The generated-title bound at spec:194 is stated for the slug, not for the heading the slug renders into

**Severity:** P3
**Where:** spec.md:194 (new)

**Claim:** spec:194 — "the slug is the title, which … means a generated document's title is always ASCII, `[a-z0-9 ]`, and ≤60 characters."

**Why this is wrong:** The same sentence pins the title row as `# Handoff: <slug, hyphens replaced by spaces>`, so `first_heading_title` returns `Handoff: my slug here` — which contains `H` and `:` (outside `[a-z0-9 ]`) and runs to 9 + 60 = **69** characters, not 60. The load-bearing half of the claim survives intact (no `|`, no backtick can appear, and 69 < the 80-character truncation at spec:336), so nothing downstream breaks — the stated bound is just measured on the wrong string.

**Suggested fix:** "…always ASCII, drawn from `Handoff: ` plus `[a-z0-9 ]`, and ≤69 characters — inside the 80-character truncation at § `create_handoff.py`, and containing neither `|` nor a backtick."

---

### F-6: § Module conventions calls `str | None` a PEP 585 annotation

**Severity:** P4
**Where:** spec.md:307 (new)

**Claim:** "the PEP 585 annotations used here (`list[str]`, `str | None`)".

**Why this is wrong:** `list[str]` is PEP 585; `str | None` is PEP 604 (3.10, and likewise a `TypeError` on 3.8 without the future import). The conclusion is right for both; only the citation covers one.

**Suggested fix:** "the PEP 585 / PEP 604 annotations used here (`list[str]`, `str | None`)".

---

### F-7: `normalize`'s docstring in the D3 code block will contain literal CR characters

**Severity:** P4
**Where:** spec.md:124-126 (new)

**Why this is wrong:** The docstring is not raw, so `\r` and `\n` are escapes — copied as-is, the module's own normalizer documentation ships with embedded carriage returns, in a spec whose thesis is that stray `\r` breaks matching. Cosmetic, but the code block is the thing implementers copy.

**Suggested fix:** Prefix with `r` (`r"""…"""`) or write the escapes as `` `\r\n` `` in backticks.

## Summary
P0: 0 | P1: 2 | P2: 1 | P3: 2 | P4: 2

Both P1s are single-sentence edits (spec:121/143/147 wording plus a named helper; one word at spec:351), and both are residue of round-4 P1s rather than new design problems — F-2 is a line the patch simply missed, F-1 is over-application of a round-4 conventions fix.

STATUS: RED P0=0 P1=2 P2=1 P3=2 P4=2
