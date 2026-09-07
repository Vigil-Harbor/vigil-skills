# VHS-33 — grilling hand-off contract v2: caller IDs, fact-item shapes, fence-empty token

**Brief:** `docs/specs/TODO/VHS-33.brief.md`
**Ticket:** VHS-33 (`9509a53b-894e-4b5c-82d2-e9cb52ff191d`, Backlog)
**Anchors verified against:** vigil-skills `7403cb5`, 2026-09-06.

## Goal

Change the `grilling` primitive's output contract — its hand-off block and its
termination tokens — once, and update every caller that parses it in the same PR.
Four changes land together: caller-supplied finding ids survive the interview as a
`ref:` field, unresolved fact requests get their own item shape in the open
frontier, a sixth exit token `fence-empty` separates the round-1 altitude-fence case
from an emptied frontier, and every rendered round is written in plain language with
its internal identifiers glossed. Two of the four were raised by CodeRabbit on the
VHS-32 PR and deliberately deferred because the block was pinned verbatim through
four review rounds; one was deferred by the VHS-32 spec itself; the fourth was
raised by the operator during the VHS-33 brief interview. Nothing executable
changes — this is a prose-contract change to four `SKILL.md` files and one reference
doc.

## Scope

### Files to change

| Path | Change |
|---|---|
| `skills/grilling/SKILL.md` | Invocation contract (`:14–23`): optional per-seed-item `id`, its legality rule, and the all-or-none rule. Per-round output contract (`:33–57`): the plain-language rendering rule and the round-preamble slot. Fact-finding (`:68–78`): operator answers are claims to verify; `:74` gains a pointer to the new `F<n>` Open form; `:76`'s retry (including its host-timeout clause) is displaced for verification dispatches only. Bounds (`:88`): same `F<n>` pointer. Termination (`:102–112`): sixth exit `fence-empty` in the `:104` exit list and its boundary with `empty-frontier`; `:108` is amended so a `stop` with an exploration in flight renders the F-item `stopped` and the question it blocked `blocked-on: F<n>`. The resume contract (`:23`) and the post-cap header rule (`:57`) are **unchanged**. Hand-off block (`:114–134`): `ref:` field on all four item shapes, `F<n>` Open items, the two reason-precedence orders, `_(none)_` empty-section rule, the `partially identified seed` reason value, and the restated Open-frontier bound at `:132`. `## What this skill never does` (`:136–138`): the `source: operator` prohibition. `## Failure modes` (`:146–151`): amendments to three existing bullets — `:151` in parallel with `:108`, `:148` gaining the verification carve-out, `:149` gaining D5's operator-claim branch. |
| `skills/spec-cycle/SKILL.md` | 2f-i step 1 (`:491–509`): pass lens-qualified finding ids as seed `id`s. 2f-i step 3 (`:518–537`): a `fence-empty` summary is persisted like any other. 2f-i step 4 (`:539–546`) and step 5 (`:548–554`): drive the id-sets from `ref:` instead of title-matching; the `not reached` clause; the multi-id, zero-id, precedence, unknown-id and missing-`ref:` rules; empty-set rendering. `## Failure modes` (`:698–708`): one bullet for the fence-empty halt outcome. |
| `skills/spec-brief/SKILL.md` | Phase 2 (`:84–90`): `fence-empty` is not a halt. Phase 3 (`:92–107`): on a `fence-empty` summary, the warning prints before the confirm block and options 1 and 3 only are offered. Phase 4 mapping rules (`:134–143`): the `F<n>` Open-item mapping, the verified/refuted operator-claim mapping, and the all-sections-empty rule for a `fence-empty` summary, which supersedes `:139` on that path only. |
| `skills/grill-me/SKILL.md` | `## Failure modes` (`:18–21`): two bullets — name `fence-empty` and say what comes back with it; record that a topic whose facts are not repo-checkable returns every fact request Open. |
| `docs/spec-workflow-reference.md` | `/spec-brief`'s termination-shapes paragraph (`:23`) — the sixth exit and where it lands. The grilling-contract paraphrase (`:35`) — `ref:` ids, the open frontier's three item shapes, and facts sourced from the exploration that found them. The bounds sentence (`:33`) is left alone. |

### Files to create

None.

### Files to leave alone

- Everything under `docs/specs/DONE/` — history, never edited (D9).
- `skills/ship-spec/`, `skills/spec-close/`, `skills/review-pr/`, every file under `agents/`.
- `lint.py`, `sync.py`, `tests/` — nothing mechanical asserts the hand-off block's
  shape today (brief F1), and this spec does not add such a mechanism.
- `README.md`, `AGENTS.md` — verified to carry no paraphrase of the hand-off block
  or the exit tokens, so a within-primitive contract revision does not reach them.
- `skills/spec-cycle/SKILL.md` outside `### 2f-i` and one `## Failure modes` bullet —
  in particular § 2b, whose pre-existing `Agent(...)` dispatch block is not this
  ticket's business.

## Decisions

D1–D12 are carried from the brief's `## Decisions carried forward`, in its
numbering. D13 records the brief's `## Scale` non-factor, as `/spec-cycle` Phase 1
requires.

**Spec-level additions**, each authorized by neither brief nor ticket, rationalized
at its point of use, and listed here so the Phase 3 drift-check sees them:

- `blocked-on: F<n>` as new Q-item reason vocabulary, and the removal of
  `fact not established` from the Q-item set (Design 2) — brief decision 3
  authorizes an *added* F-shape, not a removal from the Q set.
- Two stated reason-precedence orders, causal-before-exit, one per item shape, which
  amend `skills/grilling/SKILL.md:108` and its duplicate at `:151` (Design 2).
- Amendments to two further `## Failure modes` bullets, `:148` and `:149`, so they
  do not restate rules Design 3 and D5 carve out (Design 2).
- The restated Open-frontier bound at `:132`, which D3's named overflow F-items
  change (D13).
- `_(none)_` as the empty-*section* rendering, on every exit (Design 2).
- The legal-id lexical rule, and the all-or-none rule making a partially identified
  seed an illegal invocation (Design 1) — the brief leaves both legal — and the
  `partially identified seed` reason value that reports it (Design 1).
- The three rules on when a verification runs, including the last-rendered-round
  rule and the batch-ordering rule for verifications versus new fact needs, and the
  refuted / partially-confirmed qualifier split (Design 3).
- The resume behaviour of Open F-items — every one carries over un-re-dispatched,
  qualifier or not, and a decision downstream of one is rendered rather than waiting
  (Design 3 rule 1). `:23` itself is unchanged; the rule is stated in § Fact-finding.
- The `fence-empty`-token-versus-sections guard on both consumers (Designs 6 and 7).
- `_(none)_` stated as a sentinel callers never transcribe, and the F-chain's
  terminal-disposition antecedent (Design 2).
- The round-preamble rendering slot (Design 5), and the ≈3-sentence question-body
  bound where the brief says only "short" (Design 5).
- The boundary sentence fixing which fence-blocked rounds exit `fence-empty` and
  which exit `empty-frontier`, and the fresh-invocation-only rule (Design 4).
- Lens-qualified seed ids `<lens>/<finding-id>` (Design 6).
- The three-way precedence rule (`left open` → `deferred to option 3` →
  `dispositioned`), seed-order dedup, the `not reached` and
  `also settled (left open)` clauses, `unknown ref ignored: <id>`,
  `item missing ref: <item title>`, and the broadened definition of
  `unreferenced decisions applied: <n>` (Design 6).
- The purpose-written `fence-empty` step-5 line, and the `not grillable` clause's
  survival into it (Design 6) — brief decision 8 authorizes only that 2f-i "writes
  one short block to `grill.md`".
- The Phase 3 narrowing — including rendering the preview as what Phase 4 writes —
  and the all-sections-empty rule for a `fence-empty` brief, which supersedes
  `skills/spec-brief/SKILL.md:139` on that path (Design 7).
- `/grill-me`'s second failure-mode bullet recording the non-repo-checkable
  degradation, and Risks 5 (Design 8) — the brief's `grill-me` Scope row authorizes
  only naming `fence-empty`.
- **D9 says *extends* where brief decision 9 says *supersedes*.** Brief `:44` reads
  "notes that it supersedes VHS-32 checklist row 4"; every assertion that row makes
  survives v2 unchanged, so superseding it would retire eight still-true assertions.
  D9 extends it and adds checklist row 5 to keep them under test.

### D1 — Caller IDs survive the hand-off (brief 1, Q1)

An optional caller-supplied `id` per seed item is echoed verbatim as a `ref:` field
on every Settled and Open item that descends from it, including the rolled-up
deferred item. Determinism replaces title-matching. Honored by Design 1.

### D2 — `ref:` holds zero or more IDs (brief 2, Q9)

One decision may disposition several findings; a fact-driven decision may
disposition none. Determinism comes from the ids being present, not from there
being exactly one. Honored by Design 1 (rendering) and Design 6 (consumption).

### D3 — Fact items get their own shape (brief 3, Q2)

Explicit `F<n>` forms in `### Open frontier`, alongside the existing `F<n>` in
`### Facts established`, so a caller can tell "needs a fact" from "needs a
decision". Honored by Design 2.

### D4 — An operator-supplied fact is a claim to verify, not a fact (brief 4, Q3)

The primitive checks the claim with a read-only exploration. A confirmed claim is
established with the *found* `path:line` as its source; an unconfirmed one stays
open. The operator never hunts for paths. Honored by Design 3.

### D5 — Unverifiable operator claims stay open (brief 5, Q8)

Where the host offers no read-restricted agent class, the claim is open as
`fact not established (operator claim, unverified)`. `source: operator` is never a
legal established source. Honored by Design 3 and by the new prohibition in
`## What this skill never does`.

### D6 — `fence-empty` is a distinct exit token (brief 6, Q4)

A sixth exit, reached when round 1 renders zero items because no candidate met the
altitude fence. It goes through the hand-off block with empty sections, and the
reason line stays for humans. Honored by Design 4.

The VHS-32 wiki decision rejected *"a success token for an empty interview"* on the
grounds that it would write a hollow brief every downstream lens then treats as
authority. `fence-empty` narrows that rejection rather than reversing it: the seed
had a root and the ticket text is real, so there is something to write a brief from;
what the rejection guards against is `empty-seed`, which stays a halt. Design 7's
single `## Risks / decisions` item and its distinct warning are what keep the
resulting brief honest rather than hollow.

### D7 — A fence-empty grill still consumes the once-per-halt bound (brief 7, Q5)

The VHS-32 S8 rule stays flat: the seed cannot change between two grills in one
halt, so a re-offer would re-run the same inputs. The 2f-i menu re-renders with
options 1–3. The re-offer half of the deferred finding is **not** adopted. Honored
by Design 6, which changes nothing about the once-per-invocation bound.

### D8 — A fence-empty grill is persisted (brief 8, Q10)

2f-i writes one short block to `grill.md` recording that the grill ran and nothing
was askable; it is the only record of a consumed grill. Honored by Design 6 — and
by *not* adding a new branch: a fence-empty summary is a summary, so the existing
append path already carries it.

### D9 — The archived VHS-32 spec is not edited (brief 9, Q6)

`docs/specs/DONE/VHS-32/` is history. This spec carries its own checklist row
asserting the v2 block. That row **extends** VHS-32 checklist row 4
(`docs/specs/DONE/VHS-32/spec.md:458`) rather than superseding it: everything row 4
asserts — the guard sentence, the D2 no-mutations sentence, the fork block, the
advisory sentence, the three bounds, the S4 table, the three section headers, the
`empty-seed` exit, the resume contract — survives v2 unchanged, so row 4 stays true
and this spec adds a row (row 5) that keeps those invariants under test.

The wiki decision `decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md`
names this ticket as its revisit trigger; updating it is `/spec-close`'s
decomposition step, not this spec's.

### D10 — `/spec-brief` and the workflow reference are in scope (brief 10, Q7)

The contract's consumers change with the contract, in one PR. Honored by Designs 7
and 8.

### D11 — A plain-language rendering rule, for the primitive's rounds only (brief 11, Q11/Q13)

Every rendered round glosses each internal identifier on first use and keeps
question bodies short. The wider pass over the other lifecycle skills'
operator-facing blocks is VHS-34. Honored by Design 5 and by the Out-of-scope
fence.

### D12 — ASD-STE100 writing rules, not its dictionary (brief 12, Q14)

Short sentences, one instruction per sentence, one meaning per term, gloss every
identifier on first use. The dictionary is a reference, not a gate. Honored by
Design 5.

### D13 — Scale is an explicit non-factor

The brief declares `## Scale` → `**Factor:** no`. Recorded here so `/spec-cycle`'s
drift-check has a spec anchor and a later invocation pins to it. The scalability
lens does not run, and the design adds no scale machinery: the primitive's bounds
(round cap 3, question cap 7) already bound every rendered surface, and the open
frontier stays bounded by construction.

The bound itself is restated, because D3 changes its derivation. `:132` today reads
`(round_cap + 1) × question_cap` named items plus one rolled-up item per deferred
subtree, derived from `:63`'s "only questions actually rendered to the operator ever
become named Open items". D3 gives a *named* shape to overflow fact needs that
`:74` says reach the hand-off without ever being rendered, so the bound becomes
`(round_cap + 1) × question_cap` named items, **plus at most `question_cap`
un-rendered fact requests**, plus one rolled-up item per deferred subtree. Still
bounded, still small, and scale remains a non-factor — but the derivation must match
the shapes that now exist. `:132` is listed in the Scope table.

## Design

### 1. `ref:` — caller ids through the hand-off

**Input.** `## Invocation contract (inputs)` gains: a caller that supplies its seed
as a list of items may give each item an opaque `id`, which the primitive echoes
back through the hand-off. The primitive never parses an id, never normalizes it,
and never invents one.

Two rules make "opaque" safe, because the rendering imposes a delimiter whether or
not the contract admits it:

- **Legal id.** A non-empty string with no comma, no semicolon, no newline, and no
  leading or trailing whitespace, unique within the seed. Comma is `ref:`'s own
  delimiter; semicolon is the clause delimiter of 2f-i's step-5 line (Design 6), and
  an id containing one makes that line's clause boundaries unreadable one renderer
  down. The primitive does not validate ids; a caller that breaks this gets an
  unusable hand-off.
- **All or none.** A caller that supplies any `id` supplies one for every seed item.
  A partially identified seed is not a legal invocation. Two consequences, both
  stated so the rule prescribes and not merely diagnoses:
  - **Rendering:** the primitive renders **no `ref:` field at all** for the whole
    interview — the absent state — so no caller can mistake a dropped id for
    `ref: none`.
  - **Reporting:** in the round-1 preamble (a slot Design 5 defines) where a round is
    rendered, **and on the hand-off header's `reason:` field** as
    `partially identified seed — ref: omitted` on every exit that renders the block.
    Not on a line above the header: `skills/grilling/SKILL.md:116` says the block is
    rendered *exactly*, and 2f-i appends "the returned Grill summary verbatim"
    starting at the `## Grill summary` header (`spec-cycle:523`), so a line above it
    never reaches `grill.md` — the one artifact `/spec-close` archives as the record
    of why the spec moved, and 2f-i is the only caller that supplies ids at all. On
    `empty-seed` there is no block and no round, so the one-line reason carries it.

**Inheritance.** An item's `ref:` lists the ids of the seed items its decision bears
on. A decision inherits the ids of the tree node above it; a decision specific to
fewer seed items carries only those. The rolled-up deferred item — the case with no
`Q` number at all, which D1 names explicitly — carries the ids its parent carried,
with no narrowing.

An earlier draft narrowed it to "only the ids no rendered decision reached", to stop
a deferred subtree near the root from sweeping most of the seed into `left open`
under 2f-i's precedence rule. That narrowing is dropped: Design 6's
`also settled (left open)` clause now makes every precedence demotion visible, so the
sweep is no longer silent, and the narrowing would buy nothing while defeating
Design 6's own conservative-reporting principle — a finding that a whole unexplored
subtree still bears on is exactly the finding that should read `left open`.

**Rendering — the absent/none rule.** Two states, decided by what the caller
supplied for the seed as a whole:

- The caller supplied **no** ids (`/grill-me`, `/spec-brief`): the `ref:` field is
  **absent** from every item.
- The caller supplied ids: **every** Settled and Open item carries a `ref:` — all
  three Open shapes included. An item bearing on no seed item renders `ref: none`
  (D2); one bearing on several renders them comma-separated in seed order:
  `ref: correctness/F-2, edge-cases/F-1`.

The reason for the absent state is legibility, not compatibility: nothing mechanical
parses this block (brief F1), but `/spec-brief` transcribes Settled items into the
brief, and a universal `ref: none` would be noise in the artifact every downstream
lens treats as authority.

**Placement.** `ref:` is the last field on the item line, full stop — not predicated
on any other field's presence, since two of the three Open shapes lack the field the
first draft anchored it to.

### 2. The v2 hand-off block

This is the authoritative rendering. Everything the other designs change appears
here in one place:

```
## Grill summary — <seed title> (rounds: <n>/<round_cap>, exit: empty-frontier | fence-empty | round-cap | stop | revised-after-cap (+1 round); reason: <tree fully visited | no candidate decision met the altitude fence | cap reached | operator stop | resume>[; partially identified seed — ref: omitted])

### Settled
1. **<decision title>** (Q<n>) — chose <A/B/free-form answer>: <one line>. Facts relied on: <F-ids or "none">. ref: <id>[, <id>…] | none

### Open frontier
1. **<question title>** (Q<n>) — branches: <A/B>; recommendation: <X>; unresolved because: <stopped | round-cap | deferred | blocked-on: Q<m> | blocked-on: F<n>>. ref: <…>
2. **F<n> — <fact needed>** — unresolved because: <fact not established[ (operator claim, unverified | operator claim, refuted: <path:line>)] | stopped>. ref: <…>
3. **<parent title> — downstream decisions not explored (deferred at round <n>)** — unresolved because: deferred. ref: <…>

### Facts established
- F1 — <fact> (source: <path:line>)
```

**Item shape 2 is new** (D3). A fact was never a fork, so an F-item carries no
branches and no recommendation. Its reason value is `fact not established` or
`stopped`; the parenthetical is an **optional qualifier on the first value**, never a
third value — a caller matching the prefix `fact not established` matches every
qualified form.

**The Q-item reason set narrows.** `fact not established` leaves the question form —
it was the accommodation the brief's problem 2 names. A question waiting on a fact
renders `blocked-on: F<n>`, alongside the existing `blocked-on: Q<m>`.

**Reason precedence — the causal reason outranks the exit reason.** Several reasons
can apply to one item at once, so they are ranked, highest first. The two item shapes
draw from different value sets, so the ranking is stated for each:

```
Q-item:  deferred → blocked-on: <unresolved Q<m> or F<n>> → stopped → round-cap
F-item:  fact not established[ (<qualifier>)] → stopped
```

`deferred`, `blocked-on:` and `round-cap` are **Q-item values and never render on an
F-item**: a fact request cannot be deferred and waits on nothing. So an unresolved
F-item at a `round-cap` exit renders `fact not established`, not `round-cap`. A
`revised-after-cap (+1 round)` exit ranks as `round-cap` for a Q-item; it needs no
F-item entry.

**The F-chain's first entry has an antecedent**, without which it swallows the
second: `fact not established` applies only where the fact-finding machinery reached
a **terminal disposition** — twice unanswered (`:88`), dispatch-cap overflow (`:74`),
failed dispatch (`:76`), no read-restricted agent class (`:72`), or a verified /
refuted / unverified operator claim (Design 3). An exploration abandoned mid-flight
with none of those renders `stopped`. Stated as a rank alone, "the fact was not
established" is literally true of the abandoned case too, and `stopped` would be
unreachable.

**The rolled-up deferred item is a fixed case, not a ranking.** Its reason is always
`deferred`, on every exit — the block's third Open shape hard-codes it, and this
ticket is what gives that shape an `unresolved because:` field for the first time.

**`_(none)_` is a sentinel, not an item.** A caller reading the block treats a
section rendering `_(none)_` as containing zero items, and never transcribes the
sentinel into its own artifact. Without this, `/spec-brief` `:140` would write
`_(none)_ — spec author pins this` into `## Risks / decisions`, `:142` would write a
`## References` bullet with no `path:line`, and 2f-i step 5 would report
`item missing ref: _(none)_` — a contract violation flagged on a legitimately empty
section.

The F-item ranking follows the same principle as the Q-item one, applied honestly:
`stopped` is what the header already says, and
`fact not established (operator claim, unverified)` is what the item was waiting on.
Ranking the exit reason first would erase the operator-claim qualifier at exactly the
exit where a brief author most needs it — the qualifier attaches only to
`fact not established`, so a bare `stopped` is indistinguishable from a fact request
nobody ever answered.

The principle: the header already records *how the interview ended*, so an item that
repeats it says nothing new. What the caller cannot recover from the header is *what
this particular item was waiting on* — which is the whole point of D3's
question-versus-fact distinction. So `deferred` (an explicit operator act) wins, then
the specific blocker, and the two exit reasons rank last.

`blocked-on:` applies **only while its named blocker is itself unresolved**. A
question blocked on F1 where F1 later reached `### Facts established`, and which then
hit the round cap, renders `round-cap` — nothing blocks it any more. A question still
blocked on an unresolved F1 when the operator stops renders `blocked-on: F1`, not
`stopped`.

This changes `skills/grilling/SKILL.md:108`, which today says that on `stop` the
questions of in-flight explorations are Open with `unresolved because: stopped`.
Under the ranking, on a `stop` with an exploration in flight both items are Open and
they carry *different* reasons: the F-item renders `stopped` — **unless it carries an
`(operator claim, …)` qualifier, in which case the F-chain's first entry applies and
it renders `fact not established (operator claim, unverified)`**, because a
verification dispatch abandoned at a `stop` is also an exploration in flight, and
collapsing it to `stopped` would erase the qualifier `/spec-brief` Phase 4 carries.
The question the F-item blocked renders `blocked-on: F<n>` (the missing fact is what
that question is waiting on).

**The same rule is stated twice in the file, and both statements are amended in the
same hunk.** `:151`, the `## Failure modes` bullet, reads today: "**`stop` with
explorations in flight** — abandon them; their questions are Open with
`unresolved because: stopped`." Amending `:108` alone would ship a file that answers
the stop case two ways — the contract ambiguity this ticket exists to remove,
relocated into the artifact. Both are listed in the Scope table, and checklist row 4
asserts both.

The neighbouring bullet `:148` is in the same position for Design 3: it states
`:76`'s retry ("the question becomes an `ℹ️` fact request in the next round") without
the verification carve-out rule 1 adds. It gains one — "except a verification
dispatch, which is not retried (§ Fact-finding)". `:149`, which says every fact need
becomes a fact request where no read-restricted agent class exists, gains D5's
operator-claim branch. This is the pattern Design 2's Cross-references paragraph
already applies to `:74` and `:88`: a rule restated elsewhere in the file moves with
the rule.

**Empty sections.** A section with no items renders `_(none)_` on the line under its
header — on *every* exit, not only `fence-empty`. The commonest exit in this repo's
own history is `empty-frontier`, whose Open frontier is empty by definition, and
leaving that rendering unstated invites two implementers to pick two shapes. Note
the two sentinels are deliberately different shapes for different scopes:
`_(none)_` empties a *section*, bare `none` empties a *field* (`ref: none`,
`Facts relied on: none`).

**Cross-references.** Two sentences outside the block still describe an unresolved
fact in the old vocabulary and gain a pointer to the F-item form: § Fact-finding
`:74` ("they reach the hand-off as Open with `unresolved because: fact not
established`") and § Bounds `:88` ("A fact request the operator leaves unanswered
twice becomes an Open item"). The bounds themselves do not change — only the
cross-reference does, which the Out-of-scope fence on "the three bounds" permits.

### 3. Operator answers are claims, not facts

`## Fact-finding` gains a subsection. When the operator answers a fact request
(`F1 <answer>`), the answer is a **claim**. The primitive dispatches the same
read-restricted exploration it would have dispatched anyway, instructed to confirm
or refute that specific claim and to answer with `path:line` evidence.

- **Confirmed** → `### Facts established`, sourced by the `path:line` the
  *exploration* found. The operator's wording may be kept as the fact text; the
  source is never the operator (D5).
- **Refuted** — the exploration returned contrary evidence →
  `fact not established (operator claim, refuted: <path:line>)`. The evidence
  travels with the item. A refuted claim and an unchecked one are causally
  different, and collapsing them would hand the spec author "a human asserted this"
  while withholding "and it was checked and is wrong" — the precise failure D4's
  rationale exists to prevent.
- **Not confirmed** — `not found`, an empty return, a dispatch error, or **no
  read-restricted agent class in this host** (D5, never dispatched to anything
  write-capable) → `fact not established (operator claim, unverified)`.
- **Partially confirmed** — the exploration finds the file but at a different line,
  finds the function but with different behavior, or confirms half a two-part claim
  → **not confirmed**. Anything short of a full confirmation with a `path:line` that
  supports the whole claim is unverified. Where the exploration established a
  *different* fact, record that fact on its own terms, with its own `path:line`
  source, and leave the operator's claim Open. **The two never share a number:** the
  newly established fact takes the next unused `F<n>` in the monotonic series
  (`:48`), and the operator's claim keeps its original number as an Open F-item.
  Reusing the number would make one `F<n>` resolve to both an established fact in
  `## References` and an unestablished one in `## Risks / decisions` of the same
  brief.

Three rules on when verification runs, each stated in the skill so a reader does not
infer them:

1. **Dispatched once within one invocation; the operator is never re-asked.** A verification dispatch that
   errors, returns empty, times out, or returns without confirming is a failed
   dispatch **and is not retried** — the claim renders
   `fact not established (operator claim, unverified)`. This displaces, for
   verification dispatches only, both halves of `:76`'s retry rule: the carry-to-the-
   next-round-as-a-fact-request itself, *and* its "where the host reports a timeout,
   treat it identically" clause, which is only a classification whose consequence is
   that same retry. Re-asking is right when nobody has answered and wrong here,
   because the operator already answered.

   **`:76`'s never-returns rule is unchanged.** A dispatch that never returns blocks
   the round it belongs to; no prompt-level construct can cancel it, and the dispatch
   cap bounds how many can hang. This matters more under v2 than v1: v1 ended a fact
   need with no dispatch at all once the operator answered, so every operator answer
   now spawns a dispatch that v1 did not.

   **Across a resume, the rule is the resume contract's.** "Dispatched once" is an
   invocation-scoped rule. `:23` exempts *established* facts from re-dispatch and
   says nothing about Open F-items, so a resume would otherwise re-dispatch a
   verification and — for an item downstream of the revised decision — re-ask the
   operator for a fact they already answered. Neither is wanted: **every** Open
   F-item **carries over as Open and is not re-dispatched, qualifier or not** —
   exactly as `:23` already treats established facts. Scoping the rule to
   qualifier-carrying items alone would leave a plain `fact not established` item
   (twice unanswered, or cap overflow) re-dispatched on every resume by inference,
   in the ticket that first gives plain F-items a named Open shape.

   Where an Open F-item is downstream of the revised decision, the decision it gates
   **is rendered anyway, with the fact still open** — it does not wait. `:74`'s
   "questions downstream of a fact wait for it" governs a fact that is still coming;
   this one is not, so waiting would render nothing and, on a post-cap resume, spend
   the operator's single extra round on an empty round.
2. **It rides the normal batch and counts against the same cap.** Verification is
   dispatched in the round *after* the operator's answer, inside that round's single
   parallel batch, against the `question_cap` dispatch cap.

   Overflow needs its own rule: `:85`'s ordering ranks carried-over items, then tree
   depth, then blast radius — none of which ranks a verification, which is not an
   item, has no depth, and borrows its blast radius from a claim. So: **within a
   round's batch, new fact needs are dispatched before verifications, and
   verifications overflow first.** An unestablished fact blocks a question; a
   verification only annotates one. A verification that overflows past the last
   rendered round renders `fact not established (operator claim, unverified)`,
   exactly as rule 3 — so a claim answered in round 2 whose verification never fits
   has a stated outcome, not an accidental one.
3. **A claim answered in the last rendered round is not verified.** No extra round is
   rendered for verification alone. The claim reaches the hand-off as an Open F-item
   with `fact not established (operator claim, unverified)` — on **every** exit,
   `stop` included, per the F-item ranking in Design 2, which keeps the qualifier
   rather than collapsing it to a bare `stopped`. Under the defaults this is
   reachable in ordinary use — a fact request answered in round 3 of 3 — so it is a
   stated outcome, not an oversight.

`## What this skill never does` gains: *records an operator's claim as an
established fact, or writes `source: operator`.*

The round-end literal lines (`:52–55`) are **left unchanged**, including
`:53`'s "a fact request by number and the fact (e.g. `F1 <answer>`)". This is a
deliberate choice, not an omission: the input syntax is identical, and the
claim/verification distinction is the primitive's business, not a new step the
operator must perform.

### 4. `fence-empty` — the sixth exit

`## Termination` currently lists five exits, and `:106` routes the round-1
fence case to `empty-frontier` with a distinguishing reason line. After this change:

- `fence-empty` is the exit when **round 1 renders zero items** because no candidate
  decision met the altitude fence. Zero rounds are rendered; the header reads
  `rounds: 0/<round_cap>` and `reason: no candidate decision met the altitude fence`.
- `empty-frontier` stays reachable only after at least one round was rendered, and
  **keeps both reason lines** — `tree fully visited` and `no candidate decision met
  the altitude fence`. What changes is only that the round-1 fence case, which `:106`
  routes to `empty-frontier` today, now exits `fence-empty`. A *later* round whose
  remaining candidates all fall below the fence is still `empty-frontier` with the
  fence reason: candidates remain unasked, so "tree fully visited" would be false.
- **Fresh invocations only.** `fence-empty` is unreachable when `prior_summary` was
  supplied. A resume inherits a tree, so its "round 1" is not the interview's first
  round, and its carried-over Settled items and Facts must survive. A resume that
  renders zero items exits `empty-frontier` with `rounds: <rounds_used>/<round_cap>`,
  the fence reason, and the carried sections intact — `rounds_used` carried per the
  resume contract (`:23`). Without this rule, a fence-blocked resume would render
  `rounds: 0/<round_cap>` with three empty sections, and `/spec-brief` Phase 4 would
  write a brief that silently destroys every decision the operator had already
  settled.
- **The post-cap resume is unchanged.** A post-cap resume that renders zero items
  still exits `revised-after-cap (+1 round)` with `rounds: <round_cap>+1/<round_cap>`
  and its carried sections, exactly as `:23` and `:57` prescribe today. An earlier
  draft made that exit conditional on the round rendering at least one item, so the
  operator's single post-cap round would not be burned on a round that asked them
  nothing. That is a real improvement and it is **not taken here**: it amends the
  resume contract at `:23` — which checklist row 5 requires to survive verbatim and
  D9's extends-not-supersedes argument rests on — and it is inert without a matching
  change to `skills/spec-brief/SKILL.md:105`, which withdraws the resume option once
  a post-cap resume has *returned*, rendered or not. Two files outside this ticket's
  declared scope, to preserve a round no caller can currently spend. See § Deferred.

`fence-empty` goes through the hand-off block (D6), with all three sections rendering
`_(none)_` per Design 2's general rule. That is what separates it from `empty-seed`,
which returns a token and a one-line reason and renders no block at all; the skill's
existing "Every exit but `empty-seed` goes through the hand-off contract" sentence
covers the new token without amendment.

The header's exit enumeration gains `fence-empty`. The reason enumeration gains no
*exit*-derived value — `:106`'s existing "no candidate decision met the altitude
fence" is the one `fence-empty` uses. The one value the reason field does gain is
Design 1's `partially identified seed — ref: omitted` clause, which is orthogonal to
the exit and is specified in Design 2's block.

### 5. The plain-language rendering rule

`## Per-round output contract` gains a rule block governing the prose the primitive
renders: question titles and bodies, branch text, `For:` / `Against:` clauses,
recommendations, and fact requests.

- **Gloss every internal identifier on first use in each rendered round** — a section
  code (`2f-i`), an exit token (`empty-frontier`), a file-shape name — as
  `identifier (short gloss)`. Per *round*, not per interview: rounds reach the
  operator as separate messages, often minutes apart, and a gloss in round 1 is not
  on screen in round 3.
- **Short sentences; one instruction per sentence.**
- **One meaning per term:** the same thing keeps the same name for the whole
  interview.
- **Question bodies stay short** — at most about three sentences. Anything longer
  belongs in a branch's `For:` / `Against:`.

Two fences, both stated:

- The rule never rewrites a contract token. `ref:`, `Q<n>`, `F<n>`, the exit tokens,
  and the hand-off section headers are literal. When one appears in prose, gloss it
  in parentheses; do not paraphrase it away.
- It does not touch the round-end literal lines (`:52–55`) or the hand-off block's
  own shape.

The rule cites ASD-STE100's writing rules as its source and states that the
controlled dictionary is not adopted (D12) — its vocabulary is aerospace maintenance
and would reject words this repo needs.

**The round preamble.** `## Per-round output contract` today defines four rendered
constructs — the fork block, the plain form, the `ℹ️` fact-request form, and the two
round-end literal lines. It gains a fifth: an optional one-line **preamble** above
the round's first item, used only for contract violations the caller must see (today,
the partially identified seed of Design 1). It is defined here because Design 1
needs a rendering slot and the spec must not direct an implementer at a surface the
skill never defines.

**The preamble is not a rendered item.** It does not count against `question_cap` and
it never appears in the hand-off block. Bound 2 (`:85`) caps "rendered items per
round, questions and fact requests together"; a preamble that consumed one would let
a contract violation silently cost the operator a question — a change to a bound the
Out-of-scope fence protects.

### 6. `/spec-cycle` 2f-i — seed ids in, `ref:` out

**Step 1 (seed).** The finding id passed as the seed item's `id` is
**lens-qualified**: `<lens>/<finding-id>` (e.g. `correctness/F-2`), the shape 2b's
closure manifest already uses. This is load-bearing — two lenses routinely both
number a finding `F-1`, and a bare id would collide in exactly the case D1 exists to
make deterministic. 2f-i always identifies every seed item, satisfying Design 1's
all-or-none rule.

**Step 3 (persist).** One clarifying sentence: a `fence-empty` return carries a
`## Grill summary` block, so it passes the existing guard and is appended like any
other summary — its sections read `_(none)_`, and it is the only record that the
halt's one grill was consumed (D8). No new branch, no new file shape.

**Step 4 (apply).** Unchanged except for one guard. A Settled item is applied to the
spec if an in-place spec edit discharges it; one that cannot be (e.g. "narrow the
brief") is Settled-but-unapplied and reported as `deferred to option 3`.

The guard: **a Settled item carrying no `ref:` field, when 2f-i supplied ids, is not
applied.** Step 5 reports it as `item missing ref: <item title>`. This has to live in
step 4 because step 4 runs first — a withhold rule stated only among step 5's
reporting rules would be read after the edit it was meant to prevent. A missing field
is a contract violation, not a `ref: none`.

**Step 5 (re-render) — the brief's open risk, pinned.** The id-sets are built from
`ref:` fields, not titles. The full line:

```
grill applied: dispositioned <ids>; left open <ids>; also settled (left open) <ids>; not grillable <ids>; deferred to option 3 <ids>; not reached <ids>; unreferenced decisions applied: <n> — docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md
```

- **Every clause renders.** An empty id-set renders `none`; the
  `unreferenced decisions applied` count renders `0`. A variable-arity line is harder
  to read than a uniform one, and the first draft's asymmetry — four unconditional
  clauses plus one conditional — was an accident, not a design. Clauses are separated
  by `; `, ids within a clause by `, `; the legal-id rule (Design 1) bars both
  characters from an id so neither separator can be ambiguous.
- **Multi-id.** Every id in an applied Settled item's `ref:` enters `dispositioned`
  individually. Each set is deduplicated and ordered by seed order (lens order, then
  finding order within a lens), so the line is stable across runs.
- **Zero-id.** An item rendering `ref: none` dispositions no finding. It is still
  applied when it is a spec edit — a fact-driven decision can change the spec without
  closing a finding (D2).
- **`unreferenced decisions applied: <n>`** counts **every applied Settled item that
  dispositions no seeded id on this line** — whether it carried `ref: none`, carried
  only unknown ids, or carried only ids reported under another clause. Defining it as
  "items rendering `ref: none`" would leave three classes of applied-but-unattributed
  edit uncounted, and the field's name promises the reconciliation, not the sub-case.
- **`not reached`** (new): every seeded id that appears in no returned `ref:` at all.
  A seeded finding can go unreferenced for several reasons — it fell below the
  grill's altitude fence, `question_cap` truncation never rendered it, the interview
  stopped or capped before reaching it, or the primitive dropped its `ref:` (see
  `item missing ref:`). The clause does not distinguish them; it exists so that none
  of them disappears, which under a `ref:`-driven report is otherwise the same
  silent-mapping hole one layer down. Not-reached findings stay P0/P1. On a
  `fence-empty` exit this clause carries the entire seed.
- **Completeness.** Every seeded id appears in exactly one of `dispositioned`,
  `left open`, `deferred to option 3`, and `not reached` — disjoint and exhaustive
  over the seed. `not grillable` is reported alongside them but is disjoint from the
  seed entirely (those ids never enter it), and `also settled (left open)` is a
  re-listing of ids already in `left open`, not a fifth partition.
- **Precedence** when an id would land in several sets, highest first:
  `left open` → `deferred to option 3` → `dispositioned`. A finding referenced by
  both an Open item and an applied Settled item is reported **left open** — it is not
  fully discharged, and the conservative report is the honest one. `not grillable`
  is *not* in this chain: those ids never enter the seed, so they never appear in a
  `ref:`; step 1 populates that set and nothing else does.
- **`also settled (left open)`** carries every id precedence demoted to `left open`
  **whose Settled item was applied, or was Settled-but-unapplied (deferred to option
  3)**. Reporting is conservative; the interview's work is not undone, so without
  this clause the operator sees a still-red finding and no sign either that the spec
  moved on its behalf or that a decision exists whose discharge is menu option 3 —
  the invisible-work failure the ticket exists to close, one layer down. Ids whose
  Settled item was *applied* additionally take the existing
  ` — grilled (spec edited; not re-reviewed)` title suffix, which the current step 5
  applies only to dispositioned titles; demoted-but-deferred ids take no suffix,
  because no spec edit was made.
- **Unknown id.** Evaluated first, and it excludes ids already in `not grillable`
  (which are legitimately absent from the seed). Any other `ref:` id 2f-i did not
  seed is ignored for set-building and reported on its own line:
  `unknown ref ignored: <id>`.
- **Missing `ref:`.** An item carrying no `ref:` field when 2f-i supplied ids is a
  contract violation, not a `ref: none`. Report `item missing ref: <item title>`; the
  withhold itself is step 4's guard, stated there because step 4 runs first. Silently
  treating it as `ref: none` would edit the spec on a finding's behalf while
  reporting that finding nowhere.

On a `fence-empty` exit the line is replaced by a purpose-written one, because the
generic line reads as though something moved:

```
grill ran: nothing above the altitude fence — no finding dispositioned; not reached <all seeded ids>; not grillable <ids>; the halt's one grill is spent — docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md
```

This line is used **only when the summary's sections are genuinely empty**. A
`fence-empty` summary carrying Settled or Open items is a contract violation: step 4
runs before step 5 and has already applied those items, so printing "nothing above
the altitude fence — no finding dispositioned" would contradict the edits on disk.
Treat such a summary as `empty-frontier` — the generic seven-clause line, built from
the `ref:` fields as usual — and print
`fence-empty summary carried <n> items — treated as empty-frontier`. This is the same
guard Design 7 applies on the `/spec-brief` side.

The `not grillable` clause survives into this line deliberately. A `fence-empty` exit
requires a **non-empty** seed (step 1 refuses to invoke `grilling` when the seed is
empty after exclusions), so a run can have both a seed that reached the fence and a
non-empty not-grillable set — one lens report missing while the others carried
findings. `skills/spec-cycle/SKILL.md:700–703` states that the step-5 line is those
findings' *only* record, since they are never written to `grill.md`. Dropping the
clause on the one exit where nothing else moved would lose them entirely.

Everything 2f-i already never does — re-dispatch reviewers, increment the round
counter, change the gate formula, overwrite a prior `grill.md`, edit the brief, run
more than once per invocation — is unchanged. D7 is honored by omission: no re-offer
of option 4 is added.

**`## Failure modes`** gains one bullet: a `fence-empty` grill consumed the halt's
one grill, nothing was askable above the altitude fence, every seeded finding is
reported `not reached` and stays P0/P1, `total_p0p1` is unchanged, and **the menu
re-renders with 1–3**. The bullet uses the existing `## Failure modes` phrasing
("re-renders with 1–3", as at `:703` and `:708`) rather than "options 1–3", so the
count checklist row 10 pins does not move.

### 7. `/spec-brief` — mapping the new shapes

**Phase 2.** `fence-empty` is **not** a halt. The seed gate halts on `empty-seed`
because nothing was ever known; `fence-empty` means the seed had a root and nothing
above the fence, which is a documented outcome with a summary attached.

**Guard: the token and the sections must agree.** A `fence-empty` summary carrying
any Settled or Open item is a contract violation — Risks 2 records that this block is
model-rendered, so the mismatch is reachable. Every `fence-empty` rule below branches
on the token alone, and applying them to a summary that carried items would silently
destroy them. So: treat such a summary as `empty-frontier`, map its items by the
normal rules, and print
`fence-empty summary carried <n> items — treated as empty-frontier`. The same guard
binds 2f-i (Design 6), whose step 4 applies Settled items *before* step 5 chooses its
report line.

But it is not simply "handled like `empty-frontier`" either, because a `fence-empty`
summary has *all three* sections empty, and only the empty-**Settled** case has an
existing rule (`:139`).

**Phase 3.** The confirm block is reached, but three of its parts are wrong for this
summary. So on a `fence-empty` summary Phase 3:

- prints the warning **before** the confirm block — not after the write, where a
  Phase-4-only warning would land;
- renders options 1 and 3 only, the same narrowing `:105` already applies once a
  post-cap resume has returned, because option 2 ("Revise an answer — name the Q
  number") offers a revision against a summary with no Q numbers in it;
- renders the preview as **what Phase 4 will actually write** — `_(none)_` under
  `## Decisions carried forward` and the single `## Risks / decisions` item below,
  not the two empty lists `:94` would derive from an empty Open frontier. The confirm
  step's whole job is that the preview is the brief, and this is the one path where
  the brief carries a synthesized item the operator would otherwise never see before
  approving it.

**Phase 4** gains an all-sections-empty rule. A brief written from a `fence-empty`
summary carries:

- `_(none)_` under `## Decisions carried forward`. This **supersedes `:139` on this
  path — both its sentinel and its warning.** `:139`'s
  `_(none settled — see Risks / decisions)_` points the reader at a section that is
  itself near-empty here, and its warning ("the brief pins everything to the spec
  author") is false when nothing was pinned. `:139` is unchanged for every other
  exit.
- `_(none)_` under every section **the interview alone** feeds:
  `## Decisions carried forward` and `## Out of scope`. `## Out of scope` is fed only
  by mapping rule `:138` (a Settled decision framed as a fence), so a summary with
  zero Settled items leaves it empty too.
- **`## Scope` and `## References` are written as normal, not emptied.** `:141` feeds
  `## Scope` from "the settled decisions **and grounding facts**", and `:142` feeds
  `## References` from facts established — and Phase 1's grounding
  (`skills/spec-brief/SKILL.md:78–82`) runs *before* the interview and survives an
  altitude fence untouched. Emptying them would throw away every verified
  `path:line` the grounding pass obtained, on the one path where the interview
  settled nothing and the spec author needs that material most. A `fence-empty` brief
  therefore carries `## Scope` rows with a `Current` cell from each grounding fact
  and an empty `Change`, and `## References` bullets for those facts. Only if
  grounding itself found nothing do those two sections render `_(none)_` — by the
  general empty-section rule, not by this one.
- `## Problem`, `## Why it matters` and `## Done when` are transcribed from the
  ticket as normal — the fence blocked the interview, not the ticket.
- Exactly **one** item under `## Risks / decisions`:
  `Nothing met the altitude fence — the interview settled no decisions; spec author
  pins the entire design. spec author pins this`. The section is not left empty.
  A brief with every section empty is the hollow artifact the VHS-32 wiki decision
  rejected a success token for; one honest item naming what happened is what keeps
  this a documented outcome rather than that.
- The warning `warning: nothing met the altitude fence — the brief carries the ticket
  text and no interview outcome`, printed at Phase 3 as above.
- `Interview: 0 rounds, exit fence-empty` in the `## References` exit-token bullet.

**Phase 4 mapping rules** gain two bullets:

- An `F<n>` Open item → `## Risks / decisions`, worded as the fact that is missing,
  ending "spec author pins this". A `(operator claim, unverified)` qualifier is
  carried into the item text so the spec author knows a human already asserted an
  answer; a `(operator claim, refuted: <path:line>)` qualifier is carried **with its
  `path:line`**, so the author sees the evidence against the claim rather than a bare
  "unverified".
- A fact established from a verified operator claim → `## References` with the
  `path:line` the exploration found, like any other fact — it is a normal fact by
  then. What stays illegal: a `## Scope` row sourced from anything but an item in
  `### Facts established`. Stating it that way rather than as "a path with no
  `path:line` behind it" matters, because a *refuted* claim does carry a `path:line`
  — evidence **against** it — and that path must never populate a `Current` cell.
  The existing rule (`:141`) already routes an unsourced path to `## Risks /
  decisions`; an operator claim buys no exemption either way.

### 8. `/grill-me` and the workflow reference

**`skills/grill-me/SKILL.md`** gains two failure-mode bullets.

The first names `fence-empty`, deliberately *not* shaped like the `empty-seed`
bullet: on `fence-empty` a hand-off block does come back, with `_(none)_` sections,
and it is the deliverable. Report the reason — the topic had nothing above the
altitude fence — and stop. `/grill-me` writes nothing, as always.

The second records a degradation this ticket introduces for `/grill-me` specifically.
D4/D5 route every operator answer through a repo exploration, and `source: operator`
is never legal. `/grill-me`'s topics are "a plan, decision, or idea" — a fact request
whose answer is a policy, a meeting outcome, or an external constraint has no
`path:line` that could ever confirm it, so it will return `not found` and stay Open
as `fact not established (operator claim, unverified)` however the operator answers.
The bullet states this plainly so the operator sees a documented outcome instead of a
silent refusal to accept their answer. Widening `### Facts established` to admit a
non-repo source is **not** done here: brief decisions 4 and 5 are the operator's own,
and reversing them is a ticket, not a spec edit. Recorded as Risks 5.

**`docs/spec-workflow-reference.md`** — the paraphrase is updated, not expanded:

- `:23` (`/spec-brief`'s termination-shapes paragraph) currently reads "An emptied
  frontier means the tree was fully visited (or nothing met the altitude fence)". It
  gains the sixth exit and the boundary Design 4 fixes: an emptied frontier means at
  least one round was rendered and either the tree was fully visited or nothing left
  met the fence; a round-1 fence block is `fence-empty`, and neither writes a brief
  with interview outcomes.
- `:35` (the hand-off-block sentence) gains the caller-id `ref:` field, the open
  frontier's **three** item shapes — a question, an `F<n>` fact, and the rolled-up
  deferred subtree — and that facts carry the source the exploration found, including
  for a claim the operator supplied. Three, not two: the rolled-up deferred item is a
  distinct shape and this ticket makes it more so by giving it an
  `unresolved because: deferred` field. It is also the shape D1 exists for.
- `:33` (the bounds sentence) is left alone: no bound changes.

## Test plan

Doc/prompt-only change → review checklist, no dry-run transcript. The VHS-32
transcripts exercised the interview's *behavior*; this ticket changes the *shape* of
what it renders, and every assertion below is a grep or a diff against a file in the
worktree. No `docs/specs/TODO/ZZZ-*` artifacts are produced, so the VHS-32 cleanup
row has no counterpart here.

Rows 1 and 15 are runnable commands (`python lint.py --strict`, `python sync.py
status`); the rest are inspections. The checklist as a whole is the `/ship-spec`
gate, since `## Test command` is `N/A`.

**Review checklist:**

1. `python lint.py --strict` → exit 0; zero ERROR; `missing-requires` WARN count is
   2 (unchanged: `review-pr`, `ship-spec`).
2. `grep -nE '\b(Explore|Agent|Skill|general-purpose)\b' skills/grilling/SKILL.md skills/grill-me/SKILL.md skills/spec-brief/SKILL.md`
   → every hit is inside a parenthetical carrying "or the equivalent", or under a
   `## Tool-use notes` heading, or is the prohibition itself. For
   `skills/spec-cycle/SKILL.md`, evaluate **only the lines this change adds**
   (`git diff -U0`): no added line contains `Agent(` or a bare harness-tool call.
   Its pre-existing § 2b dispatch block is out of scope and unchanged (row 11).
3. `grep -c 'model:' skills/grilling/SKILL.md skills/grill-me/SKILL.md skills/spec-brief/SKILL.md` → 0 each.
4. **The v2 hand-off block.** `skills/grilling/SKILL.md` contains, verbatim: `ref:`
   as the last field on **all four** item shapes — the Settled line, the Open
   question line, the `**F<n> — <fact needed>**` line, and the rolled-up deferred
   line (which also gains `unresolved because: deferred`); the F-item reason set
   `fact not established | stopped` with the parenthetical shown as an optional
   qualifier on the first, never a third value; `blocked-on: F<n>` on the question
   form; **both** reason-precedence orders — the Q-item chain
   `deferred → blocked-on: … → stopped → round-cap` with the "only while its blocker
   is unresolved" rule and the `revised-after-cap`-ranks-as-`round-cap` note, and the
   F-item chain `fact not established[ (qualifier)] → stopped` with the statement
   that `deferred` / `blocked-on:` / `round-cap` never render on an F-item;
   `fence-empty` in the header's exit enumeration; `_(none)_` stated as the
   empty-section rendering **on every exit**. The amended `:108` behaviour is present
   **and so is the parallel amendment at `:151`** — `grep -n 'unresolved because: stopped'`
   returns no `## Failure modes` bullet asserting that a *blocked question* renders
   `stopped`; the `:108`/`:151` text carries the operator-claim exception. The
   F-chain's `fact not established` antecedent (terminal disposition: `:72` / `:74` /
   `:76` / `:88` / an operator claim) is stated, so `stopped` stays reachable. The
   rolled-up deferred item's reason is stated as always `deferred`. `_(none)_` is
   stated as a sentinel, not an item, that callers never transcribe. The header's
   reason field carries the `[; partially identified seed — ref: omitted]` clause
   with its append-never-replace rule. The Open-frontier bound at `:132` reads
   `(round_cap + 1) × question_cap` named items plus at most `question_cap`
   un-rendered fact requests plus one rolled-up item per deferred subtree. The three
   section headers `### Settled` / `### Open frontier` / `### Facts established` are
   unchanged.
5. **VHS-32 row 4's invariants survive** (this row *extends* that one; D9). In
   `skills/grilling/SKILL.md`, still present verbatim: the guard sentence (`:12`);
   "make no mutations of any kind"; the fork block; "It is never a default that
   carries by silence" (quoted as `:61` actually stands — two sentences; the
   run-together paraphrase an earlier draft asserted greps to nothing today); the
   three bounds with defaults 3 / 7 and brief altitude, and
   the shared fact-request cap; the fence table; the `empty-seed` exit; the resume
   contract including the single post-cap round and `revised-after-cap (+1 round)`.
   `## Tool-use notes` and `## Failure modes` are real `##` headings.
6. **`ref:` rules.** The skill states the absent-vs-`ref: none` two-state rule with
   its legibility rationale; the legal-id rule (non-empty, no comma, **no
   semicolon**, no newline, no surrounding whitespace, unique in seed); the
   all-or-none rule **with both its consequences** — no `ref:` field at all for the
   whole interview, and the report in two places: the round-1 preamble where a round
   is rendered, **and** the hand-off header's `reason:` field on every exit that
   renders the block (`empty-seed`, which renders no block, carries it on its
   one-line reason instead). The skill states that it is **not** rendered on a line
   above the `## Grill summary` header, and says why (`:116`, `spec-cycle:523`). The
   inheritance rule, under which the rolled-up deferred item carries the ids its
   parent carried with **no** narrowing; and the placement rule as "last field on the
   item line" with no dependence on another field. The header's `reason:` enumeration
   includes `partially identified seed — ref: omitted`.
   `grep -c 'ref: none' skills/grilling/SKILL.md` ≥ 1.
7. **Operator claims.** `skills/grilling/SKILL.md` contains the four dispositions
   (confirmed / refuted / not confirmed / partially confirmed → not confirmed), both
   qualifier forms `(operator claim, unverified)` and
   `(operator claim, refuted: <path:line>)`, the next-unused-`F<n>` rule for a
   different fact the exploration establishes, the no-read-restricted-agent branch,
   the "dispatched once, operator never re-asked" sentence **naming timeout among the
   failures that are not retried**, the surviving never-returns rule, the cap
   sentence, the last-rendered-round rule **stated as applying on every exit
   including `stop`**, the batch-ordering rule (new fact needs before verifications;
   verifications overflow first; an overflowed verification renders
   `fact not established (operator claim, unverified)`), and the resume clause
   ("within one invocation"; **every** Open F-item carries over un-re-dispatched,
   qualifier or not, and a decision downstream of one is rendered anyway rather than
   waiting). `:74` and `:88` each carry a pointer to the `F<n>` Open form. The two
   `## Failure modes` bullets that restate displaced rules are amended: `:148` gains
   the verification carve-out, `:149` gains the operator-claim branch.
   `## What this skill never does` contains `source: operator`. The round-end lines
   (`:52–55` pre-edit) are byte-identical (`git diff` shows no hunk on them).
8. **`fence-empty` boundary.** The skill states: round-1-only; `empty-frontier` keeps
   both reason lines and stays post-round-1; a later fence-blocked round is
   `empty-frontier`; `fence-empty` is unreachable on a resume (`prior_summary`
   present), which exits `empty-frontier` with `rounds: <rounds_used>/<round_cap>`
   and carried Settled and Facts intact. `skills/grilling/SKILL.md`'s § Termination
   exit list (`:104` pre-edit) names **six** exits including `fence-empty`. The
   resume contract (`:23`) and the post-cap header rule (`:57`) are byte-identical
   (`git diff` shows no hunk on either) — the post-cap-round question is deferred,
   see § Deferred. The `Every exit but `empty-seed`` sentence is unchanged.
9. **Plain-language rule.** `## Per-round output contract` contains the four rules
   (gloss on first use *per round*, short sentences, one instruction per sentence,
   one meaning per term), the ≈3-sentence body bound, the contract-token fence, the
   explicit "writing rules, not the controlled dictionary" sentence naming
   ASD-STE100, and the definition of the optional one-line round preamble **stated as
   not a rendered item — it does not count against `question_cap` and never appears
   in the hand-off block**.
10. **2f-i.** `skills/spec-cycle/SKILL.md` contains: `<lens>/<finding-id>` as the seed
    id shape; the fence-empty persist sentence; the **step-4 withhold guard** for an
    item missing `ref:`; the multi-id, completeness, three-way precedence, unknown-id
    and missing-`ref:` rules; the broadened
    `unreferenced decisions applied: <n>` definition; the **seven-clause** step-5
    line including `also settled (left open)` (covering both applied and
    deferred-to-option-3 demotions, with the title suffix only on the applied ones)
    and `not reached`; `none` / `0` as the
    empty renderings and `; ` / `, ` as the two separators; `unknown ref ignored:`;
    `item missing ref:`; the purpose-written fence-empty line **with its
    `not grillable` clause**, and the guard that it is used only when the sections
    are genuinely empty (`fence-empty summary carried <n> items — treated as
    empty-frontier`). The sentences `never re-dispatches reviewers`,
    `never increments the round counter`, `never overwrites`,
    `at most once per invocation`, `never edits the brief`, `not grillable`,
    `nothing grillable`, `deferred to option 3` all survive (`grep -c` each ≥ 1). No
    option 4 re-offer is added: `grep -c 'options 1–3' skills/spec-cycle/SKILL.md` is
    unchanged at 4 — the new failure-modes bullet uses the local "with 1–3" phrasing.
11. **Gate untouched.** `grep -c 'total_p0p1 == 0' skills/spec-cycle/SKILL.md`
    unchanged at 2; `git diff -U0 skills/spec-cycle/SKILL.md` shows hunks only inside
    the `### 2f-i` subsection and the one `## Failure modes` bullet — no hunk in
    2a–2e, 2b, 2g, Phase 0, Phase 1, or Phase 3.
12. **`/spec-brief`.** Phase 2 names `fence-empty` as a non-halt. Phase 3 states that
    on a `fence-empty` summary the warning prints **before** the confirm block, only
    options 1 and 3 are offered, and the preview renders what Phase 4 will write
    (`_(none)_` under Decisions plus the single Risks item), not the two empty lists
    `:94` would derive. Phase 4 carries the `F<n>` →
    `## Risks / decisions` bullet (including both qualifier forms, with the refuted
    one carrying its `path:line`), the verified-operator-claim → `## References`
    bullet worded as "sourced from anything but an item in `### Facts established`",
    and the all-sections-empty rule with all four of its parts: `_(none)_` under
    **every** section the interview would have populated — `## Decisions carried
    forward`, `## Scope` **and** `## Out of scope` — the explicit supersession of
    `:139`'s sentinel *and* warning on this path only, the single
    `## Risks / decisions` item, the rule that `## Scope` and `## References` are
    written from Phase 1 grounding facts rather than emptied, and the distinct warning
    text. Phase 2 carries the guard that a `fence-empty` summary carrying items is
    treated as `empty-frontier` with `fence-empty summary carried <n> items` printed.
    The nine-header brief
    template (`:113–128` pre-edit, one of them the conditional `## Scale`) is
    byte-identical.
13. **`/grill-me`.** `grep -c 'fence-empty' skills/grill-me/SKILL.md` ≥ 1, and the
    bullet states that a hand-off block with `_(none)_` sections comes back — distinct
    from the `empty-seed` bullet, which is unchanged. A second bullet records that a
    topic whose facts are not repo-checkable returns every fact request Open as
    `fact not established (operator claim, unverified)`.
14. **Workflow reference.** `docs/spec-workflow-reference.md` mentions `fence-empty`,
    `ref:`, and the open frontier's **three** item shapes (question, `F<n>` fact,
    rolled-up deferred subtree — matching row 4's four total item shapes); `:23`
    carries the corrected boundary; the bounds sentence (`:33` pre-edit) is
    byte-identical.
15. **Nothing else moved.** `git status --porcelain` lists only the five files in
    Scope plus this spec's own artifacts. No file under `docs/specs/DONE/`,
    `agents/`, `skills/ship-spec/`, `skills/spec-close/`, `skills/review-pr/`,
    `lint.py`, `sync.py`, or `tests/` is modified (D9 and the Out-of-scope fences).
    `python sync.py status` is clean after `python sync.py install`, and
    `python sync.py push` is a no-op — a byte-for-byte round trip.

## Test command

N/A

## Done when

Mapped 1:1 to the brief's `## Done when`.

1. The hand-off block in `skills/grilling/SKILL.md` carries an optional `ref:` field
   on every Settled and Open item including the rolled-up deferred item, defines
   `F<n>` Open forms, states the operator-claim verification rule, and lists
   `fence-empty` as an exit; the per-round output contract carries the plain-language
   rule. *(Designs 1–5; checklist 4–9.)*
2. `/spec-cycle` 2f-i passes finding ids as seed ids, reads `ref:` in its step 5
   line, and persists a `fence-empty` summary; its once-per-halt bound is unchanged.
   *(Design 6; checklist 10–11.)*
3. `/spec-brief`'s Phase 4 mapping names the `F<n>` Open form and the operator-claim
   rule; `/grill-me` names `fence-empty`; the workflow reference's paraphrase
   matches. *(Designs 7–8; checklist 12–14.)*
4. `lint.py --strict` reports zero ERROR and no new `missing-requires` WARN;
   `sync.py status` is clean and `sync.py push` round-trips byte-for-byte.
   *(Checklist 1, 15.)*
5. PR #26 threads 3945500857 and 3945500860 can be closed against the merged change.
   *(Designs 1 and 2 are those two threads' subjects; closed by hand at PR time.)*

## Out of scope

**Carried verbatim from the brief:**

1. Any change to the three bounds, the fork form, the advisory-recommendation rule,
   or the fact-finding dispatch rules.
2. The durable once-signal for 2f-i (VHS-32 Risk 14) — different surface, still
   correctly context-held.
3. The `requires:` vocabulary gaps (VHS-32 Risk 9) — their own ticket.
4. Editing anything under `docs/specs/DONE/VHS-32/` (D9).
5. A 2f-i re-offer of option 4 after a fence-empty grill (D7).
6. `source: operator` as a legal established-fact source (D4, D5).
7. Applying the plain-language rule outside the `grilling` primitive — the halt
   menus, previews and close plans of `/spec-brief`, `/spec-cycle`, `/spec-close` —
   which is VHS-34 (D11).
8. ASD-STE100's controlled dictionary as a vocabulary gate (D12).

**Spec-author additions to the fence** (each a consequence of a Decision above, not
new scope):

9. Fence item 1 and brief decision 4 are in tension: the fence bars changes to "the
   fact-finding dispatch rules", and decision 4 requires a verification dispatch that
   did not exist. This spec narrows the fence to exactly what decision 4 authorizes —
   the claim-verification path, its retry/cap/last-round rules, and nothing else. The
   three bounds, the fork form, the advisory rule and the ordinary fact-need dispatch
   are untouched.
10. Adding a mechanical assertion of the hand-off block's shape to `lint.py`,
    `sync.py`, or `tests/`. Brief F1 records that none exists; creating one is a
    design decision this ticket did not take. See Risks 1.
11. Updating the wiki decision that names this ticket as its revisit trigger — that
    is `/spec-close`'s decomposition step (D9).

## Risks

1. **The v2 contract is still prose with no mechanical assertion.** Nothing in
   `lint.py`, `sync.py` or `tests/` references `skills/grilling` (brief F1), and
   Out-of-scope 10 declines to change that. After this ships, the only assertions of
   the block's shape are this spec's checklist rows 4–8 and the archived VHS-32 row
   4 — both point-in-time, neither a regression gate. A future contract change has
   the same discovery cost this ticket paid.
2. **The `ref:` echo is model-rendered.** A mis-echoed, dropped, or malformed id is
   possible in a way a structured return value would not be. `unknown ref ignored:`,
   `item missing ref:` and the `not reached` clause are the mitigations; they make a
   mis-echo visible rather than impossible.
3. **VHS-32 Risks 9, 11 and 14 are unchanged, not fixed here.** Risk 9 (`requires:`
   has no token for nested skill invocation) and Risk 14 (the durable once-signal)
   are fenced above. Risk 11 (`user_invocable: false` is advisory; `grilling` still
   appears in the model's skill list) is unaffected by a contract-shape change — the
   `:12` guard sentence remains the only mechanism, and this spec keeps it (row 5).
4. **The touched surface is one commit old.** Every anchor here is correct at
   `7403cb5`, but `d381f88` merged the same day and no real `/spec-cycle` 2f-i grill
   has run against it. The contract is being revised before its first production
   exercise, so a shape that looks right may still read wrong in use.
5. **`/grill-me` degrades on non-repo topics.** D4/D5 send every operator answer
   through a repo exploration and bar `source: operator`. A `/grill-me` topic whose
   facts are policies, meeting outcomes or external constraints therefore cannot
   establish any fact, and every dependent question stays Open. Design 8 documents
   this in `/grill-me`'s failure modes; widening the fence would reverse the
   operator's own Q3/Q8 answers and belongs in its own ticket.
6. **A `fence-empty` brief renders an empty drift-check.** `/spec-cycle`'s Phase 3
   fallback bullet fires only on a *missing* header, and a `fence-empty` brief emits
   the header with `_(none)_` under it. Two of the three headers the parser keys on —
   `## Decisions carried forward` and `## Out of scope` — therefore render zero
   checkboxes at the HARD STOP. Mitigated (not closed) by Design 7's single
   `## Risks / decisions` item; the parser fix is deferred — see § Deferred.
7. **The post-cap resume can still burn its round on an empty one.** A post-cap
   resume that renders zero items exits `revised-after-cap (+1 round)` and consumes
   the operator's single extra round, as it does today. Fixing it means amending both
   `skills/grilling/SKILL.md:23` — a VHS-32 invariant checklist row 5 protects and
   D9's argument rests on — and `skills/spec-brief/SKILL.md:105`. Deferred rather
   than widened into this ticket; see § Deferred. A second route reaches the same
   waste: before Design 3's resume rule, a decision gated by a carried-over Open
   F-item would have waited on a fact that can never arrive. That route is closed —
   the decision renders anyway — but the underlying "a post-cap round can be spent on
   a round that renders nothing" remains true for other causes.

## References

- `skills/grilling/SKILL.md` — invocation contract `:14–23`, resume contract `:23`
  (unchanged), per-round output `:33–57` (`:48` F-numbering, `:52–55` round-end
  lines, `:57` post-cap header), decisions-are-the-operator's `:59–66` (`:63`
  rendered-items invariant), fact-finding `:68–78` (`:72` no-agent branch, `:74`
  unresolved carry, `:76` failed dispatch), bounds `:80–100` (`:85` item cap, `:88`
  twice-unanswered), termination `:102–112` (`:104` exit list, `:106` fence reason,
  `:108` stop-with-explorations, `:110` empty-seed), hand-off `:114–134` (`:116`
  render-exactly, `:119` header, `:122` Settled, `:125–126` Open, `:129` Facts,
  `:132` frontier bound), never-does `:136–138`, failure modes `:146–151` (`:148`
  failed dispatch, `:149` no-agent, `:151` stop-with-explorations).
- `skills/spec-cycle/SKILL.md` — 2f-i `:489–561` (seed `:495`, not-grillable
  `:499–505`, empty-seed guard `:507–509`, persist guard `:518–528`, verbatim append
  `:523`, apply `:539–546`, re-render `:548–554`; the seed field list spans
  `:494–495`), P2-deferral rule `:431`, Phase 3
  brief parser `:636–640`, failure modes `:698–708` (`:700–703` not-grillable record,
  `:703`/`:708` "with 1–3"), `## Tool-use notes` from `:646`.
- `skills/spec-brief/SKILL.md` — Phase 2 `:84–90`, Phase 3 `:92–107`, template
  `:113–128`, mapping rules `:134–143` (empty-Settled `:139`, Open→Risks `:140`,
  Scope `:141`, Facts→References `:142`, exit-token bullet `:143`), banner `:156–164`.
- `skills/grill-me/SKILL.md:14`, `:18–21`; `docs/spec-workflow-reference.md:23`,
  `:33`, `:35`.
- `docs/specs/DONE/VHS-32/spec.md` — checklist row 4 at `:458` (extended by row 5
  here), Design 1.1 / 1.7 / 1.8, Decisions S8 / S9, Risks 9 / 11 / 14,
  § Deferred (P2+). Read-only; never edited (D9).
- `vigil-harbor-wiki/decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md`
  — names VHS-33 as its revisit trigger; `/spec-close`'s job.
- `vigil-harbor-wiki/decisions/2026-08-09-review-round-artifacts-are-immutable.md` —
  closures are recorded forward, which is why row 5 extends rather than edits.
- PR #26 (https://github.com/ziomancer/vigil-skills/pull/26) threads 3945500857 and
  3945500860; merge commit `d381f88`.
- ASD-STE100, Simplified Technical English — Part 1 writing rules (D12).

## Deferred (P2+)

- **edge-cases R1 F-14 / R2 (reopened)** (P3) — an optional *cause* qualifier on
  `fact not established` for the four non-operator causes (`:72` no read-restricted
  agent, `:74` dispatch-cap overflow, `:76` failed dispatch, `:88` twice unanswered).
  Not folded. The operator-claim qualifiers were the caller-visible half and are in
  Design 3; distinguishing the other three is a legibility improvement with no caller
  today, and brief decision 3 pins the two-value set. Round 2 correctly caught that
  an earlier draft of this section claimed it *had* been folded — it had not.
- **edge-cases R2 F-9** (P2) — a `fence-empty` brief's present-but-empty
  `## Decisions carried forward` header defeats `/spec-cycle`'s Phase 3 drift-check
  fallback, which fires only when a header is *missing*. Design 7's single
  `## Risks / decisions` item mitigates the hollow-brief half, but the drift-check
  still renders zero checkboxes for Decisions. The fix — "if a header is missing **or
  its list is empty**" at `skills/spec-cycle/SKILL.md:640` — is a hunk in Phase 3,
  outside the `### 2f-i` region the brief scopes and checklist row 11 fences. Deferred
  as its own ticket rather than widened into this PR. Recorded as Risks 6.
- **edge-cases R2 F-11** (P2) — no path for an operator fact that is true but not
  repo-checkable. Not folded: admitting a non-repo source to `### Facts established`
  would reverse brief decisions 4 and 5, which are the operator's own answers (Q3,
  Q8). Design 8 documents the degradation in `/grill-me`'s failure modes instead, and
  Risks 5 records it as the follow-up ticket's subject.
- **edge-cases R3 F-4 / correctness R3 F-1** (P2 / P0-as-scope) — a post-cap resume
  that renders zero items still consumes the operator's one post-cap round. The
  round-3 draft fixed it inside the primitive, which amended `grilling:23` — outside
  this ticket's Scope, forbidden by checklist row 5, and falsifying one leg of D9's
  extends-not-supersedes argument — and was inert anyway without a matching change to
  `spec-brief:105`, which withdraws the resume option on *return*, not on *render*.
  Reverted to today's behaviour. Recorded as Risks 7; the fix is a two-file ticket.
- **correctness R1 F-11** (P4) — the touched surface landed one commit ago. No action
  requested by the reviewer; recorded as Risks 4.

Every other round-1 through round-4 P2/P3/P4 finding was folded into the designs, the
checklist, or the `## Risks` / `## References` sections. In particular
correctness R2 F-5 / R3 F-3 is now **closed, not deferred**: Design 2's F-item
ranking keeps `fact not established (operator claim, unverified)` on a `stop` exit,
so the qualifier survives for `/spec-brief` Phase 4 to carry.
