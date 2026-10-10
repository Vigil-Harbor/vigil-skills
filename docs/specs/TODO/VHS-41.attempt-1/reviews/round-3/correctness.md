# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | 2b placed after Step 2's short-circuits | CLOSED | spec § D1 lines 467-471 ("documented after Step 2 in file order but **invoked from inside Step 2**"); § D2 line 497-498 carries the split. One residual slip in the same sentence → new F-5 |
| correctness | F-2 (P2) | D5 never converts `:174-175` | CLOSED | § D5 opening bullet, spec:708-716. Verified `SKILL.md:174-175` is still the unpaginated `sort_by\|last` form |
| correctness | F-3 (P2) | "four bare tool names", actually seven | CLOSED | § Design preamble spec:433-438 lists `:11,:99,:120,:180,:200,:316,:345`; `grep -nE '\b(Read\|Edit\|Write\|Bash\|Grep\|Glob) tool'` returns exactly those seven |
| correctness | F-4 (P2) | `:241` branch has no 6f call site | CLOSED | § D6 "Both exit branches post 6f" spec:775-782; § D7 generalizes `:245` spec:799-801. Verified `SKILL.md:233`/`:241`/`:245` are the quoted lines |
| correctness | F-5 (P2) | row 4 unpinned; `:172` unnamed | CLOSED | Decision 5 names `:172`/`:290`/`:209` (spec:133-136); rows 4 and 5 now carry Pre/Expected numbers. The *value* pinned in row 4 is wrong → new F-2 |
| correctness | F-6 (P3) | rows 7 and 10 pass pre-change | CLOSED | Pre column added (spec:1014-1016); old row 7 → new row 8 pinned on the converted jq shape, old row 10 → new row 11 with non-goal wording. All 13 Pre values re-measured against unmodified `main` and each one matches. Two new defects in the replacement rows → F-2, F-8 |
| correctness | F-7 (P3) | `AGENTS.md:46` is the heading | CLOSED | spec:28 (`:46-48`, paragraph at `:48`), spec:985 (`:48`), spec:1123 (`:48`, `:7`). Verified `AGENTS.md:46` = `### /review-pr`, `:47` blank, `:48` the paragraph, `:7` the "no test suite" blurb |
| correctness | F-8 (P3) | `(a2)` has no guard when (a) is empty | CLOSED | § D1 "If (a) yields no record" spec:473-479 |
| correctness | F-9 (P3) | dedup-to-zero round posts no marker | CLOSED | Decision 2 second bullet spec:82-87. The rule it states creates a new liveness hole in the bounded case → new F-3 |
| edge-cases | F-1 (P1) | marker advances past unhandled reviews | CLOSED | Decision 12 contiguity rule spec:303-339; oldest-first bound spec:513-521; 6e wording `grouped (not individually triaged)` spec:890. Its supporting claim at spec:336 is false in one case → new F-3 |
| edge-cases | F-2 (P1) | failed harvest exits "Nothing to review" | CLOSED | Decision 14 bullet spec:414-422; mirrored into § D1 spec:488-491 and § D9 spec:901-905, 944-947 |
| edge-cases | F-3 (P1) | one blockquote depth per body | CLOSED | § D2 step 6 "Normalize PER SECTION" spec:551-568; § D9 edge case spec:920-922; test 22. Residual ordering circularity → new F-7 |
| edge-cases | F-4 (P1) | `\| wc -l` swallows exit status | CLOSED | Decision 7 file-capture shape spec:184-200; § D5 spec:719-726; § D9 spec:952-954. Its grep row cannot detect the antipattern → new F-8 |
| edge-cases | F-5 (P2) | resume/guard trust any author | PARTIAL | The author filter is specified (spec:504-506, 806-811, row 13) but the prescribed command is not a valid `gh` invocation, so neither query runs → new F-1. Keeps P2 until the mechanism works |
| edge-cases | F-6 (P2) | 6f not invoked on all-non-fix round | CLOSED | § D6 spec:775-782; § D7 spec:799-801 |
| edge-cases | F-7 (P2) | test plan verifies the happy parse only | CLOSED | tests 17-23 add tripwire-silence assertions, a synthetic code-mask body (21), a both-sections body (22), and a forced harvest failure (23) |
| edge-cases | F-8 (P2) | masked vs raw text handed to triage | CLOSED | § D2 step 6 "The masked text computes boundaries only" spec:570-576 |
| edge-cases | F-9 (P2) | bodies bounded by count, not size | CLOSED | § D2 step 3 file capture + size report spec:523-530 |
| edge-cases | F-10 (P3) | outside-diff side unbounded; "deferred" wording | CLOSED | § D2 step 11 hard ceiling of 50 spec:616-626; 6e line spec:890 |
| edge-cases | F-11 (P3) | phrase tripwire scope ambiguous | CLOSED | Decision 11 "evaluated per phrase, on masked text" spec:285-293. The masked artifact it names is no longer produced → new F-6 |
| conventions | F-1 (P2) | Decision 5 exclusion list incomplete | CLOSED | spec:133 adds `:172`; verified `SKILL.md:172` is the `commits/$HEAD_SHA` fetch |
| conventions | F-2 (P2) | three rows cannot fail | CLOSED | Pre column; re-pinned rows. See F-2/F-8 for the new value/command errors |
| conventions | F-3 (P2) | bare-tool-name undercount | CLOSED | spec:433-438 |
| conventions | F-4 (P2) | § Deferred departs from convention | CLOSED | spec:1137-1146 — one bullet, "Filed as VHS-42, 2026-09-08, Backlog"; VHS-42 retrieved from Plane (`07ba5525…`, backlog, created 2026-09-08). The round-1-P3 accounting bullet is gone |
| conventions | F-5 (P3) | D3 widens the inline severity rule | CLOSED | § D3 "This is a spec-level widening beyond the brief" spec:663-669 |
| conventions | F-6 (P3) | `AGENTS.md:7` known-false claim deferred | CLOSED | § D10 second bullet spec:989-993; Scope row spec:29 |
| conventions | F-7 (P3) | VHS-29's rejection of fence-masking | CLOSED | Decision 13 spec:380-391 |
| conventions | F-8 (P4) | `AGENTS.md:46` anchor | CLOSED | same as correctness F-7 |

No REOPENED items.

## Findings

### F-1: Both new comment queries use `gh api --jq --arg`, which is not a valid `gh` invocation
**Severity:** P1
**Where:** spec § D2 step 1 (spec.md:505-506); § D7 idempotency guard (spec.md:810-811)
**Claim:**
```bash
gh api --paginate repos/{owner}/{repo}/issues/<N>/comments \
  --jq --arg self "$SELF" '.[] | select(.user.login == $self) | (.body // "") | capture("review-pr:body-dispositions:r(?<r>[0-9]+)") | .r'
```
and the identical `--jq --arg self "$SELF" '…'` shape in the 6f guard.
**Why this is wrong:** `gh api` has no `--arg` flag. `gh api --help` on the pinned version (2.87.3, the version Decision 7 itself cites) lists only `--cache, -F/--field, -H/--header, --hostname, -i/--include, --input, -q/--jq, -X/--method, --paginate, -p/--preview, -f/--raw-field, --silent, --slurp, -t/--template, --verbose`. `-q/--jq` takes exactly one string. Run against the real binary:

```
$ gh api --jq --arg self "zzz" '.[] | select(.x == $self)' repos/cli/cli/labels
accepts 1 arg(s), received 4
```

`--jq` swallows `--arg`, and `self`, `$SELF` and the jq program become three extra positional arguments. Both commands abort before any request. The blast radius is total, because Decision 14 (spec:400-403) classifies exactly these two fetches as harvest failures: the resume query fails → harvest failure stands → `:81` and `:381` are blocked (spec:414-422), `REVIEW_SIGNAL` is forced to `inconclusive` (spec:410-413), and the 6f guard fails → **fail closed, do not post** (spec:423-425). Every run of the changed skill would end `inconclusive` with no disposition comment ever posted — Done-when 1 is unreachable. This is new in round 3: the `--arg` form was introduced as the fix for edge-cases r2-F-5.
**Suggested fix:** interpolate the login in the shell instead of passing a jq variable, e.g.
`--jq ".[] | select(.user.login == \"$SELF\") | (.body // \"\") | capture(\"review-pr:body-dispositions:r(?<r>[0-9]+)\") | .r"`, or keep single quotes and read it from the environment with gojq's `env` (`SELF=$SELF gh api … --jq '… select(.user.login == env.SELF) …'`). Apply the same change at spec:811, and re-word test row 13 (`grep -c 'select(.user.login == $self)'` → `2`) to match whichever form is chosen — as written that row pins the broken shape.

### F-2: Test rows 4 and 8 pin counts that a correct implementation cannot produce
**Severity:** P1
**Where:** spec § Test plan row 4 (spec.md:1021), row 8 (spec.md:1025); § Decision 5 (spec.md:124-127)
**Claim:** Row 4: `grep -c 'gh api --paginate repos'` → `9` — *"the six converted list fetches (`:68`, `:75`, `:174`, `:194`, `:224`, `:341`) plus the 2b resume query, 6a's body query, and the 6f guard"*. Row 8: `grep -cF '… select(.state != "COMMENTED") … {'` → `4` — *"the streaming verdict form at `:69`, `:175`, `:341`, and D8's Phase 2 read"*.
**Why this is wrong:** Both enumerations are arithmetically wrong against the spec's own § Design.

*Row 4 undercounts by one.* § D1 (spec:444-465) declares **four** Step 2 fetches, three of which are `gh api --paginate repos…`: `(a)` (replaces `:68`), `(b)` — the body-harvest list fetch, which is **new**, not a conversion of anything — and `(c)` (replaces `:75`). Row 4's list accounts for `(a)` and `(c)` only; `(b)` appears in neither the "six converted" half nor the three named new ones. The post-change total is **10**: `(a)`, `(b)`, `(c)`, 2b resume, D5's converted `:174`, D5's converted `:194`, D5's new body query, D6's converted `:224`, D8's converted `:341`, D7's guard. Decision 5 has the mirror-image gap — *"plus the new harvest, resume, and idempotency-guard fetches"* names three new fetches and omits **6a's body query**, while row 4 names three new fetches and omits **Step 2 `(b)`**. Neither list is complete, and they are not the same list.

*Row 8 overcounts by one.* `:341` **is** D8's Phase 2 read — verified: `SKILL.md:341-342` is the 6d Phase 2 verdict fetch, and § D8's first bullet (spec:855-862) is the conversion of it. There are exactly three sites carrying the verdict filter in a jq program (`:69`, `:175`, `:341`; confirmed by `grep -cF 'select(.state != "COMMENTED")'` = 6 = three jq sites + three prose mentions at `:65`, `:339`, `:404`), so the converted form appears **3** times, not 4.

Both rows are gate rows the round-2 reviews specifically asked to be pinned; `/ship-spec` iterates its test gate up to five times, so a wrong pin either burns iterations or pushes the implementer to delete a fetch / unify a filter to make the number match — the exact regressions rows 4 and 8 exist to prevent.
**Suggested fix:** row 4 → `10`, and list all ten sites explicitly (adding Step 2 `(b)`). Row 8 → `3`, listing `:69`, `:175`, `:341` only. Add 6a's body query to Decision 5's "plus the new …" enumeration so the two lists agree.

### F-3: Decision 12's "the next run picks up the newer ones" is false when a bounded round posts no comment
**Severity:** P1
**Where:** spec § Decision 12 (spec.md:334-336); § Decision 2 (spec.md:79-89); § D2 step 2 (spec.md:513-521)
**Claim:** *"**The harvest-set bound takes the OLDEST unhandled reviews, not the newest** (2b step 2), so the handled prefix is contiguous and `R` advances by exactly what was handled. The next run picks up the newer ones."*
**Why this is wrong:** The marker only exists inside a 6f comment, and 6f posts *"only if the round triaged ≥1 body-level finding"* (spec:803) — Decision 2 states this twice as a deliberate consequence (spec:79-87). Combine that with the oldest-first bound and there is a reachable state with **no forward progress at all**:

- First run against a PR with, say, 15 unhandled body-carrying reviews. 2b step 2 parses the **10 oldest** and defers 5.
- All 10 parse to zero surviving items — routine, since a body-carrying review whose body is only the walkthrough plus the top-level AI-prompt block parses to zero; the spec's own specimen `5135878266` is exactly that shape (spec:940-941, test 19).
- Zero items triaged → no 6f comment → **no marker**. `PRIOR_DISPOSITIONED_REVIEW_ID` stays `0`.
- Nothing was fixed, so 6a never runs (`SKILL.md:162-163`: 6a is entered only if fixes were pushed), and the in-run `LAST_BODY_REVIEW_ID` advance is discarded at end of run.
- The next run recomputes the identical harvest set, parses the identical 10 oldest, and defers the identical 5. Reviews 11-15 — which may carry the Critical/Major outside-diff items this ticket exists to surface — are **never reachable on any run**.

This is the "permanently unharvestable" failure edge-cases r2-F-1 was raised about, re-created by round 3's own closure of correctness r2-F-9. Decision 12's invariant (spec:318-320) still holds — nothing false is claimed as handled — but the liveness claim at spec:336 does not, and the operator instruction at spec:517 (`deferred <id, id, …> — re-run to pick these up`) plus the 6e line at spec:889 (`re-run to pick up`) both give advice that cannot work in this state. Decision 2 rejects the obvious remedy on a false premise: *"the alternative — advancing the marker on a round that posted nothing — breaks Decision 12's invariant"*. It does not. A review that was **fetched successfully, parsed, and had all its (zero) surviving items handled** satisfies Decision 12's own definition of the leading run verbatim; the only thing missing is a comment to carry the marker.
**Suggested fix:** decouple the marker from the disposition list. Either (a) when the round's harvest set was non-empty and its leading run is non-empty but nothing was triaged, post a marker-only comment (`No body-level findings in reviews <ids>.` plus the marker), or (b) when the harvest-set bound deferred reviews, always post the comment so the marker lands. State in Decision 2 that a parse-to-zero prefix **is** handled for marker purposes, and correct spec:336, spec:517 and spec:889 accordingly.

### F-4: `verdict-landed` is decided from the body-carrying stream, but Decision 8 verifies the `APPROVED` review carries no body
**Severity:** P1
**Where:** spec § D5 (spec.md:728-732, :739-748) vs § Decision 8 (spec.md:218-223)
**Claim:** D5's second poll query is
```bash
gh api --paginate … /reviews --jq '.[] | select(.user.login == "coderabbitai[bot]") | select((.body // "") != "") | select(.id > <LAST_BODY_REVIEW_ID>) | {id, state, submitted_at}'
```
with the inline comment *"`state` and `submitted_at` are projected because the verdict-landed rule below needs both (edge-cases r1-F-8) — `{id}` alone makes that test undecidable"*, and the rule *"Both counts 0 **and** a review satisfying `state != "COMMENTED"` **and** `submitted_at > PUSH_TIME` has landed → `REVIEW_SIGNAL=verdict-landed`"*.
**Why this is wrong:** The spec pins the verdict-landed test to a stream that is filtered to **non-empty bodies**, and Decision 8 states as verified fact that the success-case verdict has an empty body: *"the empty acknowledgement reviews — verified `body` length `0` on PR #28 reviews `5135919676`, `5135923847`, `5135925406`, **and on the `APPROVED` review `5135992754`** — are excluded by the non-empty-body test just as effectively."* An `APPROVED` review that lands after the push is therefore invisible to the only query D5 gives the test, so the "both counts 0 + verdict landed" branch can never fire on that shape. Every otherwise-clean round falls through to *"Both counts stay 0 for all attempts → `REVIEW_SIGNAL=inconclusive`"*, and 6e's honesty rule (`SKILL.md:370-377`) then prints "polling ended before CodeRabbit posted a verdict … re-run `/review-pr`" on a PR that is in fact approved. The spec's own justification for the non-empty-body filter (Decision 8: it *excludes* the `APPROVED` review) is the thing that breaks the verdict test built on top of it. Decision 8 is right that harvest and verdict need **different** filters; D5 gave the verdict test the harvest filter.
**Suggested fix:** add a third streaming query to D5 using the verdict filter — `--jq '.[] | select(.user.login == "coderabbitai[bot]") | select(.state != "COMMENTED") | {id, state, submitted_at}'` — and state that the `verdict-landed` test reads the **highest-id record of that** stream, while the body-carrying stream supplies only `new_body_items`. Keep the existing guard ("a body-carrying `COMMENTED` review that parsed to zero items must not set `verdict-landed`") — it follows from `state != "COMMENTED"` on the verdict stream anyway. Note that this adds a fourth `gh api --paginate repos` site, so row 4's expected count (F-2) becomes 11.

### F-5: D1's invocation-order sentence contradicts D1's own order line about `:79`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D1 (spec.md:467-471, :481-484)
**Claim:** *"**Order matters.** (a) → (a2) → infra-error check → (b) → **2b harvest** → (c) → then Step 2's short-circuit block. The `### 2b.` section is documented after Step 2 in file order but is **invoked from inside Step 2**, before `:79`/`:81`/`:83`."*
**Why this is wrong:** `SKILL.md:79` **is** the infrastructure-error check ("If the latest review body contains infrastructure errors … and stop"), and the order line two clauses earlier places it *before* the harvest, not after. The paragraph fourteen lines down says so a third time: *"The infrastructure-error check at `:79` runs on (a2)'s body and short-circuits before the harvest, so an errored review never reaches the parse"* (spec:481-484). So one sentence in the same paragraph asserts the opposite of the other two. An implementer who follows the "before `:79`" wording runs the parse on an errored review body, which the spec explicitly forbids — and which can fire the Decision 11 phrase tripwire on a `🔥 Problems` body as noise.
**Suggested fix:** change spec:469 to *"…invoked from inside Step 2, after the `:79` infra-error check and **before** `:81`/`:83`."*

### F-6: Decision 11's phrase tripwire runs on a "code-masked body" that D2 step 6 no longer produces
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 11 (spec.md:285-293) vs § D2 step 6 (spec.md:551-568) and step 12 (spec.md:628-630)
**Claim:** Decision 11: *"For each of the two phrases independently: if the **blockquote-stripped, code-masked body** contains `outside diff range` or `nitpick comments` (case-insensitive) and **that phrase's own section** did not match, fire the tripwire."* Step 12: *"Run both detectors of Decision 11 … and report per Decision 11."*
**Why this is wrong:** Round 3 moved normalization from body-scope to section-scope — step 6 now strips and masks *"for each section found in step 5, over that section's span only"*. No step produces a blockquote-stripped, code-masked **body**. And the phrase tripwire's whole trigger condition is *"that phrase's own section did not match"* — i.e. the case where there is no section, hence no span, hence nothing normalized for the detector to read. The one detector designed to survive CodeRabbit format drift references an artifact that exists only when the drift did *not* happen. Test 19 (spec:1046-1052) then asserts "a phrase tripwire firing here means the per-phrase / post-mask scoping … was not implemented", so the test presumes an input text the procedure never defines. An implementer will either run the phrase test on raw text — reviving the false-positive risk from a quoted code sample, which spec:291-293 says *"matters immediately"* because this very change puts both phrases into `SKILL.md` — or invent a body-wide mask the spec forbids elsewhere.
**Suggested fix:** add one sentence to step 6 or step 12: *"For the phrase tripwire only, additionally compute a body-wide masked view — fenced blocks and inline-code spans masked, no blockquote stripping (the phrase test is depth-insensitive) — and run the two phrase tests against that view."* Reference it from Decision 11 so both sites name the same artifact.

### F-7: D2 step 6's "over that section's span only" is circular — the span's end is computed in step 7
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D2 step 5 (spec.md:539-549), step 6 (spec.md:551-568), step 7 (spec.md:577-585)
**Claim:** Step 5 locates sections on raw text by the `<summary>` regex. Step 6: *"So, for each section found in step 5, **over that section's span only**: a. read the blockquote depth at the section's `<summary>` line and strip … b. mask fenced code blocks … and inline-code spans."* Step 7: *"Begin the depth walk at that preceding `<details>` line, counting `<details>` and `</details>` **in the masked text**, and end the section where depth returns to zero."*
**Why this is wrong:** Step 5 yields only the section's *start* (the summary line, and by step 7 the `<details>` line before it). The section's *end* is what step 7's depth walk computes — from the masked text step 6 is supposed to have already produced over "that section's span". Step 6 therefore needs an output of step 7 as its input. This is the same circularity edge-cases r2-F-3 raised against the old step 4a ("step 4a needs 'the section's opening line', which step 5 computes"); relocating the normalization moved the circle rather than opening it. It matters concretely: the naive resolution — normalize from the section start to end-of-body — re-creates the exact defect step 6 exists to fix, because a body carrying an Outside-diff section (depth 1) followed by a Nitpick section (depth 0) would have the nitpick section stripped at depth 1.
**Suggested fix:** define a provisional span in step 5: *"Each section's provisional span runs from the `<details>` line preceding its summary to the line before the next section's `<details>` line, or to the end of the body for the last section. Step 6 normalizes that provisional span; step 7's depth walk narrows it to the true end."*

### F-8: Two checklist commands cannot match anything as written — one is escaped for the markdown table, the other's regex has no newline class
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 8 (spec.md:1025), row 14 (spec.md:1031)
**Claim:** Row 8: `grep -cF '\| select(.state != "COMMENTED") \| {' skills/review-pr/SKILL.md`. Row 14: `grep -cE 'gh api --paginate[^\n]*\| *wc -l' skills/review-pr/SKILL.md` → `0` → `0`, *"no fetch is piped straight into an aggregate (Decision 7)"*.
**Why this is wrong:** (a) Row 8 uses `-F` (fixed string), so the markdown pipe escapes `\|` are searched **literally**. The pattern can never match the shipped file; measured, the escaped form and the unescaped form both return `0` today, and only the unescaped form will return anything after the change. Every other `-F` row in the table has an unescaped pattern, so this one row silently ships an un-runnable command. (b) Row 14's `[^\n]` is not a newline negation — POSIX/GNU bracket expressions do not honour `\n`, so it reads as "any character except backslash and `n`", and `gh api --paginate` … `wc -l` always contains an `n`. Verified against a synthetic line containing the exact antipattern:

```
$ printf 'gh api --paginate repos/o/r/pulls/1/comments --jq %s .id %s | wc -l\n' "'" "'" > t14.txt
$ grep -cE 'gh api --paginate[^\n]*\| *wc -l' t14.txt   →  0
$ grep -cE 'gh api --paginate.*\| *wc -l' t14.txt       →  1
```

Row 14 is the only mechanical guard on Decision 7's most load-bearing rule (edge-cases r2-F-4, P1: "never pipe a fetch straight into an aggregate"), and it returns `0` whether or not the antipattern is present.
**Suggested fix:** row 8 → `grep -cF '| select(.state != "COMMENTED") | {' skills/review-pr/SKILL.md` (and see F-2 for its expected value). Row 14 → `grep -cE 'gh api --paginate.*\| *(wc|jq)' skills/review-pr/SKILL.md`. Since the table forces pipe escaping, add a note under the table that `\|` in a command cell is table escaping and must be typed as `|`.

### F-9: An undefined `R` leaves the 6f comment with no marker, so the idempotency guard has nothing to match
**Severity:** P3
**Where:** spec § D7 (spec.md:818-819); § Decision 12 (spec.md:341-344)
**Claim:** *"`<R>` is computed by Decision 12's contiguity rule; if it is undefined, the comment is posted with the marker line omitted."* The guard: *"skip the post only if one already carries this exact marker."*
**Why this is worth flagging:** Decision 12 reaches "undefined `R`" whenever the *first* review in the round's ascending harvest set failed its fetch or its parse — the case a re-run is explicitly prescribed for. That round posts a real disposition comment with no marker; on re-run the guard finds no marker, and (assuming the same items re-triage) posts a second, textually near-identical comment. Decision 12 names the concurrent-run duplicate as tolerated *"because the marker makes the duplicate recognizable"* — here there is no marker to make it recognizable.
**Suggested fix:** when `R` is undefined, still emit a distinguishing marker that claims nothing, e.g. `<!-- review-pr:body-dispositions:r0 -->` (a `0` marker is already the "never posted" sentinel for the resume query at spec:509, so it cannot advance the window) — or state in D7 that the marker-less comment is knowingly re-postable and say so in the comment body.

**Grounding notes (no findings):** spec and brief re-read from disk; `AGENTS.md`, project + global `CLAUDE.md`, and all three round-2 reports read. Plane VHS-41 retrieved (`bd1504df-8bbb-4675-9f03-6dc5027b6637`, namespace `skills`, tag-exact) and matches the brief; both its Done-when clauses map to spec § Done when 1 and 2. VHS-42 retrieved and confirmed (`07ba5525-bd27-4dac-863f-b6335d7f484a`, backlog, created 2026-09-08), closing conventions r2-F-4. `skills/review-pr/SKILL.md` is 406 lines, matching spec:5; every anchor the spec cites was re-verified individually — all match. `AGENTS.md:7`, `:46`, `:48` verified. `git log` — `skills/review-pr/SKILL.md` newest touch `5b3da4c` (2026-08-18, three weeks); `AGENTS.md` newest `d381f88` (2026-09-06, two days — VHS-32, which does not touch § `/review-pr` and does not shift `:7`/`:48`). Gate rows 1, 2 and 16 executed and match exactly (`0 error(s), 1 warning(s)`; `0 error(s), 2 warning(s)` = review-pr + ship-spec; `1 failed, 158 passed, 3 skipped`, failure `test_lint.py::TestLint::test_shipped_skills_clean`). **Every "Pre" value in the rebuilt grep checklist was measured against unmodified `main` and every one is correct** — row 4 `0`, row 5 `7`, row 6 `3`, row 7 `0`, row 8 `0` (both escaped and unescaped forms), row 9 `1`/`2`, row 10 `0`, row 11 `1`, row 12 no match, row 13 `0`, row 14 `0`, row 15 `0`/`1`, row 16 as pinned. Library-API checks: `gh --version` = 2.87.3, matching Decision 7; `gh api` flag list confirms `--slurp` exists and `--arg` does not (F-1); `$TMPDIR` is set (`/tmp`) in this Git Bash, so D5/D2's `"$TMPDIR/…"` paths resolve here.

## Summary
P0: 0 | P1: 4 | P2: 4 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=4 P2=4 P3=1 P4=0
