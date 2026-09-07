# Correctness Review — round 1

Grounding complete. All files read and anchors verified; the Plane ticket resolved from shared memory (namespace `skills`, tag_exact, confidence 1.00) and its Origin/Problem text matches the brief. `git log` on the touched files shows the most recent change to `skills/spec-cycle/SKILL.md` / `AGENTS.md` / `README.md` / `docs/spec-workflow-reference.md` is `a9e7581` (2026-06-16, VHS-15); nothing has shifted under the spec in the last 7 days. `5e6d401` (2026-09-02, reviewers pinned to Opus) is recent but touches only `agents/*`, which the spec declares untouched.

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: The documentation edits cannot satisfy the spec's own "four-stage lifecycle" criterion — neither `README.md` nor `docs/spec-workflow-reference.md` mentions `/spec-close` at all
**Severity:** P0
**Where:** spec § Design 5 (`:339–346`) vs § Test plan checklist 8 (`:368`) and § Done when #9 (`:393`)
**Claim:** Done-when #9: "`AGENTS.md`, `docs/spec-workflow-reference.md`, `README.md` describe the four-stage lifecycle." Checklist 8: "each mention `/spec-brief` and describe **four stages in the order brief → cycle → ship → close**." Design 5's edit to `docs/spec-workflow-reference.md` is only: line 3 becomes "An optional interview stage plus **two** AI-driven skills that split spec authoring from implementation…" plus a new `## Skill 0: spec-brief` section. Design 5's README edit is two `§ Skills` bullets plus one `§ Requirements` line.
**Why this is wrong:** `grep -n 'spec-close' docs/spec-workflow-reference.md README.md` returns **nothing** — neither file mentions `/spec-close` today. `docs/spec-workflow-reference.md` headings are `## Skill 1: spec-cycle` (`:7`) and `## Skill 2: ship-spec` (`:97`); there is no Skill 3. `README.md` § Skills (`:9–11`) lists exactly `/spec-cycle`, `/ship-spec`, `/review-pr`. Applying Design 5 verbatim yields:
- `spec-workflow-reference.md`: Skill 0 (brief) → Skill 1 (cycle) → Skill 2 (ship), with a new opening sentence that *explicitly says* "two AI-driven skills". Three stages, and the close stage still absent.
- `README.md`: `/spec-brief`, `/grill-me`, `/spec-cycle`, `/ship-spec`, `/review-pr`. Still no close stage.

Only `AGENTS.md` (`:23–29`, which already carries `/spec-close` as item 3) reaches four. So checklist 8 — which the spec designates "the gate for `/ship-spec`" — fails on two of three files as designed, and Done-when #9 is unmet.
**Suggested fix:** either (a) extend Design 5 to add the missing close stage to both files (a `## Skill 3: spec-close` section in `docs/spec-workflow-reference.md`, a `/spec-close <spec-path>` bullet in README § Skills), and change the proposed opening to "An interview stage plus three AI-driven skills…"; or (b) narrow Done-when #9 and checklist 8 to what Design 5 actually produces ("each names `/spec-brief` as the upstream stage; `AGENTS.md` describes all four"). Option (a) is the honest reading of the brief's own Done-when bullet.

---

### F-2: D8's seed definition ("exactly the titles the halt printed") excludes scalability findings, contradicting Design 4 step 1 — and the halt block does not print them
**Severity:** P1
**Where:** spec § D8 (`:65`) vs § Design 4 step 1 (`:319`); § Scope (`:25`)
**Claim:** D8: "the grill's seed is **exactly the remaining P0/P1 titles the halt printed** (bodies read from `round-4/*.md`)." Design 4 step 1: "Read the round-4 reports (`correctness.md`, `edge-cases.md`, `conventions.md`, **plus `scalability.md` when the scale lens ran**) and extract each remaining P0/P1 finding."
**Why this is wrong:** the current 2f halt block hardcodes three lens lines and no scalability line — `skills/spec-cycle/SKILL.md:469–473`:
```
Remaining P0/P1:
  - <round 4 correctness P0/P1 titles>
  - <round 4 edge-cases P0/P1 titles>
  - <round 4 conventions P0/P1 titles>
```
The scalability lens is a real fourth summand in the gate (`:415`, "summing across **all dispatched reviewers** … or four when the scalability lens is on") and its report is persisted as `round-<N>/scalability.md` (`:399–402`). So "the titles the halt printed" is a strictly smaller set than "remaining P0/P1", and the two spec sections disagree on the seed. Worse, the spec's § Scope pins the halt-block edit to adding one menu line and forbids changing "every line of `skills/spec-cycle/SKILL.md` outside the three named edit sites" — so the omission cannot be fixed incidentally. An implementer following D8 literally would silently drop scalability P0/P1s from the grill, which is precisely the "closure manifest silently dropped a P1" failure the brief cites (brief `:19`).
**Suggested fix:** make Design 4 step 1 canonical and restate D8 as "the grill's seed is every remaining P0/P1 in the round-4 reports (`correctness.md`, `edge-cases.md`, `conventions.md`, plus `scalability.md` when the lens ran)". Then either add a fourth `- <round 4 scalability P0/P1 titles (when the lens ran)>` line to the halt block and record it as a fourth edit site in § Scope, or state explicitly in 2f-i that the seed is read from disk, not from the printed list.

---

### F-3: `--rounds 0` gets two contradictory behaviors
**Severity:** P1
**Where:** spec § Design 3 "Invocation" (`:221`) vs § Design 3 "Failure modes" (`:301`)
**Claim:** Invocation: "`--rounds` / `--questions` accept **positive integers**; defaults 3 / 7 (D6)" — with "Anything else → halt: `Usage: /spec-brief <TICKET-ID> …`". Failure modes: "`--rounds 0` → treated as `--no-grill` with a warning."
**Why this is wrong:** `0` is not a positive integer, so the Invocation rule sends it to the usage halt; the Failure-modes rule proceeds to Phase 3 with the interview skipped. Both are definite and opposite specifications of a user-visible outcome; an implementer has no basis to choose. This is not resolvable by "the more specific section wins" — the Invocation rule is equally explicit about its rejection branch.
**Suggested fix:** pick one and delete the other. Recommended: keep the Failure-modes behavior and change Invocation to "`--rounds` accepts a non-negative integer (`0` ≡ `--no-grill`, with a warning); `--questions` accepts a positive integer. Anything else → halt: `Usage: …`" — and say what `--questions 0` does (currently unspecified; see F-12).

---

### F-4: "read-only by construction" over-claims what Claude Code's `Explore` agent guarantees — it retains shell access
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D1 (`:33`), § D2 (`:39`), § S5 (`:99`), § Design 1.9 (`:181`)
**Claim:** D1: "the only dispatch the primitive is allowed to make is a **read-only** exploration agent … Claude Code binding: the `Explore` subagent type with an Opus model override". S5: "if the host offers no agent class that is **read-only by construction** … **D1's guarantee is 'cannot write'**; a general-purpose agent forfeits it".
**Why this is wrong:** in this harness `Explore` is defined as "All tools except Agent, Artifact, ArtifactComments, ArtifactData, ArtifactCheck, ExitPlanMode, **Edit, Write, NotebookEdit**" — `Bash` is *not* excluded. An `Explore` agent can therefore mutate the tree (`git`, `rm`, redirection) despite lacking the file-edit tools. So the named Claude Code binding does not deliver "cannot write by construction"; it delivers "cannot write via the edit tools". This matters because `grilling` declares `requires: filesystem: [read]`, and portability-contract `§5` dimension 3 (`docs/portability-contract.md:129`) judges parity on "no mutations outside the skill's declared scope (`requires.filesystem`)" — a transitively dispatched shell-capable agent is outside that declaration. It also weakens S5's premise: the degradation is justified by a guarantee the primary path doesn't fully provide.
**Suggested fix:** soften the claim to what is true and add the missing belt-and-braces instruction. E.g. D2's operative sentence becomes: "Dispatch a read-only exploration agent on the strongest available model (Claude Code: the `Explore` subagent type with an Opus model override, or the equivalent narrowest read-only agent class in your host) — never a general-purpose agent, which inherits the full session tool set. **Instruct the agent to answer with `path:line` evidence only and to make no mutations of any kind**, since most host agent classes retain shell access even when file-edit tools are withheld." Adjust S5's "read-only by construction" to "read-restricted" and D1's parallel sentence to match.

---

### F-5: `user_invocable: false` is asserted to suppress the Claude Code slash command; nothing in the contract or the repo establishes that
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 (`:132`)
**Claim:** "`user_invocable: false` is the repo's portable 'model-invocable only' flag (contract §2: the intent travels; **Claude Code maps it to no slash command**)."
**Why this is wrong:** `docs/portability-contract.md:34` says only: "The intent 'a user can invoke this directly' is portable. **Claude Code → slash command**; Hermes → every skill is already a slash command, so **the flag is informational there**." It establishes the `true` direction only; it never states that `false` suppresses anything, and it explicitly says the flag is *informational* on the one non-Claude target the fleet has specified. `docs/specs/DONE/VHS-20/spec.md:153` confirms the adapter **drops** `user_invocable` outright: "every Hermes skill is already a slash command, so the flag is informational there." Every one of the eight shipped skills carries `user_invocable: true`, so there is no in-repo precedent for `false` behaving as claimed. The practical consequence: after `python sync.py install`, `/grilling` may still resolve as a slash command on Claude Code, and certainly will on Hermes — so `user_invocable: false` is a declaration of intent, not a mechanism.
**Suggested fix:** keep the frontmatter value (Done-when #1 requires it) but change the rationale sentence to something defensible: "`user_invocable: false` declares the intent 'this is a primitive, not a user command' (contract §2 classes the key Portable-mapped; on Hermes the flag is informational and the VHS-20 adapter drops it). The flag is advisory — the operative guard against unprompted use is the description's 'never fired unprompted' clause and D9."

---

### F-6: Design 3 renders Tool-use notes as bold prose, while Design 6 and checklist 2 require a `## Tool-use notes` heading
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 (`:299`) vs § Design 6 (`:351`) and § Test plan checklist 2 (`:362`)
**Claim:** Design 3: "**Tool-use notes** (non-operative inventory, contract §4 case 3): Read/Grep/Bash (`git log`, read-only) for grounding; **Agent** for read-only exploration; **Skill** for `grilling`; …" — a bolded inline label. Design 6 and checklist 2 both say the exemption applies "under a `## Tool-use notes` **heading**".
**Why this is wrong:** three cross-references disagree on the same construct. It is load-bearing in two ways: (a) checklist 2's grep condition (`\bAgent\b`, `\bSkill\b` must sit "under a `## Tool-use notes` heading") is not met by a bold label, so the spec's own gate would fail on a file written per Design 3; (b) `lint.py:57` matches the case-3 exemption on a markdown heading only — `_NOTES_HEADING_RE` is tested against `cur_heading`, which is set only by lines starting with `#` (`lint.py:216–217`). A bold label yields no heading context. The lint's v1 scope (`mcp__*` only, `lint.py:25–26`) means this doesn't produce an ERROR today, but it makes the file non-conforming the moment bare-name detection lands.
**Suggested fix:** change Design 3 to `## Tool-use notes` (a real heading, matching `spec-cycle`'s `:570` and `ship-spec`'s own convention), and keep Design 6 / checklist 2 as written.

---

### F-7: `facts_policy` is a dead parameter — no caller ever sets it, and its `no` semantics are undefined
**Severity:** P2
**Where:** spec § Design 1.1 (`:139`), § Design 3 Phase 2 (`:248`), § Design 4 step 2 (`:320`), § S5 (`:99`)
**Claim:** 1.1: "`facts_policy` — whether read-only exploration may be dispatched (default yes; **a caller on a host with no read-only agent class says no**, triggering S5)."
**Why this is wrong:** all three call sites hardcode the default. `/spec-brief` Phase 2: "`facts_policy` = yes". 2f-i step 2: "`facts_policy` = yes". `/grill-me` (Design 2) passes "brief altitude, and the default bounds" and never mentions it. Meanwhile S5 places the detection *inside the primitive* ("if the host offers no agent class that is read-only by construction, the primitive does **not** dispatch"). So the caller-side switch is never exercised, and the two mechanisms are redundant. If a caller did pass `no`, the spec never says what happens — whether every fact need becomes an `ℹ️` fact request (S5's shape), or the interview proceeds without facts.
**Suggested fix:** either delete `facts_policy` from 1.1 and let S5's primitive-side detection be the sole mechanism, or keep it and add one sentence to 1.1: "`facts_policy: no` produces the S5 shape unconditionally: every fact need is rendered as an `ℹ️` fact request rather than dispatched; fact requests do not count against `question_cap`." The first is smaller and matches how the three callers are written.

---

### F-8: Three stale line anchors in § References
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § References (`:428`, `:436`)
**Claim:** "`skills/spec-cycle/SKILL.md` … Phase 0 step 1 regex `:41–46`, … step 7 `states.json` `:~150`"; "`AGENTS.md:23–31` (lifecycle), `:97–105` (Conventions incl. `## Scale` grammar)".
**Why this is wrong:** verified against current files —
- `states.json` is Phase 0 **step 7 at `skills/spec-cycle/SKILL.md:235`**, not ~150. Line 150 is inside Phase 0 step 5 (origin-sync fetch). An 85-line miss into a different step.
- `AGENTS.md` § Conventions is `:88–96`; the `## Scale` grammar the spec relies on for Phase 4 is at **`AGENTS.md:95`**. `:97–105` is blank plus `## Post-merge wiki update` — a different section entirely.
- The Phase 0 step 1 regex is at `skills/spec-cycle/SKILL.md:43–48`, not `:41–46` (minor; the ranges overlap).

The load-bearing *edit-site* anchors in § Scope all verify clean: 2f `:466–485` ✓, Tool-use notes `:570` ✓, Failure modes `:578` ✓, 2e `:426–465` ✓, 2g `:487–518` ✓, Phase 3 `:520` ✓, `AGENTS.md:23–31` ✓, `README.md:7–11` and `:54–59` ✓, `docs/spec-workflow-reference.md:3` and `:7` ✓, `docs/portability-contract.md` §2 `:26–43` / §3 `:47–103` / §4 `:107–119` ✓, `skills/spec-close/SKILL.md:312, :339` ✓, `skills/ship-spec/SKILL.md:20` ✓, `lint.py:24–33` and `:45–48` ✓, `agents/spec-reviewer-conventions.md:3` and `:17–31` ✓, commit `5e6d401` dated 2026-09-02 ✓. Only the three above are wrong.
**Suggested fix:** correct to `states.json` `:235`, `AGENTS.md:88–96` (`## Scale` grammar at `:95`), regex `:43–48`.

---

### F-9: The two dry-run transcripts cannot be produced the way the Test plan describes
**Severity:** P2
**Where:** spec § Test plan "Dry-run transcripts" (`:372–375`)
**Claim:** "Both runs use a throwaway local-only ticket id (`ZZZ-1`) **inside the ship-spec worktree**. **Run A** — `/spec-brief ZZZ-1 --rounds 3` … **Run B** — `/spec-brief ZZZ-1 --rounds 1 --questions 3`."
**Why this is wrong:** two blockers, both already known to this repo.
1. A merged skill is inert until installed — the spec's own Risk 7 (`:422`) and brief Risk 7 (`:100`) say so, and `README.md:27` / `AGENTS.md:9–15` confirm `python sync.py install` is what puts a skill in `~/.claude/skills/`. Inside a `/ship-spec` worktree the new `skills/spec-brief/SKILL.md` is a file on disk, not an installed skill; `/spec-brief ZZZ-1` will not resolve as a slash command there. The transcripts must be produced by *reading the authored `SKILL.md` from the worktree and following it*, which is a different (and legitimate) procedure than the one written.
2. Both runs require an operator to answer each round before the interview can terminate (Design 1.4: "a round is not settled until the operator answers"). `/ship-spec` Phase 2 implements autonomously; there is no operator-in-the-loop step there. Run B additionally asserts an observable ("the round renders exactly 3 questions") that depends on the model's own tree decomposition, not on anything mechanically checkable.

Secondary: the transcripts land at `docs/specs/TODO/VHS-32.test-output.txt`, but with `Test command: N/A` `/ship-spec` explicitly *omits* the test-output link from the PR checklist (`skills/ship-spec/SKILL.md:197`) and from the summary (`:241`). The artifact will be committed but unreferenced.
**Suggested fix:** restate the transcripts as what they actually are — "authoring dry-runs performed by following `skills/spec-brief/SKILL.md` as written from the worktree (the skill is not installed at ship time), with the reviewer acting as operator" — and add one line telling the implementer to link `VHS-32.test-output.txt` from the PR body manually, since ship-spec's `N/A` branch drops that link.

---

### F-10: `grilling` declares `subagents: true` as a hard requirement, which forecloses the S5 degradation on a subagent-less harness
**Severity:** P2
**Where:** spec § Design 1 frontmatter (`:126–128`), § S5 (`:99`), § Design 2 (`:192–194`)
**Claim:** `requires: subagents: true, filesystem: [read]`, mirrored onto `grill-me` per S6. S5: "if the host offers no agent class that is read-only by construction, the primitive does **not** dispatch … It asks the operator for the fact."
**Why this is wrong:** `docs/portability-contract.md:78` — "A harness MUST verify each **required** capability (no `?`) **before any mutation** and fail clearly, naming the unmet capability." The `?` optional marker exists only for `services` (`:65`), never for booleans, so `subagents: true` is unconditionally required. On a harness with no subagent affordance at all, `/grill-me` must fail pre-flight — even though the skill has a complete, designed path (S5) that needs no subagent whatsoever. The declaration is therefore stricter than the skill's actual floor.
**Suggested fix:** either drop `subagents` from both `grilling` and `grill-me` (fact-finding is an optimization, not a floor — S5 is the fallback), or keep it and add one sentence to Design 6: "`subagents` has no optional marker in contract §3, so it is declared required even though S5 defines a no-dispatch path; a harness without subagents will fail pre-flight rather than degrade. Filed as a contract-vocabulary limitation, not fixed here."

---

### F-11: An explicit "scale is not a factor" answer is discarded, losing a distinction `/spec-cycle` supports
**Severity:** P3
**Where:** spec § Design 3 Phase 4 (`:283`), § S4 (`:94`), § Out of scope (`:412`)
**Claim:** "No `## Scale` section is emitted **unless** a settled decision explicitly declared scale a factor." S4 offers as an in-altitude example: "Is scale a factor for this ticket — do we dispatch the scalability lens?"
**Why this is wrong:** `AGENTS.md:95` defines three states, not two: "`**Factor:** yes` plus a `**Target:**` line … enables the lens; **`**Factor:** no` (or `none` / `n/a`) records scale as an explicit non-factor.** Absent the section, the lens stays off". `skills/spec-cycle/SKILL.md:238` resolves `scale_lens ∈ {on, non-factor, off}`, and Phase 1 (`:313`) treats `non-factor` differently from `off` — it records a carried-forward Decision so Phase 3's drift-check has an anchor. Under the spec's rule, an operator who is *asked* the S4 question and answers "no" produces a brief indistinguishable from one where the question was never raised. The interview's whole purpose is to make settled decisions visible.
**Suggested fix:** "When a settled decision addresses scale, emit `## Scale`: `**Factor:** yes` + `**Target:** <N>` when it is a factor, `**Factor:** no` when the operator explicitly settled it as a non-factor. Omit the section only when scale was never asked (out of altitude for this ticket)."

---

### F-12: Two under-specified branches in `/spec-brief`'s argument and confirm handling
**Severity:** P3
**Where:** spec § Design 3 Phase 3 (`:254–261`), § Design 3 Failure modes (`:301`)
**Claim:** Phase 3 confirm menu option 2: "Revise an answer (name the Q number) — re-enters the interview for that question only, same bounds, rounds already used still count." Failure modes cover `--rounds 0` but not `--questions 0`.
**Why this is wrong:** (a) S2 (`:81`) pins that "`--no-grill` skips the interview, **not the confirm**", and Phase 3 confirms this ("With `--no-grill` the preview shows the Decisions list as derived from the ticket text alone and the confirm still runs"). But under `--no-grill` there is no interview and no Q numbers, so option 2 has no referent — the menu offers an action that cannot be taken. (b) `--questions 0` is a positive-integer violation per Invocation but has no Failure-modes entry the way `--rounds 0` does; with S1's hard truncation it would render a round with zero questions and loop to the round cap.
**Suggested fix:** add to Phase 3: "Under `--no-grill`, option 2 reads `2. Add a decision (state it) — appended to Decisions carried forward`." Add to Failure modes: "`--questions 0` → halt with the usage line (a zero-width round is not a bound, it is a stall)."

## Summary
P0: 1 | P1: 2 | P2: 7 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=2 P2=7 P3=2 P4=0
