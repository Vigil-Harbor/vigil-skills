# Conventions Review — round 3

Grounding: spec and brief read fresh from disk. Both are byte-identical to the `round-2/` and `round-3/` copies. `HEAD` is still `0158267f681386d7b51c3239ec2bc0b13c45ba25`, the spec's anchor commit. Read `AGENTS.md` (the tracked conventions; `CLAUDE.md` only points to it), wiki `state.md`/`filemap.md`, and wiki decisions `2026-10-13-vhs-27-delta-scoped-review-passes.md` and `2026-08-09-review-round-artifacts-are-immutable.md`. Ticket lookup failed (shared memory returned 502), so I proceeded on the brief.

Deferred-findings block: the spec has no `## Deferred — follow-up required` section (only `## Deferred (P2+)`), so there are no rows to validate and no routing violations.

Delta scope: critique was applied only to the five named headings. All five are "no text change" hits caused by the untracked VHS-41 review/attempt trees. That is the dispatch Decision 10 predicts under the currently installed rules.

## Closure of round 2 findings

The closure manifest is empty (round 2 closed green, no P0/P1). Round 2's three P3 findings are tracked for completeness.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Ticket not cached | CLOSED | `spec.md:404` records the brief-only degrade with no spec change; the outage recurs this round (see F-2 below). |
| correctness | F-2 | Touched workflow files changed within the last week | CLOSED | `HEAD` is still `0158267`. Re-checked the anchors: `skills/spec-cycle/SKILL.md:363-375`, `:417`, `:453`, `:488`, `:490`, `:492`, `:506`; the four agents' `# Delta scope` blocks (correctness `:90`, edge-cases `:88`, conventions `:93`, scalability `:77`); `README.md:10`; `docs/spec-workflow-reference.md:74` and `:81`. All match the quoted current text. |
| edge-cases | F-1 | Ticket grounding remains unavailable | CLOSED | Same disposition as correctness F-1, `spec.md:404`. |
| conventions | — | (no findings in round 2) | — | — |

No REOPENED or PARTIAL items.

## Findings

### F-1: `.attempt-<n>/` enters the skill text with no definition in any tracked file
**Severity:** P3
**Where:** spec § `### Decision 5 — ignore every open ticket's review and attempt archives`; spec § `### skills/spec-cycle/SKILL.md:490 — changed-path drop`
**Convention violated:** Repo pattern — directory layouts the skills rely on are defined in tracked files (`<TICKET-ID>.reviews/` is defined by the skill and `docs/spec-workflow-reference.md`). `AGENTS.md` describes the repo as harness-neutral and public.
**Evidence:** `grep -rn -i "attempt-" skills agents docs/*.md README.md AGENTS.md` returns nothing. The `docs/specs/TODO/<ID>.attempt-<n>/` layout exists only as operator practice (the untracked `docs/specs/TODO/VHS-41.attempt-1/`). The replacement sentence at `SKILL.md:490` names `<ticket>.attempt-<n>/` without saying what it is. The decision itself is authorized by the brief (Decision 5 and the Scope row), so this is class (a), not drift.
**Suggested fix:** Optional. Add a short gloss in the replacement sentence, for example "(an operator-made archive of a superseded attempt)", so the skill does not reference an undefined layout. No behaviour change.

### F-2: Ticket grounding unavailable
**Severity:** P3
**Where:** review grounding step (not a spec region)
**Convention violated:** None — this is a process note.
**Evidence:** `memory_search` with tags `[plane_work_item, VHS-60]` in namespace `skills` returned HTTP 502. The review used the documented brief-only degrade path, which `spec.md:404` already records.
**Suggested fix:** No spec edit. Compare the ticket with the brief when the integration is reachable.

Checks on the five in-scope headings that produced no finding:
- **Decision 5 against wiki decision 6 of VHS-27** ("code that merges after a round is a changed region"): Decision 5 narrows the changed-path set. The brief carries this explicitly as the VHS-27 follow-up, and the canonical cross-ticket brief/spec stay visible. Authorized by the brief; no silent supersession.
- **Decision 5 against "review-round artifacts are immutable"**: consistent. The archives are ignored as drift, not edited.
- **`### Changed-path filtering`**: reuses the existing drop step and its ordering and adds no new mechanism. The `docs/specs/DONE/VHS-41/reviews/correctness.md` example is illustrative and matches the brief's known-limits item in Out of scope.
- **`### skills/spec-cycle/SKILL.md:490`** and **`:492`**: the quoted "Current" blocks match the live file exactly. The replacements extend the existing sentences in place — no registry, no flag, no compatibility shim. The joining-word and punctuation lists are the pin the brief's Risk 3 asks the spec author to make.
- **`## Scenarios`**: one scenario per changed behaviour, as the brief's Done-when requires. Tokens match the mode-table replacement. Scenario 18 matches brief Decision 10.
- **Silent additions:** none in the five headings. Each traces to brief Decisions 2, 3, 5, 7, 8, 9 or 10.
- **Anchor drift:** no dead or moved citations.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 0

STATUS: GREEN
