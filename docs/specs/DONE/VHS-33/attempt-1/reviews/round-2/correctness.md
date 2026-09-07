# Correctness Review — round 2

## Grounding notes

- Spec and brief read fresh from disk. `CLAUDE.md` (global + project) read.
- Plane ticket VHS-33 retrieved from memory (`namespace: skills`, record `e96bd119-9e11-44a8-8fe0-08b2f297fc4b`, 6 chunks, `tag_exact` 1.00). No Done-when section, as the brief states. One ticket/brief divergence — the ticket's SCOPE names "the option-4 re-offer on a zero-rendered grill"; brief decision 7 (operator's own Q5 answer) declines it and spec D7 + Out-of-scope 5 record the disposition with rationale. Explicitly dispositioned, not drift. Not a finding.
- **All anchors re-verified against HEAD `7403cb5`.** `skills/grilling/SKILL.md` `:12`, `:14–23`, `:23`, `:33–57`, `:52–55`, `:53`, `:68–78`, `:72`, `:74`, `:76`, `:80–100`, `:88`, `:102–112`, `:106`, `:108`, `:114–134`, `:119`, `:122`, `:125–126`, `:129`, `:136–138`, `:146–151` — all correct. `skills/spec-cycle/SKILL.md` `:489–561`, `:491–509`, `:495`, `:499–505`, `:518–537`, `:539–546`, `:548–554`, `:646`, `:698–708` — all correct. `skills/spec-brief/SKILL.md` `:84–90`, `:92–107`, `:113–128`, `:134–143`, `:139`, `:140`, `:141`, `:142`, `:143`, `:156–164` — all correct. `skills/grill-me/SKILL.md:14`, `:18–21`; `docs/spec-workflow-reference.md:23`, `:33`, `:35`; `docs/specs/DONE/VHS-32/spec.md:458` — all correct. Design 8's verbatim quote of `:23` matches the file exactly.
- **Checklist claims independently executed:** `python lint.py --strict` → `0 error(s), 2 warning(s)` (`review-pr`, `ship-spec`) ✓ row 1. Row 2's grep returns 5 hits, every one exempt ✓. `grep -c 'total_p0p1 == 0'` → 2 ✓ row 11. `grep -c 'options 1–3'` → 4 (see F-2). `grep -rn grilling lint.py sync.py tests/` → zero hits ✓ Risks 1. `README.md`/`AGENTS.md` carry no paraphrase of the block or the exit tokens ✓ Scope "leave alone". VHS-32 Risks 9/11/14 at `:525`/`:527`/`:530` match the spec's Risk 3 characterization ✓.
- `git log -10` over the five Scope files: newest is `d381f88` (2026-09-06, PR #26), one commit old. Risks 4 records this accurately.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Design 4 defines `empty-frontier` two ways | CLOSED | spec:326–329 keeps both reason lines and pins the round-1-only boundary; Design 7's "which of the two it was" replaced at :466; Design 8 :492–497; row 8 :558–563 |
| correctness | F-2 | row 2 grep unsatisfiable vs row 10 | CLOSED | row 2 :519–524 scopes spec-cycle to `git diff -U0` added lines; § Scope :46–48 names § 2b. Grep re-run: passes today |
| correctness | F-3 | F-item "exactly two values" vs third string | CLOSED | block :223 shows the inline optional parenthetical; :232–235 states it is a qualifier, never a third value |
| correctness | F-4 | `ref:` has no slot on F-item / rolled-up item | CLOSED | block :219, :222–224 renders all four shapes with trailing `ref:`; placement rule :206–208; row 4 :526–531 |
| correctness | F-5 | seeded finding reported nowhere | CLOSED | `not reached` clause :413–417; completeness :418–419; row 10 :573 |
| correctness | F-6 | "supersedes" mischaracterizes VHS-32 row 4 | CLOSED | D9 :128–133 says *extends*; new row 5 :536–542 keeps the invariants under test |
| correctness | F-7 | empty-Settled rule over-broad | CLOSED | Design 7 all-sections-empty rule :460–466 (residual: new F-4 below) |
| correctness | F-8 | `F1 <answer>` line pinned byte-identical | CLOSED | Design 3 :310–314 records the choice explicitly |
| correctness | F-9 | `:74`/`:88` still in old vocabulary | CLOSED | Design 2 "Cross-references" :253–258; § Scope :28 names both |
| correctness | F-10 | `:23` mislabelled as contract paraphrase | CLOSED | § Scope :32 splits the two anchor groups |
| correctness | F-11 | touched surface one commit old | CLOSED (accepted) | Risks 4 :677–679; § Deferred :710–711 |
| edge-cases | F-1 | two-value reason set vs qualifier | CLOSED | same as correctness/F-3 |
| edge-cases | F-2 | rolled-up deferred item has no `ref:` slot | CLOSED | same as correctness/F-4 |
| edge-cases | F-3 | fence-empty on resume erases carried state | CLOSED | Design 4 "Fresh invocations only" :330–338; row 8 |
| edge-cases | F-4 | verification has no round on the last round | CLOSED | Design 3 rule 3 :300–305; row 7 (residual: new F-5) |
| edge-cases | F-5 | refuted and never-checked render identically | CLOSED | Design 3 :271–275 splits four dispositions; Design 7 :471–475 carries `path:line`; rows 7, 12 (residual on `stop`: new F-5) |
| edge-cases | F-6 | no missing-`ref:` tripwire, no reconciliation | CLOSED | Design 6 :418–419, :413–417, :430–433; row 10 |
| edge-cases | F-7 | partially-supplied id seed | CLOSED | Design 1 "All or none" :181–184 (residual: new F-7) |
| edge-cases | F-8 | `ref:` id lexical form undefined | CLOSED | Design 1 "Legal id" :178–180; row 6 |
| edge-cases | F-9 | empty-section rendering only for fence-empty | CLOSED | Design 2 "Empty sections" :245–251, "on *every* exit" |
| edge-cases | F-10 | step-5 line undefined when a set is empty | CLOSED | "Every clause renders" :404–406; purpose-written fence-empty line :435–440 (residual: new F-3) |
| edge-cases | F-11 | `:76` displaced wholesale | CLOSED | Design 3 rule 1 :291–296 narrows to the retry only |
| edge-cases | F-12 | partially confirmed claim has no disposition | CLOSED | Design 3 :280–284 |
| edge-cases | F-13 | `blocked-on: F<n>` / `stopped` overlap | CLOSED | Design 2 precedence :237–243 plus the stop-with-exploration sentence |
| edge-cases | F-14 | F-item reason set cannot distinguish four causes | **REOPENED (P3)** | No cause qualifier for the `:72`/`:74`/`:76`/`:88` causes exists anywhere in the spec; `## Deferred` :712–713 nonetheless claims every round-1 P2/P3/P4 was folded. See F-8 below |
| edge-cases | F-15 | not-grillable in chain and in unknown-id rule | CLOSED | Design 6 :424–425 removes it from the chain; :427–429 evaluates unknown-id first and excludes it |
| conventions | F-1 | rows 2 and 10 mutually unsatisfiable | CLOSED | same as correctness/F-2 |
| conventions | F-2 | `## Test command` carries prose | CLOSED | § Test command :602–604 is exactly `N/A`; framing moved to :511–513 |
| conventions | F-3 | Out-of-scope not split | CLOSED | :629 / :644–657 carry the two labelled lists |
| conventions | F-4 | no roll-up of spec-level additions | CLOSED | § Decisions preamble :56–72 (residual: new F-6, F-9) |
| conventions | F-5 | absent-`ref:` justified by compat | CLOSED | Design 1 :201–204 restates it as legibility |
| conventions | F-6 | no `## Risks` / `## References` | CLOSED | :659–679 and :681–706; contents independently verified |
| conventions | F-7 | wiki revisit trigger unrecorded | CLOSED | D9 :135–137; Out of scope 11 :656–657 |
| conventions | F-8 | fifth clause conditionally omitted | CLOSED | "Every clause renders" :404–406 |
| conventions | F-9 | three spellings of "empty" | CLOSED | Design 2 :249–251 distinguishes section vs field sentinels |

REOPENED: 1 (edge-cases/F-14, P3 — original severity retained, non-blocking).

## Findings

### F-1: The spec says the open frontier has *three* item shapes in four places and *two* in three places
**Severity:** P1
**Where:** spec:32 (Scope table), spec:498–500 (§ Design 8), spec:592–594 (checklist row 14) vs spec:196–197, spec:206–208, spec:222–224 (§ Design 2 block), spec:526–527 (checklist row 4)
**Claim:** Design 8: "`:35` (the hand-off-block sentence) gains the caller-id `ref:` field, **the open frontier's two item shapes**, and that facts carry the source the exploration found". Repeated verbatim in the Scope table cell for `docs/spec-workflow-reference.md` and in checklist row 14.
**Why this is wrong:** The same document, using the same word, states the opposite count four times:
- spec:196–197 — "**every** Settled and Open item carries a `ref:` — all **three** Open shapes included."
- spec:206–208 — "since **two of the three Open shapes** lack the field the first draft anchored it to."
- spec:222–224 — the authoritative block renders three numbered Open items: the Q-item, the `**F<n>**` item, and the rolled-up deferred item.
- spec:526–527 (row 4) — "`ref:` as the last field on **all four** item shapes" (one Settled + three Open).

The rolled-up deferred item is a real third Open shape — it is the case D1 exists for (brief problem 1: "a rolled-up deferred subtree, which has no Q number at all"), and this spec *newly* gives it an `unresolved because: deferred` field, making its shape more distinct, not less. An implementer following Design 8 and row 14 writes "the open frontier's two item shapes" into `docs/spec-workflow-reference.md:35` — a public paraphrase of the contract that contradicts the contract it paraphrases — and row 14 gates on that wrong statement, so the checklist certifies the error rather than catching it. This is also a direct violation of the spec's own Design 5 rule "One meaning per term: the same thing keeps the same name" (spec:361–362).
**Suggested fix:** Change all three occurrences to name what is intended. Either "the open frontier's three item shapes — questions, facts, and the rolled-up deferred subtree" (matching Design 1/Design 2/row 4), or, if only the new question-vs-fact distinction is meant for the paraphrase, say so explicitly: "that the open frontier distinguishes a question item from an `F<n>` fact item". Update Scope:32, Design 8:498–500, and row 14:592–594 together.

---

### F-2: Checklist row 10 pins `grep -c 'options 1–3'` at 4, but Design 6 prescribes a new bullet containing that exact string
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:447–450 (§ Design 6 failure-modes bullet) vs spec:577–578 (checklist row 10)
**Claim:** Design 6: "`## Failure modes` gains one bullet: … `total_p0p1` is unchanged, and the menu re-renders **with options 1–3**." Row 10: "No option 4 re-offer is added: `grep -c 'options 1–3' skills/spec-cycle/SKILL.md` is unchanged at 4."
**Why this is wrong:** `grep -c 'options 1–3' skills/spec-cycle/SKILL.md` returns 4 today (`:509`, `:516`, `:522`, `:550`). The two existing `## Failure modes` bullets use the *other* spelling — `:703` and `:708` both read "re-renders with 1–3", without "options". An implementer who copies Design 6's own wording into the new bullet takes the count to 5 and fails row 10; an implementer who matches the local `## Failure modes` style keeps it at 4 and passes. The spec does not say which, and because `## Test command` is `N/A` this checklist *is* the `/ship-spec` gate (spec:513), so the ambiguity resolves into a spurious gate failure rather than a note.
**Suggested fix:** Either word Design 6's bullet "the menu re-renders with 1–3" (matching `:703`/`:708`), or change row 10's assertion to a semantic one that does not depend on the phrasing.

---

### F-3: The purpose-written `fence-empty` line drops the `not grillable` clause, which `spec-cycle:702` calls those findings' only record
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:435–440 (§ Design 6) vs spec:404–406 ("Every clause renders") and spec:418–419 ("Completeness")
**Claim:** On a `fence-empty` exit the six-clause line "is replaced by a purpose-written one".
**Why this is wrong:** A `fence-empty` exit requires a **non-empty** seed (step 1 at `skills/spec-cycle/SKILL.md:507–509` refuses to invoke `grilling` when the seed is empty after exclusions), so a run can have both a non-empty seed *and* a non-empty not-grillable set — one lens report missing while the others carry findings. The replacement line has no `not grillable` clause. `skills/spec-cycle/SKILL.md:700–703` states that for not-grillable findings "the step 5 `not grillable <ids>` line is **their only record**" — they are deliberately never written to `grill.md`. So on the one exit where nothing else moved, the not-grillable ids are reported nowhere in the operator's summary line, which is the same silent-omission failure Design 6's own "Every clause renders" rule and completeness rule were written to prevent.
**Suggested fix:** Add the clause to the replacement line, or state in Design 6 that step 1's separate `not grillable: <lens>/<id> — reviewer report unavailable…` line still prints on this exit and is the record. Assert whichever in checklist row 10.

---

### F-4: Design 7's fence-empty brief collides with `spec-brief:139`'s existing empty-Settled sentinel and leaves `## Scope` with no stated rendering
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:460–466 (§ Design 7) against `skills/spec-brief/SKILL.md:139`
**Claim:** "a brief written from a `fence-empty` summary carries `_(none)_` under `## Decisions carried forward` and under `## Risks / decisions`, no `## Scope` rows, and a distinct warning".
**Why this is wrong:** Two gaps.
1. `skills/spec-brief/SKILL.md:139` is unconditional: "If Settled is empty, write `_(none settled — see Risks / decisions)_` under the header…". A `fence-empty` summary has an empty Settled section, so `:139` fires — and it mandates a *different* sentinel from Design 7's `_(none)_`. The spec narrates the override for the warning text but never says `:139`'s sentinel is superseded too, so an implementer has two live rules matching the same input with different output. Checklist row 12 asserts only "the all-sections-empty rule with its distinct warning text", so the gate would not catch either shape.
2. "no `## Scope` rows" leaves the mandatory `## Scope` header (template `:121`) with no stated body while the two adjacent sections get `_(none)_`. `/spec-cycle`'s Phase 3 parser keys on three brief headers; the spec's own general empty-section discipline (Design 2 :245–251) argues against leaving one blank.
**Suggested fix:** State in Design 7 that the all-sections-empty rule is the more specific rule and overrides `:139` for both the sentinel and the warning, and give `## Scope` an explicit rendering. Extend row 12 to assert all three renderings.

---

### F-5: On a `stop` exit the F-item reason precedence erases the `(operator claim, …)` qualifier that Design 3 exists to preserve
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:300–305 (§ Design 3 rule 3) and spec:237–243 (§ Design 2 precedence) vs spec:271–275 and spec:471–475
**Claim:** Rule 3: "on a `stop` exit the reason is `stopped` per the precedence order in Design 2." Design 2: the qualifier is "an **optional qualifier on the first value** [`fact not established`], never a third value."
**Why this is wrong:** Two problems, one structural and one substantive.
- *Structural:* the precedence order Design 3 cites is declared under the heading "**The Q-item reason set narrows**" (spec:236) and enumerates values from the **Q-item** set. It is not stated as an F-item rule, yet rule 3 applies it to an F-item.
- *Substantive:* because the qualifier can only attach to `fact not established`, an F-item that resolves to `stopped` carries no qualifier at all. So in the reachable case — operator answers `F1 <answer>` in round 2, verification is dispatched at the top of round 3, operator types `stop` in round 3 (`skills/grilling/SKILL.md:108` abandons in-flight explorations) — the hand-off says only "stopped", indistinguishable from a fact request nobody ever answered. Design 7's Phase 4 rule then finds no qualifier to carry, so the brief loses the fact that a human already asserted an answer. That is precisely the collapse Design 3's own refuted bullet argues against at spec:272–275.
**Suggested fix:** Either allow the qualifier on `stopped` as well (`unresolved because: stopped (operator claim, unverified)`), or state the precedence explicitly for the F-item set and record the information loss as accepted. State whichever in Design 2's F-item paragraph rather than by reference from Design 3, and assert it in row 7.

---

### F-6: The `## Decisions` roll-up calls the precedence rule "four-way"; Design 6 defines a three-way chain
**Severity:** P3
**Where:** spec:69 vs spec:420–425
**Why this is wrong:** Design 6's chain is three entries — "`left open` → `deferred to option 3` → `dispositioned`" — after the round-1 fix (edge-cases F-15) removed `not grillable` from it, with an explicit sentence saying so at spec:424–425. "Four-way" is a leftover from the pre-fix draft. The roll-up exists specifically so `/spec-cycle`'s Phase 3 drift-check can see the spec-level additions; a stale count there is the one place it should not be.
**Suggested fix:** spec:69 → "The three-way precedence rule (`left open` → `deferred to option 3` → `dispositioned`), …".

---

### F-7: "round-1 preamble" is not a rendering surface `skills/grilling/SKILL.md` defines, and does not exist on the exits where the rule is needed
**Severity:** P3
**Where:** spec:181–184 (§ Design 1, "All or none")
**Why this is wrong:** `## Per-round output contract` (`skills/grilling/SKILL.md:33–57`) defines exactly four rendered constructs — the fork block, the plain form, the `ℹ️` fact-request form, and the two round-end literal lines. There is no "preamble" anywhere in the file, so the spec directs the implementer to write a rule against a surface that has no definition. It is also unreachable on the two exits where a caller error most needs surfacing: `empty-seed` "return[s] the token and a one-line reason, and nothing else" (`:110`) and `fence-empty` renders zero rounds (spec:322), so neither has a round 1 to carry the preamble. Checklist row 6 asserts "the all-or-none rule" without pinning where the message goes.
**Suggested fix:** Either define the surface in Design 5 alongside the plain-language rule, or relocate the message to the hand-off block's reason line, which every exit but `empty-seed` renders.

---

### F-8: `## Deferred (P2+)` claims every round-1 P2/P3/P4 was folded; edge-cases R1 F-14 was not
**Severity:** P3
**Where:** spec:712–713 vs `docs/specs/TODO/VHS-33.reviews/round-1/edge-cases.md` § F-14
**Why this is wrong:** Edge-cases R1 F-14 (P3) asked for an optional cause qualifier on `fact not established` distinguishing the four reachable causes (`skills/grilling/SKILL.md:88`, `:74`, `:76`, `:72` — the last of whose `*(no read-restricted agent available in this host)*` tag has no carrier into the hand-off). The spec's Design 3 adds qualifiers only on the **operator-claim** path. The finding is neither folded nor listed as deferred, so the round-2 closure manifest and the spec's own `## Deferred` section both overstate coverage — and `/spec-close`'s reconciliation reads this section.
**Suggested fix:** Either fold it (allow the same optional-parenthetical mechanism Design 2 already defines) or add it to `## Deferred (P2+)` as a second entry with a one-line reason, and correct the "no other … is deferred" sentence.

---

### F-9: D9's "extends" is a substantive change to brief decision 9's "supersedes" and is not listed in the spec-level-additions roll-up
**Severity:** P3
**Where:** spec:128–133 (D9) and spec:56–72 (roll-up) vs brief:44
**Why this is wrong:** Brief decision 9 reads "…carries its own checklist row asserting the v2 block and **notes that it supersedes VHS-32 checklist row 4**." D9 reverses that. The change is correct (round-1 correctness F-6 established that row 4's assertions all survive v2, verified again here against `docs/specs/DONE/VHS-32/spec.md:458`), but it is a spec-level departure from a brief-recorded decision presented under a "carried from the brief" header, and the roll-up — which exists precisely so the Phase 3 drift-check sees such departures — does not list it.
**Suggested fix:** Add a bullet to the roll-up: "*extends* rather than *supersedes* for VHS-32 checklist row 4, plus new checklist row 5 keeping its invariants under test (D9) — brief decision 9 says 'supersedes'; row 4's assertions all survive v2 unchanged."

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 4 | P4: 0

STATUS: RED P0=0 P1=1 P2=4 P3=4 P4=0
