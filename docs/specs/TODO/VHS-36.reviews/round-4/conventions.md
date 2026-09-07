# Conventions Review — round 4

Grounding done fresh: spec and brief re-read from disk; `AGENTS.md` read end to end (canonical) plus the machine-local `CLAUDE.md`; `skills/grilling/SKILL.md` re-anchored at `:45–160`; the VHS-33 wiki decision read in full; `docs/specs/DONE/VHS-33/spec.md` § Test plan enumerated (16 rows) for the ledger check; DONE specs grepped for abandoned-design commentary; VHS-38/39/40 retrieved live from Plane. Every claimed fold below was verified on disk.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 (P2) | § D4 carries the batch-bound premise Design 2 disproves | CLOSED | spec:107–117 — "**One clause of this decision does not hold, and the spec departs from it.**" quotes the brief's clause, names `:90`/`:53`/`(round_cap + 1) × question_cap` as why it fails, states what Design 2 does instead, and lists what of D4 still stands |
| conventions | F-2 (P2) | `claim:` claimed as the block's first operator-authored string | CLOSED | spec:360–368 — now "the first operator-authored string to enter it **under a machine-read field grammar**"; `:67`→`:124` named as a real pre-existing gap; § Deferred bullet at :861–867 files **VHS-40** (verified live in Plane, Backlog, description accurate) |
| conventions | F-3 (P2) | Designs 7/10 promise unconditionally that a stopping-round check runs | CLOSED | spec:474–480 ("where a check was dispatched for it that check runs before the hand-off… the same qualifier it takes where no check ran at all") and spec:546–549 (same conditional on the `:156` bullet); row 6 pins both phrases (:691–696) |
| conventions | F-4 (P4) | Row 17 preamble reserves an unused exception | CLOSED | spec:775 — "no two items may quote the same sentence" |
| correctness | F-1 (P0) | Design 7's `stop` sentence asserts a check for every answered request | CLOSED | same evidence as conventions F-3 |
| correctness | F-2 (P1) | D4 carries the false bound; "deletes the overflow rule" no longer holds | CLOSED | spec:112–117 — bounds the batch itself, and re-scopes the attempt-1 claim to the *cross-batch* rule (`attempt-1/spec.md:476–488`) with the last-round hole closed by identical truncation |
| correctness | F-3 (P2) | "The last-round hole is closed" over-states itself | CLOSED | spec:325–328 — "truncation applies identically to every round, and the one claim it drops is dropped for the same reason in round 1 as in the last" |
| correctness | F-4 (P2) | Row 10 labelled "Supersedes" for rows it re-asserts | CLOSED | spec:714–717 — "**Re-asserts** VHS-33 checklist rows 5, 7 and 8 verbatim — nothing in them is superseded here", with row 5's "Plus row 4 above" carved out |
| correctness | F-5 (P3) | Surplus presumes a next batch that may not exist | CLOSED (by removal) | no `surplus` / `next round's check batch` remains in the spec |
| correctness | F-6 (P4) | Design 8 listed among blockquote designs; row 17 clause | CLOSED | spec:195–199 — "in Design 8's **fenced line**"; row 17 clause dropped |
| edge-cases | F-1 (P0) | Surplus makes "its check runs before the hand-off" false, twice | CLOSED | same as conventions F-3 |
| edge-cases | F-2 (P0) | D4 asserts the abandoned bound and the deleted last-round hole | CLOSED | spec:107–117 |
| edge-cases | F-3 (P1) | Confirmed path unnormalized | CLOSED | spec:334–336 — "the operator's wording may stand as the fact text, **held to one line by the same normalization as the `claim:` field below**"; rationale at :370–378; row 3 pins "held to one line by the same normalization" |
| edge-cases | F-4 (P2) | Deferred check leaves the gated question in a third state | CLOSED | root removed, and Design 6 independently covers it: "or once it is settled that no check will run for it" (:433–435), which truncation makes true at once |
| edge-cases | F-5 (P2) | Replaced claim can occupy two slots of one batch | CLOSED (by removal) | with no queue, a claim is checked or Open within its own round; the replacement rule (:236–240) is the only path to a second check |
| edge-cases | F-6 (P2) | Queue has no batch to ride; "oldest `F<n>`" ranks the wrong thing | CLOSED (by removal) | — |
| edge-cases | F-7 (P2) | Length bound stated in a unit the spec defines as unbounded | CLOSED | spec:346 — "elided with an ellipsis past about 200 characters"; row 3 pins "past about 200 characters" |
| edge-cases | F-8 (P2) | No rule for a normalization-emptied `claim:`; marker exclusion mechanism | CLOSED | spec:343–347 — full marker list "removed", "where nothing checkable survives, the answer was not a claim"; Design 11 (:561–562) gives the absent/empty-field fallback |
| edge-cases | F-9 (P3) | Resume paragraph reads across a fresh answer | CLOSED | spec:447–449 — "unless the operator answers it again on the resumed round, which is a new claim under the rule above" |

All eight round-3 P0/P1s are closed, and no closed item reopened in a new location. The three findings below are new text from this round's queue→truncation replacement.

## Findings

### F-1: The shipped truncation sentence claims parity with the two caps in this file whose overflow carries — including the one it cites
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 shipped blockquote (`docs/specs/TODO/VHS-36.spec.md:274–282`), rationale at `:297–304`
**Convention violated:** The file's own established overflow idiom. Both existing caps in `skills/grilling/SKILL.md` overflow by **carrying**, and the new check cap overflows by **discarding** — an inversion the shipped text presents as parity.
**Evidence:** The two rules the shipped sentence points at:

- `skills/grilling/SKILL.md:76` (two paragraphs above the insertion point at `:79`, unedited and inside the `:72`–`:78` fenced region): *"Fact needs beyond the dispatch cap **carry to the next round's batch** by the ordering rule in § Bounds; if the interview ends first they reach the hand-off as Open with `unresolved because: fact not established`."*
- `skills/grilling/SKILL.md:87` (§ Bounds item 2, pinned byte-identical by rows 9 and 10): *"At most `question_cap` rendered items per round… **overflow carries to the next round. This is a hard truncation, not a soft target.**"*

The spec's shipped text:

> Dispatch the answers' checks in **one parallel batch, capped at `question_cap` dispatches**, **exactly as fact needs are dispatched above**… That cap is **a hard truncation, as the per-round item cap is**: … the batch takes them in `F<n>` order and **the rest are not checked at all** — each is Open under the qualifier at once, and **no check is ever carried to a later round**.

and its rationale: *"Truncation is this file's own idiom for a cap: § Bounds calls the per-round item cap 'a hard truncation, not a soft target'."* In the file, "a hard truncation, not a soft target" is the second half of a sentence whose first half is *"overflow carries to the next round"* — it means "this round renders no more than N; the rest wait", not "the rest are dropped". So the one phrase the spec cites as precedent for discarding is, in situ, precedent for carrying, and the sentence ships into a file where a reader meets the carrying definition three paragraphs later.

The **rule itself is the right call** — I am not asking for the queue back. Truncation is simpler, it removed four contradictions, and its recovery path is stated (the operator re-answers the same `F<n>`, Design 1). What is missing is the acknowledgment: the primitive now has two dispatch caps, side by side in one section, with opposite overflow behavior, and nothing tells a reader (or a model executing this prose) why a fact need gets a second round and a check does not.
**Suggested fix:** Replace the two parity clauses with the asymmetry, stated. In the shipped sentence: *"…capped at `question_cap` dispatches, and let that batch resolve… That cap truncates and does not carry — unlike a fact need beyond the dispatch cap above, which carries to the next round's batch, because a fact need has nobody to re-raise it while a truncated claim can be re-answered under the same `F<n>` in any later round: the batch takes them in `F<n>` order and the rest are not checked at all…"* Drop "as the per-round item cap is" and, in the rationale at `:301–304`, drop the § Bounds quotation (it argues the other way) and lean on the four contradictions already listed. Row 3's pinned phrase list (`:645`) needs updating alongside — see F-3.

---

### F-2: The abandoned-queue paragraph rests its case on `:80`, which says something else, and `/spec-close` decomposes it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 commentary (`docs/specs/TODO/VHS-36.spec.md:306–310`)
**Convention violated:** Rationale accuracy in the D/Design layer — the same class as my round-3 F-1. This commentary is what `/spec-close` turns into a wiki decision entry recording *why* the queue was rejected, and the repo's decision pages carry the reasoning forward verbatim (the VHS-33 page's "Rejected — …" subsections do exactly this).
**Evidence:** The spec says:

> It added cross-round state to a primitive that keeps none (`:80`: "No resume state is kept beyond `prior_summary`")

`skills/grilling/SKILL.md:80` in full: *"Facts, with their source paths, are carried into the hand-off. Retrieval-first… **No resume state is kept beyond `prior_summary`: if the session ends mid-interview, the caller re-runs.**"* That is a statement about state surviving a **session boundary**, not about state within one interview. Within an interview the primitive keeps cross-round state everywhere: overflowed fact needs carry to the next round's batch (`:76`), overflowed rendered items carry with a three-key order (`:87`), a fact request is tracked until it is *"unanswered twice"* (`:90`), `F1…Fn` and `Q1…Qn` are monotonic across the whole interview (`:48`), and carried-over/re-asked items rank first in the next round. A queue of pending checks would have been no more cross-round state than `:76`'s carried fact needs already are.

The paragraph's *real* reasons are the four contradictions listed immediately after it (`:310–313`), every one of which I verified against the round-3 edge-cases findings they answer (F-4, F-5, F-6, and the `stop` case behind F-1) — those are sound and sufficient on their own. The false premise is the first clause, and it is the clause a wiki decision entry would most likely quote.
**Suggested fix:** Delete the `:80` clause and open with the contradictions: *"A carry queue was drafted for this edge in review round 3 and abandoned in round 4. It produced four contradictions at once: …"* If a statelessness argument is wanted, make it the accurate narrower one — *"a queue would be the primitive's only cross-round structure whose contents are neither rendered nor numbered, so nothing in the hand-off would show it existed"* — which is true and is the actual asymmetry with `:76`'s carried fact needs (those keep an `F<n>` and can reach the block as Open items).

---

### F-3: Checklist row 3 pins a verbatim phrase the spec's own shipped text does not contain
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 3 (`docs/specs/TODO/VHS-36.spec.md:644–646`) vs § Design 2 shipped blockquote (`:281–283`)
**Convention violated:** This spec's byte-level pin discipline — every gate row is "a grep or a diff against the worktree" (`:620`), and with `## Test command` = `N/A` the checklist **is** the `/ship-spec` gate.
**Evidence:** Row 3 asserts the `**When the check runs.**` paragraph contains, *verbatim*, three phrases; the third is `"never carried to a later round"`. The shipped text reads *"and **no check is ever** carried to a later round."* Verified mechanically:

```
$ grep -c 'never carried to a later round' docs/specs/TODO/VHS-36.spec.md
0
```

The other two phrases in that clause (`"up to `2 × question_cap` dispatches in all"`, `"a hard truncation"`) are present, as are every phrase asserted in rows 4, 5, 6, 11, 12 and 13 — I checked each against its blockquote, so this is the single mismatch. An implementer who ships Design 2's blockquote byte-for-byte, as the Design preamble requires, then runs row 3 and gets an empty grep, is left choosing between two texts this spec both pins.
**Suggested fix:** Change the row's third phrase to `"is ever carried to a later round"` (or `"no check is ever carried"`), and fold the F-1 wording change into the same edit so the row's phrase list matches the shipped sentence once.

---

### F-4: Silent-addition scan — the discard-on-truncation rule is a spec-level addition the brief does not authorize (category c)
**Severity:** P3
**Where:** spec § Design 2 (`:279–286`), § D4 (`:107–117`)
**Convention violated:** None — this is the drift-check surfacing my lens is required to do, not a defect.
**Evidence:** Brief decision 4 (`brief.md:31`) authorizes "one read-only dispatch per claim when the answer arrives… not counted against the rendered-item cap" and assumes a bound that does not exist. It authorizes neither a queue nor a discard; both are spec-level answers to an edge the brief did not see. The spec now flags this explicitly — D4's departure paragraph names the failing clause and what replaces it — which makes it **category (c), addition with rationale**, not a silent (d). Recorded here so the human drift-check sees that the one brief clause this spec knowingly departs from is also the clause whose replacement changed shape between rounds 3 and 4 (queue → discard), and that the observable consequence is new: a claim the operator answered can now reach the hand-off unchecked while dispatch slots stood idle in every later round. The degradation is in the safe direction (Open under the qualifier, never a false established fact) and is recoverable by re-answering the same `F<n>`.
**Suggested fix:** None required. If the drift-check wants it visible past this spec, one clause in D4 — *"the cost accepted is that a truncated claim is never checked unless the operator answers it again"* — puts it in the section `/spec-close` decomposes.

## Notes on things that check out

- **Recording an abandoned design in the spec's commentary is the repo's practice**, and this spec's version is well within it. `docs/specs/DONE/VHS-29/spec.md` does it four times — `:47` ("An earlier draft shipped `log-crlf.md`; it cannot survive its own commit"), `:133` ("An earlier draft carried one with no caller… Dropped."), `:226`, `:290` ("It is withdrawn, because a partial pairing is worse than none"); `DONE/VHS-28/spec.md:455` and `DONE/VHS-33/attempt-1/spec.md:254` likewise. This spec already carried two ("An earlier draft said 'verbatim'", `:358`; "An earlier draft claimed the judgment was 'never load-bearing'", `:420`) through two green-ish rounds unremarked. The round-4 paragraph is the same idiom applied to a within-cycle abandonment — the only issue with it is F-2's premise, not its presence.
- **The truncation rule is not a premature abstraction.** It invents no knob (`question_cap` is reused exactly as `:76` reuses it), adds no registry/dispatcher, and is one clause closing a branch that would otherwise have no stated behavior. It is strictly less machinery than the queue it replaced. F-1 is about how it is *justified*, not whether it should exist.
- **The supersede/re-assert ledger is complete and now correctly labelled.** VHS-33's checklist has 16 rows (`DONE/VHS-33/spec.md:444–520`). VHS-36 supersedes 4 (in part, for one line) and 9 (in part), re-asserts 5, 6, 7, 8, 11, 12 and 13, and discharges 16 by inversion (row 14). The six unnamed VHS-33 rows are all re-made in substance without needing the label: row 1 → VHS-36 row 1, row 2 → row 2, row 10 and row 14 → row 15, row 15 → row 16. VHS-33 row 3 (`grep -c 'model:' → 0` on the three skill files) is the one pin restated in a weaker form — VHS-36 row 2 asserts only that *added* lines carry no `model:` — but with row 9 pinning hunks to five regions and rows 11/12/13 pinning the other files, the whole-file guarantee still follows. The reviewer agents' deliberate `model: opus` pins are untouched; `agents/` is fenced by rows 9 and 15 and no design proposes a model or effort change.
- **The three § Deferred (P2+) entries are all real, correctly attributed, and accurately described.** Verified live in Plane: **VHS-38** (Backlog, low — Open-frontier bound vs pending F-items; it is the ticket the VHS-33 wiki page's *"a tighter bound is its own ticket"* pointed at, closing my round-1 F-6), **VHS-39** (Backlog, medium — a Decision settled on an unverified claim reaching the brief unlabelled via `spec-brief:139`; edge-cases R1 F-10), **VHS-40** (Backlog, low — `:67`'s free-form answer reaching `:124` unnormalized; conventions R3 F-2). Each ticket names its origin reviewer and round, and each has a matching spec bullet. The fourth § Deferred item (edge-cases R1 F-15) is correctly marked "Not filed" with its accept-as-noise reasoning intact.
- **Harness-neutrality holds.** No proposed shipped line names `Explore`, `Agent`, `Skill`, `general-purpose`, or a model; Design 1 inherits `:72`'s parenthetical ("the same agent class… as any other fact dispatch") rather than restating a binding, and `skills/grill-me/SKILL.md:14`'s "or the equivalent in your host" is pinned by row 12. Row 2's `lint.py --strict` assertion remains satisfiable.
- **Unwrapped one-paragraph-per-line idiom respected** — the eight bold-lead paragraphs each ship as exactly one line, no bullet or heading is added to § Fact-finding, and row 3's `awk 'NR>=70 && NR<=100'` window and `grep -c '^###' → 3` still hold after the round-4 text changes (the insertion's line count is unchanged).
- **No backwards-compat shims, no duplicate helpers.** The `claim:` field's conditional omission restores the pre-change rendering because the field is conditional, not because anything is kept alive; nothing is renamed, re-exported, deprecated, or flag-gated. The confirmed path carries normalization *by reference* to the `claim:` rule rather than restating it — the single-source-of-truth move.
- **The VHS-33 wiki decision's three decompositions still stand** in D7's note (`:147–157`): the qualifier supersession of § 3's "Rejected — a cause qualifier", the `Revisit when:` `source: operator` trigger settled as a prohibition, and the narrowing of § 3's "no dispatch is ever active at `stop`". Truncation does not weaken the third — a check fired on the stopping round's answer is still active at `stop`, for up to `question_cap` of them.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
