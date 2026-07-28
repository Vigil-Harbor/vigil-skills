# Edge-Cases Review -- round 1

## Findings

### F-1: Decision page contradicts section 3e on ship-spec preflight `list_projects` preservation
**Severity:** P0
**Where:** spec.md:357 vs spec.md:231-237
**Edge case:** Internal inconsistency in the spec
**What happens:** The decision page says both spec-cycle and ship-spec preflight list_projects are preserved. Section 3e removes ship-spec's preflight list_projects. An implementer following section 3e would remove the reachability check, contradicting the decision page.
**Suggested fix:** Resolve the contradiction per correctness F-2.

### F-2: Review-state regex `/review|qa|in.review/i` matches "Spec Review" as well as "In Review"/"PR Review" -- ambiguous tie-breaking
**Severity:** P1
**Where:** spec.md:254-255
**What happens:** states.json for every project contains both "Spec Review" (started) and "In Review"/"PR Review" (completed). Both match the regex. No tie-breaking specified. Implementer could pick wrong state.
**Suggested fix:** Add explicit `review_state_id` field per project in states.json, or tighten regex to exclude "Spec Review."

### F-3: wiki-state-update cold-cache fallback to `retrieve_work_item` contradicts Done-when criterion #3
**Severity:** P1
**Where:** spec.md:270 and spec.md:280 vs spec.md:403
**What happens:** Done-when #3 says zero retrieve_work_item hits. Test plan step 3 says "without calling retrieve_work_item." But the design explicitly retains retrieve_work_item as fallback. These contradict.
**Suggested fix:** Align test plan to say "tries memory_search first; falls back to retrieve_work_item on cache miss." Document double-failure behavior (both miss → refuse edit).

### F-4: VHS not in MCP server `config/webhooks.json` -- namespace `"vhs"` will never receive records
**Severity:** P1
**Where:** spec.md:134 and spec.md:114-128
**What happens:** VHS is not in config/webhooks.json. Events fall back to namespace "plane" but skills search "vhs". Silent degradation.
**Suggested fix:** Add webhooks.json VHS update as explicit prerequisite in Blocked-by line.

### F-5: `states.json` has no `state_group` metadata
**Severity:** P2
**Where:** spec.md:82-129 and spec.md:254-257
**What happens:** Current code uses state.group for disambiguation. states.json only stores name→UUID. Loses fidelity.
**Suggested fix:** Add group to states.json entries or document as deliberate simplification.

### F-6: spec-cycle reads `states.json` from `project_root` but always runs from target project
**Severity:** P2
**Where:** spec.md:161
**What happens:** Dual-path instruction adds complexity without clear detection logic. Installed path is always correct.
**Suggested fix:** Simplify to: "Read `~/.claude/skills/ship-spec/states.json`."

### F-7: `memory_search` staleness window not documented
**Severity:** P3
**Where:** spec.md:136-153
**Suggested fix:** Add one-line note: typical staleness under 5s, worst case 6h.

### F-8: `memory_search` returns `"Error: ..."` text on failure but spec only handles zero-result case
**Severity:** P2
**Where:** spec.md:141-151
**What happens:** MCP tools return error text, never throw. Spec doesn't distinguish zero results from error responses.
**Suggested fix:** Add: "If response starts with 'Error:', treat as MCP memory outage — warn and proceed using brief."

### F-9: Test plan contradicts design for wiki-state-update fallback
**Severity:** P2
**Where:** spec.md:387
**What happens:** Same root as F-3. Test plan says "without calling retrieve_work_item" but design retains fallback.
**Suggested fix:** Rewrite test plan step per F-3 fix.

### F-10: No JSON validity check for `states.json`
**Severity:** P3
**Where:** spec.md:392-396
**Suggested fix:** Add `python -c "import json; json.load(open('skills/ship-spec/states.json'))"` to test command.

## Summary
P0: 1 | P1: 3 | P2: 4 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=3 P2=4 P3=2 P4=0
