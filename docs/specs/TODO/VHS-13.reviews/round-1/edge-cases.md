# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Row-insert anchor is ambiguous — `Edit` into "the `|---|` separator" can hit the wrong table or fail
**Severity:** P1
**Where:** Part A step 3; Part B
Every hub has 3 tables (Pages, Decisions, Comprehension) → 3 header/separator rows; Decisions & Comprehension separators are byte-identical (`|------|-------|---------|`). "Insert immediately after the `|---|` separator" via `Edit` (needs unique `old_string`) either edits the wrong table or errors on non-unique match → sub-step silently fails → Step 8 doesn't commit → reintroduces the exact silent-drift class this ticket kills, but now it looks like the skill ran.
**Fix:** anchor on the section H2 + its header+separator tuple; require the `Edit` old_string to include the section header for uniqueness.

### F-2: Backdated entry violates "insert after separator (top)" → out-of-order table or lowered `Last updated`
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** Part A steps 3–4
Slug date older than top row (re-run over older SHA, or review-trigger filled days after a newer merge entry). Top-insert breaks newest-first (Done-when 1 promises "newest-first row"); unconditional set-to-merge-date can LOWER `Last updated` and flip-flop non-idempotently across alternating SHAs.
**Fix:** insert at first row whose date ≤ new entry's date; `Last updated = max(existing, merge-date)`.

### F-3: Skill emits no per-outcome hub-index status → skipped/failed insert stays silent
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** Part A/B; Done-when 1
Report strings exist for no-hub and row-present, plus sibling advisory — but no SUCCESS line and no Edit-FAILURE line. Success = silence; failure = silence indistinguishable from "no entry this run." The brief's whole premise is that the gap drifted silently.
**Fix:** emit exactly one `hub-index:` line per entry — `inserted <slug> → <hub>` / `row present — skipped` / `no hub — skipped` / `insert failed: <reason>`; make `insert failed` a hard stop for Step 8.

### F-4: Malformed / empty / header-absent hub table unhandled
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** Part A step 3
File exists (passes the `:86` guard) but `## Comprehension` header absent, or present without separator. "Insert after separator" has no anchor → fails silently or corrupts placement. Empty-table (separator + zero rows) works; header/separator-absent does not.
**Fix:** verify section header + separator present before inserting; else `hub-index: table missing — skipped (manual fix needed)`, don't invent the table.

### F-5: Partial prior run (bump without row, or row without bump) not covered by idempotency contract
**Severity:** P2
**Where:** D1; Part C idempotency bullet
Two separate Edits (row + Last-updated) unstaged until Step 8. Interruption between them leaves a half state. Both orderings actually self-heal (grep-skip + set-to-date are independent and idempotent) — but the contract only asserts the clean same-SHA case.
**Fix:** add a line documenting the cross-edit partial-run self-heal.

### F-6: Attributable entries with non-`<prefix>-<digit>` slugs silently fall to `info`
**Severity:** P3
**Where:** Part E `owningDir`; D7
`comprehension/2026-06-02-dyn-inference-pool.md` is a real dynasty entry; token after date is `dyn-inference` (no digit) → regex null → falls to `info` even though dynasty has a hub. Degrades to today's behavior (no regression) but per-project guarantee is best-effort.
**Fix:** document the best-effort limit in D7, or broaden regex to `<prefix>-<word>` for known hub prefixes.

### F-7: Sibling-drift advisory glob `comprehension/<prefix>-*` mismatches real `YYYY-MM-DD-<prefix>-*` naming
**Severity:** P3
**Where:** Part A step 5; D8
Real files are date-first; a prefix-anchored glob matches ZERO files → the advisory is a silent no-op.
**Fix:** substring match `comprehension/*-<prefix>-[0-9]*` mirroring `owningDir`.

### F-8: `hubPrefixMap` `readFileSync` with no try/catch — a transiently-missing/locked hub aborts the whole lint
**Severity:** P3
**Where:** Part E `hubPrefixMap`
A hub deleted/locked between the file walk and the read throws → entire `node wiki-lint.mjs .` aborts (the automated gate). Pre-existing pattern at `:447`/`:718`, but the spec adds a THIRD unguarded read over the same set.
**Fix:** wrap per-hub read in try/catch, skip on failure.

### F-9: Concurrency — two entries in one merge run target the same hub; second insert must see the first
**Severity:** P3
**Where:** Part A; D9
One merge can cross threshold for >1 comprehension entry, or a comprehension + promoted decision for the same project (Step 6 + Step 7d, same hub). Both top-anchored inserts collide if not applied sequentially to the updated tree.
**Fix:** state inserts are applied sequentially to the live working-tree file (grep-skip + anchor re-evaluated each time).

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 4 | P4: 0

STATUS: RED P0=0 P1=1 P2=4 P3=4 P4=0
