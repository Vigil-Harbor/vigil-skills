# VHS-43 — Spec-cycle fix - what green means

**Status:** Todo · **Priority:** high · **Assignee:** Devin
**Created:** 2026-10-12 · **Plane:** VHS-43 (ae1a9f75-f075-44c8-85cf-a6c61a577c51, Todo)
**Origin:** Filed 2026-09-08 after the first `/spec-cycle` run on GPT Astra with Sol reviewers (ticket n2o-10, Mac Studio): round 4 exited clean with five P1 findings parked in the spec's deferred section. The 2026-10-11 skill-pack distillation (wiki `overview/2026-10-11-skill-pack-distillation.md` §2 item 2, §3 items 2–3, §6 Wave 2 item 1) reframed the ticket as two changes to `/spec-cycle`'s review loop: replace the multi-site defer rule so an in-scope P1 always folds, and adopt a lead-judgment synthesis of the reviewers' findings. The operator waived the grilling interview (2026-10-12). A Codex review of the first draft (gpt-5.6-sol, read-only, 2026-10-12) returned RED with seven findings; its anchors were verified, its factual corrections are folded here, and the four forks it said only the operator could settle were put to the operator and are Decisions 6–9.

## Problem

From the ticket, verbatim:

> The first spec-cycle on GPT Astra with Sol reviewers. Commented the meta lessons:
>
> "Clarify what 'green' means. Five deferred P1s remain, so the gate measures review completion more reliably than shipping readiness"
>
> "Token hygiene needs measurement. The spec grew substantially, and thread limits forced reviewer reuse. We don't yet have cost evidence."
>
> ticket n2o-10 briefed and cycled on the Mac Studio, round 4 exited clean, but the five deferments may pan out to be a negative pattern if it cascades.

The mechanism behind the first lesson, walked in the current text:

1. `/spec-cycle` 2e routes a finding with two or more propagation sites that is in-scope and P1 to **defer** (`skills/spec-cycle/SKILL.md:522`).
2. A deferred finding becomes a row in `## Deferred — follow-up required`. Every reviewer is told not to re-file a P0/P1 whose root is a well-formed row "unless the candidate is an in-scope P0" (`agents/spec-reviewer-correctness.md:40`, and the same sentence in the other three agents), and a `deferred: D-<n>` disposition closes as `DEFERRED` when the row is well-formed (`agents/spec-reviewer-correctness.md:69-70`).
3. The gate is `total_p0p1 == 0` over the reviewers' STATUS lines (`skills/spec-cycle/SKILL.md:498-507`), so the parked P1 never enters it.

Three further review paths reach the same end state and are in scope:

- **The re-fold recount.** Its revert branch turns an already-folded finding back into a deferral unless it is an in-scope P0 (`skills/spec-cycle/SKILL.md:564`).
- **Round `round_cap` routing.** The same ceiling applies in the final round (`skills/spec-cycle/SKILL.md:576`); that run ends red, but the row survives into a re-run (R4, `:557`).
- **Operator (grill) rows.** A round-`round_cap` grill decision can park a finding without the routing tests (`skills/spec-cycle/SKILL.md:526`), and the reviewers exempt such a row from the ceiling test (`agents/spec-reviewer-correctness.md:36`). The grill run itself stays red (`skills/spec-cycle/SKILL.md:704-705`); a later re-run can go green over the row.

Two paths to a green marker do not pass through review at all and are deliberately left alone (Decision 6): attest mode, which runs no review and writes `verdict: green` without reading deferred rows (`skills/spec-cycle/SKILL.md:834`, `:855`), and green markers issued before this change, which stay valid while their fingerprint matches (`skills/ship-spec/SKILL.md:34`).

## Why it matters

From the ticket: "the gate measures review completion more reliably than shipping readiness", and "the five deferments may pan out to be a negative pattern if it cascades."

The cascade is on record. The distillation's transcript audit found the pattern in nine or more sessions after VHS-37 shipped the routing protocol: specs went green and could not ship, and operators re-folded the parked P1s by hand as an unreviewed "Amendment A" ("finished spec-cycle green, but it deferred two core bugs", wiki `overview/2026-10-11-skill-pack-distillation.md:28`). On VHS-55 (2026-10-11) the same thing happened and was bridged by hand: fold the in-scope P1 rows, run a two-lens delta pass, attest. A full re-run instead costs about 1.5M tokens (same file, `:27`).

## Scope (verified against current files, 2026-10-12)

| # | File / region | Current | Change |
|---|---|---|---|
| 1 | `skills/spec-cycle/SKILL.md` § 2e, routing step 3 "Apply the ceiling" (`:519-523`) | Four bullets. `:520` folds one site or none, whatever the scope. `:521` defers two or more sites when out-of-scope. `:522` defers two or more sites, in-scope, P1. `:523` folds an in-scope P0 at every site and tells the operator to stop if the fold exceeds the brief. | An in-scope P1 folds at every listed site, as an in-scope P0 does (Decision 1). Site count stays recorded as a cost note and no longer routes an in-scope finding (Decision 2). `:520` and `:521` are unchanged (Decision 5). |
| 2 | `skills/spec-cycle/SKILL.md` § 2e, routing step 4 "Act" (`:524`) | A fold that cites a row discharges it only when the row "records a P0 with `Scope: in-scope`"; any other cited row is left live. | Discharge covers an in-scope P1 row the same way, so a legacy or grill row is closed by the fold that resolves it (Decisions 7, 9). |
| 3 | `skills/spec-cycle/SKILL.md` § 2e, "Re-fold recount" (`:561-565`) | The revert-and-defer branch fires when the true site count reaches two or more "and the original finding is not an in-scope P0" (`:564`). | No branch reverts and defers an in-scope P1. Exact wording is the spec author's (Risk 2). |
| 4 | `skills/spec-cycle/SKILL.md` § 2e, the `## Deferred — follow-up required` contract (`:530-560`), the grill-row paragraph (`:526`), the round-`round_cap` routing paragraph (`:576`), and the 2f follow-up render (`:616-629`) | Rows record `Scope: in-scope`, `out-of-scope` or `operator`. R2(c) discharge exists only for in-scope P0 rows. The 2f example shows a live in-scope P1 row (`:629`). A grill row's `Scope` may read `operator — round-<round_cap> grill` with no in/out classification. | Aligned with rows 1–2: an undischarged in-scope P1 row is no longer a legal resting state for a review run. Grill rows become subject to the ceiling on a re-run (Decision 7; Risk 3 covers how their scope is classified). |
| 5 | The reviewers' Deferred-findings block, complete, in all four agents: `agents/spec-reviewer-correctness.md:31-42`, `agents/spec-reviewer-edge-cases.md:31-42`, `agents/spec-reviewer-scalability.md:31-42`, `agents/spec-reviewer-conventions.md:36-47` | The ceiling bullet flags only an in-scope **P0** row without `Discharged:`. The re-file rule suppresses a deferred root "unless the candidate is an in-scope P0". The grill bullet exempts operator rows from the ceiling test. The routing-violation example names only "an in-scope P0 recorded as out-of-scope". The discharge bullet expects `Discharged:` only on in-scope P0 rows. | Every one of those rules treats in-scope P0 and P1 alike, identically worded in the four agents. An undischarged in-scope P1 row — legacy or grill — is a routing violation on the next review run (Decisions 7, 9). |
| 6 | The reviewers' closure rule for `deferred:` dispositions: correctness `:69-74`, edge-cases `:69-74`, conventions `:74-79`, scalability `:58-63` | A `deferred: D-<n>` disposition is satisfied when the row is well-formed. | Reconciled with row 5, so a `deferred:` disposition pointing at an in-scope P0/P1 row cannot close as `DEFERRED`. |
| 7 | `skills/spec-cycle/SKILL.md` § 2b manifest construction (`:430-473`) and the failure-mode entry "Deferral row never re-verified downstream" (`:923`) | Both describe dispositions and row handling in terms of the current ceiling. | Updated where they restate the rule. |
| 8 | `skills/spec-cycle/SKILL.md` § 2c–2d (`:475-509`) | Reports are persisted per lens (2c); the gate sums STATUS lines and breaks to 2g when the total is zero (2d, `:507`), before 2e runs. No step reads the lenses' findings together. | A synthesis step sorts each round's findings into Act on / Consider / Noted / Dismissed with an Agreement Map (Decisions 3, 8). It runs every round, before the green break, so green and zero-finding rounds are synthesized too. |
| 9 | `docs/spec-workflow-reference.md:87`, `:90`, `:94`; `AGENTS.md:109` | They describe the gate exception "under the scope ceiling", the three dispositions, and the closure states. | Updated to the new rule and the synthesis step, in the same PR. |

## Decisions carried forward

The interview was waived. Decisions 1–5 are ones the operator had already recorded; the source is cited. Decisions 6–9 were settled by the operator on 2026-10-12, on the four forks the Codex review raised.

1. **An in-scope P1 always folds.** The multi-site, in-scope, P1 → defer rule is removed. Source: wiki `overview/2026-10-11-skill-pack-distillation.md:44` ("Replace with: an in-scope P1 always folds; multi-site is a cost note, not a routing rule") and `:95`; the operator's standing ruling applied on VHS-55, 2026-10-11.
2. **Multi-site is a cost note, not a routing rule,** for in-scope findings. Source: same file, `:44`.
3. **Adopt a lead-judgment synthesis of reviewer findings:** four buckets, Act on / Consider / Noted / Dismissed, with an Agreement Map. Source: same file, `:43` and `:95`.
4. **An empty review is a valid outcome.** It means a reviewer that returned a parseable report with no findings, which every agent already permits ("If no findings: write \"No findings.\"", `agents/spec-reviewer-correctness.md:181`). A missing or unparseable report is a reviewer failure and stays blocking (`skills/spec-cycle/SKILL.md:489-494`). Source: same wiki file, `:43` and `:95`.
5. **Out-of-scope routing is unchanged.** A valid out-of-scope P0/P1 with two or more propagation sites stays deferred (`skills/spec-cycle/SKILL.md:521`); a finding with one site or none still folds whatever its scope (`:520`); follow-up tickets stay operator-filed, since the skill "never files a ticket" (`:625`). Source: VHS-37 as shipped; this brief does not reopen it.
6. **The guarantee covers review-produced verdicts only.** "Green" means: a verdict with `source: review`, written by a run under the new rule, is never issued while an in-scope P0 or P1 sits undischarged in `## Deferred — follow-up required`. Attest mode and green markers issued before this change are explicitly outside the guarantee and are not edited. Why: an attestation is the operator's own override, and reaching it would add attest validation and a marker migration to a spec that does not need them.
7. **Operator (grill) rows obey the ceiling on re-run.** A row parked by a round-`round_cap` grill decision that holds an in-scope P0 or P1 is flagged by the reviewers on the next review run, like any other row. Why: it is the last review path to green with an in-scope P1 parked.
8. **Synthesis reports and prioritizes; it has no authority over the gate.** Reviewer STATUS counts, finding ids, and the fold / defer / reject obligations are unchanged. A valid in-scope P0 or P1 is always Act on. Dismissed is the existing validity test's reject (`not applicable: <reason>`), and a dismissed P0/P1 stays counted until a reviewer closes it in a later round, as a rejected finding does today. Synthesis runs every round, including a round that goes green and a round with no findings. Why: letting the lead move a blocker out of the gate would change the gate formula, which stays out of scope.
9. **Rows deferred under the old rule are flagged and discharged on re-run.** No grandfathering: on the next review run the reviewers file an undischarged in-scope P1 row as a routing violation, and the author folds and discharges it, as happens for an in-scope P0 row today. Why: grandfathering would put an exception inside the guarantee.

## Done when

The ticket states no acceptance criteria. The criteria below restate the sprint plan's line for this ticket (wiki `overview/2026-10-11-skill-pack-distillation.md:95`), the ticket's first lesson, and Decisions 6–9; the spec author makes each one checkable.

- `/spec-cycle` 2e no longer routes an in-scope P1 to defer, whatever its site count, in ordinary rounds, in the re-fold recount, and at round `round_cap`.
- A review-produced green verdict from a run under the new rule is never written while an in-scope P0 or P1 sits undischarged in `## Deferred — follow-up required`. This is what "green" is clarified to mean, and the skill's text says so in those words, naming attestation and earlier markers as outside it.
- The four reviewer agents and the skill state the same ceiling, in the complete Deferred-findings block and the `deferred:` closure rule, not only the ceiling bullet.
- `/spec-cycle` produces the four-bucket synthesis with an Agreement Map every round, including green and zero-finding rounds, without changing any reviewer's STATUS count.
- The spec's test plan walks each of these scenarios against the new text and records the outcome: an ordinary multi-site in-scope P1; a recount that reaches two sites; a legacy in-scope P1 row on re-run; a grill row holding an in-scope P1 on re-run; a dismissed P0/P1 awaiting reviewer closure; final-round routing; an empty review versus a failed reviewer.
- `docs/spec-workflow-reference.md` and `AGENTS.md` describe the new rule.
- The repo test suite and `python lint.py --strict` pass. They do not prove the invariant: `lint.py` checks capability declarations and harness-specific calls, and no test pins the routing text, so the scenario walk above is the real evidence.

## Out of scope

- **Attest mode and already-issued green markers** (Decision 6). `/spec-cycle --attest` is not edited.
- **The ticket's second lesson, token measurement** ("Token hygiene needs measurement… We don't yet have cost evidence."). The operator split it out on 2026-10-12; it is tracked as VHS-59 and nothing in this spec measures or records cost.
- **Delta-scoped review passes** and the closure ledger — VHS-27, next in the same lane.
- **The author-side ground-truth gate and `check_spec.py`** — VHS-26.
- **The other borrowings listed beside the synthesis buckets** in the distillation's §3 item 2: the doubt-driven reconcile order, the 3-cycle bound, the "doubt theater" red flag, and withholding the author's rationale from reviewers. The sprint plan's line for VHS-43 names only the buckets, the Agreement Map and the empty-review rule.
- **The out-of-scope defer rule and the single-site fold rule** (Decision 5), and the routing protocol's validity, site-naming and scope-classification steps.
- **The gate formula** `total_p0p1 == 0` and the severity scale's definitions.
- **`round_cap`, lens selection, and tier behavior** from VHS-55.
- **`/ship-spec`, `/spec-tickets`, `/spec-close`** — none of them is edited. An informational field added to the verdict marker would not require it: readers take known keys and ignore anything else (`skills/spec-cycle/SKILL.md:47`).

## Tier

**Level:** big

## Risks / decisions

1. **A fold larger than the brief supports.** An in-scope P0 fold that exceeds the brief stops and tells the operator, with no mid-loop scope-down path (`skills/spec-cycle/SKILL.md:523`). Scope row 1 folds an in-scope P1 "as an in-scope P0 does", and that includes this stop: a multi-site in-scope P1 fold that exceeds the brief stops and tells the operator, the same way. This is the brief's stated assumption, not an operator ruling — it follows from Decision 1, the Codex review recommends it, and it is the conservative branch because it hands the call back to the operator at run time. The spec carries the same stop; it is not the spec author's to widen into a mid-loop scope negotiation.
2. **The re-fold recount's wording.** Its revert-and-defer branch is conditioned on "not an in-scope P0" (`:564`). Whether the branch narrows to out-of-scope findings or is restated another way — spec author pins this.
3. **How a grill row's scope is classified.** A grill row may carry `Scope: operator — round-<round_cap> grill` when routing step 2 did not run (`skills/spec-cycle/SKILL.md:526`), and the reviewers do not validate that value against the brief today (`agents/spec-reviewer-correctness.md:36`). Decision 7 needs such a row to be tested as in-scope or out-of-scope on re-run; which lens classifies it is the spec author's to pin. One constraint is fixed: a row whose scope cannot be established is treated as in-scope, the same safe default routing step 2 uses, so uncertainty never exempts a row from Decision 6.
4. **Where the synthesis is written.** A per-round file beside the lens reports, a spec section, or printed output only. The closed-issues manifest scans named reviewer reports in each round directory (`:581-585`), and VHS-27's ledger will read the same directory — spec author pins this.
5. **Whether Consider and Noted can hold a P0 or P1 at all.** Decision 8 makes a valid in-scope P0/P1 always Act on and a wrong one Dismissed. What remains is a valid out-of-scope P0/P1 that routing defers: which bucket names it — spec author pins this.
6. **The "more than 5 Act-on means under-filtering" heuristic** from the same source (wiki distillation `:43`). It is not in the sprint plan's line for this ticket, and it conflicts with Decision 8 when more than five in-scope P0/P1 findings are real. The Codex review recommends leaving it out, and never using it as a cap — spec author pins this.
7. **Whether the green marker or Phase 3 output carries a deferred count.** The verdict marker (`skills/spec-cycle/SKILL.md:25-72`) records `gate` but not how many rows remain deferred, and Phase 3 (`:772-813`) is the operator's last look. A marker field is readable without touching `/ship-spec` (see Out of scope); a print-only line may be enough. Both regions are authorized for an informational addition only — no existing field, and nothing a reader acts on, changes. Whether to add one, and which — spec author pins this.

## References

- Ticket VHS-43, Plane, retrieved 2026-10-12 (no comments on the ticket).
- `skills/spec-cycle/SKILL.md:396` — the three standing lenses are always dispatched, so an Agreement Map always has three or four lenses to compare; tier changes `round_cap`, not the lens minimum (`docs/spec-workflow-reference.md:144-146`).
- `skills/spec-cycle/SKILL.md:430-473` — 2b manifest. `:475-494` — 2c persist and the failed-reviewer stub. `:496-509` — 2d gate. `:511-533` — 2e routing, the ceiling at `:519-523`, the action step at `:524`, grill rows at `:526`. `:530-560` — Deferred section contract, R2–R6. `:561-565` — re-fold recount. `:576` — round-`round_cap` routing. `:601-633` — 2f halt and follow-up render. `:704-705` — the grill leaves the gate unchanged. `:737-769` — 2g polish (among deferred sections it reads only `## Deferred (P2+)`). `:834`, `:855` — attest mode. `:923` — the deferral-row failure mode.
- `agents/spec-reviewer-correctness.md:31-42` — the complete Deferred-findings block (ceiling `:38`, grill exemption `:36`, re-file rule `:40`, routing violations `:42`); the same block at `spec-reviewer-edge-cases.md:31-42`, `spec-reviewer-scalability.md:31-42`, `spec-reviewer-conventions.md:36-47`. "No findings" is permitted at correctness `:181`, edge-cases `:177`, conventions `:170`, scalability `:120`.
- `skills/ship-spec/SKILL.md:22`, `:34`, `:37` — the marker reader ignores unknown fields; a fingerprint-matching green passes; review-produced and operator-attested green pass the same way.
- `docs/spec-workflow-reference.md:87`, `:90`, `:94`; `AGENTS.md:109` — the gate exception and closure states as documented.
- Wiki `overview/2026-10-11-skill-pack-distillation.md:27` (cycle cost), `:28` (friction evidence), `:43-44` (borrowings), `:95-97` and `:124` (sprint plan line and the lane order VHS-43 → VHS-27 → VHS-26, which is established: all three edit § 2e–2g of the same file, in that order).
- Wiki `projects/vigil-skills/state.md:29` — VHS-37, the routing protocol this ticket amends.
- Specs in `docs/specs/TODO/` today: VHS-13, VHS-24, VHS-41. None carries a `## Deferred — follow-up required` row marked in-scope (`grep`, 2026-10-12). Other repos' TODO directories were not checked.
- No test under `tests/` pins the ceiling or the deferred-row contract. Every `ceiling` match under `tests/` is unrelated text in the fixture `tests/fixtures/session-handoff/legacy-flat.md`.
- Codex brief review, 2026-10-12: gpt-5.6-sol, `--sandbox read-only`, high reasoning effort. Verdict RED on the first draft, seven findings (four P1 forks settled as Decisions 6–9, one P1 scope gap folded into rows 2 and 4–7, two P2 folded into Decisions 4–5, Done when and these references). It found one wrong anchor in the draft (`:26` for the cycle cost; corrected to `:27`). All anchors it cited were re-verified against the files before folding. A delta pass on the rewrite returned YELLOW: five findings closed, two partial, three P2 corrections (optional reporting regions, the oversized-fold stop, this file's test-search wording), all folded; it reported no new contradiction and all new anchors correct.
- Tier: chosen by the operator at the tier gate, 2026-10-12. Heuristic basis: files: unknown, lines: unknown, surfaces: unknown — never tweak. The sprint plan had listed this ticket as small.
- Ticket resolution: tracker (the shared-memory mirror denied read on namespace `skills`).
- Interview: skipped (--no-grill)
