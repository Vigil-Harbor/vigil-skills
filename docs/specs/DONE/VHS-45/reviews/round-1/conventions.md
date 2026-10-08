# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: `states.json` is cited as `/spec-brief`'s lookup, and it is read after approval
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 12 (the `project_id` bullet); spec § Phase 1 — Storage probe; spec § Phase 4 — File
**Convention violated:** The installed `states.json` lookup already has two different shapes. Path resolution is shared. The field and the failure mode are not.
**Evidence:** `/spec-brief` Phase 0 step 3 reads `<config-dir>/skills/ship-spec/states.json` (`$CLAUDE_CONFIG_DIR`, else `~/.claude/` / `%USERPROFILE%\.claude\`) for `namespace`, and a missing file or unknown prefix "is a warning, not a halt" (`skills/spec-brief/SKILL.md`). `/ship-spec` preflight step 9 reads `project_id` and **halts** when the prefix is missing, before any implementation (`skills/ship-spec/SKILL.md`). `/spec-close` Phase 0 step 4 reads `project_id` during preflight, before the confirmation (`skills/spec-close/SKILL.md`). Decision 12 says "the same lookup `/spec-brief` uses" and, in the same bullet, "halts the tracker modes". The read is specified on the file path, not in Phase 1, so option 1 can be offered before the file is known to be usable.
**Suggested fix:** Cite `/spec-brief` and `/spec-close` only for the config-dir path. Cite `/ship-spec` for the field (`project_id`) and the halt. Move the read into Phase 1 for `native` and `text`. A missing, unreadable, or unknown-prefix file sets storage to `halt` (option 1 omitted). `local` still does not read the file.

### F-2: Parent resolution forbids shared memory, and the AGENTS.md edit leaves the opposite rule in place
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 12 ("Do not consult shared memory."); spec § Decision 10 (External dependencies sentence)
**Convention violated:** `AGENTS.md` § External dependencies — ticket reads go through shared memory; the tracker is the write path.
**Evidence:** `AGENTS.md` says "Ticket reads now flow through MCP memory via `memory_search` (cached by MCP-33 webhook receiver). Skills warn-and-proceed on cache miss." `/spec-brief` resolves a ticket memory-first, then the tracker's retrieve-by-identifier (`skills/spec-brief/SKILL.md` Phase 0 step 5). Decision 10 adds a sentence that this skill uses the issue tracker when the probe succeeds. It does not narrow the existing sentence, so the file would state both rules. Omitting `shared-memory` from `requires:` matches Decision 12 and is the right declaration for a create precondition. The guidance file still needs to say so.
**Suggested fix:** In the External dependencies edit, state that `/spec-tickets` resolves the parent on the tracker itself because that read is a create precondition, and that it does not consult shared memory. Narrow the existing sentence to the skills that still read tickets from memory (`/spec-brief`, `/spec-cycle`, `/spec-close`'s PR lookup).

### F-3: Piece labels `P1`, `P2` reuse the review severity scale
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Phase 2 — Draft ("Stable labels in the prompt (`P1`, `P2`, …)")
**Convention violated:** `AGENTS.md` § Conventions — the shared severity scale is P0/P1/P2/P3/P4, and P0/P1 are what blocks `/ship-spec`.
**Evidence:** `AGENTS.md` says the severity scale "is shared across all reviewers" and "P0/P1 block shipping". This skill sits between `/spec-cycle` and `/ship-spec`, where `P1` already means a blocking finding. Phase 2 tells the skill to use `P1`, `P2`, … as piece labels. The Phase 3 block does not have a slot for them; it identifies pieces by slug. The two sections disagree, and the labels that do get spoken collide with the scale.
**Suggested fix:** Delete the `P1`/`P2` sentence. The approval block already names pieces by slug and says those labels are not an execution order. Do not introduce a second numeric series.

### F-4: "The `requires:` block is exactly …" is not what the test command checks
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 11 (the `requires:` fence); spec § Test command (the `python -c` lint assert)
**Convention violated:** A load-bearing `requires:` block is pinned as a set, not merely as "lints clean". `tests/test_spec_close_log.py` (`test_lint_is_clean_including_warns` and the key-set assert above it) checks both zero WARN and the exact key set, because `lint.py` accepts any schema-valid block.
**Evidence:** Contract §3 (`docs/portability-contract.md`): absent booleans mean `false`, and a `?` service is optional warn-and-proceed. Decision 11 says the block is exactly `filesystem: [read, write]` and `services: [issue-tracker?]`, and that `shell`, `network`, `subagents`, and `shared-memory` stay absent. The `python -c` gate only asserts zero `ERROR` and zero `WARN`. Copying `/spec-brief`'s full block (`shell`, `network`, `subagents`, `shared-memory?`) would still pass, and a required `shell: true` would make a harness without a shell refuse the skill before it could run.
**Suggested fix:** Keep "no new test module" and the census-only edit to `tests/test_lint.py`. Extend the `python -c` command so it also asserts the frontmatter `requires:` keys are exactly `filesystem` and `services`, `services` is `issue-tracker?`, and `shell` / `network` / `subagents` / `shared-memory` are absent.

### F-5: Decision 4's sizing sentence is the reference skill's wording
**Severity:** P3
**Where:** spec § Decision 4
**Convention violated:** The repo is public. VHS-28 and `AGENTS.md` § Superseded vendor skills treat upstream skill text as behavioral reference only; the skill body is a clean-room rewrite. Decision 4 already says "The skill text is original."
**Evidence:** `mattpocock/skills` `skills/engineering/to-tickets/SKILL.md` says "Each slice is sized to fit in a single fresh context window" and "A completed slice is demoable or verifiable on its own." Decision 4 says "verifiable on its own and small enough for one fresh context window". The brief's own words are "verifiable alone and fit one context window" — the spec moved toward the upstream sentence by adding "fresh" and "on its own". The rest of the spec does not paste that file: no "tracer bullet", no "Make the change easy…", no `ready-for-agent`, no `.scratch/` path, no "What to build", and the local line is `None — no blockers.` rather than `None (can start immediately)`. An implementer transcribing Decision 4 into `SKILL.md` would still ship the near-quote.
**Suggested fix:** Reword the sizing rule in the spec to the brief's words ("verifiable alone, and small enough for one context window") so the sentence the skill must carry is already original. Add one forbid-list to the "skill text is original" sentence: do not reuse "tracer bullet", "Make the change easy, then make the easy change.", "ready-for-agent", "What to build", or the `.scratch/` layout.

### F-6: "Frontier" is already the interview term in the workflow reference
**Severity:** P3
**Where:** spec § Phase 3 — Approval (the `Frontier` line); spec § Decision 10 (the new workflow-reference section)
**Convention violated:** Naming. `docs/spec-workflow-reference.md` (Skill 0, the grilling contract) already defines **frontier** as "every decision whose prerequisites are already settled."
**Evidence:** That definition is the interview frontier. The approval block uses `Frontier` for "nothing blocks these; they can run together" — the unblocked-piece set. Decision 10 puts a summary of this skill between Skill 1 and Skill 2 of that same document.
**Suggested fix:** In the workflow-reference summary, say "unblocked pieces" and do not use frontier unqualified. In the skill's approval block, keep the parenthetical, and add half a sentence that this list is not the grilling frontier.

### F-7: Drift-check — spec-level additions with rationale
**Severity:** P3
**Where:** spec § Decisions 3, 4, 5, 6, 7, 9, 10, 11, 12
**Convention violated:** None. These are class (c): the brief or its Risks section authorizes the pin, and the spec gives a reason. Class (d) silent additions: none found. Decisions 1, 2, and 8 stay inside the brief's Decisions carried forward.
**Evidence:** Brief Decisions 1–8 and `## Scale` (`**Factor:** no`). Risks 1–3 say the spec author pins the doc list, the lint census, and the native-relation path.
**Suggested fix:** No edit required. The drift-check list is:

- **Decision 3** — `blocked_by` in the schema is the only relation capability; `blocking` alone does not qualify; never write both. More than one create-capable integration: ask, do not pick. A reachable tracker that cannot record a parent is `halt`, not `local`. Creating every child before the edges is not a build order.
- **Decision 4** — Decision 7 wins on inputs: no repo exploration; a prefactor piece only when Design already calls for a seam; expand–contract only for one mechanical change across many Scope rows; no final integrate ticket.
- **Decision 5** — Approve is refused for a cycle, a self-edge, a duplicate slug, an unknown slug, a piece with no acceptance criterion, or an unassigned Done-when bullet. Headless hosts halt with the stated sentence. No `--yes`.
- **Decision 6** — Each criterion cites its bullet or row. No code blocks. Every Done-when bullet is on exactly one piece or marked assembled-only. Unassigned bullets block approval.
- **Decision 7** — A missing reviews directory warns once and continues. Rows under `## Deferred — follow-up required` are counted and not filed (matches the spec-cycle preamble: the operator files those, not a lifecycle skill).
- **Decision 9** — No batching, fan-out cap, token budget, or per-tenant state. The brief only says `**Factor:** no`.
- **Decisions 10–12** — The three risk pins: which docs gain the stage, census integer 12 plus the `requires:` block, and create-only resume (slug match key, no edit/delete, no native-to-text rewrite in the same run).

Checked and not filed: the `requires:` vocabulary is in contract §3; frontmatter order matches `/spec-brief`; `issue-tracker?` matches local-mode degradation when the probe itself fails; the dot-prefixed temp and the `<TICKET-ID>.<rest>` archive name match `/spec-brief` and `/spec-close`; operative steps stay on capabilities (contract §4); there is no registry and no backwards-compat shim; the tree has 11 `skills/*/SKILL.md` directories, so 12 after this skill matches Decision 11. No `## Deferred — follow-up required` section, so no routing-row check. Wiki `architecture.md` is not in `projects/vigil-skills/` (state and filemap were read). Memory namespace `skills` returned access denied; the brief was used instead.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 3 | P4: 0

STATUS: GREEN
