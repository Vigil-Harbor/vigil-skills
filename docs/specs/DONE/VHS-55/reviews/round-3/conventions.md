# Conventions Review — round 3

## Closure of round 2 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | FROZEN window counts the final round and also excludes it | CLOSED | spec.md:184, the line-555 cell at spec.md:202, and test plan item 3 at spec.md:282 state one window, `1 .. round_cap−1`, and say that window is the only FROZEN window. Brief Decision 7 is that same window. The manifest's `fixed` holds. |
| correctness | F-2 | Irreversible halt offers a worktree reuse Phase 1 does not have | CLOSED | spec.md:249–251: the path check holds until the directory is removed or renamed; `git worktree remove` discards the uncommitted tree; the branch prompt is reached only after the directory is gone; the halt does not resume Phase 3b. In-place resume stays D-1. |
| correctness | F-3 | ticket not cached | CLOSED | spec.md:314 records the brief as the record. This round's `memory_search` on namespace `skills` returned access denied again. |
| correctness | F-4 | Looser Tier heading match is not stated case-insensitive | CLOSED | spec.md:174: the looser rule is case-insensitive, the same flag as the strict match. |
| edge-cases | F-1 | A brief `**Level:**` line with trailing text is accepted as its first token | CLOSED | spec.md:175: the value is the remainder of the line; a trailing note or stuck punctuation halts; the label must start the line. |
| edge-cases | F-2 | Any integer in the ticket overrides the 1-line estimate | CLOSED | spec.md:89: only a number tied to a line count or a diff size qualifies; several qualifying numbers use the greatest; a ticket id, date, file count, or item number does not qualify. |
| edge-cases | F-3 | A bulleted `## Tweak surfaces` line never blocks `tweak` | CLOSED | spec.md:102–103: strip one leading `-`, `*`, or `N.`, ignore a line empty after that, and any other remaining line recommends `big`. |
| edge-cases | F-4 | The irreversible halt offers a worktree reuse Phase 1 does not have | CLOSED | Same halt text as correctness F-2, spec.md:249–251. |
| edge-cases | F-5 | Wiki grounding paths make the normative tweak recommendation unreachable | CLOSED | spec.md:88: wiki `state.md` and `filemap.md` grounding reads do not count. Example 1 at spec.md:109 still recommends `tweak` when those reads are present and the change names only `README.md`. |
| edge-cases | F-6 | Plane ticket body was not readable | CLOSED | spec.md:314. The finding asked for no spec change. This round's lookup was access denied again. |
| conventions | F-1 | Workflow reference still puts the seed gate inside the interview `--no-grill` skips | CLOSED | spec.md:270 names `:11`, `:17`, and `:21`: the seed gate runs before the tier gate in every mode, including `--no-grill`, and Phase 4 names `## Tier` on every brief it writes. |
| conventions | F-2 | customizing.md still says a skipped review never blocks, with no leave-alone note | CLOSED | spec.md:25: `docs/customizing.md:40` stays today's skip for `big` and an absent tier and is not updated for the irreversible halt. |

## Findings

No findings.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 0 | P4: 0

STATUS: GREEN
