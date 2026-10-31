---
name: ship-spec
description: Implement a green-lit spec in an isolated git worktree, through a test gate and a review gate, then open a PR and update the issue tracker. `--build-only` stops before review; `--from-review` continues on an existing worktree. After the PR merges, run /spec-land, then /spec-close.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: true
  subagents: optional
  services: [vcs-host, issue-tracker?]
---

# /ship-spec — implement a green-lit spec

```text
/ship-spec <spec-path> [--build-only | --from-review <worktree-path>]
```

Default runs Phases 0–7. `--build-only` runs Phases 0–3 and stops before Phase 3b: no review, commit, push, PR, SHA marker, or tracker write. `--from-review` runs Phase 0, the worktree check, then Phases 3–7, and skips Phases 1 and 2. Both flags, `--from-review` with no path, or any other flag halts with `Usage: /ship-spec <spec-path> [--build-only | --from-review <worktree-path>]` and writes nothing. `--build-only` takes no path.

A host that cannot wait prints the prompt and stops. It does not commit, roll the branch back, or delete, reuse, or rename a branch or worktree, and it does not take a numbered option whose text does one of those.

## Modes

**Build-only.** Phase 1 still cuts `<project-root>/../<TICKET-ID>-worktree` on a new branch from `origin/<default-branch>`. After Phase 3 is green, or skipped because the test command is `N/A`, print the branch, the worktree path, and `/ship-spec <spec-path> --from-review <worktree-path>`, then stop. A red test halt is still the Phase 3 halt. A red verdict still halts in Phase 0, before the worktree exists.

**Start-at-review.** After Phase 0, before Phase 3, check the path against that porcelain list. The primary checkout is its first `worktree` record. The argument must be a later `worktree` record: a linked worktree of this repository, not the primary checkout. Resolve both to absolute paths, strip a trailing separator, treat slashes alike, and on Windows compare case-insensitively. Print both strings on failure. Its `branch` line must be `refs/heads/<name>`, and `<name>` must not equal the default branch from step 5. Stop and do not commit when the path is missing, is the primary checkout, has no `branch` line, or is on the default branch. Name which of those four failed. If `<name>` does not contain the lowercased ticket id, warn, naming both, and continue.

Phases 3–7 use that worktree as cwd. The branch is `git -C <path> branch --show-current`. Do not form a branch and do not run `git worktree add`. The spec stays the absolute path from Phase 0. After the check and before Phase 3, `git fetch origin <default-branch>`. A failed fetch, or a missing `origin/<default-branch>`, stops before Phase 3 and commits nothing. Then classify both artifact paths, cwd the linked worktree, and hold the primary checkout for the copy. Run Phase 3 before Phase 3b unless the command is `N/A`; then skip the command and enter Phase 3b. The review diff is uncommitted changes plus `origin/<default-branch>...HEAD`, not a two-dot diff.

## Phase 0 — Preflight

Before any worktree work. Set each script's path and interpreter in the same shell call as the command.

**Paths.** Primary checkout: the first `worktree` record of `git worktree list --porcelain`. Spec and marker are absolute paths under it. With forward slashes, the spec path must end in `docs/specs/TODO/<TICKET-ID>.spec.md`. The ticket id is that filename minus `.spec.md`, uppercased, matching `^[A-Z][A-Z0-9]*-[0-9]+$`. Do not strip only `.md`. Halt if the file is missing, the path does not end that way, or the id does not match. Marker: `<primary>/docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`. Pass both absolute paths to `read`. An absent marker is `missing`: warn and continue.

**Sections.** Halt, naming the heading, when no unfenced line is, after at most three spaces, exactly `## Done when`, and the same for `## Test plan`. A fence is a line of three or more backticks or tildes, not prefixed `> `; it opens only when none is open and closes on the same character at least as long. Do not also require Goal, Scope, Design, or Test command.

**Tier.** Ignore fenced lines and lines prefixed `> `. The first remaining line that, after indentation, starts with `**Tier:**` (case-insensitive) wins. A second warns `tier: multiple Tier lines in the spec — using first`. Trim and lowercase the value. `small`, `big`, and `irreversible` are the tier. Any other value, including empty, warns `tier: malformed (<value>) — using big` and the tier is `big`. No label line is `big`, with no warning. Do not read the brief. Do not halt on the tier.

**Marker.** `--marker` and `--spec` are those absolute paths. The plain-text `verdict: red` read, when it runs, opens that same file.

```bash
VERDICT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-cycle/scripts/verdict_marker.py"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
"$PY" "$VERDICT" read --ticket <TICKET-ID> --marker <absolute-marker> --spec <absolute-spec> --spec-tier <spec tier>
```

`verdict_marker.py` owns the format, the fingerprint, and the six states. Do not restate them. A missing script or a non-zero exit is `unreadable` (`script missing — run python sync.py install`, or `verdict_marker.py exit <n>`). Only then, a first plain-text `verdict:` line of `red` takes the red halt. Exit-0 JSON `unreadable` or `missing` does not get that second read.

- `green`: continue. PR line `- [x] Spec verdict: green (<kind>, <date>)`, kind and date from the JSON (`no date` when absent).
- `red`: halt with the block below, whether or not the spec changed. Do not create a worktree. Do not commit.

```text
SPEC VERDICT: red (round <round>, gate <gate>, <date>).
/ship-spec does not implement a red spec.
Get a green verdict first: re-run /spec-cycle, or record your own review with
  /spec-cycle <spec-path> --attest "<reason>"
```

- `missing`, `unreadable`, `pending`, `changed`: print `SPEC VERDICT: <state> — <one line>` and continue. Do not ask Proceed/Stop. PR line: `- [ ] Spec verdict: <state> — proceeded without a green verdict`. When `changed` and `cause` is `tier`, name `marker_tier` and the spec tier and say the gate follows the spec tier. When the spec has no label line, say the spec tier is `big` because no line was recorded. Phase 3b uses the spec tier, not the marker's `tier:`. Do not rewrite the marker.

2. A missing brief warns once. Use the spec alone.
3. Read `CLAUDE.md` and `AGENTS.md` when each exists. Both are Phase 2's guardrails.
4. **Test command.** The spec's `## Test command`, verbatim. Body, fences stripped and trimmed, equal to `N/A` (case-insensitive) skips the Phase 3 command only. Phase 3b still runs, except `--build-only`, which stops before it. With no such section, use CLAUDE.md "Build & Run". If neither yields a command, halt. No AGENTS.md fallback.
4b. **Review command.** The first `## Review command` in the spec, else `CLAUDE.md`, else `AGENTS.md`. After fences are stripped, the body must be exactly one non-blank line. Empty or several lines: warn, name the file, try the next source. None is fine.
5. **Default branch.** Halt if both commands return empty. This step number stays; spec-land cites it.

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|^refs/remotes/origin/||'
git remote show origin | sed -n '/HEAD branch/s/.*: //p'
```

6. `gh auth status`. Halt if it fails.
7. **states.json.** Read `"${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/ship-spec/states.json"`. Not the copy in the target repo. A missing, unreadable, or invalid file, or a prefix that is not a key: warn and skip Phase 6. Do not halt. A missing or empty `review_state_id` does not skip the phase; Phase 6 skips the flip and still comments when the tracker answers.

One preflight line: verdict state (and, for green, its kind), tier, and mode (`default`, `build-only`, or `from-review`).

## Artifact rule

Classify once per invocation, after the worktree cwd is known and before Phase 4. Default and `--build-only` do it at the end of Phase 1. `--from-review` does it after its check. Do not classify again. Later phases say "place it by the artifact rule."

Paths: `docs/specs/TODO/<TICKET-ID>.test-output.txt` and `docs/specs/TODO/<TICKET-ID>.review.md`. Classify each once, even if absent:

```bash
if git check-ignore -q -- <path>; then rc=0; else rc=$?; fi
echo "classify: <path> exit $rc"
```

Exit 0 is `ignored`. Exit 1 is `not-ignored`. Any other exit, or a command that cannot run, stops before a later phase stages or copies anything.

In Phase 4, before `git commit`, place only a file this invocation wrote:

- `not-ignored`: `git add <path>` in the worktree.
- `ignored`: do not `git add` it, and do not `git add -f`. Copy to `<dest>`, which is `<primary>/docs/specs/TODO/<file>`. First, `git -C <primary> ls-files --error-unmatch -- <dest>`, stderr discarded, captured the same way. Exit 0 (tracked): print both paths and stop before the commit. Exit 1: create parents if needed, write a temp file in that directory, and replace the destination even when an older untracked file is there (`os.replace`, or the host equivalent). A failed replace stops and leaves the previous bytes. Any other exit, or a failed copy: print the paths and stop. Leave the worktree copy. `<primary>` is Phase 0's first porcelain `worktree` record, including a `--from-review` run that never leaves the linked worktree.

On `N/A`, leave any test-output file, in the worktree or the primary checkout, as it is. A review file this invocation did not write is left alone.

The suffix, once, is ` (kept locally at <primary>/docs/specs/TODO/<file>; not in this commit)`. Append it only when this invocation wrote that file and the held result is `ignored`.

## Phase 1 — Worktree

Default and `--build-only` only. `--from-review` does not create a worktree.

The primary checkout changes only when the artifact rule copies an ignored artifact; git does not track that copy, and no other git state in the primary checkout changes. Elsewhere, the primary checkout changes only as the artifact rule says.

1. Branch `<type>/<ticket-id-lower>-<slug>`. `<type>` is `fix`, `feat`, or `chore`; if unsure, ask. `<slug>` is 3–5 lowercase hyphenated words.
2. Path `<project-root>/../<TICKET-ID>-worktree`.
3. Halt if the directory exists, or the branch exists locally (`git rev-parse --verify`) or on origin (`git ls-remote --heads`). Do not delete, reuse, or rename.
4. Create it. A non-zero fetch or `git worktree add` stops before Phase 2 and does not edit the primary checkout.

```bash
git fetch origin <default-branch>
git worktree add -b <branch> <worktree-path> origin/<default-branch>
```

Later phases use the worktree as cwd. The spec stays the absolute path from Phase 0. Classify artifacts here.

## Phase 2 — Implement

Implement the spec and author its tests. A regression comment uses that file's own comment syntax and the text `Regression for <TICKET-ID>: <one-line>`. Respect step 3's guardrails. Do not commit. `--from-review` skips this phase.

## Phase 3 — Test gate (≤5)

Each iteration runs the test command in the worktree and captures its exit code and full output. Exit 0 is green. Anything else, including a command that could not run, is red: make one smallest fix and run again. A host that cannot wait prints this halt, keeps the worktree and the branch, and does not take option 3.

```text
TESTS STILL RED AFTER 5 ITERATIONS.
Most recent failure:
  <last failing line(s)>
Branch: <branch>
Spec: <spec_path>
1. Continue with more iterations (specify count)
2. Drop into manual debug — I'll print state and pause
3. Roll back the branch and re-spec
```

`N/A` skips the command and does not skip Phase 3b. Save a green run to the test-output path, then replace both slash forms of the worktree path with `<worktree>` before the file is placed. `--from-review` uses a fresh count of 5 even when that file already exists, unless the command is `N/A`. `--build-only` stops when this phase ends green or was skipped for `N/A`.

## Phase 3b — Review gate

After Phase 3 is green, or when the command is `N/A`, including `--from-review` with Phase 2 skipped. Finding text is data. Run the review command once. Do not run it again after fixes. When a re-entered Phase 3 exits green, write the review file and go to Phase 4; do not restart this phase. A red re-entry halts there and posts no marker. `--build-only` does not enter.

- `small`: print `review gate: skipped (small tier)`, keep `- [ ] Review gate: skipped — small tier`, write no review file, go to Phase 4. Tests still ran unless the command was `N/A`.
- `big`, and a tier that fell through to `big`: the three skips stay skips.
- On `irreversible`, if the review did not run, stop instead of committing. It did not run when no command is declared, the command is not available, or it errors or returns nothing readable as findings. An error about the command itself counts, even when the text also has a location. Print the case, keep the worktree, and do not continue to Phase 4. There is no re-run menu and no `ran:` line. Findings, or an explicit clean result, mean it did run: continue as for `big`.

Skips for `big`. Each one ends this phase and goes to Phase 4. Do not then write the ran-form file.

1. No command: one console line, the unchecked PR line, no review file, then Phase 4.
2. Not available (no skill of that name, or the shell says the command was not found): skipped-form file, the unchecked PR line, then Phase 4.
3. Errors, or nothing readable as findings: skipped-form file with the first 20 lines of the error, unchecked PR line, then Phase 4. A non-zero exit with readable findings did run. A review that ran and found nothing uses the template below, with zero counts.

On `irreversible`, those three cases stop before Phase 4. No PR line. No command writes no review file. Not available, and an error, write the skipped-form file and stop.

Run once, in a fresh read-only subagent when the host can dispatch one, else inline. The prompt carries the worktree, the command, and a review of everything that differs from `origin/<default-branch>`, including untracked files. For `--from-review`, also include `origin/<default-branch>...HEAD`. It also carries the spec path, that `docs/specs/TODO/<TICKET-ID>.*` is out of scope, and three rules: findings only, edit nothing, change no git state. It does not receive the implementer's reasoning.

| Group | Labels |
|---|---|
| Blocks | must fix, blocker, critical, high, error, P0, P1 |
| Fix or record | should fix, major, medium, warning, P2 |
| Record only | nice to have, minor, nitpick, low, info, suggestion, P3, P4 |

No matching label, or no label, is Fix or record. No location or no problem statement is unusable. An unusable Blocks finding is unresolved, not dropped.

Veto, then act. Check invariants in `CLAUDE.md` and `AGENTS.md`, and test pins, before a fix. Do not apply two fixes that break each other. Blocks is never declined: vetoed, out of scope, contradicted, or inaccurate is unresolved. Fix-or-record is applied, or recorded as vetoed, contradicts the spec, outside scope, or inaccurate. Record-only is not acted on. A veto counts as recorded.

Unresolved Blocks waits. Nothing is committed until the operator chooses. A host that cannot wait takes 3.

```text
REVIEW GATE: <n> blocking finding(s) not resolved.
  <number>. <title> (<location>) — <why not resolved>
Nothing is committed.
1. I will fix it by hand — pause; tell me when to continue
2. Override — commit with each finding above recorded as overridden
3. Abandon — stop here; the worktree is kept
```

1 records `fixed by operator`. 2 records `overridden by operator` (reason after the colon). 3 writes the file with those findings `unresolved` and stops.

If a fix landed and the command is not `N/A`, re-enter Phase 3 with a fresh count of 5. Do not review again. Do not undo a Blocks fix to reach green. A Fix-or-record fix may be reverted as `recorded: fix reverted, broke <test>`.

When the review ran, write `docs/specs/TODO/<TICKET-ID>.review.md` from the template, then place it by the artifact rule. A skipped-form file, written in the skip, omits Mode, Compared against, the count lines, and Findings. No findings: zero counts, then `## Findings` and `None.`

```markdown
# Review gate: <TICKET-ID>

- Command: <review_command>
- Mode: subagent | inline
- Compared against: origin/<default-branch>
- Result: ran | skipped — <reason>
- Error: <first 20 lines; only when the review failed>
- Blocks: <n> (<fixed> fixed, <op> fixed by operator, <ov> overridden, <un> unresolved)
- Fix or record: <n> (<fixed> fixed, <rec> recorded)
- Record only: <n>

## Findings

1. [Blocks | Fix or record | Record only | unusable] <title> — <location>
   Problem: <one or two lines>
   Disposition: fixed | fixed by operator | overridden by operator | unresolved | vetoed: <reason> | recorded: <reason> | not acted on
```

PR line: checked when the review ran, unchecked when skipped; append the suffix when this invocation wrote that file and its held result is `ignored`. Success: `- [x] Review gate: <command> — <b> blocking fixed, <s> other fixed, <r> recorded (<path or suffix>)`, plus ` — <ov> overridden by operator` when that count is above zero.

## Phase 4 — Commit

Stage by name every path `git status --porcelain -uall` lists, including untracked, deleted, and renamed paths. Skip ignored paths and the two artifact paths; those follow the artifact rule. A non-zero `git add` of an ignored artifact does not abort that rule. Never `git add -A`, `.`, or `-f`.

Write the message to a temp file outside the worktree, then place the two artifacts. Subject: `<type>(<ticket-id-lower>): <one-line, ≤72 chars>`, plus a short narrative. Do not hard-code a model attribution trailer. If the host's instructions name one, add that line; otherwise omit it. Nothing staged and `HEAD` not ahead of `origin/<default-branch>`: stop, do not push. Nothing staged and `HEAD` ahead: skip the empty commit and go to Phase 5. Otherwise `git commit -F` that file. Do not pass `--no-verify`.

## Phase 5 — Push and PR

`git push -u origin <branch>`. A rejected push halts. Do not force-push. An existing PR: print its URL, do not create another, append the section below with `gh pr edit --body-file` if the body has no `## Test plan`, and still post the marker and run Phase 6. Otherwise `gh pr create --title "<type>(<ticket-id-lower>): <one-line>" --body-file <file>`, with that file outside the worktree, same as the commit message. `<N>` is the pull number in that URL. If the URL has none, `gh pr view --json number --jq .number` for this branch only. A non-zero create or view, or no integer, halts before the marker and before Phase 6. Do not substitute the ticket's integer.

Body: Summary, Files changed, and `## Test plan`. Test plan has `- [x] <test command> — <N>/<N> pass (full output: docs/specs/TODO/<TICKET-ID>.test-output.txt)`, with the suffix instead of that path when the log is ignored. For `N/A`: `- [x] Tests: N/A — doc-only/ops-only change, no test artifacts produced`. Then the verdict line, the review line, and always `- [ ] Post-merge verification`. No harness trailer unless the host's instructions name one.

**SHA marker.** After the URL is taken, before Phase 6, even when this invocation wrote no review file. `passed` only when this invocation's review file has a line `- Result: ran`. Any other path, including a file left from an earlier run, is `skipped`. Do not pass `inconclusive` or `not-run`. `land_check.py` owns the format. Stdin from `/dev/null`:

```bash
LAND="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-land/scripts/land_check.py"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
if test -f "$LAND"; then if "$PY" "$LAND" post <N> --review <passed|skipped> < /dev/null; then rc=0; else rc=$?; fi; [ "$rc" -le 1 ] || echo "SHA marker: NOT posted (land_check.py exit $rc)"; else echo "SHA marker: NOT posted (script missing — run python sync.py install)"; fi
```

Exit 0 and 1 are the script's status lines. Any other exit is treated as 1. Every exit continues to Phase 6.

## Phase 6 — Issue tracker

Move the ticket to `review_state_id` and comment `PR opened: <pr-url>`. Say "the issue tracker". On failure, or when Phase 0 skipped this phase, print this and continue:

```text
Issue tracker skipped — no state update and no PR comment.
To complete manually:
  1. Move <TICKET-ID> to the review state
  2. Comment on the ticket: "PR opened: <pr-url>"
```

A missing or empty `review_state_id`: warn, print the state names, skip the flip, and still comment when the tracker answers.

## Phase 7 — Summary

Do not remove the worktree. Print the PR URL, spec path, branch, worktree path, one Tests line, one Review line, and the tracker result. Omit Tests when the command was `N/A`. An ignored artifact uses the suffix, not "staged in this commit". Point at `/review-pr` in the worktree, then `/spec-land` after merge (it removes the worktree) and `/spec-close`. When the marker post did not exit 0, print `SHA marker: NOT posted` and do not claim the record exists. The primary-tree line points at the artifact rule.

## Tool-use notes

- Read and write for implementation. Shell for git, `gh`, and the test command. No interactive git.
- The review runs in a read-only subagent when the host has one, else inline.
- `verdict_marker.py read` and `land_check.py post`. This skill reads the verdict marker and never writes it.
- Do not push to the default branch. Do not force-push unless the user asks. Do not pass `--no-verify`.
