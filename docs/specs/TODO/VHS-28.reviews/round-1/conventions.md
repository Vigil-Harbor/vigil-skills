# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: D4's "one module-level source" has no home in the file inventory — and its own bullets contradict it
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-28.spec.md:86` vs `:16-20`, `:197`, `:203`, `:214`
**Convention violated:** Single-source-of-truth (this review's reuse-vs-duplicate axis); the brief's "must agree **by construction**" (`VHS-28.brief.md:43`); the spec's own D2 two-script fence.
**Evidence:** Line 86 states "Both scripts import their section vocabulary from **one module-level source**." The bullets directly beneath it then describe two: line 197 puts the ordered section table in `create_handoff.py` ("the single source D4 pins"), and line 203 puts `REQUIRED_SECTIONS` / `RECOMMENDED_SECTIONS` in `validate_handoff.py` ("module-level"). The § New files table (lines 16-20) names no shared module, and line 214 says explicitly: "scripts are loaded via an `importlib` `load_script` helper because `skills/*/scripts/` is not an importable package" — so a cross-script import has no stated mechanism either. An implementer following D4's lead sentence cannot; an implementer following the Design section produces exactly the duplication D4 forbids, and "by construction" quietly degrades to "by test."
**Suggested fix:** Pick one and say which. (a) Add `skills/session-handoff/scripts/_sections.py` to the New files table, state the import mechanism both scripts use, and clarify that D2's "two scripts" fence counts executable entry points, not modules. Or (b) drop "import … from one module-level source" from line 86, state that the two vocabularies are independent and tied only by the round-trip test (test-plan item 2), and downgrade D4's heading from "agree by construction" to "agree, pinned by a round-trip test." Option (b) still satisfies the brief, which operationalizes "by construction" as exactly that round-trip check — but the spec should not claim both.

### F-2: The pytest gate contradicts the repo's recorded stdlib-only test convention
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `VHS-28.spec.md:234`, `:237`
**Convention violated:** `skills/talaria/SKILL.md:126`; `AGENTS.md` § What this repo is.
**Evidence:** `skills/talaria/SKILL.md:126` states verbatim: *"Run from the vigil-skills repo root. Use stdlib unittest; no pytest/node gate is required."* `AGENTS.md`: *"no dependencies beyond Python 3.8+ stdlib."* `tests/test_lint.py` docstring: *"Stdlib unittest. Run directly: `python tests/test_lint.py`."* The spec's third gate command is `python -m pytest tests/ -q`, and line 237's "`44 passed, 8 subtests passed`" is pytest-subtests output. I ran both against the current tree: pytest gives `44 passed, 8 subtests passed`; `python -m unittest discover -s tests -p 'test_*.py'` gives `Ran 44 tests … OK` — identical coverage, zero non-stdlib dependency.
**Suggested fix:** Replace line 234 with `python -m unittest discover -s tests -p 'test_*.py' -v`, and restate line 237's baseline as "currently 44 tests, green."

### F-3: D5's harness-specific example carries an imperative and skips the repo's canonical case-2 tag
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `VHS-28.spec.md:99-103` (esp. line 102)
**Convention violated:** `docs/portability-contract.md` §4 case 2 and case 3; §2 body conventions; `docs/authoring-portable-skills.md` habit 4.
**Evidence:** Line 102 reads: *"**Example (notes heading, harness-specific):** Claude Code stores them at `~/.claude/projects/**/<session-id>.jsonl`; **read the tail**."* Two problems. First, §4 case 3 says a notes heading *"raises a presumption of non-operativeness; it does not override an operative imperative placed there"* — "read the tail" is an imperative verb, which is the laundering the contract names explicitly. Second, D5 borrows §4's notes-heading exemption to cover a **filesystem-layout** assumption, but that exemption is written for tool names; §2's prohibition — *"assumptions about a specific harness's filesystem layout or affordances beyond what `requires` declares"* — has no notes-heading carve-out. The repo's shipped, canonical construct is the §4 case-2 tag, which `lint.py:52` matches literally (`_CASE2_TAG = "or the equivalent"`). Note `lint.py` flags only `mcp__*` identifiers, so it will not catch this — Done-when #1's "zero errors, zero warnings" claim still holds. This is contract conformance the lint cannot see.
**Suggested fix:** Recast line 102 in the shipped case-2 shape and strip the imperative: *"(e.g. Claude Code keeps session transcripts under `~/.claude/projects/**/<session-id>.jsonl`, or the equivalent in your host's session store)"*, folded into step 1's neutral imperative. Leave steps 1 and 3 as the only executed instructions.

### F-4: Exit code `2` is overloaded — BLOCKED and operator error collide, defeating D6's own rationale
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `VHS-28.spec.md:118-121` (verdict table) vs `:206`
**Convention violated:** D6's stated contract; wiki `decisions/2026-06-14-vhs-18-lint-warn-only-strict-gate.md`.
**Evidence:** The verdict table assigns `2` to `BLOCKED` (secret matched), and line 121 justifies the scheme: *"Distinct exit codes let a caller tell 'unfinished' from 'dangerous.'"* Line 206 then assigns `2` to *"Missing file"* and *"Unreadable/undecodable file"* as well. A caller receiving `2` cannot distinguish a planted credential from a typo'd path — the exact discrimination D6 was built to provide. Separately, the repo's only existing gate script defaults to exit 0 and gates only under `--strict`; the VHS-18 decision states *"The exit-code contract lives only in `--strict`; automation must call `--strict`, not parse default output."* D6 gates by default without acknowledging the divergence.
**Suggested fix:** Give operator/usage errors their own code (`3`), leaving `0`/`1`/`2` as READY/NEEDS WORK/BLOCKED. Add one sentence to D6 naming the deliberate divergence from `lint.py`'s warn-only default and why it's right here (`lint.py` is warn-only because of a documented `missing-requires` migration backlog; `validate_handoff.py` is greenfield with nothing to grandfather, so it gates on first run).

### F-5: The brief's third open question — the name — is silently unresolved
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `VHS-28.brief.md:88` vs `VHS-28.spec.md` § Decisions (no item covers it)
**Convention violated:** Silent-addition axis: D5 (line 96) and D6 (line 110) each open "Resolves the brief's open question"; the third gets no such treatment.
**Evidence:** Brief line 88 asks to confirm `session-handoff` *"does not collide with a future harness's built-in and that its `description` fires on the same natural phrasings the vendor skill claimed."* The description at spec lines 163-168 does carry all five phrasings, so half the question is answered implicitly — but the collision half is never addressed, and it is live rather than hypothetical: `~/.claude/skills/` holds `agentcraft-handoff` today, and D9 line 148 concedes both may coexist after a vendor restore ("Two skills would then advertise overlapping triggers, and the model picks by description match").
**Suggested fix:** Add two sentences — either a short D-item or a paragraph in D9 — recording the name choice, that the description deliberately claims the vendor's trigger phrasings, and what the tie-break is during coexistence.

### F-6: D8 hardcodes `.claude/handoffs/` while D5 goes to lengths to avoid `~/.claude/projects/` — asymmetry unstated
**Severity:** P3
**Where:** `VHS-28.spec.md:131-135`, `:194` vs `:95-107`
**Convention violated:** `docs/portability-contract.md` §2 ("assumptions about a specific harness's filesystem layout"); `docs/authoring-portable-skills.md` habit 4 ("No hardcoded paths").
**Evidence:** D5 spends an entire decision keeping one Claude-Code path non-operative. D8 makes another Claude-Code-named path (`.claude/handoffs/`) the operative storage location, and line 194 resolves `--continues-from` against it — with no mention of §2. Also, line 135's *"`.claude/` is gitignored in this repo"* is true of `vigil-skills` (verified in `.gitignore`) but the skill writes into whatever repo it runs in, where that may not hold.
**Suggested fix:** One sentence in D8: the path is project-local working state rather than harness config, is carried unchanged for continuity with existing documents (brief line 61), and a harness needing to relocate it does so via a `--project-path`-shaped override, not a fork. Scope line 135's gitignore claim to this repo explicitly.

### F-7: The AGENTS.md § File layout row departs from how the last three skills shipped
**Severity:** P3
**Where:** `VHS-28.spec.md:26`
**Convention violated:** Established practice for adding a skill to this repo.
**Evidence:** `git log --diff-filter=A` shows `a0ad847` (talaria), `386dc6c` (bloat-check), `8946f58` (hermes-kanban-awareness) each added a skill without touching `AGENTS.md`; `git log -- AGENTS.md` returns only `3d6ed40` and `a9e7581`. AGENTS.md § File layout already carries a generic row — *"`skills/<name>/SKILL.md` — Skill definitions"* — and adds per-skill rows only where a skill ships an unusual artifact (`skills/ship-spec/states.json`). `session-handoff` ships nothing unusual.
**Suggested fix:** Keep the § Superseded vendor skills entry — that one is genuinely new information and is what brief Done-when #5 requires. Drop the § File layout row, or justify why this skill needs one when the previous three did not; adding it turns AGENTS.md into a partial skill inventory that nothing keeps current.

### F-8: Supersession-by-deletion departs from the recorded "third-party skills coexist, preserved" posture without naming it — and the `--prune` footgun is unaddressed
**Severity:** P3
**Where:** `VHS-28.spec.md:137-148` (D9), `:33`
**Convention violated:** Wiki `comprehension/2026-05-06-custom-skills-personal-unlock.md`; `README.md` § Install.
**Evidence:** The wiki entry records: *"vigil-skills' scope is deliberately narrow (only first-party skills/agents), so peon-ping coexists in the personal home without being mirrored into the source-of-truth repo"* and *"`sync.py`'s default behavior preserves them as untracked."* `README.md` § Install repeats the promise to operators: *"Files in those directories that aren't in this repo (e.g., third-party skills installed separately) are preserved by default."* D9 deletes instead. That is defensible here — the vendor copy is broken and genuinely superseded, unlike peon-ping, which is functioning upstream software — but the spec never names the departure. It matters for the AGENTS.md wording, because the repo's one existing removal lever is a trap: `sync.py:81-84` queues a delete for **every** `dst_files - src_files` path under `skills/`, and `~/.claude/skills/` currently holds 14 third-party skills that `--prune` would take with it.
**Suggested fix:** One sentence in D9 naming the departure from the peon-ping precedent and its reason. Then require the AGENTS.md entry to spell out a *targeted* removal (`rm -rf ~/.claude/skills/agentcraft-handoff`) and to warn explicitly against reaching for `python sync.py install --prune`.

### F-9: `references/` vs the repo's only precedent, `reference/`
**Severity:** P4
**Where:** `VHS-28.spec.md:19`
**Convention violated:** In-repo naming precedent.
**Evidence:** The sole reference-directory precedent in this tree is `skills/hermes-kanban-awareness/reference/board-schema.md` — singular. `references/` (plural) is the vendor skill's spelling (`~/.claude/skills/agentcraft-handoff/references/`) and the wider Claude Code convention.
**Suggested fix:** Either is defensible; pick deliberately and say so in half a sentence, since shipping `references/` leaves the repo carrying both spellings.

### F-10: "mirroring the talaria SKILL.md convention" overstates a single-skill precedent
**Severity:** P4
**Where:** `VHS-28.spec.md:185`
**Convention violated:** Accuracy about what is and isn't an established convention.
**Evidence:** `grep -rn "^## \(Test plan\|Test command\|Done-when\)" skills/` returns `ship-spec/SKILL.md:195` (Test plan only) and `talaria/SKILL.md:124,143,159`. The wiki `decisions/` directory has zero entries ratifying it. Note also that `sync.py` mirrors `skills/` byte-for-byte, so these sections land in every operator's `~/.claude/skills/session-handoff/SKILL.md` — which talaria does deliberately (an operator-verifiable smoke), but the spec should confirm that is the intent rather than spec residue.
**Suggested fix:** Say "following `skills/talaria/SKILL.md`" rather than "the talaria convention", and add a clause confirming the test sections are meant to ship into installs.

### F-11: Spec-level additions the brief and ticket don't authorize (drift-check visibility)
**Severity:** P3
**Where:** `VHS-28.spec.md:105`, `:193`, `:194`, `:195`, `:206`
**Convention violated:** None — this is the (c) roll-up so the human drift-check can see it.
**Evidence:** Each of these commits the design to a position neither the brief nor the Plane ticket asks for, and each carries at least implicit rationale, so all classify (c) rather than (d): the session-id UUID regex and its talaria-precedent justification (line 105); the 10-row modified-file cap with `… and N more` (line 193); `--continues-from` path-escape rejection after resolution (line 194); the same-second collision discriminator (line 195); the explicit refusal of `--json` on YAGNI grounds (line 206). None changes scope or downstream-ticket interactions. Recorded here only so the drift-check has the list; no edit required.
**Suggested fix:** No change. If any of these grows during implementation (in particular the path-validation logic, which is adjacent to the D7-fenced path-classification work), that is drift.

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 4 | P4: 2

**Two things the spec gets right that are worth recording**, because both were live risks:

1. **D9's AGENTS.md placement is exactly correct**, and better than the brief. The wiki records a supersession on precisely this point — `decisions/2026-06-14-vhs-17-requires-tolerated-not-strict-yaml.md` § Related: *"the README-pointer stopgap is superseded by a tracked, harness-neutral `AGENTS.md` at repo root — future 'referenced from project guidance' requirements resolve there, not README."* The spec also correctly drops the brief's third option (`VHS-28.brief.md:52` offered "the PR description"), which is not a tracked file at all.
2. **The 7 → 8 tripwire bump is present** (spec line 27). The brief omits it; `tests/test_lint.py:49` asserts exactly 7, and the PR would have failed without it.

**Grounding caveat for the drift-check:** the wiki's `projects/vigil-skills/` pages are roughly two months stale — there is no `architecture.md`, `state.md` was last touched 2026-06-16 (VHS-15) with "What's Active" empty, and `filemap.md` still describes a 4-skill repo with no `skills/*/scripts/` precedent. Findings above are grounded in the repo tree and the `decisions/`/`comprehension/` entries, not those two pages.

STATUS: RED P0=0 P1=1 P2=4 P3=4 P4=2
