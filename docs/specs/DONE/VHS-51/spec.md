# VHS-51 — Add requires: blocks to /ship-spec and /review-pr (clear the missing-requires backlog)

## Goal

The two shipped skills with no `requires:` block get one that matches what they use, the portability contract gains the one value needed to describe `/ship-spec`'s opportunistic subagent honestly (`optional`), the lint accepts that value, and the authoring doc's promotion path and the test that pins it stop naming a backlog. After this, `python lint.py` reports zero warnings for every shipped skill, and a test keeps it that way.

## Scope

| Path | Change |
|------|--------|
| `skills/ship-spec/SKILL.md` | Frontmatter gains a `requires:` block (Decision 1). One clause in the Tool-use notes bullet about Phase 3b names the declaration. No other line changes. |
| `skills/review-pr/SKILL.md` | Frontmatter gains a `requires:` block (Decision 1). No other line changes. |
| `docs/portability-contract.md` | §3: the schema comment on `subagents`, the booleans bullet under Field semantics, the "required" parenthetical and one sentence under Availability, the lexical rule for boolean values, and one sentence under the Hermes mapping table (Decisions 2, 3). The role-token sentence names what `vcs-host` and `code-review-bot` map to (Decision 4). |
| `lint.py` | `_validate_requires_value` accepts `optional` for the three boolean keys (Decision 3). |
| `tests/test_lint.py` | Two new cases and two new fixtures for the `optional` value; the shipped-skills case also asserts zero WARN (Decisions 3, 9). |
| `tests/fixtures/optional-bool/SKILL.md`, `tests/fixtures/bad-bool.md` | New fixtures (Decision 3). |
| `docs/authoring-portable-skills.md` | The copyable template's `subagents` comment names `optional`; the WARN rule's pointer is reworded; promotion-path step 1 is deleted and the path becomes one step (Decisions 3, 7). |
| `tests/test_spec_close_log.py` | `test_missing_requires_backlog_no_longer_names_spec_close` becomes `test_missing_requires_backlog_is_clear` (Decision 7). |

Leave alone: `skills/spec-close/SKILL.md` and every other skill's frontmatter (Decision 8), `skills/ship-spec/states.json`, `sync.py`, `agents/`, every other file under `tests/`, `README.md`, `AGENTS.md`, and the `vigil-converter` repo.

## Decisions

Brief decision numbers are in parentheses.

### Decision 1 — The two blocks (brief 1, 2, 4, 5, 6)

`skills/ship-spec/SKILL.md`, placed after `user_invocable: true` and before the closing `---`:

```yaml
requires:
  shell: true
  filesystem: [read, write]
  network: true
  subagents: optional
  services: [vcs-host, issue-tracker?]
```

`skills/review-pr/SKILL.md`, same position:

```yaml
requires:
  shell: true
  filesystem: [read, write]
  network: true
  services: [vcs-host, code-review-bot]
```

Each line is backed by a use the skill already has: `/ship-spec` runs git, `gh`, the spec's test command and a hash command (shell, network), reads the spec and writes the worktree, the test capture and the review record (filesystem), uses a subagent for Phase 3b when the host has one and runs inline otherwise (`optional`), needs `gh` for the PR (`vcs-host`, required), and warns and proceeds when Plane is down at preflight step 8 and Phase 6 (`issue-tracker?`). `/review-pr` runs `gh api` and git (shell, network, `vcs-host`), reads and edits files, and stops at "No CodeRabbit reviews found" without one (`code-review-bot`, required). Neither skill's behaviour changes.

### Decision 2 — `optional` means "used when offered, never a pre-flight requirement" (brief 2)

A boolean set to `optional` says the skill uses the affordance when the harness offers it and has a stated fallback in its body when it does not. A harness never fails pre-flight on an `optional` capability and need not probe it; if the affordance fails at point of use, the skill follows the fallback its body states. This is the boolean counterpart of a trailing `?` on a service role, written as a value rather than a suffix because `true?` is a string in every YAML parser and reads as a typo. `optional` is itself a string, so a consumer must treat only the boolean `true` as a requirement and never test the value for truthiness.

### Decision 3 — All three booleans accept `optional` (brief 3; brief Risk 2)

The contract defines `optional` for `shell`, `network` and `subagents` alike, and the lint accepts it on all three. Only `subagents` has a user today. Symmetry keeps the field-semantics bullet to one sentence and the lint change to one tuple; restricting it to `subagents` would add a special case for no present benefit. The lint keeps its existing case-insensitive comparison for boolean values, and the contract's lexical rule says so for booleans.

### Decision 4 — The role tokens are named to their fleet meaning (spec addition; supports brief 4, 5)

The contract's role-token sentence already maps `issue-tracker` to Plane and `shared-memory` to the shared-memory service. It gains the same for the two tokens entering use: `vcs-host` is the pull-request host and its CLI (`gh` on GitHub), `code-review-bot` is the review bot on that host (CodeRabbit). Both are required where declared, because neither skill has a fallback. The brief settles the two tokens as required; naming their meanings in the contract is this spec's addition, so a reader of the vocabulary knows what a harness binds them to.

### Decision 5 — `issue-tracker?` on `/ship-spec`; no behaviour change (brief 6)

The block describes the skill as it runs. Preflight step 8 and Phase 6 keep their warn-and-proceed text. A tracker-less run still produces a PR with no ticket update; the brief accepts this.

### Decision 6 — `/ship-spec`'s Tool-use notes name the declaration (brief 2)

The existing bullet "The Phase 3b review runs in a read-only subagent when the host has one, inline otherwise" gains the clause ", which is what `subagents: optional` in the frontmatter declares". This is the one body edit in `/ship-spec`, so a reader who finds `optional` in the block finds its fallback named in the body.

### Decision 7 — The promotion path loses step 1; the test becomes a tripwire (brief 7)

`docs/authoring-portable-skills.md` § Promotion path: step 1 (clear the backlog) is deleted. The remaining item is renumbered 1 and its "Once step 1 is done" clause is rewritten as "Every shipped skill carries a block, so the lint reports no warnings. The hook blocks ERROR regressions; a shipped skill that loses its block is caught by `tests/test_lint.py::test_shipped_skills_clean`, since `--strict` never gates on WARNs." `tests/test_spec_close_log.py::test_missing_requires_backlog_no_longer_names_spec_close` is renamed `test_missing_requires_backlog_is_clear` and asserts that no line of the doc contains "have no `requires:` block". The old assertions (exactly one such line; names `ship-spec` and `review-pr`) are removed with the sentence they pinned. The test stays in `TestNoStaleWording` in that file because the brief's Done when names the file; moving it to `tests/test_lint.py` is a later tidy-up if wanted.

### Decision 8 — `/spec-close`'s block is left alone (brief 8)

It runs `gh pr view` and `gh pr diff` under `network: true` with no `vcs-host`. After this change it is the one block that uses `gh` without declaring the role. It is not edited here: it has a commit-SHA path that does not need `gh`, so its correct marker is `vcs-host?`, and that is a one-line follow-up once the operator confirms it. Tracked as VHS-53.

### Decision 9 — A tripwire pins zero WARN across shipped skills (brief Risk 1)

`tests/test_lint.py::test_shipped_skills_clean` gains a second assertion: `warns(lint.lint_path(s)) == []` for every shipped skill. Today only `spec-close` and `session-handoff` have such a pin (`tests/test_spec_close_log.py:1201-1203`, `tests/test_session_handoff.py:765-770`). The census assertion (11) is unchanged.

### Decision 10 — Scale is a non-factor

The brief declares no scale section. Two frontmatter blocks and one lint tuple.

## Design

### `skills/ship-spec/SKILL.md` and `skills/review-pr/SKILL.md`

Insert the Decision 1 block between `user_invocable: true` and the closing `---`, two-space indented, no comments, no blank lines. The contract's uniqueness rule (one `requires:` per skill, after the scalar keys, before the closing `---`) is met by position. In `/ship-spec`'s Tool-use notes, apply Decision 6's clause to the Phase 3b bullet.

### `docs/portability-contract.md` §3

- **Schema block:** the `subagents: true` comment becomes `# dispatches concurrent sub-agents / parallel tasks; optional = used when offered`.
- **Field semantics, booleans bullet:** becomes "`shell`, `network`, `subagents` — `true`, `false`, or `optional`. Absent = `false`. `optional` means the skill uses the affordance when the harness offers it and its body states the fallback when it does not; it is never a pre-flight requirement. A consumer treats only the boolean `true` as a requirement; `optional` is a string and must not be tested for truthiness."
- **Field semantics, services bullet:** the mapping clause becomes, in full: "a harness maps `issue-tracker` → Plane (or its own), `shared-memory` → the shared-memory/MCP service, `vcs-host` → the pull-request host and its CLI (GitHub via `gh`), `code-review-bot` → the review bot on that host (CodeRabbit), etc."
- **Availability:** the parenthetical in "A harness MUST verify each **required** capability (no `?`) before any mutation" becomes "(no `?` on a service; not `optional` on a boolean)". After the sentence on optional services, add "An `optional` boolean is likewise never verified at pre-flight; if it fails at point of use, the skill follows the fallback its body states."
- **Lexical rules, step 5:** "the remaining token must match the controlled vocabulary exactly (lowercase, unquoted)" gains "(for a boolean key: `true`, `false`, `optional`, compared case-insensitively)".
- **Hermes mapping:** one sentence directly under the table: "An `optional` boolean (`shell`, `network`, `subagents`) emits no Hermes gating key and no pre-flight requirement." No table row changes.

### `lint.py`

In `_validate_requires_value`, the boolean branch checks `val.lower() not in ("true", "false", "optional")` and its message reads `must be true/false/optional`. Nothing else changes: `REQUIRES_KEYS`, `BOOL_KEYS`, the service-token path and the block parser are untouched, and `vcs-host` and `code-review-bot` already validate.

### `tests/test_lint.py` and fixtures

- `tests/fixtures/optional-bool/SKILL.md`: a minimal skill whose block declares `shell: optional`, `filesystem: [read]`, `network: optional`, `subagents: optional`, so all three booleans are exercised (Decision 3). `test_optional_boolean_accepted` asserts zero ERROR and no `missing-requires`.
- `tests/fixtures/bad-bool.md`: the same frontmatter with `subagents: true?`, the spelling Decision 2 rejects. `test_unknown_boolean_value_rejected` asserts a `requires-malformed` ERROR.
- `test_shipped_skills_clean`: Decision 9's second assertion, with the message "unexpected WARN(s) in {s}: {warns}" so a reopened backlog names the skill. Its comment becomes "# Regression for VHS-18: lint runs clean (zero ERRORs) against the shipped skills; VHS-51: and zero WARNs".
- Each new case carries `# Regression for VHS-51: <one line>`.

### `docs/authoring-portable-skills.md`

- Template comment on the `subagents` line: `# dispatches concurrent sub-agents; or optional`.
- The WARN rule line "(advisory; see promotion path)" becomes "(advisory; never gates `--strict`)", since the promotion path no longer mentions it.
- § Promotion path: Decision 7. The paragraph above the list ("The lint ships warn-only. To promote it to a hard gate:") stays.

### `tests/test_spec_close_log.py`

Decision 7's rename and assertion. The test stays in its class; `PORTABLE_DOC` is reused.

## Test plan

Mechanical gate:

1. `python tests/test_lint.py` exits 0 with the two new cases and the strengthened shipped-skills case; census stays 11.
2. `python tests/test_spec_close_log.py` exits 0 with the renamed backlog test.
3. `python lint.py --strict` exits 0 and its stderr summary reads `lint: 0 error(s), 0 warning(s)`.
4. `skills/ship-spec/SKILL.md` contains the line `  subagents: optional` and `  services: [vcs-host, issue-tracker?]`; `skills/review-pr/SKILL.md` contains `  services: [vcs-host, code-review-bot]`.
5. `docs/authoring-portable-skills.md` has no line containing "have no `requires:` block".
6. The leave-alone paths have no tracked diff and no untracked files against `origin/main`, and `origin/main` resolves before the check runs.
7. `docs/portability-contract.md` contains the word `optional` in §3's booleans bullet.

Review checklist for the prose:

- The two blocks match Decision 1 exactly, in position and in indentation.
- The `optional` semantics are stated once in the contract and the authoring doc's template points at them; neither doc says a harness probes an `optional` capability.
- `/ship-spec`'s Phase 3b bullet names the declaration and its fallback.
- The promotion path reads as a single remaining step with no reference to a cleared one, and no sentence claims `--strict` gates a WARN.
- No `requires:` block other than the two new ones changed.

## Test command

Run from the repo root. It must exit 0.

```
python tests/test_lint.py && python tests/test_spec_close_log.py && python lint.py --strict && python lint.py 2>&1 >/dev/null | grep -q 'lint: 0 error(s), 0 warning(s)' && grep -q '^  subagents: optional$' skills/ship-spec/SKILL.md && grep -q '^  services: \[vcs-host, issue-tracker?\]$' skills/ship-spec/SKILL.md && grep -q '^  services: \[vcs-host, code-review-bot\]$' skills/review-pr/SKILL.md && ! grep -q 'have no `requires:` block' docs/authoring-portable-skills.md && git rev-parse --verify -q origin/main >/dev/null && test -z "$(git diff --name-only origin/main -- skills/spec-close skills/spec-cycle skills/spec-brief skills/spec-tickets skills/grilling skills/grill-me skills/session-handoff skills/talaria skills/hermes-kanban-awareness skills/ship-spec/states.json sync.py agents README.md AGENTS.md tests/test_session_handoff.py tests/test_talaria_bridge.py tests/test_talaria_watch.py tests/fixtures/session-handoff tests/fixtures/spec-close; git ls-files --others --exclude-standard -- skills/spec-close skills/spec-cycle skills/spec-brief skills/spec-tickets skills/grilling skills/grill-me skills/session-handoff skills/talaria skills/hermes-kanban-awareness agents tests/fixtures/session-handoff tests/fixtures/spec-close)"
```

## Done when

- Both skills carry a `requires:` block that matches what they use. — Decision 1; checked by test-plan item 4 and the review checklist.
- `python lint.py` shows no `missing-requires` warning for any shipped skill. — Decisions 1, 3, 9; checked by test-plan items 1 and 3.
- The doc and the test agree: `docs/authoring-portable-skills.md` no longer names a backlog, and `tests/test_spec_close_log.py` pins that. — Decision 7; checked by test-plan items 2 and 5.

## Out of scope

- The pre-commit hook (promotion-path step 2) and any `--strict` mode that treats WARN as an error.
- Making `/review-pr`'s reviewer swappable; VHS-52 flips `code-review-bot` to `code-review-bot?` when the fallback exists.
- Any change to `/ship-spec`'s behaviour when the tracker is unreachable.
- `/spec-close`'s `requires:` block (Decision 8).
- Wiki filemap and state lines.
- Hermes adapter code in `vigil-converter`; the contract note is the whole change there.

## Deferred (P2+)

- conventions/R1/F-3 — The swappable-reviewer work named in Out of scope was unticketed at review time (the wiki decision of 2026-09-27 calls it unticketed VHS work). Filed as VHS-52 after the green verdict and cited in Out of scope.
- conventions/R1/F-8 — The `/spec-close` `vcs-host?` follow-up (Decision 8) had no ticket at review time. Filed as VHS-53 after the green verdict.
- edge-cases/R1/F-1, conventions/R1/F-4 — The shipped Hermes adapter maps a required `vcs-host` / `code-review-bot` to `requires_tools` plus a required token env var, so on a Hermes install without tools of those names the two skills are hidden rather than failing clearly, and its `HERMES-MAPPING.md:19` and `types/hermes.ts:46-47` wording ("booleans are never optional") goes stale. The adapter's code needs no change for `optional` (`value === true`). Accepted here; a vigil-converter follow-up owns the gating names and the stale wording. Out of scope is outside the polish limits, so the bullet there is unchanged.
- edge-cases/R1/F-9 — The doc tripwire matches one exact phrase; a reworded backlog sentence would pass it. Decision 9's zero-WARN assertion catches the real state.
- correctness/R1/F-5 — Reviewers could not read the ticket from shared memory (namespace ACL); the brief transcribes the ticket's Done when verbatim, confirmed through the tracker during `/spec-brief`.

## Post-green polish

- correctness/R1/F-1, conventions/R1/F-1, edge-cases/R1/F-3 — § Decision 7 and § Design: the rewritten promotion-path sentence no longer claims `--strict` blocks a missing block; it names the unit test that does. Wording of a quoted doc sentence; the decision is unchanged.
- correctness/R1/F-2, conventions/R1/F-2, edge-cases/R1/F-2 — § Design (contract): the `optional` note moves from one table row to a sentence under the whole Hermes table, covering `shell`.
- correctness/R1/F-3, conventions/R1/F-10, edge-cases/R1/F-4 — § Decision 3 and § Design: the lint keeps its case-insensitive comparison and the contract's lexical rule says so for booleans.
- correctness/R1/F-4 — § Decision 9: `session-handoff`'s zero-WARN pin is named with its anchor.
- correctness/R1/F-6 — § Design (authoring doc): the WARN rule's "see promotion path" pointer becomes "never gates `--strict`".
- correctness/R1/F-7 — § Design (contract): the services-bullet mapping clause is given in full, with the trailing "etc." kept.
- conventions/R1/F-5 — § Design (tests): the strengthened case's regression comment names VHS-51 and zero WARNs.
- conventions/R1/F-6 — § Decision 7: one sentence says why the tripwire stays in the spec-close-named suite.
- conventions/R1/F-7 — § Decision 4: relabelled as a spec addition supporting brief 4 and 5.
- conventions/R1/F-9 — § Design (contract): the "required" parenthetical under Availability covers `optional` booleans.
- edge-cases/R1/F-5 — § Decision 2 and § Design: the truthiness hazard of a string value is stated.
- edge-cases/R1/F-6 — § Design (tests): the valid fixture exercises all three booleans; the rejected fixture uses `true?`.
- edge-cases/R1/F-7 — § Test command and § Test plan item 6: `origin/main` must resolve, untracked files count, and the other `tests/` files are on the leave-alone list.
- edge-cases/R1/F-8 — § Decision 2 and § Design: point-of-use failure of an `optional` boolean follows the body's fallback.
