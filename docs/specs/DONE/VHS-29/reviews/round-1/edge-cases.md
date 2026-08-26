# Edge-Cases Review — round 1

Grounding: spec and brief read fresh; Plane VHS-29 retrieved from the `skills` namespace (tag-exact, 1 hit, consistent with the brief); `AGENTS.md` + machine-local `CLAUDE.md`; the live `skills/spec-close/SKILL.md` (all five cited lines verified at their stated numbers); the real `vigil-harbor-wiki/log.md` header; `sync.py`; `lint.py`'s `requires:` validator; and the VHS-28 precedent (`skills/session-handoff/scripts/`, `tests/test_session_handoff.py`).

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Exit 1 is overloaded — any uncaught exception is reported to the operator as "entry already present — skipped"
**Severity:** P1
**Where:** spec.md:99–103 (D5 exit table); spec.md:168 (§ Design, `main()` flow); spec.md:185 (line 365 skip text)
**Edge case:** Any error the spec did not enumerate — `PermissionError`/`OSError` on the write (wiki file open in an editor, read-only checkout, disk full), `UnicodeDecodeError` on an existing `log.md` that is not valid UTF-8, `UnicodeDecodeError` on non-UTF-8 stdin, `KeyboardInterrupt`.
**What happens:** CPython's default uncaught-exception exit status is **1**. Exit 1 is spec'd as "Skipped — the guard string is already present", which `SKILL.md` line 365 will render as `log.md: entry already present — skipped`, and the close proceeds to print `=== CLOSE COMPLETE ===`. The entry is silently never written **and** the operator is told it already exists — so they will not re-run. This is strictly worse than today's behavior, where a failed `Write` surfaces as a tool error.
**Why the spec misses it:** The exit table's row 2 enumerates a closed list ("no `--guard`, empty stdin, guard not in entry, unreadable path") and § Design line 168 walks `main()` as a linear happy path with no `try`/`except` anywhere. Write-side failure has no row at all. `SKILL.md` is given a three-row mapping, so a fourth exit code (e.g. 127 from a missing interpreter — see F-3) has no defined behavior either.
**Suggested fix:** Wrap `main()`'s body in `try/except Exception` → print `prepend_log_entry: <path>: <err>` to stderr and `return 2`; reserve exit 1 **exclusively** for the guard hit. Add to the exit table: "any other code → treat as failure; report `log.md: NOT written (exit <n>) — <stderr>`, never as success." Add a test: a target made read-only exits 2, not 1.

### F-2: "Fresh wiki" is indistinguishable from "anchor not found in a populated `log.md`" — the script silently re-commits the exact bug this ticket exists to fix
**Severity:** P1
**Where:** spec.md:119–122 (D7 table, Fresh-wiki row); spec.md:101 (exit 0 covers "created, or appended"); spec.md:213 (test case 3)
**Edge case:** A populated `log.md` whose newest heading does not match `ENTRY_RE` — `### [2026-08-25] …` (a hand edit or a rotation script), `## [2026-8-5] …`, a tab or non-breaking space after `]`, a BOM'd first entry (see F-9), or a `log.md` left header-only-plus-prose immediately after a rotation into `log-archive.md`.
**What happens:** D7 row 2's condition is purely "no `ENTRY_RE` match", so the script appends at the **bottom** of a newest-first file, exits **0**, and `SKILL.md` reports `Prepended: log.md`. That is the original VHS-29 bug, now wearing a green success report and no longer prompting the manual re-sort the wiki header asks for. D2 deliberately makes `ENTRY_RE` narrow (line-start, real digits, mandatory trailing space) — every one of those three narrowing properties is also a new way to fall into this branch, and the spec treats the narrowing as pure upside.
**Why the spec misses it:** D7 frames the two non-normal cases as *file states* ("fresh wiki", "missing file") rather than as *what the regex failed to find*. The fixture for case 3, `log-fresh.md`, is the benign shape by construction, so no test exercises "entries exist, anchor missed". D2's claim that "both properties must hold for a false match" reasons only about false **positives**; false negatives are unexamined.
**Suggested fix:** Split the branch on evidence, not on assumption. If `ENTRY_RE` does not match **but** a line-anchored near-miss exists (`re.compile(r"^#{2,6} *\[", re.M)`), exit 2 with `no line-anchored dated entry found in <path>, but <n> heading-like line(s) present — refusing to append; inspect the file`. Only a file with zero heading-like lines takes the fresh-wiki path, and that path prints `no dated entry found — appended at end of file` to stderr so exit 0's two sub-cases are distinguishable. Add a fixture whose newest heading is `### [2026-08-25] close | …` and a test asserting exit 2. Note the follow-on: test case 14's append-wording allowlist must then permit the fresh-wiki path's "appended" wording.

### F-3: The script's runtime path and interpreter are never resolved, and `/spec-close` runs with cwd in a *different* repo
**Severity:** P1
**Where:** spec.md:178–183 (§ Design, "Line 343"); spec.md:91–96 (CLI surface)
**Edge case:** `/spec-close` executes in the **target** repo (Dynasty, MCP server, any repo with `docs/specs/`) — never in `vigil-skills`. The script ships to `<config-dir>/skills/spec-close/scripts/prepend_log_entry.py`.
**What happens:** A skill-relative or repo-relative invocation (`scripts/prepend_log_entry.py`, `skills/spec-close/scripts/…`) does not resolve from the target repo's cwd → `command not found` / exit 127, which F-1 shows has no defined skill behavior. `python` vs `python3` vs a full path is likewise unspecified, and the spec's own test-command section (line 234) acknowledges the multi-interpreter hazard for tests while saying nothing about the runtime call. Net effect: the log entry is not written and, per F-1, plausibly reported as written or skipped.
**Why the spec misses it:** § Design says the rewrite "names the script, and shows the invocation" but never states the resolution rule, delegating it to the implementer. The nearest precedent *inside the file being edited* is explicit — Phase 0 step 4 spells out `~/.claude/skills/ship-spec/states.json` **with** a `%USERPROFILE%\.claude\` Windows variant — and the brief records "Portability contract applies (`docs/portability-contract.md`)" as a carried decision, which a config-dir assumption stated nowhere cannot satisfy. (`skills/session-handoff/SKILL.md:44` uses a bare relative name, but that skill's cwd and skill dir are not split across two repos, and it takes an explicit `--project-path` for exactly this reason.)
**Suggested fix:** State the resolution rule in § Design: the invocation uses the installed skill dir resolved the same way Phase 0 step 4 resolves `states.json` (`~/.claude/skills/spec-close/scripts/prepend_log_entry.py`; `%USERPROFILE%\.claude\…` on Windows), with `$CLAUDE_CONFIG_DIR` honored if set, and name the interpreter (`python3` on Unix / `python` on Windows, or "invoke via the interpreter the harness resolves"). Add a `SKILL.md` fallback line: if the script is not found, halt the log step and print `log.md NOT written: prepend_log_entry.py not found at <path> — install with 'python sync.py install'`, never silent success.

### F-4: `log.md` is rewritten in place with no atomic replace — an interrupt or a full disk truncates the wiki's entire operations log
**Severity:** P1
**Where:** spec.md:85–89 (D5, "The script writes `log.md` in place"); spec.md:168 (§ Design, "→ write")
**Edge case:** Process killed, Ctrl-C, `ENOSPC`, or any exception between truncate and the completed write. `log.md` is not a small file — it holds every wiki entry since the 2026-08-01 rotation boundary, and the script rewrites 100% of its bytes to insert one entry.
**What happens:** `open(path, "w")` truncates to zero **before** any content is written. The window leaves `log.md` empty or half-written. Nothing in the spec detects it, and a partial file that lost its `## [` headings then hits F-2's silent-append branch on the *next* close. Recovery depends on the wiki repo being clean at that moment — and `/spec-close` explicitly leaves the wiki uncommitted (SKILL.md Phase 5 step 5), so a close that also wrote decision/comprehension files and `state.md` has no clean checkpoint to `git checkout --` back to.
**Why the spec misses it:** § Design names `skills/session-handoff/scripts/validate_handoff.py` as the shape precedent — a **read-only** script. The *writing* sibling in the same directory already solved this: `skills/session-handoff/scripts/create_handoff.py:339` `write_atomically()` does mkstemp-in-target-dir → `encoding="utf-8", newline="\n"` → `flush` → `os.fsync` → `os.replace`, with `temp_path.unlink(missing_ok=True)` on `BaseException` and an inline comment about the Windows open-source-handle hazard. D6 reasons carefully about *what bytes* go in the file and not at all about *how* they land.
**Suggested fix:** Add to D5/D6: the write goes through a temp file in `log.md`'s own directory plus `os.replace`, reusing `create_handoff.py:write_atomically`'s shape (including the `fsync` and the `BaseException` cleanup). Align on `newline="\n"` rather than `newline=""` for consistency with that precedent (identical on write; gratuitously divergent as spec'd). Add a test that the temp file is gone after both a success and a forced mid-write exception, and that the original content survives the exception.

### F-5: The blank-line rule is undefined when the anchor is at offset 0 or the existing file is empty — the stated rule produces leading blank lines
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:127–133 (D7, "Blank-line discipline"); spec.md:220 (test case 10)
**Edge case:** (a) `ENTRY_RE` matches at offset 0 — precisely the file D7 row 3 creates, on its second close; (b) `log.md` exists but is zero-byte or whitespace-only.
**What happens:** Case (a): "the text preceding the anchor is normalized to end with exactly one blank line (`\n\n`)" applied to `""` yields `"\n\n"` — the file now opens with two blank lines before its first heading. Case (b): the fresh-wiki rule right-strips to `""` then appends `"\n\n<entry>\n"` — same leading blank lines. Cosmetic, but D7 explicitly claims "Every path leaves the file ending in exactly one `\n`" and says nothing about the start, and test case 10 asserts "exactly one blank line **above** ... the inserted entry ... for all three insertion cases", which is unsatisfiable when nothing is above it. An implementer and a test author will read that differently.
**Why the spec misses it:** D7's three rows are written from the wiki's real shape (header always present), and the missing-file row's own output is never fed back as an input to the normal row.
**Suggested fix:** Add one sentence to the blank-line list: "When the anchor is at offset 0, or the existing content is empty after stripping, the entry is written with **no** leading newline." Restate test case 10 as "no leading blank line; exactly one blank line between the entry and whatever follows; file ends in exactly one `\n`", and add the second-close-on-a-created-file case as its own assertion.

### F-6: stdout/stderr encoding is unpinned — `--dry-run` raises `UnicodeEncodeError` on Windows for a realistic entry
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:107–115 (D6, "Three encoding hazards"); spec.md:105 (`--dry-run` prints to stdout); spec.md:222 (test case 12)
**Edge case:** Entry text containing any character outside cp1252, printed while stdout is a **pipe** (how every agent harness and every `subprocess` test case runs it).
**What happens:** Python uses the locale encoding for a redirected stdout, which on this machine is cp1252, not UTF-8. Close entries routinely exceed it — the live `vigil-harbor-wiki/log.md` VHS-28 entry contains `→` ("68 → 80") and `≥`. `--dry-run` prints the whole merged text, so it raises `UnicodeEncodeError`, which per F-1 exits **1** and reads as "already present — skipped". The same applies to any stderr message that echoes the entry or the guard.
**Why the spec misses it:** D6 asserts exhaustiveness ("**Three** encoding hazards on this specific write, all on Windows, all silent") and enumerates file opens and stdin only. Output streams are never mentioned; the em-dash example happens to be *inside* cp1252, which is why the hazard reads as covered.
**Suggested fix:** Add a fourth hazard to D6: all script output goes through `sys.stdout.buffer.write(text.encode("utf-8"))` / `sys.stderr.buffer.write(...)` (or an explicit `reconfigure(encoding="utf-8", errors="replace")` on both). Extend test case 12 to invoke `--dry-run` as a **subprocess** with an entry containing `→`, asserting exit 0 and UTF-8 bytes on stdout.

### F-7: Stale references to the retired prompt-level `grep -F` survive at three sites outside the five-site list, including a failure-mode entry
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:189–191 (§ Design, "What does not change"); spec.md:224 (test case 14). Live sites: `SKILL.md:380`, `:394`, `:396`
**Edge case:** A future debugger reading the failure-modes section after this ships.
**What happens:** D4 moves the guard into the script, but three sites still document it as a Bash grep the agent runs:
- `SKILL.md:380` — `Bash for ... grep -F (idempotency check)` in the tool-use notes.
- `SKILL.md:394` — "the log idempotency guard ... make[s] re-execution idempotent" (still true, but the mechanism is now exit 1, not a grep).
- `SKILL.md:396` — "**Log-guard encoding.** The `grep -F` idempotency pattern depends on the literal em dash (`—`)..." — a **failure-mode entry naming a mechanism that will no longer exist**, and whose remedy moves to D6's UTF-8 pinning.

**Why the spec misses it:** § "What does not change" updates only line 204's parenthetical, and the change list is framed as "five wording sites" derived from the brief's table of *append* wording. `grep -F` sites are a second, disjoint set. Test case 14 greps only for `append`/`Append`, so none of the three would be caught by the suite that exists to catch exactly this drift.
**Suggested fix:** Change the scope to six sites (add `:380`) and add an explicit "What also changes" note for `:394` and `:396`: reword 396 to name the script's guard and D6's UTF-8 pinning as the remedy; reword 394's clause to "the script's exit-1 guard". Widen test case 14's grep to also assert that `grep -F` no longer appears in `SKILL.md` in an idempotency context.

### F-8: No statement of what happens when two writers touch `log.md` concurrently
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:85–89 (D5); spec.md:147–151 (D9)
**Edge case:** `/wiki-after-merge` (which also prepends to `log.md`), an operator's editor, or a second `/spec-close` writing between this script's read and its write.
**What happens:** Read → guard → full-file write with no lock, no mtime re-check, and no `O_EXCL`. The interleaved write is lost silently, with no error and no record — and because the loser's entry is gone, the guard on a later re-run will not detect the loss either. The fleet genuinely has two `log.md` writers (the brief's § Scope note states this explicitly) and the wiki is a shared working tree.
**Why the spec misses it:** D9 declares scale a non-factor and reasons about *volume* ("one insertion, one file, one entry per close run"), which is unrelated to a second concurrent writer. The cited precedent again already handles the sibling case: `create_handoff.py:330` reserves its target with `open(claim, "xb")` before writing.
**Suggested fix:** Either (a) document last-writer-wins as an accepted risk in D5 with the one-line rationale ("`/wiki-after-merge` and `/spec-close` are operator-sequenced, never concurrent"), or (b) capture `os.stat()` (mtime_ns, size) immediately after the read and re-check it just before `os.replace`, exiting 2 with `log.md changed under us — re-run` on a mismatch. Undocumented is the finding; either resolution closes it.

### F-9: A BOM on the entry text survives `.strip()` and breaks the anchor for the *next* close
**Severity:** P3
**Where:** spec.md:111 (D6, stdin decode); spec.md:129 (D7, "`.strip()`ed of surrounding whitespace")
**Edge case:** Entry text arriving with a leading UTF-8 BOM.
**What happens:** `'﻿'` is not whitespace, so `.strip()` leaves it. The written entry's first line becomes `﻿## [2026-08-25] close | …`, which no longer matches `ENTRY_RE`'s `^## ` at line start. The *current* run looks fine; the **next** close cannot find this entry as an anchor and — per F-2 — silently appends at the bottom. A one-run-delayed, silent reintroduction of the original bug.
**Why the spec misses it:** D6 pins the decode's *encoding* but not BOM handling, and D7's `.strip()` is described as covering "surrounding whitespace", which reads as sufficient. BOM is a known live hazard in this repo — `tests/fixtures/bom-skill/` exists because `lint.py` had to handle it.
**Suggested fix:** `text.lstrip("﻿").strip()` on the decoded stdin (and on the existing file text before the anchor search). Extend test case 8 to feed a BOM-prefixed entry and assert the written first line starts with `## `.

### F-10: `__pycache__` beside the new script mirrors into the config dir via `sync.py install`
**Severity:** P3
**Where:** spec.md:25 (§ Scope, "`sync.py` … unchanged … walks recursively via `iter_files`")
**Edge case:** Running the test suite, which loads the script by file path (spec.md:201) and therefore writes `skills/spec-close/scripts/__pycache__/prepend_log_entry.cpython-3XX.pyc`.
**What happens:** `.gitignore` keeps it out of git, but `sync.py`'s `iter_files` is a bare `rglob("*")` with `p.is_file()` and no exclusion list, so `python sync.py install` copies the `.pyc` into the config dir. Verified as already happening from the VHS-28 precedent: `~/.claude/skills/session-handoff/scripts/__pycache__/` holds three `.pyc` files. Harmless (stale `.pyc` next to a newer `.py` is invalidated by mtime), but it is config-dir litter that outlives an interpreter upgrade.
**Why the spec misses it:** § Scope cites `iter_files` to argue no `sync.py` change is needed — correct for the `.py` file, which is the question it was asking.
**Suggested fix:** One sentence in § Scope acknowledging the pre-existing `__pycache__` mirror as accepted and out of scope (matching the VHS-28 precedent), so a reviewer of the shipped diff does not re-derive it.

### F-11: `AGENTS.md:29` restates the retired append contract and is neither in scope nor covered by the wording test
**Severity:** P2
**Where:** spec.md:11–27 (§ Scope); spec.md:224 (test case 14)
**Edge case:** A reader (human or agent) orienting via the repo's tracked project instructions after this ships.
**What happens:** `AGENTS.md:29` reads "…archive spec artifacts from `TODO/` to `DONE/<TICKET-ID>/` … **and append to wiki `log.md`**" — a verbatim restatement of the behavior being retired, in the file `AGENTS.md` itself designates as the harness-neutral source of truth and that the memory record "CLAUDE.md is gitignored" says must carry anything shipping in a PR. Test case 14's grep is scoped to `SKILL.md` alone, so the suite goes green while the repo's own instructions still document the bug. (`AGENTS.md:100` also says "It appends to `log.md`" — that one is about `/wiki-after-merge` and is correct as-is per D3/§ Out of scope; leave it.)
**Why the spec misses it:** § Scope derives its file list from the brief's five-site table, which was itself derived from a grep of `skills/spec-close/SKILL.md`. The brief's scope note ("`spec-close` is the only skill in `vigil-skills` that writes `log.md` — verified by `grep -rln "log\.md" skills/`") is scoped to `skills/`, so `AGENTS.md` was never in the search path.
**Suggested fix:** Add `AGENTS.md` (line 29 only) to § Scope's files-to-change with the reworded clause, and widen test case 14's grep to cover `AGENTS.md` with an explicit allowlist entry for line 100's `/wiki-after-merge` sentence.

### F-12: The `--guard`-in-entry tripwire is weaker than D4 claims
**Severity:** P4
**Where:** spec.md:83 (D4, "a caller cannot guard on one ticket while writing another's entry")
**Edge case:** An entry whose *body prose* mentions another ticket's close line (close entries routinely quote prior tickets — the live VHS-28 entry names VHS-28, `agentcraft-handoff`, and several sibling decisions).
**What happens:** The substring check only proves the guard appears *somewhere* in the text, so a guard matching body prose rather than the heading passes the tripwire. Harmless in practice; the claim is just stronger than the check.
**Suggested fix:** Require the guard to appear in the entry's **first line** (`entry.splitlines()[0]`), which is the heading the guard is meant to describe, and soften D4's sentence accordingly.

## Summary
P0: 0 | P1: 4 | P2: 5 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=4 P2=5 P3=2 P4=1
