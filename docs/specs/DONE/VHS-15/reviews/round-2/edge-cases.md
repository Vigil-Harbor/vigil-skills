# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P0) | Round-4 manifest hardcodes three filenames | CLOSED | Scope step-2e; §3 step 2e generalizes `SKILL.md:357–368`; §5 item 2; Done-when 2; checklist 8. |
| edge-cases | F-2 (P1) | Lens toggle / stale `scalability.md` | CLOSED | §5 stale-report guard; Phase 0 re-run pin; `scale_lens` to every reviewer; Failure mode 3; checklist 7. |
| edge-cases | F-3 (P1) | Malformed/missing STATUS | CLOSED | §4 ¶2 → `SKILL.md:482`; Failure mode 2; checklist 9. |
| edge-cases | F-4 (P1) | Partial dispatch | CLOSED | §3 step 2c stub `RED P0=1 P1=0`; §4; Failure mode 2; checklist 9. |
| edge-cases | F-5 (P2) | Free-text rendering | CLOSED | §2 opaque-single-line-text note. |
| edge-cases | F-6 (P2) | Heading regex / multiple sections | CLOSED | §2 rule 1 whole-word + first-authoritative. See NEW F-1. |
| edge-cases | F-7 (P2) | Empty-target backstop | CLOSED | §1 grounding defense-in-depth note. |
| edge-cases | F-8 (P2) | byte-for-byte overclaim | CLOSED | Goal/Decision 8/item 6 reworded. |
| edge-cases | F-9 (P3) | Non-factor teeth | CLOSED | Decision 3 softened. |
| correctness | F-1..F-3 | (P1/P2/P3) | CLOSED | §6 rows; grep; Phase 3 no-reparse. |
| conventions | F-1..F-4 | (P2/P3/P4) | CLOSED / DEFERRED | §6 rows; Decision 9/8; Deferred. |

All 15 round-1 findings closed. No REOPENED/PARTIAL.

## Findings

### F-1: Near-miss `## Scale …` headings silently dropped to off (whole-word fix traded one silent failure for another)
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design §2 rule 1; Failure mode "Malformed or target-less scale declaration"
**Edge case:** Author writes `## Scale declaration` / `## Scale (target N)` / `## Scaling and throughput` with a valid `**Factor:** yes` + `**Target:**` body.
**What happens:** The whole-word regex `^#{1,6}\s+scal(e|ing)\s*$` doesn't match → `scale_lens = off` silently; the preflight token is the indistinguishable `scale-lens: off`. A complete valid declaration is dropped with zero signal — the "decided too late" failure re-introduced one layer down. Rule 1's no-match path is the only detection outcome that is silent (rules 2/3 warn).
**Suggested fix:** Near-miss tripwire: if no whole-word heading matched but a looser `^#{1,6}\s+scal(e|ing)\b` heading exists whose body contains `**Factor:**`, warn `scale-lens: off (heading "<text>" not recognized — use a bare "## Scale"/"## Scaling" heading to enable)` instead of staying silent.

### F-2: Re-run pin gives no in-tool path to deliberately turn the lens OFF after a prior on-run
**Severity:** P2
**Where:** spec § Design §3 Phase 0 step 8 re-run pin; §5; Failure mode 3
**Edge case:** Round 1 scale-on (Decision recorded). Author deliberately narrows brief to `Factor: no` and re-runs. The pin keeps the recorded (on) decision and warns "edit the spec to change" — but Phase 1 regenerates the spec from the brief each cycle, so the interaction across the Phase 0 → Phase 1 boundary is unsequenced.
**What happens:** Graceful (anti-flip-flop, warns), but the escape hatch is underspecified: which artifact wins on a deliberate off-transition isn't stated.
**Suggested fix:** Add to the pin: "To intentionally turn the lens off, edit/remove the recorded scale Decision in `<TICKET-ID>.spec.md` (or delete the spec to force clean Phase-1 re-author); step 8 reads the spec's Decision as it exists at preflight — recorded Decision present → pin; absent → brief governs."

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 0 | P4: 0

STATUS: GREEN
