# Conventions Review — round 2

Grounding: spec read fresh, `AGENTS.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, the current `skills/review-pr/SKILL.md` (all cited anchors), `sync.py`, `lint.py` output, the pytest baseline, the wiki (`projects/vigil-skills/state.md`, `filemap.md`, `decisions/` — VHS-17/18/29/32/33/36), the brief, and all three round-1 reports.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Step 2 (a) drops `body` but infra check reads it | CLOSED | § Design D1 adds fetch `(a2)` single-resource body fetch + explicit `(a)→(a2)→infra check→(b)` order |
| correctness | F-2 (P1) | Depth count off by one | CLOSED | § D2 step 5: walk begins at the `<details>` line *preceding* the summary; verified anchors (PR#28 body 8/9, petland 3/4) |
| correctness | F-3 (P1) | `:381` "No new comments" never amended | CLOSED | § D9 rewrites `:381` → "No new findings"; verified `:381` is that line |
| correctness | F-4 (P1) | `:341` omitted from Decision 5 | CLOSED | Decision 5 now enumerates six (`:68,:75,:174,:194,:224,:341`) — all six verified as list endpoints; D8 converts `:341` |
| correctness | F-5 (P1) | `no-push` marker collides | CLOSED | Decision 12 keys the marker `r<R>` = highest review id in the harvest set |
| correctness | F-6 (P2) | No-push call site never located | CLOSED | § D4 identifies `:127` gate; § D7 amends `:245` (verified `:245` is that sentence) |
| correctness | F-7 (P2) | File-group regex matches its own summary | CLOSED | § D2 step 6: scanning starts on the line **after** the summary |
| correctness | F-8 (P2) | `sync.py status` expectation false | CLOSED | Moved to § Test plan "Observational"; `cmd_status()` returning `None` verified at `sync.py:155` |
| correctness | F-9 (P3) | Decision 2 widens the brief's window | CLOSED | Decision 2 § "How this resolves the round-1 objection"; Decision 8 § "Evidence status" |
| correctness | F-10 (P3) | `LAST_BODY_REVIEW_ID` advance undefined | CLOSED | § D6 "Advance rule", incl. the empty-harvest-set case |
| edge-cases | F-1 (P0) | same as correctness F-1 | CLOSED | § D1 `(a2)` |
| edge-cases | F-2 (P0) | `:341` unpaginated | CLOSED | § D8 first bullet |
| edge-cases | F-3 (P1) | Tripwire structurally unreachable | CLOSED | Decision 11 adds the phrase tripwire alongside the count tripwire |
| edge-cases | F-4 (P1) | Marker not unique | CLOSED | Decision 12 |
| edge-cases | F-5 (P1) | Full-history harvest defeats `:81` | CLOSED | Decision 2 marker resume; § D1 short-circuit clause is on *findings*, not the harvest set |
| edge-cases | F-6 (P1) | Quoted `<details>` in code samples | CLOSED | § D2 step 4b fence + inline-code masking, with the self-referential case named |
| edge-cases | F-7 (P1) | Harvest fetches unhandled on failure | CLOSED | Decision 14 (5 bullets incl. partial-`--paginate` and fail-closed guard) |
| edge-cases | F-8 (P1) | 6a body query `{id}` only | CLOSED | § D5 projects `{id, state, submitted_at}` with the reason stated inline |
| edge-cases | F-9 (P2) | Dedup before tripwire | CLOSED | Decision 11 uses the **pre-dedup** extraction count; § D2 step 10 |
| edge-cases | F-10 (P2) | Body-only round vs empty thread set | CLOSED | § D8 scopes the Phase 1 short-circuit to fix findings *with an inline thread* |
| edge-cases | F-11 (P2) | jq errors on null comment body | CLOSED | `(.body // "")` in § D7 guard and § D2 step 1 |
| edge-cases | F-12 (P2) | `Unlabeled` vs nitpick default | CLOSED | § D3 states precedence explicitly |
| edge-cases | F-13 (P2) | No per-round item bound | CLOSED | § D2 step 9 (20) |
| edge-cases | F-14 (P2) | Cache has no re-derive fallback | CLOSED | § D2 step 3 "cache is an optimization only" |
| edge-cases | F-15/16/17/18 (P3) | loose range / marker order / blockquote depth / concurrency | CLOSED | § D2 step 7; Decision 9; § D2 step 4a; Decision 12 § Race |
| conventions | F-1 (P2) | False `SUBTREES` claim; `scripts/` precedent | CLOSED | Decision 13. Verified: `sync.py:30 SUBTREES = ("skills", "agents")`, `iter_files` uses `root.rglob("*")` (`:45`), and four skills ship `scripts/` (`spec-close`, `session-handoff`, `talaria`, `hermes-kanban-awareness`) |
| conventions | F-2 (P2) | Two severity-matching rules | CLOSED | § D3 bullet 1 (one word-contains rule); § D2 step 7 defers to D3; Nitpick moved out of the table |
| conventions | F-3 (P2) | `AGENTS.md` § /review-pr goes stale | CLOSED | § Scope row + § D10 + test row 12. VHS-29 precedent verified — `7db7289` touches `AGENTS.md` |
| conventions | F-4 (P2) | Test plan drops the grep-checklist shape | CLOSED | § Test plan rows 3–13; missing-requires pinned at 2 (verified: `lint.py --strict` → `0 error(s), 2 warning(s)`, review-pr + ship-spec) — but see new F-2 below on row quality |
| conventions | F-5 (P2) | `sync.py status` is not a gate | CLOSED | § Test plan Observational paragraph; § Done when 2 reconciled |
| conventions | F-6 (P2) | "no test suite" claim false | CLOSED | § Test plan opens with the 5-module inventory; row 13 baseline verified exactly: `1 failed, 158 passed, 3 skipped`, failure is `test_lint.py::TestLint::test_shipped_skills_clean` (`11 != 8`) |
| conventions | F-7 (P3) | Heading naming | CLOSED | `### 2b.` / `### 6f.` throughout, matching the file's `### 1b.` / `6a`–`6e` |
| conventions | F-8 (P3) | Monotonic-id claim ungrounded | CLOSED | Decision 7 closing paragraph |
| conventions | F-9 (P3) | `--body-file` path inside the worktree | CLOSED | § D7 requires temp/scratch dir + removal; `:127`/Step 5 staging rationale verified |
| conventions | F-10 (P3) | `requires:` backlog not cited | CLOSED | § Out of scope 2 — `docs/authoring-portable-skills.md:41` verified verbatim ("Today two shipped skills (`ship-spec`, `review-pr`)…"), plus the VHS-18 wiki decision |
| conventions | F-11 (P3) | Intent-phrased prose | CLOSED | § Design preamble, citing portability-contract §4 case 1 — but the count it states is wrong; see new F-3 |

No REOPENED items. All 39 round-1 findings are closed.

## Findings

### F-1: Decision 5's exclusion list is incomplete, so test row 4's checklist is not decidable as claimed
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5 (lines 122–126); § Test plan row 4
**Convention violated:** the spec's own stated standard — "Two fetches are deliberately **excluded** and named **so the checklist is decidable**"
**Evidence:** `grep -n "gh api" skills/review-pr/SKILL.md` returns nine call sites. Six are the named list fetches; `:290` (graphql) and `:209` (`gh pr checks`) are the named exclusions; `:252`/`:262` are the `-X POST` replies row 4 names. **`:172` is unaccounted for:** `PUSH_TIME=$(gh api repos/<OWNER>/<REPO>/commits/$HEAD_SHA --jq '.commit.committer.date')`. It matches row 4's `grep -c 'gh api repos'` numerator, is not a list endpoint, and is named nowhere in Decision 5 or row 4.
**Suggested fix:** add `:172` (`commits/<sha>`, single resource) to Decision 5's excluded-and-named list, and to test row 4's "not list fetches" clause alongside the `-X POST` calls and the `reviews/<ID>` body fetches.

### F-2: Three grep-checklist rows cannot fail — they already pass against unmodified `main`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan rows 4, 7, 10
**Convention violated:** the shape § Test plan claims for itself ("every row is a command whose expected output is pinned"), and the repo's recorded prose-spec gate lesson (assert the region, not a count)
**Evidence:** run against the current worktree, pre-change:
- Row 7 (`grep -cF 'select(.state != "COMMENTED")'` → expected `≥ 3`) returns **6** today — three jq sites (`:69`, `:175`, `:342`) plus three prose mentions (`:65`, `:339`, `:404`). If an implementer *did* unify the two filters (the exact regression row 7 names), the prose mentions alone keep it at 3 and the row still passes.
- Row 10 (`grep -cF 'Duplicate comments'` → expected `≥ 1`) returns **1** today.
- Row 4 has no pinned expected value at all — its "Expected" cell is a prose judgment, not an output.

Contrast the rows that do discriminate: rows 6, 9, 11, 12 all return 0 pre-change, and rows 5, 8 change 3→0 and 1/2→0.
**Suggested fix:** pin row 7 to the jq sites only (e.g. `grep -cF 'select(.state != "COMMENTED")] |'` → exactly `0`, since D8 converts all three to the streaming form — or `grep -cF '| select(.state != "COMMENTED") | {'` → exactly `3`). Pin row 10 to the post-change count with the non-goal wording (e.g. `grep -cF 'Duplicate comments' … ` → `≥ 2` once Decision 1's explicit non-goal line lands). For row 4, give it a pinned number: after the change `grep -c 'gh api --paginate repos'` should be exactly 9 (six converted + 2b resume + 6a body query + 6f guard).

### F-3: The Design preamble's fence over pre-existing bare tool names undercounts them, and misses three inside the regions being edited
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design preamble (lines 348–352)
**Convention violated:** `docs/portability-contract.md` §4 (the rule the preamble invokes); and the repo's verify-don't-assert discipline (wiki `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`), which is the same class as round-1 conventions F-1/F-6
**Evidence:** the spec says "The file's **four** pre-existing bare tool names (`:11`, `:99`, `:120`, `:200`) are out of scope and stay." `grep -n "Read tool\|Edit tool\|Bash tool\|Write tool" skills/review-pr/SKILL.md` returns **seven** lines: `:11`, `:99`, `:120`, `:180`, `:200`, `:316`, `:345`. Three of the missed ones sit inside regions this spec edits — `:180` in 6a (D5's territory), `:316` and `:345` in 6d (D8's territory) — so the "out of scope and stay" fence is silent exactly where an implementer will be rewriting prose.
**Suggested fix:** correct the count to seven and list all seven anchors, explicitly noting that `:180`, `:316`, `:345` fall inside D5/D8's edit regions and are carried through unchanged.

### F-4: The Deferred section departs from the established `## Deferred (P2+)` convention
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Deferred (P2+), lines 932–947
**Convention violated:** the shape set by `docs/specs/DONE/VHS-36/spec.md:886-921`, and the repo's recorded practice that a valid, out-of-scope, non-trivial finding gets a ticket *and* a Deferred entry
**Evidence:** VHS-36's Deferred opens with the rule — "Filed as tickets where a future run could hit them; recorded here where the trigger is remote enough that a ticket would only age" — and every entry then carries either a ticket ID and date (`VHS-38 … Filed 2026-09-07, Backlog`) or an explicit non-filing rationale (`Not filed, because the case needs the operator to answer more than question_cap claims in a single round`). VHS-41's two real deferrals carry neither: the red-test bullet says only "the bump wants its own ticket" (no ID, no filing status), and the `AGENTS.md:7` bullet says only "belongs with the tripwire bump above". Separately, the third bullet ("Round-1 P3s folded rather than deferred") is closure accounting, not a deferral, and does not belong under this heading.
**Suggested fix:** file the red-test bump as a VHS ticket and record its ID + date on the first bullet (it is a live red on `main`, so a future `/ship-spec` run *will* hit it); either fold the second bullet into that ticket's scope or give it the explicit "not filed, because …" form. Move the round-1-P3 accounting bullet out of § Deferred — it belongs in a closing note or nowhere, since the review artifacts already record it.

### F-5: D3 changes the *inline* severity-matching rule — a behavior change on the path the ticket is not about
**Severity:** P3
**Where:** spec § Design D3, first two bullets
**Convention violated:** silent-addition class (c) — a spec-level position the brief and ticket don't authorize; flagged here for the human drift-check
**Evidence:** the brief's Scope row for Step 3 authorizes only "Body-level items enter the same triage table with their own severity labels." D3 goes further and rewrites the *existing* inline discipline: the table's emoji-keyed patterns (`skills/review-pr/SKILL.md:91-94` — `_🔴 Critical_`, `_🟠 Major_`, `_🟡 Minor_`) become word-contains, the `Nitpick` row leaves the table entirely, and two rows (`Trivial`, `Unlabeled`) are added. The change has a rationale ("so a CodeRabbit emoji change cannot silently break inline triage") and it is the right resolution of round-1 conventions F-2 — but it originates from a reviewer finding, not the brief, and § Out of scope 4's fence ("the three-cycle cap, the polling attempt counts, the fast-path threshold, or any thread-resolution or approval behavior") does not cover severity matching. Every existing inline finding on every future PR is triaged through the new rule.
**Suggested fix:** one sentence in D3 marking it as a spec-level addition beyond the brief's Step 3 row, with the emoji-fragility rationale — so the drift-check sees it as a deliberate widening rather than a table tidy-up.

### F-6: `AGENTS.md:7`'s known-false claim is deferred while the same PR edits `AGENTS.md`
**Severity:** P3
**Where:** spec § Deferred bullet 2; § D10
**Convention violated:** `AGENTS.md` is the canonical project instructions (per this repo's own `CLAUDE.md`); shipping a diff that touches it while leaving an adjacent claim the same spec documents as false is the failure mode wiki `decisions/…vhs-36-operator-claims-are-verified-not-trusted.md` exists to discourage
**Evidence:** `AGENTS.md:7` reads "Not an application — no build step, **no test suite**, no dependencies beyond Python 3.8+ stdlib." The spec's own § Test plan opens by contradicting it and verifying five pytest modules; § D10 opens `AGENTS.md` in the same PR. The deferral's stated reason — that it "belongs with the tripwire bump above" — pairs a docs sentence with a `tests/test_lint.py` integer change, which is an arbitrary bundling.
**Suggested fix:** either strike "no test suite" from `AGENTS.md:7` in D10 (a two-word edit in a file already in the diff, and § Scope's `AGENTS.md` row would need only "two sentences" instead of "one"), or replace the bundling rationale with a real one — e.g. that `AGENTS.md:7`'s framing is a single paragraph a separate pass should rewrite whole.

### F-7: Decision 13 cites VHS-29 for the refusal contract but not for its rejection of fence-masking markdown parsing
**Severity:** P3
**Where:** spec § Decision 13
**Convention violated:** engaging a prior decision on every axis it bears on (`decisions/2026-08-25-vhs-29-anchor-is-a-refusal-contract.md`)
**Evidence:** Decision 13 uses VHS-29 correctly on the refuse-vs-degrade axis. But that same decision's *Options Considered* §2 rejected the approach this spec now adopts: "**Parse the markdown.** Mask fenced blocks, walk the AST, place structurally. Rejected on cost and blast radius: **fence masking is the first step toward a markdown parser inside a skill script**." § D2 step 4b is exactly fence masking (plus inline-code spans, blockquote-depth stripping, and a `<details>` depth walk) — moved from a script into skill prose. That is not a contradiction (VHS-29's rejection is scoped to `log.md` placement and carries a concrete revisit trigger), but a reader who knows VHS-29 will ask whether the spec noticed.
**Suggested fix:** add one clause to Decision 13 — that VHS-29 rejected fence-masking *inside a script that must place a write correctly*, whereas here the parse is read-only and its failure mode is a reported tripwire rather than a corrupted file, which is why the same cost objection does not carry over.

### F-8: `AGENTS.md:46` points at the heading, not the paragraph the spec edits
**Severity:** P4
**Where:** spec § Scope row 2; § Design D10 heading
**Convention violated:** the repo's `file:line` precision norm (`AGENTS.md` § Plan & Spec Reviews: "specific `file:line` references")
**Evidence:** `AGENTS.md:46` is `### /review-pr`; the paragraph D10 appends to is `AGENTS.md:48` ("Standalone skill for triaging CodeRabbit review comments. Reads findings, verifies…"). Line 47 is blank.
**Suggested fix:** cite `AGENTS.md:46-48` (heading + paragraph) or `AGENTS.md:48` in both places.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 3 | P4: 1

STATUS: GREEN
