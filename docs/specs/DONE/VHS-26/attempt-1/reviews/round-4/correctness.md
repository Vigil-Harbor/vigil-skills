# Correctness Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Terminal addenda cannot always be “checked” | CLOSED | Spec § Decision 4, line 79 now distinguishes checker-validated addenda from the unavailable-Python unvalidated exception; Test plan line 267 and Done-when item 1 at line 279 carry the same qualification. |
| correctness | F-2 | Ticket grounding remains unavailable | PARTIAL | Ticket/shared-memory/network access remains unavailable; review proceeded from the brief as required. See F-4. |
| correctness | F-3 | Touched review surfaces changed within the last seven days | PARTIAL | Baseline remains current HEAD `fc20f94`, but `fad52c7`, `f64bebe`, and `d3730b1` still fall within the seven-day freshness window. See F-5. |
| correctness | F-4 | Review-introduced operational contracts remain implicit in the drift check | PARTIAL | The operational contracts remain explicit in the Decisions, but the candidate still adds no grouped operator drift-check item for them. See F-6. |
| edge-cases | F-1 | Duplicate-heading deletion still has no valid tombstone | CLOSED | Spec lines 50–63 and 115 replace leaf headings with full-stack-plus-occurrence identities on the referenced side; duplicate stacks, deletion, and rename are pinned in Test plan item 6 at line 264. |
| edge-cases | F-2 | Terminal gate failures emit a false dispatch message | PARTIAL | Spec lines 134–141 now report preserved reviewer output and rollback rather than claiming no dispatch, but the promised “actual” marker state is restricted to `pending` or `red`, which is not exhaustive. See F-3. |
| edge-cases | F-3 | Ticket lookup remains unavailable | PARTIAL | The external ticket source remains unavailable. See F-4. |
| conventions | F-1 | Review-introduced contracts still need drift-check visibility | PARTIAL | Removed identities, terminal addenda, cleanup, limits, retries, and post-green restrictions remain beyond-brief operational additions without a grouped drift-check note. See F-6. |
| conventions | F-2 | Ticket source remains unavailable | PARTIAL | Ticket/shared-memory/network access remains unavailable. See F-4. |
| conventions | F-3 | Review surfaces remain inside the freshness window | PARTIAL | The same recent commits still touch the workflow and reviewer surfaces. See F-5. |

The closure manifest covers both predecessor blockers with correctly formed lines: `correctness/F-1 (P0)` and `edge-cases/F-1 (P0)`.

## Findings

### F-1: Explicit coverage cannot represent the before-first-heading region
**Severity:** P0  
**Where:** spec.md:50–63, spec.md:115  
**Claim:** Explicit coverage must equal the changed-regions identity set, while every identity is strict JSON whose non-empty `stack` is “the exact full stack of Markdown heading lines.”  
**Why this is wrong:** The live changed-regions contract explicitly treats bytes before the first heading as the pseudo-region `(before first heading)` (`skills/spec-cycle/SKILL.md:480`). A valid spec can contain front matter or prose before its first heading; neither Phase 1 nor the proposed checker forbids it. When that region changes, exact expected coverage includes it, but it has no Markdown heading stack and therefore cannot pass the proposed non-empty-stack parser or current-identity resolution. The author gate becomes unsatisfiable for that valid edit.  
**Suggested fix:** Define a canonical identity for `(before first heading)` on both current and baseline sides, including its removed/changed behavior, checker resolution, correctness-prompt rendering, and tests.

### F-2: The orchestrator cannot observe the retry identity it must compare
**Severity:** P0  
**Where:** spec.md:94–96, spec.md:124–130  
**Claim:** Each validator attaches an “internal, non-printed owner,” and the orchestrator tracks repeated failures by `(code, normalized path, owner)` across separate checker executions.  
**Why this is wrong:** The skill invokes `check_spec.py` through the five-argument CLI, whose only observable diagnostics are code, path, line, and message. The checker never writes, accepts no predecessor-diagnostic input, and runs as a fresh process each time. A deliberately non-printed internal owner cannot cross that process boundary, so the orchestrator cannot distinguish a persisted diagnostic from a different same-code diagnostic after lines shift. Test plan item 8 nevertheless requires stable owner-based retry identity.  
**Suggested fix:** Put a stable owner token in a machine-readable diagnostic field, or define a state/input mechanism that carries prior diagnostic identities into the retry. Update the CLI/output contract and tests accordingly.

### F-3: Terminal messages still cannot always report the actual marker state
**Severity:** P2  
**Pre-ship recommended:** yes  
**Where:** spec.md:134–141  
**Claim:** Terminal rollback messages use `state` equal to the marker’s actual `pending` or `red` value.  
**Why this is wrong:** The live pending write may fail and the run stops only if the marker left on disk is green; a missing or unreadable marker can continue to dispatch (`skills/spec-cycle/SKILL.md:503`). Likewise, a red-marker write failure does not remove the halt menu (`skills/spec-cycle/SKILL.md:801`), so a subsequent grill can run while the marker is still pending, missing, or unreadable. The revised message fixes the prior false “no reviewer dispatched” claim, but its state domain still cannot describe every actual path.  
**Suggested fix:** Render the full marker-reader state—at least `pending`, `red`, `missing`, and `unreadable`—and add final-revision and grill regressions for failed marker writes.

### F-4: Ticket grounding remains unavailable
**Severity:** P3  
**Where:** brief.md:90  
**Claim:** The brief records the canonical Plane ticket and states that it has no acceptance criteria.  
**Why this is wrong:** Ticket/shared-memory/network access was unavailable for this review, so current ticket contents could not be independently verified. The brief was used as degraded authority as instructed.  
**Suggested fix:** Re-run ticket grounding before implementation if the canonical ticket may have changed.

### F-5: Touched workflow surfaces remain inside the freshness window
**Severity:** P3  
**Where:** spec § Scope  
**Claim:** The implementation will modify `/spec-cycle`, two reviewer contracts, workflow documentation, README, and AGENTS.md.  
**Why this is wrong:** Read-only history shows `fad52c7` and `f64bebe` on 2026-10-13 and `d3730b1` on 2026-10-12 touching these surfaces. Fresh reads at baseline `fc20f94026c3b06ca130a1822e157e80bcde533e` confirm the cited live anchors still resolve, so this is a freshness warning rather than demonstrated drift.  
**Suggested fix:** Re-run integration and anchor checks immediately before implementation.

### F-6: Review-introduced contracts still lack grouped drift-check visibility
**Severity:** P3  
**Where:** spec.md:61–79, spec.md:98, spec.md:124–141, spec.md:247  
**Claim:** The candidate adds identity tombstones, terminal addenda, cleanup, resource bounds, retry behavior, terminal rollback messages, and a post-green runtime-claim prohibition.  
**Why this is wrong:** These are reasoned additions, but the spec still does not require a grouped Phase 3 drift-check note that exposes them as contracts added during review rather than carried from the brief.  
**Suggested fix:** Add one concise drift-check item grouping the review-introduced operational contracts for explicit operator acceptance.

## Summary

P0: 2 | P1: 0 | P2: 1 | P3: 3 | P4: 0

STATUS: RED P0=2 P1=0 P2=1 P3=3 P4=0
