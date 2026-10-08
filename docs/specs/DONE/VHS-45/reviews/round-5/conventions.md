# Conventions Review — round 5

Delta-scoped pass over the sections rewritten after the 2026-10-08 operator decision (Decision 3, Decision 12, Skill outline, Phases 0, 1, 3, 4, the tracker checklist bullets, two Out-of-scope bullets, the Deferred (P2+) row, and the Decision 11 sentence removal). No P0 or P1. Three P2 clarity items, all one-sentence edits.

Grounding this round:

- Read fresh: the spec, the brief, `AGENTS.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `lint.py`, `tests/test_lint.py`, and the three round-4 reports.
- Sibling tracker phrasing read in `skills/spec-brief/SKILL.md` (lines 53, 63, 64), `skills/ship-spec/SKILL.md` (lines 40, 219 to 229, 265), and `skills/spec-close/SKILL.md` (lines 31, 61, 75, 335 to 340, 431, 432).
- Wiki: `projects/vigil-skills/state.md` and the overlapping decisions (`2026-06-14-vhs-17-requires-tolerated-not-strict-yaml.md`, `2026-09-02-plane-records-live-in-project-namespaces.md`, `2026-06-16-infra-23-provenance-fencing.md`). There is no `architecture.md` for this project.
- Reference wording: `mattpocock/skills` `skills/engineering/to-tickets/SKILL.md` fetched and compared against the rewritten sections.
- Ticket lookup: `memory_search` on namespace `skills`, tags `plane_work_item` and `VHS-45`, returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The brief is the ticket text for this pass.
- No closure manifest was passed. `scale_lens` is off. The spec has no `## Deferred — follow-up required` section, so there is no routing-row check; `## Deferred (P2+)` is the P2 carry heading.

What checked out in the rewritten sections:

- **Lint.** The `requires:` block in Decision 11 (`filesystem: [read, write]`, `services: [issue-tracker?]`) passes `lint.py` R1. The outline's "Tool-use notes" heading matches `_NOTES_HEADING_RE`, and the tagged-example wording "or the equivalent in your host" matches `_CASE2_TAG`. The census is still 11 `skills/*/SKILL.md` files, so 12 is right.
- **Capability naming.** The outline names capabilities (retrieve-by-identifier, list children of a parent, work-item create with parent, create a blocked-by relation on the dependent) and no tool. That matches contract §4 and is the same construction `spec-brief` line 64 uses ("the issue tracker's retrieve-by-identifier capability"). It is more role-neutral than the "plane-proxy's … capability" phrasing in `ship-spec` and `spec-close`.
- **Skill shape.** The section order (Invocation, Phases 0 to 4, never-does list, Tool-use notes, Failure modes) is `spec-brief`'s order.
- **Local file name.** `<PARENT-ID>.ticket-<slug>.md` falls under `spec-close` line 340 ("any other companion `<TICKET-ID>.<rest>` → `<rest>`"), as Phase 4 claims.
- **Original text.** The rewritten sections do not reuse the reference skill's wording. The shared items are generic section names (Parent, Acceptance criteria, Blocked by) and the rule that a native-edge ticket has no Blocked by section, stated in the spec's own words. The empty-set sentinel, the file layout, and the failure text are the spec's own. Decision 4's banned-phrase list still holds.
- **Leftover machinery.** None of the removed protocol remains in the scoped sections: no response field names, no fence unwrap, no paging rule, no slug-in-title match, no read-back, no temp file or rename.
- **Premature abstraction.** None added. The multi-integration prompt is justified at N=2 on this fleet (plane-proxy and the official Plane tools are both connectable).

## Closure of round 4 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Slug identity still matches the raw fenced title, so text mode never keeps a child | CLOSED | The slug-match and keep rules are gone. spec § Decision 12 lines 143 to 145: stop on failure, no resume, a second run files every piece again. Line 57: the tracker name is the short title; the slug is only in the approval block and the local file name. |
| correctness | F-2 (P1) | Native read-back takes `object.id`, but the relations list identifies the work item as `issue_id` | CLOSED | No read-back. spec § Decision 12 line 133 ("does not read its own writes back") and § Skill outline line 157 ("names no tracker response field"). |
| correctness | F-3 (P3) | ticket not cached | CLOSED | Not a spec defect. Lookup was attempted this round and denied by ACL; see grounding. Not re-filed. |
| edge-cases | F-1 (P0) | A fenced child title is "some other piece", so text mode creates another child | CLOSED | Same removal as correctness F-1. |
| edge-cases | F-2 (P1) | The official relation list has no top-level `blocked_by` | CLOSED | Same removal as correctness F-2. The only relation operation left is the create (line 53). |
| edge-cases | F-3 (P2) | A finished plane-proxy page still carries a cursor | CLOSED | No paging rule remains. The one list read is a count, reported as `unknown` when unavailable or failed, and "a notice, not a census" (line 145). |
| edge-cases | F-4 (P4) | Plane ticket text was not readable | CLOSED | Same as correctness F-3. |
| conventions | F-1 (P2) | The mode table still keys `text` off "not advertised" | CLOSED | spec § Decision 3 line 43: "The same, except it offers no such relation operation". The 404-probe rule it conflicted with is removed. |
| conventions | F-2 (P3) | Drift-check — round-4 pins with rationale | CLOSED | Every pin in that list (relation-list read, `description_html`, fence unwrap, UUID parent echo, project-field request, title-prefix parse) is removed. The replacement list is F-4 below. |

## Findings

### F-1: Done when cites Decision 3 for a rule that now lives in Decision 12
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:264 | spec § Done when (third bullet)
**Convention violated:** A fold reaches every place that states the rule (the VHS-37 propagation-site rule). This bullet sits outside the rewritten sections and was missed.
**Evidence:** Line 264: "Decision 3's rule that create-before-edge is not a build order". After the rewrite Decision 3 has no such rule and the phrase "create-before-edge" appears nowhere else. The rule is in § Decision 12, Order, line 139: "This order exists so that identifiers exist. It is not a build order". Decision 3 line 55 only points at it.
**Suggested fix:** Change the clause to: "and Decision 12's rule that the blockers-first filing order is not a build order".

### F-2: Decision 3 names the departure from the contract but not the narrowing of the brief
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:44–47 | spec § Decision 3 (`local` and `halt` rows, and the paragraph under the table)
**Convention violated:** A spec-level change to a brief decision is stated as one, with its reason, so the drift-check sees it.
**Evidence:** Brief line 27: "With no tracker reachable, the skill writes one local file per ticket." The spec takes `local` only when no integration is connected, and halts when a connected integration "does not answer" or "returns an error", which is a tracker that is not reachable. Line 47 gives the reason and cites portability-contract §3, but the decision is still headed "Brief Decision 3" with no mention that the brief's wording was narrowed. The reason itself is sound and matches the reference skill, where local files are a configured storage choice and not a failure fallback. This rule has stood since round 2, so it is a labelling gap and not a new change of direction.
**Suggested fix:** Add one sentence after line 47: "This also narrows the brief's 'no tracker reachable' to 'no issue-tracker integration connected'; a connected tracker that fails is `halt`, for the same reason."

### F-3: The existing-work read is described three different ways
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:145, 167, 184, 276 | spec § Decision 12 (No resume), § Phase 1, § Phase 3, § Out of scope
**Convention violated:** One rule, one statement. An implementer has to reconcile these by hand.
**Evidence:**
- Line 145 says Phase 1 makes the read in every mode: "the parent's children when the integration can list them, or the files matching `docs/specs/TODO/<PARENT-ID>.ticket-*.md`".
- Line 167 says "On a tracker mode it also resolves the parent and makes the one existing-work read", which reads as tracker modes only. The approval block at line 184 has a `local` count.
- Line 276 puts "detecting an earlier run's children" out of scope, while line 145 lists the parent's children. The two agree only if the reader works out that the count covers all children and does not attribute any to an earlier run.
- No line says what the block prints on `halt`.
**Suggested fix:**
- Line 167: "It resolves the parent on a tracker mode, and in every mode except `halt` it makes the one existing-work read (Decision 12). On `halt` the block prints `unknown`."
- Line 276: replace "detecting an earlier run's children" with "telling an earlier run's children apart from other children (the Phase 1 count does not)".

### F-4: Drift-check — round-5 commitments with rationale
**Severity:** P3
**Where:** spec § Decision 3; spec § Decision 12; spec § Phase 3; spec § Phase 4
**Convention violated:** None. Class (c). Brief Decisions 1 to 8 and Risks 1 to 3 still authorize the frame. None of the items below is a silent addition; each has its reason in the spec or is the operator decision dated 2026-10-08 in § Decision 12.
**Evidence:** The round-4 pin list is void (closure table above). The rewrite commits to the following, none of which the brief states:
- **Decision 12, operator decision.** No read-back, no resume, no response-shape handling. Filing is blockers first, one piece at a time, create-only. The first error stops the run with no retry and no mode switch.
- **Decision 12, stop report.** Each piece is `created <identifier or path>` or `not created`, each edge `written` or `not written`, then the failing operation and its error. `FILED` prints only when every write succeeded.
- **Decision 12, existing-work notice.** One read in Phase 1, shown as a count or `unknown`, with a warning line when the count is above zero. It adds one capability, list children of a parent, that the reference skill does not have. It is the replacement for the removed resume guard and it gates nothing.
- **Decision 12, `local` never overwrites.** An existing target path removes option 1.
- **Decision 12, parent and project references.** They come from the retrieve-by-identifier, with `halt` before approval when one is missing. The skill does not consult shared memory (reason given in Decision 10) and does not read `states.json` (no reason given). `ship-spec` line 226 and `spec-close` line 61 take `project_id` from `states.json`. Leaving it out fits a tracker-neutral skill, but it is a departure from the sibling pattern.
- **Decision 3, references and titles.** A `text` reference is the identifier and title, a `local` reference is the file name and title, the approval block shows slugs, and the tracker name and local H1 are the short title.
- **Decision 3, halt instead of warn-and-proceed.** Contract §3 and §5 dimension 2 say a missing optional service warns and proceeds. The spec halts on a connected tracker that fails, says so, and gives the reason. `requires:` keeps `issue-tracker?`, which is still accurate because the not-connected case degrades to local files.
**Suggested fix:** No edit required. Optional: add the reason for skipping `states.json` to line 137, for example "it is a Plane-specific file and this skill is tracker-neutral".

### F-5: Decision 12 carries review history in normative text
**Severity:** P3
**Where:** spec.md:135 | spec § Decision 12 (second paragraph)
**Convention violated:** `AGENTS.md` keeps process records in the reviews tree and the closure manifest, and the repo's "delete it cleanly" habit applies to removed design as well as removed code. `/ship-spec` and `/spec-close` read this paragraph as part of the decision.
**Evidence:** "Rounds 1 to 4 grew a read-back and resume protocol in this decision, and that protocol pinned one tracker's response shapes. It is removed. … Every round-4 P0 and P1 finding was against that protocol and closes with its removal." The first half is supersession rationale and belongs. The last sentence is a closure claim about review findings, which is the manifest's job.
**Suggested fix:** Keep the date, the decision, and the reason (the protocol pinned one tracker's response shapes). Move "Every round-4 P0 and P1 finding … closes with its removal" to the closure manifest.

### F-6: Phase 4 re-runs a gate on a draft that cannot have changed
**Severity:** P4
**Where:** spec.md:206 | spec § Phase 4 — File
**Convention violated:** No step without a stated purpose.
**Evidence:** "Re-run the Decision 5 gate on that frozen draft, then file". Option 1 is printed only when that gate passes, and the frozen block is the only input. The one thing that can change between approval and filing is the filesystem, which is Decision 12's overwrite rule and not Decision 5's gate.
**Suggested fix:** Either delete the clause, or replace it with "Re-check that no `local` target path exists (Decision 12), then file".

## Outside the delta scope — noted, not counted

Both are in Decision 10, which was not rewritten this round. They concern text that ships into tracked docs, and the second one touches the rewritten Decision 3.

- spec.md:108. The README bullet is given verbatim and contains "the tracker is optional per Decision 3". "Decision 3" means nothing in `README.md`. Drop "per Decision 3" from the bullet; the parenthesis already states the rule.
- spec.md:107. The AGENTS.md sentence "It uses the tracker when the Decision 3 probe succeeds, and otherwise writes local files" contradicts Decision 3, where a failed probe on a connected tracker is `halt`. If that sentence is meant as doc text, say "and writes local files only when no issue-tracker integration is connected".

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 2 | P4: 1

STATUS: GREEN
