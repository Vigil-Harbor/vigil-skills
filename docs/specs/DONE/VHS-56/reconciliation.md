# Reconciliation Report: VHS-56

> Date: 2026-10-13
> Spec: docs/specs/TODO/VHS-56.spec.md
> Merge: PR #44 (8f3771b00fa63f2c03f9cd50b260a2aae815554f)
> Plane state: Done (group: completed)

## Summary

The shipped change puts the spec's twelve decisions into the four files the spec names: the skill, the workflow reference, the README and AGENTS. `skills/spec-brief/SKILL.md` gains a reviewer-eligibility step after the tier gate, a new `## Phase 3 — Doubt pass`, the renumbered Phases 4 (Confirm) and 5 (Write), a `## Doubt pass` brief section, and new never-does, tool-use and failure-mode text. All eight acceptance criteria (four from the spec, four from the brief) are met as shipped text. Lint and the unit suite pass at HEAD. There are five drifts, all intentional. Three come from the `/ship-spec` review gate and are stated in the PR body: run identity is now part of eligibility, `completed at cap` is recorded after a cycle-2 failure, and the prompt goes by stdin. Two come from the CodeRabbit fix commit 2a4ff96: a separate `small` gate branch for Confirm option 5, and Phase 5 mapping of resumed decisions. Nothing was dropped, and no file outside the spec's scope changed.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-brief/SKILL.md` | Yes | `ticket_contract` at `:90`; `--no-grill` routed to Doubt pass at `:126`; `### Doubt-pass reviewer` at `:162`–`:173`; `## Phase 3 — Doubt pass` at `:181`–`:311`; `## Phase 4 — Confirm` at `:313`; `## Phase 5 — Write` at `:351`; `## Doubt pass` emission at `:384`–`:403`; transcription exception at `:411`; never-does at `:445`; tool-use at `:451`; failure modes at `:468`–`:475`. Frontmatter (`:1`–`:11`) untouched: the first hunk starts at old line 87. |
| `docs/spec-workflow-reference.md` | Yes | `:11` and `:21` name the doubt pass among the steps `--no-grill` keeps; `:19` covers reviewer eligibility and the irreversible halt; `:23` (Phase 3), `:25` (Phase 4), `:27` (Phase 5); § Stakes tier rows at `:152`–`:154`. Other skills' phase headings (`:51`–`:104`, `:225`–`:282`) are unchanged. |
| `README.md` | Yes | `:9` summary clause; `:65` requirement line, with no vendor or tool named. |
| `AGENTS.md` | Yes | `:25` lifecycle line ("runs or explicitly skips a fresh-context cross-model doubt pass (at most two cycles)"); `:35` Stakes tier paragraph. |

Files the spec says stay unchanged, checked with `git diff --stat 8f3771b^ 8f3771b`: `skills/grilling/`, `skills/spec-cycle/`, `skills/ship-spec/`, `skills/spec-close/`, `skills/spec-tickets/`, `agents/`, `tests/`, `lint.py`, `sync.py`. None changed. No `VHS-41.*` path is in the diff. No new agent, script, test module or capability key was added. No spec file was dropped.

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-56.review.md` and `docs/specs/TODO/VHS-56.test-output.txt` are the `/ship-spec` review-gate record and test capture. They are lifecycle artifacts and are not counted as drift, as in the VHS-26 and VHS-60 reports.

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Review an in-memory rendered draft, not a pre-confirmation file | Drifted | Shipped as specified: `skills/spec-brief/SKILL.md:187`: 'Hold that text in context as the **candidate**. From then on the candidate is the source of truth'; `:183`: 'This phase writes no file — no brief, no temp, no report'; `:353`: 'the exact candidate the operator confirmed in Phase 4 … Never re-apply the mapping rules here'; `:411` transcription exception; `:214`–`:215` payload. Drift: Design 6 asked only that affected candidate sections and their consumers be updated after a resumed interview. `:345` ships 'Apply Phase 5's mapping rules to the returned new or changed items only: a fence … goes to `## Out of scope` … an emptied Decisions list takes the `_(none settled — see Risks / decisions)_` line. Renumber each list you changed'. CodeRabbit fix (commit 2a4ff96, squashed). It also closes review-gate record-only finding 4, which `VHS-56.review.md` still lists as not acted on. |
| 2 | At most two dispatch cycles, the second earned by a draft change | Drifted | `skills/spec-brief/SKILL.md:210`: 'Cycle 2 runs only when cycle 1's reconciliation changed the candidate … Cycle 2 is the cap … never dispatch a cycle 3'; `:306`: the retry 'is not a new cycle'. Drift: the spec's Result rule gives `completed at cap` only 'when the second reconciliation changed the draft'. `:286` ships '`completed at cap` when cycle 2's reconciliation changed the candidate, or when cycle 2 failed after cycle 1 changed it (Skip or Accept cycle 1)'. This makes § Outcome agree with Decision 12's failure path. Review-gate fix, in PR body. |
| 3 | Tier controls the pass after the existing wait gate | Drifted | `skills/spec-brief/SKILL.md:191`: 'this phase never asks again whether the host can wait'; `:194` small skip; `:195`–`:196` big; `:197` irreversible; `:173` initial irreversible halt before the interview; `:334` option 5 rule. Drift: the spec gives `small` one rule, skip plus a Confirm option 5. `:193` ships a separate branch, '`small`, entered from Confirm option 5 — run the pass'. Before this branch, the gate would have skipped the run that option 5 asks for. CodeRabbit fix (commit 2a4ff96, squashed). |
| 4 | One inert `## Doubt pass` section in every written brief | Confirmed | `skills/spec-brief/SKILL.md:369` (section order); `:384`: 'Every written brief carries exactly one `## Doubt pass` section, after `## Scale` (or straight after `## Tier` when Scale is absent) and before `## Risks / decisions`'; `:386`–`:401` both record shapes; `:403` four normalized reasons, 'names no vendor, model, or tool and quotes no reviewer prose … nothing downstream gates on it'; `:286`–`:293` distinct-root counts; `:248` cut count printed. |
| 5 | Eligibility requires declared different-family identity and read-only dispatch | Drifted | `skills/spec-brief/SKILL.md:166`–`:171`: candidates, self-stated family ('Never infer a family from a tool's name'), selection order, operator tie choice, content-free identity probe, console-only diagnostics; `:246` per-run identity check. Drift: `:168` adds an eligibility condition, 'a run identity (a provider or model line) it reports on every run, apart from its final response'. `:246` now names where the identity comes from: 'Read the run's identity from the mechanism's provider or model line, not from the final response'. Review-gate fix, in PR body. |
| 6 | Reuse the declared dispatch capabilities | Confirmed | Frontmatter `skills/spec-brief/SKILL.md:5`–`:10` is unchanged (no hunk before old line 87). `:451`: 'a native agent (`subagents`), or a command-line tool or an installed skill's shell bridge (`shell`)'. No new key; `lint.py --strict` is clean at HEAD. |
| 7 | Verify reviewer facts before folding them | Confirmed | `skills/spec-brief/SKILL.md:266`: 'Open the live source and check it; reviewer prose is a lookup hint, never evidence. True: fold it, citing `path:line` … Cannot be established: add a `## Risks / decisions` item ending "spec author pins this"'; `:261`: 'Verify its factual claims first and show the result in the batch. Never fold or move it on your own'; `:274` gives the order classify, verify, compose, edit, batch, update, re-read. |
| 8 | A settled-decision contradiction gets a separate operator prompt | Confirmed | `skills/spec-brief/SKILL.md:254`–`:261` four settled targets; `:276`: 'Before Confirm, show at most 7 settled-target findings per cycle'; `:278`–`:280` keep/replace/reopen; `:282`: comma groups, re-print with reason, unknown id and mixed `abort` invalid, sole-line `abort` stops, 'Never infer an answer'; `:345` resume conflicts use temporary `F-<n>` ids. |
| 9 | A `big` operator skip requires a reason | Confirmed | `skills/spec-brief/SKILL.md:199`–`:204` offer text verbatim; `:206`: 'A bare `2`, an empty reason, or any other reply re-prints the offer and keeps the interview, as many times as needed. Option 3 stops with nothing written.' |
| 10 | Reconcile in contract/action/trade-off/noise order | Confirmed | `skills/spec-brief/SKILL.md:252`: 'You own the classification; the reviewer's labels are advisory'; `:254` settled targets first; `:263`–`:268` the four classes in order; `:265` Origin/Out-of-scope narrowing; `:270` Tier advisory, Scale through Risks or Phase 5's four cases, no free-text replacement. |
| 11 | Read an ephemeral report leniently | Drifted | `skills/spec-brief/SKILL.md:223`–`:241` report shape; `:245`–`:248` reading order (host error first, one fence stripped, fails only when empty or with neither findings nor a clean statement, first 7 kept and the rest cut and counted); `:297` failure line with the timeout bound. Drift: the spec says 'Send the exact prompt by stdin or argv, never a file'. `:212` ships 'Send the prompt by stdin; use an argument only when the mechanism takes no stdin. Never a file.', also at `:451`. Review-gate fix, in PR body. |
| 12 | Failure posture follows tier; never a silent same-model substitute | Confirmed | `skills/spec-brief/SKILL.md:297`–`:311`: failure menu, one retry per cycle, Skip for small/big only, Accept cycle 1 for irreversible only under its precondition, Abort always, '`irreversible` never skips', 'Never substitute a same-family review'; `:321` Confirm disclosures; `:336`: 'A completed result, including at cap, stands under the new tier. A skipped result runs Phase 3's gate again'. |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `/spec-brief` runs the cross-model doubt pass or announces it skipped, and every written brief records the outcome in `## Doubt pass` (spec) | Met | `skills/spec-brief/SKILL.md:191`: 'Announce every skip as `Doubt pass: skipped — <reason>`'; `:384`: 'Every written brief carries exactly one `## Doubt pass` section'; `:386`–`:401` completed and skipped records |
| 2 | A settled-decision contradiction reaches the operator in a separate pre-Confirm prompt; never folded alone (spec) | Met | `skills/spec-brief/SKILL.md:254`, `:261`: 'Never fold or move it on your own'; `:276`: 'Before Confirm, show at most 7 settled-target findings per cycle'; `:445` never-does: 'lets a reviewer finding change a settled decision without the operator' |
| 3 | An `irreversible` brief is never written unless a cross-model cycle completed; the no-reviewer halt precedes the interview; a failed dispatch cannot skip (spec) | Met | `skills/spec-brief/SKILL.md:173`: 'halt here, before the interview. Nothing is written.'; `:197`: '`irreversible` — run the pass; there is no skip'; `:311`: 'once a retry is spent without the Accept precondition, only Abort remains'; `:336` Confirm upgrade to irreversible runs the pass and 'a failure there cannot skip' |
| 4 | `python lint.py --strict` and the unittest suite pass (spec) | Met | `docs/specs/TODO/VHS-56.test-output.txt`; re-run at HEAD: `lint: 0 error(s), 0 warning(s)`, `Ran 127 tests` `OK (skipped=3)` |
| 5 | spec-brief runs the doubt pass or announces that it skipped it, and a skip is recorded in the brief (brief) | Met | `skills/spec-brief/SKILL.md:191`, `:394`–`:403`: '**Result:** skipped' / '**Reason:** <normalized reason>' |
| 6 | A finding that contradicts a settled decision reaches the operator before Confirm; the skill does not fold it alone (brief) | Met | Same anchors as row 2: `skills/spec-brief/SKILL.md:261`, `:276` |
| 7 | An `irreversible` brief is never written without the pass (brief) | Met | Same anchors as row 3: `skills/spec-brief/SKILL.md:173`, `:197`, `:311`, `:336` |
| 8 | Lint and tests pass (brief) | Met | As row 4 |

These criteria are checked as shipped text only. Whether an agent follows the instructions in a real run is behavioral and was not tested. The PR's test plan leaves "First real run" unchecked: the pass has not yet run end to end against a live second-model reviewer.

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| `python lint.py --strict` | Yes | `docs/specs/TODO/VHS-56.test-output.txt`: 0 errors, 0 warnings. Re-run at HEAD for this report, same result. |
| `python -m unittest discover -s tests -p "test_*.py"` | Yes | `docs/specs/TODO/VHS-56.test-output.txt`: 127 tests OK, 3 skipped. Re-run at HEAD for this report, same result. |
| 1. Phase order Grounding → seed gate → tier gate → Interview → Doubt pass → Confirm → Write, including `--no-grill` | Yes (text) | `skills/spec-brief/SKILL.md:71`, `:84`, `:92`, `:175`, `:181`, `:313`, `:351`; `:126` routes `--no-grill` to Phase 3 |
| 2. `small` skips without a new wait; option 5 only when eligible, runs and returns, then hides | Yes (text) | `skills/spec-brief/SKILL.md:193`–`:194`, `:334` |
| 3. `big` run/skip/abort, non-empty reason, re-print indefinitely; no-reviewer and failed-dispatch skips recorded | Yes (text) | `skills/spec-brief/SKILL.md:195`–`:206`, `:307`, `:403` |
| 4. Irreversible: early halt, Confirm-upgrade re-prompt, cycle-1 retry then Abort, cycle-2 Accept cycle 1 | Yes (text) | `skills/spec-brief/SKILL.md:173`, `:336`, `:306`–`:311`; the no-wait halt is unchanged at `:96` |
| 5. Cycle 2 only after a cycle-1 change; no cycle 3; all-rejected stops | Yes (text) | `skills/spec-brief/SKILL.md:210` |
| 6. Live verification, composition, consumer re-read, unverifiable to Risks | Yes (text) | `skills/spec-brief/SKILL.md:266`, `:274` |
| 7. Settled-target precedence and contradiction reply grammar | Yes (text) | `skills/spec-brief/SKILL.md:254`–`:261`, `:276`–`:282` |
| 8. Tier change, revise and `--no-grill` add follow the invalidation rules | Yes (text) | `skills/spec-brief/SKILL.md:336`, `:345`, `:347`, `:349` |
| 9. Exactly one `## Doubt pass`; normalized skip reasons; no raw prose or vendor | Yes (text) | `skills/spec-brief/SKILL.md:353`, `:384`, `:403` |
| 10. No filesystem write before final confirmation | Yes (text) | `skills/spec-brief/SKILL.md:183`, `:445` |
| 11. `skills/grilling/SKILL.md` unchanged; no proof ladder, sandboxed run, same-model fallback or vendor tool | Yes | `git diff --stat 8f3771b^ 8f3771b -- skills/grilling` is empty; no added line in the diff matches codex, openai, gpt, gemini, anthropic, claude, opus, sonnet or grok |
| 12. README, AGENTS and workflow reference agree on phase order, tier behavior, two-cycle cap | Yes (text) | `docs/spec-workflow-reference.md:21`–`:27`, `:152`–`:154`; `AGENTS.md:25`, `:35`; `README.md:9`, `:65`. README states no cycle cap; the spec asked it for one compact clause only. |
| 13. Lint accepts the unchanged `requires` block; full suite passes | Yes | Frontmatter untouched; lint and suite pass at HEAD |
| 14. Fold and replacement survival; Q-linked and Q-less resolutions on resume; written-candidate counts | Yes (text) | `skills/spec-brief/SKILL.md:411`, `:338`–`:345`, `:347`, `:441` |
| 15. Eligibility from self-stated family, probe, default preference, tie choice, per-dispatch identity, diagnostics; prompt carries wiki, seed, cap and narrowed contract | Yes (text) | `skills/spec-brief/SKILL.md:166`–`:171`, `:246`, `:90`, `:214`–`:219` |
| 16. Lenient reading, fence strip, fixed 7-block cap under `--questions 1`, stdin and no files, timeouts, retry and failure paths | Yes (text) | `skills/spec-brief/SKILL.md:212`, `:217`, `:221`, `:245`–`:248`, `:297`–`:311`. Stdin-first rather than stdin-or-argv (Decision 11 drift). |
| 17. Distinct-root counts, reopen counted as resolved plus one open, `Result` not `Status`, spec-brief-only renumbering, tables match | Yes (text) | `skills/spec-brief/SKILL.md:286`–`:293`, `:389`; `docs/spec-workflow-reference.md:152`–`:154`; other skills' phase headings unchanged |
| 18. Tier findings advisory; Scale through Risks or the four cases; no Tier/Scale replacement in the batch | Yes (text) | `skills/spec-brief/SKILL.md:270`, `:315` |

The spec calls this a prose-only change, so items 1 to 18 are review checks. They were re-checked against the text at HEAD for this report. No automated test was added, and the spec asked for none.

Notes:
- The committed `test-output.txt` came with feature commit 15e5363 at 23:02. It predates CodeRabbit fix 2a4ff96 at 23:22, which changed only `skills/spec-brief/SKILL.md`. The suite re-run at the merge commit for this report matches the committed numbers.
- The frontmatter `description` (`skills/spec-brief/SKILL.md:3`) does not mention the doubt pass. The spec's Scope row for the skill does not ask for that, and the review gate recorded it as record-only (finding 6). This is a note, not drift.
- The eligibility summaries in `docs/spec-workflow-reference.md:19` and `README.md:65` do not include the run-identity condition that review-gate fix (a) added to `skills/spec-brief/SKILL.md:168`. These are summary-level mirrors, so this is not counted as drift.
- Review-gate finding 4 ("Revised decisions have no stated mapping") is recorded in `VHS-56.review.md` as not acted on, but CodeRabbit fix 2a4ff96 resolved it (Decision 1 drift). Review-gate finding 5 (a redundant sentence on when the pass ends, `:210`) stays as shipped.
- The two CodeRabbit drifts are stated in the 2a4ff96 commit message. The squash commit body (title only) and the PR description do not mention them.

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:
- Decision 5 (as shipped, with the run-identity fix): a cross-model reviewer qualifies by its own stated family or provider, never by an inference from its tool name, plus read-only mode, fresh context, and a run identity reported apart from the final response that is checked on every dispatch. No vendor table. Reusable for any later cross-model step, such as a `/spec-cycle` cross-model lens.
- Decision 8 and Decision 10: reviewer output is untrusted. Facts and anchors are verified live and folded, and anything touching a settled decision, operator fence, explicit ticket decision or transcribed acceptance statement goes to an operator keep/replace/reopen batch. This is the operator-owns-decisions rule (`skills/grilling/SKILL.md:61`) applied to model review.
- Decision 3 and Decision 12: the stakes tier sets how strict the doubt pass is. `small` opts in, `big` offers it and a skip needs a reason, `irreversible` cannot skip and halts before the interview with no reviewer. This extends the VHS-55 tier ladder to `/spec-brief`, and the irreversible no-skip pattern matches `/ship-spec`'s review gate.
- Decision 1 and Decision 4: the brief is held in context as one candidate, and Confirm shows exactly the bytes that will be written. `## Doubt pass` is audit metadata that nothing downstream gates on, and it uses `**Result:**` to avoid a clash with the header's `**Status:**`.
- Decision 2: two cycles, the second only when the first changed the draft. `completed at cap` discloses an unre-reviewed final edit, including after a cycle-2 failure.
- Comprehension: before VHS-56, nothing challenged the brief. The operator ran a Codex review by hand in 13 sessions, and those reviews often came back NOT READY. `/spec-brief` now runs that review itself as Phase 3, between the interview and Confirm, and every brief records whether it ran. Confirm and Write are now Phases 4 and 5. The pass has not yet been exercised against a live second-model reviewer.

RECONCILED: yes DRIFT: 5
