# Edge-Cases Review — round 5

> Second cross-model round (Claude reviewer agents), delta over the Codex fold of the first Claude round, run outside the `/spec-cycle` loop on 2026-10-13. Persisted by hand from the agent's hand-back text; not a `round-<C>/` directory.

> Cross-model check (Claude edge-cases lens) of Codex's fold of the cross-model-claude findings, plus Codex's round-4 post-green polish to Design 6 and Test plan 14. Delta mode. Critique covers the 15 fold hunks and the unchanged sections that consume them. Read-only. No files were written.

Grounding notes:
- I read the following fresh: `docs/specs/TODO/VHS-56.spec.md` (318 lines), the brief, the fold diff, `skills/spec-brief/SKILL.md`, `skills/grilling/SKILL.md`, the mirror anchors in `docs/spec-workflow-reference.md`, `AGENTS.md` and `README.md`, the cross-model-claude reports, and the round-4 reports and synthesis.
- I also read the operator's real bridge: the installed `codex` skill, `~/.codex/config.toml`, and the `codex exec --help` text.
- Ticket lookup failed. `memory_search` on namespace `skills` returned `Access denied`, so the brief is the contract.
- HEAD is still `7c2dfa0`, the same as the baseline. Every anchor I re-checked resolves: `SKILL.md:6-9`, `:88`, `:92`, `:94`, `:124`, `:180-184`, `:188`, `:216`, `:218`, `:224`, `:256`; `grilling/SKILL.md:21`, `:23`, `:140`; `docs/spec-workflow-reference.md:23-25`, `:147-152`; `AGENTS.md:35`; `README.md:9`, `:65`. No drift.
- The spec has no `## Deferred — follow-up required` section. Its `## Deferred (P2+)` list is informal, so the routing and ceiling rules have no rows to apply to.

## Closure of cross-model-claude edge-cases findings (P1/P2)

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P1) | Doubt-pass edits have no durable home | CLOSED | Decision 1 (spec:43-45) makes the held candidate authoritative after the initial mapping, and Phase 5 writes the confirmed bytes. Design 2 (:193-197) maps the candidate once and amends the transcription rule. Design 6 (:238-242) carries resolutions through revise and adds the no-grill Add-a-decision step. Test plan 14 covers it. The polish has residual gaps, filed as new F-5 (P3). |
| edge-cases | F-2 (P2) | Class 2 / class 3 precedence | CLOSED | Decision 10 (:132) detects settled targets first. Decision 7 (:102) bars autonomous fold or move inside them. Design 2 (:195) repeats this, and Test plan 7 covers it. |
| edge-cases | F-3 (P2) | `irreversible` checks too late; a Confirm upgrade loses the interview | CLOSED | Design 1 (:189) halts right after the tier gate. Design 6 (:236) re-shows the tier prompt and keeps the interview. Decision 3 (:59) and Test plan 4 agree. |
| edge-cases | F-4 (P2) | Read-only dispatch not required | CLOSED (main part); snapshot part DEFERRED | Decision 5 (:92) requires the narrowest read-only class or sandbox and makes a write-capable-only mechanism ineligible. Design 4 (:218) says the same. The deferral reason at :313 holds. A before/after `git status` diff would flag the operator's own concurrent edits as false positives, and the spec forbids reverting anyway. With read-only mode now an eligibility condition, the remaining risk is a declared-but-unenforced sandbox, which is P3 at most. |
| edge-cases | F-5 (P2) | Reviewer that never returns hangs; no work bound | CLOSED | Design 4 (:218) bounds evidence work and the finding count and uses the host timeout. Design 7 (:250) records that a dispatch which never returns blocks the run. A new variant (the timeout length is unpinned) is filed as F-3. |
| edge-cases | F-6 (P2) | No retry on a transient failure | CLOSED | Decision 12 (:167-175) adds a retry/skip/abort prompt, one retry per cycle that does not count as a cycle. Decision 2 (:51) and Test plan 16 agree. |
| edge-cases | F-7 (P2) | No reply grammar for the small override or the contradiction batch | CLOSED | Decision 8 (:115) defines one line per item and an explicit `abort`; missing answers re-print and are never inferred; the batch is capped. The small override is now Confirm option 5 (Design 3, :203). Residual grammar gaps are filed as F-6 (P3). |
| edge-cases | F-8 (P2) | Different-family evidence undefined for the operator's real mechanism | PARTIAL | Decision 5 (:92-94) now admits shell and skill bridges and defines evidence. On the operator's real host, though, the required evidence does not exist before the interview, and the result still depends on the executor. See F-1. The original P2 stands. |

Two items were deliberately not folded:
- **cross-model-claude correctness/F-6** (P3 process note, ticket not cached). The deferral reason holds: no spec fix was proposed, and the brief's Origin records the narrowed contract.
- **edge-cases/F-4 snapshot part.** The deferral reason holds, as stated in the table above.

## Findings

### F-1: Eligibility for the operator's shell or skill reviewer still depends on the executor (continues F-8)
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5 (:92-94); § Design 1 (:183-189); § Decision 12 (:167)
**Edge case:** The operator's real host is Claude Code plus the Codex CLI through the shell or the installed `codex` skill. Eligibility must be settled at the tier gate, before the interview, and Design 1 forbids dispatching before the interview.
**What happens:**
- The evidence Decision 5 requires does not exist at that point.
  - The `codex` skill has no family field. Its frontmatter text is "Drive OpenAI Codex CLI (GPT 5.6 models)". That is a display name plus a vendor inference, which Decision 5 says is insufficient.
  - `~/.codex/config.toml` declares only `model = "gpt-6.1-sol"`, with no provider or family key.
  - A family-like value (the CLI's run header provider line) only appears in run output. That needs a dispatch, which Design 1 forbids before the interview.
- **A strict executor** therefore finds the bridge ineligible:
  - every `big` run records `skipped — no eligible cross-model reviewer`;
  - every `irreversible` run halts.
  - The brief's Problem, the hand-run Codex review, stays unsolved. README:65 will still claim that "shell/installed-skill bridges count".
- **A lax executor** runs a probe, or reads provider or vendor text as "family", and finds the bridge eligible.
- Same machine, same brief: written or refused depending on the executor.
- Other gaps:
  - "Declared model is selectable now" has conflicting declarations: the skill says gpt-5.6-*, the config says gpt-6.1-sol.
  - With no recognized ranking, the lexical tie-break picks `gpt-5.6-luna`, which the skill labels quick/cheap.
  - After selection, the identity the model reports at run time is never re-checked. A configured fallback or provider route could silently substitute a same-family model, which Decision 12's title forbids.
  - Neither the halt message (:189) nor the skip record names which check failed. The operator cannot tell what to fix.

**Why the spec misses it:** Decision 5 accepts "runtime metadata/output" as evidence. Design 1 and Decision 12 fix the decision time before any dispatch. Neither says whether a no-draft identity probe is allowed, or whether a provider or vendor field counts as a family field.
**Suggested fix:**
- In Decision 5, state:
  - (a) whether a pre-interview identity probe through the selected mechanism, in its read-only mode and with no draft, is permitted and counts as runtime metadata;
  - (b) whether a provider or vendor field counts as a family field.
- At each dispatch, compare the identity the run reports with the held evidence. A mismatch or a missing identity is a dispatch failure.
- On a skip or halt, print each candidate mechanism and its first failed check (family unknown, same family, mode unknown, model not selectable). Print to the console only; keep it out of the brief.
- Prefer the mechanism's documented default model over the lexical tie-break.
- Add these cases to Test plan 15.

### F-2: What text the parser reads for a shell or skill reviewer is undefined, so valid reports can fail the strict parse
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 11 (:163); § Design 4 (:207-218); § Design 7 (:246)
**Edge case:** Two common cases:
- **Transport lines.** A CLI reviewer writes progress, headers and token usage around its final message, and the host merges stdout and stderr into one capture.
- **A wrapped report.** The reviewer echoes the schema's ```` ```markdown ```` fence around its whole report. The schema itself is shown to it inside a fence (:145-161).

**What happens:**
- With transport lines, the last non-blank line is a transport line, not `STATUS:`.
- With a wrapped report, every `### F-<n>:` heading is fenced. The block count is 0 and disagrees with the summary.
- Either way the dispatch fails. The retry repeats the same output. Under `irreversible`, only Abort remains, so the full interview is lost on a substantively valid review.
- Sending the payload has its own gap. The installed bridge says to write long prompts to a scratch file first, but Design 7 and `SKILL.md:256` forbid any pre-confirmation write. The spec never says the payload must travel by stdin or argv, byte-exact.

**Why the spec misses it:** Decision 11 defines the report grammar but not which captured text it applies to.
**Suggested fix:**
- Define "reviewer output" as the mechanism's final response message, kept separate from progress or transport output and obtained without writing a file. Examples: stdout only, or the final message of a JSON event stream.
- A mechanism with no separable final message is ineligible.
- Tell the reviewer not to wrap the report in a fence, or strip one outer fence that encloses the whole response before parsing.
- State that the prompt travels by stdin or argv with no file, byte-for-byte.
- Add a whole-report-fence case and a trailing-transport-line case to Test plan 16.

### F-3: The timeout length is unpinned, so a host default shorter than a normal review fails every dispatch
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 4 (:218, "Use a host call timeout when offered"); § Design 7 (:250); § Decision 12
**Edge case:** The host's default shell-call timeout is shorter than a normal cross-model review of a `big` brief with live verification. Claude Code's Bash tool defaults to 2 minutes. The operator's config runs at `model_reasoning_effort = "high"`, and the bridge itself notes that "runs can take minutes".
**What happens:**
- Cycle 1 times out, and so does the retry.
- `big` and `small` always record `skipped — reviewer dispatch failed`.
- `irreversible` always ends in Abort after the interview.
- The retry also reuses the same mechanism, even when a second eligible mechanism exists.

**Why the spec misses it:** The fold fixed the hang (old F-5) by adopting "a host call timeout", but says nothing about how long it should be.
**Suggested fix:**
- Use the longest call timeout the host offers, or a background dispatch the host can wait on. Never fall back to a shorter default.
- Print the bound used in the failure line's `timeout` class.
- Optionally, let the retry pick the next eligible mechanism when its declared identity passes the same checks.

### F-4: Under `irreversible`, a cycle-2 failure aborts, yet a tier upgrade accepts the identical state
**Severity:** P3
**Where:** spec § Decision 12 (:175-177); § Design 6 (:236); Test plan 4
**Edge case:**
- **Direct path:** the tier is `irreversible`. Cycle 1 reconciles and changes the draft. Cycle 2 fails twice. Only Abort remains, and the interview and the operator's contradiction answers are lost.
- **Upgrade path:** the run goes `big` → cycle 2 fails → Skip → Confirm option 4 → `irreversible`. Decision 12 keeps the same `completed at cap`, `Cycles: 1` record and the brief is written.

**What happens:** The same end state is allowed by a detour and forbidden by the direct path, at the cost of the whole interview. Decision 12's own reasoning ("the brief requires that a pass ran") says cycle 1 is enough.
**Suggested fix:** Under `irreversible`, after a reconciled cycle 1 and an exhausted cycle-2 retry, offer "Accept cycle 1 (completed at cap, Cycles: 1)" or Abort. This is not a skip by Decision 12's own reasoning. Otherwise, state the asymmetry as intended in Test plan 4.

### F-5: The post-green polish leaves three resume gaps
**Severity:** P3
**Where:** spec § Design 6 (:238-240); Test plan 14
**Edge case:** Confirm option 2 (revise) after a doubt pass, under grilling.
**What happens:**
1. **Constraints passed in `seed` have no grilling meaning.** grilling defines `seed` as the problem statement plus grounding facts (`skills/grilling/SKILL.md:18`), and its resume contract rebuilds the tree from the summary (`:23`). An "operator-settled constraint" there has no defined treatment. The resumed interview can settle a decision that contradicts a kept Q-less resolution, such as a replaced Done-when statement. The candidate keeps both. Under `small`, re-running Phase 3 just records the tier-small skip, so a self-contradicting brief is written with no review.
2. **A Q-linked `reopen` cannot be expressed in the summary grammar.** The Open item's `unresolved because:` list (`:143`) has no doubt-pass value, and the grammar does not define a Q that is both Settled and Open.
3. **The `Interview: <n> rounds, exit <token>` References bullet goes stale** (`SKILL.md:231`). That bullet does not consume a revised decision. Phase 5 now writes exact bytes instead of re-mapping from the latest summary, so the written brief keeps the pre-revise round count and exit (for example, it lacks `revised-after-cap (+1 round)`). Today, Phase 4 re-maps it.

**Suggested fix:**
- After a resume, compare each returned Settled item with the kept constraints, and route conflicts to the Decision 8 prompt before Phase 3.
- Pass a Q-linked reopen as an Open item with `deferred`, removed from Settled, and say so.
- Refresh the Interview bullet from the returned summary header.
- Add these three cases to Test plan 14.

### F-6: The contradiction-batch grammar leaves composition and multi-line edges open
**Severity:** P3
**Where:** spec § Decision 8 (:115)
**Edge case:**
- Two overlapping findings on one target get different answers, for example `F-2: replace: A` and `F-5: replace: B`, or keep plus replace. These re-print with no stated reason, so the operator may loop.
- A replacement (decision plus rationale) needs more than one line.
- A reply names an id outside the batch, or mixes `abort` with item lines.

**What happens:** The prompt re-prints indefinitely with no reason given, or the executor improvises. Nothing is corrupted, because nothing is inferred.
**Suggested fix:**
- Allow a group answer such as `F-2,F-5: replace: <text>` for overlapping items.
- Name the specific conflict when re-printing.
- Treat ids outside the batch as invalid.
- Accept `abort` only as the sole line.

### F-7: The finding cap is tied to the interview flag, and going over it is a failure rather than a cut
**Severity:** P3
**Where:** spec § Decision 11 (:163); § Design 4 (:214)
**Edge case:** `--questions 1` (or 2) limits the interview, but it also limits the doubt report to one finding per cycle. A reviewer that returns two fails the dispatch. The same prompt on the retry likely fails again. Under `irreversible`, the run aborts.
**Suggested fix:** Separate the report cap from `--questions`, for example a fixed 7, or the larger of `question_cap` and 7. Alternatively, state that the coupling is intended and add the `--questions 1` case to Test plan 16.

## Persistence checklist (`## Doubt pass`)
1. **Atomicity — CHECKED.** It uses the existing temp-file-then-rename write (`SKILL.md:218`). Design 6 (:242) requires exactly one outcome block.
2. **Size bound — CHECKED.** Counts are bounded. The free-text skip reason is unbounded; that is already deferred (:311).
3. **Idempotency — CHECKED.** The Phase 0 collision gate covers a re-run.
4. **Read-side filtering — CHECKED.** The section is inert. Nothing consumes it or the Interview bullet; I grepped skills, agents and the workflow reference.
5. **Schema forward-compat — CHECKED.** `/spec-cycle` parses by heading. Renaming the label to `**Result:**` avoids a clash with the header's `**Status:**`.
6. **Write race — CHECKED.** Unchanged; last-writer-wins is documented at `SKILL.md:220`.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 4 | P4: 0

STATUS: GREEN
