# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Native retry cannot finish a partial graph
**Severity:** P0
**Where:** spec.md:129 | spec § Decision 12
**Claim:** "If a child for that slug already exists and the recorded edges match the approved set, skip it. If they differ, or the approved graph drops an existing slug, halt with no further creates. This skill does not repair a graph." The next bullet says a failed edge write stops the run and "A later run resumes under the create-only rules."
**Why this is wrong:** Decision 3 (spec.md:52) files every child before any `blocked_by` edge, and Decision 12 (spec.md:128) writes those edges only after the children exist. After a failed edge write, or a failed create once any already-created piece has a blocker, each existing child has an empty relation set. That set differs from the approved blockers, so the same rules halt with no further creates and refuse to repair. The resume the failed-edge bullet promises never lands the missing edges, and it also refuses the children not created yet. The named capabilities (spec.md:141) are only a liveness probe, retrieve-by-identifier, create-with-parent, and blocking-relation create. There is no child lookup and no relation read, which spec.md:124 and spec.md:130 both require in order to decide skip versus halt.
**Suggested fix:** Specify three outcomes, in this order: create every missing slug first; then write only approved `blocked_by` edges that are not already present; halt with no further writes only when an existing edge is outside the approved set or an existing slug is not in the approved graph. State that an empty relation set means "not written yet," not "differs." Name the two reads: list the parent's children (match the title form in spec.md:124) and read back `blocked_by`. Say text mode does not use this path because the section is written at create time.

### F-2: Local files are specified both with and without Blocked by
**Severity:** P0
**Where:** spec.md:191 | spec § Phase 4 — File
**Claim:** Body sections are Parent, Spec, Delivers, Acceptance criteria, Assembly, "and on `text` only, Blocked by." Local mode is "the same body, plus a status line `local-only`."
**Why this is wrong:** Decision 12 (spec.md:128) says the edge record on `text` and `local` is the `Blocked by` section: blocking titles, or `None — no blockers.` The Done when bullet (spec.md:242) says the local file's `Blocked by` section is the relation list, not an order. Phase 4 is the operative body. Followed literally, an unreachable tracker writes pieces with no dependency record, so the local row of Decision 3 does not satisfy that Done when bullet.
**Suggested fix:** Change "on `text` only" to "on `text` and `local`." Say the local body is those sections plus the `local-only` status line, and that its `Blocked by` entries are the same list Decision 12 specifies.

### F-3: Two trackers ask a question the skill cannot accept
**Severity:** P1
**Where:** spec.md:40 | spec § Decision 3
**Claim:** "If more than one connected integration can create work items, halt before approval and ask which one. Do not file to both and do not pick silently."
**Why this is wrong:** Invocation is `/spec-tickets <spec-path>` with no flags (spec.md:30). Phase 1's `halt` only suppresses option 1 (spec.md:151). The approval block (spec.md:180–183) offers approve, revise, or abort, and no integration name. Nothing re-probes a named integration or carries the answer into Phase 4. The brief already treats plane-proxy and the official Plane tool set as both present (`VHS-45.brief.md:46`). Both can create work items, so this host takes the halt branch, and the skill as written cannot file the Plane children the Done when requires.
**Suggested fix:** Add a pre-approval choice that lists the connected create-capable integrations, waits for one, re-runs the Decision 3 probe against that one, and only then prints the approval block with `native` or `text`. State that a headless host still halts with no writes.

### F-4: blocked_by endpoints are not pinned
**Severity:** P1
**Where:** spec.md:42 | spec § Decision 3
**Claim:** "Write `blocked_by` only. Never also write a `blocking` edge." Decision 12 (spec.md:128) adds those edges after the children exist, and the text/local record is "a list of blocking titles."
**Why this is wrong:** The relation is the dependency graph the brief says decides parallelism (`VHS-45.brief.md:40`). The spec never says which work item is the subject and which is the blocker. A create call of the form `(issue, related_issue, blocked_by)` can be passed either way and still "write `blocked_by` only," which inverts the frontier. "Blocking titles" is also not the match key from spec.md:124, so a text or local list can name the short title, the full title, or the slug.
**Suggested fix:** Pin one shape: on the dependent child, one `blocked_by` relation whose target is the blocker child; do not create the inverse. Pin the text and local list to the full title `<PARENT-ID> <slug>: <short title>`, or to the slug, and use that same token in the match check.

### F-5: project_id lookup is not the spec-brief lookup
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:125 | spec § Decision 12
**Claim:** "Resolve `project_id` from the installed `skills/ship-spec/states.json` … by ticket prefix, the same lookup `/spec-brief` uses." A missing file or an unknown prefix halts tracker modes.
**Why this is wrong:** `/spec-brief` reads that file for `namespace`, and a missing file or an unknown prefix is a warning that falls back to `namespace = "plane"` (`skills/spec-brief/SKILL.md:53`). `project_id` plus halt-on-unknown-prefix is `/ship-spec` Phase 0 step 9 (`skills/ship-spec/SKILL.md:41`), whose path does not consult `$CLAUDE_CONFIG_DIR`. The config-dir order in the spec does match `/spec-brief` and `/spec-close` (`skills/spec-close/SKILL.md:31`), but spec-close warns and forces partial-close instead of halting. Copying the cited lookup would file without a project id, or not halt.
**Suggested fix:** Cite `/spec-brief` only for the config-dir path. Cite `/ship-spec` Phase 0 step 9 for the prefix → `project_id` field and for halting when the prefix is missing. Keep the spec's own halt for tracker modes.

### F-6: The test command does not cover every leave-alone path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:213 | spec § Test plan
**Claim:** "`git diff --name-only origin/main --` the leave-alone paths in Scope prints nothing."
**Why this is wrong:** The command that must exit 0 (spec.md:236) lists the skill files, the three docs, `sync.py`, `states.json`, `agents`, and the four test modules other than `tests/test_lint.py`. Those four are the whole `tests/` set besides the census file. It does not list the historical notes Scope says to leave alone (spec.md:24): `docs/compound-engineering-evaluation.md` and `docs/cross-harness-spike-synthesis.md`. Both files exist. An edit there still leaves the third command empty.
**Suggested fix:** Add both paths to the `git diff` command, or narrow the Test plan sentence to the paths the command actually names.

### F-7: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec implements Plane ticket VHS-45. The brief says its Done when block is transcribed from the ticket.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45` returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. No ticket body was available. Review used the brief only. If the ticket's acceptance criteria differ from the brief, that conflict was not checked.
**Suggested fix:** Re-cache the work item into a namespace this reviewer can read, or paste the ticket acceptance criteria into the brief if they are not already the transcribed Done when list.

## Summary
P0: 2 | P1: 2 | P2: 2 | P3: 1 | P4: 0

STATUS: RED P0=2 P1=2 P2=2 P3=1 P4=0
