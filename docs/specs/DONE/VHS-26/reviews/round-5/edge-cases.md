# Edge-Cases Review — round 5

Grounding notes: `review_mode: delta`. Spec, brief, the `changed_regions` file, and the three round-4 reviewer reports were read fresh from disk (`synthesis.md` not read; nothing under `VHS-26.attempt-1/` read). The project `CLAUDE.md` was read as supplied in context. The Plane ticket lookup was denied (`Access denied: agent 'claude' lacks 'read' on namespace 'skills'`), so the review proceeded from the brief (F-4).

Anchors: every `file:line` citation in the changed regions resolves to the named symbol at HEAD `fc20f94` (equal to `round-4/baseline.commit`): `skills/spec-cycle/SKILL.md:390`, `:450`, `:454`, `:460`, `:462`, `:558`, `:578-579`, `:594-601`, `:698`, `:711-718`, `:715`, `:757`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`. No dead or moved citations.

Deferred-findings block: one `## Deferred — follow-up required` heading, preamble present with the required sentence. Row D-1 is well-formed (seven fields, blockquoted fix, one blank line before `Propagation sites`, three sites that all exist). Its `Scope` token is `out-of-scope`, so the ceiling does not apply. No routing violation; D-1's root is not re-filed.

Deleted headings: `## Deferred (P2+)` and `## Post-green polish` were read in `round-4/spec.copy.md`. All four `Deferred (P2+)` entries are folded in this revision (see the closure table), so removing them drops nothing live. The one polish entry recorded a rewording of a sentence in § Correctness reviewer changes that this revision rewrote again. With the section gone, a later green round runs 2g fresh instead of in reconcile mode (`skills/spec-cycle/SKILL.md:945-947`); its "skip any already addressed" test covers the round-4 tagged P2s, so no finding.

## Closure of round 4 findings

The manifest is empty (round 4 closed green, no P0/P1). The round-4 P2/P3 findings are listed for completeness.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P2) | Omission boundary narrows brief Decision 7 | CLOSED | new-spec line restored (§ Decision 4, spec.md:75; § Decision 8 Omission, spec.md:140); narrowing recorded in § Decisions (spec.md:34) |
| correctness | F-2 (P2) | Missing-file closure pinned for correctness only | CLOSED | path added to the phrase (§ Decision 6 step 6, spec.md:110); § Correctness reviewer changes reworded (spec.md:179) |
| correctness | F-3 (P2) | Grading order ambiguous for a row-only dead anchor | CLOSED | ordered rules 1 and 4 (spec.md:134, :137); Test plan case added (spec.md:199). A new variant of the ordering problem is F-1 below |
| correctness | F-4 (P3) | Ticket not cached | N/A | process finding; recurs as F-4 below |
| correctness | F-5 (P3) | Phase 1 rows dropped after failed first write; preamble count | CLOSED | "this includes Phase 1's rows and the new-spec line" (spec.md:110); preamble list (spec.md:26-32); Test plan (spec.md:201) |
| edge-cases | F-1 (P2) | Omission P2 tagged `Pre-ship recommended` | CLOSED | "Do not tag it" (spec.md:140); green-round sentence (spec.md:112); Test plan "untagged" (spec.md:200) |
| edge-cases | F-2 (P2) | Other lenses cannot close `ground-truth ledger missing` | CLOSED | path in the manifest phrase (spec.md:110); spec.md:179 |
| edge-cases | F-3 (P3) | "Opens code anchors, not spec sections" | CLOSED | sentence replaced (spec.md:128); residual in F-3 below |
| edge-cases | F-4 (P3) | Three row and closure states ungraded | CLOSED | rule 1 (spec.md:134); Closure "count the defect once" (spec.md:141); Test plan (spec.md:199, :201) |
| edge-cases | F-5 (P3) | No-claims line on a new spec passes every check | CLOSED | stated limit extended (spec.md:143) |
| edge-cases | F-6 (P3) | Ticket lookup blocked | N/A | process finding; recurs as F-4 below |
| conventions | F-1 (P2) | Omission tag misuses `Pre-ship recommended` | CLOSED | same as edge-cases F-1 |
| conventions | F-2 (P2) | Missing-file disposition has no verifiable anchor | CLOSED | same as edge-cases F-2 |
| conventions | F-3 (P2) | Preamble mislabels Decision 8 as carrying brief Decision 7 | CLOSED | spec.md:34 |
| conventions | F-4 (P3) | Spec-level additions not listed | CLOSED | spec.md:26-32 |

## Findings

### F-1: "Apply the first rule that matches" misgrades three row states
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Grading a checked row, spec.md:133-139); spec § Test plan (spec.md:199)
**Edge case:** Malformed and boundary inputs to the new ordered grading list.
**What happens:** The list is now strict first-match, and the order sends three states to the wrong rule:
- **`Anchor: none` rows.** Decision 3 says a claim about unreadable source has no anchor, so its spec sentence carries none. Rule 1's second condition is "the sentence carries no anchor: file a P2", and it comes before rule 2.
  - Every legitimate `Anchor: none` row draws a P2 that has no possible fix.
  - An illegitimate one (behavior that lives in a readable file) is caught by rule 1 as a P2, so rule 2's P1 is never reached.
- **A line that only moved.** The cited line no longer shows the supporting code, so rule 3 ("the anchor does not support the claim": P1) matches before rule 4, which is the rule that sends a moved line to the combined P4. The result is a blocking P1 and a red round for a stale line number.
- **An out-of-root anchor this host cannot read.** The combined P3 sits after the list, outside the first-match order. A reviewer on another host cannot open the file, and rule 3 can be read as matching: a P1 against a correct sibling-repo anchor.

None of these crashes or corrupts anything, and the agent's step 5 still verifies the claims, so this is P2. The first case does silently turn one of the two blocking checks into an advisory one.
**Why the spec misses it:** The round-4 fix for correctness F-3 put the row-only rule first so that "a defect in the row alone never blocks", but "the sentence carries no anchor" is not a row-only defect and overlaps rule 2. Rules 3 and 4 were not reordered when the list became first-match. The Test plan names "a line that moved" and the `Anchor: none` case but gives no expected grade for either.
**Suggested fix:** Reorder and qualify the rules:
1. An `Anchor: none` row is not opened: P1 only when the normal read finds the behavior in a readable file, otherwise no finding.
2. An out-of-root anchor this host cannot read: the combined P3.
3. The row's sentence is not in the spec, or a sentence whose row gives an anchor carries none, or only the row differs: P2.
4. The file or symbol of the sentence's anchor is gone, or only the line moved: Anchor drift.
5. The file and symbol are live and the code does not support the claim: P1.

State the expected grade for the moved-line and both `Anchor: none` cases in the Test plan row. The fix edits Decision 8, so 2g cannot apply it; it needs a revision or an operator edit.

### F-2: Phase 1 is told to "build" the ground-truth ledger and "put the new-spec line under its title" before any round directory exists
**Severity:** P3
**Where:** spec § Phase 1 authoring changes (spec.md:155)
**Edge case:** Partial failure: a run interrupted between Phase 1 and the first dispatch.
**What happens:** The added clause reads as an instruction to write the file during Phase 1. Decision 5 (spec.md:87) writes it only after the baseline renames, and Decision 4 (spec.md:81) says rows are held. An implementer who follows the Phase 1 wording creates `round-<C>/ground-truth-ledger.md` before the pending marker and the baseline set. If the run is then interrupted, the directory holds one file and no baseline. The next full invocation's "smallest free span" rule (`skills/spec-cycle/SKILL.md:378`) then skips that round number. Nothing is corrupted.
**Why the spec misses it:** "Build the upcoming round's ground-truth ledger while writing" was already there; the new clause about the title makes the file-writing reading more natural.
**Suggested fix:** Reword to "hold the rows and the new-spec line while writing; the file is written at dispatch (Decision 5)".

### F-3: A sample P1 against a section outside `changed_regions` has no filing permission in the unedited `# Delta scope` block
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (spec.md:128, :136)
**Edge case:** A delta pass where a row names an unchanged section. This happens when rows are held to fix a P2 omission with no spec edit (spec.md:112), or after a rebuild.
**What happens:** Decision 8 says the sample "is not limited by `changed_regions`" and rule 3 files a P1 "against the spec section that holds the claim". The byte-identical `# Delta scope` block (`agents/spec-reviewer-correctness.md:90-98`) lists the checks that are not limited (Deferred block, closures, vanished references, process failures) and allows an out-of-region filing only for a P0. One reviewer files the P1; another reads the block as forbidding it and drops a blocking finding. The gate result can differ between two runs.
**Why the spec misses it:** The round-4 fix stated that the read is not limited, but not that the filing is.
**Suggested fix:** Add one sentence to the `**Ground-truth check.**` block, which sits outside `# Delta scope`: "A finding this block produces is filed against the section the row names, on a full or a delta pass."

### F-4: Ticket lookup blocked
**Severity:** P3
**Where:** grounding step 3
**Edge case:** External system unavailable. `memory_search` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`.
**What happens:** The review proceeded from the brief alone, per the documented degraded path.
**Why the spec misses it:** Not a spec defect.
**Suggested fix:** None for the spec.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 0

STATUS: GREEN
