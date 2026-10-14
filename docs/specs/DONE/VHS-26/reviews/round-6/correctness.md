# Correctness Review — round 6

Delta pass over the eight named headings, diffed against `docs/specs/TODO/VHS-26.reviews/round-5/spec.copy.md`. Nothing blocks: the round-5 grading-order fold landed correctly and every code anchor in the changed regions still resolves at its cited line.

## Closure of round 5 findings

N/A — no closure predecessor. The manifest is empty because round 5 closed green.

- **Ledger check:** the three round-5 reports (`correctness.md`, `edge-cases.md`, `conventions.md`) hold no P0 or P1 finding, so no manifest line is required. All three have a parseable `STATUS: GREEN` line.
- **Round-5 P2 (correctness F-1 / edge-cases F-1, grading order):** folded. Decision 8's list now runs `Anchor: none`, unreadable out-of-root anchor (P3), row-only defects and a missing sentence anchor (P2), Anchor drift, then the unsupported-claim P1. That is the order the deleted `## Deferred (P2+)` entry asked for.
- **Deleted `## Deferred (P2+)`:** its only entry was that fold, so the removal drops nothing. This matches the 2g rule at `skills/spec-cycle/SKILL.md:968`.

**Deferred-findings block:** clean.
- `## Deferred — follow-up required` appears once.
- The preamble blockquote carries the required sentence.
- D-1 is well-formed: all seven fields are present, the `Suggested fix` is blockquoted with one blank line before `Propagation sites`, and its three sites all exist.
- D-1 is P1 with a stated `out-of-scope` token, so the ceiling does not apply and there is no routing violation.

**Anchors verified in the changed regions (all resolve, none moved):**
- `skills/spec-cycle/SKILL.md`: `:390`, `:450`, `:454`, `:460`, `:462`, `:558`, `:578-579`, `:594-601`, `:698`, `:711-718` (`:715` is "one site or none"), `:757`, and the 2g carry-forward at `:955-969`.
- `agents/spec-reviewer-correctness.md`: `:86` (Ledger check), `:88` (cannot-complete sentence), `:90` (`# Delta scope`), `:109` (Anchor drift).
- `agents/spec-reviewer-conventions.md:103`, `docs/spec-workflow-reference.md:43`, `README.md:10`, `AGENTS.md:27`, `:43`, `:110`.

**Git history:** the touched files carry commits from 2026-10-11 to 2026-10-13 (`fad52c7`, `f64bebe`, `d3730b1`, `7abe102`, `5f640d0`). All precede the brief's grounding commit `fc20f94`, and the anchors match the current files, so the spec is not planning around shifted code.

## Findings

### F-1: The delta-pass permission for the row sample sits outside the quoted block text, and the filing sentence is broader than the findings it can cover
**Severity:** P3
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (spec.md:128, spec.md:140)
**Claim:** "It runs on every pass, full or delta. Its row sample reads the anchors and the spec sentences the rows name; this is a grounding check, so the sample is not limited by `changed_regions`. The block says:" and, inside the block, "A finding this block produces is filed against the section the row names, on a full or a delta pass."
**Why this is wrong:**
- The first two sentences come before "The block says:", so they describe the block rather than form part of it. An implementer who copies only the bullets ships an agent whose sole delta statement is the last sentence of the grading bullet.
- The unedited `# Delta scope` block (`agents/spec-reviewer-correctness.md:90`) lists the checks that are "not limited to `changed_regions`" and then says "Do not explore any other region". The ground-truth check is not in that list, so the explicit permission needs to be in the agent text.
- "A finding this block produces" is filed "against the section the row names", but four of the block's findings have no single row: the no-path P3, the missing-file P0, the combined out-of-root P3, and the omission P2 (which on a new spec can land in a section with no row).
- A careful reader resolves both points, so this is not blocking.
**Suggested fix:** Move "It runs on every pass, full or delta" and "the sample is not limited by `changed_regions`" into the block's quoted text, for example as the opening sentence of the **Sample** bullet. Narrow spec.md:140 to "A finding a checked row produces is filed against the section that row names, on a full or a delta pass."

### F-2: Two wording nits in the changed text
**Severity:** P4
**Where:** spec § Decision 8 (spec.md:132-135); spec § Decision 4 (spec.md:71)
**Claim:** (a) "For each checked row, open the anchor fresh and read the spec sentence the row names." (b) "On a new spec's first dispatch, the line `New spec: rows cover every section.` sits between the title and the first row."
**Why this is wrong:**
- (a) Grading rule 1 says "do not open anything" for an `Anchor: none` row, and rule 2 covers an anchor the host cannot read, so the Sample bullet's unconditional "open the anchor" is narrowed two lines later.
- (b) A new spec with no runtime-behavior claims has no first row; spec.md:79 says it carries the new-spec line and the no-claims line. Spec.md:75 ("directly under its title") is the accurate placement.
**Suggested fix:** (a) "For each checked row, read the spec sentence the row names and, where the grading rules call for it, open the anchor fresh." (b) Replace "between the title and the first row" with "directly under the title".

### F-3: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** n/a
**Why this is wrong:** `memory_search` with namespace `skills` and tags `["plane_work_item", "VHS-26"]` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The review used the brief, which records that the ticket has no acceptance-criteria section (brief.md:45).
**Suggested fix:** None for the spec. Grant read on the namespace if ticket-canonical review is wanted.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 1

STATUS: GREEN
