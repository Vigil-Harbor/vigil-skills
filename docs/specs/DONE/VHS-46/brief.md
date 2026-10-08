# VHS-46 — ship-spec: pre-commit review gate; retire bloat-check
**Status:** Backlog · **Priority:** medium · **Assignee:** unassigned
**Created:** 2026-10-08 · **Plane:** VHS-46 (1c822d28-406f-4f15-8737-d55c71a66eaf, Backlog)
**Origin:** Devin, 2026-10-08: "looking to gate or hook off the new release of ponytail (github.com/DietrichGebert/ponytail). We initially tested this out by making our own with bloat-check but I hardly use it." Decision the same day: gate, not global hook; tracked separately from VHS-45 so it can ship against today's ship-spec.

## Problem

bloat-check is opt-in and manual, so it does not get run. ship-spec has no review step between the green test gate and the commit; the first review a change gets is CodeRabbit on the PR.

Ponytail v5 rebuilt its review skill as a full review: bug, risk, scale, missing test, speed, lean. It reads the callers of changed code, not only the diff, and requires a concrete failing case per finding. That overlaps bloat-check's evidence gate without matching it: bloat-check demands proof per finding type (both copies cited, a repo-wide caller search, the shorter form written out), where the review skill asks for a concrete case and a re-read. It does not cover bloat-check's invariant veto, and its yagni category is one bloat-check deliberately excluded for hardened code.

## Why it matters

A review that has to be remembered does not happen. A gate inside ship-spec runs on every change before the commit exists, so problems are fixed while the implementing context is still loaded, and the PR that CodeRabbit sees is already past one independent read.

## Scope (verified against current files, 2026-10-08)

| Path | Current | Change |
|------|---------|--------|
| `skills/ship-spec/SKILL.md` | Phase 3 test gate at `:94`, Phase 4 commit at `:131`, nothing between them. Test command resolved in Phase 0 step 4 (`:18`). No `requires:` block (frontmatter ends at `user_invocable`, `:4`). | Add the review gate between the test gate and the commit. Resolve the review command in preflight beside the test command. Record the result in `<TICKET-ID>.review.md` and one PR-body line. |
| `skills/bloat-check/SKILL.md` | Standalone skill; context collection at Step 1 (`:43`), invariant veto at Step 4 (`:68`). Referenced by no other tracked file outside `docs/specs/`. | Delete. Its invariant veto moves into the gate. |
| `tests/test_lint.py` | `:52` expects 12 shipped skills. | 11 after the delete. |
| `docs/customizing.md` | Explains how a project declares its test command (`:9`–`:22`). | Add how a project declares its review command, with one tagged example. |
| `docs/spec-workflow-reference.md` | ship-spec Phase 3 at `:174`, Phase 4 at `:180`. | Describe the gate between them. |
| `AGENTS.md`, `README.md` | ship-spec one-line descriptions at `AGENTS.md:31`, `README.md:12`. Neither mentions bloat-check. | Mention the review gate in the ship-spec description. `AGENTS.md` declares no review command (Decision 8) and gains the targeted removal note for installed `bloat-check` copies (Decision 13). |

## Decisions carried forward

1. **Should fix findings are fixed, or recorded with a one-line reason.** They do not block the commit by themselves. Forces a decision per finding without turning judgment calls into blockers. (Q1 B)
2. **The review command is declared, like the test command.** Resolution order: the spec, then the project instructions file, then skip with a one-line note. That skip also puts one line in the PR body saying no review command is declared; it writes no review file, because no review was attempted. A gate that can block a commit does not guess which skill to run. (Q2 A; Codex round 2)
3. **The review runs in a fresh subagent** that receives the diff and the spec path, not the implementer's reasoning. A host without subagents runs it inline. Independence is the point of a review. (Q3 B)
4. **One review pass.** Review, fix, re-run the test command, commit. No re-review loop; the tests check the fixes and CodeRabbit still reviews the PR. (Q4 A)
5. **The audit record is a file**, `docs/specs/TODO/<TICKET-ID>.review.md`, beside the test output, plus a one-line summary and link in the PR body. `/spec-close` archives it with the other companions. (Q5 B)
6. **A Must fix that cannot be fixed, or whose fix is vetoed, stops the run and asks the operator**: fix by hand, override and commit with the finding recorded, or abandon. A blocker never passes silently. (Q8 A)
7. **A declared review command that is not available is skipped**, and the skip is stated in both the review file and the PR body. The repo must run on any harness. (Q9 A)
8. **vigil-skills declares its own review command only in the machine-local, gitignored `CLAUDE.md`.** `AGENTS.md` declares none. `docs/customizing.md` shows how to declare one, with ponytail as a tagged example. The public repo requires no product. (Q10 A)
9. **The reviewer subagent is read-only.** It returns findings; the implementing agent applies fixes. Same rule as the spec reviewers. (Q11)
10. **Nice to have findings are written to the review file only.** Not acted on, not in the PR body. (Q12)
11. **From the ticket, unchanged:** the gate sits after the test gate passes and before the commit; Must fix findings block the commit; the skill names the review capability, not a product; a finding whose fix would trip a declared design invariant or a shape/adversarial test pin is vetoed and listed with its reason, not applied; bloat-check is retired in the same change.
12. **The gate adds no proof standard of its own.** It relies on the review skill's evidence rule and adds only the invariant veto. bloat-check's stricter per-type proof is knowingly dropped with the skill. (Codex review D1 A)
13. **Installed copies get a targeted removal note.** `sync.py install` keeps destination files the repo no longer has, so `AGENTS.md` § Superseded vendor skills gains a one-line targeted removal step for `bloat-check`, in the shape used for `agentcraft-handoff`. (D2 A)
14. **The gate runs when the test command is `N/A`.** On that path it runs after implementation and before the commit, and there is no test re-run after fixes. (D3 A)
15. **Red tests after review fixes go back into the existing test gate loop**, with a fresh count of 5 and the same halt menu. Nothing commits while tests are red. There is no second review. The saved test output is the final passing run. (D4 A)
16. **A review that errors is treated like one that is not available** (Decision 7): skipped, and recorded in the review file and the PR body. **A finding the gate cannot place in a group is treated as Should fix.** The minimum the gate needs from a review is a list of findings, each with a location, a problem statement, and a group or severity it can map to blocks / fix-or-record / record-only. (D5 A)

## Done when

- A ship-spec run with a review command that is declared and available shows the gate between test gate and commit, and a must-fix finding stops the commit.
- A ship-spec run with no review command declared completes and prints the skip note.
- bloat-check is gone from the repo and python lint.py --strict reports 0 ERROR.

## Out of scope

- Loading a lean-code ruleset into the implementing step. Review only. Tracked as VHS-48. (Q6)
- Machine setup of any review plugin. Ponytail v5.1.0 is installed on the operator's machine with its default mode off; that is not part of the repo change. The machine-local `CLAUDE.md` has no review-command line today (`CLAUDE.md:1`–`:14`); the operator adds one after this change defines the format, and the first Done-when bullet is checked on a machine that has it.
- A global hook. The decision was a gate.
- Adding a `requires:` block to `/ship-spec`. That is the existing missing-`requires:` backlog (`docs/authoring-portable-skills.md:41`, pinned by `tests/test_spec_close_log.py:1059`), not this change.
- The executor that reads `/spec-tickets` children, and any change to `/spec-tickets`.
- A re-review loop or an iteration cap for the gate (Decision 4).
- Changes to `/review-pr`, `/spec-cycle`, or the reviewer agents.
- The wiki. The `bloat-check` filemap row added on 2026-10-08 is removed post-merge by the wiki's own flow.

## Scale

**Factor:** no — a prose change to one skill, one run at a time. (Q7)

## Risks / decisions

1. The exact name and format of the review-command declaration in a spec and in the project instructions file; spec author pins this.
2. The mapping table from a review's own groups or severities onto "blocks", "fix or record" and "record only". Decision 16 fixes the default for a finding that maps to nothing; spec author pins the table.
3. How the gate finds declared invariants and test pins for the veto — `skills/bloat-check/SKILL.md` Steps 1 and 4 are the source text to carry over; spec author pins this.
4. `/ship-spec` has no `requires:` block today, so the lint already warns on it. The portability contract makes `subagents` a boolean where `true` means required (`docs/portability-contract.md:53`–`:78`); the review has an inline fallback, so this change declares no `subagents` requirement. This change adds no `requires:` block to ship-spec (see Out of scope), so the lint warning stays as it is; spec author pins nothing here beyond confirming the test gate tolerates that existing WARN.
5. Whether a spec's required sections change. `/spec-cycle` is out of scope, so a review-command section in a spec must stay optional; spec author pins this.
6. The ticket text says to pin ponytail v5.0.0; v5.1.0 was released the same day and is what is installed. No repo text should carry a version; spec author pins this.

## References

- Ticket: Plane VHS-46, resolved through the tracker (shared-memory lookup denied on namespace `skills`).
- `skills/ship-spec/SKILL.md:18`, `:94`, `:131` — test-command resolution, test gate, commit.
- `skills/bloat-check/SKILL.md:43`, `:68` — context collection and invariant veto.
- `tests/test_lint.py:52` — skill census, 12.
- `docs/customizing.md:9` — test-command declaration pattern.
- Ponytail review skill at v5.1.0: `skills/ponytail-review/SKILL.md` in `DietrichGebert/ponytail` — six finding types, "No case, no finding", groups Must fix / Should fix / Nice to have.
- Related tickets: VHS-45 (shipped, `/spec-tickets`), VHS-47 (green marker), VHS-48 (ruleset exploration), VHS-42 (lint inventory tripwire), VHS-31 (test-output path redaction, same ship-spec region).
- `sync.py:72`–`:94` — install keeps destination-only files.
- `skills/ship-spec/SKILL.md:18`–`:20` — the `N/A` test-command path skips Phase 3.
- Codex brief review (gpt-6-sol, high), 2026-10-08, round 1: 2 blockers, 5 should-fix; Decisions 12–16 and the Risks 2 and 4 rewrites are its dispositions. Round 2: 0 blockers, 3 should-fix, all dispositioned (fresh loop count, PR-body line on an undeclared skip, no `requires:` block).
- Interview: 2 rounds, exit empty-frontier
