All grounding steps completed: spec and brief re-read from disk; Plane VHS-37 retrieved from namespace `skills` (tag-exact, confidence 1.00 — the ticket's narrower "valid + out-of-scope + non-trivial" framing is the 2026-09-06 original, superseded by the brief's dated 2026-09-08 Decision 2 ceiling, which the spec follows); `CLAUDE.md` read (gitignored machine-local pointer) plus `AGENTS.md`; every Scope-table anchor re-verified against `main` at `124700b`; `git log -10` run on all six touched files.

**Anchor verification (all pass):** `SKILL.md:294-296` (Phase 1 heading 294 / `Output path:` 296) ✓; `:365-368` (2b example fence) ✓; `:378-383` (disposition prose) ✓; `:411-424` (2d) ✓; `:426-464` (2e; rounds 1–3 at 428-432, round 4 at 434-464) ✓; `:435-441` (classification bullet, REWRITE definition ends at 441) ✓; `:446-462` (closed-issues manifest) ✓; `:466-487` (2f halt) ✓; `:489-591` / `:555-557` (2f-i) ✓; `:593-624` and the "already exists" idiom at `:599-601` ✓; `:626-659` (Phase 3) ✓; `:685-` (Failure modes) ✓; `:288` (delete-to-re-author escape) ✓. Agents: `closure_manifest` at `correctness:18`, `edge-cases:18`, `conventions:20`, `scalability:18` ✓; enumeration at `correctness:38-39`, `edge-cases:38-39`, `conventions:43-44`, `scalability:30` ✓; "REOPENED items are P0" at `correctness:51`, `edge-cases:51`, `conventions:56`, `scalability:40` ✓; step 6 immediately precedes step 7 in all four ✓. `docs/spec-workflow-reference.md:84`, `:88` ✓.

**Grep baselines (all confirm the checklist's "before" values):** `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → **7**; `grep -cF 'Address every P0 and P1 finding' skills/spec-cycle/SKILL.md` → 1; `grep -c 'DEFERRED' agents/spec-reviewer-*.md` → 0 in all four; `grep -c 'DEFERRED' docs/spec-workflow-reference.md` → 0; `grep -cF 'Address every P0 and P1.' docs/spec-workflow-reference.md` → 1; `grep -cF 'including round 1' docs/spec-workflow-reference.md` → 0; `grep -rn 'Deferred' skills/spec-close/SKILL.md skills/ship-spec/SKILL.md` → 0. `sync.py push --dry-run` and `lint.py --strict` both exist (`sync.py:209`, `lint.py:270`).

**Recent commits:** `ea5c2b0` (2026-09-07, VHS-36) touched `docs/spec-workflow-reference.md` at `:31,35` — above this spec's `:84`/`:88` anchors, both of which I re-verified as correct. `ecdfefe` / `c97d4ad` (2026-09-07) touched `SKILL.md`'s 2f-i region, as the spec's Scope note already records.

---

# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | P1 revert leaves stale CLOSED entry round 4 turns into a constraint | CLOSED | spec:108 Design 3 bullet 2 ("The revert supersedes the reverted finding's closed-issues entry: at round 4 that entry's constraint is its deferral row") + D16 (spec:49). Residual placement/match-key gap filed as F-9 below. |
| correctness | F-2 | P1 "revert the original fold" undefined after a later re-edit | CLOSED | spec:108 adds "and none of the original fold's sites has been re-edited by a later fold"; spec:109 routes that case to fold-again; D16 states it. |
| correctness | F-3 | P1 checklist row 5's "7 before and after" falsified by R3 | CLOSED | spec:160 now reads "→ 8 after (7 before): the one new line is rule R3". Baseline verified at 7. Wrapping caveat filed as F-8. |
| correctness | F-4 | P2 D15 anchors `:438-441`, Scope/Design 1 anchor `:436-441` | CLOSED | All three sites now say `:435-441` (spec:17, :48, :74); verified correct against SKILL.md:435-441. |
| correctness | F-5 | P2 one malformed row → two P0s per lens | CLOSED | spec:148 step 7 sentence: "the defect is reported once, not as a second finding." |
| correctness | F-6 | P2 in-scope-P0 exception vs D17's opaque-Scope rule | CLOSED | spec:146 adds "That is different from classifying your own candidate: every lens decides for itself…". |
| correctness | F-7 | P2 revert line puts an out-of-round finding in a round-scoped manifest | CLOSED | D13 (spec:46) now carries the explicit exception. Dangling pointer filed as F-2 below. |
| correctness | F-8 | P2 R4 makes Phase 1 a no-op even after the brief is narrowed | CLOSED | R4 (spec:100): "To re-author from a changed brief (for example after 2f option 3), delete the spec first — the escape Phase 0's re-run pin already names (`:288`)." `:288` verified. |
| correctness | F-9 | P3 "fold predates this invocation" branch unreachable | CLOSED | spec:109's fallback list no longer contains it; spec:105 states prior-invocation folds are not recounted. (New D16 contradiction filed as F-1 below.) |
| correctness | F-10 | P3 Done-when 2 mechanism has no asserting checklist row | PARTIAL | spec:180 now cites "Checklist rows 4 (Phase 1 hunk), 8." Row 4 asserts only that a hunk lands in `:294-296`, not its content. P3, non-blocking. |
| edge-cases | F-1 | P0 R2 forbids the reads/edits the spec mandates | CLOSED | R2 rewritten (spec:98): reads enumerated (Design 5 render, every reviewer), two permitted edits (routing-violation repair, re-anchor), never delete, never overwrite `Follow-up`. |
| edge-cases | F-2 | P1 round 4 classifies the deferral section into neither bucket | CLOSED | D15 (spec:48) + Design 1 round-4 paragraph (spec:74): FROZEN with an append carve-out; checklist row 9 asserts `is FROZEN with one permitted edit` → 1. |
| edge-cases | F-3 | P1 nothing verifies the preamble is present | CLOSED | spec:146 block: "if it does not, file a P0 titled `routing violation: missing preamble`"; restated spec:78, :138. |
| edge-cases | F-4 | P2 `(new)` site is unfalsifiable | PARTIAL | spec:61 adds "at least one listed site must already exist", but a two-site row of one real + one `(new)` site remains unfalsifiable (spec:146 "dispute a site only when an unmarked site names a section that does not exist"). P2, unchanged severity. |
| edge-cases | F-5 | P2 recount misses `reworked:` and Decision-anchored folds | CLOSED | spec:105 checks `fixed:` **and** `reworked:` lines; Design 4 (spec:113) makes 2b prose require naming every section touched, "not only the Decision that records it". |
| edge-cases | F-6 | P2 render "never omits a row" vs unreadable heading | CLOSED | spec:131 extraction rule: every `###`-or-deeper heading is a row; unparseable id prints `D-?`; "never omits a heading it found". |
| edge-cases | F-7 | P2 R4 adopts a half-written spec with no validation | CLOSED | R4 (spec:100) adds the six-heading completeness halt. Omission of `## Test command` filed as F-3 below. |
| edge-cases | F-8 | P3 round-4 dispositions have no manifest | CLOSED | spec:74: rejection/fold recorded as a title suffix in the 2f halt block. |
| edge-cases | F-9 | P3 rows accumulate without GC; sync skew | CLOSED-as-deferred | (a) recorded in `## Deferred (P2+)` (spec:205); (b) applied in Design 6 (spec:138, "run `python sync.py install`"). |
| edge-cases | F-10 | P3 render columns not row fields; resolved rows still print | CLOSED-as-deferred | sub-parse half applied (spec:131); the resolved-row half recorded (spec:206). |
| edge-cases | F-11 | P4 duplicate anchors for the round-4 sentence | CLOSED | Unified to `:435-441` (see correctness F-4). |
| conventions | F-1 | P1 Design 2 doesn't say which of R1–R5 ship into SKILL.md | CLOSED | spec:95: "Rules R1, R2, R3, R5 are written into SKILL.md with the shape; R4's normative sentences land in Phase 1 (`:294-296`)." |
| conventions | F-2 | P1 R2 contradicts Design 5; renamed section is an unfixable P0 | CLOSED | R2's re-anchor allowance with `(re-anchored round <n>)` (spec:98), mirrored in the block (spec:146). Removal/collapse residual filed as F-5 below. |
| conventions | F-3 | P2 `grep -c 'DEFERRED, or NEW'` cannot match (wrapped enumeration) | CLOSED | Row 6 (spec:161) now uses `grep -c 'DEFERRED'`; baseline 0 in all four files verified. |
| conventions | F-4 | P2 two anchors for the same round-4 sentence | CLOSED | Same as correctness F-4. |
| conventions | F-5 | P2 Design 3's two manifest forms not in 2b's vocabulary | CLOSED | Design 4 (spec:113) declares the `(recount: …)` suffix and the revert line; Design 7 edit 1 (spec:142) names both. See F-2 below for the dangling "see …" pointer. |
| conventions | F-6 | P2 reference-doc reconciliation under-scoped | CLOSED | spec:21: `:88` gains `DEFERRED` **and** "one sentence stating the every-round deferral check"; row 10 asserts `including round 1`. |
| conventions | F-7 | P3 `routing violation:` title is a silent contract addition | CLOSED | Minor-additions bullet (spec:51): "nothing parses it and the finding's shape is otherwise the standing contract". |
| conventions | F-8 | P4 row 3's parenthetical names three sites; there are four | CLOSED | spec:158 now names four (2e step 4, shape heading, D15 sentence, Failure-modes bullet). |

## Findings

### F-1: D16 says the recount runs on a re-run and forces a fold; Design 3 says a prior-invocation fold is never recounted
**Severity:** P1
**Where:** spec.md:49 (§ Decisions, D16) vs spec.md:105 (§ Design 3, opening paragraph) and spec.md:109 (Design 3, third bullet)

**Claim:** D16 — "At round 4 the closed-issues manifest (`:446-462`) makes every CLOSED fix a regression constraint; **on a re-run there is no in-context fold record**; and a site re-edited by a later fold has no defined 'original edit' to remove. **In all three cases the recount runs but resolves by folding again with the corrected site list.**"

Design 3 — "check its `Where` against every section named on any `fixed:` / `reworked:` line of the manifests built earlier in **this invocation** (**a fold made in a prior invocation is not detectable and is not recounted**)."

**Why this is wrong:** The two texts give different, observable answers for the same input. Under Design 3, a new P0/P1 landing on a section a *prior-invocation* fold touched never enters the recount at all: it is routed by Design 1 normally, which — if it names two or more sites and is out-of-scope or an in-scope P1 — **defers**, with no `(recount: …)` suffix. Under D16, that same finding "resolves by folding again with the corrected site list", i.e. a forced fold plus the `(recount: <k> sites, fold kept)` suffix that Design 4 (spec:113) makes 2b prose require. Forcing a fold there bypasses the Decision 2 ceiling, which is the spec's central mechanism.

Design 3's third bullet is internally consistent with its own opening — the "otherwise" list is "(count still one; an in-scope P0; round 4; or a site re-edited since)" and correctly omits the re-run case. D16 is the outlier: for a prior-invocation fold there is nothing to recount, because the manifest that would name the folded section was never built in this context. This is a new variant of the root behind round-2 correctness F-1/F-2, introduced by the round-3 text that closed them.

The prose is what ships into `skills/spec-cycle/SKILL.md` § 2e (spec:17), so an implementer resolving the conflict in D16's favour writes a rule that overrides the ceiling.

**Suggested fix:** In D16 (spec:49), drop the re-run case from the "three cases" sentence and state Design 3's actual answer. E.g.: "At round 4 the closed-issues manifest (`:446-462`) makes every CLOSED fix a regression constraint, and a site re-edited by a later fold has no defined 'original edit' to remove; in both cases the recount runs but resolves by folding again with the corrected site list. On a re-run there is no in-context fold record, so the recount does not run at all and the new finding is routed by Design 1 with no recount suffix."

### F-2: Design 7's input-line clause points at two places that say nothing about the round-qualified revert line
**Severity:** P2
**Where:** spec.md:142 (§ Design 7, edit 1), against spec.md:146 (the block) and spec.md:148 (step 7)

**Claim:** The `closure_manifest` bullet gains "… a round-qualified revert line names an earlier-round finding **(see the Deferred-findings block and step 7)**".

**Why this is wrong:** Neither referenced target carries any rule about the revert line. The Deferred-findings block (spec:146) covers only preamble presence, seven-field well-formedness, `Scope` verification, same-root suppression, and routing violations — the words "revert", "round-qualified", and "earlier-round" do not appear. Step 7's new sentence (spec:148) is keyed on the `deferred: D-<n>` disposition only. The behaviour D13 promises — "reviewers treat a round-qualified line as provenance and verify it against the row, not against the prior round's reports" (spec:46) — is a spec Decision that never lands in any of the three agent edits, so the four agents ship without it. Following Design 7 literally writes a cross-reference to nothing.

This matters in practice because the reviewer's step 7 walks "every finding in the prior round" (verified at `agents/spec-reviewer-correctness.md:38`), and a revert line names a round-*m* finding that is absent from round-(N−1)'s reports — exactly the case a reviewer would otherwise flag as an unreconcilable manifest line.

**Suggested fix:** Either (a) add D13's sentence to the byte-identical block — "A manifest line whose finding id is round-qualified (`<lens>/R<m>/F-<k>`) names a finding from an earlier round whose fold was reverted; verify it against the row it cites, not against the prior round's reports, and do not treat its absence from round N−1 as a defect" — or (b) point the input-line clause at D13 by restating the rule inline instead of citing a section that lacks it.

### F-3: R4's completeness halt omits `## Test command`, which Phase 1 mandates and `/ship-spec` treats as its gate source of truth
**Severity:** P2
**Where:** spec.md:100 (§ Design 2, rule R4)

**Claim:** "If the existing file lacks any of `## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Done when`, `## Out of scope`, halt".

**Why this is wrong:** Phase 1's own minimum-section list at `skills/spec-cycle/SKILL.md:300-307` is seven items, not six — `**Test command**` sits between `Test plan` and `Done when` and is explicitly load-bearing: "ship-spec treats this as source of truth for its test gate (see ship-spec Phase 0 step 4); if absent, ship-spec falls back to CLAUDE.md 'Build & Run' and halts loudly if neither yields a runnable command." R4's sentences land at `:294-296`, immediately above that list, so the two lists are adjacent and visibly disagree.

The consequence is narrow but real, and it is the case the spec's own § Out of scope item 9 leans on R4 to cover ("R4's incompleteness halt covers the interrupted-write case", spec:198): a spec whose Phase-1 write was interrupted between `## Test plan` and `## Test command` passes R4's check, is adopted verbatim as v1, and reaches `/ship-spec` without a test command.

**Suggested fix:** Add `` `## Test command` `` to R4's list at spec:100 (between `## Test plan` and `## Done when`), matching `SKILL.md:300-307`'s order.

### F-4: The "exactly one line" rule is cited at `:369-371`, but it lives at `:378-379` — inside the region this spec edits
**Severity:** P2
**Where:** spec.md:119 (§ Design 4, closing sentence)

**Claim:** "The 'P0/P1 findings only … exactly one line' rule at `:369-371` is unchanged; the revert line is the one stated exception, defined in the same prose."

**Why this is wrong:** `SKILL.md:369-371` is a blank line plus "P0/P1 findings only (P2 dispositions are visible in the spec's edits or / its `## Deferred (P2+)` section). A synthetic missing-STATUS P0 (per" — it does not contain "exactly one line". That phrase is at `SKILL.md:378-379`: "Build it from the revision work you just did in 2e. Map each / P0/P1 finding to exactly one line: finding ID, severity, the title copied…". `:378-383` is precisely the disposition-phrase prose the Scope table (spec:16) says this spec edits.

So the spec asserts as "unchanged" a rule half of which sits inside its own edit region and which must in fact gain the revert exception — an implementer who takes the "unchanged" claim at face value edits only the disposition-phrase list at `:380-383` and leaves `:379`'s flat "Map each P0/P1 finding to exactly one line" contradicting Design 3's extra revert line. The design intent is recoverable from Design 4's fourth clause ("state that a fold reverted under the recount adds one extra, round-qualified line"), which is why this is P2 and not higher.

**Suggested fix:** Rewrite spec:119 as: "The 'P0/P1 findings only' rule at `:370-371` is unchanged. The 'Map each P0/P1 finding to exactly one line' sentence at `:378-379` gains the revert line as its one stated exception, defined in the same prose."

### F-5: R2 claims to handle a *removed* section, but its only mechanism presupposes a successor heading — and two sites collapsing into one leaves the row below the "two or more" floor
**Severity:** P2
**Where:** spec.md:98 (rule R2, edit (b)) and spec.md:146 (the well-formedness rule)

**Claim:** R2 — "re-anchoring `Where` or `Propagation sites` to a new heading when a later round **renames or removes** the section they name". Block — "its `Propagation sites` names **two or more** sections, at least one of them exists in the spec".

**Why this is wrong:** "Re-anchoring to a new heading" is defined only for a rename; a removal has no new heading to name, so R2's stated coverage of removals has no mechanism behind it. Worse, the common spec-revision case is a *merge*: a row's two sites `§ A; § B` collapse when § B is folded into § A. Re-anchoring § B to § A leaves the field naming one distinct section, so the well-formedness check's "two or more sections" fails, and the resulting `routing violation: D-<n>` P0 has no legal repair — R2's permitted edit (a) can only correct the field, and the honest correction (one site) contradicts the ceiling that put the row there, while dropping the row is forbidden ("`/spec-cycle` never deletes a row"). That is the same dead-end shape as round-2 edge-cases F-1, now reachable through the re-anchor path that closed it.

There is an escape — writing `§ A (re-anchored round 3); § A (re-anchored round 3)` satisfies "names two or more sections" literally — which is why this is P2 rather than a blocking P0, but the spec should not depend on a reader finding a duplicate-entry loophole.

**Suggested fix:** In R2 (spec:98) add a third permitted edit for the removal/merge case, e.g. "when a listed site is removed or merged into another, re-anchor it to the absorbing section and append `(merged into § <x>, round <n>)`", and in the block (spec:146) qualify the floor: "`Propagation sites` names two or more entries; entries that a `(merged into …)` marker has collapsed onto one section still satisfy the floor."

### F-6: The row shape labels the field `Suggested fix (verbatim):` while every consumer calls it `Suggested fix`
**Severity:** P3
**Where:** spec.md:89 (row shape) vs spec.md:98 (R2), spec.md:47 (D14), spec.md:146 (block)

**Claim:** Shape — `**Suggested fix (verbatim):** <the reviewer's Suggested fix, unedited>`. Block — "all seven fields are present (Finding, Deferred in, Where, **Suggested fix**, Propagation sites, Scope, Follow-up)". R2 — "The finding record — `Finding`, `Deferred in`, `Suggested fix` — is never rewritten." D14 — "the same defect the row's title and `Suggested fix` describe."

**Why this is wrong:** The producer writes one label and the three consumers name another. A reviewer implementing the well-formedness check as an exact label match reports a missing field on every conforming row; a prefix match works, but nothing in the spec says which to use. This is the field-label analogue of the anchor drift the spec has already had to fix twice.

**Suggested fix:** Pick one. Either change the shape's label to `**Suggested fix:**` and move "verbatim" into the value hint, or add `(verbatim)` to the block's seven-field enumeration and to R2/D14.

### F-7: Checklist row 10 pins an exact literal in `docs/spec-workflow-reference.md` that no Design section specifies
**Severity:** P3
**Where:** spec.md:165 (checklist row 10) vs spec.md:21 (Scope table)

**Claim:** Row 10 — "`grep -cF 'including round 1' docs/spec-workflow-reference.md` → 1". Scope — "line 88's paragraph gains `DEFERRED` in the status set and **one sentence stating the every-round deferral check**."

**Why this is wrong:** Verified baseline: `grep -cF 'including round 1' docs/spec-workflow-reference.md` → 0 today, so row 10 is asserting new wording. But the Scope table describes the sentence semantically, not lexically; an implementer who writes "checked in every round, not only from round 2" satisfies the design and fails the checklist. The phrase exists only inside the agent block's title (spec:146, "Deferred findings (every round, including round 1)"), which is a different file.

**Suggested fix:** In spec:21, pin the wording — "…and one sentence stating that the deferral check runs in every round, including round 1" — so the design and the assertion agree.

### F-8: Checklist row 5's exact count of 8 breaks if the implementer hard-wraps R3
**Severity:** P3
**Where:** spec.md:160 (checklist row 5)

**Claim:** "`grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → 8 after (7 before): the one new line is rule R3".

**Why this is wrong:** `grep -c` counts matching *lines*, and R3 (spec:99) contains two occurrences of `## Deferred (P2+)` on what the spec assumes is one line. The assumption is fragile: `SKILL.md`'s 2b prose region (`:370-388`) is hard-wrapped at roughly 72 columns while 2e's bullets (`:429-432`) are not, so an implementer matching the file's mixed style could wrap R3 across two lines and produce 9, failing an assertion the spec pins as exact. The test plan's own preamble says "Assert hunk regions, not counts" (spec:154), which row 5 does not follow.

**Suggested fix:** Loosen row 5 to `→ 8 or 9 after (7 before); rule R3 is the only new text containing the literal, and it may occupy one or two lines depending on wrap. Row 4's region assertion is what proves no existing line moved.`

### F-9: The reverted-fold superseding rule is stated in 2e's rounds-1–3 branch, but the actor is the round-4 branch — and the match key is unstated
**Severity:** P2
**Where:** spec.md:108 (Design 3, bullet 2) and spec.md:49 (D16), against `SKILL.md:446-462` (declared byte-identical, spec:23)

**Claim:** "The revert supersedes the reverted finding's closed-issues entry: at round 4 that entry's constraint is its deferral row, not the removed fix — stated in the routing text because `:446-462` is unchanged."

**Why this is wrong:** Two gaps remain after the round-2 fix. (1) *Placement.* The sentence ships into the rounds-1–3 half of 2e (spec:17 confirms the routing step replaces the bullet at `:430`), but the agent that builds the closed-issues manifest is executing the `round == 4` branch, whose text at `SKILL.md:460-461` is left byte-identical and reads flatly: "Every entry is a regression constraint: the rewritten spec must preserve the fix that closed it." A round-4 author following its own branch sees the unqualified rule; the carve-out sits under "If still red and `round < 4`". (2) *Match key.* The rule says the constraint "is its deferral row" but never says how the round-4 author links a closed-issues entry to a row. The link exists — `SKILL.md:453`'s `finding_id: "correctness/R1/F-3"` matches the row's `Finding:` field, which spec:86 defines as `<lens>/R<n>/F-<k>` — but the spec never states it, and if the revert happened in round 2 the round-3→4 manifest carries no revert line to signal it either.

Consequence: at round 4 the author re-applies the reverted fix as a regression constraint, undoing the deferral and re-creating exactly the multi-site fold the ceiling routed away.

**Suggested fix:** Add one sentence to the round-4 half of the Design 1 round-4 paragraph (spec:74), which already edits that branch: "When building the closed-issues manifest, an entry whose `finding_id` matches the `Finding:` field of a row in `## Deferred — follow-up required` is superseded: its regression constraint is the row, not the removed fix." That keeps `:446-462` byte-identical while putting the rule in the branch that executes it, and pins the match key.

## Summary
P0: 0 | P1: 1 | P2: 5 | P3: 3 | P4: 0

STATUS: RED P0=0 P1=1 P2=5 P3=3 P4=0
