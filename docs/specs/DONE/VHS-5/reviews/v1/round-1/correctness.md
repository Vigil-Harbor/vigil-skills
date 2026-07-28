# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Grounding verification

Verified against current HEAD (`skills/review-pr/SKILL.md`, commit `77f5257`):

- **Line 40** — `gh pr diff <N> --stat` — CONFIRMED present at line 40.
- **Line 241** — jq filter `select(.comments.nodes[0].author.login == "coderabbitai[bot]")` — CONFIRMED present at line 241.
- **Line 171** — Phase 6a polling cadence line — CONFIRMED present at line 171.
- **Line 252** — Phase 6d Phase 1 polling cadence — CONFIRMED present at line 252.
- **Line 254** — "If after the 2-minute polling window..." — CONFIRMED present at line 254.
- **Line 279** — Phase 6d Phase 2 polling cadence — CONFIRMED present at line 279.
- **REST occurrences of `"coderabbitai[bot]"`** — spec claims six at lines 66, 70, 158, 168, 181, 276. Verified — all six confirmed; plus the GraphQL one at 241 = 7 total. Matches spec.
- **Polling attempt-count derivation** — 5min/30s = 10, 2min/15s = 8, 3min/20s = 9. Matches spec's "10 / 8 / 9 attempts respectively."

Ticket lookup: Not attempted (out-of-band — no MCP call needed; brief is authoritative for VHS-5 and matches spec scope).

## Findings

### F-1: Test command's `python sync.py status` clause is tautological — does not actually gate on a clean mirror

**Severity:** P1
**Where:** spec § Test command (line 159); spec § Test plan structural check #1 (line 142); spec § Done when #5 (line 172).
**Claim:** The spec says the Test command verifies, in order, "(1) sync mirror is clean" and Done-when #5 says "After `python sync.py push`, `python sync.py status` reports clean (no drift between repo and `~/.claude/skills/review-pr/`)." The Test command starts with `python sync.py status && ...`.
**Why this is wrong:**

- I read `sync.py:155-173` (`cmd_status`). It iterates files and prints `[<state>] path` lines for any `differ` / `src-only` / `dst-only` file, but unconditionally returns from `cmd_status` without setting an exit code. The CLI wrapper in `main()` doesn't propagate any return either. The function exits 0 whether or not differences exist.
- I ran `python sync.py status` in the current working tree at HEAD (before any spec edits). It prints six drift lines (peon-ping skills `dst-only`, `skills/review-pr/SKILL.md differ`, `skills/ship-spec/states.json differ`) and still exits 0.
- Consequence: the `&&` chain in the Test command will proceed past `python sync.py status` regardless of mirror state. The clause is decorative — it tells the reader "look at the output" but doesn't enforce anything.
- A stronger consequence: at the moment `/ship-spec` runs the Test command (after editing `skills/review-pr/SKILL.md`, before `python sync.py push`), the mirror is by construction in `differ` state for that file. Even a reader who manually inspects the output cannot tell a "good differ" (about-to-push spec edits) from a "bad differ" (latent drift). The current working tree's pre-existing `dst-only` peon-ping files and `ship-spec/states.json differ` are out-of-scope drift the spec author does not own — they will surface in every run of the Test command and confuse the implementer into "did I miss something?"

**Suggested fix:** Drop the `python sync.py status` clause from the Test command entirely, OR replace it with a clause that actually exits non-zero on drift for the file in scope only. Done-when #5 is a separate post-merge gate (it runs after `python sync.py push`, which the spec acknowledges is outside the spec author's scope per § Scope "Do not touch ~/.claude/..."). Suggest:
1. Remove `python sync.py status && ` from the Test command's `&&` chain.
2. Reframe Test plan #1 from "exits clean" to "manual visual check — only `skills/review-pr/SKILL.md` should appear as `differ`; ignore pre-existing peon-ping `dst-only` lines and `ship-spec/states.json differ`."
3. Reframe Done-when #5 as a post-`python sync.py push` check the ship-spec runner will perform, explicitly outside the Test command.

### F-2: Test command uses bash-only syntax; spec acknowledges Windows but the assertion shape (`test "$(...)" = "6"`) silently swallows grep failures

**Severity:** P2
**Where:** spec § Test command (line 159), § "Run via Bash tool" note (line 164).
**Claim:** "Run via Bash tool (not PowerShell) — the brief's repo uses bash for all `gh`/`git` invocations per the SKILL.md shell note, and `grep -c` is the available count primitive on this machine via the Bash tool's git-bash."
**Why this is wrong:** Not wrong per se, but worth flagging — `grep -c` on a non-existent file returns exit 2 with no stdout, and `test "" = "6"` is false. If the file path is mistyped, the failure mode is "the assertion fails" rather than "the file is missing." That's tolerable, but the chain has no echo/explainer between clauses, so a failed assertion in the middle gives the implementer a binary exit code with no clue which clause failed. Suggest splitting the chain into six labeled `test`s with `echo` between them so the implementer sees which check fired.
**Suggested fix:** Wrap each assertion with an explanatory echo, e.g.:
```bash
echo "check 1: REST coderabbitai[bot] count == 6" && test "$(grep -c '"coderabbitai\[bot\]"' skills/review-pr/SKILL.md)" = "6" && \
echo "check 2: GraphQL coderabbitai count >= 1" && test ... && ...
```
Lower-priority polish; doesn't block.

### F-3: Done-when #4 anchors on `git diff --name-only main..HEAD` but ship-spec uses a worktree off main — the anchor wording may mislead

**Severity:** P3
**Where:** spec § Done when #4 (line 171).
**Claim:** "`git diff --name-only main..HEAD` (or equivalent at merge time) lists exactly that path."
**Why this is wrong:** Not wrong, just under-specified. `/ship-spec` cuts an isolated worktree (per its skill description), so at implementation time `HEAD` is the worktree branch tip. The "(or equivalent at merge time)" parenthetical hand-waves this, but a stricter formulation would name the actual ref to compare against. Cosmetic — implementer will figure it out.
**Suggested fix:** Tighten to "`git diff --name-only <merge-base>..HEAD` on the implementation branch lists exactly `skills/review-pr/SKILL.md`."

### F-4: Spec § Test plan structural #2 phrases the assertion in a way that's easy to misread

**Severity:** P3
**Where:** spec § Test plan (line 143).
**Claim:** "`grep -c '"coderabbitai\[bot\]"' skills/review-pr/SKILL.md` returns the **pre-existing** count minus 1. Initial count at HEAD is 7 occurrences..."
**Why this is wrong:** The phrase "pre-existing count minus 1" is a relative claim; the Test command itself asserts the absolute number `= "6"`. A future reader who edits the file (say, adding another REST filter unrelated to this spec) would have the Test command assertion break even though the *delta* (P0 fix) was applied correctly. The current claim is fine for round 1 (7 occurrences confirmed at HEAD), but the spec should either commit to the absolute number or commit to the delta. Mixing them invites confusion.
**Suggested fix:** Replace "pre-existing count minus 1" with "exactly 6 (the seven HEAD occurrences minus the line-241 GraphQL filter that the P0 edit drops)."

### F-5: Spec § Test command grep pattern for `"coderabbitai")` requires the closing paren — fine, but fragile to incidental formatting changes

**Severity:** P3
**Where:** spec § Test command (line 159), assertion 3.
**Claim:** `grep -c '"coderabbitai")' skills/review-pr/SKILL.md` returns at least 1 (the new GraphQL filter).
**Why this is wrong:** The pattern `"coderabbitai")` (literal close-paren) is intended to disambiguate from `"coderabbitai[bot]")` REST filters. It works for the proposed P0 edit but is fragile — if the implementer reformats the jq line (e.g., line-breaks before the close-paren) the assertion silently breaks. Low risk because the proposed edit is one-character.
**Suggested fix:** Optional: use `grep -c '"coderabbitai"' skills/review-pr/SKILL.md` (without the close-paren) and assert `= "1"` post-edit. Or leave as-is and accept the fragility — the implementer is instructed to do a literal one-character delete.

## Summary
P0: 0 | P1: 1 | P2: 1 | P3: 3 | P4: 0

STATUS: RED P0=0 P1=1 P2=1 P3=3 P4=0
