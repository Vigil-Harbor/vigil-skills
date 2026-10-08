# Reconciliation Report: VHS-45

> Date: 2026-10-08
> Spec: docs/specs/TODO/VHS-45.spec.md
> Merge: PR #31, squash commit 1bd3f29
> Plane state: Done (group: completed)

## Summary
The shipped `/spec-tickets` skill and the three doc edits match the spec. Two drift items, both informational: one wording change in the ticket Assembly paragraph, and the test-output capture that `/ship-spec` adds to every PR. The skill has not been run against a live tracker.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-tickets/SKILL.md` | Yes | New, 184 lines |
| `AGENTS.md` | Yes | Stage added as item 3; `/ship-spec` and `/spec-close` renumbered; one External dependencies sentence |
| `README.md` | Yes | Skills list, workflow line, Requirements bullet |
| `docs/spec-workflow-reference.md` | Yes | Opening sentence; `## Optional stage: spec-tickets` before Skill 2; Skill 2 and 3 headings unchanged |
| `tests/test_lint.py` | Yes | Census 8 → 12 |

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-45.test-output.txt` — the test-gate capture `/ship-spec` Phase 3 writes.

Leave-alone paths: `git diff --name-only origin/main --` over the spec's list printed nothing before merge.

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | New stage, `/spec-tickets <spec-path>`, no flags | Confirmed | `skills/spec-tickets/SKILL.md:22` — Invocation; usage line halts on anything else |
| 2 | One integration branch and one PR per spec | Drifted (wording) | `skills/spec-tickets/SKILL.md:143` — Assembly paragraph says "the pre-merge review" where the spec says "the Codex gate". Changed because the repo is public and that gate is host-specific. Stated in the PR body. |
| 3 | Tracker holds the graph in three modes | Confirmed | `skills/spec-tickets/SKILL.md:46` — mode table; `:53` — "`halt` is not `local`" |
| 4 | Reference shape, cut only from the spec | Confirmed | `skills/spec-tickets/SKILL.md:72` — "Draft the fewest pieces"; grep for the five reserved phrases returns 0 |
| 5 | Stop for approval; never file headless | Confirmed | `skills/spec-tickets/SKILL.md:125` — "approval required — this skill does not file headless" |
| 6 | Each piece has its own acceptance criteria | Confirmed | `skills/spec-tickets/SKILL.md:64` — Phase 2, Acceptance criteria paragraph |
| 7 | The only input is the spec file | Confirmed | `skills/spec-tickets/SKILL.md:34` — "It is the only source for the breakdown" |
| 8 | Stage optional; `/ship-spec` unchanged | Confirmed | `skills/ship-spec/SKILL.md` absent from the diff |
| 9 | Scale is a non-factor | Confirmed | No batching, cap, or budget in the skill |
| 10 | Which docs gain the stage | Confirmed | `AGENTS.md:29`, `README.md:11`, `README.md:66`, `docs/spec-workflow-reference.md:129` |
| 11 | Lint census set to the shipped tree | Confirmed | `tests/test_lint.py:52` — `len(skills), 12,`; `requires:` is `filesystem` + `services: [issue-tracker?]` |
| 12 | File blockers first, create-only, no resume | Confirmed | `skills/spec-tickets/SKILL.md:133` — "File blockers first"; `:159` — "No resume" |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | A new skill decomposes an approved spec into pieces | Met | `skills/spec-tickets/SKILL.md` Phases 0–4; `python tests/test_lint.py` 6/6 |
| 2 | Each piece is ticketed; dependencies are relationships, not an ordered list | Met | `skills/spec-tickets/SKILL.md:46` — `native` row; `Blocked by` section on `text` and `local` |
| 3 | The graph, not a build order, decides what can run in parallel | Met | `skills/spec-tickets/SKILL.md:133` — "It is not a build order … the edges do" |
| 4 | The reference skills supply the shape that shores up `/ship-spec` | Met | Slice rules in Phase 2; Assembly paragraph at `:143` |

Unverifiable until first use: the `native` relation path against a live tracker (spec Decision 12 names the first live run as the proof).

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| `python tests/test_lint.py` exits 0 with 12 skills | Yes | `tests/test_lint.py:48`; output in `VHS-45.test-output.txt` |
| Programmatic lint of the new skill: zero ERROR, zero WARN, exact `requires:` keys | Run at ship, exit 0 | Spec `## Test command`, second command (not a stored test) |
| Leave-alone diff prints nothing | Run at ship, exit 0 | Spec `## Test command`, third command |
| Review checklist for the skill body | Reviewed in the round-5 delta pass and at implementation | `VHS-45.reviews/round-5/` |

## Process notes
- `/spec-cycle` ended RED after round 4 (gate 14, 8, 5, 4). The operator then cut Decision 12's read-back and resume protocol and chose the reference `to-tickets` shape. A delta-scoped round 5 on the rewritten sections was green on all three lenses. The post-green drift check was not run.
- CodeRabbit raised one Major finding on PR #31 (gate on the recorded `/spec-cycle` result). It was skipped with a reasoned reply and tracked as VHS-47.
- VHS-46 (ponytail review gate in `/ship-spec`) and the executor that would read child tickets are follow-ups, not part of this change.

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision: `/spec-tickets` files blockers first, create-only, with no read-back and no resume — the operator's cut after four red rounds, and the reason the skill names capabilities instead of one tracker's response shapes.
- Decision: a connected tracker that fails halts the run instead of falling back to local files, a deliberate departure from the portability contract's warn-and-proceed.

RECONCILED: yes DRIFT: 2
