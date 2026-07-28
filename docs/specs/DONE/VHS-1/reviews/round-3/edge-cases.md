# Edge-Cases Review -- round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Test plan grep count for `list_projects` is wrong | CLOSED | Spec v3 line 410: "exactly one match" |
| edge-cases | F-2 | Decision page relative links broken | CLOSED | Spec v3 lines 391-394: cross-repo references replaced with plain-text |
| edge-cases | F-3 | spec-cycle states.json missing-file edge case not handled | CLOSED | Spec v3 line 179: "If the file is not found, default all namespaces to 'plane' and warn" |
| edge-cases | F-4 | `updated_at` not in MCP-33 metadata schema | CLOSED | Spec v3 line 282: uses `observed_at` timestamp |
| edge-cases | F-5 | Decision page `## What's preserved` non-standard | CLOSED | Spec v3 line 385: folded into `## Consequences` as `**Unchanged:**` |
| edge-cases | F-6 | Phase 1 `memory_search` namespace reference unclear | CLOSED | Spec v3 line 181: "using the namespace resolved at step 3b" |
| correctness | F-1 | Test plan grep count wrong | CLOSED | Same as edge-cases F-1 |
| correctness | F-2 | Decision page `## What's preserved` non-standard | CLOSED | Same as edge-cases F-5 |
| conventions | F-1 | Decision page uses `###` sub-headings | CLOSED | Spec v3 lines 368-388: bold-text blocks |
| conventions | F-2 | Decision page `## What's preserved` non-standard | CLOSED | Same as edge-cases F-5 |
| conventions | F-3 | Cross-repo relative paths in `## Related` | CLOSED | Same as edge-cases F-2 |
| conventions | F-4 | `> Related:` frontmatter field non-standard | CLOSED | Spec v3: frontmatter reduced to Date/Project/Status only |
| conventions | F-5 | `namespace` not explicitly listed in reviewer prompt params | PARTIAL | Addressed well enough for implementation |
| conventions | F-6 | Brief deviation for wiki-state-update not acknowledged | CLOSED | Spec v3 line 79: "**Brief departure:**" explicitly acknowledges |
| conventions | F-7 | Test plan grep count for `list_projects` | CLOSED | Same as edge-cases F-1 |

## Findings

### F-1: `source_system` parameter omitted from tool-use rules replacements but present in grounding steps
**Severity:** P4
**Where:** spec.md:191, 213, 233, 244
**Edge case:** Inconsistent parameter specification across replacement sites
**What happens:** Grounding steps include `source_system: "plane"` but tool-use rules omit it. Both produce correct results since `tags: ["plane_work_item"]` already scopes the query.
**Suggested fix:** Add a note to section 2 that `source_system` is optional in brief reminders since the tag is unambiguous, or add it to tool-use rules for consistency.

### F-2: wiki-state-update fallback uses `retrieve_work_item` (UUID-based) but agent only has ticket identifier
**Severity:** P3
**Where:** spec.md:282
**Edge case:** Fallback path requires project UUID + work item UUID that the agent may not have when memory_search returns nothing
**What happens:** `retrieve_work_item` requires UUIDs. On cold-cache path, the agent only has a ticket identifier like "DYN-17". The agent would need `retrieve_work_item_by_identifier` instead.
**Suggested fix:** Change the fallback to `retrieve_work_item_by_identifier` (which takes project_identifier + issue_identifier), or add a note explaining UUID resolution.

### F-3: wiki-state-update namespace mapping table has no fallback for unknown project prefixes
**Severity:** P3
**Where:** spec.md:284-289
**Edge case:** New project not in the inline mapping table gets no namespace default
**What happens:** Unlike spec-cycle step 3b which defaults to "plane" on unknown prefix, wiki-state-update has no fallback. The `memory_search` call would use the wrong default namespace.
**Suggested fix:** Add fallback clause: "If the ticket prefix is not in the mapping table, default namespace to 'plane' and warn."

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 1

STATUS: GREEN
