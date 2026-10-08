# Edge-Cases Review — round 4

## Closure of round 3 findings

No `## Deferred — follow-up required` section, so there is no routing-row check. `## Deferred (P2+)` is a different heading. `scale_lens` is off; no scalability report was read. Memory search is unavailable (no MCP memory tool); the brief is the ticket text. Manifest folds for the five P0/P1 lines are present; two of them do not close the failure.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Text-mode success never matches the frozen draft on plane-proxy | PARTIAL | Unwrap, entity decode, and one HTML strip are at spec § Decision 12 lines 162–164, § Phase 4 line 232, and § Test plan line 270. The child-identity parse at lines 141–148 still classifies a raw title, so a fenced `name` never matches. Residual is F-1 below. Keeps P0. |
| correctness | F-2 | The parent check rejects the only parent value plane-proxy accepts | CLOSED | spec § Decision 12 lines 137 and 145–148: create `parent` and the accepted API parent are the retrieved work-item UUID; `parent` or `parent_id`; an omitted echo key does not stop by itself. § Phase 4 line 232. § Test plan line 270. |
| correctness | F-3 | ticket not cached | CLOSED | Not a spec defect. Lookup is still unavailable. Re-recorded as F-4 below. Not promoted. |
| edge-cases | F-1 | The relation proof reads the work item, which never carries `blocked_by` | PARTIAL | spec § Decision 3 line 44 and § Decision 12 line 153 name the relation list, an empty list, a 404-before-create, and no second write. Line 153 still requires top-level `blocked_by`. The official list wraps that list under `dependencies`. Residual is F-2 below. Keeps P1. |
| edge-cases | F-2 | The body the match requires is not in the work-item read | CLOSED | spec § Decision 12 lines 162–164: send `description_html`, prove it on a later read that requests that field, create echo is not the proof, empty requested field is cannot-read, then one HTML wrapper. § Phase 4 line 232. § Test plan line 270. |
| edge-cases | F-3 | A missing project field halts, and the default retrieve has no such field | CLOSED | spec § Decision 12 line 137: request the project field; accept `project` or `project_id`; halt only when the requested field is absent or unequal. A body that never asked is not "missing". |
| edge-cases | F-4 | A rewritten title is invisible on the next run, so resume creates a second child | CLOSED | spec § Decision 12 line 143: before any create, including resume, a child title that starts with `<PARENT-ID> ` and does not parse is cannot-read. A rewrite that drops the prefix is stated as undetectable. |
| edge-cases | F-5 | "The spec's ticket" is not the parent value the tracker returns | CLOSED | Same edit as correctness F-2. |
| edge-cases | F-6 | Plane ticket text was not readable | CLOSED | Not a spec defect. Re-recorded as F-4 below. Not promoted. |
| conventions | F-1 | Drift-check — round-3 pins with rationale | CLOSED | No defect. The pins it listed are still in the spec. No new silent scope addition in the folds above. |

## Findings

### F-1: A fenced child title is "some other piece", so text mode creates another child
**Severity:** P0
**Where:** spec.md:143 | spec § Decision 12; spec § Phase 4 — File
**Edge case:** plane-proxy text mode. `formatResponse` fences every `name` (`plane-proxy/src/provenance.ts` lines 18–45 and 79–80). List, retrieve, and create all return that fence. A live `list_work_items` row is `"name": "<external_content source=\"plane\" trusted=\"false\">…</external_content>"`.
**What happens:** Line 143 keeps a child only when the title starts with `<PARENT-ID> `. A fenced name starts with `<external_content`, so it is "some other piece": not a match and not a halt. Zero matches, so the run creates. The post-create list (line 148) keeps the id only when the title parses to the slug. The fenced title does not parse, so the run halts with no further creates and no `FILED`. The next run still does not see the child and creates another. Create-only does not delete the losers. Unwrap at line 164 runs only "before the compare", which this path never reaches.
**Why the spec misses it:** The round-3 fix unwraps `name` for equality. It does not unwrap `name` before the prefix test added on this round. Line 164 even says a raw equality check halts every text create, and then leaves the raw string in charge of create-versus-adopt.
**Suggested fix:** Unwrap `name` with the Decision 12 fence rule before the prefix test, the slug parse, and the post-create keep check, on the list and on the create echo. A fenced name is not "some other piece". Only the unwrapped title is classified. Add that case to the test plan next to the text-compare bullet.

### F-2: The official relation list has no top-level `blocked_by`
**Severity:** P1
**Where:** spec.md:153 | spec § Decision 12; spec § Decision 3
**Edge case:** Native mode on the current official Plane MCP (`workitem_relation` action `list`). The tool returns `{"dependencies": <WorkItemDependencyResponse>, "custom": {...}}` (`plane-mcp-server/plane_mcp/tools/workitem_relation.py` lines 185–195). `blocked_by` is `dependencies.blocked_by`, a list of `WorkItemWithRelationType` objects whose `id` is the work item id. The 2xx body has no top-level `blocked_by` key.
**What happens:** Line 153 accepts a read only when the body's `blocked_by` is a list. This body fails that test. A missing key is not the empty set, and a value that is present and is not a list is cannot-read, which stops creates and edge writes. An empty dependency list therefore never counts as "nothing recorded yet", so the first `blocked_by` create does not run. If a create did run, the read-back still does not contain the blocker at the top level, so the run stops, does not write that edge again, and does not switch to `text`. The next run hits the same shape. `FILED` never prints. Children already created stay, with the graph unrecorded.
**Why the spec misses it:** The fold matches the legacy top-level `{blocked_by: [...]}` shape. The 30-tool server the brief points at wraps that object under `dependencies`.
**Suggested fix:** A successful relation-list read is a 2xx body whose `blocked_by` is a list, or whose `dependencies.blocked_by` is a list. The set is that list; an empty list in either place is the empty set. Take each object's `id`. A body with neither key is not the read. Do not treat the `dependencies` object itself as a non-list cannot-read. Say this in the test plan.

### F-3: A finished plane-proxy page still carries a cursor
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:139 | spec § Decision 12
**Edge case:** `list_work_items` through plane-proxy. A finished page is `next_page_results: false`, `total_pages: 1`, and `next_cursor: "50:1:0"` (live list body). The official MCP rule is the opposite: follow `next_cursor` until it is empty.
**What happens:** "Short" and "the listing says it is done" are not tied to a field. A run that pages while `next_cursor` is non-empty fetches that cursor, gets it again, and line 139 calls a repeated cursor cannot-read. That halt is before any create or edge write, so text mode never files.
**Why the spec misses it:** The repeated-cursor rule was added to stop a loop. It does not say that a cursor on a page already marked done is not fetched and is not a repeat.
**Suggested fix:** Done means `next_page_results` is false, or `next_cursor` is empty or absent. A cursor on a page the listing marks done is not requested again and is not a repeated-cursor failure.

### F-4: Plane ticket text was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45`.
**What happens:** No MCP memory tool is available. The review used the brief and the repo. The ticket body was not checked against the spec.
**Why the spec misses it:** Not a spec defect. The brief says its Done when list is transcribed from the ticket.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read `skills` if the ticket text must be confirmed.

## Summary
P0: 1 | P1: 1 | P2: 1 | P3: 0 | P4: 1

STATUS: RED P0=1 P1=1 P2=1 P3=0 P4=1
