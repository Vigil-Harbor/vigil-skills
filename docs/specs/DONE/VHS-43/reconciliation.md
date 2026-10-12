# Reconciliation Report: VHS-43

> Date: 2026-10-12
> Spec: docs/specs/TODO/VHS-43.spec.md
> Merge: PR #40, squash commit d3730b16299ea523c4824068cdb9406bedf33ff1
> Plane state: Done (group: completed)

## Summary

The shipped code matches the spec on every Scope path, all seventeen Decisions and all seven Done-when criteria. One deliberate drift: the reviewers' ceiling bullet names the scope-classification step in words where the spec quoted a line anchor. The spec was authored and implemented by a Cursor cloud agent; its review reports and verdict marker are not on disk here, so this close archives the brief, the spec and this report only.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-cycle/SKILL.md` | Yes | As specified (+110 lines net of rewrites): ceiling, Act step, grill paragraph, R2(c), R5, recount, final-round routing, 2b manifest, new § 2c-s, loop-red and guarantee scan in § 2d, 2f halt and example, Phase 3, failure mode. |
| `agents/spec-reviewer-correctness.md` | Yes | Deferred-findings block, `deferred:` closure paragraph, step-7 sentence. |
| `agents/spec-reviewer-edge-cases.md` | Yes | Same. |
| `agents/spec-reviewer-scalability.md` | Yes | Same. |
| `agents/spec-reviewer-conventions.md` | Yes | Same. |
| `docs/spec-workflow-reference.md` | Yes | `:87`, `:89`–`:92`, `:94`, Phase 3 description. |
| `AGENTS.md` | Yes | Spec-cycle bullet `:27`, severity bullet `:109`. |

Unexpected files in diff (not in spec): none. `git show --stat d3730b1` lists exactly these seven files.

Leave-alone checks, each by section hash or path diff between `7abe102` and `d3730b1`: `## Attest mode` identical; `## The verdict marker` identical; § 2f-i identical; `skills/ship-spec`, `skills/spec-tickets`, `skills/spec-close`, `tests/`, `sync.py`, `README.md` no diff; `docs/specs/` not in the diff.

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | An in-scope P1 always folds | Confirmed | `skills/spec-cycle/SKILL.md:584` — 'two or more sites and in-scope → **fold**, whatever the severity (P0 or P1)'; the old 'two or more sites, in-scope, P1 → **defer**' bullet is gone (no match). |
| 2 | Multi-site is a cost note | Confirmed | `skills/spec-cycle/SKILL.md:584` — 'append ` (sites: <k>)` … The note does not route, and no consumer parses it.' |
| 3 | Lead-judgment synthesis | Confirmed | `skills/spec-cycle/SKILL.md:498` — '### 2c-s. Lead-judgment synthesis'; four buckets and Agreement Map at `:504-517`. |
| 4 | An empty review is valid | Confirmed | `skills/spec-cycle/SKILL.md:510-511` — a "No findings." lens with a parseable STATUS is Noted; a missing STATUS or a 2c stub is Act on at P0. |
| 5 | Out-of-scope routing is unchanged | Confirmed | `skills/spec-cycle/SKILL.md:582-583` — both bullets byte-identical to `7abe102:520-521`. |
| 6 | Guarantee covers review-produced verdicts only | Confirmed | `skills/spec-cycle/SKILL.md:565` — '**Guarantee scan.** Before breaking on `total_p0p1 == 0`…'; `:837` — the guarantee sentence, naming attest mode and earlier markers as outside it. Attest section unchanged. |
| 7 | Grill rows obey the ceiling on re-run | Confirmed | `skills/spec-cycle/SKILL.md:587` — 'a legal resting state only until the next review run'; `agents/spec-reviewer-correctness.md:36` — 'It is not exempt from the ceiling.' |
| 8 | Synthesis has no authority over the gate | Confirmed | `skills/spec-cycle/SKILL.md:500` — 'It does not change a STATUS line, a finding id, or `total_p0p1`'; `:515` — 'A dismissed P0 or P1 is listed and remains in the STATUS sum'. |
| 9 | No grandfathering | Confirmed | `agents/spec-reviewer-correctness.md:38` — a P0 or P1 row with no `Discharged:` that is in-scope 'is itself a routing violation'; `:73` — such a row does not close as `DEFERRED`. |
| 10 | Brief-exceeding stop covers an in-scope P1 | Confirmed | `skills/spec-cycle/SKILL.md:584` — 'Print `fold exceeds brief: <finding id> (<k> sites) — …; marker left pending`. Do not defer the finding instead of stopping.' The spec's § Ceiling bullet quote omitted the print; the implementer added it to match this Decision and said so in the PR body. |
| 11 | Recount reverts only an out-of-scope fold | Confirmed | `skills/spec-cycle/SKILL.md:627` — 'and the original finding is out-of-scope, and 2 ≤ round < round_cap'; `:628` — 'an in-scope P0 or P1' in the Otherwise bullet. |
| 12 | Who classifies a grill row | Drifted | The classifier rule is as specified (`agents/spec-reviewer-correctness.md:38`: every lens, step 2 verbatim on `Where` and `Suggested fix`, stated tokens not re-derived). The spec's replacement text cited the step as `skills/spec-cycle/SKILL.md:518`; the shipped text reads 'the spec-cycle skill's scope-classification routing step'. The anchor was stale on arrival (the step is at `:580` after this same change) and names a path that does not exist where installed agents run. Fixed in the PR's second commit before merge. |
| 13 | Where synthesis is written | Confirmed | `skills/spec-cycle/SKILL.md:519` — 'Write `docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/synthesis.md`'; `:550` — the closed-issues scan 'does not read `synthesis.md`'; `agents/spec-reviewer-correctness.md:48`. |
| 14 | Which bucket holds an out-of-scope P0 or P1 | Confirmed | `skills/spec-cycle/SKILL.md:508` — '| Defer: valid out-of-scope P0 or P1 with two or more sites | Consider |'. Table order Fold, Defer, Reject as specified. |
| 15 | No Act-on cap | Confirmed | No 'more than 5' or 'under-filtering' text in the skill; the severity-inflation failure mode at `:948` is unchanged. |
| 16 | Deferred count is print-only | Confirmed | `skills/spec-cycle/SKILL.md:873` — 'Deferred rows: <u> undischarged (…), <d> discharged. Undischarged in-scope P0/P1: 0.'; verdict-marker section identical, no new key. |
| 17 | Tier big | Unverifiable | A property of the run, not of the diff. `round_cap`, lens selection and tier text are unchanged (`docs/spec-workflow-reference.md:145`). |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | § 2e does not route an in-scope P1 to defer, in ordinary rounds, the recount, and at `round_cap` | Met | `skills/spec-cycle/SKILL.md:584` (ceiling), `:627-628` (recount), `:639` — 'An in-scope P1 folds at round `round_cap` under that ceiling and is not deferred there.' |
| 2 | A review-produced green is never written over an undischarged in-scope P0/P1; the skill says so and names attest and earlier markers as outside | Met | `skills/spec-cycle/SKILL.md:565-569` (scan and withhold), `:837` (the sentence, in the spec's words). |
| 3 | The four agents and the skill state the same ceiling, in the whole block and the closure rule | Met | The Deferred-findings block hashes identically across the four agents at `d3730b1`, as does the `deferred:` closure paragraph; `skills/spec-cycle/SKILL.md:585` and `:618` use the same in-scope P0-or-P1 test. |
| 4 | Synthesis every round, including green and empty rounds, without changing a STATUS count | Met | `skills/spec-cycle/SKILL.md:500` — 'This step runs every round … including a round that later goes green and a round whose lenses all returned no findings.' |
| 5 | The scenario table is the record of the expected outcomes | Met | PR #40 body, "Scenario walk": rows 1–10 including 8b and 8c, each marked Pass against the landed text. |
| 6 | `docs/spec-workflow-reference.md` and `AGENTS.md` describe the new rule | Met | `docs/spec-workflow-reference.md:89` — 'Green is that sum equal to zero and the guarantee scan clean'; `:94`; `:98`; `AGENTS.md:27`, `:109`. |
| 7 | Test command passes | Met | Run on `main` @ `d3730b1`, 2026-10-12: 127 tests OK (3 skipped); `lint.py --strict` 0 errors, 0 warnings. |

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| Scenario walk, rows 1–10 with 8b and 8c | Yes, as a recorded reading | PR #40 body. The spec adds no test module by design; the suite does not execute skills. |
| Four Deferred-findings blocks byte-identical | Yes, re-checked at close | Section hash equal across the four agents at `d3730b1`. |
| ship-spec / spec-tickets / spec-close have no diff; marker has no new key; `:520-521` unchanged; only the Scope paths in the diff | Yes, re-checked at close | See Scope, leave-alone checks. |

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:
- Decision 1 + 6 + 9: what "green" means after VHS-43 — an in-scope P0 or P1 never rests in the deferred section under a review-produced green; scoped to `source: review`, with attest and earlier markers deliberately outside. Constrains every future spec-cycle change, and refines the VHS-37 routing protocol.
- Decision 6 mechanism: the guarantee scan and `loop-red` — the gate sum is unchanged, but the break has a second conjunct. Non-obvious: a round with zero reviewer findings can be red, and a `round_cap` halt can carry `gate: 0`.
- Decision 8 + 13 + 14: the synthesis reports and prioritizes and has no authority over the gate; `synthesis.md` is not a reviewer report and no closure input reads it. VHS-27 builds on where it sits.
- Decision 12 and its drift: one row classifier, used by reviewers, the scan and the Act step; and agents must not cite skill line numbers or repo paths, because they run installed, in other repos.
- Comprehension: the changed shape of the review loop (2c → 2c-s → 2d scan → 2e), what would break, and the provenance gap — brief written and Codex-reviewed locally, spec authored and implemented by a Cursor cloud agent, review reports not preserved.

RECONCILED: yes DRIFT: 1
