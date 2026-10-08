# Reconciliation Report: VHS-47

> Date: 2026-10-08
> Spec: docs/specs/TODO/VHS-47.spec.md
> Merge: PR #34, squash commit `aad9971` (ship commit `24541d8`, review-fix commit `3bb7412`)
> Plane state: Done (group: completed)

## Summary

Every file the spec names is in the diff and every decision is reflected in the shipped text. The three brief criteria are met. Two files the spec does not list are in the diff: the review-gate record and the test-output capture, both lifecycle artifacts `/ship-spec` writes. Two post-spec clarifications landed through review (a Phase 0 routing sentence for `--attest`; `ticket:` and `spec:` named at every write point) and both sit inside the spec's decisions rather than diverging from them.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-cycle/SKILL.md` | Yes | +94/−5. New `## The verdict marker` (L25) and `## Attest mode` (L815); pending write (L371), red write (L587), green write (L757); 2f-i clause (L717); Phase 3 `Verdict:` line (L765); Phase 0 routing sentence (L77, added by the review gate) |
| `skills/ship-spec/SKILL.md` | Yes | +39/−2. Phase 0 step 1b (L16–50); preflight summary names the state; PR body `Spec verdict:` line (L342); "Spec not green" rewritten (L421); tool-use bullet |
| `skills/spec-tickets/SKILL.md` | Yes | +37/−6. Step 2 clause; step 3 relabelled "Heading check" (L35); step 4 verdict read (L36–63); step 6 line; approval block `Verdict:` (L118); Phase 4 re-read (L159); failure modes (L205–206); tool-use bullet |
| `docs/spec-workflow-reference.md` | Yes | +7/−2. Attest invocation; `### Verdict marker` (L102); spec-tickets bullet (L140); ship-spec sentence (L158) |
| `AGENTS.md` | Yes | +3/−3. Items 2, 3, 4 |
| `README.md` | Yes | +3/−3. Three stage bullets |
| `docs/customizing.md` | Yes | +1/−0. Marker path in § Spec & brief layout (L76) |

Leave-alone paths (`skills/spec-close`, `skills/spec-brief`, `skills/review-pr`, `agents/`, `sync.py`, `lint.py`, `skills/ship-spec/states.json`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `tests/`): no diff, checked by the test command.

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-47.review.md` — the Phase 3b review-gate record (`/ponytail-review`, subagent mode, 1 fixed, 3 recorded). A lifecycle artifact, archived with the spec.
- `docs/specs/TODO/VHS-47.test-output.txt` — test-gate capture, exit 0. Same.

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | The marker file: path, template, field rules | Confirmed | `skills/spec-cycle/SKILL.md:25–50` — template block and five field-rule bullets match the spec verbatim |
| 2 | The fingerprint: `sha256-lf:` over CR-stripped bytes; `none` on failure | Confirmed | `skills/spec-cycle/SKILL.md:52`, restated identically at `skills/ship-spec/SKILL.md:16`; per-reader `fingerprint: none` rule in both |
| 3 | When /spec-cycle writes: pending (start of Phase 2), green (top of Phase 3), red (2f), 2f-i untouched, failed write does not change outcome | Confirmed | `:371` pending; `:757` green ("Every green run reaches this point"); `:587` red; `:717` "never rewrites the verdict marker"; `:56` failed-write rule with the three print positions; `:765` Phase 3 `Verdict:` line and its three forms |
| 4 | Attest mode: usage, no reviewers, seven-heading check, already-green exit, prompt, `replaces:` | Confirmed | `skills/spec-cycle/SKILL.md:815–843`; Phase 0 routing sentence at `:77` (review-gate fix) implements "runs none of Phase 0 steps 2 to 8" |
| 5 | Reader classification table, six rows in order, first match wins | Confirmed | `skills/spec-cycle/SKILL.md` § Reading the marker; same rows and order at `skills/ship-spec/SKILL.md:18–25`; `skills/spec-tickets/SKILL.md:38–44` carries the five-row adaptation |
| 6 | /ship-spec step 1b: green passes, red halts (four-line block), four states prompt, PR-body line | Confirmed | `skills/ship-spec/SKILL.md:16–50`; red block `:33–36` ends in the `--attest` line; `:47` "spec verdict needs an operator — stopping"; `:342` PR body |
| 7 | /spec-tickets: verdict read without fingerprint; red halts before draft; verdict line in approval block; Phase 4 re-read | Confirmed | `skills/spec-tickets/SKILL.md:36–63`; `:52` "does not file tickets for a red spec"; `:58` "fingerprint not checked on this host"; `:118`; `:159` "If the spec is unchanged, read the verdict marker again" (CodeRabbit wording fix) |
| 8 | No backfill; /spec-close and /spec-brief unchanged | Confirmed | `git diff --name-only origin/main -- skills/spec-close skills/spec-brief` empty (test command) |
| 9 | Scale is a non-factor | Confirmed | One file per spec, one read per run; no scale machinery added |
| 10 | Capability blocks untouched; census stays 11 | Confirmed | Test command's `requires:` grep empty; `tests/test_lint.py` 6/6 at census 11 |
| 11 | Room for later work: writes through three named points, one classification table | Confirmed | `skills/spec-cycle/SKILL.md:54` "Write points" paragraph names the three points and the attest writer |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | /spec-cycle records its final verdict in a form another skill can read without parsing review reports | Met | `skills/spec-cycle/SKILL.md:25` `## The verdict marker`; key-value marker with `verdict:`, `round:`, `gate:`, `date:`, `fingerprint:` |
| 2 | /spec-tickets and /ship-spec check it in preflight and do not proceed silently on a spec that is red or was never reviewed | Met | `skills/ship-spec/SKILL.md:16` step 1b (red halts, missing prompts); `skills/spec-tickets/SKILL.md:36` step 4 (red halts; missing shown as `Verdict: missing — no recorded review for this spec` for approval) |
| 3 | The CodeRabbit thread on PR #31 can be pointed at this ticket | Met | Reply posted on PR #31 thread (comment 4220265225) linking PR #34: https://github.com/Vigil-Harbor/vigil-skills/pull/31#discussion_r4223897581 |

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| Mechanical gate 1–8 (lint tests, close-log tests, strict lint, heading counts, `verdict.md` in three skills, red block, leave-alone diff, `requires:` diff) | Yes | Spec `## Test command`; run exit 0 three times (ship, post-review-gate fix, post-CodeRabbit fix); capture at `docs/specs/TODO/VHS-47.test-output.txt` |
| Review checklist (13 rows) | Yes | Checked during `/ship-spec` Phase 2 and by the review gate; fingerprint rule identical in two skills, reading rule in three, table order identical |
| Behavioural: a green `/spec-cycle` run leaves a marker `/ship-spec` passes | Not yet | Open post-install check (PR #34 body). This ticket's own `/ship-spec` ran the pre-change skill |
| Behavioural: a spec with no marker meets the confirm | Not yet | Same |

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:
- Decision 1–3, 5: the verdict is a file in the reviews directory, not a line in the spec; a fingerprint over CR-stripped bytes ties it to the exact text; a failed write never changes the run's outcome; readers classify by one table and never recompute the gate. Rejected: /spec-tickets parsing reviewer reports (CodeRabbit's PR #31 proposal), halting the review when a marker write fails (CodeRabbit outside-diff finding on PR #34, deferred by the spec).
- Decision 4, 6, 7: attest mode as the operator's recorded claim; ship-spec halts on red and prompts on everything else; spec-tickets shows the verdict and lets approval confirm it, without a fingerprint.
- Comprehension: a new data flow between three skills (writer, halting reader, advisory reader); what breaks if the marker format drifts; the first review-gate run in anger (one Fix-or-record finding, three recorded).

RECONCILED: yes DRIFT: 2
