# Correctness Review -- round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Ship-spec preflight `list_projects` replaced despite brief preserving it | CLOSED | Spec v2 line 23: "Preflight `list_projects` reachability check (line 39) is preserved." Line 247: "The existing `mcp__plane__list_projects` reachability check is **preserved**." |
| correctness | F-2 | Decision page contradicts section 3e on ship-spec preflight | CLOSED | Spec v2 section 3e (line 247) now preserves preflight, consistent with decision page (line 390) |
| correctness | F-3 | Two brief acceptance criteria missing from Done-when | CLOSED | Spec v2 lines 449-450: Done-when items 9 and 10 added, with post-MCP-33 production caveat |
| correctness | F-4 | sync.py direction mismatch | CLOSED | Spec v2 line 445: "python sync.py status shows clean diff after python sync.py push" |
| correctness | F-5 | `<PROJ>-?` placeholder dropped | CLOSED | Spec v2 line 280: placeholder guidance preserved in replacement text |
| correctness | F-6 | Phase 6 fallback loses state.group | CLOSED | Spec v2 D2 (lines 49-53): `review_state_id` eliminates regex disambiguation entirely |
| correctness | F-7 | Primary preference regex drops state.group | CLOSED | Same as F-6; `review_state_id` sidesteps the problem |
| edge-cases | F-1 | Decision page contradicts section 3e | CLOSED | Same as correctness F-2 |
| edge-cases | F-2 | Review-state regex ambiguity | CLOSED | Spec v2 D2 adds `review_state_id` per project |
| edge-cases | F-3 | wiki-state-update fallback contradicts Done-when #3 | CLOSED | Spec v2 Done-when 3 (line 443) explicitly excepts the cold-cache fallback |
| edge-cases | F-4 | VHS not in webhooks.json | CLOSED | Spec v2 Blocked-by line 7 adds VHS to prerequisites |
| edge-cases | F-5 | states.json has no state_group | CLOSED | `review_state_id` makes state_group unnecessary for the disambiguation use case |
| edge-cases | F-6 | spec-cycle reads states.json path ambiguity | CLOSED | Spec v2 line 177: simplified to `~/.claude/skills/ship-spec/states.json` |
| edge-cases | F-7 | memory_search staleness not documented | CLOSED | Spec v2 line 169: "Typical staleness: Under 5 seconds... Worst case: up to 6 hours" |
| edge-cases | F-8 | memory_search error response not handled | CLOSED | Spec v2 line 165: error handling for "Error:" response prefix documented |
| edge-cases | F-9 | Test plan contradicts design for wiki-state-update fallback | CLOSED | Spec v2 test plan step 3 (line 426): aligned with fallback design |
| edge-cases | F-10 | No JSON validity check for states.json | CLOSED | Spec v2 line 434: `python -c "import json; json.load(open(...))"` added to test command |
| conventions | F-1 | Internal contradiction ship-spec preflight | CLOSED | Same as correctness F-2 |
| conventions | F-2 | Brief deviation without acknowledgment | CLOSED | Preflight restored, no deviation remains |
| conventions | F-3 | Decision page template drift | CLOSED | Spec v2 decision page (line 356 onward) uses `## Decision`, `## Consequences`, `## Related` |
| conventions | F-4 | Decision page missing `## Related` | CLOSED | Spec v2 line 395: `## Related` section present |
| conventions | F-5 | CLAUDE.md file layout doesn't account for states.json | CLOSED | Spec v2 section 3g (lines 303-306) adds states.json to file layout |
| conventions | F-6 | Phase 6 fallback loses state.group | CLOSED | Same as correctness F-6/F-7 |
| conventions | F-7 | Spec-cycle states.json read path ambiguity | CLOSED | Same as edge-cases F-6 |

## Findings

### F-1: Test plan grep count for `list_projects` in ship-spec/SKILL.md is wrong
**Severity:** P2
**Where:** spec.md:415
**Claim:** "`grep -r 'list_projects' skills/ship-spec/SKILL.md` -> exactly two matches: preflight reachability check (line 39, preserved) and zero in Phase 6"
**Why this is wrong:** After the spec's changes, Phase 6 step 1 (currently line 216: `mcp__plane__list_projects`) is replaced with `Read states.json (already loaded at preflight)` (spec line 266). The replacement text contains no mention of `list_projects`. The only remaining match would be the preflight at line 39. So post-change, grep returns exactly ONE match, not two. The phrasing "exactly two matches" contradicts the described outcome ("zero in Phase 6"). A test plan that asserts two matches would fail validation.
**Suggested fix:** Change to: `grep -r 'list_projects' skills/ship-spec/SKILL.md` -> exactly one match: preflight reachability check (line 39, preserved); zero in Phase 6.

### F-2: Decision page has non-standard `## What's preserved` section
**Severity:** P4
**Where:** spec.md:389
**Claim:** "Template follows the established pattern (date, project, status, context, options, decision, consequences, related)"
**Why this is wrong:** No existing decision page in `vigil-harbor-wiki/decisions/` uses a `## What's preserved` heading (verified via grep). This is a novel section. The content is useful but could be folded into `## Consequences` as a subsection (e.g., `### Preserved`) to match the established pattern more closely. The spec's own line 323 claims the template "follows the established pattern" but the extra section makes it slightly non-standard.
**Suggested fix:** Either fold the `## What's preserved` content into `## Consequences` as a `### Preserved` subsection, or acknowledge the addition is intentional. This is purely cosmetic -- the page works either way.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 0 | P4: 1

STATUS: GREEN
