# Edge-Cases Review — VHS-9 Round 4

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | R3/F-1 | grep -c matches Decisions section | CLOSED | sed-scoped to Wiki-ready |
| edge-cases | R3/F-2 | grep -c "Comprehension" over-match | CLOSED | Same sed scope fix |
| edge-cases | R3/F-3 | state.md cross-project references | CLOSED | Acceptable — false positive = unnecessary derivation |
| edge-cases | R3/F-4 | Forward-compat fallback trigger | CLOSED | sed empty output → all applicable |
| edge-cases | R3/F-5 | Phase 4 em-dash encoding | CLOSED | Consistent with existing SKILL.md usage |

## Findings

### F-1 (P2): Wiki-ready preamble "Decisions and comprehension worth extracting" still matches grep -c "Decision"
The preamble is a fixed template line in the reconciliation report. It means decisions category is always classified as applicable even when no actual decision entries exist in Wiki-ready. Graceful degradation: produces unnecessary but correct derivation.

### F-2 (P3): /tmp/wiki-ready-section.txt not cleaned up
The sed output file persists between runs. Non-issue in practice (overwritten on next run, /tmp is ephemeral) but noted.

### F-3 (P4): Echo delimiters could theoretically appear in filenames
`::COMP::`, `::DECI::`, `::STATE::` — vanishingly unlikely in real wiki file paths.

STATUS: GREEN
