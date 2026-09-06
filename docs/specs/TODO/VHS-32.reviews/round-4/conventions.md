# Conventions Review — round 4

Grounding complete. Read fresh from disk: the v4 spec (562 lines), `VHS-32.brief.md`, `AGENTS.md` (the canonical project instructions; the gitignored `CLAUDE.md` points to it), the global `~/.claude/CLAUDE.md`, all three round-3 reports, and `vigil-harbor-wiki/decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md` end to end. Re-verified live: `AGENTS.md:23` ("Three skills form the spec lifecycle"), `:59` (§ Superseded vendor skills), `:68` ("Two warnings:"), `:88–96` (Conventions, `## Scale` grammar at `:95`); `skills/spec-cycle/SKILL.md` 2f halt block (exactly three options today); `README.md:3, :7–11, :30, :54–59`; `docs/spec-workflow-reference.md:3, :162`; `lint.py:45–49` (`SERVICES_VOCAB` at `:49`), `:57`, `:214–218`; `sync.py:96` (the `copy2` in `cmd_install`); `skills/bloat-check/SKILL.md:19`; `ls skills/` (no `grilling`/`grill-me`/`spec-brief` — no in-repo name conflict). `scale_lens: off` and `round-3/` contains no `scalability.md`, so the stale-report guard is a no-op. `round-4/` exists but is empty.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Post-cap revision round promised but never granted; `revised-after-cap` unreachable | CLOSED | spec:157 (§ 1.1 resume contract verbatim, incl. "runs exactly one additional round and exits `revised-after-cap (+1 round)`; a further `prior_summary` … exits `round-cap` at once"); :181 (§ 1.4 references it); :185 (§ 1.6 lists it among the bounds); :205 (`(round_cap + 1) × question_cap`); :117 / :313 ("the same `round_cap` / `question_cap` — the primitive itself grants"); checklist 4 :458; Run D :474 |
| correctness | F-2 (P2) | 2c scalability stub missing from "not grillable" | CLOSED | spec:399 ("any 2c dispatch-failure stub … `skills/spec-cycle/SKILL.md:404–409`") |
| correctness | F-3 (P2) | No derivation rule for `## Out of scope` | CLOSED | spec:338 (fence-shaped Settled → `## Out of scope`; Problem / Why it matters / Done when transcribed, never inferred) |
| correctness | F-4 (P2) | "Answer by number" vs letter selectors | CLOSED | spec:175 ("Answer by question number and branch letter (e.g. `Q3 B`)") |
| correctness | F-5 (P3) | `question_cap` declared ignored under `--no-grill` yet bounds Phase 1 | CLOSED | spec:256 ("ignored for the interview; the default question cap (7) still bounds Phase 1's grounding batch") |
| correctness | F-6 (P3) | D8 seed drifted from Design 4 step 1 | CLOSED | spec:69 ("minus the not-grillable exclusions in Design 4 step 1") |
| correctness | F-7 (P3) | Runs A and B share `ZZZ-1` | PARTIAL | spec:469 splits A/B to `ZZZ-1` / `ZZZ-2` with the rationale inline — but Run C (:473) still asserts against `ZZZ-1`; see F-3 below |
| correctness | F-8 (P3) | Local-only header fields unsourced | CLOSED | spec:338 (`**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`) |
| correctness | F-9 (P3) | `sync.py:146` cited for the install path | CLOSED | spec:447 and References :541 both now read "`sync.py:96`, the install copy; `:146` is the symmetric push copy" |
| correctness | F-10 (P4) | Residual label/bound/anchor nits | CLOSED | checklist 9 :463 ("four-case `## Scale` rule"); § 1.8 :205; References `lint.py:45–49` (verified: `SERVICES_VOCAB` is at `:49`) |
| edge-cases | F-1 (P2) | Primitive-side resume contract absent | CLOSED | Same evidence as correctness F-1; the four sub-gaps (Open items, Facts carry-over, Q numbering, `rounds_used`) are all in the :157 bullet |
| edge-cases | F-2 (P2) | Unappliable Settled item; brief not in the invariant list | CLOSED | spec:406 ("`deferred to option 3: <finding id>` … Settled-but-unapplied"); :409 invariants gain "never edits the brief"; checklist 7 :461 greps both |
| edge-cases | F-3 (P2) | Stale-`.tmp` trigger never fires; dot prefix ≠ gitignored here | CLOSED | spec:262 (tmp added to the trigger; remove-and-continue path); :336 (the `.gitignore` caveat stated — "the no-commit rule below is prose, not mechanism"). *(The removal itself raises a new P2 — F-2 below.)* |
| edge-cases | F-4 (P2) | S8's "durable backstop" needs a timestamp that does not exist | CLOSED | spec:123 ("held in context only … no on-disk signal … does not withhold option 4"); Risk 14 :526 |
| edge-cases | F-5 (P3) | Concurrent `grill.md` append loses a block; shared fixed temp name | CLOSED | spec:123 (last-writer-wins stated honestly); :405 (unique `.grill.md.<random>.tmp`); Risk 14 |
| edge-cases | F-6 (P3) | `--no-grill` grounding fan-out bound | CLOSED | spec:256 |
| edge-cases | F-7 (P3) | New paths uncovered by checklist/transcripts | CLOSED | checklist 13 :467; Run D :474 |
| conventions | F-1 (P2) | VHS-28 posture inverted; revisit trigger never engaged | CLOSED | spec:447 (second-supersession paragraph disposing the trigger, quoting the decision's own "installs and overwrites; it does not delete" consequence — verified verbatim in the decision file); D10 :77 narrowed to "the *supersession* mechanism differs"; References :543 cites the decision file |
| conventions | F-2 (P2) | `AGENTS.md` § Superseded edit had no slot; "Two warnings:" list at risk | PARTIAL | Design 5 :425 pins it as a paragraph, "not a bullet", appended after the closing "If AgentCraft reinstalls its copy…" paragraph, with the list "byte-identical"; checklist 12 :466 asserts exactly two bullets. But the Scope table :21 still directs the implementer to "One bullet in § Superseded vendor skills" — see F-1 below |
| conventions | F-3 (P3) | README tagline and Requirements left pre-VHS-32 | CLOSED | Scope row :23 now names `README.md` tagline (`:3`); Design 5 :439 rewrites it and extends the Requirements bullet with `/spec-close` |
| conventions | F-4 (P3) | v3 emission rules outside the `:31` ledger | CLOSED | spec:31 closes the class ("…and the Phase 4 emission rules these imply (the empty-Settled sentinel, the origin-annotated Scope heading, the Out-of-scope routing, the local-only header fields)") |
| conventions | F-5 (P4) | `grilling` lacked a `## Failure modes` section | CLOSED | spec:211 (§ 1.11, four lines pointing at 1.5/1.7/S9); checklist 4 :458 asserts both are real `##` headings |

The round-3 P1 (correctness F-1) is genuinely CLOSED — the mechanism now lives in the primitive's own § 1.1, is echoed in § 1.6, is asserted by checklist 4, and has a Run D exercise. No REOPENED items. Two PARTIALs, both P2, both one-line residues of otherwise-complete fixes.

## Findings

### F-1: The Scope table still tells the implementer to add "one bullet" to `AGENTS.md` § Superseded vendor skills — the exact instruction Design 5 was rewritten to forbid

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:21 (Scope table, `AGENTS.md` row) vs spec.md:425 (Design 5)
**Convention violated:** the structure of `AGENTS.md` § Superseded vendor skills (`AGENTS.md:59–80`), which `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md` § Related calls "the executable record"
**Evidence:** Design 5 now says, correctly and with its own justification:

> `AGENTS.md` § Superseded vendor skills gains one short **paragraph (not a bullet** — the section's only list is the counted "Two warnings:" about the AgentCraft removal, and it stays byte-identical), appended after the closing "If AgentCraft reinstalls its copy…" paragraph

The Scope table one page earlier still reads:

> One **bullet** in § Superseded vendor skills on the upstream name collision. § Design 5.

`AGENTS.md:68` is verified: `Two warnings:` introduces exactly two bullets, and they are scoped to the AgentCraft *removal* — a warning against deleting third-party skills, the opposite topic from `grilling`'s deliberate overwrite. The Scope table is the row an implementer works from when planning the diff; it points at Design 5, but it also states a contradictory shape in the same sentence. Checklist 12 (`:466`) would catch the resulting three-bullet list — but only after the edit is written, which is one avoidable rework cycle on the section this repo's own decision page designates as executable.

**Suggested fix:** one-word edit at `:21` — "One **short paragraph** in § Superseded vendor skills on the upstream name collision (not a bullet — see § Design 5)."

---

### F-2: "The skill's lone filesystem mutation" is asserted twice, but Phase 0 step 2 now silently deletes a file before any confirm — and checklist 9 was not updated to cover the new trigger

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:262 (Phase 0 step 2), :336 (Phase 4), :359 ("What `/spec-brief` never does"), :363 (§ Tool-use notes), :463 (checklist 9)
**Convention violated:** this repo's review posture on by-construction claims (`AGENTS.md` § "Plan & Spec Reviews": verify load-bearing claims against actual state) and the `## Tool-use notes` completeness convention that contract §4 case 3 makes the exemption home for
**Evidence:** the v4 fix for edge-cases R3 F-3 gave Phase 0 step 2 a new mutating branch (`:262`):

> If only the stale temp exists, **remove it**, log `stale temp removed: …`, and continue without halting.

and `:336` confirms it fires "whether or not any other artifact exists". That is an unlink, performed at preflight, before the Phase 3 confirm, on a path the current run did not create. Two sentences still count it out:

- `:336` — "This rename is the skill's **lone** filesystem mutation outside the brief itself."
- `:363` — "…plus the single rename of the brief's dot-prefixed temp onto its target, **the skill's lone filesystem mutation** outside the brief."

`:363` is the contract line the implementer copies into the shipped `## Tool-use notes` heading, so the shipped skill would tell an operator it performs exactly one mutation while performing a delete at step 2. `:359`'s never-list ("write anything other than the one brief file (and its transient `.tmp`)") does not name deletion either. Related residue: checklist 9 (`:463`) — the ship gate — still reads "Phase 0 step 2 checks brief, spec, and reviews", enumerating three of the four things step 2 now checks, so the new `.tmp` trigger has no gate assertion.

This is not a behavior bug — the removal is right, and `requires: filesystem: [read, write]` already covers it. It is an accuracy gap in the two sentences that state the skill's mutation surface, in a spec whose whole D1/D2/D9 argument is that stated guarantees must match mechanism (cf. the Honesty note at `:37` and Risk 10, which apply exactly this discipline to `Explore`).

**Suggested fix:** at `:336` and `:363`, replace "lone filesystem mutation outside the brief" with "…the only filesystem mutations are this rename and Phase 0 step 2's removal of a stale `.<TICKET-ID>.brief.md.tmp`"; add "delete any file other than a stale `.<TICKET-ID>.brief.md.tmp` of its own shape" to `:359`'s never-list; and extend checklist 9 to "…Phase 0 step 2 checks brief, spec, reviews, **and the stale `.tmp`, removing the latter without halting when it is alone**."

---

### F-3: Run C reuses `ZZZ-1` — the collision correctness R3 F-7 was fixed for Runs A/B reappears one bullet later

**Severity:** P3
**Where:** spec.md:469 (Test plan procedure), :471 (Run A), :473 (Run C)
**Convention violated:** internal consistency of the Test plan, which the spec designates "the gate for `/ship-spec`" (`:454`)
**Evidence:** the v4 procedure states the hazard explicitly and fixes it for two of four runs:

> Run A uses `ZZZ-1` and Run B uses `ZZZ-2` (**a shared id would trip Run B into the artifacts-exist halt and ground it on Run A's brief**), both in conversation-only mode; the emitted briefs are deleted **before commit**

Run A writes `docs/specs/TODO/ZZZ-1.brief.md`; deletion is specified relative to commit, not between runs. Run C then reuses that id and asserts the negative:

> **Run C — empty seed** … the skill re-prompts once, then halts with the S9 message; `docs/specs/TODO/ZZZ-1.brief.md` does not exist afterward.

Under the implied A→B→C→D ordering (Run D at `:474` explicitly depends on Run B's state), Run C hits Phase 0 step 2's artifacts-exist halt before ever reaching the S9 seed gate, and its one assertion is unsatisfiable because Run A's file is still there. The run exists to prove `empty-seed` writes nothing; as written it proves nothing.

**Suggested fix:** give Run C its own id (`ZZZ-3`) at `:473`, or add to the procedure at `:469`: "each run uses a distinct id (`ZZZ-1`/`ZZZ-2`/`ZZZ-3`; Run D continues Run B's `ZZZ-2` session)."

---

### F-4: Design 5 labels `/grill-me` "(existing)" in the README § Skills list — it is one of the three skills this spec creates

**Severity:** P4
**Where:** spec.md:439 (Design 5, `README.md`) vs spec.md:17, :23
**Convention violated:** internal consistency with the Scope table, which lists `README.md` gaining "Bullets for `/spec-brief`, `/grill-me`, and the missing `/spec-close`"
**Evidence:** `:439` reads "…then `/grill-me <topic>` and `/review-pr` (existing)". Verified against `README.md:7–11`: § Skills today lists exactly `/spec-cycle`, `/ship-spec`, `/review-pr`. `/review-pr` is existing; `/grill-me` is created by `:17` of this spec. The trailing parenthetical reads as covering both entries, which would tell an implementer to leave `/grill-me`'s bullet unwritten. Checklist 8 (`:462`) greps only for `/spec-brief` and `/spec-close`, so a missing `/grill-me` bullet passes the gate.

**Suggested fix:** move the parenthetical — "…then `/grill-me <topic>` (new) and `/review-pr` (existing)".

---

## Notes on the axes that came back clean

- **Contradicts a prior decision.** Re-checked against `2026-08-25-vhs-28-supersession-is-an-operator-step.md` in full: its revisit trigger ("A **second** vendor skill needs superseding … Reconsider option 2 then") is now cited and dispositioned at `:447`, and the dismissal quotes the decision's own § Consequences accurately ("`sync.py` stays non-destructive. It installs and overwrites; it does not delete" — verbatim in the file). D10's "same clean-room posture … the *supersession* mechanism differs" is now a true statement of both halves. `2026-06-16-vhs-15` (halt-block scalability line closes a residual hardcode, not adds one), `2026-06-14-vhs-17` / `-18` (all three `requires:` blocks flat, controlled-vocabulary, after the scalars; `services: [issue-tracker?, shared-memory?]` valid against `lint.py:49`), `2026-06-18-vhs-20` (D9 rests on the guard sentence, not the dropped flag), `2026-08-25-vhs-29` (the `grill.md` append is an audit trail, not the newest-first `log.md` contract) — all clean. No live conflict remains.
- **Premature abstraction.** Unchanged: `grilling` has three real callsites, at the N≥3 bar; the spec still declines a general Nth-lens registry.
- **Reuse vs duplicate.** `/spec-brief` Phase 0 keeps borrowing the live precedent rather than inventing (`spec-close:31` `<config-dir>` resolution, `:37–42` warn-only origin, `prepend_log_entry.py:370–375` atomic-write shape), and the deliberate second implementation is still justified by `prepend_log_entry.py:365–368`.
- **Unneeded backwards-compat.** None. No shims, no `_unused`, no re-exports; `--no-grill` is a D9 requirement, not a compat flag.
- **Silent spec additions vs the brief.** The `:31` ledger now closes the class rather than enumerating it, and every v4 addition traces to a named round-3 finding with its rationale at the point of use — all (c), none (d). The one v4 addition whose ledger entry is arguably strained (Phase 0 step 2's stale-tmp *removal*, filed under "the artifacts-exist halt") is raised above as F-2 on accuracy grounds, not scope grounds.
- **Repo conventions re-checked live.** `AGENTS.md:93` (`sync.py` `SUBTREES`) — three new dirs are inside `skills/`, no tuple change, Design 6 says so. `:94` (specs live in the target project) — `/spec-brief` writes relative to `project_root` = cwd. `:95` (`## Scale` grammar) — Phase 4's four-case rule matches it exactly. `:96` (`CLAUDE.md` gitignored; tracked pointers only) — every documentation edit lands in `AGENTS.md`, `README.md`, or `docs/`, and Phase 0 step 1 names `AGENTS.md` as this repo's project-instructions file. `:90–92` (reviewers read-only; shared severity scale) — untouched, and `filesystem: [read]` on the primitive matches the posture.
- **Naming.** `ls skills/` confirms no in-repo collision for `grilling`, `grill-me`, or `spec-brief`; the only collision is the intended upstream one, now documented in three places.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 1 | P4: 1

STATUS: GREEN
