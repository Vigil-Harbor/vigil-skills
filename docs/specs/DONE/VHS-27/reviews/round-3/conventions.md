# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Workflow reference still describes one round counter outside the named edit sites | CLOSED | spec § Docs line 391 names the Skill 0 grilling contract, the Phase 2 introduction (steps 6–8 and the FROZEN window `1 .. round_cap-1`), and the adapting bullet `**Targeted rewrite at round round_cap**`, all read as pass index `P`. Test plan line 450. |
| correctness | F-2 | Ticket not cached | CLOSED | spec § Deferred (P2+) line 487 keeps the grounding note and records no spec change. |
| edge-cases | F-1 | A renamed cited file never becomes a changed path, so the no-op sticks | CLOSED | Decision 5 line 60, § Changed regions lines 268–277 (`--no-renames`, `core.quotePath=false`, raw-path failure, "a command that does not finish", snapshot SHA), § Artifacts lines 217 and 230, § Two counters line 203, scenario 14 line 430, test plan line 449. |
| edge-cases | F-2 | Two headings with the same line can hide an edit | CLOSED | Decision 15 line 100 and § Changed regions lines 262–266: stack pairing, exclusive body, and emit-every-heading when filtered bytes differ and pairing explains nothing. |
| edge-cases | F-3 | A red marker whose P0/P1 headings do not parse can be replaced with green | CLOSED | § No-op steps 3–4 lines 172–173, § Dispatch line 316 (`<lens>/STATUS (P0)`), scenario 15 line 432, Decision 11 line 84. |
| conventions | F-1 | Grill paths in `### 2f-i` are not an edit site | CLOSED | § Stop screens lines 373–374 name the `### 2f-i` seed, persist, and re-render as `round-<C>`. Test plan line 450. |
| conventions | F-2 | Three workflow-reference sentences still treat `round_cap` as the cumulative round | CLOSED | Same § Docs paragraph as correctness F-1, line 391. Test plan line 450. |
| conventions | F-3 | New git commands are not added to `## Tool-use notes` | CLOSED | § Docs line 394 lists the three read-only code-drift commands beside `git rev-parse` and keeps the lone-mutation sentence. Test plan line 450. |
| conventions | F-4 | Changed-region headings do not reuse the skill's heading boundary | CLOSED | § Changed regions line 262 uses `^#{1,6}\s` and the Deferred-section fences, the same boundary as `skills/spec-cycle/SKILL.md` steps 8–9 (lines 296 and 347). |

## Findings

### F-1: Ledger sample still teaches the old header while mode requires the word `next`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Ledger lines 245–249; spec § Mode line 138
**Convention violated:** One line shape for the closure manifest. The skill's § 2b sample is the bytes a later round copies (`skills/spec-cycle/SKILL.md` lines 435–437).
**Evidence:** Mode row 8 accepts a ledger only when the first non-blank line is `closure_manifest (round <digits> → next):` (spec line 138), and the ledger fence writes that header (spec line 245). The next sentence says the line shape is the shape § 2b already uses, with one edit, and names only the re-anchor: the sample becomes `fixed: re-anchored to § Design` (spec line 249). The live sample is still:

```text
closure_manifest (round <N-1> → <N>):
  - correctness/F-2 (P1) "stale anchor in § Design" — fixed: re-anchored to SKILL.md:142
```

(`SKILL.md` lines 435–437). An edit that follows the fence writes a readable ledger. An edit that follows "one edit" and leaves `<N>` in the header fails row 8 on every re-run (`mode: full (ledger unreadable)`), so the no-op never runs.
**Suggested fix:** In § Ledger, state that the § 2b sample header also becomes `closure_manifest (round <N-1> → next):`, with `next` the literal word, and that this is the second sample edit beside the re-anchor. Say the mode check and the on-disk ledger use that same header. In the test plan, a ledger headed `round 4 → 5` is row 8 unreadable, and a ledger headed `round 4 → next` is readable.

### F-2: The workflow-reference edit list never states the delta mode
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Docs lines 385–392; spec Decision 16 lines 102–104; spec § Scope line 22
**Convention violated:** Brief Decision 16 and the brief Scope row require `docs/spec-workflow-reference.md` to state the delta mode (brief lines 34 and 54). Spec Decision 16 repeats that and says it is honored by § Docs.
**Evidence:** § Docs tells that file to add `[--full]`, to read Round 2+, the verdict `round`, the Stakes tier, and the remaining single-counter sentences as pass index `P`, and to state the PET-166 numbers (spec lines 387–392). The two-pass sentence is specified only for `AGENTS.md` (spec line 396). The test plan checks the numbers and the pass-index reading for the workflow reference, and checks delta mode only on `AGENTS.md` (spec line 447). The reference's Phase 2 still says each lens reviews the spec, with revision while `round < round_cap` (`docs/spec-workflow-reference.md` lines 70–77). § Docs names no replacement paragraph for that.
**Suggested fix:** Add a § Docs bullet that Skill 1 of `docs/spec-workflow-reference.md` states a re-run is at most two delta passes over changed regions and open P0/P1s, that a clean no-op leaves the marker, and that `--full` or a mode-table row forces a full pass. Add that sentence to the test-plan checklist beside the PET-166 check.

### F-3: Delta pass 2 keeps an out-of-scope recount fold
**Severity:** P3
**Where:** spec § Two counters lines 203–204; spec Decision 8 lines 70–72
**Convention violated:** Brief Out of scope says a delta pass uses VHS-43's routing rules as they are (brief line 76). The skill reverts an out-of-scope original fold when `2 ≤ round < round_cap` (`SKILL.md` line 627).
**Evidence:** This is a spec-level addition with rationale, already written in § Two counters: pass 2 "may not revert" because `P = 2` is still below `round_cap` on `big` and `irreversible`, and substituting `P` into `P < round_cap` would open a third delta pass (spec lines 203–204). Decision 8 records the fold and the halt (spec lines 70–72) and does not record that the recount uses the final-round rule, including when the original finding is out-of-scope. Brief Decision 8 authorizes the two-pass budget and the halt.
**Suggested fix:** Add one sentence to Decision 8: delta pass 2 uses the final-round recount rule (keep the fold, do not revert) because there is no third pass, including when the original finding is out-of-scope.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 1 | P4: 0

STATUS: GREEN
