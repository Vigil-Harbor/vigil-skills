# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Checklist row 8 is unsatisfiable — the paragraph it gates contains digits
**Severity:** P0
**Where:** `docs/specs/TODO/VHS-33.spec.md:372–374` (Test plan row 8), against Design 4 at `:238–243`
**Edge case:** The gate row asserts a property of a string the spec itself drafts, and the drafted string violates it.
**What happens:** Row 8 requires the `**Plain language.**` paragraph to contain the literal `ASD-STE100` **and** to contain "no digit". `ASD-STE100` contains `100`; the paragraph's own example identifier `2f-i` contains `2`. `## Test command` is `N/A` and the spec states "the checklist is the `/ship-spec` gate" (`:339–341`), so this row can never pass and blocks the ship gate deterministically — not on a rare input, on every run.
**Why the spec misses it:** Design 4's closing line is "That is the whole rule. No sentence count, no preamble slot." (`:245`). The intent of "no digit" is plainly "no sentence-count number", but row 8 was written as an unqualified whole-paragraph assertion while row 8 simultaneously pins two digit-bearing literals.
**Suggested fix:** Rewrite row 8's last clause to assert what Design 4 actually decided, e.g. "…and states no sentence count (no bare numeral quantifying sentences or glosses; `ASD-STE100` and `2f-i` are identifiers, not counts)." Or drop the clause and rely on row 9's no-hunk fences.

---

### F-2: Two of the five named causes of an Open F-item never produce a rendered `F<n>` number
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-33.spec.md:191–195` (Design 2, the F-item bullet)
**Edge case:** A fact need that reaches the hand-off unresolved without ever having been rendered to the operator as an `ℹ️` request.
**What happens:** Design 2 ends the bullet with "It keeps the `F<n>` number it was rendered with," but two of the five causes it lists are, by construction, never rendered:
- **dispatch-cap overflow** (`skills/grilling/SKILL.md:74`) — overflow fact needs "carry to the next round's batch" as *dispatches*, not as rendered `ℹ️` items; if the interview ends first they reach the hand-off directly.
- **stopped** (`:108`) — "in-flight explorations are abandoned"; an in-flight exploration was dispatched silently, never rendered.

The renderer then has no number for a shape whose form requires one (`**F<n> — <fact needed>**`). It either invents one — risking collision with the `### Facts established` series, which shares the same `F1…Fn` sequence per `:48` — or emits `F?`. Either way `blocked-on: F<n>` on the waiting Q-item (the new reason value this spec adds at `:196–199`) points at a number that does not resolve, which defeats the exact determinism goal that motivates the whole ticket.
**Why the spec misses it:** Design 2 assembles the cause list from `:72`, `:74`, `:76`, `:88` and `:108` and then attaches a numbering claim that is true only for the rendered subset (`:72`, `:76`, `:88`).
**Suggested fix:** One wording change inside Design 2, no new construct — the existing contract already implies numbers exist for unrendered dispatches (`:129` shows established facts as `F1 — <fact>`, and established facts come from dispatches, not from rendered requests). Replace "It keeps the `F<n>` number it was rendered with" with "It carries its number from the parallel `F1…Fn` series (`:48`), whether or not it was rendered as an `ℹ️` request."

---

### F-3: `fence-empty` writes a hollow brief that downstream lenses then treat as authority
**Severity:** P2
**Where:** `docs/specs/TODO/VHS-33.spec.md:308–309` (Design 6, "`fence-empty` is not `empty-seed`")
**Edge case:** `/spec-brief` receives a `fence-empty` summary: zero Settled, zero Open, zero Facts.
**What happens:** The spec decides Phase 2 does not halt. Following `skills/spec-brief/SKILL.md` mapping rules with an all-empty block:
- `:139` writes `_(none settled — see Risks / decisions)_` under `## Decisions carried forward` and prints "the brief pins everything to the spec author" — but
- `:140` produces an **empty** `## Risks / decisions`, so the sentinel points at nothing and the warning is false;
- `:141` gives `## Scope` **no rows** (no settled decisions, no facts);
- `:142` gives `## References` no fact bullets.

The result is a brief with a Problem paragraph and four empty sections. `skills/spec-brief/SKILL.md:88` states the rationale this spec's decision runs against verbatim: "A success token for 'nothing was ever known' would write a hollow brief that every downstream lens then treats as authority." `/spec-cycle`'s parser (`skills/spec-cycle/SKILL.md:640`) then sees a *present-but-empty* Decisions list, so the missing-header fallback does not fire — the spec itself defers that at `## Out of scope` item 10, which means nothing catches it either.
**Why the spec misses it:** D4/Design 6 reason about the exit token's routing (fence-empty ≠ empty-seed) and stop at `:139`'s empty-Settled rule, without walking the other three mapping rules with the same empty input.
**Suggested fix:** The direct fix — halting or a distinct Phase 2 branch — lands in `skills/spec-brief/SKILL.md:84–90`, which this spec's `## Files to leave alone` fences ("Phase 2 keeps halting on `empty-seed` only"), and would be a new construct under brief decision 12. Rate it against the fence: **do not fold**. Record it in `## Risks` as an accepted outcome (one entry: "a `fence-empty` brief is written with four empty sections; the References bullet carrying the reason is the only signal, and `/spec-cycle`'s present-but-empty parse is out-of-scope item 10"), or file it with VHS-34/its own ticket.

---

### F-4: The new `empty-frontier` sentence asserts something false for a round-≥2 fence-out
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:224–227` (Design 3's `:106` replacement)
**Edge case:** Round 1 settles a decision; round 2's recomputed frontier has candidates, but every one of them fails the altitude fence.
**What happens:** `fence-empty` is scoped to round 1 only ("no *round-1* candidate satisfies the altitude fence"), so this state cannot use it. The replacement text asserts `empty-frontier` "means the tree was fully visited" — which is false here: the tree has unvisited candidates that were fenced out. The block then reports `exit: empty-frontier; reason: tree fully visited`, and `/spec-brief` writes a brief with settled decisions, an empty `## Risks / decisions`, and a References bullet claiming the tree was exhausted. The operator has no signal that a whole subtree was dropped below altitude.
**Why the spec misses it:** v1's `:106` never asserted a *meaning* for `empty-frontier` — it only said the exit was "reachable only after at least one round was rendered". Design 3 adds "and means the tree was fully visited" as part of moving the fence reason to the new token, tightening a sentence that was previously loose enough to cover this path.
**Suggested fix:** One clause, inside the sentence Design 3 is already rewriting. Either soften — "`empty-frontier` is reachable only after at least one round was rendered; its reason line distinguishes `tree fully visited` from `no candidate decision met the altitude fence`" — or add the explicit carve-out: "…means the tree was fully visited, or that its remaining candidates all fell below the fence, which the reason line names." The reason list in the header is unchanged either way (row 4 still holds).

---

### F-5: The both-lists rule, read literally, also suppresses `deferred to option 3`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:269–272` (Design 5, step-5 `left open` bullet)
**Edge case:** One finding id appears on a Settled item that step 4 **could not apply** *and* on an Open item.
**What happens:** The rule reads "An id that appears on both a Settled and an Open item is listed here only." Taken literally, "here only" excludes it from every other list — including `deferred to option 3`, which is the operator's only prompt that menu option 3 (narrow the brief) is required for that finding. The id then prints under `left open` and the operator reads it as "the grill did not reach it" rather than "a decision was settled but needs option 3." The intended contrast is `left open` vs `dispositioned` (the neighbouring bullet), not vs all four lists.
**Why the spec misses it:** The bullet's justification sentence names only the dispositioned case ("a finding is not dispositioned while any question about it is open"), so the scope of "here only" was never re-read against the `deferred to option 3` bullet two lines down.
**Suggested fix:** Two words in Design 5: "…is listed under `left open` rather than `dispositioned`; it still appears in `deferred to option 3` if step 4 could not apply its Settled item." This completes the brief's Risk-1 pin rather than adding a construct, so it is inside the fence.

---

### F-6: A `ref:` id that matches no seeded finding has no step-4 rule
**Severity:** P2
**Where:** `docs/specs/TODO/VHS-33.spec.md:256–258` (Design 5, step 4)
**Edge case:** The returned block carries a `ref:` id that is malformed, is a `not grillable` id (never seeded), or is simply wrong — the primitive's output is LLM-rendered prose, not a validated schema.
**What happens:** Step 4 says "Locate the finding(s) a decision dispositions by its `ref:` ids, never by title," and defines only the `ref: none` case. With an unknown id there is no rule: the spec edit is applied anyway, the unknown id is printed under `dispositioned`, and step 5's "each dispositioned title suffixed ` — grilled (spec edited; not re-reviewed)`" (`skills/spec-cycle/SKILL.md:550–552`) has no title to suffix — so a spec edit lands at round 4 attributed to a finding that does not exist and is invisible in the re-rendered halt block. Under v1's title-matching, a bad title at least degraded to human recognition; the `ref:` path removes the fallback without adding a check. This is the same failure class (silent mis-attributed edit, no downstream reviewer to catch it) the brief names as item 1's real failure mode.
**Why the spec misses it:** The design reasons from the trusted direction (2f-i supplies the ids, so they must come back) and never treats the primitive's block as untrusted output.
**Suggested fix:** A step-4 validation sentence is close to the "seed-id legality rule" attempt 1 accreted and brief decision 12 forbids — rate it against the fence and **do not fold**. Record it in `## Deferred (P2+)` as `edge-cases/F-6` with the concrete rule the operator can adopt at the halt: "a `ref:` id matching no seeded finding is treated as `ref: none` — the edit is applied and counted in `unreferenced decisions applied`, and the id is not printed under `dispositioned`."

---

### F-7: On `fence-empty` the step-5 line prints `left open` empty while every seeded finding is in fact left open
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:277–280` (Design 5, fence-empty bullet)
**Edge case:** `fence-empty` returns to 2f-i.
**What happens:** The spec says "On `fence-empty` every list is empty and the line still prints; the findings stay P0/P1 untouched." The rendered line is then `grill applied (exit: fence-empty): dispositioned ; left open ; not grillable ; deferred to option 3 — docs/…`. But every seeded finding *is* open — they stayed P0/P1 and none was dispositioned. The one line the operator reads at the halt to see what moved reports the opposite of the truth for its most load-bearing field, and it consumed the once-per-halt grill (D5) so there is no retry. The exit token in the same line is the only disambiguator, and D5's whole point is that the operator must understand the bound was spent.
**Why the spec misses it:** The bullet reasons from the mechanical rule ("`left open` lists every id on an Open item"; there are none) rather than from what the line communicates.
**Suggested fix:** One clause on that bullet, no new construct and no sentinel (which the fence forbids): "…the line still prints with every list empty — the `fence-empty` token is the signal that nothing was askable and every seeded finding remains P0/P1; the empty `left open` is not a claim that nothing is open." Alternatively add the same sentence to the `:698–703` failure-modes edit, which already says "nothing moved."

---

### F-8: An unreferenced Settled item that step 4 could not apply appears in no step-5 list
**Severity:** P2
**Where:** `docs/specs/TODO/VHS-33.spec.md:273–276` (Design 5, `deferred to option 3` and `unreferenced decisions applied` bullets)
**Edge case:** A Settled decision with `ref: none` that step 4 cannot discharge by an in-place spec edit (`skills/spec-cycle/SKILL.md:542–545`, e.g. "narrow the brief").
**What happens:** `deferred to option 3` "lists ids on Settled items step 4 could not apply" — this item has no ids. `unreferenced decisions applied: <n>` "counts Settled items with `ref: none` that step 4 **applied**" — this one was not applied, and the clause is omitted entirely when `n` is 0. So the decision vanishes from the step-5 line altogether. It survives only inside `grill.md` as Settled-but-unapplied — but the step-5 line exists precisely "so the operator can see what moved without opening `grill.md`." The operator is then never told that option 3 is required.
**Why the spec misses it:** The two bullets partition on different axes (has-ids vs applied) and the empty intersection cell was not walked.
**Suggested fix:** Adding a sixth clause is exactly the "extra step-5 clauses" brief decision 12 fences off — rate against the fence and **do not fold** as a new clause. The in-fence alternative is one word on the existing bullet: change `deferred to option 3` to "lists ids on Settled items step 4 could not apply; an item with `ref: none` in that state is counted there as `(unreferenced)`". If even that reads as an addition, record it in `## Deferred (P2+)` as `edge-cases/F-8`.

---

### F-9: Checklist row 13 forbids the change Design 7 requires
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:391–392` (Test plan row 13), against Design 7 at `:319–335`
**Edge case:** The gate row is evaluated literally against the diff Design 7 produces.
**What happens:** Row 13 reads "`grep -c 'fence-empty' docs/spec-workflow-reference.md` ≥ 1; `:35` contains `ref:` and 'unestablished fact'; **no other line of the file changes**." Design 7 changes both `:23` and `:35`, and the `fence-empty` string the row's first clause requires lives at `:23` — the `:35` rewrite contains no `fence-empty`. So satisfying clause 1 necessarily violates clause 3. A ship-gate reader applying the row as written fails it.
**Why the spec misses it:** The row was written from `:35`'s perspective and "no other line" was meant as "no line beyond the two Design 7 names."
**Suggested fix:** "…no line other than `:23` and `:35` changes; `:23` contains `fence-empty`."

---

### F-10: The only justification anchor for the one spec-level addition points at the wrong line
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:55–57` (Decisions roll-up) and `:464` (References)
**Edge case:** A `/ship-spec` implementer verifies the sole justification for the lens-qualified seed-id form before writing it.
**What happens:** Both places claim the form is "the form 2b's closure manifest already uses at `skills/spec-cycle/SKILL.md:349`". Line 349 is `- round_number: <N>` — a reviewer-prompt parameter. The actual closure-manifest form is at `skills/spec-cycle/SKILL.md:366`:

```
  - <lens>/<finding-id> (P<sev>) "<title>" — <how addressed, with spec § anchor>
```

and 2f-i itself already uses `<lens>/<id>` at `:504`. Given brief decision 12 fences spec-level additions and this is the first item on the additions roll-up, an unverifiable anchor is exactly what a drift-check would trip on — the implementer either invents a form or stalls.
**Why the spec misses it:** Anchors were read at `7403cb5` (Risk 4) but this one was recorded off by seventeen lines, landing inside the reviewer-prompt parameter list.
**Suggested fix:** Change both occurrences of `:349` to `:366`, and add `:504` (`not grillable: <lens>/<id>`) as the in-2f-i precedent — it makes the addition self-evidently a reuse.

---

### F-11: `/spec-brief` Phase 3 offers "revise an answer by Q number" after `fence-empty`, when no Q exists
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:44` ("Phase 3 (`:92–107`) is unchanged"), against `skills/spec-brief/SKILL.md:94–105`
**Edge case:** `fence-empty` → Phase 3.
**What happens:** The preview renders two empty lists, and the menu still offers "2. Revise an answer (name the Q number)". No Q number exists. If the operator picks 2, the resume contract (`skills/grilling/SKILL.md:23`) is handed a `prior_summary` with no Settled items and a Q number that names nothing — "Settled items stay settled except the named one" has no referent, and the primitive most likely re-runs the interview against the same fence, producing `fence-empty` again and burning another round.
**Why the spec misses it:** The spec correctly notes fence-empty is not empty-seed for Phase 2, then declares Phase 3 unchanged without walking the empty case through the menu.
**Suggested fix:** Pre-existing (a fence-out already reached this menu under v1's `empty-frontier` reason line), so this spec does not create it — **do not fold**; the fix lands in the fenced Phase 3 region. Add it to `## Out of scope` beside item 11 (the sibling post-cap-resume-renders-zero item) with its own ticket, or note it under Risks.

---

### F-12: The `rounds:` value on a `fence-empty` header is never pinned, and Design 6 hard-codes one
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:224–227` (Design 3) vs `:304–306` (Design 6)
**Edge case:** Rendering the hand-off header when "nothing is rendered".
**What happens:** Design 3 says on `fence-empty` "nothing is rendered"; Design 6's example bullet asserts `Interview: 1 round, exit fence-empty (…)`. Nothing states whether the header renders `rounds: 0/3` or `rounds: 1/3`. Three consumers read that field: `/spec-brief:143` (the References bullet), `/spec-brief:159` (the terminal print), and the resume contract's `rounds_used` carry-over (`skills/grilling/SKILL.md:23`). An implementer choosing 0 makes Design 6's own worked example wrong.
**Why the spec misses it:** Design 3 reasons about items rendered, Design 6 about the caller's bullet, and neither owns the header's numeric field.
**Suggested fix:** One clause in Design 3, pinning an existing field rather than adding a construct: "the header renders `rounds: 1/<round_cap>` — the round was attempted and consumed."

---

### F-13: Three `spec-cycle` line anchors are off by one
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:249`, `:256`, `:286`, and `:465–466`
**Edge case:** `/ship-spec` re-reads anchors at implementation time (Risk 4's mitigation).
**What happens:** Verified against `7403cb5`, the commit the spec names:
- step 1's quoted string "extract each remaining P0/P1 finding: id, severity, title, body" spans `:495–496`, not `:494–495` (`:494` is the stale-`scalability.md` clause);
- step 4's "For each **Settled** item…" begins at `:539`, not `:538`;
- the closing paragraph is `:556–561`, not `:555–560`.

None breaks a gate row — row 10 only bounds hunks to `:489–561`, which holds — but each costs the implementer a re-read, and the spec asserts these were read at `7403cb5`.
**Why the spec misses it:** Off-by-one transcription; the quoted text is correct in every case, only the numbers drift.
**Suggested fix:** Correct the four numbers, or drop the sub-anchors and keep only `### 2f-i` (`:489–561`) plus the quoted strings, which are what row 10 actually checks.

---

### F-14: `left open` has no de-duplication clause, while `dispositioned` does
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:269–272`
**Edge case:** One finding id carried on two Open items (e.g. an open Q-item and the rolled-up deferred item both descending from the same seed).
**What happens:** `dispositioned` is specified as "each id once, in seed order"; `left open` says only "lists every id on an Open item". The id prints twice in the halt line. Cosmetic, but it undermines reading the line as a set of finding ids.
**Why the spec misses it:** The brief's Risk 1 pin (`brief:81`) specifies de-duplication only for `dispositioned`; the spec reuses it verbatim and does not extend it.
**Suggested fix:** Four words: "lists every id on an Open item (Q, F, or rolled-up), each id once, in seed order."

---

### F-15: `/spec-brief`'s F-item mapping flattens `stopped` to "not established"
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:297–299` (Design 6, `:140` replacement)
**Edge case:** The operator says `stop` with an exploration in flight; the F-item renders `unresolved because: stopped`.
**What happens:** The mapping writes it into `## Risks / decisions` as `<fact needed> — not established; spec author pins this`, losing the distinction between "the machinery tried and failed" and "the operator ended the interview before it ran". The spec author cannot tell whether re-dispatching would help.
**Why the spec misses it:** Design 6 writes one form for both of D3's two reason values.
**Suggested fix:** A cause qualifier is exactly what brief decision 12 fences ("no cause qualifiers") — rate against the fence and **do not fold**. If the operator wants it, it is a two-word variant (`— not established (interview stopped)`), which `skills/spec-brief/SKILL.md:80` already precedents with `(exploration failed)`; record as `## Deferred (P2+)` `edge-cases/F-15`.

---

### F-16: Row 16's VHS-36 fence greps a `git diff` whose non-content lines it also counts
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:397` (Test plan row 16)
**Edge case:** `git diff -U0` emits `@@ … @@ <context>` hunk headers whose trailing context is the nearest preceding line matching git's default funcname regex, and `grep -c` counts removed (`-`) lines as well as added ones.
**What happens:** The row demands a count of exactly `0` for `-ciE 'operator claim|verif|qualifier|source: operator'`. A hunk-header context line pulled from elsewhere in `skills/spec-brief/SKILL.md`, or a removed line, can match `verif` (`## Scope (verified against current files…)` is a real string in that file at `:141`) and fail the fence for reasons unrelated to VHS-36 scope. Because the checklist *is* the ship gate, a false positive here blocks the PR with a misleading "VHS-36 fence violated" signal.
**Why the spec misses it:** The row treats `git diff` output as if it contained only content lines.
**Suggested fix:** Restrict to added content: `git diff -U0 -- … | grep '^+' | grep -v '^+++' | grep -ciE '…'` → 0.

---

### F-17: Two rendering separators in the new block/line shapes are unspecified
**Severity:** P4
**Where:** `docs/specs/TODO/VHS-33.spec.md:178` (rolled-up Open line) and `:275–276` (clause omission)
**Edge case:** Assembling the strings.
**What happens:** (a) The rolled-up line becomes `**<parent title> — downstream decisions not explored (deferred at round <n>)** ref: <…>` — no period or separator between the bolded title and the field, unlike the other three lines which are preceded by `. ` or `; `. (b) "Omit the clause when `n` is 0" does not say the preceding `; ` goes with it, so a literal implementer can leave `…deferred to option 3 <ids>; — docs/…`.
**Why the spec misses it:** Both are assembly details below the level the design reasons at.
**Suggested fix:** Render the rolled-up line as `…(deferred at round <n>)** — ref: <…>`; add "with its leading `; `" to the omission rule.

---

### F-18: `ref:` id character legality is unspecified against a comma-separated list
**Severity:** P4
**Where:** `docs/specs/TODO/VHS-33.spec.md:158–163` (Design 1, Rendering)
**Edge case:** A caller supplies an id containing a comma, or an empty string.
**What happens:** `ref:` renders "the comma-separated ids", so an id containing a comma silently splits into two, and 2f-i step 5 then prints a phantom id. Not reachable today — the only id-supplying caller is 2f-i (Risk 1), whose ids are `<lens>/F-<n>` over a fixed four-lens vocabulary — so this is theoretical, and the fix is precisely the "seed-id legality rule" brief decision 12 removed from attempt 1.
**Why the spec misses it:** Deliberately, per the fence.
**Suggested fix:** None — rate against the fence and leave it. Noted only so a later reviewer does not re-derive it as a fold candidate.

## Summary
P0: 1 | P1: 1 | P2: 8 | P3: 6 | P4: 2

STATUS: RED P0=1 P1=1 P2=8 P3=6 P4=2
