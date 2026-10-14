# Edge-Cases Review — round 3

Grounding notes: review_mode `delta`; spec, brief and `changed_regions` file read fresh. Sources read: `skills/spec-cycle/SKILL.md` (Phase 1, Two counters, Round artifacts, Disposition ledger, 2b, 2d guarantee scan, 2e), `agents/spec-reviewer-correctness.md:55-125`, and the round-2 reports. Every `file:line` citation in the changed regions resolves to the named symbol at the cited line (`SKILL.md:384/390/444/450/454/458/460/462/511/558/698/706/711-718/715`, `agents/spec-reviewer-correctness.md:86/88/90/109`, `agents/spec-reviewer-conventions.md:103`, `AGENTS.md:27/43/110`, `README.md:10`, `docs/spec-workflow-reference.md:43`), so there is no anchor drift.

Deferred-findings block: preamble present, one section, row D-1 well-formed (seven fields, blockquoted fix, three existing propagation sites, stated `out-of-scope` token). No routing violation. D-1's root (post-green polish grounding) is not re-filed.

## Closure of round 2 findings

Closure manifest is empty (round 2 closed green); round 2 carried no P0/P1.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached (P3) | PARTIAL | Shared memory still unavailable this round (`Access denied: agent 'claude' lacks 'read' on namespace 'skills'`); no spec defect. Re-recorded as F-8 below. |
| correctness | F-2 | Author-pinned enforcement choices still lack explicit provenance labels (P3) | PARTIAL | spec.md:22 now maps each Decision to brief Decisions or fences, but does not name Decisions 4, 5, 8 as author-pinned resolutions of brief Risks / decisions items 2–5. Stays P3. |
| edge-cases | F-1 | Author-pinned enforcement choices remain implicit (P3) | PARTIAL | Same evidence as above (spec.md:22). |
| conventions | F-1 | Author-pinned enforcement choices still lack explicit provenance labels (P3) | PARTIAL | Same evidence as above (spec.md:22). |

## Findings

### F-1: Delta pass 1 after a red halt has a closure manifest, so the omission boundary fires where the spec says it must not
**Severity:** P0
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (spec.md:116); spec § Test plan (spec.md:171); spec § Decision 4 — One human-readable `ground-truth-ledger.md` per dispatched round (spec.md:65)
**Edge case:** Runtime precondition false: "the first dispatch of a re-run carries no closure manifest."
**What happens:** Decision 8's Omission bullet sets the boundary to "the sections named on `fixed:` or `reworked:` lines of the `closure_manifest` in this prompt; otherwise no section", and asserts "With no boundary there is no omission finding: this is the first dispatch of a re-run". But the live skill gives delta pass 1 a manifest: `skills/spec-cycle/SKILL.md` §2b says `closure_manifest` is "the candidate ledger on delta pass 1", and `SKILL.md:460` writes `ledger.md` "after a loop-red revision, including the final pass". After a red halt that candidate ledger carries the final-pass revision's `fixed:` lines. Decision 4 (third bullet) says that dispatch's ground-truth ledger "holds only the no-claims line" and that text an earlier invocation changed "is not covered and is not backfilled". The reviewer therefore sees a non-empty boundary and a ledger with no rows, and files P1 `ground-truth ledger omits runtime claims` for every runtime claim in those sections. Test plan line 171 requires "delta pass 1 after a red halt ... must draw no omission finding". The three statements cannot all hold; every delta re-run after a red halt that folded anything into a section with runtime claims starts with a spurious P1, burning one of its two passes.
**Why the spec misses it:** The boundary rule assumes a manifest implies a same-invocation revision. The reviewer cannot tell pass 1 from pass 2 (`P` is never sent to reviewers, `SKILL.md` § Two counters). Only a green candidate (empty manifest), `--full`, and the ledger-missing full dispatch really have no manifest.
**Suggested fix:** Give the reviewer a signal it can read, mirroring the new-spec line. For example, the first dispatch of an invocation over an existing spec writes a re-run line under the title (`Re-run: nothing authored before this dispatch.`), and the Omission bullet reads "every section when the new-spec line is present; no section when the re-run line is present; otherwise the sections named on `fixed:`/`reworked:` lines". Update Decision 4's third bullet, § Round artifact and dispatch changes ("The first pass of a re-run carries the no-claims line"), and the Test plan row together. The alternative is to drop the Test plan expectation and have the author read the candidate manifest's sections before delta pass 1, but that is the backfill the brief fences out.

### F-2: An evidence-only fix carries rows for the named claims only, but its disposition puts the whole section in the omission boundary — the loop cannot close
**Severity:** P1
**Where:** spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (spec.md:94, step 6); spec § Decision 8 — Correctness alone enforces the ledger (spec.md:116-117)
**Edge case:** Partial state across rounds: a section with several runtime claims, one of which draws `ground-truth anchor does not support claim` where only the row was wrong.
**What happens:** Step 6 says no spec text changes, "hold a corrected row for each named claim", and write `fixed: ground-truth rows carried — § <a>`. Because no section was edited, step 5 and Decision 4's second bullet ("every runtime-behavior claim in each section the revision edited") add nothing, so the next round's ledger holds only the corrected row. But § a is now "named on a `fixed:` line", so it is inside the boundary and every other runtime claim in § a has no row: P1 `ground-truth ledger omits runtime claims`. The following round carries rows for those claims only, the originally corrected claim loses its row, and the omission finding returns for it. The two findings alternate until the pass cap. This is the non-convergence the ticket exists to remove, and the spec's own promise at step 5 ("an author who follows it draws no omission finding") is false on this path.
**Why the spec misses it:** Step 6 scopes the carried rows by claim; the Omission bullet scopes the boundary by section; the disposition form joins them.
**Suggested fix:** In step 6, replace "hold a corrected row for each named claim" with "hold a row for every runtime-behavior claim in each section that contains a named claim (the section-level rule of step 5), re-reading each", so the rows carried equal the sections the disposition names. Add the case to the Test plan closure row ("an unsupported-anchor finding in a section holding other runtime claims draws no omission finding next round").

### F-3: A ground-truth finding on the final allowed pass gets a `fixed:` disposition for rows that are never written
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (spec.md:94, last sentence); spec § Test plan (spec.md:172)
**Edge case:** Partial failure across the invocation boundary.
**What happens:** Step 6 says "In both cases ... write the disposition as `fixed: ground-truth rows carried — …`", then says that on the final pass no ledger is written and "the finding stands". The final-pass `ledger.md` still needs a line for that P0/P1 (the existing Ledger check files a P0 otherwise), and the only form the spec gives claims rows were carried. The held rows do not survive the invocation; Decision 4 gives the next run's first dispatch the no-claims line only. On delta pass 1 the predecessor finding cannot meet Decision 8's Closure test ("holds a supporting row for each claim that finding named"), so it is REOPENED (P0 by the closure rule) against a manifest that says `fixed`. It converges on pass 2, but pass 1 is red by construction.
**Why the spec misses it:** The Test plan lists "the same on the final allowed pass" without stating the expected disposition or the next invocation's outcome.
**Suggested fix:** State the final-pass disposition explicitly (for example `not carried: no later dispatch — rows owed for § <a>`), and say whether the next invocation's first dispatch owes those rows. If it does, that is a named exception to Decision 4's third bullet; if not, state that the predecessor finding is closed by the no-backfill rule.

### F-4: "Section" is not defined the same way for the author's rows and the reviewer's boundary
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 6 (spec.md:93, step 5); spec § Decision 8 (spec.md:116)
**Edge case:** Nested headings. The author edits `### Apply-findings changes` and dispositions it `fixed: edited § Design`.
**What happens:** Step 5 gathers rows for "each section those edits touched" (the subsection). The reviewer's boundary is "the sections named on `fixed:` lines" (the parent, which a reader may take to include every `###` under it). Sibling subsections' claims then have no row and draw a P1 omission, although the author followed step 5.
**Why the spec misses it:** Step 5 asserts the two rules are the same without fixing the granularity. The delta block already uses "exclusive body" for a heading.
**Suggested fix:** One sentence in both places: a section is a heading's exclusive body; the disposition names the innermost heading edited, and the boundary is the exclusive body of each named heading.

### F-5: Closure rule cannot be met when the fix removes or rewrites the named claim
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Closure bullet (spec.md:117)
**Edge case:** The named claim no longer exists. Step 6's first branch corrects the wrong sentence, or the revision deletes it.
**What happens:** Closure requires "a supporting row for each claim that finding named". A deleted claim has no row, and a corrected sentence is a different claim, so a literal reading leaves the finding PARTIAL or REOPENED after a correct fix. The Sample bullet's "check every row for a claim that a predecessor ground-truth finding named" has the same hole.
**Suggested fix:** Append "or the claim no longer appears in the spec; a corrected sentence is closed by a supporting row for the corrected claim".

### F-6: Held rows have no durable home between authoring and dispatch
**Severity:** P3
**Where:** spec § Phase 1 authoring changes (spec.md:129); spec § Apply-findings changes (spec.md:143)
**Edge case:** Interruption or context compaction between Phase 1 (or a 2e revision) and the next dispatch.
**What happens:** Rows are "held" in the author's context only. If the run is interrupted after Phase 1 writes the spec and before round 1 dispatches, the next invocation sees an existing spec, Phase 1 does not re-author, and Decision 4's third bullet yields a no-claims ledger with no boundary. A brand-new spec is then never covered, silently. Within one invocation, compaction can drop held rows and tempt a no-claims write.
**Suggested fix:** One sentence: if held rows are not available at dispatch, rebuild them by re-reading the sections they covered; never substitute the no-claims line. Optionally note the interrupted-before-first-dispatch case as a known gap.

### F-7: "Check at most five rows" conflicts with "also check every row a predecessor finding named"
**Severity:** P3
**Where:** spec § Decision 8 — Sample bullet (spec.md:114)
**Edge case:** Size limit. An omission finding lists every uncovered claim in one finding, possibly dozens.
**What happens:** The next round must open every one of those rows in addition to the five-row sample, so the stated cap does not hold. Two reviewers may read the sentence differently (cap wins vs. named rows win), which the "deterministic sample" rationale in § Correctness reviewer changes was meant to prevent.
**Suggested fix:** Reword to "Check the sample of at most five rows below, plus every row for a claim a predecessor ground-truth finding named."

### F-8: Ticket lookup blocked
**Severity:** P3
**Where:** grounding step 3
**Edge case:** External system down. Shared-memory search returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`.
**What happens:** The review proceeded from the brief alone, per the documented degraded path.
**Suggested fix:** None for the spec; recheck against the live ticket when the namespace is readable.

## Summary
P0: 1 | P1: 1 | P2: 3 | P3: 3 | P4: 0

STATUS: RED P0=1 P1=1 P2=3 P3=3 P4=0
