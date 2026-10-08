# Edge-Cases Review — round 3

## Closure of round 2 findings

No `## Deferred — follow-up required` section, so there is no routing-row check. `## Deferred (P2+)` is a different heading. `scale_lens` is off; no scalability report was read. Manifest folds for the eight P0/P1 lines are present in the current spec. `skills/*/SKILL.md` is still 11 files.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Repo-root walk excludes cwd, so the usual invocation never resolves | CLOSED | spec § Decision 7 line 87: cwd is the root when it contains `AGENTS.md` or `CLAUDE.md`; separators are normalized. § Test plan line 257. |
| correctness | F-2 | Resume parses a work-item title Phase 4 never writes | CLOSED | spec § Decision 3 line 46; § Decision 12 lines 141–147; § Phase 3 line 219; § Phase 4 line 225; § Test plan line 261. Stored name and local H1 are `<PARENT-ID> <slug>: <short title>`. The approval line is display only. |
| correctness | F-3 | An incomplete local sibling has no outcome, and the temp rules disagree | CLOSED | spec § Phase 4 lines 229–231: candidates are only `<PARENT-ID>.ticket-*.md`; incomplete is a mismatch; temp is removed only after a rename onto a path that did not exist. |
| correctness | F-4 | ticket not cached | CLOSED | Not a spec defect. Lookup is still unavailable; re-recorded as F-6 below. |
| conventions | F-1 | The new README Requirements bullet is unscoped | CLOSED | spec § Decision 10 line 108: scoped `For /spec-tickets:` bullet; other bullets and the `gh` sentence are unchanged. |
| conventions | F-2 | The string Phase 4 writes is not the string Decision 12 matches | CLOSED | Same edit as correctness F-2. |
| conventions | F-3 | `issue-tracker?` halt overrides the portability contract without naming it | CLOSED | spec § Decision 3 line 55 names portability-contract §3 and keeps the `requires:` block. |
| conventions | F-4 | Drift-check — round-2 additions with rationale | CLOSED | No defect. No new silent addition this round. |
| conventions | F-5 | The local temp copies spec-brief's path and drops its commit warning | CLOSED | spec § Phase 0 line 181: temps are not gitignored; printing them is the warning. |
| conventions | F-6 | Two Storage-line grammars | CLOSED | spec § Decision 3 line 42; § Phase 3 lines 200 and 219 use that grammar. |
| edge-cases | F-1 | Zero "can create" still selects local, including a tracker that is up | CLOSED | spec § Decision 3 lines 40–42 and 55; § Test plan line 261. `local` only when no issue-tracker integration is connected. A probe that does not answer, or a connected integration that cannot create or cannot set a parent, is `halt`. |
| edge-cases | F-2 | The repo-root walk excludes the directory the operator is in | CLOSED | Same edit as correctness F-1. |
| edge-cases | F-3 | Resume matches a title the create never sets | CLOSED | Same edit as correctness F-2. Post-create list must show exactly one row with that id, that title, and the spec's ticket as parent (line 147). |
| edge-cases | F-4 | An omitted relation field never becomes the empty set | CLOSED | spec § Decision 12 line 152; § Test plan line 262. A successful work-item body that omits `blocked_by`, or whose `blocked_by` is `[]`, is the empty set. A non-list value is cannot-read. The live relation payload is a new defect, F-1 below. |
| edge-cases | F-5 | A create result with no parent field is kept as the child | CLOSED | spec § Decision 12 lines 145–147; § Test plan line 265. An omitted or null parent stops. The id is kept only when a fresh child list shows exactly one matching row. Comparing that parent to the ticket identifier is F-5 below. |
| edge-cases | F-6 | Equal edges print FILED while the approved body was not written | CLOSED | spec § Decision 12 line 159; § Phase 4 lines 227 and 235; § Test plan line 265; § Deferred (P2+) line 303. A match requires the stored body to equal the frozen draft. The official read never returns that body, F-2 below. |
| edge-cases | F-7 | Local resume does not say which files are ticket files | CLOSED | spec § Phase 4 line 229. |
| edge-cases | F-8 | The states.json path under the config dir is not written down | CLOSED | spec § Decision 12 line 137: `<config-dir>/skills/ship-spec/states.json`, and it is not `/ship-spec`'s path when `$CLAUDE_CONFIG_DIR` is set. |
| edge-cases | F-9 | The no-blocker sentinel is not defined as the empty edge set | CLOSED | spec § Decision 3 lines 46–47; § Phase 3 line 219; § Test plan line 265. |
| edge-cases | F-10 | A child-list page that errors or repeats is not a failed read | CLOSED | spec § Decision 12 line 139; § Test plan line 262. |
| edge-cases | F-11 | Two overlapping runs can both create the same slug | CLOSED | spec § Decision 12 lines 147–148: post-create recount; two rows halt; the skill does not delete the loser. |
| edge-cases | F-12 | A successful truncated body is not the failure the deferral assumes | CLOSED | spec § Decision 12 line 159 and § Deferred (P2+) line 303. A success whose stored body is not the body sent is a mismatch and does not print `FILED`. The cap stays deferred. |
| edge-cases | F-13 | The stop report names the slug and not the failing call | CLOSED | spec § Decision 12 line 163: `halt: <capability> <slug or edge> <integration name or none> <status or error payload>`. |
| edge-cases | F-14 | Ticket bodies and local files have no size bound or format version | DEFERRED | spec § Deferred (P2+) lines 301–303. Not a `D-<n>` row. Not re-filed. |
| edge-cases | F-15 | Deferred-row count is undefined | CLOSED | spec § Decision 7 line 93. Count only `### D-<n>:` headings outside fences. |
| edge-cases | F-16 | Plane ticket text was not readable | CLOSED | Not a spec defect. Re-recorded as F-6 below. |

## Findings

### F-1: The relation proof reads the work item, which never carries `blocked_by`
**Severity:** P1
**Where:** spec.md:152 | spec § Decision 12; spec § Decision 3 line 44
**Edge case:** Native mode, which is the official Plane integration. Its schema advertises `blocked_by` (`workitem_relation` `relation_type`: `blocking`, `blocked_by`, …). The relation read is a separate call. Its legacy body is `{ "blocked_by": ["<uuid>", …], "blocking": […] }`, not a work item. The current dependency list is `blocked_by: [WorkItemWithRelationType]`, a list of objects. The work-item retrieve has no `blocked_by` key at all (Plane v2 work-item read shape).
**What happens:** Line 152 accepts a read only when the body is the work item, and treats a missing key on that body as the empty set. Both faithful readings fail. If the relation payload is used, it is not the work item, so it is cannot-read and stops creates and edge writes. Children already created stay; the next run hits the same read and stops again. `FILED` never prints, and line 135 forbids switching that run to `text`. If the work-item retrieve is used, the key is always absent, so the set is empty, the edge is "not already present", and every retry writes another `blocked_by`. The contains-check on line 44 then fails because the work item still has no key, so the run stops and the next retry writes again. A list of relation objects also fails "the set is the target ids" unless an `id` is pulled out of each object. Self-hosted Plane CE makes this permanent in a second way: `create_work_item_relation` calls `/dependencies/`, which that server does not expose (plane-mcp-server issue 192), while the schema still advertises the type, so mode stays `native`.
**Why the spec misses it:** The round-2 fold defines the empty set as a missing key on the work item so the first write is not blocked. It never names the relation-list payload, which is the only body that actually contains `blocked_by`.
**Suggested fix:** Make the proof read the relation list for that child, not the work-item retrieve. A 2xx body whose `blocked_by` is a list of id strings, or a list of objects, is a successful read; the set is those ids (each object's id). A work-item body that simply has no `blocked_by` key is not a relation read and is not the empty set. Empty is only an empty list on the relation read. If that read 404s, or the create endpoint is absent, do not take `native`: take `text` when create and parent work, otherwise `halt`, and decide that before any create. After a create, a read-back that still does not contain the blocker is cannot-read and must not write that same edge again.

### F-2: The body the match requires is not in the work-item read
**Severity:** P1
**Where:** spec.md:159 | spec § Decision 12; spec § Phase 4 lines 227 and 235
**Edge case:** The tracker accepts `description_html` on create and does not return it on the default read or on the create echo. Plane v2 states that `description_html` is not part of the read shape. The official tool returns it only when `fields` includes `description_html`, and it wraps plain text into HTML on save. plane-proxy's create field is `description_html` (`plane-proxy/src/tools.ts:239`), not a markdown body.
**What happens:** Line 159 says a success whose stored body is not the body sent is a mismatch, and a native description that cannot be read is cannot-read. The create echo omits the description, so the first run mismatches as soon as the children exist. Create-only (line 135) cannot repair it. The next run reads the same shape, mismatches again, and does not print `FILED`. On `text`, `Blocked by` lives in that description, so a missing section is also a mismatch (line 153) and the edge set cannot be recovered. Even a requested `description_html` comes back as HTML, so a byte compare against the markdown section list fails the same way. Parallel resume never reaches the idempotent result.
**Why the spec misses it:** The round-2 body-equality rule assumes the tracker stores and echoes the section text. It does not name `description_html`, does not say to request that field, and does not allow an HTML wrapper.
**Suggested fix:** Send the body as the integration's description field (`description_html` on plane-proxy and on official `workitem` create). Prove it with a later read that requests that field; the create echo is not the proof. Compare the section text after one HTML wrapper is stripped, not the raw response bytes. A create echo that omits the description is not yet a mismatch. If the requested field is still empty, that is cannot-read, with no further creates and no `FILED`.

### F-3: A missing project field halts, and the default retrieve has no such field
**Severity:** P1
**Where:** spec.md:137 | spec § Decision 12; spec § Decision 3 line 55
**Edge case:** Phase 1 calls retrieve-by-identifier and then requires the parent's project id. The official v2 work-item object has no `project_id` and no `workspace_id`. The MCP field token is `project`, and only if `fields` asks for it. The default retrieve-by-identifier (`workitem_identifier` only) omits it.
**What happens:** Line 137 says a missing project field is `halt` before approval. Option 1 is omitted (Phase 1 line 185). No child is created. A reachable official tracker therefore never files, which is the opposite of the Done when bullet at line 285 (a reachable tracker gets a Plane child). plane-proxy's v1 body uses `project`, not `project_id`; a check that only accepts `project_id` halts that path too.
**Why the spec misses it:** The fold says the parent's project id must equal `states.json`'s `project_id` and that a missing field halts. It does not say to request the field, or that the key is `project` or `project_id`.
**Suggested fix:** On retrieve-by-identifier, request the project (`fields=project` on the official tool). Accept either `project` or `project_id`, and compare that UUID to `states.json` `project_id`. Halt only when the requested field is absent or unequal. A default body that never asked for the field is not "missing".

### F-4: A rewritten title is invisible on the next run, so resume creates a second child
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:147 | spec § Decision 12 lines 143–147
**Edge case:** The in-run post-create list sees a title the tracker rewrote, halts, and leaves that child in place. The operator runs the skill again, which is the documented resume.
**What happens:** Line 147 says not to treat the rewritten row as a different slug, but only inside that same create. The next run parses titles again. A title that does not parse is not a match and not an "existing slug", so line 143 sees zero matches and creates another child. Create-only cannot delete the first. The run after that sees two parseable rows, or one parseable row plus an orphan, and line 145 stops with no `FILED`.
**Why the spec misses it:** The rewrite sentence is attached to the post-create bullet. Resume's zero-match rule never looks at a child whose title does not parse.
**Suggested fix:** Before any create, a child of this parent whose title does not parse to the Decision 5 grammar is cannot-read: halt, name that id, and do not create. Apply the same rule on resume, not only on the create that just returned.

### F-5: "The spec's ticket" is not the parent value the tracker returns
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:145 | spec § Decision 12 lines 145–147
**Edge case:** Create succeeds and the child is parented. The response parent is `parent_id` (v2) or `parent` (plane-proxy v1), and the value is the parent's work-item UUID. The ticket identifier from the filename is `VHS-45`.
**What happens:** Line 145 treats a parent other than "the spec's ticket", and an omitted `parent` key, as a stop. A UUID is not `VHS-45`, and `parent_id` is an omitted `parent`, so the id is not kept and no edges are written. The next run's one-match rule (line 144) does not compare the parent value, so it can adopt the child and recover. The first run always halts after a correct create. If a later check also requires the parent string to equal `VHS-45`, the id is never kept and every retry stops the same way.
**Why the spec misses it:** "The spec's ticket" is used for both the human identifier and the parent link. The response key is not pinned.
**Suggested fix:** Resolve the parent once and keep its work-item UUID. Accept `parent` or `parent_id`. Equality is against that UUID. An omitted parent key on the create echo does not stop when the follow-up child list shows that UUID.

### F-6: Plane ticket text was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45`.
**What happens:** No MCP memory tool is available in this session. The review used the brief and the repo. The ticket body was not checked against the spec.
**Why the spec misses it:** Not a spec defect. The brief says its Done when list is transcribed from the ticket.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read `skills` if the ticket text must be confirmed.

## Summary
P0: 0 | P1: 3 | P2: 2 | P3: 0 | P4: 1

STATUS: RED P0=0 P1=3 P2=2 P3=0 P4=1
