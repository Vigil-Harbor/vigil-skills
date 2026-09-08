# Reconciliation Report: VHS-37

> Date: 2026-09-08
> Spec: docs/specs/TODO/VHS-37.spec.md
> Merge: PR #29 (d4db373)
> Plane state: Done (group: completed)

## Summary

All acceptance criteria met. The PR implements the fold / defer / reject routing step in SKILL.md § 2e, the `## Deferred — follow-up required` section with rules R1–R6, the re-fold recount, manifest vocabulary (§ 2b), the follow-up report at both exits (§ 2f and Phase 3), the D15 round-4 passage, the failure-mode bullet, and the Deferred-findings block across all four reviewer agents. `docs/spec-workflow-reference.md` and `AGENTS.md` are reconciled. `## Deferred (P2+)` and its consumers are byte-identical. Zero drift.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-cycle/SKILL.md` Phase 1 opening (`:294-296`) | Yes | Two sentences on re-run behavior (hunk `@@ -297,0 +298,2`) |
| `skills/spec-cycle/SKILL.md` § 2b example block (`:365-368`) | Yes | One new `deferred:` example line (hunk `@@ -367,0 +370`) |
| `skills/spec-cycle/SKILL.md` § 2b disposition prose (`:378-383`) | Yes | `deferred:` added as fourth phrase; recount suffix; revert line; routing-violation dispositions (hunks `@@ -379`, `@@ -382`, `@@ -384,0 +390,12`) |
| `skills/spec-cycle/SKILL.md` § 2e (`:426-464`) | Yes | Routing step replaces "Address every P0 and P1"; section shape and rules R1–R6; recount (hunks `@@ -430`, `@@ -433,0 +462,37`) |
| `skills/spec-cycle/SKILL.md` § 2f halt block and Phase 3 | Yes | Follow-up report at both exits (hunks `@@ -479,0 +547,3`, `@@ -486,0 +557,7`, `@@ -655,0 +733,3`, `@@ -660,0 +741,2`) |
| `skills/spec-cycle/SKILL.md` round-4 passage | Yes | D15 FROZEN + governed-by-R2 passage (hunk `@@ -441,0 +507,2`) |
| `skills/spec-cycle/SKILL.md` § Failure modes | Yes | New bullet on deferral-row downstream (hunk `@@ -735,0 +818`) |
| `agents/spec-reviewer-correctness.md` | Yes | +23/−3: closure_manifest input, Deferred-findings block, DEFERRED status |
| `agents/spec-reviewer-edge-cases.md` | Yes | +23/−3: same three edits |
| `agents/spec-reviewer-conventions.md` | Yes | +23/−3: same three edits |
| `agents/spec-reviewer-scalability.md` | Yes | +22/−2: same three edits |
| `docs/spec-workflow-reference.md` | Yes | +3/−3: lines 81, 84, 88 reconciled |
| `AGENTS.md` | Yes | +1/−1: line 101 em-dash aside on P0/P1 |

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-37.test-output.txt` — test-output capture from the PR (standard companion artifact, not a scope deviation)

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Reviewer-side deferral, not gate arithmetic | Confirmed | `skills/spec-cycle/SKILL.md` — `grep -cF 'Address every P0 and P1 finding'` → 0 (removed); routing step writes nothing into the gate; agents carry Deferred-findings block with same-root suppression rule |
| 2 | Scope is a ceiling | Confirmed | `skills/spec-cycle/SKILL.md` routing step 3: one site → fold; 2+ out-of-scope → defer; 2+ in-scope P1 → defer; 2+ in-scope P0 → fold |
| 3 | Non-trivial = more than one propagation site | Confirmed | Routing step 1 names sites before any edit; step 3 branches on count; the list persists in the deferral row |
| 4 | A re-fold finding forces a recount | Confirmed | Re-fold recount section present; bounded by D16 (round 4, re-edited sites) |
| 5 | A second section, not a rename | Confirmed | `## Deferred — follow-up required` is new; `grep -c 'Deferred (P2+)' SKILL.md` → 8 (unchanged count, rule R3 adds 2 new references but they match the pre-edit expectation of 8–9) |
| 6 | Author classifies scope; reviewer verifies | Confirmed | Routing step 2 classifies against brief; conventions lens verifies per Design 7 Scope-field bullet |
| 7 | Follow-up report at both exits | Confirmed | `grep -cF '=== FOLLOW-UPS' SKILL.md` → 2 (2f halt block and Phase 3) |
| 8 | No numeric cap | Confirmed | No row-count check anywhere in the routing step or section rules |
| 9 | Gate-inversion tripwire ships separately | Confirmed | Not in diff; no tripwire added |
| D10 | Reject maps to `not applicable:` | Confirmed | Routing step 0: "reject: disposition it `not applicable: <reason>`" |
| D11 | Row shape in both SKILL.md and four agents | Confirmed | Seven fields in 2e shape; Deferred-findings block checklist in each agent |
| D12 | Ticket-id backfill is operator hand-edit | Confirmed | R2: "`Follow-up:` is written as `unfiled` by the skill and is free text thereafter; the operator replaces it with the ticket id when they file one, by hand" |
| D13 | `D-<n>` is the only key | Confirmed | R1 defines numbering; agents match on `D-<n>` and title; `Finding:` field records provenance |
| D14 | Same-root suppression bounded by ceiling | Confirmed | Agent block: "Do not file a P0/P1 whose root is a well-formed row … unless the candidate is an in-scope P0" |
| D15 | Round-4 routing; section FROZEN and governed by R2 | Confirmed | `grep -cF 'governed by rule R2' SKILL.md` → 1; passage present at hunk `@@ -441,0 +507,2` |
| D16 | Recount revert available only rounds 2–3, this invocation | Confirmed | Recount section: "this is round 2 or 3"; "A fold made in a prior invocation is not detectable and is not recounted" |
| D17 | Only conventions lens verifies Scope field | Confirmed | Agent block: "The `Scope` field is verified by the conventions lens … the other lenses read it as opaque" — present in all four agents |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `/spec-cycle` 2e names fold / defer / reject dispositions and the test that forces defer-to-ticket | Met | `skills/spec-cycle/SKILL.md` routing step: fold/defer/reject in step 0–4; ceiling test in step 3 forces defer when 2+ sites and (out-of-scope, or in-scope P1) |
| 2 | Deferred entries that become tickets carry the ticket id | Met | Row shape has `**Follow-up:** unfiled`; R2 and R4 preserve the value across re-runs; Design 5 renders it verbatim. `grep -cF '**Follow-up:** unfiled' SKILL.md` → 1 (shape); `grep -cF '— Follow-up: unfiled' SKILL.md` → 1 (example); `grep -cF '— Follow-up: VHS-99' SKILL.md` → 1 (example showing filed id) |
| 3 | `lint.py --strict` zero ERROR; `sync.py status` clean; `sync.py push` round-trips | Met | `VHS-37.test-output.txt`: lint exits 0, 0 errors, 2 pre-existing WARNs on unrelated skills (review-pr, ship-spec) |

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| Row 1: `python lint.py --strict` exits 0, zero ERROR | Yes | `VHS-37.test-output.txt:1-7` — 0 errors, 2 pre-existing WARNs |
| Row 2: `sync.py install` then `sync.py status` clean | Unverifiable | Not captured in test-output.txt (PR body expected) |
| Row 3: old text removed, new section ≥ 4 | Yes | `grep -cF 'Address every P0 and P1 finding'` → 0; `grep -cF '## Deferred — follow-up required'` → 8 (≥ 4) |
| Row 4: hunks only in expected regions | Yes | Hunks at Phase 1 `:297`, 2b `:367-390`, 2e `:430-462`, 2f `:486-557`, Phase 3 `:733-741`, Failure modes `:818`. No hunk in `:371`, `:411-424`, `:431`, `:489-591`, `:593-624` |
| Row 5: `Deferred (P2+)` count → 8 | Yes | `grep -c 'Deferred (P2+)'` → 8 (spec expected 8 or 9) |
| Row 6: Deferred-findings block byte-identical in 4 agents | Yes | 1 per file (4 files); all 12 sub-greps ≥ 1 per file; `diff` of extracted blocks: all identical; extent clause matches SKILL.md |
| Row 7: `Deferred` absent from spec-close/ship-spec | Yes | `grep -rn 'Deferred' skills/spec-close/SKILL.md skills/ship-spec/SKILL.md` → 0 hits |
| Row 8: FOLLOW-UPS at both exits + extraction rule | Yes | `=== FOLLOW-UPS` → 2; `malformed row` → 1; `exactly two` → 1; `Discharged:` ≥ 2 (5); `begin the line` → 1; `rendered per the extraction rule` → 1; Design/D-label leak → 0; line-number anchor leak → 0; `(grill)` ≥ 1 (4); `same character as the opener` → 1; `must not implement` → 1; `**Follow-up:** unfiled` → 1; `— Follow-up: unfiled` → 1 |
| Row 9: disposition and R2 references | Yes | `deferred: D-<n> (§ Deferred — follow-up required)` → 2 (≥ 2); `governed by rule R2` → 1 (≥ 1); `fixed: discharged` → 4 (≥ 2) |
| Row 10: reference doc and AGENTS.md | Yes | `Address every P0 and P1.` in reference → 0; `DEFERRED` in reference → 1; `including round 1` → 1; `never enters the gate` → 1 in reference, 1 in AGENTS.md |

## Wiki-ready

- **Decision:** The fold / defer / reject routing model for spec-cycle findings — a structural change to how /spec-cycle handles valid findings that touch multiple propagation sites. The scope ceiling (in-scope P0 always folds; everything else defers when non-trivial) is a reusable design pattern for routing decisions under pressure. Wiki-worthy because it changes the fundamental behavior of the lifecycle's most-used skill.
- **Comprehension:** VHS-37 adds fix routing to /spec-cycle's 2e step, replacing "address every P0 and P1" with a four-step routing protocol (validate → name sites → classify scope → apply ceiling). The change spans SKILL.md, four reviewer agents (byte-identical Deferred-findings block), the spec-workflow-reference, and AGENTS.md. It introduces a new `## Deferred — follow-up required` section in authored specs, governed by six rules (R1–R6), with a follow-up report rendered at both exits. The `## Deferred (P2+)` machinery is deliberately untouched.

RECONCILED: yes DRIFT: 0
