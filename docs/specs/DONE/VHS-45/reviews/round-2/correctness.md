# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Native retry cannot finish a partial graph | CLOSED | spec § Decision 12 lines 149–153; § Phase 4 line 213; § Test plan line 253; § Done when line 273. Empty successful read is not a diff; missing children are created; missing native edges are written; extra, reversed, or dropped slug halts; a stopped run does not print `FILED`. |
| correctness | F-2 | Local files are specified both with and without Blocked by | CLOSED | spec § Decision 3 lines 44 and 50; § Phase 4 line 215. `Blocked by` is on `text` and `local`; `native` omits it. |
| correctness | F-3 | Two trackers ask a question the skill cannot accept | CLOSED | spec § Decision 3 lines 40–41; § Phase 3 line 190; § Phase 4 line 213; § Test plan line 252. Exact integration name before approval; Storage line carries it; a different integration at re-probe halts. |
| correctness | F-4 | blocked_by endpoints are not pinned | CLOSED | spec § Decision 3 lines 42–44; § Phase 4 line 215; § Test plan line 249. Edge on the dependent, type `blocked_by`, target = blocker id; read back; no inverse; full titles on `text` and `local`. |
| correctness | F-5 | project_id lookup is not the spec-brief lookup | CLOSED | spec § Decision 12 line 135. Path order matches `skills/spec-brief/SKILL.md:53` and `skills/spec-close/SKILL.md:31`. Field and missing-prefix halt match `skills/ship-spec/SKILL.md:41` (Phase 0 step 9), not spec-brief's namespace fallback. |
| correctness | F-6 | The test command does not cover every leave-alone path | CLOSED | spec § Test command line 267 names both historical notes. Both files exist. |
| correctness | F-7 | ticket not cached | REOPENED | `memory_search` on namespace `skills` still returns `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. Re-filed below at P3 per grounding step 3. Not a spec defect and not promoted. |
| edge-cases | F-1 | A failed edge write cannot be resumed | CLOSED | Same text as correctness F-1. Stop report lists `created` / `existing` / `missing` and `written` / `missing` / `mismatched` (line 153). |
| edge-cases | F-2 | Local re-runs halt even when Decision 12 says to skip | CLOSED | spec § Phase 4 lines 217–219 and § Decision 12 line 151. Siblings are read first; a match is skipped; a missing slug is written; a mismatch or dropped slug halts before any write; all-match is idempotent and does not halt. |
| edge-cases | F-3 | states.json handling cites a lookup that does not halt or return project_id | CLOSED | spec § Decision 12 line 135; § Phase 1 line 175. Checked before approval for tracker modes; blank `project_id`, invalid JSON, and parent-project mismatch halt; `local` does not read the file. |
| edge-cases | F-4 | Any probe failure becomes local, including a tracker that is up | CLOSED | spec § Decision 3 lines 50–53; § Test plan lines 250–251 and 255. `local` only when the named integration is confirmed not connected. Timeout, transport, non-success, error payload, unreadable schema, ACL deny, no parent, project mismatch, and unusable `states.json` are `halt`, including after approval. |
| edge-cases | F-5 | The approved mode does not record which tracker was chosen | CLOSED | spec § Decision 3 lines 38–41; § Phase 3 line 190; § Phase 4 line 213. |
| edge-cases | F-6 | blocked_by does not say which issue is the source | CLOSED | Same pin as correctness F-4, including the read-back that the blocker must not list the dependent under `blocked_by`. |
| edge-cases | F-7 | Existing-child match is not scoped, paged, or single-valued | CLOSED | spec § Decision 12 lines 137–144; § Decision 5 line 75. Children of the parent only, paginate until a short page or done, zero/one/two rules, re-list before each create, absent body or relation list is cannot-read, slug grammar refuses option 1. |
| edge-cases | F-8 | Approve is not a single defined reply | CLOSED | spec § Decision 5 lines 73–75; § Phase 3 line 209; § Test plan line 247. |
| edge-cases | F-9 | Phase 4 can file a draft the operator did not approve | CLOSED | spec § Phase 3 line 209; § Phase 4 line 213. Printed block is frozen; spec contents changed since the prompt halts; Decision 5 gate re-runs on the frozen draft. |
| edge-cases | F-10 | Local rename needs shell, which the skill declares absent | CLOSED | spec § Decision 11 line 127; § Phase 4 line 219. `shell` stays absent; rename is filesystem `write`; if the host cannot rename, `local` is `halt` and the target is not opened. |
| edge-cases | F-11 | Phase 0 deletes temps that Phase 4 does not name | CLOSED | spec § Phase 0 line 171; § Phase 4 line 219. One temp path; Phase 0 prints and does not delete; temp removed only after that slug's rename succeeds. |
| edge-cases | F-12 | Non-bullet Done-when text and uncited Test plan rows never block approval | CLOSED | spec § Decision 6 lines 81–82; § Decision 7 line 89; § Decision 5 line 75; § Phase 2 line 179. One real level-2 heading outside fences; list items and table rows are the units; Done when with neither halts; an unassigned Test plan row blocks option 1. |
| edge-cases | F-13 | project_root is cwd, and the spec path is only a filename pattern | NEW | Path shape and end-anchored ticket regex are in § Decision 7 lines 85–86. The walk now excludes cwd, which breaks invocation from the repo root. Filed as F-1. |
| edge-cases | F-14 | Ticket bodies and local files have no size bound or format version | DEFERRED | spec § Deferred (P2+) lines 289–291 declines the 32 KiB cap and format token, with a Decision 9 rationale. P2 parking section, not a `D-<n>` row. Not re-filed. |
| edge-cases | F-15 | Deferred-row count is undefined | CLOSED | spec § Decision 7 line 91. Count only `### D-<n>:` headings outside fences; zero-heading text is specified. |
| edge-cases | F-16 | Plane ticket text was not readable | REOPENED | Same denied lookup as correctness F-7. Not a spec defect. Covered by F-4 below, not promoted. |
| conventions | F-1 | states.json is cited as /spec-brief's lookup, and it is read after approval | CLOSED | Same edit as edge-cases F-3. |
| conventions | F-2 | Parent resolution forbids shared memory, and the AGENTS.md edit leaves the opposite rule in place | CLOSED | spec § Decision 10 line 105. Memory-read sentence narrowed to `/spec-brief`, `/spec-cycle`, and `/spec-close`'s PR lookup; `/spec-tickets` resolves the parent on the tracker and does not consult shared memory. |
| conventions | F-3 | Piece labels P1, P2 reuse the review severity scale | CLOSED | spec § Phase 2 line 181 forbids `P1`, `P2`, and any other severity token. |
| conventions | F-4 | The requires: block is exactly … is not what the test command checks | CLOSED | spec § Test command line 266 asserts keys `filesystem` and `services`, `issue-tracker?`, and the absence of `shell`, `network`, `subagents`, and `shared-memory`. `lint.lint_path` findings are `(severity, rule, file, line, message)` (`lint.py:50–51`, `:243–256`), so `x[0]` is the right field. |
| conventions | F-5 | Decision 4's sizing sentence is the reference skill's wording | CLOSED | spec § Decision 4 line 61 uses "verifiable alone" and "one context window", and lists the forbid-phrases. |
| conventions | F-6 | Frontier is already the interview term in the workflow reference | CLOSED | spec § Phase 3 line 198 says "not the grilling frontier". § Decision 10 line 107 says "unblocked pieces" and forbids "frontier" for that set. `docs/spec-workflow-reference.md:29` still defines frontier as the interview term. |
| conventions | F-7 | Drift-check — spec-level additions with rationale | CLOSED | No defect. Brief Risks 1–3 still authorize Decisions 10–12. |

Manifest claims for the fourteen P0/P1 lines were checked against the current spec. Each claimed edit is present. No commit in the last 7 days touches `AGENTS.md`, `README.md`, `docs/spec-workflow-reference.md`, or `tests/test_lint.py` (newest is `d4db373`, 2026-09-08). `skills/*/SKILL.md` is 11 files, so the census of 12 after this skill matches `tests/test_lint.py:52` (`len(skills) == 8` today). There is no `## Deferred — follow-up required` section. `scale_lens` is off; no scalability report was read.

## Findings

### F-1: Repo-root walk excludes cwd, so the usual invocation never resolves
**Severity:** P0
**Where:** spec.md:85 | spec § Decision 7
**Claim:** "The repo root is the nearest ancestor of cwd that contains `AGENTS.md` or `CLAUDE.md`, not cwd itself." Phase 0 (line 169) resolves the root only by that rule, and the only accepted spec path is `<root>/docs/specs/TODO/<TICKET-ID>.spec.md`.
**Why this is wrong:** "Ancestor" does not include cwd, and the sentence repeats the exclusion. Sibling skills treat the root as cwd when cwd is the directory that contains the marker: `skills/spec-cycle/SKILL.md:50` (`project_root` is the cwd), `skills/spec-brief/SKILL.md:34` (`project_root` = cwd), `skills/spec-close/SKILL.md:26` (the directory containing `CLAUDE.md`). This repo's root is that directory: it contains `AGENTS.md` and a gitignored `CLAUDE.md`. Its parent `C:\Users\zioni\Documents\Vigil-Harbor` has neither file, and `C:\Users\zioni\Documents` has neither. Invoked from the repo root — the same cwd the other lifecycle skills use — the walk skips the only directory that qualifies and then fails, or, if some further ancestor ever contains one of those names, binds the wrong root. Either way `<root>/docs/specs/TODO/<TICKET-ID>.spec.md` is not the spec the operator passed, Phase 0 halts, and nothing is drafted or filed. That contradicts Done when line 272 (a skill that decomposes an approved spec). This is the residue of edge-cases F-13: the TODO-path check and the end-anchored id regex are in place; the walk overshoots them.
**Suggested fix:** Start at cwd. If cwd contains `AGENTS.md` or `CLAUDE.md`, that directory is the root. Otherwise walk to the nearest ancestor that contains one. Delete "not cwd itself". Keep the path rule: only `<root>/docs/specs/TODO/<TICKET-ID>.spec.md`, stem matched by `^[A-Z][A-Z0-9]*-[0-9]+$` in full, anything else including `..` halts.

### F-2: Resume parses a work-item title Phase 4 never writes
**Severity:** P1
**Where:** spec.md:137 | spec § Decision 12; spec § Phase 4 line 215; spec § Phase 3 line 194
**Claim:** "The slug is the single token between `<PARENT-ID> ` and the colon, and it must match the Decision 5 grammar." Zero matches create (line 139). `Blocked by` entries "are the full title `<PARENT-ID> <slug>: <short title>`" (line 44). Phase 4's create body is Parent, Spec, Delivers, Acceptance criteria, Assembly, and on `text`/`local` Blocked by. It never sets the work item's title. The approval block names the piece `<slug> — <title>` (em dash, no parent id, no colon).
**Why this is wrong:** The first run can still file: there are no children, create returns ids, and native edges use those ids. The second run's identity check looks for `<PARENT-ID> <slug>:` in the title. Nothing in Phase 4 stored that string, so the parse yields zero matches, and line 139 creates another child per slug. A third run then sees two matches and stops (line 141). Create-only (line 133) cannot delete the duplicates. plane-proxy's create schema has a single `name` string (`plane-proxy/src/tools.ts:234`) plus `parent` (`:242`) and no separate title, so the implementer has to choose one name and the spec does not say which. Using the approval line as `name` fails the colon parse. `<short title>` is also never defined as the approval block's `<title>`.
**Suggested fix:** In Phase 4, set the work item's title — the tracker's name field — to exactly `<PARENT-ID> <slug>: <short title>`, and define `<short title>` as the approval block's `<title>`. State that the approval line's `—` is display only and is not stored. Use that same string as each local file's title line. Decision 12 parses only that stored title.

### F-3: An incomplete local sibling has no outcome, and the temp rules disagree
**Severity:** P2
**Where:** spec.md:217 | spec § Phase 4 — File
**Claim:** "A file that lacks `local-only` or a required heading is incomplete, not a match. A mismatch or a dropped slug halts before any write." Later: "Remove the temp only after that slug's rename succeeds. Do not delete a temp whose target already exists."
**Why this is wrong:** "Required heading" is not defined. Incomplete is neither a mismatch, nor a dropped slug, nor a match, nor a missing slug (the file is already there). The four outcomes that follow do not cover it, so a second run can rename over that file — the same paragraph says "renamed over the target" — or sit with no halt and no `FILED`. The cleanup pair also disagrees once a rename has succeeded: success means the target exists, and the next sentence then forbids deleting the temp. `skills/spec-brief/SKILL.md:130` already notes that a leftover `.<TICKET-ID>.….tmp` is not gitignored.
**Suggested fix:** Name the required headings as the title line plus Parent, Spec, Delivers, Acceptance criteria, Assembly, Blocked by, and the `local-only` line. An incomplete file is a mismatch: halt before any write, do not rename onto it, and do not delete its temp. After a rename onto a path that did not exist before that rename, remove the temp if the host left it behind.

### F-4: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec implements Plane ticket VHS-45. The brief says its Done when block is transcribed from the ticket.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45`, `source_system: plane`, returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. No ticket body was available. Review used the brief only. If the ticket's acceptance criteria differ from the brief, that conflict was not checked.
**Suggested fix:** Re-cache the work item into a namespace this reviewer can read, or paste the ticket acceptance criteria into the brief if they are not already the transcribed Done when list.

## Summary
P0: 1 | P1: 1 | P2: 1 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=1 P2=1 P3=1 P4=0
