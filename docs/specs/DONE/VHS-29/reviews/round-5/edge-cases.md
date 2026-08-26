# Edge-Cases Review — round 5 (delta-only)

Full report as returned by the reviewer. Grounding: spec v5 (479 lines), brief, CLAUDE.md/AGENTS.md,
round-4 reports for all three lenses. `scale_lens: off`, no stale `scalability.md`. Three
measurements run live in this repo's Git Bash / Python 3.14.

## Closure of round 4

All 24 round-4 findings CLOSED except edge-cases F-8 (PARTIAL — code block fixed, prose not; see F-1).
Verified live that D9's new form works: `SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/..."` -> `test -f`
found, and MSYS handed python `C:/Users/zioni/.claude/...`.

## Findings

### F-1: D5 specifies the exit capture two contradictory ways — and the surviving `$?` form reports success on every failure
**Severity:** P0
**Where:** spec.md:170 and spec.md:472, against the code block at spec.md:138-145

After a `fi`, `$?` is the status of the last command *inside* the block (the `rc=` assignment),
always 0. Measured:

    if python -c 'import sys; sys.exit(2)' <<'PREPEND_LOG_ENTRY_EOF'
    ...
    PREPEND_LOG_ENTRY_EOF
    then rc=0; else rc=$?; fi
    echo "rc_form=$rc"      -> rc_form=2
    echo "dollarq_form=$?"  -> dollarq_form=0

An implementer transcribing line 170's fragment emits `prepend_log_entry_exit=0` for a refusal, a
concurrent-change abort, or a PermissionError. The exit-0 branch then prints `Prepended: log.md`
over a log.md that was never written — worse than the original `set -e` bug, because it also fires
with `set -e` off.

**Fix:** substitute the `$rc` form at both sites; add a negative assertion to **Invocation string**
that a failing run reports a non-zero `prepend_log_entry_exit=`.

### F-2: A BOM on `log.md` does not take D7's refusal path — the anchor skips the newest entry and the new entry lands *second*, silently
**Severity:** P1
**Where:** spec.md:196 (D6, rewritten this round); corroborated at spec.md:211 (D7)

v5 correctly moved D6 to "the file's BOM is preserved", then claimed the consequence is a loud
refusal. Measured against D2's and D7's exact regexes:

- **2+ entries:** `ENTRY_RE` skips the BOM'd first heading and matches the second. The **Normal**
  row fires — entry spliced above entry #2, i.e. below the current newest. Exit 0, `Prepended:`,
  silently out of newest-first contract. VHS-29's own bug, reproduced through the fix.
- **One entry:** neither pattern matches (`^#{2,6} *\[` is defeated the same way), so the
  **Fresh wiki** row fires and the entry lands at the *end* of a file that demonstrably has an
  entry — contradicting line 211's guarantee.

Line 211's list names "or a BOM" as something the refusal now catches; false in both shapes.

**Fix:** run the patterns over the text with a leading BOM removed and offset matches by 1, so the
BOM is preserved in output and invisible to the anchor; delete the refusal sentence; drop "or a
BOM" from line 211; add a read-side BOM case.

### F-3: The exit-0 split branches on "stderr empty vs not", but the invocation neither isolates nor captures stderr
**Severity:** P2 · **Pre-ship recommended:** yes
"Empty" is not a value the caller holds — it is a judgement over interleaved tool output that one
stray `DeprecationWarning` inverts. **Fix:** print `prepend_log_entry_outcome=prepended|fresh|created`
on stdout and branch on that token.

### F-4: The two exit-0 notices are specified twice with different text, and D5's rendering drops the path
**Severity:** P2 · **Pre-ship recommended:** yes
D7 line 209 specifies a path-bearing notice; the table renders it as `Created: log.md (did not
exist)` with the path removed — while instructing the skill to surface it "verbatim". An operator
hit by the unquoted-backslash trap cannot learn *where* the stray file was created.

### F-5: D5's canonical invocation is, by delta 3's own new rule, an invocation that exits 2
**Severity:** P2 · **Pre-ship recommended:** yes
The block carries `--guard 'close | <PROJECT> — <TICKET-ID>:'` and a `## [YYYY-MM-DD]` heading;
both are now rejected. **Invocation string** asserts exit 0 from running it "verbatim".

### F-6: D5's unquoted-Windows-path failure trace is stale under delta 2
**Severity:** P3
The trace ends "exits 0 reporting `Prepended: log.md`" — after delta 2 the missing-file outcome
reports the created-notice instead.

## Summary
P0: 1 | P1: 1 | P2: 3 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=1 P2=3 P3=1 P4=0
