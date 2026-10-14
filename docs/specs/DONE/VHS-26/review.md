# Review gate: VHS-26

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 0 (0 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 2 (0 fixed, 2 recorded)
- Record only: 0

## Findings

1. [Fix or record] Only the correctness reviewer knows how to close a "ground-truth ledger missing" finding — skills/spec-cycle/SKILL.md:759 (and the unchanged manifest paragraph at skills/spec-cycle/SKILL.md:598-620)
   Problem: The disposition `fixed: ground-truth ledger to be written at the next dispatch — <path>` carries no `§` anchor, and only the correctness agent has the "closed when the file exists" rule, so another lens following its own step 7 may mark the finding REOPENED. The manifest paragraph still says a disposition is "always with a spec § anchor".
   Disposition: recorded: the fix contradicts the spec — the spec's Test plan requires the manifest-vocabulary paragraph to stay unchanged and the brief fences the edge-cases and scalability agents; the new §2e sentence already says the path stands in for the `§` anchor and that a reviewer closes the finding by checking the file exists.
2. [Fix or record] A "ground-truth ledger missing" finding widens the next delta pass to the whole spec — agents/spec-reviewer-correctness.md:91; skills/spec-cycle/SKILL.md:759 (consumer: unchanged skills/spec-cycle/SKILL.md:522)
   Problem: The finding has no spec site and the agent is not told what to write in `Where`; the existing changed-regions rule emits every current heading for an empty `Where` or one naming another file, so the next delta pass reviews every heading.
   Disposition: recorded: the fix is outside the spec's scope — the brief fences any link between the ground-truth ledger and the changed-regions algorithm, and the spec gives no `Where` rule for this finding. It occurs only after a failed ground-truth-ledger write.
