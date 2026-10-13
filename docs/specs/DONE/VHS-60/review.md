# Review gate: VHS-60

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 0 (0 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 2 (1 fixed, 1 recorded)
- Record only: 2

## Findings

1. [Fix or record] A `line N` that belongs to another file gets placed in the spec — skills/spec-cycle/SKILL.md:497
   Problem: a colon locator on a foreign path is never placed, but the words `line`/`lines` are placed against the spec copy whichever file they follow; a placed foreign line then switches off the blank-parent and every-heading fallbacks.
   Disposition: recorded: the fix contradicts the spec, which lists this in `## Deferred (P2+)` as not folded (round-4 edge-cases/F-2); a behaviour change belongs in a follow-up ticket.

2. [Fix or record] "Every delta pass ... still does not dispatch" reads as "delta passes never dispatch" — skills/spec-cycle/SKILL.md:456; docs/spec-workflow-reference.md:81
   Problem: the sentence joins "every delta pass" and "every other incomplete artifact set" under one verb and, read literally, contradicts the delta no-op and the two counters.
   Disposition: fixed

3. [Record only] Workflow reference overstates when the two-file round forces full mode — docs/spec-workflow-reference.md:81
   Problem: it says a later reviewed-marker run selects `mode: full (no baseline)`; the skill narrows this to when the marker records that round and the brief is unchanged.
   Disposition: not acted on

4. [Record only] The "this-spec name" boundary rule is stated only for locators, but the file decision uses the same term — skills/spec-cycle/SKILL.md:495
   Problem: it is unclear whether the boundary rule also governs the file decision two sentences earlier.
   Disposition: not acted on
