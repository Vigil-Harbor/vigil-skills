# Correctness Review — round 2

**Grounding completed.** Spec (`docs/specs/TODO/VHS-37.spec.md`) and brief re-read from disk. Plane VHS-37 retrieved from namespace `skills` (tag-exact, confidence 1.00) — the ticket's framing ("valid, out of scope, non-trivial = follow-up ticket and deferred") is the earlier, narrower rule; the brief's Decision 2 ceiling is the later 2026-09-08 refinement and the spec follows the brief, which is correct. `CLAUDE.md` read (gitignored machine-local pointer) and `AGENTS.md` read as the canonical instructions.

Every anchor in the spec's Scope table re-verified against `main` at `124700b`: `SKILL.md:294-296` (Phase 1 opening — heading at 294, `Output path:` at 296) ✓; `:365-368` (2b example block) ✓; `:378-383` (disposition-phrase prose, `fixed:`/`reworked:`/`not applicable:` at 380-383) ✓; `:411-424` (2d) ✓; `:426-464` (2e, rounds 1–3 at 428-432, round 4 at 434-464) ✓; `:436-441` / `:438-441` (see F-4) ✓; `:446-462` (closed-issues manifest) ✓; `:466-487` (2f halt) ✓; `:489-591` (2f-i, step 5 re-render at 555-557) ✓; `:593-624` (2g, "already exists" idiom at 599-601) ✓; `:626-659` (Phase 3 block) ✓; `:685-` (Failure modes) ✓. Agents: `closure_manifest` at `correctness:18`, `edge-cases:18`, `conventions:20`, `scalability:18` ✓; status enumeration at `correctness:38-39`, `edge-cases:38-39`, `conventions:43-44`, `scalability:30` ✓; "REOPENED items are P0" at `scalability:40` ✓; output contracts start at `correctness:138`, `edge-cases:133`, `conventions:127`, `scalability:76` ✓. `docs/spec-workflow-reference.md:84` ("Address every P0 and P1.") and `:88` (status set) ✓. Grep baselines: `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → **7** ✓; `grep -rn 'Deferred' skills/spec-close/SKILL.md skills/ship-spec/SKILL.md` → 0 ✓; `grep -n 'Address every P0 and P1' skills/spec-cycle/SKILL.md` → one hit (`:430`) ✓. `lint.py`'s only ERROR rules are `requires-malformed` and `operative-tool-call` (an unfenced `mcp__*` name) — nothing the new prose triggers, so checklist row 1 is sound. `sync.py push --dry-run` is a valid invocation (`sync.py:209`) ✓.

**git log (7-day window):** `ea5c2b0`, `ecdfefe`, `c97d4ad` all landed 2026-09-07. The spec's Scope note names `ecdfefe`/`c97d4ad` and the 2f-i re-verification ✓. `ea5c2b0` additionally touched `docs/spec-workflow-reference.md` — but at `:31,:35`, not the `:84`/`:88` lines this spec edits, so the new Scope row is not planning around shifted text.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | manifest disposition phrase declared vs exampled | CLOSED | one canonical `deferred: D-<n> (§ Deferred — follow-up required)` at spec:68 (Design 1 step 4), :113 (Design 4 prose), :116 (example); id forms reconciled in D13 (:46) |
| correctness | F-2 | no-re-file rule unreachable on round 1 | CLOSED | ungated "Deferred findings (every round, including round 1)" block between steps 6 and 7, spec:144-146; Scope row :20 |
| correctness | F-3 | Phase 1 does not preserve the section on a re-run | CLOSED | rule R4, spec:100; Scope row :15; cited in Done-when 2 (:180) |
| correctness | F-4 | revert collides with round-4 closed-issues + "do not delete history" | **PARTIAL** | D16 (:49) removes only the round-4 revert; a round-2/3 revert still leaves a CLOSED entry that the untouched `:446-462` collects as a regression constraint — see F-1 below. "Do not delete history" tension unaddressed in text |
| correctness | F-5 | stale closure-status enumeration | CLOSED | Design 7 item 3 (:148), Scope row :20, checklist row 6 (:161) |
| correctness | F-6 | test row 4 under-describes the 2b diff | CLOSED | row 4 names `:365-368` and `:378-383` (:159); Scope row :16 names both |
| correctness | F-7 | ceiling turned into mandate | CLOSED (deliberate) | recorded not-applied in § Deferred (P2+) :201; Decision 2 restatement :32 owns the hardening |
| correctness | F-8 | reject evaluated last | CLOSED | step 0 "Test validity", spec:60 |
| correctness | F-9 | no push round-trip row | CLOSED | checklist row 2 (:157) |
| correctness | F-10 | verbatim Suggested fix reaches /ship-spec | CLOSED | preamble :83, Design 6 :138, checklist row 8 :163 |
| correctness | F-11 | row 3's ≥3 justification | CLOSED | re-justified at :158 (2e definition and shape, D15 sentence, Failure-modes bullet) |
| correctness | F-12 | halt-and-narrow has no mechanism | CLOSED | advisory wording :67, Out of scope 8 :197, minor-additions :51 |
| correctness | F-13 | two commits touched SKILL.md | CLOSED | Scope note :11 names `ecdfefe`, `c97d4ad`, VHS-27 |
| correctness | F-14 | scalability contract omitted from the fence | CLOSED | `scalability:76-118` added at :23 |
| edge-cases | F-1 | acceptance rule unreachable (re-run r1, round-4 rows) | CLOSED | ungated block :146; D15 (:48) states round-4 rows are verified on the next invocation's round 1 |
| edge-cases | F-2 | no severity carve-out on root suppression | CLOSED | D14 (:47) + block's in-scope-P0 exception (:146) — residual ambiguity filed as F-6 below (P2) |
| edge-cases | F-3 | additive fixes undeferrable | CLOSED | `(new)` marker at :61, :90, :146 |
| edge-cases | F-4 | round-4 protocol collision | **PARTIAL** | FROZEN/REWRITE exemption closed (D15 :48); round-4 revert closed (D16 :49); the sub-case "the fold has since been overlapped by a later edit" is still absent from Design 3's fallback list (:109) — see F-2 below |
| edge-cases | F-5 | per-run round numbers / shared reviews tree | CLOSED | D13 (:46) makes `D-<n>` the sole key; D16 "No round directory is scanned" (:49); Design 3 reads this-invocation manifests only (:105); R1 continues from highest (:97) |
| edge-cases | F-6 | section not marked non-normative | CLOSED | fixed preamble :83; Design 6 :138; checklist row 8 :163 |
| edge-cases | F-7 | example phrase ≠ verified form | CLOSED | same canonical phrase as correctness/F-1 |
| edge-cases | F-8 | render must parse rows it is told not to parse | CLOSED | extraction rule with `?` / malformed-row handling, :131 |
| edge-cases | F-9 | heading prefix-confusable | CLOSED (deliberate) | § Deferred (P2+) :202; Decision 5 (:35) and rule R3 (:99) pin exact-heading matching — note R3's text is the subject of F-3 below |
| edge-cases | F-10 | routing runs inside 2f-i step 4 | CLOSED | spec:70 and minor-additions :51 |
| edge-cases | F-11 | test-plan gaps (em dash, row 3, behavior rows) | CLOSED | Test-plan preamble :154 (Git Bash, hunk regions, line shifting, `grep -cF` re-verify); row 3 re-justified :158 |
| conventions | F-1 | suppression broader than the brief authorizes | CLOSED | promoted to D14 with rationale, root definition, P0 exception (:47); Decision 1 amended (:31) |
| conventions | F-2 | round-4 rule is a silent addition outside Scope | CLOSED | D15 (:48); Scope row extended to `:426-464` naming the qualified sentence (:17); row 4 covers the range (weakly — see F-10) |
| conventions | F-3 | two `deferred:` strings | CLOSED | one canonical phrase carrying the § anchor 2b requires |
| conventions | F-4 | spec-workflow-reference not reconciled | CLOSED | Scope row :21, checklist row 10 :165 |
| conventions | F-5 | "eight fields" vs seven labels | CLOSED | seven fields everywhere (:146, D11 :44) |
| conventions | F-6 | fifth status without amending the enumeration | CLOSED (partly deliberate) | enumeration gains `DEFERRED` (:148); the illustrative example row is explicitly not required, recorded at :203 |
| conventions | F-7 | severity ladder inverted on routing violations | CLOSED | routing violations are P0 (:146) |
| conventions | F-8 | scope adjudication diluted across lenses | CLOSED | D17 (:50) + one sentence in the block (:146) |
| conventions | F-9 | two finding-id forms | CLOSED | D13 (:46) — but Design 3's extra manifest line reopens the round-scoping premise; see F-7 below (P2, new variant) |
| conventions | F-10 | roll-up of unflagged additions | CLOSED | minor-additions bullet :51 |
| conventions | F-11 | round dirs read as current state | CLOSED | D16 "No round directory is scanned" (:49); Design 3 keyed on this-invocation manifests (:105) |
| conventions | F-12 | Scope table says one paragraph per agent | CLOSED | "Three edits each" (:20) |

**Manifest-claim check.** All fifteen closure-manifest claims verified against the spec text; one wording discrepancy: the manifest describes D16 as "revert only for a fold made in rounds **2–3** of this invocation", while the spec's D16 headline (:49) says "rounds **1–3**" and Design 3 (:109) actually gates on the *current* round being 2 or 3. The operative rule is Design 3's; D16's headline describes the wrong axis (a round-3 fold recounted at round 4 would, on the headline's plain reading, be revertible — which D16's own body forbids). Folded into F-8's suggested fix.

## Findings

### F-1: A revert in rounds 2–3 leaves a stale CLOSED entry that round 4 turns into a regression constraint
**Severity:** P1
**Where:** spec § Design 3 (:105-109), § Decisions D16 (:49), § Scope "Left alone" (:23)
**Claim:** "True count now two or more, and the original finding is not an in-scope P0, and this is round 2 or 3 → **revert the original fold** (remove the edit from every site it touched) and defer both findings as two rows." And, in Scope: the "round-4 closed-issues manifest (`:446-462`)" is left byte-identical.
**Why this is wrong:** D16 removed the *round-4* revert, but not the collision. Walk the sequence: finding X is filed in round 1 and folded in the round-1 revise; round 2's reviewers write closure tables marking X **CLOSED** with the fold as evidence (persisted in `round-2/*.md` by 2c, `SKILL.md:390-397`); in the round-2 revise a new finding lands on that section, the recount fires, and Design 3 orders the fold reverted. Nothing rewrites round 2's persisted closure table. At round 4 the untouched manifest builder — "scanning every reviewer report present in each round's directory … collecting every finding whose status resolved to CLOSED in a later round's closure table" and "Every entry is a regression constraint: the rewritten spec must preserve the fix that closed it" (`skills/spec-cycle/SKILL.md:446-461`) — still collects X and instructs the round-4 author to preserve a fix that was deliberately removed and replaced by row `D-<n>`. The author either reinstates the multi-site fold the routing step exists to avoid, or silently violates a rule the spec declares unchanged. D16 (:49) cites `:446-462` only as the rationale for forbidding a *round-4* revert; it never addresses an entry produced by an earlier-round one. This is the unclosed half of round-1 correctness/F-4 (its suggested fix (a)).
**Suggested fix:** One clause in Design 3's fallback list or in D16: "A revert supersedes the reverted finding's closed-issues-manifest entry: at round 4 the entry's constraint is the deferral row `D-<n>` (the row stays), not the removed fix. Because `:446-462` is unchanged, the substitution is stated here, in the routing text the round-4 author also reads." Land it in the same Design 3 bullet as F-2's fix — one propagation site.

### F-2: "Revert the original fold" is undefined once a later round has re-edited the site
**Severity:** P1
**Where:** spec § Design 3 (:108-109)
**Claim:** "**revert the original fold** (remove the edit from every site it touched)"; the fallback branch fires only "(count still one; or an in-scope P0; or round 4; or the fold predates this invocation)".
**Why this is wrong:** With reverts now bounded to rounds 2–3, the overlap case is still reachable: a fold in the round-1 revise, a different finding's fold re-editing the same section in the round-2 revise, and a recount ordering the round-1 revert in the round-3 revise. "Remove the edit from every site it touched" has no defined meaning once the text has been rewritten — and 2e's untouched bullet "Do not delete history of what changed; … the spec at end of round must stand on its own" (`SKILL.md:432`, listed byte-identical at spec:23) gives the author no tie-breaker. Round-1 edge-cases/F-4 raised exactly this ("Design 3 is additionally undefined when a later round's fold overlapped the text being reverted") and its suggested fix (c) was not carried into the fallback list.
**Suggested fix:** Extend the fallback branch: "…or the site has been re-edited by a later round's fold — revert is not available; fold once more with the corrected site list and record the recount." One sentence, same bullet as F-1's fix.

### F-3: Checklist row 5's "7 before and after" is falsified by rule R3, which the design ships into the same file
**Severity:** P1
**Where:** spec § Test plan row 5 (:160) vs § Design 2 rule R3 (:99)
**Claim:** Row 5: "`grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` is 7 before and after." Design 2: "Rules stated with the shape: … **R3.** A row is not a `## Deferred (P2+)` entry and is never a 2g candidate; 2g reads only `## Deferred (P2+)`, by exact heading."
**Why this is wrong:** The current count is exactly 7 (verified). R3 is normative text in the 2e insertion — Decision 5 (:35) and the § Deferred (P2+) entry for edge-cases/R1/F-9 (:202) both point at R3 as the place the exact-heading fence is *stated*, so it has to ship into `SKILL.md`. Its one line contains the literal, taking the count to 8. The implementer therefore runs a row that must fail on a correct implementation, and the two ways out are both bad: chase a non-existent regression, or reword R3 to drop the literal — which silently un-closes edge-cases/R1/F-9, the finding R3 exists to close. The row's real intent (the `## Deferred (P2+)` machinery is untouched) is already covered by row 4's hunk-region assertion.
**Suggested fix:** Restate row 5 as "8 after (7 before): the single new line is rule R3's reference; no existing `Deferred (P2+)` line is edited — confirm with `git diff -U0` that no hunk covers `:424`, `:431`, or `:593-624`." Or drop row 5 and rely on row 4.

### F-4: D15 anchors the qualified sentence at `:438-441`; Scope and Design 1 anchor it at `:436-441`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions D15 (:48) vs § Scope row 3 (:17) and § Design 1 "Round 4" (:74)
**Claim:** D15: "The sentence at `:438-441` gains that qualification." Scope: "one sentence qualifying the FROZEN/REWRITE enumeration at `:436-441`". Design 1: "The sentence at `:436-441` gains that qualification."
**Why this is wrong:** In the current file the enumeration instruction spans `:435-437` ("Enumerate every section of the spec … For each, decide:") and the two definitions span `:438-441` (FROZEN at 438-439, REWRITE at 440-441). Neither cited range is the enumeration sentence; `:436-441` straddles half of it plus both definitions, `:438-441` is the definitions only. Three citations of one edit site, two of them disagreeing, is the exact drift class this spec's own D14 rationale describes.
**Suggested fix:** Use one range in all three places — `:435-441` (the enumerate-and-classify bullet as a whole), and say the added sentence follows the REWRITE definition at `:441`.

### F-5: One malformed row produces two P0 findings per lens
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 item 2 (:146) and item 3 (:148)
**Claim:** Item 2: "A row that is not well-formed … is a routing violation: file it as a P0 finding titled `routing violation: D-<n>`." Item 3: "A `deferred: D-<n>` disposition is satisfied when row `D-<n>` is well-formed …; mark the finding `DEFERRED`. Otherwise it is unsatisfied and the finding is REOPENED."
**Why this is wrong:** When a malformed row also carries a manifest line, both rules fire on the same defect: the reviewer files a P0 routing violation *and* reopens the original finding, which "REOPENED items are P0" (`agents/spec-reviewer-correctness.md:51-53`) makes a second P0. Up to four lenses run the same block, so a single missing field can add 8 to `total_p0p1`. Decision 1 (:31) stakes the design on the gate number meaning "the number of live findings that are not deliberately deferred"; double-counting one defect contradicts that, and it re-creates the oscillation the ticket exists to end (the author fixes the field, and both findings must be dispositioned).
**Suggested fix:** In item 3, add: "A row that failed the well-formedness check is reported once, as the routing-violation P0; the closure row for its finding records REOPENED with that finding as its evidence rather than a second finding."

### F-6: The in-scope-P0 exception asks three lenses to make a scope call D17 tells them to treat as opaque
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 item 2 (:146), § Decisions D17 (:50)
**Claim:** In one block: "The `Scope` field is verified by the conventions lens against the brief's Scope table and Out-of-scope list; the other lenses read it as opaque," and "Do not file a P0/P1 whose root is a well-formed row … **unless the candidate is an in-scope P0**, which is always filed with the row cited as context."
**Why this is wrong:** The exception is keyed on the *candidate's* scope, but the sentence two lines earlier tells the correctness, edge-cases, and scalability lenses that scope is not theirs to judge. A reviewer resolving that in the conservative direction — "scope is opaque to me, so I cannot establish the exception applies" — suppresses the in-scope P0, which is the single class D14's carve-out (and brief Decision 2's ceiling) exists to protect. The two operations are genuinely different (verifying the author's `Scope` field vs. classifying one's own candidate), but the block never says so, and it is the same word in the same paragraph.
**Suggested fix:** One clause in the block: "Classifying your own candidate against the brief is not the same as verifying the row's `Scope` field: every lens makes the in-scope call for its own P0 candidate; only the conventions lens adjudicates the field the author wrote."

### F-7: Design 3's extra manifest line puts an out-of-round finding into a manifest D13 calls round-scoped by construction
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 (:108), § Decisions D13 (:46)
**Claim:** Design 3: "The manifest gets an extra line for the reverted finding even though it is not a round-(N−1) finding: `<lens>/F-<k> (P<sev>) "<title>" — deferred: D-<n> (…)`." D13: "The manifest keeps 2b's two-part `<lens>/F-<k>` form (round-scoped by construction)."
**Why this is wrong:** The two-part form is unambiguous only because 2b builds the manifest from round-(N−1) findings alone (`SKILL.md:360-362`, `:378-379`). This line deliberately injects a round-(N−2) finding, so `correctness/F-2` in one manifest can name two different findings, and — more likely — names a finding the round-N reviewer cannot locate in the round-(N−1) reports it was told to read (`agents/spec-reviewer-correctness.md:30-40`). Reviewer behavior on a manifest line with no matching prior-round finding is undefined; the plausible outcome is a spurious P0, i.e. the oscillation this ticket targets. The title carries enough information to disambiguate, which is why this is P2 and not higher.
**Suggested fix:** Round-qualify that one line — `<lens>/R<m>/F-<k>` — and add a clause to D13: "the sole exception to the two-part form is Design 3's revert line, which is round-qualified because it names a finding from an earlier round; reviewers treat a round-qualified line as provenance and verify it against the row, not against the prior round's report."

### F-8: R4 makes Phase 1 a no-op on any existing spec, including after the brief is narrowed
**Severity:** P2
**Where:** spec § Design 2 rule R4 (:100), § Scope row 1 (:15), § Decisions D16 headline (:49)
**Claim:** "On a re-run with an existing `docs/specs/TODO/<TICKET-ID>.spec.md`, Phase 1 does not re-author: the existing file is v1 and Phase 2 starts from it."
**Why this is wrong:** The rule is correct for its purpose (preserving rows and operator `Follow-up:` edits) but it is written unconditionally, and its blast radius reaches the halt menu's option 3, "Treat as scoped-down — narrow the brief" (`SKILL.md:483`). After that path the operator edits the brief and re-runs; under R4 the spec is never re-authored from the narrowed brief, so the reviewers compare an un-narrowed spec against a narrowed brief for four more rounds. The escape exists — Phase 0's re-run pin already says "delete the spec to force a clean Phase-1 re-author" (`SKILL.md:288`) — but R4 does not point at it, and the sentence it adds sits 6 lines below that pin. Separately, D16's headline ("a fold made in rounds 1–3") describes the wrong axis: Design 3 (:109) gates on the *current* round being 2 or 3, so the headline reads as permitting a round-4 revert of a round-3 fold, which D16's own body forbids.
**Suggested fix:** Extend R4: "…so this section and its `Follow-up:` values survive verbatim. To re-author from a changed brief (e.g. after 2f option 3), delete the spec first — the same escape Phase 0's re-run pin names." And retitle D16: "The recount's revert is available only in rounds 2–3 of this invocation."

### F-9: Design 3's "the fold predates this invocation" branch is unreachable
**Severity:** P3
**Where:** spec § Design 3 (:105, :109)
**Claim:** The trigger reads "the `fixed:` / `reworked:` lines of the manifests built earlier in **this invocation**"; the fallback branch fires when "…or the fold predates this invocation".
**Why this is wrong:** If only this invocation's manifests are consulted, a pre-invocation fold is never detected, so the recount never runs on it and the branch cannot fire. Harmless, but it implies a detection path the design deliberately removed (D16, "No round directory is scanned"), and a reader may go looking for it.
**Suggested fix:** Drop the clause, or reword it as an observation: "a fold made in a prior invocation is not detectable and is not recounted."

### F-10: Done-when 2's mechanism and the D15 sentence have no asserting checklist row
**Severity:** P3
**Where:** spec § Test plan (:156-165), § Done when (:180)
**Claim:** Done-when 2 maps to "Design 2's `Follow-up:` field with D12's backfill rule and rule R4's re-run preservation; Design 5 renders the field's value verbatim. — **Checklist row 8**."
**Why this is wrong:** Row 8 greps `=== FOLLOW-UPS` and the preamble sentence; neither touches the `Follow-up:` field, R4's Phase 1 sentence, or the render's verbatim rule. Row 4 asserts *a* hunk exists in the Phase 1 opening, which is the only indirect coverage. Likewise the D15 round-4 sentence is only implicitly covered: row 3's ≥3 threshold is already met by the 2e definition, the shape block, and the Failure-modes bullet, so a missing D15 sentence would not fail any row — although conventions/R1/F-2's fix asked for exactly such an assertion.
**Suggested fix:** Two rows: `grep -cF 'Follow-up: unfiled' skills/spec-cycle/SKILL.md` ≥ 2 (row shape + render example), and `grep -cF 'neither FROZEN nor REWRITE' skills/spec-cycle/SKILL.md` → 1.

## Summary
P0: 0 | P1: 3 | P2: 5 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=3 P2=5 P3=2 P4=0
