# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Round-4 closed-issues manifest hardcodes the three reviewer filenames — scalability findings silently dropped as regression constraints
**Severity:** P0
**Where:** spec § Decision 8 / Design §5; the unlisted site is `skills/spec-cycle/SKILL.md:357–368` (step 2e, round-4 rewrite path)
**Edge case:** A scale-on run that does not converge by round 3 and enters the round-4 targeted rewrite, where the scalability lens raised a P0/P1 earlier that was later CLOSED.
**What happens:** Step 2e's closed-issues manifest is built by "scanning each round's three reviewer reports (`correctness.md`, `edge-cases.md`, `conventions.md`)" — a hardcoded enumeration that excludes `scalability.md`. Any scalability finding closed in rounds 1–3 is absent from the regression-constraint manifest, so the round-4 rewrite is free to regress the fix that closed it with no tripwire.
**Why the spec misses it:** §5 asserts the closure_manifest is "Already generic — built from 'every round-(N−1) P0/P1 finding' in step 2e." That conflates two artifacts. The round-2+ disposition closure_manifest (SKILL.md:290–313) is lens-agnostic. But the round-4 closed-issues regression manifest (SKILL.md:357–368) literally names the three files. The spec's Scope does not list step 2e.
**Suggested fix:** Add a step-2e edit to Scope and Design §5: change SKILL.md:358–359 to scan "every reviewer report present in each round's directory (… plus `scalability.md` when the scaling lens ran)." Add a Done-when/checklist item asserting round-4 manifest construction is lens-count-agnostic.

### F-2: Lens toggled on/off mid-run breaks closure tracking and gate continuity across rounds
**Severity:** P1
**Where:** spec § Design §5; Design §3 Phase 0 step 8
**Edge case:** The brief's `## Scale` declaration is the sole gate input, parsed once at Phase 0. A brief can be edited between `/spec-cycle` invocations (re-runs supported), or `scalability.md` from a prior round can persist on disk. Round 1 runs scale-on and writes `round-1/scalability.md`; author edits brief to `**Factor:** no` and re-runs; round 2 dispatches three lenses, each reading "every report present in `round-1/`" — including the stale `round-1/scalability.md`.
**What happens:** The three standing lenses attempt to render a now-disabled lens's findings; REOPENED defaults to P0, injecting a phantom P0 into the gate, or the loop cannot converge (no fourth summand to close it). The "byte-for-byte unchanged when off" guarantee silently fails when off follows a prior on in the same tree.
**Why the spec misses it:** §5's no-op claim assumes a clean reviews directory with no `scalability.md` ever written.
**Suggested fix:** Pass `scale_lens` to the reviewers and have the generalized step-7 read ignore a stale `scalability.md` when `scale_lens == off`; pin the scale decision to the spec's recorded Decision for the lifetime of the reviews tree (Phase 0 step 8 reads it back on re-run, warning if the brief disagrees). State the rule explicitly in §5.

### F-3: Orchestrator-side handling of a malformed/missing STATUS line from the scalability reviewer is unspecified
**Severity:** P1
**Where:** spec § Design §4; `skills/spec-cycle/SKILL.md:482` (existing "Reviewer status drift" → synthetic P0)
**Edge case:** The dispatched scalability reviewer returns a report whose last non-blank line is not a parseable `STATUS:` line.
**What happens:** SKILL.md:482 generically covers "a reviewer" → synthetic `RED P0=1`. But the spec's Failure-modes addition documents only the brief-parse malformed case, not the reviewer-output case for the new lens, and never confirms the scalability lens participates in the synthetic-P0 / round-2b manifest reconciliation.
**Suggested fix:** In §4, add: "A missing/malformed `STATUS:` from the scalability reviewer is handled by the existing reviewer-status-drift rule (SKILL.md:482) — synthetic `STATUS: RED P0=1 P1=0`, represented in the round-2b closure manifest as `scalability/STATUS (P0) …` like any lens." Confirm no edit to :482 is needed.

### F-4: Partial dispatch — scalability agent dies while the three peers return — leaves a round with no scalability.md and an unsound gate
**Severity:** P1
**Where:** spec § Design §3 step 2b / §4; SKILL.md:316–333
**Edge case:** Four agents dispatched; the scalability subagent crashes/times out/returns empty while the three peers return.
**What happens:** The spec specifies only the happy path. Step 2c has nothing to save; step 2d's "sum across dispatched reviewers" is ambiguous about whether a dispatched-but-absent reviewer counts as GREEN (0), synthetic P0, or is skipped. If silently skipped, a scale P1 vanishes and the spec goes green wrongly.
**Suggested fix:** Specify in §3 step 2c/2d: when `scale_lens == on`, the orchestrator expects four reports; a dispatched reviewer returning no parseable report is treated identically to a missing STATUS line (synthetic `RED P0=1`), and step 2c writes a stub `scalability.md` recording the dispatch failure so round-(N+1) closure has an anchor. Add to the Failure-modes addition.

### F-5: `scale_target` / `scale_dimensions` are free text interpolated into the drift-check block and reviewer prompts with no escaping
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design §3 Phase 3 and step 2b
**Edge case:** A `**Target:**` value containing markdown control characters, a pipe (`|`), backticks, or a code fence. The §2 capture regex `(.+\S)` greedily takes the whole remainder.
**What happens:** Degrades gracefully but visibly — a stray `|`/backtick can corrupt the plain-text checklist a human ticks. No crash/corruption (drift-check is printed text), so P2.
**Suggested fix:** Add a note to §2/§3: "`scale_target` is captured as opaque single-line text (the regex stops at line end) and rendered as-is in a plain-text checklist, so no escaping is required; keep it to a short single-line phrase."

### F-6: §2 heading regex and "first match" rule under heading-variant and multiple-`## Scale` inputs
**Severity:** P2
**Where:** spec § Design §2 detection rules 1 and 2
**Edge case:** (a) `## Scaling considerations` / `## Scale-out plan` — rule 1's `\b` permits trailing text, so an unrelated section is treated as the scale declaration; (b) two `## Scale` sections — "first match" silently ignores the second.
**What happens:** Mostly graceful: (a) yields `off, warn (malformed declaration)` — but the warning misleads an author who never intended that heading as a toggle; (b) silently drops a second declaration. P2 clarity.
**Suggested fix:** Anchor rule 1 to a whole-word heading (`^#{1,6}\s+scal(e|ing)\s*$`, case-insensitive); add "Multiple `## Scale` sections: the first is authoritative; subsequent ignored (warn `scale-lens: multiple Scale sections — using first`)."

### F-7: `scale_target` empty-but-Factor=yes is handled at two layers with an unstated precedence
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design §2 rule 3 vs. §1 grounding step
**Edge case:** Factor=yes, Target absent. Per §2 rule 3, Phase 0 sets `scale_lens = off` and does not dispatch. So the agent's "empty target → advisory" branch is unreachable in normal operation.
**What happens:** No runtime break, but a reviewer/implementer cannot tell whether the agent-side branch is intentional redundancy or a contradiction with §2 rule 3.
**Suggested fix:** State the agent branch is a defense-in-depth backstop: "under §2 rule 3 the orchestrator never dispatches without a non-empty `scale_target`; this branch exists so a host that dispatches the agent directly still fails safe (advisory-only)."

### F-8: Lens-off "byte-for-byte unchanged" guarantee is asserted but is a behavioral claim dressed as textual
**Severity:** P2
**Where:** spec § Goal / Decision 1 / Done-when 3; Test-plan items 3 and 6
**Edge case:** The grounding-step-7 generalization edits the three existing agents' prompt text unconditionally ("the other two lenses'" → "the other lenses'", "exactly three files" → "every report present"). That is a prompt change to the lens-off path.
**What happens:** Behaviorally a no-op, but not literally byte-identical at the prompt level. The spec uses "byte-for-byte" loosely.
**Suggested fix:** Downgrade to "behaviorally unchanged (identical dispatch, identical gate arithmetic, identical closure-table output)" for the lens-off path, reserving "byte-identical" for the dispatched 2b message specifically.

### F-9: Non-factor recorded decision has no drift-check teeth against a spec that adds scale machinery anyway
**Severity:** P3
**Where:** spec § Design §3 Phase 3 (non-factor line)
**Edge case:** Author marks `**Factor:** no` but the spec introduces batching/pagination/concurrency machinery.
**What happens:** Graceful — the Phase 3 line prompts a human but nothing parses the spec; the non-factor fence is advisory-only. Acceptable v1 limitation, P3.
**Suggested fix:** Soften Decision 3 to "recorded and surfaced in the Phase 3 drift-check for human confirmation (no automated enforcement)."

## Summary
P0: 1 | P1: 3 | P2: 4 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=3 P2=4 P3=1 P4=0
