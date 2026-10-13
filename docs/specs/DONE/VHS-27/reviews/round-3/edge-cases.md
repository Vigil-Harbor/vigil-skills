# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | A renamed cited file never becomes a changed path, so the no-op sticks | CLOSED | spec § Changed regions lines 268–277: `--no-renames`, `-c core.quotePath=false`, `--no-color`, a non-raw line is a failure, one snapshot. § Artifacts lines 217 and 230 write that snapshot, with no second `rev-parse`. Scenario 14. `git ls-files` on this tree prints forward slashes. |
| edge-cases | F-2 | Two headings with the same line can hide an edit | CLOSED | spec § Changed regions lines 264–266: stack-ordered nth pairing, a `(before first heading)` region, and an unexplained byte diff emits every heading. |
| edge-cases | F-3 | A red marker whose P0/P1 headings do not parse can be replaced with green | CLOSED | spec § No-op steps 2–4 (lines 171–173) and § Dispatch line 316 inject `<lens>/STATUS (P0)` when STATUS P0+P1 is greater than zero and no heading parsed. Both sets empty selects `mode: full (open findings unreadable)`. Scenario 15. Test plan line 449. |
| correctness | F-1 | Workflow reference still describes one round counter outside the named edit sites | CLOSED | spec § Docs lines 388–391 name the Phase 2 introduction, its halt and rewrite steps, `### The grilling contract`, and `**Targeted rewrite at round round_cap**`, and read them as pass index `P`. Those headings are in `docs/spec-workflow-reference.md` (lines 29, 70, 286). |
| correctness | F-2 | Ticket not cached | CLOSED | spec § Deferred (P2+) line 487 records no spec change. This round was told to use the brief and not to call shared memory. |
| conventions | F-1 | Grill paths in `### 2f-i` are not an edit site | CLOSED | spec § Stop screens line 374: seed, `grill.md` persist, and re-render use `round-<C>`. The heading is `skills/spec-cycle/SKILL.md` line 699. |
| conventions | F-2 | Three workflow-reference sentences still treat `round_cap` as the cumulative round | CLOSED | Same § Docs sentence as correctness F-1 (line 391). |
| conventions | F-3 | New git commands are not added to `## Tool-use notes` | CLOSED | spec § Docs line 394 names `## Tool-use notes` (`SKILL.md` line 931) and the four read-only commands. |
| conventions | F-4 | Changed-region headings do not reuse the skill's heading boundary | CLOSED | spec § Changed regions line 262 uses `^#{1,6}\s`, the boundary at `SKILL.md` lines 299 and 351. |

The three round-qualified keeps (edge-cases/R1/F-2, R1/F-3, R1/F-4) stay in the spec: locator strip and scenario 10, exclusive-body pairing, and a git failure selecting full mode or the pass-2 pending stop. No `## Deferred — follow-up required` section is present. `## Deferred (P2+)` is not that section.

## Findings

### F-1: A late full upgrade keeps the two-directory delta start
**Severity:** P1
**Where:** spec § No-op step 4, line 173; spec § Mode lines 162–164
**Edge case:** Tier `big` or `irreversible` (`round_cap` is 4). Marker `red`, `source: review`, `round: 4`. `round-5/` and `round-6/` are absent, so row 11 matches and the delta start is 5. `round-7/` already exists. Filtered spec and brief match, code drift is empty, the guarantee scan is clean, and every standing report parses with STATUS P0+P1 of 0 and no `### F-<k>:` P0/P1 heading.
**What happens:** Step 4 replaces the token with `mode: full (open findings unreadable)` and says to run the full loop. The only start computed on the row-11 path is `candidate + 1`, and only `candidate+1` and `candidate+2` were proved absent. A four-directory loop from 5 creates `round-7/` over the directory that is already there. That overwrites a prior round's reports. Brief Decision 8 says earlier reports are never overwritten. Spec Decision 8 (line 72) requires a full invocation's whole `start .. start+round_cap-1` span to be absent, and the recovery start to be the smallest free span. `small` does not hit this: its cap is 2, which is the pair row 9 already reserves.
**Why the spec misses it:** The free-span paragraph sits in § Mode, on the path that is already full before the no-op. Step 4 runs after that, names no new `start`, and scenario 15 does not say where the full loop starts. Scenario 13 covers row 9 only.
**Suggested fix:** In § No-op step 4, discard the delta start and compute `start` with the full-invocation rule in § Mode before creating any directory. If no free span of `round_cap` directories exists, stop with the marker unchanged. Add a scenario: marker round 4, `round-5/` and `round-6/` absent, `round-7/` present, both finding sets empty, red marker; the full start is not 5, and `round-7/` is not overwritten.

### F-2: A line-only Where is placed in the spec after the revision, so the open section drops out
**Severity:** P1
**Where:** spec § Changed regions, line 288
**Edge case:** Delta pass 2, or a re-run after a red halt where an earlier section grew. An unresolved P0 or P1 has a line-only `Where` (no heading title). That line was inside the section the reviewer read in the predecessor `spec.copy.md`. A red round keeps the pre-dispatch copy (line 215); pass 2's text baseline is pass 1's pre-dispatch copy (line 318). The current spec's line numbers have moved. The cited section's exclusive body is unchanged, so the text diff does not name it.
**What happens:** Line 288 emits the innermost heading of the current spec that contains that line number. The delta contract then limits new critique to that heading's exclusive body. The section the finding actually cited is unnamed, so the pass can go green without re-checking it. The next `spec.copy.md` and `baseline.commit` record that text as reviewed. Decision 15 says an open finding's heading stays in scope when its text did not change.
**Why the spec misses it:** Placement is defined only against the spec being split for the current diff ("the current spec" in the pairing rules, lines 264–266). The predecessor copy is the file the report's line numbers belong to. A line that still falls inside the current file is treated as placed, so the every-heading fallback does not run.
**Suggested fix:** Resolve a line-only `Where` against the predecessor `spec.copy.md` (pass 1's pre-dispatch copy on delta pass 2). Take the heading by the same stack pairing, and emit that heading's pair in the current spec. A paired heading that was deleted is emitted as a deletion. A line that cannot be placed in the predecessor copy emits every current heading. A `Where` that names a heading by title (`§ Mode`, `### Mode`) matches that title and does not use the line. A `Where` whose path is not the spec emits every heading rather than mapping that file's line number into the spec.

### F-3: Code-drift commands have no deadline, so a hung git never becomes the failure token
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Changed regions, lines 270–275; spec § Docs line 394
**Edge case:** One of the four listings waits on a pager, a lock, or a stuck `git` and produces no exit. Classification is still before the pending write, or pass 2 is computing drift after the pending marker was written.
**What happens:** The failure class includes "a command that does not finish" (line 275), and there is no bound that makes that true. The run sits there. It does not select `mode: full (code-drift unavailable)` and does not take the pass-2 stop. The existing fetch commands in `SKILL.md` (lines 132 and 201) are wrapped in `timeout 30`. These new commands are not, and `--no-color` does not disable the pager.
**Why the spec misses it:** § Docs adds the commands to `## Tool-use notes` as read-only siblings of `git rev-parse` and does not give them the timeout the skill already uses for git.
**Suggested fix:** Run each listing as `git --no-pager` with the same `timeout 30` as `git fetch`. On expiry, use the failure already defined: `mode: full (code-drift unavailable)` during classification, and the pass-2 pending stop when a delta was already dispatched.

## Summary
P0: 0 | P1: 2 | P2: 1 | P3: 0 | P4: 0

STATUS: RED P0=0 P1=2 P2=1 P3=0 P4=0
