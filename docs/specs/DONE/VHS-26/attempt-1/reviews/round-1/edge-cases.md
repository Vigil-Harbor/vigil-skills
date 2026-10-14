# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: Post-green polish bypasses the immutable ledger
**Severity:** P0
**Where:** spec.md:257
**Edge case:** The green round produces a pre-ship P2 that changes error-message text or another runtime-behavior clarification during existing step 2g.
**What happens:** `ground-truth.md` was frozen before dispatch, but the spec changes afterward and receives a green marker without another checker run or review. The shipped spec can therefore contain a revision-touched runtime claim absent from that dispatched round’s ledger.
**Why the spec misses it:** Done-when item 1 requires every revision-touched runtime-behavior claim in the immutable dispatched-round ledger. The integration list at spec lines 139 and 223 does not cover post-green polish, while `skills/spec-cycle/SKILL.md:939-970` explicitly permits post-dispatch edits including error-message text and forbids reopening review.
**Suggested fix:** Explicitly prohibit 2g from changing or introducing runtime-behavior claims and defer such candidates, or add a post-polish grounding/check/review mechanism consistent with ledger immutability. Add a regression test for a tagged P2 that proposes runtime-behavior wording.

### F-2: First-run ledger preparation has no parent directory
**Severity:** P1
**Where:** spec.md:202
**Edge case:** `/spec-cycle` runs for a ticket whose `.reviews/` directory does not yet exist.
**What happens:** The first step attempts to create `.reviews/.ground-truth.round-<C>.<random>.tmp` before the pending write. The temp creation fails because its parent is absent, so a clean first invocation cannot reach the checker or reviewer dispatch.
**Why the spec misses it:** The ordered flow at spec lines 202-209 prepares and checks the ledger before pending. In the current implementation, creation of `.reviews/` belongs to the later pending-write step at `skills/spec-cycle/SKILL.md:503`. The spec names creation of `round-<C>/` after checking but never moves parent-directory creation ahead of the ledger temp.
**Suggested fix:** Add an explicit idempotent creation of `<TICKET-ID>.reviews/` before ledger-temp preparation, while retaining the guarantee that no round directory or marker is created on checker failure. Test the flow from a tree with no reviews directory.

### F-3: Placeholder scanning rejects canonical `TODO` paths
**Severity:** P1
**Where:** spec.md:97
**Edge case:** A valid spec mentions its canonical artifact path, such as `docs/specs/TODO/<TICKET-ID>.spec.md`, in ordinary prose or inline code.
**What happens:** The case-insensitive whole-word `TODO` rule classifies the directory component as an unresolved placeholder and blocks every retry. This spec itself contains many such active-prose paths, including lines 42, 71, 82, 83, and 146.
**Why the spec misses it:** The exclusions cover fenced code, blockquotes, and the deferred section, but not inline-code path spans or recognized path components. Slash boundaries satisfy a normal whole-word match around `TODO`. Test-plan item 4 has no canonical-path or inline-code false-positive case.
**Suggested fix:** Define placeholder recognition so `TODO` is ignored inside path-like tokens—at minimum the canonical `docs/specs/TODO/` component—while still catching standalone author placeholders. Add positive and negative tests for plain prose, inline code, Windows paths, and canonical artifact paths.

### F-4: Python probing and checker execution can hang indefinitely
**Severity:** P1
**Where:** spec.md:123
**Edge case:** A configured Python command, launcher, filesystem read, or checker process starts but never returns.
**What happens:** `/spec-cycle` hangs before dispatch with no timeout, unavailable-Python fallback, diagnostic, or cleanup path.
**Why the spec misses it:** Decision 7 handles “none can run” and exit codes 1/2, but defines no wall-clock bound for either interpreter probing or checker execution. Existing external git operations in `skills/spec-cycle/SKILL.md` use explicit 30-second timeouts, while the new test plan covers exits and unreadable inputs but not a stalled subprocess.
**Suggested fix:** Specify bounded timeouts for interpreter probes and checker execution, define whether timeout is treated as unavailable or as blocking exit-2 behavior, delete the ledger temp on timeout, and add a stalled-child regression test.

### F-5: Persisted ledger and diagnostics have no size bound
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:40
**Edge case:** A generated ledger contains an excessive number of claims or very large Claim, Spec-locations, or Anchor fields; alternatively, a malformed large spec produces thousands of diagnostics.
**What happens:** The checker and orchestrator may consume excessive memory/context and print unbounded output. Interrupted runs can also leave unbounded random-named ledger temps because cleanup is specified only for handled checker failures.
**Why the spec misses it:** The ledger grammar and report-all diagnostic contract define no file-size, row-count, field-length, diagnostic-count, or stale-temp bound. Test-plan items 6-8 contain no oversized-input case. The persistence checklist requires an explicit bound for each persisted record.
**Suggested fix:** Add practical byte/row/field limits, cap emitted diagnostics while preserving the total error count, define stale ground-truth-temp cleanup on preflight, and test boundary and over-limit inputs.

### F-6: Ticket lookup was unavailable
**Severity:** P3
**Where:** spec § Grounding step 3
**Edge case:** The MCP memory/ticket service and network are unavailable during review.
**What happens:** Current ticket contents and acceptance criteria cannot be independently checked; this review proceeds from the brief as the degraded source.
**Why the spec misses it:** This is an environmental grounding failure rather than a spec defect. The supplied context explicitly states that the service is unavailable.
**Suggested fix:** Re-run ticket grounding when the service is available if canonical ticket content may have changed.

## Summary
P0: 1 | P1: 3 | P2: 1 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=3 P2=1 P3=1 P4=0
