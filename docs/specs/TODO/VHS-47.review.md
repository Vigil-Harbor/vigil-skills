# Review gate: VHS-47

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 0 (0 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 1 (1 fixed, 0 recorded)
- Record only: 3

## Findings

1. [Fix or record] Attest mode is unreachable from Phase 0 — skills/spec-cycle/SKILL.md, Phase 0 "Before anything else" (step 1 to step 2)
   Problem: Nothing in Phase 0 mentions `--attest` or routes to `## Attest mode`; an agent following Phase 0 top to bottom with a spec path halts at step 2 ("Brief not found") or, with a brief path, runs the full review loop and never attests. The "none of steps 2 to 8" rule is stated only in the section the agent never reaches.
   Disposition: fixed — one sentence added at the top of Phase 0: if `--attest` is present, do step 1 only, then go to `## Attest mode`.

2. [Record only] "Then" after a halt reads as a step after halting — skills/spec-tickets/SKILL.md, Phase 4 step 1
   Problem: "…halt with no writes and ask for a new approval. Then read the verdict marker again…" is written as if the marker re-read follows the halt; the intent is "if the spec did not change, also re-read the marker". Suggested: "Otherwise, read".
   Disposition: not acted on

3. [Record only] Attest prompt's `<state line>` is undefined in this skill — skills/spec-cycle/SKILL.md, Attest mode step 5 (`Current verdict: <state line, or none>`)
   Problem: `/spec-tickets` defines a fixed verdict line per state and `/ship-spec` prints `<state> — <one line>`, but `/spec-cycle` names no format, so the line will vary run to run. Cosmetic; the written marker's `replaces:` is specified separately.
   Disposition: not acted on

4. [Record only] Workflow reference orders the two ship-spec checks the other way round — docs/spec-workflow-reference.md, ship-spec Phase 0 step 1
   Problem: The doc says "confirm the sections… Then read the verdict marker"; the skill reads the marker at step 1b, before any section is read (the `## Test command` read is step 4). Both halt either way; only the narration differs.
   Disposition: not acted on
