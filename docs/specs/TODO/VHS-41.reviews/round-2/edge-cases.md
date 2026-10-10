Grounding complete. I read the spec (1703 lines), the brief, `CLAUDE.md`, the current `skills/review-pr/SKILL.md`, all three round-1 reports, and retrieved the Plane ticket (VHS-41, tag-exact match, consistent with the brief). I verified every shell/jq claim I could against `gh` 2.87.3 in Git Bash and against the live PR #28 specimen.

# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Decision 2/D1 state a different advance rule than D6 | CLOSED | § Decision 2:77-84 and § D1:735-743 now both defer to D6 as the only statement |
| correctness | F-2 | Findings-free 6f has no Step 2 call site | CLOSED | § Decision 3:118-121, D1:723-733, D7:1169-1175, D9:1338-1345, row 22 |
| correctness | F-3 | Decision 2 carries the pre-digest marker literal | CLOSED | :58 now says "a `review-pr:body-dispositions` marker (Decision 12 gives the full shape)" |
| correctness | F-4 | Row 14 regex cannot match the multi-line fetch shape | CLOSED | Ran row 14 against all 13 prescribed blocks + D9 prose: `0`, and it *would* match a single-line antipattern |
| correctness | F-5 | Row 19 attributes body content to the wrong review id | CLOSED | Rows 23/25 corrected; verified `Outside diff comments:` is body line 67 of `5135914911`, not `5135878266` |
| correctness | F-6 | `$TMPDIR` never established | CLOSED | § D1:635-653 `<SCRATCH>`; ran `d="${TMPDIR:-/tmp}/…"` — resolves |
| correctness | F-7 | Guard byte-exact, web-UI edit breaks it | CLOSED | Ran the guard jq through gh: CRLF + whitespace-only tail → exact match `true` |
| correctness | F-8 | Quoted `gh api --arg` error string wrong | CLOSED | `gh api --jq --arg self x '…'` → "accepts 1 arg(s), received 3" as spec now states |
| edge-cases | F-1 | `$TMPDIR` aborts the fetch | CLOSED | § D1:642-653; all 19 `<SCRATCH>/` sites; row 20b measured `0` |
| edge-cases | F-2 | Digest interpolates title text into a shell string | CLOSED | § Decision 12:388-398 literal id list; `sha1sum` survives only in rejected-design prose |
| edge-cases | F-3 | 6f unreachable on the three Step 2 exits | CLOSED (call sites) | D7:1169-1175 — but the *condition* still cannot fire in a real case: new F-1 |
| edge-cases | F-4 | Persistent body failure pins the floor; "failed parse" undefined | **PARTIAL** | "Failed parse" now defined (:419-421); the 403 class is wrong and the taxonomy is not total — F-2, F-5 |
| edge-cases | F-5 | Token protocol covers 2 of ~13 governed fetches | **PARTIAL** | 13 blocks now carry it, but `gh api user` (D2 step 1:762-766) is Decision-14-governed and is not — F-4 |
| edge-cases | F-6 | Prescribed blocks carry spec-side annotations | CLOSED | Grepped all extracted blocks for `r<n>-F-<n>`, `a2r1-F`, `v<n> draft`, `Decision <n>`, `D<n>`, `env.SELF`, `export SELF`: none |
| edge-cases | F-7 | CRLF / whitespace-only trailing line defeats the guard | CLOSED | Verified through gh's jq engine (`e_exactmatch: true`, `g_tab_only_line: "a"`) |
| edge-cases | F-8 | Fixed-name temp files collide under tolerated concurrency | **PARTIAL** | Per-run name added, but `mkdir -p` on a pre-existing dir returns 0 silently (measured) — F-6 |
| edge-cases | F-9 | `sha1sum` absent on macOS | CLOSED | Digest removed entirely |
| edge-cases | F-10 | No rule for a path/line that no longer resolves | CLOSED | § D3:1008-1014 named outcome `already-fixed` / `file/line no longer present`; D9:1375-1378 |
| edge-cases | F-11 | 64 KB rule reports but does not bound | CLOSED | § 2b step 3:812-825 — 256 KB ceiling, slice procedure. Residual P3 on measurement (F-13) |
| edge-cases | F-12 | Within-round dedup specified two ways | CLOSED | § 2b step 10:935-939 + Decision 9:306-307, one rule |
| edge-cases | F-13 | Row 14 guard cannot see the antipattern | CLOSED | Measured `0` on the real shapes; the `-A2` window reaches the redirect line |
| edge-cases | F-14 | Decision 14 blocks three affirmative exits, misses two | CLOSED | § Decision 14:586-594 covers `verdict-landed` / `pre-existing-approval` / `fast-path` and all three Step 2 exits |
| edge-cases | F-15 | Resume mark compared as a jq string | CLOSED | `tonumber` present; verified through gh's jq (`b_capture: 500`, numeric) |
| edge-cases | F-16 | Phrase tripwire fires on an unfenced blockquote quotation | DEFERRED | § Deferred (P2+):1694-1702, with rationale (design change, not a clarification) — accepted |
| conventions | F-1 | Decision 2/D1 state the superseded advance rule | CLOSED | Same evidence as correctness F-1 |
| conventions | F-2 | `sha1sum` prescribed as a literal binary | CLOSED | Removed |
| conventions | F-3 | `$TMPDIR` hardcoded with no definition | CLOSED | § D1 `<SCRATCH>` |
| conventions | F-4 | § Deferred routes the VHS-42 edit to `/ship-spec` | CLOSED | :1689-1692 "an explicit operator step, not a `/ship-spec` step" |
| conventions | F-5 | Row pins `≥ 3` but names two sites | CLOSED | Row 17 pins `≥ 10` and enumerates twelve sites |
| conventions | F-6 | Decision 3 / 6e block describe behavior counterparts extended | CLOSED | Decision 3:112-114; 6e block:1312-1321 gains unfetchable + size rows |
| conventions | F-7 | Decision 2 tagged *(carried from brief)* | CLOSED | :53 now "*(carried from brief; the cross-run resume marker and the advance rule are spec-author)*" |
| conventions | F-8 | Bare-tool-name fence omits `:99` | CLOSED | Design preamble:616-621 names seven sites including `:99` |
| conventions | F-9 | Review archaeology has no spec-only fence | CLOSED | Design preamble:623-631 + rows 19/21 |
| conventions | F-10 | Checklist numbering non-contiguous | CLOSED | Rows 3–22 automated, 23–29 manual, contiguous |

## Findings

### F-1: A round whose only progress is an unfetchable review posts no marker, so that review is re-fetched forever — and test row 29(ii) is unreachable
**Severity:** P0
**Where:** spec § D7 "Post condition" (`:1177-1182`); § Decision 12 (`:411-421`); test row 29(ii) (`:1605-1612`)
**Edge case:** the harvest set above the mark contains a review whose per-review body fetch returns a non-retryable status (or whose body is over the 256 KB ceiling), and the round produces no body-level findings and no `HARVEST_FLOOR`.
**What happens:** silent non-progress. Trace: harvest set `{X}`, `X > PRIOR_MARK`. 2b step 3 gets a `404` → `X` is recorded **unfetchable**, which per Decision 12 "counts as handled for contiguity" and "does *not* set a floor". So `HANDLED_THROUGH = X`, `R = X > PRIOR_MARK`, and `HARVEST_FLOOR` is **unset**. D7's post condition is `(≥1 body finding) OR (R advances past PRIOR_MARK **AND** a HARVEST_FLOOR exists)` — both disjuncts are false. No 6f comment, no marker, `PRIOR_MARK` never moves. Every future run re-fetches the same permanently-dead review, re-404s, re-reports it, and re-posts nothing. Decision 12's promise that an unfetchable review "is not retried" holds only *within* a run; across runs it is retried on every single one, forever. The identical trap fires for the over-ceiling case (`:421`, `:1400-1402`), where each run also re-downloads a >256 KB body it has already decided not to parse.
**Why the spec misses it:** the post condition was written for the *bound/failure* case (§ Decision 12 "Progress does not depend on findings", `:460-466`), where a floor always exists by construction. The unfetchable class was introduced later (a2r1-F-4) specifically as a *non*-floor, and no one re-checked D7's predicate against it. The contradiction is visible in the spec's own gate: test row 29(ii) requires that on a `404` "the round's marker must still advance past that id (Decision 12)" — under D7 as written no comment posts at all, so no marker exists to advance. A spec that pins an expected outcome its own post condition cannot produce is internally inconsistent.
**Suggested fix:** extend D7's post condition to a third disjunct and restate it in Decision 12: post when the round triaged ≥1 body-level finding, **or** when `R` would advance past `PRIOR_MARK` **and** (a `HARVEST_FLOOR` exists **or** the round recorded ≥1 unfetchable review). Equivalently, state the rule positively: *post whenever `R` would advance past `PRIOR_MARK` and the round is not "everything above the mark parsed cleanly to zero with nothing left over"*. Add the unfetchable-only case to D9's edge cases so the reader sees which clause covers it.

### F-2: `403` is classified non-retryable, but GitHub returns `403` for rate limits and token/SSO problems — so a transient failure permanently strands every affected review
**Severity:** P1
**Where:** spec § Decision 12 `HARVEST_FLOOR` bullet (`:411-421`); § Decision 14 (`:591-594`); § D9 (`:1394-1399`); 2b step 3 (`:809-812`)
**Edge case:** the run trips GitHub's primary or secondary rate limit, or the token has lost org SSO authorization / a required scope, while fetching per-review bodies.
**What happens:** permanent, silent finding loss — the exact defect this ticket exists to remove. GitHub returns **403** (not only 429) for both primary and secondary rate limits, and for SSO/scope failures. Verified locally: `gh api repos/torvalds/linux/actions/secrets` → `rc=1`, stderr `gh: You must have repository read permissions… (HTTP 403)`. Under the rule as written every such review is recorded **unfetchable** → excluded from the floor → **counted as handled for contiguity** → `HANDLED_THROUGH` and therefore `R` advance past it → the marker names it → on the next run it is below `PRIOR_MARK` and is never harvested again. The operator fixes the token, re-runs, and the reviews are gone. Decision 12's own invariant — "no review id at or below a posted marker … failed a fetch" — is violated by the very rule that was added to satisfy it. Note the asymmetry: a `429` gets one retry then becomes a *floor* (recoverable), while the `403` GitHub emits for the same underlying condition is treated as terminal.
**Why the spec misses it:** the rationale at `:414-418` reasons only about "one deleted or permission-gated review", i.e. a status that is a permanent property of *that review*. It never considers that `403` is also a property of *the caller's current session*, in which case it applies to every review in the set at once and clears on the next run.
**Suggested fix:** move `403` out of the non-retryable list. Keep non-retryable = `404` / `410` / `451` (genuine per-resource permanence). For `403`, classify by the error text: a body matching the rate-limit / secondary-limit / SSO wording is **retryable** (floor); anything else may be treated as unfetchable. Simplest safe alternative, if that discrimination is judged too fragile for a prose skill: make `403` retryable unconditionally and let the floor lift (F-10) do the work. Also state the rule Decision 12 currently only implies: *a status that applies to more than one review in the same round is a session condition, not a per-review one — floor it.*

### F-3: The harvest-set bound's scope in 6a/6b is specified three incompatible ways; one reading collapses the round, the other loses findings
**Severity:** P1
**Where:** spec § 2b step 2 (`:789-799`); § D5 (`:1085-1088`); § D6 (`:1121-1122`); § Decision 6 (`:184-188`)
**Edge case:** a first run against a long-lived PR with more than 10 body-carrying reviews above the mark, where round 1 pushes a fix and therefore reaches 6a.
**What happens:** three statements disagree and each failure mode is real.
1. 2b step 2 bounds the set to the **10 oldest** and defers the rest — but then asserts "Reachable only on a first run against a long-lived PR", while its own parenthetical "(rounds 2+: `id > LAST_BODY_REVIEW_ID`)" makes it a per-round rule.
2. D5 says: "For each review id **the body-carrying query returns**, run the 2b parse once … and count its items after dedup." After Step 2's bound, `LAST_BODY_REVIEW_ID` sits at the 10th-oldest id, so that query returns **all** the deferred reviews. Taken literally, 6a fetches and parses every remaining body — up to 256 KB each — inside a poll, purely to compute `new_body_items`. That is precisely the "exhausting the round mid-triage" that Decision 6 says the bounds exist to prevent, and it happens with no bound message, no report line, and no ceiling.
3. D6 says body findings come from "the 2b parse of **every** body-carrying review with `id > LAST_BODY_REVIEW_ID`", then sets the mark to "the contiguous successfully-parsed prefix of **this round's harvest set**". If 6a parsed 50 for counting and 6b's bound triaged 10, "successfully parsed" and "triaged" diverge, and the mark advances past 40 reviews whose items were counted but never triaged, never dispositioned, and never posted — findings silently dropped, with `HANDLED_THROUGH` claiming them.
**Why the spec misses it:** the bound was designed as a Step 2 property (Decision 6 lists it under "Three bounds are added" alongside the body-size and per-round-item bounds, both of which *are* stated inside 2b's per-body procedure). 6a/6b were written against "every … above the mark" from an earlier draft and never reconciled. Reading 3's mark divergence is invisible unless you notice that D6's "parsed" and 2b step 11's "triaged" are different populations.
**Suggested fix:** state once, in 2b step 2, that the bound applies to **every** invocation of 2b — Step 2's, 6a's counting pass, and 6b's triage pass — and strike "Reachable only on a first run". In D5, replace "for each review id the body-carrying query returns" with "for each review id in the round's **bounded** harvest set (2b step 2); reviews the bound deferred are reported by 2b step 2 and are not parsed for the count". In D6, replace "every body-carrying review with `id > LAST_BODY_REVIEW_ID`" with "the round's bounded harvest set", and define "successfully-parsed prefix" as *parsed **and** triaged*, so the mark can never pass a review whose items reached no disposition.

### F-4: `gh api user` is Decision-14-governed but is prescribed outside the capture-and-token shape, and Decision 7's blanket rule then reads every successful run as a harvest failure
**Severity:** P1
**Where:** spec § D2 step 1 block (`:762-766`); § Decision 7 (`:230-241`); § Decision 14 (`:571-579`); test row 17 (`:1552`)
**Edge case:** any run at all — this fires on the happy path.
**What happens:** a self-contradicting rule with no safe reading. Decision 14 states flatly that "`gh api user` is a harvest fetch too" and that a non-zero exit *or an empty `SELF`* is a failure. Decision 7 states, with equal force, "**Every fetch Decision 14 governs is issued in this shape, as its own Bash call**" and "**the block prints exactly one of `HARVEST_FAILURE rc=<n>` or `COUNT=<n>`. A block that prints neither is a harvest failure**". D2 step 1's prescribed block is a bare `gh api user --jq .login` — no redirect, no `rc=$?`, no `if`, and it prints neither token. An implementer applying Decision 7's rule literally classifies **every** run's login resolution as a harvest failure; Decision 14 then forbids `verdict-landed`, `pre-existing-approval`, `fast-path`, and all three Step 2 affirmative exits, so the skill can never report anything but `inconclusive`. An implementer who instead exempts it has silently reintroduced the inferred-failure mode Decision 7 was written to eliminate: on failure the block emits nothing on stdout and the agent must *infer* the failure from an absence.
**Why the spec misses it:** the a2r1-F-5 fix converted the fetches enumerated in test row 17 (twelve sites), and row 17's list does not include `gh api user`. Decision 14's "harvest fetch too" bullet and Decision 7's universal quantifier were both strengthened afterwards without re-walking D2 step 1's block. The two grep rows that would have caught it (17, and the `<SCRATCH>` count in row 20) both use `≥`, so the missing site cannot fail either.
**Suggested fix:** put D2 step 1's login fetch in the same shape as every other governed fetch — `gh api user --jq .login > "<SCRATCH>/self"` / `rc=$?` / print `HARVEST_FAILURE rc=<n>` on non-zero, `COUNT=<n>` otherwise — and add "a `COUNT=0` here is an empty login and is a harvest failure" to the block's comment. Then add it as the thirteenth site in row 17's enumeration. Alternatively, if the block is to stay bare, Decision 7 must carve it out explicitly ("the login fetch is the one governed fetch outside this shape, because its value is its own stdout") — but the shape is cheaper than the exception.

### F-5: The HTTP status the whole floor/unfetchable split depends on is never produced by the prescribed block, and the taxonomy is not total
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § 2b step 3 (`:801-812`); § Decision 12 (`:411-421`); § 6e report line (`:1315-1316`)
**Edge case:** any failed per-review body fetch.
**What happens:** the classification input is missing at the point of decision. Measured against the spec's exact block:

```
gh api repos/…/reviews/999999999 --jq '.body' > /tmp/body-999.md 2>/tmp/err404.txt
rc=$?  →  HARVEST_FAILURE rc=1
stderr →  gh: Not Found (HTTP 404)
stdout →  {"message":"Not Found","documentation_url":"…    ← the error body lands in body-999.md
```

`rc` is `1` for `404`, `403` (verified above) and, by the same code path, `5xx` — so `HARVEST_FAILURE rc=1`, the only value the block prints, cannot distinguish retryable from non-retryable. The code appears **only on stderr**, which the block neither redirects nor echoes, and 6e's report line asks for exactly that code. Decision 7's whole point is that "the failure is a printed value, never an inferred one"; here the value that decides whether a review is floored or permanently written off is inferred from unstructured stderr. Two secondary effects: the error JSON is written into `<SCRATCH>/body-<ID>.md`, so a cached-parse path that skips the `rc` check parses GitHub's error object as a review body (zero items, no tripwire); and the taxonomy is not total — `401`, `422` (which D9:1388 names as a failure without classing it), and anything else fall into neither list, so the implementer guesses, and one guess loses findings permanently (F-2) while the other pins the run.
**Why the spec misses it:** `:810` asserts "the `gh` error text carries the code" — true, but the block's contract is "prints exactly one of `HARVEST_FAILURE rc=<n>` or `COUNT=<n>`", and the error text is neither of those. The gap sits exactly between the two sentences.
**Suggested fix:** make the status a printed value. Either capture stderr in the same call and echo it — `gh api … > "<SCRATCH>/body-<ID>.md" 2> "<SCRATCH>/err-<ID>"; rc=$?; if [ "$rc" -ne 0 ]; then echo "HARVEST_FAILURE rc=$rc $(cat "<SCRATCH>/err-<ID>")"; …` — or use `gh api --silent -i` style status capture. Then state the taxonomy as **total**: name the non-retryable set explicitly and add "every other status, and every unrecognized error, is **retryable**" as the default. A retryable default is the safe side: it costs a re-run, whereas an unfetchable default costs the findings.

### F-6: `mkdir -p` on a pre-existing `<SCRATCH>` succeeds silently, so the collision the per-run name is meant to prevent is undetectable — and one run's 6e deletes the other's captures
**Severity:** P2
**Where:** spec § D1 (`:642-653`); § D8 6e (`:1327`); § Decision 12 *Race* (`:511-513`)
**Edge case:** two `/review-pr` runs on the same PR started in the same wall-clock second — the concurrency Decision 12 explicitly tolerates.
**What happens:** shared state, then destruction. Measured:

```
d="${TMPDIR:-/tmp}/review-pr-28-$(date +%s)"; mkdir -p "$d" && echo "SCRATCH=$d"
→ SCRATCH=/tmp/review-pr-28-1788861017      (first run)
→ SCRATCH=/tmp/review-pr-28-1788861017      (second run, rc=0, no warning)
```

`mkdir -p` is idempotent by definition, so both runs print a well-formed `SCRATCH=` line and proceed into the same directory. They then overwrite each other's `verdicts`, `body-<ID>.md`, `new-inline`, `guard-hits`, and `6f-body.md` — the exact half-written-file counting the spec claims the name prevents (`:651-653`). Worse, whichever run reaches 6e first executes `rm -rf "<SCRATCH>"`, deleting the other run's captured streams mid-flight; the survivor's next read of `<SCRATCH>/…` fails, and under the `wc -l < file` shape that surfaces as a `HARVEST_FAILURE` pointing at GitHub — the same misattribution D1 warns about for the `$TMPDIR` case.
**Why the spec misses it:** the fix for round-1 F-8 added uniqueness to the *name* and stopped there; nobody asked whether the create step *detects* a name that is already taken. `-p` is exactly the flag that suppresses that detection.
**Suggested fix:** create the directory in a way that fails on collision. Either `d="${TMPDIR:-/tmp}/review-pr-<N>-$(date +%s)-$$"; mkdir "$d" && echo "SCRATCH=$d"` (no `-p`, so a collision prints nothing and the existing "no `SCRATCH=` line → stop" rule fires), or use `d=$(mktemp -d "${TMPDIR:-/tmp}/review-pr-<N>-XXXXXX") && echo "SCRATCH=$d"`, which is collision-free by construction. State in D1 that the create must fail, not succeed, on a pre-existing directory.

### F-7: `<SCRATCH>` is never removed on the four early-exit paths — every approved-PR run leaks a directory
**Severity:** P2
**Where:** spec § D1 (`:653`); § D8 6e (`:1327`); the exits at `SKILL.md:79`, `:81`, `:83`, `:381`
**Edge case:** the ordinary exits — infrastructure error, `APPROVED` short-circuit, no reviews found, nothing to review.
**What happens:** unbounded accumulation of scratch directories. The scratch directory is created at the *top* of Step 2, before any of the exits, and the only cleanup site is 6e's `rm -rf "<SCRATCH>"`. But `:79` "report … and stop", `:81` "report 'Nothing to review — PR is approved' and stop", `:83` "report 'No CodeRabbit reviews found' and stop", and D9's rewritten `:381` "report 'Nothing to review' and exit" all terminate the run without reaching 6e. Re-running `/review-pr` against an already-approved PR is the single most common invocation of this skill, and it now leaves `/tmp/review-pr-<N>-<epoch>/` behind — containing `verdicts`, `body-reviews`, `inline-findings`, every fetched review body (up to 256 KB each), and possibly `6f-body.md` — on every invocation, forever.
**Why the spec misses it:** cleanup was attached to the report step because that is where the run "ends" in the happy path; the spec's own D1 order line (`:696-697`) shows the exits sitting between directory creation and any later step, but the cleanup sentence was written in D8 and never cross-checked against them.
**Suggested fix:** state the cleanup as a run-level obligation rather than a 6e step: in D1, "the directory is removed on **every** exit path — 6e's last act on the normal path, and immediately before each of Step 2's exits (`:79`, `:81`, `:83`) and `:381`'s". Give `:81` and `:381` the ordering explicitly, since both may post a 6f comment from `<SCRATCH>/6f-body.md` first.

### F-8: The phrase-scan view is defined inside a per-section step, but the phrase tripwire's trigger is "no section matched" — nesting it in the loop makes the detector unreachable again
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § 2b step 6 (`:856`, `:891-895`); § Decision 11 (`:344-362`)
**Edge case:** CodeRabbit changes the `<summary>` format so neither section pattern matches — the exact drift the tripwire exists to catch.
**What happens:** the drift detector silently never runs, which is round-1 F-3 reintroduced by placement rather than by logic. 2b step 6 is titled "**Normalize PER SECTION, over its provisional span**" and its body is written as a per-section procedure ("So, for each section's provisional span: a. … b. …"). The phrase-scan view is the last paragraph of that same step ("Additionally compute the phrase-scan view … a **body-wide** copy"). An implementer writing `for each located section: <step 6>` — the reading the step's own title invites — never executes that paragraph when zero sections were located, which is precisely the condition under which the phrase tripwire is supposed to fire. The result is the failure Decision 11 names in its closing line: "a CodeRabbit format change degrades straight back to the silent blindness this ticket exists to remove." Test row 27(ii) is the only thing that would catch it, and it is in the manual, network/synthetic-input tier — not the automated gate.
**Why the spec misses it:** the phrase-scan view was added (r3-F-4/r3-F-6) to fix an input-definition problem, and it was appended to the step where the other normalized views are defined rather than given its own step. The prose says "body-wide", but the surrounding structure says "per section", and structure wins when someone implements a numbered procedure.
**Suggested fix:** promote it to its own numbered step, before or after 6, e.g. "**6b. Compute the phrase-scan view (body-wide, once per review body, unconditionally — including when step 5 located no section).**" Add the unconditional clause in words, since that is the whole point. Renumber steps 7–12 accordingly, and update Decision 11's pointer from "defined in 2b step 6" to the new number.

### F-9: `h<IDS>` has two contradictory definitions — "the round's harvest-set review ids" versus "capped at 10 by 2b step 2's bound"
**Severity:** P2
**Where:** spec § Decision 12 (`:380-382`, `:394`); § 2b step 2 (`:789-794`); § D7 (`:1218-1224`)
**Edge case:** a first run against a PR with more than 10 unhandled body-carrying reviews — the only case where the bound fires, and therefore the only case where the two definitions differ.
**What happens:** the guard's key is undefined, and the two readings produce opposite behavior. 2b step 2 defines "**The set** is every review … with `id > PRIOR_DISPOSITIONED_REVIEW_ID` … If it exceeds **10** reviews, parse the **10 oldest**" — so "the set" is the full unhandled list (say 25) and only ten of it are parsed. Decision 12 then says `h<IDS>` is "**the round's harvest-set review ids**, ascending" *and* that "2b step 2's bound caps it at 10 ids per round". Both cannot hold. Under the 25-id reading, a new CodeRabbit review arriving between two otherwise identical runs changes `h<IDS>`, so the guard does not match and the run posts a second comment carrying the identical disposition list — duplicate audit entries on the PR, which is what the guard exists to prevent. Under the 10-id reading the guard suppresses correctly. The marker line length also differs by an order of magnitude on a mature PR.
**Why the spec misses it:** "harvest set" is used loosely for both the candidate list and the parsed prefix throughout 2b and D7 (D7's "A review recorded unfetchable this round is in the list — it was part of the harvest" is consistent with either). Decision 12's cap sentence was written assuming the tighter meaning and never reconciled with step 2's wording.
**Suggested fix:** pick the parsed prefix and name it distinctly. In 2b step 2, rename: "the **candidate set** is every review …; the round's **harvest set** is the 10 oldest candidates (all of them when there are ≤ 10); the remainder are **deferred**." Then `h<IDS>` = the harvest set, the 10-id cap is true by construction, and D7's unfetchable sentence stays correct (an unfetchable review is in the harvest set, having been attempted).

### F-10: `HARVEST_FLOOR` has no rule for being lifted, so a bound set in round 1 caps every later round's marker even after those reviews are handled
**Severity:** P2
**Where:** spec § Decision 12 (`:405-421`, `:427-433`, `:454-457`, `:467-468`)
**Edge case:** a run where round 1's harvest is bounded (floor = the lowest deferred id) and a later round of the *same run* successfully harvests and dispositions those deferred reviews.
**What happens:** work is done, dispositions are posted, and then discarded. Round 1 defers ids ≥ `F` and sets `HARVEST_FLOOR = F`. Round 2 harvests `F … F+9`, triages them, and posts a 6f comment listing every disposition. But `R = HANDLED_THROUGH` "capped **strictly below** `HARVEST_FLOOR` when a floor exists", and no rule anywhere raises or clears the floor once set — Decision 12 states the opposite ("once 300 fails, no marker in that run may name anything ≥ 300"). So round 2's marker still claims only round 1's prefix. On the next run those ten reviews are below no marker, get re-harvested, re-triaged, and re-dispositioned into a **second** comment with the same content, and the guard cannot suppress it because `R` differs. Net: the run converges one batch per run instead of one batch per round, and each converged batch leaves a duplicate disposition comment on the PR.
**Why the spec misses it:** the floor was designed for the *failure* case (r3-F-1's leapfrog example), where the floored review genuinely stays unhandled for the life of the run. The bound case was folded into the same variable later ("a review deferred by 2b step 2's bound") without noticing that a deferred review is the one floor cause that a later round of the same run routinely *does* clear.
**Suggested fix:** distinguish the two causes. Keep the floor sticky for failures (fetch/parse failure, failed 6f post — those are what the leapfrog rule protects), and make the bound's floor **provisional**: recompute it at the end of each round as "the lowest id still unhandled at this moment", so a round that handles the previously-deferred reviews raises it. State the invariant in the form that actually matters — *no marker may name an id at or above the lowest id this run has left unhandled **as of the post*** — which is stable under both causes and needs no separate lift rule.

### F-11: "Blockquote depth is constant within a provisional span" is false on the live specimen, and step 6a's "strip exactly that many" is then undefined
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § 2b step 5 (`:843-850`); § 2b step 6a (`:866-868`)
**Edge case:** the last (or only) section in a body, whose provisional span runs to end-of-body and therefore swallows CodeRabbit's top-level `🤖 Prompt for all review comments with AI agents` block.
**What happens:** the stated invariant does not hold, and the strip rule has no defined behavior for the lines where it fails. Verified against PR #28 review `5135914911` (fetched live): the Outside-diff section's `<details>` is body line 8 and it is the only section, so its provisional span is lines 8→127. Depth is 1 through line 46 (`> </blockquote></details>`) and **0** from line 47 onward — lines 48-127 carry no `>` at all. So a span with a genuinely varying depth exists in the very specimen the spec uses as its worked example, and the justification offered at `:849-850` — "because a section summary is exactly where depth changes" — is wrong: depth also changes where a section *ends*, and the last section's provisional span always extends past that point. Step 6a then says "strip **exactly** that many leading `>` markers … from every line in the span", which has no defined result on a line with zero of them. Today the damage is contained because step 7's depth walk narrows the section to lines 8-46 before anything is sliced, so the mangled tail is never read as content — but the containment is accidental, and an implementer who trusts the stated invariant (computing the strip once and applying it blindly, or treating a short line as a parse failure) has no warning.
**Why the spec misses it:** the invariant was asserted to justify hoisting the depth read out of the per-line loop; it was checked against the *section* (where it is true) rather than against the *provisional span* (where it is not).
**Suggested fix:** two words and a sentence. Change 6a to "strip **up to** that many leading `>` markers (each with at most one following space) from every line in the span; a line with fewer is left as-is." Replace the justification at `:849-850` with the true statement: "Depth is constant within the *true* section; a provisional span may extend past the section's close into lower-depth text, which step 7 discards — the strip must therefore tolerate lines shallower than the section depth."

### F-12: The `429` `Retry-After` rule is unimplementable in the prescribed capture shape
**Severity:** P3
**Where:** spec § Decision 14 (`:580`); § D7 "Error handling" (`:1273-1276`)
**Edge case:** GitHub rate-limits a harvest fetch and returns `Retry-After`.
**What happens:** the wait duration is unavailable. `Retry-After` is a response *header*; `gh api` prints no headers unless `-i`/`--include` is passed, and `--include` would prepend the header block to stdout — which the prescribed shape redirects straight into the capture file, corrupting it for the parse and for `wc -l`. So "wait the indicated duration and retry once" has no source for "the indicated duration" on any of the twelve governed fetches. The 6c rule it mirrors (`:279`) has the same shape but no redirect, so it was at least readable there.
**Why the spec misses it:** the rule was carried over verbatim from 6c's reply-error handling without re-checking it against the new redirect-to-file shape.
**Suggested fix:** either drop the header dependence — "on `429`, wait ~60 s and retry once" — or prescribe the header capture explicitly for the retry path only (`gh api -i … 2>&1 | …` in a separate diagnostic call that does not write the capture file). State which, so the implementer does not invent `--include` into the capture block.

### F-13: No prescribed way to measure a body's byte size for the 64 KB / 256 KB thresholds
**Severity:** P3
**Where:** spec § 2b step 3 (`:812-825`); § D8 6e size row (`:1317`)
**Edge case:** any body large enough to matter.
**What happens:** the two thresholds are stated in KB but the block prints only `COUNT=<n>` — a **line** count. The agent has no prescribed command producing the byte figure the branch tests and that 6e's `review <id> body <n> KB` line reports, so it must invent a second call, which the "the fetch and its status check are one Bash invocation" discipline does not anticipate.
**Why the spec misses it:** the thresholds were added as numbers (r3-F-12 asked for concrete bounds) without adding the measurement.
**Suggested fix:** have the block print both: `else echo "COUNT=$(wc -l < "$f") BYTES=$(wc -c < "$f")"; fi` for the per-review body fetch only, and note in Decision 7 that the body fetch's token carries the extra field.

### F-14: `<SCRATCH>` has no re-derivation rule, unlike every other piece of conversational state
**Severity:** P3
**Where:** spec § D1 (`:635-641`); § 2b step 4 (`:827-832`)
**Edge case:** a context compaction or a long poll sequence between Step 2 and 6b — the same condition 2b step 4 explicitly plans for.
**What happens:** 2b step 4 says the parse cache "is an optimization only … re-read that file and re-parse", and D5 says `PUSH_TIME`/`PREV_REVIEW_ID`/`LAST_BODY_REVIEW_ID` are conversational state "carried the way `:180` already describes". `<SCRATCH>` is neither re-derivable nor recoverable: re-running D1's line yields a **new** directory (different `date +%s`), so the recovery path silently orphans every capture and every fetched body written under the first one, and 6e's single `rm -rf` cleans only the second. The re-parse fallback 2b step 4 promises then fails, because the file it wants to re-read is under the lost path.
**Why the spec misses it:** `<SCRATCH>` was introduced as a substituted literal like `<SELF>`, but unlike `<SELF>` it cannot be re-derived by re-running its resolving command.
**Suggested fix:** name the recovery: "If `<SCRATCH>` is lost, do **not** re-run the resolve line — locate the run's directory with `ls -d "${TMPDIR:-/tmp}"/review-pr-<N>-*` and take the newest; if none exists, treat it as a harvest failure and end the run `inconclusive`." One sentence in D1.

### F-15: 6f's post is the only write in the design outside any observability shape, and the comment URL 6e reports is never captured
**Severity:** P3
**Where:** spec § D7 (`:1206-1210`, `:1273-1276`); § D8 6e (`:1313`, `:1328-1332`)
**Edge case:** a 6f post that fails, or a 6e report that must name `<comment-url>`.
**What happens:** `gh pr comment <N> --body-file "<SCRATCH>/6f-body.md"` is issued bare — no `rc` capture, no printed token — while the immediately preceding guard fetch is in the full capture-and-token shape. Yet the post's outcome is the most consequential value in the design: per Decision 12 a failed post floors the run and suppresses the marker on every later round. Separately, 6e's line requires `<comment-url>` "naming the comment **this round** posted", and `gh pr comment` prints that URL on stdout — which nothing captures, so the report line has no source.
**Why the spec misses it:** Decision 7's shape was framed around *fetches* ("Every fetch Decision 14 governs"), and the post is a write, so it fell outside the quantifier even though its outcome drives the floor.
**Suggested fix:** give the post the same treatment — `gh pr comment <N> --body-file "<SCRATCH>/6f-body.md" > "<SCRATCH>/6f-url"; rc=$?; if [ "$rc" -ne 0 ]; then echo "POST_FAILURE rc=$rc"; else echo "POSTED=$(cat "<SCRATCH>/6f-url")"; fi` — which supplies both the floor trigger and 6e's `<comment-url>` as printed values.

## Summary
P0: 1 | P1: 3 | P2: 7 | P3: 4 | P4: 0

STATUS: RED P0=1 P1=3 P2=7 P3=4 P4=0
