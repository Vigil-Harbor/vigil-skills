# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — round 1.

Grounding notes: spec, brief, `CLAUDE.md`, `skills/ship-spec/SKILL.md`, `skills/spec-close/SKILL.md` (archive rule, `:330`–`:340`), `tests/test_lint.py:52`–`:53`, `docs/customizing.md`, and `AGENTS.md` § Superseded vendor skills were read from disk. The ticket lookup was skipped as instructed (ACL); the brief stands in for the ticket. The spec has no `## Deferred — follow-up required` section, so there are no rows to validate.

Checked and clean: `.gitattributes` pins `*.md` to LF, so the `$`-anchored `grep -c` in the test command holds on Windows; `bloat-check` is referenced by no tracked file outside `docs/specs/` and the skill itself; `<TICKET-ID>.review.md` archives as `review.md` and does not collide with `<TICKET-ID>.reviews/` → `reviews/`; the skills directory holds 12 entries today, so 11 after the delete is right.

## Findings

### F-1: A Blocks fix undone by the re-entered test loop is still recorded as fixed
**Severity:** P1
**Where:** spec § Decision 9 (lines 114–118); § Decision 8 line 96 ("stop once"); § Design, Phase 3b steps 5–8 (lines 172–175)
**Edge case:** Partial failure across steps. The gate applies a fix for a Blocks finding in step 5, step 6 finds nothing unresolved, and step 7 re-enters the Phase 3 loop. The fix turns a test red. Phase 3's instruction is "identify the smallest blocking failure ... fix it", and the smallest change that restores green is to undo or hollow out the review fix.
**What happens:** Tests go green, step 8 writes the review file with the disposition decided in step 5 (`fixed`), the PR line counts it under "blocking fixed", and the commit goes out without the fix. The blocking finding has passed with a record that says the opposite. The halt block cannot catch it: step 6 has already run and Decision 8 says to stop once.
**Why the spec misses it:** Decision 9 hands control to the Phase 3 loop with no rule about what that loop may do to a gate fix. Decision 7's veto covers only shape, static and adversarial pins found by searching before the fix, not an ordinary test that the fix breaks. Decision 10 has no disposition for a fix that was applied and then removed. Brief Decision 6 says a blocker never passes silently.
**Suggested fix:** Add to Decision 9: "Inside the re-entered loop, a fix the gate applied for a Blocks finding is not undone to get the tests green. If green cannot be reached with the fix in place, the loop is red: print Phase 3's halt block at once, naming the finding and the failing test, without spending the remaining iterations. A fix applied for a Fix-or-record finding may be undone; its disposition becomes `recorded: fix reverted, broke <test>`. The dispositions in the review file describe the tree that is committed." Add "the fix was reverted because it broke a test" to Decision 8's list of allowed Fix-or-record reasons, and one line to the review checklist.

### F-2: A review command that exits non-zero because it found problems is treated as a failed review
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3, row 3 (line 49) and line 51; § Design, Phase 3b step 3 (line 170)
**Edge case:** External-system malformed result. Decision 2 allows a shell command. Many review and lint tools exit non-zero when they report findings.
**What happens:** "Errored or returned nothing readable" is an either/or. An agent that reads a non-zero exit as "errored" takes row 3: skip, write the file, commit. The findings, blockers included, are not processed. The skip is recorded, so it is not silent, but a declared and available command has just failed to stop a commit, which is the first Done-when bullet.
**Why the spec misses it:** "Errored" is never defined, and the only worked example is a skill invocation, which has no exit code.
**Suggested fix:** Add to Decision 3: "Errored means no list of findings could be read from the result. A non-zero exit with readable findings is a review that ran; process the findings."

### F-3: Nothing notices when the review itself changes the worktree
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 4 (lines 57–59); § Decision 9 line 118
**Edge case:** Precondition violation. The reviewer is read-only by instruction only. A declared review skill may have a fix mode, and on the inline path (line 59) the three rules are not stated at all, because they are described as part of the subagent prompt.
**What happens:** Files change during step 3. If the gate then applies no fix of its own, Decision 9 says the tests are not re-run, and Phase 4 stages "each modified file in the diff". Edits nobody reviewed or tested are committed.
**Why the spec misses it:** Decision 4 states the rule and assumes it holds. This is verification machinery, hence P2.
**Suggested fix:** Add to Decision 4: "The three rules apply on the inline path too. Record `git status --porcelain` before the review and compare after. If the review changed any file other than its own output, treat that as a fix having been applied for Decision 9 (tests re-run) and say so under `Result:` in the review file."

### F-4: A Blocks finding outside the spec's scope has no stated outcome
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 (lines 93–94, 112)
**Edge case:** The brief notes the example reviewer reads callers of changed code. It can return a blocker located in a file the spec does not touch, or in one of the spec's leave-alone paths.
**What happens:** "Outside the spec's scope" is an allowed reason for Fix or record (line 93) but is absent from the Blocks unresolved list (line 94), which reads "apply the fix" unless vetoed, contradicting the spec, impossible, or inaccurate. Line 112 says a fix adds no new scope. The two pull against each other; the literal reading widens the PR into files the spec never named, and for a leave-alone path it can fail the spec's own test command and feed F-1.
**Why the spec misses it:** The scope reason was listed for one group and not the other.
**Suggested fix:** In Decision 8's Blocks bullet, change the list to: "If its fix is vetoed, contradicts the spec, lies outside the spec's scope, cannot be made, or the agent believes the finding is inaccurate, the finding is unresolved."

### F-5: The review record has no disposition for an unresolved or abandoned Blocks finding
**Severity:** P2
**Where:** spec § Decision 10 (lines 131–132, 139); § Decision 8 line 110 (option 3)
**Edge case:** Operator picks Abandon, or the host cannot wait. Decision 8 says to write the review file.
**What happens:** The Disposition list is `fixed | fixed by operator | overridden by operator | vetoed | recorded | not acted on`. A Blocks finding that could not be fixed or that the agent thinks is inaccurate fits none of them. The header's `Blocks: <n> (fixed, fixed by operator, overridden)` no longer sums to `<n>`. Separately, a vetoed Blocks finding that is then overridden loses its veto reason, and a vetoed Fix-or-record finding can be written as either `vetoed: <reason>` (Decision 7) or `recorded: vetoed` (Decision 8), so the `<rec>` and PR-body `<r>` counts depend on which the agent picks.
**Why the spec misses it:** The template was written for the path that reaches Phase 4.
**Suggested fix:** Add `unresolved: <reason>` to the Disposition list and `<un> unresolved` to the Blocks header line. State that `overridden by operator` keeps the original reason after a dash, and that a vetoed Fix-or-record finding is written `vetoed: <reason>` and counted under recorded.

### F-6: "The uncommitted change" can miss new files, and has two bases
**Severity:** P2
**Where:** spec § Decision 4 (line 57); § Decision 10 line 129
**Edge case:** Phase 2 leaves new files untracked until Phase 4. A review tool that reads `git diff` does not see untracked files. Also, "uncommitted" is measured from HEAD while the prompt says "against `origin/<default-branch>`"; they are the same commit in a normal run and differ in a hand-cut stacked worktree or after an operator commit.
**What happens:** A change made mostly of new files is reviewed as nearly empty, returns no findings, and the record says `ran` with zero counts. In the stacked case the reviewer may be handed the dependency's diff as well.
**Why the spec misses it:** The prompt describes the change by a phrase and not by how to enumerate it.
**Suggested fix:** In Decision 4, add: "The prompt lists the changed paths, taken from `git status --porcelain` in the worktree so that untracked files are included. The change under review is the worktree against its HEAD; `Compared against:` records that commit."

### F-7: A malformed spec-level `## Review command` section: fall through or stop?
**Severity:** P2
**Where:** spec § Decision 2 (lines 33–37)
**Edge case:** The spec's section is present but empty or has two non-blank lines.
**What happens:** Line 37 says it "counts as none". Line 33 says the spec wins "when present". An agent can read this as final none (gate skipped although the project declares a command) or as falling through to the project file. Both degrade safely; they differ in whether a review runs. There is also no way for a spec to say "no review for this change": a value such as `N/A` is tried as a shell command and lands in the "not available" row with a review file.
**Why the spec misses it:** The malformed rule is stated once for both sources.
**Suggested fix:** Add to Decision 2: "A malformed section in the spec falls through to the project instructions file. A malformed section there resolves to none." If an opt-out is wanted, add: "A value of `none` (case-insensitive) in the spec resolves to none without falling through and prints the no-command skip line."

### F-8: The review file is written last, after the test loop
**Severity:** P2
**Where:** spec § Design, Phase 3b steps 7–8 (lines 174–175)
**Edge case:** Step 7 can run five or more test iterations and can end at Phase 3's halt block, where the operator may choose manual debug or roll back.
**What happens:** Until step 8 the findings and dispositions exist only in the agent's context. A halt in the test loop, a context compaction, or a session loss leaves no record of what the review found or which edits in the tree came from it. Decision 8's Abandon writes the file; Phase 3's halt does not.
**Why the spec misses it:** Step order follows the happy path.
**Suggested fix:** Swap the order: write the review file after step 6, then re-run the tests, then update the file's dispositions if F-1's rule changed any. One sentence: "The review file is written before the test re-run and corrected after it."

### F-9: Error text in the review file is unbounded and unredacted
**Severity:** P2
**Where:** spec § Decision 3, row 3 (line 49); § Decision 10
**Edge case:** Size limit and content. A failed command can emit a long trace containing absolute local paths or environment detail. The file is staged and pushed; this repo is public. VHS-31 tracks the same concern for the test output.
**What happens:** A multi-kilobyte dump with machine-local paths lands in the PR.
**Why the spec misses it:** Row 3 says "the error text" with no bound.
**Suggested fix:** In Decision 3 row 3, replace "the error text" with "the last 20 lines of the error text, with the worktree path replaced by `<worktree>`".

### F-10: Label matching is not specified beyond case
**Severity:** P3
**Where:** spec § Decision 6 (lines 69–77)
**Edge case:** `Must-fix`, `must_fix`, `High priority`, a label with an emoji prefix, or a finding carrying both a group and a severity that map to different rows (`Should fix` plus `high`).
**What happens:** The agent guesses. An unmatched blocker label drops to Fix or record, which the brief accepts, but a near-miss spelling should not be the cause.
**Suggested fix:** Add: "Compare after lowercasing and replacing hyphens and underscores with spaces; a label matches when it equals a listed label or begins with one. If a finding carries two labels that map to different groups, use the stricter group."

### F-11: No bound on a hung review, and no outcome when the subagent cannot load the skill
**Severity:** P3
**Where:** spec § Decision 3 line 51; § Decision 4; § Decision 5
**Edge case:** The review hangs, or the host dispatches a subagent that has no access to the declared skill although the main agent does.
**What happens:** A hang waits indefinitely with an operator able to interrupt. The second case is a row-3 skip; an agent might instead retry inline, which Decision 5 forbids.
**Suggested fix:** Add to Decision 3: "A review that the host reports as timed out or cancelled is row 3. A subagent that cannot run the command is row 3; the gate does not retry inline."

### F-12: The first-word availability test misreads some shell commands
**Severity:** P3
**Where:** spec § Decision 3 line 51
**Edge case:** `FOO=1 tool review`, `cd tools && ./review.sh`, or a relative script path resolved from a different directory than the worktree.
**What happens:** A working command is reported "not available" and skipped.
**Suggested fix:** Add: "Resolve the first word from the worktree. When the command starts with a variable assignment or a shell builtin, do not judge availability; run it."

### F-13: The test command checks the heading count, not its position
**Severity:** P4
**Where:** spec § Test plan item 5 (line 219) versus § Test command (line 244)
**Edge case:** The heading is added once but in the wrong place.
**What happens:** The mechanical gate passes; only the review checklist would catch it.
**Suggested fix:** Either reword item 5 to "exactly once (position is on the review checklist)" or leave as is.

## Summary
P0: 0 | P1: 1 | P2: 8 | P3: 3 | P4: 1

STATUS: RED P0=0 P1=1 P2=8 P3=3 P4=1
