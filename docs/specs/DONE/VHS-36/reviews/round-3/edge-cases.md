# Edge-Cases Review — round 3

Grounding complete: spec and brief read fresh from disk; Plane VHS-36 retrieved (namespace `skills`, tag-exact, body matches the brief); global + project `CLAUDE.md`; all four target files at `f4d9290` (HEAD); all three round-2 reviews; `docs/specs/DONE/VHS-33/attempt-1/spec.md:405–510`.

Attempt-1 check first, since it was asked directly: the **deleted overflow-ordering rule is not re-created** — attempt 1 ranked verifications against new fact needs *inside one batch* ("new fact needs are dispatched before verifications, and verifications overflow first", attempt-1 `:476–488`); this spec keeps two sequential batches with independent caps and orders only within the check batch. But attempt 1's **rule 3 — the last-rendered-round hole** — is partially re-created in bounded form by the new surplus rule, and three places in the spec still deny it. That is F-1/F-2 below.

---

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P0) | check batch bound contradicted; cap has no overflow rule | **PARTIAL** | Shipped text fixed: surplus rule + `2 × question_cap` at spec:265–267; Design 3 gains the sixth cause at :309. But D4 still ships the killed clause "the number of checks per round is bounded by the fact requests the previous round rendered" (:98–99) and "deletes … its last-round hole" (:99–100), and Designs 7/10 still assert the check always runs before the hand-off — F-1, F-2 below |
| edge-cases | F-2 (P1) | gated question noted unverified even when confirmed | CLOSED | :390–393 splits the branches ("rendered as any other question where the check confirmed … and, where it did not confirm, rendered with a one-line note") |
| edge-cases | F-3 (P1) | `claim:` inserts unbounded, unescaped operator text | **PARTIAL** | Newline, quote and marker-spoofing halves closed (:310–315, row 4 pins "held to one line" / "never carrying the block's own"). The size bound is stated in a unit this spec defines as unbounded (F-7), and the same operator string still enters the block unnormalized on the **confirmed** path (:305–306) — F-3 below |
| edge-cases | F-4 (P2) | omitted `claim:` form | CLOSED | Design 8 :456–459 "omitted **together with its leading `; `**"; row 4 :610–612 |
| edge-cases | F-5 (P2) | claim text lost across a resume | CLOSED | :401 "keeping its `claim:` text"; row 5 :628 |
| edge-cases | F-6 (P2) | a second answer to the same `F<n>` | CLOSED (new variant) | :222–226 ships "replaces the claim and gets its own check — which is not a retry…". The rule now collides with the surplus queue it did not exist beside — F-5 below |
| edge-cases | F-7 (P2) | row 17 item 3 needed arithmetic | CLOSED | "up to `2 × question_cap` dispatches in all" ships (:266); row 17 is thirteen single-sentence items (:717–736), each verified against exactly one shipped sentence |
| correctness | F-1 (P0) | row 17's one-sentence rule failed 3–4 items | CLOSED | Thirteen-item split; I mapped all thirteen to one shipped sentence each |
| correctness | F-2 (P2) | row 10 `:84–87` | CLOSED | :665–667 now `:86–88` with the pre-`**Plain language.**` note |
| correctness | F-3 (P3) | `2 × question_cap` not in shipped text | CLOSED | :291–294 |
| correctness | F-4 (P3) | § Scope nine topics under "eight" | CLOSED | :27 now enumerates eight |
| correctness | F-5 (P3) | `:67` anchor | CLOSED | :245–246 `:65–67` |
| correctness | F-6 (P3) | any-round rule under a resume lead | CLOSED | Moved into Design 1, "In any round" (:222); rationale :250–254 |
| correctness | F-7 (P4) | row 12 / § Scope enumeration slips | CLOSED | Row 12 "all seven situations … six … plus" (:683–687); § Scope :47–51 |
| correctness | F-8 (P3) | omitted form not pinned | CLOSED | Same as edge F-4 |
| conventions | F-1 (P2) | preamble scoping of Design 10's bullet | CLOSED | :182–188 splits "Design 10's **new failure-mode bullet**" from "Design 10's **`:156` amendment**" |
| conventions | F-2 (P2) | VHS-33 wiki § 3 invariant narrowed silently | CLOSED | D7 :140–144 names the invariant and tells `/spec-close` to decompose it |
| conventions | F-3 (P2) | `claim:` normalization | PARTIAL | Same as edge F-3 |
| conventions | F-4 (P4) | row 10 / row 3 ranges | CLOSED | :665, :598–600 |
| conventions | F-5 (P4) | row 12 five-vs-six | CLOSED | :683–687 |
| scalability | — | — | N/A | `scale_lens: off`; no `scalability.md` in round-2 |

**Design 3's six not-confirmed causes** — asked directly. All six are reachable and all six are dispositioned to the same Open qualifier: `not found` and empty return and dispatch error (ordinary dispatch failures, `:78`'s classes); partial support (Design 3's own last sentence); no read-restricted agent class (reachable through the unedited `:74` **Detection first** path — the fact need renders as an `ℹ️` request, the operator answers it, and no class exists to check it); and the batch-cap cause, reachable exactly as :281–289 argues. Cause 6 is the one whose *path* is under-specified — F-1, F-4, F-5, F-6 all land on it.

## Findings

### F-1: The surplus rule makes "its check runs before the hand-off" false, and that sentence ships twice
**Severity:** P0
**Where:** spec § Design 7 shipped blockquote (spec.md:425–428); § Design 10 `:156` amendment (spec.md:498–501); vs § Design 2 shipped blockquote (spec.md:265–267)
**Edge case:** The operator answers more than `question_cap` claims in the **stopping** round (or in any last rendered round). Reachable by the spec's own argument at :281–285 — Open `F<n>` items accumulate to `(round_cap + 1) × question_cap`, `:53` lets the operator answer any of them, and that is the entire justification the spec gives for the surplus rule existing.
**What happens:** Two shipped sentences of the same file contradict each other.

- Design 2 ships: *"Where the operator answered more claims than the cap allows, the surplus is checked in **the next round's check batch**, oldest `F<n>` first."*
- Design 7 ships, without qualification: *"A fact request the operator answered in the stopping round is not among the abandoned: **its check runs before the hand-off**, so the claim resolves either to an established fact or to `fact not established (operator claim, unverified)`."*
- Design 10's `:156` amendment repeats it: *"A fact need the operator answered in the stopping round is not abandoned — **its check runs before the hand-off**…"*

On `stop` there is no next round, so the surplus claims' checks do **not** run before the hand-off. Design 3's sixth cause gives those claims a landing spot, so the outcome is safe — but § Termination and § Failure modes will ship a rule that is false in the one case § Fact-finding invented the surplus rule for, and the two sections give a reader opposite answers about whether a stopping-round claim is guaranteed a check. This is worse than a doc slip because § Termination is where the reader looks up `stop`: an implementer following it will either hold the hand-off open for surplus checks (breaking the `question_cap` concurrency bound the same round introduced) or silently fail its own stated guarantee.

Row 17 item 9 ("What happens to the claim on `stop`?") is answered by exactly this sentence, so the reading gate certifies the false rule.
**Why the spec misses it:** Design 7's sentence is the round-1 F-4 fold and predates the surplus rule, which arrived this round in a different Design. The closure manifest lists the surplus rule under `**When the check runs.**` only; nothing re-read § Termination against it.
**Suggested fix:** Qualify both shipped sentences with the one exception, e.g. Design 7: *"…is not among the abandoned: its check runs before the hand-off unless the check batch was already full, and the claim resolves either to an established fact or to `fact not established (operator claim, unverified)`."* Design 10's `:156` bullet takes the same clause. Add to row 6 the assertion that `:110` contains the exception phrase, and reword row 17 item 9 to "…including when the batch cap was already full".

### F-2: § Decisions carried forward D4 still asserts the bound the shipped text abandoned, and still claims the last-round hole is deleted
**Severity:** P0
**Where:** spec § D4 (spec.md:98–100); § Design 2 commentary (spec.md:281–289 and :296–299)
**Edge case:** Same as F-1 — more answered claims than the cap, in any round.
**What happens:** D4 reads: *"Not counted against the rendered-item cap; **the number of checks per round is bounded by the fact requests the previous round rendered**. This deletes attempt 1's overflow-ordering rule and **its last-round hole**."* Design 2's own commentary directly refutes the first clause: *"the claims answered in one round are **not** bounded by that round's rendered fact requests — Open F-items accumulate to `(round_cap + 1) × question_cap`"* (:283–285). This is the exact sentence round-2 edge-cases F-1 identified as false; it was deleted from the shipped blockquote and left standing in the carried-decision section, which the spec presents in its own voice as "honored by Design 2".

The second clause is now also false in a narrower way: attempt 1's last-round hole was *every* claim answered in the last rendered round; this spec's hole is the surplus beyond the cap in the last rendered round. Design 2's *"**The last-round hole is closed.** … Here that claim's check runs before the hand-off, so the last round is not a special case"* (:296–299) is contradicted by :265–267, under which the last round **is** a special case — it is the one round whose surplus has no next batch.

`/spec-close` decomposes D-sections into wiki decisions, so a false carried decision propagates past this ticket.
**Why the spec misses it:** The round-2 fold edited the Design section and the commentary that justified it, not the decision restatement upstream of them.
**Suggested fix:** D4: replace the bound clause with *"the checks a round can fire are bounded by the outstanding `F<n>` items, and the check batch carries its own `question_cap` cap with a surplus rule (Design 2)"*; replace "and its last-round hole" with *"and its unconditional last-round hole — a claim answered in the last rendered round is checked, unless the batch cap was already full"*. Design 2 :296–299: retitle to "The last-round hole is closed for every claim the batch cap reaches" and state the residue.

### F-3: On the confirmed path the operator's wording enters `### Facts established` with no normalization rule
**Severity:** P1
**Where:** spec § Design 3 shipped blockquote (spec.md:303–306); vs the same blockquote's normalization clause (spec.md:310–315)
**Edge case:** The **modal success path** — the check confirms — with an operator answer containing a newline (a pasted log or a two-line quote), a `(source:` fragment, or a leading `- `.
**What happens:** Design 3 ships *"the operator's wording **may stand as the fact text**"*, and `:132`'s established form is `- F1 — <fact> (source: <path:line>)` — another one-item-per-line entry in the same parsed contract. The normalization the spec just added is scoped away from this path by its own words: *"The operator's answer travels in the `claim:` field of that F-item line — **the field renders for this reason value alone** — held to one line: whitespace collapsed…"*. So the guard covers the failure branch and not the success branch, and a newline in a confirmed claim splits `### Facts established` into a real bullet plus a phantom one, which `/spec-brief:142` then writes into `## References` with a `path:line` attached to the wrong text. A `(source: …)` fragment inside the operator's wording gives the line two sources.

This is round-2 F-3's root on its third channel: Design 1 hardened the exploration prompt, Design 3 hardened the `claim:` field, and the one channel that reaches the block on the path the ticket is *designed* to produce is unguarded. It is also the only channel where corrupt text arrives carrying an exploration-found `path:line`, i.e. dressed as an established fact.
**Why the spec misses it:** D6 and the brief phrase "the operator's wording may be kept as the fact text" as a courtesy about *authorship*, not as a text-transfer path; the round-2 fold reasoned about the Open item because that is where the new field lives.
**Suggested fix:** One clause on the confirmed sentence: *"…and the operator's wording may stand as the fact text, held to one line by the same normalization as the `claim:` field below."* Add to row 4 or row 3: the `**Two outcomes.**` paragraph contains "by the same normalization" (or equivalent), so the confirmed path is pinned too.

### F-4: A claim whose check the batch cap deferred leaves the gated question in a third state the rule does not disposition
**Severity:** P2
**Where:** spec § Design 6 shipped blockquote (spec.md:387–397); § Design 2 shipped blockquote (spec.md:265–267)
**Edge case:** A question is `blocked-on: F5`; the operator answers `F5`; `F5`'s check falls in the surplus and is deferred to the next round's batch.
**What happens:** The paragraph disposition two states and the surplus creates a third. *"**Once a claim's check has resolved**, the question waiting on it enters the next round's frontier whether the claim was confirmed or not"* — the check has **not** resolved, so no directive fires. But the paragraph's own closing rule says *"A question is left waiting **only** for a fact need that is still unanswered"* — and this fact need **is** answered, so the question may not be left waiting either. The implementer must invent one of: render it with the not-confirmed note (asserting an unverified status the check has not determined, and which may be reversed next round when the check confirms), render it bare (the operator settles a decision on a claim nobody has checked and is not told so — the brief's § Why it matters failure), or leave it waiting against the paragraph's explicit "only". All three degrade rather than crash, which is why this is P2 and not higher.
**Why the spec misses it:** The two-branch rule is the round-1 F-5 / round-2 F-2 fold, written when every answered claim's check resolved before the following round was rendered. The surplus rule broke that invariant in a different Design this round.
**Suggested fix:** One clause in the gated-question paragraph: *"…A question whose claim is answered but whose check the batch cap deferred waits one more round for that check, and where the interview ends first it reaches the hand-off under the exit's own reason."* That keeps the "only … still unanswered" sentence true by naming the deferral explicitly.

### F-5: A replaced claim's queued check has no disposition — one `F<n>` can occupy two slots in the same check batch
**Severity:** P2
**Where:** spec § Design 1 shipped blockquote (spec.md:222–226); § Design 2 shipped blockquote (spec.md:265–267)
**Edge case:** `F5` is answered in round 2 and lands in the surplus (unchecked). In round 3 the operator answers `F5` again with a corrected claim.
**What happens:** Design 1 ships *"a later answer to the same `F<n>` **replaces the claim and gets its own check**"*; Design 2 ships that the surplus *"is checked in the next round's check batch"*. Round 3's batch therefore has two grounds to contain `F5`: the queued surplus entry (for the superseded claim) and the new answer's own check. Nothing says the queued entry is dropped, retargeted at the current claim, or dispatched as-is. An implementer either (a) fires two checks for one item — two of `question_cap`'s slots for one fact, and two outcomes for one `F<n>`, with the superseded claim able to confirm and put a **retracted** claim into `### Facts established` under an exploration-found `path:line`, or (b) fires one and must decide which claim it carries.

Note that this is the *only* live version of the "second answer while a check is in flight" case: outside the surplus, a check batch resolves before the round that would follow is rendered (:264–265) and a hung check blocks that round, so the operator can never type a second answer while a dispatched check is genuinely in flight. The queue is what makes it reachable.
**Why the spec misses it:** The replacement rule (round-2 F-6 fold) and the surplus queue (round-2 F-1 fold) were written this round, in different Designs, against the same `F<n>` identity.
**Suggested fix:** Extend the replacement clause: *"…replaces the claim and gets its own check — the item is checked once, against its current claim, so a check the batch cap has not yet dispatched carries the replacement rather than the text it superseded."*

### F-6: The surplus queue has no batch to ride in a round where nobody answers a claim, and "oldest `F<n>` first" ranks the fact need, not the wait
**Severity:** P2
**Where:** spec § Design 2 shipped blockquote (spec.md:262–267); commentary (spec.md:272–279)
**Edge case (a):** Round N leaves two claims in the surplus. In round N+1 the operator answers only questions — no `F<n>` at all.
**What happens:** The batch's existence is conditioned on an answer: *"**At once, on the answer** … Dispatch **the answers' checks** in one parallel batch."* With no answers there are no "answers' checks", so on a literal reading no check batch is dispatched and the surplus rides again — through as many claim-free rounds as the interview has, then reaches the hand-off unchecked while `question_cap` slots stood empty every round. The disposition is safe (Design 3's sixth cause) but the outcome is wrong and silent: the primitive had capacity and did not use it.
**Edge case (b):** Ordering. `F<n>` numbers are monotonic in the order fact *needs* were raised (`:48`), not in the order claims were *answered*. So "oldest `F<n>` first" can starve a long-waiting surplus claim: a round-1 surplus on `F20` is displaced in every later batch by freshly answered low-numbered items (`F3`, `F5`, …), round after round, while the label "oldest" suggests the opposite. It is deterministic and bounded, so it degrades rather than breaks — but the shipped text also does not say whether the key orders the surplus alone or the whole batch (the commentary at :277–279 implies the whole batch; the shipped sentence attaches it to "the surplus").
**Why the spec misses it:** The surplus rule was written to close a cap-overflow hole in one round and not as a queue with a lifetime across rounds.
**Suggested fix:** (a) *"…the surplus is checked in the next round's check batch — which is dispatched for the surplus whether or not that round produced new answers — oldest `F<n>` first."* (b) Either say the key orders the whole batch and accept the inversion in one clause of the commentary, or make the key "the longest-waiting claim first, `F<n>` order breaking ties".

### F-7: The `claim:` length bound is stated in a unit this spec defines as unbounded
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 shipped blockquote (spec.md:312–315); § Design preamble (spec.md:190–193); Test plan row 4 (spec.md:605–612)
**Edge case:** An operator pastes a 200-line log as `F3 <answer>`.
**What happens:** The normalization collapses whitespace to single spaces, so the paste becomes **one line** — which satisfies "held to one line" completely. The only length bound is *"elided with an ellipsis where it would run past one line of prose"*, and the spec's own preamble states that these files are unwrapped, *"so a 'line' below is a whole paragraph"*. Under the spec's own definition of a line in this file, a multi-kilobyte single paragraph never "runs past one line of prose" and no elision is required. `:137`'s size bound counts items, not bytes, and is fenced byte-identical, so nothing else stops it. The result rides into the hand-off block and, through Design 11, into a `## Risks / decisions` bullet. Nothing in row 4 or row 17 is checkable against it — a reviewer running the gate has no test to apply, which is the half of round-2 F-3 that survives.

Degrades (bloat, not corruption) rather than breaks, hence P2 rather than F-3's original P1.
**Suggested fix:** Give the elision a unit the file does not redefine: *"…elided with an ellipsis where it runs past roughly one sentence"*, or a stated character bound. Add the chosen phrase to row 4's pinned list so the gate can check it.

### F-8: `/spec-brief` has no rule for a `claim:` field that normalization emptied, and the marker exclusion does not say how it is achieved
**Severity:** P2
**Where:** spec § Design 3 shipped blockquote (spec.md:313–315); § Design 11 (spec.md:507–512)
**Edge case:** An answer whose whole content is one of the excluded markers or reduces to nothing under normalization — e.g. `F3 unresolved because: I never checked`, or an answer that is only punctuation the normalizer rewrites.
**What happens:** Two gaps compound.

1. The rule states an outcome (*"never carrying the block's own `ref:` or `unresolved because:` markers"*) without a mechanism. Strip, elide-from-the-marker, or refuse the field are all faithful readings, and they differ: stripping can leave `claim: ""`, eliding can leave `claim: "…"`, refusing leaves an item under the qualifier with no field at all. Design 1's non-answer rule does not catch it — the body is not empty and does assert something checkable; it becomes empty only *after* normalization.
2. Design 11 takes `<answer>` from the field with no rule for absent or empty, so it writes `<fact needed> — operator claims "", unverified; spec author pins this` — a brief bullet that asserts the operator claimed nothing and is strictly worse than the plain `— not established` form the same mapping already has. Round-2 edge F-4's suggested Design 11 clause for the field-absent case was not folded, and the Design 8 fix that closed F-4 covers only the reason-value branch.

The marker list is also short: the block's fields include `branches:`, `recommendation:`, `Facts relied on:`, `source:` and `claim:` itself, and an answer containing `claim:` or `source: operator` re-enters the spoofing case the rule was written to close.
**Why the spec misses it:** The normalization is a round-3 fold to a round-2 finding about *content* and was not walked back through `/spec-brief`, which is the consumer the same fold cites (:328–331).
**Suggested fix:** Design 3: *"…markers, which are removed; where nothing checkable survives, the answer is not a claim and the rule above applies."* Design 11: *"An item carrying the qualifier with no `claim:` field, or an empty one, is written with the plain `— not established` form."* Widen the marker phrase to "any of the block's own field markers".

### F-9: The resume paragraph's unqualified "not re-dispatched" reads across a fresh answer on the resumed round
**Severity:** P3
**Where:** spec § Design 6 shipped blockquote (spec.md:399–404); vs § Design 1 (spec.md:222–226)
**Edge case:** A post-cap resume round in which the operator answers a carried Open `F<n>`.
**What happens:** Design 1 says *"In any round, the operator may answer a fact request that has already become an Open item"* → a check. The resume paragraph says the carried item *"is not re-dispatched, qualifier or not, downstream or not"* — three emphatic qualifiers and no exception for a fresh answer. The two rules are about different triggers (carry-over vs. a new answer) and a careful reader resolves it in Design 1's favour, which is why this is P3 — but on the reading where the resume paragraph wins, the operator's answer on the single post-cap round is silently discarded and the item reaches the brief carrying the claim the operator has just replaced.
**Suggested fix:** Four words on the resume paragraph: *"…and is not re-dispatched — unless the operator answers it again, which is a new claim under the rule above — qualifier or not, downstream or not."*

## Summary
P0: 2 | P1: 1 | P2: 5 | P3: 1 | P4: 0

STATUS: RED P0=2 P1=1 P2=5 P3=1 P4=0
