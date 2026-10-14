# Synthesis — round 1

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
- correctness/F-1 (P1) "Placeholder scan rejects canonical spec paths" — sites: 2 — make placeholder recognition path-aware and test the canonical artifact tree.
- correctness/F-2 (P0) "Coverage grammar has no valid empty-set representation" — sites: 3 — add a no-sections form and define its legal use.
- correctness/F-3 (P0) "Line-sensitive diagnostic keys defeat the one-attempt bound" — sites: 2 — identify failures by stable structural identity, not display line.
- correctness/F-4 (P1) "Full-pass reviewers cannot verify declared coverage completeness" — sites: 3 — derive expected coverage independently and pass it to correctness.
- edge-cases/F-1 (P0) "Post-green polish bypasses the immutable ledger" — sites: 3 — forbid 2g from changing runtime-behavior claims.
- edge-cases/F-2 (P1) "First-run ledger preparation has no parent directory" — create the reviews parent before the temp, without creating a round or marker.
- edge-cases/F-3 (P1) "Placeholder scanning rejects canonical `TODO` paths" — sites: 2 — same composed fix as correctness/F-1.
- edge-cases/F-4 (P1) "Python probing and checker execution can hang indefinitely" — sites: 2 — bound probes and checker execution and define timeout cleanup.
- conventions/F-1 (P1) "Placeholder scan rejects the canonical `TODO` artifact path" — sites: 2 — same composed fix as correctness/F-1.
- conventions/F-2 (P1) "Checker no longer verifies every brief acceptance criterion" — sites: 4 — give the checker the brief and compare criterion ordinals/counts.
- conventions/F-3 (P1) "Divergence still performs the patch pass the brief says to stop" — sites: 3 — halt before 2e and accept full-mode re-entry when no disposition ledger exists.

## Consider
(none)

## Noted
- correctness/F-5 (P3) "Ticket not cached" — expected degraded-path environment; brief remains the local authority.
- correctness/F-6 (P3) "Touched review surfaces changed within the last seven days" — re-grounded at current `fc20f94`; implementation must re-check.
- edge-cases/F-5 (P2) "Persisted ledger and diagnostics have no size bound" — fold bounded inputs/output and stale-temp cleanup as pre-ship hardening.
- edge-cases/F-6 (P3) "Ticket lookup was unavailable" — duplicate environmental note for correctness/F-5.
- conventions/F-4 (P2) "Test command is machine-specific in a cross-machine repository" — use shell-neutral `python -X utf8` commands.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Placeholder matcher rejects canonical `docs/specs/TODO/` paths | correctness/F-1; edge-cases/F-3; conventions/F-1 | correctness; edge-cases; conventions | P1; P1; P1 | Act on |
| Coverage cannot represent or independently verify the touched-section set | correctness/F-2; correctness/F-4 | correctness | P0; P1 | Act on |
| Checker retry identity moves with line numbers | correctness/F-3 | correctness | P0 | Act on |
| Post-green polish can add ungrounded runtime behavior | edge-cases/F-1 | edge-cases | P0 | Act on |
| First-run reviews parent is absent | edge-cases/F-2 | edge-cases | P1 | Act on |
| Checker subprocesses have no timeout | edge-cases/F-4 | edge-cases | P1 | Act on |
| Checker does not compare brief criteria | conventions/F-2 | conventions | P1 | Act on |
| Divergence stop happens after the prohibited patch | conventions/F-3 | conventions | P1 | Act on |
| Ticket service unavailable | correctness/F-5; edge-cases/F-6 | correctness; edge-cases | P3; P3 | Noted |
| Recently changed target surfaces | correctness/F-6 | correctness | P3 | Noted |
| Persisted and emitted checker data unbounded | edge-cases/F-5 | edge-cases | P2 | Noted |
| PowerShell-only test command | conventions/F-4 | conventions | P2 | Noted |
