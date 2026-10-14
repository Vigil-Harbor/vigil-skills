# VHS-26 — spec-cycle: author-side ground-truth gate + structured apply-findings phase (GAV-13 post-mortem)
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-10-13 · **Plane:** VHS-26 (18bfa979-46a8-4c0e-b998-a408fff0b4b2, Backlog)
**Origin:** Filed 2026-07-29 from the post-mortem of a spec-cycle run on another project's ticket (GAV-13), where the review loop diverged instead of converging. The 2026-10-11 sprint plan (wiki `overview/2026-10-11-skill-pack-distillation.md` §6) placed it in Wave 2 after VHS-43 and VHS-27, and folded a structural spec lint script (`check_spec.py`) into it. VHS-43, VHS-27 and VHS-60 have since rewritten the revision and re-run rules of the same skill, so the ticket's proposals were re-grounded against the skill at `fc20f94` and settled in a three-round interview on 2026-10-13.

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
| `skills/spec-cycle/SKILL.md` § Phase 1 — Author v1 spec | Lists the required sections and how to write them; no obligation for the author to read the code behind a claim, and no ledger (`skills/spec-cycle/SKILL.md:384-405`). | Add the author-side ground-truth gate (Decisions 2, 3, 6, 7) and the precedent rule (Decision 5). |
| `skills/spec-cycle/SKILL.md` § 2e. Revise or rewrite by pass index | Routes every P0/P1 to fold, defer or reject and names propagation sites before editing; nothing re-verifies a reviewer-supplied fact, re-reads the sites after the edits, or checks composition of overlapping wordings (`skills/spec-cycle/SKILL.md:706-722`). | Add the three apply-findings rules (Decision 4); the gate applies to every revision pass (Decisions 2, 15). |
| `skills/spec-cycle/SKILL.md` § Phase 2, before 2b (reviewer dispatch) | Reviewers are dispatched after a cold read of the spec; no structural check runs first (`skills/spec-cycle/SKILL.md:505-511`). | Run `check_spec.py` before every dispatch (Decisions 1, 8, 9, 13, 14, 15). |
| `skills/spec-cycle/SKILL.md` § 2d / 2f (gate and halt) | The loop halts only when the round cap is reached, or after delta pass 2 (`skills/spec-cycle/SKILL.md:799`). | Add the divergence stop (Decisions 10, 11, 12). |
| `skills/spec-cycle/scripts/check_spec.py` (new) | Does not exist; `skills/spec-cycle/` holds only `SKILL.md`. Three other skills ship a `scripts/` directory. | New stdlib script (Decisions 1, 9, 14, 15). |
| `tests/test_check_spec.py` (new) | Does not exist; `tests/` holds three stdlib `unittest` files. | New stdlib `unittest` file for the script (Decision 16). |
| `agents/spec-reviewer-conventions.md` | No rule about precedent or prior specs (grep, no hits). | One rule under the critique lens (Decision 5). The `# Delta scope` block is not edited. |
| `agents/spec-reviewer-correctness.md` | Does not receive or read a ledger. | Spot-check of the ledger (Decision 9). The `# Delta scope` block is not edited. |
| `docs/spec-workflow-reference.md`, `README.md`, `AGENTS.md` | Describe the spec-cycle loop without a pre-dispatch check, a ledger or a divergence stop. | Matching text (Decision 16). |

## Decisions carried forward

1. **`check_spec.py` ships in this ticket** (Q1 A). The structural lint script from the sprint plan is part of VHS-26, with the prose rules. Why: both gates sit at the same point of the loop, before reviewer dispatch, and one spec means one re-grounding of the skill.
2. **The gate is a per-round ledger file beside the spec** (Q2 B). It lives in the ticket's reviews directory and records claim, `file:line` anchor and the round in which the author read it. Why: it fits the existing round artifacts and does not add a spec section that later passes can break.
3. **The gate covers runtime-behavior claims only** (Q3 A): a sentence that states what a system will do when run. Why: covering every claim about current code duplicates the correctness lens and grows with spec size.
4. **All three apply-findings rules are added to 2e** (Q4 B): re-verify every reviewer-supplied fact against live files before embedding it; after the edits, re-read every section that consumes the edited decision; do not apply two findings' suggested wordings to overlapping text without a composition check. Why: naming propagation sites is not the same as re-reading them after the edit.
5. **"Precedent is not evidence" reaches the conventions agent** (Q6 B). The rule goes in the skill's authoring and revision text and as one rule in `agents/spec-reviewer-conventions.md`: a mechanism cited from a prior spec is checked against live code before it is cited or inherited. Why: the false precedent in the originating incident came through that lens.
6. **Runbook executability is part of the gate** (Q7). A runbook step is a runtime-behavior claim and needs an anchor like any other; one sentence tells the author to trace the call chain for a step that invokes code. No separate mechanism.
7. **A missing or incomplete ledger is a blocking script failure** (Q16 A). An explicit "no runtime-behavior claims" entry is allowed. Why: a warning makes the obligation optional again.
8. **Script failure handling** (Q8 A). The author fixes the spec and re-runs the script before reviewers are dispatched; no review round is used. If the same failure remains after one fix attempt, halt. Why: this is the round the lint exists to save.
9. **The script checks ledger anchors, and the correctness agent spot-checks the ledger** (Q10 A, Q11 A). The script verifies that each anchor's file exists and the line is in range; a path outside the tree is a warning. The correctness agent samples the ledger in addition to its present duties; the other lenses do not receive it. Why: existence and range are cheap, and one lens checks that an anchor supports its claim while the others stay independent of the author's view.
10. **Divergence trigger** (Q5 B). The loop halts when the P0/P1 count does not go down from one round to the next. Why: the ticket's "any new P1" would halt most loops at round 2.
11. **The divergence stop reuses the 2f halt menu** (Q12), with a first line that says the count did not go down. Why: that menu already offers a scope cut and a grilling round.
12. **Divergence compares consecutive passes inside one invocation only** (Q13 A). Why: a full pass and a delta pass count different scopes, so a comparison across invocations gives false stops.
13. **The script runs before every reviewer dispatch** (Q15): each full pass and each delta pass. It does not run on a no-op re-run, where nothing is dispatched.
14. **No Python on the host** (Q14 A): print one warning line, skip the script, continue. Why: the repo is public and the skill must run on any agent.
15. **Deferred rows: well-formedness only** (Q9 A). The script checks that rows in the spec's deferred-findings section are well-formed. Its other checks are those of the sprint plan: required sections, every acceptance criterion paired with a verify command, no TBDs.
16. **Other files** (Q19). New `skills/spec-cycle/scripts/check_spec.py` and `tests/test_check_spec.py` (stdlib `unittest`); matching text in `docs/spec-workflow-reference.md`, `README.md` and `AGENTS.md`; agent edits limited to the conventions and correctness agents, outside the shared `# Delta scope` block.

## Done when

The ticket states no acceptance criteria. Its proposed changes, as amended by the decisions above:

1. Author-side ground-truth gate (authoring phase + every patch pass). Any spec sentence that states what a runtime will do — fire, register, block, resolve a path, recompute a schedule — must carry a `file:line` anchor the author read in that session, not one inherited from a reviewer report, a prior spec, or the brief. It is enforced by a verification ledger (claim → anchor → read-when) kept alongside the spec (Decisions 2, 3, 7, 9).
2. The apply-findings step is structured: (a) re-verify every reviewer-supplied fact (counts, paths, mechanisms) against live files before embedding; (b) after each edit, re-read every section that consumes the edited decision, not just the section the finding pointed at; (c) never apply two findings' suggested wordings to overlapping text without an explicit composition check (Decision 4).
3. Divergence stop rule: the loop halts with the scope-reassessment menu instead of another patch pass (Decisions 10, 11, 12).
4. Precedent is not evidence: a mechanism cited from a prior spec's Runbook is re-verified against the live code path before inheritance (Decision 5).
5. Runbook executability: the author traces the exact call chain before writing any step that invokes it (Decision 6).
6. `check_spec.py` runs before every reviewer dispatch and its tests pass (Decisions 1, 8, 13, 14, 15, 16).

## Out of scope

- The script does not implement the guarantee scan (the 2d rule that withholds green while an in-scope P0 or P1 sits undischarged in the deferred-findings section); that scan stays prose (Q9 A).
- No ledger backfill for specs written before this ships. On a re-run, the ledger covers only the claims in sections that pass writes or edits (Q17 A).
- Attest mode is unchanged; the script does not run there (Q18 A).
- `/ship-spec`, `/spec-close` and `/spec-brief` are unchanged (Q19).
- The reviewer lenses' existing verification duties do not change. The two additions are the precedent rule in the conventions agent (Decision 5) and the ledger spot-check in the correctness agent (Decision 9); this rewords the ticket's non-goal.
- The GAV-9/GAV-10 rehearsal-mechanism discrepancy is a separate concern of that project, referenced here only as evidence.

## Tier

**Level:** big

## Scale

**Factor:** no

## Risks / decisions

1. Done-when wording — the ticket has no acceptance-criteria section, so `## Done when` lists its proposed changes as amended by the interview; the exact, testable form of each bullet is not established; spec author pins this.
2. Mode-table row references — if the divergence stop or the pre-dispatch check adds a row to the Phase 0 mode table, the prose references at `skills/spec-cycle/SKILL.md:378`, `:380` and `:458` must be renumbered; whether a row is added is not established; spec author pins this.
3. Overlap with the Phase 1 incomplete-spec halt — Phase 1 already halts on an existing spec that lacks any of seven required sections (`skills/spec-cycle/SKILL.md:388`); whether the script's required-sections check replaces that halt or runs after it is not established; spec author pins this.

## References

- Plane VHS-26 (18bfa979-46a8-4c0e-b998-a408fff0b4b2), read from the tracker 2026-10-13; shared memory returned HTTP 502.
- F1 — Phase 1 authoring lists required sections and carries no author read obligation and no ledger: `skills/spec-cycle/SKILL.md:384-405`.
- F2 — 2e routes every P0/P1 to fold/defer/reject and names propagation sites before editing; no fact re-verification, no composition check: `skills/spec-cycle/SKILL.md:706-722`.
- F3 — the loop halts only at the round cap or delta pass 2; no divergence stop: `skills/spec-cycle/SKILL.md:799`.
- F4 — the conventions agent has no precedent rule (grep, no hits); its `# Delta scope` block is at `agents/spec-reviewer-conventions.md:93` and the correctness agent's at `agents/spec-reviewer-correctness.md:90`; the four agents' blocks are byte-identical.
- F5 — `check_spec.py` comes from the sprint plan, not the ticket: wiki `overview/2026-10-11-skill-pack-distillation.md:47`, `:97`.
- F6 — the guarantee scan is prose in 2d: `skills/spec-cycle/SKILL.md:698`.
- F7 — no `scripts/` directory under `skills/spec-cycle/`; `skills/session-handoff/scripts/`, `skills/spec-close/scripts/` and `skills/hermes-kanban-awareness/scripts/` exist.
- F8 — Phase 1 halts on an existing spec lacking any of seven required sections: `skills/spec-cycle/SKILL.md:388`.
- F9 — the repo's tests are stdlib `unittest`, Python 3.8+ stdlib only: `AGENTS.md:7`.
- F10 — prose references to mode-table rows: `skills/spec-cycle/SKILL.md:378`, `:380`, `:458`.
- Grounded at `fc20f94` (local `main` in sync with `origin/main`).
- Tier basis: 2 files (skills/spec-cycle/SKILL.md, check_spec.py), lines: unknown, surfaces: auth — never tweak. The `auth` match is the word "session" in the ticket text.
- Interview: 3 rounds, exit empty-frontier
