# Edge-Cases Review — round 1

(Round 1 of v2. Per the orchestrator brief, v1 reviews under `docs/specs/TODO/VHS-5.reviews/v1/` are context, not a prior round to close out.)

## Closure of round N-1 findings

N/A — round 1 of v2. The two v1 review rounds are preserved as audit context but are not load-bearing prior-round findings for v2 since v2 is a structural rewrite (drops Location A entirely).

## Findings

### F-1: `--stat = "0"` assertion includes substring `--stat` — also matches `--statistics`, `--stat-name`, or any future gh flag containing that substring

**Severity:** P3
**Where:** spec.md:171 (Test command, clause 2: `test "$(grep -c -- '--stat' skills/review-pr/SKILL.md)" = "0"`)
**Edge case:** `grep -c -- '--stat'` matches any occurrence of the substring `--stat`, anywhere on any line. If a future unrelated edit introduces `--statistics`, `--stat-name`, `--stat-count`, or even a sentence like "the diff `--stat` flag was renamed to ..." inside a comment block, the assertion fails even though the P1 fix is intact. Today there is no other `--stat*` usage in SKILL.md (verified — current count is 1; post-fix should be 0), so this is forward-risk only.
**What happens:** A future maintainer adds a documentation note that mentions `--stat` (for historical context, deprecation, troubleshooting) and the Test command regresses to RED with no real defect.
**Why the spec misses it:** The substring match was the simplest available negative assertion. The spec deliberately chose presence/absence rather than line-anchored asserts (per the round-2 v1 trade-off discussion), so trading forward-fragility for simplicity is consistent with the rest of the test command.
**Suggested fix:** Tighten to a more specific pattern, e.g. `grep -c -- 'gh pr diff <N> --stat' skills/review-pr/SKILL.md` (or even `-w` for word-boundary matching: `grep -wc -- '--stat'`). The `-w` form would catch only the exact flag and not substring matches. Optional — leave as-is is also defensible because the spec author already opted into substring-match simplicity for `--name-only`.

### F-2: Two locations + `-ge "2"` gives no headroom for legitimate accidental duplication or an unrelated future polling phase

**Severity:** P3
**Where:** spec.md:156 (Test plan item 4: `-ge "2"`), spec.md:171 (Test command, clause 4)
**Edge case:** The v2 spec lands "intervals are aspirational" at exactly two locations (Phase 6d-Phase 1 and Phase 6d-Phase 2). The Test command asserts `-ge "2"`. With exactly the two target locations, the floor is right at the bottom of the valid range — there is no slack. If the implementer accidentally edits only one of the two locations, the assertion fails (correct behavior — surfaces the missed edit). But if a *third* unrelated polling block is added in a future spec without copying the phrase, `-ge "2"` continues to pass because the original two are still there. So `-ge "2"` reads as "at least one of the two cadence locations must have the phrase plus one more, OR both must," but in practice it requires both — and the spec does not say so explicitly. The spec says (Test plan, item 4) "`-ge "2"` (not `= "2"`) keeps the assertion resilient against future unrelated edits." But "future unrelated edits" that *delete* one occurrence (e.g., a refactor that consolidates 6d-Phase 1 and 6d-Phase 2 into one phase) would silently regress. Trade-off, not a bug.
**What happens:** A future refactor merges 6d-Phase 1 and 6d-Phase 2 into a single block while preserving exactly one "intervals are aspirational" sentence. Count drops to 1, Test command fails — but only on the next time someone runs this spec's Test command, which is unlikely since the spec is single-use.
**Why the spec misses it:** The spec accepts this trade-off implicitly (it's a single-use spec; future refactors are out of scope). The v1 round-2 review accepted the symmetric trade-off for the `-ge "3"` form. This finding just notes that with the floor right at the legitimate count (2 == 2), the floor's "resilience" claim is weaker than at v1's `-ge "3"` against a count-of-3 target.
**Suggested fix:** None required. Optional: change Test plan item 4 to `= "2"` to make the gate symmetric with the `--stat = "0"` and `2-minute polling window = "0"` clauses (all three are exact-count assertions in a single-use spec). Keeps the intent ("exactly two cadence locations, no more, no less") legible. Either form is defensible.

### F-3: Done-when #3 claims "VHS-4 satisfies the brief for 6a" — but VHS-4's enforcement is a wall-clock *total* bound, not the inter-poll interval the brief originally critiqued

**Severity:** P3
**Where:** spec.md:182 (Done-when #3), spec.md:48-54 (Decision 3 rationale), brief.md:48 (Done-when #3: "The 6a / 6d cadence text either matches actual runtime behavior (intervals enforced) or the wording is revised to reflect that intervals are not enforced.")
**Edge case:** The brief's Done-when #3 has a binary test: cadence text either (a) matches runtime, or (b) is revised. The spec's stance is "VHS-4 satisfied (a) for 6a." But VHS-4 enforces *total wall-clock duration* (5 min / 10 min via `FIRST_POLL_TIME`); it does NOT enforce the inter-poll "every 15 seconds" claim — Phase 6a line 185 still says "every 15 seconds" and the agent harness still fires Bash tool calls back-to-back. So the inter-poll interval remains aspirational in 6a, just as in 6d. The spec acknowledges this on spec.md:16 ("the inter-poll 'every 15 seconds' claim in 6a is still aspirational at the per-call granularity even though total duration is wall-clock-bounded") and spec.md:52 ("The 'every 15 seconds' inter-poll claim in 6a is still aspirational"). The spec then concludes that adding "intervals are aspirational" to 6a "would only restate one fact while obscuring another" — that is a legitimate clarity argument, but it does not change the underlying brief-satisfaction question. Brief Done-when #3 reads as a strict OR over per-location text, and "per-call interval is aspirational in 6a too" is uncovered by either branch (a) or branch (b) for that location.
**What happens:** No runtime consequence — Phase 6a's total-duration bound is real and the inter-poll claim's not-enforced nature is essentially harmless (sub-second polls vs. ~15s claim means agent over-polls, never under-polls). A future reader who reads the brief and Phase 6a side-by-side will notice that the brief asks for one of two outcomes per location and 6a got neither, strictly speaking. The spec author chose to declare partial satisfaction sufficient; that is a reasonable call but worth flagging because the brief's Done-when language is explicit.
**Why the spec misses it:** Decision 3 reframes the brief's binary test as "VHS-4 addressed the substantive concern (no unenforced *total* duration), so the cadence-relabeling exercise is redundant for 6a." That reframing is defensible but does deviate from the brief's literal text. Decision 5 names this explicitly ("spec author may verify the underlying code and adjust scope when reality has shifted"), which preempts a correctness-lens finding but leaves an edge-cases note: a strictly literal future reader could still file "Phase 6a's 'every 15 seconds' is aspirational and the spec did nothing about it."
**Suggested fix:** Optional one-sentence amplification in Decision 3 or Done-when #3: "Phase 6a's *inter-poll* '15 seconds' claim remains aspirational by the same back-to-back-tool-call mechanic, but the spec leaves that wording intact because changing it without also fixing the surrounding wall-clock-bound prose would be more confusing than clarifying. A follow-up spec could revisit this if the inter-poll wording proves a source of bug reports." Cheap insurance against future-reader confusion.

### F-4: `2-minute polling window = "0"` assertion is sound, but does not guard the symmetric "3 minutes" wording in Location C

**Severity:** P3
**Where:** spec.md:158 (Test plan item 5), spec.md:171 (Test command, clause 5), spec.md:130-137 (Location C edit), spec.md:138 (`CHANGES_REQUESTED after timeout` left intact)
**Edge case:** The Test command verifies the secondary wording rewrite for Location B (line 297, "2-minute polling window" → "exhausting the polling attempts"). Location C's original wording at line 322 is "every 20 seconds, up to 3 minutes" and gets rewritten. But Location C also has the "after timeout" outcomes-block sentence (line 326), which the spec explicitly leaves untouched (spec.md:138). The Test command does not assert on `3 minutes`, so an implementer who applies the Location C rewrite incompletely (e.g., leaves "up to 3 minutes" in place because they only deleted the "every 20 seconds" half) passes the test command IF the "intervals are aspirational" phrase still landed. Symmetric to the v1 round-2 F-5 finding (which produced clause 5); v2 added clause 5 for Location B but not Location C.
**What happens:** An implementer who does a partial replacement at line 322 — e.g., changes "every 20 seconds" to "in a tight loop" but forgets "up to 3 minutes" — could ship `"...Poll by making **individual Bash tool calls** in a tight loop, up to 3 minutes. ...intervals are aspirational because the agent harness fires Bash tool calls back-to-back."` That self-contradicts (3 minutes + back-to-back) and would pass the Test command. Low likelihood: the design block specifies the full replacement sentence, so an implementer following the spec literally would not produce this state. But the structural gate does not catch it.
**Why the spec misses it:** The v2 Test command added clause 5 for Location B's "2-minute polling window" leftover (from v1 round-2 F-5) but did not add a symmetric clause for Location C's "3 minutes" / "every 20 seconds" leftovers. The asymmetry is because Location B's leftover is on a *separate line* (line 297), while Location C's leftover is *within* the same sentence being replaced — so a literal replacement of the whole sentence handles it, and a guard would be redundant if the implementer follows the spec verbatim.
**Suggested fix:** Optional sixth clause: `test "$(grep -c 'every 20 seconds' skills/review-pr/SKILL.md)" = "0"` — confirms the seconds-based cadence claim is gone from Location C. Or `test "$(grep -c 'up to 3 minutes' skills/review-pr/SKILL.md)" = "0"`. Either matches the defensive style of clause 5. Cheap addition; not load-bearing because the design block is explicit about the full replacement.

### F-5: `--name-only -ge "1"` is sound today but the Done-when #2 manual step does not specify which PR to test against

**Severity:** P4
**Where:** spec.md:163 (Manual step 2: "Run `gh pr diff <N> --name-only` against any PR. Confirm exit 0 and a list of file paths.")
**Edge case:** "Against any PR" is informal. If the verifier picks a PR they don't have access to (auth error), a PR in a different repo without `gh repo set-default` configured, or a PR with zero file changes (degenerate but possible — e.g., a revert that returns to the merge-base), the manual step could fail or produce no output and the verifier might mark it as inconclusive. The structural gate already confirms the literal `--name-only` is present in SKILL.md, so the manual step is genuinely an end-to-end check — but it implicitly assumes a "normal" PR.
**What happens:** Verifier runs the command against a closed/private/empty PR, sees no output or an error, and either (a) goes hunting for a non-bug, or (b) marks the spec "untestable" and moves on. Low probability — most repos the verifier has handy will have at least one accessible PR with changes.
**Why the spec misses it:** Spec deliberately keeps manual steps light. Done-when #2 maps to brief Done-when #2 ("runs without error and produces output that supports triage scope-awareness") which is also informal.
**Suggested fix:** None required. If the spec wants to harden: "Run against any open PR in `ziomancer/vigil-skills` with at least one file change (e.g., PR #6 or PR #7 if still queryable)." Citing a known-good PR makes the step concrete. Optional.

### F-6: Re-entry / re-runs not affected — confirmed text-only change (no finding)

**Severity:** N/A (negative result documented)
**Where:** All three edits.
**Edge case probed:** If `/review-pr` re-enters Phase 6d on a second run (Phase 1 re-poll, or Phase 2 re-poll after a fix-push-review cycle), does the new wording change any control flow?
**Verification:** The Phase 6d edits are pure documentation. The attempt counts (8 for Phase 1, 9 for Phase 2) are explicitly preserved verbatim. The GraphQL filter change (P0) is a one-character string-literal edit inside the jq filter; behavior is "produce the same merged-threads array shape, but now actually populated instead of always empty." That is a *fix* of the existing control flow, not a new branch. No caller of any of these three SKILL.md sections sees a different return shape.
**Result:** No finding. Re-entry semantics are preserved.

### F-7: Spec.md's own `--stat` mention does not affect Test command (negative confirmation)

**Severity:** N/A (negative result documented)
**Where:** spec.md:100 (Design block "Current:" code fence contains `--stat`); Test command targets `skills/review-pr/SKILL.md` only.
**Edge case probed:** If `--stat` appears anywhere accessible to the Test command, the assertion `= "0"` fails.
**Verification:** The Test command (spec.md:171) explicitly targets `skills/review-pr/SKILL.md`. The spec.md file is not grepped. The brief and the v1 reviews also contain `--stat` (brief.md:28; v1 reviews discuss it) but none are in the Test command's path. Confirmed safe.
**Result:** No finding.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 4 | P4: 1

STATUS: GREEN
