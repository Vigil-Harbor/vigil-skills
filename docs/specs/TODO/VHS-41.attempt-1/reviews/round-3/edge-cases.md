# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Marker advances past undispositioned reviews | **PARTIAL** | Decision 12 (spec:309–339) fixes the *within-a-round* case (contiguity rule, oldest-first bound at 2b step 2, failed-post suppression). The invariant is stated globally ("no review id at or below a posted marker…") but enforced per round only; a *later* round of the same run computes `R` over its own harvest set and leapfrogs an earlier round's gap. See F-1 below. Original P1 retained. |
| edge-cases | F-2 | Harvest failure at Step 2 exits "Nothing to review" | **CLOSED** | Decision 14 final bullets (spec:415–422); D1's `:81` clause (spec:486–492); D9's `:381` rewrite. (Adjacent legs — fetch (a)/(c) and `:83` — are new, see F-8.) |
| edge-cases | F-3 | One blockquote depth per body defeats the code mask | **PARTIAL** | D2 reordered: step 5 on raw (spec:539), step 6 per section (spec:551), step 7 walk (spec:577). But step 6 normalizes "over that section's span only" and the span is only defined by step 7 — circular. See F-3. Original P1 retained. |
| edge-cases | F-4 | `wc -l` swallows `gh` exit status | **CLOSED** | Decision 7's required shape (spec:193–197), D5's `$TMPDIR/new_inline` + `rc=$?` (spec:722–726), test row 14 (spec:1031). |
| edge-cases | F-5 | Resume/guard trust any author's comment | **PARTIAL** | Rule stated (Decision 12 "Author filter is load-bearing", spec:341–352) but both prescribed commands are non-functional — `gh api` has no `--arg`. Verified: `gh api user --jq --arg self x '.login'` → `accepts 1 arg(s), received 4`. See F-2. |
| edge-cases | F-6 | No 6f call site for an all-non-fix incremental round | **CLOSED** | D6 "Both exit branches post 6f" (spec:775–782); D7 generalizes `:245` (spec:799–801). `:245` verified as the 6c paragraph carrying that sentence. |
| edge-cases | F-7 | Test plan verifies the happy parse only | **CLOSED** | Rows 17–19 now assert tripwire silence; rows 21–23 added (spec:1053–1073). (Row 21 is now contradicted by the D2 text itself — see F-6.) |
| edge-cases | F-8 | Masked vs raw text handed to triage | **PARTIAL** | Paragraph added (spec:570–576), but as worded it pushes step 9's *structural* matching onto raw text. See F-6. |
| edge-cases | F-9 | Bodies bounded by count, not size | **PARTIAL** | D2 step 3 adds file capture + slicing + a size report line (spec:523–530), but the threshold is literally "a stated size" — no number. See F-12. |
| edge-cases | F-10 | 20-item bound exempts outside-diff; "deferred" wrong word | **CLOSED** | D2 step 11 hard ceiling of 50, `grouped (not individually triaged)` (spec:616–626). |
| edge-cases | F-11 | Phrase tripwire scope ambiguous | **PARTIAL** | Per-phrase scoping added (spec:285–293), but it requires "the blockquote-stripped, code-masked **body**", which D2 step 6 no longer produces. See F-4. |
| correctness | F-1 | 2b placed after Step 2's short-circuits | CLOSED | D1 "Order matters" + "invoked from inside Step 2" (spec:466–471). |
| correctness | F-2 | D5 never converts `:174-175` | CLOSED | D5 first bullet (spec:708–715). |
| correctness | F-3 | "four" pre-existing bare tool names → seven | CLOSED | Design preamble (spec:431–438). |
| correctness | F-4 | All-non-fix incremental round has no 6f call site | CLOSED | D6 `:241` branch (spec:779–782). |
| correctness | F-5 | Row 4 has no pinned value; `:172` unnamed | **PARTIAL** | `:172` now named (spec:135); row 4 has a pinned value but it is wrong (9 vs 10). See F-7. |
| correctness | F-6 | Rows 7 and 10 already pass unmodified | CLOSED | Rows repinned on new strings; pre-counts verified 0/0 against `main`. |
| correctness | F-7 | `AGENTS.md:46` is the heading | CLOSED | D10 targets `:48`; verified `AGENTS.md:48` is the `/review-pr` paragraph. |
| correctness | F-8 | `(a2)` unguarded on a PR with no verdict review | CLOSED | D1 "If (a) yields no record" (spec:474–479). |
| correctness | F-9 | All-dedup round posts no marker | CLOSED | Decision 2 bullet 2 (spec:83–87). Wording wrinkle folded into F-11. |
| conventions | F-1 | Decision 5's exclusion list incomplete | CLOSED | Named exclusions (spec:131–140). |
| conventions | F-2 | Three grep rows cannot fail | **PARTIAL** | Rows repinned, but row 8's `-F` pattern can never match anything. See F-7. |
| conventions | F-3 | Bare-tool-name fence undercounts | CLOSED | spec:431–438. |
| conventions | F-4 | Deferred section convention | CLOSED | `## Deferred (P2+)` present. |
| conventions | F-5 | D3 widens inline severity rule | CLOSED | Recorded as deliberate (spec:663–669). |
| conventions | F-6 | `AGENTS.md:7` known-false claim | CLOSED | D10 second bullet; verified `AGENTS.md:7` carries "no test suite". |
| conventions | F-7 | VHS-29's rejection of fence-masking | CLOSED | Decision 13 (spec:380–391). |
| conventions | F-8 | `AGENTS.md:46` → `:48` | CLOSED | D10. |

## Findings

### F-1: A later round's marker leapfrogs an earlier round's harvest gap — Decision 12's invariant is per-round, the resume read is per-PR
**Severity:** P1
**Where:** spec § Decision 12 (`:309-339`), § Design D2 step 2 (`:513-521`), § Design D6 advance rule (`:767-774`)
**Edge case:** A multi-round run in which round 1 leaves a gap (a Decision 14 body-fetch failure, or reviews deferred by the 10-review bound) and round 2 completes cleanly.
**What happens:** Round 1 harvests `[100, 200, 300]`; review `300`'s body fetch fails. `R = 200`, marker `r200` posted. D6's advance rule then sets `LAST_BODY_REVIEW_ID = 300` ("the highest id **in the round's harvest set**") regardless of the failure. Round 2's harvest set is `[400]`, fully handled, so its `R = 400` and it posts `r400`. The resume query (2b step 1) "Take the numerically highest value" now returns **400**. Review `300` is above the round-1 marker but below the round-2 marker, and is **permanently unharvestable on every later run, silently** — the exact defect r2-F-1 was raised for, reached by a different path. The same happens with the bound: if the round's harvest set is 12 reviews, `900` and `1000` are deferred, and a later round in the same run posts a marker above them.
**Why the spec misses it:** Decision 12's rule is scoped to "the round's harvest set" and its two supporting rules cover only (a) contiguity *within* a round and (b) a failed **6f post** across rounds. There is no cross-round rule for a *harvest* gap. The invariant at `:317-320` and the D9 edge case "the unhandled reviews stay above it and the next run harvests them" are therefore both false for a multi-round run. D6's advance rule compounds it by advancing `LAST_BODY_REVIEW_ID` past a review whose fetch failed, so the gap is not even retried later in the same run.
**Suggested fix:** Add a third supporting rule to Decision 12, symmetric with the failed-post one: *"Once any round of a run leaves a review unhandled — a failed harvest fetch, or a review omitted by the 2b step 2 bound — record the lowest such id as `HARVEST_FLOOR`. Every later round of that run posts its comment with **no marker** (nothing above the floor can be claimed as handled)."* Also amend D6's advance rule to `LAST_BODY_REVIEW_ID = the highest id whose body was fetched and parsed successfully in this round`, so a failed review is retried by the next 6a poll of the same run.

### F-2: Both new author-filtered queries use `gh api --jq --arg`, which `gh` rejects outright
**Severity:** P1
**Where:** spec § Design D2 step 1 (`:506`), § Design D7 (`:811`), test row 13 (`:1030`)
**Edge case:** Every run, unconditionally — this is not an edge, it is the only path.
**What happens:** `gh api` has no `--arg` flag (verified on the installed `gh 2.87.3`: `-q/--jq`, `--paginate`, `--slurp`, `-f`, `-F`, `-H`, `-t`, … and nothing else). Running the prescribed shape errors before any HTTP call:

```
$ gh api user --jq --arg self x '.login'
accepts 1 arg(s), received 4
```

`--jq` swallows `--arg` as its program, and `self`, `"$SELF"` and the real program become surplus positional args. Per Decision 14 the resume query and the idempotency-guard fetch are both classified harvest fetches, so a non-zero exit on either is a **body harvest failure** — which (Decision 14's early-exit clause, closing r2-F-2) forces `REVIEW_SIGNAL=inconclusive` and blocks `:81` and `:381` on *every* run. The skill can never post a disposition (guard fails closed → no post → no marker) and can never report a clean PR. Test row 13 pins the broken shape (`grep -c 'select(.user.login == $self)'` → `2`), so the gate certifies the defect.
**Why the spec misses it:** the `--arg` idiom is correct for a standalone `jq` binary; Decision 7 already establishes that the repo deliberately avoids a standalone `jq` ("piping to a standalone `jq` binary would add a dependency the repo does not have"), so `$self` has no way to be bound.
**Suggested fix:** interpolate the login into the program the way the file's other queries interpolate `<PREV_REVIEW_ID>`, and retarget row 13. E.g. in D2 step 1 and D7:

```bash
SELF=$(gh api user --jq .login)
gh api --paginate repos/{owner}/{repo}/issues/<N>/comments \
  --jq ".[] | select(.user.login == \"$SELF\") | (.body // \"\") | capture(\"review-pr:body-dispositions:r(?<r>[0-9]+)\") | .r"
```

and change row 13 to a fixed prose token both sites carry (e.g. `grep -cF 'only a marker the skill wrote counts'` → `2`).

### F-3: D2 steps 6 and 7 are circular — step 6 normalizes "that section's span", which only step 7 computes
**Severity:** P1
**Where:** spec § Design D2 steps 5–7 (`:539-585`)
**Edge case:** A review body carrying both sections (the case the reorder exists for — test row 22).
**What happens:** Step 5 locates only the section's *announcement* line. Step 6 says "for each section found in step 5, **over that section's span only**: (a) strip depth … (b) mask fences". Step 7 then computes the span by a depth walk "counting `<details>` and `</details>` **in the masked text**". Step 6 needs step 7's output and step 7 needs step 6's output. An implementer resolving the deadlock the obvious way — normalize from the section start to end-of-body, then walk — reintroduces round-1 F-17 exactly: on PR #28's shape the Outside-diff section is at depth 1 and the Nitpick section that follows it is at depth 0, so stripping one `>` from "the span" eats a content `>` on every line of the Nitpick section, and its fenced blocks and item headers are corrupted before step 9 ever sees them.
**Why the spec misses it:** the reorder that closed r2-F-3 moved masking *after* section location, but the boundary walk was left after masking, and no step defines a section extent that does not already depend on the mask.
**Suggested fix:** break the cycle with a cheap provisional extent. Amend step 6 to read: *"Take a provisional span from the `<details>` line preceding this section's summary to the start of the next section summary (or end of body). Strip depth and mask fences over that provisional span. Step 7's depth walk then narrows it to the true section end; re-slice nothing — the provisional span is a superset, and depth is constant within it because a section summary is where depth changes."* State explicitly that the provisional span **includes the preceding `<details>` line** step 7 starts its walk on.

### F-4: Decision 11's phrase tripwire reads a whole-body masked text that D2 step 6 stopped producing
**Severity:** P1
**Where:** spec § Decision 11 second bullet (`:285-293`), § Design D2 step 6 (`:551-576`), step 12 (`:628-630`)
**Edge case:** The tripwire's own trigger condition — CodeRabbit changed a summary format, so *no section matched*.
**What happens:** Decision 11 requires the detector to run on "the **blockquote-stripped, code-masked body**". After the per-section rework, blockquote-stripping and masking exist only over a section span — and by construction the phrase tripwire fires precisely when there is no section span to normalize. Two outcomes, both bad: (a) taken literally the detector has no input and cannot run, so a format drift degrades straight back to silent blindness — the thing Decision 11 exists to prevent; or (b) an implementer masks the raw body at depth 0, in which case a fence sitting inside a `> [!CAUTION]` callout is not recognized (its lines start `> ``` `), so the mask misses it and a quoted `outside diff range` inside that callout fires a false tripwire. Case (b) is guaranteed from day one — this change puts both phrases into `skills/review-pr/SKILL.md`, and CodeRabbit quotes changed Markdown back inside CAUTION callouts. Test rows 19 and 21 both assert "neither tripwire fires".
**Why the spec misses it:** Decision 11 was written against the round-2 body-wide normalization and was not revisited when D2 step 6 became per-section.
**Suggested fix:** give the tripwire its own defined input. Amend Decision 11's second bullet and D2 step 12 to: *"For the phrase scan, build a **body-wide** normalized copy: strip the maximum uniform leading `>` depth found on each line independently (per-line depth, not one body depth — the tripwire only needs fences visible, not structure preserved), then mask fences and inline-code spans. Scan that copy. It is used for the phrase detector only and is never sliced into a finding."*

### F-5: `LAST_BODY_REVIEW_ID` is never advanced after Step 2's harvest, so 6a's first poll re-counts round-1 body items as new findings
**Severity:** P1
**Where:** spec § Decision 2 (`:56`), § Design D5 (`:731-732`, `:738`), § Design D6 advance rule (`:767-774`)
**Edge case:** Any PR with ≥1 body-level finding in the first (Step 2 / Step 3) round that also pushes fixes — the Done-when-1 scenario.
**What happens:** Decision 2 seeds `LAST_BODY_REVIEW_ID = PRIOR_DISPOSITIONED_REVIEW_ID` (0 on a first run). The **only** advance rule in the spec is in D6, i.e. inside 6b. Step 2's harvest and Step 3's triage never advance it. So 6a's second query, `select(.id > <LAST_BODY_REVIEW_ID>)`, returns every body-carrying review already harvested and triaged in Step 2, and D5 says "for each review id the second query returns, run the 2b parse **once** … to get its **body-item count**" — the parse count, not a post-dedup count. `new_body_items > 0` on the first poll attempt, always. Consequences: `REVIEW_SIGNAL=new-findings` is set when nothing new exists; the `verdict-landed` branch (which requires "both counts 0") becomes **unreachable** on every such PR, so the run can never honestly report "no new findings" and always ends telling the operator to re-run; and 6b is entered for a cycle whose findings all dedup away.
**Why the spec misses it:** D6's advance rule was written to close correctness r1-F-10, which was about the 6b→6a loop; the Step 2 → 6a transition has no analogous rule, and the `:215` `PREV_REVIEW_ID` precedent the spec explicitly declines to carry over ("that variable always has a review just triaged") is exactly where the missing seed would have come from.
**Suggested fix:** add to D1/D2 step 2: *"After Step 2's harvest completes and Step 3 triages it, set `LAST_BODY_REVIEW_ID` to the highest id whose body was fetched and parsed successfully in that harvest (same rule as D6), so 6a's poll is relative to what round 1 already handled."* Independently, amend D5 to count **post-dedup** new body items, so a review restating an already-triaged finding cannot set `new-findings` either.

### F-6: Step 9's item detection and Decision 10's `<details>` strip run on raw text, contradicting test row 21
**Severity:** P1
**Where:** spec § Design D2 step 6 closing paragraph (`:570-576`), step 9 (`:596-607`), test row 21 (`:1063-1068`), § D9 edge case "Body item quotes `<details>`…"
**Edge case:** A finding whose prose quotes a fenced code sample containing `` `12-30`: `` or `</details>` — i.e. every CodeRabbit review of *this very PR*, since the change writes both strings into `skills/review-pr/SKILL.md`.
**What happens:** Step 6's closing paragraph says the masked text "computes boundaries only" and that "every span handed to step 9 … is sliced from the **raw** … text". Step 9 is the step that *finds items*: it matches `` ^`(?<lines>[^`]+)`:\s*(?<labels>.*)$ `` and then "remove**s** every nested `<details>…</details>` block" — both structural operations, both on the raw span per the preceding paragraph. So a quoted `` `12-30`: `` line inside a code sample opens a phantom item (parsed 2 vs declared 1 → count tripwire fires, and one real finding is split in half), and a quoted `</details>` terminates Decision 10's strip early, handing triage a mangled item body **silently**. Test row 21 requires exactly this input to "yield 1 item and fire no tripwire" — the spec as written fails its own gate row, and D9's edge case ("masked before structural matching") contradicts step 6's paragraph.
**Why the spec misses it:** the r2-F-8 fix (raw text to triage) and the r2-F-3 fix (masking for structure) were written independently; "spans handed to step 9" reads as *step 9's outputs* in one sentence and *step 9's inputs* in the other.
**Suggested fix:** restate the rule as masked-for-matching / raw-for-content, at every level: *"All structural matching — section boundary (step 7), file groups (step 8), item headers, the nested-`<details>` strip, and the `cr-comment` marker scan (step 9) — runs on the **masked** text. Only the final extracted content (title, item body) is re-sliced from the raw blockquote-stripped text at the offsets the masked pass found, and the nested-`<details>` removal is applied to the raw slice using the offsets computed on the masked one."*

### F-7: Gate rows 4 and 8 are miscounted, and row 8's `-F` pattern can never match
**Severity:** P1
**Where:** spec § Test plan rows 4 (`:1021`) and 8 (`:1025`)
**Edge case:** Running the gate against a correct implementation of the spec.
**What happens:**
- **Row 4** expects `9` `gh api --paginate repos` occurrences and enumerates "the six converted list fetches (`:68`, `:75`, `:174`, `:194`, `:224`, `:341`) plus the 2b resume query, 6a's body query, and the 6f guard". D1 splits the `:68` site into **two** paginated fetches — `(a)` verdict determination and `(b)` the body harvest — and `(b)` is the fetch this entire ticket exists to add. The correct expected value is **10**. As pinned, a correct implementation fails the gate, and the cheapest way to satisfy `9` is to drop fetch `(b)`.
- **Row 8** expects `4` and enumerates "`:69`, `:175`, `:341`, **and D8's Phase 2 read**" — but `:341` *is* D8's Phase 2 read (D8: "6d Phase 2's verdict fetch (`:341-342`)"). There are three such sites; the value should be **3**.
- **Row 8's command is also unrunnable:** `grep -cF '\| select(.state != "COMMENTED") \| {'` uses `-F` (fixed string), where `\|` is a literal backslash-pipe. Verified: against a line containing ` | select(.state != "COMMENTED") | {id}` the `-F` pattern with backslashes returns `0` and without them returns `1`. The row returns `0` no matter what ships — it can only ever fail. (Row 14's `\|` is fine: it is `-E`, where `\|` is a literal pipe.)
**Why the spec misses it:** the row-4 enumeration counts *converted* fetches and forgets the one *added* fetch; row 8's enumeration double-names one site; and the markdown table-cell escaping of `|` leaked into a `-F` command.
**Suggested fix:** row 4 → `10`, enumerating "`:68` fetch (a), `:68` fetch (b) — the new harvest, `:75`, `:174`, `:194`, `:224`, `:341`, the 2b resume query, 6a's body query, the 6f guard". Row 8 → `3` (`:69`, `:175`, `:341`) and change the command to an `-E` form so the pipes escape legally, e.g. `grep -cE 'select\(\.state != "COMMENTED"\) \| \{'`.

### F-8: Step 2's inline and verdict fetches have no exit-status handling, and `:83` is outside the blocking clause
**Severity:** P2
**Where:** spec § Design D1 fetches (a) and (c) (`:448-464`, `:474-479`), § Decision 14 first and fifth bullets (`:401-403`, `:415-422`)
**Edge case:** A `--paginate` stream that dies on page 3 of 5 (or a total network failure) on Step 2's fetch `(c)` or `(a)`.
**What happens:** Decision 14 enumerates the fetches it governs: "a harvest **list** fetch, a single-review body fetch, the resume query, or the idempotency-guard fetch". Step 2's `(c)` (inline findings) and `(a)` (verdict) are not in that list, and D1 prescribes no `rc` capture for either — unlike D5's inline poll, which the spec explicitly wires to a file plus `rc=$?`. But `--paginate` is *new* on both: before this change they were single-request fetches where a failure was total and visible; now a partial page set "looks well-formed" (Decision 14's own words) and the round triages a subset of the PR's inline findings while `:381` reports on the remainder. That is Decision 5's failure class — findings dropped before triage — arriving through the new pagination machinery. Separately, if `(a)` and `(b)` both error, D1 says "fall through to `:83`'s no-reviews report", and Decision 14's blocking clause names only `:81` and `:381` — so a total outage is reported as the confident "No CodeRabbit reviews found".
**Why the spec misses it:** the r2-F-4 fix was scoped to "harvest" fetches because that was where `wc -l` appeared; the same partial-stream hazard now applies to every `--paginate` fetch the spec introduces.
**Suggested fix:** generalize Decision 14's first bullet to *"every `--paginate` fetch this design introduces or converts, including Step 2's verdict fetch (a) and inline fetch (c)"*, require D1's `(c)` to use Decision 7's file-capture + `rc` shape, and add `:83`'s "No CodeRabbit reviews found" to the list of affirmative early exits the blocking clause covers.

### F-9: An unresolved `$SELF` silently resets the resume window to zero and disables the guard
**Severity:** P2
**Where:** spec § Decision 12 "Author filter is load-bearing" (`:341-352`), § Design D2 step 1 (`:504`), § Design D7 (`:809`)
**Edge case:** `gh api user` fails (network blip, token scope, rate limit) or returns empty.
**What happens:** `SELF` is empty, so `select(.user.login == "")` matches no comment. The resume query yields nothing → `PRIOR_DISPOSITIONED_REVIEW_ID = 0` → the harvest re-reads the PR's entire body history (bounded to the 10 oldest) and re-triages and re-dispositions findings that were dispositioned in earlier runs. The idempotency guard also matches nothing, so the duplicate comment posts. Both failures present as normal operation: `capture` on an empty stream is documented as "safe", and Decision 14 does not classify `gh api user` as a harvest fetch.
**Why the spec misses it:** `gh api user` is treated as a setup step rather than a fetch with a failure mode; the "safe" empty-stream note for `capture` conceals it.
**Suggested fix:** add to Decision 14's first bullet and D2 step 1: *"`gh api user` is a harvest fetch. A non-zero exit or an empty `SELF` is a body harvest failure — do not proceed with an unfiltered or empty-login query; report it and end `inconclusive`."*

### F-10: CodeRabbit-supplied finding titles are quoted into the skill's own comment, so a marker string in finding text defeats the author filter
**Severity:** P2
**Where:** spec § Decision 12 "Guard"/"Author filter" (`:341-352`), § Design D7 body shape (`:829-841`)
**Edge case:** A harvested finding whose title or path contains the literal text `review-pr:body-dispositions:r<digits>`.
**What happens:** 6f writes `- \`<path>:<lines>\` — 🟡 Minor (outside-diff) — "<title>" — …` into a comment **authored by the skill**. The resume query then matches `capture("review-pr:body-dispositions:r(?<r>[0-9]+)")` anywhere in that comment body — the author filter passes, because the skill really did write it. A single injected high id closes the harvest window over every review at or below it, permanently and with no tripwire (Decision 12 itself notes "both tripwires run inside a parsed body, never on the resume"). This is not purely hypothetical: the PR shipping this change puts the marker string into `skills/review-pr/SKILL.md`, and CodeRabbit quotes changed Markdown back into finding text.
**Why the spec misses it:** Decision 12 reasons carefully about *untrusted authors* and concludes the author filter closes the hole; it does not consider that the skill launders untrusted text into its own comment. Decision 10's trust-boundary reasoning is scoped to instructions reaching triage, not to text reaching a posted comment.
**Suggested fix:** two lines in Decision 12 / D7. (1) *"Before writing a harvested title or path into the 6f body, neutralize any occurrence of `review-pr:body-dispositions:` (e.g. break the token, or wrap the title in backticks after stripping HTML comment delimiters)."* (2) *"The resume query reads the marker only from the comment's **last non-blank line**, not from anywhere in the body"* — which makes the fixed position load-bearing and matches the body shape already specified.

### F-11: A markerless 6f comment is unguarded, so every re-run re-posts it; and Decision 2's "posts no marker" disagrees with D7's post condition
**Severity:** P2
**Where:** spec § Decision 12 "Guard" (`:341-344`), § Design D7 (`:803`, `:818-819`), § Decision 2 second bullet (`:83-87`)
**Edge case:** A round where `R` is undefined — the *first* review of the harvest set failed a fetch, or an earlier round's 6f post failed.
**What happens:** D7 posts the comment "with the marker line omitted", but the idempotency guard is defined only as a search for `r<R>`. With no `R` there is nothing to search for, so the guard is a no-op: every re-run against the same PR re-triages the same items (the resume mark did not advance either) and posts another markerless disposition comment. On a PR whose oldest unhandled review is permanently 404 (deleted review), that is one duplicate comment per run, forever. Separately, Decision 2's second bullet says an all-dedup round "posts **no marker**" while D7 says 6f posts "only if the round triaged ≥1 body-level finding" — such a round triages zero, so it posts **no comment at all**; the two statements describe different behavior.
**Why the spec misses it:** the markerless path was added this round to satisfy Decision 12's invariant and the guard was not revisited for it.
**Suggested fix:** give a markerless comment a stable secondary key — e.g. `<!-- review-pr:body-dispositions:none:<lowest-unhandled-review-id> -->` — and have the guard search for whichever key this round would post. Reword Decision 2's second bullet to "posts no comment, and therefore no marker".

### F-12: D2 step 3's body-size threshold is never stated
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design D2 step 3 (`:523-530`)
**Edge case:** Any body large enough to matter — the axis r2-F-9 was raised for.
**What happens:** "If a body exceeds **a stated size**, report `body harvest: review <id> body is <n> KB — parsed from file`." No size is stated anywhere in the spec. Every other bound this design adds is a concrete number (10 reviews, 20 items, 50 ceiling, ±10 lines), so the omission reads as an unfinished sentence rather than deliberate latitude, and the size line — the one artifact that makes the size axis "degrade visibly" — fires at whatever threshold each run improvises, or never.
**Why the spec misses it:** the step was added to close r2-F-9's *mechanism* (fetch to file, read in slices) and the reporting threshold was left as a placeholder.
**Suggested fix:** name a number, e.g. *"If the file exceeds **64 KB**, report `body harvest: review <id> body is <n> KB — parsed from file in slices`"*, and state that the size line is emitted in 6e alongside the other bound lines (the 6e block at `:884-890` has no size row today).

## Summary
P0: 0 | P1: 7 | P2: 5 | P3: 0 | P4: 0

STATUS: RED P0=0 P1=7 P2=5 P3=0 P4=0
