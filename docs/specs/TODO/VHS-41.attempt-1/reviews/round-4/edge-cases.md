# Edge-Cases Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `gh api --jq --arg` invalid | CLOSED | spec:603-612 (`export SELF` + `env.SELF`), :977-981, test row 13 (:1263). New residual risk raised as F-2 below |
| correctness | F-2 | Rows 4/8 pin unproducible counts | CLOSED | row 4 `≥ 10` with the 11-site enumeration (:1254); row 8 `≥ 3` (:1258) |
| correctness | F-3 | Bounded round posts no comment | CLOSED | § Decision 12 "Progress does not depend on findings" (:388-394); D7 findings-free body (:1024-1033) |
| correctness | F-4 | `verdict-landed` read off the body-carrying stream | CLOSED | D5's third query (:876-883) + the outcome rules at :891-902 |
| correctness | F-5 | D1 invocation-order contradiction | CLOSED | D1 § "Order matters" (:558-567) names the v3 contradiction and fixes it |
| correctness | F-6 | Phrase tripwire input no longer produced | CLOSED | phrase-scan view defined at :711-715, named at :307-325 |
| correctness | F-7 | Step 6 span circular | CLOSED | provisional span, D2 step 5 (:663-670) |
| correctness | F-8 | Two checklist commands cannot match | PARTIAL | fenced block (:1234-1249) fixes the `\|` escaping; row 14's regex is line-anchored and still cannot see the multi-line continuation shape every fetch in the file uses — verified, see F-10 |
| correctness | F-9 | Undefined `R` leaves guard nothing to match | PARTIAL | `r0` sentinel added (:988-993), but a constant key fed to an exact-match guard reintroduces suppression — see F-3 |
| conventions | F-1 | Row 4 count `9` | CLOSED | row 4 `≥ 10`, fetch (b) enumerated (:1254) |
| conventions | F-2 | Row 8 count `4`, `:341` twice | CLOSED | row 8 `≥ 3` with corrected enumeration (:1258) |
| conventions | F-3 | 2b invoked "before `:79`" | CLOSED | :558-567 |
| conventions | F-4 | "every row must be able to fail" falsified | CLOSED | `[guard]` marking rule (:1216-1219) and rows 12/14/16 |
| conventions | F-5 | Bare-tool fence misses `:99` | CLOSED | seven sites now enumerated (:520-521); the "inside an edit region" sentence still omits `:99`/D3 (P4, not raised) |
| conventions | F-6 | VHS-42 claims the `AGENTS.md:7` fix | CLOSED | § Deferred :1379-1382 requires `/ship-spec` to trim it |
| edge-cases | F-1 | Later round's marker leapfrogs a gap | PARTIAL | run-scoped `HARVEST_FLOOR`/`HANDLED_THROUGH` closes the *marker* path (:344-381); D6's in-run advance rule now contradicts itself — see F-4 |
| edge-cases | F-2 | `gh api --arg` invalid | CLOSED | :603-612, :977-981 |
| edge-cases | F-3 | Steps 6/7 circular | CLOSED | :663-670 |
| edge-cases | F-4 | Phrase tripwire reads a vanished body | CLOSED | :711-715 |
| edge-cases | F-5 | `LAST_BODY_REVIEW_ID` never seeded | CLOSED | Decision 2 :77-83; D1 :589-592; D5 counts post-dedup :885-888 |
| edge-cases | F-6 | Step 9 matches on raw text | CLOSED | "Masked for matching, raw for content" :698-709; step 9 restated :747-750 |
| edge-cases | F-7 | Rows 4/8 miscounted, row 8 unrunnable | CLOSED | fenced block + corrected rows; Pre column re-verified against `main` (4=0, 5=7, 6=3, 9=1/2, 11=1, 15=0/1 — all match) |
| edge-cases | F-8 | Fetches (a)/(c) ungoverned; `:83` unblocked | PARTIAL | Decision 14 first bullet (:472-482) and the `:81`/`:83`/`:381` clause (:499-509) land; but the prescribed exit-status shape does not actually surface a failure — see F-1 — and the enumeration of "every affirmative early exit" still omits two — see F-9 |
| edge-cases | F-9 | Empty `$SELF` silently resets the window | PARTIAL | Decision 14 second bullet (:483-488) covers the *capture-time* empty case; it does not cover `SELF` not surviving into the query's Bash call — see F-2 |
| edge-cases | F-10 | Marker laundering through titles | CLOSED | position rule (:418-419) + neutralization (:420-423); implemented in both queries |
| edge-cases | F-11 | Markerless comment unguarded | PARTIAL | `r0` emitted (:988-993) and Decision 2 reworded (:96-100); the guard now over-matches on `r0` — see F-3 |
| edge-cases | F-12 | Size threshold unstated | CLOSED | 64 KB, D2 step 3 (:640-645) |

## Findings

### F-1: The prescribed exit-status shape (`; rc=$?`) makes a failed fetch indistinguishable from a small one — and prints nothing at all

**Severity:** P1
**Where:** spec § Decision 7 (:215-219), § D1 fetch (c) (:553-555), § D5 inline poll (:865-869)
**Edge case:** any `--paginate` stream that dies mid-page — the exact PR #51 shape Decision 7 was written for.
**What happens:** the required block is

```bash
gh api --paginate <endpoint> --jq '<streaming filter>' > "$TMPDIR/new_inline"; rc=$?
COUNT=$(wc -l < "$TMPDIR/new_inline")
```

Run as one Bash call, the exit status of the list is the status of the *last* command — `rc=$?` is a simple assignment, which always returns 0. Verified in this environment: `false > /dev/null; rc=$?` reports list status `0` with `rc=1`. Worse, **nothing is printed**: the fetch is redirected, `rc=$?` assigns, and `COUNT=$(…)`/`NEW_INLINE=$(…)` assign. The agent sees empty stdout and exit 0 and has no value to read at all — so it must either invent a count or re-run. If it re-runs `wc -l` in a second Bash call, `rc` is gone (the file's own `:180` note: "Individual Bash tool calls do not share shell variables"), and a partial stream reads as a genuine smaller count. Combined with zero body items and a landed verdict that sets `REVIEW_SIGNAL=verdict-landed` and licenses "no new findings" — verbatim the failure Decision 7's own prose describes at :206-213.
**Why the spec misses it:** Decision 7 correctly diagnoses the *pipeline* form (`| wc -l` reports `wc`'s status) but its replacement moves the same swallow one command to the right. `rc` is referenced only in a comment (`# rc != 0 -> a harvest failure`), never emitted, and no site tells the agent how to observe it.
**Suggested fix:** make the failure and the count both visible in the block's stdout, e.g.

```bash
gh api --paginate <endpoint> --jq '<filter>' > "$SCRATCH/new_inline"
rc=$?
if [ "$rc" -ne 0 ]; then echo "HARVEST_FAILURE rc=$rc"; else echo "COUNT=$(wc -l < "$SCRATCH/new_inline")"; fi
```

and add a sentence to Decision 7: *"The fetch and its status check are one Bash invocation, and the block must print either `HARVEST_FAILURE rc=<n>` or `COUNT=<n>`. A block that prints neither is a harvest failure."* Apply at all three sites.

### F-2: `export SELF` is a shell variable, so `env.SELF` resolves to `null` if the query runs in a separate Bash call — silently resetting the resume window *and* disabling the guard

**Severity:** P1
**Where:** spec § D2 step 1 (:603-612), § D7 guard (:966-985), § Decision 14 second bullet (:483-488)
**Edge case:** the agent splits the fenced block across Bash tool calls — which the same file explicitly warns is the norm (`:180`, and "Poll by making **individual Bash tool calls**" at `:200`, `:316`).
**What happens:** `env.SELF` is unset in the second process, so gojq yields `null`; `select(.user.login == env.SELF)` matches nothing. The resume query returns no rows → `PRIOR_DISPOSITIONED_REVIEW_ID` falls to `0` → the run re-harvests and re-dispositions the PR's entire body history. The guard returns no rows → 6f posts a duplicate comment. Both silently, and both are precisely the harms edge-cases r3-F-9 was filed for.
**Why the spec misses it:** Decision 14's remedy checks `SELF` at *capture* time ("A non-zero exit *or an empty `SELF`* is a failure"). That check passes — `gh api user` succeeded and `SELF` was non-empty *in that process*. Nothing detects that the value failed to reach the query, and neither tripwire runs on the resume path (spec's own note at :410-411).
**Suggested fix:** two edits. (a) In D2 step 1 and D7, state that the login fetch and the query are **one Bash invocation**, and that the login is otherwise carried as conversational state and substituted **literally** into the filter (`select(.user.login == "<SELF>")`) — the pattern `:180` already establishes for `PUSH_TIME`/`PREV_REVIEW_ID`, and the reason `--arg` was wanted in the first place. (b) Make the null case self-detecting inside the program, e.g. prefix with `(env.SELF // "") as $s | if $s == "" then error("SELF unset — harvest failure") else . end |`, so an unset variable raises instead of matching nothing.

### F-3: `r0` is a constant key fed to an exact-match idempotency guard, so a later round's **disposition list** is silently suppressed

**Severity:** P1
**Where:** spec § Decision 12 (:356-361 monotone rule, :398-403 guard), § D7 (:959-964, :988-993)
**Edge case:** two or more rounds of one run compute `R = 0` while still triaging body-level findings — reachable whenever a `HARVEST_FLOOR` is set early in the run (a failed body fetch, a failed 6f post, or the 2b step 2 bound) and later rounds keep finding body items.
**What happens:** concretely — round 1 harvests `[100, 200]`, 200's fetch fails → `HARVEST_FLOOR=200`, `R=100`, posts `r100` with 100's dispositions. Round 2's 6a poll surfaces review 300 with real findings; `R` is capped strictly below 200 → `HANDLED_THROUGH=100` → monotone rule → posts with `r0`. Round 3 surfaces review 400 with findings; `R=0` again; the guard finds a comment whose last non-blank line is exactly `<!-- review-pr:body-dispositions:r0 -->` and **skips the post**. Round 3's triaged body findings get no disposition anywhere on the PR, and 6e's `dispositions posted in <comment-url>` points at round 2's comment, which does not contain them. That is the audit-trail hole the ticket exists to close, re-created by the fix for correctness r3-F-9.
**Why the spec misses it:** the spec's own edge case at :1183-1184 states the rule this violates — *"**Two all-skip rounds on one PR** — each posts its own comment keyed `r<R>`. A constant `no-push` key would have suppressed the second round's dispositions."* `r0` **is** a constant key. The guard's gloss ("A marker match means 'this exact harvest was already dispositioned'", :402-403) is true for `r<id>` and false for `r0`, which by construction identifies no harvest. The aggravating case is the findings-free post condition (:959-964): it is evaluated on the *computed* `R` ("`R` would advance past `PRIOR_MARK`") but posts the *monotone-capped* value, so a purely informational round can consume the single `r0` slot before a findings round needs it.
**Suggested fix:** scope the guard to markers that actually identify a harvest. In Decision 12's **Guard** paragraph: *"The guard applies only when `R > 0`. An `r0` comment claims no harvest, so it never suppresses a later post; instead, suppress an `r0` post only when an existing self-authored comment carries `r0` **and** an identical body. A duplicate `r0` progress note is acceptable; a suppressed disposition list is not."* Restate the same exemption in D7's guard block comment, and fix 6e's `dispositions posted in <comment-url>` to name the comment this round actually posted (or `not posted — <reason>`).

### F-4: D6's advance rule states two incompatible values for `LAST_BODY_REVIEW_ID`, and the primary one causes exactly the permanent in-run gap the same bullet forbids

**Severity:** P1
**Where:** spec § D6 (:921-930)
**Edge case:** a round whose harvest set interleaves success and failure — e.g. `[100 ok, 200 fetch-fails, 300 ok]`, routine once the 2b step 2 bound admits up to 10 reviews per round.
**What happens:** the bullet says *"set `LAST_BODY_REVIEW_ID` to the highest id **whose body was fetched and parsed successfully in this round**"* (→ 300) and, one sentence later, *"It must **not** advance past a review whose fetch failed — otherwise that review is never retried by a later 6a poll of the same run, and the gap becomes permanent"* (→ 100). Both cannot hold. Under the first reading, 6a's body-carrying query filters `id > 300`, review 200 is never retried, and its findings are skipped for the whole run — the outcome the second sentence declares unacceptable. Under the second reading, 6a re-returns 300 every poll, whose items dedup to zero, so the poll can never see anything new and simply exhausts to `inconclusive`. An implementer must guess, and the two guesses produce materially different runs.
**Why the spec misses it:** the fix for edge-cases r3-F-1 moved contiguity into the *posted marker* (`HARVEST_FLOOR`, Decision 12) and the bullet's own closing sentence draws the contrast — *"the two are not the same value when a fetch failed"* — which reads as sanctioning the leapfrog for the in-run mark while the preceding sentence forbids it. The cross-run recovery is sound (the marker stays below the floor), so only the in-run behavior is at stake, but the spec text prescribes both.
**Suggested fix:** replace the first sentence with the contiguous form and delete the contradiction: *"after triage, set `LAST_BODY_REVIEW_ID` to the highest id of the **contiguous successfully-parsed prefix** of this round's harvest set — i.e. the highest successfully parsed id that is strictly below the round's lowest failed or deferred id; leave it unchanged if nothing parsed or if the lowest id in the set failed."* Then keep the justification sentence as-is, and keep the closing contrast.

### F-5: The phrase tripwire scans the whole body, so an unfenced prose occurrence of either phrase fires a false alarm — most likely on the very PR that ships this change

**Severity:** P2
**Where:** spec § Decision 11 (:307-325), § D2 step 6 phrase-scan view (:711-715)
**Edge case:** the literal `outside diff range` or `nitpick comments` appears anywhere in the review body outside a fence or code span while that phrase's own section is absent — a CodeRabbit-authored finding title, a walkthrough-table summary row, or a changed-file description.
**What happens:** the detector fires, 6e prints `Body parse tripwire: phrase on review <id>`, and the operator is told that section's harvest is untrusted. On the PR that ships this change, CodeRabbit's walkthrough will describe the diff in its own prose ("adds parsing for Outside diff range comments and Nitpick comments sections") on a review whose body carries at most one of the two sections — firing the other phrase's tripwire on essentially every round. A tripwire that fires on a healthy body trains the operator to ignore it, which is the same silent blindness by another route.
**Why the spec misses it:** Decision 11's defense is scoped to *quotation of changed Markdown*, which fence-masking handles. It does not consider CodeRabbit's own unfenced prose about this file, and the phrase-scan view is deliberately **body-wide** with no exclusion for the successfully-parsed section spans or for the top-level AI-prompt / walkthrough blocks. Test row 19 (:1279-1285) checks a body containing "Outside diff comments" — which is not the pinned phrase — so it does not exercise this.
**Suggested fix:** narrow the scan target in Decision 11 and D2 step 6: *"The phrase scan runs only on lines of the phrase-scan view that contain `<summary>`, plus any line outside every matched section span. Text inside a section that parsed successfully, inside the top-level `🤖 Prompt for all review comments with AI agents` block, and inside the walkthrough table is excluded — the drift this detector exists to catch is a change to the section **summary line**, not a mention of the phrase in prose."* Add a test row: a synthetic body with a healthy Outside-diff section whose item title contains the words "nitpick comments" must fire no tripwire.

### F-6: An item whose `cr-comment` marker sits inside the nested `<details>` block truncates the item mid-block, leaving an unbalanced block whose strip is undefined

**Severity:** P2
**Where:** spec § D2 step 9 (:736-750), § Decision 9 (:264-270), § Decision 10 (:272-293)
**Edge case:** the case Decision 9 explicitly anticipates — *"so a marker that sits inside a nested block is still found"* (:267-269).
**What happens:** step 9 terminates the item body at *"the item's `<!-- cr-comment:v1:… -->` marker, whichever comes first"*. If the marker is inside the nested `🤖 Prompt for AI Agents` block, the item span ends mid-block, so the span contains an opening `<details><summary>🤖 Prompt for AI Agents</summary>` with no matching `</details>`. Decision 10's removal is specified as dropping *"every nested `<details>…</details>`"* — a pattern with no close does not match, so the block survives into the item body and reaches Step 3. Step 3 then reads reviewer-supplied imperative instructions where it expects a claim to verify, which is exactly the trust-boundary and correctness failure Decision 10's two load-bearing reasons name.
**Why the spec misses it:** Decision 9 asserts the marker may sit inside a nested block, and step 9 independently makes the marker a terminator; neither rule was checked against the other.
**Suggested fix:** two sentences in D2 step 9. *"The item body terminates at the marker only when the marker is at nesting depth 0 within the item; a marker found inside a nested `<details>` supplies the key but does not end the item."* And in Decision 10: *"An unmatched nested `<details>` is stripped from its opening tag to the end of the item span."*

### F-7: Step 7 seeds the depth walk at the line preceding the summary with no check that the line is actually the section's `<details>`

**Severity:** P2
**Where:** spec § D2 step 7 (:717-726)
**Edge case:** CodeRabbit emits `<details><summary>⚠️ Outside diff range comments (1)</summary>` on one line, inserts a blank line or an attribute between them, or nests the section inside an outer `<details>` whose open tag happens to be the preceding line. Note the spec's own synthetic test row 21 (:1292-1297) writes exactly the single-line form.
**What happens:** the walk starts on a line that is not the section's opener. Best case the preceding line is blank or `> [!CAUTION]` and the walk still meets the combined tag — it works by accident. Worst case the preceding line is the previous section's `</details>`, so depth goes negative and "end the section where depth returns to zero" terminates at the summary line: zero items parsed against a declared count of N. Or the preceding line is an *outer* `<details>`, and the walk runs past the true section end to the outer close — and because step 5's provisional span extends to EOF for the last harvested section, the file-group scan can spill into the `Duplicate comments` section, harvesting items Decision 1 says must never be read.
**Why the spec misses it:** step 7 treats "the `<details>` sits on the line immediately preceding its summary" as verified fact from two specimens (:718-720) and turns it into an unconditional seeding rule with no precondition test. The count tripwire catches the zero-items case loudly, but not the spill case.
**Suggested fix:** add to step 7: *"Before seeding, confirm the preceding line contains `<details>` and no `</details>`. If it does not, seed the walk at the summary line itself and fire the count tripwire for that section with reason `section opener not found on the preceding line`. If the walk reaches the end of the provisional span without depth returning to zero, end the section at the provisional-span boundary and fire the same tripwire — never let the scan continue past it."*

### F-8: "Last non-blank line" is computed with `. != ""` and compared with `==`, so a CRLF or whitespace-only trailing line defeats the guard

**Severity:** P2
**Where:** spec § D2 step 1 (:609-612), § D7 guard (:978-981), § Decision 12 (:341-342)
**Edge case:** the 6f body file is written with CRLF line endings (routine on this Windows host) or ends with a line containing whitespace.
**What happens:** `split("\n")` leaves a trailing `\r` on every line, and `map(select(. != ""))` does not treat `"\r"` as blank. The guard's test is exact string equality against `"<!-- review-pr:body-dispositions:r<R> -->"`, which fails against `"<!-- … -->\r"` → the guard matches nothing → 6f posts a duplicate comment on every re-run. If the file ends with a blank CRLF line, `last` returns `"\r"` and **both** queries miss the marker: the resume window silently resets to `0` and the run re-triages the PR's entire body history. The two queries also disagree by construction — the resume query uses `capture` (a regex search, tolerant of `\r`) while the guard uses `==` (intolerant) — so the failure is asymmetric and hard to diagnose.
**Why the spec misses it:** the marker's *position* rule was hardened for the laundering attack (edge-cases r3-F-10) without also hardening how "blank" and "equal" are computed, and the body file's line endings are never specified.
**Suggested fix:** normalize in both programs and specify the writer. In D2 step 1 and D7, replace the blank test with `map(select(test("\\S")))` and add `| sub("\\s+$";"")` before `capture`/`==`; state in D7 that `<BODY_FILE>` is written with **LF** line endings and no trailing whitespace. One sentence in Decision 12: *"'Last non-blank line' means the last line containing a non-whitespace character, compared after trailing whitespace is stripped."*

### F-9: Decision 14 claims to block "every affirmative early exit" but the fast path and 6a's `pre-existing-approval` are not covered

**Severity:** P2
**Where:** spec § Decision 14 (:499-509), § D4 fast-path predicate (:836-841), skill `:182`
**Edge case:** a body-harvest failure on a round that also has one or two fix-categorized inline findings, or on a PR whose latest verdict is already a post-push `APPROVED`.
**What happens:** the clause enumerates "All **three** Step 2 exits" (`:81`, `:83`, `:381`) and forbids `verdict-landed`. It does not touch `FAST_PATH`. With the harvest failed, the body findings from the unread review were never triaged, so `round1_finding_count` is computed over a knowingly partial population and "every round-1 finding is categorized as fix" is vacuously satisfiable — the predicate fires, 6a/6b are skipped entirely, and the round ends on `Fast path: yes`. Same for `:182`'s `pre-existing-approval`, which jumps straight to 6e. In both cases the harvest failure does appear on 6e's `Body harvest failures` line, so it is not fully silent — but the two most confident report lines the skill can print are reached on a round where a finding source did not answer.
**Why the spec misses it:** the clause was written against the `REVIEW_SIGNAL`-vs-Step-2 timing problem (edge-cases r2-F-2) and enumerated the three Step 2 sites; the fast path is evaluated later, after Step 5, and was not swept.
**Suggested fix:** widen the clause: *"A standing harvest failure also blocks `FAST_PATH` (its `round1_finding_count` is computed over a population known to be incomplete — take the full 6a wait instead) and 6a's `pre-existing-approval` short-circuit. `REVIEW_SIGNAL` becomes `inconclusive` in both cases, and 6e prints the harvest failure alongside it."* Add the fast path to the D9 edge-case bullet at :1137-1142.

### F-10: Test row 14 still cannot see the multi-line antipattern — which is the only shape this file writes

**Severity:** P2
**Where:** spec § Test plan row 14 (:1246, :1264)
**Edge case:** the pipe-into-aggregate antipattern written across a `\` continuation, e.g.

```bash
gh api --paginate repos/<OWNER>/<REPO>/pulls/<N>/comments \
  --jq '.[] | select(.user.login == "coderabbitai[bot]") | .id' \
  | wc -l
```

**What happens:** verified — `grep -cE 'gh api --paginate.*\| *(wc|jq)'` returns `1` on the single-line form and `0` on the three-line form above. Every `gh api` invocation in the current SKILL.md and in every block this spec adds uses `\` continuations, so the shape an implementer would actually write is invisible to the guard. Decision 7's most load-bearing rule remains effectively unpinned, which is what correctness r3-F-8 was filed for.
**Why the spec misses it:** row 14's note (:1264) fixes the bracket-expression bug the v3 draft had and stops there; "verified to catch the antipattern" was checked against a single-line specimen only.
**Suggested fix:** replace row 14 with a shape that survives continuations, e.g. a two-part guard — `grep -cE '^\s*\| *(wc|jq|head|tail|cut)' $S` expected `0` (a continuation line that opens with a pipe into an aggregate), retaining the existing single-line regex as a second `[guard]` row. Note in the row that grep is line-based and the pair is what covers both shapes.

### F-11: No test row discriminates the round-3 P1 fixes this round just made

**Severity:** P2
**Where:** spec § Test plan (:1223-1266), § Decision 12 (:344-396), § D7 (:1024-1033)
**Edge case:** an implementation that ships the body harvest but omits `HARVEST_FLOOR`, the monotone-`R` rule, or the findings-free comment.
**What happens:** every gate row passes. Row 10 (`grep -cF 'review-pr:body-dispositions:r' ≥ 3`) is satisfied by the resume query, the guard, and the disposition body alone — none of which requires run-scoped state to exist. Row 23 exercises a forced fetch failure but only asserts the *report* lines, not that the marker stayed below the gap. So the two most expensive fixes of this round have no discriminator, and a regression on either is invisible to the gate — the same class of hole rows 13 and 14 were added to close for the other two.
**Why the spec misses it:** the test plan was rewritten for the row-4/8/13/14 corrections; the new Decision 12 machinery is prose-only and was not given a pin.
**Suggested fix:** add three grep rows and one walkthrough. `grep -cF 'HARVEST_FLOOR' $S` → `≥ 2` (Pre `0`); `grep -cF 'body-dispositions:r0' $S` → `≥ 1` (Pre `0`); `grep -cF 'oldest' $S` → `≥ 1` (Pre `0`, pins the oldest-first bound Decision 12 depends on). And extend row 23: *"with review N's fetch forced to fail and review N+1 harvested cleanly in a later cycle, the posted marker must name an id strictly below N, and a findings-free comment must post when the round deferred or failed anything."*

### F-12: `$TMPDIR` is used in three code blocks but never established

**Severity:** P3
**Where:** spec § Decision 7 (:216-218), § D1 fetch (c) (:555), § D2 step 3 (:634-636), § D7 (:1000-1006)
**Edge case:** `TMPDIR` unset in the environment. D2 step 3 calls it *"the temp/scratch directory D7 establishes"*, but D7 only says *"the system temp directory (or the harness scratch directory)"* and never names or sets a variable. It happens to be `/tmp` in this Git Bash, but it is commonly unset on Windows shells that expose only `TMP`/`TEMP`.
**What happens:** `> "$TMPDIR/body-<id>.md"` becomes `> "/body-<id>.md"` — a write to the MSYS root that either fails (loud, the subsequent read errors) or silently litters. Not corrupting, but the failure surfaces as a confusing read error rather than a harvest failure.
**Suggested fix:** in D7, define it once: *"`SCRATCH="${TMPDIR:-${TMP:-/tmp}}"`, resolved in the same Bash invocation as each write since shell variables do not persist across calls; every block below uses `$SCRATCH`."* Then use `$SCRATCH` consistently in Decision 7, D1 (c), D2 step 3 and D5.

### F-13: D5's `verdict-landed` test is undefined when the verdict stream is empty

**Severity:** P3
**Where:** spec § D5 (:876-895)
**Edge case:** a PR on which every CodeRabbit review to date is `COMMENTED` — possible on a PR whose only reviews are reply acknowledgements plus body-carrying conversational posts.
**What happens:** *"the verdict stream's highest-id record satisfies `state != "COMMENTED"` …"* has no record to evaluate. The safe fall-through is `inconclusive`, but the spec does not say so; D1 handles the exactly analogous empty case for fetch (a) explicitly (:569-573) and D5 does not.
**Suggested fix:** one clause: *"An empty verdict stream is not `verdict-landed`; the round falls through to `inconclusive`."*

### F-14: Decision 9's "raw item span" now collides with D2 step 6's defined "raw view"

**Severity:** P3
**Where:** spec § Decision 9 (:266-269), § D2 step 6 (:696-709), § D2 step 9 (:747-750)
**Edge case:** a reader resolving where the `cr-comment` scan runs.
**What happens:** Decision 9 says the marker is extracted from the *"**raw** item span, **before** the nested-`<details>` strip"* — "raw" there is temporal (pre-strip). Step 6 then defines **raw** as a named view (blockquote-stripped, not code-masked) and lists *"the `cr-comment` marker scan"* among the operations that run on the **masked** view. The two uses of the word point at different objects. In practice both views agree for a marker outside a code fence, so nothing breaks today — but the "masked for matching, raw for content" rule is the load-bearing invariant of this round's rework, and an ambiguous "raw" in the decision that governs identity is exactly where a later editor will get it wrong.
**Suggested fix:** reword Decision 9 to *"extracted before the nested-`<details>` strip of Decision 10 (and, per 2b step 6, matched on the masked view)"*, dropping the word "raw".

### F-15: `HARVEST_FLOOR` is "recorded" at two sites with a set operation, not a minimum

**Severity:** P3
**Where:** spec § D2 step 2 (:625-626), § Decision 12 (:348-350, :395-396), § D2 step 3 (:637-638)
**Edge case:** one round both defers reviews at the bound *and* has a body fetch fail among the parsed prefix.
**What happens:** Decision 12 defines the floor correctly as *"the **lowest** review id this run left unhandled"*, but the three operational sites all say "record"/"sets `HARVEST_FLOOR` at that review's id" — a plain assignment. Applied in the order the procedure runs (step 2's bound first, step 3's fetch failures second), a later assignment from a *higher* failed id would raise the floor above a lower deferred id, letting `R` claim a deferred review as handled.
**Suggested fix:** make the operation explicit at each site: *"lower `HARVEST_FLOOR` to this id if it is unset or higher — the floor is a running minimum over the whole run, never an assignment."*

## Summary
P0: 0 | P1: 4 | P2: 7 | P3: 4 | P4: 0

STATUS: RED P0=0 P1=4 P2=7 P3=4 P4=0
