# Edge-Cases Review — round 5

Delta-scoped to the sections rewritten after round 4: Decision 3, Decision 12, the Skill outline, Phases 0, 1, 3 and 4, the tracker bullets of the Test plan, the two Out of scope bullets, and the Deferred (P2+) row. No P0 or P1. The rewritten text has no path that files without approval, writes both a tracker graph and local files in one run, reverses an edge, or prints `FILED` after a failure, and its filing order can always be satisfied. Six P2/P3 clarifications follow; none needs verification machinery.

## Closure of round 4 findings

Grounding notes:

- No `## Deferred — follow-up required` section exists, so there is no routing-row check. `## Deferred (P2+)` is a different heading.
- `scale_lens` was not passed; round 4 has no `scalability.md`.
- No closure manifest was passed. Closure is verified against the spec text.
- `memory_search` on namespace `skills` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The brief is the ticket text (F-7).
- The reference `to-tickets` skill was read from `mattpocock/skills`. Its §5 is the shape Decision 12 now follows: publish in dependency order, blockers first, no read-back, no resume.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Slug identity still matches the raw fenced title, so text mode never keeps a child | CLOSED | Closed by removal. Spec § Decision 12 lines 135 and 145: no child-identity parse, no adopt-or-create, no compare. Line 57: the tracker name is the short title with no `<PARENT-ID> <slug>:` prefix. Test plan line 245 requires that the skill has no read-back, resume or compare step. |
| correctness | F-2 | Native read-back takes `object.id`, but the relations list identifies the work item as `issue_id` | CLOSED | Closed by removal. Line 133: "This skill does not read its own writes back". Line 157: "The skill names no tracker response field". No relation-list read remains in Decision 3 or Decision 12. |
| correctness | F-3 | ticket not cached | CLOSED | Not a spec defect. Re-recorded as F-7 below. |
| edge-cases | F-1 | A fenced child title is "some other piece", so text mode creates another child | CLOSED | Same removal as correctness F-1. The duplicate-on-second-run outcome is now the stated behaviour (line 145, Out of scope line 276) with the operator as the guard, not a silent result of a failed match. |
| edge-cases | F-2 | The official relation list has no top-level `blocked_by` | CLOSED | Same removal as correctness F-2. The native probe is now "offers an operation that creates a blocked-by relation" (line 42). No list shape is read. |
| edge-cases | F-3 | A finished plane-proxy page still carries a cursor | CLOSED | Closed by removal. The paginated child listing that fed resume is gone. The one remaining list read (line 145) feeds a notice that prints `unknown` on failure and gates nothing. |
| edge-cases | F-4 | Plane ticket text was not readable | CLOSED | Not a spec defect. Re-recorded as F-7 below. |
| conventions | F-1 | The mode table still keys `text` off "not advertised" | CLOSED | Line 43: the `text` row now reads "The same, except it offers no such relation operation". The 404-probe wording is gone from Decision 3. |
| conventions | F-2 | Drift-check — round-4 pins with rationale | CLOSED | No defect. Every pin in that list (relation-list proof, `description_html` read, fence unwrap, parent UUID echo, project field, title-prefix parse) was part of the removed protocol and is no longer in the spec. |

## Findings

### F-1: A target file that appears between approval and the write has no stated outcome
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:147, spec.md:206, spec.md:210 | spec § Decision 12; spec § Phase 4 — File
**Edge case:** `local` mode. The existence check runs when the approval block is rendered. The write happens later, after the operator replies. A file at a target path can exist at write time and not at render time (the operator saved one by hand, or a revise round changed a slug onto an existing name after the Phase 1 listing).
**What happens:** Line 210 says the write "never overwrites an existing file" and that "a file write that fails is a Decision 12 failure". It does not say what an existing target at write time is. One reading skips that piece and continues with the rest; the other stops. Under the skip reading, later files carry a `Blocked by` reference to a file this run did not write. Line 214's "every create returned success" probably keeps `FILED` from printing, but the text does not say so.
**Why the spec misses it:** Phase 4 re-runs "the Decision 5 gate" (line 206). The local-target check lives in Decision 12 and Phase 3, not in Decision 5, so the re-run does not include it.
**Suggested fix:** Add to line 210: "A target that exists at write time is a Decision 12 failure: stop, write nothing further, print the stop report." No new machinery; it names an outcome the failure rule already has.

### F-2: A tracker-mode run does not notice local ticket files from an earlier `local` run
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:145, spec.md:184 | spec § Decision 12 (No resume); spec § Phase 3 — Approval
**Edge case:** A first run with no integration connected writes `docs/specs/TODO/<PARENT-ID>.ticket-*.md`. A later run for the same spec has the tracker connected and takes `native` or `text`.
**What happens:** The existing-work read is "the parent's children ... or the files" — one of the two, by mode. The tracker run counts children only, reports `0`, and files. The repo then holds local ticket files beside a live tracker graph, which line 47 names as the reason `halt` exists ("local files beside a live tracker are a second graph"). The operator gets no line about it in the approval block.
**Why the spec misses it:** The never-does rule "write both tracker records and local files" (line 159) is per run. The notice was written per mode.
**Suggested fix:** On a tracker mode, make the notice cover both: the count of children, and the count of matching local files when it is above zero. For example: `Existing under parent: <n children>; <m local ticket files>`. It stays a notice and does not gate option 1. This is a directory listing the skill already knows how to do, not a new check.

### F-3: Phase 1 says the existing-work read happens only on a tracker mode
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:167 against spec.md:145 and spec.md:147 | spec § Phase 1 — Storage probe; spec § Decision 12
**Edge case:** `local` mode.
**What happens:** Line 167: "On a tracker mode it also resolves the parent and makes the one existing-work read". Read literally, `local` makes no existing-work read. Line 145 says the read is the file glob on `local`, line 184 prints `n local ticket files`, and line 147 needs the listing to omit option 1. An implementer following Phase 1 alone prints nothing or `unknown` on `local`, and has no listing for the overwrite check until Phase 4.
**Why the spec misses it:** The Phase 1 sentence joins the parent resolve (tracker only) and the existing-work read (every non-halt mode) under one condition.
**Suggested fix:** Split the sentence: "On a tracker mode it also resolves the parent. On every mode except `halt` it makes the one existing-work read (Decision 12)."

### F-4: A failed list-children read is `unknown` in one place and matches the `halt` row in another
**Severity:** P2
**Where:** spec.md:45 against spec.md:145 | spec § Decision 3 (mode table, `halt` row); spec § Decision 12 (No resume)
**Edge case:** The integration creates and resolves the parent, then returns an error on the list-children read.
**What happens:** The `halt` row's When cell is "An issue-tracker integration is connected, and it does not answer, returns an error, ...". Line 145 says the count is `unknown` "when the read is not available or fails", which keeps the mode. Both outcomes are safe: one writes nothing, the other shows `unknown` to the operator. They are still two instructions for one event. The same cell has a second loose end: with two integrations connected, one capable and one that cannot create with a parent, the `native` row and the `halt` row both match, and line 49 counts only the capable ones.
**Why the spec misses it:** "returns an error" in the `halt` row has no stated subject.
**Suggested fix:** Scope the `halt` cell to the probe and the parent resolve: "... and its capability probe or the parent retrieve does not answer or returns an error, or it cannot create a work item with a parent". Add: "An integration that cannot create a work item with a parent is ignored when another connected integration can."

### F-5: The approval-block template has no slot for the two lines Decision 12 adds
**Severity:** P3
**Where:** spec.md:179–200 against spec.md:145 and spec.md:147 | spec § Phase 3 — Approval
**Edge case:** Existing count above zero; a `local` target that already exists.
**What happens:** Decision 12 requires "one line saying that approval files these pieces in addition to what exists" and that "the block names those paths". The fenced template shows neither, and line 202 says the printed block is what approval freezes. An implementer who treats the template as the complete block drops both lines. That is the operator's only duplicate guard. The Test plan covers the paths line (line 246) and not the in-addition line (line 245).
**Suggested fix:** Add two optional lines to the template under `Existing under parent:` — `  Approval files these pieces in addition to the <n> that exist.` and `Local targets that already exist: <paths>` — and add "a count above zero prints the in-addition line" to the Test plan bullet at line 245.

### F-6: Two sentences outside the rewrite now disagree with it
**Severity:** P3
**Where:** spec.md:264; spec.md:245 and spec.md:276 | spec § Done when; spec § Test plan; spec § Out of scope
**Edge case:** None at runtime. Stale cross-references left by the rewrite.
**What happens:** Line 264 cites "Decision 3's rule that create-before-edge is not a build order". That rule is now in Decision 12's Order paragraph (line 139). Decision 3 only points to it. Lines 245 and 276 say "a second run files every piece again" with no qualifier. Line 145 limits that to a tracker, and line 147 makes a second `local` run refuse because its targets exist.
**Suggested fix:** Line 264: cite Decision 12. Lines 245 and 276: "on a tracker, a second run files every piece again; on `local` it is refused while the files exist".

### F-7: Plane ticket text was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45`.
**What happens:** `Error: Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The review used the brief, which says its Done when list is transcribed from the ticket.
**Why the spec misses it:** Not a spec defect.
**Suggested fix:** None in the spec.

## Persistence checklist (rewritten sections only)

| Item | Result |
|---|---|
| Atomicity | Operator-accepted: no temp file or rename. A killed write leaves a partial file, and the next `local` run omits option 1 because the target exists (line 147). |
| Size bound | Deferred (P2+) row, line 282. An oversized create that the tracker rejects is a Decision 12 stop. |
| Idempotency on retry | Operator-accepted: none on a tracker (line 145). `local` refuses the second run (line 147). F-6 asks the Test plan to say so. |
| Read-side filtering | Not applicable. Nothing reads these records back; `/ship-spec` ignores children (Decision 8). |
| Schema-version forward-compat | Not applicable. No format token, by the same Deferred row. |
| Write-then-read race | Operator-accepted: overlapping runs unsupported. F-1 covers the single-run gap between approval and write. |

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 2 | P4: 1

STATUS: GREEN
