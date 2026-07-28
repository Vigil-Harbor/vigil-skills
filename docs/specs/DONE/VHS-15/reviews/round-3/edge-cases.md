# Edge-Cases Review — round 3

## Closure of round 2 findings

All round-2 findings CLOSED (correctness/F-1 P1 + the folded P2/P3/P4). Verified: §6 rewordings dodge the item-12 grep; `:357–371` anchor; preflight wording; §2 near-miss tripwire; deliberate-off escape; AGENTS.md:66 SSOT; scale_lens collapse; decision-classification in Deferred. No REOPENED items.

## Findings

### F-1: Near-miss tripwire is disabled whenever any whole-word `## Scale` heading exists
**Severity:** P3
**Where:** spec § Design §2 rule 1
**Edge case:** A brief carries both a whole-word `## Scale` (`Factor: no`) and a separate near-miss `## Scaling considerations` with a real `Factor: yes` + `Target:` body.
**What happens:** The whole-word match wins (non-factor); the tripwire's guard ("if no whole-word heading matched but…") structurally cannot fire, so the factor-bearing near-miss section is dropped with no warning. Graceful (off-by-default), so P3.
**Suggested fix:** When a whole-word heading is authoritative AND a distinct near-miss `scal(e|ing)\b` heading carries a `**Factor:**` body, append a `note — ignored near-miss heading "<text>"` warning alongside the chosen token.

### F-2: §2 "Preflight-summary token" enumeration (line 136) is missing two of the seven reachable tokens listed at §3 step 8 (line 140)
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design §2 (line 136) vs. §3 Phase 0 step 8 (line 140)
**Edge case:** An implementer reading §2 (the grammar's canonical output list) rather than §3.
**What happens:** Line 136 lists 5 tokens; it omits `off (heading not recognized)` and `multiple Scale sections — using first` (both defined at line 126, both listed at line 140). The two enumerations disagree. Warning strings are defined at 126, so writable from §3 — a stale duplicate enumeration, not a missing definition.
**Suggested fix:** Extend line 136 to the full seven, matching §3 step 8 verbatim.

### F-3: Deliberate-off escape leaves a stably-noisy "brief disagrees" warning on a half-applied edit
**Severity:** P3
**Where:** spec § Design §3 Phase 0 step 8 (re-run pin + Phase 1 re-record)
**Edge case:** Author edits the recorded Decision to non-factor but leaves the brief's `Factor: yes`.
**What happens:** Converges (lens stably off) but the `brief disagrees` warning fires every re-run, and its remedy ("edit the spec's scale Decision") is already done — the real lever is the brief. Safe, P3.
**Suggested fix:** Name the brief in the warning: "…align the brief's `## Scale` with the recorded Decision (or remove the Decision) to clear."

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 0

STATUS: GREEN
