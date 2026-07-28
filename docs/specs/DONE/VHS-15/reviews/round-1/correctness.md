# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: §6 docs-reconciliation table omits `spec-workflow-reference.md:54` and `:153` — the closure-tracking invariant the spec's own §5 flags as stale
**Severity:** P1
**Where:** spec § Design §5 vs. § Design §6 table; Done-when 6
**Claim:** §5 states the invariant "each reviewer reads all three prior-round reports" becomes stale with a fourth lens. Yet the §6 reconciliation table targets only `docs/spec-workflow-reference.md:9, :39, :49, :150, :152` — it does not list line 153 (`Round 2+ closure tracking. Each reviewer reads all three prior-round reports…`) or line 54 (same prose in the Phase 2 body).
**Why this is wrong:** Verified both lines on disk. After implementation, `spec-workflow-reference.md` still asserts "reads all three prior-round reports" while the agents now read four. Defeats Done-when 6 and contradicts §5's own rationale. The spec's checklist item 9 grep (`3-lens\|three reviewer\|three lenses\|other two lenses`) will NOT catch these residuals — the offending substring is "all three prior-round reports," matching none of those four alternatives.
**Suggested fix:** Add two rows to the §6 table: `:54` and `:153`, reconciling "reads all three prior-round reports" → "reads every prior-round reviewer report present in `round-<N-1>/` (the three default lenses, plus `scalability.md` when the scaling lens ran)." Extend checklist item 9's grep to include `all three prior-round`.

### F-2: Checklist item 9's consistency grep does not cover all the phrasings §6 reconciles
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan, item 9
**Claim:** Item 9's grep `3-lens\|three reviewer\|three lenses\|other two lenses`.
**Why this is wrong:** Several reconciled phrasings are not matched: `AGENTS.md:33` "three read-only subagents", `spec-workflow-reference.md:9` "three independent AI agents", `:39` "three reviewer agents / three agent calls", `:54`/`:153` "all three prior-round reports". The grep would pass while leaving reconciled phrasings unverified — false assurance in a spec whose Test plan relies on inspection.
**Suggested fix:** Broaden to count-agnostic alternation, e.g. `grep -rinE "3-lens|three (reviewer|lens|independent|read-only|agent|prior-round)|other two lenses"`.

### F-3: §3 Phase 3 "brief-section parsing rules gain `Scale` as a recognized header" risks a double-source-of-truth
**Severity:** P3
**Where:** spec § Design §3 Phase 3 vs. §2/§3 Phase 0 step 8
**Claim:** §3 Phase 3: "The brief-section parsing rules gain `Scale` as a recognized header." But the Scale block is driven from `scale_target`/`scale_lens`, already parsed once in Phase 0 step 8.
**Why this is wrong (minor):** SKILL.md's "Brief-section parsing rules" enumerate numbered-list items for the drift-check. The Scale block is a single carried-forward value, not an enumeration. Telling the implementer to also register `Scale` invites a second parse path that could diverge from step 8's regex.
**Suggested fix:** Reword to: "Phase 3 consumes the `scale_lens`/`scale_target` already resolved in Phase 0 step 8 — no re-parse."

## Summary
P0: 0 | P1: 1 | P2: 1 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=1 P3=1 P4=0
