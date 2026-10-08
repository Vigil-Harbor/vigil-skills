# Correctness Review — round 2

Grounding performed: spec and brief read fresh from disk; machine-local `CLAUDE.md`; `AGENTS.md`; `skills/ship-spec/SKILL.md` (whole file); `docs/customizing.md` (whole file); `tests/test_lint.py:48-59`; heading map of `docs/spec-workflow-reference.md`; tracked file list under `tests/` and `skills/`; repo-wide search for `bloat-check` and `ponytail` outside `docs/specs/`; the three round-1 reports. Ticket lookup skipped per orchestrator note (ACL); the brief is used as the ticket text.

`git log -10` on the seven touched files: the newest commit is still 1bd3f29 (2026-10-08, VHS-45), the one round 1 surfaced. Nothing has landed on those files since round 1, so the round-1 anchor checks stand. Re-checked this round and matching: `skills/ship-spec/SKILL.md:17` (step 3 reads `CLAUDE.md` only), `:20` ("proceed directly to Phase 4 (commit)"), `:94` and `:131` (Phase 3 and Phase 4 headings), `:135` (explicit staging), `:195-201` (PR body Test plan block), `:241` (Phase 7 `Tests:` line); `tests/test_lint.py:52-53` (`len(skills), 12,` and "12 currently-shipped"); `docs/customizing.md:7` (`### Build & Run section`) and `:51` (`## Spec & brief layout`); `docs/spec-workflow-reference.md:174` and `:180`; `AGENTS.md:31` (lifecycle item 4), `:63` (`## Superseded vendor skills`), `:86` (the `grilling` / `grill-me` paragraph the new paragraph follows). Twelve skill directories are tracked, so 11 after the delete is right. `ponytail` appears in no tracked file outside `docs/specs/` except `skills/bloat-check/SKILL.md:19`, which is deleted, so the last clause of the test command passes. `bloat-check` is referenced by no tracked file outside `docs/specs/` and the skill itself.

Deferred findings: the spec has no `## Deferred — follow-up required` section, so there are no `D-<n>` rows, no preamble, and nothing to validate under the routing rules. Its `## Deferred (P2+)` section (spec.md:276-284) is a different, informal list of round-1 P2-and-below items the author chose not to fold; none of them is a P0 or P1.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | A Blocks-labelled finding with no location passes as `unusable`, silently | CLOSED | spec § Decision 6, spec.md:77 carries the suggested text; checklist row at spec.md:243. Manifest claim verified in both named sections. |
| correctness | F-2 (P2) | Whether the review covers untracked new files is not pinned | CLOSED | spec § Decision 4, spec.md:57: "everything that differs from `origin/<default-branch>`, including new files not yet tracked" |
| correctness | F-3 (P2) | The veto reads invariants only from the file Phase 0 step 3 reads | CLOSED | spec § Decision 2 item 2 (spec.md:34) names `CLAUDE.md` then `AGENTS.md`; § Decision 7 item 1 (spec.md:85) reads "the files named in Decision 2" |
| correctness | F-4 (P2) | The review-file format cannot express three states the Decisions produce | PARTIAL | `unresolved` added to Disposition (spec.md:144); `Error:` line added (spec.md:135); skipped run omits counts and `## Findings` (spec.md:147). Still open: no unresolved count in the `Blocks:` header line; `Mode` and `Compared against` have no value on a skip. See F-2 below. |
| correctness | F-5 (P2) | Halt option 1 routes past the review-file write | CLOSED | spec § Decision 8, spec.md:112: "continue at Phase 3b step 7 (the test re-run, then the review file)" |
| correctness | F-6 (P2) | The `docs/customizing.md` example is not pinned | CLOSED | spec § Design, spec.md:206: literal `/ponytail-review` with the tag, "appears" |
| correctness | F-7 (P3) | Two Test plan items are stronger than the test command | PARTIAL | Unchanged: the command still counts the heading without checking position and still omits `tests/fixtures`. Not in the Deferred (P2+) list. Carried in F-4 below. |
| correctness | F-8 (P3) | Two output lines are underspecified | PARTIAL | Unchanged at spec.md:151. Not in the Deferred (P2+) list. Carried in F-4 below. |
| correctness | F-9 (P3) | A leading `/` does not distinguish a skill from an absolute-path command | DEFERRED | spec § Deferred (P2+), spec.md:284 (informal list, not a `D-<n>` row; P3, does not gate) |
| correctness | F-10 (P4) | Recent commit on four touched files (informational) | CLOSED | No action was asked; no newer commit has landed |
| edge-cases | F-1 (P1) | A Blocks fix undone by the re-entered test loop is still recorded as fixed | CLOSED | spec § Decision 9, spec.md:120 (new paragraph); checklist row at spec.md:244. Manifest claim verified in both named sections. The fold opens a new variant: see F-1 below (NEW). |
| edge-cases | F-2 (P2) | A non-zero exit with findings is treated as a failed review | CLOSED | spec § Decision 3, spec.md:53 |
| edge-cases | F-3 (P2) | Nothing notices when the review itself changes the worktree | DEFERRED | spec.md:278 (informal list). The inline path now states the three rules (spec.md:59). |
| edge-cases | F-4 (P2) | A Blocks finding outside the spec's scope has no stated outcome | CLOSED | spec § Decision 8, spec.md:96: "is outside the spec's scope" is in the unresolved list |
| edge-cases | F-5 (P2) | No disposition for an unresolved or abandoned Blocks finding | PARTIAL | `unresolved` disposition added (spec.md:144). Header count and the kept reason on override are not. See F-2 below. |
| edge-cases | F-6 (P2) | "The uncommitted change" can miss new files, and has two bases | CLOSED | spec.md:57 names one base and includes untracked files; it agrees with `Compared against:` at spec.md:133 |
| edge-cases | F-7 (P2) | Malformed spec-level `## Review command`: fall through or stop? | CLOSED | spec § Decision 2, spec.md:37: "fall through to the next source in the order above" |
| edge-cases | F-8 (P2) | The review file is written last, after the test loop | DEFERRED | spec.md:279 (informal list) |
| edge-cases | F-9 (P2) | Error text in the review file is unbounded and unredacted | DEFERRED | Bound closed (spec.md:53, :135: first 20 lines); redaction deferred at spec.md:280 |
| edge-cases | F-10 (P3) | Label matching is not specified beyond case | DEFERRED | spec.md:284 (informal list) |
| edge-cases | F-11 (P3) | No bound on a hung review | DEFERRED | spec.md:284 (informal list) |
| edge-cases | F-12 (P3) | The first-word availability test misreads some shell commands | DEFERRED | spec.md:284 (informal list) |
| edge-cases | F-13 (P4) | The test command checks the heading count, not its position | PARTIAL | Unchanged; same root as correctness F-7. Carried in F-4 below. |
| conventions | F-1 (P2) | "Project instructions file" pinned to `CLAUDE.md` only | CLOSED | spec.md:34 and :85 |
| conventions | F-2 (P2) | `## Spec & brief layout` does not list the review record | CLOSED | spec § Design, spec.md:206. The Scope row was not updated to match: see F-3 below. |
| conventions | F-3 (P2) | Tagged-example phrase wording | CLOSED | spec.md:206: "or the equivalent in your host" |
| conventions | F-4 (P2) | The `AGENTS.md` removal paragraph is not pinned | CLOSED | spec § Decision 11, spec.md:157-159: literal paragraph, both shells, placed after `AGENTS.md:86` |
| conventions | F-5 (P2) | bloat-check Step 4 item 3 dropped without being named | CLOSED | spec § Decision 7 item 3, spec.md:88 |
| conventions | F-6 (P2) | Three rules added without a spec-level marker | DEFERRED | spec.md:281 (informal list, written for the drift check) |
| conventions | F-7 (P3) | Frontmatter `description` left unchanged | DEFERRED | spec.md:282 |
| conventions | F-8 (P3) | Spec-level additions listed for the drift check | CLOSED | No action was asked |
| conventions | F-9 (P3) | `<TICKET-ID>.review.md` sits beside `<TICKET-ID>.reviews/` | CLOSED | spec.md:206 states the distinction in the `docs/customizing.md` bullet |
| conventions | F-10 (P3) | Other ship-spec touchpoints in the reference doc | DEFERRED | spec.md:283 |
| conventions | F-11 (P4) | The skip line's checkbox form is not stated | PARTIAL | Unchanged: Decision 3's cells (spec.md:47-49) carry no list marker; Decision 10 calls it "the unchecked skip line". Carried in F-4 below. |

No round-1 finding is REOPENED. Both manifest lines hold as stated.

## Findings

### F-1: Override at the second halt has no defined outcome, and its printed text says "commit" while the tests are red
**Severity:** P1
**Where:** spec § Decision 9, spec.md:120, against § Decision 8, spec.md:100-112, and § Decision 9, spec.md:118
**Claim:** "If green cannot be reached with that fix in place, the finding is unresolved: stop the loop without spending the remaining iterations and print Decision 8's halt block again, naming the finding and the failing test."
**Why this is wrong:** This is a new variant of the root behind edge-cases/R1/F-1, opened by its fold. Decision 8's halt block was written for a stop that happens before any test re-run, and each of its three options is defined for that state only. The second stop reuses the block in a different state: the Blocks fix is in the tree, the tests are red, and the Phase 3 loop has been stopped part-way.

- Option 2 prints as "Override — commit with each finding above recorded as overridden" (spec.md:108), and its handler says "record them as `overridden by operator` and continue" (spec.md:112). At the first stop "continue" is Phase 3b step 7. At the second stop the run is already inside step 7 with a loop it was told to stop. The spec does not say whether the fix is now undone, whether the loop resumes, or with what count.
- The literal reading, which is also what the operator is shown, is a commit with red tests. That contradicts the same Decision two sentences earlier, "Nothing is committed while tests are red" (spec.md:118), and brief decision 15, "Nothing commits while tests are red" (brief.md:43). On that path Phase 3 has saved no passing output either (`skills/ship-spec/SKILL.md:104-106` saves only on exit 0), so the PR body's test line and "The saved test output is the output of the final passing run" (spec.md:118) would both be false.
- The other reading, undo the fix and resume, is the sensible one, but nothing licenses it: the sentence before says the fix "is not undone to get the tests green", and no disposition rule says an overridden finding's fix is removed. "The dispositions in the review file describe the tree that is committed" (spec.md:120) cannot be met by `overridden by operator` unless the spec says which tree that is.

The implementer writes the skill text from these two paragraphs, and an agent running the skill meets this at an operator prompt with nothing to resolve it. Options 1 and 3 do carry over cleanly (option 1 re-enters step 7 with a fresh count per spec.md:118; option 3 writes the file and stops), so the gap is option 2 alone.
**Suggested fix:** Add to the end of the Decision 9 paragraph at spec.md:120: "At this second stop the options mean: 1 — as in Decision 8; on resume, re-enter the loop with a fresh count of 5. 2 — Override: undo the gate's fix for each named finding, record it as `overridden by operator` with the reason `fix broke <test>`, and resume the loop with a fresh count of 5; nothing is committed until the tests are green. 3 — as in Decision 8." In Decision 8's halt block, change option 2's text to "Override — record each finding above as overridden and continue", so the printed line is true at both stops. Add one row to the Test plan review checklist: "Override at the second halt undoes the fix and returns to the test loop; it never commits on red."

### F-2: The review record still cannot count an unresolved Blocks finding, and two header fields have no value on a skip
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 10, spec.md:131-147, against § Decision 8, spec.md:112, and § Decision 3, spec.md:48
**Claim:** "Blocks: <n> (<fixed> fixed, <op> fixed by operator, <ov> overridden)" and "On a skipped run the three count lines and `## Findings` are omitted."
**Why this is wrong:** Remainder of correctness/R1/F-4 and edge-cases/R1/F-5. (a) On Abandon, and on a host that cannot wait, the file is written with findings marked `unresolved` (spec.md:112), and the new unusable-blocker path (spec.md:77) adds more of them. The header's three sub-counts then do not sum to `<n>`, and nothing says so. (b) For the "not available" row the review never ran, so `Mode` and `Compared against` have no defined value; the omission rule names only the counts and `## Findings`. (c) An override drops the reason the finding was unresolved (for example the veto reason), because `overridden by operator` takes no suffix. The implementer follows the code block and must invent all three.
**Suggested fix:** Change the header line to "Blocks: <n> (<fixed> fixed, <op> fixed by operator, <ov> overridden, <un> unresolved)". Change spec.md:147 to: "On a skipped run the `Mode`, `Compared against`, and three count lines and `## Findings` are omitted; `Mode` is kept when the review was started and failed." Change the disposition value to "overridden by operator: <the reason it was unresolved>".

### F-3: The Scope row for `docs/customizing.md` does not list the second edit the Design makes
**Severity:** P3
**Where:** spec § Scope, spec.md:14, against § Design, spec.md:206
**Claim:** "`docs/customizing.md` | New `### Review command section` after `### Build & Run section`."
**Why this is wrong:** Round 1's conventions/F-2 fold added a second edit to the Design: `## Spec & brief layout` gains the review-record path. The Scope row still names one edit. A reader checking the diff against the Scope table would see an unlisted change in a listed file. The Design is the fuller statement, so the implementer is not misled.
**Suggested fix:** Extend the Scope row: "New `### Review command section` after `### Build & Run section`. `## Spec & brief layout` lists the review record."

### F-4: Four round-1 items at P3 and P4 are neither folded nor listed as deferred
**Severity:** P3
**Where:** spec § Test command, spec.md:255; § Decision 10, spec.md:151; § Decision 3, spec.md:47-49; § Deferred (P2+), spec.md:276-284
**Claim:** The Deferred (P2+) list accounts for the round-1 items that were not folded.
**Why this is wrong:** These are unchanged and absent from that list: correctness/R1/F-7 and edge-cases/R1/F-13 (the test command counts the Phase 3b heading without checking its position, and the leave-alone diff omits `tests/fixtures`, 20 tracked files, although spec.md:19 covers "every test file other than `tests/test_lint.py`"); correctness/R1/F-8 (which `Review:` form Phase 7 prints for a skip that wrote a file, and whether `<b>` includes operator fixes); conventions/R1/F-11 (Decision 3's PR-body cells carry no `- [ ]` marker although Decision 10 calls the line "unchecked"). None gates. Also a nit in the same family: Decision 4 says the file records `mode: inline` (spec.md:59) where the template field is `Mode: subagent | inline` (spec.md:132).
**Suggested fix:** Add `tests/fixtures` to the diff path list in the test command. Either fold the other three in one line each or add them to the Deferred (P2+) list so the drift check sees them.

## Summary
P0: 0 | P1: 1 | P2: 1 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=1 P2=1 P3=2 P4=0
