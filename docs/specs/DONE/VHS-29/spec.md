# VHS-29 — `/spec-close` prepends its `log.md` entry

**Brief:** `docs/specs/TODO/VHS-29.brief.md` · **Plane:** VHS-29 · **Spec version:** v8 (round-6 delta findings folded)

> **Citation convention.** Test cases are referred to by **title**, never by number — three consecutive rounds broke numeric pointers when the plan grew. Decisions keep their `D<n>` ids, which have been stable since v2.

## Goal

Make `/spec-close` write its close entry to the **top** of the wiki's newest-first `log.md` instead of the bottom, using an insertion anchor that provably cannot match the header's own `Format: ## [YYYY-MM-DD] action | description` sentence. The deterministic part — find the anchor, refuse when the file's shape is not what the anchor assumes, refuse when the entry's own heading is not what the *next* run's anchor will look for, guard against duplicates, and land the bytes atomically — moves out of prose and into `skills/spec-close/scripts/prepend_log_entry.py`, a stdlib-only script that a test suite can drive against a fixture reproducing a real `log.md` header. Every site in the repo that documents the old append contract, or the `grep -F` guard the script retires, is reworded with it. The wiki-side "Append-only record" sentence is reconciled separately, direct on wiki master.

## Scope

### Files to change

**`skills/spec-close/SKILL.md` — nine sites.** All nine are verified at these line numbers against the current file.

| Line | Site | Change |
|---|---|---|
| 3 | Frontmatter `description` | "and append to wiki log.md" → prepend wording; `requires:` block added to the frontmatter (D10) |
| 26 | Phase 0 step 4, `states.json` path | Add `$CLAUDE_CONFIG_DIR` to the resolution, so the file states one config-dir rule rather than two (D9) |
| 204 | Phase 3 coverage-model note | Its parenthetical names the retired prompt-level `grep -F` guard; re-point at the script |
| 309 | Close-plan template | `Log.md append:` → `Log.md entry (prepended):` |
| 343 | **Phase 5 step 4** | Rewritten — the load-bearing site |
| 365 | Completion output | `Appended: log.md` → `Prepended: log.md`, plus the skip and failure lines |
| 380 | Bash tool-use bullet | Drop `` `grep -F` (idempotency check) ``; add the script invocation. `grep -rlw` / `grep -c` stay (duplicate detection, unrelated) |
| 381 | Write-targets bullet | Drop `log.md` from the Write list |
| 396 | `**Log-guard encoding.**` failure mode | Re-anchor the em-dash hazard from `grep -F` onto the script's `--guard` compare |

Line **382** (the mutation-boundary bullet) is **unchanged**: `log.md` stays in its "All other writes … happen in Phase 5, after explicit user approval" list, which remains true. The brief and the Plane ticket both said "line 382" for the Write-targets sentence; that is an off-by-one — the sentence is at 381. Corrected here.

Four of the nine sites (3, 309, 343, 365) carry `append` wording; three (204, 380, 396) carry the `grep -F` guard and no `append` at all; one (26) is the config-dir rule; one (381) is the Write-target list. The **no-stale-wording** test case asserts *both* counts, because a zero-`append` assertion alone cannot see three of the nine.

**Other tracked files:**

- `AGENTS.md:29` — "…and append to wiki `log.md`" restates the retired contract in the repo's canonical tracked doc (`CLAUDE.md` is gitignored). Reworded. `AGENTS.md:100` — "It appends to `log.md`" describing `/wiki-after-merge`, which in fact prepends; corrected in the same edit as a one-word doc fix. No behavior of that skill is touched.
- `docs/authoring-portable-skills.md:41` — the tracked missing-`requires:` backlog names three skills (`ship-spec`, `spec-close`, `review-pr`). D10 removes `spec-close` from that list; the sentence is updated to name the remaining two.

### Files to create

- `skills/spec-close/scripts/prepend_log_entry.py` — the insertion script. First script this skill has shipped.
- `tests/test_spec_close_log.py` — the test suite.
- `tests/fixtures/spec-close/log-with-entries.md` — real-shaped header + two dated entries.
- `tests/fixtures/spec-close/log-fresh.md` — real-shaped header, zero dated entries.
- `tests/fixtures/spec-close/log-h3-entries.md` — real-shaped header + entries at `###` depth, so the anchor misses. Drives D7's refusal path.
- `tests/fixtures/spec-close/log-no-trailing-newline.md` — real-shaped header + entries, ending without a final `\n`. Makes D7's tail invariant non-vacuous.

**No CRLF fixture is checked in.** An earlier draft shipped `log-crlf.md`; it cannot survive its own commit. Root `.gitattributes` is `*.md text eol=lf`, and `git check-attr -a tests/fixtures/spec-close/log-crlf.md` returns `text: set` — git normalizes CRLF→LF **into the index on `git add`** and materializes LF on every checkout. `/ship-spec` would go green (the worktree still holds the authored bytes) and the assertion would then fail or pass vacuously on every other clone, with no CI to catch it. The repo has a pin for this (`tests/fixtures/.gitattributes` carries `crlf-skill/SKILL.md -text` under a comment saying exactly why), but VHS-28's recorded position is to avoid adding entries: it exercised CRLF by **constructing it in-test** (`tests/test_session_handoff.py:471`, `write_bytes(...replace("\n", "\r\n"))`). This spec follows that, so `tests/fixtures/.gitattributes` stays untouched.

### Files to leave alone

- `skills/spec-close/SKILL.md` outside the nine sites above. (Stated as one umbrella rule rather than a phase list: sites 26, 204, 309, 343, 365 sit in Phases 0, 3, 4, 5, 5 respectively, so any per-phase carve-out is either redundant or misleading.)
- `.gitattributes`, root and `tests/fixtures/` — see above. Named explicitly so the choice reads as deliberate.
- `sync.py`, `lint.py` — unchanged. `sync.py`'s `SUBTREES = ("skills", "agents")` walks recursively via `iter_files`, so `skills/spec-close/scripts/` mirrors to the config dir with no change. That walk has no exclusion list, so running the tests will also mirror a `__pycache__/` directory beside the script — pre-existing behavior (the VHS-28 precedent already puts three `.pyc` files under `session-handoff/scripts/__pycache__/`), accepted, not addressed here.
- `wiki-after-merge` and `wiki-state-update` (wiki repo, under `.claude/skills/`) — both already prepend correctly.
- Historical `log.md` entries — the file is in contract today.

### Out-of-repo change (tracked here, shipped separately)

- `vigil-harbor-wiki/log.md` header sentence — see § Wiki-side step.

## Decisions

### D1 — Ship a script, not prose

*Carried from the brief (Devin, 2026-08-25).*

`skills/spec-close/` ships `SKILL.md` and nothing else today, so this is the skill's first script. The reason is acceptance criterion 4: a prose instruction has no behavior to test. The strongest thing a doc-only fix can pin is its own wording — and the entire point of this ticket is that a naive fix *passes* every test that does not run against a real `log.md` header. Behavior needs a callable.

This matches the repo's stated principle that only deterministic gates earn a script (VHS-28's "two scripts, not four"). Locating a byte offset with a regex that must not match one specific sentence in one specific file is a deterministic gate.

### D2 — The anchor is line-anchored on a real date, and nothing else

The insertion anchor is the first match of:

```python
ENTRY_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] ", re.M)
```

Three exclusions, each load-bearing against the header's format sentence:

- **`^` under `re.M`** — the sentence carries `## [YYYY-MM-DD]` mid-line, preceded by `Format: ` and a backtick. A line-start requirement excludes it structurally, not by luck.
- **`\d{4}-\d{2}-\d{2}`** — the literal `YYYY-MM-DD` in that same sentence is alphabetic, so even a hypothetical line-start occurrence would not match.
- **Trailing space** — every real entry heading has one; it costs nothing and rejects a bare `## [2026-08-25]` with no payload.

All three exclusions would have to fail simultaneously for the header sentence to be selected. The **header-corruption** test case pins the exact header text that breaks the naive `index("## [")` form.

`ENTRY_RE` has two jobs, and both matter: it finds the anchor on **read** (D7), and it validates the entry's own heading on **write** (D5). A narrow anchor is only safe if the entries this script writes are guaranteed to match it.

### D3 — No markdown parsing

*Consistent with VHS-28 D0 ("the validator does not parse markdown").*

The script does one line-anchored regex search over the file text. It does **not** mask fenced code blocks, track HTML comments, or otherwise model markdown structure.

The residual exposure is a fenced example entry in the header — a ```` ``` ```` block containing a line-start `## [2026-01-01] …` — which would be selected as the anchor and split the fence. This is accepted, not overlooked:

- `log.md`'s header contains no fence. Its one format reference is *inline* code inside a sentence, which is exactly the case D2 excludes.
- Fence masking would be the first step toward a markdown parser inside a skill script, which VHS-28 explicitly retired after it dragged in a terminator scan, thematic-break handling, and a subtree fallback.
- The failure is loud (a broken fence in a reviewed file), not silent, and the wiki header is a fixed, machine-shaped block that no close run edits.

If a fenced example is ever added to the header, that is the moment to revisit — not now. Recorded in § Out of scope.

### D4 — The idempotency guard moves into the script

Today the guard is a prompt-level `grep -F "close | <PROJECT> — <TICKET-ID>:"` run before a separate write. Moving it into the script makes check-and-insert one operation, so an interrupted run cannot land a duplicate between the check and the write, and the test suite can pin the guard rather than trusting an agent to run a grep first.

The matching rule against the **existing file** is byte-identical to today's:

- Literal substring match (`in`), never a regex — the guard string contains `|`, which a regex would read as alternation.
- Whole-text search, exactly as `grep -F` searches every line.
- The `close |` prefix stays — it distinguishes close entries from `wiki-after-merge`'s merge entries, which also carry the ticket ID.
- The trailing colon stays load-bearing — without it, closing `<PROJECT>-1` after `<PROJECT>-11` false-matches and silently skips the entry.

**The whole-text search is deliberately kept, and it carries a known asymmetry.** The entry-side check below is first-line-only; the existing-text search is not. A guard literal quoted inside some earlier entry's *body prose* would therefore suppress a legitimate new entry. Accepted, because narrowing it would change dedup semantics against every entry already in the file — and verified low-risk: every `close | ` occurrence in the live `log.md` is an entry heading, none is body prose. If it is ever narrowed, the natural form is to search only lines matching `ENTRY_RE`.

**Guard shape.** The guard is supplied by the caller via `--guard`, so `SKILL.md` keeps the documented literal as the single source of truth for its shape. The script validates two properties rather than trusting the caller blindly, because both failures would otherwise land on exit 1 — the silent-loss code:

- It must end with `:`. That is the property D4 names as preventing the `VHS-1` / `VHS-11` false match, and an unresolved template or a truncated guard is exactly what an over-broad match looks like.
- It must appear in the entry's **first line** — not merely somewhere in the entry. Close entries routinely quote sibling tickets in body prose (the live VHS-28 entry names several), so a whole-text check would pass on a guard that describes a different entry than the one being written.

- It must not still contain `<` or `>`. The colon check catches a *truncated* guard but is blind to an *unsubstituted* one: `close | <PROJECT> — <TICKET-ID>:` ends with a colon and appears in the first line of an entry built from the same template, so both other checks pass and a literal-placeholder entry lands permanently at position 1. Message: `guard still contains an unresolved placeholder: <guard>`.

All three failures exit 2, never 1.

**Em-dash sensitivity survives the move.** The guard literal contains `—`; any tool that normalizes it to `--` breaks dedup and produces duplicates on re-run. That hazard is unchanged by D4 — only its mechanism moves from `grep -F` to the script's `in` compare. `SKILL.md:396` is reworded accordingly rather than deleted, and D6 pins the encoding that makes the compare reliable.

### D5 — Entry text arrives on stdin; the script writes the file

Close entries are multi-paragraph prose (the VHS-28 entry runs several hundred words). A CLI argument is the wrong carrier for that, and a scratch file would add a mutation the skill's Phase-5 boundary would then have to account for and clean up. Stdin carries it with neither cost.

The script owns the write. The alternative — emit merged text to stdout for the skill to `Write` — makes the guard advisory (the skill could ignore a skip signal and Write anyway) and doubles the whole file through the agent's context on every close. Line 381's Write-targets bullet is updated to say so.

**No `--dry-run`.** An earlier draft carried one with no caller. VHS-28's shipped principle — surface with no caller becomes a prompt-driven step, not shipped code — applies directly; an operator wanting a preview can run the script against a copy. Dropped.

**CLI surface.** The `<…>` tokens are placeholders the caller substitutes before invoking — D4's third guard check rejects a guard that still contains them, and D5's heading validation rejects a literal `YYYY-MM-DD`. What must be written exactly is the **structure**: the variable indirection, both quotings, the delimiter, and the exit capture.

```bash
if "$PY" "$SCRIPT" "$LOGPATH" --guard 'close | <PROJECT> — <TICKET-ID>:' <<'PREPEND_LOG_ENTRY_EOF'
## [YYYY-MM-DD] close | <PROJECT> — <TICKET-ID>: <title>

<body>
PREPEND_LOG_ENTRY_EOF
then rc=0; else rc=$?; fi
echo "prepend_log_entry_exit=$rc"
```

Four details are load-bearing; none is cosmetic. Each has a named failure mode, and three of the four fail **silently or misleadingly** rather than loudly.

- **The guard must be single-quoted.** It contains ` | ` by construction. Unquoted, bash splits it into a pipeline: the script receives `--guard close` (no trailing colon → exit 2 with a message that blames the guard) and the shell then tries to run `VHS` → `command not found`. The literal contains no single quote, so single-quoting is total.
- **The path must be double-quoted, and expanded — `$HOME`/`$CLAUDE_CONFIG_DIR`, never `~`.** Two separate traps. (a) An unquoted Windows path (`C:\Users\...\log.md`) has its backslashes consumed as escapes, yielding `C:Users...log.md` — a *relative* path that does not exist, which takes the **missing-file outcome**, creates a stray `log.md` in the *target repo's* cwd, and exits **0** — reported as a creation rather than a failure, which is why that notice must carry the resolved path. Python accepts `/` on Windows. (b) **Bash does not expand a tilde inside double quotes** — verified: `test -f "~/.claude/skills/spec-close/SKILL.md"` is false for a file that exists, while `"$HOME/..."` is true. Since D9's pre-check and this invocation both quote the path, a `~`-rendered path makes the pre-check report not-found for an installed script and the entry is never written. `%USERPROFILE%\...` fails the same way in Git Bash — no expansion *and* consumed backslashes. See D9 for how `$SCRIPT` and `$LOGPATH` are built.
- **The heredoc delimiter must be one prose cannot produce.** Quoting (`<<'…'`) suppresses *expansion*, not *termination*. A body line equal to the delimiter ends the entry there — verified: the remainder is then handed to the shell as commands, in a tree the close has already `git mv`'d. The truncated entry is still structurally valid (correct heading, guard in the first line), so every validation passes and it lands at the top reporting success. Close-entry bodies are hundreds of words of agent-composed prose over quoted headings and table fragments, so `ENTRY` or `EOF` are reachable; `PREPEND_LOG_ENTRY_EOF` is not.
- **The exit capture must survive `set -e`.** A bare `python …; echo "…=$?"` loses the value under a `set -e` shell precisely on the two paths where it matters — exit 1 and exit 2 both terminate the shell before the `echo`. Wrapping the call in an `if` condition suspends `set -e` for it.

**Input validation, in order.** Each failure exits 2 and writes nothing:

1. **No stdin attached** — `sys.stdin is None` or `sys.stdin.isatty()`. Without this the script blocks on `read()` until an EOF that never arrives, hanging the close for the harness's full Bash timeout with the archive moves of step 3 already applied. "Empty stdin" (a pipe that closed with zero bytes) and "no stdin" (no pipe at all) are different conditions and are checked separately. Message names the heredoc form. *Platform note for the test author: on Windows, `NUL` is a character device and `isatty()` returns **True** for it, so `< /dev/null` reaches this branch there and the empty-entry branch on POSIX.*
2. **Empty entry** after decode, newline-normalize, BOM-strip, and `.strip()`.
3. **Guard shape** — non-empty, ends with `:`, present in the entry's first line (D4).
4. **Entry heading shape** — `ENTRY_RE.match(entry)` must match at offset 0. This is the write-side mirror of D7's read-side refusal, and it is not optional: an entry written as `## [2026-8-5] …`, `### [2026-08-25] …`, `## [2026-08-25]close | …`, or with a tab after the `]` satisfies every check above, lands at the top, and exits 0 — and then the *next* close's anchor skips it and inserts the newer entry **underneath** it. The file silently leaves newest-first contract, no refusal fires (real entries still exist, so D7's refusal never triggers), and nothing prompts a re-sort. That is the VHS-29 bug re-entering through the write side, one run later. Message: `entry heading does not match the log format '## [YYYY-MM-DD] …' — refusing to write an entry the anchor cannot find: <first line>`.

**Exit codes.** Exactly three, and 1 is reserved:

| Code | Meaning | `SKILL.md` behavior |
|---|---|---|
| 0 | Entry written; `prepend_log_entry_outcome=prepended` | Report `Prepended: log.md` |
| 0 | Entry written; `prepend_log_entry_outcome=fresh` or `=created` | Surface D7's stderr notice verbatim **instead of** `Prepended:` — never a paraphrase, so the operator reads the resolved path and what actually happened |
| 1 | **Only** — the guard string is already present in the existing file; nothing written | Report `log.md: entry already present — skipped` |
| 2 | Everything else: any of the four validations, any I/O failure on read **or write**, an unmatched anchor in a populated file (D7), a concurrent change (D8), an unresolved script path, or any unexpected exception | Surface stderr verbatim; report `log.md NOT written` |

**Exit 0 is three outcomes, so the script prints `prepend_log_entry_outcome=prepended|fresh|created` on stdout.** The report line depends on which one, and "was stderr empty?" is not a value the caller holds — it is a judgement over interleaved tool output that one stray `DeprecationWarning` inverts. A machine-readable token on stdout is the same device D5 already uses for the exit code, costs one `print`, and is directly assertable. The human-facing notice stays on stderr.

**The skill branches on the echoed integer, never on the harness's success/failure signal.** This is the file's first three-way exit branch; a harness reports only pass/fail, so 1 and 2 both read as failure and a correctly-skipped idempotent re-run — an *expected* path, per `SKILL.md`'s own "Interrupted execute" and "Partial-then-full re-run" failure modes — would be reported as `log.md NOT written` with a spurious recovery hint. Hence the `if`-wrapped capture and `echo "prepend_log_entry_exit=$rc"` shown in the CLI-surface block above. **`$?` after `fi` is not an equivalent shorthand — it is always `0`.** Both branches of the `if` end in an assignment, and a compound command returns the status of the last command in the taken branch, so `fi` reports success on every path. Verified: `if python -c 'sys.exit(2)'; then rc=0; else rc=$?; fi` leaves `rc=2` and `$?=0`. Writing `$?` there would print `prepend_log_entry_exit=0` for a refusal, a skip, and a `PermissionError` alike — the branch would read success forever. Any value other than 0/1/2 takes the exit-2 branch.

**127 means a missing *interpreter*, not a missing script.** Measured: `python <nonexistent>.py` prints `can't open file …: [Errno 2]` and exits **2**; only a missing interpreter yields the shell's 127. Both are failures and both land on the exit-2 branch, so behavior is right either way — but because a missing script is indistinguishable by exit code, D9's install hint is emitted from an explicit pre-check, not inferred from a code.

The reservation of 1 is a hard requirement, not a convention: CPython exits **1** on any uncaught exception, so an unguarded `PermissionError` on the write would be reported to the operator as *"entry already present — skipped"*. The close would then print a successful-looking completion block over a `log.md` that was never written, and the documented re-run path would skip it again for the same reason. `main()`'s body is therefore wrapped in a `try/except BaseException` → message to stderr → `return 2`, with **`KeyboardInterrupt` and `SystemExit` both re-raised after cleanup**. `SystemExit` matters because argparse raises it: `SystemExit(0)` for `--help` and `SystemExit(2)` for a usage error, each already carrying its own output. Swallowing them would make `--help` print help, then an error, then exit 2 — on a script D5 expects operators to run by hand. Neither re-raised code collides with the reserved 1 (an uncaught `KeyboardInterrupt` exits 130).

**Every failure message — exit 1 and exit 2 — names the resolved absolute path and the `--guard` literal.** (D7's two exit-0 notices carry the path only: no guard is implicated in placing or creating a file, and D5's table surfaces them verbatim, so they cannot grow a clause.) `/spec-close` surfaces stderr verbatim and nothing else, so that message is the entire evidence trail; `log.md changed under us` read months later in a transcript with no path and no ticket is not debuggable. Concretely: `entry already present in <path> (guard: <guard>) — skipped`; `<path> changed under us between read and replace (guard: <guard>) — re-run`. The catch-all arm follows the same rule — `<path> (guard: <guard>): unexpected failure: <type>: <exc>` — with one carve-out: a failure raised before argparse completes has neither value available and emits the exception alone.

**A failed log write never aborts the close.** Phase 5 step 3 has already `git mv`'d every spec artifact from `TODO/` to `DONE/`, across two repos neither of which is committed. Halting before the completion block would leave the operator with no `Archived:` line, no commit suggestions, and no re-run instruction over a half-mutated tree — the precise state `SKILL.md`'s "Interrupted execute" failure mode exists to make recoverable. So on exit 2 the skill continues to step 5 and prints the completion block with `log.md NOT written: <stderr>` and the recovery (`re-run /spec-close <DONE-path>` — the guard makes the retry idempotent). D9's not-found case follows the same rule.

### D6 — Encoding, newlines, and BOM are pinned explicitly

Four hazards, all silent, all live on Windows with `cp1252` as the locale encoding:

1. **File text.** The guard contains an **em dash** (`—`). Python's default text encoding on Windows is the ANSI codepage, so an unqualified `open()` mangles it on read *and* write. Every file open passes `encoding="utf-8"`.
2. **stdin.** Read via `sys.stdin.buffer.read().decode("utf-8")` — never the text wrapper, whose encoding is likewise locale-derived. **Strict, deliberately:** the two in-repo precedents (`_sections.normalize`, `lint._read_lines`) decode with `errors="replace"`, which is right for *inspecting* a file. This entry lands permanently in the wiki's operations log, so a mojibake'd entry should be refused, not silently written with U+FFFD in it. The resulting `UnicodeDecodeError` reaches D5's guard as a clean exit 2.
3. **stdout / stderr.** Both are reconfigured to `encoding="utf-8", newline="\n"` before any output. Measured on this repo's interpreter (Python 3.14, Windows, stdout piped — how every harness and every `subprocess` test sees it): `sys.stdout.encoding` is `cp1252` with `errors="surrogateescape"`, so an unqualified `print` emits transcoded cp1252 bytes with CRLF. Since D5's messages echo the `--guard` literal, every one of them carries an em dash by construction. PEP 686's UTF-8 default lands in 3.15, not 3.14.

   **The reconfigure is best-effort and outside the failure semantics** — `reconfigure` is a `TextIOWrapper` method, and `main()` may be called in-process with `sys.stdout` replaced by an `io.StringIO` (`contextlib.redirect_stdout`, `unittest -b`). Left unguarded, that `AttributeError` is caught by D5's exception guard and returns **2** — which is the exact value most tests assert as their failure signal, so a test could pass having never reached the code it exists to exercise. It is therefore wrapped in its own `try/except (AttributeError, ValueError): pass`, and every exit-2 case asserts the distinguishing **stderr text**, not the code alone.
4. **Newlines, on both sides.** `log.md` is LF-terminated (the wiki's `.gitattributes` is `* text=auto eol=lf`, and the live file has zero `\r`).
   - **Read.** `open(path, encoding="utf-8", newline="")` — *not* the default `newline=None`, whose universal-newline translation silently converts every `\r\n` to `\n` in memory, so the LF write then rewrites the whole file.
   - **Write.** `newline="\n"` (matching `create_handoff.py:347`), so nothing the script did not author is re-terminated.
   - **Entry text.** Decoded from `sys.stdin.buffer` with no newline handling of its own, so a caller piping from a Windows-native tool would embed literal CR bytes into an LF file. The decoded entry is normalized (`replace("\r\n", "\n").replace("\r", "\n")`), then BOM-stripped, then `.strip()`ed — that order, stated identically in D7 and § Design.

**Preservation, stated exactly.** The script splices text and does not re-terminate lines it did not author — **with one bounded exception**: the single line immediately above the insertion point. D7's separator normalization right-strips the preceding text and re-emits `\n\n`, so on a CRLF file that one boundary line's terminator becomes LF. This is a deliberate, named consequence of the blank-line rule, not an accident; the wiki is pure LF so it never fires in production, and the **newlines** case asserts *that specific line's* terminator rather than a blanket "untouched lines" claim that would be self-immunizing.

**A BOM on the existing file is preserved, and made invisible to the anchor.** The read opens `utf-8`, not `utf-8-sig`, and nothing strips it — the BOM sits before the anchor, and the splice touches no byte before the anchor. But both patterns are `re.M`-anchored on `^`, so a BOM that *immediately precedes an entry heading* defeats them on that line only, and the failure is silent in both directions. Measured: a headerless BOM'd file with two entries anchors on entry **2** and splices the new entry into second place, exit 0; with one entry neither pattern matches, so it takes the fresh-wiki row and lands at the **end** of a file that demonstrably has an entry — contradicting D7's own guarantee. (With `log.md`'s real header the BOM precedes `# Wiki Log` and is inert, so this never fires on the live file; the reachable shape is a second close against the bare file the missing-file outcome creates.)

Rather than reason about which shapes are safe, a leading BOM is detached before matching, the splice is performed entirely in the stripped coordinates, and the BOM is re-attached to the result. The BOM is preserved byte-for-byte and cannot influence the anchor. Detach-and-reattach rather than shift-the-offsets, deliberately: splicing in the original text at a shifted offset leaves `"﻿"` as the "text preceding the anchor", and since `'﻿'` is not whitespace, `.strip()` keeps it — so D7's degenerate rule (no leading separator when the preceding text is empty) would never fire on a BOM'd file and the result would open with a spurious blank line. In stripped coordinates the two rules compose with no extra clause.

**BOM on the entry.** `'\ufeff'` is not whitespace, so `.strip()` leaves it in place. A BOM-prefixed entry writes a first line of `\ufeff## [2026-08-25] …`, which `ENTRY_RE` cannot match — caught by D5's heading validation, but stripping it is the correct fix rather than rejecting a recoverable input. BOM is a known live hazard in this repo; `tests/fixtures/bom-skill/` exists because `lint.py` had to handle it.

**On re-implementing the normalizer.** Decode, fold newlines and strip the BOM is the same operation as `skills/session-handoff/scripts/_sections.py:76` `normalize()` — which orders the last two the other way round, immaterial since folding never creates or moves a leading BOM — and `lint.py:63` `_read_lines` is a third instance of the decode-then-BOM-strip pair. Neither is importable here: skills install independently under `<config-dir>/skills/<name>/`, and `sync.py`'s `SUBTREES` is `("skills", "agents")`, so repo-root `lint.py` never reaches the config dir at all. The sequence is therefore re-implemented deliberately — same reasoning as D8's note on `write_atomically()` — with the strict-decode divergence recorded above rather than left to look like an oversight.

### D7 — Four outcomes, and an unmatched anchor is a refusal

| Outcome | Condition | Behavior | Exit |
|---|---|---|---|
| **Normal** | `ENTRY_RE` matches | Insert `<entry>\n\n` immediately before the match's line start | 0 |
| **Refuse** | No `ENTRY_RE` match, but `^#{2,6} *\[` matches somewhere | Write nothing; stderr: `<path> (guard: <guard>): no line-anchored dated entry found, but <n> heading-like line(s) present — first is line <k>: <text> — refusing to write` | 2 |
| **Fresh wiki** | No `ENTRY_RE` match and no heading-like line at all | Place the entry after the existing content; stderr notice `<path>: no dated entry found — entry placed at end of file` | 0 |
| **Missing file** | Path does not exist | Create it containing the entry alone; stderr notice `<path> did not exist — created with this entry alone; no header synthesized` | 0 |

**The refusal row is the important one.** An earlier draft had a single "no match → put it at the end" fallback. That is precisely the VHS-29 bug wearing a green success report: a populated `log.md` whose newest heading is `### [2026-08-25] …` (a hand edit), or `## [2026-8-5] …`, or carries a tab after the `]` — every one of D2's three deliberate narrowings is also a new way to miss (a BOM is handled upstream by D6's offset match, not by this row) — would get its entry appended at the bottom of a newest-first file, exit 0, and print `Prepended: log.md`, with the manual re-sort no longer even prompted. Splitting on evidence rather than assumption means the fresh-wiki path is taken only by a file that demonstrably has no entries, and everything else is a loud stop. D5's heading validation is the same rule applied to the write side.

**Missing-file rationale:** the script does *not* synthesize a header. A header would have to assert the rotation boundary ("This file holds entries dated 2026-08-01 and later") and name `log-archive.md`, neither of which the script can know. Writing a bare entry is the honest minimum; whoever creates a fresh wiki writes its header.

**Whitespace discipline** (pinned by test):

- The entry text is newline-normalized, BOM-stripped, then `.strip()`ed before use.
- Normal outcome: the text preceding the anchor is normalized to end with exactly one blank line (`\n\n`), then `<entry>\n\n` is inserted. Result: one blank line above the new entry, one between it and the previously-newest entry. (This is the one boundary-line re-termination D6 names.)
- Fresh-wiki outcome: existing content is right-stripped, then `\n\n<entry>\n` follows it.
- Missing-file outcome: `<entry>\n`.
- **Degenerate inputs:** when the preceding text (normal outcome) or the existing content (fresh-wiki outcome) is empty after stripping, **no leading separator is emitted** — the entry starts at byte 0. Without this, a `touch`ed `log.md`, or a second close against the file the missing-file outcome created, opens with two blank lines.
- **Tail, scoped honestly.** The fresh-wiki and missing-file outcomes leave the file ending in exactly one `\n` — they author the tail. The **normal outcome leaves the tail byte-identical**, including a missing or doubled trailing newline, because it splices at the top and touches nothing after the anchor. An earlier draft claimed the one-`\n` invariant for all three; enforcing that on the normal outcome would mean rewriting bytes the script did not author, contradicting D6. `log-no-trailing-newline.md` exists so this is pinned rather than incidental.

The word "append" is deliberately absent from this table and from the Phase 5 step 4 prose that transcribes it — the **no-stale-wording** case asserts zero occurrences in `SKILL.md`, and a correct implementation must not trip its own tripwire.

### D8 — The write is atomic, and a concurrent change is detected

The script rewrites 100% of `log.md`'s bytes to insert one entry, and `log.md` holds every wiki entry since the 2026-08-01 rotation boundary (514 lines / ~146 KB today). A plain `open(path, "w")` truncates to zero *before* writing anything, so an interrupt, `ENOSPC`, or any exception in that window leaves the file empty or half-written — and a truncated file that lost its `## [` headings then lands on D7's refusal path (loudly) or, worse, its fresh-wiki path if it lost *everything*. Recovery has no clean checkpoint: `/spec-close` deliberately leaves the wiki uncommitted (`SKILL.md` Phase 5 step 5), so by the time `log.md` is written the wiki tree already carries unstaged decision, comprehension, and `state.md` changes.

**Sequence** — one ordered block:

```
open(path, encoding="utf-8", newline="") → read()
  → baseline = os.fstat(handle.fileno())        ← on the handle, not the path
  → close
[guard check, splice]
mkstemp(prefix=".prepend-log-entry.", suffix=".md.tmp", dir=<log.md's own directory>)
  → os.fdopen(fd, "w", encoding="utf-8", newline="\n") → write → flush → os.fsync → close
  → os.chmod(temp, <mode>)
  → re-stat and compare against the baseline    ← the last thing before the swap
  → os.replace(temp, target)
```

This reuses the shape of `skills/session-handoff/scripts/create_handoff.py:338` `write_atomically()`. Closing the descriptor before the replace is required on Windows, where an open *source* handle blocks `os.replace` exactly as an open target handle does; that precedent carries an inline comment saying so.

Four details the precedent does not supply, because it creates a new file where this one replaces an existing tracked file:

- **The baseline comes from `os.fstat` on the read handle, not `os.stat` on the path.** If another writer lands its own `os.replace` while our `read()` is in flight, POSIX rename swaps the inode: our handle finishes reading the *old* file, but a post-read `stat(path)` would return the *new* file's `st_mtime_ns`/`st_size`. That value would become the baseline, the re-check would match, and we would replace the file with a splice of stale content — silently dropping the other writer's entry, the exact unrecoverable case this check exists to prevent. `fstat` on the handle makes the baseline describe the bytes actually in hand.
- **The dot prefix is load-bearing, not cosmetic.** `vigil-harbor-wiki/.gitignore` carries `.*.tmp` (added for INFRA-27's plane-sync residue), and `SKILL.md:370` tells the operator to commit the wiki with `git add -A`. Without the leading dot, any leaked temp — a ~146 KB copy of `log.md` — gets staged and committed.
- **Cleanup covers the non-exceptional aborts too.** The whole sequence is wrapped in `try/finally` with `temp_path.unlink(missing_ok=True)`, not only `except BaseException`. The stat-mismatch abort is a plain `return 2`, so an exception-only cleanup would never fire on the one path most likely to leak.
- **Mode is set on both paths.** `tempfile.mkstemp` creates at `0600` by design, and `os.replace` would carry that onto `log.md` — silently making the wiki's operations log owner-only on POSIX. Git does not track non-exec mode bits, so this would never appear in a diff or survive a clone: a working-tree-only, one-way change. When the target exists, its `st_mode & 0o777` is captured with the baseline and re-applied. When it does not, the temp is chmod'd to `0o666 & ~umask` so a created `log.md` matches what a plain `open(path, "w")` would have produced. The stdlib has no umask *getter* — `os.umask()` is a setter returning the prior value — so read it with the standard `old = os.umask(0); os.umask(old)` set-and-restore; the script is single-threaded, so the window is safe.

**Concurrency.** `log.md` genuinely has two writers — `/wiki-after-merge` prepends to it as well — plus an operator's editor, on a shared working tree. A read-then-whole-file-write with no check loses an interleaved write silently, and because the loser's entry is gone the guard will not detect the loss on any later run either. The baseline is re-checked immediately before `os.replace`:

- **File existed:** `st_mtime_ns` and `st_size` from the read handle. Mismatch → exit 2. A re-stat that raises `FileNotFoundError` — the target was deleted or rotated away mid-run — is treated as a mismatch and takes the same `changed under us` message, not the catch-all's `unexpected failure`.
- **File absent:** the baseline is *absent*. `os.path.exists(path)` is re-checked; if the path has appeared, exit 2 with the same message. Without this the missing-file outcome is the one path where the detection does not apply, and a concurrently bootstrapped `log.md` would be clobbered with no signal.

This is detection, not locking: it closes the window this script actually opens, and does not pretend to serialize two concurrent writers. Locking is named in § Out of scope.

**On duplicating `write_atomically()`.** A deliberate second implementation, not an oversight. Skills install independently under `<config-dir>/skills/<name>/` and share no importable module — `sync.py`'s `SUBTREES` mirrors per-skill trees with no common package path — and `create_handoff.py`'s signature is welded to its claim-file reservation protocol, which this script has no use for. The pointer to the precedent is kept so the two stay comparable.

### D9 — Script resolution: the skill directory, never `project_root`

`/spec-close` runs with cwd = the **target** repo — Dynasty, the MCP server, any repo with `docs/specs/` — which is normally *not* `vigil-skills`. An invocation written as `python skills/spec-close/scripts/prepend_log_entry.py …` resolves only when closing a vigil-skills spec: it would work for VHS-29's own close run and fail everywhere else, with CPython's `can't open file` on stderr and exit 2.

`SKILL.md` refers to the script by skill-relative name — `scripts/prepend_log_entry.py` — matching `session-handoff`'s precedent of leaving resolution to the harness, and states the rule explicitly: **the path is resolved relative to the installed skill directory, never relative to `project_root`.** Phase 5 step 4 resolves the interpreter into `$PY` alongside the paths (below) rather than hardcoding a name, because the invocation block is transcribed verbatim and `python` is absent from `PATH` on a stock Debian/Ubuntu host — every close there would return 127. The probe tests **executability**, not presence: on Windows, `%LOCALAPPDATA%\Microsoft\WindowsApps\python3.exe` exists as an App Execution Alias stub whether or not Store Python is installed, so a presence-only check binds `$PY` to a stub that prints "Python was not found" and exits 9009 without reading stdin — a loud failure, but one whose message blames Python while the real script sits installed and a working `python` sits on the same `PATH`. Note also that the two names need not be the same interpreter: measured on the operator machine, `python3` is the WindowsApps alias at 3.13.14 while `python` is 3.14.3. Both satisfy the stdlib-only requirement, and D6's encoding measurements were re-taken under 3.13 and hold, but the spec does not assume the names are interchangeable. Naming the interpreter at all is deliberate: the script ships mode 644 with a shebang but no exec bit, and Git Bash on Windows — the shell `SKILL.md:380`'s tool-use notes assume — does not dispatch a bare `.py` path.

**Resolution order** is `$CLAUDE_CONFIG_DIR` → `~/.claude` (`%USERPROFILE%\.claude\` on Windows), matching `sync.py:36`, which resolves the install dir as `--claude-dir` → `$CLAUDE_CONFIG_DIR` → `~/.claude`. A rule that ignored the env var could point at a directory `sync.py install` never wrote to.

Phase 0 step 4 currently names only the two default locations for `states.json` and does **not** honor `$CLAUDE_CONFIG_DIR`. Rather than ship one file with two different config-dir rules — the same class of drift this ticket exists to fix — that line is brought along (site 26 in § Scope). It is a nine-word change with no behavioral risk: the env var is unset on the operator machine, so both readings resolve identically today.

The trade is worth naming. `states.json` is read by three skills — `spec-close:26`, `ship-spec:41`, `spec-cycle:235` — all stating the same two-default rule today, and no skill in the repo mentions `$CLAUDE_CONFIG_DIR` (only `sync.py` and `README.md` do). Site 26 makes `spec-close` the first, so on a machine with the env var set the three phases of one lifecycle would disagree about where their shared config lives. Sweeping all three is a separate ticket, filed rather than done here, because nothing sets the variable today and widening this spec's blast radius to two more skills is the larger risk.

**The path is built into a shell variable, expanded, never tilde-rendered.** Phase 5 step 4 opens by resolving the script once:

```bash
SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-close/scripts/prepend_log_entry.py"
LOGPATH="<wiki_root>/log.md"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
```

`${CLAUDE_CONFIG_DIR:-$HOME/.claude}` is the resolution order above, in one expansion that works quoted. Writing `~` or `%USERPROFILE%` here is the trap D5 names: both are inert inside the double quotes every later use requires.

**Not-found is detected by an explicit pre-check, not by an exit code.** Step 4 then runs `test -f "$SCRIPT"` before invoking. On failure it prints `log.md NOT written: prepend_log_entry.py not found at $SCRIPT — install with 'python sync.py install'` and, per D5, the close still runs step 5 and prints its completion block. The pre-check exists because a missing script and a refusing script both exit 2, so the actionable install hint cannot be inferred after the fact.

**Bash only, deliberately.** An earlier draft carried a second PowerShell here-string form, on the reasoning that `AGENTS.md` declares harness-neutrality and `SKILL.md` pairs shell forms elsewhere (Phase 0 step 3's `$env:USERNAME` / `$USER`). It is withdrawn, because a partial pairing is worse than none:

- **Windows PowerShell 5.1 pipes ASCII.** `$OutputEncoding` defaults to `ASCIIEncoding`, so a here-string piped to a native executable delivers the em dash as `?`. The guard reaches argv intact (UTF-16 command line), so D5's first-line check then fails on *every* close through that form, reporting a guard mismatch that is really a shell encoding default. This is `SKILL.md:396`'s own documented hazard, realized by the workaround meant to improve portability.
- **Neither control-flow mechanism ports.** `$?` is a `[bool]` in PowerShell, not the exit code (`$LASTEXITCODE` carries it), so D5's three-way branch silently collapses to pass/fail and an *expected* idempotent skip reads as a failure. `test -f` is not a PowerShell command at all, so the pre-check errors and takes the not-found branch on an installed script.

Fixing all three is possible but ships an untested second path — no test case can drive a PowerShell host from this suite. The rest of `SKILL.md` is already Bash-shaped throughout (`git log --grep`, `grep -rlw`, `sed`, `git mv`, the Phase 0 origin-sync probes at `:380`), so requiring Bash for this one step adds no constraint the skill did not already have. Recorded in § Out of scope with the `$OutputEncoding` finding, so a future PowerShell pairing starts from the evidence rather than rediscovering it.

### D10 — `requires:` block added to the frontmatter, declared against what the skill actually does

`lint.py` currently reports `WARN [missing-requires]` for `skills/spec-close/SKILL.md` (0 errors, 1 warning). D1 makes the shell dependency real, so the declaration is newly load-bearing rather than missing paperwork:

```yaml
requires:
  shell: true
  filesystem: [read, write]
  network: true
  services: [issue-tracker?, shared-memory?]
```

Placed after `user_invocable:`, per `docs/portability-contract.md`'s position rule and matching `skills/spec-cycle/SKILL.md:5-10`. (`lint.py` validates the block's content but not its position, so the rule is convention-enforced, not lint-enforced.)

Declared against evidence in the file, not against the minimum that lints:

- **`network: true`** — `SKILL.md:34` runs `timeout 30 git fetch origin`; `:74` runs `gh pr view <N> --json …` then `gh pr diff <N>`. `docs/portability-contract.md` defines `network: true` as "makes outbound network requests of its own." An undeclared `network` means a sandboxed harness pre-flights clean and then dies at Phase 2's `gh pr diff`, mid-close.
- **`services: [issue-tracker?, shared-memory?]`** — Plane at `:379` (state list, work-item lookup) and the MCP memory server at `:378`. Both are `?`-optional: the failure-modes section carries "Plane ticket not in MCP memory. Warn and proceed" and the Plane-unreachable partial-or-abort gate, which is exactly the contract's degrades-gracefully semantics.
- **`subagents` genuinely absent** — `grep -in "subagent"` over the file returns nothing.

This matches `spec-cycle`, the contract's worked reference, minus `subagents`. `lint.py` validates the vocabulary but never under-declaration, so the fuller block lints identically to the thin one — which is why the **`requires:`-matches-the-body** case asserts the declared set against the tool-use notes rather than trusting the lint.

Clearing the standing WARN also retires `spec-close` from the tracked missing-`requires:` backlog at `docs/authoring-portable-skills.md:41`; that sentence is updated to name `ship-spec` and `review-pr` only.

### D11 — Scale is a non-factor

*Carried from the brief's `## Scale` declaration (`**Factor:** no`).*

One insertion, one file, one entry per close run. No batching, no fan-out, no accumulation. The scalability lens stays off, and the design adds no scale machinery. D8's concurrency handling is not a scale concern — it addresses a second *writer*, not a larger *volume*.

## Design

### `skills/spec-close/scripts/prepend_log_entry.py`

Stdlib only (`argparse`, `os`, `re`, `sys`, `tempfile`, `pathlib`). Shape follows `skills/session-handoff/scripts/`: shebang `#!/usr/bin/env python3`, mode 644 (shebang without an exec bit, as all three shipped scripts are); module docstring stating usage, outcomes, and exit codes; `from __future__ import annotations`; a `main(argv)` returning an int; `if __name__ == "__main__": sys.exit(main(sys.argv[1:]))`.

The file-transforming logic is a pure function so tests can drive every outcome without touching disk:

```python
ENTRY_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] ", re.M)
HEADINGISH_RE = re.compile(r"^#{2,6} *\[", re.M)

def splice(existing: str | None, entry: str) -> tuple[str, str]:
    """Return (new_text, outcome). `existing` is None when log.md is absent.

    A leading BOM on `existing` is detached before matching and re-attached to
    the result: every offset, separator and degenerate-emptiness decision is
    made in the stripped coordinates (D6), so the BOM neither moves the anchor
    nor counts as preceding content.

    outcome is one of: "prepended", "fresh", "created".
    Raises AnchorMissing when existing has heading-like lines but no dated entry.
    """
```

`main()`, in order: best-effort stream reconfigure (D6 hazard 3, in its own `try/except`) → parse args → stdin-attached check → read stdin as bytes, decode UTF-8 strictly, normalize newlines, strip BOM, `.strip()` → empty check → guard shape and first-line check → entry heading check → open the file with `newline=""`, read, `os.fstat` the handle for the baseline and mode, close → exit 1 if the guard is already in the existing text → `splice()` → the D8 write block, whose re-stat sits immediately before `os.replace` → print `prepend_log_entry_outcome=<outcome>` on stdout, **after** the successful `os.replace` so a failed write never leaves a `=prepended` token beside an exit 2 → exit 0.

The D5 exception guard wraps everything, with `KeyboardInterrupt` and `SystemExit` re-raised after cleanup — so argparse's own `--help` (0) and usage-error (2) codes pass through unaltered.

A directory at `<log-path>`, or a parent directory that does not exist, is an exit-2 error — the script creates a file, never a tree.

### `skills/spec-close/SKILL.md` — the nine sites

**Line 3 (frontmatter `description`).** `…archive spec artifacts from TODO/ to DONE/, and append to wiki log.md` → `…and prepend an entry to the wiki's newest-first log.md`. Everything else — the flag descriptions, "Supersedes the former two-step reconcile/retire flow", "Pair with /spec-cycle and /ship-spec" — is untouched, so the trigger phrasing that fires the skill is preserved. D10's `requires:` block is added to the same frontmatter, after `user_invocable:`.

**Line 26 (Phase 0 step 4).** The `states.json` path gains `$CLAUDE_CONFIG_DIR` ahead of the two defaults, so the file states one config-dir resolution rule (D9).

**Line 204 (Phase 3 coverage-model note).** The parenthetical `(grep -F "close | <PROJECT> — <TICKET-ID>:")` becomes a reference to the script's `--guard` check. The note's claim — that the guard prevents duplicates while letting the close entry coexist with `wiki-after-merge`'s merge entry — is unchanged and still true.

**Line 309 (close-plan template).** `Log.md append:` → `Log.md entry (prepended):`. The rendered entry below it is unchanged.

**Line 343 (Phase 5 step 4).** Rewritten. The prose states the contract and delegates the byte work:

- The guard literal and its two load-bearing properties (the `close |` prefix, the trailing colon) stay in the prose — the caller constructs the string.
- D9's resolution rule, the interpreter, the concrete Claude Code path, the `test -f` pre-check and its install-hint message.
- The four outcomes of D7, the exit-code mapping of D5, the `echo "prepend_log_entry_exit=$rc"` capture the three-way branch reads (never a bare `$?`, which after `fi` is always 0), and the `prepend_log_entry_outcome=` token the exit-0 report branches on, using the non-`append` phrasing D7 fixes, plus the rule that exit 2 never aborts the close.
- The `$SCRIPT` / `$LOGPATH` / `$PY` assignments (all three — the invocation reads `"$PY"`, and an omitted assignment expands to the empty string and fails at the shell), the `test -f "$SCRIPT"` pre-check, D5's Bash invocation verbatim (single-quoted guard, `PREPEND_LOG_ENTRY_EOF` delimiter, `set -e`-proof exit capture), and a sentence naming why each of the four is load-bearing. Bash only — see D9 on the withdrawn PowerShell form.

**Line 365 (completion output).** `Appended: log.md` → `Prepended: log.md` when stdout carries `prepend_log_entry_outcome=prepended`. On `=fresh` or `=created` the skill surfaces D7's stderr notice verbatim **in place of** that line, so a bottom-placement or a file creation is never reported as a prepend. It branches on the token, never on whether stderr was empty — D5 rejects that discriminator by name. The exit-1 line reads `log.md: entry already present — skipped`; the exit-2 line `log.md NOT written: <stderr>` followed by the re-run recovery.

**Line 380 (Bash tool-use bullet).** `` `grep -F` (idempotency check) `` is removed — no shell grep performs the log guard any more. `grep -rlw` / `grep -c` stay (duplicate detection and fast-path coverage checks, unrelated). The bullet gains the script invocation.

**Line 381 (Write-targets bullet).** `Write for the reconciliation report, wiki entries, and log.md` → Write for the reconciliation report and wiki entries; `log.md` is written by `scripts/prepend_log_entry.py`.

**Line 396 (`Log-guard encoding` failure mode).** Re-anchored: the em-dash dependency now attaches to the script's `--guard` substring compare rather than to `grep -F`, with D6's UTF-8 pinning named as what makes it reliable. The hazard itself is unchanged and the bullet stays.

### What does not change

Phase 1 row 8 (wiki unavailable → drop the log entry from the close plan), the Phase 3c compile step, the mutation-boundary bullet at line 382, and the `Interrupted execute` / `Partial-then-full re-run` failure modes describe *whether* an entry is written, not *where* or *by what*. They keep their current wording; the interrupted-execute bullet's "log idempotency guard" phrase remains accurate, since the guard still exists — only its mechanism moved.

### Wiki-side step

`vigil-harbor-wiki/log.md`'s header opens `Append-only record of wiki operations.`, which contradicts the newest-first rule three lines below it and reads as license for exactly this bug. Reword to `Running record of wiki operations.` The `Format:` clause in the same sentence is **not** touched — that is the half the fixtures depend on.

While on wiki master, `.claude/skills/wiki-after-merge/SKILL.md:37-38` carries the same class of drift in the opposite direction: its step heading reads `**Append log.md entry (idempotent).**` over an implementation at `:39` that correctly prepends. Optional to fix in the same commit; **not** an acceptance criterion, and no behavior changes either way.

Also stale after merge, and left to `/spec-close` and `/wiki-after-merge` rather than done here: `projects/vigil-skills/filemap.md` and the VHS-18 decision's Related line both record three tracked `missing-requires` WARNs; D10 makes it two.

Per repo convention (wiki changes merge direct on master, no PR), none of this is part of the vigil-skills PR. It is recorded here and in the ship-spec PR description as an operator step, and is acceptance criterion 6.

## Test plan

`tests/test_spec_close_log.py` — stdlib `unittest`, loading the script by file path via `importlib.util` exactly as `tests/test_session_handoff.py` does. Paths resolve from `__file__`, never cwd. **Every mutating case copies its fixture into a per-test `tempfile.TemporaryDirectory()` and operates on the copy** — the checked-in fixtures are read-only inputs and no case writes under `tests/fixtures/`. Without this, run 1 mutates `log-with-entries.md` in the working tree and run 2's idempotency case exits 1 where it expects 0, with `/ship-spec` green on the first pass and a corrupted fixture in the PR.

**Division of labour.** Unit cases drive `splice()` directly. Process-level cases *that need no interposition* go through `subprocess` with the script's real argv. Cases that must act **between** the script's read and its write drive `main()` in-process — `subprocess` gives no seam — using:

- a `sys.stdin` stub exposing `isatty() -> False` and a `.buffer` over an `io.BytesIO` of UTF-8 entry bytes. Both halves are required: the precedent helper (`tests/test_session_handoff.py:91` `run_main()`) redirects stdout/stderr but leaves `sys.stdin` alone, which under `python -m unittest` in a terminal is a tty — so D5 step 1 would fire and *every* such call would exit 2 before reaching the code under test; and `io.StringIO` has no `.buffer`, which D6 hazard 2 requires, so a naive fake raises `AttributeError` into the catch-all and also exits 2. Both give a green-looking "exit 2" for the wrong reason.
- a named seam patched with `unittest.mock.patch.object` over the module's `splice` (or `os.fsync`), matching `tests/test_session_handoff.py:567`, which patches `os.replace` with `side_effect=OSError` for exactly this purpose.

**Assert the message, not just the code.** Exit 2 is the catch-all for validation, I/O, refusal, and concurrency, so a case asserting only `returncode == 2` can pass having never reached the code it exercises — the stdin and `reconfigure` traps above are live examples. Every exit-2 case additionally asserts its distinguishing stderr text.

### Fixtures

`tests/fixtures/spec-close/log-with-entries.md` reproduces the real header — the `# Wiki Log` title, the `` Append-only record of wiki operations. Format: `## [YYYY-MM-DD] action | description` `` sentence, and the newest-first blockquote — followed by two dated entries, LF-terminated. **This fixture is the test.** Without the format sentence, a naive `text.index("## [")` implementation passes everything below it.

AC6's wiki-side reword touches only that sentence's opening words; the `Format:` clause — the half that breaks the naive form — is unchanged, so the fixture stays valid either way. It is pinned on the pre-reword text deliberately, and says so in a comment.

`log-fresh.md` is the same header with zero dated entries. `log-h3-entries.md` is the same header with its entries at `###` depth. `log-no-trailing-newline.md` is `log-with-entries.md` with the final `\n` removed. CRLF is constructed in-test, never checked in (§ Scope).

### Cases

1. **Header corruption** (the regression). Prepend into `log-with-entries.md`; assert the header — every byte from `# Wiki Log` through the blockquote's last line — is unchanged, and the new entry sits between the header and the previously-first entry. A `text.index("## [")` implementation fails this.
2. **Anchor unit test.** `ENTRY_RE.search()` over the format sentence alone returns `None`; over a real entry heading it matches at offset 0.
3. **Read-side refusal.** `log-h3-entries.md` exits 2, writes nothing, and its stderr names the heading-like count. Repeated for a `## [2026-8-5]` short-date variant.
4. **Write-side heading validation.** Each of `## [2026-8-5] …`, `### [2026-08-25] …`, `## [2026-08-25]close | …`, and a tab-after-`]` entry exits 2, writes nothing, and its stderr names the format. A well-formed entry passes.
5. **Fresh wiki.** `log-fresh.md`: entry lands after the header, header byte-identical, exit 0, `prepend_log_entry_outcome=fresh` on stdout, path-bearing notice on stderr — and the notice, not `Prepended:`, is what the completion output surfaces.
6. **Missing file.** Target does not exist; created containing exactly the entry plus one trailing newline, and no synthesized header; `prepend_log_entry_outcome=created` on stdout and a path-bearing notice on stderr.
7. **Idempotency.** Two runs with the same `--guard` produce one entry; the second exits 1 and leaves the file byte-identical.
8. **Guard precision.** A file already carrying `close | VHS — VHS-11:` does not suppress an entry guarded on `close | VHS — VHS-1:`. Its inverse: an exact match does suppress.
9. **Guard shape.** A guard not ending in `:` exits 2. A guard absent from the entry's first line exits 2 — including the case where it appears in the *body* but not the heading. A wholly unsubstituted guard (`close | <PROJECT> — <TICKET-ID>:`) exits 2 and its stderr names the *unresolved placeholder* — distinguished from the other two messages, since that guard both ends in `:` and does appear in the first line of an entry built from the same template. This is the check that keeps a literal-placeholder entry out of position 1 of the wiki's permanent log, so it is asserted on the message, not the code.
10. **No stdin.** Two halves. (a) `subprocess` with `stdin=subprocess.DEVNULL`, asserting a union of the no-stdin and empty-entry messages, with a comment recording that Windows `NUL` satisfies `isatty()` while POSIX `/dev/null` does not. (b) in-process with a stdin stub whose `isatty()` returns True, asserting D5's heredoc hint exactly.
11. **Exit 1 is reserved.** A **directory** as `<log-path>` exits 2, not 1, and its stderr does not read as a skip — via `subprocess`, so the real interpreter's uncaught-exception status is what is measured. This is the portable case (`PermissionError` on Windows, `IsADirectoryError` on POSIX). A read-only *target file* is deliberately **not** used: D8's `os.replace` is governed by the parent directory's permissions on POSIX, so `chmod 0444 log.md` succeeds there and the assertion would hold only on Windows. A read-only *parent directory* case is added under `skipIf(os.name == "nt")`.
12. **Atomic write and temp hygiene.** After a successful run no temp file remains in the directory; after a forced mid-write failure the original content is byte-identical and no temp file remains. The temp name begins with `.` (load-bearing against the wiki's `.*.tmp` ignore).
13. **Concurrent change detected.** Via the in-process seam, mutate the file between read and replace; assert exit 2, the `changed under us` stderr text, unchanged content, **and** that the directory holds no leftover temp — the mismatch abort is a plain return, so exception-only cleanup would leak here. Separately, the missing-file variant: the path appears between the existence check and the replace → exit 2.
14. **Mode.** Under `skipIf(os.name == "nt")`: a `0644` target is still `0644` after the write — not `mkstemp`'s `0600`; and a *created* file's mode matches what a plain `open(path, "w")` produces under the same umask.
15. **BOM on the existing file.** A BOM-prefixed copy of `log-with-entries.md` and a BOM-prefixed headerless one-entry file, both built in-test: the new entry lands at position 1, the BOM survives in the output, and neither the fresh-wiki nor the second-entry misplacement occurs. Without D6's offset match both shapes fail silently, so this case is the pin.
16. **Em dash + BOM round-trip.** Guard and entry both carry `—`; a BOM-prefixed entry writes a first line starting with `## `; re-reading as UTF-8 yields the same characters and a second run correctly detects the guard.
17. **Newlines, all three directions.** An LF fixture contains zero `\r` after the write. A CRLF entry piped on stdin produces zero `\r` in the result. Against a CRLF target built in-test, the untouched lines keep CRLF and **the single boundary line above the insertion point is asserted to be LF** — D6 names that re-termination as the one bounded exception, so the test pins it rather than asserting a self-immunizing "untouched lines" claim. Via `subprocess` with piped stderr, a message echoing the guard comes back as valid UTF-8 with LF.
18. **Whitespace discipline.** One blank line above and below the inserted entry in the normal outcome; **no** leading blank line when the anchor is at offset 0 or the existing content is empty; the fresh-wiki and missing-file outcomes end in exactly one `\n`; and against `log-no-trailing-newline.md` the normal outcome leaves the tail byte-identical. Plus the second-close-on-a-created-file case, and its BOM'd variant — a headerless BOM'd file must yield `<BOM>## [entry]` with **no** separator between them, which is the case that distinguishes deciding emptiness in stripped coordinates from deciding it in the original text.
19. **No stale wording survives.** Two whole-file counts over `skills/spec-close/SKILL.md`, both expected **0**: `grep -in "append"` and `grep -n "grep -F"` (all four current occurrences of each are in the edit set). For `AGENTS.md`, assert on **content, not a blanket count**: the `/spec-close` bullet and the `/wiki-after-merge` paragraph — each located by substring, never by line index — contain `prepend` and not `append`. `AGENTS.md` is a living cross-skill doc that may legitimately use the word later, and a repo-wide ban asserted from a `spec-close`-named suite would fail pointing at the wrong subsystem.
20. **Invocation string.** Under `skipIf(shutil.which("bash") is None)`, run D5's documented Bash form via `bash -c` against a copied fixture — `<PROJECT>`, `<TICKET-ID>`, the date and the body substituted, but structure, quoting, delimiter and exit capture unchanged, with `$SCRIPT`, `$LOGPATH` and `$PY` built the way D9 builds them — asserting the entry lands, the guard survives with its em dash and pipe intact, and `prepend_log_entry_exit=0` plus `prepend_log_entry_outcome=prepended` appear on stdout. A companion run that fails (unsubstituted guard) asserts a **non-zero** `prepend_log_entry_exit=` — the assertion that would have caught the `$?`-after-`fi` bug, which reports 0 on every path. This is the only case that sees the shell layer at all: every other process-level case hands `subprocess` a Python-built argv, which never exercises the quoting, the heredoc delimiter, or the exit capture. A tilde-rendered path fails this case; so does an unquoted guard; so does a body line equal to the delimiter.
21. **`requires:` matches the body.** Assert the declared block equals `shell/filesystem/network/services` per D10, and that `subagents` is absent — pinning the declaration against the tool-use notes, since `lint.py` cannot detect under-declaration.
22. **Lint.** `lint.lint_path("skills/spec-close/SKILL.md")` returns zero ERROR **and zero WARN**. Asserted in-process via the same API `tests/test_lint.py` uses, because `lint.py --strict` exits on ERROR only — WARNs never affect its exit status, so the command line alone cannot enforce this.

## Test command

```
python -m unittest discover -s tests -p 'test_spec_close_log.py' -v
python lint.py --strict skills/spec-close/SKILL.md
python -m unittest discover -s tests -p 'test_*.py' -v
```

The `--strict` line is an **ERROR gate only** — zero-WARN is enforced by the **lint** case, not by it. Pin `python` by full path if more than one interpreter is on `PATH`.

## Done when

1. `/spec-close` prepends, and all nine `SKILL.md` sites (lines 3, 26, 204, 309, 343, 365, 380, 381, 396) plus `AGENTS.md:29`/`:100` and `docs/authoring-portable-skills.md:41` read consistently. — § Scope; § Design "the nine sites"; the **no-stale-wording** case (both the `append` and `grep -F` counts, since three of the nine carry no `append` wording).
2. The insertion anchor is line-anchored on a real date and provably cannot match the header's format sentence. — D2; the **header-corruption** and **anchor unit test** cases.
3. Fresh-wiki and missing-`log.md` cases are both specified; a populated file the anchor misses is a refusal rather than a silent bottom-append; and an entry whose own heading the anchor could not find is refused at write time. — D5, D7; the **read-side refusal**, **write-side heading validation**, **fresh wiki**, and **missing file** cases.
4. A test pins the header-corruption case and fails against a naive `index("## [")` implementation. — the **header-corruption** case against `log-with-entries.md`.
5. `python lint.py` reports no ERROR for `spec-close`; the full suite passes. — D10; the **`requires:`-matches-the-body** and **lint** cases; § Test command.
6. The wiki-side "Append-only record" reconciliation is recorded as an out-of-PR step with its destination named. — § Design "Wiki-side step"; `vigil-harbor-wiki/log.md`, direct on master.

## Out of scope

- **Fenced example entries in the header** (D3). No fence masking. Revisit only if a fence is added to `log.md`'s header.
- **Locking `log.md`.** D8 detects a concurrent change; it does not serialize writers.
- **A PowerShell invocation form** (D9). Withdrawn after measurement: Windows PowerShell 5.1's `$OutputEncoding` defaults to ASCII and mangles the guard's em dash, `$?` is a Boolean rather than the exit code, and `test -f` does not exist there — three fixes shipping an untested second path. The rest of `SKILL.md` is already Bash-shaped. The measurements are recorded in D9 so a future pairing starts from evidence.
- **A checked-in CRLF fixture** and any `tests/fixtures/.gitattributes` entry — CRLF is constructed in-test, per VHS-28's recorded position (§ Scope).
- **Re-sorting historical `log.md` entries.** The file is in contract today; the VHS-28 entry was prepended by hand.
- **`wiki-after-merge` and `wiki-state-update` behavior.** Both already prepend correctly and live in the wiki repo. The optional `:37-38` heading reword is a doc fix, not an acceptance criterion.
- **Log rotation** (`log-archive.md`, the `2026-08-01 and later` boundary). The script writes one entry at the top and never rotates.
- **Any other Phase 5 step**, the coverage-model derivation, or the Plane state gate.
- **`__pycache__` mirroring into the config dir** via `sync.py install` — pre-existing behavior with a VHS-28 precedent; noted in § Scope, not addressed.
- **The remaining missing-`requires:` backlog** (`ship-spec`, `review-pr`). D10 clears `spec-close` only.
- **The plane-proxy filing artifacts** carried in the brief's filing note (HTML-escaped `description_html`, stripped angle-bracket placeholders). Worth its own card; not this spec.
- **Synthesizing a `log.md` header** when the file is absent (D7).

## Deferred (P2+)

Additions the brief does not explicitly authorize, each carrying rationale in its decision. Recorded here so the Phase 3 drift check surfaces them rather than a reader discovering them in the diff.

- **D10's `requires:` block** — the brief asks only that `lint.py` "stay clean", and it is already clean (0 ERROR, 1 WARN). Included because D1 makes the shell dependency real.
- **D4's guard-shape validation** (trailing colon, entry-first-line) — the brief says the guard is "unchanged in substance". These validate the caller's input rather than change the matching rule, and both failures would otherwise land on exit 1, the silent-loss code.
- **D5's write-side heading validation** — not in the brief; the write-side mirror of D7's refusal, closing a one-run-delayed reintroduction of the ticket's own bug.
- **D5's never-abort-the-close rule** — new Phase 5 failure-path behavior the brief does not discuss; chosen to match `SKILL.md`'s existing "Interrupted execute" recovery contract over a half-mutated two-repo tree.
- **D5's echoed exit code** — Phase 5 step 4 branches on `prepend_log_entry_exit=$rc` rather than the harness's pass/fail signal. The file's first three-way exit branch; without it an expected idempotent skip reads as a failure.
- **D7's refusal branch** — the brief's § Scope says fresh-wiki should "append after the header block"; the spec narrows that to files with *no* heading-like lines and refuses the rest. A change of direction against a brief-stated behavior; Done-when #3 is restated to match.
- **D8's atomicity and concurrency detection** — the brief's open question asked only "in place or emit to stdout". Temp-file-plus-`os.replace` and a `changed under us` refusal are new operator-visible behavior.
- **D9's not-found pre-check** — `test -f "$SCRIPT"` before the invocation plus an install-hint failure line, new Phase 5 behavior the brief does not discuss; needed because a missing script and a refusing script both exit 2, so the actionable hint cannot be inferred after the fact.
- **Site 26 (`states.json` + `$CLAUDE_CONFIG_DIR`)** — a nine-word edit outside the brief's site list, taken so the file does not ship two different config-dir rules.
- **`AGENTS.md:100`** — a one-word correction to `/wiki-after-merge`'s description, a skill this ticket otherwise leaves alone. Taken because the sentence is factually wrong in the same way this ticket exists to fix.
- **The standing wording assertions** — a permanent tripwire on `SKILL.md` prose and a content assertion on `AGENTS.md`, beyond the brief's four named test cases.
