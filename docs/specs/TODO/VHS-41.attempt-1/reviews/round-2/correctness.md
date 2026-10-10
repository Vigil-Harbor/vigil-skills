# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Step 2 fetch (a) drops `body`; infra check has no input | CLOSED | spec § Design D1, fetch `(a2)` at spec:365-368; order line spec:381-386 |
| correctness | F-2 | Section depth walk off by one | CLOSED | spec § D2 step 5, spec:456-465 (seeds at preceding `<details>`, cites body lines 8/9 and 3/4); test row 17 spec:868-873; single-group caveat spec:527-530. Line numbers re-verified against round-1's specimen dump |
| correctness | F-3 | `:381` "No new comments" never amended | CLOSED | spec § D9 "Rewritten" first bullet, spec:742-746 |
| correctness | F-4 | Decision 5 omits `:341` | CLOSED | Decision 5 says six and names `:341` (spec:120-126); D8 converts `:341-342` (spec:700-713). Verified `grep -n 'gh api'` returns exactly six list endpoints + `:172` commits + 2 POSTs + graphql |
| correctness | F-5 | `no-push` marker collides across runs | CLOSED | Decision 12 rekeys to `r<highest review id>` (spec:279-288); test row 11 pins `body-dispositions:no-push` → no match (spec:847) |
| correctness | F-6 | `:245` no-push call site | CLOSED | D4 last bullet spec:573-576; D7 spec:651-652. (See new F-4 for the round-2+ variant of this class) |
| correctness | F-7 | File-group regex matches section summary | CLOSED | D2 step 6, spec:471-477 |
| correctness | F-8 | `sync.py status` expectation false | CLOSED | Observational paragraph spec:875-880; Done-when 2 spec:902-908; removed from § Test command spec:882-891 |
| correctness | F-9 | Brief window widened | CLOSED | Decision 2 marker-resumed window spec:53-82; Decision 8 "Evidence status" marks the `COMMENTED`-nitpick claim inferred spec:200-205 |
| correctness | F-10 | `LAST_BODY_REVIEW_ID` advance undefined | CLOSED | D6 advance rule spec:627-632 |
| edge-cases | F-1 | Same as correctness F-1 | CLOSED | spec:365-368, :381-386 |
| edge-cases | F-2 | `:341-342` unpaginated | CLOSED | D8 spec:700-713 |
| edge-cases | F-3 | Tripwire structurally unreachable | CLOSED | Decision 11 two detectors spec:248-270; D2 step 10; D9 added edge cases spec:753-759 |
| edge-cases | F-4 | `no-push` marker not unique | CLOSED | Decision 12 spec:279-288 |
| edge-cases | F-5 | Full-history harvest defeats `:81` | CLOSED | Decision 2 marker resume spec:53-82; D1 spec:388-393 ("condition is on *findings*, not on the harvest set"); 2b step 2 bound of 10 |
| edge-cases | F-6 | Quoted `<details>` breaks depth walk | CLOSED | D2 step 4b spec:445-450 |
| edge-cases | F-7 | Harvest fetches have no failure handling | CLOSED | Decision 14 spec:323-342; D9 edge case spec:780-783 |
| edge-cases | F-8 | 6a body query `{id}` only; verdict-landed | CLOSED | D5 projects `{id, state, submitted_at}` and restates the rule, spec:588-607 |
| edge-cases | F-9 | Dedup before tripwire comparison | CLOSED | Decision 11 pre-dedup clause spec:257-259; D2 step 10 spec:506-508 |
| edge-cases | F-10 | Body-only fix round enters 6d Phase 2 on empty thread set | PARTIAL | D8 spec:714-721 scopes the **Phase 1** short-circuit (the poll-burn half). The suggested second half — whether Phase 2 is *entered* when Phase 1 was skipped — is still unstated; `SKILL.md:331` "Enter Phase 2 only if ALL CodeRabbit threads are resolved" is undefined with no Phase 1 observation. Pre-existing shape; stays P2 |
| edge-cases | F-11 | Guard jq errors on null comment body | CLOSED | D7 spec:657-660 `(.body // "")` |
| edge-cases | F-12 | `Unlabeled` vs nitpick default-skip | CLOSED | D3 precedence spec:541-544 |
| edge-cases | F-13 | No bound on body items per round | CLOSED | 2b step 9 spec:499-504 |
| edge-cases | F-14 | Parse cache has no re-derive fallback | CLOSED | 2b step 3 spec:428-431 |
| edge-cases | F-15 | Non-numeric line range dropped | CLOSED | 2b step 7 loose capture spec:479-486 |
| edge-cases | F-16 | Marker extraction vs `<details>` strip order | CLOSED | Decision 9 spec:219-221; 2b step 7 spec:489-491 |
| edge-cases | F-17 | Blockquote strip mangles content `>` | CLOSED | D2 step 4a spec:435-442 |
| edge-cases | F-18 | Concurrent runs both post | CLOSED | Decision 12 spec:294-296; D9 edge case spec:799-800 |
| conventions | F-1 | "No helper script" rests on false `sync.py` claim | CLOSED | Decision 13 spec:298-321. Verified `sync.py:30 SUBTREES = ("skills", "agents")` and four shipped `skills/*/scripts/` dirs (spec-close, session-handoff, talaria, hermes-kanban-awareness) |
| conventions | F-2 | Two severity-matching rules | CLOSED | D3 spec:534-548; 2b step 7 defers to D3 (spec:493-494) |
| conventions | F-3 | `AGENTS.md` § /review-pr goes stale | CLOSED | Scope row spec:29; D10 spec:808-814 |
| conventions | F-4 | Test plan drops the prose-spec gate shape | CLOSED | Rows 3-13 are commands; row 1/2 pin `0 error(s), 1 warning(s)` / `2 warning(s)` — both verified by running them. (Row 4's expected is still prose — new F-5) |
| conventions | F-5 | `sync.py status` not a gate | CLOSED | § Test command spec:882-891; verified `sync.py:155 cmd_status()` returns `None` |
| conventions | F-6 | "no test suite" claim false | CLOSED | Test plan spec:818-822; Deferred spec:941-943. Verified `python -m pytest tests/ -q` → `1 failed, 158 passed, 3 skipped` exactly as row 13 pins |
| conventions | F-7 | Section naming (`Step 2b`, `6c-body`) | CLOSED | `### 2b.` spec:397; `### 6f.` spec:639-643 |
| conventions | F-8 | Monotonic-id grounding | CLOSED | Decision 7 spec:177-180 |
| conventions | F-9 | `--body-file` path unspecified | CLOSED | D7 spec:668-673 |
| conventions | F-10 | `requires:` backlog not cited | CLOSED | Out of scope 2 spec:915-922; verified `docs/authoring-portable-skills.md:41` wording |
| conventions | F-11 | New prose must not name harness tools | CLOSED | Design preamble spec:348-352 (its *count* is wrong — new F-3) |

No REOPENED items.

## Findings

### F-1: `2b` is placed after Step 2's short-circuits, but `:81`'s new clause and D1's order line both require it to run before them
**Severity:** P1
**Where:** spec § Design D1 (spec.md:381, :388-393) vs § Design D2 (spec.md:397-398)
**Claim:** D1: *"**Order matters.** (a) → (a2) → infra-error check → (b) → 2b harvest → (c)."* and *"The `APPROVED`-and-nothing-unresolved short-circuit (`:81`) is **preserved**, with one clause added: it fires when the latest verdict is `APPROVED`, there are no unresolved inline threads, **and** the 2b harvest produced no body-level findings."* D2: *"Inserted between Step 2 and Step 3 as `### 2b. Extract body-level findings`, matching the file's existing `### 1b.` shape."*
**Why this is wrong:** Step 2 ends at `skills/review-pr/SKILL.md:83`; its three short-circuits sit at `:79` (infra error), `:81` (APPROVED), `:83` (no reviews). A `### 2b.` section "between Step 2 and Step 3" therefore executes **after** `:81`. `:81`'s amended third clause ("the 2b harvest produced no body-level findings") has no value at that point, so an implementer following D2's placement ships an APPROVED short-circuit that exits before the harvest runs — the exact Done-when-1 failure on an approved PR, and the same conflation D9 fixes for `:381`. D9 also depends on the earlier ordering: *"an `APPROVED` PR with no unresolved threads and no new body findings still short-circuits at `:81`"* (spec:794-795) is only checkable if the harvest already ran. D1's order line is the correct resolution, but D2's placement sentence is the one an implementer reads when creating the section, and nothing reconciles the two. The spec knows how to say this — D7 does it for 6f: *"after 6e's report section in file order but invoked from the same points as 6c's replies"* (spec:640-641).
**Suggested fix:** Add the same file-order/invocation-order split to D2: *"`### 2b.` is documented after Step 2 in file order, but is **invoked from inside Step 2**, after fetch (b) and before the `:79`/`:81`/`:83` short-circuits — `:81`'s harvest clause and D9's `:381` rewrite both depend on the parse having already run."* Alternatively state in D1 that Step 2's short-circuit block physically moves below the 2b invocation.

### F-2: D5 never converts `:174-175`, though Decisions 5 and 7 and test rows 5/7 all require it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design D5 (spec.md:580-619) vs § Decision 5 (spec.md:120), § Decision 7 (spec.md:156-157), § Test plan rows 5 and 7 (spec.md:841, :843)
**Claim:** Decision 5 names `:174` as one of the six list fetches that must take `--paginate`; Decision 7 names `:175` as one of three `sort_by(.submitted_at) | last` sites that go page-local; test row 5 pins `grep -cF 'sort_by(.submitted_at)'` → `0` with *"all three sites converted"*.
**Why this is wrong:** D5 is the only Design section covering 6a (`:162-215`), and it addresses only the findings poll (`:194`) plus the new body query. It ends by enumerating what stays unchanged — `:186` and `:198` — and never mentions `:174-175`, the pre-existing-approval verdict fetch. Verified: `skills/review-pr/SKILL.md:174-175` still reads `gh api repos/.../pulls/<N>/reviews --jq '[.[] | ... ] | sort_by(.submitted_at) | last | {id, state, submitted_at}'`. This is the same defect class D8 spells out for `:341` ("polls a stale page-1 verdict … silently"): on a PR with >30 reviews — routine per `SKILL.md:404` — an unpaginated `last` here can hand 6a a stale `APPROVED` and fire the `pre-existing-approval` short-circuit against the wrong verdict. Round-1 F-4 rated the identical omission P1 because the Decision was *also* wrong; here the Decisions are correct and normative, so the risk is that an implementer treating § Design as the edit list skips it and only the manual grep row 5 catches it.
**Suggested fix:** Add a bullet to D5: *"The pre-existing-approval fetch (`:174-175`) is converted to the paginated streaming form — `gh api --paginate … --jq '.[] | select(.user.login == "coderabbitai[bot]") | select(.state != "COMMENTED") | {id, state, submitted_at}'` — and the highest-`id` record is taken (Decision 7)."*

### F-3: "the file's four pre-existing bare tool names" — there are seven
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design preamble (spec.md:348-352)
**Claim:** *"The file's four pre-existing bare tool names (`:11`, `:99`, `:120`, `:200`) are out of scope and stay; they are not extended."*
**Why this is wrong:** `grep -n -E '\b(Read|Edit|Write|Bash|Grep|Glob) tool' skills/review-pr/SKILL.md` returns **seven** lines: `:11` ("Use the **Bash tool**"), `:99` ("using the Read tool"), `:120` ("using Edit tool"), `:180` ("Individual Bash tool calls do not share shell variables"), `:200`, `:316`, `:345` (all "individual Bash tool calls"). Three of the seven are inside sections this spec edits or borders (`:180` and `:200` are in 6a, which D5 rewrites; `:316`/`:345` are in 6d, which D8 amends), so the miscount understates how much surrounding prose the implementer will be reading and copying style from. The scoping intent is right; the enumeration is wrong.
**Suggested fix:** Replace the parenthetical with *"(`:11`, `:99`, `:120`, `:180`, `:200`, `:316`, `:345`)"*, or drop the count and say "the file's pre-existing bare tool names are out of scope and stay; they are not extended."

### F-4: A round-2+ cycle whose new findings are all non-fix has no 6f call site
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design D6 (spec.md:633), § Design D7 (spec.md:645-654), § Design D4 (spec.md:573-576)
**Claim:** The three call sites the spec amends are Step 5 sub-step 4 (spec:571-572), `:233`'s fix-push-loop bullet (*"The fix-push-loop bullet (`:233`) gains: post this round's 6f comment after the per-thread replies"*), and `:245`'s no-push sentence (spec:651-652).
**Why this is wrong:** `skills/review-pr/SKILL.md:233` is the *"If any are categorized as `fix`"* branch; `:241` is the other branch — *"If the incremental review has no new actionable findings (or only duplicates/already-fixed), proceed to 6d."* A reachable and likely round-2 shape is: CodeRabbit's incremental review carries a nitpick-only body, 6a counts it (`new_body_items > 0` → `new-findings`), 6b triages it, everything is skipped (nitpicks default to skip per `:113` and D3), and control leaves via `:241`. None of the three amended call sites is on that path — `:245`'s amended sentence is scoped to *"after Step 3 triage completes"*, i.e. round 1. The result is a triaged body finding whose disposition is never posted, which is the audit-trail hole the brief names in § Why it matters and what Decision 3 promises ("Each round that triaged at least one body-level finding posts exactly one PR-level comment"). This is the round-2 variant of round-1 correctness F-6; D7's own rule (*"Post once per round, only if the round triaged ≥1 body-level finding"*, spec:654) states the requirement, which is why this is P2 rather than P1.
**Suggested fix:** Add to D6: *"`:241`'s no-actionable-findings branch is amended: before proceeding to 6d, post this round's 6f comment if the cycle triaged ≥1 body-level finding."*

### F-5: Test-plan row 4 has no pinned expected value, and `:172` is a third unnamed exclusion
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 4 (spec.md:840), § Decision 5 (spec.md:122-126)
**Claim:** Row 4's Expected column is prose: *"every `gh api repos/...` **list** fetch paginated; the two `-X POST` reply calls and the single-resource `reviews/<ID>` body fetches are not list fetches and take no `--paginate`."* Decision 5: *"Two fetches are deliberately **excluded** and named so the checklist is decidable."*
**Why this is wrong:** Two problems. (a) Every other row in the checklist pins a number or "no match"; row 4 pins neither, so it is the one row a reviewer must adjudicate by eye — the shape round-1 conventions F-4 asked the spec to leave behind. (b) The exclusion list is incomplete: `skills/review-pr/SKILL.md:172` is `PUSH_TIME=$(gh api repos/<OWNER>/<REPO>/commits/$HEAD_SHA --jq '.commit.committer.date')` — a `gh api repos/…` single-resource fetch that is neither a `-X POST` reply nor a `reviews/<ID>` body fetch, and Decision 5 names only `gh api graphql` (`:290`) and `gh pr checks` (`:209`) as exclusions. A reviewer running `grep -c 'gh api repos'` gets a hit the checklist does not account for, so it is not decidable as claimed.
**Suggested fix:** Pin row 4: after the change `grep -c 'gh api --paginate repos'` = 6 (`:68`, `:75`, `:174`, `:194`, `:224`, `:341` plus the 2b resume query and the 6f guard — state the exact expected total), and `grep -c 'gh api repos'` = the named non-list set: `:172` `commits/$HEAD_SHA`, the `(a2)` verdict-body fetch, and the 2b per-review body fetch. Add `:172` to Decision 5's named exclusions.

### F-6: Checklist rows 7 and 10 already pass against the unmodified file
**Severity:** P3
**Where:** spec § Test plan rows 7 and 10 (spec.md:843, :846)
**Claim:** Row 7: `grep -cF 'select(.state != "COMMENTED")'` → *"≥ 3 (`:69`, `:175`, `:342` sites)"*. Row 10: `grep -cF 'Duplicate comments'` → *"≥ 1"*.
**Why this is wrong:** Measured on `main` today, before any edit: row 7's count is **6** and row 10's is **1**. Both thresholds are satisfied by the untouched file, so neither row can detect the regression it exists to catch (filters unified per Decision 8; Duplicate section accidentally parsed per Decision 1). Rows 5, 6, 8, 9, 11 and 12 were checked the same way and are all genuinely discriminating (current counts 3, 0, 1/2, 0, 0, 0 against expected 0, ≥2, 0/0, ≥3, no-match, 1).
**Suggested fix:** Pin row 7 to the exact post-change count (currently 6; the conversions preserve all six occurrences, so `= 6`), and give row 10 a discriminating form — e.g. `grep -nF 'Duplicate comments'` and require each hit to be a non-goal sentence, or pin the count of `not parsed`/`deliberately not` adjacent to it.

### F-7: `AGENTS.md:46` is the heading; the paragraph being amended is `:48`
**Severity:** P3
**Where:** spec § Scope row 2 (spec.md:29), § Design D10 (spec.md:808), § Out of scope 3 (spec.md:923-925)
**Claim:** *"`AGENTS.md:46` § `/review-pr` | **Change — one sentence.**"* and *"The § `/review-pr` paragraph currently describes the skill as reading findings, verifying, fixing, pushing, and posting per-thread replies. Append: …"*
**Why this is wrong:** `AGENTS.md:46` is `### /review-pr` (the heading); the paragraph whose text D10 quotes and appends to is `AGENTS.md:48`. Harmless as a section pointer, but Out of scope 3 phrases it as *"the one sentence at `AGENTS.md:46`"*, which reads as a line-level edit target.
**Suggested fix:** Cite `AGENTS.md:46-48` (§ `/review-pr`, paragraph at `:48`) in all three places.

### F-8: The `(a2)` verdict-body fetch has no guard for a PR with no verdict review
**Severity:** P3
**Where:** spec § Design D1 (spec.md:365-368, :381, :393)
**Claim:** The order is *"(a) → (a2) → infra-error check → (b) → 2b harvest → (c)"*, with `(a2)` running `gh api repos/{owner}/{repo}/pulls/<N>/reviews/<VERDICT_ID> --jq '.body'`, and *"The no-reviews case (`:83`) is unchanged."*
**Why this is wrong:** `<VERDICT_ID>` is (a)'s highest-id record. On a PR with no CodeRabbit reviews at all — the `:83` case — (a) emits nothing and `<VERDICT_ID>` is unbound, but the stated order puts `(a2)` before the `:83` check. Same for the narrower case where CodeRabbit has posted only bodiless `COMMENTED` reviews (`SKILL.md:404`): (a) is empty while (b) may not be. Today this degrades benignly (`last` on an empty array yields `null` and `:79`'s substring test falls through); with `(a2)` as a separate call it becomes an errored fetch, which Decision 14 would then classify as a harvest failure and force `inconclusive`.
**Suggested fix:** One clause in D1: *"If (a) yields no record, skip (a2) and the infra-error check and fall through to `:83`'s no-reviews report (or, if (b) yielded bodies, proceed to the harvest with no verdict)."*

### F-9: A round whose harvested items all dedup away posts no marker, so a later run re-dispositions them
**Severity:** P3
**Where:** spec § Decision 2 (spec.md:78-80), § Design D7 (spec.md:654)
**Claim:** *"A round whose harvest parses to zero items posts no marker (2b/6f post only when ≥1 body item was triaged), so the next run re-fetches and re-parses those same bodies to zero. Cheap and safe; it is not a bug."*
**Why this is worth flagging:** The stated case (parses to zero) is indeed harmless. A neighbouring case is not covered: a later round's harvest parses to items that all drop at 2b step 8's dedup (Decision 9 explicitly anticipates *"a finding restated in a later review body"*). Zero items are then *triaged*, so no 6f comment and no marker — but `LAST_BODY_REVIEW_ID` advanced only in-run. On the next run, `PRIOR_DISPOSITIONED_REVIEW_ID` falls back to the earlier round's marker, those reviews are re-harvested, their items are new to the fresh run's dedup set, and they are triaged and dispositioned a second time — a duplicate disposition line for a finding already recorded on the PR. Low harm, but it is the one case where the marker-resume window under-advances against real work.
**Suggested fix:** Extend Decision 2's first bullet: *"…and likewise a round whose items all dedup against an earlier round posts no marker; the next run may re-disposition those restatements. Recognizable via the `cr-comment` key, tolerated rather than prevented."* Or post the marker whenever the harvest set was non-empty, decoupling the marker from whether a comment was posted.

**Grounding notes (no findings):** all Design/Decision line anchors re-verified against the current `skills/review-pr/SKILL.md` (406 lines, matching spec:5) — `:61-83`, `:68`, `:69`, `:75`, `:76`, `:79`, `:81`, `:83`, `:85-115`, `:96-107`, `:109-114`, `:125-161`, `:127`, `:140-144`, `:152-158`, `:162-215`, `:174`, `:175`, `:186`, `:194`, `:195`, `:198`, `:200`, `:209`, `:215`, `:217-241`, `:224`, `:233`, `:234`, `:241`, `:245`, `:273`, `:277`, `:279`, `:281-345`, `:283`, `:290`, `:341-342`, `:351-368`, `:362`, `:370-377`, `:379-406`, `:381`, `:382`, `:397`, `:399`, `:404` all match. `git log -10 -- skills/review-pr/SKILL.md` → newest touch `5b3da4c` (2026-08-18, three weeks); `-- AGENTS.md` → newest `d381f88` (2026-09-06, two days — VHS-32's `/spec-brief` addition, which does not touch § `/review-pr` at `:46-48`). Gate rows 1, 2 and 13 executed and match exactly (`0 error(s), 1 warning(s)`; `0 error(s), 2 warning(s)` for `review-pr` + `ship-spec`; `1 failed, 158 passed, 3 skipped`). Library-API checks: `gh --version` = 2.87.3 (matches Decision 7); `gh api --slurp --jq` rejects with the exact quoted message; gh's built-in jq accepts `(?<name>…)` named captures and 2b step 1's `capture("review-pr:body-dispositions:r(?<r>[0-9]+)")` emits an empty stream (exit 0) on no match rather than erroring, so the resume query is safe on PRs with unrelated or null-bodied comments. Plane VHS-41 (`bd1504df-8bbb-4675-9f03-6dc5027b6637`, namespace `skills`) retrieved and matches the brief; its "as a reply on the review (or as one PR comment listing them)" permits the spec's Decision 3 choice, and its "forbid post-filtering … record this as a pitfall" is satisfied by D9's *Never trim a finding fetch* edge case. Both brief Done-when criteria map to spec § Done when 1 and 2.

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 4 | P4: 0

STATUS: RED P0=0 P1=1 P2=4 P3=4 P4=0
