# VHS-7 — Cursor Compatibility for /spec-cycle

## Origin

Feedback captured by Devin after running `/spec-cycle` end-to-end inside Cursor (rather than Claude Code). The ticket is a raw list of friction points; this brief distills them into addressable work items.

## Problem

The spec-lifecycle skills (`spec-cycle`, `ship-spec`) and their three reviewer subagents assume a Claude Code runtime environment. Hardcoded MCP tool names, Unix-only path conventions, and undocumented edge cases cause friction or silent failures when the same skills are invoked from Cursor, Windsurf, or any non–Claude Code host.

Making the skills host-agnostic improves portability for Vigil Harbor's own multi-editor workflow and is a prerequisite for the public release posture noted in the project instructions.

## Findings (verified against current source)

### 1. Hardcoded MCP tool names

`spec-cycle/SKILL.md` (lines 97, 106, 278) and all three reviewer agents hardcode `mcp__plane__list_projects` and `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`. In Cursor, Plane surfaces as `user-plane` tools (`list_projects`, `retrieve_work_item_by_identifier`, …) — a different namespace.

**Recommendation:** Replace hardcoded tool names with capability descriptions. Example: "invoke the workspace Plane MCP (`list_projects` or equivalent)" and "invoke the MCP memory server (`memory_search` or equivalent)". Keep `memory_search` as optional enrichment, not a hard dependency.

### 2. Unix-centric `states.json` path

`ship-spec/SKILL.md` (line 40) and `spec-cycle/SKILL.md` (line 98) reference `~/.claude/skills/ship-spec/states.json`. The tilde resolves on macOS/Linux but is not a native Windows path. Cursor on Windows resolved it anyway (likely via shell expansion), but it's fragile.

**Recommendation:** Add a parenthetical: "(`~/.claude/` on Unix; `%USERPROFILE%\.claude\` on Windows)". Spec-cycle line 27 already has analogous platform-fork guidance for wiki paths — extend the same pattern here.

### 3. P2-only RED status ambiguity

The review loop (spec-cycle lines 165–170) gates on `total_p0p1 == 0`. A reviewer returning `RED P0=0 P1=0 P2=1` is technically "green" by the gating formula, but the `RED` status label creates ambiguity for the operator reading the output.

**Recommendation:** Add one clarifying line to the loop-gating section: "A reviewer may return RED with only P2+ findings; this does not block the loop since P0+P1 == 0. P2 items are advisory and carried forward as spec notes."

### 4. Doc-only / ops-only specs lack a test-gate escape hatch

`spec-cycle` (line 112) requires a `## Test command` section. `ship-spec` (lines 21–28) halts if no runnable command is found. Documentation-only or ops-only specs (infrastructure configs, runbooks, wiki-only deliverables) have no automated test to run.

**Recommendation:** Add a half-paragraph in spec-cycle Phase 1: "For documentation or ops-only specs where no code ships: `## Test plan` = review checklist; `## Test command` = `N/A` or a forward-reference to a future ticket. `ship-spec` will skip the automated test gate when Test command is `N/A`."

### 5. Synthetic / local-only ticket IDs

The skill's `docs/specs/TODO/<TICKET-ID>.brief.md` naming convention assumes the ticket ID exists in Plane. When a user says "CLT-17" but means a new workstream (no Plane issue yet), they must either create a Plane issue first or invent a synthetic ID like `CLT-PILOT-PERF`.

**Recommendation:** Add a note in Phase 0: "If the filename ticket ID does not match an existing Plane issue, treat the brief as local-only. The skill will proceed using the brief alone (memory lookup returns zero results). Create the Plane issue when scope is confirmed, then rename the brief file."

## What the feedback confirms works well

Three parallel Agent calls mapping to three Task subagents with the same prompt bundle — the Cursor agent noted this "works well." No changes needed to the parallel-review architecture.

## Decisions carried forward

- `memory_search` remains optional enrichment (already has a fallback path; this brief formalizes the intent).
- Reviewer agents are read-only by convention; this brief does not change that.
- `states.json` stays committed as a file (not migrated to env vars or a config service).

## Done when

1. No hardcoded MCP tool names remain in `spec-cycle/SKILL.md`, `ship-spec/SKILL.md`, or the three reviewer agent files. Tool references use capability descriptions with example names.
2. `states.json` path references include a Windows-compatible alternative.
3. Spec-cycle loop-gating section explicitly documents P2-only RED behavior.
4. Spec-cycle Phase 1 includes guidance for doc-only / ops-only specs (Test command = N/A).
5. Spec-cycle Phase 0 documents local-only / synthetic ticket ID handling.
6. `sync.py install` still works after all edits (no path breakage).

## Out of scope

- Refactoring `sync.py` for cross-platform path handling (works today; separate ticket if needed).
- Adding Cursor-specific integration tests or CI.
- Changing the parallel-review architecture (confirmed working).
- Migrating `states.json` content to environment variables or a config service.
