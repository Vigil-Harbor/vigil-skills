# Correctness Review — round 3

Mode: delta. The spec and brief are byte-identical to the round-2 copies, and HEAD equals the round-2 `baseline.commit` (`0158267`). All five changed regions are code-drift hits caused by the untracked VHS-41 review and attempt archives, not by spec edits. Critique was limited to the five named headings.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P3) | Ticket not cached | CLOSED | `spec.md:404` records the brief-only degrade path; the outage recurred this round (F-2 below). |
| correctness | F-2 (P3) | Touched workflow files changed within the last week | CLOSED | `spec.md:405` records it with a recheck-before-implementation instruction. Still true: `f64bebe` (2026-10-13), `d3730b1` (2026-10-12) and `7abe102` (2026-10-11) touch the target files. Every quoted "Current" block I re-read still matches HEAD. |
| edge-cases | F-1 (P3) | Ticket grounding remains unavailable | CLOSED | `spec.md:404`. |
| conventions | — | No findings | n/a | Round-2 report is GREEN with zero findings. |

Other standing checks:
- **Ledger check:** round 2 has no P0 or P1 headings in any report and all three STATUS lines parse as GREEN, so the empty manifest is complete.
- **Deferred-findings block:** the spec has no `## Deferred — follow-up required` section (only `## Deferred (P2+)`), so there are no rows to validate.
- **Anchor drift:** none. `skills/spec-cycle/SKILL.md:363-375`, `:417`, `:453`, `:488`, `:490`, `:492`, `:506`, the four agent `# Delta scope` blocks, `README.md:10` and `docs/spec-workflow-reference.md:74`/`:81` all resolve to the quoted text.

## Findings

### F-1: The replacement resolver no longer places `spec.md:<line>` locators, so the reviewers' canonical `Where` form falls to every-heading
**Severity:** P1
**Where:** spec § `skills/spec-cycle/SKILL.md:492` — open-finding resolver, line 256; spec § Scenarios, line 342
**Claim:** "resolve every positive decimal `line <n>` and inclusive `lines <start>-<end>` or `lines <start>–<end>` locator in the clause, case-insensitively, against the predecessor `spec.copy.md`. … With no heading match and no placeable line in a clause about this spec, emit every current heading."
**Why this is wrong:**
- **The locator grammar is closed and word-form only.** A clause such as `spec.md:132` or `spec.md:198-212` has no `§` segment and no `line <n>` token, so nothing is placeable and it emits every current heading.
- **This regresses shipped behaviour.** The current text at `skills/spec-cycle/SKILL.md:492` says "Otherwise place its line in the predecessor `spec.copy.md`" with no fixed locator syntax. VHS-27 scenario 17 pins the intent (`docs/specs/DONE/VHS-27/spec.md:442`): "`spec.md:173` cites the spec; with no heading phrase it uses the line in the predecessor copy."
- **The colon form is the reviewer contract's first form.** `agents/spec-reviewer-correctness.md:197` gives `**Where:** spec.md:<line> | spec § <heading>`. Of 1592 `**Where:**` lines under `docs/specs/DONE/*/reviews` and `docs/specs/TODO/*.reviews`, 646 begin with `spec.md:<digits>`. This ticket's own reports use it: `VHS-60.reviews/round-1/correctness.md:18` (`spec.md:132`) and `round-1/edge-cases.md:12` and `:22` (`spec.md:198-212`, `spec.md:198`).
- **It contradicts the brief.** Brief Decision 7 says "every cited line is placed in the predecessor copy and its innermost owning heading is unioned in"; the Scope row says "Every cited line or line range is resolved separately". The spec narrows "every cited line" to one spelling, and the result is the whole-spec delta pass the ticket exists to remove (brief Problem item 2, Done-when 1).
- **No scenario covers a colon-form or line-only `Where`.** Scenarios 10–16 never exercise one, so the scenario walk (the only behavioural oracle) cannot catch the regression.
- **A second gap in the same grammar.** `lines 282 and 286` and `lines 70–72, 80` (forms seen in the VHS-27 reports) match neither `line <n>` nor a range. They are harmless when a heading arm matches, and unplaceable otherwise.

**Suggested fix:**
- In the `:492` replacement (and Decision 8 and § Open-finding resolver step 4, which declare the same grammar), add the colon form: a this-spec path token (`spec.md`, the ticket spec filename, or its repo-relative path) followed by `:<n>`, `:<start>-<end>` or `:<start>–<end>`, with the same validity rules. This includes the parenthesised form `(spec.md:307)`.
- Add a scenario: a `Where` of `spec.md:173` with no heading phrase selects the pair of the predecessor heading owning line 173 and does not emit every heading; `spec § Round-artifact state machine; spec.md:198-212` resolves both clauses.
- Optionally let `lines <a> and <b>` or a comma list place each number.

### F-2: Ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** n/a
**Why this is wrong:** `memory_search` (namespace `skills`, tags `plane_work_item` + `VHS-60`) returned a 502 Bad Gateway. The review proceeded from the brief, which transcribes the ticket description and both comments.
**Suggested fix:** None to the spec; `spec.md:404` already records the degrade path.

### F-3: "A direct child such as …" names descendants, not direct children
**Severity:** P4
**Where:** spec § Changed-path filtering, line 107
**Claim:** "A direct child such as `docs/specs/TODO/VHS-41.reviews/round-1/correctness.md` or `docs/specs/TODO/VHS-41.attempt-1/spec.md` is dropped"
**Why this is wrong:** The first example is two levels below the matched directory. Decision 5 and the `:490` replacement correctly say "every descendant", so the rule is unambiguous; only this sentence is loose.
**Suggested fix:** Replace "A direct child such as" with "A descendant such as".

## Summary
P0: 0 | P1: 1 | P2: 0 | P3: 1 | P4: 1

STATUS: RED P0=0 P1=1 P2=0 P3=1 P4=1
