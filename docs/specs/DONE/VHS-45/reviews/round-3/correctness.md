# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Repo-root walk excludes cwd, so the usual invocation never resolves | CLOSED | spec § Decision 7: cwd is the root when it contains `AGENTS.md` or `CLAUDE.md`; separators are normalized. § Test plan repeats the cwd case. |
| correctness | F-2 | Resume parses a work-item title Phase 4 never writes | CLOSED | spec § Decision 3, § Decision 12, § Phase 3 — Approval, § Phase 4 — File, § Test plan: stored name and local H1 are `<PARENT-ID> <slug>: <short title>`; the approval line is display only. |
| correctness | F-3 | An incomplete local sibling has no outcome, and the temp rules disagree | CLOSED | spec § Phase 4 — File: candidates are only `<PARENT-ID>.ticket-*.md`; incomplete is a mismatch; temp removed only after a rename onto a path that did not exist before that rename. |
| correctness | F-4 | ticket not cached | REOPENED | Memory server unavailable (`search_tool` returned no MCP tools). Not a spec defect. Re-filed as F-3 at P3 per grounding step 3; not promoted. |
| edge-cases | F-1 | Zero "can create" still selects local, including a tracker that is up | CLOSED | spec § Decision 3: a probe that does not answer, or a connected integration that cannot create or cannot set a parent, is `halt`. `local` only when no issue-tracker integration is connected. § Test plan restates it. |
| edge-cases | F-2 | The repo-root walk excludes the directory the operator is in | CLOSED | Same edit as correctness F-1. |
| edge-cases | F-3 | Resume matches a title the create never sets | CLOSED | Same title edit as correctness F-2. § Decision 12 also keeps the id only when a fresh child list shows exactly one row with that id, a title that parses to the slug, and the spec's ticket as parent. |
| edge-cases | F-4 | An omitted relation field never becomes the empty set | CLOSED | spec § Decision 12: a successful native body that omits `blocked_by`, or whose `blocked_by` is `[]`, is the empty set. A non-list value is cannot-read and stops creates and edge writes. § Test plan restates it. |
| edge-cases | F-5 | A create result with no parent field is kept as the child | CLOSED | spec § Decision 12: an omitted or null parent stops, and the id is kept only when the post-create list shows exactly one matching row. § Test plan restates the omitted-or-null stop. |
| edge-cases | F-6 | Equal edges print FILED while the approved body was not written | CLOSED | spec § Decision 12 and § Phase 4 — File: a match requires the stored body to equal the frozen draft; a differing body is mismatched and does not print `FILED`. § Test plan and § Deferred (P2+) restate it. The new wire-format failure is F-1 below, not this hole. |
| edge-cases | F-7 | Local resume does not say which files are ticket files | CLOSED | spec § Phase 4 — File limits candidates to the ticket glob and excludes the spec, the brief, other parents, and dot-prefixed temps. |
| edge-cases | F-8 | The states.json path under the config dir is not written down | CLOSED | spec § Decision 12 names `<config-dir>/skills/ship-spec/states.json` and says this is not `/ship-spec`'s path when `$CLAUDE_CONFIG_DIR` is set. Matches `skills/spec-brief/SKILL.md` step 3, `skills/spec-close/SKILL.md` step 4, and `skills/ship-spec/SKILL.md` step 9. |
| edge-cases | F-9 | The no-blocker sentinel is not defined as the empty edge set | CLOSED | spec § Decision 3, § Decision 12, and § Phase 3 — Approval: `None — no blockers.` is the empty set, a mix with a title is cannot-read, and the approval block uses that sentinel. |
| edge-cases | F-10 | A child-list page that errors or repeats is not a failed read | CLOSED | spec § Decision 12: a page error, a non-success page, or a repeated cursor is cannot-read and halts before any create or edge write; the same rule covers a paged `blocked_by` read. § Test plan restates it. |
| edge-cases | F-11 | Two overlapping runs can both create the same slug | CLOSED | spec § Decision 12: overlapping runs are not serialized, the skill does not delete the loser, and two rows halt with no `FILED`, naming both ids. |
| edge-cases | F-12 | A successful truncated body is not the failure the deferral assumes | CLOSED | spec § Deferred (P2+) no longer claims every oversized create fails. § Decision 12: a success whose stored body is not the body sent is a mismatch and does not print `FILED`. |
| edge-cases | F-13 | The stop report names the slug and not the failing call | CLOSED | spec § Decision 12: on a halt after approval, print `halt: <capability> <slug or edge> <integration name or none> <status or error payload>`. |
| edge-cases | F-14 | Plane ticket text was not readable | REOPENED | Same unavailable memory server as correctness F-4. Covered by F-3; not promoted. |
| conventions | F-1 | The new README Requirements bullet is unscoped | CLOSED | spec § Decision 10 gives the scoped `For /spec-tickets:` bullet and says it does not change the other Requirements bullets or the `gh` sentence in AGENTS.md. |
| conventions | F-2 | The string Phase 4 writes is not the string Decision 12 matches | CLOSED | Same edit as correctness F-2. |
| conventions | F-3 | `issue-tracker?` halt overrides the portability contract without naming it | CLOSED | spec § Decision 3 names portability-contract §3, states the `requires:` block does not change, and says this skill halts instead of warn-and-proceed. §3 does say optional absence is warn-and-proceed (`docs/portability-contract.md` lines 76–78). |
| conventions | F-4 | Drift-check — round-2 additions with rationale | CLOSED | No defect. The brief's Decisions 1–8 and Risks 1–3 still authorize the pins. |
| conventions | F-5 | The local temp copies spec-brief's path and drops its commit warning | CLOSED | spec § Phase 0 — Preflight: temps are not gitignored, and printing them is the warning not to commit them. |
| conventions | F-6 | Two Storage-line grammars | CLOSED | spec § Decision 3 gives one grammar (`local` has no `via`; `halt` carries the reason). § Phase 3 — Approval's fence matches it and says not to use a second grammar. |

Manifest lines for the eight round-2 P0/P1 items match the current spec. No commit in the last 7 days touches the files this spec edits (newest is `cea8a04`, 2026-09-08). `skills/*/SKILL.md` is 11 files, so 12 after `spec-tickets` matches `tests/test_lint.py` (`len(skills) == 8` today). There is no `## Deferred — follow-up required` section. `scale_lens` is off; no scalability report was read.

## Findings

### F-1: Text-mode success never matches the frozen draft on plane-proxy
**Severity:** P0
**Where:** spec.md:159 | spec § Decision 12; spec § Decision 3; spec § Phase 4 — File
**Claim:** "plane-proxy is this row: its work-item tools expose `parent` only." "A child is a match only when the stored record equals the frozen draft. Compare the title, the parent, and each body section… text that differs is a mismatch. Fixing it would edit the body, so halt. A success response whose stored body is not the body that was sent is the same mismatch." Phase 4 prints `FILED` only when every stored body matches that draft, and create-only forbids rewriting the child.
**Why this is wrong:** The text path is the fleet's tracker, and that tracker's tool results are not the strings the skill sends. `create_work_item` accepts `description_html` and returns `formatResponse` of the Plane body (`plane-proxy/src/tools.ts` lines 239 and 248–251). `formatResponse` wraps every `name` and `description_html` in `<external_content source="plane" trusted="false">` and entity-encodes `&`, `<`, and `>` (`plane-proxy/src/provenance.ts` lines 18–22, 40–45, and 79–80). The same wrapper is on retrieve and list. A successful create therefore comes back with a title and a description that are not the frozen `<PARENT-ID> <slug>: <short title>` or the markdown sections Phase 4 sent. Decision 12 treats that as a mismatch, stops further creates, does not print `FILED`, and forbids the edit that would repair it. The next run reads the same fenced fields and halts again. Local mode is unaffected. This contradicts Done when's tracker bullet: on a reachable tracker the piece is a Plane child (`native` or `text`). Text cannot finish.
**Suggested fix:** In Decision 12, define the text-mode compare on the unwrapped work item, not the raw tool string. If the integration fences `name` and `description_html` the way plane-proxy's `formatResponse` does, strip that fence and decode entities before the title parse and the section compare. Equality is the unwrapped title and the unwrapped body sections against the frozen draft. A fence that does not unwrap, or an unwrapped body that is not the sections that were sent, stays a mismatch. State that plane-proxy always returns those two fields fenced, so a raw equality check halts every successful text create. Keep create-only.

### F-2: The parent check rejects the only parent value plane-proxy accepts
**Severity:** P1
**Where:** spec.md:144 | spec § Decision 12; spec § Phase 4 — File
**Claim:** "A create result with no id, an error payload, a parent other than the spec's ticket, an omitted parent, or a null parent also stops. That row is not the slug's child." After create, keep the id only when "the parent is the spec's ticket." Phase 4's Parent section is "the parent id." The spec's ticket id is the filename stem `^[A-Z][A-Z0-9]*-[0-9]+$` (Decision 7).
**Why this is wrong:** plane-proxy's create `parent` is `z.string().uuid()` (`plane-proxy/src/tools.ts` line 242). Retrieve-by-identifier returns the work item's `id`, which is that UUID, and `list_work_items` returns `parent` as that UUID. The identifier `VHS-45` is not a UUID, so a create that follows the spec's phrase and sends the ticket id is an error payload and Decision 12 stops with nothing filed. A create that sends the UUID then fails the read-back check if "the spec's ticket" means the identifier, which is the only parent token the spec defines. Either reading stops the text path before `FILED`. Decision 12 never says to compare the API parent to the retrieved work-item id.
**Suggested fix:** After retrieve-by-identifier, the work-item `id` is the only create `parent` and the only accepted read-back parent. Say that this id is a UUID on plane-proxy and is not the identifier string. The body Parent section shows the identifier. Compare the API parent to the retrieved id, and compare the Parent section to the identifier. An omitted, null, or other parent still stops.

### F-3: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec implements Plane ticket VHS-45. The brief says its Done when list is transcribed from the ticket.
**Why this is wrong:** No MCP memory tool is available in this session, so `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-45` could not be run. Review used the brief and the repo. If the ticket's acceptance criteria differ from the brief, that conflict was not checked.
**Suggested fix:** None in the spec. Re-cache the work item into a namespace this reviewer can read if the ticket text must be confirmed.

## Summary
P0: 1 | P1: 1 | P2: 0 | P3: 1 | P4: 0

STATUS: RED P0=1 P1=1 P2=0 P3=1 P4=0
