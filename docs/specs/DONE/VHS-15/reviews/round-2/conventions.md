# Conventions Review — round 2

## Closure of round 1 findings

All 15 round-1 findings CLOSED (1 P0, 4 P1, 5 P2, 4 P3, 1 P4) or appropriately DEFERRED. Verified each disposition against the spec on disk:
- correctness/F-1,F-2,F-3 — §6 `:54`/`:153` rows, broadened grep, Phase 3 no-reparse.
- edge-cases/F-1 (P0) — §3 step 2e + §5 item 2 generalize `SKILL.md:357–368`.
- edge-cases/F-2,F-3,F-4 (P1) — stale-guard + pin; `SKILL.md:482` route; step 2c stub.
- edge-cases/F-5..F-9, conventions/F-1 (P2/P3) — folded.
- conventions/F-2,F-3 (P3) — Decision 9 / Decision 8 + Deferred.
- conventions/F-4 (P4) — Deferred section. No REOPENED items.

## Findings

### F-1: AGENTS.md:66 frontmatter prose stale — small SSOT opportunity (spec already edits this file)
**Severity:** P4
**Where:** spec § Deferred (P2+); §6 row "AGENTS.md Conventions"
**Evidence:** `AGENTS.md:66` says agents use `name, description, user_invocable`; the three existing agents and the new one carry only `name`+`description`. The spec already edits AGENTS.md (lines 68, 202).
**Suggested fix:** Optional one-clause fix at line 66 while editing AGENTS.md. Not required for green.

### F-2: `scale_lens` two-valued at dispatch (`on|off`) vs three-valued at resolution (`on|non-factor|off`) — state the collapse
**Severity:** P3
**Where:** spec § Design §3 step 2b vs. §2
**Evidence:** §2 resolves `scale_lens ∈ {on, non-factor, off}`; §3 step 2b passes `scale_lens: <on|off>`. The non-factor→off collapse at the dispatch boundary is implied, never stated.
**Suggested fix:** Add a clause: "the reviewer-facing `scale_lens` is the dispatch-time collapse to `on|off` (both `non-factor` and `off` map to `off`)."

### F-3: Decision-classification re-audit — one new (c) item, correctly flagged
**Severity:** P3
**Where:** spec § Decisions; §1 grounding
**Evidence:** The §1 grounding empty-target backstop is a new (c) spec-addition-with-rationale (unreachable in normal operation, fail-safe). Other round-1→2 additions (`scale_lens` param, re-run pin, Failure modes) are (a) authorized by Done-when 2/3. No (d) silent additions.
**Suggested fix:** None.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 1

STATUS: GREEN
