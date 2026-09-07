# Edge-Cases Review — round 4 (delta re-check)

_Operator-requested at the post-round-4 halt (off-menu: "patch and review the delta"). Scoped to closure of round-4 edge-cases F-1 and the round-4 targeted rewrite's other edits. Not a round 5; the round counter stays at 4._

Grounding: read the spec fresh from disk, my round-4 report, and the live targets — `skills/spec-cycle/SKILL.md:490–568` and `:694–706`, `skills/spec-brief/SKILL.md:134–145`, `skills/grilling/SKILL.md:59–66`, `docs/spec-workflow-reference.md:18–36`, and the `docs/` tree. Delta-scoped: I did not re-walk the whole spec.

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | "The code block replaces `:548–549`" deletes step 5's heading and the `Print` verb | **CLOSED** | spec § Design 5 `:336–340` — "The code block replaces `:549` only — step 5's `5. **Re-render.** Print` lead-in at `:548` and its `, then the 2f halt block again …` continuation at `:550–554` are unchanged, and the line stays an inline code span on its own physical line, as today." Verified executable against the live file: `:548` is the step marker + verb, `:549` is the sole inline-code-span line, `:550–554` is the continuation. With `:549` alone replaced, step 5 survives as a step, so the three cross-references still resolve — `:503–504` ("list them in step 5 as `not grillable: …`"), `:544` ("report it in step 5 as `deferred to option 3: …`"), and `:702` ("the step 5 `not grillable <ids>` line is their only record"; the new line still contains `not grillable <ids>`). The halt-block re-render at `:550–552` keeps its verb and the ` — grilled (spec edited; not re-reviewed)` suffix. Row 10 `:493` now also asserts step 5 "still begins `5. **Re-render.** Print`", so the gate catches a regression. |

No REOPENED items. Delta walk of the other rewritten sites found no new P0/P1:

- **§ Scope / row 14 (`docs/` outside `docs/specs/`)** — `docs/` holds exactly six top-level files; the narrowed predicate still fences all five non-target ones, and row 14's separate `docs/specs/DONE/` clause preserves D7 / Out-of-scope 5. Closes round-4 F-6 without unfencing VHS-32.
- **§ Decisions roll-up (`unknown` bullet, "no empty-section sentinel")** — the `unknown` rationale is accurate: step 3's live guard (`:518–522`) tests only for `empty-seed` and a `## Grill summary` line, never for `exit:`.
- **§ Design 4 closing clause** — "This rule governs rendered rounds; the hand-off block is rendered exactly as its contract states." adds no numeric bound and no preamble slot, so row 8 remains satisfiable as written.
- **§ Design 5 both-lists rationale** ("while anything about it is still open") — closes F-7; row 10's "print `unknown`" assertion matches the shipped bullet string verbatim.
- **§ Design 6 "1 rounds"** — consistent with `spec-brief:143`'s `Interview: <n> rounds` template and the roll-up's `rounds: 1/<round_cap>`.
- **§ Design 7 `:23`** — "anything the operator deferred is still in the brief's open items" is correct against `grilling:63` (defer ⇒ one named Open item plus one rolled-up item) and `spec-brief:140`. Row 13 stays satisfiable: `docs/spec-workflow-reference.md` is unwrapped (one paragraph per line), the new `:23` contains "altitude fence" twice, "either way the reason line says which", and `fence-empty`, and `:35` is a separate single line.
- **§ Risks 2 / 3** — the Scope-rows clause matches `spec-brief:141` (`Current` from a grounding fact, `Change` from a settled decision ⇒ empty here); the suffix sentence matches live `:550–551`.

## Findings

### F-1: The test-plan preamble's `tr '\n' ' '` does not collapse the 3-space continuation indent, so a row-10 phrase that wraps inside step 5 fails the gate on correct text
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan preamble, `:430–436`; § Test plan row 10, `:485–495`
**Edge case:** Any asserted phrase in the new step-5 bullets straddles a wrap boundary in the hard-wrapped file.
**What happens:** `tr '\n' ' '` replaces the newline with one space but leaves the continuation line's leading indent, so "under\n     `dispositioned`" collapses to `under      \`dispositioned\`` — six spaces where the literal grep expects one. The preamble's own worked example ("never edits the brief", `:557–558`) happens to be *unindented* closing-paragraph text and so collapses cleanly; every phrase row 10 asserts inside step 5 ("is listed here rather than under `dispositioned`", "in seed order", "print `unknown`", "not the full red list", "5. **Re-render.** Print") sits under a 3-space list indent and does not. Failure direction is safe (blocks a correct PR rather than passing a wrong one), which keeps it below P1, but the checklist *is* the `/ship-spec` gate here — `## Test command` is `N/A`.
**Why the spec misses it:** The note was written from the one pre-edit example the author checked, which lives outside a list item.
**Suggested fix:** One word in the preamble: `(tr -s '[:space:]' ' '` before grepping, so wrapped continuation indents collapse too)`. No row changes.

### F-2: "The bullets below are added to step 5 in the file" ships two spec-relative bullets into `spec-cycle/SKILL.md`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 5, `:340` and the bullet list `:342–364`
**Edge case:** The implementer follows the new positional instruction literally — which is what it exists for, and what round-3 correctness/F-4 asked for.
**What happens:** Four bullets are shipped-rule text, but `not grillable is unchanged.` (`:355`) says nothing to a reader of the skill file (unchanged from *what*?), and two others carry spec-relative tails: "as today" (`:354`) and "Nothing else in 2f-i changes for this exit: …" (`:363–364`). Shipped verbatim they are prose noise in a prompt the model reads each halt; read as spec commentary they are silently dropped. Neither breaks 2f-i, and row 10 asserts none of these strings, so the gate is indifferent — hence P2. But it is the residue of the same "which text ships" root that round 3 opened and the round-4 fix half-closed.
**Why the spec misses it:** The bullet list was written as design exposition, then promoted to shipped text by a positional instruction added afterwards.
**Suggested fix:** In the sentence already being written, name the exception: "The bullets below are added to step 5 in the file, immediately after `:554`, except the `not grillable` bullet and the `Nothing else in 2f-i changes` sentence, which are spec-level notes; drop 'as today' from the `deferred to option 3` bullet when shipping it."

### F-3: The trailing comma that ends live `:549` is attributed to the `:550–554` continuation, so a literal replacement drops it
**Severity:** P4
**Where:** spec § Design 5, `:336–339`, against `skills/spec-cycle/SKILL.md:549–550`
**Edge case:** Implementer replaces `:549` with the code block's contents exactly.
**What happens:** Live `:549` ends `…/grill.md\`,` — the comma is on `:549`, not on `:550` (which begins "then the 2f halt block again"). The spec quotes the continuation as "`, then the 2f halt block again …`" and declares `:550–554` unchanged, so the comma belongs to a region nobody edits and can vanish; the sentence then reads "Print `<line>` / then the 2f halt block…". Purely cosmetic — "as today" arguably covers it, and no gate row checks punctuation.
**Why the spec misses it:** The wording was taken verbatim from the round-4 suggested fix, which quoted the comma with the continuation for readability.
**Suggested fix:** "…on its own physical line, keeping its trailing comma, as today."

### F-4: The Deferred preamble's "applied but not re-reviewed" is stale once this delta re-check lands
**Severity:** P4
**Where:** spec § Deferred (P2+), `:619–621`
**What happens:** The line reads "The round-4 edge-cases P1 (F-1, the `:548–549` → `:549` correction in Design 5) is applied but **not re-reviewed** — there is no round 5." That was true at the halt; after this operator-requested delta re-check the shipped artifact understates its own verification, and `/spec-close` reconciles against this section.
**Suggested fix:** "…is applied and confirmed by a delta re-check of Design 5 (edge-cases, post-round-4); there is no round 5."

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 0 | P4: 2

STATUS: GREEN
