# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Workflow reference still describes one round counter outside the named edit sites | CLOSED | spec § Docs lines 390–391 names Skill 0 `### The grilling contract`, the Phase 2 introduction (halt/rewrite steps and the FROZEN window `1 .. round_cap-1`), and `**Targeted rewrite at round round_cap**`, each as pass index `P`. Those sentences are still the single-counter text at `docs/spec-workflow-reference.md:31`, `:72`, `:90–92`, and `:307`. |
| correctness | F-2 | Ticket not cached | CLOSED | spec `## Deferred (P2+)` lines 485–487 records no spec change. Re-filed below as this round's grounding finding. |
| edge-cases | F-1 | A renamed cited file never becomes a changed path, so the no-op sticks | CLOSED | spec § Decision 5 lines 58–60, § Mode line 160, § Changed regions lines 268–275, § Artifacts lines 217 and 230, § Two counters line 203, scenarios 12 and 14, § Test plan lines 441 and 449. One snapshot, `-c core.quotePath=false --no-color --no-renames`, a non-raw line selects `mode: full (code-drift unavailable)`, and that same SHA is written. On this tree `git diff --name-only` prints forward slashes, and raw `git rev-parse HEAD` is 40 lowercase hex digits plus one LF. Line 275 defines a clean all-raw listing as complete, so a truncated-but-well-formed listing is the stated rule, not a leftover hole. |
| edge-cases | F-2 | Two headings with the same line can hide an edit | CLOSED | spec § Changed regions lines 263–266: pair by the stack, nth with nth; `(before first heading)`; if filtered bytes differ and the set would be empty, emit every heading. |
| edge-cases | F-3 | A red marker whose P0/P1 headings do not parse can be replaced with green | CLOSED | spec § Decision 11 lines 82–84, § No-op steps 3–4 (lines 172–173), § Dispatch line 316, scenario 15 line 432. STATUS P0+P1 with no `### F-<k>:` heading adds `<lens>/STATUS (P0)`. A red marker with both sets empty is `mode: full (open findings unreadable)`. |
| conventions | F-1 | Grill paths in `### 2f-i` are not an edit site | CLOSED | spec § Stop screens lines 374–375 names the seed read, the `grill.md` persist, and the re-render path as `round-<C>`. Those three still say `round-<round_cap>` at `skills/spec-cycle/SKILL.md:701`, `:737`, and `:765`. |
| conventions | F-2 | Three workflow-reference sentences still treat `round_cap` as the cumulative round | CLOSED | Same sites as correctness F-1: spec § Docs line 391. |
| conventions | F-3 | New git commands are not added to `## Tool-use notes` | CLOSED | spec § Docs lines 393–394 names `## Tool-use notes` and the three read-only commands, and keeps the lone-mutation sentence. That inventory is still `skills/spec-cycle/SKILL.md:935`. |
| conventions | F-4 | Changed-region headings do not reuse the skill's heading boundary | CLOSED | spec § Changed regions line 262 uses `^#{1,6}\s`. The skill uses that boundary at `skills/spec-cycle/SKILL.md:299` and `:351`. |

The three round-qualified keeps are still in the sections the manifest names: locator strip at § Changed regions lines 281–282 and scenario 10; exclusive bodies at lines 264–265 and § Delta contract line 345; classifying git failure before the pending write at § Mode line 160, with the pass-2 pending stop at § Two counters line 203 and scenario 12.

## Findings

### F-1: A green marker with a non-empty delta has no classified exit
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § No-op, lines 170–175
**Claim:** "If `verdict:` is `red` and either set is non-empty: this is not a no-op. Continue to the pending write and dispatch delta." Step 6 stops when both sets are empty and the scan was clean, and "This step is reached only when `verdict:` is `green`."
**Why this is wrong:** Scenarios 2b and 10 are the green marker with a non-empty changed-region set (edited spec text, or a cited file changed, including `` `skills/spec-cycle/SKILL.md:388` ``). Steps 4 and 5 match only `verdict: red`. Step 6 matches only both sets empty. The six steps never say to dispatch that green path. § Dispatch line 292 and those scenarios do: pending write, then delta. Step 4's "Run the full loop" also needs the start in § Mode line 162 (smallest free span of `round_cap` directories). Row 11 has already chosen `candidate + 1`, which reserves only two directories.
**Suggested fix:** After step 6, state that a green marker with either set non-empty continues to the pending write and dispatches delta. In step 4, state that start is recomputed by the full-invocation rule in § Mode.

### F-2: The empty-pair Done-when sentence covers only the green no-op
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Done when, line 464
**Claim:** "A delta pass on a spec with zero changed regions and zero open P0/P1 findings is a no-op that reports green and does not run a full pass. — § No-op, scenario 2"
**Why this is wrong:** Decision 11 (lines 82–84), § No-op step 4 (line 173), and scenario 15 (line 432) agree with each other: a red marker whose changed-region set and open-finding set are both empty is `mode: full (open findings unreadable)`. Step 6 and scenario 2 are the green no-op. The acceptance sentence, read on its own, rejects the red exit the algorithm requires.
**Suggested fix:** Add a parenthetical on that bullet: the no-op is the green marker in scenario 2; a red marker with both sets empty is the full pass in scenario 15.

### F-3: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Ticket VHS-27 is the canonical acceptance source when it conflicts with the brief.
**Why this is wrong:** This run was instructed not to call shared memory or the tracker. No ticket record was retrieved. The brief is the source used for Done when and Decisions 1–16. The spec already records that under `## Deferred (P2+)`.
**Suggested fix:** None for the spec. Re-check the Plane ticket when the mirror is reachable if its wording differs from the brief.

## Summary

Commits in the last 7 days on the files this spec edits: `d3730b1` (2026-10-12), `7abe102` and `5f640d0` (2026-10-11), `b1ab82b` (2026-10-10). HEAD is `c01286d` on `main`. The spec names headings, and those headings still match the skill, the four agents, the workflow reference, and `AGENTS.md`. There is no `## Deferred — follow-up required` section, so the deferred-row routing checks do not apply.

P0: 0 | P1: 0 | P2: 2 | P3: 1 | P4: 0

STATUS: GREEN
