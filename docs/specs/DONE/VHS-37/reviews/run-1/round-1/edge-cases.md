# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: The deferral-acceptance rule is unreachable on the two paths that need it most (re-run round 1, and round-4 rows)
**Severity:** P0
**Where:** spec.md:129-131 (Design 7), spec.md:81 (Design 2, "carried unchanged across rounds and re-runs"), spec.md:61 (Design 1, "also applies at round 4")
**Edge case:** `/spec-cycle` re-invoked on a spec that already carries `## Deferred — follow-up required` rows; and a row written during round 4.
**What happens:** Design 7 inserts the whole deferral contract — including the clause "the same holds for any new P0/P1 candidate whose root is already a row in that section, **in any round**" — into reviewer **step 7**, which is gated `If round_number ≥ 2` in all four agents (`agents/spec-reviewer-correctness.md:30`, `edge-cases.md:30`, `conventions.md:35`, `scalability.md:30`). Two consequences:
- `skills/spec-cycle/SKILL.md:319` is `For each round 1..4` — a re-run always starts at round 1 with no `closure_manifest`, so step 7 does not execute. Every carried row is invisible to the reviewers and every deferred finding is re-filed as a fresh P0/P1. The documented recovery path from the halt menu is literally `1. Patch manually and re-run /spec-cycle` (`SKILL.md:481`), so this is the *normal* path after a red run, and on it the feature is a no-op. The gate does not fall; the operator sees the same red list the deferral was supposed to retire.
- A row written in round 4's rewrite (Design 1 explicitly permits this) is verified by nobody: there is no round 5, and the re-run's round 1 skips step 7. Design 6's claim that a row is "checked for well-formedness by the reviewers on the round after it is written" is false for round-4 rows, and the routing-violation REOPEN — the only defense against deferring an in-scope P0 — is unavailable at exactly the round where the author is most pressured to shorten the red list.

**Why the spec misses it:** Design 7 specifies placement ("Step 7 gains one paragraph after the 'REOPENED items are P0' sentence") without noticing that step 7 is conditional. The paragraph's own words ("in any round") contradict its container. The spec never asks what happens at round 1 of any invocation, and Design 2:81 assumes cross-run carriage works.

**Suggested fix:** Split Design 7's paragraph in two. The *closure-verification* half (a `deferred: D-<n>` disposition is satisfied when …, mark `DEFERRED` in the closure table) stays in step 7. The *suppression + well-formedness* half becomes an unconditional grounding step in all four agents — e.g. a new step run at every round: "Read `## Deferred — follow-up required` in the spec. For every row, check the eight fields, the site count, and the scope classification; do not file any P0/P1 whose root is already a well-formed row; file a routing violation for any row that fails." Then state in Design 1/Design 2 that a round-4 row is verified on the next invocation's round 1 by that step.

---

### F-2: Root-match suppression has no severity carve-out, so an in-scope P0 variant of a deferred row is never filed — the Decision 2 ceiling is bypassed
**Severity:** P1
**Where:** spec.md:131 (Design 7), spec.md:53-58 (Design 1 step 3), brief Decision 2
**Edge case:** A round-2 finding is deferred as an out-of-scope P1 with a broadly worded title. In round 3 a reviewer discovers a sharper, **in-scope P0** variant of the same root (the classic escalation: "this is not just awkward, the spec is now internally inconsistent here").
**What happens:** Design 7 instructs the reviewer: "do not re-file it or any variant of the same root; the same holds for any new P0/P1 candidate whose root is already a row in that section, in any round." No severity or scope qualifier. The reviewer suppresses the P0. `total_p0p1` never sees it, the gate goes green, Phase 3 prints `=== SPEC READY ===`, and `/ship-spec` implements a spec that Decision 2 says can never ship as a known issue. The suppression list also has no expiry and no cap (Decision 8), and "root" is an undefined fuzzy match key, so the list grows monotonically and its blast radius grows with it.

A related instance: the same root filed by two lenses can be deferred under one lens and folded under the other; the suppression clause then silences the lens that would have caught the fold's propagation miss.

**Why the spec misses it:** Design 1's ceiling is written as an *author-side* routing rule only. Design 7 gives the reviewer an unconditional suppression rule and never re-states the ceiling on the reviewer side, so the two halves of Decision 2 do not meet.

**Suggested fix:** Add the ceiling to Design 7's paragraph: "Suppression is bounded by the ceiling. A new candidate whose root matches a row but which is **in-scope and P0** is filed normally at P0 with the row cited as context — an in-scope P0 cannot be carried as a known issue, whatever the row says. A row whose severity or scope is contradicted by such a candidate is also a routing violation." State the same bound in Design 1 step 4 so the author is not surprised.

---

### F-3: "Propagation sites … that exist in the spec" makes every additive fix undeferrable — defer/REOPEN oscillation
**Severity:** P1
**Where:** spec.md:131 (Design 7, "names two or more sections **that exist in the spec**" and "dispute a site only when the named section does not exist"), spec.md:51 (Design 1 step 1)
**Edge case:** A finding whose fix is additive — "the spec needs a rollback section, a Decision recording it, and a checklist row." Two or more sites, out-of-scope, so Design 1 routes it to **defer**. The `Propagation sites` field must name the sites, and one or more of them are sections the fix *would create* and that do not exist yet.
**What happens:** The reviewer's stricter check fires twice: fewer than two *existing* sections named → "routing violation — REOPEN at the original severity"; and any named-but-absent section is explicitly disputable. The correctly-deferred finding is re-filed at P0/P1 next round. The author re-routes it to defer, the next reviewer REOPENs it again. The loop oscillates until round 4 and halts red — precisely the pathology the brief's Problem section describes and this ticket exists to end. The additive class is not exotic; it is the dominant shape of a review finding against a prose spec.

Symmetrically on the author side, Design 1 step 1's site list enumerates *existing* landing places ("the Design sub-section, the authoritative contract block…"), so an additive fix counts as one site or zero and routes to **fold** even when it will in fact touch three places after the first edit — the undercount the whole test is meant to prevent.

**Why the spec misses it:** Both rules were written for the modify-in-place case and never tested against "the fix adds something new."
**Suggested fix:** Allow a site to be marked as to-be-created. In Design 2's row shape: `**Propagation sites:** § <a>; § <b> (new); …`. In Design 7: "a site marked `(new)` is a section the fix would create; it counts toward the two-site minimum and is never disputed for absence. Only an unmarked site naming a nonexistent section is a defect." In Design 1 step 1, say explicitly that sites the fix must *create* count.

---

### F-4: Round-4 protocol collision — the recount's revert violates the closed-issues regression constraint, and writing a row edits a FROZEN section
**Severity:** P1
**Where:** spec.md:61 ("also applies at round 4"), spec.md:85-91 (Design 3), against untouched `skills/spec-cycle/SKILL.md:436-458`
**Edge case:** Round 4, still red. Routing runs before the FROZEN/REWRITE manifest, per Design 1.
**What happens:** Two independent contradictions with rules the spec declares untouched:
1. **Revert vs. regression constraint.** `SKILL.md:446-458` builds a closed-issues manifest of every finding CLOSED in rounds 1–3 and states: "Every entry is a regression constraint: the rewritten spec must preserve the fix that closed it." Design 3 orders the author to "**revert the original fold** (remove the edit from every site it touched)" for exactly such a fix. The author faces two mandatory, opposed instructions at round 4 and resolves them arbitrarily; whichever way, one recorded rule is silently violated and the closure evidence of every other finding that pointed at the reverted text goes dangling. The same revert also collides with 2e's untouched bullet "Do not delete history of what changed" (`SKILL.md:433`), which the spec's Scope table lists as unchanged.
2. **Row vs. FROZEN.** `SKILL.md:437-445` requires enumerating "every section of the spec … plus any spec-specific sections" and classifying each FROZEN ("Copy the section verbatim. Do not touch") or REWRITE. `## Deferred — follow-up required` has no unresolved P0/P1 of its own, so it classifies FROZEN — yet round-4 routing must append a row to it. Design 1's only guidance is that "a deferred finding does not put its **section** into REWRITE," which addresses the finding's target section, not the deferral section itself. The author must either violate the FROZEN rule or cannot record a round-4 deferral at all.

Design 3 is additionally undefined when a later round's fold overlapped the text being reverted: "remove the edit from every site it touched" has no meaning once the text has been re-edited.

**Why the spec misses it:** Design 1 asserts round-4 compatibility in a single sentence and never walks the round-4 block's three rules (FROZEN/REWRITE, promotion, closed-issues constraints) against routing.
**Suggested fix:** Add a round-4 paragraph to Design 1: (a) `## Deferred — follow-up required` is exempt from the FROZEN/REWRITE enumeration — appending a row is never a FROZEN edit and never requires promotion; (b) a revert ordered by Design 3 at round 4 requires promoting every touched section to REWRITE **and** removing the reverted fix's entry from the closed-issues manifest, with the deferral row recorded as its replacement constraint; (c) if the fold to be reverted has since been overlapped by a later edit, revert is not available — fold with the corrected site list and record the recount.

---

### F-5: The design assumes per-run round numbers and a per-run reviews tree; both are shared across invocations
**Severity:** P1
**Where:** spec.md:42 (D13), spec.md:87 (Design 3, "the Evidence column of the persisted closure tables under `<TICKET-ID>.reviews/round-*/`"), spec.md:80-81 (Design 2)
**Edge case:** Any second invocation of `/spec-cycle` on the same ticket — the documented halt-menu recovery.
**What happens:** `SKILL.md:319` restarts the counter at 1 and 2c overwrites `round-<N>/` in place, so the reviews tree is a union of eras:
- **Colliding ids (silent drop of a live finding).** D13 chose `<lens>/R<n>/F-<k>` because "`F-3` alone is ambiguous across rounds" — but the same argument defeats the fix across *runs*. Run 1's `edge-cases/R2/F-4` and run 2's `edge-cases/R2/F-4` are different findings with identical ids, while rows deliberately outlive runs (Design 2:81). A reviewer verifying a `deferred: D-2` disposition, or matching a new candidate against a row, can bind to the wrong row, mark a live P1 `DEFERRED`, and the gate loses it with no trace.
- **Stale recount source (spurious revert).** Design 3's fallback scans `round-*/` unbounded. If run 2 goes green at round 2, `round-3/` and `round-4/` still hold run 1's closure tables, whose Evidence points at folds that this run's spec never made or has since reworked. A `Where` that matches stale evidence triggers a false recount and, under the two-or-more branch, a **revert of an edit that is currently load-bearing**. The skill already carries a guard for exactly this residue class (the stale-`scalability.md` rule, `SKILL.md:722-728`), so the hazard is known and this new read is unguarded.

**Why the spec misses it:** D13 reasons about rounds and stops there; Design 3 names a glob without asking what else is in the directory.
**Suggested fix:** (a) Make the row id invocation-stable — either qualify it with the run (`<lens>/<run-stamp>/R<n>/F-<k>`, stamp recorded once in Phase 0) or drop the round qualifier in favor of the row's own `D-<n>` as the sole cross-run key, with `Finding` kept as descriptive provenance only, and instruct the reviewer to match on `D-<n>` plus title, never on the round-qualified id alone. (b) Restrict Design 3's fallback to round directories written by **this** invocation, and say so: "closure tables from rounds this invocation has completed; a `round-<k>/` directory for a round this run has not reached is residue from a prior invocation and is ignored." (c) Add a rule for `D-<n>` assignment on a spec that already has rows: scan the section and continue from the highest existing number.

---

### F-6: Nothing marks the section non-normative, and `/ship-spec` reads the whole spec and implements it
**Severity:** P1
**Where:** spec.md:68-76 (Design 2 row shape), spec.md:122 (Design 6, "Nothing downstream reads it"), against `skills/ship-spec/SKILL.md:86` ("Read the spec and implement the changes described")
**Edge case:** The green path. The spec ships with rows carrying `**Suggested fix (verbatim):** <the reviewer's Suggested fix, unedited>` and `**Propagation sites:** § a; § b`.
**What happens:** `/ship-spec` has no section allowlist — it reads the spec end to end and implements what it finds. The deferral row is the most implementation-ready block in the file: a named target, a verbatim instruction, and a list of the exact sites to edit. The realistic outcome is that the implementer applies it, so the multi-site propagation the deferral avoided lands in shipped code without ever being reviewed — a strictly worse result than folding it, because no review round ever saw it. Design 6 asserts safety on the wrong axis: it is true that no *skill* greps the section, and irrelevant, because the consumer is an LLM reading the spec as instructions. The existing `## Deferred (P2+)` does not have this problem — it holds "one-line acknowledgments," not executable fixes.
**Why the spec misses it:** Out-of-scope item 3 fences "any `/ship-spec` consumption of the deferral sections," which the spec reads as "ship-spec is not a consumer." It is a consumer by default.
**Suggested fix:** Mandate a fixed non-normative preamble immediately under the heading, written by 2e when the section is created, and name it in Design 2's rules: e.g. `> Not part of this spec's implementation scope. Rows record P0/P1 findings deliberately not fixed here; **do not implement them**. Each becomes a follow-up ticket.` Restate it in Design 6 as the reason the bullet is safe, and add a checklist row asserting the preamble text ships.

---

### F-7: Design 4's example disposition phrase does not match the form Design 7 verifies
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:98 vs spec.md:59 and spec.md:131
**Edge case:** The author copies the manifest example rather than the prose rule.
**What happens:** Design 1 step 4 and Design 7 both specify `deferred: D-<n>`; Design 4's example writes `deferred: § Deferred — follow-up required D-2`. The reviewer's rule is stated as pattern-matching "a manifest disposition of `deferred: D-<n>`". A manifest built from the example form is a near-miss; a strict reviewer treats it as an unsatisfied disposition and REOPENs a correctly-deferred finding at its original severity. It degrades rather than breaks (both forms carry the `D-2`), which is why this is P2 and not higher.
**Why the spec misses it:** The example was written to be self-documenting and drifted from the canonical phrase.
**Suggested fix:** Change the Design 4 example line to `— deferred: D-2` and, if the section pointer is wanted, put it after the id in parentheses: `— deferred: D-2 (§ Deferred — follow-up required)`. Then state in Design 7 that the reviewer matches on the `D-<n>` token, ignoring any trailing section pointer.

---

### F-8: The follow-up render must parse rows it is told not to parse, and D12 guarantees hand-edited rows
**Severity:** P2
**Where:** spec.md:107-118 (Design 5), spec.md:41 (D12)
**Edge case:** An operator hand-edits `Follow-up: unfiled` to `Follow-up: VHS-99 (filed, waiting on Devin)`, drops a field while editing, or leaves the row heading without a title.
**What happens:** Design 5's block emits six values per row (`D-n`, finding id, severity, scope, title, follow-up), so it must locate six fields — yet the spec says "The render copies field values; it does not parse or validate rows." With no rule for a missing or reshaped field the render either omits a column silently, misaligns, or drops the row entirely; a dropped row is a silently dropped finding, which Design 6 names as the failure mode this report exists to prevent. D12 makes hand-editing the *designed* path, so malformed rows are expected, not exotic.
**Why the spec misses it:** "Does not parse" was meant as "does not judge correctness," but reads as "no extraction contract."
**Suggested fix:** Replace the sentence with an extraction rule: "The render reads each `### D-<n>:` heading and the labelled fields under it. A missing or unreadable field renders as `?` in its column; a row whose heading is unreadable renders as `D-? (malformed row — see § Deferred — follow-up required)`. The render never omits a row and never edits one." Add that `Follow-up:` is free text and is printed verbatim.

---

### F-9: The new heading is prefix-confusable with `## Deferred (P2+)`, which 2g creates on demand
**Severity:** P2
**Where:** spec.md:65 (Design 2), against untouched `SKILL.md:611, 618, 622-623`
**Edge case:** 2g runs on a spec that has both sections and must "record … in `## Deferred (P2+)` (creating the section if absent)."
**What happens:** Both headings begin `## Deferred`. An agent locating "the Deferred section" by prefix — or creating one it believes absent while the other is present — writes a P2 line into `## Deferred — follow-up required`. That line is then rendered in the FOLLOW-UPS block as a bogus follow-up and, next round, REOPENed by Design 7's well-formedness check as a malformed row at the "original severity" of a finding that has none. Decision 5 required a second section but did not require a confusable name.
**Why the spec misses it:** The spec argues correctly that the two sections are distinct by heading and never asks whether the headings are distinguishable in practice.
**Suggested fix:** Name the new section so no prefix match can confuse it — `## Follow-up required (deferred P0/P1)` — and state in Design 2 that the heading deliberately does not share a prefix with `## Deferred (P2+)`. Update Designs 4, 5, 6, 7 and checklist rows 3 and 5 to the chosen string in one pass.

---

### F-10: 2f-i step 4 now runs the routing step, so an operator-settled grill decision can be routed to defer with nowhere to report it
**Severity:** P2
**Where:** spec.md:48-59 (Design 1), against untouched `SKILL.md:541-556` (2f-i steps 4–5)
**Edge case:** After the round-4 halt, the operator picks option 4, grills a finding, and settles a decision whose fix touches two sites.
**What happens:** 2f-i step 4 says "edit the spec in place **under the 2e rounds-1–3 rules**." Those rules now begin "Route every P0 and P1 finding … before editing anything," so the author can route the operator's own settled decision to **defer** — recording a row and making no other edit, silently discarding a decision the operator just approved in an interactive interview. Step 5's fixed report vocabulary (`dispositioned` / `left open` / `not grillable` / `deferred to option 3`) has no slot for it, and `deferred to option 3` already means something entirely different (narrow the brief), so whatever the author prints, the operator reads the wrong thing. The spec never mentions 2f-i.
**Why the spec misses it:** 2f-i inherits 2e by reference, so a change to 2e changes 2f-i without appearing in the Scope table.
**Suggested fix:** Add a sentence to Design 1: "The routing step does not run inside 2f-i step 4 — a Settled grill decision is the operator's disposition and is applied as written; an item the author believes should be deferred is reported under 2f-i's existing `deferred to option 3` path, not routed." Alternatively, if routing *should* apply there, add the vocabulary slot explicitly (`routed to a follow-up row: <ids>`) and say so in the Scope table.

---

### F-11: Test-plan gaps around the new machinery and the gate commands themselves
**Severity:** P3
**Where:** spec.md:139-148 (Test plan)
**Edge case:** Running the checklist on Windows, and covering the paths F-1/F-4/F-5 exercise.
**What happens:** Three gaps: (a) rows 3 and 8 grep literals containing an em dash (`## Deferred — follow-up required`); per this repo's own recorded gate-script pitfalls, a non-ASCII literal passed through PowerShell can mismatch on encoding and return 0 — a loud false failure, but it will cost the implementer a debugging cycle, and the row gives no note about it; (b) row 3's parenthetical claims the three hits are "(2e definition, 2f render, Phase 3 render)", but the renders emit `=== FOLLOW-UPS`, not the heading — the actual hits are the 2e definition, the two render blocks' source-of-truth prose, and the Design 6 failure-mode bullet, so the count is right for the wrong reason and would not catch a missing render; (c) no row asserts the spec's round-4 or re-run behavior text exists at all, which is where F-1, F-4 and F-5 live.
**Why the spec misses it:** The checklist was written against the diff shape, not against the new behaviors.
**Suggested fix:** Note on rows 3 and 8 that the em-dash literals must be greped from Git Bash (or via a `Deferred . follow-up required` regex) and re-verified with `grep -cF` after the edit; correct row 3's parenthetical to name the four real hits; add a row asserting that SKILL.md contains the round-4 exemption sentence and the unconditional reviewer-step text from F-1's fix.

## Summary
P0: 1 | P1: 5 | P2: 4 | P3: 1

STATUS: RED P0=1 P1=5 P2=4 P3=1 P4=0
