<!-- Post-green delta pass (round 4), dispatched by the orchestrator after folding Deferred rows D-1 and D-2 under the operator's standing ruling that in-scope P1s fold. Scope limited to the fold. Transcribed from the subagent hand-back. -->

# Edge-Cases Review — round 4 (delta)

Regions reviewed: spec § Decision 8, Phase 3b irreversible bullet and halt block, § Done when ship-spec bullet, D-1/D-2 `Discharged:` lines, brief D8 / Scope row / Done when; also § Test plan against the irreversible path. Ticket not retrieved (memory denied); the brief is the record.

## Closure of round 3 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `## Tier` with no Level line has no halt | CLOSED | brief-parse step halts `tier: malformed (no Level line)`; Test plan item 6 |
| correctness | F-2 | `git worktree remove` discards a dirty tree | CLOSED | halt block corrected |
| correctness | F-3 | workflow reference N/A clause | CLOSED | gate runs for big/irreversible/absent, small skips |
| correctness | F-4 | ticket not cached | CLOSED | no spec change asked |
| edge-cases | F-1 | same as correctness F-1 | CLOSED | — |
| edge-cases | F-2 | malformed tweak-surface line | CLOSED | `surfaces: unknown`, `never tweak`, quote |
| edge-cases | F-3 | ticket body not readable | CLOSED | no spec change asked |
| correctness (manifest) | D-1 / R1 F-4 | irreversible re-run cannot resume the worktree | CLOSED (discharged) | option 1 re-resolves 4b and runs Phase 3b in the same run; halt prints worktree and branch; Done when and brief D8 carry the fold |
| edge-cases (manifest) | D-2 / R1 F-3 | clean irreversible review specified as the failed halt | CLOSED (discharged), variant filed as F-1 | both carve-outs kept, but "found nothing" has no criterion separating it from "nothing readable" |

Deferred preamble present; D-1 and D-2 well-formed P1 rows; `Discharged:` sections each carry the fold. No routing violation.

## Findings

### F-1: An empty-output review counts as success for `irreversible`
**Severity:** P1
**Where:** § Decision 8; irreversible bullet; SKILL.md:195, :273
**Edge case:** review command exits 0 and prints nothing (auth failure to stderr only; empty subagent turn; `true`/`echo`); or exit 0 with a prose "Error:".
**What happens:** SKILL.md:195 has two outcomes that both fit: "nothing readable" → failed, "ran and found nothing" → success. For `irreversible` that decides between halt and commit; an agent can read empty output as clean, write zero counts, mark `[x]`, and commit. The gate brief D2/D8 says fails closed passes silently on a broken reviewer.
**Suggested fix:** "found nothing" must be affirmative (explicit no-findings statement or empty findings list in the review's report shape); empty stdout, no findings structure with no clean statement, error string with exit 0 are `failed` for `irreversible`; say whether stderr counts. `big` keeps today's reading.

### F-2: The once-per-run rule contradicts option 1's re-run
**Severity:** P2 · **Pre-ship recommended:** yes
**Where:** Phase 3b intro; SKILL.md:185 · **Suggested fix:** amend `:185`: counts passes that ran (steps 4–8); a halt pass does not use up the one run.

### F-3: The halt does not say which file supplied the bad command, or that edits must go in the primary checkout
**Severity:** P2 · **Pre-ship recommended:** yes
**Edge case:** operator fixes AGENTS.md while the spec's broken line wins (step 4b order); or edits CLAUDE.md/AGENTS.md inside the worktree, which step 4b never reads and Phase 4 would commit. Editing the spec changes its fingerprint.
**Suggested fix:** print `Command from: <absolute source path § section>` (or the three checked paths for no-command); say edits go in the primary checkout; mention the fingerprint.

### F-4: A halted pass leaves no defined PR-body line
**Severity:** P2 · **Pre-ship recommended:** yes
**Edge case:** pass 1 halts (`not available`/`failed`), pass 2 runs with findings; today's `- [ ] Review gate: skipped — <case>` line could coexist with the `[x]` ran line.
**Suggested fix:** a halted pass keeps no PR-body line; the pass that runs sets the only one and step 8 replaces the review file whole; optionally `Halted passes: <n> (<cases>)` in the review file.

### F-5: The test plan has no checks for the irreversible path
**Severity:** P2 · **Pre-ship recommended:** yes · **Suggested fix:** add item 7 (three halts, clean success, non-zero-with-findings continues, option 1 same run, option 2 and cannot-wait stop, `changed`-confirmed still halts).

### F-6: Any reply other than `1` permanently ends the automated path
**Severity:** P3 · **Suggested fix:** trim; `1` re-run, `2` stop, re-print on anything else; cannot-wait takes 2.

### F-7: Worktree edits made during the wait are committed untested
**Severity:** P3 · **Suggested fix:** on option 1, if the worktree changed since the halt and the test command is not N/A, re-enter Phase 3 with a fresh count before Phase 3b.

### F-8: Ticket body not checked
**Severity:** P4 · environmental.

Other probes, no finding: cannot-wait on a second pass (takes 2 on the first); `--force` advice safe (worktree is always the sibling `../<TICKET-ID>-worktree`); N/A test command with irreversible; brief/spec consistency.

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=4 P3=2 P4=1
