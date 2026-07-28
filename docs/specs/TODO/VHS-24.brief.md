# VHS-24 — Spec-lifecycle skills read AGENTS.md as canonical project instructions

**Status:** Backlog · **Priority:** Medium · **Assignee:** Unassigned
**Created:** 2026-06-14 · **Plane:** VHS-24 (standalone; cross-references VHS-16/17/18)
**Origin:** The VHS-16/17/18 cross-harness spike and the AGENTS.md migration (PR #19). `CLAUDE.md` is gitignored in vigil-skills (it holds machine-local absolute paths), so the portable project instructions now live in a tracked, harness-neutral `AGENTS.md` at repo root; the local `CLAUDE.md` keeps only machine-local tips and points to it. But the spec-lifecycle skills and the conventions reviewer still read `CLAUDE.md` **directly** — they only work today because the machine-local wiki path stays in `CLAUDE.md` and the `CLAUDE.md → AGENTS.md` pointer is followed softly by the LLM. This item makes that integration explicit.

## Goal

Teach the spec-lifecycle skills to treat `AGENTS.md` as the canonical source for portable project instructions (conventions, workflow, test/build commands), while still reading machine-local values (e.g. the absolute `wiki_root` path) from the gitignored `CLAUDE.md`. No regression for downstream projects that have only a `CLAUDE.md` and no `AGENTS.md`.

## Scope

- **`spec-cycle` preflight** — currently reads `CLAUDE.md` for test commands, the wiki path, and conventions (Phase 0 step 3). Update to read `AGENTS.md` for conventions/test-commands; keep reading `CLAUDE.md` for machine-local values (wiki path) and as fallback.
- **`ship-spec` preflight** — reads `CLAUDE.md` "Build & Run" as the test-command fallback (Phase 0 step 4.2) and for conventions. Same precedence change.
- **`spec-reviewer-conventions`** — reads `CLAUDE.md` for "repo rules." Update to read `AGENTS.md` (and `CLAUDE.md`).
- **Precedence rule** — define and document, once, in a way all three consume: `AGENTS.md` is canonical for portable instructions; `CLAUDE.md` supplies machine-local values and acts as fallback when `AGENTS.md` is absent.

## Decisions carried forward

- **`AGENTS.md` = tracked, harness-neutral, canonical** portable instructions; **`CLAUDE.md` = machine-local tips + pointer** (Devin, 2026-06-14; PR #19).
- **Machine-local values stay in `CLAUDE.md`.** The absolute wiki path (resolved as `wiki_root` during preflight) and the install dir remain there and are still read from there — `AGENTS.md` must not carry machine-specific absolute paths.
- **Backward-compatible (hard constraint).** These skills are public and used across many projects; a project with only `CLAUDE.md` and no `AGENTS.md` must keep working unchanged. Read `AGENTS.md` if present, else fall back to `CLAUDE.md`. This is the main correctness risk — the spec must specify the precedence + fallback precisely and the reviewers should probe the no-AGENTS.md path.

## Done when

- `spec-cycle` and `ship-spec` preflight read `AGENTS.md` for conventions/test-command when present, `CLAUDE.md` for machine-local values + fallback; the precedence is documented in each skill body.
- `spec-reviewer-conventions` reads `AGENTS.md` (and `CLAUDE.md`) for repo rules.
- A project with only `CLAUDE.md` and no `AGENTS.md` still works (no regression) — demonstrated.
- vigil-skills' own `AGENTS.md` (PR #19) is the live source the skills read in this repo.

## Out of scope

- Migrating other repos' `CLAUDE.md` → `AGENTS.md` (downstream projects opt in on their own).
- The `AGENTS.md` content itself (shipped in PR #19).
- Teaching skills to read any *other* harness's native instruction file (e.g. Hermes `SOUL.md`) — `AGENTS.md` + `CLAUDE.md` fallback only for v1.
- Any change to the Plane/wiki evidence-triple model.

## References

- Plane: VHS-24 (standalone, priority Medium, created 2026-06-14).
- PR #19 — adds tracked `AGENTS.md`; slims local `CLAUDE.md` to machine-local + pointer.
- `docs/cross-harness-spike-synthesis.md` — the VHS-17/18 spike synthesis that surfaced this and the gitignored-`CLAUDE.md` finding.
- `skills/spec-cycle/SKILL.md` (Phase 0 step 3), `skills/ship-spec/SKILL.md` (Phase 0 step 4), `agents/spec-reviewer-conventions.md` — the three readers to update.
- Sibling cross-harness items: VHS-16 (epic), VHS-17 (portability contract), VHS-18 (authoring lint).
