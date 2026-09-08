# Conventions Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 (P1) | Grill-decision row malformed by construction (two-entry floor) | CLOSED | spec:96 carries the variant sentence verbatim ("`Propagation sites:` lists whatever sites the finding names — one entry is permitted, and `§ (operator decision — routing tests not run)` when none — and `Scope:` is written `operator — round-4 grill`"); the Design 7 block (spec:182) gains "A row whose `Deferred in:` field carries `(grill)` is exempt from the two-entry `Propagation sites` floor and from the ceiling test"; Design 5's token set accepts `operator` (spec:167); D15 permits the append at round 4 (spec:65, :100); recorded at spec:77; rows 6 and 8 grep `(grill)` (spec:197, :199) — baseline verified **0** in `SKILL.md` and in each agent today |
| edge-cases | F-2 (P1) | Step 4 discharges any cited row, folds only the new finding's sites | CLOSED | spec:94 now: discharge only "when the row itself records a P0 with `Scope: in-scope` — R2(c)'s precondition", folds "at the union of this finding's sites and the row's `Propagation sites`", and "If the cited row records anything else, it is not discharged … leave the row live"; block mirror at spec:182 ("only when the row itself records a P0 with `Scope: in-scope` … A cited P1 or out-of-scope row stays live and is not expected to carry the field") |
| correctness | F-1 (P1) | R2(c)'s precondition excludes the rows that can be cited | CLOSED (reworked, opposite direction) | R2(c) stays state-based (spec:127); step 4 (spec:94) and the block's citation sentence (spec:182) now carry the same P0+in-scope precondition, so the three invocations agree with the rule. Verified the no-remedy path is closed: the only `routing violation: D-<n>` the block still files on a cited row requires a P0 + in-scope row, which **is** ceiling-class, so step 0's "for a ceiling-class violation, the R2(c) discharge" (spec:86) names the remedy. Consequence 2 (stale row) is R5's operator-drops-by-hand path (spec:130) |
| correctness | F-2 (P2) | `` `:432` ``/`` `:288-289` `` line-number self-references in shipped text | CLOSED | spec:138 → "the history the 2e 'Do not delete history' bullet protects", justification marked "(Authoring note, not shipped text: … `:432`, which stays byte-identical.)"; spec:129 → "the escape Phase 0's re-run pin already names" + authoring note; row 8 adds ``grep -cE '`:[0-9]+' skills/spec-cycle/SKILL.md`` → 0 (spec:199) — baseline re-verified **0** today |
| correctness | F-3 (P3) | No round-4 title suffix for a deferral | CLOSED | spec:100 "…and a deferral with ` — deferred: D-<n>`"; spec:77 "a rejection, fold, or deferral is recorded as a suffix" |
| correctness | F-4 (P3) | R2's "only edits" stated as exhaustive vs R6 renumbering | CLOSED | spec:127 gains "Rule R6's merge may also renumber a row's `D-<n>` id." |
| correctness | F-5 (P4) | "discharge" carries two senses in `SKILL.md` | CLOSED | spec:77 "R2(c)'s 'discharge' is row-scoped and unrelated to 2f-i step 4's use of the word for a grill decision" |
| edge-cases | F-3 (P2) | Fence rule fixes opening but not closing | CLOSED | Pairing rule added to both copies ("closes one only when it uses the same character as the opener and is at least as long — a shorter or different marker inside an open fence is content"). Verified byte-identity: the two clauses from `runs from its heading to` through `quote fenced text safely.` are **822 chars, exact match**; rows 6/8 grep `same character as the opener` (spec:197, :199), baseline 0 |
| edge-cases | F-4 (P2) | `routing violation:` findings exempt from routing but not the recount | CLOSED | spec:135 head: "The recount does not run on a finding whose title begins `routing violation:`, and a disposition whose only named section is `§ Deferred — follow-up required` is not a recount trigger — a row repair is not a fold. A `fixed: discharged` disposition's fold sections are triggers; a later finding on one of them recounts and resolves by the last bullet" |
| edge-cases | F-5 (P3) | Row severity can never be raised | CLOSED (ledgered, not applied) | spec:250 records it in `## Deferred (P2+)` with the three-site rationale |
| edge-cases | F-6 (P3) | `Discharged:` has no re-anchoring path | CLOSED | R2(b) now reads "an entry in `Where`, `Propagation sites`, or `Discharged:`" (spec:127); block gains "A `Discharged:` entry naming a section that no longer exists is re-anchored under R2(b), not a violation; file a P2 naming the entry if it carries no marker" (spec:182) |
| conventions | F-1 (P2) | Ref-doc / AGENTS.md clause attaches to the wrong conjunct | CLOSED | spec:21 now gives `:81` in full ("P0/P1 block shipping — except that … never enters the gate; P2+ are advisory.") and pins `AGENTS.md:101` to "the same em-dash aside on its 'P0/P1 block shipping' conjunct, before '; P2+ do not.', each on a single line". Verified `AGENTS.md:101` is the severity-scale bullet and `:81` the report-emission item |
| conventions | F-2 (P2) | Extent grammar duplicated into a fifth file with no identity check | CLOSED | Row 6 (spec:197) now extracts "from `runs from its heading to` through `quote fenced text safely.`" from `SKILL.md` and diffs it against `agents/spec-reviewer-correctness.md` ("five copies, one grammar"); Design 7 (spec:180) asserts the clause is "byte-identical, from `runs from` onward, with the one in 2e". Identity independently confirmed above |
| conventions | F-3 (P2) | Ref-doc reconciliation silently omits the round-4 protocol change | **PARTIAL** | spec:21 takes the "state the boundary explicitly" option — "The reference doc is reconciled only where it restates a sentence this spec edits; its summaries of the round-4 protocol (`:86`) and the two console renders (`:88`, `:90-96`) are left to the skill." The boundary is stated, but both anchors it names are wrong and one of them collides with an edit the same cell mandates — filed below as F-1 |
| conventions | F-4 (P3) | Round-3 additions absent from the `### Minor additions` roll-up | CLOSED | spec:77 gains "a row appended for a root a discharged row already carries is suffixed ` (recurrence of D-<m>)` …; the render appends ` [discharged: <value>]` to a discharged row's `Follow-up:` value, which still prints verbatim". Round-4 residue filed below as F-2 |
| conventions | F-5 (P3) | Unscoped `lint.py --strict` departs from VHS-15 without saying why | CLOSED | Row 1 (spec:192) gains "Deliberately unscoped — scoping lint to the five changed paths (VHS-15's form) surfaces `missing-requires` WARNs on the four agent files themselves, which are pre-existing and not this ticket's." |

No REOPENED items. `scale_lens == off`, so no `scalability.md` is in scope for this gate.

**Grounding re-verified this round:** repo unchanged since round 3 (`main` at `124700b`; only the VHS-37/VHS-41 spec artifacts are untracked). All four agent anchors the spec cites are exact — `closure_manifest` at `correctness:18` / `edge-cases:18` / `conventions:20` / `scalability:18`; the status enumeration at `correctness:38-39`, `edge-cases:38-39`, `conventions:43-44`, `scalability:30`; "REOPENED items are P0" at `scalability:40`. Baselines: `grep -c 'Deferred (P2+)' skills/spec-cycle/SKILL.md` = **7** (row 5's stated "7 before" holds); `` grep -cE '`:[0-9]+' `` = 0; `grep -cE 'Design [0-9]|D1[0-7]'` = 0; all of `(grill)`, `same character as the opener`, `must not implement anything in this section`, `**Follow-up:** unfiled`, `— Follow-up: unfiled`, `fixed: discharged`, `governed by rule R2` = **0** today. Wiki `decisions/` re-scanned — no new entry since round 3; `2026-08-09-review-round-artifacts-are-immutable.md` and `2026-08-28-clt-49-deferred-writes-are-revalidated-at-apply-time.md` remain the only overlaps and both stay aligned. `docs/spec-workflow-reference.md:77` (the conventions-lens classification duty D17 cites) verified verbatim.

## Findings

### F-1: The reference-doc reconciliation boundary names the wrong two lines, and one of them is a line the same table cell mandates an edit to
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:21 (Scope row for `docs/spec-workflow-reference.md` / `AGENTS.md`) — this is the PARTIAL residue of round-3 conventions/F-3
**Convention violated:** The spec's own Scope-table discipline (spec:11, "Anchors verified against `main` at `124700b`"), which asserts every anchor in the table is verified, and its own stated reconciliation rule in the same cell.
**Evidence:** Actual line identities in `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\spec-workflow-reference.md`:

```
81: 3. **Each reviewer emits a severity-ranked report** … P0/P1 block shipping; P2+ are advisory.
84: 6. **If still red (rounds 1-3):** … Address every P0 and P1. …
85: 7. **If still red at round 4:** Targeted rewrite — classify each spec section as FROZEN (no unresolved P0/P1) or REWRITE. Build a closed-issues manifest…
86: 8. **If still red after round 4:** Halt. Present remaining P0/P1 and ask the user what to do…
88: **Round 2+ closure tracking:** … CLOSED, PARTIAL, REOPENED, or NEW…
90-96: ### Phase 3 — Drift-check checklist … three bullets
```

Three defects, one sentence:

1. **`:86` is not the round-4 protocol.** The round-4 FROZEN/closed-issues protocol that D15 carves out of is item **7 at `:85`**. `:86` is item 8, the halt render. (My round-3 report mis-cited both lines and the author transcribed them faithfully — the error is mine, but it ships in the spec.)
2. **`:88` is simultaneously edited and excluded.** The same cell says "line 88's paragraph gains `DEFERRED` in the status set and this sentence, verbatim: 'In every round, including round 1, …'" and then "its summaries of … the two console renders (`:88`, `:90-96`) are left to the skill." An implementer reading the cell top-to-bottom gets a direct contradiction about one line. Checklist row 10 (`grep -c 'DEFERRED' docs/spec-workflow-reference.md` ≥ 1 and `grep -cF 'including round 1'` → 1) forces the edit, so the outcome is recoverable — which is why this is P2 and not higher — but the contradiction costs a round if the implementer resolves it the other way. The two console renders are `:86` (item 8, the halt) and `:90-96` (Phase 3).
3. **The stated rule does not actually exclude what it is invoked to exclude.** "Reconciled only where it restates a sentence this spec edits" — `:85` *is* a restatement of `SKILL.md:435-441`, the classification bullet the spec's D15 passage edits (spec:100). So the rule as worded selects `:85` into scope rather than out of it, and the boundary sentence provides no reason for the omission round-3/F-3 was filed about.

**Suggested fix:** Replace the last sentence of the cell with anchors that hold and a rule that does the work:

> The reference doc is reconciled only where it restates a sentence this spec replaces. Its summary of the round-4 protocol (`:85`) is a one-line compression of the classification bullet, not a restatement of a sentence this spec's edits replace, and is left to the skill along with the two console renders (`:86`, `:90-96`).

Row 10 needs no change (the `:88` edit stays mandated and asserted).

### F-2: This round's two behavioral additions did not land in the `### Minor additions` roll-up
**Severity:** P3
**Where:** spec.md:77 (`### Minor additions`), against spec.md:94 and spec.md:135
**Convention violated:** The conventions lens's (c)/(d) classification duty (`docs/spec-workflow-reference.md:77`; `AGENTS.md` § Parallel review agents) and the spec's own declared device at spec:76 — "Recorded so the drift-check can see them." Same class as round-1/F-4, round-2/F-1 and round-3/F-4, all of which were applied.
**Evidence:** The roll-up gained round-3's two items (`(recurrence of D-<m>)`, `[discharged: <value>]`) and this round's grill exemption. Two constructs added **this** round are not there:

- **The cited-row-stays-live branch** (spec:94): "If the cited row records anything else, it is not discharged: fold the finding at its own sites, disposition it `fixed: edited § <a>; § <b>`, and leave the row live." The roll-up records only the positive case ("a row whose severity and scope put it under the ceiling is discharged by folding at every listed site…"). The negative case is the load-bearing half — it is what stops a live P1/out-of-scope row being marked resolved — and it drives a dedicated sentence in the reviewers' block (spec:182, "A cited P1 or out-of-scope row stays live and is not expected to carry the field"). Its rationale lives in `round-3/edge-cases.md` F-2, which the Phase 3 drift-check does not read.
- **The recount exemptions** (spec:135): routing-violation titles and row-repair dispositions are not recount triggers, while a `fixed: discharged` disposition's fold sections are. The roll-up records that "routing's tests do not run inside 2f-i step 4" but nothing about the recount's own exemptions, which are a separate carve-out from brief Decision 4.

Both are (c)-class — correct, rationale exists upstream — so this is drift-check visibility, not substance.
**Suggested fix:** Append to spec:77 in the existing comma-run style: *"…; a row cited by an in-scope-P0 filing that does not itself record an in-scope P0 is not discharged and stays live, the finding folding at its own sites only; the recount skips a `routing violation:` title and a disposition whose only named section is the deferral section, but a `fixed: discharged` disposition's fold sections do trigger it."*

### F-3: The follow-up report's shape line enumerates two scope tokens; its extraction rule accepts three
**Severity:** P4
**Where:** spec.md:157 (§ Design 5 shape) vs spec.md:167 (extraction rule)
**Convention violated:** Internal consistency between a verbatim-inserted render shape and the rule that fills it — the same class the spec polices elsewhere (Design 2's shape vs the well-formedness rule).
**Evidence:** The shape, which ships verbatim into `SKILL.md` at both exits, is `- <D-n>  <lens>/R<n>/F-<k>  <P0|P1>  <in-scope|out-of-scope>  "<title>"  — Follow-up: <value>`. The extraction rule below it now reads "scope is the token before the **first** em dash in `Scope:` (if that token is none of `in-scope`, `out-of-scope`, `operator`, print `?`)". A `(grill)` row's `Scope` is `operator — round-4 grill` (spec:96), so the render prints `operator` in a column the shape says holds one of two values. The rule is authoritative and the render is correct; only the placeholder is stale.
**Suggested fix:** `<in-scope|out-of-scope|operator>` in the shape at spec:157. (Row 8's greps are unaffected.)

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 1

STATUS: GREEN
