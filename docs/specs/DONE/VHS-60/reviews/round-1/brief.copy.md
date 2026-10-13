# VHS-60 — spec-cycle delta passes: tighten open-finding heading match and widen the code-drift path drop (VHS-27 follow-up)
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-10-13 · **Plane:** VHS-60 (04034411-013d-483e-a986-a948d87dd5d7, Backlog)
**Origin:** Filed 2026-10-12 as the follow-up to VHS-27 (delta-scoped review passes, shipped as `f64bebe`, PR #41). The description holds three P2 findings from the VHS-27 round-5 delta pass that changed the design and were deferred, plus three lower items. A comment of 2026-10-12 adds two VHS-27 review-gate findings that needed a spec decision. A comment of 2026-10-13 adds the raw-path wording drift found at the VHS-27 close. The interview on 2026-10-13 added two more review-gate findings that had no ticket. Third item in the Wave 2 spec-cycle lane, before VHS-26.

## Problem

Follow-up to VHS-27 (delta-scoped review passes). The VHS-27 spec was attested green on 2026-10-12 after a round-5 delta pass (three lenses, gate 0). That pass raised three P2 findings that change the design rather than clarify it, so they were recorded in the spec's Deferred (P2+) section instead of being folded. None produces a wrong verdict. Each makes a delta pass wider than it should be, or makes the no-op fail to fire, which is the cost VHS-27 exists to remove.

All three sit in the spec's Changed regions section (the rules that turn an open finding's Where text and the changed-path list into delta scope).

1. A prefix match on a parent or wrong heading discards the cited line. The rule selects a heading whose text equals the phrase or is the longest heading-text prefix of it, and then says a matching heading does not also use the line. A Where of "spec § Mode table, line 96" matches the heading "Mode" and drops line 96. "spec § Design, line 289" matches the empty parent heading "Design". The section the finding really sits in is left out of the delta scope. Closure verification still reads the cited text, so only new critique on that section is lost.
2. An abbreviated heading title with no line matches nothing and emits every heading. The match is one-directional. A Where of "spec § Decision 8" does not match the heading "Decision 8 — Two counters, at most two delta passes on every tier". With no line number the clause falls through to "emit every current heading", so the delta pass explores the whole spec. Numbered-decision headings are abbreviated this way in every spec in this repo.
3. Other tickets' untracked review trees and attempt archives count as code drift. The changed-path set drops this ticket's brief, spec and reviews directory only. A filename-only citation matches any changed path with that filename. Untracked files such as `docs/specs/TODO/VHS-41.reviews/round-1/correctness.md` or `docs/specs/TODO/VHS-41.attempt-1/spec.md` are listed by git on every run, so a spec that backticks a bare filename like `spec.md`, `correctness.md` or `grill.md` never reaches the no-op.

Recorded with them, lower priority:

4. On delta pass 2, an unreadable STATUS line stops the run with the marker pending. A reviewer suggested dispatching pass 2 as a full review within the same budget instead.
5. A Where clause with two § references, or a line range that crosses a heading, has no stated rule.
6. The reviewer agents' Delta scope block carries a paragraph about a `<lens>/STATUS` line that the skill no longer sends in a delta prompt.

From the VHS-27 review gate (PR #41), both needing a spec decision:

7. A full pass cannot dispatch when the commit snapshot fails. The round-artifacts rule requires the complete three-file set (spec copy, brief copy, commit) before dispatch. A first invocation in a project with no commits or no git can no longer review at all, and no stop line is defined; the unchanged preflight treats every git failure as non-fatal.
8. The mode table has no row for an absent spec file. The skill tells the operator to delete the spec to force a re-author. With a review marker, an intact baseline and an unchanged brief, that run resolves delta mode: code drift is computed against a spec that does not exist, and the freshly authored spec gets at most two delta passes with the old spec's ledger.

From the VHS-27 close (reconciliation drift S4, review-gate finding 6):

9. The raw-path rule was condensed in the build. The VHS-27 spec defines a raw path as one non-empty line with no leading double quote, no `=>`, no tab, and no backslash; the last three are banned anywhere in the line. The shipped text reads "with no leading `"`, `=>`, tab, or backslash", which can be read as banning all four only at line start. A listing line with a tab or backslash in the middle would then pass as raw.

## Why it matters

The ticket says none of these produces a wrong verdict. That holds for the items that widen a pass or block the no-op. Item 1 is narrower than it should be: reviewers newly explore only the headings a delta pass names, so a finding matched to the wrong heading loses new critique on the section it really sits in. Items 7 and 8 are different in kind: item 7 makes `/spec-cycle` unusable in a project with no commits, and item 8 reviews a freshly authored spec against the deleted spec's baseline and ledger. Delta mode has not been executed by a real run yet, and the unit suite does not execute skills, so these rules are unexercised.

## Scope (verified against current files, 2026-10-13)

| Path | Current | Change |
|---|---|---|
| `skills/spec-cycle/SKILL.md` § Changed regions, open-finding paragraph | After `§` or a heading marker, text through the next comma is matched by equality or the longest heading-text prefix; every tie is emitted and the line is then not used; with no heading match or placeable line, every current heading is emitted (`:492`). | Heading text is matched in a fixed order: equality, then headings that begin with the phrase at a boundary, then the longest boundary-valid heading prefix; the comma cut is retried against the uncut segment. Every cited line or line range is resolved separately in the predecessor copy and its owning headings are unioned in, whatever the heading match was (Decisions 7 and 8). |
| `skills/spec-cycle/SKILL.md` § Changed regions, changed-path drop | Drops the resolved brief path, `docs/specs/TODO/<TICKET-ID>.spec.md`, and every path under `docs/specs/TODO/<TICKET-ID>.reviews/`; citations match by exact value, slash-boundary suffix, or filename-only equality (`:490`). | Also drops every path under `docs/specs/TODO/` inside any ticket's `.reviews/` or `.attempt-<n>/` directory, the spec and brief copies an attempt directory holds included. Another ticket's canonical `<ID>.brief.md` and `<ID>.spec.md` still count (Decision 5). |
| `skills/spec-cycle/SKILL.md` § Changed regions, raw-path sentence | "with no leading `"`, `=>`, tab, or backslash" (`:488`). | Four separate clauses: no leading double quote; no `=>`, no tab and no backslash anywhere (Decision 9). |
| `skills/spec-cycle/SKILL.md` Phase 0 step 10, mode table | Eleven rows, first match wins; no row for an absent spec file (`:363-375`). The mode is resolved before Phase 1 (`:355`), so every first invocation also has no spec. | One new row, after the attested row (5) and before the brief-changed row (6): spec file does not exist → `mode: full (no spec)` (Decision 3). |
| `skills/spec-cycle/SKILL.md` § Round artifacts | A full pass takes one `rev-parse HEAD`; invalid or timed-out output fails the commit write; all three temps are written first and a failed rename means no dispatch (`:453`); an incomplete set does not dispatch (`:506`). | A named exception for a full pass whose snapshot fails: print that `baseline.commit` was not written, write and rename the spec copy and the brief copy, and dispatch only if both renames succeed. That round is reviewed and cannot be a delta baseline (Decision 2). |
| `skills/spec-cycle/SKILL.md` § Delta no-op, step 4 | Replaces the held token with `mode: full (open findings unreadable)` after the preflight line already printed delta; nothing says to print the replacement (`:417`). | The replacement token is printed (Decision 1). |
| `skills/spec-cycle/SKILL.md` § Two counters, delta pass 2 | An unreadable `<lens>/STATUS` in the open set stops with `open findings unreadable: <lens>/STATUS — pass 2 not dispatched; marker left pending` (`:439`). | No change (Decision 4). |
| `agents/spec-reviewer-correctness.md`, `-edge-cases.md`, `-conventions.md`, `-scalability.md` § Delta scope | A paragraph says a line whose id is `<lens>/STATUS` names no heading and is ignored as scope (`agents/spec-reviewer-edge-cases.md:96`). The block is byte-identical across the four files. | The paragraph is removed from all four; the block stays byte-identical (Decision 6). |
| `README.md` | The `/spec-cycle` usage line reads `<brief-path> [--attest "<reason>"]` (`:10`). | The usage line shows `--full` (Decision 1). |
| `docs/spec-workflow-reference.md` | Describes delta mode and the verdict marker (`:74`, `:112`). | Follows the skill where a rule it states changes (the no-spec row, the snapshot-failure pass). |

## Decisions carried forward

1. **All eleven items are in scope.** The nine in the ticket, plus two VHS-27 review-gate findings that had no ticket: the no-op prints the replacement mode token when step 4 changes it, and the `README.md` usage line gains `--full`. Why: the two extras are one sentence each and sit in text this ticket already edits.
2. **A full pass whose commit snapshot fails still reviews, as a named two-file exception.** It prints one line saying `baseline.commit` was not written, writes and renames the spec copy and the brief copy in that order by the existing temp-then-rename protocol, and dispatches only if both renames succeed. The round counts as reviewed and is not eligible as a delta baseline: the next run takes the no-baseline row, which is already full mode. Every other incomplete set still does not dispatch. A delta pass is unchanged; it never runs without a baseline. Why: a first invocation must work in a project with no commits; nothing new is needed downstream.
3. **An absent spec file is a mode-table row, placed after the attested row and before the brief-changed row.** Spec file does not exist → `mode: full (no spec)`. Rows 1 to 5 (`--full`, marker missing, marker unreadable, pending, attested) keep their tokens, so an ordinary first invocation still prints `mode: full (marker missing)`. A reviewed green or red with a deleted spec cannot reach delta. Why: deleting the spec is the documented way to force a re-author, and the new spec must not be reviewed against the old one's baseline and ledger.
4. **An unreadable status line before delta pass 2 keeps today's stop.** The marker stays pending and a later run does a full review. Why: running pass 2 as a full review would add a branch to the two counters and the halt for a rare failure.
5. **Code drift ignores every ticket's review and attempt directories.** Every path under `docs/specs/TODO/` inside any ticket's `.reviews/` or `.attempt-<n>/` directory is dropped before citations are matched. That includes the `spec.md` and `brief.md` copies an attempt directory holds; they are archives of a superseded attempt and are ignored on purpose. Only another ticket's canonical `docs/specs/TODO/<ID>.brief.md` and `<ID>.spec.md` remain visible as dependencies. Why: this removes the noise that blocks the no-op and keeps a real dependency on another open spec visible.
6. **The stale status-line paragraph is dropped from all four reviewer agents.** Why: `sync.py install` writes the skill and the agents in one run, so there is no older skill to guard against.
7. **Heading text is matched in a fixed order, and a cited line is always used.** For the phrase after `§` or a heading marker: first, a heading whose text equals the phrase; otherwise, every heading whose text begins with the phrase followed by a non-alphanumeric character or end of text ("Decision 8" selects "Decision 8 — …" and not "Decision 80"); otherwise, the longest heading text that is a prefix of the phrase and ends at a non-alphanumeric boundary in the phrase. The first arm that selects anything wins and every tie in it is emitted. When the phrase cut at the first comma selects nothing, the arms are retried against the uncut segment (Decision 8). Separately, every cited line is placed in the predecessor copy and its innermost owning heading is unioned in, whatever the heading match was, an equality match included. Why: the ticket's own fix kept "do not use the line" for an equality match, and its example "§ Design, line 289" is an equality match on an empty parent heading, so that defect would have survived; and with no order, "Decision 8" would select a heading "Decision" by prefix before the intended arm ran.
8. **A location that names two sections, or a line range, puts every one of them in the pass.** Each `§` reference or heading marker in a Where clause opens its own segment, which ends before the next `§` or heading marker; a joining word left at the end of a segment ("and", "or") is not part of the phrase. Decision 7's arms, the comma cut and its retry all apply inside that segment, never against the whole clause ("spec § Decision 8 and § Decision 14" is the two phrases "Decision 8" and "Decision 14"). A cited line range selects the innermost owning heading of every line in the range in the predecessor copy. All of it is unioned. Why: a slightly wider pass is the cheap error; a missed section is the one this ticket exists to stop.
9. **The raw-path sentence is restored to four separate clauses.** Only the double quote is tied to line start. Wording only; no behaviour decision.
10. **Done needs one real delta re-run, before merge, on this ticket's own spec, recorded as it happens.** After the spec goes green, `/spec-cycle` is re-run once with nothing changed and once after a small edit. The printed mode line, the changed-region list and the outcome of each run are recorded in the PR. This run uses the rules installed today, not the fixed ones. The unchanged re-run is not required to reach the no-op: this repo holds untracked `docs/specs/TODO/VHS-41.reviews/` and `VHS-41.attempt-1/` files, so a bare `spec.md` or `correctness.md` citation in the spec makes it dispatch, and that result is accepted as evidence of item 3. The no-op under the fixed rule is asserted by a scenario walk. Scenario walks by reading cover every fix, as in VHS-27.

## Done when

- Each of the three Where forms above resolves to the heading the finding sits in, without emitting every heading. "spec § Design, line 289" selects the section that owns line 289.
- A spec that cites a bare review-artifact filename reaches the no-op when only another ticket's untracked review or attempt files exist.
- The VHS-60 spec contains one scenario per changed behaviour. The archived VHS-27 spec is not edited.
- The no-op prints the replacement mode token when step 4 changes it (Decision 1).
- `README.md` shows `--full` on the `/spec-cycle` usage line (Decision 1).
- A full pass whose commit snapshot fails prints its line, saves the two copies and dispatches; the next run prints `mode: full (no baseline)` (Decision 2).
- A reviewed marker with the spec file deleted prints `mode: full (no spec)`; a first invocation still prints `mode: full (marker missing)` (Decision 3).
- The four reviewer agents carry no `<lens>/STATUS` scope paragraph and their Delta scope blocks are byte-identical (Decision 6).
- The raw-path sentence states four separate clauses (Decision 9).
- One real delta re-run on this ticket's own spec is recorded in the PR, as Decision 10 states.

## Out of scope

- Running delta pass 2 as a full review when a status line is unreadable (Decision 4 keeps the stop).
- Dropping other tickets' briefs and specs from code drift (Decision 5 keeps them).
- A real delta run under the fixed rules after merge and install; Decision 10 asks for the pre-merge run only.
- Known limits of Decision 5, left as they are: a deliberate citation into another ticket's `.reviews/` or `.attempt-<n>/` directory is not seen as drift; and a tracked file under `docs/specs/DONE/<ID>/reviews/` that changes while the loop is open can still match a bare filename.
- Editing the archived VHS-27 spec.
- An author-side check script. That is VHS-26.

## Tier

**Level:** big

## Risks / decisions

1. The pre-merge delta re-run in Decision 10 needs a review-produced green on this ticket's own spec. An operator-attested green selects a full pass, and then that evidence cannot be produced as stated; spec author pins this.
2. VHS-26 edits the same sections of `skills/spec-cycle/SKILL.md` next; line anchors in this brief hold at `0158267` only; spec author pins this.
3. The exact list of joining words and punctuation trimmed from the end of a `§` segment in Decision 8; spec author pins this.

## References

- Plane VHS-60 description and its two comments (2026-10-12, 2026-10-13).
- F1 — Open-finding matching uses equality or the longest heading-text prefix, then discards the line; no match and no line emits every heading (`skills/spec-cycle/SKILL.md:492`).
- F2 — The mode table has eleven rows and none for an absent spec file (`skills/spec-cycle/SKILL.md:363-375`).
- F3 — A full pass takes one `rev-parse HEAD`, and an invalid result fails the commit write, which blocks dispatch (`skills/spec-cycle/SKILL.md:453`).
- F4 — The changed-path set drops only this ticket's brief, spec and reviews directory; citations match by filename-only equality (`skills/spec-cycle/SKILL.md:490`).
- F5 — An unreadable `<lens>/STATUS` before delta pass 2 stops the run with the marker pending (`skills/spec-cycle/SKILL.md:439`).
- F6 — The raw-path sentence reads "with no leading `"`, `=>`, tab, or backslash" (`skills/spec-cycle/SKILL.md:488`).
- F7 — Review-gate findings 5 and 10 were recorded and not acted on (`docs/specs/DONE/VHS-27/review.md:25-27`, `:40-42`).
- `docs/specs/DONE/VHS-27/spec.md`, sections Changed regions, Two counters, Deferred (P2+); `docs/specs/DONE/VHS-27/reviews/round-5/`; `docs/specs/DONE/VHS-27/reconciliation.md` (drift S4).
- Wiki: `decisions/2026-10-13-vhs-27-delta-scoped-review-passes.md`, `comprehension/2026-10-13-vhs-27-delta-review-mode.md`.
- Related: VHS-27 (shipped), VHS-26 (next in the same lane, edits the same skill sections).
- Codex brief review, 2026-10-13 (`gpt-5.6-sol`, read-only): RED, P0 1, P1 4, P2 2; every cited fact confirmed. All seven folded on the operator's word: F-1 and F-2 into Decisions 7 and 8, F-3 into Decision 5 and Out of scope, F-4 into Decision 10, F-5 into Done when, F-6 into Decision 2, F-7 into Decision 3. Delta pass on the revision: F-1 to F-7 closed, one new P1 (F-8, no phrase boundary between two `§` references) folded into Decision 8; no third pass was run.
- F8 — The mode is resolved before Phase 1, so a first invocation has no spec file either (`skills/spec-cycle/SKILL.md:355`); an incomplete artifact set does not dispatch (`skills/spec-cycle/SKILL.md:506`).
- Interview: 2 rounds, exit empty-frontier
