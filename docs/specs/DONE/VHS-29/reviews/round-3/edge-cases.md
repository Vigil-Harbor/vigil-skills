# Edge-Cases Review — round 3

Grounding: spec v3 read fresh (417 lines); brief read; `<project_root>/CLAUDE.md` + `AGENTS.md` read; all three round-2 reports read (`scale_lens=off`, no stale `scalability.md` present). Verified against live files: `skills/spec-close/SKILL.md` is 400 lines with all nine cited sites confirmed at 3/26/204/309/343/365/380/381/396; `grep -in append` returns exactly 4 hits (3, 309, 343, 365) and `grep -n "grep -F"` exactly 4 (204, 343, 380, 396), all inside the edit set; `AGENTS.md` `append` hits are exactly 29 and 100; `docs/authoring-portable-skills.md:41` is the backlog sentence naming three skills; `create_handoff.py:338` is `write_atomically`, `:347` is the `newline="\n"` open; `sync.py:36` is the `CLAUDE_CONFIG_DIR` lookup; `spec-cycle/SKILL.md:5-10` is the `requires:` block; `vigil-harbor-wiki/.gitignore` carries `.*.tmp`, `.gitattributes` is `* text=auto eol=lf`, `log.md` is 514 lines with zero `\r`. Two behaviors measured on this machine's interpreter (Python 3.14.3, Windows): a missing script path exits **2**, not 127; `sys.stdin.isatty()` returns **True** under `< /dev/null` in Git Bash.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P1) | entry's own heading shape never validated | CLOSED | D5 validation step 4 (spec:141); test case 4 (:356); Done-when #3 (:388); § Deferred (:412) |
| edge-cases | F-2 (P2) | concurrency-mismatch leaks the temp | CLOSED | D8 ordered write block (:209-215), `try/finally` (:222), dot-prefix rationale (:221) — `.*.tmp` confirmed live in the wiki `.gitignore`; test 13 (:365) |
| edge-cases | F-3 (P2) | newline pinned on writes, neither read | PARTIAL | read side now pinned (D6 hazard 4, :168-171), but D7's separator normalization still re-terminates the line above the anchor, falsifying :173's absolute claim → new **F-2** |
| edge-cases | F-4 (P2) | test 9's read-only target is Windows-only | CLOSED | test case 11 (:363), directory-as-path portable case + `skipIf(nt)` read-only parent |
| edge-cases | F-5 (P2) | `reconfigure` unavailable on StringIO | CLOSED | D6 hazard 3 best-effort `try/except` (:167); standing assert-the-message rule (:341) |
| edge-cases | F-6 (P2) | no isatty guard — blocks forever | CLOSED (new variant → F-7) | D5 step 1 (:138); test case 10 (:362). Guard exists; its *test* is not reachable as written |
| edge-cases | F-7 (P2) | halts vs report-and-continue | CLOSED | D5 "A failed log write never aborts the close" (:155); D9 defers (:244) |
| edge-cases | F-8 (P2) | messages carry neither path nor guard | CLOSED (residual → F-11) | D5 blanket rule + concrete text (:157) |
| edge-cases | F-9 (P3) | guard shape unvalidated | CLOSED | D4 "Guard shape" (:111-116) |
| edge-cases | F-10 (P3) | missing-file path has no stat baseline | CLOSED | D8 "File absent" row (:228); test 13 (:365) |
| edge-cases | F-11 (P3) | mkstemp 0600 becomes log.md's mode | PARTIAL | D8 "Mode is preserved" (:223) is scoped to *when the target existed*; the created-file path still lands 0600 → new **F-9** |
| edge-cases | F-12 (P3) | whole-text vs first-line asymmetry | CLOSED | D4 records it with the byte-identity rationale (:109) |
| correctness | F-1 (P2) | stale D8 cross-references | CLOSED | :17 and :34 both read D10 |
| correctness | F-2 (P2) | D10 cites the wrong test case | **REOPENED** | :266 now says "test case 16"; case 16 is *Newlines, both directions* — the `requires:` assertion is case **19** → **F-1** |
| correctness | F-3 (P2) | re-check placement disagrees | CLOSED | D8 (:212) and § Design (:296) both put the re-stat immediately before `os.replace` |
| correctness | F-4 (P2) | test 15 cannot see three of the sites | PARTIAL | Done-when #1 (:386) now cites 18, but :29 and :201 still cite "test case 15" → **F-1** |
| correctness | F-5 (P2) | interpreter never named | CLOSED | D9 (:238) — `python`/`python3` with the mode-644 + Git-Bash rationale |
| correctness | F-6 (P3) | test 9 read-only Windows-only | CLOSED | test case 11 (:363) |
| correctness | F-7 (P3) | AGENTS.md assertion line-pinned | CLOSED | test 18 stated as whole-file counts (:370) |
| correctness | F-8 (P3) | Files-to-leave-alone asymmetry | CLOSED | single umbrella rule (:47) |
| correctness | F-9 (P3) | no baseline on the missing-file path | CLOSED | D8 "File absent" row (:228) |
| conventions | F-1 (P2) | stale `D8` cross-references | CLOSED | :17, :34 read D10 |
| conventions | F-2 (P3) | § Deferred under-reports | CLOSED | seven items (:410-416) |
| conventions | F-3 (P2) | test 15 line-pinned on AGENTS.md | CLOSED | :370 |
| conventions | F-4 (P3) | D9's `$CLAUDE_CONFIG_DIR` parity claim false | CLOSED | :240-242 states the divergence; site 26 brought along |
| conventions | F-5 (P3) | duplicated `write_atomically` unexplained | CLOSED | D8 closing paragraph (:232) |
| conventions | F-6 (P4) | shebang / `requires:` position | CLOSED | § Design (:280); D10 (:258) |

## Findings

### F-1: Three stale test-case cross-references — the same renumbering drift correctness/F-2 closed in round 2, reintroduced by v3's own renumbering
**Severity:** P0
**Where:** spec.md:29; spec.md:201; spec.md:266 (against the § Test plan list, spec.md:353-372)
**Edge case:** The test list grew from 16 cases to 20 between v2 and v3. Done-when #1 and #5 were re-pointed; three in-body references were not.
**What happens:** An implementer following the spec's own pointers writes the wrong assertion into the wrong case, or writes it twice. Concretely, the spec now attributes the same claim to two different cases in the same document — :29 says *"Test case 15 asserts **both** counts"* while Done-when #1 (:386) says *"test case 18 (both the `append` and `grep -F` counts)"*. Test case 15 is **Em dash + BOM round-trip**; it asserts nothing about wording counts.
**Why the spec misses it:** Verified by enumerating the numbered list at :353-372:
- :29 — "Test case **15** asserts both counts" → the wording-count case is **18**.
- :201 — "test case **15** asserts zero occurrences in `SKILL.md`" → **18**.
- :266 — "which is why **test case 16** asserts the declared set against the tool-use notes" → the `requires:` assertion is **19**; case 16 is *Newlines, both directions*.

This is precisely round-2 correctness/F-2 ("D10 cites test case 14; the assertion it describes is test case 16"), which was closed by re-pointing at 16 — a number the v3 renumbering then invalidated. No rationale in the spec indicates a deliberate change of direction, so it is REOPENED, not superseded.
**Suggested fix:** Re-point :29 → 18, :201 → 18, :266 → 19. Then, to stop the third recurrence, replace numeric references with the case *titles* (e.g. "the **No stale wording survives** case", "the **`requires:` matches the body** case"), which survive renumbering. § Deferred:415 already uses a title-bearing form ("Test case 18's standing wording assertions") and would be the only remaining numeric reference to keep in sync.

---

### F-2: D7's separator normalization rewrites bytes the script did not author, falsifying D6's absolute preservation claim — and test 16 is worded so it cannot catch it
**Severity:** P2
**Where:** spec § D7 "Whitespace discipline" (spec.md:195-196); against D6 hazard 4 (spec.md:173), D6 BOM (spec.md:175), test case 16 (spec.md:368)
**Edge case:** `log.md` (or a copy of it used as a target) is CRLF-terminated, BOM-prefixed, or has a markdown hard break (trailing double-space) on the line immediately above the anchor.
**What happens:** D7 mandates *"the text preceding the anchor is normalized to end with exactly one blank line (`\n\n`)"*. The natural implementation — `prefix.rstrip() + "\n\n"` — strips the trailing `\r\n\r\n` of a CRLF file and re-emits LF, flipping the terminator of the last header line to LF and leaving a single mixed-ending line at the splice point on every close. The same `rstrip()` eats a hard-break's trailing spaces, converting a hard line break to a soft one. Separately, :175 `lstrip("\ufeff")`s the **existing file text**, so a BOM-prefixed `log.md` silently loses its BOM on write. Each is a byte the script did not author.
**Why the spec misses it:** :173 states the invariant absolutely — *"existing CRLF content, if any, is preserved rather than normalized — the script splices text and never rewrites lines it did not author"* — and D7 contradicts it for exactly one line. Test 16's phrasing, *"leaves the **untouched** lines' CRLF intact"*, is self-immunizing: the boundary line is by definition touched, so the test passes either way and the drift the brief's open question #3 warned about ("'one blank line' vs 'two' is the kind of thing that silently drifts") goes unpinned. The live wiki is pure LF with `eol=lf`, so this never fires in production today — but `log-crlf.md` exists precisely to exercise the case the spec is silent about.
**Suggested fix:** Pick one and say so. Either (a) narrow :173 to "…never rewrites lines it did not author, **except the terminator of the single line immediately above the insertion point, which is re-emitted as LF**", and change test 16's CRLF clause to assert that specific line's terminator rather than "untouched lines"; or (b) require the normalization to preserve the boundary line's existing terminator (strip only whole blank lines, re-emit the detected terminator style). Add the same one-liner for the fresh-wiki right-strip (:196) and state whether the existing file's BOM is preserved or dropped.

---

### F-3: The concurrency baseline is captured *after* the read, so a write landing in the read→stat window is silently clobbered — the exact failure D8 exists to prevent
**Severity:** P2
**Where:** spec § D8 "Concurrency" (spec.md:225); § Design `main()` walkthrough (spec.md:296)
**Edge case:** `/wiki-after-merge`, a second close, or an editor replaces `log.md` between this script's `read()` returning and its `os.stat()`.
**What happens:** The baseline records the *new* file's `(st_mtime_ns, st_size)` while the in-memory text is the *old* version. The re-stat before `os.replace` matches, the check passes, and the script writes a splice of stale content — dropping the other writer's entry with no signal. D8's own rationale names this as the unrecoverable case: *"because the loser's entry is gone the guard will not detect the loss on any later run either."*
**Why the spec misses it:** :225 is explicit about the order — *"The baseline captured **immediately after the read**"* — and :296 repeats it as "read the file … capturing the stat baseline and mode". Stat-after-read makes the uncovered window a **false negative** (silent clobber); stat-*before*-read makes it a **false positive** (spurious exit 2 → documented re-run), which is the safe direction and costs nothing. The window is short, which is why this is P2 and not higher, but the failure inside it is exactly the one D8 was added for.
**Suggested fix:** Reverse the order in both places: `stat` (or `os.stat` on the path, `None` when absent) → read → re-stat immediately before `os.replace`. One sentence in D8 and one clause in § Design.

---

### F-4: The three-way exit code is never made observable — Phase 5 step 4 gives the skill no way to tell a benign skip (1) from a failure (2)
**Severity:** P2
**Where:** spec § D5 exit-code table (spec.md:143-151); § Design line 343 rewrite (spec.md:310-315)
**Edge case:** Any close where the entry is already present (exit 1) — i.e. every `--partial`-then-full re-run and every re-run after an interrupted execute, both of which `SKILL.md`'s failure modes call out as expected paths.
**What happens:** The invocation is a bare `python <path> <log> --guard '<literal>' <<'EOF' … EOF`. A harness reports "command succeeded / command failed"; 1 and 2 both read as failure. The skill then prints `log.md NOT written: <stderr>` for a correctly-skipped idempotent re-run — reporting a failure over a healthy close, which is the inverse of the confusion D5's exit-1 reservation was written to prevent, and it also fires the "re-run `/spec-close <DONE-path>`" recovery hint on a run that needs no recovery.
**Why the spec misses it:** D5 specifies the code→behavior mapping in full but never the mechanism by which the agent reads the code. `SKILL.md`'s existing convention ("If exit ≠ 0…", Phase 0 steps 2 and 6a) is binary and works for binary probes; this is the file's first three-way branch.
**Suggested fix:** Pin the invocation form in § Design's line-343 rewrite as `python <path> "<log>" --guard '<literal>' <<'EOF' … EOF` followed on its own line by `echo "prepend_log_entry_exit=$?"`, and state that Phase 5 step 4 branches on that echoed integer — never on the harness's success/failure signal — with any value other than 0/1/2 (including 127) taking the exit-2 branch.

---

### F-5: The `--guard` argument and `<log-path>` are never shell-quoted in the spec, and the guard literal contains a pipe by construction
**Severity:** P2
**Where:** spec § D5 "CLI surface" (spec.md:130-132); § Design (spec.md:315)
**Edge case:** The invocation is rendered literally as the CLI surface shows it: `prepend_log_entry.py <log-path> --guard close | VHS — VHS-29:`.
**What happens:** Bash splits on the `|`. The script receives `--guard close` (no trailing colon → exit 2, loud but with a misleading message), and the shell then tries to run `VHS` → `command not found`, exit 127. The pipeline's status is 127, which D5 maps to failure — so it degrades loudly, but the operator sees a shell error instead of an actionable one, and per F-4 the skill cannot tell the two apart anyway. On Windows/Git Bash the same omission bites `<log-path>`: an unquoted `C:\Users\...\vigil-harbor-wiki\log.md` has its backslashes consumed as escapes (`C:Users...`), so the script is handed a nonexistent relative path and takes the **missing-file outcome** — creating a stray `C:Users...log.md` in cwd and exiting **0** with `Prepended: log.md`. That is a silent success over a log entry that went nowhere.
**Why the spec misses it:** :315 pins quoting for the *heredoc* ("shown with a quoted heredoc so the entry's own backticks and `#` characters pass through unexpanded") and stops there. The guard's `|` and `—` are named repeatedly as load-bearing content (D4, D6, `SKILL.md:396`) without ever noting that `|` is also shell metacharacter.
**Suggested fix:** In the CLI surface and the line-343 rewrite, show the argument single-quoted (`--guard 'close | <PROJECT> — <TICKET-ID>:'` — the literal contains no single quote, so single-quoting is total) and the path double-quoted with forward slashes (Python accepts `/` on Windows). Add one sentence: "the guard contains ` | `; an unquoted rendering is a shell pipe, and an unquoted backslash path silently becomes a relative path that takes the missing-file outcome and exits 0."

---

### F-6: A missing script exits 2, not 127 — so the exit code cannot distinguish "script absent" from "script refused", and D9's not-found message has no specified trigger
**Severity:** P2
**Where:** spec § D5 (spec.md:151); § D9 (spec.md:236, spec.md:244)
**Edge case:** The operator's config dir is stale (`sync.py install` not run since this spec shipped), or `$CLAUDE_CONFIG_DIR` points somewhere `install` never wrote.
**What happens:** Measured on this repo's interpreter: `python /nonexistent.py` prints `can't open file …: [Errno 2] No such file or directory` and exits **2** — the script's own catch-all code. The skill's exit-2 branch surfaces stderr verbatim and prints `log.md NOT written: python: can't open file …`, losing D9's promised actionable line (`prepend_log_entry.py not found at <path> — install with 'python sync.py install'`). 127 is reachable only when the *interpreter* is missing.
**Why the spec misses it:** :151 asserts "notably **127**, a missing interpreter **or an unresolved script path**" — the second half is wrong for CPython. :244 specifies the not-found message but never says how not-found is detected, and there is no exit code that identifies it.
**Suggested fix:** Correct :151 to attribute 127 to a missing interpreter only, and note that an unresolved script path exits 2. Then specify the trigger in D9: Phase 5 step 4 checks the resolved path exists (`test -f "<path>"`) **before** invoking, and emits D9's message on that check rather than inferring it from an exit code. One added sentence in each place.

---

### F-7: Test case 10's precondition is unreachable via `subprocess`, and its only portable substitute classifies differently on Windows than on POSIX
**Severity:** P2
**Where:** spec § Test plan, case 10 (spec.md:362); against D5 validation step 1 (spec.md:138)
**Edge case:** Running the suite on Windows vs. Linux/macOS.
**What happens:** Case 10 reads "With stdin a tty (or `None`), the script exits 2 promptly with the heredoc hint." A `subprocess`-launched child cannot be given a tty portably (no pty on Windows), so the implementer reaches for `stdin=subprocess.DEVNULL` — and the two platforms then take *different branches*. Measured here: under Git Bash on Windows, `python -c "…isatty()" < /dev/null` prints **True**, because `NUL` is a character device and the CRT's `_isatty` accepts it; on POSIX `isatty(/dev/null)` is false, so the same invocation falls through step 1 to step 2 and produces the **empty-entry** message instead. A test asserting D5's heredoc hint passes on Windows and fails on Linux; a test asserting the empty-entry message does the reverse. The plan's standing "assert the message, not just the code" rule (:341) guarantees one of the two will fail rather than pass vacuously — which is good, but it will fail in CI on whichever platform the author didn't use.
**Why the spec misses it:** D5:138 treats "no stdin attached" and "empty stdin" as cleanly separable conditions. They are, on POSIX; on Windows `/dev/null` lands on the first one. The spec never names how a test supplies either.
**Suggested fix:** Split case 10 into two: (a) a `subprocess` case with `stdin=subprocess.DEVNULL` asserting *either* message via a union match, with a comment recording the `NUL`-is-a-chardev divergence; and (b) an in-process case that patches `sys.stdin` with a stub whose `isatty()` returns True, asserting D5's heredoc hint exactly. Add one line to D5:138 noting that on Windows `/dev/null` satisfies `isatty()`, so `DEVNULL` reaches the "no stdin" branch there and the "empty entry" branch on POSIX.

---

### F-8: Test cases 12 and 13 need an in-process interposition seam the test plan's own division of labour forbids, and `main()`'s stdin contract blocks the precedent helper
**Severity:** P2
**Where:** spec § Test plan preamble (spec.md:339), cases 12 and 13 (spec.md:364-365)
**Edge case:** Implementing "mutate the file between the script's read and its replace" and "a forced mid-write failure".
**What happens:** Both require a hook inside the script's execution, which `subprocess` cannot provide — yet :339 assigns exit-code assertions to `subprocess` ("Unit cases drive `splice()` directly; process-level cases (encoding, exit codes) go through `subprocess`"), and cases 12/13 assert exit codes. Driving `main()` in-process instead runs into two walls the plan doesn't address: the precedent helper `tests/test_session_handoff.py:91` `run_main()` redirects stdout/stderr to `io.StringIO` but leaves `sys.stdin` alone — under `python -m unittest` in a terminal that is a tty, so D5 step 1 fires and **every** such call exits 2 with the heredoc message before reaching the code under test; and `main()` reads `sys.stdin.buffer` (D6 hazard 2), which `io.StringIO` does not have, so a naive stdin fake raises `AttributeError` into the catch-all → also exit 2. Both give a green-looking "exit 2" for the wrong reason; only the standing assert-the-message rule catches it, and only if the author asserts the *right* message.
**Why the spec misses it:** Round 2 closed the analogous stdout/stderr hazard (D6 hazard 3) but the stdin axis was never carried through to the test plan, and cases 12/13 were added without a stated mechanism.
**Suggested fix:** Add to § Test plan: cases 12 and 13 drive `main()` in-process with (a) `sys.stdin` replaced by a stub exposing `isatty() -> False` and `.buffer` over an `io.BytesIO` of UTF-8 entry bytes, and (b) a monkeypatched seam — name one, e.g. wrapping the module's `splice` or `os.fsync` to mutate the target as a side effect — asserting the returned int plus captured stderr. Amend :339's division so it reads "process-level cases *that need no interposition* go through `subprocess`."

---

### F-9: The missing-file outcome still inherits `mkstemp`'s `0600` — D8's mode preservation is scoped to "when the target existed"
**Severity:** P3
**Where:** spec § D8 "Mode is preserved" (spec.md:223); D7 Missing-file row (spec.md:186)
**Edge case:** A fresh wiki with no `log.md`, closed on Linux or macOS.
**What happens:** No target exists, so no mode is captured and no `chmod` runs; `os.replace` carries `mkstemp`'s `0600` onto the new `log.md`. The wiki's operations log is created owner-only, git does not track the bit, and it never appears in a diff or survives a clone — the same working-tree-only, one-way change round-2/F-11 identified for the existing-file case, just on the path that path's fix excluded.
**Why the spec misses it:** :223 opens "When the target exists its `st_mode & 0o777` is captured…", and test 14 (:366) pins only the `0644`-target case, so nothing exercises the created-file mode.
**Suggested fix:** Extend :223: when the target does not exist, `chmod` the temp to `0o666 & ~umask` before the replace. Extend test 14 to assert the created file's mode matches a plain `open(path, "w")` under the same umask.

---

### F-10: "Every outcome leaves the file ending in exactly one `\n`" is unenforceable on the normal outcome, and test 17 asserts it vacuously
**Severity:** P3
**Where:** spec § D7 "Whitespace discipline" (spec.md:199); test case 17 (spec.md:369)
**Edge case:** An existing `log.md` that ends with no trailing newline, or with two.
**What happens:** The normal (prepend) outcome splices at the top and never touches the tail, so the file's ending is whatever it already was — the stated invariant is simply false for that outcome unless the script also rewrites the tail, which would contradict D6:173 all over again (see F-2). Test 17 asserts the invariant "for all three writing outcomes", but every fixture ends in exactly one `\n`, so the normal-outcome half of the assertion can never fail.
**Why the spec misses it:** The invariant was written for the two outcomes that author the tail (fresh-wiki, missing-file) and then generalized to all three.
**Suggested fix:** Scope :199 to the outcomes that author the tail: "The fresh-wiki and missing-file outcomes leave the file ending in exactly one `\n`; the normal outcome leaves the tail untouched, including a missing or doubled trailing newline." Adjust test 17 accordingly, and add a normal-outcome fixture variant with no trailing newline so the assertion is non-vacuous.

---

### F-11: The catch-all exception message has no specified shape, so D5's "every message names the path and the guard" is unmet on the widest exit-2 class
**Severity:** P3
**Where:** spec § D5 (spec.md:153, spec.md:157); § Design (spec.md:296)
**Edge case:** Any failure that reaches `except BaseException` — `ENOSPC`, a nonexistent parent directory, a `mkstemp` failure, a `PermissionError` on the replace, an unexpected `OSError` on `chmod`.
**What happens:** :153 specifies only "message to stderr → `return 2`". `/spec-close` surfaces stderr verbatim and nothing else, so if that message is a bare `repr(exc)` the operator gets `[Errno 28] No space left on device` with no path, no ticket, and no guard — on precisely the failure class where the path matters most. This is the one gap left by round-2/F-8, whose blanket rule at :157 covers the *named* messages.
**Why the spec misses it:** :157 states the requirement; :153 specifies the catch-all without applying it.
**Suggested fix:** Give :153 a concrete format — `<resolved path> (guard: <guard>): unexpected failure: <type>: <exc>` — and note the one carve-out: a failure raised before argparse completes has neither value available, so it emits the exception alone.

---

### F-12: The one load-bearing invocation is Bash-only, in a repo that declares itself harness-neutral
**Severity:** P3
**Where:** spec § Design line-343 rewrite (spec.md:315); D9 (spec.md:238)
**Edge case:** A host whose only shell is PowerShell (the primary shell on this repo's own development machine).
**What happens:** `<<'EOF'` is a parse error in PowerShell, so the step fails before the script runs. It fails loudly — no log entry, exit ≠ 0 — but the skill has no alternate form to fall back to and the operator is left hand-writing the entry.
**Why the spec misses it:** D9 resolves the ambiguity by assuming Git Bash ("the shell `SKILL.md:380`'s tool-use notes assume"), which is a fair reading of today's `SKILL.md`. But `AGENTS.md` opens "Harness-neutral by intent — written for Claude Code, Hermes, or any agent", and `SKILL.md` already gives paired forms elsewhere (Phase 0 step 3: `$env:USERNAME` / `$USER`; step 4: `~/.claude/` / `%USERPROFILE%\.claude\`). The file's own convention is to give both.
**Suggested fix:** Show the PowerShell equivalent beside the Bash heredoc in the line-343 rewrite — a single-quoted here-string piped in, `@'…'@ | python "<path>" "<log>" --guard 'close | … :'` — matching the paired-form convention already in the file. Two lines.

---

### F-13: `except BaseException` swallows argparse's `SystemExit`, so `--help` exits 2 with a spurious error appended
**Severity:** P4
**Where:** spec § D5 (spec.md:153); § Design (spec.md:296)
**Edge case:** An operator runs `prepend_log_entry.py --help`, or omits `--guard`.
**What happens:** § Design puts "parse args" inside the guard ("Everything from `parse args` onward sits inside the D5 exception guard"). `argparse` raises `SystemExit(0)` for `--help` and `SystemExit(2)` for a usage error; both are `BaseException` subclasses, so the guard catches them, prints its own failure message after argparse's output, and returns 2. `--help` succeeding-then-reporting-failure is confusing for a script D5:126 explicitly expects operators to run by hand ("an operator wanting a preview can run the script against a copy").
**Why the spec misses it:** The guard's carve-out list names only `KeyboardInterrupt`.
**Suggested fix:** Add `SystemExit` to the carve-out alongside `KeyboardInterrupt` — re-raise it after cleanup so argparse's own codes (0 for `--help`, 2 for usage) pass through unaltered. Neither collides with the reserved 1.

## Summary
P0: 1 | P1: 0 | P2: 7 | P3: 4 | P4: 1

STATUS: RED P0=1 P1=0 P2=7 P3=4 P4=1
