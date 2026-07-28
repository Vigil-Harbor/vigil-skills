# VHS-6 Round 1 — Correctness Review

## Findings

### F-1 (P0): `git symbolic-ref --short` returns wrong format for downstream use

**Location:** Design step 4b (line 99-102), referenced throughout steps 4e-4g.

`git symbolic-ref --short refs/remotes/upstream/HEAD` returns `upstream/main`, not `main`. The spec uses `upstream/<branch>` in downstream commands (e.g., `git log upstream/<branch>`), which would expand to `upstream/upstream/main` — a nonexistent ref.

Ship-spec's Phase 0 step 5 handles this correctly with `sed 's|^refs/remotes/origin/||'` (non-short form + sed strip). The spec should either:
- Use non-short form and strip with sed, or
- Use `--short` and strip the `upstream/` prefix explicitly.

### F-2 (P1): D4 regex vs step 4d regex discrepancy

**Location:** Decision D4 (line 47) vs Design step 4d (line 112).

D4 describes: `[A-Za-z0-9_./+-]+\.[a-z]{1,4}` with a filter "contains `/` or ends with a code extension."

Step 4d describes: same regex but then lists a hardcoded set of code extensions (`.ts`, `.js`, `.py`, `.md`, etc.). The Decision text says "ends with a code extension" generically; the Design text pins specific extensions. These should be aligned — the Design is more precise and should be the source of truth, but D4 should reflect it.

### F-3 (P1): Brief acceptance criterion #8 unmapped

**Location:** Brief acceptance criteria, spec Done-when section.

Brief criterion #8 calls for "actual run log output" in validation (three concrete briefs producing verifiable log lines). The spec's Test plan (lines 186-222) has empirical validation items (tests 6-8) but does not specify that their output should be captured or that the spec's test command should produce those log lines. The Done-when section lacks a criterion mapping to "actual run log output."

### F-4 (P2): `AskUserQuestion` is not a real Claude Code tool

**Location:** Design step 4g (line 138-152), Decision D6 (line 65-69).

`AskUserQuestion` is described as a tool call, but it is not a standard Claude Code tool. The spec should describe this as a conversational prompt — the LLM presents findings and asks the user inline, which is the standard Claude Code pattern for interactive decisions.

### F-5 (P2): Test command may not verify all Done-when criteria

**Location:** Test command (line 227-228) vs Done-when (lines 234-245).

The test command uses `grep -c` to verify presence of keywords but cannot verify semantic correctness of the step logic. This is expected for a skill file with no executable test suite, but should be acknowledged.

### F-6 (P2): Step 4h is redundant

**Location:** Design step 4h (line 154).

Step 4h says "No commits found: (Covered by step 4e's empty-result branch.)" — this is purely a comment restating 4e. It adds no behavior. Consider removing or folding into 4e's description.

### F-7 (P3): Minor — "stdin halt" terminology in D6

Decision D6 title says "Halt on stdin" but body clarifies this maps to the LLM's interactive prompt, not literal stdin. The title could be clearer.

## Summary

The spec is well-structured and covers the brief's requirements comprehensively. The critical issue is the `git symbolic-ref --short` format bug (F-1) which would cause every downstream git command to fail on a real fork. The regex alignment (F-2) and unmapped criterion (F-3) are secondary but should be addressed.

STATUS: RED P0=1 P1=2 P2=3 P3=1
