# Conventions Review — round 2

**Grounding notes:** Spec and brief read fresh, CLAUDE.md conventions noted, wiki `state.md` and `filemap.md` read (`architecture.md` does not exist; `decisions/` scan found no overlapping entries — the four grep hits are Dynasty/Plane-webhook pages, none constraining this spec), all five target files verified at every cited anchor, round-1 reviews read from disk, and the renumbering/placeholder claims grep-verified.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | D1 fallback path references `origin/<branch>` | CLOSED | spec § D1 5c binds `<cmp>` (counterpart vs fallback, spec.md:104–114); 5d uses `HEAD..origin/<cmp>` (spec.md:118); fallback comparison is informational-only, no ff offered (spec.md:126–132); new token `behind-N (informational — no counterpart)` (spec.md:179–180); § Decision 1 (spec.md:40) |
| correctness | F-2 (P1) | D5 defining-sentence anchor self-contradictory | CLOSED | spec § D5 re-anchored "immediately after the template's closing code fence, before the 'The last non-blank line MUST be exactly one of' paragraph" (spec.md:310); anchors `:160`/`:156`/`:149` verified correct against all three agent files |
| correctness | F-3 (P2) | 2g move-out-of-Deferred mechanic presupposes nonexistent state | CLOSED | spec § D2 2g rewritten source-agnostic with create-if-absent semantics (spec.md:206–218); 2g performs green-round carry-forward itself (spec.md:196–197); § Decision 3 (spec.md:48) |
| correctness | F-4 (P3) | Done-when 2 elides token-vocabulary supersession | CLOSED | spec.md:371 "(seven-token vocabulary per § D1 rationale, superseding the brief's four-token list)" |
| correctness | F-5 (P4) | Misenumerated "continue to step 5" sub-steps | CLOSED | spec.md:66 "all six occurrences: 4a/4b/4d/4e/4f/4g — `SKILL.md:36, 42, 56, 70, 76, 95`" — grep-confirmed |
| correctness | F-6 (P4) | "Only working-tree mutation" literally false | CLOSED | spec.md:75 and :330–331 now say "lone git-level mutation of existing tracked files" |
| edge-cases | F-1 (P1) | Branch binding breaks on fallback path | CLOSED | same root as correctness/F-1; same fix (spec § D1 5c/5e) |
| edge-cases | F-2 (P1) | 2g assumes Deferred entries exist on green round | CLOSED | same root as correctness/F-3; § D2 steps 2–4 create/remove entries explicitly (spec.md:206–218) |
| edge-cases | F-3 (P2) | No post-update re-validation after ff merge | CLOSED | 5e on-update branch re-confirms brief, re-reads CLAUDE.md, halts if `<TICKET-ID>.spec.md` arrived (spec.md:152–156); Test plan 1 covers it (spec.md:354) |
| edge-cases | F-4 (P2) | Pre-ship-tagged P2s from non-final rounds dropped | CLOSED | 2g step 1 collects from "**all rounds'** persisted reports", skips already-addressed, merges duplicates (spec.md:199–203) |
| edge-cases | F-5 (P2) | Closure manifest undefined for synthetic missing-STATUS P0 | CLOSED | D4 block defines `<lens>/STATUS (P0) "missing STATUS line"` notation reconciling with gate arithmetic (spec.md:286–290) |
| edge-cases | F-6 (P3) | Exit-code conflation in 5e; no 5d failure token | CLOSED | step-level catch-all → `origin: skipped (git error)` (spec.md:76–78); 5e distinguishes exit 1 (diverged) from exit > 1 (git error, shallow-clone note) (spec.md:162–170) |
| edge-cases | F-7 (P3) | Regex rejects digit-bearing prefixes | CLOSED | `^[A-Z][A-Z0-9]*-[0-9]+` with `WEB3-12` rationale (spec.md:243–244); Done-when 5 flags it as a superset of the brief's regex (spec.md:374) |
| edge-cases | F-8 (P3) | Transcript covers only happy ff path | CLOSED | Test plan 9 now exercises ff-success, diverged, and ff-abort with concrete scratch-repo recipes (spec.md:362); Done-when 9 (spec.md:378) |
| edge-cases | F-9 (P4) | Sub-step enumeration omits 4e/4g | CLOSED | same as correctness/F-5 |
| edge-cases | F-10 (P3) | "Verbatim" brief_path, normalization unstated | CLOSED | step 1 normalizes to project_root-relative forward-slash form (spec.md:232–234); D4 edit 1 carries the normalized path (spec.md:267–269) |
| conventions | F-1 (P2) | `closure_manifest` not mirrored into agents' inputs blocks | CLOSED | D4 edit 3 adds one identical line after `round_number` in all three inputs blocks (spec.md:296–300; anchors `:16`/`:16`/`:18` verified); Decision 5 names the VHS-1 `namespace` precedent (spec.md:56) |
| conventions | F-2 (P2) | Defining-sentence anchor self-contradictory | CLOSED | same root as correctness/F-2 |
| conventions | F-3 (P3) | Decision 4 blanket no-rename claim | CLOSED | Decision 4 now distinguishes out-of-tree (never moved) from in-tree (step 2's existing rename flow, unchanged) (spec.md:52); D3 closing note aligned (spec.md:259) |
| conventions | F-4 (P3) | `docs/customizing.md` goes silently stale | CLOSED | added to Scope table (spec.md:20) with concrete bullet wording in D3 (spec.md:261); Test plan 6 and 8 cover it (spec.md:359, :361) |
| conventions | F-5 (P3) | Token vocabulary expansion — category (c) | CLOSED | acknowledged in § Deferred (P2+) (spec.md:393); Done-when 2 annotation present |
| conventions | F-6 (P3) | Fetch-before-resolve ordering deviation — category (c) | CLOSED | acknowledged in § Deferred (P2+) (spec.md:394); Decision 2 carries the rationale (spec.md:44) |
| conventions | F-7 (P4) | Incomplete sub-step enumeration | CLOSED | same as correctness/F-5 |
| conventions | F-8 (P4) | HTML comment in template line | CLOSED | D5 template line is now bare `**Pre-ship recommended:** yes` (spec.md:307); defining sentence carries the optionality semantics (spec.md:313–317) |
| conventions | F-9 (P4) | `git rev-parse` absent from Tool-use bullet | CLOSED | D6 Bash bullet lists `git rev-parse` (and `git merge-base --is-ancestor`) in the read-only list (spec.md:326–328) |

The author's closure manifest (4 P1 entries) reconciles exactly with round 1's gate arithmetic (P0=0, P1=4 across lenses, with edge-cases/F-1 and F-2 sharing roots with correctness/F-1 and F-3); every manifest claim verified true against the spec on disk. No REOPENED, no PARTIAL.

## Findings

### F-1: Internal ticket IDs (`PET-86`, `MCP-33`) land in the public SKILL.md's example text, deviating from the `PROJ-123` placeholder idiom
**Severity:** P3
**Where:** spec § D3 step-1 replacement block, spec.md:243 (`PET-86-fix-MCP-33-regression.md` → `PET-86`)
**Convention violated:** SKILL.md's established placeholder idiom for example ticket IDs is generic `PROJ-123` (`skills/spec-cycle/SKILL.md:9`, `:23` — the exact line D3 replaces); user-recorded posture: vigil-skills is public and skills should keep internals out.
**Evidence:** Grep of `skills/spec-cycle/SKILL.md`: every example-placeholder ticket ID today is `PROJ-123` (`:9`, `:23`). The internal IDs that do appear (`MCP-33` at `:99`/`:290`, `CAL` at `:292`) are factual behavioral/historical references, not freely-chosen examples. The D3 replacement text ships a Petasos ticket name into the generic public skill where a generic two-token example would carry identical disambiguation value. (The example originates in brief Risk §5, so it is brief-carried — which is why this is P3, not P2.)
**Suggested fix:** In the D3 fenced replacement text only, genericize the example to something like `` `PROJ-86-fix-API-33-regression.md` → `PROJ-86` `` (two ID-shaped tokens preserved, so the anchoring rationale is unchanged). The spec/brief prose can keep the real PET-86 story.

### F-2: Done-when 1's counterpart-only narrowing of the brief's criterion lacks the explicit supersession annotation its siblings carry
**Severity:** P3
**Where:** spec § Done when item 1, spec.md:370; cf. brief Done-when bullet 1 ("behind-count > 0 produces a warning and an explicit user choice" — unconditional)
**Convention violated:** The spec's own self-annotation pattern for brief deviations, established in this revision: Done-when 2 says "superseding the brief's four-token list" and Done-when 5 says "digit-tolerant superset of the brief's `^[A-Z]+-[0-9]+`". Category (c) — spec-level deviation with rationale, surfaced per lens rules for drift-check visibility.
**Evidence:** Done-when 1 quietly inserts the qualifier "a **counterpart comparison** with behind-count > 0 produces a warning and an explicit user choice" — on the fallback-comparison path, behind-count > 0 now produces a warning with *no* user choice. The rationale is sound and present (§ Decision 1, spec.md:40; D1 5e, spec.md:126–132; the brief's Risk §6 delegated this path to the spec author), but unlike its two annotated siblings, the Done-when row never names itself as a deviation, so the Phase 3 literal diff against the brief's bullet 1 surfaces an unexplained mismatch.
**Suggested fix:** Append to Done-when 1 a clause in the established idiom, e.g., "(user choice on counterpart comparisons only — the fallback comparison is informational per § Decision 1, narrowing the brief's unconditional bullet 1)", or add a third one-liner to § Deferred (P2+) alongside the F-5/F-6 notes.

### F-3: customizing.md's closing claim "the skills hardcode these paths today" goes partially stale under the D3 edit
**Severity:** P4
**Where:** spec § D3 customizing.md instruction, spec.md:261 ("leave the other three bullets untouched") vs `docs/customizing.md:60`
**Convention violated:** Single-source-of-truth / no silently-stale sibling text — the same class as round-1 F-4, one sentence below the bullet being edited.
**Evidence:** `docs/customizing.md:60`: "Adjust the layout in your fork if needed; the skills hardcode these paths today." After D3, the brief path is tolerant by design, not hardcoded — the sentence stays true for only three of the four bullets it summarizes. The D3 instruction scopes the edit to the briefs bullet and explicitly freezes the other three bullets, but is silent on this closing sentence. (Also note the replacement bullet drops the existing "(loose: just enough to get started)" parenthetical, which describes brief *content*, not location — fine to drop, but worth doing knowingly.)
**Suggested fix:** Extend the D3 customizing.md instruction with one more clause: adjust the closing sentence to e.g. "the skills hardcode the spec/review/test-output paths; the brief path is tolerant on input."

### F-4: D4's rationale "P2 dispositions are already visible in `## Deferred (P2+)`" is inaccurate for fixed P2s
**Severity:** P4
**Where:** spec § D4 edit 2, spec.md:285–286
**Convention violated:** Accuracy of stated rationale (the spec's own discipline of explaining each bound).
**Evidence:** A round-(N−1) P2 that the author *fixes* in 2e never enters `## Deferred (P2+)` (SKILL.md:181 — "either fix or list"); its disposition is visible only in the spec diff. This very round demonstrates it: all five round-1 P2s were fixed, none appear in Deferred, and their dispositions reached this reviewer via an orchestrator side-note, not the section the parenthetical points at. The P0/P1-only scope itself is correct and brief-authorized (brief Decision 5, Risk §4) — only the justification sentence overclaims.
**Suggested fix:** Reword to "(P2 dispositions are visible in the spec's edits or its `## Deferred (P2+)` section)".

Positive notes (no findings): the `<cmp>`/`<branch>` two-variable fix resists inventing a second idiom — 5c's fallback chain mirrors step 4b verbatim and the spec says so; keeping the origin check inline as a step-4 sibling at N=2 remains the convention-correct anti-abstraction call; the D5 "(2g)" cross-skill step reference has direct precedent (`SKILL.md:113` references ship-spec Phase 0 step 4; `spec-retire/SKILL.md:11` references spec-reconcile Phase 0 step 1); the renumbering edit set is complete (grep confirms `:107`/`:147` are the only step-6 cross-references, and no other skill couples to spec-cycle's preflight numbering); no hardcoded MCP tool names enter any file (VHS-7 holds); reviewer read-only rule, STATUS contract, severity scale, green-gate formula, and step-7 logic are all untouched as the brief fences require; the sync-subtree claims (4 synced files, customizing.md repo-only) match CLAUDE.md's `SUBTREES` convention; and the ff-only mutation remains reconciled with "Do not commit. Do not push." via the D6 callout (a fast-forward creates no commit).

## Summary
P0: 0 | P1: 0 | P2: 0 | P3: 2 | P4: 2

STATUS: GREEN
