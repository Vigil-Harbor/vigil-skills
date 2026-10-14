# Reconciliation Report: VHS-26

> Date: 2026-10-13
> Spec: docs/specs/TODO/VHS-26.spec.md
> Merge: PR #43 (33b9215cb70d8b759c7f13695e59b1a83778fc2e)
> Plane state: Done (group: completed)

## Summary

The shipped change puts the spec's nine decisions into the six files the spec names, as prose in the skill, two reviewer agents and three documents; all six acceptance criteria are met and the lint and unit suite pass at HEAD. Two drifts, both intentional: the build applied the fix the spec had listed under `## Deferred (P2+)` (grading rule 4), and a review-fix commit replaced one clause of the §2e disposition rule with an explicit closure rule for every lens.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-cycle/SKILL.md` | Yes | Phase 1 block at `:392`–`:396`, round-artifact block at `:464`–`:483`, correctness-only input at `:569`–`:570`, §2e at `:740`, `:751`, `:757`, `:759`. One sentence at `:759` is not the spec's wording (Decision 6). |
| `agents/spec-reviewer-correctness.md` | Yes | Input bullet at `:24`; `**Ground-truth check.**` block at `:89`–`:104`. Grading rule 4 at `:97` differs from the spec (Decision 8). |
| `agents/spec-reviewer-conventions.md` | Yes | `## Precedent is not evidence` at `:109`–`:111`, under the critique lens (`:103`), after `# Delta scope` (`:93`). |
| `docs/spec-workflow-reference.md` | Yes | `:70`, `:83`, `:85`, `:96`. |
| `README.md` | Yes | One sentence added at `:10`. |
| `AGENTS.md` | Yes | `:27` and `:43` as specified. The conventions row at `:45` also gained "stale prior-spec mechanisms"; the spec names only `:27` and `:43`, but the row is in the same reviewer summary table. Not counted as drift. |

Files the spec says stay unchanged, checked with `git diff --stat 33b9215^ 33b9215`: `agents/spec-reviewer-edge-cases.md`, `agents/spec-reviewer-scalability.md`, `tests/`, `sync.py`, `skills/ship-spec`, `skills/spec-close`, `skills/spec-brief` — no change. No spec file was dropped.

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-26.review.md` and `docs/specs/TODO/VHS-26.test-output.txt` — the `/ship-spec` review-gate record and test capture. Lifecycle artifacts, not counted as drift (same treatment as VHS-60).

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Tier is `big` | Confirmed | `docs/specs/TODO/VHS-26.reviews/verdict.md:9` — 'tier: big'; verdict green at round 6; the review gate ran (`docs/specs/TODO/VHS-26.review.md`) |
| 2 | Scale is explicitly a non-factor | Confirmed | No scalability reviewer change and no scale machinery in the diff; `round-6/` holds three lens reports (correctness, edge-cases, conventions) and no scalability report |
| 3 | The obligation covers factual runtime claims, not proposed requirements | Confirmed | `skills/spec-cycle/SKILL.md:392` — 'carries a `file:line` anchor that you opened and read while preparing this dispatch'; `:394` — '`Anchor: none` is never legal for behavior implemented in a readable file, inside or outside the project root' and 'A proposed requirement about what the implementation must do is not a claim that the current runtime already does it'; `:396` — 'A Runbook step that invokes code is a runtime-behavior claim.' |
| 4 | One human-readable `ground-truth-ledger.md` per dispatched round | Confirmed | `skills/spec-cycle/SKILL.md:466` — 'The ground-truth ledger is human-readable, not a parser contract'; `:477` four facts; `:479` — 'puts `New spec: rows cover every section.` directly under the title. No other dispatch writes that line.'; `:483` no-claims line, rebuild rule and the accepted interruption gap. No added line uses the bare word "ledger" for this file (checked over every `+` line of the diff). |
| 5 | The ledger is review evidence, not a new control-plane gate | Confirmed | `skills/spec-cycle/SKILL.md:464` — 'It is not a baseline member: its absence does not make the baseline incomplete or change the mode table.' and 'print exactly `ground-truth-ledger.md NOT written: <error> — dispatching; correctness will report the missing evidence`'; `:483` — 'Write no ground-truth ledger or addendum for an edit with no later reviewer dispatch'. `grep -c "ledger NOT written:"` over the skill is 1 before and 1 after. |
| 6 | Revision is a verify–compose–edit–re-read operation | Drifted | Steps 1–5 ship as specified: `skills/spec-cycle/SKILL.md:740` (verify reviewer facts, three editing paths named), `:751` — 'state one intended result and compose the findings against it before editing', `:757` (re-read every propagation site and consumer; hold rows). Step 6 at `:759` differs in one place: the spec's clause 'a reviewer closes the finding by checking that the file exists with content' ships as 'Closure of this finding is by file existence, for every lens: a predecessor `ground-truth ledger missing` finding is CLOSED when the current round's `ground-truth-ledger.md` exists with content, whether rows or the no-claims line; no spec edit is required or expected. When the current round's file is also missing, the finding is REOPENED.' Added by review-fix commit 593a141; it restates Decision 8's closure rule for every lens. The disposition phrase and dispatch are unchanged. Intentional, stated in PR body (the statement is the 593a141 message carried in the squash commit body; the PR description's "Notes for review" does not mention it). |
| 7 | Precedent points to code; it never proves behavior | Confirmed | `skills/spec-cycle/SKILL.md:392` — 'precedent can establish naming or intent, but it does not prove runtime behavior'; `:740` — 'A prior-spec mechanism receives the same live-code verification before it is cited or inherited.'; `agents/spec-reviewer-conventions.md:110` — 'it is only a pointer to evidence'; `:111` — 'report the stale precedent at the severity dictated by the definitions below' |
| 8 | Correctness alone enforces the ledger | Drifted | Shipped as specified except grading rule 4. `ground_truth_ledger_path` appears only at `skills/spec-cycle/SKILL.md:570` and `agents/spec-reviewer-correctness.md:24`, `:89`; the block is unnumbered, top-level, after `**Ledger check.**` (`:87`) and before the cannot-complete sentence (`:106`) and `# Delta scope` (`:108`); steps are still 1–7 (`:28`–`:48`). Drift: the spec's rule 4 sends a moved line to the combined P4 and stops (first match). `agents/spec-reviewer-correctness.md:97` ships 'When only the line moved, include it in Anchor drift's combined P4, then continue to rule 5 against the live code at the symbol's current line.' This is the fix the spec records under `## Deferred (P2+)` (edge-cases/R6/F-1), applied in the build. Intentional, stated in PR body. Two wording compressions, not counted: rule 3 drops the sentence 'A row defect or a missing anchor is advisory; only an anchor that contradicts the claim blocks' (the same point is at `:104`), and the omission rule says 'one untagged P2' (`:101`) where the spec says 'Do not tag it `Pre-ship recommended`'. |
| 9 | Documentation mirrors the contract briefly | Confirmed | `docs/spec-workflow-reference.md:83` — 'It is separate from baseline completeness and from disposition `ledger.md`; a failed write warns and dispatches'; `:85` — 'It alone receives the ground-truth ledger path and deterministically samples at most five rows'; `AGENTS.md:27` carries all four summary points. `README.md:10` carries three of the four (it omits "revisions verify facts and compose overlapping edits"); the spec's Scope row asks the README for one short ledger sentence, so this is recorded as a note. No summary states behavior absent from the skill or agents. |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Phase 1 and every reviewed revision require fresh live-code anchors; every dispatched round writes a claim → section → anchor → round-read ground-truth ledger or the no-claims line (brief 1) | Met | `skills/spec-cycle/SKILL.md:392` (Phase 1), `:740` and `:757` (revisions), `:464` and `:477` (the file and its four facts), `:483` — 'write `No runtime-behavior claims were authored or revised for round <C>.` instead of rows' |
| 2 | §2e re-verifies reviewer-supplied facts, composes overlapping findings before editing, re-reads every propagation site and consumer after editing (brief 2) | Met | `skills/spec-cycle/SKILL.md:740` — 'open the live source and verify it; a report's anchor is a lookup hint, not evidence'; `:751` — 'never paste suggested wordings serially into the same text'; `:757` — 're-read every propagation site and every section that consumes the edited decision, not only the section named in the finding' |
| 3 | Phase 1, §2e and the conventions reviewer state that a prior spec is a pointer, not evidence (brief 3) | Met | `skills/spec-cycle/SKILL.md:392`, `:740`; `agents/spec-reviewer-conventions.md:109`–`:111` |
| 4 | Runbook steps that invoke code require an anchored trace through the live call chain that admits or rejects the operation (brief 4) | Met | `skills/spec-cycle/SKILL.md:396` — 'Trace its entry point through the exact live call chain to the code that admits or rejects the operation, read that code, and anchor the step there.'; `:740` for a Runbook edit in a revision |
| 5 | Only the correctness reviewer receives the ground-truth-ledger path; it applies Decision 8's deterministic sample and blocking findings and keeps its existing duties (brief 5) | Met | `skills/spec-cycle/SKILL.md:569`–`:570` — 'For the correctness reviewer additionally:'; `agents/spec-reviewer-correctness.md:92` — 'check the first two, the middle row (the lower middle for an even count), and the last two'; `:91` P0, `:98` P1; `:104` — 'The ordinary step 5 verification remains in force.' Rule 4 differs from the spec's text in the direction of its own deferred fix (Decision 8). |
| 6 | The four `# Delta scope` blocks are byte-identical; lint clean; unit suite passes (brief 6) | Met | The four blocks hash identically at HEAD (sha256 `5e76ba015b8dd56b…`, 10 lines each, the same hash VHS-60 recorded). Re-run at 33b9215 for this report: `lint: 0 error(s), 0 warning(s)`; `Ran 127 tests` — `OK (skipped=3)`. |

Whether authors and reviewers follow these instructions in a real run is behavioral and was not exercised here; every criterion above is verified as shipped text only.

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| `python lint.py --strict` | Yes | `docs/specs/TODO/VHS-26.test-output.txt` — 0 errors, 0 warnings; re-run at HEAD for this report, same result |
| `python -m unittest discover -s tests -p "test_*.py"` | Yes | `docs/specs/TODO/VHS-26.test-output.txt` — 127 tests OK, 3 skipped; re-run at HEAD for this report, same result |
| Structural checklist items (failure-message string and `ledger NOT written:` count; correctness-only path; steps 1–7 and block placement; four-way `# Delta scope` compare; out-of-scope surfaces unchanged) | Yes | Re-checked at HEAD for this report; results in the Decisions and Scope tables. The manifest-vocabulary and recount paragraphs are outside every hunk of the diff (hunks at old lines 391, 457, 541, 708, 718, 723). |
| Mental exercises of the correctness instructions, the omission boundary and closure | Partly | No artifact records a walk of the listed cases. The record that exists is the round-6 reviews (`docs/specs/TODO/VHS-26.reviews/round-6/`, correctness and edge-cases `STATUS: GREEN`) and the `/ponytail-review` gate (`docs/specs/TODO/VHS-26.review.md`, 0 blocks, 2 recorded). The spec adds no automated test and none was added. |

Notes:
- The committed `test-output.txt` predates review-fix commit 593a141 (the capture was committed with db242cb at 18:33; 593a141 at 18:53 changed only `skills/spec-cycle/SKILL.md`). The suite was re-run and passed after it, but the artifact was not refreshed. The re-run at the merge commit for this report matches the committed numbers.
- The two findings the review gate recorded and did not fix remain open and are not ticketed: only the correctness agent's own prompt carries the file-existence closure rule (the other lenses rely on the manifest line and `skills/spec-cycle/SKILL.md:759`), and a `ground-truth ledger missing` finding has no `Where` rule, so the next delta pass reviews every heading.
- Deferred row D-1 (post-green polish bypasses author grounding) is not implemented, as the spec requires; it is VHS-63.

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:
- Decision 4 and Decision 5: the ground-truth ledger is a fourth per-dispatch file that is deliberately not a baseline member, has no grammar, and has no link to changed-regions; a failed write warns and dispatches. Constraining for VHS-61 (mechanical checks) and for any later change to the mode table or round artifacts. Attempt 1 went red on exactly the machinery these two decisions fence out.
- Decision 8: one lens enforces, with a fixed five-row sample, two blocking findings (missing file P0, unsupported claim P1) and an advisory omission; the stated limits (no edited-section inventory, a no-claims line where rows were owed) are what VHS-61 inherits. Record the shipped rule 4, not the spec's: a moved line joins the combined P4 and grading continues to the blocking rule.
- Decision 6: revision is verify, compose, edit, re-read; the missing-file finding closes by file existence for every lens and carries a path in place of a `§` anchor. Reusable for any later process finding that has no spec site.
- Decision 3 and Decision 7: what counts as a runtime-behavior claim, the out-of-root and `Anchor: none` rules, and "a prior spec is a pointer, not evidence". Reusable outside `/spec-cycle`.
- Comprehension: `/spec-cycle` authors now read the live code behind every runtime-behavior claim at authoring and at each reviewed revision, and each dispatched round saves that evidence where the correctness reviewer samples it; before this, only reviewers read code, so a revision could add P1s as fast as it removed them (the GAV-13 post-mortem). Enforcement is by review only until VHS-61; post-green polish is still ungrounded (VHS-63).

RECONCILED: yes DRIFT: 2
