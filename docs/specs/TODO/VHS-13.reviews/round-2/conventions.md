# Conventions Review — round 2

## Closure of round 1 findings
All 19 round-1 findings verified **CLOSED**; no REOPENED, no PARTIAL.
- conventions/F-1 (P1) — CLOSED. D7 "present in any project hub → silent" + severity `warn`→`info` (D10). Live sim: 0 new findings, prefixMap `{dyn→dynasty, pet→petasos, rad→prime-radiant}`, baseline preserved.
- conventions/F-2 (P2) — CLOSED. Severity `info` everywhere (no stray `warn`); reuses existing `SCHEMA.md:361` row; lint-contract rows left unchanged.
- conventions/F-3 (P2) — CLOSED. SCHEMA.md added to scope; Part F edits steps 3/4 (`:299-322`) + Maintenance Contract (`:385`); anchors accurate, minimal in-line appends.
- conventions/F-4 (P3), F-5 (P3) — CLOSED (D7 best-effort note; D8 scoped to "any hub").

## Findings
No findings.

Verified no new convention violation:
- **Severity consistency** — every logic/code block uses `info`; the only `warn` mentions reference the existing contract row.
- **D10 contract-fidelity** — holds against `SCHEMA.md:361` (`INDEX|info`), `COWORK-LINT-CRON.md:108` (info = missing index entry) + `:84-88` (Tier-1 autofix = missing hub rows), and `decisions/2026-05-01-…:51` (Tier-1 autofix = missing index rows). Reusing `:361` unedited at the same severity is genuinely contract-faithful; the autofix-tier classification D10 leans on is real, not invented.
- **Part F minimal + accurate** — steps 3/4 + Maintenance Contract are one-clause appends; lint-contract rows correctly untouched. No over-reach.
- **Public-repo boundary (D3) intact** — SCHEMA.md is an internal wiki file; editing it in the wiki repo is within D3 and the internal-wiki-merges-without-review convention. Zero `vigil-skills/` files touched; prefix map from hub headers, not `states.json`.
- **No premature abstraction in Part E** — two helpers + two reads extend the existing two INDEX functions in place; mirrors the repo's own `:449-453`/`:721-724` duplication rather than introducing a shared abstraction at N=2. Correct call inside a safety-net patch.
- **Silent-additions check** — the two structural additions vs the brief (SCHEMA in scope; `info` over the brief's parenthetical "likely warn") are both spec-level additions with explicit rationale; the brief said "decide the severity," authorizing it. No (d) silent additions.
- **Live verification** — `node wiki-lint.mjs .` exit 0; revised Part E → 0 new findings; AC-5 gate satisfiable.

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 0 | P4: 0

STATUS: GREEN
