# Reconciliation Report: VHS-46

> Date: 2026-10-08
> Spec: docs/specs/TODO/VHS-46.spec.md
> Merge: PR #33, squash commit 156d388
> Plane state: Done (group: completed)

## Summary
The shipped review gate, the bloat-check retirement, and the doc edits match the spec. Two drift items, both informational: the availability test for a shell review command was changed in PR review, and the PR carries the test-output capture. The gate has not yet run on a real change; the two behavioural acceptance criteria are unverifiable until the first `/ship-spec` run after install.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/ship-spec/SKILL.md` | Yes | Step 4b, Phase 3b (8 steps), and the small edits in Phases 0, 3, 4, 5, 7, Tool-use notes, Failure modes. No phase renumbered. |
| `skills/bloat-check/SKILL.md` | Yes | Deleted with its directory |
| `tests/test_lint.py` | Yes | Census 12 → 11 |
| `docs/customizing.md` | Yes | `### Review command section`; review file path under `## Spec & brief layout` |
| `docs/spec-workflow-reference.md` | Yes | `### Phase 3b — Review gate` |
| `AGENTS.md` | Yes | Lifecycle item clause; Decision 11 paragraph verbatim |
| `README.md` | Yes | ship-spec bullet clause |

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-46.test-output.txt` — the test-gate capture `/ship-spec` Phase 3 writes. The absolute worktree path on two lint lines was replaced with `<worktree-path>` because the repo is public.

Leave-alone paths: the test command's diff check printed nothing.

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Where the gate sits | Confirmed | `skills/ship-spec/SKILL.md:139` — `## Phase 3b — Review gate (one pass)`, between Phase 3 and Phase 4 |
| 2 | The review command is declared | Confirmed | `skills/ship-spec/SKILL.md:31` — step 4b: spec, then `CLAUDE.md`, then `AGENTS.md`, then none |
| 3 | Skips and what each leaves behind | Drifted | `skills/ship-spec/SKILL.md:149` — a shell command is no longer judged by its first word; it is run, and a shell "command not found" counts as not available. Changed in PR review (CodeRabbit, commit dd7b942): a valid line can open with a variable assignment or a builtin. The three skip rows are otherwise as specified. |
| 4 | A fresh, read-only reviewer | Confirmed | Phase 3b step 3: subagent with three rules, inline fallback under the same rules |
| 5 | One pass | Confirmed | Phase 3b intro: "The review command runs once per `/ship-spec` run" |
| 6 | Three groups, one mapping | Confirmed | Phase 3b step 4: mapping table; unmapped is Fix or record; unusable blocker is unresolved |
| 7 | The invariant veto | Confirmed | Phase 3b step 5: declared invariants, test pins, other fixes |
| 8 | What happens to each group | Confirmed | Phase 3b steps 5 and 6: halt block with three options |
| 9 | Tests after fixes | Confirmed | `skills/ship-spec/SKILL.md:206` — "A fix for a Blocks finding is held"; fresh count of 5; no second halt. The literal `Held:` line is the implementer's wording. |
| 10 | The review record | Confirmed | `skills/ship-spec/SKILL.md:211` — step 8 template; override reason rule is a bullet under it |
| 11 | bloat-check is retired | Confirmed | `skills/bloat-check/` absent; `AGENTS.md:93` — removal paragraph |
| 12 | Scale is a non-factor | Confirmed | No batching, cap, or budget added |
| 13 | The lint warning stays | Confirmed | `python lint.py --strict` exits 0 with the two `missing-requires` warnings |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | A run with a declared, available review command shows the gate, and a must-fix finding stops the commit | Unverifiable | Text present (Phase 3b steps 3 to 6). Not exercised: the shipping run used the pre-change skill. Unchecked post-merge item in PR #33. |
| 2 | A run with no review command declared completes and prints the skip note | Unverifiable | Text present (Phase 3b step 1). Not exercised, same reason. |
| 3 | bloat-check is gone and `python lint.py --strict` reports 0 ERROR | Met | `skills/bloat-check` absent on main; test command exit 0 |

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| `python tests/test_lint.py` exits 0 with 11 skills | Yes | `tests/test_lint.py:52` |
| `python tests/test_spec_close_log.py` exits 0 | Yes | 60 passed, 3 skipped at ship |
| `python lint.py --strict` exits 0 | Run at ship and again after the review fix | Spec `## Test command` |
| Structural checks (bloat-check absent, heading count, leave-alone diff, no product name in four files) | Run at ship, exit 0 | Spec `## Test command` |
| Review checklist, 13 rows | Read against the shipped text by the implementer and by the coordinator | `skills/ship-spec/SKILL.md:139`–`:237` |

## Process notes
- The brief was reviewed by Codex (gpt-6-sol, high) for three rounds before `/spec-cycle`: 2 blockers and 5 should-fix, then 3 should-fix, then ready.
- `/spec-cycle` went green at round 3 (gate 2, 1, 0). The round-2 finding was caused by the round-1 fix; the coordinator kept the fix and removed the added machinery, where the cycle's re-fold rule would have reverted and deferred it.
- `/spec-tickets` ran for the first time against a live tracker: two child tickets (VHS-49, VHS-50) and one native blocked-by relation. With one edge the graph was a serial chain; `/ship-spec` did not read the children.
- Machine setup done after merge, outside the repo: installed skill updated, the installed `bloat-check` copy removed, and `## Review command` added to the machine-local `CLAUDE.md`.

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision: `/ship-spec` runs one declared review before the commit — declared not detected, one pass, a blocker is never declined or silently undone, an unavailable or failing review is a recorded skip.
- Decision: bloat-check retired; only its invariant veto survives, and its per-type proof standard is knowingly dropped.

RECONCILED: yes DRIFT: 2
