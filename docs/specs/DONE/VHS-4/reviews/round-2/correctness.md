# Correctness Review -- round 2

## Closure table (round 1 findings)

| Finding | Status | Evidence |
|---------|--------|----------|
| R1/F-1: "Three independent gates" but lists four | CLOSED | spec:65 now says "Four stages" |
| R1/F-2: Reviews-API fallback jq returns length, not id | CLOSED | spec:169-170 adds follow-up `.id` query |
| R1/F-3: REVIEW_SIGNAL=fast-path-skipped never assigned | CLOSED | spec:128 sets it; renamed to `fast-path` per conventions F-4 |
| R1/F-4: Replacement range narrower than actual | CLOSED | spec:121 now says "Replace the entire 6a section (lines 146-173)" |
| R1/F-5: D7 report string disagrees with 6e template | CLOSED | spec:87 now says `ci-check (FAILURE)` matching 6e |
| R1/F-6: Ticket VHS-4 not found in MCP memory cache | CLOSED | acknowledged; brief is local source of truth |

## Findings

### F-1: FAILURE path sets `REVIEW_SIGNAL=ci-check` but D7 and all other sections say `ci-check (FAILURE)`
**Severity:** P0
**Where:** spec.md:160
**Claim:** Line 160 reads `set REVIEW_SIGNAL=ci-check` on the FAILURE branch, but D7 (line 87), the 6e template (line 197), and the edge-cases entry (line 210) all use `ci-check (FAILURE)`. The FAILURE branch must set `REVIEW_SIGNAL=ci-check (FAILURE)` to match.
**Suggested fix:** Change line 160 from `REVIEW_SIGNAL=ci-check` to `REVIEW_SIGNAL=ci-check (FAILURE)`.

### F-2: Edge cases heading says "Three new entries" but there are seven
**Severity:** P2
**Where:** spec.md:202
**Claim:** The design section heading reads "Three new entries" but the bulleted list contains seven entries (fast path triggered, fast path + new findings, check missing/fallback, check FAILURE, push-to-check race, fallback regression, stale CI check round 2+).
**Suggested fix:** Change "Three new entries" to "Seven new entries".

### F-3: Test 1 grep expectation includes "Step 6e" but FAST_PATH does not appear in 6e
**Severity:** P2
**Where:** spec.md:224
**Claim:** Test 1 says `grep -n "FAST_PATH"` should match "Step 6 preamble (predicate definition), Step 6a (evaluation), Step 6b (skip note), Step 6e (report field)." But the Step 6e report template (lines 196-198) uses the prose "Fast path: yes/no", not the variable name `FAST_PATH`. The grep would not match in 6e.
**Suggested fix:** Change expected matches to "Step 6 preamble, Step 6a, Step 6b" — three matches, not four.

### F-4: Done-when 9 and Test 3 omit the CI-check SUCCESS review-ID fetch
**Severity:** P2
**Where:** spec.md:232-236 and spec.md:284
**Claim:** After CI-check `SUCCESS`, line 155-157 fetches the latest review `.id` via `pulls/<N>/reviews`. This is a reviews-API call, but Done-when 9 and Test 3 enumerate only "Step 2 (finding fetch), Step 6a pre-push short-circuit, Step 6a fallback branch, Step 6d Phase 2 verdict polling." The CI-check SUCCESS branch's review-ID fetch is missing from both lists.
**Suggested fix:** Add "Step 6a CI-check SUCCESS branch (review-ID fetch)" to Done-when 9's enumeration and Test 3's expected output.

STATUS: RED P0=1 P1=0 P2=3 P3=0 P4=0
