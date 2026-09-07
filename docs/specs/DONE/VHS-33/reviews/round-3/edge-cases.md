# Edge-Cases Review — round 3

Grounding complete. Read from disk: the spec, the brief, `CLAUDE.md` + `AGENTS.md`, all three round-2 reports, all five target files (`skills/grilling/SKILL.md` in full, `skills/spec-cycle/SKILL.md` §§ 2e/2f/2f-i/failure-modes, `skills/spec-brief/SKILL.md` Phases 1–4, `skills/grill-me/SKILL.md`, `docs/spec-workflow-reference.md`), `docs/specs/DONE/VHS-32/spec.md` rows 3–7, and `lint.py`'s rule set. Anchors re-verified at HEAD (`:504`, `:539`, `:549`, `:366`, `:453` in spec-cycle; `:138–143` in spec-brief; `:23`/`:35` in the workflow reference). Plane lookup: skipped in favour of the brief + ticket text already in context (namespace `skills`); no grounding gap resulted. Every checklist row walked against the text the Designs pin — I could not find an unsatisfiable row this round (rows 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16 all check out; row 7's `≥ 7` is exactly met, row 6's `≥ 3` is exactly met, row 16 now returns 0 after the `:140` blockquote was trimmed).

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Row 7 `grep -c 'ref:' ≥ 8` unmeetable | CLOSED | spec § Test plan row 7 (`:443–445`) — `≥ 7`, "matching lines, not occurrences"; the seven sites enumerate exactly |
| conventions | F-2 | Additions roll-up incomplete | CLOSED | roll-up now seven bullets (`:60–85`), incl. F-numbering-at-need-time and `rounds: 1/<round_cap>`; D7 declares its own supersessions (`:134–135`) |
| conventions | F-3 | Wiki decision narrowed but unnamed | CLOSED | D4 `:114–115` + Risks 2 `:540–545` ("`/spec-close` records the narrowing") |
| conventions | F-4 | Roll-up's both-lists rule narrower than Design 5 | CLOSED | `:68–71` — "rather than `dispositioned` (it may still appear under `deferred to option 3`)" |
| conventions | F-5 | D7 omits VHS-32 row 6 | CLOSED | `:133` — "supersede VHS-32 rows 4, 6 and 7" |
| correctness | F-1 | Row 7 unsatisfiable | CLOSED | same edit as conventions/F-1 |
| correctness | F-2 | No `ref:` descent clause for F-items | CLOSED | Design 1 `:189–190` — "a fact request from the question whose need raised it (or from the seed items directly…)"; row 7 asserts the phrase |
| correctness | F-3 | D5 cites `:555–560` | CLOSED | `:119` now `:556–561`; agrees with `:345` and § References |
| correctness | F-4 | `:151` stale after the `:108` edit | CLOSED | Design 3 `:274–277` edits `:151` in step; fence narrowed to `:136–150`; row 6 asserts `:151` |
| correctness | F-5 | D13's `question_cap` justification wrong | CLOSED | D13 `:165–167` restated as the no-change claim |
| edge-cases | F-1 | `:140` blockquote trips row 16 | CLOSED | Design 6 `:356–361` — blockquote ends at "spec author pins this`."; rationale moved to spec prose. Row 16 re-walked over all eight blockquotes: 0 matches |
| edge-cases | F-2 | Row 7 `≥ 8` | CLOSED | as conventions/F-1 |
| edge-cases | F-3 | F-items had no descent rule | CLOSED | as correctness/F-2 |
| edge-cases | F-4 | `:151` contradicts the edited `:108` | CLOSED | as correctness/F-4 |
| edge-cases | F-5 | Seeded id on no item is in no list | CLOSED | Design 5 `:325–328` + row 10 ("not the full red list") |
| edge-cases | F-6 | `:143` keyed on the token, not the reason | CLOSED | Design 6 `:365–370` — both the fence-empty and the round-2 `empty-frontier` examples |
| edge-cases | F-7 | fence-empty discards seed facts | **PARTIAL** | Design 3 `:267–268` no longer empties the section, but its shipped rationale ("normally empty too, since no round was rendered and no dispatch ran") still directs the drop → **F-2 below** |
| edge-cases | F-8 | `:108` edit was substitutive | CLOSED | Design 3 `:272–274` — "and any question that was waiting on one is Open with `unresolved because: blocked-on: F<n>`" |

Round-1 deferred items (edge-cases F-6, F-8, F-15, F-18; correctness F-11) remain recorded in § Deferred (P2+) with their reasons — unchanged and still correctly fenced.

## Findings

### F-1: Design 7 deletes the workflow reference's only record of a round-≥2 fence-out, asserting the opposite of the `:106` this same spec ships
**Severity:** P1
**Where:** spec § Design 7, `:385–391` (the `docs/spec-workflow-reference.md:23` replacement), against § Design 3, `:262–265` and § Design 6, `:368–370`
**Edge case:** Round 1 settles decisions; round 2's recomputed frontier has candidates but every one falls below the altitude fence. Exit is `empty-frontier` with reason `no candidate decision met the altitude fence` — the case Design 3 was deliberately widened to name when round-1 edge-cases/F-4 was folded, and the case Design 6's `:143` gives a worked example for in the same PR.
**What happens:** The current file text is accurate today:

> An emptied frontier means the tree was fully visited **(or nothing met the altitude fence)** — the brief carries no open items.

Design 7 replaces it with "An emptied frontier means the tree was fully visited — the brief carries no open items. A fence-empty exit means nothing met the altitude fence **in round 1** …". The parenthetical is deleted and the fence reason is re-attributed exclusively to `fence-empty`. After the change the repo's only prose paraphrase of the contract states that `empty-frontier` ⇒ tree fully visited, while `skills/grilling/SKILL.md:106` (this spec's own Design 3) states that `empty-frontier`'s reason line distinguishes the two, and `skills/spec-brief/SKILL.md:143` (this spec's own Design 6) hard-codes the counter-example `Interview: 2 rounds, exit empty-frontier (no candidate decision met the altitude fence)`. The three shipped files disagree in one PR, and the one that is correct today becomes the one that is wrong. A reader who hits that brief bullet has no document that explains it; the drop of a whole below-altitude subtree reads as clean exhaustion. This is a net regression, not an omission: information present at `7403cb5` is removed by this edit.
**Why the spec misses it:** Design 7's `:23` was written as "add the sixth exit to the list of termination shapes", and the sentence being edited already carried the fence case for a *different* token. Design 3's widening and Design 6's fold both landed after; nothing re-read `:23` against them. Row 13 asserts only that `:23` contains `fence-empty`, so the gate cannot catch it, and § Done when's "the workflow reference's paraphrase matches" is the criterion it fails.
**Suggested fix:** Keep the parenthetical, inside the sentence already being rewritten — no new construct, no length change worth counting: "An emptied frontier means the tree was fully visited, **or that a later round's remaining candidates all fell below the altitude fence** — the brief carries no open items. A fence-empty exit means nothing met the altitude fence in round 1 — the brief is written with no decisions and the reason recorded." Add to row 13: `:23` contains both `fence-empty` and "altitude fence" twice, or assert that the sentence still names the fence case for an emptied frontier.

---

### F-2: Design 3's shipped rationale tells the primitive that `### Facts established` is empty on `fence-empty`, dropping every fact `/spec-brief` put in the seed
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3, `:267–268`, and § Risks 2, `:536` (PARTIAL closure of round-2 edge-cases/F-7)
**Edge case:** `/spec-brief` reaches `fence-empty`. Phase 1 always assembles `seed` as "the problem statement, **the facts with their sources**, and any related open tickets" (`skills/spec-brief/SKILL.md:82`), so on this path the seed carries established facts and the interview renders no round.
**What happens:** The blockquote that ships into `:106` now reads "…and `### Facts established` is rendered as on any exit — **normally empty too, since no round was rendered and no dispatch ran**." The first clause fixes F-7; the trailing rationale re-imposes it, because it names *dispatch* as the only source of facts. `grilling:78` says the opposite — "Retrieval-first: if the caller supplied wiki or state context in `seed`, consult it before dispatching. **Facts, with their source paths, are carried into the hand-off.**" A primitive following the new sentence renders an empty Facts section, and `### Facts established` is the only route from the interview into the brief's `## References` (`spec-brief:142`) and into `## Scope` rows (`:141`, "`Current` filled from a fact with its `path:line`"). The brief then asserts no grounding at all for a run that read files and dispatched explorations, and Risks 2 encodes the same error as accepted ("normally no fact References"). The failure is silent: nothing prints a warning about dropped facts, and `Interview: 1 round, exit fence-empty (…)` reads as a complete record.
**Why the spec misses it:** F-7's ask ("still carries any fact the seed supplied or a dispatch returned") was folded as a scope narrowing of the *empty sections* claim; the explanatory half-sentence added alongside it re-states the removed rule as a reason.
**Suggested fix:** Two clauses, both inside text already being written, no new construct. Design 3: "… and `### Facts established` is rendered as on any exit — **empty unless the seed supplied facts or a dispatch returned one**." Risks 2: drop "normally" from "normally no fact References" and say instead "no fact References beyond the ones Phase 1 already had". Optionally add to row 6: the `:106` paragraph does not say the Facts section is empty.

---

### F-3: One finding id carried by two Settled items — one applied, one not — prints under `dispositioned` *and* `deferred to option 3`
**Severity:** P2
**Where:** spec § Design 5, `:321–329` (the step-5 construction rules), against `skills/spec-cycle/SKILL.md:539–546` (step 4)
**Edge case:** A grill settles two decisions that both name finding `edge-cases/F-3` in `ref:`. Step 4 applies the first as an in-place spec edit; the second cannot be discharged in place ("narrow the brief" — step 4's own stated example) and is reported as deferred.
**What happens:** The four lists are now defined purely mechanically. `dispositioned` = "every id on a Settled item that step 4 applied"; `deferred to option 3` = "ids on Settled items step 4 could not apply". Both clauses match, so the id prints in both lists on the same line — while step 4 leaves the finding P0/P1 and the re-rendered halt block simultaneously suffixes its title " — grilled (spec edited; not re-reviewed)". The operator reads one line saying a finding was both dispositioned and deferred, with no rule saying which wins; the honest state (still red, partly edited) is exactly the state the both-lists rule was written to make legible for the Settled∩Open case, and the sibling case was not walked. The brief's Risk 1 asked the spec author to pin precisely this line ("what the step 5 line prints when one Settled decision carries several `ref:` ids"), and this is the one partition cell left unassigned after round 2's fold of edge-cases/F-5.
**Why the spec misses it:** The both-lists rule was derived from the *semantic* case (settled-but-still-questioned) and stated only for Settled∩Open; the applied∩unapplied overlap arises from step 4's pre-existing deferral path, which Design 5 does not otherwise touch.
**Suggested fix:** This needs a clause, and "extra step-5 clauses" is named in brief decision 12 as an attempt-1 accretion — so route it, do not fold it. Add to § Deferred (P2+) with the rule to adopt if wanted, in the shape the existing four bullets use: "**edge-cases R3 F-3** (P2) — an id on both an applied and an unapplied Settled item prints under `dispositioned` and `deferred to option 3`. Not folded: a precedence clause is the reason-precedence construct brief decision 12 removed. The rule to adopt if wanted: the same precedence as the both-lists rule — an id on any unapplied Settled item prints under `deferred to option 3` only, since the finding stays P0/P1." One sentence in § Risks would also discharge it.

---

### F-4: A returned summary with no `ref:` fields at all has no step-4 rule, and "never by title" forbids the only fallback
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 5, `:305–308` (step 4) and `:331–332` (the `unreferenced decisions applied` bullet)
**Edge case:** 2f-i seeds with lens-qualified ids (it always does), and the primitive returns a v1-shaped block — every `ref:` field missing rather than present with the value `none`. The primitive is a prompt executed by a model across a skill boundary; `grilling`'s own contract makes the field conditional ("renders … when any seed item carried an `id`, and on none otherwise"), so a v1-shaped return is the natural malformed-response mode for this change, and it is the one shape step 3's guard does not check (the guard tests only for a `## Grill summary` line).
**What happens:** Step 4's shipped rule is "Locate the finding(s) a decision dispositions by its `ref:` ids, **never by title**", and the only stated tolerance is for the literal value `ref: none`. With the field absent there is nothing to locate by and the v1 fallback is forbidden, so every Settled item is applied as a spec edit while dispositioning no finding: the spec is edited, `dispositioned` prints empty, every seeded finding stays P0/P1, and the one grill per halt is spent. The direction is conservative (nothing is falsely marked green) and `unreferenced decisions applied: <n>` prints a non-zero count against an empty `dispositioned` list — so the shape is self-diagnosing — but nothing in the spec says that combination means "the primitive dropped the ids", and the operator's halt block shows nothing moved while `grill.md` records edits that did.
**Why the spec misses it:** `ref:` was reasoned about as present-or-`none`, the two states the primitive's contract produces when followed. External-response malformation on the new field was not walked; round 1's F-6 covered an *unknown* id, not an absent field.
**Suggested fix:** Complete the sentence the spec already writes — a clause, not a construct, and it stays inside D12: "A Settled item with `ref: none` — **or with no `ref:` field at all, which is what a v1-shaped return looks like** — is applied as a spec edit like any other but dispositions no finding." Optionally one clause on the count bullet: "a non-zero count against an empty `dispositioned` list means the returned block carried no ids." Row 10 already asserts the step-4 string, so extend it to the new wording.

---

### F-5: `ref:` ids do not survive a `prior_summary` resume — the descent rule is keyed on seed items only
**Severity:** P3
**Where:** spec § Design 1, `:185–192` (the `ref:` paragraph), against `skills/grilling/SKILL.md:21`, `:23` (fenced by § Files to leave alone) and `skills/spec-brief/SKILL.md:105`
**Edge case:** An id-supplying caller resumes with `prior_summary` + a Q number after a cap hit.
**What happens:** The shipped rule renders `ref:` "when any seed item carried an `id`, and on none otherwise", and derives every item's ids from *seed items*. The resume contract says "Rebuild the tree from the summary" and never mentions the seed; `/spec-brief:105` re-invokes with `prior_summary` and the bounds, saying nothing about re-passing `seed`. So on the resume round the primitive has a summary whose items carry ids and a rule that reads ids from a seed it may not have — and the omission branch ("on none otherwise") makes the silent outcome a block with every `ref:` dropped, i.e. a v1-shaped return in the shape F-4 describes. Unreachable today: 2f-i is the only id-supplying caller and has no resume path; `/spec-brief` and `/grill-me` pass no ids. It becomes reachable the moment a fourth caller supplies ids, or 2f-i gains a revise option.
**Why the spec misses it:** `:23` is fenced in § Files to leave alone (correctly — it is VHS-32's resume contract), so the resume path was not walked against the new field.
**Suggested fix:** Do not fold — a resume rule is adjacent to what brief decision 11 fences. Add to § Deferred (P2+): "**edge-cases R3 F-5** (P3) — `ref:` ids are undefined across a `prior_summary` resume. Not folded: a resume rule for the new field, on the same fence as the F-item resume rule. The rule to adopt if wanted: on a resume, an item's ids carry over from the prior summary's own `ref:` fields. Unreachable today — 2f-i is the only id-supplying caller and never resumes." Same disposition class as the already-deferred F-18.

---

### F-6: `grill applied (exit: <token>)` has no defined value when the returned header carries no readable token
**Severity:** P3
**Where:** spec § Design 5, `:313`, `:318`
**Edge case:** The primitive returns a block whose `## Grill summary` line is present (so step 3's guard passes and the block is persisted verbatim) but whose header is truncated, reworded, or missing its `exit:` field — a host cutting the response at the header, or a primitive that renders the header prose-style.
**What happens:** Step 5's line is now `grill applied (exit: <token>): …` and `<token>` is defined only as "the exit from the summary header". With no token the line prints `grill applied (exit: ):` or an invented value. The token is load-bearing by this spec's own design — "the `fence-empty` token is the signal that nothing was askable and every seeded finding remains P0/P1" — so an empty or improvised token is exactly the case where the operator most needs to distinguish "nothing was askable" from "the interview was cut short". Degrades gracefully (the lists still print and findings stay P0/P1), which is why this is not P1.
**Why the spec misses it:** The token was added as a uniform read of a field the contract always renders; the malformed-header branch of step 3's guard was not re-walked after step 5 gained a dependency on the header.
**Suggested fix:** Cheapest correct form is one clause on the `<token>` bullet, and it is not a new step-5 list: "`<token>` is the exit from the summary header; when the header carries none, print `unknown` — the persisted block is the record." If that reads as a sixth clause, route it to § Deferred with the same rule.

---

### F-7: Row 9's "`:132` is byte-identical" names a line number the `ref:` paragraph insertion shifts
**Severity:** P4
**Where:** spec § Test plan row 9, `:453`
**Edge case:** Running the row literally after the change, rather than against the pre-edit file.
**What happens:** Design 1 inserts the `ref:` paragraph between `:130` and `:132`, so the size-bound sentence lands at `:134` post-change. The row's range list is explicitly qualified "of the pre-edit file", but the `:132` sentence sits after that qualifier and reads on its own as a post-change line check, which would find the newly inserted paragraph there. No behavioural consequence — the diff-based reading is the obvious one, and the sentence is true under it.
**Why the spec misses it:** The qualifier was attached to the four ranges when they were the whole row; `:132` was appended later.
**Suggested fix:** "the pre-edit `:132` (the size-bound sentence) is byte-identical", or fold it into the range list as "and `:131–135`".

## Summary
P0: 0 | P1: 1 | P2: 3 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=3 P3=2 P4=1
