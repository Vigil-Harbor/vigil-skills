# VHS-5 — Fix review-pr skill bugs found during VHS-3 review run

## Context

The `/review-pr` skill (`skills/review-pr/SKILL.md`) was exercised end-to-end against the VHS-3 PR. Three bugs surfaced — one silently breaks the thread-resolution polling phase, one prints a CLI error on every run, and one is a documented-but-unenforced timing claim. Fixing them in a single pass keeps the skill credible the next time it ships against a real CodeRabbit-reviewed PR.

The skill source-of-truth is `skills/review-pr/SKILL.md`. Edits there must be pushed back to `~/.claude/skills/review-pr/` via `python sync.py push` after merge — but that's a workflow detail for the human running `/ship-spec`, not part of the spec scope.

## Problems

### P0 — GraphQL thread-resolution query silently returns zero threads

In Phase 6d (`SKILL.md` ~line 241), the GraphQL `reviewThreads` query filters threads by author login:

```
select(.comments.nodes[0].author.login == "coderabbitai[bot]")
```

GitHub's **GraphQL** API returns `coderabbitai` for that bot's login (no `[bot]` suffix). GitHub's **REST** API — which the rest of the skill uses — returns `coderabbitai[bot]`. The filter therefore matches nothing under GraphQL, and the skill concludes "0 CodeRabbit threads, all resolved" regardless of actual state. This silently undermines the entire Phase 2 verdict-polling decision tree, because Phase 2 entry is gated on "all CodeRabbit threads resolved."

This is the highest-severity bug because it produces a wrong-but-plausible answer with no error signal.

### P1 — `gh pr diff --stat` is not a valid invocation

Step 1 (`SKILL.md` ~line 40) calls:

```
gh pr diff <N> --stat
```

`gh pr diff` does not accept `--stat`. The call errors out on every run. The intent is "show the PR's file/line scope to contextualize findings during triage" — there are working alternatives (`--name-only`, or piping the unified diff through `diffstat`), but neither is currently in the skill.

### P2 — Polling cadence claims are not enforced

Phases 6a, 6d-Phase-1, and 6d-Phase-2 each instruct the agent to "check every 30/15/20 seconds" via individual Bash tool calls. In practice, agent tool calls fire back-to-back with no delay, so the documented cadence has no real-world effect — the polls complete in seconds, not the documented 2–5 minutes. Either the cadence should be enforced (e.g., `sleep N && <command>`) or the documentation should acknowledge that the interval is aspirational and the timeout governs total attempts, not wall-clock duration.

## Decisions carried forward

1. **P0 fix uses the GraphQL-correct login.** The filter must match `coderabbitai` (the GraphQL value). Picking the right value is non-negotiable; whether to also drop the suffix check entirely vs. accept both forms is the spec author's call, but the GraphQL path must work.
2. **P1 fix preserves the original intent.** The Step 1 `gh pr diff` call exists to give the triage step a sense of the PR's scope. The replacement should still convey "what files / how many lines changed" — `--name-only` is the lower-overhead option, `diffstat` is the higher-fidelity option. Spec author picks one with one-line rationale.
3. **P2 fix is a binary doc-vs-enforce choice.** Either add `sleep N &&` prefixes (and accept that bash tool calls block) or rewrite the cadence wording to "the timeout governs total attempts; intervals are not enforced." Pick the option that's cheaper to maintain — both are acceptable.
4. **No broader skill restructuring.** This is a targeted bug-fix pass. Resist the urge to reorganize Phase 6 or rewrite the polling logic from scratch.

## Done when

1. The 6d GraphQL query returns the expected CodeRabbit threads when run against a PR that has any (manually verifiable: paste the query into `gh api graphql`, confirm non-empty `threads`).
2. The Step 1 `gh pr diff` invocation runs without error and produces output that supports triage scope-awareness.
3. The 6a / 6d cadence text either matches actual runtime behavior (intervals enforced) or the wording is revised to reflect that intervals are not enforced.
4. `skills/review-pr/SKILL.md` is the only file changed in scope (plus possibly a comprehension entry or wiki update — see Out of scope).
5. After `python sync.py push`, `python sync.py status` reports clean.

## Out of scope

- Restructuring `/review-pr` beyond the three named bugs (no Phase 6 redesign, no new triage logic, no new error-handling cases).
- Changes to `/spec-cycle`, `/ship-spec`, or the reviewer subagents.
- Changes to `sync.py`, `states.json`, or anything outside `skills/review-pr/`.
- Adding tests — this repo has no test suite (per `CLAUDE.md`: "no build step, no test suite, no dependencies beyond Python 3.8+ stdlib"). Verification is by reading the diff and, ideally, dry-running against a live PR.
- Wiki updates beyond what `/wiki-after-merge` produces post-merge.

## References

- Plane: VHS-5 (`401bddd2-6d35-48e4-9c4e-e6d4fbec819d`)
- Skill: `skills/review-pr/SKILL.md`
- Origin: bugs surfaced during the VHS-3 review-pr dry run
