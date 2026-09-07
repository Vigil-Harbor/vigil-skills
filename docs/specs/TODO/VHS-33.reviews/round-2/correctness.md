# Correctness Review — round 2

Grounding completed: spec and brief re-read from disk at `docs/specs/TODO/VHS-33.spec.md` / `.brief.md`; Plane ticket VHS-33 retrieved from the `skills` namespace (`record_id e96bd119-9e11-44a8-8fe0-08b2f297fc4b`, confidence 1.00, tag-exact) and consistent with the brief; `CLAUDE.md` + `AGENTS.md` read; all three round-1 reports read; every `path:line` anchor in the spec re-verified against the working tree at `7403cb5`. `git log -10` over the five touched files returns one commit, `d381f88` (2026-09-06) — the files were created that day; no competing in-flight change. `scale_lens == off` and no `scalability.md` exists in `round-1/`, so the stale-report guard is a no-op.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Checklist row 8 unsatisfiable (digits) | CLOSED | spec:414 row 8 now "states no sentence count, word limit, or other numeric bound … adds no round-preamble slot" |
| correctness | F-2 | fence-empty empties every list, destroys not-grillable record | CLOSED | spec:306–312 empties only dispositioned / left open / deferred-to-3; "`not grillable` is unaffected … this line is their only record" |
| correctness | F-3 | Descent/Rendering rules have no landing site | CLOSED | spec:159–176 — omission sentence inside the `:18` blockquote, new blockquoted `ref:` paragraph landed after `:130`; row 7 (spec:405–410) asserts both. (Residual F-item gap → new F-2 below) |
| correctness | F-4 | closure-manifest anchor `:349` wrong | CLOSED | spec:60–63 and :518 now cite `:366` + `:504`, and exclude `:453` — all three verified |
| correctness | F-5 | Four edit-site ranges off by one | PARTIAL | `:495–496` ✓, `:539–546` ✓, hand-off `:118–130` ✓ in both cells; but spec:109 (D5) still cites `:555–560` while spec:318/:521 cite `:556–561` (correct) |
| correctness | F-6 | "Omit the clause when n is 0" undeclared addition | CLOSED | spec:305 "It always prints, `0` included, like the other lists" |
| correctness | F-7 | Scope table "names six exits" | CLOSED | spec:28 now "names the fence-empty shape, `ref:`, and unestablished facts" |
| correctness | F-8 | "same shape `:80` uses" overstated | CLOSED | spec:330–331 "without its `(exploration failed)` cause — no cause qualifiers" |
| correctness | F-9 | `grilling:108` still says "questions" | CLOSED | spec:250–253 replaces the clause. (New `:151` variant → new F-4 below) |
| correctness | F-10 | Rolled-up line has no separator before `ref:` | CLOSED | spec:194 / row 4 pin `)**. ref: <…>` |
| correctness | F-11 | `d381f88` landed today — no action | CLOSED | spec:554–555 Deferred (P2+) |
| edge-cases | F-1 | Row 8 unsatisfiable | CLOSED | same edit as correctness/F-1 |
| edge-cases | F-2 | Two causes never produce a rendered `F<n>` | CLOSED | spec:212–213 "carries its number from the parallel `F1…Fn` series (`:48`), whether or not it was ever rendered" |
| edge-cases | F-3 | fence-empty writes a hollow brief | CLOSED | spec:498–504 Risk 2, recorded as accepted with the out-of-scope-10 pointer, as advised |
| edge-cases | F-4 | `empty-frontier` sentence false for round-≥2 fence-out | CLOSED | spec:245–247 "distinguishes `tree fully visited` from `no candidate decision met the altitude fence` (a later round's remaining candidates all fell below the fence)" |
| edge-cases | F-5 | Both-lists rule also suppresses `deferred to option 3` | CLOSED | spec:300–301 "It still appears under `deferred to option 3` if step 4 could not apply its Settled item" |
| edge-cases | F-6 | Unknown `ref:` id has no step-4 rule | CLOSED | spec:537–541 Deferred (P2+) with the adoptable rule, as advised (do-not-fold) |
| edge-cases | F-7 | `left open` empty on fence-empty misreports | CLOSED | spec:308–310 "the empty `left open` is not a claim that nothing is open" |
| edge-cases | F-8 | Unreferenced unapplied Settled item in no list | CLOSED | spec:542–546 Deferred (P2+), as advised |
| edge-cases | F-9 | Row 13 forbids the change Design 7 requires | CLOSED | spec:436–438 "no line other than `:23` and `:35` changes"; `:23` clause added |
| edge-cases | F-10 | Justification anchor wrong | CLOSED | same as correctness/F-4 |
| edge-cases | F-11 | Phase 3 offers "revise by Q number" after fence-empty | CLOSED | spec:489–491 Out of scope 12, tied to item 11 |
| edge-cases | F-12 | `rounds:` on a fence-empty header never pinned | CLOSED | spec:247 pins `rounds: 1/<round_cap>`; row 6 (spec:403) asserts it |
| edge-cases | F-13 | Three spec-cycle anchors off by one | PARTIAL | two fixed; the closing-paragraph anchor is still `:555–560` at spec:109 (see correctness/F-5) |
| edge-cases | F-14 | `left open` has no de-dup clause | CLOSED | spec:298 "each id once, in seed order" |
| edge-cases | F-15 | `stopped` flattened to "not established" | CLOSED | spec:547–550 Deferred (P2+), as advised |
| edge-cases | F-16 | Row 16 greps non-content diff lines | CLOSED | spec:445–446 now `\| grep '^+' \| grep -v '^+++' \|` with the stated exclusion |
| edge-cases | F-17 | Two rendering separators unspecified | CLOSED | (a) period added spec:194; (b) omission rule deleted (spec:305) |
| edge-cases | F-18 | `ref:` id character legality | CLOSED | spec:551–553 Deferred (P2+), as advised |
| conventions | F-1 | `ref:` omission/descent rules have no landing anchor | CLOSED | same edit as correctness/F-3 |
| conventions | F-2 | Additions roll-up incomplete | CLOSED | spec:59–76 now five bullets incl. `blocked-on: F<n>`, both-lists rule, exit token in step-5, and the `fact not established` drop; the two constructs F-2 named are gone or declared |
| conventions | F-3 | `fact not established` kept on the Q line for no consumer | CLOSED | spec:214–217 drops it; grep re-verified — only `grilling:74`, `:88`, `:125` carry the string outside `docs/specs/` |
| conventions | F-4 | Closure-manifest anchor wrong | CLOSED | same as correctness/F-4 |
| conventions | F-5 | Scope table "six exits" | CLOSED | same as correctness/F-7 |
| conventions | F-6 | Two Scope changes with no asserting row | CLOSED | row 7 asserts callers-map "F-items"/"by `ref:`" (spec:409); row 10 asserts the `:698–703` sentence (spec:424–425) |
| conventions | F-7 | Row 10 does not re-assert VHS-32 row-7 invariants | CLOSED | spec:425–430 "Supersedes VHS-32 checklist row 7" with all nine strings; verified against `docs/specs/DONE/VHS-32/spec.md:461` |
| conventions | F-8 | Three spec-cycle anchors off by one | PARTIAL | see correctness/F-5 |
| conventions | F-9 | "the same shape `:80` uses" | CLOSED | same as correctness/F-8 |
| conventions | F-10 | Row 14 fence omits README/AGENTS | CLOSED | spec:439–442 row 14 + spec:47–50 Files to leave alone; I re-verified neither file paraphrases the contract or the exit tokens |

## Findings

### F-1: Checklist row 7's `grep -c 'ref:' ≥ 8` cannot pass — the spec's own design produces exactly 7 matching lines
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-33.spec.md:410` (Test plan row 7), against Designs 1 and 2 (`:159–179`, `:185–228`)
**Claim:** row 7 closes with `` `grep -c 'ref:' skills/grilling/SKILL.md` ≥ 8 ``.
**Why this is wrong:** `grep -c` counts *matching lines*, not occurrences, and `skills/grilling/SKILL.md` has no wrapped paragraphs — every prose paragraph and every bullet is a single physical line (`:18`, `:23`, `:29`, `:70`, `:74`, `:76`, `:85`, `:106`, `:108`, `:116`, `:132`, `:134`, `:148–151` are all one-line). Under that convention the change introduces exactly seven `ref:`-bearing lines, which is also row 7's own enumeration:

1. the `:18` seed bullet (spec:163–166 — two `ref:` mentions, one line),
2. the new `ref:` paragraph after the fence (spec:171–176 — three mentions, one line),
3. the Settled line (spec:189), 4. the Open question line (spec:192), 5. the F line (spec:193), 6. the rolled-up line (spec:194),
7. the callers-map sentence (spec:227).

That is 7 < 8. `grep -c 'ref:'` on the file today is `0`, so there is no pre-existing line to make up the difference, and `:108`, `:104`, `:106` carry no `ref:`. Round-1 row 7 asserted `≥ 6` for six sites; the spec added one site (the `ref:` paragraph) and raised the threshold by two. Because `## Test command` is `N/A` and spec:373 declares "The checklist is the `/ship-spec` gate", a faithful implementation fails the gate — the same failure class as round-1 correctness/F-1 and edge-cases/F-1. The only way to pass is to hard-wrap a paragraph against file convention, which then collides with row 15's byte-for-byte `sync.py push` round-trip expectation of a hand-edited file.
**Suggested fix:** Change row 7's last clause to `` `grep -c 'ref:' skills/grilling/SKILL.md` ≥ 7 (seed bullet, the `ref:` paragraph, four block lines, callers-map sentence) ``.

---

### F-2: The `ref:` descent rule has no clause for `F<n>` Open items, so the F line's `ref:` field can only ever render `none`
**Severity:** P1
**Where:** spec `:171–176` (Design 1, the `ref:` paragraph), against `:193` + `:203–205` (Design 2), `:298–299` (Design 5), `:387` (row 4), and brief `:38` (decision 1)
**Claim:** the paragraph that ships in `skills/grilling/SKILL.md` reads, in full:
> `ref:` renders on every Settled and Open item when any seed item carried an `id`, and on none otherwise. An item's ids are those of the seed items it descends from: a question descends from the seed items it was raised to disposition, a decision from its question, the rolled-up deferred item from the deferred question. Ids are listed in seed order; an item descending from no identified seed item (a fact-driven decision, or a question raised about an unidentified seed item) renders `ref: none`.

**Why this is wrong:** The descent enumeration covers three item kinds — question, decision, rolled-up deferred item. It does not cover the `F<n>` Open item, which this spec newly creates as a fourth kind (spec:193, `**F<n> — <fact needed>** — unresolved because: … ref: <…>`). The catch-all clause then applies by construction: an F-item "descend[s] from no identified seed item" under the rule as written, so every F-item renders `ref: none`. That contradicts three other sections of the same spec:

- **spec:203–205** — "`ref:` is the trailing field on the Settled line, the Open question line, **the new F line**, and the rolled-up line (Design 1)" — i.e. the field is declared to carry ids there.
- **spec:387 (checklist row 4)** — pins `ref: <…>` on the F line, the same placeholder used for the Q line, not the `none` arm.
- **spec:298–299 (Design 5, step 5)** — "`left open` lists every id on an Open item (**Q, F**, or rolled-up), each id once, in seed order." If F-items structurally carry no ids, the `F` arm of that rule is dead and the step-5 line silently under-reports.

It also violates the brief's load-bearing decision 1 (`brief:38`): "echoed verbatim as a `ref:` field on every Settled and Open item **that descends from it**" — brief decision 3 (`brief:40`) makes the F-item an Open item, so the brief requires a descent path for it. The natural rule ("a fact request descends from the question that needs it") is not stated, and it matters most in exactly the case Design 2 newly admits at `:212–213`: a dispatch-cap-overflow or abandoned in-flight fact need that was *never rendered* and so has no visible parent question in the block.

This is a residual of round-1 correctness/F-3 and conventions/F-1 (the descent rule now lands, but incompletely), not a reopen.
**Suggested fix:** Add one clause to the enumeration in Design 1's blockquote — "…a decision from its question, **a fact request from the question that needs it**, the rolled-up deferred item from the deferred question" — and extend row 7's paragraph assertion to require the F-item clause (e.g. `contains "descends from" and names the fact request among the descent kinds`).

---

### F-3: D5 still cites the 2f-i closing paragraph as `:555–560`, contradicting Design 5 and § References, which cite `:556–561`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:109` vs spec `:318` and spec `:521`
**Claim:** spec:109 — "Design 5 changes nothing about the bound: 2f-i's closing paragraph (`:555–560`) is untouched"; spec:318 — "The closing paragraph (`:556–561`, "never re-dispatches reviewers … at most once per invocation") is untouched."
**Why this is wrong:** At `7403cb5` the paragraph is `skills/spec-cycle/SKILL.md:556–561` — `:555` is blank and `:561` ("…does not withhold option 4.") is the paragraph's last line, so `:555–560` is wrong on both ends. Round-1 correctness/F-5, edge-cases/F-13 and conventions/F-8 all flagged this; two of the three instances were corrected and one was missed, leaving the spec citing two different ranges for one paragraph. `/ship-spec` re-reads anchors (spec Risk 4), and spec:509 asserts "All anchors were read at `7403cb5`", which this instance falsifies.
**Suggested fix:** Change spec:109 to `` (`:556–561`) `` so all three citations agree.

---

### F-4: After Design 3 edits `:108`, the fenced `## Failure modes` bullet at `:151` still gives the abandoned-exploration item the Q form — and row 9 pins it to no change
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:250–253` (Design 3's `:108` clause replacement) and `:415–418` (row 9's `:136–151` no-hunk fence), against `skills/grilling/SKILL.md:151`
**Claim:** Design 3 replaces `:108`'s "their questions are Open with `unresolved because: stopped`" with "their fact needs are Open `F<n>` items with `unresolved because: stopped`"; row 9 asserts `git diff -U0` shows **no hunks** in `:136–151`.
**Why this is wrong:** `skills/grilling/SKILL.md:151` is the `## Failure modes` bullet for the same event, in the same file, and reads verbatim today: "**`stop` with explorations in flight** — abandon them; their questions are Open with `unresolved because: stopped`." After the edit the file states two different shapes for one input: `:108` says the abandoned exploration's item is an `F<n>` Open item, `:151` says it is a question. Because row 9 explicitly forbids a hunk there, the divergence ships and is gate-enforced. A careful reader can construct a complementary reading (`:108` = the fact need, `:151` = the downstream question), but nothing in the file says so, and `:108`'s edit *replaced* rather than augmented the "their questions" clause — the strong signal is that the author considers the item a fact need, which makes `:151` stale. This is a new variant of round-1 correctness/F-9's root (the same clause exists twice; only one instance was fixed).
**Suggested fix:** Either (a) extend Design 3 to make the same one-clause replacement at `:151` and shorten row 9's fence to `:136–150`, or (b) add a sentence to Design 3 stating that `:151` is deliberately left describing the downstream question and that `stopped` is legal on both the Q and F forms, so the two sentences are complementary — and say so in `## Files to leave alone`.

---

### F-5: D13's "F-items were always counted against `question_cap`, so they were always inside it" does not hold for the never-rendered fact needs Design 2 newly names
**Severity:** P3
**Where:** spec `:149–154` (D13), against `skills/grilling/SKILL.md:74`, `:85`, `:132`
**Claim:** "No scale machinery: the hand-off block's size bound at `:132` is unchanged (F-items were always counted against `question_cap`, so they were always inside it)."
**Why this is wrong:** `:85` caps **rendered** items — "At most `question_cap` **rendered** items per round, questions and fact requests together". But Design 2 (spec:212–213) explicitly admits F-items that were never rendered: "a dispatch-cap overflow or an abandoned in-flight exploration was numbered when it became a fact need". Those come from the *dispatch* budget at `:74` ("capped at `question_cap` dispatches"), which is a second, parallel per-round allowance. So per round the Open frontier can accrete up to `question_cap` rendered items *plus* up to `question_cap` unrendered fact needs, which is not inside `:132`'s `(round_cap + 1) × question_cap` bound.

The *conclusion* is still right — `:74` already routed those unresolved fact needs to the hand-off as Open items under v1, so this spec changes only their rendered shape, and leaving `:132` alone is correct. It is the stated justification that is inaccurate, and D13 exists specifically so the Phase 3 drift-check has an anchor for the scale non-factor.
**Suggested fix:** Restate the parenthetical as the no-change claim it actually is: "(unresolved fact needs already reached the hand-off as Open items under v1 per `:74`; this spec changes their rendered shape, not their count, so `:132`'s bound is exactly as tight or loose as before)".

## Summary
P0: 0 | P1: 2 | P2: 2 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=2 P2=2 P3=1 P4=0
