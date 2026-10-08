# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Repo-root walk excludes cwd, so the usual invocation never resolves | CLOSED | spec § Decision 7 line 87: cwd is the root when it contains `AGENTS.md` or `CLAUDE.md`, otherwise the nearest ancestor; separators are normalized. § Test plan line 257. § Phase 0 line 179 cites Decision 7. |
| correctness | F-2 | Resume parses a work-item title Phase 4 never writes | CLOSED | spec § Decision 3 line 46; § Decision 12 line 141; § Phase 3 line 219; § Phase 4 line 225; § Test plan line 261. Stored name and local H1 are `<PARENT-ID> <slug>: <short title>`. The approval line is display only. Five sites; fold kept. |
| correctness | F-3 | An incomplete local sibling has no outcome, and the temp rules disagree | CLOSED | spec § Phase 4 lines 229–231: candidates are the ticket-file glob; incomplete is a mismatch and is not renamed onto; a temp is removed only after a rename onto a path that did not exist before that attempt. |
| correctness | F-4 | ticket not cached | CLOSED | Not a spec defect. No MCP memory tool is available this round, so the brief's Done when (lines 34–42) remains the acceptance text. Not re-filed. |
| edge-cases | F-1 | Zero "can create" still selects local, including a tracker that is up | CLOSED | spec § Decision 3 lines 40–41 and 52: a probe that does not answer is not "zero can create"; no create or no parent is `halt`; `local` only when no issue-tracker integration is connected. § Test plan line 261. |
| edge-cases | F-2 | The repo-root walk excludes the directory the operator is in | CLOSED | Same text as correctness F-1. |
| edge-cases | F-3 | Resume matches a title the create never sets | CLOSED | Same five sites as correctness F-2. § Decision 12 lines 146–147: after create, keep the id only when one child row has that id, that title, and the spec's ticket as parent. |
| edge-cases | F-4 | An omitted relation field never becomes the empty set | CLOSED | spec § Decision 12 lines 150–152: a successful body that omits `blocked_by` is the empty set; a non-list is cannot-read and stops creates and edge writes. § Test plan line 262. |
| edge-cases | F-5 | A create result with no parent field is kept as the child | CLOSED | spec § Decision 12 lines 145 and 147: an omitted or null parent stops; the id is kept only when a fresh child list shows exactly one matching row. § Test plan line 265. |
| edge-cases | F-6 | Equal edges print FILED while the approved body was not written | CLOSED | spec § Decision 12 lines 159–161; § Phase 4 lines 227 and 235; § Test plan line 265; § Deferred (P2+) line 303. A match requires the stored body to equal the frozen draft. A differing body does not print `FILED`. |
| edge-cases | F-7 | Local resume does not say which files are ticket files | CLOSED | spec § Phase 4 line 229: candidates are only the ticket-file glob; the spec, the brief, other parents, and dot-prefixed temps are not candidates. |
| edge-cases | F-8 | The states.json path under the config dir is not written down | CLOSED | spec § Decision 12 line 137: `<config-dir>/skills/ship-spec/states.json`, and that is not `/ship-spec`'s path when `$CLAUDE_CONFIG_DIR` is set. Matches `skills/spec-brief/SKILL.md` line 53 and `skills/spec-close/SKILL.md` line 31; `skills/ship-spec/SKILL.md` line 41 does not read that variable. |
| edge-cases | F-9 | The no-blocker sentinel is not defined as the empty edge set | CLOSED | spec § Decision 3 lines 46–47; § Decision 12 line 154; § Phase 3 lines 207 and 219. `None — no blockers.` is the empty set. A mix with a title is cannot-read. |
| edge-cases | F-10 | A child-list page that errors or repeats is not a failed read | CLOSED | spec § Decision 12 line 139: a page error, a non-success page, or a repeated cursor is cannot-read and halts before any create or edge write. The same rule covers a paged `blocked_by` read. § Test plan line 262. |
| edge-cases | F-11 | Two overlapping runs can both create the same slug | CLOSED | spec § Decision 12 lines 146–148: list again after each create; overlapping runs are not serialized; two rows halt, name both ids, and do not print `FILED`. The skill does not delete the loser. |
| edge-cases | F-12 | A successful truncated body is not the failure the deferral assumes | CLOSED | spec § Deferred (P2+) line 303 no longer claims every oversized create stops. § Decision 12 line 160: a success whose stored body is not the body sent is a mismatch and does not print `FILED`. |
| edge-cases | F-13 | The stop report names the slug and not the failing call | CLOSED | spec § Decision 12 line 163: `halt: <capability> <slug or edge> <integration name or none> <status or error payload>`. |
| edge-cases | F-14 | Plane ticket text was not readable | CLOSED | Same as correctness F-4. Not a spec defect. Not re-filed. |
| conventions | F-1 | The new README Requirements bullet is unscoped | CLOSED | spec § Decision 10 line 108: `For /spec-tickets: …`; the other Requirements bullets and the `gh` sentence are unchanged. |
| conventions | F-2 | The string Phase 4 writes is not the string Decision 12 matches | CLOSED | Same five sites as correctness F-2. |
| conventions | F-3 | `issue-tracker?` halt overrides the portability contract without naming it | CLOSED | spec § Decision 3 line 55 names portability-contract §3: only confirmed not-connected may take `local`; an unavailable tracker would warn-and-proceed there, and this skill halts instead. The `requires:` block is unchanged. |
| conventions | F-4 | Drift-check — round-2 additions with rationale | CLOSED | No edit was required. Those pins are still in the spec. Pins added since that list are F-1 below. |
| conventions | F-5 | The local temp copies spec-brief's path and drops its commit warning | CLOSED | spec § Phase 0 line 181: temps are not gitignored, and printing them is the warning not to commit them. Phase 0 still does not delete them. |
| conventions | F-6 | Two Storage-line grammars | CLOSED | spec § Decision 3 line 42 is the one grammar. § Phase 3 lines 200 and 219 copy it and say not to use a second one. |

All eight manifest lines match the current spec. There is no `## Deferred — follow-up required` section, so there is no routing-row check. `## Deferred (P2+)` is the P2 carry heading. `projects/vigil-skills/` has `state.md` and `filemap.md` and no `architecture.md`. `scale_lens` is off; no scalability report was read.

## Findings

### F-1: Drift-check — round-3 pins with rationale
**Severity:** P3
**Where:** spec § Decisions 3, 7, 10, 12; spec § Phase 0 — Preflight; spec § Phase 3 — Approval; spec § Phase 4 — File; spec § Deferred (P2+)
**Convention violated:** None. Class (c). Brief Decisions 1–8, `## Scale`, and Risks 1–3 still authorize the frame. Each item below is a review fix with the reason written next to it. No class (d) silent addition.
**Evidence:** Brief Decisions 1–8 and Risks 1–3. Round-2 conventions F-4 listed the pins through that round. These are the commitments added since that list. The census is still 11 `skills/*/SKILL.md` files, so 12 after `spec-tickets` matches § Decision 11 and `tests/test_lint.py` lines 50–55. `tests/test_session_handoff.py` lines 772–774 only checks that `session-handoff` is a member.
**Suggested fix:** No edit required. The new drift-check list is:

- **Decision 7** — Cwd is the root when it contains `AGENTS.md` or `CLAUDE.md`; otherwise the nearest ancestor. Separators are normalized, and a path is accepted when it canonicalizes to the TODO spec file.
- **Decisions 3 and 12, Phases 3–4** — The stored name and the local H1 are `<PARENT-ID> <slug>: <short title>`. The approval line `<slug> — <title>` is display only.
- **Decision 3** — `local` only when no issue-tracker integration is connected. A probe that does not answer is not "zero can create". A connected integration that cannot create, or cannot set a parent, is `halt`.
- **Decision 3** — One Storage grammar: `native` and `text` use `via <name>`, `local` has no `via`, and `halt` is `Storage: halt via <name or none> (<reason>)`.
- **Decision 3** — Names the portability-contract §3 narrowing. `?` does not become warn-and-proceed for a failing tracker. The `requires:` block stays `issue-tracker?`.
- **Decisions 3 and 12** — `None — no blockers.` is the empty set, not a title. A mix of that line and a title is cannot-read.
- **Decision 12** — The file is `<config-dir>/skills/ship-spec/states.json`. That is not `/ship-spec`'s path when `$CLAUDE_CONFIG_DIR` is set.
- **Decision 12** — A successful native body that omits `blocked_by` is the empty set. A value that is not a list is cannot-read and stops creates and edge writes.
- **Decision 12** — An omitted or null parent stops. The id is kept only when a fresh child list shows exactly one row with that id, that title, and the spec's ticket as parent.
- **Decision 12 and Phase 4** — A match requires the stored body to equal the frozen draft. A differing body, including a success whose stored body is not the body sent, is a mismatch and does not print `FILED`.
- **Decision 12** — A page error, a non-success page, or a repeated cursor is cannot-read, including a paged `blocked_by` read. A partial page is not the set.
- **Decision 12** — Overlapping runs are not serialized. The skill does not delete the loser. Two rows halt, name both ids, and do not print `FILED`.
- **Decision 12** — A halt after approval also prints `halt: <capability> <slug or edge> <integration name or none> <status or error payload>`.
- **Phase 0** — The dot-prefixed temps are not gitignored. Printing them is the warning not to commit them.
- **Phase 4** — Local candidates are the ticket-file glob. An incomplete candidate is a mismatch. A temp is removed only after a rename onto a path that did not exist before that attempt.
- **Decision 10** — The README Requirements bullet is scoped to `/spec-tickets` and does not change the other bullets.
- **Deferred (P2+)** — An oversized create is not assumed to fail. The body-mismatch rule is what blocks `FILED`.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 0

STATUS: GREEN
