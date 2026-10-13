# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: Concurrent invocations can invalidate the two-file exception

**Severity:** P1  
**Where:** spec § Round-artifact state machine; spec.md:198-212  
**Edge case:** Two `/spec-cycle` invocations for the same ticket reserve the same absent round span concurrently; one obtains a valid snapshot while the other takes the new snapshot-failure path.  
**What happens:** The random temp names avoid temp collisions, but both invocations rename over the same fixed destinations. The successful invocation can create `baseline.commit` while the failing invocation writes its two copies, or the copies can come from different invocations. Both can then dispatch into the same round directory and overwrite reports, ledgers, and the verdict marker. Most directly, a snapshot-failure round can end with a `baseline.commit`, causing the next run to enter delta mode despite Decision 2 requiring `mode: full (no baseline)`. Review evidence may no longer correspond to one coherent spec/brief/snapshot.  
**Why the spec misses it:** The current skill reserves a span by checking directory absence and later renames over fixed artifact paths (`skills/spec-cycle/SKILL.md:377`, `:443-455`); it has no ticket-scoped lock or atomic ownership claim. The new persisted two-file state relies on absence of `baseline.commit` as its discriminator, but the spec does not protect that absence from another writer.  
**Suggested fix:** Add a ticket-scoped single-writer mechanism or atomic round-span ownership claim before artifact work, with defined stale-owner recovery, and add a scenario where two invocations race across valid-snapshot and failed-snapshot branches. Require the losing invocation to stop before writing pending, artifacts, reports, or a marker.

### F-2: First-rename failure can leave an orphaned temp

**Severity:** P2  
**Pre-ship recommended:** yes  
**Where:** spec.md:198; spec § Test plan, lines 356-360  
**Edge case:** Both copy temps have been written, then renaming `spec.copy.md` fails before either rename succeeds.  
**What happens:** Two temps remain unrenamed, but the exact replacement says only to “delete an unrenamed temp.” A literal implementation may remove one and leave the other behind, contradicting the test-plan requirement that no dot-prefixed temp remain after any exercised artifact write. The run stops safely, but stale files accumulate.  
**Why the spec misses it:** The prose uses a singular cleanup instruction even though its write-all-temps-first protocol can leave two or three unrenamed temps at once.  
**Suggested fix:** Change the exact replacement to “delete every unrenamed temp created by this artifact-write attempt,” and walk failures at temp creation, temp write, and each rename position.

### F-3: Ticket grounding was unavailable

**Severity:** P3  
**Where:** review grounding step  
**Edge case:** Shared memory and Plane were unreachable.  
**What happens:** The review could not independently compare the brief and spec with the current VHS-60 tracker record or comments. It proceeded through the documented brief-only degradation path.  
**Why the spec misses it:** This is an external review-environment outage, not a defect in the proposed implementation.  
**Suggested fix:** Restore the ticket-memory integration for a later pass if independent ticket verification is required; otherwise retain the brief as authority as documented.

## Summary

P0: 0 | P1: 1 | P2: 1 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=1 P3=1 P4=0
