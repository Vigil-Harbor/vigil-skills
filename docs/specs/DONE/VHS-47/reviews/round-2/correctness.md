# Correctness Review — round 2

> Saved by the orchestrator from the reviewer's returned report (spec-cycle 2c); the reviewer did not write the file itself.

Grounding notes:

- Spec, brief, `CLAUDE.md`, the three round-1 reports, `skills/spec-tickets/SKILL.md` and `skills/ship-spec/SKILL.md` were read from disk in full. `skills/spec-cycle/SKILL.md` was read at every region the spec edits (lines 1-62, 290-330, 405-449, 528-577, 655-824). `AGENTS.md`, `README.md`, `docs/customizing.md`, `docs/spec-workflow-reference.md` and `lint.py` were checked at the lines the spec relies on.
- Ticket lookup was not attempted: the orchestrator reports the shared-memory lookup is ACL-denied on namespace `skills` and directed that the brief stand in for the ticket. No finding filed.
- The spec has no `## Deferred — follow-up required` section (its `## Deferred (P2+)` section is a different, advisory list), so the Deferred-findings block has nothing to validate.
- Recent commits on touched files, both 2026-10-08 and inside the 7-day window: `156d388` (VHS-46, ship-spec review gate) and `1bd3f29` (VHS-45, /spec-tickets). The spec was checked against the post-commit files and matches them.
- Anchors and references confirmed present: `skills/spec-cycle/SKILL.md:15` (invocation line), `:19` (`## Why split from /ship-spec`), Phase 0 steps 1 to 8 (`:29`-`:237`), `:298`, `:319`-`:323` (Phase 2 opening before `### 2a`), `:439` (2d green break), `:533` (2f), `:663`-`:665` (the "2f-i never …" sentence, with `never edits the brief,` directly before `and runs at most once per invocation`), `:670`, `:687`-`:689` (2g no-candidate exit to Phase 3), `:703`-`:710` (Phase 3, `SPEC READY`, `Rounds:`), `:758`, `:767`; `skills/ship-spec/SKILL.md:15`, `:54` (preflight summary), `:305`-`:308` (Phase 5 Test plan block), `:372`, `:384`; `skills/spec-tickets/SKILL.md:34`-`:38` (steps 2, 3, 4, 6), `:90` (`Storage:`), `:131` (Phase 4 step 1), `:165`, `:176`; `README.md:10`-`:12`; `AGENTS.md:27`, `:29`, `:31`; `docs/customizing.md:74`-`:77`; `docs/spec-workflow-reference.md:39`, `:129`, `:151`. `/spec-cycle` declares `shell: true` and `filesystem: [read, write]`; `/spec-tickets` declares `filesystem: [read, write]` and no shell; `/ship-spec` has no `requires:` block. `lint.py --strict` fails only on ERROR, and its one body rule flags `mcp__*` names, which the spec adds none of.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Green marker write is placed where 2g's no-candidate path skips it | CLOSED | spec.md:186 makes the write Phase 3's first sentence and leaves 2g unedited; spec.md:60 agrees; `skills/spec-cycle/SKILL.md:687-689` and `:439` show every green run reaches Phase 3 |
| correctness | F-2 | `Spec verdict:` line "placed first" collides with the "replace the first bullet" rule | CLOSED | spec.md:196 places the line directly above `Review gate:`; `skills/ship-spec/SKILL.md:305-308` keeps the test-command bullet first |
| correctness | F-3 | Red halt block called "three-line"; sentence does not fit /spec-tickets | PARTIAL (P2) | spec.md:144 now gives the /spec-tickets second line; spec.md:239 still says "three-line block" (see F-2) |
| correctness | F-4 | Marker H1 contains `verdict:`; key-line rule | CLOSED | spec.md:43 (the reader copies are F-4 below) |
| correctness | F-5 | /ship-spec Design does not carry the fingerprint rule | CLOSED | spec.md:193 |
| correctness | F-6 | /spec-tickets Phase 0 summary specified two ways | CLOSED | spec.md:147 and spec.md:204 now agree: the full verdict line on its own line |
| correctness | F-7 | Phase 4 re-check compares "state or kind" | CLOSED | spec.md:156 |
| correctness | F-8 | Failed pending write has no print site | CLOSED | spec.md:65 |
| correctness | F-9 | Phase 3 `Verdict: green` line is unconditional | PARTIAL (P3) | spec.md:67 adds the write-failed form; the `fingerprint: none` case has no form (see F-6) |
| correctness | F-10 | Usage line names `<brief-path>` | DEFERRED | spec.md:282 (§ Deferred (P2+)); sub-P1, no D-row needed. The round-2 edit left a new inconsistency, filed as F-1 |
| correctness | F-11 | Test command checks `requires:` on two skills | CLOSED | spec.md:253, final clause lists all three skill files |
| correctness | F-12 | `unreadable` does not cover a missing `ticket:` or `fingerprint:` line | CLOSED | spec.md:104, :108 |
| edge-cases | F-1 | Failed pending write is silent and leaves the previous verdict | CLOSED | spec.md:65 prints at once and names the marker on disk |
| edge-cases | F-2 | Attest mode: failed write, reviews directory | CLOSED | spec.md:93 |
| edge-cases | F-3 | Phase 3 prints `Verdict: green — <path>` when the write failed | PARTIAL (P2) | spec.md:67 covers the failed write; the fingerprint-not-computed form is absent, though spec.md:55 prints its own line (see F-6) |
| edge-cases | F-4 | Prompts do not say what a reply other than 1 or 2 does | CLOSED | spec.md:92, :136 |
| edge-cases | F-5 | Row order; green marker with no usable fingerprint; missing `source:` | PARTIAL (P2) | spec.md:99 fixes the order and spec.md:108 the absent fingerprint; a green marker with an absent or unknown `source:` still has no stated kind |
| edge-cases | F-6 | /spec-tickets prints plain green for `fingerprint: none` | PARTIAL (P2) | spec.md:142 states the choice; spec.md:55 still says "downstream" without limit (see F-3) |
| edge-cases | F-7 | Test command compares against a moving `origin/main` | PARTIAL (P3) | the ship-spec path was added (spec.md:253); the diff base is still `origin/main` and the item is not in § Deferred (P2+) |
| edge-cases | F-8 | Ticket rename makes a green marker unreadable | DEFERRED | spec.md:275 |
| edge-cases | F-9 | Attest fingerprint when the spec changes mid-prompt | DEFERRED | spec.md:276 |
| edge-cases | F-10 | Hash example is POSIX only | DEFERRED | spec.md:277 |
| edge-cases | F-11 | Pending write discards an attested reason | DEFERRED | spec.md:278 |
| conventions | F-1 | Classification table and parse rule have no home in /spec-cycle | PARTIAL (P2) | spec.md:181 and spec.md:243 place and pin the table; the parse rule is still not assigned to the two readers (see F-4) |
| conventions | F-2 | Three spellings of the attest invocation | PARTIAL (P2) | spec.md:71 now claims one spelling; spec.md:180 and spec.md:125 use two others (see F-1) |
| conventions | F-3 | /spec-tickets keeps "Green-lit check" | CLOSED | spec.md:202 |
| conventions | F-4 | 2f-i sentence edit position | CLOSED | spec.md:185; matches `skills/spec-cycle/SKILL.md:663-665` |
| conventions | F-5 | Test command checks two skills' frontmatter | CLOSED | spec.md:253 |
| conventions | F-6 | Failed-write rule not marked as a spec-level addition | CLOSED | spec.md:65, :67 |
| conventions | F-7 | Spec-level additions listed for the drift check | DEFERRED | spec.md:279 |
| conventions | F-8 | Headless /ship-spec stops on every pre-existing spec | DEFERRED | spec.md:280 |
| conventions | F-9 | Tool-use notes updated for /spec-cycle only | CLOSED | spec.md:194, :208 |
| conventions | F-10 | Attest mode restates the heading list | DEFERRED | spec.md:281 |
| conventions | F-11 | Fingerprint as a prose shell command | DEFERRED | spec.md:281 |

No finding is REOPENED. Every PARTIAL item is P2 or P3 and does not enter the gate.

## Findings

### F-1: Attest invocation is spelled three ways while Decision 4 says it is written the same way everywhere
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, `skills/spec-cycle/SKILL.md`, "Invocation line" (spec.md:180); § Decision 4 (spec.md:71); § Decision 6 red block (spec.md:125); § Design Docs (spec.md:212-213)
**Claim:** Decision 4: "Invocation, written the same way everywhere: `/spec-cycle <brief-path> [--attest "<reason>"]`." Design: "`Invoked as: /spec-cycle <brief-path>` gains a second form: `/spec-cycle <path> --attest "<reason>"`."
**Why this is wrong:** The round-2 edit added "written the same way everywhere" to Decision 4, but the Design bullet for the skill's own invocation line (`skills/spec-cycle/SKILL.md:15`) still prescribes a different string, and the red halt block prints a third (`/spec-cycle <spec-path> --attest "<reason>"`). `docs/spec-workflow-reference.md:43` shows `/spec-cycle <path-to-brief>` and the Docs bullet does not say whether that line changes. Behaviour is unaffected; the implementer has to pick a string for line 15.
**Suggested fix:** Replace spec.md:180 with: "**Invocation line.** `Invoked as: /spec-cycle <brief-path>` becomes `/spec-cycle <brief-path> [--attest "<reason>"]`, with one sentence: with `--attest` the path may be the spec path; see `## Attest mode`." In the Docs bullet at spec.md:212 add: "its `**Invocation:**` line gains `[--attest "<reason>"]`." Leave the red block's `<spec-path>` as is; it is an instance of the form, and § Deferred (P2+) already records that.

### F-2: Test plan still calls the red halt block "three-line"
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan checklist (spec.md:239); block at § Decision 6 (spec.md:121-126)
**Claim:** "`/ship-spec` step 1b: green passes; red halts with the three-line block".
**Why this is wrong:** The block has four lines. Decision 7 was corrected to "Decision 6's red block" (spec.md:144); this checklist row was not. A reviewer working the checklist counts lines and finds a mismatch. This is the open half of round-1 correctness F-3.
**Suggested fix:** Change spec.md:239 to "red halts with the red block (four lines, ending in the `--attest` line)".

### F-3: Decision 2's `fingerprint: none` sentence says "downstream", but /spec-tickets reads that marker as green
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 2 (spec.md:55) vs § Decision 7 (spec.md:142); § Design, `## The verdict marker` bullet (spec.md:181)
**Claim:** Decision 2: "A green marker with `fingerprint: none` reads downstream as the changed-spec case." Decision 7: "a `verdict: green` marker is always `green` here and never `changed`, including one whose `fingerprint:` is `none`".
**Why this is wrong:** Decision 7 is the explicit rule and a careful reader follows it. But Design puts Decision 2 into `/spec-cycle`'s canonical `## The verdict marker` section, so the installed skill would state a rule that one of the two downstream skills does not follow. This is the open half of round-1 edge-cases F-6.
**Suggested fix:** Add to the `## The verdict marker` bullet at spec.md:181: "Decision 2's last sentence is written as: a green marker with `fingerprint: none` reads as the changed-spec case in `/ship-spec`; `/spec-tickets` does not look at the fingerprint."

### F-4: The marker parse rule is not carried into the two skills that read the marker
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, `skills/ship-spec/SKILL.md` "Phase 0 step 1b" (spec.md:193); `skills/spec-tickets/SKILL.md` "Phase 0 step 4" (spec.md:203); § Decision 1 (spec.md:43); § Test plan (spec.md:242-243)
**Claim:** spec.md:181: "`/ship-spec` and `/spec-tickets` each carry their own [table], because a skill is read alone." spec.md:193: "Decision 6 in full, carrying Decision 5's table and Decision 2's fingerprint rule and tagged example".
**Why this is wrong:** The rule that makes the table usable (a field line has its key at the start of the line, the first line per key wins, the `# Spec verdict:` heading is not a field) is assigned only to `/spec-cycle`'s section. By the spec's own premise that a skill is read alone, the two readers do not get it. A reader that matches `verdict:` inside the H1 `# Spec verdict: <TICKET-ID>` gets the ticket id as the value and lands on `unreadable` for every marker. That is fail-safe (a confirm), but it would make the green pass unreachable on that host. This is the open half of round-1 conventions F-1.
**Suggested fix:** In spec.md:193 and spec.md:203, add "and Decision 1's reading rule (key at the start of the line, first line per key, the `# Spec verdict:` heading is not a field)". Add one Test plan checklist row: "The reading rule is stated in all three skills."

### F-5: Scope rows omit edits the Design lists
**Severity:** P3
**Where:** spec § Scope (spec.md:12-13) vs § Design (spec.md:194, :202, :204, :208)
**Claim:** The Scope rows enumerate the edits per file.
**Why this is wrong:** The `/ship-spec` row omits the Tool-use notes bullet. The `/spec-tickets` row omits the step 3 label change, the removal of the `reviews: present | absent` token, the renamed Failure modes entry, and the Tool-use notes bullet. Design is complete, so nothing is lost, but the two lists disagree.
**Suggested fix:** Append "Tool-use notes bullet." to both rows and "Step 3 relabelled; step 6's `reviews:` token removed." to the `/spec-tickets` row.

### F-6: Two display lines leave a case unstated
**Severity:** P3
**Where:** spec § Decision 3 (spec.md:67); § Decision 6 (spec.md:138)
**Claim:** "Phase 3's output gains one line … `Verdict: green — <path>`, or `Verdict: green — marker NOT written` when that write failed." and "The one-line preflight summary names the state."
**Why this is wrong:** When the green marker was written with `fingerprint: none`, Phase 3 prints the plain green line although `/ship-spec` will ask for confirmation (Decision 2's own print line is the only signal). Brief Decision 7 asks that the downstream preflight line say which kind of green it was; "names the state" implies it only through spec.md:110.
**Suggested fix:** Add a third Phase 3 form, `Verdict: green — <path> (fingerprint not computed)`, and change spec.md:138 to "names the state and, for green, its kind".

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 2 | P4: 0

STATUS: GREEN
