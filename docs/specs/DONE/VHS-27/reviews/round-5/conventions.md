# Conventions Review — round 5 (delta)

Grounding: spec re-read from disk (`C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-27.spec.md`, 499 lines), the brief, `AGENTS.md`, the three round-4 lens reports, the wiki `state.md` for vigil-skills and the VHS decision filenames, and `skills/spec-cycle/SKILL.md` for the strings the fold names. The wiki has no `architecture.md` for this project. I matched wiki decisions by filename and `state.md` summary only and did not open the decision pages; nothing in the VHS-43, VHS-47 or VHS-55 summaries conflicts with the changed regions. Tracker and shared memory were not called, as instructed.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | A STATUS-only open set still lets a red marker go green | CLOSED | § No-op step 4 (line 173): any `<lens>/STATUS` line replaces the token with `mode: full (open findings unreadable)`, discards the delta start and recomputes `start` before the pending write. Steps 5 and 7 (lines 174, 176) dispatch delta only when the open set has no such line. Decision 11 (line 84), Decision 14 (line 96), § Dispatch (line 319), § Delta contract (line 350), § Two counters pass 2 (line 204), scenario 15 (line 438), test plan (lines 454, 461). All seven manifest sections carry the fold. See F-1 below for a P2 gap on the pass-2 arm. |
| correctness | F-2 (P2) | Out of scope still says a delta pass uses the routing rules unchanged | CLOSED | § Out of scope line 488 carves out the pass-2 recount and points at Decision 8 (line 72). |
| correctness | F-3 (P2) | Grill row templates still record `round_cap` on a delta halt | CLOSED | § Stop screens line 379 names `Deferred in: round <C> (grill)` and `Scope: operator — round-<C> grill` in the revise step and the deferred-row template. Those are the three sites in `skills/spec-cycle/SKILL.md` today (lines 587, 602, 608). |
| correctness | F-4 (P3) | ticket not cached | CLOSED | § Deferred (P2+) line 499 records the round-4 re-file with no spec change. Not re-filed, per instruction. |
| edge-cases | F-1 (P1) | A suffixed `§` phrase suppresses the line and names no heading | CLOSED | § Changed regions line 291: split `Where` on `;`, match by equality or longest heading-text prefix, fall back to the line against the predecessor copy, then to every heading; a non-matching `§` phrase does not discard the line. Decision 15 (line 100), § Dispatch (line 321), scenario 17 (line 442, with the three house-form Wheres and `spec.md:173`), test plan (line 461). Decision 5 is in the manifest for this finding but carries only the edge-cases/F-2 sentence; nothing in this finding needed an edit there. |
| edge-cases | F-2 (P2) | An untracked brief is code drift, so the clean no-op never fires | CLOSED | Decision 5 (line 60), § Changed regions line 282 (drop the brief path, spec path and the ticket's `reviews/` tree before the citation tests), scenario 18 (line 444), test plan (line 461). |
| edge-cases | F-3 (P3) | ticket not cached | CLOSED | Same as correctness/F-4. |
| conventions | F-1 (P3) | ticket not cached | CLOSED | Same as correctness/F-4. |

Deferred-findings check: the spec has no `## Deferred — follow-up required` section, so the preamble, row and ceiling tests do not apply. `## Deferred (P2+)` is a different section. No manifest line is a `deferred:` disposition.

Brief fences, checked in the changed regions only:
- No new verdict-marker field (lines 189, 490).
- No author-side check script (line 489).
- FROZEN/REWRITE is unchanged in a full invocation (lines 197, 487).
- The Out-of-scope carve-out at line 488 is an explicit, reasoned deviation from the brief's "uses them as they are" sentence. It records the Decision 8 rule that round 3 settled (conventions/F-3), so it is not re-filed here.
- The agent text added by the fold (the `<lens>/STATUS` paragraph in `# Delta scope`) cites no skill line and no repo path.

## Findings

### F-1: The pass-2 STATUS stop is an unflagged third exit with no printed line, scenario or checklist row
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Two counters, line 204; spec § Stop screens, line 381; spec § Scenarios; spec § Test plan
**Convention violated:** Silent addition against the brief (class d), and the skill's pattern that every stop that leaves the marker pending prints a named line.
**Evidence:** Line 204 adds: "Before this pass is dispatched, if pass 1's open set contains a `<lens>/STATUS` line, do not dispatch, do not write a green marker, leave the marker pending, and stop without Phase 3." Brief Decision 8 and spec Decision 8 (line 72) give pass 2 one red exit, the existing halt menu. Decision 11 (line 84) and § Dispatch (line 319) say a STATUS line "takes that same full pass" via § No-op step 4, which does not run between passes. The sibling stop in the same bullet prints `code-drift: skipped (git error)`, is named in § Stop screens line 381, walked in scenario 12 and checked in the test plan. The skill's own pending stop prints `fold exceeds brief: … marker left pending` (`skills/spec-cycle/SKILL.md`, routing step 3). The STATUS stop has none of these. The operator gets a pending marker and no reason.
**Suggested fix:** Give the stop a printed line in the existing style, for example `open findings unreadable: <lens>/STATUS — pass 2 not dispatched; marker left pending`. Name it in Decision 8 as the second non-menu stop, add it to the § Stop screens sentence at line 381, add one sentence to scenario 15 or 12, and add it to the test-plan row at line 454.

### F-2: The `<lens>/STATUS` paragraph in the agents' `# Delta scope` block covers a case the skill now never sends
**Severity:** P3
**Where:** spec § Delta contract, line 350
**Convention violated:** No machinery beyond what the finding needs.
**Evidence:** § No-op step 4 (line 173) turns any open set with a `<lens>/STATUS` line into a full pass, whose prompt omits `open_findings` (line 323). The pass-2 bullet (line 204) stops before dispatch on the same condition. No delta prompt can carry such a line, yet four installed agent files gain a paragraph telling the reviewer to "Ignore it as scope."
**Suggested fix:** Either drop the paragraph, or keep it and state in § Delta contract that it is a guard for a skill and agent installed at different versions. The author can pick; the spec is fine either way.

### F-3: Scenario 15 contradicts its own premise and repeats two sentences
**Severity:** P3
**Where:** spec § Scenarios, line 438
**Convention violated:** Clarity of the behavioral oracle (§ Test plan line 448 makes the scenario list the oracle).
**Evidence:** The scenario opens "Each standing report exists and has a STATUS line", then conditions on "or a standing report is missing". It states "`start` is recomputed by § Mode" and the `mode: full (open findings unreadable)` token twice each. The title, "no parseable P0/P1 heading, nothing else changed", now covers two distinct arms: a STATUS line present, and both sets empty.
**Suggested fix:** Rewrite as two short arms: (a) a STATUS line is in the open set (missing report, missing STATUS, or a count without a heading); (b) both sets empty. Give one shared outcome sentence and one pointer to scenario 16.

### F-4: The prefix example is already an equality match after the comma cut
**Severity:** P4
**Where:** spec § Changed regions, line 291
**Convention violated:** Nit.
**Evidence:** "take the phrase up to a comma", then "`Changed regions` matches `Changed regions, line 288`" is offered as a longest-prefix example. After the comma cut the phrase is `Changed regions`, which is equality. `Mode lines 162–164` (scenario 17) is the form that actually exercises the prefix arm. No-op step 3 (line 172) and § Dispatch (line 319) also keep "so that set is not empty", a rationale from the superseded design.
**Suggested fix:** Use `Mode` matching `Mode lines 162–164` as the second prefix example, and drop the two leftover rationale clauses.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 1

STATUS: GREEN
