Verification complete. Findings below.

# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | 2b step 3's slice starts at `<summary>` | CLOSED | spec § D2 step 3 (`:921-924`): "from the `<details>` line preceding each `<summary>`… step 7's depth walk must begin on that `<details>` line" |
| correctness | F-2 | Row 23's phrase claim vacuous | CLOSED | row 23 (`:1711-1713`) restated; row 27(iii) (`:1746-1748`) is the real negative-mask discriminator |
| correctness | F-3 | Guard-key rationale false; floor latch/predicate ambiguity | CLOSED | Decision 12 (`:415-421`) new rationale; floor "recomputed at every post" (`:431-437`); latch wording replaced by "while 300 remains unhandled" (`:497-500`) |
| correctness | F-4 | D6 "same block as D5's inline poll" | CLOSED | D6 (`:1236-1242`) "its existing per-item `--jq` … unchanged — not D5's `.id`-only program"; row 17 (`:1696`) "not mergeable" |
| correctness | F-5 | Row 14's `-A2` cannot see the 5-line shape | CLOSED | row 14 now `-A5` (`:1669`, `:1693`). Verified: `0` on the exact 5-line block, `1` on a 6-line antipattern |
| correctness | F-6 | Scratch cleanup unreachable from early exits | CLOSED | D1 (`:721-730`) "removed on every exit path", naming `:79`, `:81`, `:83`, `:381` |
| edge-cases | F-1 | Unfetchable-only round posts no marker | CLOSED | D7 post condition third arm (`:1302-1312`); Decision 12 (`:511-519`); D9 (`:1540-1543`); row 29(ii) |
| edge-cases | F-2 | `403` non-retryable strands rate-limited reviews | CLOSED (residue → new F-3) | Decision 12 (`:439-456`): retryable is the default; non-retryable is exactly `404`/`410`/`451` |
| edge-cases | F-3 | Harvest-set bound scoped three ways | CLOSED | 2b step 2 candidate/harvest split (`:878-896`); D5 (`:1201-1203`); D6 advance rule "parsed *and* triaged" (`:1246-1252`) |
| edge-cases | F-4 | `gh api user` outside the capture shape | CLOSED | D2 step 1 block (`:853-855`); Decision 7 (`:250-251`); row 17 thirteen sites |
| edge-cases | F-5 | HTTP status never printed; taxonomy not total | CLOSED | every block carries `2> …err` + `$(cat …err)`. Verified live: `HARVEST_FAILURE rc=1 gh: Not Found (HTTP 404)`; retryable default (`:439-448`) |
| edge-cases | F-6 | `mkdir -p` hides a collision | CLOSED | D1 (`:702`, `:709-716`). Verified: second `mkdir` → rc=1, no `SCRATCH=` line |
| edge-cases | F-7 | `<SCRATCH>` leaked on early exits | CLOSED | D1 (`:721-730`) |
| edge-cases | F-8 | Phrase-scan view nested in the per-section loop | CLOSED | 2b step 6 (`:963-975`) "before and regardless of the per-section work below — including when step 5 located no section"; row 27(iv) |
| edge-cases | F-9 | `h<IDS>` two definitions | CLOSED | candidate/harvest split (`:878-884`); Decision 12 (`:412-415`) "at most 10 ids" |
| edge-cases | F-10 | Floor never lifted | CLOSED | Decision 12 (`:431-437`) recompute-at-every-post; failed-post cause sticky by construction |
| edge-cases | F-11 | "Depth constant in a provisional span" false | CLOSED | 2b step 5 (`:952-957`) with the line-47 evidence; step 6a "strip **up to** that many" (`:988-990`) |
| edge-cases | F-12 | `Retry-After` unimplementable | CLOSED | Decision 14 (`:633-636`) fixed 60 s; D7 (`:1406-1408`) |
| edge-cases | F-13 | No byte measurement for the KB thresholds | CLOSED | 2b step 3 block prints `BYTES=` (`:903`); Decision 7 (`:258-261`) |
| edge-cases | F-14 | `<SCRATCH>` has no re-derivation rule | CLOSED (new variant → F-6 below) | D1 (`:732-739`) |
| edge-cases | F-15 | 6f's post outside any observability shape | CLOSED (ungated → F-7 below) | D7 (`:1340-1342`) `POSTED=` / `POST_FAILURE rc=` |
| conventions | F-1 | `Decision <n>` / `D<n>` vocabulary ships | CLOSED | Design preamble (`:678-690`); row 21 alternation now includes `\bDecision [0-9]\|\bD[0-9]+\b`, Pre verified `0` |
| conventions | F-2 | `rm -rf` / `date +%s` without precedent | CLOSED | D1 (`:717-719`, `:726-728`) capability phrasing + recorded choice |
| conventions | F-3 | Block repeated verbatim, no reason given | CLOSED | Decision 7 (`:252-256`) |
| conventions | F-4 | § Deferred bullet departs from its own rule | CLOSED | `:1856-1859` "fenced in every observed specimen … the trigger is remote" |
| conventions | F-5 | Row 14 pipe-follower enumeration | CLOSED | row 14 (`:1693`) states the property, not a list |

## Findings

### F-1: `test("\\S")` reaches `gh` as `test("\S")` and aborts both new comment queries before any request
**Severity:** P1
**Where:** spec `:863` (§ D2 step 1, resume query) and `:1330` (§ D7, idempotency guard) — the only two double-backslash sites in the spec
**Edge case:** every run. The two queries are issued as Bash tool calls; a `\\` typed into a tool-call `command` is collapsed to a single `\` by JSON transport before the shell sees it (shell quoting cannot restore it — the loss is upstream of the shell).
**What happens:** hard failure on the happy path, on every invocation. Verified against gh 2.87.3, Git Bash:

```
$ gh api --paginate repos/…/issues/28/comments --jq '… map(select(test("\\S"))) …'
failed to parse jq expression (line 2, column 80)
  … map(select(test("\S"))) …
                      ^  invalid escape sequence "\S" in string literal
rc=1
```

`printf '%s' 'test("\\S")' | od -c` → `t e s t ( " \ S " )` confirms the collapse; single-backslash `\r` and `\n` survive intact, so only these two sites are affected. Rebuilt with genuine double backslashes the same query returns `rc=0` — the jq is right, the delivery is not. Consequences chain: the **resume query** failing is a harvest failure, so Decision 14 blocks all three Step 2 affirmative exits (`:81`, `:83`, `:381`) and pins `REVIEW_SIGNAL=inconclusive` on every run; the **6f guard** failing "fails closed", so no disposition comment ever posts, no marker ever lands, `PRIOR_MARK` stays `0` forever, and Done-when 1 ("produces a triage row **and a posted disposition**") is unreachable.
**Why the spec misses it:** the spec has twice rejected a prescribed command that aborts before any request — `--arg` (correctness r3-F-1) and `env.SELF` (edge-cases r4-F-2) — but both were reasoned about as *shell/gh* properties. This one is a property of the transport between the agent and the shell, which no decision covers, and neither row 13 nor row 14 pins the escape.
**Suggested fix:** remove the escape. `test("[^[:space:]]")` is backslash-free and verified equivalent in gh's gojq (`"line1\r\nfoo\r\n   \r\n" | gsub("\r";"") | split("\n") | map(select(test("[^[:space:]]"))) | last` → `foo`, identical to the `\\S` form). Change both sites, add one sentence to Decision 12's trimmed-last-line paragraph recording *why* the character class rather than `\S`, and add a grep row: `grep -cF 'test("\\S")' $S` → `[guard] 0` (Pre `0`), so the fragile form cannot come back.

### F-2: a failed body fetch leaves GitHub's error JSON in the capture file, and 2b step 4's compaction fallback re-parses it as a clean zero-item body
**Severity:** P1
**Where:** spec § 2b step 4 (`:930-935`), § 2b step 3 block (`:901-903`), § Decision 7 (`:239-240`), § Decision 12 `HANDLED_THROUGH` (`:466-468`)
**Edge case:** a per-review body fetch fails **and** the round later loses the `HARVEST_FAILURE` token from conversational state — a context compaction or a long poll sequence, which is exactly the condition 2b step 4's fallback is written for.
**What happens:** silent, permanent finding loss — the ticket's own defect, reached through the recovery path. `gh api` writes the response body to stdout even on an error, so the capture file is not empty. Verified:

```
$ gh api repos/…/pulls/28/reviews/999999999 --jq '.body' > body-999.md 2> body-999.md.err
rc=1;  err → gh: Not Found (HTTP 404)
body-999.md → {"message":"Not Found","documentation_url":"…","status":"404"}
```

2b step 4 says: "if the parsed items for any review id in the round's harvest set are not confidently in hand … **re-read that file and re-parse**." The re-read finds that JSON, locates no `<summary>` section, and yields zero items. Neither tripwire fires (the count tripwire needs a matched section; the phrase tripwire needs a trigger phrase, and the error JSON has none). The review then satisfies Decision 12's "parsed to zero surviving items counts as handled", contiguity advances past it, `R` names it, and it sits below the marker forever. Decision 12's stated invariant — "no review id at or below a posted marker … failed a fetch" — is violated by the mechanism added to recover from compaction.
**Why the spec misses it:** Decision 7 asserts "On a failure the capture file holds GitHub's error JSON … and is **never parsed or counted**", which is true only while the agent still remembers the fetch failed. 2b step 4's fallback exists precisely because that memory is unreliable, and the two rules were written in different decisions.
**Suggested fix:** make the failure a property of the filesystem, not of conversational state. In 2b step 3's block, remove or rename the capture on a non-zero exit — `if [ "$rc" -ne 0 ]; then rm -f "<SCRATCH>/body-<REVIEW_ID>.md"; echo "HARVEST_FAILURE rc=$rc $(cat …err)"; else …` — and add to 2b step 4: "a missing `body-<id>.md` on re-read is a fetch failure for that review, not a zero-item parse; classify it per Decision 12 and never treat it as handled." Add a test row pinning that a review whose fetch failed and whose parse was re-derived after a compaction still floors (or is written off) rather than advancing the mark.

### F-3: the session-condition rule is evaluated at a point where the information does not exist, and GitHub's real scope-failure status is `404`, not `403`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 12 (`:448-450`) "A status that hits more than one review in the same round is a session condition whatever its number — floor them all"; § 2b step 3 (`:908-911`) "one naming `404`, `410` or `451` records the review as **unfetchable** and moves on"
**Edge case:** (a) a harvest set of exactly one review; (b) any round where the first failing fetch is classified before the rest of the set has been attempted.
**What happens:** the safety net added for round-2 F-2 is inert. 2b step 3 decides each review's class **at its own fetch** and "moves on"; "hits more than one review in the same round" is only knowable after every fetch in the round has returned, and nothing says the per-fetch classification is provisional until then. An implementer following step 3 literally writes off `404`s one at a time and never evaluates the multi-review predicate. With a single-review harvest set the predicate is unevaluable by construction. This matters because `403` is not the status the class actually arrives as: GitHub returns **404** for a resource the caller's token is not authorized to see (it hides existence rather than admitting a permission failure), so a token that has lost `repo` scope or org SSO on the review endpoint produces exactly the status the spec classes as *permanently* non-retryable — the review is written off, the marker advances past it, and its findings are unreachable on every future run. Decision 12's own reasoning ("a wrong 'unfetchable' costs the findings") is what makes this consequential rather than cosmetic.
**Why the spec misses it:** the rule was added as prose in Decision 12 to backstop a *status-code* argument about `403`; nobody re-walked 2b step 3, which is where the decision is actually made, and the `403`-vs-`404` asymmetry in GitHub's authorization behaviour was never considered because the round-2 finding was framed around rate limits.
**Suggested fix:** two sentences. In 2b step 3: "Classification is **provisional until every fetch in the round's harvest set has returned**: record the status, continue, and classify at the end of the round." Then state the rule where it can be applied — "if the same non-retryable status hit more than one review in the round, or if the harvest set had only one member and the round also saw any other fetch fail, treat it as a session condition and floor them all." Add a line to Decision 12 noting that GitHub returns `404` for unauthorized-and-hidden resources, so the multi-review test is the only discriminator between a deleted review and a scope loss.

### F-4: 6a's `new_body_items` counts bound-deferred backlog, so a bounded first run never waits for the incremental review and can burn the three-cycle cap on history
**Severity:** P2
**Where:** spec § D5 outcome rules (`:1201-1224`), § 2b step 2 (`:878-896`), against `skills/review-pr/SKILL.md:189-215` (6a's poll loop and its purpose)
**Edge case:** a first run against a long-lived PR with more than 10 body-carrying reviews, where round 1 pushes a fix and therefore reaches 6a — the exact case 2b step 2's bound exists for.
**What happens:** 6a stops being a wait. Step 2 harvests the 10 oldest and leaves `LAST_BODY_REVIEW_ID` at the 10th; the deferred reviews all satisfy `id > LAST_BODY_REVIEW_ID`, so 6a's body-carrying query returns them on **attempt 1**, the bounded harvest parses the next 10, and if any carries a finding `new_body_items > 0` → `REVIEW_SIGNAL=new-findings` → straight to 6b, before CodeRabbit has posted anything about the push. The round then fixes backlog, pushes, loops to 6a, and hits the same condition again. Three cycles later the cap fires with `Remaining findings: …` and the run proceeds to 6d having **never once waited for the incremental review of any of its own pushes** — so a genuine new inline finding on this PR's changed code is not seen this run. The report says `new-findings`, which reads as "CodeRabbit's incremental review found things", when the count came from reviews weeks old. `verdict-landed` is unreachable for as long as backlog remains, since it requires both counts at 0.
**Why the spec misses it:** Decision 4 ("body-level findings are findings") and Decision 2 ("6a's count includes parsed body items so a body-only review cannot read as nothing new") were both written for the case where the new body items come from a *newer* review. The bound, added later, manufactures a permanent supply of "newer than the mark" reviews that are not new at all. A related imprecision at `:887-890` — "within one cycle all three see the same harvest set", where Step 2's harvest and any 6a/6b cycle necessarily have different sets — invites the same conflation.
**Suggested fix:** separate "new" from "unhandled" in 6a. Either gate the body summand on submission time the way the verdict test already is — count only reviews with `submitted_at > PUSH_TIME` toward `new_body_items`, and carry the deferred backlog to 6b through the harvest set rather than through the new-findings predicate — or state explicitly that a round entered on backlog alone does not consume a fix-push-review cycle. Whichever is chosen, say in D5 that `new-findings` sourced from backlog is reported distinctly in 6e, and fix `:887-890` to say "6a's counting pass and 6b's triage pass see the same harvest set" without Step 2.

### F-5: the partial-`--paginate` failure — the design's central assumption — is never verified and no test row exercises it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7 (`:216-223`, `:239-240`), § Decision 14 (`:637-640`), § D9 (`:1525-1530`, `:1567-1572`), test row 29(i) (`:1756-1759`)
**Edge case:** a `--paginate` stream that dies on page 3 of 5.
**What happens:** the entire capture-and-token apparatus rests on `gh api --paginate` exiting non-zero when a page fails, and nothing in the spec verifies that it does. If `gh` instead completes with status 0 after a truncated page set, `COUNT=<n>` is printed for a partial stream, the round reads a smaller-but-well-formed finding set, and the PR #51 false negative the design was written to prevent arrives through the new machinery — undetected, because "non-zero exit" is the only detector. Row 29(i) does not test this: it forces a failure on the **per-review body fetch**, which is a single-resource read with no pagination, so the one code path where a partial result can look complete has no coverage. Secondarily, Decision 7's justification is false for this case: "on a failure the capture file holds GitHub's error JSON, **not a record stream**" — in a mid-pagination failure the file holds a *partial record stream*, which is precisely why the exit status has to be trusted, and an implementer who reads that sentence as licence to detect failure by inspecting the file gets the wrong answer.
**Why the spec misses it:** every empirically verified claim in Decision 7 (`--slurp` rejection, per-page `--jq`, JSONL output) is about a *successful* fetch; the partial-stream case was reasoned about rather than measured, and row 29 was written around the body fetch because that is the one failure easy to force with a bad review id.
**Suggested fix:** (a) correct the sentence at `:239-240` to "on a single-request failure the capture file holds GitHub's error JSON; on a partial `--paginate` failure it holds a truncated record stream. In both cases it is never parsed or counted." (b) Add a row 29(iv): force a mid-pagination failure (revoke the token, or cut the network, between pages of a >1-page `pulls/<N>/comments` fetch) and record the observed `rc` and stderr; state the observed behaviour in Decision 7 so the assumption is a measured fact rather than an inference. (c) If `gh` turns out to exit 0, Decision 7 needs a second detector — e.g. compare the `COUNT` against the endpoint's `Link`-derived total, or re-fetch and compare.

### F-6: `<SCRATCH>` recovery ("the newest by name") adopts a concurrent run's directory, undoing the collision protection the `-$$` suffix provides
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D1 (`:732-739`), § D1 (`:709-716`), § Decision 12 *Race* (`:564-566`), § D8 6e (`:1463-1465`)
**Edge case:** two `/review-pr` runs on the same PR — explicitly tolerated by Decision 12 — where one of them loses `<SCRATCH>` to a compaction, which is the condition the recovery rule exists for.
**What happens:** the two protections cancel. `mkdir` without `-p` plus `-$(date +%s)-$$` guarantees the two runs get distinct directories (verified: second `mkdir` on an existing path → rc=1, no `SCRATCH=` line). The recovery rule then throws that away: "list `"${TMPDIR:-/tmp}"/review-pr-<N>-*` and take the **newest by name**" matches *any* run's directory for this PR, and the newest is the *other*, later-started run's. The recovering run then reads that run's captures (stale verdicts, another round's `guard-hits`) and overwrites its `6f-body.md` and `body-<id>.md` files; whichever run finishes first executes `rm -rf "<SCRATCH>"` under the other, after which every subsequent block's redirect fails and reports `HARVEST_FAILURE rc=1` with empty error text — misattributed to GitHub, the same misdirection D1 warns about for the bare-`$TMPDIR` case. This is round-2 F-6's defect reintroduced by round-2 F-14's fix.
**Why the spec misses it:** the recovery rule was written against the single-run failure it was asked to solve (one run, one directory, lost variable) and never re-checked against the concurrency Decision 12 tolerates two sections earlier. My own round-2 suggested fix proposed the "newest" heuristic and carried the same blind spot.
**Suggested fix:** make the run's own directory identifiable without conversational state, or refuse to guess. Simplest: have the run also record the directory's basename in a place it can re-read — e.g. name it `review-pr-<N>-<HEAD_SHA_SHORT>-<epoch>` and recover by matching the current `git rev-parse --short HEAD` — or state the conservative rule: "if the listing returns **more than one** candidate directory, do not adopt any of them; treat it as a harvest failure and end the run `inconclusive`, since another run may own them." One sentence in D1, and a line in the Decision 12 *Race* paragraph noting that recovery is the one place concurrency is not merely tolerated but harmful.

### F-7: nothing pins 6f's `POSTED=` / `POST_FAILURE` shape, so the bare `gh pr comment` passes every gate
**Severity:** P3
**Where:** spec § D7 (`:1340-1342`), test row 17 (`:1672`, `:1696`), § D8 6e (`:1410-1411`)
**Edge case:** an implementation that carries the guard block but writes the post bare, as the v6 draft did.
**What happens:** the round-2 F-15 fix is unenforceable. Row 17 counts `HARVEST_FAILURE rc=` and the post block deliberately prints `POST_FAILURE rc=` instead, so the post is outside every grep row in the checklist. An implementer who ships `gh pr comment <N> --body-file "<SCRATCH>/6f-body.md"` with no redirect and no token passes rows 1–22 — and the two values that depend on it are the floor trigger (a failed post floors the run for every later round, per Decision 12) and 6e's `dispositions posted in <comment-url>` line, which then has no source. The spec's own discipline is that every load-bearing fix gets a pinned row; this one has none.
**Why the spec misses it:** row 17 was framed as "every governed *fetch* prints its outcome" and the post is a write, so it fell outside the row's quantifier at the same place Decision 7's original quantifier let it slip.
**Suggested fix:** one row — `grep -cF 'POST_FAILURE rc=' $S ; grep -cF 'POSTED=$(' $S` → `1`, `1`, Pre `0`, `0` — and a clause in row 17's rationale saying the post is counted by the new row rather than by row 17.

### F-8: row 20's `$TMPDIR/` guard makes D1's own useful caution unshippable
**Severity:** P3
**Where:** test row 20 (`:1675`, `:1699`), § D1 (`:713-716`)
**Edge case:** an implementer who carries D1's warning into the skill file — the natural thing to do, since the warning is what stops the next editor from simplifying the path.
**What happens:** the gate punishes the correct instinct. Row 20's guard half is `grep -cF '$TMPDIR/' $S` → `[guard] 0`. D1's caution reads "Never a bare `$TMPDIR/…`", which contains the literal `$TMPDIR/`; shipping it makes the row report `1` and fail, and the cheapest way back to green is to delete the warning — the self-defeating-gate dynamic the spec has already corrected three times (rows 4, 8, 21). The prescribed forms `${TMPDIR:-/tmp}/` and `"${TMPDIR:-/tmp}"/review-pr-<N>-*` correctly do **not** contain the substring (verified), so the row is otherwise sound.
**Why the spec misses it:** the row was written to catch the *defect* form and the caution that names the defect form is textually identical to it.
**Suggested fix:** narrow the guard to the executable shape — `grep -cE '^[^#]*\$TMPDIR/' $S` or `grep -cF '> "$TMPDIR/'` → `0` — or state in row 20's rationale that a prose caution naming the literal is expected and the guard must be written so it does not match one.

### F-9: two factual slips in D1's scratch-directory rationale
**Severity:** P4
**Where:** spec § D1 (`:713-716`), (`:711-713`)
**Edge case:** none — documentation accuracy.
**What happens:** nothing breaks; a reader is misinformed twice. (a) "the redirect resolves to `/new_inline`" is a garbled literal — with `TMPDIR` unset, `$TMPDIR/verdicts` resolves to `/verdicts`; `/new_inline` appears to be a leaked placeholder from an earlier edit and will read as nonsense to the implementer. (b) "Without `-p` a collision **prints nothing** and the stop rule above fires" is wrong on the first clause: `mkdir` prints `mkdir: cannot create directory '/tmp/…': File exists` to stderr (verified). The operative rule is unaffected — no `SCRATCH=` line appears on stdout, so the stop fires — and the diagnostic is strictly better than silence, but the sentence as written would have an implementer looking for the wrong signal.
**Why the spec misses it:** both are one-line rationale edits made while fixing round-2 F-6, not re-read against a live shell.
**Suggested fix:** replace `/new_inline` with the concrete example (`/verdicts`), and reword to "a collision prints a `mkdir: … File exists` diagnostic and **no `SCRATCH=` line**, so the stop rule above fires."

---

Verified-clean, recorded so a later round need not re-run them (gh 2.87.3, Git Bash): `gh api --jq` emits **compact one-line JSON** even for records with embedded newlines, so `COUNT=$(wc -l < file)` is a record count for fetches (a)/(b)/(c) and D5's polls (measured: 3 inline records / 10718 bytes on one line each); `--slurp` is rejected alongside `--jq` exactly as Decision 7 states; `$(cat …err)` output is **not** re-scanned by the shell, so a stderr line containing `$(…)`, backticks or quotes cannot inject (probed with a hostile `.err`); a network failure yields a **two-line** stderr, so the `HARVEST_FAILURE` token can span lines but carries no status code and correctly falls to the retryable default; `mkdir` collision → rc=1 with no `SCRATCH=` line; `$$` is a fresh pid per Bash call, which is harmless because D1 evaluates it once and carries the result literally; all fifteen checkable "Pre (measured on unmodified `main`)" values in the test plan reproduce exactly.

## Summary
P0: 0 | P1: 2 | P2: 4 | P3: 2 | P4: 1

Key paths:
- Spec: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.spec.md`
- Brief: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.brief.md`
- Subject: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\skills\review-pr\SKILL.md`
- Round-2 reports: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.reviews\round-2\`

STATUS: RED P0=0 P1=2 P2=4 P3=2 P4=1
