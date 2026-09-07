# Edge-Cases Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Precedence chain has no entry for `fact not established` | CLOSED | spec.md:308–318 two chains; Design 3 rule 3 (`:443–448`) says the qualifier survives on every exit incl. `stop`. New variant → R4 F-2 |
| edge-cases | F-2 | `:108` amended, `:151` left restating the reversed rule | CLOSED | spec.md:347–354 amends both in one hunk; Scope cell names `:151`, `:148`, `:149`; rows 4 and 7. Verified against `grilling:151` |
| edge-cases | F-3 | All-sections-empty misses `## Out of scope` | CLOSED | spec.md:694–701; Risks 6 verified correct against `spec-cycle:636–640` |
| edge-cases | F-4 | Post-cap round preserved but unspendable | CLOSED (by removal) | spec.md:483–492; row 8; § Deferred + Risks 7. No dangling reference survives |
| edge-cases | F-5 | Dispatched-once is invocation-scoped; resume re-asks | CLOSED | spec.md:413, 429–437. Residual scoping gap → R4 F-8 |
| edge-cases | F-6 | Demoted `deferred to option 3` item has no clause | CLOSED | spec.md:613–622; row 10 asserts both halves |
| edge-cases | F-7 | Rolled-up narrowing fights conservative reporting | CLOSED (by removal) | spec.md:245–253; row 6 asserts "**no** narrowing" |
| edge-cases | F-8 | Phase 3 previews an empty Risks list | CLOSED | spec.md:678–683; row 12 |
| edge-cases | F-9 | `revised-after-cap` has no entry in the chain | CLOSED | spec.md:317–318; row 4 |
| edge-cases | F-10 | `:132` bound ignores named overflow F-items | CLOSED | D13 `:197–205`; `:132` in the Scope cell. No gate row asserts it → R4 F-6 |
| correctness | F-1 | Round-2 fix amended `grilling:23` outside Scope | CLOSED | Same removal as edge-cases F-4 |
| correctness | F-2 | `:151` duplicate | CLOSED | Same as edge-cases F-2 |
| correctness | F-3 | Chain does not place `fact not established` | CLOSED | Split chains + `:313–316`. New variant → R4 F-2 |
| correctness | F-4 | Row 12 calls the template "eight-section" | CLOSED | Row 12 now "nine-header" |
| conventions | F-1 | `:148`/`:149`/`:151` undesigned | CLOSED | spec.md:347–362; rows 4 and 7 |
| conventions | F-2 | All-or-none report renders outside the block `:116` renders exactly | **PARTIAL** | Report moved to the header's `reason:` field (`:232–239`) — but Design 2's block (`:280`) does not carry the value, Design 4 (`:500`) says the reason enumeration is *unchanged*, and row 6 (`:816–817`) still asserts the rejected placement → R4 F-1 |
| conventions | F-3 | § Deferred coverage claim false | CLOSED | spec.md:1066–1070 |
| conventions | F-4 | Two spec-level additions missing from the roll-up | CLOSED | spec.md:84–92 |
| conventions | F-5 | Preamble vs `question_cap` unstated | CLOSED | spec.md:540–544, cites bound 2 (`:85`) |
| conventions | F-6 | `:104` not named | CLOSED | Scope cell `:28`; row 8 |

## Findings

### F-1: The `partially identified seed` reason value is required by Design 1 and row 6, absent from the authoritative block, and forbidden by Design 4
**Severity:** P0
**Where:** spec.md:232–239 and :820–821 vs spec.md:280 and :500
**Edge case:** A caller supplies `id` on some seed items but not all — the one contract violation Design 1 exists to report.
**What happens:** Three statements in the same spec disagree:
- Design 1 (`:232–233`): the report renders "**on the hand-off header's `reason:` field** as `partially identified seed — ref: omitted` on every exit that renders the block", and explicitly *not* above the header.
- Design 2 (`:280`), declared at `:275` to be "the authoritative rendering. Everything the other designs change appears here in one place", renders the v1 enumeration — the new value is absent.
- Design 4 (`:500`): "the reason enumeration is **unchanged**." A direct prohibition on the edit Design 1 requires.
- Row 6 (`:816–817`) asserts *both* renderings at once: the rejected above-the-header placement, and four lines later the `reason:`-field assertion.

An implementer following Design 2 + Design 4 ships a block with no slot for the value; one following Design 1 + row 6 edits a line Design 4 pins. The ship gate passes on either reading of row 6's first clause and fails on the other.
**Why the spec misses it:** the round-3 → round-4 fix moved the report's home but touched neither the block literal, nor Design 4's sentence about the same literal, nor row 6's stale clause. All three were REWRITE this round.
**Suggested fix:** (a) add the value to the block's reason enumeration; (b) change Design 4's sentence; (c) replace row 6's parenthetical. Also add the missing composition rule — `reason:` is a single field and the spec never says what happens when a partially identified seed coincides with an exit that has its own reason. State it, e.g. `reason: <exit reason>; partially identified seed — ref: omitted`.

### F-2: The amended `:108`/`:151` rule and the F-item precedence chain give two different answers for a verification dispatch abandoned at `stop`
**Severity:** P1
**Where:** spec.md:340–345 vs :309–311, :320–326 and :438–448
**Edge case:** The operator answers `F1 <answer>` in round 2. Rule 2 dispatches the verification in round 3's batch. The operator types `stop` during round 3. The verification is an **exploration in flight** carrying an operator claim.
**What happens:** Two prescribed sentences, both destined for the same file, rule differently:
- Design 2 `:342–345` (the text replacing `:108`/`:151`): "on a `stop` with an exploration in flight … the F-item renders `stopped`". Unconditional over "an exploration in flight"; a verification dispatch is one.
- The F-item chain plus `:320–326` ("Ranking the exit reason first would erase the operator-claim qualifier at exactly the exit where a brief author most needs it") requires `fact not established (operator claim, unverified)`.

Downstream this is not cosmetic: `/spec-brief` Phase 4's mapping bullet (`:713–719`) carries the qualifier into `## Risks / decisions`. Under the `:108` reading the qualifier is gone — the loss § Deferred's closing paragraph claims is "**closed, not deferred**" (`:1066–1070`).

This is the precise defect the amendment exists to remove: "Amending `:108` alone would ship a file that answers the stop case two ways" (`:350–352`). Row 4 asserts the amended `:108` behaviour *and* both chains, so the gate passes with the contradiction in the file.

Secondary: `stopped` is defined at `:315–316` as "reserved for an F-item with no disposition of its own", but nothing defines when `fact not established` *applies*. Read literally it applies to every unestablished fact, making `stopped` unreachable and the F-chain vacuous.
**Suggested fix:** Qualify the `:108`/`:151` text — "the F-item renders `stopped` **unless it carries an `(operator claim, …)` qualifier**" — and define the antecedent: "`fact not established` applies only where the fact-finding machinery assigned a terminal disposition — twice unanswered (`:88`), dispatch-cap overflow (`:74`), failed dispatch (`:76`), no read-restricted agent class (`:72`), or a verified/refuted/unverified operator claim. An exploration abandoned mid-flight with none of these renders `stopped`." Add both to row 4.

### F-3: `_(none)_` is a new token in a block three callers parse, with no consumer-side rule outside the `fence-empty` path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:364–370 (Design 2, "on *every* exit"); consumers at :685–711 and :559–631
**Edge case:** Any non-`fence-empty` exit with one empty section — which Design 2 itself calls the common case. Also `### Facts established` empty on a topic needing no facts; `### Settled` empty on a round-1 `stop`.
**What happens:** the spec tells `/spec-brief` about `_(none)_` **only** on the `fence-empty` path. Everywhere else the mapping rules are unchanged: `spec-brief:140` "Open frontier items → `## Risks / decisions`, numbered, each ending 'spec author pins this'", `:142` "Facts established → `## References`, with `path:line`". An implementer transcribing the section writes `_(none)_ — spec author pins this`, or a `## References` bullet `_(none)_` with no `path:line`. Secondarily, 2f-i step 4 iterates "each **Settled** item" and step 5 reports `item missing ref: <item title>` — an implementer treating the sentinel as an item emits `item missing ref: _(none)_` and flags a contract violation on a legitimately empty section.
**Suggested fix:** one sentence in Design 2: "`_(none)_` is a sentinel, not an item: a caller treats a section rendering it as containing zero items, and never transcribes it into its own artifact." Assert in row 4.

### F-4: Verification dispatches share `question_cap` with new fact needs, and the ordering rule Design 3 points at cannot rank them
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:438–441 vs `grilling:85`, `:74`
**Edge case:** A round in which the operator answered several fact requests *and* the frontier generates new fact needs — five answers plus four new needs against a cap of seven.
**What happens:** Rule 2 says overflow "carries to the next round's batch by the existing ordering rule". `:85`'s rule is "carried-over and re-asked items first, then shallowest tree depth …, then your judgment of blast radius". A verification dispatch is not a carried-over or re-asked *item*, has no tree depth, and its blast radius is the claim's — none of the three tiers ranks it. The losing class silently reaches the hand-off Open, and under `round_cap` 3 that is terminal. The two classes degrade differently: a starved new fact need renders bare `fact not established`, a starved verification renders `fact not established (operator claim, unverified)` — indistinguishable from a claim that *was* checked and failed.

Adjacent: rule 3 covers "a claim answered in the **last rendered round**". A claim answered in round 2 whose verification overflows out of round 3's batch is not covered, and no other rule names its outcome.
**Suggested fix:** add to rule 2: "Within a round's batch, new fact needs are dispatched before verifications — an unestablished fact blocks a question, a verification only annotates one; verifications overflow first. A verification that overflows past the last round renders `fact not established (operator claim, unverified)`, as rule 3." Add to row 7.

### F-5: A `fence-empty` summary carrying items is unguarded, and `/spec-brief` Phase 4 then discards them
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:685–711, :633–638 vs :473–481
**Edge case:** The primitive returns `exit: fence-empty` in the header but a non-empty `### Settled` or `### Open frontier` — a model-rendering error, which Risks 2 records as a live risk for exactly this block.
**What happens:** both consumers branch on the token alone. Phase 4's all-sections-empty rule writes `_(none)_` under three headers regardless of what the summary carried — silently destroying every settled decision in it. 2f-i step 5 replaces the generic line with the fence-empty one while step 4, which runs first and does not branch on the token, has already applied the Settled items to the spec. The report then contradicts the edits.

This is the same harm Design 4 names in its own resume rule (`:479–481`). That reasoning closed the resume path into the failure and left the fresh-invocation path open. The three guards this spec adds (`unknown ref ignored:`, `item missing ref:`, `not reached`) all guard the `ref:` field; none guards the exit-token/section coupling this ticket newly creates.
**Suggested fix:** one clause in Design 7 and one in Design 6: "A `fence-empty` summary carrying any Settled or Open item is a contract violation. Do not apply the all-sections-empty rule or the purpose-written step-5 line; treat the summary as `empty-frontier`, map its items normally, and report `fence-empty summary carried <n> items — treated as empty-frontier`." Add to rows 10 and 12.

### F-6: Three Scope-listed `grilling` edits have no checklist row, and the checklist is the ship gate
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:28 and :197–205 vs the checklist at :788–850
**What happens:** three edits the Scope table commits to can ship unimplemented and the gate passes green:
- the restated Open-frontier bound at `:132` — row 4 covers the block, row 5 covers § Bounds' three bounds; neither names `:132`. This is the whole substance of the round-3 F-10 fix.
- the `:74` and `:88` cross-reference pointers to the new F-item form — named in the Scope cell and designed in Design 2's "Cross-references" paragraph. Row 7 asserts `:148`/`:149` and stops there.

If `:132` ships unrestated, the file states a bound D3's own new item shape falsifies.
**Suggested fix:** extend row 4 with the `:132` bound text, and row 7 with "`:74` and `:88` each carry a pointer to the `F<n>` Open form".

### F-7: The rolled-up deferred item is a third Open shape, and the precedence section states orders for two
**Severity:** P3
**Where:** spec.md:288, :304–318, :244–245
**What happens:** the section says "The two item shapes draw from different value sets" and labels the chains `Q-item:` and `F-item:`. The block defines **three** Open shapes, and Design 1 says the rolled-up one is "the case with no `Q` number at all" — so the `Q-item` label does not plainly reach it, and the `F-item` chain has no `deferred` value. In practice the block template hard-codes `unresolved because: deferred`, so the rendering is determined; but this ticket is the one that gives shape 3 that field for the first time (`grilling:126` has none today).
**Suggested fix:** one sentence after the chains: "The rolled-up deferred item is a fixed case, not a ranking: its reason is always `deferred`, on every exit." Add to row 4.

### F-8: The resume no-re-dispatch rule covers only qualifier-carrying F-items, and its downstream case leaves a dependency nothing can satisfy
**Severity:** P3
**Where:** spec.md:429–437 vs `grilling:23`, `:74`
**Edge case:** (a) A resume where an Open F-item carries a plain `fact not established` — no qualifier. (b) A resume where a qualifier-carrying F-item *is* downstream of the revised decision.
**What happens:** (a) the rule exempts only qualifier-carrying items; by expressio unius a plain Open F-item is re-dispatched on every resume. That may be wanted, but it is left to inference in the ticket that first gives plain F-items a named Open shape. (b) the rule says such an item "re-enters the frontier as a dependency of the decision being re-asked" while remaining un-re-dispatched. `:74` says "Questions downstream of a fact wait for it", so the re-asked decision waits on a fact that can never arrive, never renders, and returns Open `blocked-on: F<n>`. On a post-cap resume that is the operator's single extra round spent on a round that renders nothing — Risks 7's failure by a second route the Risk does not name.
**Suggested fix:** state both: "Every Open F-item carries over as Open and is not re-dispatched, qualifier or not. Where one is downstream of the revised decision, the decision it gates is rendered anyway with the fact still open — it does not wait." Extend Risks 7 and row 7.

## Summary
P0: 1 | P1: 1 | P2: 4 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=1 P2=4 P3=2 P4=0
