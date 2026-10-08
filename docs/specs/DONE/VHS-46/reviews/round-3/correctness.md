# Correctness Review — round 3

Grounding performed: spec and brief read fresh from disk; machine-local `CLAUDE.md`; `skills/ship-spec/SKILL.md` (whole file); `tests/test_lint.py:48-56`; heading maps of `docs/customizing.md`, `docs/spec-workflow-reference.md`, `AGENTS.md`; `README.md:12`; `skills/spec-close/SKILL.md:340` (companion rule); tracked file list under `tests/` and `skills/`; repo-wide search for `bloat-check` and `ponytail` outside `docs/specs/`; line endings of the six edited files; the three round-2 reports. Ticket lookup skipped per orchestrator note (ACL on namespace `skills`); the brief is used as the ticket text.

`git log -10` on the seven touched files: the newest commit is still 1bd3f29 (2026-10-08, VHS-45), surfaced in round 1. Nothing has landed since. Anchors re-checked and matching: `skills/ship-spec/SKILL.md:17` (step 3 reads `CLAUDE.md` only), `:20` ("proceed directly to Phase 4 (commit)"), `:94` (Phase 3), `:114-129` (Phase 3 halt block: more iterations / manual debug / roll back and re-spec), `:131` (Phase 4), `:135` (explicit staging), `:195-201` (PR body Test plan block), `:241` (Phase 7 `Tests:` line); `tests/test_lint.py:52-53` (`len(skills), 12,` and "12 currently-shipped"); `docs/customizing.md:7` and `:51`; `docs/spec-workflow-reference.md:174` and `:180`; `AGENTS.md:31`, `:63`, `:86`; `README.md:12`. Twelve skill directories are tracked, so 11 after the delete is right. `ponytail` and `bloat-check` appear in no tracked file outside `docs/specs/` except `skills/bloat-check/SKILL.md` itself, so the test command's last clause passes after the delete. All six edited text files are LF in index and working tree (`eol=lf`), so the `$`-anchored heading grep in the test command matches.

Deferred findings: the spec has no `## Deferred — follow-up required` section, so there are no `D-<n>` rows, no preamble, and nothing to validate under the routing rules. Its `## Deferred (P2+)` section (spec.md:276-285) is the informal list of P2-and-below items; it holds no P0 or P1.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Override at the second halt has no defined outcome, and its printed text says "commit" while the tests are red | CLOSED | Reworked, deliberate direction change with rationale. spec § Decision 9, spec.md:120: "There is no second review halt and Decision 8's block is not printed again"; a red loop ends in "Phase 3's own halt block ... with one added line naming the finding whose fix is being held"; "Nothing is committed until the tests are green." The override option is therefore never offered while tests are red, which removes the contradiction with spec.md:118 and brief decision 15 (brief.md:43, "the same halt menu"). Checklist row at spec.md:244 matches. No other section still refers to a second halt (Decision 8 "stop once" at spec.md:98, Phase 3b steps 6-7 at spec.md:182-183, Failure modes at spec.md:200 all agree). Manifest claim verified at both named sites. Phase 3's halt block exists as cited (`skills/ship-spec/SKILL.md:114-129`). |
| correctness | F-2 (P2) | Review record cannot count an unresolved Blocks finding; two header fields have no value on a skip | PARTIAL | (a) closed: `<un> unresolved` at spec.md:136. (b) closed: `Mode` and `Compared against` omitted on a skipped run, spec.md:147. (c) open: `overridden by operator` still takes no reason, and Decision 9 now requires one. See F-1 below. |
| correctness | F-3 (P3) | Scope row for `docs/customizing.md` omits the second edit | CLOSED | spec § Scope, spec.md:14: "`## Spec & brief layout` gains the review file's path." |
| correctness | F-4 (P3) | Four round-1 P3/P4 items neither folded nor listed | CLOSED | spec § Deferred (P2+), spec.md:285 lists all four; the `mode: inline` nit is settled at spec.md:147 ("`Mode:` is the only spelling"). `tests/fixtures` stays out of the diff list, acknowledged there. |
| edge-cases | F-1 (P2) | "Override" at the second stop has no stated outcome | CLOSED | Same rework as correctness F-1; the second stop no longer exists (spec.md:120). |
| edge-cases | F-2 (P3) | Unusable Blocks finding has no stated group tag or count | CLOSED | spec § Decision 10, spec.md:147: "An unusable finding labelled as a blocker is tagged `Blocks` and counted there." |
| edge-cases | F-3 (P3) | Halt option 1 marks every listed finding as fixed by operator | DEFERRED | spec.md:285 (informal list) |
| conventions | F-1 (P2) | The second halt reuses Decision 8's menu | CLOSED | Same rework; spec.md:120. |
| conventions | F-2 (P2) | Review-record residue from two round-1 P2s | CLOSED | (a) spec.md:136; (b) spec.md:147; (c) "A `vetoed` finding counts as recorded in the `Fix or record` line", spec.md:147; (d) spec.md:147. (e) The record reasons still live in two places, but Decision 9 cross-references Decision 8's list explicitly (spec.md:120), so a reader is not misled. |
| conventions | F-3 (P3) | Review-command resolution reads two files; docs describe one | PARTIAL | Not folded at spec.md:206 and not in the Deferred (P2+) list, although the manifest note says the remaining P3/P4 are listed. See F-3 below. |
| conventions | F-4 (P3) | Scope row for `docs/customizing.md` omits the second edit | CLOSED | spec.md:14. The hardcoded-paths sentence at `docs/customizing.md:60` is not named; the Design bullet at spec.md:206 is the fuller statement. |
| conventions | F-5 (P3) | Spec-level additions listed for the drift check | CLOSED | No action was asked. Item (4), the second operator stop, is now removed. |
| conventions | F-6 (P4) | Four round-1 P3/P4 items unchanged and unlisted | CLOSED | spec.md:285 |

No finding is REOPENED. The manifest line holds as stated: reworked, two sites, both verified.

## Findings

### F-1: `overridden by operator` has no place for the reason Decision 9 now requires
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 9, spec.md:120, against § Decision 10, spec.md:144, and § Decision 8, spec.md:112
**Claim:** "the finding is recorded as `overridden by operator` with the reason `fix broke <test>`" (spec.md:120), and the template's "Disposition: fixed | fixed by operator | overridden by operator | unresolved | vetoed: <reason> | recorded: <reason> | not acted on" (spec.md:144).
**Why this is wrong:** The template gives `vetoed` and `recorded` a `: <reason>` suffix and gives `overridden by operator` none. Decision 9 is the first place the spec asks for a reason on that value, so the implementer has a rule with no field to carry it. The same gap is the unfolded part (c) of correctness/R2/F-2: a Blocks finding overridden at Decision 8's halt loses the reason it was unresolved (for example the veto reason Decision 7 says is recorded, spec.md:90), because its one disposition slot is taken by `overridden by operator`. The code block and the prose disagree only on a suffix, and the code runs either way, so this is P2.
**Suggested fix:** In the template at spec.md:144, change `overridden by operator` to `overridden by operator: <reason>`. Add one sentence after spec.md:147: "The reason on an overridden finding is why it was unresolved (Decision 8), or `fix broke <test>` (Decision 9)."

### F-2: The Design does not say where Decision 9's added halt line and its two fix-holding rules go in the skill text
**Severity:** P3
**Where:** spec § Design, spec.md:183 and spec.md:188, against § Decision 9, spec.md:120, and § Scope, spec.md:11
**Claim:** "Phase 3's own halt block applies, with one added line naming the finding whose fix is being held." The Design's only Phase 3 edit is "**Phase 3 intro.** One sentence added" (spec.md:188), and step 7 reads "Re-run the tests when Decision 9 says so" (spec.md:183).
**Why this is wrong:** After the rework, three rules act inside Phase 3's loop and halt: a Blocks fix is held, the halt block gains a line, and a fix removed from the manual-debug option becomes `overridden by operator`. The Design lists no edit to Phase 3's loop or halt block (`skills/ship-spec/SKILL.md:98-129`), and the Scope row for the file names neither the Phase 3 intro sentence nor the step 4.1 text change the Design does make. An implementer can place the three rules in Phase 3b step 7, which is the reading the step's cross-reference supports, so nothing is lost; the spec just leaves the placement to them.
**Suggested fix:** Extend Design step 7 at spec.md:183: "Re-run the tests when Decision 9 says so. This step carries Decision 9's rules for the re-entered loop (the held Blocks fix, the added halt line, the two reverted-fix dispositions); Phase 3's own loop and halt block are not edited." Add "Phase 3 intro and Phase 0 step 4.1: one sentence each." to the Scope row at spec.md:11.

### F-3: conventions/R2/F-3 is neither folded nor listed as deferred
**Severity:** P3
**Where:** spec § Design, spec.md:206; § Deferred (P2+), spec.md:276-285
**Claim:** Manifest note: "remaining P3/P4 listed in `## Deferred (P2+)`."
**Why this is wrong:** The new `docs/customizing.md` section sits under `## What to put in your CLAUDE.md` (`docs/customizing.md:5`), and the Design text does not say the `## Review command` section is also read from `AGENTS.md`, or that `CLAUDE.md` wins when both declare one (Decision 2 item 2, spec.md:34). The item is absent from the Deferred (P2+) list. It does not gate.
**Suggested fix:** Add to spec.md:206 after "the spec-level override;": "that the section is read from `CLAUDE.md` first and `AGENTS.md` second;". Or add one Deferred (P2+) line naming conventions/R2/F-3.

### F-4: The hold rule covers a fix the gate applied, not one the operator made by hand
**Severity:** P3
**Where:** spec § Decision 9, spec.md:120, against § Decision 8, spec.md:112
**Claim:** "a fix the gate applied for a Blocks finding is not undone to get the tests green."
**Why this is wrong:** After halt option 1 the finding is `fixed by operator` and the loop is re-entered (spec.md:118). The hold rule names only gate-applied fixes, so read literally the loop may undo the operator's hand fix and still record `fixed by operator`. The closing sentence, "The dispositions in the review file describe the tree that is committed", points the right way, and a careful agent will not undo an operator's edit, so this is a wording gap.
**Suggested fix:** Change the sentence to: "a fix for a Blocks finding, whether the gate applied it or the operator made it by hand, is not undone to get the tests green."

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 0

STATUS: GREEN
