# VHS-36 — grilling: operator-supplied facts are claims to verify (split from VHS-33)

**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-09-07 · **Plane:** VHS-36 (6ee19fa5-040c-43f4-98c5-23c91f815d4c, Backlog)
**Origin:** Split out of VHS-33 on 2026-09-06 after that spec's first `/spec-cycle` attempt ran red through four rounds (gate trajectory 12 → 3 → 5 → 6); the round-3 and round-4 P0s clustered under its Design 3, which implemented this item. VHS-33 shipped the hand-off shape changes alone (PR #27, `464303f`, 2026-09-07): `ref:` caller ids, `F<n>` Open items, the `fence-empty` token, the plain-language rule. This ticket carries the operator-claim rule, and — the lesson of attempt 1 — puts the fact-finding dispatch rules for verification **in** scope. The second half of CodeRabbit thread 3945500860 on PR #26 closes against it.

## Problem

The grilling primitive's fact-finding section lets the operator answer a fact request directly (`F1 <answer>`). The hand-off block's Facts established section requires `source: <path:line>`. An operator-supplied fact has no path, so the template has no legal form for it (CodeRabbit thread 3945500860 on PR #26, second half). Today such a fact rides through as an Open item carrying `unresolved because: fact not established` — since VHS-33, an `F<n>` Open item rather than a question.

The VHS-33 brief listed "the fact-finding dispatch rules" as out of scope, but the carried decision that a claim is verified by exploration *is* a dispatch rule. Attempt 1's spec had to invent three rules on when a verification runs (last-rendered-round, batch ordering against new fact needs, refuted-versus-partially-confirmed qualifiers) and a resume rule for Open F-items carrying a qualifier; reviewers found contradictions in each across rounds 3 and 4. Attempt 1 also left one question open (edge-cases R2 F-11): an operator fact that is true but not repo-checkable has no path at all under these decisions.

## Why it matters

An unchecked operator claim becomes an axiom every downstream lens trusts: `/spec-cycle`'s reviewers treat the brief as authority, so a wrong fact in the brief is invisible to review and surfaces as a P0 against the spec, or ships. The operator has been wrong before. The hand-off block is a verbatim contract three callers parse, so the legal form for a claim — established, open, or labelled — has to be stated in the primitive once, with the timing rules that attempt 1 showed cannot be left to the spec author.

## Scope (verified against current files, 2026-09-07)

| Path | Current | Change |
|---|---|---|
| `skills/grilling/SKILL.md` | § Fact-finding `:70–79` — one parallel batch per round capped at `question_cap` before rendering; a failed dispatch is carried as an `ℹ️` fact request next round; a never-returning dispatch blocks its round (`:74–76`). Per-round input line `:53` accepts `F1 <answer>`. Hand-off `:128` Open F-item reason set `<fact not established \| stopped>`; `:132` `- F1 — <fact> (source: <path:line>)`. § What this skill never does `:141`; § Failure modes `:151–156` | Verification rule (decisions 1–2): an operator answer is a claim, dispatched at once to one read-only check (decision 4), never retried (decision 5), two outcomes (decision 6); the qualifier `fact not established (operator claim, unverified)` as a third reason value with its precedence over `stopped` (decision 7); resume treatment (decision 9); a blocked question renders anyway (decision 10); "never writes `source: operator`" under § What this skill never does; the non-repo-checkable degradation named (decision 3). The `:53` input line is unchanged — the claim/verification distinction is the primitive's business, not a new operator step |
| `skills/spec-brief/SKILL.md` | Phase 4 `:140` maps an `F<n>` Open item to `<fact needed> — not established; spec author pins this`; `:141` a Scope row needs a `path:line`-backed fact; `:142` Facts established → References with `path:line` | `:140` gains the unverified-claim form `<fact needed> — operator claims "<answer>", unverified; spec author pins this` (decision 8); a confirmed claim reaches References through `:142` unchanged, sourced by the exploration's `path:line`, never a Scope row without one |
| `skills/grill-me/SKILL.md` | § Failure modes `:19–22` — three bullets: nested skill unavailable, `empty-seed`, `fence-empty` | A fourth bullet naming the degradation: a claim the repo cannot check (no read-only agent class, or a fact with no repo footprint) stays Open and labelled; the summary is delivered as usual (decision 3) |
| `docs/spec-workflow-reference.md` | `:31` facts are the agent's job; with no read-only class the primitive renders a request. `:35` hand-off paraphrase (unresolved questions and unestablished facts, sources, `ref:`) | Paraphrase names the claim rule: an operator's answer to a fact request is checked read-only before it counts as a fact, and an unchecked one reaches the brief labelled |

## Decisions carried forward

1. **An operator-supplied fact is a claim to verify, not a fact** (carried from the VHS-33 interview, Q3, operator's own answer, 2026-09-06) — the primitive checks the claim with a read-only exploration; a confirmed claim is established with the found `path:line` as its source; an unconfirmed claim stays open; the operator never hunts for paths. Rationale: the operator has been wrong before, and an unchecked claim becomes an axiom every downstream lens trusts.
2. **Unverifiable operator claims stay open** (carried, Q8) — where the host has no read-only agent class, the claim is open as `fact not established (operator claim, unverified)`. `source: operator` is never a legal established source.
3. **Non-repo-checkable claims stay Open; no new source class** (Q1) — a claim with no repo footprint (a runner OS, a plan tier) is an Open F-item, the brief lists it under Risks for the spec author, and `/grill-me` documents the degradation in its failure modes. The hand-off block gains no section: a label is not a fact and could not back a Scope row anyway.
4. **Verification runs at once on the operator's answer** (Q2) — one read-only dispatch per claim when the answer arrives, before the next round is rendered, or before the hand-off if that was the last rendered round. It is not counted against the rendered-item cap, because nothing is rendered for it; the number of verifications per round is bounded by the fact requests rendered in the round before. This deletes attempt 1's overflow-ordering rule and its last-round hole. A hung verification blocks the hand-off, the same risk the primitive already accepts for any dispatch.
5. **A failed verification is never retried and the operator is never re-asked** (Q3) — error, empty return, or `not found`: the claim stays Open as `fact not established (operator claim, unverified)`. Re-asking is right when nobody has answered and wrong when the operator already has; the brief still carries the claim for the spec author to check by hand.
6. **Two verification outcomes** (Q4) — confirmed (established, sourced by the `path:line` the exploration found; the operator's wording may be kept as the fact text) or not confirmed (Open). If the exploration finds contrary or different evidence, that evidence becomes its own established fact under a fresh `F<n>` with its own `path:line`, and the claim stays Open. Refutation is conveyed by an established fact beside an open claim; partial confirmation collapses to not confirmed.
7. **The qualifier is a third reason value and survives every exit** (Q5) — the Open F-item reason set becomes `<fact not established | fact not established (operator claim, unverified) | stopped>`. Precedence: a claim the operator answered is never `stopped`; `stopped` is reserved for a fact need nobody answered before the interview ended. This is the one line of the VHS-33-pinned hand-off block that changes.
8. **The brief carries the claim text, labelled** (Q6) — `/spec-brief` Phase 4 maps an unverified claim to `<fact needed> — operator claims "<answer>", unverified; spec author pins this`. Labelled, the claim is a lead for the spec author; a confirmed claim reaches References like any fact.
9. **Open claims carry over a revise un-redispatched** (Q7) — on a resume from `prior_summary`, every Open F-item carries over as Open and is not re-dispatched, qualifier or not, exactly as established facts already do under the resume contract.
10. **A question blocked on a claim that did not verify renders anyway** (Q8) — the operator answered the fact request; the question it gated is rendered with the fact still Open and labelled beside the decision. `blocked-on: F<n>` is for a fact that is still coming, not one that failed to check out; otherwise decision 3's accepted degradation would stall the interview.

## Done when

- The primitive states the verification rule and the unverifiable-claim rule, with the dispatch rules for when a verification runs.
- `/spec-brief` Phase 4 maps verified operator claims; `/grill-me` names the degradation.
- `lint.py --strict` reports zero ERROR and no new `missing-requires` WARN; `sync.py status` clean; `sync.py push` round-trips byte-for-byte.
- PR #26 thread 3945500860 (second half) can be closed against the merged change.

## Out of scope

- `/spec-cycle` 2f-i (Q9) — it seeds the primitive with findings and maps only Settled and Open items, never Facts; it inherits the verification rule from the primitive without an edit. `skills/spec-cycle/SKILL.md` is fenced.
- A non-repo source class or any new hand-off section (decision 3).
- Retrying a failed verification, or re-asking the operator for an answered fact (decision 5).
- A third or fourth verification disposition (`refuted`, `partially confirmed`) or a reason value that carries evidence (decision 6).
- Carried fences from VHS-33: the three bounds, the fork form, the advisory-recommendation rule; the size-bound sentence `skills/grilling/SKILL.md:137` byte-identical; `docs/specs/DONE/` never edited. The VHS-36 spec re-asserts the VHS-33 checklist rows its one changed line (decision 7) supersedes, as VHS-33 did for VHS-32.
- The per-round input syntax at `skills/grilling/SKILL.md:53` — `F1 <answer>` is unchanged; the operator performs no new step.

## Scale

**Factor:** no

## Risks / decisions

_(none open — the interview settled every item it asked; the spec author pins implementation detail only: the verification prompt's bound, the fresh-`F<n>` numbering for contrary evidence, and the exact precedence sentence)_

## References

- `skills/grilling/SKILL.md:74–76` — fact needs dispatched in one parallel batch per round, capped at `question_cap`, before the round renders; failed dispatch carried as an `ℹ️` request; a never-returning dispatch blocks its round.
- `skills/grilling/SKILL.md:128`, `:132` — Open F-item form `**F<n> — <fact needed>** — unresolved because: <fact not established | stopped>`; established form `- F1 — <fact> (source: <path:line>)`.
- `skills/spec-brief/SKILL.md:140–142` — F-item → Risks mapping; Scope rows need a `path:line`-backed fact; Facts established → References.
- `skills/grill-me/SKILL.md:19–22` — three failure-mode bullets.
- `docs/spec-workflow-reference.md:31`, `:35` — facts are the agent's job; hand-off paraphrase.
- `docs/specs/DONE/VHS-33/attempt-1/spec.md` Design 3 (`:410–506`) and § Deferred `:1159–1163` (edge-cases R2 F-11); reviews round-3 edge-cases F-2, correctness R2/R3 F-5, round-4 edge-cases F-1 — the contradictions this brief's decisions 4, 5 and 7 remove.
- `docs/specs/DONE/VHS-33/brief.md` decision 11 — the two carried decisions, and the fence that put dispatch rules out of scope there.
- Plane VHS-33 (Done, PR #27 `464303f`); VHS-34 (plain-language pass elsewhere); VHS-37 (spec-cycle fold-vs-defer escape hatch). PR #26 thread 3945500860.
- Interview: 2 rounds, exit empty-frontier
