# Edge-Cases Review — round 3

## Closure of round 2 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | FROZEN window counts the final round and also excludes it | CLOSED | spec.md:184, the line-555 cell at spec.md:202, and test plan item 3 at spec.md:282 name one window, `1 .. round_cap−1`, and say the FROZEN test does not count `round == round_cap`. The prior "also count the current round" sentence is gone. That matches brief Decision 7; it is a deliberate drop of the extra sentence, not a second window. |
| correctness | F-2 | Irreversible halt offers a worktree reuse Phase 1 does not have | CLOSED | spec.md:249–251: path check halts until the directory is removed or renamed; `git worktree remove` discards the uncommitted tree; the branch prompt is reached only after that; the halt does not resume Phase 3b. The reuse clause is gone. In-place resume stays D-1. |
| correctness | F-3 | ticket not cached | CLOSED | spec.md:314 still records the brief as the source. This round's `memory_search` on namespace `skills` was access denied again; see F-3 below. Not a spec defect. |
| correctness | F-4 | Looser Tier heading match is not stated case-insensitive | CLOSED | spec.md:174: the looser `^#{1,6}\s+tier\b` match is case-insensitive, the same flag as the strict match. |
| edge-cases | F-1 | A brief `**Level:**` line with trailing text is accepted as its first token | CLOSED | spec.md:175: the value is the whole remainder after the label, trimmed and lowercased, and must be exactly `small`, `big`, or `irreversible`. A trailing note or stuck punctuation halts. The label must start the line. A fenced line does not count. |
| edge-cases | F-2 | Any integer in the ticket overrides the 1-line estimate | CLOSED | spec.md:89: only a number tied to a line count or a diff size qualifies; a range uses its top; several qualifying numbers use the greatest; a ticket id, date, file count, or item number does not qualify. |
| edge-cases | F-3 | A bulleted `## Tweak surfaces` line never blocks `tweak` | CLOSED | spec.md:103: strip one leading `-`, `*`, or `N.` marker, ignore a line empty after that, and treat any other remaining line as an unknown surface that recommends `big`. |
| edge-cases | F-4 | The irreversible halt offers a worktree reuse Phase 1 does not have | CLOSED | Same text as correctness F-2, spec.md:249–251. |
| edge-cases | F-5 | Wiki grounding paths make the normative tweak recommendation unreachable | CLOSED | spec.md:88: count paths the change names; a wiki `state.md` or `filemap.md` that grounding opened does not count. spec.md:109: example 1 still recommends `tweak` when those reads are present and the change names only `README.md`. |
| edge-cases | F-6 | Plane ticket body was not readable | CLOSED | spec.md:314. The finding asked for no spec change. Lookup failed the same way this round; see F-3. |
| conventions | F-1 | Workflow reference still puts the seed gate inside the interview `--no-grill` skips | CLOSED | spec.md:270 names `:11`, `:17`, and `:21`: the seed gate runs before the tier gate in every mode, and Phase 4 names `## Tier` on every brief it writes. |
| conventions | F-2 | customizing.md still says a skipped review never blocks, with no leave-alone note | CLOSED | spec.md:24: `docs/customizing.md:40` stays today's skip for `big` and an absent tier and is not updated for the irreversible halt. |

D-1 and D-2 are still well-formed. The preamble is the blockquote under `## Deferred — follow-up required` and contains `must not implement anything in this section`. Each row has all seven fields, a blockquoted suggested fix, one blank line before `**Propagation sites:**`, and two sites that name sections in the spec. Both findings are P1, so the in-scope-P0 ceiling does not apply. Their roots are not re-filed.

## Findings

### F-1: A present `## Tier` section with no Level line is not a halt
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, spec-cycle brief parse step 2 (spec.md:175); Decision 9 (spec.md:64); Decision 12 (spec.md:76)
**Edge case:** The brief has a strict `## Tier` heading and no unfenced `**Level:**` line. The body is empty, is only sibling lines (the shape Decision 12 reserves for VHS-54), or its only `**Level:**` line is inside a fence. Same shape when an unclosed fence above that line swallows it.
**What happens:** Step 1 sets `tier = big` only when no strict heading matched. Step 2 halts only when a Level line exists and its value is empty, `tweak`, unknown, or a trailing note. Step 2 also says a fenced line does not count and does not set `round_cap`. Step 3 ignores siblings. No sentence assigns `tier` or halts when the count of Level lines is zero. The only nearby "no Level line" rule is for a looser heading, and that rule ignores the heading, which is the absence path (`big`, no warning). A section that was meant to be `irreversible`, with the value lost or left in a fence, is then read as `big`: `round_cap` stays 4 and ship-spec keeps the skippable review gate. Decision 9 and Decision 12 say a present section whose value is missing halts and does not become `big`.
**Why the spec misses it:** The halt text is written for a bad value on a line (`tier: malformed (<line>)`). A missing line has no `<line>`, so it was not given a branch. Test plan item 6 covers a present `tweak`, unknown, or empty value, not a present section with no Level line.
**Suggested fix:** In step 2, if the strict section contains no unfenced Level line, halt `tier: malformed (## Tier has no Level line) — halting`, write no marker, and do not treat the section as absence. Keep the looser-heading "no Level line → ignore" rule as it is. Add that case to test plan item 6.

### F-2: A malformed tweak-surface line recommends `big` with no basis slot
**Severity:** P3
**Where:** spec § Decision 14, Extension and Basis line (spec.md:103–105)
**Edge case:** `AGENTS.md` has `## Tweak surfaces` and a non-blank line that is neither one word nor a quoted phrase after the list-marker strip, such as a prose intro (`Extra surfaces for this repo.`) or a task-list line the strip does not fully remove (`[ ] payments`).
**What happens:** The recommendation is `big`, including for the example-1 typo, but the surfaces slot is only defined as `none`, `unknown`, or a matched name. Nothing says which of those to print, or that the bad line is named. The basis can read `surfaces: none — never tweak`, which the suffix rule cannot explain. Checklist item 1 does not cover this line.
**Why the spec misses it:** Round 2 required the unknown line to recommend `big` so a bullet would not match nothing. That sentence never maps the line onto the three-slot basis.
**Suggested fix:** For that line, print `surfaces: unknown` and the `never tweak` suffix, and include a short quote of the line. Do not leave the slot as `none`.

### F-3: Plane ticket body was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` for tags `plane_work_item` and `VHS-55`, namespace `skills`, `source_system: plane`.
**What happens:** The server returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. The review used the brief. No ticket body was checked for decisions the brief might have dropped.
**Why the spec misses it:** Not a spec defect. spec.md:314 already records the brief as the source.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read namespace `skills` if a later round needs the ticket body.

Persistence for the new `## Tier` section, the `**Tier:**` line, and the marker `tier:` field: the brief stays temp-and-rename; the marker stays a whole-file replace of a single token; a missing `tier:` line is defined as not a disagreement; a missing spec line is `big`; retry replaces the same marker; concurrent writers stay outside the supported flow. No persistence finding.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 1

STATUS: GREEN
