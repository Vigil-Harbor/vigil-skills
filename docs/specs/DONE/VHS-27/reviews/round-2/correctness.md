Round-1 fixes hold against the current skill and agents. One docs edit site is still missing, and the Plane ticket was not retrieved.

# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Reader state `changed` never selects a candidate round | CLOSED | spec § Decision 14 and § Mode (candidate from `source: review` plus `^[1-9][0-9]*$`, including reader state `changed`); scenario 2b; scenario 5. Six-state table at `skills/spec-cycle/SKILL.md:64-70` still matches the spec's `unreadable` / `changed` paraphrase. |
| correctness | F-2 | Green-round `spec.copy.md` is taken before post-green polish | CLOSED | spec § Decision 2, § Artifacts, § Two counters, § Ledger, scenario 2. Current green write is still after 2g (`SKILL.md:567`, `:802-839`); the spec now rewrites `spec.copy.md` after polish and before that marker. |
| correctness | F-3 | Output-contract closure line stays on the round-1 rule | CLOSED | spec § Delta contract replaces `(Required for round_number ≥ 2; "N/A — round 1" otherwise.)` in all four agents. That parenthetical is present (`agents/spec-reviewer-correctness.md:174`, edge-cases `:169`, conventions `:163`, scalability `:110`). |
| correctness | F-4 | Ticket not cached | CLOSED | spec `## Deferred (P2+)` records no spec change. Re-filed below as this round's grounding finding; the ticket was still not retrieved. |
| edge-cases | F-1 | Ledger coverage is a substring test, so a dropped shorter id is invisible | CLOSED | spec § Delta contract ledger check (token `(^|[^A-Za-z0-9])<lens>/F-<k>([^0-9]|$)`, severity on that line before the title, title matches excluded); scenario 11; § Done when. |
| edge-cases | F-2 | House-style `path:line` citations never count as code drift, so scenario 10 no-ops | CLOSED | spec § Changed regions strips `:digits`, `:digits-digits`, en-dash ranges, and `#Ldigits` before both citation tests; scenario 10 requires `` `skills/spec-cycle/SKILL.md:388` `` not to no-op. `git diff --name-only` on this tree prints forward slashes. |
| edge-cases | F-3 | Any edit marks every ancestor section changed, so a delta pass may explore the whole spec | CLOSED | spec § Changed regions exclusive body and "do not emit an ancestor"; § Delta contract "descendant heading is in scope only when it is itself named". |
| edge-cases | F-4 | A git error suppresses the no-op, then an empty delta may go green and replace the baseline | CLOSED | spec § Decision 5, § Mode (`mode: full (code-drift unavailable)` before the pending write), § Two counters pass-2 stop, § Artifacts (delete that pass's `baseline.commit`), scenario 12. `git diff --name-only` exits 0 when there is a diff; only `--exit-code` exits 1, so a real diff is not a command failure. |
| edge-cases | F-5 | A review marker whose round is not a positive integer falls through to delta | CLOSED | spec § Mode row 10 and scenario 13; marker writes use temp-then-rename (§ Artifacts). |
| edge-cases | F-6 | `baseline.commit` and `ledger.md` treat a Windows newline as a corrupt artifact | CLOSED | spec § Mode accepts `\n` or `\r\n` on read and strips CR before the ledger header test; § Artifacts writes `baseline.commit` as raw LF. |
| edge-cases | F-7 | The no-op can report green for a red marker when reports are missing or headings do not parse | CLOSED | spec § No-op steps 2–3 and the printed `<verdict>`; § Changed regions maps a line-only `Where`, or every heading if the line cannot be placed. |
| edge-cases | F-8 | Only the immediate next round directory is reserved, so a later pass can overwrite an existing round | CLOSED | spec § Decision 8 and § Mode row 9 reserve `candidate+1` and `candidate+2`; full start requires `start` through `start+round_cap-1` free; § Artifacts partial-set routing; scenario 13. |
| conventions | F-1 | Output-contract closure line is not an edit site | CLOSED | Same edit as correctness F-3 (§ Delta contract output-contract parenthetical; § Test plan). |
| conventions | F-2 | Correctness anchor replacement leaves the old P1 rule in place | CLOSED | spec § Decision 4 and § Delta contract replace both the **Stale anchors** bullet and cross-section item 2 (`agents/spec-reviewer-correctness.md:93` and `:107-109`). |
| conventions | F-3 | Decision 7 omits the Follow-up filter § Mode applies | CLOSED | spec § Decision 7 now drops carriage returns and `**Follow-up:**` lines and no other byte, matching § Mode and the fingerprint at `SKILL.md:53`. |
| conventions | F-4 | Single-counter write-points and closure prose are not named as edit sites | CLOSED | spec § Docs names **Write points**, **Interrupted run**, the Stakes-tier `round == round_cap` paragraph, both **Round 2+ closure tracking** copies, and the `AGENTS.md` spec-brief grill clause. Those headings exist (`SKILL.md:55`, `:946`; `docs/spec-workflow-reference.md:94`, `:156`, `:306`; `AGENTS.md:25`). |
| conventions | F-5 | Invocation syntax is specified once and copied in three places | CLOSED | spec § Invocation names the H1 `Invoked as` line and the `## Attest mode` usage halt (`SKILL.md:15`, `:904`). |
| conventions | F-6 | Mode row 9 is a spec-level addition to the brief's mode list | CLOSED | spec § Decision 14 lists the span-occupied row and the non-integer `round` row as storage rules under Decision 8. |
| conventions | F-7 | § 2b's sample disposition still cites a skill line | CLOSED | spec § Ledger changes the sample at `SKILL.md:437` (`fixed: re-anchored to SKILL.md:142`) to `fixed: re-anchored to § Design`. |

## Findings

### F-1: Workflow reference still describes one round counter outside the named edit sites
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Docs
**Claim:** "The same sentence is applied to the adapting bullet `**Round 2+ closure tracking.**` so the two copies do not disagree." The Stakes-tier paragraph is the other named site: "`round == round_cap` is the FROZEN/REWRITE rewrite" describes pass index `P`, and "a delta pass whose cumulative round equals `round_cap` does not run FROZEN/REWRITE."
**Why this is wrong:** Those two edits leave other copies stating a single counter. `docs/spec-workflow-reference.md:72` says the final round, `round == round_cap`, is the rewrite. Steps 6–8 (`:90-92`) still halt and rewrite at `round == round_cap` with a FROZEN window of rounds `1 .. round_cap-1`. In `## Adapting to your stack`, the load-bearing bullet immediately after the closure bullet (`:307`) says "Targeted rewrite at round `round_cap`" and "The FROZEN window is rounds 1 .. round_cap-1." Skill 0 (`:31`) still says the grill follows `round_cap` rounds only. § Two counters is the behavior that must ship; these paragraphs are the guardrail Decision 16 says must survive the next skill edit, and the spec's own "two copies do not disagree" rule does not reach them.
**Suggested fix:** In § Docs, name those four sites and state that each describes the first invocation's pass index `P`. A delta pass does not run FROZEN/REWRITE when its cumulative round equals `round_cap`, and the grill also follows a delta halt at cumulative `C`.

### F-2: Ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Ticket VHS-27 is the canonical acceptance source when it conflicts with the brief.
**Why this is wrong:** This run was instructed not to call shared memory or the tracker. No ticket record was retrieved. The brief is the source used for Done when and Decisions 1–16. The spec already records that disposition under `## Deferred (P2+)`.
**Suggested fix:** None for the spec. Re-check the Plane ticket when the mirror is reachable if its wording differs from the brief.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

STATUS: GREEN
