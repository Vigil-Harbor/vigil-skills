# Edge-Cases Review -- round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Ship-spec preflight `list_projects` replaced despite brief preserving it | CLOSED | spec v2 lines 38, 247: preflight preserved, only Phase 6 steps 1-2 replaced |
| correctness | F-2 | Decision page contradicts section 3e on ship-spec preflight | CLOSED | spec v2 line 390: "Preflight `list_projects` reachability checks in spec-cycle and ship-spec" now consistent with section 3e line 247 |
| correctness | F-3 | Two brief acceptance criteria missing from Done-when | CLOSED | spec v2 lines 449-450: items 9-10 added |
| correctness | F-4 | `sync.py` direction mismatch (install vs push) | CLOSED | spec v2 line 445: "clean diff after `python sync.py push`" |
| correctness | F-5 | wiki-state-update replacement drops `<PROJ>-?` placeholder guidance | CLOSED | spec v2 line 280: `<PROJ>-?` placeholder text restored |
| correctness | F-6 | Phase 6 fallback logic changes from group-based to name-based | CLOSED | spec v2 D2 (line 49-53): `review_state_id` eliminates need for group-based fallback |
| correctness | F-7 | Primary preference regex drops `state.group` constraint | CLOSED | spec v2 D2: `review_state_id` sidesteps regex entirely |
| edge-cases | F-1 | Decision page contradicts section 3e on ship-spec preflight | CLOSED | Same as correctness F-2 |
| edge-cases | F-2 | Review-state regex ambiguity | CLOSED | spec v2 D2: `review_state_id` per project |
| edge-cases | F-3 | wiki-state-update cold-cache fallback contradicts Done-when #3 | CLOSED | spec v2 line 443: Done-when #3 now explicitly allows the cold-cache fallback |
| edge-cases | F-4 | VHS not in webhooks.json | CLOSED | spec v2 line 7: added to Blocked-by prerequisites |
| edge-cases | F-5 | states.json has no state_group metadata | CLOSED | spec v2 D2: `review_state_id` eliminates need for state_group |
| edge-cases | F-6 | spec-cycle reads states.json from project_root | CLOSED | spec v2 line 177: simplified to `~/.claude/skills/ship-spec/states.json` |
| edge-cases | F-7 | memory_search staleness window not documented | CLOSED | spec v2 line 169: "Typical staleness: Under 5 seconds... Worst case: up to 6 hours" |
| edge-cases | F-8 | memory_search error response not handled | CLOSED | spec v2 line 165: "If `memory_search` returns a response starting with `Error:`..." |
| edge-cases | F-9 | Test plan contradicts design for wiki-state-update fallback | CLOSED | spec v2 line 426: test plan now says "verify it tries memory_search first; if cache is cold, verify fallback fires correctly" |
| edge-cases | F-10 | No JSON validity check for states.json | CLOSED | spec v2 line 434: `python -c "import json; json.load(open('skills/ship-spec/states.json'))"` added |
| conventions | F-1 | Internal contradiction -- ship-spec preflight | CLOSED | Same as correctness F-1/F-2 |
| conventions | F-2 | Spec deviates from brief on ship-spec preflight without acknowledgment | CLOSED | spec v2 section 3e line 247: preflight preserved |
| conventions | F-3 | Decision page template drift -- missing sections | CLOSED | spec v2 lines 356, 365, 395: `## Decision`, `## Consequences`, `## Related` all present |
| conventions | F-4 | Decision page missing ## Related section | CLOSED | spec v2 line 395: `## Related` added |
| conventions | F-5 | states.json is first non-SKILL.md file; CLAUDE.md not updated | CLOSED | spec v2 section 3g line 303-305: file layout update specified |
| conventions | F-6 | Phase 6 fallback loses state.group filtering | CLOSED | spec v2 D2: `review_state_id` |
| conventions | F-7 | spec-cycle states.json read path ambiguity | CLOSED | spec v2 line 177: simplified |

## Findings

### F-1: Test plan grep count for `list_projects` is wrong -- says "exactly two" but should be "exactly one"
**Severity:** P0
**Where:** spec.md:415
**Edge case:** Internal inconsistency in the spec -- grep assertion that cannot be satisfied by the post-migration code
**What happens:** After the spec's changes, Phase 6 steps 1-2 no longer mention `list_projects` (replaced by states.json at lines 266-267). Only the preflight check at line 39 survives. `grep -r 'list_projects' skills/ship-spec/SKILL.md` would return exactly 1 match, not 2. An implementer validating against this criterion would either think the implementation is wrong or think the spec is wrong.
**Why the spec misses it:** The spec correctly removes `list_projects` from Phase 6 (section 3e, lines 253-268) but the test plan assertion at line 415 still claims "exactly two matches." The phrase "zero in Phase 6" is descriptive of the new state but the "exactly two" count includes the old Phase 6 reference that no longer exists.
**Suggested fix:** Change line 415 from "exactly two matches: preflight reachability check (line 39, preserved) and zero in Phase 6" to "exactly one match: preflight reachability check (line 39, preserved); zero in Phase 6."

### F-2: Decision page relative links are broken -- three `../` levels instead of two
**Severity:** P1
**Where:** spec.md:396-398
**Edge case:** Malformed cross-repo relative paths in the decision page template
**What happens:** The decision page lives at `vigil-harbor-wiki/decisions/2026-05-XX-plane-webhook-pivot.md`. From `decisions/`, going up one level reaches `vigil-harbor-wiki/`, and one more reaches `Vigil-Harbor/` (the parent containing all sibling repos). The spec uses `../../../MCP Server/...` and `../../../vigil-skills/...` (3 levels up), which resolves to `C:\Users\zioni\Documents\MCP Server\...` -- a path that does not exist. The correct relative path is `../../MCP Server/...` (2 levels up from `decisions/` to `Vigil-Harbor/`).
**Why the spec misses it:** Off-by-one in directory traversal depth. The author may have counted from the file itself rather than from the directory the file is in.
**Suggested fix:** Change all three `../../../` prefixes on lines 396-398 to `../../`:
- `[MCP-33 spec](../../MCP Server/docs/specs/TODO/MCP-33.spec.md)`
- `[VHS-1 brief](../../vigil-skills/docs/specs/TODO/VHS-1.brief.md)`
- Note: The `2026-04-29-state-edits-require-evidence.md` and `2026-04-29-tool-namespacing-double-underscore.md` references on lines 398-399 are sibling files in the same `decisions/` directory, so their bare-filename form is correct.

### F-3: spec-cycle states.json missing-file edge case not handled
**Severity:** P2
**Where:** spec.md:177
**Edge case:** `~/.claude/skills/ship-spec/states.json` does not exist (user has not run `sync.py install` after the file was added to the repo, or the install path was customized)
**What happens:** Spec-cycle preflight step 3b says "Read `~/.claude/skills/ship-spec/states.json`... If the prefix is not in `states.json`, default namespace to `"plane"` and warn." This handles the case where the file exists but the prefix is missing, but does not describe what to do when the file itself is absent. The `Read` tool would return an error; the spec doesn't tell the implementer whether to halt, warn, or default all namespaces to `"plane"`. Ship-spec (line 250) handles this more rigorously: "If not found, **halt**." The asymmetry is defensible (spec-cycle reads are soft, ship-spec writes are hard), but the missing-file case should be explicit for spec-cycle too.
**Why the spec misses it:** The spec only addresses the "prefix not found" case, not the "file not found" case. These are distinct failure modes.
**Suggested fix:** Add to step 3b: "If `states.json` is not found at the installed path, default all namespaces to `"plane"` and warn. The ticket lookup will still work (MCP-33 fallback namespace is `"plane"` for unmapped projects); namespace-scoped precision is degraded but not broken."

### F-4: wiki-state-update replacement text claims `updated_at` provides date checked, but this field is not in MCP-33's metadata schema
**Severity:** P2
**Where:** spec.md:280
**Edge case:** Field reference that may not exist in the `memory_search` result
**What happens:** Line 280 says "The record's `metadata.state_group` and `metadata.state` provide the current status; `updated_at` provides the date checked." MCP-33 spec section 4 defines metadata as `{identifier, state, state_group, priority, assignees}` -- no `updated_at` field. The `updated_at` might exist as an MCP memory record-level timestamp (when the record was last upserted), but the spec doesn't clarify this distinction. If the implementer looks for `updated_at` in the record metadata, it won't be there.
**Why the spec misses it:** Conflates Plane's `updated_at` (on the original issue payload) with the MCP memory record's internal timestamps. The MCP memory store likely has record-level `observed_at` or `updated_at` fields, but those aren't documented in the metadata schema that MCP-33 defines.
**Suggested fix:** Clarify: "The MCP memory record's `observed_at` timestamp (set when the record was ingested or updated by the webhook handler) provides the date checked. Do not confuse this with Plane's `updated_at` field, which is not surfaced in metadata."

### F-5: Decision page `## What's preserved` is a non-standard section heading
**Severity:** P3
**Where:** spec.md:389
**Edge case:** Decision page template drift from established convention
**What happens:** None of the 38 existing decision pages in the wiki use a `## What's preserved` heading. This section's content (preflight checks, outbound writes, wiki-state-update fallback) naturally belongs under `## Consequences` -- specifically under a subheading like `### Unchanged` or folded into the existing `### Costs` or `### If reversed` content. The page works as-is; this is a mild convention divergence.
**Why the spec misses it:** New section added in v2 to address round-1 findings about the preflight preservation claim, but placed under a novel heading rather than under the established `## Consequences` umbrella.
**Suggested fix:** Fold the content from `## What's preserved` into `## Consequences` as a `### Unchanged` sub-section, matching the Enables/Costs/If reversed pattern.

### F-6: Spec-cycle Phase 1 `memory_search` needs namespace but Phase 1 runs before reviewer dispatch
**Severity:** P3
**Where:** spec.md:179
**Edge case:** Spec-cycle Phase 1 `memory_search` call needs the namespace resolved in step 3b, but the spec only describes namespace passing to reviewer agents (Phase 2b), not how Phase 1 itself uses it
**What happens:** The spec says Phase 1 changes from `retrieve_work_item_by_identifier` to `memory_search` with "the pattern from section 2 above" -- which requires a `namespace` parameter. Step 3b resolves the namespace. Phase 1 runs after step 3b, so the namespace is available. The information is all there, but the Phase 1 instruction doesn't explicitly say "use the namespace resolved in step 3b." A careful implementer would figure this out; a less careful one might pass the default namespace.
**Why the spec misses it:** Step 3b mentions passing `namespace` to "each reviewer agent in step 2b" but doesn't mention Phase 1's own `memory_search` call.
**Suggested fix:** Change the Phase 1 instruction to: "...calling `memory_search` with the pattern from section 2 above, using the namespace resolved at step 3b."

## Summary
P0: 1 | P1: 1 | P2: 2 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=1 P2=2 P3=2 P4=0
