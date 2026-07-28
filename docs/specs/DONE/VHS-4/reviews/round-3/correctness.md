# Correctness Review -- round 3

## Closure table (round 2 findings)

| Finding | Status | Evidence |
|---------|--------|----------|
| R2/F-1: FAILURE path sets REVIEW_SIGNAL=ci-check not ci-check (FAILURE) | CLOSED | spec:160 now reads `set REVIEW_SIGNAL=ci-check (FAILURE)` |
| R2/F-2: Edge cases heading says "Three new entries" but seven | CLOSED | spec:202 now says "Eight new entries"; actual count is 8 |
| R2/F-3: Test 1 grep expectation includes Step 6e | CLOSED | spec:225 now lists only "Step 6 preamble, Step 6a, Step 6b" |
| R2/F-4: Done-when 9 and Test 3 omit CI-check SUCCESS review-ID fetch | CLOSED | spec:285 and spec:237 both include "Step 6a CI-check SUCCESS branch (review-ID fetch)" |

## Findings

### F-1: Scope table omits Step 6b edit
**Severity:** P4
**Where:** spec.md:11
**Suggested fix:** Add "Step 6b (one-line skip note)" to the scope table's SKILL.md row.

### F-2: `gh pr checks --json state` value set not pinned against `gh` CLI version
**Severity:** P3
**Where:** spec.md:146, spec.md:57
**Suggested fix:** Add a note to D4 about gh CLI version and conservative fallback behavior.

### F-3: VHS-4 Plane ticket not found in MCP memory cache
**Severity:** P3
**Suggested fix:** Cache the VHS-4 ticket via MCP webhook receiver or manual ingest.

STATUS: GREEN
