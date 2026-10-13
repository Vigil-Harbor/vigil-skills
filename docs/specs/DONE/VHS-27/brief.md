# VHS-27 — spec-cycle: switch to delta-scoped review passes after round 4 or after first GREEN
**Status:** Backlog · **Priority:** high · **Assignee:** unassigned
**Created:** 2026-10-12 · **Plane:** VHS-27 (d5a07af6-e1c8-4893-ba3d-716ed90a7063, Backlog)
**Origin:** Filed 2026-08-01 from the PET-166 case study (ten review rounds, 2026-07-28 to 2026-07-31, plus a round-11 delta close-out used as a control). Second item in the Wave 2 spec-cycle lane of the 2026-10-11 sprint plan, after VHS-43 (shipped as `d3730b1`) and before VHS-26. The ticket text predates VHS-43, VHS-47 and VHS-55; the interview on 2026-10-12 re-grounded its five proposals against the skill as it stands at `c01286d`, and a Codex review of the first draft the same day revised four decisions and added three (see References).

## Problem

spec-cycle's review loop re-runs all three full lenses every pass. Past convergence this is actively harmful: each full pass reviews the previous pass's remediation prose instead of the design, and the fixes themselves become the dominant source of new findings. The skill's 4-pass budget exists, but nothing changes the review **shape** when the loop runs long; it just re-fires the same full-lens prompts.

## Why it matters

Evidence from PET-166 (10 rounds, 2026-07-28 to 2026-07-31), as the ticket states it:

- Fix-induced churn was the dominant finding class in both cycles: 58% of post-round-1 findings (rounds 2-5) and 54% (rounds 6-10) targeted text added to satisfy earlier findings. Genuine misses dried up after round 2 (~12%).
- 3 of the 5 P0-class defects were manufactured by earlier rounds' remediations, not present in the original design.
- Author-side fatigue outpaced the finding stream: round-3 reports were written retroactively; by round 10 the closure manifest silently dropped a P1 twice and reported anchor fixes that were never applied.
- Line-number anchors alone were roughly a quarter of raw findings in rounds 6-10.
- The rounds 6-10 tail had a single root cause: a feature (PET-165) merged to master after the round-5 all-GREEN, and the full-lens response to that drift restarted the churn loop.
- Control group: the round-11 close-out ran as a delta review (three lenses, manifest-scoped to changed regions plus open findings, closure-table verification mandatory). It verified 26 closures and surfaced exactly 2 findings, both real P2s in the new text, both fixed same-session. Compare ~30 findings per full-lens round in 7-10.

## Scope (verified against current files, 2026-10-12)

| Path | Current | Change |
|---|---|---|
| `skills/spec-cycle/SKILL.md` invocation and Phase 0 | Invoked as `<brief-path> [--attest "<reason>"]` (`:15`); `--attest` with any other flag halts (`:904`). Step 9 resolves `tier` and `round_cap` once (`:343`). A re-run pins scale and tier from the existing spec (`:331`, `:345`) but has no notion of review mode. | Add `--full`, exclusive with `--attest`. Resolve a review mode (full or delta) at preflight by the mode table and print it with its reason in the preflight summary (Decisions 1, 6, 7, 12, 13, 14). The tier and scale pins are unchanged. |
| `skills/spec-cycle/SKILL.md` § The verdict marker | `round: <1..round_cap> \| not reviewed \| in progress` (`:36`). | The `round` value accepts any positive completed review round. No field is added (Decision 8). |
| `skills/spec-cycle/SKILL.md` Phase 2 loop | The pending marker is written before round 1's dispatch, replacing any marker (`:386`). `For each round 1..round_cap` (`:388`), breaking at first green (`:567`). A re-run restarts at round 1 with full lenses (`:361`). Reports land in `round-<N>/` (`:479-482`). | Classify the clean no-op before the pending write (Decision 11). On a continuing re-run, run delta passes under two counters (Decision 8). Save the per-round copies and the commit before dispatch (Decisions 2, 5). |
| `skills/spec-cycle/SKILL.md` § 2b dispatch | Rounds N > 1 pass a `closure_manifest` built in-context from the revision just done (`:430-456`, `:449`), plus `guarantee/D-<n>` lines (`:458`). It is not saved. | A delta pass also passes the changed regions and the open findings (Decisions 9, 15). The manifest comes from the saved ledger (Decision 3) and stays P0/P1 only. |
| `skills/spec-cycle/SKILL.md` § 2d gate | `total_p0p1` summed over dispatched reviewers; the guarantee scan runs before the green break (`:552-569`). | Formula unchanged. |
| `skills/spec-cycle/SKILL.md` § 2e revise, § 2f halt, § 2f-i grill | The branches test `round < round_cap` (`:575`) and `round == round_cap` (`:630`); the halt follows round `round_cap` (`:666`); the grill reads and writes `round-<round_cap>/` (`:701-705`, `:737`). | Save the disposition ledger after every red round's revision (Decision 3). Delta pass 1 revises; delta pass 2 folds without FROZEN/REWRITE and, if still loop-red, halts with the existing halt menu; the grill uses the final cumulative round (Decision 8). The halt block gains the drift warning (Decision 5). |
| `skills/spec-cycle/SKILL.md` Phase 3 | The SPEC READY block carries no tree-freeze warning (`:835-888`). | Add the drift warning (Decision 5). |
| `agents/spec-reviewer-correctness.md` | Inputs include `round_number` (1-4) and `closure_manifest` (`:17-18`). Step 7 builds a closure table from the prior round's reports on disk (`:44-70`) and does not compare it with the author's manifest. Each stale file:line anchor is a P1 (`:107-109`). | Accept the delta inputs (Decision 15); apply the delta contract (Decision 10); compare the manifest with the disk reports and file a missing line (Decision 3); split anchor drift by cause (Decision 4). |
| `agents/spec-reviewer-edge-cases.md`, `agents/spec-reviewer-conventions.md`, `agents/spec-reviewer-scalability.md` | Each carries the `closure_manifest` input and the shared Deferred-findings block (edge-cases and scalability `:31-42`, conventions `:36-47`). | Accept the delta inputs and apply the delta contract (Decisions 10, 15). The Deferred-findings block stays byte-identical across all four agents. |
| `docs/spec-workflow-reference.md` | Phase 2 describes the capped loop, the rewrite and the halt (`:70-94`); the verdict marker paragraph describes the round and gate count (`:106-108`). | Describe the delta mode, and state the rationale with the PET-166 numbers (Decision 16). |
| `AGENTS.md` | The `/spec-cycle` lifecycle item describes the loop and its `round_cap` halt (`:25-27`). | State the delta mode and `--full` (Decision 16). |

## Decisions carried forward

1. **Delta passes run on re-runs only.** A re-run of `/spec-cycle` over a spec whose verdict marker is green, or red at a halt, runs delta passes when Decision 14's table allows it. The first invocation's loop is unchanged. Why: the loop has no pass after `round_cap` or after green, so a re-run is the only place the ticket's two triggers can attach.
2. **The skill saves a copy of the spec and of the brief each round.** The copies are named files in that round's directory, written immediately before reviewers are dispatched. The changed regions are a diff of the spec against a baseline copy. Preflight reads the last completed round from the marker and selects that round's copy before the pending write replaces the marker; the selection is held for the invocation. Delta pass 2's baseline is the copy delta pass 1 saved before its dispatch. Why: an author-stated list cannot see manual patches between runs, and author fatigue is the failure PET-166 recorded.
3. **The ledger rule is a comparison against a saved ledger, P0 and P1 only.** After every red round's revision, the final round included, the skill saves the author's dispositions to a named file; the next round, in this invocation or a later one, uses it as the `closure_manifest`. A green round saves an explicit empty ledger before the green marker is written. A required ledger that is missing or unreadable selects full mode; an earlier round's ledger is never used in its place. The correctness lens alone compares it with the prior round's reports on disk and files one blocking P0 when a P0 or P1 line is missing. Why: the recorded defect was a dropped P1; today the manifest lives only in context, so a new invocation has nothing to compare.
4. **Anchor drift splits by cause.** A citation whose symbol still resolves and whose line number moved is reported once per reviewer report, as one combined P4. A citation whose symbol is gone stays a P1. Why: this removes the noise without hiding a dead reference.
5. **Code drift is detected from a commit saved beside each round's copies.** On a re-run, a spec section that cites a file changed since that commit counts as a changed region. Both stop screens also warn that a merge into reviewed surfaces while the loop is open restarts churn. The commit is not a verdict-marker field. Why: the PET-166 tail was code merging after green with the spec unchanged; text alone would leave that case to a full pass, which is what restarted the churn.
6. **A full pass is requested by `--full`.** It is exclusive with `--attest`. It does not override the tier or scale pins recorded in the spec. Why: explicit, and it adds no prompt to every re-run.
7. **A changed brief forces a full pass.** The skill compares the brief with the saved copy. Why: a delta pass against a changed brief verifies closures against the wrong axiom.
8. **Two counters, and at most 2 delta passes per re-run on every tier.** A cumulative review round names the directories and the marker's `round`, so earlier reports are never overwritten. A per-invocation pass index drives the loop logic. Delta pass 1 revises under the ordinary revision rules. Delta pass 2 routes and folds without FROZEN/REWRITE. If it is still loop-red it halts with the existing halt menu, including that menu's three-option case when only the guarantee scan withheld green; the grill option uses the final cumulative round. A green delta pass goes on to post-green polish and Phase 3 as any green round does. Why: every revise, rewrite, halt and grill step tests against `round_cap`, so one continuing number matches no branch; and the control pass converged in one round, so a spec that does not converge in two is a signal for the halt.
9. **A non-empty delta pass dispatches every lens the run would normally dispatch.** Three, or four with the scalability lens. Why: each lens verifies its own closures; the saving comes from the narrower scope.
10. **The delta restriction covers new lens exploration only.** Reviewers do not explore unchanged regions and do not re-litigate settled decisions. Closure verification, the Deferred-findings block, grounding and process failures, and vanished-reference checks run as today at their existing severities. A P0 met incidentally outside the changed regions may be reported with evidence and counts in the gate; reviewers do not read unchanged regions to look for one. Why: a blanket P0-only rule would forbid the dead-citation P1 of Decision 4 and the corrections the Deferred-findings block requires every round.
11. **Nothing changed and nothing open is a no-op that reports green.** It needs no changed region (Decision 5's included) and no open P0 or P1. The skill classifies it before the pending write. It is not a review round: no round number is taken, no copy is saved, no reviewer is dispatched, no polish or synthesis runs, and the marker is not rewritten. The guarantee scan runs first; if it withholds, the run is not a no-op and goes on to dispatch. Why: the pending write replaces the marker, so a no-op decided after it would leave a green spec pending.
12. **No saved copy means a full pass.** That run saves the first copy and prints `mode: full (no baseline)`. A delta pass never runs without a baseline, and a closed spec's archive under `DONE/` is never one.
13. **A `pending` marker means a full pass.** It takes the next unused round number, so an interrupted run's reports are not overwritten; they stay as audit evidence. Round numbers are storage, not closure ancestry: the first pass of any full invocation is a fresh full review with no closure predecessor and needs no ledger. Later passes close the completed pass before them.
14. **Mode table.** The mode is full, with its reason printed, when any of these holds: `--full` was given; the marker is missing, unreadable or `pending`; the marker is green by attestation; the brief changed; no baseline matches the round the marker names; that round's ledger is missing or unreadable. Otherwise the mode is delta. Why: an attested green has no reviewed round to continue from.
15. **Delta inputs.** Changed regions are Markdown sections together with their diff hunks, deleted and renamed headings included. Open findings are the prior round's unresolved P0 and P1 only.
16. **The rationale lives in `docs/spec-workflow-reference.md`.** That file states the delta mode with the PET-166 numbers; `AGENTS.md` states the mode and the flag in its lifecycle item.

## Done when

From the ticket, with the second criterion reworded to match Decision 11 and the third to match Decision 3:

- SKILL.md for spec-cycle encodes the delta trigger, the delta pass contract, and the ledger rule; the reviewer agent prompts (spec-reviewer-correctness / edge-cases / conventions / scalability) accept a delta manifest and closure table.
- A delta pass on a spec with zero changed regions and zero open P0/P1 findings is a no-op that reports GREEN, not a full pass.
- Ledger check: a synthetic prior-round finding omitted from the saved ledger is flagged by the correctness reviewer.
- Docs state the rationale with the PET-166 numbers so the guardrail survives future skill edits.

Added after the Codex review, 2026-10-12, on the operator's word. The spec walks each scenario and states the mode, the round number, the marker and the halt it produces:

- First delta pass after a red halt, and after a green.
- A `small`-tier continuation (the round limit is 2).
- Delta pass 2 still red, then the grill option.
- An attested green; a changed brief; an absent baseline; a `pending` marker; a run after `/spec-close` archived the spec.
- Code changed since the saved commit, with the spec and brief unchanged.

## Out of scope

- FROZEN/REWRITE is unchanged in the first invocation and does not run in a delta pass.
- VHS-43's routing rules and the gate formula are unchanged; a delta pass uses them as they are.
- No author-side check script. That is VHS-26.
- No new verdict-marker field. The `round` value's range widens; nothing is added.
- P2 and lower findings are not added to the closure manifest or the saved ledger.
- The tier and scale re-run pins are unchanged; changing either still means editing the spec.

## Tier

**Level:** big

## Risks / decisions

1. The file names and line shapes of the saved copies, the saved commit and the disposition ledger, and when each is written atomically; spec author pins this.
2. How a spec section is matched to the files it cites for Decision 5 (path citations, the Scope table, or both); spec author pins this.
3. The four reviewer agents run installed in other repos and must not cite skill line numbers or repo paths; the delta contract text has to stand without them. Spec author pins this.
4. VHS-26 edits the same sections of `skills/spec-cycle/SKILL.md` next; line anchors in this brief hold at `c01286d` only. Spec author pins this.

## References

- Plane VHS-27, ticket text of 2026-08-01 (resolved from the tracker; the shared-memory lookup was denied).
- `skills/spec-cycle/SKILL.md:36`, `:51`, `:55` — the marker's `round` grammar, the attested marker, the write points.
- `skills/spec-cycle/SKILL.md:343`, `:388`, `:567` — the loop, its cap and the green break.
- `skills/spec-cycle/SKILL.md:361`, `:386`, `:664-684` — re-run behaviour, the pending write and the round-cap halt.
- `skills/spec-cycle/SKILL.md:430-458` — the closure manifest (built in context, `:449`) and `guarantee/D-<n>` lines.
- `skills/spec-cycle/SKILL.md:498-550`, `:565-569` — the round synthesis and the guarantee scan (VHS-43).
- `skills/spec-cycle/SKILL.md:575`, `:630-660`, `:701-705`, `:737` — the revise and rewrite branches, FROZEN/REWRITE, the grill's round directory. `:802-834` — post-green polish. `:835-888` — Phase 3. `:904` — attest mode's flag rule.
- `agents/spec-reviewer-correctness.md:17-18`, `:31-42`, `:44-70`, `:107-109` — inputs, the Deferred-findings block, closure step 7, stale anchors. `:29` — the recent-history grounding check.
- `skills/spec-close/SKILL.md:329-360` — the close moves the whole reviews tree to `DONE/<TICKET-ID>/reviews/`.
- `docs/spec-workflow-reference.md:70-94`, `:106-108` — the documented loop and verdict marker.
- Wiki `overview/2026-10-11-skill-pack-distillation.md` §6 — Wave 2 order: VHS-43, VHS-27, VHS-26.
- The PET-166 review artifacts (`docs/specs/TODO/PET-166.reviews/` in the Petasos repo, gitignored and local) were not read; the numbers above are transcribed from the ticket.
- Brief review: Codex (`gpt-5.6-sol`, read-only), 2026-10-12, verdict RED on the first draft — 3 P0, 7 P1, 1 P3. All eleven were folded on the operator's word: Decisions 5, 8, 10 and 11 revised (5 reverses interview answer Q5 A), Decisions 2, 3, 6, 9, 12 and 13 tightened, Decisions 14 to 16 added, Done-when extended. A delta pass on the revision returned RED again with nine of eleven closed, two partial, and four new findings (3 P1, 1 P2), all tightening Decisions 2, 3, 8, 13 and 14 without reversing one; those were folded too. No third pass was run.
- Interview: 3 rounds, exit empty-frontier
