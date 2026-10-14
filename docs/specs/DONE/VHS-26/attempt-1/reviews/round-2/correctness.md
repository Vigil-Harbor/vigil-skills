# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Placeholder scan rejects canonical spec paths | CLOSED | Spec lines 104 and 251 exempt slash/backslash-containing path tokens and test canonical `docs/specs/TODO/` paths. |
| correctness | F-2 | Coverage grammar has no valid empty-set representation | CLOSED | Spec lines 61–65 and 113 define `coverage: no spec sections` and its exact no-claims form. |
| correctness | F-3 | Line-sensitive diagnostic keys defeat the one-attempt bound | CLOSED | Spec lines 122–128 replace display-line identity with stable `(code, normalized path, owner)` keys; lines 255 and 278 require regression coverage. |
| correctness | F-4 | Full-pass reviewers cannot verify declared coverage completeness | CLOSED | Spec lines 63 and 153–162 independently derive and pass `expected_ground_truth_coverage`; lines 212 and 218 integrate it into dispatch. |
| correctness | F-5 | Ticket not cached | CLOSED | Round 1 correctly followed the degraded path. The service remains unavailable for this pass and is reported anew as F-3. |
| correctness | F-6 | Touched review surfaces changed within the last seven days | CLOSED | Current files and anchors were re-read at HEAD `fc20f94`; the continuing freshness condition is reported anew as F-4. |
| edge-cases | F-1 | Post-green polish bypasses the immutable ledger | NEW | Spec lines 236, 256, and 268 close the post-green case, but terminal red revisions expose a new variant described in F-1 below. |
| edge-cases | F-2 | First-run ledger preparation has no parent directory | CLOSED | Spec lines 73 and 212 create the ticket reviews root before preparing the temporary ledger. |
| edge-cases | F-3 | Placeholder scanning rejects canonical `TODO` paths | CLOSED | Spec lines 104 and 251 exempt path-like tokens while retaining standalone placeholder checks. |
| edge-cases | F-4 | Python probing and checker execution can hang indefinitely | CLOSED | Spec line 130 bounds probes at 10 seconds and checker execution at 30 seconds; lines 255 and 278 require coverage. |
| edge-cases | F-5 | Persisted ledger and diagnostics have no size bound | CLOSED | Spec lines 75, 94–96, and 255 bound stale temps, input size, claim rows, field size, and diagnostic output. |
| edge-cases | F-6 | Ticket lookup was unavailable | CLOSED | Round 1 correctly degraded to the brief. The current independent lookup failure is reported as F-3. |
| conventions | F-1 | Placeholder scan rejects the canonical `TODO` artifact path | CLOSED | Spec lines 104 and 251 preserve the repository’s canonical artifact paths. |
| conventions | F-2 | Checker no longer verifies every brief acceptance criterion | CLOSED | Spec lines 84–89 add the brief to the CLI; line 103 requires count-equal ordinal pairing and a Verify line for every item. |
| conventions | F-3 | Divergence still performs the patch pass the brief says to stop | CLOSED | Spec lines 174–188 and 234 halt before 2e when the positive blocking total does not decrease. |
| conventions | F-4 | Test command is machine-specific in a cross-machine repository | CLOSED | Spec lines 261–264 use portable `python -X utf8` module commands. |

## Findings

### F-1: Terminal red revisions bypass the immutable ground-truth ledger
**Severity:** P0  
**Where:** spec.md:146, spec.md:232, spec.md:268  
**Claim:** “Every newly authored or revision-touched runtime-behavior claim is represented in that dispatched round’s immutable `ground-truth.md`,” and the grounding rules apply to “final FROZEN/REWRITE, guarantee-scan discharges, and applicable grill edits.”  
**Why this is wrong:** The proposed ledger is finalized before reviewer dispatch and is immutable afterward (spec.md:42, 73, 210–218). Revisions occur after reports return, and the spec says only the *next* ledger covers those edits (spec.md:232). On the final allowed red pass, however, the live workflow performs final 2e edits, writes `ledger.md`, and halts without another dispatch (`skills/spec-cycle/SKILL.md:763-801`). Grill edits likewise run after the halt and explicitly do not redispatch (`skills/spec-cycle/SKILL.md:932-937`). A runtime claim introduced by either terminal path therefore has no dispatched `ground-truth.md`, contradicting Done-when item 1 and the brief’s requirement that the gate cover every patch pass (`VHS-26.brief.md:58`).  
**Suggested fix:** Define a persistent grounding artifact for terminal red and grill revisions, or prohibit runtime-behavior edits on every path with no subsequent dispatch. Reconcile Decisions 3 and 9, Revision and synthesis integration, the terminal halt/grill flows, tests, and Done-when item 1 around that choice.

### F-2: The no-Python flow skips the ledger it promises to preserve
**Severity:** P0  
**Where:** spec.md:220  
**Claim:** “The no-Python path skips step 2,” where Pre-dispatch step 2 is “Prepare the temporary ground-truth ledger for `C`.”  
**Why this is wrong:** Decision 4 says the same temporary ledger is finalized into `round-<C>/ground-truth.md` even when the checker is skipped (spec.md:73), and Decision 7 explicitly says the author ledger is still written and sent to correctness when Python is unavailable (spec.md:130). Skipping preparation leaves step 6 with no ledger bytes to finalize and makes correctness’s required `ground_truth_ledger_path` nonexistent.  
**Suggested fix:** Change the no-Python rule to skip Pre-dispatch step 3, the checker execution, while still performing ledger preparation and finalization. Add an orchestrator-contract test proving an unavailable interpreter still produces and dispatches `ground-truth.md`.

### F-3: Ticket not cached
**Severity:** P3  
**Where:** brief.md:90  
**Claim:** The brief records Plane VHS-26 as its canonical ticket source.  
**Why this is wrong:** The memory/ticket service is unavailable for this review, so the ticket description and acceptance criteria could not be independently checked. Review proceeded using the brief under the required degraded path.  
**Suggested fix:** Re-run ticket grounding when the service is available and confirm that no canonical ticket criteria conflict with the brief.

### F-4: Touched review machinery changed within the freshness window
**Severity:** P3  
**Where:** spec § Scope  
**Claim:** The spec plans changes across `/spec-cycle`, both reviewer definitions, workflow documentation, README, and AGENTS.md.  
**Why this is wrong:** Read-only history shows recent commits on these surfaces: `fad52c7` and `f64bebe` on 2026-10-13, plus `d3730b1` on 2026-10-12. Current anchors resolve at HEAD `fc20f94`, so this is a freshness warning rather than a demonstrated design defect.  
**Suggested fix:** Re-run the cited-anchor and integration checks immediately before implementation, especially around artifact ordering, dispatch inputs, terminal revision paths, and divergence handling.

## Summary

P0: 2 | P1: 0 | P2: 0 | P3: 2 | P4: 0

STATUS: RED P0=2 P1=0 P2=0 P3=2 P4=0
