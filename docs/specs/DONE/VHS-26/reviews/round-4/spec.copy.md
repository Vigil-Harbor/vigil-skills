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

Decisions 4, 5 and 8 and the Test plan also pin what the brief's `## Risks / decisions` items 2, 3 and 5 left to the spec author: the file name, its place outside the baseline set, the sample size, the severities, and the checklist. Three rules are the spec author's additions and are not in the brief: the out-of-root anchor and `Anchor: none` rules of Decision 3 (the brief does not address source the author cannot read), the write order of Decision 5, and the no-path P3 of Decision 8.

### Decision 1 — Tier

**Tier:** big

The ticket changes the author/reviewer contract and the review audit trail, so the four-pass first-invocation review cap remains appropriate.

### Decision 2 — Scale is explicitly a non-factor

The brief records `Factor: no`. This is a prose workflow change with one bounded file per dispatched round and no scale machinery.

### Decision 3 — The obligation covers factual runtime claims, not proposed requirements

A runtime-behavior claim is prose asserting how existing code or an existing system behaves when run: for example, that a job fires, a registration occurs, a path resolves, a schedule is recomputed, or a guard blocks an operation. Such a sentence must carry a `file:line` anchor that the author opened and read during preparation of the current dispatch. A source named by a reviewer report, prior spec, wiki page, or brief is only a pointer until the author reads the live line.

The anchor path is project-root-relative when the file is under the project root. A claim about a system whose source is elsewhere on this machine (a sibling repository, the wiki, an installed harness file) is anchored to that file by a path that identifies it; the author still opens and reads the line. A claim about a system whose source the author cannot read (a compiled tool, a hosted service) has no anchor to give. The spec sentence must then say that the behavior is observed or assumed, and its ground-truth-ledger row records `Anchor: none` with how the behavior was observed (a command run and its output, a documentation section read) or the words `assumed, not verified`. `Anchor: none` is never legal for behavior implemented in a file the author can read, inside or outside the project root. These two rules are a spec-level addition to brief Decision 1, which states no exception.

Normative future requirements such as "the implementation must write the ground-truth ledger before dispatch" are not claims that the current runtime already behaves that way and therefore do not need a supporting current-code anchor. Any factual sentence used to justify that requirement does.

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

Each row has exactly the four facts carried by the brief: claim, plain section heading, anchor, and the dispatch round for which the author read it. The row's anchor is the anchor the spec sentence carries. `Spec section` is the innermost heading whose own body holds the sentence. An `Anchor: none` row (Decision 3) puts the observation or `assumed, not verified` after the word `none`. The format is guidance for a human reviewer, not a parser contract, stable section identity scheme, changed-regions input, or computed inventory. It carries no list of changed sections and no line that states its own coverage.

Which claims a round's ground-truth ledger holds depends only on what this invocation wrote before that dispatch:

- **A spec that Phase 1 authored in this invocation.** The first dispatch's ground-truth ledger has a row for every runtime-behavior claim in the spec.
- **A dispatch that follows a revision in the same invocation.** Evidence gathered during that revision is recorded as read in round `<C+1>`. The ground-truth ledger has a row for every runtime-behavior claim in each section the revision edited, whether or not the edit changed that sentence.
- **The first dispatch of an invocation over a spec that already existed** (delta pass 1, a `--full` re-run, any other full re-run). The invocation has authored nothing before that dispatch. The ground-truth ledger holds only the no-claims line below. Text that an operator or an earlier invocation changed outside this invocation is not covered and is not backfilled; the reviewers' ordinary verification still applies to it.

When the covered work contains no runtime-behavior claims, the file holds the explicit line `No runtime-behavior claims were authored or revised for round <C>.` in place of rows.

Rows gathered during authoring or a revision are held until the next dispatch. If they are no longer available at dispatch, the author rebuilds them by re-reading the sections they covered; the no-claims line is never written in their place. One gap is accepted: a run interrupted after Phase 1 writes the spec and before the first dispatch resumes as a re-run, so that spec's first ground-truth ledger holds the no-claims line.

The `## Deferred — follow-up required` section never contributes rows: its rows store reviewer text verbatim and are not the author's claims.

### Decision 5 — The ledger is review evidence, not a new control-plane gate

Immediately before each dispatch, the skill writes the existing baseline artifact set first. It writes the ground-truth ledger only after that set's renames have succeeded (all three files, or the two copies under the named full-pass snapshot failure), using the same same-directory temp-and-rename convention. A pass that stops at `do not dispatch` because a baseline rename failed (`skills/spec-cycle/SKILL.md:454`) therefore writes no ground-truth ledger.

The ground-truth ledger describes the spec as dispatched. On a green round, `spec.copy.md` is rewritten to the post-polish bytes (`skills/spec-cycle/SKILL.md:450`); the ground-truth ledger is not rewritten, so on that round it describes the text before polish. Grounding for polish itself is deferred row D-1.

The existing completeness and recovery rules continue to apply only to `spec.copy.md`, `brief.copy.md`, and `baseline.commit` (`skills/spec-cycle/SKILL.md:444-458`). A failed ground-truth-ledger write:

- prints `ground-truth-ledger.md NOT written: <error> — dispatching; correctness will report the missing evidence`, the `<filename> NOT written: <error>` form of `skills/spec-cycle/SKILL.md:454`, which does not contain the existing `ledger NOT written:` string of `skills/spec-cycle/SKILL.md:460`;
- does not halt, retry, roll back, create a marker state, change the mode table, or make a baseline incomplete; and
- still dispatches the correctness reviewer with the intended path, allowing review to supply this ticket's only enforcement. The reviewer's `ground-truth ledger missing` finding makes that round red; the next dispatch's successful write closes it (Decision 6 step 6).

No ground-truth ledger or addendum is written for an edit with no following reviewer dispatch, including a final-pass rewrite after its dispatch, post-green polish, or grill edits. Attest mode remains unchanged. These rules keep the ground-truth ledger aligned to reviewed snapshots and preserve the existing rule that historical round artifacts are point-in-time records.

### Decision 6 — Revision is a verify–compose–edit–re-read operation

Add an author grounding block to the ordinary §2e routing flow and explicitly apply it to ordinary revisions, delta pass 2, and the final FROZEN/REWRITE pass wherever those paths edit reviewed text:

1. Before embedding a reviewer-supplied count, path, mechanism, API behavior, or other factual assertion, open the live source and verify it. A report's anchor is a lookup hint, not evidence.
2. Before editing text targeted by more than one finding, state the single intended result and compose the findings against it. Do not paste suggested wordings serially into overlapping text.
3. Apply the routed dispositions using the existing fold/defer/reject ceiling unchanged.
4. After editing, re-read every propagation site and every section that consumes the edited decision, not only the section named in the finding. Resolve contradictions before the next dispatch.
5. For every runtime-behavior claim in each section those edits touched, whether or not the edit changed that sentence, read its live `file:line` support and hold the four facts for the next dispatched round's ground-truth ledger. A section here is the innermost heading whose own body was edited. Prior-spec mechanisms receive the same live-code verification.
6. The correctness reviewer's two blocking ground-truth findings (Decision 8) need no new routing rule and no new disposition form:
   - `runtime claim not supported by its anchor` is filed against the spec section that holds the claim. It is an ordinary fold at that section: re-read the live source, then correct the sentence or its anchor. The disposition is the existing `fixed: edited § <section>`, and step 5 supplies that section's rows.
   - `ground-truth ledger missing` has no spec site, so it folds under the existing "one site or none" ceiling (`skills/spec-cycle/SKILL.md:715`) and no spec text changes. Its disposition is a process phrase of the kind the manifest already carries for a missing STATUS line (`skills/spec-cycle/SKILL.md:578-579`): `fixed: ground-truth ledger to be written at the next dispatch`. It names no section, so the re-fold recount never reads it. The next dispatch writes what Decision 4 says that dispatch owes; rows the missing file would have held are not reconstructed. The phrase is the same on the final allowed pass, where the next dispatch belongs to a later invocation.

   The advisory ground-truth findings are P2 or P3 and never enter the manifest. A P2 omission finding is handled by the existing P2 rule: fix it by holding rows for that section for the next dispatch, or list it in `## Deferred (P2+)`.

The block supplements the current "name propagation sites before editing" rule at `skills/spec-cycle/SKILL.md:711-718`; it does not replace routing, recount, guarantee scanning, FROZEN/REWRITE, or closure manifests, and it adds no disposition form.

### Decision 7 — Precedent points to code; it never proves behavior

Phase 1 and §2e both state: a mechanism found in a prior spec or Runbook must be verified against its current live code path before the new spec cites or inherits it. The conventions reviewer receives the same rule under `# Critique lens — conventions and prior art`: precedent may establish naming or intent, but any runtime-behavior assertion it contributes is checked against current code. A prior spec that conflicts with live code is reported as stale precedent rather than propagated.

### Decision 8 — Correctness alone enforces the ledger

Only the correctness prompt receives:

```text
ground_truth_ledger_path: docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth-ledger.md
```

The edge-cases, conventions, and scalability prompt contracts do not receive the path and their verification duties do not change. In the correctness agent, add one unnumbered paragraph block titled `**Ground-truth check.**`. It is a top-level paragraph placed after step 7 and its existing `**Ledger check.**` paragraph (`agents/spec-reviewer-correctness.md:86`) and before the cannot-complete sentence (`agents/spec-reviewer-correctness.md:88`), outside `# Delta scope`. Steps 1–7 keep their numbers. The block is not part of step 7 and reads no `closure_manifest`. It runs on every pass, full or delta. Its row sample opens code anchors, not spec sections, so it does not widen a delta pass's `changed_regions`. The block says:

- **No path supplied.** When the prompt carries no `ground_truth_ledger_path` (an older caller, a hand dispatch), skip the rest of the block and file one P3, `ground-truth ledger path not supplied`.
- **Missing.** When a path was supplied and the file is missing, unreadable, zero-length, or holds neither a human-recognizable claim row nor the no-claims line, file one P0, `ground-truth ledger missing`. This is a human content check, not a grammar parser.
- **Sample.** Check at most five rows. When there are five or fewer, check all. When there are more, check the first two, the middle row (lower middle for an even count), and the last two. For each checked row, open the anchor fresh and read the spec sentence the row names.
- **Grading a checked row.** When the anchor does not support the claim as the spec states it, file a P1, `runtime claim not supported by its anchor`, against the spec section that holds the claim. An `Anchor: none` row is not opened; it draws the same P1 only when the reviewer's normal read finds the behavior implemented in a file this host can read. When the spec sentence's own anchor supports the claim and only the row differs from it, file a P2, not a P1. An anchor whose file or symbol is gone is graded by the agent's existing Anchor drift rule (`agents/spec-reviewer-correctness.md:109`): P1 per dead citation; a line that only moved joins that rule's one combined P4. One defect is one finding: when the same citation or claim is already being filed from the spec text under step 5 or Anchor drift, do not file it again here; note in that finding that the ground-truth ledger repeats it. An anchor outside the project root that this host cannot read is one combined P3.
- **Omission.** The boundary is the set of sections the rows themselves name in `Spec section`, each taken as that heading's own body, not its sub-headings. When the reviewer's normal in-scope read meets a runtime-behavior claim inside the boundary that has no row, file one P2 tagged `Pre-ship recommended`, `ground-truth ledger omits runtime claims`, and list every such claim in that one finding. A file with no rows has no boundary and draws no omission finding. `## Deferred — follow-up required` is never inside the boundary. Do not compute a section inventory or an expected claim set, and do not derive edited sections from the closure manifest or from `changed_regions`.
- **Closure.** A predecessor `runtime claim not supported by its anchor` finding is verified in step 7's closure table against the current spec, like any spec finding. A predecessor `ground-truth ledger missing` finding is CLOSED when the current round's file exists with content, whether rows or the no-claims line.

Two findings block: a missing ground-truth ledger, and a claim its anchor does not support. An omitted row is advisory. This is a stated limit: a section the author edited and gave no row at all draws no ground-truth finding, because the reviewer has no list of edited sections and this ticket gives it none; the agent's existing step 5 still verifies that section's claims about current code, and mechanical completeness is VHS-61.

The agent does not treat the illustrative Markdown layout as a strict grammar, assign stable section identities, run the changed-regions algorithm, or require untouched legacy sections to be backfilled. Its ordinary code verification remains in force; the ground-truth check is additive. The shared `# Delta scope` block remains byte-identical across all four reviewer files.

### Decision 9 — Documentation mirrors the contract briefly

`docs/spec-workflow-reference.md` is the detailed external explanation. `README.md` and `AGENTS.md` receive only short summaries: authors ground runtime claims, each dispatched round carries a ground-truth ledger, correctness samples it, and revisions verify facts and compose overlapping edits. None of these summaries introduces behavior absent from the skill or agent definitions.

## Design

### Phase 1 authoring changes

Extend Phase 1 after the instruction to read files named by the brief (`skills/spec-cycle/SKILL.md:390`) with Decision 3's obligation, including its rules for a file outside the project root and for a system with no readable source. Tell the author to build the upcoming round's ground-truth ledger while writing, using live files rather than reports or precedent. Add the Runbook call-chain sentence and the precedent rule next to this obligation so the requirement is encountered before any design prose is authored. Phase 1 does not re-author an existing spec, so on a re-run it gathers no rows (Decision 4).

Do not add the ground-truth ledger to the spec itself. It is evidence associated with the dispatch snapshot and lives only under that round's review directory.

### Round artifact and dispatch changes

In `### Round artifacts`, document `ground-truth-ledger.md` separately from the three-file baseline set so the existing mode-table and incomplete-baseline semantics do not change. State the write order of Decision 5: baseline renames first, then the ground-truth ledger by the section's atomic temp-and-rename pattern, with Decision 5's warn-and-dispatch behavior and message on failure. State Decision 4's rebuild rule for held rows there. Keep `ledger.md` as the post-revision closure manifest and retain every existing reference to it.

In §2b, add the input in the form the section already uses for per-lens inputs (`skills/spec-cycle/SKILL.md:558`): a line `For the correctness reviewer additionally:` followed by the `ground_truth_ledger_path` bullet. The first pass of an invocation that authored the spec carries Phase 1's rows. A pass that follows a revision carries the rows that revision held. The first pass of a re-run carries the no-claims line. If a loop-red final edit has no next dispatch, it creates no new evidence file.

The guarantee-scan sentence that already names "the author-side ground-truth gate (VHS-26, out of scope)" (`skills/spec-cycle/SKILL.md:698`) is left as written: the scan is still not that gate, and this ticket does not edit §2d.

### Apply-findings changes

Insert Decision 6 into §2e before edits are applied, while keeping the existing route-every-P0/P1 ordering. The composition check occurs after all findings are routed and before overlapping text is changed, because only then is the full set of intended edits known. The post-edit re-read occurs after every routed edit is applied and before `ledger.md` is written. Ground-truth rows gathered in that pass are held only for the next actual dispatch; no file is emitted merely because a revision occurred.

Step 6 adds no manifest vocabulary. The `fixed:` forms listed at `skills/spec-cycle/SKILL.md:594-601` are not extended, and the recount paragraph at `skills/spec-cycle/SKILL.md:757` is not edited: an unsupported-claim finding uses `fixed: edited § <section>`, and the missing-file phrase names no section.

The final FROZEN/REWRITE pass keeps its section boundaries and closed-issues constraints. It performs factual verification, composition, and consumer re-reading for the text it edits, but because no subsequent dispatch exists in that invocation it writes no ground-truth ledger addendum.

### Correctness reviewer changes

Add the prompt-input bullet to the agent's input list, and add the `**Ground-truth check.**` block at the place Decision 8 names. Keep the existing numbered steps 1–7, Plane degradation, whole-spec/current-code grounding, git history read, the existing `**Ledger check.**` paragraph, Anchor drift rule, severity definitions, output shape, and last-line STATUS contract unchanged.

The sample is deterministic so two reviewers do not silently choose only easy rows. Each blocking finding has a simple closure: an unsupported claim is a spec defect fixed by a spec edit, which every lens verifies against the spec as usual, and a missing file is fixed by the file existing, which the correctness lens verifies by Decision 8's Closure rule. The other lenses receive no path and have no rule of their own for the missing-file finding; that gap is listed in `## Deferred (P2+)`. The omission boundary uses only the rows in the file, so it is the same on a first pass, a later pass, and a re-run, and the reviewer derives nothing mechanically.

### Conventions reviewer changes

Under `# Critique lens — conventions and prior art`, add a `## Precedent is not evidence` subsection. It directs the reviewer to verify a mechanism inherited from a prior spec against live code, and to flag stale inheritance at the severity dictated by the existing definitions. Do not edit `# Delta scope`, the deferred-findings contract, or the output contract.

### Documentation changes

Update the existing spec-cycle descriptions in the three documentation files listed in Scope. The workflow reference names the ground-truth ledger path and the correctness-only sample. README and AGENTS stay concise. Since `sync.py` mirrors the existing `skills/` and `agents/` trees (`AGENTS.md:110`), no sync configuration changes are needed.

## Test plan

No new automated test files are added; this ticket changes prose contracts. Review the implementation with this checklist:

- Confirm Phase 1 and every §2e editing path state the live-read obligation, Runbook call-chain trace, and prior-spec rule, including the out-of-root anchor and `Anchor: none` rules.
- Confirm the round-artifact text distinguishes `ground-truth-ledger.md` from disposition `ledger.md`, writes it only for an actual dispatch and only after the baseline renames succeed, states the rebuild rule for held rows, and explicitly preserves baseline completeness and mode-table behavior.
- Confirm the failure message is `ground-truth-ledger.md NOT written: …` and that `grep -c "ledger NOT written:"` over `skills/spec-cycle/SKILL.md` returns the same count before and after the change.
- Confirm only the correctness prompt receives `ground_truth_ledger_path`.
- Confirm the correctness agent's steps are still numbered 1–7 and that the new block is titled `**Ground-truth check.**`, is not indented under step 7, and sits outside `# Delta scope`.
- Confirm the manifest-vocabulary paragraph and the recount paragraph of `skills/spec-cycle/SKILL.md` are unchanged.
- Exercise the correctness instructions mentally with: no path in the prompt; missing file; zero-length or contentless file; one to five rows; more than five rows; a dead path; a line that moved; a live line that does not support the claim; a row whose anchor differs from a correct spec sentence; an `Anchor: none` row for behavior that lives in a readable file; a citation already filed under Anchor drift.
- Exercise the omission boundary mentally with: a new spec whose rows name most sections; a pass after a revision; delta pass 1 after a red halt, which carries a closure manifest; a `--full` re-run. The last two hold only the no-claims line and must draw no omission finding. Confirm an omission is P2 in every case.
- Exercise closure mentally with: a `ground-truth ledger missing` finding followed by a successful write; the same followed by a second failed write; the same on the final allowed pass followed by a later invocation; an unsupported-claim finding fixed by correcting the sentence, and one fixed by deleting it.
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
6. The four agents’ `# Delta scope` blocks remain byte-identical, `python lint.py --strict` is clean, and `python -m unittest discover -s tests -p "test_*.py"` passes.

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

## Deferred (P2+)

- correctness/R4/F-1, conventions/R4/F-3 (P2): Decision 8 narrows the third trigger of brief Decision 7. An omission is filed only inside a section the rows name, and a new spec whose ground-truth ledger holds only the no-claims line draws no ground-truth finding. The `## Decisions` preamble does not record this as a narrowing. Not folded in polish: the fix edits Decisions.
- correctness/R4/F-2, edge-cases/R4/F-2, conventions/R4/F-2 (P2): the disposition `fixed: ground-truth ledger to be written at the next dispatch` carries no path or section that a lens without `ground_truth_ledger_path` can verify, so such a lens may mark the finding REOPENED. Suggested fix: put the next round's `ground-truth-ledger.md` path in the phrase. Not folded in polish: the phrase is in Decision 6.
- edge-cases/R4/F-1, conventions/R4/F-1 (P2): the omission finding is tagged `Pre-ship recommended`, but its fix is not a spec edit, so post-green polish has nothing legal to do with it. Suggested fix: drop the tag and say that on a green round the finding is listed in `## Deferred (P2+)`. Not folded in polish: the tag is in Decision 8.
- correctness/R4/F-3 (P2): when a row's anchor is dead and the spec sentence's own anchor is live and supports the claim, Decision 8 does not say whether the row-differs P2 or the Anchor drift P1 applies. Suggested fix: the row-differs P2 applies first; Anchor drift grades only the spec sentence's own citation. Not folded in polish: the rule is in Decision 8.

## Post-green polish

- correctness/R4/F-2, edge-cases/R4/F-2, conventions/R4/F-2: reworded the closure sentence in § Correctness reviewer changes so it no longer claims every lens can close a missing-file finding. The disposition phrase itself is unchanged; see `## Deferred (P2+)`.
