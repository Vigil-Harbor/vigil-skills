# Ground-truth ledger — round 1

New spec: rows cover every section.

- Claim: `/spec-brief` writes only its final brief through its transient atomic-write sibling.
  Spec section: Goal
  Anchor: skills/spec-brief/SKILL.md:218; skills/spec-brief/SKILL.md:256
  Read in round: 1

- Claim: `/spec-brief` returns from the optional `grilling` interview and enters Confirm immediately, with no intervening review step.
  Spec section: Current behavior (grounded)
  Anchor: skills/spec-brief/SKILL.md:160; skills/spec-brief/SKILL.md:162; skills/spec-brief/SKILL.md:166
  Read in round: 1

- Claim: Confirm previews decisions, risks, tier, and the tier basis, then offers write, revise, abort, or change-tier choices.
  Spec section: Current behavior (grounded)
  Anchor: skills/spec-brief/SKILL.md:168; skills/spec-brief/SKILL.md:170; skills/spec-brief/SKILL.md:180
  Read in round: 1

- Claim: The write template emits Tier and optional Scale before Risks / decisions and References, with no doubt-pass record.
  Spec section: Current behavior (grounded)
  Anchor: skills/spec-brief/SKILL.md:186; skills/spec-brief/SKILL.md:188; skills/spec-brief/SKILL.md:202; skills/spec-brief/SKILL.md:205
  Read in round: 1

- Claim: The skill's frontmatter declares `subagents: true`, and the portability lint accepts five named top-level `requires` keys.
  Spec section: Current behavior (grounded)
  Anchor: skills/spec-brief/SKILL.md:5; skills/spec-brief/SKILL.md:9; lint.py:44; lint.py:45
  Read in round: 1

- Claim: The skill limits filesystem mutations to the final brief, its dot-prefixed temporary sibling, creation of `docs/specs/TODO/`, and removal of a stale temporary sibling.
  Spec section: Current behavior (grounded)
  Anchor: skills/spec-brief/SKILL.md:218; skills/spec-brief/SKILL.md:254; skills/spec-brief/SKILL.md:256
  Read in round: 1

- Claim: `/spec-cycle`'s drift checklist parses Decisions, Done when, and Out of scope by heading rather than by a fixed total section count.
  Spec section: Current behavior (grounded)
  Anchor: skills/spec-cycle/SKILL.md:1065; skills/spec-cycle/SKILL.md:1067; skills/spec-cycle/SKILL.md:1070
  Read in round: 1

- Claim: The existing tier gate stops when the host cannot wait for the operator.
  Spec section: Decision 3 — Headless means the host cannot wait at the doubt-pass decision points
  Anchor: skills/spec-brief/SKILL.md:90; skills/spec-brief/SKILL.md:94
  Read in round: 1

- Claim: The current frontmatter provides the subagent capability and the portability lint's five-key vocabulary is authoritative.
  Spec section: Decision 6 — Reuse the declared `subagents` capability
  Anchor: skills/spec-brief/SKILL.md:5; skills/spec-brief/SKILL.md:9; lint.py:44; lint.py:45
  Read in round: 1

- Claim: Confirm's existing menu offers write, revise, abort, and change-tier choices.
  Spec section: 6. Renumber Confirm and Write and make the outcome visible
  Anchor: skills/spec-brief/SKILL.md:170; skills/spec-brief/SKILL.md:176
  Read in round: 1
