# VHS-56 — spec-brief: cross-model doubt pass on the brief
**Status:** Todo · **Priority:** high · **Assignee:** unassigned
**Created:** 2026-10-13 · **Plane:** VHS-56 (85bfe38a-8ecf-4f71-840e-6fb81dc8b006, Todo)
**Origin:** Filed 2026-10-11 from the skill-pack distillation (`vigil-harbor-wiki/overview/2026-10-11-skill-pack-distillation.md` §3 item 4, sprint plan §6 Wave 2). The idea comes from Osmani's doubt-driven-development skill. The ticket as filed held three changes. A cross-model review of the first draft of this brief recommended a split, and the operator split it on 2026-10-13: VHS-56 keeps the doubt pass, VHS-66 takes the sandboxed run in `grilling`, and VHS-67 takes the proof ladder and its Write gate. The Plane text of VHS-56 still describes all three; this brief is the narrowed contract.

## Problem

The brief is the one lifecycle artifact nothing challenges. Every reviewer lens is downstream of it and treats it as axiomatic. In 13 sessions since 2026-09-30 the operator bolted on a Codex or Astra brief review by hand ("write the brief, then call codex to review the brief before we hand it off to spec-cycle", 32db23c8 10-10; "call codex to review the brief until you have wrinkles ironed out", 65c6bd2b 10-08). Those reviews usually came back RED or NOT READY and changed decisions the interview had settled.

The operator asked whether the review belongs before or after grilling (879fadea 09-30); it was unanswered until this brief's interview (Decision 3).

## Why it matters

A false premise or a wrong decision in the brief is invisible to `/spec-cycle`: every lens treats the brief as authority. The review that catches them already happens, but by hand, and only when the operator remembers to ask. This brief is its own example: one hand-run Codex pass over its first draft returned NOT READY with two P0 findings, and all six of its findings held when checked against the files.

## Scope (verified against current files, 2026-10-13)

| Path | Current | Change |
|---|---|---|
| `skills/spec-brief/SKILL.md` | Phase 2 Interview (`:160`) leads straight to Phase 3 Confirm (`:166`), then Phase 4 Write (`:186`). Nothing reviews the brief. | A doubt pass between the interview and Confirm (Decisions 1 to 3), with its finding rules (Decision 4), reviewer rule (Decision 5) and tier rule (Decision 6). |
| `skills/spec-brief/SKILL.md` | Phase 3's preview (`:168`) shows the Decisions list, the Risks list, the tier and its basis line. | The preview also shows the doubt pass's outcome: what was folded, or that the pass was skipped and why (Decisions 1 and 4). |
| `skills/spec-brief/SKILL.md` | The Phase 4 template (`:191-206`) has no place for a skip record. | The brief records a skipped pass and its reason (Decision 1). Where is Risks 4. |
| `skills/spec-brief/SKILL.md` | `## What /spec-brief never does` (`:254`), `## Tool-use notes` (`:258-265`) and `## Failure modes` (`:267`) describe a skill whose only dispatches are read-restricted exploration and `grilling`. The `requires:` block (`:5-10`) already declares `shell`, `network` and `subagents`. | Updated to cover the reviewer dispatch. No new capability key is expected (Risks 6). |
| `docs/spec-workflow-reference.md` | Describes spec-brief at `:7` to `:21`. | Mirrors the shipped contract. |
| `README.md`, `AGENTS.md` | One-paragraph summaries of `/spec-brief` at `README.md:9` and `AGENTS.md:25`. | Short mirror, only where a line would otherwise be wrong. |

## Decisions carried forward

Decisions 1 and 2 are the ticket's own text. Decisions 3 to 6 were settled by the operator in a one-round interview on 2026-10-13.

1. **spec-brief runs the doubt pass or says that it skipped it.** Ticket done-when: "spec-brief runs or announces-skips the doubt pass". A silent skip is not allowed, and a skip is recorded in the brief.
2. **The doubt pass is cross-model.** Ticket title: "cross-model doubt pass on the brief".
3. **The pass sits after the interview and before Confirm (Q2).** The operator confirms once, with the findings already in the preview. Why: a pass after Confirm would reopen decisions the operator had just approved.
4. **A finding about a fact or an anchor is folded; a finding that contradicts a settled decision goes to the operator (Q3).** The skill does not change a settled decision on a reviewer's word. The operator sees the finding and re-evaluates. Why: decisions are the operator's (`skills/grilling/SKILL.md:61`).
5. **The reviewer is named in host-neutral words, and no second model means an announced skip (Q4).** The skill asks for a model from a different family. It does not name a vendor's tool. Where the host has none, the skill announces the skip and records it. Why: this repo is public and does not ship the `codex` skill; a same-model pass was rejected because two tickets in a row showed a same-model green does not hold.
6. **The tier sets whether the pass runs (Q5).** `small` skips unless the operator asks. `big` offers it. `irreversible` cannot skip: where the pass cannot run (no second model, or a session that cannot wait for the operator), the skill stops and writes nothing. Why: a stop is cheap, and "cannot skip" stays true.

## Done when

- spec-brief runs the doubt pass or announces that it skipped it, and a skip is recorded in the brief.
- A finding that contradicts a settled decision reaches the operator before Confirm; the skill does not fold it alone.
- An `irreversible` brief is never written without the pass.
- Lint and tests pass.

The ticket's other done-when items moved with the split: "grilling's Fact-finding section allows a sandboxed run" to VHS-66, and the proof-level items to VHS-67.

## Out of scope

- The proof ladder and its Write gate. VHS-67.
- The sandboxed run in `grilling`. VHS-66. This brief changes nothing in `skills/grilling/SKILL.md`.
- Shipping the `codex` skill in this repo, or naming any vendor's tool in the skill (Q4).
- A same-model fallback when no second model is available (Q4).

## Tier

**Level:** big

## Risks / decisions

1. What the reviewer receives. The ticket proposes "the brief and the ticket text only", and its source rule is "a fresh-context reviewer gets the artifact and the contract, never the claim". The pass now runs before Confirm, so no brief file exists yet; spec-brief may write only the brief and its `.tmp` (`skills/spec-brief/SKILL.md:254`). How the draft is handed over is open. Spec author pins this.
2. The cycle bound. The ticket proposes "at most two cycles"; its source uses three cycles then escalates, and treats two cycles with findings but nothing actionable as "doubt theater". Spec author pins this.
3. Interactive versus headless. The ticket proposes "Offered in interactive sessions, announced-skipped headless". How the skill tells the two apart is not stated; the only existing wording is "If the host cannot wait" at `skills/spec-brief/SKILL.md:94`. Spec author pins this.
4. The skip record. Which section of the brief holds a skip and its reason, and whether an operator's skip and a no-second-model skip are recorded the same way. `/spec-cycle` parses three of the brief's headers, so a new line must not break that parse. Spec author pins this.
5. How the skill knows a model is from a different family, and what it does when it cannot tell. Spec author pins this.
6. Whether the reviewer dispatch fits the capabilities spec-brief already declares (`:5-10`: `shell`, `filesystem`, `network`, `subagents`, two optional services). `lint.py:45` fixes the vocabulary to five keys. Spec author pins this.
7. Checking a finding before it is folded. A reviewer's output is model output. Whether a fact or anchor finding must be checked against the files before the fold (the VHS-26 rule for reviewer-supplied facts) is not stated. Spec author pins this.
8. Which findings count as "contradicts a settled decision" (Decision 4), and how the question is put to the operator: inside the Confirm preview, or as its own prompt. Under `--no-grill` there are no interview-settled decisions, only those the ticket states. Spec author pins this.
9. A `big` brief where the operator declines the offered pass. Decision 1 says the skip is recorded; whether a reason is required is open. Spec author pins this.
10. The reconcile order. The source sorts findings as contract misread, actionable, trade-off, noise. Whether the skill adopts that order is open. Spec author pins this.

## References

- Plane VHS-56 (ticket text, read 2026-10-13 through the tracker). Split tickets filed 2026-10-13: VHS-66 (sandboxed run), VHS-67 (proof ladder; also takes the absorbed VHS-39).
- `vigil-harbor-wiki/overview/2026-10-11-skill-pack-distillation.md:45` (the proposal), `:67` (before or after grilling), `:100` (Wave 2 item, tier big).
- `skills/spec-brief/SKILL.md:5-10` (requires), `:94` ("cannot wait"), `:160` (Phase 2), `:166` and `:168` (Phase 3 and its preview), `:186` (Phase 4), `:191-206` (template), `:254`, `:258-265`, `:267`.
- `skills/grilling/SKILL.md:61` (decisions are the operator's).
- `lint.py:45` (the closed `requires:` vocabulary).
- `docs/spec-workflow-reference.md:7`, `:21`; `README.md:9`; `AGENTS.md:25`.
- No `skills/codex/` in this repo (directory listing, 2026-10-13); `sync.py:29-30` mirrors only `skills/` and `agents/`.
- Source skill named by the ticket, not read: `skills/doubt-driven-development/SKILL.md` in addyosmani/agent-skills.
- Cross-model review of the first draft: Codex `gpt-5.6-sol`, read-only sandbox, 2026-10-13, one cycle, NOT READY (2 P0, 2 P1, 2 P2). Its split recommendation was adopted (see Origin); its other findings concerned the parts now in VHS-66 and VHS-67, and are carried in those tickets.
- Interview: 1 rounds, exit empty-frontier. Seven questions settled; Q6 (does "walked" block Write) and Q7 (how the sandboxed run happens) are recorded in VHS-67 and VHS-66.
