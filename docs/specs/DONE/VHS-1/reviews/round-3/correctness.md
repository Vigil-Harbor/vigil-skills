# Correctness Review -- round 3

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Ship-spec preflight `list_projects` replaced despite brief preserving it | CLOSED | spec v2 line 23/247, confirmed in v3 lines 23/249: preflight preserved |
| correctness | F-2 | Decision page contradicts section 3e on ship-spec preflight | CLOSED | spec v2/v3 section 3e (line 249) and decision page (line 385) consistent |
| correctness | F-3 | Two brief acceptance criteria missing from Done-when | CLOSED | spec v2/v3 done-when items 9-10 (lines 444-445) |
| correctness | F-4 | sync.py direction mismatch (install vs push) | CLOSED | spec v2/v3 line 440: "clean diff after python sync.py push" |
| correctness | F-5 | wiki-state-update replacement drops `<PROJ>-?` placeholder | CLOSED | spec v2/v3 line 282: placeholder guidance preserved |
| correctness | F-6 | Phase 6 fallback loses state.group filtering | CLOSED | spec v2/v3 D2: `review_state_id` eliminates need |
| correctness | F-7 | Primary preference regex drops state.group constraint | CLOSED | spec v2/v3 D2: `review_state_id` sidesteps regex |

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Test plan grep count says "exactly two" instead of "exactly one" | CLOSED | spec v3 line 410: now says "exactly one match" |
| correctness | F-2 | Decision page `## What's preserved` non-standard | CLOSED | spec v3 lines 384-388: folded into `## Consequences` as `**Unchanged:**` bold-text block |
| edge-cases | F-1 | Test plan grep count for `list_projects` wrong | CLOSED | Same as correctness R2/F-1 |
| edge-cases | F-2 | Decision page relative links 3 levels instead of 2 | CLOSED | spec v3 lines 391-392: cross-repo references now plain-text |
| edge-cases | F-3 | spec-cycle states.json missing-file not handled | CLOSED | spec v3 line 179: "If the file is not found, default all namespaces to 'plane' and warn" |
| edge-cases | F-4 | wiki-state-update `updated_at` vs `observed_at` | CLOSED | spec v3 line 282: now correctly uses `observed_at` |
| edge-cases | F-5 | Decision page `## What's preserved` non-standard | CLOSED | Same as correctness R2/F-2 |
| edge-cases | F-6 | Phase 1 namespace reference not explicit | CLOSED | spec v3 line 181: "using the namespace resolved at step 3b" |
| conventions | F-1 | Decision page uses `###` sub-headings | CLOSED | spec v3 lines 368-383: now uses `**Enables:**` bold-text pattern |
| conventions | F-2 | Decision page `## What's preserved` section non-standard | CLOSED | Same as correctness R2/F-2 |
| conventions | F-3 | Cross-repo relative paths in decision page | CLOSED | Same as edge-cases R2/F-2 |
| conventions | F-4 | Decision page frontmatter `> Related:` field non-standard | CLOSED | spec v3 lines 330-332: field removed |
| conventions | F-5 | `namespace` parameter list placement | CLOSED | spec v3 line 184 + sections 3b-3d: all three agents reference "namespace from prompt context"; line 181 now explicit for Phase 1 |
| conventions | F-6 | Brief departure for wiki-state-update not acknowledged | CLOSED | spec v3 lines 77-79: D7 now explicitly says "Brief departure" with rationale |
| conventions | F-7 | Test plan `list_projects` count | CLOSED | Same as correctness R2/F-1 |

## Findings

### F-1: Test plan wiki grep claims "one match" but grep would return two
**Severity:** P3
**Where:** spec.md:411
**Claim:** "`grep -r 'mcp__plane__retrieve_work_item' ../vigil-harbor-wiki/.claude/` -> one match: the cold-cache fallback in wiki-state-update (explicitly documented)"
**Why this is wrong:** The grep command would return two matches post-implementation, not one. The cold-cache fallback in `wiki-state-update/SKILL.md` is one match. The second match is in `vigil-harbor-wiki/.claude/settings.local.json:21` which contains `mcp__plane__retrieve_work_item_by_identifier` as a permissions allowlist entry. The `settings.local.json` entry is not a runtime call site (it is a Claude Code tool permission), so it does not violate done-when criterion #3 (which qualifies "in runtime sections"). However, the test plan describes what the grep command literally returns, and it would return 2 lines, not 1.
**Suggested fix:** Change to: "`grep -r 'mcp__plane__retrieve_work_item' ../vigil-harbor-wiki/.claude/` -> two matches: the cold-cache fallback in wiki-state-update (explicitly documented) and a permissions allowlist entry in `settings.local.json` (not a runtime call site)."

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
