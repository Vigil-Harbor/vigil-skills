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
- `--no-grill` wins over any cap flag. If both are given, warn `--rounds/--questions ignored under --no-grill` and continue — they are ignored for the interview, but the default question cap (7) still bounds Phase 1's grounding batch. The flag skips the interview only. It does not skip premise listing, flag confirmation, the Confirm gate, or `check_premises.py`.
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

Retrieval-first, in this order, stopping as soon as the seed is sufficient. A file that states what execution does does not make the seed sufficient:

1. The ticket text (or, in local-only mode, the operator's paragraph).
2. If `wiki_root` resolved: `<wiki_root>/projects/<project_slug>/state.md` (its header plus the sections the ticket touches) and `filemap.md` if present. This is the mandatory read before any fan-out.
3. The files the ticket names, by path.

Before the dispatch in step 4, and before seed assembly includes the facts with their sources, classify each grounding gap and each file-stated result:

A fact needs a run when the question asks what execution does. A file in the working tree that states a result does not skip that run. A question that asks what execution does needs a run even when it also names a path.

A fact that names a path and asks only what that file's text says gets an exploration.

A fact that is a person's intent or a preference gets no dispatch.

When a question asks what execution does and also sounds like a preference, it needs a run. Pure intent or preference, with no question about what execution does, gets no dispatch.

When both a text reading and a run reading are possible, the question needs a run if it asks what execution does, including when it names a path. Only a question that asks what the named file's text says, and does not ask what execution does, gets an exploration.

A run needs the network when the answer requires an outbound connection. When that is unclear, it needs the network.

A file that already states a plan tier skips the network only when that file is what the question asks about. It does not skip a run for a question about what execution does.

Worked split of the no-footprint examples: a runner's operating system needs a local run; an account's plan tier needs the network unless a file in the tree already states that tier and the question asks what that file says; a person's intent gets no dispatch.

A code-text gap is explored as today. A fact about what execution does is not established grounding, even when a file states the result. It is not explored and not run. A fact that names a path and asks only what the text says, and does not ask what execution does, may stay `path:line`. Under `--no-grill` the run-time fact becomes this `## Risks / decisions` item: `<fact needed> — not established (needs a run); spec author pins this`. A `needs a run` gap the per-fact rule reclassifies as pure intent or preference is not omitted. It becomes `<fact needed> — not established; spec author pins this`. Under a normal grill, put the gap in the seed as an unestablished need, labelled `needs a run`, so the primitive applies the per-fact rule itself. The label does not force a run if the primitive classifies the fact as code text.

4. Only for code-text gaps the first three leave: dispatch a read-restricted exploration agent on the strongest available model (Claude Code: the `Explore` subagent type with an Opus model override, or the equivalent narrowest read-only agent class in your host) — never a general-purpose agent, which inherits the full session tool set. Instruct it to answer with `path:line` evidence only and to make no mutations of any kind: most host agent classes keep shell access even when file-edit tools are withheld. Bound its work in the prompt: answer from the paths named in the question, and return `not found` rather than searching exhaustively. Dispatch these in one parallel batch of at most `question_cap` (the default 7 under `--no-grill`), each carrying a one-line question.

   A failed dispatch — an error, an empty return, or a return without the fact — becomes a fact request in the interview's first round. Under `--no-grill` there is no interview to carry it into, so it becomes a `## Risks / decisions` item instead: `<fact needed> — not established (exploration failed); spec author pins this`.

Assemble `seed`: the problem statement, the facts with their sources, and any related open tickets the ticket text names. The facts with their sources include a fact that names a path and asks only what the text says, and does not ask what execution does. A what-execution-does fact is not recorded there as established. Also include each unestablished `needs a run` need from the classification above. Print `grounding: <n> files read, <m> explorations dispatched (<f> failed)`.

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

The tweak path creates no brief temp and deletes nothing. `tweak` does not list premises. `small`, `big`, or `irreversible` resolves the reviewer (§ Doubt-pass reviewer, below). An `irreversible` tier with no eligible reviewer still halts there, before any premise is listed, and writes nothing. Otherwise continue to § Premise listing, then the interview, or under `--no-grill` to Phase 3 — Doubt pass. The chosen tier is kept for Phases 3 to 5.

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

If the tier is `irreversible` and no reviewer is eligible, print `irreversible needs an eligible cross-model reviewer — not available on this host` and the candidate diagnostics, then halt here, before the interview. Nothing is written. No tier ever substitutes a same-family review. That halt lists no premises.

## Premise listing

Runs after reviewer resolution and before the interview. `tweak` has already exited and lists nothing. The irreversible halt above still happens first and lists nothing. A host that cannot wait prints `premises need an operator — stopping` and writes nothing, including no temp.

A premise is a factual claim about current code, an external system, or run-time behavior that a Decision or a Scope row relies on. A requirement, an operator preference, and a settled decision are not premises. Listing proposes the premises from the ticket and from Phase 1 grounding, each with a flag. Propose `Defeats ticket: yes` only when the claim, if false, would make a ticket decision or a scope change pointless. Otherwise propose `no`. Silence is not yes. The model never clears a flag and never writes `**Override:**` on its own.

The levels are said < pointed < walked < ran < reproduced, strict and case-sensitive. ran is the gate line: a defeating premise at said, pointed, or walked blocks Write. reproduced is above the gate line and does not block.

- **said.** No source, or an operator claim stored as unverified. The Source text is `none`, or that unverified-claim text.
- **pointed.** The author opened a `path:line` in this run and the source is that citation with no step trace. Opening the line is the same habit Phase 5 already requires before a Scope Current cell is filled.
- **walked.** spec-brief itself writes the trace. Every step cites a `path:line` the author opened in this run. That trace is one `**Source:**` field line. Later steps stay on that line. A following line that, after at most three leading spaces or one leading tab, matches `^\d+\.\s` is not a continuation. A single `path:line` with no step structure stays pointed. Grilling is not asked to write the trace.
- **ran.** A `source: run:` record that grilling returned in this invocation's hand-off, under Facts established, that passes the whole confirmation paragraph (the command, an integer exit, a non-empty excerpt that supports the whole claim, and the redaction gate). spec-brief judges that the command exercises the real code or system the premise is about, not a mock or stand-in. The script does not. Source is the text from `source: run:` through the excerpt's closing quote, not the `- F1 —` prefix and not the fact sentence.
- **reproduced.** The same ran conditions, and that same Grill summary already shows this fact came from an approved network run against the real external system. The approval heading is `**Network approval.**`. The reply that runs it is `yes` or `approve`. The credential-offer gate that must pass before that approval item is rendered is not a mark on the fact line. The stored run line has no network bit. When the summary does not already show that approval, a matching hand-off line is ran, not reproduced.

A record that appears only in the ticket, the wiki, a file, or the operator's typed reply is not ran and not reproduced. spec-brief does not run commands itself, so it cannot promote a pasted record to ran. Such a record may still support pointed or walked when the author opens the cited lines. A walked trace may raise pointed to walked. It must not raise any level to ran. ran and reproduced move only from a qualifying hand-off line, and only inside the Confirm gate, including the first time Confirm is entered. That move sets Level and Source together. Match the fact sentence — the `<fact>` span in `- F<n> — <fact> (source: run: ...)`, not the whole bullet — to one premise when, after trim, it equals that premise's claim, case-sensitive, or it equals the claim after the quote-fold and the 200-character cut grilling applies when the operator's wording stands. A sentence grilling writes because the wording does not stand does not match. Do not promote every defeating premise from one run. An Open item does not promote. spec-brief passes no seed `id`, and the fact line carries no `ref:`, so claim text is the join. Do not add a field the script must parse, and do not edit grilling to add one. Under `--no-grill` there is no hand-off, so nothing is promoted to ran or reproduced, and a candidate already at either level is demoted by the Confirm gate. A premise at ran or reproduced with no matching hand-off line is demoted.

The operator confirms every flag, or confirms `_(no premises)_`. One reply per line after trimming: `P1: yes` or `P1: no`. The marker is confirmed by a reply of `none`. A missing id, an unknown id, or any other reply re-prints the list and is not confirmation, except `abort` as the only non-blank line, which stops and writes nothing, including no temp. The pre-dispatch confirm and the Confirm gate use this same yes/no shape. They list only premises that are new, whose claim or level changed, or that a Decision newly cites or a Scope row newly relies on. Every flag confirm — here, at the pre-dispatch confirm, and at the Confirm gate — writes each confirmed reply onto that item's `**Defeats ticket:**` line before anything else reads the candidate, including the doubt-pass draft and the script. In the Confirm gate that write happens before the override-or-abort gate reads the flags, so the override gate sees the flags just confirmed.

A defeating premise below ran that needs a run is added to the grilling seed, labelled `needs a run`, unless Phase 1 already added that same claim (compare the claim text after trim, case-sensitive). One seed clause, not two. spec-brief does not also run the command. On a host with no read-only sandbox, do not dispatch an exploration in place of a run, and do not treat a file that states a result as a run. The premise stays at pointed or walked when the author opened lines, otherwise said.

Ids are append-only for the whole run, including the operator. A premise is not dropped, and ids are not renumbered. The operator changes a premise through revise or through the doubt-pass replies, not by deleting its id.

A premise item, and the no-premises marker, have this shape. The same edit that writes the first item deletes the marker. When items exist, the marker is absent before the script runs.

```markdown
## Premises

1. **P1.** The vendor SDK injects the clock.
   **Level:** pointed
   **Source:** vendor/sdk.py:12
   **Defeats ticket:** no

2. **P2.** The job writes the ledger before it returns.
   **Level:** walked
   **Source:** 1. skills/app/SKILL.md:10 opens the job. 2. skills/app/SKILL.md:40 opens the write.
   **Defeats ticket:** yes
   **Override:** operator accepts the trace for this brief

3. **P3.** The ledger file appears after the job command.
   **Level:** ran
   **Source:** source: run: "python -m app.job"; exit: 0; excerpt: "wrote ledger"
   **Defeats ticket:** yes
```

```markdown
## Premises

_(no premises)_
```

Every numbered item under `## Decisions carried forward` carries `**Rests on:** none` or `**Rests on:** P1 (said); P2 (ran)`. Citations are separated by a semicolon and one space. The level in parentheses is the premise's level and must match the item. When the cited set is non-empty and every cited premise is said, pointed, or walked, that item also contains a line which, after at most three leading spaces, equals `**Below ran:** yes`. Otherwise that line is absent. `**Rests on:** none` does not take `**Below ran:**`. `**Rests on:**` and `**Below ran:**` are derived lines, not settled rationale. Rewrite them whenever a premise's level or id changes, before the gate runs. A level-only finding stays a fact/anchor fold. Moving these two lines does not make that finding a settled-target finding. The placeholder `_(none settled — see Risks / decisions)_` is not a Decision and carries no `Rests on`. Out-of-scope fences and Scope rows do not carry `Rests on`. A premise that only a Scope row relies on still appears in `## Premises` and still gates when its flag is yes.

An override is a line `**Override:** <reason>` on that premise item. The level is not raised to make the gate pass. A change to the claim text or to the level clears the override. Tell the operator that the override was cleared. An override whose reason is empty after trim is not an override.

## Phase 2 — Interview

Skipped entirely under `--no-grill`. Otherwise run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host) with `seed` from Phase 1, brief altitude — "a decision that changes the brief's Scope, Decisions carried forward, or Out of scope" — and `round_cap` / `question_cap` from the flags. Premise listing has already added each defeating below-ran `needs a run` clause that Phase 1 did not already carry. This phase does not add those clauses again and does not run the command. The primitive waits for the operator each round; this skill does nothing until the Grill summary comes back.

**If this host cannot invoke a nested skill**, halt: `grilling is unavailable in this host — re-run with --no-grill to write the brief from the ticket alone, or run the interview by hand.` Never write a silently ungrilled brief.

## Phase 3 — Doubt pass

Runs once the interview path ends, including under `--no-grill`: that flag skips only the interview. A fresh-context reviewer from a different model family challenges the draft before the operator confirms it. Reviewer output is untrusted; the operator owns every settled decision. This phase writes no file — no brief, no temp, no report.

### Render and hold the candidate

On the first entry to this phase, apply Phase 5's mapping rules and `## Scale` emission once to render the complete brief, every section except `## Doubt pass`. Under `--no-grill`, Decisions come only from decisions the ticket states explicitly (Phase 4's `--no-grill` rule). That first render includes `## Premises`, `**Rests on:**` on each numbered Decision, and `**Below ran:** yes` when every cited premise is below ran. Premises that new Decisions or Scope rows rely on, and that were not listed in premise listing, are added here. When the first premise is added, delete `_(no premises)_` in that same edit. When any item exists, the marker is absent. Hold that text in context as the **candidate**. From then on the candidate is the source of truth: reconciliation edits it in place, and displaying it, re-entering this phase, or writing it never re-derives it from the Grill summary or the ticket. The Confirm gate's Level and Source assignment, and its rewrite of derived `**Rests on:**` and `**Below ran:**` lines, edit those lines only. The never-re-derive rule stays for every other section.

Before the doubt-pass dispatch, the operator confirms flags on premises that are new, whose claim or level changed, or that a Decision newly cites or a Scope row newly relies on. Use the premise-listing reply rule. Write each confirmed reply onto that item's `**Defeats ticket:**` line before the doubt-pass draft reads the candidate. A host that cannot wait prints `premises need an operator — stopping` and writes nothing, including no temp. The doubt pass does not ask the flag question again.

### Gate

The tier and `reviewer_eligible` decide; this phase never asks again whether the host can wait. Announce every skip as `Doubt pass: skipped — <reason>`.

- `small`, entered from Confirm option 5 — run the pass.
- `small`, otherwise — skip with reason `tier small; operator did not request the pass` and go to Confirm without waiting, eligible reviewer or not. Confirm offers option 5 when one is eligible.
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
- an acceptance statement transcribed into `## Done when`;
- a `Defeats ticket` flag on a premise. For that finding, including one that also challenges the level, the whole finding goes to the operator batch. Do not split it. The model does not fold the flag. For that finding the batch accepts only `F-<n>: keep` and `F-<n>: replace: <non-empty text>`. `reopen` is not accepted: it must not remove the premise or move it into `## Risks / decisions`. The general batch's `reopen` verb stays for other settled targets. `replace` may change the flag and must leave a well-formed item in `## Premises`. If the flag becomes `yes` and the level is below ran, clear `**Override:**` only when the claim or the level also changed, and re-arm the Confirm gate before Write. `abort` as the only non-blank line still writes nothing. This adds no pass, no cycle, and no reviewer.

Verify its factual claims first and show the result in the batch. Never fold or move it on your own. Model-inferred prose and existing `## Risks / decisions` items are not settled.

**Then, in order:**

1. **Contract misread** — asks for something outside the ticket or brief contract, or misreads the draft. Reject with one line of evidence. Narrowing recorded in Origin or a settled Out of scope is not a missing requirement; a challenge to it is a settled target.
2. **Fact or anchor** — a fact, count, path, anchor, current-behavior statement, or claimed omission. A finding that challenges a premise's level, claim, or source, and does not challenge the flag, is this class. Open the live source and check it; reviewer prose is a lookup hint, never evidence. True: fold it, citing `path:line`. A valid `source: run:` record is one that passes the full confirmation gate: the command, an integer exit code, a non-empty excerpt that is not only redaction markers, a fact sentence that is not only those markers, and an excerpt that supports the whole claim. An excerpt or a fact sentence whose every non-whitespace run is made only of `[redacted]` and `.` does not pass, including `[redacted]...`, `...`, and repeated `[redacted]` markers. A fold must not delete a record that passes that gate. A `path:line` may be added beside it and is data: it must not add a Scope row or fill Current. "Cannot be established" does not apply to a record that passes that gate. A record that fails the gate is not protected and may be moved to Risks. Disproved: reject. Cannot be established: add a `## Risks / decisions` item ending "spec author pins this". A fold must not turn a run-time gap, or a `needs a run` Risks item, into a References fact that has only `path:line`. A file citation may sit beside a valid `source: run:` record and must not delete that Risks item. A `## Risks / decisions` item is not a settled target. A premise fold may edit that premise's claim, level, and source. It must not edit `Defeats ticket` and must not write `**Override:**`. If the fold changes the claim or the level, clear `**Override:**`. A fold that changes a level also rewrites every `**Rests on:**` parenthetical and adds or removes `**Below ran:** yes` in the same edit, before the gate. A fold that raises the level to ran or reproduced sets Source to the run record on the matching this-invocation hand-off line in that same edit. It must not raise the level without that record, and it must not leave Level at ran or reproduced while Source is not that record. Set both together, or demote per the Confirm gate. The reviewer's suggested level is not that record. Those two Decision lines are derived, not settled rationale. The fold still must not edit the Decision's rationale. A level-only finding does not become a settled-target finding because those derived lines move. A demotion of a defeating premise below ran does not block inside the pass. It re-arms the Confirm gate.
3. **Trade-off** — operator batch; never fold.
4. **Noise or duplicate** — reject with the duplicate id or a one-line reason.

A Tier finding is advisory evidence shown at Confirm; only Confirm's option 4 changes the tier. A Scale finding becomes a `## Risks / decisions` item ending "spec author pins this", or is resolved through Phase 5's four `## Scale` cases. Neither takes a free-text replacement in the batch.

Folds may edit Problem, Why it matters, Scope, Done when, Risks / decisions, References, and `## Premises`, including their metadata and factual anchors — never a settled target, even inside those sections. Record the source for every correction.

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

The Confirm gate runs on every entry to Confirm, before Write is offered. That includes the first entry, a return from a non-zero or did-not-run script, `--no-grill`, a skipped doubt pass, and tier `small`. It also runs again after a candidate change (option 2 revise, an added decision under `--no-grill`, or a doubt-pass fold), before Write is offered again. One procedure:

1. Before flags, overrides, and the script, assign Level and Source together from one matching hand-off line. This is not a promotion-only pass. On one Facts-established line whose fact sentence matches that premise's claim, including the quote-fold and 200-character cut when the wording stands, and whose record qualifies, set Level to ran or reproduced and set Source to that run record. That record is the text from `source: run:` through the excerpt's closing quote. Do not promote from an Open item. Do not apply one run to every defeating premise. If Level is already ran or reproduced and no hand-off line matches, demote it. Drop Source text that contains `source: run:` and is not this invocation's matching hand-off line. Walked when what remains is one Source field line and every step cites a `path:line` the author opened. Otherwise pointed when a `path:line` the author opened remains. Otherwise said, with Source `none`. A premise that was never ran or reproduced keeps its non-run level when nothing matches. Under `--no-grill` there is no summary, so nothing is promoted, and a candidate already at ran or reproduced is demoted the same way. A premise at ran or reproduced with no matching hand-off line is demoted.
2. This assignment rewrites that premise's level and source. It clears an override whose claim or level changed, including a demotion, and says so. It rewrites the derived `**Rests on:**` and `**Below ran:**` lines. It does not re-derive the rest of the candidate. The never-re-derive rule stays for every other section.
3. Append premises the current Decisions or Scope rows rely on and that are not yet items. When the first premise is added, delete _(no premises)_ in that same edit. When items exist, the marker is absent before the script runs.
4. Rewrite every `**Rests on:**` parenthetical to the premise's current level, and add or remove `**Below ran:** yes` per the citation rule, before flags are confirmed and before the script runs. A level-only change does not edit the Decision's rationale.
5. Show the candidate those rewrites produced, including its `## Doubt pass` block, before flags, overrides, and the script. The operator confirms flags and overrides against that shown text. Do not show a pre-rewrite preview and then write the rewrite.
6. The operator confirms flags on premises that are new, whose claim or level changed, or that are newly cited by `Rests on` or newly relied on by a Scope row. Silence is not yes. A partial set of replies is re-prompted and is not confirmation. `abort` as the only non-blank line stops and writes nothing, including no temp. If the host cannot wait, print `premises need an operator — stopping` and write nothing.
7. Write each confirmed flag reply onto that item's `**Defeats ticket:**` line before the override-or-abort gate reads the flags. The override gate sees the flags just confirmed.
8. Then the override-or-abort gate. Every defeating premise at said, pointed, or walked needs a non-empty override, or the operator aborts. Do not offer Write while one is missing. The operator replies `P1: <reason>` for each such premise. A reason that is empty after trim is re-prompted and is not an override. A partial set of reasons is re-prompted and is not done. `abort` as the only non-blank line writes nothing, including no temp. If the host cannot wait, print `premise override needs an operator — stopping` and write nothing. ran and reproduced need no override. A non-defeating premise below ran needs no override.
9. Apply each non-empty override reply onto `**Override:**` on that item. The model still does not write `**Override:**` on its own. If a reply changed the text, show that updated candidate once. The gate ends here. No temp exists while the menu below waits, so Abort, Revise, Change the tier, the doubt pass, and a host stop at the menu act with nothing on disk.

Write is offered only now. On a non-zero exit or a did-not-run result from `check_premises.py`, delete the temp, print the error, and return to this gate. Do not offer Write. If a flag confirm or an override prompt is pending, that prompt is the wait, and its abort rule applies. If neither prompt is pending, show Revise and Abort and do not show Write. `abort` as the only non-blank line still writes nothing, including no temp. Do not run the script again until that post-reply candidate changes. The reply write happens before the first run, so it is not a second run. A revise changes the candidate and re-enters this gate, which may run the script again only after that change.

When the gate offers Write, show `Tier: <level>`, the basis line, any Tier finding from the pass as advisory evidence, and:

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

After the resume returns, compare every returned decision with the kept resolutions; any conflict goes through Phase 3's operator batch with temporary `F-<n>` ids (not a reviewer cycle) before Phase 3 runs again, under every tier. Apply Phase 5's mapping rules to the returned new or changed items only: a fence ("X is not in scope") goes to `## Out of scope`, other Settled items to `## Decisions carried forward`, Open items to `## Risks / decisions`, and an emptied Decisions list takes the `_(none settled — see Risks / decisions)_` line. Renumber each list you changed, then update the sections that consume those items. Leave unrelated folds, resolutions, and anchors as they are. Refresh the `Interview:` References bullet from the returned header. Map a new `path:line` fact into References and Scope. Map a new `source: run:` fact into References only. It never backs a `## Scope` row on its own and does not fill Current.

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
## Premises
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

**Atomic write.** Write the full content to a dot-prefixed temporary sibling, `docs/specs/TODO/.<TICKET-ID>.brief.md.tmp`. Write the temp from the candidate after flag replies and override lines are on the items. Then run `check_premises.py` on that temp, before the rename. Exit 0 renames that temp without re-writing it. The pre-reply snapshot is never renamed. Any non-zero exit, a usage error, a missing script, a missing interpreter, a timeout, or a failure to run deletes that temp if it exists, prints the error, and returns to the Confirm gate. It does not return to a bare Write menu. Nothing is left at the brief path. If the skill's prompt and the script disagree, the script wins: do not rename. No temp exists while the Phase 4 menu waits.

Resolve the directory the way Phase 0 step 3 already does. In the shell command write `$CLAUDE_CONFIG_DIR` when it is set, otherwise `$HOME/.claude`. Never write `~` or `%USERPROFILE%` inside quotes. The script path is that directory plus `/skills/spec-brief/scripts/check_premises.py`, with `/` separators. Pre-check that the path is a file. Double-quote the script path and the temp path. Invoke `python` on those two quoted arguments, one positional brief path. Bound the process with the host's short command timeout. Do not probe `python3` before `python`. On timeout, a missing interpreter, or a spawn failure, take the did-not-run path. Do not rename.

```bash
CONFIG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SCRIPT="$CONFIG/skills/spec-brief/scripts/check_premises.py"
TEMP="docs/specs/TODO/.<TICKET-ID>.brief.md.tmp"
if test -f "$SCRIPT"; then
  python "$SCRIPT" "$TEMP"
else
  echo "premise gate: check_premises.py did not run (not found at $SCRIPT — install with 'python sync.py install') — Write blocked" >&2
  exit 3
fi
```

If the pre-check fails, do not invoke `python`. The snippet then exits 3, which is the did-not-run path, never a pass.

When the script does not run, print `premise gate: check_premises.py did not run (<reason>) — Write blocked`. Reasons include `not found at <path>`, `python not found`, and the host error text. Name `python sync.py install` in the not-found line. When the script exits non-zero, print `premise gate: check_premises.py exited <n> — Write blocked` and the script's stderr. Running the script does not add a filesystem mutation: it only reads the temp. Deleting the temp on failure is the removal this paragraph already allows.

The leading dot keeps the temp outside `/spec-close`'s `<TICKET-ID>.<rest>` companion glob. This repo's `.gitignore` does not ignore `.*.tmp`, so "a stray dot-file from a killed run must not be committed" is a prose rule, not a mechanism — Phase 0 step 2 removes such a file on the next run whether or not any other artifact exists. Create `docs/specs/TODO/` first if it does not exist. That directory creation, this rename, and Phase 0 step 2's removal of a stale temp are this skill's only filesystem mutations outside the brief itself. An interrupted write still must not leave a truncated brief: remove the temp on any failure.

Two `/spec-brief` runs on the same ticket in one worktree are outside the supported flow: the collision check is not a lock, the brief is last-writer-wins, and the stale-temp removal cannot distinguish an abandoned temp from a concurrent run's in-flight one.

**Mapping rules.** Phase 3 applies these once, to render the candidate.

- `## Problem`, `## Why it matters`, and `## Done when` are transcribed from the ticket text (or, in local-only mode, the operator's paragraph) — never inferred. After that, only a live-verified Phase 3 fold outside a settled target or an explicit operator replacement changes them; this phase keeps those changes and never restores the ticket wording.
- In local-only mode the header fields read `**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`.
- A Settled decision the operator framed as a fence (an answer of the form "X is not in scope") is written to `## Out of scope`, not to `## Decisions carried forward`.
- The remaining Settled items → `## Decisions carried forward`, numbered, each carrying the chosen branch and its one-line why. If Settled is empty, write `_(none settled — see Risks / decisions)_` under the header rather than leaving it blank, and print `warning: interview settled no decisions — the brief pins everything to the spec author`. Each numbered item also carries `**Rests on:** none` or `**Rests on:** P1 (said); P2 (ran)`, and `**Below ran:** yes` when every cited premise is said, pointed, or walked. The placeholder carries no `Rests on`.
- `## Premises` comes immediately after `## Decisions carried forward`. The section is always present. With no premises it contains exactly `_(no premises)_` and nothing else. Each item uses the shape in § Premise listing: `N. **PN.**` plus the claim, then `**Level:**`, `**Source:**`, `**Defeats ticket:**`, and `**Override:**` only when the operator recorded a non-empty reason. When the first premise is added, delete `_(no premises)_` in that same edit. When items exist, the marker is absent.
- Open frontier items → `## Risks / decisions`, numbered, each ending "spec author pins this". An `F<n>` item is written as `<fact needed> — not established; spec author pins this`, or, when it carries the `(operator claim, unverified)` qualifier, as `<fact needed> — operator claims "<answer>", unverified; spec author pins this`, with `<answer>` taken from the item's `claim:` field. An item carrying the qualifier with no `claim:` field, or an empty one, takes the plain `<fact needed> — not established; spec author pins this` form. When the item's `unresolved because` carries one short parenthetical, copy that parenthetical unchanged into the Risks line, before "spec author pins this". Do not copy a long `ℹ️` display tag. The lines are `<fact needed> — not established (no read-only sandbox); spec author pins this`, `<fact needed> — not established (network run not offered); spec author pins this`, `<fact needed> — not established (run needs a write); spec author pins this`, and `<fact needed> — not established (network approval spent, batch full); spec author pins this`. An unverified claim keeps the existing claim form, with the short parenthetical before the required ending. The lines are `<fact needed> — operator claims "<answer>", unverified (no read-only sandbox); spec author pins this`, `<fact needed> — operator claims "<answer>", unverified (network run not offered); spec author pins this`, `<fact needed> — operator claims "<answer>", unverified (run needs a write); spec author pins this`, and `<fact needed> — operator claims "<answer>", unverified (network approval spent, batch full); spec author pins this`. A claim check whose approved network run does not fit the post-answer cap uses the last of those lines and keeps `claim:`. A carried network claim that never renders keeps `claim:`.
- `## Scope` gets one row per path the settled decisions and grounding facts name: `Current` filled from a fact with its `path:line`, `Change` from the settled decision that touches it. A `source: run:` fact does not name a Scope path, never backs a `## Scope` row on its own, and does not fill Current. A `path:line` inside the excerpt or the fact sentence is data. A different fact that itself has `path:line` may still back a row. A path with no read file or fact behind it gets no row and goes to `## Risks / decisions` instead. The heading date is the date grounding ran; when preflight logged `origin: behind-N`, the heading reads `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)` and a matching `## References` bullet records it.
- Facts established → `## References`, with `path:line`. A `source: run:` fact is a `## References` bullet in the hand-off's run shape, `(source: run: "<command>"; exit: <integer>; excerpt: "<text>")`, and never backs a `## Scope` row on its own and does not fill Current. A different fact that has a `path:line` may still back a row.
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

Creates or transitions a ticket; writes anything other than the one brief file (and its transient `.tmp`, and `docs/specs/TODO/` when absent); writes a doubt-review report, or any brief or temp before the operator confirms; writes a brief when the premise gate blocks; raises a level to clear the gate; changes grilling or spec-cycle; deletes anything other than a stale `.<TICKET-ID>.brief.md.tmp` of its own shape; commits; fast-forwards or otherwise mutates the tree; invokes `/spec-cycle`; substitutes a same-family review for the doubt pass; lets a reviewer finding change a settled decision without the operator.

## Tool-use notes

- Read, Grep, and Bash (`git remote`, `git fetch origin` bounded by `timeout`, `git symbolic-ref`, `git rev-parse`, `git rev-list`, `git status`, `git log` — all read-only or ref-only, plus `mkdir` for `docs/specs/TODO/` when absent, the rename of the brief's dot-prefixed temp onto its target, the removal of a stale temp, and `python` on `check_premises.py` with the quoted temp path, bounded by the host's short command timeout, which only reads that temp — the mkdir, the rename, and the temp removal are this skill's only filesystem mutations outside the brief) for preflight, grounding, and the premise gate.
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
- **Grounding gap that needs a run** → not dispatched. Under `--no-grill` it becomes the `## Risks / decisions` item `<fact needed> — not established (needs a run); spec author pins this`.
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
- **Host cannot wait at premise listing or at the pre-dispatch flag confirm** → print `premises need an operator — stopping` and write nothing, including no temp.
- **Host cannot wait at the override prompt** → print `premise override needs an operator — stopping` and write nothing, including no temp.
- **`abort` as the only non-blank line** at the initial listing, the pre-dispatch flag confirm, the Confirm flag confirm, or the script-failure return when no flag or override prompt is pending → write nothing, including no temp.
- **Script missing** → print `premise gate: check_premises.py did not run (not found at <path> — install with 'python sync.py install') — Write blocked`, delete the temp if it exists, and return to the Confirm gate. Do not offer Write.
- **Empty or partial override** → re-prompt. Write is not offered.
- **Script non-zero, timeout, or did-not-run** → return to the Confirm gate, do not offer Write, do not run `check_premises.py` again until that post-reply candidate changes, and leave no brief.
