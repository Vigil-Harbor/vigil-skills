# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Grounding notes

- Spec read fresh from `docs/specs/TODO/VHS-33.spec.md`; brief from `.../VHS-33.brief.md`; `CLAUDE.md` read.
- Plane ticket VHS-33 retrieved from shared memory (namespace `skills`, record `e96bd119-9e11-44a8-8fe0-08b2f297fc4b`, 6 chunks). No conflict with the brief; the ticket has no Done-when section, as the brief states.
- All `path:line` anchors in the Scope table verified against HEAD `7403cb5`: `skills/grilling/SKILL.md` `:14–23`, `:33–57`, `:68–78`, `:102–112`, `:114–134`, `:136–138`, `:146–151` — all correct. `skills/spec-cycle/SKILL.md` `:491–509`, `:518–537`, `:539–546`, `:548–554`, `:698–708` — all correct. `skills/spec-brief/SKILL.md` `:84–90`, `:134–143`, `:139`, `:141` — all correct. `skills/grill-me/SKILL.md` `:18–21` — correct. `docs/spec-workflow-reference.md` `:23`, `:33`, `:35` — correct. In-design anchors `:74`, `:76`, `:88`, `:108`, `:52–55` — all correct. `docs/specs/DONE/VHS-32/spec.md:458` is indeed checklist row 4.
- Checklist claims independently verified: `python lint.py --strict` → exit 0, 0 errors, exactly 2 `missing-requires` WARNs (`review-pr`, `ship-spec`); `grep -c 'model:'` → 0 in all three files; `grep -c 'options 1–3' skills/spec-cycle/SKILL.md` → 4; `grep -c 'total_p0p1 == 0'` → 2. `AGENTS.md`/`README.md` carry no paraphrase of the hand-off block or the exit tokens, so "leave alone" is justified.

## Findings

### F-1: Design 4 defines `empty-frontier` two incompatible ways in the same section
**Severity:** P0
**Where:** spec § Design 4 (`:229–237`), § Design 7 (`:340`), § Design 8 (`:366–368`), Test plan row 7 (`:407–410`)
**Claim:** Bullet 1: "`empty-frontier` means **only** \"tree fully visited\", and stays reachable only after at least one round was rendered." Bullet 3: "A **later** round whose remaining candidates all fall below the fence is `empty-frontier` (at least one round was rendered), not `fence-empty`."
**Why this is wrong:** These two sentences cannot both be encoded. A later round whose remaining candidates all fall below the altitude fence did *not* fully visit the tree — candidates remain, unasked. Under bullet 3 that exit renders `exit: empty-frontier` with the header reason `no candidate decision met the altitude fence` (the reason enumeration the spec says at `:246` is "unchanged", and which exists at `skills/grilling/SKILL.md:119` and `:106` today). So `empty-frontier` does *not* mean only "tree fully visited". The contradiction is not incidental — Test plan row 7 pins both sentences as things the skill must state verbatim, so an implementer following the spec writes a self-contradicting contract into `skills/grilling/SKILL.md § Termination`.

It cascades to two other sections that are wrong for the same reason:
- Design 7 (`:340`): "the exit token in the final `## References` bullet records which of the two it was." Under bullet 3 it does not — `empty-frontier` still covers both "fully visited" and "later round, all remaining below the fence".
- Design 8 (`:366–367`): `docs/spec-workflow-reference.md:23` currently reads "An emptied frontier means the tree was fully visited (or nothing met the altitude fence)". The spec says `:23` "gains the sixth exit and its boundary with `empty-frontier`", but the boundary it must record is undefined until bullet 1 vs bullet 3 is resolved.

**Suggested fix:** Delete bullet 1's "means **only** \"tree fully visited\"" and replace with the actual boundary, e.g.: "`empty-frontier` stays reachable only after at least one round was rendered, and keeps both reason lines — `tree fully visited` and `no candidate decision met the altitude fence`. What changes is that the round-1 fence case, which `:106` currently routes to `empty-frontier`, now exits `fence-empty`." Then correct Design 7's "records which of the two it was" and state the same boundary for the `:23` edit. Update Test plan row 7 to match.

### F-2: Test-plan row 2 adds `skills/spec-cycle/SKILL.md` to a grep it cannot pass, and row 10 forbids the fix
**Severity:** P1
**Where:** spec Test plan row 2 (`:384–387`), row 10 (`:425–428`)
**Claim:** "`grep -nE '\b(Explore|Agent|Skill|general-purpose)\b' … skills/spec-cycle/SKILL.md` → every hit is inside a parenthetical carrying \"or the equivalent\", or under a `## Tool-use notes` heading, or is the prohibition itself".
**Why this is wrong:** VHS-32's row 2 (`docs/specs/DONE/VHS-32/spec.md:456`) deliberately covered only the three primitive files. VHS-33 adds `skills/spec-cycle/SKILL.md`, which has 8 hits, and 6 of them satisfy none of the three exemptions — they are bare harness-tool calls in § 2b, not in a parenthetical and not under `## Tool-use notes` (that heading starts at `skills/spec-cycle/SKILL.md:646`):

```
327: Single message, the reviewer Agent tool calls (three, or four when scale is declared) …
330: Agent(subagent_type="spec-reviewer-correctness", prompt=<context>)
331: Agent(subagent_type="spec-reviewer-edge-cases",  prompt=<context>)
332: Agent(subagent_type="spec-reviewer-conventions", prompt=<context>)
338: Agent(subagent_type="spec-reviewer-scalability", prompt=<context>)
341: When `scale_lens != on`, no fourth `Agent` call is emitted …
```

The row is the `/ship-spec` gate (§ Test command: "the review checklist above is the gate"), so it fails as written. And the only way to make it pass is to edit § 2b — which Test plan row 10 explicitly forbids ("no hunk in 2a–2e"). The two rows are mutually unsatisfiable.
**Suggested fix:** Either drop `skills/spec-cycle/SKILL.md` from row 2's file list (restoring the VHS-32 scope), or restrict the row's assertion to changed lines only: "no *new* bare harness-tool call is introduced; `git diff` adds no `Agent(` or `Skill(` line."

### F-3: Design 2's F-item template enumerates "exactly two" reason values but Design 3 requires a third string
**Severity:** P1
**Where:** spec § Design 2 (`:170–175`) vs § Design 3 (`:201–204`), § Design 7 (`:348–350`), Test plan rows 4 and 6
**Claim:** Design 2 gives the literal template

```
2. **F<n> — <fact needed>** — unresolved because: <fact not established | stopped>.
```

and states "The reason vocabulary is exactly two values, and both are reachable today". Design 3 then requires the Open F-item to render `unresolved because: fact not established (operator claim, unverified)`, and Test plan row 6 asserts the skill must contain that qualifier verbatim.
**Why this is wrong:** The code block presents the enumeration as exhaustive, and implementers follow code blocks. Copied into `skills/grilling/SKILL.md § Hand-off contract` as written, the contract has no legal rendering for D5's case — the decision the brief carries forward at brief-decision 5 and the spec restates at `:75–80` and `:495`. Downstream, `/spec-brief` Phase 4 (Design 7, `:348–350`) is told to detect "the `(operator claim, unverified)` qualifier, when present" in an item shape whose declared grammar excludes it.
**Suggested fix:** Make the template show the optional qualifier and drop "exactly two values", e.g. `unresolved because: <fact not established [(operator claim, unverified)] | stopped>.`, and state in one sentence that the parenthetical is an optional qualifier on `fact not established`, never a separate value.

### F-4: `ref:` has no slot on the F-item and no defined position on the rolled-up deferred item
**Severity:** P1
**Where:** spec § Design 1 (`:155–163`) vs § Design 2 (`:170–172`); § Design 1 (`:148–150`) vs `skills/grilling/SKILL.md:126`
**Claim:** Design 1: "the caller supplied ids: **every** Settled and Open item carries a `ref:` field … `ref:` is the last field on the item line, after `Facts relied on:` on a Settled item and after `unresolved because:` on an Open one." D1 (`:53–55`) and Done when 1 (`:466–468`) both say the rule covers "the rolled-up deferred item".
**Why this is wrong:** Two of the three Open item shapes have no place to put it.
1. Design 2's F-item template ends at `unresolved because: <…>.` with no `ref:` slot. An F-item is an Open item, so Design 1 says it must carry one (`ref: none` in the usual case, per D2). The two sections disagree about the same line of output.
2. The rolled-up deferred item is `**<parent title> — downstream decisions not explored (deferred at round <n>)**` (`skills/grilling/SKILL.md:126`). It has no `unresolved because:` field, so "after `unresolved because:`" does not locate anything — yet this is precisely the case D1 exists for (`:149–150`) and the one the brief's problem 1 calls out as unmappable by title.

Test plan row 4 compounds this by asserting only "the `ref:` field on the Settled item line and on the Open question line" — the two shapes Design 1 does cover — so the gate would pass with the two gaps still open.
**Suggested fix:** Show `ref:` explicitly in all three rendered shapes in Design 2 (and in the hand-off block the spec prescribes), and restate the placement rule as "`ref:` is the last field on the item line" without predicating it on `unresolved because:`. Extend Test plan row 4 to assert the F-item line and the rolled-up deferred line each carry the field.

### F-5: A seeded finding the grill never renders falls out of all four 2f-i id-sets and is reported nowhere
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 6 step 5 (`:294–322`), § Design 6 failure-modes bullet (`:329–332`)
**Claim:** "The four id-sets are built from `ref:` fields, not titles … The four sets are disjoint after this rule."
**Why this is wrong:** All four sets are now derived from `ref:` values on *returned* items. A seeded finding that the interview never rendered — it fell below the altitude fence (`skills/spec-cycle/SKILL.md:512–513`) — produces no item, therefore no `ref:`, therefore appears in none of the four sets and in no new clause. The new `; unreferenced decisions applied: <n>` clause counts the opposite case (decisions with no findings), not findings with no decision. On a `fence-empty` exit this is not an edge case: *every* seeded finding is in it, and step 5's line renders four empty id lists. The spec's own failure-modes bullet (`:329–332`) describes the fence-empty outcome but never says what step 5 prints. Since D1's whole purpose is to make the finding→disposition mapping deterministic rather than silent, leaving one class of finding silently unreported is exactly the hole the ticket is closing.
**Suggested fix:** Add a fifth trailing clause and rule to Design 6 step 5, e.g. `; not reached <ids>` — every seed id absent from every returned `ref:` — stated as staying P0/P1, and say that on `fence-empty` that clause carries the whole seed. Add a checklist assertion for the clause in Test plan row 9.

### F-6: The VHS-32 checklist row 4 "supersedes" claim mischaracterizes that row and drops live regression coverage
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D9 (`:102–107`), Test plan row 4 (`:389–397`)
**Claim:** "**This row supersedes VHS-32 checklist row 4** (`docs/specs/DONE/VHS-32/spec.md:458`), which asserts the v1 block".
**Why this is wrong:** `docs/specs/DONE/VHS-32/spec.md:458` does not assert the v1 hand-off *item lines* at all. It reads, in full: the 1.0 guard sentence; the D2 sentence including "make no mutations of any kind"; the fork block; the "advisory, never a default that carries by silence" sentence; the bounds with defaults 3 / 7 / brief altitude and the shared fact-request cap; the S4 table; "the hand-off block with `### Settled` / `### Open frontier` / `### Facts established`"; the `empty-seed` exit; the 1.1 resume contract including the single post-cap round and the `revised-after-cap (+1 round)` exit. Every one of those survives v2 unchanged — the spec's own § Out of scope (`:487–489`) says the bounds, fork form and advisory rule do not change. So nothing in row 4 is invalidated, and superseding it retires eight still-valid assertions in exchange for one narrower row that only covers the block. VHS-33's checklist has no replacement for them and, unlike Test plan row 10 for `spec-cycle`, no "no hunk outside these sections" row for `skills/grilling/SKILL.md` — the file with the most edits.
**Suggested fix:** Reword D9 and row 4 to "extends", not "supersedes" (VHS-32 row 4 remains true after this change), and add a row asserting the out-of-scope invariants survive in `skills/grilling/SKILL.md`: the fork block, the advisory sentence, the three bounds with defaults 3 / 7, the resume contract and `revised-after-cap (+1 round)`, and the `empty-seed` exit.

### F-7: "The existing empty-Settled rule already covers what a fence-empty summary produces" is over-broad
**Severity:** P2
**Where:** spec § Design 7 (`:342–344`)
**Claim:** "The existing empty-Settled rule (`:139`) already covers what a fence-empty summary produces … Nothing new is needed there."
**Why this is wrong:** A `fence-empty` summary has *all three* sections empty (spec `:239–240`), not just Settled. `skills/spec-brief/SKILL.md:139` covers only the empty-Settled case; `:140` (Open frontier → `## Risks / decisions`) and `:142` (Facts → `## References`) have no empty rule, so Phase 4 emits a brief with an empty `## Risks / decisions` and an empty `## Scope` under a mandatory-section template (`:111`, `:119–127`). Worse, the warning text `:139` mandates — "the brief pins everything to the spec author" — is false in this case: nothing is pinned to the spec author, because the Risks section is empty too. `/spec-cycle`'s brief parser keys on three of those headers, so an empty-everything brief is the hollow-authority artifact `:88` was written to prevent.
**Suggested fix:** Either state an empty-Risks rendering rule for the `fence-empty` path in Design 7, or state explicitly that a `fence-empty` brief is written with `_(none)_` in Risks plus a distinct warning naming the fence, and say why that is not the `empty-seed` halt.

### F-8: Design 3 changes what an `F1 <answer>` means, but the operator-facing line that describes it is pinned byte-identical
**Severity:** P3
**Where:** spec § Design 3 (`:192–196`), § Design 5 (`:270–271`), Test plan row 8 (`:415`)
**Claim:** Test plan row 8: "The round-end literal lines (`:52–55` pre-edit) are byte-identical." Design 5: the plain-language rule "does not touch the round-end literal lines".
**Why this is wrong:** `skills/grilling/SKILL.md:53` tells the operator: "a fact request by number and the fact (e.g. `F1 <answer>`)". After Design 3 the answer is no longer "the fact" — it is a claim the primitive verifies and may refuse to establish. The one line the operator reads every round now describes the old contract. This is not a blocker (the input syntax is unchanged), but it is a deliberate no-op sitting directly against D11/D12's plain-language goal, and the spec should say it chose it rather than leave it implicit.
**Suggested fix:** One sentence in Design 3 or Design 5 recording the decision — either "the round-end line is left alone; the claim/fact distinction is the primitive's business, not the operator's", or a one-word edit (`the fact` → `what you know`) with row 8 narrowed to line `:54`.

### F-9: § Bounds `:88` and § Fact-finding `:74` still describe the unresolved fact as reaching the hand-off under the old Q-item vocabulary
**Severity:** P3
**Where:** spec § Design 2 (`:176–179`), Scope table (`:28`)
**Claim:** Design 2 cites `skills/grilling/SKILL.md:88` and `:74` as the sources of the F-item's reason set and narrows the Q-item set to remove `fact not established`.
**Why this is wrong:** `:74` reads "if the interview ends first they reach the hand-off as Open with `unresolved because: fact not established`" and `:88` reads "A fact request the operator leaves unanswered twice becomes an Open item (`fact not established`)". After Design 2 those Open items must render in the new `F<n>` form, but neither sentence points at it, and the Scope table lists neither § Bounds (`:80–100`) nor those Fact-finding lines as touched — Fact-finding's listed change is only "operator answers are claims to verify". A reader arriving at `:88` after the change has no signal that the shape moved.
**Suggested fix:** Add § Bounds `:88` and § Fact-finding `:74` to the Scope table with a one-clause change ("names the `F<n>` Open form"), or state in Design 2 that both sentences gain a pointer to the new form. Note the § Out-of-scope fence at `:487–489` covers "the three bounds" themselves, not this cross-reference.

### F-10: `docs/spec-workflow-reference.md:23` is not part of "the grilling-contract paraphrase"
**Severity:** P4
**Where:** spec Scope table (`:32`)
**Claim:** "`docs/spec-workflow-reference.md` | The grilling-contract paraphrase (`:23`, `:33`, `:35`)".
**Why this is wrong:** `### The grilling contract` starts at `docs/spec-workflow-reference.md:25`. Line `:23` ("**Termination shapes and where each lands.**") is inside the `/spec-brief` skill section above it, describing where each exit lands in the *brief*. `:33` and `:35` are inside the contract subsection. Harmless, but the anchor grouping mislabels one of the three.
**Suggested fix:** Split the cell: "`/spec-brief`'s termination-shapes paragraph (`:23`) and the grilling-contract paraphrase (`:33`, `:35`)".

### F-11: The entire touched surface landed one commit ago
**Severity:** P4
**Where:** grounding step 6
**Claim:** Spec header: "Anchors verified against: vigil-skills `7403cb5`, 2026-09-06."
**Why this matters:** `git log` over the five Scope files returns exactly one commit — `d381f88`, merged 2026-09-06, the same day the brief and spec were written. Every anchor in the spec is correct at HEAD, so there is no drift today, but the surface is one day old and has never been exercised by a real `/spec-cycle` 2f-i run. No action needed; recorded because the grounding step requires it.
**Suggested fix:** None.

## Summary
P0: 1 | P1: 3 | P2: 3 | P3: 2 | P4: 2

STATUS: RED P0=1 P1=3 P2=3 P3=2 P4=2
