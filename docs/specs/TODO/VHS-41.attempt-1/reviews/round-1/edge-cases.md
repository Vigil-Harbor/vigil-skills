# Edge-Cases Review — round 1

Grounding: spec, brief, Plane VHS-41 (memory hit, matches brief), global + project CLAUDE.md, and the full current `skills/review-pr/SKILL.md` (406 lines) read from disk.

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Step 2 fetch (a) drops `body`, but the infrastructure-error check is specified to read it from that record
**Severity:** P0
**Where:** spec § Design D1 (`spec.md:249-250`, `:274-278`); current `skills/review-pr/SKILL.md:68-69`, `:79`
**Edge case:** CodeRabbit posts an infrastructure-error review ("Failed to clone", "🔥 Problems").
**What happens:** The current file projects `{id, state, submitted_at, body}` and `:79` reads that `body`. D1's replacement (a) projects `{id, state, submitted_at}` — no `body` — yet D1's prose says "The infrastructure-error check at `:79` keeps reading the **latest verdict** review's body (from (a)'s highest-id record)". There is no body in that record. An implementer either silently drops the infra-error check (CodeRabbit clone failures then flow into the harvest as a zero-item body and the run reports "nothing new" instead of re-triggering the review) or re-adds `body` to the stream, which under `--paginate` dumps every verdict review body on the PR into the agent's context.
**Why the spec misses it:** the projection change is presented as "unchanged semantics, page-safe form" (spec.md:245), so the dropped field was not noticed as a semantic change.
**Suggested fix:** in D1, state explicitly that after taking (a)'s highest-id record the skill fetches that one body with the single-resource call already introduced for harvest (`gh api repos/{owner}/{repo}/pulls/<N>/reviews/<VERDICT_ID> --jq '.body'`), runs the infra-error check on it, and short-circuits before fetch (b)'s per-review body fetches — not merely before the Step 2b parse.

### F-2: 6d Phase 2's verdict fetch (`:341-342`) is left unpaginated and still uses `sort_by | last`
**Severity:** P0
**Where:** spec § Decision 5 (`spec.md:104-106`) vs Decision 7 (`:146`) vs Test plan item 7 (`:569-571`) vs Scope (`:27`) and Design D8 (`:474-478`)
**Edge case:** a PR with more than one page (30) of CodeRabbit reviews — routine here, since the skill's own edge case at `SKILL.md:404` notes CodeRabbit posts one bodiless `COMMENTED` review *per thread reply*, so a 5-thread round adds 5 reviews and a multi-round PR crosses 30 easily.
**What happens:** `gh api` returns reviews oldest-first. Without `--paginate`, `sort_by(.submitted_at) | last` on `:342` returns the newest verdict *on page 1* — an old `CHANGES_REQUESTED` (or the first `APPROVED`) — so 6d Phase 2 polls a stale state for all 9 attempts and 6e prints the wrong verdict. Silent wrong answer, no error.
**Why the spec misses it:** Decision 5 enumerates "all five `gh api` fetches (`:68`, `:75`, `:174`, `:194`, `:224`)" — there are **six** list fetches; `:341` is the sixth. Decision 7 and test item 7/8 do reference `:342`, so the spec contradicts itself, and the Scope row (`:27`) and Design section list only the "6d short-circuit", never `:341`, so an implementer following the Design leaves it unconverted while test item 7 says it must be converted.
**Suggested fix:** add `:341-342` to Decision 5's enumeration and give it a Design bullet under D8: `--paginate` plus the streaming `{id, state, submitted_at}` form, take the highest id, read `.state` off it.

### F-3: The Decision 11 tripwire cannot fire for the format drift it exists to catch
**Severity:** P1
**Where:** spec § Decision 11 (`:208-220`), § Design D2 step 3 and step 7 (`:301-308`, `:330-331`), § Edge cases (`:503-505`)
**Edge case:** CodeRabbit renames a section, drops the `(N)` count, changes the delimiter (`[1]`, `— 1 item`), or stops wrapping items in `<summary>`.
**What happens:** the declared count is captured *from the summary line itself* (`<summary>[^<]*Outside diff range comments \((\d+)\)</summary>`). If that line no longer matches, no section is found, no declared count exists, zero items are parsed, and there is nothing to compare — the tripwire is structurally unreachable. The run reports "no body-level findings" and the skill degrades back to exactly the silent blindness VHS-41 exists to remove, invisibly. Decision 11 claims to be "the debuggable tripwire for the one failure this change can introduce — a CodeRabbit body-format change that the parse no longer matches"; the mechanism covers only the sub-case where the summary still matches but the *items* inside don't.
**Why the spec misses it:** the tripwire is defined as a count comparison, which presupposes the count was successfully parsed.
**Suggested fix:** add a second, independent detector to D2 step 7 that does not depend on the summary regex: if the normalized body contains the case-insensitive phrase `Outside diff range` or `Nitpick comments` anywhere, but no section was matched, report the same tripwire (phrase found, section regex did not match, review id, raw ±10 lines around the phrase) and treat the run's body-harvest as untrusted. Also specify where the raw section text is emitted — 6e's line (`:485`) carries only `declared N, parsed M`, which is not enough to debug a drift.

### F-4: The `no-push` disposition marker is not unique, so the idempotency guard suppresses genuinely new dispositions
**Severity:** P1
**Where:** spec § Decision 12 (`:222-233`), § Design D7 (`:438-445`, `:466`)
**Edge case:** two separate `/review-pr` runs on the same PR where neither round pushes (all body findings skipped) — the normal shape for a nitpick-only review, and the skill is explicitly re-runnable (`SKILL.md:160`, `:374`).
**What happens:** run A posts `<!-- review-pr:body-dispositions:no-push -->`. CodeRabbit later posts a new body finding; the operator re-runs; the round triages the new item, skips it, computes marker `no-push`, the guard finds run A's comment, and the post is **skipped**. The new finding's disposition is never recorded — a silent hole in the audit trail, in exactly the place this ticket exists to close. Worse, the run reports success; only 6e's `dispositions posted in <comment-url>` line would point at a stale comment.
**Why the spec misses it:** Decision 12 reasons about "genuinely distinct rounds still each get their comment" assuming rounds are distinguished by fix SHA, but the `no-push` sentinel collapses every non-pushing round across every run into one identity.
**Suggested fix:** make the marker unique per round regardless of push: `<!-- review-pr:body-dispositions:<HEAD_SHA-or-no-push>:<sha256-of-sorted-finding-keys> -->`, or `:no-push:<highest LAST_BODY_REVIEW_ID in this round>`. Guard on the full marker. State that a marker match means "this exact disposition set was already posted", not "this round already ran".

### F-5: Harvesting every body-carrying review on the PR defeats the `APPROVED` short-circuit and re-triages closed history on every run
**Severity:** P1
**Where:** spec § Decision 2 (`:65-72`), § Design D1 (`:273`, `:278-281`), § Design D2 step 1 (`:288-291`)
**Edge case:** re-running `/review-pr` on a mature PR — one that has already been through two or three rounds and/or is already `APPROVED`.
**What happens:** three compounding effects. (a) Step 2's `:81` short-circuit ("`APPROVED` and no unresolved comments → Nothing to review, stop") is redefined at `spec.md:278-281` to require "no body-level findings from the harvest" — but the harvest reads *every* historical body, so any nitpick ever emitted keeps the short-circuit permanently off; an approved PR now runs a full triage pass and posts a new PR comment on it. (b) Every historical body item is re-verified against the file (Step 3 sub-step 2 reads the file per finding), so a PR with 4 prior reviews × 5 nitpicks costs 20 file reads and 20 triage judgments per run, every run. (c) Every body must be pulled in full — CodeRabbit bodies with walkthrough tables run tens of KB — and Decision 5 forbids trimming; with no bound on the harvest set this is an unbounded context load in Step 2 alone. There is no cap and Decision 6 explicitly declines to add one.
**Why the spec misses it:** Decision 2's rationale argues correctly that Step 2 must not read *only the latest* body, and the "Why every review on the PR" paragraph (`:65-72`) answers a different objection (parity with the unfiltered inline fetch) without pricing the re-run case.
**Suggested fix:** bound the Step 2 harvest — either to bodies at or newer than the oldest review with an unresolved thread, or to the N most recent body-carrying reviews (N=3 covers the PR #28 incident), with the rest reachable via an explicit `--full` behavior. And restore `:81`: an `APPROVED` verdict with no unresolved threads should still short-circuit, since every body item predating the approval was, by construction, already dispositioned or superseded.

### F-6: `<details>`/`<summary>`/item-header tokens quoted inside CodeRabbit's own code snippets break the depth counter
**Severity:** P1
**Where:** spec § Design D2 step 3 (`:303-308`) and step 5 (`:310-324`)
**Edge case:** a finding whose quoted code contains the literal strings the parser counts. This is not hypothetical for this very change: VHS-41 adds `<details><summary>…Outside diff range comments (N)</summary>` and `` `171-171`: _🟡 Minor_ ``-shaped examples *into* `skills/review-pr/SKILL.md`, and CodeRabbit quotes the changed lines of a Markdown file back in its findings. Any PR touching this skill, or any Markdown/HTML file containing `<details>`, hits it.
**What happens:** "count `<details>` and `</details>` occurrences and end the section where the depth returns to zero" mis-computes the section boundary. Depth-too-high truncates the section early (items silently lost — the tripwire *may* catch it if a declared count survives), depth-too-low ends the section early and can spill the scan into the `⚠️ Duplicate comments` section or the top-level `🤖 Prompt for all review comments` block, violating Decisions 1 and 10 and double-counting findings. A stray `` `12-30`: `` line inside a quoted snippet also opens a phantom item.
**Why the spec misses it:** the parse was derived from two live specimens (PR #28, petland #64) whose findings happened not to quote HTML.
**Suggested fix:** add a normalization sub-step to D2 step 2: before matching, mask fenced code blocks (``` and ~~~, tracking fence length and language tag) and inline-code spans, so no `<details>`, `</details>`, `<summary>`, or item-header pattern inside them is counted. Add a specimen to the test plan: a body whose finding quotes a line containing `<details>`.

### F-7: The new harvest fetches have no failure handling
**Severity:** P1
**Where:** spec § Design D1 (`:263-271`), D2 step 1 (`:288-291`), D5 (`:391-394`)
**Edge case:** `gh api repos/…/reviews/<REVIEW_ID>` returns 404 (review dismissed/deleted), 403 (token scope, SAML), 429 (secondary rate limit — the harvest multiplies API calls by the number of body-carrying reviews on top of the now-paginated list fetches), or the network drops mid-`--paginate`.
**What happens:** unspecified. `gh api --jq '.body'` exits non-zero with an error on stderr and the agent has no stated behavior — most likely it moves on, and the round proceeds as if that review carried no findings. That is a silent skip of a finding source, i.e. the original bug, now with an extra failure axis. `--paginate` failing on page 3 of 5 is worse: it yields a *partial* stream that looks well-formed, and the harvest set is silently short.
**Why the spec misses it:** D7 carefully specifies error handling for the disposition *post* (`:468-471`) but nothing for the *fetches*, even though a dropped fetch loses a finding while a dropped post only loses a record.
**Suggested fix:** add to D1/D2: any non-zero exit or `Error:` output on a harvest fetch is reported as a first-class run outcome (`REVIEW_SIGNAL` cannot be `verdict-landed`; the 6e report gains `Body harvest failures: <review id> <code>`), with one retry on 429 honoring `Retry-After`, mirroring 6c. A partial `--paginate` result must never be treated as complete.

### F-8: 6a's body query returns `{id}` only, and its outcome rule reads any zero-item body-carrying review as `verdict-landed`
**Severity:** P1
**Where:** spec § Design D5 (`:391-394`, `:399-404`)
**Edge case:** a body-carrying review with `state == "COMMENTED"` and zero parsed items — e.g. CodeRabbit's conversational reply to a PR comment. The 6c-body disposition comment this spec introduces makes such replies *more* likely, not less.
**What happens:** two defects. (a) The stated outcome rule requires `state != "COMMENTED"` **and** `submitted_at > PUSH_TIME`, but the query projects only `{id}` — neither field is available, so the verdict-landed test is undecidable from the queries the spec gives, and no third query is specified. (b) The sentence "A body-carrying review that parsed to **zero** items … is exactly this case, not a new-findings case" generalizes past its example: followed literally, a `COMMENTED` chat reply sets `REVIEW_SIGNAL=verdict-landed`, which under the honesty rule at `SKILL.md:370` licenses the skill to report **"no new findings"** while a real incremental review is still inbound. That is precisely the false negative the honesty rule and the PR #51 postmortem exist to prevent, reintroduced through a new door.
**Why the spec misses it:** D5 reuses the harvest filter (Decision 8, non-empty body, any state) for a decision that Decision 8 itself says needs the verdict filter.
**Suggested fix:** project `{id, state, submitted_at}` in D5's second query, and restate the rule as: zero parsed items → `verdict-landed` **only if** that review also satisfies `state != "COMMENTED" AND submitted_at > PUSH_TIME`; otherwise the poll continues and can still end `inconclusive`.

### F-9: Dedup (D2 step 6) runs before the tripwire comparison (step 7), so legitimate restatements fire a false tripwire
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design D2 steps 6-7 (`:326-331`)
**Edge case:** the same finding appears in two harvested bodies (Round 1 harvests all reviews per Decision 2; Decision 9 explicitly anticipates "a finding restated in a later review body").
**What happens:** step 6 drops the already-triaged item, then step 7 compares "the item count parsed in each section" — now post-dedup — against the declared count, and reports a mismatch. Operators learn the tripwire is noisy and stop reading it, which disarms the one detector guarding against real format drift.
**Why the spec misses it:** steps 6 and 7 were written independently; the step numbering implies an order neither decision reasons about.
**Suggested fix:** state in step 7 that the comparison uses the **pre-dedup** extraction count, and that dedup is applied afterward; report deduped items separately (`declared N, parsed N, N-k deduped`).

### F-10: A body-only fix round enters 6d Phase 2 against an empty thread set
**Severity:** P2
**Where:** spec § Design D8 (`:474-478`); `SKILL.md:283`, `:308-316`, `:331-345`
**Edge case:** a round whose only fix-categorized findings are body-level (the exact scenario "Done when" #1 describes).
**What happens:** the short-circuit ("no fix-categorized findings across ALL rounds") no longer fires, because a body finding is fix-categorized. Phase 1 then scans review threads and finds none belonging to this round; "all_resolved if every thread's `.isResolved` is true" is vacuously true over an empty array, so the run enters Phase 2 and burns 9 verdict polls plus 8 thread polls — 17 tool calls — on a state nothing in this round can change. D8 asserts body items "never hold Phase 2 open" but nothing in the design keeps Phase 2 from being *entered* on their account.
**Why the spec misses it:** D8 addresses the operator-confusion symptom ("so an operator does not hunt for a missing thread") rather than the control-flow consequence.
**Suggested fix:** scope the 6d short-circuit to fix-categorized findings **with an inline thread**; body-only fix rounds skip Phase 1 and enter Phase 2 only under the existing `request_changes_workflow` rule.

### F-11: The idempotency guard's jq will error on a null comment body
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design D7 (`:440-441`)
**Edge case:** an issue comment whose `body` is `null` (deleted/hidden comment, some bot payloads).
**What happens:** `select(.body | contains(...))` raises `null (null) and string … cannot have their containment checked`, jq exits non-zero, the whole paginated stream aborts. Per D7's "on failure log and continue", the skill then posts — producing the duplicate comment Decision 12 exists to prevent.
**Why the spec misses it:** Decision 8 was careful to write `(.body // "")` for review bodies; the same guard was not carried to the issue-comment query.
**Suggested fix:** `select((.body // "") | contains("…")) | .id`, and state that an errored guard fetch means **do not post** (fail closed), rather than post-and-duplicate.

### F-12: `Unlabeled` → "treat as Minor" collides with the Nitpick section's "default to skip"
**Severity:** P2
**Where:** spec § Design D3 (`:345-354`)
**Edge case:** an item inside `🧹 Nitpick comments` carrying no `Critical|Major|Minor|Trivial` span — common, since nitpick items frequently carry only a category label (`_🛠️ Refactor suggestion_`).
**What happens:** two rules apply and disagree. The severity table's new `Unlabeled` row says treat as Minor (Minor = "fix if trivial and correct"); the rewritten Nitpick row says items are triaged "at their own labelled severity with a default action of skip". An implementing agent picks arbitrarily, so identical inputs produce different dispositions across runs, and a nitpick may be fixed and pushed where the brief's Decision 1 rationale expects a recorded skip.
**Why the spec misses it:** the two rows were written for different concerns (missing label vs. section semantics) and their intersection was not considered.
**Suggested fix:** state precedence explicitly — inside the nitpick section, `Unlabeled` resolves to skip-by-default; elsewhere it resolves to Minor; the report notes the missing label either way.

### F-13: No bound on body-level items per round
**Severity:** P2
**Where:** spec § Decision 6 (`:113-120`), § Design D7 (`:447-460`)
**Edge case:** a large PR whose `🧹 Nitpick comments (34)` section spans a dozen files — the body analogue of the existing "pathological 30+ findings" edge case at `SKILL.md:399`.
**What happens:** every item triggers a file read plus a triage judgment (Step 3 sub-steps 2-4), all in one round, plus a 34-line disposition comment. There is no cap and no truncation rule; Decision 5 forbids trimming, and Decision 6 declines any bound. The round exhausts its budget mid-triage with fixes possibly already pushed and no disposition comment posted.
**Why the spec misses it:** Decision 6 reads scale as "how many PRs", not "how many findings inside one body".
**Suggested fix:** add an edge case: above a stated item threshold (say 20 body items in one round), triage the outside-diff section fully, batch-skip the remaining nitpicks with a single grouped disposition line naming the count and the reason, and report the deferral in 6e.

### F-14: The parse cache is unbounded conversational state with no re-derive fallback
**Severity:** P2
**Where:** spec § Design D2 step 1 (`:290-291`), D5 (`:396-397`), D6 (`:419-422`), `SKILL.md:180`
**Edge case:** the cache must survive up to 10 poll attempts × 3 fix-push cycles of individual Bash tool calls, and a context compaction in between.
**What happens:** unlike `PUSH_TIME` and `PREV_REVIEW_ID` (scalars), the cache is a structured set of parsed items across N reviews. If it is lost or partially recalled, D6's "reusing the cached parse from 6a rather than re-fetching" has no stated fallback, and the round can triage a truncated item set — silently.
**Why the spec misses it:** it leans on `:180`'s existing note, which was written for two scalars.
**Suggested fix:** state that the cache is an optimization only: if the parsed items for any review id in the round's harvest set are not confidently in hand, re-fetch and re-parse that body; dedup by Decision 9 key makes re-parsing safe.

### F-15: An item with no line-range header never matches, and only the tripwire notices
**Severity:** P3
**Where:** spec § Design D2 step 5 (`:314-315`)
**Edge case:** a file-scoped body finding (no line range), or a range in a non-numeric form (`L12-L20`).
**What happens:** `` ^`(?<lines>\d+(?:-\d+)?)`: `` does not match, the item is not extracted, and detection depends entirely on the declared-count tripwire — which F-3 shows can itself be absent.
**Suggested fix:** widen the header pattern to `` ^`(?<lines>[^`]+)`:\s ``, validate the captured range separately, and record a non-numeric range verbatim in the finding's `lines` field.

### F-16: Marker extraction vs. `<details>` stripping order is unspecified
**Severity:** P3
**Where:** spec § Decision 9 (`:171-183`), § Design D2 step 5 (`:322-324`) and step 6
**Edge case:** a body shape where the `<!-- cr-comment:v1:… -->` marker sits *inside* the nested `<details>` block rather than after it.
**What happens:** Decision 10's strip removes the marker before Decision 9 keys the item, so the key silently falls back to `(path, line-range, title)` and dedup weakens. Degrades gracefully, but the fallback becomes the default without anyone noticing.
**Suggested fix:** in D2 step 5, extract the `cr-comment` marker from the raw item span **before** stripping nested `<details>` blocks.

### F-17: Blockquote normalization mangles legitimate `>` lines inside an item body
**Severity:** P3
**Where:** spec § Design D2 step 2 (`:294-298`)
**Edge case:** a finding whose prose quotes a diff line or a Markdown blockquote.
**What happens:** "strip every leading `>` … from every line" is applied to the whole body unconditionally, so a `>` that is content, not blockquote structure, is removed. Triage still reads sensible prose, so the impact is cosmetic — but a quoted diff `>` in a fix suggestion loses meaning.
**Suggested fix:** strip at most the depth needed to enter the section (track the blockquote depth at the section's opening `<summary>` and remove exactly that many markers per line), rather than all leading `>`.

### F-18: Two concurrent runs both pass the marker guard
**Severity:** P3
**Where:** spec § Decision 12 (`:228-231`)
**Edge case:** the operator (or two agents) runs `/review-pr <N>` twice against the same PR at once.
**What happens:** check-then-post is not atomic; both runs see no marker and both post. Last-writer-wins does not apply — both comments persist. Low probability, harmless output, but undocumented.
**Suggested fix:** one sentence in Decision 12 acknowledging the check-then-post race and stating that duplicate comments are tolerated (the marker makes them recognizable) rather than prevented.

## Summary
P0: 2 | P1: 6 | P2: 6 | P3: 4

STATUS: RED P0=2 P1=6 P2=6 P3=4
