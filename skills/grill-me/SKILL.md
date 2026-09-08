---
name: grill-me
description: Interview me on a plan, decision, or idea until the design tree is settled or a bound is hit. Ad-hoc — produces no lifecycle artifact. Use when the user says "grill me", "stress-test this", "poke holes in this plan".
user_invocable: true
requires:
  subagents: true
  filesystem: [read]
---

# /grill-me — an ad-hoc bounded interview

Invoked as: `/grill-me <topic>`.

Run the `grilling` skill (Claude Code: invoke it through the skill-invocation tool, or the equivalent in your host) with `seed` = the topic the user gave, brief altitude, and the default bounds (3 rounds, 7 questions). When it hands back, the Grill summary is the deliverable — write nothing to disk.

The `requires:` block above mirrors `grilling`'s: it declares what the delegate needs, so pre-flight is honest.

## Failure modes

- If this host cannot invoke a nested skill, say so and stop: `grilling is unavailable in this host`. Never improvise the interview inline — the bounds live in the primitive.
- On `empty-seed` (no topic, or a topic with nothing to decide), report the primitive's one-line reason and stop — there is no summary to deliver.
- On `fence-empty` (the topic has a root decision but nothing about it is askable at brief altitude), deliver the Grill summary as usual — its header's reason line is the answer.
- On a fact the check could not settle — this host offers no read-restricted agent class, the claim has no repo footprint, the check came back `not found`, empty, errored, or only partly supporting, or the round's check batch was too full to take it — the primitive leaves the fact Open and labelled `(operator claim, unverified)` instead of establishing it. Deliver the Grill summary as usual; the label is the answer, and the claim travels with it in the item's `claim:` field.
