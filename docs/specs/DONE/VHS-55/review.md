# Review gate: VHS-55

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 2 (2 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 1 (1 fixed, 0 recorded)
- Record only: 0

## Findings

1. [Blocks] A review that did not run can still edit the tree — `skills/ship-spec/SKILL.md` irreversible classification and the step 3 subagent prompt
   Problem: The three return tests ran before the subagent's first line, so a helper that printed `ran: no` and then a path plus a problem was treated as a review that ran. The step 3 prompt list did not require that first line.
   Disposition: fixed

2. [Blocks] A clean irreversible review is described as a failure — `skills/ship-spec/SKILL.md` failure mode "Review errors"
   Problem: The bullet said an irreversible command that returned nothing readable as findings halts and does not commit. That sentence also matches a reviewer that states no findings, and a non-zero exit that still prints a location and a problem. Phase 3b treats both as success.
   Disposition: fixed

3. [Fix or record] The reference confirm step cannot change the tier — `docs/spec-workflow-reference.md` Phase 3
   Problem: The confirm sentence still asked only to write, revise an answer, or abort. The skill's menu has a fourth choice, change the tier, and a tweak answer there writes nothing.
   Disposition: fixed
