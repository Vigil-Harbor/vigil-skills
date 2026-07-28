# Conventions Review — VHS-8 Round 2

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | R1/F-1 | `--force` flag silent addition | CLOSED | Flag removed, Decision 4 explicit |
| conventions | R1/F-2 | Runtime list_states vs VHS-1 caching | DEFERRED | Line 455 with rationale |
| conventions | R1/F-3 | Missing "Invoked as:" convention | CLOSED | Lines 93, 211 |
| conventions | R1/F-4 | SCHEMA.md template names not cited | CLOSED | Lines 276, 278 cite specific templates |
| conventions | R1/F-5 | Report format not anchored | DEFERRED | Line 451 |
| conventions | R1/F-6 | `retire` action tag not in SCHEMA.md | DEFERRED | Line 452 |
| conventions | R1/F-7 | Test command minimal | CLOSED | Acceptable for markdown-only repo |
| conventions | R1/F-8 | No Windows path handling | CLOSED | Agent handles at runtime |

## Findings

### F-1 (P2): log.md heading format omits commit hash

Existing log.md entries universally include `(<short-sha>)` or `(<short-sha>, PR #N)` in the heading. Spec's proposed format uses `(archived from TODO/)` instead. The merge SHA is available from the reconciliation report — including it would be more consistent.

### F-2 (P3): Deferred section is a new spec-level convention

The `## Deferred (P2+)` section doesn't exist in other specs. Useful for traceability but worth noting as a new convention.

### F-3 (P4): CLAUDE.md heading rename — ensure exact match of current heading text

The rename instruction should quote the current heading exactly to ensure Edit tool succeeds.

### F-4 (P3): Wiki path with spaces in grep commands

Phase 2a grep examples use unquoted `<wiki_root>` paths. Should use quotes for Windows compatibility.

STATUS: GREEN
