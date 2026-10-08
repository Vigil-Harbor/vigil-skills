# Conventions Review — round 1

Grounding: spec and brief read fresh from disk; `AGENTS.md` (canonical) and the machine-local `CLAUDE.md`; wiki `projects/vigil-skills/state.md` and `filemap.md` (no `architecture.md` exists for this project); wiki decisions `2026-10-08-vhs-45-…`, `2026-10-08-vhs-46-…`, `2026-09-08-vhs-37-…` (grep); `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `docs/customizing.md`, `docs/spec-workflow-reference.md`; the three target skills and `skills/spec-brief/SKILL.md` for the flag/usage idiom. Ticket lookup skipped per orchestrator note (ACL); the brief is the ticket text.

The spec has no `## Deferred — follow-up required` section, so there are no rows to validate.

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: The classification table and the marker parse rule have no stated home in `/spec-cycle`, and nothing pins the three copies together
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:77 (Decision 4 step 3), spec.md:97-112 (Decision 5), spec.md:181, :188, :194, :202 (Design)
**Convention violated:** Single source of truth for restated rules. The repo's pattern when a rule must live in more than one installed file is to restate it identically and pin that in the checklist (wiki `decisions/2026-09-08-vhs-37-spec-cycle-fold-defer-reject-routing.md:29`: "The four reviewer agents carry a byte-identical Deferred-findings block"). The spec follows that pattern for the fingerprint (spec.md:240) but not for the classification table or the reader's parse rule.
**Evidence:** Attest mode is "Decision 4 in full" (spec.md:188) and step 3 says "classify it by Decision 5" (spec.md:77), but a spec decision number cannot appear in skill text, and the Design bullet for `## The verdict marker` lists only "Decision 1's template and field rules, Decision 2, and the failed-write rule from Decision 3" (spec.md:181). Decision 5's table is placed in `/ship-spec` (spec.md:194) and, minus one row, in `/spec-tickets` (spec.md:202), and nowhere in `/spec-cycle`. The reader rule "takes the first line for each key and ignores anything else" (spec.md:43) is placed only in `/spec-cycle`, although the two skills that actually read the marker are the other two. The Test plan has no row that the copies agree.
**Suggested fix:** In Design § `skills/spec-cycle/SKILL.md`, add to the `## The verdict marker` bullet: "It also holds Decision 5's classification table; `## Attest mode` refers to it by section name." In Design § ship-spec and § spec-tickets, add: "carries the reader rule from Decision 1 (first line per key; `verdict:` and `ticket:` checked) with the table." Add one Test plan checklist row: "The classification table reads the same in `/spec-cycle` and `/ship-spec`; `/spec-tickets`' copy differs only by the missing `changed` row and its no-fingerprint note."

### F-2: Three spellings of the attest invocation; the usage line says `<brief-path>` where a spec path is accepted
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:71 (Decision 4), spec.md:125 (Decision 6 halt block), spec.md:180 and :211 (Design)
**Convention violated:** Naming consistency; the sibling usage-line idiom states exactly what is accepted (`skills/spec-brief/SKILL.md:30`, `skills/spec-tickets/SKILL.md:27`).
**Evidence:** Invocation is `/spec-cycle <path> --attest "<reason>"` with "`<path>` is the brief path or the spec path" (spec.md:71, :180). The usage halt on the same line prints `Usage: /spec-cycle <brief-path> [--attest "<reason>"]`. `AGENTS.md` and `README.md` are to show `/spec-cycle <brief-path> [--attest "<reason>"]` (spec.md:211). `/ship-spec`'s red block tells the operator to run `/spec-cycle <spec-path> --attest "<reason>"` (spec.md:125). An operator who follows the red block is passing a spec path to a command whose usage line and docs say brief path.
**Suggested fix:** Keep the one-line doc form `/spec-cycle <brief-path> [--attest "<reason>"]` in `AGENTS.md`/`README.md` and add to spec.md:211: "each adds the clause 'with `--attest` the path may be the spec path'". Change the usage halt at spec.md:71 to two lines: `Usage: /spec-cycle <brief-path>` and `       /spec-cycle <brief-or-spec-path> --attest "<reason>"`. Leave spec.md:125 as is.

### F-3: `/spec-tickets` keeps "Green-lit check" as the name of the heading check after a real verdict read arrives
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:13 (Scope row), spec.md:199-206 (Design § spec-tickets)
**Convention violated:** Naming and labels — a name that conflicts with new usage. The spec fixes the same conflict in `/ship-spec` ("The 'Spec not green' failure mode is rewritten", spec.md:138) and leaves it in `/spec-tickets`.
**Evidence:** `skills/spec-tickets/SKILL.md:35` is "3. **Green-lit check.**" (the seven-heading check) and `skills/spec-tickets/SKILL.md:176` is "**Spec not green-lit** (a required heading missing or duplicated)". After this change step 4 reads the verdict and the preflight line prints `headings: ok · verdict: <state>` (spec.md:203), so the skill would carry a step named green-lit that is not the green check, next to a failure-mode bullet "red verdict halts in preflight" (spec.md:206). No test or lint pins either label (`tests/`, `lint.py` grep: no match).
**Suggested fix:** Add to Design § spec-tickets: "**Phase 0 step 3:** the bold label becomes `Heading check.`; its text is unchanged. **Failure modes:** `Spec not green-lit` becomes `Spec headings incomplete`." Add "Step 3's label" to the Scope row at spec.md:13.

### F-4: The 2f-i sentence edit does not say where the new clause goes, and one position breaks an existing referent
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:186 (Design § spec-cycle, 2f-i)
**Convention violated:** Clarity of an edit to pinned prose; the project memory note on prose-spec gates (assert the edited region, not a count).
**Evidence:** `skills/spec-cycle/SKILL.md:663-668` reads "2f-i never re-dispatches reviewers, … never edits the brief, and runs at most once per invocation. That last bound is held in context: …". The spec says the sentence "gains: never rewrites the verdict marker". Appended at the end of the list, "That last bound" would then point at the marker clause.
**Suggested fix:** Replace spec.md:186 with: "**2f-i.** In the closing '2f-i never …' sentence, insert `never rewrites the verdict marker,` directly after `never edits the brief,` so that `runs at most once per invocation` stays the last item and 'That last bound' still refers to it."

### F-5: The test command checks two skills' frontmatter where the Test plan claims three, so the VHS-51 fence on `/ship-spec` is unguarded
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:227 (Test plan item 8), spec.md:250 (Test command, final clause)
**Convention violated:** The brief's Out-of-scope fence ("Adding a `requires:` block to `/ship-spec`", brief.md:58) and the spec's own Decision 10; the mechanical gate should hold the fence it names.
**Evidence:** Item 8: "the frontmatter of the three skills is unchanged." The command's last clause diffs only `skills/spec-cycle/SKILL.md skills/spec-tickets/SKILL.md`. `python lint.py --strict` passes with or without a `requires:` block on `/ship-spec` (`missing-requires` is a WARN, `docs/authoring-portable-skills.md:36`), and `tests/test_lint.py:52` counts skills, not blocks. An implementer who adds the block while adding a shell hash step to `/ship-spec` passes every mechanical check.
**Suggested fix:** In the final clause of the test command, change the path list to `skills/spec-cycle/SKILL.md skills/spec-tickets/SKILL.md skills/ship-spec/SKILL.md`.

### F-6: The failed-write rule is a load-bearing position the brief does not carry, stated without being marked as a spec-level addition
**Severity:** P2
**Where:** spec.md:65 (Decision 3, last paragraph before the Phase 3 line), spec.md:67
**Convention violated:** Silent addition vs the brief (class d). Decision 3 is labelled "(brief 8, 13, 17; Risks 2, 3)"; none of those covers a write that fails. The spec does label its other addition (`docs/customizing.md`, spec.md:16).
**Evidence:** "A marker write that fails does not change the run's outcome." A green run whose green write failed still prints SPEC READY and the `/ship-spec` next step while the marker on disk says pending. That is a defensible choice (downstream meets the confirm), but it is a choice. Separately, spec.md:67 adds `Verdict: green — <path>` to the Phase 3 template without saying what that line prints when the write failed.
**Suggested fix:** Prefix the paragraph at spec.md:65 with "Spec-level addition (the brief does not say what a failed write does):" and add one sentence of rationale: "the verdict was reached; the marker is its record, and a missing record already has a safe downstream path (the confirm)." Add to spec.md:67: "When the green write failed, the line reads `Verdict: green — marker NOT written`."

### F-7: Labelled and derivable spec-level additions, listed for the drift check
**Severity:** P3
**Where:** spec.md:16, :40, :95, :71, :203
**Convention violated:** None. Class (c) items the human drift check should see.
**Evidence:** (1) `docs/customizing.md` joins the Scope; labelled, with the VHS-46 precedent, which holds (`docs/customizing.md:77` is VHS-46's line in the same list). (2) `replaces: unreadable` and attestation over an unreadable marker; brief 11 says "or none" and brief 12 lists four cases, but brief 14 treats unreadable as missing, so this follows. (3) "any other flag halts" (spec.md:71) gives `/spec-cycle` an unknown-flag halt it does not have today; covered by Risk 4 and it matches `skills/spec-brief/SKILL.md:30`. (4) The `reviews: present | absent` token is removed from `/spec-tickets`' preflight line (spec.md:203), with a stated reason; nothing else in the repo reads that token.
**Suggested fix:** None required. Optionally mark items 2 to 4 "spec-level" in place, as item 1 is.

### F-8: Headless `/ship-spec` now stops on every pre-existing spec; the VHS-46 decision rejected a headless stop on other grounds
**Severity:** P3
**Where:** spec.md:112 (Decision 5), spec.md:136 (Decision 6), spec.md:162 (Decision 8)
**Convention violated:** None; the brief authorizes it (Decision 2: "A host that cannot wait stops"). Flagged so the wiki record stays coherent.
**Evidence:** `decisions/2026-10-08-vhs-46-ship-spec-review-gate-declared-one-pass.md:23`: "Halt when a declared review is unavailable: Rejected. The repo is public and must run on any harness; a headless run … would stop every time." Under this spec a headless `/ship-spec` stops on `missing`, `pending`, `unreadable` and `changed`, and no existing spec has a marker (Decision 8). The subjects differ (an optional review vs whether the spec was reviewed at all), so this is not a contradiction, but the spec does not say so. The same decision's process note ("a fix that adds a new stop or menu tends to draw the next finding") applies to the two new prompts.
**Suggested fix:** Add one sentence to Decision 8: "A headless `/ship-spec` stops on every spec that has no green marker. VHS-46 rejected a headless stop for an unavailable review because that review is optional; an unreviewed spec is not, and the brief chose the stop (Decision 2)."

### F-9: Tool-use notes are updated for `/spec-cycle` only
**Severity:** P3
**Where:** spec.md:189 vs spec.md:192-206
**Convention violated:** `docs/portability-contract.md:117` — the Tool-use notes section documents the skill's own tool surface.
**Evidence:** `/ship-spec` gains a shell hash command and a read of the marker; its notes say "Bash for git, gh, package-manager commands" (`skills/ship-spec/SKILL.md:375`). `/spec-tickets` gains a read of the marker; its notes say "File reading and writing for the spec and, in `local` mode, the ticket files" (`skills/spec-tickets/SKILL.md:167`), and "No shell" (`:170`) stays true.
**Suggested fix:** Add to Design § ship-spec: "**Tool-use notes:** the Bash bullet gains 'and the fingerprint hash'." Add to Design § spec-tickets: "**Tool-use notes:** the first bullet gains 'and the verdict marker (read only)'."

### F-10: Attest mode restates the seven-heading list a third time
**Severity:** P3
**Where:** spec.md:76 (Decision 4 step 2)
**Convention violated:** Reuse vs duplicate.
**Evidence:** The same list is at `skills/spec-cycle/SKILL.md:298` (Phase 1 re-run rule, "lacks any of") and, in a stricter form, at `skills/spec-tickets/SKILL.md:35` ("exactly once … outside a fenced block"). Attest mode lives in the same file as the first.
**Suggested fix:** Change step 2 to: "If the spec lacks any heading Phase 1's re-run rule requires, halt: `cannot attest: <heading> is missing`." State whether a duplicated heading is refused; `/spec-tickets` would refuse it later.

### F-11: Fingerprint as a prose shell command where the repo's precedent for deterministic, platform-sensitive steps is a tested script
**Severity:** P3
**Where:** spec.md:51-55 (Decision 2)
**Convention violated:** None; brief Decision 16 fixes "both use shell" and Risk 1 gives the command to the spec author. The tagged-example form matches `docs/authoring-portable-skills.md:20`.
**Evidence:** VHS-29 (wiki `state.md`, "What's Shipped") moved `/spec-close`'s log prepend "out of prose into `skills/spec-close/scripts/prepend_log_entry.py`" because the prose version went wrong on real input. The example given (`tr`, `sha256sum`) does not exist in Windows PowerShell, which is this machine's primary shell; a host that cannot compute lands in `changed` and asks to confirm, so the failure is safe but would be routine there.
**Suggested fix:** None for this ticket. If `changed` prompts turn out to be routine on Windows hosts, a stdlib script is the follow-up, and it belongs with VHS-51 because it makes `/ship-spec`'s shell dependency load-bearing.

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 5 | P4: 0

STATUS: GREEN
