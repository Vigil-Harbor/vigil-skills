# Reconciliation Report: VHS-15

> Date: 2026-06-16
> Spec: docs/specs/TODO/VHS-15.spec.md
> Merge: PR #21 (squash commit a9e7581)
> Plane state: PR Review (group: completed)

## Summary
Shipped as specified. All six Done-when criteria are met with code evidence; the diff matches the spec's Scope exactly (the new agent + eight edited files). One spec-vs-reality note: `docs/spec-workflow-reference.md` was listed under *Files to change* but was untracked on `main`, so the PR **introduced** it (reconciled content) rather than editing a tracked file — net effect identical. The only diff entry not named in the spec is the ship-spec test-output artifact.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `agents/spec-reviewer-scalability.md` | Yes | Created (+124) — the new fourth reviewer |
| `skills/spec-cycle/SKILL.md` | Yes | Changed (+140/-…) — Phase 0 step 8, 2b–2e, Phase 3, failure modes |
| `agents/spec-reviewer-correctness.md` | Yes | Changed — grounding step 7 generalized + `scale_lens` input |
| `agents/spec-reviewer-edge-cases.md` | Yes | Changed — same grounding-step-7 plumbing |
| `agents/spec-reviewer-conventions.md` | Yes | Changed — same grounding-step-7 plumbing |
| `AGENTS.md` | Yes | Changed — reviewer table/count prose + `## Scale` convention + SSOT fix |
| `README.md` | Yes | Changed — reviewer list reconciled + scalability bullet |
| `docs/spec-workflow-reference.md` | Yes | **Introduced** (+185) — was untracked on `main`; spec listed it under *Files to change*. Reconciled content + new "Optional scalability lens" subsection |
| `docs/portability-contract.md` | Yes | Changed — count-neutral phrasing of the worked `subagents` example |

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-15.test-output.txt` — the ship-spec test-gate capture (lint `--strict` output). Standard audit artifact, not a code change; benign.

Files the spec fenced as "leave alone" (`skills/ship-spec/**`, `skills/spec-close/**`, `skills/review-pr/**`, `sync.py`, `lint.py`, `states.json`): none touched. ✓

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Opt-in, author-owned, off by default; no auto-detection | Confirmed | `SKILL.md:341` — "When `scale_lens != on`, no fourth `Agent` call is emitted … behavioral no-op" |
| 2 | Option B — new fourth agent, not folded into edge-cases | Confirmed | `agents/spec-reviewer-scalability.md` exists as a standing, separately-scored lens |
| 3 | One declaration in the brief, with a target N | Confirmed | `SKILL.md:~260` step-8 Target rule — "`**Factor:** yes` with no Target → off" |
| 4 | Peer reviewer, not a new stage — pass budget untouched | Confirmed | `SKILL.md:335` — fourth call dispatched within round 2b's same message |
| 5 | Same severity scale; opt-in toggle is the calibration answer | Confirmed | `agents/spec-reviewer-scalability.md` — P0–P4 block verbatim + scale calibration paragraph |
| 6 | Scope is architectural and operational scale | Confirmed | scalability agent "Operational axes" (cost/latency/token budget) |
| 7 | Security-first (resource-exhaustion / DoS / cost-blowout) | Confirmed | scalability agent "Security axes" |
| 8 | No regression of lifecycle invariants; step-7 edit is plumbing | Confirmed | 3 reviewer agents: step 7 reads every report present + stale-`scalability.md` guard; no critique/severity change |
| 9 | Two doc reconciliations beyond brief (README, portability-contract) | Confirmed | both edited; flagged spec-additions-with-rationale |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | New scalability agent, reviewer shape, read-only, differentiator + smell-list | Met | `agents/spec-reviewer-scalability.md` — "scalability asks 'does the design hold at N×?'"; ends "Do not edit any file. You are read-only." |
| 2 | Conditional 2b dispatch iff scale declared; saves `round-<N>/scalability.md`; folds into gate + all three closure artifacts | Met | `SKILL.md:335` (dispatch), `:401` (save), `:411` 2d gate, 2e round-4 manifest, step-2b closure-manifest note |
| 3 | No scale declaration ⇒ behavior unchanged (no fourth call, no `scalability.md`, identical gate/closure even with stale file) | Met | `SKILL.md:341` no-op guard; 3-agent stale-`scalability.md` guard `when scale_lens == off` |
| 4 | Brief scale-declaration field documented in `spec-workflow-reference.md` + `AGENTS.md` | Met | `spec-workflow-reference.md` § "Optional scalability lens"; `AGENTS.md` `## Scale` convention bullet |
| 5 | Phase 3 drift-check accounts for declared scale target as carried-forward decision | Met | `SKILL.md:543-545` Scale-declaration block; Phase 1 records the Decision |
| 6 | "3-lens" prose reconciled across AGENTS.md, SKILL.md desc, spec-workflow-reference.md (+ README, portability-contract) | Met | item-12 reviewer-count grep returns zero over all touched files |

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| `python lint.py --strict` over SKILL.md + 4 agents exits 0 | Yes | `docs/specs/TODO/VHS-15.test-output.txt` — "lint: 0 error(s), 4 warning(s)" / "exit=0" |
| Item-12 reviewer-count grep returns zero over touched files | Yes (verified at ship) | n/a — locator grep, not a committed test |
| Checklist items 3–13 (lens-off no-op, stale-guard, round-4 manifest, reviewer-failure gate, etc.) | By inspection | Prompt-prose change; verified against reconciled `SKILL.md` (no unit-test suite in repo) |

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision 1 (opt-in, off by default, no auto-detection): the deliberate departure from VHS-15's "constant frame" lean — declare-don't-infer applied to the scale lens. Reusable stance for any future optional reviewer lens; constrains how the toggle default could later flip.
- Decision 2 (option B — separate agent over folding into edge-cases): architectural choice with the ticket's own stated risk as rationale (folding would dilute edge-cases focus). Constrains future "add a lens" work toward standing, separately-scored agents.
- Comprehension (optional fourth lens added to spec-cycle): what changed (new agent + conditional 2b dispatch + grounding-step-7 closure generalization with stale-report guard), why (move the scaling argument upstream), what would break (a reviewer-count regression or a step-7 read that doesn't honor `scale_lens` reintroduces phantom findings on off-runs).

RECONCILED: yes DRIFT: 1
