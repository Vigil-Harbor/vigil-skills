# Conventions Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Part E's per-project-hub `warn` produces ≥11 regressions on the live wiki — "no regression" / AC-5 ("runs clean") provably false
**Severity:** P1
**Where:** Part E; Test plan 1; Done-when 5; D7
`owningDir` keys `dyn → projects/dynasty/dynasty-hub.md` (from `dynasty-hub.md:4 > Plane project: DYN`). But DYN-prefixed entries are indexed in `prime-radiant-hub.md` (Dynasty→Prime-Radiant lineage), not a dynasty hub. e.g. `comprehension/2026-05-06-dyn-34a-...md` is only in `prime-radiant-hub.md`; today it's silent (existing "indexed anywhere" info satisfied). Part E newly fires `INDEX warn` "missing from its own project hub projects/dynasty/dynasty-hub.md". Simulation: **≥11** entries (7 comprehension + 4 decisions). `node wiki-lint.mjs .` is exit 0 / 0 INDEX today. Root error: Part E assumes one prefix → one owning hub; the real wiki files DYN work under the RAD hub. Test plan 1 only checks petasos, so the false "clean" survives the spec's own test design.
**Fix:** (a) warn only when indexed in NO hub AND prefix has a matching hub (keep "present in any hub" escape so DYN-in-RAD stays silent); or (b) drop the per-project warn for comprehension/decision, rely on the skill-time advisory. Either way, expand Test plan 1 to assert full-wiki zero-new-`warn` and walk dynasty/prime-radiant.

### F-2: Part E severity `warn` contradicts the SCHEMA.md lint contract (authoritative) and the COWORK severity legend
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** Part E; D7; Out-of-scope autofix defense; contradicts Scope "leave alone SCHEMA.md"
`SCHEMA.md:360-361` (the lint contract, per CLAUDE.md) defines `INDEX | warn` = "projects/ dir not referenced in vigil-harbor-hub.md" and `INDEX | info` = "decision/comprehension file not listed in vigil-harbor-hub.md". `COWORK-LINT-CRON.md:108` files "missing index entry" under `info`; reserves `warn` for orphan/supersession/claim-anchor. The spec's defense ("warn aligns with the autofix-eligible tier, 2026-05-01") conflates autofix tier with severity: that redesign lists "missing index rows" as a **Tier-1 autofix** (the info/mechanical lane), so the cited precedent argues for `info`, not `warn`. Promoting to `warn` adds a third INDEX semantic the contract lacks, while SCHEMA is in "leave alone" → contract/code diverge.
**Fix:** keep the per-project finding at `info` (matches the existing row + the autofix tier); OR use `warn` and add the new semantic to `SCHEMA.md:361` + remove SCHEMA from "leave alone." Don't ship a severity the contract contradicts.

### F-3: Skill hub-maintenance extends behavior beyond SCHEMA's "After every merge" routine, but SCHEMA is left untouched
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** Parts A/B/C; Scope "leave alone SCHEMA.md"
`SCHEMA.md:280-283` — the skill "orchestrates this routine end-to-end"; `SCHEMA.md:385` Maintenance Contract enumerates Log → filemap/state → comprehension → decisions → supersession → learnings; the "After every merge" routine (`:274-338`) has NO hub-index step. `SKILL.md:3/:128` frames the skill as a faithful executor of SCHEMA. Adding hub maintenance makes the skill do more than the routine it documents — the same doc/skill drift class the brief fixes, inverted.
**Fix:** add a one-line hub-index step to SCHEMA's "After every merge" routine + the Maintenance-Contract summary; drop SCHEMA from "leave alone."

### F-4: `owningDir` prefix-token extraction fragile against the real slug corpus
**Severity:** P3
**Where:** Part E `owningDir`; D7
Live slugs include topical/non-ticket prefixes (`-wiki`, `-custom`, `-vigil`, `-model`, `-cot`, `-dpo`, …) and dual prefixes (`dyn` AND `dynasty`; `cal`→calvin). Regex requires a digit after the prefix → `2026-06-02-dyn-inference-pool.md` won't match. Fallback to `info` is correct (no crash) but per-project coverage is partial and inconsistent.
**Fix:** one-sentence D7 note that the extractor matches only `<prefix>-<digit>` slugs by design (so a future reader doesn't "fix" it into the F-1 regression).

### F-5: D8 cross-check advisory is a brief suggestion, not a commitment — confirm intent (noisy given lineage)
**Severity:** P3
**Where:** D8; Part A item 5
Brief lists the cross-check under "Proposed direction (do not pre-decide)". Spec elevates it to per-run skill behavior. Given the dyn/prime-radiant lineage, it would fire on most Dynasty merges listing many "missing" siblings that are actually indexed in the sibling hub — noisy.
**Fix:** scope the advisory to "absent from ANY hub" (so cross-lineage doesn't show as missing), or downgrade to one-time; confirm at drift-check.

## Notes on what checks out (no finding)
- **D3 (public-repo boundary):** honored — zero vigil-skills files touched; prefix map from hub headers, not states.json. Cleaner, not a reinvention.
- **D4 (build on the lint):** Part D is a true message-refinement in `checkDeadLinks` (reuses resolve+existsSync, stays `error`); Part E extends the two INDEX functions. No duplicate resolver/indexer. `??` + module-scope closures valid (Node, imports at `:19-20`).
- **D5 (dynamic hubs):** `hubPrefixMap` reuses `hubIndexFiles` (`:78`). No hard-coded paths.
- **Part D false-positive risk:** none — `isProjectDoc` guard excludes the abundant valid `](../decisions/…)` links from `comprehension/` (depth-1), which also resolve.
- **Anchors:** SKILL.md:98-99, lint:443-454 / :234-249 accurate.
- **D1/D2:** grep-`-F`-skip mirrors Step 4 (`SKILL.md:38/108`); set-to-date bump idempotent; staging joins Step 8, no second commit. Sound.

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=2 P4=0
