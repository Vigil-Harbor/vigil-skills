---
name: grilling
description: Bounded design interview primitive. Models a problem as a design tree, asks the whole settled frontier each round with weighed forks and an advisory recommendation, dispatches read-restricted exploration for facts, and stops at a round cap, a per-round question cap, or an altitude fence. Not a user-facing entry point — invoked only by /grill-me, /spec-brief, and /spec-cycle's post-round-4 halt (option 4). Users who want to be grilled run /grill-me.
user_invocable: false
requires:
  subagents: true
  filesystem: [read]
---

# grilling — the bounded design interview

This skill is invoked only by `/grill-me`, `/spec-brief`, or `/spec-cycle` 2f-i. If you reached it any other way, stop and ask the user whether they meant `/grill-me`.

## Invocation contract (inputs)

The caller supplies these, in prose or as a labelled list:

- **`seed`** — the problem statement and any grounding facts already established. `/grill-me` supplies the user's topic; `/spec-brief` supplies the ticket's problem statement plus its grounding; 2f-i supplies the remaining P0/P1 findings with their bodies. Each seed item may carry an optional **`id`** — a caller-stable string the primitive echoes back as `ref:` on every Settled and Open item that descends from it. 2f-i passes finding ids; `/spec-brief` and `/grill-me` pass none, and then no `ref:` field is rendered at all.
- **`altitude`** — the fence, stated as *which artifact lines a decision must change to be askable*. The default (brief altitude) is: "a decision that changes the brief's Scope, Decisions carried forward, or Out of scope." 2f-i supplies: "a decision that dispositions one of the listed findings."
- **`round_cap`** (default 3) and **`question_cap`** (default 7).
- **`prior_summary`** *(optional)* — a Grill summary this skill returned earlier in the same session, plus the Q number to revise. This is the only resume path, and it exists for the revise case alone. The caller decides whether to offer a resume at all.

**Resume contract.** Rebuild the tree from the summary. Settled items stay settled except the named one and everything downstream of it, which re-enter the frontier. Prior Open items stay Open and are not re-asked unless they are downstream of the revised decision. Facts established carry over and are not re-dispatched. Q and F numbering continues the prior series. `rounds_used` carries over from the summary's `rounds:` field. **If `rounds_used ≥ round_cap`, this invocation runs exactly one additional round and exits `revised-after-cap (+1 round)`; a further `prior_summary` arriving with `rounds_used > round_cap` exits `round-cap` at once.**

## The design tree and the frontier

The design-tree / frontier framing is adapted from the `grilling` skill in `mattpocock/skills` (MIT); the text here is original.

Every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are settled. Each round asks the whole frontier, capped. After the operator answers, settled decisions push the frontier outward: recompute it and ask again. A question that depends on a question still open this round belongs to a later round — never drip-feed one question at a time, and never ask a question whose premise is still unsettled.

If the seed yields no root decision at all — nothing a design decision could hang off — exit `empty-seed` at once, without rendering a round.

## Per-round output contract

A question that genuinely branches is rendered as a fork:

```
❓ **Q1 — <title>**: <body>

  **A.** <branch> — *For:* <…>  *Against:* <…>
  **B.** <branch> — *For:* <…>  *Against:* <…>

➡️ **Recommend B** — <one line of why>
```

A question that does not branch uses the plain form — `❓ **Q2 — <title>**: <body>` followed by `➡️ <recommended answer>`. Fact requests use `ℹ️ **F1 — <fact needed>**: …`.

Numbers are monotonic across the whole interview: `Q1…Qn` never resets between rounds, so a carried or re-asked item keeps its number. Fact requests use the parallel `F1…Fn` series.

Each round ends with these literal lines:

```
Answer by item number: a question by number and branch letter (e.g. `Q3 B`), a fact request by number and the fact (e.g. `F1 <answer>`); a plain answer is recorded as given. "defer" moves a question to the open frontier.
"stop" ends the interview. Unanswered questions are re-asked once, then deferred; a partly answered round still uses one of your <round_cap> rounds. Round <n> of <round_cap>.
```

and then **wait**. On the single post-cap resume round the last sentence reads `Round <round_cap>+1 of <round_cap> (post-cap revision round — the last).` instead, and the hand-off header renders `rounds: <round_cap>+1/<round_cap>`.

**Plain language.** Every rendered round glosses each internal identifier on its first use in that round — a section code such as `2f-i`, an exit token such as `empty-frontier`, a file or block name — with a few words in parentheses saying what it is. Write in the ASD-STE100 style: short sentences, one instruction per sentence, one meaning per term. Keep question bodies short; the fork's `For:` / `Against:` lines carry the detail. The STE controlled dictionary is not applied. This rule governs rendered rounds; the hand-off block is rendered exactly as its contract states.

## Decisions are the operator's

The recommendation is advisory. It is never a default that carries by silence: a round is not settled until the operator answers, and this skill must not proceed on an unanswered question by adopting its own recommendation.

- **`defer`** (or an equivalent explicit skip) moves the question to the Open frontier at once. Its descendants are *not* enumerated or asked; the subtree is recorded as **one** rolled-up Open item: `<parent title> — downstream decisions not explored (deferred at round <n>)`. Only questions actually rendered to the operator ever become named Open items.
- **Omitted** (no answer given): re-ask at the top of the next round with its original number and a `(re-asked)` tag, counting against that round's cap; omitted again → treat as `defer`. A partially answered round still consumes one round of budget — that is the price of the no-silent-default rule.
- **Free-form** (neither a rendered branch letter, `defer`, nor `stop`): record it verbatim as the settled decision if it satisfies the altitude fence; otherwise re-ask once with a `(clarify)` tag. A free-form answer never adds a fourth branch to the rendered fork — it *replaces* the fork with the operator's answer.
- **Revise** arrives as a `prior_summary` plus a Q number: apply the resume contract above, including the single post-cap round.

## Fact-finding

Dispatch a read-restricted exploration agent on the strongest available model (Claude Code: the `Explore` subagent type with an Opus model override, or the equivalent narrowest read-only agent class in your host) — never a general-purpose agent, which inherits the full session tool set. Instruct it to answer with `path:line` evidence only and to make no mutations of any kind: most host agent classes keep shell access even when file-edit tools are withheld. Bound its work in the prompt: answer from the paths named in the question, and return `not found` rather than searching exhaustively.

**Detection first.** At the first fact need, determine whether this host offers an agent class that withholds the file-edit tools. If none exists, do **not** dispatch a write-capable agent: render every fact need as a fact request instead — `ℹ️ **F1 — <fact needed>**: … *(no read-restricted agent available in this host)*`.

Otherwise dispatch every fact need of a round in **one parallel batch, capped at `question_cap` dispatches**, before rendering the round. Questions downstream of a fact wait for it; the rest of the frontier is asked in the current round. Fact needs beyond the dispatch cap carry to the next round's batch by the ordering rule in § Bounds; if the interview ends first they reach the hand-off as Open with `unresolved because: fact not established`.

A dispatch that errors, returns empty, or returns without the fact is a **failed dispatch**: carry its question to the next round as an `ℹ️` fact request and render the round without it. Where the host reports a timeout, treat it identically. Where it does not, a dispatch that never returns blocks the round it belongs to — no prompt-level construct can cancel a pending dispatch; the dispatch cap bounds how many can hang, and the prompt bound above bounds each one's work.

Facts, with their source paths, are carried into the hand-off. Retrieval-first: if the caller supplied wiki or state context in `seed`, consult it before dispatching. No resume state is kept beyond `prior_summary`: if the session ends mid-interview, the caller re-runs.

## Bounds

Three bounds, and nothing else, end the interview:

1. **Round cap** — default 3, supplied per invocation.
2. **Per-round question cap** — default 7, supplied per invocation. At most `question_cap` rendered items per round, **questions and fact requests together**; overflow carries to the next round. This is a hard truncation, not a soft target. **Ordering** when truncating: carried-over and re-asked items first, then shallowest tree depth (a decision with more unsettled descendants unblocks more), then your judgment of blast radius on the artifact the altitude fence names.
3. **Altitude fence** — the `altitude` the caller supplied; brief altitude by default. A candidate decision that would not change a line of the named artifact is not asked at all.

A fact request the operator leaves unanswered twice becomes an Open item (`fact not established`) rather than recycling forever. A resume grants exactly one post-cap round, once, as the resume contract states.

**The test for "genuinely branches."** Render a question in fork form when **two or three** candidate answers each (a) are consistent with every decision already settled in this interview and (b) would produce a *different* line in the artifact the altitude fence names. If only one candidate satisfies both, use the plain form. More than three viable branches means the question is under-decomposed: split it into a prerequisite question (asked now) and its dependents (next round).

**Worked examples of the fence** (brief altitude):

| In altitude (ask) | Out of altitude (do not ask — leave to the spec) |
|---|---|
| "Should the origin-sync check offer a fast-forward, or only warn?" — changes a Decision and the Out-of-scope fence on mutation. | "Should the fast-forward use `git merge --ff-only` or `git pull --ff-only`?" — same Decision either way; the spec pins the command. |
| "Is scale a factor for this ticket — do we dispatch the scalability lens, and at what target N?" — adds or removes a Scope row. | "What regex detects the `## Scale` heading?" — implementation of an already-settled Scope row. |
| "Does `/spec-brief` write Plane state, or only read the ticket?" — Out-of-scope fence. | "Which `states.json` key does `/spec-brief` read the namespace from?" — the spec author reads the file. |

Implementation detail is the spec's job. Asking it here duplicates `/spec-cycle`.

## Termination

The exits are `empty-frontier`, `fence-empty`, `round-cap`, `stop`, `revised-after-cap (+1 round)` (the suffix is part of the rendered token), and `empty-seed`.

`empty-frontier` is reachable only after at least one round was rendered; its reason line distinguishes `tree fully visited` from `no candidate decision met the altitude fence` (a later round's remaining candidates all fell below the fence). If the tree has a root but no round-1 candidate satisfies the altitude fence, nothing is rendered and the exit is `fence-empty`, with that same fence reason and `rounds: 1/<round_cap>` — the round was attempted and consumed. Both go through the hand-off block; on `fence-empty` its Settled and Open frontier sections are empty, and `### Facts established` is rendered as on any exit — empty unless the seed supplied facts or a dispatch returned one.

On `stop`, every question answered in the stopping round is Settled (a `defer` is not a settling answer — the question is Open with `unresolved because: deferred`, per § Decisions are the operator's), pending explorations are abandoned (fact needs not yet dispatched or not yet resolved when `stop` lands — none is an active dispatch, since a batch blocks the round it belongs to), and their fact needs are Open `F<n>` items with `unresolved because: stopped`, and any question that was waiting on one is Open with `unresolved because: blocked-on: F<n>`.

Every exit but `empty-seed` goes through the hand-off contract below; `empty-seed` returns the token and a one-line reason, and nothing else.

Reaching a cap is a documented outcome, not a failure; the caller decides what to do with the open frontier.

## Hand-off contract (output)

End by rendering exactly this block in-conversation, then return. Write no file — the caller owns every write.

```
## Grill summary — <seed title> (rounds: <n>/<round_cap>, exit: empty-frontier | fence-empty | round-cap | stop | revised-after-cap (+1 round); reason: tree fully visited | no candidate decision met the altitude fence | cap reached | operator stop | resume)

### Settled
1. **<decision title>** (Q<n>) — chose <A/B/free-form answer>: <one line>. Facts relied on: <F-ids or "none">. ref: <id>[, <id>…] | none

### Open frontier
1. **<question title>** (Q<n>) — branches: <A/B>; recommendation: <X>; unresolved because: <round-cap | deferred | stopped | blocked-on: Q<m> | blocked-on: F<n>>. ref: <…>
2. **F<n> — <fact needed>** — unresolved because: <fact not established | stopped>. ref: <…>
3. **<parent title> — downstream decisions not explored (deferred at round <n>)**. ref: <…>

### Facts established
- F1 — <fact> (source: <path:line>)
```

`ref:` renders on every Settled and Open item when any seed item carried an `id`, and on none otherwise. An item's ids are those of the seed items it descends from: a question descends from the seed items it was raised to disposition, a decision from its question, a fact request from the question whose need raised it (or from the seed items directly when the need arose from the seed), the rolled-up deferred item from the deferred question. Ids are listed in seed order; an item descending from no identified seed item (a fact-driven decision, or a question raised about an unidentified seed item) renders `ref: none`. That value exists only in a run where some seed item carried an `id`; a run whose seed carried no ids omits the field on every item and never writes `ref: none`.

The Open frontier is bounded by construction at `(round_cap + 1) × question_cap` named items plus one rolled-up item per deferred subtree.

Callers map the block: `/spec-brief` turns Settled into `## Decisions carried forward`, Open Q-items and F-items into `## Risks / decisions` items ending "spec author pins this", and feeds Facts into Scope and References; 2f-i drives its 2e edits from Settled, matching each decision to its findings by `ref:`, and leaves Open in the red list.

## What this skill never does

Writes a file; edits a spec or brief; dispatches a write-capable agent; invokes `/spec-cycle`, `/ship-spec`, or `/spec-close`; answers a decision on the operator's behalf.

## Tool-use notes

- The read-restricted exploration agent (Claude Code: `Explore`, dispatched with an Opus model override) — the only dispatch this skill makes.
- Read and Grep, for consulting paths the caller supplied in `seed`.
- Nothing else: no writes, no shell, no network of its own.

## Failure modes

- **Failed dispatch** (error, empty, or no fact returned) — the question becomes an `ℹ️` fact request in the next round; see § Fact-finding.
- **No read-restricted agent class in this host** — every fact need is rendered as a fact request, tagged as such; never dispatch a write-capable agent instead.
- **`empty-seed`** — the seed has no root decision; exit at once with the token and a one-line reason, rendering no round and no hand-off block.
- **`stop` with explorations pending** — abandon them (fact needs not yet dispatched or not yet resolved when `stop` lands; no dispatch is active, since a batch blocks its round); their fact needs are Open `F<n>` items with `unresolved because: stopped`, and any question that was waiting on one is Open with `unresolved because: blocked-on: F<n>`.
