# Grill 1 — VHS-41 round 4 — 2026-09-08T09:07:50Z — findings: correctness/F-1, edge-cases/F-1, edge-cases/F-2, edge-cases/F-3, edge-cases/F-4

## Grill summary — VHS-41 round-4 remaining P1 findings (rounds: 1/3, exit: empty-frontier; reason: tree fully visited)

### Settled
1. **6f guard key identifies the harvest** (Q1) — chose A: marker becomes `<!-- review-pr:body-dispositions:r<R>:h<hex> -->`, `<hex>` a short digest over the round's sorted harvest review-id set plus the Decision 9 keys it dispositioned; guard stays a last-line exact match; resume `capture` on the `r<R>` prefix is unchanged; Decision 12 states `r0` alone is not a harvest identity. Facts relied on: F1. ref: correctness/F-1, edge-cases/F-3
2. **Fetch blocks use a stdout token protocol** (Q2) — chose A: one Bash call prints exactly one of `HARVEST_FAILURE rc=<n>` or `COUNT=<n>`; a block that prints neither is a harvest failure; applied at Decision 7, D1 fetch (c), D5 inline poll. Facts relied on: F2. ref: edge-cases/F-1
3. **`SELF` is substituted literally** (Q3) — chose A: resolve the login once as conversational state and write `select(.user.login == "<SELF>")` per the `:180` pattern; `export SELF` / `env.SELF` removed from D2 step 1 and D7. Facts relied on: F3. ref: edge-cases/F-2
4. **D6 advance rule is the contiguous prefix** (Q4) — chose A: `LAST_BODY_REVIEW_ID` = highest successfully parsed id strictly below the round's lowest failed or deferred id; unchanged if nothing parsed or the lowest id failed; re-returned parsed reviews are absorbed by D5's cached parse and dedup. Facts relied on: F4. ref: edge-cases/F-4
5. **6e names this round's comment or states why not** (Q5) — chose the plain answer: `dispositions posted in <comment-url>` names the comment this round posted, else `dispositions not posted — <guard-skipped | post failed <code>>`. Facts relied on: none. ref: edge-cases/F-3

### Open frontier
(none)

### Facts established
- F1 — gojq's `capture("review-pr:body-dispositions:r(?<r>[0-9]+)")` matches the `r<R>` prefix regardless of a trailing suffix (source: docs/specs/TODO/VHS-41.reviews/round-4/correctness.md:52)
- F2 — `false > /dev/null; rc=$?` reports list status 0 with `rc=1`; a redirected fetch followed only by assignments prints nothing to the tool result (source: docs/specs/TODO/VHS-41.reviews/round-4/edge-cases.md:48)
- F3 — individual Bash tool calls do not share shell variables; `PUSH_TIME` / `PREV_REVIEW_ID` are carried as conversational state and substituted literally (source: skills/review-pr/SKILL.md:180)
- F4 — D5 runs the 2b parse once per review (cached) and counts items after Decision 9 dedup, so a re-returned parsed review contributes zero new items (source: docs/specs/TODO/VHS-41.spec.md:885-888)
