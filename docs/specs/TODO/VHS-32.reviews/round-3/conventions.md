# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P1) | `empty-seed` unhandled at 2f-i / `/grill-me`; step 3 contradicts S9 | CLOSED | Design 4 Edit 2 step 1 guard spec:403 ("do not invoke `grilling`… write nothing to `grill.md`… re-render 1–3"); Design 2 spec:226; S9 names all three callers spec:127; checklist 7 spec:459 greps `nothing grillable` |
| edge-cases | F-2 (P1) | Hung exploration blocks the round while § 1.5 asserts it cannot | CLOSED | § 1.5 spec:183 now states the blocking case explicitly; D2 sentence gains the work bound spec:43; Risks 12 spec:523; Failure modes spec:373 |
| edge-cases | F-3 (P2) | `--no-grill` can never emit `## Scale` | CLOSED | Fifth bullet spec:343 |
| edge-cases | F-4 (P2) | Failed grounding dispatch under `--no-grill` is dropped | CLOSED | Phase 1 step 4 spec:292; Failure modes spec:373 |
| edge-cases | F-5 (P2) | Fact-dispatch cap has no overflow rule | CLOSED | § 1.5 spec:183 ("carry to the next round's batch by the S1 ordering… `fact not established`") |
| edge-cases | F-6 (P2) | Post-cap revise re-selectable without limit | CLOSED | S7 spec:117 ("one post-cap revision round … per invocation", token `revised-after-cap (+1 round)`, option 2 withdrawn); Phase 3 spec:311 |
| edge-cases | F-7 (P2) | Origin-behind warning transient, Scope claim durable | CLOSED | Phase 4 mapping spec:336 (annotated heading + matching References bullet) |
| edge-cases | F-8 (P2) | `grill.md` append: no atomicity, dedup key, durable once-signal | CLOSED | S8 spec:123 (read-modify-tmp-rename, `# Grill <k>`, last-writer-wins, datetime-vs-preflight backstop); Design 4 step 3 spec:405 |
| edge-cases | F-9 (P3) | `## Scale` had no slot in the section order | CLOSED | Fenced list spec:329 |
| edge-cases | F-10 (P3) | S9 re-prompt unmechanized in ticket mode | CLOSED | S9 spec:127 (ticket-mode re-prompt verbatim; header keeps the resolved ticket line) |
| edge-cases | F-11 (P3) | Leaked `.tmp` invisible to the artifacts check | CLOSED | Dot-prefixed temp spec:334; `stale:` row spec:267; option 1 removes it spec:271 |
| edge-cases | F-12 (P3) | Artifacts-halt option 1 worded for a branch that may not hold | CLOSED | spec:271 (conditional wording; spec never read as grounding) |
| edge-cases | F-13 (P3) | Empty `## Decisions carried forward` reads as satisfied | CLOSED | Phase 4 spec:336 sentinel `_(none settled — see Risks / decisions)_` + warning. *(Note: `spec-cycle:560` still enumerates zero items; the sentinel is the visible marker the finding asked for.)* |
| correctness | F-1 (P2) | Three wrong `spec-cycle` anchors | CLOSED | spec:529 now `:133–233`, `:237`, `:371–375` — all three re-verified on disk this round |
| correctness | F-2 (P2) | `##` headings inside Design 3 swallow Design 4–6 | CLOSED | spec:359, :365 demoted to `####`, parenthetical retained |
| correctness | F-3 (P2) | Round-budget cost absent from § 1.3's literal block | CLOSED | spec:176 ("a partly answered round still uses one of your `<round_cap>` rounds") |
| correctness | F-4 (P2) | Revise had no re-entry into the primitive | CLOSED | `prior_summary` input spec:157; Phase 3 spec:311 |
| correctness | F-5 (P2) | All-not-grillable 2f-i seed collides with S9 | CLOSED | Same guard as edge-cases F-1, spec:403 |
| correctness | F-6 (P2) | Scope table had no derivation rule | CLOSED | spec:336 (one row per named path, `Current` from a fact `path:line`, `Change` from the settled decision, no-fact → Risks) |
| correctness | F-7 (P3) | Factor/target dependency inverted | CLOSED | spec:339 ("one question, not two") |
| correctness | F-8 (P4) | "three states" over a four-bullet rule | CLOSED | spec:338 ("four input cases, three emitted shapes") |
| conventions | F-1 (P2) | Spec-additions ledger incomplete | CLOSED | Preamble spec:31 enumerates five point-of-use additions. *(A v3 residue raises a new P3 — F-4 below.)* |
| conventions | F-2 (P2) | Undotted `.tmp` vs the repo's atomic-write shape | CLOSED | spec:334 `.<TICKET-ID>.brief.md.tmp` citing `prepend_log_entry.py:370–375`; Tool-use notes spec:361 names the rename as the lone mutation; Phase 0 step 2 reports/removes a stale tmp |
| conventions | F-3 (P2) | Upstream name collision undocumented | CLOSED | Design 6 spec:445; `AGENTS.md` bullet spec:423; checklist 12 spec:464; Risk 13 spec:524. *(Placement and prior-decision engagement raise new findings — F-1/F-2 below.)* |
| conventions | F-4 (P4) | "Deferred (P2+)" mislabeled | CLOSED | spec:548 retitled |

All round-2 P0/P1s CLOSED. No REOPENED items. No PARTIALs.

## Findings

### F-1: The name-collision decision inverts half of the VHS-28 posture the spec claims to follow, and never engages that decision's explicit revisit trigger

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D10 (`:75–77`); § Design 6 (`:445`); § Risks 13 (`:524`); § References (`:543`)
**Convention violated:** prior decision `vigil-harbor-wiki/decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md` — its § Revisit trigger and its § Consequences
**Evidence:**

- D10 (`spec.md:77`) states *"Same posture as VHS-28 toward the vendor handoff skill."* VHS-28's posture has two halves. The spec adopts the clean-room half and **inverts** the other: VHS-28 superseded under a **different** name (`session-handoff`, not `agentcraft-handoff`) and therefore needed a hand-run operator removal; VHS-32 supersedes under the **same** name and relies on `sync.py` clobbering the upstream copy. "Same posture" is true of the rewrite and false of the supersession mechanism.
- That decision carries a revisit trigger this ticket fires:

  > | A **second** vendor skill needs superseding | Two instances is the threshold where a tracked uninstall manifest starts to beat a prose note. Reconsider option 2 then, not before |

  VHS-32 is the second supersession event in this repo. The spec never cites the decision page, so the trigger is neither honored nor dismissed. § References `:543` cites `state.md`'s VHS-28 *notes* and the VHS-15 decision file, but not this one.
- The disposal is short and favorable, which is why the omission is worth closing rather than living with: the decision's own § Consequences records *"`sync.py` stays non-destructive. It installs and overwrites; it does not delete"* — the exact property VHS-32 depends on. And VHS-28's hard half (*"both skills then exist on the operator machine, with overlapping descriptions, and the harness routes handoff requests to whichever one matches first"*) is precisely what the same-name choice **avoids**. The spec is on the right side of the recorded rule and doesn't say so.

**Suggested fix:** one sentence in Design 6's name-collision paragraph (or Risk 13) — *"This is the second supersession of a third-party skill in this repo, the revisit trigger in `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md`. A tracked uninstall manifest is still not warranted: unlike `agentcraft-handoff`, the same-name install overwrites in place, so there is no operator removal step and no description-matching ambiguity between two coexisting copies."* — plus a § References bullet for the decision file, and a clause in D10 narrowing "same posture as VHS-28" to the clean-room rewrite.

---

### F-2: The `AGENTS.md` § Superseded vendor skills edit has no defined slot, and the section's only bullet list is scoped "Two warnings:" about a different skill

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope table (`:21`); § Design 5 (`:423`); checklist 12 (`:464`)
**Convention violated:** the structure of `AGENTS.md` § Superseded vendor skills (`AGENTS.md:59–80`), which VHS-28's decision calls "the executable record"
**Evidence:** the spec says *"`AGENTS.md` § Superseded vendor skills gains one bullet"* and gives the bullet text. That section has exactly one bullet list, and it is introduced by a counted lead-in:

`AGENTS.md:61–80` — prose about `agentcraft-handoff`, a blockquoted removal command, then:

> Two warnings:
>
> - **Targeted removal only. Do not reach for `python sync.py install --prune`.** …
> - **This departs from recorded practice, deliberately.** `README.md` promises that separately-installed skills are preserved. …

An implementer following "gains one bullet" appends there — which makes "Two warnings" enumerate three, and files a note about `grilling`/`grill-me` overwrite-in-place under warnings scoped to the AgentCraft **removal**. The two topics are also opposites: that list warns *against* deleting third-party skills; the new bullet documents *overwriting* one.

Checklist 12 (`:464`) only asserts `grep -c 'mattpocock' AGENTS.md ≥ 1`, so the misplacement passes the gate.

Note also that the second existing warning already names `README.md`'s preservation promise as the thing being departed from. VHS-32 is a second, differently-shaped departure from the same `README.md:30` sentence (verified: *"Files in those directories that aren't in this repo … are preserved by default"* — a **same-named** third-party skill is not preserved).

**Suggested fix:** pin the insertion point in Design 5: a short paragraph (not a bullet) appended **after** the section's closing "If AgentCraft reinstalls its copy…" paragraph, under its own bolded lead — e.g. *"**`grilling` / `grill-me` (VHS-32) — superseded by overwrite, not removal.** …"* — leaving the "Two warnings:" list byte-identical. Extend checklist 12 to assert the list still reads `Two warnings:` with exactly two bullets.

---

### F-3: README's tagline and § Requirements are left describing the pre-VHS-32 shape, while the sibling doc's identical intro sentence is explicitly rewritten

**Severity:** P3
**Where:** spec § Scope table (`:23`); § Design 5 (`:437`); Done when 9 (`:488`); checklist 8 (`:460`)
**Convention violated:** internal consistency of the three tracked docs the ticket's Done-when names; the spec applies the fix to one of two parallel intro sentences
**Evidence:**

- The spec rewrites `docs/spec-workflow-reference.md:3` from "Two AI-driven skills that split spec authoring from implementation…" to a four-stage sentence (`spec.md:425`) — correct, and for exactly the right reason.
- `README.md:3` is the same class of sentence and is untouched: *"A Plane.so-aware spec → review → ship workflow with parallel reviewers, plus a CodeRabbit triage handler."* After the edit, § Skills four lines below it lists six entries including a brief stage, a close stage, and an interview primitive that the tagline does not describe. The Scope row for `README.md` names only `:7–11` and `:54–59`.
- § Requirements: Design 5 adds a line for `/spec-brief` and `/grill-me`, but `/spec-close` — which the same change is adding to § Skills — gets no Requirements line, while the existing `:58` bullet still reads "For `/spec-cycle` and `/ship-spec`: a Plane.so workspace with the plane-proxy MCP server, and `gh` CLI authenticated." `/spec-close` needs Plane state and (for the wiki half) a wiki checkout. Checklist 8 only greps for a *mention* of `spec-close`, so the gap passes.

**Suggested fix:** add `README.md:3` to the Scope row and Design 5 with a one-clause rewrite ("…a Plane.so-aware brief → spec → review → ship → close workflow…"), and either extend the existing `:58` Requirements bullet to name `/spec-close` or give it its own line.

---

### F-4: Two v3 additions change the emitted brief's bytes but are not in the `:31` spec-additions ledger

**Severity:** P3
**Where:** spec § Decisions preamble (`:31`); § Design 3 Phase 4 mapping rules (`:336`)
**Convention violated:** the drift-check classification in `agents/spec-reviewer-conventions.md` § "Silent spec additions vs the brief" — the same root as round-2 conventions F-1, now with v3 residue
**Evidence:** `:31` enumerates five point-of-use additions and presents that list as what "the drift check sees". Two v3 mapping rules that change the brief artifact are outside it:

1. **Empty-Settled sentinel** (`:336`) — *"if Settled is empty, write `_(none settled — see Risks / decisions)_` under the header rather than leaving it blank."* This puts a non-numbered line under a header `skills/spec-cycle/SKILL.md:560` parses as "enumerate the numbered list under the header". Harmless (verified: no consumer breaks) but it is a new artifact convention with no brief or ticket authorization and no ledger entry.
2. **Conditional Scope-heading suffix** (`:336`) — `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)`. The brief's Scope heading is no longer a constant string. It nests under the ledgered origin check, but the ledger names the *check*, not the artifact-format consequence, and the brief's Done-when pins "the established sections".

Neither is wrong; both are (d) silent additions relative to the enumeration `:31` promises is complete.

**Suggested fix:** extend `:31`'s sentence to close the class rather than re-enumerating forever — e.g. *"…and the Phase 4 emission rules these imply (the empty-Settled sentinel, the origin-annotated Scope heading)."*

---

### F-5: `grilling` owns failure semantics its three callers branch on, but gets no `## Failure modes` section, and no checklist row asserts its `## Tool-use notes` is a real heading

**Severity:** P4
**Where:** spec § Design 1 skeleton (`:131–209`, esp. 1.5/1.7/1.10); § Design 6 bullet 2 (`:442`); checklist 4, 9 (`:456`, `:461`)
**Convention violated:** the lifecycle-skill section convention — `skills/spec-cycle/SKILL.md:570/578`, `skills/spec-close/SKILL.md:428/438`, `skills/ship-spec/SKILL.md:261/270` all pair `## Tool-use notes` with a Failure-modes section
**Evidence:** `grilling` at ≈170 lines carries `## Tool-use notes` (1.10) but no Failure-modes heading; its failure semantics (failed dispatch, no read-restricted agent class, `empty-seed`, `stop` with explorations in flight) are distributed across 1.5, 1.7 and S5 — and all three callers' own Failure-modes sections branch on them (`spec.md:226`, `:373`, `:404`). `/spec-brief` and `/spec-cycle` both get the paired section; the primitive they depend on does not.

Separately: Design 6 bullet 2 makes the case-3 lint exemption depend on `grilling`'s `## Tool-use notes` being a **heading** (`lint.py:57, 216–217` — verified, `_NOTES_HEADING_RE` matches only `cur_heading`). Checklist 9 asserts that for `spec-brief`; checklist 4 enumerates `grilling`'s verbatim content but never asserts its heading level.

**Suggested fix:** add a short `## Failure modes` section to the § 1 skeleton (four lines, pointing at 1.5/1.7 rather than restating them), and extend checklist 4 with "…and `## Tool-use notes` is a real `##` heading."

---

## Notes on the axes that came back clean

- **Contradicts a prior decision.** Re-verified against all five VHS decision pages plus the three from 2026-08. `2026-06-14-vhs-17-requires-tolerated-not-strict-yaml` — all three `requires:` blocks flat, controlled-vocabulary, after the scalars; `services: [issue-tracker?, shared-memory?]` is valid against `lint.py:48`'s `SERVICES_VOCAB` (verified). `2026-06-14-vhs-18-lint-warn-only-strict-gate` — the `mcp__*`-only gap stays Risk 8, matching `lint.py:24–33`'s own documented v1 limitations. `2026-06-16-vhs-15-optional-scalability-lens` — the halt-block scalability line closes a residual hardcode rather than adding one. `2026-06-18-vhs-20-hermes-preflight-advisory` — D9 rests on the guard sentence, not the dropped flag. `2026-08-25-vhs-29-anchor-is-a-refusal-contract` — `grill.md`'s append-with-`---` is an audit trail, not the newest-first `log.md` contract. The one live conflict is F-1 above.
- **Premature abstraction.** Unchanged: `grilling` has N=3 real callsites, above the N≥3 bar, and the spec still declines the general Nth-lens registry that VHS-15 § Consequences already rejected.
- **Reuse vs duplicate.** `/spec-brief` Phase 0's four restated preflight steps remain justified by `prepend_log_entry.py:365–368` ("Deliberately a second implementation: skills install independently … and share no importable module"), and v3 keeps picking the better live precedent (`spec-close`'s `<config-dir>` resolution, its warn-only origin shape, its dot-prefixed atomic write).
- **Unneeded backwards-compat.** None. No shims, no `_unused`, no re-exports, no flags kept for compatibility; `--no-grill` is a stated D9 requirement.
- **Repo-level conventions re-checked live.** `AGENTS.md:93` (`sync.py` SUBTREES) — three new dirs are inside `skills/`, no tuple change, and Design 6 says so. `AGENTS.md:94` (specs live in the target project) — `/spec-brief` writes relative to `project_root` = cwd. `AGENTS.md:96` (`CLAUDE.md` gitignored; tracked pointers only) — every documentation edit lands in `AGENTS.md`, `README.md`, or `docs/`. `AGENTS.md:91–92` (reviewers read-only; shared severity scale) — untouched, and `filesystem: [read]` on the primitive matches the posture.
- **Anchors spot-checked.** `spec-cycle:133` (step 5 origin sync), `:237` (step 8 scale), `:371–375` (synthetic missing-STATUS P0), `AGENTS.md:23–29/:95`, `README.md:7–11/:30/:54–59`, `spec-workflow-reference.md:3/:7/:162` all correct on disk.
- **Skill 0 / Skill 3 numbering** in `docs/spec-workflow-reference.md` — still odd on its face, still the right trade against renumbering live anchors. Dispositioned in round 2; not re-raised.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 2 | P4: 1

STATUS: GREEN
