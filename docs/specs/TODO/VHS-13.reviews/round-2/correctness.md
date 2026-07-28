# Correctness Review — round 2

## Closure of round 1 findings
All 19 round-1 findings (3× P1, 3× P2, 5× P3 + cross-lens dupes) verified **CLOSED** against the current spec and the live wiki. Key closures:
- correctness/F-1 (P1) — CLOSED. Live-wiki simulation of revised Part E: **0** new findings (0 per-project + 0 fallback), exit 0; baseline `0 errors, 48 flags, 0 warnings, 0 info` matches Test plan 1's figure. Severity → `info` (D10). Done-when 5 redefined to exit-0.
- edge-cases/F-1 (P1) — CLOSED. D11 + Part A.5 require the `## Comprehension`/`## Decisions` header in the `Edit` old_string; hub H2 headers verified unique.
- conventions/F-1 (P1) — CLOSED. "present in any project hub → silent" keeps all attributable cross-lineage entries silent.
No REOPENED items.

## Findings

### F-1: D7 prose "indexed only in the global hub, or nowhere" slightly conflates the two code branches
**Severity:** P3
**Where:** § D7; cross-ref Part E code
D7 reads as if one rule covers both the attributable "global-only/nowhere" case (first branch `dir && !inAnyProjectHub`) and the unattributable "nowhere" case (second branch, pre-existing). Outcomes are correct (0 entries in either cell on the live wiki); code block governs and is unambiguous. Wording precision only.
**Fix (optional):** one clause distinguishing the attributable branch from the unattributable fallback.

### F-2: Recent same-area commit (`9619b58`, PET-118) within 7-day window — no impact
**Severity:** P3
Live wiki HEAD carries `9619b58 docs(wiki): post-merge update for 29e0e95 (PET-118)` + siblings — normal `/wiki-after-merge` outputs that added the PET-118 rows the spec references. Spec anchors verified against present HEAD, not stale. No action.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 0
Verified: revised Part E → 0 new findings (89+35 attributable-in-project-hub silent, 61+47 unattributable-in-surface silent, 0 new-surfacing); exit 0. SCHEMA Part-F anchors (`:299`/`:314`/`:360-361`/`:385`) accurate; lint anchors accurate; H2 headers unique; SHAs exist; PET-111 row present; single-dot project links = 0; `--autofix` unimplemented. All 5 brief Done-when map 1:1.

STATUS: GREEN
