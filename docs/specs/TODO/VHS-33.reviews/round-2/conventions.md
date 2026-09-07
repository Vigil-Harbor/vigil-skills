# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Checklist row 8 unsatisfiable (ASD-STE100 + "no digit") | CLOSED | spec § Test plan row 8, `:413–414` — last clause now "states no sentence count, word limit, or other numeric bound … adds no round-preamble slot" |
| correctness | F-2 | "On `fence-empty` every list is empty" destroys the not-grillable record | CLOSED | spec § Design 5, `:306–312` — empties only dispositioned / left open / deferred-to-option-3; "`not grillable` is unaffected … this line is their only record" |
| correctness | F-3 | Design 1's Descent/Rendering rules have no landing site | CLOSED | spec § Design 1 `:163–176` — omission sentence inside the `:18` blockquote, new blockquoted `ref:` paragraph after `:130`; Scope `:24`; row 7 `:405–410` |
| correctness | F-4 | `spec-cycle:349` is not the closure-manifest form | CLOSED | spec `:60` now cites `:366` and `:504`; verified at HEAD — `:366` is the manifest line, `:504` the 2f-i `not grillable:` line |
| correctness | F-5 | Four edit-site ranges off by one | CLOSED | spec `:25`, `:278`, `:318` now `:495–496` / `:539–546` / `:556–561`; Scope `:24` and Design 2 `:183` agree on `:118–130`. All four verified at HEAD |
| correctness | F-6 | "Omit the clause when `n` is 0" is an undeclared addition | CLOSED | spec `:305` — "It always prints, `0` included, like the other lists"; rule deleted |
| correctness | F-7 | Scope says reference "names six exits" | CLOSED | spec `:28` now "Paraphrase names the fence-empty shape, `ref:`, and unestablished facts" |
| correctness | F-8 | "same shape `:80` uses" carries a cause qualifier | CLOSED | spec `:330–331` — "without its `(exploration failed)` cause — no cause qualifiers" |
| correctness | F-9 | `grilling:108` still calls abandoned explorations "questions" | CLOSED | spec § Design 3 `:250–253` replaces the clause with "their fact needs are Open `F<n>` items with `unresolved because: stopped`" |
| correctness | F-10 | Rolled-up line has no separator before `ref:` | CLOSED | spec `:194`, `:218`; row 4 pins `)**. ref: <…>` |
| correctness | F-11 | `d381f88` landed today — no action | CLOSED | spec § Deferred `:554–555` |
| edge-cases | F-1 | Row 8 unsatisfiable (digits) | CLOSED | same edit as correctness F-1 |
| edge-cases | F-2 | Two of five F-item causes never render an `F<n>` | CLOSED (see F-2a below) | spec `:212–213` — carries its number from the `F1…Fn` series "whether or not it was ever rendered as an `ℹ️` request". Defensible against the file's own `### Facts established` usage (dispatched facts already carry F-ids). Residual raised below as P2, not a reopen |
| edge-cases | F-3 | `fence-empty` writes a hollow brief | CLOSED as accepted risk | spec § Risks 2, `:498–504` — the exact entry the finding asked for. See my F-3 for the missing prior-decision citation |
| edge-cases | F-4 | `empty-frontier` sentence false for a round-≥2 fence-out | CLOSED | spec `:242–248` — "(a later round's remaining candidates all fell below the fence)" |
| edge-cases | F-5 | Both-lists rule also suppresses `deferred to option 3` | CLOSED | spec `:300–301` — "It still appears under `deferred to option 3` if step 4 could not apply its Settled item" (roll-up wording lags — my F-4) |
| edge-cases | F-6 | `ref:` id matching no seeded finding | CLOSED (deferred) | spec § Deferred `:537–541`, with the rule to adopt |
| edge-cases | F-7 | `left open` empty on `fence-empty` while findings are open | CLOSED | spec `:309–311` — "the empty `left open` is not a claim that nothing is open" |
| edge-cases | F-8 | Unapplied `ref: none` Settled item in no list | CLOSED (deferred) | spec § Deferred `:542–546` |
| edge-cases | F-9 | Row 13 forbids the change Design 7 requires | CLOSED | spec row 13 `:436–438` — "`:23` contains it; … no line other than `:23` and `:35` changes" |
| edge-cases | F-10 | Wrong anchor for the one spec-level addition | CLOSED | same as correctness F-4 |
| edge-cases | F-11 | Phase 3 "revise by Q number" after `fence-empty` | CLOSED | spec § Out of scope item 12, `:489–491` |
| edge-cases | F-12 | `rounds:` on a `fence-empty` header never pinned | CLOSED | spec `:247` — `rounds: 1/<round_cap>`; row 6 asserts it (roll-up gap — my F-2b) |
| edge-cases | F-13 | Three `spec-cycle` anchors off by one | CLOSED | same as correctness F-5 |
| edge-cases | F-14 | `left open` has no de-duplication clause | CLOSED | spec `:298` — "each id once, in seed order" |
| edge-cases | F-15 | `stopped` and `fact not established` flatten to one text | CLOSED (deferred) | spec § Deferred `:547–550` |
| edge-cases | F-16 | Row 16 counts non-content diff lines | CLOSED | spec row 16 `:445–446` — `grep '^+' \| grep -v '^+++'`, "hunk headers and removed lines do not count" |
| edge-cases | F-17 | Two unspecified rendering separators | CLOSED | (a) period before `ref:` (`:218`); (b) the omit-when-zero clause is gone (`:305`) |
| edge-cases | F-18 | `ref:` id character legality | CLOSED (deferred) | spec § Deferred `:551–553` |
| conventions | F-1 | `ref:` omission/descent rules have no landing anchor | CLOSED | same as correctness F-3 |
| conventions | F-2 | Additions roll-up incomplete | PARTIAL | both named items folded (`:74–76`, `:305`), but three round-2 constructs are newly missing — see my F-2 |
| conventions | F-3 | `fact not established` kept for nonexistent consumers | CLOSED | dropped from the Q-item list (`:214–217`), grep evidence carried into the roll-up at `:76`; re-verified at HEAD — only `grilling:74`, `:88`, `:125` |
| conventions | F-4 | Closure-manifest anchor wrong | CLOSED | `:366` + `:504`, `:453` distinguished as "not used" |
| conventions | F-5 | Scope cell promises "six exits" | CLOSED | same as correctness F-7 |
| conventions | F-6 | Two Scope changes with no asserting row | CLOSED | row 7 `:409` asserts "F-items" and "by `ref:`"; row 10 `:424–425` asserts "A `fence-empty` exit is the same shape" |
| conventions | F-7 | Row 10 does not re-assert VHS-32 row 7 | CLOSED | spec row 10 `:425–430` carries all nine strings + the scalability line; verified against `docs/specs/DONE/VHS-32/spec.md:461`. D7 `:121–123` says so |
| conventions | F-8 | Three `spec-cycle` anchors off by one | CLOSED | verified at HEAD |
| conventions | F-9 | "the same shape `:80` uses" | CLOSED | same as correctness F-8 |
| conventions | F-10 | Row 14 omits `README.md` / `AGENTS.md` | CLOSED | Scope `:47–50` and row 14 `:439–442`; I re-verified neither file paraphrases the hand-off block or the exit tokens |

## Findings

### F-1: Checklist row 7's `grep -c 'ref:' ≥ 8` cannot be met by an implementation that follows the file's line convention

**Severity:** P0
**Where:** spec.md:410 (Test plan row 7)
**Convention violated:** `skills/grilling/SKILL.md` is written unwrapped — one line per paragraph or bullet (max line length 649 chars; `:23` is 649, `:70` is 594, `:74` is 447). `grep -c` counts *matching lines*, not occurrences. Also the spec's own gate rule, "`## Test command` is `N/A`; the checklist is the gate" (spec.md:32, :373).
**Evidence:** `grep -c 'ref:' skills/grilling/SKILL.md` is 0 today. The four Designs add `ref:` to exactly seven lines of that file:

1. `:18` seed bullet — one unwrapped line, two occurrences (`echoes back as \`ref:\``, `no \`ref:\` field is rendered at all`)
2. the Settled line in the block
3. the Open question line
4. the new F line
5. the rolled-up line
6. the new `ref:` paragraph after `:130` — one unwrapped paragraph line, two occurrences (`\`ref:\` renders on every…`, `renders \`ref: none\``)
7. `:134` callers-map sentence

That is **7 matching lines**, and 7 is the maximum available — row 7 itself names no eighth site. The arithmetic slip is traceable: round 1 read this row as "`≥ 6` — seed bullet, four block lines, callers-map sentence", which is 6 *line-sites*; adding one paragraph makes 7, but the threshold moved to 8 (counting the paragraph's two occurrences). The row's sibling, row 6, gets this right — it enumerates line-sites explicitly ("≥ 3 (exits list, `:106` paragraph, header)"), and 3 is exactly what the edits produce.

A faithful implementation fails the declared ship gate; an implementer chasing the row adds a spurious eighth `ref:` mention or hard-wraps the new paragraph against the file's convention.
**Suggested fix:** Change `≥ 8` to `≥ 7` and enumerate the sites the way row 6 does — "`grep -c 'ref:' skills/grilling/SKILL.md` ≥ 7 (seed bullet, four block lines, the `ref:` paragraph, the callers-map sentence)". If occurrence-counting was intended, say so explicitly instead: `grep -o 'ref:' skills/grilling/SKILL.md | wc -l` ≥ 9.

---

### F-2: The "Spec-level additions" roll-up is again incomplete against the round-2 Designs

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:54–80 (`## Decisions`, five bullets + "Nothing else"), against Design 2 (`:212–213`), Design 3 (`:247`), and D7 (`:121–123`)
**Convention violated:** Brief decision 12 and the spec's own D12 (`:146`): "The additions roll-up above is the complete list." The roll-up is the artifact `/spec-cycle`'s Phase 3 drift-check reads (spec.md:56–57), so an incomplete one is the failure mode it exists to prevent. This is round 1's conventions F-2 recurring on the constructs added *by* round-2 closures.
**Evidence:** Three constructs the brief does not name are absent from the five bullets:

**(a) F-number assignment at fact-need time** (Design 2, spec.md:212–213): "It carries its number from the parallel `F1…Fn` series (`:48`), whether or not it was ever rendered as an `ℹ️` request — a dispatch-cap overflow or an abandoned in-flight exploration was numbered when it became a fact need." `skills/grilling/SKILL.md:48` says only "Fact requests use the parallel `F1…Fn` series", and `:46`/`:72` reserve "fact request" for the rendered `ℹ️` form. The reading is defensible — `### Facts established` at `:129` already carries F-ids for facts obtained by *dispatch*, never rendered as requests — but it is an interpretation the spec supplies, not a rule the brief carries, and it does not ship in the file. The one case it does not cover is a dispatch-cap overflow (`:74`) that was neither dispatched nor rendered; the shipped `:108` edit ("their fact needs are Open `F<n>` items") demands a number for a path whose numbering the file never states.

**(b) `rounds: 1/<round_cap>` and "the round was attempted and consumed"** (Design 3, spec.md:247). A round-accounting rule the brief does not carry — brief decision 4 says only that `fence-empty` is "reached when round 1 renders zero items". It is load-bearing twice over: Design 6 hard-codes `Interview: 1 round` into the `/spec-brief` References bullet (`:338`), and it is the same question `## Out of scope` item 11 fences for the post-cap resume case ("a post-cap resume that renders zero items still consuming the post-cap round").

**(c) Row 10's supersession of VHS-32 checklist row 7** (D7, spec.md:121–123). Declared at its point of use — category (c), which is fine — but the brief names only row 4, and the roll-up claims completeness for constructs "the brief does not name".

**Suggested fix:** Add (a) and (b) as roll-up bullets with their one-line justification, in the shape the existing five use. For (a), add the corroborating anchor to make it a reuse rather than an addition: "`### Facts established` (`:129`) already numbers facts obtained by dispatch, never rendered as `ℹ️` requests, so the series already numbers fact *needs*." For (c), one clause in the roll-up preamble noting that D7's supersessions are declared in D7. Then re-check whether "Nothing else" still holds.

---

### F-3: `fence-empty` narrows an active wiki decision the spec never names

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D4 (`:101–105`), Design 6 (`:340–341`), Risks 2 (`:498–504`)
**Convention violated:** The repo's decisions discipline — a spec that changes the outcome a recorded decision rejected must name the decision and say it is narrowing it. `vigil-harbor-wiki/decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` is `Status: active`, and its `Revisit when:` line names this ticket by number.
**Evidence:** That decision's § Key Decisions 5 records: "**Rejected — a success token for an empty interview.** It would write a hollow brief that every downstream lens then treats as authority." The same rationale ships verbatim in `skills/spec-brief/SKILL.md:88`: "A success token for 'nothing was ever known' would write a hollow brief that every downstream lens then treats as authority."

`fence-empty` is a second success token whose `/spec-brief` outcome is, by the spec's own Risk 2, "`_(none settled …)_` under Decisions, an empty Risks list, no Scope rows, and no fact References" — the hollow brief that sentence forbids, reached through a different door (a seed with a root, but nothing above the fence). The spec handles the mechanism honestly: Design 6 cites `:88` and states that Phase 2 does not halt, and Risk 2 accepts the outcome with a rationale. What is missing is the acknowledgment that this narrows a standing decision from "no success token writes a hollow brief" to "only `empty-seed` halts". `skills/spec-brief/SKILL.md:88` is fenced out of scope (spec `:43–44`), so the shipped file will carry a rationale sentence that the same file's new behavior contradicts, with nothing in the repo saying the narrowing was deliberate.
**Suggested fix:** One clause in D4 or Risk 2: "This narrows wiki decision `2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write` § 5 — `empty-seed` remains the only halt; `fence-empty` is a success token whose brief is hollow by design, and `skills/spec-brief/SKILL.md:88`'s rationale is left as written because that sentence is about `empty-seed`. `/spec-close` records the narrowing." No file edit follows from this; it is the drift-check's and the close's anchor.

---

### F-4: The roll-up's statement of the both-lists rule is narrower than the rule Design 5 now specifies

**Severity:** P3
**Where:** spec.md:67–69 (roll-up bullet 3) vs spec.md:299–301 (Design 5, step-5 `left open` bullet)
**Convention violated:** Internal consistency between the roll-up and the design it summarizes — the roll-up is what the drift-check reads, so it must not state a rule the design contradicts.
**Evidence:** The roll-up reads: "an id on both a Settled and an Open item is printed under `left open` **only**." Design 5 now reads: "listed here rather than under `dispositioned` … **It still appears under `deferred to option 3`** if step 4 could not apply its Settled item" — the clause added to close edge-cases R1 F-5. Read literally, the roll-up forbids what the design requires.
**Suggested fix:** "…is printed under `left open` rather than `dispositioned` (it may still appear under `deferred to option 3`)."

---

### F-5: D7 names the supersession of VHS-32 rows 4 and 7; row 10 also supersedes row 6

**Severity:** P4
**Where:** spec.md:121–123 (D7) vs spec.md:419–421 (row 10)
**Convention violated:** D7's own supersession logic — the archived checklist is not re-runnable from `DONE/`, so every assertion this diff could break must be re-asserted and the supersession recorded.
**Evidence:** `docs/specs/DONE/VHS-32/spec.md:460` (row 6) pins "`grep -c 'total_p0p1 == 0'` unchanged; 2e and 2g byte-identical". Row 10 here carries all of it and tightens it (`:426–465`, `:466–487`, `:563–595`), so the supersession is factually complete — D7's sentence just says "rows 4 and 7".
**Suggested fix:** D7: "Together they supersede VHS-32 rows 4, 6 and 7."

---

## Notes (no finding)

Checked this round so later rounds need not re-derive:

- **Every anchor in the spec verifies at HEAD `7403cb5`.** I re-read all of them: `grilling` `:12`, `:18`, `:23`, `:31`, `:33–58`, `:37–44`, `:48`, `:57`, `:59–66`, `:61`, `:68–79`, `:70`, `:72`, `:74`, `:76`, `:80–100`, `:84–86`, `:88`, `:94–98`, `:104`, `:106`, `:108`, `:110`, `:118–130`, `:132`, `:134`, `:136–151`; `spec-cycle` `:366`, `:453`, `:489–561`, `:495–496`, `:504`, `:518–528`, `:539–546`, `:548–549`, `:556–561`, `:426–465`, `:466–487`, `:563–595`, `:640`, `:698–703`; `spec-brief` `:80`, `:88`, `:139`, `:140`, `:143`; `grill-me` `:14`, `:21`; `docs/spec-workflow-reference.md` `:23`, `:35`. Risk 4's accuracy claim now holds.
- **Row 1 verified by running it.** `python lint.py --strict` → 0 errors, 2 warnings, both `missing-requires` on `review-pr` and `ship-spec`. Unchanged.
- **Row 3's `grep -c … → 0` is carried precedent**, verbatim from VHS-32 checklist row 3 (`DONE/VHS-32/spec.md:457`). Not a new convention drift.
- **Row 5 still covers VHS-32 row 4 string by string**, and row 10 covers VHS-32 row 7's nine strings plus the scalability line. Re-verified against `DONE/VHS-32/spec.md:458` and `:461`.
- **`README.md` and `AGENTS.md` verified clean.** Neither paraphrases the hand-off block, the exit tokens, `Settled`/`Open frontier`, or `Grill summary`; the only `handoff` hits in `AGENTS.md` are the unrelated `session-handoff` / `agentcraft-handoff` paragraph. The spec's `:47–50` claim is accurate. `docs/customizing.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md` are likewise clean.
- **`fact not established` has no caller.** Re-ran the grep: outside `docs/specs/` and a session handoff file, only `grilling:74`, `:88`, `:125`. Dropping it from the Q-item list is the correct delete-cleanly call, and the roll-up's evidence at `:76` is accurate.
- **Still no premature abstraction.** `ref:` is a field on existing lines; `blocked-on: F<n>` reuses `blocked-on: Q<m>`; the lens-qualified id reuses a form `spec-cycle` already emits at `:366` and `:504`. No registry, dispatcher, or strategy pattern.
- **`## Out of scope` has grown from 11 fences to 12** (item 12, `/spec-brief` Phase 3's "revise by Q number", from edge-cases R1 F-11). D12 routes reviewer-driven *constructs* to `## Deferred (P2+)`; a new fence is not a construct, and item 12 correctly points at item 11's ticket. Recording it only because round 1's note asserted 1:1 parity with the brief.
- **Wiki decision `2026-08-09-review-round-artifacts-are-immutable`** is honored: no round-1 report was edited, and closure is recorded forward in this table.

## Summary
P0: 1 | P1: 0 | P2: 2 | P3: 1 | P4: 1

STATUS: RED P0=1 P1=0 P2=2 P3=1 P4=1
