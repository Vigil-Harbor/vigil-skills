# Review gate: VHS-66

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 0 (0 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 1 (1 fixed, 0 recorded)
- Record only: 3

## Findings

1. [Fix or record] Two sections give the operator a different number of chances to answer a network approval item — `skills/grilling/SKILL.md` § Bounds (line 208) vs § Fact-finding "Network approval" and § Decisions are the operator's
   Problem: § Bounds said the approval item "is not held for that second cycle", which reads as fewer chances than a normal fact request, while the rule that follows (omit re-asks once, then Open) matches § Fact-finding. An agent reading § Bounds first could Open the item after the first omission without the re-ask.
   Disposition: fixed — dropped "is not held for that second cycle:" so § Bounds states only the shared rule.
2. [Record only] Footer line appears in every round, even rounds with no approval item — `skills/grilling/SKILL.md` § Per-round output contract
   Problem: the new `F<n> yes` / `F<n> approve` sentence sits inside the literal footer block, so it prints in rounds that render no approval item. Matches the spec's "footer lines" scope; reader cost only.
   Disposition: not acted on
3. [Record only] Phase 1 numbered list is split by the per-fact classification paragraphs — `skills/spec-brief/SKILL.md` Phase 1, between steps 3 and 4
   Problem: unindented paragraphs close the ordered list, so some renderers show step 4 as "1." or detach its sub-paragraph. Placement is per spec ("before the dispatch in step 4").
   Disposition: not acted on
4. [Record only] Several rules are stated two or three times in § Fact-finding — `skills/grilling/SKILL.md` § Fact-finding (path:line-is-data, 200-character-cut scope, late-return status, mutation deletion)
   Problem: faithful to the spec, which repeats them and asks for several verbatim; adds roughly 15–20 lines of re-reading per interview. A follow-up could keep each rule in one place.
   Disposition: not acted on
