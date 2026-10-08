# Conventions Review — round 4

The five round-3 P0/P1 folds are in the spec. One mode-table cell still states the old `text` rule, and the new pins are class (c).

## Closure of round 3 findings

No `## Deferred — follow-up required` section, so there is no routing-row check. `## Deferred (P2+)` is the P2 carry heading. `scale_lens` is off; no scalability report was read. All five manifest lines match the current spec. `skills/*/SKILL.md` is still 11 files, so 12 after `spec-tickets` still matches § Decision 11 and `tests/test_lint.py`.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Text-mode success never matches the frozen draft on plane-proxy | CLOSED | spec § Decision 12: body is `description_html`; a later read requests that field; the create echo is not the proof; compare after stripping a plane-proxy `<external_content source="plane" trusted="false">` fence, decoding `&` `<` `>`, and one HTML wrapper. § Phase 4 — File: skip uses that unwrap, not the raw tool string. § Test plan restates the fence, the entity decode, and the one HTML wrapper. Three sites; fold kept. |
| correctness | F-2 | The parent check rejects the only parent value plane-proxy accepts | CLOSED | spec § Decision 12: the retrieved work-item `id` is the only create `parent` and the only accepted API parent; on plane-proxy it is a UUID, not the identifier. Accept `parent` or `parent_id`. An omitted parent on the create echo does not stop by itself. § Phase 4 — File: the Parent section is the identifier, not the UUID. § Test plan restates both. Three sites; fold kept. |
| correctness | F-3 | ticket not cached | CLOSED | Not a spec defect. No MCP memory tool is available this round. The brief's Done when (lines 34–42) remains the acceptance text. Not re-filed. |
| edge-cases | F-1 | The relation proof reads the work item, which never carries blocked_by | CLOSED | spec § Decision 3: a relation-list read and a relation-create operation are required; the enum token does not qualify; a 404 at probe time takes `text` when create and parent work, before any create. The proof read is the relation list. § Decision 12: an empty list is the empty set; a work-item body with no `blocked_by` key is not that read; a failed read-back does not write the same edge again and does not switch mode. § Test plan restates it. Three sites; fold kept. |
| edge-cases | F-2 | The body the match requires is not in the work-item read | CLOSED | Same three sites as correctness F-1. An empty requested `description_html` is cannot-read and does not print `FILED`. |
| edge-cases | F-3 | A missing project field halts, and the default retrieve has no such field | CLOSED | spec § Decision 12: request the project field; accept `project` or `project_id`; halt only when the requested field is absent or unequal; a body that never asked for the field is not "missing". One site; fold kept. |
| edge-cases | F-4 | A rewritten title is invisible on the next run, so resume creates a second child | CLOSED | spec § Decision 12: before any create, including on resume, a child whose title starts with `<PARENT-ID> ` but does not parse as `<PARENT-ID> <slug>:` is cannot-read. A rewrite that drops the prefix is stated as indistinguishable from another piece; create-only does not delete it. |
| edge-cases | F-5 | "The spec's ticket" is not the parent value the tracker returns | CLOSED | Same edit as correctness F-2. |
| edge-cases | F-6 | Plane ticket text was not readable | CLOSED | Same as correctness F-3. Not re-filed. |
| conventions | F-1 | Drift-check — round-3 pins with rationale | CLOSED | No edit was required. Pins that later P0/P1 folds had to change (a missing `blocked_by` key is not the empty set; an omitted create-echo parent does not stop by itself) are replaced in § Decision 12 with the rationale next to the new rule. The other pins are still in the spec. New pins are F-2 below. |

## Findings

### F-1: The mode table still keys `text` off "not advertised"
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3 (mode table, `text` row)
**Convention violated:** The fold has to reach every place that states the rule. § Decision 3's prose and the test plan were updated; the table's When cell was not.
**Evidence:** The paragraph above the table says a `blocked_by` token is not enough, and that a missing operation or a 404 takes `text` when create and parent work. The `text` row still says "The same, except `blocked_by` is not advertised". Read as the schema token, a token-plus-404 integration is neither `native` nor that `text` row. § Test plan already requires `text` for that case.
**Suggested fix:** Change the `text` When cell to: the same conditions, except the relation-list read and the relation-create operation are absent, or a probe of that operation returns 404. Keep the plane-proxy sentence.

### F-2: Drift-check — round-4 pins with rationale
**Severity:** P3
**Where:** spec § Decision 3; spec § Decision 12; spec § Phase 4 — File; spec § Test plan
**Convention violated:** None. Class (c). Brief Decisions 1–8, `## Scale`, and Risks 1–3 still authorize the frame. Each item below is a review fix with the reason written next to it. No class (d) silent addition.
**Evidence:** The round-3 catalogue is still the baseline. These are the commitments added since that list. They match the portability contract's capability prose (no new operative `mcp__` call), INFRA-23's fence (`source="plane" trusted="false"`, entity-encode `&` `<` `>` only), and the live `states.json` `project_id` field. `requires:` stays `filesystem` plus `services: [issue-tracker?]`, which is the contract's optional-service form, and the §3 halt narrowing named in § Decision 3 is unchanged.
**Suggested fix:** No further edit beyond F-1. The new drift-check list is:

- **Decision 3 and Decision 12** — Native requires a relation-list read and a relation-create operation, not the enum token. A 404 at probe time takes `text` when create and parent work, before any create. The proof read is the relation list. An empty list is the empty set. A work-item body with no `blocked_by` key is not that read. A failed read-back does not write the same edge again and does not switch mode.
- **Decision 12 and Phase 4** — The body is sent as `description_html`. The create echo is not the proof. A later read must request that field. Empty on that read is cannot-read and does not print `FILED`.
- **Decision 12** — Compare after unwrapping a plane-proxy `<external_content source="plane" trusted="false">` fence, decoding `&`, `<`, and `>`, then stripping one HTML wrapper. A raw equality check is not the match.
- **Decision 12 and Phase 4** — The retrieved work-item `id` is the only create parent and the only accepted API parent. The body Parent section is the identifier string. Accept `parent` or `parent_id`. An omitted parent on the create echo does not stop by itself.
- **Decision 12** — Request the project field. Accept `project` or `project_id`. Halt only when the requested field is absent or unequal.
- **Decision 12** — Before any create, including on resume, a child title that starts with `<PARENT-ID> ` but does not parse is cannot-read. A rewrite that drops the prefix is not a second halt condition.

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 1 | P4: 0

STATUS: GREEN
