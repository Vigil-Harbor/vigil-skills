# Conventions Review — round 4

Grounding: spec and brief read fresh from disk. `HEAD` is still `0158267f681386d7b51c3239ec2bc0b13c45ba25`, the spec's anchor commit, and the tracked target files are unmodified. Read `AGENTS.md` (the tracked conventions; `CLAUDE.md` only points to it), wiki `projects/vigil-skills/state.md` and `filemap.md` (there is no `architecture.md` for this project), and wiki decision `decisions/2026-10-13-vhs-27-delta-scoped-review-passes.md`. Ticket lookup failed again (shared memory returned HTTP 502), so I proceeded on the brief; the spec already records this degrade path in § Deferred (P2+), so it is not re-filed.

Deferred-findings block: the spec has no `## Deferred — follow-up required` section (only `## Deferred (P2+)`), so there are no rows to validate and no routing violations.

Delta scope: critique was applied only to the 21 named headings and the open finding's two headings.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Replacement resolver no longer places `spec.md:<line>` locators | CLOSED | All five manifest sites carry the fold: Decision 8 (`spec.md:76-81`, colon and `#L` forms plus the whole-path-token rule); § Open-finding resolver step 5 (`spec.md:130`); the `:492` replacement, second paragraph (`spec.md:339`); scenarios 19, 20 and 25 (`spec.md:436-437`, `:442`); Done when, last bullet (`spec.md:486`). The word-form list gap (`lines 282 and 286`) is also closed, in Decision 8 and scenario 25. |
| correctness | F-2 (P3) | Ticket not cached | CLOSED | `spec.md:503` records it with no spec change. |
| correctness | F-3 (P4) | "A direct child such as" names descendants | CLOSED | `spec.md:120` now reads "A descendant such as". |
| edge-cases | F-1 (P2) | `spec.md:<line>` form not a recognised locator | CLOSED | Same root and same sites as correctness F-1. |
| edge-cases | F-2 (P3) | Empty heading phrase matches symbol-led headings | CLOSED | Decision 7 "An empty phrase matches no arm" (`spec.md:56`); Decision 8 and the `:492` replacement skip an empty phrase (`spec.md:74`, `:337`); scenario 23. |
| edge-cases | F-3 (P3) | Raw-line validation runs before the archive drop | CLOSED | § Changed-path filtering states the consequence as accepted (`spec.md:120`). |
| edge-cases | F-4 (P3) | Ticket grounding unavailable | CLOSED | `spec.md:503`. |
| conventions | F-1 (P3) | `.attempt-<n>/` has no definition in a tracked file | CLOSED | The gloss "an operator-made archive of a superseded attempt" is in Decision 5 (`spec.md:48`) and in the `:490` replacement (`spec.md:323`). |
| conventions | F-2 (P3) | Ticket grounding unavailable | CLOSED | `spec.md:503`. |

No REOPENED or PARTIAL items.

## Findings

### F-1: The `/spec-close` note points at a wiki anchor that does not exist
**Severity:** P3
**Where:** spec.md:505 | spec § Deferred (P2+)
**Convention violated:** Cross-surface pointers must name the real file and text (`AGENTS.md` § Plan & Spec Reviews: "Always verify load-bearing claims against the actual codebase, wiki, and current file state").
**Evidence:** The note says wiki `projects/vigil-skills/state.md` "pins the old mode-table row 11 as a verification anchor". `state.md` has no `row 11` and no mode-table row count; its only "eleven" is "all eleven shipped skills" at line 27, which is unrelated. The stale count is in `projects/vigil-skills/filemap.md:132`: "by an eleven-row mode table". The decision page `decisions/2026-10-13-vhs-27-delta-scoped-review-passes.md` also carries "Open in VHS-60: the mode table has no row for an absent spec file, and a full pass cannot dispatch when the commit snapshot fails", and the `state.md` VHS-27 entry (line 11) says "Two mode-table gaps are open in VHS-60".
**Suggested fix:** Reword the bullet to: "For `/spec-close`: wiki `projects/vigil-skills/filemap.md` says 'eleven-row mode table' (now twelve); the VHS-27 decision page and the `state.md` VHS-27 entry list the two gaps this ticket closes."

### F-2: Spec-level additions beyond the brief, all with rationale (for the human drift check)
**Severity:** P3
**Where:** spec § Decision 7; § Decision 8; § Test plan; § Done when; § `README.md:10` — usage
**Convention violated:** None. These are class (c) additions (the spec adds them with stated rationale), surfaced as the lens requires.
**Evidence:** In the changed regions, these go past what the brief carries:
- **Blank-parent expansion** (Decision 7, `spec.md:66`; resolver step 6; scenario 24): a selected heading with a blank exclusive body also selects every nested heading when no line was placed. This is a behaviour change the brief does not name. The rationale is in the text and matches brief Decision 8's "a slightly wider pass is the cheap error".
- **Markup deletion before comparison** (Decision 7, `spec.md:56`; scenario 21): backticks, asterisks and double quotes are removed from both sides.
- **Parenthesis cut, `#L<n>` locator, word-form lists, and the empty-`Where` and path-less-clause rules** (Decision 8). The wider joining-word list (`vs`, `versus`, `against`, `&`, `/`) is authorized by brief Risk 3, which asks the spec author to pin it.
- **Deletion gate and row-reference gate** (Test plan, `spec.md:455`, `:461`). Done when labels these "Spec-level gates, not brief criteria" (`spec.md:486`), which is the right flag.
- **README says what `--full` does** (brief asks only that the line shows it).
- **Row-reference renumbering** at `:377`, `:379` and `:455` is a necessary consequence of the brief's row insert, not an addition.
**Suggested fix:** Optional. Extend the Done-when "Spec-level gates, not brief criteria" bullet, or add one sentence to Decision 7, saying the blank-parent expansion and the markup deletion are spec-level additions. No behaviour change.

### F-3: The artifact-exception heading omits the `:445` anchor its body now edits
**Severity:** P4
**Where:** spec.md:258 | spec § `skills/spec-cycle/SKILL.md:453` and `:506` — artifact exception
**Convention violated:** Repo pattern in this spec — each replacement heading lists every line it edits (the sibling heading reads "`:377`, `:379`, and `:455` — row references").
**Evidence:** The body's first block is "Current set lead-in (`:445`)", which matches `skills/spec-cycle/SKILL.md:445` exactly. The heading names only `:453` and `:506`. The Scope row covers it through "`### Round artifacts`", so nothing is out of scope.
**Suggested fix:** Rename the heading to "`skills/spec-cycle/SKILL.md:445`, `:453`, and `:506` — artifact exception".

Checks on the in-scope headings that produced no finding:
- **Anchors:** every "Current" block in the changed headings matches the live file byte-for-byte: the mode table with its four-space indent (`:363-375`), the four row-reference sentences (`:377` twice, `:379`, `:455`), the lead-in (`:445`), the artifact paragraph (`:453`), the Phase 2 precondition (`:506`), `:490`, `:492`, `README.md:10`, and `docs/spec-workflow-reference.md:74` and `:81`. No dead or moved citations.
- **Row references are complete:** `grep -nE '[Rr]ows? [0-9]' skills/spec-cycle/SKILL.md` returns lines 374, 377, 379, 455 and 1079 only, and the spec accounts for all five. No other tracked skill, agent, doc or test cites this table by row number (the hits in `skills/spec-close/SKILL.md` are its own table). No test asserts on a mode token or the `# Delta scope` block.
- **Wiki decision 3 of VHS-27** ("Any later change to spec-cycle has to say which counter it means"): Decision 2 and the `:453` replacement now say the pass "takes its cumulative round `C` and consumes pass index `P`", and Decision 11 names `round_cap` and `P`. Compliant.
- **Wiki decision 4 of VHS-27** (three saved files before each dispatch): the two-file exception departs from it, but the decision page lists this as open in VHS-60 and brief Decision 2 carries it. Authorized, not drift.
- **Wiki decision 6 of VHS-27** (code that merges is a changed region): Decision 5 narrows the path set as the brief directs; canonical cross-ticket briefs and specs stay visible.
- **Minimal diff and no compatibility shim:** Decision 2 now keeps the existing rename-failure sentence byte-for-byte, and scenario 5 was narrowed to match it. The current-ticket `.reviews/` clause kept beside the wider rule that subsumes it is acknowledged in § Deferred (P2+).
- **Reuse:** the colon and `#L` locator spellings reuse the forms the changed-path rule already strips. No registry, flag or new file is introduced.
- **Public-repo and harness-neutral rule (`AGENTS.md`):** the replacement prose names no machine path or internal-only tool.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 1

STATUS: GREEN
