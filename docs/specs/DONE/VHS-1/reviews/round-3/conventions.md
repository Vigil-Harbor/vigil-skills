# Conventions Review -- round 3

## Closure table (round 2 findings)

| ID | Round 2 title | Sev | Status | Evidence |
|---|---|---|---|---|
| F-1 | Decision page ### sub-headings → **bold-text:** in Consequences | P2 | CLOSED | Spec lines 368-388: `**Enables:**`, `**Costs:**`, `**If reversed:**`, `**Unchanged:**` all use bold-text labels, matching the established pattern. |
| F-2 | "## What's preserved" folded into Consequences | P2 | CLOSED | Spec line 385: `**Unchanged:**` block lives inside `## Consequences`, not as a separate section. |
| F-3 | Cross-repo relative paths in ## Related | P2 | CLOSED | Spec lines 391-392 use plain-text references for cross-repo items; lines 393-394 use relative links for intra-`decisions/` items. |
| F-5 | namespace parameter to all three reviewers AND Phase 1 | P3 | CLOSED | Spec line 55 (D2), line 181 (Phase 1), line 183 (Phase 2b), lines 204/224/244 (each agent). |
| F-6 | Brief acceptance criterion deviation acknowledged | P3 | CLOSED | Spec line 79: "**Brief departure:**" paragraph. Done-when #10 reflects relaxed verification. |
| F-7 | Test plan grep count fixed to "exactly one" | P4 | CLOSED | Spec line 410: exactly one match. |

All round-2 findings are closed.

## Findings

### F-1: Decision page `## Related` intra-directory links use abbreviated link text instead of full filename
**Severity:** P4
**Where:** spec.md:393-394
**Convention violated:** Existing decisions use the full filename as link text
**Evidence:** Existing pages use `[2026-04-29-state-edits-require-evidence.md](2026-04-29-state-edits-require-evidence.md)`. The spec uses `[State edits require evidence](2026-04-29-state-edits-require-evidence.md)`.
**Suggested fix:** Use full filename as link text for consistency.

### F-2: Decision page Option 3 ("Chosen") is a bare pointer with no summary
**Severity:** P3
**Where:** spec.md:354-355
**Convention violated:** Established decision pages provide multi-sentence rationale for each option including the chosen one
**Evidence:** Other decision pages provide substantive summaries in the chosen option before pointing to ## Decision.
**Suggested fix:** Add 1-2 sentence summary in Option 3 before the "See ## Decision below" pointer.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 1

STATUS: GREEN
