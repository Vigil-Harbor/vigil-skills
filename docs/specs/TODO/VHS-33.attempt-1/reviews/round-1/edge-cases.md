# Edge-Cases Review — round 1

Grounding: spec, brief, ticket (memory, tag_exact hit), CLAUDE.md/AGENTS.md pointers, and all five files the spec proposes to change (`skills/grilling/SKILL.md`, `skills/spec-cycle/SKILL.md` § 2f-i + failure modes, `skills/spec-brief/SKILL.md` Phases 2–4, `skills/grill-me/SKILL.md`, `docs/spec-workflow-reference.md:20–36`).

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: The F-item reason set is "exactly two values" and Design 3 adds a third
**Severity:** P0
**Where:** spec § Design 2 (`VHS-33.spec.md:171–179`) vs § Design 3 (`:200–204`), pinned by checklist row 4 (`:389–395`)
**Edge case:** An operator answers a fact request, the verification does not confirm it.
**What happens:** Design 2 states "The reason vocabulary is exactly two values" (`fact not established | stopped`) and checklist row 4 gates on "the two-value reason set". Design 3 mandates a third rendering, `unresolved because: fact not established (operator claim, unverified)`. An implementer who satisfies row 4 writes a two-value set that has no legal slot for the unverified-claim case; an implementer who satisfies Design 3 fails row 4 as written. A caller that pattern-matches the two literals silently drops every unverified-claim F-item, or misparses it.
**Why the spec misses it:** The two designs were written against different sources (`grilling/SKILL.md:74`/`:88`/`:108` for Design 2; the new claim path for Design 3) and never reconciled. Design 3 calls the string a "qualifier", but Design 2 says the vocabulary is closed and row 4 asserts it.
**Suggested fix:** Make the reason set explicitly `fact not established [(operator claim, unverified)] | stopped` — one value with an optional parenthetical qualifier — and restate row 4 as "the reason set `fact not established | stopped`, plus the `(operator claim, unverified)` qualifier on the first."

### F-2: The rolled-up deferred item has no field for `ref:` to attach to
**Severity:** P0
**Where:** spec § Design 1 (`:148–150`, `:162–163`), checklist row 4 (`:390`), Done when 1 (`:466–468`)
**Edge case:** A `defer` answer that rolls up a subtree — the item with no `Q` number, which D1 names as the exact case title-matching cannot map.
**What happens:** The placement rule is "`ref:` is the last field on the item line, after `Facts relied on:` on a Settled item and after `unresolved because:` on an Open one." The rolled-up item's current form (`skills/grilling/SKILL.md:126`) is `2. **<parent title> — downstream decisions not explored (deferred at round <n>)**` — it carries *neither* field, so the placement rule does not resolve, and the spec never renders a v2 block showing it. Worse, checklist row 4 gates on "`ref:` field on the Settled item line and on the Open question line" only, so the gate passes while Done-when 1 ("every Settled and Open item **including the rolled-up deferred item**") is unmet. 2f-i then sees an item with no `ref:` for the one item type whose finding ids cannot be recovered any other way.
**Why the spec misses it:** Design 1 asserts inheritance for the rolled-up item in prose but never states its rendered line; the checklist enumerates the two shapes that already have trailing fields.
**Suggested fix:** Pin the rolled-up item's v2 line verbatim, e.g. `2. **<parent title> — downstream decisions not explored (deferred at round <n>)** — unresolved because: deferred. ref: <ids>`, and add it to checklist row 4's list of verbatim assertions.

### F-3: `fence-empty` on a resume erases carried-over Settled items and facts
**Severity:** P1
**Where:** spec § Design 4 (`:230–243`), against `skills/grilling/SKILL.md:23` (resume contract) and `skills/spec-brief/SKILL.md:105`
**Edge case:** `/spec-brief` Phase 3 option 2 (or 2f-i's revise path) re-invokes with `prior_summary`, and the revised decision's subtree yields no candidate above the altitude fence.
**What happens:** Two collisions. (a) The header: Design 4 mandates `rounds: 0/<round_cap>`, but the resume contract requires `rounds_used` to carry over from the prior summary (≥1). The header cannot be both, and `/spec-brief:143`/`:159` interpolate the round count into the brief and the completion banner. (b) The sections: Design 4 mandates that "All three sections render with `_(none)_`", while the resume contract says "Settled items stay settled… Facts established carry over". Following Design 4 literally on a resume returns an empty summary; `/spec-brief` Phase 4 then applies `:139` and writes `_(none settled — see Risks / decisions)_` into the brief — every decision the operator settled before revising is destroyed, silently, in the artifact every downstream lens treats as authority.
**Why the spec misses it:** Design 4 defines fence-empty purely in terms of "round 1", and never asks what "round 1" means for an invocation that inherits a tree.
**Suggested fix:** State that `fence-empty` is reachable only on a fresh invocation (`prior_summary` absent). A resume that renders zero items exits `empty-frontier` (or `revised-after-cap (+1 round)` where the post-cap round was granted) with the carried-over Settled and Facts sections intact. Add it to checklist row 7.

### F-4: A verification dispatched "in the round after" has no round to run in on the last round
**Severity:** P1
**Where:** spec § Design 3, departure 2 (`:215–219`); interaction with `skills/grilling/SKILL.md:104–108`
**Edge case:** The operator answers `F1 <answer>` in the final round — round `round_cap`, the post-cap revision round, the round in which they type `stop`, or the round after which the frontier empties.
**What happens:** Undefined. Design 3 fixes verification to "the round *after* the operator's answer, inside that round's single parallel batch"; on the last round there is no next batch. Three unhandled sub-cases: (i) under defaults a fact request rendered in round 3 of 3 can *never* be verified, so the primitive's promise ("the operator never hunts for paths") silently degrades to "your answer was discarded" in the most common answering round; (ii) with `stop`, `:108` says in-flight explorations are abandoned and their items are Open with `unresolved because: stopped`, which collides with the `(operator claim, unverified)` qualifier — the spec does not say which reason wins; (iii) when the tree is fully visited after the answering round, the spec does not say whether the primitive renders an extra round solely to run the verification batch, or exits `empty-frontier` with the claim unverified.
**Why the spec misses it:** The "if the interview ends first, the claim reaches the hand-off unverified" sentence (`:218–219`) is attached only to the cap-overflow case, not to the no-next-round case.
**Suggested fix:** Add one rule: "A claim answered in the interview's last rendered round is not verified — no extra round is rendered for verification alone. It reaches the hand-off as an Open F-item with `fact not established (operator claim, unverified)`; on a `stop` exit the reason is `stopped`, and the qualifier is appended." Add to checklist row 6.

### F-5: A refuted claim and a never-checked claim render identically
**Severity:** P1
**Where:** spec § Design 3 (`:200–202`) and § Design 7 (`:347–351`)
**Edge case:** The exploration returns `path:line` evidence that the operator's claim is **false**.
**What happens:** Design 3 collapses four causally different outcomes — refuted, `not found`, empty return, dispatch error — into the single string `fact not established (operator claim, unverified)`. Design 7 then carries that qualifier into `## Risks / decisions` "so the spec author knows a human already asserted an answer". For a refuted claim this actively misinforms: the brief tells the spec author a human asserted an answer, and withholds the evidence that the assertion was checked and is wrong. The exploration's `path:line` — the one artifact that would settle it — is discarded. This is precisely the failure D4's recorded rationale exists to prevent ("the operator has been wrong before, and an unchecked claim becomes an axiom every downstream lens trusts"); the spec catches the unchecked case and drops the *checked-and-wrong* case on the floor.
**Why the spec misses it:** Design 3 optimizes for one legal outcome ("not confirmed"), which is right for control flow and wrong for the hand-off's information content.
**Suggested fix:** Split the qualifier: `(operator claim, refuted: <path:line>)` when the exploration returned contrary evidence, `(operator claim, unverified)` when it did not run, errored, returned empty, or returned `not found`. Carry the refuted form into `/spec-brief`'s Risks wording with the found `path:line`. Assert both in checklist row 6.

### F-6: No tripwire for a missing `ref:` field, and no reconciliation that every seeded id is reported
**Severity:** P1
**Where:** spec § Design 6, step 5 (`:294–322`)
**Edge case:** The primitive omits `ref:` from one item (an LLM renders prose; a dropped trailing field is at least as likely as a mis-echoed id), or a seeded finding is never rendered as any item at all (below the fence, truncated by the question cap, or lost in the interview).
**What happens:** Step 5 defines a tripwire for the *wrong-id* direction (`unknown ref ignored: <id>`) and none for the two *missing* directions. An item with no `ref:` field is undefined under the two-state rule (`:155–160` says every item carries one when the caller supplied ids) — 2f-i either treats it as `ref: none` (counting it into `unreferenced decisions applied`, so the finding it actually dispositioned is reported in no set) or ignores it. Either way the finding vanishes from all four id-sets and from the operator's only summary line, while the spec was edited on its behalf. The spec asserts "The four sets are disjoint after this rule" — they are disjoint but not *exhaustive*, and nothing detects the gap. This is the same class of silent mis-mapping the ticket exists to kill, moved one layer down.
**Why the spec misses it:** Step 5 is written as a set-building rule over the ids that *appear*, never as a reconciliation against the ids that were *seeded*.
**Suggested fix:** Add a completeness rule: "Every seeded id must appear in exactly one of the four sets. A seeded id that appears in no `ref:` is reported `left open` (the conservative reading) and named on a tripwire line `seeded finding unreferenced by the summary: <id>`. An Open or Settled item that carries no `ref:` field when the caller supplied ids is a contract violation: report `item missing ref: <item title>` and apply no spec edit from it." Add to checklist row 9.

### F-7: A partially-supplied id seed collapses "no id given" into `ref: none`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 (`:153–160`)
**Edge case:** A caller gives ids for some seed items and not others.
**What happens:** The rule is stated as two states "decided by what the caller supplied, **not per item**", so any id anywhere puts a `ref:` on every item. An item descending from an id-less seed item then renders `ref: none` — indistinguishable from D2's "bears on no seed item". In 2f-i that item is counted into `unreferenced decisions applied: <n>` and dispositions nothing, so the finding it actually settles stays unreported. Today only 2f-i supplies ids (and supplies them for all seed items), so this degrades gracefully — but the contract is written for arbitrary callers and states the wrong invariant.
**Why the spec misses it:** The two-state framing was chosen to keep `/grill-me` and `/spec-brief` byte-identical, and the mixed case was not considered.
**Suggested fix:** One sentence: "A caller that supplies any id supplies one for every seed item; a partially-identified seed is not a legal invocation, and the primitive reports it in the round-1 preamble rather than rendering `ref: none`."

### F-8: `ref:` id lexical form is undefined while the comma is the delimiter
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1 (`:142–144`, `:158–160`)
**Edge case:** An id that is empty, is whitespace-only, contains a comma or a newline, or is duplicated across two seed items.
**What happens:** The spec says the primitive "never parses an id, never normalizes it" and renders multiple ids "comma-separated". An id containing a comma splits into two fragments, both of which 2f-i reports as `unknown ref ignored:` while the real finding is reported nowhere (see F-6). A duplicated id makes two findings indistinguishable — the exact collision D1 exists to prevent, which lens-qualification (`:280–285`) only prevents for 2f-i's own ids. An empty id renders `ref: ` and reads as a missing field.
**Why the spec misses it:** "Opaque" was taken to mean "unconstrained"; a delimiter imposes a constraint whether or not the contract states it.
**Suggested fix:** Add: "A legal id is a non-empty string with no comma, no newline, and no leading or trailing whitespace, unique within the seed. The primitive does not normalize ids and does not validate them; a caller that violates this gets an unusable hand-off."

### F-9: Empty-section rendering is defined only for `fence-empty`, but every `empty-frontier` exit has an empty section
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 4 (`:240–241`); checklist row 4 (`:394`)
**Edge case:** The normal `empty-frontier` exit (Open frontier is empty by definition), or any exit with no facts established.
**What happens:** Design 4 introduces `_(none)_` only inside the fence-empty branch, while checklist row 4 asserts it generically as "the empty-section rendering". The commonest exit in the repo's own history (this brief's interview exited `empty-frontier`) renders an empty `### Open frontier` with no defined content, so callers see a bare header — and `/spec-brief:139`'s empty-Settled rule keys on emptiness it must first detect. Two implementers will pick two renderings.
**Why the spec misses it:** The token was introduced to solve fence-empty and its scope was never widened to the section rule it actually is.
**Suggested fix:** State the rule once in the hand-off contract, not in Design 4: "A section with no items renders `_(none)_` on the line under its header, on every exit."

### F-10: 2f-i's step-5 line is undefined when a set is empty — including the all-empty fence-empty case
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 6, step 5 (`:302–309`) and the fence-empty failure-mode bullet (`:329–331`)
**Edge case:** A `fence-empty` grill: four empty id-sets and `n == 0`.
**What happens:** The pinned line renders as `grill applied: dispositioned ; left open ; not grillable ; deferred to option 3  — docs/…/grill.md`. It reads to the operator as though a grill was applied and something moved, when the correct message is "the grill ran, nothing was askable, your one grill for this halt is spent" — the very fact D8 says `grill.md` exists to record. The spec pins the conditional rendering for the new trailing clause and leaves the four pre-existing sets' empty rendering unstated.
**Why the spec misses it:** Step 5 was revised to add a clause, not re-derived for the new exit it also introduces.
**Suggested fix:** Pin `none` as each set's empty rendering, and give the fence-empty case its own line: `grill ran: nothing above the altitude fence — no finding dispositioned; the halt's one grill is spent — docs/…/grill.md`.

### F-11: Design 3 displaces `grilling/SKILL.md:76` wholesale, including its hang rule
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3, departure 1 (`:209–213`)
**Edge case:** A verification dispatch that never returns (the host reports no timeout).
**What happens:** The departure says "The existing failed-dispatch rule (`:76`) carries a failed dispatch to the next round as a fact request; that is right when nobody has answered, and **wrong here**." Line 76 is one paragraph carrying three rules: the retry rule, the host-timeout rule, and "a dispatch that never returns blocks the round it belongs to — no prompt-level construct can cancel a pending dispatch". An implementer reading "that rule is wrong here" may exempt verification from the whole paragraph, leaving the hang case unowned — and Design 3 *increases* hang exposure, because under v1 an operator's answer ended the fact need with no dispatch at all, and under v2 every operator answer spawns one.
**Why the spec misses it:** It cites the paragraph by line number and displaces it by description; the descriptions do not line up one-to-one.
**Suggested fix:** Narrow the departure: "Only the re-ask-as-a-fact-request retry is displaced. `:76`'s host-timeout treatment and its statement that a never-returning dispatch blocks its round apply to verification dispatches unchanged; the dispatch cap bounds how many can hang."

### F-12: A partially confirmed claim has no disposition
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 (`:197–202`)
**Edge case:** The exploration finds the file the operator named but at a different line, finds the function but with different behavior, or confirms half a two-part claim.
**What happens:** The spec offers a binary (Confirmed / Not confirmed) with no rule for a partial. The primitive must judge, and the natural failure is optimistic: the fact is established with a `path:line` that does not support the operator's actual assertion, and it enters `## References` as an axiom. That is D4's stated failure mode arriving through the door D4 opened.
**Why the spec misses it:** "Confirm or refute that specific claim" assumes the exploration returns a clean verdict.
**Suggested fix:** One sentence: "Anything short of a full confirmation with a `path:line` that supports the whole claim is *not confirmed*. When the exploration establishes a *different* fact, record that fact on its own terms (source: the found `path:line`) and leave the operator's claim as an Open F-item."

### F-13: `blocked-on: F<n>` and `stopped` overlap the existing reason set with no precedence
**Severity:** P2
**Where:** spec § Design 2 (`:181–187`), against `skills/grilling/SKILL.md:108`
**Edge case:** (a) Q3 is `blocked-on: F1`, F1 resolves in round 3, and the round cap hits before Q3 is asked. (b) The operator types `stop` with an exploration in flight for F2, which blocks Q5.
**What happens:** (a) Q3 renders `blocked-on: F1` while F1 sits in `### Facts established` — the caller reads "blocked on a missing fact" and `/spec-brief` writes a Risks item that is false; the honest reason is `round-cap`. (b) `:108` assigns `stopped` to the blocked *question*; Design 2 assigns `stopped` to the *fact item*. The spec does not say whether both items appear, or which carries the reason — so a caller may see one Open item, two, or a Q-item reading `blocked-on: F2` next to an F-item reading `stopped`.
**Why the spec misses it:** It expands the reason vocabulary without stating that the reasons are mutually exclusive or how to choose when several apply.
**Suggested fix:** Add a precedence line to the Q-item reason set — `stopped` → `round-cap` → `deferred` → `blocked-on: …` — and state that on `stop` with an exploration in flight, both the F-item and its blocked question are Open, the F-item with `stopped` and the question with `blocked-on: F<n>`.

### F-14: The F-item reason set cannot distinguish four causes that a debugger needs apart
**Severity:** P3
**Where:** spec § Design 2 (`:175–179`)
**Edge case:** A fact reaches the hand-off unresolved.
**What happens:** `fact not established` covers "the operator ignored it twice" (`:88`), "the dispatch cap never reached it" (`:74`), "the dispatch failed" (`:76`), and "this host has no read-restricted agent class" (`:72`). Only the last has a rendered marker today — the `*(no read-restricted agent available in this host)*` tag on the round-1 request — and the spec gives it no carrier into the hand-off, so it is lost. A `/spec-brief` reader cannot tell "nobody asked" from "we asked and could not find out", which is the difference between re-running and pinning it in the spec.
**Why the spec misses it:** The set was derived from what is *reachable*, not from what a caller must *distinguish*.
**Suggested fix:** Allow an optional parenthetical cause on `fact not established`, mirroring F-5's qualifier: `(unanswered)`, `(not dispatched — cap)`, `(dispatch failed)`, `(no read-restricted agent in this host)`.

### F-15: Not-grillable ids are in the precedence chain and in the unknown-id rule at the same time
**Severity:** P3
**Where:** spec § Design 6, step 5 (`:311–322`)
**Edge case:** An echoed `ref:` id that names a not-grillable finding.
**What happens:** The precedence chain lists `not grillable` as its highest set, but the paragraph two lines down says not-grillable ids "never enter the seed, so they never appear in a `ref:`", and the unknown-id rule catches "a `ref:` id that 2f-i did not put in the seed" — which is exactly a not-grillable id. So the same id would be reported twice, once as `not grillable` and once as `unknown ref ignored:`, and the precedence rule's top entry is unreachable by construction.
**Why the spec misses it:** The precedence chain was written over the four printed sets, the unknown-id rule over the seed.
**Suggested fix:** Say that the unknown-id rule is evaluated first and excludes ids already in the `not grillable` set, or drop `not grillable` from the precedence chain and note that it is populated in step 1, never from `ref:`.

## Summary
P0: 2 | P1: 4 | P2: 7 | P3: 2

STATUS: RED P0=2 P1=4 P2=7 P3=2 P4=0
