# VHS-51 — Add requires: blocks to /ship-spec and /review-pr (clear the missing-requires backlog)
**Status:** Backlog · **Priority:** low · **Assignee:** unassigned
**Created:** 2026-10-08 · **Plane:** VHS-51 (27984281-29e0-4397-a8f8-a5644044c142, Backlog)
**Origin:** Raised twice on 2026-10-08 and kept out of scope both times: by the spec reviewers on VHS-46 (review gate) and by the Codex brief review on VHS-47 (green marker). Devin chose a separate ticket. The brief interview settled ten decisions in two rounds, including a small extension to the portability contract so the block can say "subagents: optional".

## Problem

`skills/ship-spec/SKILL.md` and `skills/review-pr/SKILL.md` have no `requires:` block. `python lint.py` reports a `missing-requires` WARN for each. The portability contract (`docs/portability-contract.md`) says a skill declares the capabilities it uses, and treats an undeclared one as unavailable. Both skills use shell, the filesystem, the network and `gh` throughout; `/ship-spec` also uses an optional issue tracker and, since VHS-46, an optional subagent for the review gate, and with VHS-47 it runs a hash command.

## Why it matters

The contract exists so a harness can fail clearly before any mutation when a required capability is missing, instead of inferring needs by reading the body. Two of the three skills that mutate the most (worktrees, pushes, PRs, tracker state) are the ones with no declaration. The lint's promotion path from warn-only to blocking is gated on clearing this backlog.

## Scope (verified against current files, 2026-10-08)

| Path | Current | Change |
|---|---|---|
| `skills/ship-spec/SKILL.md` | Frontmatter has `name`, `description`, `user_invocable` and no `requires:` (lint WARN at line 1). Uses git fetch/worktree/push, `gh auth` (L81) and `gh pr create` (L317), the spec's test command, a hash command (L16), Read/Edit/Write, an optional Plane integration that warns and proceeds (preflight step 8, Phase 6, L365), and a subagent for Phase 3b when the host has one, inline otherwise (L377). | Decision 1: add `requires:` with `shell: true`, `filesystem: [read, write]`, `network: true`, `subagents: optional`, `services: [vcs-host, issue-tracker?]`. Tool-use notes say the review runs in a subagent when one exists. No behaviour change. |
| `skills/review-pr/SKILL.md` | Frontmatter has `name`, `description`, `user_invocable` and no `requires:`. Uses `gh api`, `gh pr view/diff/checks/comment`, git add/commit/push, Read/Edit, and CodeRabbit throughout; with no CodeRabbit review it reports "No CodeRabbit reviews found" and stops (Step 2). | Decision 1: add `requires:` with `shell: true`, `filesystem: [read, write]`, `network: true`, `services: [vcs-host, code-review-bot]`. |
| `docs/portability-contract.md` | §3 schema (L53-60) and field semantics (L62-66): `shell`/`network`/`subagents` are booleans, absent = false; the `?` optional marker is defined for `services` only; vocabulary "extensible by a future revision of this contract". Hermes mapping table at L97-101. | Decision 2: booleans accept a third value, `optional`, meaning "used when the harness offers it; never a pre-flight requirement". One sentence in field semantics, the schema comment, and a note in the Hermes mapping row for `network`, `subagents`, `filesystem`. |
| `lint.py` | `BOOL_KEYS = {"shell", "network", "subagents"}` (L46); `_validate_requires_value` rejects anything but `true`/`false` for a boolean key (L103-108); `SERVICES_VOCAB` already holds `vcs-host` and `code-review-bot` (L48). | Decision 2: accept `optional` for the three boolean keys. Nothing else changes; the service tokens already validate. |
| `tests/test_lint.py` | Fixture-driven cases for valid blocks, malformed blocks, and `missing-requires` (L35-72); shipped-skill census pinned at 11. | Decision 2: one fixture with `subagents: optional` that lints clean, and one asserting a misspelling (e.g. `subagents: maybe`) is still `requires-malformed`. Census unchanged. |
| `docs/authoring-portable-skills.md` | L36-42 "Promotion path: warn-only → blocking": step 1 clears the backlog and names `ship-spec` and `review-pr` ("This is the tracked backlog item"); step 2 installs a pre-commit hook running `python lint.py --strict`. L36 lists the WARN rule. | Decision 4: delete step 1 and renumber, so the path is the hook alone. Decision 2: the `requires:` guidance documents the `optional` value. |
| `tests/test_spec_close_log.py` | `test_missing_requires_backlog_no_longer_names_spec_close` (L1059-1066) asserts exactly one line contains "have no `requires:` block", that it does not name `spec-close`, and that it names `ship-spec` and `review-pr`. | Decision 4: becomes a tripwire: no line in the doc says "have no `requires:` block". |

## Decisions carried forward

1. **Both skills gain an accurate `requires:` block.** `/ship-spec`: `shell: true`, `filesystem: [read, write]`, `network: true`, `subagents: optional`, `services: [vcs-host, issue-tracker?]`. `/review-pr`: `shell: true`, `filesystem: [read, write]`, `network: true`, `services: [vcs-host, code-review-bot]`. Why: the ticket asks for a block that matches what each skill uses, and these are the capabilities each one has no fallback for, plus the two it uses opportunistically.
2. **Subagents are declared `optional`, not `true` and not omitted.** Why: a subagent is useful when present (the review gate; future parallel work in `/ship-spec`) but never a pre-flight requirement, since the gate runs inline without one. Neither direction is forced.
3. **The contract gains a third boolean value, `optional`.** `docs/portability-contract.md` §3, `lint.py`, `tests/test_lint.py` and `docs/authoring-portable-skills.md` learn it; the Hermes mapping table notes that an adapter treats `optional` as not gating. Why: `subagents: optional` is a plain YAML scalar a reader and a parser both accept; the contract already calls its vocabulary extensible; `true?` would be a string that looks like a typo.
4. **`gh` is declared as the `vcs-host` role, required, on both skills.** Why: declaring up front what the agent may use is what the block is for; neither skill has a fallback without `gh`, so a harness without it fails clearly before a worktree is cut.
5. **`code-review-bot` is required on `/review-pr`.** Why: the skill as shipped stops at "No CodeRabbit reviews found" and cannot proceed; the contract defines optional as warn-and-proceed. The swappable-reviewer work (its own ticket, see Out of scope) flips the marker to `code-review-bot?` when the fallback exists.
6. **`issue-tracker?` optional on `/ship-spec`; warn-and-proceed stays.** Why: the block must describe the skill as it runs (preflight step 8 and Phase 6 warn and continue) and the repo's public-harness rule from VHS-46. A tracker-less run still produces a PR with no ticket update; accepted.
7. **Promotion-path step 1 is deleted and the path renumbered; the test becomes a tripwire.** Why: the doc is a to-do list and a cleared item is noise; history lives in git and the wiki. The test asserts no line says "have no `requires:` block", so the backlog cannot silently reopen.
8. **`/spec-close`'s block is left alone.** It runs `gh pr view` / `gh pr diff` under `network: true` without `vcs-host`, and after this change it is the one inconsistent block. Why: it degrades to a commit SHA without `gh`, so its correct marker (`vcs-host?`) needs its own look, and this ticket already grows by the contract and the lint.

## Done when

- Both skills carry a `requires:` block that matches what they use.
- `python lint.py` shows no `missing-requires` warning for any shipped skill.
- The doc and the test agree: `docs/authoring-portable-skills.md` no longer names a backlog, and `tests/test_spec_close_log.py` pins that.

## Out of scope

- The pre-commit hook (promotion-path step 2) and any `--strict` mode that treats WARN as an error. Separate ticket if wanted.
- Making `/review-pr`'s reviewer swappable (CodeRabbit was rate-limited to one review an hour for a week in early October 2026). Its own ticket; it flips `code-review-bot` to optional when it lands.
- Any change to `/ship-spec`'s behaviour when the tracker is unreachable.
- `/spec-close`'s `requires:` block (Decision 8).
- Wiki filemap and state lines: `/wiki-after-merge` owns them.
- Hermes adapter code (`vigil-converter`): the contract note is enough; the adapter is a separate repo.

## Risks / decisions

1. Lint census: `tests/test_lint.py` pins 11 shipped skills and no test pins the shipped WARN count; after this change the expected count is 0, and the filemap's "2 tracked WARNs remain" line goes stale until the post-merge routine updates it. Spec author decides whether a test pins "0 WARN across shipped skills" (`tests/test_spec_close_log.py:1201-1203` does this for `spec-close` alone) — spec author pins this.
2. `optional` on `shell` or `network` has no present user; the contract defines it for all three booleans for symmetry. Spec author decides whether the lint accepts it on all three or on `subagents` only — spec author pins this.

## References

- `docs/portability-contract.md:53-66` — `requires:` schema and field semantics; `:71-80` availability rules; `:97-101` Hermes mapping.
- `lint.py:45-48` — `REQUIRES_KEYS`, `BOOL_KEYS`, `SERVICES_VOCAB`; `:103-141` value validation; `:145-198` block parsing.
- `skills/spec-close/SKILL.md:5-9` — the precedent block (`gh` under `network: true`); `:79` the `gh pr view` use.
- `skills/ship-spec/SKILL.md:16, :81, :117, :314-317, :365, :377` — the capabilities `/ship-spec` uses.
- `skills/review-pr/SKILL.md` Step 2 — the CodeRabbit dependency and the "No CodeRabbit reviews found" exit.
- `docs/authoring-portable-skills.md:36-42` — the WARN rule and the promotion path.
- `tests/test_spec_close_log.py:1059-1066` — the backlog-sentence test; `:1201-1203` the spec-close zero-WARN test.
- `vigil-harbor-wiki/projects/vigil-skills/filemap.md:204` — the "2 tracked WARNs remain" line.
- Related tickets: VHS-17 (contract), VHS-18 (lint), VHS-46, VHS-47.
- Interview: 2 rounds, exit empty-frontier
