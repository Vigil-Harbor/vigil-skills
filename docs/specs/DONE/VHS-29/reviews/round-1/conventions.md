# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: `AGENTS.md:29` carries a sixth "append to wiki log.md" site the spec's inventory omits
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope "Files to change" / "Files to leave alone"; Done when #1
**Convention violated:** `AGENTS.md` is the canonical, tracked project doc (`CLAUDE.md` is gitignored — AGENTS.md § Conventions). Repo precedent is that a skill-behavior change reconciles the tracked docs in the same PR: VHS-15 reconciled "3-lens" → default-three across `AGENTS.md`, `README.md`, `docs/spec-workflow-reference.md`; VHS-17 shipped its pointer in `README.md` *because* `CLAUDE.md` is gitignored.
**Evidence:** `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/AGENTS.md:29` — "…archive spec artifacts from `TODO/` to `DONE/<TICKET-ID>/` (ticket prefix stripped from filenames), **and append to wiki `log.md`**." Same file, line 100, describes `/wiki-after-merge` as "It **appends** to `log.md`" — also stale, since the brief establishes that skill already prepends.
**Suggested fix:** Add `AGENTS.md` to § Scope "Files to change" with the line-29 clause reworded to "prepend an entry to the wiki's newest-first `log.md`", and either fix line 100 in the same edit or name it in § Out of scope. Extend Done-when #1 (and test case 14's grep) to cover `AGENTS.md`, not `SKILL.md` alone.

### F-2: The five-site inventory is off by one at site 5 and misses the stale `grep -F` mention at line 380
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design "`skills/spec-close/SKILL.md` — the five sites", bullet "Line 382"; § Scope line 13
**Convention violated:** The spec makes the enumerated line list load-bearing (Done-when #1 names "lines 3, 309, 343, 365, 382"), and the repo's reviewer convention is `file:line` precision (AGENTS.md § Plan & Spec Reviews).
**Evidence:** Verified against the file — lines 3, 309, 343, 365 are exact. The sentence the spec quotes for "line 382" (`Write for the reconciliation report, wiki entries, and log.md`) is at **line 381**; line 382 is the mutation-boundary bullet. Separately, `skills/spec-close/SKILL.md:380` (the Bash tool-use bullet) lists `` `grep -F` (idempotency check) `` — which D4 retires by moving the guard into the script. The spec says only that this bullet "gains the script invocation"; it never says the `grep -F` idempotency clause goes. Test case 14 greps for `append` wording, so a surviving `grep -F` claim would not be caught.
**Suggested fix:** Relabel site 5 as "lines 380–382" and state all three edits explicitly: line 380 drops `` `grep -F` (idempotency check) `` and gains the script invocation; line 381's Write-target list drops `log.md`; line 382 is unchanged in substance. Update Done-when #1's line list to match.

### F-3: The proposed `requires:` block under-declares against contract §3 and the `spec-cycle` precedent
**Severity:** P2
**Where:** spec § D8
**Convention violated:** `docs/portability-contract.md` §3 — "A skill must **declare** what it needs; a harness must not have to infer it by reading the body." The `services` vocabulary (`issue-tracker`, `shared-memory`, `?` = degrades gracefully) exists for exactly this skill's dependencies.
**Evidence:** `skills/spec-cycle/SKILL.md:5-10` — the sibling lifecycle skill and VHS-17's worked reference declares `shell / filesystem: [read, write] / network: true / subagents: true / services: [issue-tracker?, shared-memory?]`. `spec-close` uses both roles and degrades on both: `SKILL.md:378-379` names the MCP-memory search capability and plane-proxy's state-list/work-item-lookup capabilities, and § Failure modes carries "Plane ticket not in MCP memory. Warn and proceed" (optional-`?` semantics) plus the Plane-unreachable partial-or-abort gate. `SKILL.md:380` also runs `git fetch origin`, and Phase 2 uses `gh pr view` / `gh pr diff`. D8's block declares neither `services` nor `network`. This is not cosmetic: VHS-20's Hermes adapter generates its capability pre-flight *from* this block (`decisions/2026-06-18-vhs-20-hermes-preflight-advisory.md`), so an under-declared block emits a pre-flight that never mentions Plane.
**Suggested fix:** In D8, declare `services: [issue-tracker?, shared-memory?]`, and decide `network` explicitly (declare `true`, matching `spec-cycle`/`talaria`, or record why `gh`/`git fetch` under `shell` does not count). Keep `subagents` absent. Note `lint.py` validates the whole vocabulary, so the fuller block still lints clean.

### F-4: D8 invalidates the tracked missing-`requires:` backlog sentence in `docs/authoring-portable-skills.md`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D8 ("clears the standing WARN as a side effect")
**Convention violated:** That sentence is the *tracked backlog item* for promoting the lint to a hard gate — it enumerates the three skills by name, so it is a checklist, not prose.
**Evidence:** `docs/authoring-portable-skills.md:41` — "Today three shipped skills (`ship-spec`, `spec-close`, `review-pr`) have no `requires:` block… ***This is the tracked backlog item.***" After D8 lands, two remain. (Good news for D8: I checked `tests/test_lint.py` — it pins only the 8-skill inventory count and zero-ERROR, never the WARN set, so adding the block breaks no test.)
**Suggested fix:** Add `docs/authoring-portable-skills.md` to § Scope "Files to change" with line 41 updated to name `ship-spec` and `review-pr` only.

### F-5: How `SKILL.md` names the script path is unspecified — and the repo's precedent is not a repo-relative path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design "Line 343 (Phase 5 step 4)" — "names the script, and shows the invocation"; § D5 CLI surface
**Convention violated:** `skills/session-handoff/SKILL.md` (VHS-28, the shape precedent this spec cites) refers to its scripts by **bare name**, leaving resolution to the harness — consistent with contract §4's intent-over-implementation and §1's "installed to `~/.claude/skills/`".
**Evidence:** `skills/session-handoff/SKILL.md:23-24,44,50` — "`scripts/create_handoff.py` — scaffold a document…", "Run `create_handoff.py [slug] …`", "Run `validate_handoff.py <file>`". No absolute or repo-relative path anywhere. This matters more for `spec-close` than it did for `session-handoff`: `spec-close` runs with cwd = the **target project repo** (`project_root`), which is normally not `vigil-skills`, so an invocation written as `python skills/spec-close/scripts/prepend_log_entry.py …` resolves only when closing a vigil-skills spec — i.e. it would work for VHS-29's own close run and silently fail everywhere else.
**Suggested fix:** In § Design site 3, pin the reference form: bare `prepend_log_entry.py` (or `scripts/prepend_log_entry.py`) resolved relative to the skill directory, matching `session-handoff`, and add one sentence stating that the path is never written relative to `project_root`.

### F-6: `--dry-run` is unused surface, against the recorded "only deterministic gates earn a script" trimming
**Severity:** P2
**Where:** spec § D5 ("`--dry-run` … the skill does not use it"); § Test plan case 12
**Convention violated:** VHS-28's shipped principle that this spec itself cites in D1 — surface with no caller becomes a prompt-driven step, not shipped code.
**Evidence:** `docs/specs/DONE/VHS-28/brief.md:32` — "**Two scripts, not four.** `list_handoffs.py` and `check_staleness.py` become prompt-driven steps in the body… Only the deterministic gates — scaffold generation and the secret/completeness validator — earn a script." The wiki records the same rule as shipped fact: `projects/vigil-skills/filemap.md:147` — "Two scripts, not the vendor's four… since only the deterministic gates earn a script." `--dry-run` has zero callers by the spec's own admission and costs a test case.
**Suggested fix:** Drop `--dry-run` and test case 12, or add one sentence in D5 recording it as deliberate operator surface with the VHS-28 principle addressed head-on (an operator can already get the same answer by running the script against a copy).

### F-7: Spec-level additions the brief and ticket do not authorize — flagged for the drift check
**Severity:** P3
**Where:** spec § D4, § D8, § Test plan case 14
**Convention violated:** None — these are (c)-class additions carrying rationale. Recorded so the human drift-check sees them rather than discovering them in the diff.
**Evidence:** (1) **D8's `requires:` block** — neither the brief nor the Plane ticket asks for it; the brief's only lint clause is "`python lint.py` must stay clean for `spec-close`", and lint is already clean today (verified: `lint: 0 error(s), 1 warning(s)`, exit 0). The spec does flag it as included-because-D1, and it matches a tracked backlog item (F-4), so this is authorized-by-rationale, not silent. (2) **D4's exit-2 guard/entry substring tripwire** — a new failure mode not in the brief's §3 ("unchanged in substance"), justified inline. (3) **Test case 14's append-wording allowlist** — a new standing tripwire on `SKILL.md` prose beyond the brief's four test cases. All three are fine; none is a (d)-class silent addition.
**Suggested fix:** No spec edit required. Carry these three into the `/spec-cycle` Phase 3 drift-check list.

### F-8: `python lint.py --strict <file>` cannot enforce Done-when #5's "zero WARN"
**Severity:** P3
**Where:** spec § Test command line 230; § Test plan case 13; Done when #5
**Convention violated:** The lint's documented exit contract, restated in the wiki filemap.
**Evidence:** `lint.py:17` — "`python lint.py --strict` -> exits 1 if any ERROR (**WARNs never affect exit**)"; `projects/vigil-skills/filemap.md:163` repeats it. So the `--strict` line in § Test command passes whether or not D8 lands; only unittest case 13 actually pins "zero WARN". (Done-when #5's own wording — "no ERROR" — is correct; the gap is between it and test case 13's stronger claim.)
**Suggested fix:** In test case 13, state that the zero-WARN assertion is made by the unittest via `lint.lint_path()` (the shape `tests/test_lint.py` already uses), and that the `--strict` command line is an ERROR gate only.

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 2 | P4: 0

STATUS: GREEN
