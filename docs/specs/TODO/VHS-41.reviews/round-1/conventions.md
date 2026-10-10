# Conventions Review — round 1 *(attempt 2)*

Grounding: spec re-read fresh from disk (1476 lines); `AGENTS.md` end to end; global + project `CLAUDE.md`; `docs/portability-contract.md` §1–§5; current `skills/review-pr/SKILL.md` (406 lines, every cited anchor re-verified); `skills/ship-spec/SKILL.md` Phase 6 + Tool-use notes; wiki `projects/vigil-skills/state.md` + `filemap.md`; wiki `decisions/` (nothing new since `2026-09-07-vhs-36-…`); `docs/specs/DONE/VHS-32|33|36/spec.md` test plans; the brief; and attempt-1 `round-4/conventions.md`. Every `Pre` value in the test plan re-measured against the working tree — **all 16 match** (rows 4 `0`, 5 `7`, 6 `3`, 7 `0`, 8 `0`, 9 `1`/`2`, 10 `0`, 11 `1`, 12 no match, 13 `0`, 14 `0`, 15 `0`/`1`, 24 `0`, 25 `0`, 26 `0`/`0`). Rows 1–2 executed: `0 error(s), 1 warning(s)` and `0 error(s), 2 warning(s)` (`review-pr`, `ship-spec`) — both gate rows are sound. `grep -nE '\b(Read|Edit|Write|Bash|Grep) tool'` returns exactly the seven anchors the Design preamble names (`:11`, `:99`, `:120`, `:180`, `:200`, `:316`, `:345`).

## Closure of attempt-1 round-4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | `r0` sentinel makes the 6f guard a constant key | CLOSED | Marker is `r<R>:h<HEX>`; digest defined spec.md:356-362, guard keyed on both spec.md:419-433, D7 spec.md:1030-1064, edge case spec.md:1263-1270, row 25 |
| edge-cases | F-1 (P1) | `; rc=$?` prints nothing | CLOSED | Stdout token protocol spec.md:215-231; `rc=$?` on its own line + `if…echo` at D1 (c) spec.md:589-590 and D5 spec.md:914-915; D9 bullet spec.md:1237-1242; row 24 |
| edge-cases | F-2 (P1) | `export SELF` / `env.SELF` null across Bash calls | CLOSED | Literal `"<SELF>"` substitution, D2 step 1 spec.md:638-653, D7 guard spec.md:1022-1040, Decision 14 spec.md:517-521; rows 13 (positive) and 26 (guard). Also closes attempt-1 conventions r4-F-3 (`export SELF=$(…)` masking `$?`) — the assignment is gone |
| edge-cases | F-3 (P1) | `r0` constant key suppresses a later round's dispositions | CLOSED | Digest + 6e naming, spec.md:376-382, 419-433, D8 spec.md:1149, 1159-1162 |
| edge-cases | F-4 (P1) | D6's advance rule states two incompatible values | **PARTIAL** | D6 spec.md:967-973 now states the contiguous-prefix rule with a worked value — but Decision 2 (spec.md:78-80) and D1 (spec.md:624-627) still state the superseded "highest successfully parsed" rule while citing D6 → **F-1 below** |
| conventions | F-1 (P2) | § Deferred routes VHS-42 edit to `/ship-spec`'s Plane step | **REOPENED / unfixed** | spec.md:1472-1475 unchanged → F-4 below |
| conventions | F-2 (P2) | `$TMPDIR` used with no definition or fallback | **REOPENED / unfixed** | spec.md:216-218, 588, 678, 913 vs D7 spec.md:1071-1073 → F-3 below |
| conventions | F-3 (P2) | `export SELF=$(…)` masks the fetch exit status | CLOSED | as edge-cases F-2 above |
| conventions | F-4 (P3) | Decision 2 still tagged *(carried from brief)* | **OPEN** | spec.md:53 unchanged → F-7 below |
| conventions | F-5 (P3) | Decision 3 / D8 6e-block freeze seams | **OPEN** | spec.md:105-108 still single-armed; D8's 6e block spec.md:1148-1155 still has no size row → F-6 below |
| conventions | F-6 (P3) | No stated spec-only fence for review archaeology | **OPEN** | no such sentence and no guard row added → F-9 below |
| conventions | F-7 (P3) | Bare-tool fence omits `:99` inside D3's region | **OPEN** | spec.md:553-558 still lists only `:180`/`:200`/`:316`/`:345` as in-region → F-8 below |

4 of 5 manifest P1s CLOSED, 1 PARTIAL. The four conventions items that were deliberately unfixed under attempt-1's round-4 freeze are re-raised at original severity — the freeze no longer applies.

## Findings

### F-1: Decision 2 and D1 still state the superseded advance rule that D6 replaced
**Severity:** P1
**Where:** spec.md:78-80 (§ Decision 2), spec.md:624-627 (§ D1) vs spec.md:967-973 (§ D6)
**Convention violated:** PARTIAL closure of edge-cases r4-F-4 (P1) — per the closure protocol a PARTIAL keeps its original severity; and the spec's own structure, where a Decision's *Honored by* line points at the design section that states the rule in full
**Evidence:** D6 states the fixed rule and explicitly rejects the old one: *"set `LAST_BODY_REVIEW_ID` to the highest id of the **contiguous successfully-parsed prefix** … For `[100 ok, 200 fetch-failed, 300 ok]` the mark is `100`, not `300`."* But Decision 2 says *"set it to the highest id whose body was fetched and parsed successfully in that harvest (D6's rule)"* and D1 repeats it verbatim — *"…the highest id whose body was fetched and parsed successfully in this harvest — the same rule D6 applies in 6b."* On the same input those two sentences yield `300`, the value D6 names as wrong. Both cite D6 as their authority, so the contradiction is invisible to a reader who trusts the citation. Blast radius is not theoretical: D1 governs **Step 2's** harvest, which is the largest (up to 10 reviews per 2b step 2) and therefore the likeliest place for a mid-set fetch failure — and an implementer who follows D1 advances the mark past the failed review, so 6a never re-returns it and the gap becomes permanent within the run. `grep -n 'LAST_BODY_REVIEW_ID'` shows exactly these three definitional sites; there is no fourth.
**Suggested fix:** replace both sentences with the D6 formulation rather than a paraphrase — Decision 2: *"…set it to the highest id of the contiguous successfully-parsed prefix of that harvest — the highest successfully parsed id strictly below the harvest's lowest failed or deferred id (D6's rule); leave it unchanged if the lowest id failed."* and the same in D1's "Seed the body high-water mark here" paragraph, adding the `[100 ok, 200 failed, 300 ok] → 100` example or an explicit pointer to D6's.

### F-2: `sha1sum` is prescribed as a literal binary — no repo precedent, and it does not exist on macOS
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:1056-1060 (§ D7 digest block), spec.md:356-358 (§ Decision 12)
**Convention violated:** `docs/portability-contract.md` §5 (behavioral parity — a skill must reach the same observable end-state on any conforming harness/host); `AGENTS.md:3` "Harness-neutral by intent"; repo practice — `grep -rn 'sha1sum\|shasum\|md5sum\|sha256sum\|openssl' --include=*.md --include=*.py` outside `docs/specs/` returns **zero hits**, so this introduces a new external-binary dependency with no precedent to follow
**Evidence:** D7 ships the computation as a literal command: `printf '%s' '<id>,<id>,…|<key>,<key>,…' | sha1sum | cut -c1-8`. `sha1sum` is GNU coreutils. It is present in this machine's Git Bash, which is why it reads fine here — but macOS ships `shasum` / `openssl sha1` and has no `sha1sum`, so on a mac the pipeline emits `command not found`, `<HEX>` comes back empty, the guard queries for a marker line that no comment carries, and 6f re-posts a duplicate disposition comment on every run — the exact failure `r0`-plus-digest exists to prevent, arriving silently. Note this is a *new* dependency class for `/review-pr`: everything else the skill runs is `git`, `gh`, and `wc`. The repo already has a stdlib-only Python floor (`AGENTS.md:7`), which is the idiom the four shipped `scripts/` dirs use for anything computational.
**Suggested fix:** state the digest as a requirement plus one portable command. E.g. Decision 12: *"`h<HEX>` is the first 8 hex characters of a SHA-1 over the canonical string; any tool that produces it will do, so long as one run reproduces another's value."* and D7: `printf '%s' '<canonical>' | python -c "import hashlib,sys; print(hashlib.sha1(sys.stdin.buffer.read()).hexdigest()[:8])"` — or keep `sha1sum` and add *"(`shasum -a 1` where `sha1sum` is absent)"*. Add a guard row: `grep -cF 'sha1sum' $S` → whatever the chosen form pins.

### F-3: `$TMPDIR` is hardcoded as the scratch location with no definition, fallback, or repo idiom *(re-raised from attempt-1 conventions r4-F-2)*
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:216-218 (Decision 7 required shape), :588 (D1 fetch (c)), :678 (D2 step 3), :913 (D5 poll) vs spec.md:1071-1073 (D7)
**Convention violated:** `docs/portability-contract.md` §5 behavioral parity; repo practice — no `$TMPDIR` idiom exists anywhere in `skills/` (`grep -rn 'TMPDIR\|mktemp' --include=*.md skills/` returns only `hermes-kanban-awareness/SKILL.md:146` "session scratchpad"; the four shipped Python scripts use `tempfile`)
**Evidence:** D7 states the location as a *capability* — "written to the **system temp directory (or the harness scratch directory), never inside the worktree**" — but four other sites hardcode the raw variable: `> "$TMPDIR/body-<REVIEW_ID>.md"`, `> "$TMPDIR/inline_findings"`, `> "$TMPDIR/new_inline"`. `TMPDIR` is not set by bash and is not guaranteed by POSIX for non-login shells; where it is unset the redirect target becomes `/body-<id>.md` — a write to the filesystem root, which fails. Under Decision 14 that failure is classified as a *body harvest failure*, so the round forces `inconclusive` and blocks `:81`/`:83`/`:381` while reporting a harvest problem rather than a bad path. Two of the four sites (`$TMPDIR/inline_findings`, `$TMPDIR/new_inline`) sit in Decision 7's canonical shape, which is the block test row 24 pins — so the bad idiom is the one an implementer copies.
**Suggested fix:** define the location once in D1 (Step 2, alongside `PUSH_TIME`) and have every other site name it — e.g. *"Resolve a scratch directory once: `SCRATCH="${TMPDIR:-/tmp}"`, or the harness scratch directory. Every file below is written under `$SCRATCH`, never in the worktree."* — then use `"$SCRATCH/…"` in Decision 7's required-shape block, D1 (c), D2 step 3, and D5.

### F-4: § Deferred routes the VHS-42 description edit to `/ship-spec`'s Plane step, which cannot edit a description *(re-raised from attempt-1 conventions r4-F-1)*
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:1472-1475 (§ Deferred)
**Convention violated:** prior art — `/ship-spec` Phase 6's documented capability surface (`skills/ship-spec/SKILL.md:217-229`, declared dependency list at `:265`); the audit-trail rule that a filed ticket and the spec that filed it must not contradict each other (wiki `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`)
**Evidence:** the spec says *"**and VHS-42's own `RELATED` paragraph still claims that edit, so `/ship-spec`'s Plane step must trim it from the ticket when this spec ships**"*. Re-verified against the current file: Phase 6 does exactly three things — re-check reachability (`:217`), flip the ticket to the review state via the work-item **state-update** capability (`:228`), post a `PR opened: <pr-url>` **comment** (`:229`) — and its Tool-use notes (`:265`) declare "project listing, work-item state update, work-item comment". No description read or write exists. The instruction is therefore inert, and VHS-42 ships carrying a scope note claiming an edit VHS-41 already made. Constraint any fix must respect: plane-proxy escapes HTML, so a description rewrite must be plain text.
**Suggested fix:** name an actor that exists — *"…so **when this spec ships, edit VHS-42's description** (plane-proxy work-item update capability, plain text) to drop the RELATED paragraph. `/ship-spec` Phase 6 does not touch descriptions, so this is an explicit operator step."* Or drop the description edit and post the correction as a VHS-42 **comment**, which Phase 6 *can* do.

### F-5: Test row 24 pins `≥ 3` but names only two concrete sites
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:1356 (test-plan row 24)
**Convention violated:** the spec's own test-plan discipline (spec.md:1300-1305: "every row is a command whose expected output is pinned"; every positive row must be able to fail); the repo's prose-spec practice of enumerating the exact sites a count row covers (VHS-32 rows 4/6/12, VHS-33 rows 4/7, VHS-36 row 3) — and the same defect class as correctness r3-F-2 / conventions r3-F-1, where a row pinned a count a correct implementation could not produce
**Evidence:** row 24 expects `grep -cF 'HARVEST_FAILURE rc=' $S` → `≥ 3`, justified as "Decision 7's canonical shape at D1 fetch (c), D5's inline poll, and **any further site an implementer converts**". The two named sites contribute exactly one matching line each (the `if [ "$rc" -ne 0 ]; then echo "HARVEST_FAILURE rc=$rc"; …` line). The third match is only guaranteed by D9's edge-case bullet (spec.md:1237-1242), which does carry the literal `HARVEST_FAILURE rc=<n>` — but the row never names it, so an implementer who writes the two fetch blocks and paraphrases the edge case lands on `2` and fails the gate, and the cheapest way to pass is to bolt the token somewhere arbitrary. Rows 13 and 25 are correctly enumerated by contrast (`2` = two named queries; `≥ 3` = three named marker sites).
**Suggested fix:** name the third site — "…D5's inline poll, and D9's `A fetch piped straight into wc -l` edge-case bullet, which states the token pair verbatim" — keeping `≥ 3`.

### F-6: Decision 3 and D8's 6e block still describe behavior their counterparts extended *(re-raised from attempt-1 conventions r4-F-5; the freeze that excused it no longer applies)*
**Severity:** P3
**Where:** spec.md:105-108 (Decision 3) vs spec.md:1014-1019 (D7 post condition); spec.md:1148-1155 (D8's 6e block) vs spec.md:683-688 (D2 step 3)
**Convention violated:** internal consistency between the Decisions layer and the Design layer — the spec's stated structure, where each Decision's *Honored by* line points at the design section that implements it in full
**Evidence:** (1) Decision 3 states the post condition one-armed — "Each round that triaged at least one body-level finding posts exactly one PR-level comment". D7's is two-armed: that case **or** "when `R` would advance past `PRIOR_MARK` and a `HARVEST_FLOOR` exists", with the findings-free body. No contradiction, but a reader taking Decision 3 as canonical gets an incomplete rule, and Decision 3 is what the drift-check reads. (2) D2 step 3 requires the 64 KB line to "emit that line in 6e alongside the other bound lines" — closing edge-cases r3-F-12 — but D8's 6e report block lists `Body harvest bounded` and `Body items grouped` and has **no size row**, so the requirement lands nowhere.
**Suggested fix:** add one clause to Decision 3 (*"…plus, per Decision 12, a findings-free comment on a round that must record forward progress"*) and one line to D8's 6e block (`- Body harvest size: none / review <id> body <n> KB — parsed in slices`).

### F-7: Decision 2 is still tagged *(carried from brief)* although its body is mostly spec-authored resume machinery *(re-raised from attempt-1 conventions r4-F-4)*
**Severity:** P3
**Where:** spec.md:53 (heading), :56-103 (body)
**Convention violated:** the spec's own decision-labeling convention — *(carried from brief)* vs *(spec-author)* — which is the one signal the post-round-4 human drift-check reads to decide what to scrutinize
**Evidence:** the brief's Decision 2 is one sentence (brief.md:27): "in Step 2 and in each 6a/6b cycle, the body of every verdict review newer than the last one handled is read, and 6a's new-findings detection counts body items." The spec's Decision 2 now carries `PRIOR_DISPOSITIONED_REVIEW_ID`, the on-PR marker as the durable cross-run record, the seed-and-advance rule for `LAST_BODY_REVIEW_ID`, and three named consequences including the findings-free-comment rule — none of which the brief or the Plane ticket authorizes. That makes it a category **(c)** addition (rationale is explicit and in-body at spec.md:69-75), not (d) — but the heading still reads (a). Decisions 7–14 are correctly tagged *(spec-author)*.
**Suggested fix:** retag — `### Decision 2 — … *(carried from brief; the cross-run resume marker and the advance rule are spec-author)*`.

### F-8: The bare-tool-name fence still omits `:99`, which sits inside D3's edit region *(re-raised from attempt-1 conventions r4-F-7)*
**Severity:** P3
**Where:** spec.md:551-558 (Design preamble); spec.md:865-869 (D3's per-finding-loop bullet)
**Convention violated:** `docs/portability-contract.md` §4 case 1 (the rule the preamble itself invokes), applied unevenly across the spec's own edit regions
**Evidence:** `skills/review-pr/SKILL.md:99` reads `2. **Read** the actual file at the referenced line using the Read tool`, inside Step 3's per-finding loop (`:96-107`) — which D3 amends and paraphrases in capability language ("Sub-steps 2 (read the file at the referenced line), 3 … and 4 … are otherwise identical"). The preamble names `:180`/`:200` as inside D5's region and `:316`/`:345` as inside D8's, but not `:99` as inside D3's — so the one anchor an implementer is most likely to "normalize" while rewriting that bullet is the one left unmarked. Re-verified: the seven-anchor list itself is accurate.
**Suggested fix:** extend the preamble to "…including **`:99` inside D3's edit region**, `:180`/`:200` inside D5's and `:316`/`:345` inside D8's", and add "the sub-step's existing wording at `:99` is carried through unchanged" to D3's per-finding-loop bullet.

### F-9: Review-round archaeology has no stated spec-only fence, and no shipped skill carries any *(re-raised from attempt-1 conventions r4-F-6)*
**Severity:** P3
**Where:** spec.md — ~110 occurrences of `r<n>-F-<n>` / "the v1|v2|v3|v4 draft", concentrated in Design prose that describes what the skill text should say (e.g. :596-601, :683-688, :711-714, :742-753)
**Convention violated:** repo practice — `grep -rn 'r[0-9]-F-[0-9]' skills/` returns **zero** hits across all eleven shipped skills; VHS-32/33/36 all carried heavy review-citation density in their specs and none of it reached `SKILL.md`
**Evidence:** the spec is explicit about prose that *does* ship ("**Worked specimens** (kept in the skill so a future editor can re-verify without a live PR)", :824; "The skill states that limitation next to them", :838) but never states the complement. Sentences like "The v3 draft's 'before `:79`/`:81`/`:83`' contradicted this paragraph's own order line" (:599) sit *inside* the paragraph describing the ordering rule the skill must state, so the boundary is inferable but unstated — and there is now a fourth draft generation of asides to inherit it.
**Suggested fix:** one sentence in the test-plan preamble — "lens citations (`r<n>-F-<n>`) and draft-history asides are spec-internal; none of them ships into `SKILL.md`" — plus a guard row: `grep -cE 'r[0-9]-F-[0-9]|v[0-9] draft' $S` → `[guard]` `0`, Pre `0`.

### F-10: The gate checklist numbers run 3–16 then 24–26, with 17–23 after — the repo's prose-spec checklists are contiguous
**Severity:** P3
**Where:** spec.md:1320-1338 (fenced command block), :1340-1358 (Pre/Expected table), :1411-1412 (§ Test command)
**Convention violated:** repo practice for prose-spec test plans — `docs/specs/DONE/VHS-32/spec.md` (rows 1–14), `VHS-33` (1–14+), `VHS-36` (1–…) all number their review checklist contiguously and in document order; a reader looks up a row by its position
**Evidence:** the automated gate block reads `3 4 5 … 16 24 25 26`, then the manual specimen walk resumes at `17`, so the document order is 3–16, 24–26, 17–23. The spec explains it (`:1411-1412`: "24–26 were added after round 4 and keep the manual rows' numbering stable"), and the motive — not renumbering rows 17–23 mid-review — is sound while a review loop is running. But this is now a fresh attempt shipping a fresh document; the numbering artifact is the only trace of a review history the reader has no other reason to reconstruct, and `/ship-spec` reads this block as the gate. Low risk, cheap to close; flagging it because the round brief asked for the judgment.
**Suggested fix:** either renumber contiguously at post-green polish — new rows become 17/18/19, the manual walk shifts to 20–26, updating the three cross-references at :1343 (row 4's `≥ 10` note is unaffected), :1352, :1356-1358 and the § Test command sentence — or, if renumbering churn is unwanted, relabel the two groups so contiguity is per-group: `G1…G17` for the automated gate and `M1…M7` for the manual walk, which also removes the "rows 3–16 and 24–26" awkwardness from § Test command.

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 5 | P4: 0

STATUS: RED P0=0 P1=1 P2=4 P3=5 P4=0
