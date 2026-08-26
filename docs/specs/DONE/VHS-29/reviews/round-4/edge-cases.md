# Edge-Cases Review — round 4

**Grounding (all read fresh from disk this pass):** spec v4 (459 lines) and brief; `CLAUDE.md` → `AGENTS.md` (full); `skills/spec-close/SKILL.md` (400 lines — all nine cited sites verified at their stated line numbers, plus 382 confirmed as the mutation-boundary bullet and 381 as the Write-targets bullet); `skills/session-handoff/scripts/create_handoff.py` (`write_atomically` at :338) and `_sections.py` (`normalize` at :76); `lint.py` (`_read_lines` :63, `lint_path` :243, WARN never affects exit); `tests/test_session_handoff.py` (`run_main` :90, in-test CRLF at :470); `sync.py:33-39`; root `.gitattributes` (`*.md text eol=lf`); `skills/spec-cycle/SKILL.md:1-11`; `docs/authoring-portable-skills.md:41`; live `vigil-harbor-wiki/log.md` (514 lines, header verbatim as the fixture describes) and its `.gitignore` (`.*.tmp`, INFRA-27 comment present). All three round-3 reports read from disk. `scale_lens: off` — no `scalability.md` in `round-3/`; nothing to ignore.

**Two claims verified empirically on this machine rather than by reading**, because both findings below turn on shell semantics:

```
$ if test -f "~/.claude/skills/spec-close/SKILL.md"; then echo found; else echo NOT FOUND; fi
NOT FOUND                     # the file exists; double quotes suppress tilde expansion
$ if test -f ~/.claude/skills/spec-close/SKILL.md; ...      -> found
$ if test -f "$HOME/.claude/skills/spec-close/SKILL.md"; ... -> found

PS> python -c "import sys; sys.exit(1)"; echo "prepend_log_entry_exit=$?"
prepend_log_entry_exit=False   # and False again for exit 2; $LASTEXITCODE carries 1 / 2
```

**Citation convention verified.** `grep -nE "test (case )?[0-9]+|case [0-9]+|tests? 1[0-9]|Test [0-9]"` over the spec returns **zero** hits. The root-cause fix for round-3 F-1 holds; every cross-reference in § Done when, § Scope, D7 and D10 is title-based.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Stale test-case cross-references (P0) | CLOSED | spec:5 citation-convention note; zero numeric hits repo-wide over the spec; § Done when now cites **bold titles** only |
| edge-cases | F-2 | D7 separator normalization falsifies D6's absolute preservation claim | **PARTIAL** | Re-termination half closed (spec:188 names the single boundary line; the newlines case asserts *that line's* terminator). The BOM half added in the same edit is wrong — see F-4 below |
| edge-cases | F-3 | Concurrency baseline captured after the read | CLOSED | spec:226, 240 — `os.fstat(handle.fileno())` with the POSIX inode-swap rationale |
| edge-cases | F-4 | Three-way exit code never made observable | **PARTIAL** | Bash form closed (spec:141 `echo "prepend_log_entry_exit=$?"`, spec:164). The PowerShell form (spec:268-274) carries no echo, and `$?` there is a boolean — see F-2 below |
| edge-cases | F-5 | Guard/path never shell-quoted | **PARTIAL** | Quoting rules stated and justified (spec:144-147). But how `<resolved-script-path>` and `<resolved-path>` are *rendered* is still unspecified, and the two rendering forms D9 names are inert inside the mandated double quotes — see F-1 below |
| edge-cases | F-6 | Missing script exits 2, not 127 | CLOSED | spec:166 attributes 127 to the interpreter; spec:264 adds the `test -f` pre-check |
| edge-cases | F-7 | Test 10 unreachable via subprocess; Windows `NUL` satisfies `isatty()` | CLOSED | spec:151 platform note; the **no stdin** case is split (a) subprocess/DEVNULL (b) in-process stub |
| edge-cases | F-8 | Tests 12/13 need an in-process seam the plan forbids | CLOSED | spec:373-376 — Division of labour, two-part `sys.stdin` stub with both traps named, named monkeypatched seam |
| edge-cases | F-9 | Created file inherits `mkstemp` 0600 | CLOSED | spec:243 covers both paths (`0o666 & ~umask` when created); the **mode** case asserts both |
| edge-cases | F-10 | Trailing-newline invariant unenforceable on the normal outcome | CLOSED | spec:214 scopes the tail rule; `log-no-trailing-newline.md` added |
| edge-cases | F-11 | Catch-all message shape unspecified | CLOSED | spec:170 gives the format plus the before-argparse carve-out |
| edge-cases | F-12 | Bash-only invocation in a harness-neutral repo | **PARTIAL** | The *invocation* gets a PowerShell form (spec:266-274); the two control-flow mechanisms of the same step (`test -f` pre-check, exit-code echo) do not — see F-2 |
| edge-cases | F-13 | `except BaseException` swallows `SystemExit` | CLOSED | spec:168, 328 — both re-raised after cleanup, with argparse's 0/2 passthrough named |
| correctness | F-1 | Four stale test-case citations | CLOSED | same root fix as edge/F-1 |
| correctness | F-2 | `exit 127` wrong attribution | CLOSED | spec:166 |
| correctness | F-3 | Baseline from `stat(path)` not the handle | CLOSED | spec:240 |
| correctness | F-4 | Tail invariant unachievable | CLOSED | spec:214 |
| correctness | F-5 | `SystemExit` swallowed | CLOSED | spec:168 |
| correctness | F-6 | chmod between re-stat and swap | CLOSED | spec:231-233 — chmod now precedes the re-stat, which is the last line before `os.replace` |
| correctness | F-7 | BOM/newline order stated both ways | CLOSED | one order in D6:186, D7:209, § Design:326 |
| conventions | F-1 | CRLF fixture cannot survive its own commit | CLOSED | spec:47 — fixture dropped, in-test construction per VHS-28; `.gitattributes` in § Files to leave alone and § Out of scope. Verified: root `.gitattributes` is `*.md text eol=lf` |
| conventions | F-2 | v2→v3 renumbering left four pointers wrong | CLOSED | same root fix as edge/F-1 |
| conventions | F-3 | § Deferred under-reports v3's additions | CLOSED | spec:446-458 — eleven items |
| conventions | F-4 | Blanket `AGENTS.md` append ban over-broad | CLOSED | spec:407 — content assertion on two substring-located passages |
| conventions | F-5 | Normalizer duplication unexplained | CLOSED | spec:192 "On re-implementing the normalizer" + strict-decode rationale (one wording nit remains — F-12) |

## Findings

### F-1: The mandated double-quoting makes both of D9's own path-resolution forms inert in Bash — the pre-check reports "not found" for a script that is installed, and the entry is never written

**Severity:** P1
**Where:** spec § D9 (lines 258-264), § D5 CLI surface (line 136), § Design site 343 (line 345)
**Edge case:** `<resolved-path>` rendered with the tilde or `%USERPROFILE%` form D9 names, inside the double quotes D5 mandates.
**What happens:** `test -f "~/.claude/skills/spec-close/scripts/prepend_log_entry.py"` is **false for an installed script** — verified above on this machine, in Git Bash, against a file that exists. The skill then takes D9's not-found branch, prints `log.md NOT written: prepend_log_entry.py not found at <path> — install with 'python sync.py install'`, and per D5 continues to step 5 and prints a successful-looking completion block. The operator runs `sync.py install`, it reports success, the next close fails identically. The log entry is never written — the same end state as the VHS-29 bug, with a hint that cannot resolve it. `"%USERPROFILE%\.claude\..."` fails the same way in Git Bash (no expansion *and* consumed backslashes); if that form ever reaches the `<log-path>` slot instead, D5:147 already names the outcome: the **missing-file** path, a stray file in cwd, and **exit 0 reporting `Prepended: log.md`**.
**Why the spec misses it:** D9 states the resolution *order* (`$CLAUDE_CONFIG_DIR` → `~/.claude` → `%USERPROFILE%\.claude\`) and D5 states the *quoting* rule, but nothing states how the resolved value is rendered as a shell token — the one place the two rules interact. `SKILL.md:26` already hands a literal `~/.claude/skills/ship-spec/states.json` to the reader, so the tilde form is the in-file precedent an implementer will follow; and site 26 is being edited by this very spec, which pulls that string further into scope. An absolute machine path cannot substitute (AGENTS.md's conventions bar machine-local paths from tracked files), so the tilde/env form is what will be written.
**Suggested fix:** In D9, add one sentence: *the resolved path is written as `"$HOME/.claude/skills/spec-close/scripts/prepend_log_entry.py"` (or `"$CLAUDE_CONFIG_DIR/skills/…"` when set) — never `"~/…"`, because Bash does not expand a tilde inside double quotes, and never `%USERPROFILE%\…`, which Git Bash leaves literal and whose backslashes are consumed.* Apply the same rule to the `test -f` pre-check, both `python` invocations in D5/D9, and the § Design site-343 bullet.

---

### F-2: The PowerShell branch drops both mechanisms D5 and D9 declare mandatory for Phase 5 step 4 — the exit-code capture (`$?` is a Boolean in PowerShell) and the `test -f` pre-check

**Severity:** P1
**Where:** spec § D9 "Both shells get a form" (lines 266-274); § D5 exit-code table and the echoed-integer rule (lines 156-164); § D9 not-found pre-check (line 264)
**Edge case:** Phase 5 step 4 executed through a PowerShell tool — which this harness declares as the *primary* shell — using the form the spec ships.
**What happens:** Two independent failures.
- **`$?` is a boolean in PowerShell.** Verified above: `python -c "sys.exit(1)"` then `echo "prepend_log_entry_exit=$?"` prints `prepend_log_entry_exit=False`, and so does exit 2. The integer lives in `$LASTEXITCODE`. D5's three-way branch collapses to two, and the case it was raised to protect — an *expected* idempotent skip on the documented "Interrupted execute" / "Partial-then-full re-run" recovery path — is reported as `log.md NOT written` with a spurious recovery hint. As shipped the PS block carries no echo at all, so there is no value to branch on.
- **`test -f` is not a PowerShell command.** It errors (`The term 'test' is not recognized`), the skill reads that as pre-check failure, and takes the not-found branch — the same silent-loss end state as F-1, on an installed script.

**Why the spec misses it:** D9 closes round-3 F-12 by supplying a PowerShell *here-string* — the piece that was a parse error — and stops there. The paragraph's claim ("Both shells get a form") is scoped to the invocation, while D5:164 and D9:264 add two mechanisms *outside* the invocation and specify each only in Bash. § Design site 343 (line 347) likewise lists "both shell forms" for the invocation only.
**Suggested fix:** In D9's PowerShell block, add the two missing lines and name why the naive translation fails:

```powershell
if (-not (Test-Path "$env:USERPROFILE\.claude\skills\spec-close\scripts\prepend_log_entry.py")) { ... }
@'
…
'@ | python "<resolved-script-path>" "<log-path>" --guard 'close | <PROJECT> — <TICKET-ID>:'
"prepend_log_entry_exit=$LASTEXITCODE"   # $? is a BOOLEAN here — False for both 1 and 2
```

and add a sentence to D5's echoed-integer paragraph recording that `$?` carries the integer only in Bash.

---

### F-3: No test case exercises the documented invocation string, which is why F-1 and F-2 are invisible to the suite

**Severity:** P2
**Where:** spec § Test plan "Division of labour" (line 373); § Cases (390-409)
**Edge case:** the shell layer between the skill and `main(argv)`.
**What happens:** Every process-level case goes through `subprocess` with a Python-built argv and piped stdin. That path never sees the guard's ` | `, the path's quoting, the heredoc, the tilde, or `$?` — so the two highest-cost failure modes the spec identifies (D5:146-147's two "load-bearing" quotings, whose failure modes are *exit 0 over an entry that went nowhere*) are asserted in prose and pinned by nothing. The suite stays green through both F-1 and F-2.
**Why the spec misses it:** D5 documents the invocation as a contract but the test plan's division of labour splits only unit / subprocess / in-process — no row owns the shell string itself.
**Suggested fix:** Add a case: **Invocation string.** Under `skipIf(shutil.which("bash") is None)`, run the documented Bash form verbatim via `bash -c` against a tmp fixture, with the script path built the way `SKILL.md` builds it — asserting the entry lands, the guard survives with its em dash and pipe intact, and `prepend_log_entry_exit=0` appears on stdout. A tilde-quoted path fails this case; so does an unquoted guard.

---

### F-4: D6 attributes the existing file's BOM strip to a step that only touches the entry — no step in `main()` strips it

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:188 (D6 "Preservation, stated exactly"); § D5 step 2 (line 152); § Design `main()` sequence (line 326)
**Edge case:** a `log.md` that carries a UTF-8 BOM (the spec itself calls BOM "a known live hazard in this repo").
**What happens:** D6 says *"The existing file's BOM, if any, is likewise dropped by the `lstrip("﻿")` in step 2."* Step 2 is D5's **entry**-side validation (`Empty entry after decode, newline-normalize, BOM-strip, and .strip()`); it never sees the file text. The file is read via `open(path, encoding="utf-8", newline="")`, which preserves `﻿` as a character, and neither D8's sequence nor § Design's `main()` order strips it. So an implementer reading D6 adds an unspecified strip to the existing text (silently rewriting a byte the script did not author, on the very file the header-corruption case guards — and that case asserts from `# Wiki Log` onward, so a dropped BOM slips past it), while an implementer reading § Design does not. Both behaviours are defensible; the spec asserts one and specifies the other.
**Why the spec misses it:** the sentence was added in the round-3 fix for edge/F-2, to bound the preservation claim symmetrically with the boundary-line exception — but it bounded it against a step that does not exist on that side.
**Suggested fix:** Replace the sentence with the behaviour § Design actually produces: *"A BOM on the existing file is preserved — the read does not strip it, and the splice does not touch bytes before the anchor. (A BOM'd file whose first line is a dated entry takes D7's refusal path, loudly, because `ENTRY_RE` cannot match past it.)"* If dropping it is preferred instead, add the strip to `main()`'s ordered sequence and to the header-corruption case's byte assertion.

---

### F-5: Two of D7's four outcomes exit 0 and are reported as `Prepended: log.md`, and the missing-file outcome emits no distinguishing signal at all

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D7 outcome table (lines 196-201); § D5 exit-code table (line 160); § Design site 365 (line 349)
**Edge case:** a `<log-path>` that resolves somewhere other than the live `log.md` — a wrong `wiki_root`, a stale username segment, a typo, or F-1's backslash case.
**What happens:** The **missing-file** row creates the file and exits 0 with no stderr notice specified, and the exit-0 branch reports `Prepended: log.md`. Nothing in the operator-visible output distinguishes "prepended above 514 lines of history" from "created a brand-new headerless file at a path nobody intended". The close then prints its completion block, the operator commits the wiki with `git add -A` (SKILL.md:370), and the stray file ships. The **fresh-wiki** row does emit a notice — but D5's table surfaces stderr only on exit 2, so that notice is dropped too and an entry placed *at the end of the file* is reported as prepended.
**Why the spec misses it:** D5:147 identifies exactly this outcome ("a silent success over an entry that went nowhere") but treats it as an argument for quoting rather than as a reporting requirement; the exit-0 row is a single line that assumes the normal outcome.
**Suggested fix:** Give the missing-file outcome a stderr notice (`<path> did not exist — created with this entry alone; no header synthesized`), and split the exit-0 row of D5's table: report `Prepended: log.md` when stderr is empty, and otherwise surface the notice verbatim as `Created: log.md (did not exist)` / `log.md: no dated entry found — entry placed at end of file`. Add the assertion to the **fresh wiki** and **missing file** cases, which already exercise both paths.

---

### F-6: The test plan never states that fixtures are copied into a temp directory before the mutating cases run

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan (line 371, "Paths resolve from `__file__`, never cwd"); § Fixtures (382, "**This fixture is the test**")
**Edge case:** the second run of the suite.
**What happens:** Taken literally, the **header corruption**, **idempotency**, **guard precision**, **whitespace discipline**, **newlines**, **mode**, **atomic write** and **concurrent change** cases all write to their target. If the target is the checked-in fixture, run 1 mutates `tests/fixtures/spec-close/log-with-entries.md` in the working tree; run 2 sees the guard already present and the **idempotency** case's first insert exits 1 instead of 0. `/ship-spec` goes green on the first pass and carries a mutated fixture into the PR — corrupting the one artifact the load-bearing regression test depends on.
**Why the spec misses it:** the sentence about `__file__` addresses *locating* fixtures, and reads as if it had addressed *isolating* them. The precedent (`tests/test_session_handoff.py`'s `self.tmp`) is right but unstated.
**Suggested fix:** One sentence in § Test plan: *every mutating case copies its fixture into a per-test `tempfile.TemporaryDirectory()` and operates on the copy; the checked-in fixtures are read-only inputs, and no case writes under `tests/fixtures/`.*

---

### F-7: A close-entry body line equal to the heredoc delimiter truncates the entry and executes the remainder as shell commands

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D5 CLI surface (lines 135-142); § D9 PowerShell form (268-274)
**Edge case:** a body containing a line that is exactly `ENTRY` (Bash) or begins with `'@` (PowerShell). Close-entry bodies are multi-hundred-word agent-composed prose over reconciliation text, quoted headings and table fragments.
**What happens:** Bash ends the heredoc at that line. The script receives a **truncated but structurally valid** entry — correct `## [YYYY-MM-DD] close | …` heading, guard present in the first line — so every validation passes, it lands at the top of the wiki log, and exit 0 reports success. The remaining body lines are then handed to the shell as commands, in a repo the close is mid-mutation on (Phase 5 step 3's `git mv`s already applied, both trees uncommitted). The corruption is silent on the log side and arbitrary on the shell side.
**Why the spec misses it:** D5 correctly chooses the *quoted* heredoc (`<<'ENTRY'`), which closes the expansion hazard, and treats delimiter collision as covered by the same choice. It is not — quoting suppresses expansion, not termination.
**Suggested fix:** Change the delimiter to one prose cannot produce — `<<'PREPEND_LOG_ENTRY_EOF'` — in D5, D9 and § Design site 343, and add a sentence saying why a natural-language delimiter is unsafe for a body the skill does not control. (The PowerShell `'@` terminator is far less reachable but the same class; a note suffices there.)

---

### F-8: The echoed exit code is emitted by a command a `set -e` shell never reaches

**Severity:** P3
**Where:** spec § D5 CLI surface (line 141); the echoed-integer rule (line 164)
**Edge case:** a Bash tool that runs commands under `set -e` (harness or profile configuration).
**What happens:** `python …` returning 1 or 2 terminates the shell before `echo "prepend_log_entry_exit=$?"` runs. The skill gets no value for the one branch D5 calls load-bearing, and the two paths where the echo actually matters (skip and failure) are exactly the two that suppress it.
**Why the spec misses it:** the form is correct under default `set +e`, which is what the operator machine runs today — a configuration assumption, not a stated one.
**Suggested fix:** Make the capture `set -e`-proof and say so: `if python "<script>" "<log>" --guard '…' <<'PREPEND_LOG_ENTRY_EOF' … PREPEND_LOG_ENTRY_EOF; then rc=0; else rc=$?; fi; echo "prepend_log_entry_exit=$rc"` — `set -e` is suspended inside an `if` condition.

---

### F-9: The two messages the spec spells out in full both violate D5's own "every message names the path and the guard" rule, and the refusal omits the one datum that makes it actionable

**Severity:** P3
**Where:** spec § D7 refusal row (line 199); § D5 step 4 heading-validation message (line 154); § D5 message rule (line 170)
**Edge case:** the refusal path — a populated `log.md` whose newest heading drifted to `###`, a short date, or a tab after the `]`.
**What happens:** stderr reads `no line-anchored dated entry found in <path>, but <n> heading-like line(s) present — refusing to write; inspect the file`. It names the path but not the guard (D5:170 says every message names both), and — more usefully — it never names *which* line was heading-like. "3 heading-like lines present" in a 514-line file read months later in a transcript sends the operator to `grep`; `first heading-like line: '### [2026-08-25] close | …' (line 10)` is the fix, verbatim. The heading-validation message at :154 has the payload but likewise omits path and guard.
**Why the spec misses it:** D5:170's rule was added for the exit-1, concurrency and catch-all messages and never applied back over the two messages D7 and D5 step 4 had already written out.
**Suggested fix:** Extend both messages to the D5 format and add the offending line to the refusal: `<path> (guard: <guard>): no line-anchored dated entry found, but <n> heading-like line(s) present — first is line <k>: <text> — refusing to write`. Add the substring to the **read-side refusal** case's stderr assertion.

---

### F-10: A wholly unresolved guard template passes both of D4's validations — the property D4 claims catches it does not

**Severity:** P3
**Where:** spec § D4 "Guard shape" (lines 116-121)
**Edge case:** the agent fails to substitute `<PROJECT>` / `<TICKET-ID>` and composes the entry heading from the same unsubstituted template.
**What happens:** the guard is `close | <PROJECT> — <TICKET-ID>:` — it **ends with `:`** and it **is present in the entry's first line**, because both came from the same template. Both checks pass, and a literal-placeholder entry is written permanently to the wiki's operations log at position 1, exit 0, reported as success.
**Why the spec misses it:** D4 states *"an unresolved template or a truncated guard is exactly what an over-broad match looks like"* and offers the trailing-colon check as the catch. The colon check catches *truncation*; it cannot see non-substitution, and the first-line check is a consistency check between two strings that share the same defect.
**Suggested fix:** Either drop the "unresolved template" claim from D4's rationale (leaving truncation as the honest justification), or add a third cheap check — reject a guard containing `<` or `>` with `guard still contains an unresolved placeholder: <guard>` — and a **guard shape** sub-case for it.

---

### F-11: A target deleted between read and replace exits 2 through the catch-all with a misattributed message

**Severity:** P3
**Where:** spec § D8 ordered block (lines 222-234) and the concurrency bullets (247-248)
**Edge case:** the operator (or a rotation script moving entries into `log-archive.md`) deletes or renames `log.md` after the script's read.
**What happens:** the re-stat before `os.replace` raises `FileNotFoundError`. D8 specifies the *comparison* ("mismatch → exit 2") but not the raise, so it falls to D5's catch-all and reports `<path> (guard: <guard>): unexpected failure: FileNotFoundError: …` instead of the `changed under us … — re-run` message written for exactly this situation. Behaviour is safe (nothing is clobbered, `try/finally` reclaims the temp), only the diagnosis is wrong — and the operator is told to treat a re-runnable condition as an unexpected fault.
**Why the spec misses it:** D8's file-absent bullet covers the inverse case (a path that *appears*) but not a baseline that *disappears*.
**Suggested fix:** One clause in D8's first bullet: *"a re-stat that raises `FileNotFoundError` is treated as a mismatch and takes the same `changed under us` message."*

---

### F-12: D6 says the normalizer sequence is "exactly" `_sections.normalize()`; the precedent runs the two steps in the other order

**Severity:** P4
**Where:** spec:192
**Edge case:** none — the two orders are observationally identical (`﻿` is unaffected by newline folding, and a leading BOM stays leading).
**What happens:** nothing at runtime. But `_sections.py:76` is decode → BOM-strip → newline-fold, while D6/D7/§ Design pin decode → newline-normalize → BOM-strip. A reader diffing the two implementations against the word "exactly" spends a minute deciding whether the divergence is deliberate, which is the cost the paragraph exists to avoid.
**Why the spec misses it:** the paragraph was added to close conventions/F-5 (duplication unexplained) and quotes the sequence from the spec's own side.
**Suggested fix:** "Decode, strip the BOM, and fold newlines is the same set of steps as `_sections.py:76` `normalize()` (which orders the last two the other way round — the result is identical, since folding cannot create or move a leading BOM)."

## Summary
P0: 0 | P1: 2 | P2: 5 | P3: 4 | P4: 1

STATUS: RED P0=0 P1=2 P2=5 P3=4 P4=1
