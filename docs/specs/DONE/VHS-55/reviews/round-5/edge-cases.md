<!-- Second post-green delta pass (round 5), re-verifying the fold of every round-4 delta finding and probing the new text. Scope limited to the fold. Transcribed from the subagent hand-back. -->

# Edge-Cases Review — round 5 (delta)

Scope: § Decision 8, Phase 3b intro, irreversible bullet, halt block and wait paragraph, Test plan item 7, Done-when ship-spec bullet, Discharged lines, brief D8 and Done-when. Checked against `skills/ship-spec/SKILL.md:179-277` and the clean-result text of the declared `/ponytail-review` skill (`Looks good. Ship.`). Round-4 reports were not on disk at review time; closure verified against the manifest and the spec text.

## Closure of round 4 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | R4/F-1 | empty-output review counts as success | CLOSED | affirmative no-findings statement or empty findings list required; empty stdout, exit-0 error string, stderr-only error are `failed`; brief matches; variants filed as F-1, F-2, F-3 |
| edge-cases | R4/F-2 | once-per-run `:185` | CLOSED | Phase 3b intro and Decision 8 amend `:185` |
| edge-cases | R4/F-3 | halt names no source; worktree edits | CLOSED | `Command from:` line; primary-checkout and fingerprint sentence |
| edge-cases | R4/F-4 | PR-body line after a halted pass | CLOSED | no PR-body line on a halt; later pass replaces the file and adds `Halted passes:`; form refinement F-5 |
| edge-cases | R4/F-5 | Test plan | CLOSED | item 7 |
| edge-cases | R4/F-6 | reply handling | CLOSED | trim; 1/2; re-print; cannot-wait takes 2; EOF variant F-6 |
| edge-cases | R4/F-7 | edits during the wait | PARTIAL | porcelain comparison misses content edits to already-changed files (F-4) |
| correctness | R4/F-1..F-6 | see correctness lens | NOT VERIFIED HERE | same regions |

Deferred preamble present; D-1 and D-2 well-formed P1 rows; `Discharged:` sections each carry the fold. No routing violation.

## Findings

### F-1: The affirmative-clean test does not define "the return" for a skill run in a subagent
**Severity:** P2 · **Pre-ship recommended:** yes
**Edge case:** review command is a skill in subagent mode (SKILL.md:192): no stdout/stderr/exit code, only the subagent's final message. The subagent could fail to invoke the skill and review the change itself, writing "No findings."
**What happens:** the clean test is written in shell terms; a subagent's paraphrase reads as affirmative, so the irreversible gate passes with no review having run. A literal reader may also refuse ponytail-review's real clean output `Looks good. Ship.`
**Suggested fix:** subagent prompt requires a first line `ran: yes | no — <why>` followed by the reviewer's output verbatim; `ran: no` or a missing line is `failed`; a clean result is the reviewer's documented clean-result text or an explicit no-findings sentence from the reviewer itself; a subagent's own summary never counts.

### F-2: The stderr rule overlaps the non-zero-with-findings carve-out for tools that report findings on stderr
**Severity:** P2 · **Pre-ship recommended:** yes
**Edge case:** `cargo clippy`, gcc/clang `-Wall` write findings to stderr with empty stdout; a clean clippy run prints only progress on stderr.
**What happens:** "continue" and "failed" both match; if `failed` wins, the ticket can never pass the gate.
**Suggested fix:** order the tests: (1) readable findings anywhere → ran, continue; (2) affirmative clean statement → success; (3) otherwise failed. "Stderr-only error" then means an error about the command itself.

### F-3: A reviewer that is silent on success can never pass the irreversible gate, and the halt does not say how to fix it
**Severity:** P2 · **Pre-ship recommended:** yes
**Edge case:** `eslint .`, `flake8`, `shellcheck` print nothing and exit 0 when clean.
**Suggested fix:** when the return was empty, print `(no output, exit <code>)` in place of the error lines and a remedy line (`<command> && echo "no findings"`, declared in the primary checkout); Test plan item 7 gains the exit-0 empty-output case.

### F-4: The porcelain comparison misses edits to already-changed files
**Severity:** P2 · **Pre-ship recommended:** yes
**Suggested fix:** always re-enter Phase 3 on option 1 when the test command is not `N/A`; after it exits green go to step 4b then Phase 3b, not Phase 3's normal flow. Exclusion `docs/specs/TODO/<TICKET-ID>.*` confirmed to cover ship-spec's own files; the dot matters so `VHS-551` is not caught.

### F-5: `Halted passes:` has no position or bullet form; `;` clashes with shell commands; a stopped run keeps only the last halt
**Severity:** P3 · **Suggested fix:** `- Halted passes: <n> (<case> | <case>)` after `- Result:`; also on every halt's skipped-form file after the first.

### F-6: "Any other reply re-prints and waits" can loop on a host whose wait returns empty or EOF immediately
**Severity:** P3 · **Suggested fix:** an empty reply or end-of-input is a host that cannot wait: print once and take 2.

### F-7: "Option 1 is the one permitted re-run" reads as a count of one
**Severity:** P4 · **Suggested fix:** "the only re-run path, available after every halt".

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 2 | P4: 1

STATUS: GREEN
