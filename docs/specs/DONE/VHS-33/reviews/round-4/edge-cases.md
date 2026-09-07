# Edge-Cases Review — round 4

Grounding complete. Read from disk: the spec (`docs/specs/TODO/VHS-33.spec.md`), the brief, both `CLAUDE.md` files, all three round-3 reports, and all five target files (`skills/grilling/SKILL.md` in full, `skills/spec-cycle/SKILL.md` §§ 2f-i + failure modes, `skills/spec-brief/SKILL.md` Phases 1–4, `skills/grill-me/SKILL.md`, `docs/spec-workflow-reference.md:18–36`), plus `docs/specs/DONE/VHS-32/spec.md` rows 4/6/7 and `git log --name-status` on the spec artifacts. Plane VHS-33 retrieved from namespace `skills` (confidence 0.82); description matches the brief. `scale_lens == off` and no `scalability.md` exists in `round-3/` — nothing to ignore. Every checklist row walked against the text the Designs pin; rows 1–8, 11, 12, 13, 15, 16 all check out (row 6's `≥ 3` and row 7's `≥ 7` are each met exactly; row 16 returns 0 over all eight blockquotes).

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `:23` deletes the altitude-fence parenthetical | CLOSED | spec `:399–407` — "fully visited, or that a later round's remaining candidates all fell below the altitude fence — either way the reason line says which"; row 13 `:492–493` asserts "altitude fence" ≥2 and the phrase |
| correctness | F-2 | "byte-identical to v1" contradicts Design 2 | CLOSED | spec `:200–204` — narrowed to "the Settled and Open-question lines"; "The block as a whole still changes for every caller" |
| correctness | F-3 | `:106`'s "normally empty too" rationale | CLOSED | spec `:278–279` — "empty unless the seed supplied facts or a dispatch returned one"; Design 2 `:245–249`; Risk 2 `:558–559` |
| correctness | F-4 | Design 5 does not say which step-5 text ships | CLOSED (new defect → F-1 below) | spec `:328–330` adds "The code block replaces `:548–549`; the bullets below are added to step 5"; row 10 adds "is listed here rather than under `dispositioned`" + "in seed order" |
| correctness | F-5 | Row 10's bare `grep -c 'total_p0p1 == 0'` | CLOSED | spec `:471` now names `skills/spec-cycle/SKILL.md` |
| edge-cases | F-1 | `:23` asserts the opposite of the shipped `:106` | CLOSED | same edit as correctness/F-1 |
| edge-cases | F-2 | fence-empty drops seed facts | CLOSED | spec `:278–279`, Design 2 bullet `:245–249` ("for `/spec-brief`, which grounds first, that is normally not empty"), Risk 2 `:558–559` |
| edge-cases | F-3 | applied∩unapplied id prints in two lists | CLOSED (routed) | `## Deferred (P2+)` `:619–623` with the rule to adopt |
| edge-cases | F-4 | v1-shaped return has no step-4 rule | CLOSED | spec `:319–320` — "or with no `ref:` field at all, which is what a v1-shaped return looks like"; row 10 `:475` asserts it |
| edge-cases | F-5 | `ref:` ids undefined across a resume | CLOSED (routed) | `## Deferred (P2+)` `:624–629` |
| edge-cases | F-6 | `<token>` undefined on a headerless block | CLOSED | spec `:331–332` — "when the header carries none, print `unknown` — the persisted block is the record" |
| edge-cases | F-7 | Row 9's `:132` reads post-change | CLOSED | row 9 `:469` — "The pre-edit `:132` (the size-bound sentence) is byte-identical" |
| conventions | F-1 | reason-keyed `:143` missing from the roll-up | CLOSED | roll-up bullet `:86–90` |
| conventions | F-2 | D4/D6/grill-me still say "empty sections" | CLOSED | D4 `:118–119` ("its Settled and Open frontier sections empty"), D6 `:131–133` ("on the 2f-i path, which seeds findings and no facts"), Design 7 `:394–395` ("its header's reason line is the answer") |
| conventions | F-3 | Deferred preamble stale | CLOSED | spec `:599` — "round-1, round-2 and round-3" |

No REOPENED items. The two round-3 P1s are fully closed; F-1 below is a **new defect created by the correctness/F-4 fold**, not a reopening.

## Findings

### F-1: "The code block replaces `:548–549`" deletes step 5's heading and the `Print` verb, orphaning the halt-block re-render and three in-file "step 5" cross-references
**Severity:** P1
**Where:** spec § Design 5, `:322–330`, against `skills/spec-cycle/SKILL.md:548–554`, `:503`, `:544`, `:702`
**Edge case:** The implementer follows the new positional instruction literally — which is exactly what it was added for (it closes round-3 correctness/F-4, whose whole complaint was that step 5's shipped extent was ambiguous).
**What happens:** The pre-edit file is

```
548	5. **Re-render.** Print
549	   `grill applied: dispositioned <ids>; … grill.md`,
550	   then the 2f halt block again with options 1–3 only, each dispositioned title
551	   suffixed ` — grilled (spec edited; not re-reviewed)` …
```

`:548` is not part of the printed line — it is the step marker plus the verb. Replacing `:548–549` with the fenced code block leaves `### 2f-i` with steps 1, 2, 3, 4, then a bare fenced block, then the six bullets, then the verbless fragment "then the 2f halt block again with options 1–3 only, each dispositioned title suffixed …". Three consequences, none of them visible to the gate:

1. **Step 5 ceases to exist as a step.** `skills/spec-cycle/SKILL.md:503–504` ("list them in step 5 as `not grillable: …`"), `:544` ("report it in step 5 as `deferred to option 3: <finding id>`") and `:702` ("the step 5 `not grillable <ids>` line is their only record") all dangle. `:702` is the sentence that makes the not-grillable line the *only* record of a dispatch-failed finding — after the edit it points at nothing.
2. **The instruction to re-render the halt menu loses its verb.** That fragment is the mechanism returning the operator to options 1–3; it is also where the ` — grilled (spec edited; not re-reviewed)` suffix is applied.
3. **A fenced block cannot sit mid-sentence.** The pre-edit construction is "Print `<line>`, **then** the 2f halt block again" — one sentence across `:548–550`. The spec pins a fenced block into the middle of it and gives no replacement wording for `:550`'s continuation, so there is no correct way to execute the instruction as written.

Row 10 cannot catch any of this: every string it asserts (`grill applied (exit: <token>):`, `unreferenced decisions applied: <n>`, "is listed here rather than under `dispositioned`", "in seed order", "not the full red list", the nine VHS-32 row-7 strings, the `grill.md` path) survives the deletion, and the hunk stays inside `:489–561`.
**Why the spec misses it:** The sentence was written to disambiguate *which* text ships, not *what it replaces*. `:548–549` reads as "the two physical lines of the printed line" in a wrapped file, and the author's own preceding phrasing — "the line becomes" (singular) — presupposes `:548` survives. The two statements are in tension, and the newer, more explicit one is the destructive reading.
**Suggested fix:** No construct; one clause, inside text already being written. Replace "The code block replaces `:548–549`" with: "The code block replaces `:549` only — step 5's `5. **Re-render.** Print` lead-in at `:548` and its `, then the 2f halt block again …` continuation at `:550–554` are unchanged; the line stays an inline code span on its own physical line, as today. The bullets below are added to step 5 in the file, immediately after `:554`." If a fenced block is wanted instead, the spec must also pin `:550`'s replacement opening ("Then re-render the 2f halt block with options 1–3 only, …"), and row 10 should assert `### 2f-i` still contains `5. **Re-render.**`.

---

### F-2: Risk 2's "no Scope rows" is the last residue of the fence-empty-drops-facts error the same round fixed — `/spec-brief:141` builds Scope rows from grounding facts
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Risks 2, `:556–561`, against spec § Design 2 `:245–249`, § Design 3 `:278–279`, and `skills/spec-brief/SKILL.md:141–142`
**Edge case:** `/spec-brief` reaches `fence-empty` after Phase 1 grounding — the only realistic producer of this exit, and the one Risk 2 is written about.
**What happens:** Round 3's fold established that on `fence-empty` "`### Facts established` … holds whatever the seed supplied or a dispatch returned — for `/spec-brief`, which grounds first, that is normally not empty" (spec `:246–248`). `skills/spec-brief/SKILL.md:141` then reads: "`## Scope` gets one row per path the settled decisions **and grounding facts** name: `Current` filled from a fact with its `path:line`, `Change` from the settled decision that touches it." Grounding facts name paths, so the brief **does** get Scope rows — with `Current` filled and `Change` empty, since nothing settled. Risk 2 still asserts "no Scope rows". The adjacent clause in the same sentence was correctly updated ("no fact References beyond the ones Phase 1's grounding already supplied"), so the two halves of one sentence now disagree about whether the seed's facts reach the brief.

Nothing ships from Risk 2, and the error runs in the safe direction (the brief is less hollow than stated) — hence P2, not P1. But Risk 2 is the accepted-risk record `/spec-close` reconciles against and the Phase 3 drift-check reads, and it is the third site of the same root that rounds 2 and 3 each partially closed.
**Why the spec misses it:** The round-3 fold rewrote the References clause of the sentence and left the Scope clause, which had been written under the now-retracted assumption that `### Facts established` is empty on this exit.
**Suggested fix:** One clause, inside the sentence already rewritten this round: "… with `_(none settled …)_` under Decisions, an empty Risks list, Scope rows carrying only the `Current` column that Phase 1's grounding facts fill, and no fact References beyond the ones Phase 1's grounding already supplied". No new construct; `spec-brief:141` is unedited and stays fenced.

---

### F-3: The rewritten `docs/spec-workflow-reference.md:23` asserts "the brief carries no open items" for an emptied frontier — false whenever any question was deferred, which is the normal case
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7, `:399–407`, against `skills/grilling/SKILL.md:63` and `skills/spec-brief/SKILL.md:94`, `:140`
**Edge case:** Round 1 renders Q1–Q3; the operator answers Q1 and Q2 and **defers Q3**. `grilling:63`: "`defer` … moves the question to the Open frontier at once. Its descendants are *not* enumerated or asked; the subtree is recorded as **one** rolled-up Open item." Round 2's recomputed askable frontier is empty (or falls below the fence) → exit `empty-frontier`.
**What happens:** The hand-off block's `### Open frontier` carries two items (the deferred Q3 and its rolled-up subtree), `/spec-brief:140` maps both into `## Risks / decisions`, and the brief demonstrably carries open items — while the repo's only prose paraphrase of the contract tells the reader an emptied frontier means it carries none. The reason line is no help either: `tree fully visited` is itself wrong for a deferred subtree that was never enumerated. A reader who hits a `fence-empty`-adjacent brief with open items has no document that explains it, and the operator's mental model at the `/spec-brief` Phase 3 preview is exactly the wrong one.

The claim is pre-existing (`7403cb5`'s `:23` says the same), which keeps it out of P1 — but this PR rewrites that sentence, round 3 already reopened it once for the fence half, and the fix is deleting four words from text being written anyway. Row 13 asserts "altitude fence" twice and "either way the reason line says which"; both survive the fix.
**Why the spec misses it:** Design 7's `:23` edit was scoped to the exit-token taxonomy (add `fence-empty`, restore the fence parenthetical). The trailing consequence clause was carried over verbatim from the v1 sentence and never checked against `grilling:63`'s defer rule.
**Suggested fix:** Cut the false half of the conjunction the round-3 fold produced: "An emptied frontier means the tree was fully visited, or that a later round's remaining candidates all fell below the altitude fence — either way the reason line says which, **and anything the operator deferred is still in the brief's open items**." Or simply end the sentence at "says which". Row 13 needs no change.

---

### F-4: The plain-language rule's own example (`an exit token such as \`empty-frontier\``) points at text the rule does not govern — the machine-read hand-off block
**Severity:** P3
**Where:** spec § Design 4, `:298–304`, against § Design 2's fenced block `:210–223` and § Design 5 `:331–332`
**Edge case:** The primitive renders the hand-off block and applies the plain-language rule to it, glossing `exit: fence-empty` or `unresolved because: blocked-on: F3` with a parenthetical.
**What happens:** The rule is scoped to "Every rendered round", sits inside `## Per-round output contract`, and D9 confirms "for the primitive's rounds only" — so a careful read excludes the block. But the rule's illustrative list is "a section code such as `2f-i`, an exit token such as `empty-frontier`, a file or block name", and exit tokens and block names are precisely what the hand-off contract renders; the per-round literal lines at `:52–55` contain neither. A model applying the rule by its examples rather than its scope injects parentheticals into the one block three callers parse: `/spec-brief:143` matches the header's reason string, and 2f-i step 5 reads `<token>` from `exit:`. Both degrade rather than break — the reason phrase would still be a substring, and a glossed token still identifies the exit — which is why this is P3 and not P2. The `unknown` fallback (`:331–332`) covers the absent-token case, not the decorated-token case.
**Why the spec misses it:** The examples were drawn from the brief's problem statement (item 4: "exit tokens such as 'empty-frontier' appear in **question bodies**"), where they are apt; the block was never re-walked against them.
**Suggested fix:** One clause at the end of the paragraph, no new construct and no numeric bound (row 8 stays satisfied): "This rule governs rendered rounds; the hand-off block is rendered exactly as its contract states." Alternatively swap the example for one that only occurs in a round body.

---

### F-5: A finding whose spec text the grill edited can appear in no operator-visible place at all — the halt block's "grilled" suffix is keyed on `dispositioned`, which the both-lists rule empties
**Severity:** P3
**Where:** spec § Design 5, `:333–338` and § Risks 3, `:569–571`, against `skills/spec-cycle/SKILL.md:550–552`
**Edge case:** A grill settles a decision carrying `ref: edge-cases/F-3` **and** leaves an Open item carrying the same id (a second question about the same finding, or an unestablished fact whose need arose from that seed item — Design 1's descent rule gives F-items the seed's ids). Step 4 applies the Settled edit.
**What happens:** The both-lists rule prints the id under `left open`, not `dispositioned`. `unreferenced decisions applied: <n>` does not count it either — the decision *had* refs. `skills/spec-cycle/SKILL.md:551` suffixes " — grilled (spec edited; not re-reviewed)" on "each **dispositioned** title", so the re-rendered halt block shows the finding red and unmarked. The operator's two surfaces — the step-5 line and the halt block — both report that nothing moved, while the spec on disk was edited under that finding. Risk 3 anticipates the step-5 line ("prints as `left open`… `grill.md` shows it") but not the suffix, which is the surface `:551` exists to provide ("so the operator can see what moved without opening `grill.md`"). Harm is bounded: `total_p0p1` is unchanged and option 1 re-dispatches reviewers over the edited text, so nothing goes green on an unseen edit.
**Why the spec misses it:** The both-lists rule was reasoned about as a *reporting* rule for the step-5 line; `:550–552`'s dependence on the same list was not re-walked, and `:550–552` is untouched by Design 5.
**Suggested fix:** No new step-5 clause (the fenced construct). One sentence appended to Risk 3: "The halt block's ` — grilled (spec edited; not re-reviewed)` suffix is keyed on `dispositioned` too, so such a finding is unmarked there as well; `grill.md` and the spec diff are the record, and option 1 re-reviews the edited text." If a fix is wanted rather than a record, it belongs in `## Deferred (P2+)` with the rule to adopt (suffix on any id the grill's Settled items applied, whichever list it printed in).

---

### F-6: Row 14's "every file under `docs/` … unchanged" fences this spec's own artifacts, and the flow that makes it pass is an unstated ordering dependency
**Severity:** P3
**Where:** spec § Test plan row 14, `:495–498`, and § Files to leave alone, `:48–51`
**Edge case:** The `/ship-spec` implementer commits `docs/specs/TODO/VHS-33.spec.md`, `.brief.md` and `VHS-33.reviews/**` on the implementation branch — a natural choice, since all three are **untracked** in the working tree right now (`git status`: `?? docs/specs/TODO/VHS-33.spec.md`, `?? docs/specs/TODO/VHS-33.reviews/`).
**What happens:** Row 14 fails and blocks a correct PR, because those paths are under `docs/` and are not `docs/spec-workflow-reference.md`. The row only passes if the artifacts are committed to `main` *before* the worktree is cut — which is what VHS-32 did (`e193b8e docs(vhs-32): track /spec-brief spec v4 + four review rounds` landed on main ahead of the PR merge `d381f88`) — but nothing in the spec states that ordering, and `/ship-spec` Phase 4 stages only "each modified file in the diff", so it neither creates nor blesses the artifact commit. VHS-32 avoided this by enumerating (`docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `docs/customizing.md`) rather than generalizing over `docs/`. § Files to leave alone inherits the same over-reach, literally declaring the spec's own file out of scope.
**Why the spec misses it:** The `docs/` generalization was written to fence the *documentation* tree (the one real risk being README/AGENTS, checked at `:48–51`); the spec-artifact tree lives under the same prefix.
**Suggested fix:** Narrow the predicate in both places: "`README.md`, `AGENTS.md`, and every file under `docs/` **outside `docs/specs/`** other than `docs/spec-workflow-reference.md`". One qualifier, no construct.

---

### F-7: The `left open` bullet's shipped rationale says "any question about it is open", but the rule it justifies also fires on F-items and rolled-up items
**Severity:** P4
**Where:** spec § Design 5, `:336–338` (shipped bullet text)
**Edge case:** The Open item carrying the shared id is an `F<n>` fact item or the rolled-up deferred item, not a question.
**What happens:** The rule is stated over all three kinds ("every id on an Open item (Q, F, or rolled-up)"), then justified with "a finding is not dispositioned while any *question* about it is open". A reader resolving the mismatch in favour of the rationale would print the id under `dispositioned` when only a fact is outstanding — the less conservative direction. No behavioural consequence expected (the rule is stated first and unambiguously), and the conservative reading is the literal one.
**Why the spec misses it:** The rationale was written for the Settled∩Open-*question* case that motivated the rule; F-items became `ref:`-bearing later, in the same design.
**Suggested fix:** One word in the shipped bullet: "a finding is not dispositioned while anything about it is still open."

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 3 | P4: 1

STATUS: RED P0=0 P1=1 P2=2 P3=3 P4=1
