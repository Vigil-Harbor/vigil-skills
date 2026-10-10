# VHS-53 — spec-close: declare vcs-host? in its requires: block
**Status:** Backlog · **Priority:** unset · **Assignee:** unassigned
**Created:** 2026-10-08 · **Plane:** VHS-53 (915bc2d3-758c-4504-8ff2-cae4426ec9a4, Backlog)
**Origin:** Filed from the VHS-51 review on 2026-10-08. VHS-51 put the `vcs-host` role token into use on `/ship-spec` and `/review-pr` and left `/spec-close` alone (its Decision 8), which made `/spec-close` the one shipped block that runs `gh` without declaring the role. The brief interview settled six decisions in two rounds; the tree was fully visited.

## Problem

`skills/spec-close/SKILL.md` runs `gh pr view` and `gh pr diff` (Phase 2a, PR-number path) under `network: true` with `services: [issue-tracker?, shared-memory?]`. It also has a commit-SHA path that needs no `gh`, so the accurate marker is probably `vcs-host?` (optional), not `vcs-host` (required). That needs a look at whether the PR path degrades to the SHA path when `gh` is absent, or halts.

## Why it matters

The portability contract says a skill declares the capabilities it uses and a harness treats an undeclared one as unavailable. After VHS-51 every other shipped skill that calls `gh` declares `vcs-host`; `/spec-close` is the lone exception, so a harness reading its block would not know the skill can reach for the PR host at all. The contract also says an optional service's fallback is stated in the body, and today the body states none: nothing says what happens when the merge identifier is a PR number and `gh` is missing.

## Scope (verified against current files, 2026-10-10)

| Path | Current | Change |
|------|---------|--------|
| `skills/spec-close/SKILL.md:6-10` | `requires:` block: `shell: true`, `filesystem: [read, write]`, `network: true`, `services: [issue-tracker?, shared-memory?]`. No `vcs-host`. | `services` gains `vcs-host?` (Decision 1). |
| `skills/spec-close/SKILL.md:73-82` | Phase 2a step 1 finds the merge by (a) `git log --grep`, (b) shared-memory ticket lookup yielding PR refs, (c) operator prompt "Enter PR number or commit SHA". Step 2 branches on identifier type: PR number → `gh pr view` / `gh pr diff`; SHA → `git show`. No fallback is stated for a PR number when `gh` is absent or fails. | Step 2's PR-number path states its fallback (Decision 2). |
| `skills/spec-close/SKILL.md:430` | Tool-use notes bullet: "`gh pr view` / `gh pr diff` for PR data." | Gains one clause naming the declaration and that the SHA path needs no `gh` (Decision 3). |
| `tests/test_spec_close_log.py:1178-1190` | `TestSkillDeclaration.test_requires_block_matches_the_tool_use_notes` pins the declared key set `{shell, filesystem, network, services}`, forbids `subagents`, and `assertIn`s `issue-tracker?` and `shared-memory?`. It does not forbid extra services. | Gains `assertIn("vcs-host?", block)` (Decision 4). |

## Decisions carried forward

1. **The marker is `vcs-host?`, optional.** `/spec-close` runs `gh` on one path only, and every VHS close to date (VHS-45, 46, 47, 51) found the merge SHA from `git log` first and never called `gh`. Required would refuse closes that work on a `gh`-less host.
2. **The PR-number path states its fallback.** When the identifier is a PR number and `gh` is absent or fails: resolve the PR to its squash-merge SHA with `git log --grep "(#<N>)"` and take the SHA path, printing one warning line that names the missing `gh`; if that grep finds nothing (a non-squash or rebase merge), fall through to the existing step 1c operator prompt for a SHA. This is the warn-and-proceed degrade the contract requires of a `?` service, with a bounded end that reuses a prompt already in the skill.
3. **The Tool-use notes name the declaration.** The `gh pr view` / `gh pr diff` bullet gains one clause of the form "(`vcs-host?`; the SHA path needs no `gh`)", so the body and the block stay in step, which is what the test checks for.
4. **The test pin asserts the new marker.** `TestSkillDeclaration` gains one `assertIn("vcs-host?", block)`, so the line cannot be removed silently; the existing pins are unchanged.
5. **No preflight probe for `gh`.** The contract permits an early advisory probe of an optional service but never requires one. `gh` is handled only at point of use (Decision 2); the common path never calls it, so a probe would warn on closes that do not need it.
6. **Scale is not a factor.** One frontmatter line, one body passage, one test literal.

## Done when

`/spec-close`'s `requires:` block declares the `vcs-host` role with the marker that matches its behaviour; lint and the spec-close tests pass.

## Out of scope

- Any other skill's `requires:` block, including `/ship-spec`'s required `vcs-host` and `/review-pr`'s `code-review-bot` (VHS-52).
- A preflight `gh auth status` probe in `/spec-close` (Decision 5).
- Reordering or changing Phase 2a step 1's three merge-lookup strategies; only step 2's PR-number path gains a stated fallback.
- The portability contract and `lint.py`; `vcs-host` and the `?` suffix are already in the vocabulary.
- Wiki filemap and state lines.

## Scale

**Factor:** no

## Risks / decisions

_(none open — the interview visited the whole tree)_

## References

- `skills/spec-close/SKILL.md:6-10` — the current `requires:` block (F1).
- `skills/spec-close/SKILL.md:73-82`, `:430` — Phase 2a merge lookup and diff read; the Tool-use notes bullet (F2).
- `docs/portability-contract.md:63,65,78` — `?` means degrade gracefully, warn-and-proceed; the body states the fallback; optional services need not be probed at preflight (F3).
- `tests/test_spec_close_log.py:1178-1190` — the declaration pin (F4).
- `git log --grep` on vigil-skills main and `docs/specs/DONE/VHS-51/reconciliation.md:6` — every VHS close to date took the SHA path (F5).
- Related: VHS-51 (Done; the `requires:` blocks and the `optional` boolean), VHS-52 (swappable reviewer), wiki decision `decisions/2026-10-10-vhs-51-optional-is-a-value-not-a-suffix.md`.
- Interview: 2 rounds, exit empty-frontier
