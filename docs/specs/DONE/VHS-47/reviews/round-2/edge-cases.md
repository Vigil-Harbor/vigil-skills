# Edge-Cases Review — round 2

Spec: `docs/specs/TODO/VHS-47.spec.md` · Brief: `docs/specs/TODO/VHS-47.brief.md`

Grounding: spec and brief read fresh from disk; `AGENTS.md` and the machine-local `CLAUDE.md` read; the three round-1 reports read; `skills/spec-cycle/SKILL.md` (invocation, Phase 0 steps 1–2, Phase 1 re-run rule, 2c–2g, Phase 3, Tool-use notes, Failure modes), `skills/ship-spec/SKILL.md` (Phase 0, Phase 1, Phase 5 PR body, Tool-use notes, Failure modes) and `skills/spec-tickets/SKILL.md` (whole file) read at the lines the spec edits. Ticket lookup in shared memory skipped per orchestrator note (ACL); the brief is the ticket text. The spec has no `## Deferred — follow-up required` section, so there are no rows to validate. `scale_lens` is off and no `scalability.md` exists in `round-1/`.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Green marker write is placed where 2g's no-candidate path skips it | CLOSED | spec § Design, spec-cycle, "Phase 3" bullet (spec.md:186): the write is Phase 3's first sentence and 2g is not edited. Checked against `skills/spec-cycle/SKILL.md:687`–`:689` (the no-candidate exit ends "proceed to Phase 3") and `:439` (2d → 2g → Phase 3): every green path reaches Phase 3 and no red path does. Decision 3 item 2 (spec.md:60) and the 2d bullet (spec.md:183) agree on the timing. The checklist row lags; see F-3. |
| correctness | F-2 (P1) | `Spec verdict:` line "placed first" collides with Phase 5's "replace the first bullet" rule for `N/A` runs | CLOSED | spec § Design, ship-spec, "Phase 5" bullet (spec.md:196): the line sits directly above `Review gate:`; the test-command bullet stays first. Checked against `skills/ship-spec/SKILL.md:305`–`:309`: the `N/A` rule still hits the test-command bullet, and a skipped review still prints a `Review gate:` line to anchor on. |
| correctness | F-3 | Red halt block is called "three-line" | PARTIAL (P2) | Decision 7 (spec.md:144) now gives the `/spec-tickets` second line. Test plan (spec.md:239) still says "the three-line block"; the block at spec.md:122–125 has four lines. Covered by F-3 below. |
| correctness | F-4 | Marker H1 contains `verdict:` | CLOSED | Decision 1 (spec.md:43): key at the start of the line; the heading is not a field. |
| correctness | F-5 | ship-spec Design does not carry the fingerprint rule | CLOSED | spec.md:193. |
| correctness | F-6 | Phase 0 summary in /spec-tickets specified two ways | CLOSED | Decision 7 (spec.md:147) and Design (spec.md:204) both print the full verdict line. |
| correctness | F-7 | Phase 4 re-check compares "state or kind" | CLOSED | spec.md:156 compares the verdict line. |
| correctness | F-8 | Failed pending write has no print site | CLOSED | Decision 3 (spec.md:65). |
| correctness | F-9 | Phase 3 `Verdict:` line is unconditional | CLOSED | spec.md:67 gives the NOT-written form; Decision 2 (spec.md:55) prints the fingerprint-not-computed line. |
| correctness | F-10 | Usage line names `<brief-path>` | CLOSED | Acknowledged in § Deferred (P2+), spec.md:282. |
| correctness | F-11 | Test command checks `requires:` on two skills | CLOSED | Test command's last clause (spec.md:253) lists all three. |
| correctness | F-12 | `unreadable` does not cover a missing `ticket:` or `fingerprint:` line | CLOSED | Decision 5 rows (spec.md:104, :108). |
| edge-cases | F-1 | Failed pending write is silent on the interrupted path | CLOSED | Decision 3 (spec.md:65): printed at once, before round 1, naming the marker still on disk. |
| edge-cases | F-2 | Attest mode has no outcome for its own failed write | CLOSED | Decision 4 step 6 (spec.md:93). |
| edge-cases | F-3 | Phase 3 prints `Verdict: green — <path>` after a failed write | CLOSED | spec.md:67. |
| edge-cases | F-4 | Prompts do not say what other replies do | CLOSED | spec.md:92 and :136: any reply other than `1` is treated as 2. |
| edge-cases | F-5 | Decision 5: row order; green marker with no usable fingerprint | PARTIAL (P2) | Order (spec.md:99) and the absent or `none` fingerprint (spec.md:108) are folded. Part (c), a green marker with no usable `source:`, is not; see F-4 below. |
| edge-cases | F-6 | `/spec-tickets` prints plain green for `fingerprint: none` | CLOSED | Decision 7 (spec.md:142) states it and says why. Residual wording in Decision 2 is F-7 below (P3). |
| edge-cases | F-7 | Leave-alone check compares against a moving `origin/main` | PARTIAL (P3) | The `requires:` half is folded (spec.md:253). The merge-base half is not folded and is not in § Deferred (P2+). Carried as F-9 below. |
| edge-cases | F-8 to F-11 | Rename; attest fingerprint at write time; POSIX hash example; attested reason lost on re-run | CLOSED | Acknowledged in § Deferred (P2+), spec.md:275–278. |
| conventions | F-1 | Table and parse rule have no home in `/spec-cycle`; nothing pins the copies | PARTIAL (P2) | The table's home (spec.md:181) and the checklist row (spec.md:243) are folded. The reader's parse rule is still assigned only to `/spec-cycle`; see F-2 below. The new checklist row has its own gap; see F-1 below. |
| conventions | F-2 | Three spellings of the attest invocation | CLOSED | Decision 4 (spec.md:71) fixes one form; the rest is acknowledged at spec.md:282. |
| conventions | F-3 | `/spec-tickets` keeps "Green-lit check" | CLOSED | spec.md:202. |
| conventions | F-4 | 2f-i clause position | CLOSED | spec.md:185. |
| conventions | F-5 | Test command checks two skills' frontmatter | CLOSED | spec.md:253. |
| conventions | F-6 | Failed-write rule not marked as a spec-level addition | CLOSED | spec.md:65 marks it; spec.md:279 lists it. |
| conventions | F-7, F-8, F-10, F-11 | Spec-level additions; headless stop; heading list; prose hash | CLOSED | Acknowledged in § Deferred (P2+), spec.md:279–281. |
| conventions | F-9 | Tool-use notes updated for `/spec-cycle` only | CLOSED | spec.md:194 and :208. |

## Findings

No P0 or P1. I walked each marker state through both readers again, plus the write paths the round-2 edits moved:

- A red marker halts in both readers, and the only writes that replace it are a new run's pending write and an attestation behind an operator prompt.
- No path leaves a green marker for text no reviewer or operator judged without `/ship-spec` reading `changed`. The one exception needs two failed writes in one run and is in F-5.
- Phase 3 is reached on every green path and on no red one, so the moved green write cannot be skipped and cannot record a false green.
- Option 4's re-render of the halt block does not rewrite the red marker: Decision 3 item 4 and the new 2f-i clause both say so.

The findings below are gaps a careful agent would resolve but the skill text should pin.

### F-1: A literal copy of the classification table does not fit `/spec-tickets`, and the checklist row asks for a literal copy
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5 table (spec.md:101–108); § Decision 7 (spec.md:142–145); § Design, spec-tickets, "Phase 0 step 4" (spec.md:203); § Test plan (spec.md:243)
**Edge case:** Precondition mismatch between a shared table and a reader that computes no fingerprint and has no prompt.
**What happens:** The checklist says the table's "rows and order are the same in all three skills, apart from `/spec-tickets` having no `changed` row". Two cells of the remaining rows are wrong for that skill:

- The `green` row's condition is "`verdict: green` and the reader computed a fingerprint equal to the marker's". `/spec-tickets` computes none, so with the `changed` row removed a green marker matches no row.
- The action column says "Confirm" for `missing`, `unreadable` and `pending`, and "Every confirm stops on a host that cannot wait". Decision 7 says "There is no separate prompt".

An implementer who satisfies the checklist row writes installed text that disagrees with the same step's own prose. The agent running the skill can resolve it from the note ("always `green` here"), so it is not a missing outcome.
**Why the spec misses it:** The round-1 fold added the "same rows" checklist row without restating the two cells that differ.
**Suggested fix:** In § Design, spec-tickets, Phase 0 step 4, say: "The `green` row's condition reads `verdict: green`, with no fingerprint clause. The action column reads `Verdict line; continue` for `missing`, `unreadable`, `pending` and `green`, and `Halt` for `red`." Change the checklist row to: "…the same in all three skills, except that `/spec-tickets` has no `changed` row, its `green` row has no fingerprint clause, and its action column names the verdict line where the others say Confirm or Pass."

### F-2: The two skills that read the marker are not given the rule for reading it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, spec-cycle (spec.md:181); ship-spec (spec.md:193); spec-tickets (spec.md:203); § Decision 1 (spec.md:43)
**Edge case:** Malformed or unexpected marker content read by a skill that was never told the format.
**What happens:** Decision 1's reader rule (a field line has its key at the start of the line; the `# Spec verdict:` heading is not a field; first line per key wins; everything else is ignored) is placed in `/spec-cycle`'s `## The verdict marker`. `/ship-spec` carries "Decision 5's table and Decision 2's fingerprint rule"; `/spec-tickets` carries the table. Design line 181 says each carries its own copy "because a skill is read alone", but the copies leave out the rule the table depends on. A reader matching on `verdict:` anywhere in a line hits the heading first and gets the ticket id as the value, which is `unreadable` for every marker. It degrades to a confirm, so it is safe, but it is the round-1 correctness F-4 defect in the two files that do the reading.
**Why the spec misses it:** The fold for conventions/R1/F-1 moved the table and left the parse rule where it was.
**Suggested fix:** Add to both Design bullets (spec.md:193 and :203): "and Decision 1's reader rule: a field is a line that begins with its lower-case key; the `# Spec verdict:` heading is not a field; take the first line for each key, trim the value, ignore the rest." Add it to the checklist row at spec.md:243.

### F-3: Two checklist rows lag the round-2 edits
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan (spec.md:235 and :239)
**Edge case:** Regression coverage for the path round 1 found broken.
**What happens:** "Green is written after 2g" is true of a write appended to 2g's step 5, which is the placement round 1 found to be skipped on the no-candidate exit. The checklist is the only gate on skill text (spec.md:231), and this row would pass the defect it exists to catch. Separately, "red halts with the three-line block" names a block that has four lines (spec.md:122–125).
**Why the spec misses it:** The Design bullet moved; the checklist row did not.
**Suggested fix:** Replace the first row with: "Green is written as Phase 3's first step, before the output template, so a run whose 2g found no candidates writes it too; 2g's text is unchanged; red is written in 2f after round 4's edits; 2f-i writes nothing." In the second row, replace "the three-line block" with "the red halt block".

### F-4: A green marker with no usable `source:`, `round:` or `date:` has nothing to print as its kind
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5 (spec.md:110); § Decision 6 (spec.md:118, :122); § Decision 7 (spec.md:149)
**Edge case:** Malformed marker: `verdict: green`, a matching fingerprint and the right `ticket:`, but `source:` absent or neither of the two values, or `round:` or `date:` absent. A hand-written marker is the realistic cause.
**What happens:** The marker classifies `green` and passes. The PR-body line `Spec verdict: green (<kind>, <date>)` and the `/spec-tickets` line have placeholders with no value. Brief Decision 7 wants the kind stated. An agent will print something; the spec does not say what. The same holds for the red block's `round`, `gate` and `date`, where it matters less because red halts either way. This is round-1 F-5 part (c).
**Why the spec misses it:** Decision 5 tests only `verdict:`, `ticket:` and `fingerprint:`.
**Suggested fix:** Add under the Decision 5 table: "A field a printed line needs and the marker lacks is printed as `unknown`. A `verdict: green` marker whose `source:` is absent or not one of the two values is `unreadable` (reason: no source)."

### F-5: The failed green-write line has two stated positions, and a run with every write failing leaves the earlier marker standing
**Severity:** P3
**Where:** spec § Decision 3 (spec.md:65, :67); § Design, spec-cycle, "Phase 3" (spec.md:186)
**Edge case:** Partial failure. (a) The green write is Phase 3's first step, before the template prints. Line 65 says to print the NOT-written line "at once, where the write was attempted" and also "under the SPEC READY header", which comes later, and line 67 adds a second line (`Verdict: green — marker NOT written`) under `Rounds:`. The agent has to choose where the first goes. (b) A re-run on a spec with an earlier green marker where the file cannot be written at all (a lock held for the whole run): the pending write and the red write both fail, each printing its line. The marker on disk stays green. Round 2e edited the spec, so `/ship-spec` reads `changed` and confirms. `/spec-tickets` prints `Verdict: green … fingerprint not checked` for a spec whose latest review ended red.
**What happens:** (a) is cosmetic. (b) is a double failure the operator was told about twice, and the brief accepts an unchecked green in `/spec-tickets`.
**Suggested fix:** (a) "Print the line directly under the SPEC READY header; the `Verdict:` line under `Rounds:` then reads `green — marker NOT written`." (b) One sentence in the Failure-modes bullet: "If the marker on disk is green and this run ended red, delete or fix the marker by hand before `/spec-tickets`."

### F-6: A marker that exists but cannot be read, and values with trailing whitespace, are not placed
**Severity:** P3
**Where:** spec § Decision 5, `missing` and `unreadable` rows (spec.md:103–104); § Decision 1 (spec.md:43)
**Edge case:** (a) `verdict.md` exists but the read errors (permissions, a lock, or the path is a directory). The `missing` row is "does not exist"; the `unreadable` row is about content. (b) A marker saved with CRLF line endings, so a shell-extracted value is `green\r`, or a fingerprint with a trailing carriage return.
**What happens:** (a) An agent lands on `unreadable`, which is the brief's intent (Decision 14). (b) A strict comparison gives `unreadable` or `changed`; both confirm. On Windows hosts it could be routine.
**Suggested fix:** `unreadable` row: "The file cannot be read, or has no `verdict:` line…". Decision 1: "Values are trimmed of surrounding whitespace, carriage returns included."

### F-7: Decision 2 says "downstream" where it means `/ship-spec`
**Severity:** P3
**Where:** spec § Decision 2 (spec.md:55) against § Decision 7 (spec.md:142)
**Edge case:** `verdict: green` with `fingerprint: none`.
**What happens:** Decision 2's sentence goes into `/spec-cycle`'s marker section and says such a marker "reads downstream as the changed-spec case". Decision 7 says `/spec-tickets` reads it `green`. The two sit in different skills, and Decision 7 is explicit, so nothing misbehaves; an operator reading `/spec-cycle`'s text is told something untrue of one reader.
**Suggested fix:** "…reads in `/ship-spec` as the changed-spec case; `/spec-tickets` does not check fingerprints."

### F-8: Filing a deferred follow-up by hand turns every such spec `changed`
**Severity:** P3
**Where:** spec § Decision 5 `changed` row (spec.md:108); `skills/spec-cycle/SKILL.md:487` (R2)
**Edge case:** A spec that ends green with rows in `## Deferred — follow-up required`. R2 tells the operator to replace `Follow-up: unfiled` with the ticket id by hand. That edit changes the spec's bytes.
**What happens:** `/ship-spec` reads `changed` and asks to confirm, and the PR body carries the unchecked `proceeded on operator confirmation` line for a spec whose reviewed text did not change in substance. Safe, and inside brief Decision 4, but it is the expected path for any spec with deferred rows, not an exception.
**Suggested fix:** One sentence in `## The verdict marker`: "Editing a `Follow-up:` value after green changes the fingerprint; expect the confirm, or re-attest."

### F-9: The leave-alone check still compares against a moving `origin/main`
**Severity:** P3
**Where:** spec § Test command (spec.md:253)
**Edge case:** `origin/main` advances and is fetched between the worktree cut and a later test run (a `/review-pr` fix round). The first `git diff --name-only origin/main -- …` then lists files this change never touched and the gate fails. Residual of round-1 F-7; inherited from VHS-46.
**Suggested fix:** Diff against `$(git merge-base origin/main HEAD)` in both clauses, or add the item to § Deferred (P2+).

### F-10: The pending paragraph's position relative to "For each round 1..4:"
**Severity:** P4
**Where:** spec § Design, spec-cycle, "Phase 2" (spec.md:182); `skills/spec-cycle/SKILL.md:319`–`:323`
**Edge case:** "A new first paragraph before `### 2a`" can land after the line "For each round 1..4:", where it reads as a per-round step. A pending write at the top of round 2 changes nothing on disk, so the cost is nil.
**Suggested fix:** "placed above the line `For each round 1..4:`".

## Persistence checklist (the marker is persisted state)

1. **Atomicity.** Whole-file replace, no temp-and-rename. A cut-short write leaves no `verdict:` line (`unreadable`) or a green line with no fingerprint (`changed`, spec.md:108). `verdict:` is the first field, so a truncated file never shows a verdict the writer did not intend. CHECKED.
2. **Size bound.** Ten single-line fields; `reason` is one line, with line breaks folded to spaces (spec.md:71). CHECKED.
3. **Idempotency on retry.** One path per spec, whole-file replace. CHECKED.
4. **Read-side filtering.** The `ticket:` test rejects a marker copied from another spec; the rename case is acknowledged (spec.md:275). CHECKED.
5. **Forward-compat.** First line per key, unknown lines ignored, unknown verdict value is `unreadable`, the `sha256-lf:` prefix names the algorithm and a value in any other form reads as "differs". CHECKED, with F-2 for the readers' copy of the rule.
6. **Write-then-read race.** Concurrent runs over one spec are outside the supported flow by the brief; `/spec-tickets` Phase 4 re-reads. CHECKED.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 5 | P4: 1

STATUS: GREEN
