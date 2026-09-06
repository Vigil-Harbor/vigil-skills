# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: `Done when` 9 and checklist 8 require a four-stage lifecycle in `README.md` and `docs/spec-workflow-reference.md`, but Design 5's edits cannot produce one — neither file mentions `/spec-close` at all

**Severity:** P0
**Where:** spec § Design 5 (`:331–346`); § Done when item 9 (`:393`); § Test plan checklist item 8 (`:368`)
**Convention violated:** the spec's own explicit `Done when` criterion, carried 1:1 from the brief (`VHS-32.brief.md:79` — "`AGENTS.md`, `docs/spec-workflow-reference.md`, and `README.md` describe the four-stage lifecycle")
**Evidence:**
- `grep -n "spec-close" README.md` → **no matches**. `README.md:9–11` lists exactly `/spec-cycle`, `/ship-spec`, `/review-pr`.
- `grep -n "spec-close" docs/spec-workflow-reference.md` → **no matches**. Its headings are `## Skill 1: spec-cycle` (`:7`), `## Skill 2: ship-spec` (`:97`), `## Adapting to your stack` (`:162`). There is no Skill 3.
- Design 5's README edit adds only `/spec-brief` and `/grill-me` bullets plus a `grilling` note; its reference-doc edit adds only `## Skill 0: spec-brief` and rewrites line 3 to *"An optional interview stage plus **two** AI-driven skills…"* — which contradicts "four-stage lifecycle" in the same spec.
- Post-edit, README would list five slash commands and describe three lifecycle stages; the reference doc would describe three. Checklist 8 ("describe four stages in the order brief → cycle → ship → close") fails on both files as written.

This is a pre-existing gap — VHS-12 shipped `/spec-close` and updated the gitignored `CLAUDE.md` (wiki `projects/vigil-skills/state.md`, VHS-12 entry: "`CLAUDE.md` lifecycle → 'Three skills' (gitignored in-repo)") but never reached `README.md` or the reference doc. VHS-32 is the first ticket to assert those files describe the full lifecycle, so it inherits the gap.

**Suggested fix:** pick one and state it —
(a) widen Design 5: add a `/spec-close <spec-path>` bullet to `README.md` § Skills and a `## Skill 3: spec-close` section (or a one-paragraph pointer) to `docs/spec-workflow-reference.md`, and make the reference-doc intro read "An interview stage plus three AI-driven skills…"; add both paths to the Scope table; or
(b) narrow `Done when` 9 and checklist 8 to what Design 5 actually delivers — "`AGENTS.md` describes the four-stage lifecycle; `README.md` and `docs/spec-workflow-reference.md` each document `/spec-brief` upstream of `/spec-cycle`" — and record the `/spec-close` documentation gap as an explicit out-of-scope fence with a follow-up ticket.

---

### F-2: 2f-i seeds from four lenses, but the halt block it edits still hardcodes three — contradicting D8's "exactly the titles the halt printed"

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D8 (`:65`); § Design 4 Edit 1 (`:305–315`), Edit 2 step 1 (`:319`)
**Convention violated:** the VHS-15 closure generalization — wiki `decisions/2026-06-16-vhs-15-optional-scalability-lens.md` § Consequences: *"The closure machinery is generalized from 'three reviewer reports' to 'every report present per round'"*
**Evidence:** `skills/spec-cycle/SKILL.md:466–485` — the fenced halt block prints exactly three bullets:

```
Remaining P0/P1:
  - <round 4 correctness P0/P1 titles>
  - <round 4 edge-cases P0/P1 titles>
  - <round 4 conventions P0/P1 titles>
```

No scalability line. The spec's Edit 2 step 1 reads `correctness.md`, `edge-cases.md`, `conventions.md`, "plus `scalability.md` when the scale lens ran", while D8 states the seed is "exactly the remaining P0/P1 titles the halt printed" and Edit 1's new menu line advertises "the titles above." On a scale-declared brief, option 4 grills findings the operator was never shown.

**Suggested fix:** Edit 1 is already rewriting that fenced block — add a fourth bullet `- <round 4 scalability P0/P1 titles, when the scale lens ran>`, and note in Design 4 that this closes a residual three-lens hardcode VHS-15 left in 2f. Alternatively, restrict 2f-i's seed to the three standing lenses and say so.

---

### F-3: `/spec-brief` copies `/spec-cycle`'s hardcoded `~/.claude/` states.json path rather than `/spec-close`'s `$CLAUDE_CONFIG_DIR`-aware resolution

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 Phase 0 step 3 (`:227`) — "Read `states.json` exactly as `/spec-cycle` Phase 0 step 7 does (same path, same fallbacks…)"
**Convention violated:** `docs/portability-contract.md` §2 Body conventions — *"Do not survive — avoid them: … assumptions about a specific harness's filesystem layout"*; and the newer in-repo idiom established by VHS-12/VHS-29
**Evidence:**
- `skills/spec-cycle/SKILL.md:235` (the form the spec copies): "Read `~/.claude/skills/ship-spec/states.json` (`~/.claude/` on Unix; `%USERPROFILE%\.claude\` on Windows)".
- `skills/spec-close/SKILL.md:31` (the newer form): "Read `<config-dir>/skills/ship-spec/states.json`, where `<config-dir>` is `$CLAUDE_CONFIG_DIR` when set, otherwise `~/.claude/` on Unix and `%USERPROFILE%\.claude\` on Windows (the same resolution order `sync.py` installs with…)".
- `README.md:40` confirms `sync.py --claude-dir` "overrides `$CLAUDE_CONFIG_DIR` / `~/.claude`" — so the config dir is genuinely relocatable and the spec-cycle form is the stale one.

A brand-new skill should inherit the better of two live precedents, especially one whose ticket (VHS-32) is explicitly about portable, host-agnostic authoring.

**Suggested fix:** change Design 3 Phase 0 step 3 to cite `/spec-close` Phase 0 step 4's `<config-dir>` resolution (`$CLAUDE_CONFIG_DIR` → `~/.claude/` → `%USERPROFILE%\.claude\`) as the pattern to mirror, keeping spec-cycle's `plane` default and warning text.

---

### F-4: Phase 0 reads `AGENTS.md` first — a silent divergence from every sibling skill and from the repo's own downstream-customization contract

**Severity:** P2
**Where:** spec § Design 3 Phase 0 step 1 (`:225`) — "Read `AGENTS.md` and, if present, `CLAUDE.md`"
**Convention violated:** the shipped preflight idiom, and `docs/customizing.md:3`
**Evidence:**
- `docs/customizing.md:3`: *"Project-specific rules live in your project's `CLAUDE.md` — the skills read it during preflight and apply what's there."*
- `docs/spec-workflow-reference.md:18`: *"**Read your project's CLAUDE.md** (or equivalent project-instructions file)."*
- `skills/spec-cycle/SKILL.md:61` (Phase 0 step 3): "Read `<project_root>/CLAUDE.md`." `skills/ship-spec/SKILL.md:20` (step 3): "Read `<project_root>/CLAUDE.md`." Every wiki-path and username-substitution fallback the spec says it mirrors lives in that step.
- `AGENTS.md` is *this repo's* instruction file. These skills are installed into arbitrary target projects, most of which have a `CLAUDE.md` and no `AGENTS.md`.

The brief authorizes nothing here (its Scope row for `spec-brief/SKILL.md` says only "ground against repo + wiki"), and the spec gives no rationale — this is a **silent addition (d)** that changes preflight behavior in every downstream project.

**Suggested fix:** match the sibling skills — "Read `<project_root>/CLAUDE.md` (or your harness's project-instructions file; this repo's is `AGENTS.md`)" — or keep the dual read but add a one-line rationale under Design 3 and a corresponding note that this is a deliberate departure from `docs/customizing.md`.

---

### F-5: No origin-sync preflight, though `/spec-brief` grounds against the local tree and emits a "verified against current files" Scope table

**Severity:** P2
**Where:** spec § Design 3 Phase 0 (`:223–233`), Phase 1 (`:235–244`), Phase 4 (`:265–283`)
**Convention violated:** the VHS-11 / VHS-14 origin-sync idiom, applied to every lifecycle skill that cold-reads the tree
**Evidence:**
- `skills/spec-cycle/SKILL.md:74–81` (Phase 0 step 5): *"Reviewers cold-read the local tree, so a merged-but-unpulled change is a false-positive generator that pollutes the convergence signal."* Warn-only, opt-in `git merge --ff-only`, never auto-pull.
- `skills/spec-close/SKILL.md` Phase 0 (VHS-14) carries the warn-only variant; wiki `projects/vigil-skills/state.md` VHS-14 entry: *"Reuses spec-cycle's VHS-11 origin idioms (warn-only, no auto-pull)."*
- The spec's Phase 4 emits `## Scope (verified against current files, <date>)` and Phase 1 grounds by reading files and dispatching explorations — exactly the cold-read the idiom exists to protect. A brief authored on a stale tree seeds every downstream review round with the false positives VHS-11 was filed to remove.

**Suggested fix:** add a Phase 0 step — "Origin sync check (warn-only): same shape as `/spec-close` Phase 0 (detect `origin`, ref-only `git fetch`, `git rev-list --count HEAD..origin/<cmp>`, non-blocking behind-N warn, every git failure degrades to a `skipped` token)" — and add its token to the preflight summary line. If it is deliberately omitted, say so in § Out of scope with the reason.

---

### F-6: `user_invocable: false` is presented as the portable enforcement of D9, but the contract classes it as informational on the one non-Claude-Code target

**Severity:** P2
**Where:** spec § Design 1 frontmatter note (`:132`) — "`user_invocable: false` is the repo's portable 'model-invocable only' flag (contract §2: the intent travels; Claude Code maps it to no slash command)"; § Done when 1 (`:385`); checklist 5 (`:365`)
**Convention violated:** `docs/portability-contract.md` §2 frontmatter table
**Evidence:** the contract's own row reads: *"`user_invocable` | **Portable (mapped)** | The intent 'a user can invoke this directly' is portable. Claude Code → slash command; **Hermes → every skill is already a slash command, so the flag is informational there.**"* On Hermes, `grilling` becomes `/grilling` regardless. No shipped skill in this repo uses `user_invocable: false` — all seven (`bloat-check`, `hermes-kanban-awareness`, `review-pr`, `session-handoff`, `ship-spec`, `spec-close`, `spec-cycle`, `talaria`) declare `true`, so this is the repo's first use of the value and its Claude Code behavior is unverified here.

The design does not break — but D9 ("never auto-invoked") is currently resting on a frontmatter flag the contract says one target ignores.

**Suggested fix:** in Design 1, restate the claim honestly — "`user_invocable: false` declares intent; Claude Code maps it to no slash command, Hermes treats it as informational (contract §2), so the operative guarantee is the body's own 'invoked only by /grill-me, /spec-brief, or 2f-i; never fired unprompted' sentence, not the flag." Add a checklist item verifying `grilling` carries that sentence in its body, and confirm during the dry run that `/grilling` does not appear as a Claude Code slash command after `sync.py install`.

---

### F-7: `grilling` and `grill-me` descriptions compete for the same natural-language triggers, with no disambiguation

**Severity:** P2
**Where:** spec § Design 1 frontmatter `description` (`:124`); § Design 2 frontmatter `description` (`:190`)
**Convention violated:** `docs/portability-contract.md` §2 — `description` "drives progressive disclosure on both Claude Code and Hermes … Must be self-contained and intent-rich"
**Evidence:** `grilling`'s description ends "…**or when the user explicitly asks to be grilled on a plan** — never fired unprompted." `grill-me`'s reads "…Use when the user says **'grill me', 'stress-test this', 'poke holes in this plan'**." Both are model-invocable (nothing in either frontmatter disables model invocation — the spec explicitly declines `disable-model-invocation` at `:132`), so "grill me on this plan" matches both. If the model selects `grilling` directly, the caller-supplied `seed` / `altitude` / `round_cap` / `question_cap` / `facts_policy` inputs that Design 1.1 requires are unspecified, and the S2 confirm and hand-off mapping that `grill-me` owns never run.

**Suggested fix:** strip the direct-user trigger from `grilling`'s description — it should name only its three programmatic callers plus "not a user-facing entry point; users invoke `/grill-me`" — and leave the trigger phrases solely to `grill-me`. Add a checklist item asserting `grilling`'s description contains no user-phrase trigger.

---

### F-8: `--rounds 0` is both a usage error and a valid `--no-grill` alias in the same spec

**Severity:** P2
**Where:** spec § Design 3 Invocation (`:221`) vs § Design 3 Failure modes (`:301`)
**Convention violated:** internal consistency; the argument-validation idiom of `skills/spec-close/SKILL.md` (a single, unambiguous usage halt)
**Evidence:** `:221` — "`--rounds` / `--questions` accept **positive integers**; defaults 3 / 7… Anything else → halt: `Usage: /spec-brief <TICKET-ID> [--no-grill] [--rounds N] [--questions N]`". `:301` — "`--rounds 0` → treated as `--no-grill` with a warning." Zero is not a positive integer; an implementer reading Invocation halts, one reading Failure modes proceeds. (The correctness lens likely raises this too — merge if so.)

**Suggested fix:** pick one. Recommended: keep the Failure-modes behavior and amend the Invocation line to "`--rounds` accepts non-negative integers (`0` ≡ `--no-grill`, with a warning); `--questions` accepts positive integers." Also state what `--questions 0` does.

---

### F-9: S6–S8 are labelled as pins on "questions the brief left open," but the brief left none of the three open

**Severity:** P3
**Where:** spec § Decisions preamble (`:29`)
**Convention violated:** the drift-check classification this repo's own reviewer contract depends on (`agents/spec-reviewer-conventions.md` — authorized-by-brief / authorized-by-ticket / spec-addition-with-rationale / silent-addition)
**Evidence:** the preamble reads "S1–S8 are spec-author pins on the questions the brief left open ('spec author pins this')." The brief's `## Risks / decisions` explicitly defers exactly five: Risk 1 → S1, Risk 3 → S3, Risk 2 → S4, Risk 4 → S2, Risk 5 → S5. **S6** (`grill-me` mirrors `requires:`), **S7** (defer / re-ask rule), and **S8** (one grill per halt) appear nowhere in the brief or the Plane ticket. Each carries explicit rationale, so all three are legitimately category (c) *spec-addition-with-rationale* — but the blanket label presents them as (a), which is exactly what the Phase 3 drift check is supposed to catch.

**Suggested fix:** split the preamble — "S1–S5 pin the five forks the brief deferred ('spec author pins this'). S6–S8 are spec-level additions with rationale, authorized by neither brief nor ticket: <one clause each>." No design change.

---

### F-10: The `·`-separated inline menu is a new prompt idiom, and the spec renders the same prompt two different ways

**Severity:** P3
**Where:** spec § S2 (`:81`); § Design 3 Phase 0 step 2 (`:226`) vs § Design 3 Phase 3 (`:250–259`)
**Convention violated:** the repo's halt/menu shape
**Evidence:** every shipped interactive halt is a fenced block, one option per line, followed by "Wait for the user's response." — `skills/spec-cycle/SKILL.md:63–68` (upstream staleness), `:186–189` (origin sync), `:479–484` (2f halt); `skills/spec-close/SKILL.md:55` uses inline `1. Partial-close  2. Abort` only inside a table cell. The spec's Phase 0 step 2 introduces `Brief already exists at <path>. 1. Overwrite … · 2. Abort` and S2 introduces `Write the brief? 1. Write · 2. Revise an answer · 3. Abort`, while Phase 3 renders that *same* prompt as a multi-line fenced block. Two renderings of one prompt in one spec; the implementer must guess which ships.

**Suggested fix:** render both halts as fenced multi-line blocks with "Wait for the user's response." and mark S2's inline form as shorthand for the Phase 3 block, not a second rendering.

---

### F-11: `AGENTS.md` anchor `:23–31` overshoots the section by two lines

**Severity:** P4
**Where:** spec § Scope table (`:21`), § References (`:436`)
**Evidence:** `AGENTS.md:23` is "Three skills form the spec lifecycle…"; `:29` is item 3 (`/spec-close`); `:30` is blank; `:31` is the `### Parallel review agents` heading — outside the section and in the spec's own "explicitly untouched" intent. (The brief's `:21–31` is likewise loose.)

**Suggested fix:** narrow both anchors to `AGENTS.md:23–29`.

---

### F-12: The proposed README Requirements line reads as if `/spec-brief` depends on Python

**Severity:** P4
**Where:** spec § Design 5 README edit (`:346`) — "§ Requirements: 'For `/spec-brief`: nothing beyond Python — it reads the ticket through Plane / shared memory when present and degrades to conversation when not.'"
**Evidence:** `README.md:56–59` — the Python bullet is scoped to `sync.py` ("**Python 3.8+** for `sync.py`"), and the per-skill bullets name only *extra* requirements ("For `/spec-cycle` and `/ship-spec`: a Plane.so workspace…"). `/spec-brief` is prompt-only and needs no Python; "nothing beyond Python" implies an interpreter dependency it does not have.

**Suggested fix:** "For `/spec-brief`: no external services required — it reads the ticket through Plane / shared memory when present and degrades to conversation when not."

---

## Notes on the axes that came back clean

- **Premature abstraction:** not a finding. `grilling` has three real callsites (`/grill-me`, `/spec-brief`, 2f-i) — N=3, the threshold at which extraction earns its place, and the brief argues it explicitly (`VHS-32.brief.md:25`). The spec also correctly declines the generalization VHS-15's decision page already rejected ("a general Nth-pluggable-reviewer registry / plugin framework").
- **Contradicts a prior decision:** none found. The spec aligns with `2026-06-14-vhs-17-requires-tolerated-not-strict-yaml` (flat `requires:`, unquoted vocabulary, one block after the scalars), `2026-06-14-vhs-18-lint-warn-only-strict-gate` (`--strict` is the automation contract; `mcp__*`-only detection with the gap accepted as Risk 8 rather than papered over), and the VHS-28 clean-room posture. D9's "never auto-invoked" is directly aligned with `docs/compound-engineering-evaluation.md:85`, which names CE's auto-invoke ethos as counter to this repo's human-gated posture.
- **Attribution:** the in-body "Origin" line (D10, Design 1.2) is a spec-level addition the brief didn't ask for, but it has precedent — `skills/bloat-check/SKILL.md:19` ("inspired by ponytail's lazy-review format"). Not a finding.
- **Lint claims verified:** `python lint.py` → `lint: 0 error(s), 2 warning(s)`, both `missing-requires` on `review-pr` and `ship-spec`. The spec's checklist item 1 is accurate.
- **Line anchors verified:** 2f at `skills/spec-cycle/SKILL.md:466–485`, 2g at `:487`, states.json at `:235`, Tool-use notes at `:570`, Failure modes at `:578`; `skills/spec-close/SKILL.md:312`/`:339` do archive `<TICKET-ID>.reviews/` wholesale, and `:340` ("any other companion `<TICKET-ID>.<rest>`") covers the `VHS-32.test-output.txt` artifact. All correct as cited — the spec is unusually well-anchored, and the `.test-output.txt` path explicitly closes the VHS-29 drift the wiki recorded.

## Summary
P0: 1 | P1: 0 | P2: 7 | P3: 2 | P4: 2

STATUS: RED P0=1 P1=0 P2=7 P3=2 P4=2
