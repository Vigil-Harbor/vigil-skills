# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Reader state `changed` never selects a candidate round
**Severity:** P0
**Where:** spec.md:126, spec § Mode rows 5–10, scenario 2b (spec.md:368), scenario 5 (spec.md:374)
**Claim:** "Read the marker with the existing six-state reader before the pending write replaces it. When the marker is `green` or `red` and its `round` is a positive integer, the candidate round is that integer." Row 5 matches only "Marker `green` and `source: operator-attested`". Row 7 matches only "review-green or review-red". Row 10 is "Otherwise" and prints `mode: delta (continuing round <candidate>)`. Scenario 2b: a review-green marker whose filtered spec differs from `spec.copy.md` is a delta pass at cumulative round 3. Scenario 5: an attested green is `mode: full (attested)`.
**Why this is wrong:** `skills/spec-cycle/SKILL.md:64-70` is that six-state reader. State `green` requires `verdict: green` and a computed fingerprint equal to the marker's. State `changed` is `verdict: green` when the fingerprint differs, the `fingerprint:` line is absent or `none`, or the fingerprint cannot be computed. The fingerprint (`SKILL.md:53`) and the spec's text filter (spec.md:130) drop the same bytes: carriage returns and lines whose first non-blank characters are `**Follow-up:**`. An operator edit after a review-green write therefore returns `changed`, and the candidate sentence never runs. Rows 5 and 7 do not name `changed`. Row 10 still interpolates `<candidate>`. Scenario 2b and brief Decision 1 (a re-run over a green marker runs delta passes when Decision 14's table allows) have no row that can fire. The same hole drops an attested marker whose spec no longer matches its fingerprint: row 5 requires reader state `green`, `round` is `not reviewed`, and Decision 14 still requires `full (attested)`. These lines were re-read at HEAD after `d3730b1` (2026-10-12), `7abe102` and `5f640d0` (2026-10-11), and `aad9971` (2026-10-08); the six-state table is unchanged.
**Suggested fix:** Resolve the mode from the marker fields `verdict:`, `source:`, and `round:`, and treat a fingerprint mismatch as a separate fact the text diff and code drift already compute. Set the candidate whenever `source: review` and `round` is a positive integer, including when the reader would return `changed`. Keep row 5 on `source: operator-attested` whether or not the fingerprint matches. Add a row only if some `changed` case must halt for confirmation; scenario 2b must still dispatch delta with that candidate.

### F-2: Green-round `spec.copy.md` is taken before post-green polish
**Severity:** P1
**Where:** spec § Artifacts (spec.md:200-205), spec § Ledger (spec.md:230-237), spec § Two counters (spec.md:190), scenario 2 (spec.md:366)
**Claim:** "`spec.copy.md` | Immediately before this round's reviewers are dispatched | Exact bytes of the spec file at that moment." "A green pass, on either counter, breaks the loop, runs post-green polish, writes the empty ledger, then Phase 3." "Polish does not change the ledger… Write the empty ledger even when polish edits the spec." Scenario 2 requires the filtered spec to equal that saved copy before the no-op fires.
**Why this is wrong:** The green marker's fingerprint is the spec as 2g left it (`skills/spec-cycle/SKILL.md:839`). 2g runs after the green break and before that write (`SKILL.md:802-833`). Step 2 creates or extends `## Deferred (P2+)` whenever the green round has a final-round P2. Step 4 writes `## Post-green polish` for every folded candidate and records every remaining final-round P2. A green round does not run 2e (`SKILL.md:806-807`), so those sections are new bytes after `spec.copy.md` was saved. The next re-run still has reader state `green` (fingerprint matches the post-polish spec), so F-1 does not apply, the candidate is set, and § No-op step 2 diffs against the pre-polish copy. The changed-region set is non-empty. Decision 11 and the brief's second Done-when bullet (a re-run with zero changed regions and zero open P0/P1 is a no-op that reports GREEN) do not hold on that path. Delta pass 2 must keep pass 1's pre-dispatch copy; the refresh belongs on the green exit only, after 2g and before the green marker.
**Suggested fix:** On the green path, after 2g and before the green marker, rewrite that round's `spec.copy.md` to the post-polish bytes (and `brief.copy.md` only if polish touched the brief, which it does not today). Leave the pre-dispatch copy in place for a loop-red round so delta pass 2 still diffs what pass 1's reviewers saw. State in scenario 2 that the saved copy is the post-polish spec.

### F-3: Output-contract closure line stays on the round-1 rule
**Severity:** P1
**Where:** spec § Delta contract (spec.md:307); `agents/spec-reviewer-correctness.md:174`, `agents/spec-reviewer-edge-cases.md:169`, `agents/spec-reviewer-conventions.md:163`, `agents/spec-reviewer-scalability.md:110`
**Claim:** "Step 7 runs when a `closure_manifest` was provided. When none was provided, the closure section is `N/A — no closure predecessor`, including when `round_number` is greater than 1." The same section replaces the `round_number` parenthetical `(1–4)` and does not mention the output contract.
**Why this is wrong:** All four agents still emit this template line: `(Required for round_number ≥ 2; "N/A — round 1" otherwise.)` at the lines above. § Delta contract names the step-7 guard and the `(1–4)` input bullet. It does not name that template. An implementer who edits only the named sites leaves the contract requiring a closure table whenever `round_number` is at least 2. Brief Decision 13 and spec.md:149 give the first pass of every full invocation no predecessor, and that pass's cumulative round is the next unused number, which is greater than 1 whenever `round-1/` already exists (scenario 8). The contract then requires a table the new step 7 forbids.
**Suggested fix:** In § Delta contract, name the output-contract parenthetical in all four agents and replace it with: the closure section is required when `closure_manifest` was provided; otherwise the section body is `N/A — no closure predecessor`.

### F-4: Ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Ticket VHS-27 is the canonical acceptance source when it conflicts with the brief.
**Why this is wrong:** Shared memory and Plane were unavailable for this run, and the review was instructed not to call them. No ticket record was retrieved. The brief is the source used for Done-when and Decisions 1–16.
**Suggested fix:** None for the spec. Re-check the Plane ticket when the mirror is reachable if its wording differs from the brief.

## Summary
P0: 1 | P1: 2 | P2: 0 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=2 P2=0 P3=1 P4=0
