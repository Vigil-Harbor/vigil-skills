# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Placeholder scan rejects canonical spec paths | CLOSED | spec § Decision 6, lines 104–110 exempts slash/backslash-containing path tokens; § Test plan line 251 pins canonical-path coverage. |
| correctness | F-2 | Coverage grammar has no valid empty-set representation | CLOSED | spec § Decision 3, lines 50 and 61–65 defines `coverage: no spec sections` and its exact no-claims form; § Test plan line 253 covers it. |
| correctness | F-3 | Line-sensitive diagnostic keys defeat the one-attempt bound | CLOSED | spec § Decision 7, line 122 keys retries by `(code, normalized path, owner)` rather than display line; § Test plan line 255 covers shifted lines. |
| correctness | F-4 | Full-pass reviewers cannot verify declared coverage completeness | CLOSED | spec § Decision 3, line 63 independently derives `expected_ground_truth_coverage`; § Decision 10, lines 150–162 passes and verifies it in correctness. |
| correctness | F-5 | Ticket not cached | PARTIAL | brief lines 56 and 90 preserve the same-day tracker result and state that the ticket has no acceptance criteria, but the fresh `skills` namespace lookup remains inaccessible to this reviewer. See F-3. |
| correctness | F-6 | Touched review surfaces changed within the last seven days | CLOSED | Fresh reads confirm all cited live anchors still resolve: `sync.py:30`, `sync.py:48-57`, and `skills/spec-cycle/SKILL.md:378`, `:380`, `:388`, `:458`, `:503-513`, `:698`. |
| edge-cases | F-1 | Post-green polish bypasses the immutable ledger | CLOSED | spec § Revision and synthesis integration, line 236 prohibits 2g from adding or changing runtime-behavior claims; § Test plan line 256 pins the restriction. |
| edge-cases | F-2 | First-run ledger preparation has no parent directory | CLOSED | spec § Decision 4, line 73 and § Pre-dispatch flow line 212 create the reviews root before preparing the ledger temp. |
| edge-cases | F-3 | Placeholder scanning rejects canonical `TODO` paths | CLOSED | spec § Decision 6, line 104 exempts path-like tokens; § Test plan line 251 covers slash, backslash, and canonical `docs/specs/TODO/` forms. |
| edge-cases | F-4 | Python probing and checker execution can hang indefinitely | CLOSED | spec § Decision 7, line 130 bounds interpreter probes at 10 seconds and checker runs at 30 seconds, with explicit cleanup and halt behavior. |
| edge-cases | F-5 | Persisted ledger and diagnostics have no size bound | CLOSED | spec lines 75, 94, and 96 bound stale temps, emitted diagnostics, input bytes, claim rows, and field lengths; § Test plan line 255 covers the limits. |
| edge-cases | F-6 | Ticket lookup was unavailable | PARTIAL | The brief remains a usable degraded authority and records the direct tracker read at line 90, but the fresh shared-memory lookup returned an ACL error. See F-3. |
| conventions | F-1 | Placeholder scan rejects the canonical `TODO` artifact path | CLOSED | spec § Decision 6, line 104 exempts whitespace-delimited tokens containing `/` or `\`; § Test plan line 251 adds the canonical artifact-path regression. |
| conventions | F-2 | Checker no longer verifies every brief acceptance criterion | CLOSED | spec § Decision 5, lines 84–89 passes `--brief`; § Decision 6, line 103 requires equal counts, ordinal pairing, and one valid Verify line per spec item. |
| conventions | F-3 | Divergence still performs the patch pass the brief says to stop | CLOSED | spec § Decision 12, lines 176–180 halts before 2e and writes no disposition ledger; § Revision and synthesis integration line 234 repeats that ordering. |
| conventions | F-4 | Test command is machine-specific in a cross-machine repository | CLOSED | spec § Test command, lines 261–264 uses portable `python -X utf8` commands without PowerShell environment syntax. |

## Findings

### F-1: No-Python path skips the required ledger preparation
**Severity:** P0
**Where:** spec.md:220
**Convention violated:** Load-bearing brief Decisions 7 and 14, plus the spec’s own Decisions 4 and 7
**Evidence:** Brief line 43 says a missing or incomplete ledger is blocking, while line 50 permits skipping only the script when Python is unavailable. The spec likewise says the author ledger is still written on that path at line 130 and prepares it in pre-dispatch step 2 at line 213. Line 220 instead says the no-Python path “skips step 2,” which omits ledger preparation while allowing dispatch and contradicts the immutable-artifact contract.
**Suggested fix:** Change line 220 to say the no-Python path skips step 3, not step 2, and explicitly retain preparation and finalization of `ground-truth.md`.

### F-2: Review-driven operational additions need drift-check visibility
**Severity:** P3
**Where:** spec §§ Decision 4, Decision 5, Decision 7, Revision and synthesis integration
**Convention violated:** Silent-additions classification; these are category (c), spec-level additions with rationale
**Evidence:** The revised spec adds stale-temp pruning (line 75), byte/row/field and diagnostic caps (lines 94–96), fixed subprocess timeouts (line 130), and a post-green runtime-claim prohibition (line 236). These are sensible, reasoned responses to round-one findings, but they are more specific than the brief’s carried-forward decisions.
**Suggested fix:** Add a short drift-check note grouping these as review-introduced operational contracts so the operator explicitly accepts them before implementation.

### F-3: Ticket cache remains inaccessible
**Severity:** P3
**Where:** brief.md:90
**Convention violated:** Ticket-grounding fallback
**Evidence:** A fresh tag-only lookup for `plane_work_item` and `VHS-26` in namespace `skills` returned `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. The brief records a direct tracker read from 2026-10-13 and states that the ticket has no acceptance criteria, so review can proceed from the brief.
**Suggested fix:** Restore read access to the `skills` namespace and re-run ticket grounding before implementation if the ticket may have changed.

## Summary

P0: 1 | P1: 0 | P2: 0 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=0 P2=0 P3=2 P4=0
