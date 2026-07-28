# Correctness Review -- round 1

## Findings

### F-1: D5 says "Three independent gates" but lists four items
**Severity:** P2
**Where:** spec.md:65
**Claim:** "Three independent gates compose at the top of Step 6a:" followed by a numbered list of four items (1-4). Items 3 and 4 are not independent (4 is a fallback for 3).
**Suggested fix:** Change "Three independent gates" to "Four stages" or "Three gates (the third with a fallback)" and revise line 74.

### F-2: Reviews-API fallback jq query returns `length` (count) but spec says to "capture its `id`"
**Severity:** P1
**Where:** spec.md:152-155
**Claim:** The fallback reviews-API poll uses `| length`, then prose says "capture its `id` for Step 6b." The jq returns an integer, not an ID.
**Suggested fix:** Add a follow-up query after detection: `... | last | .id`.

### F-3: REVIEW_SIGNAL=fast-path-skipped never assigned in the code path
**Severity:** P2
**Where:** spec.md:118 vs spec.md:178,181
**Claim:** Every other branch explicitly sets REVIEW_SIGNAL. The fast-path branch does not.
**Suggested fix:** Add `Set REVIEW_SIGNAL=fast-path-skipped.` to line 118.

### F-4: Replacement range "lines 150-173" is narrower than the actual replacement
**Severity:** P2
**Where:** spec.md:111
**Suggested fix:** Change to "Replace the entire 6a section (lines 146-173)."

### F-5: D7 report string disagrees with 6e template
**Severity:** P2
**Where:** spec.md:87 vs spec.md:178
**Suggested fix:** Align D7 to match the 6e template: `ci-check (FAILURE)`.

### F-6: Ticket VHS-4 not found in MCP memory cache
**Severity:** P3

STATUS: RED P0=0 P1=1 P2=4 P3=1 P4=0
