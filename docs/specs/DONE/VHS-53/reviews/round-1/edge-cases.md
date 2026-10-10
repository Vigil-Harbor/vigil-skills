The fallback command accepts the newest commit whose message merely contains `(#N)`, including stash commits. I verified that against git’s actual `--grep` behavior before writing the review.

# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: Newest `(#N)` mention is treated as the squash-merge SHA
**Severity:** P1
**Where:** spec.md:85–91 (spec § Phase 2a step 2)
**Edge case:** `gh` is absent or exits non-zero, and more than one commit message contains the literal `(#<N>)`. Reproduced with git 2.55.0 on the specified argv `git log --all -1 --format=%H -F --grep="(#123)"`: a later commit whose message only cites `(#123)`, and a `refs/stash` commit whose subject is `On master: WIP title (#123)`, both sort ahead of the real squash subject `squash title (#123)`. `--all` walks `refs/stash`. Stash subjects are `On <branch>: <message>`, so a stash of the PR title ends with `(#N)` and is newer than the merge. The same argv also selects a revert or any newer commit that mentions the PR in the body. A no-match `git log` exits 0 with empty stdout (also reproduced); that part of the miss rule is fine.
**What happens:** Any non-empty stdout is taken as the shipped SHA (spec.md:90) and `gh` is not called again. `git show` then diffs the stash or the citing commit, including in `--report-only`, and Phase 2c writes that into the reconciliation report before the Phase 4 checkpoint. Scope, decisions, and acceptance are judged against the wrong tree; Phase 3 can store that SHA in the state.md evidence triple. The close looks successful.
**Why the spec misses it:** The miss path is only empty stdout or a non-zero exit. `-1` is defined as “the newest matching commit,” with no subject, parent, or ref check. `--all` is justified only as “the same reach as step 1a.”
**Suggested fix:** Keep a single `git log --grep` (do not add a second lookup). Drop `-1`. Run `git --no-pager log --exclude=refs/stash --all --format=%H%x09%P%x09%s -F --grep="(#<N>)"` so a squash that is not on `HEAD` is still visible, while stash and its index commit are not. Accept a line only when column 1 is one hex SHA (40 or 64), column 2 is exactly one parent, and the trimmed subject ends with ` (#<N>)`. Exactly one such line: take the commit-SHA branch with that SHA and set the report’s `> Merge:` value to it. Zero or more than one: the existing step 1c prompt, with no newest-wins guess. Update the review checklist (spec.md:126) to require that a newer body mention, a revert subject, and a stash do not win.

### F-2: Non-numeric `<N>` makes `gh` exit 0 for a different PR
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:72–75 (spec § Phase 2a step 2)
**Edge case:** The step 1c answer is empty, `#` only, or a branch name, and is fed back through “read it with this same step.” `<N>` is only “one leading `#` removed, no other trimming.” `gh pr view` takes `[<number> | <url> | <branch>]`, and with no argument it shows the current branch’s PR (gh 2.x help text).
**What happens:** Both commands can exit 0 for the current branch’s PR, or for whatever branch `<N>` names. The spec then uses that output and does not run the fallback, so the reconciliation diff is a different PR and the failure is invisible.
**Why the spec misses it:** Success is defined only as both exits 0. Nothing requires `<N>` to be a decimal integer before `gh` runs. The skill never defines how a PR number is recognized.
**Suggested fix:** Before either `gh` call, trim whitespace. If `<N>` is not one or more decimal digits, do not run `gh` or `git log`; print the step 1c prompt. Apply the same check to a re-entered answer.

### F-3: `-F` rationale is false and points at the regex mode that over-matches
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:88 (spec § Phase 2a step 2)
**Edge case:** Default git `--grep` is basic regex. On git 2.55.0, `--grep="(#123)"` does not match a commit whose message is only `mention #123`. The same pattern with `-E` does. `grep.patternType=extended` (or `grep.extendedRegexp=true`) selects that wider mode unless `-F` is set.
**What happens:** The command as fenced is safe. The sentence above it is not: it says default basic regex treats `(#<N>)` as a group and also matches a bare `#<N>`. An implementer who “corrects” the command to `-E` to match that sentence silently accepts every bare `#<N>` mention, which is a much larger set than F-1.
**Why the spec misses it:** The parenthesis explanation was not checked against git’s default BRE. Unescaped `(` is literal in BRE; it is a group only in ERE.
**Suggested fix:** Replace that sentence with: unescaped parentheses are already literal in default BRE; `-F` is what stops a `grep.patternType=extended` config from turning `(#<N>)` into a group that also matches bare `#<N>`. Keep `-F`.

### F-4: The one warning line collapses distinct `gh` failures
**Severity:** P3
**Where:** spec.md:76–82 (spec § Phase 2a step 2)
**Edge case:** `gh` missing from `PATH`, versus `gh pr view` non-zero (auth, network, missing PR), versus view exit 0 and diff non-zero.
**What happens:** All three print the same `gh absent or failed` line, and the spec forbids reading stderr. A re-run cannot tell a missing binary from a 401 or a bad PR number.
**Why the spec misses it:** “Exactly one warning line” is specified as a fixed string with no status in it.
**Suggested fix:** Keep a single line and still do not parse stderr, but include how each command ended (`not-run`, `unavailable`, or the exit code), e.g. `warning: gh unavailable or failed for PR #<N> (view=<status>, diff=<status>) — resolving the squash-merge SHA with git log --grep "(#<N>)"`.

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=1 P4=0
