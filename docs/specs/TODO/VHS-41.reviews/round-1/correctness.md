# Correctness Review — round 1

## Closure of round <N-1> findings

Round 1 of a fresh run (attempt 2). Per the orchestrator's `closure_manifest`, the five attempt-1 round-4 P0/P1 dispositions were verified against the current spec:

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `r0` sentinel makes the 6f guard a constant key | CLOSED | Marker is `r<R>:h<HEX>` at spec:353; digest defined 355-360; guard demands both at spec:419-433 and the jq exact-match at spec:1040; digest computation at spec:1053-1064; D9 "Two `r0` rounds in one run" at spec:1263-1270; test row 25 at spec:1357 (verified Pre `0` on `main`) |
| edge-cases | F-1 | `; rc=$?` makes a failed fetch indistinguishable from a small one | CLOSED | Canonical block spec:215-219 prints exactly one of `HARVEST_FAILURE rc=<n>` / `COUNT=<n>`; rationale spec:221-231; applied at D1 fetch (c) spec:586-590 and D5 inline poll spec:911-915; D9 bullet spec:1237-1242; test row 24 spec:1356 (Pre `0` verified) |
| edge-cases | F-2 | `export SELF` → `env.SELF` resolves to `null` across Bash calls | CLOSED | Literal `"<SELF>"` substitution at D2 step 1 spec:638-654 and D7 guard spec:1037-1040; Decision 14 bullet spec:515-521; test rows 13 (spec:1352) and 26 (spec:1358). Verified independently: `gh api --jq --arg self x '<endpoint>'` fails with `accepts 1 arg(s), received 3` before any request |
| edge-cases | F-3 | `r0` constant key suppresses later rounds' dispositions | CLOSED | Same digest change; plus 6e now names this round's outcome — `dispositions posted in <comment-url>` / `dispositions not posted — <guard-skipped \| post failed <code>>` at spec:1149 with the scoping paragraph spec:1159-1162 |
| edge-cases | F-4 | D6's advance rule states two incompatible values for `LAST_BODY_REVIEW_ID` | **PARTIAL** | D6 itself is fixed (spec:967-985, contiguous prefix, worked example `[100 ok, 200 failed, 300 ok] → 100`). But Decision 2 (spec:80-81) and D1 (spec:624-627) still state the *old* non-contiguous rule while explicitly labelling it "D6's rule". See F-1 below — this is the same defect, unfixed in two of its three sites |

Known-open attempt-1 items re-raised below: correctness/F-4 (wrong review-id attribution in test row 19) as **F-5**.

Grounding notes:
- Ticket VHS-41 retrieved from `namespace: skills` (record `bd1504df-8bbb-4675-9f03-6dc5027b6637`). Its DONE WHEN matches the brief verbatim; no conflict.
- All `:line` anchors into `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\skills\review-pr\SKILL.md` (406 lines) were opened and verified. **Every anchor is accurate** — `:11 :68 :69 :75 :76 :79 :81 :83 :85-115 :96-107 :99 :109-114 :120 :125-161 :127 :140-144 :152-158 :162-215 :172 :174-175 :180 :186 :194-195 :198 :200 :209 :215 :217-241 :224-226 :233 :234 :241 :245 :252 :262 :273 :277 :279 :281-345 :283 :290 :316 :331 :341-342 :345 :351-368 :362 :370-377 :379-406 :381 :382 :397 :404`. The "seven pre-existing bare tool names" claim (`:11 :99 :120 :180 :200 :316 :345`) is exactly right.
- All 19 test-plan **Pre** measurements reproduce exactly, including row 16's `1 failed, 158 passed, 3 skipped` and rows 1–2's lint output.
- All live-specimen claims verified: PR #28 `5135914911` (`<details>` body line 8, `<summary>` line 9, declared 1, group `skills/grilling/SKILL.md (1)`, item `171-171`, `🟡 Minor`, title, key `v1:80d76a9c27d4add3fdeb6bb9`); petland #64 `5123259707` (lines 3/4, not blockquoted, `rosa-tests/probe.mjs (1)`, `376-376`, `🔵 Trivial`, key `v1:f1a62d5b1a96778a982c2667`); the four zero-length bodies `5135919676 / 5135923847 / 5135925406 / 5135992754`.
- Verified independently: `gh` 2.87.3 rejects `--slurp` with `--jq` (exact message matches spec:193-194); gojq's `capture("…r(?<r>[0-9]+)")` works and emits nothing on non-match (spec:661-664 correct); `printf … | sha1sum | cut -c1-8` works.
- Decision 13's supporting claims verified: `sync.py:30 SUBTREES = ("skills", "agents")`, `sync.py:45 root.rglob("*")`, `sync.py:155 def cmd_status(...)` with no return, four `skills/*/scripts/` dirs, `docs/authoring-portable-skills.md:41`.
- `git log -10` on the touched files: `AGENTS.md` last changed 2026-09-06 (`d381f88`, VHS-32) — **within 7 days**. It added 13 / removed 4 lines, which could have shifted the spec's anchors; I re-verified both against the current tree and `AGENTS.md:7` ("no test suite") and `:46`/`:48` (§ `/review-pr` heading / paragraph) are correct as of now. `skills/review-pr/SKILL.md` last changed 2026-08-18 — no recent drift.

## Findings

### F-1: Decision 2 and D1 state a different `LAST_BODY_REVIEW_ID` advance rule than D6, while claiming to quote D6
**Severity:** P0
**Where:** spec.md:80-81 (§ Decision 2), spec.md:624-627 (§ D1) vs spec.md:967-975 (§ D6)
**Claim:** Decision 2: *"After Step 2's harvest and Step 3's triage, set it to the highest id whose body was fetched and parsed successfully in that harvest **(D6's rule)**."* D1: *"set `LAST_BODY_REVIEW_ID` to the highest id whose body was fetched and parsed successfully in this harvest — **the same rule D6 applies in 6b**."*
**Why this is wrong:** D6 states the opposite rule and names the discriminating case explicitly — spec.md:967-973: *"set `LAST_BODY_REVIEW_ID` to the highest id of the **contiguous successfully-parsed prefix** … the highest successfully parsed id that is strictly below the round's lowest failed or deferred id … For `[100 ok, 200 fetch-failed, 300 ok]` the mark is `100`, not `300`."* D1's phrasing yields `300` on that exact input. The two sections cannot both be followed, and D1/Decision 2 assert they are the same rule. The failure is not hypothetical in Step 2: 2b step 2 makes the Step-2 harvest set up to 10 reviews (spec.md:666-671) and 2b step 3 says a body-fetch failure *"sets `HARVEST_FLOOR` at that review's id"* (spec.md:678-682), so `[100 ok, 200 failed, 300 ok]` is reachable in Step 2's own harvest. An implementer following D1 advances the in-run mark past a failed fetch; D5's poll then filters `select(.id > <LAST_BODY_REVIEW_ID>)` (spec.md:920) and review 200 is never retried by any later 6a poll of that run — precisely the permanent gap D6:973-975 forbids. This is attempt-1 edge-cases/F-4 closed in one of three sites.
**Suggested fix:** Replace the rule text at spec.md:80-81 and spec.md:624-627 with a pointer, not a restatement — e.g. *"…set it per D6's advance rule: the highest id of the contiguous successfully-parsed prefix, strictly below this harvest's lowest failed or deferred id."* Keep the worked example in D6 only, so there is exactly one canonical statement.

### F-2: The findings-free 6f post has no call site on the Step 2 exits that need it, so a bounded zero-finding harvest still recomputes forever
**Severity:** P1
**Where:** spec § Decision 3 (spec.md:110-113), § D7 Post condition (spec.md:1014-1019), § D7 reachability edits (spec.md:1004-1012) vs § Decision 2 (spec.md:90-95), § Decision 12 (spec.md:409-415), § D9 (spec.md:1225-1228)
**Claim:** D9: *"**A bounded round parses its whole prefix to zero findings** — 6f still posts, with the findings-free body, so the marker advances and the deferred reviews are reachable next run. Without it the same bounded set recomputes forever."* D7's post condition: post *"when `R` would advance past `PRIOR_MARK` and a `HARVEST_FLOOR` exists."*
**Why this is wrong:** the spec enumerates 6f's call sites exhaustively and none of them is reachable on a zero-finding round. Decision 3:110-113 — *"invoked from every path that completes a round's triage — Step 5's push path, 6b's fix-push branch (`:233`), 6b's no-actionable branch (`:241`), and the no-push path at `:245`."* D7:1004-1012 lists exactly two wiring edits: delete the `:277` guard, and amend `:245`. `:245` lives inside 6c and, as amended, fires *"after that round's triage completes — Step 3's or any 6b cycle's."*
On a round where the harvest was bounded (2b step 2 sets `HARVEST_FLOOR`, spec.md:666-671) and the parsed prefix yields **zero** surviving items, Step 3 has nothing to triage and the run exits inside Step 2:
- `SKILL.md:81` fires if the verdict is `APPROVED` with no unresolved threads — D1:618-621 preserves it, gated only on *harvest completed without failure* and *no body findings*; a **bound** is not a Decision 14 failure (spec.md:503-513 lists fetch/parse errors only), so `:81` fires.
- `SKILL.md:381`, as rewritten by D9:1168-1172, fires on *"no inline comments **and** no body-level items after a **completed** 2b harvest → report 'Nothing to review' and exit."*

Both exit before Step 3, before Step 5, before 6a/6b and before 6c/`:245`. So 6f never runs, no marker posts, `PRIOR_MARK` never advances, and the next run recomputes the identical 10-oldest set and defers the identical tail — the exact "recomputes forever, deferred reviews unreachable on every run" defect Decision 12:409-415 says the findings-free comment exists to prevent. Grepping the spec for `6f` (37 hits) confirms no text wires it to `:81`, `:83`, or `:381`.
**Suggested fix:** Add a fifth call site to Decision 3's list and a third reachability edit to D7: before any Step 2 exit (`:81`, `:83`, `:381`), if D7's post condition holds, post the findings-free 6f comment and *then* exit. State it in D1's `:81`/`:83` paragraph and in D9's `:381` rewrite so the implementer meets it where they edit.

### F-3: Decision 2 carries the pre-digest marker literal
**Severity:** P2
**Where:** spec.md:57-58
**Claim:** *"`PRIOR_DISPOSITIONED_REVIEW_ID` is the highest review id named by a `<!-- review-pr:body-dispositions:r<id> -->` marker in a PR comment the skill itself authored"*
**Why this is wrong:** Decision 12:353 fixes the marker as `<!-- review-pr:body-dispositions:r<R>:h<HEX> -->`, and every other spelling in the spec carries the digest (spec.md:1040, 1049, 1092, 1103). spec.md:58 is the only surviving full-literal in the old shape. An implementer who writes that literal into the skill ships a marker the D7 guard's exact-match (spec.md:1040) can never match, and test row 25 (`grep -cF 'body-dispositions:r<R>:h'`, expected `≥ 3`) would still pass on the other three sites, so the gate would not catch it.
**Suggested fix:** at spec.md:58, either write the full current literal or drop the literal and say "an `r<R>` marker (Decision 12 gives the full shape)".

### F-4: Test row 14's guard regex cannot match the multi-line fetch shape the skill actually uses
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:1332 (row 14 command), spec.md:1353 (row 14 expectation)
**Claim:** row 14 `grep -cE 'gh api --paginate.*\| *(wc|jq)' $S`, expected `[guard] 0`, described as guarding *"Decision 7's most load-bearing rule"* after the v3 draft *"matched nothing whether or not the antipattern was present."*
**Why this is wrong:** the regex is line-scoped, and every `gh api` fetch in `SKILL.md` and in this spec is written across two lines with a `\` continuation (`SKILL.md:68-69`, `:75-76`, `:174-175`, `:194-195`, `:224-225`, `:341-342`; spec.md:586-587, 911-912, 919-920, 927-928, 1037-1040). The antipattern therefore lands on the `--jq` line, which contains no `gh api --paginate`. Verified empirically:

```
gh api --paginate repos/<OWNER>/<REPO>/pulls/<N>/comments \
  --jq '.[] | select(.x) | .id' | wc -l
```
→ `grep -cE 'gh api --paginate.*\| *(wc|jq)'` returns **0**; the single-line form returns **1**. So the guard still cannot fail against the realistic shape — the v3 defect is only half fixed.
**Suggested fix:** make the row multiline-aware, e.g. `grep -nE '\| *(wc|jq|head|tail|sed|cut)\b' $S` restricted to lines inside fenced `bash` blocks, or `grep -Pzoc` / a two-line `pcregrep`; or pin the complementary positive instead — assert that every `gh api --paginate` block is followed within 3 lines by `HARVEST_FAILURE rc=` (which row 24 already partly does) and drop the vacuous negative.

### F-5: Test row 19 attributes body content to the wrong review id (re-raise of attempt-1 correctness/F-4)
**Severity:** P2
**Where:** spec.md:1371-1377 (manual row 19)
**Claim:** *"`…/reviews/5135878266` — **zero** items **and neither tripwire fires**. This body carries the top-level `🤖 Prompt for all review comments with AI agents` block listing two findings **under the words "Outside diff comments"**; … a phrase tripwire firing here means the per-phrase / post-mask scoping of Decision 11 was not implemented — the detector would be noise from day one."*
**Why this is wrong:** verified against the live body. `gh api repos/Vigil-Harbor/vigil-skills/pulls/28/reviews/5135878266 --jq .body` is 2468 chars / 80 lines and contains **no occurrence of "outside diff" or "nitpick"** (case-insensitive grep: zero hits). Its AI-prompt block lists its two findings under the heading `Inline comments:` (body line 12), not "Outside diff comments". The string `Outside diff comments:` is in review **5135914911** at body line 67, inside the fence that opens at line 51. Consequence: row 19 cannot exercise the phrase tripwire at all — the trigger phrase is absent, so the detector is silent regardless of whether per-phrase/post-mask scoping was implemented. The row's stated pass condition still holds by accident (zero items, no tripwire), so the gate gives false assurance on the one property it claims to check.
**Suggested fix:** correct the attribution (the AI-prompt block on `5135878266` lists two findings under `Inline comments:`), and move the phrase-tripwire discriminator to a row that actually contains a trigger phrase outside a matched section — e.g. add a synthetic body carrying `outside diff range` in unfenced prose with no matching `<summary>`, asserting the tripwire *does* fire, paired with `5135914911` (whose line-67 `Outside diff comments:` sits in a fence) asserting it does not.

### F-6: `$TMPDIR` is used in three places but never established; D7 is cited as establishing it and does not
**Severity:** P3
**Where:** spec.md:216-218, 588, 678-680, 913 vs spec.md:1071-1076
**Claim:** 2b step 3: *"`… > "$TMPDIR/body-<REVIEW_ID>.md"` — **the temp/scratch directory D7 establishes**, never the worktree."*
**Why this is wrong:** D7:1071-1076 says only that `<BODY_FILE>` goes in *"the system temp directory (or the harness scratch directory)"*; it never names `$TMPDIR` or tells the agent to set it. On this machine Git Bash does export `TMPDIR=/tmp`, so the blocks work as written — but the variable is inherited, not established, and on a shell where it is unset the redirect resolves to `/new_inline` and fails, which the Decision 7 block then reports as `HARVEST_FAILURE rc=1`. Under Decision 14 that forces `inconclusive` on every round — a loud failure, but a spurious one with a misleading diagnosis.
**Suggested fix:** in D7, add one sentence establishing the value once — e.g. *"resolve a scratch directory once per run (`TMPDIR` if set, else `mktemp -d`) and carry it as conversational state like `PUSH_TIME`"* — and have 2b step 3 and Decision 7's canonical block reference that.

### F-7: The idempotency guard is byte-exact on the marker line, which a web-UI edit silently breaks
**Severity:** P3
**Where:** spec.md:1037-1040 (guard jq), spec.md:1033-1035 (last-non-blank rule)
**Claim:** the guard matches `((.body // "") | split("\n") | map(select(. != "")) | last // "") == "<!-- review-pr:body-dispositions:r<R>:h<HEX> -->"`.
**Why this is wrong:** two narrow byte-exactness assumptions are load-bearing and unstated. (1) Line endings: comments the skill posts via `gh pr comment --body-file` keep `\n` (verified — the one issue comment on PR #28 returns no `\r`), but a comment edited through the GitHub web UI is re-normalized to `\r\n`, after which `split("\n")` leaves a trailing `\r` on the marker line and the equality silently fails, so the guard posts a duplicate. (2) "Non-blank" is implemented as `select(. != "")`, which keeps a whitespace-only trailing line and makes it the "last non-blank line". The resume query is unaffected (its `capture` is a substring match), so the failure is guard-only and asymmetric.
**Suggested fix:** normalize before comparing — `map(sub("\r$";"")) | map(select(test("\\S")))` — or compare with `test()` on the marker literal anchored to end-of-string rather than `==`.

### F-8: The quoted `gh api --arg` error string is wrong
**Severity:** P4
**Where:** spec.md:640
**Claim:** *"`gh api --jq --arg self x '...'` fails with `accepts 1 arg(s), received 4`"*
**Why this is wrong:** running that exact form on `gh` 2.87.3 gives `accepts 1 arg(s), received 3` — `--jq` consumes `--arg` as its value, leaving `self`, `x`, and the endpoint as three positionals. The substance (no `--arg` flag; fails before any request) is correct; only the pinned count is off. It matters only because the spec offers it as verifiable evidence for test row 13.
**Suggested fix:** change `received 4` to `received 3`, or drop the count.

## Summary
P0: 1 | P1: 1 | P2: 3 | P3: 2 | P4: 1

STATUS: RED P0=1 P1=1 P2=3 P3=2 P4=1
