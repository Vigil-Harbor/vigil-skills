---
name: spec-brief
description: Produce the brief that /spec-cycle consumes. Resolves a ticket (issue tracker optional — degrades to conversation), grounds against the repo and wiki, runs the bounded grilling interview, confirms, and writes docs/specs/TODO/<TICKET-ID>.brief.md in the established section shape. First stage of the spec lifecycle: /spec-brief → /spec-cycle → /ship-spec → /spec-close.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: true
  subagents: true
  services: [issue-tracker?]
---

# /spec-brief — produce the brief

Invoked as:

```
/spec-brief <TICKET-ID>                                  # ticket + grilled interview, the default
/spec-brief <TICKET-ID> --no-grill                       # skip the interview; still confirms before writing
/spec-brief <TICKET-ID> --rounds N --questions N         # tune the interview's bounds
```

The brief is the one artifact downstream review treats as authority: every `/spec-cycle` lens reads it as settled. A fork left open here surfaces later as a P0/P1 against the spec, so settle forks here, in a bounded interview, and write what it produced.

## Invocation

- `<TICKET-ID>` matches `^[A-Z][A-Z0-9]*-[0-9]+$`.
- `--rounds 1-10` (default 3), `--questions 1-15` (default 7).
- `--no-grill` skips only the interview. With cap flags, warn `--rounds/--questions ignored under --no-grill` and continue; the default question cap still bounds Phase 1's exploration batch.
- Anything else prints `Usage: /spec-brief <TICKET-ID> [--no-grill] [--rounds 1-10] [--questions 1-15]` and stops.

## Operator replies

Read each reply for intent. Numbered lines are the fast path; a person may answer in their own words. Before acting, print `Reading: <what you will do>.` Ask again only on real ambiguity, and name it; keep every clear part of the reply. Silence or an empty reply is never yes. `abort` as the only non-blank line stops and writes nothing. An override needs a reason that is non-empty after trim. A host that cannot wait prints the prompt's stop line and writes nothing. These rules cover every prompt here except the interview, which `grilling` runs under its own rules.

## Phase 0 — Preflight

1. `project_root` = cwd. Read its project-instructions file (`CLAUDE.md`, or `AGENTS.md` where that holds the instructions). Resolve `wiki_root` and `project_slug` if a wiki is configured; if a hardcoded wiki path with a username does not exist, retry with the current user's name.
2. **Output collision.** If only a stale `docs/specs/TODO/.<TICKET-ID>.brief.md.tmp` exists, remove it, log `stale temp removed`, and continue. If the brief, the spec, or `docs/specs/TODO/<TICKET-ID>.reviews/` exists, list what exists and offer `1. Write the brief` or `2. Abort. The files stay.`, then wait. On 1, an existing brief is read as grounding; a spec is never read as grounding. Never overwrite silently.
3. **Origin sync (warn only).** Run a bounded `git fetch origin`. If the current branch is behind its origin branch, print `ORIGIN SYNC: local <branch> is <N> commits behind origin/<cmp> — the brief's "verified against current files" claim may be stale.` and log `origin: behind-N`. Any git error, no remote, or detached HEAD logs `origin: skipped`. Never update the tree.
4. **Ticket resolution.** Uppercase the identifier first; a lower-case ref is not found. Read it with the issue tracker's retrieve-by-identifier capability (e.g., `mcp__claude_ai_Plane__workitem` with `action: retrieve_by_identifier`, `workitem_identifier: "<TICKET-ID>"`, `fields: "id,name,state,description_stripped,priority,assignees,created_at"` and `expand: "state"` in Claude Code, or the equivalent in your host; load the tool first if your host defers tool schemas). `id` is the header `<uuid>`, `state.name` the `<state>`, `created_at` the `**Created:**` date, `name` the title, `description_stripped` the ticket text and `priority` `**Priority:**`. `assignees` holds member ids: print the id, and `unassigned` only for an empty list. A field you did not request comes back null, or `[]` for an array, and that never means the ticket lacks it. On a failed read, print `ticket: could not read <TICKET-ID> from the issue tracker (<error>) — continuing without it. Usually a login problem: re-authenticate the tracker connection.` (`<error>` is `no tracker connected` when no tracker tool is connected), then `ticket: unresolved (local-only) — describe the problem in a paragraph and I will proceed from that.`, and wait. On not-found, print `ticket: <TICKET-ID> not found in the issue tracker — continuing without it.`, then that same unresolved line, and wait. The brief header stays `**Plane:** unresolved (local-only)`. No retry and no cache; warn once per run.
5. Print `ticket: <tracker | local-only> · wiki: <resolved|none> · origin: <token> · grill: on (rounds=N, questions=M) | off (--no-grill)`.

## Phase 1 — Grounding (read-only)

Retrieval-first, stopping when the seed is sufficient:

1. The ticket text, or the local-only paragraph.
2. If `wiki_root` resolved: `<wiki_root>/projects/<project_slug>/state.md` (header plus touched sections) and `filemap.md`.
3. The files the ticket names.

A gap that asks what execution does is not grounding, even when a file states the result. Put it in the seed labelled `needs a run`; grilling's per-fact rule (`skills/grilling/SKILL.md` § Fact-finding) decides how it is answered. Under `--no-grill` it becomes the Risks item `<fact needed> — not established (needs a run); spec author pins this`.

4. Only for code-text gaps left after 1-3: dispatch the narrowest read-only exploration agent (Claude Code: `Explore`, or the equivalent in your host), never a general-purpose agent. Ask for `path:line` evidence only, no mutations of any kind, and `not found` rather than an exhaustive search. One parallel batch of at most `question_cap`. A failed dispatch becomes a fact request in round 1, or under `--no-grill` the Risks item `<fact needed> — not established (exploration failed); spec author pins this`.

Assemble `seed`: the problem statement, established facts with sources, related open tickets the ticket names, and each `needs a run` gap. Print `grounding: <n> files read, <m> explorations dispatched (<f> failed)`.

## Seed gate

Runs in every mode. If the ticket (or paragraph) states no problem — under two sentences, or nothing a decision could hang off — ask once (`Ticket <ID> states no problem — describe it in a paragraph and I will proceed from that.`), then halt with nothing written. Grilling's `empty-seed` exit halts the same way. Hold the ticket text, plus any paragraph collected here labelled `Seed-gate paragraph:`, as `ticket_contract` for Phase 3.

## Tier gate

Runs after the seed gate, in every mode. Nothing writes a tier the operator did not choose. Print one prompt:

```text
Tier. Pick one. This sets how much review the brief gets.

Recommended: <tweak|big>. basis: <files, lines, surfaces>

1. tweak. This writes nothing.
2. small. A small change.
3. big. The normal review.
4. irreversible. Hard to undo. The doubt pass must run.

These claims would make the ticket pointless if false:
  P1. <claim> (<level>)
Agree, or name a claim that is missing.
```

With no candidate claims, the second half reads `No claim would make this ticket pointless if false. Agree, or name one.` (§ Premises defines a claim and its level.) A missing claim the operator names is added at the level you can support. A listed claim the operator says would not defeat the ticket is dropped. A reply that answers only one half is asked again for the other half only. A host that cannot wait prints `tier needs an operator — stopping` and writes nothing.

**Tweak hint.** Recommend `tweak` only when the ticket and grounding name at most 2 files, under about 50 lines, touching no auth, payments, data migrations, or config/CI; otherwise recommend `big`. The `basis:` line names the files, lines and surfaces. The recommendation is advisory; the operator always picks.

`tweak` records no premises and writes nothing. If Phase 0 step 2 found artifacts and the operator chose to write, print their paths and say they stay actionable until removed; spec-brief deletes nothing. Otherwise print:

```text
=== NO BRIEF WRITTEN: <TICKET-ID> ===
Tier: tweak
basis: <files, lines, surfaces>

=== NEXT ===
No lifecycle — ship as a chore PR citing the ticket; the ticket's state and closing comment are yours to set.
```

For `small`, `big` or `irreversible`, resolve the reviewer (below), then run the interview, or Phase 3 under `--no-grill`.

### Doubt-pass reviewer

Find a fresh-context reviewer from a different model family: a native agent, an installed skill, or a command-line tool. It is eligible only when its own instructions, configuration or runtime output state a family different from yours (never infer one from a tool's name), it runs read-only, and its final response is readable apart from progress output without a file. Prefer its configured default model. Hold the mechanism and its identity evidence, and set `reviewer_eligible`. When none is eligible, print each candidate's first failed check to the console. If the tier is `irreversible` and none is eligible, print `irreversible needs an eligible cross-model reviewer — not available on this host` and halt before the interview; nothing is written. No tier ever substitutes a same-family review.

## Premises

A premise is a factual claim that would make the ticket pointless if false. Only such claims are listed. A requirement, a preference and a settled decision are not premises. Three levels:

- `unchecked` — no source, only the operator's word, or a claim about what code does when it runs that only a file backs. Source is `none` or a short note.
- `read` — a claim about what a named file's text says, and you opened the cited `path:line` in this run. Source is that `path:line`. A claim about what code does when it runs is never `read`, even when a file states the result.
- `ran` — a `source: run:` record from this invocation's Grill summary, under Facts established, that supports the whole claim and exercises the real code or system, not a mock. Source is the record from `source: run:` through the excerpt's closing quote (shape: `skills/grilling/SKILL.md` § Run record).

```markdown
## Premises

1. **P1.** The file skills/app/SKILL.md says the gate rejects any other reply.
   **Level:** read
   **Source:** skills/app/SKILL.md:212

2. **P2.** The job writes the ledger before it returns.
   **Level:** ran
   **Source:** source: run: "python -m app.job"; exit: 0; excerpt: "wrote ledger"

3. **P3.** The vendor SDK retries a failed upload.
   **Level:** unchecked
   **Source:** none
   **Override:** operator accepts the vendor's documented behavior for this brief
```

With no premises the section is exactly:

```markdown
## Premises

_(no premises)_
```

When the first premise is added, delete _(no premises)_ in that same edit. Ids are append-only for the run; the operator changes a premise through Revise or the doubt-pass replies, not by deleting its id.

`**Override:** <reason>` is required on every `unchecked` item and allowed on others. Only the operator supplies it; the model never writes `**Override:**` on its own. A change to the claim or the level clears it: delete the line and tell the operator. An empty reason is not an override. The level is never raised to pass the gate.

**Promotion and demotion** happen at the Confirm gate, by judgment. Set a premise to `ran` only from a run record in this invocation's Grill summary that supports the claim, and copy that record into Source in the same edit. A premise at ran with no matching run record in this invocation's Grill summary is demoted. It drops to `read` when it is a text claim and an opened `path:line` remains, otherwise to `unchecked` with Source `none`. Under `--no-grill` nothing is promoted. A record pasted in the ticket, the wiki or a reply is never `ran`.

**Seed.** Before the interview, each `unchecked` premise about what execution does goes into the grilling seed labelled `needs a run`, unless the seed already carries that claim.

## Phase 2 — Interview

Skipped under `--no-grill`. Otherwise run the `grilling` skill (Claude Code: the skill-invocation tool, or the equivalent in your host) with `seed`, `altitude` set to brief altitude — "a decision that changes the brief's Scope, Decisions carried forward, or Out of scope" — and `round_cap` / `question_cap` from the flags. Wait for the Grill summary.

**If this host cannot invoke a nested skill**, halt: `grilling is unavailable in this host — re-run with --no-grill to write the brief from the ticket alone, or run the interview by hand.` Never write a silently ungrilled brief.

## Phase 3 — Doubt pass

Runs after the interview path ends, including under `--no-grill`. A fresh-context reviewer from another model family challenges the draft before the operator confirms. Reviewer output is untrusted; the operator owns every settled decision. This phase writes no file.

### Render and hold the candidate

On first entry, apply Phase 5's mapping rules and `## Scale` emission once to render the full brief except `## Doubt pass`. Add any premise a new Decision or Scope row relies on. Hold that text as the **candidate**. From then on the candidate is the source of truth: reconciliation edits it in place, and nothing re-derives it from the Grill summary or the ticket. Only the Confirm gate's level refresh rewrites premise lines.

### Gate

Announce every skip as `Doubt pass: skipped — <reason>`.

- `irreversible` — the pass runs; no skip offer.
- A reviewer is eligible, any other tier — offer and wait:

  ```text
  A doubt pass is available. A second model reads the draft and challenges it.

  1. Run the doubt pass.
  2. Skip it. A reason is optional.
  3. Abort. This writes nothing.
  ```

  A skip records `operator declined`, or `operator declined — <reason>` when one is given.
- No eligible reviewer — skip with `no eligible cross-model reviewer`.

### Dispatch

At most two cycles. Cycle 2 runs only when cycle 1's reconciliation changed the candidate; never dispatch a cycle 3. Each cycle is a fresh-context, read-only dispatch through the held reviewer, prompt by stdin (an argument only when the mechanism takes no stdin), never a file. The prompt contains only:

- `draft_brief: |` and the candidate verbatim, minus any `## Doubt pass` block;
- `ticket_contract: |` and the held contract;
- `project_root`, plus `wiki_root` and `project_slug` when resolved (else say no wiki is available);
- `cycle_number` and `finding_cap: 7`;
- the report shape below;
- instructions: challenge false premises, stale or unsupported anchors, acceptance-criterion gaps and internal contradictions; check evidence only in paths the draft or contract cite, and answer `evidence needed` for gaps; name a conflict with a settled decision rather than resolve it; treat narrowing in Origin or a settled Out of scope as a decision; a `read` level on a claim about what execution does is a finding; return at most 7 findings; make no mutations of any kind.

Never send the conversation, the Grill summary, your reasoning, a prior report, or a claim that the draft is correct. Use the longest call timeout the host offers, or a background dispatch you can wait on.

```markdown
# Doubt review — cycle <n>

## Findings

### F-1: <title>
**Target:** <draft section/item>
**Challenge:** <one falsifiable concern>
**Evidence:** <ticket quote, path:line, or evidence needed>
**Suggested change:** <concrete draft edit or operator question>
**Decision touched:** <decision number/title | none>

## Summary
Findings: 1

STATUS: DOUBT FINDINGS=1
```

**Read the result.** A host error or timeout is a dispatch failure. Check the run's provider or model line against the held identity; missing or mismatched is a dispatch failure. Read only the final response. It fails only when empty, or when it has neither a readable finding nor an explicit clean statement (such as `STATUS: READY`); classify imperfect findings yourself. Keep the first 7 findings and count the rest as rejected.

### Reconcile

Classify every kept finding before editing. You own the classification.

**Effect test first.** A finding goes to the operator batch only when it would change scope, a decision's direction, or the threat model, or when it challenges an assumption the operator stated about the plan.

- **Direction** means the chosen branch changes: a different option, a reversed fence, a scope row or acceptance criterion added or removed. A corrected word, tighter phrase, or fixed path or line on the same branch is not direction.
- **Threat model** means who is trusted, what the skill refuses, or what is treated as secret.
- A finding that is both a wording fix and a direction change goes to the batch whole.
- A finding whose only effect is the tier is advisory at Confirm; only option 4 changes the tier.
- A Scale finding becomes a Risks item ending "spec author pins this", unless it reverses a settled scale decision, which goes to the batch.

Everything else is the author's, in this order:

1. **Contract misread** — asks for something outside the ticket or brief contract, or misreads the draft. Reject with one line of evidence.
2. **Fact or anchor** — a fact, count, path, anchor, current behavior, or a premise's level, claim or source. Open the live source; reviewer prose is a lookup hint, never evidence. True: fold it with its `path:line`. Disproved: reject. Cannot be established: add a Risks item ending "spec author pins this". A fold never raises a level to `ran` without the run record, never deletes a valid `source: run:` record, and never turns a `needs a run` Risks item into a `path:line` fact.
3. **Trade-off** — a purely technical trade-off is the author's call, recorded in the summary.
4. **Noise or duplicate** — reject with a one-line reason.

Folds may edit wording, precision and anchors in any section, including Decision text, but never a chosen branch, an Out of scope fence, or a Done-when meaning. Work in order: classify all, verify facts, compose findings that target the same text into one result, edit, run the batch, then re-read every changed section and its consumers. Record one summary line per author disposition.

**Operator batch.** Only when at least one finding escalated. Show at most 7 per cycle as `F-<n>`, each with the settled text, the challenge, and what you checked. Print:

```text
These findings would change the plan: scope, a decision's direction, the threat model, or an assumption you stated.
For each, say keep, replace, or reopen. Fast path: `F-1: keep`, `F-1: replace: <text>`, `F-1: reopen`.
`abort` as the only line stops and writes nothing.
```

Keep: the text stands. Replace: apply the new text and update every consumer; it must not change the tier. Reopen: remove the decision and add a Risks item ending "spec author pins this". Ask again only for findings no reply addressed. Hold each resolution with its Q number when its decision came from a Grill Q.

### Outcome

`Result` is `completed at cap` when cycle 2 changed the candidate or failed after cycle 1 changed it, else `completed`. `Cycles` counts reconciled cycles. Count findings per distinct root, last disposition wins: **folded**, **operator resolved** (a reopen also adds one open), **rejected** (including cut at 7), **open** (Risks items the pass left).

### Dispatch failure

Print `Doubt pass dispatch failed: cycle <n>; class <reason>; last line: <line | none>`. Offer only what applies: `1. Retry once` (once per cycle), `2. Skip` (not `irreversible`; before any reconciled cycle it records `reviewer dispatch failed — <short reason>`, after cycle 1 it keeps cycle 1 as `completed at cap`), `3. Abort — nothing written`, `4. Accept cycle 1` (`irreversible` only, after cycle 2's retry, when cycle 1 changed the candidate). Never substitute a same-family review.

## Phase 4 — Confirm

The Confirm gate runs on every entry to Confirm, including after any candidate change:

1. Refresh each premise's level by the promotion and demotion rule, clearing an override whose claim or level changed.
2. Add any premise a current Decision or Scope row newly relies on.
3. Show the candidate.
4. For each `unchecked` premise without a non-empty override, ask for a reason or `abort`:

   ```text
   These claims would defeat the ticket, and nothing has checked them. Give each a reason, or abort.
   Fast path: `P1: <reason>`.
   ```

   A host that cannot wait prints `premise override needs an operator — stopping` and writes nothing.
5. Write the replies onto `**Override:**` lines.
6. Offer the menu. No temp exists while the menu waits.

Show `Tier: <level>`, the basis line, any tier finding as advisory evidence, and:

```text
Doubt pass: <completed in N cycle(s) | completed at cap (N cycle(s)) | skipped — <reason>>
```

Then the author-choice summary, when the author made a choice:

```text
Author choices. No reply is needed to agree with a line you do not name.

F-1. <what it was>. Adopted. <why>. Decision text edited.
F-2. <what it was>. Rejected. <why>.
```

`Decision text edited` ends a line whose fold edited a Decision's text. When the Grill summary carries a line whose trimmed text is exactly `Redaction: fired` (`skills/grilling/SKILL.md:176`), print once per run, here: `A value here looks like a credential and was redacted. Treat it as exposed and rotate it with /key-rotation. If this was ordinary text, ignore this line.` Do not invoke key-rotation or wait for a reply. At cap, print `Final reconciliation edits were not re-reviewed`; when cycle 2 failed, `Cycle 2 failed; only cycle 1 completed`. Then:

```text
Write the brief?

1. Write the brief to docs/specs/TODO/<TICKET-ID>.brief.md.
2. Revise one answer. Name the question number. That decision, and what hangs on it, is asked again.
3. Abort. This writes nothing.
4. Change the tier. The tier prompt is shown again.
```

An empty reply does not write.

**Summary replies.** Naming an author-choice line is not option 2 and spends no round; not naming one agrees with it. Keep leaves it. Reverse restores the pre-fold text, or applies the reviewer's concrete edit after checking any fact it states against the live source; if neither text exists, ask again. A reverse uses only text the reviewer saw, so it does not void the pass, but a reverse that changes a premise or Decision re-runs the Confirm gate. Reopen adds a Risks item ending "spec author pins this", removes the Decision only when it is the finding's target, and voids the pass. A reply that says write and also reverses applies every reverse first, then writes; write plus reopen does not write.

**Option 4** re-shows the tier half of the prompt. A non-tweak choice updates `## Tier` and returns to the menu; `tweak` takes the tweak exit. `irreversible` with no eligible reviewer prints the irreversible message and keeps the previous tier. A completed doubt result stands under the new tier; a skipped one runs Phase 3's gate again under it, and under `irreversible` that runs the pass.

**Option 2** re-invokes `grilling` with the Grill summary as `prior_summary` and the same caps; grilling owns the single post-cap round, and this skill offers option 2 at most once after a cap hit. Before resuming, carry batch resolutions: amend Q-linked Settled items in `prior_summary` (keep, replace, or reopen to Open as `(Q<n>) … unresolved because: deferred`); pass Q-less resolutions in `seed` as operator-settled constraints. After the resume, a returned decision that conflicts with a kept resolution goes through the operator batch before Phase 3 runs again. Map only the new or changed items by Phase 5's rules, renumber the lists you changed, and refresh the `Interview:` References bullet.

**Under `--no-grill`**, option 2 reads `2. Add a decision (state it) — appended to Decisions carried forward`. Decisions come only from decisions the ticket states explicitly, each with its quote or `path:line`; anything inferred goes to Risks ending "spec author pins this".

**Void rule.** A revision, an added decision, or a summary reopen voids the doubt result: drop the `## Doubt pass` block and re-enter Phase 3 at cycle 1 under the current tier. Reviewer output is never reused.

## Phase 5 — Write

Write `docs/specs/TODO/<TICKET-ID>.brief.md`: the exact candidate the operator confirmed, with one `## Doubt pass` block. Never re-apply the mapping rules here. The brief has exactly these sections, in this order (`/spec-cycle` parses several of them):

```
# <TICKET-ID> — <title>
**Status:** … · **Priority:** … · **Assignee:** …
**Created:** <YYYY-MM-DD> · **Plane:** <TICKET-ID> (<uuid>, <state>) | unresolved (local-only)
**Origin:** <one paragraph: where this came from>

## Problem
## Why it matters
## Scope (verified against current files, <date>)
## Decisions carried forward
## Premises
## Done when
## Out of scope
## Tier
## Scale            (conditional — see the emission rule below)
## Doubt pass
## Risks / decisions
## References
```

**`## Tier`**, immediately before the conditional `## Scale`, with the chosen level:

```markdown
## Tier

**Level:** small
```

**`## Doubt pass`**, after `## Scale` (or `## Tier`) and before `## Risks / decisions`. Completed:

```markdown
## Doubt pass

**Result:** completed | completed at cap
**Cycles:** 1 | 2
**Outcome:** folded <n> fact/anchor findings; operator resolved <n> decision findings; rejected <n>; open <n>
```

Skipped:

```markdown
## Doubt pass

**Result:** skipped
**Reason:** <reason>
```

The reason is `operator declined[ — <reason>]`, `no eligible cross-model reviewer`, or `reviewer dispatch failed — <short reason>`. The section names no vendor or model and quotes no reviewer prose.

**Write and the script result.** Create `docs/specs/TODO/` if absent, and write the full content to the dot-prefixed temp `docs/specs/TODO/.<TICKET-ID>.brief.md.tmp`. Write the temp from the candidate after override lines are on the items. Then run the script and act on the exit:

```bash
CONFIG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SCRIPT="$CONFIG/skills/spec-brief/scripts/check_premises.py"
TEMP="docs/specs/TODO/.<TICKET-ID>.brief.md.tmp"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
if test -f "$SCRIPT"; then
  "$PY" "$SCRIPT" "$TEMP"
else
  echo "not found at $SCRIPT — install with 'python sync.py install'" >&2
  exit 3
fi
```

- Exit 0 → rename the temp onto the brief.
- Exit 1 with at least one `premise:` line on stderr → print `premise gate: check_premises.py exited 1 — Write blocked` and the script's stderr, delete the temp, and return to the Confirm gate. You may repair only the format lines the printed codes name; `unchecked` and `override-empty` are the operator's, through the override prompt or Revise.
- Anything else (exit 1 with no `premise:` line, exit 2, exit 3 from the snippet, a missing interpreter, a timeout) → print `premise gate: check_premises.py did not run (<reason>) — writing without the check` and rename the temp. If the rename fails, print it and return to the Confirm gate.

**Mapping rules.** Phase 3 applies these once, to render the candidate.

- `## Problem`, `## Why it matters` and `## Done when` are transcribed from the ticket (or local-only paragraph), never inferred; after that only a verified fold or an operator replacement changes them.
- Local-only header: `**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`.
- A Settled decision framed as a fence ("X is not in scope") → `## Out of scope`.
- Other Settled items → `## Decisions carried forward`, numbered, each with the chosen branch and a one-line why. If none, write `_(none settled — see Risks / decisions)_` and print `warning: interview settled no decisions — the brief pins everything to the spec author`.
- `## Premises` follows Decisions and is always present, in the § Premises shape.
- Open items → `## Risks / decisions`, numbered: `<item> — not established[ (<grilling's short reason>)]; spec author pins this`, or with a `claim:` field, `<item> — operator claims "<claim>", unverified[ (<reason>)]; spec author pins this`. Copy grilling's redacted `claim:` value as is.
- `## Scope` gets one row per path a settled decision or `path:line` fact names: `Current` from the fact with its `path:line`, `Change` from the decision. A `source: run:` fact never backs a Scope row or fills Current. A path with no fact behind it goes to Risks. The heading date is the grounding date; after `origin: behind-N` it reads `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)` with a matching References bullet.
- Facts established → `## References` with `path:line`, or in the run shape `(source: run: "<command>"; exit: <integer>; excerpt: "<text>")`.
- The final References bullet is `Interview: <n> rounds, exit <token>` (with grilling's reason in parentheses when it is `no candidate decision met the altitude fence`), or `Interview: skipped (--no-grill)`.

**`## Scale`** — four cases:

- Settled as a factor with a target → `**Factor:** yes` and `**Target:** <N>` (plus `**Dimensions:**` if given).
- Settled as a factor without a target → no section; add `Scale target — the operator settled scale as a factor but no target N was obtained; spec author pins this` to Risks and print `warning: scale factor settled without a target — section not emitted`. Never emit `**Factor:** yes` without a target: `/spec-cycle` drops it as malformed.
- Settled as not a factor → `**Factor:** no`.
- Never asked → no section.

Under `--no-grill`, apply the same cases to a scale statement the ticket makes explicitly.

Then print:

```
=== BRIEF WRITTEN: <TICKET-ID> ===
Path: docs/specs/TODO/<TICKET-ID>.brief.md
Interview: <n> rounds, exit <token>; <s> settled, <o> open   |   skipped (--no-grill)
Ticket: <tracker | local-only>

=== NEXT ===
/spec-cycle docs/specs/TODO/<TICKET-ID>.brief.md
```

Count `<s>` and `<o>` from the written brief.

## What /spec-brief never does

Its only filesystem mutations are creating `docs/specs/TODO/`, writing and renaming its temp onto the brief, and removing a stale temp of its own shape. It never creates or transitions a ticket, writes a review report, writes before the operator confirms, writes when exit 1 blocks, raises a level to pass the gate, commits, updates the tree, invokes `/spec-cycle`, or changes a chosen branch, a fence, the tier, or the threat model without the operator.

## Tool-use notes

- Read, Grep, and read-only or ref-only Bash (`git fetch origin` bounded by a timeout, `git rev-list`, `git status`), plus the mutations above and the bounded `check_premises.py` run, which only reads the temp.
- Agent for the Phase 1 exploration; the Phase 3 reviewer is a read-only native agent, skill, or command-line tool of another model family.
- Skill for `grilling`.
- The tracker's read capability, optional.

## Failure modes

- **Ticket unresolvable** → local-only mode; the seed gate still applies.
- **Wiki path missing** → skip grounding step 2.
- **Host cannot invoke a nested skill** → halt naming `--no-grill`.
- **Doubt dispatch never returns** → it blocks the run; use the longest timeout the host offers and print the bound when it times out.
