Grounding complete. Spec re-read fresh from disk (1861 lines); `AGENTS.md` end to end; global + project `CLAUDE.md`; `docs/portability-contract.md` §1–§5; current `skills/review-pr/SKILL.md` (406 lines, unmodified on `main` — `:11`, `:68`, `:75`, `:172`, `:174`, `:194`, `:224`, `:252`, `:262`, `:277`, `:279`, `:290`, `:341` re-verified); wiki `decisions/` (newest is still `2026-09-07-vhs-36-…` — nothing new since round 2); the brief; all three round-2 reports.

**Every `Pre` in the test plan re-measured against the working tree — all match**: r4 `0`, r5 `7`, r6 `3`, r7 `0`, r8 `0`, r9 `1`/`2`, r10 `0`, r11 `1`, r12 no match, r13 `0`, r14 (`-A5`) `0`, r15 `0`/`1`, r17 `0`, r18 `0`, r19 `0`/`0`, r20 `0`/`0`, r21 (extended regex) `0`, r22 `0`. Row 14's new `-A5` window was hand-checked against every block shape in the spec: the `if` line sits at +4/+6 from the `gh api --paginate` line and carries no `|` before its `wc`, so the guard neither false-positives nor is unfailable. Row 21's four alternations all measure `0` on `main`.

**Fenced-block audit:** script-extracted scan of all **13** fenced blocks (including the three indented ones at 848, 900, 1419 that a naive `^```` scan misses) for `r<n>-F-<n>` / `a2r<n>-F-<n>` / `Decision <n>` / `D<n>` / `v<n> draft` / `env.SELF` returns **zero hits** in shipped blocks; the single hit is test-plan row 19's grep pattern, which is spec-side by construction. Citation forms are consistent: `r1`/`r2`/`r3`/`r4` for attempt 1, `a2r1`/`a2r2` for this attempt, never mixed. Count arithmetic reconciles: 11 paginated sites (row 4, Decision 5) vs 13 token sites (row 17, Decision 7) differ exactly by `(a2)`, the login fetch and the per-review body fetch, minus the `:174`/verdict-stream merge — no stale count survives.

---

# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | 2b step 3's slice starts at `<summary>` | CLOSED | § D2 step 3 (spec:921-924) now slices "from the `<details>` line preceding each `<summary>`" and states step 7's seeding requirement |
| correctness | F-2 (P2) | row 23's mask claim rests on an absent phrase | CLOSED | row 23 (spec:1709-1713) restates it as "line 67's `Outside diff comments:` is not a trigger phrase, so this specimen cannot exercise the fence mask"; row 27(iii) supplies the negative-mask specimen |
| correctness | F-3 (P2) | harvest-identity rationale false; floor latch vs predicate | CLOSED | § Decision 12 spec:417-421 replaces "never share a harvest set" with the retry case; spec:428-437 makes the floor "recomputed at every post … not a latch", with the failed-post cause sticky by construction. (A new variant of the *worked example* arrives with this fix — F-3 below) |
| correctness | F-4 (P2) | D6 "same block as D5's inline poll" | CLOSED | § D6 spec:1236-1242 "with its existing per-item `--jq` … **unchanged** — not D5's `.id`-only program"; row 17 "D6's inline fetch is **not** mergeable with D5's" |
| correctness | F-5 (P2) | row 14's `-A2` misses the 4+-line shape | CLOSED | row 14 now `-A5` (spec:1669); re-measured `0`, hand-checked against the 5-line resume/guard shape |
| correctness | F-6 (P3) | cleanup unreachable from early exits | CLOSED | § D1 spec:721-730 "removed on **every** exit path", naming `:79`, `:81`, `:83`, `:381` |
| edge-cases | F-1 (P0) | unfetchable-only round posts no marker | CLOSED | § D7 post condition spec:1302-1312 third arm; § Decision 12 spec:512-519; § D9 spec:1540-1543; row 29(ii) |
| edge-cases | F-2 (P1) | `403` classed non-retryable | CLOSED | § Decision 12 spec:439-450 (non-retryable = `404`/`410`/`451`, retryable default); § D9 spec:1536-1539; 2b step 3 spec:908-911. (The multi-hit override added alongside it is F-2 below) |
| edge-cases | F-3 (P1) | bound scope specified three ways | CLOSED | 2b step 2 spec:878-896 candidate/harvest/deferred + "applies to every invocation of 2b"; D5 spec:1201-1204; D6 spec:1243-1252 "parsed-and-triaged" |
| edge-cases | F-4 (P1) | `gh api user` outside the shape | CLOSED | § D2 step 1 block spec:848-855; § Decision 7 spec:249-252; row 17 thirteen sites `≥ 12` |
| edge-cases | F-5 (P2) | HTTP status never printed; taxonomy not total | CLOSED | `2> "<SCRATCH>/<name>.err"` + `$(cat …err)` in all 13 blocks; § Decision 12 spec:446-448 "**any status or error text not listed here**" |
| edge-cases | F-6 (P2) | `mkdir -p` hides a collision | CLOSED | § D1 spec:702, 708-716 — `mkdir` without `-p`, plus `$$`, with the stop rule |
| edge-cases | F-7 (P2) | `<SCRATCH>` leaked on early exits | CLOSED | as correctness F-6 |
| edge-cases | F-8 (P2) | phrase-scan view nested in the per-section loop | CLOSED | 2b step 6 spec:963-975 hoists it "**First, once per review body … before and regardless of the per-section work below — including when step 5 located no section at all**"; row 27(iv) |
| edge-cases | F-9 (P2) | `h<IDS>` two definitions | CLOSED | 2b step 2 renames candidate/harvest set; § Decision 12 spec:412-416 "never the full candidate list … at most 10 ids" |
| edge-cases | F-10 (P2) | floor never lifted | CLOSED | § Decision 12 spec:430-437 recompute rule; § "Why it must be run-scoped" spec:496-500 |
| edge-cases | F-11 (P2) | depth constant within a provisional span is false | CLOSED | 2b step 6a spec:988-990 "strip **up to** that many … a line with fewer is left as-is"; step 5 spec:952-957 restates the true invariant |
| edge-cases | F-12 (P3) | `Retry-After` unimplementable in the capture shape | CLOSED | § Decision 14 spec:633-636 fixed 60 s, with the `--include` reason (residue → F-7 below) |
| edge-cases | F-13 (P3) | no way to measure body bytes | CLOSED | 2b step 3 block spec:903 emits `BYTES=`; spec:906-907 names it the one two-field token |
| edge-cases | F-14 (P3) | `<SCRATCH>` has no re-derivation rule | CLOSED | § D1 spec:732-739 "do **not** re-run the resolve line … take the newest by name" |
| edge-cases | F-15 (P3) | 6f's post outside any observability shape | CLOSED | § D7 block spec:1340-1342 `POSTED=` / `POST_FAILURE`; 6e line spec:1448 (residue → F-5 below) |
| conventions | F-1 (P2) | ship-ready rule scoped to fenced blocks | **PARTIAL** | § Design preamble spec:678-690 now covers "2b's steps, D3's rules and D9's edge cases" — the three regions I named — but not D7, D1 or D8, which also state shipped skill text → **F-1 below**, severity retained |
| conventions | F-2 (P3) | `rm -rf` / `date +%s` without precedent; cleanup asymmetric | CLOSED | § D1 spec:726-728 states removal as a capability with `AGENTS.md:68`'s bash-plus-host phrasing; spec:717-719 records the `date +%s`/`mkdir` choice and its lack of precedent (`mkdir -p` in `spec-close:333` verified) |
| conventions | F-3 (P3) | block repeated 12× with no stated reason | CLOSED | § Decision 7 spec:252-256 "shell state does not survive between Bash calls (`:180`) … The repetition is deliberate, not copy-paste" |
| conventions | F-4 (P3) | Deferred bullet's triage inconsistent | CLOSED | § Deferred spec:1856-1859 "CodeRabbit's quoted Markdown is **fenced** in every observed specimen … the trigger is remote" |
| conventions | F-5 (P4) | row 14 rationale enumerates incompletely | CLOSED | row 14 spec:1693 now states the property ("No `\|` in any `--jq` program is followed by …") |

All five manifest P0/P1 items CLOSED. One P2 is PARTIAL and retains its severity.

## Findings

### F-1: The shipped-text rule names 2b, D3 and D9 but not D7 — which defines an entire new skill section carrying 15 citations and 17 `Decision`/`D<n>` refs
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design preamble (spec.md:678-690); § D7 (spec.md:1278-1412); § D1 (spec.md:692-830); § D8 (spec.md:1413-1470)
**Convention violated:** the spec's own preamble rule, plus repo practice — `grep -rncE '\bDecision [0-9]|\bD[0-9]+\b' skills/*/SKILL.md` is `0` across all eleven shipped skills, and the file's idiom cross-references by step name (`:382` "per the guard in 6c", `:391`, `:406`).
**Evidence:** the preamble asserts *"The skill file carries two kinds of text from this Design section: the fenced `bash` / `text` blocks verbatim, comments included, and the operative sentences of **2b's steps, D3's rules and D9's edge cases**."* That enumeration is incomplete on its face: **D7 is the definition of a brand-new skill section** (`### 6f. Body-level dispositions`) whose post condition, neutralization rule, body-shape prose and error handling are all operative skill text — measured over D7's non-fenced prose: **15 lens citations and 17 `Decision <n>`/`D<n>` references**. D1's `<SCRATCH>` protocol (creation, every-exit removal, the loss-recovery rule) is likewise runtime instruction the skill must carry — 18 citations, 12 refs — and D8 supplies 6e's report lines (6/3). Concretely, D7's operative sentence at spec:1302 reads *"**Post condition** (Decision 12): post once per round when…"* — a dangling pointer in a file that has no Decision 12. Row 21 is whole-file, so the citation and `D<n>` halves *are* gated and a literal implementation fails its own gate; the residue is that for D7/D1/D8 the implementer has no stated rule telling them what to do about it, and the cheapest way to pass row 21 is to delete the rationale wholesale — exactly the dynamic the preamble's own closing sentence warns about.
**Suggested fix:** one clause in the preamble — replace the three-region list with *"…and the operative sentences of every Design subsection that states text the skill carries: 2b's steps, D3's triage rules, D7's 6f section, D1's scratch-directory protocol, D8's 6e report lines, and D9's edge cases."* No new test row is needed; row 21 already gates the whole file.

### F-2: Decision 12's multi-hit override ("whatever its number — never mark them unfetchable") re-opens the permanent-blindness failure the unfetchable class was added to close, and D9's shipped bullet does not carry it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 12 (spec.md:444-454); § D9 (spec.md:1531-1539)
**Convention violated:** contradicts the spec's own recorded rationale two sentences earlier, and splits a rule across a spec-only statement and a shipped one that states it differently.
**Evidence:** Decision 12 fixes the non-retryable set as `404`/`410`/`451` "because they are properties of the review rather than of the session", then adds: *"A status that hits more than one review in the same round is a session condition **whatever its number** — floor them all, **never mark them unfetchable**."* For two genuinely dead reviews inside one 10-review harvest, the second rule overrides the first and floors both. A floor is cleared only when the id becomes handled (spec:430-437); a deleted review never becomes handled; so the floor is permanent across runs, `PRIOR_MARK` never advances past it, and once more than 10 reviews sit above it the bound defers the newest ones on every run — the outcome Decision 12 itself names four lines earlier as *"permanent blindness to new findings, the defect this ticket removes."* Meanwhile D9's bullet (shipped text) states the unconditional form — *"A per-review body fetch returns a non-retryable status (404/410/451) … It is recorded **unfetchable**"* — with no multi-hit exception, so spec and skill disagree on the disposition. The rule has a genuine motivation (GitHub returns `404` rather than `403` for resources the token cannot see), but "whatever its number" is broader than that motivation.
**Suggested fix:** scope the sentence to the case it was written for and state the motivation: *"A status that hits **every** review attempted in the round is a session condition even when it is a `404` — GitHub masks permission failures as `404` — so floor them all rather than writing them off. A non-retryable status hitting only some of the round's reviews is per-review, and those are unfetchable."* Then add the same one-clause qualifier to D9's bullet so the shipped text carries the whole rule.

### F-3: Decision 12's monotone-`R` rule and its own worked example prescribe different marker values for the same round
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 12 "Rule for `R`" (spec.md:474-476) vs § Decision 12 "Why it must be run-scoped" (spec.md:496-500)
**Convention violated:** the spec's established single-source discipline for load-bearing rules — "D6 holds the only statement of that rule and its worked example" (spec.md:82-83) — applied to `R` in one place and violated in another.
**Evidence:** the rule reads *"`R` is **monotone across the rounds of a run**: a round whose computed `R` does not exceed the last `R` this run posted claims nothing new, and posts its comment with `r0`."* The worked example four paragraphs later runs: round 1 harvests `[100, 200, 300]`, 300 fails, posts `r200`; round 2's harvest is `[300, 400]`; *"if it fails again the floor stands and **round 2 posts `r200:h300,400`**."* Round 2's computed `R` is `200`, which does not exceed the `200` round 1 posted — so the rule says `r0:h300,400` and the example says `r200:h300,400`. Both satisfy Decision 12's invariant (the resume query takes the maximum across markers, and round 1's `r200` already stands), which is why this is P2 rather than higher — but they are two different comment bodies for one round, and the example is the text a reader will copy. The example's wording is new this round, arriving with the floor-recompute fix (correctness a2r2-F-3), so the two statements have not been reconciled since.
**Suggested fix:** pick one and make the other follow. The example is the more informative form; if it is intended, reword the rule as *"`R` never decreases across the rounds of a run; a round that has nothing new to claim re-posts the run's current `R` (or `r0` if none) — its `h<IDS>` still names this round's harvest, so the post is not suppressed."* If `r0` is intended, change the example's second branch to `r0:h300,400`.

### F-4: The 6f post condition is stated in three places, and the earliest statement is missing the arm added this round
**Severity:** P3
**Where:** spec § Decision 2 (spec.md:95-100); § Decision 12 "Progress does not depend on findings" (spec.md:512-519); § D7 "Post condition" (spec.md:1302-1312)
**Convention violated:** the spec's own single-source rule for load-bearing predicates (spec.md:82-83, "D6 holds the only statement of that rule"; spec.md:1048-1049, "the single shared rule of D3 … not a second, body-only rule").
**Evidence:** Decision 12 and D7 both state the three-arm condition (≥1 body finding **or** `R` advances and (a floor exists **or** an unfetchable review was recorded)). Decision 2's bullet still states a two-arm shorthand — *"Where the round has something to come back for — the harvest-set bound deferred reviews, or a fetch failed — 6f posts a findings-free comment"*, then *"On a PR where nothing was deferred and nothing failed, no comment posts and no marker is needed."* It is not strictly wrong (a `404` is a fetch that failed), but "failed" is the word Decision 12 reserves for the floor class, and the unfetchable arm — the one the edge-cases P0 was raised for — is precisely the case Decision 2's phrasing reads past. Three copies of one predicate is also how the round-1 advance-rule divergence started.
**Suggested fix:** collapse Decision 2's bullet to a pointer — *"Where the round leaves something behind, 6f posts a findings-free comment so the marker lands; Decision 12 holds the only statement of the post condition."* — and leave the full three-arm form in Decision 12, with D7 pointing at it.

### F-5: `POSTED=` / `POST_FAILURE` is load-bearing but ungated, and Decision 7 states the token without the field the block emits
**Severity:** P3
**Where:** spec § Decision 7 (spec.md:256-258); § D7 block (spec.md:1340-1342); § D7 error handling (spec.md:1406-1411); test plan rows 3-22 (spec.md:1657-1701)
**Convention violated:** the test-plan discipline this spec sets for itself — every load-bearing printed construct gets a pinned row (row 17 for `HARVEST_FAILURE rc=`, row 13 for `"<SELF>"`, row 18 for the marker, rows 19-21 for the negative guards).
**Evidence:** the post's outcome is the most consequential value in the design — a `POST_FAILURE` floors the run and suppresses the marker on every later round (spec.md:1408-1410), and `POSTED=<url>` is the only source for 6e's `dispositions posted in <comment-url>` line. No checklist row greps either token, so an implementer who writes the post bare — the v4-draft shape the spec elsewhere rejects — passes the whole gate. Separately, Decision 7 names the sibling shape as `POSTED=<url>` / `POST_FAILURE rc=<n>` while the block emits `POST_FAILURE rc=$rc $(cat "<SCRATCH>/6f-url.err")`; the same error-text field is described for `HARVEST_FAILURE` but not for its sibling.
**Suggested fix:** add one row — `grep -cF 'POST_FAILURE rc=' $S` → `1`, Pre `0` (measured) — and align Decision 7's sentence to `POST_FAILURE rc=<n> <gh error text>`.

### F-6: stderr capture to a file has no precedent in the shipped skills, and unlike `date +%s` / `mkdir` the choice is not recorded as such
**Severity:** P4
**Where:** spec § Decision 7 (spec.md:226-240); all 13 capture blocks; contrast § D1 (spec.md:717-719)
**Convention violated:** repo practice and the spec's own new habit of recording no-precedent primitives. `grep -rn '2>' skills/` returns only `2>/dev/null` — stderr **discard**, in `ship-spec`, `spec-brief`, `spec-close`, `spec-cycle`; nothing anywhere captures stderr to a file or re-reads it with `cat`. `docs/portability-contract.md` says nothing about stderr in §1-§5, so the construct is neither blessed nor forbidden.
**Evidence:** Decision 7 gives a strong *functional* rationale (the status is only on stderr and `rc` is `1` for `404`/`403`/`5xx` alike), which is why this is a nit and not a finding against the design. But D1 goes out of its way to record that "`date +%s` and `mkdir` have no precedent in the shipped skills (`mkdir -p` does, in `spec-close`)", and the same courtesy is not paid to the redirect-and-`cat` pair that appears thirteen times. I verified the construct is shell-safe as written: `$(cat …)` is inside double quotes in every block, so `gh`'s error text cannot word-split or re-evaluate.
**Suggested fix:** one clause in Decision 7 — *"Capturing stderr to a file and echoing it has no precedent in the shipped skills, whose only stderr idiom is `2>/dev/null`; it is chosen because the status text exists nowhere else."*

### F-7: D7 says its error handling "mirrors 6c's (`:279`)" on the one rule where it deliberately contradicts it
**Severity:** P4
**Where:** spec § D7 (spec.md:1406-1408); § Decision 14 (spec.md:633-636) vs `skills/review-pr/SKILL.md:279`
**Convention violated:** clarity of a cross-reference in shipped text — the skill will carry two different `429` rules within ~130 lines.
**Evidence:** `:279` reads *"On 429 with a `Retry-After` header, wait the indicated duration and retry once."* D7's shipped sentence reads *"**Error handling** mirrors 6c's (`:279`) and Decision 14: on failure log and continue, never abort; on 429, wait 60 seconds and retry once (the fixed wait, not the header)."* The divergence is deliberate and justified (Decision 14: the header is invisible in the capture shape), and the parenthetical flags it — but "mirrors 6c's" is the wrong verb for the one clause a reader must *not* mirror, and after row 21 strips the `Decision 14` pointer the parenthetical loses its reason.
**Suggested fix:** *"Error handling follows 6c's log-and-continue discipline (`:279`), with one deliberate difference: these fetches capture stdout to a file, so no response header is readable — on 429 wait 60 seconds and retry once rather than reading `Retry-After`."*

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 2 | P4: 2

Relevant paths (all absolute):
- Spec: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.spec.md`
- Brief: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.brief.md`
- Subject: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\skills\review-pr\SKILL.md`
- Conventions checked: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\AGENTS.md`, `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\portability-contract.md`, `C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki\decisions\`
- Round-2 reports: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.reviews\round-2\`

STATUS: GREEN
