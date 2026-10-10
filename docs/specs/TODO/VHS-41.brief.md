# VHS-41 — review-pr: body-level "outside diff range" findings are invisible to the comment fetch
**Status:** Backlog · **Priority:** low · **Assignee:** unassigned
**Created:** 2026-09-08 · **Plane:** VHS-41 (80abb94f-6cd5-44a7-84f1-716b17704947, Backlog)
**Origin:** Filed 2026-09-08 from the VHS-36 review session. On PR #28, CodeRabbit's incremental review carried a Minor finding only in its review body, under "Outside diff range comments"; `/review-pr`'s inline-comment fetch never saw it, and it was triaged only after the operator pasted the review text. A second inline finding in the same session was dropped by post-filtering the comment fetch with `sed` and `head`. The handoff for that session listed the gap as ticket-worthy; this ticket carries it.

## Problem

`/review-pr` Step 2 fetches CodeRabbit's inline review comments (`pulls/{N}/comments`) and triages those. CodeRabbit also reports findings in the verdict review's body under an "Outside diff range comments" section (`pulls/{N}/reviews/{id}` `.body`). Those findings never become threads, so the skill never sees them. On PR #28 (VHS-36) a body-level finding on `skills/grilling/SKILL.md` § Failure modes was only caught because the operator read the review body by hand (fixed in round 2 as the seven-cause enumeration). A second finding in the same session was truncated away by post-filtering the comment fetch with `sed` and `head`.

## Why it matters

A finding the skill never sees is a finding that ships. On PR #28 the body-level item was a real defect (an incomplete failure-mode enumeration) that reached the merge only because a human read the review body. The skill's per-thread reply mechanism exists so the PR carries a record of every judgment call; a body-level item today gets no record even when it is fixed, so the audit trail has a hole exactly where the skill is blind.

## Scope (verified against current files, 2026-09-08)

| Path | Current | Change |
|---|---|---|
| `skills/review-pr/SKILL.md` Step 2 (`:63-83`) | Fetches the latest verdict review as `{id, state, submitted_at, body}` (`:68-70`); the body's only consumer is the infrastructure-error check (`:79`). Inline findings come from `pulls/<N>/comments` with `in_reply_to_id == null` (`:75-77`). | Read the "Outside diff range comments" and "Nitpick comments" sections of the verdict review body into the finding set (Decision 1). Fetches use `--paginate`; no post-filtering of the stream (Decision 5). |
| `skills/review-pr/SKILL.md` Step 3 (`:86-115`) | Triage rules name the Outside-diff, Duplicate, and Nitpick sections "in the review body" (`:111-114`) and say Nitpick "appears in review body summary, not inline" (`:95`), but no step extracts items from them. | Body-level items enter the same triage table with their own severity labels; Duplicate section stays unread (Decision 1). |
| `skills/review-pr/SKILL.md` 6a/6b (`:163-241`) | 6a's new-findings detection (`:195-196`) and 6b's fetch (`:224-226`) read only `pulls/<N>/comments`; incremental review bodies are never fetched. | Read the body of every verdict review newer than `PREV_REVIEW_ID` in each cycle; 6a's count includes body items so a body-only review is not "nothing new" (Decision 2). |
| `skills/review-pr/SKILL.md` 6c guard (`:277`), 6e report (`:362`), edge cases (`:382`, `:397`) | A finding with no comment id gets no reply; the report lists it as "Reply skipped"; two edge cases restate the skip. | Replace the skip with one PR-level comment per round listing each body-level item's fix SHA or skip reason (Decision 3); report and edge cases updated to match. |
| `skills/review-pr/SKILL.md` fast path (`:156-161`), cycle cap (`:234`) | `round1_finding_count` and the three-cycle cap count inline findings only. | Body-level findings join the same population (Decision 4). |

## Decisions carried forward

1. **Two body sections are read, one is not** — read "Outside diff range comments" and "Nitpick comments" from the review body into triage; "Duplicate comments" stays unread. Why: those two sections can carry a new finding with a severity label, and the skip on a nitpick becomes a recorded judgment; duplicates repeat inline findings the thread loop already handles.
2. **Every newer verdict review's body is read** — in Step 2 and in each 6a/6b cycle, the body of every verdict review newer than the last one handled is read, and 6a's new-findings detection counts body items. Why: the PR #28 finding lived in the incremental review; a fix confined to Step 2 would not have caught it, and without the count change a body-only review reads as "nothing new".
3. **Dispositions go in one PR-level comment per round** — each body-level item is listed with its fix SHA or skip reason in a single PR comment posted with that round's per-thread replies. Why: a body item has no comment id, so the reply endpoint cannot be used; a PR comment is visible where a reviewer looks without pretending a thread exists.
4. **Body-level findings are findings** — they count toward the fast-path predicate, the three-cycle cap, and every report line. Why: one definition of "finding"; a fixed body item is a push like any other and deserves the incremental wait.
5. **The fetch-truncation rule ships here** — comment and review fetches use `--paginate`, and a rule forbids trimming the fetch stream with `sed` or `head`, recorded in the skill's edge cases. Why: same failure class (findings dropped before triage), and the ticket names it.

## Done when

- A PR whose only CodeRabbit finding is body-level ("Outside diff range") produces a triage row and a posted disposition.
- `lint.py --strict` zero ERROR; `sync.py status` clean.

## Out of scope

- Reading the "Duplicate comments" section of the review body (Q1).
- Adding the missing `requires:` block to `skills/review-pr/SKILL.md`; the pre-existing `missing-requires` lint warning stays tracked as-is (Q6).

## Scale

**Factor:** no

## Risks / decisions

_(none open from the interview)_

## References

- `skills/review-pr/SKILL.md:68-70`, `:79` — Step 2 fetches the verdict review body; only the infrastructure-error check reads it.
- `skills/review-pr/SKILL.md:95`, `:111-114` — Step 3 names the three body sections but no step extracts their items.
- `skills/review-pr/SKILL.md:195-196`, `:224-226` — 6a detection and 6b fetch read comments only.
- `skills/review-pr/SKILL.md:277`, `:362`, `:382`, `:397` — body-level items get no reply; reported as "Reply skipped".
- `skills/review-pr/SKILL.md:131-138`, `:252-255` — commit message lists Fixed/Skipped; replies use `pulls/<N>/comments/<id>/replies`, which a review body lacks.
- `skills/review-pr/SKILL.md:156-161` — fast-path predicate keys on `round1_finding_count`.
- `skills/review-pr/SKILL.md:1-5` — no `requires:` block; `python lint.py skills/review-pr/SKILL.md` reports 0 ERROR, 1 WARN missing-requires.
- GitHub `Vigil-Harbor/vigil-skills` PR #28, review 5135914911 body — live specimen of the body shape: `<details><summary>⚠️ Outside diff range comments (N)</summary>` → per-file `<details><summary><path> (n)</summary>` → `` `L-L`: _category_ | _severity_ | _tag_ `` item line, bold title, prose, nested "🤖 Prompt for AI Agents" block; the Nitpick and Duplicate sections share the shape. The body-level finding was in the incremental review, not the first verdict review 5135878266.
- Plane VHS-41 (`80abb94f-6cd5-44a7-84f1-716b17704947`); handoff `.claude/handoffs/2026-09-07-181007-vhs-36-merged-installed-spec-close-next.md` § Potential Gotchas.
- Interview: 1 rounds, exit empty-frontier
