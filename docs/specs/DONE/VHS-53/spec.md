# VHS-53 — spec-close: declare vcs-host? in its requires: block

## Goal

`/spec-close` declares the `vcs-host` role it already uses, as the optional marker `vcs-host?`, and its PR-number path states the warn-and-proceed fallback the portability contract requires of a `?` service. The commit-SHA path is unchanged and still does not call `gh`. One assertion pins the new marker. Nothing else moves.

## Scope

| Path | Change |
|------|--------|
| `skills/spec-close/SKILL.md` lines 5–9 | `services` gains `vcs-host?`, appended. The line becomes `  services: [issue-tracker?, shared-memory?, vcs-host?]`. `shell`, `filesystem`, and `network` stay as they are (Decision 1). |
| `skills/spec-close/SKILL.md` lines 78–81 | Phase 2a step 2's PR-number path states its fallback. Step 1 (lines 73–77) and step 3 (line 83) are not edited. The ">500 lines" sentence under step 2 stays (Decision 2). |
| `skills/spec-close/SKILL.md` line 430 | The `gh pr view` / `gh pr diff` Tool-use notes bullet gains one clause (Decision 3). |
| `tests/test_spec_close_log.py` lines 1178–1191 | `TestSkillDeclaration.test_requires_block_matches_the_tool_use_notes` gains `assertIn("vcs-host?", block)` immediately after the `shared-memory?` assert. No other assertion changes (Decision 4). |

Leave alone: every other line of those two files (including the "Merge commit not found" failure-mode bullet at line 440, the Bash Tool-use bullet at line 433, and `test_lint_is_clean_including_warns`), every other skill's `requires:` block, `docs/portability-contract.md`, `lint.py`, `docs/authoring-portable-skills.md`, wiki filemap and state lines, and `skills/spec-close/scripts/`.

## Decisions

Brief decision numbers are in parentheses. These six were settled in the brief interview. This spec does not reopen them.

### Decision 1 — The marker is `vcs-host?`, optional (brief 1)

`/spec-close` runs `gh` on one path only: Phase 2a step 2, when the identifier is a PR number, in full-close and report-only. Partial-close skips Phase 2, and the commit-SHA branch never calls `gh`. Every VHS close to date found the merge SHA from `git log` and never called `gh`. A required `vcs-host` would refuse closes that already work on a `gh`-less host. The token is appended, so the existing pair stays in its current order:

```yaml
  services: [issue-tracker?, shared-memory?, vcs-host?]
```

`issue-tracker?` and `shared-memory?` are unchanged. No other frontmatter key changes.

### Decision 2 — The PR-number path states its fallback (brief 2)

When step 2 has classified the identifier as a PR number and `gh` is absent or fails, the skill does not halt and does not invent a second lookup strategy. It warns once, resolves the PR to its squash-merge SHA with one `git log --grep "(#<N>)"`, and takes the existing commit-SHA branch. If that lookup does not resolve to exactly one such SHA, it falls through to the step 1c prompt that is already in the skill. No preflight probe (Decision 5). The passage is specified in Design.

The brief left the argv open. Design pins it: `--exclude=refs/stash`, `-F`, a subject ending in ` (#<N>)`, and exactly one parent. Zero matches and several matches are the same fall-through as finding nothing. That is how "the" squash-merge SHA is identified, not a second strategy and not a newest-wins guess. Appending `vcs-host?` (Decision 1), stripping one leading `#`, and discarding a `gh pr view` whose `gh pr diff` failed are the same kind of pin.

### Decision 3 — The Tool-use notes name the declaration (brief 3)

The line-430 bullet gains one clause of the form the brief settled, so the body and the block stay in step:

`- Read, Grep for code verification, duplicate detection, and evidence extraction. `gh pr view` / `gh pr diff` for PR data (`vcs-host?`; the SHA path needs no `gh`).`

No other Tool-use bullet changes.

### Decision 4 — The test pin asserts the new marker (brief 4)

`TestSkillDeclaration.test_requires_block_matches_the_tool_use_notes` gains one `assertIn("vcs-host?", block)`. The declared-key set, the `subagents` forbid, and the existing `assertIn`s for `issue-tracker?` and `shared-memory?` stay. The assertion reads the frontmatter (`text.split("---", 2)[1]`), which is the block Decision 1 edits. It does not parse the body; Decision 3's clause is checked by reading the bullet, not by a second assertion.

### Decision 5 — No preflight probe for `gh` (brief 5)

The contract permits an early advisory probe of an optional service and does not require one. `gh` is handled only at point of use, inside the PR-number branch. Phase 0 is not edited. The common path never calls `gh`, so a probe would warn on closes that do not need it.

### Decision 6 — Scale is a non-factor (brief 6)

One frontmatter token, one body passage, one test literal. The spec adds no scale machinery: no batching, no cache, no new loop bound, no fan-out.

## Design

### `requires:` block

In `skills/spec-close/SKILL.md`, replace the services line and nothing around it:

```yaml
  services: [issue-tracker?, shared-memory?, vcs-host?]
```

Two-space indent, single line, no quotes, no comment, `?` on each of the three tokens. `vcs-host` is already in the contract vocabulary (`docs/portability-contract.md` §3) and in `lint.py`'s `SERVICES_VOCAB`, so the line lints.

### Phase 2a step 2

Replace only the PR-number bullet. The commit-SHA bullet and the ">500 lines" sentence stay verbatim. Step 1's three strategies, including the step 1c prompt text, stay verbatim.

An identifier reaches this step already classified by the skill as it stands today. This spec does not add a classifier and does not change step 1. `<N>` is the PR number that classification selected, with one leading `#` removed if the selected text has one, so both `123` and `#123` produce the pattern `(#123)`. No other trimming. An empty or non-numeric `<N>` for which both `gh` commands exit 0 is that other PR: no argument uses the current branch's PR, and a branch name selects that branch. That success is not a fallback case. This spec does not add a digits check.

**PR number.** Run `gh pr view <N> --json files,additions,deletions`, then `gh pr diff <N>`. If both exit 0, use that output as today and do not run the fallback.

`gh` is absent or has failed when it cannot be executed (not on `PATH`, or the harness reports the command unavailable) or either of those two commands exits non-zero. Auth failure, network failure, a missing PR, and a non-zero `gh` are the same case. Do not parse `gh`'s stderr. If `gh pr view` exits 0 and `gh pr diff` does not, discard the view output.

On that case, print exactly one warning line, then run one `git log`. Do not run a second lookup.

```text
warning: gh absent or failed for PR #<N> — resolving the squash-merge SHA with git log --grep "(#<N>)"
```

```text
git --no-pager log --exclude=refs/stash --all --format=%H%x09%P%x09%s -F --grep="(#<N>)"
```

`--exclude=refs/stash` comes before `--all`, so the stash ref and the index commit it points at are not walked. A squash merge that is not on `HEAD` is still visible. This is not step 1a's reach: step 1a also passes `-- .`, and this command does not. `-F` keeps `(#<N>)` literal. Default `--grep` is basic regex, and unescaped parentheses are already literal there; `-F` is what stops a `grep.patternType=extended` config, or an `-E` flag, from turning the pattern into a group that also matches a bare `#<N>`.

Split each stdout line on the first two tab characters. Column 1 is the SHA, column 2 is the parent SHAs, and the remainder is the subject. Accept a line only when column 1 is one hex SHA of 40 or 64 characters, column 2 is exactly one parent SHA (hex, no space), and the trimmed subject ends with ` (#<N>)`. A body mention, a revert subject (it does not end with ` (#<N>)`), and anything reachable only from `refs/stash` is not accepted.

- Exactly one accepted line: take the commit-SHA branch below with that SHA. Do not call `gh` again for this identifier. The reconciliation report's `> Merge:` value is that SHA. The report format already allows a commit SHA there; this spec does not change the report template. That line may be any ref `--all` walks, including a commit that is not an ancestor of `HEAD` or of `refs/remotes/origin/HEAD`. This spec does not add an ancestor filter.
- Zero accepted lines, more than one accepted line, or a non-zero exit from that `git log`: this is "finds nothing" (a non-squash or rebase merge, no such commit, or more than one commit that looks like the squash). Do not pick the newest. Print the existing step 1c prompt, unchanged: `Could not find merge commit for <TICKET-ID>. Enter PR number or commit SHA:`. Classify the answer the same way step 2 already classifies an identifier, and read it with this same step. No second warning, no attempt counter, no new prompt, no timeout. The automated search ends at that prompt; the operator ends it by supplying a SHA (or a PR number whose lookup succeeds).

**Commit SHA.** Unchanged: `git show --stat <SHA>`, then `git show <SHA>`. This branch does not call `gh`. A failing `git show` is unchanged too; this spec adds no fallback on the SHA branch.

The ">500 lines" sentence applies to whichever diff was actually read.

The failure-mode bullet "Merge commit not found" (line 440) describes step 1 and is left as written. Step 2's degrade is stated only in step 2.

### Tool-use notes

Replace the line-430 bullet with the sentence in Decision 3. The clause sits on the `gh pr view` / `gh pr diff` sentence. The SHA path's lack of `gh` is that clause, not a new bullet.

### Test

Inside `test_requires_block_matches_the_tool_use_notes`, after `self.assertIn("shared-memory?", block)`, add:

```python
        self.assertIn("vcs-host?", block)
```

Same indent as the surrounding asserts. No new test method, no fixture, no change to `test_lint_is_clean_including_warns`.

No new persisted state. No new preflight step.

## Test plan

Mechanical gate (the `## Test command` below):

1. `python tests/test_spec_close_log.py` exits 0. `TestSkillDeclaration.test_requires_block_matches_the_tool_use_notes` includes `assertIn("vcs-host?", block)` and still passes the pins that were already there.
2. `python lint.py --strict` exits 0, and stderr contains `lint: 0 error(s), 0 warning(s)`.
3. `skills/spec-close/SKILL.md` contains the exact line `  services: [issue-tracker?, shared-memory?, vcs-host?]`.
4. `git diff --name-only origin/main` lists nothing outside `skills/spec-close/SKILL.md` and `tests/test_spec_close_log.py`.

Review checklist for the prose (not a second command):

- The PR-number bullet warns once, runs `git --no-pager log --exclude=refs/stash --all --format=%H%x09%P%x09%s -F --grep="(#<N>)"`, and takes the SHA branch only when exactly one line is a 40- or 64-character hex SHA, with exactly one parent, and a subject ending in ` (#<N>)`. A newer body mention, a revert subject, a stash, and a second matching subject do not win. Any other result prints the step 1c prompt unchanged.
- A unique accepted line is taken even when it is not an ancestor of `HEAD` or `origin/HEAD`.
- An empty or non-numeric `<N>` for which `gh` exits 0 is accepted as that other PR. No digits check is added.
- The line-430 bullet contains `` (`vcs-host?`; the SHA path needs no `gh`) ``.
- Phase 0 has no `gh` probe. The SHA bullet does not call `gh`.

## Test command

Run from the repo root in Git Bash. It must exit 0.

```
python tests/test_spec_close_log.py && python lint.py --strict && python lint.py 2>&1 >/dev/null | grep -q 'lint: 0 error(s), 0 warning(s)' && grep -qxF '  services: [issue-tracker?, shared-memory?, vcs-host?]' skills/spec-close/SKILL.md && git rev-parse --verify -q origin/main >/dev/null && test -z "$(git diff --name-only origin/main | grep -vxE '^(skills/spec-close/SKILL.md|tests/test_spec_close_log.py)$')"
```

## Done when

- `/spec-close`'s `requires:` block declares the `vcs-host` role with the marker that matches its behaviour (`vcs-host?`, with the PR-number fallback stated in the body), and lint and the spec-close tests pass. — Decisions 1–4; checked by test-plan items 1–3 and the review checklist.

## Out of scope

- Any other skill's `requires:` block, including `/ship-spec`'s required `vcs-host` and `/review-pr`'s `code-review-bot` (VHS-52).
- A preflight `gh auth status` probe in `/spec-close` (Decision 5). A timeout, an attempt counter, a stderr parser, or a second warning are the same kind of addition and are not added.
- Reordering or changing Phase 2a step 1's three merge-lookup strategies. Only step 2's PR-number path gains a stated fallback. The step 1c prompt text stays. How step 2 tells a PR number from a SHA is the skill's existing branch; this spec does not add a classifier.
- The "Merge commit not found" failure-mode bullet, the Bash Tool-use bullet, and every other line of `SKILL.md` not named in Scope.
- A fallback on the commit-SHA branch when `git show` fails.
- The portability contract and `lint.py`. `vcs-host` and the `?` suffix are already in the vocabulary.
- Wiki filemap and state lines.
- A second test assertion, a new test method, or a drift check beyond the one `assertIn` and the `## Test command` above.

## Deferred (P2+)

- edge-cases/R1/F-4 — The one warning line does not carry per-command exit status. Not folded: Decision 2 settles one line that names `gh`. Adding statuses is an observability change, not a fix for an observed wrong close.
- conventions/R1/F-2 — The test command allowlists the whole tree instead of path-scoping `git diff` the way VHS-51 does. Not folded: this run requires `git diff --name-only origin/main` to touch nothing outside the two files.
- correctness/R1/F-2 — The Plane ticket was not readable (namespace `skills` denied). No spec edit. The brief transcribes the Problem and Done when.
- edge-cases/R2/F-2 — Re-entry says both to read the answer with this step again and that the search ends at the prompt with no second warning. Not folded: ordering retry, a repeated warning, and "do not resubmit" is a control-flow change, not a wording clarification.
- edge-cases/R2/F-4 — A rejected two-parent subject is not echoed before the step 1c prompt. Not folded: the prompt text stays as Decision 2 left it, and naming the rejected SHA is an extra line.

## Post-green polish

- edge-cases/R1/F-2, edge-cases/R2/F-1 — § Design and § Test plan: an empty or non-numeric `<N>` for which `gh` exits 0 is that other PR and is not a fallback case. States the exit-0 rule already in the step. No digits check.
- edge-cases/R2/F-3 — § Design and § Test plan: a unique accepted line may be any ref `--all` walks, including one that is not an ancestor of `HEAD` or `origin/HEAD`. States the command already specified. No ancestor filter.
