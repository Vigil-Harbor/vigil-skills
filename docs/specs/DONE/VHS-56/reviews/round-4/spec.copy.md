# VHS-56 — cross-model doubt pass before brief confirmation

**Tier:** big

## Goal

Add one bounded, fresh-context, cross-model doubt pass to `/spec-brief` after the optional interview has produced a complete draft and before the operator confirms that draft. The pass challenges false premises and stale anchors without letting model output silently overturn operator-set decisions, records every skip, and preserves the existing rule that `/spec-brief` writes only its final brief through its transient atomic-write sibling (`skills/spec-brief/SKILL.md:218`, `skills/spec-brief/SKILL.md:256`).

## Current behavior (grounded)

- `/spec-brief` currently returns from the optional `grilling` interview and enters Confirm immediately; there is no intervening review step (`skills/spec-brief/SKILL.md:160`, `skills/spec-brief/SKILL.md:162`, `skills/spec-brief/SKILL.md:166`).
- Confirm currently previews decisions, risks, tier, and the tier basis, then offers write, revise, abort, or change-tier choices (`skills/spec-brief/SKILL.md:168`, `skills/spec-brief/SKILL.md:170`, `skills/spec-brief/SKILL.md:180`).
- The write template currently emits Tier and optional Scale before Risks / decisions and References, with no doubt-pass record (`skills/spec-brief/SKILL.md:186`, `skills/spec-brief/SKILL.md:188`, `skills/spec-brief/SKILL.md:202`, `skills/spec-brief/SKILL.md:205`).
- The skill's frontmatter already declares `subagents: true`, while the portability lint accepts only `shell`, `filesystem`, `network`, `subagents`, and `services` as top-level `requires` keys (`skills/spec-brief/SKILL.md:5`, `skills/spec-brief/SKILL.md:9`, `lint.py:44`, `lint.py:45`).
- The skill currently limits its filesystem mutations to the final brief, its dot-prefixed temporary sibling, creation of `docs/specs/TODO/`, and removal of a stale temporary sibling (`skills/spec-brief/SKILL.md:218`, `skills/spec-brief/SKILL.md:254`, `skills/spec-brief/SKILL.md:256`).
- `/spec-cycle`'s drift checklist parses Decisions, Done when, and Out of scope by heading rather than by a fixed total section count, so an additional top-level brief section does not change those three keys (`skills/spec-cycle/SKILL.md:1065`, `skills/spec-cycle/SKILL.md:1067`, `skills/spec-cycle/SKILL.md:1070`).

## Scope

| Path | Change |
|---|---|
| `skills/spec-brief/SKILL.md` | Add Phase 3 — Doubt pass; renumber Confirm and Write; define the held candidate, reviewer eligibility, payload, output, reconciliation, bounds, tier behavior, preview and brief record, failure modes, and tool-use constraints. Renumber only spec-brief's own phase references. |
| `docs/spec-workflow-reference.md` | Mirror the doubt-pass contract, tier behavior, two-cycle bound, reconciliation, outcome record, and new spec-brief phase numbers; update § Stakes tier. |
| `README.md` | Amend the `/spec-brief` summary and requirement line so cross-model review is visible without naming a vendor or tool. |
| `AGENTS.md` | Amend the lifecycle summary and the Stakes tier paragraph so the brief is challenged after grilling and before confirmation, with the tier rule stated compactly. |

No new agent definition, script, test module, capability key, or persistent review artifact is created.

## Decisions

Decisions 1–3, 5, 7–10 and the Design pin the brief's Risks / decisions 1–10. These additional positions are **spec-level additions**:

- Full-candidate Confirm preview (Design 6): the operator must see the text that will be written, including corrections outside Decisions and Risks.
- Completed-pass record and cumulative counts (Decision 4): disclose what was reviewed and whether the last edit was re-reviewed, alongside mandatory skip records.
- Explicit Abort in the big offer and failure menus (Decisions 9 and 12): give the operator a clear exit before writing.
- Read-only eligibility and deterministic selection, bounded report grammar and one retry per cycle (Decisions 5, 11 and 12): protect the mutation boundary and recover from a transient failure without increasing the cycle cap.
- Furthest-completed-state handling after cycle-2 failure (Decision 12): disclose partial review with the existing at-cap result rather than a new status and flag.
- Initial irreversible eligibility halt and preserving the interview on an unavailable Confirm upgrade (Design 1 and 6): avoid spending or losing interview work on an impossible tier.
- Candidate retention, transcription exceptions and amended resume summary (Decision 1 and Design 2/6): prevent a verified fold or operator resolution from reverting during rendering, revise or write.

### Decision 1 — Review an in-memory rendered draft, not a pre-confirmation file

Phase 3 initially renders and holds the complete candidate, excluding `## Doubt pass` until its outcome is known. That held text is the source of truth after the initial mapping. Reconciliation edits it in place; subsequent rendering means displaying and checking the held text, never re-deriving it from an unchanged interview summary or ticket. The reviewer receives the candidate verbatim, the resolved ticket contract including any seed-gate paragraph, and the read-only grounding context in Design 4. It receives no interview transcript, author reasoning, conversation history, or claim that the draft is correct.

The candidate stays in context; Phase 3 creates neither the final brief nor a second temporary file. Confirm displays the held candidate with its outcome block inserted, and Phase 5 writes exactly those confirmed bytes without re-running mapping rules. Design 2 defines where folds may land and the transcription exception; Design 6 carries operator resolutions through revise.

### Decision 2 — At most two dispatch cycles, with the second earned by a draft change

One eligible dispatch is cycle 1. After reconciliation, cycle 2 runs only when cycle 1 changed the candidate draft: a verified fact/anchor finding was folded, an operator changed a settled decision, or an unverifiable premise was moved into `## Risks / decisions`. A cycle whose findings are all rejected as contract misreads or noise ends after cycle 1; repeating an unchanged artifact would be doubt theater.

Cycle 2 receives the updated held candidate and is another fresh-context dispatch. It is the cap: reconcile its findings but never dispatch cycle 3, even if reconciliation changes the draft again. The outcome record says `completed at cap` when the second reconciliation changed the draft, so Confirm does not imply that the final edit was re-reviewed. A retry belongs to its failed cycle and does not earn another cycle.

### Decision 3 — Tier controls the pass after the existing wait gate

The tier gate already stops a host that cannot wait, before the interview (`skills/spec-brief/SKILL.md:92`, `skills/spec-brief/SKILL.md:94`). Phase 3 therefore repeats no wait-capability test and holds no `can_wait` variable.

- `small`: announce and record `skipped — tier small; operator did not request the pass` without waiting, including when no reviewer is eligible. Only when an eligible reviewer exists, add Confirm option `5. Run the doubt pass`; choosing it runs Phase 3 and returns to Confirm.
- `big`: offer Decision 9's run/skip/abort menu when eligible; otherwise announce and record `skipped — no eligible cross-model reviewer`.
- `irreversible`: no skip. With no eligible reviewer at the initial tier gate, halt immediately after that gate, before the interview, and write nothing. A Confirm upgrade on such a host re-shows the tier prompt and preserves the interview (Design 6).

The doubt pass still runs after `--no-grill`; that flag skips only the interview.

### Decision 4 — Add one inert `## Doubt pass` section to every written brief

Phase 5 emits `## Doubt pass` after the optional `## Scale` section (or immediately after `## Tier` when Scale is absent) and before `## Risks / decisions`.

A completed pass records:

```markdown
## Doubt pass

**Result:** completed | completed at cap
**Cycles:** 1 | 2
**Outcome:** folded <n> fact/anchor findings; operator resolved <n> decision findings; rejected <n>; open <n>
```

A skipped pass records:

```markdown
## Doubt pass

**Result:** skipped
**Reason:** <normalized reason>
```

Normalized reasons are `tier small; operator did not request the pass`, `operator declined — <reason>`, `no eligible cross-model reviewer`, or `reviewer dispatch failed — <short reason>`. The section contains no vendor, model slug, tool name, or raw reviewer prose. Define it as audit metadata with no downstream gate.

Counts aggregate across all reconciled cycles by distinct root (same target and concern); a repeated cycle-2 finding is counted once, not again as a rejected duplicate. Folded means verified autonomous fact/anchor edits; operator resolved includes keep, replace and reopen; rejected means disproved, contract misread or noise; open is the number of resulting unresolved Risks / decisions items added by the pass. Reopen counts as one operator resolution and its resulting Risks item as open. A repeated root's final disposition replaces its earlier disposition. `completed in N cycle(s)` in Confirm maps to `Result: completed` and `Cycles: N`; at-cap uses its literal result and the number of successfully reconciled cycles.

### Decision 5 — Eligibility requires declared different-family identity and read-only dispatch

Any fresh-context dispatch mechanism available in this session counts: a native subagent, an installed skill, or a command-line reviewer reached through the shell. Check the authoring model's self-reported family against an explicit family field in the mechanism's declared configuration or runtime metadata/output; compare the trimmed, case-insensitive declared family values. Check that the declared model is selectable now, fresh context is supported, and the narrowest read-only agent class or sandbox mode is available and selected. An installed skill must identify its underlying dispatch and these same properties. Tool presence, a model display name or a vendor inference is insufficient evidence. Unknown family or mode, same family, or an exclusively write-capable mechanism means ineligible; never dispatch a general-purpose write-capable reviewer.

Use the strongest eligible model by the mechanism's declared ranking; absent a ranking treat candidates as tied, and break ties by lexically first declared mechanism/model identifier. Hold the eligibility evidence and selected mechanism in context so the same session configuration yields the same answer. Each cycle and retry is fresh-context with no inherited authoring history, using the selected read-only mode and explicit no-mutation instructions. The same model may serve both cycles. The skill names no vendor or tool and maintains no identity lookup table.

### Decision 6 — Reuse the declared dispatch capabilities

Keep the frontmatter capabilities unchanged. Native dispatch relies on the already-declared `subagents: true`; command-line dispatch, including a skill's shell bridge, relies on the already-declared `shell: true` (`skills/spec-brief/SKILL.md:6`, `skills/spec-brief/SKILL.md:9`). Grounding uses the existing filesystem/network envelope (`skills/spec-brief/SKILL.md:7`, `skills/spec-brief/SKILL.md:8`), and lint's top-level vocabulary is five keys (`lint.py:45`). Add no `models`, `cross-model`, or vendor-specific key.

### Decision 7 — Verify reviewer facts before folding them

Reviewer output is untrusted. Before a fact, count, path, anchor, current-behavior statement, or claimed omission changes the candidate, the author opens the live source and checks it. A live file gets a `path:line` citation in the candidate. Outside Decision 8's settled targets, an unavailable source or unestablished claim becomes a `## Risks / decisions` premise ending `spec author pins this`, counted as open. Within those targets, neither fold nor move is autonomous: show verification's result to the operator first.

The verification order is: classify every finding; verify all actionable facts; compose findings that target the same draft text into one intended result; edit; then re-read the changed section and every section that consumes the changed decision. Reviewer prose is a lookup hint, never evidence.

### Decision 8 — A settled-decision contradiction gets a separate operator prompt

A finding contradicts a settled decision when accepting it would change any of these:

- a numbered `## Decisions carried forward` branch or its rationale;
- an operator-set `## Out of scope` fence;
- an explicit ticket decision used under `--no-grill`;
- an acceptance statement transcribed into `## Done when`.

Model-inferred prose and existing `## Risks / decisions` items are not settled decisions. Batch contradictions after factual verification and before Confirm, at most `question_cap` items per cycle (7 under `--no-grill`); Decision 11 caps the whole report at that size. Show each settled text, challenge and verification result, including unavailable or disproved evidence. Require one line per finding: `F-<n>: keep`, `F-<n>: replace: <non-empty replacement text>`, or `F-<n>: reopen`; a global `abort` stops with nothing written. Conflicting or missing item answers re-print the unanswered/invalid items and retain valid answers and the interview; never infer keep, replace or reopen. Overlapping contradictory challenges are shown together and their answers must compose to one intended replacement. Every tier waits while a pass runs. Invalid replies never discard interview work; only explicit abort ends these reconciliation prompts.

### Decision 9 — A `big` operator skip requires a reason

The `big` offer is:

```text
Doubt pass: a fresh-context reviewer from a different model family is available.
1. Run the doubt pass
2. Skip — reply `2: <reason>`
3. Abort — nothing written
```

The text after `2:` must be non-empty after trimming and becomes `operator declined — <reason>`. A bare `2`, empty reason or unrecognized reply re-prints the offer and retains the interview, however many times needed. Only option 3 aborts this menu. Generated skips (`small`, unavailable reviewer, dispatch failure) already have normalized reasons and require no invented operator reason.

### Decision 10 — Reconcile in contract/action/trade-off/noise order

First detect Decision 8 targets: a finding that would change a settled decision is a contradiction whatever else it is, including a true fact, a contract objection or an unverifiable premise. Verify its factual claims first and show the result in the operator batch; no autonomous fold or move may bypass that batch. For the remaining findings, use the following order:

1. **Contract misread** — the finding asks for something outside the ticket/brief contract or misreads the draft. Reject with one-line evidence; no draft edit.
2. **Actionable fact or anchor** — verify live. Fold when true; reject when disproved; move to Risks / decisions when it cannot be established, only outside settled targets.
3. **Trade-off / settled-decision contradiction** — route through Decision 8's operator prompt; never fold autonomously.
4. **Noise / duplicate** — reject with the duplicate id or one-line reason.

The caller owns classification; reviewer-provided classes are advisory. Contract narrowing expressly recorded in Origin or settled Out of scope is not a missing ticket requirement; identify a challenge to that narrowing as an operator decision conflict.

### Decision 11 — The reviewer report is ephemeral but machine-checkable

The fresh reviewer returns:

```markdown
# Doubt review — cycle <n>

## Findings

### F-1: <title>
**Target:** <draft section/item>
**Challenge:** <one falsifiable concern>
**Evidence:** <ticket quote, path:line, or evidence needed>
**Suggested change:** <concrete draft edit or operator question>
**Decision touched:** <decision number/title | none>

## Summary
Findings: 1

STATUS: DOUBT FINDINGS=1
```

The last non-blank line is `STATUS: READY` only for zero findings, otherwise `STATUS: DOUBT FINDINGS=<n>` for a positive integer. Count only unfenced `### F-<n>:` headings; fences of at least three backticks or tildes open/close with the same character and a closing marker at least as long. Require unique ids, all five non-empty fields, and equality of summary count, status count (READY means zero) and block count, with count no greater than `question_cap`. Missing/malformed fields or status, inconsistent counts, excess findings, empty return, a host-reported timeout or dispatch error is failure. Print `Doubt pass dispatch failed: cycle <n>; class <reason>; last line: <last non-blank reviewer line | none>` without persisting raw output. Only the normalized outcome reaches the brief.

### Decision 12 — Failure posture follows tier and never silently substitutes same-model review

Resolve eligibility before the interview and before offering/running the pass. No tier substitutes same-family review. On any dispatch failure, print Decision 11's failure line and prompt:

```text
1. Retry once (shown only if this cycle's retry is unused)
2. Skip (shown only for small/big)
3. Abort — nothing written
```

At most one retry per cycle, including a parse failure; it is a fresh dispatch of the same held candidate, not a new cycle. Invalid answers re-print the available choices and retain the interview. After the retry is used or declined, apply the existing tier outcomes when Skip is chosen: without a completed cycle, announce/record `skipped — reviewer dispatch failed — <short reason>`; after reconciled cycle 1, preserve its edits and record `completed at cap`, `Cycles: 1`, with its counts and an explicit Confirm disclosure that cycle 2 failed and final edits were not re-reviewed. Under `irreversible` Skip is unavailable: after an exhausted retry only Abort remains, and the run stops with nothing written. Explicit Abort at any failure stops with nothing written.

Delete the cycle-2-failure status and `dispatch_failed` flag. A completed record means at least one cycle was successfully reconciled, not that every attempt succeeded; `completed at cap` discloses unfinished review. Deliberately adopt conventions F-7's simpler furthest-completed-state rule: tier-only upgrades retain a completed record, including this at-cap record; only a skip needs a new pass. This supersedes the prior spec's special restart rule because the brief requires that a pass ran, while a newly attempted failure under irreversible still cannot be skipped. Confirm must show the disclosure on that upgrade too.

## Design

### 1. Extend Phase 0 state without changing invocation syntax

Keep the invocation and tier gate. Hold the resolved ticket text (or local-only paragraph) as `ticket_contract`, with a labelled seed-gate paragraph whenever one was collected. The seed gate currently substitutes that paragraph as the seed in ticket mode while retaining the ticket header (`skills/spec-brief/SKILL.md:88`). Carry both into the contract without a second tracker lookup. After a non-tweak tier is chosen, resolve:

- the author family, reviewer candidate and eligibility evidence under Decision 5;
- `reviewer_eligible` only when different-family, fresh-context and read-only evidence all pass;
- `doubt_policy` from the tier.

On initial `irreversible` with no eligible reviewer, print `irreversible needs an eligible cross-model reviewer — not available on this host` and halt immediately after the tier gate, before the interview. Do not dispatch before the interview: the reviewed artifact must include its settled decisions and open frontier.

### 2. Render the candidate draft once the interview path ends

Refactor only the prose flow, with no helper file. Apply the mapping and Scale-emission rules once on the invocation's first entry to Phase 3 to create the held candidate, containing every final section except `## Doubt pass`. Under `--no-grill`, initial decision derivation uses only explicit ticket decisions, as the current rule requires (`skills/spec-brief/SKILL.md:184`). Thereafter the candidate is authoritative, including when Phase 3 is re-entered: “re-render” means checking and displaying its edited text, not re-applying initial mappings.

Verified folds may edit Problem, Why it matters, Scope, Done when, Risks / decisions and References; metadata or factual anchors there may also be corrected. A fold must not autonomously change Decisions carried forward, Out of scope, an explicit ticket decision, a transcribed acceptance statement or their rationale: Decision 8 takes precedence, even inside an otherwise editable section. Tier and Scale remain operator-set and require operator resolution for any proposed change. Operator replacements/reopens may edit their targeted section and all consuming sections after the answer. Record source evidence for every factual correction.

Amend the transcription rule, which currently says Problem, Why it matters and Done when are transcribed and never inferred (`skills/spec-brief/SKILL.md:224`): initial text is transcribed, but a live-verified fold outside settled targets or an explicit operator replacement may change it afterward. Phase 5 must preserve that exception rather than restoring ticket wording. After each edit, check the held candidate's sections for consistency so cycle 2 and Confirm receive the composed artifact.

### 3. Gate by tier and reviewer eligibility

Use Decision 5's eligibility evidence and Decision 3's tier policy. Announce every skip immediately. The initial irreversible eligibility halt belongs after the tier gate, as Design 1 specifies; Phase 3 never repeats its wait test.

For `small`, go directly to Confirm with the tier-small skip, including on a host without a reviewer. Show option 5 only when eligible; selection records an explicit request and runs the pass without the big offer. Once a result returns, hide option 5 for that unchanged candidate so it cannot reset the two-cycle bound. A substantive revision creates a new candidate pass under Design 6.

### 4. Dispatch fresh, read-only doubt reviews

Each dispatch prompt contains only:

- `draft_brief: |` followed by the exact held candidate excluding only any previous `## Doubt pass` audit block;
- `ticket_contract: |` followed by the resolved ticket text/local-only paragraph and any labelled seed-gate paragraph;
- `project_root` for live read-only verification;
- `wiki_root` and `project_slug` when Phase 0 resolved them (otherwise declare wiki unavailable);
- `cycle_number` (`1` or `2`);
- `question_cap` as the report/finding work bound (7 under `--no-grill`);
- the report schema from Decision 11;
- instructions to challenge false premises, stale or unsupported anchors, acceptance-criterion gaps, and internal contradictions; to identify decision conflicts rather than resolve them; and to make no mutations.

Use the narrowest read-only class or sandbox available for the selected mechanism; a write-capable-only mechanism is ineligible. State that the reviewer has no authority to change settled decisions and makes no mutations, including report writes. Bound evidence work to paths cited in the candidate or contract; return `evidence needed` for a gap rather than search exhaustively, and return at most `question_cap` findings. Origin and settled Out of scope may legitimately narrow stale ticket text; identify that decision rather than treating the narrowing as a defect. Receive no prior conversation, Grill summary, author rationale or prior report. Use a host call timeout when offered; absent such support, do not invent a timeout guarantee.

### 5. Reconcile one complete report before considering another cycle

Apply Decision 11's status/count/field/fence checks before reconciliation; a failed report goes to Decision 12's retry/skip/abort prompt. Otherwise classify every finding under Decision 10, with settled-target precedence, before editing.

For overlaps, declare one intended result and compose the findings. Verify sources, edit eligible candidate text, run the operator contradiction batch, update Risks / decisions, then re-read all changed and consuming sections. Hold Decision 4's cumulative distinct-root counts. If cycle 1 changed the candidate, dispatch cycle 2 with that held text. Reconcile cycle 2 identically but stop at the cap. Neither display nor count generation re-derives candidate content.

### 6. Renumber Confirm and Write and make the outcome visible

Rename the existing sections to `## Phase 4 — Confirm` and `## Phase 5 — Write`. Confirm previews the full final candidate including the `## Doubt pass` block and prints one summary line:

```text
Doubt pass: <completed in N cycle(s) | completed at cap (N cycle(s)) | skipped — reason>
```

Retain the write/revise/abort/change-tier choices currently at `skills/spec-brief/SKILL.md:170`–`skills/spec-brief/SKILL.md:176`, adding option 5 only under Design 3's small rule. Full preview is a spec-level addition. At-cap always adds `Final reconciliation edits were not re-reviewed`; after cycle-2 failure, also print `Cycle 2 failed; only cycle 1 completed` (ephemeral disclosure, not a new result or gate flag).

Changing tier asks the tier gate again, then re-evaluates the doubt policy. With no eligible reviewer, an irreversible choice prints Design 1's message and re-shows the tier prompt, retaining the interview, candidate and previous tier until a feasible answer. Invalid replies re-show the prompt and discard nothing, consistent with the current post-interview tier rule (`skills/spec-brief/SKILL.md:180`). A feasible tier-only change updates the candidate's Tier and basis preview; Decision 12 deliberately retains completed outcomes across tiers, including at-cap. Only a prior skip is re-evaluated; an eligible upgrade to irreversible runs Phase 3, and failure while that tier is active cannot skip. A tweak choice follows the existing no-write exit (`skills/spec-brief/SKILL.md:180`).

Every substantive Confirm content change invalidates the result; tier-only changes use the preceding rule. On Phase 3 re-entry remove only the outdated doubt audit block and preserve the rest of the candidate. Before option 2 resumes grilling, carry each contradiction answer as the settled item's current text/rationale: keep preserves it, replace substitutes it, and reopen records the operator's settled choice to leave the named issue open plus its Open frontier item. Amend genuine Q-linked Settled items within `prior_summary`; its shared Settled grammar requires `(Q<n>)` (`skills/grilling/SKILL.md:140`). Keep ticket decisions and replacement acceptance statements without a Q in the authoritative candidate and supply them as separately labelled operator-settled constraints in the existing `seed` context, outside the summary's Settled section. Do not invent Q numbers or reset resume counters. Pass the amended summary, those named constraints and the Q to revise under the existing resume contract, which reopens that Q and its downstream decisions (`skills/grilling/SKILL.md:21`, `skills/grilling/SKILL.md:23`). Any such deliberate reopening names the affected resolutions; the prior answer is never silently restored.

After the resumed interview returns, update only candidate sections affected by its explicit revised decisions and their consumers, preserving unrelated verified folds, operator resolutions and source anchors. Named Q-less constraints remain in the held candidate even when absent from the returned summary; only an explicit operator revision that names an affected constraint may reopen or replace it. Re-run Phase 3 from cycle 1 under the current tier. Under `--no-grill`, option 2's current Add a decision branch (`skills/spec-brief/SKILL.md:184`) appends directly to the held candidate, preserving prior corrections; clear the result and re-enter Phase 3 under the tier policy. Neither path reuses old reviewer output. Retain the existing post-cap option-2 omission and resume arithmetic (`skills/spec-brief/SKILL.md:182`).

Phase 5 writes the exact full candidate Confirm displayed, with exactly one Decision 4 outcome block already inserted; never re-run initial mapping or append a second block. Keep the existing temporary-sibling atomic write (`skills/spec-brief/SKILL.md:218`). Renumber only spec-brief's own phase references, including `skills/spec-brief/SKILL.md:124`, `:180`, `:182`, `:216` and the spec-brief block at `docs/spec-workflow-reference.md:23`–`:25`. Do not renumber the reference to spec-cycle's parser at `skills/spec-brief/SKILL.md:188` or the spec-cycle and ship-spec phase headings (`docs/spec-workflow-reference.md:102`, `:246`).

### 7. Update the non-mutation and failure documentation

Preserve the existing mutation boundary in `## What /spec-brief never does` (`skills/spec-brief/SKILL.md:256`) and explicitly forbid doubt reports or pre-confirmation brief writes. Add the fresh read-only cross-model dispatch to `## Tool-use notes`. Add these `## Failure modes`:

- no eligible different-family reviewer;
- malformed/empty/timed-out reviewer output;
- a reviewer dispatch that never returns blocks the run; a host-offered call timeout is used when available and its expiry is dispatch failure;
- operator abandons the contradiction batch;
- cycle-2 failure preserves the furthest completed state under small/big after the retry/skip choice;
- invalid `big` skip reason;
- `irreversible` cannot skip an unavailable or failed pass; failed dispatch offers one retry per cycle, otherwise stops with nothing written;
- invalid post-interview replies re-print their prompt and preserve the interview; only explicit abort ends those prompts.

### 8. Mirror the public contract

In the spec-brief block of `docs/spec-workflow-reference.md`, insert Phase 3 and renumber Confirm/Write; mirror the held candidate, eligibility, tier policy, two-cycle/one-retry bounds, reconciliation precedence, operator ownership and outcome record. Update § Stakes tier (`docs/spec-workflow-reference.md:147`–`:152`): small defaults to a skip with the Confirm-only override, big offers run or a reasoned skip when eligible, and irreversible requires a pass with an early no-reviewer halt and no dispatch-failure skip. Update the same clauses in AGENTS' Stakes tier paragraph (`AGENTS.md:35`). Keep other skills' phase numbers intact.

In `README.md:9` and `AGENTS.md:25`, add one compact clause: after the bounded interview, `/spec-brief` runs or explicitly skips a fresh-context cross-model doubt pass before confirmation. At `README.md:65`, say the pass additionally needs any session-available fresh-context mechanism declaring a different family and offering read-only execution; shell/installed-skill bridges count, absence degrades by tier. Name no vendor tool or same-model fallback.

## Test plan

This is a prose-only skill change. Review the final diff against this matrix:

1. Phase order is Grounding → seed gate → tier gate → Interview (optional) → Doubt pass → Confirm → Write, including `--no-grill`.
2. `small` announces the tier-small skip without a new wait, even without a reviewer; Confirm option 5 appears only when eligible, runs the pass and returns to Confirm, then hides for the unchanged candidate.
3. `big` offers run/skip/abort; skip requires a non-empty reason; invalid answers preserve the interview and re-print indefinitely. No-reviewer and failed-dispatch skips are announced and recorded.
4. Initial `irreversible` without a reviewer halts immediately after the tier gate, before interview; unavailable Confirm upgrades re-show the tier prompt and retain work. Failures while irreversible is active allow one retry per cycle, then only Abort; nothing is written. A tier-only upgrade retains a completed at-cap record with its unfinished-review disclosure under Decision 12's deliberate simplification. The no-wait halt is tested at the existing tier gate, not as a Phase 3 branch.
5. Cycle 2 occurs only after a cycle-1 draft change; no cycle 3 exists; a cycle-1 all-rejected result stops without a theater pass.
6. Fact/anchor findings are live-verified before edits, overlapping edits are composed, consumers are re-read, and unverifiable claims become Risks / decisions.
7. Any finding changing a settled target takes contradiction precedence, even a verified fact or unavailable premise. Evidence is checked first, shown in the bounded per-item batch, and missing/invalid/contradictory answers never become implicit keep/replace/reopen; only explicit abort stops those prompts. Include ticket-stated decisions under `--no-grill`.
8. Changing tier, revising an interview answer, and adding a decision under `--no-grill` follow Design 6's invalidation rules and re-enter Phase 3 when required.
9. Every written brief has exactly one `## Doubt pass` section; every skip has a normalized reason; completed records contain counts but no raw reviewer prose or model/vendor name.
10. The skill still promises and performs no filesystem write before final confirmation.
11. `skills/grilling/SKILL.md` is unchanged, and no proof ladder, sandboxed run, same-model fallback, or vendor tool enters the diff.
12. README, AGENTS, and the workflow reference agree with the skill on phase order, tier behavior, and the two-cycle cap.
13. Portability lint accepts the unchanged `requires` block and the full stdlib test suite passes.
14. A verified Problem fold and operator Done-when replacement survive display, cycle 2 and write; written bytes equal the full Confirm preview. On revise of an unrelated Q, Q-linked answers amend Settled while Q-less resolutions remain in the candidate and named seed constraints without extending the summary grammar; neither is lost when the summary returns. Unrelated folds remain, and revising a dependent Q explicitly names reopened resolutions. The no-grill Add a decision preserves earlier corrections.
15. Eligibility checks explicit family and mode evidence consistently for native, skill and shell mechanisms; unknown/same-family/write-capable-only candidates are ineligible. Prompts carry resolved wiki context, collected seed paragraph and the report work bound; narrowed Origin/Out-of-scope is respected.
16. Parse zero/positive counts, duplicate ids, missing fields, fenced fake headings and report-cap violations; every failure prints cycle/class/last line and offers available retry/skip/abort choices. One retry per cycle never adds a cycle or reuses malformed prose. Test cycle-1 skip, cycle-2 furthest-completed result, irreversible abort and invalid replies.
17. Two-cycle counts deduplicate repeated roots and count reopen as resolved plus its new open item; Result never collides with the ticket Status label. Renumber only spec-brief references; the per-tier tables and summaries match.

## Test command

```text
python lint.py --strict
python -m unittest discover -s tests -p "test_*.py"
```

## Done when

- `/spec-brief` runs the cross-model doubt pass or announces that it skipped it, and every written brief records the completed or skipped outcome in `## Doubt pass` (completed records are the flagged spec-level addition in Decision 4).
- A finding that contradicts a settled decision reaches the operator in a separate pre-Confirm reconciliation prompt; the skill never folds it alone.
- An `irreversible` brief is never written unless a cross-model cycle completed; an initial no-eligible-reviewer halt precedes interview, and a failed dispatch while irreversible is active cannot skip and ends with nothing written after the retry/abort choices.
- `python lint.py --strict` and `python -m unittest discover -s tests -p "test_*.py"` pass.

## Out of scope

- The proof ladder and its Write gate (VHS-67).
- A sandboxed run in `grilling` (VHS-66); `skills/grilling/SKILL.md` remains unchanged.
- Shipping a `codex` skill, naming any vendor's tool in the skill, or adding a vendor/model lookup table.
- A same-model fallback when no different-family reviewer is eligible.
- A new reviewer agent file, persistent doubt-review report, script, test module, or capability key.
- Changes to `/spec-cycle`, `/ship-spec`, `/spec-close`, `/spec-tickets`, reviewer agents, `lint.py`, `sync.py`, or any `VHS-41.*` path.

## Deferred (P2+)

- round-1 correctness/F-4 + edge-cases/F-3 — Canonical ticket verification was unavailable because shared memory denied the `skills` namespace; the brief remained the local source of truth, so no speculative scope edit was made.
- round-1 edge-cases/F-4 — A maximum length for the operator's free-text `big` skip reason is an optional audit-size improvement; the required contract only pins non-empty, recorded reasoning.
- cross-model-claude correctness/F-6 — Ticket-cache access is a review-environment process note with no proposed spec fix; use the brief's recorded narrowed contract until an authorized ticket read is available.
- cross-model-claude edge-cases/F-4 (snapshot suggestion only) — Read-only eligibility is folded; before/after git-status snapshots add detection that cannot prevent a forbidden write and can confuse unrelated concurrent edits, so no additional mutation-detection machinery is specified.
- round-4 edge-cases/F-1 — Canonical-ticket grounding remains unavailable under this invocation's declared network outage; the brief's narrowed contract is used, with no speculative scope change.

## Post-green polish

- conventions/R4/F-1 (P2) — Clarified Design 6's resume serialization and Test plan 14: Q-linked answers amend the existing summary; Q-less resolutions are retained as named seed constraints and in the candidate. This preserves the resolution-retention decision without extending grilling's shared grammar.
