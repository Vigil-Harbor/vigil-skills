# Brief: VHS-9 — spec-retire fast-path when wiki coverage already exists

## Problem

During the ADA-17 pilot, `/spec-retire` Phase 2b (wiki decomposition) spent multiple tool calls drafting wiki proposals from scratch — decisions, comprehension entries, state.md updates — only to discover that `/wiki-after-merge` had already created those entries at merge time. This is wasted work and token budget in every case where the merge-time skill ran successfully.

The current flow always runs the full derivation pipeline before checking for duplicates (Phase 2a greps for existing entries, but 2b still drafts proposals for anything not in the exclusion list). When wiki-after-merge has already covered everything, the entire 2b derivation is redundant.

## Goal

Add an early-exit fast-path at the top of Phase 2b that detects when wiki coverage is already complete, skipping straight to a "anything missing?" confirmation rather than re-deriving the full proposal set.

## Acceptance criteria

1. **Fast-path detection:** Before drafting any wiki proposals, Phase 2b checks whether all four wiki artifact categories already exist for the ticket:
   - `comprehension/` entry mentioning `<TICKET-ID>`
   - `decisions/` entry mentioning `<TICKET-ID>` (if the reconciliation report flagged decisions worth extracting)
   - `state.md` entry in "What's Shipped" with the ticket's evidence triple
   - `log.md` entry mentioning `<TICKET-ID>`

2. **Full-coverage exit:** If all applicable categories are present, Phase 2b prints a summary of what was found and asks: `Wiki coverage already exists (created by /wiki-after-merge). Anything missing? [skip/edit]`. On "skip", proceed directly to Phase 2c with an empty proposal set (archive-only). On "edit", fall through to the normal derivation flow.

3. **Partial-coverage handling:** If some but not all categories are present, Phase 2b reports what's covered and what's missing, then derives proposals only for the missing categories (not the full set).

4. **No behavioral change for clean-slate cases:** When no wiki entries exist for the ticket, the flow is unchanged — full derivation as today.

5. **Token savings are measurable:** In the full-coverage case, Phase 2b should complete in 1-2 tool calls (grep + user prompt) rather than the current 5-8 calls (read spec, read reconciliation, draft decisions, draft comprehension, draft state.md edit, compile).

## Secondary: gitignored-spec fallback prominence

When `docs/specs/` is gitignored and the spec file isn't tracked, the reconcile skill recovers content via `git show`. This works but the recovery path should be more visible:

6. **Fallback notice:** If Phase 0 detects the spec is untracked (`git ls-files --error-unmatch` fails), print a notice: `Spec file is untracked (gitignored). Content recovered from git history.` This makes the recovery explicit rather than silent.

## Constraints

- The fast-path check must be lightweight (file greps, not LLM analysis).
- The detection logic should tolerate minor naming variations in comprehension/decision filenames (grep for ticket ID, not exact filename match).
- Must not break partial-retire mode (which already skips 2b entirely).
- The existing duplicate-detection in Phase 2a remains — fast-path is an optimization layer above it.

## Out of scope

- Changing `/wiki-after-merge` behavior.
- Adding inter-skill communication or shared state beyond filesystem checks.
- Modifying Phase 2a duplicate detection (it still runs for the partial-coverage path).

## Context

- **Origin:** First production run of VHS-8 skills (spec-reconcile + spec-retire) on ADA-17.
- **Affected file:** `skills/spec-retire/SKILL.md` — Phase 2b section.
- **Related skills:** `/wiki-after-merge` (creates the wiki entries this fast-path detects), `/spec-reconcile` (runs before spec-retire).
- **Priority:** Low — both skills are production-ready; this is an efficiency optimization.
