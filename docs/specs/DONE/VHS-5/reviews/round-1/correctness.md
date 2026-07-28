# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1 (this is the v2 spec's first review pass; v1 reviews are preserved at `docs/specs/TODO/VHS-5.reviews/v1/` but per orchestrator instructions are not used for closure, as v2 is a structural rewrite, not a continuation).

## Grounding summary

- Spec read: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-5.spec.md` (205 lines).
- Brief read: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-5.brief.md` (65 lines).
- CLAUDE.md read.
- Skill source verified at HEAD `19d2d98` (matches spec's cited commit): `skills/review-pr/SKILL.md`, 374 lines total.
- Plane MCP cache: tag-only search for `["plane_work_item","VHS-5"]` in namespace `vhs` returned 0 results (cache miss — see F-5 below).
- Git log on the touched file: most recent commit is `fcc5ee9` (VHS-4 fast-path / CI-check). The spec already accounts for this — Decision 3 names it explicitly.

Verification of every cited line:

| Cited | Actual content (verified) | Matches spec? |
|---|---|---|
| line 40 | `gh pr diff <N> --stat` | yes |
| lines 156–214 | Phase 6a containing `FAST_PATH` (line 160), `FIRST_POLL_TIME` (line 185), 5-min wall-clock bound extending to 10 min (line 210) | yes |
| line 185 | "Poll by making **individual Bash tool calls** every 15 seconds. Note the wall-clock time at first poll as `FIRST_POLL_TIME`…" | yes — confirms the inter-poll "every 15 seconds" claim in 6a is still present and unenforced at per-call granularity, exactly as Decision 3 admits |
| line 284 | `}' --jq '… select(.comments.nodes[0].author.login == "coderabbitai[bot]")]}'` | yes |
| line 295 | "Poll by making **individual Bash tool calls** (not a sleep loop — sleep loops are blocked in this environment). Check every 15 seconds, up to 2 minutes." | yes |
| line 297 | "If after the 2-minute polling window some threads are still unresolved, report the unresolved thread file paths and the manual resolve command:" | yes |
| line 322 | "Poll by making **individual Bash tool calls** every 20 seconds, up to 3 minutes." | yes |

Other code claims verified:

- Decision 3's attempt-count derivation: 2 min / 15s = 8 attempts; 3 min / 20s = 9 attempts. Arithmetic correct.
- Only one `--stat` occurrence in the file (line 40). Spec's test grep `--stat = 0` will fire correctly.
- Nine `coderabbitai[bot]` occurrences in the file, eight of which are REST-API jq filters (lines 64, 66, 70, 169, 190, 202, 206, 224, 319) plus one comment text at line 64. The only GraphQL filter is line 284. Spec's claim that the P0 fix targets only the GraphQL site is correct; preserving the REST `coderabbitai[bot]` literals (called out in § Out of scope) is also correct.
- `/ship-spec` does cut from `origin/<default-branch>` (verified at `skills/ship-spec/SKILL.md` line 75), so Done-when #4's "merge-base..HEAD" framing holds.

## Findings

### F-1: Brief Done-when #3 not literally satisfied for Phase 6a — inter-poll cadence wording remains aspirational and uncaveated in the file

**Severity:** P2
**Where:** spec § Decision 3 (lines 46–64) and § Done when, item 3 (line 182); brief § Done when, item 3 (line 48).

**Claim:** Spec asserts the brief's Done-when #3 ("the 6a / 6d cadence text either matches actual runtime behavior (intervals enforced) or the wording is revised to reflect that intervals are not enforced") is "satisfied by VHS-4 for 6a and by this spec for 6d."

**Why this is wrong (or rather: nuance the spec papers over):** Brief Done-when #3 talks specifically about the *cadence text* in the file. After VHS-4, Phase 6a line 185 still reads "Poll by making **individual Bash tool calls** every 15 seconds." That phrase makes a per-call interval claim that the harness does not enforce. VHS-4 added *total* wall-clock duration enforcement (`FIRST_POLL_TIME` + 5-min / 10-min ceilings); it did not address inter-poll cadence wording. The spec admits this directly: line 52 ("The 'every 15 seconds' inter-poll claim in 6a is still aspirational") and line 142 ("Phase 6a (lines 156–214) has a `FAST_PATH` predicate plus `FIRST_POLL_TIME`-based wall-clock bound").

The brief's Done-when #3 is binary: cadence text enforced, or cadence text revised. Phase 6a's cadence text is neither. The spec's argument that VHS-4 "addressed the brief's Phase 6a concern through a different mechanism (real wall-clock gating)" is a *defensible* trade-off, but it's a scope reduction relative to the brief's literal acceptance criterion, not full satisfaction.

This is **P2 (not P1)** because:
- The spec is explicit and audit-trail-honest about the trade-off (Decision 3 and Decision 5).
- The remaining gap (a single uncaveated "every 15 seconds" line in 6a) is cosmetic — Phase 6a will not silently misbehave; the total-duration bound is real.
- The brief itself authorizes the spec author to "verify the underlying code and adjust scope when reality has shifted" (per Decision 5 in the spec, an inference about brief flexibility).

**Suggested fix:** Either (a) bite off a tiny additional edit in scope — append a parenthetical caveat to line 185 such as "(intervals are aspirational; the harness fires Bash tool calls back-to-back — total polling duration is bounded below by `FIRST_POLL_TIME` instead)" — which closes Done-when #3 literally; or (b) revise spec § Done when item 3 to say "partially defers to VHS-4 for 6a inter-poll cadence; brief Done-when #3 is satisfied for total polling duration in 6a but not for the inter-poll wording, which is left in place because the wall-clock enforcement makes the wording's literal-truth defect non-load-bearing." Option (a) is mechanically tiny (one-line edit) and removes the only loose thread. Option (b) is paperwork and keeps the spec to the current scope.

### F-2: Decision 3's "intervals are aspirational" rewrite is internally inconsistent for Phase 6d-Phase 1 — secondary-rewrite wording omits `<N>` but Done-when #3's narrative implies all interval phrasing was reframed

**Severity:** P4 (nit, no functional impact)
**Where:** spec § Design § P2 edits (Location B, line 116→120 rewrite).

**Claim:** The new Phase 6d-Phase 1 text says "Make up to 8 polling attempts; the attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back."

**Why this is a nit:** The phrase "Make up to 8 polling attempts" is a fine rewording of "up to 2 minutes / every 15 seconds = 8 attempts." However, the spec presents both rewrites (Location B and Location C) as using the *identical* phrase ("The attempt count governs total polling, not wall-clock duration — intervals are aspirational because the agent harness fires Bash tool calls back-to-back" — § Cross-edit consistency, line 146). Location B's new wording uses "the attempt count governs total polling, not wall-clock duration" (lowercase "the"), while Location C uses "The attempt count governs total polling, not wall-clock duration" (capital "The"). The spec calls these "identical" but they differ by capitalization because Location C starts a new sentence. This is a P4 — implementer would resolve trivially.

**Suggested fix:** None required; the inconsistency is a sentence-boundary artifact. If the spec author wants pedantic consistency, rephrase the cross-edit-consistency claim to "the same clause appears verbatim in both rewrites (modulo sentence-initial capitalization)."

### F-3: Test command uses `grep -c '"coderabbitai")'` — pattern is correct, but the rationale wording in § Test plan undersells *why* the pattern is unique

**Severity:** P3
**Where:** spec § Test plan structural step 1 (line 153); spec § Test command (line 171).

**Claim:** "`grep -c '"coderabbitai")' skills/review-pr/SKILL.md` returns at least 1 — the new GraphQL filter is present (positive presence of the P0 fix; more resilient than an absolute count of the suffixed form, which could shift if an unrelated commit adds or removes a REST literal elsewhere in the skill)."

**Why this is a nit:** The pattern is technically correct — `"coderabbitai")` (with closing paren) appears only when the jq `select(... == "coderabbitai")` form is used. None of the eight REST-API `coderabbitai[bot]` occurrences match this pattern because they're all either `"coderabbitai[bot]"` (with a `]` before the `"`) or appear inside an array-comprehension `[bot]")]` (which has `]")]`, not `")`). So the test grep is well-targeted and will not false-positive on REST occurrences.

However, the spec doesn't spell this out. A future reader might wonder "why does the closing paren disambiguate?" — the answer is "REST jq filters all wrap the `coderabbitai[bot]` literal in either an array comprehension or a longer expression where `)` does not follow the closing quote." A one-sentence rationale would help.

**Suggested fix:** Add to § Test plan structural step 1: "The trailing `)` in the pattern is what makes this unique — REST occurrences of `coderabbitai[bot]` are all inside `[...]` array comprehensions or wrap in longer jq expressions, so `")` only appears immediately after the GraphQL filter literal."

### F-4: Done-when #5 (`python sync.py status` post-push) describes a manual check; the Test command does not verify it — spec is explicit about this, but the brief's Done-when #5 is the same check

**Severity:** P3
**Where:** spec § Done when item 5 (line 184); brief § Done when item 5 (line 50).

**Claim:** Spec says: "After `python sync.py push` (run by the human or by `/ship-spec`'s post-merge step, not by the Test command), `python sync.py status` shows no remaining `differ` entry for `skills/review-pr/SKILL.md`. This is a post-push manual check, deliberately outside the structural Test command — see § Test plan note."

**Why this is a finding:** The spec is correct that `sync.py status` does not exit non-zero, so chaining it inside the Test command would be cosmetic. And the spec is correct that pre-existing drift (peon-ping `dst-only` entries, etc.) would clutter the report on every Test command run. However, this means the Test command alone cannot prove Done-when #5 is satisfied — the implementer (or `/ship-spec`) must remember to run `sync.py status` post-merge and visually confirm the `differ` entry for `skills/review-pr/SKILL.md` is gone. This is a structural gap in the verification gate, but it's a brief constraint (no test infra) and the spec acknowledges it. The implementer's workflow (`/ship-spec` Phase 7-ish) handles this naturally.

**Suggested fix:** None blocking. Consider adding a § Test plan note: "Done-when #5 is verified manually post-merge by running `python sync.py status` and confirming `skills/review-pr/SKILL.md` is not in the `differ` list. The Test command intentionally omits this because `sync.py status` is a no-op-exit-code informational tool." (Spec already says this at line 159 — could be cross-referenced more explicitly in § Done when item 5.)

### F-5: Plane MCP cache miss for VHS-5 — ticket description / acceptance criteria not retrievable

**Severity:** P3
**Where:** grounding step 3.

**Claim:** Per orchestrator instructions, the reviewer should retrieve the Plane ticket via `memory_search(namespace="vhs", tags=["plane_work_item","VHS-5"], source_system="plane")` and use the ticket as canonical when it conflicts with the brief.

**Why this is a finding:** The MCP query returned 0 results in the `vhs` namespace. The ticket may not yet be cached (webhook receiver MCP-33 may not have fired for VHS-5). The brief is treated as canonical for this review. If the Plane ticket's acceptance criteria differ from the brief, that drift will not be caught by this review.

**Suggested fix:** None within this review's authority. Note for the orchestrator: if the Plane ticket is later cached and its acceptance criteria differ from the brief's, re-run the review.

## Summary

P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 1

The spec accurately describes the current state of `skills/review-pr/SKILL.md` at HEAD `19d2d98`. All cited lines (40, 156–214, 284, 295, 297, 322) match actual file content. The P0 GraphQL fix is correctly targeted at the only GraphQL filter and would not collide with the eight REST-API call sites. The P1 `--name-only` replacement is reasonable per brief Decision 2. The P2 cadence rewrite is locally consistent and the cross-edit "identical phrase" claim is essentially right (modulo a trivial sentence-initial capitalization difference, F-2). The Test command's grep patterns are well-chosen and disambiguate the GraphQL fix from REST literals.

The one substantive question is F-1: the spec's choice to leave Phase 6a's "every 15 seconds" wording untouched, on the grounds that VHS-4 made the total-duration concern moot. The spec is explicit and honest about this scope decision, but brief Done-when #3 is framed around the *text* in 6a, not the runtime behavior. The decision is defensible (the spec author has authority to scope), but should be either fixed with a one-line caveat on line 185 or explicitly carved out in spec § Done when item 3 rather than claimed as "satisfied by VHS-4." Rated P2 because the runtime behavior is correct after VHS-4; only the cadence wording is misleading.

STATUS: GREEN
