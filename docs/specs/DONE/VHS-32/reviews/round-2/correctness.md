# Correctness Review — round 2

Grounding complete. All spec claims re-verified against the current files; the Plane ticket resolved from shared memory (namespace `skills`, tag-exact, confidence 1.00) and matches the brief. `git log` on the touched files: newest change to `skills/spec-cycle/SKILL.md` / `AGENTS.md` / `README.md` / `docs/spec-workflow-reference.md` is `a9e7581` (2026-06-16, VHS-15); `5e6d401` (2026-09-02) touches only `agents/*`, which the spec declares untouched. `python lint.py` run read-only: `0 error(s), 2 warning(s)` (`review-pr`, `ship-spec`) and `--strict` exits 0 — the spec's checklist-1 baseline is exact.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | docs cannot satisfy four-stage lifecycle | CLOSED | spec:22 (Scope row adds `## Skill 3: spec-close`), :23 (README `/spec-close` bullet), :27 (Scope note), :417 ("Four AI-driven skills"), :424–427, :429, :452 (`grep -c 'spec-close' … ≥ 1`). Verified both files are 0 today. |
| correctness | F-2 (P1) | D8 seed excludes scalability | CLOSED | spec:69 (D8 restated "every remaining P0/P1 … on disk"), :381 (halt block scalability line), :19 (Scope row). |
| correctness | F-3 (P1) | `--rounds 0` contradictory | CLOSED | spec:252 (`1 ≤ N ≤ 10` / `1 ≤ N ≤ 15`, "there is no `0` alias"); grep confirms no residual `--rounds 0` anywhere in the spec. |
| correctness | F-4 (P2) | "read-only by construction" over-claim | CLOSED | spec:37 (honesty note), :43 ("make no mutations of any kind"), :512 (Risk 10). |
| correctness | F-5 (P2) | `user_invocable: false` mechanism claim | CLOSED | spec:73, :148 ("the flag is advisory"), :513. |
| correctness | F-6 (P2) | Tool-use notes bold label vs heading | CLOSED (with a new side-effect) | spec:355 is now a real `## Tool-use notes` heading — but see new F-2 below on its level inside the spec doc. |
| correctness | F-7 (P2) | `facts_policy` dead parameter | CLOSED | removed; spec:103 states "There is no caller-side `facts_policy` switch". |
| correctness | F-8 (P2) | three stale anchors | PARTIAL | the three named are fixed (states.json `:235` ✓, `AGENTS.md:88–96`/`:95` ✓, regex `:43–48` ✓) but three *other* anchors in § References are wrong — new F-1 below. |
| correctness | F-9 (P2) | dry-run transcripts unproducible | CLOSED | spec:457 (authoring dry-run procedure, manual PR-body link), :460 (Run B now "at most 3 items"). |
| correctness | F-10 (P2) | `subagents: true` forecloses S5 | CLOSED (recorded) | spec:105 (contract limitation), :511 (Risk 9). |
| correctness | F-11 (P3) | `Factor: no` discarded | CLOSED | spec:338. |
| correctness | F-12 (P3) | `--questions 0` / `--no-grill` option 2 | CLOSED | spec:252, :309. |
| edge-cases | F-1 (P0) | same root as correctness F-1 | CLOSED | as above. |
| edge-cases | F-2 (P1) | empty seed → hollow brief | CLOSED | spec:125–127 (S9), :279, :287, :296, :158, :186, :461 (Run C). |
| edge-cases | F-3 (P1) | exploration hang/crash stalls round | CLOSED | spec:182 (failed-dispatch rule + per-round dispatch cap), :290, :367. Residual: a dispatch that hangs where the host reports no timeout is still outside the rule — not actionable in a prompt-only skill, so not raised. |
| edge-cases | F-4 (P1) | fact requests uncapped | CLOSED | spec:81 ("questions and fact requests together"), :103, :61, :184. |
| edge-cases | F-5 (P1) | revise: no invalidation/budget/address | CLOSED (mechanism gap → new F-4) | spec:117 (downstream return + `revised-after-cap`), :81 (monotonic Q numbers), :305, :309. |
| edge-cases | F-6 (P1) | overwrite guard + non-atomic write | CLOSED | spec:259–273 (brief/spec/reviews + git-status halt), :331 (tmp-then-rename). |
| edge-cases | F-7 (P1) | scale factor without target | CLOSED | spec:335–339; verified against `spec-cycle:598–603` malformed-scale behavior. |
| edge-cases | F-8 (P1) | host cannot invoke nested skill | CLOSED | spec:225, :296, :366, :398, :436, :511. |
| edge-cases | F-9 (P2) | flag boundary values | CLOSED | spec:252–254. |
| edge-cases | F-10 (P2) | 2f-i missing report / synthetic P0 | CLOSED (one corner open → new F-5) | spec:397 ("Not grillable"). |
| edge-cases | F-11 (P2) | `grill.md` overwritten | CLOSED | spec:123 (S8 append-only), :399. |
| edge-cases | F-12 (P2) | `--no-grill` invents decisions | CLOSED | spec:309 (explicit-statement-only derivation), :333 (`Interview: skipped (--no-grill)`). |
| edge-cases | F-13 (P2) | defer expands unbounded subtree | CLOSED | spec:114 (one rolled-up Open item), :204 (by-construction bound). |
| edge-cases | F-14 (P2) | `subagents: true` unconditional | CLOSED (recorded) | spec:105, :511; README Requirements reworded at :429. |
| edge-cases | F-15 (P2) | free-form / partial / `stop` in flight | CLOSED (one claim overstated → new F-3) | spec:116, :186. |
| edge-cases | F-16 (P3) | `user_invocable: false` unprecedented | CLOSED | spec:150 (1.0 guard), :513. Verified: all 8 shipped skills carry `true`. |
| conventions | F-1 (P0) | same root as correctness F-1 | CLOSED | as above. |
| conventions | F-2 (P2) | halt hardcodes three lenses | CLOSED | spec:381, :393. |
| conventions | F-3 (P2) | states.json path resolution | CLOSED | spec:274 uses `<config-dir>` per `spec-close:31` (verified). |
| conventions | F-4 (P2) | Phase 0 reads AGENTS.md first | CLOSED | spec:258 ("`CLAUDE.md` (or your harness's project-instructions file; in this repo that is `AGENTS.md`…)"). |
| conventions | F-5 (P2) | no origin-sync preflight | CLOSED | spec:275, matching `spec-close:37–42` (verified). |
| conventions | F-6 (P2) | `user_invocable` informational | CLOSED | spec:148. |
| conventions | F-7 (P2) | description trigger competition | CLOSED | spec:148 ("no user-phrase triggers"), :449. |
| conventions | F-8 (P2) | `--rounds 0` dual meaning | CLOSED | spec:252. |
| conventions | F-9 (P3) | S6–S8 mislabelled | CLOSED | spec:31 ("S1–S5 pin the five forks the brief explicitly deferred … S6–S9 are spec-level additions"). |
| conventions | F-10 (P3) | inconsistent menu idiom | CLOSED | spec:261–271 and :302–307 both fenced, one option per line, "Wait for the user's response." |
| conventions | F-11 (P4) | `AGENTS.md:23–31` overshoot | CLOSED | spec:21 now `:23–29`; verified `:23` is the "Three skills" sentence and `:29` the last item. |
| conventions | F-12 (P4) | README Requirements implies Python | CLOSED | spec:429. |

All round-1 P0/P1 items are CLOSED. The one PARTIAL (correctness F-8) is P2 and is carried as new F-1.

## Findings

### F-1: Three wrong `spec-cycle` line anchors in § References — one points at a different Phase 0 step entirely
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:518 (§ References, `skills/spec-cycle/SKILL.md` bullet)
**Claim:** "Phase 0 step 1 regex `:43–48`, step 3 … `:61`, **step 5 origin check `:74–81`**, step 7 `states.json` `:235`, **step 8 scale `:238`**, **2b closure-manifest synthetic P0 form `:376–381`** …"
**Why this is wrong:** verified against `skills/spec-cycle/SKILL.md` (620 lines):
- **Step 5 (origin sync) begins at `:133`**, not `:74`. Lines `:73–83` are *step 4*'s upstream check (`git symbolic-ref refs/remotes/upstream/HEAD`, `git fetch upstream`). The spec's Phase 0 step 4 deliberately models `/spec-close`'s origin check rather than `/spec-cycle`'s (which offers a fast-forward), so an implementer who follows this anchor lands on the wrong skill's wrong remote.
- The **synthetic missing-STATUS P0 form** is at `:371–375` (`A synthetic missing-STATUS P0 … appears as '<lens>/STATUS (P0) "missing STATUS line"'`); `:376–381` is the closure-verification/mapping prose. § Design 4 step 1 (spec.md:397) leans on that form to define "not grillable".
- **Step 8 scale** starts at `:237`, not `:238` (off by one — trivial).
Every *edit-site* anchor re-verifies clean: 2f `:466–485` ✓, 2e `:426–465` ✓, 2g `:487–518` ✓, Tool-use notes `:570` ✓, Failure modes `:578` ✓ (heading text is "Failure modes to watch for"), Phase 3 `:520` ✓, malformed-scale `:598–600` ✓, `spec-close:31` / `:37–42` / `:312` / `:339–340` ✓, `ship-spec:20` / `:197` / `:241` ✓, contract §2 `:26–43` / `:34` / §3 `:47–103` / `:65` / `:78` / §4 `:107–119` / §5 dim 3 `:129` ✓, `lint.py:24–33` / `:45–48` / `:57,216–217` ✓, `VHS-20/spec.md:153` ✓, `bloat-check:19` ✓, `AGENTS.md:23–29` / `:88–96` / `:95` ✓, `README.md:7–11` / `:54–59` ✓, `spec-workflow-reference.md:3` / `:7` / `:162` ✓, wiki decision file exists ✓. That is why this is P2 and not P1: no anchor an implementer edits against is wrong.
**Suggested fix:** in § References change to "step 5 origin check `:133–233`", "2b closure-manifest synthetic P0 form `:371–375`", "step 8 scale `:237`".

---

### F-2: `## Tool-use notes` and `## Failure modes` are emitted at `##` inside § Design 3, so Design 4/5/6 fall under a "Failure modes" heading
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:355, :359 (inside `### 3. skills/spec-brief/SKILL.md`), affecting spec.md:371, :409, :431
**Claim:** spec.md:355 `## Tool-use notes` — "(A real `## Tool-use notes` heading in the skill file — contract §4 case 3, matching `spec-cycle:570`.)"; spec.md:359 `## Failure modes`.
**Why this is wrong:** the intent (verified correct) is that the *authored skill file* carry `##` headings, because `lint.py:57` matches `_NOTES_HEADING_RE` against `cur_heading`, which `lint.py:216–217` sets only from lines beginning with `#`. But writing them at `##` **in the spec document** closes `## Design` at line 354: `### 4. skills/spec-cycle/SKILL.md — 2f fourth option` (`:371`), `### 5. Documentation edits` (`:409`) and `### 6. Portability and lint posture` (`:431`) now sit under `## Failure modes`, and the spec appears to declare its own top-level `## Tool-use notes` / `## Failure modes` sections. Compare the sibling case at spec.md:315–329, where the brief template is safely inside a fence. Round-1 correctness F-6 asked for a real heading; the fix landed at the wrong nesting depth.
**Suggested fix:** demote to `#### Tool-use notes` / `#### Failure modes` (or put the two blocks inside a fenced excerpt, as the Phase 4 template is), keeping the parenthetical that says the skill file itself uses `##`. Checklist 9 (spec.md:453) already asserts the skill-file requirement, so nothing is lost.

---

### F-3: S7 says the round-budget cost is stated "where the operator sees it", but § 1.3's verbatim closing lines do not say it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:115 (S7, "Omitted") vs spec.md:173–176 (§ Design 1.3 literal round-footer block)
**Claim:** S7: "A partially answered round still consumes one round of budget — that is the price of D4's no-silent-default rule, **and the spec says so where the operator sees it (Design 1.3's closing line)**."
**Why this is wrong:** the literal block § 1.3 pins is: `Answer by number. "defer" moves a question to the open frontier; a free-form answer is recorded as given.` / `"stop" ends the interview. Unanswered questions are re-asked once, then deferred. Round <n> of <round_cap>.` Nothing there says a partially answered round consumes a round. § 1.3 is marked as the *contract* wording ("Each round ends with the literal lines"), so an implementer writing `grilling` reproduces it verbatim and the operator-visible statement S7 promises never exists. This is the cross-section pattern the round-1 lenses flagged twice (a prose claim about a code block the block does not carry).
**Suggested fix:** add the clause to the literal block, e.g. `… Unanswered questions are re-asked once, then deferred; a partly answered round still uses one of your <round_cap> rounds.` — or drop the "and the spec says so where the operator sees it" claim from S7.

---

### F-4: Phase 3 option 2 (revise) has no defined re-entry into the primitive — § 1.1's invocation contract has no input for the settled tree
**Severity:** P2
**Where:** spec.md:117 (S7 revise bullet), :305 (Phase 3 option 2) vs :152–157 (§ 1.1 Invocation contract) and :182 ("No resume state is kept")
**Claim:** Phase 3 option 2: "Revise an answer (name the Q number) — that decision and everything settled downstream of it return to the frontier; one extra round is granted if the cap was hit." S7 assigns the same rule to the primitive ("Revise (Phase 3 option 2, by global Q number)"), and § 1.7 makes `revised-after-cap` a `grilling` exit token.
**Why this is wrong:** by Phase 3 the primitive has already terminated — § 1.8 says it "ends by rendering exactly this block in-conversation and **returning**". § 1.1's inputs are only `seed`, `altitude`, `round_cap`, `question_cap`; there is no `prior_state` / settled-tree input, and § 1.5 explicitly says no resume state is kept. So the spec never says *how* the caller re-enters: re-invoke `grilling` (with what seed?), or continue the interview in-conversation without re-invoking. An implementer authoring `skills/spec-brief/SKILL.md` has to invent the mechanism, and whichever they pick, the `revised-after-cap` token has to be produced by a second invocation that thinks it is at round 0. Nothing else in the design is under-specified this way — Phase 2's invocation is explicit.
**Suggested fix:** one sentence in Phase 3 option 2 and one bullet in § 1.1. E.g. § 1.1 gains "`prior_summary` (optional) — a returned Grill summary to resume from; the named decision and its downstream items re-enter the frontier, `rounds_used` carries over, and the exit token becomes `revised-after-cap` if the cap was already hit"; Phase 3 option 2 gains "…`/spec-brief` re-invokes `grilling` with the Grill summary as `prior_summary` and the same bounds."

---

### F-5: A 2f-i seed in which every finding is "not grillable" collides with S9's never-write-on-`empty-seed` rule
**Severity:** P2
**Where:** spec.md:397 (Design 4 step 1), :399 (step 3), :401 (step 5) vs :127 (S9) and :186 (§ 1.7)
**Claim:** Step 1 excludes missing/unparseable reports and synthetic `missing STATUS line` P0s from the seed. Step 3: "Append the returned Grill summary verbatim to `…/round-4/grill.md`." Step 5 prints `grill applied: <s> … — docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`. S9: "callers treat `empty-seed` as a halt and **never write on it**", and § 1.7 says `empty-seed` alone does *not* go through the § 1.8 hand-off.
**Why this is wrong:** 2f-i is reached exactly on the pathological path where reviewers may have crashed — `spec-cycle:581` treats a status-less report as `RED P0=1` without necessarily writing a file, and `spec-cycle:404–409` writes a stub only for the *scalability* lens. If every remaining P0/P1 is a synthetic or unavailable-report item, step 1 yields an empty seed, `grilling` exits `empty-seed`, and there is **no Grill summary to append** — yet step 3 is unconditional and step 5 prints a path to a file that was never created. Two spec rules give opposite instructions for the same state.
**Suggested fix:** add a guard to Design 4 step 1: "If the seed is empty after these exclusions, do not invoke `grilling`. Print `nothing grillable — every remaining finding is a dispatch failure; option 1 re-dispatches the affected lens(es)`, write no `grill.md`, and re-render the menu with options 1–3."

---

### F-6: The brief's `## Scope (verified against current files, <date>)` table has no derivation rule
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:323 (Phase 4 template), :333 (mapping rules)
**Claim:** the only rule touching Scope is "Facts → the Scope table's 'Current' column and `## References` (with `path:line`)". Settled → Decisions carried forward; Open → Risks / decisions; exit token → References.
**Why this is wrong:** the emitted header makes a verification claim ("verified against current files, `<date>`") that the spec itself relies on elsewhere — Phase 0 step 4's origin warning says "the brief's 'verified against current files' claim may be stale" (spec.md:275). But nothing says which rows the table gets (the target files/paths), where the "Change" column comes from, or what discharges the "verified" claim (Phase 1 grounding? a `path:line` per row?). `docs/specs/DONE/VHS-11/brief.md:25–47` — the shape the spec names as its target and which I verified has exactly this 3-column table — is the only guide, and the spec cites it only for the `## Risks / decisions` convention. Every other section has an explicit mapping rule; the one that asserts ground truth has none.
**Suggested fix:** add one mapping line: "Scope rows are the files the settled decisions and grounding facts name, one row per path, `Current` filled from a fact with its `path:line` and `Change` from the settled decision that touches it; a path with no read file or fact behind it does not get a row — it goes to `## Risks / decisions`. The heading date is the date grounding ran."

---

### F-7: Phase 4's `## Scale` rule inverts the factor/target dependency
**Severity:** P3
**Where:** spec.md:336
**Claim:** "The target is a prerequisite of the factor question (S4's example asks both), so the primitive asks it in the same round."
**Why this is wrong:** the dependency runs the other way — you need a target only *if* scale is a factor, so the factor is the prerequisite. And as written ("asks it in the same round") the sentence also reads as two questions in one round, which § D5 / § 1.2 forbid for a question whose prerequisite is open in that round. S4's example (spec.md:98) actually resolves it by making them **one** question ("Is scale a factor for this ticket — do we dispatch the scalability lens, and at what target N?"), which is consistent; only the Phase 4 sentence is wrong.
**Suggested fix:** "The factor and its target are one question, not two (S4's example asks both in a single item), so a settled 'yes' normally arrives with its N."

---

### F-8: "three states" labels a four-bullet rule
**Severity:** P4
**Where:** spec.md:335–339
**Claim:** "**`## Scale` emission** (three states, matching `AGENTS.md:95` and `/spec-cycle` Phase 0 step 8)" followed by four bullets.
**Why this is wrong:** the three states are the *emitted* shapes (`Factor: yes` + target / `Factor: no` / no section), matching `scale_lens ∈ {on, non-factor, off}` at `skills/spec-cycle/SKILL.md:239` — but the rule enumerates four input cases, so the count reads as an error. (`AGENTS.md:95` verified: three declared states.)
**Suggested fix:** "(four input cases, three emitted shapes …)".

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 1 | P4: 1

STATUS: GREEN
