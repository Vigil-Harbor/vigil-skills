# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Looser Tier heading rule halts every valid `## Tier` section | CLOSED | spec.md:174 — looser rule runs only when no strict `^#{1,6}\s+tier\s*$` heading matched; a second strict heading warns and is not a near-miss |
| correctness | F-2 | Malformed-brief halt runs before the re-run pin | CLOSED | spec.md:168–172, 175, 298 — pin resolves a recorded line before the brief parse can halt; Done when states the same partition |
| correctness | F-3 | A non-bare `**Tier:**` line is read as absent and becomes `big` | CLOSED | spec.md:180 — label match is case-insensitive; any other value, including a trailing note, halts and is not `big` |
| correctness | F-4 | Irreversible "re-run /ship-spec" cannot resume the worktree it just created | DEFERRED | D-1 (spec.md:320–329) is well-formed: preamble present, seven fields, blockquoted fix, two sites, `§ Decision 8` exists; Finding is P1 so the ceiling does not apply |
| correctness | F-5 | Post-cap Confirm still offers only options 1 and 3 | CLOSED | spec.md:154 — post-cap menu is options 1, 3, and 4; an invalid re-ask reprints and does not discard the interview |
| correctness | F-6 | Tweak-floor match mode and basis line are not pinned tightly enough | CLOSED | spec.md:92–113 — segment-or-filename equality, union of both instruction files, comma-separated basis grammar, four examples |
| correctness | F-7 | `round_cap` rewrite leaves literal cap-of-4 sentences in force | CLOSED | spec.md:202 names spec-cycle:672; spec.md:270 names workflow-reference :66, :27, :102; spec.md:271 names AGENTS.md:25. Those lines still carry the literal caps the table describes |
| correctness | F-8 | Ship-spec's other copies of the gate contract stay unconditional | CLOSED | spec.md:234 leaves the canonical table fingerprint-only; spec.md:241 keeps the `N/A` test skip; spec.md:256 adds the irreversible exception at ship-spec:432–433 |
| correctness | F-9 | ticket not cached | CLOSED | Not a spec defect. spec.md:314 records the brief as the record. This round's lookup failed the same way; see F-3 |
| edge-cases | F-1 | Malformed-brief halt and the re-run pin cannot both be true | CLOSED | Same partition as correctness F-2 (spec.md:168–175, 298) |
| edge-cases | F-2 | A near-miss `**Tier:**` line is read as absent `big` | CLOSED | spec.md:180 — same reader rule as correctness F-3, used by the re-run pin, attest, and ship-spec |
| edge-cases | F-3 | A clean irreversible review is specified as the failed halt | DEFERRED | D-2 (spec.md:331–340) is well-formed on the same checks as D-1; Finding is P1 |
| edge-cases | F-4 | Irreversible re-run stops on the leftover worktree | CLOSED | spec.md:249–251 names `<worktree-path>` and `<branch>` and says the halt does not resume Phase 3b by itself. The reuse clause is a new inaccuracy; see F-2 |
| edge-cases | F-5 | Failure-mode bullets still say a failed review never halts | CLOSED | spec.md:256 |
| edge-cases | F-6 | At `round_cap = 2`, FROZEN ignores the round that reviewed the revision | PARTIAL | spec.md:202 adds the current-round sentence, but the same cell still rewrites line 555's window to `1 .. round_cap−1`, and spec.md:184 still says the FROZEN test covers only that window. See F-1 |
| edge-cases | F-7 | `round_cap = 2` leaves the grill-apply rules and the grilling cap bound to the wrong 4 | CLOSED | spec.md:202–203 rewrites line 672 under `round < round_cap` and says not to re-run FROZEN; spec.md:213 keeps the grilling call's literal 3 and names it the interview cap. `skills/grilling/SKILL.md:20` defaults `round_cap` to 3, so the literal is the interview's own parameter |
| edge-cases | F-8 | Quoted multi-word surface signals do not match a "whole word" check | CLOSED | spec.md:92 phrase rule; spec.md:113 example 4 (`drop table` → `surfaces: data`) |
| edge-cases | F-9 | `small` plus `Test command: N/A` drops both gates | CLOSED | spec.md:241 — `small` does not skip Phase 3; the existing `N/A` skip (`skills/ship-spec/SKILL.md:60`, `:144`) still applies; a doc-only `small` change commits with both skipped |
| edge-cases | F-10 | A fenced `**Level:**` line in the brief becomes the tier | CLOSED | spec.md:175 — unfenced Level line only; a fenced example does not set `round_cap` |
| edge-cases | F-11 | Confirming a tier mismatch ships the absent-line tier, not the marker | CLOSED | spec.md:232–233 requires the confirm to say the gate follows the spec tier and that a marker `irreversible` is not enforced. The attest rewrite is an explicit non-fold (spec.md:313) so a pre-VHS-55 green marker with no `tier:` line is left as it is; ship-spec still classifies a disagreeing `tier:` as `changed` |
| edge-cases | F-12 | Plane ticket body was not readable | CLOSED | Not a spec defect. spec.md:314. Same access denial this round; see F-3 |
| conventions | F-1 | Irreversible reinstates a rejected VHS-46 halt and drops its review-file record | CLOSED | spec.md:60 names the VHS-46 decision and limits the supersession to `irreversible`. spec.md:244–247 writes today's skipped-form review file on the unavailable and failed halts, and no file for no command. spec.md:256 amends the failure-mode bullets |
| conventions | F-2 | Basis-line template does not generate the normative examples | CLOSED | spec.md:105–113 — three comma-separated slots, singular when the count is 1, examples are the exact strings |
| conventions | F-3 | Tweak-surfaces "then" reads as first-wins | CLOSED | spec.md:102–103 — both files are read, signals union, body runs to the next heading, and this is not the review-command order at `skills/ship-spec/SKILL.md:71–73` |
| conventions | F-4 | Workflow-reference cap and gate sentences stay literal | CLOSED | spec.md:270 lists :66, :27, :102, :84–86, :246, and :187. Those lines still contain the literal caps and the unconditional skip the edit targets |
| conventions | F-5 | A near-miss Tier heading halts; Scale's near-miss only warns | CLOSED | spec.md:174 states the halt is stricter than Scale on purpose and forbids warn-and-continue |
| conventions | F-6 | Decision 14 pins past Risk 2 | CLOSED | spec.md:86, 89, 102 label the heuristic's extra pins, including the extension substring, as spec pins beyond Risk 2 |
| conventions | F-7 | README still states a fixed 4-pass loop | CLOSED | spec.md:23 — `README.md:10` stays the big-tier maximum and is not updated. `README.md:10` still says "4 passes complete" |

Anchors rechecked against the tree that includes `b1ab82b` and `8d404d0` (2026-10-10) and `aad9971`, `156d388`, `1bd3f29` (2026-10-08). The line numbers the spec cites still point at the phrases it names, including spec-cycle:109, :330–340, :371, :397–404, :646, :672, :757, :822–824, :839; spec-brief:65, :86, :88, :105, :125; ship-spec:30–31, :60, :71–73, :107–119, :144, :183, :187–195, :432–433; spec-tickets:36, :38–44, :198; AGENTS.md:25, :27, :105, :108.

## Findings

### F-1: FROZEN window counts the final round and also excludes it
**Severity:** P0
**Where:** spec § `round_cap` substitution (spec.md:184 and spec.md:202); spec § Test plan item 3 (spec.md:282)
**Claim:** "The closed-issues manifest and the FROZEN test cover rounds `1 .. round_cap − 1`." The line-555 cell then says both: replace `rounds 1–3` with `rounds 1 .. round_cap−1`, and "a section is REWRITE when `round == round_cap` has an unresolved P0/P1 in it, and FROZEN only when neither the prior rounds nor the current round do." Test plan item 3: reading the rewritten ranges with `round_cap = 4` "matches today's ranges."
**Why this is wrong:** Today's FROZEN bullet is "no unresolved P0/P1 in this section across rounds 1–3" (`skills/spec-cycle/SKILL.md:555`) and does not include round 4. The cell tells the implementer to write that same prior-rounds window into line 555 and, in the same edit, to write a second sentence that counts round `round_cap`. At `round_cap = 2` those two sentences disagree on the only review of the revised spec: prior-rounds-only freezes a section that round 2 just failed (the edge-cases/R1/F-6 hole), and the added sentence rewrites it. At `round_cap = 4` the added sentence does not match today, so test plan item 3 is false for that bullet. Brief Decision 7 states the same prior-rounds window the summary sentence repeats. The closed-issues manifest at line 565 can stay on `1 .. round_cap−1`; the FROZEN test cannot be both windows.
**Suggested fix:** One rule, in the paragraph at spec.md:184 and in the line-555 cell. FROZEN only when neither rounds `1 .. round_cap−1` nor the current round has an unresolved P0/P1 in the section; REWRITE when the current round does. Keep the manifest on `1 .. round_cap−1`. In test plan item 3, say `round_cap = 4` matches today's revision, rewrite, and revert predicates, and that the FROZEN test now also counts the final round.

### F-2: Irreversible halt offers a worktree reuse Phase 1 does not have
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, ship-spec Phase 3b (spec.md:249–251)
**Claim:** "A re-run stops on Phase 1's existing-worktree and existing-branch checks until the operator removes them (`git worktree remove` discards the uncommitted implementation, which is not in the primary tree) or explicitly reuses that worktree."
**Why this is wrong:** The worktree-path check is a hard halt with only `git worktree remove` or rename (`skills/ship-spec/SKILL.md:108–113`). It has no reuse option. The branch check's "reuse / delete / rename" (`:119`) is reached only after that directory is gone, and it does not define reuse as continuing the dirty worktree. The uncommitted implementation is only in that worktree (`:126`). "Explicitly reuses that worktree" is not a path the operator can take. D-1 still owns in-place Phase 3b resume; this sentence should stop claiming a reuse that the checks do not offer.
**Suggested fix:** Delete "or explicitly reuses that worktree." Say the worktree-path check halts until the directory is removed or renamed, that `git worktree remove` discards the uncommitted tree, and that the branch prompt is reached only after that. Leave in-place resume to D-1.

### F-3: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Plane ticket VHS-55 is canonical where it conflicts with the brief.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-55` returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. The review used the brief. spec.md:314 already records that.
**Suggested fix:** Re-check the ticket text if a host with `skills` read access is available before ship.

### F-4: Looser Tier heading match is not stated case-insensitive
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, spec-cycle brief parse step 1 (spec.md:174)
**Claim:** The strict heading match is "case-insensitive." The looser rule is "a heading that matches `^#{1,6}\s+tier\b`" with no case flag. The same step says `## Tier list` does not match the strict pattern, and that a near-miss carrying a Level line must not be read as absent.
**Why this is wrong:** A case-sensitive `\btier\b` does not match `## Tier list` or `## Tiering`. Those are the title-case near-misses this step names. Read as absent, they become `big` with no warning, which is the downgrade the looser halt was added to prevent. Scale's near-miss regex sits in the same case-insensitive step (`skills/spec-cycle/SKILL.md:294–301`); this sentence does not.
**Suggested fix:** Say the looser pattern is case-insensitive, same as the strict match, so `## Tier list` plus an unfenced `**Level:**` line halts.

## Summary
P0: 1 | P1: 0 | P2: 2 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=0 P2=2 P3=1 P4=0
