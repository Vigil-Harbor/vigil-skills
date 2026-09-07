# Correctness Review — round 4

Grounding complete. Read fresh from disk: the spec (`docs/specs/TODO/VHS-36.spec.md`), the brief, `CLAUDE.md`/`AGENTS.md`, the Plane ticket VHS-36 (namespace `skills`, tag-exact hit — description matches the brief), all four target files at `f4d9290` (`git rev-parse HEAD` = `f4d9290`, still HEAD), `docs/specs/DONE/VHS-33/spec.md` `## Test plan` rows 1–16, `docs/specs/DONE/VHS-33/attempt-1/spec.md:410–506`, the VHS-33 wiki decision page, all three round-3 reviewer reports, and Plane VHS-39 / VHS-40 (both exist, Backlog). `git log` on the four touched files shows only the VHS-32/VHS-33 series (`d381f88`…`648f4ff`); nothing landed after the anchors were read.

**On the orchestrator's two specific questions.** (1) The truncation rule is **not** attempt-1 rule 3 returning. Attempt-1 `:495–498` ("A claim answered in the last rendered round is not verified. No extra round is rendered for verification alone") made the last round unverifiable *by construction* for every claim; VHS-36 fires the check on the answer and drops only claims past `question_cap` in **any** round, so the last round is not privileged. It is also not attempt-1's rule 2 (`:481–488`), which ranked verifications against new fact needs inside one shared batch. Different construct; `:87` stays byte-identical. (2) The three D7 wiki quotes are verbatim-accurate against `vigil-harbor-wiki/decisions/2026-09-07-vhs-33-...md` (the `Revisit when:` header, § 3's "Rejected — a cause qualifier on the F-item text", and § 3's "no dispatch is ever active at `stop`, because a batch blocks the round it belongs to"). The supersede/re-assert ledger against VHS-33 `## Test plan` checks out on every row (see F-6 for one count nit).

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Design 7's `stop` sentence asserts a check runs for every answered fact request | CLOSED | spec:472–476 now conditional ("where a check was dispatched for it that check runs… the same qualifier it takes where no check ran at all"); Design 10's `:156` mirror at :547–549 takes the same conditional; row 6 (:685–696) pins "where a check was dispatched for it" / "where no check ran at all"; row 17 item 9 reworded (:789–790) |
| correctness | F-2 (P1) | D4 carries the false bound and a stale attempt-1 claim | CLOSED | bound clause gone from D4 (:96–103); departure paragraph added (:107–117) naming `:90`, `:53` and the Open-F-item accumulation; attempt-1 claim re-scoped at :115–117 (but see F-3, F-6 below) |
| edge-cases | F-1 (P0) | surplus rule makes "its check runs before the hand-off" false | CLOSED at the root | the carry queue is gone; spec:279–283 ships hard truncation ("the rest are not checked at all… no check is ever carried to a later round"). See F-1 and F-2 below for two residues of the fold |
| edge-cases | F-2 (P0) | D4 asserts the abandoned bound / last-round hole deleted | CLOSED | as correctness F-2; Design 2's last-round commentary rewritten (:323–328) to "truncation applies identically to every round" |
| edge-cases | F-3 (P1) | confirmed path enters `### Facts established` un-normalized | CLOSED | spec:334–336 "held to one line by the same normalization as the `claim:` field below"; commentary "Both channels are normalized, not just the Open one" (:371–378); row 3 pins the phrase (:645–646) |
| edge-cases | F-4 (P2) | deferred check leaves gated question undispositioned | CLOSED by construction | no deferral exists; a truncated claim is "Open under the qualifier at once" (:282) and Design 6's "once it is settled that no check will run for it" (:434–435) dispositions it |
| edge-cases | F-5 (P2) | replaced claim occupies two batch slots | CLOSED by construction | no queue; each round's batch is built from that round's answers only (:271–274) |
| edge-cases | F-6 (P2) | queue has no batch to ride; starvation ordering | CLOSED by construction | no queue; a dropped claim is re-requestable by re-answering the same `F<n>` (:238–240, :314–316) |
| edge-cases | F-7 (P2) | `claim:` length bound stated in a unit the spec defines as unbounded | CLOSED | "elided with an ellipsis past about 200 characters" (:346–347); pinned in row 3 (:647) |
| edge-cases | F-8 (P2) | no rule for an emptied `claim:`; marker exclusion has no mechanism | CLOSED | Design 3 "any of the block's own field markers (…) removed… where nothing checkable survives, the answer was not a claim and the rule above applies" (:343–347); Design 11 absent/empty-field rule (:560–562) |
| edge-cases | F-9 (P3) | resume "not re-dispatched" reads across a fresh answer | CLOSED | :447–449 "unless the operator answers it again on the resumed round, which is a new claim under the rule above" |
| conventions | F-1 (P2) | D4 carries the disproved batch-bound premise unflagged | CLOSED | D4 departure paragraph (:107–117) |
| conventions | F-2 (P2) | "first operator-authored string" claim false (`:67`→`:124`) | CLOSED | reworded to "under a machine-read field grammar" (:359–361); `:67`/`:124` gap named and filed as VHS-40 (:366–368, :861–867) — Plane VHS-40 verified to exist, Backlog |
| conventions | F-3 (P2) | Designs 7 and 10 over-claim on `stop` | CLOSED | same evidence as correctness F-1 |
| conventions | F-4 (P4) | row 17 preamble reserves an unused exception | CLOSED | :775 now "no two items may quote the same sentence" |
| correctness | F-3 (P2) | "last-round hole is closed" over-states / disagrees with adjacent commentary | CLOSED | the contradicting paragraph is gone with the queue; :323–328 now says truncation is symmetric across rounds |
| correctness | F-4 (P2) | row 10 mislabelled "Supersedes" | CLOSED | :714 "**Re-asserts VHS-33 checklist rows 5, 7 and 8 verbatim**" (see F-6 for the count nit inside the parenthetical) |
| correctness | F-5 (P3) | surplus presumes a next round's batch that may not exist | CLOSED by construction | no surplus |
| correctness | F-6 (P4) | Design 8 listed among blockquote designs; row 17's vacuous "only where noted" | CLOSED | preamble now "in Design 8's fenced line" (:195–197); row 17 clause dropped |

Nothing REOPENED. Two new findings below are residues of the round-4 queue removal.

## Findings

### F-1: Test-plan row 3 pins a phrase the shipped text does not contain — the gate row cannot pass
**Severity:** P1
**Where:** spec § Test plan row 3 (`VHS-36.spec.md:644–645`) vs § Design 2 shipped blockquote (`:282–283`)
**Claim:** Row 3: "The `**When the check runs.**` paragraph contains, verbatim, … and **"never carried to a later round"**".
**Why this is wrong:** The shipped sentence — which the Design preamble says "ships byte-for-byte" (`:195–197`) — reads:

> `…each is Open under the qualifier at once, and no check is ever carried to a later round.`

`grep -F 'never carried to a later round'` against the edited `skills/grilling/SKILL.md` returns nothing: the file will say *"no check is ever carried"*, not *"never carried"*. I confirmed the whole spec carries only two instances of the string `carried to a later round` (`:282` shipped, `:645` the pin) and they disagree on the preceding words. The checklist **is** the `/ship-spec` gate for this ticket (`## Test command` is `N/A`, spec `:619–620`), so a mechanically-unsatisfiable row turns the gate red on a correctly-implemented change and leaves the implementer choosing between editing a byte-pinned blockquote and editing the gate. The other two pins in the same clause ("up to `2 × question_cap` dispatches in all", "a hard truncation") both match exactly, so this is an isolated slip introduced when the surplus sentence was rewritten this round.
**Suggested fix:** In row 3 (`:644–645`) replace `"never carried to a later round"` with `"is ever carried to a later round"` (or the backtick-free `"no check is ever carried to a later round"`). Do not touch the shipped sentence.

### F-2: The shipped truncation sentence equates the check cap with § Bounds' item cap, which does the opposite on overflow
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 shipped blockquote (`VHS-36.spec.md:279–283`), with its rationale at `:302–304`
**Claim:** "That cap is **a hard truncation, as the per-round item cap is**: … the rest are not checked at all — each is Open under the qualifier at once, and no check is ever carried to a later round." Rationale: "Truncation is this file's own idiom for a cap: § Bounds calls the per-round item cap 'a hard truncation, not a soft target'."
**Why this is wrong:** `skills/grilling/SKILL.md:87` reads, in full:

> `2. **Per-round question cap** — default 7, supplied per invocation. At most `question_cap` rendered items per round, **questions and fact requests together**; overflow carries to the next round. This is a hard truncation, not a soft target.`

The per-round item cap **carries its overflow to the next round** — that clause sits one sentence before the phrase the spec borrows, and `:76` restates it for fact needs ("Fact needs beyond the dispatch cap carry to the next round's batch"). The check cap is the first cap in this file that *discards* the excess. The shipped sentence therefore asserts a likeness ("as the per-round item cap is") on precisely the axis where the two caps differ, three paragraphs above the `:87` a reader can check. The sentence self-corrects after the colon, so the operative behavior is unambiguous and no wrong implementation follows from the spec — but the primitive is prose read by a model, and "hard truncation, as the per-round item cap is" is a live cue toward carry-over. The rationale paragraph inherits the same borrowed authority. (The bare quotation of "a hard truncation, not a soft target" at `:303–304` is accurate; only the equation is not.)
**Suggested fix:** Drop the four words of analogy from the shipped sentence and let the definition stand, e.g. "That cap is a hard truncation: where the operator answered more claims in one round than the cap allows, the batch takes them in `F<n>` order and the rest are not checked at all — each is Open under the qualifier at once, and no check is ever carried to a later round, unlike a rendered item beyond the per-round cap." Adjust the rationale at `:302–304` to cite the phrase as an idiom for cap-enforcement rather than as a precedent for the disposal rule. Row 3's `"a hard truncation"` pin survives either way.

### F-3: D4's departure paragraph says "dispatch at once" stands unchanged, but truncation means some claims get no dispatch at all
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions carried forward, D4 (`VHS-36.spec.md:112–115`)
**Claim:** "Design 2 therefore bounds the **check batch itself** at `question_cap` and truncates at it, rather than relying on a bound that does not exist. **Everything else in decision 4 stands unchanged: dispatch at once**, nothing rendered for a check, no ordering extension at `:87`, and a hung check blocking the hand-off."
**Why this is wrong:** The brief's decision 4 (`VHS-36.brief.md:31`) opens "**one read-only dispatch per claim** when the answer arrives". Under the round-4 truncation rule, a claim past the `question_cap`-th in a round receives **zero** dispatches, ever — `:282` "the rest are not checked at all… no check is ever carried to a later round". So the departure from decision 4 is two-fold, not one: the false bound *and*, as its consequence, the one-dispatch-per-claim guarantee. The paragraph discloses the truncation in the preceding sentence, so a careful reader unravels it — but the closing list is what `/spec-close` decomposes into the decision record, and it reads as "every claim still gets its dispatch, just immediately". This is the same class as round-3 conventions F-1 (a D-section clause the Design then disproves), one clause further in.
**Suggested fix:** Narrow the list: "Everything else in decision 4 stands unchanged in kind: a check that is dispatched fires at once, nothing is rendered for it, § Bounds `:87` needs no ordering extension, and a hung check blocks the hand-off. What the cap removes is decision 4's implicit guarantee that *every* claim gets a dispatch — Design 3 gives a truncated claim a stated outcome instead."

### F-4: "unblocks nothing by being early" no longer describes what the check batch's ordering key decides
**Severity:** P3
**Where:** spec § Design 2 commentary (`VHS-36.spec.md:293–295`)
**Claim:** "the check batch carries its own one-key order — oldest `F<n>` first — which needs neither tree depth nor blast radius, because a check is not a rendered item and **unblocks nothing by being early**."
**Why this is wrong:** That rationale was sound while the surplus queue existed, where position in the order changed only *when* a check ran. Under truncation, position decides **whether** a claim is checked at all: everything past `question_cap` resolves to `fact not established (operator claim, unverified)` permanently (`:282`). "Unblocks nothing" remains literally true — Design 6 renders the gated question either way (`:432–439`) — but the sentence is now the spec's only defence of the ordering key at the moment that key became a selection rule, and blast radius is exactly the key one would reach for when choosing which claims to spend the budget on. Not a behavior defect (the disposition of every dropped claim is stated), so it is rationale accuracy rather than a hole.
**Suggested fix:** Extend the clause: "…because a check is not a rendered item and unblocks nothing by being early — under the cap the order decides which claims are checked at all, and oldest-first matches § Bounds' own 'carried-over and re-asked items first' priority rather than inventing a second ranking."

### F-5: Design 10's failure-mode bullet omits the batch-cap cause that Design 12's `/grill-me` bullet is required to name
**Severity:** P3
**Where:** spec § Design 10, new § Failure modes bullet (`VHS-36.spec.md:537–541`) vs § Design 12 (`:583–589`) and Test plan row 12 (`:742–749`)
**Claim:** "- **Operator claim not checked** (a failed check, a check that could not be dispatched, or a claim with no repo footprint) — …"
**Why this is wrong:** The spec is explicit that the label arises from **seven** situations, and row 12 makes `/grill-me`'s bullet enumerate all seven, including "the round's check batch was too full to take it" (`:592–595`, `:744–747`). The primitive's own failure-mode bullet — the one a reader of `skills/grilling/SKILL.md` hits first — names three, and truncation is at best implicit in "a check that could not be dispatched" (which more naturally reads as the no-read-restricted-agent-class case, already its own bullet at `:154`). The bullet does point at § Fact-finding and § Termination, so nothing is unreachable; the asymmetry is that the caller's failure modes are more complete than the primitive's about a rule the primitive owns.
**Suggested fix:** Three words in the parenthetical: "(a failed check, a check that could not be dispatched or that the round's check batch was too full to take, or a claim with no repo footprint)". No test-plan row change needed — row 8 pins only the bullet's opening and position.

### F-6: Three bookkeeping inaccuracies
**Severity:** P4
**Where:** spec `:115–116`, `:116`, `:716`
**Claim:** (a) "Attempt 1's ***cross-batch*** ordering rule"; (b) "(`attempt-1/spec.md:476–488`)"; (c) row 10: "**two anchors** are re-translated for post-VHS-33 numbering".
**Why this is wrong:** (a) Design 2 describes the same rule correctly nine lines later as ranking "verifications against new fact needs **inside one batch**" (`:288–289`), and attempt-1 `:481–488` says "**within a round's batch**, new fact needs are dispatched before verifications". "Cross-batch" is the one word in the spec that mis-describes it; "shared-batch" or "cross-kind" is what the rest of the spec means. (b) `attempt-1/spec.md:476–477` is the tail of rule 1 ("this one is not, so waiting would render nothing…"); rule 2 begins at `:478` and its overflow paragraph runs `:481–488`. (c) Comparing VHS-33 row 5's anchors (`:12`, `:70`, `:37–44`, `:61`, `:84–86`, `:94–98`, `:23`) against VHS-36 row 10's (`:12`, `:72`, `:37–44`, `:63`, `:86–88`, `:96–100`, `:23`), **four** are re-translated, not two — `:70`→`:72`, `:61`→`:63`, `:84–86`→`:86–88`, `:94–98`→`:96–100`. Every translated anchor is itself correct against the file at `f4d9290`; only the count is wrong (it was inherited verbatim from round-3 correctness F-4's suggested wording).
**Suggested fix:** (a) "Attempt 1's *shared-batch* ordering rule"; (b) cite `attempt-1/spec.md:478–488`; (c) "four anchors are re-translated".

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=2 P3=2 P4=1
