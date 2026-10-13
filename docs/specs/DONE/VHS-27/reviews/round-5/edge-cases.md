# Edge-Cases Review — round 5 (delta)

Both round-4 P1s are closed in the current spec text. The fold left four P2 gaps and two smaller ones; none produces a wrong verdict or blocks the gate.

Grounding: spec, brief and the three round-4 reports were read fresh from disk; `synthesis.md` was not read. The tracker and shared memory were not called, as instructed. The spec has no `## Deferred — follow-up required` section (`## Deferred (P2+)` at line 497 is a different section), so the deferred-row routing checks do not apply.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | A STATUS-only open set still lets a red marker go green | CLOSED | § No-op step 4 (line 173) replaces the token with `mode: full (open findings unreadable)` before the pending write and recomputes `start`. Steps 5 and 7 (lines 174, 176) exclude a `<lens>/STATUS` line. Decision 11 (line 84), Decision 14 (line 96), § Dispatch (line 319), § Two counters pass-2 stop (line 204), § Delta contract (line 350), scenario 15 (line 438), test plan (lines 454, 461). Steps 4–7 are exhaustive over red/green × empty/non-empty × STATUS present. |
| correctness | F-2 | Out of scope still says a delta pass uses the routing rules unchanged | CLOSED | § Out of scope line 488 carves out the pass-2 recount and points at Decision 8. |
| correctness | F-3 | Grill row templates still record `round_cap` on a delta halt | CLOSED | § Stop screens line 379 names `Deferred in: round <C> (grill)` and `Scope: operator — round-<C> grill` in the revise step and the deferred-row template. |
| correctness | F-4 | ticket not cached | CLOSED | § Deferred (P2+) line 499 records it with no spec change. Not re-filed, per this pass's instructions. |
| edge-cases | F-1 | A suffixed `§` phrase suppresses the line and names no heading | CLOSED | § Changed regions line 291: split on `;`, equality or longest heading-text prefix, line fallback against the predecessor copy, every-heading fallback, `spec.md` tokens defined. Decision 15 (line 100), § Dispatch (line 321), scenario 17 (line 442) with the three suffixed Wheres and `spec.md:173`, test plan (line 461). Residual variants are F-1 and F-2 below. |
| edge-cases | F-2 | An untracked brief is code drift, so the clean no-op never fires | CLOSED | § Changed regions line 282 drops the brief path, the spec path and the ticket's `reviews/` paths before both citation tests. Decision 5 (line 60), scenario 18 (line 444), test plan (line 461). A wider variant is F-3 below. |
| edge-cases | F-3 | ticket not cached | CLOSED | Same as correctness F-4. |
| conventions | F-1 | ticket not cached | CLOSED | Same as correctness F-4. |

## Findings

### F-1: An abbreviated heading title with no line emits every heading
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Changed regions, line 291; spec § Decision 15, line 100
**Edge case:** An open P0 or P1 has a Where of `spec § Decision 8` — the reviewer output contract's `spec § <heading>` form, with no line. The heading text is `Decision 8 — Two counters, at most two delta passes on every tier`. The same happens for a full title cut at its own comma (`§ Decision 8 — Two counters, at most…` becomes the phrase `Decision 8 — Two counters`; Decisions 3 and 8 both have commas).
**What happens:** The match is one-directional: a heading matches when its text equals the phrase or is a prefix of it. Here the phrase is a prefix of the heading, so nothing matches. With no line, the clause "has neither a matching heading nor a placeable line" and every current heading is emitted. The delta pass then explores the whole spec under the two-pass budget, which is the churn the ticket exists to stop. The verdict is not wrong, and with a line the predecessor-copy fallback resolves correctly.
**Why the spec misses it:** Scenario 17 covers only phrases longer than the heading (`No-op step 4`, `Mode lines 162–164`). Numbered-decision headings, which every spec in this repo has, are abbreviated the other way.
**Suggested fix:** Add a third match arm: when no heading equals the phrase or is a prefix of it, select every heading whose text begins with the phrase followed by a non-alphanumeric character or end of text (`Decision 8` matches `Decision 8 — …` and not `Decision 80`). State that the comma cut is retried against the uncut clause when the cut phrase matches nothing. Add `spec § Decision 8` to scenario 17.

### F-2: A short or ancestor prefix match discards a line that points elsewhere
**Severity:** P2
**Where:** spec § Changed regions, line 291 ("A matching heading does not also use the line"); spec § Decision 15, line 100
**Edge case:** Where is `spec § Design, line 289` or `spec § Decisions (Decision 11), line 84`. `## Design` and `## Decisions` match by equality or prefix, and their exclusive bodies are empty (lines 34–35, 106–107). A prefix collision does the same: `§ Mode table, line 96` matches `### Mode` although the finding sits in Decision 14.
**What happens:** The parent or wrong heading is emitted, the line is not used, and the section the finding actually sits in is not in the delta scope. Closure verification still reads the cited text (the delta contract does not limit closures), so the open finding itself is checked. What is lost is new critique on that section.
**Why the spec misses it:** "A match does not use the line" was written when a match meant an exact title. The round-4 fold widened a match to any prefix and did not revisit that sentence. The original reason for it (a moved line overriding a real title) no longer holds, because lines now resolve against the predecessor copy.
**Suggested fix:** When a clause has both a matching heading and a line, also resolve the line in the predecessor copy and emit the union. That only widens scope. Require the prefix to end at a non-alphanumeric boundary in the phrase.

### F-3: Other tickets' review trees and attempt archives still defeat the no-op
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Changed regions, line 282; spec § Scenarios, scenario 18; spec § Decision 5, line 60
**Edge case:** The tree holds untracked review files that are not under this ticket's `reviews/` directory. This repo has them today: `docs/specs/TODO/VHS-41.reviews/round-1/correctness.md` and `docs/specs/TODO/VHS-41.attempt-1/spec.md`, `…/brief.md`, `…/reviews/round-4/grill.md`. A ticket's own `<TICKET-ID>.attempt-N/` archive is also outside the dropped prefix. The spec backticks a bare filename such as `correctness.md`, `spec.md` or `grill.md`; this spec does at lines 171, 291, 319 and 377.
**What happens:** `git ls-files --others` lists those files on every run regardless of `baseline.commit`. A filename-only span matches any changed path with that filename, so the citing headings are code drift permanently. Step 6 never fires and each re-run dispatches a delta. Scenario 18's "the result is the no-op" is false for this spec in this repo. The outcome is an unnecessary delta pass, not a wrong verdict.
**Why the spec misses it:** The exclusion is scoped to this ticket's three locations, as round-4 F-2 suggested. Spec-cycle never commits, so sibling tickets' trees are untracked just as often.
**Suggested fix:** Drop every path under `docs/specs/TODO/` that matches `*.reviews/` or `*.attempt-*/`, not only this ticket's `reviews/`. Add a sibling ticket's untracked `reviews/` tree to scenario 18.

### F-4: The pass-2 `<lens>/STATUS` stop prints nothing and has no scenario
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Two counters, line 204; spec § Stop screens, line 381; spec § Scenarios
**Edge case:** Delta pass 1 is red and one reviewer returns no parseable STATUS line, or a 2c stub stands in for a crashed lens. The skill already lists reviewer status drift as a known failure mode.
**What happens:** Line 204 says not to dispatch pass 2, to leave the marker pending and to stop without Phase 3. No output line is named. The code-drift stop two sentences later prints `code-drift: skipped (git error)`, and § Stop screens line 381 names only that stop. The operator sees a run that ends with a pending marker and no reason. The next run takes row 4 and spends a full `round_cap` invocation, although pass 1's ledger and reports are intact.
**Why the spec misses it:** The fold added the stop for symmetry with § No-op step 4 and did not give it a message, a scenario or a test-plan line. Line 461 checks only the classification-time case.
**Suggested fix:** Name the printed line, for example `open findings unreadable: <lens>/STATUS — pass 2 not dispatched, marker left pending`, and add it to § Stop screens line 381 and to scenario 15. Consider dispatching pass 2 as `review_mode: full` within the same budget, as § Artifacts line 233 already does for an unreadable ledger, so one dropped STATUS line does not cost a full invocation.

### F-5: A clause with two `§` references or a line range is unspecified
**Severity:** P3
**Where:** spec § Changed regions, line 291
**Edge case:** Where is `spec § Decision 8 line 72 and § Decision 14 line 96` (the "and" form appears in round-4 closure evidence), `§ Mode, § No-op`, or `lines 344–348` where the range crosses a heading.
**What happens:** The split is on `;` only and the phrase runs "up to a comma". The first example yields one phrase with two line numbers and no rule for which to use. The second drops the second `§`. A range has no stated endpoint. A reasonable agent resolves each `§` and takes the first line of the range, but the spec does not say so. Case and whitespace sensitivity of the phrase comparison are also unstated.
**Why the spec misses it:** The rule was written against the three Wheres quoted in round-4 F-1.
**Suggested fix:** One sentence: each `§` in a clause starts its own phrase, a range resolves every line in it (or its first line), and the comparison ignores case and surrounding whitespace.

### F-6: Scenario 15 says every report exists and then lists a missing one
**Severity:** P4
**Where:** spec § Scenarios, scenario 15, line 438
**Edge case:** Reading the scenario as a test oracle.
**What happens:** The scenario opens with "Each standing report exists and has a STATUS line" and then includes "or a standing report is missing". It also states the `mode: full (open findings unreadable)` outcome and the `start` recompute twice.
**Why the spec misses it:** The fold appended the STATUS branch to the both-sets-empty text.
**Suggested fix:** Split it into 15a (STATUS line or missing report) and 15b (both sets empty), each with one outcome sentence.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 1 | P4: 1

STATUS: GREEN
