# Correctness Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | A late full upgrade keeps the two-directory delta start | CLOSED | Decision 8 line 72 discards `candidate + 1` and recomputes the free span. Mode lines 160 and 164 and No-op step 4 line 173 do the same before any directory is created. Scenario 16 line 436 starts at 8 and leaves `round-7/` in place. Test plan lines 448 and 455. |
| edge-cases | F-2 | A line-only Where is placed in the spec after the revision, so the open section drops out | CLOSED | Decision 15 line 100 and Changed regions line 289 resolve a line-only `Where` against the predecessor `spec.copy.md`, then stack-pair into the current spec. Dispatch line 319 passes that paired heading. Scenario 17 line 438. Test plan line 455. |
| edge-cases | F-3 | Code-drift commands have no deadline, so a hung git never becomes the failure token | CLOSED | Changed regions lines 269–278 wrap `rev-parse` and the four listings in `timeout 30 git --no-pager`. Docs line 396 names the same commands. Test plan lines 447 and 456. |
| correctness | F-1 | A green marker with a non-empty delta has no classified exit | CLOSED | No-op step 7 line 176: a green marker with either set non-empty dispatches delta at `candidate + 1`. Scenarios 2b and 10 are named there. |
| correctness | F-2 | The empty-pair Done-when sentence covers only the green no-op | CLOSED | Done when line 470: the no-op is the green marker in scenario 2; a red marker with both sets empty is the full pass in scenario 15. |
| correctness | F-3 | ticket not cached | CLOSED | Deferred (P2+) line 493 records no spec change. Re-filed below as this round's grounding finding. |
| conventions | F-1 | Ledger sample still teaches the old header while mode requires the word `next` | CLOSED | Ledger lines 250–251: the § 2b sample header becomes `closure_manifest (round <N-1> → next):`, and `round 4 → 5` is row 8 unreadable. Test plan line 455. |
| conventions | F-2 | The workflow-reference edit list never states the delta mode | CLOSED | Docs line 394: Skill 1 states two delta passes, the clean no-op, and `--full` / mode-table full. Test plan line 453. |
| conventions | F-3 | Delta pass 2 keeps an out-of-scope recount fold | CLOSED | Decision 8 line 72 and Two counters line 204: pass 2 keeps the fold and does not revert, including when the original finding is out-of-scope. |

The closure manifest's seven `fixed` lines match those folds. `## Deferred (P2+)` is present once. There is no `## Deferred — follow-up required` section. Commits on the files this spec edits in the last 7 days: `d3730b1` (2026-10-12), `7abe102` and `5f640d0` (2026-10-11), `b1ab82b` (2026-10-10). HEAD is `c01286d`.

## Findings

### F-1: A STATUS-only open set still lets a red marker go green
**Severity:** P1
**Where:** spec § No-op steps 2–5, lines 171–174; spec § Dispatch line 317; spec § Delta contract lines 344–348; spec § Two counters line 206; spec § Scenarios line 434
**Claim:** "If a report's STATUS P0+P1 is greater than zero and it has no `### F-<k>:` heading of that severity, the open set contains `<lens>/STATUS (P0)` and the run is a delta, not a no-op and not a green write over the red marker."
**Why this is wrong:** Steps 2 and 3 and Dispatch line 317 add `<lens>/STATUS (P0)` when a standing report is missing, has no STATUS line, or has STATUS P0+P1 greater than zero and no `### F-<k>:` heading of that severity. That makes the open set non-empty, so step 4's full upgrade does not run. Step 5 dispatches delta. The prompt line names no heading. Changed regions line 289 emits a heading only from a `Where`. The delta-scope block (lines 344–348) applies critique only to headings named in `changed_regions` or `open_findings`, and the ledger check (line 360) counts a finding only when it has a `### F-<k>:` heading. A compliant reviewer with an empty changed-region set and a heading-less STATUS line files nothing and returns GREEN. Line 206 then breaks the loop and Phase 3 writes the green marker. The same path applies to a missing standing report, whose only signal is `<lens>/STATUS (P0)` with no section. Test plan line 455 checks only "Scenario 15 does not write green over a red marker from an empty delta," which is the both-sets-empty branch. The both-sets-empty branch is sound: it recomputes a full start and re-reads the spec. The STATUS-greater-than-zero branch does not.
**Suggested fix:** In No-op, after steps 2 and 3, if the open set contains any `<lens>/STATUS` line, replace the token with `mode: full (open findings unreadable)`, discard the delta start, and compute `start` with the full-invocation rule, the same as step 4. Say that in Decision 11, scenario 15, and the test plan. A heading-less pseudo-line is not a delta scope.

### F-2: Out of scope still says a delta pass uses the routing rules unchanged
**Severity:** P2
**Where:** spec § Out of scope line 482; spec § Decision 8 line 72; spec § Two counters line 204
**Claim:** "The routing rules and the gate formula. A delta pass uses them as they are."
**Why this is wrong:** Decision 8 and Two counters line 204 change one routing rule on delta pass 2: the recount may keep a fold and may not revert, including when the original finding is out-of-scope, because `2 ≤ P < round_cap` on `big` and `irreversible` would open a third delta pass. The skill today reverts that fold when `2 ≤ round < round_cap` (`skills/spec-cycle/SKILL.md` line 627). Line 204 is the rule an implementer follows. Line 482 still tells them the routing rules are used as they are. Brief Out of scope line 76 uses the same sentence; the pass-2 exception is already the recorded Decision 8 rule.
**Suggested fix:** In § Out of scope, carve out the pass-2 recount: a delta pass uses the routing rules and the gate formula as they are, except delta pass 2 keeps the fold and does not revert, as Decision 8 states. This edit belongs in the revision with F-1. Post-green polish does not edit Out of scope.

### F-3: Grill row templates still record `round_cap` on a delta halt
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Stop screens lines 373–375
**Claim:** "In `### 2f-i`, the seed read, the `grill.md` persist, and the re-render path use `round-<C>` on every halt."
**Why this is wrong:** Those three paths are named, and they still say `round-<round_cap>` at `skills/spec-cycle/SKILL.md` lines 701, 737, and 765. The row templates that 2f-i step 4 appends are not named. They still write `Deferred in: round <round_cap> (grill)` and `Scope: operator — round-<round_cap> grill` at `SKILL.md` lines 587, 602, and 608. A delta halt at cumulative round 6 on `big` (`round_cap` is 4) persists `grill.md` under `round-6/` and records the row as round 4. Closure does not read `grill.md`, so the gate still runs. The recorded round is wrong.
**Suggested fix:** In § Stop screens, name those three template strings as edit sites and substitute `C` for `round_cap` in `Deferred in:` and in the `operator — round-<C> grill` scope token.

### F-4: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Ticket VHS-27 is the canonical acceptance source when it conflicts with the brief.
**Why this is wrong:** This run was instructed not to call shared memory or the tracker. No ticket record was retrieved. The brief is the source used for Done when and Decisions 1–16. The spec already records that under `## Deferred (P2+)`.
**Suggested fix:** None for the spec. Re-check the Plane ticket when the mirror is reachable if its wording differs from the brief.

## Summary

P0: 0 | P1: 1 | P2: 2 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=1 P4=0
