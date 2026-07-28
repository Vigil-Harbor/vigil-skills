# Conventions Review — round 1

## Closure of round <N-1> findings

N/A — round 1 (v2 spec). The v1 review history (`docs/specs/TODO/VHS-5.reviews/v1/round-{1,2}/`) is informational only for this run; v2 is a structural rewrite (drops the Phase 6a "Location A" edit entirely), so v1 closure tracking does not apply. The spec itself acknowledges this in § Goal and Decision 5.

## Findings

### F-1: Test command shape diverges from prior VHS specs but the divergence is structurally required

**Severity:** P3
**Where:** spec.md:171 (Test command)
**Convention violated:** Prior VHS spec test-command pattern. VHS-3:253, VHS-4:270, VHS-6:227 all use `python sync.py status && grep -c <pattern> <file> && ...` — bare `grep -c` chained via `&&`, each clause's non-zero count satisfies `&&`. VHS-1:429 uses `python sync.py status` + a `python -c json.load` rather than greps.
**Evidence:** VHS-5 spec line 171 uses `test "$(grep -c <pat> <file>)" -ge "1"` (and `= "0"` for two absence assertions: `--stat` count = 0 and `2-minute polling window` count = 0). The structural divergence is forced by the absence assertions: a bare `grep -c '--stat' file` exits 1 on zero matches, which would fail the `&&` chain when zero is the desired outcome. The spec explicitly documents (§ Test plan note on lines 159) why `python sync.py status &&` is also dropped: it does not exit non-zero so chaining it is decorative, and pre-existing peon-ping / states.json drift would clutter the report. Both explanations are sound. This is exactly the same disposition v1 round 2 reached on the equivalent finding.
**Suggested fix:** None required. The spec's deviation is self-documented in the surrounding prose. Optional micro-edit: add a single sentence inside the Test command code block (or immediately below it) calling out "absence-assertion forces `test "$(...)"` wrapper" — that prevents a future maintainer from "converging" the shape with VHS-3/4/6 without realizing the `--stat = 0` clause forbids it.

### F-2: Spec references a CLAUDE.md comment-style rule that does not exist in this repo

**Severity:** P4
**Where:** spec.md §§ "P0 edit" (lines 90-92, the `Note:` block proposed above the GraphQL filter) — the spec itself does not cite CLAUDE.md, but the review-context for this round explicitly invokes one
**Convention violated:** None — the rule cited in the round-context prompt (`CLAUDE.md`: "Default to writing no comments. Only add one when the WHY is non-obvious") **is not present in `vigil-skills/CLAUDE.md`**. Grep of CLAUDE.md for `no comments|non-obvious|WHY` returns zero matches; the file's 78 lines cover sync commands, architecture, file layout, and YAML-frontmatter conventions but contain no prose-comment-style guidance. The same observation was logged in v1 round-2 conventions F-2.
**Evidence:** Spec lines 90-92 propose a ~36-word `Note:` block explaining why the GraphQL site uses `coderabbitai` while REST sites elsewhere use `coderabbitai[bot]`. The WHY *is* genuinely non-obvious — REST/GraphQL bot-login asymmetry is the precise failure mode the P0 bug embodies, and a future "helpful" edit re-adding the suffix is exactly the regression this comment prevents. The comment passes the spirit of the (informal) "WHY non-obvious" rule even though the rule isn't formalized in this repo.
**Suggested fix:** None required. If the spec author wants to be terser, collapse the `Note:` to one line ("GraphQL bot login is `coderabbitai` — REST returns the `[bot]` suffix; this jq runs against GraphQL"). Either form is acceptable. The framing in the round-context prompt mis-attributes the rule to CLAUDE.md, but the spec itself does not make that mis-attribution.

### F-3: Cross-edit verbatim-duplication is well-justified at N=2

**Severity:** Informational (no finding)
**Where:** spec.md § Cross-edit consistency (lines 144-146)
**Convention violated:** None. The `spec-reviewer-conventions` prompt's "three similar lines is better than a premature abstraction" rule sets the threshold at N≥3 for extraction. v1 had three copies and the conventions reviewer was already fine with that; v2 reduces to two copies, well below the threshold.
**Evidence:** The shared ~20-word phrase ("The attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back") appears in exactly two Phase 6d locations after the edit. Section is explicitly defended in spec (lines 144-146) and the defense is correct.
**Suggested fix:** None.

### F-4: Backwards-compat rejection (Decision 1) is the right call

**Severity:** Informational (no finding)
**Where:** spec.md § Decision 1 (lines 22-34)
**Convention violated:** None.
**Evidence:** Decision 1 fixes the jq filter to `"coderabbitai"` and explicitly forbids `or "coderabbitai[bot]"`. The repo's general posture (CLAUDE.md, prior VHS specs) is "trust framework guarantees; don't add shims for cases that cannot occur" — GitHub's GraphQL API contractually returns `coderabbitai` (no suffix) at this call site, so an `or` clause would be a shim against a case that does not exist in this surface. Rejecting it is consistent with "single source of truth; match what GraphQL actually returns" (spec line 32). The REST jq filters elsewhere in the skill (line 64, 66, 70, 169, 190, 202, 206, 224, 319) continue to use `coderabbitai[bot]` — correct for REST — and the spec § Out of scope (line 195) explicitly preserves this asymmetry.

### F-5: Decision 5 (acknowledge VHS-4 overlap) is non-standard but earns its keep

**Severity:** P4
**Where:** spec.md § Decision 5 (lines 70-72)
**Convention violated:** None — this is a structural-style observation. Prior VHS specs do not have an analogous "Decision N — acknowledge prior overlap" section because none had the v1-stale-vs-v2 history this spec carries.
**Evidence:** The section is short (3 lines of body) and load-bearing: it explains to a future reader why v2's cadence rewrite covers only two of the three sites the brief named, preventing the natural "you missed a site" confusion when diffing the spec against the brief. Without it, a careful reader has to assemble the rationale themselves from § Goal + Decision 3 + § Scope. With it, the rationale lives in one place. Not defensive — informative. The bar for adding a non-standard decision is "does it save a future reader meaningful confusion?"; this clears it.
**Suggested fix:** None. Optional: consider shortening the heading to "Decision 5 — Scope reconciliation with VHS-4" or similar (drops "explicitly" which is the only word that reads slightly defensive). Pure nit.

### F-6: VHS-6 mention in § References is appropriately scoped

**Severity:** Informational (no finding)
**Where:** spec.md § References (line 203)
**Convention violated:** None.
**Evidence:** The reference reads "PR #7 (VHS-6) — added upstream-staleness check to spec-cycle Phase 0 (which, if installed, would have flagged v1's stale anchors before review)". This is descriptive (explains the historical context for why v1 went stale) rather than prescriptive (the spec does not propose changing anything about VHS-6 or relying on its check). It belongs in References because it provides causal context for the v1→v2 history that opens the spec. Not out-of-scope drift.

### F-7: No contradiction with prior wiki decisions

**Severity:** Informational (no finding)
**Where:** N/A
**Convention violated:** None.
**Evidence:** Scanned `vigil-harbor-wiki/decisions/` (48 entries). Grep for `review-pr|FAST_PATH|FIRST_POLL_TIME|coderabbit|GraphQL|polling cadence` returns zero matching files. None of the decisions touch `/review-pr` semantics. The closest related entries (`2026-05-06-vigil-skills-spec-review-hardening` in comprehension; `2026-05-08-vhs-1-plane-reads-onto-mcp-cache` in comprehension) are orthogonal. Spec's Decision 3 alignment with VHS-4's FAST_PATH/FIRST_POLL_TIME design is anchored against `projects/vigil-skills/state.md` (which records the VHS-4 shipment) and `filemap.md` (which records the per-PR update history); no decisions-page contradiction is possible because the design was never written up as a wiki decision. The spec's prose description of Phase 6a (FAST_PATH predicate, FIRST_POLL_TIME wall-clock bound, 5-minute total / 10-minute extended) matches what state.md describes and what the current SKILL.md lines 149-218 actually contain.

### F-8: Silent spec additions check — clean

**Severity:** Informational (no finding)
**Where:** Decisions 1-5
**Convention violated:** None.
**Evidence:** Walking the five Decisions through the (a)/(b)/(c)/(d) classification:
- **Decision 1** (drop `[bot]`, no `or` clause): brief Decision 1 says "whether to also drop the suffix check entirely vs. accept both forms is the spec author's call". Category (c) — spec-level addition with explicit rationale (the GraphQL surface cannot return the suffixed form). Authorized.
- **Decision 2** (`--name-only`): brief Decision 2 says "Spec author picks one with one-line rationale". Category (a) — authorized by brief.
- **Decision 3** (P2 doc rewrite for 6d only, leave 6a untouched): brief Decision 3 permits doc-vs-enforce as a binary choice, but the brief listed three sites (6a + two 6d sites); restricting to two is a category (c) spec-level addition. The spec defends this explicitly in Decision 3 itself (VHS-4 addressed 6a via wall-clock enforcement, not aspirational-cadence relabeling) and in Decision 5. Authorized with rationale.
- **Decision 4** (no broader restructuring): brief Decision 4 same. Category (a).
- **Decision 5** (acknowledge VHS-4 overlap): meta-decision; category (c), informational. Authorized.
No silent (d)-category drift.

### F-9: Test plan acknowledges the no-test-suite stance correctly

**Severity:** Informational (no finding)
**Where:** spec.md § Test plan (lines 148-166)
**Convention violated:** None.
**Evidence:** Test plan opens with a verbatim citation of CLAUDE.md's "no build step, no test suite, no dependencies beyond Python 3.8+ stdlib". Falls back to structural greps + manual verification, matching the pattern established by VHS-1 (json.load + sync status), VHS-3, VHS-4, VHS-6 (sync status + grep counts). Done-when #6 maps to the Test command exit code. Done-when #5 (post-`sync.py push` cleanliness) is correctly carved out as a manual post-push check rather than gated by the Test command — this matches the brief's Done-when #5 framing and is consistent with the v1 round-2 conventions disposition.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 2

STATUS: GREEN
