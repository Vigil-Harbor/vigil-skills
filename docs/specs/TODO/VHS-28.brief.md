# VHS-28 — Own the session-handoff skill in vigil-skills; retire the untracked `agentcraft-handoff` copy

**Status:** Backlog · **Priority:** Medium · **Assignee:** Unassigned
**Created:** 2026-08-23 · **Plane:** VHS-28 (standalone; prior art INFRA-21, cancelled 2026-08-23)
**Origin:** VHS-28 was filed as a validator bug — `agentcraft-handoff/scripts/validate_handoff.py` built its section patterns as `##?`, which matches one `#` or two but never three, so every `###` heading read as **missing** rather than *incomplete*. The skill's own `create_handoff.py` emits two of its three REQUIRED sections at `###` depth (`### Important Context` at line 300, `### Immediate Next Steps` at line 284), so **the template could not pass its own validator** no matter what was written into it. A one-character-class fix (`##?` → `#{1,6}`, three places) was applied live and measured 68 → 80, `NEEDS WORK` → `READY`.

The fix is real but **not durable**, and that — not the regex — is the reason for this item. `~/.claude/skills/agentcraft-handoff/` carries a `.agentcraft-managed` marker, is not a git repository, and is not mirrored in `vigil-skills/skills/`. The fix exists on one machine with no history and dies on the next AgentCraft reinstall or `~/.claude/skills/` re-sync.

**Decision (Devin, 2026-08-23): do not patch the AgentCraft copy. Roll our own.** Ticket done-when #3 offered adoption *or* a recorded decision to stay untracked; this brief takes the adopt path, by clean-room rewrite rather than by copying the vendor's code into a public repo.

## Goal

A tracked, portable **`session-handoff`** skill in `vigil-skills/skills/`, clean-room written, that fully supersedes `agentcraft-handoff` — correct heading handling by construction, a smoke test, `lint.py`-clean frontmatter, and installation through `sync.py` like every other skill in this repo. After it ships, the AgentCraft-managed copy is deleted locally and handoff requests route to ours.

## Why not simply patch the installed skill

- **Not durable.** No git, `.agentcraft-managed`, outside `sync.py`'s `SUBTREES`. This is the ticket's own stated failure mode.
- **Provenance.** `vigil-skills` is public. Copying ~1,150 lines of a third-party vendor-managed skill into it is not a clean adoption; a rewrite we own is.
- **Portability.** The vendor body is AgentCraft-branded throughout ("heroes", "hero handoff", "next AgentCraft session"). Skills in this repo must read as harness-neutral and carry a `requires:` declaration per `docs/portability-contract.md` §2–§3.

## Scope

### 1. New skill — `skills/session-handoff/`

Clean-room authored. No file copied from `~/.claude/skills/agentcraft-handoff/`; that tree is reference material for *behavior*, not a source of text.

- **`SKILL.md`** — frontmatter `name` / `description` / `user_invocable: true` / `requires:` (`shell: true`, `filesystem: [read, write]`; no `network`, no `subagents`). Harness-neutral body: no vendor product nouns, no assumption of a specific UI.
- **`scripts/create_handoff.py`** — scaffold a timestamped handoff at `.claude/handoffs/YYYY-MM-DD-HHMMSS-<slug>.md`, pre-filled with branch, recent commits, and modified files; `--continues-from <file>` for chaining.
- **`scripts/validate_handoff.py`** — completeness + secret scan + score. Correct heading handling by construction.
- **`references/handoff-template.md`** — the section structure, harness-neutral.

**Two scripts, not four.** `list_handoffs.py` and `check_staleness.py` become prompt-driven steps in the body (a `git log` / directory listing the agent already knows how to run). Only the deterministic gates — scaffold generation and the secret/completeness validator — earn a script.

### 2. Modes the skill must cover

- **CREATE** — scaffold, fill, validate, report.
- **RESUME** — list available handoffs, assess staleness against commits since the handoff timestamp, read, verify context, resume at next-step #1.
- **SESSION TRANSFER** — invoked with a session UUID: locate the source transcript, read the tail, summarize in 2–3 sentences, continue the work without interrogating the user. This mode is **harness-specific** (Claude Code stores transcripts at `~/.claude/projects/<project-dir>/<session-id>.jsonl`); the spec must decide how to carry it without hardcoding one harness's layout into a portable skill — a guarded/optional mode with an explicit fallback when no transcript is found.

### 3. Validator correctness — the original VHS-28 bug

- Heading patterns accept `#` through `######` in **all three** places: the required-section match, the section-terminator scan (otherwise a `###` subsection fails to terminate its parent and content bleeds across it, making the ≥50-character content check over-generous), and the recommended-section match.
- The shipped template's heading depths and the validator's accepted depths must agree **by construction** — a freshly generated scaffold with content filled in at the template's own depths validates with zero sections reported `missing`.
- Preserve the three distinctions the vendor fix was smoke-tested against: level-3 section with real content → passes; genuinely absent section → still `missing`; level-3 section with 5 characters → still `incomplete`.

### 4. Tests — `tests/test_session_handoff.py`

The absence of any test is how a regex that failed on the template's own output went unnoticed. Cover, at minimum: the three distinctions above; a generated-scaffold round-trip (create → fill → validate clean); and at least one secret-pattern positive. Follows the existing `tests/test_lint.py` / `tests/test_talaria_*.py` shape (stdlib + pytest, fixtures under `tests/fixtures/`).

### 5. Supersession of `agentcraft-handoff`

Ours fully replaces it, including the session-transfer mode. **`~/.claude/skills/agentcraft-handoff/` is deleted after install** — note that this is an *operator step outside the PR diff*, since `ship-spec` PRs the repo and cannot touch `~/.claude/`. The spec must state where that step is recorded so it is not lost (skill body, `AGENTS.md`, or the PR description), and what the expected behavior is if AgentCraft restores its managed copy on a later run.

## Decisions carried forward

- **Clean-room rewrite, not a port** (Devin, 2026-08-23). Public repo; no vendor-derived code.
- **Lean surface — two scripts.** `list` and `staleness` are prompt-driven, not scripted.
- **Full supersession** (Devin, 2026-08-23). Ours owns every handoff trigger *and* the session-UUID transfer mode; the AgentCraft copy is removed locally.
- **Spec-lifecycle process** (Devin, 2026-08-23). Brief → `/spec-cycle` → `/ship-spec`, per repo convention — not a direct branch commit.
- **Portability contract applies** (`docs/portability-contract.md` §2–§3). Canonical `SKILL.md` under `skills/<name>/`, `requires:` block declared, `python lint.py` clean.
- **Storage location unchanged** — `.claude/handoffs/`, `YYYY-MM-DD-HHMMSS-<slug>.md`. Existing handoff documents on disk (e.g. the MCP-49/50/53/54 sprint handoff that surfaced this bug) must remain readable and listable by the new skill.

## Scale

**Factor:** no — a single-user, single-document-at-a-time skill; handoff directories hold tens of files, not thousands. The scalability lens stays off.

## Done when

1. `skills/session-handoff/` exists in `vigil-skills`, installs via `python sync.py install`, and `python lint.py` reports no ERROR for it.
2. The heading regex accepts `#` through `######` in all three places, and a freshly generated scaffold — filled in at the template's own heading depths — validates with **no section reported `missing`**.
3. `tests/test_session_handoff.py` passes, covering the three heading distinctions, a scaffold round-trip, and a secret-pattern positive.
4. The skill handles all three modes (CREATE, RESUME, SESSION TRANSFER) with the vendor skill uninstalled.
5. `~/.claude/skills/agentcraft-handoff/` is removed on the operator machine, and that step plus the AgentCraft-may-restore-it caveat is recorded in a tracked file.
6. VHS-28's original done-when #1, #2 and #4 are satisfied by the above; done-when #3 is satisfied by adoption-via-rewrite, recorded as such.

## Out of scope

- **The second false positive, deliberately.** The "referenced file(s) not found" check resolves every path-looking string against the handoff's own project root, so cross-repo and skill-relative paths always read as broken (five such warnings on a correct document, none dead links). Distinguishing a cross-repo reference from a typo needs more than a regex — that is a design call and, per the ticket, its own card. The rewrite may carry the check forward as-is or drop it, but must not attempt to solve it here.
- Generating a Hermes (or any other harness) adapter for this skill — that flows through the VHS-16 cross-harness line, not this item.
- Migrating or rewriting existing handoff documents already on disk.
- Preventing AgentCraft from reinstalling its own managed skill; we control our copy and the local deletion, not the vendor's installer.
- Any change to `sync.py`, `lint.py`, or the spec-lifecycle skills.

## Open questions for the spec

- **Gate semantics.** The vendor body says "do not finalize with secrets detected or score below 70." Keep the numeric threshold, or replace it with a pass/fail on required-sections-plus-no-secrets? A score that the template itself could not reach is what pushed authors toward gaming it.
- **Session-transfer portability.** How to express "read the previous session's transcript" without hardcoding Claude Code's `~/.claude/projects/**/<uuid>.jsonl` layout — a `requires:`-declared capability, a documented harness-specific block, or a graceful degrade to `git status` + ask.
- **Name.** `session-handoff` is the working name; confirm it does not collide with a future harness's built-in and that its `description` fires on the same natural phrasings the vendor skill claimed ("create handoff", "save state", "load handoff", "resume from", "continue where we left off").

## References

- **Plane VHS-28** — the source card, with the measured before/after and the "fix applied, NOT durable" status section.
- `~/.claude/skills/agentcraft-handoff/` — behavioral reference only. `SKILL.md`, `scripts/{create,validate,list}_handoff*.py`, `scripts/check_staleness.py`, `references/{handoff-template,resume-checklist}.md`. Carries `.agentcraft-managed`; the `#{1,6}` fix is live there today and will not survive a reinstall.
- `docs/portability-contract.md` §1–§3 — canonical source format, portable frontmatter subset, `requires:` schema.
- `docs/authoring-portable-skills.md` + `lint.py` — authoring discipline and the portability lint the new skill must pass.
- `tests/test_lint.py`, `tests/test_talaria_watch.py` — the test shape to follow.
- `AGENTS.md` § File layout / Conventions — where a new skill and its config are expected to live.
- Handoff document that surfaced the bug: `MCP Server/.claude/handoffs/2026-08-23-031109-mcp-49-50-53-54-high-priority-sprint.md` (its Potential Gotchas section carries the original write-up).
- **INFRA-21** ("Build session handoff manifest rail", cancelled 2026-08-23) — prior art, not a duplicate: it covered building a handoff rail, which this skill superseded.
