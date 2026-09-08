# Conventions Review — round 4

## Closure of round 3 findings

Round-4 protocol note: the rewrite's FROZEN/REWRITE discipline was followed as `SKILL.md:442-445` requires — the two FROZEN sections edited (§ Scope, § Design 4) are named as explicit one-clause promotions in the closure manifest, not silently touched.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | D16 vs Design 3 on re-run recount | CLOSED | spec:49 — "On a re-run there is no in-context fold record, so the recount does not run at all"; matches Design 3's opening (spec:107) |
| correctness | F-2 | Input-line clause points at text lacking the revert rule | CLOSED | spec:144 now cites the block only; spec:148 carries "A manifest line whose finding id is round-qualified … verify it against the row it cites" |
| correctness | F-3 | R4 halt omits `## Test command` | CLOSED | spec:101 lists it between `## Test plan` and `## Done when`; matches `SKILL.md:300-307` (verified) |
| correctness | F-4 | "exactly one line" miscited at `:369-371` | CLOSED | spec:121 cites `:370-371` and `:378-379`; verified against `SKILL.md` (370-371 = P0/P1-only, 378-379 = exactly-one-line) |
| correctness | F-5 | Removal/merge has no mechanism; two-site floor | CLOSED | spec:99 adds `(removed round <n>)`, marker per entry, floor waiver; spec:148 floor is "two or more **entries**" |
| correctness | F-6 | `Suggested fix (verbatim):` label mismatch | CLOSED | spec:89 label is `**Suggested fix:**`; "verbatim" moved into the value hint |
| correctness | F-7 | Row 10 pins unmandated literal | CLOSED | spec:21 quotes the sentence verbatim in the Scope row |
| correctness | F-8 | Row 5 exact count 8 | CLOSED | spec:162 → "8 or 9" with rationale |
| correctness | F-9 | Revert-supersession stated in wrong branch; match key unstated | CLOSED | spec:74 (round-4 paragraph) — "an entry whose `finding_id` matches the `Finding:` field … is superseded" |
| edge-cases | F-1 | Round-4 FROZEN makes a routing-violation P0 unrepairable | CLOSED | spec:48 (D15) + spec:74 — section governed by R2, unresolved-P0/P1 test does not apply, no promotion needed |
| edge-cases | F-2 | Preamble check has no textual key in the agents | CLOSED | spec:148 — "first non-blank content … must be a blockquote containing the sentence …" (residue → F-3 below) |
| edge-cases | F-3 | Markdown inside verbatim `Suggested fix` truncates the section | CLOSED | spec:89 (`> `-prefixed blockquote), spec:78 + spec:133 (extent = next `##` not inside a blockquote), spec:148 mirrors both |
| edge-cases | F-4 | Duplicate section undefined | CLOSED | spec:103 (R6, merge-into-first) + spec:148 `routing violation: duplicate section` |
| edge-cases | F-5 | Row 5 `→ 8` falsified by a wrap | CLOSED | spec:162 |
| edge-cases | F-6 | Removal with no successor; no repair | CLOSED | spec:99 `(removed round <n>)`; spec:148 waiver clause |
| edge-cases | F-7 | Settled grill deferral has no landing place | CLOSED | spec:70 — discharged by appending a row with `Deferred in: round 4 (grill)` (attribution residue → F-1 below) |
| edge-cases | F-8 | No row asserts the block's substance reaches the agents | CLOSED | spec:163 — four per-file `grep -cF` assertions added |
| edge-cases | F-9 | Marker appended field-level, read site-level | CLOSED | spec:99 — "the marker goes on that entry, not on the field" |
| conventions | F-1 | Row 8's `Follow-up: unfiled` assertion falsified by the row shape | CLOSED | spec:165 — `**Follow-up:** unfiled` → 1 and `— Follow-up: unfiled` → 1; both literals verified against spec:93 and spec:129 |
| conventions | F-2 | D15 append-only vs R2's repair/re-anchor at round 4 | CLOSED | spec:48 + spec:74 enumerate the permitted round-4 edits identically |
| conventions | F-3 | Rows 5 and 9 assert wrap-sensitive counts/phrases | **PARTIAL** | Row 5 fixed (spec:162). Row 9 (spec:166) replaced one six-word phrase with two more multi-word literals, both landing in hard-wrapped regions — see F-2 below. Keeps P2. |
| conventions | F-4 | Row 10 pins a literal no Design mandates | CLOSED | spec:21 |
| conventions | F-5 | "end of the spec" ×3 with no section terminator | CLOSED | spec:78 + spec:133 define the extent identically |
| conventions | F-6 | "immediately under the heading" invites a false preamble P0 | CLOSED | spec:148 — "first non-blank content under the heading" (residue → F-3 below) |

## Findings

### F-1: `## Deferred — follow-up required`'s append is attributed to rule R2 three times, but R2 grants only edits to *existing* rows
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:99 (R2) vs spec.md:48 (D15), spec.md:70 (Design 1, grill clause), spec.md:74 (Design 1 "Round 4")
**Convention violated:** The producer/consumer pairing D11 states as this spec's own discipline ("the seven field labels … appear once in 2e (producer) and once per agent"), and the same defect class round-3 correctness/F-2 raised — a cross-reference naming a rule that does not carry the content attributed to it.
**Evidence:** R2's operative sentence is scoped to existing rows: "The only edits the skill makes to an **existing row** are (a) repairing the field a `routing violation: D-<n>` finding names, or inserting a missing preamble, and (b) re-anchoring an entry…". Appending a new row is granted elsewhere — Design 1 step 4, "Defer: add a row to `## Deferred — follow-up required`" (spec:68). But three other passages attribute the append to R2:
- spec:48 — "the edits permitted at round 4 are exactly R2's — **appending a row routed this round** …";
- spec:70 — "discharged by appending a row in the shape below with `Deferred in: round 4 (grill)` — **rule R2's append**";
- spec:74 — "**R2's edits — appending a row routed this round**, repairing …, inserting a missing preamble, re-anchoring — are permitted here without promotion."

This ships into SKILL.md. A round-4 author who follows the pointer ("permitted edits are exactly R2's") and reads R2 finds three edits, none of them an append — which contradicts the very grill-discharge path spec:70 defines and would re-open round-3 edge-cases/F-7. The inline enumerations at spec:48 and :74 are what actually rescue the reader, so this is an attribution defect rather than a functional gap — P2, same call round-3 correctness/F-2 got for the identical shape.
**Suggested fix:** One clause on R2 (spec:99), before the existing-row sentence: "The skill appends a new row when routing defers a finding (Design 1 step 4) or when a Settled grill decision dispositions one as a follow-up. The only edits it makes to an *existing* row are (a) … and (b) …." No other text needs to change; spec:48/:70/:74 then cite a rule that contains what they claim.

### F-2: Checklist row 9 re-pins multi-word literals in the two hard-wrapped regions this spec edits — the exact trade round-3 conventions/F-3 asked it to stop making
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:166 (§ Test plan row 9), against spec.md:156 (the Test plan preamble) and spec.md:163, :165 (rows 6, 8)
**Convention violated:** MEMORY `project_prose_spec_gate_script_pitfalls` — "assert hunk regions not counts … re-verify backtick phrases with `grep -cF`" — restated by the spec's own preamble ("Assert hunk regions, not counts"; "the file is hard-wrapped in places and a phrase can straddle a line break"). Round-3 conventions/F-3 flagged rows 5 and 9; row 5 was fixed and row 9 was rewritten to carry *two* phrase assertions instead of one.
**Evidence:** Row 9 asserts `grep -cF 'deferred: D-<n> (§ Deferred — follow-up required)' skills/spec-cycle/SKILL.md` **≥ 2 (2b prose, 2e step 4)** and `grep -cF 'governed by rule R2' … ` ≥ 1 (the D15 passage in the round-4 half). Measured line widths in the target regions:

```
2b prose (:370-383)        68–73 cols, every line
round-4 half (:435-464)    72–78 cols, every line
2e bullets (:429-432)      25 / 34 / 229 / 132 cols  (unwrapped)
```

The first literal is 46 characters. Its 2e occurrence is safe (that region is unwrapped), but its 2b occurrence lands in the disposition-phrase list at `:380-383`, which is hard-wrapped at ~72 columns — a 46-char run appended to a phrase list there will straddle a break unless the implementer knows not to let it, and the row's `≥ 2` requires *both* occurrences to match. `governed by rule R2` (19 chars) sits in a ~76-column wrapped region with a comparable exposure. Round-3's suggested fix — "assert an unwrappable token instead" — was applied to row 5 and not to row 9. The same exposure exists in rows 6 and 8 (`must not implement anything in this section`, 44 chars, asserted per agent file).
**Suggested fix:** Add one sentence to the Test plan preamble (spec:156), which fixes rows 6, 8 and 9 at once and costs nothing to verify: "Every literal a checklist row greps must be written on a single line in the target file — do not wrap a line that carries one; if the surrounding prose is hard-wrapped, the literal starts a new line." Alternatively narrow row 9's second assertion to `grep -cF 'rule R2'` and drop the `≥ 2` on the first in favour of row 4's hunk-region assertion.

### F-3: The preamble's textual key differs from the preamble the spec ships, so the byte-key the block was given still needs a substance read
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:148 (§ Design 7 block) vs spec.md:83 (§ Design 2 preamble); spec.md:163, :165 (rows 6, 8)
**Convention violated:** The align-the-label discipline this spec applied one round ago to the identical shape — round-3 correctness/F-6, closed by making producer and consumer name the field `Suggested fix` byte-for-byte. Round-3 edge-cases/F-2 asked for a textual key precisely so the check stops being a paraphrase judgment.
**Evidence:** The shipped preamble (spec:83) reads `` … Not part of this spec's implementation: `/ship-spec` must not implement anything in this section. …`` — with `/ship-spec` in inline code. The consumer key (spec:148) is "a blockquote containing the sentence `` `/ship-spec must not implement anything in this section` ``" — the whole sentence in inline code, `/ship-spec` unbackticked. As literal strings the two do not contain one another; the longest shared run is `must not implement anything in this section`, which is exactly what checklist rows 6 and 8 grep. So the spec's own gate already uses the correct sub-phrase while the rule the reviewers execute uses one the conformant preamble does not carry. A reviewer reading for substance passes it, which is why this is P2 and not higher — but "check for the sentence" was adopted specifically to remove that judgment call, and the only failure mode on the wrong side is a false `routing violation: missing preamble` P0 filed by all four lenses on a well-formed spec.
**Suggested fix:** Make the key the same run the checklist already greps: in spec:148, "must be a blockquote carrying the sentence `must not implement anything in this section` (the preamble names `/ship-spec` as the actor); if it is absent or the blockquote lacks that sentence, file a P0 titled `routing violation: missing preamble`."

### F-4: Two load-bearing spec-level additions from this round are absent from the "minor additions" roll-up the drift-check reads
**Severity:** P3
**Where:** spec.md:51 (§ Decisions, "Minor additions, recorded so the drift-check can see them") vs spec.md:78, :89, :133, :148
**Convention violated:** `docs/spec-workflow-reference.md:77` and `AGENTS.md` § Parallel review agents — the conventions lens classifies every decision as brief-authorized, ticket-authorized, spec-addition-with-rationale, or silent addition — and this spec's own stated practice of recording additions in one place so the Phase 3 drift-check can see them.
**Evidence:** The roll-up records eight items (`D-<n>` allocation, no GC, `(none)` render, site disputes, the `routing violation:` title prefix, the 2f-i exemption, advisory halt-and-narrow, round-4 title suffixes, R6). Two constructs added this round are not among them, and neither is in the brief:
- the **section-extent grammar** — "runs from its heading to the next `##` heading that is not inside a blockquote, or to end of file. A line prefixed `> ` is never a heading and never a row" (spec:78, restated at :133 and :148);
- the **`Suggested fix` escaping rule** — the field is stored as a `> `-prefixed blockquote rather than the reviewer's raw text (spec:89).

Both are (c)-class — they exist for a stated reason (round-3 edge-cases/F-3 and conventions/F-5) and the rationale is recoverable from the reviews — so nothing here is wrong. But the drift-check reads the spec, not the review directory, and these are the two rules that decide what a downstream reader parses as a row.
**Suggested fix:** Two clauses appended to spec:51: "the section's extent is defined by grammar (heading → next `##` not inside a blockquote) rather than by position, so a copied heading inside a row cannot end it; a deferred `Suggested fix` is stored `> `-prefixed rather than raw, which is the one place a reviewer's text is transformed on the way into the spec."

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
