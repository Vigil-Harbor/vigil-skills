# Spec Workflow — Clean-Room Reference

Six skills form the spec lifecycle, and `/spec-tickets` is the optional one. `/spec-brief` settles the brief before any review context is spent. `/spec-cycle` authors the spec and reviews it. `/spec-tickets`, when you invoke it, files pieces of that spec. `/ship-spec` implements the spec. After the pull request merges, `/spec-land` records the land, and `/spec-close` harvests and archives.

The split between authoring and implementation is load-bearing. Spec context grows with review rounds, and implementation context grows with the codebase. Combining them risks hitting the context window mid-flight, with no stable point to resume from. The session boundary is that point: a green-lit spec on disk stays a stable artifact. If implementation aborts, you re-run from the spec without re-reviewing it. The paragraphs below are the overview a person reads. Each skill's rules live in its own `SKILL.md`, and that file is what an agent follows. This page does not restate phases, gates, or reply grammar. When the two disagree, the skill wins.

## Lifecycle at a glance

`/spec-brief` → `/spec-cycle` → (`/spec-tickets`) → `/ship-spec` → merge → `/spec-land` → `/spec-close`.

Parentheses mark the optional stage. Skipping it changes nothing about how `/ship-spec` runs. `/grill-me` is the ad-hoc interview, and it writes no lifecycle artifact. `/review-pr` triages CodeRabbit findings on an open pull request. Neither is a step in the chain above.

## spec-brief

Produce the brief that `/spec-cycle` consumes. It resolves the ticket when a tracker is connected and degrades to the conversation when it is not, grounds against the repo and the wiki, runs a bounded interview, and writes `docs/specs/TODO/<TICKET-ID>.brief.md`. The brief is the artifact every later reviewer treats as authority, so a fork left open in it shows up later as a finding against the spec. Confirming the text is part of writing it.

Invocation: `/spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`.

The rules are in skills/spec-brief/SKILL.md.

## spec-cycle

Author a spec from a brief, then run a parallel review until the spec is green or `round_cap` passes complete. It records a verdict marker and stops before any implementation. You leave this skill holding a spec and a verdict, and you start the next skill by hand. Its green NEXT recommends `/spec-tickets` when the spec splits into two or more pieces that can each be verified alone, and `/ship-spec` otherwise. That line is advice. Neither command runs from spec-cycle.

Invocation: `/spec-cycle <brief-path> [--attest "<reason>" | --full]`.

The rules are in skills/spec-cycle/SKILL.md.

## spec-tickets

Optional. Invoking it files verifiable pieces, with blocking edges, as children of the spec's ticket. Where the tracker can relate work items, the edges are blocked-by relations. Where it cannot, each child carries a Blocked by section. With no tracker connected, each piece is one local file beside the spec. A spec that does not split files nothing and points at `/ship-spec`. Existing pieces stop a re-run until they are removed by hand. `/ship-spec` still ships the whole spec either way.

Invocation: `/spec-tickets docs/specs/TODO/<TICKET-ID>.spec.md`.

The rules are in skills/spec-tickets/SKILL.md.

## ship-spec

Implement a green-lit spec in an isolated git worktree, through a test gate and a review gate, then open a pull request and update the issue tracker. The primary checkout stays as it was, apart from a local copy of an ignored test or review record. A build-only run stops once the tests are green and prints the command that continues at review.

Invocation: `/ship-spec <spec-path> [--build-only | --from-review <worktree-path>]`.

The rules are in skills/ship-spec/SKILL.md.

## spec-land

After the pull request is merged, confirm the landed code matches the recorded head and patch-id, move the ticket, write the wiki merge line and the filemap delta, and clean up the worktree and the branch. It is the step between the merge and the close. It never merges and never commits. Cleanup removes the worktree and the feature branch, then runs the project's post-land command from the main checkout.

Invocation: `/spec-land <PR-number | PR-URL | spec-path>`.

The rules are in skills/spec-land/SKILL.md.

## spec-close

Close a shipped spec: reconcile it against the code that shipped, propose wiki entries sized to the brief, archive the artifacts, and prepend the wiki log entry. Run it after `/spec-land`. The invocation forms are `<spec-path | TICKET-ID | docs/specs/TODO/<TICKET-ID>/>`. A ticket that has artifacts but no spec gets an archive-only close: the archive plus the log entry, with no reconciliation.

Invocation: `/spec-close <spec-path> [--report-only | --partial]`. The argument may also be a ticket id or a `docs/specs/TODO/<TICKET-ID>/` folder.

The rules are in skills/spec-close/SKILL.md.

## Shared artifacts

The verdict marker is `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`. `skills/spec-cycle/scripts/verdict_marker.py`'s docstring is the one statement of its format, fingerprint, and states. spec-cycle writes the marker. ship-spec and spec-tickets read it and do not restate the format. Briefs, specs, and reviews live in the target project, not in this skills repo. The rest of the layout — test output, ticket files, and the `docs/specs/DONE/<TICKET-ID>/` archive — is in `docs/customizing.md`. A project may gitignore `docs/specs/`. The skills still resolve those paths on disk.

## Adapting to your stack

The skills are designed to be tool-agnostic. The integration points to swap:

| This workflow uses | You'd replace with |
|---|---|
| Plane (issue tracker) | Jira, Linear, Asana, GitHub Issues, etc. |
| Plane connector tools | Your tracker's API/MCP/CLI |
| `states.json` (maps ticket prefixes to project IDs and state UUIDs) | Your tracker's project/workflow config |
| `gh` CLI (PRs) | Your git host's CLI (`gh`, `glab`, Bitbucket API, etc.) |
| Wiki (conventions reviewer reads `decisions/`, `architecture.md`, etc.) | Your team's docs, ADRs, Confluence, Notion — or omit `wiki_root` |
| `docs/specs/TODO/<TICKET-ID>.*` file layout | Whatever path convention you prefer |

## Things not to change

These are load-bearing. Leave them as the skills state them.

- **Session boundary between spec-cycle and ship-spec.** Combining them is the main failure mode: context exhaustion mid-implementation, with no recovery point. A green spec on disk is what you re-run from.
- **Parallel multi-lens review.** Sequential reviews let later reviewers anchor on earlier findings. Parallel dispatch forces independent reads.
- **Reviewers are read-only.** They never edit files. spec-cycle owns the edits, so a reviewer cannot change the spec and introduce a new issue while reviewing it.
- **STATUS line protocol.** A machine-parseable last line, `GREEN` or `RED P0=<n> P1=<n> ...`, gates the loop. The orchestrator sums P0+P1 across the reviewers it dispatched.
- **Round 2+ closure tracking.** Reviewers read the predecessor round when a closure manifest is provided, and they produce a closure table. Without that, the loop does not converge: reviewers re-raise issues that were already fixed.
- **Targeted rewrite at the last pass, not a blank slate.** A blank-slate rewrite regresses closed findings. The rewrite keeps sections that already converged. A delta pass never runs that rewrite.
- **Worktree isolation in ship-spec.** Working in the user's checkout means one bad git operation can lose uncommitted work. The worktree is the boundary.
- **One test fix per iteration.** Bundling several fixes makes it impossible to say which fix resolved which failure. One fix, then run the tests again.
