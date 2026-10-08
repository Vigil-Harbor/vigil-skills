# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: A Blocks-labelled finding with no location passes as `unusable`, silently
**Severity:** P1
**Where:** spec § Decision 6 (spec.md:77); spec § Decision 8 (spec.md:94-96); spec § Decision 10 (spec.md:137-144)
**Claim:** "A finding with no location or no problem statement is recorded as `unusable` and not acted on."
**Why this is wrong:** The rule is applied before, and regardless of, the finding's label. A finding the review labelled Must fix / P0 / critical that carries no file location (a whole-change finding such as a missing test, or a reviewer that omits the location line) is therefore never a Blocks finding: it is not fixed, is never "unresolved" under Decision 8, does not reach the halt block, and is absent from the PR body line (Decision 10 counts only fixed / recorded / overridden). The only trace is a line in the review file. The brief forbids exactly this: decision 6 ends "A blocker never passes silently", decision 11 says "Must fix findings block the commit", and Done-when bullet 1 requires that "a must-fix finding stops the commit" (brief.md:34, :39, :48). Brief decision 16 (brief.md:44) states the minimum the gate needs from a review but does not say a blocker below that minimum may be dropped; the one silent path it licenses is a review that errors as a whole.
**Suggested fix:** In Decision 6, replace the last sentence of the paragraph at spec.md:77 with: "A finding with no location or no problem statement is `unusable`. An unusable finding whose label maps to Blocks is an unresolved Blocks finding: it goes to Decision 8's halt block with the reason `no location` or `no problem statement`. Any other unusable finding is recorded and not acted on." Add a matching line to the Test plan review checklist: "An unusable finding labelled as a blocker reaches the halt block; it is never dropped."

### F-2: Whether the review covers untracked new files is not pinned
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 4 (spec.md:57); spec § Decision 2 (spec.md:37)
**Claim:** "the instruction to review the uncommitted change in that worktree against `origin/<default-branch>`"
**Why this is wrong:** At Phase 3b nothing is staged or committed (`skills/ship-spec/SKILL.md:92`, staging happens in Phase 4 at `:135`). Every file Phase 2 created is untracked. A review that reads `git diff origin/<default-branch>` sees modified tracked files only, so a change whose substance is a new file (VHS-45 added `skills/spec-tickets/SKILL.md`, 184 new lines, commit 1bd3f29) would be reviewed without it, and the gate would report clean. The spec neither tells the reviewer that untracked files are part of the change nor gives it the list.
**Suggested fix:** Add to Decision 4: "The prompt lists the changed paths from `git status --porcelain` in the worktree, untracked files included, and states that untracked files are part of the change." Add one checklist line to the Test plan.

### F-3: The veto reads invariants only from the file Phase 0 step 3 reads
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7 (spec.md:85)
**Claim:** "Against the invariants the project instructions file declares ... Phase 0 step 3 already reads that file."
**Why this is wrong:** Phase 0 step 3 reads `<project_root>/CLAUDE.md` and nothing else (`skills/ship-spec/SKILL.md:17`). The source text the brief names for carry-over (Risk 3, brief.md:71) reads both: "The project's agent instructions (CLAUDE.md / AGENTS.md)" (`skills/bloat-check/SKILL.md:47`). In this repo `CLAUDE.md` is a gitignored 14-line pointer and every convention lives in `AGENTS.md` (`AGENTS.md:99-107`), so the veto as written finds no declared invariant here unless the agent follows the pointer on its own. The test-pin half of the veto is unaffected.
**Suggested fix:** Reword item 1 of Decision 7: "Against the invariants the project's agent instructions declare (`CLAUDE.md`, and `AGENTS.md` when present, or the equivalent on your host) — design invariants, frozen exports, cannot-be-disabled floors, and similar declarations." Drop the sentence "Phase 0 step 3 already reads that file", or extend Phase 0 step 3's note to say the veto reads both.

### F-4: The review-file format cannot express three states the Decisions produce
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 10 (spec.md:124-140) against § Decision 3 (spec.md:48-49) and § Decision 8 (spec.md:110)
**Claim:** "Disposition: fixed | fixed by operator | overridden by operator | vetoed: <reason> | recorded: <reason> | not acted on" and "Blocks: <n> (<fixed> fixed, <op> fixed by operator, <ov> overridden)"
**Why this is wrong:** (a) Decision 8 option 3 (and the cannot-wait host) writes the review file while Blocks findings are still unresolved; no disposition value and no header count covers "unresolved". (b) Decision 3 row 3 requires the file to state "the error text"; the template has no field for it. (c) For both skip rows the review never ran, so `Mode`, `Compared against`, and the three count lines have no defined value. The implementer follows the code block and must invent all three.
**Suggested fix:** Add `unresolved: <reason>` to the Disposition list and `, <un> unresolved` to the Blocks header line. Add below the template: "A skipped run writes only `Command`, `Result: skipped — <reason>`, and, for a failed run, an `Error:` line with the error text; it writes no counts and no `## Findings` section."

### F-5: Halt option 1 routes past the review-file write
**Severity:** P2
**Where:** spec § Decision 8 (spec.md:110) against § Design steps 6-8 (spec.md:173-175)
**Claim:** "On 1, pause; on resume, go to Decision 9's test re-run and then Phase 4"
**Why this is wrong:** The Design orders the steps halt (6), test re-run (7), write the review file (8), then Phase 4. Decision 8 names the test re-run and Phase 4 and omits the write. A careful reader resolves it from the Design list, but the two sections describe different paths.
**Suggested fix:** Change to "On 1, pause; on resume, record those findings as `fixed by operator` and continue with step 7 (test re-run) and step 8 (review file)." Use the same "continue with step 7" wording for option 2.

### F-6: The `docs/customizing.md` example is not pinned to the brief's choice
**Severity:** P2
**Where:** spec § Design, `docs/customizing.md` (spec.md:197); spec § Decision 2 (spec.md:39)
**Claim:** "One example, tagged as an example ...: a skill invocation of a review skill. This is the only place a product name may appear."
**Why this is wrong:** Brief decision 8 says the doc shows the declaration "with ponytail as a tagged example" (brief.md:36). The spec says a product name "may" appear and gives no literal, so the implementer chooses both whether to name it and what the invocation string is. The test command only asserts the name is absent from four other files (spec.md:244), so either outcome passes.
**Suggested fix:** Give the literal example block in the Design section, with the invocation string the operator will use and no version, and change "may appear" to "appears".

### F-7: Two Test plan items are stronger than the test command
**Severity:** P3
**Where:** spec § Test plan items 5 and 6 (spec.md:219-220) against § Test command (spec.md:244)
**Claim:** "contains the `## Phase 3b — Review gate (one pass)` heading exactly once, between the Phase 3 and Phase 4 headings" and "The leave-alone paths have no diff against `origin/main`."
**Why this is wrong:** The command counts the heading (`grep -c ... = "1"`) but does not check its position. The leave-alone list says "every test file other than `tests/test_lint.py`" (spec.md:19); the diff check names the four other `tests/test_*.py` files but not `tests/fixtures/` (20 tracked files). The machine-local `CLAUDE.md` is gitignored (`.gitignore:7`) and cannot be diffed, which is fine but unstated.
**Suggested fix:** Either move the position requirement to the review checklist, or add a line-number comparison. Add `tests/fixtures` to the diff path list.

### F-8: Two output lines are underspecified
**Severity:** P3
**Where:** spec § Decision 10 (spec.md:144)
**Claim:** "`Review:   docs/specs/TODO/<TICKET-ID>.review.md` or `Review:   skipped — <reason>`" and "`<b> blocking fixed, <s> other fixed, <r> recorded`"
**Why this is wrong:** For Decision 3 rows 2 and 3 the gate was skipped and a file exists; the spec does not say which `Review:` form applies. The PR line does not say whether findings recorded as `fixed by operator` count in `<b>`.
**Suggested fix:** State that a skip with a file prints `Review:   skipped — <reason> (docs/specs/TODO/<TICKET-ID>.review.md)`, and that `<b>` includes operator fixes.

### F-9: A leading `/` does not distinguish a skill from an absolute-path command
**Severity:** P3
**Where:** spec § Decision 2 (spec.md:37); § Decision 3 (spec.md:51)
**Claim:** "It is either a skill invocation (a line beginning `/`) or a shell command."
**Why this is wrong:** A shell command given by absolute POSIX path (`/usr/local/bin/review --uncommitted`) begins with `/`. It is classified as a skill, no skill of that name exists, and the gate reports "not available" for a command that would have run.
**Suggested fix:** Add: "A line beginning `/` whose first word contains a second `/` is a shell command."

### F-10: Recent commit on four touched files (informational)
**Severity:** P4
**Where:** spec § Scope (spec.md:13-17)
**Claim:** Census is 12; `AGENTS.md` lifecycle item 4 is ship-spec; ship-spec Phase 3 and Phase 4 entries in `docs/spec-workflow-reference.md`.
**Why this is wrong:** It is not wrong. Commit 1bd3f29 (2026-10-08, VHS-45) changed `AGENTS.md`, `README.md`, `docs/spec-workflow-reference.md` and `tests/test_lint.py` today. Every spec and brief anchor was checked against the post-commit files and matches: `tests/test_lint.py:52` (12), `AGENTS.md:31`, `README.md:12`, `docs/spec-workflow-reference.md:174` and `:180`, `skills/ship-spec/SKILL.md:18`, `:20`, `:94`, `:131`, `skills/bloat-check/SKILL.md:43` and `:68`, `sync.py:72-94`, `tests/test_spec_close_log.py:1059`, `docs/authoring-portable-skills.md:41`, `skills/spec-close/SKILL.md:340` (companion rule, `review.md` does not collide with `reviews/`). `.gitattributes` pins `*.md` to LF, so the `$`-anchored grep in the test command holds on Windows.
**Suggested fix:** None.

## Summary
P0: 0 | P1: 1 | P2: 5 | P3: 3 | P4: 1

STATUS: RED P0=0 P1=1 P2=5 P3=3 P4=1
