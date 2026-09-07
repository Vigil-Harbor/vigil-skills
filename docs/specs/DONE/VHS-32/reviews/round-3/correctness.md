# Correctness Review — round 3

Grounding complete. Spec (556 lines) and brief re-read from disk. Plane VHS-32 resolved from shared memory (namespace `skills`, tag-exact, confidence 1.00) — description and Done-when match the brief; no conflict. `AGENTS.md` read (project instructions; `CLAUDE.md` is the machine-local pointer). Every `file:line` anchor in § References and § Scope re-verified against the current tree. `git log` on the touched files: newest is `a9e7581` (2026-06-16); nothing in the last 7 days (`5e6d401`, 2026-09-02, touches only `agents/*`, declared untouched). `scale_lens: off` and no `scalability.md` exists in `round-2/` — no stale-report guard needed.

Anchor spot-checks that passed this round: `spec-cycle:43–48` (regex), `:61` (step 3, incl. username substitution), `:133–233` (step 5), `:235`, `:237`, `:268–272` (`**Dimensions:**`), `:371–375`, `:404–410`, `:415`, `:426–465`, `:466–485` (halt block is exactly 3 options today), `:487–518`, `:520`, `:570`, `:578`, `:598–600`; `spec-close:31, :37–42, :312, :339, :340`; `ship-spec:20, :197, :241`; `portability-contract:26–43, :34, :47–103, :65, :78, :107–119, :129`; `lint.py:24–33, :57, :216–217`; `sync.py:96`; `prepend_log_entry.py:370–375`; `create_handoff.py:340–341`; `bloat-check:19`; `VHS-20/spec.md:153`; `AGENTS.md:23–29, :88–96, :95`; `README.md:7–11, :30, :54–59`; `docs/spec-workflow-reference.md:3, :7, :162`; `customizing.md:3`; `spec-reviewer-conventions.md:3, :17–31`. Independently confirmed: `review-pr` and `ship-spec` are the only skills without `requires:` (checklist-1 baseline of 2 WARNs is exact); no shipped skill uses `user_invocable: false`; `grep -c 'spec-close'` is 0 in both `README.md` and `docs/spec-workflow-reference.md`; `spec-cycle` and `spec-close` both declare `network: true`; `spec-cycle` Phase 3 parses exactly three brief headers.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P1) | `empty-seed` unhandled at 2 of 3 call sites; 2f-i contradicts S9 | CLOSED | spec:403 (step 1 guard: "do not invoke `grilling`… write nothing to `grill.md`… re-render 1–3"), :226 (grill-me `empty-seed` line), :127 (S9 names all three callers), :298, :459 (checklist greps "nothing grillable") |
| edge-cases | F-2 (P1) | hung exploration blocks the round while § 1.5 asserts it cannot | CLOSED | spec:183 ("a dispatch that never returns blocks the round it belongs to"), :43 (D2 sentence gains "answer from the paths named… return `not found`"), :523 (Risk 12), :373 (Failure-modes bullet) |
| correctness | F-1 (P2) | three wrong `spec-cycle` anchors in § References | CLOSED | spec:529 — `:133–233` / `:237` / `:371–375` all verified correct against the file |
| correctness | F-2 (P2) | `## Tool-use notes` / `## Failure modes` emitted at `##` inside Design 3 | CLOSED | spec:359, :363 are `####`, each with a parenthetical saying it is `##` in the shipped file |
| correctness | F-3 (P2) | round-budget cost not stated where the operator sees it | CLOSED | spec:176 ("a partly answered round still uses one of your `<round_cap>` rounds") |
| correctness | F-4 (P2) | Phase 3 option 2 has no re-entry into the primitive | PARTIAL | spec:157 adds `prior_summary`, :311 re-invokes with it — but the promised post-cap extra round has no mechanism; see F-1 below |
| correctness | F-5 (P2) | all-not-grillable 2f-i seed collides with S9 | CLOSED | spec:403 (same guard as edge F-1) |
| correctness | F-6 (P2) | brief Scope table has no derivation rule | CLOSED | spec:336 ("one row per path the settled decisions and grounding facts name… a path with no read file or fact behind it gets no row") |
| correctness | F-7 (P3) | Scale rule inverts factor/target dependency | CLOSED | spec:339 ("The factor and its target are one question, not two") |
| correctness | F-8 (P4) | "three states" labels a four-bullet rule | CLOSED | spec:338 ("four input cases, three emitted shapes"); residual echo in checklist 9 noted as F-10 below |
| edge-cases | F-3 (P2) | `--no-grill` can never emit `## Scale` | CLOSED | spec:343 (same four cases applied to explicit ticket text) |
| edge-cases | F-4 (P2) | failed grounding dispatch under `--no-grill` has nowhere to land | CLOSED | spec:292 (`<fact needed> — not established (exploration failed); spec author pins this`) |
| edge-cases | F-5 (P2) | fact-dispatch cap has no overflow rule | CLOSED | spec:183 ("Fact needs beyond the dispatch cap carry to the next round's batch by the S1 ordering") |
| edge-cases | F-6 (P2) | option 2 re-selectable without limit after `revised-after-cap` | PARTIAL | spec:117, :311 bound the *offer* to once — but the granted round itself is unmechanized; see F-1 |
| edge-cases | F-7 (P2) | origin-behind warning transient vs durable Scope claim | CLOSED | spec:336 (Scope heading gains "local tree `<N>` commits behind origin/`<cmp>`" + References bullet) |
| edge-cases | F-8 (P2) | `grill.md` append has no atomicity/dedup/durable once-signal | CLOSED | spec:123 (tmp-rename, `# Grill <k>` counter, last-writer-wins, datetime backstop), :405 |
| edge-cases | F-9 (P3) | `## Scale` has no position in the section order | CLOSED | spec:329 (slot between Out of scope and Risks, marked conditional) |
| edge-cases | F-10 (P3) | S9 re-prompt unmechanized in ticket mode | CLOSED | spec:127 (`Ticket <ID> states no problem — describe it in a paragraph…`) |
| edge-cases | F-11 (P3) | leaked `.tmp` invisible to the artifacts check / archived by spec-close | CLOSED | spec:334 (dot-prefixed temp, outside the `<TICKET-ID>.<rest>` glob — verified at `spec-close:340`), :267 (stale row in the halt) |
| edge-cases | F-12 (P3) | artifacts-halt option 1 worded for a branch that may not hold | CLOSED | spec:271 (conditional wording: "if only a spec and reviews exist, the brief is written fresh") |
| edge-cases | F-13 (P3) | interview that settles nothing writes an empty Decisions section | CLOSED | spec:336 (`_(none settled — see Risks / decisions)_` + warning) |
| conventions | F-1 (P2) | spec-additions ledger incomplete | CLOSED | spec:31 lists the five point-of-use additions |
| conventions | F-2 (P2) | undotted `.tmp` name | CLOSED | spec:334 (dot-prefixed, precedent `prepend_log_entry.py:370–375` verified), :361 (lone mutation named in Tool-use notes) |
| conventions | F-3 (P2) | upstream directory-name collision | CLOSED | spec:445 (Design 6), :423 (`AGENTS.md` § Superseded bullet — section exists at `AGENTS.md:59`), :464 (checklist 12), :524 (Risk 13) |
| conventions | F-4 (P4) | "Deferred" header said "not folded into v2" while entries said folded | CLOSED | spec:548 ("folded in a different shape than proposed, or deliberately not folded") |

Both round-2 P1s are CLOSED. The two PARTIALs (correctness F-4, edge-cases F-6) share one root — the revise path's missing budget mechanism — carried below as F-1 at P1 (their original severity was P2, but the residue is now a functional gap, not a documentation gap).

## Findings

### F-1: The post-cap revision round is promised in three places and granted by none — `revised-after-cap` is an unreachable exit, and option 2 after a cap hit silently drops the operator's revision
**Severity:** P1
**Where:** spec.md:117 (S7), :157 (§ 1.1), :185 (§ 1.6), :187 (§ 1.7), :192 (§ 1.8), :307/:311 (Design 3 Phase 3), :456 (checklist 4)
**Claim:**
- S7 (:117): "`/spec-brief` re-invokes `grilling` … and **the same bounds**; … `rounds_used` carries over. If the round budget is already exhausted, **one** post-cap revision round is granted per invocation and the exit token becomes `revised-after-cap (+1 round)`".
- Phase 3 (:311): "Option 2 re-invokes `grilling` with the Grill summary as `prior_summary` and **the same bounds** (S7)".
- § 1.1 (:157): "`rounds_used` carries over from the summary's `rounds:` field."
- § 1.7 (:187): "Exits: `empty-frontier`, `round-cap`, `stop`, `revised-after-cap`, and `empty-seed`."

**Why this is wrong:** the two skills are separate files, and the round cap is enforced by the primitive (§ 1.6, :185 — "The three bounds with defaults (D6)", no post-cap exception). Trace the designed path: the interview exits `round-cap` (rounds_used = round_cap = 3) → the operator picks option 2 → `/spec-brief` re-invokes with `prior_summary` and *the same bounds* → the primitive rebuilds the tree, computes `rounds_used (3) ≥ round_cap (3)`, and terminates immediately at `round-cap`. The revised decision and its downstream items were returned to the frontier (:157) but are never re-asked; they land in § Open frontier and, via the Phase 4 mapping (:336), in `## Risks / decisions`. `/spec-brief` then re-renders the confirm with options 1 and 3 only (:311), so the operator loses the revision entirely on the exact case S7 exists to serve. Nothing in the spec raises the budget: the caller is explicitly told to pass "the same bounds", § 1.1's input list has no `grant_extra_round` / adjusted `round_cap`, and checklist 4 (:456) — which enumerates what `grilling`'s body must carry verbatim — does not list a post-cap-grant rule, so the shipped primitive will not have one. Consequently `revised-after-cap` (:187) and the `(+1 round)` form in the hand-off header (:192) are tokens no rule in the spec can emit — an internal inconsistency, not just a gap.

**Suggested fix:** pin the mechanism in the primitive and make the caller's wording match. In § 1.1, add to the `prior_summary` bullet: "When `rounds_used ≥ round_cap`, this invocation runs **one** additional round (once per `prior_summary` chain) and exits `revised-after-cap`; a second `prior_summary` arriving with `rounds_used > round_cap` exits `round-cap` at once." Add the same sentence to § 1.6's bounds list and to checklist 4's verbatim list. Then change "the same bounds" at :117 and :311 to "the same `round_cap` / `question_cap` (the primitive itself grants the single post-cap round — § 1.1)". Also update § 1.8's "bounded by construction at `round_cap × question_cap`" to `(round_cap + 1) × question_cap`.

### F-2: 2f-i's "not grillable" list misses the other dispatch-failure form the spec's own References cite — the 2c scalability stub
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:403 (Design 4 Edit 2 step 1); References :529 cites "2c scalability stub `:404–410`"
**Claim:** "**Not grillable:** a report that is missing or unparseable, and any synthetic `missing STATUS line` P0 (2b's closure-manifest form) — these are dispatch failures, not design questions."
**Why this is wrong:** `skills/spec-cycle/SKILL.md:404–409` defines a *second* dispatch-failure artifact: when the scalability reviewer returns nothing parseable, 2c writes a **stub** `scalability.md` — "a one-line body plus `STATUS: RED P0=1 P1=0` — so the gate has a summand". That file is present on disk and its STATUS line parses cleanly, so it is neither "missing" nor (by the STATUS test) "unparseable"; and its P0 is not the 2b `missing STATUS line` synthetic. Its P0 contributes to `total_p0p1` and therefore can be one of the findings still red at the round-4 halt. Under step 1 as written, that P0 enters the grill seed with no id/title/body to interview on, and the operator is asked to disposition "the scalability subagent crashed" as a design question — precisely the category step 1 exists to exclude.
**Suggested fix:** extend the exclusion at :403 to name it: "…and any 2c dispatch-failure stub report (a lens report whose body records a dispatch failure rather than findings — `spec-cycle:404–409`)". No other text changes; the existing "not grillable" print line and the empty-seed guard already cover the consequences.

### F-3: Phase 4 gives derivation rules for five sections and none for `## Out of scope` — the one artifact section the altitude fence names but the Settled mapping cannot reach
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:315–332 (Phase 4 section order), :336 (Mapping rules); fence at :61 (D6), :89 (S3), :155 (§ 1.1)
**Claim:** the fence is stated three times as "only decisions that change the brief's **Scope, Decisions carried forward, or Out of scope**", and S4's third worked example (:99) explicitly classifies "Does `/spec-brief` write Plane state, or only read the ticket?" as changing the "**Out-of-scope fence**". But the Phase 4 mapping (:336) routes *all* Settled items to `## Decisions carried forward`, and `## Out of scope` (and `## Done when`) appear only in the section-order block at :327–328 with no derivation rule anywhere in the spec (`grep` confirms: the only other occurrences are the fence statements and the spec's own headings).
**Why this is wrong:** a settled decision whose whole purpose is to draw a fence is filed as a carried-forward decision, and the emitted brief's `## Out of scope` is left to improvisation or empty. That is visible downstream: `skills/spec-cycle/SKILL.md:559–562` parses exactly `Decisions carried forward` / `Done when` / `Out of scope`, and Phase 3 renders an "Out-of-scope fences" checklist from it — an empty section degrades the drift check to its fallback bullet (`:563`). The gap also means the fence's third clause is unenforceable by construction: no rendered artifact ever receives those decisions.
**Suggested fix:** one clause in the :336 mapping rules — "a Settled decision the operator framed as a fence (an answer of the form 'X is not in scope') is written to `## Out of scope` instead of `## Decisions carried forward`; `## Done when` and `## Problem` / `## Why it matters` are transcribed from the ticket text (or, in local-only mode, from the operator's paragraph), never inferred." That also closes the header question in F-8.

### F-4: § 1.3's verbatim round-end block tells the operator to "Answer by number" while the fork form's selectors are letters
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:163–177 (§ 1.3 fork block and the literal round-end lines), :116 (S7)
**Claim:** the fork block renders branches as `**A.**` / `**B.**` under `❓ **Q1 — <title>**`, and S7 defines a valid answer as "a rendered branch letter, `defer`, or `stop`" (anything else is free-form). The literal, operator-facing line at :175 says: "Answer by number."
**Why this is wrong:** this is a verbatim contract line — the implementer copies it into `grilling/SKILL.md` and the operator reads it every round. "By number" names the Q index, not the branch selector, so the one instruction the operator gets omits the letter that actually settles a fork. An operator answering "1" on a two-branch Q1 produces an answer S7 must then classify as free-form and re-ask with a `(clarify)` tag — friction on the interview's single most-repeated line, and squarely against the fatigue mitigation the ticket is built around.
**Suggested fix:** change :175 to "Answer by question number and branch letter (e.g. `Q3 B`); a plain answer is recorded as given." Keep the rest of the block unchanged.

### F-5: Phase 1's grounding-dispatch cap is `question_cap`, which the Invocation section declares "ignored" under `--no-grill`
**Severity:** P3
**Where:** spec.md:254 (Invocation), :292 (Phase 1 step 4)
**Claim:** :254 — "`--no-grill` wins over any cap flag; if both are given, warn `--rounds/--questions ignored under --no-grill` and continue." :292 — grounding dispatches run "in one parallel batch of at most `question_cap` dispatches".
**Why this is wrong:** Phase 1 runs on both paths, and under `--no-grill` `question_cap` has been declared ignored, leaving the dispatch batch's only bound referring to a value the spec just discarded. The intended reading is surely "the flag is ignored; the default 7 still bounds Phase 1", but as written an implementer can equally read it as unbounded.
**Suggested fix:** at :254 add "— the defaults (3 / 7) still stand; `question_cap` continues to bound Phase 1's grounding batch", or at :292 write "at most 7 dispatches (the `question_cap` default; the flag is ignored under `--no-grill`)".

### F-6: D8's description of the 2f-i seed no longer matches Design 4 step 1 after the not-grillable exclusions landed
**Severity:** P3
**Where:** spec.md:69 (D8), :403 (Design 4 step 1)
**Claim:** D8 — "the grill's seed is **every remaining P0/P1 finding in the round-4 reports on disk** … which is the same set the (corrected) halt block prints."
**Why this is wrong:** step 1 removes missing/unparseable reports and 2b synthetics from the seed (and F-2 above would remove 2c stubs too), so the seed is a strict subset of what the halt block prints whenever any dispatch failure is outstanding. D8 is the Decisions-section statement an implementer treats as the rule; the drift between the two invites building the seed without the exclusions.
**Suggested fix:** append to :69 — "…minus the not-grillable exclusions in Design 4 step 1 (dispatch failures, which stay P0/P1 and are reported, not interviewed)."

### F-7: Dry-run Runs A and B share the ticket id `ZZZ-1`, so Run B exercises the artifacts-exist halt instead of the round-cap path
**Severity:** P3
**Where:** spec.md:457 (Test plan procedure), :460–461 (Runs A/B), :260–273 (Phase 0 step 2)
**Claim:** "Both runs use a throwaway local-only id (`ZZZ-1`) … the emitted `docs/specs/TODO/ZZZ-1.brief.md` is deleted before commit."
**Why this is wrong:** the deletion is specified relative to *commit*, not relative to Run B. Run A writes `ZZZ-1.brief.md`; Run B then trips Phase 0 step 2's artifacts-exist halt (:260), and its option 1 says "an existing brief is read as grounding first" — so Run B's seed would be contaminated by Run A's shallow-tree brief, and the transcript would document the halt path rather than the round-cap path the run exists to demonstrate.
**Suggested fix:** in the procedure at :457, add "delete `docs/specs/TODO/ZZZ-1.brief.md` between runs (or run B under `ZZZ-2`)"; optionally note that the incidental artifacts-exist halt is itself worth one transcript line.

### F-8: The brief header's `**Status:** / **Priority:** / **Assignee:**` fields have no source in local-only mode
**Severity:** P3
**Where:** spec.md:319–320 (Phase 4 header template), :281 (Phase 0 step 5c)
**Claim:** the emitted header is `**Status:** … · **Priority:** … · **Assignee:** …` / `**Plane:** <TICKET-ID> (<uuid>, <state>) | unresolved (local-only)`.
**Why this is wrong:** the `**Plane:**` line has an explicit local-only branch; the three metadata fields do not. In conversation-only mode there is no ticket to read them from, and the spec never says what to write — leaving the implementer to invent values in the header of the artifact every downstream lens treats as authority. (Ticket mode is fine: the fields come from the resolved work item, as in `docs/specs/TODO/VHS-32.brief.md:3`.)
**Suggested fix:** one clause at :319 — "in local-only mode these read `Status: local-only · Priority: unset · Assignee: unassigned`." Best folded together with F-3's transcription rule.

### F-9: `sync.py:146` is in `cmd_push`, not the install path the sentence describes
**Severity:** P3
**Where:** spec.md:445 (Design 6)
**Claim:** "`sync.py install` copies file-by-file (`sync.py:96,146`), so a separately-installed upstream copy at those paths is overwritten".
**Why this is wrong:** `sync.py:96` is the `shutil.copy2` inside `cmd_install` (`def cmd_install` at `:62`, `def cmd_push` at `:110`) and does support the claim. `sync.py:146` is the `copy2` inside `cmd_push` — the config-dir → repo direction, which has nothing to do with overwriting a third-party install. The name-collision argument (and `AGENTS.md` bullet at :423, Risk 13 at :524) rests on the install path alone; the extra anchor points an implementer verifying the claim at the wrong function.
**Suggested fix:** cite `sync.py:96` only, or write "`sync.py:96` (install) — `:146` is the symmetric push copy".

### F-10: Residual label and bound nits left by round-2 fixes
**Severity:** P4
**Where:** spec.md:463 (checklist 9), :205 (§ 1.8), :534 (References, `lint.py:45–48`)
**Claim / why:** (a) checklist 9 still says "the **three-state** `## Scale` rule" — the exact label round-2 correctness F-8 flagged, now corrected at :338 to "four input cases, three emitted shapes"; the checklist should use the same words so the grep-level gate matches the design. (b) § 1.8's "bounded by construction at `round_cap × question_cap` named items" omits the S7 post-cap round (see F-1); once F-1 is fixed it should read `(round_cap + 1) × question_cap`. (c) `lint.py:45–48` is cited for "controlled vocabulary", but `SERVICES_VOCAB` — the entry the spec's `services: [issue-tracker?, shared-memory?]` declaration depends on — is at `:49`; the range should be `:45–49`.
**Suggested fix:** three one-token edits.

## Summary
P0: 0 | P1: 1 | P2: 3 | P3: 5 | P4: 1

STATUS: RED P0=0 P1=1 P2=3 P3=5 P4=1
