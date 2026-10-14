# Conventions Review — round 4

Grounding notes: `review_mode: delta`. Read fresh from disk: the spec (`C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-26.spec.md`, byte-identical to `round-4/spec.copy.md`), the brief, the `changed_regions` file, the closure manifest (`round-3/ledger.md`), and the three round-3 reviewer reports (not `synthesis.md`). Conventions source: `AGENTS.md` (the gitignored `CLAUDE.md` points to it). Wiki: `projects/vigil-skills/state.md` (header and VHS entries only); no `architecture.md` exists for this project; decisions read: VHS-37 fold/defer/reject routing, VHS-43 in-scope P1 always folds, VHS-27 delta-scoped review passes. The shared-memory ticket lookup was denied again (`agent 'claude' lacks 'read' on namespace 'skills'`), so I proceeded from the brief. Nothing under `VHS-26.attempt-1/` was read.

Deferred-findings block: one section, preamble blockquote present with the required sentence. Row D-1 is well-formed: titled heading, seven fields, blockquoted fix with one blank line before `Propagation sites`, three sites that all exist as headings. Its `Scope` states `skills/spec-cycle/SKILL.md` §2g, and the brief's Scope table has no §2g row, so the stated region is correct. The token is `out-of-scope`, so the ceiling does not apply. No routing violation. D-1's root (post-green polish grounding) is not re-filed.

Anchor check for the changed regions: every `file:line` citation resolves to the named symbol at HEAD `fc20f94` (equal to `round-4/baseline.commit`). Checked: `skills/spec-cycle/SKILL.md:390`, `:444-458`, `:450`, `:454`, `:460`, `:462`, `:558`, `:578-579`, `:594-601`, `:698`, `:711-718`, `:715`, `:757`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`. No dead or moved citations.

## Closure of round 3 findings

All four manifest lines are `reworked: deliberate direction change`. Each names the sections it edited, and every named section appears in `changed_regions`.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Delta pass 1 after a red halt carries a closure manifest, so the omission boundary is not empty on a re-run | CLOSED | spec § Decision 8, Omission bullet (spec.md:124): the boundary is the sections the rows name, "A file with no rows has no boundary", and it does not "derive edited sections from the closure manifest". The new-spec line is gone from the whole spec (grep, no hits). Test plan spec.md:184 names the delta-pass-1 case with a manifest. |
| edge-cases | F-1 (P0) | Delta pass 1 after a red halt has a closure manifest, so the omission boundary fires where the spec says it must not | CLOSED | Same root and evidence as correctness F-1; Decision 4 third bullet (spec.md:67) and § Round artifact and dispatch changes (spec.md:147) agree. |
| correctness | F-2 (P1) | An evidence-only ground-truth fix puts a section in the omission boundary with rows for only the named claims | CLOSED | spec § Decision 6 step 6 (spec.md:98-100): the `ground-truth rows carried` disposition is removed (grep, no hits). An unsupported claim is an ordinary fold with `fixed: edited § <section>` and step 5 supplies every row for that section. An omission is now P2 (spec.md:124). § Apply-findings changes (spec.md:155) matches. |
| edge-cases | F-2 (P1) | An evidence-only fix carries rows for the named claims only, but its disposition puts the whole section in the omission boundary | CLOSED | Same root and evidence as correctness F-2. |
| correctness | F-3 (P3) | Decisions preamble does not mark the author-pinned choices | CLOSED | spec.md:24 names Risks items 2, 3 and 5 and what each pinned. The residual about the additions list is F-3 below. |
| correctness | F-4 (P3) | ticket not cached | PARTIAL | Host condition; the lookup was denied again this round. No spec defect. |
| correctness | F-5 (P4) | Done-when item 6 and § Test command quote the unittest pattern differently | CLOSED | spec.md:197 and spec.md:209 both use `-p "test_*.py"`. |
| edge-cases | F-3 (P2) | A ground-truth finding on the final allowed pass gets a `fixed:` disposition for rows that are never written | CLOSED | spec.md:100: one phrase on every pass, "rows the missing file would have held are not reconstructed"; Closure bullet spec.md:125 closes on the file existing with content. |
| edge-cases | F-4 (P2) | "Section" is not defined the same way for the author's rows and the reviewer's boundary | CLOSED | spec.md:61, spec.md:97 and spec.md:124 all use the innermost heading's own body. |
| edge-cases | F-5 (P2) | Closure rule cannot be met when the fix removes or rewrites the named claim | CLOSED | spec.md:125 verifies against the current spec like any spec finding; Test plan spec.md:185 covers "fixed by deleting it". |
| edge-cases | F-6 (P3) | Held rows have no durable home between authoring and dispatch | CLOSED | spec.md:71 adds the rebuild rule and the accepted interruption gap; spec.md:145 places it in `### Round artifacts`. |
| edge-cases | F-7 (P3) | "Check at most five rows" conflicts with "also check every row a predecessor finding named" | CLOSED | The predecessor-row clause is removed from the Sample bullet (spec.md:122). |
| edge-cases | F-8 (P3) | Ticket lookup blocked | PARTIAL | Same host condition as correctness F-4. |
| conventions | F-1 (P2) | New `fixed: ground-truth rows carried` disposition is not reconciled with the manifest vocabulary, the recount trigger, or the other lenses' closure check | PARTIAL | Points 1 and 2 are closed by removal: no section-naming form is added, and the replacement phrase names no section, so the recount at `SKILL.md:757` never reads it. Point 3 (how a lens without the path closes the finding) is still open; see F-2. Stays P2. |
| conventions | F-2 (P2) | `Anchor: none` relaxes brief Decision 1 but is presented as carried from the brief | CLOSED | spec.md:40 ("These two rules are a spec-level addition to brief Decision 1") and spec.md:24. Decision 8 now grades a `none` row for "a file this host can read" (spec.md:123). |
| conventions | F-3 (P2) | Decision 3 uses the bare word "ledger" | CLOSED | spec.md:40 and spec.md:42 now read "ground-truth-ledger row" and "ground-truth ledger". No bare use remains in a changed body. |
| conventions | F-4 (P3) | Spec-level additions in this revision, for the human drift check | PARTIAL | spec.md:24 lists three additions and the Risks items. The list is not complete for this revision; see F-3 and F-4. |

## Findings

### F-1: The omission finding is tagged `Pre-ship recommended`, which the repo defines as a spec-text fold in 2g
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Omission bullet, spec.md:124); spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (spec.md:102)
**Convention violated:** Naming and labels — reuse of an existing tag with a different meaning.
**Evidence:**
- `agents/spec-reviewer-correctness.md:210-216`: emit the line "only on P2 findings where you recommend the orchestrator fold the clarification into the spec during spec-cycle's post-green polish step (2g)".
- `skills/spec-cycle/SKILL.md:949-964`: 2g collects every tagged P2 from all rounds and applies it "only if it is a clarification — wording, file:line anchors, examples, error-message text, checklist rows".
- spec.md:102 says an omission is fixed "by holding rows for that section for the next dispatch". That is no spec edit, and spec.md:87 says polish writes no ground-truth ledger.

On a green round the tagged omission becomes a 2g candidate with nothing to fold and no later dispatch to hold rows for. The implementer of 2g has no rule for it, and the correctness agent is told to use a tag whose own contract it does not meet.
**Suggested fix:** Drop "tagged `Pre-ship recommended`" from the Omission bullet. In spec.md:102 add: "On a green round there is no next dispatch; the finding is listed in `## Deferred (P2+)`." Update the Test plan omission row (spec.md:184) if it should assert the untagged form.

### F-2: The missing-file disposition carries no anchor a lens without the path can verify (residual of round-3 conventions F-1)
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (step 6, spec.md:100); spec § Correctness reviewer changes (spec.md:163)
**Convention violated:** Cross-surface wire-format lock; the manifest rule that a disposition is verifiable by the reviewer.
**Evidence:**
- `skills/spec-cycle/SKILL.md:584-590`: each P0/P1 line carries a disposition phrase "always with a spec § anchor the reviewer can verify".
- The new phrase `fixed: ground-truth ledger to be written at the next dispatch` names no section and no path. The cited precedent (`SKILL.md:578-579`, the synthetic missing-STATUS line) is real, so the form is defensible.
- spec.md:163 claims "Each blocking finding closes by a rule every lens can already apply ... a missing file is fixed by the file existing." The edge-cases, conventions and scalability agents verify predecessor findings "against the current spec", receive no `ground_truth_ledger_path` (spec.md:118), and are not edited. Only the correctness Closure bullet (spec.md:125) says how to close this finding.

A lens that cannot verify a `fixed:` claim may mark the finding REOPENED, which its step 7 grades P0. The phrase also promises a future write rather than recording a fix, so it reads the same whether or not the next write succeeds.
**Suggested fix:** Either weaken spec.md:163 to say the correctness lens closes the missing-file finding and the other lenses treat it as a process finding with no spec site, or have §2e's phrase carry the reviews-directory file name (`ground-truth-ledger.md` in the next dispatched round's directory) so any lens can check existence. Both edits stay inside `skills/spec-cycle/SKILL.md`.

### F-3: The preamble says Decision 8 "carries brief Decision 7" and lists three additions, but Decision 8 now narrows that brief decision
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions (spec.md:22, spec.md:24); spec § Decision 8 — Correctness alone enforces the ledger (spec.md:124, spec.md:127)
**Convention violated:** Silent additions vs the brief — a departure with rationale that the provenance paragraph mislabels.
**Evidence:**
- Brief Decision 7 (brief.md:40): the correctness agent "files a finding ... when its own normal read of the spec finds a runtime-behavior claim with no row."
- Spec Decision 8: the finding is filed only for a claim inside a section some row already names, and "a section the author edited and gave no row at all draws no ground-truth finding".
- Brief Decision 2 and spec.md:65 require a row for every claim in a new spec, but a new spec's section with no rows is now outside enforcement.

The spec gives a rationale ("stated limit", VHS-61), and the direction change is the answer to two round-3 P0s, so this is not a silent addition. But spec.md:24 says "Three rules are the spec author's additions", and the human drift check reads that paragraph.
**Suggested fix:** In spec.md:24 add: "Decision 8 also narrows brief Decision 7: an omission is filed only inside a section the rows name, and is advisory (P2); a section with no rows is left to step 5 and VHS-61." Change "Three rules are" to wording that does not read as exhaustive, or complete the list per F-4.

### F-4: Spec-level additions in this revision, for the human drift check
**Severity:** P3
**Where:** spec § Decision 4 (spec.md:61, spec.md:71); § Decision 6 step 6 (spec.md:100, spec.md:102); § Decision 8 (spec.md:123, spec.md:125)
**Convention violated:** Silent-addition audit, category (c): additions with rationale must stay visible.
**Evidence:** None of these is in the brief's Decisions or in spec.md:24's list; each carries inline rationale and stays inside the brief's fences (no parser, no computed inventory, no new halt, retry or marker state):
- the rebuild rule for held rows and the accepted interrupted-before-first-dispatch gap (spec.md:71);
- "the row's anchor is the anchor the spec sentence carries" and the P2 for a row that differs from a correct spec sentence (spec.md:61, spec.md:123);
- the literal process phrase `fixed: ground-truth ledger to be written at the next dispatch` (spec.md:100) — a new literal, although no new section-naming form;
- the closure rule for a missing-file finding and the combined P3 for an unreadable out-of-root anchor (spec.md:123, spec.md:125).

They agree with prior decisions: VHS-43's ceiling is used unchanged (`SKILL.md:715`), VHS-27's two counters are respected (`<C>`, `<C+1>`, "final allowed pass"), and no mode-table row moves.
**Suggested fix:** Extend spec.md:24 with one sentence naming these, or leave as is; nothing here blocks.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
