# Edge-Cases Review — round 2

Grounding complete. I read the spec and brief fresh, `CLAUDE.md` + the global conventions, all four target files at `f4d9290` (HEAD), all three round-1 reviews, and the attempt-1 Design 3 region. Ticket lookup: I worked from the brief (its `## Origin`/`## Done when` already reproduce VHS-36's Plane body verbatim, per round-1 correctness's tag-exact hit).

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | row 3 `###` grep asserts 0 | CLOSED | row 3 now asserts diff-based `grep -c '^+#'` → 0 **and** `grep -c '^###'` → 3 unchanged (spec :547–549) |
| correctness | F-2 | "fourth bullet" should be fifth | CLOSED | Design 10: "A **fifth** is inserted after `:154`, third in reading order" (:440) |
| correctness | F-3 | bold = ship vs. marker, unstated | CLOSED | new § Design preamble "**Reading the blockquotes.**" (:176–180) splits Designs 1–6/8/9/11/12 from 7/10/13 |
| correctness | F-4 | Design 6 vs. unedited `:76` | CLOSED | shipped text names it: "The dispatch rule above says a question downstream of a fact waits for it; that governs a fact still coming" (:343–344) |
| correctness | F-5 | row 11 mis-attributes VHS-33 row 11 | CLOSED | row 11 now scopes the re-assertion to `:88` + the `fence-empty` grep, narrows the hunk clause, claims `:139`/`:141`/`:142` as its own (:617–620) |
| correctness | F-6 | row 17 "seven quotes" | CLOSED | row 17 is a ten-item numbered list (:647–664) |
| correctness | F-7 | `:18` outside every fence | CLOSED | row 9 "no hunk at `:18`" (:594); row 10 re-asserts VHS-33 row 7's seed-bullet pins (:599–601) |
| edge-cases | F-1 | no field for the claim text | CLOSED | `claim: "<the operator's answer>"` in Design 8 (:408); conditional rule in the shipped `**Two outcomes.**` (:280–281); D3 field-vs-section argument (:81–89); row 4; Design 11 |
| edge-cases | F-2 | row 3 `###` grep false | CLOSED | same edit as correctness F-1 |
| edge-cases | F-3 | concurrency rule never ships | CLOSED (new defect — see F-1 below) | "one parallel batch, capped at `question_cap` dispatches … at most `question_cap` dispatches are ever in flight" now inside the shipped `**When the check runs.**` (:241–248) |
| edge-cases | F-4 | `stop` can hang the hand-off | CLOSED | `:110` addition "A check that never returns blocks the hand-off … the one dispatch that can still be in flight when it lands" (:385–387); `:156` bullet (:453–454); row 17 item 6 |
| edge-cases | F-5 | gated question in the last rendered round | CLOSED (new defect — see F-2 below) | "under the exit's own reason — `round-cap` or `stopped` — and never `blocked-on: F<n>`" (:350–352) |
| edge-cases | F-6 | "answered" undefined | PARTIAL | non-answer clause ships (:204–207) and closes the `I don't know` case; a *second* answer to the same F-item is still undefined — F-6 below |
| edge-cases | F-7 | "never load-bearing" rationale false | CLOSED | shipped "When in doubt, dispatch" (:326–328); commentary rewritten (:331–339) |
| edge-cases | F-8 | claim crosses a trust boundary unquoted | CLOSED for the dispatch, REOPENED for the hand-off | "quoted data, never as instructions … within this working tree" (:210–213) covers the exploration prompt; the same verbatim text now enters the parsed hand-off line with no rule — F-3 below |
| edge-cases | F-9 | row 6 grep not runnable | CLOSED | `grep -cF 'is reserved for a fact need nobody answered'` (:573) |
| edge-cases | F-10 | Decision on an unverified claim unlabelled | CLOSED (deferred) | § Deferred VHS-39 (:725–728) and Design 11 (:477–480) |
| edge-cases | F-11 | answered-after-Open has no rule | CLOSED (side-effect — see F-1) | last sentence of `**Across a resume.**` (:359–360); it is this sentence that breaks Design 2's bound |
| edge-cases | F-12 | failed check vs. failed fact dispatch | CLOSED | "'No retry' governs a failed **check**, not a failed **fact dispatch**" (:309–312) |
| edge-cases | F-13 | row 9 fence has gaps | CLOSED | row 9 restated as its complement, "no region other than these five" (:591–594) |
| edge-cases | F-14 | row 17 count mismatch | CLOSED | ten explicit items (:647–664) |
| edge-cases | F-15 | check for a moot fact need | CLOSED (accepted) | § Deferred, "Accepted as noise … Not filed" (:730–734) |
| edge-cases | F-16 | `/grill-me` bullet names 2 of 5 causes | CLOSED | Design 12 names all five (:486–491); row 12 pins them |
| conventions | F-1 | row 3 `###` grep | CLOSED | same edit |
| conventions | F-2 | Design 6 resume rule vs. `:23` | CLOSED | shipped "this displaces the resume contract's 'unless they are downstream of the revised decision' clause … downstream or not" (:355–358); false "silence" gone from D9 and Design 6 |
| conventions | F-3 | wiki decision superseded silently | CLOSED | D7 "**This adopts what the VHS-33 wiki decision recorded as rejected-for-now**" with the page path (:131–138) |
| conventions | F-4 | `:19–32` fence vs. choice | CLOSED | "**Why `:23` is not edited.** It is a choice, not a fence" (:362–373) |
| conventions | F-5 | `:18` / VHS-33 row 7 | CLOSED | rows 9 and 10 (see correctness F-7) |
| conventions | F-6 | deferred size bound names no ticket | CLOSED | § Deferred, VHS-38, filed 2026-09-07 (:718–723) |
| conventions | F-7 | Design 3's bullet list | CLOSED | "This ships as one paragraph, not a bold lead plus a bullet list" (:287–289); row 3 asserts `grep -c '^- '` → 0 |
| conventions | F-8 | row 6 backtick | CLOSED | same as edge-cases F-9 |
| conventions | F-9 | `:143` comma/semicolon | CLOSED | Design 9 is semicolon-separated throughout (:431–434) |
| scalability | — | — | N/A | `scale_lens: off`; no `scalability.md` in round-1 |

Round-1 P0/P1 are all closed. Two of the folds, however, interact with each other and with the new `claim:` field in ways the spec does not cover — that is what follows.

## Findings

### F-1: The check batch's shipped bound is contradicted by the shipped resume/Open-item rule, and the cap has no overflow rule
**Severity:** P0
**Where:** spec § Design 2, shipped blockquote (spec.md:246–248) vs. § Design 6, shipped blockquote (spec.md:359–360)
**Edge case:** The operator answers an `F<n>` that is already an **Open** item — reachable without a resume via `skills/grilling/SKILL.md:90` ("A fact request the operator leaves unanswered twice becomes an Open item"), and explicitly legalized by this spec.
**What happens:** Two shipped sentences in the same section disagree about what bounds the check batch.

- Design 2 ships: *"the checks fired on one round's answers are bounded by the fact requests **that round rendered**, which the same cap already bounds."*
- Design 6 ships: *"A fact request the operator answers **after it became an Open item** is a claim like any other, and gets its one check."*

An Open F-item is not a fact request that round rendered — Open items are never re-rendered (`:65`, and the resume paragraph itself says they carry over as Open, un-redispatched). Open F-items accumulate to `(round_cap + 1) × question_cap` by `:137` (28 at the defaults), while a round renders at most `question_cap`. So the count of checks a round can fire is bounded by 28, not by 7, and the shipped justification for "the same cap already bounds it" is false.

The rule the justification supports — *"one parallel batch, capped at `question_cap` dispatches"* — then has a branch with no stated behavior. An implementer facing 9 answered claims and a cap of 7 has two readings: (a) fire all 9, breaking the concurrency bound the paragraph just introduced and giving the hand-off 9 independent chances to hang (F-4's accepted risk, multiplied); or (b) truncate at 7 and silently leave 2 claims unchecked — and "no check was dispatched because the batch was full" is not among Design 3's five enumerated not-confirmed causes, so the two dropped claims have no stated disposition. Attempt 1's overflow-ordering rule was deleted on exactly this reasoning (spec :253–258, "§ Bounds' three-key ordering never has to rank a thing that is not a rendered item"), and § Bounds `:87` is pinned byte-identical, so no existing rule ranks them either.
**Why the spec misses it:** The bound sentence is the round-1 edge-cases F-3 fold (which reasoned only about the round's own rendered `ℹ️` requests); the Open-item sentence is the round-1 F-11 fold, added to a different Design. Neither fold re-read the other. Design 2's own commentary ("The ordering rule at `:87` is not extended", :253) rests entirely on the bound being true.
**Suggested fix:** Pick one and make the shipped text say it. Simplest that preserves both folds: change Design 2's clause to *"…the checks fired on one round's answers are bounded by the `F<n>` items outstanding, and the batch is capped at `question_cap` dispatches; where more claims were answered than the cap allows, the remainder are checked in the next batch, and any still unchecked when the interview ends are Open with `fact not established (operator claim, unverified)`."* Then add "an answered claim the cap left unchecked" to Design 3's list of not-confirmed causes, and add "what happens when more claims are answered than the batch cap allows" to row 17.

### F-2: The gated question is rendered with an "unverified status" note even when the check **confirmed** the claim
**Severity:** P1
**Where:** spec § Design 6, shipped blockquote (spec.md:345–349); contradicts § Design 3 shipped text (spec.md:274–276)
**Edge case:** The check confirms — the modal success path — and a question was waiting on that fact.
**What happens:** The shipped sentence reads: *"Once a claim's check has resolved, the question waiting on it enters the next round's frontier **whether the claim was confirmed or not**, and is rendered with a one-line note giving the claim's text **and its unverified status**."* The concessive clause covers both branches, so the trailing "and is rendered with a one-line note … and its unverified status" attaches to both. On the confirmed branch that is false and self-contradicting: Design 3 ships "**Confirmed**: the fact goes to `### Facts established`, sourced by the `path:line` the *exploration* found". The operator is then shown a decision annotated "unverified" about a fact the primitive has just established with a path, and the interview's own § Facts established says the opposite. The stated purpose of the note — "so the operator decides on the same information the hand-off will carry" — is defeated in exactly the case where the hand-off carries an established fact.
**Why the spec misses it:** The paragraph is the round-1 F-5 fold, written for the not-confirmed case (D10's whole rationale is "otherwise D3's accepted degradation would stall the interview"); "whether the claim was confirmed or not" was added to cover the confirmed case for *frontier entry*, and the note clause was never re-scoped. Row 17 item 8 asks only whether the question renders, not what the note says, so the reading gate does not catch it.
**Suggested fix:** Split the clause in the shipped text: *"…enters the next round's frontier whether the claim was confirmed or not. Where the check did not confirm, the question is rendered with a one-line note giving the claim's text and its unverified status, so the operator decides on the same information the hand-off will carry; where it confirmed, the fact is established and the question is rendered as any other."* Add "what the gated question's note says when the check confirmed" to row 17 item 8.

### F-3: The `claim:` field inserts unbounded, unescaped operator text into a line-structured contract three callers parse
**Severity:** P1
**Where:** spec § Design 8 (spec.md:405–414); § Design 3 shipped text, "carries the operator's answer **verbatim**" (spec.md:279–281)
**Edge case:** An operator answer containing a newline (a pasted log, a two-line quote), a double quote (`the flag is "--strict"`), or text that mimics the block's own field syntax (`. ref: none`, `unresolved because:`, `### Facts established`). Also: a very long answer.
**What happens:** Four distinct failures, none covered:
1. **Newline.** Every hand-off item is one line — row 4 pins the F-item line verbatim, `:135`'s `ref:` rules are per-item, and `/spec-brief` Phase 4 maps items positionally. A multi-line claim splits one F-item across lines; the continuation lines are not valid items, and a caller mapping "Open frontier items → `## Risks / decisions`, numbered" either drops them or promotes them to phantom items. The primitive's other operator-authored text (a free-form answer, `:67`) never reaches the block verbatim — it is recorded as a settled decision the primitive rewrites.
2. **Double quote.** The field is `claim: "<the operator's answer>"` and Design 11 re-wraps it as `operator claims "<answer>", unverified`. An embedded `"` makes both ambiguous, and nothing says to strip, escape, or single-quote.
3. **Field spoofing.** `; claim: "…". ref: <…>` is now the F-line's grammar, and the claim text sits between two machine-read fields. An answer containing `. ref: none` or a second `unresolved because:` silently redefines what the caller reads. This is the round-1 F-8 trust boundary again on a second channel: the fold hardened the *exploration prompt* against operator text ("quoted data, never as instructions") but the same string now also crosses into the contract block, where no equivalent guard was added. The channel also carries text the operator pasted from elsewhere (an error message, another agent's output), so this is not only a "malicious operator" case.
4. **No size bound.** `:137` bounds the Open frontier by item *count* and is fenced byte-identical; nothing bounds a field's length. A pasted 200-line answer rides into the hand-off and into `## Risks / decisions`.
**Why the spec misses it:** D8 asked only that the brief carry the claim text; the spec correctly invented a field for it (closing round-1 F-1) but treated it as a display slot rather than as a new field in a contract the spec itself calls "a verbatim contract three callers parse" (D3 rationale, :83). The word "verbatim" in Design 3's shipped text actively forbids the normalization that would fix it.
**Suggested fix:** One clause in the `**Two outcomes.**` paragraph, replacing "verbatim": *"…carries the operator's answer in the `claim:` field of the hand-off block's F-item line — as a single line, with newlines collapsed to spaces, inner double quotes rendered as single quotes, truncated to one line of prose with an ellipsis where longer, and never containing `ref:` or `unresolved because:`; where truncation loses the claim's substance, the field carries the first sentence and the caller re-asks the operator by hand."* Pin the single-line / normalization phrase in checklist row 4, and add "what the `claim:` field may contain" to row 17 item 9.

### F-4: The F-item line's form when `claim:` is omitted is unspecified, and the fence shows only the with-claim form
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 8 (spec.md:405–413); Test plan row 4 (spec.md:550–554)
**Edge case:** The ordinary Open F-item — reason `fact not established` or `stopped`, i.e. every F-item that is not an unverified claim.
**What happens:** The fenced template — the thing the block is rendered from "exactly" (`:118`) — now reads `…| stopped>; claim: "<the operator's answer>". ref: <…>`, and Design 8 says the field "is omitted otherwise" without saying what the line then looks like. Three renderings follow from "omit the field": `…| stopped> ref: <…>` (no terminator), `…| stopped>; ref: <…>` (stray semicolon), or the pre-change `…| stopped>. ref: <…>` (correct). The spec treats this punctuation as gate-relevant everywhere else — row 4 re-asserts that the rolled-up line "ends `)**. ref: <…>`" — so the omitted form is the one F-line variant nothing pins. Downstream, `/spec-brief` Design 11 also has no rule for the malformed case it can now receive (qualifier present, `claim:` absent).
**Why the spec misses it:** Design 8 deliberately keeps the conditional-render rule *outside* the fence ("it is not restated inside the fence", :413) so the fence stays one line. That is a reasonable choice, but the rule as written states only presence/absence, not the resulting punctuation.
**Suggested fix:** Extend Design 8's sentence: *"…and is omitted otherwise, the line then reading `…| stopped>. ref: <…>` exactly as before this change."* Add to row 4: "an F-item under `fact not established` or `stopped` renders `>. ref:` with no `claim:` field." Add one clause to Design 11: "an item carrying the qualifier with no `claim:` field is written with the plain `— not established` form."

### F-5: A carried-over Open claim loses its `claim:` text across a resume
**Severity:** P2
**Where:** spec § Design 6, `**Across a resume.**` (spec.md:355–360); § Design 11 (spec.md:458–465)
**Edge case:** `/spec-brief`'s revise path — an Open F-item carrying the qualifier existed in `prior_summary`, and the resumed run renders a fresh hand-off.
**What happens:** `prior_summary` is the primitive's only persisted state (`:80`, `:21`), and the resumed run rebuilds the tree from it and re-renders the whole block at the end. The shipped rule says the item "carries over as Open and is not re-dispatched, qualifier or not" — it says nothing about the item's *fields*. If the rebuild re-emits the reason value but not the `claim:` text (nothing tells it to, and the text is not part of the item's identity the way `F<n>` and `ref:` are), the final hand-off — the one `/spec-brief` maps — carries the qualifier with no answer, which is precisely the D8-unimplementable state round-1 F-1 was raised to prevent, restored one path over. The claim text is sitting in the summary being rebuilt from, so this is loss by omission, not by unavailability.
**Why the spec misses it:** The resume paragraph was written to settle *re-dispatch*, the one thing D9 asked about; the `claim:` field arrived in a different Design, after D9 was settled.
**Suggested fix:** One clause in the shipped `**Across a resume.**` paragraph: *"…and carries its `claim:` text with it, so the resumed hand-off is not poorer than the one it was rebuilt from."* Assert it in row 5 alongside the other displacement phrases.

### F-6: A second answer to the same `F<n>` has no rule — "its one check" reads as silently dropping the operator's correction
**Severity:** P2
**Where:** spec § Design 6 (spec.md:359–360); § Design 4, `**No retry, and no re-ask.**` (spec.md:304–313); § Design 1 (spec.md:202–214)
**Edge case:** The operator answers `F2 <claim>` in round 2, the check does not confirm, and in round 3 the operator types `F2 <corrected claim>` — the natural response to seeing the fact land Open, and permitted by `:53`, which restricts no `F<n>` to the round that rendered it.
**What happens:** Three shipped sentences point in different directions. Design 1 is unconditional ("When the operator answers a fact request … the answer is a **claim**" → dispatch a check). Design 6 says an answer to an already-Open item "gets **its one check**" — singular, which reads as *the item has had its check; this answer gets none*. Design 4 forbids retry but scopes the ban to a failed check, not to a new claim. So an implementer either (a) silently discards the operator's correction — a fact that could now be established stays Open and the *old* claim text reaches the brief, or (b) fires a second check and must decide whether `claim:` holds the old text, the new text, or both. The failure in (a) is silent: nothing tells the operator their correction was ignored, and the hand-off shows a claim they have already retracted.
**Why the spec misses it:** Round-1 F-6 defined "answered" for the *first* answer (closing the `I don't know` case) and F-11 legalized an answer arriving late; neither asked what a *replacement* answer does. The precedence sentence ("a fact need the operator answered is never `stopped`") is indifferent to which answer.
**Suggested fix:** One clause, wherever the claim rule is stated: *"A later answer to the same `F<n>` replaces the claim: the item's `claim:` field takes the new text, and the new claim gets its own check. That is not a retry — 'no retry' governs a check that failed on the same claim."* Add it to row 17 item 2 ("what counts as an operator answer, and what does not") or as a new item.

### F-7: Row 17 item 3 cannot be answered by one sentence without arithmetic, which the row itself forbids
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 17 preamble and item 3 (spec.md:647–654); § Design 2 shipped text (spec.md:241–248)
**Edge case:** Running the gate. `## Test command` is `N/A`, so this checklist *is* the `/ship-spec` gate, and Done-when bullet 1 maps row 17.
**What happens:** The row's preamble states "an answer that requires combining two sentences, **or any inference**, fails the row." Item 3 asks "How many checks run at once, **and how many dispatches may a round make?**" The only shipped sentence that speaks to it says "at most `question_cap` dispatches are ever in flight, though a round may now make two batches rather than one." The first half answers the first question directly; the second half yields the round's dispatch budget only by multiplying two batches by the per-batch cap — the spec's own commentary does that arithmetic for the reader ("a round may now make up to `2 × question_cap` dispatches in total", :262) and then explicitly says it wants that not derived: "so a reader does not have to derive it". The commentary does not ship. A strict reviewer fails a faithful implementation; a lenient one passes it, so the row's outcome depends on the reviewer, which is what a verbatim reading gate exists to remove.
**Why the spec misses it:** The concurrency phrase and the ten-item reading gate came from two different round-1 folds (F-3 and F-14), and the gate item asks for the one quantity the shipped sentence states implicitly.
**Suggested fix:** Either put the total in the shipped sentence — "…though a round may now make two batches, up to `2 × question_cap` dispatches in all" (and add that phrase to row 3's verbatim list) — or split row 17 item 3 into "how many checks run at once" and drop the second half.

## Summary
P0: 1 | P1: 2 | P2: 4 | P3: 0 | P4: 0

STATUS: RED P0=1 P1=2 P2=4 P3=0 P4=0
