The spec’s line anchors match the current skill and tests. One git-regex sentence in the fallback passage is false, and the Plane ticket could not be read.

# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: Default `git log --grep` does not treat `(#N)` as a group
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Phase 2a step 2 (the paragraph under the `git log` command)
**Claim:** "`-F` makes the parentheses literal. Git's default basic regex would treat `(#<N>)` as a group and also match a bare `#<N>`."
**Why this is wrong:** That paragraph is part of the Phase 2a passage this spec copies into `skills/spec-close/SKILL.md`. `git log --grep` defaults to basic regular expressions, and in BRE unescaped parentheses are already literal. On git 2.55.0.windows.5, `git log -1 --format=%s --grep="(feat)"` matched nothing, while the same pattern with `-E` matched `feat(vhs-51): … (#36)`. With `-E`, `--grep="(#36)"` also matched a newer commit whose subject is `close(vhs-51): archive spec to DONE/` (bare `#36` in the body). `git log --all -1 --format=%H -F --grep="(#36)"` returned only `8d404d0`, the squash subject that actually contains `(#36)`. The fenced command is the right one; the reason given for it is not. `-F` matters when `grep.patternType` is `extended` (or `-E` is on), not because the default already groups.
**Suggested fix:** Keep `git log --all -1 --format=%H -F --grep="(#<N>)"`. Replace the basic-regex sentence with: default `--grep` is basic and already treats unescaped parentheses as literal; `-F` keeps them literal if pattern type is extended, which would otherwise match a bare `#<N>`.

### F-2: ticket not cached
**Severity:** P3
**Where:** grounding step 3 (Plane ticket VHS-53)
**Claim:** The ticket's description and acceptance criteria are canonical when they conflict with the brief.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-53` returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. No ticket body was available. The review used the brief, which transcribes the Problem and Done when.
**Suggested fix:** None in the spec. Re-check the ticket when the `skills` namespace is readable; until then the brief stays the stand-in.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

STATUS: GREEN
