# Correctness Review — round 5

> Second cross-model round (Claude reviewer agents), delta over the Codex fold of the first Claude round, run outside the `/spec-cycle` loop on 2026-10-13. Persisted by hand from the agent's hand-back text; not a `round-<C>/` directory.

## Closure of round 4 (cross-model-claude) findings

I checked each finding against the current spec at `docs/specs/TODO/VHS-56.spec.md`, not against the fold author's claims.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Reconciliation edits have no defined home, so re-rendering or revise drops folds and operator replacements | CLOSED | **Single source of truth.** Decision 1 (spec:43-45) makes the held candidate authoritative after the first mapping. Reconciliation edits it in place, and Phase 5 writes the confirmed bytes. Design 2 (spec:193) says "re-render" means display, not re-derivation.<br>**Where folds may land.** Design 2 (spec:195) pins the editable sections and the settled-target carve-out. Design 2 (spec:197) amends the `:224` transcription rule; that rule does exist at `skills/spec-brief/SKILL.md:224`.<br>**Revise path.** Design 6 (spec:238-240) amends Q-linked Settled items in `prior_summary` (the grammar at `skills/grilling/SKILL.md:140` requires `(Q<n>)`). Q-less items stay in the candidate and in seed constraints. After the resume, only the affected sections are updated. The `--no-grill` Add a decision branch appends to the held candidate.<br>**Write.** Design 6 (spec:242) writes the exact Confirm bytes with one outcome block.<br>**Test.** Test plan 14 checks all of this.<br>All three sub-defects (re-render, the `:224` rule, option-2 revise) are addressed. Residual gaps are filed below as P2s, not as a reopen. |
| edge-cases | F-1 (P1) | Doubt-pass edits have no durable home (same root) | CLOSED | Same evidence as correctness F-1. Edge-cases items 3 and 4 asked for Phase 5 to write the preview verbatim and for a revise to keep resolutions. Decision 1 and Design 6 (spec:242) now state the first, and Design 6 (spec:238-240) the second. |
| correctness | F-2 (P2) | "host cannot wait" branches unreachable | CLOSED | Decision 3 (spec:55) says the tier gate already stops a non-waiting host (`SKILL.md:92`, `:94`, both verified) and drops `can_wait`. `host cannot wait` is gone from Decision 4's reasons (spec:86) and from Design 7. Test plan 4 (spec:270) tests the no-wait halt at the tier gate. A grep finds no remaining `headless`, `can_wait` or `host cannot wait` branch. |
| correctness | F-3 (P2) | Reviewer payload omits `wiki_root` | CLOSED | Design 4 (spec:212) adds `wiki_root` and `project_slug`, or an explicit "wiki unavailable". Phase 0 resolves both at `SKILL.md:34`. |
| correctness | F-4 (P3) | Skip reason for `small` with no reviewer | CLOSED | Decision 3 (spec:57) and Design 3 (spec:203) both say the tier-small reason applies "including when no reviewer is eligible". |
| correctness | F-5 (P3) | Two-cycle count aggregation and summary-line mapping | CLOSED | Decision 4 (spec:88) pins distinct-root cumulative counts, how reopen is counted, final-disposition replacement, and the `completed in N cycle(s)` → `Result: completed` / `Cycles: N` mapping. Design 6 (spec:231) adds `completed at cap (N cycle(s))`. |
| correctness | F-6 (P3) | ticket not cached | DEFERRED | Spec § Deferred (P2+) at spec:312. It is still access-denied this round (see F-8). |

**Round-4 Codex polish (Design 6 ¶3 and Test plan 14, unreviewed).**
- **Correct:**
  - The `(Q<n>)` grammar claim matches `skills/grilling/SKILL.md:140`.
  - The resume-contract anchors (`:21`, `:23`) match.
  - The `seed` context exists (`grilling/SKILL.md:18`).
  - Test plan 14 agrees with Design 6.
- **Gaps:** reopen serialization and some dead phrasing remain (F-2, F-7).

**Closure formalities.**
- No formal `closure_manifest` was supplied, so I ran no ledger check.
- The spec has no `## Deferred — follow-up required` section, only `## Deferred (P2+)`. The Deferred-findings rules therefore have no rows to check.

## Findings

### F-1: A reviewer finding on Tier or Scale has no defined route; the contradiction batch's `replace` could set a tier outside the tier gate
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 (spec:195); § Decision 8 (spec:108-115); § Decision 10 (spec:132-139)

**Claim:** Design 2 says "Tier and Scale remain operator-set and require operator resolution for any proposed change." Decision 8's settled targets are only Decisions carried forward, Out of scope, explicit ticket decisions and Done-when acceptance statements.

**Why this is wrong:**
- Tier and Scale are not Decision 8 targets. Decision 10's settled-target precedence therefore does not catch a Tier or Scale finding.
- The only operator path the spec defines for a "settled-decision contradiction" (class 3) is Decision 8's batch, whose answers are `keep | replace: <text> | reopen`.
- If the executor routes a Tier challenge there:
  - `replace: tweak` writes `tweak` into a brief, which `skills/spec-brief/SKILL.md:110` forbids.
  - `replace: irreversible` changes the tier mid-pass without the Design 6 tier-gate re-ask or the doubt-policy re-evaluation, so the pass that is running keeps big's Skip option.
  - `reopen` leaves `## Tier` with no legal value.
- A free-text Scale replacement can produce `**Factor:** yes` without a Target. `SKILL.md:236` exists to prevent exactly that.

**Suggested fix:** Add to Design 2 or Decision 10:
- A finding against Tier is shown to the operator as advisory evidence. The only way to change the tier is Confirm option 4, which re-runs the tier gate and Design 6's tier rule.
- A finding against Scale either goes to `## Risks / decisions` ending "spec author pins this", or is resolved only through the existing four Scale emission cases.
- Add a matching Test plan row.

### F-2: Reopen serialization into `prior_summary` is underspecified against grilling's grammar
**Severity:** P2
**Where:** spec § Design 6 ¶3 (spec:238), the Codex post-green polish; Test plan 14 (spec:280)

**Claim:** "reopen records the operator's settled choice to leave the named issue open plus its Open frontier item. Amend genuine Q-linked Settled items within `prior_summary`…"

**Why this is wrong:**
- For a Q-linked item, this reads as keeping a Settled `(Q<n>)` entry and also adding an Open frontier entry.
- Grilling's grammar does not support that:
  - An Open Q-item needs `(Q<n>)` plus an `unresolved because:` token from a closed set: `round-cap | deferred | stopped | blocked-on: …` (`skills/grilling/SKILL.md:143`). "Reopened by operator" is not in that set.
  - The resume contract treats a Q as either Settled or Open (`:23`).
- So a reopened Q is either present in both lists, or carries an invented reason token. That is the same grammar extension conventions R4/F-1 removed for Q-less items.
- Test plan 14 tests only the replace case and the Q-less case.

**Suggested fix:** Pin one representation. For example, a Q-linked reopen leaves Settled and appears once in Open frontier as `(Q<n>) … unresolved because: deferred`. Under the resume contract (`:23`) it is then not re-asked unless it is downstream of the revised Q. Q-less reopens stay only in the held candidate. Add the reopen case to Test plan 14.

### F-3: Revise-path metadata goes stale under the candidate-authoritative rule (Interview bullet, BRIEF WRITTEN counts)
**Severity:** P2
**Where:** spec § Design 6 ¶4 (spec:240); § Decision 1 (spec:45)

**Claim:** "After the resumed interview returns, update only candidate sections affected by its explicit revised decisions and their consumers, preserving unrelated verified folds…"

**Why this is wrong:**
- Today Phase 4 re-maps from the latest summary. That keeps the final `## References` bullet `Interview: <n> rounds, exit <token>` fresh (`SKILL.md:231`).
- Under the new rule that bullet is not a consumer of any revised decision. Read strictly, a revise (for example one exiting `revised-after-cap (+1 round)`) writes the pre-revise round count and exit token.
- Facts newly established in the resumed round that no revised decision relies on also have no defined destination in Scope or References.
- Separately, the post-write print `<s> settled, <o> open` (`SKILL.md:247`) is derived from the summary. After doubt-pass replace or reopen answers, it can disagree with the written brief.

**Suggested fix:** In Design 6, list the summary-derived metadata that is always refreshed after a resume: the Interview bullet, newly established Facts going to References, and Scope rows. State that the BRIEF WRITTEN counts are taken from the written candidate.

### F-4: The `small` path names two different points where the held candidate is created
**Severity:** P3
**Where:** spec § Design 2 (spec:193); § Design 3 (spec:203); § Decision 3 (spec:57)

**Claim:** Design 2 says the candidate is created "on the invocation's first entry to Phase 3". Design 3 says small goes "directly to Confirm". Decision 3 says option 5 "runs Phase 3 and returns to Confirm".

**Why this is wrong:** One reading is that small (or a no-reviewer big) never enters Phase 3 before Confirm. In that case:
- Confirm has no held candidate to display.
- The `--no-grill` Add a decision branch has nothing to append to (Design 6 ¶4).
- Option 5 would be the "first entry" and re-apply the mappings.

A careful reader resolves this as "Phase 3 always runs; the gate decides whether to dispatch", but the text does not say so.

**Suggested fix:** State that Phase 3 always runs after the interview path. Candidate creation and the Design 3 gate come first, and "directly to Confirm" means "without an offer or dispatch".

### F-5: The renumbering list contains a line with no phase reference and omits two stale `--no-grill` flow statements
**Severity:** P3
**Where:** spec § Design 6 (spec:242)

**Claim:** "Renumber only spec-brief's own phase references, including `skills/spec-brief/SKILL.md:124`, `:180`, `:182`, `:216`…"

**Why this is wrong:**
- `SKILL.md:182` contains no phase number. Only `:124`, `:180` and `:216` say "Phase 4".
- The spec also misses statements whose meaning changes, not their numbers:
  - `SKILL.md:124`: "or under `--no-grill` to Confirm". It should now go to the doubt pass.
  - `docs/spec-workflow-reference.md:11` and `:21`: "`--no-grill` skips the interview but not the seed gate, the tier gate, or the confirmation step / Confirm". These should now also name the doubt pass, which Decision 3 says still runs.
- Test plan 1 and 12 would catch these, but the edit list does not.

**Suggested fix:** Drop `:182`. Add `:124`'s `--no-grill` destination and the two workflow-reference `--no-grill` sentences to the Design 6 and Design 8 edit list.

### F-6: Cycle-2 failure: one at-cap state is writable after an upgrade to irreversible but not when irreversible was chosen directly
**Severity:** P3
**Where:** spec § Decision 12 (spec:175-177); § Design 6 ¶2 (spec:236)

**Claim:** "tier-only upgrades retain a completed record, including this at-cap record … a newly attempted failure under irreversible still cannot be skipped."

**Why this matters:**
- Two runs can reach the same state: cycle 1 reconciled and changed, then cycle 2 failed twice.
- Via big, Skip, then an upgrade to irreversible, that state is written as `completed at cap`, `Cycles: 1`.
- Under irreversible chosen directly, the same state offers only Abort, which discards the interview and the cycle-1 reconciliation.
- The written outcome would be identical, and both satisfy the spec's Done-when #3 ("a cross-model cycle completed").

The spec states this deliberately. I am flagging it for the drift check, not as a contradiction.

**Suggested fix:** Optional. Under irreversible, after a reconciled cycle 1 and an exhausted cycle-2 retry, offer "Accept cycle 1 (completed at cap)" next to Abort. Otherwise, leave the asymmetry as is and list it in the drift checklist.

### F-7: Minor text issues: Decisions preamble, dead phrases, history-relative wording
**Severity:** P4
**Where:** spec:31; spec:238; spec:240; spec:177

- **spec:31.** "Decisions 1–3, 5, 7–10 and the Design pin the brief's Risks / decisions 1–10." Decision 4 pins Risks 4 and Decision 6 pins Risks 6 directly. The sentence suggests that 4 and 6 are only additions.
- **spec:238.** "Keep ticket decisions … without a Q" in the grilling-resume path is dead text. Ticket decisions exist only under `--no-grill`, where option 2 is Add a decision, not a grilling resume.
- **spec:240.** "Only an explicit operator revision that names an affected constraint" cannot happen through option 2, which names a Q number.
- **spec:177.** "Delete the cycle-2-failure status and `dispatch_failed` flag" refers to a prior spec draft, not to anything in `SKILL.md`. The unqualified "conventions F-7" should read `cross-model-claude conventions/F-7`.

**Suggested fix:** Use "Decisions 1–10", reword the two dead clauses, and state the rule positively ("there is no separate cycle-2-failure status or flag").

### F-8: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Not applicable; this is a process note.
**Why this is wrong:** `memory_search` on namespace `skills`, tags `["plane_work_item","VHS-56"]`, returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. I used the brief's narrowed contract. The spec's Deferred (P2+) section (spec:310, :312) already records this.
**Suggested fix:** None for the spec.

## Grounding notes (no finding)

**Anchors.** Every `path:line` the fold added or changed resolves to the described text at HEAD `7c2dfa0`, which equals the round-4 baseline commit:
- `skills/spec-brief/SKILL.md`: `:5`–`:9`, `:88`, `:92`, `:94`, `:124`, `:160`, `:162`, `:166`, `:168`, `:170`–`:176`, `:180`, `:184`, `:186`, `:188`, `:202`, `:205`, `:216`, `:218`, `:224`, `:254`, `:256`.
- `skills/grilling/SKILL.md`: `:21`, `:23`, `:61`, `:140`.
- `lint.py`: `:44`, `:45`.
- `skills/spec-cycle/SKILL.md`: `:1065`, `:1067`, `:1070`.
- `docs/spec-workflow-reference.md`: `:23`–`:25`, `:102` (spec-cycle Phase 3), `:147`–`:152` (Stakes tier table), `:246` (ship-spec Phase 3).
- `README.md`: `:9`, `:65`. `AGENTS.md`: `:25`, `:35`.

No anchor drift: there is no dead symbol and no moved line.

**Done-when mapping.**
- #1 maps to Decisions 3 and 4.
- #2 maps to Decisions 8 and 10, with settled-target precedence.
- #3 maps to Decisions 3 and 12 and Designs 1 and 6.
- #4 maps to § Test command.

The brief's Risks 1–10 are each pinned.

**Cross-section walk.** These agree across sections:
- Decision 4 ↔ Design 6 on the result tokens and summary line.
- Decision 8 ↔ Decision 11 ↔ Design 4 on `question_cap` (7 under `--no-grill`).
- Decision 12's menu ↔ Design 7's failure modes ↔ Test plan 16.
- Decision 11's example is internally consistent (one block, `Findings: 1`, `DOUBT FINDINGS=1`).
- The Scope table matches Design 8, including AGENTS.md's Stakes tier paragraph.

**Git history.** All commits from the last 7 days touching the target files (`33b9215`, `fad52c7`, `f64bebe`, `d3730b1`, `7abe102`, `5f640d0`) predate the baseline. The untracked `docs/specs/TODO/VHS-41.spec.md` edits `AGENTS.md:7` and `:46-48` only, so it does not overlap VHS-56's `:25` and `:35`.

**Ground-truth.** The round-4 ledger exists and holds only the no-claims line, so there are no rows to sample and no omission boundary. As instructed, this is a stated limit, not a finding. I verified every fold-added claim about current files directly instead (above).

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 4 | P4: 1

STATUS: GREEN
