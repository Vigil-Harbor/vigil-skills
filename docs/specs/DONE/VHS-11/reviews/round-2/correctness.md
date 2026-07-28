# Correctness Review — round 2

**Grounding notes:** Spec (`C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-11.spec.md`, Draft v2), brief, CLAUDE.md, all three round-1 review files, and all five target files read fresh from disk. Plane ticket VHS-11 retrieved from MCP memory (namespace `skills`, record `9bf0aea4`, confidence 0.82) — ticket and brief agree. Anchor verification: every SKILL.md anchor (`:23`, `:96`, `:101`, `:107`, `:142–152`, `:144`, `:147`, `:152`, `:172–174`, `:181`, `:264–273`, `:277–283`, `:280`, `:285–293`) and all nine agent anchors (`correctness.md:16/:146/:160`, `edge-cases.md:16/:141/:156`, `conventions.md:18/:135/:149` — inputs-block `round_number` line, `**Severity:**` template line, template closing fence respectively) and `docs/customizing.md:51–60` (briefs bullet at `:55`) match current files exactly. The closure_manifest's four P0/P1 claims were independently verified against the v2 spec — all four hold. The renumbering grep confirms the only in-file step-number cross-references are SKILL.md:107 and :147 (both covered by the spec), the six "continue to step 5" lines inside step 4 (correctly left untouched), and :113 (references ship-spec's numbering, unaffected). `sync.py:30` confirms `SUBTREES = ("skills", "agents")`, validating the spec's claim that `docs/customizing.md` is outside the synced subtrees. Git log on touched files: newest commit `27d8f26` (2026-05-27) — outside the 7-day window.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | D1 fallback path references `origin/<branch>` | CLOSED | spec.md:104–114 — 5c binds `<cmp>` (counterpart vs fallback); 5d/5e use `origin/<cmp>` (:118, :126); ff offer restricted to counterpart (:124, :134); fallback informational-only with its own token (:126–132); Decision 1 (:40) encodes the paths |
| correctness | F-2 | D5 defining-sentence anchor self-contradictory | CLOSED | spec.md:310 — re-anchored "immediately after the template's closing code fence, before the 'The last non-blank line MUST be exactly one of' paragraph"; anchors `:160`/`:156`/`:149` verified as the closing fences in all three agent files |
| correctness | F-3 | 2g move-out-of-Deferred references state no step creates | CLOSED | spec.md:206–218 — 2g steps 2–4 are source-agnostic with "creating the section/entry if absent"; step 4 removes entries only "if the finding already has an entry" |
| correctness | F-4 | Token-vocabulary supersession unannotated in Done-when | CLOSED | spec.md:371 — Done-when 2: "(seven-token vocabulary per § D1 rationale, superseding the brief's four-token list)"; rationale paragraph at :184 |
| correctness | F-5 | Misenumerated "continue to step 5" sub-steps | CLOSED | spec.md:66 — "all six occurrences: 4a/4b/4d/4e/4f/4g — SKILL.md:36, 42, 56, 70, 76, 95"; grep confirms exactly those six lines |
| correctness | F-6 | "Only working-tree mutation" literally false | CLOSED | spec.md:75, :329–331 — rephrased to "the skill's lone git-level mutation of existing tracked files" in both D1 intro and D6 bullet |
| edge-cases | F-1 | Branch binding breaks on fallback path | CLOSED | Same root and fix as correctness/F-1 (spec.md:104–132) |
| edge-cases | F-2 | 2g assumes Deferred entries exist on green round | CLOSED | spec.md:195–197 ("the round that goes green never runs 2e... this step performs their carry-forward bookkeeping"), :206–218; 2d advisory cross-ref names 2g as the carrier (spec.md:224) |
| edge-cases | F-3 | No post-update re-validation after ff merge | CLOSED | spec.md:152–156 — on-update branch re-confirms brief (step 2), re-reads CLAUDE.md (step 3), halts if `<TICKET-ID>.spec.md` arrived with the update |
| edge-cases | F-4 | Non-final-round tagged P2s silently drop | CLOSED | spec.md:199–203 — 2g step 1 collects "from **all rounds'** persisted reports — not only the final round's", with dedup and already-addressed skip |
| edge-cases | F-5 | Manifest undefined for synthetic missing-STATUS P0 | CLOSED | spec.md:286–290 — `<lens>/STATUS (P0) "missing STATUS line" — <disposition>` notation "so the manifest always reconciles with the prior round's gate arithmetic" |
| edge-cases | F-6 | Exit-code conflation in 5e; no 5d failure token | CLOSED | spec.md:76–78 (step-level catch-all → `origin: skipped (git error)`); :168–170 (exit > 1 mapped to catch-all, shallow-clone named) |
| edge-cases | F-7 | Regex rejects digit-bearing prefixes | CLOSED | spec.md:243–244 — `^[A-Z][A-Z0-9]*-[0-9]+` with `WEB3-12` rationale; Done-when 5 (:374) annotates the superset |
| edge-cases | F-8 | Dry-run covers only happy ff path | CLOSED | spec.md:362 — Test-plan item 9 now pins ff-success, diverged (no offer), and ff-abort (verbatim error, no retry) transcripts |
| edge-cases | F-9 | Step-4 sub-step enumeration incomplete | CLOSED | Same fix as correctness/F-5 (spec.md:66) |
| edge-cases | F-10 | "Verbatim" brief_path unnormalized | CLOSED | spec.md:232–234 (step 1 normalization: project_root-relative, forward slashes); :267–269 (D4 edit 1 carries the normalized path) |
| conventions | F-1 | closure_manifest not mirrored into agent input contract | CLOSED | spec.md:296–300 — D4 edit 3 adds the identical `closure_manifest` line after `round_number` in all three agents (`:16`/`:16`/`:18` verified); Decision 5 (:56) |
| conventions | F-2 | Defining-sentence anchor contradiction | CLOSED | Same fix as correctness/F-2 (spec.md:310) |
| conventions | F-3 | Decision 4 overstates "never moved or renamed" | CLOSED | spec.md:52 — scoped: "Out-of-tree briefs are never moved or renamed...; in-tree briefs remain subject to step 2's existing local-only-ticket rename flow (unchanged)" |
| conventions | F-4 | customizing.md layout section goes silently stale | CLOSED | spec.md:20 (Files-to-change row) + :261 (D3 briefs-bullet edit); Done-when 5 (:374) covers it |
| conventions | F-5 | Token expansion flagged for drift-check | CLOSED | spec.md:393 — Deferred entry with disposition; Done-when 2 annotation done |
| conventions | F-6 | Fetch-before-resolve ordering deviation | CLOSED | spec.md:44 (Decision 2 carries the rationale, scopes step 4 out) + :394 Deferred entry |
| conventions | F-7 | Sub-step enumeration incomplete | CLOSED | Same fix as correctness/F-5 (spec.md:66) |
| conventions | F-8 | HTML comment in emitted template line | CLOSED | spec.md:307 — template line is now bare `**Pre-ship recommended:** yes`; optionality lives in the defining sentence (:313–317) |
| conventions | F-9 | `git rev-parse` absent from Tool-use bullet | CLOSED | spec.md:328 — extended D6 bullet lists `git rev-parse` in the read-only set |

No REOPENED or PARTIAL items. The closure manifest's four stated dispositions all verify against the spec as claimed.

## Findings

### F-1: D3's customizing.md edit leaves the section's closing line stale ("the skills hardcode these paths today")
**Severity:** P3
**Where:** spec.md:261 (§ D3, customizing.md edit)
**Claim:** "change the briefs bullet to read 'Briefs at `docs/specs/TODO/<TICKET-ID>.brief.md` (canonical; alternate directories and `<TICKET-ID>-slug.md` filenames are tolerated on input...)' and leave the other three bullets untouched."
**Why this is wrong:** The edit is correct as far as it goes, but the same section closes with `docs/customizing.md:60`: "Adjust the layout in your fork if needed; the skills hardcode these paths today." After D3 lands, the brief path is precisely no longer hardcoded — the section's own bullet will say so five lines earlier. The edit instruction covers the four bullets but is silent on the closing sentence, leaving the delivered file mildly self-contradictory. A careful reader unravels it (the bullet's parenthetical is more specific), so this is an improvement, not a blocker.
**Suggested fix:** Extend the D3 customizing.md edit with one more clause: adjust `:60` to e.g. "Adjust the layout in your fork if needed; the skills hardcode the spec/reviews/test-output paths today (brief location is tolerant on input per the bullet above)."

### F-2: Done-when 1's counterpart-only narrowing of the brief's "explicit user choice" lacks the supersession annotation Done-when 2 and 5 carry
**Severity:** P4
**Where:** spec.md:370 (Done-when 1) vs brief Done-when bullet 1 (brief.md:59)
**Claim:** "a counterpart comparison with behind-count > 0 produces a warning and an explicit user choice (ff-only update / proceed)".
**Why this is wrong:** It isn't wrong — the brief's Risk §6 delegated fallback behavior to the spec, Decision 1 (spec.md:40) carries the rationale, and the round-1 suggested fix explicitly endorsed restricting the offer to the counterpart case. But the brief's bullet 1 is unqualified ("behind-count > 0 produces a warning and an explicit user choice"), and the spec's v2 convention — established by Done-when 2 ("superseding the brief's four-token list") and Done-when 5 ("digit-tolerant superset of the brief's...") — is to flag each delegated-decision divergence inline so the Phase 3 drift-check diff is self-explaining. Done-when 1 narrows silently by qualifier instead.
**Suggested fix:** Append to Done-when 1: "(choice restricted to counterpart comparisons per brief Risk §6 delegation; fallback comparisons are warn-only per Decision 1)."

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 1

STATUS: GREEN
