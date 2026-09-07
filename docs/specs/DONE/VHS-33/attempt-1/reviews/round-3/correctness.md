# Correctness Review — round 3

Grounding: spec and brief read fresh; VHS-33 Plane record retrieved from the `skills` namespace (confirms no "Done when" section in the ticket); both CLAUDE.md files read; every path:line anchor verified against HEAD `7403cb5`; the checklist's greps and `python lint.py --strict` executed; `git log` run on the five touched files; all three round-2 reports read.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Open frontier "three shapes" vs "two" | CLOSED | All 5 sites now say three Open shapes / four total: spec:28, :32, :234, :660, :775 |
| correctness | F-2 (P2) | Row 10 pins `options 1–3` at 4 vs new bullet | CLOSED | spec:568–573 uses "re-renders with 1–3"; verified `grep -c 'options 1–3'` = 4 and `'with 1–3'` = 2 (`:703`, `:708`) |
| correctness | F-3 (P2) | fence-empty line drops `not grillable` | CLOSED | spec:552, :555–561; `spec-cycle:700–703` verified |
| correctness | F-4 (P2) | Design 7 collides with `spec-brief:139` | CLOSED | spec:596–609 |
| correctness | F-5 (P2) | `stop` erases operator-claim qualifier | **PARTIAL** | Structural half fixed (spec:277–294); substantive half neither remedied nor recorded as accepted — see F-3 below |
| correctness | F-6 (P3) | roll-up says "four-way" | CLOSED | spec:76–77 |
| correctness | F-7 (P3) | round-1 preamble undefined | CLOSED | spec:456–462; row 9 asserts it |
| correctness | F-8 (P3) | § Deferred blanket "all folded" claim | CLOSED | spec:905–926; residual sentence at :928 now reads "Every **other** …", spot-verified against all 26 round-1/round-2 P2+ findings and holds |
| correctness | F-9 (P3) | D9 extends-vs-supersedes not in roll-up | CLOSED | spec:83–86 quotes brief `:44` verbatim |
| edge-cases | F-1 (P0) | precedence contradicts stop example | CLOSED | spec:277–302; `:108` named in Scope |
| edge-cases | F-2 (P1) | rule 1 reinstates the retry | CLOSED | spec:352–361; never-returns preserved at :363–367 |
| edge-cases | F-3..F-6, F-8, F-10, F-12..F-17 | — | CLOSED | see round-3 edge-cases report |
| edge-cases | F-7 (P2) | zero-item resume burns post-cap round | CLOSED (fix introduces F-1 below) | spec:411–416 |
| edge-cases | F-9, F-11 | — | DEFERRED (accepted) | spec:912–924 + Risks 5, 6 |
| conventions | F-1..F-4 | — | CLOSED | spec:65–67, :596–601, :905–911, :125–131 |

## Findings

### F-1: The round-2 fix for edge-cases F-7 amends `grilling/SKILL.md:23`, which the Scope table does not authorize, checklist row 5 forbids, and D9's rationale denies

**Severity:** P0
**Where:** spec § Design 4 (spec.md:411–416) vs § Test plan row 5 (spec.md:701–706), row 8 (spec.md:732–734), D9 (spec.md:149–155), Scope table (spec.md:28)

**Claim:** "**A post-cap round is spent only if it rendered.** `revised-after-cap (+1 round)` is the exit only when the granted post-cap round actually rendered at least one item. A post-cap resume that renders zero items exits `empty-frontier` instead, and the round is **not** consumed…"

**Why this is wrong:** This is a direct amendment of the resume contract at `skills/grilling/SKILL.md:23`, which today reads: "**If `rounds_used ≥ round_cap`, this invocation runs exactly one additional round and exits `revised-after-cap (+1 round)`; a further `prior_summary` arriving with `rounds_used > round_cap` exits `round-cap` at once.**"

Three consequences, each verified:

1. **Not in Scope.** The Scope table's `grilling` cell covers `:14–23` only for "optional per-seed-item `id`, its legality rule, and the all-or-none rule." The resume-contract exit rule is not listed as changing anywhere.
2. **Checklist rows 5 and 8 are mutually unsatisfiable.** Row 5 requires that "still present **verbatim**: … the resume contract including the single post-cap round and `revised-after-cap (+1 round)`." Row 8 requires "a post-cap round that renders zero items is **not** consumed." If `:23` is edited, row 5 fails; if not, the shipped file states the unconditional rule at `:23` and the conditional rule in § Termination — the exact contract ambiguity this ticket exists to close. Same failure class as round-1 conventions F-1, which was a P0.
3. **D9's load-bearing rationale is falsified.** spec.md:150–155 asserts "everything row 4 asserts — … **the resume contract** — survives v2 unchanged, so row 4 stays true." `docs/specs/DONE/VHS-32/spec.md:458` asserts "`grilling` body contains, **verbatim**: … the 1.1 resume contract including the single post-cap round and the `revised-after-cap (+1 round)` exit." Under Design 4 that no longer holds verbatim, so the "extends, not supersedes" argument loses one of its nine legs.

Two smaller consequences ride along: `grilling:57` mandates that a post-cap round render `rounds: <round_cap>+1/<round_cap>` in the header, and Design 4 does not say what the header reads when the round is *not* consumed; and Design 4 names no `reason:` value for the post-cap `empty-frontier` exit.

**Suggested fix:** Add `:23` to the Scope table cell; state the amended sentence explicitly in Design 4 with the zero-item header and reason; amend row 5 to carve out the exit-sentence condition; amend D9 to acknowledge the one departure from row 4's verbatim list.

---

### F-2: Design 2 amends `grilling/SKILL.md:108` but not its verbatim duplicate at `:151`, so the shipped file contradicts itself on the stop case

**Severity:** P1
**Where:** spec § Design 2 (spec.md:296–302) and Scope table (spec.md:28) vs `skills/grilling/SKILL.md:151` and `:148`

**Why this is wrong:** `:108` is not the only place that sentence lives. `skills/grilling/SKILL.md:151` is the § Failure modes bullet: "- **`stop` with explorations in flight** — abandon them; their questions are Open with `unresolved because: stopped`." After the change, `:108` would say the blocked question renders `blocked-on: F<n>` while `:151` still says `stopped`. The Scope table's `## Failure modes` cell says only "the new prohibitions and shapes"; checklist row 4 asserts "the amended `:108` behaviour" without mentioning `:151`. Nothing catches the divergence.

Secondary: `:148` ("**Failed dispatch** … the question becomes an `ℹ️` fact request in the next round") restates `grilling:76`'s retry, which Design 3 rule 1 displaces for verification dispatches. `:148` stays true for ordinary fact needs but reads as unconditional.

**Suggested fix:** Name `:151` and `:148` in Design 2 and in the Scope table's `## Failure modes` cell; extend row 4 to assert `:151` carries the same split; decide and state whether `:148` gains a verification carve-out.

---

### F-3: The reason-precedence chain still does not place `fact not established`, and ranks two values illegal for an F-item (round-2 correctness F-5, PARTIAL)

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 (spec.md:266–294) and § Design 3 rule 3 (spec.md:373–377)

**Why this is wrong:** Round 2 fixed the *structural* half — the precedence is now its own bolded block rather than under "The Q-item reason set narrows" — but the substantive half is still open:

- `fact not established` — the F-item's base value, and the only one the qualifiers attach to — **appears nowhere in the chain**.
- `round-cap` **is** in the chain but is not a legal F-item value. An unresolved F-item at a round-cap exit has two readings.
- `deferred` and `blocked-on` are likewise not legal F-item values, so three of the chain's four terms are Q-only.
- The round-2 consequence persists: on a `stop`, an F-item rendering `stopped` carries no qualifier, so Design 7's Phase 4 carry rule finds none and the brief loses "a human already asserted an answer".

**Suggested fix:** State the F-item ranking in F-item terms in Design 2's F-item paragraph; then either allow the qualifier on `stopped` or record the loss as accepted. Assert whichever in row 7.

---

### F-4: Checklist row 12 calls the `/spec-brief` template "eight-section"; it declares nine headers

**Severity:** P4
**Where:** spec § Test plan row 12 (spec.md:768)
**Why this is wrong:** `skills/spec-brief/SKILL.md:119–127` declares nine `##` headers: Problem, Why it matters, Scope, Decisions carried forward, Done when, Out of scope, Scale, Risks / decisions, References. Eight is right only if `## Scale` is excluded as conditional, which the row does not say.
**Suggested fix:** "The nine-header brief template (`:113–128` pre-edit, one of them the conditional `## Scale`)…" — or drop the count.

## Verified clean this round

All 30-odd path:line anchors in § Scope and § References resolve at `7403cb5`; `python lint.py --strict` → exit 0, 2 `missing-requires` WARNs as row 1 claims; `grep -c 'total_p0p1 == 0'` = 2 (row 11); `grep -c 'options 1–3'` = 4 (row 10); `grep -c 'model:'` = 0 on all three files (row 3); row 2's grep passes on all five hit sites; `spec-cycle:640` and `:700–703` match their descriptions; the wiki decision does name VHS-33 as its revisit trigger; the Plane ticket has no "Done when" section, so the brief's synthesized criteria stand and the spec maps them 1:1. `git log` shows the entire touched surface last moved in `d381f88` — already recorded as Risks 4.

## Summary
P0: 1 | P1: 1 | P2: 1 | P3: 0 | P4: 1

STATUS: RED P0=1 P1=1 P2=1 P3=0 P4=1
