# Correctness Review — round 4

_(A first dispatch of this round crashed on a transport error before writing anything; this is the retry's report.)_

**Grounding performed.** Read `docs/specs/TODO/VHS-33.spec.md` and `.brief.md` fresh from disk; `CLAUDE.md` (machine-local) and `AGENTS.md` (canonical project instructions); Plane ticket VHS-33 retrieved from namespace `skills` via `memory_search` (tag_exact, confidence 1.00) — description matches the brief, no Done-when section, as the brief states. All three round-3 reports read. `scale_lens: off` and no `scalability.md` exists in `round-3/`, so the stale-report guard is a no-op. `git log -10` over the five touched files: newest commit is `d381f88` (2026-09-06, today), already recorded in § Deferred as correctness R1 F-11; no drift since.

**Anchor sweep — every path:line in the spec re-verified against the live tree.** `skills/grilling/SKILL.md` `:12`, `:18`, `:23`, `:31`, `:33–58`, `:37–44`, `:48`, `:57`, `:59–66`, `:61`, `:63`, `:68–79`, `:70`, `:72`, `:74`, `:76`, `:80–100`, `:84–86`, `:88`, `:94–98`, `:104`, `:106`, `:108`, `:110`, `:118–130`, `:129`, `:132`, `:134`, `:136–150`, `:151` — all correct (`:118` opens the fence, `:130` closes it; `:151` is the `stop` failure-mode bullet and sits outside the `:136–150` fence). `skills/spec-cycle/SKILL.md` `:366`, `:426–465`, `:453`, `:466–487`, `:489–561`, `:495–496`, `:504`, `:518–528`, `:539–546`, `:548–549`, `:556–561`, `:563–595`, `:640`, `:698–703` — all correct. `skills/spec-brief/SKILL.md` `:80`, `:84–90`, `:88`, `:92–107`, `:99`, `:105`, `:134–143`, `:139`, `:140`, `:143`, `:159`; `skills/grill-me/SKILL.md` `:14`, `:21` (two failure-mode bullets today); `docs/spec-workflow-reference.md` `:23`, `:35` (and `grep` confirms those are the file's *only* termination/hand-off paraphrases, so Design 7's two-line scope is complete); `docs/specs/DONE/VHS-32/spec.md:458` (row 4), `:460–461` (rows 6/7); wiki `decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` § 5 including the verbatim "Rejected — a success token for an empty interview" clause. **No stale anchors.**

**Gate-row satisfiability walk.** Row 4 (every v2-block string appears verbatim in the Design 2 fence, and the header reason list is byte-identical to v1) ✓. Row 5 covers every clause of `DONE/VHS-32/spec.md:458` ✓. Row 6: `grep -c 'fence-empty' skills/grilling/SKILL.md` yields exactly 3 lines (`:104`, the one-line `:106` paragraph, the block header) ✓; `:104` lists exactly six tokens ✓. Row 7: `grep -c 'ref:' skills/grilling/SKILL.md` is **0** today and the Designs produce exactly 7 matching lines (seed bullet, `ref:` paragraph, four block lines, callers-map sentence) — the file is unwrapped, one paragraph per line ✓. Row 9's diff fences hold (Design 4's insertion lands at old-side 57/58, outside `:59–100`; Design 3's `:151` edit is outside `:136–150`) ✓. Row 11: the new `:140` and `:143` are single unwrapped bullets, so both greps land ✓. Row 16: I re-derived the grep over every added/modified line the Designs pin in `grilling` and `spec-brief` — zero hits on `operator claim|verif|qualifier|source: operator` ✓. Rows 12, 13, 14, 15 ✓. **One row is not literally executable — F-1 below.**

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Design 7's `:23` deletes the altitude-fence parenthetical | CLOSED | spec:398–402 blockquote now "fully visited, or that a later round's remaining candidates all fell below the altitude fence — either way the reason line says which"; row 13 (spec:491–494) asserts "altitude fence" ≥2× and "either way the reason line says which"; count verified = 2 |
| correctness | F-2 (P2) | Design 1 "byte-identical" overstated | CLOSED | spec:200–204 narrowed to "the Settled and Open-question lines"; Design 2 bullet spec:229–231 and Risk 1 spec:551–555 narrowed in step |
| correctness | F-3 (P2) | `:106`'s "normally empty" reason clause wrong for `/spec-brief` | CLOSED (see F-2 below for a residual variant) | spec:279 now "empty unless the seed supplied facts or a dispatch returned one"; Design 2 spec:245–249 and Risk 2 spec:559 restated |
| correctness | F-4 (P2) | Design 5 step 5 doesn't say which text ships; both-lists rule ungated | CLOSED | spec:328–329 "The code block replaces `:548–549`; the bullets below are added to step 5 in the file"; row 10 (spec:475–477) asserts "is listed here rather than under `dispositioned`" and "in seed order" |
| correctness | F-5 (P4) | Row 10's `grep -c 'total_p0p1 == 0'` names no file | CLOSED | spec:471 now names `skills/spec-cycle/SKILL.md` |
| edge-cases | F-1 (P1) | `:23` deletes the round-≥2 fence-out record | CLOSED | same edit as correctness F-1 |
| edge-cases | F-2 (P2) | `:106` rationale drops seed facts | CLOSED | same edit as correctness F-3 |
| edge-cases | F-3 (P2) | Id on an applied and an unapplied Settled item | CLOSED (deferred with rule) | spec:619–623, `## Deferred (P2+)`, carries the rule to adopt |
| edge-cases | F-4 (P2) | Summary with no `ref:` fields has no step-4 rule | CLOSED | spec:319–320 "or with no `ref:` field at all, which is what a v1-shaped return looks like"; row 10 (spec:475) asserts it |
| edge-cases | F-5 (P3) | `ref:` ids across a `prior_summary` resume | CLOSED (deferred with rule) | spec:624–629 |
| edge-cases | F-6 (P3) | `<token>` undefined when the header carries none | CLOSED | spec:331–332 "when the header carries none, print `unknown` — the persisted block is the record" |
| edge-cases | F-7 (P4) | Row 9's `:132` names a shifted line | CLOSED | spec:469 "The pre-edit `:132`" |
| conventions | F-1 (P2) | Reason-keyed `:143` missing from the roll-up | CLOSED | spec:86–90 adds the bullet in the roll-up's shape, near-verbatim to the suggested fix |
| conventions | F-2 (P2) | D4 still says "empty sections" | CLOSED | D4 spec:117–119 "with its Settled and Open frontier sections empty"; D6 spec:131–132 qualified to the 2f-i path; Design 7's grill-me blockquote spec:394–396 drops "and empty sections" |
| conventions | F-3 (P4) | `## Deferred (P2+)` preamble stale | CLOSED | spec:599–600 "Every other round-1, round-2 and round-3 P2+ finding was folded" — matches the actual round-3 dispositions I re-derived |

No REOPENED items. Both round-3 P1s are closed by one edit that I verified renders the fence case on both exits and is now gate-held.

## Findings

### F-1: Row 10 asserts phrases against `spec-cycle/SKILL.md`, which is hard-wrapped — one clause is already unsatisfiable as a grep today, and six more are wrap-fragile
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan preamble (`:419`) and row 10 (`:470–485`)
**Claim:** `:419` — "Every row is a grep or a diff against the worktree." Row 10 — "**Supersedes VHS-32 checklist row 7:** `### 2f-i` still contains "never re-dispatches reviewers", "never increments the round counter", "never overwrites", "at most once per invocation", **"never edits the brief"**, …"
**Why this is wrong:** `skills/grilling/SKILL.md` is unwrapped — the spec says so explicitly and leans on it in row 7 ("the file is unwrapped, one paragraph per line"). `skills/spec-cycle/SKILL.md` is **hard-wrapped at ~78 columns**, and the spec makes no equivalent note. The closing paragraph at `:556–558` reads:

```
2f-i never re-dispatches reviewers, never increments the round counter, never
changes the gate formula, never overwrites a prior `grill.md`, never edits the
brief, and runs at most once per invocation.
```

`grep -c "never edits the brief" skills/spec-cycle/SKILL.md` returns **0** on the live file (I ran it; every other row-10 string returns ≥1). The phrase straddles `:557`/`:558`. So as a literal grep the row fails today and will fail after the change — and Design 5 (`:359–360`) explicitly forbids the only edit that would fix it: "The closing paragraph (`:556–561` …) is untouched." An implementer who takes the preamble at its word gets a red gate row with no legal remedy, and the tempting remedy — reflowing `:556–558` — is inside row 10's own permitted hunk range (`:489–561`) and would silently violate Design 5.

Six further row-10 assertions target text this spec asks the implementer to *write into* the wrapped file, so each can straddle a break depending on where the implementer wraps: "is listed here rather than under `dispositioned`", "in seed order", "not the full red list" (step 5 bullets), "by its `ref:` ids, never by title" and "or with no `ref:` field at all" (step 4), and "A `fence-empty` exit is the same shape" (`:698–703`). Row 10's two single-line assertions are safe — the replaced `:548–549` is one long backticked line carrying both `grill applied (exit: <token>):` and `unreferenced decisions applied: <n>` — and so is `<lens>/<finding-id>` in step 1. Rows 4–7 and 11 are unaffected because `grilling` and `spec-brief`'s mapping bullets are unwrapped.

This is P2, not P1: the shipped skill text is correct either way, and a reader who checks the section prose rather than running `grep` passes the row. VHS-32's row 7 shipped with the identical defect. But the spec states the checklist *is* the `/ship-spec` gate (`:420–421`), so a row that cannot pass is worth one sentence.
**Suggested fix:** Add one sentence to the Test-plan preamble: "`skills/spec-cycle/SKILL.md` is hard-wrapped; phrase assertions against it are checked over the section text (e.g. `tr '\n' ' '` before grepping), not line-anchored — `never edits the brief` already spans `:557–558` in the pre-edit file." No new construct, no row change.

---

### F-2: Risk 2 says a fence-empty brief has "no Scope rows", but the same spec's callers-map sentence feeds Facts into Scope and `spec-brief:141` emits a row per fact-named path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Risks 2 (`:556–559`), against § Design 2's callers-map blockquote (`:253–257`) and `skills/spec-brief/SKILL.md:141`
**Claim:** "`/spec-brief` does not halt on it (Design 6), so the brief is written with `_(none settled …)_` under Decisions, an empty Risks list, **no Scope rows**, and no fact References beyond the ones Phase 1's grounding already supplied"
**Why this is wrong:** Round 3 corrected the References half of this sentence (correctness F-3 / edge-cases F-2) but left the Scope half carrying the same superseded assumption. `skills/spec-brief/SKILL.md:141` reads: "`## Scope` gets one row per path the settled decisions **and grounding facts** name: `Current` filled from a fact with its `path:line`, `Change` from the settled decision that touches it. A path with no read file or fact behind it gets no row…" — so a path *with* a fact behind it does get a row, with `Current` filled and `Change` empty. Design 6 does not edit `:141`, and the spec's own callers-map replacement (`:255–256`) keeps "feeds Facts into Scope and References" — so the spec asserts in one section that facts feed Scope and in another that a fence-empty brief has no Scope rows, on the exact path (`/spec-brief`, which grounds first) where Design 2 (`:246–248`) says Facts established is "normally not empty."

Nothing ships from Risk 2 — it is a spec-side accepted-risk narrative, so this misdescribes the outcome rather than misdirecting an implementer, which is why it is P2. But it is the last residue of a root the round-3 fold otherwise closed, and it understates the artifact (`/spec-close` reconciles against this section).
**Suggested fix:** Replace "no Scope rows" with "at most the Scope rows Phase 1's grounding facts name, each with an empty `Change` column (`spec-brief:141`)". One clause, inside the sentence already rewritten in round 3.

---

### F-3: Design 6's shipped `:143` example renders "1 round" against its own "`<n> rounds`" template
**Severity:** P4
**Where:** spec § Design 6, `:379–384` (shipped text for `skills/spec-brief/SKILL.md:143`)
**Claim:** "> The exit token and round count go in a final `## References` bullet: `Interview: <n> rounds, exit <token>` … `Interview: 1 round, exit fence-empty (no candidate decision met the altitude fence)`"
**Why this is wrong:** The template pins the literal word `rounds`; the worked example immediately below renders the singular `round`. Both are shipped file text after this change, so `/spec-brief` carries a rule whose example does not match its own format string — an implementer following the template literally writes "Interview: 1 rounds". The live `:159` print block has the same `<n> rounds` template and is not edited, so the two surfaces would also disagree with each other on a one-round exit. Row 11 asserts neither string, so it is gate-invisible. Cosmetic only.
**Suggested fix:** Either write the example as `Interview: 1 rounds, exit fence-empty (…)` to match the template, or change the template to `Interview: <n> round(s)`. The first is the smaller edit and keeps `:143` consistent with the untouched `:159`.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 0 | P4: 1

STATUS: GREEN
