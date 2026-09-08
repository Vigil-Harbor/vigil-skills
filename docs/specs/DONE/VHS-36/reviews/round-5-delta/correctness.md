# Correctness Review — round 5 (delta-only)

Grounding done. HEAD is `f4d9290`; all four target files unchanged since the anchors were read (last touch `648f4ff`, part of the VHS-33 series that predates the anchor commit). I read the spec fresh, the DELTA, all three round-4 reports, and re-verified every source line the changed sections quote.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Row 3 pins "never carried to a later round", shipped text says "no check is ever carried" | **CLOSED** | spec:679 now pins `"no check is ever carried to a later round"`; shipped sentence spec:286–287 contains it verbatim; `grep -F 'never carried to a later round'` over the spec → 0 |
| edge-cases | F-1 (P0) | Same defect — the gate row cannot pass | **CLOSED** | identical evidence; the gate row and the byte-pinned blockquote now agree |
| conventions | F-3 (P2) | Same defect | **CLOSED** | identical evidence |
| edge-cases | F-2 (P2) | Truncation key ships without a direction | **CLOSED** | shipped text spec:285 "in ascending `F<n>` order (lowest first)"; pinned in row 3 (:678–679); commentary :298–299 "ascending `F<n>`, oldest fact need first" agrees, and :48's monotonic series makes lowest = oldest |
| conventions | F-1 (P2) / correctness F-2 (P2) | Shipped sentence claims parity with `:87` | **CLOSED** | "as the per-round item cap is" gone (grep → 0); shipped text now "unlike a fact need beyond the dispatch cap above, which does carry", true against `SKILL.md:76`; new commentary ¶ at :315–324 states the asymmetry. See F-2 below for a nit inside that ¶ |
| conventions | F-2 (P2) | Queue ¶ rests on `:80`, which says something else | **CLOSED** | the `:80` clause is gone (grep "No resume state is kept" → 0); replaced at :333–336 with "the primitive's only cross-round structure whose contents are neither rendered nor numbered", which is accurate against `:76`'s carried-but-numbered fact needs |
| edge-cases | F-4 (P2) | "at most one check" understates the loss | **CLOSED** | "Truncation costs at most one check" and "the one claim it drops" both gone (grep → 0); new **The cost, stated plainly.** ¶ (:338–348) gives `answered − question_cap`, up to 21 under the defaults — arithmetic consistent with :312's `(round_cap + 1) × question_cap` |
| edge-cases | F-5 (P2) | Emptiness test fires at render time | **CLOSED** | matched pair landed: intake at spec:230 ("or an answer that the normalization below leaves empty — is not a claim: no check is dispatched, and the fact request counts as unanswered under § Bounds"), render-site at :378 ("an answer this leaves empty was not a claim, and the intake rule above governs it"). Both halves pinned in row 3 (:682–685) |
| edge-cases | F-3 (P2) | Truncation is silent to the operator | **CLOSED as recorded-not-folded** | new § Deferred bullet (:905–913) plus the disclosure in the cost ¶ (:342–347); the two texts agree on the reason and on the un-filed status |
| edge-cases | F-6 (P3) | Re-answered Open `F<n>` that confirms — Open entry not withdrawn | **CLOSED** | shipped text :366–367 "leaving the Open frontier if it was there, since one `F<n>` has one disposition"; consistent with Design 4's "The two never share a number" (:422) and with Design 6's resume rule (:480–481) |
| edge-cases | F-7 (P3) | Gated-question note is a fourth boundary; commentary counts three | **CLOSED, pair complete** | Design 6 shipped text :471 "in its normalized form"; Design 3 commentary :408–411 "four boundaries … the gated question's note in Design 6 … and all four are stated". Neither half is missing |
| edge-cases | F-8 (P4) / correctness F-5 (P3) | Design 10 bullet omits the truncation cause | **CLOSED** | :571 "a check that could not be dispatched **or that the round's batch cap truncated**"; row 8 (:738–740) pins only the lead and position, so no row conflict |
| correctness | F-3 (P2) | D4 says "dispatch at once" stands unchanged | **CLOSED** | :112–117 "stands unchanged **in kind**… What the cap does remove is decision 4's implicit guarantee that *every* claim gets a dispatch — a claim past the cap in its round receives none, ever… That is the accepted cost" |
| correctness | F-4 (P3) | "unblocks nothing by being early" no longer describes the key | **CLOSED** | phrase gone (grep → 0); :301–306 concedes the key is a selection rule under truncation and gives a positive justification (determinism + matching § Bounds' first key) |
| correctness | F-6a (P4) | "cross-batch" mis-names the attempt-1 rule | **CLOSED** | :117 "*shared-batch*"; grep "cross-batch" → 0 |
| correctness | F-6b (P4) | attempt-1 citation `:476–488` | **REGRESSED** — see F-1 below. My round-4 finding was itself wrong; the fold acted on it |
| correctness | F-6c (P4) | row 10 says "two anchors" | **CLOSED** | :752–753 "four anchors are re-translated… `:70`→`:72`, `:61`→`:63`, `:84–86`→`:86–88`, `:94–98`→`:96–100`". All four verified correct against the file at `f4d9290`: `:72` is the dispatch sentence, `:63` the advisory sentence, `:86–88` the three bounds, `:96–100` the worked-examples table |
| conventions | F-4 (P3) | Discard-on-truncation is a category-c addition the brief does not authorize | **CLOSED (conventions' call)** | change 4's D4 rewrite is exactly the disclosure the category asks for: :114–117 names the removed guarantee and calls it "the accepted cost" |

**Plainly, on the two gate-blocking findings: correctness F-1 (P1) and edge-cases F-1 (P0) are both CLOSED.** The pin and the byte-pinned shipped sentence now agree, and I verified all thirteen phrases row 3 pins against the reconstructed shipped text — including the four this delta added — with no mismatch.

**Matched pairs, both fully applied.** Changes 5/6 (emptiness test render-time → intake) are both on disk and agree: the intake sentence forward-references "the normalization below", the render-site sentence back-references "the intake rule above", and the shipped paragraph order (Design 1 first, Design 3 third of eight) makes both directions true. Changes 7/8 (fourth boundary) are both on disk and agree on the count and on which surface the fourth is. Neither pair is half-applied.

**No new cross-section inconsistency found.** I re-walked every section that cites the changed text: D1/D4/D10 in § Decisions, Designs 2/3/4/6/7/10/12, test-plan rows 3, 4, 5, 6, 8, 10, 12, 17, § Out of scope, and § Deferred. The three call-site counts still reconcile (Design 3 names six not-confirmed causes; Design 12 and row 12 name those six plus Design 5's no-dispatch case = seven; Design 12's commentary at :627 says exactly that). Design 10's shorter four-cause parenthetical uses different wording from Design 12's, but row 12's pins are scoped to `/grill-me`'s bullet, so there is no gate conflict.

## Findings

### F-1: The attempt-1 citation was correct before the fold and is now off by two lines
**Severity:** P4
**Where:** spec § Decisions carried forward, D4 (`VHS-36.spec.md:117–118`)
**Claim:** "Attempt 1's *shared-batch* ordering rule (`attempt-1/spec.md:478–488`) is deleted outright"
**Why this is wrong:** My round-4 F-6b asserted that "`:476–477` is the tail of rule 1" and "rule 2 begins at `:478`". That was wrong. `docs/specs/DONE/VHS-33/attempt-1/spec.md` at `f4d9290` reads:

```
474|   this one is not, so waiting would render nothing and, on a post-cap resume, spend
475|   the operator's single extra round on an empty round.
476|2. **It rides the normal batch and counts against the same cap.** Verification is
477|   dispatched in the round *after* the operator's answer, inside that round's single
478|   parallel batch, against the `question_cap` dispatch cap.
```

Rule 1's tail is `:474–475`; rule 2 opens at `:476`. The original citation `:476–488` spanned rule 2 exactly, from its bold lead to the end of its overflow paragraph. The new `:478–488` starts mid-sentence at "parallel batch, against the `question_cap` dispatch cap." and drops the rule's opening. The cited range still contains the overflow rule the sentence is about, so nothing is misdirected — this is precision, not misdirection, and the file is an archived DONE spec nobody implements from. Recording it so the error I introduced does not propagate into `/spec-close`'s decision record.
**Suggested fix:** Restore `(`attempt-1/spec.md:476–488`)`.

### F-2: The new asymmetry paragraph describes `:87`'s two sentences as one
**Severity:** P4
**Where:** spec § Design 2 commentary (`VHS-36.spec.md:317–321`)
**Claim:** "`:87` carries rendered items beyond the per-round cap — its phrase 'a hard truncation, not a soft target' is **the second half of a sentence whose first half is** 'overflow carries to the next round'"
**Why this is wrong:** `skills/grilling/SKILL.md:87` reads `…**questions and fact requests together**; overflow carries to the next round. This is a hard truncation, not a soft target.` Those are two consecutive sentences, not two halves of one; the carry clause is the tail of the sentence beginning "At most `question_cap` rendered items per round". The paragraph's substantive point — that the borrowed phrase modifies a rule whose overflow carries, so it cannot license discarding — is correct and unaffected. Non-shipping commentary; no implementation follows from it. (DELTA.md also describes this change as quoting `:76` and `:87` "in full"; it paraphrases both with embedded quotations. Same class.)
**Suggested fix:** "…its phrase 'a hard truncation, not a soft target' is the sentence immediately following 'overflow carries to the next round', so it means…".

### F-3: § Deferred's preamble no longer describes its contents
**Severity:** P4
**Where:** spec § Deferred (P2+) preamble (`VHS-36.spec.md:884–885`) vs the new bullet (`:905–913`)
**Claim:** "**Round-1 findings** that are valid, out of this brief's scope, and non-trivial — **filed** rather than folded:"
**Why this is wrong:** The section now holds five bullets: three round-1 findings, one round-3 finding (VHS-40, `:903`), and — new this delta — one **round-4** finding. Two of the five are explicitly **not** filed (`:912–913` "not filed, because the case needs the operator to answer more than `question_cap` claims in a single round"; `:919` "Not filed; re-raise if it shows up in practice"). The drift is pre-existing — VHS-40 already broke "Round-1" at round 4 and the round-1 F-15 entry already broke "filed" — and change 11 extends rather than creates it. It matters only because `/spec-close` decomposes this section, and the recorded provenance of the truncation-visibility decision is the useful part.
**Suggested fix:** "Review findings that are valid, out of this brief's scope, and non-trivial — filed as tickets, or recorded here where no ticket is warranted:".

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 0 | P4: 3

STATUS: GREEN
