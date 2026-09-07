# Edge-Cases Review — round 2

Grounding complete: spec, brief, Plane ticket VHS-33 (record `e96bd119`, confidence 1.00), CLAUDE.md, all five target files, and the three round-1 reports read from disk. Two claims verified empirically (`grep -c 'ref:'` on the current `grilling/SKILL.md` = 0; `git diff -U0` insertion hunk headers anchor to the old-side line *before* the insertion).

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Row 8 unsatisfiable ("ASD-STE100" + "no digit") | CLOSED | spec § Test plan row 8, `:413–414` — now "states no sentence count, word limit, or other numeric bound…" |
| correctness | F-2 | fence-empty empties every list, destroying the not-grillable record | CLOSED | spec § Design 5, `:306–309` |
| correctness | F-3 | Design 1 Descent/Rendering have no landing site | PARTIAL | landing site shipped (`:163–176` blockquote, row 7), but the descent rule enumerates only question / decision / rolled-up — no F-item clause → **F-3 below** |
| correctness | F-4 | `:349` anchor wrong | CLOSED | spec `:60` cites `:366` + `:504` |
| correctness | F-5 | Four edit-site ranges off by one | CLOSED | `:25`, `:183`, `:277`, `:286`, `:318` now `:495–496` / `:539–546` / `:556–561` / `:118–130` |
| correctness | F-6 | "Omit the clause when `n` is 0" undeclared addition | CLOSED | `:305` "It always prints, `0` included" |
| correctness | F-7 | Scope cell "names six exits" | CLOSED | Scope table row now "names the fence-empty shape, `ref:`, and unestablished facts" |
| correctness | F-8 | "the same shape `:80` uses" overstated | CLOSED — but the fold's wording lands inside the file text and trips row 16 → **F-1 below** | spec `:330–331` |
| correctness | F-9 | `:108` still calls abandoned-exploration items "questions" | CLOSED | Design 3 `:251–253` edits `:108`; the duplicate at `:151` is a new variant → **F-4 below** |
| correctness | F-10 | Rolled-up line has no separator before `ref:` | CLOSED | `:194`, `:218` |
| correctness | F-11 | `d381f88` anchors (no action) | CLOSED | § Deferred, last bullet |
| edge-cases | F-1 | Row 8 unsatisfiable | CLOSED | same edit as correctness/F-1 |
| edge-cases | F-2 | Two of five causes never produce a rendered `F<n>` | CLOSED | spec `:211–213` |
| edge-cases | F-3 | fence-empty writes a hollow brief | CLOSED (accepted) | § Risks 2, `:498–504` |
| edge-cases | F-4 | `empty-frontier` sentence false for a round-≥2 fence-out | CLOSED in the primitive | Design 3 `:243–245`; caller-side consequence is new → **F-6 below** |
| edge-cases | F-5 | Both-lists rule also suppresses `deferred to option 3` | CLOSED | `:300–301` |
| edge-cases | F-6 | Unknown `ref:` id has no step-4 rule | DEFERRED as agreed | § Deferred (P2+) bullet 1 |
| edge-cases | F-7 | Empty `left open` on fence-empty misleads | PARTIAL | `:308–310` covers the total fence-out; a *partial* fence-out has the same hole and no signal → **F-5 below** |
| edge-cases | F-8 | Unreferenced + unapplied Settled item in no list | DEFERRED as agreed | § Deferred bullet 2 |
| edge-cases | F-9 | Row 13 forbids the change Design 7 requires | CLOSED | row 13, `:437–438` |
| edge-cases | F-10 | `:349` anchor | CLOSED | `:60` |
| edge-cases | F-11 | Phase 3 revise-by-Q after fence-empty | CLOSED (fenced) | § Out of scope 12 |
| edge-cases | F-12 | `rounds:` on a fence-empty header unpinned | CLOSED | Design 3 `:246–247` (`rounds: 1/<round_cap>`) |
| edge-cases | F-13 | Three spec-cycle anchors off by one | CLOSED | as correctness/F-5 |
| edge-cases | F-14 | `left open` had no de-dup clause | CLOSED | `:298` |
| edge-cases | F-15 | `stopped` flattened to "not established" | DEFERRED as agreed | § Deferred bullet 3 |
| edge-cases | F-16 | Row 16 counts non-content diff lines | CLOSED | row 16, `:445–447` |
| edge-cases | F-17 | Two rendering separators unspecified | CLOSED | `:194` (period), `:305` (always prints) |
| edge-cases | F-18 | `ref:` id character legality | DEFERRED as agreed | § Deferred bullet 4 |
| conventions | F-1 | `ref:` omission/descent rules have no anchor | PARTIAL | same as correctness/F-3 |
| conventions | F-2 | Additions roll-up incomplete | CLOSED | roll-up now five bullets (`:59–76`); omit-when-zero deleted |
| conventions | F-3 | `fact not established` kept on the Q line for no consumer | CLOSED | `:214–217`, `:74–76` (grep evidence recorded) |
| conventions | F-4 | Closure-manifest anchor wrong | CLOSED | `:60` |
| conventions | F-5 | Scope cell promises "six exits" | CLOSED | Scope table row |
| conventions | F-6 | Two Scope changes with no asserting row | CLOSED | row 7 (callers-map: "F-items", "by `ref:`"), row 10 ("A `fence-empty` exit is the same shape") |
| conventions | F-7 | Row 10 doesn't re-assert VHS-32 row 7 | CLOSED | row 10, `:425–430` (all nine strings) |
| conventions | F-8 | Three spec-cycle anchors off by one | CLOSED | as correctness/F-5 |
| conventions | F-9 | "the same shape `:80`" not the same string | CLOSED — see **F-1 below** | `:330–331` |
| conventions | F-10 | Row 14 omits README/AGENTS | CLOSED | row 14 `:439–442`, § Files to leave alone `:47–50` |

## Findings

### F-1: Design 6's `:140` file text contains the word "qualifiers", which checklist row 16 requires to be absent — the ship gate can never pass
**Severity:** P0
**Where:** spec § Design 6, `:328–331` (the blockquoted replacement for `skills/spec-brief/SKILL.md:140`) against § Test plan row 16, `:445–447`
**Edge case:** The gate row is run literally against the diff the design produces — i.e. every run, not a rare input.
**What happens:** Row 16 is
`git diff -U0 -- skills/grilling/SKILL.md skills/spec-brief/SKILL.md | grep '^+' | grep -v '^+++' | grep -ciE 'operator claim|verif|qualifier|source: operator'` → **0**.
Design 6's blockquote — file text by the spec's own convention (`` `:140` becomes: `` + blockquote, the same convention correctness/F-3 forced Design 1 to adopt) — ends `…without its `(exploration failed)` cause — **no cause qualifiers**)`. That is one added content line in `skills/spec-brief/SKILL.md` matching `qualifier`, so the row returns ≥ 1 and fails. `## Test command` is `N/A` and `:373` states "The checklist is the `/ship-spec` gate", so a deterministic row failure blocks ship — and it fails with the maximally misleading signal "VHS-36 fence violated" on a change that has nothing to do with VHS-36. Verified: `sed -n '140p' skills/spec-brief/SKILL.md | grep -ciE '<row-16 pattern>'` is `0` today, so the hit is created by this edit alone.
**Why the spec misses it:** Two round-1 folds collided. correctness/F-8 and conventions/F-9 asked for "without its `(exploration failed)` cause"; the author added the spec's own rationale ("— no cause qualifiers") *inside* the blockquote, where it becomes shipped prose. Row 16 was reviewed for false positives from hunk headers (edge-cases/F-16) but not against the spec's own added text.
**Suggested fix:** End the blockquote at `…without its `(exploration failed)` cause).` and move the justification to the spec sentence that follows the blockquote (e.g. "The cause parenthetical is dropped per the roll-up's no-cause-qualifiers rule."). Rationale about the fence belongs in the spec, not in `spec-brief`'s mapping rule. No other added line in either grepped file matches the row-16 pattern (checked all eight blockquotes).

---

### F-2: Row 7's `grep -c 'ref:' ≥ 8` fails at the seven lines the design actually produces
**Severity:** P1
**Where:** spec § Test plan row 7, `:410`, against Designs 1 and 2
**Edge case:** The gate row is evaluated on a diff written in this repo's prose style (one paragraph = one line — see `skills/grilling/SKILL.md:29`, `:70`, `:74`, `:76`, `:78`).
**What happens:** `grep -c` counts *matching lines*, not occurrences. Post-change, `ref:` appears on exactly seven lines of `skills/grilling/SKILL.md`: the `:18` seed bullet (two occurrences, one line), the new `ref:` paragraph (two occurrences, one line), the four block lines (Settled, Open Q, F, rolled-up), and the callers-map sentence. `7 < 8` → row 7 fails, and again the gate is the ship gate. Verified: `grep -c 'ref:' skills/grilling/SKILL.md` is `0` today and `grep -o … | wc -l` is `0`, so seven is the complete post-change set. The row is satisfiable only by hard-wrapping the new paragraph across lines — a formatting the spec never asks for and that no other paragraph in the file uses.
**Why the spec misses it:** Round 1's row 7 said `≥ 6` for six single-line sites (seed bullet, four block lines, callers-map). Folding correctness/F-3 added one line, and the bump to `≥ 8` appears to have counted *occurrences* (9) rather than lines (7).
**Suggested fix:** `` grep -c 'ref:' skills/grilling/SKILL.md `` → **≥ 7**, or state occurrences explicitly (`` grep -o 'ref:' … | wc -l `` ≥ 8). Prefer the line count, matching every other `grep -c` row in the checklist.

---

### F-3: The shipped descent rule enumerates three item kinds; the block defines four — F-items have no `ref:` descent rule
**Severity:** P1
**Where:** spec § Design 1, `:171–176` (the `ref:` paragraph that ships into `skills/grilling/SKILL.md`), against `:193` (the F line) and § Design 5, `:297–299`
**Edge case:** An unresolved fact need reaching the hand-off from a 2f-i grill — i.e. the exact shape D3 exists to create, on the only caller that supplies ids.
**What happens:** The paragraph reads "An item's ids are those of the seed items it descends from: **a question** descends from the seed items it was raised to disposition, **a decision** from its question, **the rolled-up deferred item** from the deferred question," and then "an item descending from no identified seed item (a fact-driven decision, or a question raised about an unidentified seed item) renders `ref: none`." A fact request is not a question in this file's vocabulary (`:46` renders `❓` questions and `ℹ️` fact requests separately; `:85` counts "questions and fact requests together"), so an F-item matches no descent clause and falls into the catch-all: **every F-item renders `ref: none`**. Consequences, all silent:
- Brief decision 1 ("`ref:` … on every Settled and Open item that descends from it") is violated for the new shape.
- Design 5's `left open` is defined as "every id on an Open item (**Q, F**, or rolled-up)" — the F arm is then always empty, so a finding whose only open item is a fact need is listed nowhere in the step-5 line (compounding F-5).
- The `blocked-on: F<n>` waiting question is the only carrier of that finding's id, and per `:63` ("Only questions actually rendered to the operator ever become named Open items") a fact-blocked question is typically never rendered — so the id can vanish entirely.

Checklist row 7 asserts only that the paragraph contains "and on none otherwise" and "descends from", so nothing at the gate catches it.
**Why the spec misses it:** The descent list was written against v1's item inventory (question / decision / rolled-up) and not re-read after Design 2 added the fourth Open form.
**Suggested fix:** One clause inside the paragraph the spec already writes — completing an enumeration, not a new construct: "…a decision from its question, **a fact request from the question whose need raised it** (or from the seed items directly, when the need arose from the seed), the rolled-up deferred item from the deferred question." Add to row 7: the paragraph names the fact request among the descent paths.

---

### F-4: `:151` still says abandoned explorations produce "questions", contradicting the `:108` this spec rewrites — and row 9 forbids fixing it
**Severity:** P2
**Where:** spec § Design 3, `:251–253` (the `:108` edit) and § Scope "Files to leave alone" `:39` + row 9 `:415–418`, against `skills/grilling/SKILL.md:151`
**Edge case:** `stop` with explorations in flight — the second of D3's exactly-two F-item reasons.
**What happens:** After the edit, `:108` reads "…in-flight explorations are abandoned, and their **fact needs are Open `F<n>` items** with `unresolved because: stopped`", while `:151` (§ Failure modes, fenced by "Files to leave alone" and by row 9's no-hunk range `:136–151`) still reads "**`stop` with explorations in flight** — abandon them; **their questions are Open** with `unresolved because: stopped`." The shipped file then states both shapes for the same input. A primitive reading § Failure modes renders a Q-item where D3 requires an F-item; the block is legal either way (`stopped` is a legal reason on both lines), so nothing downstream catches the divergence, and 2f-i's `left open` composition differs between the two readings. This is worse than the round-1 state: correctness/F-9's single wrong sentence has become a self-contradiction.
**Why the spec misses it:** correctness/F-9 named `:108` only; the identical sentence at `:151` was inside a range the spec had already fenced, and the fence was not re-examined after the `:108` edit was adopted.
**Suggested fix:** Extend Design 3 with the matching one-clause edit at `:151` ("their fact needs are Open `F<n>` items with `unresolved because: stopped`"), narrow "Files to leave alone" to `:136–150`, and change row 9's no-hunk range to `:136–150` plus an assertion that `:151` contains the F-item wording. Row 5's supersession list does not pin `:151`'s text, so nothing else breaks. If the fence is held instead, say in § Risks that the file carries two wordings and that `stopped` is legal on both forms.

---

### F-5: A seeded finding that yields no item at all appears in none of the four step-5 lists, on every exit but `fence-empty`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 5, `:294–312` (step-5 construction rules)
**Edge case:** A *partial* fence-out — some seeded findings produce askable candidates, others do not (or their candidates are truncated away by `question_cap` and the round cap arrives first). Exit is `empty-frontier` or `round-cap`, not `fence-empty`.
**What happens:** The four lists are now defined mechanically: `dispositioned` = ids on applied Settled items, `left open` = ids on Open items, `deferred to option 3` = ids on unapplied Settled items, `not grillable` = pre-seed exclusions. A finding that never became any item matches none of them, so its id is silently absent from the one line the operator reads "to see what moved without opening `grill.md`" (`spec-cycle:550–552`). It stays P0/P1 and the grill bound is spent. The spec added exactly this reassurance for the total case — "the `fence-empty` token is the signal that nothing was askable … the empty `left open` is not a claim that nothing is open" (`:308–310`) — but on `empty-frontier`/`round-cap` the token carries no such signal, so the partial case reads as "the grill accounted for everything".
**Why the spec misses it:** The fold of edge-cases/F-7 reasoned about the all-empty exit only; the partition was never walked for a mixed seed.
**Suggested fix:** One sentence appended to the `left open` bullet, no fifth clause (which brief decision 12 fences): "A seeded id that appears on no Settled and no Open item is in none of these lists — it stayed P0/P1 and is still listed in the re-rendered halt block; the lists report what the grill touched, not the full red list." Optionally assert the sentence in row 10.

---

### F-6: `/spec-brief` records the altitude-fence reason only for `fence-empty`, not for the round-≥2 fence-out Design 3 now formally recognizes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 6, `:336–338` (the `:143` replacement), against § Design 3, `:243–245`
**Edge case:** Round 1 settles decisions; round 2's recomputed frontier has candidates but every one falls below the altitude fence. Exit is `empty-frontier` with reason `no candidate decision met the altitude fence` — the case Design 3 was widened to cover when edge-cases/F-4 was folded.
**What happens:** The new `:143` rule attaches the reason to the token: "On `fence-empty` the bullet also carries the header's reason." A round-≥2 fence-out is not `fence-empty`, so the brief's only interview record is `Interview: 2 rounds, exit empty-frontier` — byte-identical to a fully-visited tree. The operator's brief asserts a clean exhaustion while a whole subtree was dropped below altitude, and the reason line that Design 3 just made load-bearing is discarded at the one place it would have been persisted. `/spec-cycle` then reviews that brief as authority.
**Why the spec misses it:** Design 3 was widened for the primitive's reason line; Design 6 keys the caller's bullet on the exit *token*, and the two were not re-read against each other after the fold.
**Suggested fix:** Key the clause on the reason, not the token — same length, inside the line already being rewritten: "When the header's reason is `no candidate decision met the altitude fence`, the bullet also carries it: `Interview: 1 round, exit fence-empty (no candidate decision met the altitude fence)` or `Interview: 2 rounds, exit empty-frontier (no candidate decision met the altitude fence)`." Row 11's assertions still hold.

---

### F-7: "on `fence-empty` its three sections are empty" discards the grounding facts the caller supplied in `seed`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3, `:247–248` and § Design 2, `:220`
**Edge case:** `/spec-brief` reaches `fence-empty` after a Phase 1 that read files and dispatched explorations — the normal case, since Phase 1 always assembles "the problem statement, **the facts with their sources**" into `seed` (`skills/spec-brief/SKILL.md:82`).
**What happens:** `### Facts established` is the *only* route from the interview back into the brief's `## References` and `## Scope` rows (`spec-brief:141–142`), and `grilling:78` says "Facts, with their source paths, are carried into the hand-off" — including the retrieval-first ones consulted from `seed`. Forcing all three sections empty therefore drops facts that *were* established, on a path the spec deliberately writes a brief for. The brief then claims no grounding at all, and § Risks 2 records that outcome ("no fact References") as accepted without noticing that the facts existed. If instead the primitive never echoes seed facts, then `/spec-brief` loses its Phase-1 facts on *every* exit — a larger, pre-existing problem this spec would be worth flagging rather than silently depending on.
**Why the spec misses it:** Brief decision 4 says "empty sections" and Design 3 transcribed it as "all three"; the natural reading of the brief is "nothing was settled and nothing is open", which is about the two frontier sections.
**Suggested fix:** Two blockquote words, inside text already being written and not asserted by any checklist row: Design 3 → "on `fence-empty` its Settled and Open frontier sections are empty; `### Facts established` still carries any fact the seed supplied or a dispatch returned." Design 2's bullet → "On `fence-empty` Settled and Open frontier are empty." Update § Risks 2's "no fact References" clause accordingly.

---

### F-8: The `:108` edit removes the only sentence that put a fact-blocked question into the Open frontier on `stop`
**Severity:** P3
**Where:** spec § Design 3, `:251–253`
**Edge case:** `stop` while an exploration is in flight and a downstream question is waiting on it (`grilling:74`, "Questions downstream of a fact wait for it").
**What happens:** v1's `:108` ("their questions are Open with `unresolved because: stopped`") was the explicit exception to `:63`'s "Only questions actually rendered to the operator ever become named Open items" — it is what made an unrendered, fact-blocked question survive into the hand-off. The replacement clause names only the fact need, so the waiting question falls back under `:63` and is not rendered at all. The operator keeps the actionable F-item, but the brief loses one open branch, and the new `blocked-on: F<n>` reason value loses the producer this case would have given it. Legal output either way; the loss is a branch the spec author never sees.
**Why the spec misses it:** correctness/F-9's suggested fix was transcribed as a swap ("their questions" → "their fact needs") rather than an addition.
**Suggested fix:** Make it additive rather than substitutive: "…in-flight explorations are abandoned, their fact needs are Open `F<n>` items with `unresolved because: stopped`, and any question that was waiting on one is Open with `unresolved because: blocked-on: F<n>`." That is the reason value Design 2 already adds, so it introduces no construct — and it gives `blocked-on: F<n>` a named producer.

## Summary
P0: 1 | P1: 2 | P2: 4 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=2 P2=4 P3=1 P4=0
