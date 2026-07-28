# Conventions Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: Closure-manifest prompt field not mirrored into the agents' documented input contract
**Severity:** P2
**Where:** spec § D4 (`docs/specs/TODO/VHS-11.spec.md:225-252`) vs. § Scope file table (rows for the three agent files, `:17-19`)
**Convention violated:** Repo precedent from VHS-1: orchestrator prompt fields added to the 2b dispatch are mirrored into each agent's "The orchestrator passes these in your prompt:" block. Wiki filemap (`vigil-harbor-wiki/projects/vigil-skills/filemap.md:48`): "`namespace` added to orchestrator-provided inputs block" — namespace landed on *both* sides of the contract.
**Evidence:** `agents/spec-reviewer-correctness.md:10-16` enumerates exactly six prompt fields (`spec_path`, `brief_path`, `project_root`, `ticket_id`, `namespace`, `round_number`); same block exists in all three agents. D4 mandates a new round-N>1 `closure_manifest` prompt block, and the spec's Decision 5 claims "agents now verify the author's claim against the spec instead of inferring intent from a diff" — but the only agent-file edit is D5's marker. The brief's Out-of-scope fence covers "the reviewer agents' step-7 closure logic or closure-table format," not the inputs block, so mirroring is permitted. As written, the behavioral claim rests on agents spontaneously consuming an undocumented prompt block.
**Suggested fix:** Extend the three agent-file edits (D5 or a small D4b) to add one line to each agent's orchestrator-inputs block — e.g., `closure_manifest` — the author's stated disposition of round-(N−1) P0/P1 findings (rounds ≥ 2 only; verify these claims in step 7) — leaving step-7 logic and the closure-table format untouched.

### F-2: D5's defining-sentence anchor is self-contradictory (inside vs. outside the output template)
**Severity:** P2
**Where:** spec § D5, `docs/specs/TODO/VHS-11.spec.md:262` ("And one defining sentence below each template (after the 'If no findings' line)")
**Convention violated:** Internal consistency of anchors; the agents' fenced output templates are emitted verbatim by reviewers, so anything inserted inside the fence becomes report content.
**Evidence:** The `(If no findings: write "No findings.")` line sits **inside** the fenced ```markdown template in all three agent files (`agents/spec-reviewer-correctness.md:154`, `agents/spec-reviewer-edge-cases.md:150`, `agents/spec-reviewer-conventions.md:143`); the fence closes several lines later after `STATUS: GREEN`. "Below each template" points after the closing fence; "after the 'If no findings' line" points inside it, between `## Findings` and `## Summary`. Following the parenthetical literally injects instruction prose into the emitted report shape of all three reviewers.
**Suggested fix:** Re-anchor unambiguously: "immediately after the template's closing ``` fence, before the 'The last non-blank line MUST be...' paragraph" (and drop the 'If no findings' parenthetical).

### F-3: Decision 4's blanket "Briefs are never moved or renamed by this skill" overstates the design and clashes with unchanged step-2 text
**Severity:** P3
**Where:** spec § Decision 4 (`docs/specs/TODO/VHS-11.spec.md:51`) and § D3 closing note (`:223`)
**Convention violated:** Spec decisions should accurately characterize the text they leave in place (the spec's own "Files to leave alone" discipline).
**Evidence:** Existing `skills/spec-cycle/SKILL.md:25` instructs: "rename all `<TICKET-ID>.*` artifacts under `docs/specs/TODO/` (**brief**, spec, reviews directory, test output)". The brief is not "an artifact the skill itself created," yet step 2 explicitly renames it in the in-tree case. D3's step-1 replacement text is correctly scoped ("A brief **outside that directory** stays where it is... never moved or promoted"), but Decision 4's summary sentence is unscoped and contradicts the preserved step-2 instruction for canonical-location briefs.
**Suggested fix:** Scope the Decision 4 sentence: "Out-of-tree briefs are never moved or renamed by this skill; in-tree briefs remain subject to step 2's existing local-only-ticket rename flow."

### F-4: `docs/customizing.md` "Spec & brief layout" goes silently stale under D3
**Severity:** P3
**Where:** spec § Scope "Files to change" / "Files to leave alone" (`docs/specs/TODO/VHS-11.spec.md:12-33`)
**Convention violated:** Reuse / single-source-of-truth — the brief-layout statement lives in two committed places, and the spec updates only one. CLAUDE.md lists `docs/customizing.md` as the downstream-facing configuration guide.
**Evidence:** `docs/customizing.md:55`: "Briefs at `docs/specs/TODO/<TICKET-ID>.brief.md`" — exactly the expectation D3 loosens. The file appears in neither the change table nor the leave-alone list, so the omission is undeclared rather than decided. (Parenthetically: untracked `docs/spec-workflow-reference.md:17,20` states the same expectation and Phase 0 step numbering; untracked, so informational only.)
**Suggested fix:** Either add a one-line customizing.md edit to scope ("brief location is tolerant on input; spec artifacts are canonical at `docs/specs/TODO/`") or list it under "Files to leave alone" with a stated reason.

### F-5: Preflight-token vocabulary expanded beyond the brief's four tokens — spec-level addition, flagged with rationale
**Severity:** P3
**Where:** spec § D1 preflight summary + rationale (`docs/specs/TODO/VHS-11.spec.md:149-159`); brief Done-when bullet 2 names exactly `in-sync | behind-N (updated) | behind-N (user proceeded) | skipped`
**Convention violated:** None — this is a category (c) classification (spec-level addition with explicit rationale) surfaced per lens rules so the human drift-check sees it. The rationale (the brief's own Decision 1 requires three distinguishable no-update outcomes) is sound, and the ff-abort path (`update failed — proceeded`) is likewise a spec-added path consistent with never-auto-pull.
**Evidence:** Spec line 159: "Rationale for two tokens beyond the brief's four..."
**Suggested fix:** None required; ensure the Phase 3 drift-check checklist row for brief Done-when bullet 2 notes the expanded vocabulary.

### F-6: Fetch-before-resolve ordering deviates from the VHS-6 step-4 idiom — spec-level deviation, flagged with rationale
**Severity:** P3
**Where:** spec § Decision 2 (`docs/specs/TODO/VHS-11.spec.md:41-43`) and D1 step 5b parenthetical (`:89-91`)
**Convention violated:** None violated — brief Decision 2 says "mirror the VHS-6 pattern... don't invent a second idiom," and the spec deviates on one axis (b/c order) with explicit, technically correct rationale: `git rev-parse --verify origin/<branch>` in 5c can only see a counterpart branch after a fetch, whereas step 4 resolves via `refs/remotes/upstream/HEAD` before fetching (`skills/spec-cycle/SKILL.md:38-48`). Category (c) — surfaced for drift-check visibility.
**Suggested fix:** None required.

### F-7: D1's "continue to step 5" enumeration is incomplete (a/b/d/f — actually a/b/d/e/f/g)
**Severity:** P4
**Where:** spec § D1 first paragraph (`docs/specs/TODO/VHS-11.spec.md:65`)
**Convention violated:** Anchor accuracy (the conclusion — no text change needed — is correct for all occurrences).
**Evidence:** `skills/spec-cycle/SKILL.md` contains six "continue to step 5" lines inside step 4: `:36` (4a), `:42` (4b), `:56` (4d), `:70` (4e), `:76` (4f), `:95` (4g). The spec's parenthetical names only "a/b/d/f". An implementer grepping to verify per Test-plan item 2 would count six, not four.
**Suggested fix:** Change the parenthetical to "(a/b/d/e/f/g sub-steps — six occurrences)".

### F-8: HTML comment embedded in the emitted findings-template line
**Severity:** P4
**Where:** spec § D5 template line (`docs/specs/TODO/VHS-11.spec.md:259`): `**Pre-ship recommended:** yes   <!-- optional; P2 findings only -->`
**Convention violated:** Existing template idiom — option enumeration inline (`**Severity:** P0 | P1 | P2 | P3 | P4`) with usage instructions outside the fence; no HTML comments anywhere in the three templates today.
**Evidence:** Reviewers copy template lines verbatim into reports; the comment risks being emitted literally. The defining sentence (D5's second edit) already carries the optionality semantics, making the comment redundant.
**Suggested fix:** Drop the HTML comment from the template line; the defining sentence suffices.

### F-9: `git rev-parse` still absent from the extended Tool-use bullet
**Severity:** P4
**Where:** spec § D6 Bash bullet (`docs/specs/TODO/VHS-11.spec.md:277-284`)
**Convention violated:** Tool-use notes should enumerate the git commands the skill runs. Preexisting omission (step 4b already uses `git rev-parse --verify`, unlisted at `skills/spec-cycle/SKILL.md:280`), but D1 step 5c adds two more uses, and the bullet is being rewritten anyway.
**Suggested fix:** Add `git rev-parse` to the read-only list in the extended bullet.

Positive notes (no findings): the spec correctly resists extracting a shared "staleness check" abstraction at N=2 (two inline siblings is the convention-correct call); no host-specific tool names are introduced (VHS-7 host-agnostic rule holds); the reviewer read-only rule, shared severity scale, green-gate formula, and round cap are untouched as the brief requires; the `--ff-only` mutation is reconciled with SKILL.md's "Do not commit. Do not push." via the D6 Tool-use callout; the `**Pre-ship recommended:**` bold-label form matches the existing findings-template idiom better than the brief's camelCase suggestion (and the brief delegates the mechanism). All line anchors checked in `skills/spec-cycle/SKILL.md` (`:23`, `:96`, `:99`, `:101`, `:107`, `:144`, `:142-152`, `:172-174`, `:181`, `:264-273`, `:277-283`, `:285-293`) and the three agent anchors (`:146`/`:141`/`:135`) verify against current files at HEAD `27d8f26`.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 4 | P4: 3

STATUS: GREEN
