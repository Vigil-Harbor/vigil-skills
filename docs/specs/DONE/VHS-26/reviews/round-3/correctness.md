# Correctness Review — round 3

Grounding notes: spec, brief and `changed_regions` were read fresh from disk. The Plane ticket lookup was denied (`Access denied: agent 'claude' lacks 'read' on namespace 'skills'`), so the review proceeded from the brief (F-4). Every `file:line` citation inside the changed regions resolves at the cited line in the live tree (HEAD `fc20f94`, equal to `round-3/baseline.commit`): `skills/spec-cycle/SKILL.md:390`, `:444-458`, `:450`, `:454`, `:460`, `:462`, `:558`, `:698`, `:711-718`, `:715`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`; `AGENTS.md:110`. No moved or dead anchors. `git log` shows the touched files changed in the last 7 days (`fad52c7` and `f64bebe` on 2026-10-13, `d3730b1` on 2026-10-12); the spec's anchors already reflect that code.

Deferred-findings block: preamble present with the required sentence, one section, row D-1 well-formed (seven fields, three existing propagation sites, `Scope` token `out-of-scope`), so the ceiling does not apply. No routing violation.

## Closure of round 2 findings

No `closure_manifest` lines were supplied (round 2 closed green with no P0/P1), so the Ledger check has nothing to require. The round-2 P3 findings are tracked for completeness.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | PARTIAL | Shared memory still denies the `skills` namespace; re-filed as F-4 (P3). No spec defect. |
| correctness | F-2 | Author-pinned enforcement choices still lack explicit provenance labels | PARTIAL | New `## Decisions` preamble (spec.md:22) maps each Decision to brief Decisions or fences, but does not label Decisions 4, 5, 8 as resolutions of brief Risks items 2–3. Re-filed as F-3 (P3). |
| edge-cases | F-1 | Author-pinned enforcement choices remain implicit | PARTIAL | Same root as correctness F-2; see F-3. |
| conventions | F-1 | Author-pinned enforcement choices still lack explicit provenance labels | PARTIAL | Same root as correctness F-2; see F-3. |

## Findings

### F-1: Delta pass 1 after a red halt carries a closure manifest, so the omission boundary is not empty on a re-run
**Severity:** P0
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Omission bullet, spec.md:116); spec § Decision 4 (third bullet, spec.md:65); spec § Test plan (spec.md:171)
**Claim:** Decision 8: "The boundary is: every section when the new-spec line is present; otherwise the sections named on `fixed:` or `reworked:` lines of the `closure_manifest` in this prompt; otherwise no section. ... With no boundary there is no omission finding: this is the first dispatch of a re-run, and nothing is backfilled." Test plan: "delta pass 1 after a red halt; a `--full` re-run; a pass dispatched full because `ledger.md` was missing. The last three must draw no omission finding."
**Why this is wrong:** The spec assumes the first dispatch of a re-run has no `closure_manifest`. That holds for a `--full` re-run and for the missing-`ledger.md` case, but not for delta pass 1.
- `skills/spec-cycle/SKILL.md:566`: "Include `closure_manifest` only when this pass has a closure predecessor. It is the exact bytes read from that predecessor's `ledger.md`: the candidate ledger on delta pass 1, or the preceding pass ledger thereafter."
- `skills/spec-cycle/SKILL.md:460`: `ledger.md` is written "after a loop-red revision, including the final pass". A red halt's candidate ledger therefore carries `fixed:` / `reworked:` lines naming the sections the final revision edited.
- Decision 4 says that same dispatch's ground-truth ledger "holds only the no-claims line", and Decision 5 says the final-pass revision writes no ground-truth ledger.

Following Decision 8 literally, the reviewer on delta pass 1 after a red halt has a non-empty boundary and a ledger with no rows. It files P1 `ground-truth ledger omits runtime claims` for every runtime claim in the sections the prior invocation's final revision touched. Those sections are also in `changed_regions` or `open_findings`, so the reviewer does read them. That contradicts the Test plan, Decision 4's "is not covered and is not backfilled", and the brief's no-backfill fence (brief.md:70). Every delta re-run after a red halt would start with a spurious blocking P1.
**Suggested fix:** Make the "no boundary" case depend on something the ground-truth ledger itself states, not on the absence of a manifest. For example, Decision 4's third bullet writes a distinct line under the title (parallel to the new-spec line, e.g. `Re-run: nothing authored before this dispatch.`), and the Omission bullet reads "no section when the re-run line is present; every section when the new-spec line is present; otherwise the sections named on `fixed:`/`reworked:` lines". Propagate to § Phase 1 authoring changes, § Round artifact and dispatch changes ("The first pass of a re-run carries ..."), § Correctness reviewer changes ("The omission boundary uses only ...") and the Test plan omission row.

### F-2: An evidence-only ground-truth fix puts a section in the omission boundary with rows for only the named claims
**Severity:** P1
**Where:** spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (step 6, spec.md:94); spec § Decision 8 (Omission bullet, spec.md:116)
**Claim:** Step 6: "When only the evidence was wrong or absent, no spec text changes ... hold a corrected row for each named claim for the next dispatched round's ground-truth ledger, and write the disposition as `fixed: ground-truth rows carried — § <a>; § <b>`, naming each section whose claims the carried rows cover". Step 5: "an author who follows it draws no omission finding."
**Why this is wrong:** The disposition is a `fixed:` line that names § a, so Decision 8's Omission boundary for the next round includes § a. Step 6 carries rows only for the claims the finding named. Step 5's every-claim-in-the-section rule applies only to "each section those edits touched", and in the evidence-only case no section is edited. Any other runtime-behavior claim in § a then has no row in round C+1's ground-truth ledger. The reviewer reads § a (it is an `open_findings` heading on a delta pass, and whole-spec on a full pass) and must file P1 `ground-truth ledger omits runtime claims`. Fixing one unsupported anchor or one omitted claim produces a new blocking finding in the same section in the next round, and carrying those rows can repeat the pattern. This is the divergence the ticket exists to remove, and it contradicts step 5's guarantee. The Test plan closure row "an unsupported-anchor finding where only the row was wrong" would fail the mental exercise.
**Suggested fix:** In step 6, carry a row for every runtime-behavior claim in each section named on the disposition (the same section-level rule as step 5), not only the named claims. Alternatively, keep per-claim carrying and state in the Omission bullet that sections named only after `ground-truth rows carried —` are not in the boundary. Update § Apply-findings changes and the Test plan closure row to match whichever is chosen.

### F-3: Decisions preamble maps to brief decisions but still does not mark the author-pinned choices
**Severity:** P3
**Where:** spec § Decisions (spec.md:22)
**Claim:** "Decision 4 carries brief Decisions 2 and 3; Decision 5 carries the brief's Out-of-scope fences on dispatch and control flow; ... Decision 8 carries brief Decision 7".
**Why this is wrong:** Not wrong, but incomplete against the three round-2 P3s. The file name, warn-and-dispatch failure behavior, five-row sample and P0/P1/P3 severities are author-pinned resolutions of brief Risks / decisions items 2 and 3 (brief.md:87-88). The preamble presents them as carried from the brief.
**Suggested fix:** Add one clause: "Decisions 4, 5 and 8 also pin the choices the brief left to the spec author in Risks / decisions items 2 and 3 (file name and artifact-set status; sample size and severities)."

### F-4: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec is authored from the VHS-26 brief and ticket.
**Why this is wrong:** `memory_search` on namespace `skills` returned an access-denied error, so the Plane ticket could not be read. The brief states the ticket has no acceptance criteria (brief.md:45), so the brief's Done-when list was used as canonical.
**Suggested fix:** None to the spec. Re-check against the live ticket if access is restored.

### F-5: Done-when item 6 and § Test command quote the unittest pattern differently
**Severity:** P4
**Where:** spec § Test command (spec.md:184); spec § Done when item 6 (spec.md:196)
**Claim:** Test command uses `-p "test_*.py"`; Done when uses `-p 'test_*.py'`.
**Why this is wrong:** Same command, two quotings, after this round changed only one of them. `AGENTS.md:7` uses single quotes.
**Suggested fix:** Use one form in both places.

## Summary
P0: 1 | P1: 1 | P2: 0 | P3: 2 | P4: 1

STATUS: RED P0=1 P1=1 P2=0 P3=2 P4=1
