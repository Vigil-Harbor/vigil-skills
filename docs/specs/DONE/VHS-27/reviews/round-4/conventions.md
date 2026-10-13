# Conventions Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Ledger sample still teaches the old header while mode requires the word `next` | CLOSED | spec § Ledger lines 250–251: two sample edits; the header becomes `closure_manifest (round <N-1> → next):` with `next` literal, and the re-anchor sample is `fixed: re-anchored to § Design`. A `round 4 → 5` header is row 8 unreadable; `round 4 → next` is readable. Test plan line 455. |
| conventions | F-2 | The workflow-reference edit list never states the delta mode | CLOSED | spec § Docs line 394: Skill 1 states a re-run is at most two delta passes over changed regions and open P0/P1s, a clean no-op leaves the marker, and `--full` or a mode-table row forces a full pass. Test plan line 453. |
| conventions | F-3 | Delta pass 2 keeps an out-of-scope recount fold | CLOSED | spec Decision 8 line 72 and § Two counters lines 203–205: delta pass 2 uses the final-round recount rule and may keep a fold, including when the original finding is out-of-scope, because there is no third pass. |
| correctness | F-1 | A green marker with a non-empty delta has no classified exit | CLOSED | spec § No-op step 4 (line 173) recomputes the full-invocation `start` on a red empty pair. Step 7 (line 176) sends a green marker with either set non-empty to the pending write and a delta dispatch. Scenarios 2b and 10. |
| correctness | F-2 | The empty-pair Done-when sentence covers only the green no-op | CLOSED | spec § Done when line 470: the no-op is the green marker in scenario 2; a red marker with both sets empty is the full pass in scenario 15. |
| correctness | F-3 | ticket not cached | CLOSED | spec § Deferred (P2+) line 493 records no spec change. Re-filed below as this round's grounding note. |
| edge-cases | F-1 | A late full upgrade keeps the two-directory delta start | CLOSED | spec Decision 8 line 72, § Mode lines 160–164, § No-op step 4 line 173, scenario 16 line 436, and the test plan lines 448 and 455: a later full token discards `candidate + 1`, takes the smallest free span of `round_cap`, and leaves the marker unchanged when no span is free. |
| edge-cases | F-2 | A line-only Where is placed in the spec after the revision, so the open section drops out | CLOSED | spec Decision 15 line 100, § Changed regions line 289, § Dispatch line 319, scenario 17 line 438, and the test plan line 455: a line-only `Where` is resolved in the predecessor `spec.copy.md` and mapped by stack pairing. |
| edge-cases | F-3 | Code-drift commands have no deadline, so a hung git never becomes the failure token | CLOSED | spec Decision 5 line 60, § Changed regions lines 269–278, § Docs line 396, § Two counters line 204, scenario 12 line 428, and the test plan lines 447 and 456: each listing is `timeout 30 git --no-pager`, and expiry is the existing failure. |

The five round-qualified recount keeps remain folded in the sections the manifest names: the rename lists both paths (Decision 5, § Mode, § Changed regions, § Artifacts, § Two counters, scenario 14, test plan); the locator strip covers `path:line` (scenario 10, § Done when); an ancestor is emitted only when it is itself changed (§ Delta contract); a classifying git failure selects full mode before the pending write, and a pass-2 failure leaves the marker pending (scenario 12); a fingerprint mismatch still sets the candidate when `source:` is `review` and `round:` is a positive integer (Decision 14, scenario 2b). The spec has no `## Deferred — follow-up required` section. `## Deferred (P2+)` is a separate section, so the deferred-row routing checks do not apply.

## Findings

### F-1: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Convention violated:** Ticket lookup for silent-addition axis (b). The reviewer tool-use rule looks up the Plane work item when that axis needs the ticket's acceptance criteria.
**Evidence:** This run forbade the issue tracker and shared memory, so no ticket record was retrieved. The brief is the source used for Done when and Decisions 1–16. spec § Deferred (P2+) line 493 already records the same note for correctness/F-4, including the round-2 and round-3 re-files, with no spec change.
**Suggested fix:** None for the spec. The brief stays the source. Re-check the Plane ticket only if the mirror is later reachable and its wording differs from the brief.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
