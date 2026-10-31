# Spec Workflow — Clean-Room Reference

Five AI-driven skills, plus one optional stage: an interview stage that produces the brief, two that split spec authoring from implementation into separate sessions, `/spec-land` as the post-merge step before `/spec-close`, and the close. The optional stage, spec-tickets, sits between authoring and implementation and breaks a green-lit spec into dependency-linked tickets. The split is load-bearing: spec context grows with review rounds, implementation context grows with the codebase — combining them risks hitting the context window ceiling mid-flight. The session boundary also means a green-lit spec on disk is a stable artifact: if implementation aborts, you re-run without re-reviewing.

---

## Skill 0: spec-brief

**Purpose:** produce the brief. Why it sits upstream of everything else: every reviewer lens treats the brief as authority, so a fork left open in it is invisible to review and surfaces later as a P0/P1 against the spec — a branch settled in an interview costs one question, the same branch settled at review round 2 costs a full parallel dispatch plus a revision pass. A premise is a claim that would make the ticket pointless if false. Each is `unchecked`, `read` (what a file's text says, opened in this run), or `ran` (a run record from this invocation's interview), and an `unchecked` premise blocks Write until the operator records a reason.

**Invocation:** `/spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`. `--rounds` takes 1–10 (default 3), `--questions` takes 1–15 (default 7); there is no `0` alias, because a zero-width round is a stall, not a bound. `--no-grill` skips the interview but not the seed gate, the tier gate, the doubt pass, or the confirmation step. It does not skip the Confirm gate or `check_premises.py`. The seed gate runs before the tier gate in every mode, including `--no-grill`, and is not part of the interview that flag skips.

**Phase 0 — Preflight.** Read the project-instructions file and resolve the wiki. Check for existing artifacts at `docs/specs/TODO/<TICKET-ID>.*` — a brief, a spec, a reviews tree — and halt rather than overwrite the axiom prior review rounds were measured against; a stale temp file from an interrupted run is removed without halting. Run a warn-only origin-sync check (grounding reads the local tree; the skill never updates it). Resolve the ticket through the issue tracker, then — if it is unreachable — conversation-only mode, where the operator states the problem in a paragraph.

**Phase 1 — Grounding (read-only).** Retrieval-first: the ticket text, then the project wiki's state and filemap, then the files the ticket names by path, and only then read-restricted exploration agents for the gaps that remain — dispatched in one bounded parallel batch, instructed to answer with `path:line` evidence and make no mutations.

**Seed gate.** Runs after Phase 1 and before the tier gate, in every mode, including `--no-grill`. It is not part of the interview that flag skips. A seed that states no problem is re-prompted once, then the run halts. Nothing is written on an empty seed. An empty seed halts before the tier question.

**Tier gate.** Runs after the seed gate passes, in every mode, before the interview and before Confirm. The operator sets the tier. A host that cannot wait prints `tier needs an operator — stopping` and stops. Nothing is written. The same prompt lists the claims that would make the ticket pointless if false; the operator agrees or names a missing one. The tier ladder, the `## Tier` grammar, and the tweak hint are § Stakes tier below. After a non-tweak tier, the skill resolves whether a doubt-pass reviewer is eligible: a session-available mechanism that itself states a model family or provider different from the author's, offers fresh context and a read-restricted or read-only mode, and returns a final response without a file. An `irreversible` tier with no eligible reviewer halts here, before the interview, with nothing written.

**Phase 2 — Interview.** Run the grilling contract below against the grounded seed at brief altitude. `--no-grill` skips this interview. It does not skip the seed gate, the tier gate, the doubt pass, or Confirm.

**Phase 3 — Doubt pass.** Render the complete brief once and hold it as the candidate; from then on edits land in that held text and nothing re-derives it. The pass is offered at every tier when a reviewer is eligible (run, skip, or abort; a skip needs no reason), and `irreversible` must run (§ Stakes tier). A fresh-context, read-only reviewer from a different model family gets the candidate, the ticket contract, and the project and wiki roots — no conversation or author reasoning — and returns at most 7 findings in its final response, read leniently. The author owns reconciliation, and escalates on effect, not location: the operator batch gets a finding that changes scope, a decision's direction, or the threat model, or that challenges an operator assumption about the plan, as keep, replace, or reopen, never folded alone. An assumption whose only effect is the tier is not in that batch. A finding that only changes the tier, including a challenge to an assumption about the tier, is shown at Confirm and is not a batch question; only option 4 changes the tier. If one finding would change the tier and would also change scope, direction, or the threat model, the whole finding goes to the batch; on that row, replace must not change the tier, and new text that would change it is asked again and not applied. The author folds wording, precision, and anchors, including inside a Decision, and decides a purely technical trade-off; otherwise contract misreads are rejected, facts and anchors are verified live and folded, rejected, or moved to `## Risks / decisions`, and noise is rejected. The batch is printed only when a finding escalated. At most two cycles: cycle 2 runs only when cycle 1 changed the candidate, and there is no cycle 3. Each cycle gets one retry on a dispatch failure. Failure may skip below `irreversible`; `irreversible` never skips, and may only accept a reconciled cycle 1 that changed the draft, at cap, or abort. No tier substitutes a same-family review. Nothing is written in this phase. Level findings are verified fact/anchor folds; a fold never raises a level to ran without the run record.

**Phase 4 — Confirm.** Show the full candidate as it will be written, including its `## Doubt pass` block, plus `Tier: <level>`, the basis line, and a `Doubt pass:` summary line, then ask: write, revise an answer by question number, abort, or change the tier. Changing the tier asks the tier gate again. A non-tweak choice returns to the preview; a completed doubt result stands, and a skip is re-evaluated under the new tier. A `tweak` answer writes nothing. The author's adopt and reject choices show as one short summary that needs no reply; naming a line keeps, reverses, or reopens it. A revision, an added decision, or a summary reopen voids the doubt result and runs Phase 3 again from cycle 1. A summary reverse to text the reviewer already saw does not void it. Confirmation happens even under `--no-grill` — the brief is the artifact every downstream lens treats as authority, and the cost is one prompt. The Confirm gate runs before Write is offered, including the first entry and any return from exit 1. It promotes a premise to ran only from a supporting run record in this invocation's Grill summary, demotes a ran premise with no such record, adds premises the current Decisions or Scope rows newly rely on, shows the candidate, and asks the operator for a reason, or abort, on each unchecked premise without one, writing the replies onto `**Override:**` lines. When the operator picks Write, Phase 5 writes the temp from the candidate, runs `check_premises.py` on it, and renames it on exit 0. Exit 1 with `premise:` codes blocks Write, deletes the temp, and returns to the gate; any other result, such as a missing script, a crash, or a timeout, warns and writes.

**Phase 5 — Write.** Write the confirmed candidate to `docs/specs/TODO/<TICKET-ID>.brief.md` through a dot-prefixed temp file renamed over the target, so an interrupted write never leaves a truncated brief. Settled decisions become `## Decisions carried forward`; `## Premises` follows that section, and the same edit that adds the first premise deletes `_(no premises)_`; open frontier items become `## Risks / decisions`, each ending "spec author pins this"; established facts become `## References` with their source; a `path:line` source may also back a Scope row; a `source: run:` fact is a References entry citing `run: "<command>"` with the exit code and the excerpt, and it never backs a Scope row on its own; every brief this phase writes carries a `## Tier` section immediately before the conditional `## Scale`, with one `**Level:**` line whose value is `small`, `big`, or `irreversible`; an optional `## Scale` section is emitted only when the operator settled scale as a factor *and* gave a target N; every brief carries one `## Doubt pass` section after Scale (or after Tier) and before `## Risks / decisions`, recording `completed` or `completed at cap` with its cycle count and finding counts, or `skipped` with a normalized reason. That section is audit metadata: it names no vendor, model, or tool, and nothing downstream gates on it.

**Termination shapes and where each lands.** An emptied frontier means the tree was fully visited, or that a later round's remaining candidates all fell below the altitude fence — either way the reason line says which, and anything the operator deferred is still in the brief's open items. A fence-empty exit means nothing met the altitude fence in round 1 — the brief is written with no decisions and the reason recorded. A cap hit or an operator stop is a documented outcome, not a failure: the unresolved branches — questions and unestablished facts alike — go to `## Risks / decisions` for the spec author. An empty seed is the one shape that writes nothing at all.

### The grilling contract

The interview itself is a separate, model-invocable primitive, reused by three callers — this skill, an ad-hoc `/grill-me` command, and the halt menu in spec-cycle that follows the first invocation's `round_cap` passes (2 when the tier is `small`, 4 otherwise) or a later delta halt at cumulative round `C`. The interview that menu starts keeps its own cap of 3. It is never fired unprompted.

It models the problem as a **design tree**: every decision branches into the decisions that hang off it, and the **frontier** is every decision whose prerequisites are already settled. Each round asks the whole frontier at once — never one question at a time — then waits. A question that genuinely branches is rendered as a **fork** with two or three weighed candidates and an explicit recommendation. That recommendation is **advisory**: it never carries by silence.

Facts are the agent's job; decisions are the operator's. A code-text fact is **dispatched to a read-restricted exploration agent**, not asked, or rendered as an explicit request when the host has no such agent class. A run-time fact goes to a host-enforced read-only sandbox, or becomes a fact request when there is none; a network run needs the operator's approval. An operator's answer to a fact request is a claim, checked read-only; when not confirmed it travels unverified in `claim:`.

Three bounds, and nothing else, end the interview: a **round cap** (default 3), a **per-round item cap** (default 7, a hard truncation, with fact requests counting against the same cap), and an **altitude fence** — only decisions that would change a line of the brief's Scope, Decisions carried forward, or Out of scope are askable at all. Implementation detail is the spec's job.

It ends by rendering a **hand-off block** — settled decisions, the open frontier with a reason for each unresolved question and each unestablished fact, the facts established with their sources (a `path:line` or a `source: run:` record), and, when the caller tagged its seed items, a `ref:` on each item naming the seed items it came from — and writes no file: every write belongs to the caller. A run-sourced fact is References-only for `/spec-brief`. When redaction changes operator text, the primitive prints one non-blocking rotation notice and the summary carries the line `Redaction: fired`.

---

## Skill 1: spec-cycle

**Purpose:** Take a short brief (a half-page problem statement with acceptance criteria) and produce a converged engineering spec, reviewed by independent AI agents (three by default, plus an optional fourth scalability lens when scale is declared).

**Invocation:** `/spec-cycle <path-to-brief> [--attest "<reason>" | --full]`. `--full` is exclusive with `--attest` and forces a full review without changing the recorded tier or scale decision.

### Phase 0 — Preflight

Before writing anything:

1. **Read the brief.** Expected location: `docs/specs/TODO/<TICKET-ID>.brief.md`. Extract the ticket ID from the filename.
2. **Read your project's CLAUDE.md** (or equivalent project-instructions file). Note test commands, conventions, and any wiki path.
3. **Look up the ticket in your issue tracker** (Jira, Linear, Plane, etc.) for canonical acceptance criteria. If the tracker is unreachable, proceed using the brief alone — it's the local source of truth.
4. **Upstream and origin check** (warn only). If the current branch is behind `upstream/<default-branch>` (forks) or behind its origin branch, print one warning each and continue; it never asks and never updates the tree. With no such remote, skip it.

### Phase 1 — Author v1 spec

Write a spec at `docs/specs/TODO/<TICKET-ID>.spec.md` covering at minimum:

- **Goal** — one paragraph: what ships and why.
- **Scope** — files to change, files to create, files explicitly untouched.
- **Design** — the proposed implementation. Non-obvious decisions get their own subsection with rationale. If the brief carries forward explicit decisions (e.g., "rename, don't alias"), the spec must reflect each one.
- **Test plan** — what tests to add/update, what regression tests guard against the bug class.
- **Test command** — the exact shell command(s) to run. This becomes the single source of truth for the implementation skill's test gate. For doc-only or ops-only work where no code ships, set this to `N/A` and provide a review checklist instead.
- **Done when** — bullet list mapped 1:1 to the brief's acceptance criteria.
- **Out of scope** — explicit fences carried from the brief.

While authoring, every factual claim about how existing code or a system behaves at runtime carries a `file:line` anchor read from the live source during preparation of that dispatch. A prior spec, reviewer report, wiki page, or brief points to evidence but does not replace the live read. Source outside the project root is still opened and identified by path; when source is genuinely unreadable, the sentence says the behavior is observed or assumed and its evidence records `Anchor: none`. A Runbook step that invokes code is traced through the exact live call chain that admits or rejects it.

### Phase 2 — Parallel review loop

On the first invocation, `round_cap` is 2 when the tier is `small` and 4 otherwise (`big`, `irreversible`, or an absent tier). Pass-index `P` runs from 1 through that cap. Revision runs while `P < round_cap`; `P == round_cap` is the FROZEN/REWRITE pass and the halt follows it. A cumulative round `C` names review directories and markers; on the first invocation `C == P`. The single-counter paragraphs and steps below describe that first invocation's pass index. Grilling's own cap of 3 is separate.

On a re-run after a reviewed green or red halt, spec-cycle uses at most two delta passes: each lens gets `spec_diff` (the spec against the last round's `spec.copy.md`) and the open P0/P1 findings and judges scope itself, while closure, grounding, process, vanished-reference, and Deferred-row checks still run on the whole spec. Delta pass 1 revises normally. Delta pass 2 folds without FROZEN/REWRITE, then halts if still red. An unchanged green spec with nothing open stops with `nothing changed since green round <C>` and writes nothing. `--full`, a missing, pending or attested marker, a missing round snapshot, or a missing spec forces a full invocation. A change to the brief or to cited code is not detected; pass `--full` after either. The first invocation remains a full review.

The delta shape exists because PET-166 showed the churn cost of repeated full lenses: 58% of findings in rounds 2–5 and 54% in rounds 6–10 targeted text added to satisfy earlier findings; genuine misses dried up after round 2 at about 12%; 3 of 5 P0-class defects were manufactured by earlier remediations. Its round-11 delta close-out verified 26 closures and surfaced 2 findings, both P2s, versus about 30 findings per full-lens round in rounds 7–10.

Each round:

1. **Re-read the spec from disk.** Never trust your own prior write — the file is truth.
2. **Save the round artifacts, then dispatch the reviewer agents in parallel** (one message, multiple agent calls — three by default; a fourth, scalability, when the brief declares scale). The saved round artifact is `spec.copy.md`, the exact spec bytes the reviewers see; a failed write stops before dispatch. Every actual dispatch also writes `docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth-ledger.md`: a human-readable claim → spec section → anchor → round-read record, or an explicit no-claims line. It is separate from `spec.copy.md` and from disposition `ledger.md`; a failed write warns and dispatches so correctness can report the missing evidence. Each reviewer uses a different lens:

   **Correctness reviewer** — Does the spec actually solve the brief? Verifies every claim about current code by reading the actual files. It alone receives the ground-truth ledger path and deterministically samples at most five rows, blocking on a missing ground-truth ledger or a live anchor that does not support its claim while treating omissions as advisory. Checks also include unmapped acceptance criteria, internal contradictions, references to nonexistent symbols, stale file:line anchors, cross-section consistency (function signatures declared in one section match call sites in another), and library API correctness against the project's pinned versions.

   **Edge-cases reviewer** — What breaks it? Probes: empty/null/zero-length inputs, concurrency and races on shared state, external-system failures (down, slow, malformed response), partial-failure consistency, config drift, observability gaps, persistence atomicity/idempotency/size-bounds (for any spec that introduces persisted state). For each axis, asks what the spec says happens and whether that's adequate.

   **Conventions reviewer** — Does it follow the repo? Reads CLAUDE.md, the project wiki (if any), and greps the codebase for established patterns. Checks: stated conventions followed, no contradiction with prior decisions, no premature abstractions (registry/factory at N=1), reuse vs. duplication, no unneeded backwards-compat shims, silent spec additions not authorized by the brief. Also classifies every spec decision as authorized-by-brief, authorized-by-ticket, spec-addition-with-rationale, or silent-addition.

   **Scalability reviewer** *(optional — dispatched only when the brief declares scale a factor)* — Does the design hold at the brief's declared target N? Probes: per-item work that should be batched, O(N) where O(1)/O(log N) exists, unbounded accumulation, per-instance state that collides across instances, fan-out without a concurrency cap, a singular config/path where a power user needs many, plus operational scale (cost-per-op, latency, token/context budget). The differentiator from edge-cases: edge-cases asks "is it correct under one adverse input?"; scalability asks "does the design hold at N×?"

3. **Each reviewer emits a severity-ranked report** with findings at P0-P4 and a machine-parseable last line: `STATUS: GREEN` or `STATUS: RED P0=<n> P1=<n> ...`. P0/P1 block shipping — except that a finding the author routed, under the scope ceiling, to a well-formed row in the spec's `## Deferred — follow-up required` section is not re-filed by the reviewers and so never enters the gate — a malformed row, a duplicate section, a routing-changing scope error, or an undischarged in-scope P0 or P1 row, including a grill row the ceiling classifies as in-scope, is still filed as a P0; P2+ are advisory.
4. **Save each report to disk** at `docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/<lens>.md`.
5. **Gate check:** Sum P0+P1 across all dispatched reviewers. The sum is unchanged. Green is that sum equal to zero and the guarantee scan clean. A review-produced green verdict is not written while an undischarged in-scope P0 or P1 row remains. "Still red" in steps 6–8 is loop-red: `total_p0p1 > 0` or the scan withheld.
6. **If loop-red while first-invocation `P < round_cap`:** Edit the spec in place. Route every P0 and P1 finding to exactly one disposition — **fold** (edit every propagation site), **defer** (an in-scope P0 or P1 folds at every site, the site count is a cost note, and deferral is the out-of-scope finding with two or more sites), or **reject** (`not applicable`). Before embedding reviewer-supplied facts, verify them against live source; compose findings that target overlapping text into one intended result; then re-read every propagation site and consumer after the edits. Re-read and anchor every runtime-behavior claim in each edited section, holding those rows for the next actual dispatch's ground-truth ledger. P2+ items either get fixed or listed in a `## Deferred (P2+)` section. With `round_cap` 2, this is pass 1 only.
7. **If loop-red at first-invocation `P == round_cap`:** Targeted rewrite — classify each spec section as FROZEN (no unresolved P0/P1 in this invocation's earlier passes) or REWRITE. Build a closed-issues manifest from those earlier passes as regression constraints. No blank-slate rewrites. A full invocation whose cumulative start is not 1 still rewrites at its final `P`, not when `C == round_cap`. Delta passes never run this step.
8. **If loop-red after the final allowed pass:** Halt at cumulative round `C`. When reviewer P0/P1 titles remain, present them and ask the user what to do (patch manually, ship by hand, narrow the brief, or grill the remaining findings — a bounded interview scoped to those titles, whose own cap is 3, whose decisions route back through the in-place revise rules; it never re-dispatches reviewers and never increments `C`); options 1–4 stay. When no reviewer P0/P1 remains, Remaining P0/P1 is `GREEN WITHHELD: <D-ids>` and option 4 is not offered. Grill artifacts use `round-<C>/`.

**Round 2+ closure tracking:** This label describes the first invocation's pass index. A full invocation's first pass has no closure predecessor even when its cumulative round is greater than 1; later passes close the preceding pass. Delta pass 1 closes the candidate round. When a closure predecessor exists, each reviewer reads its reports (the three default lenses, plus `scalability.md` when the scaling lens ran) and produces a closure table showing CLOSED, PARTIAL, REOPENED, DEFERRED, or NEW. Reopened items are P0 unless the spec deliberately changed direction with rationale. In every dispatched round, including the first, each reviewer also checks the spec's `## Deferred — follow-up required` rows for well-formedness and does not re-file a finding whose root a well-formed row already carries. `DEFERRED` is not the closure state of an undischarged in-scope P0 or P1. After the reports are saved and before the gate break, the author writes `round-<C>/synthesis.md` (Act on / Consider / Noted / Dismissed). The gate sum does not read that file.

### Phase 3 — Drift-check checklist (hard stop)

When the spec goes green, render a structured checklist comparing the spec back to the brief. A review-produced green verdict (`source: review`) from a run under this rule is never written while an in-scope P0 or P1 sits undischarged in `## Deferred — follow-up required`. Attest mode and green markers issued before this change are outside this guarantee and are not edited. The checklist also shows that round's `synthesis.md` path and the deferred-row tally (`<u>` undischarged — `<out>` out-of-scope, `<op>` operator, `<x>` other — and `<d>` discharged; undischarged in-scope P0/P1 is 0).

- **Decisions carried in brief** — is each one preserved in the spec?
- **Done-when criteria** — is each one mapped to a spec section?
- **Out-of-scope fences** — does any spec section violate one?

Then stop. The user reviews the checklist and invokes the implementation skill separately.

### Verdict marker

spec-cycle records its verdict at `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`: green or red, the cumulative round and gate count, the date, and a fingerprint of the spec text that was judged (SHA-256 over the file with carriage returns removed and `**Follow-up:**` lines dropped, every other byte kept, so filing a follow-up ticket after green does not change it). `skills/spec-cycle/scripts/verdict_marker.py` owns the format: it computes the fingerprint, reads a marker into one of six states, and writes it. `round` is any positive completed review round, or `not reviewed`, or `in progress`; no field was added for delta mode. It is written at three points. Pending is written once per invocation immediately before the first dispatch; a failed write prints and the run continues. Red is written at the halt and names the halting cumulative round, which equals `round_cap` only when a full invocation began at round 1. Green is written after post-green polish. The downstream skills read this marker instead of parsing review reports. Attest mode, `/spec-cycle <path> --attest "<reason>"`, records a green verdict by hand when the review happened outside the loop: it checks the spec's headings, shows the current verdict, and writes an operator-attested marker only on confirmation. It resolves no review mode, dispatches no reviewer and edits no spec.

### Optional scalability lens

By default the loop runs the three standing lenses. A brief can turn on a **fourth, scalability lens** — the "case of N" advocate — by declaring scale a factor. The lens is **opt-in per brief**: absent the declaration the loop is unchanged (three standing lenses, identical gate arithmetic and closure-table output). There is no auto-detection — spec-cycle never guesses scale relevance from the spec body.

The toggle is an optional top-level `## Scale` section in the brief. Worked forms:

```markdown
## Scale
- **Factor:** yes
- **Target:** 10^6 records/day; 500 concurrent tenants; ≤ $0.002/op
- **Dimensions:** throughput, multi-tenant fan-out, cost-per-op
```

```markdown
## Scale
- **Factor:** no — single-invocation skill edit; N=1 by nature.
```

How it is read (Phase 0):

- **Heading** — a whole-word `## Scale` or `## Scaling` heading enables detection. `## Scaling considerations` / `## Scale-out plan` do **not** match, so an unrelated prose heading never becomes a false toggle.
- **Factor** — `**Factor:** yes` (or `on` / `true`) turns the lens **on** (a target is required, below); `**Factor:** no` (or `none` / `n/a`) records scale an explicit **non-factor**; anything else, or a missing `**Factor:**` line, leaves the lens **off**.
- **Target** — `**Target:** <N>` states the scale the design must hold at, in any unit (requests/sec, records, tenants, concurrent agents, $/op). It is what lets the lens score blocking (P0/P1) vs. advisory (P2+). `**Factor:** yes` with **no** `**Target:**` does **not** enable the lens — declare-don't-infer.
- **Dimensions** *(optional)* — `**Dimensions:** <free text>` names the scaling axes.

When on, the scalability reviewer is dispatched in the same parallel message as the standing lenses, saves to `round-<N>/scalability.md`, emits the same `STATUS:` contract, and folds its P0/P1 into the same gate and round-2+ closure tracking. A design architecturally unable to reach the declared target N is P1 (the scaling analogue of non-functional code); a self-contradiction against a declared scale "Done when" is P0; a concern that only bites *beyond* the declared target stays P2+. A declared non-factor is surfaced in the Phase 3 drift-check for human confirmation.

### Stakes tier

Ceremony follows a tier the operator sets at `/spec-brief`'s tier gate, after the seed gate and before the interview. Nothing writes a tier the operator did not choose.

| Tier | What changes |
|---|---|
| `tweak` | spec-brief only. Writes no brief, no spec, and no marker. The operator ships it as a chore PR. |
| `small` | spec-cycle keeps the three standing lenses and sets `round_cap` to 2. ship-spec skips the review gate and keeps the test gate. spec-brief offers the doubt pass when a reviewer is eligible. |
| `big` | Today's loop. `round_cap` is 4. ship-spec's three review-gate skip cases stay skips. An absent tier means `big`, with no warning. spec-brief offers the doubt pass when a reviewer is eligible. |
| `irreversible` | `big`, plus the tier on every reviewer prompt, plus a ship-spec review gate that stops instead of committing when the review did not run. It adds no lens. spec-brief requires a doubt pass: it halts before the interview when no reviewer is eligible, and a failed dispatch cannot skip. |

Scale stays its own `## Scale` declaration and never follows from the tier.

**Grammar.** In the brief, a whole-word heading matching `^#{1,6}\s+tier\s*$` (case-insensitive) opens `## Tier`. The body runs to the next heading. A `**Level:**` line, unfenced, after indentation, names `small`, `big`, or `irreversible`. Sibling lines are ignored. The first strict section wins and a second warns `tier: multiple Tier sections — using first`. No strict heading means `big` and `round_cap` 4, with no warning. A looser heading that merely starts with `tier` and whose body contains an unfenced `**Level:**` line, a strict section with no unfenced Level line, and a Level value of `tweak`, empty, an unknown token, or punctuation stuck to the token each warn `tier: <reason> — using big` and continue. A typo in the brief therefore reads as `big`; the warning is the only guard.

In the spec, the recorded tier is the first unfenced line that, after indentation, starts with `**Tier:**` (case-insensitive), wherever it sits. The value is the text after the label, trimmed, then lowercased. Exactly `small`, `big`, or `irreversible`. A second line warns `tier: multiple Tier lines in the spec — using first`. No label line at all means `big`, with no warning. Any other value, including empty or `tweak`: spec-cycle halts `tier: malformed (<value>) — halting`; ship-spec warns and uses `big`. A fenced example and a mid-line mention are not a declaration. Fences are a marker of three or more backticks or tildes; a blockquote neither opens nor closes one.

Once a spec exists, a valid recorded line wins over an absent, disagreeing, or malformed brief: warn `tier: brief <absent|disagrees|malformed> — using recorded` and do not halt. A recorded line outside the three values halts and does not fall through to the brief. ship-spec reads the spec line every time and never reads the brief for the tier. A bad recorded value halts in spec-cycle only; ship-spec warns. A marker `tier:` that is missing is not a disagreement. A tier mismatch warns, names both values, says the gate follows the spec tier, and continues. It does not ask for confirmation. When the spec has no label line, that warning says the spec tier is `big` because no line was recorded.

`round_cap` is 2 for `small` and 4 for `big`, `irreversible`, and an absent tier. In a full invocation, ordinary revision runs while pass index `P < round_cap`; `P == round_cap` is FROZEN/REWRITE. The FROZEN window is that invocation's earlier passes, not cumulative round numbers left by an older invocation. Delta mode has its own two-pass bound and never runs FROZEN/REWRITE. Grilling's interview cap of 3 is not `round_cap`.

A host that cannot wait at the tier gate prints `tier needs an operator — stopping` and stops. Nothing is written.

**Tweak hint.** spec-brief recommends `tweak` only when the ticket and grounding name at most 2 files, under about 50 lines, touching no auth, payments, data migrations, or config/CI; otherwise it recommends `big`, with one `basis:` line naming the files, lines and surfaces. The recommendation is advisory; the operator always picks.

---

## Optional stage: spec-tickets

**Purpose:** Break one green-lit spec into pieces that can each be verified alone, record which pieces block which, and file them as children of the spec's ticket — so the dependency graph, not a build order, says what can run in parallel.

**Invocation:** `/spec-tickets <path-to-spec>`

- **Input** — the green-lit spec file and nothing else. No brief, no ticket id, no conversation.
- **Verdict read** — preflight reads the spec's verdict marker. A red verdict halts before any draft; every other state is printed as a `Verdict:` line in the approval block, which approval confirms. No fingerprint is checked here.
- **Approval gate** — the skill prints the breakdown (pieces, acceptance criteria, blocking edges, the unblocked pieces) and waits. It files only on an explicit approval and never runs headless.
- **Three storage modes** — blocked-by relations when the tracker can write them; a `Blocked by` section on each child when it cannot; one local file per piece (`docs/specs/TODO/<TICKET-ID>.ticket-<slug>.md`) when no tracker is connected. A connected tracker that fails halts the run; it does not fall back to local files.
- **Filing** — blockers first, create-only. The first failed write stops the run with a report of what was and was not filed. There is no resume: a second run on a tracker files the pieces again.
- **ship-spec unchanged** — every piece lands on the spec's one branch and one PR. Skipping this stage changes nothing downstream.

The steps are in `skills/spec-tickets/SKILL.md`.

---

## Skill 2: ship-spec

**Purpose:** Take a green-lit spec through implementation, test gate, commit, PR, and issue-tracker update. Uses an isolated git worktree so the user's primary working tree is never touched, except a copy of an ignored test-output or review artifact into `docs/specs/TODO/` beside the spec; git does not track that copy, and no tracked file or git state in the primary checkout changes.

**Invocation:** `/ship-spec <path-to-spec> [--build-only | --from-review <worktree-path>]`. Build-only stops before review and cuts a new worktree. From-review checks the worktree, re-runs the tests, then reviews, commits, and opens the PR.

### Phase 0 — Preflight

1. **Read the spec.** Halt when it has no `## Done when` or no `## Test plan`. Red halts. Any other verdict warns and continues.
2. **Resolve the test command.** Priority: spec's `## Test command` section (authoritative for this change) > project's CLAUDE.md Build & Run section (fallback). If neither yields a runnable command, halt. If the test command is `N/A`, the automated test gate is skipped entirely.
3. **Discover the default branch** via `git symbolic-ref refs/remotes/origin/HEAD` (fallback: `git remote show origin`). Works for main, master, trunk, etc.
4. **Confirm GitHub CLI is authenticated** (`gh auth status`).

### Phase 1 — Worktree setup

Implementation runs in an isolated git worktree, not the user's checkout. This avoids stash/restore ceremony, preserves the user's uncommitted changes and branch state, and enables parallel ship-spec runs on different tickets.

1. Form branch name: `<type>/<ticket-id-lower>-<slug>` (e.g., `fix/proj-123-handle-empty-input`).
2. Worktree path: `<project-root>/../<TICKET-ID>-worktree` (sibling directory).
3. Check for worktree-path and branch conflicts — halt if either exists, don't auto-delete.
4. `git fetch origin <default-branch>` then `git worktree add -b <branch> <worktree-path> origin/<default-branch>`.

All subsequent phases run inside the worktree. The spec stays in the user's primary tree (it's metadata, not part of the code change).

### Phase 2 — Implement + author tests

Read the spec and implement everything it describes. Author the tests from the test plan. A regression comment uses the file's own comment syntax and the text `Regression for <TICKET-ID>: <one-line>`, not required to be `//`. Don't commit yet.

### Phase 3 — Test gate loop (up to 5 iterations)

Run the resolved test command. On failure: identify the smallest blocking issue, fix it, re-run. One fix per iteration — keeps the evidence trail clean. Capture full output to `docs/specs/TODO/<TICKET-ID>.test-output.txt`.

If still red after 5 iterations, halt and ask the user: continue with more iterations, drop into manual debug, or roll back and re-spec.

### Phase 3b — Review gate

One review of the change, between the green test gate and the commit. The project declares the review command (a `## Review command` section in the spec, else in `CLAUDE.md`, else in `AGENTS.md` — the first source that declares one wins); the skill names no reviewer of its own, and a missing command is a skip — one console line, one line in the PR body, no review file. A declared command that is unavailable or fails is also skipped, and recorded, for `big` and an absent tier. On `irreversible`, if the review did not run, stop instead of committing. `small` skips the review gate before the three cases, prints `review gate: skipped (small tier)`, writes no review file, and still runs the test gate. The review runs once, in a fresh read-only subagent when the host has one and inline otherwise; the reviewer reports findings and edits nothing. Each finding is mapped to one of three groups: Blocks, Fix or record, Record only. Before any fix is applied it passes a veto against the project's declared invariants and the test suite's shape, static, and adversarial pins; a vetoed fix is not applied. Blocks findings are fixed, and one that cannot be resolved halts the run for the operator with nothing committed. Fix-or-record findings are fixed or recorded with a one-line reason. If any fix was applied, the tests are re-run through the Phase 3 loop with a fresh count of 5; the review is not run again. The result is written to `docs/specs/TODO/<TICKET-ID>.review.md` and committed with the change when that path is not ignored; when it is ignored, the file is kept locally and copied to the primary checkout beside the spec, and the PR body says so. With an `N/A` test command the review gate still runs for `big`, `irreversible`, and an absent tier, and there is no test re-run. `small` skips the review gate even then.

### Phase 4 — Commit

Stage files explicitly (no `git add -A`). Commit with a conventional-commits message:

```
<type>(<ticket-id>): <summary, <=72 chars>

<2-4 sentence narrative>

<File-level change list or layer enumeration>
```

The message is passed with `git commit -F`. Don't skip pre-commit hooks.

### Phase 5 — Push and open PR

`git push -u origin <branch>`, then `gh pr create` with a structured body: summary bullets, files-changed table, test plan section linking the captured test output, or naming it as kept locally when that path is ignored.

### Phase 6 — Issue tracker update

Move the ticket to a review/in-review state. Comment on the ticket with the PR URL. If the tracker is unreachable, print manual instructions and continue.

### Phase 7 — Summary

Print the PR URL, spec path, branch, worktree path. The worktree stays alive for review fixes (the user can `cd` into it and push follow-up commits). After the PR merges, `/spec-land` is the post-merge step.

---

## Skill 2b: spec-land

**Purpose:** the post-merge step, after the PR is already merged and before `/spec-close`. On one confirmation it checks the landed tree against the head, base, and patch-id last recorded on the PR, moves the ticket to Done or to Post-merge Checklists, writes the wiki merge line and the filemap delta when a wiki is configured, then removes the worktree and the local and remote feature branch and runs the project's post-land command. It never merges, never commits, and never pushes anything except the remote branch delete.

**Invocation:** `/spec-land <PR-number | PR-URL | spec-path>`. No argument uses the current branch's PR. The working directory is the target repo.

The ordered steps, the marker read, and the cleanup rules are in `skills/spec-land/SKILL.md`. The latest-marker read (`latest`), the marker post (`post`, which `/ship-spec` and `/review-pr` call), marker parsing, the patch-id decision, and path overlap are `skills/spec-land/scripts/land_check.py`. The skill invokes that script and does not reimplement it.

---

## Skill 3: spec-close

**Purpose:** the close and harvest. `/spec-land` is the post-merge step; spec-close remains the close and harvest, once that step has run. In one pass it reconciles the spec against the code that actually shipped (a reconciliation report — the lone write before the confirmation checkpoint), proposes wiki entries from the difference (decisions, comprehension notes, state updates), archives the spec artifacts from `docs/specs/TODO/` to `docs/specs/DONE/<TICKET-ID>/`, and prepends an entry to the wiki's newest-first `log.md`. The issue tracker's state gates the mode: a completed ticket permits a full close, anything else offers a partial close. `--report-only` writes just the reconciliation report; `--partial` forces archive-only. See `skills/spec-close/SKILL.md` for the phase-by-phase detail.

---

## Adapting to your stack

The skills are designed to be tool-agnostic. The integration points to swap:

| This workflow uses | You'd replace with |
|---|---|
| Plane (issue tracker) | Jira, Linear, Asana, GitHub Issues, etc. |
| `mcp__plane__*` tools | Your tracker's API/MCP/CLI |
| `states.json` (maps ticket prefixes to project IDs and state UUIDs) | Your tracker's project/workflow config |
| `gh` CLI (PRs) | Your git host's CLI (`gh`, `glab`, Bitbucket API, etc.) |
| Wiki (conventions reviewer reads `decisions/`, `architecture.md`, etc.) | Your team's docs, ADRs, Confluence, Notion — or omit `wiki_root` |
| `docs/specs/TODO/<TICKET-ID>.*` file layout | Whatever path convention you prefer |

The things **not** to change (they're load-bearing):

- **Session boundary between spec-cycle and ship-spec.** Combining them is the #1 failure mode — context exhaustion mid-implementation with no recovery point.
- **Parallel multi-lens review.** Sequential reviews let later reviewers anchor on earlier findings instead of reading independently. Parallel dispatch forces independent reads.
- **Reviewers are read-only.** They never edit files. The orchestrator (spec-cycle) owns all edits. This prevents reviewers from "fixing" things in ways that introduce new issues.
- **STATUS line protocol.** Machine-parseable last line (`GREEN` or `RED P0=<n> P1=<n> ...`) gates the loop. The orchestrator sums P0+P1 across all dispatched reviewers.
- **Round 2+ closure tracking.** This means pass index on the first invocation. A full invocation's first pass has no predecessor even when cumulative `C > 1`; delta pass 1 closes the candidate round. Reviewers read all reports from the actual predecessor when a closure manifest is provided, and produce a closure table. Without this, the loop doesn't converge — reviewers re-raise issues that were already fixed.
- **Targeted rewrite at pass `P == round_cap`, not blank-slate.** Blank-slate rewrites regress closed findings. The FROZEN/REWRITE manifest preserves sections converged in the earlier passes of that full invocation. Delta passes never run it.
- **Worktree isolation in ship-spec.** Working in the user's checkout means you're one bad `git stash pop` away from losing their uncommitted work.
- **One test fix per iteration.** Bundling multiple fixes makes it impossible to attribute which fix resolved which failure.
