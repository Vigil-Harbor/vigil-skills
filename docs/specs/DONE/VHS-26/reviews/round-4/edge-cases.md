# Edge-Cases Review — round 4

Grounding notes: `review_mode: delta`. Spec, brief, the `changed_regions` file and the round-3 `ledger.md` (the closure manifest) were read fresh, along with all three round-3 reports. Sources read: `skills/spec-cycle/SKILL.md` (mode table `:355-380`, Phase 1 `:384-390`, Delta no-op, Two counters, Round artifacts `:444-460`, §2b `:554-604`, §2d `:696-704`, §2e `:706-722`, recount `:757`, §2g `:939-970`) and `agents/spec-reviewer-correctness.md:55-112`. Nothing under `VHS-26.attempt-1/` was read.

Anchor check: every `file:line` citation in the changed regions resolves to the named symbol at the cited line at HEAD `fc20f94` — `SKILL.md:390`, `:444-458`, `:450`, `:454`, `:460`, `:462`, `:558`, `:578-579`, `:594-601`, `:698`, `:711-718`, `:715`, `:757`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`. No dead or moved anchors.

Deferred-findings block: one section, preamble present with the required sentence. Row D-1 is well-formed (seven fields, blockquoted fix with one blank line before `Propagation sites`, three existing sites, stated `out-of-scope` token, `Follow-up: VHS-63`). The ceiling does not apply. No routing violation. D-1's root is not re-filed.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Delta pass 1 after a red halt carries a closure manifest, so the omission boundary is not empty on a re-run | CLOSED | Deliberate direction change with rationale. Decision 8 Omission bullet (spec.md:124) now takes the boundary from the rows' own `Spec section` values and forbids deriving it from the closure manifest or `changed_regions`. Decision 4 third bullet (spec.md:67) gives that dispatch the no-claims line, so there is no boundary. Test plan (spec.md:184) agrees. |
| edge-cases | F-1 (P0) | Delta pass 1 after a red halt has a closure manifest, so the omission boundary fires where the spec says it must not | CLOSED | Same root and evidence. The new-spec line is gone from Decision 4, § Phase 1 authoring changes and § Round artifact and dispatch changes. Omission is now P2 (spec.md:124, :127). |
| correctness | F-2 (P1) | An evidence-only ground-truth fix puts a section in the omission boundary with rows for only the named claims | CLOSED | Deliberate direction change. Decision 6 step 6 (spec.md:98-100) removes the carried-rows disposition. An unsupported claim is an ordinary fold, and step 5 supplies every row for that section. A row-only mismatch is P2 (spec.md:123). The claim-versus-section mismatch no longer exists. |
| edge-cases | F-2 (P1) | An evidence-only fix carries rows for the named claims only … the loop cannot close | CLOSED | Same root and evidence. § Apply-findings changes (spec.md:153-155) matches. |
| edge-cases | F-3 (P2) | Ground-truth finding on the final pass gets a `fixed:` disposition for rows never written | CLOSED | spec.md:100 gives one phrase for every pass and closes on file existence (spec.md:125). Test plan spec.md:185 lists the final-pass case. A residual is filed as F-2 below. |
| edge-cases | F-4 (P2) | "Section" not defined the same way for rows and boundary | CLOSED | spec.md:61, :97 and :124 all say innermost heading, own body. |
| edge-cases | F-5 (P2) | Closure cannot be met when the fix removes or rewrites the claim | CLOSED | spec.md:125 verifies against the current spec; Test plan spec.md:185 covers deletion. |
| edge-cases | F-6 (P3) | Held rows have no durable home | CLOSED | Rebuild rule and named accepted gap at spec.md:71; propagated to spec.md:145 and :178. |
| edge-cases | F-7 (P3) | "At most five" versus "also every named row" | CLOSED | The named-row clause is removed from the Sample bullet (spec.md:122). |
| edge-cases | F-8 (P3) | Ticket lookup blocked | PARTIAL | Host condition, still denied this round; see F-6. No spec defect. |
| correctness | F-3 (P3) | Preamble does not mark author-pinned choices | CLOSED | spec.md:24. |
| correctness | F-4 (P3) | ticket not cached | PARTIAL | Host condition; see F-6. |
| correctness | F-5 (P4) | unittest pattern quoted two ways | CLOSED | spec.md:197 and :209 both use double quotes. |
| conventions | F-1 (P2) | New `fixed: ground-truth rows carried` disposition not reconciled | PARTIAL | Points 1 and 2 are closed: the form is removed, spec.md:155 says the vocabulary and recount paragraphs are untouched. Point 3 (how a lens without the path closes a no-spec-site finding) still applies to the missing-file phrase; filed as F-2 below. Stays P2. |
| conventions | F-2 (P2) | `Anchor: none` presented as carried from the brief | CLOSED | Labelled at spec.md:24 and :40. Grading now covers any file "this host can read" (spec.md:123). |
| conventions | F-3 (P2) | Bare "ledger" in Decision 3 | CLOSED | spec.md:40 and :42 say "ground-truth ledger". |
| conventions | F-4 (P3) | Spec-level additions for the drift check | CLOSED | spec.md:24 names the three surviving additions; the new-spec line and the manifest-derived boundary no longer exist. |

Manifest check: all four round-3 P0/P1 findings have a line, and every section each line names carries the stated rework.

## Findings

### F-1: The omission P2 is tagged `Pre-ship recommended`, which makes it a 2g candidate that 2g has no legal way to act on
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 8 — Correctness alone enforces the ledger (Omission bullet, spec.md:124); spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (spec.md:102)
**Edge case:** Partial failure across the green boundary. The omission P2 is the only ground-truth finding on a round that goes green, or it was raised on an earlier round and the loop then goes green.
**What happens:** `skills/spec-cycle/SKILL.md:949-955` collects every `Pre-ship recommended` P2 from all rounds' reports. Step 3 (`:959-965`) applies a candidate only when it is a spec clarification. The omission finding's only fix is holding rows for a next dispatch (spec.md:102). On green there is no next dispatch, and Decision 5 forbids a ground-truth ledger or addendum for polish (spec.md:87). So 2g meets a candidate that is neither a clarification nor over a hard limit. Three outcomes are plausible, and the spec picks none:
- 2g records it as folded with no change.
- 2g lists it in `## Deferred (P2+)`.
- 2g "fixes" it by adding or changing anchors in the spec sentences without the live read. That is the ungrounded polish row D-1 already defers; this tag feeds it.

For an earlier-round omission P2 that was fixed by held rows, 2g's "skip any already addressed by an earlier revision" test has nothing in the spec to check, so it may be re-collected. The correctness agent's own contract reserves the tag for a P2 whose fix is folded into the spec, which this one is not.
**Why the spec misses it:** Decision 6's last paragraph covers only the 2e path, and the green round never runs 2e (`SKILL.md:943-945`).
**Suggested fix:** Drop the `Pre-ship recommended` tag from the omission finding. Alternatively keep it and add one sentence to Decision 6's P2 paragraph: on a green round the omission P2 is recorded in `## Deferred (P2+)` and no ground-truth ledger is written. Either stays inside §2e and the correctness agent; §2g is not edited.

### F-2: The other lenses have no rule for closing `ground-truth ledger missing`, although the spec says every lens can already apply one
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 6 (step 6, second bullet, spec.md:100); spec § Correctness reviewer changes (spec.md:163)
**Edge case:** Runtime precondition false. The spec assumes "a missing file is fixed by the file existing" is "a rule every lens can already apply".
**What happens:** In round C+1 the edge-cases, conventions and scalability lenses read round C's `correctness.md`, see a P0, and must mark it CLOSED, PARTIAL or REOPENED "against the current spec". The manifest line reads `fixed: ground-truth ledger to be written at the next dispatch`. It names no section and no path, and those lenses receive no `ground_truth_ledger_path`. The closure rule at spec.md:125 is written into the correctness agent only. A lens that follows its step 7 literally finds no spec evidence and marks the finding PARTIAL or REOPENED, which is P0 by its own closure rule. One such call makes round C+1 red for a defect that is already repaired. On the final pass it costs a red halt. The missing-STATUS precedent (`SKILL.md:576-580`) shows lenses usually cope with a process phrase, so this is non-deterministic, not certain.
**Why the spec misses it:** Round-3 conventions F-1 point 3 raised it for the carried-rows form. The rework removed that form but kept a no-spec-site disposition.
**Suggested fix:** Put a verifiable anchor in the phrase: `fixed: ground-truth ledger to be written at the next dispatch — docs/specs/TODO/<TICKET-ID>.reviews/round-<C+1>/ground-truth-ledger.md`. Any lens can then check that the file exists. A path is not a `§` section, so the recount still never reads it. Reword spec.md:163 from "every lens can already apply" to say the path on the manifest line is what the other lenses check.

### F-3: "The row sample opens code anchors, not spec sections" no longer matches the Sample and Grading bullets
**Severity:** P3
**Where:** spec § Decision 8 (spec.md:118, against :122-123)
**Edge case:** Delta pass where a row names a section outside `changed_regions` and `open_findings`. This happens when rows are held to fix a P2 (omission, or row-differs) with no spec edit (spec.md:102), or after a rebuild.
**What happens:** The Sample bullet now says "read the spec sentence the row names", and Grading files a P1 "against the spec section that holds the claim". The preamble still says the sample opens no spec sections and does not widen the delta scope. One reviewer grades the row and files against an out-of-scope section; another skips it.
**Suggested fix:** Replace the sentence with: "Its row sample reads the anchors and the spec sentences the rows name; this is a grounding check, so it is not limited by `changed_regions`."

### F-4: Three row and closure states have no grading rule
**Severity:** P3
**Where:** spec § Decision 8 (Sample, Grading and Closure bullets, spec.md:122-125); spec § Test plan (spec.md:183, :185)
**Edge case:** Malformed rows and repeated failure.
**What happens:**
- **Row with no matching sentence.** A row names a claim or heading that is no longer in the spec (a stale rebuilt row, a renamed heading). "Read the spec sentence the row names" has no target, and no severity is given.
- **Sentence with no anchor.** The row's anchor supports the claim but the spec sentence carries none. The row-differs P2 presumes the sentence has an anchor.
- **Second failed write.** The predecessor `ground-truth ledger missing` is not closed, so it is REOPENED (P0), and the Missing bullet files a fresh P0 for the same file. One defect is counted twice; "one defect is one finding" is scoped to citations.

All three degrade without harm: the gate result is the same.
**Suggested fix:** Add to Grading: "A row whose sentence is not in the spec, or whose sentence carries no anchor, is the same P2." Add to Closure: "When the current file is also missing, mark the predecessor REOPENED and cite this round's `ground-truth ledger missing` finding; do not count it twice." Add the first two cases to the Test plan's mental-exercise row.

### F-5: A no-claims line on a newly authored spec passes every check
**Severity:** P3
**Where:** spec § Decision 8 (stated limit, spec.md:127); spec § Decision 4 (spec.md:71)
**Edge case:** Silent failure. Held rows are lost before the first dispatch (compaction, or the interrupted-Phase-1 gap), and the author writes the no-claims line.
**What happens:** The Missing check passes, there is no boundary, and no omission finding is possible. The first ground-truth ledger of a new spec is empty and the round can go green. Decision 4 forbids this but nothing detects it, because the reviewer cannot tell a new spec from a re-run. The stated limit describes "a section the author edited and gave no row at all", not this whole-file case. The brief accepts review-only enforcement (Risks item 4), and step 5 of the agent still verifies the claims, so this is a note, not a request for new machinery.
**Suggested fix:** Extend the stated-limit sentence: "The same holds for a file that carries the no-claims line where rows were owed."

### F-6: Ticket lookup blocked
**Severity:** P3
**Where:** grounding step 3
**Edge case:** External system down. `memory_search` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`.
**What happens:** The review proceeded from the brief alone, per the documented degraded path.
**Suggested fix:** None for the spec.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 4 | P4: 0

STATUS: GREEN
