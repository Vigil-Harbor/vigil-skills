# Conventions Review — round 3

Grounding: spec re-read fresh from disk (1147 lines), `AGENTS.md` end to end, `docs/portability-contract.md` §4, current `skills/review-pr/SKILL.md` (406 lines — every cited anchor re-verified), wiki `decisions/` (nothing new since `2026-09-07-vhs-36-…`; VHS-29/VHS-18 re-checked), wiki `projects/vigil-skills/{state,filemap}.md`, the brief, all three round-2 reports, and Plane VHS-42.

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | 2b placed after Step 2's short-circuits | CLOSED | § D1 "Order matters": 2b documented after Step 2 but **invoked from inside it** — but see new F-3 on the `:79` half of that sentence |
| correctness | F-2 (P2) | `:174-175` never converted | CLOSED | § D5 first bullet converts it to the paginated streaming form + highest-`id` |
| correctness | F-3 (P2) | "four bare tool names" — there are seven | CLOSED | § Design preamble lists all seven; verified `grep -nE 'Read tool\|Edit tool\|Bash tool\|Write tool'` → `:11 :99 :120 :180 :200 :316 :345`. New variant at F-5 below |
| correctness | F-4 (P2) | Round-2+ all-non-fix cycle has no 6f call site | CLOSED | § D6 "Both exit branches post 6f" (`:233`, `:241`); § D7 amends `:245` |
| correctness | F-5 (P2) | Row 4 unpinned; `:172` unnamed | PARTIAL | Decision 5 now names `:172`/`:290`/`:209` ✓ and row 4 has a pinned number — but the number is wrong (new F-1) |
| correctness | F-6 (P3) | Rows 7/10 already pass unmodified | CLOSED | Test table gained a measured `Pre` column; every Pre value I re-measured is correct (`0,7,3,0,0,1/2,0,1,0,0/1`) |
| correctness | F-7 (P3) | `AGENTS.md:46` is the heading | CLOSED | `:46-48` / `:48` throughout; verified `:46` = `### /review-pr`, `:48` = the paragraph |
| correctness | F-8 (P3) | `(a2)` unguarded when no verdict review | CLOSED | § D1 "If (a) yields no record" paragraph |
| correctness | F-9 (P3) | All-dedup round posts no marker | CLOSED | Decision 2, second consequence bullet |
| edge-cases | F-1 (P1) | Marker advances past unhandled reviews | CLOSED | Decision 12 contiguity rule + invariant + oldest-first bound (2b step 2) |
| edge-cases | F-2 (P1) | Step 2 harvest failure exits "Nothing to review" | CLOSED | Decision 14 bullet "blocks every affirmative early exit" (`:81`, `:381`) |
| edge-cases | F-3 (P1) | One blockquote depth per body | CLOSED | 2b step 6 "Normalize PER SECTION, not per body" with both verified specimens |
| edge-cases | F-4 (P1) | `\| wc -l` swallows exit status | CLOSED | Decision 7 "Never pipe a fetch straight into an aggregate" + required shape block; test row 14 |
| edge-cases | F-5 (P2) | Resume/guard trust any author | CLOSED | Decision 12 "Author filter is load-bearing"; `$self` in 2b step 1 and 6f; test row 13 |
| edge-cases | F-6 (P2) | 6f sites miss all-non-fix incremental round | CLOSED | § D6 `:241` branch; § D7's generalized `:245` |
| edge-cases | F-7 (P2) | Test plan verifies happy parse only | CLOSED | Rows 19 (zero-item + no tripwire), 21 (code-mask synthetic), 22 (both-sections), 23 (failure path) |
| edge-cases | F-8 (P2) | Masked vs raw text into triage unstated | CLOSED | 2b step 6 "The masked text computes boundaries only"; spans sliced from raw |
| edge-cases | F-9 (P2) | Bodies bounded by count, not size | CLOSED | 2b step 3 fetch-to-file + slice-read + size report |
| edge-cases | F-10 (P3) | 20-item bound leaves outside-diff unbounded | CLOSED | 2b step 11 hard ceiling of 50; "grouped (not individually triaged)" naming |
| edge-cases | F-11 (P3) | Phrase tripwire per-phrase vs per-body | CLOSED | Decision 11 "evaluated per phrase, on masked text" |
| conventions | F-1 (P2) | Decision 5 exclusion list incomplete (`:172`) | CLOSED | Decision 5 § "Named exclusions" — `:172`, `:290`, `:209`, plus `-X POST` and single-resource reads. Verified `grep -n 'gh api'` returns exactly those nine sites |
| conventions | F-2 (P2) | Three grep rows cannot fail | PARTIAL | `Pre` column added and rows repinned ✓ — but row 4's `9` and row 8's `4` are both arithmetically wrong (new F-1, F-2), and the preamble's "every row must be able to fail" is now falsified by rows 12/14/16 (new F-4) |
| conventions | F-3 (P2) | Design preamble undercounts bare tool names | CLOSED | All seven anchors listed, with `:180`/`:200`/`:316`/`:345` called out as inside D5/D8 edit regions. New variant (`:99` inside D3's) at F-5 |
| conventions | F-4 (P2) | Deferred departs from convention | CLOSED | § Deferred opens with the filed-vs-recorded rule; VHS-42 carries ID + date + state; accounting bullet removed. **Ticket verified live in Plane** (`07ba5525…`, created 2026-09-08, `state_group: backlog`) |
| conventions | F-5 (P3) | D3 rewrites the inline severity rule | CLOSED | § D3 bullet 1 "This is a spec-level widening beyond the brief" |
| conventions | F-6 (P3) | `AGENTS.md:7` known-false claim deferred | CLOSED | § D10 `:7` strike; § Scope row; test row 15 (Pre `0`,`1` verified) |
| conventions | F-7 (P3) | Decision 13 doesn't engage VHS-29's fence-masking rejection | CLOSED | Decision 13 § "On VHS-29's rejection of fence-masking" |
| conventions | F-8 (P4) | `AGENTS.md:46` is the heading | CLOSED | `:46-48` / `:48` cited in § Scope and § D10 |

No REOPENED items. 26 of 28 CLOSED; 2 PARTIAL, both on the same test-plan row-quality axis, carried below.

## Findings

### F-1: Test row 4's pinned count is `9`; the design produces `10` — Step 2 fetch `(b)` is missing from the enumeration
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 4; § Design D1
**Convention violated:** the spec's own stated gate shape ("every row is a command whose expected output is pinned"), and the repo's recorded prose-spec gate lesson (a pinned number must be derived from the design, not estimated)
**Evidence:** row 4 expects `grep -c 'gh api --paginate repos'` → `9` = "the six converted list fetches (`:68`, `:75`, `:174`, `:194`, `:224`, `:341`) plus the 2b resume query, 6a's body query, and the 6f guard". But § D1 states "The two fetches become four" and its code block shows **three** paginated Step-2 fetches: `(a)` (converted `:68`), `(b)` (**new** body-harvest reviews query), `(c)` (converted `:75`). `(b)` is a fourth new paginated fetch and is counted nowhere. Six converted + four new (`(b)`, 2b resume, 6a body, 6f guard) = **10**. `(b)` cannot be folded into `(a)` — D1 says explicitly "Do not unify with (a)". Pre value `0` re-measured and correct.
**Suggested fix:** change row 4's expected to `10` and add "Step 2 fetch `(b)`, the body-harvest reviews query" to the enumeration.

### F-2: Test row 8's pinned count is `4`; its own enumeration lists `:341` twice
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan row 8
**Convention violated:** same as F-1 — a pinned expectation that does not follow from the design; plus `AGENTS.md` § Plan & Spec Reviews `file:line` precision
**Evidence:** row 8 expects `grep -cF '| select(.state != "COMMENTED") | {'` → `4` — "the streaming verdict form at `:69`, `:175`, `:341`, and D8's Phase 2 read". **`:341` *is* D8's Phase 2 read** — § D8 bullet 1 reads "6d Phase 2's verdict fetch (`:341-342`)". Only three sites take the converted `… | {` shape: § D1 `(a)` (`:69`), § D5's `:174-175` conversion, § D8's `:341-342` conversion. Expected should be `3`. (Round-2 conventions F-2's suggested fix named `3` for exactly this row.) The row's own justification note is otherwise correct: I re-measured the bare phrase at **6** pre-change (`:65`, `:69`, `:175`, `:339`, `:342`, `:404`), so pinning on the converted shape is the right call.
**Suggested fix:** change row 8's expected to `3` and drop the duplicated "and D8's Phase 2 read" clause (or replace it with "(= D8's Phase 2 read)" appended to `:341`).

### F-3: D1 says 2b is invoked "before `:79`", contradicting its own order line and its `:79` paragraph
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design D1, "Order matters" paragraph
**Convention violated:** internal consistency of a load-bearing ordering claim; `AGENTS.md` § Plan & Spec Reviews (`file:line` precision)
**Evidence:** three statements in the same subsection disagree on where `:79` sits:
- "…is **invoked from inside Step 2**, before `:79`/`:81`/`:83`"
- "**Order matters.** (a) → (a2) → infra-error check → (b) → **2b harvest** → (c) → then Step 2's short-circuit block." — the infra-error check *is* `:79`, and it precedes the harvest
- "The infrastructure-error check at `:79` runs on (a2)'s body and short-circuits **before the harvest**, so an errored review never reaches the parse."

Verified against the file: `:79` is the infra-error sentence, `:81` the `APPROVED` short-circuit, `:83` the no-reviews line. The intended reading is unambiguous from the latter two statements, but an implementer following the first would place the harvest ahead of the infra-error short-circuit, letting an errored review body reach the parse — the exact case the third statement exists to prevent.
**Suggested fix:** change the first sentence to "…invoked from inside Step 2, after `:79`'s infrastructure-error check and before `:81`/`:83`".

### F-4: The test plan's "every row must be able to fail against the unmodified file" is falsified by four of its own rows
**Severity:** P3
**Where:** spec § Test plan opening paragraph vs rows 3, 12, 14, 16
**Convention violated:** the prose-spec gate shape the spec attributes to VHS-32/33/36, stated as an absolute the table does not meet
**Evidence:** the preamble says "every row is a command whose expected output is pinned, and every row must be able to *fail* against the unmodified file." Rows 12 (`body-dispositions:no-push` → no match / no match), 14 (`--paginate … | wc -l` → `0` / `0`) and 16 (pytest baseline → "unchanged") are all `pre == post` by design — they are negative guards against a *wrong implementation*, not discriminators against `main`. Row 3 has no Pre at all. The grep-table's own intro already anticipates this ("a row that cannot discriminate is visible as `pre == post`"), so the absolute in the preamble is the only thing out of step.
**Suggested fix:** soften the preamble to "every *positive* row must be able to fail against the unmodified file; rows whose Pre equals their Expected are negative guards against a wrong implementation and are marked as such" — and mark rows 12, 14, 16 accordingly.

### F-5: The bare-tool-name fence names `:180`/`:200`/`:316`/`:345` as inside edit regions but misses `:99`, which sits inside D3's
**Severity:** P3
**Where:** spec § Design preamble; § D3 fourth bullet
**Convention violated:** `docs/portability-contract.md` §4 case 1 (the rule the preamble invokes), applied unevenly across the spec's own edit regions
**Evidence:** `skills/review-pr/SKILL.md:99` reads `2. **Read** the actual file at the referenced line using the Read tool` and lives inside Step 3's per-finding loop (`:96-107`). § D3 explicitly amends that loop and paraphrases the same sub-step in capability language — "Sub-steps 2 (read the file at the referenced line), 3 (verify against current code) and 4 (categorize) are otherwise identical". The preamble's fence names only D5's (`:180`, `:200`) and D8's (`:316`, `:345`) as falling inside edit regions, so `:99` — the one an implementer is most likely to normalize while rewriting D3's bullet — is unmarked.
**Suggested fix:** add `:99` to the "inside an edit region" list in the Design preamble ("`:99` inside D3's"), and add "the sub-step's existing wording at `:99` is carried through unchanged" to D3's per-finding-loop bullet.

### F-6: VHS-42's ticket body claims the `AGENTS.md:7` fix for itself; the spec now folds it into D10
**Severity:** P3
**Where:** spec § Deferred; Plane VHS-42 (`07ba5525-bd27-4dac-863f-b6335d7f484a`)
**Convention violated:** the repo's audit-trail discipline that a filed ticket and the spec that filed it must not contradict each other (wiki `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`)
**Evidence:** VHS-42's description closes with "RELATED — `AGENTS.md:7` still claims the repo has no test suite; five pytest modules exist. Same doc-hygiene sweep, worth folding in here." The spec's § Deferred now says the opposite: "The `AGENTS.md:7` 'no test suite' correction is folded into D10 **here** rather than into VHS-42, since this diff already opens that file." Whoever picks up VHS-42 after VHS-41 merges will look for an edit that is already made.
**Suggested fix:** add one clause to § Deferred — "(VHS-42's RELATED paragraph still claims this edit; trim it from the ticket when this spec ships)" — so `/ship-spec`'s Plane step has the instruction, rather than leaving the ticket to age with a stale scope note.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 3 | P4: 0

STATUS: GREEN
