# Edge-Cases Review — round 6

Grounding notes: `review_mode: delta`. The spec, brief, `changed_regions` file and the three round-5 reviewer reports were read fresh from disk (`synthesis.md` not read; nothing under `VHS-26.attempt-1/` read). The project `CLAUDE.md` was read as supplied in context. The Plane ticket lookup was denied (`Access denied: agent 'claude' lacks 'read' on namespace 'skills'`), so the review proceeded from the brief (F-5).

Anchors: every `file:line` citation I re-checked resolves to the named symbol at HEAD `fc20f94` (equal to `round-5/baseline.commit`). That covers `skills/spec-cycle/SKILL.md` `:390`, `:450`, `:454`, `:460`, `:462`, `:558`, `:578-579`, `:594-601`, `:698`, `:711-718`, `:715`, `:757` and `agents/spec-reviewer-correctness.md` `:86`, `:88`, `:109`. No dead or moved citations.

Deferred-findings block: one `## Deferred — follow-up required` heading, and its preamble carries the required sentence. Row D-1 is well-formed (seven fields, blockquoted fix, one blank line before `Propagation sites`, three sites that all exist). Its `Scope` token is `out-of-scope`, so the ceiling does not apply. No routing violation; D-1's root is not re-filed.

Deleted heading `## Deferred (P2+)`: read in `round-5/spec.copy.md`. It held one entry, the grading-order P2 (correctness/R5/F-1, edge-cases/R5/F-1). This revision folds it: Decision 8's rules are reordered as that entry suggested and the Test plan row states the grades. The removal drops nothing live.

## Closure of round 5 findings

The manifest is empty (round 5 closed green, no P0/P1). The round-5 P2–P4 findings are listed for completeness.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P2) | Unsupported-anchor P1 ahead of the Anchor drift rule | CLOSED | § Decision 8 rules 4 and 5 (spec.md:137-138); Test plan (spec.md:200). New variant: F-1 below |
| correctness | F-2 (P3) | Preamble vs "adds no manifest vocabulary" | CLOSED | § Apply-findings changes (spec.md:172) |
| correctness | F-3 (P3) | Illustrative block does not show the new-spec line | CLOSED | sentence added after the block (spec.md:71) |
| correctness | F-4 (P3) | Ticket not cached | N/A | process finding; recurs as F-5 below |
| edge-cases | F-1 (P2) | First-match order misgrades three row states | CLOSED | rules 1–5 reordered (spec.md:134-138); Test plan grades (spec.md:200). New variants: F-1, F-2, F-3 below |
| edge-cases | F-2 (P3) | Phase 1 told to "build" the file before a round directory exists | CLOSED | "hold the rows … written at dispatch (Decision 5), not during Phase 1" (spec.md:156) |
| edge-cases | F-3 (P3) | No filing permission for a sample P1 outside `changed_regions` | CLOSED | sentence added (spec.md:140); residual wording in F-4 below |
| edge-cases | F-4 (P3) | Ticket lookup blocked | N/A | process finding; recurs as F-5 below |
| conventions | F-1 (P3) | Unsupported-anchor rule before Anchor drift | CLOSED | same as correctness F-1 |
| conventions | F-2 (P3) | Closure route for other lenses rests on unedited text | CLOSED | "The path stands in for the `§` anchor" (spec.md:110) |
| conventions | F-3 (P3) | Spec-level additions not listed | CLOSED | Decision 8 bullet (spec.md:32); rule 3 rationale reworded (spec.md:136) |
| conventions | F-4 (P4) | Green-round sentence sits in the §2e block | CLOSED | parenthetical added (spec.md:112) |

## Findings

### F-1: A moved line whose code no longer supports the claim stops at rule 4 and draws only the combined P4
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Grading a checked row, spec.md:133-138); spec § Test plan (spec.md:200)
**Edge case:** A sampled row has two defects at once: the cited line is stale, and the code at the symbol's real location does not do what the sentence says. The typical cause is an author who cites a wrong line and also misreads the function.
**What happens:** The list is strict first-match. Rule 4 matches ("or only its line moved") and hands the citation to Anchor drift, which files the combined P4. Rule 5, the blocking `runtime claim not supported by its anchor`, is never reached. The round stays green on a false runtime claim.
- On a full pass, the agent's step 5 would probably still catch it.
- On a delta pass it would not when the row names an unchanged section, because the sample is the only check that is "not limited by `changed_regions`" (spec.md:128).

Nothing crashes, so this is P2, but it silently turns one of the two blocking checks into a nit.
**Why the spec misses it:** Round 5's reorder put Anchor drift ahead of the unsupported-claim rule to stop a stale line number from blocking. Rule 5's precondition "the file and symbol resolve" is also true for a moved line, but first-match never gets there. The Test plan lists "a line that only moved (combined P4, no P1)" and has no case for a moved line with unsupported code.
**Suggested fix:**
- Split rule 4. Keep "the file or symbol of the spec sentence's own anchor is gone: Anchor drift grades it, P1 per dead citation" as a terminal rule.
- Reword the moved-line half: "When only the line moved, the citation joins Anchor drift's combined P4, and grading continues at rule 5 against the code at the symbol's current line."
- Add a Test plan case: "a line that moved and whose code does not support the claim (combined P4 and P1)".

The fix edits Decision 8, so 2g cannot apply it; it needs a revision or an operator edit.

### F-2: An `Anchor: none` row whose spec sentence carries an anchor is graded by rule 1, not as a row defect
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (rules 1 and 3, spec.md:134, :136)
**Edge case:** Row and sentence disagree in the direction rule 3 does not name. Rule 3 covers "the row gives an anchor and the sentence carries none"; the mirror state, row `none` and sentence anchored, matches rule 1 first.
**What happens:** Two outcomes, both wrong:
- The sentence's own anchor shows the behavior lives in a readable file, so rule 1's condition holds and it files a P1 against a spec sentence that is correctly anchored. Decision 6 step 6 then prescribes "correct the sentence or its anchor", and there is nothing to correct. This contradicts rule 3's stated intent that a row defect is advisory.
- The reviewer follows "do not open anything" and files nothing, so the row defect goes unreported.

The same first-match stop means a `none` row whose sentence is not in the spec at all never reaches rule 3's P2. The cost is a spurious red round or a missed advisory; no corruption.
**Why the spec misses it:** Rule 1 keys on the row alone; the round-5 reorder moved it ahead of the row-versus-sentence comparison.
**Suggested fix:** Open rule 1 with "The row reads `Anchor: none` and the spec sentence it names carries no anchor". Extend rule 3's second condition to "the row and the sentence disagree on whether there is an anchor". Add the Test plan case "an `Anchor: none` row whose sentence carries a correct anchor (P2, not P1)".

### F-3: Rule 2's "no other finding" does not bind the agent's own Anchor drift rule on the same citation
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (rule 2 and the "One defect is one finding" paragraph, spec.md:135, :140); spec § Test plan (spec.md:200)
**Edge case:** Runtime precondition violation: the reviewer runs on a host without the sibling repository or wiki that an out-of-root anchor names (Decision 3 makes such anchors legal).
**What happens:** The reviewer's normal read meets the same citation in the spec text. The unedited Anchor drift rule (`agents/spec-reviewer-correctness.md:109`) says a citation whose symbol is gone is a P1, and has no out-of-root exception. The dedupe paragraph then gives that filing precedence ("already being filed … under … Anchor drift, do not file it again here"). The combined P3 is suppressed and the P1 stands. The Test plan expects "combined P3, no P1". The author can only reject the finding, so the loop recovers at the cost of a red round.
**Why the spec misses it:** Rule 2 says the row "draws no other finding", which reads as scoped to the ground-truth block. Nothing says how Anchor drift treats an unreadable out-of-root path.
**Suggested fix:** Add to the `**Ground-truth check.**` block, which sits outside the Anchor drift paragraph: "An out-of-root citation this host cannot read is not a dead citation: Anchor drift does not grade it, in the row sample or in the normal read."

### F-4: "A finding this block produces is filed against the section the row names" covers findings that have no row
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (spec.md:140)
**Edge case:** Missing or mismatched inputs to the new filing sentence.
**What happens:**
- The block also produces `ground-truth ledger missing`, `ground-truth ledger path not supplied` and the omission P2. None of them has a row, and the omission finding can span several sections.
- Rules 1 and 5 file "against the spec section that holds the claim". When a row's `Spec section` is wrong or stale (heading renamed, sentence moved), the two instructions name different sections. Decision 6 step 6 folds "at that section" and dispositions `fixed: edited § <section>`, so the manifest can name a section that does not hold the sentence.

A human reviewer resolves both; nothing breaks.
**Why the spec misses it:** The sentence was added to close round-5 F-3 and was written for the common case.
**Suggested fix:** "A finding from a checked row is filed against the spec section that holds the sentence (the section the row names, when the sentence is not in the spec), on a full or a delta pass."

### F-5: Ticket lookup blocked
**Severity:** P3
**Where:** grounding step 3
**Edge case:** External system unavailable. `memory_search` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`.
**What happens:** The review proceeded from the brief alone, per the documented degraded path.
**Why the spec misses it:** Not a spec defect.
**Suggested fix:** None for the spec.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 4 | P4: 0

STATUS: GREEN
