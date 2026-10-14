# VHS-26 — spec-cycle: author-side ground-truth gate + structured apply-findings phase (GAV-13 post-mortem)
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-10-13 · **Plane:** VHS-26 (18bfa979-46a8-4c0e-b998-a408fff0b4b2, Backlog)
**Origin:** Filed 2026-07-29 from the post-mortem of a spec-cycle run on another project's ticket (GAV-13), where the review loop diverged instead of converging. The 2026-10-11 sprint plan (wiki `overview/2026-10-11-skill-pack-distillation.md` §6) placed it in Wave 2 and folded a structural lint script (`check_spec.py`) into it. The first brief (2026-10-13, three-round interview) carried the script and a divergence stop as well. **This is attempt 2.** Attempt 1 went red after four rounds (gate 11 → 6 → 2 → 3); every round-4 P0 was against script and ledger machinery the review loop itself had added. The operator chose to narrow: the script moved to VHS-61 and the divergence stop to VHS-62, and this brief keeps the author-side prose rules only. Attempt 1's brief, spec, reviews and run report are at `docs/specs/TODO/VHS-26.attempt-1/`.

## Problem

GAV-13 (YouTube digest chain hardening, 2026-07-29) went through rounds 4–6 with the design sections stable and sound, while three consecutive post-round patch passes each introduced new P1s into the Runbook — P1 counts went 4 → 3 → 7. The loop diverged instead of converging.

Root cause (from the session post-mortem): the spec-cycle process makes reviewers read code ("verify every claim by reading the actual files" is in the four reviewer agent prompts) but places no ground-truth obligation on the author — neither at initial authoring nor, worse, during the unstructured apply-findings step between rounds. Concrete failures, all one Read away from prevention:

- Runbook steps written against a scheduler never read: the scheduler sandboxes scripts to one directory and refuses to fire paused jobs, so the authored rehearsal mechanism could not execute at all.
- Reviewer-supplied facts embedded unverified (a "15 records / 9 enabled" count from a round-5 report; the live file says 20/11).
- Two reviewers' suggested wordings applied verbatim in one pass without composing them — producing a direct contradiction (wrapper form vs pinned signatures) that two lenses then re-found independently.
- A mechanism inherited from precedent specs unverified: "manual paused fires" appears in two earlier specs' Runbooks as the scheduler-level rehearsal mechanism, and does not work against the current scheduler (the blocking is deliberate and tested). The conventions lens treats the prior-spec corpus as authoritative, so false precedent propagates.

## Why it matters

Every defect was caught, but only by the reviewers, and only after a round was spent on each. This is about making the author's loop contact ground truth so the reviewers stop being the first readers of the code. Without that, a revision can add P1s as fast as it removes them, and the loop runs to its cap without converging.

## Scope (verified against current files, 2026-10-13)

| Path | Current | Change |
|---|---|---|
| `skills/spec-cycle/SKILL.md` § Phase 1 — Author v1 spec | Lists the required sections and how to write them; no obligation for the author to read the code behind a claim, and no ledger (`skills/spec-cycle/SKILL.md:384-405`). | Add the author-side ground-truth obligation and the ground-truth ledger (Decisions 1, 2, 3, 6), and the precedent rule (Decision 5). |
| `skills/spec-cycle/SKILL.md` § 2e. Revise or rewrite by pass index | Routes every P0/P1 to fold, defer or reject and names propagation sites before editing; nothing re-verifies a reviewer-supplied fact, re-reads the sites after the edits, or checks composition of overlapping wordings (`skills/spec-cycle/SKILL.md:706-722`). | Add the three apply-findings rules (Decision 4); the ground-truth obligation applies to every revision (Decisions 1, 5). |
| `skills/spec-cycle/SKILL.md` § Round artifacts and § 2b (reviewer dispatch) | A round saves `spec.copy.md`, `brief.copy.md` and `baseline.commit` before dispatch (`skills/spec-cycle/SKILL.md:444-460`); each lens receives the same inputs (`:511`). | The ground-truth ledger is one more file of a dispatched round; only the correctness lens is given its path (Decisions 2, 7). |
| `agents/spec-reviewer-correctness.md` | Does not receive or read a ledger. | Spot-check of the ground-truth ledger (Decision 7). The `# Delta scope` block (`:90`) is not edited. |
| `agents/spec-reviewer-conventions.md` | No rule about precedent or prior specs (grep, no hits). | One rule under the critique lens (Decision 5). The `# Delta scope` block (`:93`) is not edited. |
| `docs/spec-workflow-reference.md`, `README.md`, `AGENTS.md` | Describe the spec-cycle loop without an author read obligation or a ground-truth ledger. | Matching text, kept short (Decision 8). |

## Decisions carried forward

1. **Author-side ground-truth obligation.** In Phase 1 and in every revision, a spec sentence that states what a system will do when run needs a `file:line` anchor that the author read in this run. An anchor taken from a reviewer report, a prior spec, a wiki page or the brief tells the author where to look; it does not count until the author has read the line. (First interview Q3 A: runtime-behavior claims only, because covering every claim about current code duplicates the correctness lens.)
2. **The gate is a per-round ground-truth ledger file** (first interview Q2 B). One file per dispatched round, saved with that round's other artifacts in the ticket's reviews directory. Each row holds four things: the claim, the spec section it sits in (plain heading text), the `file:line` anchor, and the round in which the author read it. A spec with no runtime-behavior claims says so in one explicit line. The file is called the "ground-truth ledger" everywhere, because `ledger.md` already names the disposition ledger.
3. **Ledger rows are plain text for a human and one reviewer to read.** No machine-checked grammar, no section identity scheme, and no requirement that the ledger equal a computed set. Why: attempt 1 tied the ledger to the changed-regions algorithm and drew two P0s for it.
4. **All three apply-findings rules are added to 2e** (first interview Q4 B): re-verify every reviewer-supplied fact against live files before embedding it; after the edits, re-read every section that consumes the edited decision; do not apply two findings' suggested wordings to overlapping text without composing them into one intended result first. Why: naming propagation sites is not the same as re-reading them after the edit.
5. **"Precedent is not evidence" reaches the conventions agent** (first interview Q6 B). The rule goes in the skill's authoring and revision text and as one rule in `agents/spec-reviewer-conventions.md`: a mechanism cited from a prior spec is checked against live code before it is cited or inherited. Why: the false precedent in the originating incident came through that lens.
6. **Runbook executability is part of the obligation** (first interview Q7). A runbook step that invokes code is a runtime-behavior claim and needs an anchor like any other; one sentence tells the author to trace the call chain to the code that enforces the behavior. No separate mechanism.
7. **The correctness agent spot-checks the ledger; no other lens receives it** (first interview Q11 A). It samples rows, reads each sampled anchor fresh, and files a finding when an anchor does not support its claim, when the ledger is absent, or when its own normal read of the spec finds a runtime-behavior claim with no row. Its existing verification duties stay as they are. Why: one lens checks that the author's evidence holds, and the others stay independent of the author's view. This spot-check is the only enforcement in this ticket.
8. **Other files.** Matching text in `docs/spec-workflow-reference.md`, `README.md` and `AGENTS.md`; agent edits limited to the correctness and conventions agents, outside the shared `# Delta scope` block.

## Done when

The ticket states no acceptance criteria. Its proposed changes, as narrowed for attempt 2:

1. Author-side ground-truth obligation at authoring and at every revision: any spec sentence that states what a runtime will do — fire, register, block, resolve a path, recompute a schedule — carries a `file:line` anchor the author read in that run, not one inherited from a reviewer report, a prior spec, or the brief. A ground-truth ledger (claim → spec section → anchor → round read) is written for every dispatched round (Decisions 1, 2, 3).
2. The apply-findings step is structured: (a) re-verify every reviewer-supplied fact (counts, paths, mechanisms) against live files before embedding; (b) after the edits, re-read every section that consumes the edited decision, not just the section the finding pointed at; (c) never apply two findings' suggested wordings to overlapping text without an explicit composition check (Decision 4).
3. Precedent is not evidence: a mechanism cited from a prior spec's Runbook is re-verified against the live code path before inheritance, in the skill and in the conventions agent (Decision 5).
4. Runbook executability: the author traces the exact call chain before writing any step that invokes it (Decision 6).
5. The correctness agent receives the ground-truth ledger and spot-checks it (Decision 7).
6. The four agents' `# Delta scope` blocks are still byte-identical, and the repo's lint and test suite pass.

## Out of scope

Split to other tickets:

- **`check_spec.py` and every mechanical check** — the structural lint (required sections, criterion paired with a verify command, no TBDs, deferred rows well-formed), any script check of the ledger (anchor file exists, line in range, well-formedness), the fix-and-re-run rule, the no-Python fallback, and a new `scripts/` directory or test file. All of it is VHS-61. Nothing in this ticket runs a program.
- **The divergence stop** (halt when the P0/P1 count does not go down) and any change to 2d gating, the 2f halt block or the mode table. That is VHS-62.

Fences from attempt 1 (each was review-added machinery that drew new findings):

- No link between the ledger and the changed-regions algorithm: no section identities, no computed expected coverage, no tombstones for removed headings.
- No ledger or addendum for a revision that has no following reviewer dispatch (the final-pass rewrite and grill edits). The ledger exists for a dispatched round only.
- No new halt, no new marker state, no rollback, no retry rule, no temp-file cleanup step and no size bounds.
- No change to `sync.py`, `tests/`, `/ship-spec`, `/spec-close` or `/spec-brief`.

Other fences:

- No ledger backfill for specs written before this ships. On a re-run, the ledger covers only the claims in sections that pass writes or edits (first interview Q17 A).
- Attest mode is unchanged (first interview Q18 A).
- The guarantee scan (the 2d rule that withholds green while an in-scope P0 or P1 sits undischarged) is unchanged.
- The reviewer lenses' existing verification duties do not change. The two additions are the precedent rule in the conventions agent (Decision 5) and the ledger spot-check in the correctness agent (Decision 7); this rewords the ticket's non-goal. The edge-cases and scalability agents are not edited.
- The GAV-9/GAV-10 rehearsal-mechanism discrepancy is a separate concern of that project, referenced here only as evidence.

## Tier

**Level:** big

## Scale

**Factor:** no

## Risks / decisions

1. Done-when wording — the ticket has no acceptance-criteria section, so `## Done when` lists its proposed changes as narrowed; the exact, testable form of each bullet is not established; spec author pins this.
2. Ledger file name and its place in the round-artifact rules — the name must not collide with the disposition `ledger.md`, and whether a round with a missing ground-truth ledger counts as an incomplete artifact set for the mode table is not established; spec author pins this, without adding a mode-table row (the prose row references at `skills/spec-cycle/SKILL.md:378`, `:380` and `:458` must not move).
3. Spot-check sample size and finding severity — how many rows the correctness agent samples, and the severity of an unsupported anchor or a missing ledger, are not established; spec author pins this.
4. Enforcement is by review only — with the script in VHS-61, nothing mechanical stops a dispatch without a ledger; the correctness agent's finding is the only check until VHS-61 ships. This is accepted for this ticket and is not a gap for the spec to close.
5. This spec is a prose change to a skill and two agents; its test plan is a review checklist plus the repo's existing lint and unit tests, not new tests; spec author pins the checklist.

## References

- Plane VHS-26 (18bfa979-46a8-4c0e-b998-a408fff0b4b2), read from the tracker 2026-10-13; shared memory returned HTTP 502.
- Split tickets filed 2026-10-13: VHS-61 (782f8148-d5e4-48db-81b4-bca4b3ac6f08, `check_spec.py` structural lint) and VHS-62 (f05bf80d-9f1b-42eb-92b9-13e0345d98ae, divergence stop). Both carry the decisions the first interview settled for them and the lessons of attempt 1.
- Attempt 1: `docs/specs/TODO/VHS-26.attempt-1/` — `brief.md` (the first brief, 20 settled decisions), `spec.md` (301 lines), `reviews/` (rounds 1–4, verdict red, gate 3), `run-report.md`. Round-4 P0s: `reviews/round-4/correctness.md` F-1 and F-2, `reviews/round-4/edge-cases.md` F-1.
- F1 — Phase 1 authoring lists required sections and carries no author read obligation and no ledger: `skills/spec-cycle/SKILL.md:384-405`.
- F2 — 2e routes every P0/P1 to fold/defer/reject and names propagation sites before editing; no fact re-verification, no composition check: `skills/spec-cycle/SKILL.md:706-722`.
- F3 — round artifacts are defined at `skills/spec-cycle/SKILL.md:444-460`; reviewer dispatch at `:511`; the disposition ledger at `:462`.
- F4 — the conventions agent has no precedent rule (grep, no hits); its `# Delta scope` block is at `agents/spec-reviewer-conventions.md:93` and the correctness agent's at `agents/spec-reviewer-correctness.md:90`; the four agents' blocks are byte-identical.
- F5 — the guarantee scan is prose in 2d: `skills/spec-cycle/SKILL.md:698`.
- F6 — prose references to mode-table rows: `skills/spec-cycle/SKILL.md:378`, `:380`, `:458`.
- F7 — the repo's tests are stdlib `unittest`, Python 3.8+ stdlib only: `AGENTS.md:7`.
- Grounded at `fc20f94` (local `main` in sync with `origin/main`).
- Tier: `big`, chosen by the operator for the first brief and not re-asked after the narrowing.
- Interview: 3 rounds, exit empty-frontier (first brief). The narrowing of 2026-10-13 was the operator's choice at the attempt-1 halt menu (option 3), with the split made at the operator's instruction; no second interview was run.
