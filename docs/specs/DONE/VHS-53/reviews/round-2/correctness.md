The fallback command matches the current skill and git’s actual `%x09` output. Round-1 blockers are closed; the Plane ticket is still unreadable.

# Correctness Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Default `git log --grep` does not treat `(#N)` as a group | CLOSED | spec § Phase 2a step 2, line 90: default `--grep` is basic regex and unescaped parentheses are already literal; `-F` is what stops `grep.patternType=extended` or an `-E` flag. The fenced command at line 87 still passes `-F`. |
| correctness | F-2 | ticket not cached | REOPENED | `memory_search` on namespace `skills` still returns `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. Spec § Deferred (P2+) line 163 records no edit. That heading is not `## Deferred — follow-up required`, so there is no well-formed `D-<n>` row. Not escalated: round-1 suggested fix was none in the spec, and this run caps the denial at P3. Re-noted below. |
| edge-cases | F-1 | Newest `(#N)` mention is treated as the squash-merge SHA | CLOSED | spec lines 80–95 drop `-1`, use `git --no-pager log --exclude=refs/stash --all --format=%H%x09%P%x09%s -F --grep="(#<N>)"`, accept only one 40- or 64-hex SHA with exactly one parent and a subject ending in ` (#<N>)`, and send zero, many, or a non-zero exit to the step 1c prompt. Checklist line 130 matches. On git 2.55.0.windows.5, that format emits byte 9 between fields; `8d404d0` has one parent and its subject ends with ` (#36)`. |
| edge-cases | F-2 | Non-numeric `<N>` makes `gh` exit 0 for a different PR | REOPENED | spec line 74 still strips only one leading `#` and adds no digits check. Spec line 159 says not folded. Deliberate: spec § Out of scope line 150 leaves the existing PR-number versus SHA branch unclassified, matching brief decision 2 (fallback only) and brief Out of scope (no new step-1 strategy). Original severity was P2; not re-filed here. |
| edge-cases | F-3 | `-F` rationale is false and points at the regex mode that over-matches | CLOSED | Same sentence as correctness F-1, spec line 90. The command keeps `-F` and does not add `-E`. |
| edge-cases | F-4 | The one warning line collapses distinct `gh` failures | REOPENED | spec lines 82–84 still print one fixed `gh absent or failed` line and line 78 still says not to parse stderr. Spec line 160 says not folded. Deliberate: brief decision 2 settles one warning line that names `gh`. Original severity was P3; not re-filed here. |
| conventions | F-1 | Spec-level command pins the brief left open | CLOSED | spec § Decision 2 line 36 names the pins the brief left open (`--exclude=refs/stash`, `-F`, subject ending, exactly one parent, leading-`#` strip, discard view when diff fails). Line 90 drops the false “same reach as step 1a” claim and states that step 1a passes `-- .` (`skills/spec-close/SKILL.md:74`) and this command does not. |
| conventions | F-2 | Whole-tree diff allowlist is not the repo's leave-alone form | REOPENED | spec § Test command line 139 is still `git diff --name-only origin/main` filtered to the two files. Spec line 161 says not folded because this run requires that allowlist. Deliberate non-change of a P3; not a correctness defect and not re-filed here. |

`8d404d0` (2026-10-10) touches `tests/test_spec_close_log.py` only around the backlog-wording test. `TestSkillDeclaration` is still at lines 1178–1191, which is what the spec cites. `skills/spec-close/SKILL.md` was not in that commit. Cited anchors match the current files: requires at lines 5–9, Phase 2a step 2 at 78–81, tool-use bullet at 430, failure-mode bullet at 440, Bash bullet at 433, step 3 at 83. `lint.py` `SERVICES_VOCAB` includes `vcs-host`, and `docs/portability-contract.md` §3 line 65 already defines the `?` suffix.

## Findings

### F-1: ticket not cached
**Severity:** P3
**Where:** grounding step 3 (Plane ticket VHS-53)
**Claim:** The ticket's description and acceptance criteria are canonical when they conflict with the brief.
**Why this is wrong:** `memory_search` with `namespace: skills`, `tags: ["plane_work_item", "VHS-53"]`, `source_system: plane`, `max_results: 1` returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. No ticket body was available. The review used the brief, which transcribes the Problem and Done when. The spec's Done when (line 144) matches that brief sentence, and nothing in the brief conflicts with the design that was checked against the code.
**Suggested fix:** None in the spec. Re-check the ticket when the `skills` namespace is readable; until then the brief stays the stand-in.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
