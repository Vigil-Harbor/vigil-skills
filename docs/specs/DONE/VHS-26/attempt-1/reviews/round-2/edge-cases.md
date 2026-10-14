# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Placeholder scan rejects canonical spec paths | CLOSED | spec § Decision 6 line 104 exempts slash/backslash-containing path tokens; § Test plan line 251 covers canonical paths. |
| correctness | F-2 | Coverage grammar has no valid empty-set representation | NEW | `coverage: no spec sections` now handles unchanged passes at lines 50, 61, 65, and 113, but section deletion/rename remains unrepresentable; see F-1. |
| correctness | F-3 | Line-sensitive diagnostic keys defeat the one-attempt bound | CLOSED | spec § Decision 7 line 122 keys retries by stable validator owner rather than display line; § Test plan line 255 covers shifted lines. |
| correctness | F-4 | Full-pass reviewers cannot verify declared coverage completeness | NEW | spec lines 63, 154, and 159 add independently derived expected coverage, but deleted headings emitted by the existing diff algorithm cannot be encoded; see F-1. |
| correctness | F-5 | Ticket not cached | PARTIAL | The memory/ticket service and network remain unavailable; review again used the brief as degraded authority. |
| correctness | F-6 | Touched review surfaces changed within the last seven days | CLOSED | All proposed existing files were reread cold from disk; the spec’s cited live anchors resolve at `sync.py:30`, `sync.py:48-57`, and `skills/spec-cycle/SKILL.md:378`, `:388`, `:503-513`, and `:698`. |
| edge-cases | F-1 | Post-green polish bypasses the immutable ledger | CLOSED | spec § Revision and synthesis integration line 236 forbids post-green changes to runtime behavior; § Test plan line 256 and § Done when line 268 carry the constraint. |
| edge-cases | F-2 | First-run ledger preparation has no parent directory | CLOSED | spec § Decision 4 line 73 and § Pre-dispatch flow line 212 create the ticket reviews root before preparing the ledger temp. |
| edge-cases | F-3 | Placeholder scanning rejects canonical `TODO` paths | CLOSED | spec § Decision 6 line 104 exempts slash/backslash-containing path tokens; § Test plan line 251 includes canonical and Windows-path cases. |
| edge-cases | F-4 | Python probing and checker execution can hang indefinitely | CLOSED | spec § Decision 7 line 130 bounds interpreter probes at 10 seconds and checker runs at 30 seconds, with cleanup and explicit timeout behavior; § Test plan line 255 covers it. |
| edge-cases | F-5 | Persisted ledger and diagnostics have no size bound | CLOSED | spec lines 75 and 94-96 bound stale temps, inputs, claim rows, field lengths, and diagnostic output; § Test plan line 255 covers the limits. |
| edge-cases | F-6 | Ticket lookup was unavailable | PARTIAL | The supplied environment still has no memory/ticket service or network, so canonical ticket contents remain unverified. |
| conventions | F-1 | Placeholder scan rejects the canonical `TODO` artifact path | CLOSED | spec § Decision 6 line 104 exempts path-like tokens and § Test plan line 251 pins canonical `docs/specs/TODO/` behavior. |
| conventions | F-2 | Checker no longer verifies every brief acceptance criterion | CLOSED | spec § Decision 5 lines 84-89 pass the brief; § Decision 6 line 103 compares brief criteria ordinally with spec Done-when items and Verify commands. |
| conventions | F-3 | Divergence still performs the patch pass the brief says to stop | CLOSED | spec § Decision 12 line 180 and § Revision and synthesis integration line 234 halt before 2e without editing or writing a disposition ledger. |
| conventions | F-4 | Test command is machine-specific in a cross-machine repository | CLOSED | spec § Test command lines 262-263 use portable `python -X utf8` module/script commands without PowerShell environment syntax. |

## Findings

### F-1: Deleted headings have no valid coverage representation
**Severity:** P0
**Where:** spec.md:61-63
**Edge case:** A revision deletes a section or renames a heading between the usable predecessor `spec.copy.md` and the next dispatch.
**What happens:** The existing changed-regions algorithm emits the old heading as `deleted: true` (`skills/spec-cycle/SKILL.md:480`), so independently derived expected coverage includes a changed heading that no longer exists. The ledger grammar can only list `§ <heading>` entries, while the checker requires every explicit coverage heading to exist in the current spec. Listing the deleted heading fails structural validation; omitting it fails the correctness reviewer’s exact-coverage comparison. No valid ledger can pass.
**Why the spec misses it:** Decision 3 requires the exact heading set from the existing changed-regions algorithm and simultaneously requires every listed heading to exist, without a tombstone form or a rule excluding deleted headings. The test plan covers explicit coverage forms but not deletion or rename.
**Suggested fix:** Define a coverage tombstone such as `§ <heading> (removed)` and teach the checker and correctness prompt to validate it against the predecessor, or explicitly derive expected coverage from current-side headings only while separately carrying deletions. Add deletion and rename regressions.

### F-2: Unavailable-Python flow skips the ledger it must dispatch
**Severity:** P0
**Where:** spec.md:220
**Edge case:** No configured or ordinary Python 3 interpreter can run.
**What happens:** The pre-dispatch flow says the no-Python path skips step 2, which is preparation of the temporary ground-truth ledger. Later steps must finalize that temp and dispatch its path to correctness, so implementation either stops on a missing temp or dispatches without the mandatory immutable ledger.
**Why the spec misses it:** Line 220 directly contradicts lines 73, 77, and 130, which say the ledger is still prepared, written, and sent to correctness when the checker is skipped, as well as Done-when item 1.
**Suggested fix:** Change line 220 so the no-Python path skips step 3—the checker execution—not step 2. Add an orchestrator-contract test proving ledger preparation/finalization and both correctness inputs remain present when Python is unavailable.

### F-3: Checker-driven spec edits leave expected coverage stale
**Severity:** P1
**Where:** spec.md:122-128; spec.md:210-214
**Edge case:** The first checker run fails, and the allowed fix attempt edits the spec after `expected_ground_truth_coverage` was derived—for example, replacing a placeholder inside a runtime-behavior sentence on an otherwise unchanged re-run.
**What happens:** The retry re-reads changed files but never re-derives the predecessor diff or expected coverage. A pass initially classified as `no spec sections` can therefore retain that stale expectation after the fix changes a section; correctness then compares the ledger against the stale set and can miss the newly concrete runtime claim.
**Why the spec misses it:** The ordered flow derives expected coverage once before preparing and checking the ledger. Decision 7 specifies fixing, rereading, and rerunning, but not recomputing coverage or rebuilding the ledger from the new diff.
**Suggested fix:** After any checker-driven spec edit, recompute expected coverage against the same predecessor snapshot, rebuild or update the temporary ledger, and then rerun the checker. Add a regression beginning with an unchanged pass whose first validation repair changes a runtime-behavior sentence.

### F-4: Ticket lookup remains unavailable
**Severity:** P3
**Where:** brief.md:90
**Edge case:** The MCP memory/ticket service and network are unavailable during review.
**What happens:** Current Plane ticket contents and acceptance criteria cannot be independently checked; this pass relies on the brief as the degraded authority.
**Why the spec misses it:** This is an environmental grounding failure, not a defect in the proposed design.
**Suggested fix:** Re-run ticket grounding when the service is available if canonical ticket content may have changed.

## Summary

P0: 2 | P1: 1 | P2: 0 | P3: 1 | P4: 0

STATUS: RED P0=2 P1=1 P2=0 P3=1 P4=0
