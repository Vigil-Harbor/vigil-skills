# Spec: VHS-1 — Lift Plane reads from skills onto MCP webhook cache + Phase E sunset

> Status: v3 (post-round-2)
> Date: 2026-05-08
> Brief: docs/specs/TODO/VHS-1.brief.md
> Plane: VHS-1 (`62ac6daa-5f84-4d26-be43-d60296ce869d`)
> Blocked by: MCP-33 in production with at least one full state-transition cycle backfilled; VHS added to MCP server's `config/webhooks.json` `project_namespaces` (e.g., `"VHS": "vhs"`)

## Goal

Replace 6 synchronous Plane MCP reads in vigil-skills and wiki-state-update with `memory_search` calls against the MCP memory cache populated by MCP-33's webhook receiver. Add a committed `states.json` so ship-spec can resolve state UUIDs without calling `list_states` or `list_projects` at runtime. Ship the Phase E sunset paperwork (CLAUDE.md update, wiki decision page) in the same PR.

## Scope

### Modified files

| File | Change |
|------|--------|
| `skills/spec-cycle/SKILL.md` | Replace `mcp__plane__retrieve_work_item_by_identifier` with `memory_search` in tool-use notes; add namespace resolution from `states.json` in preflight |
| `agents/spec-reviewer-correctness.md` | Replace `retrieve_work_item_by_identifier` and `retrieve_work_item` with `memory_search` in grounding step (line 21) and tool-use rules (line 172) |
| `agents/spec-reviewer-edge-cases.md` | Replace `retrieve_work_item_by_identifier` with `memory_search` in grounding step (line 21) and tool-use rules (line 165) |
| `agents/spec-reviewer-conventions.md` | Replace `retrieve_work_item_by_identifier` with `memory_search` in tool-use rules (line 158) |
| `skills/ship-spec/SKILL.md` | Rewrite Phase 6 steps 1–2: read `states.json` instead of calling `list_projects` + `list_states`. Preflight `list_projects` reachability check (line 39) is preserved. |
| `vigil-harbor-wiki/.claude/skills/wiki-state-update/SKILL.md` | Replace `mcp__plane__retrieve_work_item` with `memory_search` for ticket state verification (line 27); retain `retrieve_work_item` as cold-cache fallback |
| `CLAUDE.md` | Update "External dependencies" section; add `states.json` to file layout |
| `docs/customizing.md` | Update the `list_states` reference (line 66) to describe the `states.json` lookup |

### New files

| File | Purpose |
|------|---------|
| `skills/ship-spec/states.json` | Committed config mapping project identifiers to project UUIDs, MCP namespaces, review-state IDs, and state-name-to-UUID maps |
| `vigil-harbor-wiki/decisions/2026-05-XX-plane-webhook-pivot.md` | Decision page capturing rationale for webhook-driven reads over synchronous Plane calls |

### Files NOT touched

- `skills/spec-cycle/SKILL.md` line 29 — preflight `list_projects` reachability check. Preserved: it costs one call and provides a useful "is Plane up" signal for outbound writes later in the workflow.
- `skills/ship-spec/SKILL.md` line 39 — preflight `list_projects` reachability check. Preserved: ship-spec performs outbound Plane writes in Phase 6 (`update_work_item`, `create_work_item_comment`); losing the preflight reachability signal would cause those writes to fail opaquely if Plane is down.
- `skills/ship-spec/SKILL.md` lines 221–222 — `update_work_item` and `create_work_item_comment`. Outbound writes; webhooks don't replace these.
- `skills/review-pr/SKILL.md` — no Plane reads.
- MCP Server repo — MCP-33 is a separate ticket. The VHS → `config/webhooks.json` addition is a prerequisite tracked in the Blocked-by line.

## Decisions

### D1: `states.json` keyed by project identifier, not project UUID

The brief's scope wrinkle asks whether `states.json` should be keyed by project identifier (`MCP`, `DYN`, `VHS`) or project UUID. **Key by identifier.** The ticket prefix IS the project identifier. Ship-spec already parses the ticket prefix (e.g., `MCP` from `MCP-33`) to resolve the project. Keying by identifier eliminates the `list_projects` call at ship-spec Phase 6 step 1 — the skill no longer needs to translate prefix → UUID because `states.json[prefix].project_id` provides it directly.

### D2: `states.json` includes `namespace` and `review_state_id` per project

The `memory_search` tool requires a `namespace` parameter (defaults to `"personal"`, which is wrong for Plane records). MCP-33 ingests records into project-specific namespaces (`MCP→mcp`, `DYN→dynasty`, etc. per `config/webhooks.json`). Rather than duplicating the namespace mapping in every skill, `states.json` includes a `namespace` field per project.

Additionally, each project has a `review_state_id` field that directly points to the UUID of the review-equivalent state (e.g., "In Review" for MCP, "PR Review" for DYN/VHS). This eliminates regex ambiguity: every project's `states` map contains both "Spec Review" and "In Review"/"PR Review", and the regex `/review|qa|in.review/i` matches both. An explicit `review_state_id` sidesteps the disambiguation problem entirely.

Spec-cycle reads `states.json` at preflight and passes the namespace to reviewer agents via their prompt.

### D3: `states.json` drift — opt-in validation, not hot-path cross-check (brief option b)

The brief offers three options for detecting states.json drift: (a) accept silent drift, (b) opt-in `--validate-states` flag, (c) separate maintenance script. **Choosing (b).** Ship-spec gains a `--validate-states` flag (documented, not implemented in the skill markdown — the implementer runs `list_states` manually and diffs against the file). This satisfies the acceptance criterion of zero `list_states` calls in the runtime path while providing a manual cross-check when drift is suspected. The flag is a note in the skill, not executable code — vigil-skills has no runtime.

### D4: Reviewer agents duplicate the `memory_search` snippet (no shared helper)

Three reviewer agents each gain the same 3-line pattern: `memory_search` → check for results → fall back to brief. The brief acknowledges the duplication smell and recommends duplicating for v1. A shared helper module isn't natural for skill-system markdown (skills are independent prompt documents, not importable code). Factor later if a fourth call site appears.

### D5: wiki-state-update gets its own namespace mapping

wiki-state-update is in a different repo (`vigil-harbor-wiki`) and can't read `states.json` from `vigil-skills`. It gets a small inline namespace mapping table (3 entries: MCP→mcp, DYN→dynasty, VHS→vhs). This is acceptable duplication: the wiki skill only needs project-slug → namespace, and the mapping changes when a new project adopts the workflow (rare, ~1/quarter).

### D6: Phase E ships in the same PR as Phase D

Per the brief's decision #4. Splitting risks "we'll write the decision page later" tail. The decision page is small; ship it together. The optional manifest cleanup (removing dead `tools:` entries from skill YAML) is the only deferrable bit — and we're deferring it (see Out of scope).

### D7: Cold-cache fallback matches today's Plane-outage behavior

When `memory_search` returns zero hits for a ticket, skills warn-and-proceed using the brief alone. This is the same behavior as today's Plane MCP outage path. No new failure mode for users.

**Exception:** wiki-state-update retains a `retrieve_work_item` fallback for cold-cache because the evidence triple is correctness-critical (per the state-edits-require-evidence decision). If both `memory_search` and `retrieve_work_item` return nothing, wiki-state-update refuses the edit per its existing refusal semantics. This is correct — do not silently proceed without evidence.

**Brief departure:** Brief acceptance criterion #6 (line 76) says "verified by running it with the Plane MCP server stopped." This spec intentionally relaxes that criterion: because the evidence triple is correctness-critical, a warm-cache-only guarantee is insufficient. The fallback to `retrieve_work_item` means wiki-state-update may call Plane MCP on cache miss. Done-when item 10 reflects this relaxed verification.

### D8: `docs/customizing.md` line 66 — rewrite the `list_states` reference

The customizing doc currently says ship-spec "probes `mcp__plane__list_states`." This becomes inaccurate. Rewrite to describe the `states.json` lookup. User-facing behavior is unchanged.

## Design

### 1. `states.json` schema and contents

File: `skills/ship-spec/states.json`

```json
{
  "MCP": {
    "project_id": "98788c4e-f30f-466d-9562-19e28aa4e53e",
    "namespace": "mcp",
    "review_state_id": "f724dfef-38e4-4a3e-8b60-9bad988a6829",
    "states": {
      "Backlog": "e9a009e5-58e1-4b19-8441-b17e686fa304",
      "Todo": "d8a725e9-d855-4df0-a515-11bd21e22dcb",
      "Ready to Ship": "61f619ab-c9a8-44b1-8e17-bab92748b8a6",
      "In Progress": "d003997d-ac55-4901-a412-7a149d43b414",
      "Spec Authoring": "ed4867e6-3c99-4143-b313-ddc91eadfad5",
      "Spec Review": "48e7cbfc-4cf0-448e-93de-5e894c24d057",
      "In Review": "f724dfef-38e4-4a3e-8b60-9bad988a6829",
      "Done": "2de7ddd1-932b-4bb5-b4b6-3af340134bf6",
      "Cancelled": "c38e4b91-2e58-44d8-a1ed-0ab645c7b6e3"
    }
  },
  "DYN": {
    "project_id": "60c4d66a-0b83-477f-b848-a80fcd8ce72c",
    "namespace": "dynasty",
    "review_state_id": "2f177294-83d8-4c9a-b74d-03bbc6826593",
    "states": {
      "Backlog": "9590c0ce-406c-43f9-ad89-3020d9121721",
      "Todo": "52277d44-ac3b-4698-8879-3366dc1b7dc0",
      "Ready to Ship": "761587ce-90ab-45e3-b41a-ae5cceb77e4a",
      "In Progress": "86e6bf8e-c596-4c13-853d-e695972442d1",
      "Spec Authoring": "2b2bb01d-8eb8-4a46-acd2-a8cd28a4c5f3",
      "Spec Review": "1c0c0587-02bf-48a3-9c01-98bd83894542",
      "PR Review": "2f177294-83d8-4c9a-b74d-03bbc6826593",
      "Done": "2f72aa3c-f999-4bf0-84aa-9b4f322a7e74",
      "Cancelled": "1323fe07-3abf-405a-a969-20a4561e4244"
    }
  },
  "VHS": {
    "project_id": "401bddd2-6d35-48e4-9c4e-e6d4fbec819d",
    "namespace": "vhs",
    "review_state_id": "c0e933ae-0094-443a-8cdb-9eb4190441e3",
    "states": {
      "Backlog": "0b42a227-5e4c-4345-aa9d-61c05b336395",
      "Todo": "9fe4453b-bf1c-4735-98b4-18db62bcb3ba",
      "Ready to Ship": "ef90a3a5-628e-4a31-b069-244fe4c871ff",
      "In Progress": "87718378-7a8e-4e1e-8296-78b78a6d6a22",
      "Spec Authoring": "b33ab308-de4a-4610-992b-ed53e7e92d3e",
      "Spec Review": "a50423f8-48a1-44ff-87e4-4f91d7eb10b9",
      "PR Review": "c0e933ae-0094-443a-8cdb-9eb4190441e3",
      "Done": "ba79301e-288a-48fa-8e66-4f8d8c66d618",
      "Cancelled": "b54dfa77-bee0-49c0-b413-c862ed63cddc"
    }
  }
}
```

State UUIDs fetched from Plane on 2026-05-08. The file is hand-maintained; adding a new project means one PR.

**Prerequisites:**
- MCP-33 must be in production with at least one state-transition cycle backfilled.
- VHS must be added to the MCP server's `config/webhooks.json` `project_namespaces` mapping (e.g., `"VHS": "vhs"`) before this ships. Without it, MCP-33's webhook handler falls back to namespace `"plane"` for VHS events, and the `namespace: "vhs"` in states.json won't match.

### 2. Replacement pattern: `memory_search` for ticket lookup

Every `retrieve_work_item_by_identifier` call is replaced with the same pattern:

```
memory_search(
  namespace: <namespace from states.json>,
  tags: ["plane_work_item", "<TICKET-ID>"],
  source_system: "plane",
  max_results: 1
)
```

Where `<TICKET-ID>` is the full identifier (e.g., `MCP-33`), matching the tag convention from MCP-33 spec §4 handler matrix: `Tags: ['plane_work_item', '<PROJ-N>']`.

**Fallback when zero results:** Warn and proceed using the brief alone. This matches today's Plane-outage behavior and covers the cold-cache case (ticket hasn't been touched since MCP-33 shipped).

**Error handling:** If `memory_search` returns a response starting with `"Error:"` (the MCP server convention for failures — tools return text, never throw), treat it as MCP memory outage. Warn (including the error text) and proceed using the brief alone.

**What the result provides:** The `memory_search` result contains the record's text content (description) and metadata (`{identifier, state, state_group, priority, assignees}` — per MCP-33 spec §4). This provides the same information as `retrieve_work_item_by_identifier`, minus the Plane HTML description (replaced by `description_stripped` text).

**Typical staleness:** Under 5 seconds (webhook delivery + ingestion latency). Worst case: up to 6 hours (reconciliation interval) if webhooks fail to deliver.

### 3. Per-file changes

#### 3a. `skills/spec-cycle/SKILL.md`

**Preflight (Phase 0):** After step 3 (read CLAUDE.md), add step 3b:

> 3b. Read `~/.claude/skills/ship-spec/states.json` (installed by `sync.py`). If the file is not found, default all namespaces to `"plane"` and warn — ticket lookup still works (MCP-33 fallback namespace is `"plane"` for unmapped projects); namespace-scoped precision is degraded but not broken. If the file exists, look up the ticket prefix to get the `namespace`. If the prefix is not in `states.json`, default namespace to `"plane"` and warn. Pass `namespace` to Phase 1's own `memory_search` call and to each reviewer agent in step 2b.

**Phase 1 — Author v1 spec:** The instruction "Read the brief, the linked Plane ticket (if reachable)..." changes from calling `retrieve_work_item_by_identifier` to calling `memory_search` with the pattern from §2 above, using the namespace resolved at step 3b.

**Phase 2b — Dispatch reviewers:** Each agent's prompt gains a new field: `namespace: <resolved namespace>`.

**Tool-use notes (line 208):** Replace:
```
- mcp__plane__retrieve_work_item_by_identifier for Plane ticket fetch.
```
With:
```
- mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search for Plane ticket lookup (tags: [plane_work_item, <TICKET-ID>], namespace from states.json). Falls back to brief alone on zero results or error response.
```

**Failure modes — "Plane unreachable":** Rename to "Ticket not in MCP memory cache" and update the text: "When `memory_search` returns zero results or an error for the ticket, warn-and-proceed using only the brief. The brief is the local source of truth. This covers cold-cache (ticket untouched since MCP-33 shipped) and MCP memory outage."

#### 3b. `agents/spec-reviewer-correctness.md`

**Grounding step 3 (line 21):** Replace:
```
3. **Retrieve the Plane ticket if a `ticket_id` is given.** Use `mcp__plane__retrieve_work_item_by_identifier`. The ticket's description and acceptance criteria are canonical when they conflict with the brief.
```
With:
```
3. **Retrieve the Plane ticket if a `ticket_id` is given.** Use `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` with `namespace` (from prompt context), `tags: ["plane_work_item", "<TICKET-ID>"]`, `source_system: "plane"`, `max_results: 1`. If zero results or error, note as a finding (P3 — "ticket not cached") and proceed using the brief. The ticket's description and acceptance criteria are canonical when they conflict with the brief.
```

**Tool-use rules (line 172):** Replace:
```
- Use `mcp__plane__retrieve_work_item_by_identifier` and `mcp__plane__retrieve_work_item` for ticket lookup. If Plane is unreachable, note it as a finding and proceed using the brief.
```
With:
```
- Use `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` for ticket lookup (tags: [plane_work_item, <TICKET-ID>], namespace from prompt context). If zero results or error, note as a P3 finding and proceed using the brief.
```

#### 3c. `agents/spec-reviewer-edge-cases.md`

**Grounding step 3 (line 21):** Replace:
```
3. **Retrieve the Plane ticket if `ticket_id` is given** via `mcp__plane__retrieve_work_item_by_identifier`.
```
With:
```
3. **Retrieve the Plane ticket if `ticket_id` is given** via `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` with `namespace` (from prompt context), `tags: ["plane_work_item", "<TICKET-ID>"]`, `source_system: "plane"`, `max_results: 1`. If zero results or error, proceed using the brief.
```

**Tool-use rules (line 165):** Replace:
```
- Use `mcp__plane__retrieve_work_item_by_identifier` for ticket lookup.
```
With:
```
- Use `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` for ticket lookup (tags: [plane_work_item, <TICKET-ID>], namespace from prompt context). If zero results or error, proceed using the brief.
```

#### 3d. `agents/spec-reviewer-conventions.md`

**Tool-use rules (line 158):** Replace:
```
- Use `mcp__plane__retrieve_work_item_by_identifier` for ticket lookup if needed.
```
With:
```
- Use `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` for ticket lookup if needed (tags: [plane_work_item, <TICKET-ID>], namespace from prompt context). If zero results or error, proceed using the brief.
```

#### 3e. `skills/ship-spec/SKILL.md`

**Preflight (line 39):** The existing `mcp__plane__list_projects` reachability check is **preserved** (ship-spec still needs Plane MCP reachable for Phase 6 outbound writes). Add a new step after it:

```
9. Read `skills/ship-spec/states.json` (from `~/.claude/skills/ship-spec/states.json` as installed by `sync.py`). Look up the ticket prefix (e.g., `MCP` from `MCP-33`). Confirm the prefix exists and has a `project_id`, `review_state_id`, and `states` map. If not found, **halt** — the project must be added to states.json before ship-spec can manage it.
```

**Phase 6 — Plane update (lines 216–222):** Replace steps 1–2:

Current:
```
1. Resolve the project: `mcp__plane__list_projects` → find the one whose identifier matches the ticket prefix.
2. Discover the review-equivalent state: `mcp__plane__list_states` for that project.
   - Prefer: `state.group == "started"` AND name matches `/review|qa|in.review/i`.
   - Fallback: any state with `state.group == "started"`.
   - If neither matches, warn and skip the state flip.
```

New:
```
1. Read `states.json` (already loaded at preflight). Look up the ticket prefix to get `project_id` and `review_state_id`.
2. Use `review_state_id` directly as the target state for the flip. If `review_state_id` is absent or empty, warn and skip the state flip — print available state names from `states.json` so the user can update manually.
```

Steps 3–4 (`update_work_item`, `create_work_item_comment`) remain unchanged — outbound writes still use the Plane MCP path.

#### 3f. `vigil-harbor-wiki/.claude/skills/wiki-state-update/SKILL.md`

**Line 27 — evidence triple, Plane state verification:** Replace:
```
1. **Plane state-at-time-of-check.** A Plane ticket URL or ID with the closure date. Use the Plane MCP tool (`mcp__plane__retrieve_work_item`) to fetch the current status; record the date checked. If no Plane ticket exists for the work, use `<PROJ>-?` as a placeholder and explicitly note the absence in the entry body.
```
With:
```
1. **Plane state-at-time-of-check.** A Plane ticket URL or ID with the closure date. Use `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` to fetch the cached ticket state: `namespace` from the project mapping below, `tags: ["plane_work_item", "<TICKET-ID>"]`, `source_system: "plane"`, `max_results: 1`. The record's `metadata.state_group` and `metadata.state` provide the current status; the MCP memory record's `observed_at` timestamp (set when the record was ingested or updated by the webhook handler) provides the date checked. If zero results or error, fall back to `mcp__plane__retrieve_work_item` (Plane may be ahead of the cache for tickets untouched since MCP-33 shipped). If both return nothing, refuse the edit — do not proceed without evidence. If no Plane ticket exists for the work, use `<PROJ>-?` as a placeholder and explicitly note the absence in the entry body.

   Project namespace mapping:
   | Plane prefix | Namespace |
   |---|---|
   | MCP | mcp |
   | DYN | dynasty |
   | VHS | vhs |
```

**Note:** wiki-state-update retains a fallback to `mcp__plane__retrieve_work_item` for the cold-cache case. This is intentional: the evidence triple is a correctness-critical gate (per the state-edits-require-evidence decision), so a zero-result from `memory_search` should try the live source before giving up. The other skills (spec-cycle, reviewers) don't have this requirement — they warn-and-proceed.

#### 3g. `CLAUDE.md` — External dependencies and file layout sections

**External dependencies:** Replace:
```
- **Plane MCP server** — ticket lookup and state updates. Skills warn-and-proceed if unreachable.
```
With:
```
- **Plane MCP server** — state updates (write) and reachability checks (preflight). Ticket reads now flow through MCP memory via `memory_search` (cached by MCP-33 webhook receiver). Skills warn-and-proceed on cache miss.
```

**File layout:** Add after the `sync.py` line:
```
- `skills/ship-spec/states.json` — Committed config mapping project identifiers to state UUIDs, MCP namespaces, and review-state IDs. Synced alongside SKILL.md by `sync.py`.
```

#### 3h. `docs/customizing.md` line 66

Replace:
```
`/ship-spec` flips a ticket to a review-equivalent state after PR open. The skill probes `mcp__plane__list_states` and prefers a started state matching `/review|qa|in.review/i`. If your Plane workspace has no such state, the skill skips the flip and reports the available states so you can update manually.
```
With:
```
`/ship-spec` flips a ticket to a review-equivalent state after PR open. The skill reads `skills/ship-spec/states.json` and uses the `review_state_id` field for the project. If your project isn't in `states.json` or has no `review_state_id`, the skill skips the flip and reports the available state names so you can update manually. To add a new project, run `mcp__plane__list_states` for the project and add an entry to `states.json`.
```

### 4. Decision page

File: `vigil-harbor-wiki/decisions/2026-05-XX-plane-webhook-pivot.md`

Template follows the established pattern (date, project, status, context, options, decision, consequences, related):

```markdown
# Decision: Plane ticket reads pivot from synchronous MCP to webhook-cached memory

> Date: 2026-05-XX (set to merge date)
> Project: VHS
> Status: active

## Context

The spec-cycle / ship-spec / wiki-state-update workflow made 8 synchronous
Plane MCP reads per run. MCP-33 shipped a webhook receiver that ingests
`plane_work_item` records into MCP memory on every Plane state change. 6 of
the 8 reads are now redundant — the same data is cached locally, refreshed
within seconds of any state change.

## Options Considered

### 1. Keep synchronous reads
Rejected. Each `retrieve_work_item_by_identifier` is a round-trip to Plane
through the MCP shim. Spec-cycle with 4 review rounds burns 4 redundant
reads on the same ticket. Plane MCP has been the flakiest dependency in the
chain.

### 2. Poll Plane on a schedule, cache locally
Rejected. Polling adds complexity (interval tuning, staleness window) and
doesn't leverage the webhook infrastructure MCP-33 already provides.

### 3. Replace reads with `memory_search` against webhook-cached records
Chosen. See ## Decision below.

## Decision

Replace 6 of 8 synchronous Plane MCP reads with `memory_search` calls
filtered by `tags=[plane_work_item, <TICKET-ID>]` against the MCP memory
cache. Add a committed `states.json` mapping project identifiers to state
UUIDs and review-state IDs, eliminating `list_states` and `list_projects`
from ship-spec's runtime path. Cold-cache fallback matches today's
Plane-outage behavior (warn-and-proceed using the brief alone).

## Consequences

**Enables:** Skills decouple from Plane MCP availability for reads. Single-digit ms
latency instead of round-trip through the MCP shim. `states.json` provides a
stable, versionable state mapping — no runtime `list_states` calls.
wiki-state-update retains `retrieve_work_item` fallback for cold-cache because
the evidence triple is correctness-critical.

**Costs:** MCP memory becomes a new dependency for ticket reads. Different blast
radius from Plane — unlikely to fail simultaneously. `states.json` is
hand-maintained. Adding a new project requires one PR. Drift risk bounded:
state UUIDs change rarely, opt-in `--validate-states` cross-check available.
wiki-state-update has a small inline namespace mapping table (3 entries),
duplicated from `states.json`, since it lives in a different repo.

**If reversed:** Revert the 6 skill/agent files to their pre-migration state. Delete
`states.json`. No data migration needed — `memory_search` records remain
in MCP memory regardless.

**Unchanged:** Preflight `list_projects` reachability checks in spec-cycle and
ship-spec. Outbound writes: `update_work_item` (state flip),
`create_work_item_comment`. wiki-state-update retains a `retrieve_work_item`
fallback for cold-cache (evidence triple is correctness-critical).

## Related
- MCP-33 spec (vigil-harbor/MCP Server repo) — Plane webhook receiver that populates the cache
- VHS-1 brief (vigil-harbor/vigil-skills repo, `docs/specs/TODO/VHS-1.brief.md`)
- [State edits require evidence](2026-04-29-state-edits-require-evidence.md) — why wiki-state-update retains the `retrieve_work_item` fallback
- [Tool namespacing](2026-04-29-tool-namespacing-double-underscore.md) — tool name format convention
```

The date placeholder (`XX`) is set to the merge date at commit time.

### 5. Wiki index update

Add the decision link to `vigil-harbor-wiki/index.md` in the decisions section, following the existing format.

## Test plan

This repo has no test suite (skills are markdown files, not executable code). Validation is end-to-end behavioral:

1. **Grep validation (automated, run in PR CI via CodeRabbit or manual):**
   - `grep -r 'mcp__plane__retrieve_work_item' skills/ agents/` → zero matches in runtime sections
   - `grep -r 'mcp__plane__list_states' skills/` → zero matches
   - `grep -r 'list_projects' skills/ship-spec/SKILL.md` → exactly one match: preflight reachability check (line 39, preserved); zero in Phase 6
   - `grep -r 'mcp__plane__retrieve_work_item' ../vigil-harbor-wiki/.claude/` → one match: the cold-cache fallback in wiki-state-update (explicitly documented)

2. **`states.json` schema validation:**
   - All three projects (MCP, DYN, VHS) present
   - Each has `project_id`, `namespace`, `review_state_id`, `states` with at least Backlog/In Progress/Done/Cancelled
   - `review_state_id` value matches an entry in the project's `states` map

3. **End-to-end smoke test (manual, post-MCP-33 production, pre-merge validation):**
   - Run `spec-cycle` on a known ticket (e.g., MCP-33 or VHS-1 itself) → verify the reviewer agents receive namespace and successfully query `memory_search`
   - Run `ship-spec` on a green-lit spec → verify Phase 6 reads states.json, uses `review_state_id`, and flips the ticket without calling `list_states` or `list_projects`
   - Run `wiki-state-update` on a recent shipped commit → verify it tries `memory_search` first; if cache is warm, evidence triple produced without `retrieve_work_item`; if cache is cold, verify fallback fires correctly
   - Diff spec-cycle output against pre-migration baseline on the same ticket. Differences should be limited to non-load-bearing prose (ordering, whitespace). Cite the diff command + result in the PR body.

4. **Sync validation:** `python sync.py push && python sync.py status` → clean diff

## Test command

```bash
python sync.py install --dry-run && python sync.py status && python -c "import json; json.load(open('skills/ship-spec/states.json'))"
```

No build or test suite exists for this repo. The sync command validates that all skill/agent files are well-formed and can be installed. The `json.load` call validates `states.json` syntax (stdlib only, matching the repo's no-dependency constraint). End-to-end validation is manual (see test plan §3).

## Done when

1. `grep -r 'mcp__plane__retrieve_work_item' skills/ agents/` returns zero hits in runtime call sites.
2. `grep -r 'mcp__plane__list_states' skills/` returns zero hits.
3. `grep -r 'mcp__plane__retrieve_work_item' ../vigil-harbor-wiki/.claude/` returns zero hits in runtime sections, except the explicit cold-cache fallback in wiki-state-update (which calls `retrieve_work_item` only when `memory_search` returns zero results).
4. `skills/ship-spec/states.json` exists with entries for MCP, DYN, VHS; ship-spec resolves the review-equivalent state from `review_state_id` without calling Plane.
5. `python sync.py status` shows clean diff after `python sync.py push`.
6. `vigil-harbor-wiki/decisions/2026-05-XX-plane-webhook-pivot.md` exists, follows the decisions/ template (## Decision, ## Consequences, ## Related), and is linked from `index.md`.
7. `CLAUDE.md` "External dependencies" section reflects that Plane reads flow through MCP memory. File layout section documents `states.json`.
8. `docs/customizing.md` describes the `states.json` lookup instead of `list_states`.
9. spec-cycle and ship-spec runs against a known ticket produce a spec diff against the pre-migration baseline that is either empty or limited to non-load-bearing prose. Diff command + result cited in the PR body. (Exercised post-MCP-33 production per the Blocked-by prerequisite.)
10. wiki-state-update produces a valid evidence triple on a recent shipped commit using `memory_search` as the primary path. Verified by confirming `memory_search` is called first; `retrieve_work_item` fallback fires only on cache miss. (Exercised post-MCP-33 production per the Blocked-by prerequisite.)

## Out of scope

1. **The webhook receiver itself (MCP-33)** — separate ticket, separate repo.
2. **Adding states for other projects** (CAL, CLT, DEM, INFRA, MED, ADA) — separate per-project actions when those projects adopt the workflow.
3. **Changes to Plane writes** (`update_work_item`, `create_work_item_comment`) — those stay on the live Plane MCP path.
4. **Adding new MCP tools** (e.g., `memory_search_plane` convenience wrapper) — reuse the generic `memory_search` surface.
5. **Replacing the Plane MCP server entirely** — still needed for writes.
6. **Pruning dead `tools:` entries from skill YAML frontmatter** — optional cleanup, deferrable to a follow-up.
7. **End-to-end smoke test execution** — requires MCP-33 in production. Done-when items 9–10 describe the procedure; execution happens post-MCP-33 ship per the Blocked-by prerequisite.
