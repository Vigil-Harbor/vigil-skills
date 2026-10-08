# Conventions Review — round 2

Grounding: spec and brief read fresh from disk; `AGENTS.md` (canonical) and the machine-local `CLAUDE.md`; wiki `projects/vigil-skills/state.md` and `filemap.md` by grep (no `architecture.md` exists for this project); wiki decisions `2026-10-08-vhs-45-…`, `2026-10-08-vhs-46-…`, `2026-08-09-review-round-artifacts-are-immutable.md`, `2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`; `skills/spec-tickets/SKILL.md` in full; `skills/spec-cycle/SKILL.md` lines 1–62, 294–325, 426–445, 530–566, 658–824; `skills/ship-spec/SKILL.md` lines 1–56, 276–315, 370–394; `docs/spec-workflow-reference.md` lines 127–158; `docs/customizing.md` and `README.md` by grep; all three round-1 reports. Ticket lookup skipped per orchestrator note (ACL); the brief is the ticket text.

The spec has no `## Deferred — follow-up required` section (its `## Deferred (P2+)` section is the ordinary P2 carry), so there are no rows, preamble, or ceiling to validate. `scale_lens` is off and no `scalability.md` is present in round 1.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Green marker write is placed where 2g's no-candidate path skips it | CLOSED | spec.md:186 puts the write as Phase 3's first sentence and says 2g is not edited; the Design has no 2g bullet. `skills/spec-cycle/SKILL.md:689` (no-candidate exit) and step 5 both fall into Phase 3 (`:703`), so every green run reaches the write. Decision 3 item 2 (spec.md:60) and the checklist row (spec.md:235) agree with that position. |
| correctness | F-2 (P1) | `Spec verdict:` line "placed first" collides with Phase 5's "replace the first bullet" rule | CLOSED | spec.md:196 places the line directly above `Review gate:`; `skills/ship-spec/SKILL.md:305`–`:308` keeps the test-command bullet first, so the `N/A` rule still hits the right bullet. |
| correctness | F-3 (P2) | Red halt block called "three-line"; sentence does not fit /spec-tickets | PARTIAL | spec.md:144 now says "Decision 6's red block" and gives the `/spec-tickets` second line. spec.md:239 still says "the three-line block" (the block at spec.md:122–125 is four lines). See F-3. |
| correctness | F-4 (P2) | Marker H1 contains `verdict:` | CLOSED | spec.md:43: key at the start of the line; the heading is not a field. Carriage of that rule to the readers is F-2 below. |
| correctness | F-5 (P2) | /ship-spec Design does not carry the fingerprint rule | CLOSED | spec.md:193. |
| correctness | F-6 (P2) | /spec-tickets Phase 0 summary specified two ways | CLOSED | spec.md:147 and spec.md:204 now both print the full verdict line. |
| correctness | F-7 (P2) | Phase 4 re-check compares "state or kind" | CLOSED | spec.md:156: "the verdict line it would now print differs from the line that was printed". |
| correctness | F-8 (P2) | Failed pending write has no print site | CLOSED | spec.md:65: printed at once, before round 1, naming the marker on disk. |
| correctness | F-9 (P3) | Phase 3 `Verdict:` line is unconditional | PARTIAL | spec.md:67 adds the `marker NOT written` form. No form for `fingerprint: none`; Decision 2's separate `fingerprint not computed` line (spec.md:55) covers it. P3, no action needed. |
| correctness | F-10 (P3) | Usage line names `<brief-path>` | DEFERRED (P2+) | spec.md:282. See F-1 for what remains inconsistent. |
| correctness | F-11 (P3) | Test command checks `requires:` on two skills | CLOSED | spec.md:253 final clause lists all three skill files. |
| correctness | F-12 (P3) | `unreadable` misses absent `ticket:` / `fingerprint:` | CLOSED | spec.md:104, :108. |
| edge-cases | F-1 (P2) | Failed pending write is silent | CLOSED | spec.md:65. |
| edge-cases | F-2 (P2) | Attest: no outcome on failed write; no directory create | CLOSED | spec.md:93. |
| edge-cases | F-3 (P2) | Phase 3 prints green path when the write failed | CLOSED | spec.md:67. The `fingerprint: none` sub-case is covered by Decision 2's own line. |
| edge-cases | F-4 (P2) | Prompts do not define other replies | CLOSED | spec.md:92, :136: any reply other than `1` is treated as 2. |
| edge-cases | F-5 (P2) | Row precedence; green marker with unusable fingerprint or source | PARTIAL | (a) and (b) closed: spec.md:99 (first match wins), spec.md:108 (absent or `none`). (c) a green marker with no usable `source:` is not placed. See F-6. |
| edge-cases | F-6 (P2) | /spec-tickets prints plain green for `fingerprint: none` | PARTIAL | spec.md:142 now states the `/spec-tickets` reading explicitly. spec.md:55 still says such a marker "reads downstream as the changed-spec case" with no scope. See F-4. |
| edge-cases | F-7 (P3) | Leave-alone check compares against a moving `origin/main` | PARTIAL | The third-skill half is closed (spec.md:253). The `merge-base` half is neither folded nor listed in `## Deferred (P2+)`. See F-10. |
| edge-cases | F-8, F-9, F-10 (P3), F-11 (P4) | Rename, attest fingerprint timing, POSIX example, discarded reason | DEFERRED (P2+) | spec.md:275–278. |
| conventions | F-1 (P2) | Classification table and parse rule have no home; copies unpinned | PARTIAL | Table: closed (spec.md:181 `### Reading the marker`, canonical; spec.md:243 pins the copies). Reader parse rule is still placed only in `/spec-cycle`. See F-2. |
| conventions | F-2 (P2) | Three spellings of the attest invocation | PARTIAL | spec.md:71 now fixes one spelling "everywhere"; spec.md:180 and spec.md:125 still spell it two other ways. See F-1. |
| conventions | F-3 (P2) | `/spec-tickets` keeps "Green-lit check" for the heading check | CLOSED | spec.md:202. No other file uses either label (repo grep: only `skills/spec-tickets/SKILL.md:35`, `:176`). |
| conventions | F-4 (P2) | 2f-i clause position | CLOSED | spec.md:185; matches `skills/spec-cycle/SKILL.md:663`–`:665`. |
| conventions | F-5 (P2) | Test command guards two skills' frontmatter | CLOSED | spec.md:253. |
| conventions | F-6 (P2) | Failed-write rule unmarked as a spec-level addition | CLOSED | spec.md:65 ("a spec-level rule; the brief does not state one"); spec.md:67 gives the failed form of the `Verdict:` line. |
| conventions | F-9 (P3) | Tool-use notes updated for `/spec-cycle` only | CLOSED | spec.md:194, :208. |
| conventions | F-7, F-8, F-10, F-11 (P3) | Spec-level additions list; headless stop vs VHS-46; heading list restated; prose hash command | DEFERRED (P2+) | spec.md:279–281. |

No REOPENED items. Both manifest lines verify as `fixed`.

## Findings

### F-1: The attest invocation is still spelled three ways, against the spec's own "written the same way everywhere"
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:180 (Design, Invocation line) vs spec.md:71 (Decision 4); also spec.md:125
**Convention violated:** Naming consistency; the sibling usage idiom gives one line that is also the halt text (`skills/spec-brief/SKILL.md:30`, `skills/spec-tickets/SKILL.md:27`). Residual of conventions R1 F-2.
**Evidence:** Decision 4: "Invocation, written the same way everywhere: `/spec-cycle <brief-path> [--attest "<reason>"]`." Design, eleven lines of intent later: "`Invoked as: /spec-cycle <brief-path>` gains a second form: `/spec-cycle <path> --attest "<reason>"`". The red halt block prints `/spec-cycle <spec-path> --attest "<reason>"`. An implementer following the Design bullet writes `<path>` on the skill's own invocation line, which Decision 4 forbids.
**Suggested fix:** Replace the Design bullet at spec.md:180 with: "**Invocation line.** `Invoked as: /spec-cycle <brief-path>` becomes `Invoked as: /spec-cycle <brief-path> [--attest "<reason>"]`, with one sentence: with `--attest` the path may be the spec path; see `## Attest mode`." Leave spec.md:125 as is; it is a concrete instance for an operator who is holding a spec path, and Decision 4's first sentence already allows it.

### F-2: The reader's parse rule is placed only in the skill that writes the marker
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:193 (Design, `/ship-spec` step 1b), spec.md:203 (Design, `/spec-tickets` step 4); rule at spec.md:43
**Convention violated:** The spec's own stated rule, "a skill is read alone" (spec.md:181), and the restate-identically pattern it applies to the table and the fingerprint. Residual of conventions R1 F-1.
**Evidence:** The rule "key at the start of the line … the `# Spec verdict:` heading is not a field … a reader takes the first line for each key and ignores anything else" is one of Decision 1's field rules, which the Design places in `/spec-cycle`'s `## The verdict marker`. `/ship-spec` carries "Decision 5's table and Decision 2's fingerprint rule"; `/spec-tickets` carries the table. Neither carries the parse rule, and they are the two readers. A reader matching `verdict:` anywhere on a line reads the H1 and lands on `unreadable` for every marker (correctness R1 F-4's case).
**Suggested fix:** At spec.md:193 change "carrying Decision 5's table and Decision 2's fingerprint rule" to "carrying Decision 1's reader rule (a field line starts with its key; the first line for each key wins; the heading is not a field), Decision 5's table, and Decision 2's fingerprint rule". At spec.md:203 add "and Decision 1's reader rule" after "carrying Decision 5's table without the `changed` row". Add to the checklist row at spec.md:243: "and each reader states the field-line rule."

### F-3: The Test plan still calls the red block "three-line"
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:239 (Test plan checklist)
**Convention violated:** Internal naming consistency. Residual of correctness R1 F-3, which was fixed in Decision 7 only.
**Evidence:** "red halts with the three-line block". The block at spec.md:122–125 has four lines, and Decision 7 now calls it "Decision 6's red block".
**Suggested fix:** Change "red halts with the three-line block" to "red halts with the red block".

### F-4: Decision 2 still says a `fingerprint: none` marker reads as changed "downstream", which Decision 7 contradicts for `/spec-tickets`
**Severity:** P2
**Where:** spec.md:55 (Decision 2) vs spec.md:142 (Decision 7)
**Convention violated:** Internal consistency between two decisions. Residual of edge-cases R1 F-6.
**Evidence:** Decision 2: "A green marker with `fingerprint: none` reads downstream as the changed-spec case." Decision 7: "a `verdict: green` marker is always `green` here and never `changed`, including one whose `fingerprint:` is `none`". Decision 7 is the explicit and later statement, so the intent is clear; the Decision 2 sentence is the one that goes into `## The verdict marker` verbatim. Not tagged for 2g because the edit is inside a Decision.
**Suggested fix:** In spec.md:55 change "reads downstream as the changed-spec case" to "reads in `/ship-spec` as the changed-spec case; `/spec-tickets` does not look at the fingerprint (Decision 7)".

### F-5: The failed green write is given a print position inside a template the skill renders verbatim, and the Design does not add it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:65 (Decision 3) vs spec.md:186 (Design, Phase 3)
**Convention violated:** The Phase 3 output is a verbatim template (`skills/spec-cycle/SKILL.md:705`: "render this output verbatim"); a line that appears inside it has to be in the template.
**Evidence:** Decision 3 says the failure line is printed "at once, where the write was attempted" and then, for the green write, "under the SPEC READY header". The write is Phase 3's first sentence, before the template prints, so those are two different positions. The Design bullet says only "The output template gains the `Verdict:` line", and spec.md:67 already gives that line a failed form. An implementer has three candidate places for one message.
**Suggested fix:** Extend the Design bullet at spec.md:186: "The output template gains the `Verdict:` line in its two forms (Decision 3). When the green write failed, the `verdict marker NOT written: …` line is printed directly under the `=== SPEC READY` header line; that conditional line is shown in the template with a render-only-when note, the way the Scale block is."

### F-6: A green marker with no usable `source:` has no kind to print
**Severity:** P2
**Where:** spec.md:104–110 (Decision 5)
**Convention violated:** None of the repo's; carried PARTIAL from edge-cases R1 F-5 (c). Listed so the count is honest.
**Evidence:** "`green` carries its kind: `review, round <n>` or `operator-attested`." A marker with `verdict: green`, a matching fingerprint, and `source:` absent or neither value passes as `green` with nothing to put in `green (<kind>, <date>)` or in the PR-body line that brief Decision 7 requires to say which kind it was. Not tagged for 2g because the edit is inside a Decision.
**Suggested fix:** Add to the `unreadable` row at spec.md:104: "or it is `verdict: green` and its `source:` line is absent or is neither of the two values".

### F-7: The marker is the first file in the reviews tree that is rewritten in place; the spec does not say how that sits with the immutable-artifacts decision
**Severity:** P3
**Where:** spec.md:26 (Decision 1), spec.md:162 (Decision 8)
**Convention violated:** None; brief Decisions 1 and 13 choose the directory and the overwrite. Flagged so the wiki record stays coherent.
**Evidence:** `decisions/2026-08-09-review-round-artifacts-are-immutable.md:22`: "Review-round artifacts are never edited after their round closes." The other non-round file in that tree is append-only (`skills/spec-cycle/SKILL.md:664`: "never overwrites a prior `grill.md`"). `verdict.md` is replaced whole on every write, and only an attested marker keeps a trace of what it replaced. After `/spec-close` it sits at `DONE/<TICKET-ID>/reviews/verdict.md` with a `spec:` field naming a `TODO/` path that no longer exists.
**Suggested fix:** One sentence in Decision 8: "`verdict.md` is current state, not a round artifact: it is rewritten in place, the round reports beside it stay immutable, and once archived its `spec:` path is historical."

### F-8: Attestation is an unverified operator claim that passes like a verified one; VHS-36 prohibited that shape elsewhere and the spec does not distinguish the two
**Severity:** P3
**Where:** spec.md:69–95 (Decision 4), spec.md:110 (Decision 5)
**Convention violated:** None; brief Decisions 5 to 7 authorize it. Same kind of note as round 1's F-8.
**Evidence:** `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md:35`: "Rejected — `source: operator` as a legal established source. An unchecked operator claim becomes an axiom every downstream lens trusts". This spec writes `source: operator-attested` and "Both pass the same way". The subjects differ (a fact inside a brief that reviewers treat as authority, versus a labelled verdict whose kind is printed in preflight and in the PR body), and the label is what answers VHS-36's objection, but the spec does not say so.
**Suggested fix:** One sentence in Decision 4 or in `## Deferred (P2+)` beside the VHS-46 note: "VHS-36 prohibits an unverified operator claim as an established fact because nothing downstream can tell it from a verified one. An attested verdict is labelled at every read (Decision 5's kind, the PR-body line), so it is never mistaken for a reviewed one."

### F-9: Spec-level additions new in round 2, for the drift check
**Severity:** P3
**Where:** spec.md:202, :92, :136, :142
**Convention violated:** None. Class (c) items; the list at spec.md:279 predates them.
**Evidence:** (1) `/spec-tickets` step 3 is relabelled "Heading check" and its failure mode "Spec incomplete"; rationale given in place. (2) "Any reply other than `1` is treated as 2" in both new prompts; `/spec-tickets`' own block is stricter in wording (trim; empty reply and timeout named, `skills/spec-tickets/SKILL.md:122`–`:125`) but the effect is the same. (3) `/spec-tickets` reads a `fingerprint: none` green marker as green; follows from brief Decision 16.
**Suggested fix:** Append the three to the conventions/R1/F-7 line in `## Deferred (P2+)`.

### F-10: The moving-`origin/main` half of edge-cases R1 F-7 is neither folded nor recorded
**Severity:** P3
**Where:** spec.md:253 (Test command); `## Deferred (P2+)`
**Convention violated:** `skills/spec-cycle/SKILL.md:441`: P2+ items "are carried forward as spec notes in the `## Deferred (P2+)` section".
**Evidence:** The command still diffs against `origin/main` (the form VHS-46 used). The deferred list names edge-cases F-8 to F-11 and not F-7.
**Suggested fix:** Add: "edge-cases/R1/F-7 — the leave-alone check diffs against `origin/main`, not the merge base; a fetch after another merge can fail it for unrelated files. Left: same form as VHS-46."

### F-11: Scope rows do not name every edit the Design makes
**Severity:** P4
**Where:** spec.md:11–13
**Convention violated:** None; the rows are per file and every file is listed.
**Evidence:** Row 1 says "Green write after 2g" and omits the 2d sentence (the write is in Phase 3, spec.md:186). Row 2 omits `/ship-spec`'s Tool-use notes bullet (spec.md:194). Row 3 omits the step 3 relabel and the Tool-use notes bullet (spec.md:202, :208).
**Suggested fix:** Row 1: "Green write at the start of Phase 3. One sentence in 2d." Row 2: add "Tool-use notes entry." Row 3: add "Step 3 relabelled. Tool-use notes entry."

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 4 | P4: 1

STATUS: GREEN
