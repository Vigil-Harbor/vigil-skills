# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: Design 1's `ref:` omission and descent rules have no landing anchor in the file they must ship in

**Severity:** P1
**Where:** spec.md:154–163 (Design 1 "Descent" / "Rendering"), cross-checked against spec.md:24 (Scope table) and spec.md:369–371 (checklist row 7)
**Convention violated:** Brief decision 1 — "an optional caller-supplied `id` … echoed verbatim as a `ref:` field on every Settled and Open item that descends from it … **absent when the caller passed none**." Also the spec's own rule that "the checklist is the gate" (spec.md:32, :341).
**Evidence:** Design 1 has three parts. Only the first carries a file anchor and a blockquote of the text to write: "**Invocation contract** (`skills/grilling/SKILL.md:18`). The `seed` bullet gains one sentence: > Each seed item may carry an optional **`id`** …". The "**Descent.**" and "**Rendering.**" paragraphs carry no anchor and no blockquote. The Scope table's `grilling` cell allocates Design 1 only to `:18`. Checklist row 7 enumerates the expected `ref:` occurrences as exactly "seed bullet, four block lines, callers-map sentence" (`grep -c 'ref:' ≥ 6`) — leaving no room for a descent or rendering paragraph in the shipped file.

The consequence is load-bearing, not cosmetic. The block template the spec *does* pin (spec.md:173) reads `ref: <id>[, <id>…] | none`, which tells a reader of the shipped `SKILL.md` that `none` is the value when there are no ids. The omission rule — the field is not rendered *at all* when no seed item carried an `id` — exists nowhere in the text the spec commits to writing. Without it the primitive renders `ref: none` on every item for `/spec-brief` and `/grill-me`, which contradicts Design 6's premise ("`/spec-brief` passes no seed ids, so the block it receives has no `ref:` fields", spec.md:291) and voids Risk 1's mitigation ("`/spec-brief` and `/grill-me` supply none and see v1 lines", spec.md:445). Design 6 leaves `/spec-brief`'s Phase 4 mapping rules unchanged, so those `ref: none` fields would flow into `## Risks / decisions` text unhandled.

The descent rule has the same gap: nothing in the shipped file would tell the primitive *which* ids a given Settled item carries, only that it echoes ids "on every … item that descends from it".

**Suggested fix:** Decide explicitly whether "Descent" and "Rendering" are file text or spec-side explanation, and say so. If file text (recommended for the omission rule at minimum): give each an anchor in Design 1 and a Scope-table entry, e.g. fold the omission rule into the `:18` blockquote — "… If no seed item carried an `id`, the field is not rendered on any item." — and add it to checklist row 7 as a verbatim assertion, correcting row 7's `ref:` count accordingly. If explanation only, state that the block's `| none` arm is the sole in-file expression and reconcile Design 6 and Risk 1 with it.

---

### F-2: The "Spec-level additions" roll-up is not complete, though it claims to be

**Severity:** P2
**Where:** spec.md:52–70 (`## Decisions`, "Spec-level additions" + "Nothing else.")
**Convention violated:** Brief decision 12 ("The spec stays inside the brief… If a reviewer finding seems to need one, the spec lists it") and the spec's own D12 (spec.md:132–135, "The additions roll-up above is the complete list").
**Evidence:** At least two load-bearing constructs the brief does not name are absent from the four-bullet roll-up:

1. **The dual-representation rule for `fact not established`** (spec.md:196–199): "`fact not established` stays in the Q-item list for callers already matching it; the primitive now renders the fact as an F-item and the waiting question as `blocked-on: F<n>`." The brief's decision 3 says only that the F-item reason set "is exactly those two values" — it authorizes nothing about what the Q-item list keeps. Risk 2 (spec.md:446–450) discusses it, but Risk is not the roll-up, and the roll-up is what the Phase 3 drift-check reads.
2. **"Omit the clause when `n` is 0"** (spec.md:276) — a formatting rule the brief's Risk 1 pin does not carry. The brief pinned the `unreferenced decisions applied: <n>` clause and then said "reuse it, **and stop there**" (brief.md:81); attempt 1's accretion of "extra step-5 clauses" is named in brief decision 12 as the thing not to repeat.

**Suggested fix:** Add both to the roll-up with their one-line justification, or delete the constructs. The roll-up is the artifact the drift-check trusts; an incomplete one is worse than a longer one.

---

### F-3: `fact not established` is kept on the Q-item line for consumers that do not exist

**Severity:** P2
**Where:** spec.md:196–199 (Design 2), spec.md:176 (the Q-line in the v2 block), spec.md:446–450 (Risk 2)
**Convention violated:** Unneeded backwards-compat — a retained value with no identified consumer, kept "for callers already matching it."
**Evidence:** `grep -rn 'fact not established' --include=*.md .` (excluding `docs/specs/`) returns only `skills/grilling/SKILL.md:74`, `:88`, and `:125` — the primitive's own text. No caller matches on the string: `/spec-brief`'s Phase 4 maps Open items generically (`skills/spec-brief/SKILL.md:140`), `/grill-me` delivers the block verbatim, and 2f-i's step 5 does not read reasons. The spec's own D3 (spec.md:86–89) reassigns `:74`'s and `:88`'s routing to the F-form, and Design 2 states the primitive "now renders the fact as an F-item" — so after this change no code path produces a Q-item with that reason. The value is dead the moment the spec lands.

Risk 2's rationale ("removing it is the kind of narrowing attempt 1 spent rounds on") does not hold on inspection: deleting one alternative from an enum the spec is already rewriting verbatim is a smaller edit than keeping it plus the two explanatory sentences plus the Risk entry.

**Suggested fix:** Either drop `fact not established` from the Q-item reason list in the v2 block (and from checklist row 4's assertion, which currently does not pin it either way), or — if kept deliberately — name the consumer it is kept for and list it in the additions roll-up per F-2.

---

### F-4: The closure-manifest anchor cited to justify lens-qualified ids is wrong

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:55–57 (additions roll-up bullet 1), spec.md:464 (References)
**Convention violated:** AGENTS.md § Plan & Spec Reviews — "Always verify load-bearing claims against the actual codebase … never review from memory or stale buffers." The whole justification for this spec-level addition is "reuse of an existing form", so its citation is load-bearing.
**Evidence:** The spec says the `<lens>/<finding-id>` form is "already used at `skills/spec-cycle/SKILL.md:349`". Line 349 is `- \`round_number: <N>\`` — a reviewer-prompt parameter. The form actually appears at `:366` (`- <lens>/<finding-id> (P<sev>) "<title>" — <how addressed, with spec § anchor>`), `:373`, and — better still for this spec's purposes — at `:504`, inside 2f-i itself (`not grillable: <lens>/<id> — reviewer report unavailable`).
**Suggested fix:** Re-cite as `skills/spec-cycle/SKILL.md:366` (2b closure manifest) and add `:504` (2f-i already emits the same form in its not-grillable line) — the second anchor makes the reuse argument stronger, since it shows 2f-i's own output already speaks this id form.

---

### F-5: The Scope table promises the workflow reference will "name six exits"; Design 7 does not, and no checklist row asks for it

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:28 (Scope table, `docs/spec-workflow-reference.md` row) vs spec.md:319–327 (Design 7) and spec.md:391–392 (checklist row 13)
**Convention violated:** Internal consistency between Scope, Design, and the checklist that is declared the gate (spec.md:32).
**Evidence:** The Scope cell reads "Paraphrase names six exits, `ref:`, and F-items (Design 7)". Design 7's replacement text for `:23` names five termination *shapes* — emptied frontier, fence-empty, cap hit, operator stop, empty seed — and never mentions `revised-after-cap (+1 round)`. Checklist row 13 asserts only `grep -c 'fence-empty' ≥ 1` plus `ref:` and "unestablished fact" at `:35`. Nothing anywhere requires six exits.
**Suggested fix:** Correct the Scope cell to what Design 7 actually does ("paraphrase gains the fence-empty shape, `ref:`, and unestablished facts"). Naming all six tokens in a prose paraphrase is not obviously desirable — the reference deliberately describes shapes, not tokens — so fix the Scope cell rather than the design.

---

### F-6: Two Scope-table changes have a Design but no asserting checklist row

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:24 and :25 (Scope table) vs the checklist at spec.md:345–397
**Convention violated:** The spec's own gate rule — "`## Test command` is `N/A`; the checklist is the gate" (spec.md:32, :341). A change with no asserting row can silently fail to ship.
**Evidence:**
- **Callers-map sentence** (Scope row 1, Design 2 at spec.md:203–209). Row 4 pins the block lines; row 7 counts the sentence only as one of six `ref:` occurrences. Nothing asserts its new content — "Open Q-items and F-items into `## Risks / decisions`", "matching each decision to its findings by `ref:`".
- **2f-i failure-modes sentence** (Scope row 2, Design 5 at spec.md:282–284). Row 10 permits a hunk at `:698–703` but requires nothing there. If the implementer skips the sentence, every row still passes.

**Suggested fix:** Extend row 7 (or add a row) to assert the callers-map sentence contains `F-items` and "by `ref:`"; extend row 10 to assert `skills/spec-cycle/SKILL.md` contains "A `fence-empty` exit is the same shape".

---

### F-7: Checklist row 10 does not re-assert the VHS-32 row-7 invariants this spec's 2f-i edits put at risk

**Severity:** P2
**Where:** spec.md:109–112 (D7), spec.md:379–385 (checklist row 10)
**Convention violated:** D7's own supersession logic — the archived VHS-32 checklist is not re-runnable (`docs/specs/DONE/VHS-32/` is untouched), so any assertion this spec's diff could break must be re-asserted here.
**Evidence:** D7 and row 5 handle VHS-32 checklist row 4 (the `grilling` body) carefully and completely — I verified row 5 against `docs/specs/DONE/VHS-32/spec.md:458` string by string, and it covers every one. But this spec also edits `### 2f-i`, which VHS-32 checklist **row 7** (`spec.md:461`) pins: "never re-dispatches reviewers", "never increments the round counter", "never overwrites", "at most once per invocation", "never edits the brief", "not grillable", "nothing grillable", "deferred to option 3", and the `docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md` path. Row 10 here re-asserts only the last two of those nine ("at most once per invocation", "never edits the brief"). Step 5 is being rewritten verbatim and it is where "deferred to option 3" and "not grillable" live.
**Suggested fix:** Extend row 10 (or add a row 10b, mirroring row 5's supersession pattern for `grilling`) re-asserting VHS-32 row 7's nine strings, and state in D7 that row 5 supersedes VHS-32 row 4 *and* the new row supersedes VHS-32 rows 6–7.

---

### F-8: Three `spec-cycle` anchors are off by one, against a Risk-4 claim that all were read at `7403cb5`

**Severity:** P3
**Where:** spec.md:249 (`:494–495`), :254 (`:538–546`), :286 (`:555–560`), :464–467 (References); claim at spec.md:454–455
**Convention violated:** Risk 4's own assertion — "All anchors were read at `7403cb5` on 2026-09-06".
**Evidence:** At `7403cb5`: the step-1 phrase "extract each remaining P0/P1 finding: id, severity, title, body" spans `:495–496`, not `:494–495` (line 494 is "is stale from a prior on-run and is ignored, matching the closure-read guard in"). Step 4 begins at `:539`, not `:538` (blank). The closing paragraph is `:556–561`, not `:555–560`. The `grilling` and `spec-brief` anchors I spot-checked (`:12`, `:18`, `:23`, `:31`, `:37–44`, `:57`, `:61`, `:70`, `:72`, `:74`, `:76`, `:84–86`, `:88`, `:94–98`, `:104`, `:106`, `:108`, `:110`, `:119–130`, `:132`, `:134`; `spec-brief:80`, `:88`, `:139`, `:140`, `:143`; `grill-me:14`, `:21`; `spec-workflow-reference:23`, `:35`) are all correct — the drift is confined to `spec-cycle`.
**Suggested fix:** Shift the three `spec-cycle` anchors by one. Each edit is also pinned by a verbatim quote, so this is cosmetic — but Risk 4 makes an accuracy claim the anchors should honor.

---

### F-9: "the same shape `:80` uses" is not the same string

**Severity:** P3
**Where:** spec.md:298–300 (Design 6, `:140` replacement)
**Convention violated:** Reuse-vs-duplicate precision — a claimed reuse that is not verbatim invites an implementer to copy the wrong text.
**Evidence:** The spec writes the F-item mapping as `<fact needed> — not established; spec author pins this` and calls it "the same shape `:80` uses for a failed exploration under `--no-grill`". `skills/spec-brief/SKILL.md:80` actually reads `<fact needed> — not established (exploration failed); spec author pins this` — the cause parenthetical differs, deliberately (a different cause), but the claim as written says "same".
**Suggested fix:** "the same shape `:80` uses, without its `(exploration failed)` cause" — one clause, and it also forestalls a reviewer reading the omitted parenthetical as the "cause qualifiers" D12 forbids.

---

### F-10: Checklist row 14's untouched-file fence omits `README.md` and `AGENTS.md`

**Severity:** P3
**Where:** spec.md:393–394 (checklist row 14), spec.md:46 (Files to leave alone)
**Convention violated:** The spec's five-file fence; VHS-32's precedent, whose checklist row 8 (`docs/specs/DONE/VHS-32/spec.md:462`) explicitly gated `AGENTS.md`, `docs/spec-workflow-reference.md`, and `README.md` together as the three prose surfaces.
**Evidence:** Row 14 fences `agents/`, `skills/ship-spec/`, `skills/spec-close/`, `docs/specs/DONE/`, `lint.py`, `sync.py`, `tests/` — but not the two tracked prose files that also mention `grilling` (`README.md:13,16,64`; `AGENTS.md` § spec lifecycle). I verified neither paraphrases the hand-off contract or the exit tokens, so excluding them from *scope* is correct — but they should be named in the fence so the diff can't quietly grow. `docs/customizing.md` and `docs/portability-contract.md` are likewise unfenced.
**Suggested fix:** Add `README.md`, `AGENTS.md`, and `docs/` (other than `docs/spec-workflow-reference.md`) to row 14 and to `## Scope` → "Files to leave alone", with a one-line note that neither README nor AGENTS.md paraphrases the contract.

---

## Notes (no finding)

Things I checked that hold, so later rounds need not re-derive them:

- **VHS-32 checklist row 4 supersession (D7) is honest.** I compared spec.md:358–365 against `docs/specs/DONE/VHS-32/spec.md:458` string by string; every assertion is carried. `docs/specs/DONE/VHS-32/` is untouched by every row.
- **The `grilling:68–79` fence is intact.** No design edits it; checklist row 9's no-hunk ranges (`:1–17`, `:19–32`, `:59–100`, `:136–151`) cover every "Files to leave alone" range for that file, including `:68–79` and the bounds. Row 16's VHS-36 grep is a real fence, not decoration.
- **Spec-template conformance** with `skills/spec-cycle/SKILL.md:300–313`: Goal / Scope / Design / Test plan / Test command `N/A` with a review checklist / Done when / Out of scope all present; every brief decision has a named `### D<n>` subsection; D13 records the `## Scale` non-factor as the required carried-forward Decision.
- **Out-of-scope parity**: the spec's 11 fences map 1:1 onto the brief's 11, with no additions.
- **No premature abstraction.** `ref:` is a field on an existing line, `blocked-on: F<n>` reuses the existing `blocked-on: Q<m>` form, and the lens-qualified id reuses a form already in `spec-cycle` (see F-4 for the correct anchor). No registry, dispatcher, or strategy pattern appears.
- **Consumer sweep**: the five files in scope are the complete set that parse or paraphrase the hand-off block. `lint.py`, `sync.py`, and `tests/` contain no reference to `skills/grilling`, confirming the brief's fact F1.

## Summary
P0: 0 | P1: 1 | P2: 6 | P3: 3 | P4: 0

STATUS: RED P0=0 P1=1 P2=6 P3=3 P4=0
