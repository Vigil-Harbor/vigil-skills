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

# /spec-brief — produce the brief

Invoked as:

```
/spec-brief <TICKET-ID>                                  # ticket + grilled interview, the default
/spec-brief <TICKET-ID> --no-grill                       # skip the interview; still confirms before writing
/spec-brief <TICKET-ID> --rounds N --questions N         # tune the interview's bounds
```

The brief is the one lifecycle artifact nothing downstream challenges: `/spec-cycle` dispatches three or four adversarial lenses, and every one of them treats the brief as authority. A fork left open in the brief is therefore invisible to review, and surfaces later as a P0/P1 against the spec. This skill settles those forks first, in a bounded interview, and writes what the interview produced.

## Invocation

- `<TICKET-ID>` must match `^[A-Z][A-Z0-9]*-[0-9]+$` — `/spec-cycle`'s Phase 0 ticket-ID pattern, anchored at both ends because here it is the whole argument, not a filename prefix.
- `--rounds N`: integer, `1 ≤ N ≤ 10`. `--questions N`: integer, `1 ≤ N ≤ 15`. Defaults 3 and 7. The ceilings exist so a flag cannot defeat the fatigue bound this skill adds; there is no `0` alias, because a zero-width round is a stall, not a bound.
- `--no-grill` wins over any cap flag. If both are given, warn `--rounds/--questions ignored under --no-grill` and continue — they are ignored for the interview, but the default question cap (7) still bounds Phase 1's grounding batch.
- Anything else — a malformed ID, a non-integer, an out-of-range value, an unknown flag — halts with: `Usage: /spec-brief <TICKET-ID> [--no-grill] [--rounds 1-10] [--questions 1-15]`.

## Phase 0 — Preflight

1. `project_root` = cwd. Read `<project_root>/CLAUDE.md` (or your harness's project-instructions file; in this repo that is `AGENTS.md`, which the gitignored `CLAUDE.md` points to). Resolve `wiki_root` and `project_slug` if a wiki is configured. If the file hardcodes a username-bearing wiki path that does not exist on this machine, replace the username segment with the current user (Windows: `$env:USERNAME`; Unix: `$USER`) and re-check — the same fallback `/spec-cycle` uses.

2. **Output collision.** Check `docs/specs/TODO/<TICKET-ID>.brief.md`, `docs/specs/TODO/<TICKET-ID>.spec.md`, `docs/specs/TODO/<TICKET-ID>.reviews/`, and `docs/specs/TODO/.<TICKET-ID>.brief.md.tmp`. If **only** the stale temp exists, remove it, log `stale temp removed: .<TICKET-ID>.brief.md.tmp`, and continue without halting. If any other artifact exists, halt:

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

3. **Namespace.** Read `<config-dir>/skills/ship-spec/states.json`, where `<config-dir>` is `$CLAUDE_CONFIG_DIR` when set, otherwise `~/.claude/` on Unix and `%USERPROFILE%\.claude\` on Windows. Look up the ticket prefix for the `namespace` used by the shared-memory lookup in step 5. A missing or unparseable file, or an unknown prefix, is a warning, not a halt: fall back to `namespace = "plane"` and continue.

4. **Origin sync check (warn-only).** Grounding reads the local tree, so a tree behind `origin` produces a brief whose "verified against current files" claim is stale. This step never updates the tree. Any git failure inside it → log `origin: skipped (git error)` and continue.
   a. `git remote get-url origin 2>/dev/null`. Non-zero exit → log `origin: skipped (no remote)` and continue.
   b. `timeout 30 git fetch origin 2>/dev/null` — ref update only. Failure is non-fatal: log `origin: fetch failed (proceeding with available refs)`.
   c. `git symbolic-ref --short -q HEAD`. Empty (detached HEAD) → log `origin: skipped (detached HEAD)`. Otherwise capture `<branch>`, then bind `<cmp>`: `origin/<branch>` if it verifies, else origin's default branch, else `main`, else `master`. None resolve → log `origin: skipped (no comparison branch)`.
   d. `git rev-list --count HEAD..origin/<cmp>`. Zero → log `origin: in-sync`.
   e. Otherwise print `ORIGIN SYNC: local <branch> is <N> commits behind origin/<cmp> — grounding reads the local tree; the brief's "verified against current files" claim may be stale. Consider 'git merge --ff-only origin/<cmp>' first.`, log `origin: behind-N (warned)`, and continue.

5. **Ticket resolution**, in this order, each step optional:
   a. The shared-memory service's tag-only search capability (e.g., `mcp__claude_ai_Vigil_Harbor_MCP_Server__memory_search` in Claude Code, or the equivalent in your host) with `tags: ["plane_work_item", "<TICKET-ID>"]`, the `namespace` from step 3, `source_system: "plane"`, `max_results: 1`.
   b. On zero results or an error: the issue tracker's retrieve-by-identifier capability (e.g., `mcp__plane__retrieve_work_item_by_identifier` in Claude Code, or the equivalent in your host's tracker integration).
   c. On failure of both: **conversation-only mode.** Print `ticket: unresolved (local-only) — describe the problem in a paragraph and I will proceed from that.` and wait. Apply the seed gate (§ Phase 2) to the answer: re-prompt once, then halt. The brief header will read `**Plane:** unresolved (local-only)`, and `/spec-cycle`'s local-only path applies downstream.

   Log one token: `ticket: memory | tracker | local-only`.

6. Print a one-line preflight summary: `ticket: <token> · namespace: <ns> · wiki: <resolved|none> · origin: <token> · grill: on (rounds=N, questions=M) | off (--no-grill)`.

## Phase 1 — Grounding (read-only)

Retrieval-first, in this order, stopping as soon as the seed is sufficient:

1. The ticket text (or, in local-only mode, the operator's paragraph).
2. If `wiki_root` resolved: `<wiki_root>/projects/<project_slug>/state.md` (its header plus the sections the ticket touches) and `filemap.md` if present. This is the mandatory read before any fan-out.
3. The files the ticket names, by path.
4. Only for gaps the first three leave: dispatch a read-restricted exploration agent on the strongest available model (Claude Code: the `Explore` subagent type with an Opus model override, or the equivalent narrowest read-only agent class in your host) — never a general-purpose agent, which inherits the full session tool set. Instruct it to answer with `path:line` evidence only and to make no mutations of any kind: most host agent classes keep shell access even when file-edit tools are withheld. Bound its work in the prompt: answer from the paths named in the question, and return `not found` rather than searching exhaustively. Dispatch these in one parallel batch of at most `question_cap` (the default 7 under `--no-grill`), each carrying a one-line question.

   A failed dispatch — an error, an empty return, or a return without the fact — becomes a fact request in the interview's first round. Under `--no-grill` there is no interview to carry it into, so it becomes a `## Risks / decisions` item instead: `<fact needed> — not established (exploration failed); spec author pins this`.

Assemble `seed`: the problem statement, the facts with their sources, and any related open tickets the ticket text names. Print `grounding: <n> files read, <m> explorations dispatched (<f> failed)`.

## Phase 2 — Interview

Skipped entirely under `--no-grill`. Otherwise run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host) with `seed` from Phase 1, brief altitude — "a decision that changes the brief's Scope, Decisions carried forward, or Out of scope" — and `round_cap` / `question_cap` from the flags. The primitive waits for the operator each round; this skill does nothing until the Grill summary comes back.

**Seed gate.** Before the interview, gate the seed: if the ticket text (or the operator's local-only paragraph) states no problem — under two sentences, or nothing a design decision could hang off — re-prompt once, then halt. In ticket mode the re-prompt is `Ticket <ID> states no problem — describe it in a paragraph and I will proceed from that.`, and the brief header keeps the resolved ticket line while the paragraph becomes the seed. In local-only mode it repeats Phase 0 step 5c's request. If the primitive itself returns `empty-seed`, halt the same way — nothing is written. A success token for "nothing was ever known" would write a hollow brief that every downstream lens then treats as authority.

**If this host cannot invoke a nested skill**, halt: `grilling is unavailable in this host — re-run with --no-grill to write the brief from the ticket alone, or run the interview by hand.` Never write a silently ungrilled brief.

## Phase 3 — Confirm

Render a preview — the numbered `## Decisions carried forward` list (from the summary's Settled items) and the `## Risks / decisions` list (from its Open frontier, each ending "spec author pins this") — then:

```
Write the brief?
1. Write docs/specs/TODO/<TICKET-ID>.brief.md
2. Revise an answer (name the Q number) — that decision and everything settled downstream of it return to the frontier; if the cap was hit, one extra round is granted, once
3. Abort — nothing written
```

Wait for the user's response.

Option 2 re-invokes `grilling` with the Grill summary as `prior_summary` and the same `round_cap` / `question_cap`. The primitive itself owns the resume arithmetic and grants the single post-cap round, exiting `revised-after-cap (+1 round)`; this skill offers option 2 at most once after a cap hit, and once a post-cap resume has returned the block re-renders with options 1 and 3 only.

Under `--no-grill`, option 2 reads `2. Add a decision (state it) — appended to Decisions carried forward`, and the preview's Decisions list is derived **only** from decisions the ticket text states explicitly, each carrying its quote or `path:line`. Anything the model would have to infer goes to `## Risks / decisions` ending "spec author pins this". The altitude fence applies to that derivation exactly as it applies to the interview.

## Phase 4 — Write

Write `docs/specs/TODO/<TICKET-ID>.brief.md` with exactly these sections, in this order and with these headers (`/spec-cycle`'s Phase 3 parser keys on three of them):

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

**Atomic write.** Write the full content to a dot-prefixed temporary sibling, `docs/specs/TODO/.<TICKET-ID>.brief.md.tmp`, and rename it over the target in one step, so an interrupted write never leaves a truncated brief; remove the temp on any failure. The leading dot keeps it outside `/spec-close`'s `<TICKET-ID>.<rest>` companion glob. This repo's `.gitignore` does not ignore `.*.tmp`, so "a stray dot-file from a killed run must not be committed" is a prose rule, not a mechanism — Phase 0 step 2 removes such a file on the next run whether or not any other artifact exists. Create `docs/specs/TODO/` first if it does not exist. That directory creation, this rename, and Phase 0 step 2's removal of a stale temp are this skill's only filesystem mutations outside the brief itself.

Two `/spec-brief` runs on the same ticket in one worktree are outside the supported flow: the collision check is not a lock, the brief is last-writer-wins, and the stale-temp removal cannot distinguish an abandoned temp from a concurrent run's in-flight one.

**Mapping rules.**

- `## Problem`, `## Why it matters`, and `## Done when` are transcribed from the ticket text (or, in local-only mode, the operator's paragraph) — never inferred.
- In local-only mode the header fields read `**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`.
- A Settled decision the operator framed as a fence (an answer of the form "X is not in scope") is written to `## Out of scope`, not to `## Decisions carried forward`.
- The remaining Settled items → `## Decisions carried forward`, numbered, each carrying the chosen branch and its one-line why. If Settled is empty, write `_(none settled — see Risks / decisions)_` under the header rather than leaving it blank, and print `warning: interview settled no decisions — the brief pins everything to the spec author`.
- Open frontier items → `## Risks / decisions`, numbered, each ending "spec author pins this".
- `## Scope` gets one row per path the settled decisions and grounding facts name: `Current` filled from a fact with its `path:line`, `Change` from the settled decision that touches it. A path with no read file or fact behind it gets no row and goes to `## Risks / decisions` instead. The heading date is the date grounding ran; when preflight logged `origin: behind-N`, the heading reads `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)` and a matching `## References` bullet records it.
- Facts established → `## References`, with `path:line`.
- The exit token and round count go in a final `## References` bullet: `Interview: <n> rounds, exit <token>`, or `Interview: skipped (--no-grill)`.

**`## Scale` emission** — four input cases, three emitted shapes:

- A settled decision says scale **is** a factor **and** carries a target → emit `## Scale` with `**Factor:** yes` and `**Target:** <N>` (plus `**Dimensions:**` if given). The factor and its target are one question, not two, so a settled "yes" normally arrives with its N.
- Settled "is a factor" but no target was obtained (cap hit, deferred) → emit **no** `## Scale` section, add `Scale target — the operator settled scale as a factor but no target N was obtained; spec author pins this` to `## Risks / decisions`, and print `warning: scale factor settled without a target — section not emitted`. Never emit `**Factor:** yes` without a target: `/spec-cycle` would silently drop it as malformed.
- Settled "is **not** a factor" → emit `## Scale` with `**Factor:** no`, so `/spec-cycle` records the non-factor Decision.
- Never asked → no section.

Under `--no-grill`, apply the same four cases to a scale declaration the ticket text states explicitly: factor plus target → emit; factor without target → no section, a Risks item, and the warning; an explicit non-factor → `**Factor:** no`. If the ticket says nothing about scale, emit no section.

Then print:

```
=== BRIEF WRITTEN: <TICKET-ID> ===
Path: docs/specs/TODO/<TICKET-ID>.brief.md
Interview: <n> rounds, exit <token>; <s> settled, <o> open   |   skipped (--no-grill)
Ticket: <memory | tracker | local-only>

=== NEXT ===
/spec-cycle docs/specs/TODO/<TICKET-ID>.brief.md
```

## What /spec-brief never does

Creates or transitions a ticket; writes anything other than the one brief file (and its transient `.tmp`, and `docs/specs/TODO/` when absent); deletes anything other than a stale `.<TICKET-ID>.brief.md.tmp` of its own shape; commits; fast-forwards or otherwise mutates the tree; invokes `/spec-cycle`.

## Tool-use notes

- Read, Grep, and Bash (`git remote`, `git fetch origin` bounded by `timeout`, `git symbolic-ref`, `git rev-parse`, `git rev-list`, `git status`, `git log` — all read-only or ref-only, plus `mkdir` for `docs/specs/TODO/` when absent, the rename of the brief's dot-prefixed temp onto its target, and the removal of a stale temp, which are this skill's only filesystem mutations outside the brief) for preflight and grounding.
- Agent for the read-restricted exploration dispatched in Phase 1.
- Skill for `grilling`.
- Write for the single brief file.
- The shared-memory search capability and the issue tracker's read capability, both optional.
- Do not commit. Do not push. Do not open PRs. Do not run `/spec-cycle`.

## Failure modes

- **Ticket unresolvable** (both services down) → local-only mode, not an error; the seed gate still applies.
- **Empty seed** (the ticket text is a bare title, or the local-only paragraph states no problem) → re-prompt once, then halt; nothing is written.
- **Wiki path missing** → skip grounding step 2 silently.
- **Artifacts exist** → halt with the Phase 0 step 2 block; never overwrite silently.
- **Origin behind** → warn only; never update the tree.
- **Host cannot invoke a nested skill** → halt naming `--no-grill` as the alternative; never write an ungrilled brief without the flag.
- **Exploration dispatch fails** → a fact request in round 1, or a `## Risks / decisions` item under `--no-grill`. A dispatch that never returns blocks its batch; the batch cap and the prompt's own bound are the mitigations.
- **Operator abandons mid-interview** → nothing is written; re-run to start over. No resume state is kept, by design.
- **`--no-grill` with cap flags** → warn, ignore the caps, continue.
