<!-- Second post-green delta pass (round 5), re-verifying the fold of every round-4 delta finding. Scope limited to the fold. Transcribed from the subagent hand-back. -->

# Correctness Review — round 5 (delta)

Read spec (353 lines), brief, `skills/ship-spec/SKILL.md` :1-320 and :420-436 fresh from disk. Round-4 reports were not yet on disk at review time; closure checked against the orchestrator's manifest plus the spec text. Every ship-spec anchor the delta cites still matches current text: :60, :71-73, :144, :183, :185, :187-195, :432-433.

## Closure of round 4 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | once-per-run `:185` unamended | CLOSED | Phase 3b intro amends `:185`; Decision 8 says the same |
| correctness | F-2 | Discharged lines vary the § 2e shape | CLOSED | both lines identical, all named sections exist and carry the fold |
| correctness | F-3 | no error-excerpt slot | CLOSED | line 2 of the halt block, "failed case only" |
| correctness | F-4 | no Test plan item | CLOSED | item 7 |
| correctness | F-5 | spec edit at the halt leaves marker `changed` | CLOSED | sentence in the halt block; fingerprint covers the whole spec (SKILL.md:22, :31) |
| correctness | F-6 | brief/spec wording | CLOSED | brief D8 and both Done-when bullets match; one P4 leftover below |
| edge-cases | F-1 | empty-output review counted as success | CLOSED | affirmative no-findings statement required; empty stdout, exit-0 error string, stderr-only error are `failed`; `big` keeps SKILL.md:195 |
| edge-cases | F-2 | once-per-run | CLOSED | as correctness F-1 |
| edge-cases | F-3 | halt names no source; primary-checkout rule | CLOSED | `Command from:` line; sources match step 4b (:72-73); primary-checkout claim holds (:128); worktree copy would be staged (:283) |
| edge-cases | F-4 | PR-body line after a halted pass | CLOSED | no PR-body line on a halt; later pass sets the only line; `Halted passes:`; consistent with step 8 (:251-277) |
| edge-cases | F-5 | test plan | CLOSED | item 7 |
| edge-cases | F-6 | any other reply ended the run | CLOSED | trim; 1/2; otherwise re-print |
| edge-cases | F-7 | worktree edits during the wait untested | PARTIAL | re-entry added, but the porcelain comparison misses the common case (F-1 below) |

## Findings

### F-1: The `git status --porcelain` check misses edits to files the implementation already touched
**Severity:** P2 · **Pre-ship recommended:** yes
**Why this is wrong:** porcelain prints status code and path only; every implementation file is already ` M`/`??` at the halt, so a second edit leaves the output byte-identical, and a new file under an untracked directory collapses into `?? dir/`. Edits to implementation files skip Phase 3 and are committed untested on the irreversible tier. Test plan item 7 inherits the gap.
**Suggested fix:** drop the comparison and always re-enter Phase 3 on option 1 when the test command is not `N/A`; or compare content (hash of `git diff HEAD --binary` plus hashed untracked file contents, same exclusion). Update item 7.

### F-2: "the one permitted re-run" reads as a count limit next to "This loop has no cap"
**Severity:** P3 · **Suggested fix:** "option 1 is the only route to another pass; uncapped because each pass needs an operator action."

### F-3: The brief's Scope row for ship-spec still says "a clean review" without the affirmative requirement
**Severity:** P4 · **Suggested fix:** "a review that affirmatively states no findings".

### F-4: Grounding gaps: round-4 reports not on disk; ticket not cached
**Severity:** P3 · process note; persist the delta-pass reports under `round-4/`.

No contradictions between the delta text and unchanged regions: `small` and `big` bullets keep today's skips and the `:185` rule; Discharged lines satisfy discharge verification; both D-rows well-formed; preamble present; ceiling does not apply (P1 rows).

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 1

STATUS: GREEN
