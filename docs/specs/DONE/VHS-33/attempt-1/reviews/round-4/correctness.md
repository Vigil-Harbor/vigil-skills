# Correctness Review — round 4

Grounding: all five touched files read at HEAD (`7403cb5`), every cited anchor re-verified, the Plane ticket retrieved from the `skills` namespace (tag_exact, confidence 1.00), `lint.py --strict` run to verify checklist row 1, and all three round-3 reports read.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Post-cap rule amends `grilling:23`, unauthorized by Scope, forbidden by row 5, falsifies D9 | CLOSED | Rule removed. spec:482–492; Scope cell spec:28 lists `:23`/`:57` unchanged; row 8 spec:843–845 asserts byte-identical; Risks 7 spec:993–998; § Deferred spec:1055–1061. No dangling reference to the removed machinery. |
| correctness | F-2 | `:108` amended, duplicate `:151` left restating reversed rule | CLOSED | spec:347–354; Scope cell names all three bullets; row 4 spec:800–802. `:151` text matches the spec's quote exactly. |
| correctness | F-3 | Precedence chain does not place `fact not established`, ranks two illegal F-item values | CLOSED | Two chains at spec:308–318 with the "never render on an F-item" statement. (Residual reachability gap → new F-3.) |
| correctness | F-4 | Row 12 says "eight-section"; template declares nine headers | CLOSED | spec:883–885. Verified `spec-brief:113–128` declares nine `##` headers. |
| edge-cases | F-1 | Precedence chain has no entry for `fact not established` | CLOSED | Two per-shape chains spec:308–318; rule 3 now reads "on **every** exit, `stop` included" spec:444–447. |
| edge-cases | F-2 | Spec leaves `:151` restating the reversed rule | CLOSED | As correctness F-2. |
| edge-cases | F-3 | All-sections-empty rule misses `## Out of scope` | CLOSED | spec:694–701; Risks 6 spec:987–992. |
| edge-cases | F-4 | Post-cap round preserved but unspendable | CLOSED (by removal + deferral) | spec:482–492; § Deferred spec:1055–1061. Verified `spec-brief:105` does withdraw the option on *return*. |
| edge-cases | F-5 | "Dispatched once" is invocation-scoped | CLOSED | Rule 1 retitled spec:413; resume paragraph spec:431–437; row 7. Consistent with `grilling:23`. |
| edge-cases | F-6 | Demoted `deferred to option 3` item has no clause | CLOSED | `also settled (left open)` spec:616–622. |
| edge-cases | F-7 | Rolled-up narrowing fights conservative reporting | CLOSED (by removal) | spec:245–253; row 6 spec:817–819. No dangling reference. |
| edge-cases | F-8 | Phase 3 previews an empty Risks list | CLOSED | spec:678–683; row 12 spec:873–875. |
| edge-cases | F-9 | `revised-after-cap` has no precedence entry | CLOSED | spec:317–318. |
| edge-cases | F-10 | `:132` bound vs named overflow F-items | CLOSED | D13 spec:197–205; `:132` in the Scope cell. |
| conventions | F-1 | `## Failure modes` restates the same rules with no design | CLOSED | spec:355–362; row 7 spec:833–834. |
| conventions | F-2 | All-or-none report renders outside the block `:116` renders exactly | **PARTIAL** | Design 1 spec:231–239 relocates it to the header `reason:` field, but the **authoritative block at spec:280 was not updated**, Design 4 spec:501 still says "the reason enumeration is unchanged", and row 6 spec:816–817 still asserts the superseded placement → new F-1 and F-2. |
| conventions | F-3 | § Deferred blanket coverage claim is false | CLOSED | spec:1065–1069. |
| conventions | F-4 | Two spec-level additions missing from the roll-up | CLOSED | spec:84–86, :90–92, :64–65, :66–67, :71. |
| conventions | F-5 | Preamble's relation to `question_cap` unstated | CLOSED | spec:541–544, citing `:85` (verified). |
| conventions | F-6 | `:104`'s exit list not gated | CLOSED | Row 8 spec:841–842. Verified `:104` today names five exits. |

**Anchor re-verification at `7403cb5`:** every path:line in the spec checks out — `grilling` `:12`, `:14–23`, `:23`, `:33–57`, `:48`, `:52–55`, `:57`, `:59–66`, `:63`, `:68–78`, `:72`, `:74`, `:76`, `:80–100`, `:85`, `:88`, `:102–112`, `:104`, `:106`, `:108`, `:110`, `:114–134`, `:116`, `:119`, `:122`, `:125–126`, `:129`, `:132`, `:136–138`, `:146–151`, `:148`, `:149`, `:151`; `spec-cycle` `:431`, `:489–561`, `:499–505`, `:507–509`, `:518–528`, `:523`, `:539–546`, `:548–554`, `:636–640`, `:646`, `:698–708`, `:700–703`; `spec-brief` `:78`, `:80`, `:84–90`, `:92–107`, `:94`, `:105`, `:113–128`, `:134–143`, `:156–164`; `grill-me:14`, `:18–21`; `spec-workflow-reference.md:23`, `:33`, `:35`. Quoted text at `:74`, `:88`, `:108`, `:148`, `:149`, `:151` matches verbatim. Row 1 verified (`python lint.py --strict` → `0 error(s), 2 warning(s)`). Row 10's grep = 4, row 11's = 2. `git log -10` on the five files: only `d381f88` — already Risks 4.

## Findings

### F-1: The authoritative hand-off block omits the `partially identified seed` reason value that four other sections require
**Severity:** P0
**Where:** spec § Design 2, spec.md:280 (vs spec.md:28, :71, :231–233, :501, :820–821)
**Claim:** Design 2 opens "This is the authoritative rendering. **Everything the other designs change appears here in one place**" (spec.md:275–277), and the block's header line reads `… reason: tree fully visited | no candidate decision met the altitude fence | cap reached | operator stop | resume)`.
**Why this is wrong:** Four other sections state that the header's `reason:` field carries a sixth value this block does not list: the Scope table (spec.md:28), the Decisions roll-up (spec.md:71), Design 1 (spec.md:231–233), and checklist row 6 (spec.md:820–821). A fifth section contradicts all of them: Design 4 (spec.md:501) — "The header's exit enumeration gains `fence-empty`; **the reason enumeration is unchanged**."

An implementer copies the code block into `skills/grilling/SKILL.md:119` (the block is the deliverable — `:116` says "End by rendering exactly this block"), ships a header without the value, and then fails the spec's own checklist row 6 at the `/ship-spec` gate. A code block that disagrees with its surrounding prose is the load-bearing disagreement: implementers follow the block.

A second leg, unresolved by any section: **how the value composes with the real exit reason.** `reason:` today holds exactly one value. Design 1 requires the annotation "on every exit that renders the block", i.e. alongside `cap reached` / `operator stop`. Row 6's "the `reason:` enumeration includes …" reads as an *alternative* — which on a `stop` would replace `operator stop` and destroy the exit reason the header exists to carry. Neither separator nor precedence is stated.
**Suggested fix:** Render the reason field as two slots in Design 2's block — `reason: <…exit reason…>[; partially identified seed — ref: omitted]` — and add one sentence: the clause is appended after the exit reason, separated by `; `, on every exit that renders the block, and never replaces it. Change Design 4's "the reason enumeration is unchanged" clause, and align row 6 to assert the composed shape.

### F-2: Checklist row 6 still asserts the round-3 rendering that Design 1 now explicitly forbids
**Severity:** P0
**Where:** spec § Test plan, row 6, spec.md:815–817
**Claim:** "…and the report **on the first rendered line (round preamble, or immediately above the `## Grill summary` header when no round renders)**".
**Why this is wrong:** Design 1 spec.md:234–239 forbids exactly that placement, in terms, citing `grilling:116` ("End by rendering exactly this block in-conversation") and `spec-cycle:523` ("append the returned Grill summary verbatim") — both verified. Row 6 is the surviving round-3 text and is the artifact `/ship-spec` greps against, so as written the checklist would *require* the implementer to produce the very line conventions/F-2 was raised to remove.

Row 6's "when no round renders" case is also wrong on both of its possible exits: on `fence-empty` a block *is* rendered and Design 1 routes the report to the header's `reason:` field; on `empty-seed` there is no header at all (`grilling:110`) and Design 1 spec.md:239 routes it to that one-line reason.
**Suggested fix:** "…and the report in two places — the round-1 preamble where a round is rendered, and the hand-off header's `reason:` field on every exit that renders the block (`empty-seed` carries it on its one-line reason instead); the skill states that it is **not** rendered on a line above the `## Grill summary` header."

### F-3: The F-item precedence chain makes `stopped` unreachable on a literal reading, contradicting the `:108`/`:151` amendment
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2, spec.md:308–345
**Why this is wrong:** A precedence chain is applied by testing each value's applicability top-down. For an F-item abandoned mid-flight at a `stop`, `fact not established` is literally applicable — the fact was not established — so the higher entry wins and `stopped` can never render. The only thing preventing that reading is the prose gloss at spec.md:316–317 ("`stopped` is reserved for an F-item with no disposition of its own"), which narrows `fact not established` by definition rather than by rank. The Q-item chain has no such circularity, so the asymmetry is easy to miss — and spec.md:342–345 ships the opposite behaviour in the `:108`/`:151` amendment that row 4 pins.
**Suggested fix:** State the F-chain with the applicability condition inline: `fact not established[ (<qualifier>)] — where the fact request reached a terminal unestablished state (twice unanswered, dispatch-cap overflow, failed dispatch, no read-restricted agent class, or an operator claim) → stopped — an exploration abandoned mid-flight at a stop, nothing learned`. Mirror the qualification in row 4.

### F-4: The `fence-empty` brief's forced-empty `## Scope` silently overrides mapping rule `:141`, discarding Phase 1 grounding
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7, spec.md:694–701 (and § Design 4, spec.md:494–496)
**Why this is wrong:** `## Scope` is not fed only by the interview. `skills/spec-brief/SKILL.md:141`: "`## Scope` gets one row per path **the settled decisions and grounding facts** name: `Current` filled from a fact with its `path:line`…". Those grounding facts come from Phase 1 (`spec-brief:78–82`, which dispatches read-restricted explorations and prints `grounding: <n> files read, <m> explorations dispatched`) — they exist *before* the interview and survive an altitude fence untouched. Likewise `:142` routes Facts established → `## References`.

So on a `fence-empty` run the spec produces a brief that throws away every verified `path:line` Phase 1 obtained: no `## Scope` rows (Design 7's rule) and no fact bullets in `## References` (Design 4's empty `### Facts established`). That is precisely the material a spec author needs on the one path where the interview settled nothing. Design 7 is meticulous about declaring its supersession of `:139` but supersedes `:141` and `:142` silently.
**Suggested fix:** Narrow the rule to the sections the interview alone feeds: `_(none)_` under `## Decisions carried forward` and `## Out of scope`; `## Scope` is written from Phase 1's grounding facts as normal (a `Current` cell with an empty `Change`), and `## References` carries those facts per `:142`. If discarding them is intentional, say so and add the supersession of `:141`/`:142` to the roll-up.

### F-5: The Scope table promises a `## Failure modes` change no Design prescribes and no checklist row asserts
**Severity:** P3
**Where:** spec § Scope, spec.md:28
**Why this is wrong:** Design 2 prescribes the F-item shape for the *hand-off block* (`:114–134`) and prescribes exactly three `## Failure modes` edits (`:151`, `:148`, `:149`). Nothing in Designs 1–8 specifies a new `## Failure modes` bullet for the F-item shape, and row 4 asserts only the three amendments.
**Suggested fix:** Delete "the new F-item shape, plus" from that cell.

### F-6: Checklist row 5 lists a paraphrase among strings asserted "present verbatim"
**Severity:** P3
**Where:** spec § Test plan, row 5, spec.md:809
**Why this is wrong:** `grilling:61` reads "The recommendation is **advisory. It is never a default that carries by silence**" — two sentences. `grep -F 'advisory, never a default that carries by silence'` returns nothing today, so the row fails against the *unmodified* file it is meant to protect.
**Suggested fix:** Quote it as it stands — "It is never a default that carries by silence" — or move it to the row's descriptive list.

### F-7: `spec-cycle:495` cited for the 2f-i seed shape spans `:494–495`
**Severity:** P4
**Where:** spec § References, spec.md:1012
**Why this is wrong:** `spec-cycle:494–495` reads "…extract each remaining P0/P1 finding: **id, severity, title,** / **body.**" — the field list starts on `:494`.
**Suggested fix:** Cite `:494–495`.

## Summary
P0: 2 | P1: 0 | P2: 2 | P3: 2 | P4: 1

STATUS: RED P0=2 P1=0 P2=2 P3=2 P4=1
