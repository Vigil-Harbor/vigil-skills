# Edge-Cases Review — round 4

## Closure of round 3 findings

`scale_lens == off` and `round-3/` contains no `scalability.md`, so the three standing lenses are the full prior round.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | D16 vs Design 3 on re-run recount | CLOSED | spec:49 — "On a re-run there is no in-context fold record, so the recount does not run at all and the new finding is routed by Design 1 with no recount suffix" |
| correctness | F-2 | Input-line clause points at text that says nothing about the revert line | CLOSED | spec:148 block now carries the round-qualified-line rule verbatim; spec:144 cites only the block |
| correctness | F-3 | R4 omits `## Test command` | CLOSED | spec:101 list now includes `## Test command`; matches `SKILL.md:300-307` |
| correctness | F-4 | "exactly one line" cited at `:369-371` | CLOSED | spec:121 now splits `:370-371` (unchanged) from `:378-379` (gains the exception); verified `SKILL.md:379` carries the sentence |
| correctness | F-5 | Removal with no successor; merge collapses below the floor | CLOSED | spec:99 adds `(removed round <n>)`; floor restated as "two or more **entries**"; spec:148 mirrors both |
| correctness | F-6 | `Suggested fix (verbatim):` label drift | CLOSED | spec:89 label is now `**Suggested fix:**` with "verbatim" in the value hint |
| correctness | F-7 | Row 10 pins unspecified wording | CLOSED | spec:21 quotes the sentence verbatim; row 10's `including round 1` is inside it (baseline verified 0 today) |
| correctness | F-8 | Row 5's exact 8 breaks on wrap | CLOSED | spec:162 now "8 or 9" with the wrap rationale |
| correctness | F-9 | Reverted-fold supersession stated in the wrong branch, match key unstated | CLOSED | spec:74 places it in the round-4 paragraph and pins `finding_id` ↔ `Finding:` |
| edge-cases | F-1 | Round-4 FROZEN leaves a routing violation unrepairable; D15 contradicts `:438-439` | CLOSED | spec:48/:74 — the unresolved-P0/P1 test "does not apply to it", R2's edits permitted without promotion; row 9 literal updated. *(New variant at round 4 for R6 — see F-3 below.)* |
| edge-cases | F-2 | Preamble check has no textual key in the agents | CLOSED (with residue) | spec:148 requires "a blockquote containing the sentence …"; row 6 greps it per agent file. Residue filed as F-4 below |
| edge-cases | F-3 | Verbatim `Suggested fix` truncates the section / invents rows | CLOSED | spec:89-90 blockquotes the field; spec:78 and :133 define extent as "next `##` not inside a blockquote"; `> `-prefixed lines excluded in both producer and consumer |
| edge-cases | F-4 | Duplicate section undefined | CLOSED (with residue) | spec:103 rule R6 + spec:148 `routing violation: duplicate section`. Round-4 residue filed as F-3 below |
| edge-cases | F-5 | Row 5's exact `→ 8` | CLOSED | spec:162 |
| edge-cases | F-6 | Re-anchor has no target on removal | CLOSED | spec:99 `(removed round <n>)`; spec:148 waives the existing-site test when any marker is present |
| edge-cases | F-7 | Settled grill deferral has no landing place | CLOSED | spec:70 — discharged as an appended row with `Deferred in: round 4 (grill)`; 2f-i step 5 re-render shows it |
| edge-cases | F-8 | No row asserts the block's substance reaches the agents | CLOSED | spec:163 row 6 adds per-file `must not implement anything in this section`, `routing violation: missing preamble`, `in-scope P0` |
| edge-cases | F-9 | Marker appended field-level, read site-level | CLOSED | spec:99 — "the marker goes on that entry, not on the field" |
| conventions | F-1 | Row 8's `Follow-up: unfiled` falsified by the row shape | CLOSED | spec:165 asserts `**Follow-up:** unfiled` → 1 and `— Follow-up: unfiled` → 1; both verified against spec:93 and spec:129 |
| conventions | F-2 | D15 append-only vs R2 repair at round 4 | CLOSED | spec:48/:74 (same fix as edge-cases/F-1) |
| conventions | F-3 | Rows 5 and 9 assert wrap-sensitive counts/phrases | PARTIAL | Row 5 fixed (spec:162); row 9 replaced one fragile phrase with another (`governed by rule R2`, `deferred: D-<n> (§ Deferred — follow-up required)`) and row 3 has the same exposure — see F-6 |
| conventions | F-4 | Row 10 pins an unspecified literal | CLOSED | spec:21 |
| conventions | F-5 | Three sections claim "end of spec"; render has no terminator | CLOSED | spec:78 and :133 define the section's extent |
| conventions | F-6 | "immediately under the heading" invites a false preamble P0 | PARTIAL (P4) | The placement half is closed ("first non-blank content under the heading", spec:148); the "substance, not byte-equality" half was declined in favour of a strict textual key, which now mismatches the preamble — see F-4 |

## Findings

### F-1: A row recording an **in-scope P0** is well-formed by every check the spec adds, so the ceiling's one hard rule is unenforced and the gate can go green with an unshippable spec

**Severity:** P1
**Where:** spec.md:148 (§ Design 7, the Deferred-findings block), against spec.md:31 (Decision 1), spec.md:67 (Design 1 step 3), spec.md:47 (D14)
**Edge case:** The author writes a deferral row for a finding that is genuinely in-scope and genuinely P0 — an authoring error, or a row inherited across a re-run, or a row produced by F-2's path below. The row is honest: `**Finding:** correctness/R2/F-3 (P0)` and `**Scope:** in-scope — § Scope row 3`.
**What happens:** Nothing catches it, and the gate can go green.

- The block's well-formedness test is purely structural: seven fields present, `Propagation sites` has two-or-more entries with at least one existing. A P0/in-scope row passes all of it.
- The block's routing-violation clause fires only when the `Scope` field "is wrong in a way that changes the routing (**an in-scope P0 recorded as out-of-scope**)". Here `Scope` is *correct*, so the clause does not fire. D17 gives the conventions lens the job of verifying the field's truth, not of testing the row against the ceiling.
- The only remaining backstop is D14's carve-out: "unless the candidate is an in-scope P0, which is always filed". That fires only if some lens **regenerates the finding** that round *and* independently classifies it in-scope. Reviewers regenerate findings from spec text non-deterministically — that is the brief's own founding premise ("findings are regenerated by the reviewers from the spec text each round"). On any round where no lens happens to re-raise it, `total_p0p1 == 0` and the spec goes green carrying a P0 the brief says "is the one thing a spec cannot ship as a known issue".

This falsifies the exact guarantee Decision 1 makes to the operator at spec:31 — "an in-scope P0 is never suppressed, so the count cannot hide the one class that blocks shipping." As written, the count *can* hide it: suppression is not required for the hiding, silence is enough.
**Why the spec misses it:** Round-1 edge-cases/F-2 asked "can suppression hide an in-scope P0?" and was closed by adding the filing exception on the *candidate* side. Nobody then asked the mirror question on the *row* side: the row shape at spec:86 explicitly admits `(P0 | P1)` (correctly — an out-of-scope P0 with two sites defers), and no consumer rule ever reads severity and scope together. Design 1 step 3 states the ceiling for the producer; the verification architecture the spec builds (D17: author classifies, reviewer verifies) is never pointed at it.
**Suggested fix:** One clause in the byte-identical block at spec:148, immediately after the `Scope`-verification sentence: "A row whose `Finding` severity is `P0` and whose `Scope` is `in-scope` is itself a routing violation whatever else it satisfies — the ceiling forbids deferring an in-scope P0. File it once, as a P0 titled `routing violation: D-<n>`, naming the ceiling; every lens applies this test (it reads the row's own two labels and needs no independent scope call)." Add to checklist row 6: `grep -cF 'in-scope' agents/spec-reviewer-*.md` is already covered — extend it with a per-file `grep -cF 'forbids deferring an in-scope P0'` → 1.

---

### F-2: Design 3's revert path defers the **new** finding unconditionally, bypassing both the scope ceiling and the propagation-site test for it

**Severity:** P1
**Where:** spec.md:110 (§ Design 3, second bullet), against spec.md:61-67 (Design 1 steps 1–3) and brief Decision 2
**Edge case:** Round 2 folds an out-of-scope P1 at one site. Round 3 files a **new, in-scope P0** whose `Where` lands on that same section — the exact scenario Design 3 exists to detect, and the common one: the brief's own VHS-41 specimen is characterised as a run "whose findings were all in-scope mechanics".
**What happens:** The recount fires. Its second bullet reads:

> True count now two or more, **and the original finding is not an in-scope P0**, and this is round 2 or 3, and none of the original fold's sites has been re-edited by a later fold → **revert the original fold** … and **defer both findings as two rows**.

Every guard on that bullet tests the **original** finding. The new finding is deferred by fiat: it never runs Design 1 step 2 (classify scope) or step 3 (apply the ceiling). So an in-scope P0 is routed to defer, which Design 1 step 3 forbids in the same insertion ("two or more sites, in-scope, P0 → **fold**: edit every site on the list") and which brief Decision 2 makes load-bearing. Concretely: the spec is inconsistent or unimplementable, `/spec-cycle` records that as a known issue, and — via F-1 above — nothing downstream catches the row. The bullet is also the only way a **trivial** finding gets deferred: the new finding may have exactly one propagation site of its own, and Decision 3's non-trivial test never runs on it either.
**Why the spec misses it:** The ceiling was clearly in view when this bullet was written — it is the reason for the "not an in-scope P0" guard — but the guard was applied to the finding being *reverted*, not to the finding being *newly routed*. The recount's framing ("evidence that the original site list was short") keeps the attention on the original.
**Suggested fix:** Qualify the "defer both" clause at spec:110: "→ **revert the original fold** (remove the edit from every site it touched), defer the original finding as a row, and route the new finding through Design 1 steps 1–3 as normal. If the ceiling routes the new finding to **fold** (in-scope P0, or one site or none), the original is still reverted and deferred and the new finding is folded at every site on its own list; only a new finding the ceiling routes to defer becomes the second row." Mirror the qualifier in Decision 4's one-line restatement at spec:34.

---

### F-3: R6's duplicate-section merge is not among the round-4 permitted edits, so a duplicate present at round 4 halts the run red with no legal repair

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:48 (D15), spec.md:74 (§ Design 1 "Round 4" — the text that ships), spec.md:103 (rule R6), spec.md:148 (block)
**Edge case:** Two `## Deferred — follow-up required` headings are present when round 4 runs — reachable through the documented option-1 hand-patch, through a re-run adopting a spec that already had two (R4 does not re-author), and through a round-4 REWRITE of a neighbouring section.
**What happens:** The two rules give opposite answers. R6 (unqualified, so it applies in every round) says "the author merges the later sections into it **in the same round**". D15 and its shipped mirror say the section is FROZEN and enumerate the permitted round-4 edits exhaustively — "the edits permitted at round 4 are **exactly** R2's — appending a row routed this round, repairing the field a routing violation names, inserting a missing preamble, and re-anchoring". A merge is none of those. So either the author merges (breaking FROZEN) or does not (breaking R6), and the reviewers' `routing violation: duplicate section` P0 survives round 4 → `total_p0p1 ≥ 1` per lens that ran the block → red halt on a structural duplicate. Bounded: the next invocation's round 1 can merge under R6, which is why this is P2 and not the P1 its round-3 twin was. Also secondary: R6's renumbering of colliding `D-<n>` ids invalidates any `deferred: D-<n>` line in the round-(N−1) manifest, which the reviewer then marks REOPENED (P0) for a row that is actually fine.
**Why the spec misses it:** D15 was rewritten this round to enumerate the permitted round-4 edits, and R6 was added this round in a different section. The enumeration was built from R2's list and never re-walked against the new rule.
**Suggested fix:** Add R6's merge to the enumeration at spec:48 and spec:74 — "…, re-anchoring, and R6's merge of a duplicate section into the first — none of which is a FROZEN edit or needs promotion" — and add to R6 at spec:103: "the renumbered rows keep their finding records; a manifest line citing a renumbered `D-<n>` is verified against the row's `Finding:` field, not its id."

---

### F-4: The preamble sentence the reviewers are told to look for is not the sentence the spec writes — the backticks around `/ship-spec` break literal containment

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:83 (§ Design 2 preamble) vs spec.md:148 (§ Design 7 block)
**Edge case:** Any conforming implementation — this is not an error path, it is the designed output.
**What happens:** The block requires "the first non-blank content under the heading must be a blockquote **containing the sentence** `/ship-spec must not implement anything in this section`". The preamble the skill actually writes is (raw bytes verified):

```
> Known, unfixed P0/P1 findings. Not part of this spec's implementation: `/ship-spec` must not implement anything in this section. Each row becomes a follow-up ticket filed by the operator.
```

The required sentence has no internal backticks; the produced text code-spans `/ship-spec`. A reviewer applying "contains the sentence" as written does not find it and files `routing violation: missing preamble` — a P0 with **no legal repair**: R2's carve-out permits "inserting a missing preamble", but the preamble is present, so the author either inserts a duplicate (creating a second violation) or strips the backticks, silently changing the fixed preamble Design 2 mandates. That is a red gate on a code-span. A reviewer reading rendered prose accepts it, so the failure is intermittent across lenses and rounds, which is worse than deterministic — one lens files the P0 and the other three do not.
**Why the spec misses it:** My round-3 F-2 asked for a textual key and the spec supplied one; conventions/round-3 F-6 asked in parallel for "check the sentence's substance, not byte-equality" and that half was declined. The key was written by quoting the sentence *out of* the preamble, which dropped the inner code span. Neither checklist row catches it: rows 6 and 8 both grep `must not implement anything in this section`, a substring common to both forms.
**Suggested fix:** Make the key the substring both forms share, in the block at spec:148: "…must be a blockquote whose text contains `must not implement anything in this section` (the surrounding wording and any code spans are free)." That is byte-identical to what checklist rows 6 and 8 already assert, so the producer, the consumer, and the gate agree on one literal.

---

### F-5: `Where` is the key D14 suppression matches on, and it is the one row field no reviewer check ever validates

**Severity:** P2
**Where:** spec.md:47 (D14), spec.md:99 (rule R2 clause (b)), spec.md:148 (block well-formedness rule)
**Edge case:** A later round renames, merges, or removes the spec section a row's `Where` names — the ordinary consequence of a fold, and the case R2(b) was written for.
**What happens:** R2(b) *permits* re-anchoring "an entry in `Where` **or** `Propagation sites`", but nothing requires it and nothing detects the omission: the block's well-formedness rule checks section existence for `Propagation sites` only ("at least one names a section that exists in the spec … every other entry names an existing section, is marked `(new)`, or carries one of those markers"). `Where` is checked for *presence*, never for *resolution*. Meanwhile D14 defines same-root suppression as "the **same spec section in `Where`** and the same defect the row's title and `Suggested fix` describe". So after a rename the row's `Where` names § Design 3 while every regenerated candidate names § Design 3a: the roots no longer match, suppression stops, the deferred P0/P1 comes back as a fresh finding, and the gate goes red for a defect that was deliberately routed away. Nothing tells anyone why — the row is still "well-formed" by every stated test. The follow-up report also renders the row as an open follow-up, so the operator can end up filing a ticket for the same defect that just re-entered the gate. Degrades rather than corrupts (an LLM reviewer may match the renamed section semantically), hence P2 rather than P1.
**Why the spec misses it:** `Propagation sites` got the existence machinery because it carries the two-entry floor that the ceiling depends on. `Where` carries no floor, so it was never given a check — and the fact that it is simultaneously the suppression key was established in a different Decision (D14) from the one that wrote the check (Design 7).
**Suggested fix:** One clause in the block at spec:148, in the well-formedness definition: "…and its `Where` names a section that exists in the spec or carries a `(re-anchored round <n>)` / `(removed round <n>)` marker; a `Where` that resolves to no section is a routing violation, repairable under R2(b)." And one in R2 at spec:99: make the re-anchor obligatory rather than merely permitted — "when a later round renames, merges, or removes the section an entry names, the author **re-anchors it in the same round**".

---

### F-6: Checklist rows 3 and 9 pin long exact literals into the file's hard-wrapped regions — row 5's wrap fix did not generalize

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:160 (row 3), spec.md:166 (row 9), against spec.md:156 (the Test-plan preamble)
**Edge case:** The implementer matches the local wrap style of the region each edit lands in — which the spec's own preamble tells them to expect ("the file is hard-wrapped in places and a phrase can straddle a line break").
**What happens:** Measured line widths in the target regions: 2b prose (`:370-383`) wraps at 68–73 columns; the round-4 half (`:435-445`) wraps at 60–78; the 2e rounds-1–3 bullets (`:428-432`) are unwrapped (229 and 132 chars). So:

- Row 9's `grep -cF 'deferred: D-<n> (§ Deferred — follow-up required)'` ≥ 2 requires that 47-character literal to survive intact inside a 73-column paragraph (Design 4's 2b touch). A wrap anywhere inside it drops the count to 1 and the row fails on a byte-correct implementation.
- Row 9's `grep -cF 'governed by rule R2'` ≥ 1 lands in the ~77-column round-4 half. Same exposure.
- Row 3's `grep -cF '## Deferred — follow-up required'` ≥ 4 counts one hit in the D15 passage, also in the hard-wrapped round-4 half; a wrap there yields 3 and the row fails.

The outcome is the recorded trap this repo has now hit three rounds running (`project_prose_spec_gate_script_pitfalls`, "assert hunk regions not counts"): the implementer chases a phantom regression or hand-edits the checklist, and in the latter case the assertion that was supposed to protect the design is silently gone.
**Why the spec misses it:** Round-3's fix was applied to row 5 specifically ("8 or 9") rather than to the class. Rows 3 and 9 acquired new literals in the same rewrite and were not re-tested against the wrap widths of the regions their text lands in.
**Suggested fix:** Either pin the formatting — one sentence in the Test-plan preamble: "Every literal a checklist row greps must be written on a single unwrapped line in `SKILL.md`, even where the surrounding paragraph wraps" — or make the rows wrap-proof: row 9 → `grep -cF 'deferred: D-' skills/spec-cycle/SKILL.md` ≥ 2 and `grep -cF 'rule R2' skills/spec-cycle/SKILL.md` ≥ 1; row 3 → `grep -cF 'follow-up required' skills/spec-cycle/SKILL.md` ≥ 4. The first option is cheaper and preserves the assertions' precision.

---

### F-7: Out-of-scope 9 leans on R4's incompleteness halt, but a write truncated after `## Out of scope` passes that halt and silently loses every deferral row

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:200 (§ Out of scope item 9), spec.md:101 (rule R4), spec.md:78 (Design 2 — "a spec section at the end of the spec")
**Edge case:** Phase 1 or a 2e revision is interrupted mid-write (crash, kill, tool timeout) after the seven mandated headings are on disk but before or during the deferral section. This is the persistence-atomicity axis for the one new persisted structure this spec introduces, and the spec fences atomic writes explicitly on the strength of R4 covering it.
**What happens:** Out-of-scope 9 states: "R4's incompleteness halt covers the interrupted-write case." It does not, for this section. R4 halts only when the file lacks one of `## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Test command`, `## Done when`, `## Out of scope`. The deferral section sits *after* all of them (Design 2 places it at the end of the spec), so a truncation past `## Out of scope` leaves every required heading intact:

- Truncated **before** the deferral heading → the section vanishes. The next round's render prints `(none)`, the reviewers find no rows, D14 suppression stops applying, and every deferred P0/P1 returns as a fresh finding with no record that it was ever routed. That is § Design 6's named failure mode — "a silently dropped finding" — arriving with no signal at all.
- Truncated **inside** a row → a partial row; the reviewers file `routing violation: D-<n>`, repairable under R2(a). This branch is fine.

The first branch is silent data loss of exactly the records this feature exists to preserve, and the operator's only reminder (the follow-up report) is rendered *from the lost section*, so it reports `(none)` with no distinction from "nothing was deferred".
**Why the spec misses it:** Out-of-scope 9 was written to fence the atomic-write change and reached for R4 as the covering mitigation; R4's list is Phase 1's minimum-section list, which predates this section and does not include it. The two were never walked against a truncation point *after* the last mandated heading.
**Suggested fix:** Two edits, both one clause. (a) Correct spec:200 to say what is actually covered: "R4's incompleteness halt covers an interrupted write that lands before `## Out of scope`; a truncation after it can silently drop `## Deferred — follow-up required` and is not detected." (b) Add the honest reminder to § Design 6's failure-mode bullet at spec:140: "A spec that carried rows in a prior round and renders `(none)` now is the signature of a truncated write, not of an empty section — check `git diff` on the spec before proceeding."

---

### F-8: "rule R2's append" cites a rule that defines no append

**Severity:** P3
**Where:** spec.md:70 (§ Design 1, the 2f-i sentence — text that ships into SKILL.md), spec.md:48 (D15), against spec.md:99 (R2)
**Edge case:** A reader — the round-4 author, or a reviewer verifying a round-4 row — follows the cross-reference.
**What happens:** R2 says "The **only edits the skill makes to an existing row** are (a) … and (b) …". Appending a *new* row is not among them, and R2 never mentions an append; the append is created by Design 1 step 4 ("Defer: add a row to `## Deferred — follow-up required`"). Both spec:70 ("— rule R2's append —") and spec:48 ("the edits permitted at round 4 are exactly R2's — appending a row routed this round …") attribute it to R2. Behaviour is still determinate because both sites enumerate the append inline, so this costs a reader one lookup rather than producing wrong output.
**Suggested fix:** Say where it comes from: at spec:70, "— the Design 1 step 4 append, which R2 does not restrict (R2 governs edits to *existing* rows)"; at spec:48, "the edits permitted at round 4 are the step-4 append (including a row discharging a Settled grill decision) plus R2's row edits — repairing …".

---

### F-9: Design 5's `Scope` sub-parse is ambiguous when the citation itself contains an em dash

**Severity:** P3
**Where:** spec.md:133 (§ Design 5 extraction rule), against spec.md:92 (row shape)
**Edge case:** A `Scope` value whose brief citation carries an em dash — e.g. `out-of-scope — § Out-of-scope item 3 — the follow-ups artifact`. Ordinary, since the brief's own Scope-table rows and Out-of-scope items are written with em dashes.
**What happens:** The rule is "scope is the token before the em dash in `Scope:`" with no "first" qualifier. A render splitting on the last em dash yields the citation fragment in the scope column; the row prints a wrong but plausible value rather than the `?` the spec reserves for unparseable fields, so the operator reads an in-scope/out-of-scope classification that is not there. Degrades gracefully — the row itself is intact and the reviewers read the field directly — hence P3.
**Suggested fix:** One word at spec:133: "scope is the token before the **first** em dash in `Scope:`; if that token is neither `in-scope` nor `out-of-scope`, print `?`."

## Summary
P0: 0 | P1: 2 | P2: 5 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=2 P2=5 P3=2 P4=0
