# Correctness Review — VHS-9 Round 1

## Findings

### F-1 (P2): Phase 0 notice text factually incorrect for spec-retire context
spec.md:55 — Notice says "Content recovered from git history" but spec-retire reads from disk, not git history. The recovery language describes spec-reconcile's behavior (which uses `git show`), not spec-retire's.
**Suggested fix:** Change to: "Note: Spec file is untracked (gitignored). Archive step will use mv + git add instead of git mv."

### F-2 (P2): `<project_slug>` undefined — inconsistent with existing SKILL.md's `<project>` variable
spec.md:92 — Introduces `<project_slug>` without defining derivation. Existing SKILL.md uses `<project>`. Wiki project slugs (e.g., `vigil-skills`) don't match states.json prefixes (`VHS`).
**Suggested fix:** Use `<project>` consistently and add resolution note in Stage 2.

### F-3 (P2): Contradictory language about what Phase 2c receives in full-coverage skip case
spec.md:115 vs spec.md:140 — Line 115 says "empty proposals + log.md idempotency check"; line 140 says "archive list and log.md entry." Inconsistent on whether log.md entry is included.
**Suggested fix:** Align both references. Recommend: log.md entry is always compiled by 2c; Phase 4's idempotency check handles dedup.

### F-4 (P3): VHS-9 Plane ticket not found in MCP memory cache
Grounding step — `memory_search` returned zero results. Brief used as canonical source. No impact on review.

### F-5 (P3): Phase 2a and fast-path Stage 2 perform redundant greps
spec.md:83-88 vs SKILL.md:41 — Comprehension/decisions greps are identical in both phases. Redundancy is harmless but undermines token-savings goal.
**Suggested fix:** Note intentional redundancy or reuse 2a results.

STATUS: GREEN
