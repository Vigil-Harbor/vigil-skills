# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: Malformed-brief halt and the re-run pin cannot both be true
**Severity:** P0
**Where:** spec § spec-cycle, lines 175–179; Done when, line 295
**Edge case:** A spec already has a valid `**Tier:**` line, and a later `/spec-cycle` sees a brief whose `## Tier` section is malformed (no `**Level:**` line, `tweak`, unknown token, or a looser `tier` heading whose body contains a `**Level:**` line).
**What happens:** The Level step and the looser-heading rule halt, write no marker, and leave the existing marker. The re-run pin in the next paragraph says that same malformed brief does not halt: the recorded line is authoritative and the run warns `tier: brief malformed — using recorded`. Done when says a malformed `## Tier` always halts, with no recorded-line exception. One of those three instructions is wrong no matter which the implementer codes. The safe coding (always halt) makes the pin's "using recorded" path unreachable, so a typo in the brief blocks re-review of a spec that already records `irreversible`. The pin coding (continue) violates Done when.
**Why the spec misses it:** The halt is inside the numbered brief parse and has no "unless a recorded line exists" guard. The pin is a later override that names `malformed` but never amends the halt or Done when.
**Suggested fix:** Parse the recorded spec line first. A valid recorded line wins over an absent, disagreeing, or malformed brief: warn and continue, do not halt. Halt a malformed brief only when the spec has no valid recorded line. Halt a recorded line outside `small|big|irreversible` without falling through to the brief. State that same partition in Done when.

### F-2: A near-miss `**Tier:**` line is read as absent `big`
**Severity:** P1
**Where:** spec § Reader rule for the spec line, line 183; Decision 9, lines 62–63; ship-spec, line 229; attest, line 223
**Edge case:** The only tier declaration is a labeled line the whole-line regex does not accept: `**tier:** irreversible` (label case), or `**Tier:** irreversible — unskippable gate` (trailing words). A token with the punctuation stuck to it, such as `irreversible.`, does match and halts.
**What happens:** The line is not a candidate, so spec-cycle's re-run pin, attest mode, and ship-spec all take "no line" and set `big` with no warning. An intended `irreversible` spec skips the review gate whenever the three Phase 3b cases skip. A trailing-note `small` is likewise reviewed and shipped as `big` (`round_cap` 4, review gate not skipped). Brief Decision 12's rule that an intended `irreversible` is never silently read as `big` is broken. The brief parser does not have this hole: a present `## Tier` section with a bad or missing level halts.
**Why the spec misses it:** Absence is defined as "regex did not match", and the regex requires a case-sensitive `**Tier:**` label and end-of-line immediately after one token. Test-plan item 5 only carves out fenced lines and mid-sentence mentions, not a labeled line with a suffix or a lowercase label.
**Suggested fix:** Treat a line whose label is `**Tier:**` case-insensitively as present. If the rest is not exactly `small`, `big`, or `irreversible` after lowercasing and trim, halt `tier: malformed (<line>)` in spec-cycle, attest, and ship-spec. Do not default that line to `big`. Keep ignoring real prose that has no `**Tier:**` label, and keep ignoring fenced copies.

### F-3: A clean irreversible review is specified as the failed halt
**Severity:** P1
**Where:** spec § ship-spec, Decision 8 and Phase 3b, lines 60–61 and 243–251; `skills/ship-spec/SKILL.md:195`
**Edge case:** Tier is `irreversible`, the review command runs, and it found nothing (today's success path: go to step 8 and write `## Findings` / `None.`). Same gap if the only reading of "returns nothing readable" swallows that result.
**What happens:** The halt predicate is "errors or returns nothing readable", and the only success sentence is "when the command returns readable findings, steps 4 to 8 run". A review that ran and found nothing returns no findings, so it is not that success sentence. The nearest specified bucket is `<command> failed`: no review file, no Phase 4, nothing committed. Irreversible cannot ship the normal clean review. The non-zero-exit carve-out on the same skill line is covered only if "readable findings" is read generously; the found-nothing carve-out is not.
**Why the spec misses it:** Decision 8 cites `SKILL.md:187-195`, which contains both carve-outs, then restates success more narrowly than that paragraph and restates the third skip as "nothing readable" without repeating "found nothing is step 8".
**Suggested fix:** For `irreversible`, keep both carve-outs: a non-zero exit that still returns readable findings continues into steps 4–8, and a review that ran and found nothing is success (step 8, zero counts, `None.`), not `<command> failed`. Halt only for no command, command not available (including the step-3 "command not found" come-back), or a return that is an error or not a findings report.

### F-4: Irreversible re-run stops on the leftover worktree
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § ship-spec, lines 243–248; `skills/ship-spec/SKILL.md:107-119`
**Edge case:** The irreversible halt fires after Phase 1 has created `<TICKET-ID>-worktree` and the branch, with tests possibly green and the implementation uncommitted. The operator repairs the review command and re-runs `/ship-spec`, which the halt text says to do.
**What happens:** Phase 1 halts because the worktree path already exists, and again because the branch exists. The gate is never reached. The worktree halt suggests `git worktree remove` and `--force` if the directory is broken; a dirty tree needs `--force`, which deletes the only copy of the implementation. The irreversible halt does not print the worktree path (step 6 option 3 does).
**Why the spec misses it:** The resume sentence is "re-run /ship-spec" and does not mention Phase 1's two pre-create checks or that this halt leaves a dirty worktree.
**Suggested fix:** In the halt text, name `<worktree-path>` and `<branch>`, and say a re-run stops on both until the operator removes them (implementation is not in the primary tree) or explicitly reuses that worktree. Do not imply a second invocation resumes Phase 3b by itself.

### F-5: Failure-mode bullets still say a failed review never halts
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § ship-spec, line 253; `skills/ship-spec/SKILL.md:432-433`
**Edge case:** Tier is `irreversible` and the review command is missing, unavailable, or failed. The implementer treats the Failure modes section as the rule for those cases.
**What happens:** Those bullets say skip, record, and "Never halt for it." Phase 3b as specified halts. The spec preserves the `:432-433` wording for `big` and an absent line, and never says to add an irreversible exception, so the skill text contradicts the new halt. Following the failure-mode bullets commits past the skipped gate.
**Why the spec misses it:** The irreversible edit list stops at the Phase 3b steps. The "never halt" sentences are mentioned only so `big` keeps them.
**Suggested fix:** Change those two failure-mode bullets so `irreversible` halts with the Phase 3b case text and does not commit, and `big` / absent keep today's skip.

### F-6: At `round_cap = 2`, FROZEN ignores the round that reviewed the revision
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § `round_cap` substitution, lines 54–56 and 202–203; `skills/spec-cycle/SKILL.md:555-558`
**Edge case:** Tier is `small` (`round_cap = 2`). Round 1 is red and revises. Round 2's review files a P0/P1 in a section that had none in round 1. The round is still red, so 2e takes the rewrite branch.
**What happens:** FROZEN is "no unresolved P0/P1 across rounds `1 .. round_cap−1`", which is round 1 only. That section is FROZEN and copied verbatim. REWRITE is "has unresolved P0/P1" with no statement that the current round counts. A literal reading freezes the section round 2 just failed, so the rewrite does not apply the only review of the revised spec. The loop still halts red (the rewrite is not re-reviewed), but the halt's spec does not contain the round-2 fix.
**Why the spec misses it:** The substitution replaces "rounds 1–3" with `1 .. round_cap−1` and does not say the current round's findings force REWRITE. With four rounds the final round is a minority; with two it is half the loop and the only look at the revision.
**Suggested fix:** State that a section is REWRITE if the current round (`round == round_cap`) has an unresolved P0/P1 in it, and FROZEN only if neither the prior rounds nor the current round do. Add that sentence to the line-555 replacement.

### F-7: `round_cap = 2` leaves the grill-apply rules and the grilling cap bound to the wrong 4
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § `round_cap` substitution, lines 189–215; `skills/spec-cycle/SKILL.md:646` and `:672`
**Edge case:** `round_cap` is 2, the loop halts after round 2, and the operator picks menu option 4. Separately, the review-loop variable and the grilling argument share the name `round_cap`.
**What happens:** The substitution table says rewrite those lines and no other numerals. Line 672 is not in the table, so grill-apply still says "under the 2e rounds-1–3 rules" after that heading has been rewritten to `rounds 1 .. round_cap−1`. There is no rounds-1–3 block when the cap is 2, so the apply step has no target and grill decisions can be dropped while the red marker stays. Line 646 stays `` `round_cap` 3 ``. If that identifier is the variable just set to 2, the post-halt interview runs with cap 2 instead of its own cap of 3.
**Why the spec misses it:** The table covers the round-4 phrases inside 2f-i paths but not the "rounds-1–3 rules" cross-reference. The grilling clause says the cap is the interview's, but it does not say the call passes the literal 3 rather than the review-loop variable.
**Suggested fix:** Add line 672 to the table: apply under the `round < round_cap` revise rules, and do not re-run FROZEN. At line 646, name the interview bound something other than the review-loop `round_cap` and state that the call passes the literal 3.

### F-8: Quoted multi-word surface signals do not match a "whole word" check
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 14, lines 92–99
**Edge case:** The ticket names one file, states a line count under 50, and the change text is "drop table users" or "add an environment variable", with no path segment in the built-in list (for example `scripts/cleanup.sql` or `README.md`).
**What happens:** Files and lines pass. "A subject signal is a whole word", but `drop table`, `delete rows`, `environment variable`, and `feature flag` are phrases. A token compare never matches them, `surfaces` stays `none`, and the recommendation is `tweak` for a data or config change. Decision 4 says any of those four surfaces blocks `tweak` at any size. The operator can still pick another tier; the floor the recommendation exists to enforce does not fire.
**Why the spec misses it:** The table quotes those phrases and the matching rule only says "whole word". No rule says a quoted phrase matches as a bounded phrase.
**Suggested fix:** Say a one-word subject signal matches a whole word, and a quoted multi-word signal matches that phrase with a word boundary on each end. Add a worked example that is `tweak`-sized except for "drop table" or "environment variable", with recommendation `big`.

### F-9: `small` plus `Test command: N/A` drops both gates, and the spec says Phase 3 still runs
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § ship-spec, line 242; `skills/ship-spec/SKILL.md:60-61` and `:144`
**Edge case:** The spec's resolved test command is `N/A` (doc-only or ops-only) and the tier is `small`.
**What happens:** Today Phase 3 is skipped entirely and Phase 3b is the only pass before commit. `small` then skips Phase 3b even when a review command is declared. Nothing automated runs. The spec also says "Phase 3 still runs", which is false for `N/A`. Forcing that sentence runs the command `N/A`, fails the test loop, and a doc-only `small` spec cannot commit.
**Why the spec misses it:** The `small` bullet never mentions the `N/A` exception. "Phase 3 still runs" only distinguishes the test gate from the review-gate skip.
**Suggested fix:** Say `small` does not skip Phase 3 itself, and the existing `N/A` skip still applies; `small` still skips Phase 3b after that. State that a doc-only `small` change commits with both the test loop and the review gate skipped, after the verdict check.

### F-10: A fenced `**Level:**` line in the brief becomes the tier
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § spec-cycle parse step 2, lines 175–176
**Edge case:** The brief's `## Tier` body contains a fenced example `**Level:** small` (or `tweak`) before the real `**Level:** irreversible`. Phase 4 will not emit this; an edited brief will.
**What happens:** The Level regex is not fence-aware. The first match wins. `small` is used, `round_cap` is 2, and ship-spec skips the review gate, with only the multiple-Level warning. A fenced `tweak` halts the real `irreversible` brief. The spec reader ignores fences; the brief reader does not.
**Why the spec misses it:** Fence skipping is specified only for the spec's `**Tier:**` line. The brief parse follows the Scale factor regex, which also does not skip fences, but a wrong Scale factor does not turn off an unskippable ship gate.
**Suggested fix:** When scanning a `## Tier` body, ignore lines inside the same fences the spec reader uses. If the first unfenced Level line is missing, halt. Do not let a fenced example set `round_cap` or the ship gate.

### F-11: Confirming a tier mismatch ships the absent-line tier, not the marker
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Re-run pin, line 179; ship-spec, lines 233–236
**Edge case:** Re-run of a spec that has no `**Tier:**` line, brief says `irreversible`. Phase 1 does not insert a line. The marker is written `tier: irreversible`. Fingerprint matches. Attest's already-green return does not rewrite the marker (line 223).
**What happens:** ship-spec reads the spec as `big` (no line) and the marker as `irreversible`, so the state is `changed`. The existing proceed line is "I have reviewed this spec". After confirm, Phase 3b uses the spec tier, `big`, and the three skip cases stay skips. The unskippable gate does not run. The spec says the confirm names both values, not that proceeding makes the review gate skippable under `big`.
**Why the spec misses it:** The pin documents this as the `changed` state and tells the operator to add the line, but the confirm has no required sentence for what the gate will do if they press proceed anyway.
**Suggested fix:** Require the confirm text to say the gate follows the spec tier (here `big` because no `**Tier:**` line was recorded) and that `irreversible` on the marker will not be enforced. Tell attest's early return to rewrite `tier:` when the fingerprint matches but the marker tier disagrees, instead of leaving the mismatch in place.

### F-12: Plane ticket body was not readable
**Severity:** P4
**Where:** grounding step 3
**Edge case:** `memory_search` for tags `plane_work_item` and `VHS-55` on namespace `skills`.
**What happens:** The server returned access denied for this agent. The review used the brief only. No ticket body was checked for decisions the brief might have dropped.
**Why the spec misses it:** Not a spec defect. The brief is the carried-forward record of the ticket.
**Suggested fix:** None in the spec. Re-run the lookup with a principal that can read namespace `skills` if a later round needs the ticket body.

## Summary
P0: 1 | P1: 2 | P2: 8 | P3: 0 | P4: 1

STATUS: RED P0=1 P1=2 P2=8 P3=0 P4=1
