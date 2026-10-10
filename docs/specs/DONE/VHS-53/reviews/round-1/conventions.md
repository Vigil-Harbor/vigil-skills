The spec matches the portability contract and the VHS-51 decision: services stay a `?` suffix, the token is already in the lint vocabulary, and the edit stays inside the two files the brief names. Two spec-level pins are worth a drift-check; neither blocks.

# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Spec-level command pins the brief left open
**Severity:** P3
**Where:** spec § Decision 1 (lines 24–27); spec § Phase 2a step 2 (lines 72–91)
**Convention violated:** Silent-addition axis (c) — positions the brief does not spell out, each with rationale in Design, none labeled as an addition.
**Evidence:** Brief decision 1 only settles `vcs-host?`. Brief decision 2 settles `git log --grep "(#<N>)"`, one warning, then the existing step 1c prompt. The spec additionally commits to: appending the token so the line is `services: [issue-tracker?, shared-memory?, vcs-host?]` (ship-spec and review-pr put required `vcs-host` first); the flags `--all -1 --format=%H -F` (line 85), where `-F` changes match semantics versus default basic regex; stripping one leading `#` so `#123` and `123` both become `(#123)` (line 72); and discarding a successful `gh pr view` when `gh pr diff` is non-zero (line 76). Line 88 says `--all` "has the same reach as step 1a's `git log --all`", but step 1a is `git log --all --oneline -i -E --grep="…" -- .` (`skills/spec-close/SKILL.md:74`) — the pathspec is not in the fallback. Wiki decision `2026-10-10-vhs-51-optional-is-a-value-not-a-suffix.md` is aligned (services keep `?`; this ticket was the filed follow-up), and `lint.py` `SERVICES_VOCAB` already contains `vcs-host`.
**Suggested fix:** Under Decisions, add one sentence that these four pins are spec-level and the brief left them open. Either add `-- .` to the fallback command or drop the "same reach" sentence. No behavior change is required if the drift-check accepts the pins.

### F-2: Whole-tree diff allowlist is not the repo's leave-alone form
**Severity:** P3
**Where:** spec § Test plan item 4 (line 122); spec § Test command (line 135)
**Convention violated:** Prior shipped test commands scope `git diff --name-only origin/main --` to leave-alone paths (VHS-45, VHS-46, VHS-47, VHS-51). This spec inverts that into "nothing outside these two files."
**Evidence:** VHS-51's command ends with `git diff --name-only origin/main -- <leave-alone paths>` and an untracked check. VHS-53 uses `git diff --name-only origin/main | grep -vxE '^(skills/spec-close/SKILL.md|tests/test_spec_close_log.py)$'`. The brief's Done when is only "lint and the spec-close tests pass." In `/ship-spec`'s fresh worktree the allowlist matches "nothing else moves." On a branch that also differs in any other tracked path, the gate fails even though those paths are outside this change. Untracked files are invisible to `git diff`, so the check does not see them either way.
**Suggested fix:** Keep the allowlist only if a clause says it assumes a worktree cut from `origin/main` whose only edits are those two files. Otherwise switch to the established form: `git diff --name-only origin/main --` the leave-alone paths named in Scope and Out of scope.

## Summary

Wiki `projects/vigil-skills/architecture.md` is not present; this review used `filemap.md`, `state.md`, and the overlapping decisions (`2026-10-10-vhs-51-optional-is-a-value-not-a-suffix.md`, `2026-06-14-vhs-17-requires-tolerated-not-strict-yaml.md`, `2026-06-14-vhs-18-lint-warn-only-strict-gate.md`). Shared-memory lookup for namespace `skills` was denied; the brief's Problem and Done when were used instead. No `## Deferred — follow-up required` section is present.

P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 0

STATUS: GREEN
