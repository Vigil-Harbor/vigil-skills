# Correctness Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `gh api --jq --arg` invalid | CLOSED | spec:603–620, :966–986, row 13 (:1263). Verified live against `gh 2.87.3`: `gh api … --jq '… select(.user.login == env.SELF) …'` resolves `env.SELF`; `capture("…r(?<r>[0-9]+)")` (RE2 named group) works and emits an empty stream on non-match with rc 0 |
| correctness | F-2 | rows 4/8 pin impossible counts | CLOSED | row 4 now `≥10` with the full 11-site enumeration (:1254); row 8 `≥3` with `:341` counted once (:1258). Pre values re-measured on `main`: row 4 = `0`, row 8 = `0` |
| correctness | F-3 | bounded round posts nothing → no progress | CLOSED | Decision 12 "Progress does not depend on findings" (:388–394); D7 post condition case 2 (:959–964); findings-free body (:1024–1033) |
| correctness | F-4 | verdict-landed read off the body-filtered stream | CLOSED | D5's third query (:876–883) + the verdict-landed rule (:891–902). Verified: PR #28 `5135992754` (`APPROVED`) has body length 0 |
| correctness | F-5 | D1 "before :79" contradicts its own order line | CLOSED | D1 :558–564 now reads (a)→(a2)→`:79`→(b)→2b→(c)→`:81`/`:83` |
| correctness | F-6 | phrase-tripwire input undefined | CLOSED | Decision 11 :307–325 + D2 step 6 :711–715 define the body-wide phrase-scan view |
| correctness | F-7 | steps 6/7 circular | CLOSED | D2 step 5 provisional span (:664–670), step 6 normalizes it, step 7 narrows it |
| correctness | F-8 | row 8 `-F` escaping, row 14 dead regex | **PARTIAL** | Row 8 fixed (fenced block, Pre `0` verified). Row 14's `.*` still cannot match the backslash-continued form the spec uses everywhere — see F-5 below. Keeps P2 |
| correctness | F-9 | undefined `R` leaves an unguarded comment | **CLOSED (new variant)** | `r0` sentinel (:988–993) closes the unguarded case but makes the guard key constant — new P1, F-1 below |
| edge-cases | F-1 | cross-round marker leapfrog | CLOSED | `HARVEST_FLOOR` is run-scoped (:344–381); D6 advance rule :921–930 |
| edge-cases | F-2 | `--arg` rejected by `gh` | CLOSED | same evidence as correctness F-1 |
| edge-cases | F-3 | steps 6/7 circular | CLOSED | D2 step 5 :664–670 |
| edge-cases | F-4 | phrase tripwire reads a view step 6 stopped producing | CLOSED | D2 step 6 :711–715 |
| edge-cases | F-5 | `LAST_BODY_REVIEW_ID` never advanced after Step 2 | CLOSED | Decision 2 :77–83; D1 :589–592; D5 counts post-dedup :885–888 |
| edge-cases | F-6 | step 9 structural matching on raw text | CLOSED | D2 step 6 "Masked for matching, raw for content" :698–709; step 9 :747–750 |
| edge-cases | F-7 | gate rows 4/8 miscounted | CLOSED | rows 4/8 rewritten; Pre values re-measured |
| edge-cases | F-8 | fetches (a)/(c) ungoverned; `:83` unblocked | CLOSED | Decision 14 bullets 1 (:471–482) and 6 (:499–509) name `:81`, `:83`, `:381`; D1 (c) captures `rc` (:555) |
| edge-cases | F-9 | empty `$SELF` | CLOSED | Decision 14 :483–488 |
| edge-cases | F-10 | marker laundering via harvested titles | CLOSED | Decision 12 position + neutralization :412–423; D7 :995–998 |
| edge-cases | F-11 | markerless 6f comment unguarded | **PARTIAL** | `r0` closes the unguarded half; the guard is now collision-prone — F-1 below. Keeps P2 |
| edge-cases | F-12 | body-size threshold unstated | CLOSED | D2 step 3 names 64 KB (:640–645) |
| conventions | F-1 | row 4 count `9` omits fetch (b) | CLOSED | row 4 :1254 enumerates fetch (b) |
| conventions | F-2 | row 8 count `4` lists `:341` twice | CLOSED | row 8 :1258 |
| conventions | F-3 | D1 "before `:79`" | CLOSED | D1 :558–564 |
| conventions | F-4 | test-plan absolute falsified by its own rows | CLOSED | preamble :1216–1219 distinguishes positive rows from `[guard]` rows |
| conventions | F-5 | bare-tool-name fence misses `:99` inside D3's region | **PARTIAL** | Design preamble (frozen this round) :522–525 still names only `:180`/`:200` (D5) and `:316`/`:345` (D8); `:99` ("using the Read tool") sits inside D3's `:85-115` region and is unmentioned. Keeps P3 |
| conventions | F-6 | VHS-42 `RELATED` contradicts the spec | CLOSED | § Deferred :1379–1382 instructs `/ship-spec` to trim it |

**Grounding notes.** All test-plan Pre values re-measured on unmodified `main` and every one matches: row 4 `0`, row 5 `7`, row 6 `3`, row 7 `0`, row 8 `0`, row 9 `1`/`2`, row 10 `0`, row 11 `1`, row 12 no match, row 13 `0`, row 14 `0`, row 15 `0`/`1`, row 16 `1 failed, 158 passed, 3 skipped`. `skills/review-pr/SKILL.md` is 406 lines as the header claims, and every file:line anchor the spec cites resolves to the symbol named. `AGENTS.md:7` carries "no test suite"; `:46` is the `### /review-pr` heading and `:48` the paragraph. Plane VHS-41 retrieved (`bd1504df-8bbb-4675-9f03-6dc5027b6637`) — description and Done-when agree with the brief. `git log -10` on the touched files: most recent is `d381f88` (2026-09-06, 2 days ago), which touched `AGENTS.md` but not `skills/review-pr/SKILL.md`.

## Findings

### F-1: The `r0` sentinel makes the 6f idempotency guard a constant key, so a later round's dispositions are silently suppressed
**Severity:** P1
**Where:** spec § Decision 12 (:356–361, :398–403), § D7 (:966–993)
**Claim:** Decision 12: *"If no id qualifies, `R` is `0` … `R` is **monotone across the rounds of a run**: a round whose computed `R` does not exceed the last `R` this run posted claims nothing new, and posts its comment with `r0`."* And the guard: *"skip the post only if one already carries the exact marker line this round would post — **including `r0`**."*
**Why this is wrong:** `r0` is not a harvest identity — Decision 12 itself says it "claims nothing". But the guard treats marker equality as harvest equality (*"A marker match means 'this exact harvest was already dispositioned', not 'this round already ran'"*, :402–403). For `r0` that reading is false, so `r0` behaves exactly like the constant `no-push` key the spec's own edge case forbids.

Reachable path, all inside one run: harvest set `[100, 200, 300]`; review 100's body fetch fails → `HARVEST_FLOOR = 100`; 200 and 300 parse with findings and are dispositioned. `HANDLED_THROUGH` requires *every* review in `(PRIOR_MARK, id]` handled, and 100 was not, so no id qualifies → `R = 0`. Round 1 posts its comment ending `<!-- review-pr:body-dispositions:r0 -->`. Round 2 triages review 400's body findings; the floor still stands, so `R` is still `0`; the guard at :978–981 finds the round-1 comment whose last non-blank line is that exact string and **skips the post**. Review 400's dispositions never reach the PR.

This contradicts two frozen statements:
- § Decision 3 (:107–108): *"Each round that triaged at least one body-level finding posts **exactly one** PR-level comment listing every body-level item…"*
- § D9 edge case (:1183–1184): *"**Two all-skip rounds on one PR** — each posts its own comment keyed `r<R>`. A constant `no-push` key would have suppressed the second round's dispositions."*

The cross-run variant is worse: if the fetch failure is persistent (a deleted or permission-gated review), a whole re-run computes `R = 0`, matches the prior run's `r0` comment, and posts nothing at all — the audit-trail hole the brief names, restored. Note the guard-skip also interacts badly with Decision 12's `HANDLED_THROUGH`, which requires items "dispositioned in a **posted** comment": a guard-skipped round did not post, so it can never advance the mark either.

**Suggested fix:** Make the guard key identify the harvest, not just `R`. Minimal change that preserves everything else: emit the marker as `<!-- review-pr:body-dispositions:r<R>:h<hex> -->` where `<hex>` is a short digest over the round's sorted harvest review-id set plus the Decision 9 keys it dispositioned. The resume query's `capture("review-pr:body-dispositions:r(?<r>[0-9]+)")` still matches the `r<R>` prefix unchanged (verified: gojq's `capture` matches the prefix regardless of the suffix), while the guard's `==` on the full marker line now distinguishes round 1's `r0:h…` from round 2's `r0:h…`. Alternatively, scope the guard: apply marker-equality only when `R > 0`; when `R == 0`, compare the full comment body instead. Either way, add a sentence to Decision 12 stating that `r0` is not a harvest identity and must not be used alone as a duplicate key.

### F-2: D2 step 2 sources the rounds-2+ harvest set from Step 2's fetch (b), a snapshot taken before any incremental review exists
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D2 step 2 (:622–624)
**Claim:** *"**Harvest set, oldest-first bound.** The set is every review from **Step 2 fetch (b)** with `id > PRIOR_DISPOSITIONED_REVIEW_ID` (rounds 2+: `id > LAST_BODY_REVIEW_ID`)…"*
**Why this is wrong:** The parenthetical establishes that step 2 runs in rounds 2+, but Step 2 fetch (b) is executed exactly once, inside Step 2 (§ D1 :546–547), before any push and therefore before any incremental review is submitted. Filtering that stale snapshot by `id > LAST_BODY_REVIEW_ID` in round 2 yields the empty set — which is precisely the PR #28 scenario the ticket exists to fix (*"the PR #28 finding lived in the **incremental** review"*, § Decision 2 :66–67). The correct source for rounds 2+ is D5's body-carrying poll query (:871–874, `select(.id > <LAST_BODY_REVIEW_ID>)`), which D6 confirms: *"Body findings for the round come from the 2b parse of every body-carrying review with `id > LAST_BODY_REVIEW_ID`, reusing 6a's cached parse"* (:919–920). Two adjacent sections name two different sources for the same set.
**Suggested fix:** Rewrite D2 step 2's first sentence to: "The set is every body-carrying review with `id > PRIOR_DISPOSITIONED_REVIEW_ID`, from Step 2 fetch (b) on the first invocation and from 6a's body-carrying poll (D5) on every later round, where the bound is `id > LAST_BODY_REVIEW_ID`."

### F-3: D6's advance rule states two clauses that only agree under an unstated "contiguous" reading, and D1's seeding restates only the looser one
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D6 (:921–925), § D1 (:589–592)
**Claim:** D6: *"set `LAST_BODY_REVIEW_ID` to the highest id **whose body was fetched and parsed successfully in this round** … It must **not** advance past a review whose fetch failed."*
**Why this is wrong:** When the failure is not the highest id, the two clauses give different answers. Harvest `[100, 200, 300]` with 200's fetch failing: "the highest id parsed successfully" is `300`, which does advance past the failed `200`, so the first clause produces exactly what the second forbids and the harm the second names ("that review is never retried by a later 6a poll of the same run") lands. The intended value is clearly the highest successfully-parsed id *below the lowest failure* — the same contiguity Decision 12 spells out for `HANDLED_THROUGH` (:350–354) — but D6 never says "contiguous", and D1's seeding (:589–592) restates only the unqualified clause while deferring to "the same rule D6 applies in 6b", so the ambiguity propagates to Step 2.
**Suggested fix:** In D6, replace the primary clause with: "set `LAST_BODY_REVIEW_ID` to the highest successfully-fetched-and-parsed id that is **below the lowest id whose fetch or parse failed in this round** (i.e. the highest contiguous handled id); leave it unchanged if nothing parsed." Mirror that wording in D1's seeding paragraph rather than referring out.

### F-4: Test row 19's factual claims about review `5135878266` are false, making the row unable to detect what it says it detects
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 19 (:1279–1285)
**Claim:** *"`…/reviews/5135878266 --jq '.body'` — **zero** items **and neither tripwire fires**. This body carries the top-level `🤖 Prompt for all review comments with AI agents` block listing two findings **under the words "Outside diff comments"**; a parse returning 2 has violated Decision 10, and a phrase tripwire firing here means the per-phrase / post-mask scoping of Decision 11 was not implemented."*
**Why this is wrong:** I fetched the body. It is 2468 chars, and `grep -i 'outside'` returns **zero** matches; `grep -i 'nitpick'` returns zero matches. Its prompt block is headed `Inline comments:` (body line 12) and lists two *inline* findings by `Line 144:` / `Line 126:`. Consequences:
- The phrase tripwire cannot fire on this body under **any** implementation, per-phrase-scoped or not, because neither phrase is present. The row therefore provides zero evidence for Decision 11's scoping — the exact thing it is cited as pinning (edge-cases r2-F-7).
- "A parse returning 2" is unreachable: there is no section summary matching D2 step 5's patterns and no `` `L-L`: `` item header anywhere in the body, so no naive parse produces 2 either.

The specimen that actually carries the claimed shape is `5135914911` (row 17): its top-level prompt block does restate the outside-diff finding under `Outside diff comments:` at body line 67, inside a ``` fence. That is where Decision 10's double-count risk and Decision 11's masking are genuinely exercised.
**Suggested fix:** Rewrite row 19 to what the specimen supports — "zero items, neither tripwire fires; this body has no harvestable section and no occurrence of either tripwire phrase, so it pins only that a section-less body parses cleanly." Move the Decision-10 / phrase-masking pin into row 17, restated against `5135914911`: "its top-level `🤖 Prompt for all review comments with AI agents` block restates the outside-diff finding under `Outside diff comments:` (body line 67, inside a fence); a parse returning 2 items has violated Decision 10, and a fired phrase tripwire means the fence mask or the per-phrase scoping was not implemented." Also correct § Decision 10's aside (:289–293) to attribute the observation to `5135914911`.

### F-5: Test row 14's regex still cannot match the backslash-continued antipattern, which is the only form the spec ever writes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 14 (:1246 command, :1264 expectation)
**Claim:** *"`grep -cE 'gh api --paginate.*\| *(wc|jq)' $S` … `[guard]` `0` — no fetch is piped straight into an aggregate (Decision 7)."* Closure manifest: *"row 14 uses `.*` and now catches the antipattern."*
**Why this is wrong:** `grep` is line-oriented. Every `gh api --paginate` invocation in this spec is written across two lines with a `\` continuation (D1 (a), (b), (c); D2 step 1; D5's three queries; D6; D8; D7's guard), so a wrong implementation would write the antipattern the same way and the `| wc -l` would land on the *second* line. Verified:

```
gh api --paginate repos/o/r/pulls/1/comments \
  --jq '.[] | .id' | wc -l
```
`grep -cE 'gh api --paginate.*\| *(wc|jq)'` → `0`. The single-line form matches, but nothing in the spec would be written that way. The guard is therefore inert for Decision 7's most load-bearing rule — the same defect class as the round-3 `[^\n]` regex, in a different disguise.
**Suggested fix:** Use a multiline-capable check. Either `rg -U -c 'gh api --paginate(\\\n|.)*?\| *(wc|jq)\b' $S` (ripgrep is available in this environment), or a line-based two-step that is honest about its limits: `grep -n -A2 'gh api --paginate' $S | grep -cE '\| *(wc|jq|head|tail|sed|cut)\b'`. Whichever form is chosen, state its expected count in the row and re-measure the Pre.

### F-6: D2's finding record and D3's triage record disagree on the `origin` field's value domain
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D2 (:775–778) vs § D3 (:826)
**Claim:** D2: *"Each surviving item becomes a finding record: `{origin: "body", section: "outside-diff" | "nitpick", review_id, key, path, lines, severity, title, body}`."* D3: *"The triage record gains an `origin` field (`inline` / `body:outside-diff` / `body:nitpick`)…"*
**Why this is wrong:** Two adjacent sections declare two incompatible shapes for the same field. D2 hands Step 3 a record with `origin: "body"` plus a separate `section`; D3 says the record carries a single combined `origin` whose domain includes `body:outside-diff` — a value D2's schema can never produce, and it drops the `section` field D2 says is load-bearing. 6e's report line (`outside-diff: b1, nitpick: b2`, :1078) and 6f's body shape (`(outside-diff)` / `(nitpick)`, :1016–1018) read the split, so a round-trip write-site/read-site trace mismatches on the field name.
**Suggested fix:** Pick one. Simplest is to make D3 agree with D2: "The triage record carries D2's `origin` (`inline` / `body`) and, for body findings, `section` (`outside-diff` / `nitpick`), so 6f can route the disposition and 6e can report the split." Then add `origin: "inline"` explicitly to the inline path so both origins have the same shape.

### F-7: D2 step 5's "blockquote depth is constant within a provisional span" is false for the last section
**Severity:** P3
**Where:** spec § D2 step 5 (:669–670)
**Claim:** *"Blockquote depth is constant within a provisional span, because a section summary is exactly where depth changes."*
**Why this is wrong:** A provisional span that has no following section runs "to end of body" (:665–667), and depth is not constant over that region. Verified on PR #28 `5135914911`: the Outside-diff section's provisional span runs body line 8 → 127; lines 8–~40 are at depth 1 while lines 41–127 (the `🪄 Autofix`, `ℹ️ Review info`, and top-level prompt blocks) are at depth 0. Step 6a then strips one `>` level from lines that never had one. The consequence is benign here — step 7's depth walk terminates at the true section end before any of that region is sliced into content — but the stated invariant is what a later editor would rely on when deciding whether the per-section normalization can be simplified, and it does not hold.
**Suggested fix:** Restate as: "Blockquote depth is constant within the *true* section, because a section summary is exactly where depth changes; a provisional span may extend past the true section into depth-0 trailer blocks, which step 7's walk discards before any content is sliced. Stripping is a no-op on lines that carry no `>`."

## Summary
P0: 0 | P1: 1 | P2: 5 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=5 P3=1 P4=0
