# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | tripwire / 44-passed baseline on unmerged branch | CLOSED | spec § Preconditions:10–24; table verified — `origin/main`=`a0ad847`, 5 `SKILL.md`, `tests/test_lint.py:52` asserts `4`; local branch 8 ahead, 7 skills, asserts `7`. "44 passed" removed from § Test command:310 |
| correctness | F-2 | 68 attributed to "the untouched scaffold" | CLOSED | D6:153 now says "fully-written handoff"; ticket chunk 2 confirms "Measured on a real, fully-written handoff: score 68 → 80" |
| correctness | F-3 | D9 puts operative `~/.claude/…` in SKILL.md | CLOSED | D9:194 harness-neutral sentence; literal path confined to `AGENTS.md` (D9:195) |
| correctness | F-4 | section vocabulary never enumerated | **PARTIAL (P2)** | D4:130 enumerates `REQUIRED_SECTIONS`/`RECOMMENDED_SECTIONS`, but `TEMPLATE_SECTIONS` — the thing D4:126 calls the single source — is still not enumerated. See F-8 below |
| correctness | F-5 | exit 2 overloaded | CLOSED | D6:162 adds exit `3` for operator error |
| correctness | F-6 | D3 span contradicts itself | CLOSED | D3:119 |
| correctness | F-7 | fenced blocks not excluded | CLOSED | D3:97 fence masking (but see F-2/F-5 below for its own defects) |
| correctness | F-8 | `--project-path` purposeless | CLOSED | § `create_handoff.py`:266 |
| correctness | F-9 | advisory score undefined | CLOSED (deferred) | § Deferred:342 |
| correctness | F-10 | test-plan zero-WARN vs Test command | CLOSED | test-plan item 10:299 uses `lint.lint_path`; `tests/test_lint.py:44-46` anchor verified accurate |
| correctness | F-11 | `tests/fixtures/` unused | CLOSED | § Scope:38 + test-plan item 5:294 |
| correctness | F-12 | pytest gate not stdlib-only | CLOSED | § Test command:304–310 |
| correctness | F-13 | "~1,150 lines" is scripts only | CLOSED | D1:58 "1,147 lines of scripts; ≈1,570 including SKILL.md and references" — verified: 1147 + 203 + 139 + 80 = 1569 |
| edge-cases | F-1 | span own-content clause unreachable | CLOSED | D3:119 clause deleted; leaf invariant D4:132 + test item 3:292 |
| edge-cases | F-2 | no text encoding specified | CLOSED | § Encoding discipline:254–260; `cp1252` / `utf8_mode 0` and `U+FEFF` in commit `cb106d5`'s subject both re-verified |
| edge-cases | F-3 | tripwire anchored to unmerged branch | CLOSED | § Preconditions |
| edge-cases | F-4 | legacy corpus unpinned | CLOSED | `tests/fixtures/legacy-handoff.md` + D4:130 + item 5. Verified the vendor template's names/depths satisfy D4's leaf invariant (all 9 names are leaves in `references/handoff-template.md`) |
| edge-cases | F-5 | matcher unifies depth only | **PARTIAL (P1)** | D3:82–95 pins indent/separator/closing-seq/case/setext — but `\r` and the thematic-break matcher remain unspecified. See F-1, F-3 |
| edge-cases | F-6 | generic `KEY=value` class dropped | CLOSED | D1:65 restores it; widths widened at :66; test item 6:295 |
| edge-cases | F-7 | exit 2 overloaded | CLOSED | D6:162 |
| edge-cases | F-8 | BLOCKED has no locus | CLOSED | D6:170 |
| edge-cases | F-9 | fences not excluded | CLOSED | D3:97 |
| edge-cases | F-10 | last section swallows footer | CLOSED | D3:120 + item 3:292 |
| edge-cases | F-11 | `--continues-from` degrades silently | CLOSED | :270 hard error, `resolve()`, case-insensitive |
| edge-cases | F-12 | no git subprocess timeout | CLOSED | :268 10-second timeout |
| edge-cases | F-13 | long slug `OSError` | CLOSED | :267 60-char cap |
| edge-cases | F-14 | `$` vs `fullmatch` | CLOSED | D5:147; `talaria_watch.py:23,77` confirmed `^[0-9a-f]{16}$` + `.fullmatch` |
| edge-cases | F-15 | fallback covers "not found" only | CLOSED | D5:145 "missing **or unusable**"; stats re-measured: 4,181 files / 3.14 GB / 39.6 MB max / 27 over 10 MB (spec says 4,178 / 3.13 — drift only) |
| edge-cases | F-16 | non-atomic write, unbounded chain | CLOSED | :271 `os.replace`; :249 5-hop cap + visited set |
| edge-cases | F-17 | branch-switch staleness | CLOSED | :249 branch compared first, `--all` |
| edge-cases | F-18 | `--project-path` unvalidated | CLOSED | :266 |
| edge-cases | F-19 | table not escaped | CLOSED | :269 |
| edge-cases | F-20 | ancestor repo shadows temp dir | CLOSED | item 8:297 |
| edge-cases | F-21 | score recreates threshold pressure | CLOSED | D6:166 explicit non-gate label |
| conventions | F-1 | shared module has no home | CLOSED | § Scope:33 `scripts/_sections.py`; D4:124 import mechanism; D2:75 fence counts entry points |
| conventions | F-2 | pytest vs stdlib-only | CLOSED | § Test command:310; `skills/talaria/SKILL.md:126` anchor verified |
| conventions | F-3 | case-2 tag missing | CLOSED | D5:142 uses "or the equivalent in your host"; `lint.py` `_CASE2_TAG` confirmed (but anchor stale — F-11) |
| conventions | F-4 | exit 2 overloaded | CLOSED | D6:162 |
| conventions | F-5 | name unresolved | CLOSED | D11:212 |
| conventions | F-6 | D8 asymmetry unstated | CLOSED | D8:184 |
| conventions | F-7 | AGENTS.md File layout row | CLOSED | D12:223 (but its supporting claim is inaccurate — F-9) |
| conventions | F-8 | `--prune` footgun / posture | CLOSED | D9:201–202; verified `sync.py:81-84`, 21 skill dirs − 7 ours = **14** third-party, `README.md:30` promise confirmed, wiki file exists |
| conventions | F-9 | `references/` vs `reference/` | CLOSED | D12:222; `skills/hermes-kanban-awareness/reference/` confirmed as the sole precedent |
| conventions | F-10 | "talaria convention" overstates | CLOSED | :252 reworded to "as it is for talaria" |
| conventions | F-11 | unauthorized spec-level additions | CLOSED (deferred) | § Deferred:341 |

`scale_lens: off` — no `scalability.md` present in `round-1/`; nothing to carry.

## Findings

### F-1: `_HEADING_RE` captures the `\r` of a CRLF line into the title, so every required section reports `missing` on a Windows-authored handoff — and test-plan item 7 asserts the opposite

**Severity:** P1
**Where:** spec § D3 (`docs/specs/TODO/VHS-28.spec.md:82-86`, `:94`); § Encoding discipline (`:259`); test plan item 7 (`:296`)
**Claim:**
```python
_HEADING_RE = re.compile(
    r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$",   # depth, title
    re.MULTILINE,
)
```
…"Section names are matched case-insensitively against the captured title after stripping" (`:94`), and item 7: "a BOM-prefixed handoff and a CRLF handoff both validate correctly" (`:296`).

**Why this is wrong:** With `re.MULTILINE`, `$` matches immediately before `\n`, so on `"## Current State Summary\r\n"` the regex must consume the `\r`. `[ \t]*` cannot match `\r`, but `(.*?)` can (`.` excludes only `\n`), so backtracking resolves group 2 to `"Current State Summary\r"`. The case-insensitive comparison against `"Current State Summary"` then fails, and the section is reported **`missing`** — the exact symptom class VHS-28 was filed for (ticket: "The section is reported missing even when present and fully written").

The encoding discipline does not save this. `lint._read_lines` (`lint.py:63-73`, anchor verified) normalizes only because it ends in `.splitlines()`; `section_span(masked, section)` operates on a whole-document **string**, so `\r` survives the decode. And the spec's "after stripping" (`:94`) is scoped by the preceding bullet to the *ATX closing sequence*, not `str.strip()` — the regex's own `[ \t]*` right-trim is presented as the complete right-hand handling, which is precisely why an implementer would not add a second strip.

This matters here more than usual: the target machine is Windows (`locale.getpreferredencoding(False)` → `cp1252`, verified), and `create_handoff.py` writing with `encoding="utf-8"` and no `newline=` argument uses `os.linesep` translation on Windows — **the tool's own scaffold will be CRLF.** The scaffold cannot pass its own validator, again.

The same defect hits the thematic-break terminator: `---\r\n` is not `---` "alone on a line" under a naive check (D3:107-110).

**Suggested fix:** In § Encoding discipline, add a normalization step to the read discipline: after decode and BOM strip, `text = text.replace("\r\n", "\n").replace("\r", "\n")` before any matching, and state that `section_span` operates on the normalized string. Belt-and-braces in D3: change `[ \t]*#*[ \t]*$` to `[ \t]*#*[ \t\r]*$` and state that the captured title is `.strip()`ed before comparison. Extend test-plan item 7 to assert that a CRLF scaffold validates `READY` with **zero `missing`**, not merely "correctly".

---

### F-2: Required-section content is measured on the fence-masked copy, so a section whose body is a fenced block reports `incomplete` — the very outcome D3's masking paragraph says it exists to prevent

**Severity:** P1
**Where:** spec § D3 fence masking (`:97`); `section_span` signature (`:102-113`); § D3 consequence 2 (`:119`); § `validate_handoff.py` (`:278`)
**Claim:** "`section_span` and the `[TODO: …]` scan operate on a **fence-masked copy** of the document: lines between matching ``` / ~~~ fences are blanked before matching" (`:97`), `def section_span(masked, section)` returning offsets whose `end` is "`len(masked)`" (`:112`), and "required sections present **and** ≥50 characters of own content" (`:278`).

**Why this is wrong:** The spans returned index into `masked`. The spec never re-introduces the original document for the content measurement, so the literal implementation is `len(masked[start:end].strip()) >= 50`. Under that reading, a required section whose body is (or is mostly) a fenced block measures near zero and is reported `incomplete`.

This is not hypothetical for these three names. `### Immediate Next Steps` — one of the three `REQUIRED_SECTIONS` (`:130`) — is the section most likely to be written as a command block. So:

    ### Immediate Next Steps

    1. Run the migration:
       ```bash
       python migrate.py --dry-run && python migrate.py
       ```

…measures 21 characters after masking → `NEEDS WORK`, exit `1`, and the CREATE workflow's "do not finalize" instruction (`:248`) fires on a complete document.

D3's own rationale for masking (`:97`) is: "a fully-written section reports `incomplete` — reintroducing the exact symptom class VHS-28 was filed for." Measuring on the masked copy causes exactly that, by a different route.

The same ambiguity breaks D6's locus requirement (`:170`): if "blanked" means replacing a fenced line with `""` rather than with same-length spaces, offsets and therefore reported `<file>:<line>` values shift.

Test-plan item 2 (`:291`) does not catch this — "A section containing a fenced block with a `# comment` line validates complete" is satisfiable by a section that also carries ≥50 characters of prose.

**Suggested fix:** State in D3 that masking is **length-preserving** (fenced-line characters replaced with spaces, newlines kept), that `section_span`'s offsets are therefore valid against both the masked copy and the original, and that **content length, the finding excerpts, and the reported line numbers are all computed against the original document sliced with those offsets** — masking governs matching only. Add a test-plan item 2 case: a required section whose entire body is a fenced code block validates **complete**.

---

### F-3: The thematic-break terminator — load-bearing per D3 consequence 3 — is left as prose while the heading matcher beside it is pinned to the character

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D3 (`:107-110`, `:120`)
**Claim:** "`end` is the offset of the next heading at ANY depth, the next thematic break (`---`/`***`/`___` alone on a line), or `len(masked)`" (`:107-109`); consequence 3: "Thematic-break termination protects the footer… Without this… an empty required section would return `READY`" (`:120`).

**Why this is wrong:** D3 exists because the vendor left the heading matcher's axes unspecified per call site and they diverged (`:79`). The thematic-break matcher sits in the same module, gates the same verdict, and is specified only by three example strings — leaving unpinned: minimum run length (CommonMark needs ≥3; is `--` a break?), interior spaces (`- - -` is a valid CommonMark break), leading indent (0–3 spaces), trailing whitespace, and `\r` (see F-1). Two implementers will write two different matchers, which is the bug class this decision was created to close.

**Suggested fix:** Add a `_THEMATIC_BREAK_RE` to the `_sections.py` block in D3 with the same completeness treatment, e.g. `^ {0,3}(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$` with `re.MULTILINE`, and add it to D4's `_sections.py` export list (`:126-128`).

---

### F-4: D3's setext bullet contradicts D3's own terminator definition for the `---` underline form

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D3 (`:95` vs `:107-109`)
**Claim:** "**Setext headings (`Title` over `---`) are not supported.** … a setext heading in a hand-edited document neither opens **nor terminates** a section." (`:95`)

**Why this is wrong:** The span definition three lines later terminates at "the next thematic break (`---`/`***`/`___` alone on a line)" (`:108`). A setext `---` underline *is* `---` alone on a line, so it **does** terminate the enclosing section. The claim holds only for the `===` underline form. An implementer following `:95` will not terminate; one following `:108` will — and only the second is what D3 consequence 3 (`:120`) depends on.

**Suggested fix:** Narrow `:95` to: "Setext headings are not recognized as headings — they never *open* a section. A `---` underline still terminates the current section as a thematic break; a `===` underline does not."

---

### F-5: "matching ``` / ~~~ fences" and "following `lint.py`'s `_FENCE_RE` handling" describe two different algorithms

**Severity:** P2
**Where:** spec § D3 (`:97`)
**Claim:** "lines between **matching** ``` / ~~~ fences are blanked before matching, following `lint.py`'s `_FENCE_RE` handling (`lint.py:55, 209-215`)."

**Why this is wrong:** Both anchors are accurate (`lint.py:55` is ``_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")``; `lint.py:209-215` is the toggle) — but `lint.py`'s handling is **not** "matching" fences. It is a boolean toggle flipped by *any* fence marker of *either* character at *any* length:

```python
if _FENCE_RE.match(stripped):
    in_fence = not in_fence
    continue
```
So a ``` line inside a `~~~` block closes it, and a 4-backtick opener is closed by a 3-backtick line. CommonMark — and the word "matching" — require the same character and a closing run at least as long as the opener. The two readings diverge on real handoff content (a fenced markdown example containing a nested fence is common in a handoff about markdown tooling), and divergence flips headings between masked and unmasked, i.e. between `missing` and present.

`lint.py` carries fixtures for exactly this family (`tests/fixtures/indented-fence/`, `tests/fixtures/split-marker/`), so the repo already knows the edge exists.

**Suggested fix:** Pick one and say so. Recommended: specify CommonMark matching semantics (same fence character, closing run ≥ opening run, an unterminated fence runs to EOF) and drop "following `lint.py`'s handling" to "using `lint.py:55`'s `_FENCE_RE` shape". Add a test-plan item 2 case for an unterminated fence (asserting the sections after it are reported, not silently masked away) and for a nested/mismatched fence pair.

---

### F-6: The test plan's exit-code and env-isolation cases are incompatible with the in-process `load_script` helper it names, and no `main(argv) -> int` contract is declared

**Severity:** P2
**Where:** spec § Test plan preamble (`:288`); item 6 (`:295`); item 8 (`:297`); § `create_handoff.py` (`:264`); § `validate_handoff.py` (`:276`)
**Claim:** "scripts load via an `importlib` `load_script` helper because `skills/*/scripts/` is not an importable package" (`:288`), then item 6: "Clean → `READY`/`0`; unfilled TODO → `NEEDS WORK`/`1`; … missing file and no-argument → `3`."

**Why this is wrong:** `tests/test_talaria_watch.py:21-29` (verified) executes the module in-process; there is no process to have an exit code. The repo's precedent is to assert on a **returned** int — `tests/test_talaria_bridge.py:424-426`: `exit_code = bridge._print_failure("doctor", failure); self.assertEqual(exit_code, 1)`. But neither § `create_handoff.py` nor § `validate_handoff.py` declares a `main(argv) -> int` entry point; both describe only a CLI and "Exits `0`/`1`/`2`/`3`". An implementer who writes `sys.exit(...)` inside `main()` forces every item-6 case into `assertRaises(SystemExit)` gymnastics, and item 8's "no-argument" case cannot be exercised at all without `sys.argv` patching.

(Item 8's `GIT_CEILING_DIRECTORIES` approach does work in-process, since a `subprocess.run(["git", …])` with no `env=` inherits the patched `os.environ` — that half is fine.)

**Suggested fix:** Add one line to § `create_handoff.py` and § `validate_handoff.py`: "Exposes `main(argv: list[str]) -> int`; the `if __name__ == '__main__'` guard is `sys.exit(main(sys.argv[1:]))`, following `talaria_bridge.py`'s return-an-int discipline. Tests assert on the returned int, not on `SystemExit`."

---

### F-7: § `create_handoff.py` never states that it imports `_sections`, and the declared `sys.path` mutation contradicts the repo's only recorded precedent

**Severity:** P2
**Where:** spec § D4 (`:124`); § `create_handoff.py` (`:264`) vs § `validate_handoff.py` (`:276`)
**Claim:** D4: "The single source is `_sections.py`, importable by both entry points (same directory; **each entry point inserts its own directory on `sys.path` before importing**)." § `validate_handoff.py`: "Stdlib only. **Imports `_sections`.**" § `create_handoff.py`: "Stdlib only." — no import mentioned, despite D4 assigning it `TEMPLATE_SECTIONS`.

**Why this is wrong:** Two things.

1. **Cross-section disagreement.** An implementer reading § `create_handoff.py` in isolation has no instruction to import the shared vocabulary and will inline the template table — which silently re-creates the two-source drift D4 exists to eliminate. The round-trip test (item 4) would still pass, because it generates its own input from the same inlined table; only the leaf-invariant test (item 3), which reads `TEMPLATE_SECTIONS`, would notice, and only if it reads it from `_sections` rather than from the generated document.

2. **The mechanism works but contradicts recorded practice.** I traced it: under `tests/test_talaria_watch.py:21-29`'s `load_script`, `module_from_spec` sets `__file__`, so a module-level `sys.path.insert(0, str(Path(__file__).resolve().parent))` followed by `import _sections` resolves correctly. **The orchestrator's concern is answered — it does work.** But `skills/talaria/scripts/talaria_bridge.py:4` states "This file deliberately avoids HTTP and `sys.path` mutation", and `talaria_bridge.py:215-226` implements `_temporary_sys_path` as a restoring context manager for exactly this reason. A permanent module-level insert leaks into any test process that loads the script, and would shadow a future second `_sections.py` anywhere on the path.

**Suggested fix:** (a) Add "Imports `TEMPLATE_SECTIONS` from `_sections`" to § `create_handoff.py`:264. (b) Change D4:124 to the talaria-consistent mechanism: load `_sections` via `importlib.util.spec_from_file_location` from `Path(__file__).resolve().parent / "_sections.py"`, or wrap the `sys.path` insert in a restoring `try/finally` — and cite `talaria_bridge.py:215-226` as the precedent. (c) Add to item 3 that the leaf-invariant assertion reads `TEMPLATE_SECTIONS` from the loaded `_sections` module, so an inlined copy in `create_handoff.py` fails the suite.

---

### F-8: `TEMPLATE_SECTIONS` — the artifact D4 calls the single source — is the one thing D4 never enumerates, and the leaf invariant makes its shape non-obvious

**Severity:** P2 *(PARTIAL carry-forward of correctness/F-4, original severity retained)*
**Where:** spec § D4 (`:126`, `:130`, `:132`)
**Claim:** "`TEMPLATE_SECTIONS` — the ordered `(depth, name)` table `create_handoff.py` renders" (`:126`); "**The vocabulary reuses the vendor's names and depths verbatim**" (`:130`); leaf invariant (`:132`).

**Why this is incomplete:** v2 enumerates `REQUIRED_SECTIONS` with depths and `RECOMMENDED_SECTIONS` without them (`:130`), but not `TEMPLATE_SECTIONS`. The leaf invariant then constrains that unenumerated table in a way that is not derivable from the two lists: `Current State Summary` is `##` and `Important Context`/`Immediate Next Steps` are `###`, so the `###` pair **cannot** be nested under `Current State Summary` (that would make it a non-leaf and fail item 3) — they require at least one `##` container heading that appears in neither list. D4 alludes to this only via a parenthetical ("the vendor's `## Context for Resuming Agent` is one", `:132`).

I verified the invariant *is* satisfiable as claimed: in `~/.claude/skills/agentcraft-handoff/references/handoff-template.md`, all nine names are leaves (`Current State Summary`:39 → next `## Codebase Understanding`:43; `Important Context`:97 → `### Assumptions Made`:101; `Immediate Next Steps`:80 → `### Blockers/Open Questions`:86; and the six recommended likewise). So the design is sound — but it only holds if the implementer reconstructs roughly the vendor's container skeleton, and D1 (`:58`) forbids copying "template prose", which is what container headings are. The spec should not leave the implementer to guess whether the containers are exempted.

**Suggested fix:** Enumerate `TEMPLATE_SECTIONS` as an explicit ordered `(depth, name)` table in D4, and add one sentence to D1 carry-forward 2 stating that container heading names are the implementer's to choose (they are never validated), with only the nine `REQUIRED ∪ RECOMMENDED` names fixed by the on-disk schema.

---

### F-9: D5's bounded-read instruction names the wrong end as truncated

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D5 point 3 (`:144`)
**Claim:** "Read the **last 256 KB**, decode from the last complete record boundary, discard a truncated final line."

**Why this is wrong:** In a tail read of a JSONL file, the partial record is the **first** line in the window (the read starts at an arbitrary byte offset mid-record), not the final one. The instruction as written tells the agent to protect the end and leaves the start unprotected, so the first line of the window is a JSON fragment that fails to parse. The same offset can also land mid-UTF-8-sequence; that half is rescued only incidentally by § Encoding discipline's `errors="replace"` (`:260`), which will corrupt the fragment rather than announce it.

**Suggested fix:** Rewrite `:144` as: "Seek to `max(0, size - 256*1024)` and read to EOF; decode with `errors='replace'`; **discard the first line if the read did not start at byte 0** (it is a partial record), and discard the final line if it does not parse as JSON (a live writer may be mid-append)."

---

### F-10: Stale anchor — `lint.py:52` does not hold `_CASE2_TAG`

**Severity:** P2
**Where:** spec § D5 point 1 (`:142`)
**Claim:** "phrased with the repo's canonical §4 case-2 tag (`lint.py:52`, `_CASE2_TAG = \"or the equivalent\"`)."

**Why this is wrong:** `_CASE2_TAG = "or the equivalent"` is at **`lint.py:60`**, on `HEAD` and on `origin/main` alike (`lint.py` is byte-identical between them — `git diff --stat origin/main -- lint.py` is empty). Line 52 is `SERVICES_VOCAB = {...}`. Every other anchor in the spec verified clean: `lint.py:55` (`_FENCE_RE`) ✓, `lint.py:64-73` (`_read_lines`) ✓, `lint.py:209-215` (fence toggle) ✓, `lint.py:291` (`return 1 if (strict and n_err > 0) else 0`) ✓, `sync.py:81-84` (prune loop) ✓, `skills/ship-spec/SKILL.md:76` (`git worktree add … origin/<default-branch>`) ✓, `skills/talaria/SKILL.md:126` ✓, `tests/test_lint.py:44-46` ✓.

*Severity note:* my lens instructions class stale anchors as P1. I am rating this P2 deliberately, because the spec quotes both the symbol name and its literal value, so the citation is self-correcting and misleads nobody — and the repo's shared scale (`AGENTS.md:69`) reserves P0/P1 for load-bearing issues. Flagging the departure rather than making it silently.

**Suggested fix:** `lint.py:52` → `lint.py:60`.

---

### F-11: D12's supporting claim about `AGENTS.md` is inaccurate — there is already a plain per-skill row

**Severity:** P3
**Where:** spec § D12 (`:223`)
**Claim:** "the file adds per-skill rows only for unusual artifacts (`skills/ship-spec/states.json`)."

**Why this is wrong:** `AGENTS.md:54` is `- skills/spec-close/SKILL.md — Post-merge close skill … Installed to ~/.claude/skills/spec-close/SKILL.md.` — an ordinary per-skill `SKILL.md` row, not an unusual artifact. So § File layout does carry at least one plain skill row.

D12's **conclusion** still stands on its other evidence, which I verified: `AGENTS.md` was last touched by `3d6ed40` (2026-06-14), before `a0ad847` talaria (2026-06-28), `386dc6c` and `8946f58` — so the last three skills to ship genuinely added none. Only the "only for unusual artifacts" generalization is false.

**Suggested fix:** Replace the parenthetical with "the file's rows are inconsistent — `skills/spec-close/SKILL.md` has one (`AGENTS.md:54`), the last three skills to ship do not — so a new row would extend an inventory nothing keeps current."

---

### F-12: "resolved before or alongside this work" reopens the boundary § Out of scope just drew

**Severity:** P3
**Where:** spec § Out of scope (`:337`) vs § Preconditions (`:24`)
**Claim:** "**Fixing `main`'s pre-existing red suite** is a precondition to be resolved before or alongside this work (see Preconditions), **not part of this spec's diff**."

**Why this is loose:** "alongside" and "not part of this spec's diff" pull in opposite directions, and the resolution is heavier than the Preconditions text implies. The three commits named at `:19` are not independently cherry-pickable in practice — they sit on `feat/tal-003-talaria-skill` interleaved with five others (`9f0ac85`, `4e5dfc9`, `1b16a60`, `d36e747`, `0932eb6` — the last being this spec's own brief), so "land the three commits above on `main` first" is really "merge that branch's PR". Worth naming so the implementer does not attempt a partial cherry-pick and produce a third divergent tripwire value.

**Suggested fix:** In § Preconditions `:24`, replace "land the three commits above on `main` first" with "merge the open `feat/tal-003-talaria-skill` PR (which carries `386dc6c`, `8946f58`, `7a3a929` among 8 commits) to `main` first"; in § Out of scope `:337`, drop "or alongside".

## Summary
P0: 0 | P1: 2 | P2: 8 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=2 P2=8 P3=2 P4=0
