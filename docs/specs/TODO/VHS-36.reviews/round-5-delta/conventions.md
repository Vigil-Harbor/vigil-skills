# Conventions Review — round 5 (delta)

Grounding done: DELTA.md read in full; only the spec sections it names re-read from disk; `skills/grilling/SKILL.md:60–102` re-read for the quotation and anchor checks; `docs/specs/DONE/VHS-33/spec.md` checklist rows 5/7/8 and `DONE/VHS-33/attempt-1/spec.md:474–490` read for the ledger and citation checks. Every phrase pinned by row 3 was grepped against the spec's own blockquotes.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 (P2) | Shipped truncation sentence claims parity with two caps that carry | **CLOSED** | spec:283–287 — "That cap is a hard truncation:" (the false "as the per-round item cap is" is gone) and the asymmetry now ships: "unlike a fact need beyond the dispatch cap above, which does carry". The misused § Bounds citation is gone (`grep -c "this file's own idiom"` → 0) and spec:315–324 states the inversion and its reason. The retained "exactly as fact needs are dispatched above" (:279) is about the batch mechanism, not overflow, and is accurate. |
| conventions | F-2 (P2) | Abandoned-queue paragraph rests on `:80` | **CLOSED** | `grep -c 'No resume state is kept'` → 0. spec:332–336 now carries the accurate narrower point ("the primitive's only cross-round structure whose contents are neither rendered nor numbered … where `:76`'s carried fact needs keep their `F<n>` and reach the block as Open items"), which matches `SKILL.md:76` verbatim. The four contradictions are intact and the paragraph keeps the VHS-29/VHS-28 abandoned-design idiom. |
| conventions | F-3 (P2) | Row 3 pins a phrase the shipped text lacks | **CLOSED** | spec:679 now pins "no check is ever carried to a later round" — present at :286–287. I re-grepped all eleven phrases row 3 pins (4 in **When the check runs.**, 4 in **Two outcomes.**, 3 in **Operator answers are claims.**, plus the gated-question phrase): all present, including the two new pins "ascending `F<n>` order (lowest first)" (:285) and "or an answer that the normalization below leaves empty" (:230). `grep -c 'never carried to a later round'` → 0 and `grep -c 'where nothing checkable survives'` → 0. |
| conventions | F-4 (P3) | Silent-addition scan: discard rule is a category (c) addition | **CLOSED** | spec:114–117 now carries exactly the clause I suggested, in the section `/spec-close` decomposes: "What the cap does remove is decision 4's implicit guarantee that *every* claim gets a dispatch … That is the accepted cost." |

**Verbatim check of change 3's new quotations** (asked for explicitly): both are accurate in substance. `SKILL.md:76` reads *"Fact needs beyond the dispatch cap carry to the next round's batch by the ordering rule in § Bounds"* — the spec's paraphrase at :316–317 is exact. `SKILL.md:87` reads *"…overflow carries to the next round. This is a hard truncation, not a soft target."* — both quoted strings are byte-present, but the spec's claim about how they sit in the line is wrong by one sentence boundary (F-3 below).

**Other lenses' folds, where they touch text I read:** changes 5/6 (intake emptiness test + the `an answer this leaves empty was not a claim, and the intake rule above governs it` tail) landed and are mutually consistent; change 7's "four boundaries … all four are stated" matches Design 6's new "in its normalized form" (change 8); change 9's Design 10 bullet, change 2's ordering direction, and change 10's row-10 anchors all landed as described.

## Findings

### F-1: The new "cost, stated plainly" paragraph denies a signal Design 6 renders
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 commentary (`docs/specs/TODO/VHS-36.spec.md:341–344`), repeated in § Deferred (`:905–908`)
**Convention violated:** Rationale accuracy in the layer `/spec-close` decomposes — the same class as my round-4 F-2. This paragraph and the § Deferred bullet are precisely the text a wiki decision entry will carry forward as *why the improvement was not taken*.
**Evidence:** The new paragraph says:

> The operator is **not** told which claims the cap dropped: nothing is rendered for a check, and nothing is rendered for a missing one, so re-answering the same `F<n>` is a path the operator can take only if they notice the item in the hand-off.

But Design 6, untouched by this round except for change 8, renders exactly such a signal (`:467–471`):

> Once a claim's check has resolved — **or once it is settled that no check will run for it** — the question waiting on it enters the next round's frontier: … where the claim was not confirmed, **rendered with a one-line note giving the claim's text in its normalized form and its unverified status**, so the operator decides on the same information the hand-off will carry.

Design 2 makes a truncated claim "Open under the qualifier **at once**" (`:286`), so "settled that no check will run for it" is true at once and the note fires in the *next rendered round*, not only in the hand-off. This is not an incidental overlap: my round-4 closure of edge-cases R3 F-4 rests on exactly this Design 6 clause. So the spec now relies on the note in one place and denies it in another. The denial is right in its narrow sense (the operator is never told *that the cap* dropped it, and an ungated F-item renders nothing), and the § Deferred entry's proposal — a note *naming* the truncated `F<n>` — is still a real improvement. What is wrong is the unqualified "nothing is rendered for a missing one" and "only if they notice the item in the hand-off".
**Suggested fix:** Qualify both spots with one clause. In `:341–344`: *"…nothing is rendered for a missing one — except where a question was gated on that `F<n>`, which Design 6 renders next round with the claim's text and its unverified status, so re-answering is a path the operator can take at once there and, for an ungated claim, only if they notice the item in the hand-off."* In the § Deferred bullet, change "instead of leaving the operator to spot the item in the hand-off" to "…which Design 6's gated-question note already gives for a claim some question waits on, but not for any other". No shipped text changes.

---

### F-2: Design 1's dispatch sentence still reads as the guarantee D4 now says the cap removes
**Severity:** P3
**Where:** spec § Design 1 shipped blockquote (`:232–235`) vs § D4 (`:114–117`)
**Convention violated:** None — this is the drift surface change 4 opened, recorded for the human check.
**Evidence:** Change 4 newly names what the cap takes away: *"decision 4's implicit guarantee that *every* claim gets a dispatch — a claim past the cap in its round receives none, ever."* The shipped sentence that creates that impression is unqualified: *"Otherwise dispatch one read-restricted exploration to check it…"* (`:232`). The cap arrives two paragraphs later in the shipped file. `SKILL.md:76` states its own general rule and its cap in the **same sentence** ("dispatch every fact need of a round in one parallel batch, capped at `question_cap` dispatches"), so the file's idiom is tighter than this. Row 17's reading gate is built to be answered by Design 2 for item 1 and item 7, so a careful reader composes them correctly; a model executing the prose might not.
**Suggested fix:** Optional and explicitly not required. If folded, three words in Design 1 — "dispatch one read-restricted exploration to check it, **subject to the batch cap below**" — with no re-pin needed (row 3's phrases are substrings and are unaffected). Weigh against change 11's own stated reason for not touching shipped behavior after the last full round; a cross-reference is not behavior, but it is still added shipped bytes no lens has read.

---

### F-3: The `:87` characterization describes two sentences as one
**Severity:** P4
**Where:** spec `:317–321`
**Convention violated:** This spec's quotation precision (my own round-4 wording, folded verbatim — the error is mine to correct).
**Evidence:** The spec says the phrase *"a hard truncation, not a soft target"* "is the second half of a sentence whose first half is 'overflow carries to the next round'". `SKILL.md:87` in full: *"…At most `question_cap` rendered items per round, **questions and fact requests together**; overflow carries to the next round. **This is a hard truncation, not a soft target.**"* They are two sentences; the second refers back with "This is". The argument the spec builds on it — that the phrase describes a cap whose overflow carries, not one that discards — is entirely correct and unaffected.
**Suggested fix:** "…its phrase 'a hard truncation, not a soft target' is the sentence immediately after 'overflow carries to the next round' and refers back to it, so it means…".

---

### F-4: The re-anchored attempt-1 citation starts mid-sentence
**Severity:** P4
**Where:** spec § D4 (`:117–118`)
**Convention violated:** This spec's byte-level anchor discipline. The change was made for accuracy (correctness R4 F-6b) and lands two lines off.
**Evidence:** `attempt-1/spec.md:478` is *"   parallel batch, against the `question_cap` dispatch cap."* — the tail of rule 2's lead sentence, which begins at `:476`. The shared-batch ordering rule itself is the paragraph `:480–488` (*"Overflow needs its own rule: `:85`'s ordering ranks carried-over items…"* through *"…not an accidental one."*); the whole rule-2 item is `:476–488`. The new range `:478–488` contains the rule but opens mid-sentence and belongs to neither unit. DELTA.md does not explain the range change, only the *shared-batch* rewording.
**Suggested fix:** `attempt-1/spec.md:480–488` if the citation means the ordering-rule paragraph (it does — "ordering rule" is the noun), or `:476–488` for the whole item.

---

### F-5: § Deferred's preamble no longer describes two of its five entries
**Severity:** P4
**Where:** spec `:884–885`
**Convention violated:** Section-preamble accuracy; widened by change 11.
**Evidence:** The preamble reads *"Round-1 findings that are valid, out of this brief's scope, and non-trivial — **filed** rather than folded"*. The list now holds VHS-40 (conventions **round 3** F-2), the new truncation-visibility bullet (edge-cases **round 4** F-3, explicitly **not filed**), and the F-15 bullet (**not filed**). One entry already mismatched before this round; change 11 makes two of five.
**Suggested fix:** *"Review findings that are valid, out of this brief's scope, and non-trivial — filed as tickets, or recorded here where the case is too rare to file:"*.

## Notes on things that check out

- **Both new records are in the repo's idiom and are accurate.** The abandoned-queue paragraph (`:326–336`) now reads as the VHS-29 / VHS-28 pattern does — the thing tried, when it was abandoned, and the concrete failures — with the false `:80` premise replaced by a claim I verified against `SKILL.md:76` and `:80`. The § Deferred not-filed bullet (`:905–913`) matches the shape of the existing F-15 not-filed bullet: reason not taken, the loss it accepts, and the condition that would make it worth filing. Both decompose cleanly.
- **D4 still reads as a faithful ledger.** `:96–103` is the brief's decision restated with its Design honors; `:105–120` is one clearly fenced departure paragraph naming the failing brief clause, why it fails (`:90`, `:53`, `(round_cap + 1) × question_cap`), what replaces it, what survives "in kind", and now the accepted cost. Nothing was added to D4 that the brief or the review record does not authorize.
- **Row 10's ledger edit is correct.** All four re-translations verified on disk: dispatch sentence `:70`→`:72`, "advisory… carries by silence" `:61`→`:63`, bounds `:84–86`→`:86–88`, worked-examples table `:94–98`→`:96–100` — a uniform +2 from VHS-33's `**Plain language.**` insertion. Four is also the complete set: row 5's other anchors (`:12`, `:23`, `:37–44`) and rows 7/8's (`:18`, `:53`, `:139`, no anchor) all sit before the insertion point and are unshifted, which I spot-checked line by line. The supersede/re-assert ledger is otherwise unchanged and still complete (supersedes VHS-33 rows 4 and 9 in part; re-asserts 5, 6, 7, 8, 11, 12, 13; discharges 16 by inversion).
- **Harness neutrality holds for every line added this round.** `grep -nE '\b(Explore|Agent|Skill|general-purpose)\b'` over the spec returns three hits, all pre-existing and legitimate: row 2's own assertion, and `:254`'s quotation of `SKILL.md:72`'s existing guard. `model:` appears once, inside row 2's assertion. No new shipped byte in changes 2, 5, 6, 8 or 9 names a tool, an agent class, or a model.
- **No shipped-paragraph count changed.** Changes 3, 4 and 11 add prose only outside the blockquotes; the eight bold-lead paragraphs row 3 pins are still eight, one line each, so row 3's `awk 'NR>=70 && NR<=100'` window and `grep -c '^###' → 3` are unaffected.
- **The truncation set is consistent across every section that names it:** Design 2 (`:283–287`), Design 3's not-confirmed list ("a claim the round's check batch was too full to take", `:371`), Design 10's fifth bullet ("or that the round's batch cap truncated", `:571`), row 6's `:110` conditional, and row 12's six-cause enumeration for `/grill-me`. Change 9 closed the last gap in that set.
- **No premature abstraction and no compat shim added this round.** The changes are all prose precision — a direction, an asymmetry, a cost, a cross-reference, and four anchors. Nothing new is introduced that a second callsite would justify.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 3

STATUS: GREEN
