# VHS-24 — Spec-lifecycle skills read AGENTS.md as canonical project instructions

**Ticket:** VHS-24 (Plane, priority Medium, Backlog, standalone; cross-references VHS-16/17/18)
**Brief:** `docs/specs/TODO/VHS-24.brief.md`

## Goal

Teach the three spec-lifecycle readers — `spec-cycle` preflight, `ship-spec` preflight, and the `spec-reviewer-conventions` agent — to treat a project's tracked, harness-neutral `AGENTS.md` as the canonical source for *portable* project instructions (conventions, workflow, build/test commands), while continuing to read *machine-local* values (the absolute `wiki_root` path, install dir) from the gitignored `CLAUDE.md`. The change is documentation-only (markdown skill/agent bodies — no executable code ships) and must be backward-compatible: a project that has only `CLAUDE.md` and no `AGENTS.md` keeps working unchanged.

## Scope

Files to change (repo source-of-truth; `sync.py` mirrors `skills/` and `agents/` into `~/.claude/`):

- **`skills/spec-cycle/SKILL.md`** — Phase 0 step 3 (lines 61–63): reads `CLAUDE.md` for test commands ("Build & Run"), the wiki path, and the project slug. Re-point the *portable* reads (test commands) at `AGENTS.md`-first; keep the *machine-local* read (wiki path) on `CLAUDE.md`; add the precedence rule.
- **`skills/ship-spec/SKILL.md`** — Phase 0 step 3 (line 17, conventions reference) and step 4.2 (line 21, the `CLAUDE.md` "Build & Run" test-command **fallback**), the failure message (line 26), and the guardrails note (line 90). Same precedence change. Step 4.1 (the spec's own `## Test command` as first source of truth) is unchanged.
- **`agents/spec-reviewer-conventions.md`** — frontmatter `description` (line 3), grounding step 2 (line 25, "Read `<project_root>/CLAUDE.md` end to end"), the "Stated conventions (CLAUDE.md)" axis (lines 65–67), the output-contract "Convention violated" hint (line 142), and the tool-use note (line 170). Read `AGENTS.md` (if present) **and** `CLAUDE.md`.

New file (single documentation source for the precedence rule):

- **`docs/customizing.md`** — already the documented home for "how downstream projects configure these skills via their own `AGENTS.md` / `CLAUDE.md`" (per `AGENTS.md` line 55). Add/confirm a short canonical **"Project-instruction precedence"** section that the three readers point at. *(If `docs/customizing.md` does not yet exist on disk, create it with just this section; the implementer confirms during ship-spec.)*

Files to leave alone:

- The vigil-skills `AGENTS.md` content itself (shipped in PR #19) — out of scope.
- `skills/spec-close/SKILL.md` — not a brief-named reader; it does not read `CLAUDE.md` for portable conventions. Leave alone.
- `states.json`, `sync.py`, `lint.py` — no change.
- Any other repo's `CLAUDE.md` — downstream projects opt in on their own.

## Decisions carried forward (from the brief)

1. **`AGENTS.md` = tracked, harness-neutral, canonical** portable instructions; **`CLAUDE.md` = machine-local tips + pointer** (Devin, 2026-06-14; PR #19). The design re-points only the *portable* reads at `AGENTS.md`; machine-local reads stay on `CLAUDE.md`.
2. **Machine-local values stay in `CLAUDE.md`.** The absolute wiki path (resolved as `wiki_root`) and install dir remain there and are still read from there. `AGENTS.md` must not carry machine-specific absolute paths, so the design must **not** move the wiki-path read to `AGENTS.md`.
3. **Backward-compatible (hard constraint).** These skills are public and used across many projects. Read `AGENTS.md` if present, **else fall back to** `CLAUDE.md`. A project with only `CLAUDE.md` must keep working unchanged. This is the primary correctness risk; the precedence + fallback is specified precisely below and the reviewers should probe the no-`AGENTS.md` path.

## Design

### Decision A — Canonical precedence rule, stated once and restated compactly

**The single documented source of truth** is a short section in `docs/customizing.md` (the file `AGENTS.md` already nominates for downstream configuration). Canonical text:

> **Project-instruction precedence.** At `<project_root>`, read `AGENTS.md` if it exists — it is the canonical source for *portable* instructions (conventions, workflow, build/test commands). Read `CLAUDE.md` for *machine-local* values (the absolute `wiki_root` path, the install dir) and as the **fallback** for portable instructions when `AGENTS.md` is absent. When both exist, `AGENTS.md` wins for portable instructions; `CLAUDE.md` still supplies machine-local values. A project with only `CLAUDE.md` (no `AGENTS.md`) keeps working unchanged.

**Why not share at runtime?** The skills and the agent are installed independently into `~/.claude/` and run against arbitrary downstream repos. A skill body cannot, at runtime, read a sibling skill file or a vigil-skills `docs/` file that won't be present in the target project. Therefore each of the three readers must be **self-contained**: it carries a compact inline restatement of the precedence rule (enough to act on) plus a pointer to `docs/customizing.md` for maintainers. "Define and document once" (brief) is honored by a single canonical prose home in `docs/customizing.md`; the inline restatements are the minimum required for self-containment, not duplicated logic. This is the deliberate resolution of the single-source-of-truth ↔ portable-self-containment tension — flagged here so the conventions reviewer reads it as an authorized (c)-class addition, not silent drift toward duplication.

### Decision B — Per-file edits (portable read → `AGENTS.md`-first; machine-local read stays on `CLAUDE.md`)

**`skills/spec-cycle/SKILL.md` (Phase 0 step 3).** Re-author step 3 so:
- **Test commands** (portable) — read from `AGENTS.md` ("Build & Run"/sync/test section) when present, else `CLAUDE.md`. *(spec-cycle does not run tests; it only identifies the command(s) so the authored spec's `## Test command` can reflect repo norms.)*
- **Wiki path** (machine-local) — **unchanged**: still read from `CLAUDE.md`, with the existing username-segment re-resolution.
- **Project slug** — read from `AGENTS.md` if stated there, else `CLAUDE.md` (typically the repo name; non-load-bearing).
- Prepend the compact precedence restatement + pointer to `docs/customizing.md`.
- Update the lead-in from "Read `<project_root>/CLAUDE.md`. Identify:" to name both files per precedence.

**`skills/ship-spec/SKILL.md`.**
- **Step 3 (line 17)** — "Read … conventions (build, lint, test, etc.)" re-pointed to `AGENTS.md`-first, `CLAUDE.md` for machine-local + fallback. Add the compact precedence restatement.
- **Step 4.2 (line 21)** — the test-command **fallback** changes from "`CLAUDE.md` 'Build & Run' second" to "`AGENTS.md` 'Build & Run' second (else `CLAUDE.md`)". **Step 4.1 (the spec's own `## Test command`) remains the first source of truth — unchanged.** The `N/A` exception is unchanged.
- **Failure message (line 26)** — update the "`CLAUDE.md` 'Build & Run' did not produce a parseable command" line to read "`AGENTS.md`/`CLAUDE.md` 'Build & Run' did not produce a parseable command."
- **Guardrails note (line 90)** — "Project-specific guardrails … live in `<project_root>/CLAUDE.md`" → "… live in `<project_root>/AGENTS.md` (machine-local guardrails in `CLAUDE.md`)."

**`agents/spec-reviewer-conventions.md`.**
- **Frontmatter `description` (line 3)** — "Reads CLAUDE.md, the project wiki…" → "Reads AGENTS.md / CLAUDE.md, the project wiki…".
- **Grounding step 2 (line 25)** — "Read `<project_root>/CLAUDE.md` end to end." → "Read `<project_root>/AGENTS.md` (if present) and `<project_root>/CLAUDE.md` end to end; `AGENTS.md` is canonical for portable conventions, `CLAUDE.md` for machine-local values and as fallback." Note both may be absent (already tolerated for the wiki; same posture).
- **"Stated conventions (CLAUDE.md)" axis (lines 65–67)** — rename heading to "Stated conventions (AGENTS.md / CLAUDE.md)"; bullets reference both.
- **Output contract (line 142)** — "Convention violated: <which CLAUDE.md rule …>" → "… AGENTS.md / CLAUDE.md rule …".
- **Tool-use note (line 170)** — add `AGENTS.md` alongside `CLAUDE.md` in the read list.
- **No new orchestrator-passed prompt field.** The agent already receives `project_root` and reads files under it directly; it discovers `AGENTS.md` itself. spec-cycle's step 2b reviewer prompt is therefore unchanged — keeping the change self-contained to the agent body and avoiding cross-file coupling.

### Decision C — `AGENTS.md` section names the readers look for

`AGENTS.md` is harness-neutral prose, not a rigid schema. The readers look for the same human section names they look for in `CLAUDE.md` today ("Build & Run" for commands, "Conventions" for rules). vigil-skills' own `AGENTS.md` uses "## Sync commands", "## Conventions", "## Architecture" — there is no literal "Build & Run" heading because this repo has no build step. The readers must therefore treat the section-name match as **best-effort prose scan, not exact-heading match** (consistent with how the conventions reviewer already reads `CLAUDE.md` "end to end"). For vigil-skills specifically, conventions come from `AGENTS.md` "## Conventions"; there is no runnable build/test command beyond the portability lint (see Test command), so a spec authored in this repo legitimately uses `lint.py` / `N/A`.

## Test plan

Documentation/instruction-only change (markdown skill + agent bodies; no executable behavior ships). The quality gate is the review checklist below, guarded mechanically by the portability lint.

**Automated guard (the Test command):** run the portability lint `--strict` over the three edited files to confirm no harness-coupling regression was introduced (the lint flags operative bare `mcp__*` tool calls and malformed `requires:` blocks per the portability contract). Edits are prose about reading `AGENTS.md`/`CLAUDE.md` and must keep the lint green.

**Review checklist (the substantive gate — maps to Done-when):**
1. **Precedence documented once.** `docs/customizing.md` carries the canonical "Project-instruction precedence" section; each of the three readers carries a compact restatement + pointer to it (no divergent wording).
2. **spec-cycle preflight** (step 3) reads `AGENTS.md` for test commands when present, `CLAUDE.md` for the wiki path (machine-local) and as fallback. The wiki-path read was **not** moved to `AGENTS.md`.
3. **ship-spec preflight** (steps 3 + 4.2 + failure message + guardrails note) reads `AGENTS.md`-first for conventions/test-command fallback, `CLAUDE.md` for machine-local + fallback. Step 4.1 (spec `## Test command`) and the `N/A` exception are unchanged.
4. **spec-reviewer-conventions** reads `AGENTS.md` (and `CLAUDE.md`) in grounding step 2; description, conventions axis, output contract, and tool-use note all reference both.
5. **No-regression / fallback:** by inspection, a project with only `CLAUDE.md` and no `AGENTS.md` follows the same path as today (every `AGENTS.md` read is guarded by an "if present, else `CLAUDE.md`" fallback). No reader hard-requires `AGENTS.md`.
6. **Self-containment:** no reader references a sibling skill file or a vigil-skills `docs/` path at *runtime* (pointers to `docs/customizing.md` are maintainer-facing comments only).
7. **Live source:** in this repo the skills now read vigil-skills' own tracked `AGENTS.md` (PR #19), not the gitignored `CLAUDE.md`, for portable conventions.
8. **Parity:** `python sync.py status` shows the edited `skills/` + `agents/` files as the only diffs vs `~/.claude/` (informational, run before the ship-spec sync step).

## Test command

```
python lint.py --strict skills/spec-cycle/SKILL.md skills/ship-spec/SKILL.md agents/spec-reviewer-conventions.md
```

Stdlib-only, no install. `--strict` exits non-zero on any ERROR (operative bare harness-tool call or malformed `requires:`); WARN (e.g., an agent file with no `requires:` block) never affects exit. This is the regression guard; the review checklist above is the substantive quality gate for the behavioral Done-when items, which are LLM-runtime instruction behavior and not unit-testable.

## Done when

1. `spec-cycle` and `ship-spec` preflight read `AGENTS.md` for conventions/test-command when present, `CLAUDE.md` for machine-local values + fallback; the precedence is documented in each skill body. *(checklist 1–3)*
2. `spec-reviewer-conventions` reads `AGENTS.md` (and `CLAUDE.md`) for repo rules. *(checklist 4)*
3. A project with only `CLAUDE.md` and no `AGENTS.md` still works (no regression) — demonstrated by inspection of the guarded fallback in every re-pointed read. *(checklist 5)*
4. vigil-skills' own `AGENTS.md` (PR #19) is the live source the skills read in this repo. *(checklist 7)*

## Out of scope

- Migrating other repos' `CLAUDE.md` → `AGENTS.md` (downstream projects opt in on their own).
- The `AGENTS.md` content itself (shipped in PR #19).
- Teaching skills to read any *other* harness's native instruction file (e.g. Hermes `SOUL.md`) — `AGENTS.md` + `CLAUDE.md` fallback only for v1.
- Any change to the Plane/wiki evidence-triple model.
- Adding a machine-parseable schema to `AGENTS.md` — reads stay best-effort prose scans (Decision C).
