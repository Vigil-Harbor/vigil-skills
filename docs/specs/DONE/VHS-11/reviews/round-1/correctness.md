# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1.

**Grounding notes:** Spec, brief, `CLAUDE.md`, `skills/spec-cycle/SKILL.md`, and all three agent files read fresh from disk. Plane ticket VHS-11 retrieved from MCP memory (namespace `skills`, record `9bf0aea4`, all 6 chunks) — ticket and brief agree; the brief's framing correction on item 4 (agents already self-serve closure at round ≥ 2) is accurate against `agents/spec-reviewer-*.md` step 7. `git log -10` on the four touched files: most recent commit is `27d8f26` (2026-05-27, 14 days ago) — outside the 7-day window; no recently-shifted code. Anchor verification: every SKILL.md anchor the spec cites (`:23`, `:96`, `:99`, `:101`, `:107`, `:142–152`, `:144`, `:147`, `:172–174`, `:181`, `:264–273`, `:277–283`, `:280`, `:285–293`) and all three agent anchors (`correctness.md:146`, `edge-cases.md:141`, `conventions.md:135` — each the `**Severity:**` template line) match the current files exactly. Done-when items 1–9 map 1:1 to the brief's nine criteria. Step-number renumbering edit set is complete: a repo-wide grep confirms the only "step 6" cross-references are `SKILL.md:107` and `:147` (both covered), and no other file couples to spec-cycle's Phase 0 step numbers.

## Findings

### F-1: D1 fallback path references `origin/<branch>` — a ref the fallback exists because it doesn't have
**Severity:** P1
**Where:** spec.md § D1, steps 5c–5e (spec.md:99–107 vs :109–115, :119–146)
**Claim:** 5c says "If the current branch has no origin counterpart, fall back to the default branch … If none resolve: log `origin: skipped (no comparison branch)`." Then 5d runs `git rev-list --count HEAD..origin/<branch>` and 5e runs `git merge-base --is-ancestor HEAD origin/<branch>`, prompts "local `<branch>` is `<N>` commits behind origin/`<branch>`", and merges `git merge --ff-only origin/<branch>`.
**Why this is wrong:** `<branch>` is bound in 5c to the *current* branch (`git symbolic-ref --short -q HEAD` output: "Otherwise capture as `<branch>`"). The fallback to the default branch never binds a variable. So in the fallback path, every later use of `origin/<branch>` literally names the ref whose nonexistence triggered the fallback — `git rev-list --count HEAD..origin/<branch>` fails with "unknown revision," and the skill text gives no handling for that failure. The alternative reading (silently re-bind `<branch>` to the default branch) makes the 5e prompt misreport: "local main is N commits behind origin/main" while the user sits on `feature-x`. Either reading is defective, and this is precisely the case the brief's Risk 6 delegated to the spec author to define. Note the resulting ff offer in the fallback case also fast-forwards the *current feature branch* onto the default branch's tip — a surprising consequence the spec never states.
**Suggested fix:** Introduce a second placeholder in 5c — e.g., "capture the current branch as `<branch>`; bind the comparison ref as `<cmp>` (the counterpart `origin/<branch>` when it exists, else the resolved default branch)." Use `origin/<cmp>` throughout 5d–5e, make the prompt name both ("local `<branch>` is `<N>` commits behind `origin/<cmp>`"), and add one sentence stating what an ff update means in the fallback case (it moves `<branch>` to `origin/<cmp>`'s tip) — or restrict the ff *offer* to the counterpart case and warn-only in the fallback case.

### F-2: D5's two placement locators for the defining sentence contradict each other; one reading corrupts the output-contract template
**Severity:** P1
**Where:** spec.md:262 ("And one defining sentence below each template (after the 'If no findings' line)")
**Claim:** The defining sentence goes "below each template (after the 'If no findings' line)".
**Why this is wrong:** The "(If no findings: write "No findings.")" line sits *inside* the fenced output-contract template in all three agent files — `agents/spec-reviewer-correctness.md:154`, `agents/spec-reviewer-edge-cases.md:150`, `agents/spec-reviewer-conventions.md:143` — followed by `## Summary`, the `STATUS:` line, and the closing fence. "Below each template" and "after the 'If no findings' line" therefore point at two different places. The parenthetical reading inserts orchestrator-facing meta prose *into* the machine template, so every future reviewer report (all three lenses, all projects) would carry the stray sentence between Findings and Summary. Test-plan item 5 would not catch it — it checks the sentence exists and that STATUS/step-7 sections are unchanged, not where the sentence landed. This is a misleading edit anchor in the exact artifact class this spec is hardening.
**Suggested fix:** Replace the parenthetical with an unambiguous anchor: "directly below the closing code fence of the `# Output contract` template, before the 'The last non-blank line MUST be exactly one of' paragraph" (i.e., after `correctness.md:160`, `edge-cases.md:156`, `conventions.md:149`).

### F-3: 2g's move-out-of-Deferred mechanic references state no step creates for the green round
**Severity:** P2
**Where:** spec.md § D2, 2g steps 3–4 (spec.md:179–186)
**Claim:** "A candidate that exceeds these limits stays in `## Deferred (P2+)` untouched" and "Move each folded P2 out of `## Deferred (P2+)`…"
**Why this is wrong:** `## Deferred (P2+)` is populated only by 2e (`SKILL.md:181`), which runs only "If still red and `round < 4`." The round that goes green never executes 2e, so the final round's P2s — exactly the population 2g draws candidates from (PET-86: green at round 2 with ~5 fresh P2s) — were never written into Deferred. 2d's existing sentence (`SKILL.md:174`, "carried forward as spec notes in the `## Deferred (P2+)` section") gestures at it but no step performs the carry on the green round. 2g's steps 3–4 therefore instruct moving/keeping entries that may not exist. Graceful in practice (an LLM operator will improvise — which is the undocumented-discretion failure mode this ticket exists to remove), but the mechanism is incomplete as written.
**Suggested fix:** Add to 2g (between steps 1 and 3): "First record every final-round P2 in `## Deferred (P2+)` (the 2d carry-forward), then process candidates" — or rewrite step 4 to not presuppose: "Record each folded candidate in `## Post-green polish`; record every non-folded P2 (tagged or not) in `## Deferred (P2+)`."

### F-4: Origin token vocabulary deliberately supersedes the brief's Done-when enumeration — say so in the spec's Done-when, not only in D1
**Severity:** P3
**Where:** spec.md:149–159 and Done-when 2 (spec.md:321)
**Claim:** Six tokens (adds `behind-N (update failed — proceeded)`, `behind-N (diverged — proceeded)`; reshapes `skipped` → `skipped (<reason>)`) vs. the brief's Done-when list of four (`in-sync | behind-N (updated) | behind-N (user proceeded) | skipped`).
**Why this is wrong:** It isn't wrong — the rationale at spec.md:159 is sound (the brief's own Decision 1 mandates three distinct no-update outcomes its token list can't express) and Decision 1 semantics are preserved. But Phase 3's drift-check diffs Done-when against the brief literally, and spec Done-when 2 ("includes an origin token") silently elides the divergence. One clause closes the loop.
**Suggested fix:** In Done-when 2, append "(six-token vocabulary per § D1 rationale, superseding the brief's four-token list)."

### F-5: D1 misenumerates which step-4 sub-steps contain "continue to step 5"
**Severity:** P4
**Where:** spec.md:65 ("The 'continue to step 5' lines inside step 4 (a/b/d/f sub-steps)")
**Claim:** Those lines live in sub-steps a/b/d/f.
**Why this is wrong:** They occur six times, in sub-steps a, b, d, e, f, and g — `SKILL.md:36, 42, 56, 70, 76, 95`. The load-bearing conclusion (no text change needed; they now land on the origin check by design) holds for all six, and test-plan item 2's grep would still pass.
**Suggested fix:** "(a/b/d/e/f/g sub-steps — six occurrences)".

### F-6: "The skill's only working-tree mutation" is literally false
**Severity:** P4
**Where:** spec.md:73–74 (D1 intro) and spec.md:281–283 (D6 Bash bullet)
**Claim:** The ff merge is "the skill's only working-tree mutation" / "the lone working-tree mutation in this skill."
**Why this is wrong:** spec-cycle writes the spec and review reports into the working tree every run (`SKILL.md:279` — "Read, Edit, Write for spec authorship"). The brief carries the same phrasing (Decisions 1), so this is inherited, and the intended meaning (only git-level mutation of pre-existing tracked state) is clear in context.
**Suggested fix:** "the lone git-level mutation of existing tracked files" or "the only Bash/git working-tree mutation."

## Summary
P0: 0 | P1: 2 | P2: 1 | P3: 1 | P4: 2

STATUS: RED P0=0 P1=2 P2=1 P3=1 P4=2
