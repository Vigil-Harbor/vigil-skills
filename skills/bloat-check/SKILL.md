---
name: bloat-check
description: >
  Mechanical-bloat review of a diff (PR, branch, or working tree): duplicated
  blocks, re-implemented helpers, dead code, copy-paste epilogues, and provable
  shrinks. Every finding is evidence-verified and checked against declared
  design invariants and shape/adversarial test pins before it is reported.
  Use when the user says "bloat check", "duplication pass", "what can be
  deleted", "mechanical bloat", or invokes /bloat-check.
user_invocable: true
requires:
  shell: true
  filesystem: [read]
  subagents: true
---

# /bloat-check — verified mechanical-bloat review

Hunt one thing: code in the diff that provably does not need to exist. Report it dense enough to act on, with the evidence attached. This skill is inspired by ponytail's lazy-review format but adds the two gates that format lacks: every finding must carry verified evidence, and every finding must survive an invariant veto. Precision over volume — a finding that gets reverted costs more than one never filed.

## Scope

In scope (the tags):

- `dup:` a block that is a copy (verbatim or near-verbatim) of code that already exists in the codebase, or a helper that re-implements an existing one line for line. Replacement: call the original.
- `dead:` zero-caller functions, identity functions (return their argument unchanged), unused imports/variables/branches introduced by the diff. Replacement: nothing.
- `epilogue:` the same statement block pasted at multiple exit points of one function. Replacement: a single helper/closure at one seam.
- `stdlib:` a hand-rolled implementation of something the language's standard library ships. Name the exact function.
- `shrink:` same logic, fewer lines, semantics provably identical. Show the shorter form.

Out of scope — route to a normal review pass, never report here:

- Correctness bugs, security holes, performance.
- Design-level YAGNI opinions: abstraction-with-one-implementation, "config nobody sets", speculative flexibility. These require intent judgment, and on hardened code deliberate redundancy is the feature. If one looks egregious, put a single line in a trailing `note:` section, not in the findings.
- Anything whose removal changes observable behavior, however slightly.

## Input parsing

- `/bloat-check 152` or a PR URL → review that PR's diff (fetch it from the code host).
- `/bloat-check <branch>` → diff of that branch against the default branch.
- `/bloat-check` (no arg) → the working diff (staged + unstaged) against HEAD.

## Step 1 — collect context before scanning

Read, in this order, and keep notes on declared invariants:

1. The project's agent instructions (CLAUDE.md / AGENTS.md): any "Key Design Invariants", frozen-export rules, cannot-be-disabled floors, or similar declarations.
2. The full diff.
3. For every symbol the diff touches that you may flag: the surrounding file as it exists on the diff's branch, not the default branch.

Lazy about the solution, never about reading: a duplication claim requires having read both copies; a dead-code claim requires having searched for callers.

## Step 2 — candidate scan

Walk the diff hunk by hunk collecting candidates under the five tags. For diffs over roughly 500 lines, delegate this pass to a subagent per file group and merge the candidate lists; keep only the conclusions in the main context.

## Step 3 — evidence gate (mandatory, per candidate)

A candidate becomes a finding only with recorded proof:

- `dup:` / `epilogue:` — cite both locations and state the match ("line-for-line", "identical except variable name", "N of M lines shared"). Diff-read both; do not trust resemblance from memory.
- `dead:` — a caller search across the whole repo (not just the diff) showing zero call sites, or the function body showing identity. Count call sites for the replacement estimate.
- `stdlib:` — name the exact stdlib function and confirm it covers the hand-rolled behavior including edge cases the code handles.
- `shrink:` — write the shorter form out and confirm it is semantics-preserving (same side-effect ordering, same exception surface, same types).

A candidate that cannot be proven is dropped silently. It does not go in the report hedged with "might".

## Step 4 — invariant veto (mandatory, before reporting)

For each surviving finding:

1. Search the test suite for shape/AST/static tests and adversarial suites that reference the symbol or file. A finding whose fix would trip a pin is vetoed, or re-scoped so the pin survives.
2. Check the finding against the invariants collected in Step 1. Deliberate defense-in-depth redundancy (a floor plus a visible default, a behavioral test plus a shape test, an inline literal a test pins) is not bloat. Veto it.
3. Check findings against each other: if applying finding A breaks the assumption finding B relies on (for example A rewrites a function whose exact source another test pins), report the interaction explicitly instead of listing them as independent cuts.

Vetoed candidates are reported in their own section with the veto reason — one line each. That trail is the difference between "we checked" and "we missed it".

## Output format

One line per finding, then the sections:

```
<file>:L<start>-<end>: <tag>: <what>. <replacement>. [evidence: <proof in a few words>]
```

Then:

```
vetoed:
<file>:L<line>: <tag> candidate — <veto reason in one line>

net: -<N> lines possible.
```

If nothing survives: `Lean already.` and stop.

Report only, by default: do not apply fixes unless the user asks. When asked to apply, re-run the touched tests plus any shape/adversarial suites found in Step 4 before declaring done.

## Tool-use notes

Diff retrieval and caller searches are ordinary shell + file-search operations *(e.g. `gh pr diff` and `Grep` in Claude Code, or the equivalent in your host)*.
