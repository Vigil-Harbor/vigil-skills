# Edge-Cases Review — round 3

Grounding: spec, brief, `CLAUDE.md`, the three round-2 reports, and the five target files.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Precedence order contradicts stop-with-exploration sentence | CLOSED | spec:277–302; Scope table :28 lists `:108`. New defect in the *same* machinery → F-1 below |
| edge-cases | F-2 | Design 3 rule 1 reinstates the retry it displaces | CLOSED | spec:352–361; never-returns restated at :363–367 |
| edge-cases | F-3 | Different-fact branch allocates no `F<n>` | CLOSED | spec:343–345 |
| edge-cases | F-4 | Precedence demotion applies the edit, reports finding untouched | CLOSED | spec:492 seven-clause line; :531–537; :219–226 narrowing. Residual gaps → F-6, F-7 |
| edge-cases | F-5 | Missing-ref withhold governs step 4, written in step 5 | CLOSED | spec:479–486 |
| edge-cases | F-6 | `unreferenced decisions applied` covers one of four classes | CLOSED | spec:507–511 |
| edge-cases | F-7 | Zero-item resume burns the post-cap round | PARTIAL | spec:411–416 adds the rule, but no caller can spend the preserved round → F-4 |
| edge-cases | F-8 | Fence-empty summary reaches Phase 3's unusable revise option | PARTIAL | spec:585–591; preview body still unaddressed → F-8 |
| edge-cases | F-9 | Fence-empty brief's empty headers defeat drift-check fallback | DEFERRED (accepted) | spec:604–609, :912–919, Risks 6. Same class recurs at a third header → F-3 |
| edge-cases | F-10 | All-or-none violation has no reporting slot, no rendering | CLOSED | spec:206–217; :456–462 |
| edge-cases | F-11 | No path for a true but non-repo-checkable operator fact | DEFERRED (accepted) | spec:640–649; Risks 5; § Deferred :920–924 |
| edge-cases | F-12 | Completeness partitions using a set never in the seed | CLOSED | spec:520–524 |
| edge-cases | F-13 | `not reached` names one of four causes | CLOSED | spec:512–519 |
| edge-cases | F-14 | Legal-id bars `ref:`'s delimiter but not step 5's | CLOSED | spec:202–205; :498–500 |
| edge-cases | F-15 | Scope-row fence does not exclude a refuted claim's path | CLOSED | spec:624 |
| edge-cases | F-16 | Two sentinels compete for an empty Decisions section | CLOSED | spec:596–601 |
| edge-cases | F-17 | Row 2 cites row 10 for a row 11 assertion | CLOSED | spec:688 |
| correctness | F-1 | Three item shapes in four places, two in three | CLOSED | spec:28 / :620–629 / :775 |
| correctness | F-2 | Row 10 pins `options 1–3` at 4 | CLOSED | spec:571–573; verified `grep -c` = 4 |
| correctness | F-3 | Fence-empty line drops `not grillable` | CLOSED | spec:552, :555–561 |
| correctness | F-4 | `:139` collision and unrendered `## Scope` | CLOSED | spec:596–603. Third header still uncovered → F-3 |
| correctness | F-5 | `stop` exit erases the `(operator claim, …)` qualifier | **REOPENED** | spec:376 still resolves `stop` → `stopped`; the new chain :281 has no entry for `fact not established` and its stated principle yields the opposite → F-1 |
| correctness | F-6..F-9 | — | CLOSED | spec:76, :456–462, :905–911, :83–86 |
| conventions | F-1..F-4 | — | CLOSED | spec:65–67, :596–601, :905–929, :125–131 |

## Findings

### F-1: The new precedence chain has no entry for `fact not established`, and Design 3 rule 3 cites it for a ruling it cannot yield
**Severity:** P0
**Where:** spec § Design 2 (spec.md:268–302, chain at :281) vs § Design 3 rule 3 (spec.md:373–377)
**Edge case:** Any Open F-item at a `stop` or `round-cap` exit — reachable under the defaults on the path the spec itself calls "reachable in ordinary use".
**What happens:** The implementer has two reasons applying to one item and no ranking. Design 2 fixes the F-item's reason set at exactly two — `fact not established` or `stopped` — but the chain is `deferred → blocked-on: <unresolved Q<m> or F<n>> → stopped → round-cap`. `fact not established` is absent. `deferred` and `blocked-on:` can never apply to an F-item, so the chain is *inert* for exactly the item shape D3 was created to give a shape to. Rule 3 then resolves by assertion — "on a `stop` exit the reason is `stopped` **per the precedence order in Design 2**" — citing an order that does not contain the value it is displacing.

Worse, the same rule resolves the two exits opposite ways. Rule 3's own sentence says the claim "reaches the hand-off as an Open F-item with `fact not established (operator claim, unverified)`" — the causal reason winning, as at `round-cap`. On `stop` the exit reason wins. Identical item, two orderings.

The concrete loss is round-2 correctness F-5's, unchanged: on `stop` the F-item renders bare `stopped`, the qualifier can only attach to `fact not established`, so `/spec-brief` Phase 4 finds no qualifier and the brief loses "a human already asserted an answer, and it was never checked".
**Why the spec misses it:** The round-2 fix promoted the ordering to a principled rule — "the header already records *how the interview ended* … What the caller cannot recover from the header is *what this particular item was waiting on*". Applied to an F-item, `stopped` is precisely what the header already says and `fact not established (operator claim, unverified)` is precisely what the item was waiting on. **The new principle argues against rule 3's ruling.** The chain still sits directly under "**The Q-item reason set narrows**" and was never re-derived for the F-item set the same design introduces. Row 4 pins the chain and row 7 pins rule 3 separately, so the gate asserts both halves of the contradiction without comparing them.
**Suggested fix:** State the F-item ranking in Design 2's F-item paragraph, consistent with the stated principle: `fact not established[ (qualifier)]` outranks both exit reasons, so an unresolved fact renders its causal reason on every exit, and `stopped` is reserved for an F-item with no other disposition. Amend rule 3's last clause to match; extend row 4 to assert the chain covers the F-item value set. If instead the exit reason is intended to win, say so as a stated exception with its loss recorded — and then `stopped` must carry the qualifier.

---

### F-2: The spec amends `:108` but leaves `skills/grilling/SKILL.md:151` restating the rule it just reversed
**Severity:** P1
**Where:** spec § Design 2 (spec.md:296–302), Scope table (spec.md:28), row 4 (spec.md:690–700) vs `grilling/SKILL.md:151` and `:148`
**What happens:** The shipped file contradicts itself. `:108` becomes "the F-item renders `stopped`, the question it blocked renders `blocked-on: F<n>`". `:151` still reads verbatim: "- **`stop` with explorations in flight** — abandon them; their questions are Open with `unresolved because: stopped`." A `## Failure modes` bullet is a summary a reader trusts; the one that survives says the questions render `stopped`.

Same shape one bullet up: `:148` restates `grilling:76`'s retry, which Design 3 rule 1 now displaces for verification dispatches.
**Why the spec misses it:** The Scope table lists `## Failure modes (:146–151)` only for "the new prohibitions and shapes". Design 2 tracks `:108` because § References catalogues it, but `:151` is catalogued only as a range. Row 4 asserts "the amended `:108` behaviour"; nothing reads `:151`. `git diff` review would show a hunk at `:108`, none at `:151`, and nothing flagging that as wrong.
**Suggested fix:** Name `:151` and `:148` in the Scope cell and in Design 2's `:108` paragraph. Extend row 4 to assert `:151` carries the same split, row 7 to assert `:148`'s carve-out. Then sweep § References' catalogued ranges for any other rule stated twice in the same file — `:74`/`:88` are already handled by Design 2's Cross-references paragraph; that is the pattern.

---

### F-3: The all-sections-empty rule covers two empty brief sections and misses a third that `/spec-cycle` parses
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 Phase 4 (spec.md:593–612) vs `spec-brief/SKILL.md:138` and `spec-cycle/SKILL.md:636–640`
**Edge case:** A `fence-empty` brief for a ticket whose text states no out-of-scope items.
**What happens:** `## Out of scope` is populated only by mapping rule `:138` (a Settled decision framed as a fence). A `fence-empty` summary has zero Settled items, so the section is empty. Design 7 prescribes `_(none)_` for Decisions and Scope and one item for Risks, and says nothing about `## Out of scope` — a bare header between two sections that got sentinels.

It also lands on the deferred drift-check hole: `## Out of scope` is one of the three headers `/spec-cycle`'s Phase 3 parser keys on (`:638`), and `:640`'s fallback fires only when a header is *missing*. So a `fence-empty` brief renders zero Out-of-scope checkboxes **and** zero Decisions checkboxes; Risks 6 accounts for one.
**Suggested fix:** Replace the per-section enumeration with the general rule over the template: every section the interview would have populated — Decisions, Scope, Out of scope — renders `_(none)_`; Risks carries the one item; Problem / Why it matters / Done when / References are transcribed as normal. Add `## Out of scope` to row 12 and extend Risks 6 to two headers.

---

### F-4: The post-cap-round-not-consumed rule preserves a round no caller can spend, and its rationale cites the line that makes it unrecoverable
**Severity:** P2
**Where:** spec § Design 4 (spec.md:411–416) vs `spec-brief/SKILL.md:105` and `grilling/SKILL.md:23`
**What happens:** The rule works at the primitive's level, but the only caller that resumes is `/spec-brief` Phase 3, and `:105` reads "this skill offers option 2 at most once after a cap hit, and **once a post-cap resume has returned** the block re-renders with options 1 and 3 only." *Returned* — not *rendered*. So the caller withdraws option 2 whether the round rendered or not, and the preserved round is unreachable. 2f-i never resumes and `/grill-me` has no resume path. The only observable effect is the exit token and the `rounds:` count.

The spec's own rationale inverts the causality: it cites `:105` as the reason the round must not be burned, when `:105` is the mechanism that prevents recovery either way.
**Suggested fix:** Either (a) narrow `:105` in the same PR — "once a post-cap resume has returned **having rendered at least one item**" — and add it to Design 7 and row 12; or (b) drop the not-consumed rule and keep only the exit-token correction, recording in § Deferred that the preserved round has no caller. Either way rewrite the rationale so it does not cite `:105` as evidence for a benefit `:105` blocks.

---

### F-5: "Dispatched once; the operator is never re-asked" is scoped to one invocation, and the resume contract re-asks and re-dispatches
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 rule 1 (spec.md:352–361) vs `grilling/SKILL.md:23`
**Edge case:** `/spec-brief` Phase 3 option 2 — the operator revises a decision upstream of a fact request they already answered with a claim that came back unverified.
**What happens:** Both halves of rule 1 break. `:23` exempts only *established* facts from re-dispatch, so the rebuilt tree re-dispatches the verification rule 1 says is "**not retried**". And "Prior Open items stay Open and are not re-asked **unless they are downstream of the revised decision**" puts an Open F-item back on the frontier, where § Fact-finding renders it as an `ℹ️` fact request — re-asking the operator for the fact rule 1 says they are never re-asked for.
**Why the spec misses it:** Rule 1 is written entirely inside one interview. Design 3 never touches § Invocation contract, and row 5 protects the resume contract as a VHS-32 invariant, so the spec's own gate pushes against noticing that v2 adds an item shape the resume contract does not enumerate.
**Suggested fix:** Scope rule 1 to "within one invocation" and state the resume behaviour for an Open F-item carrying a claim qualifier: it carries over as Open and its verification is not re-dispatched, matching how `:23` treats established facts. Add the resume clause to row 7.

---

### F-6: Precedence demotes a `deferred to option 3` item to `left open` and no clause records that option 3 would discharge it
**Severity:** P2
**Where:** spec § Design 6 (spec.md:526–537)
**What happens:** The chain puts the id in `left open`. `also edited (left open)` cannot pick it up — that clause carries only ids "whose Settled item was nonetheless **applied**", and a `deferred to option 3` item is by definition not applied. So the operator sees the finding in `left open` with no signal that the interview produced a Settled decision whose discharge is menu option 3. Same information-loss shape as round-2 F-4, at the middle rung of the same chain.
**Suggested fix:** Either widen the clause into a general demotion-visibility clause — `also settled (left open) <ids>`, carrying every demoted id whose Settled item was applied *or* deferred to option 3, with the applied ones additionally taking the title suffix — or state the loss. Pin whichever in row 10.

---

### F-7: The rolled-up-deferred narrowing and Design 6's conservative-reporting principle pull opposite ways
**Severity:** P2
**Where:** spec § Design 1 Inheritance (spec.md:219–226) vs § Design 6 Precedence (spec.md:526–530)
**What happens:** Design 1's narrowing strips an id from the rolled-up deferred item's `ref:` when any rendered decision reached it, so step 5 reports it `dispositioned` with no trace that a whole subtree bearing on it went unexplored. Design 6 states the opposite principle for the structurally identical case: "A finding referenced by both an Open item and an applied Settled item is reported **left open** — the conservative report is the honest one." Mechanically compatible; what breaks is the invariant a reader would infer.

Second-order ambiguity in "no rendered decision **reached**": unclear whether a rendered-but-still-Open question counts.
**Why the spec misses it:** The narrowing was derived before `also edited (left open)` existed. With that clause in place the sweep is no longer silent, so the narrowing solves a problem the sibling fix already solved, at the cost of the conservative report.
**Suggested fix:** Either drop the narrowing now that the demotion is visible, and let the rolled-up item carry its parent's ids so conservative reporting holds uniformly; or keep it and state it as a deliberate exception. Define "reached" explicitly. Add the chosen rule to row 6.

---

### F-8: On the `fence-empty` path Phase 3 previews an empty Risks list and Phase 4 writes one
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 Phase 3 (spec.md:585–591) and Phase 4 (spec.md:604–609) vs `spec-brief/SKILL.md:94`
**What happens:** `:94` derives the preview's Risks list from the summary's Open frontier, which on `fence-empty` is `_(none)_`. So the preview shows two empty lists, and Phase 4 then writes one Risks item the operator never saw. The confirm step's only job is that what is previewed is what is written.
**Suggested fix:** One sentence in Design 7's Phase 3 paragraph: the preview renders the same single Risks item Phase 4 will write, and `_(none)_` under Decisions, so the preview is the brief. Extend row 12.

---

### F-9: `revised-after-cap (+1 round)` has no entry in the Open-item reason set or the precedence chain
**Severity:** P3
**Where:** spec § Design 2 block (spec.md:259, :281)
**What happens:** The header renders `exit: revised-after-cap (+1 round)`, and every Open item needs an `unresolved because:` value. Neither the set nor the chain names this exit. An implementer will most likely pick `round-cap`, which is defensible, but the chain is now presented as the authoritative ranking and the reader has no entry to apply. The ambiguity is pre-existing; promoting the ordering to a stated rule makes it visible.
**Suggested fix:** One sentence: on a `revised-after-cap (+1 round)` exit the exit reason is `round-cap` for ranking purposes. Add to row 4.

---

### F-10: The Open-frontier bound, restated verbatim in D13, does not account for never-rendered overflow F-items
**Severity:** P3
**Where:** spec § D13 (spec.md:184–186) vs `grilling/SKILL.md:132`, `:63`, `:74`
**What happens:** `:74` says overflow fact needs "reach the hand-off as Open with `unresolved because: fact not established`" — items never rendered to the operator. `:63` states the counter-invariant, "Only questions actually rendered to the operator ever become named Open items", and `:132` derives the bound from it. D3 now gives those overflow needs a formal named Open shape, so up to `question_cap` items can sit in the frontier outside the derivation. Bounded and small, and scale is a declared non-factor — but D13 restates the bound as a drift-check anchor, and `:132` sits inside a range the Scope table says changes without being mentioned.
**Suggested fix:** Restate the bound as `(round_cap + 1) × question_cap` named items **plus at most `question_cap` un-rendered fact requests**, plus one rolled-up item per deferred subtree — or reconcile `:63`. Add `:132` to the Scope cell either way.

## Summary
P0: 1 | P1: 1 | P2: 6 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=1 P2=6 P3=2 P4=0
