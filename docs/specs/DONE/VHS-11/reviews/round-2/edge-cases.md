# Edge-Cases Review — round 2

**Grounding notes:** All anchors the revised spec cites verify against current files at HEAD `27d8f26` (most recent commit touching any target file; no shifts in the last 7 days): SKILL.md `:23/:96/:101/:107/:144/:142–152/:147/:172–174/:181/:277–283/:285–293`; agent `**Severity:**` lines at `correctness.md:146` / `edge-cases.md:141` / `conventions.md:135`; closing fences at `:160/:156/:149`; `round_number` input lines at `:16/:16/:18`. Grep confirms exactly two "step 6" cross-references (`SKILL.md:107`, `:147`) and six "continue to step 5" lines (`:36/:42/:56/:70/:76/:95`) — the spec's renumbering edit set is complete. Every closure-manifest claim verified against the current spec text and the target files' line anchors.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | D1 fallback references `origin/<branch>` | CLOSED | 5c binds `<cmp>` (spec.md:104–114); 5d/5e use `origin/<cmp>` (spec.md:118, 126); ff offer restricted to counterpart comparison, fallback informational-only with own token (spec.md:124–132); Decision 1 (spec.md:40) |
| correctness | F-2 | D5 defining-sentence anchor self-contradictory | CLOSED | Re-anchored "immediately after the template's closing code fence, before the 'last non-blank line' paragraph" with anchors `:160/:156/:149` (spec.md:310) — all three verified as the actual closing fences |
| correctness | F-3 | 2g move-out-of-Deferred references absent state | CLOSED | 2g steps 2–4 create-section/entry-if-absent and record-remaining mechanics (spec.md:206–218); intro names the green-round carry-forward (spec.md:195–197) |
| correctness | F-4 | Done-when 2 elides token-vocabulary supersession | CLOSED | "(seven-token vocabulary per § D1 rationale, superseding the brief's four-token list)" (spec.md:371) |
| correctness | F-5 | Misenumerated "continue to step 5" sub-steps | CLOSED | "all six occurrences: 4a/4b/4d/4e/4f/4g — SKILL.md:36, 42, 56, 70, 76, 95" (spec.md:66) — matches grep |
| correctness | F-6 | "Only working-tree mutation" literally false | CLOSED | "lone git-level mutation of existing tracked files" (spec.md:75, 329–331) |
| edge-cases | F-1 | `<branch>` binding breaks on fallback path | CLOSED | Same root as correctness/F-1; `<cmp>` binding + informational fallback (spec.md:97–132) |
| edge-cases | F-2 | 2g assumes Deferred entries exist on green round | CLOSED | 2g rewritten source-agnostic; performs green-round carry-forward itself (spec.md:191–219); 2d advisory names 2g as carrier (spec.md:224) |
| edge-cases | F-3 | No post-update re-validation after ff | CLOSED | 5e on-update branch: re-confirm brief, re-read CLAUDE.md, halt-and-ask if spec output path arrived (spec.md:152–157) |
| edge-cases | F-4 | Non-final-round tagged P2s silently dropped | CLOSED | 2g step 1: "from **all rounds'** persisted reports — not only the final round's" + dedup/already-addressed handling (spec.md:199–203) |
| edge-cases | F-5 | Manifest undefined for synthetic missing-STATUS P0 | CLOSED | `<lens>/STATUS (P0) "missing STATUS line"` notation, reconciles with gate arithmetic (spec.md:286–290) |
| edge-cases | F-6 | Exit-code conflation in 5e; no 5d failure token | CLOSED | Step-level catch-all (spec.md:76–78); exit 1 vs exit > 1 split in 5e (spec.md:162–170) |
| edge-cases | F-7 | Regex rejects digit-bearing prefixes | CLOSED | `^[A-Z][A-Z0-9]*-[0-9]+` with WEB3-12 rationale (spec.md:242–244); Done-when 5 annotated (spec.md:374) |
| edge-cases | F-8 | Transcript covers only happy ff path | CLOSED | Test-plan item 9: ff-success, diverged, ff-abort, attached at ship time (spec.md:362) |
| edge-cases | F-9 | Enumeration omits 4e/4g | CLOSED | spec.md:66 (same as correctness/F-5) |
| edge-cases | F-10 | `brief_path` "verbatim" — normalization unstated | CLOSED | Normalized project_root-relative forward-slash form defined in step 1 (spec.md:232–234) and used in 2b (spec.md:267–269) |
| conventions | F-1 | `closure_manifest` not mirrored into agent input contract | CLOSED | D4 edit 3 adds identical line to all three inputs blocks after `round_number` (spec.md:296–300) |
| conventions | F-2 | D5 anchor self-contradictory | CLOSED | Same as correctness/F-2 (spec.md:310) |
| conventions | F-3 | Decision 4 overstates "never moved or renamed" | CLOSED | Scoped: out-of-tree never moved; in-tree subject to step 2's rename flow (spec.md:52) |
| conventions | F-4 | customizing.md goes silently stale | CLOSED | In scope table (spec.md:20) + concrete edit text in D3 (spec.md:261) |
| conventions | F-5 | Token vocabulary expanded beyond brief | CLOSED | Deferred entry with disposition (spec.md:393) + Done-when 2 annotation |
| conventions | F-6 | Fetch-before-resolve ordering deviation | CLOSED | Decision 2 rationale (spec.md:44) + Deferred entry (spec.md:394) |
| conventions | F-7 | Enumeration incomplete | CLOSED | spec.md:66 |
| conventions | F-8 | HTML comment in template line | CLOSED | Template line is bare `**Pre-ship recommended:** yes` (spec.md:307) |
| conventions | F-9 | `git rev-parse` absent from Tool-use bullet | CLOSED | Listed in D6 read-only set (spec.md:327) |

The closure manifest's four P0/P1 claims all verify; no REOPENED, no PARTIAL.

## Findings

### F-1: 2g's hard limits do not protect Done-when — a post-green "wording" clarification can rewrite acceptance criteria
**Severity:** P3
**Where:** spec.md:210–213 (§ D2, 2g step 3)
**Edge case:** a reviewer tags a P2 `Pre-ship recommended: yes` whose suggested fix rewords a Done-when bullet (precisely the edit class this spec itself performed twice — Done-when 2's and 5's annotations).
**What happens:** Step 3's allowed categories ("wording, file:line anchors, examples, error-message text, checklist rows") admit Done-when edits, and the hard-limit list protects only "the spec's Decisions or Out-of-scope sections." A Done-when rewording after the green verdict changes the contract ship-spec implements against and the criteria Phase 3's drift-check diffs against the brief — with no re-review, by design (2g step 5). Partially mitigated: Phase 3 still renders the brief-vs-spec Done-when mapping for the human, so drift is visible-if-looked-at rather than invisible. Degrades semi-gracefully → P3.
**Why the spec misses it:** The hard limits were written against the scope-creep risk (brief Risks §2: "no behavior reversals, no new scope") and enumerate the two sections that encode decisions/fences — Done-when encodes the acceptance contract but isn't named.
**Suggested fix:** Extend 2g step 3's hard limits: "no edits to the spec's Decisions, Out-of-scope, or Done-when sections (Done-when may gain parenthetical annotations only, never reworded criteria)."

### F-2: Step 1 normalization is undefined for a brief path outside `project_root`
**Severity:** P3
**Where:** spec.md:232–238 (§ D3, step 1 replacement text)
**Edge case:** user invokes `/spec-cycle` with an absolute path outside the repo (`C:\elsewhere\PROJ-9-notes.md`) or a `../`-escaping relative path. The tolerance text scopes alternates to "anywhere **in the repo**," but no branch defines what happens when the resolved path is not under `project_root`.
**What happens:** "Normalize it to a project_root-relative path with forward slashes" is impossible (or yields a `../`-prefixed escape). Step 2's existence check still passes (the file exists), so the skill proceeds and 2b hands the unnormalizable path to three subagents whose cwd resets between calls and whose sandboxed read scope may not include out-of-root paths. Each agent records a blocked grounding step as a finding and continues — three degraded reviews in one round, the exact convergence-signal pollution items 1 and 4 exist to prevent. Same blast radius as round-1 F-10, surviving through the gap that F-10's fix only covered in-repo forms.
**Why the spec misses it:** The round-1 fix defined the normalized form but not the precondition for it; "anywhere in the repo" implicitly excludes out-of-repo without saying what the skill does when the implicit precondition is violated.
**Suggested fix:** One sentence in step 1: "If the resolved path is not under `project_root`, halt and ask the user to either move the brief into the repo or confirm proceeding — on confirm, pass the absolute path in 2b and note that reviewer access to out-of-root paths is host-dependent."

### F-3: Done-when 1 elides the diverged carve-out — "behind-count > 0 produces … an explicit user choice" is false on the diverged path
**Severity:** P3
**Where:** spec.md:370 (Done-when 1) vs spec.md:162–167 (D1 5e diverged branch) and spec.md:40 (Decision 1)
**Edge case:** ship-time checklist evaluation (or an implementer cross-checking Done-when against D1) on the diverged-counterpart path: behind-count > 0, warning emitted, no choice offered — by explicit Decision 1 design.
**What happens:** A literal Done-when 1 check fails for a behavior the spec's own Decision 1 mandates. Worst realistic outcome: an implementer "fixes" D1 to always offer the choice in order to satisfy Done-when 1, reintroducing the offer-on-diverged path Decision 1 forbids. Same divergence-elided-in-Done-when class as round-1 correctness/F-4, which Done-when 2's annotation pattern already established the fix shape for.
**Why the spec misses it:** Done-when 1 was inherited from the brief's first bullet (which carries the same elision); the round-1 revision annotated Done-when 2 and 5 but not 1.
**Suggested fix:** Qualify Done-when 1: "…produces a warning and an explicit user choice (ff-only update / proceed) **when fast-forward is feasible; diverged → warn-only, no offer, per Decision 1**."

### F-4: D6 failure-modes bullet over-claims the catch-all — "any other git failure in step 5 maps to `skipped (git error)`" contradicts the ff-abort token
**Severity:** P4
**Where:** spec.md:338–341 (D6 first new bullet) vs spec.md:157–160 (D1 5e ff-abort) and spec.md:344–346 (D6 second new bullet)
**Edge case:** user-confirmed ff merge aborted by git — a git failure inside step 5 whose token is `behind-N (update failed — proceeded)`, not `skipped (git error)`.
**What happens:** The normative D1 catch-all is correctly qualified ("not handled by an explicit branch below," spec.md:76–77), but the advisory bullet drops the qualifier, so the two new failure-mode bullets disagree with each other about which token the ff-abort maps to. A future debugger reading only `## Failure modes` would grep logs for the wrong token. Degrades gracefully — D1 is unambiguous and bullet 2 names the real behavior.
**Suggested fix:** Mirror the qualifier in bullet 1: "any other git failure in step 5 **not handled by an explicit 5e branch** maps to `origin: skipped (git error)`."

### F-5: 2g "runs exactly once" has no run marker — interrupted-session re-entry duplicates bookkeeping
**Severity:** P4
**Where:** spec.md:193 (§ D2, 2g intro) and spec.md:215–218 (step 4)
**Edge case:** session interrupted between 2g step 3 and step 4 (or user asks to re-run after a partial polish); the resumed operator re-executes 2g.
**What happens:** Candidates are re-collected and re-applied (mostly idempotent for wording edits), but step 4's record-keeping appends — duplicate lines in `## Post-green polish` and duplicate `## Deferred (P2+)` entries. Human-visible markdown duplication, no data loss → P4.
**Suggested fix:** One sentence in 2g's intro: "If a `## Post-green polish` section already exists in the spec, treat 2g as already-run: reconcile (merge/dedup) rather than append."

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 3 | P4: 2

STATUS: GREEN
