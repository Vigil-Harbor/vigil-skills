# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Test Plan step 1 and Done-when 5 ("lint runs clean") are factually false against the live wiki — Part E surfaces 10 pre-existing dynasty-hub drift entries as new `warn`s
**Severity:** P1
**Where:** spec § Test plan step 1; § Done when item 5; § Part E "No regression"
Implemented Part E's exact logic (`hubPrefixMap` + `owningDir` + per-project loop) against the live wiki on 2026-06-14 → **10 new `INDEX warn`** findings, for **dynasty** (not petasos): 6 comprehension (`2026-05-06-dyn-34a-...`, `...dyn-93-...`, `...dyn-96-...`) + 4 decisions (`2026-05-06-dyn-34-...`, `...dyn-95-...`). These pass today because the current `info` check matches the full path in ANY surface, and these dyn paths appear in `prime-radiant-hub.md` and `log-archive.md`. Part E narrows to the OWNING hub → flips them to warn. Baseline today: `0 errors, 48 flags, 0 warnings, 0 info` (exit 0); Part E takes warnings 0 → 10. Spec then puts the dynasty backfill out of scope → the acceptance gate (Done-when 5) is unsatisfiable on first run.
**Fix:** reconcile — (a) redefine "runs clean" = exit 0 (`warn` ≠ exit 1, `:783`) and state Part E is EXPECTED to surface dynasty backfill candidates; or (b) fold dynasty backfill into scope. Rewrite Test plan/Done-when text — they currently promise zero new `warn`, which is false.

### F-2: D7's prefix→dir attribution conflicts with deliberate cross-project hub filing (prime-radiant lists DYN entries) — Part E will `warn` against author intent
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** D7; Part E loop
`prime-radiant-hub.md:55` deliberately lists `2026-05-06-dyn-34a-score-calibration-skeleton.md` (Dynasty→prime-radiant lineage). Part E keys off `dyn` prefix → `dynasty-hub.md`, finds it absent, warns — even though the entry IS in a project hub. Dominant source of F-1's 10 findings.
**Fix:** (a) warn only when in NO project hub; or (b) document cross-lineage filing as accepted advisory.

### F-3: D5 hub-resolution example `calvin-hub.md` does not exist — only 3 hubs exist
**Severity:** P3
**Where:** D5; Part A
Only dynasty, petasos, prime-radiant have hubs (3 of 14 dirs). `projects/calvin/calvin-hub.md` does not exist → the cited example resolves nowhere. Part A's "no hub → skipped" handles it (11 of 14 hit skip), but D5 implies hub presence is the norm.
**Fix:** change example to petasos; note hubs exist for a minority, so "no hub → skipped" is the common path.

### F-4: Step 6 `<trigger>` derivation underspecified vs real table data
**Severity:** P3
**Where:** Part A step 1
`petasos-hub.md` uses `merge` for almost every row but `review` for PET-106 (`:57`). Skill fires only on threshold-crossing merge; no signal for review vs merge. Honest answer: always `merge`.
**Fix:** state skill always writes `merge`; drop "or review/etc. as applicable."

### F-5: Same-date insert-position determinism unstated
**Severity:** P3
**Where:** Part A steps 2–3; Done-when 1
petasos hub has multiple `2026-06-14` rows. grep-skip mechanics are sound; the unstated invariant is deterministic insert position for same-date entries.
**Fix:** one sentence — idempotency rests on the fixed-string slug grep; same-date insert is "immediately below the separator," reached only when grep confirms absence.

## Summary
P0: 0 | P1: 1 | P2: 1 | P3: 3 | P4: 0
Verified accurate: all anchors, exit-code (`:783`), Part D depth math, `owningDir`/`hubPrefixMap` regexes, `Plane project:` headers (PET/DYN/RAD present), slug regex (141/151 match), SHAs c53b33a/dd4b9c2/5989f35, no-package.json, `--autofix` non-implementation. Blocker is F-1: "runs clean" gate contradicts the out-of-scope fence.

STATUS: RED P0=0 P1=1 P2=1 P3=3 P4=0
