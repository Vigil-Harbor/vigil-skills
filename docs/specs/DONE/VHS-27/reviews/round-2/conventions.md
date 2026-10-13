# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Reader state `changed` never selects a candidate round | CLOSED | spec § Mode, lines 126–130 and 152; scenario 2b, line 396 |
| correctness | F-2 | Green-round `spec.copy.md` is taken before post-green polish | CLOSED | spec § Decision 2, line 48; § Artifacts, line 214; scenario 2, line 394 |
| correctness | F-3 | Output-contract closure line stays on the round-1 rule | CLOSED | spec § Delta contract, line 329 |
| correctness | F-4 | Ticket not cached | CLOSED | spec § Deferred (P2+), line 472; no spec change, as the finding asked |
| edge-cases | F-1 | Ledger coverage is a substring test | CLOSED | spec § Decision 3, line 52; ledger check, line 353; scenario 11, line 414 |
| edge-cases | F-2 | House-style `path:line` citations never count as code drift | CLOSED | spec § Changed regions, lines 275–276; scenario 10, line 412 |
| edge-cases | F-3 | Any edit marks every ancestor section changed | CLOSED | spec § Decision 10, line 80; § Changed regions, line 263; § Delta contract, line 340 |
| edge-cases | F-4 | A git error suppresses the no-op, then an empty delta may go green | CLOSED | spec § Decision 5, line 60; § Mode, line 160; § Two counters, line 202; scenario 12, line 416 |
| edge-cases | F-5 | A review marker whose round is not a positive integer falls through to delta | CLOSED | spec § Mode row 10, line 155; § Artifacts, line 223; scenario 13, line 418 |
| edge-cases | F-6 | `baseline.commit` and `ledger.md` treat a Windows newline as corrupt | CLOSED | spec § Mode, lines 136–138; § Artifacts, line 221 |
| edge-cases | F-7 | The no-op can report green for a red marker | CLOSED | spec § No-op, lines 171–172 and 179; § Changed regions, line 283 |
| edge-cases | F-8 | Only the immediate next round directory is reserved | CLOSED | spec § Decision 8, line 72; § Mode row 9, line 154; § Artifacts, line 227 |
| conventions | F-1 | Output-contract closure line is not an edit site | CLOSED | spec § Delta contract, line 329 |
| conventions | F-2 | Correctness anchor replacement leaves the old P1 rule in place | CLOSED | spec § Decision 4, line 56; § Delta contract, lines 345–347 |
| conventions | F-3 | Decision 7 omits the Follow-up filter § Mode applies | CLOSED | spec § Decision 7, line 68 |
| conventions | F-4 | Single-counter write-points and closure prose are not named as edit sites | CLOSED | spec § Docs, lines 373–386, names Write points, Interrupted run, both Round 2+ copies, Stakes tier, and the spec-brief grill bullet |
| conventions | F-5 | Invocation syntax is specified once and copied in three places | CLOSED | spec § Invocation, line 116 |
| conventions | F-6 | Mode row 9 is a spec-level addition to the brief's mode list | CLOSED | spec § Decision 14, line 96, lists the span row and the non-integer round row as storage rules |
| conventions | F-7 | § 2b's sample disposition still cites a skill line | CLOSED | spec § Ledger, line 248 |

## Findings

### F-1: Grill paths in `### 2f-i` are not an edit site
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Two counters, line 202; spec § Stop screens, line 367
**Convention violated:** The spec's own rule that every edit site is a heading. The grill's directory is not only the halt menu.
**Evidence:** `skills/spec-cycle/SKILL.md` `### 2f-i` still reads and writes `round-<round_cap>`: the seed at line 701, the persist path at line 737, and the re-render path at line 765. The spec says the grill uses `round-<C>/` but never names `### 2f-i`. On a full invocation that does not start at round 1, `C` is not `round_cap` either (spec § Two counters, lines 191–197; § Stop screens, line 367).
**Suggested fix:** Name `### 2f-i` in § Stop screens. Say the seed, the `grill.md` persist, and the re-render path use `round-<C>` on every halt. That equals `round-<round_cap>` only when the full invocation started at round 1.

### F-2: Three workflow-reference sentences still treat `round_cap` as the cumulative round
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Docs, lines 377–384
**Convention violated:** The same "two copies must not disagree" rule § Docs already applies to Round 2+ closure tracking. These three sentences are the remaining copies of the single-counter story.
**Evidence:** `docs/spec-workflow-reference.md` line 31 (`### The grilling contract`) says the grill follows `round_cap` rounds. Line 72 (Phase 2 intro) says the final round, `round == round_cap`, is the rewrite and the halt follows that cap. Line 307 (adapting bullet `**Targeted rewrite at round round_cap**`) says the same. § Docs names the Stakes-tier paragraph and the two Round 2+ paragraphs, and not these three.
**Suggested fix:** Name all three in § Docs. State that each describes the first invocation's pass index `P`, and that a delta halt, and a full invocation whose start is not 1, rewrites and grills at cumulative `C`.

### F-3: New git commands are not added to `## Tool-use notes`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Changed regions, lines 265–270; spec § Docs, lines 373–376
**Convention violated:** The skill's command inventory is `## Tool-use notes`. Prior spec-cycle edits list every git command there. This spec adds three and does not name that heading.
**Evidence:** `skills/spec-cycle/SKILL.md` line 935 lists `git rev-parse` and calls `git merge --ff-only` the lone git-level mutation of tracked files. It does not list `git diff` or `git ls-files`. The spec's code-drift set is `git diff --name-only`, `git diff --name-only --cached`, and `git ls-files --others --exclude-standard`, plus `git rev-parse HEAD` (spec § Changed regions, lines 265–270, and § Artifacts, line 229).
**Suggested fix:** Name `## Tool-use notes` in § Docs. Add those read-only commands beside `git rev-parse`. Leave the lone-mutation sentence as it is: the new commands do not change tracked files.

### F-4: Changed-region headings do not reuse the skill's heading boundary
**Severity:** P3
**Where:** spec § Changed regions, line 261
**Convention violated:** Reuse the heading rule the skill already uses, instead of a second grammar.
**Evidence:** Phase 0 step 8 and step 9 end a section body at the next `^#{1,6}\s` heading (`skills/spec-cycle/SKILL.md` lines 299 and 351). The spec splits on `^#{1,6} ` (exactly one space). A tab or a second space is a boundary for tier and scale and not for a changed region. Fences are already reused from the Deferred section; the heading test is not.
**Suggested fix:** In § Changed regions, use `^#{1,6}\s`, still at column 0, still outside a Deferred-section fence, and still not a blockquote line.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
