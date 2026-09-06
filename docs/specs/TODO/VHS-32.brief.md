# VHS-32 — `/spec-brief`: a bounded grilling interview upstream of the spec loop

**Status:** Backlog · **Priority:** Medium · **Assignee:** Unassigned
**Created:** 2026-09-06 · **Plane:** VHS-32 (`4f74afce-518e-4313-8105-43553c50693c`, Backlog)
**Origin:** `mattpocock/skills` (read 2026-09-06, `skills/productivity/{grill-me,grilling}`) formalizes an interview loop this repo performs ad hoc. Today the brief is produced by an unbounded "draft the brief" prompt against the ticket plus some poking around; nothing structures the questions, nothing forces forks to be stated as forks, and nothing bounds when the interview stops.

## Problem

**1. The brief is the one lifecycle artifact nothing challenges.**
`/spec-cycle` dispatches three-to-four adversarial lenses, but every one of them is downstream of the brief and treats it as axiomatic. `agents/spec-reviewer-conventions.md` makes this explicit: it classifies each spec decision as *authorized-by-brief* / *authorized-by-ticket* / *spec-addition-with-rationale* / *silent-addition* — the brief is the authority the spec is measured against, never itself measured. `spec-reviewer-correctness` reads the brief in its mandatory grounding step (step 2) to check the spec solves it. A fork left unresolved in the brief is therefore invisible to all four lenses; it surfaces later as a P0/P1 against the *spec*, and costs a full parallel review round to shake out.

**2. Brief authoring is unbounded and unstructured.**
There is no `/spec-brief` skill. `/spec-cycle` Phase 0 step 2 already tolerates the consequence — "**Local-only ticket IDs** … treat the brief as local-only … Create the Plane issue when scope is confirmed" — i.e. the lifecycle documents a brief arriving from nowhere. The quality of that arrival is operator-dependent.

**3. The existing brief format is already a grilling transcript — produced by hand.**
`docs/specs/DONE/VHS-11/brief.md` carries **Decisions carried forward** (6 numbered, each a settled branch: "Never auto-pull", "Post-green polish is bounded and gate-preserving") and **Risks / decisions** (6, several ending "spec author pins this" / "Spec author defines behavior"). That is precisely a resolved design tree plus an explicitly deferred frontier. The artifact shape exists; the process that fills it does not.

**4. `/spec-cycle` 2f dead-ends on a three-way menu.**
`skills/spec-cycle/SKILL.md:467–484` — after 4 red rounds the skill prints remaining P0/P1 titles and offers "1. Patch manually / 2. Ship by hand / 3. Narrow the brief", then "Wait for the user." All three options hand the operator an unstructured problem at the exact moment the design is most tangled and author fatigue is highest (the VHS-27 ticket documents this fatigue directly: "round-3 reports were written retroactively; by round 10 the closure manifest silently dropped a P1 twice").

## Why it matters

- **Cheapest place to resolve a fork is the brief.** A branch settled in the interview costs one question. The same branch settled at spec round 2 costs a parallel 3–4 agent dispatch plus a revision pass; at round 4 it costs the FROZEN/REWRITE protocol (`:434–465`).
- **Fills the only unstaffed lifecycle stage.** `/spec-cycle` → `/ship-spec` → `/spec-close` all exist and are tracked. Brief authoring is the sole hand-rolled step.
- **Reuses one primitive twice.** The same interview serves brief authoring and the 2f halt. Extracting it as a model-invocable primitive (rather than inlining it once) is what makes the second use a single Skill call.
- **Bounded blast radius.** Two new skill directories plus one stub, and one edited section of `skills/spec-cycle/SKILL.md`. Markdown/prompt only — no Python, no new runtime state, no new dependencies. Same profile as VHS-6, VHS-7, VHS-11.

## Scope (verified against current files, 2026-09-06)

| Location | Current | Change |
|---|---|---|
| `skills/grilling/SKILL.md` *(new)* | — | The model-invocable interview primitive. Design-tree / frontier-per-round model; per-round output contract (below); fact-finding dispatch rules; bounding rules; termination and hand-off contract. `requires:` declares `subagents: true`, `filesystem: [read]`. |
| `skills/grill-me/SKILL.md` *(new)* | — | User-invocable stub: `user_invocable: true`, body delegates to the `grilling` primitive. Ad-hoc "grill me on this" with no lifecycle artifact. |
| `skills/spec-brief/SKILL.md` *(new)* | — | `/spec-brief <TICKET-ID>` — resolve ticket (issue-tracker optional, degrade to conversation), ground against repo + wiki, run `grilling` bounded, emit `docs/specs/TODO/<TICKET-ID>.brief.md` in the established section shape. |
| `skills/spec-cycle/SKILL.md` 2f (`:467–484`) | Three-option menu, then "Wait for the user." | Add a fourth option: grill the *named remaining P0/P1 findings only*, then route the resulting decisions through the existing 2e revise path. Round cap stays 4; the grill cannot start a round 5. |
| `AGENTS.md` § "Workflow: spec lifecycle" (`:21–31`) | Three skills listed | Becomes four: `/spec-brief` → `/spec-cycle` → `/ship-spec` → `/spec-close`. |
| `docs/spec-workflow-reference.md` | Opens at "Take a short brief…" | Add a preceding section documenting where the brief comes from and the grilling contract. |
| `README.md` | Skill list | Add the three new skills. |

**Preserved (NOT changed):** the green gate (`total_p0p1 == 0`), the ≤4-round cap, 2e FROZEN/REWRITE, 2g post-green polish, the Phase 3 HARD STOP, the four reviewer agents, `/ship-spec`, `/spec-close`, `states.json`.

## Decisions carried forward

1. **Fact-finding subagents are `Explore`-class and Opus — never `general-purpose`.** `general-purpose` carries the full tool set and inherits the session's permissions; grill fact-finding is read-only by nature and must not be able to write. Opus because these agents' answers become brief decisions (same reasoning as commit `5e6d401`, which pinned the four reviewers to Opus). Claude Code binding: `Agent({subagent_type: "Explore", model: "opus", …})` — the `model` override on the call, since `Explore` is built-in and has no agent file to carry `model:` frontmatter.
2. **That binding is expressed as intent, with the Claude Code form parenthetical.** `docs/portability-contract.md` §2 classes `model` and `allowed-tools` as **Claude-Code-only** ("Adapters may drop or translate them"). The skill body therefore says *"dispatch a read-only exploration agent on the strongest available model (Claude Code: the `Explore` subagent type with an Opus model override) — never a general-purpose agent, which inherits the full session tool set"*, matching the VHS-7 host-agnostic construction. The *prohibition* is portable even where the mechanism is not.
3. **Facts are the agent's job; decisions are the user's.** A frontier question needing a repo/filesystem fact is dispatched, not asked. A running exploration is an unsettled prerequisite: only questions downstream of it wait — the rest of the frontier is asked now.
4. **Forks are stated as forks, with weighed branches.** This is the deliberate divergence from the upstream primitive, which offers only a single recommended answer. Every question that genuinely branches renders each branch with a *For:* / *Against:* line, then a recommendation. Per-round format:

    ```
    ❓ **Q1 — <title>**: <body>

      **A.** <branch> — *For:* <…>  *Against:* <…>
      **B.** <branch> — *For:* <…>  *Against:* <…>

    ➡️ **Recommend B** — <one line of why>
    ```

    Non-branching questions keep the plain `➡️ <recommended answer>` form; a fork table on a question with one real answer is noise. **The recommendation is advisory, never a default that carries by silence** — the operator retains the right to overturn it, and a round is not settled until they answer. The primitive must not proceed on an unanswered question by taking its own recommendation.
5. **Ask the whole frontier in one round, then wait.** A question whose answer depends on another question open in the same round belongs to a later round. No drip-feed of one question at a time.
6. **The interview is bounded three ways** (the point of the ticket — the current process has no stop condition):
   - **Round cap**, default 3. Configurable per invocation.
   - **Per-round question cap**, default 7. Overflow moves to the next round by frontier depth.
   - **Altitude fence:** only decisions that change the brief's *Scope*, *Decisions carried forward*, or *Out of scope*. Implementation detail is the spec's job, and asking about it here duplicates `/spec-cycle`.
7. **Hitting the cap is a documented outcome, not a failure.** Unresolved frontier branches are written into the brief's `## Risks / decisions` as open items ending "spec author pins this" — the convention VHS-11 already uses. The interview never blocks the brief from being written.
8. **The 2f grill is scoped to the named findings, and cannot patch.** It interviews only the remaining P0/P1 titles the halt already printed — not the whole design. It produces decisions; applying them runs through the existing 2e revise path. It never re-dispatches reviewers and never increments the round counter.
9. **Grilling is never auto-invoked.** `/spec-brief` runs it by contract; `/spec-cycle` 2f offers it as a menu choice. Nothing else fires it unprompted, and `/spec-brief` accepts a flag to skip it for a brief the operator already has settled.
10. **Clean-room, not a port.** `mattpocock/skills` is MIT but this repo is public and its own thing; the upstream text is behavioral reference only, same posture as VHS-28's treatment of the vendor handoff skill. The design-tree/frontier idea is attributed in the brief and the spec, not copied.

## Done when

- `skills/grilling/SKILL.md` exists, model-invocable, carrying: design-tree/frontier model, the one-round-per-frontier rule, the fork output contract of D4, the `Explore`/Opus/never-general-purpose dispatch rule of D1–D2, and the three bounds of D6.
- `skills/grill-me/SKILL.md` exists, `user_invocable: true`, delegating to `grilling`.
- `skills/spec-brief/SKILL.md` exists and `/spec-brief <TICKET-ID>` produces `docs/specs/TODO/<TICKET-ID>.brief.md` with the established sections (Problem / Why it matters / Scope / Decisions carried forward / Done when / Out of scope / Risks / References), the settled tree landing in *Decisions carried forward* and the unresolved frontier in *Risks / decisions*.
- `/spec-brief` degrades to conversation-only when the issue-tracker service is absent (`services: [issue-tracker?]`), consistent with the portability contract's optional-service rule.
- `skills/spec-cycle/SKILL.md` 2f offers the fourth option; the surrounding text states that the grill cannot re-dispatch reviewers, cannot increment the round counter, and routes through 2e.
- The 2f grill persists its outcome to `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md` so `/spec-close` reconciliation can see why the spec changed after the halt.
- All three new `SKILL.md` files carry a valid `requires:` block; `python lint.py --strict` reports zero ERROR and no new `missing-requires` WARN.
- No bare harness tool name appears as an operative imperative in any new file (lint `operative-tool-call` clean); the `Explore` / Opus binding appears only inside a parenthetical per D2.
- `AGENTS.md`, `docs/spec-workflow-reference.md`, and `README.md` describe the four-stage lifecycle.
- `python sync.py status` is clean and `python sync.py push` round-trips byte-for-byte. Doc/prompt-only spec → `Test command: N/A` per the VHS-7 convention; Test plan is a review checklist plus a dry-run transcript of one `/spec-brief` run reaching an empty frontier and one hitting the round cap.

## Out of scope

- Porting any other upstream skill — `domain-modeling`, `grill-with-docs`, `to-spec`, `to-tickets`, `wayfinder`, `triage`. `to-spec`'s user-story spec template in particular is a different spec model from this repo's and is not adopted.
- Auto-invoking grilling from `/spec-cycle` Phase 1 authoring, `/ship-spec`, or `/spec-close`.
- Making the interview mandatory, or gating `/spec-cycle` on a brief having been grilled.
- Any change to the green gate, severity scale, round cap, FROZEN/REWRITE protocol, 2g polish, or the four reviewer agents.
- Creating or transitioning Plane tickets from `/spec-brief` beyond the ticket *read*; ticket creation stays where `/spec-cycle` Phase 0 step 2 already puts it.
- A fifth reviewer lens that reviews the brief. This ticket resolves forks *before* the brief exists; it does not add adversarial review *of* the brief.
- Anything in VHS-26 (author-side ground-truth gate during spec authoring and apply-findings) or VHS-27 (delta-scoped review passes past round 4). Both act on the spec loop; this acts upstream of it. VHS-32's 2f option and VHS-27's post-round-4 delta reviews touch adjacent text and should be sequenced, not merged.

## Risks / decisions

1. **Interview fatigue is the failure mode that kills this.** If `/spec-brief` asks 20 questions the operator will stop running it, and an unrun skill is worse than the current ad-hoc prompt. The three bounds in D6 are the mitigation; the spec author should pin the defaults and state the reasoning. Open: whether the per-round cap should be a hard truncation or a soft target.
2. **"Altitude fence" is prose, not mechanism.** Nothing stops the interview drifting into implementation detail. Accepted — same trust model as the rest of the repo's skills (cf. VHS-11 Risks §2). The spec should give two or three worked examples of an out-of-altitude question so the fence is legible.
3. **The fork format could be over-applied.** Rendering *For:* / *Against:* on a question with one plausible answer is noise that trains the operator to skim. D4 says non-branching questions use the plain form; the spec author pins the test for "genuinely branches."
4. **Grill-then-write may drift from grill-then-agree.** The upstream primitive is explicit: "Do not act on it until the user confirms you have reached a shared understanding." Whether `/spec-brief` writes the brief on an empty frontier automatically, or requires a confirm first, is a real fork — spec author pins it. Recommendation: confirm first, since the brief is the artifact every downstream lens treats as authority.
5. **`Explore` is a Claude Code built-in agent type.** Other harnesses have no such roster. D2's phrasing keeps the *prohibition* portable, but a harness with only one agent class cannot honor the read-only guarantee. The spec should state the degradation: if no read-only agent class exists, the primitive asks the operator rather than dispatching a write-capable agent.
6. **The 2f grill lands in text VHS-27 also targets.** Both edit the post-round-4 region of `skills/spec-cycle/SKILL.md`. Whichever ships second rebases onto the first; if VHS-27 ships first, the fourth menu option must compose with delta-scoped reviews rather than assume the current full-lens shape.
7. **A merged skill is inert until installed.** `python sync.py install` is required before `/spec-brief` or `/grill-me` resolve on any machine — the VHS-29 close hit exactly this. Never use `--prune` to do it (VHS-28 note: it queues deletes for the 14 separately-installed third-party skills under `~/.claude/skills/`).

## References

- Plane: VHS-32 (Backlog, Medium, created 2026-09-06). Adjacent open: VHS-26 (author-side ground-truth gate), VHS-27 (delta-scoped review passes) — both Backlog.
- Upstream reference: `mattpocock/skills` @ main, read 2026-09-06 — `skills/productivity/grilling/SKILL.md` (the primitive), `skills/productivity/grill-me/SKILL.md` (4-line user stub), `skills/engineering/grill-with-docs/SKILL.md` (composes `grilling` + `domain-modeling`), `skills/engineering/to-spec/SKILL.md` (synthesis-without-interview counterpart). MIT.
- `skills/spec-cycle/SKILL.md` (620 lines, read 2026-09-06) — Phase 0 step 1–2 brief resolution and local-only-ticket fallback `:23–60`, 2e FROZEN/REWRITE `:426–465`, **2f halt menu `:467–484`** (the insertion point), 2g post-green polish `:486–518`, Phase 3 HARD STOP `:520`.
- `agents/spec-reviewer-conventions.md`, `agents/spec-reviewer-correctness.md` — the brief-as-authority classification and the mandatory brief read.
- `docs/portability-contract.md` §2 (frontmatter classes; `model` / `allowed-tools` Claude-Code-only), §3 (`requires:` schema, optional-service `?` semantics).
- `docs/specs/DONE/VHS-11/brief.md` — the target brief shape: *Decisions carried forward* (settled tree) + *Risks / decisions* (deferred frontier, "spec author pins this").
- Precedent: commit `5e6d401` (reviewers pinned to Opus, working contract 2026-09-02); VHS-28 (clean-room rewrite posture toward third-party source); VHS-7 (`N/A` test command for doc-only specs, host-agnostic capability prose).
- Wiki: `vigil-harbor-wiki/projects/vigil-skills/state.md` — VHS-29 install-inertia note; VHS-28 `--prune` warning.
