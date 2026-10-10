# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Newest `(#N)` mention is treated as the squash-merge SHA | CLOSED | spec § Decision 2 (lines 34–36), § Phase 2a step 2 (lines 86–95), § Test plan (line 130): no `-1`; `--exclude=refs/stash`; exactly one accepted line; zero or many do not pick the newest; checklist names a body mention, a revert, a stash, and a second subject |
| edge-cases | F-2 | Non-numeric `<N>` makes `gh` exit 0 for a different PR | DEFERRED | spec § Deferred (P2+) line 159 — not folded; P2+ carry, not a `## Deferred — follow-up required` row |
| edge-cases | F-3 | `-F` rationale is false and points at the regex mode that over-matches | CLOSED | spec § Phase 2a step 2 line 90: default `--grep` is basic and parentheses are already literal; `-F` stops an extended pattern type |
| edge-cases | F-4 | The one warning line collapses distinct `gh` failures | DEFERRED | spec § Deferred (P2+) line 160 — not folded; P2+ carry |
| correctness | F-1 | Default `git log --grep` does not treat `(#N)` as a group | CLOSED | same sentence as edge-cases F-3, spec line 90 |
| correctness | F-2 | ticket not cached | DEFERRED | spec § Deferred (P2+) line 163 — no spec edit; the brief stays the stand-in |
| conventions | F-1 | Spec-level command pins the brief left open | CLOSED | spec § Decision 2 lines 36–37 labels the argv, the append, the `#` strip, and the discarded `gh pr view`; line 90 drops the false "same reach" claim |
| conventions | F-2 | Whole-tree diff allowlist is not the repo's leave-alone form | DEFERRED | spec § Deferred (P2+) line 161 — test command line 139 unchanged, with an explicit not-folded reason |

## Findings

No findings.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 0 | P4: 0

Wiki `projects/vigil-skills/architecture.md` is not present; this review used `filemap.md`, `state.md`, and the overlapping decisions (`2026-10-10-vhs-51-optional-is-a-value-not-a-suffix.md`, `2026-06-14-vhs-17-requires-tolerated-not-strict-yaml.md`, `2026-06-14-vhs-18-lint-warn-only-strict-gate.md`). The spec has no `## Deferred — follow-up required` section. `## Deferred (P2+)` is the spec-cycle P2+ carry; the four round-1 items there are P2/P3 acknowledgments, so they are not re-filed. `vcs-host?` matches `lint.py` `SERVICES_VOCAB` and the VHS-51 decision (services keep a `?` suffix; this ticket is the filed follow-up). Shared-memory lookup for namespace `skills` was denied; the brief's Problem and Done when were used instead.

STATUS: GREEN
