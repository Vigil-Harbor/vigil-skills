# Conventions Review -- round 2

## Findings

### F-1: Decision page uses `### Enables` / `### Costs` / `### If reversed` sub-headings instead of established bold-text pattern
**Severity:** P2
**Where:** spec.md:367-387 (decision page template, `## Consequences` section)
**Convention violated:** Wiki `decisions/` formatting convention -- established by 10+ existing decision pages
**Evidence:** The overwhelming majority of existing decision pages (state-edits-require-evidence, tool-namespacing-double-underscore, wiki-maintenance-redesign, drawbridge-out-of-band-audit, blog-content-boundary, etc.) use `**Enables:**`, `**Costs:**`, `**If reversed:**` as bold-text blocks within `## Consequences`. Only one page (`2026-05-04-dpo-v6-cross-scale-validation-prereg.md`) uses `###` sub-headings. The spec's decision page template uses `### Enables`, `### Costs`, `### If reversed` -- the minority pattern.
**Suggested fix:** In the decision page template (spec lines 367-387), replace `### Enables`, `### Costs`, `### If reversed` with `**Enables:**`, `**Costs:**`, `**If reversed:**` bold-text blocks inside `## Consequences`, matching the dominant pattern.

### F-2: Decision page `## What's preserved` section is non-standard
**Severity:** P2
**Where:** spec.md:389-394 (decision page template)
**Convention violated:** Wiki `decisions/` section structure -- no existing decision page uses `## What's preserved`
**Evidence:** Grepping all 35+ decision pages in `vigil-harbor-wiki/decisions/` for `## What's preserved` yields zero matches. The standard sections are: Context, Options Considered, Decision, Consequences (with Enables/Costs/If reversed), and Related. Some pages add `## Migration`, `## Confirmed by Code`, or domain-specific sections, but `## What's preserved` is not an established pattern. Its content (preflight checks, outbound writes, wiki-state-update fallback) is either already stated in `## Decision` or belongs in `## Consequences` under `**Enables:**` or as a note in `## Decision`.
**Suggested fix:** Fold the content of `## What's preserved` into `## Decision` (as a "What remains unchanged" paragraph) or into `## Consequences` under `**Enables:**`. Remove the standalone section.

### F-3: Decision page `## Related` section uses cross-repo relative paths that break out of the wiki repository
**Severity:** P2
**Where:** spec.md:396-399 (decision page template, `## Related` section)
**Convention violated:** Wiki `decisions/` link convention -- all existing `## Related` links use paths relative within the wiki repo (`../comprehension/...`, `../projects/...`, same-directory refs)
**Evidence:** Grepping all `## Related` sections in existing decision pages shows links like `../comprehension/2026-04-29-dyn-17-revert-incident.md`, `../projects/mcp-server/architecture.md`, `2026-05-01-wiki-maintenance-redesign.md`. None use `../../../` paths crossing repo boundaries. The spec's proposed `## Related` section contains `../../../MCP Server/docs/specs/TODO/MCP-33.spec.md` and `../../../vigil-skills/docs/specs/TODO/VHS-1.brief.md` which break out of the wiki into sibling repos. These links are invalid as relative markdown links and don't follow the established pattern.
**Suggested fix:** Replace cross-repo relative paths with plain-text references (e.g., `MCP-33 spec (vigil-harbor/MCP Server repo)`) or Plane ticket links, consistent with how other decision pages handle cross-repo references.

### F-4: Decision page frontmatter uses `> Related:` field not established in existing pages
**Severity:** P4
**Where:** spec.md:330 (decision page template frontmatter)
**Convention violated:** Wiki `decisions/` frontmatter field convention
**Evidence:** Existing decision pages use `> Related comprehension:` and `> Related decision:` for frontmatter cross-references (see `2026-04-29-state-edits-require-evidence.md` lines 6-7, `2026-05-01-wiki-maintenance-redesign.md` line 7). Most pages have no `> Related` frontmatter at all -- they use the `## Related` section at the end. The spec's `> Related: MCP-33 (Plane webhook receiver), VHS-1 (this ticket)` field is a new pattern.
**Suggested fix:** Either remove `> Related:` from frontmatter (the `## Related` section already covers this) or split into `> Related ticket:` for specificity. Either way, this is cosmetic.

### F-5: Spec-cycle section 3a adds `states.json` read but does not add `namespace` to the existing reviewer prompt parameter list
**Severity:** P3
**Where:** spec.md:176-182 (section 3a)
**Convention violated:** Completeness of prompt-parameter documentation -- the spec-cycle SKILL.md lines 71-81 enumerate all parameters for each reviewer's prompt; the spec adds `namespace` but only mentions it in passing
**Evidence:** Current spec-cycle SKILL.md (lines 71-81) lists exactly which parameters go to each agent's prompt: `spec_path`, `brief_path`, `project_root`, `ticket_id`, `round_number`, `wiki_root` (conventions only), `project_slug` (conventions only). The spec proposes adding `namespace` but says only "Each agent's prompt gains a new field: `namespace: <resolved namespace>`" at line 182 without specifying where in the Phase 2b parameter list it should be inserted or whether it goes to all three agents (it should, per sections 3b-3d which all reference "namespace from prompt context").
**Suggested fix:** Explicitly state that `namespace` is added to the Phase 2b parameter list for all three reviewers (alongside `spec_path`, `brief_path`, etc.), not just conventions.

### F-6: Brief acceptance criterion for wiki-state-update says "without calling Plane MCP" but spec preserves `retrieve_work_item` fallback
**Severity:** P3
**Where:** spec.md:450 (done-when item 10) vs brief.md:76
**Convention violated:** Brief is upstream source of truth; deviations should be acknowledged in a Decision entry
**Evidence:** Brief line 76: "wiki-state-update produces a valid evidence triple ... on a recent shipped MCP commit without calling Plane MCP -- verified by running it with the Plane MCP server stopped." Spec done-when item 10: "Verified by confirming `memory_search` is called first; `retrieve_work_item` fallback fires only on cache miss." The spec's verification method is softer -- it no longer requires the evidence triple to be producible with Plane stopped, because the spec explicitly preserves the `retrieve_work_item` fallback. This is a justified deviation (D7 + the evidence-triple decision), but the spec doesn't have a Decision entry that explicitly acknowledges it as a departure from the brief's acceptance criterion. D7 discusses the fallback behavior but doesn't say "this modifies brief acceptance criterion #6."
**Suggested fix:** Add a sentence to D7 (or a new D9) noting that this intentionally relaxes the brief's "without calling Plane MCP" criterion, since the evidence triple's correctness-critical nature makes a warm-cache-only guarantee insufficient.

### F-7: Test plan grep for `list_projects` in ship-spec expects "exactly two matches" but Phase 6 replacement removes one, leaving ambiguity
**Severity:** P3
**Where:** spec.md:415 (test plan item 1, third bullet)
**Convention violated:** Internal consistency of test plan with proposed changes
**Evidence:** Spec line 415: `grep -r 'list_projects' skills/ship-spec/SKILL.md` expects "exactly two matches: preflight reachability check (line 39, preserved) and zero in Phase 6." The current file has `list_projects` at lines 39 (preflight) and 216 (Phase 6 step 1). After the spec's changes, line 216 is replaced, so the grep should find exactly **one** match (the preflight at line 39), not "exactly two." The phrasing "exactly two matches ... and zero in Phase 6" is confusing -- "zero in Phase 6" is a qualifier, not a separate count. But the literal grep command returns 1 match, not 2.
**Suggested fix:** Rewrite to: `grep -r 'list_projects' skills/ship-spec/SKILL.md` returns exactly one match: the preflight reachability check (line 39). Phase 6 no longer references `list_projects`.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 3 | P4: 1

STATUS: GREEN
