# VHS-11 — spec-cycle: 4 enhancements surfaced by the PET-86 run

**Status:** Backlog · **Priority:** Medium · **Assignee:** Unassigned
**Created:** 2026-06-10 · **Plane:** VHS-11
**Origin:** Constructive feedback from running `/spec-cycle` end-to-end on PET-86 (Petasos): v1 authoring → 2 review rounds → green at round 2. The skill performed well; these are four bounded enhancements, each grounded in a specific moment in that run, ordered by value. Reviews persisted at `petasos:docs/specs/TODO/PET-86.reviews/round-{1,2}/`.

## Problem

Four gaps, each verified against `skills/spec-cycle/SKILL.md` (current main, 293 lines, read 2026-06-10):

1. **(High) No local-branch-vs-origin sync check.** Phase 0 step 4 (`:30–96`, shipped as VHS-6) checks *upstream* staleness for forks, but nothing checks whether the local default branch is behind `origin`. On PET-86, two PRs (#60/#61) were squash-merged to `origin/master` earlier in the same session without a local pull. In round 1, both the correctness and conventions reviewers flagged `petasos/console/_validation.py` as "nonexistent / fabricated precedent" — right about the local tree, wrong about the repo. Two reviewers each spent a finding (P1/P2) on a stale-tree artifact and the author burned a revision hedging a citation that was true. Reviewers cold-read from the local tree, so any merged-but-unpulled change is a false-positive generator that pollutes the convergence signal.

2. **(Medium) Post-green edits are unsanctioned.** The gate (`2d`, `:163–174`) breaks the loop the instant `total_p0p1 == 0`; P2+ findings are carried to a `## Deferred (P2+)` section (`:174`, `:181`). The skill is silent on whether post-green edits are permitted. On PET-86, round 2 went green with ~5 P2s, three of which the edge-cases reviewer explicitly tagged "worth folding in before ship-spec" — they hardened the exact failure class the ticket targeted. The author folded them in via undocumented discretion. Ambiguity sits at exactly the decision point where value is highest and risk lowest; deferring a reviewer-recommended one-line clarification to a future ticket is waste.

3. **(Medium) Brief-path resolution is brittle against real layouts.** Phase 0 step 1 (`:23`) expects `docs/specs/TODO/<TICKET-ID>.brief.md` and extracts `ticket_id` from the filename. The PET-86 brief lived at `docs/briefs/PET-86-profile-aware-deployment.md` — different directory, descriptive-suffix filename. The run worked because the steps are lenient, but spec artifacts landed in `docs/specs/TODO/` while the brief stayed in `docs/briefs/`: companions in different trees with different naming conventions. The 2b reviewer prompt also hardcodes `brief_path: docs/specs/TODO/<TICKET-ID>.brief.md` (`:144`) rather than the resolved path, and the Phase 3 brief-section parser (`:264–273`) assumes specific headers (it has a fallback bullet, but only per missing header).

4. **(Medium) No standardized per-round closure manifest in reviewer prompts.** The 2b prompt (`:142–152`) passes `spec_path/brief_path/project_root/ticket_id/namespace/round_number` — no "what changed since round N-1" block. On PET-86, the author hand-wrote a "here's what changed, confirm closed" block into each round-2 prompt and got reliable CLOSED/REOPENED verdicts. **Correction to the ticket's framing, verified against the agent files:** the three reviewer agents already self-serve closure at `round_number ≥ 2` — step 7 in each (`agents/spec-reviewer-{correctness,edge-cases,conventions}.md`) reads prior-round review files from disk and renders a required CLOSED/PARTIAL/REOPENED/NEW closure table. The gap is orchestrator-side: the agents must *infer* how each finding was addressed from a spec diff, with no author-stated intent. The round-4 closed-issues manifest (`:196–210`) is itself built by scanning those closure tables, so making them more reliable strengthens the round-4 path too.

## Why it matters

- **Convergence signal integrity.** Items 1 and 4 both protect the same thing: the trustworthiness of the review loop's gate. Stale trees inject false positives; improvised closure checking makes round-over-round verdicts operator-dependent.
- **Cheap, precedented mechanics.** Item 1 generalizes the existing VHS-6 staleness logic to the origin/local axis — same skip-silently / warn-and-prompt pattern, two git commands. Items 2–4 are prompt/flow text only.
- **Bounded blast radius.** Markdown-only edits to `skills/spec-cycle/SKILL.md` plus (for item 4 and the optional `preShipRecommended` tag in item 2) the three reviewer agent files. No new tools, no runtime state, no new dependencies. Same profile as VHS-6, VHS-7. Public repo, security-first posture: all added git operations are read-only or local-ref-only except the explicitly user-confirmed `--ff-only` update (see Risks §1).

## Scope (verified against current files, 2026-06-10)

| Location | Current behavior | Change |
|---|---|---|
| `skills/spec-cycle/SKILL.md` Phase 0, after step 4 (`:96`) | Upstream staleness check only; no origin comparison | Insert origin-sync check: `git fetch origin` (bounded timeout, non-fatal on network failure) + `git rev-list --count <branch>..origin/<branch>`. If > 0: warn, offer a `--ff-only` update before authoring; never auto-pull. Skip silently when no `origin` remote. Renumber steps 5–6 if inserted as a numbered step. |
| `skills/spec-cycle/SKILL.md` Phase 0 closing (`:101`) | Preflight summary includes upstream token | Add origin token: `origin: in-sync / behind-N (updated) / behind-N (user proceeded) / skipped` |
| `skills/spec-cycle/SKILL.md` between 2d and Phase 3 (`:172–174`, `:236`) | Loop breaks on green; all P2+ deferred; silent on post-green edits | Add explicit bounded post-green polish step: fold in P2s a reviewer tagged pre-ship-recommended; clarifications only — no behavior reversals, no new scope; no mandatory re-review; touched P2s move from `## Deferred (P2+)` to addressed with a one-line note |
| `agents/spec-reviewer-*.md` findings format | P2s are prose; intent inferred | Optional per-P2 `preShipRecommended: true|false` tag so the author isn't inferring intent from prose (spec author decides exact placement in the findings schema) |
| `skills/spec-cycle/SKILL.md` Phase 0 step 1 (`:23`) | Expects `docs/specs/TODO/<TICKET-ID>.brief.md`; ticket-id from filename | Explicitly support (a) alternate brief directories (e.g., `docs/briefs/`) and (b) descriptive-suffix filenames (`<TICKET-ID>-slug.md`) in ticket-id extraction (uppercase `[A-Z]+-[0-9]+` prefix match); state that `docs/specs/TODO/` is canonical for spec artifacts regardless of brief location |
| `skills/spec-cycle/SKILL.md` 2b prompt (`:144`) | `brief_path` hardcoded to canonical shape | Pass the *resolved* brief path from Phase 0 |
| `skills/spec-cycle/SKILL.md` 2b prompt (`:142–152`) | No round-over-round context | For rounds N > 1, mandate a closure-manifest block: round-(N-1) P0/P1 findings + one-line "how addressed" each (author-stated intent). Complements — does not replace — the agents' existing step-7 disk-read closure verification |
| `skills/spec-cycle/SKILL.md` `## Tool-use notes` (`:277–283`) | Lists `git fetch upstream` etc. | Add `git fetch origin` and the conditional `git merge-base`/`--ff-only` update (the lone working-tree mutation, user-confirmed) |
| `skills/spec-cycle/SKILL.md` `## Failure modes` (`:285–293`) | 7 bullets | Add: origin unreachable (skip, non-fatal); diverged local branch (`--ff-only` impossible — warn and proceed, never merge/rebase) |

**Preserved (NOT changed):**

- The upstream staleness check (VHS-6) — the origin check is a sibling, not a replacement.
- The green gate semantics (`total_p0p1 == 0`) and the ≤4-round loop structure.
- The round-4 FROZEN/REWRITE targeted-rewrite protocol and its closed-issues manifest (`:184–213`).
- Reviewer agents' step-7 closure verification and the required closure-table output section.
- The session-boundary HARD STOP and the Phase 3 drift-check checklist (PET-86 confirmed these work — "What worked" list in the ticket).
- `/ship-spec`, `/spec-reconcile`, `/spec-retire` — untouched.

## Decisions carried forward

1. **Never auto-pull.** The origin-sync check warns and offers a `--ff-only` update; the user confirms. If the branch has diverged (ff impossible), warn and proceed — no merge, no rebase, ever. This is the only working-tree mutation in the skill and it must remain opt-in.
2. **Origin check mirrors the VHS-6 pattern.** Skip silently when no `origin` remote; bounded-timeout fetch with non-fatal network failure; result token in the preflight summary. Generalize the existing staleness logic, don't invent a second idiom.
3. **Post-green polish is bounded and gate-preserving.** Only P2s a reviewer tagged pre-ship-recommended; clarifications only — no behavior reversals, no new scope; no mandatory re-review round. The green verdict stands; the polish step cannot reopen the loop.
4. **`docs/specs/TODO/` stays canonical for spec artifacts.** Alternate brief locations are tolerated on input, not promoted. The skill states where companions land so brief/spec co-location drift is a documented choice, not an accident.
5. **The closure manifest is author-stated intent, additive to agent self-service.** Reviewer agents keep their disk-read closure step; the manifest gives them the author's claim to verify against, making CLOSED/REOPENED verdicts consistent regardless of operator.
6. **All four items ship as one markdown-only change.** Same blast-radius class as VHS-6/VHS-7; a per-item revert is a section-level edit.

## Done when

- Phase 0 contains an origin-sync check after the upstream block: `git fetch origin` (bounded timeout, non-fatal) + `git rev-list --count <branch>..origin/<branch>`; behind-count > 0 produces a warning and an explicit user choice (ff-only update / proceed anyway); no `origin` remote → silent skip with summary token.
- The preflight summary line includes an origin token (`in-sync | behind-N (updated) | behind-N (user proceeded) | skipped`).
- A post-green polish step exists between the gate and Phase 3, with the three guardrails (reviewer-tagged P2s only; clarifications only; no re-review) stated explicitly; the `## Deferred (P2+)` language in 2d/2e cross-references it.
- Reviewer findings format supports an explicit pre-ship-recommended marker on P2s (exact mechanism per spec author), and the polish step keys off it.
- Phase 0 step 1 documents alternate brief directories and descriptive-suffix filenames; ticket-id extraction is specified for `<TICKET-ID>-slug.md`; canonical artifact location is stated.
- The 2b prompt passes the resolved `brief_path`, and for rounds N > 1 includes the mandated closure-manifest block (round-(N-1) P0/P1 findings + how addressed).
- `## Tool-use notes` and `## Failure modes` cover the new git operations and the two new failure modes (origin unreachable; diverged branch).
- `python sync.py status` shows the edits cleanly; `python sync.py push` round-trips byte-for-byte.
- A dry-run transcript (any repo with a deliberately stale local branch) shows the origin check firing, the user prompt, and the ff-only path; pinned in the spec's Test plan (doc-only spec → review-checklist Test plan, `Test command: N/A` per the VHS-7 convention).

## Out of scope

- Mirroring the origin-sync check into `/ship-spec` Phase 0 (ship-spec works in an isolated worktree created from a fresh ref; separate brief if wanted).
- Auto-pull, merge, or rebase of any kind — the skill never mutates the working tree without explicit confirmation.
- Custom remote names beyond the literal `origin` and `upstream`.
- Rewriting the reviewer agents' step-7 closure logic or the closure-table format — item 4 feeds them better input, nothing more.
- Changing the green-gate formula, severity scale, or round cap.
- A general brief-discovery search (globbing the repo for candidate briefs); only the two named layout tolerances.
- Normalizing/moving existing briefs already on disk in any repo.
- LLM classification of whether origin commits are relevant to the brief — behind-count is the only signal; relevance stays the upstream check's heuristic.

## Risks / decisions

1. **`--ff-only` update is a working-tree mutation in a skill documented as non-mutating.** Mitigation: explicit user confirmation, ff-only (no merge commits, no history rewriting), and a Tool-use-notes callout so reviewer agents don't flag it. If the user declines, reviewers may still produce stale-tree false positives — the warning at least names the cause, which is the bulk of the value.
2. **Post-green polish could become scope creep by another name.** The guardrails are prose, not mechanism; a sloppy operator can stretch "clarification." Accepted: same trust model as the rest of the skill (cf. VHS-6 Risks §7 — the skill cannot enforce careful reading).
3. **`preShipRecommended` touches three agent files.** Keeping it optional (spec author may choose a prose-tag convention instead of a schema change) bounds the edit. If skipped, the polish step falls back to "reviewer explicitly recommends folding in before ship-spec" prose detection — weaker but workable.
4. **Closure-manifest block grows prompt size each round.** Bounded: P0/P1 findings only (P2s are advisory), one line each, rounds 2–4 only. PET-86 round-2 hand-written equivalent was ~10 lines.
5. **Ticket-id extraction from descriptive-suffix filenames can mis-fire** (e.g., a brief named `PET-86-fix-MCP-33-regression.md` contains two ID-shaped tokens). Rule: anchored prefix match only (`^[A-Z]+-[0-9]+`), which resolves this case unambiguously. Spec author pins the regex.
6. **Behind-origin check on detached HEAD or non-default branches.** Spec author defines behavior: compare the *current* branch to its origin counterpart when one exists; fall back to the default branch; skip with a token on detached HEAD.

## References

- Plane: VHS-11 (created 2026-06-10, priority Medium)
- Skill: `skills/spec-cycle/SKILL.md` (293 lines, read 2026-06-10) — Phase 0 step 4 `:30–96`, gate `:163–174`, deferral `:174/:181`, round-4 manifest `:196–210`, 2b prompt `:142–152`, brief parsing `:264–273`
- Agents: `agents/spec-reviewer-{correctness,edge-cases,conventions}.md` — step 7 closure verification (round ≥ 2), required closure-table section
- Trigger run: PET-86 (Petasos) — reviews at `petasos:docs/specs/TODO/PET-86.reviews/round-{1,2}/`; stale-tree incident re `petasos/console/_validation.py` (PRs #60/#61 squash-merged to `origin/master`, local not pulled)
- Precedent: `docs/specs/TODO/VHS-6.brief.md` + spec (upstream staleness check — the pattern item 1 generalizes); VHS-7 (`N/A` test-command convention for doc-only specs)
- Wiki: `vigil-harbor-wiki/projects/vigil-skills/state.md` (VHS-6 shipped 2026-05-11, commit 19d2d98); skepticism rule in `vigil-harbor-wiki/CLAUDE.md` — the origin check mechanizes it for the local-tree-vs-repo case
