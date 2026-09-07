# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1. (Attempt 1's four rounds are archived at `docs/specs/TODO/VHS-33.attempt-1/reviews/` and are explicitly not carried forward per brief decisions 11–12; per the orchestrator's instruction, absence of attempt-1 machinery is not treated as a gap.)

Grounding completed: spec and brief read from disk; Plane ticket VHS-33 retrieved from the `skills` namespace (`record_id e96bd119-9e11-44a8-8fe0-08b2f297fc4b`, confidence 1.00) and is consistent with the brief; `CLAUDE.md` read; every cited path:line verified against the working tree; `python lint.py --strict` run (exit 0, 2 `missing-requires` WARNs — `review-pr`, `ship-spec` — confirming checklist row 1's baseline).

## Findings

### F-1: Checklist row 8 is unsatisfiable — it requires "ASD-STE100" and "no digit" in the same paragraph
**Severity:** P0
**Where:** `docs/specs/TODO/VHS-33.spec.md:373-374` (Test plan row 8), against `:239-243` (Design 4)
**Claim:** Row 8: "A paragraph beginning `**Plain language.**` … it contains "first use", "ASD-STE100", and "dictionary is not applied"; **it contains no digit**."
**Why this is wrong:** The paragraph row 8 gates is given verbatim at spec `:239-243`. It contains `ASD-STE100` (digits `1`,`0`,`0`) — which row 8 itself *requires* — and also the token `` `2f-i` `` (digit `2`) and the phrase "one instruction per sentence". No paragraph can satisfy both halves of row 8. This is not cosmetic: spec `:341` states "The checklist is the `/ship-spec` gate because `## Test command` is `N/A`", and `## Test command` is indeed `N/A` (`:399-401`). A gate row that can never pass blocks ship.
**Suggested fix:** Replace `it contains no digit` with the assertion actually intended by Design 4's closing sentence ("That is the whole rule. No sentence count, no preamble slot.") — e.g. `it states no sentence count, word limit, or other numeric bound on round length, and adds no round-preamble slot`.

---

### F-2: "On `fence-empty` every list is empty" contradicts 2f-i's not-grillable rule and destroys the only record of not-grillable findings
**Severity:** P1
**Where:** spec `:277-280` (Design 5, step-5 construction rules)
**Claim:** "On `fence-empty` every list is empty and the line still prints; the findings stay P0/P1 untouched and the menu re-renders with options 1–3 (D5, D6)."
**Why this is wrong:** Not-grillable findings are excluded from the seed *before* the primitive is invoked, so the exit token has no bearing on them. `skills/spec-cycle/SKILL.md:499-505`: "**Not grillable:** a report that is missing or unparseable … Exclude them from the seed and list them in step 5 as `not grillable: <lens>/<id> — reviewer report unavailable; option 1 re-dispatches that lens.`" And `skills/spec-cycle/SKILL.md:700-702`: "Not-grillable findings also stay P0/P1 but are **not** written to `grill.md` … the step 5 `not grillable <ids>` line is **their only record**."

A run with some not-grillable findings plus a grillable remainder that renders nothing at the fence exits `fence-empty` with a non-empty `not grillable` list. An implementer following spec `:277` literally would emit an all-empty line and silently drop the only audit record those findings have. (The spec's own step-5 rules at `:274` say "`not grillable` is unchanged" — `:277` contradicts that four lines later.)
**Suggested fix:** Rewrite `:277-278` as: "On `fence-empty` the `dispositioned`, `left open`, and `deferred to option 3` lists are empty and `unreferenced decisions applied` is omitted; `not grillable` is unaffected — those findings never entered the seed. The line still prints; …"

---

### F-3: Design 1's "Descent" and "Rendering" rules have no landing site in `skills/grilling/SKILL.md`, so the omit-when-no-ids guarantee never ships
**Severity:** P1
**Where:** spec `:155-163` (Design 1), against `:369-371` (row 7) and `:405-409` (Done when)
**Claim:** "If no seed item carried an `id`, the field is not rendered anywhere — the block is byte-compatible with v1 for `/spec-brief` and `/grill-me`." (spec `:161-163`); restated at `:187-189`, `:291-292` (Design 6), and `:443-445` (Risk 1).
**Why this is wrong:** Every other design in this spec names its edit site explicitly — `:147` ("**Invocation contract** (`skills/grilling/SKILL.md:18`). The `seed` bullet gains one sentence:"), `:203` ("**Callers-map sentence** (`:134`) becomes:"), `:216`/`:221` ("`:104` becomes:", "`:106` becomes:"), `:235` ("inserted after `:57`"). Design 1's **Descent** (`:155-156`) and **Rendering** (`:158-163`) paragraphs name no site and are not presented as blockquoted replacement text, so on the spec's own convention they are commentary. Checklist row 7 confirms it: it enumerates exactly six `ref:` sites — "seed bullet, four block lines, callers-map sentence" — and `grep -c 'ref:' skills/grilling/SKILL.md` is **0** today, so those six are the complete post-change set. No rendering rule is among them.

The only text that reaches the primitive is the seed-bullet sentence at spec `:150-152` ("echoes back as `ref:` on every Settled and Open item that descends from it. 2f-i passes finding ids; `/spec-brief` and `/grill-me` pass none."), plus a fenced template (spec `:169-182`) that shows `ref:` unconditionally on four lines with `none` as a *legal value* on the Settled line. Faced with a no-id caller, a primitive reading only that text is at least as likely to render `ref: none` as to omit the field. That breaks brief decision 1 ("absent when the caller passed none", brief `:38`), Risk 1's mitigation, and Design 6's "the block it receives has no `ref:` fields" — i.e. `/spec-brief` and `/grill-me` do **not** get v1-byte-compatible output.

The same gap applies to the descent rule: nothing in the shipped file states that a decision descends from its question or that the rolled-up item descends from the deferred question.
**Suggested fix:** State where Descent and Rendering land — e.g. two sentences appended immediately after the hand-off fence (checklist row 9 already permits hunks in `:101–135`, and `:132` can stay byte-identical if they go at `:133`) — and add a checklist assertion for the conditional: `skills/grilling/SKILL.md` contains a sentence stating the `ref:` field is omitted from all four lines when no seed item carried an `id`. Adjust row 7's parenthetical accounting to match (`≥ 6` already permits more sites).

---

### F-4: `skills/spec-cycle/SKILL.md:349` does not contain the closure-manifest `<lens>/<finding-id>` form
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:55-57` (§ Decisions, spec-level additions roll-up) and `:464` (§ References)
**Claim:** "Seed ids are lens-qualified, `<lens>/<finding-id>` (Design 5). Reuse of the form 2b's closure manifest already uses at `skills/spec-cycle/SKILL.md:349`, not a new one".
**Why this is wrong:** `skills/spec-cycle/SKILL.md:349` is `` - `round_number: <N>` `` — a reviewer-prompt parameter. The closure-manifest form is at `skills/spec-cycle/SKILL.md:366`: `` - <lens>/<finding-id> (P<sev>) "<title>" — <how addressed, with spec § anchor> ``, with the example at `:367`. The *substance* of the claim is correct (the form is a reuse, not a new construct) — only the anchor is wrong, and it is the sole evidence backing a declared spec-level addition, which Phase 3's drift-check and `/ship-spec` will re-read.

Related, worth one clause: the file carries two id shapes — two-part `<lens>/<finding-id>` at `:366` and three-part `correctness/R1/F-3` at `:453` (2e's round-4 closed-issues manifest). The spec's choice of the two-part form matches 2f-i's existing `not grillable: <lens>/<id>` at `:504`, but the spec never says which of the two it means.
**Suggested fix:** Change both citations to `skills/spec-cycle/SKILL.md:366`, and add "(the two-part form, as at `:366` and `:504` — not 2e's three-part round-qualified form at `:453`)".

---

### F-5: Four `spec-cycle` / `grilling` edit-site ranges are off by one against the current files
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:25`, `:249`, `:257`, `:286`, `:465-467` (spec-cycle anchors); `:24`, `:167` (grilling hand-off block)
**Claim / Why this is wrong** (all verified at HEAD `7403cb5`):
- Step 1's quoted text — "extract each remaining P0/P1 finding: id, severity, title, body" — is at `skills/spec-cycle/SKILL.md:495-496`. The spec cites `:494–495`; `:494` is the stale-`scalability.md` clause and `:496` (which carries the word "body") is excluded.
- Step 4 begins at `:539` ("4. **Apply.** For each **Settled** item, edit the spec in place…"); `:538` is blank. The spec cites `:538–546`.
- The 2f-i closing paragraph is `:556-561` ("2f-i never re-dispatches reviewers … does not withhold option 4."); `:555` is blank and `:561` is excluded. The spec cites `:555–560` twice (`:286`, `:466`).
- The `grilling` hand-off fenced block content is `:119-129`, with fences at `:118` and `:130`. Design 2 (`:167`) says "The block at `:119–130` becomes:" (includes the closing fence) while the Scope table (`:24`) says `:119–134` (includes the size bound and callers-map sentence, both handled separately). The two cells disagree with each other.

In each case the spec quotes the replaced text verbatim, so an implementer working from the quote lands correctly — but `/ship-spec` re-reads anchors, and checklist row 10's "hunks only inside `:489–561`" is derived from these ranges.
**Suggested fix:** Correct to `:495–496`, `:539–546`, `:556–561`; make Design 2 and the Scope table agree on the hand-off block range (`:118–130` for the fence, `:132` bound and `:134` callers-map cited separately).

---

### F-6: "Omit the clause when `n` is 0" is an undeclared spec-level addition, contradicting the spec's own completeness claim
**Severity:** P2
**Where:** spec `:275-276`, against `:52-70` (§ Decisions roll-up) and `:132-135` (D12)
**Claim:** "`unreferenced decisions applied: <n>` counts Settled items with `ref: none` that step 4 applied. **Omit the clause when `n` is 0.**" — while `:68` says "Nothing else." and `:134` says "The additions roll-up above is the complete list."
**Why this is wrong:** The roll-up declares four additions; the omit-when-zero rule is a fifth and is not listed. Brief decision 12 (`VHS-33.brief.md:49`) names "extra step-5 clauses" among the attempt-1 accretions that are explicitly *not* carried, and brief Risk 1 (`:81`) authorizes only "a decision with zero ids is counted in an `unreferenced decisions applied: <n>` clause. Reviewers did not object to that pin itself; **reuse it, and stop there**." A conditional-omission rule is past "stop there". It also makes the step-5 line's shape variable, which nothing else in the line does (`dispositioned`, `left open`, `not grillable`, `deferred to option 3` all print even when empty — see `skills/spec-cycle/SKILL.md:549`).
**Suggested fix:** Delete the omit rule (print `unreferenced decisions applied: 0`, matching the other always-printed lists), or, if it is wanted, add it to the roll-up at `:62-66` with its one-line justification.

---

### F-7: Scope table says the workflow reference "names six exits"; Design 7's replacement text names none
**Severity:** P2
**Where:** spec `:28` (Scope table, `docs/spec-workflow-reference.md` row) vs `:319-327` (Design 7) and `:391-392` (row 13)
**Claim:** Scope table: "Paraphrase **names six exits**, `ref:`, and F-items (Design 7) | `:23`, `:35`".
**Why this is wrong:** Design 7's verbatim replacement for `docs/spec-workflow-reference.md:23` names five *termination shapes* in prose (emptied frontier, fence-empty, cap hit, operator stop, empty seed) and enumerates no exit tokens; `revised-after-cap (+1 round)` is absent, and the current `:23` (verified) carries no token list either. Checklist row 13 asserts only `fence-empty` ≥ 1 and that `:35` contains `ref:` and "unestablished fact" — consistent with Design 7, not with the Scope table. An implementer reading the Scope table could add a six-token enumeration to `:23`, diverging from the blockquoted text the spec pins.
**Suggested fix:** Change the Scope-table cell to "Paraphrase names the fence-empty shape, `ref:`, and unestablished facts (Design 7)".

---

### F-8: "the same shape `:80` uses" — the cited shape carries a cause qualifier the new F-item shape drops
**Severity:** P3
**Where:** spec `:298-299` (Design 6)
**Claim:** "An `F<n>` item is written as `<fact needed> — not established; spec author pins this` (the same shape `:80` uses for a failed exploration under `--no-grill`)."
**Why this is wrong:** `skills/spec-brief/SKILL.md:80` reads `<fact needed> — not established (exploration failed); spec author pins this` — with a parenthetical cause the new shape deliberately drops (consistent with the roll-up's "no cause qualifiers", spec `:69`). "The same shape" overstates it; it is the same shape *minus* the qualifier.
**Suggested fix:** "(the shape `:80` uses for a failed exploration under `--no-grill`, without its `(exploration failed)` qualifier — see the roll-up's no-cause-qualifiers rule)".

---

### F-9: `grilling:108` still calls abandoned-exploration items "questions" while Design 2 makes them F-items
**Severity:** P3
**Where:** spec `:193-195` (Design 2, the `stopped` value), against `skills/grilling/SKILL.md:108`
**Claim:** The F-item's reason takes "`stopped` (an exploration abandoned at `stop`, per `:108`)".
**Why this is wrong:** `skills/grilling/SKILL.md:108` reads "On `stop` … in-flight explorations are abandoned, and **their questions** are Open with `unresolved because: stopped`." `:108` is neither in the spec's "Files to leave alone" list (`:36-39`) nor in any Design, so it ships unchanged, telling the primitive those items are questions (Q form) while Design 2 says they are F-items. Output is not *wrong* either way — `stopped` is a legal reason on both the Q line and the F line — but the two readings produce different blocks for the same input.
**Suggested fix:** Either name `:108` in "Files to leave alone" with a one-line note that `stopped` is legal on both forms, or add one clause to `:108` ("their fact requests are Open as `F<n>` items with `unresolved because: stopped`"). The latter is a hunk in `:101–135`, which checklist row 9 already permits.

---

### F-10: The rolled-up Open line in the pinned block has no separator before `ref:`
**Severity:** P4
**Where:** spec `:178` (Design 2, hand-off block)
**Claim:** `3. **<parent title> — downstream decisions not explored (deferred at round <n>)** ref: <…>`
**Why this is wrong:** The Settled line (`:173`) and the Open question line (`:176`) both end a sentence before the field (`… ref:` after a period); the F line (`:177`) likewise. The rolled-up line runs `**` straight into ` ref:`. Checklist row 4 pins the block verbatim, so the inconsistency ships.
**Suggested fix:** `… (deferred at round <n>)**. ref: <…>`

---

### F-11: `d381f88` landed today on all five touched files — anchors re-verified, no drift found
**Severity:** P4
**Where:** grounding step 6
**Claim:** spec `:454-455`: "All anchors were read at `7403cb5` on 2026-09-06; `/ship-spec` re-reads."
**Why this is wrong:** Nothing is wrong — surfacing per the grounding contract. `git log -10 --oneline --since="14 days ago"` over the five touched files returns exactly one commit, `d381f88 feat(vhs-32): /spec-brief and the grilling interview primitive (#26)`, i.e. these files were *created* today. I re-verified every anchor at the current working tree; apart from F-4 and F-5 the citations hold, and no in-flight change is competing with this spec.
**Suggested fix:** None.

## Summary
P0: 1 | P1: 2 | P2: 4 | P3: 2 | P4: 2

STATUS: RED P0=1 P1=2 P2=4 P3=2 P4=2
