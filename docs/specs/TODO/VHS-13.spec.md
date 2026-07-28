# VHS-13 — Spec: maintain project-hub index tables in /wiki-after-merge + guard relative-link depth

**Ticket:** VHS-13 · **Brief:** `docs/specs/TODO/VHS-13.brief.md` · **Status:** Spec (authored 2026-06-14, revised round 2)
**Implementation repo:** `vigil-harbor-wiki` (internal) — **not** this public `vigil-skills` repo. See § Decision D3.

---

## Goal

Close the silent-drift gap in `/wiki-after-merge`: when a post-merge run creates a `comprehension/` entry (or a decision enters via the promotion/supersession path), the matching `projects/<X>/<X>-hub.md` **Decisions** / **Comprehension** index table must be updated in the *same atomic commit* — newest-first row, correct `../../` link depth, `> Last updated:` bumped — and a same-SHA re-run must propose zero further changes. Secondarily, harden `wiki-lint.mjs` so (a) a single-dot `](../decisions/` / `](../comprehension/` link inside `projects/<X>/*.md` produces an *actionable wrong-depth* message instead of a bare dead-link, and (b) a comprehension/decision file missing **from any project hub** (not merely "indexed somewhere, incl. the global hub") is surfaced. The net result: the manual backfill performed in wiki commit `c53b33a` becomes reproducible by the patched skill + lint alone.

## Scope

**Files to change — all in the `vigil-harbor-wiki` repo:**

- `.claude/skills/wiki-after-merge/SKILL.md` (131 lines) — the primary change:
  - **Step 6** (`:50–56`): after the comprehension stub is written/filled, insert a newest-first row into the project hub's `## Comprehension` table.
  - **Step 7d** (`:92–96`): when the promotion/supersession path *adds* a new `decisions/<slug>.md` for the project, insert a newest-first row into the hub's `## Decisions` table.
  - **Step 8 staging list** (`:99`): add `projects/<project>/<project>-hub.md`.
  - **Idempotency contract** (`:103–112`): add a hub-index bullet.
  - **"What this skill does NOT do"** (`:114–122`) / **"Related"** (`:123–131`): keep consistent.
- `SCHEMA.md` (456 lines) — doc-of-record sync (D11): the skill *operationalizes* this routine (`SCHEMA.md:280–283`), so the routine must name the new surface:
  - **"After every merge" step 3** (`:299–312`, comprehension) and **step 4** (`:314–322`, decision promotion): each gains a one-clause hub-index mention.
  - **Maintenance Contract** summary line (`:385`): extend the routine chain to name the project-hub index rows.
  - The **lint-contract rows** (`:360–361`) are **not** changed — the new per-project signal stays `INDEX | info`, which `:361` already covers (D10).
- `wiki-lint.mjs` (783 lines) — the safety net:
  - `checkDeadLinks` (`:234–249`): emit a wrong-depth hint for dead single-dot decision/comprehension links from `projects/<X>/`.
  - `checkComprehensionCoverage` (`:443–454`) **and** `checkIndexCompleteness` decisions block (`:715–723`): add per-project-hub enforcement at severity `info`, retaining today's behavior for entries already indexed in any project hub.

**New files:** none.

**Files to leave alone:** the `wiki-state-update` skill, the pre-commit hook, Step 7c (Plane reconciliation), and **everything in the `vigil-skills` repo** (`/spec-cycle`, `/ship-spec`, `/spec-close`, `states.json`, `sync.py`). The hub *template* and table *schema* are not restructured — rows are added, columns are not.

## Decisions

The brief's carried-forward decisions plus the choices the brief deliberately left to this spec. Each names how the design honors it.

### D1 — Idempotency is non-negotiable

Every new write must survive a same-SHA re-run with zero duplicate rows and no double-bumped dates (`SKILL.md:103–112`).
**How honored:** the hub-row insert is guarded by a fixed-string grep for the entry's full path (`comprehension/<slug>.md` / `decisions/<slug>.md`) — the same grep-skip idiom Step 4 uses for `log.md` (`SKILL.md:38`). The full-path key is collision-safe: `pet-1` does not substring-match `comprehension/2026-…-pet-118-….md`. The `> Last updated:` write is `max(existing, merge-date)` (D11), so a re-run never changes it. A partial prior run is **self-healing**: the row-grep and the date-`max` are independent and each idempotent, so a re-run reconciles whichever half (row, or date) a crashed prior run left missing — neither can double-apply.

### D2 — Single atomic commit

New hub mutations join Step 8's existing commit (`SKILL.md:98`); no second commit, no pre-confirmation write. The skill commits only if all sub-steps succeed.
**How honored:** the hub row and `Last updated` edit are *proposed* during Step 6/7d via `Edit` (like the other sub-steps) but staged and committed only at Step 8, alongside `log.md`/`filemap.md`/`state.md`/comprehension entry. If any sub-step fails — including a failed hub insert (D11) — nothing commits.

### D3 — Public-repo boundary (implementation repo = `vigil-harbor-wiki`)

`/wiki-after-merge` lives in the internal `vigil-harbor-wiki` repo. This ticket is *tracked* in VHS, but the change *ships* in the wiki repo. `vigil-skills` must stay free of any dependency on wiki-repo internals (CLAUDE.md "External dependencies"; VHS-12 precedent; memory `feedback_internal_wiki_repo`).
**How honored:** zero files under `vigil-skills/` are touched (the spec artifact itself is the only thing that lands here). The lint's per-project mapping is derived from the wiki's *own* hub headers (D7), **not** from `vigil-skills/skills/ship-spec/states.json` — so no cross-repo coupling is introduced.
**Consequence for `/ship-spec`:** ship-spec cuts its worktree from the *invoking* repo's default branch and runs the spec's Test command there. For this ticket that repo must be `vigil-harbor-wiki`. Per the internal-wiki convention (wiki-skill changes merge without the public PR/CodeRabbit flow), the realistic path is to implement directly in the wiki repo (or run ship-spec *from* the wiki repo). This spec does **not** redesign ship-spec; it flags the boundary so the operator routes implementation to the correct repo. Phase 3's drift-check surfaces this explicitly.

### D4 — Build on the lint, don't fork it

DEAD_LINK and INDEX already exist; extend them. A parallel checker would be the duplicate-code finding the conventions reviewer exists to catch.
**How honored:** the wrong-depth hint is a *message refinement inside* `checkDeadLinks` — it reuses the existing `resolve(fileDir, link)` + `existsSync` resolution (`:243–244`) and only branches the `check(...)` message when the dead link matches the wrong-depth shape; severity stays `error`. The per-project enforcement *extends* `checkComprehensionCoverage` / `checkIndexCompleteness` rather than adding a new top-level check function or a second resolver.

### D5 — Hubs are discovered dynamically

`wiki-lint.mjs:78` (`hubIndexFiles`) derives hub files via the `projects/<x>/<x>-hub.md` pattern; the skill's hub lookup resolves the same way, never hard-coding per-project paths.
**How honored:** the skill resolves the hub as `projects/<project>/<project>-hub.md` from the project it already computes in Step 5 (e.g. `Petasos → petasos → projects/petasos/petasos-hub.md`). **Hubs exist for only a minority of projects today** (dynasty, petasos, prime-radiant — 3 of ~14 project dirs), so for most merges the Part A "no hub → skipped" branch is the *expected, common* path, not an error. The lint reuses `hubIndexFiles(files)` (`:78–79`) for its hub set in both INDEX checks and the new per-project map (D7).

### D6 — Guard placement: skill-time *and* lint-time (both)

The brief allows the gap to be closed "skill-time, lint-time, or both." This spec does **both**, by role:
- **Skill-time (prevention):** Step 6/7d insert the row, so a correctly-run skill never produces the drift.
- **Lint-time (detection):** the per-project INDEX `info` catches drift from a *skipped* skill run, a manual edit, or a pre-patch historical entry — the cases the skill cannot retroactively cover.

### D7 — Per-project attribution, and the non-regression model (the round-1 P1 fix)

To enforce per-project indexing the lint must attribute a flat `comprehension/2026-06-14-pet-118-….md` file to a project. The map is built dynamically: for each hub, parse `> Plane project: <PREFIX>` (e.g. `petasos-hub.md:4` → `PET`), keying `PREFIX.toLowerCase() → <dir>`; a file's prefix is the first ticket token in its slug (`/\d{4}-\d{2}-\d{2}-([a-z]+)-\d/` → `pet`).
**Rationale for the source:** a hardcoded prefix→dir table is the duplicate-data smell D4 forbids; reading `vigil-skills/.../states.json` violates D3. The hub self-declares its prefix, so the wiki is internally self-describing.
**The non-regression rule (round-1 correctness-F1 / conventions-F1):** an entry is flagged **only when it appears in *no* project hub at all** (i.e. indexed only in the global `vigil-harbor-hub.md`, or nowhere). An entry present in **any** `projects/*/*-hub.md` is silent — even if that hub is not its prefix-derived hub. This is load-bearing: Dynasty work is deliberately filed under the **prime-radiant** hub (Dynasty→Prime-Radiant lineage — e.g. `prime-radiant-hub.md` lists `2026-05-06-dyn-34a-…`). A naive "must be in its *prefix* hub" rule would fire ~11 false positives on the live wiki and break "runs clean." The "present in any project hub → silent" escape keeps cross-lineage filing legal while still catching the real gap (an entry — like the pre-backfill PET-111 row — present in *no* project hub).
**Best-effort limit (edge-F6 / conventions-F4):** the extractor matches only `<prefix>-<digit>`-shaped slugs. Topical or dual-prefix slugs (`2026-05-01-wiki-…`, `2026-06-02-dyn-inference-pool` with no ticket number) and any prefix with no hub fall through to the **existing** "indexed anywhere" `info` check, unchanged. This is a documented best-effort net, not a regression — and the match rule is intentionally narrow so a future reader does not broaden it back into the prefix-hub false-positive trap.

### D8 — Cross-check surfaces sibling drift but does not auto-backfill

The brief's direction-1 cross-check and the out-of-scope fence ("Backfilling other project hubs … operational cleanup") are reconciled: the skill inserts **only the current run's** entry, and emits an *advisory note* listing any other same-project files (slug contains the project's `<prefix>-<digit>` token — the **same** attribution rule as D7's `owningDir`) that are absent **from any hub**. Scoping the advisory to "absent from any hub" (not "absent from the prefix hub") prevents the cross-lineage noise D7 describes. It never auto-inserts; bulk backfill remains the post-ship operational sweep.

### D9 — Decision-row maintenance is conditional, comprehension-row is per-run

The skill scaffolds comprehension on every threshold-crossing run, so the comprehension-row insert is unconditional (when a comprehension entry is created). It does **not** author decisions; a decision row is inserted **only if** this run produced a new `decisions/<slug>.md` via Step 7d's promotion/supersession path. Supersession *marking* stays in the decision entry file (existing Step 7d behavior) and does not restructure the hub table — "adding rows," not schema changes.

### D10 — New per-project signal is severity `info`, matching the SCHEMA lint contract

The new per-project-hub finding is `INDEX | info`, not `warn`.
**Rationale (round-1 conventions-F2):** `SCHEMA.md:360–361` is the authoritative lint contract — it assigns `INDEX | warn` to "a `projects/` directory not referenced in `vigil-harbor-hub.md`" and `INDEX | info` to "a decision/comprehension file not listed." `COWORK-LINT-CRON.md` files "missing index entry" under `info`; the 2026-05-01 redesign classifies "missing index rows" as a **Tier-1 mechanical/autofix** item (the `info` lane). Using `info` therefore *refines the surface set the existing `:361` row checks* (from "any surface" to "any project hub") **without** changing severity — so no contract-row edit is needed and the cron's triage stays correct. Actionability comes from the message naming the specific expected hub, not from the severity. Exit code is unaffected either way (`warn`/`info` both exit 0 — `:783`), so nothing about the CI gate turns on this choice.

### D11 — Hub edits are deterministic, observable, and self-stopping

The insert mechanics (round-1 edge-F1/F2/F3/F4/F9, correctness-F5) are pinned so the skill cannot silently mis-edit or silently fail:
- **Unique anchor:** every hub has three byte-identical-looking table separators (Pages, Decisions, Comprehension). The `Edit` `old_string` **must include the `## Comprehension` / `## Decisions` section header** (or a unique anchor strictly beneath it), never a bare `|---|` separator — otherwise the edit could hit the wrong table or error on a non-unique match.
- **Date-descending placement:** insert below the first existing data row whose date is `≤` the new entry's date (current-date → top; backdated → correct slot), preserving the table's newest-first invariant even on a re-run over an older SHA.
- **`max()` date bump:** `> Last updated:` is set to `max(existing, merge-date)` so an older re-run never lowers it.
- **Table-shape guard:** if the target `## Section` header or its separator is absent (degenerate/empty/hand-broken hub), skip with a status line — never invent the table.
- **One status line per entry:** the skill emits exactly one `hub-index:` outcome per comprehension/decision entry — `inserted <slug> → <hub>` / `row present — skipped` / `no hub — skipped` / `table missing — skipped` / `insert failed: <reason>`. The whole ticket exists because the gap was *silent*; the happy path must leave a breadcrumb too.
- **Fail-stops-commit:** `insert failed` is a hard stop — Step 8 does not commit (consistent with "commits only if all sub-steps succeed").
- **Sequential inserts:** when one run produces multiple entries for the same hub (two comprehension entries, or a comprehension + a promoted decision), inserts are applied sequentially against the updated working-tree file, each re-running the grep-skip and re-evaluating the anchor.

## Design

### Part A — Skill: comprehension hub-row insert (Step 6)

Append to Step 6 of `SKILL.md`, after "the agent writes the body". Resolve the hub as `projects/<project>/<project>-hub.md` (project from Step 5; hubs are a minority — D5). Then, in order:

1. **Hub present?** If the file does not exist → `hub-index: no hub at <path> — skipped`; stop (never create a hub).
2. **Table present?** Confirm the `## Comprehension` header **and** its `|---|` separator exist. If not → `hub-index: comprehension table missing in <hub> — skipped (manual fix)`; stop (never invent the table — § Scope).
3. **Already indexed?** `grep -F "comprehension/<slug>.md" <hub>` — if present → `hub-index: row present — skipped`; stop (idempotent; full-path key is collision-safe — D1).
4. **Build the row:** `| <YYYY-MM-DD> | [<Title>](../../comprehension/<slug>.md) | merge |` — date/slug from the entry, `<Title>` from the entry's H1, trigger **always `merge`** (the skill is merge-triggered; `review`/other triggers are out-of-band and not the skill's job — round-1 correctness-F4). `../../` is mandatory (hub is depth 2). The row date **is** the entry's slug `YYYY-MM-DD`; this same value is the `Last updated` candidate in step 6 — the skill has no separate "merge-date".
5. **Insert, date-descending (D11):** place the row immediately below the first data row whose date is `≤` the new entry's date, comparing dates as zero-padded `YYYY-MM-DD` **strings** (lexical order = chronological — no `Date` parsing, no `Math.max`). Skip any existing row whose first cell is not `YYYY-MM-DD`-shaped while scanning for the slot; if no well-formed data row exists, insert directly below the separator. The `Edit` `old_string` **must include the `## Comprehension` header** so it cannot match the Decisions/Pages separators.
6. **Bump `> Last updated:`** to the later of the existing value and the entry's slug date, compared as `YYYY-MM-DD` strings (D11) — never lower it; a same-date re-run is a no-op. If the existing `> Last updated:` line is missing or not `YYYY-MM-DD`-shaped, treat existing as empty (the new date wins) and emit `hub-index: Last updated malformed — set to <date>`.
7. **Completeness advisory (D8):** list any other entries whose slug contains this project's `<prefix>-<digit>` token that are absent from **any** hub → `hub-index: N sibling entries un-indexed (backfill candidates: …)`. Do not auto-insert.
8. **Status line (D11):** emit exactly one `hub-index:` outcome (`inserted` / `row present — skipped` / `no hub — skipped` / `table missing — skipped` / `insert failed: <reason>`). `insert failed` is a hard stop for Step 8.
9. The edit lands in the working tree via `Edit`; staged in Step 8, not committed here.

### Part B — Skill: decision hub-row insert (Step 7d)

Extend Step 7d's supersession bullet so that **if** this run added a new `decisions/<slug>.md` for the project (promotion path), insert a newest-first row into the hub's `## Decisions` table using the **same mechanics as Part A (1–9)**, keyed on `decisions/<slug>.md`. Supersession of an existing decision continues to be recorded in the decision *entry file* (`superseded` marker + replacement link); the hub table is row-add-only.

### Part C — Skill: Step 8 staging, idempotency contract, cross-refs

- **Step 8 staging list** (`:99`) — add `projects/<project>/<project>-hub.md` to the `git add` set, "(if a hub row was inserted)".
- **Idempotency contract** (`:103–112`) — add: `Step 6 / 7d (hub index): the fixed-string grep on the entry path prevents duplicate rows; the Last updated bump is max(existing, merge-date). A second run on the same SHA inserts zero rows and changes zero dates; a partial prior run is self-healing (the row-grep and date-max are independent and each idempotent).`
- **"What this skill does NOT do"** — add: hub maintenance is row-add-only; it never restructures the table schema or invents a missing hub/table.
- **"Related"** — note the hub file as a Step 8 commit target; no new external dependency.

### Part D — Lint: actionable wrong-depth message (`checkDeadLinks`)

Inside the `if (!existsSync(targetPath))` block (`:244`), branch the message before the generic `check`:

```js
const isProjectDoc = /^projects\/[^/]+\//.test(file);
const wrongDepth = /^\.\.\/(decisions|comprehension)\//.test(link); // single-dot
if (isProjectDoc && wrongDepth) {
  const ups = file.split('/').length - 1; // projects/<X>/foo.md → 2
  check('DEAD_LINK', 'error',
    `${file} → ${link} (wrong relative depth from ${file.replace(/[^/]+$/, '')}; ` +
    `use ${'../'.repeat(ups)}${link.replace(/^\.\.\//, '')} — entries live at wiki root)`);
} else {
  check('DEAD_LINK', 'error', `${file} → ${link} (target not found)`);
}
```

Severity stays `error` (the link genuinely doesn't resolve; exit-code behavior unchanged — `:783`). The `isProjectDoc` guard correctly excludes the abundant *valid* `](../decisions/…)` links that originate from `comprehension/` (a depth-1 dir, where `../decisions/` is correct *and* resolves) — verified, no false-positive risk. Links that resolve are untouched.

### Part E — Lint: per-project-hub INDEX enforcement (`info`)

Add helpers (note the `try/catch` — a transiently-missing/locked hub must not crash the whole lint; round-1 edge-F8):

```js
// prefix (lowercase) → project dir, from each hub's "> Plane project: <PREFIX>"
const hubPrefixMap = (files) => {
  const m = {};
  for (const hub of hubIndexFiles(files)) {
    const dir = hub.split('/')[1];
    let txt;
    try { txt = readFileSync(join(wikiRoot, hub), 'utf-8'); } catch { continue; }
    const pm = txt.match(/Plane project:\s*([A-Za-z]+)/);
    if (pm) m[pm[1].toLowerCase()] = dir;
  }
  return m;
};
// project dir that owns a comprehension/decisions file, or null (best-effort — D7)
const owningDir = (file, prefixMap) => {
  const pm = file.match(/\/\d{4}-\d{2}-\d{2}-([a-z]+)-\d/);
  return pm ? (prefixMap[pm[1]] ?? null) : null;
};
```

In `checkComprehensionCoverage` (`:449–453`) and `checkIndexCompleteness` decisions (`:721–724`), replace the single "indexed anywhere" loop with (comprehension shown; decisions identical with its own array):

```js
const prefixMap = hubPrefixMap(files);
const projectHubTexts = hubIndexFiles(files).map(h => {
  try { return readFileSync(join(wikiRoot, h), 'utf-8'); } catch { return ''; }
});
for (const c of comprehensions) {
  const dir = owningDir(c, prefixMap);
  const inAnyProjectHub = projectHubTexts.some(t => t.includes(c));
  if (dir && !inAnyProjectHub) {
    // attributable to an existing hub but present in NO project hub → the real gap
    check('INDEX', 'info', `${c} not listed in any project hub (expected projects/${dir}/${dir}-hub.md)`);
  } else if (!dir && !indexSurfaces.some(t => t.includes(c))) {
    // unattributable + in no surface at all → existing behavior, unchanged
    check('INDEX', 'info', `${c} not listed in vigil-harbor-hub.md or any project hub comprehension table`);
  }
}
```

**No regression (D7):** an attributable entry already in *any* project hub (incl. cross-lineage DYN-in-prime-radiant) → silent, exactly as today. An attributable entry in **no** project hub (only global, or nowhere) → `info` (the targeted gap; previously the "nowhere" sub-case was already `info`, the "global-only" sub-case newly surfaces — at the same `info` severity, so exit code is unchanged). An unattributable entry → unchanged `info`. Because the new signal is `info` (`:783`), "lint runs clean" (exit 0) is preserved unconditionally.

This "any project hub → silent" escape is **deliberate** (edge-F3): an entry filed in a *sibling/non-prefix* project hub — legitimate cross-lineage filing, which the wiki maintains no registry to distinguish from a genuine misfile — stays silent. The lint catches only the entry present in **no** project hub (the c53b33a-class gap); the skill-time advisory (Part A step 7) is the backstop for a misfile-into-the-wrong-hub. See Done-when AC-3.

### Part F — SCHEMA.md doc-of-record sync (D11 / conventions-F3)

The skill operationalizes SCHEMA's "After every merge" routine (`SCHEMA.md:280–283`), so the routine must name the surface the skill now maintains — otherwise this change re-creates the doc/skill drift the brief is fixing, inverted.

- **Step 3** (`:299–312`, comprehension): append a clause — "…and, if the project has a `projects/<X>/<X>-hub.md`, add a newest-first row to its **Comprehension** table (`../../` links)."
- **Step 4** (`:314–322`, decision promotion): append the equivalent for the hub's **Decisions** table.
- **Maintenance Contract** (`:385`): extend the chain to "…comprehension → decisions (+ project-hub index rows) → supersession scan → learnings."
- The lint-contract rows (`:360–361`) are **left unchanged** (D10).

## Test plan

Hybrid change: the **lint** is code (deterministically checkable); the **skill** is agent-executed prose (review-checklist + reproduction). The wiki repo has **no test harness and no `package.json`** — wiki-lint has no self-tests — so the lint is exercised by running it against the live wiki plus throwaway fixtures.

**1. Lint — baseline + non-regression (the round-1 P1 gate):**
- `node wiki-lint.mjs .` from the wiki root → **exit 0** (only `error` sets exit 1; this change adds no `error`).
- Diff the finding set against the pre-patch baseline (`0 errors, 48 flags, 0 warnings, 0 info` on 2026-06-14). Walk **dynasty and prime-radiant explicitly**: confirm the Dynasty→Prime-Radiant lineage entries (e.g. `comprehension/2026-05-06-dyn-34a-…`, indexed in `prime-radiant-hub.md`) stay **silent** under Part E's "present in any project hub → silent" rule — they must NOT newly appear. Any new `info` that does appear is a genuine "in no project hub" gap (the feature working, advisory only); it never changes exit status.

**2. Lint — wrong-depth hint (Part D):**
- Add `[x](../decisions/nope.md)` to a scratch `projects/petasos/_fixture.md`; run lint → expect a `DEAD_LINK` `error` whose message names the correct `../../` depth (not the bare "target not found"). Delete; re-run → clean.

**3. Lint — per-project-hub `info` (Part E):**
- Create scratch `comprehension/2026-06-14-pet-999-fixture.md` referenced in `vigil-harbor-hub.md` **only** (not the petasos hub) → expect `INDEX info` "not listed in any project hub (expected projects/petasos/petasos-hub.md)". Add the row to `petasos-hub.md` → re-run → clears.
- Negative A (cross-lineage): a scratch entry referenced **only** in a *non-prefix* project hub → must stay silent (proves the no-regression escape).
- Negative B (unknown/topical prefix): a fixture `…-zzz-1` and a `…-pet-topical` (no digit) → fall to the existing `info`, never a new per-project line.

**4. Skill — reproduction of `c53b33a` (review):**
- On a wiki checkout *before* `c53b33a` (e.g. at `dd4b9c2`), dry-run the patched Step 6 logic for the PET-111 comprehension entry → confirm it would insert the PET-111 `## Comprehension` row (anchored on the section header, D11) with a `../../` link and `max()`-bump `Last updated`, matching the manual backfill.
- **Idempotency:** run the same logic against the *current* (already-fixed) petasos hub → zero row inserts, zero date changes (Done-when 1 / D1).
- **Multi-entry:** simulate a run producing two same-project entries → confirm sequential inserts produce two correctly-ordered rows (D11).
- **Date semantics:** confirm `Last updated` is compared/stored as `YYYY-MM-DD` strings — a re-run over an *older* SHA must not lower the hub's `Last updated`, and a missing/malformed existing `Last updated` is overwritten with a status line (edge-F1).

**5. Skill — prose review checklist:**
- Step 8 staging names the hub file; idempotency bullet added (incl. partial-run self-heal); Step 6/7d sub-steps unambiguous; `../../` stated mandatory; status-line + fail-stops-commit present; no second commit / no pre-confirmation write (D2); table-shape guard present; "does NOT"/"Related" consistent; SCHEMA steps 3/4 + Maintenance Contract updated (Part F).

## Test command

Run from the `vigil-harbor-wiki` repo root (located per `vigil-skills/CLAUDE.md` § Key paths):

```bash
node wiki-lint.mjs .
```

Exit 0 = clean (only `error`-severity findings set exit 1 — `wiki-lint.mjs:783`). This is the automated gate for the **lint** change (Parts D, E) and the non-regression check (Test plan 1). The fixture procedures (Test plan 2–3) and the skill review/reproduction (Test plan 4–5) are manual — they have no runner. Because the implementation repo is the wiki (D3), `/ship-spec` must execute this command in the wiki worktree, not in `vigil-skills`.

## Done when

1. **(Brief AC-1 — skill hub maintenance + idempotency)** A `/wiki-after-merge` run that creates a comprehension entry (or promotes/supersedes a decision) leaves the matching project-hub index table current — correct `../../` links, newest-first row, `Last updated` bumped — in the **same atomic commit**, and a same-SHA re-run proposes zero further changes. → Parts A, B; D1, D2, D11.
2. **(Brief AC-2 — link-depth guard)** Single-dot `](../decisions/` / `](../comprehension/` links inside `projects/<X>/*.md` are caught with a correct-depth hint, and every hub/project-doc decision and comprehension link resolves to an existing file. → Part D + Parts A/B writing `../../` by construction; existing DEAD_LINK `error` enforces resolution.
3. **(Brief AC-3 — per-project-hub indexing gap)** A comprehension/decision file missing from **any** project hub is surfaced (both the skill-time advisory and the lint-time `info`), **without regressing** the live wiki (cross-lineage entries indexed in a sibling project hub stay silent — D7). → Parts A(7), E; D6, D7, D10. (The "any project hub" reading is the accepted scope — an entry in a sibling/non-prefix hub stays silent by design, with the skill advisory as the misfiling backstop; confirm at drift-check — edge-F3.)
4. **(Brief AC-4 — skill + doc self-consistency)** The idempotency-contract section and the Step 8 staging list name the hub file; "does NOT"/"Related" stay consistent; and SCHEMA's "After every merge" routine + Maintenance Contract name the hub-index surface. → Parts C, F.
5. **(Brief AC-5 — reproduces the manual backfill, runs clean)** `node wiki-lint.mjs .` **exits 0** on the live wiki (this change adds no `error`-severity findings, and Part E's per-project signal is `info`, which never changes exit status), and the manual backfill `c53b33a` performed is reproducible by the patched skill + lint alone. → Test plan 1, 4.

## Out of scope

- Backfilling other project hubs (`mcp-server`, `calvin`, `dynasty`, etc.) that may carry the same drift — operational cleanup; run the patched skill/lint over them once it ships (D8).
- Any change to Step 7c (Plane sibling reconciliation) or the evidence-triple / `/wiki-state-update` machinery.
- Restructuring the hub page template or the Decisions/Comprehension table schema beyond adding rows (D9, D11).
- Creating decision entries from scratch inside `/wiki-after-merge` — the skill scaffolds comprehension, not decisions; the hub decision-row insert fires only when a decision already enters via the promotion/supersession path (D9).
- Implementing a `wiki-lint.mjs --autofix tier1` fixer. `--autofix` is referenced in `COWORK-LINT-CRON.md` but is **not** implemented in the lint's arg parser (`:88–113`). The new per-project signal is `info` (D10), aligning with the SCHEMA contract (`:361`) and the autofix-eligible "missing index entries" tier (decision `2026-05-01-wiki-maintenance-redesign`) — a severity-classification choice, not a commitment to build the fixer.
- Changing the lint-contract rows in `SCHEMA.md` (`:360–361`) — the new signal reuses the existing `INDEX | info` row (D10); only the routine steps + Maintenance Contract are touched (Part F).
- Any change to the public `vigil-skills` spec-lifecycle skills (`/spec-cycle`, `/ship-spec`, `/spec-close`) or `states.json` (D3).

## Post-green polish

Spec went green at round 2 (all three lenses P0=P1=0). The bounded post-green polish folded the two round-2 P2s tagged `Pre-ship recommended`, both as clarifications:
- **edge-cases/F-1** — Part A steps 4–6 + Test plan 4 now pin the date semantics: the row date and `Last updated` are the **same** `YYYY-MM-DD` slug date (no undefined "merge-date"), compared/stored as zero-padded `YYYY-MM-DD` strings (lexical = chronological), with a missing/malformed existing `Last updated` overwritten + status line.
- **edge-cases/F-3** — Part E "No regression" + Done-when AC-3 now state explicitly that the "any project hub → silent" escape is deliberate (cross-lineage filing is legal and indistinguishable from a misfile without a registry the wiki lacks); the skill advisory is the misfiling backstop. Flagged for drift-check confirmation.

## Deferred (P2+)

The round-2 advisory findings below are acknowledged and intentionally not folded (they are robustness/precision notes, not blockers; carry into `/ship-spec`):
- **edge-cases/F-2 (P3)** — date-descending scan vs a malformed first-row date: mitigated by Part A step 5's "skip non-`YYYY-MM-DD` rows" clause; deeper validation deferred.
- **edge-cases/F-4 (P3)** — `insert failed` hard-stop leaves Step 7c Plane writes committed + prior sequential inserts in the working tree; recoverable via grep-skip self-heal + `git checkout`. Documentation-only; deferred.
- **edge-cases/F-5 (P4)** — `projectHubTexts` double-reads each hub; sub-ms window, `info`-only impact. Optional hoist; deferred.
- **correctness/F-1 (P3)** — D7 prose vs the two Part E code branches; code governs and is unambiguous. Wording-only; deferred.

All round-1 P1/P2 findings were folded in-place during the round-2 revision (see § Decisions D5, D7, D8, D10, D11 and § Design Parts A, B, E, F); the round-1 P3 precision findings were also addressed rather than deferred.
