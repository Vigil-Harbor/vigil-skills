# Conventions Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: Placeholder scan rejects the canonical `TODO` artifact path
**Severity:** P1
**Where:** spec.md:97
**Convention violated:** Project artifacts convention in `AGENTS.md:111`
**Evidence:** `AGENTS.md:111` requires specs, briefs, and reviews under `docs/specs/TODO/<TICKET-ID>.*`, and the live `/spec-cycle` contract uses that path throughout (`skills/spec-cycle/SKILL.md:15`, `:27`, `:386`). The proposed case-insensitive whole-word `TODO` rule excludes fences, blockquotes, and deferred rows, but not inline-code paths. Consequently, active prose such as this spec’s own `docs/specs/TODO/...` references at lines 42 and 71 is classified as an unresolved placeholder.
**Suggested fix:** Exempt inline-code spans and path components from placeholder detection, or recognize `TODO` only in standalone placeholder forms. Add regression cases proving canonical `docs/specs/TODO/...` references pass while genuine TODO prose fails.

### F-2: Checker no longer verifies every brief acceptance criterion
**Severity:** P1
**Where:** spec.md:87, spec.md:96
**Convention violated:** Load-bearing brief Decision 15 and the originating structural-lint contract
**Evidence:** The brief requires the script to check “every acceptance criterion paired with a verify command” (`VHS-26.brief.md:51`, `:63`), matching the recorded sprint decision (`overview/2026-10-11-skill-pack-distillation.md:47`, `:97`). The proposed CLI receives no brief path, and Decision 6 checks only the Done-when items the spec author chose to include, explicitly leaving 1:1 brief mapping to a reviewer. An omitted brief criterion therefore passes the mechanical gate.
**Suggested fix:** Give the checker the resolved brief path and define a deterministic criterion-to-Done-when mapping it can validate, or explicitly return this decision to the operator and amend the brief before review.

### F-3: Divergence still performs the patch pass the brief says to stop
**Severity:** P1
**Where:** spec.md:172, spec.md:225, spec.md:261
**Convention violated:** Load-bearing divergence decision in `VHS-26.brief.md`
**Evidence:** The brief says the loop halts when the blocking count does not decrease (`VHS-26.brief.md:46`) and reaches the scope-reassessment menu “instead of another patch pass” (`VHS-26.brief.md:60`). The spec instead applies all current P0/P1 findings, records the resulting unreviewed edits, and only then halts. That repeats the originating failure mode—an unreviewed remediation introducing new blockers—before the operator can reassess scope.
**Suggested fix:** On a non-decreasing positive total, write the red marker and halt before 2e edits. If preserving dispositions is required, record findings as still open without modifying the spec.

### F-4: Test command is machine-specific in a cross-machine repository
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:248
**Convention violated:** Cross-machine, cross-platform project contract in `AGENTS.md:7` and `AGENTS.md:59`
**Evidence:** The authoritative test command uses PowerShell-only `$env:PYTHONIOENCODING=...` syntax, while the repository describes itself as cross-machine and its existing canonical suite command is shell-neutral: `python -m unittest discover -s tests -p 'test_*.py'`.
**Suggested fix:** Use the existing portable commands directly, or use `python -X utf8` if UTF-8 mode is necessary. Encoding correctness should also be pinned inside the tests rather than depending on a PowerShell environment assignment.

## Summary

P0: 0 | P1: 3 | P2: 1 | P3: 0 | P4: 0

STATUS: RED P0=0 P1=3 P2=1 P3=0 P4=0
