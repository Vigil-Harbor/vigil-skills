# Edge-Cases Review — round 2

Grounding: spec + brief re-read from disk, Plane VHS-41 retrieved (namespace `skills`, tag-exact, matches the brief), global + project `CLAUDE.md`, all three round-1 reports, and the full current `skills/review-pr/SKILL.md` (406 lines). `scale_lens == off` and no `scalability.md` exists in `round-1/`, so nothing to guard against.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Step 2 fetch (a) drops `body` | CLOSED | spec § D1 fetch (a2), lines 366-368; order stated line 381-386 |
| edge-cases | F-2 | `:341` unpaginated with `sort_by\|last` | CLOSED | § Decision 5 line 120-121 names six fetches; § D8 lines 700-712 converts |
| edge-cases | F-3 | count tripwire structurally unreachable | CLOSED | § Decision 11 lines 255-267 — two detectors, phrase detector independent of the summary regex, raw ±10 lines reported |
| edge-cases | F-4 | `no-push` marker collides | CLOSED | § Decision 12 line 279-281 rekeys to `r<R>`; test row 11 pins `no-push` absent. (New defects in the replacement: F-1, F-2 below) |
| edge-cases | F-5 | unbounded harvest defeats `:81` | CLOSED | § Decision 2 lines 56-59; § D1 line 388-393 keys `:81` on findings not harvest-set size; 10-review bound line 419-424. (New defect in the resume: F-1 below) |
| edge-cases | F-6 | `<details>` in code samples breaks the walk | CLOSED | § D2 step 4b lines 444-450. The test-plan specimen the fix also asked for was not added → new P2 F-7; the blockquote/mask interaction is new P1 F-3 |
| edge-cases | F-7 | no failure handling on harvest fetches | PARTIAL | § Decision 14 lines 323-342 covers 6a's signal, but the guard is not applied at Step 2's `:81` / `:381` exits (new P1 F-2) nor detectable through the `\| wc -l` pipe (new P1 F-4) |
| edge-cases | F-8 | 6a body query projects `{id}` only | CLOSED | § D5 line 591 projects `{id, state, submitted_at}`; rule at 599-607 requires both conditions |
| edge-cases | F-9 | dedup before tripwire | CLOSED | § Decision 11 lines 257-259; § D2 step 10 line 506-508 |
| edge-cases | F-10 | body-only fix round enters 6d Phase 2 | CLOSED | § D8 lines 713-721 scopes the Phase 1 short-circuit to fix findings with an inline thread; § Decision 4 lines 104-107 |
| edge-cases | F-11 | null comment body breaks guard jq | CLOSED | § D7 line 660 `(.body // "")`; fail-closed line 662-663 |
| edge-cases | F-12 | Unlabeled vs nitpick default collide | CLOSED | § D3 lines 542-544 states precedence |
| edge-cases | F-13 | no bound on body items per round | PARTIAL | § D2 step 9 lines 499-504 adds the 20-item bound, but the grouped/deferred items are permanently dropped by the marker advance (F-1) and the outside-diff side is still unbounded (F-10) |
| edge-cases | F-14 | parse cache has no re-derive fallback | CLOSED | § D2 step 3 lines 428-431 |
| edge-cases | F-15 | non-numeric line range | CLOSED | § D2 step 7 lines 480-484 |
| edge-cases | F-16 | marker extraction vs `<details>` strip order | CLOSED | § Decision 9 lines 219-221; § D2 step 7 line 490-491 |
| edge-cases | F-17 | blockquote strip depth | CLOSED | § D2 step 4a lines 435-442. (Scoping of that depth is new P1 F-3) |
| edge-cases | F-18 | concurrent runs race | CLOSED | § Decision 12 lines 294-296; § D9 line 799-800 |
| correctness | F-1 | infra-check reads a dropped body | CLOSED | § D1 (a2) + order, lines 366-386 |
| correctness | F-2 | depth walk off by one | CLOSED | § D2 step 5 lines 458-465 begins at the preceding `<details>` |
| correctness | F-3 | `:381` never amended | CLOSED | § D9 lines 742-746 |
| correctness | F-4 | `:341` omitted from Decision 5 | CLOSED | § Decision 5 line 120-121; § D8 lines 700-712 |
| correctness | F-5 | `no-push` marker collides | CLOSED | § Decision 12 lines 282-288 |
| correctness | F-6 | no-push call site unlocated | CLOSED | § D4 lines 573-576; § D7 lines 650-652 amends `:245`. (Residual 6b path → P2 F-6) |
| correctness | F-7 | file-group regex matches the summary | CLOSED | § D2 step 6 lines 471-475 scans from the line after the summary |
| correctness | F-8 | `sync.py status` expectation false | CLOSED | § Test plan Observational, lines 875-880; § Done when 2 |
| correctness | F-9 | Decision 2 widens "verdict review" | CLOSED | § Decision 8 evidence-status para, lines 199-205 |
| correctness | F-10 | `LAST_BODY_REVIEW_ID` advance undefined | CLOSED | § D6 lines 627-632 |
| conventions | F-1 | helper-script claim false | CLOSED | § Decision 13 lines 300-321 |
| conventions | F-2 | two severity rules | CLOSED | § D3 lines 534-539; § D2 step 7 lines 493-494 |
| conventions | F-3 | `AGENTS.md` stale | CLOSED | § Scope row line 29; § D10 lines 808-814 |
| conventions | F-4 | test plan drops prose-spec gate shape | CLOSED | § Test plan gate tables, lines 827-849 |
| conventions | F-5 | `sync.py status` not a gate | CLOSED | § Test plan lines 875-880, 889-891 |
| conventions | F-6 | "no test suite" claim | CLOSED | § Test plan lines 818-822; § Deferred lines 941-944 |
| conventions | F-7 | section naming convention | CLOSED | `### 2b.` line 396, `### 6f.` lines 639-643 |
| conventions | F-8 | monotonic-id grounding | CLOSED | § Decision 7 lines 177-180 |
| conventions | F-9 | `--body-file` path inside worktree | CLOSED | § D7 lines 667-673 |
| conventions | F-10 | `requires:` deferral citation | CLOSED | § Out of scope 2, lines 915-922 |
| conventions | F-11 | intent-phrased prose | CLOSED | § Design preamble lines 348-352 |

## Findings

### F-1: The disposition marker advances past reviews that were never dispositioned, making them permanently unharvestable
**Severity:** P1
**Where:** spec § Decision 12 line 279-281; § D2 step 1 lines 410-413; § D2 step 2 lines 419-424; § D6 lines 627-632
**Edge case:** three reachable paths, all created by this round's marker-resume machinery.
1. **Harvest-set bound.** A first run against a mature PR with 15 body-carrying reviews parses the 10 newest and reports the 5 omitted ids. `R` = "the highest review id in the round's **harvest set**" — which is one of the parsed 10. The marker posts as `r<R>`.
2. **Decision 14 harvest failure.** Review `X` in the harvest set 404s/429s twice. Decision 14 records the failure and forces `inconclusive`. `X` is still in the harvest set, so `R ≥ X`.
3. **Failed 6f post in a multi-round run.** Round 2's 6f post fails (D7: "on failure log and continue"). Round 3 triages items and posts `r<R3>`, `R3 > R2`.

**What happens:** the next run computes `PRIOR_DISPOSITIONED_REVIEW_ID = R` and harvests only `id > R`. In (1) the 5 omitted reviews — which may carry Critical/Major outside-diff items, not just nitpicks — are excluded forever. In (2) the review that *never answered* is excluded forever, so Decision 14's whole remedy ("degrades to `inconclusive`, whose honesty rule already tells the operator to re-run") is hollow: the prescribed re-run cannot reach it. In (3) round 2's dispositions are unrecoverable — the audit-trail hole the ticket exists to close, silently reintroduced. All three are silent on the *next* run; nothing re-reports them.
The bound's own operator message makes it worse — `re-run after this round's disposition marker advances` (line 421) instructs the operator to do the exact thing that makes the omitted reviews unreachable.
**Why the spec misses it:** Decision 12 chose `R` for monotonicity and uniqueness ("`R` is monotone and unique per round whether or not the round pushed", line 288) and never asked whether every id `≤ R` was actually dispositioned. Decision 2 frames the marker as "the durable record of *handled*" (line 75) while three new mechanisms — the 10-review bound, Decision 14's failure path, and D7's log-and-continue post — all produce reviews that are in the set but not handled.
**Suggested fix:** define `R` as **the highest review id that was actually parsed, triaged, and included in this comment**, and add the invariant to Decision 12: *no review id at or below the marker may have been omitted by the bound, failed a harvest fetch, or been deferred by the 20-item bound*. Concretely: (a) the bound parses the **10 oldest** unhandled reviews, not the newest, so `R` advances contiguously and the newest are picked up on the next run; or, if newest-first is preferred, `R` = the highest id below the lowest omitted id. (b) If any review in the round's harvest set failed its fetch, cap `R` below that id (and if the failure is the lowest id in the set, post the comment with no marker, or suppress the post). (c) In a multi-round run, if any earlier round's 6f post failed, do not post a later round's marker above that round's `R`. (d) Fix the bound's operator message — the current text is actively wrong advice.

### F-2: A failed harvest at Step 2 exits "Nothing to review" — Decision 14's fail-closed rule only guards 6a
**Severity:** P1
**Where:** spec § D1 lines 388-393 (amended `:81`); § D9 lines 742-746 (rewritten `:381`); § Decision 14 lines 334-337
**Edge case:** the 2b harvest's list fetch, a single-review body fetch, or the `PRIOR_DISPOSITIONED_REVIEW_ID` resume fetch fails (403 token scope, 429 secondary limit — likely, since the harvest multiplies API calls by the number of body-carrying reviews — or a dropped `--paginate` page), on a PR whose latest verdict is `APPROVED` with no unresolved inline threads, or on a PR with no new inline comments.
**What happens:** the harvest "produced no body-level findings" **vacuously**. `:81` fires: *"Nothing to review — PR is approved"*, and the run stops. Or `:381` fires: *"Nothing to review"*, exit. Decision 14's protection is written entirely in terms of `REVIEW_SIGNAL` (`"While any harvest failure stands, REVIEW_SIGNAL must not be verdict-landed"`), and `REVIEW_SIGNAL` is a **6a** variable — the flow exits at Step 2 and never reaches 6a, so nothing degrades to `inconclusive`. A finding source that did not answer is reported to the operator as a clean bill of health, on the two earliest and most confident exits in the skill. This is the original bug (a finding the skill never sees) with a new failure axis, and it is *more* damaging than the 6a case because both exit lines are affirmative.
**Why the spec misses it:** Decision 14 was written against the round-1 F-7 finding, which was scoped to 6a/6b; the amended `:81` clause and the rewritten `:381` were written under D1/D9 for a different concern (Decision 2's resume window) and the two never met.
**Suggested fix:** add a clause to Decision 14: *"A standing body-harvest failure also blocks every affirmative early exit. `:81`'s `APPROVED` short-circuit and `:381`'s 'Nothing to review' both require the harvest to have **completed**, not merely to have produced zero findings. On a harvest failure at Step 2, report `body harvest failed — cannot confirm 'nothing to review'` with the review id and status code, and exit `inconclusive` rather than clean."* Mirror the wording into D1 line 388-393 and D9 line 742-746 so an implementer editing either site sees it.

### F-3: One blockquote depth is computed per body, but a body carrying both sections has two different depths — which defeats the new code mask
**Severity:** P1
**Where:** spec § D2 step 4a lines 435-442 and step 4b lines 444-450; § D2 step 5 lines 452-465
**Edge case:** a single review body carrying **both** an Outside-diff section and a Nitpick section. This is CodeRabbit's ordinary shape, and the spec's own evidence establishes the two have different blockquote depths: the outside-diff section is wrapped in `> [!CAUTION]` (depth 1, verified on PR #28 `5135914911`), the nitpick section is not (depth 0, verified on petland `5123259707`). Both specimens are *different reviews*, so no specimen exercises the combined case.
**What happens:** step 4 is written as one normalization pass over the body ("The procedure operates on one review body at a time" line 399; "Determine the blockquote depth at **the section's** opening line and strip exactly that many … per line", singular) that runs **before** step 5 finds the sections. Two consequences, and the spec permits either:
- Depth taken as 0 (from the nitpick section): the outside-diff section's lines keep their `> ` prefixes, so its fenced code blocks read as `> ```bash` and step 4b's mask does not recognize them. Every `<details>`, `</details>`, `<summary>` and `` `12-30`: `` token quoted inside a code sample is then counted by the depth walk — the exact round-1 F-6 defect this round's masking rule was added to close, back in force: the section boundary mis-computes, items are silently lost, or the scan spills into the `Duplicate comments` section (violating Decision 1) and double-counts.
- Depth taken as 1 (from the outside-diff section): a stripping pass over the nitpick section removes a leading `>` that is *content*, which is round-1 F-17 unfixed for that section.

There is also a stated-order circularity: step 4a needs "the section's opening line", which step 5 computes; an implementer following the numbered order literally has no section to take a depth from.
**Why the spec misses it:** step 4a was written to answer F-17 (don't over-strip) and step 4b to answer F-6 (mask before matching); both were reasoned against a single specimen at a time, and the sequencing (`4 → 5`) hard-codes body-scope on a property the spec itself documents as section-scoped.
**Suggested fix:** reorder and re-scope. Make section location the first operation, on **raw** text (the summary regex at step 5 is unanchored, so `> <summary>⚠️ Outside diff range comments (1)</summary>` still matches). Then, **per section**: (1) read the blockquote depth at that section's summary line; (2) strip exactly that depth from that section's span only; (3) mask fenced and inline code within that span; (4) run the depth walk. State explicitly that depth is a per-section property because the two sections observably differ, and add a specimen row to the test plan for a body carrying both (see F-7).

### F-4: `| wc -l` swallows `gh api --paginate`'s exit status, so Decision 14's partial-stream rule cannot be enforced at the site that introduces it
**Severity:** P1
**Where:** spec § Decision 7 lines 168-175; § D5 lines 583-585; § Decision 14 lines 338-340
**Edge case:** `gh api --paginate` fails on page 3 of 5 — network drop, secondary rate limit, token expiry mid-stream. Decision 14 already names this as the dangerous case: *"A `--paginate` stream that fails partway yields a **partial** result that looks well-formed. Treat a non-zero exit as invalidating the whole stream."*
**What happens:** the rule is unenforceable as written at 6a's inline-findings poll, which this spec converts to `gh api --paginate … --jq '… | .id' | wc -l`. In a pipeline the shell reports **`wc`'s** status, and `wc -l` on a truncated stream exits 0 with a smaller number. There is no `set -o pipefail`, no `${PIPESTATUS[0]}` check, and no stderr inspection anywhere in the spec. So a partial stream produces `new_inline = 0`; combined with a zero body-item count and a landed verdict, 6a sets `REVIEW_SIGNAL=verdict-landed` and 6e is licensed by the honesty rule to print **"no new findings"** — the PR #51 false negative, arriving through the new pagination machinery. The same masking applies to any future `| wc -l` the "stream one line per match, then `| wc -l`" pattern (line 171) invites, and Decision 5's remedy at line 791-792 ("redirect it to a file and read the file in slices") is the only place a redirect appears, and it is offered for a different purpose.
**Why the spec misses it:** Decision 7 introduced the pipe to make counts page-safe; Decision 14 was written later against the *fetch* failure axis and reasons about "non-zero exit" without noticing that the one command the spec pipes is the one whose exit status is now invisible.
**Suggested fix:** in Decision 7, state that any streamed fetch that feeds an aggregate is captured to a file first and the aggregate taken from the file, with the fetch's own exit status checked — e.g. `gh api --paginate … --jq '…' > "$TMP/new_inline" ; rc=$?` then `wc -l < "$TMP/new_inline"`, and `rc != 0` → body/inline harvest failure per Decision 14 (never a count of 0). If a pipeline is kept, require `set -o pipefail` on that Bash call and say so in the skill, since the skill's shell note (`SKILL.md:11`) does not set it today. Add a grep row pinning that no `gh api --paginate` in the file pipes into `wc -l` without one of the two guards.

### F-5: The resume high-water mark and the idempotency guard trust any comment on the PR, from any author
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D2 step 1 lines 404-407; § D7 lines 658-660
**Edge case:** a PR comment written by someone other than the skill that contains the marker text — an operator quoting a prior disposition comment in a follow-up, a handoff note pasting the comment body, a bot mirroring PR comments, or a review of *this very repo* where the marker literal is discussed.
**What happens:** the resume query scans **all** issue comments with no `select(.user.login == …)` filter and takes the numerically highest `r<id>` it finds. A quoted marker carrying a high id silently raises `PRIOR_DISPOSITIONED_REVIEW_ID`, and the harvest window for that PR closes over every review at or below it — permanently, and with no tripwire (both tripwires run inside a parsed body, not on the resume). The 6f guard has the same exposure in the other direction: a quoted marker makes the guard believe this round was already dispositioned and suppresses the post. Both failures are silent and both are exactly the audit-trail hole Decision 12 exists to close. (The literal in the shipped skill file is `r<R>`, non-numeric, so the file itself is safe — but a *rendered* marker in any comment is not.)
**Why the spec misses it:** Decision 12 reasons about the marker as a self-written record; the query it specifies does not encode that assumption. Every *review* fetch in the spec carries `select(.user.login == "coderabbitai[bot]")`; the two new *comment* queries carry no author predicate at all.
**Suggested fix:** filter both queries to comments authored by the account the skill posts as — resolve it once (`gh api user --jq .login`, or `gh pr comment`'s author) and add `select(.user.login == "<SELF>")` to the resume query at line 406 and the guard at line 660. State in Decision 12 that only a marker in a comment the skill itself authored counts as a durable record. Add a grep row asserting both new comment queries carry an author filter.

### F-6: The 6f invocation sites do not cover an incremental round whose body findings are all non-fix
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D6 line 633-634; § D7 lines 645-652; current `SKILL.md:241`, `:245`
**Edge case:** round 2+ where the incremental review carries only body-level nitpicks (or outside-diff items that triage to skip) and nothing is pushed — the single most likely body-level shape, since nitpicks default to skip (Decision 12 itself says "the all-skip path is the **most** likely one for body findings").
**What happens:** D6 amends only the **fix-push-loop** bullet (`:233`) to post 6f. The no-fix exit from 6b is `SKILL.md:241` ("If the incremental review has no new actionable findings … proceed to 6d"), which D6 does not touch. D7's other reachable site is `:245`, whose amended sentence reads *"If no fixes were pushed (all non-fix), non-fix replies are still posted **after Step 3 triage completes**"* — Step 3 is round-1 triage, so an implementer reading it literally does not apply it to a 6b cycle. Result: the round's body dispositions are never posted and no marker lands. 6e still prints `Body-level findings: B … dispositions posted in <comment-url>` with no URL — semi-visible, but the run reports otherwise-normal completion. Because no marker lands, a re-run does re-harvest, so this degrades rather than corrupts — hence P2, not P1.
**Why the spec misses it:** D7 asserts 6f is "invoked from the same points as 6c's replies" and treats that as sufficient, but 6c's own coverage of the 6b-all-non-fix path is exactly the pre-existing gap `:245`'s Step-3 wording leaves open — and this change makes that gap load-bearing for the disposition record.
**Suggested fix:** in D6, add a bullet amending `SKILL.md:241`: *"If the incremental review has no fix-categorized findings, post this round's non-fix replies and — if the round triaged ≥1 body-level finding — this round's 6f comment, then proceed to 6d."* And generalize `:245`'s wording from "after Step 3 triage completes" to "after that round's triage completes", so it covers Step 3 and every 6b cycle.

### F-7: The test plan verifies the happy parse only — no row exercises masking, a both-sections body, tripwire silence, or any failure path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan rows 14-17, lines 855-873
**Edge case:** every new mechanism this round added.
**What happens:** rows 14-16 walk three real bodies and pin item counts; row 17 pins the `<details>`/`<summary>` adjacency. Nothing pins:
- **the code mask (D2 4b).** Round-1 F-6's suggested fix asked for a specimen whose finding quotes a line containing `<details>`; the rule landed, the specimen did not. Since this change *puts* `<details><summary>…Outside diff range comments (N)</summary>` into `skills/review-pr/SKILL.md`, the first PR to exercise the new code is the one CodeRabbit will quote those lines back on — the mask is load-bearing on day one and unverified.
- **a body carrying both sections at different blockquote depths** — the F-3 case, and the case neither specimen covers.
- **tripwire silence.** Row 16 pins "zero items" on `5135878266` but not "neither tripwire fires". That body carries the top-level `🤖 Prompt for all review comments with AI agents` block restating outside-diff findings; if it contains the phrase `outside diff range`, the new phrase tripwire fires on a perfectly normal body and the detector becomes noise on the very first run.
- **any Decision 14 path** — no row induces or asserts a harvest-fetch failure, a partial stream, or the fail-closed guard.
**Why the spec misses it:** the test plan was carried forward from round 1, when the only verification question was "does the parse read the two known bodies"; the round-2 machinery (mask, tripwires, bounds, failure handling) added no rows.
**Suggested fix:** add rows: (a) each of rows 14-16 additionally asserts **neither tripwire fires** and names the parsed/declared/deduped counts; (b) a synthetic-body row — a body whose finding quotes ```` ```markdown ```` containing `<details><summary>x (1)</summary>` — asserting the mask keeps the item count at the declared value; (c) a row on any live review body carrying both an Outside-diff and a Nitpick section, asserting both parse; (d) a row asserting that with a harvest fetch forced to fail (e.g. an unreachable review id), the run reports `Body harvest failures` and does **not** print "Nothing to review" or `verdict-landed`.

### F-8: Whether triage receives masked or raw item text is unstated
**Severity:** P2
**Where:** spec § D2 step 4b lines 444-450; step 7 lines 477-491; finding record lines 510-513
**Edge case:** any body item whose finding includes a suggested diff or code sample — i.e. most of them.
**What happens:** step 4b masks code "before any structural matching"; step 7 then extracts "the item body" and the record carries a `body` field that feeds Step 3's verify-against-the-file loop. The spec never says whether the masked text is discarded after boundary computation and spans re-sliced from the raw body. An implementer who carries the masked text forward hands Step 3 a finding whose suggested code has been replaced by placeholders, so "verify whether the finding applies to the current code" (`SKILL.md:100`) runs against a claim with its evidence removed — a body item is then more likely to be skipped as unverifiable, and the 6f disposition reason is written from mutilated text. Degrades rather than crashes, but silently and in the direction of dropping findings.
**Why the spec misses it:** step 4b was added purely as a boundary-computation fix; the data-flow consequence for the record produced in step 7 was not traced.
**Suggested fix:** one sentence in step 4b: *"The masked text is used only to compute section, group, and item boundaries. Every span handed to step 7 and to Step 3 — item body, title, marker — is sliced from the **raw** (blockquote-stripped) text at those offsets."*

### F-9: Harvested bodies are bounded by count but not by size, and 2b has no slicing escape hatch
**Severity:** P2
**Where:** spec § D2 step 1 lines 415-417 and step 2 lines 419-424; § D9 lines 788-792
**Edge case:** a first run on a mature PR where up to 10 review bodies are fetched in full. CodeRabbit bodies with walkthrough tables and a `Nitpick comments (34)` section over a dozen files run tens of KB each; Decision 5 forbids trimming any of it.
**What happens:** the two bounds this round added are both on *counts* — 10 reviews, 20 surviving items — and the 20-item bound applies *after* parsing, so nothing bounds ingestion. Ten large bodies land in the agent's context before triage begins. The likely outcome is a context compaction mid-run, which is precisely what step 3's re-derive fallback then answers by **re-fetching the same bodies** — a loop that re-loads the bytes that caused the compaction. Neither bound reports on this axis, so the failure looks like a stalled or confused round rather than a named degradation, and Decision 6's promise that a pathological input "degrades **loudly and visibly**" does not hold for the size axis.
**Why the spec misses it:** Decision 6 explicitly frames the bounds as protection against "a pathological input"; the pathology it prices is item count, not body bytes.
**Suggested fix:** in D2 step 1, direct the per-review body fetch to a file in the temp/scratch directory (the same directory D7 already establishes for `<BODY_FILE>`) and have the parse read that file in slices — the remedy D9 line 791-792 already states for the no-trim rule, wired into the procedure rather than left in an edge-case bullet. Add a reported size bound alongside the count bound: if a body exceeds a stated size, report `body harvest: review <id> body is <n> KB — parsed from file` rather than inlining it.

### F-10: The 20-item bound leaves the outside-diff side unbounded, and its "deferral" has no return path
**Severity:** P3
**Where:** spec § D2 step 9 lines 499-504; § D8 line 731
**Edge case:** a section shaped `⚠️ Outside diff range comments (40)`.
**What happens:** the bound says "triage the outside-diff section **in full**, then group the remaining nitpick items" — so the pathological case the bound exists to contain is exempt from it whenever the items are outside-diff rather than nitpick. Separately, the grouped nitpicks are reported as "deferred" (`Body items deferred (per-round bound): … <n> nitpicks grouped`) but the marker advance (F-1) means no later run re-harvests them, so "deferred" is really "dropped, with a count recorded". Low severity — a grouped disposition line is still posted and nitpicks default to skip — but the report word is wrong.
**Suggested fix:** state that outside-diff items above the bound are also grouped once the round's total exceeds a stated hard ceiling, and change the 6e wording from "deferred" to "grouped (not re-harvested)" unless F-1's marker fix gives them a return path.

### F-11: The phrase tripwire's scope is ambiguous between per-phrase and per-body
**Severity:** P3
**Where:** spec § Decision 11 lines 260-262; § D2 step 10 lines 506-508
**Edge case:** a review body where one section matches and the *other* section's phrase appears only in prose — or a body with no sections at all that mentions "nitpick comments" in its summary line.
**What happens:** "the normalized body contains the case-insensitive phrase `outside diff range` or `nitpick comments` but **no section matched**" reads globally, so a body whose Nitpick section parsed fine suppresses the tripwire for a genuinely drifted Outside-diff section — a false negative on the detector added specifically to survive format drift. Read per-phrase instead, an ordinary body mentioning the other phrase in prose fires a false alarm, and operators learn to ignore the tripwire (the failure mode round-1 F-9 was raised to prevent). It is also unstated whether the phrase test runs on masked (4b) or unmasked text; on unmasked text, a quoted code sample containing the phrase fires it.
**Suggested fix:** make it explicitly per-phrase and post-mask: *"For each of the two phrases independently: if the masked, blockquote-stripped body contains the phrase (case-insensitive) and **that phrase's** section did not match, fire the phrase tripwire for that section."* Confirm on specimen `5135878266` that neither phrase fires (F-7 row (a)).

## Summary
P0: 0 | P1: 4 | P2: 5 | P3: 2

STATUS: RED P0=0 P1=4 P2=5 P3=2
