# Conventions Review — round 3

**Grounding (all read fresh from disk this pass):** `docs/specs/TODO/VHS-29.spec.md` (v3) and `VHS-29.brief.md`; `CLAUDE.md` → `AGENTS.md` (full); `docs/portability-contract.md` §3/§ Uniqueness-position; `docs/authoring-portable-skills.md:41`; `lint.py` (`_read_lines`, `_lint_requires`, `lint_path`); `tests/test_lint.py`, `tests/test_session_handoff.py`; `skills/spec-close/SKILL.md` (all ten cited lines verified at their stated numbers, file is 400 lines); `skills/spec-cycle/SKILL.md:5-10`; `skills/session-handoff/scripts/{_sections.py,create_handoff.py}`; `sync.py:33-39`; root and `tests/fixtures/` `.gitattributes` (plus `git check-attr` on the proposed fixture paths); `docs/specs/DONE/VHS-28/spec.md`. Wiki: `projects/vigil-skills/{state,filemap}.md`, `decisions/` (VHS-18 lint-warn-only, both VHS-28 entries incl. its Revisit-trigger table, wiki-maintenance-redesign), live `log.md` header. Plane VHS-29 via `memory_search` namespace `skills`, tag-exact, 1 hit. All three round-2 reports read from disk. `scale_lens: off` — no `scalability.md` in `round-2/`; nothing to ignore.

**Verified counts backing the spec's claims:** `grep -in "append" skills/spec-close/SKILL.md` → 4 (lines 3, 309, 343, 365); `grep -n "grep -F"` over the same file → 4 (204, 343, 380, 396); `grep -in "append" AGENTS.md` → 2 (29, 100). A repo-wide `git grep -in append` over tracked non-spec, non-test files confirms **no tenth site** — `README.md` and `docs/` carry no stale log-append wording. The spec's nine-site inventory and its 4/3/1/1 breakdown are correct. `tests/test_lint.py:50-53` pins `len(skills) == 8` over `skills/*/SKILL.md`; adding `skills/spec-close/scripts/` does not move that count, so no tripwire bump is owed.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Stale `D8` refs survive v2 renumbering | CLOSED | spec:17 `(D10)`; spec:34 "D10 removes `spec-close` from that list". All 65 `D<n>` citations re-audited by grep — every one resolves to its intended decision |
| conventions | F-2 | § Deferred under-reports v2's own additions | CLOSED | spec:406–417 now carries seven bullets incl. D7's refusal branch and D8's atomicity/concurrency. (v3 introduced two *new* unlisted additions — new F-3 below, not a reopening) |
| conventions | F-3 | Test 15's `AGENTS.md` assertion line-pinned | CLOSED | spec:370 (test 18) is whole-file counts only, with the rationale stated; line numbers demoted to § Scope pointers |
| conventions | F-4 | D9 claims parity Phase 0 step 4 doesn't have | CLOSED | spec:240–242 states the divergence, cites `sync.py:36` (verified: `CLAUDE_CONFIG_DIR` read there, inside `resolve_claude_dir` at :33–39), and brings site 26 along |
| conventions | F-5 | `write_atomically()` duplicated without rationale | CLOSED | spec:232 "On duplicating `write_atomically()`" — independent installs, no shared module, claim-file params inapplicable |
| conventions | F-6 | Shebang / `requires:` position unpinned | CLOSED | spec:280 names `#!/usr/bin/env python3` + mode 644 (verified: all three shipped scripts are git mode `100644` with that shebang); spec:258 "after `user_invocable:`" per contract:93 |
| correctness | F-1 | Two live `D8` refs wrong | CLOSED | as conventions F-1 |
| correctness | F-2 | **D10 cites the wrong test case** | **REOPENED** | v2 said "test case 14"; v3 says "test case 16" (spec:266) — but v3 renumbered the suite 17→20 cases, and case 16 is now "Newlines, both directions." The requires-vs-body assertion is case **19**. Same pointer, wrong again. See F-2 below |
| correctness | F-3 | Re-check placement vs § Design; temp cleanup | CLOSED | spec:207–215 one ordered write block with the re-stat immediately before `os.replace`; spec:222 `try/finally`; spec:221 dot prefix documented as load-bearing against the wiki's `.*.tmp` ignore |
| correctness | F-4 | Done-when #1's cited test can't see 3 of 8 sites | CLOSED | spec:370 asserts two whole-file counts; spec:386 cites case 18; spec:29 states the 4/3/1/1 breakdown |
| correctness | F-5 | Interpreter never named | CLOSED | spec:238 `python <resolved-path>` / `python3 <resolved-path>`, with the Git-Bash-no-shebang-dispatch rationale |
| correctness | F-6 | Read-only-target test is Windows-only | CLOSED | spec:363 — directory-as-path is the portable case; read-only *parent* added under `skipIf(os.name == "nt")`; read-only target explicitly rejected with the POSIX `rename(2)` reason |
| correctness | F-7 | Test 15 stated two ways at once | CLOSED | spec:370 is whole-file counts only |
| correctness | F-8 | Files-to-leave-alone carve-out asymmetry | CLOSED | spec:47 single umbrella rule + the Phases 0/3/4/5/5 note |
| correctness | F-9 | No stat baseline on the missing-file path | CLOSED | spec:228 explicit "File existed" / "File absent" rows |
| edge-cases | F-1 | **P1** Entry heading never validated | CLOSED | D5 "Input validation, in order" step 4 (spec:141) with the full message text; test case 4 (spec:356) drives all four malformed variants |
| edge-cases | F-2 | Temp leak on mismatch; prefix unnamed | CLOSED | spec:210 `prefix=".prepend-log-entry."`; spec:222 `try/finally`; test 13 asserts no leftover temp |
| edge-cases | F-3 | Newline discipline pinned on neither read | CLOSED **in the decision** | spec:168–173 pins `newline=""` on read and normalizes decoded stdin. *But* the CRLF fixture this closure introduced is not shippable under the repo's `.gitattributes` policy — new F-1 below |
| edge-cases | F-4 | Read-only assertion Windows-only | CLOSED | as correctness F-6 |
| edge-cases | F-5 | `reconfigure` AttributeError swallowed into exit 2 | CLOSED | spec:167 own `try/except (AttributeError, ValueError)`; spec:341 "Assert the message, not just the code" as a standing test-plan rule |
| edge-cases | F-6 | No `isatty` guard — script blocks forever | CLOSED | D5 validation step 1 (spec:138) separates "no stdin" from "empty stdin"; test case 10 |
| edge-cases | F-7 | "Halts" vs "report and continue" | CLOSED | spec:155 "A failed log write never aborts the close"; D9 spec:244 reworded to match |
| edge-cases | F-8 | Messages carry neither path nor guard | CLOSED | spec:157 with both concrete message forms |
| edge-cases | F-9 | `--guard` shape unvalidated → exit 1 silent loss | CLOSED | D4 "Guard shape" (spec:111–116), D5 step 3, test case 9 |
| edge-cases | F-10 | Missing-file path has no concurrency baseline | CLOSED | spec:228 "File absent" row |
| edge-cases | F-11 | `mkstemp` 0600 becomes `log.md`'s mode | CLOSED | spec:223; test case 14 under `skipIf(os.name == "nt")` |
| edge-cases | F-12 | Whole-text vs first-line guard asymmetry | CLOSED | spec:109 records the asymmetry, the acceptance rationale, and the natural narrowing |

26 of 27 closed. One REOPENED (correctness F-2), carried as F-2 below.

## Findings

### F-1: The CRLF fixture cannot survive a checkout — the repo's `.gitattributes` policy for byte-exact fixtures is not applied
**Severity:** P1
**Where:** spec.md:43 (§ Files to create); spec.md:349 (§ Fixtures); spec.md:368 (test case 16); spec.md:45–50 (§ Files to leave alone, which omits `.gitattributes`)
**Convention violated:** `tests/fixtures/.gitattributes` — the repo's explicit, comment-documented policy that fixtures encoding exact bytes must be pinned `-text`; and the VHS-28 precedent this spec cites throughout for its test shape.
**Evidence:** The spec ships `tests/fixtures/spec-close/log-crlf.md` as a checked-in fixture and never mentions `.gitattributes`. Root `.gitattributes` is:

```
*.md text eol=lf
*.py text eol=lf
```

`git check-attr -a` on the proposed path returns, today:

```
tests/fixtures/spec-close/log-crlf.md: text: set
tests/fixtures/spec-close/log-crlf.md: eol: lf
```

`text: set` means git normalizes CRLF→LF **into the index on `git add`** and materializes LF on checkout. The fixture's one load-bearing property is destroyed by the commit that adds it.

The repo already solved this twice, two different ways, and the spec matches neither:

1. **Pinned fixture** — `tests/fixtures/.gitattributes` carries `crlf-skill/SKILL.md -text` under the comment *"These fixtures encode exact bytes (CRLF, BOM, 0-byte, tabs) that the lint's robustness tests depend on. Disable text/EOL normalization so they round-trip unchanged across platforms and checkouts."* `git check-attr` on that path returns `text: unset`, and `od -c` confirms the `\r\n` bytes survive.
2. **Built in-test** — VHS-28, the precedent this spec follows for script shape, test shape, and fixture placement, exercises CRLF without a fixture at all: `tests/test_session_handoff.py:471` does `path.write_bytes(minimal_document().replace("\n", "\r\n").encode("utf-8"))` into a tmp dir. Its spec states the reasoning at `docs/specs/DONE/VHS-28/spec.md:60`: *"Root `.gitattributes` (`*.md text eol=lf`) already normalizes them, so **no `-text` entry is needed** and none should be added."* That sentence is true only because VHS-28 shipped no byte-exact fixture; VHS-29 does.

**Why this is P1 rather than P2.** `/ship-spec` implements and runs the test gate inside an isolated worktree, so the fixture is authored there and its on-disk CRLF bytes are still present when the suite runs — the gate goes green. The normalization has already happened in the index. After merge, every other checkout (the primary tree's `git pull`, any fresh clone, any other machine) materializes the fixture as LF, and test case 16's third assertion — *"Prepending into `log-crlf.md` leaves the untouched lines' CRLF intact"* — either **fails** (if written as `assertIn(b"\r\n", result)`) or **passes vacuously** (if written as "terminators unchanged from the fixture"), depending on phrasing the spec does not pin. Both outcomes ship: a red suite on main that the ship gate structurally cannot catch, or a dead assertion standing in for D6's read-side newline guarantee. The repo has no CI (verified: no `.github/workflows/`), so nothing else catches it either.

**Suggested fix:** Prefer option 2 — drop `tests/fixtures/spec-close/log-crlf.md` from § Files to create and restate test case 16's CRLF half as constructed in-test from `log-with-entries.md`, matching `test_session_handoff.py:471`. This keeps `tests/fixtures/.gitattributes` untouched, which is what VHS-28's recorded reasoning asks for. If a checked-in fixture is preferred instead, then `tests/fixtures/.gitattributes` becomes a **tenth changed file**: add `spec-close/log-crlf.md -text`, list it in § Scope, and say in § Fixtures that the `-text` pin is load-bearing — the `crlf-skill` precedent, not an oversight. Either way, § Files to leave alone should stop being silent about `.gitattributes`.

---

### F-2: The v2→v3 test renumbering left four internal pointers on the wrong case — including the exact pointer round-2 correctness F-2 was raised to fix
**Severity:** P1
**Where:** spec.md:29, spec.md:33, spec.md:201, spec.md:266
**Convention violated:** Internal cross-reference integrity. `AGENTS.md` § Plan & Spec Reviews requires precise references; the spec makes its numbered test cases load-bearing pointers (§ Scope, D7, D10, and § Done when all cite them as acceptance evidence). This is also a REOPENED round-2 item — correctness F-2, which the closure manifest reports as "fixed."
**Evidence:** v2 had 17 test cases; v3 has 20. Four citations were not re-derived. Every test-case reference in the spec, by grep:

| spec line | says | v3 case at that number | correct target |
|---|---|---|---|
| 29 | "Test case 15 asserts **both** counts" | 15 = Em dash + BOM round-trip | **18** |
| 33 | "so test case 15 can assert a whole-file count of zero" | 15 = Em dash + BOM round-trip | **18** |
| 201 | "test case 15 asserts zero occurrences in `SKILL.md`" | 15 = Em dash + BOM round-trip | **18** |
| 266 | "which is why **test case 16** asserts the declared set against the tool-use notes" | 16 = Newlines, both directions | **19** |
| 382, 386, 387, 388, 389, 390, 415 | 20 / 18 / 1,2 / 3,4,5,6 / 1 / 19,20 / 18 | — | all correct |

Line 266 is the reopening: round-2 correctness F-2 flagged D10 citing "test case 14," the spec changed it to 16, and the renumbering in the same revision made 16 wrong. The remaining `D<n>` citations are clean — I re-audited all 65 by grep and every one resolves to its intended decision, so the D-axis fix from round 2 held; the defect migrated to the test axis.

Lines 29 and 33 sit in § Scope, which is the first substantive section an implementer reads and the one that establishes *why* the nine-site inventory needs two counts rather than one. Line 201 carries D7's self-consistency argument ("a correct implementation must not trip its own tripwire") on a pointer to an unrelated case.

**Why P1 and not P0.** My closure-table rule defaults REOPENED items to P0. I am not applying that here: the correct targets are unambiguously recoverable from § Done when (#1 correctly cites 18, #5 correctly cites 19, 20), and each cited case is itself fully specified, so the spec is implementable. But this is the third consecutive round in which a renumbering has left dangling internal pointers, and the fix that needs to land is a mechanical whole-document audit rather than another one-off patch — which is why it belongs above the gate rather than in the 2g polish pass.

**Suggested fix:** Change lines 29, 33, and 201 to **test case 18**, and line 266 to **test case 19**. Then, to stop this recurring: either freeze the test-case numbering for the remainder of the spec's life (append new cases at the end rather than inserting), or replace numeric citations with the cases' short titles ("the no-stale-wording case", "the `requires:`-matches-the-body case"), which survive renumbering. The same treatment would future-proof the `D<n>` citations.

---

### F-3: § Deferred's inclusion criteria are not applied to v3's own two additions
**Severity:** P3
**Where:** spec.md:406–417 (§ Deferred); spec.md:155 (D5, "A failed log write never aborts the close"); spec.md:33 (§ Scope, `AGENTS.md:100`)
**Convention violated:** The drift-check contract. `/spec-cycle` Phase 3 renders the spec's deferred items so a human sees brief-unauthorized additions *before* implementation. Round-1 conventions F-7 established that this spec routes such items through § Deferred; round-2 F-2 extended it from three items to seven. Two of v3's own additions did not follow.
**Evidence:** § Deferred's stated criterion is "Additions the brief does not explicitly authorize." Two v3 items meet it and are absent:

- **D5's "A failed log write never aborts the close" (spec:155).** This is new operator-visible control flow in Phase 5: on exit 2 the skill continues to step 5 and prints a completion block carrying `log.md NOT written: <stderr>` plus a re-run recovery. The brief discusses the log step's *placement* and *guard*, never its failure contract, and today's `SKILL.md:343` states none. The section already lists D7's refusal branch and D8's atomicity/concurrency — both likewise failure-path behavior — so the omission is inconsistent with its own precedent, not with an external standard.
- **`AGENTS.md:100` (spec:33).** The brief names five `SKILL.md` sites and the wiki; it never mentions `AGENTS.md`. Line 29 was added in round 1 as a genuine same-contract site. Line 100 is different in kind: it documents `/wiki-after-merge`, a skill the brief and the spec's own § Out of scope both put explicitly off-limits. The spec discloses it in § Scope as "a one-word doc fix" with no behavior change — which is class (c), rationale given — but it never reaches the drift check. Note that this edit is *forced* by test case 18's blanket whole-file count over `AGENTS.md` (see F-4): the tripwire choice is what pulled an out-of-scope skill's documentation into the change set, which is exactly the kind of coupling a drift check exists to surface.

Site 26 got a § Deferred bullet for being "a nine-word edit outside the brief's site list." `AGENTS.md:100` is the same shape and the same size.

**Suggested fix:** Add two bullets to § Deferred: (1) *D5's never-abort-the-close rule — new Phase 5 failure-path behavior the brief does not discuss; chosen to match `SKILL.md`'s existing "Interrupted execute" recovery contract over a half-mutated two-repo tree*; (2) *`AGENTS.md:100` — a one-word correction to `/wiki-after-merge`'s description, a skill this ticket otherwise leaves alone; taken because test 18's whole-file `append` count over `AGENTS.md` requires it.*

---

### F-4: Test 18's blanket zero-`append` tripwire over `AGENTS.md` is over-broad, and it lives in a spec-close-specific test file
**Severity:** P3
**Where:** spec.md:370 (test case 18)
**Convention violated:** Test-ownership locality. Every existing suite in this repo gates the subsystem it is named for: `tests/test_lint.py` asserts over `lint.py` and its fixture corpus (its one repo-wide assertion, `test_shipped_skills_clean`, is *about* the lint's coverage and is documented in the wiki filemap as "a deliberate tripwire, not a clean-run check"); `tests/test_session_handoff.py` asserts over `skills/session-handoff/`. Nothing currently reaches out from a skill's own suite to gate `AGENTS.md`.
**Evidence:** `tests/test_spec_close_log.py` would assert `grep -in "append"` == 0 over `AGENTS.md` — a 108-line living cross-skill doc that most feature PRs edit, and which describes eight skills. The word is legitimately usable there: `skills/spec-cycle/SKILL.md:335` ("append a fourth call to the same message") and `:495` ("reconcile rather than append") show the vocabulary is in ordinary use elsewhere in the repo. When someone later writes a legitimate `append` into `AGENTS.md`, the failing test is named `test_spec_close_log`, which points at the wrong subsystem and gives no hint why the word is forbidden.

Round-2 conventions F-3 anticipated this and offered the narrower form as the alternative ("if a blanket zero is too broad for a doc that may legitimately use the word later, assert on the two sentences located by substring"). The spec took the blanket zero without recording that it considered and rejected the narrower option — and, as F-3 above notes, the blanket form is what dragged `AGENTS.md:100` into scope.

The `SKILL.md` half of test 18 is fine as a blanket count: that file is this ticket's subject, the count is verified at 4 today with all four in the edit set, and the spec argues correctly at line 201 that a correct implementation must not trip its own tripwire.

**Suggested fix:** Keep the whole-file blanket count for `skills/spec-close/SKILL.md`. For `AGENTS.md`, either (a) narrow to content: assert the `/spec-close` bullet and the `/wiki-after-merge` paragraph each contain `prepend` and neither contains `append` — located by substring, never by index, which satisfies round-2 F-3 without the repo-wide claim; or (b) keep the blanket count but state in test 18 that it is a deliberate repo-wide tripwire on this vocabulary, with a failure message that says so, matching how `test_shipped_skills_clean` documents itself.

---

### F-5: D6 re-implements `_sections.normalize()` verbatim, with no equivalent of D8's duplication note, and silently diverges on decode strictness
**Severity:** P3
**Where:** spec.md:164, spec.md:171, spec.md:175 (D6 hazards 2 and 4, and the BOM paragraph); spec.md:232 (D8's duplication note, which does not cover this)
**Convention violated:** Reuse-vs-duplicate / single source of truth. The repo runs `bloat-check` and CodeRabbit over every PR and both are built to flag a near-verbatim second copy of a named helper — which is precisely why round-2 conventions F-5 asked for D8's paragraph.
**Evidence:** D6 specifies, in pieces: decode stdin UTF-8 → normalize `\r\n` and lone `\r` to `\n` → strip a leading BOM. `skills/session-handoff/scripts/_sections.py:76-87` is that exact operation, already shipped, already named:

```python
def normalize(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    if text.startswith("﻿"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")
```

`lint.py:63-73` `_read_lines` is a third instance of the same decode-then-BOM-strip pair. D8 earned a paragraph explaining why `write_atomically()` is re-implemented; D6 re-implements a *closer* duplicate — identical semantics, no parameters to differ on — and says nothing. D8's rationale does extend to it (skills install independently; `sync.py`'s `SUBTREES` is `("skills", "agents")`, so `lint.py` at repo root is never mirrored into the config dir and a shipped skill script cannot import it), but a reviewer of the diff has to re-derive that, or files it as duplication.

Two undocumented divergences from the precedent, both of which look like oversights unless stated:

- **Order.** `_sections.normalize` strips the BOM *before* folding newlines; D6 (spec:171, :175) folds newlines *before* stripping the BOM. Both are correct — U+FEFF is untouched by newline folding — but the inversion reads as accidental.
- **Strictness.** Both precedents decode with `errors="replace"`; D6 specifies bare `.decode("utf-8")`. Strict is the better choice here (silently substituting U+FFFD into an entry that lands permanently in the wiki's operations log would be worse than refusing it, and D5's exception guard turns the `UnicodeDecodeError` into a clean exit 2) — but the spec never says it chose strict, so the divergence reads as inconsistency rather than a decision.

**Suggested fix:** Widen D8's closing paragraph — or add a two-sentence sibling to D6 — to cover the normalization helper as well: `_sections.normalize()` and `lint._read_lines()` are the same operation, neither is importable from an independently-installed skill (`sync.py` mirrors only `skills/` and `agents/`, so repo-root `lint.py` never reaches the config dir), and the sequence is therefore re-implemented deliberately. In the same place, state the strict decode as a choice — *unlike the two precedents, this script decodes strictly, because a mojibake'd entry should be refused rather than silently written into the wiki's permanent log* — and align the BOM-strip/newline-fold order with the precedent unless there is a reason not to.

## Summary
P0: 0 | P1: 2 | P2: 0 | P3: 3 | P4: 0

STATUS: RED P0=0 P1=2 P2=0 P3=3 P4=0
