# VHS-45 — Decompose a green-lit spec into dependency-linked tickets

## Goal

Add an optional lifecycle stage, `/spec-tickets`, that reads one green-lit spec, breaks it into verifiable pieces with blocking edges, stops for operator approval, and only then files each piece as a child of the spec's ticket. The dependency graph is the tracker's blocking relations when the host can write them, a `Blocked by` section when it cannot, or one local file per piece when no tracker is connected. `/ship-spec` stays one worktree, one branch, and one PR, and this ticket does not teach it to read the children.

## Scope

| Path | Change |
|------|--------|
| `skills/spec-tickets/SKILL.md` | Create. The skill body specified in Design. |
| `AGENTS.md` | Name `/spec-tickets` as an optional stage between `/spec-cycle` and `/ship-spec`. |
| `README.md` | Same placement in the skills list, the opening workflow line, and Requirements. |
| `docs/spec-workflow-reference.md` | Opening sentence plus one optional-stage section. Do not renumber Skill 2 or Skill 3. |
| `tests/test_lint.py` | `test_shipped_skills_clean`: set the census integer and its message from 8 to the post-change count (12 on 2026-10-08). |

Leave alone:

- `skills/ship-spec/SKILL.md`, `skills/spec-cycle/SKILL.md`, `skills/spec-close/SKILL.md`
- `docs/portability-contract.md`, `docs/customizing.md`, `docs/authoring-portable-skills.md`
- `sync.py` (`SUBTREES` already mirrors `skills/`), `skills/ship-spec/states.json`, `agents/`
- Every test file other than `tests/test_lint.py`
- The spec being decomposed. The skill reads it and does not write it.
- Historical notes (`docs/compound-engineering-evaluation.md`, `docs/cross-harness-spike-synthesis.md`). They are not the lifecycle list.

## Decisions

### Decision 1 — A new stage between `/spec-cycle` and `/ship-spec`

Brief Decision 1. The breakdown is its own user-invoked skill. It is not a section of the spec and not a mode of `/ship-spec`. Invocation is `/spec-tickets <spec-path>` with no flags. An unknown flag, a missing path, a brief path, a bare ticket id, or a conversation halts with a one-line usage string and writes nothing.

### Decision 2 — One integration branch and one PR per spec

Brief Decision 2. Every filed piece carries an Assembly paragraph: the piece lands on the parent spec's single integration branch and single PR, and it does not open a PR of its own. This skill does not create the branch, the worktree, or the PR. No piece is an "integrate and verify" ticket. The spec's full Done when and the Codex gate are that check, and they run once on the assembled PR (Decision 6).

### Decision 3 — The tracker holds the graph, in three mutually exclusive modes

Brief Decision 3. Check the host's tracker once, read-only, before the approval prompt, and show the mode in that prompt. One integration per run.

| Mode | When | What is written |
|------|------|-----------------|
| `native` | An issue-tracker integration is connected, the parent ticket resolves through it, it can create a work item with a parent, and it offers an operation that creates a blocked-by relation between two work items | Child work items of the parent, plus one blocked-by relation per edge. No `Blocked by` section. No local files. |
| `text` | The same, except it offers no such relation operation | Child work items of the parent, each with a `Blocked by` section. No relation writes. No local files. A host whose tracker tools set a parent and nothing else is this row. |
| `local` | No issue-tracker integration is connected. This is the only `local` trigger | One file per piece at `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md`, including `Blocked by`. No tracker writes. |
| `halt` | An issue-tracker integration is connected, and the Phase 1 probe or the parent retrieve does not answer or returns an error, or no connected integration can create a work item with a parent | Nothing. |

`halt` is not `local`. portability-contract §3 lets an unavailable optional service warn and proceed. This skill halts instead, because local files beside a live tracker are a second graph. This narrows the brief's "no tracker reachable" to "no integration connected". The `requires:` block does not change.

If more than one connected integration can create a work item with a parent, stop before the approval block, print their names, and wait for the operator to name one. A reply that is not one of those names, an empty reply, or a host that cannot wait halts with no writes. The chosen name is part of the approved draft.

Storage line, one grammar. `native` and `text` print `Storage: <mode> via <name>`. `local` prints `Storage: local` and has no `via`. `halt` prints `Storage: halt via <name or none> (<reason>)`.

Each `native` edge is one relation, created on the dependent child, of the blocked-by kind, with the blocker child as its target. Do not also create the inverse relation. An integration that offers only the inverse kind is `text`.

A `Blocked by` section is a list of references, one per line, or the single line `None — no blockers.` On `text` a reference is the blocker's tracker identifier and its title. On `local` it is the blocker's file name and its title. Filing blockers first (Decision 12) is what makes those identifiers exist. In the approval block, before anything is filed, blockers are shown by slug. The section is a relation list, not a numbered procedure.

A child's tracker name, and a local file's H1, is the piece's short title as the approval block shows it. The slug appears only in the approval block and in the local file name.

The mode is fixed for the run. A tracker error after approval stops the run (Decision 12). It does not switch the mode, and it does not fall back to local files.

### Decision 4 — Reference shape, cut only from the spec

Brief Decision 4, bounded by Decision 7. Where this brief states no rule of its own, the pieces follow the reference shape: a vertical slice that is verifiable alone and small enough for one context window, prefactoring ahead of the slice it unblocks, expand–contract for a wide refactor, and a pointer to the spec instead of a copy of it. The skill text is original. It does not quote or vendor the reference skills, and it does not reuse these phrases: "tracer bullet", "Make the change easy, then make the easy change.", "ready-for-agent", "What to build", or a `.scratch/` layout.

Decision 7 wins on inputs. The skill does not explore the repo for extra work. A prefactor piece exists only when the spec's Design already calls for a seam, and that piece is still verifiable. Expand–contract is proposed only when the spec's Design is one mechanical change across many Scope rows: one expand piece, one or more migrate pieces blocked by expand, one contract piece blocked by every migrate piece. The skill does not add a final integrate ticket (Decision 2, Decision 6).

A horizontal slice (a layer with no end-to-end outcome) is not a legal piece. Each piece has at least one acceptance criterion.

"One context window" is this sizing rule. It is not a token budget, a batch size, or a fan-out cap (Decision 9).

### Decision 5 — Stop for approval; never file headless

Brief Decision 5. After the draft and the storage probe, print the breakdown and wait. There is no `--yes` and no environment-variable bypass.

File only when option 1 was printed and the reply, after trim, is exactly `1`. A reply of exactly `3` aborts and writes nothing. Any other non-empty reply, including a line that starts with `1` but is longer, is revise: re-render, do not file, and do not change the storage mode. Only a new Phase 1 probe can leave `halt`. Empty reply, EOF, timeout, or a host that cannot wait: print `approval required — this skill does not file headless` and write nothing. A typed `1` when option 1 was omitted does not file.

Option 1 is omitted, and approval is refused, while the draft has a cycle, a self-edge, a duplicate slug, a slug outside `^[a-z0-9]+(-[a-z0-9]+)*$` or longer than 40 characters, an edge to an unknown slug, a piece with no acceptance criterion, or a Done-when bullet or Test plan row that is neither assigned nor marked assembled-only.

### Decision 6 — Each piece has its own acceptance criteria

Brief Decision 6. Criteria are one line each, drawn from the spec's Done when and Test plan, and each line cites the bullet or row it comes from. The ticket does not paste Design, Test plan prose, or code. No code blocks in a ticket body.

Assignable units are list items and table rows under the one real `## Done when` and the one real `## Test plan` (Decision 7). If Done when has neither, halt and do not approve. Every such unit is assigned to exactly one piece, or marked assembled-only. The default assembled-only items are the spec's full Done when taken as a whole, and the Codex gate. Those two are named in every piece's Assembly paragraph and are not a child's criteria. Anything else the draft cannot place is listed as unassigned and blocks option 1 until revise assigns it or the operator marks it assembled-only.

### Decision 7 — The only input is the spec file

Brief Decision 7. The repo root is cwd when cwd contains `AGENTS.md` or `CLAUDE.md`. Otherwise it is the nearest ancestor of cwd that contains one of those files. The only accepted path is `<root>/docs/specs/TODO/<TICKET-ID>.spec.md`, where the stem before `.spec.md` is the whole ticket id `^[A-Z][A-Z0-9]*-[0-9]+$`. Normalize separators, and accept a path when it canonicalizes to that file. A prefix of a longer stem does not match. Anything else, including `..`, halts with the usage line and writes nothing.

The skill reads that file and nothing else for the breakdown. It does not read the sibling brief, the reviews tree, or the conversation as a source of pieces.

Green-lit means each of `## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Test command`, `## Done when`, and `## Out of scope` occurs once as a level-2 heading outside a fenced block. A missing heading or a second heading of the same name halts. The skill does not re-run reviewers. If `docs/specs/TODO/<TICKET-ID>.reviews/` is absent, warn once and continue.

Rows under `## Deferred — follow-up required`, when that section exists, are not filed. Count only `### D-<n>:` headings outside fences. If the section exists and that count is zero, print `Deferred rows not filed: 0 (no D-<n> headings)`.

### Decision 8 — The stage is optional, and `/ship-spec` is unchanged

Brief Decision 8. Not invoking the skill is the skip. A spec with no children still ships through `/ship-spec` exactly as today. This ticket does not edit `skills/ship-spec/SKILL.md`, and the skill does not tell `/ship-spec` to read child tickets. Each child's Assembly paragraph says the parent `/ship-spec` run ignores children until a later executor ticket.

### Decision 9 — Scale is a non-factor

The brief's `## Scale` sets `**Factor:** no`. The skill adds no batching, no fan-out cap, no token budget, and no per-tenant state. Decision 4's slice-size sentence is the only limit, and it is a decomposition rule.

### Decision 10 — Which docs gain the stage

Risk 1, pinned from the tree on 2026-10-08.

- `AGENTS.md` lists the stages as a numbered workflow ("Four skills form the spec lifecycle", `/ship-spec` at item 3). Insert `/spec-tickets` as the optional third stage and renumber `/ship-spec` and `/spec-close`. The opening sentence names five skills and says the third is optional. Under External dependencies, keep the memory-read sentence for the skills that still read tickets that way (`/spec-brief`, `/spec-cycle`, and `/spec-close`'s PR lookup). Add one sentence: `/spec-tickets` resolves the parent on the tracker itself, because that read is a create precondition, and it does not consult shared memory. It uses the tracker when one is connected and the Decision 3 probe succeeds, writes local files only when no issue-tracker integration is connected, and halts otherwise. It does not claim plane-proxy grew relations.
- `README.md` lists the same commands and opens with "brief → spec → review → ship → close". Place `/spec-tickets` between `/spec-cycle` and `/ship-spec`, mark it optional, and change that line to `brief → spec → review → (optional tickets) → ship → close`. Add one Requirements bullet in the existing scoped shape: `For /spec-tickets: an operator is required at approval; the tracker is optional (local files only when no issue-tracker integration is connected); gh is not required.` That bullet does not change the `/spec-cycle`, `/ship-spec`, `/spec-close`, or `/review-pr` bullets, and it does not change the `gh` sentence under AGENTS.md External dependencies.
- `docs/spec-workflow-reference.md` opens "Four AI-driven skills" and numbers Skill 0 through Skill 3. Change the opening sentence so the optional stage is visible. Insert `## Optional stage: spec-tickets` between Skill 1 and Skill 2. Leave the Skill 2 and Skill 3 headings in place. The new section is a summary (purpose, invocation, approval gate, the three modes, ship-spec unchanged) and points at `skills/spec-tickets/SKILL.md` for the steps. In that summary say "unblocked pieces". Do not use "frontier" for that set. The document already uses frontier for the grilling interview.
- `docs/portability-contract.md` does not list the stages. It uses `spec-cycle` as the worked `requires:` example. No edit.
- `docs/customizing.md` and `docs/authoring-portable-skills.md` do not list the stages. No edit.

### Decision 11 — The lint census is set to the tree this change ships

Risk 2, pinned from `tests/test_lint.py` (`test_shipped_skills_clean` expects `len(skills) == 8`).

On 2026-10-08 the tree has 11 `skills/*/SKILL.md` files: `bloat-check`, `grill-me`, `grilling`, `hermes-kanban-awareness`, `review-pr`, `session-handoff`, `ship-spec`, `spec-brief`, `spec-close`, `spec-cycle`, `talaria`. The assertion is already false on this tree. `tests/test_session_handoff.py` only checks that `session-handoff` is a member; it does not encode a count.

This change adds `spec-tickets`, so the expected integer becomes 12, and the message's "8 currently-shipped" becomes "12 currently-shipped". The assertion stays a census of `skills/*/SKILL.md`, not an increment of the stale 8. If the worktree's measured count at implementation differs, use the measured count and say so in the PR; do not leave the assertion at 8 or 9. No other edit to that test. No new test module. VHS-42's other work is not this ticket.

The new skill's `requires:` block is exactly:

```yaml
requires:
  filesystem: [read, write]
  services: [issue-tracker?]
```

`shell`, `network`, `subagents`, and `shared-memory` stay absent. `user_invocable: true`. Frontmatter keys are `name`, `description`, `user_invocable`, `requires`, in that order. `python lint.py --strict` ignores WARNs, so the test gate asserts zero ERROR, zero WARN, and this exact `requires:` key set.

### Decision 12 — File in dependency order, create-only, with no resume

Risk 3. The native relation path has been seen as a schema only. Nothing in the lifecycle has created a relation through it. The first live `native` run is the proof. This skill does not read its own writes back; the operator checks the result in the tracker's own view.

Operator decision, 2026-10-08, after review round 4. Rounds 1 to 4 grew a read-back and resume protocol in this decision, and that protocol pinned one tracker's response shapes. It is removed. Filing follows the reference shape: publish blockers first, then stop.

**Parent.** On `native` and `text`, Phase 1 resolves the parent through the integration's retrieve-by-identifier capability. Create uses the parent reference, and the project reference when one is needed, that the integration's own create operation takes, both from that retrieve. If the retrieve fails, or lacks a reference the create needs, storage is `halt` before approval. The skill does not consult shared memory and does not read `states.json`: the parent retrieve already carries the project, and `states.json` holds one host's state ids, which a create-only skill does not need.

**Order.** File blockers first: a piece is filed only after every piece that blocks it. Among pieces that are ready together, use the approval block's order. File one piece at a time. Create the child. On `native`, then create that child's relations; its blockers already have identifiers. On `text` and `local`, the `Blocked by` section in the body carries the references the earlier creates returned. This order exists so that identifiers exist. It is not a build order, it is not written into any ticket, and it is not what decides which pieces can run together.

**Create-only.** Do not edit a ticket, delete a ticket, remove a relation, or change any ticket's state, including the parent's. A new child keeps the tracker's create default state.

**Failure.** When a create or a relation write returns an error, or a create returns no identifier, stop at once. No further writes, no retry, no mode switch. Print a stop report: each piece as `created <identifier or path>` or `not created`, each edge as `written` or `not written`, then the operation that failed and the error as the integration returned it. A stopped run does not print `FILED`. The operator files the rest by hand from that report, or deletes what was created and runs again.

**No resume.** A second run for the same spec does not find, reuse, or compare an earlier run's children. On a tracker it files every approved piece again. The guard is the operator. Phase 1 makes one read for existing work: the parent's children when the integration can list them, and the files matching `docs/specs/TODO/<PARENT-ID>.ticket-*.md`. The approval block reports those counts, or `unknown` when the read is not available or fails. The count is a notice, not a census. A count above zero adds one line saying that approval files these pieces in addition to what exists.

`local` never overwrites. If the target path of any approved slug already exists, option 1 is omitted and the block names those paths. A target that appears between approval and the write is a failure stop, as above.

plane-proxy is not given a relation tool.

## Design

### Skill outline

`skills/spec-tickets/SKILL.md` sections, in order: frontmatter, title and the one-paragraph contract, Invocation, Phase 0 — Preflight, Phase 1 — Storage probe, Phase 2 — Draft, Phase 3 — Approval, Phase 4 — File, What `/spec-tickets` never does, Tool-use notes, Failure modes.

Operative steps name capabilities (retrieve-by-identifier, list children of a parent, work-item create with parent, create a blocked-by relation on the dependent). A harness tool name appears only as a tagged example with "or the equivalent in your host", or as declarative text under Tool-use notes. The skill names no tracker response field. Do not invent a relation-tool identifier in the skill; Phase 1 reads whatever the named integration actually offers.

The never-does list: edit the spec; edit `/ship-spec`, `/spec-cycle`, or `/spec-close`; create a branch, worktree, or PR; transition or rewrite the parent; dispatch an implementer; file from a brief, a ticket id, or a conversation; file headless; write both tracker records and local files; write the inverse of a blocked-by relation; delete or update a ticket; overwrite a local ticket file; resume or repair an earlier run.

### Phase 0 — Preflight

Resolve the repo root and the spec path per Decision 7. Read the spec. Require the seven headings. Print one preflight line: ticket id, headings ok, reviews present or absent.

### Phase 1 — Storage probe

Read-only. Produces `native`, `text`, `local`, or `halt`, plus the reason and the integration name when there is one. On a tracker mode it also resolves the parent. On every mode except `halt` it makes the one existing-work read (Decision 12). `halt` still allows the draft to be shown. It does not allow option 1.

### Phase 2 — Draft

From Design and Scope only, draft the fewest pieces that satisfy Decision 4. Assign each Done-when unit and each Test plan row per Decision 6. A Test plan row follows the piece whose criterion cites it. A row that only the assembled PR can satisfy is assembled-only.

Pieces are named by slug. Those names are not an execution order. Do not label pieces `P1`, `P2`, or any other severity token.

### Phase 3 — Approval

Print:

```text
SPEC TICKETS: <PARENT-ID>
Spec: <path>
Storage: <native or text> via <name> | local | halt via <name or none> (<reason>)
Deferred rows not filed: <n>
Existing under parent: <n children or unknown>, <n local ticket files>
<when either count is above zero: Approving files these pieces in addition to what exists.>
<when a local target exists: Cannot file — these paths exist: <paths>>

Pieces:
- <slug> — <title>
  Delivers: <one paragraph>
  Acceptance: <one line per criterion, with spec anchor>
  Blocked by: <slugs, or None — no blockers.>
Unblocked (can run together; not an execution order; not the grilling frontier): <slugs>
Waiting: <slug> blocked by <slugs>
Done-when assigned: <bullet → slug>
Done-when assembled-only: <bullets>
Unassigned: <bullets or none>

1. Approve and file
2. Revise — say what to merge, split, or re-edge
3. Abort — nothing filed
```

Option 1 is omitted when storage is `halt`, when the draft is not approvable (Decision 5), or when a `local` target already exists (Decision 12). Replies are matched by Decision 5. The block that was printed, not a later re-read of the spec, is what approval freezes. The Storage line uses the Decision 3 grammar, not a second one. `None — no blockers.` in this block is the empty edge set.

### Phase 4 — File

If the spec file's contents changed since the block was printed, halt with no writes and ask for a new approval. The frozen pieces, edges, criteria, and anchors are the only input. Do not redraft from Design. Re-run the Decision 5 gate on that frozen draft, then file in the Decision 12 order.

Body sections, in order: Parent (the parent's identifier), Spec (path plus section anchors only), Delivers (one paragraph), Acceptance criteria (the checklist), Assembly (Decision 2 and Decision 6). On `text` and `local`, add Blocked by with the Decision 3 references, or the sentinel when the set is empty. `local` puts `local-only` on the line after the H1. `native` omits Blocked by. Send the body as the integration's description field.

`local` writes `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md`. It never overwrites an existing file (Decision 12). A file write that fails is a Decision 12 failure.

Do not touch the parent. Do not set a state on a new child beyond the tracker's create default.

Print `FILED: <PARENT-ID>` only when every create and every relation write returned success. Include the mode, the integration name, the counts, the created identifiers or paths, and the unblocked set. A stopped run does not print `FILED`.

The local filename matches `/spec-close`'s existing companion rule (`<TICKET-ID>.<rest>` → `<rest>`), so a later close can archive `ticket-<slug>.md` without a change to that skill. This spec does not change the closer.

### Doc edits

Decision 10 is the whole edit. Do not restate phase text into `AGENTS.md` or `README.md`. The workflow reference section stays a summary.

### Census edit

Decision 11 is the whole edit to `tests/test_lint.py`.

## Test plan

Mechanical gate:

1. `python tests/test_lint.py` exits 0. `test_shipped_skills_clean` sees 12 skills (or the measured census from Decision 11) and zero ERROR findings, including `skills/spec-tickets/SKILL.md`.
2. A programmatic lint of `skills/spec-tickets/SKILL.md` finds zero ERROR and zero WARN, and the `requires:` keys are exactly `filesystem` and `services` with value `issue-tracker?`.
3. `git diff --name-only origin/main --` the leave-alone paths in Scope, including the two historical notes, prints nothing.

Review the new skill against this checklist. The mechanical gate does not cover it:

- Invocation rejects a brief path, a bare id, a non-TODO path, and an unknown flag without writing. Invoked from the repo root, that directory is the root when it contains `AGENTS.md` or `CLAUDE.md`.
- A spec missing one required heading, or carrying two of one name, halts without writing.
- The approval block appears before any tracker create and before any local file. Only an exact `1`, and only when option 1 was printed, files.
- A cycle, an illegal slug, an unassigned Done-when bullet or Test plan row, and a headless host each refuse filing and write nothing.
- `native` edges are on the dependent and target the blocker, with no inverse relation. `native` tickets have no `Blocked by` section. `text` and `local` tickets have the section and no relation write. A `text` reference is the blocker's tracker identifier and title; a `local` reference is the blocker's file name and title. The tracker name and the local H1 are the piece's short title. `local` is taken only when no issue-tracker integration is connected. A connected integration that cannot create with a parent, or that does not answer, is `halt`, not `local`.
- An integration with no blocked-by relation operation, or with only the inverse kind, takes `text`. A tracker error after approval stops the run. It does not switch the mode and does not write local files.
- A parent that does not resolve halts and does not write local files.
- Two create-capable integrations require an exact name before approval. The Storage line shows that name.
- Pieces are filed blockers first, one at a time. A failed create or relation write stops the run with no retry. The stop report lists each piece as created or not created and each edge as written or not written, gives the failing operation and its error, and does not say `FILED`.
- The skill has no read-back step, no resume step, and no compare of stored tickets against the draft. It says that a second run on a tracker files every piece again. The approval block reports the count of existing children or local ticket files, or `unknown`.
- `local` omits option 1 when a target file for an approved slug already exists, and names the paths.
- The skill body names no tracker response field and contains no operative `mcp__` tool call.
- `skills/ship-spec/SKILL.md` has no diff.

## Test command

Run each command from the repo root. Each must exit 0. The third must print no paths.

```
python tests/test_lint.py
python -c "import lint,re; from pathlib import Path; p=Path('skills/spec-tickets/SKILL.md'); t=p.read_text(encoding='utf-8'); f=lint.lint_path(p); e=[x for x in f if x[0]==lint.ERROR]; w=[x for x in f if x[0]==lint.WARN]; assert not e, e; assert not w, w; fm=t.split('---',2)[1]; req=fm.split('requires:',1)[1]; keys=re.findall(r'(?m)^  ([a-z-]+):', req); assert keys==['filesystem','services'], keys; assert 'issue-tracker?' in req; assert 'shell:' not in req and 'network:' not in req and 'subagents:' not in req and 'shared-memory' not in req"
git diff --name-only origin/main -- skills/ship-spec/SKILL.md skills/spec-cycle/SKILL.md skills/spec-close/SKILL.md docs/portability-contract.md docs/customizing.md docs/authoring-portable-skills.md docs/compound-engineering-evaluation.md docs/cross-harness-spike-synthesis.md sync.py skills/ship-spec/states.json agents tests/test_session_handoff.py tests/test_spec_close_log.py tests/test_talaria_bridge.py tests/test_talaria_watch.py
```

## Done when

- A new vigil-skills skill decomposes an approved spec into pieces. — `skills/spec-tickets/SKILL.md` Phases 0–4, gated by `python tests/test_lint.py` and the programmatic lint.
- Each piece is ticketed, and the dependencies are relationships rather than an ordered list. — Decision 3's three modes. On a reachable tracker the piece is a Plane child (`native` or `text`). `local` is only the not-connected row of that same decision, and its `Blocked by` section is still a relation list, not an order.
- The dependency graph, not a build order, decides what can run in parallel. — The approval block's unblocked set, and Decision 12's rule that the blockers-first filing order is not a build order. Native edges point from the dependent to the blocker.
- The published reference skills supply the shape, and that shape is what shores up `/ship-spec`. — Decision 4's slice rules, plus Decision 2's Assembly paragraph on every piece. `/ship-spec` is shored up by receiving pieces that already fit its one branch and one PR. Its file is not edited (Decision 8).

## Out of scope

- Any edit to `skills/ship-spec/SKILL.md`. Running pieces in parallel, one implementer per unblocked piece, merger agents, and worktrees per piece are a follow-up. This skill does not design that executor.
- Adding a relation capability to plane-proxy. A proxy host takes the `text` mode.
- Porting the reference repo's `tdd` or `code-review` skills. The pre-commit review step is VHS-46.
- Any input other than a spec file.
- Writing a task graph into the spec, or teaching the review lenses to check the breakdown.
- Migrating `/ship-spec` or `/spec-close` off plane-proxy.
- Editing, deleting, or transitioning tickets that already exist. Create-only (Decision 12).
- Resuming or repairing a partial filing, reading writes back, and matching an earlier run's children to pieces. The existing-work count is a notice only. A second run on a tracker files again, and a second `local` run is refused (Decision 12).
- Filing the spec's deferred-follow-up rows as pieces.
- Changing `sync.py`, `states.json`, `docs/portability-contract.md`, or the tests other than the census integer in `tests/test_lint.py`.

## Deferred (P2+)

- edge-cases/R1/F-14 — No body-size cap and no format token on the ticket body. Not folded: a 32 KiB cap and a `Format: spec-tickets/1` line would be new machinery beside Decision 9's non-factor note. An oversized create is not assumed to fail. If the tracker rejects it, that is a Decision 12 failure stop.
