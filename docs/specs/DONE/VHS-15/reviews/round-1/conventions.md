# Conventions Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Residual hardcoded "three" at spec-workflow-reference.md:153 (closure-tracking invariant) not in the reconciliation table
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design §6 table; the omitted target is `docs/spec-workflow-reference.md:153` (and `:54`)
**Convention violated:** The spec's own reconciliation goal (Done-when 6) and self-imposed consistency check (Test plan item 9).
**Evidence:** On disk, `:153` reads "**Round 2+ closure tracking.** Each reviewer reads **all three prior-round reports**…"; `:54` carries the identical phrasing. Under the fourth lens, each reviewer reads four reports when scale is on, so "all three prior-round reports" becomes a stale count. This phrasing matches neither alternation in the item-9 grep, so the spec's own consistency gate passes while the contradiction survives.
**Suggested fix:** Add `:54` and `:153` to the §6 table, reconciling to "reads all prior-round reports present (the three default lenses plus `scalability.md` when the scaling lens ran)." Broaden the item-9 grep to include `all three prior-round`.

### F-2: README.md and portability-contract.md reconciliation is scope beyond the brief's named targets — correctly flagged
**Severity:** P3
**Where:** spec § Decision 9; § Design §6 rows for `README.md`, `docs/portability-contract.md:138`
**Convention violated:** None — this is the drift-visibility note required by the "Silent spec additions vs the brief" axis. Brief Done-when names only AGENTS.md / SKILL.md description / spec-workflow-reference.md.
**Evidence:** The spec adds two more files and labels them Decision 9 "spec-level additions, flagged," pre-conceding portability-contract.md drops to a no-op if judged out of scope. Correct (c) classification, not (d) silent drift.
**Suggested fix:** None required. The human approving the drift-check should note these two files are reconciled beyond the brief's literal Done-when list.

### F-3: The grounding-step-7 edit to the three existing agents is closure plumbing required by an authorized Done-when, not a fenced lens re-tuning
**Severity:** P3
**Where:** spec § Decision 8; § Design §5; Scope
**Convention violated:** None. Recording the brief-fence judgment.
**Evidence:** Brief Out-of-scope fences "Re-scoring or re-tuning the existing three lenses, …severity rubric, …gate formula, …round cap." The edit touches only grounding step 7 (which prior-round files the closure-read enumerates) — not the critique lens, severity block, gate formula, or round cap. It is instrumentally required by brief Done-when 2 ("fold into round-2+ closure tracking exactly as the other lenses do"). The fence argument holds; authorized-by-Done-when plumbing.
**Suggested fix:** None.

### F-4: AGENTS.md "name, description, user_invocable" frontmatter convention slightly overstated
**Severity:** P4
**Where:** spec § Design §1 (frontmatter)
**Evidence:** AGENTS.md:66 says agents use `name, description, user_invocable`, but the three existing agents carry only `name` + `description`. The new agent correctly mirrors the actual existing-agent shape. AGENTS.md:66 is stale prose predating this ticket.
**Suggested fix:** Optional: while editing AGENTS.md, a one-word correction at line 66. Not required for green.

## Decision classification (Silent-additions audit)

| Spec decision | Class | Basis |
|---|---|---|
| D1 Opt-in / off-by-default | (a) brief | brief Decisions, divergence verified in ticket |
| D2 Option B over A | (a) brief / (b) ticket | brief resolves ticket's open A-vs-B |
| D3 One declaration with target N | (a) brief | brief |
| D4 Peer reviewer, pass budget untouched | (a) brief | brief |
| D5 Shared severity verbatim | (a) brief | brief |
| D6 Architectural + operational scale | (a) brief | brief |
| D7 Security-first | (a) brief | brief |
| D8 No regression; step-7 edit is plumbing | (a) brief + (c) | brief fences re-tuning; step-7 mechanism is spec-level elaboration with rationale |
| D9 README + portability-contract reconciliation | (c) spec-addition-with-rationale | beyond brief Done-when; explicitly flagged |

No (d) silent additions found.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 1

STATUS: GREEN
