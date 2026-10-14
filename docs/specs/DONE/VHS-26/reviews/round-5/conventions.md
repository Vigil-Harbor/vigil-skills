# Conventions Review — round 5

Grounding notes: `review_mode: delta`. Read fresh from disk: the spec (`C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-26.spec.md`, byte-identical to `round-5/spec.copy.md`), the brief (identical to `round-5/brief.copy.md`), the `changed_regions` file, and the three round-4 reviewer reports (not `synthesis.md`). Conventions source: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\AGENTS.md` (the gitignored `CLAUDE.md` points to it). Wiki: `projects/vigil-skills/state.md` and `filemap.md` (relevant entries only; no `architecture.md` exists for this project). Decisions read: review-round artifacts are immutable (2026-08-09), VHS-43 in-scope P1 always folds, VHS-27 delta-scoped review passes, VHS-60 delta scope resolver. The shared-memory ticket lookup was denied (`agent 'claude' lacks 'read' on namespace 'skills'`), so I proceeded from the brief. Nothing under `VHS-26.attempt-1/` was read.

Deferred-findings block: one `## Deferred — follow-up required` section, with the preamble blockquote carrying the required sentence. Row D-1 is well-formed: titled heading, seven fields, blockquoted fix with one blank line before `Propagation sites`, and three sites that all exist as headings. Its `Scope` states `skills/spec-cycle/SKILL.md` §2g, and the brief's Scope table has no §2g row, so the stated region is correct. The token is `out-of-scope`, so the ceiling does not apply. No routing violation, and D-1's root is not re-filed.

Anchor check for the changed regions: every `file:line` citation resolves to the named symbol at HEAD `fc20f94` (equal to `round-5/baseline.commit`; the cited files have no working-tree changes). Checked: `skills/spec-cycle/SKILL.md:390`, `:558`, `:578-579`, `:711-718`, `:715`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`. No dead or moved citations.

Deleted headings (bodies read in `round-4/spec.copy.md`):
- **`## Deferred (P2+)`** held four entries, and each is now folded in the spec text:
  - the narrowing of brief Decision 7 is recorded at spec.md:34;
  - the disposition phrase carries the path at spec.md:110;
  - the `Pre-ship recommended` tag is dropped at spec.md:140, with the green-round sentence at spec.md:112;
  - the row-versus-drift precedence is stated at spec.md:134 and spec.md:137.
- **`## Post-green polish`** held one line, recording a round-4 rewording of a sentence in § Correctness reviewer changes. This revision rewrote that sentence again (spec.md:179).
- The removal drops nothing live. `skills/spec-cycle/SKILL.md:946-947` treats an absent section as "2g not yet run", and no other skill reads either heading (grep over `skills/` and `agents/`). The round-4 reports and spec copy keep the record, in line with the immutable-round-artifacts decision. No finding.

## Closure of round 4 findings

The closure manifest is empty because round 4 closed green with no P0 or P1. The table tracks the P2 to P4 findings so the fold can be checked.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P2) | Row-named omission boundary narrows brief Decision 7's third trigger | CLOSED | Both suggested fixes applied. The new-spec line is restored (spec.md:75, :140) with no manifest read, and the narrowing is recorded at spec.md:34 and in the stated limits at spec.md:143. |
| correctness | F-2 (P2) | Closing `ground-truth ledger missing` is pinned for the correctness agent only | CLOSED | spec.md:110 puts the round-`<C+1>` path in the phrase; spec.md:179 names it as what the other lenses check; Test plan spec.md:201 adds the two-lens case. Residual filed as F-2 below. |
| correctness | F-3 (P2) | Grading order ambiguous for a dead anchor that appears only in the row | CLOSED | spec.md:134 (rule 1 comes first) and spec.md:137 ("never a citation that appears only in the row"); Test plan spec.md:199 names the combined case. |
| correctness | F-4 (P3) | Ticket not cached | PARTIAL | Host condition; the lookup was denied again. No spec defect. |
| correctness | F-5 (P3) | Phase 1 rows dropped after a failed first write; "Three rules" count nit | CLOSED | spec.md:110 ("this includes Phase 1's rows and the new-spec line"); Test plan spec.md:201; the preamble no longer states a count (spec.md:26-32). |
| edge-cases | F-1 (P2) | Omission P2 tagged `Pre-ship recommended` | CLOSED | spec.md:140 ("Do not tag it"); spec.md:112; Test plan spec.md:200 ("untagged in every case"). |
| edge-cases | F-2 (P2) | Other lenses have no rule for closing `ground-truth ledger missing` | CLOSED | Same evidence as correctness F-2. |
| edge-cases | F-3 (P3) | "Opens code anchors, not spec sections" does not match the Sample bullet | CLOSED | spec.md:128 uses the suggested wording. See F-3 below for the drift-check note. |
| edge-cases | F-4 (P3) | Three row and closure states have no grading rule | CLOSED | spec.md:134 (sentence absent, or no anchor); spec.md:141 (REOPENED, counted once); Test plan spec.md:199 and :201. |
| edge-cases | F-5 (P3) | A no-claims line on a new spec passes every check | CLOSED | spec.md:143 names it as the second stated limit. |
| edge-cases | F-6 (P3) | Ticket lookup blocked | PARTIAL | Same host condition. |
| conventions | F-1 (P2) | Omission finding tagged `Pre-ship recommended` | CLOSED | Same evidence as edge-cases F-1. |
| conventions | F-2 (P2) | Missing-file disposition carries no anchor a lens without the path can verify | CLOSED | spec.md:110 and :179. |
| conventions | F-3 (P2) | Preamble says Decision 8 carries brief Decision 7 but it narrows it | CLOSED | spec.md:34. |
| conventions | F-4 (P3) | Spec-level additions for the human drift check | CLOSED | spec.md:26-32 lists every item round 4 named. Two smaller ones from this revision are in F-3 below. |

## Findings

### F-1: Under "apply the first rule that matches", the unsupported-anchor rule comes before the Anchor drift rule
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Grading a checked row, spec.md:133-137)
**Convention violated:** Prior decision VHS-27 #9 ("Anchor drift splits by cause, in both modes": a moved line is one combined P4, a gone symbol is a P1), and the existing rule at `agents/spec-reviewer-correctness.md:109`.
**Evidence:** Rule 3 reads "The anchor does not support the claim as the spec states it: file a P1". Rule 4 hands a dead or moved spec-sentence anchor to Anchor drift. Read literally, a moved line or a gone file also "does not support the claim", so rule 3 matches first and rule 4 is never reached. A moved line would then be a blocking P1 instead of the combined P4. The dedupe paragraph at spec.md:139 rescues the outcome in practice, because Anchor drift files the citation independently. The numbered order still contradicts the instruction to apply the first match.
**Suggested fix:** Swap rules 3 and 4, or open rule 3 with "The anchor's file and symbol resolve at the cited line, and the line does not support the claim".

### F-2: The closure route for the other lenses rests on unedited text that says something else
**Severity:** P3
**Where:** spec § Correctness reviewer changes (spec.md:179); spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (step 6, spec.md:110)
**Convention violated:** Cross-surface contract left implied; the manifest rule at `skills/spec-cycle/SKILL.md:584-590`.
**Evidence:**
- spec.md:179 says the other lenses "verify it from the path on the manifest line".
- spec.md:128 says those lenses' "verification duties do not change", and their step 7 verifies each finding "against the current spec".
- `skills/spec-cycle/SKILL.md:589-590` (not edited) says a disposition is "always with a spec § anchor the reviewer can verify". The new phrase has a path and no `§`.

The missing-STATUS precedent at `SKILL.md:578-579` already breaks that sentence, so this is defensible. A file-existence check in the reviews directory is still a duty that no unedited agent text states.
**Suggested fix:** Add one clause in §2e where the phrase is introduced: "the path stands in for the § anchor; a reviewer closes the finding by checking that the file exists with content". This stays inside `skills/spec-cycle/SKILL.md` and edits no fenced agent.

### F-3: Spec-level additions in this revision, for the human drift check
**Severity:** P3
**Where:** spec § Decisions (spec.md:26-34); spec § Decision 4 (spec.md:75); spec § Decision 8 (spec.md:128, :134)
**Convention violated:** Silent-addition audit, category (c): additions with rationale must stay visible.
**Evidence:** All three stay inside the brief's fences (no parser, no computed inventory, no link to changed-regions, no new halt or marker state).
- **The restored new-spec line** `New spec: rows cover every section.` and the "every section" omission boundary. It is listed at spec.md:29 with rationale. It reads no manifest, so round-3 F-1 stays closed. It does not conflict with the brief's "no computed expected coverage" fence, because spec.md:140 forbids computing an inventory.
- **"The sample is not limited by `changed_regions`"** (spec.md:128). This is not in the preamble list. The shared `# Delta scope` block lists the checks that run everywhere and does not name this one, and the brief forbids editing that block. VHS-27 decision 7 lets grounding run everywhere, so the position is consistent with it, but the agent will hold a specific sentence outside the block that extends the block's list.
- **A sampled sentence that carries no anchor is graded P2** (spec.md:134). The preamble names only "the P2 for a row that differs from its spec sentence". The stated reason, "so that a defect in the row alone never blocks", does not cover this case: a missing anchor is a defect in the spec sentence, against Decision 3. Brief Risks item 3 leaves severities to the spec author, so this is permitted.

**Suggested fix:** Add the last two items to the Decision 8 bullet at spec.md:32. Reword the rule-1 rationale to "so that a row defect or a missing anchor is advisory; only an anchor that contradicts the claim blocks".

### F-4: The green-round sentence sits in the §2e block, which a green round never runs
**Severity:** P4
**Where:** spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (spec.md:112)
**Convention violated:** Reuse of an existing rule without naming it.
**Evidence:** `skills/spec-cycle/SKILL.md:943-945` says "the round that goes green never runs 2e". The listing in `## Deferred (P2+)` on a green round is already done by 2g steps 2 and 4 (`SKILL.md:956-969`), unedited. The sentence is therefore descriptive and needs no §2g edit, which also keeps it clear of row D-1.
**Suggested fix:** Append "(by the existing 2g carry-forward, which this ticket does not edit)".

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 3 | P4: 1

STATUS: GREEN
