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

### Decision 1 — Tier

**Tier:** big

The ticket changes the author/reviewer contract and the review audit trail, so the four-pass first-invocation review cap remains appropriate.

### Decision 2 — Scale is explicitly a non-factor

The brief records `Factor: no`. This is a prose workflow change with one bounded file per dispatched round and no scale machinery.

### Decision 3 — The obligation covers factual runtime claims, not proposed requirements

A runtime-behavior claim is prose asserting how existing code or an existing system behaves when run: for example, that a job fires, a registration occurs, a path resolves, a schedule is recomputed, or a guard blocks an operation. Such a sentence must carry a project-root-relative `file:line` anchor that the author opened and read during preparation of the current dispatch. A source named by a reviewer report, prior spec, wiki page, or brief is only a pointer until the author reads the live line.

Normative future requirements such as “the implementation must write the ledger before dispatch” are not claims that the current runtime already behaves that way and therefore do not need a supporting current-code anchor. Any factual sentence used to justify that requirement does.

A Runbook step that invokes code is a runtime-behavior claim. Before writing or revising it, the author traces the invoked entry point through the call chain to the code that admits or rejects the operation and anchors the step to that live code. A command copied from precedent without that trace does not satisfy the obligation.

### Decision 4 — One human-readable `ground-truth-ledger.md` per dispatched round

Every dispatched round may contain `docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth-ledger.md`, called the **ground-truth ledger** everywhere in prose. This name cannot be confused with the existing disposition `ledger.md`, whose closure-manifest role is defined at `skills/spec-cycle/SKILL.md:462`.

The ledger is deliberately human-readable and has no machine-checked grammar. The skill shows this illustrative shape:

```markdown
# Ground-truth ledger — round <C>

Coverage: full spec (new) | <plain heading>; <plain heading> | none (no spec text changed)

- Claim: <runtime-behavior sentence or concise identifying excerpt>
  Spec section: <plain Markdown heading text>
  Anchor: <project-relative path>:<one-based line>
  Read in round: <C>
```

Each row has exactly the four facts carried by the brief: claim, plain section heading, anchor, and the dispatch round for which the author read it. `Coverage:` is a review-visible provenance note, not another row: a new spec says `full spec (new)`; a later dispatch lists the plain headings the preceding revision wrote or edited; a no-edit pass says `none (no spec text changed)`. When the covered authoring or revision work contains no runtime-behavior claims, the file includes the explicit line `No runtime-behavior claims were authored or revised for round <C>.` The format remains guidance for a human reviewer, not a parser contract, stable section identity scheme, changed-regions input, or computed inventory.

For a newly authored spec, round 1 covers runtime-behavior claims throughout the new spec. After round `<C>` is revised, evidence gathered while preparing the next dispatch is recorded as read in round `<C+1>` and covers claims in every section that revision wrote or edited. On a later `/spec-cycle` invocation over a pre-existing spec, untouched sections are not backfilled; only sections the invocation writes or edits enter the next dispatched round’s ledger.

### Decision 5 — The ledger is review evidence, not a new control-plane gate

Immediately before each dispatch, the skill writes the ground-truth ledger by the existing same-directory temp-and-rename convention, then writes the existing baseline artifact set. The exact spec bytes described by the ledger are the bytes copied to that round’s `spec.copy.md`.

The existing completeness and recovery rules continue to apply only to `spec.copy.md`, `brief.copy.md`, and `baseline.commit` (`skills/spec-cycle/SKILL.md:444-458`). A missing or failed ground-truth-ledger write:

- prints `ground-truth ledger NOT written: <error> — dispatching; correctness will report the missing evidence`;
- does not halt, retry, roll back, create a marker state, change the mode table, or make a baseline incomplete; and
- still dispatches the correctness reviewer with the intended ledger path, allowing review to supply this ticket’s only enforcement.

No ground-truth ledger or addendum is written for an edit with no following reviewer dispatch, including a final-pass rewrite after its dispatch, post-green polish, or grill edits. Attest mode remains unchanged. These rules keep the ledger aligned to reviewed snapshots and preserve the existing rule that historical round artifacts are point-in-time records.

### Decision 6 — Revision is a verify–compose–edit–re-read operation

Add an author grounding block to the ordinary §2e routing flow and explicitly apply it to ordinary revisions, delta pass 2, and the final FROZEN/REWRITE pass wherever those paths edit reviewed text:

1. Before embedding a reviewer-supplied count, path, mechanism, API behavior, or other factual assertion, open the live source and verify it. A report’s anchor is a lookup hint, not evidence.
2. Before editing text targeted by more than one finding, state the single intended result and compose the findings against it. Do not paste suggested wordings serially into overlapping text.
3. Apply the routed dispositions using the existing fold/defer/reject ceiling unchanged.
4. After editing, re-read every propagation site and every section that consumes the edited decision, not only the section named in the finding. Resolve contradictions before the next dispatch.
5. For each factual runtime claim authored or changed by those edits, read its live `file:line` support and carry the four ledger facts into the next dispatched round. Prior-spec mechanisms receive the same live-code verification.

The block supplements the current “name propagation sites before editing” rule at `skills/spec-cycle/SKILL.md:711-718`; it does not replace routing, recount, guarantee scanning, FROZEN/REWRITE, or closure manifests.

### Decision 7 — Precedent points to code; it never proves behavior

Phase 1 and §2e both state: a mechanism found in a prior spec or Runbook must be verified against its current live code path before the new spec cites or inherits it. The conventions reviewer receives the same rule under `# Critique lens — conventions and prior art`: precedent may establish naming or intent, but any runtime-behavior assertion it contributes is checked against current code. A prior spec that conflicts with live code is reported as stale precedent rather than propagated.

### Decision 8 — Correctness alone enforces the ledger

Only the correctness prompt receives:

```text
ground_truth_ledger_path: docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth-ledger.md
```

The edge-cases, conventions, and scalability prompt contracts do not receive the path and their verification duties do not change. In the correctness agent, add a mandatory grounding step outside `# Delta scope`:

1. Read the ledger fresh. If it is missing or unreadable, file one P0, `ground-truth ledger missing`, because the required evidence artifact for this dispatch does not exist.
2. Treat a zero-length file, a file with no human-recognizable `Coverage:` declaration, or a file containing neither a human-recognizable claim row nor the exact no-claims line as the same P0. This is a human content check, not a grammar parser.
3. Use `Coverage:` as the omission-check boundary. On later rounds, compare its heading list with sections named on `fixed:` or `reworked:` closure-manifest lines and with edits encountered during ordinary closure/current-spec reading; an edited section visibly omitted from `Coverage:` is P1. Do not compute a section inventory, run the changed-regions algorithm, or backfill untouched headings.
4. If the explicit no-claims line is present but the reviewer’s normal in-scope read encounters a factual runtime-behavior claim inside the declared coverage, file one P1, `ground-truth ledger omits runtime claims`.
5. Otherwise spot-check at most five rows. When there are five or fewer, check all. When there are more, check the first two, the middle row (lower middle for an even count), and the last two. For each sample, open the anchor fresh and confirm the cited line supports the claim.
6. A missing file, out-of-range line, or reference to a symbol that does not exist is P0 under the agent’s existing nonexistent-reference definition. A live anchor that exists but does not support the claim is P1. During the agent’s normal review, any in-scope factual runtime claim inside the declared coverage with no ledger row is also P1. Coalesce multiple omissions of the same kind into one finding and list each claim.

The agent does not treat the illustrative Markdown layout as a strict grammar, compute an expected claim set, assign stable section identities, or require untouched legacy sections to be backfilled. The visible `Coverage:` note lets the reviewer test author-stated provenance without coupling the ledger to changed-regions computation; mechanical completeness remains VHS-61. Its ordinary code verification remains in force; the ledger spot-check is additive. The shared `# Delta scope` block remains byte-identical across all four reviewer files.

### Decision 9 — Documentation mirrors the contract briefly

`docs/spec-workflow-reference.md` is the detailed external explanation. `README.md` and `AGENTS.md` receive only short summaries: authors ground runtime claims, each dispatched round carries a ground-truth ledger, correctness samples it, and revisions verify facts and compose overlapping edits. None of these summaries introduces behavior absent from the skill or agent definitions.

## Design

### Phase 1 authoring changes

Extend Phase 1 after the instruction to read files named by the brief (`skills/spec-cycle/SKILL.md:390`) with Decision 3’s obligation. Tell the author to build the upcoming round’s ground-truth ledger while writing, using live project files rather than reports or precedent. Add the Runbook call-chain sentence and the precedent rule next to this obligation so the requirement is encountered before any design prose is authored.

Do not add the ground-truth ledger to the spec itself. It is evidence associated with the exact dispatch snapshot and lives only under that round’s review directory.

### Round artifact and dispatch changes

In `### Round artifacts`, document `ground-truth-ledger.md` separately from the three-file baseline set so the existing mode-table and incomplete-baseline semantics do not change. Reuse the section’s atomic temp-and-rename pattern, with Decision 5’s warn-and-dispatch behavior on failure. Keep `ledger.md` as the post-revision closure manifest and retain every existing reference to it.

In §2b, add `ground_truth_ledger_path` only to the correctness reviewer’s prompt. The first full pass carries Phase 1’s ledger. A later pass carries the ledger assembled by the immediately preceding revision. If a loop-red final edit has no next dispatch, it creates no new evidence file.

### Apply-findings changes

Insert Decision 6 into §2e before edits are applied, while keeping the existing route-every-P0/P1 ordering. The composition check occurs after all findings are routed and before overlapping text is changed, because only then is the full set of intended edits known. The post-edit re-read occurs after every routed edit is applied and before `ledger.md` is written. Ground-truth rows gathered in that pass are held only for the next actual dispatch; no file is emitted merely because a revision occurred.

The final FROZEN/REWRITE pass keeps its section boundaries and closed-issues constraints. It performs factual verification, composition, and consumer re-reading for the text it edits, but because no subsequent dispatch exists in that invocation it writes no ground-truth ledger addendum.

### Correctness reviewer changes

Add the prompt-input bullet and ledger grounding step before the existing deferred-findings and closure checks in `agents/spec-reviewer-correctness.md`. Keep the existing Plane degradation, whole-spec/current-code grounding, git history read, closure-ledger check, severity definitions, output shape, and last-line STATUS contract unchanged.

The ledger sample is deterministic so two reviewers do not silently choose only easy rows. `Coverage:` makes the later-full-pass boundary visible even though those prompts carry no `changed_regions`; the reviewer checks that author-stated boundary against the closure evidence it already reads rather than deriving one mechanically. The normal review is still responsible for noticing an uncovered runtime claim inside that boundary; the bounded anchor sample tests whether the author’s positive evidence is trustworthy without turning correctness into a second mechanical linter.

### Conventions reviewer changes

Under `# Critique lens — conventions and prior art`, add a `## Precedent is not evidence` subsection. It directs the reviewer to verify a mechanism inherited from a prior spec against live code, and to flag stale inheritance at the severity dictated by the existing definitions. Do not edit `# Delta scope`, the deferred-findings contract, or the output contract.

### Documentation changes

Update the existing spec-cycle descriptions in the three documentation files listed in Scope. The workflow reference names the ledger path and correctness-only sample. README and AGENTS stay concise. Since `sync.py` mirrors the existing `skills/` and `agents/` trees (`AGENTS.md:54-61`), no sync configuration changes are needed.

## Test plan

No new automated test files are added; this ticket changes prose contracts. Review the implementation with this checklist:

- Confirm Phase 1 and every §2e editing path state the live-read obligation, Runbook call-chain trace, and prior-spec rule.
- Confirm the round-artifact text distinguishes `ground-truth-ledger.md` from disposition `ledger.md`, writes it only for an actual dispatch, and explicitly preserves baseline completeness and mode-table behavior.
- Confirm only the correctness prompt receives `ground_truth_ledger_path`.
- Exercise the correctness instructions mentally with: missing ledger, zero-length/contentless ledger, missing or incomplete `Coverage:` provenance on a later full pass, explicit no-claims line contradicted within coverage, one to five rows, more than five rows, dead path, out-of-range line, and a live line that does not support the claim.
- Confirm the conventions agent has the precedent rule and that the edge-cases and scalability agents are unchanged.
- Extract each agent’s `# Delta scope` block and compare the four byte-for-byte.
- Inspect `git diff -- skills/spec-cycle/SKILL.md agents/spec-reviewer-correctness.md agents/spec-reviewer-conventions.md docs/spec-workflow-reference.md README.md AGENTS.md` to confirm no out-of-scope surface changed.
- Run the existing portability lint and full stdlib unit suite.

## Test command

```powershell
$env:PYTHONIOENCODING='utf-8'
python lint.py --strict
python -m unittest discover -s tests -p 'test_*.py'
```

The implementation review also runs the manual checklist above; no script is added to automate it.

## Done when

1. Phase 1 and every reviewed revision require fresh live-code anchors for factual runtime-behavior claims, and every dispatched round writes a human-readable coverage note plus claim → section → anchor → round-read ground-truth ledger or the explicit no-claims line.
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
**Follow-up:** unfiled
