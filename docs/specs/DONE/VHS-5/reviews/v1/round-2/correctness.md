# Correctness Review — round 2

## Closure of round 1 findings

| ID  | Severity | Status | Evidence (spec section/line) |
|-----|----------|--------|------------------------------|
| F-1 | P1       | CLOSED | Test command (line 159) drops the `python sync.py status &&` clause entirely. § Test plan (lines 142-147) replaces the absolute-count claim with positive-presence `-ge 1` and adds an explicit "Note on `python sync.py status`" paragraph (lines 147) explaining why it is omitted. Done-when #5 (line 172) is reframed as a post-`sync.py push` manual check, explicitly outside the Test command. |
| F-2 | P2       | CLOSED (by acknowledgment) | Test command (line 159) still uses `&&` chaining without labeled echoes, but the surrounding paragraph at line 164 acknowledges the diagnostic limitation: "If an assertion fails, the `&&` chain returns the failing clause's exit code; re-run individual clauses to identify which check fired." Round 1 marked this P2 (polish, doesn't block); the spec author chose to acknowledge rather than restructure, which is acceptable for P2. |
| F-3 | P3       | CLOSED | Done-when #4 (line 171) now reads "`git diff --name-only <merge-base>..HEAD` on the implementation branch lists exactly that path" with a parenthetical noting that `/ship-spec` cuts an isolated worktree from main and that the merge-base ref at implementation time is main's tip. Matches the round-1 suggested fix verbatim. |
| F-4 | P3       | CLOSED | § Test plan #1 (line 142) reframes from absolute `= "6"` (suffixed-count minus 1) to positive presence: `grep -c '"coderabbitai")'` returns at least 1, with a rationale clause: "more resilient than an absolute count of the suffixed form, which could shift if an unrelated commit adds or removes a REST literal elsewhere in the skill". Test command at line 159 uses `-ge "1"` consistent with this. |
| F-5 | P3       | CLOSED (by acknowledgment) | The close-paren pattern is retained at line 159 and Test plan #1 (line 142), but the spec author has implicitly accepted the fragility (the proposed P0 edit is a one-character delete — round 1 noted "low risk because the proposed edit is one-character"). Round 1 also explicitly offered "leave as-is and accept the fragility" as one of two acceptable resolutions. Acceptable for P3. |

All five round-1 findings are now resolved (three CLOSED by edit, two CLOSED by author acknowledgment of acceptable trade-off).

## Grounding verification

Re-verified against current HEAD `skills/review-pr/SKILL.md`:

- Line 40: `gh pr diff <N> --stat` — confirmed present (target of P1 edit).
- Line 171: Phase 6a polling cadence "Check every 30 seconds, up to 5 minutes (10 attempts)" — confirmed (target of P2 edit, location A).
- Line 241: jq filter `select(.comments.nodes[0].author.login == "coderabbitai[bot]")` — confirmed (target of P0 edit).
- Line 252: Phase 6d Phase 1 "Check every 15 seconds, up to 2 minutes" — confirmed (target of P2 edit, location B).
- Line 254: "If after the 2-minute polling window..." — confirmed (secondary P2 edit, location B).
- Line 279: Phase 6d Phase 2 "every 20 seconds, up to 3 minutes" — confirmed (target of P2 edit, location C).
- Only one `--stat` occurrence in SKILL.md (line 40); `--name-only` is absent. The Test command's assertion #2 (`grep -c -- '--stat' = "0"`) and assertion #3 (`-ge "1"` for `--name-only`) are both satisfiable by the proposed P1 edit alone. No incidental `--stat` substrings — the other `stat` tokens are `state`, `status`, `submitted_at` which do not contain the leading `--`.

## Findings

No new findings.

The spec's four test-command assertions (P0 GraphQL presence, P1 `--stat` absence, P1 `--name-only` presence, P2 "intervals are aspirational" count >= 3) all map cleanly to the proposed edits with no overlap or gap. Manual checks cover the end-to-end paths the structural greps cannot reach.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 0 | P4: 0

STATUS: GREEN
