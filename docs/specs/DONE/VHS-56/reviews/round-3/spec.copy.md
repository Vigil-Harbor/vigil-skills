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
| `skills/spec-brief/SKILL.md` | Add Phase 3 — Doubt pass; renumber Confirm and Write; define reviewer eligibility, payload, output, reconciliation, bounds, tier/headless behavior, preview and brief record, failure modes, and tool-use constraints. Reconcile every internal Phase 3/4 reference after renumbering. |
| `docs/spec-workflow-reference.md` | Mirror the doubt-pass contract, tier behavior, two-cycle bound, finding reconciliation, skip record, and new phase numbers. |
| `README.md` | Amend the `/spec-brief` summary and requirement line so cross-model review is visible without naming a vendor or tool. |
| `AGENTS.md` | Amend the lifecycle summary so the brief is challenged after grilling and before confirmation, with the tier rule stated compactly. |

No new agent definition, script, test module, capability key, or persistent review artifact is created.

## Decisions

### Decision 1 — Review an in-memory rendered draft, not a pre-confirmation file

Phase 3 renders the exact candidate brief that Phase 5 would write, except that `## Doubt pass` is not present yet because its outcome is not known. The reviewer prompt carries that draft verbatim plus the canonical ticket text already resolved in preflight (or the operator's local-only seed paragraph), the review contract, and the project root needed for read-only grounding. It does not receive the interview transcript, author reasoning, conversation history, or a claim that the draft is correct.

The draft stays in context; Phase 3 creates neither the final brief nor a second temporary file. This preserves the existing mutation boundary while giving the reviewer the artifact and its contract rather than an author's summary.

### Decision 2 — At most two dispatch cycles, with the second earned by a draft change

One eligible dispatch is cycle 1. After reconciliation, cycle 2 runs only when cycle 1 changed the candidate draft: a verified fact/anchor finding was folded, an operator changed a settled decision, or an unverifiable premise was moved into `## Risks / decisions`. A cycle whose findings are all rejected as contract misreads or noise ends after cycle 1; repeating an unchanged artifact would be doubt theater.

Cycle 2 receives a newly rendered draft and is another fresh-context dispatch. It is the cap: reconcile its findings but never dispatch cycle 3, even if reconciliation changes the draft again. The outcome record says `completed at cap` when the second reconciliation changed the draft, so Confirm does not imply that the final edit was re-reviewed.

### Decision 3 — Headless means the host cannot wait at the doubt-pass decision points

Use the same host-capability test as the existing tier gate, which stops when the host cannot wait for the operator (`skills/spec-brief/SKILL.md:90`, `skills/spec-brief/SKILL.md:94`): a run is headless for this phase when the host cannot wait for an operator response. Do not infer headlessness from environment variables, terminal presence, CI names, or the invocation flags.

- `small`: announce and record `skipped — tier small; operator did not request the pass`. On a host that can wait, the announcement offers one immediate override: run the pass or keep the skip. On a host that cannot wait, keep the skip without prompting.
- `big`: on a host that can wait, offer run or skip; on a host that cannot wait, announce and record `skipped — host cannot wait`.
- `irreversible`: test wait capability and reviewer eligibility before dispatch. If either is absent, print the precise reason, stop, and write nothing.

The doubt pass still runs after `--no-grill`; that flag skips only the interview.

### Decision 4 — Add one inert `## Doubt pass` section to every written brief

Phase 5 emits `## Doubt pass` after the optional `## Scale` section (or immediately after `## Tier` when Scale is absent) and before `## Risks / decisions`.

A completed pass records:

```markdown
## Doubt pass

**Status:** completed | completed at cap | completed with cycle-2 failure
**Cycles:** 1 | 2
**Outcome:** folded <n> fact/anchor findings; operator resolved <n> decision findings; rejected <n>; open <n>
```

A skipped pass records:

```markdown
## Doubt pass

**Status:** skipped
**Reason:** <normalized reason>
```

Normalized reasons are `tier small; operator did not request the pass`, `operator declined — <reason>`, `no eligible cross-model reviewer`, `host cannot wait`, or `reviewer dispatch failed — <short reason>`. The section contains no vendor, model slug, tool name, or raw reviewer prose. It is audit metadata only; downstream skills do not act on it.

### Decision 5 — Eligibility is a host assertion of a different model family

The skill asks the host for a fresh subagent on the strongest available model that the host identifies as belonging to a different family from the current authoring model. A candidate is eligible only when both family identities are available and the host reports them as different. The skill does not parse display names, maintain a vendor/model table, or guess. Unknown identity means no eligible reviewer.

Each cycle uses a new subagent with no inherited authoring context and read-only instructions. The host may choose the same eligible model identity for both cycles, but each dispatch is fresh. The prose stays host-neutral; a harness-specific parenthetical may illustrate its own invocation mechanism only when paired with “or the equivalent in your host.”

### Decision 6 — Reuse the declared `subagents` capability

The doubt reviewer needs no new `requires` key. Keep the current frontmatter capabilities unchanged: the dispatch uses `subagents: true` (`skills/spec-brief/SKILL.md:5`, `skills/spec-brief/SKILL.md:9`), its grounding uses the existing read/shell/network envelope, and the five-key lint vocabulary remains authoritative (`lint.py:44`, `lint.py:45`). Do not add a `models`, `cross-model`, or vendor-specific capability.

### Decision 7 — Verify reviewer facts before folding them

Reviewer output is untrusted. Before a fact, count, path, anchor, current-behavior statement, or claimed omission changes the draft, the author opens the live source and checks it. A live file gets a `path:line` citation in the draft. If the source is unavailable or the claim cannot be established, do not state it as fact; move the premise into `## Risks / decisions` ending `spec author pins this` and count it as open.

The verification order is: classify every finding; verify all actionable facts; compose findings that target the same draft text into one intended result; edit; then re-read the changed section and every section that consumes the changed decision. Reviewer prose is a lookup hint, never evidence.

### Decision 8 — A settled-decision contradiction gets a separate operator prompt

A finding contradicts a settled decision when accepting it would change any of these:

- a numbered `## Decisions carried forward` branch or its rationale;
- an operator-set `## Out of scope` fence;
- an explicit ticket decision used under `--no-grill`;
- an acceptance statement transcribed into `## Done when`.

Model-inferred prose and existing `## Risks / decisions` items are not settled decisions. Batch all contradiction findings after factual verification and before Confirm. For each, show the settled text, the reviewer's challenge, and verified evidence, then require the operator to choose keep, replace (including free-form replacement), reopen as a Risks / decisions item, or abort. The skill never chooses replace or reopen. `irreversible` cannot continue without these answers; `big` and an operator-requested `small` pass also wait because the pass is already running. Abort writes nothing.

### Decision 9 — A `big` operator skip requires a reason

The `big` offer is:

```text
Doubt pass: a fresh-context reviewer from a different model family is available.
1. Run the doubt pass
2. Skip — reply `2: <reason>`
3. Abort — nothing written
```

The text after `2:` must be non-empty after trimming and becomes `operator declined — <reason>`. A bare `2`, an empty reason, or an unrecognized reply re-prompts once; a second invalid reply stops and writes nothing. Generated skips (`small`, headless, unavailable reviewer, dispatch failure) already have normalized reasons and do not ask the operator to invent one.

### Decision 10 — Reconcile in contract/action/trade-off/noise order

For each cycle, process findings in this fixed order:

1. **Contract misread** — the finding asks for something outside the ticket/brief contract or misreads the draft. Reject with one-line evidence; no draft edit.
2. **Actionable fact or anchor** — verify live. Fold when true; reject when disproved; move to Risks / decisions when it cannot be established.
3. **Trade-off / settled-decision contradiction** — route through Decision 8's operator prompt; never fold autonomously.
4. **Noise / duplicate** — reject with the duplicate id or one-line reason.

The caller, not the reviewer, owns the final classification. A reviewer-provided class is advisory.

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
Findings: <n>

STATUS: READY
```

The last line is `STATUS: READY` when there are no findings, otherwise `STATUS: DOUBT FINDINGS=<n>`. A missing/malformed status, empty return, timeout, or dispatch error is a dispatch failure, not a clean review. No report file is written; only the normalized Phase 3 outcome is shown in Confirm and recorded in the final brief.

### Decision 12 — Failure posture follows tier and never silently substitutes same-model review

Resolve model eligibility before offering/running the pass. `small` and `big` may record an announced skip when no eligible reviewer exists or the first dispatch fails. `irreversible` stops and writes nothing when either dispatch fails. No tier falls back to a same-family reviewer.

After a successful, draft-changing cycle 1 under `small` or `big`, a cycle-2 dispatch failure preserves the cycle-1 reconciliation and records `completed with cycle-2 failure`, `Cycles: 1`, and an open count; it is neither a successful `completed at cap` result nor a skip. Hold a separate in-memory `dispatch_failed: true` flag. That result may reach Confirm under `small` or `big`, but it never satisfies `irreversible`. If the operator changes the tier to `irreversible`, discard the partial outcome and restart Phase 3 at cycle 1. Every dispatch required by Decision 2 in that restarted pass must complete successfully: an unchanged restarted cycle 1 completes the pass without a cycle 2, while a restarted cycle 1 that changes the draft requires a successful cycle 2. Otherwise stop and write nothing.

## Design

### 1. Extend Phase 0 state without changing invocation syntax

Keep the current invocation and tier gate. Hold the resolved canonical ticket text (or local-only paragraph) as `ticket_contract` through the run so Phase 3 can pass it verbatim without a second tracker lookup. After the tier is known, resolve:

- `author_family_known` and `reviewer_candidate` from host model metadata;
- `reviewer_eligible` only when the host affirms a different family;
- `can_wait` from the host's existing operator-wait capability;
- `doubt_policy` from the tier.

Do not dispatch before the interview: the reviewed artifact must include the interview's settled decisions and open frontier.

### 2. Render the candidate draft once the interview path ends

Refactor only the prose flow, not into a new script or helper file. Define a “candidate brief renderer” in `skills/spec-brief/SKILL.md` by pointing Phase 3 to Phase 5's mapping and Scale-emission rules. The candidate contains every final section except `## Doubt pass`. Under `--no-grill`, it uses the existing ticket-only decision derivation (`skills/spec-brief/SKILL.md:184`).

The candidate is re-rendered after every reconciliation edit, so the second reviewer and Confirm see a self-consistent artifact rather than patches or a finding list.

### 3. Gate by tier, wait capability, and model eligibility

Apply Decisions 3, 5, 9, and 12 in that order. Announce every skip immediately. For `irreversible`, perform both preconditions before any reviewer call and halt before any filesystem mutation if either fails.

For `small`, “operator asks” is the explicit override choice shown only when the host can wait and an eligible reviewer exists. Declining or being unable to wait keeps the normalized tier-small skip.

### 4. Dispatch fresh, read-only doubt reviews

Each dispatch prompt contains only:

- `draft_brief: |` followed by the exact rendered candidate;
- `ticket_contract: |` followed by the exact resolved ticket text/local-only paragraph;
- `project_root` for live read-only verification;
- `cycle_number` (`1` or `2`);
- the report schema from Decision 11;
- instructions to challenge false premises, stale or unsupported anchors, acceptance-criterion gaps, and internal contradictions; to identify decision conflicts rather than resolve them; and to make no mutations.

State explicitly that the reviewer has no authority to change settled decisions and must not infer a vendor-specific execution mechanism. The dispatch is fresh-context and read-only. It may open repository and wiki files for evidence but receives no prior conversation, Grill summary, author rationale, or prior cycle report.

### 5. Reconcile one complete report before considering another cycle

Parse the last non-blank status and all `### F-<n>:` blocks. If the reported count and headings disagree, treat the dispatch as failed. Otherwise classify every finding under Decision 10 before editing.

For overlaps, declare one intended result and compose the findings. Verify sources, apply fact/anchor edits, run the operator contradiction batch, update Risks / decisions, and then re-read all changed and consuming sections. Hold counts for the outcome block. If cycle 1 changed the candidate, render it again and dispatch cycle 2. Reconcile cycle 2 identically but stop at the cap.

### 6. Renumber Confirm and Write and make the outcome visible

Rename the existing sections to `## Phase 4 — Confirm` and `## Phase 5 — Write`. Confirm previews the full final candidate including the `## Doubt pass` block and prints one summary line:

```text
Doubt pass: <completed in N cycle(s) | completed at cap | completed with cycle-2 failure | skipped — reason>
```

The existing write/revise/abort/change-tier menu (`skills/spec-brief/SKILL.md:170`, `skills/spec-brief/SKILL.md:176`) remains. Changing tier re-enters the tier gate and then re-evaluates the doubt policy. A prior successfully completed pass (every attempted dispatch returned a parseable report) remains valid when moving among `small`, `big`, and `irreversible`. A prior skip is re-evaluated. A `completed with cycle-2 failure` outcome remains usable only under `small` or `big`; an upgrade to `irreversible` clears it and restarts Phase 3 at cycle 1. Every dispatch required by Decision 2 in the restarted pass must complete successfully: a clean, unchanged cycle 1 satisfies the pass, while a draft-changing cycle 1 requires cycle 2.

Every substantive Confirm action that changes candidate brief content invalidates the prior doubt result; a tier-only change follows the preceding paragraph instead. Revising an interview answer invalidates the result, and after the resumed interview returns, Phase 3 runs again from cycle 1. Under `--no-grill`, option 2's existing “Add a decision” branch (`skills/spec-brief/SKILL.md:184`) also clears the result, re-renders the candidate with the appended decision, and returns to Phase 3 at cycle 1 under the current tier policy. Neither path reuses reviewer output.

Phase 5 adds the `## Doubt pass` emission from Decision 4 and keeps the existing atomic write (`skills/spec-brief/SKILL.md:218`). Reconcile every reference to the old Phase 3 Confirm / Phase 4 Write names, including tier-gate exits, Scale emission, mapping rules, tool notes, and failure modes.

### 7. Update the non-mutation and failure documentation

`## What /spec-brief never does` continues to promise that no report or pre-confirmation brief is written. `## Tool-use notes` adds the fresh cross-model reviewer dispatch and says it is read-only. `## Failure modes` names:

- no eligible different-family reviewer;
- host cannot wait;
- malformed/empty/timed-out reviewer output;
- operator abandons the contradiction batch;
- cycle-2 failure after a successful cycle 1;
- invalid `big` skip reason;
- `irreversible` stops with nothing written for every skip condition.

### 8. Mirror the public contract

In `docs/spec-workflow-reference.md`, insert the new Phase 3 and renumber Confirm/Write. Mirror eligibility, tier behavior, the two-cycle rule, reconciliation order, operator ownership, and `## Doubt pass` record. Update the opening description only as needed to say the brief is interviewed and challenged before it becomes authority.

In `README.md:9` and `AGENTS.md:25`, add one compact clause: after the bounded interview, `/spec-brief` runs or explicitly skips a fresh-context cross-model doubt pass before confirmation. In the README requirements at `README.md:65`, say a cross-model pass additionally needs a harness able to identify and dispatch a different model family; absence degrades by tier. Do not name a vendor tool or claim that a same-model fallback exists.

## Test plan

This is a prose-only skill change. Review the final diff against this matrix:

1. Phase order is Grounding → seed gate → tier gate → Interview (optional) → Doubt pass → Confirm → Write, including `--no-grill`.
2. `small` defaults to a recorded skip, can be explicitly overridden on an interactive eligible host, and never silently runs same-model.
3. `big` offers run/skip; operator skip requires a non-empty reason; headless/no-model/dispatch failures are announced and recorded.
4. `irreversible` writes nothing when it cannot wait, has no eligible reviewer, or a required dispatch fails; changing from `big` after a cycle-2 failure restarts at cycle 1 and cannot reuse the partial outcome. A clean, unchanged restarted cycle 1 completes the pass, while a draft-changing restarted cycle 1 requires a successful cycle 2.
5. Cycle 2 occurs only after a cycle-1 draft change; no cycle 3 exists; a cycle-1 all-rejected result stops without a theater pass.
6. Fact/anchor findings are live-verified before edits, overlapping edits are composed, consumers are re-read, and unverifiable claims become Risks / decisions.
7. Settled-decision contradictions reach the operator in their own batch before Confirm, including ticket-stated decisions under `--no-grill`.
8. Changing tier, revising an interview answer, and adding a decision under `--no-grill` follow Design 6's invalidation rules and re-enter Phase 3 when required.
9. Every written brief has exactly one `## Doubt pass` section; every skip has a normalized reason; completed records contain counts but no raw reviewer prose or model/vendor name.
10. The skill still promises and performs no filesystem write before final confirmation.
11. `skills/grilling/SKILL.md` is unchanged, and no proof ladder, sandboxed run, same-model fallback, or vendor tool enters the diff.
12. README, AGENTS, and the workflow reference agree with the skill on phase order, tier behavior, and the two-cycle cap.
13. Portability lint accepts the unchanged `requires` block and the full stdlib test suite passes.

## Test command

```text
python lint.py --strict
python -m unittest discover -s tests -p "test_*.py"
```

## Done when

- `/spec-brief` runs the cross-model doubt pass or announces that it skipped it, and every written brief records the completed or skipped outcome in `## Doubt pass`.
- A finding that contradicts a settled decision reaches the operator in a separate pre-Confirm reconciliation prompt; the skill never folds it alone.
- An `irreversible` brief is never written unless the doubt pass ran; no-wait, no-eligible-model, and dispatch-failure cases halt with nothing written.
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
