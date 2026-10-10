# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Step 2 fetch (a) drops `body`, but the prose says the infra-error check reads the body from that record
**Severity:** P0
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Design D1, code block lines 244–250 vs. prose lines 275–278
**Claim:** The code block is annotated `# (a) VERDICT determination — unchanged semantics, page-safe form.` and projects `{id, state, submitted_at}`. Three lines below: *"The infrastructure-error check at `:79` keeps reading the **latest verdict** review's body (from (a)'s highest-id record)."*
**Why this is wrong:** The current fetch at `skills/review-pr/SKILL.md:69` projects `{id, state, submitted_at, body}` — `body` is present precisely because `:79` consumes it ("If the latest review body contains infrastructure errors — look for `"Failed to clone"`, `"🔥 Problems"`…"). D1's replacement drops `body`, so the semantics are *not* unchanged and `(a)`'s record has no field for `:79` to read. Nothing else in D1 supplies it: the single-review body fetch at spec line 266 is described as running *per review id from (b)*, i.e. the harvest set, and D1 explicitly requires the infra check to run **ahead** of the harvest ("it runs ahead of the harvest so an errored review short-circuits before the parse"). An implementer following the code block ships a skill whose infrastructure-error short-circuit has no input. Per the cross-section walk, a code block that disagrees with the surrounding prose is P0 — implementers follow code blocks.
**Suggested fix:** Either restore `body` to `(a)`'s projection (`{id, state, submitted_at, body}`) and delete the "unchanged semantics" claim's ambiguity, or state explicitly that after taking `(a)`'s highest-id record the skill runs `gh api repos/{owner}/{repo}/pulls/<N>/reviews/<THAT_ID> --jq '.body'` for the infra check, before the harvest.

---

### F-2: The section-boundary depth count is off by one — `<details>` opens on the line *before* the `<summary>`
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Design D2, step 3 (lines 301–308)
**Claim:** *"A section opens on a line matching either `<summary>[^<]*Outside diff range comments \((\d+)\)</summary>` … The section is the `<details>` block that summary opens: **from the opening line**, count `<details>` and `</details>` occurrences and end the section where the depth returns to zero."*
**Why this is wrong:** In both live specimens the section's own `<details>` sits on the *preceding* line, so starting the count at the summary line seeds depth at 0 instead of 1.

PR #28 review `5135914911` (`.body`, after `>`-stripping), verified via `gh api`:
```
 8  <details>                                              <-- section <details>, NOT counted
 9  <summary>⚠️ Outside diff range comments (1)</summary><blockquote>   <-- "opening line", depth 0
11    <details>                                            depth 1  (file group)
22      <details>                                          depth 2  (AI-prompt block)
38      </details>                                         depth 1
44    </blockquote></details>                              depth 0  <-- algorithm ends section HERE
46  </blockquote></details>                                <-- actual section end
```
petland PR #64 review `5123259707` is identical in shape (`<details>` at line 3, `<summary>🧹 Nitpick comments (1)</summary><blockquote>` at line 4, file-group close at 35, section close at 37).

The section therefore ends at the **first file group's** close. Both worked specimens have exactly one file group, so test-plan items 4 and 5 pass and the bug is invisible — but CodeRabbit groups outside-diff/nitpick items **per file**, and any review whose section spans two or more files silently loses every item after the first group. Decision 11's tripwire catches it (declared N > parsed n), so it degrades to a loud report rather than silence, but the shipped parse is wrong for the common multi-file case, which is the case this ticket exists to cover.
**Suggested fix:** In step 3, seed the depth at 1 at the summary line (equivalently: "the section's `<details>` is the line immediately preceding the summary; begin counting there"), and add a test-plan specimen with a ≥2-file-group section, or state in the specimen note that both specimens are single-group and do not exercise the boundary walk.

---

### F-3: Edge case `:381` ("No new comments → report 'Nothing to review' and exit") is never amended, and it fires in exactly the Done-when scenario
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Design D9 (lines 492–499) — the "Rewritten" list names only `:382` and `:397`
**Claim:** D9 rewrites two edge cases; § Done when item 1 asserts *"A PR whose only CodeRabbit finding is body-level … produces a triage row and a posted disposition."*
**Why this is wrong:** `skills/review-pr/SKILL.md:381` reads:
```
- **No new comments**: report "Nothing to review" and exit
```
"Comments" here means the inline-comment population from Step 2 — the exact conflation of *comment* with *finding* that this ticket exists to break. On a PR whose only finding is body-level there are zero new comments, so this edge case instructs the agent to exit before Step 2b's harvest has any effect. D1 does patch the adjacent `:81` short-circuit ("no unresolved comments now means no unresolved inline threads **and** no body-level findings"), which makes the omission of `:381` an inconsistency rather than a deliberate choice. As written the spec ships a line that contradicts its own Done-when 1.
**Suggested fix:** Add `:381` to D9's "Rewritten" list: *"No new **findings** (no inline comments and no body-level items after the Step 2b harvest): report 'Nothing to review' and exit."*

---

### F-4: Decision 5 enumerates five `gh api` fetches and omits `:341`, which Decision 7 and test items 7–8 both require converting
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Decision 5 (lines 105–107) vs. § Decision 7 (lines 130–131), § Design D8 (lines 472–479), § Test plan items 7–8 (lines 569–575)
**Claim:** Decision 5: *"`--paginate` added to all **five** `gh api` fetches (`:68`, `:75`, `:174`, `:194`, `:224`)"*. Decision 7 lists *"`--jq '… | sort_by(.submitted_at) | last'` (`:69`, `:175`, **`:342`**)"* as page-local and silently wrong. Test item 7: *"**Every** `gh api` list fetch in the file carries `--paginate`, and no `--jq` program in the file still contains `last` …"*. Test item 8 names `:342` as a verdict-filter site to check.
**Why this is wrong:** `grep -n "gh api" skills/review-pr/SKILL.md` returns six list endpoints, not five: `:68`, `:75`, `:174`, `:194`, `:224`, **`:341`** (6d Phase 2's verdict poll, `pulls/<N>/reviews`, whose `--jq` at `:342` is `'[.[] | select(…)] | sort_by(.submitted_at) | last | .state'`). Design section D8 is titled "6d (`:281-283`) and 6e (`:351-368`)" and covers only 6d's short-circuit and 6e's report lines — no design item instructs the implementer to touch `:341-342` at all. So the enumeration an implementer will follow (Decision 5 + D1–D9) leaves an aggregating `last` on an un-paginated endpoint, and test-plan item 7 — the reviewer gate the spec itself defines — then fails.

Related, same site class: `:290`'s `gh api graphql` `--jq` contains an array-wrap (`[.nodes[] | select(…)]`) at `:305`. It is manually cursor-paginated and correctly out of scope, but test item 7's wording ("every `gh api` list fetch") reads as covering it.
**Suggested fix:** Change Decision 5 to "all six `gh api` list fetches (`:68`, `:75`, `:174`, `:194`, `:224`, `:341`)"; add a D8 bullet converting `:341-342` to the paginated streaming form (`--paginate … --jq '.[] | select(…) | select(.state != "COMMENTED") | {id, state}'`, take the highest `id`); and scope test item 7 to exclude `gh api graphql` and `gh pr checks` explicitly.

---

### F-5: The `no-push` idempotency marker collides across runs, silently suppressing a later round's dispositions
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Decision 12 (lines 228–234), § Design D7 (lines 438–466)
**Claim:** *"`HEAD_SHA` is the full SHA of the commit the round's fixes landed in (or `no-push` for a round with no fixes), so genuinely distinct rounds still each get their comment."*
**Why this is wrong:** The stated conclusion does not follow for the no-push case, because `no-push` is a constant, not a per-round discriminator. Reachable sequence, all inside behavior the skill documents:

1. Run 1 on PR #N: only body-level finding is a nitpick, categorized `skip` → no push → 6c-body posts with marker `<!-- review-pr:body-dispositions:no-push -->`.
2. CodeRabbit later posts a second body-level item (`:186`/`:198` and the honesty rule at `:370-377` both exist because late reviews are normal; the skill tells the operator to re-run).
3. Operator re-runs `/review-pr` (explicitly supported — `:160`, `:400`, `:406`). The new item is skipped too → no push → the guard finds the run-1 comment carrying the identical marker and **skips the post**.

The second item's disposition is never recorded. That is precisely the audit-trail hole the brief names in § Why it matters, and it violates brief Decision 3 ("each body-level item is listed with its fix SHA or skip reason"). Nitpicks default to `skip` (`:113`), so the all-skip path is the *most* likely one for body-level findings, not a corner.
**Suggested fix:** Make the no-push marker distinguishing — e.g. `no-push@<current HEAD SHA>` (the PR head at triage time), or key the marker on the highest `review_id` in the round's harvest set (`<!-- review-pr:body-dispositions:r<LAST_BODY_REVIEW_ID> -->`), which is monotone and unique per round in both the push and no-push cases. Correct the Decision 12 sentence accordingly.

---

### F-6: The no-push call site for the 6c-body comment is asserted but never located in the flow
**Severity:** P2
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Design D4 (lines 377–380), § Design D7 (line 436)
**Claim:** D4: *"Step 5 sub-step 4 (`:140-144`): after the fix and non-fix per-thread replies, the round posts its 6c-body comment. If a round's *only* findings are body-level and all are non-fix, there is no push and no thread reply — the 6c-body comment is still posted (with `no-push` as its marker SHA)."*
**Why this is wrong:** `skills/review-pr/SKILL.md:127` gates all of Step 5 with **"Only if fixes were made:"**. Sub-step 4 (`:140-144`) is inside that gate, so amending it does not reach the no-push case. The skill already solves this problem for replies at `:245` ("If no fixes were pushed (all non-fix), non-fix replies are still posted after Step 3 triage completes") — but D7 places 6c-body "as a sub-section of 6c, immediately after the non-fix reply mechanism", i.e. in the *mechanism* description, and never amends `:245`'s call-site sentence. An implementer gets an assertion that the comment is posted with no section that posts it.
**Suggested fix:** Add to D7 (or D4) an explicit amendment of `:245`: "…non-fix replies are still posted after Step 3 triage completes, followed by this round's 6c-body comment (marker `no-push`)."

---

### F-7: The file-group regex also matches the section-summary line it is nested under
**Severity:** P2
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Design D2, step 4 (lines 310–312)
**Claim:** *"Inside a section, a nested `<summary>(?<path>[^<]+?) \((?<n>\d+)\)</summary>` opens a per-file group."*
**Why this is wrong:** The section summary itself satisfies that pattern. Verified on PR #28 `5135914911` line 9: `<summary>⚠️ Outside diff range comments (1)</summary><blockquote>` → `path = "⚠️ Outside diff range comments"`, `n = 1`. Same on petland `5123259707` line 4 for `🧹 Nitpick comments (1)`. Step 3 defines the section as beginning *at* that line ("from the opening line"), and step 4 says to scan "inside a section" — so a literal reading creates a phantom file group whose `path` is the section title, and every subsequent item is attributed to it. A careful reader unravels this from step 3's intent, which is why it is P2 rather than P0, but the two rules as stated overlap.
**Suggested fix:** In step 4, say the file-group scan starts on the **line after** the section summary; or disambiguate the group regex with a path shape guard (e.g. require `path` to contain `/` or `.`, or to not match the two section phrases).

---

### F-8: Test-plan item 3's `sync.py status` expectation is false against the current baseline
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Test plan item 3 (lines 545–546), § Done when item 2 (lines 601–602)
**Claim:** *"`python sync.py status` — must show `skills/review-pr/SKILL.md` as the **only** difference against `~/.claude/`, and nothing else unexpected."* Done-when 2 restates it as *"`sync.py status` clean."*
**Why this is wrong:** Measured now, on `main`, at `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills`:
- `python sync.py status` emits **1674 rows, all `[ dst-only]`** (agentcraft-guide, app-setup, codex, higgsfield, huashu-design and their `.git` trees, etc.). It is nowhere near "clean" today and will not be after this change.
- `skills/review-pr/SKILL.md` appears in **zero** rows — the installed copy is currently in sync — so it is not a pre-existing difference either.
- `python sync.py status` exits **0** regardless, and `python lint.py --strict` exits **0**, so the § Test command chain does pass. The automated gate is fine; the *stated criterion* is not verifiable as written and will read as a failure to whoever runs it.

Also confirms the surrounding claims are accurate: `python lint.py skills/review-pr/SKILL.md --strict` → `0 error(s), 1 warning(s)`, `WARN [missing-requires] line 1`, exit 0; `AGENTS.md:7` does say "no build step, no test suite".
**Suggested fix:** Reword item 3 to what is actually checkable: *"`python sync.py status` exits 0, and `skills/review-pr/SKILL.md` is the only **`src`/content** difference introduced by this change; the ~1674 pre-existing `dst-only` rows for locally installed, unmirrored skills are unrelated and unchanged."* Soften Done-when 2 to match (the brief and Plane ticket both say "clean", so note the reconciliation rather than silently diverging).

---

### F-9: Decision 2 widens the brief's "verdict review" to "body-carrying review" and to *every* review in Step 2
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Decision 2 (lines 51–72), § Decision 8 (lines 151–169)
**Claim:** Spec Decision 2: *"Step 2 harvests the body of **every** body-carrying CodeRabbit review on the PR."*
**Why this is worth flagging:** Brief § Decisions carried forward item 2 (and the Plane ticket, retrieved from namespace `skills`, record `bd1504df-8bbb-4675-9f03-6dc5027b6637`) reads *"Every newer **verdict** review's body is read — in Step 2 and in each 6a/6b cycle, the body of every **verdict** review **newer than the last one handled**."* The spec changes both the selector (verdict → non-empty body) and, for Step 2, the window (newer-than → all). Both changes are argued with rationale (Decision 8's filter split is well grounded — I verified PR #28's acknowledgement reviews `5135919676`, `5135923847`, `5135925406` and the `APPROVED` `5135992754` all have `body` length 0, so the non-empty-body test does exclude them), and both make the harvest a superset, so the brief's intent is served. Recording it only so the operator sees the brief decision was consciously widened, not drifted.

One sub-claim is asserted rather than observed: *"a review carrying only nitpicks can be submitted with state `COMMENTED` and a non-empty body."* Neither cited specimen shows this — petland `5123259707` carries its nitpick section on a `CHANGES_REQUESTED` review. The design is safe either way; the justification is speculative.
**Suggested fix:** Add one line to Decision 2 noting the deliberate widening relative to the brief; mark the `COMMENTED`-nitpick-review claim as inferred rather than verified, or cite a specimen.

---

### F-10: `LAST_BODY_REVIEW_ID`'s advance rule is undefined for a round that parsed no bodies
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-41.spec.md` § Design D6 (lines 419–423)
**Claim:** *"After triage, advance `LAST_BODY_REVIEW_ID` to the highest id parsed, exactly as `PREV_REVIEW_ID` is advanced at `:215`."*
**Why this is wrong:** A cycle can reach 6b on `new_inline > 0` with `new_body_items == 0` (D5's first outcome rule sums the two). In that round no body was parsed, so "the highest id parsed" has no value and the advance is a no-op with no stated semantics. The consequence is benign — the next 6a re-matches the same body-carrying reviews, the per-run parse cache (D2 step 1) prevents re-parsing, and Decision 9's key dedup prevents re-triage — but the rule as stated has an undefined branch. The `:215` analogy does not carry over: `PREV_REVIEW_ID` always has a review just triaged.
**Suggested fix:** State it as "advance `LAST_BODY_REVIEW_ID` to the highest id **in the round's harvest set** (whether or not it parsed to items); leave it unchanged if the harvest set was empty."

---

**Grounding notes (no findings):** all 33 line anchors in the spec verified against `skills/review-pr/SKILL.md` — every one matches, and the file is exactly 406 lines as the spec states. `git log -10 -- skills/review-pr/SKILL.md` shows the most recent touch as `5b3da4c` on 2026-08-18, three weeks old — nothing landed in the last 7 days. Live-specimen claims all check out: PR #28 `5135914911` yields exactly one item (`skills/grilling/SKILL.md`, `171-171`, `_🟡 Minor_`, title *List all unverified-check outcomes in the failure modes.*, key `v1:80d76a9c27d4add3fdeb6bb9`, declared count 1, `> [!CAUTION]`-blockquoted); petland #64 `5123259707` yields exactly one nitpick item (`rosa-tests/probe.mjs`, `376-376`, `_🔵 Trivial_`, key `v1:f1a62d5b1a96778a982c2667`, **not** blockquoted); PR #28 `5135878266` has no harvestable section and its top-level `🤖 Prompt for all review comments with AI agents` block does list two inline findings. `gh version 2.87.3` matches Decision 7, and `gh api … --slurp --jq` rejects with the exact message quoted: `the --slurp option is not supported with --jq or --template`.

## Summary
P0: 1 | P1: 4 | P2: 3 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=4 P2=3 P3=2 P4=0
