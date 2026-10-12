<!-- Post-green delta pass (round 4), dispatched by the orchestrator after folding Deferred rows D-1 and D-2 under the operator's standing ruling that in-scope P1s fold. Scope limited to the fold: spec § Decision 8, § Design ship-spec Phase 3b irreversible bullet + halt block, § Done when ship-spec bullet, the two Discharged lines, brief D8 / Scope row / Done when. Transcribed from the subagent hand-back. -->

# Correctness Review — round 4 (delta)

Files read: spec, brief, `skills/ship-spec/SKILL.md` (:20-280, :415-436), spec-cycle § 2e row shape and R2 (`skills/spec-cycle/SKILL.md:508`, `:533`, `:539`, `:609`), `AGENTS.md:105`, every round-3 report. Ticket not retrieved (memory_search denied on namespace `skills`); the brief is the record. Recent ship-spec commits 8d404d0, aad9971, 156d388; every anchor the fold cites still holds (`:183`, `:185`, `:187-195`, `:195`, `:177`, `:71-78`, `:432-433`).

## Closure of round 3 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | R1/F-4 (D-1) | Irreversible "re-run /ship-spec" cannot resume the worktree it just created | CLOSED | spec § Decision 8 (option 1 re-resolves step 4b and reruns Phase 3b in the same invocation); halt block prints worktree and branch, says the worktree is kept, option 2 warns `remove` refuses and `--force` discards; Done when "in the same run"; brief D8. |
| edge-cases | R1/F-3 (D-2) | A clean irreversible review is specified as the failed halt | CLOSED | Decision 8 and the irreversible bullet keep both carve-outs; halt cases are no command, not available (incl. step-3 come-back), error or unreadable output; matches SKILL.md:189, :195, :273. |
| correctness | F-1 | Present `## Tier` with no Level line has no halt | CLOSED | spec brief-parse step halts; Test plan item 6 |
| correctness | F-2 | `git worktree remove` said to discard a dirty tree | CLOSED | halt block |
| correctness | F-3 | Workflow reference `N/A` clause | CLOSED | spec § Design docs row |
| correctness | F-4 | ticket not cached (P3) | OPEN (environmental) | — |
| edge-cases | F-1 | `## Tier` with no Level line is not a halt | CLOSED | as above |
| edge-cases | F-2 | Malformed tweak-surface line has no basis slot (P3) | CLOSED | `surfaces: unknown` with `never tweak` suffix and a quote |
| edge-cases | F-3 | Plane ticket body not readable (P4) | OPEN (environmental) | § Deferred (P2+) |
| conventions | — | no round-3 findings | — | round-3/conventions.md GREEN |

Both discharges verified at every section the `Discharged:` lines name. Consistency with Decision 2 (fail-closed), Decision 9, the marker-state table, and the Phase 3 halt-and-wait pattern holds.

## Findings

### F-1: The fold leaves `:185`'s "runs once per run, not again after an operator fix" unamended
**Severity:** P2 · **Pre-ship recommended:** yes
**Where:** spec § Design → ship-spec → Phase 3b intro; § Decision 8
**Claim:** only `:183` gains the irreversible exception.
**Why this is wrong:** SKILL.md:185 forbids re-running after an operator fix; option 1 does exactly that. The edited skill would contradict itself.
**Suggested fix:** Amend `:185` too: "runs once per run" counts a review that ran; an irreversible halt means it did not run; option 1 is the allowed re-run.

### F-2: The two `Discharged:` lines vary the § 2e shape, but are not malformed rows
**Severity:** P3 · **Where:** D-1, D-2
**Why this is wrong:** `folded after round 3 (…)` vs the `folded round <n> — § <a>; § <b>` shape; `brief D8` is not a spec section. Not a routing violation: both rows are P1, well-formed, R2(c) applies only to P0 rows, AGENTS.md:105 names only an in-scope P0 row without `Discharged:` as the P0 case.
**Suggested fix:** Normalise to `**Discharged:** folded round 3 — § Decision 8; § Design, ship-spec Phase 3b; § Done when`.

### F-3: Halt prose adds the error text, but the halt template has no slot for it
**Severity:** P3 · **Suggested fix:** add `<first 20 lines of the error text — failed case only>` under the first line.

### F-4: No Test plan checklist item covers the folded irreversible behaviour
**Severity:** P3 · **Suggested fix:** add item 7 covering the three halts, the two carve-outs, option 1 in the same run, and `big`/absent skips.

### F-5: The halt invites a spec edit after step 1b has already checked the fingerprint
**Severity:** P3 · **Suggested fix:** list CLAUDE.md/AGENTS.md first, or say that editing the spec's § Review command leaves the marker `changed` for later readers.

### F-6: Brief and spec wording on D8 differ slightly
**Severity:** P4 · **Suggested fix:** add "in the same run" to the brief's Done when; say a clean review goes to step 8.

### F-7: Ticket not cached
**Severity:** P3 · environmental; none in the spec.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 4 | P4: 1

STATUS: GREEN
