# Edge-Cases Review — VHS-9 Round 1

## Findings

### F-1 (P1): `<project_slug>` is undefined — state.md grep will use a literal placeholder
spec.md:90 — Introduces `<project_slug>` without defining how to derive it. Wiki project slugs (e.g., `vigil-skills`) don't match Plane prefixes (`VHS`). The state.md grep will always fail, classifying state.md as `missing` and defeating the fast-path.
**Suggested fix:** (a) Add `wiki_slug` to states.json, (b) define resolution rule in Phase 0, or (c) change grep to scan all state.md files: `grep -rl "<TICKET-ID>" "<wiki_root>/projects/" --include="state.md"`.

### F-2 (P2): Full-coverage skip path creates ambiguity about log.md retirement entry
spec.md:115, 140 — Wiki-after-merge writes a merge-event log entry; spec-retire writes a retirement-event log entry with different format. Fast-path's grep matches the merge entry, so retirement entry is never written (Phase 4 idempotency guard skips it).
**Suggested fix:** Use retirement-specific grep marker (`grep -F "retire | <PROJECT> — <TICKET-ID>"`), or always propose the retirement log entry.

### F-3 (P3): grep -rl against non-existent wiki subdirectory
spec.md:84-87 — If `decisions/` or `comprehension/` doesn't exist, grep returns exit 2. With `2>/dev/null` this is handled, but combined-call exit code parsing is underspecified.
**Suggested fix:** Add note that classification is per-command stdout, not combined exit code.

### F-4 (P2): Phase 0 notice says "Content recovered from git history" but spec-retire doesn't do that
spec.md:55 — Same as correctness F-1. Notice text describes spec-reconcile behavior, not spec-retire.

### F-5 (P2): Partial-coverage derivation scoping underspecified for state.md
spec.md:129-131 — "Scoped to missing categories" is ambiguous about whether shared inputs (reconciliation report) are still read.
**Suggested fix:** Clarify that inputs are always read; only the drafting/proposal step is scoped.

### F-6 (P3): Comprehension "Always" applicability causes false `missing` for small tickets
spec.md:71 — Small bug fixes don't produce comprehension entries. If comprehension is always applicable, the fast-path never reaches full-coverage for the most common case.
**Suggested fix:** Make comprehension conditional on reconciliation report flagging architectural changes.

### F-7 (P3): Phase 2a and Phase 2b fast-path redundant greps
spec.md:139 — Same as correctness F-5. Harmless redundancy, explicit preservation per out-of-scope.

STATUS: RED P0=0 P1=1 P2=3 P3=3 P4=0
