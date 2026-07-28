# Conventions Review — VHS-9 Round 1

## Findings

### F-1 (P3): Unicode checkmarks/crosses not used in any existing skill
spec lines 107-109, 124-128 — `grep -r "✓\|✗" skills/` returns zero matches. Existing skills use plain text.
**Suggested fix:** Use `[found]`/`[missing]` or keep symbols with fallback note.

### F-2 (P2): Gitignored-spec notice claims "Content recovered from git history" but spec-retire has no such mechanism
spec lines 55-56 — Same root issue as correctness F-1 and edge-cases F-4. Notice describes spec-reconcile behavior.
**Suggested fix:** Change to: "Note: Spec file is untracked (gitignored). Proceeding with on-disk copy."

### F-3 (P2): log.md categorized as Phase 2b "coverage category" but log.md isn't derived in Phase 2b
spec lines 73-74, 92-93, 109, 128 — Phase 2b derives decisions, comprehension, state.md. Log.md is compiled in Phase 2c and written in Phase 4. Blending it into the 2b coverage model misrepresents phase boundaries.
**Suggested fix:** Restructure to separate 2b derivation categories from log.md observation.

### F-4 (P3): `[skip/edit]` prompt format has no precedent
spec line 113 — Existing skills use `[y/N]` format.
**Suggested fix:** Use `[y/N]` pattern or add parenthetical clarification.

### F-5 (P3): Four-category conditional applicability model goes beyond brief
spec lines 29-34, 66-76 — Brief doesn't frame conditional applicability as a formal model. Surfacing for drift-check.

### F-6 (P2): Reconciliation report "Wiki-ready" heading tolerance is a behavioral addition
spec lines 67, 76 — "(or equivalent heading)" tolerance and fallback for absent section are new.
**Suggested fix:** Scope to existing `## Wiki-ready` heading or note as robustness addition.

### F-7 (P4): `2>/dev/null` Windows compatibility
spec lines 53, 83-93 — Consistent with existing SKILL.md precedent. No change needed.

STATUS: GREEN
