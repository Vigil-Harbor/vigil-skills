# VHS-13 — Patch /wiki-after-merge: maintain project-hub index tables + guard relative-link depth

**Status:** Backlog · **Priority:** Medium · **Assignee:** Unassigned
**Created:** 2026-06-14 · **Plane:** VHS-13
**Origin:** Two recent Petasos after-merge runs (5989f35 / PET-110, dd4b9c2 / PET-111) correctly created or skipped their comprehension entries per the Step 6 routine, but left the matching row in `projects/petasos/petasos-hub.md` missing. The gap was caught only by an out-of-band, later-abandoned backfill (c53b33a) that also fixed a second broken relative link in `architecture.md`. The skill mutates five files after a merge but never touches the per-project hub that carries the Decisions and Comprehension index tables, so those tables drift silently.

## Problem

`/wiki-after-merge` (`vigil-harbor-wiki/.claude/skills/wiki-after-merge/SKILL.md`, 131 lines) writes `log.md` (Step 4), `filemap.md` (Step 5), the comprehension entry (Step 6), `state.md` (Step 7), and `overview/learnings.md` (Step 7d), and stages them in a single atomic commit (Step 8). It does **not** write `projects/<X>/<x>-hub.md`, which maintains its own newest-first **Decisions** and **Comprehension** tables plus a `> Last updated:` line.

Verified against the live wiki (2026-06-14):

- `projects/petasos/petasos-hub.md` carries a `## Decisions` table (24 rows) and a `## Comprehension` table, both linking entries with the two-level `../../` prefix because the hub sits at depth two (`projects/petasos/`). Step 8's staging list (`SKILL.md:99`) names `log.md`, `filemap.md`, `state.md`, and the comprehension entry — the hub file is absent.
- The skill creates **comprehension** entries (Step 6) but does not create **decision** entries; the only decision-table contact today is Step 7d's supersession scan (`SKILL.md:95`), which already reads "titles + the hub/project-hub decision tables." So the hub-row insert has a clear home for comprehension (fold into Step 6) but a narrower one for decisions (the promotion/supersession path), and the brief should not assume a decision is created on every run.

### Secondary bug (same area)

Project docs two levels deep (e.g. `projects/petasos/architecture.md`) have repeatedly shipped single-dot relative links `](../decisions/…)` / `](../comprehension/…)` where the correct depth is `](../../…)`. Two such links existed in `architecture.md` (the PET-107 and PET-109 decision links); the out-of-band edit fixed one and missed the other before c53b33a closed the gap. As of this brief, `grep -rn "](\.\./decisions/\|](\.\./comprehension/" projects/` returns **zero** matches — the known instances are already fixed, so this is regression-prevention, not an outstanding defect.

### What the lint already does (scope-narrowing — verify before duplicating)

`wiki-lint.mjs` already covers part of the proposed safety net; the spec author must build on it rather than add a parallel check:

- **DEAD_LINK** (`wiki-lint.mjs:234`, severity `error`) resolves every markdown link with `resolve(fileDir, link)` and flags non-existent targets. A single-dot `](../decisions/…)` from `projects/petasos/architecture.md` resolves to the non-existent `projects/decisions/…` and is **already** an error. The link-depth bug is therefore caught the next morning — what's missing is (a) an actionable "wrong depth, use `../../`" message, and (b) catching it *in the skill before the commit* rather than a day later.
- **INDEX** (`wiki-lint.mjs:443–451` comprehension, `:715–723` decisions, severity `info`) already flags entries "not listed in `vigil-harbor-hub.md` or any project hub" table. Two real limits: it's `info` (non-alarming), and it's satisfied by indexing in **either** the global hub **or** any project hub — an entry indexed only in `vigil-harbor-hub.md` but missing from its own project hub passes. The actual gap is *per-project-hub* enforcement, not "indexed somewhere."

## Proposed direction (do not pre-decide in this brief)

1. **Hub-index maintenance (primary).** When Step 6 creates a comprehension entry — and when the decision-promotion/supersession path adds or supersedes a decision — insert a newest-first row into the matching table in `projects/<X>/<x>-hub.md`, bump the hub's `> Last updated:`, and stage the hub file in the Step 8 atomic commit. Links must use the `../../` prefix. Idempotent: grep-skip if the row already exists; cross-check against `ls comprehension/ | grep <proj>-` (and the decisions equivalent) before assuming the table is complete.
2. **Link-depth guard.** In the skill (or as a lint rule) reject single-dot `](../decisions/` / `](../comprehension/` links inside `projects/<X>/*.md` with a message naming the correct `../../` depth, and verify every decision/comprehension link in the hub and project docs resolves to an existing file. Reuse/upgrade DEAD_LINK rather than duplicating its resolution logic.
3. **Lint safety net (optional).** Rather than add a new check, raise the existing INDEX check so a `comprehension/` or `decisions/` file that is missing **from its own project hub** is flagged (today it passes if indexed anywhere). Decide the severity (likely `warn`, matching the autofix-eligible "missing index entries" tier from the 2026-05-01 redesign).

## Decisions carried forward

- **Idempotency is non-negotiable.** Every new write must survive a same-SHA re-run with no duplicate rows and no double-bumped dates, consistent with the skill's existing idempotency contract (`SKILL.md:103–112`).
- **Single atomic commit.** New hub mutations join Step 8's existing commit; do not introduce a second commit or a pre-confirmation write (the skill commits only if all sub-steps succeed — `SKILL.md:98`).
- **Public-repo boundary.** `/wiki-after-merge` lives in the internal `vigil-harbor-wiki` repo, not in this public `vigil-skills` repo. This ticket is tracked in VHS but the change ships in the wiki repo's skill; keep vigil-skills free of any dependency on wiki-repo internals (per CLAUDE.md and the VHS-12 precedent).
- **Build on the lint, don't fork it.** DEAD_LINK and INDEX already exist; extend them. A parallel checker would create the duplicate-code finding the conventions reviewer is built to catch.
- **Hubs are discovered dynamically.** `wiki-lint.mjs:78` already derives hub files via the `projects/<x>/<x>-hub.md` pattern; the skill's hub lookup should resolve the same way, not hard-code per-project paths.

## Done when

- A `/wiki-after-merge` run that creates a comprehension entry (or promotes/supersedes a decision) leaves the matching project-hub index table current — correct `../../` links, newest-first row, `Last updated` bumped — in the **same atomic commit**, and re-running on the same SHA proposes zero further changes.
- Single-dot `](../decisions/` / `](../comprehension/` links inside `projects/<X>/*.md` are caught (the skill refuses, or the lint flags them with the correct-depth hint), and every hub/project-doc decision and comprehension link resolves to an existing file.
- The per-project-hub indexing gap is closed: a comprehension/decision file missing from its own project hub is surfaced (decide skill-time, lint-time, or both), without regressing the existing global-hub INDEX behavior.
- The skill's idempotency contract section and Step 8 staging list are updated to name the hub file; `SKILL.md` "Related" / cross-references stay consistent.
- Wiki lint runs clean on a representative post-merge commit; the manual backfill that c53b33a performed is reproducible by the skill alone.

## Out of scope

- Backfilling other project hubs (`mcp-server`, `calvin`, `dynasty`, etc.) that may carry the same drift — operational cleanup, run the patched skill/lint over them once it ships, not skill-design work.
- Any change to Step 7c (Plane sibling reconciliation) or the evidence-triple / `/wiki-state-update` machinery.
- Restructuring the hub page template or the Decisions/Comprehension table schema beyond adding rows.
- Creating decision entries from scratch inside `/wiki-after-merge` (the skill scaffolds comprehension, not decisions; this ticket only maintains the index when a decision already enters via the promotion/supersession path).
- Changes to the public `vigil-skills` spec-lifecycle skills (`/spec-cycle`, `/ship-spec`, `/spec-close`).

## References

- Plane: VHS-13 (created 2026-06-14, priority Medium)
- Skill source: `vigil-harbor-wiki/.claude/skills/wiki-after-merge/SKILL.md` (131 lines, read 2026-06-14) — Step 6 (`:50`), Step 7d supersession (`:92–96`), Step 8 staging (`:98–101`), idempotency contract (`:103–112`)
- Hub under-maintenance: `projects/petasos/petasos-hub.md` — `## Decisions` / `## Comprehension` tables, `../../` links (read 2026-06-14)
- Lint: `wiki-lint.mjs` — DEAD_LINK (`:234`, error), INDEX comprehension (`:443–451`, info) + decisions (`:715–723`, info), dynamic hub discovery (`:78`)
- Commits: c53b33a (the manual backfill this ticket automates — added the PET-111 hub comprehension row, fixed the second `architecture.md` link); 5989f35 (PET-110 after-merge) and dd4b9c2 (PET-111 after-merge) exposed the gap — all three verified present in wiki history 2026-06-14
- Precedent: `decisions/2026-05-01-wiki-maintenance-redesign.md` (Tier-1 mechanical autofix covers "missing index entries"); MERGE_DRIFT daily safety-net model (`COWORK-LINT-CRON.md`)
