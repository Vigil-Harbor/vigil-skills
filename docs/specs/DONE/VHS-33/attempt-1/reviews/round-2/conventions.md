# Conventions Review — round 2

Grounding: the spec and brief read fresh, `AGENTS.md` (the canonical project instructions `CLAUDE.md` points to), the wiki's `projects/vigil-skills/` pages and both overlapping decisions, the round-1 reports for all three lenses, and every anchor the spec cites verified against the live files (`skills/grilling/SKILL.md`, `skills/spec-cycle/SKILL.md`, `skills/spec-brief/SKILL.md`, `skills/grill-me/SKILL.md`, `docs/spec-workflow-reference.md`, `docs/specs/DONE/VHS-32/spec.md:458`), plus `python lint.py --strict` for checklist row 1.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 (P0) | rows 2/10 mutually unsatisfiable | CLOSED | spec `:522–524` scopes `spec-cycle` to `git diff -U0` added lines; § Scope `:46–48` names § 2b |
| conventions | F-2 (P1) | `## Test command` carries prose | CLOSED | `:602–604` body is exactly `N/A`; framing moved to Test-plan preamble `:511–513` |
| conventions | F-3 (P2) | Out-of-scope framing | CLOSED | `:629` / `:644–657` split; item 9 states the fence-vs-decision-4 tension |
| conventions | F-4 (P2) | no roll-up of spec-level additions | **PARTIAL** | preamble `:56–72` enumerates eight, but Design 1's all-or-none and legal-id rules are absent — see new F-1 |
| conventions | F-5 (P3) | absent-`ref:` justified by a nonexistent compat concern | CLOSED | `:201–204` now legibility, states nothing mechanical parses the block |
| conventions | F-6 (P3) | no `## Risks` / `## References` | CLOSED | `:659`, `:681`; shape matches `DONE/VHS-32/spec.md` (`:515`, `:533`, `:553`) |
| conventions | F-7 (P3) | wiki revisit trigger unrecorded | CLOSED | D9 `:135–137`, fence item 11 `:656`, References `:700–701` |
| conventions | F-8 (P3) | conditional fifth clause | CLOSED | `:403–406` — every clause renders, `none` / `0` |
| conventions | F-9 (P4) | three spellings of "empty" | **PARTIAL** | `:249–251` fixes the section/field split, but Design 7 `:460–462` adds a *fourth* literal against `spec-brief/SKILL.md:139` — see new F-2 |
| correctness | F-1 (P0) | `empty-frontier` two ways | CLOSED | Design 4 `:325–329` |
| correctness | F-2 (P1) | row 2 unpassable / row 10 forbids fix | CLOSED | as conventions F-1 |
| correctness | F-3 (P1) | "exactly two" reason values vs a third | CLOSED | `:232–234` — optional qualifier on the first value, never a third |
| correctness | F-4 (P1) | no `ref:` slot on F-item / deferred item | CLOSED | block `:223–224`; placement rule `:206–208` |
| correctness | F-5 (P2) | seeded-but-never-rendered finding unreported | CLOSED | `not reached` `:414–419` |
| correctness | F-6 (P2) | "supersedes" mischaracterizes VHS-32 row 4 | CLOSED | D9 `:128–133` reads "extends"; new checklist row 5 `:537–542`. Verified: every assertion in `DONE/VHS-32/spec.md:458` survives v2, so "extends" is the correct framing |
| correctness | F-7 (P2) | empty-Settled rule over-broad | CLOSED | Design 7 `:460–466` (but see new F-2) |
| correctness | F-8 (P3) | round-end line pinned while its meaning changed | CLOSED | `:311–314` records the choice |
| correctness | F-9 (P3) | `:88` / `:74` old vocabulary | CLOSED | Design 2 Cross-references `:253–258` + Scope row `:28` |
| correctness | F-10 (P4) | `:23` mislabeled | CLOSED | Scope `:32`; Design 8 `:492` |
| correctness | F-11 (P4) | surface one commit old | CLOSED | Risks 4 `:677–679`; Deferred `:710–711` |
| edge-cases | F-1 (P0) | F-item reason set / third value | CLOSED | `:232–234` |
| edge-cases | F-2 (P0) | deferred item has no field for `ref:` | CLOSED | `:224` |
| edge-cases | F-3 (P1) | `fence-empty` on resume erases carried items | CLOSED | `:330–338` fresh-invocation-only |
| edge-cases | F-4 (P1) | verification has no round on the last round | CLOSED | `:300–305` |
| edge-cases | F-5 (P1) | refuted vs never-checked identical | CLOSED | `:271–275` |
| edge-cases | F-6 (P1) | no missing-`ref:` tripwire, no reconciliation | CLOSED | `:418–419` completeness; `:430–433` `item missing ref:` |
| edge-cases | F-7 (P2) | partially-supplied id seed | CLOSED | `:181–184` all-or-none |
| edge-cases | F-8 (P2) | id lexical form undefined | CLOSED | `:178–180` |
| edge-cases | F-9 (P2) | `_(none)_` only for fence-empty | CLOSED | `:245–248` on every exit |
| edge-cases | F-10 (P2) | step-5 line undefined when empty | CLOSED | `:403–406`; fence-empty line `:435–440` |
| edge-cases | F-11 (P2) | `:76` displaced wholesale | CLOSED | `:289–295` narrows to the retry only |
| edge-cases | F-12 (P2) | partially confirmed has no disposition | CLOSED | `:280–284` |
| edge-cases | F-13 (P2) | reason overlap, no precedence | CLOSED | `:236–243` |
| edge-cases | F-14 (P3) | `fact not established` can't distinguish four causes | **REOPENED (as a false closure claim)** | Not folded anywhere. § Deferred `:712–713` nonetheless asserts it was. See new F-3 |
| edge-cases | F-15 (P3) | not-grillable in the chain and in the unknown-id rule | CLOSED | `:423–425` (excluded from the chain), `:427–429` (unknown-id evaluated first) |

All round-1 P0/P1 items are CLOSED. The two PARTIALs and the REOPENED item are P2/P3/P4 in origin and are re-filed below at their own severity.

## Findings

### F-1: The spec-level-additions roll-up omits Design 1's two caller-facing constraints
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:56–72` (the `## Decisions` preamble) vs § Design 1 `:178–184`
**Convention violated:** The roll-up's own stated purpose — "listed here so the Phase 3 drift-check sees them" (`:57`) — plus the silent-additions axis: a spec-level addition must be visible to the drift-check, and `skills/spec-cycle/SKILL.md:598–620` renders the drift-check from the *brief's* decision list, so the roll-up is the only place these surface.
**Evidence:** The brief's decision 1 (`VHS-33.brief.md:36`) authorizes only "an optional caller-supplied `id` per seed item is echoed verbatim … absent when the caller passed none." Design 1 adds two constraints the brief does not carry, and neither appears in the eight-item roll-up:
- **Legal id** (`:178–180`) — "A non-empty string with no comma, no newline, and no leading or trailing whitespace, unique within the seed."
- **All or none** (`:181–184`) — "A caller that supplies any `id` supplies one for every seed item. A partially identified seed is **not a legal invocation**."

The all-or-none rule in particular makes a class of invocation illegal that the brief left legal; it is the most caller-visible addition in the spec, and it is the one item a drift-check reading the roll-up would not see. Two smaller Design additions are also unlisted: Design 3's third verification rule (`:300–305`, "a claim answered in the last rendered round is not verified" — the roll-up says "the two departures", and this is a third, non-departure rule) and Design 5's `≈3-sentence` question-body bound (`:363–364`, where the brief says only "keeps question bodies short").
**Suggested fix:** Add to the `:56–72` list: "The legal-id lexical rule and the all-or-none rule for partially identified seeds (Design 1)" and "The last-rendered-round verification rule (Design 3)"; change roll-up item 4's "the two departures" to "the three rules on when verification runs". Optionally add the ≈3-sentence bound as a fifth-order item.

### F-2: Design 7 writes a third sentinel into a brief cell `spec-brief/SKILL.md:139` already owns, without saying it supersedes it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 `:460–462`; checklist row 12 `:583–588`
**Convention violated:** D12's own "one meaning per term" (`:151–155`), and the repo's single-source-of-truth pattern — `_(none settled — see Risks / decisions)_` is an existing, deliberately-chosen artifact convention (VHS-32 edge-cases R2 F-13, folded at `DONE/VHS-32/spec.md:338`).
**Evidence:** `skills/spec-brief/SKILL.md:139` reads, in full: *"If Settled is empty, write `_(none settled — see Risks / decisions)_` under the header rather than leaving it blank, and print `warning: interview settled no decisions — the brief pins everything to the spec author`."* On a `fence-empty` exit Settled **is** empty, so `:139` fires. Design 7 then says the brief "carries `_(none)_` under `## Decisions carried forward` … and a distinct warning … rather than `:139`'s 'the brief pins everything to the spec author'." The spec states explicitly that it replaces the **warning**; it says nothing about replacing the **sentinel**, so an implementer has two literals for the same cell and the spec does not say which wins. The repo now holds four spellings of the same idea (`_(none)_`, `_(none settled — see Risks / decisions)_`, `ref: none`, `Facts relied on: none`), and `:249–251` distinguishes only two of them.

Note the substantive point: `:139`'s sentinel is *wrong* on this path regardless — it points the reader at `## Risks / decisions`, which Design 7 also renders empty. So the override is right; it is only unstated.
**Suggested fix:** One sentence in Design 7: "On the `fence-empty` path the Settled sentinel is `_(none)_`, not `:139`'s `_(none settled — see Risks / decisions)_` — that pointer would send the reader to a section this path also leaves empty. `:139` is unchanged for every other exit." Add the sentinel to checklist row 12's assertion list alongside the warning text.

### F-3: § Deferred (P2+) asserts every other round-1 P2/P3/P4 was folded; edge-cases F-14 was not
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Deferred (P2+) `:712–713`
**Convention violated:** `skills/spec-cycle/SKILL.md:431` — *"For P2 findings, either fix or list them in a `## Deferred (P2+)` section at the end of the spec with one-line acknowledgments."* Also the forward-closure principle in `vigil-harbor-wiki/decisions/2026-08-09-review-round-artifacts-are-immutable.md`: closure is recorded forward and must be true when recorded.
**Evidence:** The spec claims "No other round-1 P2/P3/P4 finding is deferred: all were folded into the designs, the checklist, or the new `## Risks` / `## References` sections." Edge-cases R1 F-14 (P3) asked that `fact not established` carry an optional cause qualifier, because it currently covers four causes a debugger must tell apart: the operator ignored it twice (`skills/grilling/SKILL.md:88`), the dispatch cap never reached it (`:74`), the dispatch failed (`:76`), and this host has no read-restricted agent class (`:72`). The spec adds qualifiers only on the **operator-claim** path (`:223`). Grepping the spec for the other three causes returns nothing but D5 and two cross-references. Concretely, `:72`'s existing rendered marker — `*(no read-restricted agent available in this host)*` — still has no carrier into the hand-off, which is the specific loss F-14 named.
**Suggested fix:** Either fold it (extend `:223`'s qualifier slot to the non-operator causes, mirroring the operator forms) or replace the blanket sentence with a real Deferred entry: "**edge-cases R1 F-14** (P3) — an optional cause qualifier on `fact not established` for the non-operator causes (`:72` / `:74` / `:76` / `:88`). Not folded: the operator-claim qualifiers were the caller-visible half; distinguishing the other three is a legibility improvement with no caller today."

### F-4: The VHS-32 wiki decision's rejected alternative bears on `fence-empty` and is not acknowledged
**Severity:** P3
**Where:** spec § D6 `:105–109`, § Design 7 `:454–466`, § References `:700–701`
**Convention violated:** the "contradicts a prior decision" axis — a decision page whose subject overlaps must be aligned with or explicitly superseded, not brushed past.
**Evidence:** `vigil-harbor-wiki/decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` § Key Decision 5 records: *"**Rejected — a success token for an empty interview.** It would write a hollow brief that every downstream lens then treats as authority."* `fence-empty` is a success token for an interview that rendered zero items, and Design 7 has `/spec-brief` write a brief from it — `_(none)_` under Decisions and under Risks, no Scope rows. The spec cites this decision page only as a revisit trigger (`:135–137`, `:700–701`). Design 7 `:454–457` does argue the distinction in substance ("the seed had a root and nothing above the fence, which is a documented outcome with a summary attached"), which is why this is P3 and not higher — but the argument never names the rejected alternative it is narrowing, and `/spec-close`'s decomposition will have to reconstruct it.
**Suggested fix:** One sentence in D6 or Design 7: "The VHS-32 wiki decision rejected a success token for an *empty interview* on the grounds that it writes a hollow brief. `fence-empty` narrows that rejection rather than reversing it: the seed had a root, the ticket text is real, and the brief's distinct warning names the fence — what the rejection guards against is `empty-seed`, which stays a halt."

## Verified, not findings

- **D9's "extends, not supersedes" is correct.** `docs/specs/DONE/VHS-32/spec.md:458` read in full. Every assertion it makes — the `:12` guard sentence, "make no mutations of any kind", the fork block, the advisory sentence, the three bounds with defaults 3 / 7 and the shared fact-request cap, the S4 worked-examples table, the three section headers, `empty-seed`, the resume contract with `revised-after-cap (+1 round)` — survives v2 unchanged, and VHS-33 checklist row 5 re-asserts all of them. "Extends" is right; VHS-32 row 4 stays true. Calling it "the fence table" instead of "the S4 table" is also right — `S4` is an archived spec's internal section id, not an artifact anchor.
- **New section shape matches the VHS-32 precedent.** `## Risks` / `## References` / `## Deferred (P2+)` appear in the same order and at the same altitude as `DONE/VHS-32/spec.md:515` / `:533` / `:553`.
- **Anchor grounding is clean.** Every line reference in § References resolves: `grilling` `:12`, `:14`, `:23`, `:52–55`, `:72`, `:74`, `:76`, `:88`, `:106`, `:108`, `:119`, `:122`, `:125–126`, `:129`, `:136–138`, `:146–151`; `spec-cycle` `:489`, `:495`, `:499–505`, `:518–528`, `:539–546`, `:548–554`, `:646`, `:698–708`; `spec-brief` `:84–90`, `:92–107`, `:113–128`, `:134–143`, `:156–164`; `grill-me` `:14`, `:18–21`; `spec-workflow-reference.md` `:23`, `:33`, `:35`. The spec silently corrected three off-by-one ranges the brief carried.
- **Checklist grep counts verified live:** `options 1–3` = 4, `total_p0p1 == 0` = 2, and `python lint.py --strict` → exit 0, 0 errors, exactly 2 `missing-requires` WARNs (`review-pr`, `ship-spec`).
- **No premature abstraction, no backwards-compat drift.** `ref:` is a contract field on a primitive with three real callers, not a registry at N=1. The Q-item reason set narrows by *removal* (`fact not established` leaves the question form, `:236`) rather than by deprecation shim — clean deletion, per AGENTS.md.
- **`fence-empty` as a token name** departs from the `empty-seed` / `empty-frontier` shape, but the brief pins the name (decision 6) and the ticket carries it. Brief-authorized, not drift.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
