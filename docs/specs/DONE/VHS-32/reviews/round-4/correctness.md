# Correctness Review — round 4

Grounding complete. Spec (562 lines) and brief re-read fresh from disk. Plane VHS-32 resolved from shared memory (namespace `skills`, `tag_exact`, confidence 1.00, record `723323e4-…`); its Scope, Decisions 1–10, Done-when and Out-of-scope chunks match the brief — no conflict, brief remains usable as the authority. `AGENTS.md` read (`CLAUDE.md` is the gitignored pointer). `git log` on all touched files: newest is `7db7289` (2026-08-25) — nothing in the last 7 days; `5e6d401` (2026-09-02) touches only `agents/*`, declared untouched. `scale_lens: off` and no `scalability.md` exists in `round-3/` — no stale-report guard needed.

Anchors re-verified this round against current files: `spec-cycle:43–48` (regex, prefix-anchored — the spec's "anchored at both ends since here it is the whole argument" is correct), `:60` (local-only path), `:61` (step 3 incl. username substitution), `:235` (step 7 states.json fallbacks), `:237` (step 8), `:404–409` (2c dispatch-failure stub — the new v4 exclusion), `:415/:422` (gate), `:426–465` (2e; round-4 rewrite precedes 2f, so "it already ran before the halt" is accurate), `:466–485` (2f — exactly three options today, three-lens hardcode confirmed at `:472–474`), `:487–518`, `:520`, `:559–563` (three-header parser), `:570`, `:578`, `:598–600`; `spec-close:31, :37–42, :339, :340`; `ship-spec:20, :197, :241`; `lint.py:24–33, :45–48, :57, :216–217` and the `?`-stripping services check at `:138–139`; `sync.py:96` (`copy2` in `cmd_install`, def `:62`) and `:146` (`cmd_push`, def `:110`); `prepend_log_entry.py:370–375`; `create_handoff.py:340–341`; `bloat-check:19`; `portability-contract:26–43, :34, :47–103, :65, :78, :107–119, :129`; `VHS-20/spec.md:153`; `AGENTS.md:23–29, :59–80, :95`; `README.md:3, :7–11, :30, :54–59`; `spec-workflow-reference.md:3, :7, :97, :162`; wiki `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md:91–92, :104`. Independently confirmed: `review-pr` and `ship-spec` are still the only skills without `requires:` (checklist-1 baseline of 2 is exact); no shipped skill uses `user_invocable: false`; `grep -c 'spec-close'` is 0 in both `README.md` and `docs/spec-workflow-reference.md`; `/spec-cycle`'s `requires:` block is byte-identical to the one the spec proposes for `/spec-brief`, so checklist 1 has an exact precedent.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | post-cap revision round promised, never granted; `revised-after-cap` unreachable | CLOSED | spec:157 (`prior_summary` bullet: "If `rounds_used ≥ round_cap`, this invocation runs exactly one additional round and exits `revised-after-cap (+1 round)`; a further `prior_summary` … exits `round-cap` at once"), :185 (1.6 lists the post-cap round among the bounds), :205 (`(round_cap + 1) × question_cap`), :117 / :313 ("the same `round_cap` / `question_cap` — the primitive itself grants"), :458 (checklist 4), :474 (Run D). Traced: cap-hit → resume → +1 round → `rounds_used > round_cap` → hard stop. Bound holds at `round_cap + 1`. |
| correctness | F-2 (P2) | 2c scalability stub missing from "not grillable" | CLOSED | spec:405 names "any 2c dispatch-failure stub … `skills/spec-cycle/SKILL.md:404–409`"; anchor verified — `:404–409` is exactly the stub rule |
| correctness | F-3 (P2) | no derivation rule for `## Out of scope` / transcribed sections | CLOSED | spec:338 (fence-shaped Settled → `## Out of scope`; Problem / Why it matters / Done when transcribed, never inferred) |
| correctness | F-4 (P2) | round-end line says "Answer by number" while forks use letters | CLOSED | spec:175 ("Answer by question number and branch letter (e.g. `Q3 B`)") — residual F-item gap filed below as F-3 |
| correctness | F-5 (P3) | Phase 1 cap refers to a flag declared ignored under `--no-grill` | CLOSED | spec:256 ("the default question cap (7) still bounds Phase 1's grounding batch"), :294 ("the default 7 under `--no-grill`") |
| correctness | F-6 (P3) | D8 seed statement predates the exclusions | CLOSED | spec:69 ("minus the not-grillable exclusions in Design 4 step 1") |
| correctness | F-7 (P3) | Runs A and B share `ZZZ-1` | CLOSED | spec:469 ("Run A uses `ZZZ-1` and Run B uses `ZZZ-2`") — a new variant survives on Runs C/D; filed as F-1 below |
| correctness | F-8 (P3) | local-only header fields unsourced | CLOSED | spec:338 ("`**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`") |
| correctness | F-9 (P3) | `sync.py:146` is in `cmd_push` | CLOSED | spec:447 and :545 both now read "`sync.py:96`, the install copy; `:146` is the symmetric push copy" — verified against `sync.py` |
| correctness | F-10 (P4) | checklist "three-state" label, 1.8 bound, `lint.py` range | CLOSED (a, b) / PARTIAL (c) | (a) spec:463 "four-case"; (b) spec:205 `(round_cap + 1) × question_cap`; (c) spec:539 now cites `lint.py:45–49`, but `SERVICES_VOCAB` is at `:48` and `:49` is blank — see F-4 below |
| edge-cases | F-1 (P2) | primitive would exit `round-cap` with zero questions on resume | CLOSED | same root as correctness F-1; spec:157 is the mechanism |
| edge-cases | F-2 (P2) | no disposition for a Settled decision not executable as a spec edit; brief not fenced | CLOSED | spec:408 ("`deferred to option 3: <finding id>` … Settled-but-unapplied … 2f-i never edits the brief"), :411 (invariant), :461 (checklist 7) |
| edge-cases | F-3 (P2) | stale `.tmp` cleanup never fires; dot prefix not uncommittable here | CLOSED | spec:262 (stale-only temp → remove and continue, no halt), :336 ("this repo's `.gitignore` does not ignore `.*.tmp`, so the no-commit rule below is prose, not mechanism"), :556 |
| edge-cases | F-4 (P2) | S8's "durable backstop" rests on a timestamp `/spec-cycle` never records | CLOSED | spec:123 ("held in context only … no on-disk signal distinguishes this invocation's grill from a prior one"), :529 (Risk 14), :555 |
| edge-cases | F-5 (P3) | concurrent `grill.md` appends; shared fixed temp name | CLOSED | spec:123 (lost update, accepted), :407 (`.grill.md.<random>.tmp`, with the reason it need not be fixed) |
| edge-cases | F-6 (P3) | `--no-grill` fan-out bounded by an ignored value | CLOSED | same as correctness F-5 |
| edge-cases | F-7 (P3) | new v3 paths unexercised by checklist/transcripts | CLOSED | spec:467 (checklist 13 covers the `--no-grill` Scale derivation, failed-dispatch→Risks, option-2 wording), :474 (Run D) |
| conventions | F-1 (P2) | name-collision inverts VHS-28 posture; revisit trigger unengaged | CLOSED | spec:447 (Design 6 dispositions the trigger, quoting the decision's own "installs and overwrites; it does not delete" — verified at wiki decision `:91–92`, trigger at `:104`), :77 (D10 narrowed to "the *supersession* mechanism differs"), :548 |
| conventions | F-2 (P2) | `AGENTS.md` § Superseded edit has no slot; "Two warnings:" scoping | CLOSED | spec:425 (paragraph, not bullet, appended after the "If AgentCraft reinstalls…" paragraph at `AGENTS.md:79–80`; list stays byte-identical), :466 (checklist 12 asserts exactly two bullets) |
| conventions | F-3 (P3) | README tagline / Requirements left at pre-VHS-32 shape | CLOSED | spec:23 (Scope row now names `README.md` tagline `:3`), :439 (new tagline + `/spec-close` Requirements line + `/spec-brief` line) |
| conventions | F-4 (P3) | two v3 additions absent from the `:31` ledger | CLOSED | spec:31 closes the class ("together with the Phase 4 emission rules these imply (the empty-Settled sentinel, the origin-annotated Scope heading, the Out-of-scope routing, the local-only header fields)") |
| conventions | F-5 (P4) | `grilling` has no `## Failure modes`; no heading-level assertion | CLOSED | spec:211 (§ 1.11, four lines), :458 (checklist 4: "`## Tool-use notes` and `## Failure modes` are real `##` headings") |

Both round-3 P1-class roots are closed with real mechanism, not wording. All 10 brief/ticket "Done when" criteria remain mapped 1:1 in spec § Done when (items 1–10), and each mapping target exists in the spec as cited.

## Findings

### F-1: Dry-run Run C asserts the absence of a file Run A writes, on the same ticket id — and Run D re-enters Run B's id with no ordering or cleanup rule
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:469 (Test plan procedure), :471 (Run A), :473 (Run C), :474 (Run D); Phase 0 step 2 at :262–277
**Claim:**
- :469 — "Run A uses `ZZZ-1` and Run B uses `ZZZ-2` (a shared id would trip Run B into the artifacts-exist halt and ground it on Run A's brief) … the emitted briefs are deleted **before commit**."
- :471 — Run A: "option 1 **writes a brief** whose `## Risks / decisions` carries no 'spec author pins this' items…"
- :473 — Run C: "local-only mode, operator answers `ok`; the skill re-prompts once, then halts with the S9 message; `docs/specs/TODO/ZZZ-1.brief.md` **does not exist afterward**."
- :474 — Run D: "**after Run B's `round-cap` exit**, choose option 2 on a settled Q…"

**Why this is wrong:** round 3 fixed the A↔B id collision by giving B its own id, but the same root survives in the two rows v4 added. Run A writes `docs/specs/TODO/ZZZ-1.brief.md` and the deletion is specified relative to *commit*, not between runs. In the listed order (A→B→C→D), Run C on `ZZZ-1` therefore (a) trips the Phase 0 step 2 artifacts-exist halt (spec:262 — the brief exists, tracked/untracked notwithstanding) before the S9 seed gate it exists to exercise is ever reached, and (b) its stated pass condition — "`ZZZ-1.brief.md` does not exist afterward" — is false on arrival, because Run A created it. A checklist row whose assertion is falsified by a sibling row is not a usable gate, and § Test plan is explicitly "the gate for `/ship-spec`" (:453). Run D is the same shape one step milder: it names no id, so an implementer reading it as a fresh `/spec-brief ZZZ-2` run hits the identical halt, while reading it as a continuation of Run B's confirm block contradicts Run B's own asserted outcome (:472 says Run B's brief *is* written, i.e. option 1 was taken).
**Suggested fix:** two clauses at :469. Give C and D their own ids — "Run A `ZZZ-1`, Run B `ZZZ-2`, Run C `ZZZ-3`, Run D `ZZZ-4`" (and change `ZZZ-1` → `ZZZ-3` at :473) — or state "each run uses a fresh id, and any emitted brief is deleted before the next run". For D, add whether it re-runs from scratch or is taken at Run B's confirm before option 1; if the latter, note that Run B's write assertion is checked after D returns.

### F-2: § 1.7's exit enumeration drops the `(+1 round)` suffix every other site treats as part of the token
**Severity:** P3
**Where:** spec.md:187 (§ 1.7) vs :157 (§ 1.1), :192 (§ 1.8 hand-off block), :117 (S7), :458 (checklist 4), :474 (Run D)
**Claim:** :187 — "Exits: `empty-frontier`, `round-cap`, `stop`, `revised-after-cap`, and `empty-seed`." Every other occurrence writes `revised-after-cap (+1 round)`, including the § 1.8 code block the implementer copies verbatim (`exit: empty-frontier | round-cap | stop | revised-after-cap (+1 round)`) and checklist 4's grep target.
**Why this is wrong:** the exit token is consumed downstream as a literal — Phase 4 emits `Interview: <n> rounds, exit <token>` into the brief's `## References` (:338) and the `=== BRIEF WRITTEN ===` block (:352), and checklist 4 asserts the body carries "the `revised-after-cap (+1 round)` exit". With two spellings in the same file, the emitted brief's audit line is not pinned. A careful reader unravels it (the suffix reads as an annotation), which is why this is not P2 — but the round-4 spec should not leave the implementer to choose.
**Suggested fix:** at :187 write "`revised-after-cap (+1 round)`" to match § 1.8, or add a half-sentence in § 1.7 saying the `(+1 round)` suffix is part of the rendered exit string.

### F-3: The verbatim round-end instruction covers Q-items only, while S5 requires the operator to answer F-items too
**Severity:** P3
**Where:** spec.md:175 (§ 1.3 literal round-end lines) vs :103 (S5), :183 (§ 1.5), :81 (S1, "Fact requests use the parallel `F1…Fn` series")
**Claim:** :175 — "Answer by question number and branch letter (e.g. `Q3 B`); a plain answer is recorded as given. 'defer' moves a question to the open frontier." But S5 (:103) renders fact requests as `ℹ️ **F1 — <fact needed>**` in the same round, counts them against the same cap, and requires an operator answer: "A fact request the operator leaves unanswered **twice** becomes an Open item ('fact not established')."
**Why this is wrong:** this is the interview's single most-repeated operator-facing line and it is specified verbatim, so whatever it says is what ships. Round 3 narrowed it from the generic "Answer by number" to "question number and branch letter" — which is right for forks but now excludes the F-series by construction. On the degraded path (no read-restricted agent class in the host — S5's whole reason to exist) *every* rendered item can be an `ℹ️ F` item, and the only instruction the operator gets tells them to answer with a Q number and a branch letter. That is the same fatigue surface D6 and S1 exist to protect.
**Suggested fix:** extend :175 — "Answer by item number: a question by number and branch letter (e.g. `Q3 B`), a fact request by number and the fact (e.g. `F1 <answer>`); a plain answer is recorded as given."

### F-4: `lint.py:45–49` overshoots the controlled-vocabulary block by one blank line
**Severity:** P4
**Where:** spec.md:539 (§ References)
**Claim:** "`lint.py:24–33` — documented v1 limitations; `:45–49` controlled vocabulary".
**Why this is wrong:** the vocabulary constants are `lint.py:45` (`REQUIRES_KEYS`), `:46` (`BOOL_KEYS`), `:47` (`FILESYSTEM_VOCAB`), `:48` (`SERVICES_VOCAB`); `:49` is blank and `:50` is `ERROR = "ERROR"`. Round-3 F-10(c) asked for `:45–49` on the belief that `SERVICES_VOCAB` sat at `:49`; the underlying concern (the `services:` vocabulary must be inside the cited range) is now satisfied either way, so nothing load-bearing turns on this.
**Suggested fix:** cite `lint.py:45–48`.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 1

STATUS: GREEN
