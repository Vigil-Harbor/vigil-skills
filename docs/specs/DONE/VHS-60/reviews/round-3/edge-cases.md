# Edge-Cases Review — round 3

Delta pass. The spec is byte-identical to `round-2/spec.copy.md` and `round-3/spec.copy.md`; `HEAD` is still the anchor commit `0158267f681386d7b51c3239ec2bc0b13c45ba25`. All five changed regions are code-drift hits from the untracked VHS-41 review/attempt trees, which is the noise Decision 5 exists to remove. The spec has no `## Deferred — follow-up required` section, so there are no rows to validate.

## Closure of round 2 findings

The closure manifest is empty (round 2 closed green, no P0/P1). The P3 findings are tracked for completeness.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Ticket not cached | CLOSED | spec § Deferred (P2+), line 404 records the brief-only degrade path; the outage recurred this round (F-4 below). |
| correctness | F-2 | Touched workflow files changed within the last week | CLOSED | spec.md:405; `HEAD` equals the anchor commit and the quoted blocks still resolve at `skills/spec-cycle/SKILL.md:363-375`, `:417`, `:453`, `:488`, `:490`, `:492`, `:506`, `README.md:10`, `docs/spec-workflow-reference.md:74` and `:81`, and `agents/spec-reviewer-edge-cases.md:88-98`. |
| edge-cases | F-1 | Ticket grounding remains unavailable | CLOSED | spec.md:404; no spec change required. Recurs as F-4 below. |
| conventions | — | (no findings) | N/A | round-2 `conventions.md` reports none. |

## Findings

### F-1: The `spec.md:<line>` Where form is not a recognised locator, so it emits every heading
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:256 | spec § `skills/spec-cycle/SKILL.md:492` — open-finding resolver
**Edge case:** An open finding whose `Where` is the colon form (`spec.md:132`, `spec.md:55-57`, `spec.md:147-158 (Edge cases table)`) with no `§` reference.
**What happens:** The replacement resolves only `line <n>` and `lines <start>-<end>` locators. A `spec.md:132` clause is about this spec, has no heading segment and no recognised locator, so it takes the "emit every current heading" fallback. The delta pass becomes full-width for that finding. Nothing breaks; the pass is just as wide as a full one.
**Why the spec misses it:** `spec.md:<line>` is the first `Where` form in all four reviewer output contracts (`agents/spec-reviewer-edge-cases.md:193` and its siblings) and is the most common form in this repo's stored reports. The current skill text says only "place its line", and the archived VHS-27 wording says "the clause has a line number", so the colon form is arguably placeable today. The replacement's explicit keyword grammar closes that reading. No scenario covers a colon-form `Where`; scenarios 10–16 all use `§` or `line`/`lines`.
**Suggested fix:** In the second replacement paragraph at spec.md:256, also recognise a locator directly after a this-spec path: `:<n>`, `:<start>-<end>` and `:<start>–<end>`, with the same validity rules. Mirror it in Decision 8 and add one scenario (`spec.md:132` selects only the heading owning line 132).

### F-2: An empty heading phrase matches every heading that starts with a non-alphanumeric character
**Severity:** P3
**Where:** spec.md:254 | spec § `skills/spec-cycle/SKILL.md:492` — open-finding resolver
**Edge case:** A segment whose phrase is empty after the comma cut or the terminal `and`/`or` trim, e.g. `spec §, line 40` or `spec § and § Decision 8`.
**What happens:** Arm 1 is empty. Arm 2 ("begins with the phrase and is followed by a non-ASCII-alphanumeric character") is satisfied by every heading whose text begins with a backtick, quote or other symbol. This spec has six such headings (`` `skills/spec-cycle/SKILL.md:363-375` — mode table `` and its siblings). Because arm 2 is non-empty, the uncut-segment retry never runs. The result is an arbitrary widening, not a narrowing, so it is safe.
**Why the spec misses it:** Neither Decision 7 nor the replacement says what an empty phrase does.
**Suggested fix:** Add "An empty phrase matches no arm" to the replacement, so the uncut retry and then the line or every-heading fallback apply.

### F-3: Raw-line validation runs before the archive drop, so a non-raw archive path still fails code drift
**Severity:** P3
**Where:** spec.md:107 | spec § Changed-path filtering
**Edge case:** An untracked file inside another ticket's `.reviews/` or `.attempt-<n>/` tree whose name git quotes (a double quote, control character or tab) or that contains `=>`.
**What happens:** The design applies the drop "after collecting and validating raw git-listing lines". The non-raw line is a code-drift failure before the drop can remove it, so the run takes the existing failure path instead of the no-op. This is graceful and conservative, but it is the same class of noise Decision 5 targets.
**Why the spec misses it:** Scenario 7 covers only well-formed archive paths; the ordering is stated but its consequence is not.
**Suggested fix:** Either state the consequence in § Changed-path filtering as accepted, or leave as is. No behaviour change is required.

### F-4: Ticket grounding unavailable
**Severity:** P3
**Where:** review grounding step 3
**Edge case:** The memory server returned HTTP 502 for the VHS-60 lookup.
**What happens:** The tracker record could not be compared with the brief; the review used the brief-only degrade path.
**Why the spec misses it:** Review-environment outage, not a spec defect.
**Suggested fix:** No spec edit.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 0

STATUS: GREEN
