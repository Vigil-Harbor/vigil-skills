---
name: spec-tickets
description: Optional stage between /spec-cycle and /ship-spec. Break one green-lit spec into verifiable pieces with blocking edges, stop for operator approval, then file each piece as a child of the spec's ticket — blocked-by relations where the tracker has them, a Blocked by section where it does not, one local file per piece when no tracker is connected. Never files headless. Does not change how /ship-spec runs.
user_invocable: true
requires:
  filesystem: [read, write]
  services: [issue-tracker?]
---

# /spec-tickets — break a green-lit spec into dependency-linked tickets

Invoked as:

```
/spec-tickets <spec-path>
```

This skill reads one green-lit spec, drafts the fewest pieces that can each be verified alone, records which pieces block which, and stops for the operator. Only after approval does it file each piece as a child of the spec's ticket. The dependency graph lives in the tracker, not in the spec and not in an ordered list.

The stage is optional. Not invoking it is the skip: a spec with no child tickets ships through `/ship-spec` exactly as before.

## Invocation

- `<spec-path>` is the only argument. There are no flags.
- The repo root is the current directory when it contains `AGENTS.md` or `CLAUDE.md`; otherwise it is the nearest ancestor that contains one of them.
- The only accepted path is `<root>/docs/specs/TODO/<TICKET-ID>.spec.md`, where the file stem before `.spec.md` is the whole ticket id and matches `^[A-Z][A-Z0-9]*-[0-9]+$`. Normalize path separators, and accept a path that resolves to that file. A stem that only begins with a ticket id does not match.
- Anything else — a missing path, an unknown flag, a brief path, a bare ticket id, a path outside `docs/specs/TODO/`, a path containing `..`, or a request to work from the conversation — halts with `Usage: /spec-tickets docs/specs/TODO/<TICKET-ID>.spec.md` and writes nothing.

`<PARENT-ID>` below is the ticket id taken from the file name.

## Phase 0 — Preflight

1. Resolve the repo root and the spec path as above.
2. Read the spec. It is the only source for the breakdown. Do not read the sibling brief, the reviews directory, or the conversation for pieces.
3. **Green-lit check.** Each of `## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Test command`, `## Done when`, and `## Out of scope` must occur exactly once as a level-2 heading outside a fenced block. A missing heading, or a second heading of the same name, halts with the heading named. This skill does not re-run reviewers.
4. If `docs/specs/TODO/<PARENT-ID>.reviews/` is absent, warn once and continue.
5. **Deferred rows.** If the spec has a `## Deferred — follow-up required` section, count its `### D-<n>:` headings outside fenced blocks. Those rows are never filed as pieces. If the section exists and the count is zero, the count line later reads `Deferred rows not filed: 0 (no D-<n> headings)`.
6. Print one line: `ticket: <PARENT-ID> · headings: ok · reviews: present | absent`.

## Phase 1 — Storage probe

Read-only. Decide, once, where the graph will be written. One integration per run.

| Mode | When | What is written |
|------|------|-----------------|
| `native` | An issue-tracker integration is connected, the parent ticket resolves through it, it can create a work item with a parent, and it offers an operation that creates a blocked-by relation between two work items | Child work items of the parent, plus one blocked-by relation per edge. No `Blocked by` section. No local files. |
| `text` | The same, except it offers no such relation operation | Child work items of the parent, each with a `Blocked by` section. No relation writes. No local files. |
| `local` | No issue-tracker integration is connected. This is the only `local` trigger | One file per piece at `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md`, including `Blocked by`. No tracker writes. |
| `halt` | An issue-tracker integration is connected, and this probe or the parent retrieve does not answer or returns an error, or no connected integration can create a work item with a parent | Nothing. |

Rules:

- **`halt` is not `local`.** An optional service that is unavailable would normally warn and proceed. Here it halts, because local files beside a live tracker would be a second graph.
- **More than one candidate.** If more than one connected integration can create a work item with a parent, stop before the approval block, print their names, and wait for the operator to name one. A reply that is not one of those names, an empty reply, or a host that cannot wait halts with no writes. The chosen name is part of the approved draft.
- **Relation direction.** A `native` edge is one relation, created on the dependent child, of the blocked-by kind, with the blocker child as its target. An integration that offers only the inverse kind (a blocker pointing at what it blocks) is `text`.
- **Parent.** On `native` and `text`, resolve the parent with the integration's retrieve-by-identifier capability. Keep the parent reference, and the project reference when a create needs one, in the form that integration's own create operation takes. If the retrieve fails, or lacks a reference the create needs, the mode is `halt`. Do not consult shared memory and do not read any state-id config file for this.
- **Existing work.** On every mode except `halt`, make one read for work an earlier run may have left: the parent's children when the integration can list them, and the files matching `docs/specs/TODO/<PARENT-ID>.ticket-*.md`. Keep the two counts. If the children read is unavailable or fails, that count is `unknown`; it does not change the mode. The counts are a notice, not a census.
- **The mode is fixed for the run.** Nothing after this phase switches it.

The storage line has one grammar: `Storage: native via <name>`, `Storage: text via <name>`, `Storage: local`, or `Storage: halt via <name or none> (<reason>)`.

`halt` still lets the draft be shown in Phase 3. It does not allow filing.

## Phase 2 — Draft

Draft from the spec's Design and Scope only. Do not explore the repo for extra work.

**What a piece is.**

- A piece is a narrow slice that delivers one end-to-end outcome and can be verified without the other pieces. A slice of a single layer with no outcome of its own is not a piece.
- A piece is small enough for one agent to finish in a single fresh context. This is a sizing rule for the breakdown. It is not a token budget, a batch size, or a cap on parallel work.
- Draft the fewest pieces that satisfy those two rules.
- **Preparatory pieces.** When the spec's Design already calls for a seam that a later piece needs, that seam is its own piece ahead of the piece it unblocks, and it must still be verifiable alone. Do not invent a seam the Design does not name.
- **Wide mechanical change.** When the spec's Design is one mechanical change across many Scope rows, so that no narrow slice could land working, use expand–contract: one piece that adds the new form beside the old; one or more pieces that move callers across, each blocked by the first; one piece that removes the old form, blocked by every mover.
- Do not add a final "integrate and verify" piece. The parent spec's full Done when and the pre-merge review run once on the assembled PR and are that check.

**Slugs.** Name each piece with a slug matching `^[a-z0-9]+(-[a-z0-9]+)*$`, at most 40 characters, unique in the draft. Slugs are names, not an order. Do not label pieces with severity-style tokens such as `P1` or `P2`. Give each piece a short title as well; the short title is what gets stored.

**Edges.** For each piece, list the pieces that must be complete before it can start. An edge exists only when the blocker genuinely gates the piece. A piece with no blockers can start at once.

**Acceptance criteria.** Each piece has at least one criterion. A criterion is one line, drawn from the spec's Done when or Test plan, and cites the bullet or row it comes from. The assignable units are the list items and table rows under `## Done when` and `## Test plan`. If `## Done when` has neither list items nor table rows, halt. Every unit is assigned to exactly one piece or marked assembled-only. A Test plan row follows the piece whose criterion cites it; a row that only the assembled PR can satisfy is assembled-only. Two things are assembled-only by default and never a child's criteria: the spec's full Done when taken as a whole, and the pre-merge review of the assembled PR. Anything the draft cannot place is listed as unassigned.

## Phase 3 — Approval

Print the breakdown and wait. There is no bypass flag and no environment-variable bypass.

```text
SPEC TICKETS: <PARENT-ID>
Spec: <path>
Storage: <storage line from Phase 1>
Deferred rows not filed: <n>
Existing under parent: <n children or unknown>, <n local ticket files>
<when either count is above zero: Approving files these pieces in addition to what exists.>
<when a local target exists: Cannot file — these paths exist: <paths>>

Pieces:
- <slug> — <short title>
  Delivers: <one paragraph>
  Acceptance: <one line per criterion, with spec anchor>
  Blocked by: <slugs, or None — no blockers.>
Unblocked (can run together; not an execution order): <slugs>
Waiting: <slug> blocked by <slugs>
Done-when assigned: <bullet → slug>
Done-when assembled-only: <bullets>
Unassigned: <bullets or none>

1. Approve and file
2. Revise — say what to merge, split, or re-edge
3. Abort — nothing filed
```

**Option 1 is omitted** while any of these holds:

- the storage mode is `halt`;
- the mode is `local` and the target path of any piece already exists (name the paths);
- the draft has a cycle, a self-edge, a duplicate slug, a slug outside the grammar, or an edge to an unknown slug;
- a piece has no acceptance criterion;
- a Done-when unit or Test plan row is neither assigned nor marked assembled-only.

**Replies.**

- Exactly `1`, after trimming, and only when option 1 was printed: file.
- Exactly `3`: abort and write nothing.
- Any other non-empty reply, including a longer line that starts with `1`: revise. Re-render the block. Do not file. A revision never changes the storage mode; only a fresh run of Phase 1 can leave `halt`.
- An empty reply, end of input, a timeout, or a host that cannot wait: print `approval required — this skill does not file headless` and write nothing.

The block that was printed is what approval freezes — its pieces, edges, criteria, and anchors — not a later re-read of the spec.

## Phase 4 — File

1. If the spec file's contents changed since the approved block was printed, halt with no writes and ask for a new approval.
2. Work only from the frozen draft. Do not redraft from the spec.
3. **File blockers first.** A piece is filed only after every piece that blocks it. Among pieces that are ready together, use the approval block's order. File one piece at a time. This order exists so that a blocker's identifier exists before anything refers to it. It is not a build order, it is not written into any ticket, and it does not decide which pieces can run together — the edges do.
4. **Per piece.**
   - `native`: create the child work item under the parent, then create its blocked-by relations to its blockers.
   - `text`: create the child work item under the parent with a `Blocked by` section in its body.
   - `local`: write `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md`. Never overwrite an existing file; a target that exists at write time is a failure (step 6).
5. **What a ticket contains.** The tracker name, or the local file's H1, is the piece's short title. Send the body as the integration's description field. Body sections, in order:
   - **Parent** — the parent's identifier.
   - **Spec** — the spec path and the section anchors the piece draws on. Point at the spec; do not copy its Design, its Test plan prose, or any code. No code blocks in a ticket.
   - **Delivers** — one paragraph: the end-to-end outcome.
   - **Acceptance criteria** — the checklist from the frozen draft.
   - **Assembly** — this piece lands on the parent spec's single integration branch and single PR and does not open a PR of its own; the parent's full Done when and the pre-merge review run once on the assembled PR; a `/ship-spec` run on the parent does not read child tickets.
   - **Blocked by** — `text` and `local` only. One reference per line, or the single line `None — no blockers.` On `text` a reference is the blocker's tracker identifier and its title. On `local` it is the blocker's file name and its title. This is a relation list, not a numbered procedure. `native` tickets omit the section.

   A `local` file carries the line `local-only` directly after its H1.
6. **Failure.** When a create, a relation write, or a file write returns an error, or a create returns no identifier, stop at once. No further writes, no retry, no switch of mode, no fall-back to local files. Print a stop report: each piece as `created <identifier or path>` or `not created`, each edge as `written` or `not written`, then the operation that failed and the error as it was returned. A stopped run never prints `FILED`. The operator files the rest by hand from that report, or deletes what was created and runs again.
7. **Create-only.** Do not edit a ticket, delete a ticket, remove a relation, or change any ticket's state, including the parent's. A new child keeps the tracker's default state for a new item.
8. **Success.** Only when every create and every relation write returned success, print:

```text
FILED: <PARENT-ID>
Storage: <storage line>
Pieces: <n> · Edges: <n>
- <slug> → <identifier or path>
Unblocked (can run together): <slugs>
```

**No resume.** This skill does not read its own writes back, and a second run does not find, reuse, or compare an earlier run's tickets. On a tracker, a second run files every approved piece again; the existing-work line in the approval block is the operator's warning. A second `local` run is refused while its target files exist.

## What /spec-tickets never does

Edits the spec. Edits or changes the behaviour of `/ship-spec`, `/spec-cycle`, or `/spec-close`. Creates a branch, a worktree, or a PR. Transitions or rewrites the parent ticket. Dispatches an implementer. Files from a brief, a ticket id, or a conversation. Files headless. Writes both tracker records and local files in one run. Writes the inverse of a blocked-by relation. Deletes or updates a ticket. Overwrites a local ticket file. Resumes or repairs an earlier run. Files a deferred follow-up row as a piece.

## Tool-use notes

- File reading and writing for the spec and, in `local` mode, the ticket files.
- The issue tracker's capabilities, all optional: retrieve a work item by identifier, list the children of a parent, create a work item with a parent, and create a blocked-by relation on the dependent. Use whatever the connected integration offers for each, or the equivalent in your host. This skill names no tracker response field; read what the integration returns the way that integration documents it.
- A host whose tracker integration sets a parent and nothing else takes the `text` mode.
- No shell, no network beyond the tracker integration, no subagents, no shared-memory lookup.
- `local` file names fit `/spec-close`'s companion rule (`<TICKET-ID>.<rest>`), so a later close archives `ticket-<slug>.md` with the rest of the spec's artifacts.

## Failure modes

- **Wrong argument** → the usage line; nothing written.
- **Spec not green-lit** (a required heading missing or duplicated) → halt naming the heading.
- **Tracker connected but failing, or unable to create with a parent** → `halt`; the draft is shown, filing is not offered, no local files are written.
- **Parent does not resolve** → `halt`.
- **Two capable integrations and no name given** → halt with no writes.
- **Draft not approvable** (cycle, bad slug, unassigned unit) → option 1 omitted until a revision fixes it.
- **No operator** → `approval required — this skill does not file headless`.
- **Spec changed after approval** → halt; ask for a new approval.
- **A write fails mid-run** → stop report; no `FILED`; no retry.
- **Run twice on a tracker** → duplicates. The approval block's existing-work line is the only guard.
