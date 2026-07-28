# VHS-15 — Optional scaling-advocate reviewer for /spec-cycle (the "case of N" lens)

## Goal

Add an **optional fourth review lens** to `/spec-cycle` — a scaling advocate (the "power-user for the case of N") that the spec author turns **on per-brief** when scale is a real factor. A new read-only `agents/spec-reviewer-scalability.md` is dispatched in the **same** parallel 2b message as the existing three, reads the same spec, emits the **same** `STATUS:` contract, and folds its P0/P1 into the **same** `total_p0p1` gate and round-2+ closure tracking. When the brief declares no scale factor (the default), spec-cycle's behavior is **unchanged** — identical dispatch (three lenses, no fourth `Agent` call), no `scalability.md`, identical gate arithmetic, identical closure-table output. (The dispatched 2b message is byte-identical to today; the small prompt-text edits to the three existing agents — Design §5 — are a behavioral no-op when the lens is off, not literally byte-identical agent files.) The point is to move the scaling argument upstream into the brief/spec, where direction is still negotiable, instead of discovering it at PR review when it is too late.

## Scope

### Files to create
- `agents/spec-reviewer-scalability.md` — the fourth reviewer agent, following the established reviewer shape (grounding → critique lens → shared severity definitions → output contract with a machine-parseable `STATUS:` last line), read-only.

### Files to change
- `skills/spec-cycle/SKILL.md` — the orchestrator. Edits, all additive/conditional:
  - **Phase 0:** new step 8 (*Scale-lens detection*) parsing the brief's scale declaration; preflight-summary token extended.
  - **Phase 1:** record the scale declaration in the spec as a carried-forward decision so Phase 3 can verify it.
  - **Step 2b:** conditionally append the scalability `Agent` call to the same parallel message **iff** the brief declares scale on; pass `scale_lens` (the current run's on/off resolution) to **every** dispatched reviewer and the extra `scale_target`/`scale_dimensions` to the scalability reviewer; reword the "Dispatch 3 reviewers" heading.
  - **Step 2c:** conditional `round-<N>/scalability.md` save path; a dispatched-but-absent scalability reviewer is persisted as a stub recording the dispatch failure (Design §3).
  - **Step 2d:** reword the gate to sum across *the dispatched reviewers* (already generic; tighten the prose that says "three").
  - **Step 2e:** generalize the round-4 closed-issues regression manifest (currently scans the three named report files, `SKILL.md:357–371`) to scan every report present per round, so a closed scalability finding survives as a round-4 regression constraint (Design §5).
  - **Phase 3:** render a *Scale declaration* drift-check block when scale is on (and a one-line note when explicitly marked a non-factor), consuming the `scale_lens`/`scale_target` resolved in Phase 0 — no re-parse.
  - **Description (frontmatter, line 3), line 17, line 475 (tool-use note):** reconcile "3-lens" prose to "three default + optional fourth."
  - **Failure modes:** add (a) the malformed / missing-target scale-declaration behavior, (b) the scalability reviewer's missing/malformed-STATUS and dispatched-but-absent handling, and (c) the lens-toggled-between-runs / stale-`scalability.md` pin.
- `agents/spec-reviewer-correctness.md`, `agents/spec-reviewer-edge-cases.md`, `agents/spec-reviewer-conventions.md` — **grounding step 7 only**: generalize the hardcoded three-file prior-round closure read to "every reviewer report present in `round-<N-1>/`" (with the stale-report guard: ignore a `scalability.md` when the run's `scale_lens == off`), and change "the other two lenses'" → "the other lenses'." Behavioral no-op when the lens is off (Design §5). This is closure-protocol plumbing, **not** a re-tuning of the critique lens or severity (see Decision 8).
- `AGENTS.md` — "Workflow" line 25, "Parallel review agents" section (line 33 + the agent table), "Conventions" line 68, the frontmatter-convention line 66 (agents carry only `name`+`description` — SSOT fix folded per round-2 conventions/F-1); and add the brief scale-declaration field to brief conventions.
- `README.md` — lines 9 and 15 (+ the reviewer list) reconciled to default-three / optional-fourth.
- `docs/spec-workflow-reference.md` — the clean-room reference: Phase 2 reviewer descriptions (lines 9, 39, 49), the closure-tracking invariant prose (lines 54 and 153, "reads all three prior-round reports"), the load-bearing-invariants list (lines 150, 152), plus a new subsection documenting the brief scale-declaration grammar and the optional-fourth-lens shape. This is the canonical home of the "brief schema" doc (Done-when bullet 4).
- `docs/portability-contract.md` — line 138, a count-neutral phrasing of the worked `subagents` example (spec-level addition, flagged in Decision 9).

### Files to leave alone
- `skills/ship-spec/**`, `skills/spec-close/**`, `skills/review-pr/**` — out of scope per the brief.
- `sync.py`, `lint.py` — no tooling change; `sync.py` already mirrors `skills/` and `agents/`, so the new agent ships with no `SUBTREES` edit.
- `skills/ship-spec/states.json` — unchanged.
- The shared severity rubric, the `total_p0p1` gate **formula**, and the ≤4-round cap — explicitly untouched (only prose that *counts* reviewers is reconciled).

## Decisions

Each maps 1:1 to a "Decisions carried forward" item in the brief; Decisions 9 names the two spec-level doc additions beyond the brief's named targets.

### Decision 1 — Opt-in, author-owned, off by default
The lens runs **only** when the brief explicitly declares scale a factor (Decision 3's grammar). Absent that declaration, no fourth `Agent` call is emitted and spec-cycle is behaviorally unchanged (identical dispatch, gate arithmetic, and closure-table output — see Goal and Decision 8 for the byte-identical-message vs. behavioral-no-op distinction). **No auto-detection or inference** — spec-cycle never guesses scale relevance from the spec body. This is a deliberate departure from VHS-15's "constant frame" lean, made with the requester this cycle: most fixes are genuinely small, and an always-on fourth lens taxes every pass (cost, convergence, false-positive scale findings on N=1 work) for no return. *If the council later wants always-on, only the toggle default flips — the rest of this spec stands.*

### Decision 2 — Implementation is option B (a new fourth agent), not option A (fold into edge-cases)
A standing, separately-scored `agents/spec-reviewer-scalability.md`, not a new dimension inside `spec-reviewer-edge-cases`. Resolves the ticket's open A-vs-B using the ticket's own stated risk for A: folding scale into edge-cases "risks diluting that reviewer's focus and burying scale findings under edge-case noise." The edge-cases-vs-scalability differentiator and the ticket's smell-list are written into the new agent's critique lens (Decision 6 / Design §1) so the lens never degenerates into re-finding edge cases.

### Decision 3 — One declaration, in the brief, with a target N
The toggle is a brief `## Scale` section that (a) names the scaling dimension(s) and (b) states the **target scale the design must hold at** (requests/sec, records, tenants, concurrent agents, $/op — any unit). The author may also mark scale an explicit **non-factor**, which is recorded and surfaced in the Phase 3 drift-check for human confirmation (no automated enforcement that the spec stays scale-free — the lens is off by definition). "Scaling matters" with **no** target is not actionable and does **not** enable the lens (Design §2 spells the exact grammar and the missing-target behavior): a target is what lets the lens score P0/P1 vs. advisory.

### Decision 4 — A peer reviewer, not a new stage — the pass budget is untouched
The lens is dispatched **within** round 2b alongside the existing three, in the same single parallel message, saved to `round-<N>/scalability.md`, emitting the same `STATUS: GREEN | RED P0=… P1=…` contract, read-only, never editing files or git state. Because it runs inside a round rather than adding one, the ≤4-pass cap and the session-boundary HARD STOP are unchanged. This directly answers the ticket's "does a 4th reviewer push past the pass budget?" — **no**.

### Decision 5 — Same severity scale; the opt-in toggle *is* the severity-calibration answer
The new agent reuses the shared P0–P4 definitions **verbatim** (no parallel ladder). Blocking severities apply **only** because the author declared the target N load-bearing:
- **P1** — the design as specified **cannot reach the declared target N** (architecturally unable). The scaling analogue of "non-functional code."
- **P0** — the spec **contradicts a declared scale "Done when"** (or is internally inconsistent / references nonexistent symbols, like any lens).
- **P2+** — concerns that only bite **beyond** the declared N, or "would be nicer at scale." Advisory, never blocking.

This resolves the ticket's worry that "a scale concern real only at 100× should not block a spec the way a correctness bug does": with opt-in + declared-N, it doesn't.

### Decision 6 — Scope is architectural *and* operational scale
The lens covers **structural** scaling (data structures, algorithmic complexity, fan-out/concurrency, batching/pagination, per-instance state collision) **and** **operational** scale (cost-per-op, latency, token/context budget under repeated/large-N invocation). The declared target N may be expressed in any of these units. Answers the ticket's third open question.

### Decision 7 — Security-first (pairs with the Petasos posture)
Scale is a security surface. The lens explicitly covers resource-exhaustion / DoS, missing rate-limits and backpressure, unbounded fan-out as an amplification vector, and cost-blowout as a denial vector. A scale-driven security regression is rated on the shared scale, **not** softened because it "only bites at N." The reviewer is parse-and-read-only — it never executes spec or skill content.

### Decision 8 — No regression of the lifecycle invariants
The session boundary, the three load-bearing existing lenses, read-only reviewers, the `STATUS`-line gate protocol, round-2+ closure tracking, and the Phase 3 drift-check HARD STOP are all preserved. The fourth lens is additive and gated; it cannot weaken the existing gate. The one edit to the existing three agents (grounding step 7, Design §5) is **closure-protocol plumbing** — generalizing which prior-round report files are read so the 4th lens's findings are tracked like any other — explicitly **not** a re-scoring or re-tuning of those lenses' critique behavior or severity (which the brief fences). It is a **behavioral** no-op when the lens is off: the generalized read resolves to the same three files and (per Design §5) explicitly ignores any stale `scalability.md` a prior on-run may have left, producing identical closure-table output. The agent-file *text* changes; its *behavior* when off does not.

### Decision 9 — Two doc reconciliations beyond the brief's named targets (spec-level additions, flagged)
The brief's Done-when names `AGENTS.md`, `SKILL.md` description, and `docs/spec-workflow-reference.md` as 3-lens reconciliation targets. Two more files carry the same now-incomplete "three" prose:
- **`README.md`** (lines 9, 15) — the repo's front door; leaving it stale would visibly contradict the reconciliation. Reconciled to default-three / optional-fourth.
- **`docs/portability-contract.md`** (line 138) — a worked `requires:`-schema example that says "dispatching three reviewers in parallel (`subagents`)." The `subagents: true` declaration is unchanged by this work; the count is illustrative. Reconciled to a count-neutral phrasing ("dispatching reviewer subagents in parallel") rather than chasing the number.

Both are flagged here so the conventions reviewer classifies them as spec-additions-with-rationale, not scope creep. If a reviewer judges `portability-contract.md` out of scope, it drops to a no-op without affecting any Done-when.

## Design

### §1 — The new agent: `agents/spec-reviewer-scalability.md`

Structurally identical to the other three reviewers (compare `agents/spec-reviewer-edge-cases.md`): YAML frontmatter (`name`, `description` — no `requires:`; agents are not skills), an opening role line, a **Mandatory grounding step**, a **Critique lens**, the **shared severity definitions** (verbatim) plus a scale-specific calibration paragraph, an **Output contract**, and **Tool-use rules** ending "Do not edit any file. You are read-only."

**Frontmatter.**
```yaml
---
name: spec-reviewer-scalability
description: Review an engineering spec for scalability — does the design hold at the brief's declared target N? Probes algorithmic complexity, per-item work that should be batched, unbounded accumulation, per-instance state collision, uncapped fan-out, single-valued config where a power user needs many, and operational scale (cost/latency/token budget). Dispatched only when the brief declares scale a factor. Returns severity-ranked findings with a machine-parseable STATUS line.
---
```

**Opening role line.** "You are a scalability reviewer for an engineering spec. Your single job: decide whether the spec's design **holds at the target scale the brief declares** — not whether it is correct at N=1 (correctness owns that) and not whether a single adverse input breaks it (edge-cases owns that), but whether the *architecture* survives N×."

**Grounding step.** Same ordered, non-optional shape as the peers. Inputs passed by the orchestrator: `spec_path`, `brief_path`, `project_root`, `ticket_id`, `namespace`, `round_number`, `closure_manifest` (round ≥2 only) — **plus** `scale_target` (the declared target N) and `scale_dimensions` (the declared axes). Steps: (1) read the spec fresh from `spec_path`; (2) read the brief; (3) retrieve the Plane ticket if `ticket_id` given, via the MCP memory server's search capability *(e.g. `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` in Claude Code, or the equivalent semantic-search tool in your host)* with `namespace`, `tags: ["plane_work_item","<TICKET-ID>"]`, `source_system: "plane"`, `max_results: 1`, falling back to the brief on zero results/error; (4) read `<project_root>/CLAUDE.md`; (5) read the actual files the spec proposes to change, to understand the per-invocation/per-item work and where it sits in a hot path; (6) identify the scaling-relevant axes (fan-out points, accumulation sites, external calls per item, shared/per-instance state); (7) **if `round_number ≥ 2`**, read every reviewer report present in `round-<N-1>/` (the three standing lenses plus its own `scalability.md`) and render a closure table as the first output section, same format as the peers. If `scale_target` is empty/absent in the prompt, record it as a finding and score everything advisory (P2 max). **This branch is a defense-in-depth backstop, not a contradiction with Design §2 rule 3:** under that rule the orchestrator never dispatches the lens without a non-empty `scale_target`, so in normal spec-cycle operation this branch does not fire. It exists so that a host which dispatches the agent directly (outside spec-cycle's gate) still fails safe — advisory-only rather than blocking on an unscored target. If any grounding step is blocked (file unreadable, MCP unreachable), record it as a finding and continue.

**Critique lens — does the design hold at N×.** The differentiator is stated up front, verbatim from the ticket/brief: *edge-cases asks "is it correct under one adverse input?"; scalability asks "does the design hold at N×?"* The lens must not re-file edge cases. Then the ticket's smell-list, written in as the hunt targets:
- per-item work that should be **batched** (per-item LLM calls / network round-trips / DB queries in a hot loop);
- **O(N)** (or worse) where **O(1)/O(log N)** exists; wrong data structure for the access pattern;
- **unbounded accumulation** (arrays/maps/logs/context that grow with N without a bound or pagination);
- **per-instance state that collides across instances** (a shared path / singleton / global / fixed filename / fixed lock when N instances run concurrently);
- **fan-out without a concurrency cap** (uncapped parallel dispatch, no backpressure);
- a **singular config / path / identifier** where a power user wants many (one hardcoded tenant/dir/key).

Operational axes (Decision 6): cost-per-op, latency, and **token/context budget** under repeated/large-N invocation (especially relevant since VHS specs are largely skill-shaped — a prompt that balloons with N is a scale defect). Security axes (Decision 7): resource-exhaustion / DoS, missing rate-limits/backpressure, uncapped fan-out as amplification, cost-blowout as a denial vector. For each finding the lens states the **declared target N it is scored against** — a concern with no path to the target is P1; a concern that only appears past the target is P2+.

**Severity.** The shared P0–P4 block, copied verbatim from the peer agents. Then, mirroring how edge-cases adds its own calibration line, a scale-specific paragraph: *"For scalability findings specifically: a design architecturally **unable to reach the declared `scale_target`** = P1 (the scaling analogue of non-functional code); a spec that **contradicts a declared scale 'Done when'** = P0; a concern that only bites **beyond** the declared target, or is merely 'nicer at scale,' = P2 or below. Score against the **declared** target N, never an imagined larger one."*

**Output contract.** `# Scalability Review — round <N>`, the round-≥2 closure table, `## Findings` with per-finding fields (`**Severity:**`, `**Where:**`, `**Scale axis:**` <which smell/axis>, `**Holds at target?:**` <where it breaks vs. `scale_target`>, `**Why the spec misses it:**`, `**Suggested fix:**`), `## Summary` line, and the mandatory last line `STATUS: GREEN` (P0==0 AND P1==0) or `STATUS: RED P0=<n> P1=<n> P2=<n> P3=<n> P4=<n>`. The optional `**Pre-ship recommended:** yes` line is permitted on P2 findings only, identical rules to the peers.

**Tool-use rules.** `Read`/`Grep`/`Glob` for spec/brief/CLAUDE.md/source; `Bash` for read-only git introspection only; the MCP memory search capability (tagged-example phrasing, to satisfy `lint.py` R2). Ends "Do not edit any file. You are read-only."

### §2 — The brief scale-declaration grammar (the toggle)

The brief carries an optional top-level section. Canonical worked forms:

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

**Deterministic detection** (spec-cycle Phase 0 step 8):
1. **Section heading:** the first line matching `^#{1,6}\s+scal(e|ing)\s*$` (case-insensitive, **whole-word** — `## Scale` and `## Scaling` match; `## Scaling considerations` / `## Scale-out plan` do **not**, so an unrelated prose heading never becomes a false toggle). The section body runs to the next `^#{1,6}\s` heading or EOF. No match → `scale_lens = off` (default; silent) — **except the near-miss tripwire:** if no whole-word heading matched but some heading line matches the looser `^#{1,6}\s+scal(e|ing)\b` *and* its section body contains a `**Factor:**` line, warn `scale-lens: off (heading "<text>" not recognized — use a bare "## Scale"/"## Scaling" heading to enable)` instead of staying silent. (A declared-intent drop should be visible, symmetric with rules 2 and 3; the lens still stays off, preserving the false-toggle protection.) If more than one whole-word heading matches, the **first** is authoritative; subsequent ones are ignored with a warning (`scale-lens: multiple Scale sections — using first`).
2. **Factor:** within the section, the first line matching `\*\*Factor:\*\*\s*(\S+)`; lowercase the captured token:
   - `yes` / `on` / `true` → candidate **on** (requires a target, below).
   - `no` / `off` / `none` / `non-factor` / `n/a` → `scale_lens = non-factor` (recorded; lens does **not** run).
   - anything else, or no `**Factor:**` line at all → `scale_lens = off`, warn `scale-lens: off (malformed declaration)`.
3. **Target (only when Factor is on):** the first line matching `\*\*Target(?:\s*N)?:\*\*\s*(.+\S)` → `scale_target`. If present and non-empty → `scale_lens = on`. If absent/empty → `scale_lens = off`, warn `scale-lens: off (factor=yes but no target — add a Target to enable)`. *(A declared-on lens with no target cannot score P0/P1, so an incomplete declaration must not silently enable it — declare-don't-infer, from the missing direction.)*
4. **Dimensions (optional):** `\*\*Dimensions:\*\*\s*(.+\S)` → `scale_dimensions` (free text; may be empty).

`scale_target` and `scale_dimensions` are captured as **opaque single-line text** (each regex stops at the line end, so neither can carry a newline). They are rendered as-is into the plain-text Phase 3 drift-check checklist and splatted into the scalability reviewer's prompt; because the surface is plain text (not a markdown table or persisted structured record), a stray `|`/backtick/`*` is at worst a cosmetic blemish in the printed checklist — no escaping is required. Authors should keep the target to a short single-line phrase; a future change to a *table*-shaped drift-check would need to revisit this.

Outputs carried to later phases: `scale_lens ∈ {on, non-factor, off}`, `scale_target`, `scale_dimensions`. Preflight-summary token (the full set of seven reachable values, matching §3 step 8): `scale-lens: on (target: <…>)` | `scale-lens: non-factor (recorded)` | `scale-lens: off` | `scale-lens: off (no target)` | `scale-lens: off (malformed declaration)` | `scale-lens: off (heading not recognized)` | `scale-lens: multiple Scale sections — using first`.

### §3 — spec-cycle integration edits (exact)

**Phase 0 — new step 8 (`Scale-lens detection`).** Inserted after step 7, before the preflight-summary paragraph. Runs the §2 detection against the brief located in step 2. Sets `scale_lens` / `scale_target` / `scale_dimensions`, **resolved once and held constant for the entire invocation** (so the per-round reviewer set is consistent across the loop). **Re-run pin (cross-invocation):** if `docs/specs/TODO/<TICKET-ID>.spec.md` already exists and carries a recorded scale Decision (written by Phase 1), that recorded decision — *as it exists at preflight* — is authoritative; if the brief's `## Scale` now disagrees, warn (`scale-lens: brief disagrees with recorded spec Decision — using recorded; align the brief's ## Scale with the recorded Decision, or edit/remove the Decision, to clear`) rather than silently flipping mid-tree. **Deliberate-off escape:** to intentionally turn the lens off after a prior on-run, the author edits or removes the recorded scale Decision in the spec (or deletes the spec to force a clean Phase-1 re-author from the now-off brief). The precedence is simply: *recorded Decision present → pin to it; absent → the brief governs.* The preflight-summary sentence (`SKILL.md:237`, the one listing the upstream and origin check tokens) gains a scale-lens token after the origin token and before "— then continue": `scale-lens: on (target: …) / non-factor (recorded) / off / off (no target) / off (malformed declaration) / off (heading not recognized) / multiple Scale sections — using first`.

**Phase 1.** One added instruction: when `scale_lens ∈ {on, non-factor}`, record the scale declaration in the spec as a carried-forward **Decision** (target N when on; the non-factor note otherwise), so Phase 3's drift-check has a spec anchor to verify against. No change when `off`.

**Step 2b.** Heading → "### 2b. Dispatch the reviewers in parallel". The three existing `Agent` calls are unchanged and always dispatched. Add, in the **same** single message, **iff `scale_lens == on`**:
```
Agent(subagent_type="spec-reviewer-scalability", prompt=<context>)
```
The shared prompt-params list (`spec_path`, `brief_path`, `project_root`, `ticket_id`, `namespace`, `round_number`) is unchanged, **plus one new param passed to every dispatched reviewer**: `scale_lens: <on|off>` — the dispatch-time collapse of the Phase-0 three-valued resolution (`on` stays `on`; both `non-factor` and `off` map to the reviewer-facing `off`). The three standing lenses use it solely to decide whether to read a prior-round `scalability.md` during closure tracking (Design §5); the scalability reviewer always receives `on`. A new sub-bullet states: *for the scalability reviewer additionally* — `scale_target: <from step 8>` and `scale_dimensions: <from step 8>` (mirroring the existing "for the conventions reviewer additionally" sub-bullet for `wiki_root`/`project_slug`). Note: when `scale_lens != on`, **no** fourth `Agent` call is emitted; the only difference from today's dispatch is the inert `scale_lens: off` param on the three standing prompts — a behavioral no-op (Design §5, Decision 8).

**Step 2c.** The save-path block gains a fourth line, applied only when the scalability reviewer was dispatched:
```
docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/scalability.md
```
If the scalability reviewer was dispatched but returned **no parseable report at all** (subagent crash, timeout, empty return), step 2c writes a **stub** `scalability.md` recording the dispatch failure (e.g. a one-line body + `STATUS: RED P0=1 P1=0`), so the gate has a summand and round-(N+1) closure tracking has an anchor. This mirrors the dispatched-but-absent handling in §4.

**Step 2d.** "sum of P0+P1 from RED status lines" already sums across whatever ran; reword "GREEN contributes 0" prose and any "three" references to "across all dispatched reviewers (three, or four when the scalability lens is on)." The gate **formula is unchanged** — only the count of summands varies, and only when scale is on.

**Step 2e (round-4 rewrite).** The round-4 targeted rewrite builds a **closed-issues regression manifest** by "scanning each round's three reviewer reports (`correctness.md`, `edge-cases.md`, `conventions.md`)" (`SKILL.md:357–371`). This is a **distinct artifact** from the round-2+ disposition `closure_manifest` (step 2b prose, `SKILL.md:290–313`) — and unlike that one it **hardcodes the three filenames**. Generalize it to "scanning every reviewer report present in each round's directory (`correctness.md`, `edge-cases.md`, `conventions.md`, plus `scalability.md` when the scaling lens ran)" so a scalability finding closed in rounds 1–3 survives as a round-4 regression constraint. The FROZEN/REWRITE logic and the round cap itself are untouched.

**Phase 3 — drift-check.** Consume the `scale_lens`/`scale_target` already resolved in Phase 0 step 8 — **no re-parse of the brief**. When `scale_lens == on`, render an extra block after "Out-of-scope fences":
```
Scale declaration:
  [ ] Target N: <scale_target> — addressed by the spec's design? (yes/no/note)
```
When `scale_lens == non-factor`, render a single line: `Scale: explicitly marked a non-factor in the brief — confirm the spec adds no scale machinery.` When `off`, render nothing (unchanged output). The existing "Brief-section parsing rules" (which enumerate numbered-list items under `Decisions`/`Done when`/`Out of scope`) are **not** extended to re-read `## Scale`; the drift-check renders the already-carried value, so there is a single source of truth for the parse (step 8).

**Description / line 17 / line 475 / Failure modes.** Frontmatter `description` and the line-17 summary: "a 3-lens parallel review" → "a parallel review (three default lenses, plus an optional fourth scalability lens when the brief declares scale a factor)". Line 475 tool-use note: "for the three reviewers" → "for the reviewers (three, or four when scale is declared)". Add three Failure modes:

- **Malformed or target-less scale declaration.** A `## Scale` section with no parseable `**Factor:**`, or `**Factor:** yes` with no `**Target:**`, does not enable the lens — spec-cycle warns (`scale-lens: off (malformed declaration)` / `(no target)`) and runs the unchanged three. Declare-don't-infer: an incomplete declaration never silently activates the fourth lens.
- **Scalability reviewer status drift / dispatched-but-absent.** A missing or unparseable `STATUS:` line from the scalability reviewer is handled by the existing reviewer-status-drift rule (synthetic `STATUS: RED P0=1 P1=0`); a dispatched reviewer that returns no report at all is treated identically and persisted as a stub `scalability.md` (step 2c). Either way the gate gets a blocking summand instead of silently dropping a scale concern — it cannot go green on a vanished reviewer.
- **Scale toggled between runs (stale `scalability.md`).** `scale_lens` is resolved once in Phase 0 and held constant for the whole invocation, so within a single converging run the per-round report set is consistent. Across separate invocations sharing a reviews tree, Phase 0 step 8 pins to the spec's recorded scale Decision (Phase 1 wrote it) and warns if the brief now disagrees rather than silently flipping. As a backstop, every reviewer receives `scale_lens`, and the generalized closure read (Design §5) ignores any `scalability.md` in `round-<N-1>/` when `scale_lens == off` — so a stale report from a prior on-run can never inject a phantom finding into an off-run's gate.

### §4 — Gate arithmetic with the fourth lens

`total_p0p1` is defined (step 2d) as the sum of P0+P1 across the RED status lines of **the dispatched reviewers**. With the lens on, the scalability reviewer's `STATUS:` line is one more summand — P0/P1 block, P2+ don't, identical to the peers. With the lens off, there is no fourth summand and the arithmetic is identical to today. No formula change; only the count of summands varies, and only when the author opted in.

A missing or malformed `STATUS:` line from the scalability reviewer needs **no new rule** — spec-cycle's existing "Reviewer status drift" failure mode (`SKILL.md:482`, written for "a reviewer") already maps it to a synthetic `STATUS: RED P0=1 P1=0`. In the round-2+ closure manifest that synthetic finding is represented as `scalability/STATUS (P0) "missing STATUS line"`, exactly like any lens (the manifest's missing-STATUS convention is already lens-agnostic). No edit to `SKILL.md:482` is required; the spec only needs to confirm the fourth lens is in scope of that rule, which it is by the rule's own "a reviewer" wording.

### §5 — Closure tracking with the fourth lens

Round-2+ convergence requires every round-N reviewer to see every round-(N−1) finding. There are **three** distinct closure artifacts in spec-cycle, and two of them hardcode the count "three" — both must be generalized for the fourth lens to fold in cleanly:

1. **Round-2+ disposition `closure_manifest` (orchestrator → reviewers; step 2b prose, `SKILL.md:290–313`, built in step 2e).** Already lens-agnostic — it is built from "every round-(N−1) P0/P1 finding," not from a per-lens file list. When the scalability lens ran, its P0/P1 dispositions (and any synthetic missing-STATUS P0, §4) appear in the manifest like any lens, with **no construction change**. A one-line note is added to the step-2b closure-manifest description making this explicit.
2. **Round-4 closed-issues regression manifest (step 2e round==4 branch, `SKILL.md:357–371`).** Hardcodes the three filenames. Generalized in Design §3 step 2e so a closed scalability finding survives as a round-4 regression constraint. *(This is the edge-cases P0 fix — the round-2+ manifest in (1) and this round-4 manifest are different artifacts; only this one named the files.)*
3. **Disk-read closure table (each reviewer, grounding step 7).** Each reviewer reads the prior-round reports from disk to verify the manifest's claims independently. Grounding step 7 currently enumerates exactly three files. Change (all four agents) to: *"read every reviewer report present in `round-<N-1>/` (the three standing lenses, plus `scalability.md` when the scaling lens ran)"*, and "the other two lenses'" → "the other lenses'".

   **Stale-report guard (the lens-toggle edge).** The generalized read in (3) also carries one condition: **when `scale_lens == off` for the current run, ignore any `scalability.md` present in `round-<N-1>/`.** It is stale from a prior on-run and its findings are out of scope for the current gate; rendering them would let a now-disabled lens inject a phantom REOPENED→P0. With the run-level `scale_lens` flag passed to every reviewer (§3 step 2b) plus the Phase 0 step-8 pin (a re-run reads back the spec's recorded scale Decision and warns if the brief now disagrees, rather than silently flipping), the off-run is a true behavioral no-op regardless of what files a prior on-run left on disk: it reads the same three reports and renders the same table.

   This is closure plumbing only — no critique-lens or severity change (Decision 8). When the lens has never run in the tree, every clause above resolves to "read the same three files" and the behavior is identical to today.

### §6 — Docs reconciliation (exact targets)

| File:line | Current | Reconciled to |
|---|---|---|
| `skills/spec-cycle/SKILL.md:3` | "a 3-lens parallel review loop" | "a parallel review loop (three default lenses, plus an optional fourth scalability lens)" |
| `skills/spec-cycle/SKILL.md:17` | "loop a 3-lens parallel review" | "loop a parallel review (three default lenses, plus an optional fourth when the brief declares scale)" |
| `skills/spec-cycle/SKILL.md:268` | "### 2b. Dispatch 3 reviewers in parallel" | "### 2b. Dispatch the reviewers in parallel" |
| `skills/spec-cycle/SKILL.md:270` | "Single message, three Agent tool calls" | "Single message, the reviewer Agent tool calls (three, or four when scale is declared)" |
| `skills/spec-cycle/SKILL.md:475` | "for the three reviewers" | "for the reviewers (three, or four when scale is declared)" |
| `AGENTS.md:25` | "a 3-lens parallel review loop" | "a parallel review loop (three default lenses + optional fourth scalability lens)" |
| `AGENTS.md:33` + table | "dispatches three read-only subagents" + 3-row table | "three by default (+ an optional fourth)"; add a `spec-reviewer-scalability` row marked *optional — dispatched only when the brief declares scale* |
| `AGENTS.md:66` | "Skills and agents use YAML frontmatter (`name`, `description`, `user_invocable`)." | "Skills use `name`, `description`, `user_invocable`; agents use `name`, `description`." (SSOT fix folded since AGENTS.md § Conventions is already being edited — closes round-2 conventions/F-1) |
| `AGENTS.md:68` | "shared across all three reviewers" | "shared across all reviewers (the three default lenses plus the optional scalability lens)" (count reconciliation only; the severity *rubric* is untouched — Decision 5) |
| `AGENTS.md` Conventions / brief notes | — | add the `## Scale` brief-field convention (one short paragraph + the on/non-factor forms) |
| `README.md:9` | "a 3-lens parallel review loop (correctness / edge-cases / repo-conventions)" | "…(correctness / edge-cases / repo-conventions, plus an optional scalability lens)" |
| `README.md:15` + list | "dispatches three reviewers in parallel" | "three by default, plus an optional fourth"; add the scalability lens to the list, marked optional |
| `docs/spec-workflow-reference.md:9` | "reviewed by three independent AI agents" | "reviewed by independent AI agents (three by default, plus an optional fourth scalability lens when scale is declared)" |
| `docs/spec-workflow-reference.md:39` | "Dispatch three reviewer agents in parallel" | "Dispatch the reviewer agents in parallel (three by default; a fourth, scalability, when the brief declares scale)" + a short paragraph describing the scalability lens beside the other three |
| `docs/spec-workflow-reference.md:49` | "Sum P0+P1 across all three reviewers" | "Sum P0+P1 across all dispatched reviewers" |
| `docs/spec-workflow-reference.md:54` | "**Round 2+ closure tracking:** Each reviewer reads all three prior-round reports…" | "…reads all prior-round reviewer reports present (the three default lenses, plus `scalability.md` when the scaling lens ran)…" |
| `docs/spec-workflow-reference.md:150,152` | "Three-lens parallel review" / "across all three reviewers" | "Parallel multi-lens review" / "across all dispatched reviewers" (keep the *parallel-dispatch* invariant intact — it is what is load-bearing, not the count) |
| `docs/spec-workflow-reference.md:153` | "**Round 2+ closure tracking.** Each reviewer reads all three prior-round reports…" | "…reads all prior-round reviewer reports present (the three default lenses, plus `scalability.md` when the scaling lens ran)…" (this load-bearing-invariant line goes stale under a fourth lens — caught by correctness/F-1 round 1) |
| `docs/spec-workflow-reference.md` (new subsection) | — | "Optional scalability lens" — the brief `## Scale` grammar (Design §2), how to set the target N, how to mark a non-factor; this is the Done-when "brief schema" doc |
| `docs/portability-contract.md:138` | "dispatching three reviewers in parallel (`subagents`)" | "dispatching reviewer subagents in parallel (`subagents`)" (count-neutral; Decision 9) |

`docs/spec-workflow-reference.md`'s "Adapting to your stack" / load-bearing list keeps "parallel dispatch," "read-only reviewers," "STATUS line protocol," and "round-2+ closure tracking" as invariants — none weaken; only the literal reviewer *count* is generalized.

## Test plan

No code ships — this is a markdown/prompt-logic change (one new agent, edits to one skill, three agents, four docs). The only mechanical gate in the repo is the portability lint (`lint.py`, per `docs/authoring-portable-skills.md`). The quality gate is the lint plus the structured review checklist below; the dispatch/gate/closure logic is prompt prose and is verified by inspection, not unit tests (consistent with how the existing three lenses are "tested").

**Automated (lint):**
1. `python lint.py --strict` over the new agent and the edited skill exits 0 — i.e., the new agent's memory-search reference uses the tagged-example form (`… or the equivalent …`) so it is not flagged `operative-tool-call`, and no `requires:`-block regression is introduced in `SKILL.md`. (Agents carry no `requires:` block; a `missing-requires` WARN on the agent is advisory and never gates `--strict`.)
2. `python lint.py` (warn-only) over the touched files surfaces no new ERROR.

**Review checklist (the human/quality gate):**
3. **Lens-off no-op.** A brief with **no** `## Scale` section (or `**Factor:** no`) ⇒ step 2b emits exactly the three existing `Agent` calls, no `round-<N>/scalability.md` is written, and `total_p0p1` sums three status lines. Confirm by reading the reconciled step 2b/2c/2d: the fourth call and save path are guarded by `scale_lens == on`.
4. **Lens-on dispatch.** A brief with `**Factor:** yes` + `**Target:** …` ⇒ a fourth `spec-reviewer-scalability` call in the *same* parallel 2b message, `scale_target`/`scale_dimensions` passed, report saved to `round-<N>/scalability.md`, P0/P1 folded into `total_p0p1`.
5. **Malformed / target-less declaration.** `## Scale` with no parseable `**Factor:**`, or `**Factor:** yes` with no `**Target:**`, ⇒ lens off + the documented warning; never silently enabled.
6. **Closure no-op.** With `scalability.md` absent, each existing agent's generalized step-7 read resolves to the same three files and the same closure table — behaviorally identical (the agent prompt text changes; its behavior when off does not).
7. **Stale-report guard.** With a `scalability.md` left in `round-<N-1>/` from a prior on-run but `scale_lens == off` this run, the three standing lenses ignore it (no phantom REOPENED→P0); the Phase 0 step-8 pin warns if the brief now disagrees with the recorded scale Decision.
8. **Round-4 manifest.** The round-4 closed-issues regression manifest (`SKILL.md:357–371`) scans every report present per round (incl. `scalability.md`) — a closed scalability finding survives as a round-4 regression constraint, not silently dropped.
9. **Reviewer-failure gate.** A scalability reviewer with a missing/malformed STATUS, or that returns no report at all, yields a synthetic `RED P0=1` (and a stub `scalability.md`) — the gate cannot go green on a vanished fourth reviewer.
10. **Severity reuse.** The new agent's P0–P4 block is verbatim the peers'; the scale calibration is an added paragraph, not a parallel ladder.
11. **Differentiator present.** The new agent's critique lens contains the edge-cases-vs-scalability differentiator and the full smell-list (Design §1).
12. **Docs consistency.** Locate every reviewer-count mention over the touched files (incl. `agents/spec-reviewer-*.md` and `docs/spec-workflow-reference.md`) with `grep -rinE "[0-9]+-lens|three (reviewer|lens|independent|read-only|agent|prior-round)|other two lenses"`. **Pass = the grep returns zero** after a faithful §6 implementation: every reconciled phrasing keeps "three" clear of the matched nouns (the §6 forms use "three default lenses" / "three by default" / "all prior-round reviewer reports present" — none of which the alternation matches), so any surviving hit is a bare/unqualified residual (e.g. "a 3-lens review", "dispatches three reviewers", "the other two lenses") to reconcile. The grep is a locator, not a semantic check — pair it with an eyeball pass over the §6 rows.
13. **Drift-check.** Phase 3 renders the Scale-declaration block when on, the non-factor line when so marked, and nothing when off — consuming the Phase 0 value, no re-parse.

## Test command

```
python lint.py --strict skills/spec-cycle/SKILL.md agents/spec-reviewer-scalability.md agents/spec-reviewer-correctness.md agents/spec-reviewer-edge-cases.md agents/spec-reviewer-conventions.md
```

Must exit 0. (Markdown/prompt change — no unit-test suite exists in this repo; the review checklist above is the substantive gate, per the spec-cycle doc-only/ops-only convention. `ship-spec` runs this command as its test gate; checklist items 3–13 are verified by inspection during review.)

## Done when

1. `agents/spec-reviewer-scalability.md` exists, following the established reviewer shape (grounding → critique lens → shared severity definitions → output contract with a machine-parseable `STATUS:` last line), read-only, with the edge-cases-vs-scalability differentiator and the ticket's smell-list in its critique lens. *(Design §1)*
2. `spec-cycle` step 2b **conditionally** dispatches the scalability reviewer in the same parallel message as the existing three **iff** the brief declares scale a factor; its report saves to `docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/scalability.md`; its P0/P1 fold into the step-2d `total_p0p1` gate and **all three** closure artifacts (the round-2+ disposition manifest, the round-4 regression manifest, and the per-reviewer disk-read closure table) exactly as the other lenses do. *(Design §3, §4, §5)*
3. When the brief carries **no** scale declaration (or marks scale a non-factor), spec-cycle's behavior is **unchanged** — identical dispatch (no fourth call), no `scalability.md`, identical gate arithmetic and closure-table output, even when a prior on-run left a stale `scalability.md` on disk — demonstrated by review-checklist items 3, 6, and 7. *(Design §3, §5; Test plan)*
4. The brief scale-declaration field is documented in `docs/spec-workflow-reference.md` (the "brief schema" home) and `AGENTS.md`: how to turn the lens on, how to state the target N, how to mark scale an explicit non-factor. *(Design §2, §6)*
5. The Phase 3 drift-check accounts for a declared scale target as a carried-forward decision, checked back against the spec. *(Design §3 Phase 3; Phase 1 records it)*
6. Docs/prose that hardcode "3-lens" are reconciled to the default-three / optional-fourth shape across `AGENTS.md`, `SKILL.md` description, and `docs/spec-workflow-reference.md` (and, per Decision 9, `README.md` and `docs/portability-contract.md`). *(Design §6)*

## Out of scope

- **Making the lens run by default or auto-detecting scale.** Opt-in per brief, full stop; auto-inference is rejected (Decision 1).
- **A fifth/Nth pluggable-reviewer framework.** Exactly one optional lens with a brief-level toggle; no reviewer-registry/plugin system (premature abstraction at N=1).
- **Re-scoring or re-tuning the existing three lenses**, or changing the shared severity rubric, the gate formula, or the round cap. (The grounding-step-7 closure-read generalization is plumbing, not lens re-tuning — Decision 8.)
- **Performance/load testing, benchmarking, or profiling of any target system.** The lens argues about scale at the *spec* level; it runs nothing and measures nothing.
- **Implementing Serenade / the Hermes autonomous-business agent / any hackathon deliverable.** Serenade is the forcing function, not a deliverable here.
- **Touching `/ship-spec`, `/spec-close`, or `/review-pr`.** Contained to `/spec-cycle` and its agents (+ the named docs).

## Deferred (P2+)

The P0/P1s and every pre-ship-recommended P2 from rounds 1–2 were addressed in-place. The new-in-round-2 P2s (near-miss heading tripwire, deliberate-off escape) and the round-2 P3/P4 clarity items (`scale_lens` collapse, the `:357–371` anchor, the preflight-summary anchor, and the `AGENTS.md:66` SSOT fix) were all folded as well. Remaining items are informational confirmations requiring no spec change, recorded so the human drift-check sees them:

- **conventions/F-2 (P3, round 1)** and **conventions/F-3 (P3, round 1)** — the README/portability-contract reconciliations are correctly flagged spec-additions-with-rationale (Decision 9); the grounding-step-7 edit is authorized closure plumbing (Decision 8).
- **conventions/F-3 (P3, round 2)** — decision-classification re-audit found one new (c) spec-addition (the §1 grounding empty-target backstop), properly flagged; no (d) silent additions.
- **edge-cases/F-1 (P3, round 3)** — the near-miss tripwire (§2 rule 1) is structurally skipped when a whole-word `## Scale` heading *also* exists, so a second, distinct near-miss heading carrying a real `**Factor:**` body could still be dropped silently. Genuinely narrow (requires two scale-ish headings in one brief), degrades gracefully (lens stays off by default), and the fix would add a new warning branch beyond a pure clarification — deferred rather than folded in 2g. Worth a follow-up if it ever bites.

## Post-green polish

Green at round 3 (all three lenses GREEN, P0=P1=0). The bounded post-green polish folded the round-3 pre-ship-recommended P2 clarifications (no behavior reversals, no scope/Decision/Done-when changes):

- **correctness/F-1 + conventions/F-1 (P2)** — restored the `AGENTS.md:68` §6 row (accidentally overwritten when the round-2 `AGENTS.md:66` row was inserted) and added a `SKILL.md:270` §6 row ("three Agent tool calls" → "the reviewer Agent tool calls (three, or four …)"), so the §6 "exact targets" table matches Scope and the item-12 grep gate is honestly satisfiable. Both are count reconciliations; the severity rubric is untouched (Decision 5).
- **edge-cases/F-2 (P2)** — re-synced the §2 "Preflight-summary token" enumeration (was 5 tokens) to the full seven reachable values, matching §3 step 8 verbatim.
- **edge-cases/F-3 (P3, error-message text)** — named the brief as the other lever in the "brief disagrees with recorded Decision" warning so a half-applied deliberate-off edit can reach a quiet steady state.
- **conventions/F-2 (P3)** — subsumed by the `SKILL.md:270` §6 row above.

