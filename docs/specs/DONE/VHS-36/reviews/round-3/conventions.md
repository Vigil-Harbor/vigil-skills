# Conventions Review — round 3

Grounding done fresh: spec and brief re-read from disk at `f4d9290`; `AGENTS.md` read end to end (canonical) plus the machine-local `CLAUDE.md`; wiki `decisions/2026-09-07-vhs-33-…` read in full; all four target files re-anchored (`skills/grilling/SKILL.md`, `skills/spec-brief/SKILL.md:138–143`, `skills/grill-me/SKILL.md:14,:19–22`, `docs/spec-workflow-reference.md:31,:35`); `lint.py` header read for R1/R2 behavior; all three round-2 reports read. Every claimed fold below was verified on disk, not taken on report.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Preamble mis-scopes Design 10's new bullet | CLOSED | spec:182–188 — Design 10's **new failure-mode bullet** now sits in the byte-for-byte group, `:156` amendment in the reader-only group; bullet ships with `- **Operator claim not checked**` (:492), matching row 8 (:645–647) |
| conventions | F-2 | VHS-33 wiki § 3 invariant falsified unnamed | CLOSED | spec:140–144 quotes "no dispatch is ever active at `stop`…", names Design 2 as the narrowing, and tells `/spec-close` to decompose **all three** |
| conventions | F-3 | `claim:` carried unbounded operator prose | CLOSED | shipped `**Two outcomes.**` (:313–315): "held to one line: whitespace collapsed to single spaces, inner double quotes rendered as single, elided with an ellipsis… never carrying the block's own `ref:` or `unresolved because:` markers"; row 3 and row 4 pin it |
| conventions | F-4 | Row 10 `:84–87`; row 3 awk label | CLOSED | row 10 now `:86–88` with the pre-`**Plain language.**` note (:663–665) — verified against the file (`:86` cap 3, `:87` cap 7 + "questions and fact requests together", `:88` brief altitude); row 3 relabelled (:598–600) |
| conventions | F-5 | Row 12 five-vs-six count | CLOSED | row 12 (:682–689) reads "all seven situations… Design 3's six not-confirmed causes… plus Design 5's no-dispatch case"; Design 3 ships six causes (:306–309); Design 12 commentary (:543–545) and its shipped bullet (:534–539) both say seven |
| correctness | F-1 | Row 17 compound items fail "one sentence" (P0) | CLOSED | row 17 is thirteen items (:710–736); items 9/10 split `stop` from hung check, 5/6 split paths from quoted-data, 12/13 split render from exit reason; each maps to one shipped sentence — checked individually against Designs 1–3, 6, 7 |
| correctness | F-2 | Row 10 `:84–87` | CLOSED | as above |
| correctness | F-3 | `2 × question_cap` not shipped | CLOSED | shipped (:269): "a round makes at most two batches, up to `2 × question_cap` dispatches in all"; commentary re-worded (:291–294); row 3 pins the phrase |
| correctness | F-4 | § Scope "eight" vs nine topics | CLOSED | spec:27 now lists eight comma-items (topics 1+2 joined) |
| correctness | F-5 | `:67` anchor for defer/omitted/free-form | CLOSED | spec:244 now `:65–67` |
| correctness | F-6 | Late-answer rule shipped under the resume lead | CLOSED | moved into `**Operator answers are claims.**` (:222–226) with a placement rationale (:250–254) |
| correctness | F-7 | Row 12 / § Scope enumerations | CLOSED | row 12 as above; § Scope (:47–51) now enumerates `:123`/`:126`/`:131` and `:124` |
| correctness | F-8 | Omitted `claim:` form not pinned | CLOSED | Design 8 (:455–459) "omitted **together with its leading `; `**… `…| stopped>. ref: <…>`"; row 4 restates it (:610–612) |
| edge-cases | F-1 | Batch bound contradicted; no overflow rule (P0) | CLOSED | shipped surplus rule (:266–268) "the surplus is checked in the next round's check batch, oldest `F<n>` first"; Design 3 adds "a claim the batch cap left unchecked when the interview ended" as a not-confirmed cause (:308–309). *(A residue of the falsified premise survives in § D4 — new F-1 below, distinct location, does not reopen this)* |
| edge-cases | F-2 | Gated question noted "unverified" when confirmed (P1) | CLOSED | shipped (:389–393) splits the branches: "rendered as any other question where the check confirmed, since the fact is then established, and, where it did not confirm, rendered with a one-line note…" |
| edge-cases | F-3 | `claim:` unescaped into a parsed contract (P1) | CLOSED | same normalization clause as conventions F-3; rationale at :326–333. *(Its "first operator-authored string" premise is false — new F-2 below, distinct root)* |
| edge-cases | F-4 | Omitted form unspecified | CLOSED | as correctness F-8 |
| edge-cases | F-5 | `claim:` text lost across a resume | CLOSED | shipped `**Across a resume.**` (:400–402) "keeping its `claim:` text"; row 5 pins "keeping its" |
| edge-cases | F-6 | Second answer to the same `F<n>` | CLOSED | shipped (:223–226) "a later answer to the same `F<n>` replaces the claim and gets its own check — which is not a retry, because…"; row 3 pins "replaces the claim"; row 17 item 3 |
| edge-cases | F-7 | Row 17 item 3 needs arithmetic | CLOSED | product now ships; row 17 item 4 answerable from one sentence |

All five of my round-2 findings and all three other-lens P0/P1s are closed on disk. Two new findings below share roots with closed items but sit in different text.

## Findings

### F-1: § D4 still carries the batch-bound premise that Design 2 disproves, unflagged
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions carried forward, D4 (`docs/specs/TODO/VHS-36.spec.md:98–99`) vs § Design 2 commentary (`:281–289`)
**Convention violated:** The spec's own displacement-naming idiom — everywhere else it departs from a carried rule it names the departure in the departed rule's terms: `:110–113` (D5 "displaces `:78`'s failed-dispatch carry"), `:156–161` (D9 "**displaces** the resume contract's clause"), `:140–144` (D7 "Design 2 narrows it"). This is the repo's decision-layer bookkeeping practice — VHS-33's wiki page does the same for VHS-32 § 5 — and `/spec-close` decomposes the D-section.
**Evidence:** D4 reads:

> Not counted against the rendered-item cap; the number of checks per round is bounded by the fact requests the previous round rendered.

Design 2's own commentary states the opposite as the reason the surplus rule exists (`:283–285`):

> A round renders at most `question_cap` items, but the operator may answer an `F<n>` that became an Open item in an earlier round, so the claims answered in one round are **not** bounded by that round's rendered fact requests — Open F-items accumulate to `(round_cap + 1) × question_cap`.

This is the exact premise edge-cases round-2 F-1 raised a P0 against. The fold corrected the Design and left the premise standing in the section that records what the brief decided. The brief's decision 4 does carry that clause verbatim (`brief.md:31`), so this is faithful carrying of a clause the spec then disproves — which is precisely the case the spec's idiom says to name. Nothing ships from D4, so no wrong code results; the cost is that the spec hands `/spec-close` a decision record with a false rationale, and a reader who stops at D4 gets the pre-round-3 model of the bound.
**Suggested fix:** One clause on D4, e.g.: *"…before the hand-off if that was the last rendered round. Not counted against the rendered-item cap. The brief's clause 'bounded by the fact requests the previous round rendered' does not hold — an already-Open `F<n>` can be answered in any later round (Design 2's surplus rationale) — so the batch cap is a real edge and Design 2 ships the surplus rule for it. The decision's operative content is unchanged: dispatch at once, nothing rendered, and no ordering extension at § Bounds `:87`."*

---

### F-2: Design 3's rationale claims `claim:` is the block's first operator-authored string; `:67`'s free-form answer already reaches `:124`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3, "Why the `claim:` field is normalized rather than verbatim" (`:326–333`), specifically `:328–329`
**Convention violated:** Reuse / single-source-of-truth — a spec that adds a rule for one channel must not assert the structurally identical sibling channel does not exist; and rationale accuracy, since this paragraph is what `/spec-close` will decompose into the wiki as *why* the field is normalized.
**Evidence:** The spec says:

> The hand-off is a one-item-per-line contract three callers parse (`:139`), and the claim is the first *operator-authored* string ever to enter it

`skills/grilling/SKILL.md:67` already routes operator prose into the block:

> **Free-form** (neither a rendered branch letter, `defer`, nor `stop`): record it **verbatim** as the settled decision if it satisfies the altitude fence… it *replaces* the fork with the operator's answer.

and `:124` — the Settled line inside the same pinned fence — is:

> `1. **<decision title>** (Q<n>) — chose <A/B/free-form answer>: <one line>. Facts relied on: <F-ids or "none">. ref: <id>[, <id>…] | none`

So an operator's free-form answer lands in `:124`'s `chose` slot, recorded verbatim, on a line `/spec-brief` maps positionally (`:139`, and `skills/spec-brief/SKILL.md:139`) — with no newline, quote, or length rule anywhere. The normalization Design 3 ships is right, and the *dispatch*-side version of the claim ("the first operator-authored string to cross into one", `:236–240`) is true; only the block-side "first ever" is false. Round-2 edge-cases F-3 asserted the same thing ("never reaches the block verbatim — it is recorded as a settled decision the primitive rewrites"), which `:67` and `:124` do not support. The practical cost: the spec adds a rule for one of two identical channels while asserting the other is absent, so the gap is neither fixed nor deferred, and the wiki inherits the wrong reason.
**Suggested fix:** Reword `:328–329` to the true, still-sufficient claim — *"the claim is the first operator-authored string to enter the block under a machine-read field grammar, between `unresolved because:` and `ref:`"* — and add one § Deferred (P2+) bullet: *"`:67`'s free-form answer already reaches `:124`'s `chose` slot verbatim with no normalization rule; out of this brief's scope (the Settled line is untouched here), filed as VHS-nn."* Keeps Design 3's fence and shipped text unchanged.

---

### F-3: Designs 7 and 10 promise unconditionally that a stopping-round answer's check runs before the hand-off; the new surplus rule exempts some
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 shipped text (`:427–430`) and § Design 10's `:156` amendment (`:499–501`), vs § Design 2 shipped text (`:266–268`)
**Convention violated:** The spec's own one-source-of-truth rule for the precedence/`stop` story (`:434–437`: "stated **once**, here, where `stopped` is defined… § Failure modes points at it rather than restating the reasoning") — the single statement now over-claims relative to a rule added in a different Design this round.
**Evidence:** Design 7 ships:

> A fact request the operator answered in the stopping round is not among the abandoned: its check runs before the hand-off, so the claim resolves either to an established fact or to `fact not established (operator claim, unverified)`.

Design 2 ships the surplus rule: checks are "capped at `question_cap` dispatches", and beyond that "the surplus is checked in **the next round's check batch**". On `stop` there is no next round, so a surplus claim's check does *not* run before the hand-off. Design 3 does cover the disposition ("a claim the batch cap left unchecked when the interview ended" → the qualifier), so the sentence's *conclusion* holds and no wrong behavior follows — but its stated mechanism is false for that sub-case, and it is the sentence row 17 item 9 makes a reader quote. The same over-claim is mirrored at `:499–501` ("its check runs before the hand-off"). The D7 wiki note (`:141–143`) inherits it: "a check fired on the stopping round's answer *is* active at `stop`" is true of at most `question_cap` of them.
**Suggested fix:** Four words in both shipped sentences, e.g. Design 7: *"…is not among the abandoned: its check runs before the hand-off, **or, where the batch cap left it unchecked, it resolves under the qualifier all the same** — so the claim resolves either to an established fact or to `fact not established (operator claim, unverified)`."* Mirror at `:156` with *"— its check runs before the hand-off unless the batch cap left it unchecked, and a check that never returns blocks it."*

---

### F-4: Row 17's preamble reserves an exception it never uses
**Severity:** P4
**Where:** spec § Test plan row 17 preamble (`:715–716`)
**Convention violated:** Gate rows must be unambiguously satisfiable — the same class round 1 and round 2 both flagged on this row (correctness R1 F-6, R2 F-1).
**Evidence:** The preamble ends *"…two items may quote the same sentence only where noted."* No item below carries such a note, and I checked all thirteen against the shipped blockquotes — each maps to a distinct sentence. A reviewer running the row looks for a marker that does not exist.
**Suggested fix:** Drop the clause, or make it a flat prohibition: *"no two items may quote the same sentence."*

## Notes on things that check out

- **The surplus rule is not a re-creation of attempt 1's deleted construct.** Attempt 1's rule ranked *verifications against new fact needs inside one shared batch* and had to extend § Bounds' three-key ordering to rank a non-rendered item. The new rule is a one-key overflow order (`oldest F<n> first`) inside a check-only batch; `:87` is pinned byte-identical (rows 9 and 10) and the spec argues the distinction explicitly at `:272–279`. It is not premature abstraction either — it is one clause closing a branch that had no stated behavior, and it invents no new knob: `question_cap` is reused as a dispatch cap exactly as `:76` already does.
- **`2 × question_cap` introduces no new bound.** It states a derived quantity in the shipped text so the reading gate needs no arithmetic; § Bounds' "Three bounds, and nothing else, end the interview" is untouched, and a dispatch budget is not an interview-ending bound.
- **Harness-neutrality holds.** No proposed shipped line names `Explore`, `Agent`, `Skill`, `general-purpose`, or a model; Design 1 inherits `:72`'s parenthetical ("the same agent class… as any other fact dispatch") rather than restating a binding. `lint.py` R2 flags only `mcp__*` identifiers (docstring limitation 1), so row 1's exit-0 / two-WARN assertion is satisfiable. `skills/grill-me/SKILL.md:14`'s "or the equivalent in your host" parenthetical is pinned byte-identical by row 12.
- **Reviewer agents and the model/effort dial untouched.** `agents/` is fenced by rows 9 and 15; row 2 additionally asserts no added line contains `model:`.
- **No backwards-compat shims.** The `claim:` omission rule restores the pre-change rendering because the field is conditional, not because anything is being kept alive for compatibility. Nothing renamed, re-exported, deprecated, or flag-gated.
- **Silent-addition scan (category d): none.** This round's three additions are all category (c) with named rationale — the surplus rule (`:281–289`), the `2 × question_cap` budget (`:291–294`), and the thirteen-item gate (a test-plan mechanic, not a design commitment). F-1 above is a stale premise, not an unauthorized addition.
- **Design 2's citation of `(round_cap + 1) × question_cap` survives VHS-38.** The spec files that bound as suspect for *undercounting* pending F-items (`:790–794`); if it undercounts, more Open F-items exist than cited, which strengthens rather than weakens the surplus rule's necessity. No contradiction.
- **Anchors re-verified at `f4d9290`.** `skills/spec-brief/SKILL.md:139–142` (Design 11's blockquote reproduces `:140` faithfully; `:141`/`:142` carry the `path:line` Scope gate and the References mapping the spec relies on), `skills/grill-me/SKILL.md:14`, `:19–22` (three bullets today), `docs/spec-workflow-reference.md:31`, `:35`. Row 3's post-edit `awk 'NR>=70 && NR<=100'` window is correct: the eight-paragraph run adds ~16 lines, putting `## Bounds` at post-edit `:98`, and § Bounds numbers `1./2./3.` so the window yields `grep -c '^- '` → 0 either way.
- **The VHS-33 supersede/re-assert ledger remains complete**, and D7's wiki note now hands `/spec-close` all three decompositions (the qualifier supersession, the `source: operator` Revisit-when trigger settled as a prohibition, and the § 3 "no dispatch is ever active at `stop`" narrowing).

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 0 | P4: 1

STATUS: GREEN
