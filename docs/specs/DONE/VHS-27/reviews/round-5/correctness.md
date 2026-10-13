# Correctness Review — round 5 (delta)

Both round-4 P1s are closed in the current spec text. I found no new P0 or P1 in the changed regions; two P2s and two P3s follow.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | A STATUS-only open set still lets a red marker go green | CLOSED | § No-op step 4 (line 173) selects `mode: full (open findings unreadable)` when the open set holds any `<lens>/STATUS` line, before the pending write, and recomputes `start`. Steps 5 and 7 (lines 174, 176) dispatch delta only when no such line is present. Decisions 11 and 14 (lines 84, 96), § Mode line 164, § Dispatch line 319, § Two counters line 204 (pass-2 stop), scenario 15 (line 438) and test plan lines 454 and 461 agree. I walked every verdict/set combination through steps 4–7 and found no path that reaches a delta dispatch with a heading-less line. |
| correctness | F-2 (P2) | Out of scope still says a delta pass uses the routing rules unchanged | CLOSED | § Out of scope line 488 carves out the pass-2 recount and points at Decision 8. It matches Decision 8 (line 72) and § Two counters line 204. The rule it overrides is real: `skills/spec-cycle/SKILL.md:627` reverts when `2 ≤ round < round_cap`. |
| correctness | F-3 (P2) | Grill row templates still record `round_cap` on a delta halt | CLOSED | § Stop screens line 379 names `Deferred in: round <C> (grill)` and `Scope: operator — round-<C> grill` in the revise step and the deferred-row template. Those strings exist today with `round_cap` at `skills/spec-cycle/SKILL.md:587`, `:602`, `:608`. |
| correctness | F-4 (P3) | ticket not cached | CLOSED | `## Deferred (P2+)` line 499 records it with no spec change. Not re-filed this round, per the dispatch instruction. |
| edge-cases | F-1 (P1) | A suffixed `§` phrase suppresses the line and names no heading | CLOSED | § Changed regions line 291 splits `Where` on `;`, matches by equality or longest heading-text prefix, falls back to the line in the predecessor `spec.copy.md` when no heading matches, and emits every heading when neither works. Decision 15 (line 100), § Dispatch line 321, scenario 17 (line 442) and test plan line 461 agree. I ran the round-3 and round-4 `Where` strings through the rule: `No-op step 4`, `Mode lines 162–164`, `Changed regions, line 288`, `Dispatch line 317` and `Scenarios, scenario 17` all resolve; `Decision 15, line 100` matches no heading by prefix and correctly falls to line 100. A residual mis-match case is F-2 below. |
| edge-cases | F-2 (P2) | An untracked brief is code drift, so the clean no-op never fires | CLOSED | § Changed regions line 282 drops the brief path, the spec path and the ticket's `reviews/` tree before the citation tests, and says a filename-only match does not see a dropped path. Decision 5 (line 60), scenario 18 (line 444) and test plan line 461 agree. A residual for other tickets' files is F-4 below. |
| edge-cases | F-3 (P3) | ticket not cached | CLOSED | Same as correctness F-4. |
| conventions | F-1 (P3) | ticket not cached | CLOSED | Same as correctness F-4. |

Grounding notes:
- **Manifest:** it carries a line for each of the two round-4 P1s, and each named section holds the fold.
- **Deferred findings:** the spec has no `## Deferred — follow-up required` section, so the routing checks do not apply.
- **Edit-site anchors:** every anchor the changed regions name still resolves in `skills/spec-cycle/SKILL.md`, the four `agents/spec-reviewer-*.md` files, `docs/spec-workflow-reference.md` and `AGENTS.md`. The spec carries no file:line anchor that is stale.
- **Recent commits on the touched files:** `d3730b1` (2026-10-12), `7abe102` and `5f640d0` (2026-10-11). The spec is written against `c01286d`, which is HEAD.

## Findings

### F-1: The pass-2 STATUS stop prints nothing and no scenario walks it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Two counters, line 204; spec § Stop screens, line 381; spec § Scenarios, scenario 1
**Claim:** "Before this pass is dispatched, if pass 1's open set contains a `<lens>/STATUS` line, do not dispatch, do not write a green marker, leave the marker pending, and stop without Phase 3. A later run takes row 4."
**Why this is wrong:** This exit is new in the round-4 fold. The neighbouring code-drift stop in the same bullet prints `code-drift: skipped (git error)`, and § Stop screens line 381 names that stop as distinct from the halt menu. The STATUS stop has no printed line, so the operator sees the run end with a pending marker and no reason. Scenario 1 still says a loop-red pass 1 leads to pass 2 at cumulative round 6 with no exception. Decision 8, scenario 12 and the test plan do not mention the stop either. The trigger is realistic: today a reviewer that returns no parseable STATUS line is a synthetic P0 (`skills/spec-cycle/SKILL.md:947`), and a crashed scalability lens gets a stub (`:491-496`); a full invocation carries on past both. The stop is safe, since the marker stays pending, but an implementer has to guess the message.
**Suggested fix:** Give the stop a printed line in § Two counters, for example `open findings unreadable: <lens>/STATUS — pass 2 not dispatched`. Name it beside the code-drift stop in § Stop screens line 381. Add one sentence to scenario 1 or 15 and one clause to test plan line 454.

### F-2: A prefix match on the wrong heading still discards the line
**Severity:** P2
**Where:** spec § Changed regions, line 291; spec § Decision 15, line 100
**Claim:** "Select every current heading whose text equals that phrase, or whose text is the longest heading-text prefix of that phrase … A matching heading does not also use the line."
**Why this is wrong:** The prefix is a raw text prefix with no word boundary and no check against the cited line. A `Where` of `spec § Mode table, line 96`, meaning Decision 14, matches `### Mode` and drops line 96. `spec § Scope row, line 287`, meaning the numbered item in § Changed regions, matches `## Scope` and drops line 287. In both cases the finding's real section is not named, which is the round-4 defect again in a narrower form. I rate it P2 rather than P1 because closure verification is not limited to `changed_regions` (§ Delta contract line 346), so the open finding is still checked; only new critique on that section is lost.
**Suggested fix:** When a clause matches a heading by prefix and also has a line number, resolve the line as well and emit the union of both headings. Keep "does not use the line" for an equality match only. Add one such `Where` to scenario 17.

### F-3: Scenario 15 contradicts its own premise and repeats two sentences
**Severity:** P3
**Where:** spec § Scenarios, line 438
**Claim:** "Each standing report exists and has a STATUS line. … or a standing report is missing, the open set contains `<lens>/STATUS (P0)`."
**Why this is wrong:** The premise says every standing report exists, then the scenario covers a missing one. The token sentence and "`start` is recomputed by § Mode" each appear twice, once for the STATUS branch and once for the both-empty branch. The outcome is the same in both, so nothing is wrong in behaviour, but the row reads as two scenarios merged.
**Suggested fix:** Open with "Either (a) a standing report is missing, has no STATUS line, or has STATUS P0+P1 above zero with no P0/P1 heading, or (b) both sets are empty." State the token and the `start` recompute once.

### F-4: Another ticket's untracked review files still match a filename-only span
**Severity:** P3
**Where:** spec § Changed regions, lines 282 and 286
**Claim:** "drop the resolved brief path, the spec path `docs/specs/TODO/<TICKET-ID>.spec.md`, and every path under `docs/specs/TODO/<TICKET-ID>.reviews/` from the changed-path set."
**Why this is wrong:** The drop covers this ticket only. Line 286 lets a filename-only span match any changed path with that filename. In this repo `docs/specs/TODO/VHS-41.reviews/` is untracked today, so `git ls-files --others` lists its `verdict.md` on every run, and after this change it will also hold `spec.copy.md` and `ledger.md`. A spec that backticks one of those bare names never reaches the no-op. Few specs cite those names; this spec is one that does.
**Suggested fix:** Drop every path under `docs/specs/TODO/*.reviews/`, or exempt the artifact filenames this skill writes from the filename-only rule.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 2 | P4: 0

STATUS: GREEN
