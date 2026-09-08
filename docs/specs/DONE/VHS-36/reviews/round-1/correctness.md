# Correctness Review — round 1

Grounding complete. Verified all anchors against `f4d9290` (current HEAD), read the VHS-33 frozen checklist and attempt-1 Design 3, ran `lint.py --strict`, and retrieved the Plane ticket (namespace `skills`, tag-exact hit — its Done-when matches the brief verbatim).

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: Checklist row 3's `###` grep asserts 0, but the file has three `###` lines that rows 3/10 and the Design preamble all require to stay
**Severity:** P0
**Where:** spec § Test plan, row 3 (`docs/specs/TODO/VHS-36.spec.md:449`); contradicts spec § Design preamble (`:157–159`) and § Test plan row 10 (`:490–500`)
**Claim:** "No `###` heading was added: `grep -c '^###' skills/grilling/SKILL.md` → 0."
**Why this is wrong:** The command returns **3**, not 0, today and after the change:

```
skills/grilling/SKILL.md:123:### Settled
skills/grilling/SKILL.md:126:### Open frontier
skills/grilling/SKILL.md:131:### Facts established
```

`grep -c '^###'` counts lines starting with `###` regardless of the surrounding code fence. The spec knows this — its own Design preamble says "the file's only `###` markers are inside the fenced hand-off block" (`VHS-36.spec.md:157`) — and checklist row 10 *requires* those three markers to still be present verbatim (`VHS-36.spec.md:497`), re-asserting VHS-33 checklist row 5 (`docs/specs/DONE/VHS-33/spec.md`, row 5: "`### Settled` / `### Open frontier` / `### Facts established`"). Row 3 and row 10 therefore cannot both pass. Because `## Test command` is `N/A`, this checklist **is** the `/ship-spec` gate, so a row that fails by construction blocks the ship.
**Suggested fix:** Replace the command in row 3 with one that tests what the prose intends — no `###` heading *added*:
`git diff -U0 -- skills/grilling/SKILL.md | grep -c '^+###'` → 0
(or, if a whole-file form is wanted, `grep -c '^###' skills/grilling/SKILL.md` → **3**, unchanged, and note the three are the fenced hand-off subsections).

### F-2: Design 10 calls the new grilling failure-mode bullet "a fourth bullet"; there are already four, and row 8 says five
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 10 (`VHS-36.spec.md:357`) vs § Test plan row 8 (`:478–480`)
**Claim:** "A fourth bullet is inserted after `:154` (the no-read-restricted-agent bullet)."
**Why this is wrong:** `skills/grilling/SKILL.md` § Failure modes already has four bullets — `:153` Failed dispatch, `:154` No read-restricted agent class, `:155` `empty-seed`, `:156` `stop` with explorations pending. The new one is the **fifth**, which is exactly what checklist row 8 asserts ("`## Failure modes` has five bullets"). (The `/grill-me` counterpart in Design 12 *is* correctly a fourth bullet — `skills/grill-me/SKILL.md:20–22` has three — which is probably where the ordinal was copied from.) Position is unambiguous in both Design 10 and row 8, so this is a wording slip, not a mis-placement.
**Suggested fix:** In Design 10, change "A fourth bullet is inserted after `:154`" to "A fifth bullet is inserted after `:154`, third in reading order".

### F-3: Bold means "ship this" in Designs 1–6 and "reader's marker, do not ship" in Designs 7/10/13, and only Design 7 says so
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 7 (`:320–321`), § Design 10 (`:368–370`), § Design 13 (`:406–420`) vs § Test plan row 3 (`:442–447`)
**Claim:** Design 7: "(The bold marks the addition for this spec's reader; the shipped text carries no bold.)" — but Design 10's `:156` blockquote and both Design 13 blockquotes use the same convention with no such parenthetical, while Designs 1–6's blockquotes use bold as **shipped** text (row 3 asserts `**Operator answers are claims.**` etc. appear verbatim).
**Why this is wrong:** Three blockquotes carry bold with no stated disposition:
- Design 10, `:156`: `**A fact need the operator answered in the stopping round is not abandoned — its check runs before the hand-off.**`
- Design 13, `:31`: `**An operator who answers a fact request has made a claim, not established a fact: …**`
- Design 13, `:35`: `**including an operator's claim the check did not confirm, …**`

An implementer following the Designs-1–6 convention ships the `**`. No checklist row catches it: row 6 only greps `:156` for "is not abandoned", and row 13 only greps `:31`/`:35` for "has made a claim, not established a fact" / "labelled unverified" — all substring matches that pass with or without the markers. The ambiguity is sharper for `docs/spec-workflow-reference.md`, where `:31` and `:35` already legitimately carry bold (`**dispatched to a read-restricted exploration agent**`, `**hand-off block**`), so stray bold would not look out of place on review.
**Suggested fix:** Repeat Design 7's parenthetical under Designs 10 and 13, or add one sentence to the § Design preamble: "In Designs 7, 10, and 13 the bold marks the addition for this spec's reader and is not shipped; in Designs 1–6, 9, 11, and 12 the blockquote is the shipped text byte-for-byte, bold included."

### F-4: Design 6 does not reconcile "rendered anyway" with the unedited `:76` sentence "Questions downstream of a fact wait for it"
**Severity:** P2
**Where:** spec § Design 6 (`:283–289`); target file `skills/grilling/SKILL.md:76`
**Claim:** "Once a claim's check has resolved, a question that was waiting on it enters the next round's frontier whether the claim was confirmed or not… A question is left waiting only for a fact need that is still unanswered."
**Why this is wrong:** `skills/grilling/SKILL.md:76` says, unedited and three paragraphs above the insertion point, "Questions downstream of a fact wait for it; the rest of the frontier is asked in the current round." The new text re-scopes that sentence without naming it. Design 4 sets the pattern for exactly this move — it explicitly says it "displaces the failed-dispatch rule above" and names which clauses of `:78` it displaces — and attempt 1 also named the rule it was scoping (`docs/specs/DONE/VHS-33/attempt-1/spec.md:472–475`, "`:74`'s 'questions downstream of a fact wait for it' governs a fact that is still coming"). Dropping the explicit reconciliation leaves the shipped file with two sentences in the same section that a reader must reconcile unaided — the exact class of drift the round-3/round-4 P0s on attempt 1 hit. Not a hard contradiction (`:76` is naturally read as waiting for the *dispatch* to return, which a resolved-but-unconfirmed check satisfies), so it is clarity, not breakage.
**Suggested fix:** Add one clause to Design 6's first blockquote, mirroring Design 4's idiom: "…still coming — the sense in which the dispatch rule above says a downstream question waits for its fact. Once a claim's check has resolved…"

### F-5: Row 11 mis-attributes VHS-33 checklist row 11
**Severity:** P3
**Where:** spec § Test plan row 11 (`:505–506`)
**Claim:** "**Re-asserts VHS-33 checklist row 11** for `:141`/`:142`/`:88`."
**Why this is wrong:** VHS-33 checklist row 11 (`docs/specs/DONE/VHS-33/spec.md`) reads: "`git diff -U0 -- skills/spec-brief/SKILL.md` shows hunks only at `:140` and `:143`; `grep -c 'fence-empty' skills/spec-brief/SKILL.md` ≥ 1; `:140` contains `F<n>` and 'not established; spec author pins this'; `:88` unchanged." It never mentions `:141` or `:142` — those pins are VHS-36's own, from Design 11's load-bearing argument (`VHS-36.spec.md:382–388`). Only the `:88` pin and the `fence-empty` grep are actual re-assertions of row 11. Harmless to the gate (all three pins are asserted either way) but it misdescribes what is inherited.
**Suggested fix:** Reword to "**Re-asserts VHS-33 checklist row 11** for `:88` and the `fence-empty` grep; `:141`/`:142` are pinned by this spec (Design 11), and `:143` — which VHS-33 row 11 also pinned — is covered by the hunk-only-at-`:140` assertion."

### F-6: Row 17's "seven quotes" matches neither reading of the question list
**Severity:** P3
**Where:** spec § Test plan row 17 (`:530–535`)
**Claim:** "…and whether a question waiting on it renders. Each answer is a quoted sentence from the file — the reviewer records the seven quotes."
**Why this is wrong:** The listed questions are: when a check is dispatched; how many can be in flight; what happens on error, on `not found`, on partial support, and with no read-restricted agent class; what happens on `stop`; what happens on a resume; whether a gated question renders. Counted individually that is **nine**; counted as semicolon-separated groups (with the four not-confirmed causes sharing Design 3's single "Not confirmed" bullet as their one quote) it is **six**. Seven is neither, so a reviewer running the row cannot tell when it is satisfied.
**Suggested fix:** Say "records one quote per bullet below" and render the questions as an explicit numbered list, or change "seven" to "six" and mark the four not-confirmed causes as sharing one quote.

### F-7: `skills/grilling/SKILL.md:18` falls outside every no-hunk range and every phrase pin
**Severity:** P3
**Where:** spec § Test plan row 9 (`:482–489`); spec § Scope (`:42–46`)
**Claim:** Row 9: "It shows **no** hunks in `:1–17`, `:19–32` … `:144–150`." § Scope: "**Files to leave alone** — every one of these is asserted by the Test plan."
**Why this is wrong:** The ranges deliberately skip `:18` — the `seed` bullet carrying `id` / `ref:` — because VHS-33 *edited* that line and copied its range split from there (`docs/specs/DONE/VHS-33/spec.md` row 9: "no hunks in `:1–17`, `:19–32`, …"). VHS-36 does not edit `:18`, and it does not re-assert VHS-33 checklist row 7, which was the row that pinned the seed bullet's contents (`id`, `ref:`, "no `ref:` field is rendered at all"). So nothing in this spec's checklist would catch an accidental edit to `:18`. (The other gaps in the ranges — `:69`, `:79–81`, `:109` — are blank lines plus `:80`, which row 3 pins by phrase, so they are covered.)
**Suggested fix:** Change row 9's first range from `:1–17` to `:1–18`, or add "and VHS-33 checklist row 7's seed-bullet pins still hold" to row 10.

## Summary
P0: 1 | P1: 0 | P2: 3 | P3: 3 | P4: 0

Everything else checked out. Verified as accurate: all `skills/grilling/SKILL.md` anchors (`:12`, `:23`, `:48`, `:53`, `:59`, `:72`, `:74`, `:76`, `:78`, `:80`, `:87`, `:90`, `:92`, `:110`, `:121`, `:127`, `:128`, `:132`, `:135`, `:137`, `:143`, `:153–156`); `skills/spec-brief/SKILL.md:88`, `:140–142`, `:173–174`; `skills/grill-me/SKILL.md:14`, `:19–22`; `docs/spec-workflow-reference.md:23`, `:31`, `:35`. `python lint.py --strict` → exit 0, 0 errors, exactly 2 `missing-requires` WARNs (`review-pr`, `ship-spec`), so row 1 holds. Row 2's grep hits are all parentheticals with "or the equivalent", `## Tool-use notes` entries, or the prohibition itself. Row 7's `grep -c 'source: operator'` is 0 today, so → 1 after the change is right. Row 14's `≥ 6` holds (7 added lines match `operator claim|verif`). The four Done-when criteria map 1:1 to the Plane ticket's. Attempt-1 Design 3's three killed constructs — the `refuted` disposition (`attempt-1/spec.md:420–425`), the verification-overflow ordering rule (`:476–488`), and the last-rendered-round hole (`:489–495`) — are each affirmatively removed and replaced, not reintroduced. `git log` on the four files shows only the VHS-33 series (`c97d4ad`…`648f4ff`, merged as `464303f` today); the spec's anchors were read at `f4d9290`, which is HEAD, so nothing is stale.

STATUS: RED P0=1 P1=0 P2=3 P3=3 P4=0
