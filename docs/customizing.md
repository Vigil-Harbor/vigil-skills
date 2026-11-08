# Customizing Vigil Skills for your project

These skills are intentionally generic. Project-specific rules live in your project's `CLAUDE.md` or `AGENTS.md`. Each key below says which file is read.

## What to put in your `CLAUDE.md`

### Build & Run section

Read from `CLAUDE.md` only, and only when the spec has no `## Test command`. `/ship-spec` reads it as the test-gate fallback. `/review-pr` follows that same rule before it commits fixes. Example:

````markdown
## Build & Run

```bash
npm install
npm run build       # tsc -> dist/
npm test            # all tests
npm run lint        # eslint
```
````

Per-spec overrides go in the spec's `## Test command` section, which takes precedence.

### Review command section

Read from `CLAUDE.md` first, then `AGENTS.md`. `/ship-spec` has a review gate between its test gate and the commit: it runs one review of the change, fixes what blocks, and fixes or records the rest. The skill ships no reviewer of its own — you declare the command.

Add a `## Review command` heading whose content is one line: how to run a review of uncommitted changes on your host. It is either a skill invocation (a line beginning `/`) or a shell command:

```markdown
## Review command

<one line: your review command>
```

Example value: `/ponytail-review` *(e.g., the review skill of the ponytail plugin in Claude Code, or the equivalent in your host)*.

A section that is empty, or has more than one non-blank line, is ignored with a warning. A spec can override the project's command with its own `## Review command` section, which takes precedence; the section is optional in a spec.

If no review command is declared anywhere, the gate is skipped: `/ship-spec` prints a one-line note, puts `Review gate: skipped — no review command declared` in the PR body, and commits as before. A declared command that is not available on the host, or that fails, is also skipped and never blocks the commit.

### Key rotation (optional)

`/key-rotation` reads an optional project section for the provider roster, shared-account notes, the notify list, and the record path. The same block may live in `AGENTS.md`. The skill uses project-instructions text the harness already supplied. When the harness supplied none, it reads `CLAUDE.md` and then `AGENTS.md` at the project root, each only when the file can be read, and uses the first `## Key rotation` section. A missing or unreadable file is an absent section: the skill asks and does not stop. A missing section or a missing key is asked the same way. The skill matches the heading `## Key rotation` and no other.

````markdown
## Key rotation

Providers: source host, build service
Shared accounts: one credential covers two roles; name the roles
Notify: the operator's on-call channel
Record path: .key-rotation/record-YYYY-MM-DD.md
````

### Project guardrails

If your project has load-bearing rules — async handling, error patterns, ordering constraints — list them here. The reviewers and `/ship-spec` will respect them. Example:

```markdown
## Conventions

- All `recorder.record*` calls must be `await`ed; unawaited calls cause sequence-index collisions.
- Tools return text strings, never throw exceptions.
- TypeScript ESM with `.js` extensions in imports.
```

### Wiki integration (optional)

The `spec-reviewer-conventions` agent can read a wiki for prior decisions. If you have one, point at it. spec-land takes the `Slug:` value raw, so leave it unquoted: a backticked slug becomes part of the filemap path.

```markdown
## Wiki

Path: ~/code/myproject-wiki
Slug: myproject
```

spec-land reads the wiki path from a line naming the wiki or from a line under `## Wiki`, and reads `Slug:` under `## Wiki`. It reads `CLAUDE.md` first, then the landed `AGENTS.md`. The other lifecycle skills resolve `wiki_root` and `project_slug` from the same files. The agent reads `<wiki>/projects/<slug>/architecture.md`, `state.md`, `filemap.md`, and scans `<wiki>/decisions/` for relevant prior decisions.

If you don't have a wiki, omit `wiki_root` from the orchestrator prompt and the agent skips this step gracefully.

### Post-land command

Read from the first of `CLAUDE.md` and the landed `AGENTS.md` that holds a `## Post-land command` section. That file is the only one read. Fence lines do not count. The section is exactly one non-blank line. spec-land runs it in the main checkout only when that checkout holds the landed commit. A section with more lines is skipped with a warning.

```markdown
## Post-land command

python sync.py install
```

## Spec & brief layout

Skills assume:

- Briefs at `docs/specs/TODO/<TICKET-ID>.brief.md` (loose: just enough to get started). That path is the canonical *location*, but alternate directories and `<TICKET-ID>-slug.md` filenames are tolerated on input — spec artifacts still land in `docs/specs/TODO/` regardless.
- Specs at `docs/specs/TODO/<TICKET-ID>.spec.md` (`/spec-cycle` writes here)
- Reviews at `docs/specs/TODO/<TICKET-ID>.reviews/round-<N>/<lens>.md`
- The spec's recorded verdict at `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md` (written by `/spec-cycle`, read by `/ship-spec` and `/spec-tickets`)
- Test output captured to `docs/specs/TODO/<TICKET-ID>.test-output.txt`
- The review gate's record at `docs/specs/TODO/<TICKET-ID>.review.md` (one file, written by `/ship-spec`; distinct from the `<TICKET-ID>.reviews/` directory `/spec-cycle` writes)
- Local ticket files at `docs/specs/TODO/<TICKET-ID>.ticket-<slug>.md` (spec-tickets, `local` mode)
- The reconciliation report at `docs/specs/TODO/<TICKET-ID>.reconciliation.md` (spec-close)
- The archive at `docs/specs/DONE/<TICKET-ID>/` (spec-close)

Adjust the layout in your fork if needed; the skills hardcode the spec/reviews/test-output paths today (brief location is tolerant on input per the bullet above).

A project may gitignore `docs/specs/`. The lifecycle still runs: the skills resolve those paths from the repo root on disk. `/ship-spec` classifies the test output and the review record per path; an ignored one is kept locally and copied into the primary checkout beside the spec, and the PR body says so. `/spec-close` archives on disk, and it prints a target-repo commit suggestion only for paths it staged. The wiki, or whatever knowledge layer the project uses, is the durable record.

## Plane.so integration

spec-brief, spec-cycle, spec-tickets, ship-spec, spec-land, and spec-close read the issue tracker. ship-spec and spec-land are the two that move a ticket's state, both through `skills/ship-spec/states.json`. Configure the tracker connection per your host's docs.

`/ship-spec` flips a ticket to a review-equivalent state after PR open. The skill reads the installed `states.json` and uses the `review_state_id` field for the project. If your project isn't in `states.json` or has no `review_state_id`, the skill skips the flip and reports the available state names so you can update manually. `/spec-land` moves the ticket to Done or Post-merge Checklists from the same file. To add a new project, call the tracker's state-list capability for the project and add an entry to `states.json`.

## Default branch

`/ship-spec` discovers your default branch via `git symbolic-ref refs/remotes/origin/HEAD` (with a `git remote show origin` fallback). Works for `main`, `master`, `trunk`, etc. — no hardcoding required.

## Worktree path

`/ship-spec` cuts a sibling worktree at `<project-root>/../<TICKET-ID>-worktree`. Your primary working tree is never touched. If you want a different convention, fork and adjust Phase 1 step 2 of the skill.
