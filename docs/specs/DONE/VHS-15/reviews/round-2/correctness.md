# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | §6 table omits `spec-workflow-reference.md:54` and `:153` | CLOSED | §6 rows for `:54` and `:153` added; Scope line 26 lists both; checklist grep broadened to include `prior-round`. |
| correctness | F-2 (P2) | Checklist grep too narrow | CLOSED (introduces NEW F-1) | Grep broadened; over-broadening creates the new contradiction below. |
| correctness | F-3 (P3) | Phase 3 brief-parsing double-source | CLOSED | §3 Phase 3 now "no re-parse … single source of truth (step 8)". |
| edge-cases | F-1 (P0) | Round-4 manifest hardcodes three filenames | CLOSED | Scope step-2e bullet; §3 step 2e; §5 item 2; Done-when 2; checklist 8. |
| edge-cases | F-2 (P1) | Lens toggled on/off; stale `scalability.md` | CLOSED | §5 stale-report guard; Phase 0 re-run pin; `scale_lens` to every reviewer; Failure mode 3; checklist 7. |
| edge-cases | F-3 (P1) | Malformed/missing STATUS unspecified | CLOSED | §4 ¶2 (existing `SKILL.md:482` rule); Failure mode 2; checklist 9. |
| edge-cases | F-4 (P1) | Partial dispatch — scalability agent dies | CLOSED | §3 step 2c stub; §4; Failure mode 2; checklist 9. |
| edge-cases | F-5..F-9 | (P2/P3) | CLOSED | Folded in §2/§1/Goal/Decision 3. |
| conventions | F-1 (P2) | Residual `:153`/`:54` | CLOSED | §6 rows added. |
| conventions | F-2,F-3 (P3) | Informational | CLOSED | Decision 9 / Decision 8 / Deferred. |
| conventions | F-4 (P4) | `AGENTS.md:66` stale | DEFERRED | Recorded in `## Deferred (P2+)`. |

All five round-1 P0/P1 dispositions verify as genuinely fixed. No REOPENED items.

## Findings

### F-1: Broadened checklist grep (item 12) flags the spec's own reconciled `:9`/`:3`/`:17`/`:25` targets — gate contradicts §6
**Severity:** P1
**Where:** spec § Test plan item 12 vs. § Design §6 rows `:9`, `:3`, `:17`, `:25`
**Claim:** Item 12 asserts the grep `grep -rinE "3-lens|three (reviewer|lens|independent|read-only|agent|prior-round)|other two lenses"` "returns **only reconciled phrasings**."
**Why this is wrong:** The reconciled `:9` ("three independent AI agents (plus …)") matches `three (independent)`; reconciled `:3`/`:17`/`:25` ("three lenses …") match `three (lens)`. So a faithful §6 implementation leaves these as grep hits. Read as a zero-match gate, item 12 fails on reconciled text; the two sections can't both be satisfied as written.
**Suggested fix:** Either reconcile `:9`/`:3`/`:17`/`:25` to forms where "three" isn't adjacent to a matched noun (e.g. "three default lenses", "independent AI agents (three by default, …)"), or reframe item 12 as a locator whose pass condition is "every hit is an accepted reconciled construction; no bare/unqualified count remains," enumerating the count-phrasings expected to survive.

### F-2: `SKILL.md:357–368` round-4-manifest anchor stops short of the block (actual 357–371)
**Severity:** P3
**Where:** Scope line 19, §3 step 2e, §5 item 2, checklist 8
**Why this is wrong:** The generalized phrase is at 358–359 (inside range), but the block extends to ~371; the upper bound clips the artifact.
**Suggested fix:** Cite `SKILL.md:357–371`. Cosmetic.

### F-3: Phase 0 step-8 preflight-summary anchor says the sentence "ends" where it does not
**Severity:** P3
**Where:** §3 Phase 0 step 8
**Why this is wrong:** `SKILL.md:237` continues past "…origin check result token (…)" with a parenthetical and "— then continue." The paraphrase still locates the insertion point but "ending" is inaccurate.
**Suggested fix:** Reword to "the preflight-summary sentence (`SKILL.md:237`) gains a scale-lens token after the origin token, before '— then continue.'"

## Summary
P0: 0 | P1: 1 | P2: 0 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=1 P2=0 P3=2 P4=0
