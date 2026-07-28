# VHS-7 — Cursor Compatibility for /spec-cycle

## Goal

Make the spec-lifecycle skills (`spec-cycle`, `ship-spec`, `spec-reconcile`, `spec-retire`) and their three reviewer subagents host-agnostic by replacing hardcoded MCP tool names with capability descriptions, adding cross-platform path guidance, and documenting three edge cases that cause friction outside Claude Code: P2-only RED gating ambiguity, doc-only specs with no test command, and synthetic ticket IDs with no Plane backing.

## Scope

### Files to change

| File | Change type |
|------|-------------|
| `skills/spec-cycle/SKILL.md` | Replace 3 hardcoded MCP tool names; add Windows path note for `states.json`; add P2-only RED clarification; add doc-only/ops-only guidance; add synthetic ticket ID note |
| `skills/ship-spec/SKILL.md` | Replace 4 hardcoded MCP tool names; add Windows path note for `states.json`; add `N/A` test-command escape hatch |
| `skills/spec-reconcile/SKILL.md` | Replace 6 hardcoded MCP tool name occurrences (4 Plane, 2 memory); add Windows path note for `states.json` |
| `skills/spec-retire/SKILL.md` | Replace 4 hardcoded MCP tool name occurrences across 3 lines (all Plane); add Windows path note for `states.json` |
| `agents/spec-reviewer-correctness.md` | Replace 2 hardcoded MCP tool names |
| `agents/spec-reviewer-edge-cases.md` | Replace 2 hardcoded MCP tool names |
| `agents/spec-reviewer-conventions.md` | Replace 1 hardcoded MCP tool name |
| `docs/customizing.md` | Replace 1 hardcoded MCP tool name (`mcp__plane__list_states` on line 66) |

### Files to leave alone

- `sync.py` — works today; cross-platform path handling is a separate ticket per brief.
- `skills/ship-spec/states.json` — content unchanged; only references to its path are updated.

## Decisions

### Decision 1: Capability descriptions with full Claude Code example names

The brief recommends replacing hardcoded tool names with capability descriptions. The spec adopts a consistent pattern across all files:

**For Plane MCP tools:** Replace each hardcoded tool name with prose describing the capability, followed by the full Claude Code tool name as an example. Pattern: "call the Plane MCP server's project-list capability (e.g., `mcp__plane__list_projects` in Claude Code, or the equivalent in your host's Plane integration)".

**For MCP memory tools:** Same pattern: "call the MCP memory server's search capability (e.g., `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` in Claude Code, or the equivalent semantic-search tool in your host)".

**Rationale:** Keeping the full Claude Code tool name (including namespace prefix) in the example preserves grepability for Claude Code users and aligns with the `__` namespacing convention. The capability description in prose makes the intent clear to any host. This avoids inventing a variable/indirection layer while preserving both portability and discoverability.

### Decision 2: memory_search remains optional enrichment (carried from brief)

The existing fallback paths ("if zero results or error, proceed using the brief alone") are already correct. This spec formalizes that `memory_search` is enrichment, not a dependency, by making the capability-description phrasing say "if available" rather than implying it's required.

### Decision 3: states.json stays as a committed file (carried from brief)

No migration to env vars or config service. Only the path references change to include a Windows-compatible alternative.

### Decision 4: Scope expansion beyond the brief

The brief scoped to `spec-cycle/SKILL.md`, `ship-spec/SKILL.md`, and the three reviewer agents — those were the only spec-lifecycle skills when the brief was written. VHS-8 and VHS-9 subsequently added `spec-reconcile/SKILL.md` and `spec-retire/SKILL.md`, both containing the same hardcoded MCP tool names (using the `mcp__claude_ai_Plane__` prefix variant). This spec expands scope to include those files and `docs/customizing.md` (which has `mcp__plane__list_states`), honoring the brief's intent: host-agnostic tool references across all spec-lifecycle skills.

## Design

### 1. MCP tool-name replacement pattern

Each hardcoded tool name is replaced with a capability description following this template:

```
call the <server-name> server's <capability> capability
(e.g., `<full-claude-code-tool-name>` in Claude Code, or the equivalent in your host)
```

The replacements, file by file:

**`skills/spec-cycle/SKILL.md`:**
- Phase 0 step 5 (line 97, `mcp__plane__list_projects`): Replace with Plane project-list capability description.
- Phase 1 paragraph (line 106, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with MCP memory search capability description. Retain the parameter guidance (`tags`, `namespace`, `source_system`, `max_results`).
- Tool-use notes (line 278, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with capability description. Keep the parameter specification.

**`skills/ship-spec/SKILL.md`:**
- Phase 0 step 8 (line 39, `mcp__plane__list_projects`): Replace with Plane project-list capability description.
- Phase 6 step 3 (line 219, `mcp__plane__update_work_item`): Replace with Plane work-item state-update capability description.
- Phase 6 step 4 (line 220, `mcp__plane__create_work_item_comment`): Replace with Plane work-item comment capability description.
- Tool-use notes (line 256, `mcp__plane__*`): Replace wildcard with "Plane MCP tools (project listing, work-item state update, work-item comment) — or the equivalent capabilities in your host's Plane integration".

**`skills/spec-reconcile/SKILL.md`:**
- Phase 0 step 4 (line 14, `~/.claude/skills/ship-spec/states.json` reference — not a tool name, but included here for the `states.json` path note; see Design section 2).
- Phase 0 step 5 line in the preflight long line (line 15, `mcp__claude_ai_Plane__list_states` and `mcp__claude_ai_Plane__retrieve_work_item_by_identifier`): Replace with Plane state-list and work-item-lookup capability descriptions.
- Phase 1 step b (line 25, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with MCP memory search capability description.
- Tool-use notes (line 103, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with capability description.
- Tool-use notes (line 104, `mcp__claude_ai_Plane__list_states` and `mcp__claude_ai_Plane__retrieve_work_item_by_identifier`): Replace with Plane capability descriptions.

**`skills/spec-retire/SKILL.md`:**
- Phase 1 step 1 (line 30, `mcp__claude_ai_Plane__list_states(project_id)`): Replace with Plane state-list capability description.
- Phase 1 step 2 (line 31, `mcp__claude_ai_Plane__retrieve_work_item_by_identifier(...)`): Replace with Plane work-item-lookup capability description.
- Tool-use notes (line 251, `mcp__claude_ai_Plane__list_states` and `mcp__claude_ai_Plane__retrieve_work_item_by_identifier`): Replace with Plane capability descriptions.

**`agents/spec-reviewer-correctness.md`:**
- Grounding step 3 (line 22, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with MCP memory search capability description.
- Tool-use rules (line 173, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with capability description.

**`agents/spec-reviewer-edge-cases.md`:**
- Grounding step 3 (line 22, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with MCP memory search capability description.
- Tool-use rules (line 166, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with capability description.

**`agents/spec-reviewer-conventions.md`:**
- Tool-use rules (line 159, `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search`): Replace with capability description.

**`docs/customizing.md`:**
- Line 66 (`mcp__plane__list_states`): Replace with Plane state-list capability description.

### 2. Cross-platform states.json path

Four locations reference `~/.claude/skills/ship-spec/states.json`:
- `spec-cycle/SKILL.md` Phase 0 step 6 (line 98)
- `ship-spec/SKILL.md` Phase 0 step 9 (line 40)
- `spec-reconcile/SKILL.md` Phase 0 step 4 (line 14)
- `spec-retire/SKILL.md` Phase 0 step 6 (line 19)

Add a parenthetical after each: `(~/.claude/ on Unix; %USERPROFILE%\.claude\ on Windows)`. This matches the existing pattern at spec-cycle line 27 where wiki paths already have a platform fork.

### 3. P2-only RED status clarification

In `spec-cycle/SKILL.md`, after the loop-gating formula block (after the `If total_p0p1 == 0` line in section 2d), add:

> A reviewer may return `STATUS: RED` with only P2+ findings (P0=0 P1=0). This does not block the loop since the gate checks `total_p0p1 == 0`. P2+ items are advisory — they are carried forward as spec notes in the `## Deferred (P2+)` section but do not prevent the spec from going green.

### 4. Doc-only / ops-only test-gate escape hatch

**In `spec-cycle/SKILL.md` Phase 1**, after the `## Test command` bullet (after the interpreter-pinning guidance), add:

> For documentation-only or ops-only specs where no code ships (infrastructure configs, runbooks, wiki-only deliverables): set `## Test plan` to a review checklist describing what a human reviewer should verify. Set `## Test command` to `N/A`. When `ship-spec` encounters `Test command: N/A`, it skips the automated test gate (Phase 3) entirely. The review checklist in Test plan serves as the quality gate instead.

**In `ship-spec/SKILL.md` Phase 0 step 4**, insert between step 4.1 ("Spec § Test command first") and step 4.2 ("CLAUDE.md fallback"):

> **Exception: `N/A` test command.** After reading the `## Test command` section, extract its raw text content (strip markdown code fences if present, trim leading/trailing whitespace). If the resulting string matches `N/A` (case-insensitive), record the resolved test command as `N/A` and do not fall through to step 4.2 or 4.3. When Phase 3 encounters a resolved test command of `N/A`, skip the test gate loop entirely — Phase 2 (implementation) still runs normally, then proceed directly to Phase 4 (commit). The spec's `## Test plan` review checklist is the quality gate for doc-only and ops-only changes.

### 5. Synthetic / local-only ticket ID handling

In `spec-cycle/SKILL.md` Phase 0, after step 2 (brief existence check), add:

> **Local-only ticket IDs.** If the filename's ticket ID does not match an existing Plane issue (the MCP memory lookup in Phase 1 returns zero results, and no Plane issue is reachable), treat the brief as local-only. The skill proceeds using the brief alone — this is the normal fallback path, not an error. Create the Plane issue when scope is confirmed, then rename all `<TICKET-ID>.*` artifacts under `docs/specs/TODO/` (brief, spec, reviews directory, test output) to match the real ticket ID.

## Test plan

Since this is a documentation-only change (editing `.md` skill and agent files), there is no automated test suite to run. The verification is:

1. **sync.py install --dry-run**: Confirm the sync script still correctly identifies all skill and agent files and would install them without path errors.
2. **sync.py install**: Actually install the updated files to `~/.claude/` and confirm no breakage.
3. **Grep audit**: Verify zero remaining hardcoded MCP tool names across all changed files. Run against specific in-scope paths:
   ```
   grep -rE "mcp__(plane__|claude_ai_Plane__|claude_ai_Vigil_Harbor_MCP_Server__)" \
     skills/spec-cycle/SKILL.md \
     skills/ship-spec/SKILL.md \
     skills/spec-reconcile/SKILL.md \
     skills/spec-retire/SKILL.md \
     agents/spec-reviewer-correctness.md \
     agents/spec-reviewer-edge-cases.md \
     agents/spec-reviewer-conventions.md \
     docs/customizing.md
   ```
   This should return zero results. The regex covers all three MCP tool-name prefix patterns: `mcp__plane__`, `mcp__claude_ai_Plane__`, and `mcp__claude_ai_Vigil_Harbor_MCP_Server__`.
4. **Spot-check**: Read each changed file end-to-end to confirm capability descriptions are consistent, the `states.json` path parentheticals are present, and the three new documentation sections (P2-only RED, doc-only escape hatch, synthetic ticket IDs) read clearly.

## Test command

```
python sync.py install --dry-run && python sync.py install
```

## Done when

1. No hardcoded MCP tool names remain in `spec-cycle/SKILL.md`, `ship-spec/SKILL.md`, `spec-reconcile/SKILL.md`, `spec-retire/SKILL.md`, the three reviewer agent files, or `docs/customizing.md`. Tool references use capability descriptions with full Claude Code tool names as examples.
2. `states.json` path references include a Windows-compatible alternative (`%USERPROFILE%\.claude\` parenthetical) in all four skill files that reference it.
3. Spec-cycle loop-gating section explicitly documents P2-only RED behavior.
4. Spec-cycle Phase 1 includes guidance for doc-only / ops-only specs (Test command = N/A).
5. Spec-cycle Phase 0 documents local-only / synthetic ticket ID handling (with full artifact rename guidance).
6. Ship-spec Phase 0 step 4 includes the `N/A` escape hatch between steps 4.1 and 4.2, with exact parsing rule.
7. `sync.py install` still works after all edits (no path breakage).

## Out of scope

- Refactoring `sync.py` for cross-platform path handling (works today; separate ticket if needed).
- Adding Cursor-specific integration tests or CI.
- Changing the parallel-review architecture (confirmed working by Devin's feedback).
- Migrating `states.json` content to environment variables or a config service.
