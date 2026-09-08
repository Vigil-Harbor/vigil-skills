# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Revert leaves stale CLOSED entry | CLOSED | spec § Design 3 bullet 2 ("The revert supersedes the reverted finding's closed-issues entry…") + § Decisions D16 |
| correctness | F-2 | "Revert the original fold" undefined after re-edit | CLOSED | spec § Design 3 bullet 2 precondition ("none of the original fold's sites has been re-edited by a later fold") and fallback bullet 3 |
| correctness | F-3 | Row 5's "7 before and after" falsified by R3 | CLOSED | spec § Test plan row 5 now "8 after (7 before)" — but see new F-5 below (wrap-fragile) |
| correctness | F-4 | D15 anchor disagreement | CLOSED | `:435-441` used identically in § Scope row 3, § Design 1 "Round 4", D15 |
| correctness | F-5 | One malformed row → two P0s per lens | CLOSED | spec § Design 7 item 3 ("the defect is reported once, not as a second finding") |
| correctness | F-6 | In-scope-P0 exception vs. opaque `Scope` | CLOSED | § Design 7 block ("That is different from classifying your own candidate…") |
| correctness | F-7 | Revert line out of 2b's round-scoped form | CLOSED | D13 exception clause; § Design 3 line is `<lens>/R<m>/F-<k>`; § Design 4 states it |
| correctness | F-8 | R4 no-op after narrowed brief; D16 headline axis | CLOSED | R4's "delete the spec first — the escape Phase 0's re-run pin already names"; D16 retitled "rounds 2–3 of this invocation" |
| correctness | F-9 | Unreachable "predates this invocation" branch | CLOSED | § Design 3 reworded to a parenthetical observation |
| correctness | F-10 | Done-when 2 / D15 unasserted | CLOSED | § Test plan rows 8 and 9 |
| edge-cases | F-1 | R2 forbids the reads/edits the spec mandates (P0) | CLOSED | R2 rewritten: reads allowed, two permitted edits, never delete, never overwrite `Follow-up:`. The round-4 residue is filed fresh as F-1 below |
| edge-cases | F-2 | Round-4 section in neither bucket | CLOSED | D15 + § Design 1 "Round 4" adopt FROZEN + append carve-out verbatim; row 9 asserts it. (My own suggested wording; its interaction with the repair path is new F-1) |
| edge-cases | F-3 | Nothing verifies the preamble | **PARTIAL** | § Design 7 block adds `routing violation: missing preamble`, but the block never carries the preamble's text, so only the *absent* case is checkable — see F-2 below |
| edge-cases | F-4 | `(new)` sites unfalsifiable | CLOSED | § Design 1 step 1 and the block both require ≥1 existing site |
| edge-cases | F-5 | Recount misses `reworked:` / Decision anchors | CLOSED | § Design 3 "every section named on any `fixed:`/`reworked:` line"; § Design 4's "names every spec section the edit touched" |
| edge-cases | F-6 | Render locator vs. malformed-row fallback | CLOSED | § Design 5 "every `###`-or-deeper heading inside the section" — the consequence is new F-3 |
| edge-cases | F-7 | R4 adopts a half-written spec | CLOSED | R4's required-heading check + halt string; § Out of scope 9 records the write-discipline deferral |
| edge-cases | F-8 | Round-4 reject recorded nowhere | CLOSED | § Design 1 "Round 4" title-suffix rule + minor-additions bullet |
| edge-cases | F-9 | Unbounded rows / version skew | CLOSED | (a) recorded in § Deferred (P2+) under brief Decision 8; (b) applied in § Design 6's `sync.py install` sentence |
| edge-cases | F-10 | Render columns / resolved row | CLOSED | sub-parse rule in § Design 5; suffix half recorded in § Deferred (P2+) |
| edge-cases | F-11 | D15 anchor drift (P4) | CLOSED | unified to `:435-441` |
| conventions | F-1 | Which of R1–R5 ship as prose | CLOSED | § Design 2 sentence after the shape block; row 5 recalibrated |
| conventions | F-2 | R2 contradiction + unfixable rename | CLOSED | R2 carve-out (b) and the mirrored clause in the § Design 7 block — narrow residue filed as F-6 |
| conventions | F-3 | `grep 'DEFERRED, or NEW'` cannot match | CLOSED | row 6 asserts the bare token `DEFERRED`, ≥1 per file |
| conventions | F-4 | Two anchors for one round-4 sentence | CLOSED | unified to `:435-441` |
| conventions | F-5 | Design 3's two manifest forms outside 2b | CLOSED | § Design 4 carries both; § Design 7 item 1 carries the consumer clause |
| conventions | F-6 | `spec-workflow-reference.md` under-scoped | CLOSED | § Scope last row: `:88` gains `DEFERRED` **and** the every-round sentence; row 10 asserts `including round 1` |
| conventions | F-7 | Mandated `routing violation:` title | CLOSED | minor-additions bullet in § Decisions |
| conventions | F-8 | Row 3 parenthetical names 3 of 4 sites | CLOSED | row 3 now `≥ 4` with four sites named |

## Findings

### F-1: At round 4 the deferral section is FROZEN with append as its only permitted edit, so a round-3 routing-violation P0 can never be repaired — and D15 contradicts the FROZEN rule it is inserted beside
**Severity:** P1
**Where:** spec § Decisions D15 (:48), § Design 1 "Round 4" (:74), § Design 7 block (:146), against untouched `skills/spec-cycle/SKILL.md:438-445`
**Edge case:** A reviewer files `routing violation: D-2` (or `routing violation: missing preamble`) as a P0 in **round 3** — the ordinary outcome of a dropped field after the operator's `Follow-up:` hand-edit, which D12 makes the designed path. The gate is red, so 2e runs the round-4 targeted rewrite.
**What happens:** Two things, both fatal to the round.
- **Unrepairable P0.** The round-4 rewrite is the step that addresses round-3 findings. D15 makes `## Deferred — follow-up required` FROZEN with exactly one permitted edit — "appending a row routed in this round" — and adds "no REWRITE section may modify it". Repairing the malformed field (R2 carve-out (a)) or inserting the missing preamble is not that edit, and D15 grants no promotion path, so the P0 survives into round 4's reports, `total_p0p1 ≥ 1` for every lens that ran the block, and the run halts red on a formatting typo. This is round-2 F-1's dead-end reproduced one round later; R2's carve-out closed it for rounds 1–3 only.
- **Internal contradiction in the shipped file.** The untouched classification rule the D15 sentence is inserted directly beneath reads "**FROZEN** — no unresolved P0/P1 in this section across rounds 1–3" (`SKILL.md:438-439`). A routing violation's `Where` *is* that section, so the standing rule classifies it REWRITE while the new sentence, one line later, classifies it FROZEN unconditionally. The round-4 author has two adjacent rules giving opposite answers for the one case that matters; the REWRITE branch loses the finding record D15 exists to protect, the FROZEN branch guarantees the red halt above.
**Why the spec misses it:** D15 was written (from round-2 F-2's suggested fix, mine) to answer "what preserves the section at round 4?" and never asks "what repairs it at round 4?". The interaction with the routing-violation P0 that R2's carve-out was added to make repairable was not re-walked at round 4.
**Suggested fix:** One clause on D15 and its Design 1 mirror: "…with two permitted edits: appending a row routed in this round, and the R2 carve-out repairs — the field a `routing violation: D-<n>` names, a missing preamble, and a re-anchor. Neither is a FROZEN edit and neither needs promotion; the classification rule's 'unresolved P0/P1' test does not apply to this section, whose contents are governed by R2 in every round." Extend checklist row 9's `is FROZEN with one permitted edit` literal to whatever the final wording is.

### F-2: The reviewers are told to check for a "fixed preamble line" whose text ships only into SKILL.md, so the check the spec added cannot be run against a paraphrase
**Severity:** P1
**Where:** spec § Design 7 item 2 (:146), § Design 2 (:78-83), § Decisions D11 (:44), § Design 6 (:138)
**Edge case:** The author writes the section and paraphrases the fence — `> Deferred findings. See the follow-up report.` — dropping "`/ship-spec` must not implement anything in this section". An ordinary LLM-authoring outcome for a fixed-string rule stated once, and the expected outcome for a section created by the documented option-1 hand-patch.
**What happens:** The block's whole preamble rule is "The section must carry **its fixed preamble line** immediately under the heading; if it does not, file a P0". The four agent files are byte-identical and self-contained by construction — D11 states outright that "Agents have no include mechanism and must not read the skill file by an install-specific path" — and the block never carries the preamble's text. So a reviewer has no referent for "its fixed preamble line": it can detect an *absent* line, but cannot adjudicate a present-but-weakened one, and will read any blockquote under the heading as satisfying the rule. The spec then goes green with the section's only fence missing its operative sentence, and `/ship-spec` (`skills/ship-spec/SKILL.md`: "Read the spec and implement the changes described") reads the most implementation-ready block in the file — a named target section, a verbatim `Suggested fix`, and an explicit site list — with nothing telling it to skip. The deliberately-deferred multi-site propagation lands in shipped code having been reviewed by no round, which is strictly worse than folding it. Checklist row 8's `grep -cF 'must not implement anything in this section' skills/spec-cycle/SKILL.md` asserts only that the *producer* says to write it.
**Why the spec misses it:** D11 identified exactly this consumer-side problem for the row and solved it by carrying the seven field labels into the block; the preamble was added later (round-2 F-3) on the producer side and did not get the same treatment.
**Suggested fix:** Make the check textual, in the block itself: "The section must carry its preamble line immediately under the heading — a blockquote containing the sentence `/ship-spec` must not implement anything in this section. If the line is absent or does not carry that sentence, file a P0 titled `routing violation: missing preamble`." Add to checklist row 6: `grep -cF 'must not implement anything in this section' agents/spec-reviewer-*.md` → 1 per file, four files.

### F-3: A verbatim `Suggested fix` carrying a markdown heading silently truncates the section or invents a row
**Severity:** P1
**Where:** spec § Design 2 row shape (:89), § Design 5 extraction rule (:131), § Design 7 block (:146)
**Edge case:** The deferred finding's `Suggested fix` quotes markdown — a proposed heading, a fenced block, or replacement prose containing `##`/`###` at line start. Not exotic: reviewer suggested fixes in this very run routinely quote section headings and rule text, and several quote `## Deferred — follow-up required` itself.
**What happens:** The field is mandated as "`<the reviewer's Suggested fix, unedited>`" and labelled `(verbatim)`, so the author must copy heading lines through. Round 2's F-6 fix broadened the render's locator from `### D-<n>:` to "**every `###`-or-deeper heading inside the section**", which turns any copied `###` line into a phantom row: the report prints `- D-?  (malformed row — see § Deferred — follow-up required)` for text that is not a row, and the reviewers' well-formedness scan sees a heading with none of the seven fields — a routing violation P0 with no field to repair, since R2's carve-out (a) repairs "the field a `routing violation: D-<n>` finding names" and this violation names none.
The `##` case is worse. The section is defined as "a spec section at the end of the spec, found by exact heading"; a copied `##` line at line start ends it. Every row after that point falls outside the section: the render omits them (breaking Design 5's "never omits a heading it found", because the locator never reaches them), the reviewers do not see them, D14 suppression stops applying, and all those deferred P0/P1s return as fresh findings on the next round — the feature unwinding itself silently, which § Design 6 names as the one failure mode this machinery exists to prevent.
**Why the spec misses it:** The row shape treats `Suggested fix` as a scalar on one template line; the extraction rule was widened for robustness against a malformed *heading* and never re-checked against the one field whose contents are attacker-shaped by construction (arbitrary reviewer markdown, copied unedited).
**Suggested fix:** One clause in Design 2's shape and one in Design 5: "`Suggested fix (verbatim)` is copied unedited except that every line which would parse as a markdown heading (`#`-prefixed at line start) or as a fence is prefixed with `> ` so it cannot be read as a row heading or a section boundary; the text is otherwise unchanged. The section ends at the next `##` heading that is not inside a row's quoted block." Mirror one sentence in the § Design 7 block so the consumer applies the same boundary.

### F-4: A duplicate `## Deferred — follow-up required` section is undefined — the render, `D-<n>` allocation, and D14 suppression all silently pick one
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 (:78), R1 (:97), § Design 5 (:123, :131), § Design 7 block (:146)
**Edge case:** Two sections with the same heading. Reachable by the documented option-1 hand-patch, by a re-run whose author appends a section it did not notice was already there, and by F-3's boundary truncation above (which effectively yields a second, orphaned block).
**What happens:** Every rule keys on "the section", singular. R1 allocates from "the highest number **already in the section**", so a second section restarts at `D-1` and two rows now answer to the same id. `deferred: D-1` in the manifest then matches two rows; the reviewer verifying well-formedness may check the well-formed one and pass a malformed one, and D14 suppression ("match on `D-<n>` and the row title") can retire a live P1 against the wrong row's root. Design 5 renders "from `## Deferred — follow-up required` and nothing else" without saying which, so the report can print one section's rows and drop the other's — a silently dropped follow-up. Nothing corrupts code; the accounting quietly goes wrong.
**Why the spec misses it:** The section is treated as a singleton because the skill creates it. The skill has two recorded idioms for exactly this hazard which the spec does not reach for: 2g's "if a `## Post-green polish` section already exists … reconcile (merge/dedup) rather than append" (`SKILL.md:600-601`) and Phase 0 step 8's `multiple Scale sections — using first` token.
**Suggested fix:** One sentence in Design 2: "If more than one `## Deferred — follow-up required` heading is present, the first is authoritative and the author merges the later ones into it in the same round, renumbering colliding `D-<n>` ids from the highest in the merged section (the finding record is otherwise unchanged); reviewers file a routing violation naming the duplicate if it is still present." One clause in the § Design 7 block so the consumer can see it.

### F-5: Checklist row 5's exact `→ 8` is falsified by a benign line wrap in R3
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 5 (:160), § Design 2 R3 (:99)
**Edge case:** The implementer wraps R3 at the ~72-column width `SKILL.md` uses in the round-4 half (`:435-464`) and the 2b prose (`:369-383`), rather than the unwrapped style of the 2e rounds-1–3 bullets (`:431`).
**What happens:** R3 carries the literal `## Deferred (P2+)` **twice on one line**; `grep -c` counts lines, so a single-line R3 gives 8 (verified baseline: 7) and a wrapped R3 that breaks between the two literals gives 9. The row asserts exactly 8, so a byte-correct implementation fails its own gate and the implementer chases a phantom regression or hand-edits the checklist — the same trap round-2 correctness/F-3 flagged, moved one notch. The spec nowhere says R3 must stay on one line.
**Why the spec misses it:** Row 5 was recalibrated from 7 to 8 by counting occurrences of the new rule, not lines of the new rule, and the repo's own recorded practice ("assert hunk regions not counts") was applied to row 4 but not carried back to row 5.
**Suggested fix:** Make it wrap-proof: `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → 8 **or 9** (the one new rule R3 carries the literal twice; a line wrap between them adds a second matching line), with row 4's hunk assertion — no hunk over `:411-424`, `:431`, `:593-624` — as the actual protection of brief Decision 5. Or drop row 5 and say so.

### F-6: R2's re-anchor carve-out has no target when a section is removed with no successor, and the resulting routing violation has no repair
**Severity:** P2
**Where:** spec § Design 2 R2 clause (b) (:98), § Design 7 block well-formedness rule (:146)
**Edge case:** A later round's fold consolidates two Design sub-sections into one under a *different* name, or a round-4 REWRITE drops a section entirely. The removed section is the only site on a row's `Propagation sites` that existed (the rest are `(new)`).
**What happens:** R2(b) permits "re-anchoring `Where` or `Propagation sites` **to a new heading** when a later round renames or removes the section they name" — for a removal with no successor there is no new heading to name. The block's well-formedness rule requires "at least one of them exists in the spec", so the row is now not well-formed; the reviewers file `routing violation: D-<n>` every round, and the two permitted edits do not include marking a vanished site `(new)` or retiring an obsolete row (R5 leaves resolution judgment entirely to the operator, and the skill "never deletes a row"). The gate cannot go green until the operator hand-edits outside the skill — the narrow residue of the loop round-2 F-1 closed.
**Why the spec misses it:** The rename case drove R2(b) and "removes" was added to the same clause without asking what the re-anchor target is when nothing replaces the section.
**Suggested fix:** Extend R2(b): "…to a new heading; when the section was removed with no successor, the author appends `(section removed round <n>)` to that site instead — the site no longer counts toward the two-site minimum, and a row left with no existing site is annotated `obsolete: root removed round <n>` in `Follow-up:` and is not a routing violation." Mirror the two markers in the § Design 7 block's well-formedness rule.

### F-7: A Settled grill decision to defer a finding has no landing place, and the report re-rendered two steps later will not show it
**Severity:** P2
**Where:** spec § Design 1 (:70, "Routing does not run inside 2f-i step 4"), § Design 5 red-path bullet (:133), minor-additions bullet (:51), against `skills/spec-cycle/SKILL.md:542-553`
**Edge case:** The operator picks halt option 4 and the grill settles a remaining P0/P1 as "this is a follow-up ticket, not a fold" — the single most likely outcome for the findings this ticket exists to route, since option 4 is the sanctioned late-round judgment step.
**What happens:** Routing is the only thing that creates a row, and it is switched off inside 2f-i step 4. The decision is therefore "applied as written" as an in-place spec edit with no defined shape — an ad-hoc note that no render, no reviewer, and no next-invocation suppression rule reads — or it falls into 2f-i's `deferred to option 3` bucket, which is defined for "narrow the brief"-class decisions and leaves the finding P0/P1. Step 5 then re-renders "the 2f halt block again", which per Design 5 now carries the follow-up report — and the operator sees a report that omits the deferral they just settled. That is a silently dropped follow-up, the failure mode § Design 6 exists to name. It degrades rather than breaks, hence P2.
**Why the spec misses it:** The exemption was written to stop routing from second-guessing an operator decision (a good rule), without asking what happens when the operator's decision *is* a deferral.
**Suggested fix:** One sentence beside the exemption: "Routing's tests do not run inside 2f-i step 4 — a Settled decision is applied as written. A Settled decision that dispositions a finding as a follow-up is discharged by appending a row to `## Deferred — follow-up required` in the shape above (`Deferred in: round 4 (grill)`), which is the round-4 append carve-out; step 5's re-render then shows it."

### F-8: No checklist row asserts that the block's substance reaches the four agents
**Severity:** P3
**Where:** spec § Test plan row 6 (:161), § Design 7 item 2 (:146)
**Edge case:** A partial or paraphrased insertion of the Deferred-findings block into one of the four files.
**What happens:** Row 6 asserts the block's opening literal and a bare `DEFERRED` token, plus byte-identity across the four. Byte-identity catches divergence but not a uniformly wrong block: the preamble check, the in-scope-P0 carve-out, the re-anchor allowance and the "reported once" rule could all be dropped in all four files and every assertion still passes. Given that the whole feature is inert without the block (§ Design 6), the gate is thin.
**Suggested fix:** Add to row 6: `grep -cF 'routing violation: missing preamble' agents/spec-reviewer-*.md` → 1 per file and `grep -cF 'unless the candidate is an in-scope P0' agents/spec-reviewer-*.md` → 1 per file.

### F-9: `(re-anchored round <n>)` is appended field-level by the producer and read site-level by the consumer
**Severity:** P3
**Where:** spec § Design 2 R2 clause (b) (:98) vs § Design 7 block (:146)
**Edge case:** A `Propagation sites` field listing three sites, one of which is re-anchored.
**What happens:** R2 says to append the marker "to the field", which puts one suffix at the end of a semicolon-separated list; the block reads it per-site — "a **site** suffixed `(re-anchored round <n>)` is checked against the new heading it names". With three sites and one trailing marker the reviewer cannot tell which site was re-anchored, and may check the wrong one or read the marker as applying to all. Cosmetic in effect; it only matters when a re-anchor and a stale site coexist.
**Suggested fix:** Say "appending `(re-anchored round <n>)` to the re-anchored site, not to the field" in R2.

## Summary
P0: 0 | P1: 3 | P2: 4 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=3 P2=4 P3=2 P4=0
