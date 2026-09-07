# VHS-32 — `/spec-brief`: a bounded grilling interview upstream of the spec loop

**Ticket:** VHS-32 (Plane `4f74afce-518e-4313-8105-43553c50693c`, Backlog, Medium)
**Brief:** `docs/specs/TODO/VHS-32.brief.md`
**Spec status:** GREEN at round 4 (post-green polish applied — see § Post-green polish)
**Change class:** markdown / prompt text only — no Python, no runtime state, no new dependencies (same profile as VHS-6, VHS-7, VHS-11)

## Goal

Add a fourth, upstream stage to the spec lifecycle — `/spec-brief` — so that the brief `/spec-cycle` treats as unchallengeable authority is produced by a **bounded, structured interview** rather than an unbounded ad-hoc prompt. The interview is extracted as a model-invocable primitive skill, `grilling`, that models the problem as a design tree, asks the whole settled frontier per round, states forks as weighed forks with an advisory recommendation, dispatches read-restricted exploration agents for facts instead of asking the operator, and stops on one of three bounds (round cap, per-round question cap, altitude fence). The same primitive is reused in two more places: a user-invocable `/grill-me` stub for ad-hoc use with no lifecycle artifact, and a fourth option in `/spec-cycle`'s post-round-4 halt menu that grills only the remaining P0/P1 findings and routes the decisions through the existing 2e revise path. Everything the brief lists as preserved stays byte-identical: the green gate, the ≤4-round cap, 2e FROZEN/REWRITE, 2g polish, the Phase 3 HARD STOP, the four reviewer agents, `/ship-spec`, `/spec-close`, `states.json`.

## Scope

| Path | Status | Change |
|---|---|---|
| `skills/grilling/SKILL.md` | **new** | The interview primitive. `user_invocable: false`; `requires: subagents: true, filesystem: [read]`. § Design 1. |
| `skills/grill-me/SKILL.md` | **new** | User-invocable stub delegating to `grilling` with defaults. `user_invocable: true`; `requires:` mirrors the primitive's (§ S6). § Design 2. |
| `skills/spec-brief/SKILL.md` | **new** | `/spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`. Resolves the ticket (both services optional), warn-only origin check, grounds against repo + wiki, runs `grilling` at brief altitude, confirms, then writes `docs/specs/TODO/<TICKET-ID>.brief.md`. `user_invocable: true`; `requires: shell: true, filesystem: [read, write], network: true, subagents: true, services: [issue-tracker?, shared-memory?]`. § Design 3. |
| `skills/spec-cycle/SKILL.md` § 2f (`:466–485`) | edit | The fenced halt block gains a scalability line in its `Remaining P0/P1` list (closing a three-lens hardcode VHS-15 left there) and a fourth menu option; the closing sentence is reworded; a new `### 2f-i` subsection is inserted between 2f and 2g. Round counter and gate untouched. § Design 4. |
| `skills/spec-cycle/SKILL.md` § Tool-use notes (`:570`) and § Failure modes (`:578`) | edit | One bullet each for the 2f-i skill invocation and its failure modes. § Design 4. |
| `AGENTS.md` § "Workflow: spec lifecycle" (`:23–29`) and § "Superseded vendor skills" | edit | "Three skills" → four; `/spec-brief` becomes item 1, the others renumber 2–4; one sentence naming `grilling` as the shared model-invocable primitive. One short paragraph (not a bullet — see § Design 5) in § Superseded vendor skills on the upstream name collision. § Design 5. |
| `docs/spec-workflow-reference.md` (`:3`, before `:7`, after `:161`) | edit | Intro sentence rewritten for four stages; new `## Skill 0: spec-brief` section (with `### The grilling contract`) before `## Skill 1`; new `## Skill 3: spec-close` pointer section before `## Adapting to your stack`. § Design 5. |
| `README.md` tagline (`:3`), § Skills (`:7–11`) and § Requirements (`:54–59`) | edit | Bullets for `/spec-brief`, `/grill-me`, and the missing `/spec-close`; a note that `grilling` is a model-invocable primitive; Requirements line for `/spec-brief`. § Design 5. |

**Files explicitly untouched:** `agents/*` (all four reviewers), `skills/ship-spec/**` (including `states.json`), `skills/spec-close/**`, `sync.py`, `lint.py`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `docs/customizing.md`, and every line of `skills/spec-cycle/SKILL.md` outside the three named edit sites (in particular Phase 0, Phase 1, 2a–2e, 2g, Phase 3).

**Scope note on `/spec-close` documentation (spec-addition with rationale).** `README.md` and `docs/spec-workflow-reference.md` do not mention `/spec-close` today — VHS-12 shipped the skill and updated the gitignored `CLAUDE.md` only. The brief's Done-when requires those two files to "describe the four-stage lifecycle", which is impossible without adding the third stage they never got. The addition is one bullet and one short pointer section, both pure documentation of a skill that already ships; nothing about `/spec-close` itself changes.

## Decisions

D1–D10 are carried from the brief. S1–S5 pin the five forks the brief explicitly deferred to the spec author ("spec author pins this"). S6–S9 are spec-level additions with rationale, authorized by neither brief nor ticket; each is small, and each exists because a reviewer lens or the design itself needed a rule the brief did not anticipate. Five further reviewer-driven additions are recorded at their point of use rather than as S-items, and are listed here so the drift check sees them: the warn-only origin check (Design 3 Phase 0 step 4), the artifacts-exist halt (Phase 0 step 2), the dot-prefixed tmp-then-rename write (Phase 4), the `## Scale` emission rule (Phase 4, per `AGENTS.md:95`), and the upstream name-collision note (Design 6 and `AGENTS.md` § Superseded vendor skills) — together with the Phase 4 emission rules these imply (the empty-Settled sentinel, the origin-annotated Scope heading, the Out-of-scope routing, the local-only header fields).

### D1 — Fact-finding subagents are read-restricted exploration agents on the strongest model, never general-purpose

Honored in `grilling` § Fact-finding (Design 1.5): the only dispatch the primitive is allowed to make is a read-restricted exploration agent, instructed to make no mutations. Claude Code binding: the `Explore` subagent type with an Opus model override on the call — `Explore` is a built-in with no agent file to carry `model:` frontmatter, so the override travels on the call. `general-purpose` is prohibited because it inherits the session's full tool set and permissions. Opus for the same reason as commit `5e6d401` (reviewers pinned to Opus): these answers become brief decisions.

**Honesty note (from round 1):** in Claude Code, `Explore` withholds the file-edit tools but retains shell access, so "read-only" here means *read-restricted by tool set plus instructed not to mutate*, not "cannot write by construction". The D2 sentence carries that instruction explicitly.

### D2 — The binding is expressed as portable intent; the Claude Code form is a parenthetical

`docs/portability-contract.md` §2 classes `model` and `allowed-tools` as Claude-Code-only. The exact operative sentence in `grilling` (echoed in `spec-brief` Phase 1) is:

> Dispatch a read-restricted exploration agent on the strongest available model (Claude Code: the `Explore` subagent type with an Opus model override, or the equivalent narrowest read-only agent class in your host) — never a general-purpose agent, which inherits the full session tool set. Instruct it to answer with `path:line` evidence only and to make no mutations of any kind: most host agent classes keep shell access even when file-edit tools are withheld. Bound its work in the prompt: answer from the paths named in the question, and return `not found` rather than searching exhaustively.

The prohibition and the no-mutation instruction are the operative content; the mechanism is a case-2 tagged example per contract §4. No bare harness tool name appears as an imperative anywhere in the three new files (the lint's v1 scope flags only `mcp__*`, but the authoring rule is applied to `Explore`, `Agent`, `Skill` too — § Test plan item 2).

### D3 — Facts are the agent's job; decisions are the operator's

Design 1.5: a frontier question that needs a repo/filesystem fact is dispatched, not asked. A running exploration is an unsettled prerequisite: only the questions downstream of it wait; the rest of the frontier is asked in the current round. Design 1.4 forbids the primitive from answering a *decision* on the operator's behalf.

### D4 — Forks are stated as forks, with weighed branches; the recommendation is advisory

Design 1.3 fixes the per-round output contract with the `For:` / `Against:` fork form and the plain form. Design 1.4 states the no-silent-default rule: a round is not settled until the operator answers; the primitive must not proceed on an unanswered question by taking its own recommendation. S3 pins the test for "genuinely branches".

### D5 — Ask the whole frontier in one round, then wait

Design 1.2: the frontier is every decision whose prerequisites are settled; a question that depends on another question open in the same round is deferred to a later round. No drip-feed.

### D6 — Three bounds: round cap (3), per-round question cap (7), altitude fence

Design 1.6. Round cap and question cap are per-invocation parameters with those defaults; `/spec-brief` exposes them as `--rounds` / `--questions` (bounded, § Design 3 Invocation). The altitude fence is a per-invocation *scope statement* the caller supplies: brief altitude for `/spec-brief` and `/grill-me` (only decisions that change the brief's Scope, Decisions carried forward, or Out of scope), finding scope for 2f-i (only decisions that disposition a named P0/P1). S1 pins hard truncation; S4 gives the worked examples. Fact requests share the per-round cap (S5), so nothing rendered to the operator is unbounded.

### D7 — Hitting a cap is a documented outcome, not a failure

Design 1.7: every termination except `empty-seed` (S9) ends through the same hand-off contract. Unresolved frontier items are returned as **Open**, and `/spec-brief` writes each one into `## Risks / decisions` as an item ending "spec author pins this" (the VHS-11 convention). The interview never blocks the brief from being written.

### D8 — The 2f grill is scoped to the named findings and cannot patch

Design 4: the grill's seed is **every remaining P0/P1 finding in the round-4 reports on disk** — `correctness.md`, `edge-cases.md`, `conventions.md`, plus `scalability.md` when the scale lens ran — which is the same set the (corrected) halt block prints, minus the not-grillable exclusions in Design 4 step 1 (dispatch failures, which stay P0/P1 and are reported, not interviewed). It produces decisions; `/spec-cycle` applies them through the 2e in-place revise rules. It never re-dispatches reviewers, never increments the round counter, and the primitive itself has no write capability (`filesystem: [read]`), so it *cannot* patch even if misprompted. Outcome persisted by the caller to `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`, append-only (S8).

### D9 — Grilling is never auto-invoked

`/spec-brief` runs it by contract (skippable with `--no-grill`); `/spec-cycle` 2f offers it as a menu choice; `/grill-me` is an explicit user command. `grilling`'s description names exactly those three callers and says it is not a user-facing entry point; its body opens with a guard sentence (Design 1.0). `user_invocable: false` is an *advisory* declaration of the same intent — contract §2 says the flag is informational on Hermes and the VHS-20 adapter drops it — so the guard sentence, not the flag, is the operative mechanism. Nothing in Phase 1 authoring, `/ship-spec`, or `/spec-close` references the primitive.

### D10 — Clean-room, not a port

Every sentence in the three new files is written fresh against the *behavior* summarized in the brief; no upstream text is copied. The design-tree / frontier idea is attributed to `mattpocock/skills` (MIT) in one "Origin" line in `grilling`'s body and in this spec — attribution of the idea, not of text. Same clean-room posture as VHS-28 toward the vendor handoff skill (the *supersession* mechanism differs — see Design 6 and Risk 13); precedent for an in-body attribution line is `skills/bloat-check/SKILL.md:19`.

### S1 — The per-round question cap is a hard truncation, not a soft target *(brief Risk 1)*

**Pin:** at most `question_cap` rendered items per round (questions and fact requests together); overflow is carried to the next round. **Rationale:** a soft target is not a bound, and "the brief is not bounded by anything" is the problem statement. The overflow already has a rule (D6), so truncation loses nothing. **Ordering** when truncating: carried-over and re-asked items first, then shallowest tree depth (a decision with more unsettled descendants unblocks more), then the primitive's judgment of blast radius on the brief's Scope. **Numbering is monotonic across the whole interview** — `Q1…Qn` never resets between rounds, so a carried item keeps its number and the confirm prompt's "name the Q number" is unambiguous. Fact requests use the parallel `F1…Fn` series.

### S2 — `/spec-brief` confirms before writing, even on an empty frontier *(brief Risk 4)*

**Pin:** confirm first. When the primitive hands back, `/spec-brief` renders the settled tree and open frontier as they will appear in the brief and shows the Phase 3 confirm block (fenced, one option per line, "Wait for the user's response." — the repo's halt idiom). **Rationale (the brief's own recommendation):** the brief is the artifact every downstream lens treats as authority; the cost is one prompt. `--no-grill` skips the interview, not the confirm. Option 2 ("revise") semantics are pinned in S7.

### S3 — The test for "genuinely branches" *(brief Risk 3)*

**Pin:** a question is rendered in fork form when **two or three** candidate answers each (a) are consistent with every decision already settled in this interview and (b) would produce a *different* line in the brief's Scope, Decisions carried forward, or Out of scope. If only one candidate satisfies both, use the plain form. More than three viable branches means the question is under-decomposed: split it into a prerequisite question (asked now) and its dependents (next round). **Rationale:** (a) removes branches the tree already pruned; (b) is the altitude fence restated. Capping at three keeps the fork table readable and forces decomposition instead of a menu.

### S4 — Altitude fence worked examples *(brief Risk 2)*

The `grilling` body carries these three contrasts verbatim (Design 1.6):

| In altitude (ask) | Out of altitude (do not ask — leave to the spec) |
|---|---|
| "Should the origin-sync check offer a fast-forward, or only warn?" — changes a Decision and the Out-of-scope fence on mutation. | "Should the fast-forward use `git merge --ff-only` or `git pull --ff-only`?" — same Decision either way; the spec pins the command. |
| "Is scale a factor for this ticket — do we dispatch the scalability lens, and at what target N?" — adds or removes a Scope row. | "What regex detects the `## Scale` heading?" — implementation of an already-settled Scope row. |
| "Does `/spec-brief` write Plane state, or only read the ticket?" — Out-of-scope fence. | "Which `states.json` key does `/spec-brief` read the namespace from?" — the spec author reads the file. |

### S5 — Degradation when no read-restricted agent class exists, and the fact-request bound *(brief Risk 5)*

**Pin:** the primitive detects, at its first fact need, whether the host offers an agent class that withholds file-edit tools (Claude Code: `Explore`). If none exists, it does **not** dispatch a write-capable agent. It renders the fact as a fact request, distinguishable from a decision question: `ℹ️ **F1 — <fact needed>**: … *(no read-restricted agent available in this host)*`. The same rendering is used when a dispatched exploration fails (Design 1.5). **Fact requests count against the per-round cap** exactly like questions (S1 ordering puts carried items first). A fact request the operator leaves unanswered twice becomes an Open item ("fact not established") rather than recycling forever. **Rationale:** D1's guarantee is "cannot write"; a general-purpose agent forfeits it, and a wrong fact is cheaper to correct than an unexpected mutation. Round 1 showed that exempting fact requests from the cap voided D6 on exactly the degraded path where the operator does the most work. There is no caller-side `facts_policy` switch — detection is the primitive's job, and no caller had a reason to set it.

**Contract limitation, recorded not fixed:** `requires.subagents` is a boolean with no optional marker (contract §3 gives `?` only to `services`), so `subagents: true` is a hard pre-flight requirement. A host with *no* subagent affordance at all fails pre-flight rather than degrading to fact requests, even though S5 would work there. The brief's Scope row fixes `subagents: true` for `grilling`, so this spec keeps it and records the gap in § Risks; relaxing the contract vocabulary is its own ticket.

### S6 — `grill-me` declares the primitive's `requires:` transitively *(spec addition)*

**Pin:** `skills/grill-me/SKILL.md` carries `requires: subagents: true, filesystem: [read]` — identical to `grilling`. **Rationale:** contract §3 says a harness verifies the *invoked* skill's declaration before running it and must not infer capabilities from the body. A stub that declares nothing would pass pre-flight and then fail at point of use inside the delegate. Mirroring is the cheapest honest declaration.

### S7 — Unanswered, deferred, free-form, and revised answers *(spec addition)*

**Pin:**
- **`defer`** (or an equivalent explicit skip) moves the question to the Open frontier at once. Its descendants are *not* enumerated or asked; the subtree is recorded as **one** rolled-up Open item: `<parent title> — downstream decisions not explored (deferred at round <n>)`. Only questions actually rendered to the operator ever become named Open items.
- **Omitted** (no answer given): re-asked at the top of the next round with its original number and a `(re-asked)` tag, counting against that round's cap; omitted again → treated as `defer`. A partially answered round still consumes one round of budget — that is the price of D4's no-silent-default rule, and the spec says so where the operator sees it (Design 1.3's closing line).
- **Free-form** (neither a rendered branch letter, `defer`, nor `stop`): recorded verbatim as the settled decision if it satisfies the altitude fence; otherwise re-asked once with a `(clarify)` tag. A free-form answer never adds a fourth branch to the rendered fork — it *replaces* the fork with the operator's answer.
- **Revise** (Phase 3 option 2, by global Q number): `/spec-brief` re-invokes `grilling` with the returned Grill summary as `prior_summary` (Design 1.1) and the same `round_cap` / `question_cap`; the primitive owns the resume arithmetic: the named decision **and every decision settled downstream of it** return to the frontier and are re-asked, `rounds_used` carries over, and if the budget is already exhausted the primitive itself grants **one** post-cap round for that resume and exits `revised-after-cap (+1 round)`. `/spec-brief` offers option 2 at most once after a cap hit; after that resume returns, the confirm re-renders with options 1 and 3 only. Downstream items that do not fit go Open. Under `--no-grill` there are no Q numbers, so option 2 reads `Add a decision (state it)` instead.

**Rationale:** D4 forbids the primitive from taking its own recommendation on silence, but an interview that deadlocks on one skipped line, or that lets an upstream answer change while its dependents stand, produces the contradictory brief the ticket exists to prevent.

### S8 — 2f-i runs once per halt; `grill.md` is append-only *(spec addition)*

**Pin:** option 4 may be chosen once per `/spec-cycle` invocation. After the grill's decisions are applied, the 2f menu re-renders with options 1–3 only, preceded by a one-line outcome summary. `grill.md` is never overwritten: a later invocation's grill (reached via option 1 → re-run) appends a new block — `---`, then `# Grill <k> — <TICKET-ID> round 4 — <ISO datetime> — findings: <ids>` where `<k>` is one more than the number of lines matching `^# Grill ` already in the file (anchored — the `## Grill summary` line inside each block is not one) — so `/spec-close`'s archived copy carries every grill that shaped the spec. The append is written read-modify-tmp-rename (the Phase 4 discipline), so a kill mid-append leaves the prior file intact; under concurrent invocations sharing the reviews tree the append is last-writer-wins over the whole file — a concurrent grill can be lost and nothing detects it; accepted, since grilling one ticket's round 4 from two sessions is outside the supported flow (Risk 14). The once-per-invocation bound is held in context only: `/spec-cycle` records no preflight timestamp, so no on-disk signal distinguishes this invocation's grill from a prior one. An existing `# Grill` header this session did not write does not withhold option 4; the `<k>` counter makes any duplicate visible in the audit trail after the fact (Risk 14). **Rationale:** the gate is unchanged by the grill (no reviewer has verified the edits), so the honest next step is option 1; and the whole point of `grill.md` is an audit trail.

### S9 — An empty seed is a halt, not an empty frontier *(spec addition)*

**Pin:** `/spec-brief` gates the seed before the interview: if the ticket text (or the operator's local-only paragraph) states no problem — under two sentences, or nothing a design decision could hang off — it re-prompts once, then halts with `No problem statement — nothing to grill. Re-run /spec-brief when you have one.` In ticket mode the re-prompt is `Ticket <ID> states no problem — describe it in a paragraph and I will proceed from that.`; the brief header keeps the resolved ticket line and the paragraph becomes the seed. In local-only mode the re-prompt repeats Phase 0 step 5c's request. The primitive independently distinguishes `empty-seed` (no frontier at round 1 because the tree has no root) from `empty-frontier` (tree fully visited) and returns the former as a distinct exit token; callers treat `empty-seed` as a halt and never write on it (`/spec-brief`: halt per Phase 2; 2f-i: the Design 4 step 1 guard means the primitive is not even invoked; `/grill-me`: Design 2). **Rationale:** a success token for "nothing was ever known" writes a hollow brief that every downstream lens then treats as authority.

## Design

### 1. `skills/grilling/SKILL.md` — the primitive

Target length ≈ 170 lines. Section skeleton, with load-bearing sentences given verbatim where the wording is the contract.

**Frontmatter**

```yaml
---
name: grilling
description: Bounded design interview primitive. Models a problem as a design tree, asks the whole settled frontier each round with weighed forks and an advisory recommendation, dispatches read-restricted exploration for facts, and stops at a round cap, a per-round question cap, or an altitude fence. Not a user-facing entry point — invoked only by /grill-me, /spec-brief, and /spec-cycle's post-round-4 halt (option 4). Users who want to be grilled run /grill-me.
user_invocable: false
requires:
  subagents: true
  filesystem: [read]
---
```

`user_invocable: false` declares the intent "this is a primitive, not a user command". Contract §2 classes the key Portable-mapped; on Hermes the flag is informational and the VHS-20 adapter drops it, and no shipped skill in this repo has used `false` before — so the flag is advisory. The operative guard is the body's opening sentence (1.0). The description carries **no user-phrase triggers** (those live only in `grill-me`), so the two skills do not compete for "grill me on this". No `disable-model-invocation`, no `model`, no `allowed-tools` — all Claude-Code-only.

**1.0 Guard.** The body opens with: *"This skill is invoked only by `/grill-me`, `/spec-brief`, or `/spec-cycle` 2f-i. If you reached it any other way, stop and ask the user whether they meant `/grill-me`."*

**1.1 Invocation contract (inputs).** The caller supplies, in prose or as a labelled list:

- `seed` — the problem statement and any grounding facts already established. `/grill-me`: the user's topic. `/spec-brief`: the ticket's problem statement plus Phase 1 grounding. 2f-i: the remaining P0/P1 findings with their bodies.
- `altitude` — the fence, stated as *which artifact lines a decision must change to be askable*. Default (brief altitude): "a decision that changes the brief's Scope, Decisions carried forward, or Out of scope." 2f-i supplies: "a decision that dispositions one of the listed findings."
- `round_cap` (default 3), `question_cap` (default 7).
- `prior_summary` (optional) — a Grill summary this primitive returned earlier in the same session, plus the Q number to revise. This is the only resume path, and it exists for the S7 revise case alone. The resume contract, carried verbatim in the body: the primitive rebuilds the tree from the summary; Settled items stay settled except the named one and everything downstream of it, which re-enter the frontier; prior Open items stay Open and are not re-asked unless downstream of the revised decision; Facts established carry over and are not re-dispatched; Q/F numbering continues the prior series; `rounds_used` carries over from the summary's `rounds:` field. **If `rounds_used ≥ round_cap`, this invocation runs exactly one additional round and exits `revised-after-cap (+1 round)`; a further `prior_summary` arriving with `rounds_used > round_cap` exits `round-cap` at once.** The caller decides whether to offer a resume at all.

**1.2 The design tree and the frontier.** Origin line: *"The design-tree / frontier framing is adapted from the `grilling` skill in `mattpocock/skills` (MIT); the text here is original."* Then: every decision branches into the decisions that hang off it; the **frontier** is every decision whose prerequisites are settled. Each round asks the whole frontier (D5), capped (S1). After answers, settled decisions push the frontier outward; recompute and ask again. A question that depends on a question still open this round belongs to a later round. If the seed yields no root decision at all, exit `empty-seed` at once (S9).

**1.3 Per-round output contract.** Fork form (D4), verbatim from the brief:

```
❓ **Q1 — <title>**: <body>

  **A.** <branch> — *For:* <…>  *Against:* <…>
  **B.** <branch> — *For:* <…>  *Against:* <…>

➡️ **Recommend B** — <one line of why>
```

Plain form for non-branching questions: `❓ **Q2 — <title>**: <body>` / `➡️ <recommended answer>`. Fact requests (S5) use `ℹ️ **F1 — …**`. Numbers are monotonic across the interview (S1). Each round ends with the literal lines:

```
Answer by item number: a question by number and branch letter (e.g. `Q3 B`), a fact request by number and the fact (e.g. `F1 <answer>`); a plain answer is recorded as given. "defer" moves a question to the open frontier.
"stop" ends the interview. Unanswered questions are re-asked once, then deferred; a partly answered round still uses one of your <round_cap> rounds. Round <n> of <round_cap>.
```

and the primitive **waits**. On the single post-cap resume round the last sentence reads `Round <round_cap>+1 of <round_cap> (post-cap revision round — the last).` instead, and the 1.8 header renders `rounds: <round_cap>+1/<round_cap>`.

**1.4 Decisions are the operator's.** Verbatim: *"The recommendation is advisory. It is never a default that carries by silence: a round is not settled until the operator answers, and this skill must not proceed on an unanswered question by adopting its own recommendation."* Then S7's omitted / defer / free-form rules and the 1.1 resume contract.

**1.5 Fact-finding.** The D2 sentence verbatim. Detection first (S5): if the host has no read-restricted agent class, every fact need is a fact request. Otherwise, dispatch every fact need of a round in **one parallel batch, capped at `question_cap` dispatches**, before rendering the round; questions downstream of a fact wait, the rest are asked now (D3). Fact needs beyond the dispatch cap carry to the next round's batch by the S1 ordering; if the interview ends first they reach the hand-off as Open with `unresolved because: fact not established`. A dispatch that errors, returns empty, or returns without the fact is a **failed dispatch**: its question is carried to the next round as an `ℹ️` fact request, and the round renders without it. Where the host reports a timeout, treat it identically. Where it does not, a dispatch that never returns blocks the round it belongs to — no prompt-level construct can cancel a pending dispatch (§ Risks 12); the dispatch cap bounds how many can hang, and the D2 prompt bounds each one's work. Facts, with their source paths, are carried into the hand-off (1.8). Retrieval-first: if the caller supplied wiki/state context in `seed`, consult it before dispatching. No resume state is kept beyond `prior_summary` (1.1): if the session ends mid-interview, the caller re-runs (`/spec-brief` § Failure modes).

**1.6 Bounds.** The three bounds with defaults (D6), the shared-cap and ordering rule (S1, S5), the single post-cap resume round (1.1), the S3 branching test, and the S4 examples table verbatim. Closing sentence: *"Implementation detail is the spec's job. Asking it here duplicates `/spec-cycle`."*

**1.7 Termination.** Exits: `empty-frontier`, `round-cap`, `stop`, `revised-after-cap (+1 round)` (the suffix is part of the rendered token), and `empty-seed`. `empty-frontier` is reachable only after at least one round was rendered; if the tree has a root but no round-1 candidate satisfies the altitude fence, the exit is still `empty-frontier` but the 1.8 header's reason reads `no candidate decision met the altitude fence` rather than `tree fully visited`, so callers can tell the two apart (a distinct token and a 2f-i re-offer are deferred — § Deferred). All but `empty-seed` go through 1.8; `empty-seed` returns the token and a one-line reason. On `stop`, every question answered in the stopping round is Settled, in-flight explorations are abandoned, and their questions are Open with `unresolved because: stopped`. *"Reaching a cap is a documented outcome, not a failure; the caller decides what to do with the open frontier."*

**1.8 Hand-off contract (output).** The primitive ends by rendering exactly this block in-conversation and returning; it writes no file:

```
## Grill summary — <seed title> (rounds: <n>/<round_cap>, exit: empty-frontier | round-cap | stop | revised-after-cap (+1 round); reason: tree fully visited | no candidate decision met the altitude fence | cap reached | operator stop | resume)

### Settled
1. **<decision title>** (Q<n>) — chose <A/B/free-form answer>: <one line>. Facts relied on: <F-ids or "none">.

### Open frontier
1. **<question title>** (Q<n>) — branches: <A/B>; recommendation: <X>; unresolved because: <round-cap | deferred | stopped | fact not established | blocked-on: Q<m>>.
2. **<parent title> — downstream decisions not explored (deferred at round <n>)**

### Facts established
- F1 — <fact> (source: <path:line>)
```

The Open frontier is bounded by construction at `(round_cap + 1) × question_cap` named items plus one rolled-up item per deferred subtree. Callers map this: `/spec-brief` → Settled becomes `## Decisions carried forward`, Open becomes `## Risks / decisions` items ending "spec author pins this", Facts feed Scope and References. 2f-i → Settled drives the 2e edits, Open stays in the red list.

**1.9 What this skill never does.** Writes a file; edits a spec or brief; dispatches a write-capable agent; invokes `/spec-cycle`, `/ship-spec`, or `/spec-close`; answers a decision on the operator's behalf.

**1.10 Tool-use notes** (a `## Tool-use notes` heading — contract §4 case 3): the read-restricted exploration agent (Claude Code: `Explore` with an Opus override); Read/Grep for consulting seed-supplied paths. Nothing else.

**1.11 Failure modes** (a `## Failure modes` heading, pairing with 1.10 as every lifecycle skill does): four lines pointing at the rules rather than restating them — failed dispatch (1.5), no read-restricted agent class (S5), `empty-seed` (1.2 / 1.7), `stop` with explorations in flight (1.7).

### 2. `skills/grill-me/SKILL.md` — the user stub

≈ 20 lines.

```yaml
---
name: grill-me
description: Interview me on a plan, decision, or idea until the design tree is settled or a bound is hit. Ad-hoc — produces no lifecycle artifact. Use when the user says "grill me", "stress-test this", "poke holes in this plan".
user_invocable: true
requires:
  subagents: true
  filesystem: [read]
---
```

Body: invoked as `/grill-me <topic>`. One operative paragraph: *"Run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host) with `seed` = the topic the user gave, brief altitude, and the default bounds (3 rounds, 7 questions). When it hands back, the Grill summary is the deliverable — write nothing to disk."* Two failure-mode lines: *"If this host cannot invoke a nested skill, say so and stop: `grilling is unavailable in this host`. Never improvise the interview inline — the bounds live in the primitive."* and *"On `empty-seed` (no topic, or a topic with nothing to decide), report the primitive's one-line reason and stop — there is no summary to deliver."* S6's `requires:` mirror is explained in one sentence ("declares what the delegate needs, so pre-flight is honest").

### 3. `skills/spec-brief/SKILL.md` — the lifecycle stage

Target length ≈ 230 lines. Mirrors `/spec-cycle`'s phase structure and reuses its idioms (fenced halt blocks + "Wait for the user's response.", `states.json` lookup via the `<config-dir>` resolution `/spec-close` uses, warn-only origin check in `/spec-close`'s shape) rather than inventing new ones.

**Frontmatter**

```yaml
---
name: spec-brief
description: Produce the brief that /spec-cycle consumes. Resolves a ticket (issue tracker optional — degrades to conversation), grounds against the repo and wiki, runs the bounded grilling interview, confirms, and writes docs/specs/TODO/<TICKET-ID>.brief.md in the established section shape. First stage of the spec lifecycle: /spec-brief → /spec-cycle → /ship-spec → /spec-close.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: true
  subagents: true
  services: [issue-tracker?, shared-memory?]
---
```

`shell: true` covers read-only `git` probes (origin check, `git log`, `git status`) and `grep` during grounding. `network: true` is declared because the origin check's bounded, ref-only `git fetch origin` is an outbound request of the skill's own — the same reason `/spec-cycle` and `/spec-close` declare it. Ticket reads go through the declared optional services, not the skill's own network.

**Invocation:** `/spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`.

- `<TICKET-ID>` must match `^[A-Z][A-Z0-9]*-[0-9]+$` — the `/spec-cycle` Phase 0 step 1 regex (`skills/spec-cycle/SKILL.md:43–48`), anchored at both ends since here it is the whole argument.
- `--rounds N`: integer, `1 ≤ N ≤ 10`. `--questions N`: integer, `1 ≤ N ≤ 15`. Defaults 3 / 7 (D6). The ceilings exist so a flag cannot defeat the fatigue bound the ticket adds; there is no `0` alias — a zero-width round is a stall, not a bound.
- `--no-grill` wins over any cap flag; if both are given, warn `--rounds/--questions ignored under --no-grill` and continue — ignored for the interview; the default question cap (7) still bounds Phase 1's grounding batch.
- Anything else (bad ID, non-integer, out of range, unknown flag) → halt: `Usage: /spec-brief <TICKET-ID> [--no-grill] [--rounds 1-10] [--questions 1-15]`.

**Phase 0 — Preflight**

1. `project_root` = cwd. Read `<project_root>/CLAUDE.md` (or your harness's project-instructions file; in this repo that is `AGENTS.md`, which the gitignored `CLAUDE.md` points to) — the same step, with the same wiki-path and username-substitution fallback, as `/spec-cycle` Phase 0 step 3. Resolve `wiki_root` and `project_slug` if a wiki is configured.
2. **Output collision.** Check `docs/specs/TODO/<TICKET-ID>.brief.md`, `<TICKET-ID>.spec.md`, `<TICKET-ID>.reviews/`, and `.<TICKET-ID>.brief.md.tmp`. If only the stale temp exists, remove it, log `stale temp removed: .<TICKET-ID>.brief.md.tmp`, and continue without halting. If any artifact exists, halt:

   ```
   ARTIFACTS EXIST for <TICKET-ID>:
     brief:   <path | none>  (<tracked | untracked | modified> per git status)
     spec:    <path | none>
     reviews: <N> round(s) | none
     stale:   .<TICKET-ID>.brief.md.tmp from an interrupted run | none
   Writing a new brief changes the axiom every review round was measured against; prior closure tables become unverifiable.

   What would you like to do?
   1. Write the brief — an existing brief is read as grounding first; if only a spec and reviews exist, the brief is written fresh (the spec is never read as grounding, or the brief would inherit the artifact it exists to authorize); a stale .tmp is removed
   2. Abort
   ```

   Wait for the user's response. Never overwrite silently. The git-status column tells the operator whether the old brief is recoverable from history.
3. **Namespace.** Read `<config-dir>/skills/ship-spec/states.json`, where `<config-dir>` is `$CLAUDE_CONFIG_DIR` when set, otherwise `~/.claude/` on Unix and `%USERPROFILE%\.claude\` on Windows — the resolution `/spec-close` Phase 0 step 4 uses (`skills/spec-close/SKILL.md:31`). Same fallbacks and warnings as `/spec-cycle` Phase 0 step 7: missing or unparseable file, or unknown prefix → `namespace = "plane"` with a warning.
4. **Origin sync check (warn-only).** Same shape and tokens as `/spec-close` Phase 0 step 6 (`skills/spec-close/SKILL.md:37–42`): detect `origin`, bounded ref-only fetch, resolve `<branch>`/`<cmp>`, `git rev-list --count HEAD..origin/<cmp>`; behind-N → print `ORIGIN SYNC: local <branch> is <N> commits behind origin/<cmp> — grounding reads the local tree; the brief's "verified against current files" claim may be stale. Consider 'git merge --ff-only origin/<cmp>' first.` and continue. Never updates the tree. Any git failure → `origin: skipped (git error)`.
5. **Ticket resolution, in order, each optional:**
   a. Shared-memory tag-only search (`tags: ["plane_work_item", "<TICKET-ID>"]`, `namespace` from step 3, `source_system: "plane"`, `max_results: 1`) — e.g., `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` in Claude Code, or the equivalent in your host.
   b. On zero results or error: the issue tracker's retrieve-by-identifier capability (e.g., `mcp__plane__retrieve_work_item_by_identifier` in Claude Code, or the equivalent in your host).
   c. On failure of both: **conversation-only mode.** Print `ticket: unresolved (local-only) — describe the problem in a paragraph and I will proceed from that.` and wait. Apply the S9 seed gate to the answer (re-prompt once, then halt). The brief header will read `**Plane:** unresolved (local-only)`; `/spec-cycle` Phase 0 step 2's local-only path then applies downstream.
   Log one token: `ticket: memory | tracker | local-only`.
6. Print a one-line preflight summary: `ticket: <token> · namespace: <ns> · wiki: <resolved|none> · origin: <token> · grill: on (rounds=N, questions=M) | off (--no-grill)`.

**Phase 1 — Grounding (read-only)**

Retrieval-first, in this order, stopping when the seed is sufficient:

1. The ticket text (or the operator's paragraph). Apply the S9 seed gate here too when the ticket text itself is empty or a bare title.
2. If `wiki_root` resolved: `<wiki_root>/projects/<project_slug>/state.md` (header + the sections the ticket touches) and `filemap.md` if present. This is the mandatory read before any fan-out.
3. Files the ticket names, by path.
4. Only for gaps the above leave: dispatch read-restricted exploration per the D2 sentence (verbatim), in one parallel batch of at most `question_cap` dispatches (the default 7 under `--no-grill`), each with a one-line question and the instruction to answer with `path:line` evidence and make no mutations. A failed dispatch (error, empty, no fact) becomes a fact request in the interview's first round; under `--no-grill` it becomes a `## Risks / decisions` item instead — `<fact needed> — not established (exploration failed); spec author pins this`.

Assemble `seed`: problem statement, facts with sources, related open tickets if the ticket text names any. Print `grounding: <n> files read, <m> explorations dispatched (<f> failed)`.

**Phase 2 — Interview**

Skipped entirely when `--no-grill` (D9). Otherwise run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host) with `seed` from Phase 1, brief altitude (the default fence, stated verbatim), and `round_cap` / `question_cap` from the flags. The primitive waits for the operator each round; `/spec-brief` does nothing until the Grill summary comes back. On `empty-seed`, halt per S9 — nothing is written. **If this host cannot invoke a nested skill**, halt: `grilling is unavailable in this host — re-run with --no-grill to write the brief from the ticket alone, or run the interview by hand.` Never write a silently ungrilled brief.

**Phase 3 — Confirm (S2)**

Render a preview: the numbered `## Decisions carried forward` list (from Settled) and the `## Risks / decisions` list (from Open, each ending "spec author pins this"), then:

```
Write the brief?
1. Write docs/specs/TODO/<TICKET-ID>.brief.md
2. Revise an answer (name the Q number) — that decision and everything settled downstream of it return to the frontier; if the cap was hit, one extra round is granted, once
3. Abort — nothing written
```

Wait for the user's response. Option 2 re-invokes `grilling` with the Grill summary as `prior_summary` and the same `round_cap` / `question_cap` (S7 — the primitive itself grants the single post-cap round, Design 1.1); after a post-cap resume returns it is no longer offered and the block re-renders with options 1 and 3. Under `--no-grill`, option 2 reads `2. Add a decision (state it) — appended to Decisions carried forward`, and the preview's Decisions list is derived **only** from decisions the ticket text states explicitly, each carrying its quote or `path:line`; anything the model would have to infer goes to `## Risks / decisions` ending "spec author pins this". The altitude fence applies to that derivation exactly as it applies to the interview.

**Phase 4 — Write**

Write `docs/specs/TODO/<TICKET-ID>.brief.md` with exactly the established sections, in this order and with these headers (the `/spec-cycle` Phase 3 parser keys on three of them):

```
# <TICKET-ID> — <title>
**Status:** … · **Priority:** … · **Assignee:** …
**Created:** <YYYY-MM-DD> · **Plane:** <TICKET-ID> (<uuid>, <state>) | unresolved (local-only)
**Origin:** <one paragraph: where this came from>

## Problem
## Why it matters
## Scope (verified against current files, <date>)
## Decisions carried forward
## Done when
## Out of scope
## Scale            (conditional — see the emission rule below)
## Risks / decisions
## References
```

Write the full content to a dot-prefixed temporary sibling (`.<TICKET-ID>.brief.md.tmp` — the dot keeps it outside `/spec-close`'s `<TICKET-ID>.<rest>` companion glob, `skills/spec-close/SKILL.md:340`; the shape matches the repo's shipped atomic writers, `skills/spec-close/scripts/prepend_log_entry.py:370–375`, though unlike the wiki this repo's `.gitignore` does not ignore `.*.tmp`, so the no-commit rule below is prose, not mechanism) and rename it over the target in one step, so an interrupted write never leaves a truncated brief; remove the temp file on any failure. A stray dot-file from a killed run must not be committed; Phase 0 step 2 removes it on the next run whether or not any other artifact exists. Create `docs/specs/TODO/` first if it does not exist (as `/spec-cycle` does for its review subdirs, `skills/spec-cycle/SKILL.md:573`). The directory creation, this rename, and Phase 0 step 2's removal of a stale `.<TICKET-ID>.brief.md.tmp` are the skill's only filesystem mutations outside the brief itself. Two `/spec-brief` runs on the same ticket in one worktree are outside the supported flow: the collision check is not a lock, the brief is last-writer-wins, and the stale-temp removal cannot distinguish an abandoned temp from a concurrent run's in-flight one (Risk 15).

Mapping rules: `## Problem`, `## Why it matters`, and `## Done when` are transcribed from the ticket text (or, in local-only mode, the operator's paragraph), never inferred; in local-only mode the header fields read `**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`; a Settled decision the operator framed as a fence (an answer of the form "X is not in scope") is written to `## Out of scope` rather than `## Decisions carried forward`; the remaining Settled → `## Decisions carried forward`, numbered, each carrying the chosen branch and its one-line why — if Settled is empty, write `_(none settled — see Risks / decisions)_` under the header rather than leaving it blank, and print `warning: interview settled no decisions — the brief pins everything to the spec author`; Open → `## Risks / decisions`, numbered, each ending "spec author pins this"; Scope → one row per path the settled decisions and grounding facts name, `Current` filled from a fact with its `path:line`, `Change` from the settled decision that touches it — a path with no read file or fact behind it gets no row and goes to `## Risks / decisions`; the Scope heading date is the date grounding ran, and when preflight logged `origin: behind-N` the heading reads `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)` with a matching `## References` bullet; Facts → `## References` (with `path:line`); the exit token and round count go in a final References bullet — `Interview: <n> rounds, exit <token>`, or `Interview: skipped (--no-grill)`.

**`## Scale` emission** (four input cases, three emitted shapes — matching `AGENTS.md:95` and `/spec-cycle` Phase 0 step 8):
- A settled decision says scale **is** a factor **and** carries a target → emit `## Scale` with `**Factor:** yes` and `**Target:** <N>` (and `**Dimensions:**` if given). The factor and its target are one question, not two (S4's example asks both in a single item), so a settled "yes" normally arrives with its N.
- Settled "is a factor" but no target was obtained (cap hit, deferred) → emit **no** `## Scale` section, add `Scale target — the operator settled scale as a factor but no target N was obtained; spec author pins this` to `## Risks / decisions`, and print `warning: scale factor settled without a target — section not emitted`. Never emit `**Factor:** yes` without a target: `/spec-cycle` would silently drop it as malformed.
- Settled "is **not** a factor" → emit `## Scale` with `**Factor:** no`, so `/spec-cycle` records the non-factor Decision.
- Never asked → no section.
- Under `--no-grill`, apply the same cases to a scale declaration the ticket text states explicitly (factor + target → emit; factor without target → no section, Risks item, warning; explicit non-factor → `**Factor:** no`); if the ticket says nothing about scale, emit no section.

Then print:

```
=== BRIEF WRITTEN: <TICKET-ID> ===
Path: docs/specs/TODO/<TICKET-ID>.brief.md
Interview: <n> rounds, exit <token>; <s> settled, <o> open   |   skipped (--no-grill)
Ticket: <memory | tracker | local-only>

=== NEXT ===
/spec-cycle docs/specs/TODO/<TICKET-ID>.brief.md
```

**What `/spec-brief` never does:** create or transition a ticket; write anything other than the one brief file (and its transient `.tmp`, and the `docs/specs/TODO/` directory when absent); delete anything other than a stale `.<TICKET-ID>.brief.md.tmp` of its own shape; commit; fast-forward or otherwise mutate the tree; invoke `/spec-cycle`.

#### Tool-use notes

(In the skill file this is a real `## Tool-use notes` heading — contract §4 case 3, matching `spec-cycle:570`; it is `####` here only so it nests under Design 3.) Read/Grep/Bash (`git remote`, `git fetch origin` bounded by `timeout`, `git symbolic-ref`, `git rev-parse`, `git rev-list`, `git status`, `git log` — all read-only or ref-only, plus `mkdir` for `docs/specs/TODO/` when absent, the rename of the brief's dot-prefixed temp onto its target, and the removal of a stale temp — the skill's only filesystem mutations outside the brief) for preflight and grounding; Agent for read-restricted exploration; Skill for `grilling`; Write for the single brief file; the shared-memory search and issue-tracker read capabilities.

#### Failure modes

(A real `## Failure modes` heading in the skill file.)

- Ticket unresolvable (both services down) → local-only, not an error; the S9 seed gate still applies.
- Empty seed (ticket text is a bare title, or the local-only paragraph states no problem) → re-prompt once, then halt; nothing written.
- Wiki path missing → skip grounding step 2 silently.
- Artifacts exist → halt with the Phase 0 step 2 block; never overwrite silently.
- Origin behind → warn only; never update.
- Host cannot invoke a nested skill → halt naming `--no-grill` as the alternative; never write ungrilled without the flag.
- Exploration dispatch fails → fact request in round 1 (or a Risks item under `--no-grill`); a dispatch that never returns blocks its batch — see § Risks 12.
- Operator abandons mid-interview → nothing is written; re-run to start over. No resume state is kept, by design (no runtime state).
- `--no-grill` with cap flags → warn, ignore the caps, continue.

### 4. `skills/spec-cycle/SKILL.md` — 2f fourth option

**Edit 1 — the halt block (`:466–485`).** The fenced block's `Remaining P0/P1` list gains a fourth line, the menu gains a fourth option, and the closing sentence changes:

```
SPEC NOT GREEN AFTER 4 ROUNDS.
Remaining P0/P1:
  - <round 4 correctness P0/P1 titles>
  - <round 4 edge-cases P0/P1 titles>
  - <round 4 conventions P0/P1 titles>
  - <round 4 scalability P0/P1 titles — only when scale_lens == on for this invocation>

Spec at: docs/specs/TODO/<TICKET-ID>.spec.md
Reviews at: docs/specs/TODO/<TICKET-ID>.reviews/

What would you like to do?
1. Patch manually and re-run /spec-cycle
2. Skip /ship-spec and ship by hand
3. Treat as scoped-down — narrow the brief
4. Grill the remaining findings — a bounded interview scoped to the titles above; decisions route through 2e revise (see 2f-i)
```

The scalability line closes a residual three-lens hardcode VHS-15 left in this block (its closure machinery was generalized to "every report present per round", but the halt print was not). `Wait for the user.` becomes: `Wait for the user. Options 1–3 end the skill as today. Option 4 runs 2f-i once, then re-renders this menu without option 4.`

**Edit 2 — new subsection `### 2f-i. Option 4 — grill the remaining findings`,** inserted between the halt block and `### 2g`:

1. **Seed.** Read the round-4 reports on disk (`correctness.md`, `edge-cases.md`, `conventions.md`, plus `scalability.md` only when `scale_lens == on` for this invocation — a `scalability.md` present in `round-4/` under `scale_lens == off` is stale from a prior on-run and is ignored, matching the closure-read guard at `skills/spec-cycle/SKILL.md:604–620`) and extract each remaining P0/P1 finding: id, severity, title, body. Nothing else enters the seed — the grill is finding-scoped (D8), not a re-interview of the design. **Not grillable:** a report that is missing or unparseable, any synthetic `missing STATUS line` P0 (2b's closure-manifest form), and any 2c dispatch-failure stub (a lens report whose body records a dispatch failure rather than findings — `skills/spec-cycle/SKILL.md:404–409`) — these are dispatch failures, not design questions. Exclude them from the seed and list them in step 5 as `not grillable: <lens>/<id> — reviewer report unavailable; option 1 re-dispatches that lens.` They stay P0/P1. **If the seed is empty after these exclusions, do not invoke `grilling`:** print `nothing grillable — every remaining finding is a dispatch failure; option 1 re-dispatches the affected lens(es)`, write nothing to `grill.md`, and re-render the menu with options 1–3 (there is nothing for option 4 to do).
2. **Run.** Invoke the `grilling` skill (Claude Code: through the skill-invocation tool, or the equivalent in your host) with that seed, `altitude` = "a decision that dispositions one of the listed findings", default bounds (`round_cap` 3, `question_cap` 7). The interview blocks on the operator per round. If this host cannot invoke a nested skill, print `grilling is unavailable in this host` and re-render the menu with options 1–3.
3. **Persist.** Append the returned Grill summary verbatim to `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`, preceded by `---` if the file already exists and by the header line `# Grill <k> — <TICKET-ID> round 4 — <ISO datetime> — findings: <ids>` (`<k>` = lines matching `^# Grill ` + 1). Write it read-modify-tmp-rename via a uniquely named dot-prefixed temp in the same directory (`.grill.md.<random>.tmp` — unlike Phase 4's, nothing detects this one by name, so it need not be fixed). Concurrent invocations sharing the reviews tree are outside the supported flow (S8, Risk 14). Never overwrite an existing `grill.md` (S8). This is the caller's write, not the primitive's. `/spec-close` archives the whole `<TICKET-ID>.reviews/` tree (`skills/spec-close/SKILL.md:339`), so the file travels to `DONE/` unchanged and the reconciliation report can see why the spec moved after the halt.
4. **Apply.** For each **Settled** item, edit the spec in place under the 2e rounds-1–3 rules (address the finding per the decision; the spec must stand on its own at the end). The round-4 FROZEN/REWRITE protocol is not re-run — it already ran before the halt. A Settled decision that cannot be discharged by an in-place spec edit (e.g., "narrow the brief" — that is menu option 3's job) is **not applied**: report it in step 5 as `deferred to option 3: <finding id>`, leave the finding P0/P1, and record it in `grill.md` as Settled-but-unapplied. 2f-i never edits the brief. **Open** and **not grillable** items are not touched; they remain P0/P1.
5. **Re-render.** Print `grill applied: dispositioned <ids>; left open <ids>; not grillable <ids>; deferred to option 3 <ids> — docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`, then the 2f halt block again with options 1–3 only (S8), each dispositioned title suffixed ` — grilled (spec edited; not re-reviewed)` so the operator can see what moved without opening `grill.md`. The round counter is still 4; no reviewer is re-dispatched; `total_p0p1` is unchanged because no reviewer has re-verified — the honest path to green is option 1.

Invariants, stated in the subsection verbatim: *"2f-i never re-dispatches reviewers, never increments the round counter, never changes the gate formula, never overwrites a prior `grill.md`, never edits the brief, and runs at most once per invocation."*

**Edit 3 — Tool-use notes (`:570`):** add `- Skill invocation of \`grilling\` — only from 2f-i, only after the operator picks option 4.` **Failure modes (`:578`):** add `- **2f-i grill hits its cap, the operator stops, or the host cannot invoke a nested skill.** Open and not-grillable findings stay P0/P1; \`grill.md\` records them as Open (append-only); the menu re-renders with 1–3. The grill cannot make the spec green on its own.`

No other line of the file changes. VHS-27's post-round-4 delta reviews would sit in the same region; whichever ships second rebases (brief Risk 6). If VHS-27 lands first, 2f-i composes by leaving the re-dispatch decision to the menu — the grill still ends at "re-render".

### 5. Documentation edits

**`AGENTS.md` (`:23–29`).** "Three skills form the spec lifecycle." → "Four skills form the spec lifecycle. The interview stage is separate so the brief — the artifact every reviewer treats as authority — is settled before review context is spent; the authoring/impl pair runs in separate sessions to avoid token-cap pressure; the post-merge close runs after code ships:". New item 1:

> 1. **`/spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`** — Produces the brief. Resolves the ticket (tracker optional — degrades to conversation), grounds against repo + wiki, runs the bounded `grilling` interview (round cap 3, seven items per round, brief-altitude fence), confirms, and writes `docs/specs/TODO/<TICKET-ID>.brief.md`. Reads tickets; never creates or transitions them. `grilling` is the shared model-invocable primitive (also behind `/grill-me` and `/spec-cycle`'s post-round-4 option 4); it is never fired unprompted.

Existing items renumber 2–4; the `/spec-cycle` item gains "…halts at a session boundary with a drift-check checklist, or — if still red after 4 rounds — a menu whose fourth option grills the remaining findings."

`AGENTS.md` § Superseded vendor skills gains one short paragraph (not a bullet — the section's only list is the counted "Two warnings:" about the AgentCraft removal, and it stays byte-identical), appended after the closing "If AgentCraft reinstalls its copy…" paragraph: *"**`grilling` / `grill-me` (VHS-32) — superseded by overwrite, not removal.** These share directory names with `mattpocock/skills`; `sync.py install` overwrites a separately-installed upstream copy at those paths. Intended — the clean-room rewrite supersedes it, and because the install overwrites in place there is no operator removal step and no two-copies routing ambiguity. To keep both, rename the upstream copy before installing."*

**`docs/spec-workflow-reference.md`.** Line 3 opening: "Two AI-driven skills that split spec authoring from implementation…" → "Four AI-driven skills: an interview stage that produces the brief, two that split spec authoring from implementation into separate sessions, and a post-merge close…". New section before `## Skill 1: spec-cycle`:

> ## Skill 0: spec-brief
> **Purpose:** produce the brief. Why upstream: every reviewer lens treats the brief as authority, so a fork left open in it is invisible to review and surfaces as a P0/P1 against the spec. Invocation and flags; phases 0–4 in one paragraph each (mirroring § 3 above); the termination shapes (empty frontier / cap hit / stop / empty seed) and where each lands in the brief.
> ### The grilling contract
> Design tree, frontier, one round per frontier, the fork form, advisory recommendation, read-restricted fact-finding, the bounds with defaults (including the shared cap on fact requests), the hand-off block. One sentence on the 2f reuse.

New section before `## Adapting to your stack` (`:162`):

> ## Skill 3: spec-close
> One paragraph: after the PR merges, reconcile the spec against shipped code, propose wiki entries, archive `TODO/` → `DONE/<TICKET-ID>/`, prepend the wiki log entry; Plane state gates full vs partial close; `--report-only` / `--partial`. Points to `skills/spec-close/SKILL.md` for the phases. *(Documents a skill that already ships; see Scope note.)*

**`README.md`.** The tagline at `:3` becomes "A Plane.so-aware brief → spec → review → ship → close workflow with a bounded design interview and parallel reviewers, plus a CodeRabbit triage handler." § Skills becomes, in lifecycle order: `/spec-brief <TICKET-ID>` (one-line summary), `/spec-cycle` (existing), `/ship-spec` (existing), `/spec-close <spec-path>` (new one-liner mirroring `AGENTS.md` item 4), then `/grill-me <topic>` (new) and `/review-pr` (existing); and a final line: "`grilling` is the model-invocable interview primitive behind `/grill-me`, `/spec-brief`, and `/spec-cycle`'s post-round-4 option 4 — not a slash command." § Requirements: the existing `/spec-cycle` and `/ship-spec` bullet gains `/spec-close` (Plane state plus, for the wiki half, a wiki checkout); and a new line: "For `/spec-brief` and `/grill-me`: no external services required — `/spec-brief` reads the ticket through Plane / shared memory when present and degrades to conversation when not. Both need a harness that can dispatch a read-restricted subagent."

### 6. Portability and lint posture (cross-cutting)

- All three new files: exactly one `requires:` block, flat, controlled vocabulary only, placed after the scalar keys (contract §3 uniqueness/position). Expected lint outcome: zero ERROR, and `missing-requires` WARN count unchanged from today (the two pre-existing WARNs are `review-pr` and `ship-spec`, untouched).
- Every harness-specific name (`Explore`, `Agent`, `Skill`, `mcp__*`) appears only as a case-2 tagged parenthetical ("…or the equivalent in your host") inside operative prose, or under a `## Tool-use notes` **heading** (case 3 — a heading, not a bold label, because `lint.py:57,216–217` keys the exemption on `cur_heading`). The lint's v1 scope only flags `mcp__*`; the review checklist grep covers the rest.
- No `model:` frontmatter anywhere (it is agent-file frontmatter, and no agent file is added). The Opus intent lives in the D2 sentence only.
- **Nested skill invocation is not expressible in `requires:`** (contract §3 vocabulary: `shell`, `filesystem`, `network`, `subagents`, `services`). A harness therefore cannot pre-flight it. All three call sites carry the explicit point-of-use halt instead (Design 2, 3 Phase 2, 4 step 2). Recorded in § Risks as a contract-vocabulary gap.
- `sync.py` needs no change: three new `skills/<name>/SKILL.md` directories are inside the mirrored `skills/` subtree. **Name collision, intended:** `grilling/` and `grill-me/` share directory names with the `mattpocock/skills` upstream. `sync.py install` copies file-by-file (`sync.py:96`, the install copy; `:146` is the symmetric push copy), so a separately-installed upstream copy at those paths is overwritten — the clean-room rewrite supersedes it by design, and `README.md:30`'s preservation promise covers only paths this repo does not contain. An operator who wants both renames the upstream copy first. This is the second supersession of a third-party skill in this repo — the revisit trigger in `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md`. A tracked uninstall manifest is still not warranted: unlike `agentcraft-handoff`, the same-name install overwrites in place, so there is no operator removal step and no description-matching ambiguity between two coexisting copies; that decision's own consequence ("`sync.py` … installs and overwrites; it does not delete") is the property relied on. Ships as a paragraph in `AGENTS.md` § Superseded vendor skills (checklist 12).

## Test plan

Doc/prompt-only change → review checklist plus two dry-run transcripts (VHS-7 / VHS-11 convention).

**Review checklist (the gate for `/ship-spec`):**

1. `python lint.py --strict` → exit 0; zero ERROR; `missing-requires` WARN count is 2 (unchanged: `review-pr`, `ship-spec`).
2. `grep -nE '\b(Explore|Agent|Skill|general-purpose)\b' skills/grilling/SKILL.md skills/grill-me/SKILL.md skills/spec-brief/SKILL.md` → every hit is inside a parenthetical carrying "or the equivalent", or under a `## Tool-use notes` heading, or is the prohibition itself ("never a general-purpose agent").
3. `grep -c 'model:' skills/grilling/SKILL.md skills/grill-me/SKILL.md skills/spec-brief/SKILL.md` → 0 each.
4. `grilling` body contains, verbatim: the 1.0 guard sentence; the D2 sentence (including "make no mutations of any kind"); the fork block; the "advisory, never a default that carries by silence" sentence; the bounds with defaults 3 / 7 / brief altitude and the shared fact-request cap; the S4 table; the hand-off block with `### Settled` / `### Open frontier` / `### Facts established`; the `empty-seed` exit; the 1.1 resume contract including the single post-cap round and the `revised-after-cap (+1 round)` exit. `## Tool-use notes` and `## Failure modes` are real `##` headings.
5. `grep -n 'user_invocable' skills/grilling/SKILL.md` → `false`; `grill-me` and `spec-brief` → `true`. `grilling`'s description contains none of "grill me", "stress-test", "poke holes".
6. `skills/spec-cycle/SKILL.md`: diff touches only the 2f fenced block and its closing sentence, a new `### 2f-i` subsection, one Tool-use-notes bullet, one Failure-modes bullet. `grep -c 'total_p0p1 == 0'` unchanged; 2e and 2g byte-identical (`git diff -U0` shows no hunks in `:426–465` or `:487–518` of the pre-edit file).
7. `2f-i` text contains "never re-dispatches reviewers", "never increments the round counter", "never overwrites", "at most once per invocation", "never edits the brief", "not grillable", "nothing grillable", "deferred to option 3", and the path `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`. The halt block contains the scalability line.
8. `AGENTS.md`, `docs/spec-workflow-reference.md`, `README.md` each mention `/spec-brief` **and** `/spec-close`, and describe four stages in the order brief → cycle → ship → close. `grep -c 'spec-close' README.md docs/spec-workflow-reference.md` → ≥ 1 each (both are 0 today).
9. `spec-brief` body: `## Tool-use notes` and `## Failure modes` are real headings; the Invocation section states the `1–10` / `1–15` ranges and no `0` alias; Phase 0 step 2 checks brief, spec, reviews, and the stale `.tmp`, removing the latter without halting when it is alone; Phase 4 states the tmp-then-rename write and the four-case `## Scale` rule.
10. `python sync.py status` clean after `python sync.py install`; `python sync.py push` is a no-op (byte-for-byte round trip). After install, confirm `/grilling` is not offered as a slash command in Claude Code; if it is, that is a documented limitation (D9), not a blocker — the guard sentence governs.
11. No file under `agents/`, `skills/ship-spec/`, `skills/spec-close/` changed.
12. `AGENTS.md` § Superseded vendor skills carries the `grilling` / `grill-me` name-collision paragraph (`grep -c 'mattpocock' AGENTS.md` ≥ 1), and the section's "Two warnings:" list still has exactly two bullets.
13. `spec-brief` body: the `--no-grill` path states its own `## Scale` derivation, its failed-dispatch → Risks rule, and its option-2 wording; the Phase 3 option-2 path states re-invocation with `prior_summary`, the single post-cap round granted by the primitive, and the fallback to options 1 and 3.
14. After the dry runs, `git status --porcelain docs/specs/TODO/` shows no `ZZZ-*` path and no `.*.tmp`.

**Dry-run transcripts** — captured into `docs/specs/TODO/VHS-32.test-output.txt` (the conventional ship-spec companion path; `/spec-close` archives it as `test-output.txt` per `skills/spec-close/SKILL.md:340`; the VHS-29 close flagged an unstated test-output artifact as drift, so it is stated here). **Procedure:** the new skills are not installed inside the ship-spec worktree (a merged skill is inert until `python sync.py install`), so each run is an *authoring dry-run*: the implementer reads `skills/spec-brief/SKILL.md` and `skills/grilling/SKILL.md` from the worktree and follows them literally, acting as the operator for every round. Each run uses a fresh id — Run A `ZZZ-1`, Run B `ZZZ-2`, Run C `ZZZ-3`; Run D continues Run B's `ZZZ-2` session at its confirm block before option 1 is taken, and Run B's write assertion is checked after D returns — because a shared id would trip the artifacts-exist halt and ground one run on another's brief. All runs are in conversation-only mode; the emitted briefs are deleted before commit and only the transcript is kept. Because `/ship-spec`'s `N/A` branch omits the test-output link from the PR body (`skills/ship-spec/SKILL.md:197, :241`), the implementer links `VHS-32.test-output.txt` from the PR body by hand.

- **Run A — empty frontier.** Seed: a two-paragraph problem statement with a shallow tree; `--rounds 3`; the operator answers every question; exit `empty-frontier` in ≤3 rounds; the confirm block appears; option 1 writes a brief whose `## Risks / decisions` carries no "spec author pins this" items and whose References bullet reads `Interview: <n> rounds, exit empty-frontier`.
- **Run B — round cap.** Seed: an obviously deep tree; `--rounds 1 --questions 3`; the single round renders **at most** 3 items (the cap is the checkable observable; the exact count depends on the model's decomposition); exit `round-cap`; the confirm preview shows ≥1 Open item; the written brief carries those items in `## Risks / decisions` each ending "spec author pins this".
- **Run C — empty seed** (checklist row, not a transcript): local-only mode, operator answers `ok`; the skill re-prompts once, then halts with the S9 message; `docs/specs/TODO/ZZZ-3.brief.md` does not exist afterward.
- **Run D — revise after cap** (checklist row, not a transcript): after Run B's `round-cap` exit, choose option 2 on a settled Q; the resume renders exactly one further round whose round-end line reads `Round 2 of 1 (post-cap revision round — the last).`, exits `revised-after-cap (+1 round)`, and the confirm re-renders with options 1 and 3.

## Test command

N/A

## Done when

Mapped 1:1 to the brief's `## Done when`:

1. `skills/grilling/SKILL.md` exists, `user_invocable: false`, carrying the design-tree/frontier model, the one-round-per-frontier rule, the D4 fork contract, the D1–D2 dispatch rule, and the three D6 bounds. *(Design 1; checklist 4–5.)*
2. `skills/grill-me/SKILL.md` exists, `user_invocable: true`, delegating to `grilling`. *(Design 2; checklist 5.)*
3. `skills/spec-brief/SKILL.md` exists; `/spec-brief <TICKET-ID>` writes `docs/specs/TODO/<TICKET-ID>.brief.md` with the eight established sections, Settled → Decisions carried forward, Open → Risks / decisions. *(Design 3 Phase 4; transcripts A/B.)*
4. `/spec-brief` degrades to conversation-only when the issue-tracker service is absent; `requires.services` marks both services optional. *(Design 3 Phase 0 step 5c.)*
5. `skills/spec-cycle/SKILL.md` 2f offers option 4; the surrounding text states the grill cannot re-dispatch reviewers, cannot increment the round counter, and routes through 2e. *(Design 4; checklist 6–7.)*
6. 2f-i persists its outcome to `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md` (append-only). *(Design 4 step 3; checklist 7.)*
7. All three new files carry a valid `requires:` block; `python lint.py --strict` reports zero ERROR and no new `missing-requires` WARN. *(Design 6; checklist 1.)*
8. No bare harness tool name as an operative imperative in any new file; the `Explore` / Opus binding appears only inside the D2 parenthetical. *(Design 6; checklist 2–3.)*
9. `AGENTS.md`, `docs/spec-workflow-reference.md`, `README.md` describe the four-stage lifecycle (which, for the latter two, requires the `/spec-close` documentation they never received — Scope note). *(Design 5; checklist 8.)*
10. `python sync.py status` clean; `python sync.py push` round-trips byte-for-byte; `Test command: N/A`; Test plan is a review checklist plus the two dry-run transcripts. *(§ Test plan; checklist 10.)*

## Out of scope

Carried verbatim from the brief:

- Porting any other upstream skill (`domain-modeling`, `grill-with-docs`, `to-spec`, `to-tickets`, `wayfinder`, `triage`); `to-spec`'s user-story template is not adopted.
- Auto-invoking grilling from `/spec-cycle` Phase 1 authoring, `/ship-spec`, or `/spec-close`.
- Making the interview mandatory, or gating `/spec-cycle` on a brief having been grilled.
- Any change to the green gate, severity scale, round cap, FROZEN/REWRITE protocol, 2g polish, or the four reviewer agents.
- Creating or transitioning Plane tickets from `/spec-brief`; ticket creation stays in `/spec-cycle` Phase 0 step 2.
- A fifth reviewer lens that reviews the brief.
- Anything in VHS-26 or VHS-27; the 2f-i text and VHS-27's delta reviews are sequenced, not merged.

Spec-author additions to the fence (each a consequence of a Decision above, not new scope):

- Resume state for an abandoned interview — none is kept (no runtime state; Design 3 § Failure modes).
- Extending `lint.py` to flag bare `Explore` / `Agent` / `Skill` names — the review checklist grep covers this change; a lint extension is its own ticket.
- Extending the portability contract's `requires:` vocabulary (an optional marker for booleans; a token for nested skill invocation) — recorded as gaps in § Risks, not fixed here.
- An offered fast-forward in `/spec-brief`'s origin check — warn-only, like `/spec-close`; the skill never mutates the tree.

## Risks

1. **Interview fatigue** (brief Risk 1) — mitigated by S1 hard truncation over questions *and* fact requests, S7 defer/re-ask, and the bounded flags (`1–10` / `1–15`); the defaults are a first guess, exposed so they can be tuned without a spec change.
2. **Altitude fence is prose** (brief Risk 2) — S4 examples make it legible; same trust model as VHS-11 Risk 2.
3. **Fork form over-applied** (brief Risk 3) — S3's two-part test plus the three-branch cap.
4. **Grill-then-write drift** (brief Risk 4) — S2 confirm-first, including under `--no-grill`, with the `--no-grill` derivation rule pinned.
5. **No read-restricted agent class on some hosts** (brief Risk 5) — S5: ask, never dispatch write-capable; fact requests share the cap.
6. **VHS-27 adjacency** (brief Risk 6) — Design 4 closing paragraph; whichever ships second rebases.
7. **Inert until installed** (brief Risk 7) — `/ship-spec`'s summary already tells the operator to run `python sync.py install`; never `--prune`.
8. **The lint does not enforce D2 for non-`mcp__` names.** Accepted; checklist 2 is the manual gate, and the lint's own docstring records this as a v1 limitation.
9. **`requires:` cannot express two things this design relies on** — an *optional* `subagents` (S5's degradation exists but a subagent-less host fails pre-flight anyway) and *nested skill invocation* (no token, so no pre-flight; every call site halts at point of use instead). Both are contract §3 vocabulary gaps, recorded here for a follow-up ticket; neither is fixed by this spec.
10. **`Explore` retains shell access in Claude Code.** D1's "read-only" is read-restricted-plus-instructed, not read-only by construction; the D2 sentence carries the no-mutation instruction, and the exploration prompts in Phase 1 repeat it. Accepted as the best available binding.
11. **`user_invocable: false` is unprecedented and advisory.** First use in this repo; informational on Hermes. D9's guarantee rests on the 1.0 guard sentence and the description, verified by checklist 5 and 10.
12. **A hung exploration blocks its round.** No prompt-level construct can cancel a pending dispatch, and no resume state exists beyond `prior_summary`. Accepted; the mitigations are the per-round dispatch cap and the D2 prompt's own bound ("answer from the named paths; return `not found` rather than searching exhaustively"). `/spec-cycle` carries the same exposure for its reviewers.
13. **Upstream name collision.** `grilling` / `grill-me` overwrite a same-named third-party install on `sync.py install`. Intended and documented in `AGENTS.md`; the alternative (`vh-grilling`) was rejected because the slash-command name is the product.
14. **`grill.md` has no cross-session or cross-invocation coordination.** The once-per-invocation bound is context-held (`/spec-cycle` writes no preflight timestamp, and Phase 0 is out of scope); concurrent appends from two sessions are last-writer-wins and undetectable. Accepted; the `<k>` counter exposes duplicates after the fact, and two sessions grilling one ticket's round 4 is outside the supported flow.
15. **Two `/spec-brief` runs on one ticket in one worktree.** The collision check is not a lock; the brief is last-writer-wins; the stale-temp removal can delete a concurrent run's in-flight temp. Accepted; outside the supported flow.

## References

- Brief: `docs/specs/TODO/VHS-32.brief.md` (read 2026-09-06).
- `skills/spec-cycle/SKILL.md` (620 lines, read 2026-09-06): Phase 0 step 1 regex `:43–48`, step 3 (project-instructions read + wiki resolution) `:61`, step 5 origin check `:133–233`, step 7 `states.json` `:235`, step 8 scale `:237`, 2b closure-manifest synthetic P0 form `:371–375`, 2c scalability stub `:404–410`, gate `:415`, 2e `:426–465`, **2f `:466–485`**, 2g `:487–518`, Phase 3 `:520`, Tool-use notes `:570`, Failure modes `:578`, malformed-scale failure mode `:598–600`, stale-`scalability.md` closure guard `:604–620`.
- `skills/spec-close/SKILL.md:31` (`<config-dir>` resolution), `:37–42` (warn-only origin check), `:312, :339–340` (archives `<TICKET-ID>.reviews/` wholesale and any `<TICKET-ID>.<rest>` companion).
- `skills/ship-spec/SKILL.md:20` (`N/A` test-command handling), `:197, :241` (test-output link omitted under `N/A`).
- `docs/portability-contract.md` §2 (`:26–43`; `user_invocable` row `:34`), §3 (`:47–103`; optional marker `:65`, MUST-verify `:78`), §4 (`:107–119`), §5 dimension 3 `:129`.
- `docs/specs/DONE/VHS-20/spec.md:153` — the Hermes adapter drops `user_invocable`.
- `lint.py:24–33` — documented v1 limitations; `:45–48` controlled vocabulary; `:57, :216–217` heading-keyed case-3 exemption.
- `agents/spec-reviewer-conventions.md:3` (`model: opus`), `:17–31` (wiki reads), and the authorized-by-brief classification — the "brief as unchallenged authority" problem statement.
- `docs/specs/DONE/VHS-11/brief.md` — the target brief shape; `## Risks / decisions` items ending "spec author pins this".
- `docs/customizing.md:3` — downstream projects configure skills via their `CLAUDE.md`.
- `skills/bloat-check/SKILL.md:19` — precedent for an in-body attribution line.
- `skills/spec-close/scripts/prepend_log_entry.py:370–375` and `skills/session-handoff/scripts/create_handoff.py:340–341` — the repo's dot-prefixed atomic-write precedent.
- `sync.py:96` — the `copy2` in `cmd_install` (same-named third-party skills are overwritten; `:146` is the symmetric push copy); `README.md:30` — the preservation promise's actual scope.
- Commit `5e6d401` — reviewers pinned to Opus (2026-09-02).
- `AGENTS.md:23–29` (lifecycle), `:88–96` (Conventions; `## Scale` grammar at `:95`); `README.md:7–11, :54–59`; `docs/spec-workflow-reference.md:3, :7, :162`.
- Wiki: `vigil-harbor-wiki/projects/vigil-skills/state.md` — VHS-29 install-inertia note, VHS-28 `--prune` warning and clean-room posture; `decisions/2026-06-16-vhs-15-optional-scalability-lens.md` — closure machinery generalized to every report present; `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md` — revisit trigger on a second supersession, dispositioned in Design 6.
- Origin (idea attribution only, MIT): `mattpocock/skills` `skills/productivity/grilling/SKILL.md`, `skills/productivity/grill-me/SKILL.md`, re-read 2026-09-06.

## Deferred (P2+)

Round-1 through round-4 P2+ findings folded in a different shape than proposed, or deliberately not folded, with one-line acknowledgments:

- edge-cases R4 F-1's distinct `fence-empty` exit token and a 2f-i re-offer of option 4 on a zero-rendered grill — not folded (new behavior, beyond post-green polish limits). The 1.8 header's reason line now distinguishes "tree fully visited" from "no candidate decision met the altitude fence", which is the observable the finding asked for; the token and re-offer are a follow-up candidate.

- edge-cases R2 F-8 / R3 F-4's durable once-signal — not folded: `/spec-cycle` records no timestamp to compare against, so the bound stays context-held and is recorded as Risk 14 (a same-day header check was also rejected: an option-1 re-run the same day is legitimate).
- edge-cases R3 F-3's `.gitignore` addition — not adopted (out of scope; the prose no-commit rule plus Phase 0 removal stands, and the spec now says the rule is prose).
- conventions R2 F-3's rename alternative (`vh-grilling`) — not adopted; overwrite is intended (Risk 13).

- conventions F-5 (origin-sync) — **folded** (Design 3 Phase 0 step 4). Listed here only because it was the largest P2 addition; the fast-forward *offer* is explicitly out of scope.
- edge-cases F-13's proposed numeric cap on `## Risks / decisions` — folded as the by-construction bound in Design 1.8 rather than a separate cap.
- correctness F-9's secondary note (test-output link omitted under `N/A`) — folded as a manual PR-body step in § Test plan; changing `/ship-spec` is out of scope.

## Post-green polish

Folded after the round-4 green gate (2g), clarifications only — no behavior reversals, no Decisions / Out-of-scope / Done-when edits:

- conventions R4 F-1 — Scope table `AGENTS.md` row now says "short paragraph (not a bullet)", matching Design 5.
- conventions R4 F-2 — Phase 4, the never-list, and Tool-use notes now name all three filesystem mutations (directory creation, temp rename, stale-temp removal); checklist 9 covers the stale-`.tmp` trigger.
- conventions R4 F-3 / correctness R4 F-1 — dry-run ids are distinct (`ZZZ-1` / `ZZZ-2` / `ZZZ-3`); Run D is pinned as a continuation of Run B's confirm; checklist 14 asserts no `ZZZ-*` or `.*.tmp` leaks.
- conventions R4 F-4 — README `/grill-me` marked "(new)".
- edge-cases R4 F-1 — 1.7 and the 1.8 header carry a reason line distinguishing a fully visited tree from a fence-emptied frontier (the new token is deferred).
- edge-cases R4 F-2 — 2f-i halt block and step 1 read `scalability.md` only when `scale_lens == on` for this invocation; References cite the `:604–620` guard.
- edge-cases R4 F-3 — Phase 4 creates `docs/specs/TODO/` when absent (as `/spec-cycle` does at `:573`); Tool-use notes list `mkdir`.
- edge-cases R4 F-4 — the post-cap resume round renders `Round <round_cap>+1 of <round_cap> (post-cap revision round — the last).`; Run D asserts it.
- edge-cases R4 F-5 — 2f-i step 5 prints finding ids per category and suffixes dispositioned titles in the re-rendered halt block.
- edge-cases R4 F-6 — Phase 4 and Risk 15 record concurrent `/spec-brief` runs as outside the supported flow.
- edge-cases R4 F-8 — the `# Grill <k>` counter operand is anchored (`^# Grill `).
- correctness R4 F-2 — 1.7 spells the exit as `revised-after-cap (+1 round)` and says the suffix is part of the token.
- correctness R4 F-3 — the round-end line tells the operator how to answer `F` items.
- correctness R4 F-4 — `lint.py` vocabulary anchor is `:45–48`.
