# Conventions Review — round 4

> Cross-model round (Claude reviewer agents) over the round-3 green spec, run outside the `/spec-cycle` loop on 2026-10-13. Persisted by hand from the agent's hand-back text; not a `round-<C>/` directory.

## Closure of round 3 findings
N/A — no closure predecessor. No closure manifest was passed, and this is the first pass of a full invocation.

Grounding: I read the spec, the brief, `AGENTS.md` (the gitignored `CLAUDE.md` points to it), `docs/authoring-portable-skills.md`, `skills/spec-brief/SKILL.md` and `docs/spec-workflow-reference.md`. From the wiki I read `projects/vigil-skills/state.md`, `filemap.md` and the distillation overview. The wiki has no `architecture.md` for this project. Decisions read: VHS-55 (stakes tier), VHS-46 (ship-spec review gate), VHS-36 (operator claims), PET-184 (cross-model checkpoint) and the CROSS Codex review gate. I checked every `path:line` anchor in the spec against the live files and all of them resolve: `lint.py:44` is the comment above `REQUIRES_KEYS`, which is fine. The spec has no `## Deferred — follow-up required` section, so the deferred-findings checks do not apply.

## Findings

### F-1: The "host cannot wait" branch can never run, and VHS-55 already recorded why
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3 (spec.md:43-51); § Decision 4 reason list (spec.md:76); § Design 1 `can_wait` (spec.md:167); § Design 7 failure modes (spec.md:222); § Done when (spec.md:264)
**Convention violated:** wiki decision `2026-10-11-vhs-55-ceremony-follows-an-operator-set-stakes-tier.md` §1, plus the live tier gate.
**Evidence:** The tier gate runs in every mode before the interview: `If the host cannot wait, print tier needs an operator — stopping and stop. Write nothing.` (`skills/spec-brief/SKILL.md:94`). VHS-55 §1 says: "`/spec-brief` already has mandatory operator waits (Confirm), so a headless path through it does not exist; a default would only hide the stop." Phase 3 is therefore only reached on a host that can wait. Even so, the spec adds:
- a `can_wait` state variable;
- a normalized reason `host cannot wait` and the `big` branch that records it;
- a separate wait test for `irreversible`;
- a failure-mode bullet;
- a "no-wait" clause in Done when.

None of these can run. They are ceremony, and they suggest headless runs reach Phase 3, which contradicts the recorded decision.
**Suggested fix:** Replace Decision 3's three bullets with one sentence: "Phase 3 is reached only on a host that passed the tier gate's wait test (`skills/spec-brief/SKILL.md:94`), so no wait test is repeated here." This also settles brief Risks 3. Then remove:
- `can_wait`;
- the `host cannot wait` reason;
- the `big` headless branch;
- the `irreversible` wait precondition;
- the failure-mode bullet;
- "no-wait" from Done when.

Brief Decision 6's "a session that cannot wait" stays true, because the tier gate stops first.

### F-2: A second invalid reply throws away the whole interview, unlike the skill's other post-interview prompts
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9 (spec.md:116); § Decision 8 (spec.md:103)
**Convention violated:** the skill's existing rule for invalid replies after the interview (`skills/spec-brief/SKILL.md:180`).
**Evidence:** `SKILL.md:180` says: "On option 4's re-ask, a reply other than `1`–`4` re-prints the tier prompt and does not discard the interview. The first tier-gate ask, before any interview, still stops and writes nothing on any other reply." The skill only stops on an invalid reply before any operator effort has been spent. Decision 9 instead says "a second invalid reply stops and writes nothing", which discards the full interview and the cycle work over a typo. Decision 8's contradiction batch does not say what an invalid reply does at all.
**Suggested fix:** In Decision 9, an unrecognized reply, a bare `2`, or an empty reason re-prints the offer and does not discard the interview. Option 3 is the only way to abort. Give Decision 8's batch the same rule.

### F-3: Every `small` run gains an extra blocking prompt, which blurs the brief's small/big distinction
**Severity:** P2
**Where:** spec § Decision 3, `small` bullet (spec.md:47); § Design 3 (spec.md:182)
**Convention violated:** brief Decision 6 ("`small` skips unless the operator asks. `big` offers it.") and the purpose of the `small` tier in VHS-55 ("Cheapness comes from fewer rounds").
**Evidence:** On any host that can wait (which, per F-1, is every host that reaches this phase) with an eligible reviewer, the spec's `small` path "offers one immediate override: run the pass or keep the skip". That is an offer and an extra stop on every `small` brief, which makes `small` behave like `big` minus the reason requirement. The VHS-46 decision's process note warns that "a fix that adds a new stop or menu tends to draw the next finding".
**Suggested fix:** For `small`, announce the skip without waiting. Express "operator asks" as one more Confirm option, shown only under `small` with an eligible reviewer: `5. Run the doubt pass`. That option runs Phase 3 and returns to Confirm. This adds no new stop and keeps the brief's distinction.

### F-4: The per-tier ceremony tables are not updated
**Severity:** P2
**Where:** spec § Design 8 (spec.md:229-233); Scope rows for `docs/spec-workflow-reference.md` and `AGENTS.md`
**Convention violated:** single source of truth for "what changes per tier" (VHS-55; `docs/spec-workflow-reference.md` § Stakes tier; `AGENTS.md:35`).
**Evidence:** The reference's Stakes tier table (`docs/spec-workflow-reference.md:147-152`) and the AGENTS "**Stakes tier.**" paragraph (`AGENTS.md:35`) list everything each tier changes. After this spec:
- `small` also skips the doubt pass by default;
- `irreversible` also requires a successful cross-model pass and halts without one.

Design 8 only names `AGENTS.md:25` and the reference's phase prose, so both tables become incomplete. These are the places a reader checks to learn what `irreversible` costs.
**Suggested fix:** Design 8 should name both surfaces:
- `small` row: "spec-brief records a doubt-pass skip unless the operator asks."
- `irreversible` row: "spec-brief halts with nothing written unless the cross-model doubt pass completes."

Add the same two clauses to `AGENTS.md:35`.

### F-5: No stated way for a host whose own subagents cannot switch model family to reach eligibility
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5 (spec.md:78-82); § Decision 6 (spec.md:84-86); § Design 8 README requirement (spec.md:233)
**Convention violated:** portability habits 1 and 3 (`docs/authoring-portable-skills.md:9`, `:20`): lead with intent, and give harness examples only as tagged parentheticals.
**Evidence:** The harness `README.md:63` names, Claude Code, can only give its native subagents same-family models. The operator's real practice (brief § Problem; the distillation's "using the existing codex skill") is a cross-model CLI or skill that the operator installed. The spec does three things that, together, leave that practice without a conforming route:
- it says the skill "asks the host for a fresh subagent";
- it forbids naming a vendor's tool;
- it says "unknown identity means no eligible reviewer".

As written, the pass will usually record `no eligible cross-model reviewer` on the primary harness, and every `irreversible` brief will halt there. It is also unstated whether a CLI-driven reviewer relies on the existing `shell` capability or on `subagents`; Decision 6 says the dispatch uses `subagents`.
**Suggested fix:** Add one host-neutral sentence to Decision 5: "Any fresh-context dispatch mechanism available in the session counts, whether a native subagent, an installed skill, or a command-line reviewer, when it declares the model family it runs. Prefer one whose sandbox enforces read-only, and always give the Phase 1 no-mutation instruction." In Decision 6, say that a CLI-driven dispatch falls under the already-declared `shell: true`. The rule against naming a vendor stays.

### F-6: Additions the brief does not ask for, presented without flagging them as additions
**Severity:** P2
**Where:** spec § Design 6 (spec.md:205); § Decision 4 (spec.md:57-65); § Done when (spec.md:262); § Decision 9 (spec.md:113); § Decision 12 / Design 6 (spec.md:157, :211)
**Convention violated:** the rule against silent additions to the brief. These are class (d): positions the brief and ticket do not authorize, and the spec does not mark them as additions.
**Evidence:**
- (i) Confirm now "previews the full final candidate". The brief's Scope row only says the preview "also shows the doubt pass's outcome", and the current preview (`SKILL.md:168`) shows only Decisions, Risks, tier and basis. This changes Confirm on every run.
- (ii) The brief asks only that "a skip is recorded in the brief" (Decision 1, Done when, Risks 4). The spec records completed passes too, with four counts, and strengthens its own Done when to "every written brief records the completed or skipped outcome".
- (iii) The `big` offer adds a third option, Abort.
- (iv) A `completed with cycle-2 failure` status, a `dispatch_failed` flag, and restart rules when the tier is raised to `irreversible`.
**Suggested fix:** Either drop (i) and keep the current preview plus the one summary line, or mark each item as a spec-level addition with a one-line rationale. Bring Done when back to the brief's wording unless (ii) is kept on purpose. See F-7 for (iv).

### F-7: The cycle-2 failure handling can collapse into the existing `completed at cap` status
**Severity:** P3
**Where:** spec § Decision 12, paragraph 2 (spec.md:157); § Design 6, paragraph 1 (spec.md:211); Test plan row 4
**Convention violated:** the VHS-46 lesson that removing added machinery is what closed the review churn.
**Evidence:** `completed at cap` already tells the operator that the last edit was not re-reviewed. A cycle-2 dispatch failure tells them the same thing about the cycle-1 edits. The separate status, the in-memory flag, and the two restart paragraphs (with their mirrored test row) exist only to tell those two apart.
**Suggested fix:** Use one rule for every failed dispatch in any cycle: `small`/`big` record the furthest completed state (`completed at cap` with `Cycles: 1`), and `irreversible` stops. When the tier is raised to `irreversible`, rerun Phase 3 only when the record is a skip. If the operator wants the stricter split, keep it, but say why the `completed at cap` disclosure is not enough.

### F-8: The reviewer prompt carries no wiki path but tells the reviewer it may open wiki files
**Severity:** P3
**Where:** spec § Design 4 (spec.md:186-195)
**Convention violated:** the repo's reviewer-dispatch pattern, where `/spec-cycle` passes `wiki_root` and `project_slug` to the reviewers that read the wiki.
**Evidence:** The prompt list "contains only" `draft_brief`, `ticket_contract`, `project_root`, `cycle_number`, the schema and the instructions. Then: "It may open repository and wiki files for evidence." Without `wiki_root`, the reviewer cannot find the wiki.
**Suggested fix:** Add "`wiki_root` and `project_slug` when Phase 0 resolved them" to the prompt list.

### F-9: The doubt-pass `**Status:**` label repeats the brief header's `**Status:**` label
**Severity:** P4
**Where:** spec § Decision 4 (spec.md:62, :72)
**Convention violated:** the brief template's header `**Status:** … · **Priority:** …` (`SKILL.md:192`).
**Evidence:** Each brief would then have two `**Status:**` lines with different meanings: ticket status and doubt-pass status. No parser reads either today.
**Suggested fix:** Rename the field to `**Result:**`, or `**Outcome:**`, merging it with the existing Outcome line.

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 2 | P4: 1

STATUS: GREEN
