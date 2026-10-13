# Correctness Review — round 4

Mode: delta. Critique was limited to the 21 named headings and the open finding's two headings. HEAD is still `0158267`.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Replacement resolver no longer places `spec.md:<line>` locators | CLOSED | All five manifest sites carry the fold. Decision 8 (`spec.md:76-83`) declares the colon and `#L` forms, the whole-path-token rule, and list/partial-range placement. § Open-finding resolver step 5 (`:130`) and the `:492` replacement (`:339`) state the same grammar. Scenarios 19, 20 and 25 (`:436-442`) exercise it. Done when (`:486`) gates it. Walked `spec.md:132`, `spec § Design (spec.md:289)`, and the real round-3 forms `spec.md:256 \| spec § …` and `spec § … , line 256; spec § Scenarios, line 342`: each places its line and none reaches the every-heading fallback. |
| correctness | F-2 (P3) | Ticket not cached | CLOSED | Recorded at `spec.md:503`. The outage recurred (F-1 below). |
| correctness | F-3 (P4) | "A direct child such as …" names descendants | CLOSED | `spec.md:120` now reads "A descendant such as". |
| edge-cases | F-1 (P2) | `spec.md:<line>` not a recognised locator | CLOSED | Same fold as correctness/F-1. |
| edge-cases | F-2 (P3) | Empty heading phrase matches symbol-led headings | CLOSED | Decision 7 (`:56`) says "An empty phrase matches no arm"; Decision 8 (`:74`) and the `:492` replacement skip an empty phrase; scenario 23 covers `spec §, line 40`. A residual marker-only variant is F-2 below. |
| edge-cases | F-3 (P3) | Raw-line validation runs before the archive drop | CLOSED | `spec.md:120` states the consequence and accepts it. |
| edge-cases | F-4 (P3) | Ticket grounding unavailable | CLOSED | `spec.md:503`. |
| conventions | F-1 (P3) | `.attempt-<n>/` undefined in tracked files | CLOSED | Gloss added in Decision 5 (`:48`) and the `:490` replacement (`:323`). |
| conventions | F-2 (P3) | Ticket grounding unavailable | CLOSED | `spec.md:503`. |

Standing checks:
- **Ledger check:** the only round-3 P0/P1 heading is correctness/F-1, and the manifest line matches its id with `(P1)` directly after. All three round-3 STATUS lines parse. Nothing is missing.
- **Deferred-findings block:** the spec has no `## Deferred — follow-up required` section (only `## Deferred (P2+)`), so there are no rows to validate.
- **Anchor drift:** none. A script confirmed every `Current` block in § Exact prose replacements is a verbatim substring of its target at the cited line: `skills/spec-cycle/SKILL.md:363`, `:377` (both sentences), `:379`, `:417`, `:445`, `:453`, `:455`, `:488`, `:490`, `:492`, `:506`; the four agent blocks at `:90`, `:88`, `:93`, `:77`; `README.md:10`; `docs/spec-workflow-reference.md:74` and `:81`.
- **Row references:** a grep for `[Rr]ows? [0-9]` in the skill returns exactly lines 374, 377, 379, 455 and 1079. That matches the spec's count of three paragraphs with moved rows and the unchanged `rows 1–5`, `Row 5` and two `row 4` references. Scenario 26's mapping agrees with the replacement table.
- **Recent commits on touched files:** `f64bebe` (2026-10-13), `d3730b1` (2026-10-12) and `7abe102` (2026-10-11) fall inside seven days. `spec.md:502` already records this with a recheck instruction; the quoted text still matches HEAD.
- **Cross-section walk:** these agree across Decision 7, Decision 8, § Open-finding resolver, the `:492` replacement and scenarios 10–25:
  - the joining-word, punctuation and locator-joiner lists;
  - the whole-path-token character set;
  - the per-clause fallback condition;
  - the blank-parent rule.
- **Decision 2:** the claim that the rename-failure sentence is kept byte-for-byte holds against `SKILL.md:453`. `round_cap` 4 for `big` (Decision 11) matches `SKILL.md:343`, and the `C`/`P` wording matches `SKILL.md:435`.
- **Done-when coverage:** all ten brief criteria map to a spec section and scenario.

## Findings

### F-1: Ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** n/a
**Why this is wrong:** `memory_search` (namespace `skills`, tags `plane_work_item` + `VHS-60`, `source_system: plane`) returned 502 Bad Gateway. The review used the brief, which transcribes the ticket description and both comments.
**Suggested fix:** None to the spec; `spec.md:503` already records the degrade path.

### F-2: A phrase made only of stripped marker characters is not skipped
**Severity:** P3
**Where:** spec § `skills/spec-cycle/SKILL.md:492` — open-finding resolver, line 337
**Claim:** "Skip a segment whose phrase is then empty. Compare the phrase with heading text case-sensitively, after deleting every backtick, asterisk, and double-quote character from both"
**Why this is wrong:**
- The skip is tested after normalization but before the backtick, asterisk and quote deletion. A phrase that is only such characters is non-empty at the skip and empty at the compare.
- The real case is a `Where` of the form ``spec § `### Decision 5 — …` ``. The `### ` inside the backticks opens a new heading-marker segment, so the `§` segment is a lone backtick.
- Decision 7's "An empty phrase matches no arm" is not carried into the `:492` replacement text. As written, the lone backtick counts as a non-empty phrase that matched nothing, so a clause with no placed line emits every heading.
- This widens, which the spec treats as the safe direction. The form appears once in 1601 stored `**Where:**` lines (`VHS-60.reviews/round-3/conventions.md:26`).

**Suggested fix:** In the `:492` replacement, test emptiness after the marker-character deletion (for example "Skip a segment whose phrase is empty after that deletion"), or leave it and add the case to `## Deferred (P2+)`.

### F-3: The whole-path-token rule is stated only beside the locator grammar, but scenario 20 relies on it for the file decision
**Severity:** P3
**Where:** spec § `skills/spec-cycle/SKILL.md:492` — open-finding resolver, lines 337-339; spec § Scenarios, line 437
**Claim:** "another file path with no this-spec name emits every current heading" (paragraph 1) and "A this-spec name counts only when the character before it is absent or is not a letter, digit, `.`, `/`, backslash, `-`, or `_`" (paragraph 2, inside the locator definition).
**Why this is wrong:** Scenario 20 expects a clause opening with `docs/specs/DONE/VHS-27/spec.md:291` to be "another path". That holds only if the token rule in paragraph 2 also governs the file decision in paragraph 1. A reader can work this out, and the scenario pins the outcome, so it is a clarity point only.
**Suggested fix:** Move the "counts only when…" sentence to directly after the file-decision sentence, or add "(as a whole path token, defined below)" there.

### F-4: The deletion gate's "every removed line" test does not fit sentence-level replacements
**Severity:** P4
**Where:** spec § Test plan, line 461
**Claim:** "every removed line must be the old side of a `Current` block in § Exact prose replacements"
**Why this is wrong:** The row-reference and set-lead-in edits replace one sentence inside a long paragraph line (`SKILL.md:377`, `:379`, `:445`, `:455`). `git diff` reports the whole paragraph line as removed, and that line is not literally a `Current` block. The gate's closing sentence ("until the old wording is shown to survive elsewhere") resolves it, so this is wording only.
**Suggested fix:** Say "every removed line must be, or must contain, the old side of a `Current` block, and must differ from its added counterpart only by that block's replacement".

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 3 | P4: 1

STATUS: GREEN
