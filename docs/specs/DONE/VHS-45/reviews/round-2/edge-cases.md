# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Native retry cannot finish a partial graph | CLOSED | spec § Decision 12, lines 149–153: a successful empty read is not a difference; missing slugs are created, then missing native edges; extra, reversed, or dropped slug halts; a stopped run does not print `FILED`. Phase 4 line 213 and Test plan line 253 restate it. |
| correctness | F-2 | Local files are specified both with and without Blocked by | CLOSED | spec § Phase 4 — File, line 215: `Blocked by` is on `text` and `local`; `native` omits it. |
| correctness | F-3 | Two trackers ask a question the skill cannot accept | CLOSED | spec § Decision 3, lines 38–40: exact integration name before approval; `Storage: <mode> via <name>`; a different integration at re-probe halts. |
| correctness | F-4 | blocked_by endpoints are not pinned | CLOSED | spec § Decision 3, lines 42–44: edge on the dependent, type `blocked_by`, target = blocker id, read back, inverse not added; text and local use the full title. |
| correctness | F-5 | project_id lookup is not the spec-brief lookup | CLOSED | spec § Decision 12, line 135: config-dir order cited from `/spec-brief` and `/spec-close`; `project_id` and halt-on-unknown-prefix cited from `/ship-spec` Phase 0 step 9. Phase 1 line 175 runs that check before approval. Those skills do use that split (`skills/spec-brief/SKILL.md` step 3, `skills/spec-close/SKILL.md` step 4, `skills/ship-spec/SKILL.md` step 9). |
| correctness | F-6 | The test command does not cover every leave-alone path | CLOSED | spec § Test command, line 267 includes both historical notes. `tests/` has only the four modules named besides `tests/test_lint.py`. |
| correctness | F-7 | ticket not cached | CLOSED | Not a spec defect (round-1 fix was none). `memory_search` on namespace `skills` still returns access denied; re-recorded as F-14. |
| conventions | F-1 | states.json cited as spec-brief and read after approval | CLOSED | Same as correctness F-5: Phase 1 line 175, Decision 12 line 135. |
| conventions | F-2 | Parent resolution forbids shared memory; AGENTS.md edit leaves the opposite rule | CLOSED | spec § Decision 10, line 105: narrow the memory-read sentence to `/spec-brief`, `/spec-cycle`, and `/spec-close`'s PR lookup, and state that `/spec-tickets` resolves the parent on the tracker and does not consult shared memory. |
| conventions | F-3 | Piece labels P1, P2 reuse the review severity scale | CLOSED | spec § Phase 2 — Draft, line 181: do not label pieces with severity tokens. |
| conventions | F-4 | requires block is not what the test command checks | CLOSED | spec § Test command, line 266 asserts the key set `filesystem` and `services`, `issue-tracker?`, and the absence of `shell`, `network`, `subagents`, and `shared-memory`. |
| conventions | F-5 | Decision 4's sizing sentence is the reference skill's wording | CLOSED | spec § Decision 4, lines 61–62 uses the brief's wording and lists the forbidden phrases. |
| conventions | F-6 | Frontier is already the interview term | CLOSED | spec § Phase 3 — Approval, line 198 says "Unblocked" and "not the grilling frontier". Decision 10 line 107 forbids "frontier" in the workflow-reference summary. |
| conventions | F-7 | Drift-check — spec-level additions with rationale | CLOSED | No defect. Round-1 asked for no edit. |
| edge-cases | F-1 | A failed edge write cannot be resumed | CLOSED | Same text as correctness F-1. Stop report is line 153. |
| edge-cases | F-2 | Local re-runs halt even when Decision 12 says to skip | CLOSED | spec § Phase 4 — File, line 217 and Decision 12 line 151: read existing files, skip a match, write missing slugs, halt on mismatch before any write, all-match is idempotent. A stale body that is not an edge mismatch is a new case, F-6. |
| edge-cases | F-3 | states.json handling cites a lookup that does not halt or return project_id | CLOSED | Decision 12 line 135: missing, unreadable, invalid JSON, unknown prefix, blank `project_id`, and a parent project mismatch set `halt` before approval. `local` does not read the file. |
| edge-cases | F-4 | Any probe failure becomes local, including a tracker that is up | PARTIAL | The halt list at line 53 does name "does not return", transport, non-success, error payload, unreadable schema, ACL denial, no parent, project mismatch, and unusable `states.json`. Line 40 still sets `local` when zero integrations "can create", which is the same input. Residual filed as F-1. |
| edge-cases | F-5 | The approved mode does not record which tracker was chosen | CLOSED | Decision 3 lines 38–40. Test plan line 252. |
| edge-cases | F-6 | blocked_by does not say which issue is the source | CLOSED | Decision 3 line 42. Test plan line 249. |
| edge-cases | F-7 | Existing-child match is not scoped, paged, or single-valued | PARTIAL | Lines 137–142 list only the parent's children, page until a short page, zero/one/two, re-list before each create, and refuse a create with no id, an error payload, or a parent other than the spec's ticket. A create result that omits `parent` is not covered, and the new id is not confirmed by a post-create list. Residual filed as F-5. |
| edge-cases | F-8 | Approve is not a single defined reply | CLOSED | Decision 5 lines 73–74: file only on exact `1` when option 1 was printed; exact `3` aborts; any other non-empty reply revises and does not change storage; empty, EOF, timeout, or cannot-wait is the headless halt. |
| edge-cases | F-9 | Phase 4 can file a draft the operator did not approve | CLOSED | Phase 3 line 209 freezes the printed block. Phase 4 line 213 halts if the spec file changed, refuses a redraft, and re-runs the Decision 5 gate on the frozen draft. |
| edge-cases | F-10 | Local rename needs shell, which the skill declares absent | CLOSED | Decision 11 line 127: rename is filesystem `write`. Phase 4 line 219: if the host cannot rename onto the target, `halt` and do not open the target; never write the target in place. |
| edge-cases | F-11 | Phase 0 deletes temps that Phase 4 does not name | CLOSED | Phase 0 line 171 prints `docs/specs/TODO/.<PARENT-ID>.ticket-<slug>.md.tmp` and does not delete. Phase 4 line 219 removes a temp only after that slug's rename and does not delete a temp whose target already exists. |
| edge-cases | F-12 | Non-bullet Done-when text and uncited Test plan rows never block approval | CLOSED | Decision 7 line 89: one level-2 heading per required name, outside a fence; a second heading halts. Decision 6 lines 81–82: list items and table rows are the units; Done when with neither halts; anything unassigned blocks option 1. |
| edge-cases | F-13 | project_root is cwd, and the spec path is only a filename pattern | PARTIAL | Line 85 anchors the ticket id and accepts only `<root>/docs/specs/TODO/<TICKET-ID>.spec.md`. The same sentence excludes cwd from the root walk. Residual filed as F-2. |
| edge-cases | F-14 | Ticket bodies and local files have no size bound or format version | DEFERRED | spec § Deferred (P2+), line 291 declines a 32 KiB cap and a format token. Not a `D-<n>` row. A success-with-truncation hole that the note does not cover is F-12. |
| edge-cases | F-15 | Deferred-row count is undefined | CLOSED | Decision 7 line 91: count only `### D-<n>:` headings outside fences, and print the zero-heading sentence when the section exists and the count is 0. |
| edge-cases | F-16 | Plane ticket text was not readable | CLOSED | Not a spec defect. Lookup is still denied; re-recorded as F-14. |

No `## Deferred — follow-up required` section is present, so there is no routing-row check. `## Deferred (P2+)` is a different heading.

## Findings

### F-1: Zero "can create" still selects local, including a tracker that is up
**Severity:** P0
**Where:** spec.md:40 | spec § Decision 3
**Edge case:** The only integration is connected but times out, returns an ACL denial, or has a readable schema with no work-item create. Also a connected integration that can create issues but cannot set a parent.
**What happens:** Line 40 sets `local` as soon as the count of integrations that "can create work items" is zero, and then writes `docs/specs/TODO/<PARENT-ID>.ticket-*.md`. Line 50 says the only `local` trigger is a named integration confirmed not connected. Line 53 says a probe that does not return, an ACL denial, and no parent-link capability are `halt` and must not switch mode. Line 249 and the Done when bullet at line 273 repeat "not connected only". The same input is both `local` and `halt`. The local reading writes a second graph beside a live tracker. A later native or text run then halts on those files (line 54) and cannot finish the real children.
**Why the spec misses it:** The round-1 halt list was added, and the opening count was left in place above it. Nothing says the count is skipped when the probe errors or the schema is readable but has no create.
**Suggested fix:** Delete the "zero can create → local" sentence. `local` only when every probed integration returns a positive not-connected result and none of the line 53 conditions fired. Timeout, transport error, non-success, error payload, unreadable schema, ACL denial, no create capability, and no parent-link are `halt` before that count. Say that an integration that did not answer is not "zero can create".

### F-2: The repo-root walk excludes the directory the operator is in
**Severity:** P1
**Where:** spec.md:85 | spec § Decision 7
**Edge case:** The skill is invoked from the repo root, which is the usual cwd. That directory contains `AGENTS.md` and, on this machine, `CLAUDE.md`. The invocation examples in `/ship-spec` are relative paths from that directory.
**What happens:** "The nearest ancestor of cwd … not cwd itself" skips the directory that holds the markers. The parent of `vigil-skills` does not show `AGENTS.md` or `CLAUDE.md` in its listing, so the walk finds no root and Phase 0 halts with the usage line. No tickets are filed. If some higher directory did contain one of those files, local files and the accepted spec path would bind to that other tree.
**Why the spec misses it:** `/spec-cycle` sets `project_root` to cwd when cwd contains `CLAUDE.md` (`skills/spec-cycle/SKILL.md` Phase 0 step 1). `/spec-brief` does the same. This sentence excludes that directory. A backslash or absolute Windows path is also "anything else" and halts, because normalization is not specified.
**Suggested fix:** Walk cwd and then its ancestors, and take the nearest directory that contains `AGENTS.md` or `CLAUDE.md`, including cwd. Normalize separators and accept that path when it canonicalizes to `<root>/docs/specs/TODO/<TICKET-ID>.spec.md`. Keep the halt for `..` and for a stem that is not the whole ticket id.

### F-3: Resume matches a title the create never sets
**Severity:** P1
**Where:** spec.md:137 | spec § Decision 12; spec § Phase 4 — File, line 215
**Edge case:** The work-item create stores the short title, a tracker-rewritten title, or no title in the shape `<PARENT-ID> <slug>: <short title>`. The same gap exists for the local file's heading: the filename contains the slug, but the matcher does not.
**What happens:** Line 137 parses the slug as the single token between `<PARENT-ID> ` and the colon. Nothing in Phase 4 sets the work item's title, or the local H1, to that string. The next run sees zero matches, creates another child, and then line 141 stops on two matches. Create-only (line 133) cannot delete the duplicate. Edges can attach to either id. `FILED` never prints, and the extra ticket stays.
**Why the spec misses it:** The full-title form is specified for `Blocked by` lines (line 44) and for the read-side match, not for the create or the local heading. "local-only under the title" assumes a title that is never defined.
**Suggested fix:** On create, set the title to exactly `<PARENT-ID> <slug>: <short title>`, and use that as the local H1 with `local-only` on the next line. After create, list the parent's children again and require exactly one title that parses to that slug and whose id is the id just returned. If the tracker rewrote the title, or the count is not one, halt with no further creates and do not treat the rewritten row as a different slug.

### F-4: An omitted relation field never becomes the empty set
**Severity:** P1
**Where:** spec.md:144 | spec § Decision 12
**Edge case:** The relation read returns a successful work-item body with no `blocked_by` field, or a body whose list is under some other key. This is the normal "no edges yet" payload if the integration omits an empty list. It is also every read that happens after the children exist and before the first edge write.
**What happens:** Line 144 says an absent relation list is "cannot read" and halts before any further create. Line 149 says only an empty set from a successful read means nothing is recorded yet. The spec never says which payload is which, so a missing key follows the absent-list sentence. Native resume halts before writing edges. The next run reads the same shape and halts again. Pieces with no blockers deadlock the same way, because there is no edge write that would add the field. `FILED` is never printed. The narrower phrase "before any further create" also leaves an edge-phase read free to continue after creates are finished, which is the opposite stop from line 42.
**Why the spec misses it:** The empty-set rule and the cannot-read rule meet at an undefined JSON shape. No example marks `blocked_by: []` on a 2xx work-item body as the successful empty read.
**Suggested fix:** A 2xx body that is the work item and whose `blocked_by` field is a list is a successful read; `[]` means nothing recorded yet. Non-success, an error payload, a body that is not the work item, or a relation field that is not a list is cannot-read and stops creates and edge writes. State that a successful work-item body that omits the field is the empty set, not cannot-read, so a missing key cannot block the first edge write. Do not treat a partial page as the whole set (see F-10).

### F-5: A create result with no parent field is kept as the child
**Severity:** P1
**Where:** spec.md:141 | spec § Decision 12
**Edge case:** The create call returns a success body with an id and no parent field, and the tracker did not attach the spec's ticket as parent. Also a success body whose parent field is present but null.
**What happens:** Line 141 stops for no id, an error payload, or a parent other than the spec's ticket. An omitted or null parent is none of those, so the id is kept. The next list of the parent's children does not show it. Zero matches creates a second child. The first id can still receive `blocked_by` edges. Create-only cannot delete the orphan. Two later matches then stop the run permanently.
**Why the spec misses it:** Round 1 asked to reject a dropped parent. The new sentence only rejects a parent that is present and different. There is no list-after-create check that the id is among the parent's children.
**Suggested fix:** If the create body omits parent, or parent is null, do not keep that id until a fresh child list shows exactly one row for the slug and that row's id equals the created id. If the list does not show it, halt with no further creates and do not write edges to the returned id. Keep the existing stop for a parent that is present and different.

### F-6: Equal edges print FILED while the approved body was not written
**Severity:** P1
**Where:** spec.md:151 | spec § Decision 12; spec § Phase 4 — File, lines 213–222
**Edge case:** A second approval changes Delivers, acceptance lines, or anchors and keeps the same slugs and the same blockers. The existing text, local, or native body still has the previous wording. The `Blocked by` set, or the native id set, is unchanged.
**What happens:** Line 147 defines the recorded set as titles or blocker ids only. Line 151 skips a child whose recorded set equals the approved set and tells the run not to halt. Line 222 prints `FILED` when every child exists and every edge is recorded. The skill does not edit bodies (line 133), so the new criteria are never stored, and the operator is told the approved draft was filed. Parallel implementers then follow the stale acceptance text.
**Why the spec misses it:** Create-only forbids the repair, and the skip rule treats "edges match" as "the frozen draft is already stored". Phase 4 says the frozen criteria are the only input, but it never compares them to the stored body.
**Suggested fix:** A skip is allowed only when the stored body matches the frozen body section for section (Parent, Spec anchors, Delivers, Acceptance, Assembly, and `Blocked by` on text and local, plus `local-only` on local). Any other difference is a mismatch: halt before any write, list the slug as `mismatched`, and do not print the idempotent result or `FILED`. Name those headings as the required set so a file that merely contains `local-only` is not a match.

### F-7: Local resume does not say which files are ticket files
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:217 | spec § Phase 4 — File
**Edge case:** `docs/specs/TODO/` already holds `<PARENT-ID>.spec.md`, the brief, and other tickets' files. None of them contain `local-only`.
**What happens:** "Read every existing sibling first" and "a file that lacks `local-only` or a required heading is incomplete, not a match" can be read as every file in that directory. The spec file itself then fails the check, the mismatch halt fires before any write, and local mode cannot file. The native/text guard at line 54 is already limited to `<PARENT-ID>.ticket-*.md`. The local paragraph is not.
**Why the spec misses it:** "Dropped slug" implies slug-bearing files, but the incomplete-file sentence is not tied to that glob. "Required heading" is also unnamed, so a file that has `local-only` and is missing Acceptance can still be called a match.
**Suggested fix:** Candidates are only `docs/specs/TODO/<PARENT-ID>.ticket-*.md`, excluding dot-prefixed temps. The spec, the brief, other parents, and temps are not candidates. A candidate is incomplete unless it has `local-only` and every body heading from line 215.

### F-8: The states.json path under the config dir is not written down
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:135 | spec § Decision 12
**Edge case:** The implementer copies only the config-dir sentence and opens `<config-dir>/states.json`, or copies `/ship-spec` Phase 0 step 9 and ignores `$CLAUDE_CONFIG_DIR`.
**What happens:** `/spec-brief` and `/spec-close` read `<config-dir>/skills/ship-spec/states.json`. `/ship-spec` reads `~/.claude/skills/ship-spec/states.json` and does not consult `$CLAUDE_CONFIG_DIR`. Decision 12 says "that path order" and never writes the `skills/ship-spec/states.json` suffix. The wrong file is missing, so every tracker mode halts before approval even when the installed file is valid. Local mode, which does not read the file, still works, so the failure looks like "no tracker".
**Why the spec misses it:** The round-1 fix split the citation into directory order versus field and halt, and the relative file path was not restated.
**Suggested fix:** Name the file as `<config-dir>/skills/ship-spec/states.json`, with the config-dir order already in that paragraph. Say this is not `/ship-spec`'s path when `$CLAUDE_CONFIG_DIR` is set.

### F-9: The no-blocker sentinel is not defined as the empty edge set
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:44 | spec § Decision 3; spec § Decision 12, line 147
**Edge case:** An existing text or local body contains the single line `None — no blockers.`, and the approved set for that piece is empty. A second run parses every non-blank line of `Blocked by` as a title.
**What happens:** The recorded set becomes `{None — no blockers.}`, which is not in the approved set, so line 151 treats it as an extra edge and halts before any write. The idempotent re-run of a graph whose pieces have no blockers never prints `FILED`. The approval block's word "none" (line 197) is a third spelling, so a compare against the printed block fails the same way.
**Why the spec misses it:** Line 44 says the section is either full titles or that one line. Line 147 says the recorded set is the full titles in the section. It never says the sentinel is the empty set and is not itself a title.
**Suggested fix:** On read, the single line `None — no blockers.` is the empty set. Any other line is a full title. A mix of the sentinel and a title is cannot-read. Use that same sentinel in the approval block instead of "none".

### F-10: A child-list page that errors or repeats is not a failed read
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:137 | spec § Decision 12
**Edge case:** The second page of the parent's children returns a transport error, a non-success status, or the same cursor again. The relation read is a paged list and only the first page is returned.
**What happens:** Pagination stops only on a short page or when "the listing says it is done". An error is neither, so it can be taken as the end of the list. Slugs on the unseen page are created again. A repeated cursor never produces a short page, so the probe hangs. A short relation page is a successful subset: an extra or reversed edge on a later page is invisible, missing edges look unwritten, and line 222 can print `FILED` while the stored graph is not the approved set.
**Why the spec misses it:** Paging is specified for the child list only, and only for the happy stop conditions. The cannot-read rule is stated for the relation body, not for a failed page.
**Suggested fix:** A page error, a non-success page, or a repeated cursor is cannot-read and halts before any create or edge write. Apply the same paging rule to the `blocked_by` read. Do not treat a partial page as the set.

### F-11: Two overlapping runs can both create the same slug
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:142 | spec § Decision 12
**Edge case:** The first run is still inside create (no timeout bound; a five-minute tool call is only "does not return" after the host gives up). The operator starts a second run. Both re-list, both see zero children, both create.
**What happens:** Line 142 closes the race only for a list that already shows one or two children. It does not cover two creates that both passed that list. Both children remain. The next run hits two matches and stops. Create-only cannot delete either. Nothing in the spec says which writer wins or that the duplicate is left on purpose.
**Why the spec misses it:** The re-list is the whole concurrency story. There is no unique title constraint and no post-create recount shared with F-3.
**Suggested fix:** After every create, list that slug again before the next create. Two rows is a halt with no further writes and no `FILED`, and the stop report names both ids. State that overlapping runs are not serialized and that the skill will not delete the loser.

### F-12: A successful truncated body is not the failure the deferral assumes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:291 | spec § Deferred (P2+); spec § Decision 12, line 144
**Edge case:** The tracker returns success and stores a body shorter than the one sent. `Blocked by` is the last section (line 215), so it is the part that gets cut. Local files have no tracker error at all.
**What happens:** The deferral says an oversized create stops under Decision 12 and does not print `FILED`. Decision 12 stops on an error payload, not on a 2xx body that is shorter than the request. If the truncated section still parses as the approved edge set, F-6's skip prints `FILED` with the criteria gone. If the section is gone, the absent-section rule halts and, because bodies are not edited, the children can never gain `Blocked by`. Local files are unbounded and a retry overwrites the temp and renames it, so size never fails there.
**Why the spec misses it:** The note treats "create failed" as the only oversized outcome. Read-back compares edges, not the stored body to the body that was sent.
**Suggested fix:** Keep the cap deferred if that is still the call, but delete the claim that every oversized create stops. A success response whose stored body is not the body sent is a mismatch, not an idempotent skip and not `FILED`.

### F-13: The stop report names the slug and not the failing call
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:153 | spec § Decision 12
**Edge case:** A relation write, a child list, or a parent retrieve returns an error payload, an ACL denial, or a non-success status after some children already exist.
**What happens:** The operator sees each slug as `created`, `existing`, or `missing`, and each edge as `written`, `missing`, or `mismatched`. The integration name, the capability that failed, the status, and the error payload are not in that report. Phase 1's reason is only for the pre-approval probe. A later debugger cannot tell a dropped parent from a timeout from a reversed edge.
**Why the spec misses it:** The round-1 stop-report sentence listed the three tokens and `FILED` suppression, and no field for the tracker error.
**Suggested fix:** On every halt after approval, add one line: `halt: <capability> <slug or edge> <integration name> <status or error payload>`, then the per-slug and per-edge tokens. Do not print `FILED`.

### F-14: Plane ticket text was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45`, `source_system: plane`.
**What happens:** The call returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. This review used the brief and the repo. The ticket body was not checked against the spec.
**Why the spec misses it:** Not a spec defect. The brief says its Done when list is transcribed from the ticket.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read `skills` if the ticket text must be confirmed.

## Summary
P0: 1 | P1: 5 | P2: 7 | P3: 0 | P4: 1

STATUS: RED P0=1 P1=5 P2=7 P3=0 P4=1
