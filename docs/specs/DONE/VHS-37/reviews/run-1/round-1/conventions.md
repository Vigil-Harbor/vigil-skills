# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Design 7's no-re-file rule suppresses findings the brief never authorized suppressing, and contradicts the spec's own Decision 1
**Severity:** P1
**Where:** spec § Design 7 (the inserted reviewer paragraph); cross-check spec § Decisions 1
**Convention violated:** Silent spec addition (class (d)) that changes reviewer behavior; also contradicts a load-bearing claim the spec itself makes about the gate.
**Evidence:** Design 7 says: "*do not re-file it or any variant of the same root; the same holds for any new P0/P1 candidate whose root is already a row in that section, **in any round**.*" The brief authorizes only the narrower rule — brief Decision 1: "*the reviewer agents gain a rule for accepting a well-formed deferral instead of re-filing it*", and its mechanism is scoped to the `closure_manifest`, which by `skills/spec-cycle/SKILL.md:361-363` carries **round-(N−1) findings only**. The spec then asserts the opposite of what its own rule produces — spec Decision 1: "*`total_p0p1` is still summed from the `STATUS` lines only, so the number the operator reads is still the number of live findings.*" Under Design 7 a genuinely new P0 that shares a root with a `D-<n>` row is never counted, so the number is no longer the number of live findings. Combined with Design 2's "*the row stays … The skill does not garbage-collect*", a single round-1 deferral becomes a permanent gag on that root for the life of the spec, including after the spec text under it has been rewritten.
**Suggested fix:** Narrow the rule to what the brief authorizes and state the residual risk. Replace "*or any variant of the same root; the same holds for any new P0/P1 candidate whose root is already a row in that section, in any round*" with: a reviewer must not re-file **the deferred finding itself** while its row is well-formed; a **new** P0/P1 whose root matches a `D-<n>` row is filed normally, and the author routes it under Design 1 — where step 3's ceiling and Design 3's recount already handle it (in the common case it defers again as a second row, at no gate cost past that round). If the broad suppression is genuinely wanted, promote it to a numbered spec-level decision (D14) with rationale and amend Decision 1's "number of live findings" sentence, which is currently false under it.

### F-2: The round-4 rule in Design 1 is a silent addition, and its edit site is outside the Scope table's declared range
**Severity:** P1
**Where:** spec § Design 1, final paragraph ("*The step also applies at round 4: routing runs before the FROZEN/REWRITE manifest, and a deferred finding does not put its section into REWRITE.*"); spec § Scope row 1
**Convention violated:** Silent spec addition (class (d)) that changes behavior; Scope table under-declares the edit surface.
**Evidence:** The brief says nothing about round 4. Its Scope row for 2e reads "`skills/spec-cycle/SKILL.md` §2e (`:426-434`)" — and `:426-434` covers only the rounds-1–3 half; line 434 is the bare opener `If still red and \`round == 4\`:`, with the FROZEN/REWRITE definitions at `:435-441` and the closed-issues manifest at `:447-461`. The spec carries that same range forward verbatim in its own Scope table. But "*a deferred finding does not put its section into REWRITE*" edits the meaning of `:438-441` ("**REWRITE** — has unresolved P0/P1 OR has cross-references to a REWRITE section"), and it interacts with the closed-issues regression manifest at `:447-461`, neither of which the Scope table names. Nothing in D10–D13 flags this as a spec-level addition.
**Suggested fix:** Either (a) fence it — add to § Out of scope: "the round-4 FROZEN/REWRITE classification; a deferred finding is classified by the existing rule" — or (b) own it: promote it to a numbered spec-level decision with rationale, extend the Scope row to `skills/spec-cycle/SKILL.md` § 2e round-4 half (`:434-464`), name the exact sentence at `:438-441` being qualified, and add a checklist row asserting the hunk covers it.

### F-3: Two different `deferred:` disposition strings, and the short one violates 2b's existing "always with a spec § anchor" rule
**Severity:** P1
**Where:** spec § Design 1 step 4 and § Design 7 vs. § Design 4
**Convention violated:** Naming conflict with the existing manifest disposition vocabulary at `skills/spec-cycle/SKILL.md:378-383`.
**Evidence:** Design 1 step 4 and Design 7 both pin the contract string as `deferred: D-<n>` — Design 7: "*A manifest disposition of `deferred: D-<n>` is satisfied when …*". Design 4's example line writes a different string: `— deferred: § Deferred — follow-up required D-2`. The existing 2b prose these join is: "*a concise disposition phrase — e.g., `fixed: edited § <section>`, `reworked: …`, or `not applicable: <one-line reason>` — **always with a spec § anchor the reviewer can verify**.*" So `deferred: D-2` alone breaches the standing § -anchor requirement, while the Design 4 example that satisfies it is not the string Design 7 matches on. An author following the example produces a manifest line the reviewer rule does not recognize — which re-files the deferral and reproduces exactly the loop this ticket exists to break.
**Suggested fix:** Pick one form and use it in all three places. Recommended: `deferred: D-<n>, § Deferred — follow-up required` (satisfies 2b's § anchor and keys on `D-<n>`). Update Design 1 step 4, the Design 4 example line, and Design 7's matching sentence to that exact string, and add a checklist row: `grep -cF 'deferred: D-<n>, § Deferred — follow-up required' skills/spec-cycle/SKILL.md` → 2 (2b prose + 2e), plus 1 per agent file.

### F-4: `docs/spec-workflow-reference.md` is not reconciled, though every prior spec-cycle behavior change reconciled it
**Severity:** P2
**Where:** spec § Scope (absent); spec § Out of scope (absent)
**Convention violated:** The repo's docs-reconciliation pattern for lifecycle-skill changes; `AGENTS.md` treats `docs/spec-workflow-reference.md` as the canonical workflow reference.
**Evidence:** `docs/spec-workflow-reference.md:84` states the exact rule this spec replaces: "*6. **If still red (rounds 1-3):** Edit the spec in place. **Address every P0 and P1.** P2+ items either get fixed or listed in a `## Deferred (P2+)` section.*" Line 88 states the closure-status set this spec extends: "*produces a closure table showing which findings are CLOSED, PARTIAL, REOPENED, or NEW*". Line 77 describes the conventions lens's ownership of brief-authorization classification. Precedent is 4-for-4: `git log -- docs/spec-workflow-reference.md` → `ea5c2b0` (VHS-36), `c97d4ad` (VHS-33), `d381f88` (VHS-32), `a9e7581` (VHS-15); the VHS-15 state.md entry records "*Docs reconciled … across `AGENTS.md`, `README.md`, `docs/spec-workflow-reference.md`*", and VHS-17's close logged a dropped spec-workflow-reference pointer as DRIFT. This spec neither edits the file nor fences it. (`README.md` and `AGENTS.md` are genuinely clean — grep confirms neither carries the 2e rule or the status set.)
**Suggested fix:** Add a Scope row for `docs/spec-workflow-reference.md` (`:84`, `:88`) — one clause on line 84 naming fold / defer / reject, and `DEFERRED` added to line 88's status set — plus a checklist row (`grep -cF 'Address every P0 and P1.' docs/spec-workflow-reference.md` → 0). If the author would rather not widen the diff, fence it explicitly in § Out of scope with the reason, so the drift is a recorded decision rather than an omission.

### F-5: "all eight fields" does not match the row template, which has seven `**labels**` plus a heading
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 (well-formedness check); spec § Design 2 (row template); spec § Decisions D11
**Convention violated:** Label precision on a contract that a reviewer mechanically checks; single-source-of-truth between producer and consumer.
**Evidence:** Design 2's template is `### D-1: <title …>` followed by seven `**Field:**` lines (Finding, Deferred in, Where, Suggested fix, Propagation sites, Scope, Follow-up). Design 7 requires "*row `D-<n>` with all eight fields (title, Finding, Deferred in, Where, Suggested fix, Propagation sites, Scope, Follow-up)*" — counting the `###` heading as a field. D11 compounds it: "*The **eight field labels** appear once in 2e (producer) and once per agent as a single-line checklist*" — there are seven labels. A reviewer checking for eight `**…:**` labels finds seven and, per Design 7's own rule, marks the finding REOPENED — a well-formed deferral re-filed on a counting artifact.
**Suggested fix:** In Design 7 write "*with the `D-<n>` heading carrying a title and all seven fields (Finding, Deferred in, …)*"; in D11 change "eight field labels" to "seven field labels plus the titled heading". Also reconcile against the brief, whose Scope row enumerates eight items but counts severity separately and has no title — say in D11 that the spec folds severity into `Finding:` and adds the title, so a reader diffing against the brief sees it was deliberate.

### F-6: `DEFERRED` is added as a fifth closure status without amending the enumeration it contradicts, in the same file
**Severity:** P2
**Where:** spec § Design 7 ("Two edits per agent"); spec § Scope row for the four agents
**Convention violated:** Do not leave two contradicting statements of the same contract in one file (the repo's supersede-and-state pattern, e.g. `2026-08-09-review-round-artifacts-are-immutable.md`).
**Evidence:** Design 7 declares exactly two edits per agent — the `closure_manifest` input line and a paragraph after "REOPENED items are P0". Neither touches the enumeration that governs the closure table: `agents/spec-reviewer-correctness.md:38` (and `edge-cases:38`, `conventions:43`, `scalability:30`) reads "*verify against the current spec whether it is CLOSED, PARTIAL, REOPENED, or NEW*". After the change each agent file says in one place that four statuses exist and in another that "*Mark such a finding `DEFERRED` in the closure table (a fifth status)*". The markdown closure-table example immediately below (`correctness:43-49`, `scalability:33-38`) also shows no `DEFERRED` row.
**Suggested fix:** Make it three edits per agent: extend the enumeration to "CLOSED, PARTIAL, REOPENED, DEFERRED, or NEW", and add one `DEFERRED` example row to each agent's closure-table block (each agent's example rows are lens-specific, so the row is per-file while the paragraph stays byte-identical — note that in Design 7 so checklist row 6's byte-identical assertion is not read as covering the example rows).

### F-7: "REOPEN it at the original severity" for the *stricter* checks silently weakens the existing REOPENED-is-P0 rule
**Severity:** P2
**Where:** spec § Design 7, "Two checks are stricter: …"
**Convention violated:** Contradicts an existing rule in all four agent files without acknowledging the change.
**Evidence:** The standing rule the new paragraph is inserted directly beneath reads (`agents/spec-reviewer-correctness.md:51-53`, `conventions:56-58`, `scalability:40-42`): "*REOPENED items are P0 unless evidence shows the spec deliberately changed direction with rationale.*" Design 7 routes an ordinary malformed row to "*mark the finding REOPENED with the failing field as evidence*" (P0 by that rule), then routes the two **routing violations** it calls "*stricter*" to "*REOPEN it at the original severity*" — which for a deferred P1 is P1, i.e. **less** severe than the malformed-row case. The ladder is inverted relative to the labels, and the "at the original severity" clause is a new exception to the REOPENED-is-P0 rule that D10–D13 do not record.
**Suggested fix:** Make both paths P0 (a routing violation is at least as bad as a missing field) and drop "at the original severity"; or, if de-escalation is intended, state it as a numbered spec-level decision and reword "stricter" to "narrower" so the label matches the effect. Either way, say explicitly whether the new paragraph creates an exception to the existing "REOPENED items are P0" sentence.

### F-8: Scope adjudication is spread across all four lenses, diluting the lens that owns it
**Severity:** P2
**Where:** spec § Design 7 (identical paragraph in four agents); spec § Decisions 6
**Convention violated:** Lens separation as recorded in `AGENTS.md` § "Parallel review agents" and `docs/spec-workflow-reference.md:77`; the rationale of wiki decision `2026-06-16-vhs-15-optional-scalability-lens.md` § 2.
**Evidence:** `AGENTS.md` assigns brief-authorization to one lens: "*`spec-reviewer-conventions` | Does it follow the repo? | AGENTS.md / CLAUDE.md rules, wiki decisions, premature abstractions, duplicate code*", and `docs/spec-workflow-reference.md:77` is explicit — the conventions reviewer "*Also classifies every spec decision as authorized-by-brief, authorized-by-ticket, spec-addition-with-rationale, or silent-addition.*" Design 7 gives all four lenses the job of checking "*the `Scope` field is consistent with the brief's Scope table and Out-of-scope list*", and instructs them to emit "*a P2 correction*" when it is wrong. VHS-15 § 2 rejected folding a dimension into another lens precisely because "*it dilutes the edge-cases reviewer's focus*". The brief's own Decision 6 rationale warns against the adjacent hazard: an `In-fence` tag "*invites reviewers to file scope opinions as findings*" — which the "P2 correction" clause now does, one lens-change short of the thing the brief fenced.
**Suggested fix:** Split the paragraph's obligations: **all four** lenses verify well-formedness (row exists, eight/seven fields present, ≥2 named sections that exist) and honor the no-re-file rule; **only the conventions lens** verifies the `Scope` field against the brief and may emit the P2 correction. The other three read `Scope` as opaque. This keeps the inserted paragraph byte-identical across four files except one sentence, or — cleaner — keeps it byte-identical and puts the scope-verification sentence in a fifth, conventions-only line, which checklist row 6 can then assert as `→ 1` in one file.

### F-9: Finding ids appear in two forms inside one contract
**Severity:** P3
**Where:** spec § Decisions D13; § Design 2 (`Finding:` field); § Design 4 (example line)
**Convention violated:** One identifier form per contract.
**Evidence:** D13's claim checks out — `skills/spec-cycle/SKILL.md:454` does use `finding_id: "correctness/R1/F-3"` — but the closure manifest that carries the disposition uses the two-part form throughout (`:362-363`: `<lens>/<finding-id>` … `correctness/F-2`), and the spec's own Design 4 example keeps it: `edge-cases/F-4 (P1) … — deferred: …`. So the manifest names the finding `edge-cases/F-4` while the row it points at names it `edge-cases/R3/F-4`. Design 7 keys on `D-<n>`, so nothing breaks; but a reviewer cannot cross-check that the row belongs to the disposition without inferring the round.
**Suggested fix:** Add one sentence to D13: the manifest keeps 2b's two-part form (it is round-scoped by construction), the row uses the three-part form because rows outlive rounds, and the reviewer matches on `D-<n>` — so the two forms never need to be equal. Or make Design 4's example use the three-part id and say the manifest accepts either.

### F-10: Roll-up of unflagged spec-level additions (class (d)), each small
**Severity:** P3
**Where:** spec §§ Design 1, 2, 5, 7
**Convention violated:** Silent additions the brief and ticket do not authorize should be visible to the human drift-check.
**Evidence:** None of the following appears in the brief or in the spec's D10–D13 list: (i) Design 2 — "*`D-<n>` numbers … never reused*"; (ii) Design 2 — "*the row stays … the operator can drop the row by hand. The skill does not garbage-collect*"; (iii) Design 5 — the `(none)` empty render; (iv) Design 7 — "*dispute a site only when the named section does not exist*"; (v) Design 1 step 3 — "*the honest path is to halt and narrow the brief*", which points at 2f option 3, a menu that by `skills/spec-cycle/SKILL.md:466-487` only renders **after round 4**, so during rounds 1–3 the named escape does not exist.
**Suggested fix:** Add one line each to the "Spec-level decisions (not in the brief)" list, or a short "minor additions" bullet naming (i)–(iv). For (v), say what the author actually does in rounds 1–3 — most likely: fold with the corrected site list and record the over-run as a P2 note, with the scope-down deferred to the 2f menu if the run reaches it.

### F-11: Design 3's re-run path reads round directories as current-state evidence
**Severity:** P3
**Where:** spec § Design 3
**Convention violated:** `vigil-harbor-wiki/decisions/2026-08-09-review-round-artifacts-are-immutable.md`.
**Evidence:** Design 3 says on a re-run to consult "*the Evidence column of the persisted closure tables under `<TICKET-ID>.reviews/round-*/`*". The decision states these are "*dated evidence of what reviewers knew and said at a moment in time*" and that "*Archived review directories carry claims that are false about the current code … Anyone reading them must read forward to the last round.*" Reading is fine (nothing mutates), but a round-1 Evidence cell naming a section the spec has since restructured will mis-seed the recount.
**Suggested fix:** One clause in Design 3: read the round directories **newest-first** and take the latest closure table's evidence for a given finding, and verify the named section still exists in the current spec before counting it as a fold site.

### F-12: Scope table says one inserted paragraph per agent; Design 7 specifies two edits
**Severity:** P4
**Where:** spec § Scope, last row
**Convention violated:** Scope table should enumerate the edit surface Design later assumes.
**Evidence:** Scope row: "*`DEFERRED` becomes a legal closure disposition and a legal closure-table status; the no-re-file rule (Design 7). **One identical inserted paragraph per file.***" Design 7: "*Two edits per agent, identical text across the four files: 1. The `closure_manifest` input line gains … 2. Step 7 gains one paragraph …*" (and F-6 argues it should be three).
**Suggested fix:** "Two edits per file: one clause appended to the `closure_manifest` input line, one identical inserted paragraph in step 7." Update if F-6 is taken.

## Summary
P0: 0 | P1: 3 | P2: 5 | P3: 3 | P4: 1

STATUS: RED P0=0 P1=3 P2=5 P3=3 P4=1
