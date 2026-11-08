---
name: spec-tickets
description: Optional stage between /spec-cycle and /ship-spec. Splits one green-lit spec into verifiable pieces with blocking edges and files them as children of the spec's ticket — blocked-by relations where the tracker has them, a Blocked by section where it does not, one local file per piece when no tracker is connected. Files nothing for a spec that does not split. Does not change how /ship-spec runs.
user_invocable: true
requires:
  shell: optional
  filesystem: [read, write]
  services: [issue-tracker?]
---

# /spec-tickets — file verifiable pieces of one spec

This skill reads one spec, drafts the fewest pieces that each deliver one end-to-end outcome and can be verified alone, and files them. The dependency graph lives in the tracker, not in the spec and not in an ordered list.

The stage is optional. Not invoking it is the skip. Invoking it is the authorization to file.

## Invocation

One argument: `docs/specs/TODO/<TICKET-ID>.spec.md`. The file stem is the ticket id, `<PARENT-ID>`. Anything else prints `Usage: /spec-tickets docs/specs/TODO/<TICKET-ID>.spec.md` and stops with nothing written.

## Operator replies

The one prompt is the integration pick. Read the reply for intent. The numbered list is the fast path. Print `Reading: <what you will do>.` before acting. An ambiguous reply is asked again, naming what is unclear. Silence or an empty reply is never yes, and at the integration pick it stops with nothing written. `abort` as the only non-blank line stops with nothing written.

## Phase 0 — Preflight

Read the spec. It is the only source for pieces.

**Heading check.** Halt, naming the heading, when the spec lacks `## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Done when` or `## Out of scope`.

**Verdict read.** `verdict_marker.py` owns the marker. Run this block as one shell call:

```bash
VERDICT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-cycle/scripts/verdict_marker.py"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
"$PY" "$VERDICT" read --ticket <PARENT-ID> --marker docs/specs/TODO/<PARENT-ID>.reviews/verdict.md --no-fingerprint
```

`red` halts before any draft:

```text
SPEC VERDICT: red (round <round>, gate <gate>, <date>).
/spec-tickets does not file tickets for a red spec.
Get a green verdict first: re-run /spec-cycle, or record your own review with
  /spec-cycle <spec-path> --attest "<reason>"
```

Any other state continues. The report line is `Verdict: <state>`, plus the JSON `kind` and `date` when the state is green, or the `reason` when the state is unreadable.

A missing script, a non-zero exit, output that is not JSON, or a host with no shell reads the marker as plain text. A first `verdict:` line of `red` halts as above. Anything else is `Verdict: unreadable (<reason>)`. The reason is `script missing — run python sync.py install`, `verdict_marker.py exit <n>`, or `no shell — verdict not fully checked`.

**Deferred rows.** Headings under `## Deferred — follow-up required` are never filed as pieces. Their count is shown in the report.

## Phase 1 — Storage probe

Read-only. One integration per run.

| Mode | When | What is written |
|------|------|-----------------|
| `native` | A connected integration resolves the parent, creates a work item with a parent, and creates a blocked-by relation | Child work items, plus one blocked-by relation per edge |
| `text` | The same, except it creates no blocked-by relation | Child work items, each with a `Blocked by` section |
| `local` | No issue-tracker integration is connected | One file per piece at `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md` |
| `halt` | An integration is connected and the probe or the parent retrieve fails, or none can create a work item with a parent | Nothing; the run stops here. |

`halt` is not `local`. Local files beside a live tracker would be a second graph.

More than one integration that can create a work item with a parent asks which one, before drafting. That pick is the prompt in Operator replies.

A `native` edge is one blocked-by relation on the dependent, targeting the blocker. An integration that offers only the inverse kind is `text`.

On `native` and `text`, resolve the parent through the integration's retrieve-by-identifier capability. A retrieve that fails, or that lacks a reference the create needs (the parent reference, or the project reference when a create takes one), is `halt`.

**halt.** Print `Storage: halt via <name or none> (<reason>) — nothing filed.` and stop before drafting. The draft is not shown.

**Duplicate guard.** Count the files matching `docs/specs/TODO/<PARENT-ID>.ticket-*.md`. In `native` and `text`, also count the parent's children through the integration. The applicable counts are the file count in `local`, and both counts in `native` and `text`. When any applicable count is above zero, print `NOT FILED: <PARENT-ID> already has children (<n>: <identifiers> | not checked (local)) and local ticket files (<n>). If they are pieces from an earlier /spec-tickets run, delete them by hand and run again; otherwise split this spec by hand.` When an applicable count cannot be read, print `NOT FILED: cannot count <PARENT-ID>'s children through <name> (<reason>) — children: unknown, local ticket files: <n | unknown>.` Either way stop with nothing written. A tracker with no list-children capability therefore never files in `native` or `text`.

## Phase 2 — Draft

Draft from the spec's Design and Scope only.

**What a piece is.** A piece delivers one end-to-end outcome and can be verified without the other pieces. A slice of a single layer with no outcome of its own is not a piece. A piece is small enough for one agent to finish in a single fresh context. Draft the fewest pieces that satisfy those two rules. When the Design already calls for a seam a later piece needs, that seam is its own piece and must still be verifiable alone. Do not invent a seam the Design does not name. When the Design is one mechanical change across many Scope rows, use expand–contract: one piece that adds the new form beside the old; one or more pieces that move callers across, each blocked by the first; one piece that removes the old form, blocked by every mover. Do not add a final integrate-and-verify piece. The parent spec's full Done when and the pre-merge review run once on the assembled PR.

**Slugs.** Each piece has a short title and a unique kebab-case slug of at most 40 characters matching `^[a-z0-9]+(-[a-z0-9]+)*$`.

**Edges.** For each piece, list the pieces that must be complete before it can start. An edge exists only when the blocker genuinely gates the piece. A piece with no blockers can start at once.

**Acceptance criteria.** Each piece has at least one line citing the Done-when or Test-plan item it comes from. Every Done-when and Test-plan item goes to exactly one piece or is marked assembled-only. A Test plan row follows the piece whose criterion cites it. A row that only the assembled PR can satisfy is assembled-only. The spec's full Done when taken as a whole, and the pre-merge review of the assembled PR, are assembled-only.

**One-piece exit.** When the draft has fewer than two pieces, print `one piece — run /ship-spec docs/specs/TODO/<PARENT-ID>.spec.md`, file nothing, and stop.

**Draft checks.** Before any write: no cycle, no self-edge, no duplicate slug, no slug outside the grammar, no edge to an unknown slug, no piece without an acceptance criterion, no Done-when or Test-plan item left neither assigned nor assembled-only. Repair the draft once where the fix is clear (re-edge, rename, assign an item or mark it assembled-only), then run the one-piece exit again and re-run the checks. A check that cannot be cleared prints `NOT FILED: <check> — <detail>` and stops with nothing written.

## Phase 3 — File

Work from the checked draft. Do not redraft mid-filing. File blockers first, one at a time, so a blocker's id exists before anything refers to it.

- `native`: create the child under the parent, then create its blocked-by relations.
- `text`: create the child under the parent with a `Blocked by` section.
- `local`: write `docs/specs/TODO/<PARENT-ID>.ticket-<slug>.md`. Never overwrite an existing file.

**Ticket contents.** The tracker name, or the local file's H1, is the short title. Body sections, in order: **Parent** (the parent's identifier); **Spec** (the spec path and the section anchors — point at the spec; no code blocks); **Delivers** (one paragraph); **Acceptance criteria** (the checklist); **Assembly** (this piece lands on the parent spec's single PR and does not open its own; `/ship-spec` on the parent does not read child tickets); **Blocked by** (`text` and `local` only: one reference per line, or `None — no blockers.`). A `local` file carries the line `local-only` directly after its H1.

**Failure.** On the first failed write, or a create that returns no identifier, stop with no retry and no fallback. Print the stop report. A create that committed but returned no identifier is `not created`; check the tracker before filing the rest by hand.

**Create-only.** Never edit or delete a ticket, remove a relation, or change any ticket's state, the parent's included. Never edit the spec.

## Report

On success:

```text
FILED: <PARENT-ID>
Storage: <native via <name> | text via <name> | local>
Verdict: <line from Phase 0>
Deferred rows not filed: <n>
Pieces: <n> · Edges: <n>
- <slug> — <short title> → <identifier or path>; blocked by <slugs | none>
Unblocked (can run together; not an order): <slugs>
Assembled-only: <Done-when and Test-plan items, or none>
Repaired: <each draft-check repair, such as an edge dropped to break a cycle, or none>
Next: /ship-spec docs/specs/TODO/<PARENT-ID>.spec.md
```

On a stop after a failed write, the same header lines, then each piece as `created <identifier or path>` or `not created`, each edge as `written` or `not written`, then the failed operation and its error as returned. The first line reads `STOPPED: <PARENT-ID>`, never `FILED`. The operator files the rest by hand from that report, or deletes what was created and runs again. The duplicate guard stops a re-run until then. Check the tracker before filing by hand when a create's outcome is unknown.

## Tool-use notes

The capability inventory: retrieve a work item by identifier, list the children of a parent, create a work item with a parent, create a blocked-by relation on the dependent; or the equivalent in the host. `native` and `text` file only when the list-children read works. One `verdict_marker.py read --no-fingerprint` call. `local` file names fit spec-close's companion rule (`<TICKET-ID>.<rest>`), so a later close archives `ticket-<slug>.md` with the spec's artifacts.
