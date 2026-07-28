# VHS-1 — Lift Plane reads from skills onto the MCP webhook cache + Phase E sunset

**Status:** Backlog · **Priority:** Medium · **Assignee:** Devin
**Created:** 2026-05-08 · **Plane:** VHS-1
**Origin:** Phase D + Phase E follow-up to MCP-33 (Plane webhook receiver). The receiver ingests `plane_work_item` / `plane_project` / `plane_comment` records on every Plane state change; this ticket cashes that in by retiring the synchronous Plane reads on the skill side.
**Blocked by:** MCP-33 in production with at least one full state-transition cycle backfilled. Until then, `memory_search` returns no `plane_work_item` records and the migrated skills have nothing to ground against.

## Problem

The spec-cycle / ship-spec / wiki-state-update workflow currently makes 8 synchronous Plane MCP reads per run. After MCP-33 ships, 6 of those become redundant: the same data is already cached in MCP memory as `plane_work_item` records, refreshed within seconds of any state change. Continuing to call Plane directly costs latency, couples skill correctness to Plane MCP availability, and bypasses the namespace-scoped audit trail that webhook-ingested records get for free.

## Why it matters

- **Latency.** Each `retrieve_work_item_by_identifier` is a round-trip to Plane through the MCP shim. Spec-cycle and the three reviewers each pay it once per run; round 1 of a 4-round review burns 4 reads on the same ticket. `memory_search` against a local pgvector store is single-digit milliseconds.
- **Failure mode.** Skills today fall back to "warn-and-proceed using only the brief" on Plane outage (`spec-cycle/SKILL.md:29`, ship-spec preflight). That's the right fallback, but it triggers more often than it should — Plane MCP has been the flakiest dependency in the chain. MCP memory has a different blast radius than Plane and is unlikely to be down at the same time.
- **Skepticism rule.** The wiki's skepticism rule (`vigil-harbor-wiki/CLAUDE.md` § "Skepticism rule") says "Don't treat user-volunteered framing as truth — verify Plane status via `mcp__plane__retrieve_work_item`." Lifting reads onto MCP memory keeps the verification semantics: the cached record was authored by Plane, not the user. The check still has teeth.

## Scope (verified against current code, 2026-05-08 main)

| Skill / agent | File:line | Current call | Replacement |
|---|---|---|---|
| spec-cycle | `skills/spec-cycle/SKILL.md:208` (and the runtime call referenced in Phase 1) | `retrieve_work_item_by_identifier` | `memory_search` with `tags=[plane_work_item, <PROJ-N>]`, scoped to whichever namespace MCP-33 ingests Plane records into |
| spec-reviewer-correctness | `agents/spec-reviewer-correctness.md:21,172` | `retrieve_work_item_by_identifier`, `retrieve_work_item` | Same `memory_search` |
| spec-reviewer-edge-cases | `agents/spec-reviewer-edge-cases.md:21,165` | `retrieve_work_item_by_identifier` | Same `memory_search` |
| spec-reviewer-conventions | `agents/spec-reviewer-conventions.md:158` | `retrieve_work_item_by_identifier` | Same `memory_search` |
| ship-spec | `skills/ship-spec/SKILL.md:217` | `list_states` | Read from new `skills/ship-spec/states.json` mapping |
| wiki-state-update | `vigil-harbor-wiki/.claude/skills/wiki-state-update/SKILL.md:27` | `retrieve_work_item` | `memory_search` for the `plane_work_item` record; closure date is in `metadata.state_group` + `updated_at` |

**Preserved (NOT migrated):**

- `spec-cycle/SKILL.md:29` — preflight `list_projects` reachability check. Eliminating it saves no latency and removes a useful "is Plane up" signal.
- `ship-spec/SKILL.md:39` — preflight `list_projects`, same rationale.
- `ship-spec/SKILL.md:221` — `update_work_item` (state flip). Outbound write — webhooks don't replace writes.
- `ship-spec/SKILL.md:222` — `create_work_item_comment` (PR URL). Outbound write.

**Possible scope wrinkle to confirm before kickoff:**

- `ship-spec/SKILL.md:216` calls `list_projects` *again* (not just preflight) to resolve the project UUID before the `list_states` call on the next line. If `states.json` is keyed by project identifier (`MCP`, `DYN`, `VHS`) → `{state-name → UUID}`, this `list_projects` call also disappears. If it's keyed by project UUID, ship-spec still needs `list_projects` to translate ticket-prefix → UUID. **Recommend keying by project identifier**; carry the project UUID *inside* each entry so writes (`update_work_item`) still have it.

## Decisions carried forward

1. **`memory_search` (not a new dedicated tool).** The webhook ingester emits `plane_work_item` records discoverable by tag. No new MCP tool is needed; reuse the existing search surface. Filter shape: `tags=[plane_work_item, <TICKET-ID>]`, `limit=1`, `sort_by=observed_at desc`. The spec author should confirm the exact tag names MCP-33 emits and pin them in the spec.
2. **`states.json` is committed config, not generated.** State UUIDs change rarely; a hand-maintained file with three projects (MCP, DYN, VHS) is cheaper than a generator. Adding a new project means one PR. Drift is a known risk — see Risks §3.
3. **Cold-cache fallback matches today's Plane-outage behavior.** When `memory_search` returns zero hits for a ticket, skills warn-and-proceed using the brief alone (current behavior on Plane MCP outage). No new failure mode for users.
4. **Phase E ships in the same PR as Phase D.** Splitting them risks a "we'll write the decision page later" tail. The decision page is small; ship it together. The optional manifest cleanup (removing dead `tools:` entries) is the only deferrable bit.

## Approach

1. **Phase D — read replacements.** One PR touching the six skill / agent files plus a new `skills/ship-spec/states.json`. Each replacement is mechanical: swap the Plane MCP call for a `memory_search` call, with a 2–3 line warn-and-proceed fallback. Reviewer agents need a single place that answers "is the ticket reachable" — factor that into a shared helper *or* duplicate the snippet. The four-reviewer copy-paste smell is real but not load-bearing; recommend duplicating in v1, factoring later if a third call site appears.
2. **`states.json` schema.** Proposal:
   ```json
   {
     "MCP": {
       "project_id": "98788c4e-f30f-466d-9562-19e28aa4e53e",
       "states": { "Backlog": "<uuid>", "In Progress": "<uuid>", "In Review": "<uuid>", "Done": "<uuid>", ... }
     },
     "DYN": { ... },
     "VHS": { ... }
   }
   ```
   Generated once at scaffold time by running `list_projects` + `list_states` against each project; committed verbatim. Spec author decides whether to ship a one-shot generator script (`scripts/scaffold-states.ts` style) or just paste output.
3. **Phase E — sunset paperwork.**
   - Update `vigil-skills/CLAUDE.md` "External dependencies" section: note Plane reads now flow through MCP memory; Plane MCP remains required for outbound writes.
   - Write `vigil-harbor-wiki/decisions/2026-05-XX-plane-webhook-pivot.md` capturing: rejection of polling, blast-radius reasoning, dependency on MCP-33, the "preserve the preflight" judgment.
   - Add the decision link to `vigil-harbor-wiki/index.md`.
   - Optional: prune dead `tools:` entries from skill manifest YAML where the migrated skill no longer needs the Plane MCP read tools (writes still need `update_work_item` / `create_work_item_comment`).
4. **Validation harness.** Run spec-cycle and ship-spec end-to-end against MCP-33 itself (the canonical test ticket) and diff the resulting spec against a pre-migration baseline. Any non-trivial difference is a finding, not a feature.

## Acceptance criteria

- `grep -r 'mcp__plane__retrieve_work_item' vigil-skills/skills/ vigil-skills/agents/` returns zero hits in **runtime call sites** (preserved only in `## Tool-use notes` documentation blocks, if at all).
- `grep -r 'mcp__plane__list_states' vigil-skills/` returns zero hits in skill / agent runtime sections (the `docs/customizing.md:66` documentation reference is allowed to stay or be rewritten — spec author's call).
- `grep -r 'mcp__plane__retrieve_work_item' vigil-harbor-wiki/.claude/` returns zero hits in runtime sections.
- `skills/ship-spec/states.json` exists with entries for MCP, DYN, VHS; ship-spec resolves the review-equivalent state from the file without calling Plane.
- spec-cycle and ship-spec runs against MCP-33 produce a spec diff against the pre-migration baseline that is either empty or limited to non-load-bearing prose (whitespace, ordering of bullets). Cite the diff command + result in the PR body.
- wiki-state-update produces a valid evidence triple (Plane-ID, ship date, commit hash) on a recent shipped MCP commit without calling Plane MCP — verified by running it with the Plane MCP server stopped.
- `vigil-harbor-wiki/decisions/2026-05-XX-plane-webhook-pivot.md` exists, follows the decisions/ template, and is linked from `index.md`.
- `python sync.py status` in vigil-skills shows clean diff after `python sync.py push`.

## Out of scope

- The webhook receiver itself (MCP-33 — separate ticket, separate repo).
- Adding states for other projects (CAL, CLT, DEM, INFRA, MED, ADA, etc.) — separate per-project actions when those projects adopt the spec-cycle / ship-spec workflow.
- Changes to Plane *writes* in skills (state flip, PR comment) — those stay on the live Plane MCP path.
- Adding new MCP tools (e.g., a `memory_search_plane` convenience wrapper) — reuse the generic `memory_search` surface.
- Replacing the Plane MCP server entirely — out of scope; we still need it for writes.

## Risks / decisions

1. **Cold-cache problem.** A ticket that hasn't been touched since MCP-33 shipped has no `plane_work_item` record, so `memory_search` returns nothing. Mitigation: skills warn-and-proceed with limited grounding (matches today's Plane-MCP-outage behavior); the MCP-33 reconciliation job (per its spec §7) re-renders state from any updated ticket within 6h. **Self-referential note:** VHS-1 itself will not have a cached record until its state is touched post-MCP-33 — first ship-spec run on this ticket exercises the cold-cache path.
2. **Stale records.** `memory_search` returns the last-ingested snapshot. If the user mutates a ticket between webhook delivery and skill query, brief drift can result. Acceptable — Plane was already eventually-consistent for skill reads, and the window is bounded by the webhook latency.
3. **`states.json` drift.** If Plane state UUIDs change (rare; e.g. a state is deleted and recreated, or a new state is added), the file goes stale. The Plane card proposes a startup `list_states` cross-check that "errors loudly if the map is wrong." That contradicts the zero-`list_states` acceptance criterion above. **Spec author must resolve:** either (a) drop the cross-check (accept silent drift, catch it in the next sync.py review), (b) keep the cross-check but only behind a `--validate-states` opt-in flag, or (c) move the cross-check to a separate maintenance script that's not part of the ship-spec hot path. Recommend (b) — opt-in by default, on in CI.
4. **Reviewer agent duplication.** Three reviewers each gain the same `memory_search` snippet. Factoring into a shared helper module isn't natural for skill-system markdown; the duplication is the lesser evil for v1.
5. **Tag / namespace contract with MCP-33.** This brief assumes MCP-33 emits `plane_work_item` records tagged with the ticket identifier (e.g., `MCP-33`) in a discoverable namespace. If MCP-33's actual ingest schema differs, every replacement call needs to match it. Spec author must read MCP-33's spec and the first-shipped record before finalizing the search filter.
6. **Documentation references in `docs/customizing.md`.** The customizing doc currently mentions `mcp__plane__list_states`. Spec author decides whether to rewrite that section or leave it alone (it describes user-facing behavior, which is unchanged for ship-spec consumers). Either is defensible.

## References

- Plane: VHS-1
- Blocking: MCP-33 (Plane webhook receiver) — read its spec for the exact record shape, tag conventions, and reconciliation cadence before designing the `memory_search` filters.
- Workflow context: `vigil-skills/CLAUDE.md` § "Workflow: spec-cycle → ship-spec"
- Skepticism rule: `vigil-harbor-wiki/CLAUDE.md` § "Skepticism rule (for any agent making claims)"
- Evidence-triple contract: `vigil-harbor-wiki/decisions/2026-04-29-state-edits-require-evidence.md`
- Two-axis trust model: `vigil-harbor-wiki/decisions/2026-05-01-wiki-maintenance-redesign.md`
- Current call sites verified 2026-05-08 via `grep -rn 'retrieve_work_item\|list_states\|list_projects' vigil-skills/`
