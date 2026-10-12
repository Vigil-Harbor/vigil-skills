# VHS-43 — Spec-cycle fix — what green means

**Brief:** operator-approved VHS-43 brief (grilling waived; Decisions 1–9 settled). Authoring copy was the attached brief; it is not in this repo's tree. **Plane:** VHS-43 (`ae1a9f75-f075-44c8-85cf-a6c61a577c51`, Todo). **Date:** 2026-10-12. **Grounded on:** `main` @ `7abe102`.

Line numbers below are that tree, before these edits. The review of this spec dispatches the four reviewer agents as they stand on that commit. This spec changes those agents; the review does not use the text it proposes.

The distillation file the brief cites (`overview/2026-10-11-skill-pack-distillation.md`) was not readable here: cloning `Vigil-Harbor/vigil-harbor-wiki` returned repository-not-found. Decisions 1–4 are carried from the brief's quotations of that file. This spec does not add distillation text the brief did not quote. Plane `workitem retrieve` for VHS-43 returned the same problem statement the brief quotes. Shared-memory search on namespace `skills` is the miss the brief already records; the brief is the ticket source.

## Goal

A review-produced green verdict means the spec is clear of undischarged in-scope P0 and P1 findings, not merely that the reviewers finished a round. `/spec-cycle` folds every in-scope P1, however many propagation sites it has, and the site count is only a cost note. The same rule covers the re-fold recount, final-round routing, legacy rows from the old defer rule, and operator (grill) rows on the next review run. Each round also writes a four-bucket lead-judgment synthesis with an Agreement Map. The synthesis does not change any reviewer's STATUS line or the gate sum. Attest mode and green markers already issued stay as they are.

## Scope

| Path | Change |
|---|---|
| `skills/spec-cycle/SKILL.md` | Ceiling in § 2e (`:519-523`), the Act step (`:524`), the grill-row paragraph (`:526`), R2(c) and R5 (`:555`, `:558`), the re-fold recount (`:561-565`), the final-round routing paragraph (`:576`), the 2b manifest construction (`:449-451`, `:455`), the 2f example (`:628-629`), the 2d break (`:507`), the 2e entry conditions (`:513`, `:567`), the 2f halt entry, Remaining list, and option 4 (`:603`, `:605-622`), a new synthesis step between 2c and 2d, the Phase 3 green write and checklist (`:772-813`), and the deferral-row failure mode (`:923`). |
| `agents/spec-reviewer-correctness.md`, `agents/spec-reviewer-edge-cases.md`, `agents/spec-reviewer-scalability.md` | Deferred-findings block `:31-42`, including the Routing violations bullet's acceptance of a `guarantee/D-<n>` manifest id, and the `deferred:` closure paragraph `:69-74` (scalability: `:58-63`). One sentence on step 7 (`:44`, scalability `:44`) so `synthesis.md` is not a closure input. |
| `agents/spec-reviewer-conventions.md` | The same block at `:36-47`, including that same Routing violations sentence, the same closure paragraph at `:74-79`, and the same step-7 sentence at `:49`. The four copies of the block stay byte-identical, as they are today. |
| `docs/spec-workflow-reference.md` | `:87`, `:89`, `:90`, `:91`, `:92`, `:94`, and the Phase 3 description at `:96-104`. |
| `AGENTS.md` | The spec-cycle bullet (`:27`) and the severity bullet (`:109`). |

Leave alone:

- `skills/spec-cycle/SKILL.md` § Attest mode (`:830-857`), including the attested-marker write at `:855`. No edit.
- The verdict-marker field list (`:29-42`) and the reader table (`:63-70`). No new key.
- `skills/ship-spec/SKILL.md`, `skills/spec-tickets/SKILL.md`, `skills/spec-close/SKILL.md`. Ship-spec's reader takes known keys and ignores anything else (`skills/ship-spec/SKILL.md:22`); a fingerprint-matching green passes (`:34`); review-produced and operator-attested green pass the same way (`:37`).
- The one-site-or-none fold (`skills/spec-cycle/SKILL.md:520`) and the two-or-more-sites out-of-scope defer (`:521`). Routing steps 0–2 (validity, site naming, scope classification) at `:516-518`.
- The gate formula `total_p0p1` = sum of P0+P1 on RED STATUS lines (`:500-505`). Severity definitions. `round_cap`, lens selection, and tier behavior.
- `## Deferred (P2+)` and 2g (`:737-768`), which still reads only that section.
- 2f-i (`:634-735`). The grill run still appends a row without running the routing tests, and `total_p0p1` is still unchanged at `:703-705`.
- The severity-inflation failure mode (`:876`). It stays verbatim and is not an Act-on cap.
- `README.md`, `docs/customizing.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`. Grep on this tree finds no ceiling restatement in those files.
- `sync.py`, `skills/ship-spec/states.json`, every file under `tests/`. No new test module.
- Historical specs under `docs/specs/DONE/`.
- `docs/specs/TODO/VHS-43.*` — this spec, any brief, `.reviews/` including `synthesis.md`, and `test-output.txt` — is not staged. The PR's diff is the five Scope paths.

## Decisions

### Decision 1 — An in-scope P1 always folds

Brief Decision 1. The bullet at `skills/spec-cycle/SKILL.md:522` (two or more sites, in-scope, P1 → defer) is removed. An in-scope P1 folds at every listed site, as an in-scope P0 does. This applies in ordinary rounds, in the re-fold recount, and at round `round_cap`.

### Decision 2 — Multi-site is a cost note

Brief Decision 2. For an in-scope finding the site count is recorded and does not route. Out-of-scope routing is Decision 5 and is unchanged.

### Decision 3 — Lead-judgment synthesis

Brief Decision 3. After each round's reports are on disk and before the green break, the author writes four buckets — Act on, Consider, Noted, Dismissed — and an Agreement Map. The schema is Decision 13.

### Decision 4 — An empty review is valid

Brief Decision 4. A parseable report with no findings ("If no findings: write \"No findings.\"", `agents/spec-reviewer-correctness.md:181`, edge-cases `:177`, conventions `:170`, scalability `:120`) is a valid lens outcome. A missing or unparseable report, and a 2c dispatch-failure stub (`skills/spec-cycle/SKILL.md:489-494`), stay blocking.

### Decision 5 — Out-of-scope routing is unchanged

Brief Decision 5. `:520` and `:521` stay byte-identical. A valid out-of-scope P0 or P1 with two or more sites is still deferred. Follow-up tickets stay operator-filed (`:625`).

### Decision 6 — The guarantee covers review-produced verdicts only

Brief Decision 6. A verdict with `source: review`, written by a run under this rule, is never written while an in-scope P0 or P1 sits undischarged in `## Deferred — follow-up required`. Attest mode and green markers issued before this change are outside the guarantee and are not edited. The skill states that sentence at the green write. The break gains a scan that enforces it. The scan is not a new program and is not VHS-26.

### Decision 7 — Grill rows obey the ceiling on re-run

Brief Decision 7. A row parked by a round-`round_cap` grill decision is classified on the next review run. An in-scope P0 or P1 is a routing violation. The propagation-sites exemptions on a `(grill)` row stay. 2f-i itself does not start applying the ceiling.

### Decision 8 — Synthesis has no authority over the gate

Brief Decision 8. STATUS counts, finding ids, and the fold / defer / reject obligations are unchanged. A valid in-scope P0 or P1 is always Act on. Dismissed is routing step 0's reject (`not applicable: <reason>`). A dismissed P0 or P1 stays in that round's STATUS sum until a later round's reviewer closure marks it closed. Synthesis does not subtract it and does not carry a phantom count into the next round. Synthesis runs every round, including a green round and a round with no findings.

### Decision 9 — No grandfathering

Brief Decision 9. On the next review run an undischarged in-scope P1 row, legacy or grill, is a routing violation. The author folds and discharges it, as for an in-scope P0 row today.

### Decision 10 — The brief-exceeding stop covers an in-scope P1

Brief Risk 1, pinned here. The stop already on an in-scope P0 fold (`skills/spec-cycle/SKILL.md:523`) covers an in-scope P1 fold with the same sentence: if the fold is more than the brief supports, stop and tell the operator. There is no mid-loop scope-down path. No new menu and no new marker write. Do not defer the finding instead of stopping. Do not write a review-produced green verdict on that stop. Print `fold exceeds brief: <finding id> (<k> sites) — <brief row or Out-of-scope item>; marker left pending`. The Phase 2 pending marker stays.

### Decision 11 — The recount reverts only an out-of-scope fold

Brief Risk 2, pinned here. The revert-and-defer branch fires only when the original finding is out-of-scope. An in-scope P0 or P1 never takes that branch; the fold is kept and the site list is corrected, with the existing `(recount: <k> sites, fold kept)` suffix.

### Decision 12 — Who classifies a grill row

Brief Risk 3, pinned here. Every lens classifies a `Scope` token of `operator`, and any token other than `in-scope` or `out-of-scope`, by routing step 2 (`skills/spec-cycle/SKILL.md:518`) verbatim. The test uses the row's `Where` and its `Suggested fix`, not `Where` alone. In-scope means both fall inside a brief Scope row and outside every Out-of-scope item. Anything else is out-of-scope, including a `Where` that does not map to a spec Scope row. The only in-scope default is the one step 2 already states: the brief has no Scope table or no Out-of-scope list. A missing `Where` or `Suggested fix` on the row is in-scope, because the test cannot be run. A stated `in-scope` or `out-of-scope` token is not re-derived. The conventions lens still verifies a stated region (`agents/spec-reviewer-correctness.md:37`); the other lenses still read a stated region as opaque. The guarantee scan, the Act step's ceiling test, and a 2c-s classification of an existing row use this step-2 application and no other. An unparseable `Finding` severity is read as P1 for that ceiling test, in the same words as the reviewers' ceiling bullet. That reading is not a second classifier. A new P0 or P1 finding's bucket still comes from steps 0–3, and the scope step inside that is this same step 2. A P2, P3, or P4 is Noted and is not routed through those steps.

### Decision 13 — Where synthesis is written

Brief Risk 4, pinned here. Each round writes `docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/synthesis.md` beside the lens reports. The author also prints a one-line count per bucket. The spec file is not edited by synthesis. The closed-issues scan (`skills/spec-cycle/SKILL.md:581-585`) keeps its named report list and does not read `synthesis.md`. VHS-27 may read the file later; this spec does not define that ledger.

### Decision 14 — Which bucket holds an out-of-scope P0 or P1

Brief Risk 5, pinned here. A valid out-of-scope P0 or P1 with two or more sites is Consider. That is the deferral Decision 5 keeps. Noted never holds a P0 or P1. Dismissed holds a P0 or P1 only when step 0 rejects it. Act on holds every fold: every valid in-scope P0 and P1, every P0/P1 with one site or none, and every finding whose title begins `routing violation:`. Act on, Consider, and Dismissed hold P0 and P1 findings only. A P2, P3, or P4 is Noted.

### Decision 15 — No Act-on cap

Brief Risk 6, pinned here. The distillation's "more than 5 Act-on means under-filtering" heuristic is not adopted. The skill does not count Act-on items toward a warning or a cap. The severity-inflation failure mode at `skills/spec-cycle/SKILL.md:876` stays verbatim.

### Decision 16 — Deferred count is print-only

Brief Risk 7, pinned here. Phase 3 prints a deferred-row tally and the path of that round's `synthesis.md`. The verdict marker gains no field. A count stored on the marker would be a second source of truth that ship-spec is required not to read.

### Decision 17 — Tier

**Tier:** big

Brief `## Tier` / `**Level:** big`. `round_cap` stays 4. This spec does not change tier, lens selection, or `round_cap`.

## Design

### Ceiling

In `skills/spec-cycle/SKILL.md` § 2e, replace the four bullets under **Apply the ceiling** (`:519-523`) with these three. The first two are today's `:520` and `:521`, unchanged.

- one site or none → **fold**, whatever the scope or severity;
- two or more sites and out-of-scope → **defer**, whatever the severity;
- two or more sites and in-scope → **fold**, whatever the severity (P0 or P1): edit every site on the list. An in-scope P0 or P1 cannot ship as a known issue. When the site count `k` is 2 or more, append ` (sites: <k>)` to the disposition phrase, after the section list and before a recount suffix if there is one. The note does not route, and no consumer parses it. If the fold is more than the brief supports, stop and tell the operator; there is no mid-loop scope-down path (2f option 3 is reachable only after round round_cap).

Routing steps 0, 1, and 2 (`:516-518`) stay as written.

**Act** (`:524`). A fold that cites a row `D-<n>` discharges it when the row records a P0 or a P1 that the ceiling test classifies as in-scope. That is R2(c), extended from P0 to P1. The fold is the union of the finding's sites and the row's `Propagation sites`, and the disposition is `fixed: discharged D-<n> — edited § <a>; § <b> (§ Deferred — follow-up required)`. A cited row the ceiling test classifies as out-of-scope stays live: fold the finding at its own sites, disposition `fixed: edited § <a>; § <b>`, and do not discharge the row.

A grill row whose token is `operator` and that classifies as in-scope is the same discharge. In that same fold, repair `Scope` to `in-scope — <the step-2 citation>` (an R2(a) repair) and then append `Discharged:`. One disposition, the discharge form. The finding record (`Finding`, `Deferred in`, `Suggested fix`) is still never rewritten. The guarantee scan does not rewrite it, and it does not rewrite a heading id.

`R2` (`:555`). The discharge sentence covers a row whose `Finding` severity is `P0` or `P1`, or whose severity does not parse and is read as P1, and whose ceiling classification is, or becomes under an (a) repair, in-scope. That reading is not written back into the row. The scan does not add an edit to R2 or to the `:576` FROZEN list. `R5` (`:558`): a fold that resolves an in-scope P0 or P1 row's root is completed by that R2(c) discharge in the same round.

A placeholder entry `§ (operator decision — routing tests not run)` does not count as a section a fold can land on. Redo step 1, append the sites it names, and discharge against those. If the redo finds no existing section, the stop in Decision 10 applies, and no review-produced green verdict is written. Print `fold exceeds brief: <finding id> (<k> sites) — <brief row or Out-of-scope item>; marker left pending`. The pending marker stays.

### Re-fold recount

In the recount (`:561-565`):

- The sentence that a discharged finding resolves by the last bullet because it "is an in-scope P0" (`:561`) names an in-scope P0 or P1.
- The revert condition (`:564`) requires the original finding to be out-of-scope. Replace "the original finding is not an in-scope P0" with "the original finding is out-of-scope". Scope is re-computed by routing step 2 on the original finding every time the recount runs. Unclassifiable is in-scope, so the fold is kept. The recount does not read `synthesis.md` for scope.
- The inner fold clause on that same bullet names "in-scope P0 or P1, or one site or none". An out-of-scope original is still reverted and deferred when the new finding folds. Only a new finding the ceiling defers becomes the second row.
- The Otherwise bullet (`:565`) names "an in-scope P0 or P1" where it now names "an in-scope P0".

An in-scope finding therefore never re-enters `## Deferred — follow-up required` through the recount. A fold made in a prior invocation is still not recounted (`:561`).

### Grill rows, final round, and the follow-up example

The grill paragraph (`:526`) keeps its rule: 2f-i step 4 does not run the routing tests, and a Settled grill decision that parks a finding appends a row with `Deferred in: round <round_cap> (grill)` and, when step 2 did not run, `Scope: operator — round-<round_cap> grill`. Add this sentence: the row is a legal resting state only until the next review run; that run's ceiling classifies it, and an in-scope P0 or P1 is folded and discharged. 2f-i does not change. The grill run stays red because `total_p0p1` is unchanged (`:703-705`).

The final-round paragraph (`:576`) already runs the same routing step. Add this sentence: an in-scope P1 folds at round `round_cap` under that ceiling and is not deferred there.

The 2f example (`:628-629`) teaches a live in-scope P1 as an ordinary row. Replace the second sample line with a discharged in-scope P1:

```text
  - D-1  correctness/R2/F-3  P1  out-of-scope  "<title>"  — Follow-up: unfiled
  - D-2  edge-cases/R3/F-4   P1  in-scope      "<title>"  — Follow-up: unfiled [discharged: folded round 3 — § Design; § Test plan]
```

The render rule is unchanged: it still prints every row, and a row carrying `Discharged:` still prints ` [discharged: <value>]` and needs no ticket (`:625`). Add this sentence after the example: an undischarged in-scope P0 or P1 line in this render is a defect in the run, not a legal resting state.

Under the row template (`:547`), add this sentence: an undischarged row the ceiling classifies as in-scope is not a legal resting state. The template's `Scope:` alternatives stay, because a discharged row still records `in-scope` and a grill row still records `operator` until a fold repairs it.

In the 2b manifest prose after `:455`, add this sentence: a `deferred:` disposition is legal only when routing deferred the finding (out-of-scope, two or more sites). An in-scope P0 or P1 is never dispositioned `deferred:`. The sample line at `:438` stays, as the shape of a legal deferral. The recount's round-qualified revert line stays `deferred:` and is only emitted for an out-of-scope original. A scan discharge that has no reviewer finding is dispositioned `guarantee/D-<n> (P<sev>) "<row title>" — fixed: discharged D-<n> — edited § <a>; § <b> (§ Deferred — follow-up required)`. The scan does not emit `fixed: repaired` for an unparseable severity or id. At `:449-451`, the sentence that the recount's revert line is the one exception names both that line and a `guarantee/D-<n>` line. A `guarantee/` line is not required to match a round-(N−1) finding.

### Reviewer Deferred-findings block

The block is byte-identical today across `agents/spec-reviewer-correctness.md:31-42`, `agents/spec-reviewer-edge-cases.md:31-42`, `agents/spec-reviewer-scalability.md:31-42`, and `agents/spec-reviewer-conventions.md:36-47`. After the edit the four copies are byte-identical again. Copy every bullet that this section does not replace verbatim from today's correctness file.

Replace **Operator (grill) rows** with:

> A row whose `Deferred in:` field carries `(grill)` is exempt from the two-entry `Propagation sites` floor and from the at-least-one-existing-site and every-other-entry tests on `Propagation sites`. It is not exempt from the ceiling. The ceiling classifies its `Scope` token by the rule in this block. The conventions lens does not treat the token `operator` as a stated file region.

**Scope field** stays verbatim (`:37` in the correctness file).

Replace **The ceiling** with:

> A row whose `Finding` severity is `P0` or `P1`, that carries no `Discharged:` field, and that is in-scope under the test in this bullet, is itself a routing violation whatever else it satisfies — the ceiling forbids deferring an in-scope P0 or P1. File it once, as a P0 titled `routing violation: D-<n>`, naming the ceiling, unless you are filing the underlying in-scope P0 or P1 under the re-file exception, which cites the row and names the ceiling instead. A `Finding` severity that does not parse is read as P1 for this test. Take the `Scope` token as the text before the first em dash (`—`), trimmed. Token `in-scope` is in-scope. Token `out-of-scope` is not. Token `operator`, and any other token, is classified by routing step 2 of `/spec-cycle` (`skills/spec-cycle/SKILL.md:518`) verbatim, applied to the row's `Where` and its `Suggested fix`: in-scope when both fall inside a row of the brief's Scope table and outside every Out-of-scope item; out-of-scope otherwise, including when `Where` does not map to a spec Scope row. The only in-scope default is step 2's own: the brief has no Scope table or no Out-of-scope list. A missing `Where` or `Suggested fix` classifies in-scope. The P1 reading is not written into the row. An unparseable `D-<n>` id does not stop the test. When the classification is in-scope, file `routing violation: D-?`. Every lens runs this classification. A stated `in-scope` or `out-of-scope` token is not re-derived here. This is the only row classifier. The guarantee scan, the Act step, and a 2c-s reading of an existing row use it and no other. The author's fold of that violation is the R2(c) discharge, and it does not rewrite `Finding` or the heading id.

Replace **Discharge** so that every "in-scope P0" obligation names an in-scope P0 or P1:

- An empty, unparseable, or names-no-section `Discharged:` is still treated as absent. An in-scope P0 or P1 row carrying one is still `routing violation: D-<n>`.
- A row cited when an in-scope P0 or P1 was filed under the re-file exception must carry `Discharged:` by the next round when the ceiling classifies the row as in-scope, including after a `Scope` repair from `operator` to `in-scope`. If that fold happened and the row still carries none, file `routing violation: D-<n>`.
- A cited row the ceiling classifies as out-of-scope stays live and is not expected to carry `Discharged:`.
- The rest of today's bullet stays: sections named in `Discharged:` must carry the fold; a removed section is re-anchored under R2(b) and a missing marker is a P2; a title `(recurrence of D-<m>)` is a new row.

Replace the re-file exception. Today's sentence (`:40`) suppresses a P0/P1 whose root is a well-formed row unless the candidate is an in-scope P0. The exception is an in-scope P0 or P1. The sentence that each lens decides for itself whether a P0 it is about to file is in-scope covers a P0 or a P1.

In **Free-form row text**, the phrase "the `(grill)` exemption" becomes "the `(grill)` propagation-sites exemption", so the inert-text bullet does not preserve a ceiling exemption.

In **Routing violations**, the example "an in-scope P0 recorded as out-of-scope" becomes "an in-scope P0 or P1 recorded as out-of-scope". The rest of the bullet stays, including the P2 for a `Scope` error that does not change routing. Add this sentence, identically worded in all four copies: a manifest line whose finding id is `guarantee/D-<n>` records a scan discharge the lead made with no reviewer finding. Verify a `fixed: discharged` line against row `D-<n>`'s `Discharged:` and the sections it names. Do not treat its absence from round N−1 as a defect, and do not add it to the closure table as a reviewer finding. The scan does not emit `fixed: repaired`.

### Closure rule for `deferred:`

The paragraph is byte-identical today at correctness `:69-74`, edge-cases `:69-74`, conventions `:74-79`, and scalability `:58-63`. Keep the four copies identical.

A `deferred: D-<n>` disposition is satisfied, and the finding is `DEFERRED`, only when the row is well-formed and the ceiling test does not classify it as an undischarged in-scope P0 or P1. When the row is an undischarged in-scope P0 or P1, including a grill row the ceiling classifies as in-scope, do not mark `DEFERRED`. Mark the finding REOPENED and cite the `routing violation: D-<n>` the block files as the evidence. The defect is reported once, not as a second finding. A missing row and a malformed row stay REOPENED as they are today.

### `synthesis.md` is not a reviewer report

On each agent's step 7, after the named report list (correctness and edge-cases `:44`, conventions `:49`, scalability `:44`), add this sentence, identically worded:

> Do not read `synthesis.md` in that directory. It is the lead's bucket report, not a reviewer report, and it is not a closure input.

The stale-report guard for `scalability.md` is unchanged. The "No findings." lines are unchanged.

### Synthesis step

Insert **2c-s. Lead-judgment synthesis** after 2c (`:475-494`) and before 2d (`:496`). It runs every round, after the reports (and any 2c stub) are on disk, including a round that later goes green and a round whose lenses all returned no findings. It does not edit the spec. It does not change a STATUS line, a finding id, or `total_p0p1`.

For each P0 or P1 finding in this round's reports, apply routing steps 0–3. A P2, P3, or P4 does not take those steps. That application, for a P0 or P1, is the lead judgment. Assign one bucket (Decision 14). The table is first-match, in this order:

| Routing result | Bucket |
|---|---|
| P2, P3, or P4 | Noted |
| Fold: valid in-scope P0 or P1, any site count; any P0 or P1 with one site or none; any title beginning `routing violation:` | Act on |
| Defer: valid out-of-scope P0 or P1 with two or more sites | Consider |
| Reject: step 0 on a P0 or P1, the finding is wrong | Dismissed |
| A lens whose findings section is "No findings." and whose STATUS is parseable | Noted, one line `<lens> — no findings` |
| Missing or unparseable STATUS, or a 2c stub (`:489-494`) | Act on, id `<lens>/STATUS`, severity P0 |

A one-site P2 matches the first row and is not Act on. A P2, P3, or P4 is still handled by `:527`: fix it, or list it in `## Deferred (P2+)`. The bucket does not route it through steps 0–3.

An Act-on entry with two or more sites records `sites: <k>` as the cost note. Consider never contains an in-scope P0 or P1. Noted never contains a P0 or P1. A dismissed P0 or P1 is listed and remains in the STATUS sum 2d computes. The next round's closure is what retires it, the same as a `not applicable:` disposition today. Synthesis does not add a count of its own.

The Agreement Map groups findings that share a root (same spec section, same defect). Each finding stays in its own bucket. The map does not promote or demote a finding. Columns: root, finding ids, lenses, severities, bucket. When the grouped findings have different buckets, the bucket cell is `mixed:` followed by each id and its bucket. Grouping does not merge STATUS counts.

Write `docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/synthesis.md`:

```markdown
# Synthesis — round <N>

Lenses: <dispatched lens names>
Empty review: <lens names with no findings, or none>

## Act on
- <lens>/F-<k> (P<sev>) "<title>" — sites: <k> — <one line>

## Consider
(none)

## Noted
- <lens> — no findings

## Dismissed
- <lens>/F-<k> (P<sev>) "<title>" — not applicable: <reason>

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
```

Each bucket section is a list or the single line `(none)`. `Empty review` lists only lenses with a parseable report and no findings. A stub or a missing STATUS is Act on and is not on that line. Print one line to the operator: `synthesis: Act on <a>, Consider <c>, Noted <n>, Dismissed <d> — round-<N>/synthesis.md`.

Each invocation's first write of `round-<N>/synthesis.md` replaces any existing file of that name, by tmp-rename in the same directory. Later lines in the same invocation append. A failed write prints `synthesis NOT written: <error>` and does not change the gate or routing. Do not append to a file this invocation did not write. A prior round's file is not edited. The recount re-runs routing step 2 for scope, as § Re-fold recount states, and does not read this file for it.

2e routes each P0 and P1 from steps 0–3. The 2e disposition is authoritative for those findings. Act on folds, Consider defers, Dismissed is `not applicable:`. When a 2e disposition puts a finding in a different bucket than this invocation's synthesis recorded, including a recount that keeps or reverts a fold, append `adjustment: <id> — <old bucket> → <new bucket> — <reason>`. The closure manifest is still built from the 2e dispositions (`:449`), not from the map.

The closed-issues scan (`:581-585`) still names `correctness.md`, `edge-cases.md`, `conventions.md`, and `scalability.md` when the lens ran. It does not read `synthesis.md`.

### What green means

`total_p0p1` stays the sum of P0+P1 from RED STATUS lines (`:500-505`). GREEN contributes 0. A RED line with P0=0 and P1=0 still does not block (`:509`).

Before breaking on `total_p0p1 == 0` (`:507`), scan `## Deferred — follow-up required`. Reuse the 2f extraction rule (`:625`) for the section's extent, its row headings, severity, the `Scope` token, and `Discharged:`. Do not invent a second parser for those. Also read each row's `**Where:**` and `**Suggested fix:**` verbatim; that extraction rule does not yield them. A missing field classifies the row in-scope. A row withholds the break when its `Finding` severity is P0 or P1, it has no `Discharged:` field that names a section (empty, unparseable, or names no section counts as absent, the same test as the reviewers' Discharge bullet), and the ceiling test classifies it as in-scope. That includes a grill row whose token is `operator`. A `?` from the extraction rule is not one case. These rules apply only to a row with no valid `Discharged:` (empty, unparseable, or names no section counts as absent). A `Scope` token the render would print as `?` does not withhold by itself. Classify it with the step-2 classifier, the same as `operator` and any other token. Withhold only when that classification is in-scope; the 2e action is the R2(c) discharge, and that same fold repairs `Scope` to `in-scope — <the step-2 citation>`. A severity or a `D-<n>` id the render would print as `?` is not rewritten. The severity is read as P1 for this test only. Scope still comes from the step-2 classifier, not from the malformation. When that classification is in-scope, withhold and print `green withheld: D-<n> — malformed row`, using `D-?` when the id does not parse. Do not discharge the row in that round, and do not emit `fixed: repaired`. The next round's reviewers file `routing violation: D-<n>` (or `routing violation: D-?`), and that finding's ordinary R2(c) discharge is what clears it. When the classification is out-of-scope, do not withhold and do not discharge; the row stays live.

When the scan is clean, break as today: 2g, then Phase 3, which writes the green marker.

When the scan is not clean, do not break, do not run 2g, and do not write `verdict: green`. Print `green withheld: <D-ids> — undischarged in-scope P0/P1`, or `green withheld: D-<n> — malformed row` when the withhold is an unparseable severity or id. Append `guarantee: withheld <D-ids>` to this round's `synthesis.md`. Discharge each row the ceiling classifies as an undischarged in-scope P0 or P1 in this round's 2e under R2(c), including the `Scope` repair a grill row or a `?` scope token needs. A `?` severity or id is the withhold above and is not discharged in that round. A scan discharge with no reviewer finding is dispositioned `guarantee/D-<n> (P<sev>) "<row title>" — fixed: discharged D-<n> — edited § <a>; § <b> (§ Deferred — follow-up required)`. These rows are not added to `total_p0p1`.

Define loop-red once, in § 2d, after the gate formula (`:500-505`) and before the break (`:507`): the round is red when `total_p0p1 > 0` or the guarantee scan withheld. The formula for `total_p0p1` is unchanged. `:513` ("If still red and `round < round_cap`"), `:567` ("If still red and `round == round_cap`"), and `:603` ("If after round round_cap the spec is still red") use that definition and no other.

- If `round < round_cap`, loop-red enters 2e at `:513`. The next round's reviewers see the discharge.
- If `round == round_cap`, loop-red enters 2e at `:567`. Discharge inside that round's 2e, then take the 2f red write (`:603`) with `gate:` equal to the STATUS sum (0 when no reviewer P0/P1 remains). Phase 3 is not rendered. Ship-spec already halts on `verdict: red` whatever `gate` is (`skills/ship-spec/SKILL.md:33`).

In the halt block (`:605-622`), when no reviewer P0/P1 remains, Remaining P0/P1 is the line `GREEN WITHHELD: <D-ids>` and option 4 is not offered. Option 1, patch manually and re-run `/spec-cycle`, is how that discharge is reviewed. When reviewer P0/P1 titles remain, Remaining lists those titles and options 1–4 stay, including option 4. 2f-i (`:634-735`) is not edited.

The scan is this skill's instruction to the agent executing it, the same layer as the rest of § 2e. It is not `check_spec.py` and it is not the author-side ground-truth gate (VHS-26, out of scope).

At the top of Phase 3, before the green write (`:772`), the skill states, in these words:

> A review-produced green verdict (`source: review`) from a run under this rule is never written while an in-scope P0 or P1 sits undischarged in `## Deferred — follow-up required`. Attest mode and green markers issued before this change are outside this guarantee and are not edited.

The marker's keys are unchanged. `gate: 0` on a green marker still means the STATUS sum was 0. The scan has already passed by the time Phase 3 writes it.

In the Phase 3 template (`:776-809`), after the scale block and before `=== FOLLOW-UPS ===`, always render:

```text
Synthesis: docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/synthesis.md
Deferred rows: <u> undischarged (<out> out-of-scope, <op> operator, <x> other), <d> discharged. Undischarged in-scope P0/P1: 0.
```

`<u>`, `<out>`, `<op>`, `<x>`, and `<d>` count rows by the raw `Scope` token the 2f render already uses. `<x>` is the count of tokens that render prints as `?`. It can be non-zero on a green path: an out-of-scope row whose token prints `?` does not withhold. The tally reuses the 2f extraction rule for extent, headings, severity, the scope token, and `Discharged:`, and also reads `**Where:**` and `**Suggested fix:**`. A missing field classifies in-scope, the same reading as the guarantee scan. The in-scope figure is the guarantee scan's count and is 0 on every path that reaches this template. An absent deferred section renders all zeros. No marker field carries these numbers.

### Failure mode

Append to the deferral-row failure mode (`:923`): an undischarged in-scope P0 or P1 row, including a grill row the ceiling classifies as in-scope, is a routing violation on the next review run and is not a legal resting state. A review-produced green verdict is never written while one remains. Attest mode and markers written before this change are outside that. A `deferred:` disposition aimed at such a row does not close as `DEFERRED`.

### Docs

Reference `:89`, `:91`, `:92`, `:96-104` and `AGENTS.md:27` go beyond brief row 9. They are required by brief Done-when "describe the new rule" because those lines restate the gate break, the recount, the halt, Phase 3, and the spec-cycle summary that this change alters.

`docs/spec-workflow-reference.md:87`. The exception clause names an undischarged in-scope P0 or P1 row, grill rows the ceiling classifies as in-scope included, where it now names only "an in-scope P0 row without `Discharged:`".

`:89` (step 5). Green is the STATUS sum equal to zero and the guarantee scan clean. "Still red" in steps 6–8 is loop-red: `total_p0p1 > 0` or the scan withheld. The sum itself is unchanged. A review-produced green verdict is not written while an undischarged in-scope P0 or P1 row remains.

`:90` (step 6). The entry is loop-red while `round < round_cap`. The defer parenthetical states that an in-scope P0 or P1 folds at every site, the site count is a cost note, and deferral is the out-of-scope finding with two or more sites.

`:91` (step 7). The entry is loop-red at `round == round_cap`. The recount sentence also states that an in-scope P0 or P1 is not reverted to a deferral.

`:92` (step 8). The halt entry is loop-red. When no reviewer P0/P1 remains, Remaining P0/P1 is `GREEN WITHHELD: <D-ids>` and option 4 is not offered. When reviewer titles remain, options 1–4 stay.

`:94`. `DEFERRED` is not the closure state of an undischarged in-scope P0 or P1. After the reports are saved and before the gate break, the author writes `round-<N>/synthesis.md` (Act on / Consider / Noted / Dismissed, plus an Agreement Map). The gate sum does not read that file.

`:96-104`. Phase 3 also shows the synthesis path and the deferred-row tally, and states the guarantee sentence from Decision 6.

`AGENTS.md:27`. The spec-cycle bullet states that a review-produced green verdict is never recorded while an undischarged in-scope P0 or P1 remains in `## Deferred — follow-up required`, and that each round writes `synthesis.md` without changing the STATUS gate.

`AGENTS.md:109`. The same exception clause as `:87` of the reference: an undischarged in-scope P0 or P1 row, including a grill row the ceiling classifies as in-scope, is still filed as a P0. The sentence that those definitions do not change with tier stays.

## Test plan

The suite does not execute these skills, and no test pins the routing text. Under `tests/`, `ceiling` occurs only in `tests/fixtures/session-handoff/legacy-flat.md` (`:15`, `:31`, `:41`, `:45`, `:46`), all of them a queue-retry fixture. No new test module and no grep gate. The scenario walk is the evidence the suite does not provide. The implementer reads the landed text against each row and records pass or fail in the PR body.

| # | Scenario | Expected reading of the landed text |
|---|---|---|
| 1 | Ordinary multi-site in-scope P1 | The ceiling's third bullet folds it at every site and records `(sites: <k>)`. It is not a row in `## Deferred — follow-up required`. |
| 2 | Recount whose true site count reaches two, original finding an in-scope P1 | The revert condition requires the original to be out-of-scope, so this finding keeps the fold and gains `(recount: <k> sites, fold kept)`. No deferral row. |
| 3 | Legacy undischarged in-scope P1 row on a re-run | The ceiling bullet files `routing violation: D-<n>`. The `deferred:` closure paragraph does not mark `DEFERRED`. R2(c) discharges the row on the fold. |
| 4 | Grill row holding an in-scope P1 on a re-run | The grill bullet keeps the propagation-sites exemptions and withdraws the ceiling exemption. Step 2 classifies the `operator` token on `Where` and `Suggested fix`; in-scope is a routing violation and a discharge, with `Scope` repaired to `in-scope` in that same fold. |
| 5 | Dismissed P0 or P1 | The finding is under Dismissed in `synthesis.md` and remains in that round's STATUS sum. Nothing in 2d subtracts it. A later round's closure is what retires it. |
| 6 | Final-round routing of an in-scope P1 | `:576` folds it. It is not deferred. A round that is otherwise red still halts red after the fold. |
| 7 | Empty review versus a failed reviewer | "No findings." plus a parseable GREEN STATUS is a Noted line and can be part of a green round. A missing STATUS or a 2c stub is Act on at P0 and blocks, per `:489-494` and the reviewer-status-drift failure mode. |
| 8 | Green write with a live in-scope row | The guarantee scan withholds the break and does not write `verdict: green`. loop-red (`total_p0p1 > 0` or the scan withheld) is what `:513`, `:567`, and `:603` test, so a zero sum with a withhold still enters 2e and, at `round_cap`, 2f. Attest mode's section has no diff, so an attestation can still record green. |
| 8b | Scan discharge with no reviewer finding | The 2b note and the scan discharge use `guarantee/D-<n> (P<sev>) "<row title>" — fixed: discharged D-<n> — edited § <a>; § <b> (§ Deferred — follow-up required)`. `:449-451` names that line as an exception beside the recount's revert line. The Routing violations bullet, identical in the four agents, verifies it against row `D-<n>`'s `Discharged:` and the sections it names, does not treat its absence from round N−1 as a defect, and does not add it to the closure table. loop-red is what enters 2e, so the discharge has a manifest line when the STATUS sum is 0. |
| 10 | Odd Scope token, and a `?` severity or id | An out-of-scope row whose token prints `?` does not withhold, and Phase 3 may count it in `<x> other`. An unparseable severity is read as P1 and is not written into `Finding`. An unparseable id is not renumbered. Either one withholds only when step 2 says in-scope, as `green withheld: D-<n> — malformed row` (`D-?` when the id does not parse), with no edit that round. The ceiling bullet states that a `Finding` severity that does not parse is read as P1 for this test, so the next round files that `routing violation:`. It is discharged under R2(c) without rewriting `Finding` or the heading. An out-of-scope row with a `?` severity or id stays live and does not withhold. |
| 8c | Halt when the sum is 0 and the scan withheld | Remaining P0/P1 is `GREEN WITHHELD: <D-ids>`. Option 4 is not on the menu. Option 1 is the re-run that reviews the discharge. When reviewer P0/P1 titles remain, options 1–4 stay. 2f-i is not edited. |
| 9 | One-site P2 | The synthesis table is first-match and its first row is P2, P3, or P4, so this finding is Noted. Steps 0–3 are not applied to it. `:527` still fixes it or lists it in `## Deferred (P2+)`. It is not Act on. |

Also confirm: the four Deferred-findings blocks are byte-identical to each other; `skills/ship-spec/SKILL.md`, `skills/spec-tickets/SKILL.md`, and `skills/spec-close/SKILL.md` have no diff; the verdict-marker template has no new key; `:520` and `:521` are unchanged; `git diff --name-only main...HEAD` lists only the five Scope paths.

## Test command

```text
python -m unittest discover -s tests -p 'test_*.py' && python lint.py --strict
```

## Done when

- `/spec-cycle` § 2e does not route an in-scope P1 to defer, whatever its site count, in ordinary rounds, in the re-fold recount, and at round `round_cap`.
- A review-produced green verdict from a run under this rule is never written while an in-scope P0 or P1 sits undischarged in `## Deferred — follow-up required`. The skill states that, and names attest mode and earlier markers as outside it.
- The four reviewer agents and the skill state the same ceiling, in the complete Deferred-findings block and in the `deferred:` closure rule.
- `/spec-cycle` writes the four-bucket synthesis and an Agreement Map every round, including green rounds and rounds with no findings, without changing any reviewer's STATUS count.
- The test plan's scenario table is the record of the expected outcome for an ordinary multi-site in-scope P1, a recount that reaches two sites, a legacy in-scope P1 row on re-run, a grill row holding an in-scope P1 on re-run, a dismissed P0 or P1 awaiting reviewer closure, final-round routing, and an empty review versus a failed reviewer.
- `docs/spec-workflow-reference.md` and `AGENTS.md` describe the new rule.
- `python -m unittest discover -s tests -p 'test_*.py'` and `python lint.py --strict` pass. They do not prove the invariant. The scenario walk does.

## Out of scope

- Attest mode and already-issued green markers (Decision 6). `## Attest mode` is not edited.
- Delta-scoped review passes and the closure ledger (VHS-27). `synthesis.md` is only required to sit where that ledger can find it later.
- The author-side ground-truth gate and `check_spec.py` (VHS-26). The guarantee scan is a step in this skill, not that program.
- The other borrowings listed beside the synthesis buckets in the distillation: the doubt-driven reconcile order, the 3-cycle bound, the "doubt theater" red flag, and withholding the author's rationale from reviewers.
- The out-of-scope defer rule, the single-site fold rule (Decision 5), and routing steps 0–2.
- The gate formula `total_p0p1 == 0` and the severity scale's definitions. The break's second conjunct does not change the sum. loop-red does not change it either. It is only the test `:513`, `:567`, and `:603` use to enter 2e and 2f.
- `round_cap`, lens selection, and tier behavior (VHS-55).
- `/ship-spec`, `/spec-tickets`, and `/spec-close`. No informational field is added to the verdict marker.
- The Act-on-count heuristic (Decision 15) and the token-measurement lesson. The ticket's second lesson ("Token hygiene needs measurement… We don't yet have cost evidence.") is VHS-59. This spec does not address it.

## Deferred (P2+)

- correctness/R1/F-5 (P3): not folded. No spec change. Plane retrieve already matched the brief, and the ticket states no acceptance criteria.
- correctness/R1/F-6 (P3): not folded. The spec is grounded on `7abe102`, the commit the finding names.
- conventions/R1/F-3 (P4): not folded. `:603` is the paragraph that writes the red marker; `:602` is blank; `:604` is the opening fence.
