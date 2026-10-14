# Correctness Review — round 4

Grounding notes: review_mode `delta`. Spec, brief, the `changed_regions` file and `round-3/ledger.md` (the closure manifest) were read fresh from disk, along with the three round-3 reviewer reports (`synthesis.md` not read; nothing under `VHS-26.attempt-1/` read). The Plane ticket lookup was denied (`Access denied: agent 'claude' lacks 'read' on namespace 'skills'`), so the review proceeded from the brief (F-4).

Anchors: every `file:line` citation inside the changed and open-finding regions resolves to the named symbol at the cited line in the live tree (HEAD `fc20f94`, equal to `round-4/baseline.commit`): `skills/spec-cycle/SKILL.md:390`, `:444-458`, `:450`, `:454`, `:460`, `:462`, `:558`, `:578-579`, `:594-601`, `:698`, `:711-718`, `:715`, `:757`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`. No dead or moved citations. `grep -c "ledger NOT written:"` over the skill currently returns 1, and the proposed `ground-truth-ledger.md NOT written:` string does not contain it, as the Test plan assumes.

Git history: the touched files changed in the last 7 days (`fad52c7` and `f64bebe` on 2026-10-13, `d3730b1` on 2026-10-12). The spec's anchors already reflect that code.

Deferred-findings block: one section, preamble present with the required sentence. Row D-1 is well-formed (seven fields, blockquoted fix with one blank line before `Propagation sites`, three sites that all exist under their current headings). Its `Scope` token is `out-of-scope`, so the ceiling does not apply. No routing violation. D-1's root (post-green polish grounding) is not re-filed.

## Closure of round 3 findings

Ledger check: the manifest carries one line each for `correctness/F-1 (P0)`, `correctness/F-2 (P1)`, `edge-cases/F-1 (P0)` and `edge-cases/F-2 (P1)`, with the severity directly after the id. Round-3 conventions filed no P0/P1. Nothing is missing.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Delta pass 1 after a red halt carries a closure manifest, so the omission boundary is not empty on a re-run | CLOSED | Deliberate direction change. Decision 8 Omission bullet (spec.md:124): boundary is "the set of sections the rows themselves name"; "A file with no rows has no boundary"; "do not derive edited sections from the closure manifest". Decision 4 third bullet (spec.md:67) gives delta pass 1 the no-claims line. Test plan (spec.md:184) now matches. All six manifest sites carry the change. |
| correctness | F-2 (P1) | An evidence-only ground-truth fix puts a section in the omission boundary with rows for only the named claims | CLOSED | Deliberate direction change. Decision 6 step 6 (spec.md:98-102) removes the carried-rows disposition; an unsupported claim is an ordinary fold with `fixed: edited § <section>` and step 5 supplies the whole section's rows; omission is P2. All five manifest sites carry the change. |
| correctness | F-3 (P3) | Decisions preamble does not mark the author-pinned choices | CLOSED | spec.md:24 names Risks items 2, 3 and 5 and the author additions (see F-5 for a count nit). |
| correctness | F-4 (P3) | ticket not cached | PARTIAL | Host condition; lookup denied again. Re-filed as F-4. No spec defect. |
| correctness | F-5 (P4) | unittest pattern quoted two ways | CLOSED | spec.md:197 and spec.md:209 both use `"test_*.py"`. |
| edge-cases | F-1 (P0) | Delta pass 1 after a red halt has a closure manifest, so the omission boundary fires | CLOSED | Same root and evidence as correctness F-1. |
| edge-cases | F-2 (P1) | An evidence-only fix carries rows for the named claims only — the loop cannot close | CLOSED | Same root and evidence as correctness F-2. The alternating-finding path no longer exists: no blocking finding is fixed by rows alone. |
| edge-cases | F-3 (P2) | Final-pass ground-truth finding gets a `fixed:` disposition for rows never written | CLOSED | spec.md:100: the phrase is the same on the final pass; spec.md:125: closure is the file existing with content, including the no-claims line. |
| edge-cases | F-4 (P2) | "Section" defined differently for author and reviewer | CLOSED | spec.md:61, spec.md:97 and spec.md:124 all use the innermost heading's own body. |
| edge-cases | F-5 (P2) | Closure rule cannot be met when the fix removes the claim | CLOSED | spec.md:125 verifies against the current spec; Test plan spec.md:185 adds the deletion case. |
| edge-cases | F-6 (P3) | Held rows have no durable home | CLOSED | spec.md:71 adds the rebuild rule and names the interrupted-before-first-dispatch gap. |
| edge-cases | F-7 (P3) | Five-row cap conflicts with predecessor-named rows | CLOSED | The predecessor-rows clause is removed from the Sample bullet (spec.md:122). |
| edge-cases | F-8 (P3) | Ticket lookup blocked | PARTIAL | Same as correctness F-4. |
| conventions | F-1 (P2) | New `fixed: ground-truth rows carried` disposition not reconciled | PARTIAL | Items 1 and 2 are closed: the form is removed, and spec.md:155 states the vocabulary and recount paragraphs are not edited. Item 3 (how a lens without the path closes a no-site finding) is asserted at spec.md:163 but not pinned; see F-2. Stays P2. |
| conventions | F-2 (P2) | `Anchor: none` relaxes brief Decision 1 unlabelled | CLOSED | spec.md:40 labels both rules as a spec-level addition; spec.md:123 extends the grading to any file the host can read. |
| conventions | F-3 (P2) | Bare word "ledger" in Decision 3 | CLOSED | spec.md:40 and spec.md:42 now say "ground-truth-ledger row" / "ground-truth ledger". |
| conventions | F-4 (P3) | Spec-level additions for the drift check | CLOSED | spec.md:24. Residual gap filed as F-1 below. |

## Findings

### F-1: The row-named omission boundary narrows brief Decision 7's third trigger, and a new spec whose ground-truth ledger holds only the no-claims line draws no ground-truth finding
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Omission bullet and "stated limit" paragraph, spec.md:124, spec.md:127); spec § Decisions (spec.md:22, spec.md:24)
**Claim:** "The boundary is the set of sections the rows themselves name ... A file with no rows has no boundary and draws no omission finding." Preamble: "Decision 8 carries brief Decision 7"; "Three rules are the spec author's additions".
**Why this is wrong:** Brief Decision 7 (brief.md:40) says the correctness agent files a finding "when its own normal read of the spec finds a runtime-behavior claim with no row", and adds "This spot-check is the only enforcement in this ticket." Round 3's spec met that for a new spec through the new-spec line (boundary = every section). This revision removed that line to close F-1, although only the closure-manifest branch was at fault. The result:
- On a Phase-1-authored spec, a section with runtime claims and no rows at all draws no finding.
- A new spec whose author writes the no-claims line passes the whole ground-truth check: not missing, nothing to sample, no boundary. The reviewer cannot tell that file from a legitimate re-run file.

Decision 8 states the limit for "a section the author edited", with the reason that the reviewer "has no list of edited sections". That reason does not apply to a new spec, where every section is covered and no list is needed. The preamble does not record the change as a narrowing of brief Decision 7, so the human drift check cannot see it.

Rated P2 rather than P1 because the brief leaves severities to the spec author (Risks item 3), fences out computed coverage and backfill, the limit is partly disclosed, and the reviewer's existing step 5 still verifies claims about current code.
**Suggested fix:** Either of:
- (a) Restore the author-stated first-dispatch line for a Phase-1-authored spec (`New spec: rows cover every section.`) and make the boundary "every section when that line is present; otherwise the sections the rows name". No manifest is read, so round-3 F-1 stays closed. The omission can stay P2.
- (b) Keep the design and add one sentence to spec.md:24 and spec.md:127: this narrows brief Decision 7's third trigger; a new spec with whole sections unrowed, or with only the no-claims line, is not detected until VHS-61.

### F-2: Closing `ground-truth ledger missing` is pinned for the correctness agent only, but the spec says every lens can already apply it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Correctness reviewer changes (spec.md:163); spec § Decision 6 step 6 (spec.md:100); spec § Decision 8 Closure bullet (spec.md:125)
**Claim:** "Each blocking finding closes by a rule every lens can already apply: ... a missing file is fixed by the file existing."
**Why this is wrong:** The edge-cases and conventions agents verify each predecessor finding "against the current spec" (`agents/spec-reviewer-edge-cases.md:57`). They receive no `ground_truth_ledger_path` and are not edited. The disposition `fixed: ground-truth ledger to be written at the next dispatch` names no spec section, and `skills/spec-cycle/SKILL.md:586-590` (left unchanged) says a disposition is "always with a spec § anchor the reviewer can verify". The closure rule that makes the finding CLOSED lives only in the correctness agent's new block. A second lens that finds nothing to verify may mark it PARTIAL or REOPENED, and REOPENED is P0. The missing-STATUS precedent the spec cites (`SKILL.md:578-579`) is a synthetic line with no reviewer finding behind it, so it does not establish how the other lenses close a real one. This is the unresolved third item of round-3 conventions F-1.
**Suggested fix:** Make the phrase self-verifying without touching the fenced agents, for example `fixed: ground-truth ledger to be written at the next dispatch — closes when ground-truth-ledger.md exists in the reviewing round's directory`. Alternatively, change spec.md:163 to say only the correctness lens closes it by rule and the other lenses mark it from the same file-existence check named in the phrase. Add the two-lens case to the Test plan closure row.

### F-3: Grading order is ambiguous for a dead anchor that appears only in the row
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Grading a checked row (spec.md:123); spec § Decision 6 step 6 (spec.md:98-102)
**Claim:** "When the spec sentence's own anchor supports the claim and only the row differs from it, file a P2, not a P1. An anchor whose file or symbol is gone is graded by the agent's existing Anchor drift rule ...: P1 per dead citation".
**Why this is wrong:** Both sentences apply to a row whose anchor is dead while the spec sentence carries a live, supporting anchor. If a reviewer takes the Anchor drift sentence, the result is a blocking P1 with no spec site. Decision 6 step 6 gives only two blocking dispositions, and `fixed: edited § <section>` would name a section with no edit. That is the evidence-only-fix path round-3 F-2 removed. The Test plan lists "a dead path" and "a row whose anchor differs from a correct spec sentence" separately and does not give the combined outcome.
**Suggested fix:** State the precedence in the Grading bullet: "The row-differs P2 applies first. Anchor drift grades the spec sentence's own citation, never a citation that appears only in the row." Add the combined case to the Test plan row at spec.md:183.

### F-4: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** The spec is authored from the VHS-26 brief and ticket.
**Why this is wrong:** `memory_search` on namespace `skills` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The brief states the ticket has no acceptance criteria (brief.md:45), so the brief's Done-when list was used as canonical.
**Suggested fix:** None to the spec.

### F-5: After a failed first write, a new spec's Phase 1 rows are dropped although the author still holds them; preamble count nit
**Severity:** P3
**Where:** spec § Decision 6 step 6 (spec.md:100); spec § Decision 4 (spec.md:71); spec § Decisions (spec.md:24)
**Claim:** "rows the missing file would have held are not reconstructed"; "the no-claims line is never written in their place"; "Three rules are the spec author's additions".
**Why this is wrong:** Not a contradiction on a careful read, but the two sentences sit close together. If round 1's write fails and the revision edits no section, round 2's file holds the no-claims line, and the Phase 1 evidence for the whole new spec is never recorded even though the rows are in hand. The Test plan closure row ("followed by a successful write") does not state that outcome. Separately, spec.md:24 says "Three rules" and lists four (Decision 3 itself says "These two rules"); the rebuild rule and the row-differs P2 are also author additions it does not list.
**Suggested fix:** Either let the next dispatch after a `ground-truth ledger missing` finding also write rows still held from the failed write, or add "this includes Phase 1's rows for a new spec" to step 6 and the expected result to the Test plan. Change "Three rules" to match the list.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 2 | P4: 0

STATUS: GREEN
