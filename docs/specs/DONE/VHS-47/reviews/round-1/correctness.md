# Correctness Review — round 1

Grounding notes:

- Spec, brief, `CLAUDE.md`, and the three skill files were read from disk in full. `AGENTS.md`, `README.md`, `docs/spec-workflow-reference.md`, `docs/customizing.md`, `lint.py`, `tests/test_lint.py`, `skills/spec-close/SKILL.md` and `skills/spec-brief/SKILL.md` were checked at the lines the spec and brief rely on.
- Ticket lookup was not attempted: the orchestrator reports the shared-memory lookup is ACL-denied on namespace `skills` and directed that the brief stand in for the ticket. No finding filed.
- The spec has no `## Deferred — follow-up required` section, so the Deferred-findings block has nothing to check.
- Recent commits on touched files (both landed 2026-10-08, inside the 7-day window): `156d388` (VHS-46, ship-spec Phase 3b review gate) and `1bd3f29` (VHS-45, /spec-tickets). The spec was checked against the post-commit files. One finding (F-2) comes from the interaction with text that `156d388` left in Phase 5.
- Anchors verified as accurate: brief `skills/spec-cycle/SKILL.md:298`, `:439`, `:533`, `:566`, `:670`, `:703`; `skills/ship-spec/SKILL.md:15`, `:384`; `skills/spec-tickets/SKILL.md:35`, `:5`–`:8`; `skills/spec-close/SKILL.md:339`–`:340`; `README.md:10`–`:12`; `AGENTS.md` items 2, 3, 4 (lines 27, 29, 31); `docs/customizing.md` `## Spec & brief layout` (line 69); `skills/spec-brief/SKILL.md:36` collision check; `tests/test_lint.py:52` asserts 11 skills and `skills/` holds 11; `.gitattributes` forces `eol=lf` on `*.md`, so the Test command's `$`-anchored greps are safe on Windows; `/ship-spec` has no `requires:` block; `/spec-cycle` declares `shell: true` and `filesystem: [read, write]`; `/spec-tickets` declares `filesystem: [read, write]` and no shell.

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Green marker write is placed where 2g's no-candidate path skips it
**Severity:** P1
**Where:** spec § Design, `skills/spec-cycle/SKILL.md`, bullet "2g." (spec.md:184); also § Decision 3 item 2 (spec.md:60)
**Claim:** "**2g.** A new final step 6: write the green marker (Decision 3 item 2)." Decision 3 item 2: "After 2g has finished and before Phase 3 prints, write a green marker".
**Why this is wrong:** 2g has an early exit. `skills/spec-cycle/SKILL.md:687`–`:689` reads: "2. If there are no candidates: print `post-green polish: none tagged`, record any remaining final-round P2s in `## Deferred (P2+)` (creating the section if absent), and proceed to Phase 3." An agent following that step leaves 2g at step 2 and never reaches a step 6 appended after step 5. The no-candidate path is the ordinary one (no reviewer tagged a P2 `Pre-ship recommended`). On that path the run ends green with the pending marker from Decision 3 item 1 still on disk, `/ship-spec` classifies it `pending` and asks for confirmation, and Phase 3 still prints `Verdict: green — …/verdict.md`. That contradicts brief Decision 17 ("a run that has just ended green passes its own fingerprint check") and Done-when bullet 1. The Design names no edit to step 2, so the spec as written produces this.
**Suggested fix:** In § Design, `skills/spec-cycle/SKILL.md`, replace the 2g bullet with: "**2g.** A new final step 6: write the green marker (Decision 3 item 2). Step 2's no-candidate exit is reworded from 'and proceed to Phase 3' to 'and go to step 6', so both paths through 2g write the marker." Add one row to the Test plan review checklist: "Green is written on the 2g path with no candidates as well as on the path that folds candidates." (Equivalent alternative: move the write out of 2g and make it the first sentence of Phase 3, before the output template; then update Decision 3 item 2's wording and the checklist row "Green is written after 2g" to match.)

### F-2: `Spec verdict:` line "placed first" collides with Phase 5's "replace the first bullet" rule for `N/A` runs
**Severity:** P1
**Where:** spec § Design, `skills/ship-spec/SKILL.md`, bullet "Phase 5" (spec.md:196); § Decision 6 last paragraph (spec.md:138)
**Claim:** "**Phase 5:** the Test plan block gains the kept `Spec verdict:` line, placed first."
**Why this is wrong:** `skills/ship-spec/SKILL.md:305` (current text, unchanged by this spec) says: "(When the resolved test command is `N/A`, replace the first bullet with `- [x] Tests: N/A — doc-only/ops-only change, no test artifacts produced` and omit the test-output file link.)" Today the first bullet is the test-command bullet at `:306`. With the verdict line placed first, "the first bullet" is the verdict line, so an `N/A` run following the skill text replaces the verdict line with the `Tests: N/A` line and leaves the stale `<combined test command>` bullet in place. `N/A` is the normal case for doc-only specs, which most specs in this repo are. The result drops the trace that brief Decisions 7 and 9 require ("the PR body say[s] which kind it was"; "`/ship-spec` puts one line in the PR body"). The spec lists no edit to the `:305` parenthetical.
**Suggested fix:** In § Design, `skills/ship-spec/SKILL.md`, change the Phase 5 bullet to: "**Phase 5:** the Test plan block gains the kept `Spec verdict:` line, placed directly above the `Review gate:` line. The test-command bullet stays first, so the existing `N/A` rule ('replace the first bullet') is unchanged." If the line must be first, instead add: "and the `N/A` parenthetical is reworded from 'replace the first bullet' to 'replace the test-command bullet'."

### F-3: Red halt block is called "three-line" but has four lines, and its sentence does not fit /spec-tickets
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7 (spec.md:144); § Test plan checklist (spec.md:237); block at § Decision 6 (spec.md:121–126)
**Claim:** "`red`: halt in preflight, before any draft, with the same three-line block as Decision 6 naming `/spec-tickets`." Test plan: "red halts with the three-line block".
**Why this is wrong:** The Decision 6 block is four lines (`SPEC VERDICT: red …`, `/ship-spec does not implement a red spec.`, `Get a green verdict first: …`, the indented `/spec-cycle <spec-path> --attest "<reason>"`). Swapping the name gives "/spec-tickets does not implement a red spec", which is the wrong verb: that skill files tickets. The implementer has to guess the text.
**Suggested fix:** Call it "the red halt block" in both places, and give the /spec-tickets second line in Decision 7: `/spec-tickets does not file tickets for a red spec.`

### F-4: The marker's H1 contains the string `verdict:`; the key-line rule does not say keys start the line
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 1 (spec.md:29, :43); § Decision 5 `unreadable` row (spec.md:104)
**Claim:** "Fields are `key: value` lines, lower-case keys, one per line. A reader takes the first line for each key and ignores anything else in the file."
**Why this is wrong:** The template's first line is `# Spec verdict: <TICKET-ID>`. A reader that looks for the first line containing `verdict:` gets `VHS-47` as the value and lands on `unreadable` for every marker. The rule depends on the key starting the line and never says so.
**Suggested fix:** Add to the first field rule: "A field line begins with its key at the first character of the line; the `# Spec verdict:` heading is not a field." Or retitle the H1 so it has no `verdict:` substring (for example `# Spec verdict — <TICKET-ID>`).

### F-5: Design for /ship-spec does not carry the fingerprint rule the Test plan requires there
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, `skills/ship-spec/SKILL.md` (spec.md:194); § Test plan checklist (spec.md:240)
**Claim:** Design: "**Phase 0 step 1b:** Decision 6 in full, carrying Decision 5's table." Test plan: "The fingerprint rule (carriage returns removed, `sha256-lf:` prefix) is stated once in `/spec-cycle` and restated identically in `/ship-spec`."
**Why this is wrong:** Decision 6 and Decision 5 say "computing the fingerprint" and do not say how. Decision 2 is assigned only to `/spec-cycle`'s `## The verdict marker` section (spec.md:181). The Design bullet for `/ship-spec` therefore omits what the checklist demands. A `/ship-spec` that hashes the raw bytes classifies every green marker `changed` on a CRLF checkout.
**Suggested fix:** Change the bullet to: "**Phase 0 step 1b:** Decision 6 in full, carrying Decision 5's table and Decision 2's fingerprint rule and tagged command example, word for word as `/spec-cycle` states them."

### F-6: Phase 0 summary in /spec-tickets is specified two ways
**Severity:** P2
**Where:** spec § Decision 7 (spec.md:147–152) vs § Design, `skills/spec-tickets/SKILL.md`, "Phase 0 step 6" (spec.md:203)
**Claim:** Decision 7: "The verdict line is printed in the Phase 0 summary and in the approval block" (the full `Verdict: …` lines). Design: "the printed line gains `· verdict: <state>`".
**Why this is wrong:** One section puts the full `Verdict:` line in the Phase 0 summary, the other a bare state token. Phase 4's re-read compares against "the line that was printed", so which form is printed matters.
**Suggested fix:** In Decision 7 say: "The Phase 0 line carries the token `· verdict: <state>`; the full verdict line is printed in the approval block, directly under `Storage:`", and name the approval-block line as the one Phase 4 compares against.

### F-7: Phase 4 re-check compares "state or kind"; brief Decision 15 says the verdict line
**Severity:** P2
**Where:** spec § Decision 7 (spec.md:156)
**Claim:** "read the marker again; if its state or kind differs from the line that was printed, halt with no writes and ask for a new approval."
**Why this is wrong:** Brief Decision 15: "stops for a new approval if the verdict line differs from the one it printed." The printed line also carries the date and, for `unreadable`, the reason. A marker rewritten green on a later date, or unreadable for a different reason, passes the spec's check and fails the brief's. The practical gap is small (Phase 4 step 1 already halts on a changed spec), but the wording narrows a carried decision.
**Suggested fix:** "if the verdict line it would now print differs from the one that was printed, halt with no writes and ask for a new approval."

### F-8: A failed pending write has no print site, and can leave an earlier green marker in place
**Severity:** P2
**Where:** spec § Decision 3, failed-write paragraph (spec.md:65)
**Claim:** "Print `verdict marker NOT written: <error>` directly under the SPEC READY header or above the halt block. The marker on disk is then whatever the last successful write left, normally pending."
**Why this is wrong:** The two print sites cover the green and red writes. The pending write happens at the start of Phase 2 where neither exists. If the pending write fails on a re-run, the marker on disk is the previous run's (possibly green and still matching), not pending, while a new review is in flight.
**Suggested fix:** Add: "A failed pending write prints the same line at once, before round 1 is dispatched, and the run continues. The marker on disk is then the previous run's; the line says so."

### F-9: Phase 3 `Verdict: green — <path>` line is unconditional
**Severity:** P3
**Where:** spec § Decision 3 (spec.md:67); § Design "Phase 3" (spec.md:187)
**Claim:** "Phase 3's output gains one line under `Rounds:`: `Verdict: green — docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`."
**Why this is wrong:** When the green write failed, or wrote `fingerprint: none`, the line still states a green marker at that path, beside the NOT-written line.
**Suggested fix:** State that the line is replaced by the `verdict marker NOT written: <error>` line when the write failed, and gains ` (fingerprint not computed)` when it was written with `fingerprint: none`.

### F-10: Usage line names `<brief-path>` while attest mode takes a brief or spec path
**Severity:** P3
**Where:** spec § Decision 4 (spec.md:71); § Design Docs (spec.md:211)
**Claim:** "Invocation: `/spec-cycle <path> --attest "<reason>"`. `<path>` is the brief path or the spec path" and usage `Usage: /spec-cycle <brief-path> [--attest "<reason>"]`.
**Why this is wrong:** The usage line and the `AGENTS.md` / `README.md` form imply attest needs a brief path, while the `/ship-spec` red block tells the operator to pass `<spec-path>`.
**Suggested fix:** Print two usage lines: `/spec-cycle <brief-path>` and `/spec-cycle <brief-or-spec-path> --attest "<reason>"`.

### F-11: Test command checks `requires:` on two skills; Test plan item 8 says three
**Severity:** P3
**Where:** spec § Test plan item 8 (spec.md:227); § Test command (spec.md:250)
**Claim:** "No `requires:` block changed: the frontmatter of the three skills is unchanged."
**Why this is wrong:** The final clause diffs only `skills/spec-cycle/SKILL.md` and `skills/spec-tickets/SKILL.md`. A `requires:` block added to `/ship-spec`, which the Out-of-scope list fences off (VHS-51), would pass the gate.
**Suggested fix:** Add `skills/ship-spec/SKILL.md` to that `git diff` path list.

### F-12: `unreadable` does not cover a marker with no `ticket:` or no `fingerprint:` line
**Severity:** P3
**Where:** spec § Decision 5 table (spec.md:104, :108)
**Claim:** "`unreadable` | The file has no `verdict:` line with one of the three values, or its `ticket:` value is not this spec's ticket id".
**Why this is wrong:** A marker with a valid `verdict:` and no `ticket:` line, or a green one with no `fingerprint:` line, is not clearly placed in any row.
**Suggested fix:** "or it has no `ticket:` line, or its `ticket:` value is not this spec's ticket id"; and in the `changed` row, "the marker's is `none` or absent".

## Summary
P0: 0 | P1: 2 | P2: 6 | P3: 4 | P4: 0

STATUS: RED P0=0 P1=2 P2=6 P3=4 P4=0
