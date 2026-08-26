# Edge-Cases Review — round 2

Grounding: `skills/spec-close/SKILL.md` is 400 lines with all eight cited line numbers confirmed; `python lint.py skills/spec-close/SKILL.md` returns `0 error(s), 1 warning(s)` exactly as D10 claims, and `lint.py`'s vocabulary accepts D10's proposed block; the real `vigil-harbor-wiki/log.md` (514 lines, 146 KB, pure LF, `.gitattributes` `* text=auto eol=lf`) confirms D2/D3 — its first line-anchored `## [` is line 10, with nothing matching earlier. No CI workflows exist in the repo.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | § Scope forbids the edit § Design mandates (line 204) | CLOSED | spec § Scope table row `204` (line 18); "Files to leave alone" line 43; § Design line 249; Done-when #1 line 324 |
| correctness | F-2 | D4 retires `grep -F` but two SKILL.md sites name it | CLOSED | § Scope rows 380/396 (lines 22, 24); § Design lines 262, 266; D4 "Em-dash sensitivity survives the move" line 108 |
| correctness | F-3 | `requires:` block under-declares | CLOSED | D10 lines 193–213 with per-capability evidence; test case 16 line 309. Verified: `lint.py` `REQUIRES_KEYS`/`SERVICES_VOCAB` accept the block as written |
| correctness | F-4 | Mutation-boundary site is 381, not 382 | CLOSED | spec line 26 corrects the brief explicitly; verified against `SKILL.md:381`/`:382` |
| correctness | F-5 | D6 pins encoding except on the `--dry-run` path | CLOSED | `--dry-run` dropped entirely, D5 line 116 |
| correctness | F-6 | Test 14's allowlist names a nonexistent survivor | CLOSED | now test case 15, stated as a count with no allowlist (line 308); D7 line 175 |
| correctness | F-7 | Exit 1 ambiguous between skip and crash | CLOSED | D5 exit table + line 136 reservation rationale; test case 9 |
| correctness | F-8 | Blank-line discipline breaks on degenerate inputs | CLOSED | D7 "Degenerate inputs" bullet line 172; test case 14 |
| correctness | F-9 | D2's property count contradicts its paragraph | CLOSED | D2 now states "Three exclusions", lists three, references three (lines 70–76) |
| correctness | F-10 | Fixture reproduces a header the spec changes | CLOSED | § Test plan line 288 pins the pre-reword text and says why it stays valid |
| correctness | F-11 | Wiki sibling carries the same stale heading | CLOSED | § Wiki-side step line 276, explicitly non-AC |
| edge-cases | F-1 | Exit 1 overloaded — exceptions read as skipped | CLOSED | D5 table line 129–134; `try/except BaseException` line 136; test case 9 |
| edge-cases | F-2 | Fresh wiki indistinguishable from anchor-not-found | CLOSED | D7 four-outcome table with `HEADINGISH_RE` (line 158); fixture `log-h3-entries.md`; test case 3. Verified `HEADINGISH_RE` does not match the real header |
| edge-cases | F-3 | Script runtime path/interpreter never resolved | CLOSED | D9 lines 185–191, skill-relative rule + not-found halt message |
| edge-cases | F-4 | No atomic replace | CLOSED | D8 lines 177–181 reusing `create_handoff.py:338` `write_atomically()`; test case 10 |
| edge-cases | F-5 | Blank-line rule undefined on degenerate inputs | CLOSED | D7 line 172; test case 14 |
| edge-cases | F-6 | stdout/stderr encoding unpinned | CLOSED | D6 hazard 3 line 144; test case 13. (New variant on *availability* of `reconfigure` filed below as F-5 — different root) |
| edge-cases | F-7 | Stale `grep -F` at 380/394/396 | CLOSED | 380/396 in § Scope; :394 recorded as deliberately kept in § Design "What does not change" line 270 |
| edge-cases | F-8 | No statement on concurrent writers | CLOSED | D8 "Concurrency" line 183; § Out of scope names locking. (Residual leak filed below as F-2 — new root) |
| edge-cases | F-9 | BOM survives `.strip()` | CLOSED | D6 BOM paragraph line 147; test case 12 |
| edge-cases | F-10 | `__pycache__` mirrors into config dir | CLOSED | § Scope line 44; § Out of scope line 339 |
| edge-cases | F-11 | `AGENTS.md:29` restates the retired contract | CLOSED | § Scope line 30 (both :29 and :100); test case 15. Verified those are `AGENTS.md`'s only two "append" hits |
| edge-cases | F-12 | Guard-in-entry tripwire weaker than claimed | CLOSED | D4 "Consistency tripwire" line 106 (first line, with rationale); test case 8. (F-1 below is a different root — the heading's own shape) |
| conventions | F-1 | `AGENTS.md:29` a sixth site | CLOSED | § Scope line 30 |
| conventions | F-2 | Five-site inventory off by one; misses 380 | CLOSED | § Scope table now eight rows; line 26 records the off-by-one |
| conventions | F-3 | `requires:` under-declares vs contract §3 | CLOSED | D10 |
| conventions | F-4 | D8 invalidates the tracked backlog sentence | CLOSED | § Scope line 31; D10 line 213. Verified `docs/authoring-portable-skills.md:41` names all three skills today |
| conventions | F-5 | Script path naming unspecified | CLOSED | D9 |
| conventions | F-6 | `--dry-run` is unused surface | CLOSED | dropped, D5 line 116 |
| conventions | F-7 | Unauthorized spec-level additions | CLOSED | § Deferred line 346 routes all three to the Phase 3 drift check, as the finding asked |
| conventions | F-8 | `--strict` cannot enforce zero WARN | CLOSED | test case 17 line 310; § Test command line 320 |

All 31 round-1 findings are CLOSED. No PARTIAL, no REOPENED.

## Findings

### F-1: The entry's own heading shape is never validated — the script can write an entry its own anchor cannot find, silently
**Severity:** P1
**Where:** spec § Decisions D5 (line 241, `main()` sequence); D4 "Consistency tripwire" (line 106); § Test plan case 8 (line 301)
**Edge case:** The caller supplies entry text whose first line does not match `ENTRY_RE` — `## [2026-8-5] close | …`, `### [2026-08-25] close | …`, `## [2026-08-25]close | …`, or a tab after the `]`. All satisfy the only two checks the spec specifies (non-empty after strip; `--guard` present in the first line).
**What happens:** Exit 0, `Prepended: log.md`, entry lands at the top. The *next* close's `ENTRY_RE` skips it and anchors on the entry below it, inserting the newer entry **underneath** the malformed one. `log.md` is now out of newest-first contract, no refusal fires (real entries still exist, so D7's `AnchorMissing` path is never reached), and nothing prompts the operator to re-sort. This is the VHS-29 bug re-entering through the write side.
**Why the spec misses it:** D7 line 162 enumerates exactly these variants — "`### [2026-08-25] …` (a hand edit), or `## [2026-8-5] …`, or carries a tab after the `]`" — as realistic read-side hazards, and builds the refusal row around them. The spec never applies the same skepticism to the string it is about to write, even though the entry heading is the one input the script fully controls the shape of. D4's tripwire checks where the guard sits in the first line, not whether the first line is a valid entry heading; test case 12 asserts only that a BOM-stripped first line "starts with `## `", which every variant above except the `###` one satisfies.
**Suggested fix:** Add to D5's `main()` sequence, immediately after the guard/first-line check: *exit 2 unless `ENTRY_RE.match(entry)` matches at offset 0, with stderr `entry heading does not match the log format '## [YYYY-MM-DD] …' — refusing to write an entry the anchor cannot find: <first line>`.* Add a test case: each of the four malformed headings above exits 2 and writes nothing. The machinery already exists — test case 2 line 295 asserts `ENTRY_RE` matches a real heading at offset 0.

### F-2: The concurrency-mismatch path returns 2 without unlinking the temp file, and `/spec-close`'s own suggested `git add -A` then commits it into the wiki
**Severity:** P2
**Where:** spec § Decisions D8 (lines 181, 183); § Test plan case 11 (line 304)
**Edge case:** `os.stat` re-check mismatches immediately before `os.replace` — i.e. `/wiki-after-merge`, an editor, or a second close touched `log.md` during the window.
**What happens:** The temp file has already been written and fsynced by that point. D8 specifies cleanup only "with `temp_path.unlink(missing_ok=True)` on `BaseException`", and a mismatch is an ordinary `return 2`, not an exception — so the temp survives in `<wiki_root>/`. `/spec-close` deliberately leaves the wiki uncommitted, and `SKILL.md:371` prints `(in wiki) git add -A && git commit -m "close(...): wiki harvest"` as the suggested next command. `-A` stages the orphan, and a ~146 KB copy of `log.md` under a `tmp…` name gets committed to the wiki. The spec also never names a temp prefix, so the file has no dot-prefix or recognizable name to make it obvious (the precedent at `create_handoff.py:337` uses `prefix=".session-handoff."`).
**Why the spec misses it:** D8 imports the precedent's cleanup contract verbatim, but the precedent has no non-exceptional early-return between mkstemp and replace — the mismatch check is new surface with no matching cleanup. Test case 10 asserts "no temp file remains" only for the success and forced-mid-write-failure paths; test case 11, which is the path that leaks, asserts only "exit 2 and unchanged content".
**Suggested fix:** In D8, state that the mismatch path unlinks the temp before returning 2 (or that the whole write is wrapped in `try/finally` with `temp_path.unlink(missing_ok=True)`), and name the prefix — `prefix=".prepend-log-entry."`, matching the precedent's dot convention so a leak is at least hidden from `git add -A` on POSIX. Extend test case 11 to assert the directory holds no extra files afterward.

### F-3: Newline discipline is pinned on the writes and on neither read — `\r\n` in the existing file is normalized (contradicting D6), and `\r\n` in the entry text is embedded verbatim
**Severity:** P2
**Where:** spec § Decisions D6 hazard 4 (line 145) and its closing sentence (line 149); D6 hazard 2 (line 143); § Test plan case 13 (line 306)
**Edge case:** (a) `log.md` contains CRLF — an editor save, a clone without the wiki's `.gitattributes`, or a copy of the file used as a test target. (b) The entry text arriving on stdin contains CRLF — any caller that pipes from a Windows-native tool rather than a Git Bash heredoc.
**What happens:** (a) D6 line 149 states "Existing CRLF content, if any, is preserved rather than normalized." The described implementation cannot do this: `open(path, encoding="utf-8")` with the default `newline=None` performs universal-newline translation on read, so every `\r\n` becomes `\n` in memory, and the `newline="\n"` write then emits LF — a one-entry insert becomes a whole-file rewrite, which is precisely the harm hazard 4 exists to prevent. (b) Conversely, the entry text is decoded from `sys.stdin.buffer` with no newline handling at all, so an entry carrying `\r\n` writes literal CR bytes into an LF file. Test case 13's guarantee ("an LF fixture contains zero `\r` after the write") holds only because its own entry text happens to be LF.
**Why the spec misses it:** D6 treats newlines as a property of the write alone. Both reads bypass the pinning — one by using text mode's default translation, the other by using binary mode with no normalization. Live impact is currently limited: the wiki's `.gitattributes` is `* text=auto eol=lf` and `log.md` today has zero `\r` (verified), so (a) is latent. (b) has no such mitigation.
**Suggested fix:** In D6 hazard 4, specify `open(path, encoding="utf-8", newline="")` for the read — which is what actually makes line 149's preservation claim true — and add to hazard 2 that the decoded stdin is normalized (`entry.replace("\r\n", "\n").replace("\r", "\n")`) before the BOM strip. Extend test case 13 to feed a CRLF entry and assert zero `\r` in the result, and to prepend into a CRLF fixture and assert the untouched lines keep their CRLF.

### F-4: Test case 9's read-only-target assertion holds only on Windows
**Severity:** P2
**Where:** spec § Test plan case 9 (line 302)
**Edge case:** The suite is run on Linux or macOS.
**What happens:** POSIX `rename(2)` — and therefore `os.replace` — checks write+execute on the *containing directory*, not the mode of the target file. With the D8 atomic-replace design, replacing a mode-`0444` `log.md` in a writable directory **succeeds**. The case asserts exit 2; it gets exit 0. A contributor on POSIX sees a red suite for a script that is behaving correctly, and the assertion that actually matters — that exit 1 is never produced by an I/O failure — is proven on one platform only.
**Why the spec misses it:** The case was written in round 1 against a plain in-place `open(path, "w")`, where the target's own mode *is* what fails. D8 replaced that write with `mkstemp` + `os.replace` in the same round, which moved the permission check from the file to the directory; test case 9 was not re-derived against the new write path. `AGENTS.md` states the repo is cross-platform and there is no CI to catch the divergence (verified: no `.github/workflows/`).
**Suggested fix:** Replace the read-only-*target* case with a read-only-*directory* case on POSIX (`os.chmod(dir, 0o555)`, `skipIf(os.name == "nt")`, since Windows ignores directory read-only for file creation), and keep the directory-as-`<log-path>` case as the portable one that runs everywhere. Alternatively drop the read-only case and rely on directory-as-path plus a monkeypatched write that raises — the point of the case is the exit code, not the specific I/O error.

### F-5: `sys.stdout.reconfigure` is not available on every stream the script may be handed, and the failure is swallowed into exit 2 — which is the value test case 11 asserts
**Severity:** P2
**Where:** spec § Decisions D6 hazard 3 (line 144); § Design `main()` sequence (line 241, "reconfigure stdout/stderr (D6) → parse args"); § Test plan case 11 (line 304)
**Edge case:** `main()` is called in-process with `sys.stdout`/`sys.stderr` replaced by a non-`TextIOWrapper` — `io.StringIO` under `contextlib.redirect_stdout`, `unittest`'s `-b` buffering, or any harness that wraps the streams.
**What happens:** `reconfigure` is a `TextIOWrapper` method; `StringIO` does not have it. `AttributeError` on the first statement of `main()`, caught by D5's `except BaseException` guard, message to stderr, `return 2`. Two consequences. First, any in-process invocation of `main()` is unconditionally exit 2 under stream capture. Second, and worse: test case 11 asserts exactly `exit 2` for the concurrency-mismatch path via "a patched `splice` that touches the file" — which reads as an in-process call. If that test captures output, it passes with the correct exit code having never reached `splice`, `os.stat`, or the comparison. The concurrency detection D8 introduces could be entirely absent and the test would still be green.
**Why the spec misses it:** D6 hazard 3 reasons about the *encoding* of the real piped stdout and correctly concludes reconfigure is needed; it never considers the stream not supporting the call. The `main()` ordering in § Design puts reconfigure first, inside the guard, which converts a missing method into the same exit code several tests use as their success signal.
**Suggested fix:** In D6 hazard 3, specify the reconfigure as best-effort and outside the failure semantics: `for s in (sys.stdout, sys.stderr): getattr(s, "reconfigure", lambda **k: None)(encoding="utf-8", newline="\n")`, or wrap it in its own `try/except (AttributeError, ValueError): pass`. Separately, state in test case 11 that the mismatch is asserted on a distinguishing signal — the exact stderr text `log.md changed under us — re-run` — not on the exit code alone, so it cannot pass on an unrelated exit 2. The same "assert the message, not just the code" note should apply to test cases 3 and 9.

### F-6: With no stdin redirect the script blocks forever — there is no `isatty` guard on the one required input
**Severity:** P2
**Where:** spec § Decisions D5 (lines 112, 124, and the exit table's "empty stdin" row at line 132); § Design (line 241)
**Edge case:** The script is invoked without a pipe or heredoc — an operator running it by hand to inspect behavior (which D5 line 116 explicitly suggests: "an operator wanting a preview can run the script against a copy"), a harness that does not attach a pipe, or a `SKILL.md` invocation whose heredoc was mis-rendered.
**What happens:** `sys.stdin.buffer.read()` blocks until EOF, which never arrives on a terminal. The script hangs. In an agent harness this consumes the Bash tool's full timeout and returns a signal-derived exit code (124/137/143) that D5's contract does not enumerate — it lands in "any other exit code … treated as failure", which is at least safe, but only after a multi-minute stall at Phase 5 step 4, with the archive moves of step 3 already committed to the working tree.
**Why the spec misses it:** D5 specifies the *empty* stdin case (exit 2) but treats "no stdin" and "empty stdin" as the same thing. They differ: empty means a pipe that closed with zero bytes; none means no pipe at all, where there is no close to wait for. D5 line 116's own suggestion that an operator run the script by hand makes the interactive case a documented usage path.
**Suggested fix:** In D5, before the read: *exit 2 with `no entry text on stdin — pipe the entry, e.g. python prepend_log_entry.py <path> --guard '<literal>' <<'EOF' … EOF` when `sys.stdin` is `None` or `sys.stdin.isatty()`.* Add a test case asserting the interactive path exits 2 promptly rather than blocking (drive it with `stdin=None` under `subprocess` on a pty, or simply assert the guard function's behavior directly).

### F-7: "Halts" (D9) and "report and continue" (D5) describe the same failure differently, and step 3 has already mutated the tree
**Severity:** P2
**Where:** spec § Decisions D9 (line 191, "the log step **halts and prints**"); D5 exit table row 2 (line 132, "Surface stderr verbatim; report `log.md NOT written`"); § Design line 260 (the completion block carries an exit-2 line)
**Edge case:** The script is not found (exit 127), or exits 2 for any reason, at Phase 5 step 4.
**What happens:** Undefined whether `/spec-close` aborts or proceeds to step 5 and the completion block. It matters: step 3 (archive) has already `git mv`'d every spec artifact from `TODO/` to `DONE/`, and Phase 5 writes to two repos neither of which is committed. A literal "halt" means the operator gets no completion block — no `Archived:` line, no commit suggestions, no re-run instruction — for a tree that is already half-mutated across two repos, which is exactly the state `SKILL.md:394`'s "Interrupted execute" failure mode exists to make recoverable. The three sites read as three different contracts: D9 says halt, D5 says report, § Design line 260 shows a completion-block line that only exists if the run continued.
**Why the spec misses it:** D9 was added in round 1 to close the script-resolution finding and chose "halts" to emphasize "never silent success"; D5's table was written independently for the exit-code mapping. Neither cross-references the other, and neither states what happens to the rest of Phase 5.
**Suggested fix:** Pick one and say it in both places. The safer reading, and the one consistent with `SKILL.md`'s existing re-run contract: *a failed log write never aborts the close — step 5 and the completion block always run, the completion block carries `log.md NOT written: <stderr>`, and it names the recovery (`re-run /spec-close <DONE-path>`; the guard makes the retry idempotent).* Reword D9's "halts and prints" to "the log step fails loudly and the close reports `log.md NOT written`", and add the recovery sentence to D5's exit-2 row.

### F-8: The exit-2 and refusal messages carry neither the guard nor the run's identity — and D6's stderr rationale cites a message the spec never specifies
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions D7 (lines 158, 159); D8 (line 183, `log.md changed under us — re-run`); D6 hazard 3 (line 144)
**Edge case:** A close run fails at step 4 and the operator (or a later debugger reading a transcript) has to work out which close, which ticket, and which guard string was in play.
**What happens:** The refusal message names the path and a heading-like count; the stat-mismatch message names neither the path nor the guard nor the ticket — it says the literal string `log.md`, not `<path>`. `/spec-close` surfaces stderr verbatim, so that is the entire evidence trail. Since `log.md` genuinely has two writers plus an operator's editor, "changed under us" is the message most likely to appear months later in a transcript with no other context. Separately, D6 hazard 3 justifies the stderr reconfigure with "Any stderr message echoing `--guard` carries an em dash by construction, so this is not hypothetical" — but no message the spec specifies echoes `--guard`. The reconfigure is still correct (paths can carry non-ASCII), but its stated evidence does not exist in the design.
**Why the spec misses it:** The messages were each written to explain one condition, not to identify one run. The spec's own debuggability standard is higher elsewhere — D7's refusal deliberately names the heading-like count so the operator knows what to inspect.
**Suggested fix:** Specify that every exit-2 and exit-1 message names the resolved absolute `<path>` and the `--guard` literal. Concretely: `log.md NOT written: <path> changed under us between read and replace (guard: <guard>) — re-run`, and `entry already present in <path> (guard: <guard>) — skipped`. This makes D6 hazard 3's rationale literally true and gives the transcript enough to tie a failure to a ticket. Worth folding into the spec at 2g even if nothing else changes.

### F-9: `--guard` is validated only as non-empty; the two properties D4 calls load-bearing are never checked, and an under-specific guard exits 1 — the silent-loss code
**Severity:** P3
**Where:** spec § Decisions D4 (lines 101–102); D5 (line 241, "exit 2 unless `--guard` is non-empty and appears in the entry's first line")
**Edge case:** The caller constructs a degenerate or over-broad guard — a template substitution that left `<PROJECT>` unresolved, a guard truncated before the trailing colon, or any short substring that already occurs in the 146 KB of existing entry prose.
**What happens:** The guard is found in the existing text, the script exits **1**, and `/spec-close` reports `log.md: entry already present — skipped`. The close prints a successful-looking completion block over a `log.md` that never received the entry, and the documented re-run skips it again for the same reason — the exact failure chain D5 line 136 wrote the exit-1 reservation to prevent, arriving through the guard rather than through an exception.
**Why the spec misses it:** D4 declares both the `close |` prefix and the trailing colon load-bearing and explains precisely why (the `VHS-1` / `VHS-11` false match), then D5 validates neither. The only guard check is non-emptiness and first-line presence.
**Suggested fix:** Either (a) add to D5: *exit 2 unless the guard is at least N characters and ends with `:`* — the colon is the property D4 says prevents the false match and is trivially checkable without hardcoding `close |` into a generically-named script; or (b) state explicitly in D4 that guard *shape* validation stays with the caller and `SKILL.md`'s documented literal is the only enforcement, so the omission is a recorded decision rather than a gap. Option (a) is cheap and closes a silent-loss path.

### F-10: The missing-file outcome has no stat baseline and no exclusive create — a concurrently created `log.md` is silently clobbered
**Severity:** P3
**Where:** spec § Decisions D7 "Missing file" row (line 160); D8 "Concurrency" (line 183)
**Edge case:** `log.md` does not exist at read time, and `/wiki-after-merge` or an operator creates it before this script's `os.replace`.
**What happens:** D8's protection is defined as "captures `os.stat()` immediately after reading and re-checks it immediately before `os.replace`" — with no file there is no baseline to capture, so the mismatch check has nothing to compare. `os.replace` overwrites the newly created file unconditionally, and the other writer's content is gone with no signal. Low frequency (fresh-wiki bootstrap only), but the loss is total for that file and, exactly as D8 notes for the general case, the guard will never detect it on any later run.
**Why the spec misses it:** D8's concurrency reasoning is written entirely against the populated-file path; D7's missing-file row is written as a convenience case ("Create it containing the entry alone") with no concurrency dimension.
**Suggested fix:** Add to D8: *when the file was absent at read time, the baseline is "absent" — re-check `os.path.exists(path)` immediately before `os.replace` and exit 2 with `<path> appeared under us — re-run` if it now exists.* One line, and it makes the missing-file row obey the same contract as the others.

### F-11: `mkstemp`'s `0600` mode silently becomes `log.md`'s mode on POSIX — the precedent creates files, this one replaces an existing one
**Severity:** P3
**Where:** spec § Decisions D8 (line 181, "reusing the shape of `create_handoff.py:338`")
**Edge case:** The script runs on Linux or macOS against an existing `log.md` whose mode is the usual `0644`.
**What happens:** `tempfile.mkstemp` creates with `0600` by design, and `os.replace` carries that mode onto `log.md`. The wiki's operations log becomes owner-read/write only. Git does not track non-exec mode bits, so this never shows in a diff and never round-trips through a clone — it is a working-tree-only, silent, one-way change that only surfaces if another user or a service account reads the file. Windows is unaffected (mode is largely ignored; ACLs inherit from the directory).
**Why the spec misses it:** The precedent it copies (`create_handoff.py:337`) writes a *brand-new* handoff document, where `0600` is the correct and intended mode. D8 imports the mechanism without noting that replacing an existing tracked file changes the property the precedent never had to preserve.
**Suggested fix:** Add to D8: *when the target exists, capture its mode alongside `st_mtime_ns`/`st_size` and `os.chmod(temp_path, st.st_mode & 0o777)` before the replace; when it does not, leave `mkstemp`'s default.* One line, and it makes the "the script splices text and never rewrites what it did not author" spirit of D6 line 149 true for metadata as well as bytes.

### F-12: The existing-text guard search is whole-text while the entry-side check is first-line — D4's own rationale applies to both
**Severity:** P3
**Where:** spec § Decisions D4 (lines 100, 106)
**Edge case:** The guard literal for the ticket being closed appears in the *body prose* of some earlier entry rather than in any entry heading.
**What happens:** The whole-text `in` check matches, exit 1, `entry already present — skipped`, and the close's entry is silently never written — with no way for a later re-run to recover, since the false match is permanent.
**Why the spec misses it:** D4 line 106 makes precisely this argument to justify the first-line rule on the *entry* side — "close entries routinely quote sibling tickets in their body prose (the live VHS-28 entry names several), so a whole-text check would pass on a guard that matches body prose rather than the heading it is supposed to describe" — and then leaves the *existing-text* check whole-text, where the same exposure produces a worse outcome (silent skip rather than a loud exit 2). The spec's justification is byte-identity with today's `grep -F`, which is legitimate; the gap is that the asymmetry is never acknowledged. In practice the risk is low: bodies in the real `log.md` name bare ticket IDs, not the full `close | VHS — VHS-29:` literal (verified across the current file).
**Suggested fix:** No behavior change required — add one sentence to D4 recording the asymmetry and why byte-identity wins: *"The existing-text search stays whole-text, byte-identical to today's `grep -F`. It carries the mirror of the exposure the first-line rule closes on the entry side — a guard literal quoted in body prose would suppress a legitimate entry — accepted because narrowing it would change dedup semantics against every entry already in the file."* If it is ever narrowed, the natural form is to search only lines matching `ENTRY_RE`.

## Persistence checklist

`log.md` is persisted state that survives a process restart, so the checklist applies.

1. **Atomicity** — CHECKED. D8 (mkstemp-in-dir → fsync → close → `os.replace`), test case 10. Residual: the mismatch return path leaks the temp (F-2).
2. **Size bound** — CHECKED. Verified: the live `log.md` is 514 lines / 146 KB since the 2026-08-01 rotation, read whole and rewritten whole once per close. Rotation is an explicit out-of-scope item and is the release valve. Entry text is unbounded but operator-authored and single-record.
3. **Idempotency on retry** — CHECKED. D4's guard makes check-and-insert one operation; test case 6 pins byte-identity on the second run. Residual: F-9 (an over-broad guard makes the *first* run look like a retry).
4. **Read-side mode filtering** — N/A. No smoke-test/ablation/dev-mode records exist in this file class.
5. **Schema-version forward-compat** — CHECKED. D7's four-outcome split *is* the forward-compat story: a `log.md` whose shape drifts from `ENTRY_RE` is a loud refusal, not a silent bottom-append. Residual: the same tolerance is not applied to entries this script writes (F-1).
6. **Write-then-read race** — CHECKED for the populated path (D8 stat re-check, documented as detection not locking, with locking named in § Out of scope). FLAGGED for the missing-file path (F-10).

## Summary
P0: 0 | P1: 1 | P2: 7 | P3: 4 | P4: 0

STATUS: RED P0=0 P1=1 P2=7 P3=4 P4=0
