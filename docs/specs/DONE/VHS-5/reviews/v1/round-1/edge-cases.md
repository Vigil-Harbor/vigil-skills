# Edge-Cases Review — round 1

## Closure of round N-1 findings

N/A — round 1.

## Findings

### F-1: Test command's `grep -c "intervals are aspirational"` is brittle against future doc-touches
**Severity:** P2
**Where:** spec.md:159 (Test command), spec.md:134–135 (Cross-edit consistency note)
**Edge case:** The spec hard-codes `test "$(grep -c 'intervals are aspirational' skills/review-pr/SKILL.md)" = "3"` as a "Done when" criterion. The phrase is intentionally repeated three times across Phase 6a, 6d-Phase-1, 6d-Phase-2. If a future unrelated edit (typo fix, wording polish, or a fourth polling section added in a sibling spec) changes the count to 2 or 4, the test command fails even though the P2 fix is still semantically correct.
**What happens:** False-negative on the test gate. A reviewer or future maintainer running `/ship-spec` re-validation gets a `RED` from a structurally fine change. The single-character delta is `=` versus `-ge`.
**Why the spec misses it:** § "Cross-edit consistency" acknowledges the verbatim repetition is intentional but never reasons about what happens when the count drifts. The test command treats "3" as load-bearing when it is really a floor.
**Suggested fix:** Either change the assertion to `-ge "3"` (matches the other "at least N" probes in the same test command for `--name-only` and the new `"coderabbitai")`), or keep `= "3"` and add a one-line note in § "Cross-edit consistency" that future edits which change this count must update the test command in lock-step. The `-ge` option is simpler and matches the pattern of the other assertions in the line.

### F-2: Test command relies on bash + GNU grep + UTF-8 LF — does not enforce that contract
**Severity:** P3
**Where:** spec.md:158–164 (Test command + the "Run via Bash tool, not PowerShell" note)
**Edge case:** The Test command uses `test "$(...)"` POSIX semantics and GNU `grep -c` with BRE escaping (`\[bot\]`). Verified empirically: bash 5.2 (msys) + grep 3.0 + LF line endings handle this correctly on this machine, and `grep -c` returning exit-1-when-count-is-0 is harmless because command substitution captures stdout regardless. However, the spec only mentions "Run via Bash tool (not PowerShell)" as prose. If a future runner pipes this through `cmd.exe`, MSYS without `grep`, or PowerShell's `Select-String` shim, the BRE escapes and `test` syntax silently fail.
**What happens:** The whole assertion chain short-circuits at the first `test` and exits 0 (or errors with a parse failure), depending on shell. False positive (PowerShell would not even parse `&&` chains the same way).
**Why the spec misses it:** The spec author trusts the orchestrator to obey the "Run via Bash tool" note. That trust is reasonable for `/ship-spec`, but the test command is also the kind of thing future readers cut-and-paste into ad hoc shells.
**Suggested fix:** Add `#!/usr/bin/env bash` (or `bash -c '...'`) framing at the top of the test command block, or wrap the whole thing as `bash -c "..."`. Alternatively, change the prose to "MUST run via bash; failure to do so silently passes." Low-priority because the orchestrator does run it via Bash.

### F-3: "Pre-existing count is 7" claim is not version-pinned and can drift between spec write-time and ship-time
**Severity:** P2
**Where:** spec.md:143 (Test plan, structural item 2) and spec.md:162 (Test command rationale)
**Edge case:** The spec asserts the pre-edit count of `"coderabbitai[bot]"` is exactly 7, post-edit is 6. Verified on `HEAD` today (grep -c returns 7). But if another commit lands on `main` before this spec ships and changes any of the six REST-side filters (e.g., consolidates lines 158/168 into one call), the pre-edit count is no longer 7 and the post-edit assertion `= "6"` becomes wrong.
**What happens:** Spec ships, agent applies the single P0 edit correctly, test command fails because `grep -c` returns 5 (or 7 if a sibling added a filter), the implementer goes hunting for a bug that does not exist.
**Why the spec misses it:** The Test command bakes in an absolute count rather than a delta (pre-count minus 1). The skill source is a moving target; the spec snapshot is from one read of HEAD.
**Suggested fix:** Change item 2 of the structural assertions to a delta: capture the count before the edit, assert after-count equals before-count minus 1. Or, more conservatively, rebase the count in the Test command immediately before applying. The most resilient assertion is `test "$(grep -c '"coderabbitai\[bot\]"' skills/review-pr/SKILL.md)" -ge "1"` combined with `test "$(grep -c '"coderabbitai")' skills/review-pr/SKILL.md)" -ge "1"` — the existence of both forms confirms the edit landed without pinning a precise count.

### F-4: Test command does not guard against the explanatory note re-introducing the `[bot]` literal
**Severity:** P3
**Where:** spec.md:75–77 (the new clarifying note above the edited code fence)
**Edge case:** The note text reads: "GitHub's GraphQL API returns `coderabbitai` for the bot login (no `[bot]` suffix). The REST API used elsewhere in this skill returns `coderabbitai[bot]`." That second sentence contains the literal string `coderabbitai[bot]` inside a backtick. If the implementer writes the note with double-quotes around the bot login (rather than backticks), the count of `"coderabbitai[bot]"` jumps to 7 and the test command fails. The current note as written uses backticks, but the spec text mixes both backtick and double-quote usage in adjacent paragraphs, so a careful reader might "fix" punctuation in either direction.
**What happens:** Reviewer applies the edit using double-quotes around the REST form in the explanatory note (intuitive for "scare-quoting" a literal), test command fails on the post-edit `= "6"` assertion, debugging loop.
**Why the spec misses it:** § "Design / P0 edit" prescribes the note text but doesn't constrain its punctuation. The test command then becomes sensitive to punctuation in the prose, not just the code.
**Suggested fix:** Add an explicit instruction in the Design block: "When writing the explanatory note, use backticks (not double quotes) around `coderabbitai[bot]` so the post-edit count of the double-quoted literal stays at 6." Or change the test assertion to `-ge "6"` so an extra accidental occurrence is tolerated.

### F-5: No fallback if `gh pr diff <N> --name-only` has its own edge behaviors (large PRs, no-access)
**Severity:** P3
**Where:** spec.md:33–42 (Decision 2 — P1 `gh pr diff` replacement)
**Edge case:** Probe items in the brief flag (a) PR with zero file changes, (b) PRs requiring pagination, (c) PR the user does not have access to. Empirically `gh pr diff` does not paginate via `--name-only` (it streams the full diff and gh extracts names), but on inaccessible PRs gh exits non-zero with an error to stderr. The replaced command is bare (not chained with `||`), so a non-zero exit in Step 1 prints an error and continues — same surface as the current `--stat` bug, just a different error message.
**What happens:** On inaccessible PRs, Step 1 prints "gh: Not Found (HTTP 404)" and the skill keeps going to Step 2 where the same auth issue will fail more loudly. Cosmetically noisier than necessary; no data loss.
**Why the spec misses it:** Brief Decision 2 frames `--name-only` as "lower overhead" and considers cross-platform availability (`diffstat` on Windows) but does not consider failure modes of the replacement itself. Out-of-scope for "fix three named bugs" but worth flagging.
**Suggested fix:** Add a one-liner in § "Out of scope" or § "Decisions / Decision 2": "Failure modes of `gh pr diff --name-only` itself (auth, deleted PRs, etc.) are intentionally not handled — those surface again in Step 2 with the same error, where they are already documented." This makes the deliberate non-handling visible.

### F-6: Polling cadence rewrite leaves "after the polling window" wording in some places and not others
**Severity:** P3
**Where:** spec.md:115–121 (Location B alignment) and the **un-aligned** Phase 6a "extend the wait to 10 minutes total" leftover
**Edge case:** The spec catches the "after the 2-minute polling window" phrase in Location B and rewrites it to "after exhausting the polling attempts." Good. But Location A's new wording still says "extend to a further 10 attempts" without saying when. The original said "extend the wait to 10 minutes total" — a wall-clock claim. The replacement says "extend to a further 10 attempts" which mixes attempt-count framing with a magnitude that came from wall-clock arithmetic (5 min + 5 min). A reader sees "10 then a further 10" and reasonably asks "what does the second 10 buy me if attempts are sub-second?" The spec § P2 explicitly says intervals are aspirational because tool calls fire back-to-back — so "extend by 10 more attempts" buys ~0 additional real time.
**What happens:** Reader confusion. The skill remains correct; the documentation tells a story that doesn't quite hang together. No functional consequence.
**Why the spec misses it:** The spec author preserved attempt counts verbatim (good) but did not reason about whether "10 then 10 more" is still meaningful in attempt-count framing. With sub-second polls, 20 attempts is just "poll 20 times" — the "extend on still-in-progress" gates nothing useful.
**Suggested fix:** Either drop the "extend to a further 10 attempts" clause (simpler: just say "up to 10 attempts; if `gh pr checks <N>` still shows in_progress, report that and stop") or replace it with an attempt-count-meaningful gating ("on in_progress, double the attempt budget once"). Minor; ignore if the spec wants to preserve maximum continuity with the prior wording.

### F-7: No observability hook for polling-phase failures (gh rate-limit, network blip)
**Severity:** P3
**Where:** spec.md:97–131 (P2 polling rewrites)
**Edge case:** The probe asks: what if `gh api` is rate-limited mid-poll? The spec does not introduce new error handling because the brief says not to. But the polling rewrite is the perfect insertion point for a tripwire-style log: "Poll attempt N failed with: <err>" so a debug session can see which attempt blew up. The current wording says "fires back-to-back" — fine — but offers no breadcrumb for the case where one of those Bash calls returns non-zero.
**What happens:** A flaky `gh api` invocation today silently moves to the next attempt because the polling loop is unrolled into individual Bash tool calls and there is no aggregated error pickup. With sub-second cadence, 10 attempts of `gh api` against a rate-limited endpoint = 10 consecutive 429s in <2 seconds, exhausting the budget for nothing.
**Why the spec misses it:** Brief Decision 4 explicitly forbids new error branches, so the spec author chose not to add error reporting. Reasonable, but worth surfacing: the "intervals are aspirational" reframe doubles down on this gap because sub-second cadence makes transient errors hit the cap immediately.
**Suggested fix:** Out-of-scope for VHS-5 per Decision 4 — note as a follow-up. If the spec wants to address it: add one sentence to each polling block saying "If a poll's `gh api` call returns non-zero, record the error and count it as one attempt." No code change, just a documentation guard.

### F-8: `python sync.py status` is asserted to "exit clean" but its actual exit behavior is unverified
**Severity:** P3
**Where:** spec.md:142, spec.md:159 (Test command chains with `&&`)
**Edge case:** The first assertion in the test command is bare `python sync.py status` (no `--check` flag, no `; test $? = 0` wrapper). If `sync.py status` always exits 0 regardless of drift (it just prints a diff), then the `&&` chain proceeds even when the repo and `~/.claude/` mirror disagree. The spec's "Done when" item 5 (post-`python sync.py push`, status reports clean) and Test command both depend on `sync.py status` having a non-zero exit when drifted. That is a `sync.py` implementation detail not visible from the spec.
**What happens:** Silent pass on a drifted mirror. The Test command claims green; the actual ~/.claude/ mirror remains stale because the agent never ran `push`.
**Why the spec misses it:** The spec takes `sync.py status`'s exit semantics as given. Not unreasonable — but the gate is load-bearing for "Done when #5" and the spec does not cite evidence for the exit behavior.
**Suggested fix:** Add a one-line note: "Assumes `python sync.py status` exits non-zero on drift. If it exits 0 unconditionally, replace this assertion with `test -z \"$(python sync.py status)\"` or equivalent." Cheap insurance against a brittle gate.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 6 | P4: 0

STATUS: GREEN
