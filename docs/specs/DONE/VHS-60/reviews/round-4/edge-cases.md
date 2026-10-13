# Edge-Cases Review — round 4

Delta pass. Spec and brief were read fresh from disk, and `HEAD` is still the anchor commit `0158267f681386d7b51c3239ec2bc0b13c45ba25`.

- **Anchors:** every quoted `Current` block still resolves at its cited line: `skills/spec-cycle/SKILL.md:363-375`, `:377`, `:379`, `:417`, `:445`, `:455`, `:488`, `:490`, `:492`, `:506`, `:1079`; the four agent `# Delta scope` blocks (correctness `:90`, edge-cases `:88`, conventions `:93`, scalability `:77`); `README.md:10`; `docs/spec-workflow-reference.md:74` and `:81`. No anchor drift.
- **Row references:** a repo-wide search for `[Rr]ows? [0-9]` finds mode-table references only at `SKILL.md:374`, `:377`, `:379`, `:455` and `:1079`, which is the set the spec lists. The other hits are spec-close's own table.
- **Deferred-findings block:** the spec has no `## Deferred — follow-up required` section (only `## Deferred (P2+)`), so there are no rows to validate and no routing violations.
- **Critique scope:** limited to the 21 headings in `changed_regions` plus the open-finding headings.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Replacement resolver no longer places `spec.md:<line>` locators | CLOSED | All five manifest sites carry the fold: Decision 8 (spec.md:76-83), § Open-finding resolver step 5 (spec.md:130), the `:492` replacement's second paragraph (spec.md:339), scenarios 19, 20 and 25 (spec.md:436-437, 442), Done when (spec.md:486). Walked `spec.md:132`, `spec.md:198-212`, `(spec.md:307)`, `spec.md:256 \| spec § …`, and the foreign forms `docs/specs/DONE/VHS-27/spec.md:291` and `VHS-27.spec.md:256`; each resolves as the scenarios state. The optional word-form list (`lines 282 and 286`) is also folded. |
| correctness | F-2 (P3) | Ticket not cached | CLOSED | spec.md:503 records it; the outage recurred (F-5 below). |
| correctness | F-3 (P4) | "A direct child such as …" names descendants | CLOSED | spec.md:120 now reads "A descendant such as". |
| edge-cases | F-1 (P2) | `spec.md:<line>` form not a recognised locator | CLOSED | Same fold as correctness/F-1. |
| edge-cases | F-2 (P3) | Empty heading phrase matches symbol-leading headings | CLOSED | Decision 7 "An empty phrase matches no arm" (spec.md:56); Decision 8 and the `:492` replacement skip an empty segment (spec.md:74, 337); scenario 23. One residual variant is filed as F-1 below. |
| edge-cases | F-3 (P3) | Raw-line validation runs before the archive drop | CLOSED | spec.md:120 states the consequence as accepted. |
| edge-cases | F-4 (P3) | Ticket grounding unavailable | CLOSED | spec.md:503. |
| conventions | F-1 (P3) | `.attempt-<n>/` undefined in tracked files | CLOSED | Gloss added in Decision 5 (spec.md:48) and the `:490` replacement (spec.md:323). |
| conventions | F-2 (P3) | Ticket grounding unavailable | CLOSED | spec.md:503. |

No REOPENED, PARTIAL or DEFERRED items.

## Findings

### F-1: A phrase that is empty only after marker deletion counts as a miss, so `§ `### Heading`` emits every heading
**Severity:** P3
**Where:** spec § Decision 7 — ordered boundary-aware heading matching always unions cited lines (spec.md:56) | spec § `skills/spec-cycle/SKILL.md:492` — open-finding resolver (spec.md:337)
**Edge case:** A `Where` that wraps a heading with its hash marker in backticks, as round 3's own conventions/F-1 does: ``spec § `### Decision 5 — ignore every open ticket's review and attempt archives` ``.
**What happens:**
- The `§` opens one segment and the `### ` inside the backticks opens a second, so the first segment is a lone backtick.
- That phrase is non-empty after normalization (the trim list is `,` `:` `.` `)` `]`), so the skip rule does not fire.
- The comparison then deletes the backtick, the phrase is empty and matches no arm, and the retry gives the same result.
- It is therefore "a non-empty phrase that matched no heading", and with no placed line the clause emits every current heading, although the second segment matches exactly.
- The same holds for a segment of only `**` or `"`. This is a widening, so it is safe; one of 1604 stored `Where` lines has this shape.
**Why the spec misses it:** The skip is defined on the normalized phrase and the emptiness rule on the marker-deleted phrase; nothing joins them.
**Suggested fix:** In Decision 8 and the `:492` replacement, make the skip read "a segment whose phrase is empty after normalization and marker deletion is skipped".

### F-2: A word-form line that belongs to another file is placed in this spec and can rescue an unmatched phrase
**Severity:** P3
**Where:** spec § Decision 8 — segment multiple references and expand line ranges (spec.md:78-81) | spec § Scenarios, scenario 20
**Edge case:** A clause about this spec that also cites another file's line in words, such as `spec.md:17, SKILL.md lines 129, 169, 176, 252` or `spec § <phrase>, SKILL.md line 173`. Seven stored `Where` lines have this shape.
**What happens:**
- The whole-path-token guard covers only the colon form. The word form has no file binding, so 129, 169, 176 and 252 are placed in the predecessor spec copy and their unrelated owners are unioned in. That is a widening.
- The narrowing case is rarer: if the `§` phrase matches nothing, the foreign line is "a placed line", which suppresses the every-heading fallback and leaves only an unrelated heading in scope.
**Why the spec misses it:** Scenario 20 exercises only the foreign colon form.
**Suggested fix:** Optional. Say that a word-form locator immediately preceded by another file's name (a path token that is not a this-spec name) is not placed, and add that form to scenario 20. Otherwise record it in `## Deferred (P2+)`.

### F-3: The parenthesis cut adds a second way for an exact match to pre-empt a longer heading
**Severity:** P3
**Where:** spec § Decision 8 — segment multiple references and expand line ranges (spec.md:72) | spec § Deferred (P2+) (spec.md:504)
**Edge case:** A spec with both a heading `X` and a heading `X (…)`, and a `Where` of `spec § X (…)`.
**What happens:** The phrase is cut at the parenthesis to `X`, arm 1 matches `X` exactly, and the retry on the uncut segment never runs. The heading the finding names is left out. When only `X (…)` exists (for example `## Deferred (P2+)` in this spec), arm 2 selects it correctly.
**Why the spec misses it:** `## Deferred (P2+)` records this pre-emption for the comma cut only; the parenthesis cut is new this round and has the same shape.
**Suggested fix:** Extend the recorded item to read "a comma-cut or parenthesis-cut exact match". No behaviour change is needed.

### F-4: The deletion gate diffs against a fixed SHA, so unrelated merges show up as findings
**Severity:** P3
**Where:** spec § Test plan (spec.md:461)
**Edge case:** `main` advances between the anchor commit and the implementation branch; the brief's Risk 2 says VHS-26 edits the same skill sections next.
**What happens:** `git diff 0158267… -- skills agents README.md docs/spec-workflow-reference.md` then includes every hunk merged since the anchor. Each removed line outside a `Current` block must be treated "as a finding until the old wording is shown to survive elsewhere". The gate becomes noisy, not wrong.
**Why the spec misses it:** The gate assumes the implementation branch is cut from the anchor commit.
**Suggested fix:** Diff against `git merge-base HEAD origin/main`, or state that the gate is run on a branch cut from the anchor.

### F-5: Ticket grounding unavailable
**Severity:** P3
**Where:** review grounding step 3
**Edge case:** `memory_search` (namespace `skills`, tags `plane_work_item` + `VHS-60`) returned HTTP 502.
**What happens:** The tracker record could not be compared with the brief; the review used the brief-only degrade path.
**Why the spec misses it:** Review-environment outage, not a spec defect.
**Suggested fix:** No spec edit; spec.md:501 and :503 already record it.

### F-6: Decision 7 no longer says which side's headings are matched
**Severity:** P4
**Where:** spec § Decision 7 — ordered boundary-aware heading matching always unions cited lines (spec.md:56)
**Edge case:** A heading renamed between the predecessor copy and the current spec.
**What happens:** Round 3 said "compare current heading text"; this round says "compare heading text and phrase". Both readings are safe: against current headings the old name misses and emits every heading, and against predecessor headings it pairs to `deleted: true` while the text diff emits the new name. An implementer still has to pick one.
**Why the spec misses it:** The word "current" was dropped when the sentence was rewritten for marker deletion.
**Suggested fix:** Restore "current" in Decision 7 and in the `:492` replacement's "Compare the phrase with heading text".

### F-7: The artifact-exception heading cites `:453` and `:506` but its first block edits `:445`
**Severity:** P4
**Where:** spec § `skills/spec-cycle/SKILL.md:453` and `:506` — artifact exception (spec.md:258-260)
**Edge case:** n/a (anchor label).
**What happens:** Nothing breaks; the block body names `:445` correctly and the quoted sentence is at that line.
**Why the spec misses it:** The lead-in edit was added this round under the existing heading.
**Suggested fix:** Leave as is, or add `:445` to the heading.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 5 | P4: 2

STATUS: GREEN
