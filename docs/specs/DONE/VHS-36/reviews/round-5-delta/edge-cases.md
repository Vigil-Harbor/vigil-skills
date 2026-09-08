# Edge-Cases Review — round 5 (delta-only)

Read: `docs/specs/TODO/VHS-36.reviews/round-5-delta/DELTA.md`, the current spec, the target `skills/grilling/SKILL.md` at `f4d9290`, `docs/specs/DONE/VHS-33/spec.md`, `.../VHS-33/attempt-1/spec.md`, and the brief. Plane VHS-36 retrieved.

## Closure of round 4 findings (mine)

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P0) | Row 3 pins a phrase the truncation sentence does not contain | **CLOSED** | Row 3 now pins `"no check is ever carried to a later round"` (spec:679); shipped text spec:286–287 reads "…and no check is ever carried to a later round, unlike a fact need beyond the dispatch cap above, which does carry." Byte-equal. The two new row-3 pins also match verbatim: `"ascending F<n> order (lowest first)"` = :285; `"an answer this leaves empty was not a claim"` = :378; `"or an answer that the normalization below leaves empty"` = :230. The dropped pin `where nothing checkable survives` appears nowhere in the spec (grep clean). |
| edge-cases | F-2 (P2) | Ordering key ships without a direction | **CLOSED**, residue → new F-1 | Direction now in the shipped sentence (:285) and pinned (:678–679); the stale "unblocks nothing by being early" rationale is replaced by :299–306, which concedes the key is a selection rule under truncation and gives the reason for shipping the direction. Residue is *membership* of the ordered set, not direction — new F-1 below. |
| edge-cases | F-3 (P2) | Truncated claim is silent to the operator | **DISCLOSED, deliberately not folded** — disposition honest; disclosure has one inaccuracy → new F-3 | :341–348 states the silence, states the operator is not told, names the mitigation as considered-and-declined, and points at § Deferred :905–913, which names me, the round, the finding id, the reason, and the trigger for re-raising. That is an honest disposition and I accept it: the loss is bounded and safe, and adding a rendering behavior after the last review round is exactly the round-3 failure. The one defect is accuracy, not honesty — see new F-3. |
| edge-cases | F-4 (P2) | "at most one check" understates the loss | **CLOSED** | :338–340 "Truncation drops `answered − question_cap` checks in a round — up to 21 under the defaults", consistent with the reachability paragraph at :310–313 ((3+1)×7 = 28; 28−7 = 21). :359 now "the claims it drops". |
| edge-cases | F-5 (P2) | Emptiness test fires at render time, after the dispatch | **CLOSED**, residue → new F-5 | Intake clause at :230 with both intake consequences; Design 3's tail at :378 now defers to it ("the intake rule above governs it"). The test is decidable at intake — see the probe answers below. |
| edge-cases | F-6 (P3) | Re-answered Open `F<n>` that confirms | **CLOSED** | :366–367 "leaving the Open frontier if it was there, since one `F<n>` has one disposition". Holds against Design 4 — see probe answers. |
| edge-cases | F-7 (P3) | Fourth boundary | **CLOSED** | :408–411 counts four and names the gated note; Design 6 ships "in its normalized form" (:471). |
| edge-cases | F-8 (P4) | Failure-mode bullet omits truncation | **CLOSED** | :571–572 "a check that could not be dispatched or that the round's batch cap truncated". |

Other lenses' folds I verified while checking cross-section consistency: change 3's `:76`/`:87` characterisation (accurate in substance, one wording defect — new F-8); change 4's `shared-batch` relabel (correct against `attempt-1/spec.md:482–483`) but its anchor re-cite is a regression (new F-4); change 10's four anchor re-translations (`:70`→`:72`, `:61`→`:63`, `:84–86`→`:86–88`, `:94–98`→`:96–100`) — all four correct against `skills/grilling/SKILL.md` at `f4d9290`, and the count is right: VHS-33 row 7 cites the callers-map sentence with no line number, so `:139` is this spec's own pin, not a fifth translation.

## Answers to the three probes

**Is "an answer that the normalization below leaves empty" decidable at intake?** Yes. The normalization (:374–378) is a pure, deterministic text function of the answer alone — whitespace collapse, quote folding, field-marker removal, length elision — with no dependency on the check, the round, or any later state. The forward reference is to a paragraph two paragraphs later in the same inserted run, and the spec's own idiom already uses "the normalization below" / "the rule above" in both directions. Routing it to "counts as unanswered under § Bounds" composes correctly with `:90`: two such answers to the same `F<n>` make it Open as plain `fact not established`, no qualifier, no `claim:` field — which is also the right answer under D7's precedence (the operator never *answered* it, by the spec's own definition of answered at :227–232). It composes correctly with truncation too: a non-claim never enters the batch, so it cannot consume a slot. The residue is what happens when a non-claim arrives *after* a real claim on the same `F<n>` (new F-5).

**Does "leaving the Open frontier if it was there" hold for Design 4's contrary-evidence case?** Yes. The clause is scoped to the **Confirmed** branch; contrary evidence is not a confirmation, and Design 4 (:415–423) puts the evidence under a *fresh* number while explicitly leaving "the claim Open under its original number". So one `F<n>` still has one disposition, and Design 4's own invariant ("The two never share a number") is the same rule stated for the other case. No conflict.

**Is "ascending `F<n>` order (lowest first)" fully determined?** Tie-break: yes — `F<n>` is unique per fact need, and Design 1's replacement rule ("a later answer to the same `F<n>` replaces the claim") collapses a within-round duplicate to one entry, so the order is strict and total. Membership: **no** — see new F-1.

## Findings

### F-1: The truncation set is counted in claims, but the cap is a dispatch cap — a no-repo-footprint claim consumes a slot it never needed
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 shipped blockquote (`VHS-36.spec.md:278–287`) vs § Design 5 (`:444–451`)
**Edge case:** In one round the operator answers more claims than `question_cap`, and at least one of the low-numbered claims has no repo footprint.
**What happens:** The cap is stated over dispatches — "one parallel batch, **capped at `question_cap` dispatches**" — but the truncation trigger and the ordered set are stated over claims: "where the operator answered more **claims** in one round than the cap allows, the batch takes **them** in ascending `F<n>` order … and the rest are not checked at all". Design 5 says a no-footprint claim gets **no dispatch** at all, yet it is unambiguously a claim (the paragraph calls it one and gives it the qualifier). So with `question_cap = 7`, nine claims answered, two of them no-footprint and among the seven lowest `F<n>`: the trigger fires (9 > 7), the ordered set takes the seven lowest, only five dispatches actually fire, and two checkable claims at higher `F<n>` are dropped permanently with two batch slots unused. The loss is silent (the operator is not told which were dropped, :341–344) and terminal (no carry, :286). It degrades safely — the claim still reaches the caller labelled — which is why this is P2.
**Why the spec misses it:** The truncation sentence was written before Design 5's no-dispatch case was in view, and the two paragraphs never meet: Design 2 counts answered claims, Design 5 removes some of them from the dispatch set.
**Suggested fix:** Two words in the shipped sentence: "…where the operator answered more claims **needing a dispatch** in one round than the cap allows, the batch takes them in ascending `F<n>` order (lowest first)…". Row 3's pin `"ascending F<n> order (lowest first)"` is unaffected.

### F-2: "nothing checkable" carries opposite dispositions in Design 1 and § Termination, and change 5 widened the collision
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 (`:229–232`) vs § Design 7 shipped text (`:508–510`)
**Edge case:** `F3 I don't know` (or an answer the normalization empties) in the stopping round.
**What happens:** Design 1: an answer that "asserts **nothing checkable**" is *not a claim* — no check, counts as unanswered, so on `stop` it takes `stopped` and no `claim:` field. § Termination: the claim takes the qualifier "where no check ran at all, because the claim **named nothing checkable** or the round's check batch was full" — here "nothing checkable" means Design 5's no-repo-footprint case and yields the *opposite* disposition (qualifier plus a `claim:` field). An implementer reading :508–510 for the `stop` case can route an "I don't know" to `fact not established (operator claim, unverified)` with an empty `claim:` field, which contradicts D7's precedence ("`stopped` is reserved for a fact need nobody answered") and produces the exact hand-off shape Design 11's fallback (:594–596) exists to paper over. The sentence's own subject ("A fact request the operator **answered** in the stopping round") fences it for a careful reader, which is why this is P2 and not higher. The wording pre-dates the delta, but change 5 widened Design 1's non-claim category and made it the governing intake rule, so the collision is now load-bearing where it was incidental. Reading-gate item 9 quotes this very sentence.
**Suggested fix:** In § Design 7, use Design 5's own words: "…because the claim **named nothing in any file** or the round's check batch was full." Row 6's pins ("where no check ran at all", "where a check was dispatched for it", "is not among the abandoned", "blocks the hand-off") are untouched by that edit.

### F-3: The new disclosure says nothing is rendered for a missing check — Design 6 renders one
**Severity:** P3
**Where:** spec § Design 2 commentary (`:341–344`); § Deferred (`:905–908`) vs § Design 6 shipped blockquote (`:465–472`)
**Edge case:** A truncated claim that a question was gated on.
**What happens:** The disclosure states flatly: "nothing is rendered for a check, and nothing is rendered for a missing one, so re-answering the same `F<n>` is a path the operator can take only if they notice the item in the hand-off"; the § Deferred bullet repeats it ("instead of leaving the operator to spot the item in the hand-off"). Design 6 says that "once it is settled that no check will run for it" — which truncation settles at once — the gated question enters the **next** round's frontier "rendered with a one-line note giving the claim's text in its normalized form and its unverified status". So for a gated claim, something *is* rendered in the next round, before the hand-off, and the operator can re-answer then. The error is in the safe direction (it understates the operator's information and so overstates the cost of not folding), and both sentences are commentary, which is why this is P3 — but it is a new statement contradicting a section the delta did not touch, which is the failure mode this spec hit in every prior round, and `/spec-close` decomposes this paragraph as the recorded reason for the deferral.
**Suggested fix:** One clause in each: "…nothing is rendered for a missing one **except where a question was gated on it, which renders Design 6's unverified note**, so re-answering the same `F<n>` is a path the operator can take only where the claim gated a question or they notice the item in the hand-off." Mirror the exception in the § Deferred bullet.

### F-4: Change 4 replaced a correct attempt-1 anchor with one that starts mid-sentence
**Severity:** P3
**Where:** spec § Decisions D4 (`:117–118`) → `docs/specs/DONE/VHS-33/attempt-1/spec.md`
**Edge case:** Not an input edge — a citation the round-4 fold changed on a mistaken premise.
**What happens:** D4 now cites `attempt-1/spec.md:478–488`. In the archive file, rule 2 begins at **`:476`** ("2. **It rides the normal batch and counts against the same cap.**"); `:475` is the tail of rule 1; `:478` is the fragment "parallel batch, against the `question_cap` dispatch cap."; the overflow paragraph runs `:480–488`. The previous citation `:476–488` was the whole of rule 2 and was correct. The round-4 correctness finding that prompted the change asserts ":476–477 is the tail of rule 1" and "rule 2 begins at :478" — both false against the file — so the fold made a right anchor wrong. The relabel from *cross-batch* to *shared-batch* in the same change is correct (`attempt-1:482–483` "within a round's batch").
**Why the spec misses it:** The author folded another lens's stated line numbers without re-reading the archived file.
**Suggested fix:** Restore `attempt-1/spec.md:476–488` (or cite `:480–488` if only the overflow paragraph is meant). Correctness should be told its round-4 F-6(b) was wrong.

### F-5: A non-claim answer arriving for an `F<n>` that already carries a claim has no stated effect on the existing `claim:` field
**Severity:** P3
**Where:** spec § Design 1 (`:229–232` intake, `:240–244` replacement); § Design 11 (`:594–596`)
**Edge case:** `F5` answered in round 1 with a real claim, check not confirmed → Open with the qualifier and a `claim:` field. In round 2 the operator types `F5 I don't know`, or an answer the normalization empties.
**What happens:** Two readings, both defensible from the shipped text. (a) The later reply is "not a claim", so it replaces nothing: `F5` keeps the qualifier and the round-1 claim text, and the reply is merely counted as unanswered. (b) "a later answer to the same `F<n>` **replaces the claim**" applies to any later answer, so the claim is replaced by nothing: `F5` carries the qualifier with an empty `claim:` field — the precise shape Design 11's fallback dispositions ("An item carrying the qualifier with no `claim:` field, or an empty one, takes the plain … form"), which is the tell that the state is reachable and undispositioned in the primitive. Under (b) on a stopping round there is a further wobble against D7's precedence. The outcome is safe under both readings (the item stays Open, and the brief mapping has a fallback), so P3 — but the primitive and the caller disagree about whether the state exists, which is the same shape as round-4 F-5.
**Why the spec misses it:** Change 5 moved the emptiness test into the intake sentence that also carries the replacement rule; the two clauses of that paragraph were never composed against each other.
**Suggested fix:** Five words on the replacement clause: "…a later answer to the same `F<n>` **that is a claim** replaces the claim and gets its own check". A non-claim reply then leaves the item exactly as it stands, and Design 11's fallback stays purely defensive.

### F-6: § Deferred's preamble no longer describes its own contents
**Severity:** P3
**Where:** spec § Deferred (`:884–885`) vs the new bullet (`:905–913`)
**What happens:** The preamble reads "Round-1 findings that are valid, out of this brief's scope, and non-trivial — **filed rather than folded**". Change 11's bullet is a round-**4** finding, squarely **in** this brief's scope (it is about Design 2's own truncation rule), and explicitly **not filed** ("not filed, because the case needs the operator to answer more than `question_cap` claims in a single round"). Three of the preamble's four criteria fail. The last bullet already strained "filed" pre-delta; the new one breaks the round and scope criteria as well. `/spec-close` decomposes this section, where the preamble is what tells a reader why each bullet is there.
**Suggested fix:** Widen the preamble: "Findings that are valid but not folded — out of scope, or accepted as a bounded cost. Filed as tickets where a future run could hit them; noted here where the trigger is remote."

### F-7: Two phrases the round-4 fold added ship unpinned, and the checklist is the only gate
**Severity:** P3
**Where:** spec § Test plan rows 3 and 5 (`:670–694`, `:711–720`) vs `:366–367`, `:471`
**Edge case:** An implementer transcribes the blockquotes and drops a clause; `## Test command` is `N/A`, so the checklist *is* the `/ship-spec` gate.
**What happens:** Change 2, 5, 6's other clauses and change 9 are all covered by a pin or an adjacent one, but two fold-added phrases are asserted nowhere: Design 3's `"leaving the Open frontier if it was there"` (the whole of the F-6 fold — without it, the double-render into a brief's `## References` **and** `## Risks / decisions` that Design 4 forbids is back) and Design 6's `"in its normalized form"` (the whole of the F-7 fold). Both can be lost silently and the gate still passes.
**Suggested fix:** Add `"leaving the Open frontier if it was there"` to row 3's `**Two outcomes.**` pin list, and `"in its normalized form"` to row 5's `**A question the claim gated is rendered anyway.**` pin list. No new row.

### F-8: `:87`'s "hard truncation" phrase is a whole sentence, not the second half of one
**Severity:** P4
**Where:** spec § Design 2 commentary (`:315–321`) vs `skills/grilling/SKILL.md:87`
**What happens:** The new paragraph says the phrase "a hard truncation, not a soft target" "is the second half of a sentence whose first half is 'overflow carries to the next round'". In the file, `:87` reads "…; overflow carries to the next round. **This is a hard truncation, not a soft target.**" — two sentences, joined by an anaphoric "This". The conclusion drawn from it is correct; only the structural description is wrong, in a paragraph whose whole purpose is to correct a previous misuse of that same citation.
**Suggested fix:** "…its sentence 'This is a hard truncation, not a soft target' follows directly on 'overflow carries to the next round', so it means…".

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 5 | P4: 1

STATUS: GREEN
