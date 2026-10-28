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

The `requires:` block above mirrors `grilling`'s, so pre-flight is honest.

## Failure modes

- If this host cannot invoke a nested skill, say `grilling is unavailable in this host` and stop. Never improvise the interview inline.
- On `empty-seed`, report the primitive's one-line reason and stop.
- On `fence-empty`, deliver the Grill summary; its reason line is the answer.
- A fact the check could not settle stays Open as `fact not established`, with the operator's claim in `claim:` when there was one; deliver the summary as usual.
