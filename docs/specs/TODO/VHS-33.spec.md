# VHS-33 — grilling hand-off contract v2: caller IDs, fact-item shapes, fence-empty token

**Brief:** `docs/specs/TODO/VHS-33.brief.md` (narrowed 2026-09-06; attempt 1 archived at
`docs/specs/TODO/VHS-33.attempt-1/`) · **Plane:** VHS-33 (Backlog) · **Attempt:** 2

## Goal

Change the `grilling` primitive's hand-off block — the one output every caller parses —
so that (1) a caller-supplied id survives the interview and comes back as a `ref:` field
on every Settled and Open item, (2) an unresolved fact request has its own `F<n>` Open
form instead of riding through as a question, (3) a round-1 interview that renders
nothing because no candidate met the altitude fence exits with a distinct `fence-empty`
token, and (4) every rendered round glosses its internal identifiers in plain language.
Then update the three callers and the reference paraphrase that consume the block. Five
files, prose only, one PR. Operator-supplied facts as claims to verify are **VHS-36**
and are not touched here.

## Scope

### Files to change

| Path | What changes | Where |
|---|---|---|
| `skills/grilling/SKILL.md` | `id` on seed items and the `ref:` paragraph after the hand-off fence (Design 1); plain-language paragraph (Design 4); six exits, the `fence-empty` paragraph, and the `stop` sentence (Design 3); the v2 hand-off block and callers-map sentence (Design 2) | `:18` (seed bullet), after `:57` (per-round output), `:104`, `:106`, `:108` (termination), `:118–130` (hand-off fence), new paragraph after `:130`, `:134` (callers map), `:151` (failure-modes `stop` bullet) |
| `skills/spec-cycle/SKILL.md` | 2f-i step 1 passes lens-qualified finding ids as seed `id`; step 4 locates findings by `ref:`; step 5 line reads `ref:` and prints the exit token; one sentence in the 2f-i failure-modes bullet (Design 5) | `:495–496`, `:539–546`, `:548–549`, `:698–703` |
| `skills/spec-brief/SKILL.md` | Phase 4 mapping for `F<n>` Open items; `fence-empty` recorded with its reason in the References bullet (Design 6) | `:140`, `:143` |
| `skills/grill-me/SKILL.md` | Failure-modes bullet naming `fence-empty` beside `empty-seed` (Design 7) | `:21` (new bullet after it) |
| `docs/spec-workflow-reference.md` | Paraphrase names the fence-empty shape, `ref:`, and unestablished facts (Design 7) | `:23`, `:35` |

### Files to create

None. `## Test command` is `N/A`; the checklist is the gate.

### Files to leave alone

- `skills/grilling/SKILL.md:14–17`, `:19–24` (invocation contract other than the seed
  bullet, including the `:23` resume contract), `:59–66` (Decisions are the
  operator's), `:68–79` (Fact-finding — VHS-36's surface), `:80–100` (Bounds),
  `:136–150` (What this skill never does, Tool-use notes, Failure modes other than
  the `:151` `stop` bullet, which Design 3 edits in step with `:108`).
- `skills/spec-cycle/SKILL.md` everywhere outside `### 2f-i` (`:489–561`) and the
  2f-i failure-modes bullet (`:698–703`): the 2f halt menu, 2e, 2g, Phase 3, the
  gate formula.
- `skills/spec-brief/SKILL.md` outside Phase 4's mapping rules (`:134–143`): Phase 2
  (`:84–90`) keeps halting on `empty-seed` only; Phase 3 (`:92–107`) is unchanged.
- `docs/specs/DONE/VHS-32/` (D7).
- `agents/`, `skills/ship-spec/`, `skills/spec-close/`, `lint.py`, `sync.py`, `tests/`.
- `README.md`, `AGENTS.md`, and every file under `docs/` outside `docs/specs/` other than
  `docs/spec-workflow-reference.md`. Neither README nor AGENTS.md paraphrases the
  hand-off contract or the exit tokens (checked 2026-09-06), so they are fenced, not
  in scope.

## Decisions

D1–D12 are the brief's `## Decisions carried forward`, in its numbering. D13 records
the brief's `## Scale` non-factor. **Spec-level additions** — constructs the brief does
not name, each justified at its point of use and listed here for the Phase 3
drift-check:

- Seed ids are lens-qualified, `<lens>/<finding-id>` (Design 5). Reuse of the two-part
  form 2b's closure manifest uses at `skills/spec-cycle/SKILL.md:366` and 2f-i's own
  `not grillable:` line uses at `:504` — not 2e's round-qualified three-part
  `correctness/R1/F-3` at `:453`. Needed because every lens numbers its findings
  `F-1…`.
- `blocked-on: F<n>` as a Q-item reason (Design 2). Needed by D3: once the fact is its
  own Open item, the question waiting on it has to point at it, exactly as
  `blocked-on: Q<m>` already points at a question.
- The both-lists rule in the step-5 line (Design 5): an id on both a Settled and an
  Open item is printed under `left open` rather than `dispositioned` (it may still
  appear under `deferred to option 3`). Needed to make the brief's Risk 1 pin
  complete; one sentence.
- The step-5 line carries the summary's exit token (Design 5). Needed so a
  `fence-empty` grill is legible at the halt without opening `grill.md` (D6);
  uniform across exits, no purpose-written line.
- The Q-item reason list drops `fact not established` (Design 2). Needed by D3: a
  caller can tell "needs a fact" from "needs a decision" only if that reason renders
  on F-items alone. No caller matches the string today — outside `docs/specs/`,
  `grep -rn 'fact not established'` hits only the primitive (`:74`, `:88`, `:125`).
- F-items carry their number from the `F1…Fn` series whether or not they were rendered
  (Design 2). Reuse, not addition: `### Facts established` (`:129`) already numbers
  facts obtained by dispatch and never rendered as `ℹ️` requests, so the series
  already numbers fact needs. Needed so `blocked-on: F<n>` always resolves.
- `rounds: 1/<round_cap>` on a `fence-empty` header (Design 3). Needed because three
  consumers read the field (`spec-brief:143`, `:159`; `grilling:23`) and Design 6's
  References bullet hard-codes the value. The round was attempted and consumed.
- The `/spec-brief` References bullet is keyed on the header's *reason*, not the exit
  token (Design 6), so a later-round `empty-frontier` fence-out also records
  `no candidate decision met the altitude fence`. Needed because Design 3 makes that
  reason load-bearing on both exits; one rule instead of two, inside the line already
  being rewritten (edge-cases R2 F-6).
- `unknown` as the step-5 `<token>` when the returned header carries no exit
  (Design 5). Needed because step 5 now depends on a header field step 3's guard does
  not check (it tests only for a `## Grill summary` line); the persisted block is the
  record (edge-cases R3 F-6). The step-4 tolerance for a Settled item with no `ref:`
  field at all (Design 5, edge-cases R3 F-4) is the same one-clause read of the same
  malformed return.

Nothing else. In particular this spec adds no seed-id legality rule, no empty-section
sentinel in the hand-off block, no round preamble, no reason-precedence order, no cause qualifiers, and no
verification or resume rule for F-items (D11, D12).

### D1 — Caller IDs survive the hand-off (brief 1, Q1)

Design 1 adds an optional `id` to each seed item and Design 2 renders it as `ref:` on
every Settled and Open item, including the rolled-up deferred item. Absent entirely
when the caller passed no ids.

### D2 — `ref:` holds zero or more IDs (brief 2, Q9)

`ref:` renders a comma-separated list, or `none`. Determinism comes from the field
being present whenever the caller supplied ids, not from its arity (Design 1).

### D3 — Fact items get their own shape (brief 3, Q2)

Design 2 adds the `**F<n> — <fact needed>**` Open form with the reason set
`fact not established | stopped` — exactly two values, no qualifier. The Bounds and
Fact-finding sentences that route unresolved facts to the hand-off (`:74`, `:88`) are
not edited; they say "Open with `fact not established`", and the F-form is where such
an item now lands.

### D4 — `fence-empty` is a distinct exit token (brief 4, Q4)

Design 3 makes it the sixth exit, reached only when round 1 renders zero items because
no candidate met the altitude fence. It goes through the hand-off block with its
Settled and Open frontier sections empty; the header's reason line stays. It narrows wiki decision
`2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write` § 5 — see Risks 2.

### D5 — A fence-empty grill still consumes the once-per-halt bound (brief 5, Q5)

Design 5 changes nothing about the bound: 2f-i's closing paragraph (`:556–561`) is
untouched and the menu re-renders with options 1–3. No re-offer.

### D6 — A fence-empty grill is persisted (brief 6, Q10)

Design 5: the returned summary has a `## Grill summary` block, so step 3's existing
guard lets it through and appends it verbatim under the usual `# Grill <k>` header.
That block — a header carrying `exit: fence-empty` and three empty sections, on the
2f-i path, which seeds findings and no facts — is the "one short block". No
purpose-written text.

### D7 — The archived VHS-32 spec is not edited (brief 7, Q6)

Checklist row 5 re-asserts every string VHS-32 checklist row 4 asserts and adds the v2
block; row 10 re-asserts every string VHS-32 checklist row 7 pins in 2f-i and the
byte-identical fences of its row 6. Together they supersede VHS-32 rows 4, 6 and 7,
which are not re-runnable from `DONE/`. These supersessions are declared here, not in
the additions roll-up: they are checklist bookkeeping, not constructs.
`docs/specs/DONE/VHS-32/` is untouched.

### D8 — `/spec-brief` and the workflow reference are in scope (brief 8, Q7)

Designs 6 and 7.

### D9 — A plain-language rendering rule, for the primitive's rounds only (brief 9, Q11/Q13)

Design 4 adds one paragraph to the per-round output contract. No other skill's
operator-facing block is touched (VHS-34).

### D10 — ASD-STE100 writing rules, not its dictionary (brief 10, Q14)

Design 4's paragraph names the writing rules and says the dictionary is not applied.

### D11 — Operator-supplied facts are out of this ticket (brief 11)

No design here verifies, qualifies, or resumes an operator-supplied fact. Checklist
row 16 greps the `grilling` diff for the words that would mean otherwise.

### D12 — The spec stays inside the brief (brief 12)

The additions roll-up above is the complete list. A reviewer finding that seems to
need another construct goes to `## Deferred (P2+)` with its id.

### D13 — Scale is an explicit non-factor

The brief's `## Scale` says `**Factor:** no`. Recorded here so Phase 3 has its anchor.
No scale machinery: the hand-off block's size bound at `:132` is unchanged. Unresolved
fact needs already reached the hand-off as Open items under v1 (`:74`); this spec
changes their rendered shape, not their count, so the bound is exactly as tight as
before.

## Design

### 1. `ref:` — caller ids through the hand-off

**Invocation contract** (`skills/grilling/SKILL.md:18`). The `seed` bullet gains two
sentences:

> Each seed item may carry an optional **`id`** — a caller-stable string the primitive
> echoes back as `ref:` on every Settled and Open item that descends from it. 2f-i
> passes finding ids; `/spec-brief` and `/grill-me` pass none, and then no `ref:`
> field is rendered at all.

**The `ref:` paragraph** — new, inserted after the hand-off fence closes (`:130`) and
before the size-bound sentence (`:132`), so the descent and omission rules ship in
the file:

> `ref:` renders on every Settled and Open item when any seed item carried an `id`,
> and on none otherwise. An item's ids are those of the seed items it descends from:
> a question descends from the seed items it was raised to disposition, a decision
> from its question, a fact request from the question whose need raised it (or from
> the seed items directly when the need arose from the seed), the rolled-up deferred
> item from the deferred question. Ids are
> listed in seed order; an item descending from no identified seed item (a fact-driven
> decision, or a question raised about an unidentified seed item) renders `ref: none`.

Descent is the primitive's own tree, not a title match. With no ids, the Settled and
Open-question lines are byte-identical to v1 — the `ref:` field is the only thing
appended to them. The block as a whole still changes for every caller: the header
gains `fence-empty`, the F-item form is new, and the rolled-up line gains a period
(Design 2). `/spec-brief` and `/grill-me` receive that no-id block.

### 2. The v2 hand-off block

The fenced block at `:118–130` becomes:

```
## Grill summary — <seed title> (rounds: <n>/<round_cap>, exit: empty-frontier | fence-empty | round-cap | stop | revised-after-cap (+1 round); reason: tree fully visited | no candidate decision met the altitude fence | cap reached | operator stop | resume)

### Settled
1. **<decision title>** (Q<n>) — chose <A/B/free-form answer>: <one line>. Facts relied on: <F-ids or "none">. ref: <id>[, <id>…] | none

### Open frontier
1. **<question title>** (Q<n>) — branches: <A/B>; recommendation: <X>; unresolved because: <round-cap | deferred | stopped | blocked-on: Q<m> | blocked-on: F<n>>. ref: <…>
2. **F<n> — <fact needed>** — unresolved because: <fact not established | stopped>. ref: <…>
3. **<parent title> — downstream decisions not explored (deferred at round <n>)**. ref: <…>

### Facts established
- F1 — <fact> (source: <path:line>)
```

Changes against v1, and nothing else:

- `fence-empty` joins the header's exit list (Design 3). The reason list is unchanged.
- `ref:` is the trailing field on the Settled line, the Open question line, the new
  F line, and the rolled-up line (Design 1). When no seed item carried an id the
  field is omitted on all four (Design 1), so the Settled and Open-question lines are
  unchanged for a no-id caller.
- **The F-item is new** (D3). A fact request was never a fork, so it carries no
  branches and no recommendation. Its `unresolved because:` takes exactly two values:
  `fact not established` (the fact-finding machinery finished without the fact — twice
  unanswered per `:88`, dispatch-cap overflow per `:74`, failed dispatch per `:76`, no
  read-restricted agent per `:72`) or `stopped` (an exploration abandoned at `stop`,
  per `:108`). It carries its number from the parallel `F1…Fn` series (`:48`),
  whether or not it was ever rendered as an `ℹ️` request — a dispatch-cap overflow or
  an abandoned in-flight exploration was numbered when it became a fact need.
- The Q-item reason list gains `blocked-on: F<n>` beside `blocked-on: Q<m>` and drops
  `fact not established`: the fact is now its own F-item and the question waiting on
  it points there. D3 holds only if the fact reason renders on F-items alone; no
  caller matches the string (additions roll-up).
- The rolled-up line gains a period before `ref:`, matching the other three lines.
- Empty sections render as the header with nothing under it. On `fence-empty` Settled
  and Open frontier are empty; Facts established holds whatever the seed supplied or a
  dispatch returned — for `/spec-brief`, which grounds first, that is normally not
  empty. `/spec-brief` already handles an empty
  Settled section (`:139`).

**Callers-map sentence** (`:134`) becomes:

> Callers map the block: `/spec-brief` turns Settled into `## Decisions carried
> forward`, Open Q-items and F-items into `## Risks / decisions` items ending "spec
> author pins this", and feeds Facts into Scope and References; 2f-i drives its 2e
> edits from Settled, matching each decision to its findings by `ref:`, and leaves
> Open in the red list.

The size bound at `:132` is unchanged.

### 3. `fence-empty` — the sixth exit

`:104` becomes:

> The exits are `empty-frontier`, `fence-empty`, `round-cap`, `stop`,
> `revised-after-cap (+1 round)` (the suffix is part of the rendered token), and
> `empty-seed`.

`:106` becomes:

> `empty-frontier` is reachable only after at least one round was rendered; its reason
> line distinguishes `tree fully visited` from `no candidate decision met the altitude
> fence` (a later round's remaining candidates all fell below the fence). If the tree
> has a root but no round-1 candidate satisfies the altitude fence, nothing is
> rendered and the exit is `fence-empty`, with that same fence reason and
> `rounds: 1/<round_cap>` — the round was attempted and consumed. Both go through
> the hand-off block; on `fence-empty` its Settled and Open frontier sections are
> empty, and `### Facts established` is rendered as on any exit — empty unless the
> seed supplied facts or a dispatch returned one.

`:108` has one clause replaced so the `stop` sentence names the F-item shape and keeps
the waiting question: "their questions are Open with `unresolved because: stopped`"
becomes "their fact needs are Open `F<n>` items with `unresolved because: stopped`,
and any question that was waiting on one is Open with `unresolved because:
blocked-on: F<n>`". The rest of the sentence is unchanged. The `## Failure modes`
bullet at `:151` describes the same event; its clause "their questions are Open with
`unresolved because: stopped`" is replaced with the same wording, so the file says one
thing about `stop`.

`:110` ("Every exit but `empty-seed` goes through the hand-off contract") is already
true of the sixth exit and is not edited. `empty-seed` (no root at all, `:31`) is
unchanged and remains the only exit without a block.

### 4. The plain-language rendering rule

One paragraph, inserted after `:57` (the post-cap-round sentence) and before
`## Decisions are the operator's`:

> **Plain language.** Every rendered round glosses each internal identifier on its
> first use in that round — a section code such as `2f-i`, an exit token such as
> `empty-frontier`, a file or block name — with a few words in parentheses saying
> what it is. Write in the ASD-STE100 style: short sentences, one instruction per
> sentence, one meaning per term. Keep question bodies short; the fork's `For:` /
> `Against:` lines carry the detail. The STE controlled dictionary is not applied. This
> rule governs rendered rounds; the hand-off block is rendered exactly as its contract
> states.

That is the whole rule. No sentence count, no preamble slot.

### 5. `/spec-cycle` 2f-i — seed ids in, `ref:` out

**Step 1** (`:495–496`): "extract each remaining P0/P1 finding: id, severity, title,
body" becomes "extract each remaining P0/P1 finding: id, severity, title, body. The
id is lens-qualified — `<lens>/<finding-id>`, the two-part form 2b's closure manifest
and this step's own `not grillable:` line already use — and is passed as the seed
item's `id` so the hand-off's `ref:` field carries it back."

**Step 4** (`:539–546`): "For each **Settled** item, edit the spec in place …" gains,
after its first sentence: "Locate the finding(s) a decision dispositions by its
`ref:` ids, never by title. A Settled item with `ref: none` — or with no `ref:` field
at all, which is what a v1-shaped return looks like — is applied as a spec edit like
any other but dispositions no finding."

**Step 5** (`:548–549`): the line becomes

```
grill applied (exit: <token>): dispositioned <ids>; left open <ids>; not grillable <ids>; deferred to option 3 <ids>; unreferenced decisions applied: <n> — docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md
```

built as follows (this is the brief's Risk 1 pin). The code block replaces `:549`
only — step 5's `5. **Re-render.** Print` lead-in at `:548` and its `, then the 2f
halt block again …` continuation at `:550–554` are unchanged, and the line stays an
inline code span on its own physical line, keeping its trailing comma, as today. The
bullets below are added to step 5 in the file, immediately after `:554`, except the
`not grillable` bullet and the closing "Nothing else in 2f-i changes for this exit"
sentence, which are spec-level notes; drop "as today" from the `deferred to option 3`
bullet when shipping it:

- `<token>` is the exit from the summary header; when the header carries none, print
  `unknown` — the persisted block is the record.
- `dispositioned` lists every id on a Settled item that step 4 applied, each id once,
  in seed order, however many ids one decision carried.
- `left open` lists every id on an Open item (Q, F, or rolled-up), each id once, in
  seed order. An id that appears on both a Settled and an Open item is listed here
  rather than under `dispositioned` — a finding is not dispositioned while anything
  about it is still open. It still appears under `deferred to option 3` if step 4
  could not apply its Settled item. A seeded id that appears on no Settled and no Open
  item is in none of these lists — it stayed P0/P1 and is still listed in the
  re-rendered halt block; the lists report what the grill touched, not the full red
  list.
- `deferred to option 3` lists ids on Settled items step 4 could not apply, as today.
- `not grillable` is unchanged.
- `unreferenced decisions applied: <n>` counts Settled items with `ref: none` that
  step 4 applied. It always prints, `0` included, like the other lists.
- On `fence-empty` the `dispositioned`, `left open`, and `deferred to option 3` lists
  are empty and the count is `0`; `not grillable` is unaffected — those findings never
  entered the seed and this line is their only record. The `fence-empty` token is the
  signal that nothing was askable and every seeded finding remains P0/P1; the empty
  `left open` is not a claim that nothing is open. The menu re-renders with options
  1–3 (D5, D6). Nothing else in 2f-i changes for this exit: step 3's guard passes the
  block (it has a `## Grill summary` line) and appends it verbatim.

**Failure-modes bullet** (`:698–703`) gains one sentence at its end: "A `fence-empty`
exit is the same shape: nothing moved, the empty summary is persisted, the menu
re-renders with 1–3."

The closing paragraph (`:556–561`, "never re-dispatches reviewers … at most once per
invocation") is untouched.

### 6. `/spec-brief` — mapping the new shapes

`/spec-brief` passes no seed ids, so the block it receives has no `ref:` fields
(Design 1). Two mapping rules change:

`:140` becomes:

> Open frontier items → `## Risks / decisions`, numbered, each ending "spec author
> pins this". An `F<n>` item is written as `<fact needed> — not established; spec
> author pins this`.

That is the shape `:80` uses for a failed exploration under `--no-grill`, without its
`(exploration failed)` cause — no cause qualifiers (roll-up). The rationale stays in
this spec, not in the shipped rule: checklist row 16 greps the shipped text.

`:143` becomes:

> The exit token and round count go in a final `## References` bullet:
> `Interview: <n> rounds, exit <token>`, or `Interview: skipped (--no-grill)`. When the
> header's reason is `no candidate decision met the altitude fence`, the bullet also
> carries it: `Interview: 1 rounds, exit fence-empty (no candidate decision met the
> altitude fence)`, or `Interview: 2 rounds, exit empty-frontier (no candidate
> decision met the altitude fence)` for a later-round fence-out.

`fence-empty` is not `empty-seed`: Phase 2 (`:88`) does not halt on it, the brief is
written, and `:139`'s empty-Settled rule and warning apply. No other line changes.

### 7. `/grill-me` and the workflow reference

`skills/grill-me/SKILL.md`: a third failure-modes bullet after `:21`:

> - On `fence-empty` (the topic has a root decision but nothing about it is askable at
>   brief altitude), deliver the Grill summary as usual — its header's reason line is
>   the answer.

`docs/spec-workflow-reference.md:23` becomes:

> **Termination shapes and where each lands.** An emptied frontier means the tree was
> fully visited, or that a later round's remaining candidates all fell below the
> altitude fence — either way the reason line says which, and anything the operator
> deferred is still in the brief's open items. A fence-empty exit means nothing
> met the altitude fence in round 1 — the brief is written with no decisions and the
> reason recorded. A cap hit or an operator stop is a documented outcome, not a
> failure: the unresolved branches — questions and unestablished facts alike — go to
> `## Risks / decisions` for the spec author. An empty seed is the one shape that
> writes nothing at all.

`:35` becomes:

> It ends by rendering a **hand-off block** — settled decisions, the open frontier
> with a reason for each unresolved question and each unestablished fact, the facts
> established with their sources, and, when the caller tagged its seed items, a
> `ref:` on each item naming the seed items it came from — and writes no file: every
> write belongs to the caller.

## Test plan

Doc/prompt-only change → review checklist, no dry-run transcript. Every row is a grep
or a diff against the worktree. `skills/grilling/SKILL.md` and the `spec-brief` mapping
bullets are unwrapped, so their phrase assertions are line greps;
`skills/spec-cycle/SKILL.md` is hard-wrapped at about 78 columns, so phrase assertions
against it are checked over the section text (`tr -s '[:space:]' ' '` before grepping,
so wrapped continuation indents collapse too), not line-anchored — "never edits the
brief" already spans `:557–558` in the pre-edit file. The checklist is the `/ship-spec` gate because
`## Test command` is `N/A`.

**Review checklist:**

1. `python lint.py --strict` → exit 0; zero ERROR; `missing-requires` WARN count is 2
   (unchanged: `review-pr`, `ship-spec`).
2. `grep -nE '\b(Explore|Agent|Skill|general-purpose)\b' skills/grilling/SKILL.md skills/grill-me/SKILL.md skills/spec-brief/SKILL.md`
   → every hit is inside a parenthetical carrying "or the equivalent", or under a
   `## Tool-use notes` heading, or is the prohibition itself. For
   `skills/spec-cycle/SKILL.md`, `git diff -U0` added lines contain no `Agent(`.
3. `grep -c 'model:' skills/grilling/SKILL.md skills/grill-me/SKILL.md skills/spec-brief/SKILL.md` → 0 each.
4. **The v2 block.** `skills/grilling/SKILL.md` contains, verbatim, inside the
   hand-off fence: `exit: empty-frontier | fence-empty | round-cap | stop | revised-after-cap (+1 round)`;
   `ref: <id>[, <id>…] | none` on the Settled line; `ref: <…>` on the Open question
   line, the F line, and the rolled-up line (which ends `)**. ref: <…>`);
   `**F<n> — <fact needed>** — unresolved because: <fact not established | stopped>`;
   the Open question line's reason list is exactly
   `<round-cap | deferred | stopped | blocked-on: Q<m> | blocked-on: F<n>>`. The
   reason list in the header is unchanged from v1.
5. **Supersedes VHS-32 checklist row 4.** `grilling` body still contains, verbatim:
   the guard sentence (`:12`); the fact-finding dispatch sentence including "make no
   mutations of any kind" (`:70`); the fork block (`:37–44`); "advisory. It is never a
   default that carries by silence" (`:61`); the bounds with defaults 3 / 7 / brief
   altitude and "questions and fact requests together" (`:84–86`); the worked-examples
   table (`:94–98`); `### Settled` / `### Open frontier` / `### Facts established`;
   the `empty-seed` exit; the `:23` resume contract with `revised-after-cap (+1 round)`.
   `## Tool-use notes` and `## Failure modes` are real `##` headings. Plus row 4 above.
6. `grep -c 'fence-empty' skills/grilling/SKILL.md` ≥ 3 (exits list, `:106` paragraph,
   header). The `:104` sentence lists exactly six tokens. The `:106` paragraph says
   `fence-empty`, `no candidate decision met the altitude fence`, and
   `rounds: 1/<round_cap>`. The `:108` sentence contains "their fact needs are Open
   `F<n>` items with `unresolved because: stopped`" and "blocked-on: F<n>"; the
   `:151` bullet contains "their fact needs are Open `F<n>` items".
7. The `seed` bullet in `## Invocation contract` contains `id`, `ref:`, and "no
   `ref:` field is rendered at all". A paragraph beginning `` `ref:` renders on every
   Settled and Open item `` sits between the hand-off fence and the size-bound
   sentence and contains "and on none otherwise", "descends from", and "a fact request
   from the question whose need raised it". The callers-map sentence contains
   "F-items" and "by `ref:`". `grep -c 'ref:' skills/grilling/SKILL.md` ≥ 7 —
   matching lines, not occurrences: seed bullet, the `ref:` paragraph, four block
   lines, callers-map sentence; the file is unwrapped, one paragraph per line.
8. A paragraph beginning `**Plain language.**` sits between the post-cap-round
   sentence and `## Decisions are the operator's`; it contains "first use",
   "ASD-STE100", and "dictionary is not applied"; it states no sentence count, word
   limit, or other numeric bound on round length, and adds no round-preamble slot.
9. `git diff -U0 -- skills/grilling/SKILL.md` shows **no hunks** in `:1–17`, `:19–32`,
   `:59–100`, `:136–150` of the pre-edit file (invocation apart from the seed bullet,
   resume contract, tree/frontier, Decisions, Fact-finding, Bounds, and the three
   tail sections). The pre-edit `:132` (the size-bound sentence) is byte-identical.
10. `git diff -U0 -- skills/spec-cycle/SKILL.md` shows hunks only inside `:489–561`
    (`### 2f-i`) and `:698–703`; `grep -c 'total_p0p1 == 0' skills/spec-cycle/SKILL.md`
    unchanged; 2e
    (`:426–465`), 2f's fenced menu (`:466–487`), and 2g (`:563–595`) byte-identical.
    2f-i step 1 contains `<lens>/<finding-id>`; step 4 contains "by its `ref:` ids,
    never by title" and "or with no `ref:` field at all"; step 5 contains
    `grill applied (exit: <token>):`, `unreferenced decisions applied: <n>`, "is listed
    here rather than under `dispositioned`", "in seed order", "print `unknown`", and
    "not the full red list", and still begins `5. **Re-render.** Print`; the
    `:698–703` bullet contains "A
    `fence-empty` exit is the same shape". **Supersedes VHS-32 checklist row 7:**
    `### 2f-i` still contains "never re-dispatches reviewers", "never increments the
    round counter", "never overwrites", "at most once per invocation", "never edits
    the brief", "not grillable", "nothing grillable", "deferred to option 3", and the
    path `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`; the 2f halt block
    still contains the scalability line.
11. `git diff -U0 -- skills/spec-brief/SKILL.md` shows hunks only at `:140` and
    `:143`; `grep -c 'fence-empty' skills/spec-brief/SKILL.md` ≥ 1; `:140` contains
    `F<n>` and "not established; spec author pins this"; `:88` unchanged.
12. `skills/grill-me/SKILL.md` `## Failure modes` has three bullets; the third names
    `fence-empty`; `:14` unchanged.
13. `grep -c 'fence-empty' docs/spec-workflow-reference.md` ≥ 1 and `:23` contains
    it; `:23` contains "altitude fence" at least twice and "either way the reason line
    says which" (the emptied-frontier fence case survives the rewrite); `:35` contains
    `ref:` and "unestablished fact"; no line other than `:23` and `:35` changes.
14. No file under `agents/`, `skills/ship-spec/`, `skills/spec-close/`,
    `docs/specs/DONE/` changed; `lint.py`, `sync.py`, `tests/`, `README.md`,
    `AGENTS.md`, and every file under `docs/` outside `docs/specs/` other than
    `docs/spec-workflow-reference.md` unchanged.
15. `python sync.py status` clean after `python sync.py install`; `python sync.py push`
    is a no-op (byte-for-byte round trip).
16. **VHS-36 fence.** `git diff -U0 -- skills/grilling/SKILL.md skills/spec-brief/SKILL.md | grep '^+' | grep -v '^+++' | grep -ciE 'operator claim|verif|qualifier|source: operator'`
    → 0 (added content lines only; hunk headers and removed lines do not count).

## Test command

N/A

## Done when

- The hand-off block in `skills/grilling/SKILL.md` carries an optional `ref:` field on
  every Settled and Open item including the rolled-up deferred item (Designs 1, 2;
  rows 4, 7), defines `F<n>` Open forms (Design 2; row 4), and lists `fence-empty` as
  an exit (Design 3; row 6); the per-round output contract carries the plain-language
  rule (Design 4; row 8).
- `/spec-cycle` 2f-i passes finding ids as seed ids, reads `ref:` in its step 5 line,
  and persists a `fence-empty` summary; its once-per-halt bound is unchanged
  (Design 5; row 10).
- `/spec-brief`'s Phase 4 mapping names the `F<n>` Open form (Design 6; row 11);
  `/grill-me` names `fence-empty` (Design 7; row 12); the workflow reference's
  paraphrase matches (Design 7; row 13).
- `lint.py --strict` reports zero ERROR and no new `missing-requires` WARN;
  `sync.py status` is clean and `sync.py push` round-trips byte-for-byte (rows 1, 15).
- PR #26 thread 3945500857 can be closed against the merged change; thread 3945500860
  can be answered with the `F<n>` shape and pointed at VHS-36 for its second half.

## Out of scope

Carried from the brief, verbatim in substance:

1. Operator-supplied facts as claims to verify, unverifiable-claim handling, and any
   `/spec-brief` mapping for verified operator claims — **VHS-36** (row 16).
2. Any change to the three bounds, the fork form, the advisory-recommendation rule,
   or the fact-finding dispatch rules (`skills/grilling/SKILL.md:68–79`) (row 9).
3. The durable once-signal for 2f-i (VHS-32 Risk 14).
4. The `requires:` vocabulary gaps (VHS-32 Risk 9).
5. Editing anything under `docs/specs/DONE/VHS-32/` (row 14).
6. A 2f-i re-offer of option 4 after a fence-empty grill (D5).
7. `source: operator` as a legal established-fact source (row 16).
8. Applying the plain-language rule outside the `grilling` primitive — VHS-34.
9. ASD-STE100's controlled dictionary as a vocabulary gate (row 8).
10. The Phase 3 drift-check's missing-header fallback on a present-but-empty list
    (`skills/spec-cycle/SKILL.md:640`) — its own ticket.
11. A post-cap resume that renders zero items still consuming the post-cap round
    (`grilling:23` + `spec-brief:105`) — its own ticket.
12. `/spec-brief` Phase 3 offering "revise an answer by Q number" after a summary
    with no Q items (`spec-brief:99`) — pre-existing under v1's fence reason line,
    fenced Phase 3 region; the same ticket as item 11 (edge-cases R1 F-11).

## Risks

1. **A caller that greps the v1 Open line shape** would see a trailing `ref:` only when
   it supplied ids (Design 1). `/spec-brief` and `/grill-me` supply none and see
   unchanged Settled and Open-question lines; the F-item form and the `fence-empty`
   header they do see are covered by Designs 6 and 7. The only id-supplying caller is
   2f-i, updated in the same PR.
2. **A `fence-empty` brief is hollow** (edge-cases R1 F-3). `/spec-brief` does not
   halt on it (Design 6), so the brief is written with `_(none settled …)_` under
   Decisions, an empty Risks list, at most the Scope rows Phase 1's grounding facts
   name (each with an empty `Change` column, `spec-brief:141`), and no fact References beyond the
   ones Phase 1's grounding already supplied; the
   `Interview:` bullet carrying the reason is the only signal, and `/spec-cycle`'s
   present-but-empty parse is Out of scope 10. Accepted: halting lands in the fenced
   Phase 2 region and would be a new construct; the operator sees the empty preview
   at Phase 3 and can abort. This narrows wiki decision
   `2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write` § 5 ("Rejected — a
   success token for an empty interview"): `empty-seed` remains the only halt;
   `fence-empty` is a success token whose brief is hollow by design. The rationale
   sentence at `spec-brief:88` is left as written because it is about `empty-seed`.
   `/spec-close` records the narrowing.
3. **Both-lists rule hides partial progress.** A finding with one settled and one open
   question prints as `left open`. The spec edit from the settled decision still
   happened (step 4) and `grill.md` shows it. The halt block's
   ` — grilled (spec edited; not re-reviewed)` suffix (`spec-cycle:551`) is keyed on
   `dispositioned` too, so such a finding is unmarked there as well; `grill.md` and the
   spec diff are the record, and option 1 re-reviews the edited text. Accepted for a
   one-line rule.
4. **Line anchors drift** the moment `grilling`, `spec-cycle`, or `spec-brief` is
   edited. All anchors were read at `7403cb5` on 2026-09-06; `/ship-spec` re-reads.

## References

- `skills/grilling/SKILL.md:12` (guard), `:18` (seed bullet), `:23` (resume contract),
  `:31` (`empty-seed`), `:33–58` (per-round output; `:48` F-numbering, `:57` post-cap
  sentence), `:72`, `:74`, `:76` (fact-finding terminal dispositions), `:88` (twice
  unanswered), `:104`, `:106`, `:108`, `:110` (termination), `:118–130` (hand-off
  fence), `:132` (bound), `:134` (callers map) — read 2026-09-06 at `7403cb5`.
- `skills/spec-cycle/SKILL.md:366` (closure-manifest `<lens>/<finding-id>` form),
  `:453` (2e's three-part form, not used), `:504` (2f-i `not grillable:` form),
  `:489–561` (2f-i; `:495–496` step 1, `:518–528` step 3 guard, `:539–546` step 4,
  `:548–549` step 5, `:556–561` closing paragraph), `:698–703` (2f-i failure-modes
  bullet).
- `skills/spec-brief/SKILL.md:80` (failed-exploration Risks wording), `:88` (empty-seed
  halt), `:139` (empty Settled), `:140`, `:143`; `skills/grill-me/SKILL.md:14`, `:21`;
  `docs/spec-workflow-reference.md:23`, `:35`.
- `docs/specs/DONE/VHS-32/spec.md:458` (checklist row 4, superseded by row 5 here).
- `docs/specs/TODO/VHS-33.attempt-1/` — brief, spec, twelve reviewer reports. Structure
  not carried (brief decision 12).
- PR #26 threads 3945500857, 3945500860; merge commit d381f88.
- VHS-36 (operator-supplied facts), VHS-34 (plain-language pass elsewhere), VHS-37
  (spec-cycle fold-vs-defer escape hatch).

## Deferred (P2+)

Not folded, each with the reason. Every other round-1 through round-4 P2+ finding was
folded. The round-4 edge-cases P1 (F-1, the `:548–549` → `:549` correction in
Design 5) is applied and confirmed CLOSED by an operator-requested delta re-check
(`round-4/edge-cases-delta.md`, STATUS GREEN); there is no round 5.

## Post-green polish

Off-protocol: the gate never went green in 2d (round 4 closed at `total_p0p1 = 1`);
the operator chose "patch and review the delta" at the halt, and the delta re-check
returned GREEN. Its two `Pre-ship recommended` P2s and two P4s were folded here as
clarifications, none touching Decisions, Out of scope, or Done when:

- **edge-cases R4-delta F-1** — Test-plan preamble: `tr -s '[:space:]' ' '` so
  wrapped continuation indents collapse before phrase greps.
- **edge-cases R4-delta F-2** — Design 5 names which step-5 bullets ship and which
  are spec-level notes; "as today" dropped from the shipped `deferred to option 3`
  bullet.
- **edge-cases R4-delta F-3** — Design 5: the replaced `:549` keeps its trailing comma.
- **edge-cases R4-delta F-4** — Deferred preamble records the delta re-check.

- **edge-cases R1 F-6** (P2) — a `ref:` id that matches no seeded finding has no
  step-4 rule. Not folded: a validation rule is the seed-id legality construct brief
  decision 12 removed from attempt 1. The rule to adopt if wanted: treat it as
  `ref: none` — apply the edit, count it under `unreferenced decisions applied`, do not
  print the id under `dispositioned`.
- **edge-cases R1 F-8** (P2) — a Settled item with `ref: none` that step 4 could not
  apply appears in no step-5 list; `grill.md` records it as Settled-but-unapplied
  (`spec-cycle:543–545`). Not folded: a sixth clause is the "extra step-5 clauses"
  fence. Rare by construction (a fact-driven decision that requires narrowing the
  brief).
- **edge-cases R1 F-15** (P3) — `/spec-brief` maps a `stopped` F-item and a
  `fact not established` F-item to the same "not established" Risks text. Not folded:
  a cause qualifier, fenced by brief decision 12. Two words if the operator wants it
  later: `(interview stopped)`, on the `:80` precedent.
- **edge-cases R1 F-18** (P4) — `ref:` id character legality against the
  comma-separated list. Not folded, by the same fence; unreachable today (2f-i is the
  only id-supplying caller and its ids are `<lens>/F-<n>`).
- **edge-cases R3 F-3** (P2) — an id on both an applied and an unapplied Settled item
  prints under `dispositioned` and `deferred to option 3`. Not folded: a precedence
  clause is the reason-precedence construct brief decision 12 removed. The rule to
  adopt if wanted: an id on any unapplied Settled item prints under
  `deferred to option 3` only, since the finding stays P0/P1.
- **edge-cases R3 F-5** (P3) — `ref:` ids are undefined across a `prior_summary`
  resume; the descent rule reads ids from seed items and the resume contract (`:23`)
  never mentions the seed. Not folded: a resume rule for the new field, on the same
  fence as the F-item resume rule (brief decision 11). The rule to adopt if wanted: on
  a resume, an item's ids carry over from the prior summary's own `ref:` fields.
  Unreachable today — 2f-i is the only id-supplying caller and never resumes.
- **correctness R1 F-11** (P4) — the touched files landed in `d381f88` today; anchors
  re-verified, no action requested.
