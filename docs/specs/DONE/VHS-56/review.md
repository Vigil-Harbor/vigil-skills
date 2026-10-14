# Review gate: VHS-56

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 0 (0 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 3 (3 fixed, 0 recorded)
- Record only: 3

## Findings

1. [Fix or record] The per-run identity check fails every dispatch for reviewers whose family is only stated in their config — skills/spec-brief/SKILL.md:167-170, :245
   Problem: Eligibility accepts a family stated in instructions or configuration, but each dispatch fails on a missing run identity, and the skill never says where that identity is read from; such a reviewer passes eligibility and then fails every cycle, leaving only Abort under irreversible.
   Disposition: fixed
2. [Fix or record] § Outcome's rule for `Result` contradicts the failure path's `completed at cap` — skills/spec-brief/SKILL.md:285 vs :306-307, :402
   Problem: After cycle 1 changed the draft and cycle 2 failed (Skip or Accept cycle 1), § Dispatch failure records `completed at cap` but § Outcome yields `completed`, hiding that the last edits were not re-reviewed.
   Disposition: fixed
3. [Fix or record] Sending the prompt "by argument" fails for normal-sized briefs on Windows — skills/spec-brief/SKILL.md:211, :450
   Problem: The prompt carries the full candidate (recent briefs are 19–24 KB); argv dispatch exceeds cmd.exe's 8,191-character limit and the retry fails the same way.
   Disposition: fixed
4. [Record only] Revised decisions have no stated mapping into the candidate — skills/spec-brief/SKILL.md:344, :408, :187
   Problem: After an option-2 revision the agent is told to update affected sections but not whether the fence → Out of scope, renumbering and empty-Settled rules apply to the returned items.
   Disposition: not acted on
5. [Record only] Redundant sentence on when the pass ends — skills/spec-brief/SKILL.md:209
   Problem: "A cycle whose findings were all rejected ends the pass" restates the cycle-2 rule more narrowly and can read as a separate rule.
   Disposition: not acted on
6. [Record only] The frontmatter `description` does not mention the doubt pass — skills/spec-brief/SKILL.md:3
   Problem: README and AGENTS name the doubt pass; the one-line description harnesses load still reads "runs the bounded grilling interview, confirms, and writes".
   Disposition: not acted on
