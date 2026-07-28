# VHS-6 Round 1 — Conventions Review

## Findings

### F-1 (P2): `AskUserQuestion` is not a Claude Code tool

**Location:** Design step 4g (line 138), Decision D6 (line 65-69).

The spec references `AskUserQuestion` as a tool call. This tool does not exist in Claude Code's standard toolset. The conventional pattern for interactive prompts in Claude Code skills is to present the information conversationally and wait for user input — the LLM naturally pauses for the user to respond. The spec should describe this as "present findings and ask the user" rather than referencing a specific tool.

Ship-spec's Phase 3 test-gate uses the same pattern: "What would you like to do? 1. Continue... 2. Drop into manual debug... 3. Roll back..." — no tool call, just conversational prompting.

### F-2 (P3): Spec mirrors ship-spec's `sed` pattern for default-branch detection but uses a different approach

Ship-spec Phase 0 step 5 uses `git symbolic-ref refs/remotes/origin/HEAD | sed 's|^refs/remotes/origin/||'` (long form + sed). This spec uses `git symbolic-ref --short` (short form) which returns `upstream/main` not `main`. While not a convention violation per se (different remote, different context), aligning with the established pattern would be more consistent.

### F-3 (P3): Good — env var naming follows convention

`SPEC_CYCLE_UPSTREAM_WINDOW` follows the `SPEC_CYCLE_` prefix convention for spec-cycle-scoped configuration.

### F-4 (P3): Good — failure modes section follows existing pattern

The two new failure-mode bullets match the style and tone of the existing bullets in the spec-cycle SKILL.md.

### F-5 (P3): Good — step renumbering approach is clean

Inserting as step 4 and renumbering 4→5, 5→6 is the cleanest approach. The grep audit (`grep -r "Phase 0 step" skills/ agents/`) confirming no external references to step numbers is good practice.

### F-6 (P4): Consider whether "Halt on staleness" heading in step 4g should use the same "HARD STOP" language as Phase 3

Phase 3's drift-check uses "HARD STOP" terminology. The upstream staleness halt is a softer gate (user can proceed). The current "Halt on staleness" is appropriately differentiated.

### F-7 (P4): Step 4h could be removed

Step 4h is a comment ("No commits found: Covered by step 4e's empty-result branch."). It adds no behavior. Convention in existing skills is to avoid no-op steps.

## Summary

The spec follows repo conventions well. The main concern is the `AskUserQuestion` tool reference (F-1), which should be replaced with the standard conversational prompt pattern. The symbolic-ref approach (F-2) is a consistency suggestion, not a convention violation.

STATUS: GREEN
