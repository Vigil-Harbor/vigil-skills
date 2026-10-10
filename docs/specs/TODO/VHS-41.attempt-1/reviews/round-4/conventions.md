# Conventions Review — round 4

## Grounding

Spec re-read fresh from disk (1383 lines), `AGENTS.md` end to end, global + project `CLAUDE.md`, `docs/portability-contract.md` §4/§5, current `skills/review-pr/SKILL.md` (406 lines, every cited anchor re-verified), `skills/ship-spec/SKILL.md` Phase 6, wiki `decisions/` (nothing new since `2026-09-07-vhs-36-…`), wiki `projects/vigil-skills/state.md` + `log.md`, the brief, and all three round-3 reports. Every `Pre` value in the rewritten test plan re-measured against the working tree — all 13 match (row 4 `0`, row 5 `7`, row 6 `3`, row 7 `0`, row 8 `0`, row 9 `1`/`2`, row 10 `0`, row 11 `1`, row 12 no match, row 13 `0`, row 14 `0`, row 15 `0`/`1`), and `grep -n 'gh api'` returns exactly the nine call sites Decision 5 accounts for.

**Round-4 protocol.** The spec is untracked (`?? docs/specs/TODO/VHS-41.spec.md`) and `round-4/` is empty, so no byte-diff against the round-3 text is possible. I verified the freeze by matching every verbatim quotation the three round-3 reports made of FROZEN text against the current file — Design preamble (seven anchors, the "only D5's/D8's" clause), Decision 8's four verified review ids, Decision 7's `--slurp`/`gh 2.87.3`/required-shape block, Decisions 3/4/6/9/10/13, D3's "spec-level widening", D4's three bullets, D8's `:341-342` conversion and 6e block, D10, Test command, Done when, Out of scope. All match, and their line offsets shift uniformly with the growth of the REWRITE sections above them. **No FROZEN section was silently changed, and no REWRITE section rewrites FROZEN text.** Two places where the freeze left a visible seam are F-5 below.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | `gh api --jq --arg` is not a valid invocation | CLOSED | § D2 step 1 `:608`, § D7 `:977` — `export SELF=$(gh api user --jq .login)` + `select(.user.login == env.SELF)`; row 13 repinned on `env.SELF`. Residual on the assignment shape → new F-3 |
| correctness | F-2 (P1) | Rows 4/8 pin counts a correct impl can't produce | CLOSED | Row 4 `≥ 10` with all eleven sites enumerated; row 8 `≥ 3` with `:341` named once; Decision 5 `:146-149` carries the identical eleven-site list |
| correctness | F-3 (P1) | Bounded parse-to-zero round posts no marker → no progress | CLOSED | Decision 2 consequence 1 `:88-95`; Decision 12 "Progress does not depend on findings" `:388-394`; D7 post condition `:959-964` + findings-free body `:1024-1033` |
| correctness | F-4 (P1) | `verdict-landed` read off the body-carrying stream | CLOSED | § D5 third query `:876-882` (verdict filter) and the rule at `:891-902` reading the test off that stream |
| correctness | F-5 (P2) | D1 says 2b runs "before `:79`" | CLOSED | § D1 `:560-566` — "after the `:79` check and before `:81`/`:83`", order line now names `:79` explicitly |
| correctness | F-6 (P2) | Phrase tripwire reads an artifact D2 stopped producing | CLOSED | Decision 11 defines the **phrase-scan view** `:314-325`; D2 step 6 computes it `:711-715` |
| correctness | F-7 (P2) | Steps 6/7 circular | CLOSED | D2 step 5 provisional span `:663-670` |
| correctness | F-8 (P2) | Row 8 `-F` escaping / row 14 `[^\n]` | CLOSED | Checklist moved into a fenced block `:1234-1249` with unescaped pipes; row 14 → `\| *(wc\|jq)`; re-measured `0` |
| correctness | F-9 (P3) | Undefined `R` → markerless comment | CLOSED | `r0` sentinel, Decision 12 `:356-361`, D7 `:988-993` |
| edge-cases | F-1 (P1) | Later round's marker leapfrogs an earlier gap | CLOSED | `HARVEST_FLOOR` run-scoped, Decision 12 `:344-355`, `:375-381` |
| edge-cases | F-2 (P1) | `--arg` | CLOSED | as correctness F-1 |
| edge-cases | F-3 (P1) | Step 6/7 circularity | CLOSED | as correctness F-7 |
| edge-cases | F-4 (P1) | Phrase tripwire input | CLOSED | as correctness F-6 |
| edge-cases | F-5 (P1) | `LAST_BODY_REVIEW_ID` never seeded after Step 2 | CLOSED | Decision 2 `:77-83`; § D1 "Seed the body high-water mark here" `:589-592`; D5 counts **post-dedup** `:885-888` |
| edge-cases | F-6 (P1) | Structural matching on raw text | CLOSED | D2 step 6 "Masked for matching, raw for content" `:698-709`; step 9 restates `:747-750` |
| edge-cases | F-7 (P1) | Rows 4/8 miscounted + unrunnable | CLOSED | as correctness F-2 / F-8 |
| edge-cases | F-8 (P2) | Step 2 `(a)`/`(c)` ungoverned; `:83` outside the block | CLOSED | Decision 14 first bullet generalized to "every `--paginate` fetch this design introduces or converts" `:471-482`, all **three** Step 2 exits named `:499-509` |
| edge-cases | F-9 (P2) | Empty `SELF` | CLOSED | Decision 14 `:483-488` |
| edge-cases | F-10 (P2) | Marker literal in a harvested title | CLOSED | Decision 12 position + neutralization `:412-423`; D7 `:995-998` |
| edge-cases | F-11 (P2) | Markerless comment unguarded | CLOSED | `r0` sentinel + guard `:398-403` |
| edge-cases | F-12 (P2) | Body-size threshold unstated | CLOSED | D2 step 3 — **64 KB** `:640-645`. 6e template seam → new F-5 |
| conventions | F-1 (P2) | Row 4 pinned 9, design produces 10 | CLOSED | Row 4 `≥ 10`, eleven sites enumerated incl. Step 2 fetch (b) |
| conventions | F-2 (P2) | Row 8 pinned 4, `:341` counted twice | CLOSED | Row 8 `≥ 3`, `:341` named once, command unescaped; re-measured bare phrase `6` / converted shape `0` pre-change, matching the row's own note |
| conventions | F-3 (P2) | D1 "before `:79`" | CLOSED | as correctness F-5 |
| conventions | F-4 (P3) | "every row must be able to fail" falsified | CLOSED | Preamble `:1216-1219` splits positive rows from `[guard]`; rows 12/14/16 marked. Re-checked: no other row has `Pre == Expected` |
| conventions | F-5 (P3) | Bare-tool-name fence misses `:99` inside D3's region | **OPEN (not fixed)** | Design preamble `:521-525` still names only `:180`/`:200`/`:316`/`:345` as inside edit regions. Deliberate — preamble and D3 are FROZEN. Re-raised at original severity → F-7 |
| conventions | F-6 (P3) | VHS-42's RELATED paragraph contradicts the spec | **PARTIAL** | § Deferred `:1379-1382` now carries the instruction — but it routes it to a `/ship-spec` step that has no such capability → new F-1 |

No REOPENED items. 24 of 26 CLOSED; 1 PARTIAL, 1 deliberately OPEN under the freeze.

## Findings

### F-1: § Deferred routes the VHS-42 description edit to `/ship-spec`'s Plane step, which cannot edit a ticket description
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:1379-1382 (§ Deferred)
**Convention violated:** prior art — `/ship-spec` Phase 6's documented capability surface (`skills/ship-spec/SKILL.md:217-229`, `:265`); the audit-trail rule that a filed ticket and the spec that filed it must not contradict each other (wiki `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`)
**Evidence:** the spec says "**and VHS-42's own `RELATED` paragraph still claims that edit, so `/ship-spec`'s Plane step must trim it from the ticket when this spec ships**". `/ship-spec` Phase 6 does exactly three things: re-check reachability (`:219`), flip the ticket to the review state via the work-item **state-update** capability (`:228`), and post a `PR opened: <pr-url>` **comment** (`:229`). Its declared dependency list (`:265`) is "project listing, work-item state update, work-item comment" — no description write. There is no step that reads or rewrites a description, so the instruction is inert and VHS-42 keeps a scope note claiming an edit VHS-41 already made. (This is the residual of my own round-3 F-6 suggested wording, which named that step without checking it.) Related constraint the fix must respect: per the operator's recorded practice, plane-proxy escapes HTML, so a description rewrite must be sent as plain text.
**Suggested fix:** reword the clause to name an actor that exists — e.g. "…so **when this spec ships, edit VHS-42's description** (plane-proxy work-item update capability, plain text) to drop the RELATED paragraph; `/ship-spec` Phase 6 does not touch descriptions, so this is an explicit operator step." Alternatively drop the instruction and post it as a VHS-42 comment instead, which `/ship-spec` *can* do.

### F-2: `$TMPDIR` is used as the scratch location with no definition, fallback, or repo precedent
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:216, :555, :634, :867, :869 (Decision 7 required shape, D1 `(c)`, D2 step 3, D5 poll) vs spec.md:1000-1005 (D7)
**Convention violated:** `docs/portability-contract.md` §5 behavioral parity / the repo's harness-neutral discipline; no established `$TMPDIR` idiom exists anywhere in `skills/` (grep: the only shell-prose scratch reference is `skills/hermes-kanban-awareness/SKILL.md:146` "session scratchpad"; the four Python scripts all use `tempfile.mkstemp`)
**Evidence:** D7 states the location as a capability — "written to the **system temp directory (or the harness scratch directory), never inside the worktree**" — but D2 step 3 and D5 hardcode the variable: `> "$TMPDIR/body-<REVIEW_ID>.md"`, `> "$TMPDIR/new_inline"`. `TMPDIR` is not set by bash and is not guaranteed by POSIX; it happens to be set (`/tmp`) in this machine's Git Bash, which is why round 3 recorded it as resolving "here". Where it is unset the redirect target becomes `/body-<id>.md` — a write to the filesystem root, which fails, and under Decision 14 every such failure is a body-harvest failure that forces `inconclusive` and blocks `:81`/`:83`/`:381`. The failure is silent-looking: the skill reports a harvest failure, not a bad path.
**Suggested fix:** define the location once, in D7, and have D2/D5 name it rather than the raw variable — e.g. "`SCRATCH="${TMPDIR:-/tmp}"` resolved once at Step 2 (or the harness scratch directory); every file below is written under `$SCRATCH`, never in the worktree" — then use `"$SCRATCH/..."` in D1 `(c)`, D2 step 3, D5, and Decision 7's required-shape block.

### F-3: `export SELF=$(gh api user --jq .login)` masks the fetch's exit status — the antipattern Decision 7 exists to forbid
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:608 (D2 step 1), spec.md:977 (D7 guard)
**Convention violated:** the spec's own Decision 7 rule ("Never pipe a fetch straight into an aggregate … the shell reports the *last* command's status") and Decision 14's requirement that `gh api user` be treated as a harvest fetch; ShellCheck SC2155, the standard statement of this rule
**Evidence:** Decision 14 says "**`gh api user` is a harvest fetch too** … A non-zero exit *or an empty `SELF`* is a failure" (spec.md:483-488), and D2 step 1's own comment repeats it: `# empty or non-zero => harvest failure (Decision 14)`. But in `export SELF=$(cmd)` the exit status observed by `$?` is `export`'s (always `0`), not the command substitution's — the substitution's status only propagates through a *plain* assignment. So the "non-zero exit" half of the check cannot be performed as written. This is the same class of masked-status defect Decision 7 spends a paragraph on and test row 14 guards mechanically; the spec reintroduces it in the two commands Decision 14 singles out. Practical blast radius is contained because the empty-`SELF` half still fires (a failed `gh api` prints nothing on stdout), so the rule degrades rather than breaks — hence P2, not P1.
**Suggested fix:** split the assignment at both sites: `SELF=$(gh api user --jq .login); rc=$?; export SELF` — with `rc != 0` **or** an empty/`null` `SELF` classified as a harvest failure per Decision 14. `export` is still needed (gojq's `env.SELF` reads the process environment), so only the ordering changes.

### F-4: Decision 2 is still tagged *(carried from brief)* although its body is now mostly spec-authored resume machinery
**Severity:** P3
**Where:** spec.md:53 (heading), :56-103 (body)
**Convention violated:** the spec's own decision-labeling convention — *(carried from brief)* vs *(spec-author)* — which is what the post-round-4 human drift-check reads to decide what to scrutinize
**Evidence:** the brief's Decision 2 is one sentence: "in Step 2 and in each 6a/6b cycle, the body of every verdict review newer than the last one handled is read, and 6a's new-findings detection counts body items." The spec's Decision 2 now carries `PRIOR_DISPOSITIONED_REVIEW_ID`, the on-PR `<!-- review-pr:body-dispositions:r<id> -->` marker as the durable cross-run record, the seed-and-advance rule for `LAST_BODY_REVIEW_ID`, and three named consequences including the findings-free-comment rule — none of which the brief or the Plane ticket authorizes. This is a category (c) addition, not (d): the rationale is explicit and in-body ("*How this resolves the round-1 objection…*", spec.md:69-75). But the heading tag still reads (a), which is the one signal the drift-check uses. Decisions 11/12/14 are correctly tagged *(spec-author)*; Decision 5's additions are pure enumeration of a brief rule and its tag is fine.
**Suggested fix:** retag the heading — `### Decision 2 — every body-carrying review newer than the last dispositioned one is read *(carried from brief; the cross-run resume marker is spec-author)*` — so the drift-check sees a decision to review rather than a brief clause to skim.

### F-5: Two FROZEN sections still describe behavior their REWRITE counterparts extended this round
**Severity:** P3
**Where:** spec.md:105-107 (Decision 3, FROZEN) vs spec.md:959-964 (D7); spec.md:1077-1084 (D8's 6e template, FROZEN) vs spec.md:640-645 (D2 step 3)
**Convention violated:** internal consistency between the Decisions layer and the Design layer — the spec's stated structure, where each Decision's *Honored by* line points at the design section that implements it in full
**Evidence:** these are the two visible seams of the round-4 freeze, and both are freeze artifacts rather than protocol violations (neither REWRITE section altered FROZEN text):
1. Decision 3 states the post condition as "Each round that triaged at least one body-level finding posts exactly one PR-level comment listing every body-level item with its fix SHA or skip reason." D7's post condition is now two-armed — that case **or** "when `R` would advance past `PRIOR_MARK` and a `HARVEST_FLOOR` exists", with a findings-free body (spec.md:1024-1033). Decision 3 does not forbid the second arm, so there is no contradiction, but a reader who takes Decision 3 as the canonical statement gets an incomplete rule.
2. D2 step 3 requires the 64 KB line to "emit that line in 6e alongside the other bound lines", closing edge-cases r3-F-12. D8's 6e report block lists `Body harvest bounded` and `Body items grouped` but has **no size row** — exactly the gap r3-F-12 named ("the 6e block … has no size row today").
**Suggested fix:** at post-green polish, add one clause to Decision 3 ("…plus, per Decision 12, a findings-free comment on a round that must record forward progress") and one line to D8's 6e block (`- Body harvest size: none / review <id> body <n> KB — parsed in slices`).

### F-6: Review-round archaeology has no stated spec-only fence, and no shipped skill carries any
**Severity:** P3
**Where:** spec.md — 102 occurrences of `r<n>-F-<n>` / "the v1|v2|v3 draft"; concentrated in REWRITE prose that describes what the skill text should say (e.g. :564-566, :644-645, :667-668, :705-709)
**Convention violated:** repo practice — `grep -rn 'r[0-9]-F-[0-9]' skills/` returns **zero** hits across all eleven shipped skills; VHS-32/33/36 all carried heavy review-citation density in their specs and none of it reached `SKILL.md`
**Evidence:** the spec is explicit about some prose that *does* ship ("**Worked specimens** (kept in the skill so a future editor can re-verify without a live PR)", spec.md:780; "The skill states that limitation next to them", :794), and about the tripwire wording. It never states the complement — that lens citations and "the v3 draft said X" asides are spec-internal and never ship. Sentences like "The v3 draft's 'before `:79`/`:81`/`:83`' contradicted this paragraph's own order line" (spec.md:564) sit inside the paragraph describing the ordering rule the skill must state, so the boundary is inferable but not stated. Low probability, cheap to close, and a mechanical guard is available in a section that is already REWRITE.
**Suggested fix:** add a guard row to the checklist — `17 grep -cE 'r[0-9]-F-[0-9]|v[0-9] draft' $S` → `[guard]` `0`, Pre `0` — and one sentence in the test-plan preamble or § Deferred: "lens citations and draft-history asides are spec-internal; none of them ships into `SKILL.md`."

### F-7: The bare-tool-name fence still omits `:99`, which sits inside D3's edit region *(carried from r3-F-5, deliberately unfixed)*
**Severity:** P3
**Where:** spec.md:521-525 (Design preamble, FROZEN); spec.md:823-826 (D3's per-finding-loop bullet, FROZEN)
**Convention violated:** `docs/portability-contract.md` §4 case 1 (the rule the preamble invokes), applied unevenly across the spec's own edit regions
**Evidence:** `skills/review-pr/SKILL.md:99` reads `2. **Read** the actual file at the referenced line using the Read tool`, inside Step 3's per-finding loop (`:96-107`) — which D3 amends and paraphrases in capability language ("Sub-steps 2 (read the file at the referenced line), 3 … and 4 … are otherwise identical"). The preamble names `:180`/`:200` as inside D5's region and `:316`/`:345` as inside D8's, but not `:99` as inside D3's, so the one anchor an implementer is most likely to normalize while rewriting that bullet is unmarked. Both sections are FROZEN this round, so the omission is a deliberate non-fix per the closure manifest, correctly handled. Re-raised at its original severity so it does not drop off the ledger before ship.
**Suggested fix:** at post-green polish (or in `/ship-spec`'s implementation note), extend the preamble list to "including `:99` inside D3's edit region, `:180`/`:200` inside D5's and `:316`/`:345` inside D8's", and add "the sub-step's existing wording at `:99` is carried through unchanged" to D3's per-finding-loop bullet.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 4 | P4: 0

STATUS: GREEN
