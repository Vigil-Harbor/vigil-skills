# Conventions Review — round 2

**Grounding completed.** Spec and brief re-read from disk at `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-37.spec.md` / `.brief.md`. `AGENTS.md` read end to end (the canonical instructions; `CLAUDE.md` is the gitignored machine-local pointer). Wiki read at `C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki` — `decisions/2026-08-09-review-round-artifacts-are-immutable.md`, `decisions/2026-06-16-vhs-15-optional-scalability-lens.md`, `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`. All three round-1 reports read. Repo greps re-run against `main`: `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → **7**; `skills/spec-cycle/SKILL.md:430` → `- Address every P0 and P1 finding.`; `docs/spec-workflow-reference.md:84`/`:88` → present as the spec describes; all four agent anchors (`correctness:18/38-39`, `edge-cases:18/38-39`, `conventions:20/43-44`, `scalability:18/30`) verified accurate. `README.md`, `docs/customizing.md`, `docs/portability-contract.md` confirmed clean of the 2e rule and the closure-status set.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | manifest phrase declared vs exampled | CLOSED | spec § Design 1 step 4, § Design 4 prose + example, all use `deferred: D-<n> (§ Deferred — follow-up required)`; D13 reconciles id-form |
| correctness | F-2 | no-re-file rule unreachable on round 1 | CLOSED | § Design 7 item 2 — ungated block between step 6 and step 7 (verified: step 6 is grounding in all four agents, step 7 is the `round_number ≥ 2` gate) |
| correctness | F-3 | Phase 1 does not preserve the section on re-run | CLOSED | § Design 2 R4; § Scope row `:294-296`; § Done when criterion 2 |
| correctness | F-4 | revert vs round-4 regression constraint | CLOSED | § Decisions D16; § Design 3 third bullet |
| correctness | F-5 | stale closure-status enumeration | CLOSED | § Design 7 item 3; § Scope agents row; checklist row 6 (but see F-3 below — the grep cannot match) |
| correctness | F-6 | test-plan row 4 under-describes the 2b diff | CLOSED | checklist row 4 and § Scope 2b row both name `:365-368` and `:378-383` |
| correctness | F-7 | ceiling as mandate | CLOSED | dispositioned in § Deferred (P2+) with rationale; § Decisions 2 restatement |
| correctness | F-8 | reject evaluated last | CLOSED | § Design 1 step 0 "Test validity" runs first |
| correctness | F-9 | `sync.py push` round-trip has no checklist row | CLOSED | checklist row 2 adds `push --dry-run` |
| correctness | F-10 | verbatim `Suggested fix` in a ship-spec-implemented spec | CLOSED | § Design 2 preamble fence |
| correctness | F-11 | row 3's ≥3 justification | PARTIAL | row 3 now names three sites; there are four (see F-8 below), count still holds at ≥3 |
| correctness | F-12 | "halt and narrow the brief" has no mechanism | CLOSED | § Decisions "Minor additions" bullet; § Out of scope 8 |
| correctness | F-13 | two commits touched SKILL.md | CLOSED | § Scope line 11 (re-verify note) |
| correctness | F-14 | "Left alone" omits scalability's contract | CLOSED | § Scope "Left alone" now lists `scalability:76-118` |
| edge-cases | F-1 | acceptance rule unreachable on re-run/round-4 | CLOSED | § Design 7 item 2 ungated block; § Design 6 |
| edge-cases | F-2 | no severity carve-out on root suppression | CLOSED | § Decisions D14; § Design 7 block "unless the candidate is an in-scope P0" |
| edge-cases | F-3 | additive fixes undeferrable | CLOSED | `(new)` marker in § Design 1 step 1, § Design 2 shape, § Design 7 block |
| edge-cases | F-4 | round-4 protocol collision | CLOSED | § Decisions D15, D16; § Design 1 "Round 4" (but see F-4 below — anchor disagreement) |
| edge-cases | F-5 | per-run round numbers / reviews tree | CLOSED | § Decisions D13, D16 ("No round directory is scanned"); § Design 2 R1 |
| edge-cases | F-6 | section not marked non-normative | CLOSED | § Design 2 preamble; § Design 6; checklist row 8 |
| edge-cases | F-7 | Design 4 example vs Design 7 form | CLOSED | same canonical phrase (correctness/F-1) |
| edge-cases | F-8 | render must parse hand-edited rows | CLOSED | § Design 5 extraction rule (`?` columns, malformed-row line) |
| edge-cases | F-9 | heading prefix-confusable | CLOSED | dispositioned in § Deferred (P2+); § Decisions 5 and § Design 2 R3 pin exact-heading matching |
| edge-cases | F-10 | 2f-i step 4 runs routing | CLOSED | § Design 1 closing line; § Decisions "Minor additions" |
| edge-cases | F-11 | test-plan gaps | PARTIAL | (a) em-dash/Git-Bash note added to § Test plan preamble ✓; (b) row 3 parenthetical still incomplete (F-8 below); (c) no row asserts the D15 round-4 sentence exists — row 6 covers only the reviewer block |
| conventions | F-1 | no-re-file rule unauthorized, contradicts Decision 1 | CLOSED | § Decisions D14 with rationale, root definition, in-scope-P0 exception; § Decisions 1 sentence amended to "live findings that are not deliberately deferred" |
| conventions | F-2 | round-4 rule silent + outside Scope range | CLOSED | § Decisions D15; § Scope 2e row extended to `:426-464`; checklist row 4 |
| conventions | F-3 | two `deferred:` disposition strings | CLOSED | one canonical phrase carrying the § anchor 2b requires; checklist row 9 |
| conventions | F-4 | `docs/spec-workflow-reference.md` unreconciled | CLOSED | § Scope row (`:84`, `:88`); checklist row 10 (but under-scoped — see F-6 below) |
| conventions | F-5 | "eight fields" vs seven labels | CLOSED | § Decisions D11 "seven field labels plus the titled heading"; § Design 7 block "all seven fields" |
| conventions | F-6 | closure-table example row | PARTIAL | enumeration gains `DEFERRED`; example row deliberately not required — dispositioned in § Deferred (P2+) with rationale |
| conventions | F-7 | "REOPEN at the original severity" inverts the ladder | CLOSED | § Design 7 block routes every routing violation to a P0 finding; the de-escalation clause is gone |
| conventions | F-8 | scope adjudication spread across four lenses | CLOSED | § Decisions D17; one sentence in the byte-identical block assigns `Scope` to the conventions lens, opaque to the rest |
| conventions | F-9 | two finding-id forms | CLOSED | § Decisions D13 |
| conventions | F-10 | roll-up of silent additions | CLOSED | § Decisions "Minor additions" bullet covers (i)–(v) |
| conventions | F-11 | round dirs read as current state | CLOSED | § Decisions D16 "No round directory is scanned" — honors `decisions/2026-08-09-review-round-artifacts-are-immutable.md` |
| conventions | F-12 | Scope says one paragraph, Design says two edits | CLOSED | § Scope agents row now reads "Three edits each" |

No REOPENED items. Both PARTIALs (correctness/F-11, edge-cases/F-11, conventions/F-6) were P3/P2 originally and keep that severity; conventions/F-6's residue is an explicit, reasoned disposition and needs nothing further.

## Findings

### F-1: Design 2 does not say which of R1–R5 become SKILL.md prose, and under the natural reading R3 breaks checklist row 5
**Severity:** P1
**Where:** spec § Design 2 ("Rules stated with the shape:", R1–R5) vs § Test plan row 5
**Convention violated:** Brief Decision 5 — `## Deferred (P2+)` and its consumers are "**Untouched, byte-identical**"; checklist row 5 is the mechanism that enforces it. Also the repo's recorded gate-script practice ("assert hunk regions not counts; re-verify backtick phrases with `grep -cF`", MEMORY `project_prose_spec_gate_script_pitfalls`).
**Evidence:** Design 2 says the section is "Defined in the same 2e insertion" and then "**Rules stated with the shape:**" — i.e. R1–R5 are prose written into `skills/spec-cycle/SKILL.md` § 2e. R3 reads: "*A row is not a `## Deferred (P2+)` entry and is never a 2g candidate; 2g reads only `## Deferred (P2+)`, by exact heading.*" That is one new line carrying the literal, so the verified baseline `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → **7** becomes **8**. Checklist row 5 asserts it "is 7 before and after." The two statements cannot both hold. The ambiguity is compounded by R4, whose parenthetical relocates its own normative text elsewhere ("*One sentence added at `:294-296`*"), and by R5, which describes reviewer/closure-table behavior that § Design 7's three-edits list does not carry into any agent file — so a third rule apparently ships nowhere.
**Suggested fix:** In § Design 2, state explicitly which rules are SKILL.md prose (R1, R2, R3, R5 under the shape; R4's normative sentence at `:294-296` per the Scope row) and which are spec-level notes. Then re-calibrate checklist row 5 to the real post-edit value — `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` → **8**, with the seven pre-existing lines (`:371`, `:424`, `:431`, `:611`, `:618`, `:622`, `:623`) unchanged — or, better and consistent with the recorded practice, replace the count with the region assertion checklist row 4 already makes (no hunk touches `:411-424`, `:431`, `:593-624`), which is what brief Decision 5 actually protects. If R5's closure-table behavior is meant to bind reviewers, § Design 7 needs a fourth edit or an explicit note that R5 is author-facing only.

### F-2: R2's "nothing reads, changes, or removes a row" contradicts Design 5, and leaves a renamed section as an unfixable routing-violation P0
**Severity:** P1
**Where:** spec § Design 2 R2 (last sentence) vs § Design 5 (extraction rule) and § Design 7 item 2 (well-formedness)
**Convention violated:** The repo's supersede-and-state pattern — do not leave two contradicting statements of the same contract in one file (`decisions/2026-08-09-review-round-artifacts-are-immutable.md` applies the same "mark and link, never leave the record disagreeing with itself" discipline). Also brief Decision 1, whose whole point is that a well-formed deferral stops being re-filed.
**Evidence:** R2 ends: "*Nothing in `/spec-cycle` reads, changes, or removes a row once written.*" Design 5 says the opposite in the same spec: "*the render reads each `### D-<n>:` heading and the labelled fields under it*", and it runs at both exits. That is the soft half. The load-bearing half is `changes`: § Design 7's well-formedness test requires "*every named site either exists in the spec or is marked `(new)`*", and a row that fails it is "*a routing violation: file it as a P0 finding titled `routing violation: D-<n>`*". Spec sections get renamed in normal operation — an in-place rewrite in rounds 1–3 (`SKILL.md:432`, "*if a section is rewritten, that's fine*") or a round-4 REWRITE (`SKILL.md:438-441`). The moment a rename lands, a previously well-formed row's `Propagation sites` name a section that no longer exists; the reviewer must file a P0, and R2 forbids the author from re-anchoring the row to fix it. D15 exempts the deferral section from FROZEN/REWRITE but says nothing about rows whose *targets* were rewritten. The result is a gate that cannot go green, produced by a legitimate edit — the exact oscillation this ticket exists to end.
**Suggested fix:** Narrow R2 to what it means and add the re-anchor allowance. Replace the last sentence with: "`/spec-cycle` never removes a row and never rewrites its `Finding`, `Deferred in`, `Where`, `Suggested fix`, or `Follow-up` fields; § Design 5 reads every row to render the report. When a later round renames or removes a spec section a row's `Where` or `Propagation sites` names, the author re-anchors those two fields to the new heading in the same round and appends `(re-anchored round <n>)` — the finding record is unchanged, so the row stays well-formed." Add the mirror clause to § Design 7's block ("a re-anchored site is not a routing violation") so the byte-identical consumer text matches the producer, and note the re-anchor in D15 as the round-4 case.

### F-3: Checklist row 6's `grep -c 'DEFERRED, or NEW'` cannot match — the enumeration wraps across lines in three of the four agents
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 6, second assertion
**Convention violated:** The repo's recorded prose-spec gate-script practice — "re-verify backtick phrases with `grep -cF`" — and the spec's own § Scope row, which already acknowledges the wrap by citing two-line anchors.
**Evidence:** The current text in three files is line-broken exactly at the comma the grep spans:
```
   verify against the current spec whether it is CLOSED, PARTIAL, REOPENED,
   or NEW (a new variant of the same root). Render a closure table as the
```
(`agents/spec-reviewer-correctness.md:38-39`, `edge-cases.md:38-39`, `conventions.md:43-44` — the spec's own Scope row cites these as two-line ranges). Only `scalability.md:30` is a single unwrapped line. After the natural edit the text reads `… REOPENED, DEFERRED,` / `or NEW …`, so `grep -c 'DEFERRED, or NEW' agents/spec-reviewer-*.md` returns **0** in three of four files, not "1 per file". The implementer's only ways out are an undocumented reflow of three files or an undocumented edit to the checklist.
**Suggested fix:** Assert the token, not the phrase: `grep -c 'DEFERRED' agents/spec-reviewer-*.md` → 1 per file, four files (verified 0 today in all four). If the ordered enumeration itself must be pinned, use a multiline check and say so: `grep -cPzo 'REOPENED, DEFERRED,\s+or NEW' …`, run from Git Bash per the § Test plan preamble.

### F-4: Two different anchors for the same round-4 sentence, and neither is the sentence the spec describes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope row 3 and § Design 1 "Round 4" (`:436-441`) vs § Decisions D15 (`:438-441`)
**Convention violated:** Anchor precision on the one edit site the round-1 review asked the spec to name exactly (conventions/F-2's fix: "name the exact sentence at `:438-441` being qualified").
**Evidence:** § Scope: "*Round 4 (`:434-464`): one sentence qualifying the FROZEN/REWRITE enumeration at `:436-441`*"; § Design 1: "*The enumeration sentence at `:436-441` gains: …*"; § Decisions D15: "*The sentence at `:438-441` gains that qualification.*" In the file, `:435-437` is the enumeration sentence ("*Enumerate every section of the spec (…). For each, decide:*") and `:438-441` is the FROZEN/REWRITE definition pair. `:436-441` starts mid-sentence and is a range no statement in the file begins at. Checklist row 4's hunk range (`:426-464`) covers all three readings, so nothing fails — this costs the implementer a decision the spec should have made.
**Suggested fix:** Pick one and use it in all three places. Recommended: "*the FROZEN/REWRITE definition pair at `:438-441`*" (D15's form), since the qualification is about how a section is *classified*, not about the enumeration instruction. Update § Scope row 3 and § Design 1's "Round 4" paragraph to match D15.

### F-5: Design 3 emits two manifest line forms that Design 4 declares out of 2b's vocabulary and Design 7 never teaches the reviewers to accept
**Severity:** P2
**Where:** spec § Design 3 (bullets 2 and 3) vs § Design 4 ("Nothing else in 2b changes") and § Decisions D10 ("only `deferred:` is new")
**Convention violated:** Single source of truth for the manifest contract — 2b is the producer contract and the four agents are the consumer contract; the spec extends the emitted shape in a third place (Design 3) while both contracts say they are otherwise unchanged.
**Evidence:** Design 3 emits (a) a suffix on an existing phrase — "*append `(recount: <k> sites, fold kept)` to the disposition phrase*" — and (b) an entirely extra manifest line: "*The manifest gets an extra line for the reverted finding even though it is not a round-(N−1) finding: `<lens>/F-<k> (P<sev>) "<title>" — deferred: D-<n> (§ Deferred — follow-up required; revert of round <m> fold)`*". Form (b) directly contradicts the standing 2b rule the spec leaves untouched (`SKILL.md:369-371`): "*P0/P1 findings only*" from round N−1, and "*Map each P0/P1 finding to exactly one line*". It also contradicts the reviewer's own contract, which the agents state as "*author-stated disposition of each round-(N−1) P0/P1 finding*" (`correctness:18` etc.) — a reviewer reading a line for a finding that is not in round N−1's reports has no rule for it. Design 4 nonetheless says "Nothing else in 2b changes" and D10 says "only `deferred:` is new", so the spec asserts a vocabulary it then exceeds. (The row itself is covered by the ungated block, so the fallout is confusion rather than a re-file — hence P2, not higher.)
**Suggested fix:** Fold both forms into § Design 4's 2b touch, which the Scope row already opens (`:378-383`): add one sentence to the disposition prose — "a `fixed:`/`reworked:` phrase may carry a `(recount: <k> sites, fold kept)` suffix; a fold reverted under the recount adds one extra line for the original finding even though it predates round N−1, marked `revert of round <m> fold`" — and add the matching clause to § Design 7 item 1's `closure_manifest` input line so the consumer contract and the producer contract are edited together. Extend checklist row 4's 2b hunk expectation accordingly.

### F-6: The `docs/spec-workflow-reference.md` reconciliation is under-scoped — the reference would still frame the deferral machinery as round-2+ only
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope last row (`docs/spec-workflow-reference.md` `:84`, `:88`)
**Convention violated:** The repo's docs-reconciliation pattern for lifecycle-skill changes (VHS-15, -32, -33, -36 — 4-for-4), which reconciles the canonical reference to what actually ships, not just to the lines that changed verbatim.
**Evidence:** Line 88 is the *only* place the reference describes reviewer closure behavior, and it is explicitly round-scoped: "*Round 2+ closure tracking: Each reviewer reads all prior-round reviewer reports present … and produces a closure table showing which findings are CLOSED, PARTIAL, REOPENED, or NEW.*" The spec's fix adds only `DEFERRED` to that set. But the load-bearing property this spec spent two P0s establishing (correctness/F-2, edge-cases/F-1) is that the deferral block is **ungated** — § Design 7 item 2: "*Deferred findings (every round, including round 1)*", and § Design 6 restates it. After the reconciliation the reference still says the machinery is round-2+, which is the precise misreading the two P0s were about; a reader of the canonical doc would reproduce the original bug.
**Suggested fix:** Keep the edit inside the declared `:88` scope by extending that paragraph rather than only its status list: "*Round 2+ closure tracking … CLOSED, PARTIAL, REOPENED, DEFERRED, or NEW. Reopened items are P0 … **In every round, including round 1, each reviewer also checks the spec's `## Deferred — follow-up required` rows for well-formedness and does not re-file a finding whose root a well-formed row already carries.***" Add a checklist assertion to row 10: `grep -cF 'including round 1' docs/spec-workflow-reference.md` → 1.

### F-7: `routing violation: D-<n>` mandates a finding title — a silent spec-level addition against a fenced contract
**Severity:** P3
**Where:** spec § Design 7 item 2 (the block); cross-check § Decisions D10–D17 and the "Minor additions" bullet; § Out of scope 2
**Convention violated:** Silent spec addition (class (d)); brushes the reviewer output contract the brief fenced (brief Decision 6 / spec § Out of scope 2).
**Evidence:** The block instructs every lens to "*file it as a P0 finding titled `routing violation: D-<n>`, naming the failing field or rule*". No brief decision, ticket criterion, or spec decision authorizes a mandated title string; D10–D17 and the "Minor additions" bullet do not list it. The reviewer contract's finding shape is `### F-<n>: <Short title>` (`agents/spec-reviewer-conventions.md:127-158` and peers) — a free-text title. Mandating its content is a light touch on a surface § Out of scope 2 declares untouched ("*Any change to the reviewer output contract*"). The mandate is also the only place in the spec where a fixed finding title becomes a machine-readable key, without saying whether anything reads it.
**Suggested fix:** Add one clause to the "Minor additions" bullet: "the routing-violation finding carries a fixed title prefix `routing violation: D-<n>` so a reader can group them; nothing parses it, and the finding's shape is otherwise the standing contract (§ Out of scope 2 is unaffected)." Or drop the mandated title and say "*name the failing field or rule in the finding title*".

### F-8: Checklist row 3's parenthetical names three hit sites; there are four
**Severity:** P4
**Where:** spec § Test plan row 3
**Convention violated:** Edge-cases round-1 F-11(b) asked for the parenthetical to name the real hits; it now names three of four.
**Evidence:** Row 3: "*`grep -cF '## Deferred — follow-up required' skills/spec-cycle/SKILL.md` ≥ 3 (2e definition and shape, the D15 sentence, the Failure-modes bullet)*". § Design 1 step 4 also carries the `##` form — "*add a row to `## Deferred — follow-up required` (shape below)*" — so the post-edit count is 4, not 3. The `≥ 3` bound still passes, so nothing fails; the parenthetical just under-describes what a shortfall would mean.
**Suggested fix:** "≥ 4 (2e step 4's defer instruction, the shape heading, the D15 sentence, the Failure-modes bullet)".

## Summary
P0: 0 | P1: 2 | P2: 4 | P3: 1 | P4: 1

STATUS: RED P0=0 P1=2 P2=4 P3=1 P4=1
