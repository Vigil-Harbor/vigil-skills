# Correctness Review — round 5 (delta-only)

Full report as returned by the reviewer. Grounding: spec v5 (479 lines), brief, all three
round-4 reports, AGENTS.md. Delta-scoped: only code anchors touched by a v5 delta were
re-verified. Re-confirmed live — SKILL.md still 400 lines, unchanged since b9afacd; all nine
sites at their stated numbers; `grep -in append` -> 4, `grep -n "grep -F"` -> 4. Delta-7's
cross-skill claim exact: spec-close:26, ship-spec:41, spec-cycle:235 all use the two-default
rule, and CLAUDE_CONFIG_DIR appears only in sync.py and README.md. Delta-9's seam anchor exact
(test_session_handoff.py:567). Delta-10's stale-count claim exact (filemap.md:164). Zero numeric
test-case citations remain.

## Closure of round 4

All 24 round-4 findings CLOSED except edge-cases F-8 (PARTIAL — the `set -e` fix landed in the
code block but not in the prose; see F-1).

## Findings

### F-1: The `set -e` fix landed in the code block but the prose still prescribes the broken form — and the prescribed form always echoes `0`
**Severity:** P0
**Where:** spec.md:170 and spec.md:472, against the code block at spec.md:143-144

In `if cmd; then rc=0; else rc=$?; fi`, the compound command's status is that of the last command
in the taken branch — an assignment — so `fi` always returns 0. An `echo "prepend_log_entry_exit=$?"`
placed after it prints `0` unconditionally, on the guard-skip path (exit 1) and every failure path
(exit 2) alike. D5 spends its longest paragraph establishing that the skill must branch on this
integer; transcribing spec:170's literal makes the branch read 0 forever, so a refusal, a
concurrency abort and a PermissionError all print `Prepended: log.md`. § Design line 363 says the
invocation lands "verbatim", so an implementer has two mutually exclusive instructions for the
single most load-bearing line of the new Phase 5 step.

**Fix:** point spec:170 and spec:472 at the `$rc` form; state why `$?` there is always 0.

### F-2: D9 mandates `python3` on Unix; the block § Design orders written "verbatim" hardcodes `python`
**Severity:** P1
**Where:** D9 line 266 vs the CLI block at spec:135-145 and § Design line 363

v5's deltas 1 and 8 closed the interpreter question in the wrong direction: § Design instructs the
implementer to transcribe one Bash block verbatim, and that block names `python` only. On a stock
Debian/Ubuntu host (no `python-is-python3`) the documented invocation returns 127 and every close
prints `log.md NOT written: python: command not found`. The **Invocation string** case runs the
form verbatim, so the suite fails there too, pointing at the shell layer rather than the
interpreter name.

**Fix:** resolve into `$PY` in the preamble; have D9 point at the variable.

### F-3: D5's exit-0 notice row says "surface the notice verbatim" then gives a non-verbatim string
**Severity:** P2 · **Pre-ship recommended:** yes
The second example (`Created: log.md (did not exist)`) shares no words with D7's actual notice.

### F-4: D4's new placeholder check makes D5's "shown exactly as it must be written" template self-rejecting
**Severity:** P2 · **Pre-ship recommended:** yes
Run literally, the documented form now exits 2 on the `<`/`>` check, and the **Invocation string**
case asserts an outcome literal execution cannot produce.

### F-5: D4's third guard check has no test case
**Severity:** P2
The highest-consequence of the three checks — an unsubstituted guard lands a literal-placeholder
entry permanently at position 1 — and the **Guard shape** case still pins only two failures.

### F-6: D6's replacement BOM claim is right about preservation but over-general about the refusal
**Severity:** P2
`ENTRY_RE` is `re.M`-anchored, so in a BOM'd file with two or more dated entries the anchor binds
to entry 2 and the new entry is spliced into second place, exit 0, empty stderr — a silent
newest-first violation, not the loud refusal the sentence promises.

## Summary
P0: 1 | P1: 1 | P2: 4 | P3: 0 | P4: 0

STATUS: RED P0=1 P1=1 P2=4 P3=0 P4=0
