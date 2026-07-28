# VHS-16 — Cross-harness skill parity: fork CE converter, Hermes-first (epic)

**Status:** Backlog · **Priority:** High · **Assignee:** Unassigned
**Created:** 2026-06-14 · **Plane:** VHS-16 (parent of VHS-17 … VHS-23)
**Origin:** The compound-engineering evaluation (`docs/compound-engineering-evaluation.md`, merged 2026-06-14) parked the multi-harness converter as a Tier-3 watch-item: *"The multi-harness converter CLI — notable only because your MCP server already serves OpenClaw/Calvin; revisit if cross-harness skill parity ever becomes a goal."* (eval doc, "Tier 3 — watch, don't lift yet"). That goal is now active. This epic turns the watch-item into work.

> **Note on looping this epic.** VHS-16 is a parent/orientation brief, not a directly shippable unit — there is no single worktree change that "implements" it and no test that proves it green on its own. Its children **are** the loopable units. A `/spec-cycle` → `/ship-spec` loop should read this brief for shared context and the carried-forward decisions, then pick up **VHS-17** (the unblocker) and **VHS-18**. The epic's own "Done when" is satisfied by its children merging, not by a commit against VHS-16. The child items are already filed (verified in Plane 2026-06-14): VHS-17 contract, VHS-18 authoring/lint, VHS-19 converter fork, VHS-20 Hermes adapter, VHS-21 conformance suite, VHS-22 sync.py multi-harness distribution, VHS-23 validate inherited CE targets (v2).

## Goal

Make vigil-skills run on any agent harness in the fleet — Claude Code, Hermes, and (later) OpenClaw/Calvin and Codex — so a skill "just works" regardless of which harness is holding it. Model-capability parity arrived in 2026; the remaining problem is **clarity of intent** and harness-neutral packaging, not lowest-common-denominator dumbing-down.

## Context (verified 2026-06-14)

- **Canonical source format is Claude Code `SKILL.md`.** The repo already installs to `~/.claude/skills/` via `sync.py`, whose `SUBTREES = ("skills", "agents")` (`sync.py:30`) is the existing distribution spine. Today the repo ships **4 skills** (`skills/{review-pr,ship-spec,spec-close,spec-cycle}`) and **3 agents** (`agents/spec-reviewer-{correctness,edge-cases,conventions}.md`).
- **CE's converter is the reference, not the product.** EveryInc/compound-engineering-plugin (MIT) ships a Bun/TypeScript converter that re-targets Claude Code skills to Codex, Cursor, Copilot, Gemini, Windsurf, OpenClaw, and Qwen — **but not Hermes** (verified in the eval doc, "What Compound Engineering actually is"). Hermes is therefore the headline new work, not a freebie from CE.
- **Hermes already has a skills system** (wiki: `tools/hermes-agent/`, sourced 2026-05-23). Skills live in `~/.hermes/skills/` with a sync-pass + content-hash manifest (user-modified skills never overwritten), a skill loader with "discovery and progressive disclosure," distribution via **taps** (GitHub repos, no registry), **bundles** (group skills under one slash command), and a **curator** that prunes/consolidates agent-created skills. This is a SKILL-like target, which is what makes behavioral parity plausible rather than a rewrite.
- **Prior art in VHS:** VHS-7 "Cursor Compatibility with /spec-cycle." This epic generalizes that one-off into a contract-driven approach.

## Decisions carried forward

- **Canonical source = Claude Code `SKILL.md`.** Adapters are generated, never hand-maintained; the source never forks per harness.
- **Converter = fork CE's MIT converter.** Strip CE-specific skill content, keep the conversion engine, own the fork. MIT permits this (eval doc, Decision 2).
- **v1 target harness = Hermes** (no CE adapter exists). Claude Code is the source/native baseline and needs no conversion.
- **OpenClaw + Codex = inherited from CE's adapters but unvalidated → deferred to v2** (VHS-23). Gemini / Cursor / Copilot / Windsurf / Qwen = out of scope for now.
- **"Just works" contract** = intent clarity + explicit capability/tool-requirement declaration + zero harness-specific assumptions in skill bodies. Parity is judged **behaviorally**, not by string-identical output.
- **Security-first (non-negotiable).** Forking third-party code is a supply-chain surface: the fork must be vetted, dependency-pinned, and audited, and conversion must **never execute** skill content. This matches the repo's security-first posture and the Petasos pairing.
- **No regression of the evidence model.** Nothing in this epic touches the Plane/wiki evidence-triple model or the `/spec-cycle` drift-check HARD STOP (eval doc, Decision 3).

## Done when

- All child items are filed and each is independently brief/`spec-cycle`-able with its own acceptance criteria. *(Filing already done — VHS-17…23 exist in Plane as of 2026-06-14; this criterion is met.)*
- A vigil skill authored once in `SKILL.md` runs to **behavioral parity** on Claude Code (source) and Hermes (v1 target), proven by the conformance suite (VHS-21).
- The portability contract (VHS-17) and harness-agnostic authoring guidelines (VHS-18) are merged and referenced from `CLAUDE.md`.

## Out of scope

- Validating OpenClaw/Codex (deferred to VHS-23, v2) and adding Gemini/Cursor/Copilot/Windsurf/Qwen.
- Rewriting skills into a new format — the source stays `SKILL.md`.
- Any change to the Plane/wiki evidence-triple model or the `/spec-cycle` drift-check HARD STOP.
- Installing, vendoring, or running the compound-engineering plugin itself (only its converter engine is forked).

## References

- Plane: VHS-16 (epic, priority High, created 2026-06-14); children VHS-17…VHS-23 (verified present 2026-06-14).
- `docs/compound-engineering-evaluation.md` (merged 2026-06-14) — Tier-3 watch-item that seeded this epic; CE converter target list; MIT-license / parts-donor decisions.
- `sync.py:30` — `SUBTREES = ("skills", "agents")`, the distribution spine that VHS-22 extends.
- Repo skill/agent inventory: `skills/{review-pr,ship-spec,spec-close,spec-cycle}`, `agents/spec-reviewer-*.md` (read 2026-06-14).
- Wiki: `tools/hermes-agent/{architecture.md,cli-commands.md}` (Hermes skills dir, taps, bundles, curator; sourced 2026-05-23).
- Prior art: Plane VHS-7 "Cursor Compatibility with /spec-cycle."
