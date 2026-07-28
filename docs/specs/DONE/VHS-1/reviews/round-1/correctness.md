# Correctness Review -- round 1

## Findings

### F-1: Ship-spec preflight `list_projects` replaced despite brief explicitly preserving it
**Severity:** P1
**Where:** spec.md:231-237 (section 3e)
**Claim:** "**Preflight (line 39):** Remove: `8. mcp__plane__list_projects -- confirm Plane MCP is reachable. Warn-and-proceed on failure.` Replace with: `8. Read skills/ship-spec/states.json...`"
**Why this is wrong:** The brief at line 32 explicitly lists `ship-spec/SKILL.md:39` -- preflight `list_projects` -- as "Preserved (NOT migrated)" with the rationale "same rationale [as spec-cycle]: it costs one call and provides a useful 'is Plane up' signal." The brief distinguishes between the preflight `list_projects` (line 39, preserved) and the Phase 6 `list_projects` (line 216, eliminated by states.json). By replacing the preflight check, ship-spec loses its Plane reachability signal before Phase 6 writes (`update_work_item`, `create_work_item_comment`), which will fail opaquely if Plane is down. The spec does not acknowledge this as a deliberate departure from the brief.
**Suggested fix:** Restore the preflight `list_projects` at step 8 (or add a separate reachability probe). Only replace the Phase 6 step 1 `list_projects` with states.json. If the spec author intentionally departs from the brief, add a Decision section with rationale.

### F-2: Decision page template contradicts section 3e on ship-spec preflight
**Severity:** P0
**Where:** spec.md:357
**Claim:** "Preflight `list_projects` reachability checks in spec-cycle and ship-spec."
**Why this is wrong:** The decision page template (section 4, line 357) says both spec-cycle AND ship-spec preflight `list_projects` reachability checks are preserved. But section 3e (lines 231-237) explicitly removes ship-spec's preflight `list_projects` at line 39 and replaces it with states.json reading. This is an internal contradiction within the spec -- the decision page says one thing, the per-file changes say another. The implementer cannot follow both.
**Suggested fix:** Resolve the contradiction. If the preflight `list_projects` in ship-spec IS removed (per section 3e), update the decision page template to say only spec-cycle's preflight is preserved. If F-1 is addressed by restoring it, update section 3e instead.

### F-3: Two brief acceptance criteria missing from spec's Done-when list
**Severity:** P0
**Where:** spec.md:399-408 (Done when)
**Claim:** The spec lists 8 Done-when items.
**Why this is wrong:** The brief's acceptance criteria (lines 71-78) and the Plane ticket both include two criteria absent from the spec's Done-when list:
  1. "spec-cycle and ship-spec runs against MCP-33 produce a spec diff against the pre-migration baseline that is either empty or limited to non-load-bearing prose. Cite the diff command + result in the PR body." (brief line 75)
  2. "wiki-state-update produces a valid evidence triple (Plane-ID, ship date, commit hash) on a recent shipped MCP commit without calling Plane MCP -- verified by running it with the Plane MCP server stopped." (brief line 76)

The spec's test plan section 3 describes these as post-merge manual smoke tests, and Out of scope item 8 explicitly defers their execution. But these are brief acceptance criteria, not optional validations. Dropping them from Done-when without acknowledging the departure is unmet criterion coverage.
**Suggested fix:** Add both as Done-when items (items 9 and 10), noting they are exercised post-MCP-33-production per the "Blocked by" prerequisite. Alternatively, add a Decision section explaining why the brief's acceptance criteria are deferred with explicit rationale.

### F-4: `sync.py` direction mismatch between spec and brief
**Severity:** P2
**Where:** spec.md:405
**Claim:** "`python sync.py status` shows clean diff after `python sync.py install`."
**Why this is wrong:** The brief at line 78 says "python sync.py status in vigil-skills shows clean diff after python sync.py **push**." The spec says `install` (repo -> ~/.claude/), while the brief says `push` (~/.claude/ -> repo). Both demonstrate sync parity, but the wording should match the brief.
**Suggested fix:** Change to `python sync.py status` shows clean diff after `python sync.py push` to match the brief.

### F-5: Replacement text for wiki-state-update drops `<PROJ>-?` placeholder guidance
**Severity:** P2
**Where:** spec.md:266-270
**Why this is wrong:** The actual file at `vigil-harbor-wiki/.claude/skills/wiki-state-update/SKILL.md:27` includes additional text: "If no Plane ticket exists for the work, use `<PROJ>-?` as a placeholder and explicitly note the absence in the entry body." The replacement text at line 270 drops this guidance.
**Suggested fix:** Append the `<PROJ>-?` placeholder guidance to the replacement text at line 270.

### F-6: Ship-spec Phase 6 fallback logic changes from group-based to name-based
**Severity:** P2
**Where:** spec.md:254-257
**Why this is wrong:** Current fallback is "any state with `state.group == 'started'`." Spec proposes "state named 'In Progress'." Since states.json lacks group info, group-based matching is lost.
**Suggested fix:** Add state_group to states.json entries or acknowledge as deliberate simplification.

### F-7: Primary preference regex drops `state.group` constraint
**Severity:** P3
**Where:** spec.md:255
**Why this is wrong:** Current code requires `state.group == "started"` AND name regex. New code drops group. "Spec Review" matches the regex too.
**Suggested fix:** Add state_group to states.json or tighten regex to exclude "Spec Review."

## Summary
P0: 2 | P1: 1 | P2: 3 | P3: 1 | P4: 0

STATUS: RED P0=2 P1=1 P2=3 P3=1 P4=0
