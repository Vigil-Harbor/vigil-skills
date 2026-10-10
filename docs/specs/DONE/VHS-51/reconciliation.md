# Reconciliation Report: VHS-51

> Date: 2026-10-10
> Spec: docs/specs/TODO/VHS-51.spec.md
> Merge: PR #36 (8d404d0)
> Plane state: Done (group: completed)

## Summary
PR #36 shipped every path in the spec's Scope table and nothing else apart from the two expected ship-spec artifacts; all ten decisions are confirmed literally against HEAD, the three Done-when criteria are met, and the test command's four live checks (`test_lint`, `test_spec_close_log`, `lint --strict`, lint summary) pass with `lint: 0 error(s), 0 warning(s)`.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/ship-spec/SKILL.md` | Yes | Frontmatter block at lines 5-10; one body clause at line 419. No other hunks. |
| `skills/review-pr/SKILL.md` | Yes | Frontmatter block at lines 5-9; no other hunks. |
| `docs/portability-contract.md` | Yes | Schema comment (58), booleans bullet (63), services mapping (65), Availability (78), lexical rule 5 (87), Hermes sentence (103). |
| `lint.py` | Yes | Boolean branch at 106-108 only. |
| `tests/test_lint.py` | Yes | Zero-WARN assertion (60-61), two new cases (63-73). |
| `tests/fixtures/optional-bool/SKILL.md` | Yes | New; declares all three booleans `optional`. |
| `tests/fixtures/bad-bool.md` | Yes | New; `subagents: true?`. |
| `docs/authoring-portable-skills.md` | Yes | Template comment (16), WARN rule (36), promotion path now one step (41). |
| `tests/test_spec_close_log.py` | Yes | Rename + single `assertEqual(backlog, [])` at 1059-1063. |

Leave-alone list: `git diff --name-only 8d404d0~1 8d404d0` over every leave-alone path (spec-close, spec-cycle, spec-brief, spec-tickets, grilling, grill-me, session-handoff, talaria, hermes-kanban-awareness, `skills/ship-spec/states.json`, `sync.py`, `agents/`, `README.md`, `AGENTS.md`, other `tests/` files and fixtures) is empty. Respected. The only `requires:` lines in the skills diff are the two added blocks.

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-51.review.md` — ship-spec review record; expected artifact, not drift.
- `docs/specs/TODO/VHS-51.test-output.txt` — ship-spec test capture; expected artifact, not drift.

Dropped: none.

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | The two `requires:` blocks, exact YAML, after `user_invocable: true` before `---` | Confirmed | `skills/ship-spec/SKILL.md:4-11` — `user_invocable: true` / `requires:` / `shell: true` / `filesystem: [read, write]` / `network: true` / `subagents: optional` / `services: [vcs-host, issue-tracker?]` / `---`; `skills/review-pr/SKILL.md:4-10` — same with `services: [vcs-host, code-review-bot]` and no `subagents` line. Two-space indent, no comments or blank lines. |
| 2 | `optional` = used when offered, never a pre-flight requirement; string, never truthiness-tested | Confirmed | `docs/portability-contract.md:63` — '`optional` means the skill uses the affordance when the harness offers it ... never a pre-flight requirement ... must not be tested for truthiness'; `:78` — 'An `optional` boolean is likewise never verified at pre-flight; if it fails at point of use, the skill follows the fallback its body states.' |
| 3 | All three booleans accept `optional`; lint stays case-insensitive; contract says so | Confirmed | `lint.py:106` — `if val.lower() not in ("true", "false", "optional"):`; `lint.py:108` — 'must be true/false/optional'; `docs/portability-contract.md:87` — '(for a boolean key: `true`, `false`, `optional`, compared case-insensitively)'; fixture `tests/fixtures/optional-bool/SKILL.md:5-8` exercises `shell`, `network`, `subagents`. |
| 4 | Role tokens `vcs-host` / `code-review-bot` named to fleet meaning | Confirmed | `docs/portability-contract.md:65` — '`vcs-host` → the pull-request host and its CLI (GitHub via `gh`), `code-review-bot` → the review bot on that host (CodeRabbit), etc.' |
| 5 | `issue-tracker?` on `/ship-spec`; no behaviour change | Confirmed | `skills/ship-spec/SKILL.md:10` — `services: [vcs-host, issue-tracker?]`; the merge diff for this file has only the frontmatter hunk and the line-419 clause, so preflight step 8 / Phase 6 text is untouched. |
| 6 | Phase 3b Tool-use bullet names the declaration | Confirmed | `skills/ship-spec/SKILL.md:419` — 'inline otherwise, which is what `subagents: optional` in the frontmatter declares.' |
| 7 | Promotion path loses step 1 (one step remains); test renamed to `test_missing_requires_backlog_is_clear` asserting no backlog line | Confirmed | `docs/authoring-portable-skills.md:40-41` — single item '1. **Install a pre-commit hook** ... caught by `tests/test_lint.py::test_shipped_skills_clean`, since `--strict` never gates on WARNs.'; `tests/test_spec_close_log.py:1059` — `def test_missing_requires_backlog_is_clear(self):`, `:1063` — `self.assertEqual(backlog, [])`; test remains in `TestNoStaleWording`. |
| 8 | `/spec-close` block left alone (VHS-53 follow-up) | Confirmed | `skills/spec-close/SKILL.md:5-9` — block still `services: [issue-tracker?, shared-memory?]` (no `vcs-host`); path absent from the merge diff. |
| 9 | Zero-WARN tripwire in `test_shipped_skills_clean`; census 11 unchanged | Confirmed | `tests/test_lint.py:49` — '# Regression for VHS-18 ... VHS-51: and zero WARNs'; `:52` — `len(skills), 11`; `:60-61` — `skill_warns = warns(lint.lint_path(s))` / `assertEqual(skill_warns, [], f"unexpected WARN(s) in {s}: ...")`. |
| 10 | Scale is a non-factor | Confirmed | Merge stat excluding artifacts: 9 files, 63 insertions, 18 deletions; two frontmatter blocks and one lint tuple. |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Both skills carry a `requires:` block that matches what they use | Met | `skills/ship-spec/SKILL.md:5-10`, `skills/review-pr/SKILL.md:5-9` match Decision 1 byte-for-byte (see Decision 1 row); `grep -c '^  subagents: optional$' skills/ship-spec/SKILL.md` = 1. |
| 2 | `python lint.py` shows no `missing-requires` warning for any shipped skill | Met | Ran `python lint.py --strict` → exit 0, stderr `lint: 0 error(s), 0 warning(s)`; `python lint.py 2>&1 >/dev/null \| grep 'lint:'` → `lint: 0 error(s), 0 warning(s)`; `python lint.py 2>&1 \| grep -c missing-requires` → 0; `python tests/test_lint.py` → `Ran 8 tests ... OK` (includes the zero-WARN assertion at `tests/test_lint.py:60-61`). |
| 3 | Doc and test agree: authoring doc names no backlog, `tests/test_spec_close_log.py` pins that | Met | `grep 'have no \`requires:\` block' docs/authoring-portable-skills.md` → no match; `tests/test_spec_close_log.py:1059-1063` asserts `backlog == []`; ran `python tests/test_spec_close_log.py` → `Ran 60 tests ... OK (skipped=3)`. |

The brief's "Done when" (brief lines 39-41) is the same three bullets; no distinct criteria.

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| 1. `python tests/test_lint.py` exits 0 with two new cases and strengthened shipped-skills case; census 11 | Yes (ran: 8 tests OK) | `tests/test_lint.py:48-61` (`test_shipped_skills_clean`, census at :52), `:63-67` (`test_optional_boolean_accepted`), `:69-73` (`test_unknown_boolean_value_rejected`) |
| 2. `python tests/test_spec_close_log.py` exits 0 with renamed backlog test | Yes (ran: 60 tests OK, 3 skipped) | `tests/test_spec_close_log.py:1059-1063` |
| 3. `python lint.py --strict` exits 0; summary `lint: 0 error(s), 0 warning(s)` | Yes (ran: exit 0, summary matches) | Not a unit test; encoded in the spec Test command (`docs/specs/TODO/VHS-51.spec.md:148`) and pinned indirectly by `tests/test_lint.py:60-61` |
| 4. Literal lines in the two frontmatters | Yes (verified by grep) | `skills/ship-spec/SKILL.md:9-10`, `skills/review-pr/SKILL.md:9`; grep gate in spec Test command (`VHS-51.spec.md:148`) |
| 5. Authoring doc has no "have no `requires:` block" line | Yes | `tests/test_spec_close_log.py:1059-1063`; grep gate in spec Test command |
| 6. Leave-alone paths have no tracked diff / untracked files vs `origin/main`; `origin/main` resolves | Yes (verified: merge diff over the leave-alone list is empty) | Shell gate in spec Test command (`VHS-51.spec.md:148`); no unit test |
| 7. Contract booleans bullet contains `optional` | Yes (verified by grep) | `docs/portability-contract.md:63`; no unit test (prose review-checklist item) |

Review checklist for the prose: blocks match Decision 1 in position and indentation (lines cited above); `optional` semantics stated once in the contract (`:63`) with the authoring template pointing at it (`docs/authoring-portable-skills.md:16`), and neither doc says a harness probes an `optional` capability; `/ship-spec` Phase 3b bullet names declaration and fallback (`:419`); promotion path is one step with no cleared-step reference and no claim that `--strict` gates a WARN (`:41`); no `requires:` block other than the two new ones changed.

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision 2 + 3: the portability contract's boolean capability keys (`shell`, `network`, `subagents`) now accept a third value, `optional`, meaning "used when the harness offers it, body states the fallback, never a pre-flight requirement". This is a fleet-wide contract vocabulary change: every consumer (Hermes adapter in `vigil-converter`, any future harness) must treat only the boolean `true` as a requirement and must not test the string `optional` for truthiness; an `optional` boolean emits no Hermes gating key. The value was chosen over a `true?` suffix because `true?` is a string in every YAML parser and reads as a typo. Constraining for anyone writing an adapter.
- Decision 4: the role tokens `vcs-host` (pull-request host and its CLI, `gh` on GitHub) and `code-review-bot` (the review bot on that host, CodeRabbit) now have stated fleet meanings in the contract. Reusable by any skill that declares them; `vcs-host` is required on both new blocks because neither skill has a `gh`-less fallback.
- Decision 9: `tests/test_lint.py::test_shipped_skills_clean` is now the zero-WARN tripwire for the whole shipped-skill set (previously only `spec-close` and `session-handoff` had per-skill pins). Non-obvious because `lint.py --strict` never gates on WARNs, so this unit test, not the hook, is what catches a shipped skill that loses its `requires:` block. The wiki filemap line "2 tracked WARNs remain" is now stale (brief Risk 1).
- Decision 8: `/spec-close` is now the one block that uses `gh` without declaring `vcs-host`; its correct marker is `vcs-host?` (it degrades to a commit SHA), tracked as VHS-53. Worth a state line so the inconsistency is known rather than rediscovered.
- Comprehension: short note warranted. The `requires:` contract gained a value (`optional` on booleans) rather than a key, and the lint, the authoring template, the Availability rule, the lexical rule and the Hermes mapping all moved together; the missing-requires backlog is cleared and the promotion path to a blocking lint is now the pre-commit hook alone. Not an architectural change, but a vocabulary change that downstream adapters (vigil-converter's `HERMES-MAPPING.md` "booleans are never optional" wording, per Deferred edge-cases/R1/F-1) must track, so a brief comprehension entry keeps the contract's revision history findable.

RECONCILED: yes DRIFT: 0
