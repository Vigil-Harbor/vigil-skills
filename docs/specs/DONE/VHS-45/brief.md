# VHS-45 — New skill: decompose a spec into dependency-linked tickets so implementation can run in parallel
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-10-08 · **Plane:** VHS-45 (da46a6a9-b232-4c13-810c-892c8961ca36, Backlog)
**Origin:** Devin, 2026-10-08, while setting up the CLT-221 + CLT-272 lanes on petland (Opus brief, Astra/Codex review of brief and PR, Grok for spec-cycle and implementation): "grok to do the workhorse stuff of spec-cycle and implementation (which honestly needs a new VHS skill with proper spec decomposition and ticketing pieces of dependency relationships, not a build-order, for parallelization). Matt Pocock skills would shore up that ship-spec shape."

## Problem

`/ship-spec` takes one green-lit spec through one worktree, one implementation loop and one PR. A spec's implementation steps are a build order: a single sequence for a single agent. Nothing in the lifecycle turns a spec into separately shippable pieces, records which piece depends on which, or files those pieces as tickets.

## Why it matters

A workhorse model implements the whole spec serially, and parallel agents cannot be pointed at it safely.

## Scope (verified against current files, 2026-10-08)

| Path | Current | Change |
|------|---------|--------|
| `skills/spec-tickets/SKILL.md` | Does not exist. | New skill `/spec-tickets`: breaks a green-lit spec into pieces, stops for operator approval, then files each piece as a child ticket of the spec's ticket with its blocking edges (Decisions 1, 3, 5, 6, 7). |
| `skills/ship-spec/SKILL.md` | One agent, one worktree at `<project-root>/../<TICKET-ID>-worktree` cut from `origin/<default-branch>`, eight phases, no subagent dispatch (`skills/ship-spec/SKILL.md:57`, `:76`). | None. Left alone in this ticket (see Out of scope). |
| `skills/spec-cycle/SKILL.md` | A spec's required sections are Goal, Scope, Design, Test plan, Test command, Done when, Out of scope; there is no task-graph section (`skills/spec-cycle/SKILL.md:298`). | None. The breakdown is not written into the spec (Decision 1). |
| `AGENTS.md` | Lists the lifecycle stages; `/ship-spec` is item 3 (`AGENTS.md:29`). | Name `/spec-tickets` as an optional stage between `/spec-cycle` and `/ship-spec` (Decisions 1, 8). |

## Decisions carried forward

1. **A new stage skill, `/spec-tickets`, between `/spec-cycle` and `/ship-spec`** (Q1, Q11). Why: it is the reference shape (the reference repo's breakdown is its own user-invoked skill), it keeps the reviewed spec stable, and it gives the approval step a home.
2. **One integration branch and one PR per spec** (Q2). Why: `/review-pr`, `/spec-close`, the Codex gate and the single Plane state flip keep working unchanged. The pieces are written to be assembled this way; the executor that assembles them is out of scope here.
3. **The tracker is the source of truth for the dependency graph** (Q3). Each piece is a child ticket of the spec's ticket. Blocking edges are native `blocked_by` links where the host's tracker integration has a blocking-relation capability. Where it has none, each ticket carries a "Blocked by" section. With no tracker reachable, the skill writes one local file per ticket. Why: this is the reference skill's rule, and it is what the ticket asks for.
4. **`to-tickets` and `implement-spec` from `mattpocock/skills` are the references** (Q5). Where the operator has stated no decision of their own, the spec follows the reference shape: vertical slices that are verifiable alone and fit one context window, prefactoring first, expand–contract for wide refactors, and pointers to the spec in place of duplicated text. Why: the operator wants to run the reference workflow as designed, to learn from it.
5. **The skill always stops for operator approval before it files tickets** (Q6). It does not run headless. Why: a wrong breakdown is cheap to fix before tickets exist, and the workhorse model starts after this stage.
6. **Each piece carries its own acceptance criteria**, taken from the spec's Done when and Test plan (Q7). The spec's full Done when and the Codex gate apply once, on the assembled branch.
7. **The input is a green-lit spec file from `/spec-cycle`, and nothing else** (Q8). Why: pieces trace to reviewed text, and there is one input shape to specify.
8. **The stage is optional for now, until the downstream is smoothed out** (Q12). A spec with no breakdown ships through `/ship-spec` exactly as today, and `/ship-spec` ignores child tickets until the executor follow-up lands.

## Done when

Transcribed from the ticket's "What is asked for":

- A new vigil-skills skill that decomposes an approved spec into pieces.
- Each piece is ticketed in Plane, with the dependency relationships between pieces recorded as relationships, not as an ordered list.
- The dependency graph, not a build order, decides what can run in parallel.
- Matt Pocock's published skills are the reference for the shape; use them to shore up /ship-spec.

## Out of scope

- **The ship-spec orchestrator reshape** (Q4): running pieces in parallel with an implementer per unblocked piece is a follow-up ticket, not yet filed. This ticket changes nothing in `skills/ship-spec/SKILL.md`.
- **Adding relations to plane-proxy** (Q10): the skill names the capability, not a tool. A host on the proxy gets the "Blocked by" text path. The operator notes the proxy may no longer be needed now that the official Plane tool set is about 30 tools.
- **Porting the reference repo's `tdd` or `code-review` skills** (Q5). The pre-commit review step is VHS-46.
- **Inputs other than a spec file** (Q8): a ticket or a conversation as input is not supported.
- **Writing a task graph into the spec, or having the review lenses check the breakdown** (Q1).

## Scale

**Factor:** no

## Risks / decisions

1. Which other tracked docs name the lifecycle stages and need the new stage added (`README.md`, `docs/spec-workflow-reference.md`, `docs/portability-contract.md`) — not read during grounding; spec author pins this.
2. Whether `tests/test_lint.py`'s skill-inventory tripwire must change for the new skill, and whether it is still stale as VHS-42 reports — not read during grounding; spec author pins this.
3. The native-relation path has only been seen as a tool schema; no `blocked_by` link has been created through it, and the lifecycle skills' other Plane steps have not been run against the official Plane tools — spec author pins this.

## References

- `skills/ship-spec/SKILL.md:57`, `:76` — one worktree per spec, cut from origin's default branch only; `:226-229` — one Plane ticket flipped per spec.
- `skills/spec-cycle/SKILL.md:298` — a spec's required sections; no task-graph section.
- `AGENTS.md:29` — the lifecycle list entry for `/ship-spec`.
- `mattpocock/skills` `skills/engineering/to-tickets/SKILL.md` — vertical slices, blocking edges, expand–contract, approval loop (§4), and the storage rule: native blocking links, else a "Blocked by" section, else one local file per ticket; tickets are sub-issues of the source issue (§5).
- `mattpocock/skills` `skills/engineering/implement-spec/SKILL.md` — the task graph worked as a frontier on one integration branch.
- `mattpocock/skills` `skills/engineering/README.md` — the breakdown is its own user-invoked skill, run after `to-spec` and before `implement-spec`.
- `petland/.claude/orchestration-templates/grok-ship-spec.md` — `/ship-spec` is driven headless and cannot ask the operator anything.
- `petland/.claude/orchestration-templates/CODEX-GATE.md` — the Codex gate runs one round per PR head sha.
- `AGENTS.md`; `docs/portability-contract.md` §4 — the repo is public; skills name capabilities, not tools.
- Plane has native "Blocked by" and "Blocking" relations — operator screenshot, `Screenshot 2026-10-08 021730.png`.
- The official Plane tools expose a work-item relation capability with a built-in `blocked_by` type — tool schema, this session.
- plane-proxy has no relation support — its work-item tool schemas expose `parent` only; a search of the proxy source found one unrelated match in `src/logger.ts`.
- Related tickets: VHS-46 (ship-spec pre-commit review gate; retire bloat-check), VHS-31, VHS-27, VHS-43, VHS-44.
- Interview: 3 rounds, exit empty-frontier
