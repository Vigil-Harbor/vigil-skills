# Conventions Review — round 3

Grounded against the spec, brief, `AGENTS.md`, the live skill files, and the wiki.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Roll-up omits Design 1's caller-facing constraints | CLOSED | spec.md:56–86 — roll-up now carries the legal-id rule, the all-or-none rule, "the three rules on when a verification runs", the round-preamble slot, and the ≈3-sentence bound |
| conventions | F-2 | Design 7 writes a third sentinel into a cell `spec-brief:139` owns | CLOSED | spec.md:598–601; row 12 (spec.md:764–767) asserts both |
| conventions | F-3 | § Deferred asserts every round-1 P2+ was folded; edge-cases F-14 was not | CLOSED | spec.md:905–926 — four real entries with reasons. (The *blanket* sentence survives at :928–929 and is false for a different finding — new F-3 below.) |
| conventions | F-4 | VHS-32 wiki decision's rejected alternative unacknowledged | CLOSED | spec.md:125–131 |
| correctness | F-1 | Three-vs-two open-frontier item shapes | CLOSED | spec.md:32, :659–664, :774–778 all read "three item shapes" |
| correctness | F-2 | Row 10 pins `options 1–3` at 4 vs Design 6's bullet | CLOSED | spec.md:571–573 uses the local "with 1–3" phrasing; verified live: `grep -c 'options 1–3'` = 4, `:703`/`:708` use "with 1–3" |
| correctness | F-3 | fence-empty line drops `not grillable` | CLOSED | spec.md:552, :555–561; `spec-cycle:700–703` confirms "their only record" |
| correctness | F-4 | `:139` collision + `## Scope` rendering | CLOSED | spec.md:598–603 |
| correctness | F-5 | `stop` erases the `(operator claim, …)` qualifier | **PARTIAL** | Structural half closed — precedence is now its own paragraph (spec.md:277). Substantive half open: spec.md:269–271 confines the qualifier to `fact not established`, and spec.md:376 still routes a `stop` to bare `stopped`. P2 retained → F-3 below |
| correctness | F-6 | "four-way" precedence | CLOSED | spec.md:76 |
| correctness | F-7 | "round-1 preamble" is not a defined surface | CLOSED | spec.md:456–462 |
| correctness | F-8 | Deferred overstates coverage | CLOSED | spec.md:905–911 |
| correctness | F-9 | D9's "extends" not in the roll-up | CLOSED | spec.md:83–86 |
| edge-cases | F-1 | Precedence contradicts its own stop sentence | CLOSED | spec.md:277–302 |
| edge-cases | F-2 | Rule 1 reinstates the retry it displaces | CLOSED | spec.md:357–367 |
| edge-cases | F-3 | "different fact" `F<n>` collision | CLOSED | spec.md:344–348 |
| edge-cases | F-4 | Precedence demotion hides an applied edit | CLOSED | spec.md:531–537 + :222–226 |
| edge-cases | F-5 | Withhold governs step 4, written in step 5 | CLOSED | spec.md:482–486 |
| edge-cases | F-6 | `unreferenced decisions applied` too narrow | CLOSED | spec.md:507–511 |
| edge-cases | F-7 | Zero-item resume burns the post-cap round | CLOSED | spec.md:412–416 |
| edge-cases | F-8 | fence-empty reaches Phase 3's revise option | CLOSED | spec.md:585–591 |
| edge-cases | F-9 | Empty-but-present headers defeat the drift-check | **DEFERRED (accepted)** | spec.md:912–919 + Risks 6; reason verified — the fix lands at `spec-cycle:640`, in Phase 3, outside the `### 2f-i` region the brief's Scope row scopes |
| edge-cases | F-10 | All-or-none has no reporting slot | CLOSED | spec.md:206–217 (see F-2 below on *where* it renders) |
| edge-cases | F-11 | No path for a true-but-not-repo-checkable fact | **DEFERRED (accepted)** | spec.md:920–924 + Design 8 + Risks 5; reason verified |
| edge-cases | F-12 | Completeness partitions with a non-seed set | CLOSED | spec.md:520–524 |
| edge-cases | F-13 | `not reached` rationale names one cause | CLOSED | spec.md:512–519 |
| edge-cases | F-14 | Legal-id bars `,` but not `;` | CLOSED | spec.md:201–205; separators pinned at :499–500 |
| edge-cases | F-15 | Scope-row fence admits a refuted `path:line` | CLOSED | spec.md:622–629 |
| edge-cases | F-16 | Two sentinels compete | CLOSED | spec.md:598–601 |
| edge-cases | F-17 | Row 2 cites row 10 | CLOSED | spec.md:688 now reads "(row 11)" |

(No `scalability.md` exists in `round-2/`; `scale_lens == off` — nothing to ignore.)

## Findings

### F-1: The spec amends `grilling:108` but leaves `## Failure modes` — which restates the same rules at `:148`, `:149` and `:151` — with no design, no prescribed text, and no checklist row

**Severity:** P1
**Where:** spec.md:28 (Scope table, `skills/grilling/SKILL.md` row), against spec.md:296–302 (Design 2) and spec.md:357–367 (Design 3 rule 1)
**Convention violated:** AGENTS.md § Plan & Spec Reviews; the repo's single-source-of-truth pattern; and the spec's own D12 "one meaning per term" (spec.md:173–177). Structurally: every other changed surface has a Design prescribing the new text *and* a checklist row asserting it — `## Test command` is `N/A`, so the checklist **is** the gate.
**Evidence:** `skills/grilling/SKILL.md:151`, read live, is a second statement of exactly the rule Design 2 amends:

```
- **`stop` with explorations in flight** — abandon them; their questions are Open with `unresolved because: stopped`.
```

Design 2 says that under v2 "the question it blocked renders `blocked-on: F<n>` … `:108` is amended to say so." `:151` is not named, so the shipped file would carry two contradictory prescriptions for the same input — the exact P0 that edge-cases R2 F-1 raised against the spec, relocated into the artifact. Two neighbouring bullets are in the same position:

- `:148` — "**Failed dispatch** (error, empty, or no fact returned) — the question becomes an `ℹ️` fact request in the next round" — which Design 3 rule 1 displaces for verification dispatches.
- `:149` — "**No read-restricted agent class in this host** — every fact need is rendered as a fact request" — which D5 overrides for an operator claim.

The Scope cell reads only "`## Failure modes` (`:146–151`): the new prohibitions and shapes" — a phrase that reads as *adding* bullets, not amending existing ones. No Design prescribes any `## Failure modes` text for `grilling`; checklist row 5 asserts only that the heading is a real `##` heading.
**Suggested fix:** Give the change a home in the designs. Design 2: "`:151`'s bullet is amended in the same hunk as `:108`…". Design 3: "`:148` gains 'except a verification dispatch, which is not retried', and `:149` gains the operator-claim branch." Extend checklist row 4 (or add 5a) to assert all three bullets by their new text.

### F-2: The all-or-none violation renders a line outside the hand-off block, which `grilling:116` says is rendered exactly — and 2f-i's verbatim append cannot capture it

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:212–217 (§ Design 1, "Reporting")
**Convention violated:** the cross-surface axis — the wire format between the primitive and its callers must be locked, not implied. `grilling:116` and `spec-cycle:523–528` are the two halves.
**Evidence:** `skills/grilling/SKILL.md:116`: *"End by rendering exactly this block in-conversation, then return."* The spec adds a rendered line **above** `## Grill summary` on any exit that renders no round, without naming `:116` as amended and without a checklist row pinning it. The consequence is one-sided: 2f-i is the **only** caller that supplies ids, so an all-or-none violation can only occur there — and `spec-cycle:523` appends "the returned Grill summary verbatim", starting at the `## Grill summary` header. A violation reported above that header is absent from `grill.md`, the artifact `/spec-close` archives as the record of why the spec moved.
**Suggested fix:** Either (a) put the no-round report on the header's `reason:` field or the first line *inside* the block, and say `:116` is unchanged; or (b) keep the line above the header, state that `:116` now admits one optional preamble line, and have Design 6 step 3 capture it in the `# Grill <k>` header line 2f-i already writes. Assert whichever in row 6.

### F-3: § Deferred's closing coverage claim is false again — correctness R2 F-5's substantive half is neither folded nor listed

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:928–929 (§ Deferred (P2+), closing sentence)
**Convention violated:** `skills/spec-cycle/SKILL.md:431`; the forward-closure principle in `vigil-harbor-wiki/decisions/2026-08-09-review-round-artifacts-are-immutable.md`. Same root as round-2 F-3, new instance.
**Evidence:** The sentence reads "Every other round-1 and round-2 P2/P3/P4 finding was folded…". Correctness R2 F-5 (P2, Pre-ship recommended) asked for one of two remedies: allow the qualifier on `stopped`, **or** state the F-item precedence explicitly and *record the information loss as accepted*. The spec did neither. spec.md:269–271 still confines the parenthetical to "an optional qualifier on the first value", and spec.md:376 still says "on a `stop` exit the reason is `stopped`". In the reachable case — operator answers `F1 <answer>` in round 2, verification in flight, operator types `stop` — the hand-off renders bare `stopped`, and Design 7's Phase 4 carry rule finds no qualifier. The brief author loses the fact that a human already asserted an answer.
**Suggested fix:** Cheapest honest close: one sentence in Design 2's F-item paragraph — "the qualifier may also attach to `stopped` (`unresolved because: stopped (operator claim, unverified)`), because the causal history survives the exit reason" — plus the same in row 7. Otherwise add a fifth § Deferred entry naming correctness R2 F-5 and the accepted loss, and replace the blanket sentence.

### F-4: Two spec-level additions are missing from the drift-check roll-up

**Severity:** P3
**Where:** spec.md:56–86
**Convention violated:** the roll-up's stated purpose (spec.md:57). `spec-cycle:636` renders the drift-check from the *brief's* decision list, so the roll-up is the only surface on which a spec-level addition reaches the HARD STOP.
**Evidence:** Two additions rationalized at their point of use but absent from the list:
- **The purpose-written `fence-empty` step-5 line** (spec.md:548–561), including the `not grillable` clause's survival. Brief decision 8 authorizes only that 2f-i "writes one short block to `grill.md`"; the brief's `spec-cycle` Scope row authorizes only "consume `ref:` in step 5 instead of title-matching".
- **`/grill-me`'s second failure-mode bullet and Risks 5** (spec.md:640–649, :864–869). The brief's `grill-me` Scope row authorizes one change — "Names `fence-empty` alongside `empty-seed`".
**Suggested fix:** Add two bullets naming both.

### F-5: The round preamble's relationship to `question_cap` is unstated, leaving Out-of-scope fence 1 on inference

**Severity:** P3
**Where:** spec.md:456–462 against spec.md:815–816
**Convention violated:** the fence's own terms. Out-of-scope 1 bars "any change to the three bounds"; `grilling:85` defines bound 2 as "At most `question_cap` **rendered items** per round".
**Evidence:** The preamble is "an optional one-line preamble above the round's first item". If an implementer reads it as a rendered item, a round that reports a contract violation asks one fewer question — a silent change to bound 2 on the exact path fence 1 protects.
**Suggested fix:** One clause in Design 5: "The preamble is not a rendered item: it does not count against `question_cap` and does not appear in the hand-off block." Add to row 9.

### F-6: `grilling:104`'s exit enumeration is not named among the lines that gain `fence-empty`

**Severity:** P4
**Where:** spec.md:424–425 and checklist row 8
**Evidence:** `grilling:104` reads "The exits are `empty-frontier`, `round-cap`, `stop`, `revised-after-cap (+1 round)` …, and `empty-seed`." Design 4's closing line says only "The **header's** exit enumeration gains `fence-empty`". Row 4 asserts the header; row 8 asserts the boundary sentences but not `:104`'s list.
**Suggested fix:** Row 8: add "`skills/grilling/SKILL.md`'s § Termination exit list names six exits including `fence-empty`."

## Verified, not findings

- **The two deferrals the orchestrator asked about are legitimate.** edge-cases R2 F-9's reason checks out: the fix belongs at `skills/spec-cycle/SKILL.md:640`, inside § Brief-section parsing rules under Phase 3 — outside `### 2f-i` (`:489–561`) and outside the one `## Failure modes` bullet, which is the entire `spec-cycle` surface the brief's Scope row authorizes. edge-cases R2 F-11's reason also checks out: folding it would admit a non-`path:line` source to `### Facts established`, reversing brief decisions 4 and 5 (the operator's own Q3/Q8 answers) — reversing a brief decision is a ticket, not a spec edit. Both are recorded as Risks as well as § Deferred, which is the shape 2g expects. Caveat, not a finding: neither follow-up names a ticket id, where D11 filed VHS-34; VHS-32's own § Deferred used "a follow-up candidate" with no id, so this matches precedent.
- **`## Deferred (P2+)`'s shape matches the repo, not `/spec-close`.** `skills/spec-close/SKILL.md` contains no reference to a Deferred section (grep: zero hits) — it walks Scope, Decisions, acceptance criteria and Test plan. The real consumers are `spec-cycle:431` and 2g, and the spec satisfies both.
- **Amending `grilling:108` does not breach the brief's fence.** Fence item 1 bars the three bounds, the fork form, the advisory rule and the fact-finding dispatch rules. `:108` is § Termination, inside the brief's own declared `:102–112` range, and the change is rendering vocabulary, not a dispatch rule. Disclosed in the Scope table, the roll-up, Design 2 and row 4.
- **The round preamble does not breach the fork form.** It is a new construct beside the four existing ones; row 5 still asserts the fork block verbatim. The `## Per-round output contract` range the brief scopes (`:33–58`) covers it. The only gap is the `question_cap` interaction — F-5.
- **"Files to leave alone" is accurate.** Grepped `README.md`, `AGENTS.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `lint.py`, `sync.py`, `tests/` for `empty-frontier` / `empty-seed` / `Grill summary` / hand-off paraphrase: zero hits outside `docs/spec-workflow-reference.md:23`/`:35` and the two skills already in Scope. AGENTS.md's only `grilling` paraphrase is the bounds, which do not change.
- **Every anchor re-verified live at `7403cb5`.** `grilling` `:48`, `:52–55`, `:57`, `:72`, `:74`, `:76`, `:85`, `:88`, `:104`, `:106`, `:108`, `:110`, `:116`, `:119`, `:122`, `:125–126`, `:129`, `:136–138`, `:146–151`; `spec-cycle` `:431`, `:489–561`, `:495`, `:507–509`, `:518–528`, `:539–546`, `:548–554`, `:640`, `:698–708`; `spec-brief` `:86`, `:88`, `:92–107`, `:105`, `:113–128`, `:134–143`, `:139`, `:141`; `spec-workflow-reference` `:23`, `:33`, `:35`. All resolve.
- **D6 now engages the shipped prose, not just the wiki page.** `skills/spec-brief/SKILL.md:88` carries the rejected alternative verbatim, and Design 7's Phase 2 paragraph distinguishes `fence-empty` from it on the same terms.
- **No premature abstraction, no backwards-compat drift.**

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=1 P2=2 P3=2 P4=1
