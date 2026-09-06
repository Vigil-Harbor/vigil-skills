# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Docs can't satisfy four-stage lifecycle | CLOSED | Scope rows spec:22–23 + Scope note spec:27; Design 5 spec:424–429 adds `## Skill 3: spec-close` + README `/spec-close` bullet; checklist 8 spec:452 asserts `grep -c 'spec-close'` ≥ 1 in both (both are 0 today — verified) |
| correctness | F-2 (P1) | D8 seed excludes scalability | CLOSED | D8 spec:69 restated as "every remaining P0/P1 … on disk"; halt-block scalability line spec:381; rationale spec:393 |
| correctness | F-3 (P1) | `--rounds 0` contradictory | CLOSED | spec:252 pins 1–10 / 1–15, "there is no `0` alias"; Failure modes spec:369 no longer mentions it |
| correctness | F-4 (P2) | "read-only by construction" over-claims `Explore` | CLOSED | Honesty note spec:37; D2 sentence spec:43 ("make no mutations of any kind"); Risks 10 spec:512 |
| correctness | F-5 (P2) | `user_invocable: false` asserted as enforcement | CLOSED | D9 spec:73 ("advisory"); spec:148; Risks 11 spec:513; checklist 10 spec:454 |
| correctness | F-6 (P2) | Tool-use notes as bold prose vs heading | CLOSED | spec:355 "(A real `## Tool-use notes` heading … matching `spec-cycle:570`)"; Design 6 spec:434 cites `lint.py:57,216–217` — verified, exemption is keyed on `cur_heading` |
| correctness | F-7 (P2) | `facts_policy` dead parameter | CLOSED | Removed from Design 1.1 spec:152–156; removal stated in S5 spec:103 |
| correctness | F-8 (P2) | Three stale line anchors | CLOSED | References spec:518–531 re-verified against disk: `spec-cycle:466–485/570/578`, `spec-close:31/37–42/339–340`, `ship-spec:20/197/241`, `portability-contract:34/65/78/107–119/129`, `lint.py:24–33/45–48/57/216–217`, `VHS-20/spec.md:153`, `bloat-check:19`, `customizing.md:3` — all correct |
| correctness | F-9 (P2) | Dry-run transcripts unproducible | CLOSED | Test plan Procedure spec:457 (authoring dry-run, `ZZZ-1`, manual PR-body link) |
| correctness | F-10 (P2) | `subagents: true` forecloses S5 degradation | CLOSED (recorded, not fixed — as suggested) | S5 "Contract limitation" spec:105; Risks 9 spec:511 |
| correctness | F-11 (P3) | Explicit non-factor scale discarded | CLOSED | Phase 4 Scale emission spec:338 (`**Factor:** no`) |
| correctness | F-12 (P3) | Under-specified argument/confirm branches | CLOSED | spec:252–254; Phase 3 spec:302–309 |
| edge-cases | F-1 (P0) | Same root as correctness F-1 | CLOSED | As above |
| edge-cases | F-2 (P1) | Empty seed → hollow brief | CLOSED | S9 spec:125–127; Phase 0 5c spec:279; Phase 1 spec:287; Run C spec:461 |
| edge-cases | F-3 (P1) | Exploration hang/crash stalls interview | CLOSED | Failed-dispatch rule spec:182 (error / empty / no-fact / reported timeout → `ℹ️` next round, "never blocks a round"); Phase 1 step 4 spec:290; Failure modes spec:367. Residual: a host that reports no timeout can still hang — not expressible in prompt text, and outside this lens |
| edge-cases | F-4 (P1) | Fact requests uncapped | CLOSED | S5 spec:103; D6 spec:61; 1.5 dispatch cap spec:182 |
| edge-cases | F-5 (P1) | Revise: no invalidation / budget / addressing | CLOSED | S7 spec:117; monotonic numbering S1 spec:81; Phase 3 spec:305 + `--no-grill` variant spec:309 |
| edge-cases | F-6 (P1) | Overwrite guard + non-atomic write | CLOSED | Phase 0 step 2 spec:259–273 (brief/spec/reviews + git-status column, fenced halt); Phase 4 spec:331. *Temp-file naming raises a new P2 — see F-2 below* |
| edge-cases | F-7 (P1) | Scale factor without target | CLOSED | Phase 4 spec:335–339, three-state rule anchored to `AGENTS.md:95` (verified) |
| edge-cases | F-8 (P1) | Host cannot invoke nested skill | CLOSED | spec:225, :296, :398; Design 6 spec:436; Risks 9 spec:511 |
| edge-cases | F-9 (P2) | Flag value / `--no-grill` interaction | CLOSED | spec:252–254 |
| edge-cases | F-10 (P2) | 2f-i missing/unparseable report, synthetic P0 | CLOSED | Design 4 step 1 spec:397 "Not grillable" |
| edge-cases | F-11 (P2) | `grill.md` overwritten | CLOSED | S8 spec:123; Design 4 step 3 spec:399 |
| edge-cases | F-12 (P2) | `--no-grill` derivation unruled | CLOSED | Phase 3 spec:309 |
| edge-cases | F-13 (P2) | `defer` expands frontier unboundedly | CLOSED | S7 rolled-up item spec:114; by-construction bound spec:204 |
| edge-cases | F-14 (P2) | `subagents: true` hard-fails | CLOSED (recorded) | spec:105, :511 |
| edge-cases | F-15 (P2) | Invalid / free-form answers, `stop` in flight | CLOSED | S7 spec:116; 1.7 spec:186 |
| edge-cases | F-16 (P3) | `user_invocable: false` unprecedented | CLOSED | Risks 11 spec:513 |
| conventions | F-1 (P0) | Same root as correctness F-1 | CLOSED | As above |
| conventions | F-2 (P2) | Halt block hardcodes three lenses | CLOSED | spec:381 + spec:393; aligns with wiki `2026-06-16-vhs-15-optional-scalability-lens.md` § Consequences |
| conventions | F-3 (P2) | Stale `~/.claude/` states.json path | CLOSED | Phase 0 step 3 spec:274 now cites `<config-dir>` per `skills/spec-close/SKILL.md:31` — verified that line carries exactly the `$CLAUDE_CONFIG_DIR` → `~/.claude/` → `%USERPROFILE%\.claude\` order |
| conventions | F-4 (P2) | `AGENTS.md`-first project-instructions read | CLOSED | Phase 0 step 1 spec:258 — "Read `<project_root>/CLAUDE.md` (or your harness's project-instructions file; in this repo that is `AGENTS.md`…)", matching `spec-cycle:61` / `docs/customizing.md:3` |
| conventions | F-5 (P2) | No origin-sync preflight | CLOSED | Phase 0 step 4 spec:275, warn-only per `spec-close:37–42`; fast-forward offer fenced out at spec:499 |
| conventions | F-6 (P2) | `user_invocable: false` presented as enforcement | CLOSED | spec:73, :148, :513 |
| conventions | F-7 (P2) | `grilling`/`grill-me` compete for triggers | CLOSED | Description spec:140 names only the three callers + redirect; checklist 5 spec:449 asserts no "grill me"/"stress-test"/"poke holes" |
| conventions | F-8 (P2) | `--rounds 0` dual behavior | CLOSED | spec:252 |
| conventions | F-9 (P3) | S6–S8 mislabeled as brief-deferred | CLOSED | Preamble spec:31 now splits D1–D10 / S1–S5 / S6–S9. *Ledger completeness raises a new P2 — see F-1 below* |
| conventions | F-10 (P3) | `·`-separated inline menu, two renderings | CLOSED | Phase 0 step 2 spec:261–271 and Phase 3 spec:302–307 are both fenced, one option per line, each followed by "Wait for the user's response."; S2 spec:85 now describes rather than re-renders |
| conventions | F-11 (P4) | `AGENTS.md:23–31` overshoots | CLOSED | spec:21 and spec:529 use `:23–29`; verified `AGENTS.md:29` is the last list item, `:31` is the next heading |
| conventions | F-12 (P4) | README Requirements implies Python dep | CLOSED | spec:429 — "no external services required" |

All 12 round-1 P0/P1s are CLOSED. No REOPENED items.

## Findings

### F-1: The spec-additions ledger claims S6–S9 is the complete set, but v2 added four more unauthorized-by-brief behaviors that live only in Design prose

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions preamble (`:31`); Design 3 Phase 0 step 2 (`:259`), step 4 (`:275`); Phase 4 (`:331`, `:335–339`)
**Convention violated:** the drift-check classification this repo's reviewer contract runs on — `agents/spec-reviewer-conventions.md` § "Silent spec additions vs the brief" (authorized-by-brief / by-ticket / spec-addition-with-rationale / silent-addition), which the Phase 3 HARD STOP checklist is built from
**Evidence:** spec:31 reads *"S6–S9 are spec-level additions with rationale, authorized by neither brief nor ticket; each is small, and each exists because a reviewer lens or the design itself needed a rule the brief did not anticipate."* That last clause describes four more v2 behaviors that are **not** in the S-ledger:

- **Origin sync check** (Phase 0 step 4, `:275`) — neither brief nor ticket authorizes it; it came from round-1 conventions F-5. Only its *fast-forward offer* is fenced (`:499`); the check itself is unclassified.
- **Output-collision halt** (Phase 0 step 2, `:259–273`) — from edge-cases F-6.
- **tmp-then-rename write** (`:331`) — from edge-cases F-6; adds a transient artifact and a Bash mutation (see F-2).
- **`## Scale` three-state emission** (`:335–339`) — anchored to `AGENTS.md:95`, but the brief's Done-when names only the eight sections.

The spec already models the right disclosure exactly once — the `/spec-close` documentation is called out as a **"Scope note on `/spec-close` documentation (spec-addition with rationale)"** at `:27`, with its own reasoning. These four got Design-section prose but no ledger entry, so a reader who trusts the preamble's enumeration will not see them at the drift check.

**Suggested fix:** one sentence at `:31` — "S6–S9 pin rules the design needed; four further reviewer-driven additions are recorded at their point of use rather than as S-items: the warn-only origin check (Phase 0 step 4), the output-collision halt (Phase 0 step 2), the tmp-then-rename write (Phase 4), and the three-state `## Scale` emission (Phase 4, per `AGENTS.md:95`)." No design change.

---

### F-2: The atomic write uses an undotted `<TICKET-ID>.brief.md.tmp` — the repo's two shipped atomic writers both dot-prefix, and the undotted name is exactly what `/spec-close`'s archive glob sweeps into `DONE/`

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 Phase 4 (`:331`); § Tool-use notes (`:357`); § "What `/spec-brief` never does" (`:353`)
**Convention violated:** the repo's established atomic-write shape, and `/spec-close`'s archive contract
**Evidence:** both shipped atomic writers dot-prefix, and one of them says why in a docstring:

`skills/spec-close/scripts/prepend_log_entry.py:370–372`
> The dot prefix is load-bearing, not cosmetic: the wiki's `.gitignore` carries `.*.tmp`, and SKILL.md tells the operator to commit the wiki with `git add -A`, so an undotted leak would be staged and committed.

`skills/session-handoff/scripts/create_handoff.py:340–341` and `prepend_log_entry.py:374–375` both use `tempfile.mkstemp(prefix=".<skill>.", suffix=".md.tmp", dir=...)`. `skills/session-handoff/SKILL.md:72` further instructs the reader to **ignore** `*.tmp` — "abandoned name reservations, not documents."

Three consequences of the undotted plain sibling:

1. `vigil-skills/.gitignore` (and, by construction, a target project's) carries no `*.tmp` entry — an abandoned `VHS-32.brief.md.tmp` in `docs/specs/TODO/` is a tracked-candidate file, the exact leak the docstring above exists to prevent.
2. `skills/spec-close/SKILL.md:340` archives *"any other companion `<TICKET-ID>.<rest>` → `<rest>`"*. A leftover matches, so a truncated temp lands permanently at `DONE/<TICKET-ID>/brief.md.tmp` — and step `:343`'s "skip if the source no longer exists" makes it re-runnable, not detected.
3. `:353` says `/spec-brief` never writes "anything other than the one brief file (and its transient `.tmp`)", but § Tool-use notes `:357` describes its Bash use as *"all read-only or ref-only"* — the rename is neither. The repo's idiom is to name the one mutation explicitly: `skills/spec-cycle/SKILL.md:573` — *"the lone git-level mutation of existing tracked files in this skill — `git merge --ff-only origin/<branch>`, run only after explicit user confirmation."*

**Suggested fix:** name the temp `.<TICKET-ID>.brief.md.tmp` (dot-prefixed, citing `prepend_log_entry.py:370–372` as the precedent), state that a stray dot-file is ignorable and must not be committed, and amend § Tool-use notes to read "…all read-only or ref-only, plus the single `mv`/rename of the brief's dot-prefixed temp onto its target — the skill's lone filesystem mutation outside the brief."

---

### F-3: `grilling/` and `grill-me/` take the exact directory names of the upstream skills they clean-room, so `sync.py install` silently overwrites a separately-installed third-party copy

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope table (`:16–17`); § D10 (`:75–77`); § Design 6 (`:437`) — "`sync.py` needs no change: three new `skills/<name>/SKILL.md` directories are inside the mirrored `skills/` subtree"
**Convention violated:** `README.md:30`'s preservation promise, and the VHS-28 supersession idiom recorded in `AGENTS.md` § "Superseded vendor skills"
**Evidence:**

- `sync.py:96` / `:146` — install is a bare `shutil.copy2(src, dst)` at the matching relative path. A repo `skills/grilling/SKILL.md` unconditionally overwrites `<config-dir>/skills/grilling/SKILL.md`, with no `--prune` involved and no operator step.
- `README.md:30`: *"Files in those directories that aren't in this repo (e.g., third-party skills installed separately) are preserved by default."* A **same-named** third-party skill is not preserved — it is clobbered, and the README's promise reads as if it would be.
- The upstream this spec clean-rooms ships at exactly these names: `docs/specs/TODO/VHS-32.spec.md:531` — *"`mattpocock/skills` `skills/productivity/grilling/SKILL.md`, `skills/productivity/grill-me/SKILL.md`"*. Any operator who installed the upstream (the population most likely to want this feature) collides.
- The repo has a recorded posture for precisely this: `AGENTS.md` § "Superseded vendor skills" — VHS-28 replaced a vendor skill under a **different** name (`session-handoff`, not `agentcraft-handoff`), with two explicit warnings and *"that is an operator step."* Wiki `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md` carries the same rule. VHS-32 supersedes by name collision and says nothing.

No live collision on this machine (`~/.claude/skills/` holds neither directory today), so nothing breaks here — but the repo is public, and this is a downstream-user data-loss path the repo already has a documented posture against.

**Suggested fix:** cheapest — add one line to Design 6 and one bullet to `AGENTS.md` § "Superseded vendor skills" (or a note beside `README.md:30`): "`grilling` / `grill-me` share directory names with `mattpocock/skills`. `sync.py install` overwrites a separately-installed upstream copy at those paths; the clean-room rewrite is intended to supersede it, and an operator who wants both must rename one." Add a checklist row asserting the note ships. If overwriting is *not* intended, rename to `vh-grilling` / a distinct stub name instead.

---

### F-4: The "Deferred (P2+)" section's header says "not folded into v2", but all three entries say "folded"

**Severity:** P4
**Where:** spec `:533–539`
**Evidence:** `:535` — *"Round-1 P2+ findings **not folded** into v2, with one-line acknowledgments"* — then `:537` "conventions F-5 (origin-sync) — **folded**", `:538` "edge-cases F-13's proposed numeric cap — **folded**", `:539` "correctness F-9's secondary note — **folded**". The section is actually a *disposition note for three P2s whose fold took a different shape than the finding proposed* — a useful thing, mislabeled.

**Suggested fix:** retitle to "Round-1 P2+ findings folded in a different shape than proposed" and drop "not folded" from the lead sentence.

---

## Notes on the axes that came back clean

- **Reuse vs duplicate.** `/spec-brief` Phase 0 restates four preflight steps that already exist in `/spec-cycle` and `/spec-close` rather than factoring them out. Not a finding: the repo has a recorded rationale for exactly this, at `skills/spec-close/scripts/prepend_log_entry.py:365–368` — *"Deliberately a second implementation: skills install independently under `<config-dir>/skills/<name>/` and share no importable module."* v2 also picked the *better* of the two live precedents for both duplicated steps (`spec-close`'s `<config-dir>` resolution and its warn-only origin shape), which is what round-1 F-3/F-5 asked for.
- **Premature abstraction.** Unchanged from round 1 — `grilling` has N=3 real callsites, and the spec still declines the general Nth-reviewer registry that `2026-06-16-vhs-15-optional-scalability-lens.md` § Consequences already rejected as premature.
- **Contradicts a prior decision.** None. Verified against `2026-06-14-vhs-17-requires-tolerated-not-strict-yaml` (all three `requires:` blocks are flat, controlled-vocabulary, after the scalars — `spec-brief`'s is byte-identical to `spec-cycle`'s), `2026-06-14-vhs-18-lint-warn-only-strict-gate` (the `mcp__*`-only gap is Risk 8, not papered over; `lint.py:24–33` confirms the limitation is documented upstream), `2026-06-16-vhs-15` (the halt-block scalability line now *closes* the residual hardcode rather than adding a new one), `2026-06-18-vhs-20-hermes-preflight-advisory` (`user_invocable` dropped by the adapter — `docs/specs/DONE/VHS-20/spec.md:153` verified, and D9 now rests on the guard sentence, matching that decision's "the adapter does not claim a runtime hard-fail it cannot deliver" posture), and `2026-08-25-vhs-29-anchor-is-a-refusal-contract` (append-only `grill.md` with a `---` separator is an audit trail, not the newest-first `log.md` contract — no conflict).
- **Lint posture re-verified live.** `python lint.py` → `lint: 0 error(s), 2 warning(s)`, both `missing-requires` on `review-pr` and `ship-spec`. Checklist item 1's expected count of 2 is accurate. `lint.py` does not validate `user_invocable` at all, so `false` is lint-neutral — consistent with Risks 11.
- **Skill-0 / Skill-3 numbering.** `docs/spec-workflow-reference.md` would read `Skill 0 → Skill 1 → Skill 2 → Skill 3`. Odd on its face, but it preserves the existing `## Skill 1` / `## Skill 2` anchors rather than renumbering them, and the Scope table states the insertion points explicitly. Acceptable trade, not a finding.
- **Portability contract anchors.** All eight cited spans verified against `docs/portability-contract.md` (`:34` `user_invocable` row, `:65` optional `?` marker, `:78` MUST-verify, `:107–119` §4, `:129` dimension 3). The two `mcp__*` mentions the spec puts in `/spec-brief`'s operative Phase 0 both carry "or the equivalent in your host" on the same line — case-2 clean under `lint.py`'s ±1-line window.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 0 | P4: 1

STATUS: GREEN
