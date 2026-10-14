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
   c. On failure of both: **conversation-only mode.** Print `ticket: unresolved (local-only) — describe the problem in a paragraph and I will proceed from that.` and wait. Apply the seed gate (§ Seed gate) to the answer: re-prompt once, then halt. The brief header will read `**Plane:** unresolved (local-only)`, and `/spec-cycle`'s local-only path applies downstream.

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

## Seed gate

Runs after Phase 1 and before the tier gate, in every mode, including `--no-grill`. The sentence "Skipped entirely under `--no-grill`" in Phase 2 does not cover this step.

Gate the seed: if the ticket text (or the operator's local-only paragraph) states no problem — under two sentences, or nothing a design decision could hang off — re-prompt once, then halt, and nothing is written. In ticket mode the re-prompt is `Ticket <ID> states no problem — describe it in a paragraph and I will proceed from that.`, and the brief header keeps the resolved ticket line while the paragraph becomes the seed. In local-only mode it repeats Phase 0 step 5c's request. An empty seed halts before the tier question. If the interview's primitive itself returns `empty-seed`, halt the same way — nothing is written. A success token for "nothing was ever known" would write a hollow brief that every downstream lens then treats as authority.

Once the seed passes, hold the resolved ticket text (or the local-only paragraph) as `ticket_contract`. When this gate collected a paragraph, append it, labelled `Seed-gate paragraph:`. Phase 3 sends `ticket_contract` to its reviewer; it never looks the ticket up again.

## Tier gate

Runs after the seed gate passes, in every mode, before the interview and before Confirm. Nothing in any mode writes a tier the operator did not choose. There is no `--tier` flag and no default that skips the question.

If the host cannot wait, print `tier needs an operator — stopping` and stop. Write nothing. The tier is not filled in.

Otherwise compute the tweak-floor heuristic below and print:

```text
Tier: recommended <tweak|big>
<basis line>

1. tweak
2. small
3. big
4. irreversible
```

The recommended row carries ` (recommended)`. A reply of `1`, `2`, `3`, or `4` after trimming sets the tier. Any other reply stops and writes nothing.

`tweak` is never written into a brief, a spec, or a marker. It exits as follows:

- Collision case: Phase 0 step 2 showed its halt and the operator chose option 1. Print the paths of the brief, the spec, and the reviews tree that exist, state that they stay actionable by `/ship-spec` and `/spec-close` until the operator removes or archives them and re-runs `/spec-brief` clean, and state that spec-brief deletes nothing. Do not print the NEXT block. A stale temp that step 2 already removed is not this case.
- Otherwise print:

```text
=== NO BRIEF WRITTEN: <TICKET-ID> ===
Tier: tweak
<basis line>

=== NEXT ===
No lifecycle — ship as a chore PR citing the ticket; the ticket's state and closing comment are yours to set, since no lifecycle stage will touch it.
```

The tweak path creates no brief temp and deletes nothing. `small`, `big`, or `irreversible` resolves the reviewer (§ Doubt-pass reviewer, below), then continues to the interview, or under `--no-grill` to Phase 3 — Doubt pass. The chosen tier is kept for Phases 3 to 5.

### Tweak-floor heuristic

The recommendation is `tweak` only when the estimate is known, the change is at most 2 files and under 50 lines, and it touches none of auth, payments, data, or config. Any of those four surfaces blocks `tweak` at any size. The heuristic never recommends `small` or `irreversible`. Those are choices on the prompt.

The estimate comes from the ticket text (or the local-only paragraph) and the Phase 1 grounding facts. Scope rows do not exist yet. There is no diff.

A check that cannot be answered is unknown. Any unknown check, or any failed check, recommends `big`.

- **Files.** Distinct file paths the change names. A directory does not count. A wiki `state.md` or `filemap.md` that grounding opened does not count. No file path named for the change → unknown.
- **Lines.** An integer the texts tie to a line count or a diff size; a range uses its top; if several qualify, use the greatest. A ticket id, a date, a file count, or an item number does not qualify. "Under 50" means 49 or fewer. A single typo, a single wording replacement, or a single identifier rename, in one named file, with no other change described, estimates at 1 line. If no qualifying number is stated, that 1-line estimate applies only to that single-edit case; any other change is unknown. A qualifying number wins over the 1-line estimate.
- **Surfaces.** `none` only when at least one file path is named and every named path and the described change were checked and none matched. No named path → unknown, which blocks `tweak`.

Built-in taxonomy. Matching is case-insensitive. A path signal equals one path segment, or equals the whole filename. `config.py` does not match the filename `config`. A directory segment `config` does. A one-word subject signal matches a whole word in the change description. A quoted multi-word signal matches that phrase with a word boundary at each end. The bare word "data" is not a signal.

| Surface | Path signal | Subject signal |
|---|---|---|
| auth | `auth`, `login`, `session`, `oauth`, `credential`, `secret`, `permission`, `rbac` | password, token, credential, secret, login, session, oauth, permission |
| payments | `billing`, `payment`, `invoice`, `subscription`, `checkout`, `payout`, `stripe` | charge, invoice, refund, payout, subscription |
| data | `migration`, `migrations`, `schema` | migration, schema, "drop table", "delete rows" |
| config | a segment or filename `config`; a filename `.env`; a filename `states.json`; a path under `.github/workflows/` | "environment variable", "feature flag" |

A `SKILL.md` file and a docs markdown file are not config unless a signal above matches. `AGENTS.md` and `CLAUDE.md` are not config unless a signal above matches.

**Extension.** An extension signal matches a named path as a substring on purpose, and is not the built-in segment rule. Read the target project's `AGENTS.md` and `CLAUDE.md` when each file is present. This is not a first-source-wins read: each file that is present contributes. Each whole-word `## Tweak surfaces` heading contributes. Its body runs to the next `^#{1,6}` heading. Each non-blank line is one extra signal. Strip one leading list marker (`-`, `*`, or `N.`) and then trim. A line that is empty after that is ignored. A remaining one-word line matches as a one-word signal. A remaining quoted phrase uses the phrase rule above. Any other remaining line is an unknown surface and recommends `big`. Its basis slot is `surfaces: unknown`, with the `never tweak` suffix and a short quote of the line. It is not `surfaces: none`. Signals union. Neither heading hides the other. A one-word signal matches a named path as a substring or the change description as a whole word. A quoted multi-word line uses the phrase rule above. A match blocks `tweak`. No heading in either file means the built-in four only. Extra signals only add surfaces.

**Basis line.** One line, three comma-separated slots, then the suffix, prefixed `basis: `. Files: `<n> file` or `<n> files` (singular when `n` is 1) plus ` (<paths>)`, or `files: unknown`. Lines: `~<m> line` or `~<m> lines` (singular when `m` is 1), or `lines: unknown`. Surfaces: `surfaces: none`, `surfaces: unknown`, or `surfaces: <name>`. When more than one surface matches, name every match, built-in order auth then payments then data then config, then extension lines in file order, joined by `+`. The suffix is `ticket text + grounding` when the recommendation is `tweak`, and `never tweak` otherwise.

Worked examples, normative for that shape:

1. Ticket "fix the typo recieve in README.md". Grounding also opened wiki `state.md` and `filemap.md`. Those do not count. The change names `README.md` only. Recommendation `tweak`. `basis: 1 file (README.md), ~1 line, surfaces: none — ticket text + grounding`
2. Ticket "add a state UUID to skills/ship-spec/states.json". Recommendation `big`. `basis: 1 file (skills/ship-spec/states.json), lines: unknown, surfaces: config — never tweak`
3. Ticket "make the gate stricter" and grounding names no path. Recommendation `big`. `basis: files: unknown, lines: unknown, surfaces: unknown — never tweak`
4. Ticket "drop table users in scripts/cleanup.sql". Grounding names that file and states 10 lines. The phrase "drop table" matches data. Recommendation `big`. `basis: 1 file (scripts/cleanup.sql), ~10 lines, surfaces: data — never tweak`

### Doubt-pass reviewer

Resolve this after a non-tweak tier is chosen and before the interview. Phase 3 dispatches a fresh-context reviewer from a different model family; this step finds out whether one exists.

- **Candidates.** Any mechanism available in this session counts: native agent dispatch, an installed skill, or a command-line tool. A skill counts only when it names the mechanism it dispatches through.
- **Family.** A candidate's family is what it states itself — in its instructions, its configuration, or its runtime output (such as a provider or model line). Its own provider or vendor statement counts as its family. Never infer a family from a tool's name. Compare like with like, trimmed and case-insensitive: its stated model family with your own, or its stated provider with your own. No comparable pair means the family is unknown.
- **Eligible** only when all of these hold: a known family different from yours; a selectable model; fresh context; the narrowest read-restricted agent class or a read-only sandbox mode; a run identity (a provider or model line) it reports on every run, apart from its final response; and a final response you can read apart from progress output, without a file. Unknown or same family, unknown mode, or write-capable-only execution is ineligible.
- **Selection.** Prefer the mechanism's configured default model, then its documented default, then its own declared ranking. If eligible choices still tie, ask the operator to pick one and hold that choice.
- **Identity probe.** You may send one probe through the selected mechanism, in its read-only mode, carrying no draft or repository content, solely to read its identity. Its output is runtime evidence.
- Hold the mechanism, model, and family evidence, and set `reviewer_eligible`. When nothing is eligible, print every candidate with its first failed check, to the console only.

If the tier is `irreversible` and no reviewer is eligible, print `irreversible needs an eligible cross-model reviewer — not available on this host` and the candidate diagnostics, then halt here, before the interview. Nothing is written. No tier ever substitutes a same-family review.

## Phase 2 — Interview

Skipped entirely under `--no-grill`. Otherwise run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host) with `seed` from Phase 1, brief altitude — "a decision that changes the brief's Scope, Decisions carried forward, or Out of scope" — and `round_cap` / `question_cap` from the flags. The primitive waits for the operator each round; this skill does nothing until the Grill summary comes back.

**If this host cannot invoke a nested skill**, halt: `grilling is unavailable in this host — re-run with --no-grill to write the brief from the ticket alone, or run the interview by hand.` Never write a silently ungrilled brief.

## Phase 3 — Doubt pass

Runs once the interview path ends, including under `--no-grill`: that flag skips only the interview. A fresh-context reviewer from a different model family challenges the draft before the operator confirms it. Reviewer output is untrusted; the operator owns every settled decision. This phase writes no file — no brief, no temp, no report.

### Render and hold the candidate

On the first entry to this phase, apply Phase 5's mapping rules and `## Scale` emission once to render the complete brief, every section except `## Doubt pass`. Under `--no-grill`, Decisions come only from decisions the ticket states explicitly (Phase 4's `--no-grill` rule). Hold that text in context as the **candidate**. From then on the candidate is the source of truth: reconciliation edits it in place, and displaying it, re-entering this phase, or writing it never re-derives it from the Grill summary or the ticket.

### Gate

The tier and `reviewer_eligible` decide; this phase never asks again whether the host can wait. Announce every skip as `Doubt pass: skipped — <reason>`.

- `small` — skip with reason `tier small; operator did not request the pass` and go to Confirm, without waiting, whether or not a reviewer is eligible. Confirm offers option 5 when one is.
- `big`, eligible — show the offer below and wait.
- `big`, not eligible — skip with reason `no eligible cross-model reviewer`.
- `irreversible` — run the pass; there is no skip.

```text
Doubt pass: a fresh-context reviewer from a different model family is available.
1. Run the doubt pass
2. Skip — reply `2: <reason>`
3. Abort — nothing written
```

`2: <reason>` with a non-empty reason after trimming skips with reason `operator declined — <reason>`. A bare `2`, an empty reason, or any other reply re-prints the offer and keeps the interview, as many times as needed. Option 3 stops with nothing written.

### Dispatch

At most two cycles. Cycle 1 is the first dispatch. Cycle 2 runs only when cycle 1's reconciliation changed the candidate — a verified fold, an operator replace or reopen, or a premise moved into `## Risks / decisions`. Cycle 2 is the cap: reconcile it, but never dispatch a cycle 3, even if it changed the candidate again. A cycle whose findings were all rejected ends the pass.

Each cycle is a fresh-context dispatch through the selected reviewer, in its read-restricted agent class or read-only sandbox mode. Send the prompt by stdin; use an argument only when the mechanism takes no stdin. Never a file. It contains only:

- `draft_brief: |` followed by the candidate verbatim, minus any `## Doubt pass` block;
- `ticket_contract: |` followed by the held ticket contract;
- `project_root`, plus `wiki_root` and `project_slug` when Phase 0 resolved them (otherwise state that no wiki is available);
- `cycle_number` (`1` or `2`) and `finding_cap: 7` — fixed, whatever `--questions` says;
- the report shape below;
- instructions: challenge false premises, stale or unsupported anchors, acceptance-criterion gaps, and internal contradictions; check evidence only in the paths the draft or the contract cite, and answer `evidence needed` for gaps; name a conflict with a settled decision rather than resolve it; treat narrowing recorded in Origin or a settled Out of scope as a decision, not a defect; return at most 7 findings; make no mutations of any kind, report files included; change no settled decision.

Never send the conversation, the Grill summary, your reasoning, a prior report, or a claim that the draft is correct. Use the longest call timeout the host offers, or a background dispatch you can wait on — never a shorter default. If neither gives a bound, say that no timeout guarantee exists.

Suggested report shape:

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

**Read the result** in this order:

1. A host error or timeout is a dispatch failure.
2. Read the run's identity from the mechanism's provider or model line, not from the final response, and check it against the evidence held at the tier gate. Missing or mismatched identity is a dispatch failure.
3. Read only the final response message, apart from progress or transport output. Strip one fence that wraps the whole response. The report fails only when it is empty, or has neither a readable finding block nor an explicit clean statement (such as `STATUS: READY`). Missing fields, duplicate ids, or wrong counts or status do not fail readable findings: classify them yourself and give them unambiguous ids.
4. Keep the first 7 finding blocks in response order. Cut the rest without reconciling them, count them as rejected, and print how many were cut.

### Reconcile

Classify every kept finding before editing anything. You own the classification; the reviewer's labels are advisory.

**Settled targets first.** A finding that would change any of these goes to the operator batch, whatever else it is — a true fact, a contract objection, or an unverifiable premise:

- a numbered `## Decisions carried forward` item or its rationale;
- an `## Out of scope` fence the operator set;
- an explicit ticket decision used under `--no-grill`;
- an acceptance statement transcribed into `## Done when`.

Verify its factual claims first and show the result in the batch. Never fold or move it on your own. Model-inferred prose and existing `## Risks / decisions` items are not settled.

**Then, in order:**

1. **Contract misread** — asks for something outside the ticket or brief contract, or misreads the draft. Reject with one line of evidence. Narrowing recorded in Origin or a settled Out of scope is not a missing requirement; a challenge to it is a settled target.
2. **Fact or anchor** — a fact, count, path, anchor, current-behavior statement, or claimed omission. Open the live source and check it; reviewer prose is a lookup hint, never evidence. True: fold it, citing `path:line`. Disproved: reject. Cannot be established: add a `## Risks / decisions` item ending "spec author pins this".
3. **Trade-off** — operator batch; never fold.
4. **Noise or duplicate** — reject with the duplicate id or a one-line reason.

A Tier finding is advisory evidence shown at Confirm; only Confirm's option 4 changes the tier. A Scale finding becomes a `## Risks / decisions` item ending "spec author pins this", or is resolved through Phase 5's four `## Scale` cases. Neither takes a free-text replacement in the batch.

Folds may edit Problem, Why it matters, Scope, Done when, Risks / decisions, and References, including their metadata and factual anchors — never a settled target, even inside those sections. Record the source for every correction.

Work in this order: classify all; verify every actionable fact; compose findings that target the same text into one intended result; edit; run the operator batch; update `## Risks / decisions`; then re-read every changed section and every section that consumes a changed decision, so the next cycle and Confirm get one consistent candidate.

**Operator batch.** Before Confirm, show at most 7 settled-target findings per cycle, numbered `F-<n>`. For each, show the settled text, the challenge, and the verification result, including unavailable or disproved evidence. Every tier waits here. Accepted replies, one per line:

- `F-<n>: keep` — the text stands;
- `F-<n>: replace: <non-empty text>` — the text may continue on indented lines; update every consumer;
- `F-<n>: reopen` — remove the decision and add it to `## Risks / decisions` ending "spec author pins this".

A comma-separated id group (`F-1, F-3: keep`) answers overlapping challenges together; overlapping answers must compose to one intended result. Re-print missing, invalid, or conflicting items with the specific reason, keeping the valid answers and the interview. An unknown id is invalid, and so is `abort` mixed with item answers. `abort` as the only non-blank line stops with nothing written. Never infer an answer. Hold each resolution with its Q number when its decision came from a Grill Q.

### Outcome

`Result` is `completed at cap` when cycle 2's reconciliation changed the candidate, or when cycle 2 failed after cycle 1 changed it (Skip or Accept cycle 1); otherwise `completed`. `Cycles` is the number of reconciled cycles. Count findings per distinct root (same target, same concern) across both cycles; a root's last disposition wins:

- **folded** — verified fact or anchor edits you made;
- **operator resolved** — keep, replace, and reopen;
- **rejected** — disproved, contract misread, noise, or cut at the cap of 7;
- **open** — `## Risks / decisions` items the pass left unresolved, reopens included.

A reopen counts as resolved and as one new open item.

### Dispatch failure

Print `Doubt pass dispatch failed: cycle <n>; class <reason>; last line: <last non-blank final-response line | none>`; a timeout reason includes the bound used. Then offer only the choices that apply:

```text
1. Retry once
2. Skip
3. Abort — nothing written
4. Accept cycle 1 (completed at cap)
```

- **Retry** — only when this cycle's retry is unused. One per cycle; it re-sends the same candidate and is not a new cycle.
- **Skip** — `small` and `big` only. Before any cycle reconciled, skip with reason `reviewer dispatch failed — <short reason>`. After cycle 1 reconciled, keep its edits and record `completed at cap`, `Cycles: 1`.
- **Accept cycle 1** — `irreversible` only, after cycle 2's retry is spent, when cycle 1 reconciled and changed the candidate. Records the same as Skip after cycle 1.
- **Abort** — always offered; stops with nothing written.

`irreversible` never skips: once a retry is spent without the Accept precondition, only Abort remains. Invalid replies re-print the available choices and keep the interview. Never substitute a same-family review.

## Phase 4 — Confirm

Show the full candidate exactly as Phase 5 will write it, with its `## Doubt pass` block in place, then `Tier: <level>`, the basis line, any Tier finding from the pass as advisory evidence, and:

```text
Doubt pass: <completed in N cycle(s) | completed at cap (N cycle(s)) | skipped — <reason>>
```

At cap, also print `Final reconciliation edits were not re-reviewed`. When cycle 2 failed, also print `Cycle 2 failed; only cycle 1 completed`. Then:

```
Write the brief?
1. Write docs/specs/TODO/<TICKET-ID>.brief.md
2. Revise an answer (name the Q number) — that decision and everything settled downstream of it return to the frontier; if the cap was hit, one extra round is granted, once
3. Abort — nothing written
4. Change the tier — ask the tier gate again
5. Run the doubt pass
```

Wait for the user's response.

Option 5 appears only when the tier is `small`, a reviewer is eligible, and the pass has not yet run on this candidate. It runs Phase 3 without the `big` offer and returns here; it stays hidden until the candidate changes.

Option 4 shows the same tier prompt. A reply of `1`, `2`, `3`, or `4` after trimming sets the tier. A non-tweak choice returns to the preview with the new tier. A `tweak` choice takes the tier gate's tweak exit before Phase 5. On option 4's re-ask, a reply other than `1`–`4` re-prints the tier prompt and does not discard the interview. The first tier-gate ask, before any interview, still stops and writes nothing on any other reply. Choosing `irreversible` with no eligible reviewer prints the tier gate's `irreversible needs an eligible cross-model reviewer` message and re-shows the tier prompt, keeping the interview, the candidate, and the previous tier. A non-tweak change updates the candidate's `## Tier` and the basis line. A completed result, including at cap, stands under the new tier. A skipped result runs Phase 3's gate again under the new tier; under `irreversible` that runs the pass, and a failure there cannot skip.

Option 2 re-invokes `grilling` with the Grill summary as `prior_summary` and the same `round_cap` / `question_cap`. The primitive itself owns the resume arithmetic and grants the single post-cap round, exiting `revised-after-cap (+1 round)`; this skill offers option 2 at most once after a cap hit, and once a post-cap resume has returned the block re-renders with options 1, 3, and 4, plus 5 under its rule. Option 2 stays omitted there. A revision (option 2) does not clear the tier.

Before resuming, carry the operator's batch resolutions:

- Amend Q-linked items in `prior_summary`: keep leaves the current text and rationale, replace substitutes the new text, and reopen removes the item from Settled and lists it once in Open frontier as `(Q<n>) … unresolved because: deferred`. Invent no Q numbers and reset no counters.
- Q-less resolutions stay in the candidate only. Pass `seed` again with kept Q-less resolutions in its problem statement, labelled as operator-settled constraints the interview must not re-decide. They are not grounding facts: an empirical claim inside one keeps its verification status.

After the resume returns, compare every returned decision with the kept resolutions; any conflict goes through Phase 3's operator batch with temporary `F-<n>` ids (not a reviewer cycle) before Phase 3 runs again, under every tier. Update the affected candidate sections and their consumers, keeping unrelated folds, resolutions, and anchors. Refresh the `Interview:` References bullet from the returned header, and map newly established facts into References and Scope.

Under `--no-grill`, option 2 reads `2. Add a decision (state it) — appended to Decisions carried forward`, and the candidate's Decisions list is derived **only** from decisions the ticket text states explicitly, each carrying its quote or `path:line`. Anything the model would have to infer goes to `## Risks / decisions` ending "spec author pins this". The altitude fence applies to that derivation exactly as it applies to the interview. An added decision is appended to the candidate, keeping its corrections.

Any content change here — a revision or an added decision — voids the doubt-pass result. Drop only the outdated `## Doubt pass` block and re-enter Phase 3 at cycle 1 under the current tier. Reviewer output is never reused.

## Phase 5 — Write

Write `docs/specs/TODO/<TICKET-ID>.brief.md`: the exact candidate the operator confirmed in Phase 4, with its one `## Doubt pass` block. Never re-apply the mapping rules here and never add a second block. The brief has exactly these sections, in this order and with these headers (`/spec-cycle`'s Phase 3 parser keys on three of them):

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
## Tier
## Scale            (conditional — see the emission rule below)
## Doubt pass
## Risks / decisions
## References
```

**`## Tier` emission.** On the write path the tier is `small`, `big`, or `irreversible`. Emit `## Tier` immediately before the conditional `## Scale`, exactly:

```markdown
## Tier

**Level:** small
```

with the chosen level in place of `small`. Emit no second `**Level:**` line and no sibling line. The rest of Phase 5, including Scale's four cases, is unchanged.

**`## Doubt pass` emission.** Every written brief carries exactly one `## Doubt pass` section, after `## Scale` (or straight after `## Tier` when Scale is absent) and before `## Risks / decisions`. A completed pass:

```markdown
## Doubt pass

**Result:** completed | completed at cap
**Cycles:** 1 | 2
**Outcome:** folded <n> fact/anchor findings; operator resolved <n> decision findings; rejected <n>; open <n>
```

A skipped pass:

```markdown
## Doubt pass

**Result:** skipped
**Reason:** <normalized reason>
```

The reason is one of `tier small; operator did not request the pass`, `operator declined — <reason>`, `no eligible cross-model reviewer`, or `reviewer dispatch failed — <short reason>`. Counts follow Phase 3 § Outcome. The section names no vendor, model, or tool and quotes no reviewer prose. It is audit metadata; nothing downstream gates on it.

**Atomic write.** Write the full content to a dot-prefixed temporary sibling, `docs/specs/TODO/.<TICKET-ID>.brief.md.tmp`, and rename it over the target in one step, so an interrupted write never leaves a truncated brief; remove the temp on any failure. The leading dot keeps it outside `/spec-close`'s `<TICKET-ID>.<rest>` companion glob. This repo's `.gitignore` does not ignore `.*.tmp`, so "a stray dot-file from a killed run must not be committed" is a prose rule, not a mechanism — Phase 0 step 2 removes such a file on the next run whether or not any other artifact exists. Create `docs/specs/TODO/` first if it does not exist. That directory creation, this rename, and Phase 0 step 2's removal of a stale temp are this skill's only filesystem mutations outside the brief itself.

Two `/spec-brief` runs on the same ticket in one worktree are outside the supported flow: the collision check is not a lock, the brief is last-writer-wins, and the stale-temp removal cannot distinguish an abandoned temp from a concurrent run's in-flight one.

**Mapping rules.** Phase 3 applies these once, to render the candidate.

- `## Problem`, `## Why it matters`, and `## Done when` are transcribed from the ticket text (or, in local-only mode, the operator's paragraph) — never inferred. After that, only a live-verified Phase 3 fold outside a settled target or an explicit operator replacement changes them; this phase keeps those changes and never restores the ticket wording.
- In local-only mode the header fields read `**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`.
- A Settled decision the operator framed as a fence (an answer of the form "X is not in scope") is written to `## Out of scope`, not to `## Decisions carried forward`.
- The remaining Settled items → `## Decisions carried forward`, numbered, each carrying the chosen branch and its one-line why. If Settled is empty, write `_(none settled — see Risks / decisions)_` under the header rather than leaving it blank, and print `warning: interview settled no decisions — the brief pins everything to the spec author`.
- Open frontier items → `## Risks / decisions`, numbered, each ending "spec author pins this". An `F<n>` item is written as `<fact needed> — not established; spec author pins this`, or, when it carries the `(operator claim, unverified)` qualifier, as `<fact needed> — operator claims "<answer>", unverified; spec author pins this`, with `<answer>` taken from the item's `claim:` field. An item carrying the qualifier with no `claim:` field, or an empty one, takes the plain `<fact needed> — not established; spec author pins this` form.
- `## Scope` gets one row per path the settled decisions and grounding facts name: `Current` filled from a fact with its `path:line`, `Change` from the settled decision that touches it. A path with no read file or fact behind it gets no row and goes to `## Risks / decisions` instead. The heading date is the date grounding ran; when preflight logged `origin: behind-N`, the heading reads `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)` and a matching `## References` bullet records it.
- Facts established → `## References`, with `path:line`.
- The exit token and round count go in a final `## References` bullet: `Interview: <n> rounds, exit <token>`, or `Interview: skipped (--no-grill)`. When the header's reason is `no candidate decision met the altitude fence`, the bullet also carries it: `Interview: 1 rounds, exit fence-empty (no candidate decision met the altitude fence)`, or `Interview: <n> rounds, exit empty-frontier (no candidate decision met the altitude fence)` for a later-round fence-out, with `<n>` taken from the summary header.

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

Count `<s>` and `<o>` from the written brief's settled decisions and open `## Risks / decisions` items, not from the Grill summary.

## What /spec-brief never does

Creates or transitions a ticket; writes anything other than the one brief file (and its transient `.tmp`, and `docs/specs/TODO/` when absent); writes a doubt-review report, or any brief or temp before the operator confirms; deletes anything other than a stale `.<TICKET-ID>.brief.md.tmp` of its own shape; commits; fast-forwards or otherwise mutates the tree; invokes `/spec-cycle`; substitutes a same-family review for the doubt pass; lets a reviewer finding change a settled decision without the operator.

## Tool-use notes

- Read, Grep, and Bash (`git remote`, `git fetch origin` bounded by `timeout`, `git symbolic-ref`, `git rev-parse`, `git rev-list`, `git status`, `git log` — all read-only or ref-only, plus `mkdir` for `docs/specs/TODO/` when absent, the rename of the brief's dot-prefixed temp onto its target, and the removal of a stale temp, which are this skill's only filesystem mutations outside the brief) for preflight and grounding.
- Agent for the read-restricted exploration dispatched in Phase 1.
- The Phase 3 doubt reviewer: a fresh-context, read-only dispatch to a different model family — a native agent (`subagents`), or a command-line tool or an installed skill's shell bridge (`shell`) — chosen at the tier gate. The prompt goes by stdin (an argument only when the mechanism takes no stdin); the report is the final response, never a file.
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
- **No eligible different-family reviewer** → `small` and `big` skip and record it; `irreversible` halts after the tier gate, before the interview. Candidate diagnostics go to the console only.
- **Doubt dispatch fails** — an empty or unreadable report, a host error or timeout, or missing or mismatched run identity → print the failure line and offer Phase 3's failure choices.
- **Doubt dispatch never returns** → it blocks the run. Use the longest timeout the host offers or a background dispatch you can wait on, and print the bound when it times out.
- **Operator abandons the contradiction batch** (`abort`) → nothing is written.
- **Cycle 2 fails** under `small` or `big` → Retry or Skip; Skip keeps cycle 1's edits as `completed at cap`, `Cycles: 1`.
- **Invalid `big` skip reason** (bare `2` or empty) → re-print the offer; the interview is kept.
- **`irreversible` dispatch fails** → never skip: one retry per cycle, then Accept cycle 1 only when Phase 3's precondition holds, otherwise Abort with nothing written.
- **Invalid reply to any post-interview prompt** → re-print that prompt and keep the interview; only an explicit abort ends it.
