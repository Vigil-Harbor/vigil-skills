# Reconciliation Report: VHS-60

> Date: 2026-10-13
> Spec: docs/specs/TODO/VHS-60.spec.md
> Merge: PR #42, squash `fad52c78247263ba829ee5519ba2c63bbdc78f0f`
> Plane state: Done (group: completed)

## Summary

The shipped change is the spec's sixteen `Current`/`Replacement` pairs applied to seven files, verified byte-for-byte before the commit, plus one sentence reworded by the review gate. All ten brief criteria are met. Two drifts: that reworded sentence, and the shape of the Decision 10 evidence.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-cycle/SKILL.md` | Yes | As specified, except one sentence (see Decision 2) |
| `agents/spec-reviewer-correctness.md` | Yes | As specified |
| `agents/spec-reviewer-edge-cases.md` | Yes | As specified |
| `agents/spec-reviewer-conventions.md` | Yes | As specified |
| `agents/spec-reviewer-scalability.md` | Yes | As specified |
| `README.md` | Yes | As specified |
| `docs/spec-workflow-reference.md` | Yes | As specified, except the same sentence (see Decision 2) |

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-60.review.md` and `docs/specs/TODO/VHS-60.test-output.txt` — the `/ship-spec` review-gate record and test capture. Lifecycle artifacts, not counted as drift.

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Print a late mode override | Confirmed | `skills/spec-cycle/SKILL.md:418` — 'replace the token with `mode: full (open findings unreadable)` and print that replacement token' |
| 2 | A failed full-pass snapshot has one two-file exception | Drifted | `skills/spec-cycle/SKILL.md:456` carries the exception as specified, but its last sentence ships as 'A delta pass never uses this exception. Any other incomplete artifact set still does not dispatch.' The spec's text was 'Every delta pass and every other incomplete artifact set still does not dispatch.', which read literally as "delta passes never dispatch". Reworded by the review gate (`review.md` finding 2); same rewording at `docs/spec-workflow-reference.md:81`. Wording only. |
| 3 | A deleted spec forces full mode | Confirmed | `skills/spec-cycle/SKILL.md:370` — '\| 6 \| Spec file does not exist \| `mode: full (no spec)` \|'; prose row references renumbered at `:378`, `:380`, `:458` |
| 4 | Delta pass 2's unreadable-status stop is unchanged | Confirmed | `skills/spec-cycle/SKILL.md:440` — 'pass 2 not dispatched; marker left pending' is untouched by the diff |
| 5 | Ignore every open ticket's review and attempt archives | Confirmed | `skills/spec-cycle/SKILL.md:493` — 'is `<ID>.reviews/` or `<ID>.attempt-<n>/` (an operator-made archive of a superseded attempt)' |
| 6 | Remove the stale status paragraph from all four agents | Confirmed | `<lens>/STATUS` names-no-heading paragraph absent from all four agents; the four `# Delta scope` blocks hash identically (sha256 `5e76ba015b8d…`) |
| 7 | Ordered boundary-aware heading matching always unions cited lines | Confirmed | `skills/spec-cycle/SKILL.md:495` (three arms, marker deletion) and `:497` — 'Independently of every heading match, resolve every line locator' |
| 8 | Segment multiple references and expand line ranges | Confirmed | `skills/spec-cycle/SKILL.md:495`–`:499` — segments, parenthesis cut, joining words, colon and word-form locators, per-clause fallback |
| 9 | State raw-path constraints as four separate clauses | Confirmed | `skills/spec-cycle/SKILL.md:491` — 'It has no leading `"`; it contains no `=>` anywhere, no tab anywhere, and no backslash anywhere.' |
| 10 | Pre-merge evidence uses this spec's real re-run | Drifted | The PR body records a real delta run under the pre-change rules, but not as "once unchanged and once after one small edit". It is one invocation: an unchanged pass 1 (round 3, `mode: delta (continuing round 2)`, 5 code-drift regions, red at gate 1) and a pass 2 after a large revision (round 4, 21 changed headings, green). No separate small-edit run was made. |
| 11 | Stakes tier | Confirmed | Spec line `**Tier:** big`; marker `tier: big`; the review gate ran |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | The three Where forms resolve without an every-heading fallback | Met | `skills/spec-cycle/SKILL.md:495` (arm 2 selects `Decision 8 — …`; boundary test) and `:497` (line always unioned); spec scenarios 10–12 |
| 2 | A bare review-artifact filename does not block the no-op | Met | `skills/spec-cycle/SKILL.md:493` — other tickets' `.reviews/` and `.attempt-<n>/` paths dropped before citation matching. The pre-change behaviour is recorded in the PR: 5 false code-drift regions from VHS-41 archives |
| 3 | One scenario per changed behaviour; archived VHS-27 spec unchanged | Met | Spec § Scenarios 1–26; `git diff --stat 0158267 fad52c7 -- docs/specs/DONE` is empty |
| 4 | The no-op prints the replacement mode token | Met | `skills/spec-cycle/SKILL.md:418` |
| 5 | README shows `--full` on the usage line | Met | `README.md:10` — '[--attest "<reason>" \| --full]' |
| 6 | A snapshot-failed full pass prints its line, saves two copies, dispatches | Met | `skills/spec-cycle/SKILL.md:456` — 'baseline.commit NOT written: full-pass snapshot unavailable (<reason>) — dispatching with spec.copy.md and brief.copy.md only'; `:446` lead-in; `:513` precondition |
| 7 | Reviewed marker with deleted spec prints `mode: full (no spec)` | Met | `skills/spec-cycle/SKILL.md:370`; rows 1–5 unchanged above it |
| 8 | Four agents omit the status paragraph; Delta scope blocks byte-identical | Met | See Decision 6 |
| 9 | Raw-path sentence states four separate clauses | Met | `skills/spec-cycle/SKILL.md:491` |
| 10 | One real delta re-run on this ticket's own spec is recorded in the PR | Met | PR #42 body § "Decision 10 evidence"; shape differs from the spec's wording (Decision 10, Drifted) |

Spec-level gates (not brief criteria): the colon-form locator is recognised (`:497`); every prose row reference names its intended row (`:378`, `:380`, `:458`; `rows 1–5` at `:375` and `row 4` unchanged); the build removed no line outside the stated edits (worktree rebuilt from `origin/main` plus the spec's pairs and compared byte-for-byte before the commit).

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| `python lint.py --strict` | Yes | `test-output.txt` — 0 errors, 0 warnings |
| `python -m unittest discover -s tests -p "test_*.py"` | Yes | `test-output.txt` — 127 tests OK, 3 skipped |
| Scenario walk and implementation review (no new automated test; the suite does not execute prose skills) | Yes | Round-4 reviews in `reviews/round-4/`; `/ponytail-review` in `review.md` |

## Notes for the wiki

- The spec's `## Deferred (P2+)` note for `/spec-close` was "corrected" after round 4 on a reviewer's claim that `state.md` has no row-11 anchor. That claim was wrong: wiki `projects/vigil-skills/state.md:12` does pin `skills/spec-cycle/SKILL.md:375 — '| 11 | Otherwise | …'` as the VHS-27 verification line, and that line is now row 12 at `:376`. `filemap.md:132` also says "eleven-row mode table". Both are stale.
- Open after this ticket: a word-form `line N` that follows another file's name is still placed in this spec (`review.md` finding 1; round-4 edge-cases/F-2). Not ticketed.

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:
- Decision 7 and Decision 8: the open-finding resolver grammar was first pinned from the brief's two examples and failed against real `Where` text (1,252 of 1,595 stored fields use the colon form); the shipped grammar is taken from the stored reports. Constraining for any later change to the resolver.
- Decision 2 and Decision 3: the two mode-table gaps the VHS-27 decision page lists as open are closed (two-file exception; `mode: full (no spec)` row).
- Decision 5: code drift ignores every ticket's review and attempt archives.
- Comprehension: what delta scope selection does now, and the lesson from this ticket's own run (a same-model author and reviewers passed a spec that a cross-model round and then a real delta pass found two P1s in).

RECONCILED: yes DRIFT: 2
