# VHS-6 Round 2 — Correctness Review

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `git symbolic-ref --short` returns wrong format | CLOSED | spec line 98: long-form + `sed 's|^refs/remotes/upstream/||'` matching ship-spec SKILL.md:32 |
| correctness | F-2 | D4 regex vs step 4d extension list mismatch | CLOSED | spec D4 line 47 now lists identical extensions as step 4d line 110 |
| correctness | F-3 | Brief acceptance criterion about actual run log output unmapped | CLOSED | spec Done-when #12 (line 245): "Empirical validation (tests 6-8) produces verifiable log output" |
| correctness | F-4 | `AskUserQuestion` is not a real tool | CLOSED | spec D6 line 63: "conversational prompt, not tool call"; step 4g uses numbered-options + "Wait for the user's response" |
| correctness | F-5 | Test command coverage gap | CLOSED | spec lines 224-230 acknowledge no executable test suite |
| correctness | F-6 | Step 4h redundant | CLOSED | step h eliminated; behavior folded into 4e empty-result branch |
| correctness | F-7 | "stdin halt" terminology in D6 | CLOSED | D6 title: "conversational prompt, not tool call" |
| edge-cases | F-1 | symbolic-ref format bug | CLOSED | same fix as correctness F-1 |
| edge-cases | F-2 | No timeout on git fetch | CLOSED | spec line 104: `timeout 30 git fetch upstream` |
| edge-cases | F-3 | AskUserQuestion not real | CLOSED | same fix as correctness F-4 |
| edge-cases | F-4 | BRE alternation not portable | CLOSED | spec line 124 and D8: `--extended-regexp` with ERE `|` |
| edge-cases | F-5 | Single-tier query handling undefined | CLOSED | spec step 4e: explicit "only if" conditions |
| edge-cases | F-6 | Windows path separators | CLOSED | deferred to P2+ section |
| edge-cases | F-7 | Fetch failure log misleading | CLOSED | spec line 106: "proceeding with available refs" |
| edge-cases | F-8 | Step 4f flow diagram | CLOSED | deferred to P2+ section |
| conventions | F-1 | AskUserQuestion not a Claude Code tool | CLOSED | same fix as correctness F-4 |
| conventions | F-2 | symbolic-ref approach inconsistent | CLOSED | spec line 98 uses same long-form + sed pattern |
| conventions | F-7 | Step 4h could be removed | CLOSED | step h removed |

## Findings

### F-1 (P2): Done-when #1 parenthetical lists 8 items for 7 sub-steps

Done-when #1 says "sub-steps a–g" (7 letters) but the parenthetical lists 8 activities. The 8th item ("clean/skip logging") is distributed across sub-steps, not a distinct sub-step. Cosmetic mismatch.

### F-2 (P3): Brief idempotency criterion not mapped

Brief acceptance criterion calls for "re-run produces the same result." The design inherently satisfies it (git fetch idempotent, queries deterministic for a given ref state) but Done-when doesn't explicitly claim it.

### F-3 (P3): Plane ticket not in MCP memory cache

`memory_search` for VHS-6 returned zero results. Review used the brief as authoritative source.

STATUS: GREEN
