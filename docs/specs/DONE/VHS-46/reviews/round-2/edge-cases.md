# Edge-Cases Review — round 2

Grounding notes: spec and brief read fresh from disk; `CLAUDE.md` (machine-local pointer) and `skills/ship-spec/SKILL.md` re-read; all three round-1 reports read. The ticket lookup was skipped as instructed (ACL on namespace `skills`); the brief stands in for the ticket. `scale_lens` is off and no `scalability.md` exists in round-1. The spec has no `## Deferred — follow-up required` section, so there are no D-rows to validate; its `## Deferred (P2+)` list is a different section and is treated as acknowledged P2+ items, not re-filed.

## Closure of round 1 findings

Status "ACK" means the item is listed in the spec's `## Deferred (P2+)` section (acknowledged, not folded, not re-filed). "OPEN" means a P3/P4 that was neither folded nor listed; it has no gate effect.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Blocks-labelled finding with no location passes as `unusable` | CLOSED | spec § Decision 6, line 77: an unusable finding whose label maps to Blocks "is an unresolved Blocks finding: it goes to Decision 8's halt block"; checklist row at line 243 |
| correctness | F-2 | Untracked new files not pinned | CLOSED | § Decision 4, line 57: "everything that differs from `origin/<default-branch>`, including new files not yet tracked" |
| correctness | F-3 | Veto reads invariants from `CLAUDE.md` only | CLOSED | § Decision 2 line 34 and § Decision 7 line 85 read both `CLAUDE.md` and `AGENTS.md` |
| correctness | F-4 | Review-file format cannot express three states | PARTIAL (P2) | `unresolved` disposition added (line 144); `Error:` line added (line 135); line 147 omits counts and `## Findings` on a skip. Still open: the `Blocks:` header (line 136) has no unresolved count, and `Mode` / `Compared against` have no stated value on a skip row where the review never ran |
| correctness | F-5 | Halt option 1 routes past the review-file write | CLOSED | § Decision 8, line 112: "continue at Phase 3b step 7 (the test re-run, then the review file)" |
| correctness | F-6 | `docs/customizing.md` example not pinned | CLOSED | § Design, line 206 gives the literal example |
| correctness | F-7 | Two Test plan items stronger than the test command | OPEN (P3) | Test command (line 255) still counts the heading without checking position and omits `tests/fixtures` |
| correctness | F-8 | Two output lines underspecified | OPEN (P3) | Line 151 unchanged: no `Review:` form for a skip that wrote a file; `<b>` and operator fixes not stated |
| correctness | F-9 | Leading `/` versus absolute-path command | ACK | § Deferred (P2+), line 284 |
| correctness | F-10 | Recent commit on touched files (informational) | CLOSED | No action was required |
| edge-cases | F-1 (P1) | Blocks fix undone by the re-entered test loop still recorded as fixed | CLOSED | § Decision 9, line 120: a Blocks fix "is not undone to get the tests green"; unreachable green makes the finding unresolved and prints the halt block again; a Fix-or-record fix may be reverted with `recorded: fix reverted, broke <test>`; "The dispositions in the review file describe the tree that is committed"; checklist row at line 244. One new variant on the second stop is filed below as F-1 (P2) |
| edge-cases | F-2 | Non-zero exit with findings treated as a failed review | CLOSED | § Decision 3, line 53 |
| edge-cases | F-3 | Nothing notices when the review changes the worktree | ACK | § Deferred (P2+), line 278; the inline path now carries "the same three rules" (line 59) |
| edge-cases | F-4 | Blocks finding outside the spec's scope has no outcome | CLOSED | § Decision 8, line 96 lists "is outside the spec's scope" |
| edge-cases | F-5 | No disposition for an unresolved or abandoned Blocks finding | PARTIAL (P2) | `unresolved` added (line 144, line 112 option 3). Still open: header count for unresolved; whether a vetoed Fix-or-record finding counts under `<rec>`; overridden finding keeps no reason |
| edge-cases | F-6 | "Uncommitted change" misses new files, two bases | CLOSED | § Decision 4, line 57 names one base and includes untracked files; `Compared against:` (line 133) matches |
| edge-cases | F-7 | Malformed spec-level `## Review command` | CLOSED | § Decision 2, line 37: malformed "fall through to the next source in the order above". The optional opt-out value was not added; not required |
| edge-cases | F-8 | Review file written last, after the test loop | ACK | § Deferred (P2+), line 279 |
| edge-cases | F-9 | Error text unbounded and unredacted | PARTIAL (P2) / ACK | Bounded to the first 20 lines (line 53, line 135); redaction listed at § Deferred (P2+), line 280 |
| edge-cases | F-10 | Label matching beyond case | ACK | § Deferred (P2+), line 284 |
| edge-cases | F-11 | Hung review; subagent cannot load the skill | ACK | § Deferred (P2+), line 284 |
| edge-cases | F-12 | First-word availability test | ACK | § Deferred (P2+), line 284 |
| edge-cases | F-13 | Test command checks heading count, not position | OPEN (P4) | Test plan item 5 (line 228) and the test command are unchanged |
| conventions | F-1 | Project instructions file pinned to `CLAUDE.md` only | CLOSED | Lines 34 and 85 |
| conventions | F-2 | Review record missing from `## Spec & brief layout` | CLOSED | § Design `docs/customizing.md`, line 206 |
| conventions | F-3 | Tagged-example phrase wording | CLOSED | Line 206: "or the equivalent in your host" |
| conventions | F-4 | `AGENTS.md` removal paragraph not pinned | CLOSED | § Decision 11, line 159 gives the paragraph verbatim |
| conventions | F-5 | Cross-finding interaction check dropped unnamed | CLOSED | § Decision 7, item 3 (line 88) |
| conventions | F-6 | Three spec-level additions unmarked | ACK | § Deferred (P2+), line 281 |
| conventions | F-7 | Frontmatter `description` unchanged | ACK | § Deferred (P2+), line 282 |
| conventions | F-8 | Spec-level additions listed for drift check | CLOSED | No action was required |
| conventions | F-9 | `review.md` beside `reviews/` | CLOSED | Line 206 states the distinction in `docs/customizing.md` |
| conventions | F-10 | Other ship-spec mentions in the workflow reference | ACK | § Deferred (P2+), line 283 |
| conventions | F-11 | Skip line's checkbox form not stated | OPEN (P4) | Decision 3 cells (lines 47–49) still carry no list marker; line 151 calls it "the unchecked skip line" |

Manifest verdicts: both lines verified as fixed. No REOPENED items.

## Findings

### F-1: "Override" at the second stop has no stated outcome for the fix or the tests
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9, line 120, against § Decision 8, lines 107–112
**Edge case:** Partial failure, second stop. The gate applied a Blocks fix, the re-entered loop cannot go green with it in place, and Decision 9 prints Decision 8's halt block again. The operator picks option 2.
**What happens:** At the first stop, option 2 is well defined: nothing was applied for the finding, so "record ... and continue" goes on to step 7. At the second stop the tree holds the fix and the tests are red. The menu text reads "Override — commit with each finding above recorded as overridden", and line 112 says "continue", while line 118 says "Nothing is committed while tests are red." The spec does not say whether the override releases the fix so the loop may undo it, what the loop count is on resume, or what `overridden by operator` means for a tree that may still contain the fix. Read literally, the Blocks fix stays protected after the override, the loop resumes, cannot go green, and prints the halt block a third time. A careful agent will most likely revert the fix and resume, or ask the operator, and the red-tests rule rules out a commit; so this does not gate. It is a path the round-1 fix opened and left for the agent to work out.
**Why the spec misses it:** Decision 9 reuses Decision 8's block as written, and the three options were worded for a finding with no fix in the tree.
**Suggested fix:** Add to Decision 9, after "This is a second stop, separate from the one Decision 8 describes.": "At this stop the options mean: 1 — the operator fixes by hand; on resume the finding is `fixed by operator` and the loop restarts with a fresh count of 5. 2 — the finding is `overridden by operator`; its fix may now be undone, and the loop restarts with a fresh count of 5. 3 — as in Decision 8. Tests must still be green before the commit under every option."

### F-2: An unusable Blocks finding has no stated group tag or count
**Severity:** P3
**Where:** spec § Decision 6, line 77; § Decision 10, lines 136 and 142
**Edge case:** A finding labelled as a blocker with no location, after the operator picks fix-by-hand or override.
**What happens:** The Findings line offers `[Blocks | Fix or record | Record only | unusable]` as one choice. The agent picks either `[unusable]` with disposition `fixed by operator`, or `[Blocks]`. The `Blocks: <n>` header and the PR-body counts differ by one depending on the pick. Nothing is lost; the record is just not uniform.
**Why the spec misses it:** Round 1's fix made an unusable finding able to be a Blocks finding; the template still treats the two as exclusive.
**Suggested fix:** Add to Decision 10: "An unusable finding whose label maps to Blocks is written `[Blocks]`, with `(no location)` or `(no problem statement)` in place of the missing part, and is counted under Blocks."

### F-3: Halt option 1 marks every listed finding as fixed by operator
**Severity:** P3
**Where:** spec § Decision 8, line 112
**Edge case:** The halt block lists three findings; the operator fixes two by hand and resumes.
**What happens:** "On resume, record those findings as `fixed by operator`" records all three. The third is recorded as fixed without having been touched. The operator is present and made the call, so this is a record-accuracy matter only.
**Suggested fix:** Change to: "on resume, record as `fixed by operator` the findings the operator says were fixed; any other listed finding is `overridden by operator`."

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 0

STATUS: GREEN
