The ticket lookup was denied in the `skills` namespace, so this review is grounded in the brief and the skills the spec actually calls. The spec has no deferred section to check.

# Edge-Cases Review — round 1

## Closure of round <N-1> findings
N/A — round 1

## Findings

### F-1: A failed edge write cannot be resumed
**Severity:** P0
**Where:** spec.md:52, spec.md:128-131
**Edge case:** Partial failure after at least one child exists and before its approved `blocked_by` edges are stored. Triggered by a tracker error, a timeout, or a create that returns success but no usable id, on the create-all-then-edges sequence Decision 3 allows.
**What happens:** The run stops and leaves children with no edges (native) or with a `Blocked by` section that does not match (text, if the body was not written). The next run, after a fresh approval, loads those children, sees recorded edges that differ from the approved set, and halts with no further creates. Decision 12 forbids editing a child, deleting an edge, or rewriting native onto text. The missing edges are never written. The same deadlock happens if a later re-probe flips mode: resume is allowed only when the mode matches, and the skill will not move an existing child onto the other mode.
**Why the spec misses it:** The same bullet says a failed edge write stops the run and that a later run resumes under the create-only rules. The create-only rule treats any edge difference as a graph the skill must not repair. Empty edges versus the approved set is a difference. The test checklist (spec.md:224-225) covers "do not rewrite onto text" and "do not edit an existing child," but not "finish edges that were never written."
**Suggested fix:** Split incomplete from conflict. If every existing child's recorded edges are a subset of the approved set (no extras, no reversed edges) and every existing slug is still in the draft, write only the missing edges and create only missing children. If any extra edge, reversed edge, or dropped slug is present, halt with no writes. The stop report must list each slug as `created <id>`, `existing <id>`, or `missing`, and each edge as `written`, `missing`, or `mismatched`, and must not print `FILED`. Add those two cases to the review checklist.

### F-2: Local re-runs halt even when Decision 12 says to skip
**Severity:** P0
**Where:** spec.md:128-131 and spec.md:192-193
**Edge case:** A second local-mode run after any target file already exists: a finished run, a retry of the same draft, or a kill after some renames and before the rest.
**What happens:** Phase 4 halts before the first write whenever any `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md` exists, and the next run halts on those files. A finished graph cannot no-op. A partial rename cannot be completed. The files that did land stay, the ones that did not are never written, and the operator cannot tell "all present and matching" from "half written" or "content differs," because the halt text is unspecified and `FILED` is suppressed. Per-file temp-and-rename is atomic; the set of files is not.
**Why the spec misses it:** Decision 12 includes local mode: the `Blocked by` section is the edge record, a matching child is skipped, a differing child halts, and a later run resumes. Phase 4 states the opposite for the same files ("halt before the first write"; "the next run halts on those files").
**Suggested fix:** Make Phase 4 implement Decision 12 for local files. Read every existing sibling first. If any file differs, names a slug the draft dropped, or is not a complete body, halt before any write and print the paths. If existing files match and some slugs are absent, write only the absent files. If all match, print the idempotent result and do not halt. Keep "halt with no writes" for a real mismatch.

### F-3: `states.json` handling cites a lookup that does not halt or return `project_id`
**Severity:** P1
**Where:** spec.md:125-126
**Edge case:** Missing file, empty `CLAUDE_CONFIG_DIR`, invalid JSON or a BOM, prefix present with `project_id` null or `""`, or a retrieved parent whose project is not that id. Also copying `/spec-brief`'s failure path.
**What happens:** `/spec-brief` Phase 0 step 3 (`skills/spec-brief/SKILL.md:53`) reads `namespace` and, on a missing, unparseable, or unknown prefix, warns and continues with `namespace = "plane"`. It does not read `project_id` and does not halt. An implementer who follows "the same lookup `/spec-brief` uses" will file with no project scope. An implementer who only treats an OS-unreadable file as fatal will let `json.loads` throw on invalid JSON, or will send an empty `project_id` and still create. A parent resolved by identifier in another project then gets children in the `states.json` project (or the reverse). The check is also specified only at file time, so the approval block can show `Storage: native` for a run that cannot file.
**Why the spec misses it:** Decision 12 names `project_id` and says missing or unknown prefix halts, then cites the spec-brief lookup, which is the other behavior. `/ship-spec` does halt on a missing prefix (`skills/ship-spec/SKILL.md:41`) but does not consult `$CLAUDE_CONFIG_DIR`. Unparseable JSON, an empty id, and a project mismatch are not in the failure list. `local` mode correctly skips the file; tracker modes do not say what "unreadable" includes.
**Suggested fix:** Do not cite `/spec-brief` for this. In Phase 1, for tracker modes only: resolve the config dir the way `/spec-close` does, and treat an empty `CLAUDE_CONFIG_DIR` as unset. Halt with no writes on missing, unreadable, invalid JSON, unknown prefix, or blank `project_id`, and show that as `halt (<reason>)` before approval. After retrieve, require the parent's project id to equal that `project_id`; otherwise halt with no writes.

### F-4: Any probe failure becomes `local`, including a tracker that is up
**Severity:** P1
**Where:** spec.md:46-50
**Edge case:** Timeout, HTTP 401/403/429/5xx, an error string inside a success body, a schema payload that is not a schema, or an ACL-denied provider. The portability contract treats transport-up plus ACL deny as unavailable (`docs/portability-contract.md:76`), not as "no tracker."
**What happens:** There is no timeout, so a hung probe waits indefinitely. Any failure the implementer classifies as "the probe failed" selects `local` and, after approval, writes ticket files. Decision 3 says local files are only for an unreachable tracker, and a reachable tracker that cannot record children must not be mirrored to disk. A later run whose probe succeeds takes `native` or `text`, does not look at those files, and creates a second graph. The skill forbids writing both only in one run. Optional `issue-tracker?` is warn-and-proceed at point of use (`docs/portability-contract.md:78`); a host that continues after a mid-file tracker error records a partial graph and can still look like success.
**Why the spec misses it:** `local` is defined as "the tracker probe itself fails," and the only non-local failures named are "no parent-link capability" and "parent does not resolve." Timeout, auth, and malformed success are not classified. Phase 4's local-file check does not run in tracker modes.
**Suggested fix:** `local` only when the named integration is confirmed not connected. Timeout, non-success status, error-in-success, unreadable schema, and ACL deny are `halt`, before approval and on the pre-write re-probe, with no files and no creates. Bound the probe and each write with a timeout that is `halt`, not `local`. On `native` or `text`, if any `<PARENT-ID>.ticket-*.md` sibling exists, halt and name the paths. Say explicitly that a tracker error after approval is a hard stop, not warn-and-proceed and not a mode switch.

### F-5: The approved mode does not record which tracker was chosen
**Severity:** P1
**Where:** spec.md:38-40 and spec.md:161-166
**Edge case:** Two connected integrations both advertise `blocked_by` (or neither does). The operator names one before approval. The pre-write re-probe asks again, or silently uses the other, and both answers are the mode token `native` (or both `text`).
**What happens:** The mode-token check does not fire. Children and edges are written to the tracker that was not approved. Nothing in the approval block shows the integration name, so the operator cannot see the swap. The phrase "the single issue-tracker integration the operator named" never says where that name is stored.
**Why the spec misses it:** Decision 3 says not to pick silently and to halt if the mode token changes. The token is only `native | text | local | halt`. The printed block has no integration field. The headless rule is specified for the filing prompt, not for this earlier question.
**Suggested fix:** Persist the chosen integration id on the draft. Print it on the `Storage:` line. On re-probe, if the id is missing or different, halt with no writes even when the mode token is unchanged. If the host cannot wait for the "which integration?" question, halt with no writes; do not pick.

### F-6: `blocked_by` does not say which issue is the source
**Severity:** P1
**Where:** spec.md:42 and spec.md:128
**Edge case:** The relation write succeeds, but the edge is stored on the blocker pointing at the dependent (or a `blocking` edge is what the API actually stored).
**What happens:** The frontier is inverted. Pieces the operator was told can run together are the blocked ones, and the skill will not remove or reverse the edge (create-only, and "never also write a `blocking` edge" does not say to verify direction). Text mode is unambiguous (the section sits on the dependent). Native mode is not.
**Why the spec misses it:** Decision 3 says to write type `blocked_by` only and that the name `blocking` does not qualify. It never says the relation is created on the dependent work item and points at the blocker's id. The checklist (spec.md:221) checks that native tickets lack a `Blocked by` section and have a parent, not which way the edge points.
**Suggested fix:** State that each edge is created on the dependent, type `blocked_by`, target = the blocker id. Read it back. If the dependent does not list that blocker, or the blocker lists the dependent, stop with no further edge writes and do not "fix" it by adding the inverse. Add that read-back to the checklist.

### F-7: Existing-child match is not scoped, paged, or single-valued
**Severity:** P1
**Where:** spec.md:124-130
**Edge case:** More children than one result page; two tickets with the same slug; a title the tracker rewrote; a create that returns HTTP success with an error or a null id; a create whose `parent` was dropped; two overlapping runs; a relation or description field omitted from the read.
**What happens:** A short page hides an existing slug, so the run creates a duplicate. Two matches make "the" child undefined, and an edge attaches to one of them. A rewritten title misses the match key and duplicates again. A null id or an ignored `parent` records an orphan that the next run does not see as the child, so it creates another. Two concurrent runs both observe no child and both create; there is no unique constraint and the skill cannot delete. A missing description or relation list treated as "no blockers" skips a child whose approved set is also empty, leaving real edges in place, or halts forever if the sets differ. The slug grammar is not in Decision 5's refusal list, so an illegal slug is approved and then fails the match key on retry.
**Why the spec misses it:** The match key is "the slug token in a title of the form…", singular, with no parent filter, no pagination stop, and no "two matches → halt." Read-back is "if the host cannot read its edges," which does not distinguish absent field from `None — no blockers.` Decision 5's approval refusals omit the slug grammar from Decision 12.
**Suggested fix:** Before any create, list only children of the resolved parent, follow pages until a short page, and parse slugs with an explicit rule (second token, then `:`, must match the slug grammar). Zero matches → create. One match → use that id. Two matches, or a create result with no id, an error payload, or a parent other than the spec's ticket → stop, and do not use that row as the slug's child. Absent body or absent relation list is "cannot read," not an empty edge set. Compare blocker identities as a set. Refuse at approval any slug outside `^[a-z0-9]+(-[a-z0-9]+)*$` or longer than 40 characters. Re-read that slug immediately before each create so overlapping runs do not both pass the check.

### F-8: Approve is not a single defined reply
**Severity:** P1
**Where:** spec.md:64-68 and spec.md:185
**Edge case:** Empty reply, EOF, timeout, `approve`, `yes`, `1 but split the auth piece`, or `1` when option 1 was omitted because storage is `halt` or the draft is not approvable. Also a host that returns immediately without a user channel.
**What happens:** The spec says to wait and lists three choices, but never says which strings file. A revise line that starts with `1`, or an empty read treated as the menu default, takes option 1. Filing is create-only, so those tickets cannot be removed by this skill. "If the host cannot wait" is undefined, so a non-interactive caller can stall on the prompt or be judged able to wait because the tool call returned.
**Why the spec misses it:** Decision 5 names the three choices and the headless sentence, and Phase 3 says option 1 is omitted in some states. It does not say that omission rejects a typed `1`, and it does not define the accept token. The checklist says a headless host writes nothing, without saying how that is detected.
**Suggested fix:** File only on a reply that is exactly `1` after trim, and only when option 1 was printed. Any other text, including a line that starts with `1`, is revise or abort as specified, and does not file. Empty, EOF, and timeout use the existing headless halt and write nothing. Revise must not change `Storage` or reveal option 1; only a new Phase 1 probe can leave `halt`.

### F-9: Phase 4 can file a draft the operator did not approve
**Severity:** P1
**Where:** spec.md:187-191
**Edge case:** The spec file changes after the prompt, or the model re-reads Design and Scope in Phase 4 and redrafts titles, criteria, or edges. Phase 4 re-checks only the cycle rule.
**What happens:** Tickets are created for a graph that was not the approved block. A new cycle is caught; a dropped criterion, a new slug, or a rewritten acceptance line is not. Create-only means the unapproved children stay.
**Why the spec misses it:** Phase 4 says re-probe, refuse a mode change, re-check the cycle rule, then create from the title and body rules. It never says the approved block is immutable input. Decision 5's other refusals (duplicate slug, unknown edge, missing criterion, unassigned Done-when bullet) are not repeated at file time.
**Suggested fix:** Freeze the approved pieces, edges, criteria, and cited anchors as the only Phase 4 input. Do not re-derive from disk. Re-run the full Decision 5 gate on that frozen draft. If the spec file's hash changed since the prompt was rendered, halt with no writes and ask for a new approval.

### F-10: Local rename needs shell, which the skill declares absent
**Severity:** P1
**Where:** spec.md:112-116 and spec.md:192
**Edge case:** A harness that does not expose shell when `shell` is absent (`docs/portability-contract.md:63`). Local mode still requires a temp sibling renamed onto the target. `docs/specs/TODO/` is missing, or the process is killed during a direct write of the target.
**What happens:** The declared capabilities cannot perform the rename. The fallback is a direct write of `<PARENT-ID>.ticket-<slug>.md`. A kill mid-write leaves a truncated file. The next run treats any existing target as reason to halt (F-2), so the truncated body becomes the stored graph. `/spec-brief` declares `shell: true` for this same temp-and-rename (`skills/spec-brief/SKILL.md:130` and its Tool-use notes).
**Why the spec misses it:** Decision 11 forbids `shell` and requires filesystem `write`. Phase 4 requires a rename and does not say what to do when rename is unavailable, nor that a short or heading-less target is not a valid ticket file.
**Suggested fix:** Keep `shell` absent if that decision stands, but state that atomic rename is part of filesystem `write`. If the host cannot rename a temp onto a path that does not exist, `local` is `halt` and the target must not be opened. Never write the target in place. A file that lacks the `local-only` line and the required headings is an incomplete write, not a matching child.

### F-11: Phase 0 deletes temps that Phase 4 does not name
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:147 and spec.md:192
**Edge case:** The temp path is not the `.tmp` glob, or a rename failed after the temp held a finished body. Abort, or a later preflight, runs Phase 0.
**What happens:** Phase 0 deletes `docs/specs/TODO/.<PARENT-ID>.ticket-*.md.tmp` before approval. Phase 4 only says "dot-prefixed temp sibling," so a temp without that suffix is never removed, and a finished temp that matches is destroyed even when the operator aborts. That temp is the only copy of the approved wording if the draft is not frozen yet. This repo does not gitignore `.*.tmp` (`skills/spec-brief/SKILL.md:130`).
**Why the spec misses it:** The two phases do not name one filename. "Abort writes nothing" is already false for this delete, and the delete is unconditional.
**Suggested fix:** Use one path in both phases: `docs/specs/TODO/.<PARENT-ID>.ticket-<slug>.md.tmp`. Phase 0 prints stale temps and does not delete them. Phase 4 removes a temp only after a successful rename of that same slug, and does not delete a temp whose target already exists.

### F-12: Non-bullet Done-when text and uncited Test plan rows never block approval
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:80 and spec.md:155-157
**Edge case:** `## Done when` or `## Test plan` is prose, a table, or a second heading (including one inside a fence). A Test plan row is not cited by any criterion and is not assembled-only. Duplicate `## Done when` sections.
**What happens:** "Every Done-when bullet" is vacuously true when nothing is parsed as a bullet, so the block shows `Unassigned: none` and the prose obligations are dropped. A test row that no criterion cites disappears with no line in the prompt. Headings are specified as "the spec contains" those strings, so a fenced example can satisfy a missing section, and a second real section can be ignored. `/spec-cycle` requires Done when to be a bullet list (`skills/spec-cycle/SKILL.md:308`).
**Why the spec misses it:** Decision 6's gate is bullets and citations, and the approval block has no unassigned-test-row line. Decision 7 does not say headings are unique ATX level-2 lines outside fences.
**Suggested fix:** Require one real level-2 heading per required name, outside fences; two of the same name halts. List items and table rows are the assignable units; if Done when has none, halt, do not approve. A Test plan row that is neither cited nor assembled-only is listed under `Unassigned` and blocks option 1, same as a Done-when bullet.

### F-13: `project_root` is cwd, and the spec path is only a filename pattern
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:77-80 and spec.md:145-147
**Edge case:** The skill is invoked from a subdirectory, or with an absolute path whose basename matches `<TICKET-ID>.spec.md` but which is not `docs/specs/TODO/<TICKET-ID>.spec.md`. The id regex is an unanchored prefix of the stem, so `VHS-45.notes.spec.md` can yield `VHS-45`.
**What happens:** Local files are written to `cwd/docs/specs/TODO/`, which may be the wrong tree or may not exist (the write then fails mid-set). A copy of the spec outside TODO is ticketed as the parent. `/ship-spec` and `/spec-close` both require the TODO path shape (`skills/ship-spec/SKILL.md:15`, `skills/spec-close/SKILL.md:26`).
**Why the spec misses it:** Decision 7 checks the file name. Phase 0 sets `project_root` to cwd and says "resolve under it," without a containment check. `/spec-close` uses the directory that contains `CLAUDE.md`, not cwd.
**Suggested fix:** Resolve the repo root by walking up to `AGENTS.md` or `CLAUDE.md`. Accept only `<root>/docs/specs/TODO/<TICKET-ID>.spec.md` with the ticket regex end-anchored (`^[A-Z][A-Z0-9]*-[0-9]+$`). Anything else, including `..`, halts with the usage line and writes nothing.

### F-14: Ticket bodies and local files have no size bound or format version
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:86-88 and spec.md:191-192
**Edge case:** A piece whose rendered body is larger than the tracker accepts, or a later edit to the body shape read back as edges.
**What happens:** Decision 9 forbids a fan-out cap, not a field cap. An oversized create fails mid-batch and hits the F-1 stop. A later reader that still string-matches `Blocked by` can false-skip or false-halt on a changed layout. There is no `status=complete` beyond the rename, and no version token.
**Why the spec misses it:** The persistence rules in Decision 12 cover create-only and temp rename. They do not bound the body or version the local file.
**Suggested fix:** Refuse approval when any rendered body exceeds 32 KiB (this is a field cap, not a piece cap). Put `Format: spec-tickets/1` under the title. On read-back, an unknown or missing format is "cannot read edges" (halt), not an empty edge set.

### F-15: Deferred-row count is undefined
**Severity:** P3
**Where:** spec.md:80 and spec.md:167
**Edge case:** `## Deferred — follow-up required` contains prose, a fenced example, or `### D-<n>:` headings.
**What happens:** `Deferred rows not filed: <n>` can be 0 while deferred rows exist, or a prose paragraph can be counted as a row. Nothing is filed from the section either way; the operator is told the wrong count.
**Why the spec misses it:** Decision 7 says rows are counted and not filed, and does not define a row.
**Suggested fix:** Count only `### D-<n>:` headings outside fences. If the section exists and the count is zero, print `Deferred rows not filed: 0 (no D-<n> headings)`.

### F-16: Plane ticket text was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45`.
**What happens:** The call returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. The review used the brief and the repo. No ticket body beyond the brief was checked.
**Why the spec misses it:** Not a spec defect. Recorded because the ticket lookup was blocked.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read `skills` if the ticket text must be confirmed.

## Summary
P0: 2 | P1: 8 | P2: 4 | P3: 1 | P4: 1

STATUS: RED P0=2 P1=8 P2=4 P3=1 P4=1
