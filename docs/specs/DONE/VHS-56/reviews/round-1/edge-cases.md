# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: A partially failed pass can become valid for an irreversible brief
**Severity:** P1
**Where:** docs/specs/TODO/VHS-56.spec.md:155; docs/specs/TODO/VHS-56.spec.md:209
**Edge case:** A `big` pass completes cycle 1, changes the draft, then suffers a cycle-2 dispatch failure. At Confirm, the operator changes the tier to `irreversible`.
**What happens:** Decision 12 records the result as `completed at cap`. Design 6 preserves a prior completed pass across tier changes, so the workflow can write an irreversible brief despite the dispatch failure. This bypasses the stated irreversible failure policy.
**Why the spec misses it:** The persisted outcome and tier-change rule do not distinguish successful cap completion from a cycle-2 failure. Design 6 re-evaluates prior skips but explicitly preserves completed passes.
**Suggested fix:** Distinguish successful completion from completion with a failed dispatch in the in-memory state. Apply the irreversible failure gate when changing tiers; a pass with either dispatch failed cannot satisfy it. Specify whether that transition stops or permits a new pass, and add this exact transition to the review matrix. Scope the cycle-2 continuation rule explicitly to `small` and `big`.

### F-2: Adding a decision under `--no-grill` retains a stale doubt result
**Severity:** P1
**Where:** docs/specs/TODO/VHS-56.spec.md:209
**Edge case:** After completing the doubt pass under `--no-grill`, the operator selects Confirm option 2 and adds a decision.
**What happens:** The final brief can contain a newly added, unreviewed decision while retaining the completed result from the previous candidate. This new decision can contradict existing acceptance criteria without passing through the new doubt/reconciliation step.
**Why the spec misses it:** The preserved menu has a distinct `--no-grill` branch: `skills/spec-brief/SKILL.md:184` appends a decision directly. Design 6 invalidates review only for “revising an interview answer” and resumes Phase 3 after “the resumed interview returns”; neither event occurs on this branch.
**Suggested fix:** Explicitly invalidate the doubt result after `--no-grill` option 2 adds a decision, re-render the candidate, and return through Phase 3 from cycle 1 with the applicable tier policy. Add this branch to Test plan item 8.

### F-3: Ticket grounding was blocked by namespace permissions
**Severity:** P2
**Where:** docs/specs/TODO/VHS-56.brief.md:4
**Edge case:** The mandatory ticket lookup is attempted through shared memory.
**What happens:** The service returns `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. This review therefore uses the supplied brief as its ticket-contract authority.
**Why the spec misses it:** This is a review-environment limitation, not a defect in the proposed implementation. The brief expressly records that the tracker text predates the scope split.
**Suggested fix:** No implementation change required. Preserve this grounding limitation in the review record; restore namespace access if independent ticket verification is needed.

### F-4: The persisted operator skip reason has no size bound
**Severity:** P3
**Where:** docs/specs/TODO/VHS-56.spec.md:116
**Edge case:** An operator supplies a very long explanation after `2:`.
**What happens:** The entire explanation becomes audit metadata in the brief and is carried into downstream context. The fixed-size outcome record can thus acquire arbitrarily large free text.
**Why the spec misses it:** The only validation trims whitespace and rejects an empty reason; no length or single-line normalization is defined.
**Suggested fix:** Define a modest length limit and normalize the reason to one line before recording it. Re-prompt for a concise reason when it exceeds the limit.

## Summary

P0: 0 | P1: 2 | P2: 1 | P3: 1 | P4: 0

Persistence checklist for the new `## Doubt pass` metadata:

- **Atomicity — CHECKED:** Design 6 preserves the existing full-brief temporary-file rename (`skills/spec-brief/SKILL.md:218`).
- **Size bound — FLAGGED:** F-4 covers the unbounded operator reason; other outcome fields have fixed cardinality.
- **Idempotency — CHECKED:** Existing artifact-collision confirmation prevents silent retries from creating duplicate records; the metadata belongs to the single brief.
- **Read-side mode filtering — CHECKED:** Decision 4 makes the section inert; no production/dev record selection is introduced.
- **Schema-version compatibility — CHECKED:** Existing briefs can lack the new section because downstream skills do not consume it.
- **Concurrent writes — CHECKED:** The inherited write contract explicitly documents last-writer-wins and excludes concurrent runs for the same ticket (`skills/spec-brief/SKILL.md:220`).

No Deferred section is present. External failure axes examined include host model metadata, reviewer dispatch and return parsing, operator waiting, source availability, ticket retrieval, and final brief file I/O.

STATUS: RED P0=0 P1=2 P2=1 P3=1 P4=0
