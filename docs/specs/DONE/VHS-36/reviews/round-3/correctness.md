# Correctness Review — round 3

Grounding complete. Spec, brief, `CLAUDE.md`/`AGENTS.md` conventions, the Plane ticket (namespace `skills`, tag-exact hit — its description matches the brief), all four target files at `f4d9290` (still HEAD, `git rev-parse` confirmed), `docs/specs/DONE/VHS-33/spec.md` `## Test plan` rows 1–16, `docs/specs/DONE/VHS-33/attempt-1/spec.md:410–506`, the VHS-33 wiki decision page, and all three round-2 reviewer reports have been read. `git log` on the four touched files shows only the VHS-33 series (`c97d4ad`…`648f4ff`); nothing landed after the anchors were read.

**On the orchestrator's specific question:** the surplus rule is **not** attempt-1's overflow-ordering rule returning. Attempt-1 `:476–488` ranked verifications *against new fact needs inside one shared batch* ("new fact needs are dispatched before verifications, and verifications overflow first"), which is why it had to reach into § Bounds' three-key ordering. VHS-36's surplus rule orders only *within the checks' own separate batch* (`oldest F<n> first`), never against a rendered item, and `:87` stays byte-identical. Different construct. The three wiki quotes in § D7 are verbatim-accurate against `vigil-harbor-wiki/decisions/2026-09-07-vhs-33-the-hand-off-carries-ids-and-a-hollow-brief-is-a-success.md` (`:6`, `:62`, `:66`).

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | row 17 one-sentence rule fails items 3/6/8/10 | CLOSED | spec:710–736 — thirteen items; I mapped each to exactly one shipped sentence (item 1→`At once, on the answer:…`; 2→`An answer that asserts nothing checkable…`; 3→`In any round…replaces the claim…`; 4→`Dispatch the answers' checks…up to 2 × question_cap…`; 5→`Bound it as any fact dispatch is bounded…`; 6→`Pass the claim…as quoted data…`; 7→`**Not confirmed** —…`; 8→`The operator's answer travels in the claim: field…`; 9→X1; 10→`A check that never returns blocks the round it precedes…`; 11→`For F<n> items this displaces…`; 12→`Once a claim's check has resolved…`; 13→`If no further round is rendered…`). No two items collide. (See new F-1: item 9's sentence is itself wrong.) |
| correctness | F-2 (P2) | row 10 range `:84–87` | CLOSED | spec:664 now `:86–88`; verified `:86` default 3, `:87` default 7 + "questions and fact requests together", `:88` "brief altitude by default" |
| correctness | F-3 (P3) | `2 × question_cap` not shipped | CLOSED | spec:267 shipped "up to `2 × question_cap` dispatches in all"; commentary reworded at :291–294; pinned in row 3 (:593–594) |
| correctness | F-4 (P3) | § Scope eight-vs-nine | CLOSED | spec:27 list now has eight comma-items, matching the eight bold leads pinned in row 3 |
| correctness | F-5 (P3) | `:67` anchor | CLOSED | spec:244 now `:65–67`; verified `:65` defer, `:66` omitted, `:67` free-form |
| correctness | F-6 (P3) | answered-after-Open under resume lead | CLOSED | moved into Design 1 blockquote (spec:222–226) with a "Why … sits here" note at :250–254 |
| correctness | F-7 (P4) | row 12 / § Scope enumerations | CLOSED | row 12 (:683–687) now "seven … six … plus"; § Scope (:47–51) now lists `:123`/`:126`/`:131`/`:124` |
| correctness | F-8 (P3) | `claim:` omitted form | CLOSED | Design 8 (:455–459) "omitted **together with its leading `; `**"; row 4 (:610–612) |
| edge-cases | F-1 (P0) | check batch's shipped bound false; no overflow rule | CLOSED **in shipped text** | false clause gone from Design 2's blockquote; surplus rule at :266–268; Design 3 gains the sixth cause (:308–310); rationale at :281–289. *But the same false bound survives verbatim in § D4 — raised fresh as F-2 below, not as a re-open* |
| edge-cases | F-2 (P1) | gated question carries "unverified" when confirmed | CLOSED | spec:392–394 splits the branches |
| edge-cases | F-3 (P1) | `claim:` verbatim/unescaped | CLOSED | "verbatim" gone; spec:311–315 normalization; pinned in row 3 (:594–596) and row 4 (:608–609); rationale :326–333 |
| edge-cases | F-4 (P2) | omitted form unspecified | CLOSED | same as correctness F-8 |
| edge-cases | F-5 (P2) | `claim:` lost across a resume | CLOSED | spec:401 "keeping its `claim:` text"; row 5 pins "keeping its" (:628) |
| edge-cases | F-6 (P2) | second answer to same `F<n>` | CLOSED | spec:223–226 "a later answer to the same `F<n>` replaces the claim and gets its own check"; row 3 pins "replaces the claim" |
| edge-cases | F-7 (P2) | row 17 item 3 arithmetic | CLOSED | product now ships; row 17 item 4 answerable by the one sentence |
| conventions | F-1 (P2) | preamble strips bold from Design 10's new bullet | CLOSED | spec:182–188 scopes Design 10's new bullet to the shipped-with-bold group |
| conventions | F-2 (P2) | VHS-33 wiki § 3 invariant unnamed | CLOSED | spec:140–144 quotes it verbatim and names Design 2 as the narrowing; quote verified against the wiki page `:62` |
| conventions | F-3 (P2) | unbounded operator text in the pinned line | CLOSED | same as edge-cases F-3 |
| conventions | F-4 (P4) | row 3 awk label, row 10 range | CLOSED | :598–600 relabelled; :664 corrected |
| conventions | F-5 (P4) | row 12 count | CLOSED | :683–687 |

## Findings

### F-1: Design 7's shipped `stop` sentence asserts a check runs for *every* answered fact request — Design 5 and Design 2 both ship cases where none runs
**Severity:** P0
**Where:** spec § Design 7 blockquote (`VHS-36.spec.md:427–430`); contradicts § Design 5 blockquote (`:366–373`) and § Design 2 blockquote (`:266–268`); pinned by § Test plan row 17 item 9 (`:730`)
**Claim:** the sentence appended to `skills/grilling/SKILL.md:110`, shipped byte-for-byte:

> A fact request the operator answered in the stopping round is not among the abandoned: its check runs before the hand-off, so the claim resolves either to an established fact or to `fact not established (operator claim, unverified)`.

**Why this is wrong:** "its check runs before the hand-off" is false for two cases the spec itself enumerates, both of which land in the same file, in the section immediately above:

1. **No repo footprint.** Design 5 ships: "Where the claim names nothing in any file … **no check is dispatched**, and the claim is Open with the same `fact not established (operator claim, unverified)` qualifier" (`:366–370`). A no-footprint claim answered in the stopping round gets no check at all, yet § Termination tells the reader its check runs.
2. **Batch-cap surplus** (new this round). Design 2 ships: "Where the operator answered more claims than the cap allows, the surplus is checked in **the next round's check batch**" (`:266–268`). On `stop` there is no next round, so a surplus claim answered in the stopping round is never checked — which the spec acknowledges elsewhere, in Design 3's sixth not-confirmed cause: "**a claim the batch cap left unchecked when the interview ended**" (`:309–310`).

This is the same failure shape the round-2 edge-cases P0 raised and the author fixed by *deleting* a false justifying clause from a shipped paragraph ("bounded by the fact requests that round rendered, which the same cap already bounds"). The identical false-mechanism clause now sits in § Termination and was not re-scoped when the surplus rule landed. The consequence is worse than commentary drift because both texts ship into a single prose file that a model reads as instructions: § Fact-finding says "no check is dispatched", § Termination says "its check runs".

The claim's *disposition* is right in every case — the trailing disjunction ("resolves either to an established fact or to the qualifier") holds, and the precedence sentence ("a fact need the operator answered is never `stopped`") is unaffected. Only the mechanism clause is wrong.

Worse, checklist row 17 item 9 — "What happens to the claim on `stop`?" — is answerable by exactly this sentence and no other, so the `/ship-spec` gate (`## Test command` is `N/A`, so this checklist *is* the gate, spec:568–569) certifies the false sentence as the file's single source of truth for the `stop` case.
**Suggested fix:** Condition the clause in Design 7's shipped text, e.g. "…is not among the abandoned: where a check was dispatched for it, that check runs before the hand-off, and the claim resolves either to an established fact or to `fact not established (operator claim, unverified)` — as it does where the batch cap or a claim with no repo footprint left it unchecked." Then either leave row 17 item 9 as is (the revised sentence still answers it alone) or reword it to "What happens to a claim the operator answered in the stopping round?".

### F-2: § D4 still carries the false bound that was deleted from Design 2's shipped text, and its "deletes attempt 1's overflow-ordering rule" claim no longer holds
**Severity:** P1
**Where:** spec § D4 (`VHS-36.spec.md:96–104`); contradicted by § Design 2 commentary (`:281–289`) and § Design 2 blockquote (`:266–268`)
**Claim:** § D4, restating the brief's decision the spec says it honors:

> Not counted against the rendered-item cap; **the number of checks per round is bounded by the fact requests the previous round rendered.** This **deletes attempt 1's overflow-ordering rule and its last-round hole.**

**Why this is wrong:** Both halves are now false against this spec's own Design 2.

- The bound is refuted in terms, three pages later: "the operator may answer an `F<n>` that became an Open item in an earlier round, so the claims answered in one round are **not** bounded by that round's rendered fact requests — Open F-items accumulate to `(round_cap + 1) × question_cap`" (`:281–286`). That is the exact statement round-2 edge-cases F-1 raised as a P0 and the author fixed by removing it from the shipped paragraph — but the fix stopped at the blockquote and left the restatement in § Decisions carried forward. Verified against `skills/grilling/SKILL.md:90` ("A fact request the operator leaves unanswered twice becomes an Open item") and `:53` (accepts `F1 <answer>` with no restriction to the current round), which is what makes the bound false.
- Design 2 now ships an overflow rule ("the surplus is checked in the next round's check batch, oldest `F<n>` first", `:266–268`) and a narrow last-round hole (Design 3's sixth cause, `:309–310`). Attempt 1's *cross-batch ordering* rule is indeed gone — I verified against `docs/specs/DONE/VHS-33/attempt-1/spec.md:476–488`, which ranked verifications against new fact needs inside one shared batch — but "deletes … its last-round hole" is now only true for the ordinary case; attempt-1's rule-2 consequence ("a verification that overflows past the last rendered round renders `fact not established (operator claim, unverified)`", attempt-1 `:486–488`) is precisely what Design 3's sixth cause reinstates in reduced form.

§ Decisions carried forward is the spec's ledger of what it honors and where it deviates — it does exactly this bookkeeping elsewhere (D7's wiki-narrowing note at `:140–144`, D9's displacement note at `:158–161`). Leaving D4 unamended means the one brief decision the spec knowingly departs from is the one decision recorded as honored without qualification, and `/spec-close` would decompose the false bound into the decision layer.
**Suggested fix:** Amend D4 to record the deviation, e.g.: "Not counted against the rendered-item cap. The brief's further clause — that the checks per round are bounded by the fact requests the previous round rendered — does not hold: an operator may answer an `F<n>` that became an Open item in an earlier round, so Design 2 bounds the batch itself at `question_cap` and ships a surplus rule instead. Attempt 1's *cross-batch* ordering rule (its `:476–488`) is deleted; its overflow consequence survives only as Design 3's sixth not-confirmed cause."

### F-3: "The last-round hole is closed" over-states its own design, and disagrees with the paragraph eight lines above it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2, commentary (`VHS-36.spec.md:296–299`) vs the same section's "Why the surplus rule exists at all" (`:281–289`)
**Claim:** "Attempt 1 left a claim answered in the last rendered round unverified by construction — reachable in ordinary use under the defaults. Here that claim's check runs before the hand-off, **so the last round is not a special case.**"
**Why this is wrong:** With the surplus rule, a claim answered in the last rendered round *beyond `question_cap`* is again unverified by construction — the last round is a special case for exactly that slice, because it is the one round whose surplus has no "next round's check batch" to fall into. The adjacent commentary says so in the other direction ("A claim the cap never reaches before the interview ends is Open under the qualifier, which Design 3 lists among the not-confirmed causes", `:287–289`). Two commentary paragraphs in one Design section give a reader opposite impressions of whether the last round is special. Neither ships, so this is confusion rather than breakage — but it is the same unreconciled-fold pattern that produced F-1 and F-2.
**Suggested fix:** Narrow the sentence: "…so the last round is no longer a special case for any claim the check batch reaches. The one residue is a claim the batch cap left unchecked in the last rendered round; Design 3 gives it a stated outcome rather than an accidental one."

### F-4: Checklist row 10 is labelled "Supersedes" for three VHS-33 rows it wholly re-asserts
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 10 (`VHS-36.spec.md:657`)
**Claim:** "**Supersedes VHS-33 checklist rows 5, 7 and 8: still present verbatim.**"
**Why this is wrong:** The header contradicts its own body — "supersedes … still present verbatim" — and nothing in VHS-33 rows 5, 7 or 8 is in fact superseded. I checked each against `docs/specs/DONE/VHS-33/spec.md` `## Test plan`: row 5's clauses (guard sentence, `:70`→`:72` dispatch sentence, fork block, advisory sentence, bounds, worked-examples table, the three `###`, `empty-seed`, the `:23` resume contract) are all re-asserted unchanged, with two anchors correctly re-translated for post-VHS-33 numbering; row 7 (`seed` bullet, `grep -c 'ref:'` ≥ 7, callers-map sentence) and row 8 (`**Plain language.**`) likewise. The only supersession this spec makes is row 4's F-line clause (row 4, `:613–614`) and row 9 in part (`:649`), and both are labelled correctly. Row 5's trailing "Plus row 4 above" makes a transitive reading defensible, but the verb still mislabels a re-assertion.

This matters because the repo maintains a running supersede/re-assert ledger across VHS-32 → VHS-33 → VHS-36 (VHS-33 row 5 is itself "Supersedes VHS-32 checklist row 4"), and `/spec-close` decomposes it. A future spec reading "VHS-36 supersedes VHS-33 rows 5, 7 and 8" would conclude those pins no longer bind and stop carrying them.
**Suggested fix:** "10. **Re-asserts VHS-33 checklist rows 5, 7 and 8 verbatim** (row 5's own 'Plus row 4 above' clause is superseded by row 4 here; two anchors are re-translated for post-VHS-33 numbering)."

### F-5: The surplus rule presumes a "next round's check batch" that only exists if the next round produces answers
**Severity:** P3
**Where:** spec § Design 2 blockquote (`VHS-36.spec.md:266–268`)
**Claim:** "Where the operator answered more claims than the cap allows, the surplus is checked in the next round's check batch, oldest `F<n>` first."
**Why this is wrong:** The same paragraph defines the check batch as firing on *answers* ("Dispatch the answers' checks in one parallel batch"). If round *n* leaves surplus and round *n+1* answers only questions — no `F<n>` answers at all — it is not stated whether a check batch fires anyway to drain the surplus, or whether the surplus waits for a round in which some claim is answered. An implementer can read it either way; the second reading can strand a surplus claim across several rounds even though dispatch slots were idle. The final disposition is not at risk (Design 3's sixth cause covers a claim still unchecked when the interview ends), so this is timing clarity, not a hole.
**Suggested fix:** Two words: "the surplus is checked in the next round's check batch — which fires for surplus alone if no new claim was answered — oldest `F<n>` first."

### F-6: Two nits
**Severity:** P4
**Where:** spec § Design preamble (`:182–184`); § Test plan row 17 preamble (`:715–716`)
**Claim:** (a) "In Designs 1–6, **8**, 9, 11 and 12 … the blockquote is the shipped text byte-for-byte". (b) "two items may quote the same sentence only where noted."
**Why this is wrong:** (a) Design 8 has no blockquote — its `:128` replacement is a fenced code block (`:451–453`), and the rest of the section is prose. Listing it among the blockquote designs is harmless but inaccurate. (b) No item in the thirteen is annotated as sharing a sentence, and none needs to (I mapped all thirteen to distinct sentences), so the permission is vacuous — a reviewer running the row may hunt for the "noted" exception that does not exist.
**Suggested fix:** (a) Drop `8` from the list, or say "the blockquote or fenced line". (b) Delete the clause, or state "no two items may quote the same sentence."

## Summary
P0: 1 | P1: 1 | P2: 2 | P3: 1 | P4: 1

STATUS: RED P0=1 P1=1 P2=2 P3=1 P4=1
