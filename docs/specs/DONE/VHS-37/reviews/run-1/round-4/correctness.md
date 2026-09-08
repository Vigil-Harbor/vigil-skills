# Correctness Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | D16 vs Design 3 on re-run recount (P1) | CLOSED | spec:49 now reads "On a re-run there is no in-context fold record, so the recount does not run at all and the new finding is routed by Design 1 with no recount suffix"; Design 3's opening (spec:107) and "Otherwise" bullet (spec:111) agree |
| correctness | F-2 | Input-line clause pointed at nothing (P2) | CLOSED | spec:144 clause now cites only the Deferred-findings block; the block (spec:148) carries D13's round-qualified-revert sentence verbatim |
| correctness | F-3 | R4 omits `## Test command` (P2) | CLOSED | spec:101 list now `## Goal, ## Scope, ## Design, ## Test plan, ## Test command, ## Done when, ## Out of scope` — matches `skills/spec-cycle/SKILL.md:300-307` |
| correctness | F-4 | "exactly one line" mis-anchored (P2) | CLOSED | spec:121 now cites `:370-371` for "P0/P1 findings only" and `:378-379` for "Map each … exactly one line". Verified: SKILL.md:370-371 and :378-379 |
| correctness | F-5 | Removed/merged site had no mechanism; floor unsatisfiable (P2) | CLOSED | R2 (spec:99) adds `(removed round <n>)`; block (spec:148) floor is now "two or more **entries**" and waives the existing-site test on any marker |
| correctness | F-6 | `Suggested fix (verbatim):` label skew (P3) | CLOSED | shape spec:89 label is `**Suggested fix:**`; "verbatim" moved into the value hint |
| correctness | F-7 | Row 10 literal unspecified by any Design (P3) | CLOSED | Scope row spec:21 pins the sentence verbatim, containing "In every round, including round 1" |
| correctness | F-8 | Row 5 exact count of 8 (P3) | CLOSED | spec:162 → "8 or 9 after (7 before)". Baseline verified: `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → 7 |
| correctness | F-9 | Supersession stated in wrong branch; match key unstated (P2) | CLOSED | Design 1 Round-4 (spec:74) carries it in the round-4 branch and pins the key (`finding_id` ↔ row `Finding:`); verified against SKILL.md:453, :460 |
| edge-cases | F-1 | Round-4 routing-violation P0 unrepairable; D15 contradicts FROZEN (P1) | **PARTIAL** | Field-repair, preamble-insert and re-anchor are now carved out (spec:48, :74). The **duplicate-section** violation class added this round (R6, spec:103; block, spec:148) is not in the carve-out — see F-1 below |
| edge-cases | F-2 | Preamble check had no textual referent (P1) | CLOSED | block spec:148 now names the sentence and titles the P0 `routing violation: missing preamble`; row 6 (spec:163) asserts it per agent file. Residual byte-level skew filed fresh as F-2 below |
| edge-cases | F-3 | Verbatim `Suggested fix` truncates/invents rows (P1) | CLOSED | shape spec:89-90 makes it a `> `-prefixed blockquote; extent defined identically in Design 2 (spec:78), Design 5 (spec:133) and the block (spec:148) |
| edge-cases | F-4 | Duplicate section undefined (P2) | CLOSED | R6 (spec:103) + block's `routing violation: duplicate section`. Its round-4 interaction is F-1 below |
| edge-cases | F-5 | Row 5 exact `→ 8` (P2) | CLOSED | spec:162 |
| edge-cases | F-6 | Removal with no successor (P2) | CLOSED | R2 (spec:99) `(removed round <n>)`; block waiver (spec:148) |
| edge-cases | F-7 | Settled grill deferral has no landing place (P2) | CLOSED | Design 1 (spec:70) — append with `Deferred in: round 4 (grill)`; 2f-i step 5 re-render verified at SKILL.md:555-557 |
| edge-cases | F-8 | No row asserts the block's substance (P3) | CLOSED | row 6 (spec:163) adds three per-file literal assertions. Baseline `grep -c 'DEFERRED' agents/spec-reviewer-*.md` → 0 in all four, as claimed |
| edge-cases | F-9 | Marker field-level vs site-level (P3) | CLOSED | R2 spec:99 — "the marker goes on that entry, not on the field" |
| conventions | F-1 | Row 8 `Follow-up: unfiled` falsified by row shape (P1) | CLOSED | spec:165 asserts `**Follow-up:** unfiled` → 1 (shape, spec:93) and `— Follow-up: unfiled` → 1 (render, spec:129); both verified against the spec's own text |
| conventions | F-2 | D15 vs R2 contradictory mandates at round 4 (P2) | **PARTIAL** | R2's edits are now explicitly permitted at round 4 (spec:48, :74). R6's merge is still outside the enumeration — F-1 below |
| conventions | F-3 | Rows 5/9 wrap-sensitive (P2) | **PARTIAL** | Row 5 closed. Row 9's literal went from a 6-word to a 4-word plain-prose phrase in the hard-wrapped round-4 region; rows 6 and 8 add more. See F-3 below |
| conventions | F-4 | Row 10 pins an unspecified literal (P3) | CLOSED | Scope row spec:21 quotes the sentence verbatim |
| conventions | F-5 | "end of the spec"; no section terminator (P3) | CLOSED | extent pinned identically in Design 2/5/7 |
| conventions | F-6 | "immediately under the heading" literalism (P4) | **PARTIAL** | "first non-blank content under the heading" adopted (spec:148); the "substance, not byte-equality" half was not — F-2 below |

Grounding notes: `git log` shows `ecdfefe`, `c97d4ad` (2026-09-07, `skills/spec-cycle/SKILL.md`) and `ea5c2b0`, `c97d4ad` (2026-09-07, `docs/spec-workflow-reference.md`) inside the 7-day window. The spec already surfaces the two SKILL.md commits (spec:11). I verified the reference-doc hunks landed at `:23`, `:31`, `:35` with no net line change, so `:84` and `:88` are still accurate. Plane VHS-37 retrieved from the `skills` namespace; its description matches the brief, and its narrower title test ("out-of-scope") is superseded by the brief's Decision 2 with rationale, which the spec carries.

## Findings

### F-1: At round 4 the permitted-edit enumeration excludes R6's merge, so a `routing violation: duplicate section` has no repair — and R6 says the opposite
**Severity:** P1
**Where:** spec § Decisions D15 (spec.md:48), § Design 1 "Round 4" (spec.md:74), § Design 2 rule R6 (spec.md:103), § Design 7 block (spec.md:148)

**Claim:** D15 — "its contents are governed by rule R2 in every round, so **the edits permitted at round 4 are exactly R2's** — appending a row routed this round …, repairing the field a routing violation names, inserting a missing preamble, and re-anchoring — none of which is a FROZEN edit or needs promotion."

R6 — "If more than one `## Deferred — follow-up required` heading is present, the first is authoritative: the author merges the later sections into it **in the same round**, renumbering colliding `D-<n>` ids …"

Block — "If the heading appears more than once, file a P0 titled `routing violation: duplicate section`."

**Why this is wrong:** Three of the four permitted round-4 edits map to a repair the block can demand; the fourth violation class the block defines — a duplicate heading — maps to none of them. R2's repair (a) is scoped to "the field a `routing violation: D-<n>` finding names"; a duplicate-section violation names no field and is not `D-<n>`-shaped. Merging is a section-level operation R2 does not define — R2 opens "The only edits the skill makes to an **existing row**" (spec:99). So under D15's exhaustive "exactly R2's", the round-4 author must not merge; under R6's unqualified "in the same round", they must. Two shipped rules, opposite answers, same input.

The untouched round-4 protocol closes the escape: `skills/spec-cycle/SKILL.md:438-439` says a FROZEN section is "Copy the section verbatim from the current spec. Do not touch", and D15 removes the promotion path outright ("the classification rule's 'unresolved P0/P1' test does not apply to it"), so the section can never be classified REWRITE. Anything not in the enumeration is forbidden.

The consequence is not only a stalled repair. D15 permits appending a round-4-routed row, and R1 allocates `D-<n>` "from the highest number already in **the section**" (spec:98) — with two sections present and no merge, "the section" is ambiguous, so the round-4 append can mint a third colliding id. Every downstream consumer keyed on `D-<n>` then misbehaves: the 2b manifest's `deferred: D-<n>` resolves to two rows, D14 suppression "match on `D-<n>` and the row title" (spec:47) can retire a live finding against the wrong root, and Design 5's render prints one section's rows and silently drops the other's — the exact silently-dropped-follow-up failure § Design 6 exists to name.

Supporting evidence for the same root: both D15 and Design 1's Round-4 mirror attribute "appending a row routed this round" to R2, which contains no append rule at all (the append lives in Design 1 step 4). The enumeration is being sourced from a rule that does not carry two of the four items it lists, which is how the merge fell out.

This is a new variant of the root behind edge-cases/R3/F-1 and conventions/R3/F-2, introduced by the round-4 text that closed them: the carve-out was written against the routing-violation classes that existed in round 3 and not re-walked after R6 added a fifth.

**Suggested fix:** Make the round-4 enumeration cover every violation the block can file, and drop the false attribution to R2. In D15 (spec:48) and its Design 1 "Round 4" mirror (spec:74), replace "the edits permitted at round 4 are exactly R2's" with an explicit list: "the edits permitted at round 4 are: appending a row routed this round (Design 1 step 4, including a row discharging a Settled grill decision), R2's two row edits — repairing the field a `routing violation: D-<n>` names, and re-anchoring — inserting a missing preamble, and R6's merge of a duplicate section; none is a FROZEN edit and none needs promotion." Optionally add a round qualifier to R6 pointing at the same list so the two rules cannot drift again. Extend checklist row 9 to grep whatever unwrappable token the final wording carries (see F-3).

### F-2: The block's textual key for the preamble does not occur in the preamble the spec prescribes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 preamble (spec.md:83) vs § Design 7 block (spec.md:148)

**Claim:** Design 2's preamble ships as: `> Known, unfixed P0/P1 findings. Not part of this spec's implementation: `/ship-spec` must not implement anything in this section. Each row becomes a follow-up ticket filed by the operator.`

The block ships as: "the first non-blank content under the heading must be a blockquote containing **the sentence** `/ship-spec must not implement anything in this section`; if it is absent or lacks that sentence, file a P0 titled `routing violation: missing preamble`."

**Why this is wrong:** The producer writes the tool name inside a code span — `` `/ship-spec` must not implement … `` — while the consumer's key is the same words with no internal code span. As a fixed string the key does not occur in the text it keys on. The closure manifest states edge-cases/R3/F-2 was closed by making the block "carry the sentence … as the textual key", but the key and the text differ by exactly the markdown the spec itself inserts.

A reviewer applying the rule literally files `routing violation: missing preamble` as a P0 against every conforming spec, every round, in every lens that runs the block — a self-inflicted gate block on the feature's own happy path. A reviewer applying it by substance passes. Nothing in the block says which reading governs; conventions/R3/F-6 flagged exactly this ambiguity ("unstated whether the check is on exact text or on presence") and the round-4 rewrite adopted its "first non-blank content" clause but not its "substance, not byte-equality" clause. This is also the marker-skew class conventions/R3/F-1 was P1 for, and the repo's recorded pitfall for it (MEMORY `project_prose_spec_gate_script_pitfalls` — "re-verify backtick phrases with `grep -cF`") applies to a prose key as much as to a grep.

It stays P2 rather than P1 because the checklist rows were written around the hazard — row 8 and row 6 both grep the backtick-free tail `must not implement anything in this section`, which matches both forms — so the gate script passes either way and the design intent is recoverable.

**Suggested fix:** Pick one form and use it in both places. Simplest: drop the inner code span from the preamble at spec:83 so it reads `… Not part of this spec's implementation: /ship-spec must not implement anything in this section. …`, making the block's key a true substring. Alternatively, keep the code span and rewrite the block's rule as "… must be a blockquote whose text carries the substance of the sentence *`/ship-spec` must not implement anything in this section* (markdown emphasis on the tool name is immaterial); a section with no blockquote at all, or one that omits this instruction, is the violation."

### F-3: Checklist rows 6, 8 and 9 pin multi-word plain-prose phrases in exactly the regions of the target files that are hard-wrapped
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan rows 6, 8, 9 (spec.md:163, :165, :166) against § Test plan preamble (spec.md:156)

**Claim:** Preamble — "Where a row greps a short token rather than a phrase, that is deliberate: the file is hard-wrapped in places and a phrase can straddle a line break." Row 9 — "`grep -cF 'governed by rule R2' skills/spec-cycle/SKILL.md` ≥ 1 (the D15 passage in the round-4 half)." Row 6 — "`grep -cF 'must not implement anything in this section'` … ≥ 1" per agent file. Row 8 — the same literal in SKILL.md.

**Why this is wrong:** The preamble states the right rule and rows 6, 8 and 9 do not follow it. Verified wrapping: `skills/spec-cycle/SKILL.md:435-462` — the round-4 half, where Design 1's Round-4 passage lands — is hard-wrapped at roughly 72 columns (`:438-441`, `:442-445`, `:446-462` all break mid-sentence), and so is 2b's prose at `:369-383`. `agents/spec-reviewer-correctness.md:34-40` and the corresponding regions in the edge-cases and conventions agents are wrapped the same way (`agents/spec-reviewer-scalability.md:30` is not, which is a separate hazard for row 6's byte-identity assertion).

`governed by rule R2` is four words of plain prose landing in the one region that is definitely wrapped; `must not implement anything in this section` is seven. A byte-correct implementation that wraps between "governed by" and "rule R2", or anywhere inside the seven-word phrase, yields 0 and fails its own gate — the same trap conventions/R3/F-3 and edge-cases/R3/F-5 raised for row 5, which the spec fixed by loosening the count rather than by removing the phrase dependency. Rows 3 and 9's other literals are inside markdown code spans, which authors do not usually break, so they are materially safer; the plain-prose ones are not.

**Suggested fix:** Convert the three plain-prose assertions to unwrappable tokens or to `grep -z`-style multiline checks, and say which you chose. E.g. row 9: `grep -cF 'rule R2' skills/spec-cycle/SKILL.md` ≥ 1, with row 4's hunk-region assertion as the real protection. Rows 6 and 8: `grep -cF 'implement anything in this' <file>` ≥ 1, or state in the Design 2 / Design 7 text that the preamble sentence and the block's key sentence are each written on a single unwrapped line and add that as the checked invariant.

### F-4: Step 7's REOPENED evidence assumes a routing-violation finding that is never filed when the row is missing entirely
**Severity:** P3
**Where:** spec § Design 7 item 3 (spec.md:150) against the block (spec.md:148)

**Claim:** "A `deferred: D-<n>` disposition is satisfied when row `D-<n>` is well-formed per the Deferred-findings block; mark the finding `DEFERRED`. **Otherwise** mark it REOPENED with the routing-violation finding **already filed by that block** as its evidence — the defect is reported once, not as a second finding."

**Why this is wrong:** "Otherwise" covers two cases, and the block only produces a finding for one of them. The block files `routing violation: D-<n>` for a row that exists but is malformed, and `routing violation: missing preamble` / `duplicate section` for section-level defects. It files nothing when the manifest claims `deferred: D-5` and no `D-5` row exists at all — the most likely shape of a false disposition, since the whole point of the check is to catch a claim the spec does not back. In that case the reviewer is told to cite evidence that was never produced.

The outcome is not wrong — the standing REOPENED rule still makes it a P0 — only the stated evidence pointer is unsatisfiable, which will read as a contradiction to a literal reviewer and invite an invented citation.

**Suggested fix:** Split the "otherwise" in spec:150: "If no row `D-<n>` exists, mark the finding REOPENED and cite the absent row as the evidence. If the row exists but is not well-formed, mark it REOPENED with the `routing violation: D-<n>` finding this block already filed as its evidence — the defect is reported once, not as a second finding."

### F-5: The Phase 1 anchor `:294-296` names the heading and the "Output path" line, not where R4's sentences can land
**Severity:** P3
**Where:** spec § Scope row 1 (spec.md:15), § Design 2 rule R4 (spec.md:101), § Test plan row 4 (spec.md:161)

**Claim:** "`skills/spec-cycle/SKILL.md` Phase 1 opening (`:294-296`) | Two sentences …", "(Two sentences at `:294-296`; …)", and row 4's "hunks fall only in: Phase 1 opening (`:294-296`) …".

**Why this is wrong:** Verified current content: `:294` is the heading `## Phase 1 — Author v1 spec`, `:295` is blank, `:296` is "Output path: `docs/specs/TODO/<TICKET-ID>.spec.md`.", and `:298` begins "Read the brief, the linked Plane ticket …". R4's two sentences are about what Phase 1 does on a re-run, so they land at `:297`-ish — after the output-path line and before the authoring instruction — which is outside the cited span. Row 4 then uses the same span as a hunk-region assertion, so a correct insertion produces a hunk at `+297` that a literal reader scores as out of region.

Low severity because "Phase 1 opening" is an accurate region label and a human running row 4 will accept it; but the spec's other anchors are line-exact, so the inconsistency invites a second-guess.

**Suggested fix:** Widen the anchor to `:294-298` in spec:15, spec:101 and spec:161, and say in R4 where the sentences go: "after the `Output path:` line and before the `Read the brief …` paragraph".

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=2 P4=0
