# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1.

**Grounding completed.** Spec and brief read from disk; Plane VHS-37 retrieved from the `skills` namespace (tag-exact, confidence 1.00) — the ticket's framing ("valid, out-of-scope, non-trivial = follow-up ticket and deferred") is consistent with the brief, which carries the later 2026-09-08 refinement (Decision 2's ceiling). `AGENTS.md` read (the canonical instructions; `CLAUDE.md` is the gitignored machine-local pointer). All file:line anchors in the spec's Scope table were re-grepped: `SKILL.md:426-434` (2e), `:411-424` (2d), `:365-368` / `:378-383` (2b), `:466-487` (2f halt), `:626-659` (Phase 3 render), `:593-624` (2g), `:685-` (Failure modes), `correctness:18/:30-53`, `edge-cases:18/:30-53`, `conventions:20/:35-58`, `scalability:18/:30-42/:40`, and the three output contracts at `correctness:138`, `edge-cases:133`, `conventions:127` — **all accurate**. The two grep-baseline claims verified: `grep -rn 'Deferred' skills/spec-close/SKILL.md skills/ship-spec/SKILL.md` → 0 hits; `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → 7. `lint.py --strict` exists and exits 1 only on ERROR (`lint.py:270,291`). Anchor hygiene on this spec is unusually good; the findings below are all design-level.

## Findings

### F-1: The manifest disposition phrase is declared one way and exampled another
**Severity:** P0
**Where:** spec § Design 4 (line 98) vs § Design 1 step 4 (line 59) and § Design 7 (line 131)
**Claim:** Design 1 step 4: "disposition it `deferred: D-<n>`." Design 7's acceptance rule: "A manifest disposition of `deferred: D-<n>` is satisfied when …". But Design 4's example block writes:
```text
  - edge-cases/F-4 (P1) "jq empty-array path" — deferred: § Deferred — follow-up required D-2
```
**Why this is wrong:** The example and the declaration disagree on the exact string, and the reviewer-side rule keys off the declared form. Worse, the example's form is the one 2b's existing prose actually demands — `skills/spec-cycle/SKILL.md:382-383` requires a disposition phrase "always with a spec § anchor the reviewer can verify," which bare `deferred: D-2` does not carry. So the two forms are not interchangeable: the declaration violates 2b's standing rule, and the example violates Design 7's matching rule. Implementers follow the code block; reviewers follow Design 7. A second axis compounds it: the example uses the two-part id `edge-cases/F-4` (the form 2b mandates at `:366`), while the row's `**Finding:**` field and Design 5's render use the round-qualified `edge-cases/R3/F-4` (D13, line 42). Nothing says how the reviewer matches one to the other.
**Suggested fix:** Pin one canonical phrase in Design 1 step 4, Design 4's example, and Design 7's rule — e.g. `deferred: D-<n> (§ Deferred — follow-up required)` — and state explicitly that the manifest keeps 2b's two-part `<lens>/<finding-id>` id while the row's `Finding` field is round-qualified, with the round supplied by the manifest's own round header.

### F-2: The no-re-file rule is unreachable on round 1, so a re-run re-files every deferral
**Severity:** P0
**Where:** spec § Design 7 (line 131)
**Claim:** "do not re-file it or any variant of the same root; the same holds for any new P0/P1 candidate whose root is already a row in that section, **in any round**."
**Why this is wrong:** The paragraph is inserted "after the 'REOPENED items are P0' sentence" — i.e. inside step 7, whose opening line is `7. **If `round_number ≥ 2`**, …` (`agents/spec-reviewer-correctness.md:30`, `edge-cases.md:30`, `conventions.md:35`, `scalability.md:30`). A round-1 reviewer skips the entire step and never reads the rule. That is not hypothetical: the spec itself asserts rows persist across invocations (Design 2 line 81, "carried unchanged across rounds and re-runs"; D12 line 41, "a re-run of `/spec-cycle` carries existing rows unchanged"), `SKILL.md:280-290` documents the cross-invocation re-run pin, and 2f option 1 (`SKILL.md:481`) makes "Patch manually and re-run /spec-cycle" the primary red-path recovery. Phase 2 restarts unconditionally at round 1 (`SKILL.md:319`, "For each round 1..4"). So on the single most common recovery path the deferrals are all re-filed as P0/P1, the gate goes red again, and the escape hatch the brief exists to build does not fire. The rule's own words ("in any round") contradict its placement.
**Suggested fix:** Do not put the rule in step 7. Add it as its own ungated grounding step (or as a bullet in each agent's critique lens) that runs at every `round_number`: "Before filing any P0/P1, check the spec's `## Deferred — follow-up required` section; a finding whose root is already a well-formed row there is not filed — record it as DEFERRED." Keep only the *manifest-verification* half (checking a `deferred:` disposition against the row) inside step 7.

### F-3: Nothing makes Phase 1 preserve the deferral section on a re-run
**Severity:** P1
**Where:** spec § Decisions D12 (line 41), § Design 2 rules (line 81)
**Claim:** "Nothing in `/spec-cycle` reads, changes, or removes a row once written; rows are carried unchanged across rounds and re-runs" and "a re-run of `/spec-cycle` carries existing rows unchanged, so the render (Design 5) prints whatever the field holds."
**Why this is wrong:** Phase 1 (`SKILL.md:294-315`) says "Output path: `docs/specs/TODO/<TICKET-ID>.spec.md` … Write a spec that covers, at minimum: …" with no already-exists branch. The only hint that a re-run does not blank-slate is an aside in the scale re-run pin (`SKILL.md:288`, "delete the spec to force a clean Phase-1 re-author"), which is not a rule about section preservation. Compare 2g, which *does* state the pattern explicitly: "If a `## Post-green polish` section already exists in the spec, treat 2g as already-run: reconcile (merge/dedup) rather than append" (`SKILL.md:599-601`). The spec adds no equivalent for `## Deferred — follow-up required`, yet cross-invocation persistence is the sole mechanism by which brief Done-when 2 ("Deferred entries that become tickets carry the ticket id") is met — an operator's hand-edited `Follow-up: VHS-99` survives only if the section survives.
**Suggested fix:** Add one rule to the Design 2 insertion, mirroring 2g's wording: "Phase 1 on a re-run preserves an existing `## Deferred — follow-up required` section verbatim, including operator hand-edits to `Follow-up:`; it is never re-authored from the brief." Cite it in the Done-when mapping for criterion 2.

### F-4: Design 3's revert collides with the round-4 closed-issues regression constraint and 2e's "do not delete history"
**Severity:** P1
**Where:** spec § Design 3 (lines 87-91)
**Claim:** "True count now two or more → **revert the original fold** (remove the edit from every site it touched) and defer both findings as two rows."
**Why this is wrong:** Two untouched pieces of 2e forbid this.
1. The round-4 closed-issues manifest (`SKILL.md:449-462`) is built from "every finding whose status resolved to CLOSED in a later round's closure table," and the file states: "Every entry is a regression constraint: the rewritten spec must preserve the fix that closed it." A fold made in round 2 and marked CLOSED in round 3's closure table is such an entry. Design 3's revert at round 4 removes exactly that fix — a direct violation of a rule the spec leaves byte-identical. Design 1 (line 61) claims round 4 is handled ("routing runs before the FROZEN/REWRITE manifest, and a deferred finding does not put its section into REWRITE") but says nothing about the closed-issues manifest.
2. The 2e bullet at `SKILL.md:432` — "Do not delete history of what changed" — which the spec explicitly keeps unchanged (line 61), is in tension with "remove the edit from every site it touched."
3. Bookkeeping gap: the reverted finding was filed in round N−2, so it produces no line in the round-(N−1)→N manifest (2b builds the manifest from round-(N−1) findings only, `SKILL.md:360-362`). Its status silently flips from CLOSED to deferred with no disposition line for any reviewer to verify.
**Suggested fix:** Add to Design 3: (a) a revert supersedes the closed-issues-manifest entry for that finding — the entry is rewritten as "closed by deferral D-`<n>`, fix reverted," and the FROZEN/REWRITE protocol promotes every reverted site to REWRITE; (b) the revert is history-preserving in the 2e sense because the row records what was removed and why; (c) a reverted out-of-round finding gets an explicit extra manifest line (`<lens>/F-<k>` … `deferred: D-<n> (revert of round <m> fold)`) even though it is not a round-(N−1) finding.

### F-5: The agents' closure-status enumeration is left stale, so the edited agent contradicts itself
**Severity:** P1
**Where:** spec § Scope (line 17), § Design 7 (lines 126-131)
**Claim:** Scope: "`DEFERRED` becomes a legal closure disposition and **a legal closure-table status**." Design 7: "**Two edits per agent**" — the `closure_manifest` input line, and one paragraph appended after the "REOPENED items are P0" sentence.
**Why this is wrong:** The sentence that actually defines the status vocabulary is not one of the two edits. It sits at `agents/spec-reviewer-correctness.md:38-39` (and `edge-cases.md:38-39`, `conventions.md:43-44`, `scalability.md:30`): "verify against the current spec whether it is CLOSED, PARTIAL, REOPENED, or NEW (a new variant of the same root)." After the change, each agent file tells the reviewer the status set is four items and then, a dozen lines later, tells it to emit a fifth. This is precisely the one-site-fix-that-needed-two-sites failure mode the spec exists to prevent — and Design 7's "two edits per agent, identical text" instruction actively forbids the third edit. (The output contract sections are correctly out of scope: they render `<table per the grounding step>` at `correctness:147`, `edge-cases:141`, `conventions:136`, so no contract edit is needed. The stale site is the grounding step, not the contract.)
**Suggested fix:** Make it three edits per agent: also amend the enumeration to "CLOSED, PARTIAL, REOPENED, DEFERRED, or NEW", and update the Scope table row and Design 7's "Two edits per agent" count. Add a checklist row asserting `grep -c 'CLOSED, PARTIAL, REOPENED, DEFERRED, or NEW' agents/spec-reviewer-*.md` → 1 per file.

### F-6: Test-plan row 4 under-describes the 2b diff that Design 4 specifies
**Severity:** P1
**Where:** spec § Test plan row 4 (line 142)
**Claim:** "`git diff --stat` for `skills/spec-cycle/SKILL.md` touches **only the 2b example list**, 2e, 2f halt block, Phase 3 block, and Failure modes".
**Why this is wrong:** Design 4 (lines 93-99) specifies **two** touches in 2b: the example block at `:365-368` *and* the disposition-phrase prose at `:378-383` (verified — line 382 is where `fixed:` / `reworked:` / `not applicable:` are listed). A gate script written against row 4 — and the spec's own "Gate-script hygiene" note (line 148) tells the implementer to write one asserting hunk regions — would flag the legitimate `:378-383` hunk as an unauthorized edit. The Scope table (line 14) has the same narrowing: it labels the 2b row "§ 2b closure-manifest **examples** (`:361-388`)" and describes the change as "One new example line," omitting the prose edit entirely.
**Suggested fix:** Rewrite row 4 as "touches only the 2b example block (`:365-368`) and the 2b disposition-phrase prose (`:378-383`), 2e, …", and fix the Scope table row 2 description to name both touches.

### F-7: Design 1 turns the brief's ceiling into a mandate
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 step 3 (lines 54-56), § Decisions 2 (line 28)
**Claim:** "two or more sites and out-of-scope → **defer**, whatever the severity; two or more sites, in-scope, P1 → **defer**".
**Why this is wrong:** Brief Decision 2 is titled "Scope is a **ceiling**, not a required conjunct" and is worded permissively throughout: "Out-of-scope + non-trivial is **deferrable** at any severity. In-scope + non-trivial is **deferrable** at P1 and below" (brief:29). A ceiling bounds what *may* be deferred; the spec converts it into what *must* be. Under the spec, an author who spots a cheap, obviously-correct two-site fix for an out-of-scope P1 is forbidden to make it. That is drift from a load-bearing brief decision, and it is unenforceable besides — Design 7's reviewer checks only catch under-deferral (a row with fewer than two sites), never over-folding, so the mandate has no verification path.
**Suggested fix:** Restate step 3 as a permission with a default: "→ **defer** (fold only when the author records a one-line reason in the manifest that the fix is trivially safe at every site)". Or keep the mandate and amend Decision 2's restatement (line 28) to say the spec deliberately hardens the brief's ceiling into a rule, with rationale.

### F-8: Reject is evaluated last, after the author has already been told to enumerate propagation sites
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 (lines 50-59)
**Claim:** "Route every P0 and P1 finding … **in this order**: 1. Name the propagation sites … 3. Apply the ceiling: … the finding is wrong (misread, stale, already handled) → **reject**."
**Why this is wrong:** Step 1 asks the author to "List every place in the spec the fix must land" for a finding that, per the last clause of step 3, may have no valid fix at all. The routing order forces wasted work on exactly the findings that should be dismissed fastest, and invites an author who has just written a two-site list to reach for defer rather than reject. Validity is a precondition of routing, not a branch of it.
**Suggested fix:** Promote reject to step 0: "0. **Test validity.** If the finding is wrong (misread, stale, already handled) → reject; disposition it `not applicable: <reason>` and stop. Otherwise continue." Renumber the rest and drop the reject clause from the ceiling.

### F-9: `sync.py push` round-trip is a Done-when criterion with no checklist row
**Severity:** P2
**Where:** spec § Done when (line 164), § Test plan row 2 (line 140)
**Claim:** Done-when 3 quotes the brief verbatim — "`lint.py --strict` reports zero ERROR; `sync.py status` clean; **`sync.py push` round-trips byte-for-byte**" — and maps it to "Checklist rows 1, 2; the Test command."
**Why this is wrong:** Row 2 tests only the repo→config direction: `sync.py status` after `sync.py install`. The push direction (config→repo) is never exercised, so the byte-for-byte round-trip half of the criterion has no covering row. This is not idle: the memory note "sync.py --claude-dir after subcommand" records that the top-level flag is silently ignored and hits the live `~/.claude`, which is exactly the kind of thing a push round-trip catches and an install-then-status does not.
**Suggested fix:** Add a row: "`python sync.py push --dry-run` (flag after the subcommand) reports no pending changes for `skills/spec-cycle/SKILL.md` or the four `agents/spec-reviewer-*.md` after `install`; `git status --porcelain` on those five paths is empty."

### F-10: The row carries a verbatim "Suggested fix" into a spec that `/ship-spec` implements
**Severity:** P2
**Where:** spec § Design 2 (line 72), § Design 6 (line 122)
**Claim:** Row field: "**Suggested fix (verbatim):** <the reviewer's Suggested fix, unedited>". Design 6: "Nothing downstream reads it — `/ship-spec` and `/spec-close` do not consume the section."
**Why this is wrong:** "Does not consume" is a statement about *added machinery*, not about what the implementing agent reads. `/ship-spec` hands the whole spec file to an implementer, and a section containing an unedited, imperative "Suggested fix" reads exactly like work to do. The existing `## Deferred (P2+)` section is safe from this because `SKILL.md:431` constrains it to "one-line acknowledgments"; the new section deliberately carries full prescriptive text. Grep confirms zero `Deferred` hits in either downstream skill today (checklist row 7 verified), so no fence exists on the read side either.
**Suggested fix:** Add one line to the section body, defined in the Design 2 insertion: a fixed header sentence under the `## Deferred — follow-up required` heading — "Known, unfixed findings. `/ship-spec` must not implement anything in this section." Add a checklist row asserting the sentence is emitted with the section.

### F-11: Checklist row 3's ≥3 justification does not match the design's occurrence sites
**Severity:** P3
**Where:** spec § Test plan row 3 (line 141)
**Claim:** "`grep -cF '## Deferred — follow-up required' skills/spec-cycle/SKILL.md` ≥ 3 (2e definition, 2f render, Phase 3 render)."
**Why this is wrong:** Design 5's rendered block (lines 108-111) contains no occurrence of the section name — it is `=== FOLLOW-UPS …` plus row lines — so neither the 2f nor the Phase 3 render is guaranteed to produce the literal unless the surrounding instruction prose happens to name the section. Meanwhile Design 6's failure-mode bullet (line 122) *does* contain the literal and is not in the parenthetical. The threshold will probably pass by accident (the 2e insertion alone likely emits it twice), but the row does not check what it claims to check.
**Suggested fix:** Re-justify as "(2e definition ×2, Failure-modes bullet)" and add a separate row for the renders: `grep -cF '=== FOLLOW-UPS' skills/spec-cycle/SKILL.md` → 2 — which row 8 already does. Or require each render's instruction prose to name the source section and keep ≥4.

### F-12: "Halt and narrow the brief" has no mid-loop mechanism
**Severity:** P3
**Where:** spec § Design 1 step 3 (line 57)
**Claim:** "(An in-scope P0 … cannot ship as a known issue. If the fold is more than the brief supports, the honest path is to **halt and narrow the brief**.)"
**Why this is wrong:** The only scope-down affordance is 2f option 3 (`SKILL.md:483`), and 2f fires only "If after round 4 the spec is still red" (`SKILL.md:468`). At round 2 an author facing an unfoldable in-scope P0 has no supported exit; the advice is unactionable. The brief has the same gap (brief:29, "or the brief scoped down via 2f option 3"), so this is inherited rather than introduced — but the spec is where it becomes an instruction to an agent.
**Suggested fix:** Either mark the sentence advisory ("stop and tell the operator; there is no mid-loop scope-down path — 2f option 3 is only reachable after round 4"), or file the mid-loop halt as a follow-up and say so in Out of scope.

### F-13: Two commits touched `SKILL.md` yesterday
**Severity:** P3
**Where:** spec § Scope (lines 13-16)
**Claim:** Anchors `:426-434`, `:466-487`, `:626-659`, `:685-`.
**Why this is wrong:** Not wrong — all anchors verified accurate as of now — but `git log` shows `ecdfefe` and `c97d4ad` landed 2026-09-07 (one day ago) on `skills/spec-cycle/SKILL.md`, both in the 2f-i grilling hand-off region immediately below the 2f halt block the spec edits. Design 5 depends on 2f-i step 5's wording ("then the 2f halt block again with options 1–3 only", verified at `SKILL.md:555-557`), which those commits are adjacent to. Also note brief:67 flags Plane VHS-27 as open and owning the same 2f region.
**Suggested fix:** Add a one-line note under Scope that the anchors were verified against `ecdfefe` (2026-09-07) and that the implementer must re-verify `:466-487` and 2f-i step 5 against `main` at implementation time; name VHS-27 as the rebase counterpart.

### F-14: "Left alone" lists three output contracts, omitting scalability's
**Severity:** P4
**Where:** spec § Scope, "Left alone, byte-identical" (line 19)
**Claim:** "the reviewer output contracts (`correctness:138-176`, `edge-cases:133-165`, `conventions:127-158`)".
**Why this is wrong:** The spec goes out of its way (line 21) to argue the scalability agent is in scope, then omits its output contract from the fence. Verified: `agents/spec-reviewer-scalability.md` has the same structure, with its closure-table stanza at `:84`.
**Suggested fix:** Add `scalability:<start>-<end>` to the list.

## Summary
P0: 2 | P1: 4 | P2: 4 | P3: 3 | P4: 1

STATUS: RED P0=2 P1=4 P2=4 P3=3 P4=1
