# Review gate: VHS-27

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 0 (0 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 4 (2 fixed, 2 recorded)
- Record only: 6

## Findings

1. [Fix or record] The final-pass paragraph says there is no next closure manifest, but the new ledger is one — skills/spec-cycle/SKILL.md:765
   Problem: an agent following the condensed sentence writes a final-pass ledger without the rejection, fold and deferral lines, and the next delta pass 1 files a missing-line finding.
   Disposition: fixed
2. [Fix or record] First-invocation rule text was rewritten shorter, not only re-indexed — skills/spec-cycle/SKILL.md:695, 753-754, 765, 794
   Problem: the spec leaves that loop unchanged. Lost: the red-marker field list, "option 4 leaves the marker untouched", the halt-title suffix formats, the revert manifest line's severity and title, and "do not run 2g".
   Disposition: fixed
3. [Fix or record] A full pass now cannot dispatch when the commit snapshot fails — skills/spec-cycle/SKILL.md:453
   Problem: a first invocation in a project with no commits or no git can no longer review, and no stop line is defined; the unchanged preflight treats git failure as non-fatal.
   Disposition: recorded: the fix contradicts the spec (§ Artifacts requires the complete three-file set before dispatch); added to follow-up ticket VHS-60
4. [Fix or record] The mode table has no row for an absent spec file — skills/spec-cycle/SKILL.md:353-379
   Problem: deleting the spec to force a re-author, with a review marker and intact baseline, resolves delta mode for a freshly authored spec.
   Disposition: recorded: the fix is outside the spec's scope (§ Mode has no such row); added to follow-up ticket VHS-60
5. [Record only] No-op step 4 switches the mode after the preflight line already printed delta — skills/spec-cycle/SKILL.md:417
   Problem: nothing tells the agent to print the replacement token.
   Disposition: not acted on
6. [Record only] "with no leading" reads as banning the four characters only at line start — skills/spec-cycle/SKILL.md:488
   Problem: the spec bans a leading quote and any `=>`, tab or backslash anywhere.
   Disposition: not acted on
7. [Record only] The Anchor-drift paragraph is glued under a bullet — agents/spec-reviewer-correctness.md:110
   Problem: no blank line before it, so Markdown reads it as part of the Implementation-gap bullet.
   Disposition: not acted on
8. [Record only] Unrelated facts deleted while counters were reworded — docs/spec-workflow-reference.md:98, 112, 310
   Problem: the re-file rule and synthesis buckets, attest's checks, and the convergence rationale sentence are gone.
   Disposition: not acted on
9. [Record only] Stale leftovers — skills/spec-cycle/SKILL.md:1038, :57
   Problem: "steps 2 to 9" where step 10 now exists; "before round 1" where the first dispatch can be any cumulative round.
   Disposition: not acted on
10. [Record only] README usage line lacks `--full` — README.md:10
    Problem: not in the diff and not in the spec's Scope table.
    Disposition: not acted on
