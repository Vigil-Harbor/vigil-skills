# Correctness Review — round 4

The round-3 text-mode fold unwraps the body compare, but the slug match still runs on plane-proxy’s fenced `name`. That leaves the fleet path unable to finish.

## Closure of round 3 findings

No commit in the last 7 days touches the files this spec edits (newest is `d4db373`, 2026-09-08). `skills/*/SKILL.md` is still 11 files, so 12 after `spec-tickets` matches `tests/test_lint.py` lines 50–55. There is no `## Deferred — follow-up required` section. `scale_lens` is off; no scalability report was read. Memory lookup is still unavailable.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Text-mode success never matches the frozen draft on plane-proxy | PARTIAL | Equality compare unwraps the fence (spec § Decision 12 lines 160–164, § Phase 4 line 232, § Test plan line 270). Slug identity at lines 141–148 still uses the raw title. plane-proxy fences `name` before that check (`plane-proxy/src/provenance.ts` lines 18–45, 79–80). |
| correctness | F-2 | The parent check rejects the only parent value plane-proxy accepts | CLOSED | spec § Decision 12 lines 137 and 145–148: create parent and API parent are the retrieved work-item UUID; body Parent is the identifier; omitted echo parent does not stop. § Phase 4 line 231. § Test plan line 270. `create_work_item` `parent` is `z.string().uuid()` (`plane-proxy/src/tools.ts` line 242). |
| correctness | F-3 | ticket not cached | CLOSED | Not a spec defect. Lookup is still unavailable. Re-filed as F-3 below. |
| edge-cases | F-1 | The relation proof reads the work item, which never carries blocked_by | CLOSED | spec § Decision 3 line 44; § Decision 12 line 153; § Test plan line 267. Proof is the relation list. An empty list is the empty set. A work-item body with no `blocked_by` key is not that read. A 404 at probe time takes `text` before any create. A failed read-back does not write the same edge again and does not switch mode. |
| edge-cases | F-2 | The body the match requires is not in the work-item read | CLOSED | spec § Decision 12 lines 162–164: body is `description_html`; a later read requests it; the create echo is not the proof; an empty requested field is cannot-read; one HTML wrapper is stripped after the fence unwrap. § Phase 4 line 232. § Test plan line 270. |
| edge-cases | F-3 | A missing project field halts, and the default retrieve has no such field | CLOSED | spec § Decision 12 line 137: request the project field; accept `project` or `project_id`; halt only when the requested field is absent or unequal; a body that never asked is not "missing". |
| edge-cases | F-4 | A rewritten title is invisible on the next run, so resume creates a second child | CLOSED | spec § Decision 12 line 143 halts, before any create, a child whose title starts with `<PARENT-ID> ` but does not parse. A prefix-dropping stored rewrite is explicitly not a halt, because it cannot be told from another child of the same parent. The fenced-name failure is correctness F-1, still PARTIAL, not this row. |
| edge-cases | F-5 | "The spec's ticket" is not the parent value the tracker returns | CLOSED | Same UUID / `parent` / `parent_id` edit as correctness F-2. |
| edge-cases | F-6 | Plane ticket text was not readable | CLOSED | Not a spec defect. Re-filed as F-3. |
| conventions | F-1 | Drift-check — round-3 pins with rationale | CLOSED | No defect. The round-3 pin list was informational. Not re-filed. |

## Findings

### F-1: Slug identity still matches the raw fenced title, so text mode never keeps a child
**Severity:** P0
**Where:** spec.md:143 | spec § Decision 12; spec § Phase 4 — File
**Claim:** "A title that does not start with that prefix belongs to some other piece. It is not a match, and it is not a reason to halt." "Zero matches: create." "Keep the id only when that list shows exactly one row … and the title parses to the slug. Otherwise halt." Unwrap is specified later: "Before the compare, unwrap. … plane-proxy always returns those two fields fenced, so a raw equality check halts every successful text create."
**Why this is wrong:** `formatResponse` fences every string `name`, including names inside a list page (`plane-proxy/src/provenance.ts` lines 18–21 and 40–45; `list_work_items` returns `formatResponse` at `plane-proxy/src/tools.ts` lines 112–118). A stored title `VHS-45 draft: Short title` is returned as `<external_content source="plane" trusted="false">VHS-45 draft: Short title</external_content>`. That string does not start with `VHS-45 `, so line 143 classifies the skill’s own child as some other piece. The post-create keep rule then fails the parse and halts before the unwrap-and-compare step. The next run still sees zero slug matches and creates another child. The two-match halt never fires, because a fenced title never parses as the slug. Create-only cannot delete the extras, and `FILED` never prints. That is the same text-path failure as round-3 correctness F-1: on plane-proxy, the reachable tracker, a piece is not successfully ticketed (spec § Done when, the tracker bullet).
**Suggested fix:** Unwrap `name` before every slug parse, not only before the body compare. State that the prefix test, the zero/one/two match rules, and the post-create "title parses to the slug" check all use the unwrapped title. A fenced name is not "some other piece" and is not a tracker rewrite. Repeat that in § Phase 4 and in the test-plan resume bullet.

### F-2: Native read-back takes `object.id`, but the relations list identifies the work item as `issue_id`
**Severity:** P1
**Where:** spec.md:153 | spec § Decision 12
**Claim:** "A 2xx body whose `blocked_by` is a list of id strings, or a list of objects, is a successful read. The set is those ids, taking each object's id."
**Why this is wrong:** A list of id strings still works. `WorkItemWithRelationType` also has `id` as the work-item id. The current relations GET does not. Plane’s relation list builds `blocked_by` entries as `{project_id, issue_id}` with no `id` (`makeplane/plane` preview `IssueRelationViewSet.list`, and the response change in [makeplane/plane#8860](https://github.com/makeplane/plane/pull/8860)). Taking `object.id` yields an empty set. After a real relation create, the read-back "does not contain the blocker", which line 153 calls cannot-read. The run does not write the edge again and does not switch to `text`, so native mode never prints `FILED`. The same miss happens on resume, because the approved edge looks absent.
**Suggested fix:** In § Decision 12, define the work-item id on a relation object as `issue_id` when that key is present, otherwise `id`. Say a 2xx list of objects that have neither key is cannot-read. Add the `issue_id` case to the test-plan native bullet.

### F-3: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec implements Plane ticket VHS-45. The brief says its Done when list is transcribed from the ticket.
**Why this is wrong:** No MCP memory tool is available in this session, so `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45` could not be run. Review used the brief and the repo. If the ticket’s acceptance criteria differ from the brief, that conflict was not checked.
**Suggested fix:** None in the spec. Re-cache the work item into a namespace this reviewer can read if the ticket text must be confirmed.

## Summary
P0: 1 | P1: 1 | P2: 0 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=1 P2=0 P3=1 P4=0
