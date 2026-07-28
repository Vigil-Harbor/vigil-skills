# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | `grep -c "intervals are aspirational"` brittle to count drift | CLOSED | spec.md:145 now uses `-ge "3"`; spec.md:159 test command uses `-ge "3"`. Lower-bound semantics adopted as suggested. |
| edge-cases | F-2 | Test command relies on bash + GNU grep + LF (unenforced) | OPEN (P3) | Spec.md:164 still says "Run via Bash tool (not PowerShell)" as prose only; no `bash -c "..."` wrap. Same severity as round 1; not regressed. |
| edge-cases | F-3 | Pre-existing absolute count `= "6"` for REST `"coderabbitai[bot]"` would drift | CLOSED | Spec.md:159 test command no longer asserts on REST `"coderabbitai[bot]"` count at all; only `-ge "1"` on the new GraphQL `"coderabbitai")` literal. The brittle absolute count is gone. |
| edge-cases | F-4 | Punctuation drift in explanatory note could re-introduce `"coderabbitai[bot]"` and break `= "6"` | CLOSED | Same root cause as F-3 — the brittle assertion is gone. Explanatory-note punctuation no longer affects the test command. |
| edge-cases | F-5 | No fallback for `gh pr diff --name-only` failure modes | OPEN (P3) | Spec.md:33-42 (Decision 2) unchanged from round 1; the suggested § Out-of-scope sentence about `--name-only` failure modes was not added. Not regressed; same severity. |
| edge-cases | F-6 | "Extend further 10 attempts" loses meaning under aspirational intervals | OPEN (P3) | Spec.md:105 still reads `if at the 10th attempt ... extend to a further 10 attempts`. The spec did not address F-6. The Phase 6a wording still gates the extension on `gh pr checks <N>` showing "in_progress", which is a coherent state observation (not a wall-clock test), so the "extend" clause is more defensible than round 1 implied — it's still PARTIAL, but the concrete confusion is mild. Keeping at P3. |
| edge-cases | F-7 | No observability hook for polling-phase failures | OPEN (P3) | Spec § P2 polling rewrites unchanged. Brief Decision 4 forbids new error branches; the spec author honored that. Not regressed. |
| edge-cases | F-8 | `python sync.py status` exit semantics unverified | CLOSED | The `python sync.py status` clause has been removed from the test command (spec.md:159). Done-when #5 is now framed as a post-`sync.py push` manual check scoped to `skills/review-pr/SKILL.md` only (spec.md:172). The load-bearing dependency on `status` exit code is gone. |
| correctness | F-1 | `python sync.py status` tautology | CLOSED | Test command no longer chains on `sync.py status`; spec.md:147 explicitly explains the omission. |
| correctness | F-2 | No labels between assertions | OPEN (P2) | Polish only; not regressed. |
| correctness | F-3 | Done-when #4 anchor wording | CLOSED | Spec.md:171 now says "merge-base..HEAD on the implementation branch lists exactly that path" per the suggested tightening. |
| correctness | F-4 | Test plan "pre-existing count minus 1" ambiguous | CLOSED | Test plan now phrases assertion 1 as `-ge "1"` (positive presence), no longer "count minus 1". |
| correctness | F-5 | `"coderabbitai")` close-paren grep is fragile | OPEN (P3) | Spec.md:159 still uses `"coderabbitai")` with literal close-paren. Same risk; not regressed. |
| conventions | F-1 | Exact-count assertions drift from prior-VHS pattern | CLOSED | Spec.md:159 now uses `-ge` lower-bound assertions like prior-VHS, except for the `--stat = "0"` which is intentionally exact (zero-match is the only valid outcome). |
| conventions | F-2 | Comment text verbosity | OPEN (P3) | Design block unchanged. Acceptable; not regressed. |
| conventions | F-3 | "Cargo-cult code" editorializing | OPEN (P4) | Tone-only; not regressed. |
| conventions | F-4 | Exact-count assertions are silent spec additions | CLOSED | The exact counts are gone (see conventions F-1); only `-ge` floors remain plus the `= "0"` for `--stat`. |
| conventions | F-5 | "Three similar lines" citation accuracy | OPEN (P4) | Citation in spec.md:135 unchanged; pure attribution nit. |

All round-1 P0/P1 findings are CLOSED. Remaining OPEN items are P3/P4 and were already accepted in round 1.

## Findings

### F-1: Test command uses `-ge` lower bounds — accidental duplication of edited lines passes silently

**Severity:** P3
**Where:** spec.md:159 (Test command), spec.md:142-145 (Test plan items 1, 3, 4)
**Edge case:** All three of the new presence assertions use `-ge "N"` (>= 1 for `"coderabbitai")`, >= 1 for `--name-only`, >= 3 for `intervals are aspirational`). The trade-off vs the previous `= N` form is that an implementer (or a future editor) who accidentally duplicates the edited fence — e.g., copies the jq line twice in different phases, or pastes the polling-cadence block four times — passes the test command with no warning. The spec.md:145 rationale explicitly accepts this for the "intervals are aspirational" floor ("a future cadence-related edit that adds a fourth occurrence does not break the assertion") but applies the same logic to `"coderabbitai")` and `--name-only` without naming the trade-off.
**What happens:** A malformed edit that duplicates one of the target literals passes the test gate. The implementer ships a structurally weird SKILL.md (two jq filters where there should be one); next `/review-pr` run hits the same line twice through different code paths. Practically very unlikely (the edits are 1-character or single-line) but worth noting because the prior round flagged the symmetric concern (false negatives from `=`).
**Why the spec misses it:** The spec swapped `=` for `-ge` to address F-1/F-3 from round 1 (false negatives on benign drift). It did not call out that the new floors trade false negatives for false positives. Acceptable trade-off — the manual end-to-end step in § Test plan (paste the GraphQL query, run `gh pr diff`) catches the duplication case anyway.
**Suggested fix:** Optional one-line acknowledgment in § Test command rationale: "The `-ge` floors trade brittleness against benign edits for tolerance of accidental duplication; the manual end-to-end steps in § Test plan catch the duplication case." Not load-bearing — leave as-is is also fine.

### F-2: `test "$(grep -c -- '--name-only' SKILL.md)" -ge "1"` could match `--name-only-foo` or partial words

**Severity:** P4
**Where:** spec.md:159 (Test command assertion 3)
**Edge case:** `grep -c -- '--name-only' skills/review-pr/SKILL.md` matches any line containing the substring `--name-only`. Today only one line contains it (the gh command). But `--name-only` is a flag that could appear in `git diff --name-only`, `git log --name-only`, etc., if the skill ever adds another such invocation. Not a defect today — the assertion is "at least 1" and any of those occurrences would satisfy it. The edge case is more subtle: if a future edit replaces `gh pr diff <N> --name-only` with a different mechanism but adds `git log --name-only` elsewhere, the test still passes even though the P1 fix has been silently regressed.
**What happens:** Latent false positive after far-future edits. Today's spec ships correctly.
**Why the spec misses it:** A presence check is, by definition, weaker than a position-specific check. The spec author opted for presence to gain resilience against unrelated line moves; this is the dual cost.
**Suggested fix:** None for this spec — the trade-off was made consciously. If the implementer wants to harden: `grep -c 'gh pr diff <N> --name-only' skills/review-pr/SKILL.md` would pin the exact invocation, but at the cost of brittleness against whitespace/formatting drift. Leave as-is.

### F-3: Test command `test "$(grep -c -- '--stat' SKILL.md)" = "0"` is correct, but the `-c` exit-1-on-zero-matches behavior is subtle

**Severity:** P4
**Where:** spec.md:159 (Test command assertion 2)
**Edge case:** `grep -c` exits with code 1 when there are zero matches (no lines printed to stdout actually contain the pattern), but it still prints `0` to stdout. Inside `$(...)`, only stdout is captured, and the `$(...)` exit code does not propagate through `test`. So `test "$(grep -c -- '--stat' SKILL.md)" = "0"` correctly succeeds when there are zero matches. This works empirically — but is one of those bash idioms that bites readers who think `set -e` or `set -o pipefail` semantics apply. No defect; the spec gets this right by accident of `grep -c`'s side-effect of printing `0`.
**What happens:** Nothing today. Worth noting because if any future maintainer wraps this test command in `set -eo pipefail` or `bash -e`, the grep's exit-1 may abort the script before `test` runs. Out of scope for VHS-5.
**Why the spec misses it:** This is a bash gotcha, not a spec defect. The spec command works as written.
**Suggested fix:** None. Note here purely for the round-2 record.

### F-4: Manual "Done-when #5" check is robust against pre-existing drift, but the spec does not name the pre-existing drift items

**Severity:** P3
**Where:** spec.md:172 (Done-when #5), spec.md:147 (§ Test plan note on `sync.py status`)
**Edge case:** Done-when #5 reads: "After `python sync.py push`, `python sync.py status` shows no remaining `differ` entry for `skills/review-pr/SKILL.md`." This is the correct narrowing — it scopes the manual check to one file and ignores ambient drift. The spec.md:147 note even calls out that the working tree has pre-existing drift (peon-ping `dst-only`, `ship-spec/states.json differ`). Good. The remaining edge: the verifier needs to remember to look only at the `skills/review-pr/SKILL.md` line in `sync.py status` output. If the implementer's eye drifts to other `differ` lines and they push those too as part of "cleaning up", they ship sync edits outside this spec's scope.
**What happens:** Implementer over-corrects, pushes ambient drift (which is the user's local state, not authoritative). Not a data-loss event, but introduces noise into the commit history beyond what this spec authorizes.
**Why the spec misses it:** The narrowed assertion is on the right axis; the spec just doesn't warn that the implementer must not "fix" other `differ` lines they happen to see.
**Suggested fix:** Add one sentence to Done-when #5: "Other `differ`/`dst-only` lines in `sync.py status` output are pre-existing drift unrelated to this spec — do not push them as part of VHS-5." Cheap insurance.

### F-5: Spec § P2 Location B includes a secondary edit ("after the 2-minute polling window" → "after exhausting the polling attempts") that the test command does not verify

**Severity:** P3
**Where:** spec.md:115-121 (Location B alignment), spec.md:159 (Test command), spec.md:170 (Done-when #3)
**Edge case:** The spec correctly identifies that line 254 of SKILL.md ("If after the 2-minute polling window some threads are still unresolved") must be rewritten alongside the polling-cadence rewrite at line 252. The test command does NOT assert on this — it only asserts that "intervals are aspirational" appears `-ge 3` times. An implementer who applies the three primary polling-cadence rewrites but forgets to touch line 254 passes the test command. The leftover "after the 2-minute polling window" wording in production then directly contradicts the new aspirational-intervals framing.
**What happens:** Subtle inconsistency in the shipped SKILL.md: three polling blocks correctly reframe intervals as aspirational, but the immediately-following sentence at line 254 still says "after the 2-minute polling window." A reader gets mixed signals. No functional break — the polling logic still uses attempt counts.
**Why the spec misses it:** The Location B alignment is described in the Design block but is not encoded in the test command. The "intervals are aspirational" floor counts the *cadence* sentences, not the *aftermath* sentence.
**Suggested fix:** Add a fifth assertion to the test command: `test "$(grep -c '2-minute polling window' skills/review-pr/SKILL.md)" = "0"` — confirms the wall-clock leftover is gone. Or, less assertively, add a structural test plan item that flags the line-254 edit as part of the verification gate. The test command-line change is one literal `&&` clause; minimal cost.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 3 | P4: 2

STATUS: GREEN
