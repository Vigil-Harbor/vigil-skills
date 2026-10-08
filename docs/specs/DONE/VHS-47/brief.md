# VHS-47 — spec-cycle: write a machine-readable green marker that /spec-tickets and /ship-spec read
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-10-08 · **Plane:** VHS-47 (583f77c0-ff95-4df3-aecf-fa1e7a317222, Backlog)
**Origin:** CodeRabbit review of PR #31 (VHS-45, /spec-tickets), 2026-10-08 — one Major finding on skills/spec-tickets/SKILL.md line 35. It was skipped in that PR with a reasoned reply; Devin asked for this follow-up.

## Problem

Nothing downstream of /spec-cycle can tell whether a spec actually ended green. /spec-tickets and /ship-spec both treat "green-lit" as a structural check: the required headings are present. A spec that never went through review, or that ended red after round 4, passes that check. In /spec-tickets it can reach "Approve and file"; in /ship-spec it can be implemented. The operator is the only guard.

CodeRabbit proposed that /spec-tickets parse the reviewer reports and halt unless the combined P0+P1 count is zero. That was declined because it would put a second copy of /spec-cycle's gate arithmetic in another skill, and that arithmetic is not simple: deferred follow-up rows do not count, a post-round-4 grill can settle findings, and a delta pass after a manual patch can turn a spec green without a full round. VHS-45 itself is the specimen: its round-4 reports say RED, and its green came from a delta-scoped round 5.

## Why it matters

The lifecycle's stages run in separate sessions, often on separate agents. The only thing that crosses the boundary is what is on disk. Today the verdict is not on disk in a form a skill can read, so "green-lit" is an assumption each downstream stage makes about a file it did not review.

## Scope (verified against current files, 2026-10-08)

| Path | Current | Change |
|------|---------|--------|
| `skills/spec-cycle/SKILL.md` | Green is decided at step 2d (`:439`, `total_p0p1 == 0`), followed by the bounded polish 2g (`:670`), which may edit the spec, then the Phase 3 drift check (`:703`). Red is decided at the 2f halt (`:533`). The post-round-4 interview is 2f-i (`:566`). A re-run on an existing spec does not re-author it (`:298`). No verdict is written anywhere. | Write the marker on the green path and at the red halt; the red marker describes the spec as it stands at the halt, after that round's 2e edits. Write a pending marker when the review loop starts. Add the operator-attest flag. |
| `skills/ship-spec/SKILL.md` | Phase 0 step 1 confirms the spec path and shape (`:15`). "Spec not green" is a failure-mode note keyed on missing headings (`:384`). | Read the marker in preflight: green passes; red halts; missing or changed-spec asks the operator to confirm. One PR-body line when the operator confirmed past it. |
| `skills/spec-tickets/SKILL.md` | Phase 0 step 3 "Green-lit check" is the heading check (`:35`). | Read the marker in preflight with the same rules; show the verdict line in the approval block. |
| `skills/spec-close/SKILL.md` | Archives `<TICKET-ID>.reviews/` whole and any `<TICKET-ID>.<rest>` companion (`:339`–`:340`). | None. A marker inside the reviews directory is archived as is. |
| `docs/spec-workflow-reference.md`, `AGENTS.md`, `README.md` | Describe the three stages without a verdict marker (`README.md:10`–`:12` carries the stage summaries and `/spec-cycle`'s invocation). | Describe the marker and the attest flag where each stage is described. |

## Decisions carried forward

1. **The marker is a file in the reviews directory** (`docs/specs/TODO/<TICKET-ID>.reviews/`), not text in the spec. It keeps the verdict out of the document it judges, so a fingerprint of the spec is simple, and `/spec-close` already archives that directory. (Q1 A)
2. **No marker: warn and ask the operator to confirm.** A host that cannot wait stops. Old specs still ship with one confirmation; nothing proceeds silently. (Q2 A)
3. **Red marker: halt**, in both `/ship-spec` and `/spec-tickets`. The way past it is a green verdict. (Q3 A)
4. **Green marker, but the spec changed since: warn and ask to confirm.** Small hand edits after green are normal; the operator decides. (Q4 A)
5. **An operator can attest a spec green** when the verdict was reached outside `/spec-cycle` (a manual patch and a delta review by hand). (Q5 B)
6. **Attestation is a flag on `/spec-cycle`.** It needs an existing spec, runs no review, shows the current verdict, asks the operator to confirm, and writes a green marker marked operator-attested with a one-line reason. It never runs headless. (Q8 A)
7. **An attested green passes like a reviewed green.** The downstream preflight line and the PR body say which kind it was. (Q9 A)
8. **After the post-round-4 interview the marker stays red.** The interview does not re-run reviewers, so nothing has verified the spec. (Q6)
9. **Confirming past a missing or changed-spec marker leaves a trace.** `/ship-spec` puts one line in the PR body; `/spec-tickets` shows the verdict line in its approval block. (Q10)
10. **From the ticket, unchanged:** `/spec-cycle` writes the marker — green or red, the round it ended on, the gate count, the date, and a fingerprint of the spec file it applies to. `/spec-tickets` and `/ship-spec` read it in preflight. Neither parses reviewer reports or re-derives the gate.
11. **An attested marker records what it is.** Verdict green; source operator-attested; round and gate count written as not reviewed; the operator's reason; the date; the fingerprint; and one line quoting the verdict it replaced, or none. This qualifies Decision 10: round and gate count are real numbers only on a marker a review produced. (Codex round 1, D1)
12. **When attestation is allowed.** On a spec with no marker, a pending marker, a red marker, or a green marker whose spec has changed. It replaces the old marker and quotes the old verdict. It is refused on a spec that lacks a required heading. On a green marker that still matches the spec it does nothing and says so. (D2)
13. **Pending.** When the review loop starts, `/spec-cycle` overwrites the marker with a pending verdict. A run that reaches a verdict replaces it with green or red. An interrupted run leaves pending. Downstream treats pending exactly like a missing marker (Decision 2), naming it. (D3)
14. **Broken markers, and hosts that cannot wait.** A marker that is unreadable, malformed, or written for a different ticket is treated as missing, with the reason named in the warning. Every confirm prompt in this change stops on a host that cannot wait. A red marker halts whether or not the spec has changed since. (D4)
15. **`/spec-tickets` and the verdict.** Red stops in preflight, before any draft. Otherwise the verdict line is in the approval block and `Approve and file` is the confirmation; there is no second prompt. Immediately before filing it reads the marker again and stops for a new approval if the verdict line differs from the one it printed. Reading the marker is not reading the reviews for pieces; the breakdown still comes from the spec alone. (D5)
16. **Who checks the fingerprint.** The fingerprint is a content hash of the spec with line endings normalised. `/spec-cycle` computes it and `/ship-spec` verifies it; both use shell. `/spec-tickets` declares no shell and does not verify it: its approval block says the fingerprint was not checked on this host. A `/ship-spec` host that cannot compute the hash treats the marker as the changed-spec case (Decision 4). (D6 A)
17. **The green marker covers the spec after the bounded polish (2g).** It is written once polish has finished, so a run that has just ended green passes its own fingerprint check. (Codex round 2)

## Done when

- /spec-cycle records its final verdict in a form another skill can read without parsing review reports.
- /spec-tickets and /ship-spec check it in preflight and do not proceed silently on a spec that is red or was never reviewed.
- The CodeRabbit thread on PR #31 can be pointed at this ticket.

## Out of scope

- Backfilling markers for specs that already exist. They get no marker and meet the confirm prompt. (Q11)
- `/spec-close` reading the marker. It archives it with the reviews directory and nothing more. (Q11)
- Delta-scoped review rounds (VHS-27) and VHS-43's work.
- Any change to the reviewer agents, the gate formula, or the routing rules.
- Adding a `requires:` block to `/ship-spec`. It already runs `git` and `gh` through the shell with no declaration, so the hash command adds no capability it does not already use. Clearing that backlog, with the doc sentence and the test that pin it, is VHS-51. The lint census stays 11.
- The executor that reads `/spec-tickets` children.

## Scale

**Factor:** no — one small file per spec. (Q7)

## Risks / decisions

1. The marker's file name and format, the exact spelling of its fields and verdict values, and the hash command and normalisation that give the same fingerprint under Windows and Unix line endings; spec author pins this.
2. The exact step text that writes the green marker after 2g and the red marker at the 2f halt (Decisions 17 and the Scope row fix the timing; the wording is the spec author's); spec author pins this.
3. The exact step at which the pending marker is written on a first run and on a re-run (Decision 13 fixes the behaviour; the step is the spec author's); spec author pins this.
4. The attest flag's exact spelling and usage line, and how it combines with the brief-path argument; spec author pins this.
5. Whether `/spec-cycle`'s own `requires:` block already covers a hash command and a new file write, and whether `/spec-tickets`' block needs any change for reading one more file (neither should; confirm against the files); spec author pins this.
6. VHS-27 and VHS-43 touch the same region of `/spec-cycle`; whether this change must leave room for them; spec author pins this.

## References

- Ticket: Plane VHS-47, resolved through the tracker (shared-memory lookup is denied on namespace `skills`).
- `skills/spec-cycle/SKILL.md:298`, `:439`, `:533`, `:566`, `:670`, `:703` — re-run rule, gate, halt, post-round-4 interview, polish, drift check.
- `skills/ship-spec/SKILL.md:15`, `:384` — spec path check; the "Spec not green" note.
- `skills/spec-tickets/SKILL.md:35` — the heading-only green-lit check.
- `skills/spec-close/SKILL.md:339`–`:340` — companion archive rule.
- PR #31 CodeRabbit thread: https://github.com/Vigil-Harbor/vigil-skills/pull/31
- Specimen: `docs/specs/DONE/VHS-45/reviews/` — round-4 reports RED, round 5 a delta pass.
- Related tickets: VHS-45, VHS-46 (both shipped), VHS-27, VHS-43.
- `skills/spec-tickets/SKILL.md:5`–`:8` — `requires:` has filesystem and an optional issue tracker, no shell.
- Codex brief review (gpt-6-sol, high), 2026-10-08, round 1: 1 blocker, 5 should-fix, 2 minor; Decisions 11–16 and the Scope and Risks edits are its dispositions. Round 2: 0 blockers, 2 should-fix; Decision 17 and the `requires:` fence (VHS-51) are its dispositions.
- Interview: 2 rounds, exit empty-frontier
