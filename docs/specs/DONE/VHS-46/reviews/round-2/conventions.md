# Conventions Review — round 2

Grounding performed: spec and brief read fresh from disk; `AGENTS.md` (tracked project instructions) and the machine-local `CLAUDE.md` pointer; `skills/ship-spec/SKILL.md` (whole file); `skills/bloat-check/SKILL.md` Steps 1–4; `docs/customizing.md`; `docs/spec-workflow-reference.md` ship-spec region and "Adapting to your stack"; `docs/portability-contract.md` §4; `skills/spec-cycle/SKILL.md` (the `## Deferred (P2+)` and `## Deferred — follow-up required` rules, `:441`–`:462`); `skills/spec-close/SKILL.md:339`–`:340` (companion rule); `tests/test_lint.py:48`–`:59`; `README.md:12`, `:36`; tracked `tests/` listing; wiki `projects/vigil-skills/filemap.md` and `state.md` (no `architecture.md` exists for this project); wiki decisions `2026-08-25-vhs-28-supersession-is-an-operator-step.md`, `2026-09-27-cross-codex-review-gate-replaces-coderabbit.md`, `2026-08-09-review-round-artifacts-are-immutable.md`. Other decision titles were scanned and judged non-overlapping. Ticket lookup skipped per orchestrator note (ACL); the brief is the ticket text. The three round-1 reports were read; the round-2 report of another lens already present in the directory was not read.

Deferred-findings block: the spec has no `## Deferred — follow-up required` section, so there are no rows, no preamble, and no ceiling to check. Its `## Deferred (P2+)` section (spec.md:276–284) is the advisory list `skills/spec-cycle/SKILL.md:459` describes, uses that exact heading, and holds no P0/P1.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Blocks-labelled finding with no location passes as `unusable` | CLOSED | spec § Decision 6, line 77: an unusable finding whose label maps to Blocks "is an unresolved Blocks finding: it goes to Decision 8's halt block"; checklist row at line 243; `unresolved` added to the Disposition list at line 144. Matches the manifest. |
| correctness | F-2 (P2) | Untracked new files not pinned | CLOSED | § Decision 4, line 57: "everything that differs from `origin/<default-branch>`, including new files not yet tracked" |
| correctness | F-3 (P2) | Veto reads invariants from `CLAUDE.md` only | CLOSED | § Decision 7 item 1, line 85 ("the files named in Decision 2"); § Decision 2 item 2, line 34 names `CLAUDE.md`, then `AGENTS.md` |
| correctness | F-4 (P2) | Review-file format cannot express three states | PARTIAL | `unresolved` disposition (line 144), `Error:` line (line 135) and the skipped-run rule (line 147) were added. Still open: the `Blocks:` header (line 136) has no unresolved count; `Mode` and `Compared against` have no value on a not-available skip. Not in § Deferred (P2+). See F-2 below. |
| correctness | F-5 (P2) | Halt option 1 routes past the review-file write | CLOSED | § Decision 8, line 112: "continue at Phase 3b step 7 (the test re-run, then the review file)" |
| correctness | F-6 (P2) | `docs/customizing.md` example not pinned | CLOSED | § Design `docs/customizing.md`, line 206: the literal is written out, no version, "the only place a product name appears" |
| correctness | F-7 (P3) | Two Test plan items stronger than the test command | PARTIAL | Unchanged: line 255 counts the heading without checking position and omits `tests/fixtures`. Not listed in § Deferred (P2+). P3, no disposition required; see F-6 below. |
| correctness | F-8 (P3) | Two output lines underspecified | PARTIAL | Unchanged at line 151. Not listed. P3; see F-6 below. |
| correctness | F-9 (P3) | Leading `/` and absolute-path commands | DEFERRED | § Deferred (P2+), line 284 (advisory entry, not a D-row) |
| correctness | F-10 (P4) | Recent commit on four touched files | CLOSED | Informational; anchors re-checked this round against `tests/test_lint.py:52`, `AGENTS.md:31`, `README.md:12`, `docs/spec-workflow-reference.md:174`/`:180`, `skills/ship-spec/SKILL.md:18`/`:94`/`:131` |
| edge-cases | F-1 (P1) | Blocks fix undone by the re-entered test loop still recorded as fixed | CLOSED | § Decision 9, line 120: a Blocks fix "is not undone to get the tests green"; a second halt names the finding and the failing test; a reverted Fix-or-record fix is `recorded: fix reverted, broke <test>`; "The dispositions in the review file describe the tree that is committed." Checklist row at line 244. Matches the manifest. A P2 residue on what the halt options do at this second stop is F-1 below (NEW variant, does not reopen the P1). |
| edge-cases | F-2 (P2) | Non-zero exit with findings treated as failed | CLOSED | § Decision 3, line 53 |
| edge-cases | F-3 (P2) | Nothing notices a review that changes the worktree | DEFERRED | § Deferred (P2+), line 278. Its claim that the rules cover the inline path holds: line 59 "under the same three rules". |
| edge-cases | F-4 (P2) | Blocks finding outside the spec's scope | CLOSED | § Decision 8, line 96: "is outside the spec's scope" is in the unresolved list |
| edge-cases | F-5 (P2) | No disposition for unresolved or abandoned Blocks | PARTIAL | `unresolved` added (line 144). Still open: no header count; `overridden by operator` drops the original reason; a vetoed Fix-or-record finding can be `vetoed: <reason>` (Decision 7, line 90) or `recorded: vetoed` (Decision 8, line 95), so `<rec>` is ambiguous. Not in § Deferred (P2+). See F-2 below. |
| edge-cases | F-6 (P2) | Untracked files; two bases | CLOSED | § Decision 4, line 57: one base, untracked files included; line 133 records it |
| edge-cases | F-7 (P2) | Malformed spec-level section: fall through or stop | CLOSED | § Decision 2, line 37: "warn in one line naming the file, and fall through to the next source" |
| edge-cases | F-8 (P2) | Review file written last | DEFERRED | § Deferred (P2+), line 279 |
| edge-cases | F-9 (P2) | Error text unbounded and unredacted | DEFERRED | Bound folded (§ Decision 3, line 53; line 135); redaction in § Deferred (P2+), line 280, pointing at VHS-31 |
| edge-cases | F-10, F-11, F-12 (P3) | Label matching; hung review; first-word test | DEFERRED | § Deferred (P2+), line 284 |
| edge-cases | F-13 (P4) | Heading count, not position | PARTIAL | Unchanged at lines 228 and 255. P4; see F-6 below. |
| conventions | F-1 (P2) | Project instructions pinned to `CLAUDE.md` only | CLOSED | § Decision 2 item 2 (line 34) and § Decision 7 item 1 (line 85). The author widened review-command resolution as well as the veto; see F-3 below (P3). |
| conventions | F-2 (P2) | Review record missing from `## Spec & brief layout` | CLOSED | § Design `docs/customizing.md`, line 206. The Scope row at line 14 was not updated; see F-4 below (P3). |
| conventions | F-3 (P2) | "on your host" vs "in your host" | CLOSED | Line 206: "or the equivalent in your host", matching `docs/portability-contract.md:115` |
| conventions | F-4 (P2) | `AGENTS.md` removal paragraph not pinned | CLOSED | § Decision 11, lines 157–159: literal paragraph, both shells, "retired, not replaced", no `--prune`. Consistent with wiki decision VHS-28 (targeted removal, `sync.py` gains no delete path). |
| conventions | F-5 (P2) | bloat-check Step 4 item 3 dropped unnamed | CLOSED | § Decision 7 item 3, line 88, carries `skills/bloat-check/SKILL.md:74` |
| conventions | F-6 (P2) | Three unmarked spec-level additions | DEFERRED | § Deferred (P2+), line 281 lists all three for the drift check |
| conventions | F-7 (P3) | Frontmatter `description` unchanged | DEFERRED | § Deferred (P2+), line 282 |
| conventions | F-8 (P3) | Class (c) additions, informational | CLOSED | No action was required |
| conventions | F-9 (P3) | `review.md` beside `reviews/` | CLOSED | Line 206: "one file, distinct from the `<TICKET-ID>.reviews/` directory `/spec-cycle` writes" |
| conventions | F-10 (P3) | Other ship-spec mentions in the reference doc | DEFERRED | § Deferred (P2+), line 283 |
| conventions | F-11 (P4) | Skip line's checkbox form | PARTIAL | Decision 3 cells (lines 47–49) still carry no `- [ ]`; line 151 calls it "the unchecked skip line". P4; see F-6 below. |

No finding is REOPENED. Both manifest lines verify as fixed.

## Findings

### F-1: The second halt reuses Decision 8's menu, whose options are written for a tree with green tests
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9 (line 120) against § Decision 8 (lines 100–112)
**Convention violated:** Reuse of an existing block without restating what differs. Decision 8's own text says "stop once" (line 98) and routes option 1 and option 2 to "Phase 3b step 7"; Decision 9 says "Nothing is committed while tests are red" (line 118).
**Evidence:** At the second stop the Blocks fix is in place and the tests are red. Option 2's menu text is "Override — commit with each finding above recorded as overridden" (line 108) and its rule is "record them as `overridden by operator` and continue" (line 112). Neither says whether an override lifts the "is not undone" rule, so the loop is either still stuck or the fix is removed under a record that does not say so. Option 1 records the finding as `fixed by operator` although the gate applied the fix and the operator repaired a test. Every path still ends at an operator and nothing commits silently, which is why this is P2 and does not reopen edge-cases F-1.
**Suggested fix:** Add to Decision 9 after "naming the finding and the failing test": "At this stop, option 1 means the operator makes the tests pass with the fix in place; the finding stays `fixed`. Option 2 lifts the rule for that finding: the fix may be undone in the loop and the finding is recorded `overridden by operator`. In both cases the loop restarts with a fresh count of 5. Option 3 is unchanged."

### F-2: Review-record residue from two round-1 P2s is neither folded nor listed in `## Deferred (P2+)`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 10 (lines 131–147); § Decision 7 (line 90); § Decision 8 (line 95); § Decision 4 (line 59); § Deferred (P2+) (lines 278–284)
**Convention violated:** `skills/spec-cycle/SKILL.md:459`: "For P2 findings, either fix or list them in a `## Deferred (P2+)` section at the end of the spec with one-line acknowledgments."
**Evidence:** correctness/R1/F-4 and edge-cases/R1/F-5 are partly folded and absent from the Deferred list. What remains: (a) `Blocks: <n> (<fixed> fixed, <op> fixed by operator, <ov> overridden)` does not sum to `<n>` when Abandon writes `unresolved`; (b) line 147 omits the counts and `## Findings` on a skipped run but leaves `Mode` and `Compared against`, which have no value when the command was not available; (c) a vetoed Fix-or-record finding is `vetoed: <reason>` under Decision 7 and a `recorded` reason under Decision 8, so `<rec>` and the PR line's `<r>` depend on the agent's choice; (d) line 59 writes `mode: inline` where the template field is `Mode:`; (e) the allowed record reasons now live in two places (Decision 8's list and Decision 9's addition).
**Suggested fix:** In Decision 10: append `, <un> unresolved` to the `Blocks:` line; change line 147 to "On a skipped run only `Command`, `Result` and, for a failed run, `Error` are written."; add "A vetoed Fix-or-record finding is written `vetoed: <reason>` and counted under recorded." Change line 59 to "`Mode: inline`". Move `fix reverted, broke <test>` into Decision 8's reason list with "(Decision 9 only)". Or add one Deferred (P2+) line naming correctness/R1/F-4 and edge-cases/R1/F-5 with what was left.

### F-3: Review-command resolution now reads two files; the test-command fallback and `docs/customizing.md` still describe one
**Severity:** P3
**Where:** spec § Decision 2 item 2 (line 34); § Design `docs/customizing.md` (line 206)
**Convention violated:** None broken. Class (c) addition with rationale, plus a consistency gap with `skills/ship-spec/SKILL.md:17`, `:21` and `docs/customizing.md:3`–`:5`.
**Evidence:** Brief Decision 2 says "the spec, then the project instructions file" (singular). The spec reads `CLAUDE.md`, then `AGENTS.md`, with the reason given ("a repo may keep its tracked instructions in `AGENTS.md`"). The test command still falls back to `CLAUDE.md` "Build & Run" only (`skills/ship-spec/SKILL.md:21`), so a project that keeps both sections in `AGENTS.md` gets a review command and no test command. The new doc section lands under `## What to put in your CLAUDE.md` (`docs/customizing.md:5`), and the Design text does not say the section may also sit in `AGENTS.md`, or that `CLAUDE.md` wins when both declare one.
**Suggested fix:** Add to the `docs/customizing.md` Design paragraph: "It states that the section is read from `CLAUDE.md` first and `AGENTS.md` second, and that this is wider than the test-command fallback, which reads `CLAUDE.md` only."

### F-4: The Scope row for `docs/customizing.md` does not list the second edit the Design makes
**Severity:** P3
**Where:** spec § Scope (line 14) against § Design `docs/customizing.md` (line 206)
**Convention violated:** Scope table as the complete list of edits per file.
**Evidence:** Scope: "New `### Review command section` after `### Build & Run section`." Design adds a bullet to `## Spec & brief layout` as well. `docs/customizing.md:60` ("the skills hardcode the spec/reviews/test-output paths today") is left naming three paths when there will be four.
**Suggested fix:** Extend the Scope cell: "`## Spec & brief layout`: add the review record to the artifact list and to the hardcoded-paths sentence."

### F-5: Spec-level additions made this round, listed for the human drift check
**Severity:** P3
**Where:** spec § Decision 2 (line 34), § Decision 3 (line 53), § Decision 7 item 3 (line 88), § Decision 9 (line 120), § Decision 11 (lines 157–159)
**Convention violated:** None. Class (c) items.
**Evidence:** (1) `AGENTS.md` as a second source for the review command (see F-3). (2) Error text cut to its first 20 lines. (3) The cross-fix check, authorized by brief Risk 3 as carry-over from `skills/bloat-check/SKILL.md:74`. (4) The second operator stop inside the re-entered test loop; brief Decision 15 says "the same halt menu" for red tests, and the spec adds a different stop for the Blocks-fix case, with the reason stated. (5) A first-party retirement recorded under `AGENTS.md` § Superseded vendor skills; the wiki decision VHS-28 revisit trigger ("A second vendor skill needs superseding") is not reached because `bloat-check` is not a vendor skill and `sync.py` gains no delete path, but the spec does not say so.
**Suggested fix:** None required. Optionally add one sentence to Decision 11: "This is a first-party retirement, so the VHS-28 decision's second-vendor trigger is not reached."

### F-6: Four round-1 P3/P4 items are unchanged and unlisted
**Severity:** P4
**Where:** spec § Test command (line 255); § Decision 10 (line 151); § Decision 3 (lines 47–49)
**Convention violated:** None; `skills/spec-cycle/SKILL.md:459` requires a disposition for P2 only.
**Evidence:** correctness/R1/F-7 (heading position unchecked; `tests/fixtures` absent from the leave-alone diff although line 19 says "every test file other than `tests/test_lint.py`"), correctness/R1/F-8 (`Review:` summary form for a skip that wrote a file), edge-cases/R1/F-13, conventions/R1/F-11 (`- [ ]` marker on the skip line).
**Suggested fix:** Add `tests/fixtures` to the path list at line 255 and write the Decision 3 PR-body cells as `- [ ] Review gate: skipped — …`; or add one Deferred (P2+) line naming the four.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 3 | P4: 1

STATUS: GREEN
