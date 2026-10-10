# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1

## Grounding notes
- I read the spec, brief, CLAUDE.md (machine-local; it points to AGENTS.md), `lint.py`, `tests/test_lint.py`, `tests/test_spec_close_log.py`, `tests/test_session_handoff.py` (the WARN pin), `docs/portability-contract.md` §3, `docs/authoring-portable-skills.md`, and `skills/{ship-spec,review-pr,spec-close}/SKILL.md`.
- I ran the current `python lint.py`: 0 errors, 2 warnings (`missing-requires` on review-pr and ship-spec). `--strict` exits 0. This matches the spec's premise.
- Anchors I checked, all accurate:
  - `lint.py:45-48` (vocabulary; `vcs-host` and `code-review-bot` already in `SERVICES_VOCAB`)
  - `lint.py:103-108` (boolean branch)
  - `tests/test_spec_close_log.py:1059-1066` (backlog test) and `:1201-1203` (spec-close zero-WARN)
  - `docs/authoring-portable-skills.md:16` (template) and `:38-42` (promotion path)
  - `skills/ship-spec/SKILL.md:81` (`gh auth`), `:82` (preflight step 8, warn-and-proceed), `:317` (`gh pr create`), `:363-367` (Phase 6, Plane unreachable), `:413` (the Phase 3b Tool-use bullet, verbatim as Decision 6 quotes it)
  - `skills/review-pr/SKILL.md:83` ("No CodeRabbit reviews found" and stop)
- Both skills end their frontmatter with `user_invocable: true`, so Decision 1's placement works. `.gitattributes` forces LF on `*.md`, so the `$`-anchored greps in the test command will match. In `grep -q '^  services: \[vcs-host, issue-tracker?\]$'` (basic regex), `?` is literal, so it is correct. The leave-alone list in the test command plus ship-spec and review-pr accounts for all 11 shipped skill directories.
- Recent commits: `aad9971` (VHS-47) and `156d388` (VHS-46) both landed 2026-10-08, today, and touch `skills/ship-spec/SKILL.md` (and the VHS-46 one touches `tests/test_spec_close_log.py`). The spec already accounts for them (hash command at step 1b, the Phase 3b subagent/inline gate), so it is not planning around outdated code.
- Ticket: I did not retrieve VHS-51 from shared memory. The orchestrator said namespace `skills` is ACL-denied, so I used the brief as authority (F-5).
- Deferred section: none present, so there are no routing checks to run.

## Findings

### F-1: The rewritten promotion-path sentence claims the hook blocks missing-requires regressions; `--strict` never gates WARNs
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7; § Design › `docs/authoring-portable-skills.md`
**Claim:** "its 'Once step 1 is done' clause is rewritten as 'Every shipped skill carries a block, so `--strict` is clean and the hook blocks regressions.'"
**Why this is wrong:** `--strict` exits 1 only on ERROR. `lint.py:17` says "WARNs never affect exit", `lint.py:290` returns `1 if (strict and n_err > 0)`, and `docs/authoring-portable-skills.md:27,31` says "WARNs never gate". `--strict` was already clean before this change (I ran it: exit 0 with 2 WARNs). So "carries a block, so `--strict` is clean" does not follow. A new skill without a block raises only a `missing-requires` WARN, which a `--strict` pre-commit hook would let through. The real guard against a reopened backlog is Decision 9's unit-test assertion. The old wording had the same flaw, but the spec writes this sentence fresh, so the doc would make a false statement in new text. Implementation still works.
**Suggested fix:** Reword the step-1 text along these lines: "Install a pre-commit hook that runs `python lint.py --strict` … It blocks ERROR regressions. Every shipped skill now carries a block, and `tests/test_lint.py::test_shipped_skills_clean` fails if one goes missing (WARNs never gate `--strict`)."

### F-2: Decision 3 allows `shell: optional`, but the Hermes `shell` row is left mapping to a requirement
**Severity:** P2
**Where:** spec § Design › `docs/portability-contract.md` §3, "Hermes mapping" bullet; § Decision 3
**Claim:** "the row for `network`, `subagents`, `filesystem` gains to its Note: 'an `optional` boolean is not emitted as a requirement'."
**Why this is wrong:** `docs/portability-contract.md:100` maps `shell` to "a `terminal`-toolset requirement" in a row of its own. Decision 3 makes `optional` valid on `shell`, and Decision 2 / the new booleans bullet says `optional` "is never a pre-flight requirement". Read literally, the table then tells an adapter to emit a terminal requirement for `shell: optional`, which contradicts the new semantics. The note also lands in the one row where the contract already emits nothing ("no direct Hermes frontmatter equivalent"), and `filesystem` in that row is not a boolean. The brief wording ("the Hermes mapping table notes that an adapter treats `optional` as not gating") covers the table, not only that row.
**Suggested fix:** Also add to the `shell` row's Note: "`shell: optional` emits no terminal requirement". Or attach the note to the table as a whole, for example a sentence under it: "An `optional` boolean emits no Hermes gating key and is not enforced by the adapter's pre-flight."

### F-3: The lexical-rule edit puts booleans under "exactly (lowercase, unquoted)", but the lint accepts any case
**Severity:** P2
**Where:** spec § Design › `docs/portability-contract.md` §3, "Lexical rules, step 5"; § Design › `lint.py`
**Claim:** Step 5 "the remaining token must match the controlled vocabulary exactly" gains "(for a boolean key: `true`, `false`, `optional`)". The lint check stays `val.lower() not in ("true", "false", "optional")`.
**Why this is wrong:** Step 5 (`docs/portability-contract.md:87`) says matching is **exactly** (lowercase, unquoted). `lint.py:106` lowercases first, so `Optional` and `OPTIONAL` would lint clean. The parenthetical now explicitly brings boolean values under the lowercase-exact rule. For `true`/`false` that was arguably harmless (YAML booleans are case-tolerant). `Optional` is just a different string to a real YAML parser and to any adapter that compares against `optional`. The result is a new contract/lint mismatch on the value this ticket introduces.
**Suggested fix:** Pick one. (a) Make the boolean branch compare `val` without `.lower()` for `optional`, or for all three values, and add `subagents: Optional` as a second `requires-malformed` case. (b) Word step 5 so booleans are case-insensitive, for example "(for a boolean key: `true`, `false`, `optional`, case-insensitive)".

### F-4: Decision 9 says only spec-close pins zero WARN; session-handoff does too
**Severity:** P3
**Where:** spec § Decision 9
**Claim:** "Today only `spec-close` has such a pin (`tests/test_spec_close_log.py:1201-1203`)."
**Why this is wrong:** `tests/test_session_handoff.py:765-770` (`test_skill_lints_clean`) also asserts `[f for f in findings if f[0] == lint.WARN] == []` for `skills/session-handoff/SKILL.md`. This does not change the implementation.
**Suggested fix:** Say "Today only `spec-close` and `session-handoff` have such a pin (`tests/test_spec_close_log.py:1201-1203`, `tests/test_session_handoff.py:765-770`)."

### F-5: Ticket not retrieved
**Severity:** P3
**Where:** grounding step 3
**Claim:** n/a
**Why this is wrong:** The orchestrator said shared-memory namespace `skills` is ACL-denied for this agent, so I could not check the ticket's acceptance criteria against the brief. I used the brief's Done-when, and all three items map: Decision 1 → test-plan item 4; Decisions 1/3/9 → items 1 and 3; Decision 7 → items 2 and 5.
**Suggested fix:** None needed in the spec. The orchestrator may confirm the ticket's AC from the Plane tracker directly.

### F-6: The "see promotion path" pointer on the WARN rule loses its referent
**Severity:** P3
**Where:** spec § Design › `docs/authoring-portable-skills.md`
**Claim:** Only the template comment and § Promotion path change.
**Why this is wrong:** `docs/authoring-portable-skills.md:36` reads "**WARN `missing-requires`** — no `requires:` block (advisory; see promotion path)". Once step 1 is deleted, the promotion path no longer says anything about `missing-requires`, so the pointer goes nowhere.
**Suggested fix:** Change it to "(advisory; never gates `--strict`)", or drop the parenthetical pointer.

### F-7: The services-bullet splice ignores the existing ", etc."
**Severity:** P4
**Where:** spec § Design › `docs/portability-contract.md`, "Field semantics, services bullet"
**Claim:** "after '… `shared-memory` → the shared-memory/MCP service', add '`vcs-host` → …'"
**Why this is wrong:** The current text at `docs/portability-contract.md:65` continues "…the shared-memory/MCP service, etc." The instruction says nothing about the comma separator or where the trailing "etc." goes.
**Suggested fix:** Give the resulting sentence in full, for example "…`shared-memory` → the shared-memory/MCP service, `vcs-host` → the pull-request host and its CLI (GitHub via `gh`), `code-review-bot` → the review bot on that host (CodeRabbit), etc."

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 3 | P4: 1

STATUS: GREEN
