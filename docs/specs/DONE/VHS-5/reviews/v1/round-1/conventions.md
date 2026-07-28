# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: Test command uses `grep -c` chained with `&&` and string equality, but `grep -c` returns nonzero exit on zero matches — the chain breaks correctly only because each expected count is non-zero. The deeper concern is portability: VHS-1/VHS-3/VHS-4/VHS-6 all use `grep -c "<pattern>" <file>` as a count printer, never as an exit gate via `test "$(grep -c ...)" = "0"`

**Severity:** P2
**Where:** spec.md § Test command (line 159)
**Convention violated:** Prior VHS test-command pattern. VHS-3 line 253: `python sync.py status && grep -c "@coderabbitai resolve" skills/review-pr/SKILL.md && grep -c "comments.*replies" skills/review-pr/SKILL.md`. VHS-4 line 270 and VHS-6 line 227 follow the same shape — bare `grep -c` invocations chained with `&&`, where the test passes when each grep prints a non-zero count. None of the prior specs wrap grep counts in `test "$(...)" = "N"` assertions.
**Evidence:** VHS-3 `Test command`: bare `grep -c` chain. VHS-5 spec: `test "$(grep -c '"coderabbitai\[bot\]"' skills/review-pr/SKILL.md)" = "6"` — a structurally different shape. The new shape is stricter (asserts an exact count), but it also asserts a load-bearing magic number (`= "6"`) that depends on counts at REST sites the spec is not changing. If any unrelated future edit adds or removes a `"coderabbitai[bot]"` REST literal at lines 66/70/158/168/181/276, the test command for VHS-5 breaks even though the VHS-5 fix remains correct. This is a brittleness drift away from the prior VHS pattern.
**Suggested fix:** Either (a) loosen the assertion to `-le "6"` or simply drop the equality and assert `grep -c '"coderabbitai\[bot\]"' skills/review-pr/SKILL.md` returns non-zero plus a separate assertion that the GraphQL filter at line 241 uses `"coderabbitai")` (e.g., grep for the suffix `coderabbitai")` which only matches the GraphQL site), or (b) call out explicitly in the spec that the "= 6" assertion is the spec's snapshot of HEAD and any unrelated REST-literal change requires updating this test command. Option (a) is preferred — it matches the prior-VHS pattern more closely and survives unrelated edits.

### F-2: Comment text injected at SKILL.md line 241 explains REST-vs-GraphQL login difference inline. The spec defends three verbatim copies of the "intervals are aspirational" phrase on the "three similar lines is better than a premature abstraction" principle, then adds a single ~50-word comment whose WHY is genuinely non-obvious (GitHub's GraphQL API drops the `[bot]` suffix). The comment is justified, but the wording is more verbose than the rest of the skill's note style

**Severity:** P3
**Where:** spec.md § P0 edit (lines 75-77) / Design block
**Convention violated:** SKILL.md's existing comment style. Looking at lines 64, 69, 84, 154 of the current SKILL.md, the in-fence comments are 1-line `#`-prefixed hints, e.g., `# Get the PR's diff scope — helps contextualize findings`. The proposed comment is a 3-sentence prose block immediately above the code fence. That's idiomatically fine for a markdown skill, but it's structurally heavier than the surrounding "note:" comments in the file.
**Evidence:** Existing skill comments in SKILL.md (lines 64, 69, 84, 154) are terse one-line `#` annotations inside the code fence. The proposed VHS-5 comment is markdown prose outside the fence.
**Suggested fix:** Either shorten to a one-line note (e.g., "Note: GraphQL returns `coderabbitai`; REST returns `coderabbitai[bot]`. The filter below runs against GraphQL data.") or keep the verbose form but acknowledge in the spec that the longer form is intentional because the WHY (REST/GraphQL parity surprise) is the exact failure mode that produced this bug. Either is acceptable; the spec should make the choice explicit. The comment does meet the "WHY non-obvious" bar — the same bug recurring in 3 months would be a meaningful cost — so I am not recommending removal.

### F-3: P0 decision rationale uses an argumentative aside ("cargo-cult code") that reads as editorializing rather than referencing a concrete convention

**Severity:** P4
**Where:** spec.md § Decision 1 (line 29)
**Convention violated:** Tone. CLAUDE.md does not contain a "cargo-cult code" prohibition by name. The spec's reasoning is sound — adding `or "coderabbitai[bot]"` at a site GraphQL never reaches really is dead-code — but framing it as "cargo-cult" without citing the convention reads as personal style. The reviewer task brief mentioned "trust internal code and framework guarantees; don't validate against scenarios that can't happen." That principle is the right one to cite explicitly.
**Evidence:** Spec line 29: "adding `or "coderabbitai[bot]"` would be cargo-cult code: it can never match the GraphQL surface this jq runs against." Reviewer task brief: "trust internal code and framework guarantees; don't validate against scenarios that can't happen."
**Suggested fix:** Replace "would be cargo-cult code" with a phrase that names the convention directly, e.g., "would add a clause that can never fire — defensive code for a scenario the GraphQL contract excludes." Pure prose nit; the decision itself is correct.

### F-4: Spec correctly accounts for the "no test suite" stance, but the Test command rationale block (line 162) introduces a small assertion that the spec author did NOT state in the brief

**Severity:** P4
**Where:** spec.md § Test command rationale (line 162)
**Convention violated:** Silent spec additions vs the brief (spec-reviewer-conventions task instruction). The spec adds an exact-count assertion (`= "6"` for REST `"coderabbitai[bot]"` occurrences, `= "3"` for the new "intervals are aspirational" phrase) with the rationale that this verifies the spec's claimed mechanical changes. The brief never required exact counts — the brief's Done-when is structural (`grep` for presence). The exact-count form is a spec-level decision, not authorized by the brief.
**Evidence:** Brief Done-when #1–#3 describe behavior, not exact occurrence counts. The "exact 6" and "exact 3" assertions are spec additions with rationale (Decision-3 in the test command block: "the six REST occurrences remain at lines 66/70/158/168/181/276"). Per the reviewer task brief's "silent spec additions" check, this is category (c) — spec-level addition with rationale — which is fine (P3 normally). It's a P4 here because the rationale is articulated in the spec body, just not flagged as an explicit decision.
**Suggested fix:** Promote the "exact count" assertion to an explicit Decision (e.g., "Decision 5 — test command asserts exact occurrence counts as a regression brake on accidental REST-literal edits") or downgrade to a soft assertion as proposed in F-1. The current placement (buried in the test-command rationale) makes the brittleness contract less visible. Either edit closes the drift.

### F-5: Spec's "Cross-edit consistency" defense (line 135) explicitly invokes the "three similar lines" threshold from CLAUDE.md, but CLAUDE.md does not actually state that threshold — it appears only in the reviewer's task brief

**Severity:** P4
**Where:** spec.md § Cross-edit consistency (line 135)
**Convention violated:** Citation accuracy. The spec says "Three copies × ~20 words is well below the 'three similar lines → premature abstraction' threshold." That phrasing implies a written convention. `vigil-skills/CLAUDE.md` does not contain the "three similar lines" phrase — it appears in the reviewer agent's prompt template (the lens this review uses), not in the repo's CLAUDE.md.
**Evidence:** Grep for "three similar lines" in `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\CLAUDE.md` returns no matches. The phrase is from the reviewer task prompt: "Three similar lines is better than a premature abstraction."
**Suggested fix:** Either drop the implied citation ("Three copies × ~20 words is well below the abstraction threshold") or attribute it to the reviewer convention rather than CLAUDE.md. The substantive call (keep three verbatim copies) is correct — the three identical clauses at N=3 callsites with self-contained spec readability are the right outcome. This is a pure citation nit.

### F-6: Wiki check — no conflicting decisions, but the wiki's `state.md` for vigil-skills (last updated 2026-05-11) is not aware VHS-5 exists. Not a finding against the spec, but worth surfacing

**Severity:** P4
**Where:** N/A (wiki gap, not a spec defect)
**Convention violated:** None — wiki gap is downstream of merge, handled by `/wiki-after-merge` per CLAUDE.md.
**Evidence:** `vigil-harbor-wiki/projects/vigil-skills/state.md` line 25: "(VHS-2 and VHS-5 existence/status not tracked here — verify in Plane if planning next sprint)". No decisions in `vigil-harbor-wiki/decisions/` mention `/review-pr`, the GraphQL author filter, or the polling-cadence question. No comprehension entries contradict or duplicate VHS-5's approach.
**Suggested fix:** None for this spec. `/wiki-after-merge` will produce the comprehension entry and state.md update post-merge per the established workflow. Just noting that no prior decision blocks any of VHS-5's choices.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 4

STATUS: GREEN
