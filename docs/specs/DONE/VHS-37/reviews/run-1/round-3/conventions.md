**Grounding completed.** Spec and brief re-read from disk (`C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-37.spec.md`, `.brief.md`). `AGENTS.md` read end to end (the canonical project instructions; `CLAUDE.md` is the gitignored machine-local pointer). Wiki read at `C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki` — `decisions/2026-08-09-review-round-artifacts-are-immutable.md`, `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`, `decisions/2026-06-16-vhs-15-optional-scalability-lens.md`, plus `projects/vigil-skills/state.md` and `filemap.md`. All three round-2 reports read. Baselines re-verified against `main` at `124700b`: `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → **7** (`:371, :424, :431, :611, :618, :622, :623`); `SKILL.md:430` → `- Address every P0 and P1 finding.`; `docs/spec-workflow-reference.md:84`/`:88` as described; `grep -c 'DEFERRED' agents/spec-reviewer-*.md` → 0 in all four; `grep -rn 'Deferred' skills/spec-close/SKILL.md skills/ship-spec/SKILL.md` → 0. The three anchors that disagreed last round (`:435-441`) now agree in § Scope row 3, § Design 1 "Round 4", and D15. `README.md`, `docs/customizing.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md` re-confirmed clean of the 2e rule and the closure-status set. `scale_lens == off`, and no `scalability.md` exists in `round-2/` — nothing to guard against.

---

# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Revert leaves a stale CLOSED entry | CLOSED | § Design 3 bullet 2 (:108) "The revert supersedes the reverted finding's closed-issues entry"; D16 (:49) |
| correctness | F-2 | "Revert the original fold" undefined after re-edit | CLOSED | § Design 3 (:108) "none of the original fold's sites has been re-edited by a later fold"; fallback (:109) "or a site re-edited since" |
| correctness | F-3 | Row 5's "7 before and after" falsified by R3 | CLOSED | § Test plan row 5 (:160) now "8 after (7 before): the one new line is rule R3" |
| correctness | F-4 | D15 anchors `:438-441`, Scope/Design 1 `:436-441` | CLOSED | all three now `:435-441` (:17, :48, :74) |
| correctness | F-5 | One malformed row → two P0s per lens | CLOSED | § Design 7 item 3 (:148) "the defect is reported once, not as a second finding" |
| correctness | F-6 | In-scope-P0 exception vs opaque `Scope` | CLOSED | § Design 7 block (:146) "That is different from classifying your own candidate" |
| correctness | F-7 | Out-of-round manifest line vs D13 | CLOSED | D13 (:46) round-qualified exception; § Design 3 (:108) `<lens>/R<m>/F-<k>`; § Design 4 (:113); § Design 7 item 1 (:142) |
| correctness | F-8 | R4 makes Phase 1 a no-op after a narrowed brief | CLOSED | R4 (:100) delete-to-re-author pointer citing `:288`; D16 headline retitled "rounds 2–3" (:49) |
| correctness | F-9 | Unreachable "predates this invocation" branch | CLOSED | § Design 3 (:105) reworded as an observation; branch removed from the fallback list (:109) |
| correctness | F-10 | Done-when 2 / D15 sentence unasserted | PARTIAL | row 9 (:164) asserts the D15 literal ✓; row 8's `Follow-up: unfiled` assertion is present but cannot match — see F-1 below |
| edge-cases | F-1 | R2 forbids the reads/edits the spec mandates (P0) | CLOSED | R2 rewritten (:98) — reads allowed, two permitted edits, never delete a row, never overwrite `Follow-up` (round-4 residue is NEW, see F-2 below) |
| edge-cases | F-2 | Round 4 preserves the section in neither bucket | CLOSED | D15 (:48) and § Design 1 "Round 4" (:74) — FROZEN with an append carve-out; checklist row 9 (:164) |
| edge-cases | F-3 | Nothing verifies the preamble | CLOSED | § Design 7 block (:146) `routing violation: missing preamble` P0, gated on section presence; § Design 6 (:138) |
| edge-cases | F-4 | `(new)` sites unfalsifiable | CLOSED | § Design 1 step 1 (:61), § Design 2 shape (:90), § Design 7 block (:146) — at least one listed site must exist |
| edge-cases | F-5 | Recount misses `reworked:` / Decision-anchored folds | CLOSED | § Design 3 (:105) "every section named on any `fixed:` / `reworked:` line"; § Design 4 (:113) "names every spec section the edit touched" |
| edge-cases | F-6 | Render locator vs "never omits a row" | CLOSED | § Design 5 (:131) rewritten — every `###`-or-deeper heading is a row, `D-?` fallback |
| edge-cases | F-7 | R4 adopts a truncated/broken spec | CLOSED | R4 (:100) six-heading completeness halt; § Out of scope 9 (:198) fences the write discipline |
| edge-cases | F-8 | Round-4 `reject` recorded nowhere | CLOSED | § Design 1 "Round 4" (:74) title-suffix form; minor-additions bullet (:51) |
| edge-cases | F-9 | Unbounded rows (a) / version skew (b) | CLOSED | (a) dispositioned § Deferred (P2+) (:205) with rationale; (b) § Design 6 (:138) `sync.py install` sentence |
| edge-cases | F-10 | Render columns are sub-parses / resolved rows | CLOSED | § Design 5 (:131) severity-and-scope sub-parse rule; resolved-row half dispositioned § Deferred (P2+) (:206) |
| edge-cases | F-11 | Anchor disagreement (P4) | CLOSED | single `:435-441` in all three places |
| conventions | F-1 | Which of R1–R5 ship as SKILL.md prose; R3 vs row 5 | CLOSED | § Design 2 (:95) names R1/R2/R3/R5 as prose and R4 at Phase 1; R5 marked "Author-facing" (:101); row 5 recalibrated (:160) |
| conventions | F-2 | R2 contradicts Design 5; renamed section unfixable | CLOSED | R2 (:98) reads allowed + `(re-anchored round <n>)` allowance; mirrored in § Design 7 block (:146). Round-4 interaction is a new collision — F-2 below |
| conventions | F-3 | `grep -c 'DEFERRED, or NEW'` cannot match | CLOSED | row 6 (:161) now asserts the bare token, "0 today in all four" (verified) |
| conventions | F-4 | Two anchors for the round-4 sentence | CLOSED | `:435-441` everywhere |
| conventions | F-5 | Design 3 emits two out-of-vocabulary manifest forms | CLOSED | § Design 4 (:113) carries both the `(recount: …)` suffix and the revert line into the 2b prose; § Design 7 item 1 (:142) carries the consumer half |
| conventions | F-6 | `spec-workflow-reference.md` reconciliation under-scoped | CLOSED | § Scope last row (:21) — `:88` gains `DEFERRED` **and** the every-round sentence; row 10 (:165) |
| conventions | F-7 | `routing violation: D-<n>` mandated title | CLOSED | minor-additions bullet (:51) records the fixed prefix and that nothing parses it |
| conventions | F-8 | Row 3 parenthetical names three of four sites | CLOSED | row 3 (:158) now "≥ 4" with all four named |

No REOPENED items. The single PARTIAL (correctness/F-10) is a P3 whose residue is covered by F-1 below.

## Findings

### F-1: Checklist row 8's `Follow-up: unfiled` assertion is falsified by the row shape the same spec prescribes
**Severity:** P1
**Where:** spec.md:163 (§ Test plan row 8) vs spec.md:92 (§ Design 2 row shape); § Done when criterion 2 (spec.md:180)
**Convention violated:** The repo's recorded prose-spec gate practice — "re-verify backtick phrases with `grep -cF`" (MEMORY `project_prose_spec_gate_script_pitfalls`) — and the spec's own § Test plan preamble, which restates it. This is the same class as round-2 correctness/F-3, which the spec accepted and fixed for row 5.
**Evidence:** Row 8 asserts `grep -cF 'Follow-up: unfiled' skills/spec-cycle/SKILL.md` **≥ 2**, with the parenthetical "(row shape, render example)". The row shape at `:92` is `**Follow-up:** unfiled` — every field in the block uses the `**Label:**` bold form. `-F` is a fixed-string match, so the shape line does not contain the literal. Verified empirically:

```
$ printf '%s\n' '**Follow-up:** unfiled' | grep -cF 'Follow-up: unfiled'
0
```

Only the render example at `:127` (`— Follow-up: unfiled`) carries the literal, so the post-edit count is **1**, not ≥ 2, and the row fails on a correct implementation. The two ways out are both bad and both undocumented: chase a phantom regression, or drop the bold markers from the row shape — which would silently change the field syntax that § Design 7's well-formedness check reads. This is also load-bearing beyond the row: § Done when criterion 2 ("Deferred entries that become tickets carry the ticket id") maps to "Checklist rows 4 (Phase 1 hunk), 8", and row 8 is the only assertion that touches the `Follow-up:` field at all — round-2 correctness/F-10 asked for exactly this row and it landed in a form that cannot pass.
**Suggested fix:** Assert the bold form, matching the shape block: `grep -cF '**Follow-up:** unfiled' skills/spec-cycle/SKILL.md` → 1 (row shape) **and** `grep -cF '— Follow-up: unfiled' skills/spec-cycle/SKILL.md` → 1 (render example). Or, in one row, `grep -c 'Follow-up:\*\{0,2\} unfiled' skills/spec-cycle/SKILL.md` → 2. Same care applies to any future assertion over a `**Label:**` field.

### F-2: At round 4, D15's append-only FROZEN rule and R2's repair/re-anchor carve-out give the author contradictory mandates
**Severity:** P2
**Where:** spec.md:48 (D15), spec.md:74 (§ Design 1 "Round 4"), spec.md:98 (R2), spec.md:67 (§ Design 1 step 3)
**Convention violated:** Cross-surface completeness — the spec's own D11 rationale (a producer rule and its consumer rule are edited together) and the supersede-and-state discipline the wiki applies (`decisions/2026-08-09-review-round-artifacts-are-immutable.md`: never leave the record disagreeing with itself). This is the round-4 half of my round-2 F-2, whose suggested fix asked to "note the re-anchor in D15 as the round-4 case"; the rounds-1–3 half is closed, and the collision itself is new because both rules changed this round.
**Evidence:** R2 (`:98`) grants the skill exactly two edits to an existing row — repairing the field a `routing violation: D-<n>` finding names, and re-anchoring `Where` / `Propagation sites` after a rename — with no round qualifier. D15 (`:48`) now says the section is FROZEN, "its preamble and every existing row are copied verbatim and no REWRITE section may modify it — with one permitted edit: appending a row routed in this round, which needs no promotion." D15 also states that routing runs at round 4. Walk it: round 4's reviewers file `routing violation: D-<n>` against a malformed row; § Design 1 step 3 routes it (one site — the row) to **fold**, and step 4 says "edit every listed site"; D15 permits only an append. The author must break one of two mandatory rules. The "needs no promotion" clause implies other edits *would* be promotable under the untouched protocol at `SKILL.md:442-445`, but D15's "copied verbatim … no REWRITE section may modify it" reads the other way, and the spec never says which. The same collision blocks re-anchoring a row whose target section the round-4 REWRITE just renamed. The consequence is bounded — round 4 halts red either way, and the next invocation's round 1 can repair the row under R4's preservation rule — which is why this is P2 and not the P0 its rounds-1–3 twin was.
**Suggested fix:** One clause in D15 and its § Design 1 "Round 4" mirror: "R2's two row edits — repairing the field a `routing violation: D-<n>` names, and re-anchoring `Where` / `Propagation sites` after a round-4 rename — are permitted at round 4 alongside the append and need no promotion; the finding record is still never rewritten." Alternatively state the opposite explicitly ("neither repair is available at round 4; the row is repaired on the next invocation's round 1") so the author has a rule instead of a choice.

### F-3: Rows 5 and 9 assert wrap-sensitive counts and phrases where the repo's recorded practice is a region assertion
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:160 (row 5), spec.md:164 (row 9), against spec.md:154 (§ Test plan preamble)
**Convention violated:** MEMORY `project_prose_spec_gate_script_pitfalls` — "assert hunk regions not counts" — which the spec's own preamble restates ("Assert hunk regions, not counts"), and which round-2 conventions/F-3 already had to invoke once for row 6.
**Evidence:** Row 5 pins `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → 8, on the reasoning that rule R3 adds exactly one line. R3's text carries the literal **twice** in one sentence ("A row is not a `## Deferred (P2+)` entry and is never a 2g candidate; 2g reads only `## Deferred (P2+)`, by exact heading"). `grep -c` counts matching *lines*: if the implementer wraps R3 at the ~72-column width used in the neighbouring round-4 block (`SKILL.md:435-464`), the two occurrences land on separate lines and the count is 9, not 8 — the same wrap failure that killed row 6 last round, in the same file. (The adjacent 2e bullets at `:428-432` are unwrapped, so the outcome depends entirely on an unstated formatting choice.) Row 9's `grep -cF 'is FROZEN with one permitted edit'` is a six-word phrase with the same exposure. Row 5's own text already concedes the point — "row 4's region assertion is what proves no existing line moved" — so the count adds risk without adding coverage, which is precisely the trade the recorded practice resolves.
**Suggested fix:** Replace row 5's count with the region assertion it defers to: "no `git diff -U0` hunk covers `:371`, `:411-424`, `:431`, or `:593-624`; the `Deferred (P2+)` machinery is untouched" (row 4 already asserts most of this — add `:371`). For row 9, assert an unwrappable token instead: `grep -cF 'is FROZEN' skills/spec-cycle/SKILL.md` → 1. If a phrase must be pinned, say so and use the multiline form the preamble's Git-Bash note already anticipates.

### F-4: Row 10 pins a literal in `docs/spec-workflow-reference.md` that no Design section mandates
**Severity:** P3
**Where:** spec.md:165 (row 10) vs spec.md:21 (§ Scope, reference row)
**Convention violated:** The producer/consumer pairing the spec applies everywhere else — every other checklist literal is quoted verbatim in a Design section (row 9's FROZEN sentence in § Design 1, row 8's preamble in § Design 2, row 6's block title in § Design 7).
**Evidence:** Row 10 requires `grep -cF 'including round 1' docs/spec-workflow-reference.md` → 1. The Scope row that authorizes the edit says only that `:88`'s paragraph "gains `DEFERRED` in the status set and one sentence stating the every-round deferral check" — no wording is given, and no Design section carries the sentence. An implementer who writes "in every round, round 1 included" satisfies the design and fails the gate. Verified: `docs/spec-workflow-reference.md:88` contains no such phrase today, and its paragraph is round-scoped ("Round 2+ closure tracking").
**Suggested fix:** Quote the sentence in the § Scope row (or a one-line Design 7 addendum), e.g. "In every round, including round 1, each reviewer also checks the spec's `## Deferred — follow-up required` rows for well-formedness and does not re-file a finding whose root a well-formed row already carries" — then row 10's literal is anchored to text the spec actually specifies.

### F-5: Three sections claim "the end of the spec" and the render has no section terminator
**Severity:** P3
**Where:** spec.md:78 (§ Design 2, "a spec section at the end of the spec"), spec.md:131 (§ Design 5 extraction rule), against `skills/spec-cycle/SKILL.md:431` and `:611-623` (2g)
**Convention violated:** Reuse-and-disambiguate: `## Deferred (P2+)` (`SKILL.md:431`) and `## Post-green polish` (`:620`) are both already specified as living "at the end of the spec", and brief Decision 5's whole rationale is that the two Deferred sections must be unambiguously distinguishable.
**Evidence:** § Design 5's rewritten locator is "every `###`-or-deeper heading **inside the section**", but nothing defines where the section ends. With `## Deferred (P2+)` placed after `## Deferred — follow-up required` (a legal layout — both are "at the end"), a render that does not stop at the next `##` sweeps up 2g's P2 entries; a render that stops at the first blank line finds nothing. Rule R3 fences the two headings for *matching* ("headings are matched exactly") but says nothing about ordering or extent. The failure is silent in exactly the direction § Design 6 names as the one thing this report exists to prevent.
**Suggested fix:** One clause in § Design 5: "the section runs from its heading to the next `##`-level heading or EOF; every `###`-or-deeper heading in that span is a row." Optionally pin the order in § Design 2: "placed immediately before `## Deferred (P2+)` when both are present."

### F-6: "immediately under the heading" invites a false preamble P0
**Severity:** P4
**Where:** spec.md:146 (§ Design 7 block) vs spec.md:81-83 (§ Design 2 shape)
**Convention violated:** Reviewer-literalism hygiene — the oscillation class this ticket exists to end.
**Evidence:** The block instructs every lens: "The section must carry its fixed preamble line **immediately under the heading**; if it does not, file a P0 titled `routing violation: missing preamble`." The shape block at `:81-83` shows heading → blank line → blockquote, which is the only valid markdown. It is also unstated whether the check is on exact text or on presence, so a paraphrased-but-equivalent fence is adjudicated differently by different lenses — on a rule whose only failure mode is a P0.
**Suggested fix:** "…must carry its fixed preamble line as the first non-blank content under the heading; check for the sentence's substance, not byte-equality — a section with no fence at all is the violation."

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=2 P3=2 P4=1
