# Conventions Review — round 3

Grounding notes: spec, brief, `AGENTS.md` (the tracked conventions file that the gitignored `CLAUDE.md` points to), wiki `state.md` and `filemap.md` listing (no `architecture.md` exists for this project), and wiki decisions `2026-08-09-review-round-artifacts-are-immutable.md`, `2026-09-08-vhs-37-spec-cycle-fold-defer-reject-routing.md`, `2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md` were read. The shared-memory ticket lookup was denied (`agent 'claude' lacks 'read' on namespace 'skills'`); I proceeded from the brief per the degraded path. Nothing under `VHS-26.attempt-1/` was read.

Deferred-findings block: one section, preamble present with the required sentence. Row D-1 is well-formed (seven fields, blockquoted fix, three propagation sites that all exist). Its `Scope` states `skills/spec-cycle/SKILL.md` §2g Post-green polish, and the brief's Scope table has no §2g row, so the stated region is correct. The token is `out-of-scope`, so the ceiling does not apply. No routing violation.

Anchor check for the changed regions: every `file:line` citation resolves to the named symbol at the current file — `skills/spec-cycle/SKILL.md:390`, `:444-458`, `:450`, `:454`, `:460`, `:462`, `:558`, `:698`, `:711-718`, `:715`; `agents/spec-reviewer-correctness.md:86`, `:88`, `:109`; `AGENTS.md:110`. No dead or moved citations.

## Closure of round 2 findings

The closure manifest is empty (round 2 closed green, no P0/P1). The round-2 P3s are listed for completeness.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | ticket not cached | CLOSED | Host condition, no spec change required; lookup was denied again this round and the brief was used. |
| correctness | F-2 | Author-pinned enforcement choices still lack explicit provenance labels | PARTIAL | spec § Decisions, line 22, now maps each Decision to brief Decisions, but still does not name Decisions 4, 5, 8 and the checklist as resolutions of brief § Risks / decisions items 2–5. Stays P3 (see F-4). |
| edge-cases | F-1 | Author-pinned enforcement choices remain implicit | PARTIAL | Same root and evidence as correctness F-2. |
| conventions | F-1 | Author-pinned enforcement choices still lack explicit provenance labels | PARTIAL | Same root and evidence as correctness F-2. |

## Findings

### F-1: New `fixed: ground-truth rows carried` disposition is not reconciled with the existing manifest vocabulary, the recount trigger, or the other lenses' closure check
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 6 — Revision is a verify–compose–edit–re-read operation (step 6, spec.md:94); spec § Decision 8 — Correctness alone enforces the ledger (Closure bullet, spec.md:117)
**Convention violated:** Cross-surface wire-format lock; repo pattern that every new manifest line shape is enumerated where the manifest grammar lives and carved in or out of the recount explicitly.
**Evidence:**
- `skills/spec-cycle/SKILL.md:594-601` enumerates the legal `fixed:` forms and says a `fixed:` phrase "names **every** spec section the edit touched". The new form names sections where no edit happened, and the spec's Design tells the implementer to edit only §2e, `### Round artifacts` and §2b's input list.
- `skills/spec-cycle/SKILL.md:757` makes "every section named on any `fixed:` / `reworked:` line of the manifests built earlier in this invocation" a re-fold recount trigger, and carves out the one existing non-fold form in words ("a row repair is not a fold"). The spec does not say whether a carried-rows line is a trigger. As written it is, so a later finding in that section recounts a fold that had no site.
- The edge-cases, conventions and scalability agents verify every predecessor finding "against the current spec" and treat a `fixed:` line as naming sections that carry the fold. They receive no ledger path and are not edited (brief fence), so a ground-truth finding fixed with no spec change gives them nothing to verify. The Closure bullet covers the correctness agent only. The existing precedent for a line the other lenses cannot verify (`guarantee/D-<n>`) told all four what to do with it.
**Suggested fix:** Add to Decision 6 step 6 and § Apply-findings changes, all inside `skills/spec-cycle/SKILL.md` and therefore in scope:
1. The form is added to the manifest-vocabulary paragraph at `skills/spec-cycle/SKILL.md:594-601` as the one `fixed:` form whose sections are covered, not edited.
2. A carried-rows-only disposition is not a recount trigger, in the same sentence shape as the existing row-repair carve-out.
3. One sentence on how a lens without the path closes such a finding. The cheapest option that touches no fenced agent is to have the manifest line carry the ground-truth ledger's path as its verifiable anchor.

### F-2: `Anchor: none` relaxes brief Decision 1 but is presented as carried from the brief
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3 — The obligation covers factual runtime claims, not proposed requirements (spec.md:38); spec § Decisions (spec.md:22)
**Convention violated:** Silent spec additions vs the brief, category (d): an unlabelled exception to a carried decision.
**Evidence:** Brief Decision 1: a runtime-behavior sentence "needs a `file:line` anchor that the author read in this run". Brief Decision 2: each row holds "the `file:line` anchor". Brief Done-when 1 has no exception. The spec now allows a sentence with no anchor and a row reading `assumed, not verified`, while spec.md:22 says "Decision 3 carries brief Decisions 1 and 6". The rationale is sound for a system with no readable source, but the drift check cannot see that it is the author's addition. Decision 8 grades an `Anchor: none` row only for behavior under the project root. An out-of-root but readable system (the brief's originating scheduler case) recorded as `assumed` therefore draws no finding.
**Suggested fix:** In spec.md:22 or Decision 3, label the out-of-root and `Anchor: none` rules as a spec-level addition with their rationale ("the brief does not address unreadable source"). Consider one clause in Decision 8's grading bullet for a `none` row on a source the reviewer can read outside the root. No design change is required for green.

### F-3: Decision 3 uses the bare word "ledger" that Decision 4 forbids in the same revision
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:38 ("its ledger row records `Anchor: none`"); also the example quote at spec.md:40
**Convention violated:** Naming and labels — the spec's own rule at spec.md:46 ("called the **ground-truth ledger** everywhere in prose, never the bare word 'ledger'"), which exists because `ledger.md` is the disposition ledger (`skills/spec-cycle/SKILL.md:462`).
**Evidence:** § Phase 1 authoring changes tells the implementer to carry Decision 3's rules "including its rules for a file outside the project root and for a system with no readable source" into the skill. Copied as written, "its ledger row" lands in a file where "ledger" already means the closure manifest. The headings of Decisions 5 and 8 also use the bare word. Those are outside the changed bodies, and renaming them would churn D-1's `Where` and `Propagation sites`, so leave them.
**Suggested fix:** spec.md:38 → "its ground-truth-ledger row records `Anchor: none`". Optionally spec.md:40 → "must write the ground-truth ledger before dispatch".

### F-4: Spec-level additions in this revision, for the human drift check
**Severity:** P3
**Where:** spec § Decision 4 (spec.md:63, new-spec line); § Decision 5 (spec.md:73, write order; spec.md:79, message form); § Decision 6 step 6 (spec.md:94); § Decision 8 (spec.md:112, no-path P3; spec.md:116, omission boundary from the closure manifest; spec.md:117, closure rule)
**Convention violated:** Silent-addition audit, category (c): additions with rationale must stay visible.
**Evidence:** None of these is in the brief's Decisions; each has inline rationale and stays inside the brief's fences (no parser, no computed inventory, no new halt or retry). The no-path tolerance follows the existing "older callers" pattern at `skills/spec-cycle/SKILL.md:556`. The `<filename> NOT written:` message reuses `:454`. Not rewriting the ledger after polish agrees with the wiki decision that review-round artifacts are immutable. This also carries the residual round-2 P3: spec.md:22 maps Decisions to brief Decisions, but Decisions 4, 5, 8 and the checklist also resolve brief § Risks / decisions items 2–5 and are not labelled so.
**Suggested fix:** Extend spec.md:22 with one sentence: "Decisions 4, 5 and 8 and the Test plan also pin brief § Risks / decisions items 2–5; the new-spec line, the write order, the no-path P3, the closure-manifest omission boundary and Decision 6 step 6 are author additions."

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
