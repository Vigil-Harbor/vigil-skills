# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Row 7's `grep -c 'ref:' ≥ 8` unmeetable | **CLOSED** | spec.md:443–445 now `≥ 7 — matching lines, not occurrences: seed bullet, the `ref:` paragraph, four block lines, callers-map sentence; the file is unwrapped, one paragraph per line`. Verified: `grep -c 'ref:' skills/grilling/SKILL.md` = 0 today; max line length 649 (unwrapped); the four Designs add `ref:` to exactly 7 lines. `≥` absorbs an 8th if the seed sentences land as their own paragraph. |
| conventions | F-2 | Additions roll-up incomplete | **PARTIAL** | (a) F-numbering bullet added, spec.md:79–82, with the `:129` reuse anchor; (b) `rounds: 1/<round_cap>` bullet added, spec.md:83–85; (c) D7 now says "declared here, not in the additions roll-up: they are checklist bookkeeping, not constructs" (spec.md:134–135). Round-2's three items are closed. A new omission from the round-2 folds remains — F-1 below. |
| conventions | F-3 | `fence-empty` narrows an unnamed wiki decision | **CLOSED** | D4 spec.md:114–115 names `2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write` § 5; Risk 2 spec.md:540–545 quotes "Rejected — a success token for an empty interview", states the narrowing, and says `/spec-close` records it. Decision file re-read: `Status: active`, `Revisit when:` names VHS-33; § 5's rejected item matches the quote verbatim. |
| conventions | F-4 | Roll-up's both-lists wording narrower than Design 5 | **CLOSED** | spec.md:68–70: "printed under `left open` rather than `dispositioned` (it may still appear under `deferred to option 3`)". Matches Design 5 spec.md:322–326. |
| conventions | F-5 | D7 names rows 4 and 7; row 10 also supersedes row 6 | **CLOSED** | spec.md:133 "Together they supersede VHS-32 rows 4, 6 and 7". Verified against `docs/specs/DONE/VHS-32/spec.md:460` (row 6) — row 10 here carries `grep -c 'total_p0p1 == 0'` unchanged plus 2e/2f-menu/2g byte-identical, a superset. |
| correctness | F-1 | Row 7 `≥ 8` cannot pass | **CLOSED** | Same edit. |
| correctness | F-2 | `ref:` descent rule has no F-item clause | **CLOSED** | Design 1 spec.md:189–190: "a fact request from the question whose need raised it (or from the seed items directly when the need arose from the seed)". Four item kinds now enumerated against the block's four `ref:`-bearing lines; row 7 asserts the phrase. |
| correctness | F-3 | D5 cites `:555–560`, Design 5 cites `:556–561` | **CLOSED** | spec.md:119 now `:556–561`; agrees with spec.md:345 and § References spec.md:561. Verified: the paragraph is `skills/spec-cycle/SKILL.md:556–561`. |
| correctness | F-4 | `:151` keeps the Q form after `:108` is rewritten; row 9 pins it | **CLOSED** | Design 3 spec.md:274–277 makes the same clause replacement at `:151`; row 9 spec.md:452 narrows the no-hunk fence to `:136–150`; § Files to leave alone spec.md:39–40 excludes the `:151` bullet; row 6 spec.md:436–437 asserts `:151` contains "their fact needs are Open `F<n>` items". Verified `skills/grilling/SKILL.md:151` still reads "their questions are Open". |
| correctness | F-5 | D13's `question_cap` justification does not hold | **CLOSED** | D13 spec.md:165–167 restated as the no-change claim: "Unresolved fact needs already reached the hand-off as Open items under v1 (`:74`); this spec changes their rendered shape, not their count". |
| edge-cases | F-1 | Design 6's `:140` text contains "qualifiers", which row 16 forbids | **CLOSED** | Design 6 blockquote spec.md:356–358 ends at `spec author pins this`.`; the no-cause-qualifier rationale moved to prose at spec.md:360–361. Re-walked every added line to `grilling` and `spec-brief`: none matches `operator claim\|verif\|qualifier\|source: operator`. |
| edge-cases | F-2 | Row 7 `≥ 8` | **CLOSED** | Same edit. |
| edge-cases | F-3 | Descent rule enumerates three kinds, block defines four | **CLOSED** | Same edit as correctness/F-2. |
| edge-cases | F-4 | `:151` divergence | **CLOSED** | Same as correctness/F-4. |
| edge-cases | F-5 | Seeded finding yielding no item is in no step-5 list | **CLOSED** | Design 5 spec.md:326–328 adds "the lists report what the grill touched, not the full red list"; row 10 spec.md:459 asserts the string. |
| edge-cases | F-6 | `:143` records the fence reason only for `fence-empty` | **CLOSED (with a new roll-up gap — F-1 below)** | Design 6 spec.md:363–370 is now reason-keyed and carries the round-≥2 `empty-frontier` example. |
| edge-cases | F-7 | fence-empty discards seed-supplied facts | **CLOSED** | Design 3 spec.md:266–268 "`### Facts established` is rendered as on any exit"; Design 2 spec.md:236–238; Risk 2 spec.md:536 hedged to "normally no fact References". (Residual summary-text drift → F-2 below.) |
| edge-cases | F-8 | `:108` edit drops the fact-blocked question | **CLOSED** | Design 3 spec.md:272–274 is additive: "and any question that was waiting on one is Open with `unresolved because: blocked-on: F<n>`". Row 6 asserts "blocked-on: F<n>" in `:108`. |

No `scalability.md` exists in `round-2/`; `scale_lens == off` — nothing to ignore.

Gate trend: round 1 P0=2/P1=4/P2=18/P3=11/P4=4 → round 2 P0=2/P1=4/P2=8/P3=3/P4=1. Every round-2 P0/P1 was created by a round-1 fold. Round 3's job was to check whether the round-2 folds did the same; from this lens they did not.

## Findings

### F-1: The reason-keyed `:143` rule changes `/spec-brief` behavior on `empty-frontier`, and the additions roll-up does not carry it

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:363–370 (Design 6, the `:143` replacement) against spec.md:55–89 (`## Decisions` roll-up, seven bullets + "Nothing else")
**Convention violated:** Brief decision 12 and the spec's own D12 (spec.md:158–159): "The additions roll-up above is the complete list." The roll-up is what `/spec-cycle`'s Phase 3 drift-check reads (spec.md:56–57), so an incomplete one is the exact failure it exists to prevent. Same root as round-1 conventions/F-2 and round-2 conventions/F-2, recurring on a round-2 fold.
**Evidence:** The brief scopes reason-recording to one exit — `## Scope` row for `spec-brief`: "`fence-empty` handled like `empty-frontier` with the reason recorded (Q4)"; decision 4: "it goes through the hand-off block with empty sections, and the reason line stays for humans." The shipped rule Design 6 now writes is keyed on the *reason*, not the token, and its second example is `Interview: 2 rounds, exit empty-frontier (no candidate decision met the altitude fence)` "for a later-round fence-out" — a change to what `/spec-brief` writes on an exit path none of the brief's four items covers. `skills/spec-brief/SKILL.md:143` today reads only "`Interview: <n> rounds, exit <token>`, or `Interview: skipped (--no-grill)`".

The fold is good engineering — one rule beats two, it sits inside the line already being rewritten, and row 11's assertions still hold — which is why this is P2 and not P1: it is a category-(c) addition with a thin rationale rather than a construct the four items do not need. But nothing in the spec flags it as reaching past `fence-empty`, and D12's alternative disposition ("a reviewer finding that seems to need another construct goes to `## Deferred (P2+)` with its id") was not taken either. As written it is the silent-addition shape the drift-check is supposed to catch.
**Suggested fix:** One roll-up bullet in the shape the seven existing ones use, e.g.: "The `/spec-brief` References bullet is keyed on the header's *reason*, not the exit token (Design 6), so a round-≥2 `empty-frontier` fence-out also records `no candidate decision met the altitude fence`. Needed because Design 3 makes that reason load-bearing on both exits; one rule instead of two, inside the line already being rewritten (edge-cases R2 F-6)." Then re-check that "Nothing else" (spec.md:87) still holds.

### F-2: D4 still states the fence-empty contract as "empty sections", which Designs 2 and 3 no longer say

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:113 (D4), corroborated at spec.md:126 (D6) and spec.md:380–381 (Design 7's `/grill-me` blockquote), against spec.md:236–238 (Design 2) and spec.md:266–268 (Design 3)
**Convention violated:** Internal consistency between the `## Decisions` summary and the Design it summarizes — the same root as round-2 correctness/F-3 (two ranges for one paragraph) and round-2 correctness/F-4 (`:108` updated, `:151` left stale), both rated P2. `## Decisions` is what the Phase 3 drift-check reads against the brief.
**Evidence:** The edge-cases R2 F-7 fold narrowed the claim in the Designs: Design 2 — "On `fence-empty` Settled and Open frontier are empty; Facts established holds whatever was established"; Design 3 — "its Settled and Open frontier sections are empty, and `### Facts established` is rendered as on any exit". Risk 2 was correctly hedged to "normally no fact References" (spec.md:536). D4 was not: it still reads "It goes through the hand-off block with empty sections; the header's reason line stays" — an unqualified, general statement of the exit's contract that now contradicts its own Design. This matters because `/spec-brief` Phase 1 assembles "the problem statement, **the facts with their sources**" into `seed` (`skills/spec-brief/SKILL.md:82`) and `skills/grilling/SKILL.md:78` says "Facts, with their source paths, are carried into the hand-off" — so on the `/spec-brief` path the third section is precisely the one that can be non-empty.

Two more sites read as general claims but are accurate for their own caller, so they need only a per-path qualifier, not a correction: D6's "three empty sections" (2f-i seeds findings, never facts) and Design 7's grill-me blockquote "its header's reason line and empty sections are the answer" (`/grill-me` seeds a topic). The grill-me one is the only one that ships into a file.

Not P0 despite the literal "spec is internally inconsistent" trigger: nothing ships from D4, no checklist row reads it, Design 3's blockquote is the normative text an implementer writes, and row 6 asserts the `:106` paragraph independently. Calibrated to the round-2 precedent for the identical shape.
**Suggested fix:** D4, two words: "It goes through the hand-off block with its Settled and Open frontier sections empty; the header's reason line stays." D6: "…and three empty sections — on the 2f-i path, which seeds findings and no facts". Design 7's blockquote: "its header's reason line and empty sections are the answer" → "…its header's reason line is the answer" (a `/grill-me` seed carries no facts, so nothing is lost and the shipped text stops asserting a general rule).

### F-3: `## Deferred (P2+)`'s preamble is stale after round 2

**Severity:** P4
**Where:** spec.md:576
**Convention violated:** D12's bookkeeping contract — the Deferred section plus its preamble is the operator's record of what was folded versus fenced, read at the Phase 3 halt.
**Evidence:** "Not folded, each with the reason. Every other **round-1** P2+ finding was folded." All eight round-2 P2/P3/P4 findings were also folded and none deferred, but the sentence still scopes the claim to round 1, so the section under-reports what it accounts for. The five listed items are all round-1 ids.
**Suggested fix:** "Every other round-1 and round-2 P2+ finding was folded."

## Notes (no finding)

Recorded so round 4 need not re-derive:

- **Three round-2 folds I checked against the roll-up and judged *not* to need a bullet.** (a) The `:151` edit — declared at three points of use (§ Scope table row, § Files to leave alone spec.md:39–40, Design 3) and asserted by rows 6 and 9; it is a consistency edit keeping one file saying one thing about `stop`, not a construct. (b) "the lists report what the grill touched, not the full red list" — a clarification of existing list semantics, adding no sixth step-5 clause, which is the fence brief decision 12 names. (c) The additive `:108` clause producing `blocked-on: F<n>` — roll-up bullet 2 already covers that reason value, and v1's `:108` already carried the `:63` exception this restores. Do not over-fold these.
- **D7's supersession accounting now verifies.** Read `docs/specs/DONE/VHS-32/spec.md:458` (row 4), `:460` (row 6), `:461` (row 7). Row 5 here covers every row-4 string; row 10 covers row 7's nine strings plus the scalability line and is a superset of row 6. VHS-32 row 4 does **not** pin `:151`'s text, so Design 3's new `:151` edit breaks nothing. VHS-32 rows 5, 8, 9 are preserved by construction (rows 9, 11, 13's no-hunk fences), so they need no supersession.
- **All anchors re-verified at `7403cb5`.** `grilling` `:18`, `:48`, `:57`(+`:58` blank, `:59` heading — Design 4's insertion point is clean), `:63`, `:74`, `:78`, `:85`, `:88`, `:104`, `:106`, `:108`, `:110`, `:118–130`, `:132`, `:134`, `:151`; `spec-cycle` `:366`, `:453`, `:495–496`, `:504`, `:539`, `:548–549`, `:556–561`, `:698–703`; `spec-brief` `:80`, `:82`, `:88`, `:139`, `:140`, `:143`, `:159`; `grill-me` `:14`, `:20–21`; `docs/spec-workflow-reference.md` `:23`, `:35`. All correct.
- **Row 7's arithmetic re-verified by measurement**, not by reading: `grep -c 'ref:' skills/grilling/SKILL.md` = 0; longest line 649 chars, so the file is genuinely unwrapped and `grep -c` counts paragraph-sites.
- **`fact not established` still has no caller.** Re-ran the grep: outside `docs/specs/` only `grilling:74`, `:88`, `:125` plus one session-handoff file. Dropping it from the Q-item reason list remains the correct delete-cleanly call.
- **Still no premature abstraction, no duplication, no backwards-compat cruft.** `ref:` is a field on existing lines; `blocked-on: F<n>` reuses `blocked-on: Q<m>`; the lens-qualified id reuses `spec-cycle:366`/`:504`; Design 6's F-item Risks text reuses `spec-brief:80`'s shape. The omit-`ref:`-entirely rule is brief decision 1, not a compat shim.
- **Portability conventions hold.** No added line in `grilling`, `grill-me`, or `spec-brief` matches `\b(Explore|Agent|Skill|general-purpose)\b` or `model:`; Design 4's new paragraph names no harness mechanism. Consistent with `docs/authoring-portable-skills.md` § "Lead with intent" and the ASD-STE100 rule's prose posture.
- **Wiki decisions scanned.** Only `2026-09-06-vhs-32-…` overlaps and is now named. `2026-08-09-review-round-artifacts-are-immutable` is honored — no round-1 or round-2 report was edited; closure is recorded forward. `2026-06-16-vhs-15-optional-scalability-lens` is satisfied by the brief's `**Factor:** no` and D13.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 0 | P4: 1

STATUS: GREEN
