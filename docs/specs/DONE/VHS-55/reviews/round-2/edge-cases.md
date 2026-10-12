# Edge-Cases Review — round 2

## Closure of round 1 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Looser Tier heading rule halts every valid `## Tier` section | CLOSED | spec § spec-cycle brief parse step 1, lines 173–174: looser rule only when no strict heading matched; a second strict heading is not a near-miss |
| correctness | F-2 | Malformed-brief halt runs before the re-run pin | CLOSED | spec § Re-run pin, lines 168–172; brief parse runs only when the pin did not take a valid line; Done when line 298 |
| correctness | F-3 | A non-bare `**Tier:**` line is read as absent and becomes `big` | CLOSED | spec § Reader rule, line 180: label is case-insensitive; any other value halts and is not `big` |
| correctness | F-4 | Irreversible "re-run /ship-spec" cannot resume the worktree it just created | DEFERRED | D-1, lines 320–329, well-formed (P1, preamble present, seven fields, blockquoted fix, two existing sites) |
| correctness | F-5 | Post-cap Confirm still offers only options 1 and 3 | CLOSED | spec § Confirm, line 154: post-cap menu is 1, 3, and 4; invalid re-ask does not discard the interview |
| correctness | F-6 | Tweak-floor match mode and basis line are not pinned tightly enough | CLOSED | spec § Decision 14, lines 92–113: segment/filename equality, union, comma-separated basis matching the examples |
| correctness | F-7 | `round_cap` rewrite leaves literal cap-of-4 sentences in force | CLOSED | substitution table lines 186–213 includes 672 and 646; docs paragraph line 270 names `:66`, `:27`, `:102`; AGENTS `:25` |
| correctness | F-8 | Ship-spec's other copies of the gate contract stay unconditional | CLOSED | spec § ship-spec, lines 234, 241, and 255: canonical table stays fingerprint-only; `N/A` unchanged; `:432–433` gain the exception |
| correctness | F-9 | ticket not cached | CLOSED | spec § Deferred (P2+), line 314: brief is the record. This round's `memory_search` on namespace `skills` was access denied again; not a spec defect |
| conventions | F-1 | Irreversible reinstates a rejected VHS-46 halt and drops its review-file record | CLOSED | Decision 8, line 60, supersedes VHS-46 for `irreversible` only; Phase 3b lines 243–255 write the skipped-form file on unavailable and failed |
| conventions | F-2 | Basis-line template does not generate the normative examples | CLOSED | spec § Decision 14, lines 105–113: three comma-separated slots; examples match |
| conventions | F-3 | Tweak-surfaces "then" reads as first-wins | CLOSED | spec § Decision 14, line 102: both files, union, not the review-command order; body runs to the next heading |
| conventions | F-4 | Workflow-reference cap and gate sentences stay literal | CLOSED | spec § Docs, line 270: `:66`, `:27`, `:102`, `:84–86`, `:246`, and `:187` |
| conventions | F-5 | A near-miss Tier heading halts; Scale's near-miss only warns | CLOSED | spec line 174: stricter than Scale on purpose; do not warn-and-continue |
| conventions | F-6 | Decision 14 pins past Risk 2 | CLOSED | lines 87, 89, and 102 labeled `spec pin beyond Risk 2` |
| conventions | F-7 | README still states a fixed 4-pass loop | CLOSED | spec § Scope leave-alone, line 24: `README.md:10` stays the big-tier maximum |
| edge-cases | F-1 | Malformed-brief halt and the re-run pin cannot both be true | CLOSED | same partition as correctness F-2, lines 168–172 and 298 |
| edge-cases | F-2 | A near-miss `**Tier:**` line is read as absent `big` | CLOSED | reader rule line 180, used by attest, the re-run pin, and ship-spec |
| edge-cases | F-3 | A clean irreversible review is specified as the failed halt | DEFERRED | D-2, lines 331–340, well-formed. Phase 3b lines 243 and 254 still halt on "nothing readable" and succeed only on "readable findings" |
| edge-cases | F-4 | Irreversible re-run stops on the leftover worktree | CLOSED | halt text lines 248–250 names `<worktree-path>`, `<branch>`, and that a re-run does not resume Phase 3b. The missing resume path stays D-1 |
| edge-cases | F-5 | Failure-mode bullets still say a failed review never halts | CLOSED | spec line 255 |
| edge-cases | F-6 | At `round_cap = 2`, FROZEN ignores the round that reviewed the revision | CLOSED | substitution row for line 555, spec line 202: current round forces REWRITE |
| edge-cases | F-7 | `round_cap = 2` leaves the grill-apply rules and the grilling cap bound to the wrong 4 | CLOSED | line 213 (skill line 672) and line 213's grilling clause (skill line 646 passes literal 3) |
| edge-cases | F-8 | Quoted multi-word surface signals do not match a "whole word" check | CLOSED | line 93 phrase rule; example 4, line 113 |
| edge-cases | F-9 | `small` plus `Test command: N/A` drops both gates | CLOSED | spec line 241: `N/A` still skips Phase 3 for every tier; `small` still skips Phase 3b |
| edge-cases | F-10 | A fenced `**Level:**` line in the brief becomes the tier | CLOSED | brief parse step 2, line 175: fenced lines ignored |
| edge-cases | F-11 | Confirming a tier mismatch ships the absent-line tier, not the marker | PARTIAL | confirm half folded at lines 232–233. Attest already-green return stays (line 221); § Deferred (P2+) line 313 records that on purpose |
| edge-cases | F-12 | Plane ticket body was not readable | CLOSED | spec line 314. Lookup this round returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`; review used the brief |

## Findings

### F-1: A brief `**Level:**` line with trailing text is accepted as its first token
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § spec-cycle brief parse step 2, line 175; contrast spec § Reader rule, line 180
**Edge case:** The brief's `## Tier` section has one unfenced line `**Level:** small | big | irreversible`, or `**Level:** small — actually irreversible`, or a mid-line mention `values: **Level:** small` before the real line. Same shape with the token `irreversible` is not this hole.
**What happens:** The regex captures the first `\S+` and does not require the rest of the line to be empty. `small | big | irreversible` is `small` with no "multiple Level lines" warning. `round_cap` is 2 and ship-spec skips the review gate. The spec reader, attest, and ship-spec halt on that same shape (`trailing note` or punctuation). A grammar paste therefore takes the tier that drops the gate, while the identical junk on `**Tier:**` halts.
**Why the spec misses it:** Step 2 halts only when the captured token is empty, `tweak`, or unknown. Trailing words are defined out of the token. Decision 12's "unknown token halts" is applied to that capture, not to the whole line.
**Suggested fix:** After the token, require the rest of the line to be empty, and anchor the match at the start of the line after indentation, same as the spec label. Otherwise halt `tier: malformed (<line>)`. A fenced example still does not count.

### F-2: Any integer in the ticket overrides the 1-line estimate
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 14, line 89
**Edge case:** The ticket is not the single-typo example. It names one file, states no line count, and contains some other integer: a ticket id, a date, "see item 2", or "3 call sites". Or it states two numbers, such as "3 functions, about 80 lines".
**What happens:** "An integer the texts state" matches the unrelated number, and "a stated number wins over that 1-line estimate." There is no rule for which integer when several appear. Using `2` from "item 2" makes lines `~2`, which is under 50, so a one-file change with `surfaces: none` is recommended `tweak` even when the diff was never sized. Using `80` recommends `big`. Checklist item 1 cannot catch this; all four examples have either no extra integer or a single explicit line count.
**Why the spec misses it:** The line rule does not say the integer must be a line or diff count, and it does not say which number wins.
**Suggested fix:** Count only a number the text ties to lines or a diff. If several qualify, use the greatest. A ticket id, a date, a file count, or an item number does not qualify. If none qualify, keep the 1-line typo rule or `lines: unknown`.

### F-3: A bulleted `## Tweak surfaces` line never blocks `tweak`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 14, Extension, lines 102–103
**Edge case:** The target project's `AGENTS.md` contains a normal list:

```markdown
## Tweak surfaces
- payments
- billing export
```

**What happens:** Each non-blank line is one signal, but the match rules cover only a one-word signal and a quoted multi-word line. `- payments` is neither, so it matches no path and no description. The extra surface does not block `tweak`. A one-file, under-50 change in that area is recommended `tweak` with `surfaces: none`. A line that is only spaces is non-blank, trims to empty, and is also unspecified; an empty substring would match every path and force `big`.
**Why the spec misses it:** "Trimmed" does not strip a list marker, and no sentence says what a line that is neither one word nor a quoted phrase does.
**Suggested fix:** Strip one leading list marker (`-`, `*`, or `N.`) before classifying. Ignore a line that is empty after that. A remaining line that is neither one word nor a quoted phrase warns and recommends `big` (unknown surface), rather than matching nothing.

### F-4: The irreversible halt offers a worktree reuse Phase 1 does not have
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § ship-spec Phase 3b, line 250; `skills/ship-spec/SKILL.md:107-119`
**Edge case:** The irreversible halt has already created `<TICKET-ID>-worktree` and the branch, with the implementation uncommitted. The operator follows the new sentence and tries to "explicitly reuse that worktree" without discarding it. Resume itself stays D-1.
**What happens:** Phase 1's path check fires first and has no reuse choice: remove the directory or rename it, then re-run. `git worktree remove` on that dirty tree discards the only copy of the implementation, which the parenthetical states, but the `or explicitly reuses` clause presents reuse as the alternative that keeps the tree. The branch question (reuse / delete / rename) is never reached while the directory exists, and the skill never defines reuse as "continue this dirty tree at Phase 3b". The operator either loops on the path halt or removes the worktree and loses the work.
**Why the spec misses it:** The sentence was added so a re-run would not be described as resuming Phase 3b. It names a reuse action the pre-create checks do not provide.
**Suggested fix:** Delete the reuse alternative. Say the path check halts until the directory is removed or renamed, that removal discards the uncommitted tree, and that this halt does not continue that tree at Phase 3b. Leave the actual resume design on D-1.

### F-5: Wiki grounding paths make the normative tweak recommendation unreachable
**Severity:** P3
**Where:** spec § Decision 14, lines 88–90; `skills/spec-brief/SKILL.md:73-82`
**Edge case:** A one-file typo, as in example 1, in a project whose wiki resolved. Phase 1 records `state.md` and `filemap.md` plus `README.md`.
**What happens:** "Distinct file paths named in those texts" counts the wiki paths. That is more than one named file, so the 1-line rule does not apply, lines are unknown, and the recommendation is `big` even though the change is the worked tweak example. The failure is safe (it does not recommend `tweak` too often). Example 1 still passes only when grounding is defined to name `README.md` alone, which the skill's grounding step does not do once a wiki resolves.
**Why the spec misses it:** The estimate source is "ticket text and the Phase 1 grounding facts," and those facts include every file grounding opened.
**Suggested fix:** Count paths the change names, not wiki `state.md` / `filemap.md` reads. Say example 1 still recommends `tweak` when those grounding reads are present and the change names only `README.md`.

### F-6: Plane ticket body was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` for tags `plane_work_item` and `VHS-55` on namespace `skills`, `source_system: plane`.
**What happens:** The server returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. The review used the brief. No ticket body was checked for decisions the brief might have dropped.
**Why the spec misses it:** Not a spec defect. § Deferred (P2+) line 314 already records the brief as the source.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read namespace `skills` if a later round needs the ticket body.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 1 | P4: 1

STATUS: GREEN
