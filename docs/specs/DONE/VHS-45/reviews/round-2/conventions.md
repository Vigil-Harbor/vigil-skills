# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Native retry cannot finish a partial graph | CLOSED | spec § Decision 12 lines 149–153; § Phase 4 line 213; § Test plan line 253; § Done when line 274 |
| correctness | F-2 | Local files are specified both with and without Blocked by | CLOSED | spec § Decision 3 line 44; § Phase 4 line 215 (`text` and `local` both get Blocked by; `native` omits it) |
| correctness | F-3 | Two trackers ask a question the skill cannot accept | CLOSED | spec § Decision 3 line 40; § Phase 3 line 190; § Phase 4 line 213; § Test plan line 252 |
| correctness | F-4 | blocked_by endpoints are not pinned | CLOSED | spec § Decision 3 lines 42–44; § Phase 4 line 215; § Test plan line 249 |
| correctness | F-5 | project_id lookup is not the spec-brief lookup | CLOSED | spec § Decision 12 line 135 cites spec-brief/spec-close for the path and ship-spec Phase 0 step 9 for `project_id` plus halt |
| correctness | F-6 | The test command does not cover every leave-alone path | CLOSED | spec § Test command line 267 names both historical notes |
| correctness | F-7 | ticket not cached | CLOSED | `memory_search` on namespace `skills` is still access denied; the brief's Done when is the transcribed ticket list. Not a spec defect; not re-filed |
| edge-cases | F-1 | A failed edge write cannot be resumed | CLOSED | Same text as correctness F-1: missing native edges are written; extra or reversed edges halt; stop report does not print `FILED` |
| edge-cases | F-2 | Local re-runs halt even when Decision 12 says to skip | CLOSED | spec § Phase 4 line 217: read siblings first; skip matches; write missing slugs; mismatch halts before any write; all-match is idempotent |
| edge-cases | F-3 | states.json handling cites a lookup that does not halt or return project_id | CLOSED | spec § Decision 12 line 135; § Phase 1 line 175 runs the check before approval; `local` does not read the file |
| edge-cases | F-4 | Any probe failure becomes local, including a tracker that is up | CLOSED | spec § Decision 3 lines 50–53; § Test plan lines 249–251 |
| edge-cases | F-5 | The approved mode does not record which tracker was chosen | CLOSED | spec § Decision 3 line 40; Storage line carries the name; § Phase 4 line 213 halts if the integration changed |
| edge-cases | F-6 | blocked_by does not say which issue is the source | CLOSED | spec § Decision 3 line 42: edge on the dependent, target = blocker id, read back, do not add the inverse |
| edge-cases | F-7 | Existing-child match is not scoped, paged, or single-valued | CLOSED | spec § Decision 12 lines 137–144; slug grammar in § Decision 5 line 75 |
| edge-cases | F-8 | Approve is not a single defined reply | CLOSED | spec § Decision 5 line 73: exact `1` files, exact `3` aborts, any other non-empty reply revises |
| edge-cases | F-9 | Phase 4 can file a draft the operator did not approve | CLOSED | spec § Phase 3 line 209; § Phase 4 line 213 freezes the printed block and re-runs the Decision 5 gate |
| edge-cases | F-10 | Local rename needs shell, which the skill declares absent | CLOSED | spec § Decision 11 line 127; § Phase 4 line 219: rename is filesystem `write`; failure is `halt`; never write the target in place |
| edge-cases | F-11 | Phase 0 deletes temps that Phase 4 does not name | CLOSED | spec § Phase 0 line 171 prints the one temp path and does not delete; § Phase 4 line 219 removes a temp only after that slug's rename |
| edge-cases | F-12 | Non-bullet Done-when text and uncited Test plan rows never block approval | CLOSED | spec § Decision 6 line 81; § Decision 7 line 89 |
| edge-cases | F-13 | project_root is cwd, and the spec path is only a filename pattern | CLOSED | spec § Decision 7 line 85: walk to `AGENTS.md` or `CLAUDE.md`; TODO path; end-anchored ticket id |
| edge-cases | F-14 | Ticket bodies and local files have no size bound or format version | DEFERRED | spec § Deferred (P2+) line 291 declines the fold with rationale. That is the spec-cycle P2 carry section, not a `## Deferred — follow-up required` row. Not re-filed |
| edge-cases | F-15 | Deferred-row count is undefined | CLOSED | spec § Decision 7 line 91 counts only `### D-<n>:` headings outside fences |
| edge-cases | F-16 | Plane ticket text was not readable | CLOSED | Same access denial as correctness F-7. The finding asked for no spec edit. Not re-filed |
| conventions | F-1 | states.json cited as spec-brief's lookup, and read after approval | CLOSED | spec § Decision 12 line 135; § Phase 1 line 175 |
| conventions | F-2 | Parent resolution forbids shared memory, and the AGENTS.md edit leaves the opposite rule | CLOSED | spec § Decision 10 line 105 narrows the memory-read sentence and states this skill does not consult shared memory |
| conventions | F-3 | Piece labels P1, P2 reuse the review severity scale | CLOSED | spec § Phase 2 line 181 forbids severity tokens; pieces are slugs |
| conventions | F-4 | The requires block is exactly … is not what the test command checks | CLOSED | spec § Test command line 266 asserts the key set, `issue-tracker?`, and the four absent keys |
| conventions | F-5 | Decision 4's sizing sentence is the reference skill's wording | CLOSED | spec § Decision 4 lines 61–67 uses the brief's wording and names the forbid-list |
| conventions | F-6 | Frontier is already the interview term in the workflow reference | CLOSED | spec § Phase 3 line 198 says "not the grilling frontier"; § Decision 10 line 107 says "unblocked pieces" |
| conventions | F-7 | Drift-check — spec-level additions with rationale | CLOSED | Round-1 list stood. Additions since that list are this round's F-4 |

No `## Deferred — follow-up required` section, so no routing-row check. `## Deferred (P2+)` is the existing P2 carry heading, not a second copy of the routing section. Wiki `projects/vigil-skills/` has `state.md` and `filemap.md` and no `architecture.md`.

## Findings

### F-1: The new README Requirements bullet is unscoped
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 10, line 106
**Convention violated:** `README.md` § Requirements scopes every service bullet to the skills it covers. An unscoped `gh` / tracker sentence would contradict the bullets already there and `AGENTS.md` § External dependencies.
**Evidence:** `README.md` line 63: "For `/spec-cycle`, `/ship-spec`, and `/spec-close`: a Plane.so workspace with the plane-proxy MCP server, and `gh` CLI authenticated." Line 65 scopes `/review-pr` the same way. `AGENTS.md` line 121: "`gh` CLI — PR creation, CodeRabbit thread management. Must be authenticated." Decision 10 says only "Add a Requirements bullet: an operator is required at approval; the tracker is optional per Decision 3; `gh` is not required." Decision 10's AGENTS.md edit does not mention `gh`, so the two tracked files would disagree if the new bullet is copied as written.
**Suggested fix:** Write the bullet in the existing shape: `For /spec-tickets: an operator is required at approval; the tracker is optional per Decision 3 (local files only when it is confirmed not connected); gh is not required.` Say it does not change the `/spec-cycle`, `/ship-spec`, `/spec-close`, or `/review-pr` bullets.

### F-2: The string Phase 4 writes is not the string Decision 12 matches
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Phase 4 — File, line 215; spec § Phase 3 — Approval, lines 194–197; spec § Decision 3, line 44; spec § Decision 12, line 137
**Convention violated:** One name for one record. The approval display, the tracker title, and the resume key are three different shapes, and only one of them is defined.
**Evidence:** Decision 3 defines the full title as `<PARENT-ID> <slug>: <short title>` and Decision 12 parses the slug as the single token between `<PARENT-ID> ` and the colon. Phase 3 prints `- <slug> — <title>` (em dash, no parent id). Phase 4's body list is Parent, Spec, Delivers, Acceptance criteria, Assembly, and Blocked by on `text` and `local`. It says `local-only` goes "under the title" and never says to set the work-item title or the local H1 to the Decision 3 string. A body written from the Phase 4 list, with the approval line as the name, will not match on the next run.
**Suggested fix:** In Phase 4, state that the tracker work-item title and the local file's H1 are exactly `<PARENT-ID> <slug>: <short title>`, the same string Blocked by lines and the Decision 12 parse use. Say the approval block's `<slug> — <title>` is display only.

### F-3: `issue-tracker?` halt overrides the portability contract without naming it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3, lines 50–53; spec § Decision 11, lines 119–127
**Convention violated:** `docs/portability-contract.md` §3 availability and point-of-use rules. Wiki decision `2026-06-18-vhs-20-hermes-preflight-advisory` restates the same optional-service rule. Drift is explicit in behavior and silent about the decision it narrows.
**Evidence:** The contract says a service is available only when a liveness probe succeeds, and "an ACL-denied or misconfigured provider counts as unavailable" (`docs/portability-contract.md` line 76). For an optional service, "absence never blocks" and point-of-use failure is "warn-and-proceed" (line 78). Decision 11 declares `services: [issue-tracker?]`. Decision 3 then puts ACL denial, a probe that does not return, and a failed write in `halt`, not `local`, and says "It is not warn-and-proceed." That sentence does not name §3, so a later edit can "correct" the halt back to the contract's degrade path and file a second graph.
**Suggested fix:** In Decision 3, after the halt list, name the narrowing: `?` means only confirmed not-connected may take `local`. An ACL-denied, misconfigured, or failing tracker is unavailable under portability-contract §3 and would warn-and-proceed; this skill halts instead, because a local file beside a live tracker is a second graph. Do not change the `requires:` block.

### F-4: Drift-check — round-2 additions with rationale
**Severity:** P3
**Where:** spec § Decisions 3, 4, 5, 6, 7, 10, 11, 12; spec § Phase 3 — Approval; spec § Phase 4 — File
**Convention violated:** None. Class (c). The brief's Decisions 1–8, `## Scale`, and Risks 1–3 still authorize the pins. Each item below is a review fix with the reason written next to it. No class (d) silent addition.
**Evidence:** Brief Decisions 1–8 and Risks 1–3. Round-1 conventions F-7 already listed the earlier pins. These are the commitments added since that list.
**Suggested fix:** No edit required. The new drift-check list is:

- **Decision 3** — The edge is created on the dependent, type `blocked_by`, target = the blocker id, then read back. Text and local use the full title. The chosen integration name is part of the approved draft. `local` only when that integration is confirmed not connected. Probe failures, ACL denial, and write failures halt. A tracker mode halts if a `<PARENT-ID>.ticket-*.md` file already exists.
- **Decision 4** — Sizing words are the brief's. The skill must not reuse the named upstream phrases.
- **Decision 5** — File only on exact `1` when option 1 was printed. Exact `3` aborts. Any other non-empty reply revises and does not change storage. Slug grammar is `^[a-z0-9]+(-[a-z0-9]+)*$`, at most 40 characters.
- **Decision 6** — List items and table rows are the assignable units. Done when with neither halts. An unassigned Test plan row blocks option 1.
- **Decision 7** — Repo root is the nearest ancestor with `AGENTS.md` or `CLAUDE.md`. The ticket id is the whole stem. Headings count only outside fences. Deferred rows are `### D-<n>:` headings.
- **Decision 10** — The External dependencies sentence keeps memory reads for `/spec-brief`, `/spec-cycle`, and `/spec-close`'s PR lookup. This skill resolves the parent on the tracker. The workflow summary says "unblocked pieces."
- **Decisions 11–12** — Rename is filesystem `write`; if the host cannot rename, `local` halts and the target is not opened. A successful empty relation read means nothing recorded yet. Missing native edges are created. A text or local body is not patched. `states.json` is read before approval on tracker modes; the parent's project id must match. Children are listed with pagination; two matches stop; the slug is re-listed immediately before each create.
- **Phases 3–4** — The printed block is what approval freezes. A spec-file change since the prompt halts.

### F-5: The local temp copies spec-brief's path and drops its commit warning
**Severity:** P3
**Where:** spec § Phase 0 — Preflight, line 171; spec § Phase 4 — File, line 219
**Convention violated:** `skills/spec-brief/SKILL.md` line 130: the dot-prefixed temp is outside `/spec-close`'s companion glob, and `.gitignore` does not ignore `.*.tmp`, so a stray temp must not be committed. That is a prose rule. Spec-brief removes the stale temp on the next run. This spec prints it and, once the target exists, never deletes it.
**Evidence:** Phase 0 names `docs/specs/TODO/.<PARENT-ID>.ticket-<slug>.md.tmp`, prints existing temps, and does not delete them. Phase 4 removes a temp only after that slug's rename succeeds, and does not delete a temp whose target already exists. A failed rename, or a temp left beside a matching target, stays in a tracked directory with no "do not commit" line.
**Suggested fix:** In Phase 0, copy spec-brief's one sentence: these temps are not gitignored and must not be committed; printing them is the warning. Keep the no-delete rule from the prior round.

### F-6: Two Storage-line grammars
**Severity:** P4
**Where:** spec § Decision 3, line 40; spec § Phase 3 — Approval, line 190
**Convention violated:** None load-bearing. The same line is specified twice.
**Evidence:** Decision 3: `Storage: <mode> via <name>` and "`local` has no name." The Phase 3 fence: `Storage: <native|text|local|halt> via <integration name, or none> (<reason when halt>)`. `local` is either bare or `via none`. `halt`'s reason exists only in the fence.
**Suggested fix:** Put one grammar in Decision 3 and copy it into the fence. `native` and `text` use `via <name>`. `local` has no `via`. `halt` is `Storage: halt via <name or none> (<reason>)`.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 2 | P4: 1

STATUS: GREEN
