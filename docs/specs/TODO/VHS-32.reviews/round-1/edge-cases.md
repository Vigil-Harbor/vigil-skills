# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — round 1.

*Grounding completed: `docs/specs/TODO/VHS-32.spec.md`, `docs/specs/TODO/VHS-32.brief.md`, Plane VHS-32 via memory (namespace `skills`, tag-exact hit, confidence 1.00), `CLAUDE.md` (global + project), `AGENTS.md`, `skills/spec-cycle/SKILL.md` (620 lines; 2f verified at `:466–485`, step 7 at `:235`, 2c at `:390–410`, Tool-use notes `:569`, Failure modes `:577`), `docs/portability-contract.md` §2–§5, `lint.py`, `README.md`, `docs/spec-workflow-reference.md`. `python lint.py` run read-only: `0 error(s), 2 warning(s)` — `review-pr`, `ship-spec` — confirming the spec's checklist-1 baseline claim.*

## Findings

### F-1: `README.md` and `docs/spec-workflow-reference.md` cannot satisfy Done-when 9 — neither file mentions `/spec-close` today, and Design 5 adds none
**Severity:** P0
**Where:** spec § Design 5 (`:339–346`), § Test plan checklist 8 (`:368`), § Done when 9 (`:393`)
**Edge case:** Precondition violation — the spec assumes both docs already describe the three-stage lifecycle and only need a fourth stage prepended.
**What happens:** Checklist 8 ("each mention `/spec-brief` **and describe four stages in the order brief → cycle → ship → close**") fails at the `/ship-spec` gate, so the ship checklist blocks on a criterion no specified edit can produce.
**Why the spec misses it:** Verified against the files:
- `grep -n 'spec-close' README.md docs/spec-workflow-reference.md` → **no matches in either file.**
- `docs/spec-workflow-reference.md` `## ` headings are exactly: `Skill 1: spec-cycle` (`:7`), `Scale` (`:75`, `:82` — inside examples), `Skill 2: ship-spec` (`:97`), `Adapting to your stack` (`:162`). Adding "Skill 0: spec-brief" yields **three** documented skills, not four.
- `README.md` § Skills (`:9–11`) lists `/spec-cycle`, `/ship-spec`, `/review-pr`. Design 5 adds `/spec-brief`, `/grill-me`, and one `grilling` line — still no `/spec-close`, so the list is brief → cycle → ship → *review-pr*.

Only `AGENTS.md` (`:23–31`) actually enumerates three lifecycle skills and can renumber to four.
**Suggested fix:** Extend the Design 5 edits: add a `/spec-close <spec-path>` bullet to `README.md` § Skills and a `## Skill 3: spec-close` section (or a one-paragraph pointer) to `docs/spec-workflow-reference.md`, and add both to the § Scope table. Alternatively, narrow Done-when 9 / checklist 8 to "mention `/spec-brief` and place it first in the lifecycle order they document" and record the `/spec-close` doc gap as out of scope.

---

### F-2: Conversation-only mode accepts an empty or absent problem paragraph and writes a hollow brief
**Severity:** P1
**Where:** spec § Design 3 Phase 0 step 4c (`:231`), Phase 1 (`:237–244`), Phase 4 (`:263–283`)
**Edge case:** Empty input. Both ticket services are down (4c), the skill prints `describe the problem in a paragraph and I will proceed from that.` and waits — and the operator answers with nothing, one word, or `ok`.
**What happens:** `seed` is empty or near-empty → the design tree has no nodes → the frontier is empty on round 0 → `grilling` exits `empty-frontier` immediately → Phase 3 renders an empty preview → option 1 writes `docs/specs/TODO/<TICKET-ID>.brief.md` with the eight headers and empty (or model-invented) `## Problem`, `## Scope`, `## Done when`. `/spec-cycle` then consumes that file as the authority every one of the four lenses measures the spec against, and its Phase 3 drift check enumerates nothing. Nothing in the pipeline flags it: an `empty-frontier` exit is the *success* token.
**Why the spec misses it:** § Design 1.7 treats "empty frontier" as a normal exit and never distinguishes "nothing left to ask" from "nothing was ever known". There is no minimum-viable-seed gate anywhere in Phases 0–4, and § Failure modes (`:301`) lists five modes, none of which is an empty seed. Test-plan Run A (`:374`) exercises `empty-frontier` from a *good* seed only, so the transcript gate cannot catch it either.
**Suggested fix:** Add to Phase 0 step 4c: if the operator's paragraph is empty or under a stated floor (e.g. fewer than two sentences, or no verb-bearing problem statement), re-prompt once, then halt with `No problem statement — nothing to grill. Re-run /spec-brief when you have one.` Additionally, in § Design 1.7 split the exit token into `empty-frontier` vs `empty-seed`, and make Phase 3 refuse option 1 on `empty-seed`. Add a Run C transcript for it.

---

### F-3: A read-only exploration agent that hangs or crashes stalls the interview with no timeout, no cap, and no recovery — and no resume state exists
**Severity:** P1
**Where:** spec § Design 1.5 (`:158`), § Design 3 Phase 1 step 4 (`:242`), § Failure modes (`:301`), § Out of scope (`:410`)
**Edge case:** External-system failure — a dispatched exploration subagent hangs, times out, or crashes without returning.
**What happens:** § 1.5 says "Dispatch every fact need of a round in one parallel batch **before rendering the round**". A single non-returning agent therefore blocks the whole round from rendering — the operator sees no questions and no error. And because the spec explicitly keeps **no resume state** ("re-run to start over", `:301`, `:410`), an interview that stalls or is killed at round 3 of 3 loses every settled decision. There is also no cap on batch width: seven frontier questions each needing two facts is a fourteen-agent parallel dispatch, per round.
**Why the spec misses it:** § 1.5 covers exactly one failure shape — "an exploration that returns *without the fact*" — and maps it to a next-round `ℹ️` fact request. It has no branch for *does not return at all*. This is a solved problem elsewhere in the same file's neighborhood: `skills/spec-cycle/SKILL.md:404–410` explicitly handles "subagent crash, timeout, empty return" by writing a stub so the gate still has a summand. The new primitive inherits none of that discipline.
**Suggested fix:** In § Design 1.5 add: (a) a bounded wait — "if an exploration has not returned by the time the rest of the batch has, render the round without it and carry its question to the next round as an `ℹ️` fact request"; (b) a per-round dispatch cap tied to `question_cap`; (c) a crash/empty-return rule identical to (a). Add a matching `## Failure modes` bullet to `/spec-brief`.

---

### F-4: S5 exempts fact requests from `question_cap`, so the degraded path has no bound at all — and failed explorations recycle into more of them
**Severity:** P1
**Where:** spec § S5 (`:97–99`), § Design 1.5 (`:158`), § D6 (`:55–57`)
**Edge case:** Runtime precondition violation — the host has no read-only-by-construction agent class, so `facts_policy` = no and every fact need becomes an operator-facing `ℹ️` request.
**What happens:** S5 states verbatim: "*Fact requests do not count against `question_cap`.*" On the degraded path **every** fact need is a fact request, so a round can render 7 questions plus an unbounded number of `ℹ️` lines. The per-round question cap — one of the three bounds that are the entire point of the ticket (D6; brief Risk 1: "Interview fatigue is the failure mode that kills this") — is void precisely where the operator is doing the most manual work. The non-degraded path leaks the same way: § 1.5 turns a fact-less exploration into an `ℹ️` next round, with no limit on how many rounds that recycles.
**Why the spec misses it:** S5's rationale reasons only about *safety* ("a wrong fact is cheaper to correct than an unexpected mutation") and never re-checks the exemption against D6. Design 1.6 lists the three bounds but does not restate that fact requests sit outside one of them, so the reader of `grilling` § Bounds will not see the hole.
**Suggested fix:** Change S5 to: fact requests are capped separately at `question_cap` per round (or share the cap, with questions taking priority and facts overflowing by the S1 ordering rule). State the cap explicitly in § Design 1.6 alongside the other three bounds so the fence is visible where it is enforced.

---

### F-5: Phase 3 option 2 "Revise an answer" has no dependent-decision invalidation, no round budget, and an ambiguous question address
**Severity:** P1
**Where:** spec § S2 (`:79–81`), § Design 3 Phase 3 (`:250–261`), § S1 (`:77`)
**Edge case:** State corruption via re-entry. The operator revises a decision that other decisions in the same interview were settled *on top of*.
**What happens:** The design tree is explicitly prerequisite-ordered — "the **frontier** is every decision whose prerequisites are settled" (`:141`). Revising Q1 from branch A to branch B therefore invalidates every decision settled downstream of it, but the spec says only "re-enters the interview **for that question only**". The result is a `## Decisions carried forward` list that is internally contradictory: item 1 says B while items 3 and 5 were chosen assuming A. That list is the authority `/spec-cycle`'s four lenses measure the spec against, so the contradiction propagates as P0/P1 findings against the *spec* — exactly the cost the brief exists to avoid.

Two more undefined sub-cases on the same line:
- **"same bounds, rounds already used still count"** — after a `round-cap` exit, rounds used *equals* `round_cap`, so a revision has zero budget. Does it run anyway (violating the cap), or no-op back to the confirm prompt (an option-2 loop the operator cannot escape except by 1 or 3)?
- **"name the Q number"** — S1 says a carried-over question "keeps its number so the operator can track it across rounds", implying globally unique numbering, but § 1.3 renders `Q1`, `Q2`… per round with no stated global counter, and fact requests use a separate `F`-series. If numbers restart each round, `Q2` is ambiguous at the confirm prompt.
**Suggested fix:** In S2 option 2, state: revising a settled decision returns it *and every decision settled downstream of it* to the frontier, and those are re-asked (or moved to Open if the budget is exhausted); if `rounds_used == round_cap`, allow exactly one revision round and record the exit token as `revised-after-cap`. In § Design 1.3, pin question numbers as monotonic across the whole interview (`Q1…Qn`, never reset).

---

### F-6: Brief overwrite has no guard for an in-flight spec/reviews tree, and the Phase 4 write is not atomic
**Severity:** P1
**Where:** spec § Design 3 Phase 0 step 2 (`:226`), Phase 4 (`:263`)
**Edge case:** Partial failure + write-then-read race against a different skill. `/spec-brief VHS-40` is re-run on a ticket whose `/spec-cycle` has already produced `VHS-40.spec.md` and `VHS-40.reviews/round-1..3/`.
**What happens:** The collision check inspects only `docs/specs/TODO/<TICKET-ID>.brief.md`. The operator sees "Brief already exists — 1. Overwrite · 2. Abort", picks 1, and the brief is replaced. Every reviewer reads `brief_path` **fresh from disk each round** (`spec-cycle:349`; each reviewer's grounding step 2), so round 4 is now measured against a different axiom than rounds 1–3, and every CLOSED entry in the prior rounds' closure tables — and the round-4 closed-issues manifest built from them (`spec-cycle:446–460`) — becomes unverifiable. Nothing warns.

Separately, Phase 4 describes a single direct write of a fully-templated file. If it is interrupted (context cap, host kill, disk error) after the existing brief was truncated, the operator is left with a half-written brief and no copy of the original — and by design no resume state exists to recover the interview that produced it.
**Suggested fix:** Extend Phase 0 step 2's check to `docs/specs/TODO/<TICKET-ID>.spec.md` and `docs/specs/TODO/<TICKET-ID>.reviews/`; when either exists, print a stronger halt naming them (`A spec and N review rounds already exist for <TICKET-ID>. Overwriting the brief invalidates their closure tables.`) and require an explicit confirm. In Phase 4, require write-to-temp-then-rename, or a `<TICKET-ID>.brief.md.bak` copy taken before an overwrite.

---

### F-7: A settled "scale is a factor" decision with no Target emits a malformed `## Scale` section that `/spec-cycle` silently ignores
**Severity:** P1
**Where:** spec § Design 3 Phase 4 mapping rules (`:283`)
**Edge case:** Partial data — the operator settles the *factor* question but never supplies a target N.
**What happens:** The spec's rule is conditional on the factor only: "No `## Scale` section is emitted **unless a settled decision explicitly declared scale a factor**, in which case the section is written in the grammar `AGENTS.md` § Conventions specifies (`**Factor:** yes` + `**Target:**`)." Nothing requires the interview to have *elicited* a target. If the settled decision is "yes, scale matters" with no number, `/spec-brief` writes `**Factor:** yes` with an empty or absent `**Target:**`. `/spec-cycle` Phase 0 step 8's documented behavior for exactly that shape (`skills/spec-cycle/SKILL.md:598–600`) is: "A `## Scale` section with no parseable `**Factor:**`, or `**Factor:** yes` with no `**Target:**`, does **not** enable the lens — Phase 0 step 8 warns (`scale-lens: off (malformed…`)". So a decision the operator explicitly settled is silently discarded one stage downstream, the scalability reviewer never runs, and the only signal is a warning line in a different skill's preflight.
**Why the spec misses it:** § S4's own worked example uses the scale question ("Is scale a factor for this ticket — do we dispatch the scalability lens?") as the canonical *in-altitude* question, but the mapping rule at `:283` treats the answer as a single boolean and never makes `**Target:**` a prerequisite of emitting the section.
**Suggested fix:** In the Phase 4 mapping rules, state: emit `## Scale` only when the settled decision carries **both** factor and target; if the factor is settled `yes` with no target, the target is a prerequisite question — ask it in the same round (it is in-altitude by S4) or, if the interview has ended, carry it into `## Risks / decisions` as `Scale target — spec author pins this` and emit `**Factor:** no` is *not* acceptable; emit no section and print a warning naming the dropped decision.

---

### F-8: No stated behavior when the host cannot invoke a nested skill — the interview is silently skipped
**Severity:** P1
**Where:** spec § Design 2 (`:198`), § Design 3 Phase 2 (`:248`), § Design 4 step 2 (`:320`), § Design 3 Failure modes (`:301`)
**Edge case:** Runtime precondition violation on a non-Claude-Code host. All three call sites depend on one mechanism — "run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host)".
**What happens:** The portability contract's `requires:` vocabulary (§3: `shell`, `filesystem`, `network`, `subagents`, `services`) has **no token for "can invoke another skill"**, so a conforming harness cannot pre-flight this and cannot fail clearly on it (§3's "fail clearly, naming the unmet capability" is unreachable). On a host where model-invocable skill delegation does not exist, `/spec-brief` Phase 2 has no defined fallback: the most likely outcomes are a silent skip straight to Phase 3 — producing a brief indistinguishable from `--no-grill` but *without* the warning `--no-grill` prints in the preflight line (`:233`) — or an inline improvisation of the interview with none of the bounds. `/grill-me` degenerates to a 15-line stub that does nothing.
**Why the spec misses it:** § Design 3 § Failure modes enumerates five modes (ticket unresolvable, wiki missing, brief exists, operator abandons, `--rounds 0`) and omits the single most load-bearing dependency of the design. § Design 6's portability posture reasons only about *tool-name* portability (case-2 tagging), not about whether the delegation itself is portable. Brief Risk 5 anticipated the `Explore` degradation but not the `Skill` one.
**Suggested fix:** Add a `/spec-brief` and `/grill-me` failure mode: "**Host cannot invoke a nested skill.** Halt with `grilling is unavailable in this host — re-run with --no-grill to write the brief from the ticket alone, or run the interview manually.` Never write a brief silently ungrilled." Note in § Design 6 that "nested skill invocation" is a capability the contract's §3 vocabulary does not yet express, and either propose it as a contract revision or record it as an accepted gap in § Risks.

---

### F-9: `--questions 0`, non-positive, and non-integer flag values are undefined; `--no-grill` + `--rounds N` interaction is undefined
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 Invocation (`:221`), § Failure modes (`:301`)
**Edge case:** Malformed / boundary input on the two numeric flags.
**What happens:** The spec says the flags "accept positive integers" and separately defines `--rounds 0` → treated as `--no-grill` with a warning — an internal tension (0 is not a positive integer) that signals the boundary was considered for one flag only. Undefined today: `--questions 0` (a cap of zero renders zero questions per round, so `round_cap` empty rounds elapse and the brief is written with an empty `## Decisions carried forward` and the whole tree pinned in `## Risks / decisions` — nonsense output that reads exactly like a legitimate `round-cap` exit); `--rounds -1` / `--questions abc` (the only defined halt is for a malformed TICKET-ID); `--questions 999` (no upper bound, so a flag can defeat the fatigue bound the ticket exists to add); `--no-grill --rounds 3` together.
**Suggested fix:** In § Design 3 Invocation, state: `--rounds` and `--questions` must parse as integers ≥ 1 and ≤ a stated ceiling (e.g. 10 / 15); anything else → the same usage halt as a bad ticket ID. Keep `--rounds 0` as the one documented alias for `--no-grill`, or drop it in favor of the usage halt. State that `--no-grill` wins over any cap flags and warns that they were ignored.

---

### F-10: 2f-i's seed has no rule for a missing round-4 report, or for the synthetic missing-STATUS P0 that has no body
**Severity:** P2
**Where:** spec § Design 4 Edit 2 step 1 (`:319`), step 5 (`:323`)
**Edge case:** Malformed upstream artifact. 2f-i is reached precisely on the pathological path, where a reviewer may have crashed.
**What happens:** Step 1 says "Read the round-4 reports (`correctness.md`, `edge-cases.md`, `conventions.md`, plus `scalability.md` when the scale lens ran) and extract each remaining P0/P1 finding: id, severity, title, body." Two shapes break it:
1. **A standing lens returned nothing.** `spec-cycle` writes a stub only for a vanished *scalability* reviewer (`:404–410`); for a crashed standing lens the documented behavior is only "treat its report as `STATUS: RED P0=1 P1=0`" (`:579`) — the file may not exist. 2f-i has no read-failure branch.
2. **The synthetic missing-STATUS P0.** `spec-cycle:376–381` gives it a canonical form (`<lens>/STATUS (P0) "missing STATUS line"`), and it *does* count toward the gate that put the operator at the 2f halt. It has no body, and no operator decision can disposition it — it is a dispatch failure, not a design question. Grilling the operator on it wastes a round; skipping it silently makes step 5's `grill applied: <s> dispositioned, <o> left open` line under-count and misdescribe why the spec is still red.
**Suggested fix:** Add to step 1: "A round-4 report that is missing or unparseable, and any synthetic `missing STATUS line` P0, is **excluded from the seed** and listed verbatim in the step-5 re-render as `not grillable: <lens>/<id> — reviewer report unavailable; re-run /spec-cycle (option 1) to re-dispatch that lens.` It stays P0/P1 and is recorded as Open in `grill.md`."

---

### F-11: `grill.md` silently overwrites the prior invocation's audit artifact
**Severity:** P2
**Where:** spec § Design 4 Edit 2 step 3 (`:321`), § S8 (`:109–111`), § Done when 6 (`:390`)
**Edge case:** Re-entry across invocations. S8 bounds option 4 to "once per `/spec-cycle` **invocation**", and its own recommended next step is option 1 — "Patch manually and re-run `/spec-cycle`" — which produces a second invocation that can reach 2f and pick option 4 again.
**What happens:** Step 3 writes to the fixed path `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md` with no existence check. The second grill silently destroys the first, including the header line naming the earlier findings and date. Done-when 6 and the D8 rationale justify this file precisely as the record "`/spec-close` reconciliation can see why the spec changed after the halt" — and `/spec-close` archives `<TICKET-ID>.reviews/` wholesale (`skills/spec-close/SKILL.md:312, :339`), so what reaches `DONE/` is the last grill only, while the spec on disk carries edits from both.
**Suggested fix:** Make the path invocation-unique (`grill-<n>.md`, or append with a `---` separator and a fresh `# Grill — … — <date>` header rather than replacing). State the rule in step 3 explicitly: "never overwrite an existing `grill*.md`."

---

### F-12: The `--no-grill` path invents `Decisions carried forward` with no rule, no altitude fence, and no operator adjudication
**Severity:** P2
**Where:** spec § Design 3 Phase 3 (`:261`), § D9 (`:67–69`), § Failure modes `--rounds 0` (`:301`)
**Edge case:** The interview — the skill's only mechanism for keeping decisions with the operator — is switched off.
**What happens:** "With `--no-grill` the preview shows the Decisions list **as derived from the ticket text alone** and the confirm still runs." No derivation rule is given, no altitude fence applies (the fence is defined only as a `grilling` input, § 1.1), and nothing constrains how many decisions the model manufactures. D3 and D4 forbid the primitive from answering a decision on the operator's behalf; `--no-grill` routes around that prohibition entirely, and the sole guard becomes one yes/no confirm over a list the operator did not author. The resulting brief is byte-indistinguishable from a grilled one downstream — the References bullet `Interview: <n> rounds, exit <token>` (`:283`) has no defined value in this mode. `--rounds 0` inherits all of it.
**Suggested fix:** Pin the `--no-grill` derivation: decisions are extracted **only** where the ticket text states them explicitly (quote or `path:line` per item); anything the model would have to infer goes to `## Risks / decisions` ending "spec author pins this". Emit `Interview: skipped (--no-grill)` in References and in the `=== BRIEF WRITTEN ===` block so the two provenances are distinguishable.

---

### F-13: A single `defer` on a shallow node expands the Open frontier by an unbounded, never-shown subtree
**Severity:** P2
**Where:** spec § S7 (`:105–107`), § D7 (`:59–61`), § Design 1.8 (`:164–177`)
**Edge case:** Size limit on the emitted artifact. S7: a deferred question "stops blocking its descendants (**which are then also Open, not asked**)".
**What happens:** Deferring one root-level question moves its entire subtree to Open. Those items land in the brief's `## Risks / decisions`, each ending "spec author pins this" (D7) — items the operator never saw rendered, in a list with no size bound. Worse, the descendants of an unsettled node are generally *not enumerable* (the tree is discovered as decisions settle), so the primitive must either fabricate speculative descendants (noise in the authority artifact) or emit nothing for them (silently losing the frontier the cap-hit contract promises to preserve). The spec never says which.
**Suggested fix:** In S7, state the rule: only questions that were **rendered** to the operator enter the Open frontier as named items; the subtree below a deferred node is recorded as one rolled-up item — `<parent title> — downstream decisions not explored (deferred at round <n>); spec author pins this`. State a cap on `## Risks / decisions` items (e.g. `round_cap × question_cap`) in § Design 1.8.

---

### F-14: `subagents: true` is declared unconditionally, so a subagent-less host hard-fails pre-flight even though only fact-finding needs it
**Severity:** P2
**Where:** spec § Design 1 frontmatter (`:126–128`), § Design 2 (`:192–194`), § Design 3 frontmatter (`:211–215`), § S5 (`:97`), § S6 (`:101–103`), § Design 5 README (`:346`)
**Edge case:** Configuration drift / capability absence. Contract §3 gives an optional marker (`?`) only to `services`; booleans are required-or-absent, and "A harness MUST verify each **required** capability (no `?`) before any mutation and fail clearly."
**What happens:** On a host with no subagent affordance at all, `/spec-brief` and `/grill-me` fail pre-flight and produce nothing — even though the design already contains a working degradation for missing fact-finding (S5: ask the operator; § 1.1 `facts_policy` = no). S5 is written for the narrower case of "no agent class that is *read-only by construction*", which is satisfied by a host with write-capable subagents; the "no subagents whatsoever" case has no path. Related accuracy issue: the proposed README § Requirements line — "For `/spec-brief`: **nothing beyond Python** — it reads the ticket through Plane / shared memory when present and degrades to conversation when not" — understates the declaration (`shell: true`, `subagents: true`) and describes only the *services* degradation.
**Suggested fix:** Either keep `subagents: true` and state in all three bodies that fact-finding is the sole consumer and that a host lacking it should be run with `facts_policy: no` (adding a note that the contract's boolean fields cannot express optionality — a §3 gap worth its own ticket), or drop `subagents` from `grill-me`/`grilling` and declare it only where it is load-bearing. Reword the README Requirements line to name the actual capabilities.

---

### F-15: Invalid, free-form, or partial operator answers — and `stop` with explorations in flight — are undefined
**Severity:** P2
**Where:** spec § Design 1.3 (`:154`), § 1.4 (`:156`), § S7 (`:105–107`), § 1.7 (`:162`)
**Edge case:** Malformed input from the human. Each round ends with the literal `Answer by number. "defer" moves a question to the open frontier. "stop" ends the interview.`
**What happens:** Three shapes have no rule:
1. **An answer that is not a number, `defer`, or `stop`** — free prose ("neither, do X"), or a letter outside the rendered branches (`C` when only A/B exist). Treating it as an omission triggers S7's re-ask and burns a round; treating it as a new branch silently expands past the S3 three-branch cap.
2. **A partial answer** (6 of 7). S7's `(re-asked)` tag implies the round advanced and consumed one of three, so answering six questions costs the operator a third of the budget — defensible, but never stated, and the interaction with the S1 carry-over queue (a carried question plus a re-asked question can together exceed `question_cap`) is unspecified.
3. **`stop` mid-round with explorations in flight** — § 1.7 lists `stop` as an exit through the 1.8 hand-off, but does not say whether answers already given in the stopping round are recorded as Settled, or what happens to the pending explorations and the `### Facts established` block.
**Suggested fix:** Add to § 1.3: "An answer that is neither a rendered branch letter, `defer`, nor `stop` is treated as a **free-form answer** and recorded as the settled decision verbatim, provided it satisfies the altitude fence; otherwise re-ask once with `(clarify)`." Add to § 1.7: "`stop` settles every question answered in the current round, abandons in-flight explorations, and reports them under Open with `unresolved because: stopped`."

---

### F-16: `user_invocable: false` is unprecedented in this repo and informational on the one non-native target the contract names
**Severity:** P3
**Where:** spec § Design 1 frontmatter (`:125`, `:132`), § D9 (`:67–69`)
**Edge case:** Portability degradation of a guarantee, not a crash.
**What happens:** `grep -rn 'user_invocable' skills/` returns eight files, **all `true`** — `grilling` would be the repo's first `false`, so the flag has no shipped precedent and `lint.py` validates only `requires:` (R1) and `mcp__*` operativeness (R2); nothing checks it. Contract §2 says the flag is "Portable (mapped)" but that on Hermes "every skill is already a slash command, so the flag is **informational there**". D9's "never auto-invoked / never fired unprompted" therefore rests, on that harness, entirely on the sentence inside `description:` — and `description` is precisely the field that drives progressive disclosure and model selection, so a description naming three callers is also an invitation.
**Suggested fix:** Add one sentence to § Design 1 acknowledging the mapping loss and stating the second guard: `grilling`'s body opens with an explicit "invoked only by `/grill-me`, `/spec-brief`, or `/spec-cycle` 2f-i; if you reached this skill any other way, stop and ask the user" line, so the prohibition survives a harness where the flag does not.

## Summary
P0: 1 | P1: 7 | P2: 7 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=7 P2=7 P3=1 P4=0
