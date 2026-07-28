# Conventions Review -- round 1

## Findings

### F-1: Internal contradiction -- ship-spec preflight `list_projects` removed in section 3e but claimed preserved in decision page
**Severity:** P0
**Where:** spec.md:231-238 vs spec.md:357
**Convention violated:** Spec internal consistency
**Evidence:** Section 3e removes ship-spec preflight list_projects. Decision page says it's preserved. Three sections disagree.
**Suggested fix:** Decide one way. Brief preserves it (line 32). Restore in section 3e or update decision page.

### F-2: Spec deviates from brief on ship-spec preflight preservation without acknowledgment
**Severity:** P1
**Where:** spec.md:231-238 vs brief.md:32
**Convention violated:** Brief is upstream source of truth; deviations should be explicit
**Evidence:** Brief line 32 preserves ship-spec preflight list_projects. Spec replaces it without a Decision entry.
**Suggested fix:** Restore or add Decision D9 with rationale.

### F-3: Decision page template drift -- missing `## Decision` and `## Consequences` sections
**Severity:** P2
**Where:** spec.md:304-361
**Convention violated:** Wiki decisions/ template format
**Evidence:** All existing decision pages have ## Decision and ## Consequences. Proposed page uses non-standard ## Blast radius and ## What's preserved.
**Suggested fix:** Rename to match template. Add ## Decision summary, ## Consequences with standard substructure.

### F-4: Decision page missing `## Related` section
**Severity:** P2
**Where:** spec.md:304-361
**Convention violated:** Wiki decisions/ template format
**Evidence:** Every existing decision page ends with ## Related.
**Suggested fix:** Add ## Related section with cross-references.

### F-5: `states.json` is first non-SKILL.md file in a skill directory -- CLAUDE.md file layout section does not account for it
**Severity:** P3
**Where:** spec.md:80-130 and CLAUDE.md:48-51
**Suggested fix:** Add note to CLAUDE.md file layout about states.json.

### F-6: Phase 6 fallback loses `state.group` filtering
**Severity:** P3
**Where:** spec.md:252-258
**Suggested fix:** Add state_group to states.json or acknowledge as simplification.

### F-7: Spec-cycle `states.json` read path ambiguity
**Severity:** P3
**Where:** spec.md:160-161
**Suggested fix:** Simplify to ~/.claude/skills/ship-spec/states.json.

## Summary
P0: 1 | P1: 1 | P2: 2 | P3: 3 | P4: 0

STATUS: RED P0=1 P1=1 P2=2 P3=3 P4=0
