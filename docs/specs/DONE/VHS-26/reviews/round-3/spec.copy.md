# VHS-26 — Author-grounded spec-cycle revisions

## Goal

Make `/spec-cycle` authors verify runtime-behavior claims against live code during initial authoring and every reviewed revision, preserve that evidence in a per-dispatch ground-truth ledger, and have the correctness reviewer enforce the obligation. The same change makes apply-findings passes compose overlapping edits and re-read their consumers, while teaching both authors and the conventions reviewer that prior specs are pointers to evidence rather than evidence themselves.

## Scope

| Path | Change |
|---|---|
| `skills/spec-cycle/SKILL.md` | Add the author-side grounding rule to Phase 1 and §2e, define and write the per-round ground-truth ledger, pass only its path to the correctness reviewer, and add the apply-findings composition and re-read rules. The current authoring, round-artifact, dispatch, and revision surfaces are at `skills/spec-cycle/SKILL.md:384`, `skills/spec-cycle/SKILL.md:444`, `skills/spec-cycle/SKILL.md:511`, and `skills/spec-cycle/SKILL.md:706`. |
| `agents/spec-reviewer-correctness.md` | Accept and read the ground-truth-ledger path, perform the bounded spot-check, and report missing or unsupported evidence. Keep `# Delta scope` byte-identical to the other reviewer agents; it currently begins at `agents/spec-reviewer-correctness.md:90`. |
| `agents/spec-reviewer-conventions.md` | Add the “precedent is not evidence” rule under its critique lens, outside the shared delta block. The critique lens currently begins at `agents/spec-reviewer-conventions.md:103`. |
| `docs/spec-workflow-reference.md` | Briefly document author grounding, the fourth per-dispatch artifact, correctness enforcement, and structured apply-findings behavior in the existing spec-cycle section at `docs/spec-workflow-reference.md:43`. |
| `README.md` | Add one short ground-truth-ledger sentence to the `/spec-cycle` overview at `README.md:10`; do not turn the README into the normative contract. |
| `AGENTS.md` | Add the matching project-level invariant to the lifecycle description and reviewer summary at `AGENTS.md:27` and `AGENTS.md:43`. |

No new file is created outside the existing per-round review directories. `agents/spec-reviewer-edge-cases.md`, `agents/spec-reviewer-scalability.md`, `tests/`, `sync.py`, and every other lifecycle skill remain unchanged.

## Decisions

Decisions 1 and 2 record the brief's `## Tier` and `## Scale` sections. The others carry the brief's numbered decisions: Decision 3 carries brief Decisions 1 and 6; Decision 4 carries brief Decisions 2 and 3; Decision 5 carries the brief's Out-of-scope fences on dispatch and control flow; Decision 6 carries brief Decision 4; Decision 7 carries brief Decision 5; Decision 8 carries brief Decision 7; Decision 9 carries brief Decision 8.

### Decision 1 — Tier

**Tier:** big

The ticket changes the author/reviewer contract and the review audit trail, so the four-pass first-invocation review cap remains appropriate.

### Decision 2 — Scale is explicitly a non-factor

The brief records `Factor: no`. This is a prose workflow change with one bounded file per dispatched round and no scale machinery.

### Decision 3 — The obligation covers factual runtime claims, not proposed requirements

A runtime-behavior claim is prose asserting how existing code or an existing system behaves when run: for example, that a job fires, a registration occurs, a path resolves, a schedule is recomputed, or a guard blocks an operation. Such a sentence must carry a `file:line` anchor that the author opened and read during preparation of the current dispatch. A source named by a reviewer report, prior spec, wiki page, or brief is only a pointer until the author reads the live line.

The anchor path is project-root-relative when the file is under the project root. A claim about a system whose source is elsewhere on this machine (a sibling repository, the wiki, an installed harness file) is anchored to that file by a path that identifies it; the author still opens and reads the line. A claim about a system whose source the author cannot read (a compiled tool, a hosted service) has no anchor to give. The spec sentence must then say that the behavior is observed or assumed, and its ledger row records `Anchor: none` with how the behavior was observed (a command run and its output, a documentation section read) or the words `assumed, not verified`. `Anchor: none` is never legal for behavior implemented in a file under the project root.

Normative future requirements such as "the implementation must write the ledger before dispatch" are not claims that the current runtime already behaves that way and therefore do not need a supporting current-code anchor. Any factual sentence used to justify that requirement does.

A Runbook step that invokes code is a runtime-behavior claim. Before writing or revising it, the author traces the invoked entry point through the call chain to the code that admits or rejects the operation and anchors the step to that live code. A command copied from precedent without that trace does not satisfy the obligation.

### Decision 4 — One human-readable `ground-truth-ledger.md` per dispatched round

Every dispatched round writes `docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth-ledger.md`, called the **ground-truth ledger** everywhere in prose, never the bare word "ledger". This name cannot be confused with the existing disposition `ledger.md`, whose closure-manifest role is defined at `skills/spec-cycle/SKILL.md:462`.

The ground-truth ledger is deliberately human-readable and has no machine-checked grammar. The skill shows this illustrative shape:

```markdown
# Ground-truth ledger — round <C>

- Claim: <runtime-behavior sentence or concise identifying excerpt>
  Spec section: <plain Markdown heading text>
  Anchor: <path>:<one-based line>
  Read in round: <C>
```

Each row has exactly the four facts carried by the brief: claim, plain section heading, anchor, and the dispatch round for which the author read it. An `Anchor: none` row (Decision 3) puts the observation or `assumed, not verified` after the word `none`. The format is guidance for a human reviewer, not a parser contract, stable section identity scheme, changed-regions input, or computed inventory. It carries no list of changed sections.

Which claims a round's ground-truth ledger holds depends only on what this invocation wrote before that dispatch:

- **A spec that Phase 1 authored in this invocation.** The first dispatch's ground-truth ledger has a row for every runtime-behavior claim in the spec, and carries one extra line directly under its title, the **new-spec line**: `New spec: rows cover every section.`
- **A dispatch that follows a revision in the same invocation.** Evidence gathered during that revision is recorded as read in round `<C+1>`. The ground-truth ledger has a row for every runtime-behavior claim in each section the revision edited, whether or not the edit changed that sentence. It has no new-spec line.
- **The first dispatch of an invocation over a spec that already existed** (delta pass 1, a `--full` re-run, any other full re-run). The invocation has authored nothing before that dispatch. The ground-truth ledger holds only the no-claims line below. Text that an operator or an earlier invocation changed outside this invocation is not covered and is not backfilled; the reviewers' ordinary verification still applies to it.

When the covered work contains no runtime-behavior claims, the file holds the explicit line `No runtime-behavior claims were authored or revised for round <C>.` in place of rows.

The `## Deferred — follow-up required` section never contributes rows: its rows store reviewer text verbatim and are not the author's claims.

### Decision 5 — The ledger is review evidence, not a new control-plane gate

Immediately before each dispatch, the skill writes the existing baseline artifact set first. It writes the ground-truth ledger only after that set's renames have succeeded (all three files, or the two copies under the named full-pass snapshot failure), using the same same-directory temp-and-rename convention. A pass that stops at `do not dispatch` because a baseline rename failed (`skills/spec-cycle/SKILL.md:454`) therefore writes no ground-truth ledger.

The ground-truth ledger describes the spec as dispatched. On a green round, `spec.copy.md` is rewritten to the post-polish bytes (`skills/spec-cycle/SKILL.md:450`); the ground-truth ledger is not rewritten, so on that round it describes the text before polish. Grounding for polish itself is deferred row D-1.

The existing completeness and recovery rules continue to apply only to `spec.copy.md`, `brief.copy.md`, and `baseline.commit` (`skills/spec-cycle/SKILL.md:444-458`). A failed ground-truth-ledger write:

- prints `ground-truth-ledger.md NOT written: <error> — dispatching; correctness will report the missing evidence`, the `<filename> NOT written: <error>` form of `skills/spec-cycle/SKILL.md:454`, which does not contain the existing `ledger NOT written:` string of `skills/spec-cycle/SKILL.md:460`;
- does not halt, retry, roll back, create a marker state, change the mode table, or make a baseline incomplete; and
- still dispatches the correctness reviewer with the intended path, allowing review to supply this ticket's only enforcement. The reviewer's `ground-truth ledger missing` finding makes that round red; Decision 6 step 6 says how the next round closes it.

No ground-truth ledger or addendum is written for an edit with no following reviewer dispatch, including a final-pass rewrite after its dispatch, post-green polish, or grill edits. Attest mode remains unchanged. These rules keep the ground-truth ledger aligned to reviewed snapshots and preserve the existing rule that historical round artifacts are point-in-time records.

### Decision 6 — Revision is a verify–compose–edit–re-read operation

Add an author grounding block to the ordinary §2e routing flow and explicitly apply it to ordinary revisions, delta pass 2, and the final FROZEN/REWRITE pass wherever those paths edit reviewed text:

1. Before embedding a reviewer-supplied count, path, mechanism, API behavior, or other factual assertion, open the live source and verify it. A report's anchor is a lookup hint, not evidence.
2. Before editing text targeted by more than one finding, state the single intended result and compose the findings against it. Do not paste suggested wordings serially into overlapping text.
3. Apply the routed dispositions using the existing fold/defer/reject ceiling unchanged.
4. After editing, re-read every propagation site and every section that consumes the edited decision, not only the section named in the finding. Resolve contradictions before the next dispatch.
5. For every runtime-behavior claim in each section those edits touched, whether or not the edit changed that sentence, read its live `file:line` support and hold the four facts for the next dispatched round's ground-truth ledger. Prior-spec mechanisms receive the same live-code verification. This is the same section-level rule the reviewer applies in Decision 8, so an author who follows it draws no omission finding.
6. A finding that the correctness reviewer files against the ground-truth ledger itself (missing, an anchor that does not support its claim, an omitted claim) is routed like any other finding. It is fixed by re-reading the live source. When the spec sentence is wrong, correct it; that section is then an ordinary fold site. When only the evidence was wrong or absent, no spec text changes: the finding has no site, and folds under the existing "one site or none" ceiling (`skills/spec-cycle/SKILL.md:715`). In both cases hold a corrected row for each named claim for the next dispatched round's ground-truth ledger, and write the disposition as `fixed: ground-truth rows carried — § <a>; § <b>`, naming each section whose claims the carried rows cover (after `fixed: edited § <a>` when spec text also changed). For a `ground-truth ledger missing` finding, the carried rows are the rows the missing file owed; when it owed the new-spec line, the next ground-truth ledger carries that line and the disposition reads `fixed: ground-truth rows carried — every section`. On the final allowed pass no later dispatch exists, so no ground-truth ledger is written (Decision 5) and the finding stands in the red halt block like any other unresolved finding.

The block supplements the current "name propagation sites before editing" rule at `skills/spec-cycle/SKILL.md:711-718`; it does not replace routing, recount, guarantee scanning, FROZEN/REWRITE, or closure manifests.

### Decision 7 — Precedent points to code; it never proves behavior

Phase 1 and §2e both state: a mechanism found in a prior spec or Runbook must be verified against its current live code path before the new spec cites or inherits it. The conventions reviewer receives the same rule under `# Critique lens — conventions and prior art`: precedent may establish naming or intent, but any runtime-behavior assertion it contributes is checked against current code. A prior spec that conflicts with live code is reported as stale precedent rather than propagated.

### Decision 8 — Correctness alone enforces the ledger

Only the correctness prompt receives:

```text
ground_truth_ledger_path: docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth-ledger.md
```

The edge-cases, conventions, and scalability prompt contracts do not receive the path and their verification duties do not change. In the correctness agent, add one unnumbered paragraph block titled `**Ground-truth check.**`. It is a top-level paragraph placed after step 7 and its existing `**Ledger check.**` paragraph (`agents/spec-reviewer-correctness.md:86`) and before the cannot-complete sentence (`agents/spec-reviewer-correctness.md:88`), outside `# Delta scope`. Steps 1–7 keep their numbers. The block is not part of step 7 and does not depend on a `closure_manifest` being present. It runs on every pass, full or delta. Its row sample opens code anchors, not spec sections, so it does not widen a delta pass's `changed_regions`. The block says:

- **No path supplied.** When the prompt carries no `ground_truth_ledger_path` (an older caller, a hand dispatch), skip the rest of the block and file one P3, `ground-truth ledger path not supplied`.
- **Missing.** When a path was supplied and the file is missing, unreadable, zero-length, or holds neither a human-recognizable claim row nor the no-claims line, file one P0, `ground-truth ledger missing`. This is a human content check, not a grammar parser.
- **Sample.** Check at most five rows. When there are five or fewer, check all. When there are more, check the first two, the middle row (lower middle for an even count), and the last two. Also check every row for a claim that a predecessor ground-truth finding named (see Closure below). For each checked row, open the anchor fresh and confirm the cited line supports the claim.
- **Grading a checked row.** A live anchor that does not support its claim is P1, `ground-truth anchor does not support claim`. An anchor whose file or symbol is gone is graded by the agent's existing Anchor drift rule (`agents/spec-reviewer-correctness.md:109`): P1 per dead citation; a line that only moved and still supports the claim joins that rule's one combined P4. One defect is one finding: when the same citation or claim is already being filed from the spec text under step 5 or Anchor drift, do not file it again here; note in that finding that the ground-truth ledger repeats it. An anchor outside the project root that this host cannot read is one combined P3, not a blocking finding. An `Anchor: none` row is not opened; it is P1, `ground-truth anchor does not support claim`, only when the reviewer's normal read finds the behavior implemented in a file under the project root.
- **Omission.** The boundary is: every section when the new-spec line is present; otherwise the sections named on `fixed:` or `reworked:` lines of the `closure_manifest` in this prompt; otherwise no section. `## Deferred — follow-up required` is never inside the boundary. When the reviewer's normal in-scope read meets a runtime-behavior claim inside the boundary that has no row, file one P1, `ground-truth ledger omits runtime claims`, and list every such claim in that one finding. With no boundary there is no omission finding: this is the first dispatch of a re-run, and nothing is backfilled. Do not compute a section inventory or an expected claim set.
- **Closure.** A predecessor finding filed by this block is verified in step 7's closure table like any other. It is CLOSED when the current ground-truth ledger holds a supporting row for each claim that finding named, or, for `ground-truth ledger missing`, when the current file exists with content.

The agent does not treat the illustrative Markdown layout as a strict grammar, assign stable section identities, run the changed-regions algorithm, or require untouched legacy sections to be backfilled; mechanical completeness remains VHS-61. Its ordinary code verification remains in force; the ground-truth check is additive. The shared `# Delta scope` block remains byte-identical across all four reviewer files.

### Decision 9 — Documentation mirrors the contract briefly

`docs/spec-workflow-reference.md` is the detailed external explanation. `README.md` and `AGENTS.md` receive only short summaries: authors ground runtime claims, each dispatched round carries a ground-truth ledger, correctness samples it, and revisions verify facts and compose overlapping edits. None of these summaries introduces behavior absent from the skill or agent definitions.

## Design

### Phase 1 authoring changes

Extend Phase 1 after the instruction to read files named by the brief (`skills/spec-cycle/SKILL.md:390`) with Decision 3's obligation, including its rules for a file outside the project root and for a system with no readable source. Tell the author to build the upcoming round's ground-truth ledger while writing, using live files rather than reports or precedent, and to put the new-spec line under its title. Add the Runbook call-chain sentence and the precedent rule next to this obligation so the requirement is encountered before any design prose is authored. Phase 1 does not re-author an existing spec, so on a re-run it gathers no rows (Decision 4).

Do not add the ground-truth ledger to the spec itself. It is evidence associated with the dispatch snapshot and lives only under that round's review directory.

### Round artifact and dispatch changes

In `### Round artifacts`, document `ground-truth-ledger.md` separately from the three-file baseline set so the existing mode-table and incomplete-baseline semantics do not change. State the write order of Decision 5: baseline renames first, then the ground-truth ledger by the section's atomic temp-and-rename pattern, with Decision 5's warn-and-dispatch behavior and message on failure. Keep `ledger.md` as the post-revision closure manifest and retain every existing reference to it.

In §2b, add the input in the form the section already uses for per-lens inputs (`skills/spec-cycle/SKILL.md:558`): a line `For the correctness reviewer additionally:` followed by the `ground_truth_ledger_path` bullet. The first pass of an invocation that authored the spec carries Phase 1's ground-truth ledger. A pass that follows a revision carries the rows that revision held. The first pass of a re-run carries the no-claims line. If a loop-red final edit has no next dispatch, it creates no new evidence file.

The guarantee-scan sentence that already names "the author-side ground-truth gate (VHS-26, out of scope)" (`skills/spec-cycle/SKILL.md:698`) is left as written: the scan is still not that gate, and this ticket does not edit §2d.

### Apply-findings changes

Insert Decision 6 into §2e before edits are applied, while keeping the existing route-every-P0/P1 ordering. The composition check occurs after all findings are routed and before overlapping text is changed, because only then is the full set of intended edits known. The post-edit re-read occurs after every routed edit is applied and before `ledger.md` is written. Ground-truth rows gathered in that pass, including rows carried to close a ground-truth finding (Decision 6 step 6), are held only for the next actual dispatch; no file is emitted merely because a revision occurred.

The final FROZEN/REWRITE pass keeps its section boundaries and closed-issues constraints. It performs factual verification, composition, and consumer re-reading for the text it edits, but because no subsequent dispatch exists in that invocation it writes no ground-truth ledger addendum.

### Correctness reviewer changes

Add the prompt-input bullet to the agent's input list, and add the `**Ground-truth check.**` block at the place Decision 8 names. Keep the existing numbered steps 1–7, Plane degradation, whole-spec/current-code grounding, git history read, the existing `**Ledger check.**` paragraph, Anchor drift rule, severity definitions, output shape, and last-line STATUS contract unchanged.

The sample is deterministic so two reviewers do not silently choose only easy rows. The omission boundary uses only what the reviewer already holds: the new-spec line, or the closure manifest it already reads for step 7. The reviewer derives nothing mechanically. The normal review is still responsible for noticing an uncovered runtime claim inside that boundary; the bounded anchor sample tests whether the author's positive evidence is trustworthy without turning correctness into a second mechanical linter.

### Conventions reviewer changes

Under `# Critique lens — conventions and prior art`, add a `## Precedent is not evidence` subsection. It directs the reviewer to verify a mechanism inherited from a prior spec against live code, and to flag stale inheritance at the severity dictated by the existing definitions. Do not edit `# Delta scope`, the deferred-findings contract, or the output contract.

### Documentation changes

Update the existing spec-cycle descriptions in the three documentation files listed in Scope. The workflow reference names the ground-truth ledger path and the correctness-only sample. README and AGENTS stay concise. Since `sync.py` mirrors the existing `skills/` and `agents/` trees (`AGENTS.md:110`), no sync configuration changes are needed.

## Test plan

No new automated test files are added; this ticket changes prose contracts. Review the implementation with this checklist:

- Confirm Phase 1 and every §2e editing path state the live-read obligation, Runbook call-chain trace, and prior-spec rule, including the out-of-root anchor and `Anchor: none` rules.
- Confirm the round-artifact text distinguishes `ground-truth-ledger.md` from disposition `ledger.md`, writes it only for an actual dispatch and only after the baseline renames succeed, and explicitly preserves baseline completeness and mode-table behavior.
- Confirm the failure message is `ground-truth-ledger.md NOT written: …` and that `grep -c "ledger NOT written:"` over `skills/spec-cycle/SKILL.md` returns the same count before and after the change.
- Confirm only the correctness prompt receives `ground_truth_ledger_path`.
- Confirm the correctness agent's steps are still numbered 1–7 and that the new block is titled `**Ground-truth check.**`, is not indented under step 7, and sits outside `# Delta scope`.
- Exercise the correctness instructions mentally with: no path in the prompt; missing file; zero-length or contentless file; one to five rows; more than five rows; a dead path; a line that moved; a live line that does not support the claim; an `Anchor: none` row for behavior that lives in the repo; a citation already filed under Anchor drift.
- Exercise the omission boundary mentally with: a new spec carrying the new-spec line; a pass after a revision with a closure manifest; delta pass 1 after a red halt; a `--full` re-run; a pass dispatched full because `ledger.md` was missing. The last three must draw no omission finding.
- Exercise closure mentally with: a `ground-truth ledger missing` finding followed by a successful write; the same followed by a second failed write; an unsupported-anchor finding where only the row was wrong; the same on the final allowed pass.
- Confirm the conventions agent has the precedent rule and that the edge-cases and scalability agents are unchanged.
- Extract each agent's `# Delta scope` block and compare the four byte-for-byte.
- Inspect `git diff -- skills/spec-cycle/SKILL.md agents/spec-reviewer-correctness.md agents/spec-reviewer-conventions.md docs/spec-workflow-reference.md README.md AGENTS.md` to confirm no out-of-scope surface changed.
- Run the existing portability lint and full stdlib unit suite.

## Test command

Run both from the repository root:

```text
python lint.py --strict
python -m unittest discover -s tests -p "test_*.py"
```

The implementation review also runs the manual checklist above; no script is added to automate it.

## Done when

1. Phase 1 and every reviewed revision require fresh live-code anchors for factual runtime-behavior claims, and every dispatched round writes a human-readable claim → section → anchor → round-read ground-truth ledger or the explicit no-claims line.
2. §2e re-verifies reviewer-supplied facts, composes findings that overlap the same text before editing, and re-reads every propagation site and consumer after editing.
3. Phase 1, §2e, and the conventions reviewer all state that a prior spec is a pointer rather than evidence and require live-code verification before inheriting a runtime mechanism.
4. Runbook steps that invoke code require an anchored trace through the exact live call chain that admits or rejects the operation.
5. Only the correctness reviewer receives the ground-truth-ledger path; it applies Decision 8’s deterministic sample and blocking findings while retaining its existing verification duties.
6. The four agents’ `# Delta scope` blocks remain byte-identical, `python lint.py --strict` is clean, and `python -m unittest discover -s tests -p 'test_*.py'` passes.

## Out of scope

- `check_spec.py`, any structural or ledger script, required-section/TBD/deferred-row checks, fix-and-rerun behavior, no-Python fallback, a new `scripts/` directory, or new tests. These belong to VHS-61; nothing in this ticket runs a new program.
- The divergence stop, P0/P1 trend arithmetic, any §2d gate change, any §2f halt-menu change, or any mode-table change. These belong to VHS-62.
- Any connection between the ground-truth ledger and changed-regions computation: no section identities, computed expected coverage, or deleted-heading tombstones.
- A ledger or addendum for an edit with no later reviewer dispatch, including final-pass rewrites, post-green polish, and grill edits.
- A new halt, marker state, rollback, retry rule, temp-file cleanup step, or size bound.
- Backfilling untouched sections in specs authored before this ships.
- Changes to attest mode, the guarantee scan, the edge-cases or scalability reviewers, `sync.py`, `tests/`, `/ship-spec`, `/spec-close`, or `/spec-brief`.
- Resolving the GAV-9/GAV-10 rehearsal-mechanism discrepancy; it is evidence for this ticket, not work in this repository.

## Deferred — follow-up required

> Known, unfixed P0/P1 findings. Not part of this spec's implementation: `/ship-spec` must not implement anything in this section. Each row becomes a follow-up ticket filed by the operator.

### D-1: Post-green polish bypasses author grounding
**Finding:** edge-cases/R1/F-2 (P1)
**Deferred in:** round 1
**Where:** spec § Decision 5 — The ledger is review evidence, not a new control-plane gate; spec § Decision 6 — Revision is a verify–compose–edit–re-read operation; spec § Apply-findings changes
**Suggested fix:**
> Require post-green polish to live-verify any factual claim or anchor it applies, compose overlapping candidates, and re-read affected consumers, while preserving the brief’s explicit rule that polish produces no ledger/addendum and no new review round.

**Propagation sites:** § Decision 5 — The ledger is review evidence, not a new control-plane gate; § Decision 6 — Revision is a verify–compose–edit–re-read operation; § Apply-findings changes
**Scope:** out-of-scope — `skills/spec-cycle/SKILL.md` §2g Post-green polish; the brief Scope table contains no §2g or post-green-polish row
**Follow-up:** VHS-63
