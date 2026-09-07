# Reconciliation Report: VHS-33

> Date: 2026-09-07
> Spec: docs/specs/TODO/VHS-33.spec.md
> Merge: PR #27 — merge commit `464303f` (branch `feat/vhs-33-grilling-handoff-v2`, five commits `c97d4ad`, `27b99b6`, `e9747be`, `ecdfefe`, `648f4ff`); repo home is now `Vigil-Harbor/vigil-skills`
> Plane state: Done (group: completed)

## Summary

Everything the spec scoped shipped, in exactly the five files it named, and all thirteen decisions are reflected in the merged text. The one drift is wording: five spec-quoted sentences were re-phrased during the three CodeRabbit rounds (two on the personal-account run, three after the repo moved to the org), and `(D5, D6)` was dropped from the shipped step-5 `fence-empty` bullet. None of the rewordings adds a construct, so brief decision 12 holds; the reconciliation counts them as one Drifted item.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/grilling/SKILL.md` | Yes | +15/−10 — seed `id` + `ref:` descent paragraph, plain-language paragraph, six exits + `fence-empty` paragraph, v2 hand-off block, callers-map sentence, both `stop` sentences |
| `skills/spec-cycle/SKILL.md` | Yes | +41/−9 — 2f-i step 1 lens-qualified seed ids, step 4 `ref:` matching, step 5 line + six list-rule bullets, failure-modes bullet |
| `skills/spec-brief/SKILL.md` | Yes | +2/−2 — `:140` F-item mapping; `:143` fence-reason bullet |
| `skills/grill-me/SKILL.md` | Yes | +1/−0 — third failure-modes bullet for `fence-empty` |
| `docs/spec-workflow-reference.md` | Yes | +2/−2 — `:23` termination shapes; `:35` hand-off paraphrase |

Unexpected files in diff (not in spec): none. Files to leave alone: `git diff --stat 20d8acd 464303f` over `agents/`, `skills/ship-spec/`, `skills/spec-close/`, `docs/specs/DONE/`, `lint.py`, `sync.py`, `tests/`, `README.md`, `AGENTS.md` is empty (checklist row 14).

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| D1 | Caller IDs survive the hand-off | Confirmed | `skills/grilling/SKILL.md:18` — "Each seed item may carry an optional **`id`** — a caller-stable string the primitive echoes back as `ref:` on every Settled and Open item that descends from it"; `:129` rolled-up line ends `)**. ref: <…>` |
| D2 | `ref:` holds zero or more IDs | Confirmed | `skills/grilling/SKILL.md:124` — `ref: <id>[, <id>…] \| none` |
| D3 | Fact items get their own shape | Confirmed | `skills/grilling/SKILL.md:128` — `**F<n> — <fact needed>** — unresolved because: <fact not established \| stopped>`; the Q-item reason list at `:127` no longer carries `fact not established`; `:74` and `:88` untouched (no hunk) |
| D4 | `fence-empty` is a distinct exit token | Confirmed | `skills/grilling/SKILL.md:106` — six tokens; `:108` — "nothing is rendered and the exit is `fence-empty`"; header at `:121` lists it |
| D5 | A fence-empty grill still consumes the once-per-halt bound | Confirmed | `skills/spec-cycle/SKILL.md` 2f-i closing paragraph ("runs at most once per invocation") is context in the diff, not a hunk; step-5 bullet — "The menu re-renders with options 1–3." |
| D6 | A fence-empty grill is persisted | Confirmed | `skills/spec-cycle/SKILL.md` 2f-i failure-modes bullet — "A `fence-empty` exit is the same shape: nothing moved, the empty summary is persisted, the menu re-renders with 1–3."; step-3 guard untouched |
| D7 | The archived VHS-32 spec is not edited | Confirmed | `docs/specs/DONE/VHS-32/` absent from the diff (row 14); rows 5 and 10 re-assert VHS-32 rows 4/6/7 and pass |
| D8 | `/spec-brief` and the workflow reference are in scope | Confirmed | both files in the diff (Scope table) |
| D9 | Plain-language rule, for the primitive's rounds only | Confirmed | `skills/grilling/SKILL.md:59` — paragraph beginning `**Plain language.**`; no other skill's operator-facing block touched |
| D10 | ASD-STE100 writing rules, not its dictionary | Confirmed | `skills/grilling/SKILL.md:59` — "Write in the ASD-STE100 style … the dictionary is not applied" |
| D11 | Operator-supplied facts are out of this ticket | Confirmed | row 16: added lines in `grilling` and `spec-brief` match none of `operator claim\|verif\|qualifier\|source: operator` |
| D12 | The spec stays inside the brief | Confirmed | no new construct beyond the spec's additions roll-up; the review-round rewordings below are clarifications of existing sentences |
| D13 | Scale is an explicit non-factor | Confirmed | `skills/grilling/SKILL.md:137` size-bound sentence byte-identical to pre-edit `:132` (row 9); CodeRabbit round 3 asked to widen it and was declined on that fence |
| — | Spec-quoted text in Designs 2, 3, 5, 6 | Drifted | Five sentences differ from the spec's quoted text, all CodeRabbit-raised and each re-checked against rows 6, 7, 9, 10, 11, 16: (a) `grilling:110` `stop` sentence — a `defer` is not a settling answer, "pending explorations" (not "in flight"), with the reason the in-flight state is unreachable; (b) `grilling:156` `stop` bullet retitled "with explorations pending", same wording; (c) `grilling:135` `ref:` paragraph gained two sentences — `ref: none` exists only in a run where some seed item carried an `id`, and the `ref: none` case is "a decision whose question an established fact raised rather than a seed item", with "relying on a fact never changes an item's ids"; (d) `spec-cycle` step 5 `unreferenced decisions applied` counts Settled items "with `ref: none` — or with no `ref:` field at all", matching step 4; (e) `spec-brief:143` later-round example uses `<n>` not a literal `2`. Also, `(D5, D6)` was dropped from the shipped step-5 `fence-empty` bullet (brief-decision labels mean nothing in the skill file; PR body records it). |

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Hand-off block carries optional `ref:` on every Settled and Open item incl. rolled-up; defines `F<n>` Open forms; lists `fence-empty`; per-round contract carries the plain-language rule | Met | rows 4, 6, 7, 8 all pass on `464303f` — `grep -c 'ref:' skills/grilling/SKILL.md` = 7 lines; `grep -c fence-empty` = 3; `grep -c '^\*\*Plain language\.\*\*'` = 1 |
| 2 | 2f-i passes finding ids as seed ids, reads `ref:` in step 5, persists a `fence-empty` summary; once-per-halt bound unchanged | Met | row 10 — all pinned phrases present (`<lens>/<finding-id>`, "by its `ref:` ids, never by title", `grill applied (exit: <token>):`, `unreferenced decisions applied: <n>`, "never re-dispatches reviewers", "at most once per invocation"); `grep -c 'total_p0p1 == 0'` unchanged at 2 |
| 3 | `/spec-brief` Phase 4 names the `F<n>` Open form; `/grill-me` names `fence-empty`; workflow reference matches | Met | `spec-brief:140` — "An `F<n>` item is written as `<fact needed> — not established; spec author pins this`"; `grill-me` `## Failure modes` has three bullets, third names `fence-empty`; `spec-workflow-reference.md:23` contains "altitude fence" twice and `:35` contains `ref:` and "unestablished fact" |
| 4 | `lint.py --strict` zero ERROR, no new `missing-requires` WARN; `sync.py status` clean; `sync.py push` round-trips | Met | `python lint.py --strict` exit 0 with `missing-requires` count 2 (unchanged: `review-pr`, `ship-spec`); `python sync.py install` applied 4 actions from `464303f` and `sync.py status` then showed only pre-existing `dst-only` entries; push round-trip verified on the worktree during ship (row 15) |
| 5 | PR #26 thread 3945500857 closed against the merged change; 3945500860 answered with the `F<n>` shape and pointed at VHS-36 | Met | replies 3952623796 and 3952623913 posted 2026-09-07; both threads `isResolved: true` |

## Test Plan

The spec's `## Test command` is `N/A`; the sixteen-row review checklist is the gate.

| Test | Exists? | Location |
|---|---|---|
| Rows 1, 3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 16 | Yes — re-run on `main` at `464303f` at close, all pass | greps recorded in this report's Decisions and Acceptance tables |
| Rows 2, 5, 9, 15 | Yes — run at ship (`c97d4ad`) and after each review-round commit (`27b99b6`, `e9747be`, `ecdfefe`, `648f4ff`) in the worktree; row 9's hunk set re-checked at `648f4ff` (no hunk in pre-edit `:1–17`, `:19–32`, `:59–100`, `:136–150`; `:132` byte-identical) | PR #27 body and review-round commit messages |
| CodeRabbit | Yes — three incremental reviews under the org plan: 5 findings, 3 fixed, 2 skipped with replies; verdict APPROVED before merge, 10/10 threads resolved | PR #27 |

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:

- Decision (multi-judgment): the hand-off carries the caller's ids and 2f-i matches decisions to findings by `ref:` only, never by title (D1, D2); decisions descend only from their question, so `ref: none` is a fact-raised question's mark and exists only in a tagged run (review-round clarification, CodeRabbit-raised); an unresolved fact is an `F<n>` item, not a question (D3); `fence-empty` is a success token whose brief is hollow by design — this narrows wiki decision `2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write` § 5 ("Rejected — a success token for an empty interview"): `empty-seed` stays the only halt (D4, Risk 2); a fence-empty grill still consumes the once-per-halt bound, with no re-offer (D5).
- Comprehension: the hand-off contract went to v2 — `ref:` field, `F<n>` Open form, sixth exit token, plain-language rule for rendered rounds — and the three callers plus the reference paraphrase moved with it in one PR; what would break is any consumer that greps the v1 line shapes; the size bound and the fact-finding section are untouched (VHS-36's surface).
- Judgment calls worth carrying: the size-bound sentence was left byte-identical under the spec's row 9 even though CodeRabbit argued it undercounts pending F-items — a tighter bound is a separate ticket; the `Interview: 1 rounds` example was kept because it renders a fixed template.

RECONCILED: yes DRIFT: 1
