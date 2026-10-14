# Correctness Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor

## Findings

### F-1: Placeholder scan rejects canonical spec paths
**Severity:** P1
**Where:** spec.md:97
**Claim:** “Outside fenced code, blockquotes, and `## Deferred — follow-up required`, the case-insensitive whole-word tokens … `TODO` … are unresolved-placeholder errors.”
**Why this is wrong:** Inline code is not exempt, so the checker would classify `TODO` in canonical paths such as `docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/ground-truth.md` as a whole-word placeholder. This spec contains active, unfenced examples at spec.md:42, spec.md:71, spec.md:82-83, and spec.md:146. Following the design would therefore make the checker reject this spec and ordinary specs that cite the repository’s required artifact location.
**Suggested fix:** Exempt the canonical `docs/specs/TODO/` path segment from placeholder detection, or define a parser rule that distinguishes path segments from author placeholders. Add positive tests for canonical paths alongside genuine `TODO` prose.

### F-2: Coverage grammar has no valid empty-set representation
**Severity:** P0
**Where:** spec.md:61
**Claim:** “On later passes, `coverage` names every section that the pass writes or edits; the author does not backfill untouched sections from an older spec,” while the checker requires “a non-empty valid `coverage:`” and runs before every dispatch.
**Why this is wrong:** A legitimate re-run can dispatch without having edited any spec section: current Phase 1 explicitly does not re-author an existing spec (`skills/spec-cycle/SKILL.md:388`), and full-mode fallbacks or `--full` can proceed directly to review. For that pass, `coverage: all spec sections` violates the no-backfill rule, while any `§ <heading>` list falsely claims coverage of an untouched section. The CLI has no mode or predecessor input that could resolve this contradiction (`spec.md:79-84`).
**Suggested fix:** Add an exact `coverage: no spec sections` form, pair it with the no-claims sentence, and specify when it is legal. Cover unchanged full re-runs and red-marker delta re-runs with no pre-dispatch text edit.

### F-3: Line-sensitive diagnostic keys defeat the one-attempt bound
**Severity:** P0
**Where:** spec.md:115
**Claim:** Diagnostics are tracked by `(code, normalized path, line)`, and if a key from the preceding failed run recurs, the process halts after one fix attempt.
**Why this is wrong:** Fixing another earlier diagnostic can shift an unfixed defect to a new line. The same missing `Verify` line or malformed ledger field then has a different key and receives another attempt, even though the checker reports all violations on every run. Repeated edits above the defect can evade the halt indefinitely, contradicting the asserted “same failure” bound at spec.md:121 and Done-when item 6 at spec.md:267.
**Suggested fix:** Track a stable logical diagnostic identity, such as code, normalized path, owning section/row/item identity, and normalized message independent of source line. Add a test where fixing an earlier error shifts an unchanged later error.

### F-4: Full-pass reviewers cannot verify declared coverage completeness
**Severity:** P1
**Where:** spec.md:151
**Claim:** The correctness reviewer will “verify that coverage includes every section authored on round 1 or named as changed by the current pass.”
**Why this is wrong:** The proposed dispatch adds only `ground_truth_ledger_path` to correctness (`spec.md:143-147`, `spec.md:209`). Full reviewer prompts omit `changed_regions` (`skills/spec-cycle/SKILL.md:542-556`), while the closure manifest contains only P0/P1 dispositions and explicitly excludes P2 changes (`skills/spec-cycle/SKILL.md:566-575`). The checker receives only project root, spec, ledger, and round and merely validates that listed headings exist (`spec.md:79-84`, `spec.md:106`). On a later full pass, neither checker nor reviewer receives the expected changed-section set, so omitted revision-touched sections cannot be detected.
**Suggested fix:** Persist and pass an explicit expected-coverage section list, or give correctness a predecessor spec snapshot/deterministic diff for every pass and require comparison against the ledger. Include P2 and incidental author edits in that source of truth.

### F-5: Ticket not cached
**Severity:** P3
**Where:** brief.md:90
**Claim:** The brief records Plane VHS-26 as its ticket source.
**Why this is wrong:** The memory/ticket service is unavailable for this review, so the canonical ticket description and acceptance criteria could not be independently checked. Review proceeded using the brief as the available authority.
**Suggested fix:** Re-run ticket grounding when the service is available and confirm that no ticket criteria conflict with the brief.

### F-6: Touched review surfaces changed within the last seven days
**Severity:** P3
**Where:** spec § Scope
**Claim:** The spec plans changes across the spec-cycle skill, both reviewer definitions, workflow documentation, README, and AGENTS.md.
**Why this is wrong:** These surfaces changed repeatedly in the freshness window: `fad52c7` on 2026-10-13 touched the skill, both agents, README, and workflow reference; `f64bebe` on 2026-10-13 and `d3730b1` on 2026-10-12 also changed the same review machinery. The spec is grounded at current HEAD `fc20f94`, and its checked anchors still resolve, so this is a freshness signal rather than a demonstrated defect.
**Suggested fix:** Re-run the cited-anchor and integration checks immediately before implementation, especially around dispatch, delta/full mode, artifact ordering, and closure-manifest behavior.

## Summary

P0: 2 | P1: 2 | P2: 0 | P3: 2 | P4: 0

STATUS: RED P0=2 P1=2 P2=0 P3=2 P4=0
