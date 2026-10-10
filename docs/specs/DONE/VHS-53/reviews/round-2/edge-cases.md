The fallback command matches the round-1 fix on git 2.55. One silent wrong-PR path is still specified, and the re-entry wording can drop a corrected lookup.

# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Newest `(#N)` mention is treated as the squash-merge SHA | CLOSED | spec § Decision 2 (lines 32–36), § Phase 2a step 2 (lines 86–95), review checklist (line 130). Re-checked on git 2.55.0.windows.5: the specified argv returns one one-parent subject hit for `(#36)` (`8d404d00`); `--exclude=<full-ref> --all` drops a uniquely reachable tip; a body mention is not a subject hit. |
| edge-cases | F-2 | Non-numeric `<N>` makes `gh` exit 0 for a different PR | REOPENED | Still specified at lines 74–76. § Deferred (P2+) and § Out of scope decline a digits check. Deliberate direction — not escalated to P0. Re-filed below at the original P2; `## Deferred (P2+)` is not a well-formed `D-n` row. |
| edge-cases | F-3 | `-F` rationale is false and points at the regex mode that over-matches | CLOSED | spec.md:90 now says default BRE already treats unescaped parentheses as literal and `-F` blocks `grep.patternType=extended` / `-E`. Confirmed: extended grep without `-F` selects `close(vhs-51)` for `(#36)`; with `-F` it selects the squash subject. |
| edge-cases | F-4 | The one warning line collapses distinct `gh` failures | REOPENED | Lines 82–84 and 160 keep one fixed line; Decision 2 and the brief require that. Deliberate — not escalated (original P3). Not re-filed. |
| correctness | F-1 | Default `git log --grep` does not treat `(#N)` as a group | CLOSED | Same sentence as edge-cases F-3, spec.md:90. |
| correctness | F-2 | ticket not cached | CLOSED | spec.md:163 records the denial. This run was told the `skills` namespace is ACL-denied and to use the brief. The round-1 fix was no spec edit. |
| conventions | F-1 | Spec-level command pins the brief left open | CLOSED | spec.md:36 labels the argv, the `#` strip, and the discarded `gh pr view` as pins the brief left open. spec.md:90 drops the false "same reach as step 1a" claim. |
| conventions | F-2 | Whole-tree diff allowlist is not the repo's leave-alone form | REOPENED | spec.md:139 is still the inverted allowlist; line 161 declines the VHS-51 form on purpose. Deliberate — original P3, not escalated, not an edge-case re-file. |

## Findings

### F-1: Empty or branch `<N>` skips the fallback when `gh` exits 0
**Severity:** P2
**Where:** spec.md:74–76 (spec § Phase 2a step 2)
**Edge case:** `<N>` is empty (the step 1c answer was empty or `#` only — one leading `#` is stripped, nothing else is trimmed), or it is a branch name. `gh pr view` / `gh pr diff` take `[<number> \| <url> \| <branch>]`, and with no argument both use the current branch's PR (gh help text on this machine).
**What happens:** Both commands can exit 0 for that other PR. The spec then uses the diff and does not run `git log` or the step 1c prompt. Phase 2c writes a reconciliation report for the wrong PR. The same path runs again when the new fallback prompt re-enters "this same step."
**Why the spec misses it:** Success is defined only as both exits 0. Line 74 forbids any trim or digits check. Round-1 F-2 is restated under `## Deferred (P2+)` rather than handled. The review checklist does not mention it.
**Suggested fix:** Before either `gh` call, trim whitespace. If `<N>` is not one or more decimal digits, do not run `gh` or `git log`; print the step 1c prompt. Apply the same check to a re-entered answer. If a digits guard stays out of scope, say explicitly that an empty or non-numeric `<N>` for which `gh` exits 0 is accepted as that other PR and is not a fallback case.

### F-2: Re-entry tells the agent both to rerun the lookup and to stop searching
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:80 and spec.md:95 (spec § Phase 2a step 2)
**Edge case:** `git log` returns zero accepted lines or more than one, the operator enters another PR number, and `gh` fails again. Separately, an agent re-submits the identifier that just failed.
**What happens:** Line 95 says to read the answer with this same step (which line 80 says must print the one warning and run `git log`) and that a PR number whose lookup succeeds ends the prompt. The same sentence says the automated search ends at the prompt, with no second warning and no new prompt. One reading never calls `gh` or `git log` on the corrected PR number, so a number that would resolve is stuck at the prompt. The other reading warns again, which violates "exactly one warning" / "no second warning." Zero matches and several matches use the same prompt, so a retry of the same number loops with no signal that a SHA is now required. The checklist does not cover a second answer.
**Why the spec misses it:** The three constraints are in one sentence and are not ordered. "No attempt counter" is intentional; it does not say which instruction wins when they conflict, or that the agent must not invent the next answer.
**Suggested fix:** State that each operator answer is classified and read with this step again; a PR number may call `gh` and, on failure, the one `git log`; a SHA takes the SHA branch. Print the warning only on the first `gh` failure of the close. On another miss, reprint the same step 1c prompt and wait. Do not resubmit the identifier that just failed. Add that sentence to the review checklist.

### F-3: The one accepted line can be a local commit that only looks like the squash
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:90–95 (spec § Phase 2a step 2)
**Edge case:** `origin` fetch already failed (Phase 0 logs `origin: fetch failed` and continues) and `gh` then fails on the same outage, or the only subject that ends with ` (#<N>)` is a one-parent commit on a side branch while the real merge is a two-parent commit. vigil-skills has the second shape for `#27`: `464303fe` is the only `(#27)` subject hit and it has two parents, so the rule rejects it. A one-parent local subject with the same ending would be the sole accept. No such impostor is in this repo's history (every unique one-parent hit is an ancestor of `origin/main`).
**What happens:** That SHA is stored in `> Merge:` and `git show` diffs it. The report is written before the Phase 4 checkpoint. Phase 3 can copy it into the state.md evidence triple. The close looks resolved. A second subject hit would have prompted; a unique impostor does not.
**Why the spec misses it:** "Exactly one accepted line" is defined as the squash, and line 90 keeps a squash that is not on `HEAD` visible via `--all`. Nothing says a unique hit is taken even when it is not contained in `HEAD` or `refs/remotes/origin/HEAD`, or when the two-parent commit with the same suffix was ignored.
**Suggested fix:** In the exactly-one bullet, state that the match may be any ref `--all` walks, including a commit that is not an ancestor of `HEAD` or `origin/HEAD`. If that is not wanted, treat the line as not found unless it is an ancestor of `HEAD` or of `refs/remotes/origin/HEAD` when that ref exists. Put the chosen rule on the review checklist.

### F-4: A two-parent merge the rule already found is not given back at the prompt
**Severity:** P3
**Where:** spec.md:92–95 (spec § Phase 2a step 2)
**Edge case:** The only `(#<N>)` subject is a two-parent merge, as with `#27` / `464303fe` on this repo. `git show` of that commit does list the shipped files (5 files, not an empty combined diff).
**What happens:** The line is rejected and the unchanged step 1c prompt is printed with no SHA. The operator has to rediscover the commit the command just walked. Pasting that SHA later works; nothing in the prompt says it was seen.
**Why the spec misses it:** "Finds nothing" includes "a non-squash," and the prompt text is frozen, so the rejected SHA is dropped on the floor.
**Suggested fix:** Keep the prompt text, but print the rejected SHA on its own line before the prompt (not a second warning), for example `not a squash (2 parents): <SHA>`. Still do not auto-select it.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
