# Conventions Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: Irreversible reinstates a rejected VHS-46 halt and drops its review-file record
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8; spec § ship-spec, Phase 3b
**Convention violated:** Active wiki decision `decisions/2026-10-08-vhs-46-ship-spec-review-gate-declared-one-pass.md` (status: active). The spec changes the skill sentence and does not name the decision it overturns.
**Evidence:** That decision rejects "Halt when a declared review is unavailable" because "a headless run without the plugin would stop every time," and chooses: "No command declared is a skip with a PR-body line; a declared command that is unavailable or fails is a skip recorded in the review file as well. A skip never blocks the commit." `skills/ship-spec/SKILL.md:432-433` still says those two cases "Never halt" and that the failed case is "skip and record, with the first 20 lines of the error text in the review file." The spec only amends the `:183` "skip never blocks" sentence, says `:432-433` stay as written for `big` and an absent line, and for `irreversible` says "Write no review file and do not start Phase 4."
**Suggested fix:** In Decision 8, say this supersedes that VHS-46 rule for `irreversible` only (brief Decision 8: a skipped gate must not commit), and that `small`, `big`, and an absent line keep it. On the unavailable and failed halts, still write today's skipped-form review file (command, case, first 20 lines of error) before stopping; keep no file only for the no-command case, which writes none today. Add failure-mode bullets so `:432-433` are not an unconditional "Never halt."

### F-2: Basis-line template does not generate the normative examples
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 14, basis line
**Convention violated:** The pinned contract (brief Risk 2) is two shapes at once. Checklist item 1 gates the examples.
**Evidence:** The template is `basis: <n> files (<paths>) | files: unknown, ~<m> lines | lines: unknown, surfaces: none | <surface> | surfaces: unknown — ticket text + grounding | never tweak`. The normative example is `basis: 1 file (README.md), ~1 line, surfaces: none — ticket text + grounding`. Example 2 is known files plus `lines: unknown` plus `surfaces: config`, a combination the pipe sketch does not show. Singular "1 file" / "~1 line" and comma separators are only in the examples.
**Suggested fix:** Delete the pipe sketch. State the line as three comma-separated slots (files, lines, surfaces) plus the suffix rule already there, with singular when the count is 1, and keep the three examples as the exact strings.

### F-3: Tweak-surfaces "then" reads as first-wins, but the next sentences union both files
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 14, Extension
**Convention violated:** Instruction-file fallback in this repo is first source wins. `skills/ship-spec/SKILL.md:71-73`: "Take the first source that yields one" — `CLAUDE.md`, then `AGENTS.md`. `AGENTS.md` § Machine-local config: tracked instructions live in `AGENTS.md`; `CLAUDE.md` is the gitignored local file.
**Evidence:** The spec says "The target project's `AGENTS.md`, then `CLAUDE.md` when that file exists," then "No heading in either file means the built-in four only. Extra signals only add surfaces." "Then" is the review-command idiom (and the order is reversed). "Either" and "only add" describe a union. A first-wins reading hides one file's signals.
**Suggested fix:** Say both files are read when present; a `## Tweak surfaces` body in each contributes; signals union and neither heading hides the other; this is not the review-command order. Say the body runs to the next `^#{1,6}` heading, same as the `## Tier` / `## Scale` section rule.

### F-4: Workflow-reference cap and gate sentences stay literal after the ladder edit
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Docs and AGENTS.md (`docs/spec-workflow-reference.md`)
**Convention violated:** VHS-15 reconciled every default-three / optional-fourth sentence in this doc rather than leaving a heading that contradicted the body (`decisions/2026-06-16-vhs-15-optional-scalability-lens.md`, reversal cost). The spec's own new section would contradict sentences it does not list.
**Evidence:** The spec rewrites only `:84-86` and `:246`. Still hardcoded: `:66` "Parallel review loop (up to 4 rounds)", `:27` "post-round-4 halt menu", `:102` "red at the round-4 halt". `:187` still says a missing command is a skip and an unavailable or failed command "is also skipped, and recorded," with no irreversible exception.
**Suggested fix:** Point those four sites at `round_cap` (grilling's own cap of 3 stays where it is the interview). Add one clause to the Phase 3b paragraph: `irreversible` halts on the three skip cases and does not commit; `big` and an absent tier keep the skip.

### F-5: A near-miss Tier heading halts; Scale's near-miss only warns
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § spec-cycle, Parse step 1
**Convention violated:** Silent addition. Brief Decision 12 says duplicates warn "as Scale does" and a bad value on a present section halts. It does not mention a non-matching heading. Scale's near-miss (`skills/spec-cycle/SKILL.md:299-304`) warns and stays off; it does not halt the run.
**Evidence:** "A heading that matches the looser `^#{1,6}\s+tier\b` and whose body contains a `**Level:**` line is malformed: halt. A looser heading with no `**Level:**` line is ignored." `## Tier list` plus a Level line would halt and write no marker. The same shape under Scale warns and continues.
**Suggested fix:** One sentence that this is stricter than Scale on purpose: a near-miss with a Level line must not be read as absent, because absence is `big` and could downgrade an intended `irreversible` (brief Decision 12). Scale can warn-and-stay-off because off is its safe direction.

### F-6: Decision 14 pins past Risk 2
**Severity:** P3
**Where:** spec § Decision 14
**Convention violated:** Spec-level additions. Brief Risk 2 asks the author to pin the estimate's source, the basis line, a surface taxonomy, one extension point, "never recommend tweak" when the estimate is unknown, and two or three examples. It does not pin the items below.
**Evidence:** "The heuristic never recommends `small` or `irreversible`." A single typo, wording replacement, or identifier rename "estimates at 1 line." An extension signal "matches a named path as a substring," while a built-in path signal matches "a path segment or a filename."
**Suggested fix:** Keep them, but label each as a spec pin beyond Risk 2. For the path match, say the substring is deliberate (a project signal is not limited to one path segment), so it is not read as the built-in segment rule.

### F-7: README still states a fixed 4-pass loop
**Severity:** P3
**Where:** spec § Scope, leave-alone list
**Convention violated:** None that the brief requires changed. `README.md:10` is the tracked user-facing lifecycle line ("until findings clean or 4 passes complete"). VHS-17 put discoverability in `README.md` because `CLAUDE.md` is gitignored. The brief's scope table does not list `README.md`.
**Evidence:** The spec leaves `README.md` alone while `AGENTS.md:27` is updated to `round_cap`. After this ships, the two tracked intros disagree.
**Suggested fix:** Either one phrase in the leave-alone note that `README.md:10` stays the `big` maximum and is not updated, or add that one sentence to the doc edits. Do not expand further into `README.md`.

## Summary
P0: 0 | P1: 0 | P2: 5 | P3: 2 | P4: 0

STATUS: GREEN
