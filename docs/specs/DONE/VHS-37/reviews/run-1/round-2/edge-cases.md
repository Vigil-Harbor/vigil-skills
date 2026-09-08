# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Manifest disposition phrase declared one way, exampled another | CLOSED | One canonical `deferred: D-<n> (§ Deferred — follow-up required)` at spec:68, :113, :116; D13 at :46 |
| correctness | F-2 | No-re-file rule unreachable on round 1 | CLOSED | Ungated block, spec § Design 7 item 2 (:144-146), placed between agent steps 6 and 7 |
| correctness | F-3 | Nothing makes Phase 1 preserve the section on a re-run | CLOSED | Rule R4 (:100) + Scope row `:294-296` (:15) + Done-when 2 (:180). New residual filed as F-7 below |
| correctness | F-4 | Design 3 revert vs round-4 closed-issues constraint | CLOSED | D16 (:49): revert only in rounds 2–3 of this invocation |
| correctness | F-5 | Agents' closure-status enumeration left stale | CLOSED | Design 7 item 3 (:148); Scope agents row (:20); checklist row 6 (:161) |
| correctness | F-6 | Test-plan row 4 under-describes the 2b diff | CLOSED | Row 4 (:159) and Scope 2b row (:16) both name `:365-368` and `:378-383` |
| correctness | F-7 | Ceiling turned into a mandate | CLOSED (dispositioned) | § Deferred (P2+) :201 with rationale; Decision 2 restated (:32) |
| correctness | F-8 | Reject evaluated last | CLOSED | Validity is now step 0, before site-naming (:60) |
| correctness | F-9 | `sync.py push` round-trip has no checklist row | CLOSED | Row 2 now runs `push --dry-run` with the flag after the subcommand (:157) |
| correctness | F-10 | Verbatim `Suggested fix` in a spec ship-spec implements | PARTIAL | Preamble added (:83) but its presence is never verified — see F-3 below |
| correctness | F-11 | Row 3's ≥3 justification wrong | CLOSED | Row 3 parenthetical now names the three real sites (:158) |
| correctness | F-12 | "Halt and narrow the brief" has no mechanism | CLOSED | Minor-additions bullet (:51) makes it advisory; Out-of-scope 8 (:197) |
| correctness | F-13 | Two commits touched SKILL.md yesterday | CLOSED | Scope preamble names `ecdfefe` / `c97d4ad` and the re-verify duty (:11) |
| correctness | F-14 | "Left alone" omits scalability's output contract | CLOSED | `scalability:76-118` listed (:23) |
| edge-cases | F-1 | Deferral-acceptance rule unreachable (re-run r1, round-4 rows) | CLOSED | Ungated block (:144-146); D15 (:48) routes round-4 rows to the next invocation's round 1 |
| edge-cases | F-2 | Root-match suppression has no severity carve-out | CLOSED | D14 (:47) + the block's in-scope-P0 exception (:146) |
| edge-cases | F-3 | "sites that exist in the spec" makes additive fixes undeferrable | CLOSED | `(new)` marker at :61, :90, :146. New variant filed as F-4 below |
| edge-cases | F-4 | Round-4 protocol collision | PARTIAL | D16 closes the revert half; D15's "neither FROZEN nor REWRITE" leaves the section unpreserved — F-2 below |
| edge-cases | F-5 | Per-run round numbers / per-run reviews tree | CLOSED | D13 (:46), D16 "no round directory is scanned" (:49), R1 (:97) |
| edge-cases | F-6 | Nothing marks the section non-normative | PARTIAL | Preamble mandated (:83); no rule verifies it is present — F-3 below |
| edge-cases | F-7 | Design 4 example ≠ verified form | CLOSED | Example at :116 is the canonical phrase |
| edge-cases | F-8 | Render must parse rows it is told not to parse | PARTIAL | Extraction rule added (:131) but self-contradictory — F-6 below |
| edge-cases | F-9 | Heading prefix-confusable with `## Deferred (P2+)` | CLOSED (dispositioned) | § Deferred (P2+) :202 with rationale; Decision 5 and R3 require exact heading match |
| edge-cases | F-10 | 2f-i step 4 would run routing | CLOSED | Design 1 closing line (:70) + minor-additions bullet (:51) |
| edge-cases | F-11 | Test-plan gaps (em dash, row 3, round-4 text) | CLOSED | Test-plan preamble mandates Git Bash + `grep -cF` re-verify (:154); row 3 corrected |
| conventions | F-1 | No-re-file rule suppresses unauthorized findings | CLOSED | D14 (:47) with rationale, root definition, P0 exception; Decision 1 amended (:31) |
| conventions | F-2 | Round-4 rule is a silent addition outside Scope range | CLOSED | D15 (:48); Scope 2e row extended to `:426-464` (:17) |
| conventions | F-3 | Two `deferred:` strings; short one lacks a § anchor | CLOSED | Canonical phrase carries the § anchor everywhere |
| conventions | F-4 | `spec-workflow-reference.md` not reconciled | CLOSED | Scope row (:21) + checklist row 10 (:165); verified `:84`/`:88` are the right lines |
| conventions | F-5 | "all eight fields" ≠ seven labels + heading | CLOSED | D11 (:44) and the block say seven fields plus the titled heading |
| conventions | F-6 | `DEFERRED` added without amending the enumeration | CLOSED (partially applied, dispositioned) | Design 7 item 3; § Deferred (P2+) :203 |
| conventions | F-7 | "REOPEN at original severity" weakens REOPENED-is-P0 | CLOSED | Block now specifies P0 `routing violation: D-<n>`, P2 for non-routing scope errors |
| conventions | F-8 | Scope adjudication spread across four lenses | CLOSED | D17 (:50); block says the other lenses read `Scope` as opaque |
| conventions | F-9 | Finding ids in two forms in one contract | CLOSED | D13 (:46) separates manifest form from row provenance |
| conventions | F-10 | Roll-up of unflagged spec-level additions | CLOSED | Minor-additions bullet (:51) |
| conventions | F-11 | Design 3 reads round directories as current state | CLOSED | D16 (:49) + Design 3 "manifests built earlier in this invocation" (:105) |
| conventions | F-12 | Scope says one paragraph; Design 7 says two edits | CLOSED | Scope agents row now says "Three edits each" (:20) |

## Findings

### F-1: Rule R2 forbids the reads and edits the same spec mandates, and dead-ends the only repair for a routing violation
**Severity:** P0
**Where:** spec.md:98 (Design 2, R2) vs spec.md:123-131 (Design 5), spec.md:146 (Design 7 block), spec.md:59-68 (Design 1)
**Edge case:** A row is malformed — the operator's hand-edit of `Follow-up:` (D12's *designed* path) reflows a field, or a field is dropped. Also: every normal green/red exit, which renders the report.
**What happens:** R2's last sentence is absolute: "Nothing in `/spec-cycle` reads, changes, or removes a row once written." Two consequences, both in the same document:
- **Contradiction on the read.** Design 5's follow-up report is a `/spec-cycle` render that "reads each `### D-<n>:` heading and the labelled fields under it," and Design 7's block has every dispatched reviewer read every row each round. R2 says nothing in the skill reads a row. An implementer writing R2 verbatim into SKILL.md ships a rule that forbids the render the same file mandates two sections later.
- **Unrepairable P0 loop on the change.** A row that is not well-formed is, per the block, filed as a P0 `routing violation: D-<n>` — by all three or four lenses, since nothing dedups it (`total_p0p1` = 3 or 4 for one typo). 2e must then route that P0: valid, one site (the row itself), so Design 1 step 3 says **fold — edit every site on the list**. Editing the row is exactly what R2 forbids. The author must violate one of two mandatory rules; if it obeys R2 the finding cannot be closed, the reviewers re-file it every round, and the run burns to a red halt on a formatting typo, with the operator's only recovery being a hand-edit outside the skill.
**Why the spec misses it:** R2 was written to protect `Follow-up:` from being overwritten by the skill (D12's real concern) and over-generalized to the whole row and to reading. The spec never walks the routing-violation P0 back through Design 1 to see where its fix lands.
**Suggested fix:** Narrow R2 to what D12 needs and carve out the repair: "`/spec-cycle` never *overwrites* a `Follow-up:` value and never deletes a row. It reads rows in Design 5's render and the reviewers read them every round. The one edit the skill may make to an existing row is the repair of a `routing violation: D-<n>` P0 — correcting the malformed field named by the finding, leaving `Follow-up:` untouched." Add a sentence to Design 7's block that a routing violation already filed by another lens in the same round is one finding, not N.

---

### F-2: At round 4 the deferral section is classified into neither bucket, so nothing preserves it — and any REWRITE section may edit it
**Severity:** P1
**Where:** spec.md:48 (D15), spec.md:74 (Design 1 "Round 4"), against untouched `skills/spec-cycle/SKILL.md:435-444`
**Edge case:** Round 4, still red. The FROZEN/REWRITE enumeration runs over "every section of the spec … plus any spec-specific sections."
**What happens:** D15 exempts `## Deferred — follow-up required` from both classes. But in the untouched round-4 protocol, **FROZEN is the only thing that preserves a section** ("Copy the section verbatim from the current spec. Do not touch"), and the containment rule is written against FROZEN only: "Sections in REWRITE may only modify themselves — they may not silently change content in FROZEN sections." A section that is neither therefore has (a) no verbatim-copy guarantee and (b) no protection from a REWRITE section reaching into it — the containment sentence, read literally, permits it. At the one round where the author is rewriting under pressure, the section holding every deferred P0/P1 can be reworded, renumbered, or dropped with no rule broken. If it is dropped: the follow-up report at the 2f halt prints `(none)`, every proposed follow-up is silently lost, and on the next invocation the reviewers have no rows to match against, so all the deferred findings return as fresh P0/P1 — the feature silently unwinds itself at exactly the round D15 was added to cover.
**Why the spec misses it:** D15 solves the round-1 F-4 collision by removing the section from the protocol rather than by giving it a rule inside it, and assumes "not FROZEN" means "safe to append" when it actually means "not preserved."
**Suggested fix:** Classify it FROZEN with an explicit append carve-out instead of exempting it. Replace D15's clause with: "`## Deferred — follow-up required` is FROZEN: its preamble and every existing `### D-<n>` row are copied verbatim. The single permitted edit is *appending* a new row routed in this round — appending is not a FROZEN edit and needs no promotion. No REWRITE section may modify it. A finding routed to defer does not put its target section into REWRITE." Add a checklist row asserting that sentence ships.

---

### F-3: Nothing verifies the preamble is present, and it is the only thing standing between a deferral row and `/ship-spec` implementing it
**Severity:** P1
**Where:** spec.md:78-83 (Design 2 preamble), spec.md:146 (Design 7 well-formedness definition), spec.md:163 (checklist row 8), against `skills/ship-spec/SKILL.md:86` ("Read the spec and implement the changes described")
**Edge case:** The author writes the section but omits or paraphrases the preamble — an ordinary LLM-authoring miss on a "fixed line" rule stated once, 60 lines away from the row template it precedes. Also any spec whose section was created by a hand-patch between runs (the documented option-1 recovery).
**What happens:** The well-formedness check the reviewers run is defined entirely over **rows** — heading title, seven fields, two-or-more sites, `Scope`. It never looks at the preamble. So a section with a perfect row and no fence is not a routing violation, is never filed, and ships green. `/ship-spec` then reads a spec containing the most implementation-ready block in the file — a named target section, a verbatim `Suggested fix`, and an explicit list of the sites to edit — with nothing telling it to skip. The deliberately-deferred multi-site propagation lands in shipped code having never been reviewed by any round, which is strictly worse than folding it would have been. Checklist row 8 asserts only that the string exists in **SKILL.md**, i.e. that the skill *says* to write it — it cannot and does not assert that any produced spec carries it, and there is no runtime check either.
**Why the spec misses it:** Round-1 F-6/correctness-F-10 were read as "mandate the preamble," and the mandate was added to the producer side only. The consumer-side verification that already exists for rows was not extended to the fence.
**Suggested fix:** One clause in the Design 7 block, which the reviewers run every round: "A `## Deferred — follow-up required` section that does not carry the fixed preamble line immediately under its heading is a routing violation: file it as a P0 titled `routing violation: missing preamble`." Restate in Design 2 that the preamble is checked by the reviewers, and in Design 6 that this — not the absence of a downstream grep — is why the bullet is safe.

---

### F-4: A site marked `(new)` is unfalsifiable, so any finding can be made "non-trivial" and deferred
**Severity:** P2
**Where:** spec.md:61 (Design 1 step 1), spec.md:90 (Design 2 shape), spec.md:146 (Design 7 block, "dispute a site only when an **unmarked** site names a section that does not exist")
**Edge case:** A one-site in-scope P1 the author would rather not fold. It writes `**Propagation sites:** § Design 2 (new); § Test plan row (new)`.
**What happens:** The row is well-formed by definition: two sites, both `(new)`, and the block explicitly forbids disputing a `(new)` site for absence while also saying "whether a listed site was truly necessary is the author's call." The site count is brief Decision 3's *entire* mechanical test, and its stated rationale is that it is "checkable by the next round's reviewer after the fact." After the `(new)` fix it is checkable only for unmarked sites, i.e. only in the class the author does not choose. Combined with D14 suppression, the practical gate becomes P0-only: any P1 can be routed out of the count by naming two sections that do not exist yet. Brief Decision 8's rationale — "the ceiling plus the well-formedness check is the whole defense" — rests on a check that no longer bites here. Nothing corrupts; the failure is that the ticket's own value quietly erodes over runs.
**Why the spec misses it:** The `(new)` marker was added to unblock genuinely additive fixes (round-1 F-3) and the marker's effect on the *verifiability* of the count was not re-examined.
**Suggested fix:** Add one bound to the well-formedness definition: "At least one listed site must be a section that exists in the spec; a row whose sites are all `(new)` is not well-formed. A fix that lands on no existing section is a single additive edit and folds." That preserves the additive-fix case (which always also touches Decisions, Test plan, or Done-when) while restoring falsifiability.

---

### F-5: The recount does not fire for a `reworked:` disposition, or any fold whose manifest line anchors a Decision rather than the edited section
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:105 (Design 3), against `skills/spec-cycle/SKILL.md:380-383` (the 2b disposition-phrase vocabulary)
**Edge case:** A round-2 finding is dispositioned `reworked: deliberate direction change, see § Decisions D16` — the form 2b prescribes — while the actual edit landed in § Design 3. In round 3 a reviewer files a new P1 whose `Where` is § Design 3.
**What happens:** Design 3's trigger is "check its `Where` against the sections named in the `fixed:` / `reworked:` lines." The only section named on that line is § Decisions D16, so `§ Design 3` does not match and the recount silently does not run. The author folds again with no site-list redo and no `(recount: …)` marker, which is precisely today's behavior and the pathology brief Decision 4 exists to end. It is not hypothetical: three of the fifteen lines in this very run's closure manifest are `reworked:` and their anchors name Decisions, not the Design sections that were actually edited. The failure is silent — the reviewer sees no recount marker, and there is nothing to distinguish "recount ran and kept the fold" from "recount never fired."
**Why the spec misses it:** Design 3 assumes a manifest line's § anchor names the *edited* section; 2b only requires "a spec § anchor the reviewer can verify," and for a rework the natural anchor is the Decision.
**Suggested fix:** Two words in Design 3 plus one in Design 4. Design 3: "check its `Where` against **every** section named on any `fixed:` / `reworked:` line of the manifests built earlier in this invocation." Design 4 (which already edits the 2b prose): "a `fixed:` or `reworked:` phrase names every spec section the edit touched, not only the Decision that records it."

---

### F-6: The render's "never omits a row" cannot hold when rows are located by the heading it says may be unreadable
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:131 (Design 5 extraction rule)
**Edge case:** A hand-edited row whose heading is `### D-3 title` (colon dropped), `#### D-3: title` (level drifted), or `### D3: title`.
**What happens:** The rule is stated twice over: the locator is "each `### D-<n>:` heading," and the fallback is "a row whose heading is unreadable prints as `- D-?  (malformed row …)`." A row whose heading does not match the locator is never found, so the fallback can never fire and the row is silently omitted — contradicting the very next sentence, "The render never omits a row." A silently omitted row is a silently dropped follow-up, which Design 6 names as the one failure mode this report exists to prevent, and D12 makes hand-editing the designed path so malformed headings are expected rather than exotic.
**Why the spec misses it:** The fallback and the locator were written in one sentence each and never checked against each other.
**Suggested fix:** Split locator from parser: "The render treats **every `###`-or-deeper heading inside the section** as a row. A heading whose `D-<n>` id does not parse prints as `- D-?  (malformed row — see § Deferred — follow-up required)`; a missing or unreadable field prints as `?` in its column. The render never omits a heading it found and never edits one."

---

### F-7: R4 makes Phase 1 adopt whatever spec file is on disk, including a half-written or hand-broken one, with no validation
**Severity:** P2
**Where:** spec.md:100 (Design 2, R4), spec.md:15 (Scope, Phase 1 `:294-296`), against `skills/spec-cycle/SKILL.md:280-289` (Phase 0 re-run pin)
**Edge case:** A prior invocation is interrupted (Ctrl-C, context exhaustion, host cut) partway through a Phase 1 or 2e write; or the operator takes halt-menu option 1, "Patch manually and re-run `/spec-cycle`," and the manual patch truncates or mangles the file. Both are ordinary events on this skill's documented recovery path.
**What happens:** R4 converts previously-ambiguous behavior into a guarantee: "the existing file is v1 and Phase 2 starts from it." There is no atomicity discipline on the spec write (the repo has the pattern — 2f-i writes `grill.md` via `.tmp` + rename — but Phase 1/2e do not use it), and R4 adds no sanity check before adoption. So the reviewers cold-read a truncated spec, file a wall of P0s against sections that were cut off mid-write, and the run burns rounds repairing an artifact of a crash. The escape hatch exists — Phase 0's re-run pin says "delete the spec to force a clean Phase-1 re-author" — but it is stated in the *scale-lens* paragraph 130 lines away and R4 does not point at it, so neither the author nor the operator is told the recovery.
**Why the spec misses it:** R4 was derived from a single requirement (rows must survive a re-run) and pins the whole Phase 1 branch to satisfy it, without asking what else arrives at that branch.
**Suggested fix:** Two clauses on R4: "Before adopting, Phase 1 checks the existing file for its required headings (`## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Done when`, `## Out of scope`). If any is missing the file is not a usable v1 — print `existing spec is incomplete; delete docs/specs/TODO/<TICKET-ID>.spec.md to force a clean re-author, or patch it` and stop rather than reviewing a partial artifact." Optionally note that Phase 1 and 2e writes should use the same tmp-rename discipline 2f-i already uses.

---

### F-8: Round-4 dispositions have no manifest to land in, so `reject` at round 4 is recorded nowhere
**Severity:** P3
**Where:** spec.md:60 (Design 1 step 0, "disposition it `not applicable: <reason>` in the next manifest and stop"), against `skills/spec-cycle/SKILL.md:355-362` (the manifest is built in 2b when dispatching round N)
**Edge case:** Round 4 routing, which D15 explicitly enables.
**What happens:** The closure manifest for round N is built in round N's 2b from round (N−1)'s revision work. There is no round 5, so nothing built in round 4's 2e ever reaches a manifest. Defer survives, because the row is persisted in the spec; **fold** survives implicitly, because the edit is in the spec; **reject** leaves no record at all — step 0's instruction ("in the next manifest") is unexecutable, and the finding still appears verbatim in the 2f halt block's remaining-P0/P1 list with no indication the author judged it invalid. The operator reads a red list containing items the author deliberately rejected, and on the next invocation the reasoning is gone. It degrades rather than breaks, hence P3.
**Why the spec misses it:** Step 0 is written once for all rounds; D15 extends routing to round 4 without re-reading step 0's landing place.
**Suggested fix:** One sentence in Design 1's Round 4 paragraph: "At round 4 there is no next manifest. A rejection is recorded in the 2f halt block by suffixing the finding's title ` — rejected: <reason>`, and a fold by ` — folded § <section>`, so the operator sees the author's disposition alongside the remaining red list."

---

### F-9: Rows accumulate without bound or GC across invocations, and a partial `sync.py install` makes the whole feature a silent no-op
**Severity:** P3
**Where:** spec.md:51 (minor additions, "the skill never garbage-collects a row"), spec.md:97 (R1), spec.md:146 (Design 7 block), spec.md:20 (Scope, five files edited together)
**Edge case:** (a) A ticket that goes through several `/spec-cycle` invocations; (b) an operator who pulls a merged PR and does not run `python sync.py install`, or installs mid-flight.
**What happens:** Two persistence-checklist items are unhandled.
- **Size bound / accumulation.** Nothing caps or ages the section (brief Decision 8, authorized), nothing removes a row whose ticket the operator filed, and R5 keeps a row even after a later fold resolves it. Every dispatched reviewer must read and root-match against every row, every round, forever. The suppression surface therefore grows monotonically across the ticket's life, and each added row raises the chance of a false root match retiring a live P1. Acknowledged for the P0 class (D14's exception), unbounded for P1.
- **Version skew.** The behavior lives in five files that must move together (SKILL.md plus four agents), and this repo's recorded operational hazard is exactly that a merged change is inert until `sync.py install` runs. New skill + old agents = specs carry rows that no reviewer reads, so every deferral is re-filed and the operator sees a red run with no explanation anywhere. Nothing in the section marks a version, and Design 6's failure-mode bullet does not cover it.
**Why the spec misses it:** Decision 8 fences numeric caps, which the spec correctly honors; neither the growth-over-time consequence nor the split-install consequence is a numeric cap.
**Suggested fix:** (a) Add to R5 or the render: a row whose `Follow-up:` is no longer `unfiled` prints in the report under a `filed` sub-list and may be dropped by the operator; state that the operator is the GC. (b) Add one line to Design 6's failure-mode bullet: "The section is inert unless the four reviewer agents carry the Deferred-findings block. If a spec shows rows and the reviewers still re-file them, the agents are out of date — run `python sync.py install`."

---

### F-10: Two render columns are not row fields, and a row resolved by a later fold still prints as an open follow-up
**Severity:** P3
**Where:** spec.md:126-131 (Design 5), spec.md:86 (row shape), spec.md:101 (R5)
**Edge case:** Any render.
**What happens:** The report's columns are `D-n · finding · severity · scope · title · Follow-up`, but severity is a parenthetical *inside* the `Finding:` field (`<lens>/R<n>/F-<k> (P0 | P1)`) and scope is the leading token of a `Scope:` field whose remainder is a citation. The extraction rule speaks only of "labelled fields," so both columns require an unstated sub-parse, and the `?` fallback has no defined trigger for them. Separately, R5 keeps a row whose root a later fold resolved — including the in-scope-P0 case D14 mandates filing and Design 1 mandates folding — so the report reliably presents already-fixed defects to the operator as follow-ups to file. Both are cosmetic-to-mildly-wasteful, not dangerous.
**Why the spec misses it:** Design 5's example was written before the row shape folded severity into `Finding:` (D11).
**Suggested fix:** Say in Design 5 that severity is taken from the parenthetical in `Finding:` and scope from the token before the em dash in `Scope:`, each `?` when unparseable. In R5, have the render suffix such a row ` — resolved by a later fold; drop if no ticket is wanted`.

---

### F-11: D15 anchors the round-4 edit at `:438-441`; Design 1 and the Scope table anchor the same sentence at `:436-441`
**Severity:** P4
**Where:** spec.md:48 (D15) vs spec.md:17 (Scope 2e row) and spec.md:74 (Design 1 Round 4)
**Edge case:** The implementer follows D15 rather than the Scope table, or checklist row 4 asserts hunk regions against one of the two.
**What happens:** Both anchors sit inside the declared 2e range, so nothing breaks — but the spec names two different edit sites for one sentence, and the checklist's "assert hunk regions" instruction has no single region to assert. Verified against `main`: `:435-437` is the enumerate-every-section sentence, `:438-441` the FROZEN/REWRITE bullet pair.
**Suggested fix:** Pick one — `:436-441` reads correctly as "the FROZEN/REWRITE enumeration" — and make D15 match.

## Summary
P0: 1 | P1: 2 | P2: 4 | P3: 3 | P4: 1

STATUS: RED P0=1 P1=2 P2=4 P3=3 P4=1
