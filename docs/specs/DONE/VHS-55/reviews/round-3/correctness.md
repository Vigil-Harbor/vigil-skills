# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | FROZEN window counts the final round and also excludes it | CLOSED | spec.md:184 and the line-555 cell at spec.md:202 state one window, `1 .. round_cap−1`, and say not to count `round == round_cap`. Test plan item 3 (spec.md:282) matches that window and today's predicates at `round_cap = 4`. The extra "count the current round" sentence was not adopted; brief Decision 7 requires this window. |
| correctness | F-2 | Irreversible halt offers a worktree reuse Phase 1 does not have | CLOSED | spec.md:249–251 no longer says "explicitly reuses that worktree." Path check is remove or rename (`skills/ship-spec/SKILL.md:108–112`); the branch prompt is only the next check (`:119`). In-place resume stays D-1. |
| correctness | F-3 | ticket not cached | CLOSED | spec.md:314 still records the brief as the source. This round's lookup failed the same way; see F-4. |
| correctness | F-4 | Looser Tier heading match is not stated case-insensitive | CLOSED | spec.md:174: the looser rule is case-insensitive, the same flag as the strict match. |
| edge-cases | F-1 | A brief `**Level:**` line with trailing text is accepted as its first token | CLOSED | spec.md:175: the value is the trimmed remainder and must be exactly `small`, `big`, or `irreversible`; a trailing note halts. A mid-line mention does not count. The spec reader at spec.md:180 uses the same rule. |
| edge-cases | F-2 | Any integer in the ticket overrides the 1-line estimate | CLOSED | spec.md:89: only a number tied to a line count or a diff size qualifies; a range uses its top; several use the greatest; a ticket id, date, file count, or item number does not. |
| edge-cases | F-3 | A bulleted `## Tweak surfaces` line never blocks `tweak` | CLOSED | spec.md:103: strip one list marker, ignore a line empty after that, and any other remaining line is an unknown surface that recommends `big`. |
| edge-cases | F-4 | The irreversible halt offers a worktree reuse Phase 1 does not have | CLOSED | Same text as correctness F-2, spec.md:249–251. |
| edge-cases | F-5 | Wiki grounding paths make the normative tweak recommendation unreachable | CLOSED | spec.md:88: wiki `state.md` / `filemap.md` reads do not count, and example 1 still recommends `tweak` when only `README.md` is named. |
| edge-cases | F-6 | Plane ticket body was not readable | CLOSED | spec.md:314. Not a spec defect. Same access denial this round; see F-4. |
| conventions | F-1 | Workflow reference still puts the seed gate inside the interview `--no-grill` skips | CLOSED | spec.md:270 names `:11`, `:17`, and `:21`. Those lines still say what the edit targets (`docs/spec-workflow-reference.md:11`, `:17`, `:21`). |
| conventions | F-2 | customizing.md still says a skipped review never blocks, with no leave-alone note | CLOSED | spec.md:25: `docs/customizing.md:40` stays today's skip for `big` and an absent tier. That line still says a failed or unavailable command is skipped and never blocks the commit. |

Anchors rechecked against the tree through `b1ab82b` and `8d404d0` (2026-10-10). The lines the spec cites still hold the phrases it names, including spec-brief `:65`, `:86`, `:88`, `:105`, `:125`; spec-cycle `:36`, `:109`, `:330–340`, `:369`, `:371`, `:495`, `:507`, `:548–555`, `:565`, `:646`, `:672`, `:757`, `:822–824`, `:839`; ship-spec `:30–31`, `:60`, `:71–73`, `:108–119`, `:144`, `:183`, `:187–195`, `:432–433`; spec-tickets `:34–36`, `:38–44`, `:198`; AGENTS.md `:25`, `:27`, `:105`, `:108`; README.md `:10`. D-1 and D-2 remain well-formed P1 rows (preamble present, seven fields, blockquoted fixes, two sites, ceiling does not apply). Their roots were not re-filed.

## Findings

### F-1: A present `## Tier` section with no Level line has no halt in the parse steps
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, spec-cycle brief parse step 2 (spec.md:175); contrast spec § Decision 9 (spec.md:64) and § Decision 12 (spec.md:76)
**Claim:** "Any other value, including empty, `tweak`, a trailing note, or punctuation stuck to the token, halts." Step 3: "Sibling lines in the section are ignored." Decision 9: "A present section or line whose value is missing, unknown, or `tweak` halts. It does not become `big`."
**Why this is wrong:** The halt is specified for a Level line whose value is empty or not one of the three tokens. It is not specified for a strict `## Tier` section that has no unfenced Level line at all — only sibling lines, or only a fenced `**Level:**` example, which step 2 says does not count. Step 1 sets `tier = big` only when no strict heading matched. An implementer following the numbered steps can leave that section unset or fall through to `big`, which brief Decision 12 forbids for a missing value on a present section. The spec reader does not have this hole: absence there is "no label line at all," and an empty `**Tier:**` line halts (spec.md:180).
**Suggested fix:** In step 2, if the strict section contains no unfenced Level line, halt `tier: malformed (no Level line) — halting`. Do not treat it as absence.

### F-2: The irreversible halt says `git worktree remove` discards a dirty tree
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, ship-spec Phase 3b (spec.md:251)
**Claim:** "`git worktree remove` discards the uncommitted implementation, which is not in the primary tree."
**Why this is wrong:** Phase 1's path check tells the operator to `git worktree remove` or rename, and mentions `--force` only "if it's broken" (`skills/ship-spec/SKILL.md:108–112`). Default `git worktree remove` refuses an unclean worktree; only `--force` deletes it. The implementation is only in that worktree (`skills/ship-spec/SKILL.md:126–132`), so the warning is aimed at the right tree, but the command named does not discard it. D-1 still owns in-place resume; this sentence should not overstate the command that refuses.
**Suggested fix:** Say `git worktree remove` refuses a dirty worktree, and `git worktree remove --force` discards the uncommitted tree that is not in the primary checkout. Leave resume on D-1.

### F-3: The workflow reference still says an `N/A` test command runs the review gate
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Docs and AGENTS.md (spec.md:270); `docs/spec-workflow-reference.md:187`
**Claim:** At `:187`, "`irreversible` halts on the three skip cases and does not commit; `big` and an absent tier keep the skip."
**Why this is wrong:** That paragraph ends with "With an `N/A` test command the gate still runs, and there is no test re-run" (`docs/spec-workflow-reference.md:187`). The `:187` edit does not touch that clause. For `small`, Phase 3b is skipped before the three skip cases, including when the test command is `N/A` (spec.md:241). After the edit as written, the reference would still say the gate runs for every `N/A` change.
**Suggested fix:** In the `:187` sentence, say the review gate still runs for `big`, `irreversible`, and an absent tier when the test command is `N/A`, and that `small` skips it.

### F-4: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Plane ticket VHS-55 is canonical where it conflicts with the brief.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-55` returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. The review used the brief. spec.md:314 already records that.
**Suggested fix:** Re-check the ticket text if a host with `skills` read access is available before ship.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
