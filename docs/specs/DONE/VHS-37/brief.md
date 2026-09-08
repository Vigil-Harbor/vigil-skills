# VHS-37 — spec-cycle: escape hatch for valid, non-trivial findings (fold-vs-defer routing)
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-09-08 · **Plane:** VHS-37 (a2781741-e5f4-4761-9ec5-f7cb44782d56, Backlog)
**Origin:** Filed 2026-09-06 out of the VHS-33 attempt-1 post-mortem, where four review rounds went 12 → 3 → 5 → 6 and three of the last four P0s were self-inflicted propagation misses. Reaffirmed by the operator on 2026-09-08 with a second specimen from this repo: VHS-41 attempt 1, gate 13 → 5 → 11 → 5, oscillating, where rounds 3–4 kept surfacing shell and jq mechanics introduced by the previous round's own fix. The memory record "defer out-of-scope spec-cycle findings" carries the operator's rule informally; this ticket makes it mechanical.

## Problem

`/spec-cycle` has no fix routing. §2e tells the author to "address every P0 and P1 finding", and the only alternative path, `## Deferred (P2+)`, is by its own name P2-and-below. So every P0/P1 gets folded into the spec. A fold that adds a rule to one Design section must then propagate to the authoritative contract block **and** to the checklist row that gates it; miss either and the next round files a P0 against the fix. The operator (2026-09-08): "the agent will fix a round 2 finding, and that patch becomes a fixation for following review rounds. The pattern is consistent. What should happen is fix routing. Non-trivial patches get their own ticket later and marked known/deferred in the spec so the later fix can hook in cleanly. Trivial patches proceed into the next review rounds." He also requires that the skill never file the ticket itself — it reports proposed follow-ups at the end, alongside the spec.

## Why it matters

`/spec-cycle` has been run over 200 times and is the operator's main point of leverage in the lifecycle, so the failure mode compounds. On VHS-33 the spec reached 1,178 lines for a prose-only change to five files that the brief scoped as four items, and its own "spec-level additions" roll-up listed about twenty constructs the brief never authorized. Deferral happened three times across that run, and only where a hard rule forbade folding — never on cost/benefit grounds, because nothing in the skill offers that route. The budget spent re-patching a previous round's patch is budget not spent on the design, and a spec that oscillates rather than converges burns all four rounds and halts red.

## Scope (verified against current files, 2026-09-08)

| Path | Current | Change |
|---|---|---|
| `skills/spec-cycle/SKILL.md` §2e (`:426-434`) | "Address every P0 and P1 finding." Only P2s may be "fix or list in `## Deferred (P2+)`". No disposition vocabulary exists, so folding is the path of least resistance. | Gains the fold / defer-to-ticket / reject routing: the propagation-site test (Decision 3), the scope ceiling (Decision 2), and the re-fold recount (Decision 4). |
| `skills/spec-cycle/SKILL.md` 2d gate (`:411-424`) | `total_p0p1` is summed across the dispatched reviewers' `STATUS` lines, green at 0; computed from the reports, never from author dispositions. | **Unchanged, deliberately** (Decision 1). Deferral works by the reviewers not re-filing, so the sum falls on its own. |
| `skills/spec-cycle/SKILL.md` `## Deferred (P2+)` and its consumers — 2e (`:431`), 2d (`:424`), 2g (`:593-624`, esp. `:611`, `:618`, `:622-623`), 2f option 3, and the failure-mode note at `:371` | The section is P2-and-below by name, and 2g plus 2f option 3 read it by that name. | **Untouched, byte-identical** (Decision 5). The routed P0/P1 deferrals go in a new, separate section so this spec's own fix is not a multi-site propagation. |
| `skills/spec-cycle/SKILL.md` spec-output sections | No section carries a P0/P1 the author chose not to fix. | New `## Deferred — follow-up required` section in the authored spec. Each row: lens-qualified finding id · severity · round deferred · affected spec section and anchor · the reviewer's `Suggested fix` verbatim · the propagation sites named under Decision 3 · the author's in-scope/out-of-scope classification · `Follow-up: unfiled` (Decisions 5, 6). |
| `skills/spec-cycle/SKILL.md` Phase 3 drift-check (`:626-676`) and 2f halt menu (`:466-487`) | The only two end-of-run renders. Neither reports follow-ups; `/spec-cycle` prints no per-round summary at all. | Both gain the follow-up report, rendered from the new section so there is one source of truth (Decision 7). Console only. |
| `agents/spec-reviewer-correctness.md` (`:18`, `:43-51`), `agents/spec-reviewer-edge-cases.md` (`:18`), `agents/spec-reviewer-conventions.md` (`:20`) | Each receives `closure_manifest` — "author-stated disposition of each round-(N−1) P0/P1 finding … verify these claims against the spec" — and re-opens unsatisfied dispositions as P0. | `DEFERRED` becomes a legal disposition. A finding recorded as deferred in the required shape is checked for well-formedness and for a correct scope classification, instead of being re-filed (Decisions 1, 6). |
| `agents/spec-reviewer-*.md` output contract (`correctness:138-176`, `edge-cases:133-165`, `conventions:127-158`) | A finding carries Severity / Where / Claim / Why this is wrong / Suggested fix, plus optional `**Pre-ship recommended:** yes` on P2s. No scope tag. | **Unchanged** (Decision 6 fences it). |

## Decisions carried forward

1. **Reviewer-side deferral, not gate arithmetic.** `DEFERRED` becomes a legal `closure_manifest` disposition and the reviewer agents gain a rule for accepting a well-formed deferral instead of re-filing it. The gate formula is not touched. *Why:* findings are regenerated by the reviewers from the spec text each round, so only a reviewer rule can stop the re-file; subtracting from the count would need a per-finding ledger matched by title across rounds, and would hide live findings from the number the operator reads.
2. **Scope is a ceiling, not a required conjunct.** Out-of-scope + non-trivial is deferrable at any severity. In-scope + non-trivial is deferrable at **P1 and below**. An in-scope **P0** must be folded, or the brief scoped down via 2f option 3. *Why:* the ticket's original "valid + out-of-scope + non-trivial" test would have blocked every deferral in the VHS-41 specimen, whose findings were all in-scope mechanics; but P0 means "internally inconsistent or unimplementable", which is the one thing a spec cannot ship as a known issue.
3. **Non-trivial = more than one propagation site.** Before editing, the author names every site the fix must land on — the Design section, the authoritative contract block, the checklist row, the Decisions list. More than one site named → non-trivial → defer. Zero or one → fold. *Why:* it is mechanical, checkable by the next round's reviewer after the fact, and naming the sites is itself the propagation discipline whose absence caused three of VHS-33's last four P0s.
4. **A re-fold finding forces a recount.** A new P0/P1 whose `Where` lands on a section a prior round's fold touched makes the author redo Decision 3's site count on the *original* fix, with the new finding as evidence. True count now above one → revert the fold and defer both findings. Still one → patch once more and record that the recount ran. *Why:* the under-count is not discovered at fold time, it is discovered when the reviewer catches it; that moment is the second flag, and without a rule the author simply patches again.
5. **A second section, not a rename.** `## Deferred (P2+)` keeps its name and its meaning; routed P0/P1 deferrals go in a new `## Deferred — follow-up required` with the row shape in the Scope table. *Why:* 2g and 2f option 3 read the old section by name, so renaming it would make this very spec a multi-site propagation — the thing Decision 3 defers. It also gives the reviewer's well-formedness check one unambiguous section to look in.
6. **The author classifies scope; the reviewer verifies it.** The in-scope/out-of-scope call is made against the brief's Scope table and Out-of-scope list, recorded in the deferral row, and checked by the well-formedness rule from Decision 1. Reviewers emit no scope tag. *Why:* the verification path Decision 1 already opens is enough; adding an `In-fence` line to the output contract would tax every finding to serve the few that get deferred, and invites reviewers to file scope opinions as findings.
7. **The follow-up report is console output at both exits.** Appended to Phase 3's drift-check block on the green path and to the 2f halt menu on the red path, rendered from the new section. *Why:* deferrals pile up fastest on the red path, which is where the list is most needed; a written artifact has no consumer today, since neither `/spec-close` nor `/ship-spec` reads `## Deferred`.
8. **No numeric cap on deferrals.** The Decision 2 ceiling plus the well-formedness check is the whole defense. *Why:* the ceiling already blocks the only deferral that can make a spec unshippable, and an arbitrary N punishes a spec legitimately carrying many small out-of-scope findings.
9. **The gate-inversion tripwire ships separately.** Halting early when `total_p0p1` rises between rounds is a good signal and a separate ticket; the "a round that defers more than it folds renders the scope-down option early" variant belongs with it. *Why:* the lesson of this ticket is that a small spec converges and a large one oscillates. Deferring the tripwire is the ticket taking its own medicine, and VHS-27 already owns that region of the file.

## Done when

- `/spec-cycle` 2e names the fold / defer-to-ticket / reject dispositions and the test that forces defer-to-ticket.
- Deferred entries that become tickets carry the ticket id.
- `lint.py --strict` reports zero ERROR; `sync.py status` clean; `sync.py push` round-trips byte-for-byte.

## Out of scope

1. The gate-inversion tripwire, and its "defers more than it folds" variant — a separate ticket (Decision 9).
2. Any change to the reviewer output contract, including an `In-fence: yes|no` tag on findings (Decision 6).
3. A `docs/specs/TODO/<TICKET-ID>.follow-ups.md` artifact, and any `/ship-spec` or `/spec-close` consumption of the deferral sections (Decision 7).
4. Renaming or re-scoping `## Deferred (P2+)`, or changing 2g and 2f option 3 (Decision 5).
5. Any numeric cap on how much one spec may defer (Decision 8).
6. `/spec-cycle` filing, transitioning, or commenting on a ticket. The skill reports proposed follow-ups; the operator files them.
7. Any change to the 2d gate formula (Decision 1).

## Risks / decisions

1. Backfilling a filed ticket id into a `Follow-up: unfiled` row — the Done-when requires that deferred entries which become tickets carry the ticket id, but the skill never files, so whether that is an operator hand-edit or a re-read on the next `/spec-cycle` run is unpinned; spec author pins this.

## References

- `skills/spec-cycle/SKILL.md:426-434` — §2e, "Address every P0 and P1 finding"; P2-only deferral.
- `skills/spec-cycle/SKILL.md:411-424` — 2d, `total_p0p1` summed across reviewer `STATUS` lines, green at 0.
- `skills/spec-cycle/SKILL.md:593-624` — 2g post-green polish; the existing bounded fold-vs-record decision for P2s, with hard limits, recording overflow in `## Deferred (P2+)`.
- `skills/spec-cycle/SKILL.md:466-487` — 2f halt menu (red path); `:626-676` — Phase 3 drift-check block (green path). The only two end-of-run renders; no per-round summary exists.
- `agents/spec-reviewer-correctness.md:18,43-51` — `closure_manifest` input and the rule that re-opens unsatisfied dispositions as P0. Same input at `agents/spec-reviewer-edge-cases.md:18` and `agents/spec-reviewer-conventions.md:20`.
- `agents/spec-reviewer-correctness.md:138-176` — finding output contract (no scope tag); `agents/spec-reviewer-edge-cases.md:133-165`, `agents/spec-reviewer-conventions.md:127-158`.
- `grep -rn Deferred skills/spec-close/SKILL.md skills/ship-spec/SKILL.md` → 0 hits, 2026-09-08. Neither downstream skill reads the section.
- Plane VHS-27 — "spec-cycle: switch to delta-scoped review passes after round 4 or after first GREEN"; open, same 2f region. Whichever ships second rebases.
- Specimens: `docs/specs/DONE/VHS-33/attempt-1/` (gate 12 → 3 → 5 → 6) and `docs/specs/TODO/VHS-41.attempt-1/` (gate 13 → 5 → 11 → 5).
- Interview: 2 rounds, exit empty-frontier
