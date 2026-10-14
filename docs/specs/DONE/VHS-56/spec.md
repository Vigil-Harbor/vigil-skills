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

Decisions 1–10 pin the brief's Risks / decisions 1–10 in order. Decision 4's completed-pass record, Decisions 11–12 and the positions below are **spec-level additions**:

- Full-candidate Confirm preview (Design 6): the operator must see the text that will be written, including corrections outside Decisions and Risks.
- Completed-pass record and cumulative counts (Decision 4): disclose what was reviewed and whether the last edit was re-reviewed, alongside mandatory skip records.
- Explicit Abort in the big offer and failure menus (Decisions 9 and 12): give the operator a clear exit before writing.
- Read-restricted eligibility and deterministic selection, a bounded lenient report and one retry per cycle (Decisions 5, 11 and 12): preserve the mutation boundary and recover from a transient failure without increasing the cycle cap.
- Furthest-completed-state handling after cycle-2 failure (Decision 12): disclose partial review with the at-cap result.
- Initial irreversible eligibility halt and preserving the interview on an unavailable Confirm upgrade (Design 1 and 6): avoid spending or losing interview work on an impossible tier.
- Candidate retention, transcription exceptions and amended resume summary (Decision 1 and Design 2/6): prevent a verified fold or operator resolution from reverting during rendering, revise or write.

### Decision 1 — Review an in-memory rendered draft, not a pre-confirmation file

Phase 3 always runs after the interview path, including `--no-grill`: first render and hold the complete candidate, excluding `## Doubt pass` until its outcome is known, then apply the gate. “Directly to Confirm” means without an offer or dispatch. That held text is the source of truth after the initial mapping. Reconciliation edits it in place; subsequent rendering means displaying and checking it, never re-deriving it from an unchanged summary or ticket. The reviewer receives the candidate verbatim, the resolved ticket contract including any seed-gate paragraph, and Design 4's grounding context; no interview transcript, author reasoning, history or claim that the draft is correct.

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

Counts are per distinct finding root (same target and concern) across reconciled cycles; a root's last disposition wins. Folded means verified autonomous fact/anchor edits; operator resolved includes keep, replace and reopen; rejected means disproved, contract misread, noise or cut at the report cap. Open counts resulting unresolved Risks / decisions items, including reopens. Print the number cut separately to the console. `completed in N cycle(s)` maps to `Result: completed`, `Cycles: N`; at-cap uses its literal result and successfully reconciled cycle count.

### Decision 5 — Eligibility requires declared different-family identity and read-only dispatch

Any session-available native, installed-skill or shell mechanism counts when it itself states its model family or provider in its instructions, configuration or runtime output (such as a provider or model line). Its own provider/vendor statement counts as its family; an author's inference from its tool name does not. Compare like with like, trimmed and case-insensitive: a stated model family with the author's self-reported model family, or a stated provider with the author's self-reported provider. When no comparable pair exists, the family is unknown. Require a selectable model, fresh context, the narrowest read-restricted agent class or a read-only sandbox mode (`skills/spec-brief/SKILL.md:78`), and a separable final response obtained without a file. A skill must identify its underlying dispatch. Unknown/same family, unknown mode or write-capable-only execution is ineligible.

Prefer the mechanism's own configured default model, then its documented default; otherwise use its declared ranking. If eligible mechanisms/models remain tied, ask the operator to select one and hold that choice. One pre-interview identity probe through the selected mechanism is allowed in its read-restricted/read-only mode, with no draft or repository content, solely to read identity; its output is runtime evidence. Hold mechanism, model and family evidence. At each real cycle/retry, compare the reported identity with that evidence; missing or mismatched identity is dispatch failure. Every dispatch is fresh-context with explicit no-mutation instructions. On an eligibility skip or halt, print every candidate mechanism and its first failed check to the console only. Name no vendor/tool and maintain no identity table.

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

Model-inferred prose and existing `## Risks / decisions` items are not settled decisions. After verification, batch at most 7 contradictions per cycle before Confirm. Show each settled text, challenge and verification result, including unavailable/disproved evidence. Accept `F-<n>: keep`, `F-<n>: replace: <non-empty text>`, or `F-<n>: reopen`; a comma-separated id group may answer overlapping challenges together. Replacement text may continue on indented lines. Re-print missing, invalid or conflicting items with the specific reason, retaining valid answers and interview work. Unknown ids and mixed abort/item replies are invalid; `abort` as the sole non-blank line stops with nothing written. Overlapping answers must compose to one intended result; never infer an answer. Every tier waits while a pass runs. For resume conflicts, use the same prompt with temporary F ids; this is caller reconciliation, not another reviewer cycle.

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

The caller owns classification; reviewer-provided classes are advisory. Contract narrowing expressly recorded in Origin or settled Out of scope is not a missing ticket requirement; identify a challenge to that narrowing as an operator decision conflict. A Tier finding is advisory evidence shown at Confirm; only Confirm's change-tier option and the tier gate change Tier. A Scale finding goes to Risks / decisions ending `spec author pins this`, or is resolved through the four Scale emission cases (`skills/spec-brief/SKILL.md:233`–`:240`); neither uses a free-text Tier/Scale replacement in the contradiction batch.

### Decision 11 — Read an ephemeral report leniently

Reviewer output is the mechanism's final response message, separate from progress/transport output, obtained without writing a file. Send the exact prompt by stdin or argv, never a file. Strip one outer fence wrapping the whole response. Ask for at most 7 findings per cycle, independent of `--questions`, in this suggested shape:

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

Judge host errors/timeouts first. A report-reading failure is only an empty return or one with neither readable finding blocks nor an explicit clean statement (such as `STATUS: READY`), matching `vigil-harbor-wiki/decisions/2026-10-11-vhs-55-ceremony-follows-an-operator-set-stakes-tier.md:43`. Missing fields, duplicate ids and inconsistent/missing counts or status do not fail readable findings: the author classifies them under Decision 10 and assigns unambiguous batch ids. Retain the first 7 finding blocks in response order; cut and count the rest without reconciliation. Decision 5's identity failure is separate. Print `Doubt pass dispatch failed: cycle <n>; class <reason>; last line: <last non-blank final-response line | none>`; a timeout reason includes the bound used. Persist only the normalized outcome.

### Decision 12 — Failure posture follows tier and never silently substitutes same-model review

Resolve eligibility before the interview and before offering/running the pass. No tier substitutes same-family review. On any dispatch failure, print Decision 11's failure line and prompt:

```text
1. Retry once (shown only if this cycle's retry is unused)
2. Skip (shown only for small/big)
3. Abort — nothing written
4. Accept cycle 1 (completed at cap) (irreversible only, after cycle 2's retry is exhausted and cycle 1 reconciled and changed the draft)
```

At most one retry per cycle; it is a fresh dispatch of the same held candidate, not a new cycle. Invalid answers re-print the available choices and retain the interview. Small/big Skip without a completed cycle announces/records `skipped — reviewer dispatch failed — <short reason>`. Skip after reconciled cycle 1, or irreversible's Accept cycle 1, preserves its edits and records `completed at cap`, `Cycles: 1`, with its counts and Confirm disclosure that cycle 2 failed and final edits were not re-reviewed. Irreversible never skips; after an exhausted retry without the Accept precondition only Abort remains. Explicit Abort always stops with nothing written.

A completed record means at least one cycle reconciled; `completed at cap` discloses unfinished review, with no separate failure result or flag. A tier-only change keeps any completed record, including at cap; only a skip is re-evaluated, because the brief requires that a pass ran. Confirm shows the disclosure after an upgrade too.

## Design

### 1. Extend Phase 0 state without changing invocation syntax

Keep the invocation and tier gate. Hold the resolved ticket text (or local-only paragraph) as `ticket_contract`, with a labelled seed-gate paragraph whenever one was collected. The seed gate currently substitutes that paragraph as the seed in ticket mode while retaining the ticket header (`skills/spec-brief/SKILL.md:88`). Carry both into the contract without a second tracker lookup. After a non-tweak tier is chosen, resolve:

- the author family, reviewer candidate and eligibility evidence under Decision 5;
- `reviewer_eligible` only when all Decision 5 checks pass;
- `doubt_policy` from the tier.

On initial `irreversible` with no eligible reviewer, print `irreversible needs an eligible cross-model reviewer — not available on this host` plus Decision 5's candidate diagnostics, and halt immediately after the tier gate, before the interview. Before the interview allow only Decision 5's content-free identity probe; a real review waits for the settled decisions and open frontier.

### 2. Render the candidate draft once the interview path ends

Refactor only the prose flow, with no helper file. Apply the mapping and Scale-emission rules once on the invocation's first entry to Phase 3 to create the held candidate, containing every final section except `## Doubt pass`. Under `--no-grill`, initial decision derivation uses only explicit ticket decisions, as the current rule requires (`skills/spec-brief/SKILL.md:184`). Thereafter the candidate is authoritative, including when Phase 3 is re-entered: “re-render” means checking and displaying its edited text, not re-applying initial mappings.

Verified folds may edit Problem, Why it matters, Scope, Done when, Risks / decisions and References; metadata or factual anchors there may also be corrected. A fold must not autonomously change Decisions carried forward, Out of scope, an explicit ticket decision, a transcribed acceptance statement or their rationale: Decision 8 takes precedence, even inside an otherwise editable section. Tier/Scale findings follow Decision 10's dedicated routes. Operator replacements/reopens may edit their targeted section and all consumers after the answer. Record source evidence for every factual correction.

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
- `finding_cap: 7`, independent of interview flags;
- the report schema from Decision 11;
- instructions to challenge false premises, stale or unsupported anchors, acceptance-criterion gaps, and internal contradictions; to identify decision conflicts rather than resolve them; and to make no mutations.

Use the selected narrowest read-restricted agent class or a read-only sandbox mode, with no mutations (including report writes) and no authority to change settled decisions. Bound evidence work to cited paths; return `evidence needed` for gaps and at most 7 findings. Origin/settled Out of scope may narrow stale ticket text: identify that decision rather than a defect. Receive no conversation, Grill summary, author rationale or prior report. Use the longest call timeout the host offers or a background dispatch it can wait on, never a shorter default; if neither supplies a bound, state that no timeout guarantee exists. Obtain identity evidence separately from the final response, check it under Decision 5, and read the response under Decision 11.

### 5. Reconcile one complete report before considering another cycle

Apply Decision 5's identity check and Decision 11's lenient reading/cut before reconciliation; failures go to Decision 12's available choices. Otherwise classify each retained finding under Decision 10, with settled-target precedence, before editing.

For overlaps, declare one intended result and compose the findings. Verify sources, edit eligible candidate text, run the operator contradiction batch, update Risks / decisions, then re-read all changed and consuming sections. Hold Decision 4's cumulative distinct-root counts. If cycle 1 changed the candidate, dispatch cycle 2 with that held text. Reconcile cycle 2 identically but stop at the cap. Neither display nor count generation re-derives candidate content.

### 6. Renumber Confirm and Write and make the outcome visible

Rename the existing sections to `## Phase 4 — Confirm` and `## Phase 5 — Write`. Confirm previews the full final candidate including the `## Doubt pass` block and prints one summary line:

```text
Doubt pass: <completed in N cycle(s) | completed at cap (N cycle(s)) | skipped — reason>
```

Retain the write/revise/abort/change-tier choices currently at `skills/spec-brief/SKILL.md:170`–`skills/spec-brief/SKILL.md:176`, adding option 5 only under Design 3's small rule. Full preview is a spec-level addition. At-cap always adds `Final reconciliation edits were not re-reviewed`; after cycle-2 failure, also print `Cycle 2 failed; only cycle 1 completed` (ephemeral disclosure, not a new result or gate flag).

Changing tier asks the tier gate again, then re-evaluates the doubt policy. With no eligible reviewer, an irreversible choice prints Design 1's message and re-shows the tier prompt, retaining the interview, candidate and previous tier until a feasible answer. Invalid replies re-show the prompt and discard nothing, consistent with the current post-interview tier rule (`skills/spec-brief/SKILL.md:180`). A feasible tier-only change updates the candidate's Tier and basis preview; Decision 12 deliberately retains completed outcomes across tiers, including at-cap. Only a prior skip is re-evaluated; an eligible upgrade to irreversible runs Phase 3, and failure while that tier is active cannot skip. A tweak choice follows the existing no-write exit (`skills/spec-brief/SKILL.md:180`).

Every substantive Confirm content change invalidates the result; tier-only changes use the preceding rule. On Phase 3 re-entry remove only the outdated audit block. Before option 2 resumes grilling, amend Q-linked `prior_summary` items: keep preserves current text/rationale, replace substitutes it, and reopen removes it from Settled and appears once in Open frontier as `(Q<n>) … unresolved because: deferred` (`skills/grilling/SKILL.md:140`, `:143`). Retain Q-less operator resolutions in the candidate (Q-less reopens only there); pass `seed` again with kept Q-less resolutions in its problem-statement part (`skills/grilling/SKILL.md:18`) as explicitly labelled operator-settled constraints the interview must not re-decide. They are not grounding facts: an empirical claim inside one keeps its verification status and is never recorded as an established fact (`skills/grilling/SKILL.md:159`). Pass the amended summary and Q to revise under the existing resume contract, which reopens that Q and downstream decisions (`skills/grilling/SKILL.md:21`, `:23`); invent no Q numbers and reset no counters.

After resume, compare every returned decision with kept resolutions; any conflict goes through Decision 8 before Phase 3 runs again, including under small. Update affected candidate sections and consumers, preserving unrelated verified folds, resolutions and anchors. Always refresh the `Interview:` References bullet from the returned header (`skills/spec-brief/SKILL.md:231`), newly established facts into References and Scope under the existing mapping (`:229`, `:230`), and derive BRIEF WRITTEN settled/open counts from the written candidate rather than the summary (`:247`). Restart Phase 3 at cycle 1 under the current tier. Under `--no-grill`, option 2's Add a decision branch (`:184`) appends to the held candidate, preserves corrections, clears the result and re-enters Phase 3. Neither path reuses reviewer output. Retain the post-cap option-2 omission and resume arithmetic (`:182`).

Phase 5 writes the exact full Confirm candidate with one outcome block; never re-run initial mapping or append another. Keep the temporary-sibling atomic write (`skills/spec-brief/SKILL.md:218`). Renumber only spec-brief's own phase references (`:124`, `:180`, `:216`) and headings (`:166`, `:186`); route `:124`'s `--no-grill` destination to Doubt pass. In `docs/spec-workflow-reference.md:11`, `:21`, name Doubt pass among the steps `--no-grill` retains; renumber its spec-brief block (`:23`–`:25`). Leave the spec-cycle parser reference (`skills/spec-brief/SKILL.md:188`) and other skills' phase headings (`docs/spec-workflow-reference.md:102`, `:246`) intact.

### 7. Update the non-mutation and failure documentation

Preserve the existing mutation boundary in `## What /spec-brief never does` (`skills/spec-brief/SKILL.md:256`) and explicitly forbid doubt reports or pre-confirmation brief writes. Add the fresh read-only cross-model dispatch to `## Tool-use notes`. Add these `## Failure modes`:

- no eligible different-family reviewer;
- empty/unreadable, host-error/timed-out output or missing/mismatched run identity;
- a never-returning dispatch blocks the run; use Design 4's longest timeout or waitable background route and print the bound on timeout failure;
- operator abandons the contradiction batch;
- cycle-2 failure preserves the furthest completed state under small/big after the retry/skip choice;
- invalid `big` skip reason;
- `irreversible` never skips; offer one retry per cycle, then Accept cycle 1 only under Decision 12's precondition, otherwise Abort with nothing written;
- invalid post-interview replies re-print their prompt and preserve the interview; only explicit abort ends those prompts.

### 8. Mirror the public contract

In the spec-brief block of `docs/spec-workflow-reference.md`, insert Phase 3 and renumber Confirm/Write; mirror the held candidate, eligibility, tier policy, two-cycle/one-retry bounds, reconciliation precedence, operator ownership and outcome record. Update § Stakes tier (`docs/spec-workflow-reference.md:147`–`:152`): small defaults to a skip with the Confirm-only override, big offers run or a reasoned skip when eligible, and irreversible requires a pass with an early no-reviewer halt and no dispatch-failure skip. Update the same clauses in AGENTS' Stakes tier paragraph (`AGENTS.md:35`). Keep other skills' phase numbers intact.

In `README.md:9` and `AGENTS.md:25`, add one compact clause: after the bounded interview, `/spec-brief` runs or explicitly skips a fresh-context cross-model doubt pass before confirmation. At `README.md:65`, require a session-available fresh-context mechanism that itself states a different family/provider and offers the narrowest read-restricted agent class or a read-only sandbox mode; shell/installed-skill bridges count under Decision 5, absence degrades by tier. Name no vendor tool or same-model fallback.

## Test plan

This is a prose-only skill change. Review the final diff against this matrix:

1. Phase order is Grounding → seed gate → tier gate → Interview (optional) → Doubt pass → Confirm → Write, including `--no-grill`.
2. `small` announces the tier-small skip without a new wait, even without a reviewer; Confirm option 5 appears only when eligible, runs the pass and returns to Confirm, then hides for the unchanged candidate.
3. `big` offers run/skip/abort; skip requires a non-empty reason; invalid answers preserve the interview and re-print indefinitely. No-reviewer and failed-dispatch skips are announced and recorded.
4. Initial `irreversible` without a reviewer halts after the tier gate, before interview; unavailable Confirm upgrades re-show the tier prompt and retain work. Cycle-1 failure offers one retry then only Abort. After reconciled cycle 1 changes the draft and cycle 2 exhausts its retry, offer Accept cycle 1 beside Abort, yielding the same disclosed at-cap record as a tier-only upgrade. Test the no-wait halt at the existing tier gate.
5. Cycle 2 occurs only after a cycle-1 draft change; no cycle 3 exists; a cycle-1 all-rejected result stops without a theater pass.
6. Fact/anchor findings are live-verified before edits, overlapping edits are composed, consumers are re-read, and unverifiable claims become Risks / decisions.
7. Settled-target findings take contradiction precedence, including verified facts/unavailable premises and ticket decisions under `--no-grill`. Verify evidence first. Test grouped overlapping answers, indented multiline replacements, specific conflict messages, unknown ids, mixed abort/item replies, sole-line abort and retained valid answers; never infer keep/replace/reopen.
8. Changing tier, revising an interview answer, and adding a decision under `--no-grill` follow Design 6's invalidation rules and re-enter Phase 3 when required.
9. Every written brief has exactly one `## Doubt pass` section; every skip has a normalized reason; completed records contain counts but no raw reviewer prose or model/vendor name.
10. The skill still promises and performs no filesystem write before final confirmation.
11. `skills/grilling/SKILL.md` is unchanged, and no proof ladder, sandboxed run, same-model fallback, or vendor tool enters the diff.
12. README, AGENTS, and the workflow reference agree with the skill on phase order, tier behavior, and the two-cycle cap.
13. Portability lint accepts the unchanged `requires` block and the full stdlib test suite passes.
14. A Problem fold and Done-when replacement survive display, cycle 2 and exact-preview write. Revise an unrelated Q: Q-linked keep/replace amends Settled; a Q-linked reopen leaves Settled and appears once Open with `deferred`; Q-less resolutions remain in the candidate and reach the re-passed `seed` as labelled operator-settled constraints, never as Facts established, without grammar extensions. Test dependent-Q resume arithmetic, preserved unrelated folds, returned-decision conflicts routed through Decision 8 before Phase 3 (also small), refreshed Interview metadata/new facts in References and Scope, and written-candidate BRIEF WRITTEN counts. No-grill Add a decision preserves corrections.
15. Native/skill/shell eligibility accepts self-stated family/provider in instructions, config or runtime, not inference from tool names; unknown/same-family/write-capable-only or inseparable-final-response candidates fail. Test the content-free pre-interview probe, configured/documented default preference, operator tie choice, per-dispatch missing/mismatched identity, and per-candidate first-failed-check console diagnostics. Prompts carry wiki/seed context, fixed cap and narrowed contract.
16. Read readable findings with missing fields, duplicate ids or inconsistent counts/status and explicit clean statements leniently; strip one whole-response fence and ignore trailing transport output. With `--questions 1`, retain 7 blocks and cut/count excess without failure. Send prompts via stdin/argv with no files. Test empty/host-error/unreadable failures, longest-timeout/waitable-background selection, printed timeout bound, identity failure, one retry per cycle, cycle-1 skip, cycle-2 at-cap/irreversible Accept or Abort, and invalid replies.
17. Two-cycle counts deduplicate repeated roots and count reopen as resolved plus its new open item; Result never collides with the ticket Status label. Renumber only spec-brief references; the per-tier tables and summaries match.
18. Tier findings appear as advisory evidence; only Confirm change-tier re-runs the tier gate/policy. Scale findings use Risks or the four existing emission cases, including factor-without-target; contradiction replacements cannot set Tier/Scale.

## Test command

```text
python lint.py --strict
python -m unittest discover -s tests -p "test_*.py"
```

## Done when

- `/spec-brief` runs the cross-model doubt pass or announces that it skipped it, and every written brief records the completed or skipped outcome in `## Doubt pass` (completed records are the flagged spec-level addition in Decision 4).
- A finding that contradicts a settled decision reaches the operator in a separate pre-Confirm reconciliation prompt; the skill never folds it alone.
- An `irreversible` brief is never written unless a cross-model cycle completed; initial no-eligible-reviewer halt precedes interview, and failed dispatch cannot skip (Decision 12 permits accepting reconciled cycle 1 at cap).
- `python lint.py --strict` and `python -m unittest discover -s tests -p "test_*.py"` pass.

## Out of scope

- The proof ladder and its Write gate (VHS-67).
- A sandboxed run in `grilling` (VHS-66); `skills/grilling/SKILL.md` remains unchanged.
- Shipping a `codex` skill, naming any vendor's tool in the skill, or adding a vendor/model lookup table.
- A same-model fallback when no different-family reviewer is eligible.
- A new reviewer agent file, persistent doubt-review report, script, test module, or capability key.
- Changes to `/spec-cycle`, `/ship-spec`, `/spec-close`, `/spec-tickets`, reviewer agents, `lint.py`, `sync.py`, or any `VHS-41.*` path.

## Deferred (P2+)

- round-1 correctness/F-4 + edge-cases/F-3; cross-model-claude correctness/F-6; round-4 edge-cases/F-1; cross-model-claude-2 correctness/F-8; round-5 correctness/F-2 + edge-cases/F-1; round-6 correctness/F-1 + edge-cases/F-1 + conventions/F-1 — Canonical-ticket grounding was blocked by earlier `skills` namespace denial and this invocation's network outage; these process notes propose no spec fix, so the brief remains the narrowed contract without speculative scope edits.
- round-1 edge-cases/F-4 — A maximum length for the operator's free-text `big` skip reason is an optional audit-size improvement; the required contract only pins non-empty, recorded reasoning.
- cross-model-claude edge-cases/F-4 (snapshot suggestion only) — Read-only eligibility is folded; before/after git-status snapshots add detection that cannot prevent a forbidden write and can confuse unrelated concurrent edits, so no additional mutation-detection machinery is specified.
- cross-model-claude-2 edge-cases/F-3 (optional retry failover only) — The timeout fix is folded; selecting a different retry mechanism adds eligibility machinery beyond the decided single-mechanism retry.
- round-5 conventions/F-2 — Updated flagged additions are surfaced in the final human drift checklist; this advisory asks for no design change.
