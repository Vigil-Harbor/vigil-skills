# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | F-item reason set is "exactly two" but Design 3 adds a third | CLOSED | spec.md:223 renders the parenthetical inline; :232–234 pins it as an optional qualifier on the first value; checklist row 4 (:526–533) |
| edge-cases | F-2 | Rolled-up deferred item has no field for `ref:` | CLOSED | spec.md:224 (shape 3 now carries `unresolved because: deferred. ref:`); placement rule :206–208; row 4 asserts all four shapes |
| edge-cases | F-3 | `fence-empty` on a resume erases carried Settled/Facts | CLOSED | spec.md:330–338 "Fresh invocations only"; checklist row 8. New adjacent issue → F-7 below |
| edge-cases | F-4 | Verification "in the round after" has no round on the last round | CLOSED | spec.md:300–305 Design 3 rule 3 |
| edge-cases | F-5 | Refuted and never-checked claims render identically | CLOSED | spec.md:271–275 refuted disposition with `path:line`; Design 7 :471–475 carries it into the brief |
| edge-cases | F-6 | No tripwire for missing `ref:`, no seed-id reconciliation | CLOSED | spec.md:413–433. Residual quality issues → F-6, F-12, F-13 below |
| edge-cases | F-7 | Partially-supplied id seed collapses into `ref: none` | PARTIAL | spec.md:181–184 declares it illegal and reports it, but does not say what `ref:` renders for the unidentified subset, and the reporting slot does not exist on a zero-round exit → F-10 |
| edge-cases | F-8 | `ref:` id lexical form undefined while comma is the delimiter | CLOSED | spec.md:178–180 legal-id rule. Same class one layer down → F-14 |
| edge-cases | F-9 | Empty-section rendering defined only for `fence-empty` | CLOSED | spec.md:245–251 `_(none)_` on every exit, `none` for fields |
| edge-cases | F-10 | Step-5 line undefined when a set is empty | CLOSED | spec.md:403–406 all clauses unconditional; :435–440 purpose-written fence-empty line |
| edge-cases | F-11 | Design 3 displaces `grilling:76` wholesale including its hang rule | **REOPENED** | spec.md:289–295 narrows the displacement, but `:76`'s "host-timeout treatment" *is* the displaced retry → F-2 below (P1) |
| edge-cases | F-12 | A partially confirmed claim has no disposition | PARTIAL | spec.md:279–284 adds the fourth disposition, but the "different fact" branch allocates no `F<n>` → F-3 below |
| edge-cases | F-13 | `blocked-on: F<n>` and `stopped` overlap with no precedence | **REOPENED** | spec.md:239–243 states a precedence order and then contradicts it in the next sentence → F-1 below (P0) |
| edge-cases | F-14 | F-item reason set cannot distinguish four causes | PARTIAL (accepted) | Manifest records the deliberate scope call; brief decision 3 pins the two-value set. No action |
| edge-cases | F-15 | Not-grillable ids in two rules at once | CLOSED | spec.md:423–425 removes it from the precedence chain; :426–429 evaluates unknown-id first. Residual wording → F-12 |
| correctness | F-1 | `empty-frontier` defined two incompatible ways | CLOSED | spec.md:326–329 keeps both reason lines; only the round-1 case moves |
| correctness | F-2 | Row 2 grep unsatisfiable, row 10 forbids the fix | CLOSED | spec.md:521–524 scopes the spec-cycle half to added lines. Cross-ref nit → F-17 |
| correctness | F-3 | F-item template "exactly two" vs Design 3's third string | CLOSED | same edit as edge-cases F-1 |
| correctness | F-4 | `ref:` has no slot on F-item / rolled-up item | CLOSED | same edit as edge-cases F-2 |
| correctness | F-5 | Seeded-but-unrendered finding falls out of all four sets | CLOSED | spec.md:413–417 `not reached`. Its stated cause is too narrow → F-13 |
| correctness | F-6 | VHS-32 row 4 "supersedes" mischaracterization | CLOSED | spec.md:129–133 D9 now says *extends*; checklist row 5 |
| correctness | F-7 | "empty-Settled rule already covers fence-empty" over-broad | PARTIAL | spec.md:458–466 adds the all-sections-empty rule, but does not reconcile the sentinel text with `spec-brief:139` → F-16 |
| correctness | F-8 | `F1 <answer>` meaning changes while its operator-facing line is pinned | CLOSED | spec.md:310–314 states it as a deliberate choice with rationale |
| correctness | F-9 | `:88` / `:74` still use the old vocabulary | CLOSED | spec.md:253–258 Cross-references |
| correctness | F-10 | `:23` is not part of the grilling-contract paraphrase | CLOSED | Scope table :32 lists `:23` separately from `:33`, `:35` |
| correctness | F-11 | Touched surface is one commit old | CLOSED | spec.md:677–679 Risks 4; § Deferred (P2+) |
| conventions | F-1 | Rows 2 and 10 mutually unsatisfiable | CLOSED | spec.md:521–524 |
| conventions | F-2 | `## Test command` carries prose under `N/A` | CLOSED | spec.md:602–604 is exactly `N/A` |
| conventions | F-3 | "Carried from the brief" but fences were widened | CLOSED | spec.md:629 / :644–657 split into carried vs spec-author additions |
| conventions | F-4 | No roll-up of spec-level Design additions | CLOSED | spec.md:56–72 |
| conventions | F-5 | Absent-`ref:` justified by a nonexistent parser-compat concern | CLOSED | spec.md:201–204 "legibility, not compatibility" |
| conventions | F-6 | No `## Risks` / `## References` | CLOSED | spec.md:659–706 |
| conventions | F-7 | VHS-32 wiki decision revisit trigger unrecorded | CLOSED | spec.md:135–137; Out of scope 11 |
| conventions | F-8 | `unreferenced decisions applied` conditionally omitted | CLOSED | spec.md:403–406 |
| conventions | F-9 | Three spellings of "empty" coexist | PARTIAL | spec.md:248–251 distinguishes `_(none)_` from `none`, but Design 7 adds a fourth unreconciled sentinel → F-16 |

## Findings

### F-1: Design 2's reason-precedence order contradicts its own stop-with-exploration sentence
**Severity:** P0
**Where:** spec.md:239–243 (§ Design 2, "The Q-item reason set narrows")
**Edge case:** `stop` exit with a fact request unresolved and a question blocked on it — the exact scenario the paragraph's last sentence describes.
**What happens:** The paragraph states the ranking `stopped` → `round-cap` → `deferred` → `blocked-on: …`, then in the next sentence says: "On a `stop` with an exploration in flight, both items are Open: the F-item with `stopped`, the question it blocked with `blocked-on: F<n>`." Under the stated ranking, `stopped` outranks `blocked-on`, so that question must render `stopped`. Two rules in the same paragraph prescribe two different rendered strings for the same item. An implementer picks one; two implementers pick two. It also silently contradicts the existing `skills/grilling/SKILL.md:108` ("their questions are Open with `unresolved because: stopped`"), which the spec does not flag as changed.
**Why the spec misses it:** This is the round-1 F-13 fix. The precedence order was added to resolve the overlap, and the worked example that was meant to illustrate it instead demonstrates the opposite ordering. The round-cap example and the stop example are constructed on incompatible principles: one says the exit reason wins, the other says the causal reason wins.
**Suggested fix:** Pick one and make both examples consistent. The stronger choice, given D3's whole purpose is letting a caller tell "needs a fact" from "needs a decision": rank the *causal* reason above the *exit* reason (`deferred` → `blocked-on: …` → `stopped` → `round-cap`), and rewrite the round-cap example accordingly. If instead the exit reason must win, change the stop sentence to "the F-item with `stopped`, the question it blocked also with `stopped`" and say explicitly that `blocked-on: F<n>` is reachable only on `empty-frontier` and `revised-after-cap`.

### F-2: Design 3 rule 1 reinstates the very retry it says it displaces
**Severity:** P1
**Where:** spec.md:289–295 (§ Design 3, rule 1)
**Edge case:** A verification dispatch that the host reports as timed out.
**What happens:** Rule 1 says "Dispatched once; the operator is never re-asked… **Only that retry is displaced.** `:76`'s host-timeout treatment … appl[ies] to verification dispatches unchanged." But `grilling/SKILL.md:76`'s host-timeout treatment is literally *"Where the host reports a timeout, treat it identically"* — identically to a failed dispatch, whose treatment is "carry its question to the next round as an `ℹ️` fact request", i.e. re-ask the operator. So on a timeout the spec says both (a) never re-ask, render `fact not established (operator claim, unverified)` per Design 3's third disposition (which lists "a dispatch error"), and (b) carry it back to the operator as a fact request. The two produce different rendered rounds and different hand-off blocks, and a timeout is the commonest verification failure.
**Why the spec misses it:** Round-1 F-11 asked for the displacement to be narrowed rather than wholesale. The narrowing kept `:76`'s two clauses as a unit, but one of those clauses ("treat it identically") is only a *classification* whose consequence is the displaced retry.
**Suggested fix:** State it in two parts: "A verification dispatch that errors, returns empty, times out, or returns without confirmation is a failed dispatch **and is not retried** — the claim renders `fact not established (operator claim, unverified)`. `:76`'s *never-returns* rule is unchanged: a dispatch that never returns blocks the round it belongs to, bounded by the dispatch cap." Drop the phrase "host-timeout treatment … unchanged".

### F-3: The "different fact" branch allocates no `F<n>`, colliding with the claim it replaces
**Severity:** P2
**Where:** spec.md:279–284 (§ Design 3, "Partially confirmed")
**Edge case:** The operator claims F1 is at `a.py:10`; the exploration finds the function at `b.py:40` with different behavior.
**What happens:** The spec says record the different fact "on its own terms, with its own `path:line` source, and leave the operator's claim Open." F1 is now simultaneously an Open F-item and an entry in `### Facts established`. The numbering rule (`grilling:48`) says the F series is monotonic and never resets, but says nothing about allocating a number for a fact that was never rendered as a request. If the implementer reuses F1, a Settled item's `Facts relied on: F1` resolves to two different things, and `/spec-brief` maps F1 into `## References` *and* into `## Risks / decisions` in the same brief.
**Suggested fix:** Add one sentence: "A fact the exploration establishes that is not the claim gets the **next unused `F<n>`**; the operator's claim keeps its original number and stays Open. The two never share a number."

### F-4: Precedence demotion applies the spec edit and reports the finding as untouched
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:420–422 (Design 6, "Precedence"), read against spec.md:392–394 (step 4) and `spec-cycle/SKILL.md:550–551`
**Edge case:** A finding id appearing in both an applied Settled item's `ref:` and any Open item's `ref:`.
**What happens:** Step 4 applies the Settled edit to the spec unconditionally. Step 5's precedence puts the id in `left open`. The existing step-5 rendering suffixes ` — grilled (spec edited; not re-reviewed)` onto "each **dispositioned** title", so that finding's title gets no suffix — the operator sees an unmodified red finding while the spec was in fact edited on its behalf. That is the same class of invisible spec mutation the brief's problem 1 exists to eliminate, one layer down.
This is not exotic: Design 1's inheritance rule says "a decision inherits the ids of the tree node above it", and the rolled-up deferred item "carries the ids its parent carried" with no rule narrowing it to the ids of the *unexplored* subtree. A deferred subtree near the root therefore carries most or all seed ids, and precedence sweeps them all into `left open` while their Settled siblings still edited the spec.
**Suggested fix:** Two edits. (a) In step 5: "An id demoted to `left open` by precedence, whose Settled item was applied, is additionally listed as `also edited (left open): <ids>`, and its title carries the ` — grilled (spec edited; not re-reviewed)` suffix." (b) In Design 1, narrow the rollup: "The rolled-up deferred item carries only the ids of seed items no rendered decision reached."

### F-5: The missing-`ref:` withhold governs step 4 but is written in step 5
**Severity:** P2
**Where:** spec.md:430–433 vs spec.md:392–394 (step 4: "Unchanged in substance")
**Edge case:** The primitive returns a Settled item with no `ref:` field when 2f-i seeded ids — the mis-echo Risk 2 names.
**What happens:** The withhold rule ("apply **no** spec edit from that item") is a step-4 behavior, but it appears only in step 5's bullet list, and Design 6's step 4 paragraph says "**Unchanged in substance.**" 2f-i executes step 4 before step 5. An implementer editing `spec-cycle/SKILL.md` per Design 6 writes no withhold into step 4's prose, so at runtime the model applies the edit and only later prints `item missing ref: <item title>`.
**Suggested fix:** Move the withhold sentence into Design 6 step 4 and change "Unchanged in substance" to name the one substantive change.

### F-6: `unreferenced decisions applied: <n>` covers only one of four classes of unaccounted edit
**Severity:** P2
**Where:** spec.md:410–412 (Design 6, "Zero-id")
**What happens:** The count is defined narrowly as items "rendering `ref: none`". Three other applied items therefore appear in no clause and in no count: (a) all refs unknown → `unknown ref ignored:` prints per id but the *edit* is counted nowhere; (b) all refs demoted by precedence → F-4 above; (c) a hallucinated ref matching a `not grillable` id, which spec.md:426–429 explicitly excludes from unknown-reporting, so it is swallowed with no line at all.
**Suggested fix:** Redefine `n` as "applied Settled items that disposition no seeded id in this line — whether they carried `ref: none`, only unknown ids, or only ids reported under another clause."

### F-7: A zero-item resume burns the single post-cap round and reports a round that never rendered
**Severity:** P2
**Where:** spec.md:330–338 (§ Design 4, "Fresh invocations only")
**Edge case:** `prior_summary` with `rounds_used ≥ round_cap`; the revised Q, once re-opened, no longer clears the altitude fence, so the resume renders zero items.
**What happens:** The rule routes it to "`revised-after-cap (+1 round)` where the post-cap round was **granted**". Granted is not rendered: the header renders `rounds: <round_cap>+1/<round_cap>` for a round that asked the operator nothing, and `/spec-brief` Phase 3 (`spec-brief:105`) then re-renders "with options 1 and 3 only" — the operator's one and only post-cap round is spent on an empty round with no path to recover it.
**Suggested fix:** Add: "A resume that renders zero items has not used its post-cap round: exit `empty-frontier` with `rounds: <rounds_used>/<round_cap>` and the fence reason, carried sections intact. `revised-after-cap (+1 round)` is rendered only when the post-cap round actually rendered at least one item."

### F-8: A `fence-empty` summary reaches Phase 3's confirm block, which offers a revise option that cannot be exercised
**Severity:** P2
**Where:** spec.md:454–466 (§ Design 7) and the Scope table (spec.md:30)
**What happens:** Phase 3 (`spec-brief:92–107`) is untouched by this spec, so it renders a preview of two empty lists with no explanation, then prints option 2 — "Revise an answer (name the Q number)" — against a summary containing zero Q numbers. An operator who picks 2 either gets an error the spec does not define, or re-invokes `grilling` with an empty `prior_summary`. Worse for legibility: Design 7's warning lives in **Phase 4**, i.e. it prints *after* the operator has already confirmed the write.
**Suggested fix:** Add a Phase 3 bullet to Design 7 and to the Scope table's `spec-brief` row: on a `fence-empty` summary, render the warning **before** the confirm block, and render options 1 and 3 only.

### F-9: A `fence-empty` brief's present-but-empty headers defeat `/spec-cycle`'s only drift-check fallback
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:458–466 read against `spec-cycle/SKILL.md:635–640`
**What happens:** The Phase 3 parser enumerates "the numbered list under the header" and renders the fallback bullet **only "if a header is missing."** Design 7 emits the headers with `_(none)_` under them. Header present, list empty → zero checkboxes and no fallback. Because Design 7 makes *all* sections empty and emits no `## Scope` rows, the entire HARD-STOP drift check degrades to an empty form — the one gate between an uninterviewed brief and `/ship-spec` renders nothing to check, silently.
**Suggested fix:** Either (a) have Design 7 omit the empty headers entirely, or, better, (b) extend the Scope table's `spec-cycle` row with a one-line change to `spec-cycle:640`: "If a header is missing **or its list is empty**, render the fallback bullet for that section." Note this is a hunk outside `### 2f-i`, so checklist row 11 needs the exception written in.

### F-10: An all-or-none violation has no reporting slot on the exits where it is likeliest, and no prescribed rendering
**Severity:** P2
**Where:** spec.md:181–184 (§ Design 1, "All or none")
**What happens:** The rule says the primitive "says so in its round-1 preamble." On `fence-empty` zero rounds are rendered and on `empty-seed` no block is produced at all, so the violation is reported nowhere. Separately, the rule diagnoses without prescribing: it says what the primitive does *not* do but never says what it *does* render for those items. And "round-1 preamble" is not a rendering slot defined anywhere in `## Per-round output contract`.
**Suggested fix:** "A partially identified seed is reported on the first line the primitive renders — the round-1 preamble, or, where no round is rendered, immediately above the `## Grill summary` header — and the primitive renders **no `ref:` field at all** for the whole interview (the absent state), so no caller can mistake a dropped id for `ref: none`." Add a `## Per-round output contract` line defining the preamble slot.

### F-11: There is no path for an operator fact that is true but not repo-checkable
**Severity:** P2
**Where:** spec.md:262–284 (§ Design 3) and spec.md:307–308
**Edge case:** `/grill-me "should we restructure the on-call rotation"`, or any fact request whose answer is a policy, a decision made in a meeting, or an external constraint.
**What happens:** `### Facts established` requires `(source: <path:line>)`; `source: operator` is now flatly prohibited; and every claim goes through an exploration instructed to "answer from the paths named in the question, and return `not found` rather than searching exhaustively." A non-repo claim therefore always returns `not found` → `fact not established (operator claim, unverified)`, permanently. Every question downstream renders `blocked-on: F<n>`, and the interview cannot settle them. Under v1 the operator's answer simply became the fact. `/grill-me` — whose description is "a plan, decision, or idea", not "a repo" — degrades to an all-open summary on any non-repo topic, and the primitive never says why.
**Suggested fix:** Add a fifth branch: a claim no path could carry is not a failed verification — record it as `(source: operator statement, not repo-checkable)` and scope the prohibition to repo claims. If the fence must stay absolute, say so explicitly in `/grill-me`'s failure modes so the degradation is a documented outcome rather than a surprise.

### F-12: The completeness rule partitions the seed using a set that never enters the seed
**Severity:** P3
**Where:** spec.md:418–419 vs spec.md:423–425
**What happens:** "The four disposition sets plus `not reached` are disjoint and exhaustive over the seed" includes `not grillable` — which the precedence bullet says "never enter[s] the seed". The partition is stated as five sets, one of which is empty over the seed by construction.
**Suggested fix:** "Every seeded id appears in exactly one of `dispositioned`, `left open`, `deferred to option 3`, and `not reached` — disjoint and exhaustive over the seed. `not grillable` is reported alongside them but is disjoint from the seed entirely."

### F-13: `not reached`'s stated meaning is wrong for its most common causes
**Severity:** P3
**Where:** spec.md:413–417
**What happens:** The clause is defined as "every seeded id that appears in no returned `ref:` at all", but the explanation gives exactly one cause: "it fell below the grill's altitude fence." With `question_cap` 7 and eleven findings, findings 8–11 do not render in round 1 at all; if the operator stops after round 1 they land in `not reached` having never been fence-tested. A finding whose `ref:` the model dropped lands there too.
**Suggested fix:** Reword the rationale to name all four causes and say the clause does not distinguish them; it exists so none disappears.

### F-14: The legal-id rule bars `ref:`'s delimiter but not the step-5 line's
**Severity:** P3
**Where:** spec.md:178–180 vs spec.md:400
**What happens:** The rule bars comma, newline, and surrounding whitespace. The step-5 line uses `;` to separate its six clauses. An id containing `;` renders a step-5 line whose clause boundaries are unreadable — the same failure comma caused inside `ref:`, one renderer down.
**Suggested fix:** Add `;` to the barred characters, and state the within-clause separator for the step-5 line explicitly (comma-space).

### F-15: The `## Scope`-row fence does not exclude a refuted claim's `path:line`
**Severity:** P3
**Where:** spec.md:476–480
**What happens:** The fence is worded as "a `## Scope` row for a path with no `path:line` behind it." A refuted claim *has* a `path:line` — evidence **against** it. Read literally, the fence permits a `## Scope` row whose `Current` cell is populated from a path cited to disprove a claim.
**Suggested fix:** "What stays illegal: a `## Scope` row sourced from anything but an item in `### Facts established`. A refuted claim's `path:line` is evidence against a claim, never a `Current` cell."

### F-16: Two sentinels now compete for an empty `## Decisions carried forward`
**Severity:** P3
**Where:** spec.md:460–462 vs `spec-brief/SKILL.md:139`
**What happens:** `:139` says an empty Settled section is written as `_(none settled — see Risks / decisions)_`; Design 7 says a fence-empty brief "carries `_(none)_`". Design 7 states precedence for the *warning* but not for the sentinel text. `:139`'s cross-reference is also false on this path, since Risks is empty too.
**Suggested fix:** "On a `fence-empty` summary, `## Decisions carried forward` and `## Risks / decisions` both read `_(none)_`; `:139`'s sentinel and its warning are both superseded on this path."

### F-17: Checklist row 2 cites row 10 for an assertion that lives in row 11
**Severity:** P4
**Where:** spec.md:523–524
**What happens:** Row 2 ends "Its pre-existing § 2b dispatch block is out of scope and unchanged (row 10)." Row 10 asserts 2f-i's *contents*; the no-hunk-outside-2f-i assertion is row 11. Rows were renumbered when row 5 was inserted for D9.
**Suggested fix:** Change `(row 10)` to `(row 11)`.

## Summary
P0: 1 | P1: 1 | P2: 9 | P3: 5 | P4: 1

STATUS: RED P0=1 P1=1 P2=9 P3=5 P4=1
