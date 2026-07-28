# Batch Reconciliation — vigil-skills — 2026-07-27

Batch archive performed 2026-07-27 under a **partial-close policy**: archive only.
No per-spec acceptance verification was done, no per-spec reconciliation report was
written, and no wiki decomposition (decisions / comprehension / `state.md` flips) was
performed for any ticket in this batch.

## Branch resolution

Default branch resolved via `git symbolic-ref refs/remotes/origin/HEAD` -> `refs/remotes/origin/main`.
Containment was tested against **`origin/main`** because the local `main` was 1 commit
behind. The working tree is checked out on the feature branch `feat/tal-003-talaria-skill`,
which was left untouched — no checkout, commit, or branch operation was performed.

## Gate used

**Each archived ticket has at least one commit that is an ancestor of `main`
(tested against `origin/main`, per the resolution above).**

Plane state was explicitly **NOT** used as the gate. In this workspace 7 of 9 projects
place their review state in the state group `completed`, so a ticket sitting in review
with an open, unmerged PR reads as "completed" through the Plane API. Git ancestry is
the only trustworthy shipped-signal, so ancestry is what gated this batch.

## Archived

| Ticket | Commit | Subject | Plane state | Needs transition |
|---|---|---|---|---|
| VHS-1 | `8f9ac93` | feat(vhs-1): lift Plane reads onto MCP webhook cache + states.json (#4) | Done | no |
| VHS-3 | `4889eec` | Merge pull request #5 from ziomancer/feat/vhs-3-per-thread-hash-replies | Done | no |
| VHS-4 | `fcc5ee9` | feat(vhs-4): fast path for trivial PRs + CI-check gate for review completion (#6) | Done | no |
| VHS-5 | `ac7c778` | Merge pull request #8 from ziomancer/fix/vhs-5-review-pr-graphql-stat-cadence | Done | no |
| VHS-6 | `19d2d98` | Merge pull request #7 from ziomancer/feat/vhs-6-upstream-staleness-check | Done | no |
| VHS-7 | `491f13a` | feat(vhs-7): make spec-lifecycle skills host-agnostic (#11) | Done | no |
| VHS-8 | `82f2ce9` | Merge pull request #9 from ziomancer/feat/vhs-8-spec-retirement-pipeline | Done | no |
| VHS-9 | `1b3d854` | Merge pull request #10 from ziomancer/feat/vhs-9-wiki-coverage-fast-path | Done | no |
| VHS-11 | `4088ee8` | feat(vhs-11): origin-sync check + 3 review-loop enhancements for spec-cycle (#13) | Done | no |

Artifacts moved from `docs/specs/TODO/<T>.<artifact>` to `docs/specs/DONE/<T>/<artifact>`
with the ticket prefix stripped (`<T>.spec.md` -> `spec.md`, `<T>.brief.md` -> `brief.md`,
`<T>.reviews/` -> `reviews/`, `<T>.test-output.txt` -> `test-output.txt`). No existing
`DONE/` archive was overwritten.

## Plane bookkeeping — shipped to `main` but not marked Done

(none) — all nine archived tickets were already in Plane state `Done`.

## Not archived

### HOLD (commits exist but not on `main` — open PR or abandoned branch)

none

### SKIP (no commits / not ticket-shaped)

- **VHS-13** — remains in `docs/specs/TODO/` (`VHS-13.brief.md`, `VHS-13.spec.md`, `VHS-13.reviews/`, `VHS-13.test-output.txt`)
- **VHS-24** — remains in `docs/specs/TODO/` (`VHS-24.brief.md`, `VHS-24.spec.md`)

### Not in scope for this batch

- **VHS-16** — `VHS-16.brief.md` is present in `docs/specs/TODO/` but was not classified in
  the batch triage (neither cleared, HOLD, nor SKIP). It was left exactly where it is and
  needs a triage pass of its own.

## Limitations

- Per-spec **acceptance criteria were NOT verified** against shipped code. "Archived" here
  means "a commit for this ticket is on `main`", nothing stronger.
- Reconciliation **attribution across specs this old is unreliable** — a spec's stated scope
  routinely drifts from what its ship-commit actually contained, and later tickets frequently
  land changes that a naive diff would credit to the earlier spec.
- Any spec that needs a real audit should be **re-run through `/spec-close` individually from
  its `DONE/` path**, which will produce a proper per-spec reconciliation report and the wiki
  decomposition this batch deliberately skipped.
