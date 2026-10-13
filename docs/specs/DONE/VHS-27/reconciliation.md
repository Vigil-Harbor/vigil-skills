# Reconciliation Report: VHS-27

> Date: 2026-10-13
> Spec: docs/specs/TODO/VHS-27.spec.md
> Merge: PR #41 (squash f64bebe)
> Plane state: Done (group: completed)

## Summary

The shipped change matches the spec in scope and in every decision. All seven files the spec names are in the diff, none of the files it says to leave alone was touched, and the two extra files are the expected ship-spec gate records. All 17 decisions (the tier decision plus Decisions 1-16) have their rule text in the shipped prose. Seven of the nine "Done when" bullets are met; the other two describe run-time behaviour that nothing has executed, so they are unverifiable rather than unmet.

Four design clauses drifted from the spec text:

1. A failed pending-marker write over a green marker now stops the run before dispatch. The spec says the pending write is unchanged, and the pre-change skill said "print the failed-write line and continue". Added in CodeRabbit round 1 (pre-squash commit `32b457b`).
2. The `# Delta scope` block in the four reviewer agents carries one sentence the spec's verbatim block does not: a `deleted: true` entry is read from the predecessor `spec.copy.md`. Same round.
3. The `changed_regions` input bullet in the four agents carries one sentence the spec's bullet does not: it names the `(before first heading)` sentinel. The spec defines that sentinel for the skill (spec § Changed regions) but did not put it in the agent bullet. Same round.
4. The raw-path definition was condensed. The spec bans a leading quote and any `=>`, tab or backslash anywhere in the line. The skill says "with no leading `"`, `=>`, tab, or backslash", which can be read as banning all four only at line start. The review gate recorded this as finding 6 and did not act on it.

Items 1-3 are deliberate review-driven additions. Item 4 is an unfixed wording weakness.

How this was verified: every Confirmed and Met row below was checked by grep or file read at `f64bebe`. These are prose skills and agents. The lint and unit suite do not execute them, and no `/spec-cycle` delta run has been made with the shipped skill, so "Confirmed" means the rule text is present, not that an agent was observed following it. The scenario walks in the spec's test plan were done by reading.

Shared-block check (SHA-256 of each extracted block, first 16 hex digits, same value in all four agent files):

| Block | Hash | Identical across four? |
|---|---|---|
| `# Delta scope` section (heading to the line before `# Critique lens`) | 6df82fddd3d365da | yes |
| Three delta input bullets (`review_mode`, `changed_regions`, `open_findings`) | 989c27daaf2d4c2e | yes |
| Anchor-drift paragraph | afc49889024cd835 | yes |
| Deferred-findings block | 61a4e21f1207e464 | yes, and identical to the block at `f64bebe^` |

After removing the two added sentences (items 2 and 3), the delta-scope block and the input bullets equal the spec's text byte for byte. The anchor paragraph and the correctness ledger check equal the spec's text with no change.

Known gaps, both consistent with the spec and deferred to VHS-60 (not drift, not unmet criteria):

- The mode table has no row for an absent spec file. The spec's § Mode has no such row either (review gate finding 4).
- A full pass cannot dispatch when the commit snapshot fails, for example in a project with no commits. The spec's § Artifacts requires the complete three-file set before dispatch (review gate finding 3).

Other observations:

- `README.md:10` still shows the usage line without `--full`. `README.md` is not in the spec's Scope table (review gate finding 10, not acted on). Whether VHS-60 covers it was not checked.
- `docs/specs/TODO/VHS-27.review.md` lists findings 7, 8 and 9 as "not acted on", but the squash contains their fixes (blank line before the Anchor-drift paragraph, "steps 2 to 10", restored reference facts). The record understates what shipped.
- No-op step 4 replaces the mode token after the preflight line already printed delta, and nothing says to print the replacement (review gate finding 5). The spec's § No-op step 4 is equally silent, so this is not drift.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-cycle/SKILL.md` | yes | +259 lines changed. Mode table, no-op, two counters, round artifacts, ledger, changed regions, dispatch inputs, both stop screens. |
| `agents/spec-reviewer-correctness.md` | yes | Delta inputs, delta-scope block, ledger check, anchor paragraph replacing the Stale-anchors bullet and walk item 2. |
| `agents/spec-reviewer-edge-cases.md` | yes | Delta inputs, delta-scope block, anchor paragraph. |
| `agents/spec-reviewer-conventions.md` | yes | Same as edge-cases. |
| `agents/spec-reviewer-scalability.md` | yes | Same as edge-cases. |
| `docs/spec-workflow-reference.md` | yes | Delta mode, `--full`, `round` range, PET-166 numbers, pass-index readings. |
| `AGENTS.md` | yes | `/spec-cycle` and `/spec-brief` lifecycle items. |

Files the spec says to leave alone (`skills/ship-spec/`, `skills/spec-tickets/`, `skills/spec-close/`, `skills/spec-brief/`, `sync.py`, `lint.py`, `tests/`): `git diff --stat f64bebe^ f64bebe` over those paths is empty. The Deferred-findings block is unchanged (see Summary).

Dropped (named by the spec, not in the diff): none.

Unexpected files in diff (not in spec):

- None that count as drift.
- `docs/specs/TODO/VHS-27.review.md` — expected ship-spec review-gate record.
- `docs/specs/TODO/VHS-27.test-output.txt` — expected ship-spec test-gate record.

## Decisions

Rows S1-S4 are design clauses, not numbered decisions. They hold the four drift items.

| # | Decision | Status | Evidence |
|---|---|---|---|
| Tier | Tier is big; `round_cap` stays 4; the two-pass delta budget is the same on every tier | Confirmed | `skills/spec-cycle/SKILL.md:437` "A delta invocation has at most two passes on every tier"; tier step at `:343` untouched by the diff; marker records `tier: big` |
| 1 | Delta passes run on re-runs only; the first invocation's loop is unchanged | Confirmed | `skills/spec-cycle/SKILL.md:435` "When `start` is 1 this is the existing first-invocation loop"; `:375` row 11 is the only delta row |
| 2 | A copy of the spec and of the brief every round; green rewrites `spec.copy.md` to post-polish bytes | Confirmed | `skills/spec-cycle/SKILL.md:449` "Exact spec bytes the reviewers see. On green only, rewrite after 2g"; `:450` brief copy never rewritten; `:506` "Before dispatch, atomically save the three-file set" |
| 3 | The ledger is a saved file, P0 and P1 only; correctness alone checks it | Confirmed | `skills/spec-cycle/SKILL.md:790` "After every loop-red revision, including the final pass in either mode, atomically write `ledger.md`"; `:472` empty green ledger; `:468` "P2+ never enters it"; `agents/spec-reviewer-correctness.md:86` "file one P0 titled `ledger omits a P0/P1 line`" (no ledger check in the other three agents) |
| 4 | Anchor drift splits by cause: moved line is one combined P4, dead symbol is a P1 | Confirmed | `agents/spec-reviewer-correctness.md:111`, `agents/spec-reviewer-edge-cases.md:102`, `agents/spec-reviewer-conventions.md:107`, `agents/spec-reviewer-scalability.md:91` "File those moved citations once per report, as one combined P4"; grep finds no "Stale anchors" or "re-grep" left in the correctness agent |
| 5 | Code drift uses the saved commit; failure selects full before the pending write; both stop screens warn | Confirmed | `skills/spec-cycle/SKILL.md:479` "first run `timeout 30 git --no-pager rev-parse HEAD`"; `:379` "changes the token to `mode: full (code-drift unavailable)`"; `:490` drops the brief, spec and reviews paths; `:809` and `:1008` DRIFT paragraph. See S4 for the raw-path wording |
| 6 | `--full` requests a full pass, exclusive with `--attest` | Confirmed | `skills/spec-cycle/SKILL.md:15` usage line; `:76` "`--full` takes no value and is exclusive with `--attest`"; `:365` row 1; `:427` "`--full` and every full token skip this classification" |
| 7 | A changed brief forces a full pass | Confirmed | `skills/spec-cycle/SKILL.md:370` row 6 "`mode: full (brief changed)`"; `:359` filtered comparison keeps "final-newline presence" |
| 8 | Two counters; at most two delta passes on every tier; whole span free before any directory | Confirmed | `skills/spec-cycle/SKILL.md:433` "`C` is the cumulative positive review round"; `:437` "Never substitute `P < round_cap` for this two-pass bound"; `:377` "Reserve the span before creating any directory"; `:36` "round: <positive integer>" |
| 9 | A non-empty delta pass dispatches every lens the run would normally dispatch | Confirmed | `skills/spec-cycle/SKILL.md:548` "Every non-empty delta pass dispatches all lenses this invocation would normally dispatch" |
| 10 | The delta restriction covers new exploration only; contract text cites no skill line or repo path | Confirmed | `agents/spec-reviewer-correctness.md:94` "Those checks are not limited to `changed_regions`"; `:96` "A named heading covers its exclusive body only"; grep of the four agents finds no `SKILL.md`, `skills/` or file:line citation. See S2 for the added sentence |
| 11 | Nothing changed and nothing open is a no-op, classified before the pending write | Confirmed | `skills/spec-cycle/SKILL.md:412` "after Phase 1 and before pending"; `:419` "leaves the marker byte-for-byte untouched"; `:417` red marker with both sets empty goes full; `:423` NO-OP block |
| 12 | No saved copy means a full pass; the DONE archive is never a baseline | Confirmed | `skills/spec-cycle/SKILL.md:371` row 7 "`mode: full (no baseline)`"; `:357` "Never search another round or `docs/specs/DONE/`" |
| 13 | A pending marker means a full pass at the smallest free span | Confirmed | `skills/spec-cycle/SKILL.md:368` row 4; `:377` "smallest positive `start` for which the whole span ... is absent ... Its first pass has no closure predecessor"; `:1079` interrupted run "never overwrites the partial directory" |
| 14 | Mode table resolved from marker fields, not from the six-state reader | Confirmed | `skills/spec-cycle/SKILL.md:355` "The marker reader's six states are not the mode key"; `:365`-`:375` eleven rows with the spec's tokens; `:379` and `:417` the two overrides |
| 15 | Delta inputs: headings with exclusive-body hunks, stack pairing, open P0/P1 only, `Where` resolution | Confirmed | `skills/spec-cycle/SKILL.md:477` "Pair headings in document order by their full stack of heading lines"; `:492` "split `Where` on `;`"; `:601` "Open findings are extracted, not recalled"; `:530`-`:545` prompt shape. See S3 for the added bullet sentence |
| 16 | The rationale lives in the workflow reference; `AGENTS.md` names the mode and flag without the numbers | Confirmed | `docs/spec-workflow-reference.md:76` "58% of findings in rounds 2–5 and 54% in rounds 6–10"; `AGENTS.md:27` "at most two delta passes"; grep count of `PET-166`, `58%`, `54%` in `AGENTS.md` is 0 |
| S1 | § Dispatch: "The pending write is unchanged in contents" (pre-change skill: a failed pending write prints the line and continues) | Drifted | `skills/spec-cycle/SKILL.md:57` "A failed write does not change the run's outcome, with one exception"; `:496` "If the marker on disk is then `green`, stop before dispatch"; `docs/spec-workflow-reference.md:112` "If this write fails while the existing marker is green, the run stops before dispatch". Contents of the write are unchanged; the failure path is new. CodeRabbit round 1 |
| S2 | § Delta contract: behaviour section inserted "verbatim" in all four agents | Drifted | `agents/spec-reviewer-correctness.md:96` adds "A `deleted: true` entry has no body in the current spec: read that heading's body in `spec.copy.md` in the prior round's reviews directory". Same sentence in the other three. The spec does not cover how a reviewer reads a deleted section. CodeRabbit round 1 |
| S3 | § Delta contract: `changed_regions` input bullet text | Drifted | `agents/spec-reviewer-correctness.md:22` adds "The heading `(before first heading)` names the bytes before the first Markdown heading". Same sentence in the other three. The sentinel itself is in the spec (§ Changed regions) and in the skill (`skills/spec-cycle/SKILL.md:477`). CodeRabbit round 1 |
| S4 | § Changed regions: raw path has "no leading `"`, no `=>`, no tab, and no backslash" | Drifted | `skills/spec-cycle/SKILL.md:488` "with no leading `"`, `=>`, tab, or backslash". The condensed list can be read as line-start only. Review gate finding 6, not acted on |

## Acceptance Criteria

The nine bullets are the spec's "Done when" list. The brief's four ticket criteria and five added scenario criteria map onto them one to one.

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | The skill encodes the delta trigger, the delta pass contract and the ledger rule; the four agents accept `review_mode`, `changed_regions`, `open_findings` and verify closures when a manifest is provided | Met | `skills/spec-cycle/SKILL.md:355` (mode), `:410` (no-op), `:431` (two counters), `:459` (ledger); agent input bullets at `agents/spec-reviewer-correctness.md:21`-`:23` and the same three bullets in the other three; step 7 guard "If a `closure_manifest` was provided" at correctness `:47`, edge-cases `:47`, conventions `:52`, scalability `:47` |
| 2 | A delta pass with zero changed regions and zero open P0/P1 is a no-op that reports green and does not run a full pass | Unverifiable | Rule text present: `skills/spec-cycle/SKILL.md:419` "A green marker with both sets empty and a clean scan prints the following block and stops". No run has exercised it |
| 3 | A prior-round P0 or P1 omitted from the saved ledger is one blocking P0 from the correctness reviewer; a longer id does not cover a shorter one | Unverifiable | Rule text present: `agents/spec-reviewer-correctness.md:86` "The manifest covers it when a line matches the id as a token" (the token regex follows on that line) and "A match inside a quoted title, or inside a longer id, is not coverage". No synthetic ledger was run through the reviewer |
| 4 | `docs/spec-workflow-reference.md` states the rationale with the PET-166 numbers | Met | `docs/spec-workflow-reference.md:76` carries 58%, 54%, about 12%, 3 of 5, 26 closures, 2 findings both P2s, about 30 per round |
| 5 | The spec walks the first delta pass after a red halt and after a green | Met | Spec scenarios 1, 2 and 2b at `docs/specs/TODO/VHS-27.spec.md:408`, `:410`, `:412` |
| 6 | The spec walks a small-tier continuation | Met | Spec scenario 3 at `docs/specs/TODO/VHS-27.spec.md:414` |
| 7 | The spec walks delta pass 2 still red, then the grill option | Met | Spec scenario 4 at `docs/specs/TODO/VHS-27.spec.md:416` |
| 8 | The spec walks an attested green, a changed brief, an absent baseline, a pending marker and a run after spec-close | Met | Spec scenarios 5-9 at `docs/specs/TODO/VHS-27.spec.md:418`, `:420`, `:422`, `:424`, `:426` |
| 9 | The spec walks code changed since the saved commit with spec and brief unchanged, including a locator-only citation | Met | Spec scenario 10 at `docs/specs/TODO/VHS-27.spec.md:428`; locator strip shipped at `skills/spec-cycle/SKILL.md:490` |

## Test Plan

The spec ships no test module. Its oracle is the scenario list, checked by reading the edited skill. The checklist rows below were re-checked by grep and file read during this reconciliation; none was executed, because the suite does not run skills.

| Test | Exists? | Location |
|---|---|---|
| `python lint.py --strict` reports 0 errors | yes, ran | `docs/specs/TODO/VHS-27.test-output.txt`: "lint: 0 error(s), 0 warning(s)", exit 0 |
| `python -m unittest discover -s tests -p "test_*.py"` passes | yes, ran | `docs/specs/TODO/VHS-27.test-output.txt`: "Ran 127 tests ... OK (skipped=3)", exit 0. No test references delta mode |
| Review gate | yes, ran | `docs/specs/TODO/VHS-27.review.md`: /ponytail-review, 0 blocks, 4 fix-or-record (2 fixed, 2 recorded to VHS-60), 6 record-only |
| Checklist: invocation accepts `--full`, rejects it with `--attest`, both usage sites updated | by reading | `skills/spec-cycle/SKILL.md:15`, `:76`, `:1036` |
| Checklist: mode rows 1-11 print the spec's tokens; code-drift failure prints `mode: full (code-drift unavailable)` | by reading | `skills/spec-cycle/SKILL.md:365`-`:375`, `:379` |
| Checklist: no-op block, untouched marker, the dispatch and full-pass branches, the pass-2 `<lens>/STATUS` stop | by reading | `skills/spec-cycle/SKILL.md:412`-`:427`, `:439` |
| Checklist: round files before dispatch, green copy rewrite, ledger timing, temp-then-rename, LF on write and LF or CRLF on read | by reading | `skills/spec-cycle/SKILL.md:359`, `:449`-`:457` |
| Checklist: delta pass 2 folds without FROZEN/REWRITE; full invocation from round 1 still rewrites at `P == round_cap`; span free first | by reading | `skills/spec-cycle/SKILL.md:435`, `:437`, `:756`, `:377` |
| Checklist: four agents carry the bullets, delta-scope section, anchor paragraph and output parenthetical; correctness has the ledger check; no repo path or skill line cited | by reading, plus hashes | Summary hash table; output parenthetical at correctness `:190`, edge-cases `:186`, conventions `:180`, scalability `:127` |
| Checklist: four Deferred-findings blocks unchanged and identical | by hash | Summary hash table (61a4e21f1207e464 before and after) |
| Checklist: workflow reference carries the numbers, the delta statement and the pass-index readings; `AGENTS.md` names delta mode, `--full` and the delta halt, without the numbers | by reading | `docs/spec-workflow-reference.md:31`, `:47`, `:72`, `:74`, `:76`, `:98`, `:112`, `:160`, `:310`, `:311`; `AGENTS.md:25`, `:27` |
| Checklist: halt screen and Phase 3 screen both carry the DRIFT paragraph | by reading | `skills/spec-cycle/SKILL.md:809` (above "What would you like to do?" at `:811`), `:1008` (above "=== NEXT ===" at `:1010`) |
| Checklist: scenarios 10, 11, 14, 15, 16, 17, 18 outcomes | by reading only | Rule text at `skills/spec-cycle/SKILL.md:359`, `:417`, `:488`-`:492` and `agents/spec-reviewer-correctness.md:86`. No scenario was run |
| Checklist: tool-use notes list the code-drift commands; 2f-i uses `round-<C>` | by reading | `skills/spec-cycle/SKILL.md:1067`; `:713`, `:734`, `:867`; grep finds no `round-<round_cap>` left in the skill |

## Wiki-ready

- Decision 8: why wiki-worthy — two counters replace the single round number. Cumulative round `C` names directories and the marker's `round` (now any positive integer); pass index `P` drives revise, rewrite and halt. Every later spec-cycle change has to say which counter it means, and a delta re-run is capped at two passes on every tier.
- Decision 14: why wiki-worthy — the eleven-row mode table is the single place that decides full versus delta, keyed on the marker's `verdict`, `source` and `round` fields and not on the six-state reader. A fingerprint mismatch alone does not force a full pass.
- Decision 2 and Decision 3: why wiki-worthy — each round directory now holds `spec.copy.md`, `brief.copy.md`, `baseline.commit` and `ledger.md`. These are new on-disk artifacts that spec-close archives with the reviews tree, and a missing one silently selects a full pass.
- Decision 5: why wiki-worthy — code that merges after green is now a changed region through the saved commit, and both stop screens warn about it. This is the PET-166 tail (a merge after an all-green round restarted the churn) turned into a rule.
- Decision 11: why wiki-worthy — a re-run over a green spec with nothing changed and nothing open is a no-op that leaves the marker untouched. Operators can re-run `/spec-cycle` as a cheap check.
- Decision 4: why wiki-worthy — reviewer severity changed in both modes: a moved line number is one combined P4 per report, and only a dead symbol is a P1.
- Drift S1: why wiki-worthy — a failed pending-marker write over a green marker stops the run before dispatch. This is the one case where a failed marker write changes the run's outcome, and it is not in the spec.
- Comprehension: what changed and why — a re-run of `/spec-cycle` over a reviewed green or a red halt no longer restarts at round 1 with full lenses. It runs at most two delta passes scoped to changed heading bodies, sections citing changed code, and open P0/P1 findings, with all lenses still dispatched. PET-166 showed that full passes past convergence review the previous round's fixes: 58% and 54% of later findings targeted remediation text, and a delta close-out found 2 findings against about 30 per full round. The first invocation's loop is unchanged; `--full` or any mode-table row falls back to a full invocation.
- Comprehension: what changed and why — two gaps are open in VHS-60: the mode table has no row for an absent spec file, and a full pass cannot dispatch when the commit snapshot fails (a project with no commits). `README.md` still shows the usage line without `--full`.

RECONCILED: yes DRIFT: 4
