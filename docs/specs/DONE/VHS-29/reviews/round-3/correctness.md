# Correctness Review — round 3

Grounding: read fresh from disk — spec v3, `VHS-29.brief.md`, all three round-2 reviews, `CLAUDE.md` → `AGENTS.md`, `skills/spec-close/SKILL.md` (all ten cited lines verified at their stated numbers), `skills/spec-cycle/SKILL.md:1-11`, `docs/portability-contract.md:55-92`, `docs/authoring-portable-skills.md:41`, `lint.py`, `sync.py:30-39`, `skills/session-handoff/scripts/create_handoff.py:338-357`, `tests/test_lint.py`, `tests/test_session_handoff.py`, and in the wiki `log.md`, `.gitignore:8`, `.gitattributes`, `.claude/skills/wiki-after-merge/SKILL.md:35-42`. Plane VHS-29 retrieved from namespace `skills` (tag-exact, 1 hit; full description fetched — its five DONE-WHEN items all map to spec Done-when 1–4 and 6). Measured on this machine: `python -V` = 3.14.3; `sys.stdout.encoding` = `cp1252`/`surrogateescape` piped and unpiped; `python <missing>.py` → **exit 2**; missing interpreter → exit 127; `python lint.py skills/spec-close/SKILL.md` → `0 error(s), 1 warning(s)`; live `log.md` = 514 lines / 149,495 bytes / **zero `\r`**; all `close | ` occurrences in `log.md` are entry headings, none in body prose. `git log`: no commit to `skills/spec-close/SKILL.md` in the last 7 days (newest `b9afacd`, 2026-06-14); **`AGENTS.md` moved yesterday** (`40c4bb8`, 2026-08-24) — both cited lines (`:29`, `:100`) re-verified as current, and they remain the file's only `append` occurrences.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Two live `D8` refs should read `D10` | CLOSED | spec:17 (Scope row 3), :34 (authoring-portable bullet); grep for `D8` returns only atomicity refs (:203, :396, :414) |
| correctness | F-2 | D10 cites the wrong test case | **REOPENED** | spec:266 now cites "test case 16"; case 16 is *Newlines, both directions* (:368) — the `requires:` assertion is case 19 (:371). See F-1 below |
| correctness | F-3 | Re-check placement / temp cleanup | CLOSED | D8 write block :207-215 (re-stat before swap), :222 `try/finally`, :221 dot prefix, § Design :296; tests 12/13 (:364-365). Residual nit → F-5 |
| correctness | F-4 | Done-when #1 cited test 15 | CLOSED | Done-when #1 (:386) now cites case 18 and both counts. Same class recurs elsewhere → F-1 |
| correctness | F-5 | Interpreter never named | CLOSED | D9 :238 `python` / `python3` + mode-644 + Git-Bash rationale (git index confirms `100644` on all three shipped scripts) |
| correctness | F-6 | Read-only-target test Windows-only | CLOSED | test 11 (:363) uses directory-as-target as the portable case, read-only *parent* under `skipIf(nt)` |
| correctness | F-7 | Test 15's `AGENTS.md` half stated twice | CLOSED | test 18 (:370) is whole-file counts only |
| correctness | F-8 | Files-to-leave-alone carve-out asymmetry | CLOSED | :47 umbrella rule; phase spans verified against `SKILL.md` headings (0/3/4/5/5) |
| correctness | F-9 | No stat baseline on the missing-file path | CLOSED | D8 :227-228 File existed / File absent rows. Residual → F-3 |
| edge-cases | F-1 | Entry's own heading never validated (P1) | CLOSED | D5 validation step 4 (:141), test case 4 (:356), Done-when #3 (:388), § Deferred (:412) |
| edge-cases | F-2 | Temp not unlinked on the mismatch abort | CLOSED | :222 `try/finally`, not `except`-only; test 13 asserts no leftover |
| edge-cases | F-3 | Newline pinned on writes, neither read | CLOSED | D6 hazard 4 (:168-173) bidirectional; fixture `log-crlf.md` (:43); test 16 |
| edge-cases | F-4 | Read-only-target Windows-only | CLOSED | same as correctness F-6 |
| edge-cases | F-5 | `reconfigure` unavailable on `StringIO` | CLOSED | D6 :167 own `try/except`; standing "assert the message, not just the code" rule (:341) |
| edge-cases | F-6 | No `isatty` guard | CLOSED | D5 step 1 (:138) separates no-stdin from empty-stdin; test 10 |
| edge-cases | F-7 | Halts vs report-and-continue | CLOSED | D5 :155 "A failed log write never aborts the close"; D9 :244 defers to it |
| edge-cases | F-8 | Messages carry neither path nor guard | CLOSED | D5 :157 with concrete message text |
| edge-cases | F-9 | Guard shape unvalidated | CLOSED | D4 :111-116, both failures exit 2; test 9 |
| edge-cases | F-10 | Missing-file path unguarded | CLOSED | D8 :228 |
| edge-cases | F-11 | `mkstemp` 0600 becomes `log.md`'s mode | CLOSED | D8 :223 chmod before replace; test 14 under `skipIf(nt)` |
| edge-cases | F-12 | Whole-text vs first-line asymmetry | CLOSED | D4 :109; verified live — no body prose in `log.md` carries a full guard literal |
| conventions | F-1 | Stale `D8` cross-references | CLOSED | same as correctness F-1 |
| conventions | F-2 | § Deferred under-reports v2's additions | CLOSED | seven items at :410-416 |
| conventions | F-3 | Line-pinned `AGENTS.md` assertion | CLOSED | test 18 (:370) whole-file counts |
| conventions | F-4 | D9 claims parity Phase 0 step 4 lacks | CLOSED | D9 :242 states the divergence; site 26 brought along (`SKILL.md:26` verified to name only the two defaults) |
| conventions | F-5 | Duplicating `write_atomically()` | CLOSED | D8 :232 |
| conventions | F-6 | Shebang / `requires:` position unpinned | CLOSED | § Design :280; D10 :258 (contract's position rule at `portability-contract.md:92` verified) |

## Findings

### F-1: Four stale test-case citations — § Scope (×2), D7, and D10 all point at tests that now assert something else
**Severity:** P1
**Where:** spec.md:29, :33, :201 (all "test case 15"); spec.md:266 ("test case 16")
**Claim:**
- `:29` — "Test case 15 asserts **both** counts, because a zero-`append` assertion alone cannot see three of the nine."
- `:33` — "…so test case 15 can assert a whole-file count of zero."
- `:201` — "test case 15 asserts zero occurrences in `SKILL.md`, and a correct implementation must not trip its own tripwire."
- `:266` — "…which is why **test case 16** asserts the declared set against the tool-use notes rather than trusting the lint."

**Why this is wrong:** v3's expanded test plan renumbered. Test case **15** is now *"Em dash + BOM round-trip"* (spec.md:367) and test case **16** is *"Newlines, both directions"* (spec.md:368). The wording tripwire is case **18** (spec.md:370) and the `requires:` assertion is case **19** (spec.md:371) — which Done-when #1 (:386) and #5 (:390) and § Deferred (:415) all cite correctly. So the spec states, in four places across three sections, that two tests assert things they do not, and each of those sections is the *rationale* section an implementer reads before writing the test.

`:266` is a direct reopen of round-2 correctness F-2 (same root: D10 cites the wrong test number). The closure manifest acknowledges the renumbering — "renumbered to 19 in v3's expanded plan; Done-when #5 cites 19 and 20" — so Done-when was updated and D10 was not. No rationale is recorded for a deliberate change of direction, so per the closure rule this is a reopen, not a redirection.

**Suggested fix:** `:29`, `:33`, `:201` → "test case 18". `:266` → "**test case 19**". While in there, consider making § Scope and D7 refer to the test by name ("the standing no-stale-wording assertion") rather than by number, since this is the second round in which plan renumbering has broken these pointers.

### F-2: `exit 127` is the wrong code for an unresolved script path — CPython exits 2, which collides with the script's own catch-all
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D9 (spec.md:236); spec § D5 (spec.md:151); spec § D9 (spec.md:244)
**Claim:** D9: "An invocation written as `python skills/spec-close/scripts/prepend_log_entry.py …` … would work for VHS-29's own close run and **silently fail (exit 127)** everywhere else." D5: "Any other exit code — notably **127**, a missing interpreter **or an unresolved script path** — is treated as failure, never as success or skip."
**Why this is wrong:** Measured on this machine (Python 3.14.3, and again on the 3.13 `python3` shim):

```
$ python nonexistent_script_xyz.py; echo "exit=$?"
C:\Python314\python.exe: can't open file '...nonexistent_script_xyz.py': [Errno 2] No such file or directory
exit=2
$ nosuchinterp99 foo.py; echo $?
bash: nosuchinterp99: command not found
127
```

127 is the *shell's* "command not found" — it applies to a missing **interpreter**, never to a missing script path. An unresolved script path exits **2**, with a loud CPython message on stderr (so "silently" is also inaccurate).

Two consequences, neither fatal but both worth pinning:
1. The wrong-cwd failure D9 exists to prevent lands on **exit 2** — the script's own catch-all — so it is correctly reported as `log.md NOT written: <stderr>`. The design still behaves right; only the rationale is wrong.
2. Because of that collision, D9's promised message — `log.md NOT written: prepend_log_entry.py not found at <path> — install with 'python sync.py install'` (spec.md:244) — cannot be derived from the exit code. The skill surfaces stderr verbatim (D5 :157), so what the operator actually sees is CPython's `can't open file …`, not the crafted install hint. The spec never says how `SKILL.md` distinguishes not-found.

**Suggested fix:** In D5:151 say "Any other exit code — notably 127, a **missing interpreter** — is treated as failure"; add that a missing *script path* surfaces as exit 2 with CPython's `can't open file` on stderr, which the exit-2 row already handles. In D9, either (a) drop the crafted not-found message and let CPython's stderr carry it, or (b) state the mechanism — `SKILL.md` checks the resolved path exists before invoking, and emits the install hint itself.

### F-3: D8's concurrency baseline is taken from `stat(path)` after the read, not from the handle that was read — a rename during the read is undetected
**Severity:** P3
**Where:** spec § D8 "Concurrency" (spec.md:225-228)
**Claim:** "The baseline captured immediately after the read is re-checked immediately before `os.replace`… **File existed:** `st_mtime_ns` and `st_size`. Mismatch → exit 2."
**Why this is wrong:** If `/wiki-after-merge` (the second writer D8 names) lands its own `os.replace` between our `open()` and the completion of our `read()`, POSIX rename swaps the inode: our open handle continues reading the *old* file to completion, but the post-read `stat(path)` returns the **new** file's `st_mtime_ns`/`st_size`. That value becomes the baseline, the re-stat before the swap matches it, and we replace the file with content spliced from the old inode — silently losing the interleaved write, which is precisely the outcome D8 says the check exists to prevent ("because the loser's entry is gone the guard will not detect the loss on any later run either"). The window is small (~146 KB read) but it is the one window the stated protocol does not cover, and D8's "closes the multi-second window this script actually opens" is stated as if it covered the whole read-to-replace span.
**Suggested fix:** Capture the baseline with `os.fstat(handle.fileno())` on the handle the content was actually read from, rather than `os.stat(path)` after the close. One line, no new behavior, and it makes the baseline describe the bytes in hand.

### F-4: "Every outcome leaves the file ending in exactly one `\n`" is unachievable in the normal outcome without rewriting bytes D6 says the script never touches
**Severity:** P3
**Where:** spec § D7 "Whitespace discipline" (spec.md:199) vs § D6 (spec.md:173); test case 17 (spec.md:369)
**Claim:** D7: "Every outcome leaves the file ending in exactly one `\n`." D6: "the script splices text and never rewrites lines it did not author."
**Why this is wrong:** In the normal (prepend) outcome the script inserts before the anchor and leaves everything after it byte-identical, so the file's tail is whatever the existing `log.md` had. If a `log.md` ends with no trailing newline, or with three, the result does too — the invariant does not hold. Enforcing it requires right-stripping and re-adding `\n` at EOF, i.e. rewriting bytes the script did not author, which D6 forbids. Test case 17 asserts the invariant "for all three writing outcomes", but its fixtures are all well-formed, so it passes either way and the implementer gets no signal about which rule wins.
**Suggested fix:** Scope the invariant: "The fresh-wiki and missing-file outcomes leave the file ending in exactly one `\n`; the normal outcome leaves the file's tail untouched." Adjust test 17 to assert the tail is byte-identical in the normal outcome, and add a fixture whose tail is not well-formed so the choice is pinned rather than incidental.

### F-5: The `except BaseException` guard swallows `SystemExit` as well, so `--help` exits 2 and argparse's own exit is re-labeled
**Severity:** P3
**Where:** spec § D5 (spec.md:153); § Design (spec.md:296)
**Claim:** "`main()`'s body is therefore wrapped in `try/except BaseException` → message to stderr → `return 2`, with `KeyboardInterrupt` re-raised after cleanup"; and "Everything from `parse args` onward sits inside the D5 exception guard."
**Why this is wrong:** `SystemExit` is the other `BaseException` subclass that argparse actually raises. With `parse args` inside the guard, `prepend_log_entry.py --help` raises `SystemExit(0)`, is caught, gets an unexplained error message on stderr, and returns **2**; a genuine argparse usage error (already `SystemExit(2)` with its own stderr message) gets a second, redundant message layered on. The spec carves out `KeyboardInterrupt` for exactly this reason and stops one exception short.
**Suggested fix:** Add `SystemExit` to the carve-out — `except (KeyboardInterrupt, SystemExit): cleanup; raise` before the `except BaseException` arm — or move `parse args` outside the guard. Either way, state it in D5 alongside the `KeyboardInterrupt` sentence.

### F-6: D8's write block annotates the re-stat as "the last thing before the swap", and the next line of the same block is `os.chmod`
**Severity:** P4
**Where:** spec § D8 (spec.md:212-214); § Design (spec.md:296)
**Claim:** The block reads `→ re-stat and compare against the baseline ← the last thing before the swap` / `→ os.chmod(temp, original mode) when the target existed` / `→ os.replace(temp, target)`; § Design says "the D8 write block, whose re-stat sits immediately before `os.replace`".
**Why this is wrong:** The code block contradicts its own inline annotation and the § Design prose one line later — there is a `chmod` between. Harmless in effect (microseconds), but this is the same section round-2 correctness F-3 was raised against, and implementers follow the code block.
**Suggested fix:** Move `os.chmod(temp, original mode)` above the re-stat line. The mode is captured with the baseline anyway, and the annotation then becomes literally true.

### F-7: BOM-strip / newline-normalize order is stated in both orders
**Severity:** P4
**Where:** spec § D6 (spec.md:171) and § Design (spec.md:296) vs § D7 (spec.md:194)
**Claim:** D6: "The decoded entry is normalized (`replace("\r\n", "\n")…`) **before the BOM strip**"; § Design: "decode UTF-8, normalize newlines, strip BOM, strip". D7: "The entry text is **BOM-stripped, newline-normalized**, then `.strip()`ed before use."
**Why this is wrong:** Functionally identical (normalization neither creates nor consumes a BOM), so nothing breaks — but the spec asserts a specific order in two places and the opposite in a third, which reads as though the order were load-bearing.
**Suggested fix:** Make D7:194 read "newline-normalized, BOM-stripped, then `.strip()`ed", matching D6 and § Design.

## Summary
P0: 0 | P1: 1 | P2: 1 | P3: 3 | P4: 2

STATUS: RED P0=0 P1=1 P2=1 P3=3 P4=2
