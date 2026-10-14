# VHS-26 — Author-grounded spec-cycle revisions

## Goal

Make `/spec-cycle` converge on implementable text by requiring the author to ground runtime-behavior claims in live files, mechanically rejecting structurally incomplete specs before reviewer fan-out, structuring how review findings are applied, and stopping automatic review churn when the blocking count does not improve. The change preserves the independent reviewers as the verdict authority: the author ledger is evidence for one correctness-lens spot-check, not a substitute for review.

## Scope

| Path | Change |
|---|---|
| `skills/spec-cycle/SKILL.md` | Add the author ground-truth ledger, pre-dispatch `check_spec.py` gate, structured apply-findings rules, live-code precedent rule, and within-invocation divergence halt. Preserve the existing guarantee scan and mode table. |
| `skills/spec-cycle/scripts/check_spec.py` | New Python 3.8+ stdlib checker for required sections, per-criterion verification lines, unresolved placeholders, deferred-row structure, and ground-truth-ledger structure/anchors. |
| `tests/test_check_spec.py` | New stdlib `unittest` coverage for the checker, including CLI exit behavior and Windows-safe path/newline cases. |
| `agents/spec-reviewer-correctness.md` | Add the round ground-truth ledger as a correctness-only input and require a deterministic support/completeness spot-check. Do not edit the shared `# Delta scope` block. |
| `agents/spec-reviewer-conventions.md` | Add “precedent is not evidence”: prior specs can locate a mechanism, but live code must validate it. Do not edit the shared `# Delta scope` block. |
| `docs/spec-workflow-reference.md` | Document the author ledger, checker, structured revision rules, and divergence halt. |
| `README.md` | Update the short `/spec-cycle` description to name the structural gate and early divergence halt. |
| `AGENTS.md` | Update the lifecycle and reviewer summaries with the new gate and the two reviewer-specific additions. |

Files explicitly unchanged:

- `agents/spec-reviewer-edge-cases.md` and `agents/spec-reviewer-scalability.md`; neither receives or reads the author ledger.
- `skills/ship-spec/`, `skills/spec-close/`, and `skills/spec-brief/`.
- `sync.py`; its recursive `iter_files()` already mirrors every file below `skills/` and therefore installs `skills/spec-cycle/scripts/check_spec.py` without a new subtree rule (`sync.py:30`, `sync.py:48-57`).
- The guarantee scan in `skills/spec-cycle/SKILL.md` remains prose and is not implemented by `check_spec.py` (`skills/spec-cycle/SKILL.md:698`).
- Existing specs and review directories are not backfilled.

## Decisions

### Decision 1 — preserve the stakes tier

**Tier:** big

The change affects the authoring authority, every review pass, persistent round artifacts, two reviewer contracts, and the condition that stops the loop. Four full passes remain available, subject to the new earlier divergence stop.

### Decision 2 — scale is an explicit non-factor

The brief records `**Factor:** no`. The checker handles one spec and one ledger per invocation and introduces no batching, fan-out, or scale target. No scalability reviewer is added.

### Decision 3 — one immutable ground-truth ledger per dispatched round

Every dispatched round gains `docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth.md`. It is frozen with that round’s other point-in-time artifacts and is never edited after dispatch, matching the established forward-only review-artifact convention.

The author prepares the ledger before dispatch using this exact grammar:

```markdown
# Ground-truth ledger — round <C>

round: <C>
coverage: all spec sections | no spec sections | § <heading>; § <heading>; ...

## Claims

### G-1: <short label>
**Claim:** <the runtime-behavior claim as written or an unambiguous paraphrase>
**Spec locations:** § <heading>; § <heading>; ...
**Anchor:** `<project-relative-path>:<positive-line-number>`
**Read in round:** <C>
```

`coverage: all spec sections` is required for a newly authored spec. `coverage: no spec sections` is required when the pass has no known text change against a usable predecessor; it must use the no-claims form below. Otherwise `coverage` names every section changed against the immediate usable `spec.copy.md` baseline, including P2 and incidental edits. Every listed heading must exist in the current spec. A claim repeated across sections may use one row with multiple `Spec locations` entries.

The orchestrator derives `expected_ground_truth_coverage` independently: `all spec sections` when Phase 1 created the spec; the exact text-changed heading set from the existing changed-regions algorithm when a candidate or immediately preceding round supplies a usable `spec.copy.md`; otherwise `no spec sections`. Code-only drift does not add coverage. The author ledger must equal that set. This does not backfill an older spec when no usable text baseline exists.

If the covered sections contain no sentence that states what a runtime does when executed, `## Claims` contains exactly the line `No runtime-behavior claims in the covered sections.` and no `G-<n>` row. A claim includes executable behavior such as firing a job, registering a handler, blocking an operation, resolving a path, reading or writing state, recomputing a schedule, or invoking a command. Pure scope statements, proposed file names, and test intentions are not runtime-behavior claims.

For round 1 the author reads every anchor while authoring; for a later round the author reads it while revising, even when a reviewer, brief, or prior spec supplied the same fact. A Runbook step that invokes code is a runtime-behavior claim: the author traces its call chain to the enforcing code and records the supporting line, rather than anchoring only the command’s surface entry point.

### Decision 4 — prepare the ledger without consuming a failed round

The current loop writes `pending` immediately before its first dispatch and creates a round directory for the saved artifact set (`skills/spec-cycle/SKILL.md:503-513`). The new gate runs before both events so a structural failure consumes no cumulative round and does not leave a pending marker.

Before preparing the temp, create `docs/specs/TODO/<TICKET-ID>.reviews/` idempotently; do not create `round-<C>/` and do not write a marker. For the selected cumulative round `C`, the author atomically prepares the ledger at `docs/specs/TODO/<TICKET-ID>.reviews/.ground-truth.round-<C>.<random>.tmp`. The checker reads that temporary path. Once the check passes (or is skipped because Python is unavailable), the first pass writes `pending`, creates `round-<C>/`, and moves the same bytes into `round-<C>/ground-truth.md` as part of the pre-dispatch artifact write. Later passes do the same preparation and move without rewriting `pending`. A failed or halted check deletes its temporary file; it does not create `round-<C>/`.

At preflight, remove only stale files in this ticket’s reviews root matching `.ground-truth.round-*.tmp`; never recurse and never touch a round directory. Concurrent invocations over one spec are already unsupported. This bounds interrupted temp accumulation without widening deletion scope.

The finalized ledger is added to the round-artifact completeness rule. Its temp is prepared before the three existing copy temps; final renames are `ground-truth.md`, `spec.copy.md`, `brief.copy.md`, then `baseline.commit`. The existing full-pass snapshot exception may omit only `baseline.commit`, never the ground-truth ledger. Any ledger rename failure uses the existing `ground-truth.md NOT written: <error>` stop shape and does not dispatch.

### Decision 5 — `check_spec.py` has a stable, project-root-explicit CLI

The skill invokes the script adjacent to its installed `SKILL.md`, not a presumed repo-relative copy:

```text
<python> <spec-cycle-skill-root>/scripts/check_spec.py \
  --project-root <absolute-project-root> \
  --brief <resolved-brief-path> \
  --spec docs/specs/TODO/<TICKET-ID>.spec.md \
  --ledger docs/specs/TODO/<TICKET-ID>.reviews/.ground-truth.round-<C>.<random>.tmp \
  --round <C>
```

The CLI accepts only those five required arguments. Relative `--brief`, `--spec`, and `--ledger` paths resolve against `--project-root`; absolute inputs are accepted. It reads UTF-8 with an optional BOM and recognizes LF, CRLF, and a missing final newline. It never writes.

Diagnostics use `ERROR <code> <path>:<line-or-0>: <message>` and `WARN <code> <path>:<line-or-0>: <message>`, one per line in deterministic source order, followed by `check_spec: <E> error(s), <W> warning(s)`. Emit at most 200 diagnostic lines, then one `... <n> additional diagnostic(s) omitted` line; the summary carries the full counts. Exit 0 means no errors (warnings allowed), exit 1 means one or more validation errors, and exit 2 means usage, an unreadable required input, or an unexpected checker failure. The skill treats exit 1 and 2 as blocking checker failures.

Before decoding, reject a brief, spec, or ledger larger than 1 MiB with exit 1 and `input-too-large`. A ledger may contain at most 500 claim rows, and each field line may contain at most 16 KiB after its label; exceeding either is an error. These bounds keep a persisted round record and the checker’s context output finite while remaining far above current artifacts.

### Decision 6 — the checker owns mechanical structure, not semantic truth

`check_spec.py` performs these checks and no semantic review:

1. The spec contains exactly one unfenced level-2 heading for each of `Goal`, `Scope`, `Design`, `Test plan`, `Test command`, `Done when`, and `Out of scope`. A duplicate is an error. This supplements rather than replaces Phase 1’s existing early halt for a re-run whose spec lacks a required heading (`skills/spec-cycle/SKILL.md:388`); that halt remains useful when Python is unavailable and keeps the existing operator remedy.
2. Parse the first brief section headed `Done when` or `Acceptance criteria` (case-insensitive, trailing punctuation allowed) and its top-level ordered or unordered items. Parse the spec’s `## Done when` items by the same list rule. When the brief has such a section, the counts must match exactly and ordinal `n` in the spec is the mechanical pair for ordinal `n` in the brief; semantic equivalence remains a correctness-review duty. Every spec item has, before the next peer item or section, one indented `**Verify:**` line. Its value is either a non-empty backticked shell command, or `N/A — <manual check>` only when `## Test command` is exactly `N/A`. Duplicate, empty, or malformed Verify lines are errors.
3. Outside fenced code, blockquotes, and `## Deferred — follow-up required`, the case-insensitive whole-word tokens and literal listed below are unresolved-placeholder errors. Ignore a match inside a whitespace-delimited token that contains `/` or `\`, so canonical artifact paths and other path components are not placeholders. Historical reviewer text in deferred rows stays instruction-inert and is not scanned as author prose.

   ```text
   TBD
   TODO
   TBC
   ???
   ```
4. If `## Deferred — follow-up required` exists, apply the current reviewer block’s fence, blockquote, section-extent, preamble, row-heading, seven-required-field, optional-Discharged-field, Suggested-fix blockquote, and Propagation-sites heading-reference rules. The checker reports structural errors only. It does not classify Scope, enforce the P0/P1 ceiling, discharge rows, or implement the 2d guarantee scan.
5. The ledger has one matching `round:` value, one of the three valid `coverage:` forms, and either the exact no-claims sentence or one or more `G-<positive integer>` rows with all four fields. `no spec sections` requires the no-claims sentence. IDs are unique; every `Spec locations` and explicit coverage entry names a heading in the spec; every `Read in round` equals `--round`.
6. A project-relative anchor must remain below `--project-root`, name an existing regular file, and use a line from 1 through that file’s physical line count. A syntactically absolute anchor, or a relative anchor that resolves outside the root, emits `WARN anchor-outside-root` and is not existence/range checked. Missing, directory, zero, malformed, and out-of-range in-tree anchors are errors.

The checker cannot decide whether prose is a runtime-behavior claim or whether an anchor supports it. The author contract and correctness spot-check own those judgments. An empty or incomplete ledger is still blocking because the mechanical half of the obligation must not be optional.

### Decision 7 — one fix attempt per repeated checker diagnostic

Before every reviewer dispatch, including both full and delta passes, run the checker after the fresh spec read and ledger preparation. A delta no-op still dispatches nothing and therefore runs no checker.

On a blocking run, print the checker output, fix the spec and/or temporary ledger, re-read every file changed by that fix, and run the checker again without incrementing `P` or `C`. Each validator attaches an internal, non-printed owner such as required heading name, Done-when ordinal, deferred row id plus field, ledger row id plus field, normalized anchor, or whole-document sentinel. Track blocking diagnostics by `(code, normalized path, owner)`, never by display line. If any key from the preceding failed run appears again, delete the ledger temp and halt:

```text
check_spec: repeated failure after one fix attempt — <code> <path>:<current-line>; no reviewer dispatched; marker unchanged
```

If only newly exposed keys remain, they receive the same one-fix-attempt rule. This honors the “same failure” bound without turning a second, different diagnostic into an unexplained halt. Because the checker reports all violations rather than short-circuiting, the normal case is one correction and one clean re-run.

Resolve a runnable Python 3 interpreter using the project’s configured Python command when present, then the host’s ordinary Python 3 command. Bound each probe at 10 seconds. A failed or timed-out candidate advances to the next; if none runs, print exactly `check_spec: skipped (python unavailable)` once for the invocation and continue on every pass without probing again. Bound each checker execution at 30 seconds. A checker timeout deletes the ledger temp and halts immediately with `check_spec: timed out after 30s — no reviewer dispatched; marker unchanged`; it is not a spec-fix attempt. The author ledger is still written on the unavailable-Python path and the correctness reviewer still receives it. Attest mode, the delta no-op, and every path that performs no dispatch skip the checker silently except for that one unavailable warning on a dispatching invocation.

### Decision 8 — authoring and revision treat precedent as a locator, never evidence

Phase 1 gains a ground-truth pass after reading the brief and named files: for each runtime-behavior sentence the author intends to write, read the enforcing live code and add a ledger row. A prior spec, reviewer report, wiki page, or brief can identify where to look but cannot support the claim by itself. A Runbook mechanism inherited from precedent must be traced through the live call chain before it is specified.

The same rule is added to ordinary revision and final rewrite. This is separate from the reviewers’ existing obligation to verify current-code claims: it prevents the author from making the reviewers the first code readers.

### Decision 9 — apply findings as a composed, re-grounded change set

After routing all P0/P1 findings and before editing, 2e adds an apply plan for every finding that will fold:

1. **Re-verify supplied facts.** Open the live file for every reviewer-supplied count, path, symbol, mechanism, or runtime statement before embedding it. If live evidence disagrees, reject the fact or rewrite the fix around the evidence; never copy the stale statement. Any runtime claim introduced or changed is entered in the next round’s ground-truth ledger.
2. **Detect overlap and compose once.** Map each fold to exact target headings and, when available, line spans. Two folds overlap when they target the same prose span or when one replaces text the other quotes. Compose overlapping fixes into one intended result before editing; do not apply reviewer Suggested-fix text sequentially. Record each finding’s normal disposition separately even when one composed edit closes several.
3. **Re-read consumers after edits.** After the edit set lands, re-read every propagation site and every section that consumes the edited decision, signature, path, command, or invariant. Repair contradictions before writing the disposition ledger. This is a post-edit read, not satisfied by the pre-edit site enumeration.

These rules run on every revision shape: ordinary full passes, both delta passes, final FROZEN/REWRITE, guarantee-scan discharges, and applicable grill edits. They do not change fold/defer/reject routing or the scope ceiling.

### Decision 10 — only correctness receives and samples the ground-truth ledger

Every correctness prompt adds:

```text
ground_truth_ledger_path: docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth.md
expected_ground_truth_coverage: all spec sections | no spec sections | § <heading>; § <heading>; ...
```

The correctness agent reads it after the spec and brief. Its existing “verify every claim” duty remains authoritative. The new check is:

- Compare the ledger’s coverage exactly with `expected_ground_truth_coverage`, which the orchestrator derived independently from Phase 1 creation state or the usable predecessor text diff. A mismatch is P1.
- If there are one to three claim rows, check all. If there are four or more, check the first, the last, and row `floor((n+1)/2)` in document order. Also check every row tied to a Runbook or Done-when section, even if that exceeds three.
- For each sampled row, read the anchor fresh and decide whether it supports the claim and whether all listed spec locations say the same thing.
- While performing the existing whole-spec correctness walk, file one P1 titled `ground-truth ledger omits runtime claims` when a runtime-behavior claim in covered sections has no ledger row. File P1 for an unsupported sampled claim. Malformed or unreadable ledgers remain process failures; the pre-dispatch checker should normally prevent them.

This is a spot-check of evidence quality plus a completeness check encountered during the lens’s existing read. It does not allow the correctness lens to trust unsampled claims, and it does not change any other lens’s input. To avoid collision with the existing closure `ledger.md`, agent prose calls the new file the “ground-truth ledger” everywhere.

### Decision 11 — conventions explicitly rejects unverified precedent

Under the conventions lens’s “Contradicts a prior decision” / prior-art work, add:

> Precedent is a locator, not evidence. When the spec inherits a runtime mechanism from a prior spec, Runbook, review archive, or wiki narrative, trace it to current live code before accepting it. A precedent-only mechanism with no live-code support is P1 when following it would be non-functional, otherwise P2.

The agent’s mandatory repository and wiki grounding remains unchanged. The shared `# Delta scope` block is untouched.

### Decision 12 — divergence compares blocking totals inside this invocation only

After 2d computes `total_p0p1`, retain the previous dispatched pass’s total in invocation context. Starting with the second dispatched pass, a loop-red pass with `total_p0p1 > 0` diverges when its total is greater than or equal to the immediately preceding pass’s total. Green-withheld rows do not count because the trigger is the reviewer P0/P1 total; a pass with total 0 follows the guarantee-scan discharge path.

The comparison never crosses invocation boundaries, never compares a full run to a later delta run, and does not read older marker or synthesis counts. P2+ remains irrelevant.

When divergence triggers, do not enter 2e, do not edit the spec, and do not write a disposition `ledger.md`. Write the red marker and stop immediately. On a later invocation the ordinary mode table sees the missing candidate ledger and selects `mode: full (ledger unreadable)`; that conservative re-entry cost is preferable to performing the unreviewed patch pass the stop exists to prevent.

Write the normal red marker for cumulative round `C` and render the existing 2f block, prefixed with:

```text
DIVERGENCE STOP: round <C> gate <current> did not decrease from round <previous-C> gate <previous>.
```

The Remaining list, follow-up rendering, four options, fingerprint, and option-4 behavior are unchanged. A divergence on the final allowed pass takes this immediate branch instead of final FROZEN/REWRITE. The current mode table receives no row: a later run sees the ordinary review-produced red marker and row 9’s missing-ledger fallback. Therefore the numbered references to rows 4, 8, 9, and 10 at `skills/spec-cycle/SKILL.md:378`, `:380`, and `:458` do not move.

### Decision 13 — docs describe behavior; tests pin the parser contract

`docs/spec-workflow-reference.md` is the detailed public contract. `README.md` and `AGENTS.md` receive concise summaries only. The Python module exposes pure parse/validate functions plus `main(argv)` so tests can exercise the rules without subprocess dependence, while at least one CLI test pins stdout/stderr and exit codes.

## Design

### Phase 1 authoring flow

After the existing brief/ticket/named-file reads, add an explicit author-grounding walk:

1. Draft the seven required sections and `**Verify:**` line under every Done-when item.
2. Enumerate every runtime-behavior sentence in the draft.
3. Read the enforcing live file and call chain; correct the draft when evidence disagrees.
4. Build the round-1 ground-truth ledger with `coverage: all spec sections`.
5. Save the spec. Phase 2’s pre-dispatch gate validates it and finalizes the ledger.

The scale and tier Decisions remain separate. Phase 1’s existing incomplete-spec re-run halt stays before this flow on an existing spec.

### Pre-dispatch flow

For each pass, after deriving `C` and cold-reading the spec but before `pending`, round-directory creation, snapshot, or agent calls:

1. Create the ticket reviews root if absent and derive `expected_ground_truth_coverage` from the Phase 1 creation flag or usable predecessor text diff.
2. Prepare the temporary ground-truth ledger for `C`.
3. Run `check_spec.py` with the resolved brief, applying Decision 7 on failure.
4. If this is the invocation’s first dispatch, atomically write `verdict: pending`.
5. Acquire the existing commit snapshot.
6. Atomically finalize `ground-truth.md` with the existing round-artifact set.
7. Dispatch all enabled lenses in parallel; add both ground-truth inputs only to correctness.

The no-Python path skips step 2 but not steps 1 or 5. The full-pass invalid-snapshot exception still dispatches with ground-truth/spec/brief and without `baseline.commit`.

### Checker parser boundaries

Implement one fence-aware ATX-heading scan and reuse its section extents for required sections, Done when, Test command, and deferred rows. Fences follow the existing deferred-section rules: at most three leading spaces, three or more matching backticks or tildes, same character and at least opener length to close, and blockquoted markers are inert. A heading must be outside a fence and blockquote.

Brief criteria and spec Done-when peers are non-indented unordered markers (`-`, `*`, `+`) or ordered markers (`N.`) in their section’s exclusive body. A Verify line must be indented under its peer so prose elsewhere cannot satisfy it. The checker reports all errors in one run.

Ledger anchors split on the final colon followed by decimal digits, preserving Windows drive prefixes. Project-relative paths normalize separators only for containment and file access; diagnostics echo the supplied form. Physical line count uses universal newline splitting and counts a final unterminated line.

### Revision and synthesis integration

Lead-judgment synthesis and routing remain in their current order. Decision 9 runs after routing has identified folds and before edits. Dispositions still map one-to-one to findings; a composed edit may be named by several lines. The next ground-truth ledger covers every section changed by the revision and every new or changed runtime claim.

The divergence comparison runs after reports, synthesis, STATUS parsing, and the guarantee scan have established loop-red, but before 2e. It takes the immediate red-marker/halt branch with the divergence prefix and performs no patch.

Post-green polish may still clarify non-behavioral wording, anchors, examples, and checklist rows. A candidate that would add or change a runtime-behavior claim—including executable error behavior—is beyond 2g’s limits and is recorded in `## Deferred (P2+)` with that reason. Thus the reviewed ledger remains complete when the green marker is written.

### Documentation updates

- `README.md`: replace “until findings clean or 4 passes complete” with tier-aware wording that names pre-dispatch structural validation and the no-improvement stop.
- `AGENTS.md`: lifecycle summary names `ground-truth.md`, checker-before-fan-out, structured revisions, and divergence; reviewer table notes correctness’s spot-check and conventions’ live-code precedent rule.
- `docs/spec-workflow-reference.md`: document the full ledger grammar, checker exit/failure behavior, apply rules, and divergence comparison/stop.

## Test plan

Add `tests/test_check_spec.py`, loading the script by file path in the existing stdlib style. Cover:

1. A minimal valid spec plus valid in-tree ledger returns 0.
2. Each required heading missing and duplicated; headings in fences/blockquotes do not count.
3. Brief/spec criterion count and ordinal pairing; Done-when unordered and ordered items with valid commands; missing, duplicate, empty, unindented, and malformed Verify lines; `N/A — manual` accepted only with `Test command: N/A`.
4. Placeholder tokens in active prose block; tokens in fences, blockquotes, deferred Suggested-fix text, and slash/backslash-containing path tokens do not. Include canonical `docs/specs/TODO/` paths.
5. Deferred section preamble, duplicate section, malformed row IDs, missing fields, Suggested-fix quote boundaries, propagation-site counts, nonexistent headings, re-anchored/removed exemptions, and grill-row exemptions. Assert no scope-ceiling or guarantee-scan behavior exists in the script.
6. Ledger matching round, unique IDs, all/no-sections/explicit coverage forms, expected-coverage prompt contract, valid spec locations, explicit no-claims form, missing/extra fields, and mixed no-claims-plus-row rejection.
7. Anchor parsing for project-relative paths, Windows drive-like absolute paths, `..` escapes, missing files, directories, line 0, out-of-range lines, CRLF, BOM, and a final unterminated line. Outside-root anchors warn but do not fail solely for containment.
8. Deterministic diagnostic order, 200-line output cap with full summary counts, 1 MiB/500-row/16 KiB bounds, stable owner-based retry identity across shifted lines, and exits 0/1/2; unreadable inputs return 2.
9. Orchestrator-contract regressions over `skills/spec-cycle/SKILL.md` and the two edited agent files: reviews-root creation precedes the ledger temp; checker is before dispatch; probes/checker are bounded; attest/no-op skip it; post-green polish cannot change runtime behavior; divergence halts before 2e and is within-invocation; correctness alone receives both ground-truth inputs; the two shared `# Delta scope` blocks remain byte-identical to their pre-change counterparts; and the conventions rule contains the live-code requirement.
10. The full existing suite and portability lint remain green.

## Test command

```text
python -X utf8 -m unittest discover -s tests -p "test_*.py"
python -X utf8 lint.py --strict
```

## Done when

1. Every newly authored or revision-touched runtime-behavior claim is represented in that dispatched round’s immutable `ground-truth.md`, with a live `file:line` read in the same round; unchanged passes use the explicit no-sections form; Runbook calls are traced to enforcing code; and post-green polish cannot alter runtime behavior.
   **Verify:** `python -m unittest tests.test_check_spec.TestLedgerValidation tests.test_check_spec.TestAnchorValidation`
2. Every 2e revision re-verifies reviewer-supplied facts, composes overlapping proposed wordings before editing, and re-reads all consumer/propagation sections after editing.
   **Verify:** `python -m unittest tests.test_check_spec.TestSkillContract.test_apply_findings_rules`
3. A second consecutive dispatched pass in one invocation with a positive P0/P1 total that is not lower halts before 2e through the existing 2f menu with the divergence prefix; comparisons never cross invocations.
   **Verify:** `python -m unittest tests.test_check_spec.TestSkillContract.test_divergence_contract`
4. Prior specs and review/wiki narratives are treated only as locators: the authoring/revision rules and conventions lens require current live-code evidence before inheriting a runtime mechanism.
   **Verify:** `python -m unittest tests.test_check_spec.TestSkillContract.test_precedent_requires_live_code`
5. Runbook executability is part of the same runtime-claim ledger and requires an enforcing-call-chain anchor rather than a separate mechanism.
   **Verify:** `python -m unittest tests.test_check_spec.TestSkillContract.test_runbook_claim_contract`
6. `check_spec.py` compares every brief criterion ordinal with a spec Done-when item and Verify command before every full or delta reviewer dispatch, reports all structural failures within explicit size/output bounds, permits one fix attempt per stable repeated diagnostic, uses bounded subprocesses, skips once per invocation when Python is unavailable, and is fully covered by the new stdlib test module.
   **Verify:** `python -m unittest tests.test_check_spec`

## Out of scope

- Implementing the guarantee scan in Python or changing its scope/discharge semantics.
- Backfilling ground-truth ledgers for specs or untouched sections written before VHS-26.
- Running the checker in attest mode or on a delta no-op.
- Changing `/ship-spec`, `/spec-close`, `/spec-brief`, reviewer severity definitions, fold/defer/reject routing, or the review gate formula.
- Giving the ground-truth ledger to edge-cases, conventions, or scalability reviewers; only correctness spot-checks it.
- Editing any reviewer’s shared `# Delta scope` block.
- Resolving the GAV-9/GAV-10 rehearsal mechanism; it remains incident evidence only.

