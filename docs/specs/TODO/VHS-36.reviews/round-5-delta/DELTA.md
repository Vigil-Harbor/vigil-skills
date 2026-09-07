# VHS-36 — delta since the round-4 reviewers read the spec

Not a fifth review round. The three round-4 lenses read the spec, then the round-4
targeted rewrite (2e) was applied. This file is the complete changeset since that
read, for a delta-only verification pass.

Every change below is a fold of a round-4 finding. Nothing else in the spec moved.
`skills/grilling/SKILL.md` and the other three target files are **unchanged on
disk** — the spec is still unimplemented, and its anchors are still `f4d9290`.

---

## 1. Test plan row 3 — the two P0/P1 findings (correctness R4 F-1, edge-cases R4 F-1)

**Was:**
> "up to `2 × question_cap` dispatches in all", "a hard truncation", and "never
> carried to a later round"; the `**Two outcomes.**` paragraph contains "held to
> one line by the same normalization" (the confirmed path), "normalized to one
> line", "past about 200 characters", and "where nothing checkable survives"; the
> `**Operator answers are claims.**` paragraph contains "In any round" and
> "replaces the claim";

**Now:**
> "up to `2 × question_cap` dispatches in all", "a hard truncation", "ascending
> `F<n>` order (lowest first)", and "no check is ever carried to a later round";
> the `**Two outcomes.**` paragraph contains "held to one line by the same
> normalization" (the confirmed path), "normalized to one line", "past about 200
> characters", and "an answer this leaves empty was not a claim"; the
> `**Operator answers are claims.**` paragraph contains "In any round", "replaces
> the claim", and "or an answer that the normalization below leaves empty";

Two pins were stale against the shipped text (`never carried` vs `no check is ever
carried`; `where nothing checkable survives`, whose sentence was reworded by
change 6). Two pins were added for text added this round.

---

## 2. Design 2 shipped blockquote (edge-cases R4 F-2, conventions R4 F-1, correctness R4 F-2)

**Was:**
> …up to `2 × question_cap` dispatches in all. That cap is a hard truncation, as
> the per-round item cap is: where the operator answered more claims in one round
> than the cap allows, the batch takes them in `F<n>` order and the rest are not
> checked at all — each is Open under the qualifier at once, and no check is ever
> carried to a later round. Nothing is rendered for a check…

**Now:**
> …up to `2 × question_cap` dispatches in all. That cap is a hard truncation: where
> the operator answered more claims in one round than the cap allows, the batch
> takes them in ascending `F<n>` order (lowest first) and the rest are not checked
> at all — each is Open under the qualifier at once, and no check is ever carried to
> a later round, unlike a fact need beyond the dispatch cap above, which does carry.
> Nothing is rendered for a check…

Dropped the false parity with `:87` (whose "hard truncation" phrase belongs to a
sentence that *carries* overflow); shipped the ordering direction, which previously
existed only in non-shipping commentary; named the asymmetry with `:76`.

---

## 3. Design 2 commentary (conventions R4 F-1/F-2, correctness R4 F-2/F-4, edge-cases R4 F-2/F-3/F-4)

- **Ordering-key rationale.** "which needs neither tree depth nor blast radius,
  because a check is not a rendered item and unblocks nothing by being early" →
  replaced with a version that concedes the key is now a *selection* rule under
  truncation, not a delay: "What it decides under truncation is which claims are
  checked at all… The direction ships in the sentence itself, because an unstated
  direction would let two implementations drop two different sets of claims from
  the same transcript."
- **New paragraph** "**It is deliberately the opposite of the two caps beside it,
  and the shipped sentence says so.**" — quotes `:76` and `:87` in full, states
  that both carry, and gives the reason the check cap does not (a fact need has
  nobody to re-raise it; a truncated claim can be re-answered).
- **Removed** "Truncation is this file's own idiom for a cap: § Bounds calls the
  per-round item cap 'a hard truncation, not a soft target'." — the citation argued
  the opposite of what it was used for.
- **Queue-abandonment paragraph.** Removed the clause "It added cross-round state
  to a primitive that keeps none (`:80`: 'No resume state is kept beyond
  `prior_summary`')" — `:80` is about session boundaries, not within-interview
  state, and `:76`/`:87`/`:90`/`:48` all keep cross-round state. Replaced with the
  accurate narrower point: a queue would have been "the primitive's only cross-round
  structure whose contents are neither rendered nor numbered". The four
  contradictions it lists are unchanged.
- **New paragraph** "**The cost, stated plainly.**" — replaces "Truncation costs at
  most one check" (false; the drop is `answered − question_cap`, up to 21 under the
  defaults) with the real magnitude, states that the operator is **not** told which
  claims were dropped, and records that making truncation visible was considered and
  deliberately not folded (see change 11).
- **Last-round-hole paragraph:** "the one claim it drops" → "the claims it drops".

---

## 4. § Decisions D4 (correctness R4 F-3, F-6a, F-6b)

**Was:** "Everything else in decision 4 stands unchanged: dispatch at once, nothing
rendered for a check, no ordering extension at `:87`, and a hung check blocking the
hand-off. Attempt 1's *cross-batch* ordering rule (`attempt-1/spec.md:476–488`)…"

**Now:** "Everything else in decision 4 stands unchanged **in kind**: a check that
is dispatched fires at once… **What the cap does remove is decision 4's implicit
guarantee that *every* claim gets a dispatch — a claim past the cap in its round
receives none, ever, and Design 3 gives it a stated outcome instead. That is the
accepted cost.** Attempt 1's *shared-batch* ordering rule
(`attempt-1/spec.md:478–488`)…"

---

## 5. Design 1 shipped blockquote (edge-cases R4 F-5)

**Was:** "An answer that asserts nothing checkable — an explicit non-answer such as
"I don't know", or an empty body — is not a claim…"

**Now:** "An answer that asserts nothing checkable — an explicit non-answer such as
"I don't know", an empty body, **or an answer that the normalization below leaves
empty** — is not a claim…"

The emptiness test moves to **intake**, where its two consequences (no dispatch;
counts as unanswered under § Bounds) can actually be applied. It previously sat in
the render-time sentence, after the dispatch it was meant to prevent.

---

## 6. Design 3 shipped blockquote (edge-cases R4 F-5, F-6)

- **Confirmed branch:** "the fact goes to `### Facts established`, sourced by the
  `path:line` the *exploration* found" → "…sourced by the `path:line` the
  *exploration* found — **leaving the Open frontier if it was there, since one
  `F<n>` has one disposition** — and…". Closes the case where a re-answered Open
  `F<n>` confirms and could otherwise render in both sections.
- **Normalization tail:** "where nothing checkable survives, the answer was not a
  claim and the rule above applies" → "**an answer this leaves empty was not a
  claim, and the intake rule above governs it**" (pairs with change 5).

---

## 7. Design 3 commentary (edge-cases R4 F-7)

"one string across **three** boundaries — the exploration prompt, the established
fact, and the `claim:` field — and all three are stated" → "**four** boundaries …
**and the gated question's note in Design 6, which renders the same normalized
text** — and all four are stated."

---

## 8. Design 6 shipped blockquote (edge-cases R4 F-7)

"rendered with a one-line note giving the claim's text and its unverified status" →
"…giving the claim's text **in its normalized form** and its unverified status".

---

## 9. Design 10 shipped bullet (correctness R4 F-5, edge-cases R4 F-8)

"(a failed check, a check that could not be dispatched, or a claim with no repo
footprint)" → "(a failed check, a check that could not be dispatched **or that the
round's batch cap truncated**, or a claim with no repo footprint)".

---

## 10. Test plan row 10 (correctness R4 F-6c)

"and two anchors are re-translated for post-VHS-33 numbering" → "and **four**
anchors are re-translated for post-VHS-33 numbering: `:70`→`:72`, `:61`→`:63`,
`:84–86`→`:86–88`, `:94–98`→`:96–100`".

---

## 11. § Deferred (P2+) — new entry (edge-cases R4 F-3)

New bullet: **Telling the operator which claims the batch cap truncated.** Records
that a one-line note in the next rendered round would make Design 1's re-answer path
usable; not folded, because it adds a rendering behavior after the last review round
— which is how the round-3 carry queue went wrong — and the loss it mitigates is
bounded and safe. Not filed as a ticket; the case needs the operator to answer more
than `question_cap` claims in one round.

---

## Author's own verification already run

All 30 phrases pinned by Test plan rows 3, 4, 5, 6, 11, 12 and 13 were extracted and
matched mechanically against the reconstructed shipped text (blockquotes + Design 8's
fenced line, unwrapped). 30/30 present. That check is the author's, not a lens's.

---

# Addendum — folds applied after the three delta reviews

All three delta lenses returned **GREEN** (P0=0, P1=0 each). Both gate-blocking
round-4 findings — correctness F-1 (P1) and edge-cases F-1 (P0), the same row-3 pin
mismatch — were confirmed CLOSED by all three. The residue below was then folded.
These bytes have **not** been reviewed.

**Shipped text (4 changes):**

- **Design 2** — "more claims in one round" → "more claims **needing a dispatch** in
  one round". The cap is a dispatch cap, but the truncation set was counted in
  claims; a no-repo-footprint claim (Design 5, no dispatch) could consume a slot and
  push a checkable claim out. *(edge-cases delta F-1, P2)*
- **Design 7** — "because the claim named nothing **checkable**" → "named nothing
  **in any file**". "Nothing checkable" is Design 1's term for a non-claim, which
  takes the opposite disposition; Design 5's own words remove the collision.
  *(edge-cases delta F-2, P2)*
- **Design 1** — "dispatch one read-restricted exploration to check it**, subject to
  the batch cap below**". D4 now names the removed every-claim-gets-a-dispatch
  guarantee; the sentence that created that impression was unqualified.
  *(conventions delta F-2, P3)*
- **Design 1** — "a later answer to the same `F<n>` **that is itself a claim**
  replaces the claim … **A later reply that is not a claim leaves the item exactly
  as it stands.**" Closes the case where a non-claim reply arrives for an `F<n>`
  that already carries one. *(edge-cases delta F-5, P3)*

**Commentary and test plan (5 changes):**

- **Design 2 cost ¶** and the **§ Deferred bullet** — both said nothing is rendered
  for a missing check; Design 6 renders one for a *gated* claim. Both now carry the
  exception. *(conventions delta F-1 P2, edge-cases delta F-3 P3)*
- **Design 2 asymmetry ¶** — `:87`'s "hard truncation" phrase described as "the
  second half of a sentence"; it is a whole sentence referring back with "This is".
  *(all three lenses, P4)*
- **D4** — attempt-1 citation restored to `:476–488`. The round-4 change to
  `:478–488` acted on a correctness finding that was itself wrong; rule 2 opens at
  `:476`, verified on disk. *(all three lenses)*
- **§ Deferred preamble** — "Round-1 findings … filed rather than folded" described
  neither the round-3/round-4 entries nor the two not-filed ones. Widened.
  *(all three lenses)*
- **Test plan rows 3 and 5** — added the two fold-added phrases that shipped
  unpinned: `"leaving the Open frontier if it was there"` and `"in its normalized
  form"`. Without them the F-6 and F-7 folds could be dropped silently and the gate
  would still pass. *(edge-cases delta F-7, P3)*

**Author's verification:** all 34 phrases now pinned by rows 3, 4, 5, 6, 11, 12 and
13 were extracted and matched mechanically against the reconstructed shipped text.
34/34 present. Eight stale phrases confirmed absent.
