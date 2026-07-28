# VHS-8 — /spec-reconcile + /spec-retire: post-convention spec retirement pipeline

**Status:** Todo · **Priority:** Medium · **Assignee:** —
**Created:** 2026-05-15 · **Plane:** VHS-8
**Origin:** Phase 1 of the [spec migration manifest](../../../vigil-harbor-wiki/triage/2026-05-12-spec-migration-manifest.md)
(2026-05-12). The manifest inventoried 22 post-convention specs with closed Plane tickets
across 4 projects, plus 2 partial-retire candidates. This ticket implements the two skills
that process that backlog.

## Problem

Closed specs accumulate in `docs/specs/TODO/` across multiple repos after implementation
ships. The knowledge they encode — design decisions, edge-case rationale, acceptance
criteria — is trapped in files nobody reads post-merge. The wiki is the intended long-term
home for this context, but the decomposition from "spec file" to "wiki entries + archived
spec" is currently a manual, error-prone process that nobody runs consistently.

Today's state:

- 22 specs are ready for full retirement (verified closed in Plane).
- 2 specs (DYN-34, DYN-34b) need partial retirement (code shipped, parent ticket open).
- No automated pipeline exists to reconcile spec-vs-code drift or decompose specs into
  wiki-friendly knowledge units.

## Why it matters

1. **Knowledge decay.** Specs reference line numbers, function names, and architecture
   that drifts within weeks of shipping. Without reconciliation, the spec becomes
   misleading — worse than absent.
2. **Wiki completeness.** The wiki's `decisions/` and `comprehension/` directories are
   the canonical knowledge layer. Unretired specs leave gaps in the wiki's coverage.
3. **Clutter and signal/noise.** `TODO/` directories filled with closed-ticket specs
   obscure the active work surface.
4. **Scale.** 22 specs now, growing with every shipped ticket. Manual retirement doesn't
   scale; the backlog will only grow.

## Scope

Two new skills in `vigil-skills/skills/`:

### `/spec-reconcile <spec-path>`

Diff a closed spec against shipped code. Produces a reconciliation report confirming
implementation matches spec intent, or flags drift.

**Inputs:** Path to a spec file (e.g., `docs/specs/TODO/VHS-3.spec.md`).

**Outputs:** A reconciliation report — structured findings on:
- Which acceptance criteria are met in code (with grep evidence).
- Which aspects drifted (spec said X, code does Y).
- Which spec elements were descoped or deferred.

**Key behaviors:**
- Read-only — never edits code or spec files.
- Must verify Plane ticket state via `list_states` using `group == "completed"` (not
  hardcoded UUIDs). Warn-and-halt if ticket is not in a completed state.
- Produces output suitable for `/spec-retire` to consume (machine-readable reconciliation
  status at the end, e.g., `RECONCILED: true` or `RECONCILED: false, DRIFT_COUNT: N`).

### `/spec-retire <spec-path> [--partial]`

Decomposes a reconciled spec into wiki entries, archives the spec file and companions,
and appends to wiki `log.md`.

**Inputs:** Path to a spec file that has already been reconciled.

**Outputs:**
- Proposed wiki entries: `decisions/<date>-<slug>.md` and/or `comprehension/<date>-<slug>.md`.
- `state.md` update proposal (with evidence triple per wiki convention).
- Archive operation: moves spec + brief + reviews to `docs/specs/DONE/<TICKET-ID>/`.
- `log.md` append in wiki.

**Key behaviors:**
- Checks Plane ticket state via `list_states` using `group == "completed"`.
- **Duplicate detection:** before proposing wiki entries, scans `decisions/` and
  `comprehension/` for pre-existing entries that cover the same ticket or topic.
  Skips rather than duplicates.
- **Partial mode (`--partial`):** for specs where implementation shipped but parent
  Plane ticket stays open (e.g., DYN-34/34b). Skips wiki decomposition (already done)
  and state.md flip (parent still active). Archives spec files only + log.md append.
  Detect via `group == "started"` on the parent ticket.
- Respects wiki evidence-triple convention for state.md edits (Plane-ID, date,
  commit hash + `Verification:` grep line).
- Halts for user confirmation before writing any files.

## Approach

1. **Skill structure mirrors existing conventions.** Each skill gets
   `skills/<name>/SKILL.md` with YAML frontmatter, phased execution (preflight → work →
   output), and explicit halt-points for user confirmation. Follow the patterns
   established by `spec-cycle` and `ship-spec`.

2. **`/spec-reconcile` phases:**
   - Phase 0 (Preflight): resolve spec path, extract ticket-id, verify Plane state.
   - Phase 1 (Code grep): for each acceptance criterion in the spec, produce a grep or
     file-read confirming presence/absence in the shipped code.
   - Phase 2 (Drift analysis): compare spec's stated approach against actual
     implementation. Note any divergences.
   - Phase 3 (Report): emit structured reconciliation report to stdout + optionally
     write to a sibling file `<TICKET-ID>.reconciliation.md`.

3. **`/spec-retire` phases:**
   - Phase 0 (Preflight): resolve spec path, confirm reconciliation status, verify
     Plane state, detect partial-retire case.
   - Phase 1 (Duplicate scan): scan wiki `decisions/` and `comprehension/` for existing
     coverage.
   - Phase 2 (Decomposition): extract decision-worthy and comprehension-worthy content
     from the spec. Propose wiki entries with proper frontmatter and anchors.
   - Phase 3 (State.md update): propose state.md edits with evidence triples.
   - Phase 4 (Archive): move spec + companions to `DONE/<TICKET-ID>/` (or project's
     equivalent pattern — model-adapter uses `DONE/<TICKET>/spec.md` folder convention).
   - Phase 5 (Log): append to wiki `log.md`.
   - Phase 6 (User review): present all proposed changes for confirmation before writing.

4. **Plane state resolution.** Both skills call `list_states` for the relevant project
   and match on `group == "completed"` rather than hardcoding state UUIDs. This is
   future-proof and matches the pattern established in VHS-1's `states.json`.

5. **Pilot on ADA-17.** Per manifest recommendation — it's a small, self-contained spec
   with clear acceptance criteria and no partial-retire complexity.

## Acceptance

- `/spec-reconcile` produces a correct reconciliation report for ADA-17 that verifies
  acceptance criteria against shipped code with grep evidence.
- `/spec-retire` (full mode) decomposes ADA-17 into at least one wiki entry, archives
  the spec file, and appends to `log.md`.
- `/spec-retire --partial` correctly handles DYN-34: archives spec + companions,
  appends to log.md, does NOT propose wiki decomposition or state.md flip.
- Both skills correctly gate on Plane ticket state (reject if not completed/started
  respectively).
- Duplicate detection prevents proposing a wiki entry that already exists.
- No hardcoded state UUIDs anywhere — all state matching uses `group ==` comparisons.
- Skills follow vigil-skills conventions: YAML frontmatter, `user_invocable: true`,
  phased structure.

## Risks / decisions

- **Reconciliation depth.** How thoroughly should `/spec-reconcile` verify acceptance
  criteria? A shallow grep may miss semantic drift; deep analysis risks hallucination.
  Recommend: grep + file-read with explicit "UNVERIFIABLE" status for criteria that
  can't be confirmed via text search (e.g., "latency < 50ms"). Let the user make the
  call on those.

- **Archive location convention.** Different repos use different patterns:
  vigil-skills/MCP Server use flat `TODO/` → should move to `DONE/<TICKET-ID>/`;
  model-adapter already uses `DONE/<TICKET>/spec.md`. The skill should detect which
  convention the target repo uses and follow it. If neither exists, default to
  `DONE/<TICKET-ID>/`.

- **Wiki entry granularity.** A single spec might yield zero, one, or multiple wiki
  entries. The skill should propose candidates and let the user accept/reject/merge.
  Don't force 1:1 spec-to-wiki-entry mapping.

- **Cross-repo operation.** `/spec-retire` reads from the spec's repo but writes to the
  wiki repo. The skill needs the wiki path — source from `CLAUDE.md` (already the
  convention for `spec-cycle` and `ship-spec`).

- **Reconciliation file persistence.** Should the reconciliation report be written to
  disk or just emitted to stdout? Recommend: write to disk as
  `<TICKET-ID>.reconciliation.md` alongside the spec. It's useful audit trail and
  `/spec-retire` can read it to skip re-analysis.

## References

- Plane: VHS-8
- Manifest: `vigil-harbor-wiki/triage/2026-05-12-spec-migration-manifest.md`
- Existing skill patterns: `skills/spec-cycle/SKILL.md`, `skills/ship-spec/SKILL.md`
- Wiki conventions: `vigil-harbor-wiki/SCHEMA.md`
- State.md evidence requirement: `vigil-harbor-wiki/decisions/2026-04-29-state-edits-require-evidence.md`
- VHS-1 `states.json` pattern: `skills/ship-spec/states.json`
- Recommended pilot: ADA-17 (`model-adapter/docs/specs/DONE/ADA-17/spec.md`)
- Partial-retire candidates: DYN-34, DYN-34b
