# Conventions Review -- round 1

## Findings

### F-1: Scope table omits CLAUDE.md update -- /review-pr description will drift
**Severity:** P2
**Where:** spec.md:9 (Scope table)
**Convention violated:** CLAUDE.md accuracy; VHS-1 precedent (section 3g updated CLAUDE.md when dependency descriptions changed)
**Evidence:** CLAUDE.md line 45 says "resolves threads via `@coderabbitai resolve`" — inaccurate after VHS-3.
**Suggested fix:** Add CLAUDE.md to scope table with description update.

### F-2: "Stale CHANGES_REQUESTED with no findings" edge case not addressed
**Severity:** P3
**Where:** spec.md:148-158 (Edge cases table)
**Convention violated:** Current SKILL.md edge case coverage (line 258)
**Suggested fix:** Add explicit entry.

### F-3: Test command is minimal compared to VHS-1 precedent
**Severity:** P4
**Where:** spec.md:214-217 (Test command)
**Suggested fix:** Consider appending grep checks to the test command.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 1

STATUS: GREEN
