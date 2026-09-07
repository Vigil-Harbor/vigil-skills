# Conventions Review — round 4

Grounding complete. I read the spec and brief fresh, `AGENTS.md` (the canonical project instructions, per the gitignored `CLAUDE.md`), the global user conventions, all three round-3 reports, every anchored region of the five target files, and the one overlapping wiki decision. `wiki_root` has no `architecture.md` for `vigil-skills`; `state.md`/`filemap.md` present. `scale_lens: off` and `round-3/` holds no `scalability.md` — the stale-report guard is a no-op.

Anchors re-verified live at `7403cb5`: `grilling` `:18`, `:23`, `:104`, `:106`, `:108`, `:110`, `:118–130`, `:132`, `:134`, `:151`; `spec-cycle` `:366`, `:453`, `:495–496`, `:504`, `:539`, `:548–549`, `:698–703`; `spec-brief` `:140`, `:143`, `:159`; `grill-me` `:14`, `:21` (two bullets today); `docs/spec-workflow-reference.md` `:23`, `:35`. All correct. Wiki `decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` § 5 re-read: `Status: active`, `Revisit when:` names VHS-33, and the "Rejected — a success token for an empty interview" clause matches Risk 2's quote verbatim.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Design 7 deletes the altitude-fence parenthetical from `:23` | CLOSED | spec § Design 7, `:399–407` — "the tree was fully visited, or that a later round's remaining candidates all fell below the altitude fence — either way the reason line says which"; row 13 (`:491–494`) asserts "altitude fence" ≥2× and "either way the reason line says which". Verified the new text contains "altitude fence" exactly twice. |
| correctness | F-2 (P2) | "byte-identical to v1" contradicts Design 2's four changes | CLOSED | spec § Design 1, `:200–204` narrowed to the Settled/Open-question *lines*, with the four block-level changes stated; Design 2 `:230–231` ("unchanged for a no-id caller"); Risk 1 `:551–555` ("unchanged Settled and Open-question lines") |
| correctness | F-3 (P2) | `:106`'s "normally empty too, since no round was rendered" is wrong for `/spec-brief` | CLOSED | spec § Design 3, `:278–279` — "empty unless the seed supplied facts or a dispatch returned one"; Design 2 `:246–249`; Risk 2 `:558–559` ("beyond the ones Phase 1's grounding already supplied") |
| correctness | F-4 (P2) | Design 5 doesn't say which step-5 text ships; both-lists rule ungated | CLOSED | spec `:329–330` — "The code block replaces `:548–549`; the bullets below are added to step 5 in the file"; row 10 (`:475–478`) now asserts "is listed here rather than under `dispositioned`" and "in seed order" |
| correctness | F-5 (P4) | Row 10's `grep -c 'total_p0p1 == 0'` names no file | CLOSED | row 10, `:471` — `grep -c 'total_p0p1 == 0' skills/spec-cycle/SKILL.md` |
| edge-cases | F-1 (P1) | `:23` loses the only record of a round-≥2 fence-out | CLOSED | same edit as correctness F-1 |
| edge-cases | F-2 (P2) | `:106` rationale drops seed-supplied facts | CLOSED | same edit as correctness F-3 |
| edge-cases | F-3 (P2) | id on an applied *and* an unapplied Settled item | CLOSED (routed) | § Deferred (P2+), `:620–623`, with the rule to adopt — correct disposition under brief decision 12 |
| edge-cases | F-4 (P2) | No step-4 rule for a summary with no `ref:` fields at all | CLOSED | spec § Design 5, `:319–320` — "or with no `ref:` field at all, which is what a v1-shaped return looks like"; row 10 (`:475`) asserts the string |
| edge-cases | F-5 (P3) | `ref:` ids undefined across a `prior_summary` resume | CLOSED (routed) | § Deferred (P2+), `:624–629` |
| edge-cases | F-6 (P3) | `exit: <token>` undefined when the header carries none | CLOSED | spec § Design 5, `:331–332` — "when the header carries none, print `unknown` — the persisted block is the record". *The rule now exists; its declaration and gate coverage do not → F-1 below (NEW, same root as my round-3 F-1).* |
| edge-cases | F-7 (P4) | Row 9's `:132` reads as a post-change line check | CLOSED | row 9, `:469` — "The pre-edit `:132` (the size-bound sentence) is byte-identical" |
| conventions | F-1 (P2) | Reason-keyed `:143` not in the additions roll-up | CLOSED | roll-up gains an eighth bullet, `:86–90`, citing edge-cases R2 F-6; "Nothing else" (`:92`) re-checked against it |
| conventions | F-2 (P2) | D4 still says "empty sections" | CLOSED | D4 `:119` ("its Settled and Open frontier sections empty"); D6 `:132` ("on the 2f-i path, which seeds findings and no facts"); Design 7's grill-me blockquote `:395` ("its header's reason line is the answer") |
| conventions | F-3 (P4) | Deferred preamble stale after round 2 | CLOSED | `:599–600` — "Every other round-1, round-2 and round-3 P2+ finding was folded". Verified: the only round-3 P2+ non-folds are edge-cases R3 F-3 and F-5, both listed |
| conventions | — | NEW | NEW | The `unknown` exit-token fallback folded from edge-cases R3 F-6 is absent from the roll-up and from every gate row → F-1 below |

No REOPENED items.

## Findings

### F-1: The round-3 `unknown` exit-token fallback is a shipped sentinel that the additions roll-up does not carry and no checklist row asserts

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 5, `:331–332`, against § Decisions roll-up `:60–94` (eight bullets + "Nothing else") and § Test plan row 10 `:470–485`
**Convention violated:** Brief decision 12 and the spec's own D12 (`:162–165`): "The additions roll-up above is the complete list." The roll-up is what `/spec-cycle`'s Phase 3 drift-check reads (`:57–58`), so an incomplete one is exactly the failure it exists to prevent. Also the gate-coverage precedent this spec set in round 3 for the sibling fold (correctness R3 F-4 → row 10 gained "is listed here rather than under `dispositioned`" and "in seed order").
**Evidence:** The shipped step-5 bullet now reads:

> `<token>` is the exit from the summary header; when the header carries none, print `unknown` — the persisted block is the record.

`unknown` is a new literal that is not one of the six exit tokens and appears nowhere else in this spec (`grep -n unknown` on the spec returns exactly `:332`). The roll-up bullet that covers the token (`:83–85`) says only that the step-5 line "carries the summary's exit token … uniform across exits, no purpose-written line" — it does not reach a malformed header. And the roll-up's closing sentence (`:92–94`) explicitly disclaims "no **empty-section sentinel**" — a missing-value sentinel is the same class of construct brief decision 12 removed from attempt 1 (`_(none)_`), so a Phase 3 reader comparing the roll-up against the Designs finds a sentinel the roll-up says is not there.

The gate gap compounds it, and asymmetrically: its sibling fold from the same round *is* gate-held — row 10 (`:475`) asserts step 4 contains "or with no `ref:` field at all" — while row 10 asserts nothing about `unknown`. It can silently fail to ship, and 2f-i is a prompt with no behavior its own text does not state.

This is category (d), a silent addition, rather than a wrong rule: `unknown` is a sensible choice with repo precedent (`skills/spec-brief/SKILL.md:30`, `:53` use "unknown" for an unrecognized input; `skills/talaria/scripts/talaria_bridge.py:387` uses `"unknown"` as a stored value). Round-3 edge-cases offered the fold *or* a Deferred route; folding was the right call under the operator's standing preference. It just has to be declared. P2, not P1: the rule ships correct if the implementer follows Design 5 literally, and the pre-existing four lists still print without it.

**Suggested fix:** Two edits, both inside text already present, no new construct.

1. Add a ninth roll-up bullet in the shape of the existing eight, e.g.: "`unknown` as the step-5 `<token>` when the returned header carries no exit (Design 5). Needed because step 5 now depends on a header field step 3's guard does not check (it tests only for a `## Grill summary` line); the persisted block is the record (edge-cases R3 F-6). The step-4 tolerance for a Settled item with no `ref:` field at all (Design 5, edge-cases R3 F-4) is the same one-clause read of the same malformed return." Then re-check that "Nothing else" (`:92`) still holds — in particular whether "no empty-section sentinel" needs the qualifier "other than the step-5 `unknown` token".
2. Add one clause to row 10: step 5 also contains "print `unknown`". The string is already in the pinned text.

## Notes (no finding)

Recorded so the orchestrator need not re-derive them.

- **The byte-identical narrowing (correctness R3 F-2) needs no roll-up bullet.** Its text sits at `:200–204`, which is Design 1's spec-side commentary, not a blockquote — the shipped `ref:` paragraph ends at `:198`. It corrects a wrong justification, ships nothing, and adds no construct. Same for Design 2's `:230–231` and Risk 1's `:551–555`. Correctly *not* in the roll-up.
- **The step-4 no-`ref:`-field clause is a clause, not a construct — but it belongs in F-1's bullet.** It is a direct completion of a sentence brief decisions 1 and 2 authorize, and Design 1's own contract already defines the field-absent state. It is gate-held by row 10. I name it in F-1's fix only because it and `unknown` are one posture (tolerating a malformed return from a prompt-implemented primitive) and one bullet covers both honestly.
- **The "v1-shaped return" gloss is not an unneeded backwards-compat shim.** `grilling` and `spec-cycle` ship in the same PR and `sync.py install` is all-or-nothing per run, so no real v1/v2 skew exists — but the rule's actual justification (a model dropping a conditional field) is sound and identical, and the gloss aids the implementer. Not the `_unused`-var / type-re-export pattern AGENTS.md's delete-cleanly posture targets. Checked, no finding.
- **`spec-brief:143` vs `:159` is not a divergence.** `:143` is the brief's `## References` bullet; `:159` is the console summary block (`Interview: <n> rounds, exit <token>; <s> settled, <o> open`). Different surfaces, legitimately different shapes; on `fence-empty` the console line reads `0 settled, 0 open` and is self-legible. `:159` is correctly fenced by row 11's "hunks only at `:140` and `:143`", and roll-up bullet 7's citation of it as a `rounds:` consumer is accurate.
- **Design 7's `:35` enumerates two of three Open-item kinds** ("a reason for each unresolved question and each unestablished fact"), where the live text says "each unresolved item" — the rolled-up deferred item is neither. Not raised: the rolled-up item carries no `unresolved because:` field even in v1, so the new wording is more precise about the two that do, and `:35` is an explicitly lossy paraphrase. Judged not a finding rather than a P4.
- **Still no premature abstraction, no duplication, no compat cruft.** `ref:` is a field on existing lines; `blocked-on: F<n>` reuses `blocked-on: Q<m>`; the F-item reuses the existing `F1…Fn` series (`grilling:48`, `:129`); the lens-qualified id reuses `spec-cycle:366`/`:504` rather than 2e's three-part `:453`; Design 6's F-item Risks text reuses `spec-brief:80`'s shape. `fence-empty` is a sixth member of an existing enum, not a new dispatch mechanism.
- **Portability conventions hold.** No added line in `grilling`, `grill-me`, or `spec-brief` matches `\b(Explore|Agent|Skill|general-purpose)\b` or `model:`; Design 4's plain-language paragraph names no harness mechanism. Rows 2 and 3 gate it. Consistent with `docs/authoring-portable-skills.md`.
- **Wiki decisions re-scanned.** Only `2026-09-06-vhs-32-…` overlaps; D4 and Risk 2 name it, quote § 5 verbatim, state the narrowing, and hand recording to `/spec-close` — the correct disposition, and its `Revisit when:` already names VHS-33. `2026-08-09-review-round-artifacts-are-immutable` honored: no round-1/2/3 report was edited; closure is recorded forward. `2026-06-16-vhs-15-optional-scalability-lens` satisfied by the brief's `**Factor:** no` and D13. `2026-08-25-vhs-28-supersession-is-an-operator-step` is the posture D7 reuses for the checklist supersessions.
- **`fact not established` still has no caller** outside `docs/specs/`: only `grilling:74`, `:88`, `:125`. Dropping it from the Q-item reason list remains the correct delete-cleanly call.
- **Gate trend across attempt 2 (this lens):** R1 P0=2/P1=4/P2=18/P3=11/P4=4 → R2 P0=2/P1=4/P2=8/P3=3/P4=1 → R3 P0=0/P1=1/P2=3/P3=2/P4=1 (worst lens) → R4 P0=0/P1=0/P2=1. Round 3's folds produced one bookkeeping gap and no new P0/P1 — the first round in this attempt where that is true.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 0

STATUS: GREEN
