# VHS-33 — grilling hand-off contract v2: caller IDs, fact-item shapes, fence-empty token
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-09-06 · **Narrowed:** 2026-09-06 (attempt 2) · **Plane:** VHS-33 (9509a53b-894e-4b5c-82d2-e9cb52ff191d, Backlog)
**Origin:** Follow-up to VHS-32 (PR #26, merged as d381f88 on 2026-09-06). Three gaps on one surface — the `grilling` primitive's hand-off block and its termination tokens. Two were raised by CodeRabbit on the VHS-32 PR (threads 3945500857 and 3945500860, left open on purpose so they close against this ticket) and deliberately not fixed there because the block was pinned verbatim through four review rounds; one was deferred by the VHS-32 spec itself (§ Deferred (P2+), from edge-cases R4 F-1). This brief was produced by the first real `/spec-brief` run, and that run surfaced a fourth item: the interview's own wording needs a plain-language rule.

**Attempt 1 (2026-09-06) ran `/spec-cycle` red through four rounds** (gate 12 → 3 → 5 → 6) and was scoped down by the operator. The spec had grown to 1,178 lines; its round-3 and round-4 P0s clustered under the operator-claim verification item (interview Q3/Q8), which is a fact-finding dispatch rule and needs its own interview. That item is now **VHS-36**. The attempt-1 brief, spec and twelve reviewer reports are in `VHS-33.attempt-1/` beside this file. This brief is the original narrowed by hand; no `/spec-brief` re-run.

## Problem

The hand-off block in `skills/grilling/SKILL.md` is the primitive's entire output contract. Callers parse it: `/spec-brief` maps Settled to "Decisions carried forward" and Open to "Risks / decisions", and `/spec-cycle` 2f-i drives its 2e spec edits from Settled while printing finding ids in its step-5 summary. The block was pinned verbatim through four review rounds and is asserted literally by the VHS-32 test-plan checklist row 4, which is why none of these was fixed inside the ship PR.

1. **No caller ID survives the hand-off** (CodeRabbit 3945500857, Major). 2f-i seeds the primitive with each remaining P0/P1 finding as `{id, severity, title, body}`, and its step 5 prints "dispositioned {ids}; left open {ids}; not grillable {ids}; deferred to option 3 {ids}". But the hand-off emits only Q numbers and decision titles. Nothing carries the caller's stable id back out, so the mapping from a Settled item to the finding it dispositions is by title match. Two findings with similar titles, or a rolled-up deferred subtree (which has no Q number at all, only a parent title), cannot be mapped deterministically. 2f-i then applies Settled decisions to the spec without reviewer re-dispatch, so a mis-mapping is not caught by anything downstream.

2. **Fact items have no hand-off shape** (CodeRabbit 3945500860, Major — first half). The Bounds section says a fact request the operator leaves unanswered twice becomes an Open item, but the Open frontier template defines only Q-numbered questions with branches and a recommendation. An unresolved fact currently rides through as a question carrying "unresolved because: fact not established", which is the spec's accommodation rather than a shape. The thread's second half — a fact the operator supplies directly has no `path:line` and so no legal form — is **VHS-36**. Until VHS-36 lands, an operator-supplied answer to a fact request is treated as today: the fact is not established, and with this ticket it renders as an `F<n>` Open item rather than a Q item.

3. **Fence-empty exit token and the 2f-i re-offer** (VHS-32 spec, Deferred (P2+), from edge-cases R4 F-1). VHS-32 folded half of this finding: the 1.8 header's reason line now distinguishes "tree fully visited" from "no candidate decision met the altitude fence". Deferred as beyond post-green-polish limits: a distinct fence-empty exit token, and a 2f-i re-offer of option 4 when a grill renders zero items. Both are new behavior. Belongs here because a new token is a change to the same termination and hand-off contract as items 1 and 2.

4. **The rendered rounds use internal identifiers without glossing them** (raised by the operator during this brief's interview, 2026-09-06). Section codes such as "2f-i" and exit tokens such as "empty-frontier" appear in question bodies as if the operator knew them; the operator answered round 1 "going off context clues".

## Why it matters

These are contract-shape changes to a block three callers parse and one checklist greps verbatim. Landing them one at a time means three rounds of the same coordination; landing them together is one edit to the primitive, one to 2f-i's step 5, and one checklist-row update.

None is urgent: the primitive ships in VHS-32 with all three known and recorded. Item 1 is the one with a real failure mode in normal use (a mis-mapped Settled decision edits the spec silently). Items 2 and 3 are shape and legibility gaps. Item 4 is the cost of every interview: the operator answers under time pressure, and an unglossed code forces a lookup mid-round.

## Scope (verified against current files, 2026-09-06)

| Path | Current | Change |
|---|---|---|
| `skills/grilling/SKILL.md` | Invocation contract `:14–24` (`seed`, `altitude`, `round_cap`, `question_cap`, `prior_summary`); per-round output contract `:33–58`; fact-finding `:68–79`; termination `:102–112` (five exits); hand-off block `:114–135` with `### Settled` / `### Open frontier` / `### Facts established`, Q-only Open items, `source: <path:line>` | Optional per-seed-item `id` input echoed as `ref:` (0..n ids) on every Settled and Open item including the rolled-up deferred one (Q1, Q9); `F<n>` forms in Open frontier (Q2); sixth exit `fence-empty` through the hand-off block (Q4); plain-language rendering rule in the per-round output contract, STE writing rules only (Q11, Q13, Q14). The fact-finding section `:68–79` is **not** edited. |
| `skills/spec-cycle/SKILL.md` | 2f-i step 1 seeds `id, severity, title, body` (`:494–495`); step 3 persist guard `:518–528` (`empty-seed` or no `## Grill summary` block → write nothing); step 5 line `:549` prints finding ids by category; failure-modes bullets `:698–708` | Pass finding ids as the seed `id`; consume `ref:` in step 5 instead of title-matching (Q1, Q9); persist a `fence-empty` summary as one short block (Q10); the once-per-halt bound is unchanged — `fence-empty` consumes it and the menu re-renders with 1–3 (Q5) |
| `skills/spec-brief/SKILL.md` | Phase 2 halts on `empty-seed` (`:88`); Phase 3 preview reads Settled / Open frontier (`:94`); option 2 resume exits `revised-after-cap` (`:105`); Phase 4 mapping `:138–143` — Open → Risks, Facts → References "with `path:line`"; References bullet interpolates the exit token (`:159`) | Mapping rule for `F<n>` Open items (→ `## Risks / decisions` as "fact not established") (Q7); `fence-empty` handled like `empty-frontier` with the reason recorded (Q4) |
| `skills/grill-me/SKILL.md` | Delivers the Grill summary; stops on `empty-seed` (`:14`, `:21`) | Names `fence-empty` alongside `empty-seed` in its failure modes (Q4) |
| `docs/spec-workflow-reference.md` | Paraphrases the contract at `:23–35` ("emptied frontier", "empty seed", "hand-off block — settled decisions, the open frontier … facts established with their sources") | Paraphrase updated for `ref:`, F-items, and the sixth exit (Q7) |

## Decisions carried forward

1. **Caller IDs survive the hand-off** (Q1) — an optional caller-supplied `id` per seed item is echoed verbatim as a `ref:` field on every Settled and Open item that descends from it, including the rolled-up deferred item; absent when the caller passed none. Determinism over title-matching.
2. **`ref:` holds zero or more IDs** (Q9) — one decision can disposition several findings, and a fact-driven decision may disposition none. Determinism comes from the IDs being present, not from there being exactly one.
3. **Fact items get their own shape** (Q2) — explicit `F<n>` forms in `### Open frontier` (`unresolved because: fact not established | stopped`) alongside the existing `F<n>` in `### Facts established`, so a caller can tell "needs a fact" from "needs a decision". The reason set is exactly those two values.
4. **`fence-empty` is a distinct exit token** (Q4) — a sixth exit, reached when round 1 renders zero items because no candidate met the altitude fence; it goes through the hand-off block with empty sections, and the reason line stays for humans.
5. **A fence-empty grill still consumes the once-per-halt bound** (Q5) — the VHS-32 S8 rule stays flat: the seed cannot change between two grills in one halt, so a re-offer would re-run the same inputs. The menu re-renders with options 1–3. The re-offer half of the deferred finding is therefore *not* adopted.
6. **A fence-empty grill is persisted** (Q10) — 2f-i writes one short block to `grill.md` recording that the grill ran and nothing was askable; it is the only record of a consumed grill.
7. **The archived VHS-32 spec is not edited** (Q6) — `docs/specs/DONE/VHS-32/` is history. The VHS-33 spec carries its own checklist row asserting the v2 block and notes that it supersedes VHS-32 checklist row 4.
8. **`/spec-brief` and the workflow reference are in scope** (Q7) — the contract's consumers change with the contract, in one PR.
9. **A plain-language rendering rule is in scope, for the primitive's rounds only** (Q11, Q13) — every rendered round glosses each internal identifier on first use and keeps question bodies short. A wider pass over the other lifecycle skills' operator-facing blocks (halt menus, previews, close plans) is its own ticket, filed as VHS-34.
10. **ASD-STE100 writing rules, not its dictionary** (Q14) — short sentences, one instruction per sentence, one meaning per term, gloss every identifier on first use. The dictionary is a reference, not a gate; its vocabulary is aerospace maintenance and would reject words this repo needs.
11. **Operator-supplied facts are out of this ticket** (operator, 2026-09-06, scoping down attempt 1) — interview decisions Q3 and Q8 (a supplied fact is a claim to verify by exploration; unverifiable claims stay open; `source: operator` is never legal) are carried to VHS-36 unchanged. This ticket does not touch the fact-finding section and adds no verification, qualifier, or resume rule for F-items.
12. **The spec stays inside the brief** (operator, 2026-09-06, scoping down attempt 1) — the spec author adds no construct the four items do not need. Attempt 1 accreted an all-or-none seed-id legality rule, a `_(none)_` empty-section sentinel, a round-preamble slot, reason-precedence orders, and extra step-5 clauses; none is carried. If a reviewer finding seems to need one, the spec lists it in `## Deferred (P2+)` with the finding id, and the operator decides at the halt.

## Done when

_(The ticket has no Done-when section. The criteria below are its stated fix directions, made checkable by the decisions above.)_

- The hand-off block in `skills/grilling/SKILL.md` carries an optional `ref:` field on every Settled and Open item including the rolled-up deferred item, defines `F<n>` Open forms, and lists `fence-empty` as an exit; the per-round output contract carries the plain-language rule.
- `/spec-cycle` 2f-i passes finding ids as seed ids, reads `ref:` in its step 5 line, and persists a `fence-empty` summary; its once-per-halt bound is unchanged.
- `/spec-brief`'s Phase 4 mapping names the `F<n>` Open form; `/grill-me` names `fence-empty`; the workflow reference's paraphrase matches.
- `lint.py --strict` reports zero ERROR and no new `missing-requires` WARN; `sync.py status` is clean and `sync.py push` round-trips byte-for-byte.
- PR #26 thread 3945500857 can be closed against the merged change; thread 3945500860 can be answered with the `F<n>` shape and pointed at VHS-36 for its second half.

## Out of scope

- Operator-supplied facts as claims to verify, unverifiable-claim handling, and any `/spec-brief` mapping for verified operator claims (Q3, Q8) — **VHS-36**.
- Any change to the three bounds, the fork form, the advisory-recommendation rule, or the fact-finding dispatch rules (`skills/grilling/SKILL.md:68–79`) — VHS-36 for the operator-claim part, a ticket otherwise.
- The durable once-signal for 2f-i (VHS-32 Risk 14) — different surface, still correctly context-held (ticket).
- The `requires:` vocabulary gaps (VHS-32 Risk 9) — their own ticket (ticket).
- Editing anything under `docs/specs/DONE/VHS-32/` (Q6).
- A 2f-i re-offer of option 4 after a fence-empty grill (Q5).
- `source: operator` as a legal established-fact source (Q3, Q8; VHS-36).
- Applying the plain-language rule outside the `grilling` primitive — the halt menus, previews and close plans of `/spec-brief`, `/spec-cycle`, `/spec-close` — its own ticket, VHS-34 (Q13).
- ASD-STE100's controlled dictionary as a vocabulary gate (Q14).
- The Phase 3 drift-check's missing-header fallback not firing on a present-but-empty list (`skills/spec-cycle/SKILL.md:640`; attempt-1 edge-cases R2 F-9) — outside 2f-i, its own ticket.
- A post-cap resume that renders zero items still consuming the operator's one post-cap round (attempt-1 edge-cases R3 F-4) — needs `grilling:23` and `spec-brief:105` together, its own ticket.

## Scale

**Factor:** no

## Risks / decisions

1. What the 2f-i step 5 line prints when one Settled decision carries several `ref:` ids, and how a decision with zero ids is reported there — spec author pins this. Attempt 1 pinned: each id enters `dispositioned` individually, seed-order deduplicated; a decision with zero ids is counted in an `unreferenced decisions applied: <n>` clause. Reviewers did not object to that pin itself; reuse it, and stop there.

## References

- `skills/grilling/SKILL.md:14–24` (invocation contract), `:33–58` (per-round output), `:68–79` (fact-finding — not edited), `:80–100` (bounds), `:102–112` (termination), `:114–135` (hand-off block) — read 2026-09-06.
- `skills/spec-cycle/SKILL.md:494–495` (2f-i seed shape), `:518–528` (step 3 persist guard), `:549` (step 5 line), `:698–708` (failure modes).
- `skills/spec-brief/SKILL.md:88`, `:94`, `:105`, `:138–143`, `:159`; `skills/grill-me/SKILL.md:14`, `:21`; `docs/spec-workflow-reference.md:23–35`.
- F1 — nothing mechanical asserts the hand-off block's shape: `lint.py`, `sync.py`, `tests/` contain no reference to `skills/grilling`; the only verbatim assertion is the archived `docs/specs/DONE/VHS-32/spec.md:458` (checklist row 4).
- `docs/specs/DONE/VHS-32/spec.md` — Design 1.1 (resume contract), 1.7 (termination), 1.8 (hand-off), Design 4 step 5, Test plan checklist row 4, § Deferred (P2+); Decisions S8, S9; Risks 9, 14.
- `docs/specs/TODO/VHS-33.attempt-1/` — the first attempt: `brief.md` (original, with Q3/Q8), `spec.md` (1,178 lines; its `## Decisions` roll-up lists every spec-level addition), `reviews/round-{1..4}/`. Read the round-4 reports before authoring; do not carry the spec's structure.
- PR #26 (https://github.com/ziomancer/vigil-skills/pull/26) threads 3945500857 and 3945500860; merge commit d381f88.
- VHS-36 (operator-supplied facts as claims to verify), VHS-34 (plain-language pass over the other lifecycle skills), VHS-37 (spec-cycle fold-vs-defer escape hatch — filed from this attempt's evidence).
- ASD-STE100, Simplified Technical English — writing rules (Part 1) as the starting point for Decision 10.
- Interview: 3 rounds, exit empty-frontier (2026-09-06). Narrowed by hand 2026-09-06 after attempt 1.
