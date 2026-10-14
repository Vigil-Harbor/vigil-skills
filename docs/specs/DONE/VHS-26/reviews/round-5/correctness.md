# Correctness Review — round 5

Mode: delta. Spec read fresh from `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-26.spec.md`; it is byte-identical to `round-5/spec.copy.md`. Nothing under `VHS-26.attempt-1/` was read.

## Closure of round 4 findings

The closure manifest is empty (round 4 closed green with no P0/P1), so the ledger check has nothing to require. The table tracks the round-4 P2/P3 findings that this revision folded.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P2) | Omission boundary narrows brief Decision 7's third trigger | CLOSED | spec § Decisions, spec.md:34 records the narrowing; § Decision 8 spec.md:143 states both undetected cases |
| correctness | F-2 (P2) | Missing-file closure pinned for correctness only | CLOSED | spec.md:110 puts the `round-<C+1>` path in the phrase; spec.md:179 says the other lenses verify from that path |
| correctness | F-3 (P2) | Grading order ambiguous for a dead anchor only in the row | CLOSED (new variant: F-1 below) | spec.md:134 rule 1 and spec.md:137 last sentence; Test plan spec.md:199 |
| correctness | F-4 (P3) | ticket not cached | not a spec item | recurs as F-4 below |
| correctness | F-5 (P3) | Phase 1 rows dropped after a failed first write; preamble count nit | CLOSED | spec.md:110 says the drop is intended; Test plan spec.md:201; preamble is now a list, spec.md:26-32 |
| edge-cases | F-1 (P2) | Omission P2 tagged `Pre-ship recommended` | CLOSED | spec.md:140 "Do not tag it"; spec.md:112 green-round sentence, which matches 2g steps 2 and 4 (`skills/spec-cycle/SKILL.md:955-969`) |
| edge-cases | F-2 (P2) | Other lenses have no rule to close `ground-truth ledger missing` | CLOSED | spec.md:110, spec.md:179 |
| edge-cases | F-3 (P3) | "opens code anchors, not spec sections" stale | CLOSED | spec.md:128 carries the suggested sentence |
| edge-cases | F-4 (P3) | Three row and closure states ungraded | CLOSED | spec.md:134 (no sentence, no anchor); spec.md:141 (second failed write counted once); Test plan spec.md:199, :201 |
| edge-cases | F-5 (P3) | No-claims line on a new spec passes every check | CLOSED | spec.md:143 second stated limit |
| edge-cases | F-6 (P3) | Ticket lookup blocked | not a spec item | — |
| conventions | F-1 (P2) | Omission finding tagged `Pre-ship recommended` | CLOSED | spec.md:140, spec.md:112 |
| conventions | F-2 (P2) | Missing-file disposition carries no verifiable anchor | CLOSED | spec.md:110 |
| conventions | F-3 (P2) | Preamble says Decision 8 "carries" brief Decision 7 but narrows it | CLOSED | spec.md:34 |
| conventions | F-4 (P3) | Spec-level additions for the human drift check | CLOSED | spec.md:26-32 |

**Deleted headings.** All four entries of the removed `## Deferred (P2+)` are folded as shown above, so the removal drops nothing live. The removed `## Post-green polish` held one line describing a rewording that this revision supersedes. Its absence means 2g will not treat itself as already-run (`skills/spec-cycle/SKILL.md:945-947`), which is the right behaviour for a fresh green round.

**Deferred-findings block.** The section appears once and its preamble carries the required sentence. D-1 is well-formed: seven fields, blockquoted fix, three existing propagation sites. Its stated `out-of-scope` token keeps it under the ceiling. No routing violation.

**Anchors in the changed regions.** All resolve at the cited lines after today's commits `fad52c7` and `f64bebe`:
- `skills/spec-cycle/SKILL.md` :390, :558, :578-579, :711-718, :715
- `agents/spec-reviewer-correctness.md` :86, :88, :109

Unchanged-section anchors :450, :454, :460, :462, :594-601, :698 and :757 also still resolve.

## Findings

### F-1: "Apply the first rule that matches" puts the unsupported-anchor P1 ahead of the Anchor drift rule
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Grading a checked row (spec.md:133-139)
**Claim:** "Apply the first rule that matches: … 3. The anchor does not support the claim as the spec states it: file a P1, `runtime claim not supported by its anchor` … 4. The file or symbol of the spec sentence's own anchor is gone: the agent's existing Anchor drift rule grades it …, P1 per dead citation, and a line that only moved joins that rule's one combined P4."
**Why this is wrong:** Under a literal first-match reading, rule 4 is unreachable. A citation whose file is gone, or whose line moved, also "does not support the claim as the spec states it", so rule 3 matches first. For a moved line that yields a blocking P1 where the agent's Anchor drift rule says "do not file a P1" (`agents/spec-reviewer-correctness.md:109`), and where the Test plan row at spec.md:199 lists "a line that moved" as its own case. The trailing "one defect is one finding" paragraph (spec.md:139) rescues this when Anchor drift has already filed the citation, which is why this is not blocking. The numbered order and the stated intent still disagree. Round 4's unordered prose did not have this problem; the first-match framing added to close round-4 F-3 introduced it.
**Suggested fix:** Swap rules 3 and 4, or scope rule 3: "The anchor's file and symbol resolve, at the cited line or a moved one, and the live code does not support the claim as the spec states it." Add the expected outcome for "a line that moved" (combined P4, no P1) to the Test plan row at spec.md:199.

### F-2: The preamble lists Decision 6's phrase as an addition while § Apply-findings changes says step 6 adds no manifest vocabulary
**Severity:** P3
**Where:** spec § Decisions (spec.md:31); spec § Decision 6 step 6 (spec.md:108-110), against the unchanged § Apply-findings changes (spec.md:171)
**Claim:** "Decision 6: the literal disposition phrase for a missing ground-truth ledger" (an author addition) and "no new section-naming disposition form", against "Step 6 adds no manifest vocabulary."
**Why this is wrong:** The revision deliberately weakened "no new disposition form" to "no new section-naming disposition form" and now pins a literal, path-bearing `fixed:` phrase. The unchanged sentence at spec.md:171 still says no vocabulary is added. A careful reader resolves it: the `fixed:` forms at `skills/spec-cycle/SKILL.md:594-601` are not edited and the recount ignores a phrase with no `§`. The two sentences no longer say the same thing.
**Suggested fix:** Change spec.md:171 to "Step 6 adds one process phrase and no section-naming form; the `fixed:` forms listed at … are not extended".

### F-3: The illustrative ground-truth-ledger block does not show the new-spec line
**Severity:** P3
**Where:** spec § Decision 4 (spec.md:62-69, against :75)
**Claim:** The block shows the title followed directly by a row; the prose says the new-spec line sits "directly under its title".
**Why this is wrong:** Not a contradiction, since the line is conditional. But the skill is told to show "this illustrative shape", and implementers copy blocks. The omission boundary of Decision 8 depends on that one line being present and recognisable.
**Suggested fix:** Add a commented optional line to the block, or one sentence after it: "On a new spec's first dispatch the line `New spec: rows cover every section.` sits between the title and the first row."

### F-4: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** The spec is authored from the VHS-26 brief and ticket.
**Why this is wrong:** `memory_search` on namespace `skills` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The brief says the ticket states no acceptance criteria (brief.md:45), so the brief's Done-when list was used as canonical. All six brief Done-when items still map to spec Done-when items 1-6.
**Suggested fix:** None to the spec.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 0

STATUS: GREEN
