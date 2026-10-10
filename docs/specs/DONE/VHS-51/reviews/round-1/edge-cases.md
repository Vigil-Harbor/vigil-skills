# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1

Grounding notes:
- I read the spec, the brief, `lint.py`, `tests/test_lint.py`, `tests/fixtures/`, `tests/test_spec_close_log.py` (L1059-1066, L1185-1203), `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, and the frontmatter, Tool-use notes and Phase 3b text of `skills/ship-spec/SKILL.md` and `skills/review-pr/SKILL.md`.
- I also read the one live downstream consumer of `requires:`: `vigil-converter/src/converters/claude-to-hermes.ts` and `vigil-converter/HERMES-MAPPING.md`. The repo is out of scope for edits, but it is the failure axis for the new values.
- I skipped the Plane ticket lookup, because the `skills` memory namespace is ACL-denied for this agent, as the caller said. I worked from the brief.
- The spec has no `## Deferred — follow-up required` section, so there are no routing checks to run.
- Persistence checklist: N/A. The spec adds no persisted state.
- I ran `python lint.py` read-only. It reports `0 error(s), 2 warning(s)` (ship-spec and review-pr `missing-requires`), which confirms the starting state. There are 11 shipped skills. `.gitattributes` forces `*.md eol=lf`, so the test command's `$`-anchored greps are safe on this Windows checkout.

## Findings

### F-1: Required `vcs-host` / `code-review-bot` hide both skills on Hermes as the adapter ships today
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 1, § Decision 4, § Out of scope (last bullet)
**Edge case:** Runtime precondition. Someone converts the two skills with the shipped Hermes adapter.
**What happens:** `claude-to-hermes.ts` maps a required (no `?`) `vcs-host` to `requires_tools: [vcs-host]` plus a required env var `VCS_HOST_TOKEN`. It maps `code-review-bot` to `requires_tools: [code-review-bot]` plus `CODE_REVIEW_BOT_TOKEN` (`SERVICE_MAP`, L48-50; `buildGating`, L190-206). HERMES-MAPPING.md marks both tool names as provisional. Hermes `requires_tools` controls visibility: a skill is hidden when the tool is missing. Today both skills have no block and are emitted ungated, so they are visible. After this change they would be the first vigil skills to emit `requires_tools`. On a Hermes install with no tool literally named `vcs-host` they disappear silently, and a user is asked for two credentials the skills never read (both use `gh`'s own auth). Brief decision 4 wants a harness without `gh` to "fail clearly before a worktree is cut". On Hermes the result is a silent disappearance instead.
**Why the spec misses it:** The Out of scope line says "the contract note is the whole change there". The only Hermes note the spec adds covers `optional` booleans. It does not mention that the two required roles now flow into the adapter's gating path. `HERMES-MAPPING.md` (a) also says of `shell`: "n/a — `shell` is a boolean, never optional". That row goes stale under Decision 3.
**Suggested fix:** Add a Risks line (or an Out-of-scope line) saying that the provisional Hermes mapping gates both skills on `vcs-host` / `code-review-bot` and that this is accepted. Name a vigil-converter follow-up for the gating and for the stale "never optional" row. No code change is needed in this spec.

### F-2: The contract's Hermes table leaves `shell: optional` unmapped
**Severity:** P2
**Where:** spec § Design › `docs/portability-contract.md` §3, "Hermes mapping" bullet
**Edge case:** A skill declares `shell: optional`. Decision 3 makes this legal and lint accepts it.
**What happens:** The spec adds "an `optional` boolean is not emitted as a requirement" only to the `network`, `subagents`, `filesystem` row (and `filesystem` is not a boolean). The `shell` row still reads "a `terminal`-toolset requirement" with no note. An adapter author who follows the contract table would emit terminal gating for `shell: optional`, which is the opposite of Decision 2. The current converter happens to be safe (`value === true`), but the contract text the spec writes is internally inconsistent.
**Why the spec misses it:** Decision 3 extends `optional` to all three booleans, but the Hermes edit names only one table row.
**Suggested fix:** Put the same note on the `shell` row. Or move it into a single sentence under the table: "for any boolean, `optional` emits no gating key and no required pre-flight line."

### F-3: The rewritten promotion path says the hook blocks regressions it cannot block
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7 ("Every shipped skill carries a block, so `--strict` is clean and the hook blocks regressions.")
**Edge case:** A future skill is added without a `requires:` block, and the pre-commit hook (`python lint.py --strict`) is installed.
**What happens:** `missing-requires` is a WARN, and `--strict` exits 1 only on ERROR (`lint.py:291`). The hook passes and the regression lands. The repo already says this: `tests/test_spec_close_log.py:1196-1197` notes "`lint.py --strict` exits on ERROR only — WARNs never affect its exit status, so the command line alone cannot enforce zero-WARN." Only Decision 9's unit test would catch it. Also, `--strict` was already "clean" in exit-code terms before this change, so the "so" clause carries no information.
**Why the spec misses it:** The rewrite keeps the old wording's promise. The spec's own Out of scope excludes "any `--strict` mode that treats WARN as an error", which is the thing that would make the promise true.
**Suggested fix:** Reword along these lines: "Every shipped skill carries a block, so the lint reports no warnings; the hook blocks ERROR regressions, and `tests/test_lint.py::test_shipped_skills_clean` catches a skill added without a block."

### F-4: Lint accepts `OPTIONAL` / `Optional`, but the contract text the spec writes says lowercase exactly
**Severity:** P3
**Where:** spec § Design › `lint.py`; § Design › contract "Lexical rules, step 5"
**Edge case:** Mixed-case value, e.g. `subagents: Optional`.
**What happens:** `_validate_requires_value` compares `val.lower()`, so lint passes `Optional`, `OPTIONAL` and `TRUE`. The spec now writes the boolean values into rule 5 ("must match … **exactly** (lowercase, unquoted) … (for a boolean key: `true`, `false`, `optional`)"). Lint and contract therefore disagree on a value the spec itself introduces. The outcome is harmless today: the converter's js-yaml treats `Optional` as a string, so it is not a requirement.
**Why the spec misses it:** The spec keeps `.lower()` without noting the tolerance.
**Suggested fix:** Either compare exactly (`val not in ("true", "false", "optional")`; none of the shipped skills uses a capitalised value), or add the case tolerance to lint.py's docstring list of "slightly stricter/looser than §3" deviations, next to the tab-indent note.

### F-5: `optional` is a truthy string, so a naive consumer inverts it
**Severity:** P3
**Where:** spec § Decision 2; § Design › contract "Field semantics, booleans bullet"
**Edge case:** A third-party harness or adapter reads `requires.subagents` with truthiness (`if caps["subagents"]:` in Python, `if (req.subagents)` in JS).
**What happens:** `"optional"` is a non-empty string, so the consumer treats it as required and fails pre-flight on a host without subagents. That is the opposite of the declared meaning. vigil-converter is safe (`value === true`), but the contract is written for "any conforming harness".
**Why the spec misses it:** Decision 2 explains why `true?` was rejected, but not the parsing hazard of the replacement value.
**Suggested fix:** Add one clause to the booleans bullet: "a consumer treats only the boolean `true` as a requirement; `optional` is a string and must not be tested for truthiness."

### F-6: Tests pin only `subagents: optional`, and not the spelling Decision 2 rejects
**Severity:** P3
**Where:** spec § Design › `tests/test_lint.py` and fixtures
**Edge case:** `shell: optional` / `network: optional` (accepted per Decision 3), and `subagents: true?` (rejected per Decision 2).
**What happens:** The `optional-bool` fixture is the ship-spec block verbatim, so only `subagents: optional` is exercised. If someone narrows the tuple to a `subagents`-only special case later, Decision 3 breaks silently. The `bad-bool` fixture uses `maybe`. The value most likely to actually appear is `true?`, which the spec calls out as a typo hazard, and it is not pinned.
**Why the spec misses it:** The fixture is chosen to mirror Decision 1, not Decision 3.
**Suggested fix:** Add `shell: optional` and `network: optional` to the `optional-bool` fixture, or to a second fixture. Use `subagents: true?` in `bad-bool.md`, or add it as a second rejected case.

### F-7: The test command's leave-alone guard can pass vacuously and is narrower than Scope
**Severity:** P3
**Where:** spec § Test command (final clause); § Test plan item 6
**Edge case:** (a) `origin/main` does not resolve in the run context. (b) A new untracked file appears under a leave-alone path. (c) A change lands in another file under `tests/`.
**What happens:** (a) `git diff` writes its error to stderr, `$(...)` comes back empty, and `test -z` passes, so the guard goes green on an error. (b) `git diff` never lists untracked files. (c) Scope says to leave alone "every other file under `tests/`", but the path list leaves `tests/` out entirely (`test_session_handoff.py`, `test_talaria_*.py`).
**Why the spec misses it:** The command checks only tracked diffs over a hand-picked subset of paths.
**Suggested fix:** Prefix the clause with `git rev-parse --verify -q origin/main >/dev/null &&`. Append `git ls-files --others --exclude-standard -- <same paths>` inside the `$(...)`. Add `tests/test_session_handoff.py tests/test_talaria_bridge.py tests/test_talaria_watch.py tests/fixtures/session-handoff tests/fixtures/spec-close` to the path list. Or narrow test-plan item 6's wording to match what the command checks.

### F-8: What happens when an `optional` boolean fails at point of use is unstated
**Severity:** P3
**Where:** spec § Design › contract "Availability" bullet
**Edge case:** The host offers subagents, so /ship-spec takes the subagent branch, but the dispatch then errors.
**What happens:** /ship-spec Phase 3b step 3 treats a dispatch error as "review errors" and skips the gate (`review gate: skipped (<command> failed)`). It does not fall back to inline. The contract's existing point-of-use rule covers "required → fail; optional → warn-and-proceed" for services only. The new sentence covers only pre-flight ("never verified at pre-flight"). VHS-21, which builds conformance assertions from §5 "honored gates", has no defined expectation for an optional boolean that fails mid-run.
**Why the spec misses it:** The Availability addition is scoped to pre-flight only.
**Suggested fix:** Extend the added sentence: "An `optional` boolean is likewise never verified at pre-flight; if it fails at point of use, the skill follows the fallback its body states."

### F-9: The doc tripwire matches only one exact phrase
**Severity:** P4
**Where:** spec § Decision 7
**Edge case:** The backlog sentence comes back reworded (e.g. "lack a `requires:` block").
**What happens:** `test_missing_requires_backlog_is_clear` still passes. This is low risk because Decision 9's zero-WARN assertion catches the real state; only the doc can drift.
**Why the spec misses it:** The test asserts an exact substring.
**Suggested fix:** None needed. Optionally, also assert that no line in § Promotion path names `ship-spec` or `review-pr`.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 5 | P4: 1

Relevant paths:
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-51.spec.md
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\lint.py (L103-109 boolean branch, L291 strict exit)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\tests\test_spec_close_log.py (L1059-1066, L1194-1203)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\portability-contract.md (§3 L53-103)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\authoring-portable-skills.md (L38-42)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-converter\src\converters\claude-to-hermes.ts (L48-50, L99-110, L186-210)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-converter\HERMES-MAPPING.md (§(a) table)

STATUS: GREEN
