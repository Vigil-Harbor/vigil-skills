# Correctness Review — round 3

Grounding: read `docs/specs/TODO/VHS-33.spec.md`, `docs/specs/TODO/VHS-33.brief.md`, `CLAUDE.md`, all three round-2 reports, and every anchored file. Plane ticket VHS-33 retrieved from namespace `skills` (tag_exact, confidence 1.00) — its description matches the brief; it has no Done-when section, as the brief states. `git log -10` on the five touched files: the sole recent commit is `d381f88` (2026-09-06, today), already recorded in § Deferred as correctness R1 F-11; all anchors re-verified against the working tree at that commit.

**Anchor sweep (all verified, no stale anchors):** `skills/grilling/SKILL.md` `:12`, `:18`, `:23`, `:31`, `:37–44`, `:48`, `:57`, `:59–66`, `:61`, `:68–79`, `:70`, `:72`, `:74`, `:76`, `:80–100`, `:84–86`, `:88`, `:94–98`, `:104`, `:106`, `:108`, `:110`, `:118–130`, `:129`, `:132`, `:134`, `:136–150`, `:151` — all correct. `skills/spec-cycle/SKILL.md` `:366`, `:426–465`, `:453`, `:466–487`, `:489–561`, `:495–496`, `:504`, `:518–528`, `:539–546`, `:548–549`, `:556–561`, `:563–595`, `:698–703` — all correct. `skills/spec-brief/SKILL.md` `:80`, `:88`, `:105`, `:134–143`, `:139`, `:140`, `:143`, `:159`; `skills/grill-me/SKILL.md` `:14`, `:21`; `docs/spec-workflow-reference.md` `:23`, `:35`; `docs/specs/DONE/VHS-32/spec.md:458` (row 4) plus its rows 6/7 at `:460–461`; wiki `decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` § 5 — all correct.

**Gate-row satisfiability walk (the operator's specific ask).** I re-derived every checklist row against the text the Designs actually pin:

- Row 7 `grep -c 'ref:' skills/grilling/SKILL.md ≥ 7` — `grep -n "ref:" skills/grilling/SKILL.md` returns **zero** lines today, and the Designs produce exactly 7 matching lines (seed bullet `:18`; the `ref:` paragraph; four block lines; the callers-map sentence). The file is unwrapped, one paragraph per line — confirmed by inspection. **Satisfiable.**
- Row 6 `grep -c 'fence-empty' ≥ 3` — exactly 3 lines (`:104`, the `:106` paragraph, the block header). **Satisfiable.**
- Row 16 (VHS-36 fence) — I checked every added/modified line the spec pins in `grilling` and `spec-brief` against `operator claim|verif|qualifier|source: operator`. Zero hits, including the whole-line rewrites of `grilling:18`, `spec-brief:140`, and `spec-brief:143` (a modified line contributes its *entire* new text to `grep '^+'`). The round-2 P0 is genuinely gone. **Satisfiable.**
- Row 9 (`:136–150` fence, narrowed from `:136–151`) — Design 3 now edits `:151`, which sits outside the fence. Design 4's insertion lands between old `:58` and `:59`; under `-U0` git reports it at old-side position 57 or 58, both outside `:59–100`. **Satisfiable.**
- Row 4 — every string it pins appears verbatim in the Design 2 block. Row 5 covers every clause of VHS-32 row 4 (`DONE/VHS-32/spec.md:458`); row 10 covers every clause of VHS-32 rows 6 and 7 (`:460–461`). **Satisfiable.**
- Row 14 — the `docs/` fence is satisfiable: `## Test command` is `N/A` so `/ship-spec` writes no `test-output.txt` (`skills/ship-spec/SKILL.md:20`, `:241`), and it stages only files in the diff (`:135`), so the spec artifacts under `docs/specs/TODO/` are not touched by the implementation.

No self-contradictory gate row this round.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Row 7's `≥ 8` cannot pass | CLOSED | spec:443–445 now `≥ 7` with the seven matching lines enumerated; verified against a 0-baseline `grep -n 'ref:'` on the live file |
| correctness | F-2 (P1) | `ref:` descent rule has no F-item clause | CLOSED | spec:189–190 "a fact request from the question whose need raised it (or from the seed items directly when the need arose from the seed)"; row 7 (spec:442–443) asserts the phrase |
| correctness | F-3 (P2) | D5 cites `:555–560` | CLOSED | spec:119 and spec:561 both now `:556–561`; matches live `skills/spec-cycle/SKILL.md:556–561` |
| correctness | F-4 (P2) | `:151` left stale, row 9 fenced it | CLOSED | spec:274–277 edits `:151` in step with `:108`; row 9 (spec:450–453) narrowed to `:136–150`; Files-to-leave-alone (spec:39–40) restated |
| correctness | F-5 (P3) | D13's `question_cap` justification | CLOSED | spec:165–167 restated as the no-change claim, citing `:74` |
| edge-cases | F-1 (P0) | "qualifiers" inside the shipped `:140` | CLOSED | spec:355–358 blockquote ends at `spec author pins this`.`; the rationale moved to spec prose at spec:360–361; row-16 grep re-derived over every added line → 0 |
| edge-cases | F-2 (P1) | Row 7 `≥ 8` | CLOSED | same edit as correctness F-1 |
| edge-cases | F-3 (P1) | Four item kinds, three descent clauses | CLOSED | same edit as correctness F-2 |
| edge-cases | F-4 (P2) | `:151` says "questions" | CLOSED | same edit as correctness F-4 |
| edge-cases | F-5 (P2) | Seeded id in no list | CLOSED | spec:325–328 adds the sentence; row 10 (spec:459) asserts "not the full red list" |
| edge-cases | F-6 (P2) | `:143` keyed on token, not reason | CLOSED | spec:365–370 now keys on "When the header's reason is `no candidate decision met the altitude fence`" and gives both the `fence-empty` and `empty-frontier` renderings |
| edge-cases | F-7 (P2) | fence-empty empties Facts established | PARTIAL | spec:235–238 and spec:266–268 no longer force it empty ("rendered as on any exit"), which closes the harm; but the shipped reason clause "normally empty too, since no round was rendered and no dispatch ran" is inaccurate for `/spec-brief` — see F-3 below |
| edge-cases | F-8 (P3) | `:108` edit dropped the waiting question | CLOSED | spec:271–274 is additive: fact needs → `F<n>` `stopped`, waiting question → `blocked-on: F<n>`; row 6 (spec:435–437) asserts both |
| conventions | F-1 (P0) | Row 7 `≥ 8` vs line convention | CLOSED | same edit as correctness F-1 |
| conventions | F-2 (P2) | Roll-up incomplete | CLOSED | spec:79–85 adds the F-numbering and `rounds: 1/<round_cap>` bullets; D7 (spec:134–135) declares its supersessions bookkeeping, not constructs |
| conventions | F-3 (P2) | Wiki decision unnamed | CLOSED | D4 (spec:114–115) and Risk 2 (spec:540–545) name `2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write` § 5; § 5 verified in the wiki, including the "Rejected — a success token for an empty interview" clause |
| conventions | F-4 (P3) | Both-lists roll-up wording | CLOSED | spec:68–71 now carries the "(it may still appear under `deferred to option 3`)" clause |
| conventions | F-5 (P4) | D7 omits row 6 | CLOSED | spec:132–133 "supersede VHS-32 rows 4, 6 and 7" |

No REOPENED items. `scale_lens: off` and no `scalability.md` exists in `round-2/`, so the stale-report guard is a no-op.

## Findings

### F-1: Design 7's `docs/spec-workflow-reference.md:23` deletes the altitude-fence parenthetical from the emptied-frontier sentence, contradicting Design 3 and Design 6 in the same PR
**Severity:** P1
**Where:** spec § Design 7, `:383–391`, against § Design 3 `:262–265` and § Design 6 `:365–370`
**Claim:** The spec pins `:23` to become, verbatim:
> **Termination shapes and where each lands.** An emptied frontier means the tree was fully visited — the brief carries no open items. A fence-empty exit means nothing met the altitude fence in round 1 …

**Why this is wrong:** The live `docs/spec-workflow-reference.md:23` reads today:

> An emptied frontier means the tree was fully visited **(or nothing met the altitude fence)** — the brief carries no open items.

The replacement drops that parenthetical, but the same PR ships two files that assert the opposite. Design 3's `:106` blockquote (spec:262–265) says `empty-frontier`'s reason line "distinguishes `tree fully visited` from `no candidate decision met the altitude fence` (**a later round's remaining candidates all fell below the fence**)". Design 6's `:143` (spec:369–370) spells the same case out explicitly: `Interview: 2 rounds, exit empty-frontier (no candidate decision met the altitude fence)` "for a later-round fence-out". So after this PR, `grilling:106` and `spec-brief:143` say an emptied frontier may mean a whole subtree fell below altitude, while `spec-workflow-reference:23` says it means the tree was fully visited.

This is a regression, not a neutral rewrite: the parenthetical is exactly the half of edge-cases R4 F-1 that VHS-32 already folded (brief `## Problem` item 3, "VHS-32 folded half of this finding: the 1.8 header's reason line now distinguishes 'tree fully visited' from 'no candidate decision met the altitude fence'"), and this ticket exists to land the other half. Deleting it re-introduces the ambiguity in the one document a reader consults for the paraphrase. It also removes the only place the round-≥2 fence-out is described, since the new second sentence scopes the fence explanation to `fence-empty` / round 1 only. Nothing in the spec offers a rationale for the deletion, and row 13 (spec:472–474) does not assert the parenthetical, so the loss is gate-invisible.

**Suggested fix:** Keep the clause when rewriting `:23` — one word longer than the current pin:

> **Termination shapes and where each lands.** An emptied frontier means the tree was fully visited, or that a later round's remaining candidates all fell below the altitude fence — either way the reason line says which. A fence-empty exit means nothing met the altitude fence in round 1 — the brief is written with no decisions and the reason recorded. A cap hit or an operator stop is a documented outcome, not a failure: the unresolved branches — questions and unestablished facts alike — go to `## Risks / decisions` for the spec author. An empty seed is the one shape that writes nothing at all.

Then extend row 13 to assert `:23` contains both `fence-empty` and `altitude fence` twice (or the phrase "either way the reason line says which"), so the distinction is gate-held.

---

### F-2: Design 1's "with no ids the block is byte-identical to v1" contradicts Design 2's own list of four changes to the block
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1, `:194–195`; echoed in § Design 2 `:220–221` ("so the v1 lines are the no-id rendering") and § Risks 1 `:531–533` ("`/spec-brief` and `/grill-me` supply none and see v1 lines")
**Claim:** "Descent is the primitive's own tree, not a title match. With no ids the block is byte-identical to v1, which is what `/spec-brief` and `/grill-me` receive."
**Why this is wrong:** Design 2 (spec:216–238) enumerates four changes to the block that are independent of `ref:` and therefore apply to a no-id caller too: the header's exit list gains `fence-empty`; the `**F<n> — <fact needed>**` Open form is new; the rolled-up line "gains a period before `ref:`"; and the Open question line's reason list gains `blocked-on: F<n>` and drops `fact not established`. A `/spec-brief` or `/grill-me` grill that ends with an unresolved fact now renders an F-item where v1 rendered a Q-item — the whole point of D3 — so the block a no-id caller receives is demonstrably *not* byte-identical to v1. The accurate statement is narrower: the Settled and Open-question **lines** are byte-identical to v1 for a no-id caller, because the `ref:` field is the only thing appended to them.

Nothing downstream breaks (no checklist row and no caller greps v1 byte-identity — the brief's F1 records that the only verbatim assertion was the archived `DONE/VHS-32/spec.md:458`, superseded here by row 5), so this is a wrong justification rather than a wrong instruction. But `/spec-brief` and `/grill-me` are exactly the callers whose exposure to the new shapes Design 6 and Design 7 have to cover, and "byte-identical" invites a reader to conclude they need no update at all.

**Suggested fix:** In Design 1, replace the sentence with: "With no ids, the Settled and Open-question lines are byte-identical to v1 — the `ref:` field is the only thing appended to them. The block as a whole still changes for every caller: the header gains `fence-empty`, the F-item form is new, and the rolled-up line gains a period (Design 2)." Trim Design 2's "so the v1 lines are the no-id rendering" to "so those two lines are unchanged for a no-id caller", and narrow Risk 1's "see v1 lines" the same way.

---

### F-3: The shipped `:106` clause "normally empty too, since no round was rendered and no dispatch ran" is wrong for `/spec-brief`, which always supplies grounding facts in `seed`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3, `:266–268` (the `:106` blockquote — shipped file text); echoed in § Design 2 `:235–238` and § Risks 2 `:536–537` ("normally no fact References")
**Claim:** "on `fence-empty` its Settled and Open frontier sections are empty, and `### Facts established` is rendered as on any exit — normally empty too, since no round was rendered and no dispatch ran."
**Why this is wrong:** The governing clause ("rendered as on any exit") is right and closes edge-cases R2 F-7's actual harm. The trailing *reason* is not. `skills/spec-brief/SKILL.md:82` assembles `seed` as "the problem statement, **the facts with their sources**, and any related open tickets", and `skills/grilling/SKILL.md:18` defines `seed` as "the problem statement **and any grounding facts already established**". `skills/grilling/SKILL.md:78` then says "Facts, with their source paths, are carried into the hand-off", with the retrieval-first sentence immediately after it covering exactly the seed-supplied case. So for the caller that reaches `fence-empty` most often, `### Facts established` is normally **non**-empty, and the brief's `## References` and `## Scope` rows are fed from it (`spec-brief:141–142`). The clause names only the two producers that happen to be absent (round rendering, dispatch) and silently drops the third that is present.

This matters because it is shipped text in the primitive's own termination section — a caller reading `:106` would conclude a `fence-empty` hand-off carries no facts, which is the reading edge-cases R2 F-7 flagged. Risk 2's "normally no fact References" inherits the same error.

**Suggested fix:** Drop the causal clause and state the rule, inside the text already being written: "…and `### Facts established` is rendered as on any exit — it carries whatever the seed supplied or a dispatch returned, which for a caller that grounds first is normally not empty." Change Risk 2's clause to "and whatever fact References the seed's grounding supplied". No new construct, no checklist-row change (row 6 asserts only `fence-empty`, the fence reason, and `rounds: 1/<round_cap>`).

---

### F-4: Design 5 does not say which of its step-5 text is added to `skills/spec-cycle/SKILL.md`, and the both-lists rule it declares as a spec-level addition has no checklist assertion
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 5, `:310–339`, against § Decisions roll-up `:68–71` and row 10 `:454–466`
**Claim:** "**Step 5** (`:548–549`): the line becomes ```…``` built as follows (this is the brief's Risk 1 pin): …" followed by six bullets.
**Why this is wrong:** Every other Design in this spec marks shipped text unambiguously — Design 1, 3, 4, 6 and 7 all use "`:NNN` becomes:" plus a blockquote, and Design 5's own steps 1 and 4 quote the replacement strings inline. Step 5 alone gives a code block plus six unmarked bullets, with no statement of whether the bullets go into the file or stay in the spec. The answer is only recoverable indirectly: row 10 (spec:459) requires step 5 to contain "not the full red list", a phrase that appears solely in the `left open` bullet — so the bullets must ship. An implementer who reads the bullets as spec-side exposition would ship the one-line format string and nothing else, and 2f-i would then contain no rule for building any of the four lists.

The gate gap compounds it. The both-lists rule is one of only seven items in the § Decisions "Spec-level additions" roll-up (spec:68–71), declared there precisely so Phase 3's drift-check can find it — but row 10 asserts only `grill applied (exit: <token>):`, `unreferenced decisions applied: <n>`, and "not the full red list". The both-lists rule, the seed-order dedup, and the `fence-empty` list-emptying rule can all silently fail to ship without any row noticing, while the brief's Risk 1 ("What the 2f-i step 5 line prints when one Settled decision carries several `ref:` ids … — spec author pins this") requires the *skill* to carry them, since 2f-i is a prompt and has no behavior its own text does not state.

**Suggested fix:** One sentence in Design 5 before the bullets: "The code block replaces `:548–549`; the bullets below are added to step 5 in the file, immediately after it." Then add one clause to row 10: step 5 also contains "is listed here rather than under `dispositioned`" and "in seed order". Both strings are already in the pinned text; no new construct.

---

### F-5: Row 10's `grep -c 'total_p0p1 == 0'` names no file
**Severity:** P4
**Where:** spec § Test plan, row 10, `:456`
**Claim:** "`grep -c 'total_p0p1 == 0'` unchanged"
**Why this is wrong:** The row's other clauses all name `skills/spec-cycle/SKILL.md` explicitly; this one is bare, so as literally written it is `grep` with no path and reads stdin. It is inherited verbatim from `DONE/VHS-32/spec.md:460`, which had the same gap, and the intent is unambiguous from context.
**Suggested fix:** `grep -c 'total_p0p1 == 0' skills/spec-cycle/SKILL.md` unchanged.

## Summary
P0: 0 | P1: 1 | P2: 3 | P3: 0 | P4: 1

STATUS: RED P0=0 P1=1 P2=3 P3=0 P4=1
