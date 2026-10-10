# Reconciliation Report: VHS-53

> Date: 2026-10-10
> Spec: docs/specs/TODO/VHS-53.spec.md
> Merge: PR #37 (2f2fb8f)
> Plane state: Done (group: completed)

## Summary
PR #37 shipped exactly the two code paths the spec names plus the two ship-spec audit artifacts; all six decisions are confirmed literally against HEAD, the single Done-when criterion is met, and the spec's test gate passes on main (`lint: 0 error(s), 0 warning(s)`, spec-close tests OK with 3 skipped).

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-close/SKILL.md` | Yes | +27/−3: `vcs-host?` appended to `services`; Phase 2a step 2 PR-number bullet gains the stated fallback; Tool-use notes bullet gains the clause |
| `tests/test_spec_close_log.py` | Yes | +1: `assertIn("vcs-host?", block)` in `TestSkillDeclaration` |

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-53.test-output.txt` — ship-spec test capture (expected audit artifact, not drift)
- `docs/specs/TODO/VHS-53.review.md` — ship-spec review-gate record (expected audit artifact, not drift)

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | The marker is `vcs-host?`, optional | Confirmed | `skills/spec-close/SKILL.md:9` — '  services: [issue-tracker?, shared-memory?, vcs-host?]' |
| 2 | The PR-number path states its fallback | Confirmed | `skills/spec-close/SKILL.md:88` — 'warning: gh absent or failed for PR #<N> — resolving the squash-merge SHA…'; `:92` — 'git --no-pager log --exclude=refs/stash --all --format=%H%x09%P%x09%s -F --grep="(#<N>)"'; `:100` — zero or several accepted lines fall through to the step 1c prompt |
| 3 | The Tool-use notes name the declaration | Confirmed | `skills/spec-close/SKILL.md:451` — '`gh pr view` / `gh pr diff` for PR data (`vcs-host?`; the SHA path needs no `gh`).' |
| 4 | The test pin asserts the new marker | Confirmed | `tests/test_spec_close_log.py:1192` — 'self.assertIn("vcs-host?", block)' |
| 5 | No preflight probe for `gh` | Confirmed | Phase 0 of `skills/spec-close/SKILL.md` contains no `gh` invocation (grep count 0 between `## Phase 0` and `## Phase 1`) |
| 6 | Scale is a non-factor | Confirmed | Diff adds no loop, cache, batch, or fan-out; one token, one passage, one assertion |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `requires:` declares the `vcs-host` role with the marker that matches its behaviour (`vcs-host?`, fallback stated in the body); lint and the spec-close tests pass | Met | `skills/spec-close/SKILL.md:9`, `:88-100`; `python tests/test_spec_close_log.py` → OK (skipped=3); `python lint.py --strict` → `lint: 0 error(s), 0 warning(s)` |

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| 1. spec-close tests pass with the new `assertIn` | Yes | `tests/test_spec_close_log.py:1192` |
| 2. `lint.py --strict` exits 0 with zero warnings | Yes | run on main at 2f2fb8f: `lint: 0 error(s), 0 warning(s)` |
| 3. exact `services` line present | Yes | `skills/spec-close/SKILL.md:9` (`grep -qxF` passes) |
| 4. diff against origin/main touches only the two files | Yes | PR #37 file list: the two files plus the two audit artifacts |
| Review checklist (prose): warn once, one `git log`, one-parent + subject-ends-with rule, fall-through prompt, no digits check, no ancestor filter, Tool-use clause, no Phase 0 probe | Yes | `skills/spec-close/SKILL.md:84-100`, `:451`; Phase 0 unchanged |

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision 2: how a skill identifies "the" squash-merge SHA for a PR without `gh`: `git log --exclude=refs/stash --all -F --grep="(#N)"`, accept only a one-parent commit whose subject ends with ` (#N)`, and treat zero or several accepted lines as not found rather than picking the newest. Reusable by any skill that needs a PR-to-SHA fallback on this fleet; constraining because it deliberately refuses two-parent merges and body mentions.
- Decision 1 + 5: the pattern for an optional service, now exercised: declare `?`, no preflight probe, warn once at point of use, state the degrade in the body. Completes the `?` contract that VHS-51's decision entry defines; worth one paragraph in that lineage rather than a new comprehension entry.
- Comprehension: not warranted. One passage in one skill; the VHS-51 comprehension entry already covers the contract vocabulary.

RECONCILED: yes DRIFT: 0
