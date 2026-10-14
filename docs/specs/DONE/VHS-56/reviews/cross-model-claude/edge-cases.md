# Edge-Cases Review — round 4

> Cross-model round (Claude reviewer agents) over the round-3 green spec, run outside the `/spec-cycle` loop on 2026-10-13. Persisted by hand from the agent's hand-back text; not a `round-<C>/` directory.

## Closure of round 3 findings
N/A — no closure predecessor. This is the first pass of a full invocation with no `closure_manifest`. For context I read the round-1 to round-3 headings. None of the findings below repeats an earlier finding.

Grounding notes:
- Spec, brief, `skills/spec-brief/SKILL.md`, `skills/grilling/SKILL.md` (resume contract), `skills/spec-cycle/SKILL.md` (brief parsers at :288-300, :345-351, :1065-1072), `lint.py:44-45`, `README.md:9,65`, `AGENTS.md:25` and `docs/spec-workflow-reference.md:7-30` were all read live.
- The ticket lookup was blocked: `memory_search` on namespace `skills` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. I used the brief as the ticket source of truth, as instructed. This is already carried in the spec's `## Deferred (P2+)`, so it is not re-filed here.
- The spec has no `## Deferred — follow-up required` section, so the Deferred-findings rules have no rows to check.
- Anchor drift: every `path:line` citation in the spec resolves to the symbol it names at HEAD 7c2dfa0. No P1 or P4 for drift.

Persistence checklist for the new persisted `## Doubt pass` section:
1. Atomicity: CHECKED. It rides the existing temp-then-rename write (`SKILL.md:218`).
2. Size bound: counts are bounded. The operator's free-text skip reason is unbounded, which is already deferred as a P3.
3. Idempotency: CHECKED. A re-run hits the Phase 0 collision gate.
4. Read-side filtering: CHECKED. No downstream parser reads the section. The spec-cycle Tier and Scale heading regexes (`^#{1,6}\s+tier\s*$`, `^#{1,6}\s+scal(e|ing)\s*$`) cannot match `## Doubt pass`.
5. Schema forward-compat: CHECKED. No reader requires the section, so older briefs without it stay valid.
6. Write race: CHECKED. The skill already documents last-writer-wins at `SKILL.md:220`.

## Findings

### F-1: Doubt-pass edits have no durable home, so re-rendering or revising silently drops them, including operator "replace" answers
**Severity:** P1
**Where:** spec § Decision 1; § Design 2 (lines 172-176); § Design 6 (lines 203-215)
**Edge case:** Several things can follow a reconciliation that changed the candidate:
- the mandated re-render after each reconciliation edit;
- Confirm option 2 ("Revise an answer");
- the `--no-grill` "Add a decision" re-render;
- Phase 5 rendering the file it writes.

Before any of these, the operator may have chosen "replace" or "reopen" in the Decision 8 batch, or a fact or anchor fold may have landed.
**What happens:**
- Design 2 defines the candidate renderer as Phase 5's mapping rules. Those rules are a function of the Grill summary (Settled → Decisions, Open frontier → Risks), the ticket text, grounding facts, tier and scale (`SKILL.md:222-240`).
- Reconciliation edits change the rendered draft text. They do not change any of those inputs.
- On option 2, `grilling` rebuilds the tree from `prior_summary` (`skills/grilling/SKILL.md:21-23`). That summary has never seen the operator's doubt-pass replacement. The resumed candidate therefore puts the original settled decision back. The operator explicitly overruled that decision.
- Phase 3 then restarts at cycle 1 with a fresh reviewer. It may not raise the same contradiction again. The written brief would then carry the overruled decision as authority, under a `## Doubt pass` block reading `completed`.
- The same loss applies to the `--no-grill` "Add a decision" re-render, which re-derives from the ticket alone.
- Read literally, it also applies to "re-rendered after every reconciliation edit" and to Phase 5's write, because Phase 5 keeps its "Write … with exactly these sections" plus mapping rules. Nothing tells Phase 5 to write the previewed candidate rather than re-map from the summary.

**Why the spec misses it:** No section says where reconciled state lives:
- Decision 1 only says the draft "stays in context".
- Design 6 says Confirm previews "the full final candidate", but it never says that Phase 5 writes exactly that preview.
- No section says how operator replacements survive a resume.

This breaks the brief's Decision 4: the operator owns settled decisions, and the skill must not change them on a reviewer's word. Here the skill reverts the operator's own ruling. It also breaks the Done-when guarantee that a contradiction is resolved by the operator.
**Suggested fix:**
1. Add to Design 2 a held `reconciled_state` that the renderer reads alongside the summary:
   - operator replacements and reopens, keyed to the settled item they amend;
   - folded facts as grounding facts with `path:line`;
   - premises moved into Risks / decisions.
2. "Re-render" then means rendering the summary plus `reconciled_state`.
3. State in Phase 5: "write the candidate Confirm previewed, byte for byte, plus `## Doubt pass`; do not re-map from the Grill summary."
4. For option 2, choose one of these and state it:
   - pass the operator's replacements into `prior_summary` as amended Settled items; or
   - warn `revise discards doubt-pass resolutions: <list>` and require re-confirmation.
5. Add a Test-plan row: "the written brief equals the Confirm preview; an operator replace survives a revise or re-render, or the discard is announced."

### F-2: Classes 2 and 3 have no precedence rule, so a true fact about a settled decision can be folded without the operator
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 10 (lines 118-127); § Decision 7 (lines 88-92); § Decision 8 (lines 94-103)
**Edge case:** The reviewer challenges a fact or anchor that sits inside a numbered `## Decisions carried forward` item or its rationale. For example: "Decision 3's why cites `X:61`; the file actually says Y."
**What happens:**
- The finding is a class-2 "actionable fact or anchor" (fold when true). It is also a Decision 8 contradiction, because accepting it would change "a numbered … branch or its rationale".
- Decision 10 requires a single class per finding, processed in a fixed order with class 2 before class 3, and gives no tie-break.
- An executor that classifies it as class 2 folds a verified fact into a settled decision with no operator prompt.
- Decision 7's "move the premise into `## Risks / decisions`" for unverifiable claims does the same thing autonomously when the premise lives in a settled decision. It removes or alters a settled item.

This breaks Done-when #2 ("the skill never folds it alone").
**Why the spec misses it:** Decision 8 defines contradiction broadly, while Decisions 7 and 10 give fold and move actions with no carve-out.
**Suggested fix:** Add to Decision 10: "A finding that would change any Decision 8 target is class 3, whatever else it is. Verification under Decision 7 still runs first, and its result is shown as the 'verified evidence' in the operator prompt. Class-2 fold and move actions apply only to text outside Decision 8's targets."

### F-3: `irreversible` checks preconditions only after the full interview, and a Confirm tier change to `irreversible` throws the interview away
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 (lines 161-170); § Decision 3 (`irreversible` bullet, line 49); § Design 6 (lines 210-211)
**Edge case:** The tier is `irreversible` on a host with no eligible different-family reviewer. On a Claude-Code-only host this is the common case, since its subagent model choices are all one family. The same applies when the operator picks option 4 → `irreversible` at Confirm on such a host.
**What happens:**
- Design 1 resolves `reviewer_eligible` "after the tier is known", before the interview. Nothing acts on it until Phase 3.
- The operator sits through up to 10 rounds × 15 questions, then gets "stop, write nothing".
- At Confirm, choosing `irreversible` re-enters the doubt policy and stops. The whole interview and any contradiction answers are discarded because of a menu choice the host could never satisfy.
- The brief's rationale for stopping ("a stop is cheap", brief Decision 6) only holds if the stop happens early.

**Why the spec misses it:** Eligibility is computed early but enforced only at Phase 3. The option-4 path reuses "stop" rather than re-prompting.
**Suggested fix:**
- In Design 1 / Design 3: when the tier gate returns `irreversible` and `reviewer_eligible` is false, halt immediately after the tier gate with the precise reason, before the interview. Wait capability is already proven by the tier gate.
- In Design 6: on option 4 → `irreversible` with no eligible reviewer, print `irreversible needs an eligible cross-model reviewer — not available on this host` and re-show the tier prompt. Keep the interview; do not stop.

### F-4: The reviewer dispatch is not required to use a read-restricted class or sandbox, so "nothing written before Confirm" rests on a prompt instruction
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5 (lines 78-82); § Design 4 (lines 184-195); § Design 7; Test plan item 10
**Edge case:** The host's only different-family mechanism is a general-purpose agent, or a CLI bridge whose default sandbox can write. The reviewer then "helpfully" fixes the stale anchor it found, or writes a report file.
**What happens:**
- The repo is mutated before Confirm.
- `## What /spec-brief never does` (`SKILL.md:256`) and Test plan item 10 become false.
- No check detects the change, so the skill reports a clean run.

**Why the spec misses it:** Phase 1 already asks for the narrowest read-only agent class and forbids a general-purpose agent, because "most host agent classes keep shell access even when file-edit tools are withheld" (`SKILL.md:78`). Design 4 only says "read-only instructions" and "make no mutations", which is weaker than the skill's own existing pattern.
**Suggested fix:**
- In Design 4: require "the narrowest read-only agent class or sandbox mode the host offers for that model; never a general-purpose or write-capable mode." If the only eligible mechanism is write-capable, treat the reviewer as not eligible.
- Take a `git status --porcelain` snapshot before and after each dispatch. Any difference is a dispatch failure that prints the changed paths. The skill must not revert them; it names them for the operator.

### F-5: A reviewer that never returns hangs the run, and there is no work bound or honest "blocks" statement
**Severity:** P2
**Where:** spec § Decision 11 (line 151: "timeout … is a dispatch failure"); § Design 4; § Design 7 failure-mode list
**Edge case:** The cross-model reviewer is slow, or loops over the whole repo and wiki doing "live read-only verification".
**What happens:**
- The spec names "timeout" as a dispatch failure but defines no timeout value and no mechanism.
- On most hosts a subagent or CLI call blocks the caller until it returns. The skill therefore hangs indefinitely.
- The `small`/`big` "announced skip" and the `irreversible` "stop" are never reached. The operator's only exit is an interrupt, which loses the interview.

Phase 1 handles the same problem honestly. It bounds the prompt ("answer from the paths named … return `not found` rather than searching exhaustively") and documents that "a dispatch that never returns blocks its batch" (`SKILL.md:78`, `:275`). Design 4 gives the reviewer an unbounded mandate.
**Why the spec misses it:** "Timeout" is listed as an outcome without a source for it.
**Suggested fix:**
- Add a work bound to the Design 4 prompt: verify only paths cited in the draft or ticket, cap the number of findings, and return `evidence needed` rather than searching.
- Add to Failure modes: "a reviewer dispatch that never returns blocks the run; where the host offers a call timeout, use one, and its expiry is a dispatch failure."

### F-6: A transient dispatch failure has no retry, so it costs the operator's chosen pass, or the whole interview under `irreversible`
**Severity:** P2
**Where:** spec § Decision 12 (lines 155-157); § Decision 4 normalized reasons
**Edge case:** A single rate limit, network blip, or malformed status line on cycle 1 or cycle 2.
**What happens:**
- **`big`, operator chose "Run":** the pass is recorded as `skipped — reviewer dispatch failed — …` with no chance to retry, even though the host can wait (the tier gate proved it).
- **`irreversible`, cycle 2:** a single blip discards the full interview, the cycle-1 reconciliation, and the operator's contradiction answers. "No resume state is kept" (`SKILL.md:276`), so the operator redoes everything.

**Why the spec misses it:** Decision 12 maps the first failure directly to skip or stop.
**Suggested fix:** On any dispatch failure, prompt `Doubt pass dispatch failed (<cycle>, <class>): 1. Retry once  2. Skip (small/big only)  3. Abort`. Allow at most one retry per cycle, and do not count the retry as a cycle. The existing outcomes apply after the retry is used or declined.

### F-7: The `small` override prompt and the contradiction batch have no reply grammar or invalid-reply rule
**Severity:** P2
**Where:** spec § Decision 3 (`small` bullet); § Decision 8 (line 103); § Design 3 (line 182)
**Edge case:** The operator gives an ambiguous or partial reply. Examples: "2" to a three-item batch, "replace with something simpler", "keep all but F-3", or text that is not a menu choice. Another case is a batch of many items, since a noisy reviewer can flag every decision.
**What happens:**
- Decision 9 pins strict parsing for the `big` offer: re-prompt once, then stop.
- The `small` override and the per-item keep / replace / reopen / abort batch have no format, no per-item addressing, no rule for where free-form replacement text goes, and no invalid-reply rule. The executor has to improvise.
- An ambiguous reply read as "replace" or "reopen" changes a settled decision that the operator did not clearly choose to change. This is exactly what "the skill never chooses replace or reopen" forbids.
- Nothing caps the batch size, so a garbage-heavy reviewer can flood the operator. This runs against the fatigue bound the skill exists to enforce.

**Why the spec misses it:** Only the `big` offer got a grammar.
**Suggested fix:**
- Define one reply line per item, `F-<n>: keep | replace: <text> | reopen`, or a global `abort`.
- Treat an item with no valid answer as `keep` only after a single re-prompt, or stop. Pick one and state it.
- Apply Decision 9's re-prompt-once rule to the `small` override.
- Cap the batch, for example at the grilling `question_cap`. Excess items go to Risks / decisions as open, and the outcome counts them.

### F-8: "The host identifies a different family" is undefined for the operator's real mechanism, so eligibility and the `irreversible` gate depend on the agent
**Severity:** P2
**Where:** spec § Decision 5 (lines 78-82); § Decision 6
**Edge case:** A Claude Code host whose native subagent models are all one family, but where a different-family CLI bridge is reachable through shell or a locally installed skill. This is the operator's actual setup, the "codex review the brief" habit in the brief's Problem.
**What happens:** Decision 5 forbids parsing display names or keeping a model table, and Decision 6 ties the dispatch to `subagents: true`. An executor must then decide whether a shell-reached CLI counts as "the host" asserting a family.
- One run reads the bridge's documentation and counts it as eligible. That is arguably the forbidden name-parsing, and it may run with a write-capable sandbox (see F-4).
- Another run finds no host assertion and skips, or under `irreversible` stops.

The same brief on the same machine can therefore be written or refused depending on the agent. The feature may also never fire on the primary host, which leaves the brief's Problem (the hand-run review) unsolved.
**Why the spec misses it:** "Host metadata" and "subagent" are never tied to concrete evidence an executor can check.
**Suggested fix:** State whether a non-subagent bridge counts, without naming a vendor. If it counts, define the evidence: "a dispatch mechanism available in this session whose own runtime output or declared configuration states its model family, compared with the authoring model's self-reported family". If it does not count, say so explicitly and note in README that such a host always skips (or stops under `irreversible`).

### F-9: The headless branches cannot be reached, because the tier gate already stops a host that cannot wait
**Severity:** P3
**Where:** spec § Decision 3 (lines 45-49); § Decision 4 reason list; § Design 7 ("host cannot wait")
**Edge case:** A headless host.
**What happens:**
- The tier gate prints `tier needs an operator — stopping` and stops when the host cannot wait (`SKILL.md:94`), and Design 1 keeps it unchanged.
- Every run that reaches Phase 3 has therefore already proven `can_wait`. The `big` `skipped — host cannot wait` record and the `small` "keep the skip without prompting" branch can never fire, and `can_wait` at Phase 3 is always true.
- README/AGENTS mirrors would then advertise "announced-skipped headless" behavior that cannot happen.
- An operator who walks away mid-pass is not "cannot wait"; the host simply waits forever. This matches the existing abandonment behavior and is fine, but it is not what Decision 3 describes.

**Why the spec misses it:** Decision 3 borrows the tier gate's test without noting that the tier gate runs first.
**Suggested fix:** State that `can_wait` is established by the tier gate. Keep the `host cannot wait` reason only for a host whose wait capability is per-prompt, and say so; otherwise drop it from the reason list and the failure modes.

### F-10: `ticket_contract` can be a bare title or stale relative to the operator's seed and split decisions, which feeds a stream of false contradictions
**Severity:** P3
**Where:** spec § Design 1 (line 163); § Design 4
**Edge case:** Two cases:
- **Ticket mode where the seed gate re-prompted:** the ticket is a bare title, and the operator's paragraph became the seed (`SKILL.md:88`).
- **Stale tracker text:** the tracker text no longer matches the operator's settled scope. VHS-56 itself is an example: Plane still describes three parts after the split.

**What happens:**
- In the re-prompt case, the operator's paragraph is not in `ticket_contract`. The reviewer judges a full brief against a title.
- In the stale case, every cycle, and every re-run after a revise, flags the narrowed scope as dropped ticket requirements.
- These route as Out-of-scope or Done-when contradictions into the operator batch every time.

**Why the spec misses it:** `ticket_contract` holds "ticket text (or local-only paragraph)" only.
**Suggested fix:** Include the seed-gate paragraph whenever one was collected. Tell the reviewer that the draft's Origin paragraph and settled Out-of-scope items may legitimately narrow the ticket, and that such narrowing is a decision to identify, not a defect.

### F-11: Report parsing has gaps, and a failed review leaves no evidence for debugging
**Severity:** P3
**Where:** spec § Decision 11 (lines 129-151); § Design 5 (line 199)
**Edge case:** The reviewer's output can disagree with itself in ways the parse rule does not cover:
- three counts that can disagree: `Findings: <n>`, `DOUBT FINDINGS=<n>`, and the number of headings;
- `STATUS: READY` alongside `### F-` blocks;
- duplicate `F-<n>` ids;
- an `### F-` line inside a fenced quote;
- a finding missing `Target` or `Decision touched`.

On failure, the raw report is discarded.
**What happens:**
- "Reported count and headings disagree" does not say which count. Malformed fields have no rule.
- A failure prints only `<short reason>`. Under `irreversible` the run stops, with no way to see what the reviewer actually returned.

**Suggested fix:**
- Require all three counts to be equal. Ignore `### F-` lines inside fences. Treat duplicate ids or a missing `Target` or `Challenge` as malformed.
- On any dispatch failure, print (not persist) the cycle number, the failure class, and the reviewer's last non-blank line.

### F-12: The reason and count semantics are ambiguous for `small` with no reviewer, and for two-cycle totals
**Severity:** P3
**Where:** spec § Decision 3; § Decision 4 (lines 62-76); § Decision 12 (line 155)
**Edge case:** Several cases are not pinned:
- **`small` with no eligible reviewer:** Design 3 implies the tier-small reason, while Decision 12 implies `no eligible cross-model reviewer`.
- **Counts across two cycles:** whether they are summed, and whether a cycle-2 duplicate of a cycle-1 rejection counts twice.
- **"reopen" answers:** whether they count as "operator resolved" or as "open".

**What happens:** The audit record varies by executor. It degrades gracefully.
**Suggested fix:**
- Pin the `small` reason: tier-small when no override was offered.
- Say the counts are cumulative over both cycles, with a cycle-2 duplicate counted once.
- Say a reopen counts as resolved and its new Risks item counts as open, or choose the other way and state it.

### F-13: The renumbering instruction risks rewriting references to other skills' "Phase 3"
**Severity:** P3
**Where:** spec § Design 6 (line 215); § Design 8 (line 231)
**Edge case:** Some "Phase 3" references belong to other skills and must stay as they are:
- `SKILL.md:188` says "`/spec-cycle`'s Phase 3 parser", which refers to spec-cycle.
- `docs/spec-workflow-reference.md:102` is spec-cycle's "Phase 3 — Drift-check".
- `:246` is ship-spec's "Phase 3 — Test gate loop".

**What happens:** "Reconcile every reference to the old Phase 3 / Phase 4" invites a blanket replace. Rewriting `SKILL.md:188` or the other skills' headings to "Phase 4" would make them false.
**Suggested fix:** Scope the instruction to spec-brief's own phase references, listing `SKILL.md:124`, `:180`, `:182`, `:216` and the workflow-reference spec-brief block `:23-25`. Explicitly exclude `SKILL.md:188` and the doc's spec-cycle and ship-spec sections.

### F-14: `## Doubt pass` reuses the `**Status:**` label already used in the brief header
**Severity:** P4
**Where:** spec § Decision 4 (lines 62, 72)
**Edge case:** Any future reader keyed on `**Status:**` in a brief. The header line at `SKILL.md:192` carries the ticket status. No current consumer parses it (I grepped every skill).
**Suggested fix:** Use a distinct label such as `**Result:**` in the Doubt pass block.

## Summary
P0: 0 | P1: 1 | P2: 7 | P3: 5 | P4: 1

STATUS: RED P0=0 P1=1 P2=7 P3=5 P4=1
