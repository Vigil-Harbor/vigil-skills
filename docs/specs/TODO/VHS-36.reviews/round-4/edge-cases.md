# Edge-Cases Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Surplus rule falsifies "its check runs before the hand-off", twice | CLOSED | Queue removed (spec:279–283). Design 7 now conditional — "where a check was dispatched for it that check runs before the hand-off … the same qualifier it takes where no check ran at all" (spec:473–476); mirrored at `:156` (spec:546–549); row 6 pins both phrases (spec:685–696) |
| edge-cases | F-2 | D4 carries the bound Design 2 disproved | CLOSED | spec:105–117 — explicit departure paragraph; "Attempt 1's *cross-batch* ordering rule … is deleted outright" |
| edge-cases | F-3 | Confirmed path enters `### Facts established` unnormalized | CLOSED | spec:335–336 "held to one line by the same normalization as the `claim:` field below"; commentary spec:370–378; row 3 pins the phrase |
| edge-cases | F-4 | Deferred check leaves the gated question in a third state | CLOSED | No deferral exists; Design 6 gains "or once it is settled that no check will run for it" (spec:432–433), pinned by rows 3 and 5 |
| edge-cases | F-5 | Replaced claim's queued check can occupy two batch slots | CLOSED | No queue; one check per answer, dispatched at once. Residue in a different direction → new F-6 below |
| edge-cases | F-6 | Queue has no batch to ride; `F<n>` key ranks the need, not the wait | PARTIAL | Queue half dissolved. The key half survives in stronger form: `F<n>` order is now *terminal* rather than merely delaying, its direction ships nowhere, and the rationale that justified the one-key order is stale → new F-2 (P2, original severity kept) |
| edge-cases | F-7 | Length bound stated in a unit the spec defines as unbounded | CLOSED | spec:345–346 "elided with an ellipsis past about 200 characters"; row 3 pins "past about 200 characters" |
| edge-cases | F-8 | No mechanism for the marker exclusion; no rule for an emptied field | PARTIAL | Markers now "removed" and the list widened (spec:343–345); Design 11 gains the empty-field fallback (spec:560–562). Residue: *when* the emptiness test fires → new F-5 (P2, original severity kept) |
| edge-cases | F-9 | Resume's unqualified "not re-dispatched" vs a fresh answer | CLOSED | spec:447–448 "unless the operator answers it again on the resumed round, which is a new claim under the rule above"; row 5 unchanged |
| correctness | F-1 | Design 7's `stop` sentence asserts a check for *every* answered request | CLOSED | Same evidence as edge-cases F-1; both no-check causes named in the shipped sentence |
| correctness | F-2 | D4 carries the false bound; "deletes the overflow rule" no longer holds | CLOSED | spec:105–117 |
| correctness | F-3 | "The last-round hole is closed" over-states its own design | CLOSED | spec:324–328 rewritten — truncation is round-agnostic, so the claim now holds. Its new wording introduces a separate defect → new F-4 |
| correctness | F-4 | Row 10 labelled "Supersedes" for rows it re-asserts | CLOSED | spec:714 "**Re-asserts VHS-33 checklist rows 5, 7 and 8 verbatim**" |
| correctness | F-5 | Surplus presumes a next round's batch | CLOSED | Dissolved with the queue |
| correctness | F-6 | Two nits (Design 8 in the blockquote list; vacuous "where noted") | CLOSED | spec:195–198 lists "Design 8's fenced line" separately; spec:775 now "no two items may quote the same sentence" |
| conventions | F-1 | D4 premise unflagged | CLOSED | spec:105–117 |
| conventions | F-2 | "first operator-authored string" false against `:67`/`:124` | CLOSED | spec:360–368 "under a machine-read field grammar"; gap filed as VHS-40 (spec:861–867) |
| conventions | F-3 | Designs 7/10 promise the check unconditionally | CLOSED | Same as edge-cases F-1 |
| conventions | F-4 | Row 17 reserves an unused exception | CLOSED | spec:775 |

`scale_lens` is `off`; the stale `scalability.md` in round-3 is out of scope and was not read for closure.

## Findings

*(Persistence checklist: N/A — prose-only change. The primitive writes no file, and keeps no state beyond `prior_summary`, which the caller owns; the round-4 rewrite removed the one construct that would have added cross-round state.)*

*(Attempt-1 rule-3 check, as asked: **truncation is not that rule under another name.** Attempt 1's rule 3 dropped **every** claim answered in the last rendered round, unconditionally and by construction, because the check was dispatched in the *following* round — `docs/specs/DONE/VHS-33/attempt-1/spec.md:498–506`. Here the check fires on the answer, so the last rendered round's claims are checked up to the cap, and the drop is cap-driven and round-agnostic. The only residual last-round asymmetry is in the *mitigation*, not the rule — see F-3.)*

### F-1: Checklist row 3 pins a phrase the shipped truncation sentence does not contain
**Severity:** P0
**Where:** spec § Test plan row 3 (`VHS-36.spec.md:644–646`) vs § Design 2 shipped blockquote (`:279–283`)
**Edge case:** Not an input edge — a gate edge. `## Test command` is `N/A`, so this checklist **is** the `/ship-spec` gate (spec:619–621), and row 3 asserts three strings "verbatim".
**What happens:** The row asserts the `**When the check runs.**` paragraph contains, verbatim, `"never carried to a later round"`. The paragraph ships (byte-for-byte, per the Design preamble) as:

> …each is Open under the qualifier at once, and **no check is ever carried to a later round**.

`grep -F 'never carried to a later round'` returns nothing against that text. The other two pins in the same clause do match ("up to `2 × question_cap` dispatches in all", "a hard truncation"), and every other new pin I checked this round matches (`held to one line by the same normalization`, `normalized to one line`, `past about 200 characters`, `where nothing checkable survives`, `In any round`, `replaces the claim`, `or once it is settled that no check will run for it`, `is not among the abandoned`, `where a check was dispatched for it`, `where no check ran at all`, `blocks the hand-off`, `is not abandoned`, `check batch was too full`, `taken from the item's claim: field`, and the Design 8 fence line against row 4). So this is the single stale pin — but a shipper who implements the spec faithfully fails its own gate, and a shipper who makes the gate pass has silently edited a byte-for-byte blockquote.
**Why the spec misses it:** The truncation sentence and the row-3 pin were written in the same round-4 fold; the pin was written from the intent ("no carry") rather than from the shipped wording, which uses the `no … ever` construction instead of `never`.
**Suggested fix:** Change row 3's third pin to `"is ever carried to a later round"` (or `"no check is ever carried"`), matching the blockquote. Do not edit the blockquote — it is the more natural sentence and Design 7/`:156` do not depend on the wording.

### F-2: The truncation key ships without a direction, and the direction the commentary intends drops the freshest fact requests first
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 shipped blockquote (`:280–282`); commentary (`:288–295`)
**Edge case:** More answered claims in one round than `question_cap` — the case the rule exists for.
**What happens:** The shipped sentence is the only text a reader of `skills/grilling/SKILL.md` gets, and it says the batch "takes them in `F<n>` order". It never says *which* direction, and "`F<n>` order" also reads as "in the order the `F<n>` answers were given". The stated direction lives only in non-shipping commentary ("the check batch carries its own one-key order — oldest `F<n>` first"). Two implementers can therefore drop two different sets of claims, permanently and silently, from the same transcript. Nothing in row 3, row 17, or the reading gate pins the direction (item 4 asks how many, not which).

On the substance of the key: ascending `F<n>` = oldest fact *need* first. Those are the claims for Open items the operator volunteered from earlier rounds, whose gated questions have usually already been rendered or resolved. The claims it truncates first are the highest-numbered — this round's freshly rendered fact requests, which are exactly the ones gating the *next* round's frontier. Under Design 6 the gated question still renders, so nothing blocks; but it renders with an unverified note where a check would have established the fact. So the key preferentially spends the batch on the claims with the least live downstream and drops the ones with the most. It is defensible as consistency with § Bounds `:87` ("carried-over and re-asked items first") — but `:87`'s carry is a *delay*, and this one is terminal, so the analogy does not transfer without saying so.
**Why the spec misses it:** The order key is inherited verbatim from the round-3 queue, where it ranked a delay. The rationale at `:294–295` still argues from that world — "a check … unblocks nothing by being early" is true of blocking, but under truncation position now decides *established fact* vs. *permanently unverified*, which the same sentence dismisses as not needing "blast radius".
**Suggested fix:** Two words in the shipped sentence: "…the batch takes them in ascending `F<n>` order (lowest first) and the rest are not checked at all…". Add `"ascending"` (or `"lowest first"`) to row 3's pinned list. In the `:288–295` commentary, replace "unblocks nothing by being early" with the true form — "no question is blocked by a check's lateness (Design 6 renders it either way), so the key needs no tree depth or blast radius; what it decides is which claims are checked at all, and `F<n>` order settles that deterministically."

### F-3: A truncated claim is silent to the operator, so the mitigation the spec rests the design on cannot be exercised
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 commentary (`:313–316`); § Design 2 shipped blockquote (`:280–283`); § Design 6 (`:432–438`)
**Edge case:** The operator answers `question_cap + k` claims in a round; `k` of them are never checked.
**What happens:** Nothing is rendered for a check by design ("Nothing is rendered for a check"), and nothing is rendered for a *missing* check either. The operator observes:

- If a question was gated on that `F<n>`: a one-line note next round saying the claim is unverified — indistinguishable from a claim the check ran on and refuted.
- Otherwise: nothing at all until the hand-off block, where the item reads `unresolved because: fact not established (operator claim, unverified)` — the same string all seven causes produce.

The spec's stated remedy is "the operator can re-request by answering the same `F<n>` again in a later round (Design 1)". To exercise it the operator must know *which* of their answers were dropped, and they are never told; an Open F-item is not re-rendered in later rounds (`:66`'s re-ask is for questions; `:90` only covers unanswered ones). And in the last rendered round — including `stop` and the single post-cap resume round — there is no later round at all, so the remedy is unavailable exactly where the loss is final. The outcome is safe (the claim still reaches the brief in its `claim:` field, labelled, for the spec author), which is why this is P2 and not higher — but the argument that carried the round-4 redesign presumes a recovery path the operator cannot see or, at the end, reach.
**Why the spec misses it:** Under the round-3 queue the surplus was recovered by the primitive, so no operator action was needed; the round-4 fold replaced the mechanism and kept the "it's recoverable" framing without re-deriving who has to act.
**Suggested fix:** Either (a) one clause in the shipped sentence — "…and the rest are not checked at all: each is Open under the qualifier at once, and the next rendered round names those `F<n>` in one line so the operator may answer them again" (a note, not a rendered item, so `question_cap` is untouched) — or (b) if the silence is intended, say so in the commentary and drop the recovery claim: "the operator is not told which claims the cap dropped; the recovery path is the labelled `claim:` field the spec author reads, not a re-answer."

### F-4: "Truncation costs at most one check" / "the one claim it drops" understates the loss by up to `round_cap × question_cap`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 commentary (`:313–316` and `:324–328`)
**Edge case:** The spec's own reachability argument — Open F-items accumulate to `(round_cap + 1) × question_cap` and `:53` accepts any of them, so under the defaults an operator can answer 14–28 claims in one round against a batch cap of 7.
**What happens:** Two commentary sentences describe truncation as dropping a single check: "Truncation costs **at most one check** that the operator can re-request…" and "…the **one claim** it drops is dropped for the same reason in round 1 as in the last." Both are quantitatively false against the same section's reachability paragraph (`:298–304`): the drop is `answered − question_cap`, up to 21 claims under the defaults. Nothing ships from these sentences, so no wrong behavior follows — but they are the cost side of the truncation-vs-queue trade the whole round-4 rewrite turns on, and `/spec-close` decomposes this section into the decision layer, where "costs at most one check" would read as a settled fact about the primitive.
**Why the spec misses it:** The sentences were written against the mental model of a batch overflowing by a little; the reachability paragraph that gives the real magnitude sits fifteen lines above and was written for a different purpose (justifying that the edge exists at all).
**Suggested fix:** `:313–316`: "Truncation costs the checks past the cap — up to `answered − question_cap` in a round, each of which the operator can re-request…". `:324–328`: "…and the claims it drops are dropped for the same reason in round 1 as in the last."

### F-5: The "nothing checkable survives" test fires at render time, after the dispatch it is meant to prevent
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 shipped blockquote (`:341–347`); vs § Design 1 (`:226–229`); § Design 11 (`:560–562`)
**Edge case:** An answer whose whole content is field markers or punctuation — `F3 unresolved because: source:` — i.e. an answer that is non-empty on arrival and empty only after normalization.
**What happens:** The clause "where nothing checkable survives, the answer was not a claim and **the rule above applies**" sits inside the sentence that describes how the `claim:` field is *rendered* — a hand-off-time operation. But "the rule above" (Design 1) is an *intake* rule with two intake consequences: "no check is dispatched, and the fact request counts as unanswered under § Bounds." Neither can be applied at render time: a check has already been dispatched (a wasted slot in a batch this same Design says truncates at `question_cap`), and § Bounds' unanswered accounting drives a re-ask in the *next* round, which by then may not exist. For a truncated claim the collision is direct — the shipped truncation sentence says it "is Open under the qualifier at once", while this clause says the same item is not a claim at all and therefore takes the plain `fact not established` reason.

Design 11's fallback ("An item carrying the qualifier with no `claim:` field, or an empty one, takes the plain … form") is the tell: it dispositions a state Design 3 declares unreachable. Defensive, and it keeps `/spec-brief` safe — but the two rules disagree about whether that state exists, and only one of them is in the primitive.
**Why the spec misses it:** The clause is the round-4 fold to round-3 F-8, which was raised as a *content* question (what does the field hold?) and answered in the field-rendering sentence, not walked back to the intake sentence where its consequences live.
**Suggested fix:** Move the test to intake. Design 1: "An answer that asserts nothing checkable — an explicit non-answer such as 'I don't know', an empty body, **or an answer that survives the normalization below as nothing** — is not a claim…". Design 3 then reads "…and the whole elided with an ellipsis past about 200 characters; an answer that survives this as nothing was not a claim, under the rule above." Row 3's `"where nothing checkable survives"` pin moves with it (or becomes `"survives the normalization below as nothing"`).

### F-6: A re-answered Open `F<n>` that confirms — nothing says the Open entry is withdrawn
**Severity:** P3
**Where:** spec § Design 1 (`:236–240`); § Design 3 (`:332–336`); § Design 4 (`:388–390`)
**Edge case:** `F5` goes Open (twice unanswered, or truncated); in a later round the operator answers it and the check confirms.
**What happens:** Design 1 creates the first path by which an Open F-item can resolve mid-interview — before this ticket an Open F-item stayed Open by construction. Design 3 says the confirmed fact "goes to `### Facts established`", but no sentence says the item leaves `### Open frontier`. An implementer that models the F-item as *appended to* rather than *moved between* sections renders `F5` twice, and `/spec-brief` then writes it into `## References` (established, with a `path:line`) **and** `## Risks / decisions` (operator claims X, unverified) of the same brief — the exact outcome Design 4 forbids ("The two never share a number — one `F<n>` must not resolve to both an established fact in a brief's `## References` and an unestablished one in its `## Risks / decisions`").

P3 rather than higher because Design 4's invariant, though stated for the contrary-evidence case, is worded generally enough for a careful reader to apply here, and "the fact need is Open with…" / "the fact goes to…" read naturally as one item with one current state.
**Why the spec misses it:** The replacement rule (Design 1) and the two-outcome rule (Design 3) were written against a claim's *first* check; the Open→established transition is a consequence of the two together and is not stated in either.
**Suggested fix:** Five words on Design 3's confirmed branch: "…the fact goes to `### Facts established`, **leaving the Open frontier if it was there**, sourced by the `path:line`…". Or extend Design 1's replacement clause: "…replaces the claim and gets its own check, whose outcome replaces the item's disposition."

### F-7: The rendered gated-question note is a fourth boundary the operator's string crosses; the commentary counts three
**Severity:** P3
**Where:** spec § Design 3 commentary (`:376–378`); § Design 6 shipped blockquote (`:436–438`)
**Edge case:** A multi-kilobyte or newline-bearing claim that was not confirmed, gating a question that renders next round.
**What happens:** The commentary asserts "this is one string across three boundaries — the exploration prompt, the established fact, and the `claim:` field — and all three are stated." Design 6 ships a fourth: the gated question is "rendered with a one-line note giving the claim's text and its unverified status". That note is a rendered round, so the damage is cosmetic rather than contractual, and "one-line note" plus "the same information the hand-off will carry" bounds it by implication — which is why this is P3 and not P2. But the enumeration is what `/spec-close` decomposes as the reason the normalization exists, and it under-counts its own channels.
**Suggested fix:** Either name the fourth channel in the commentary ("four boundaries — the exploration prompt, the established fact, the `claim:` field, and the gated question's note, which carries the same normalized text"), or make the shipped note explicit: "…a one-line note giving the claim's text **in its normalized form** and its unverified status".

### F-8: § Failure modes' new bullet does not name truncation among its three groups
**Severity:** P4
**Where:** spec § Design 10 shipped bullet (`:538–541`)
**Edge case:** An operator (or a `/grill-me` user) looks up why a claim came back unverified, in the section built for exactly that lookup.
**What happens:** The bullet's parenthetical is "(a failed check, a check that could not be dispatched, or a claim with no repo footprint)" — three groups covering the seven causes only if the reader files "the round's check batch was too full" under "could not be dispatched". Design 12's `/grill-me` bullet names all seven explicitly and row 12 greps for "check batch was too full"; the primitive's own failure-mode bullet is the one surface where truncation is reachable by inference alone.
**Suggested fix:** Four words: "(a failed check, a check that could not be dispatched **or that the round's batch cap truncated**, or a claim with no repo footprint)". Row 8 already asserts the bullet's lead and position; no new pin needed.

## Summary
P0: 1 | P1: 0 | P2: 4 | P3: 2 | P4: 1

STATUS: RED P0=1 P1=0 P2=4 P3=2 P4=1
