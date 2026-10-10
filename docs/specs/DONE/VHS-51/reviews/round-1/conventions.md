# Conventions Review: round 1

## Closure of round 0 findings
N/A, round 1.

(Grounding: I read the spec, the brief and AGENTS.md (CLAUDE.md here only points to AGENTS.md). From the wiki I read the decisions for VHS-17, VHS-18, VHS-20, VHS-29, VHS-46 and VHS-47, the cross-project decision of 2026-09-27 (Codex replaces CodeRabbit), and the `state.md` and `filemap.md` lines that matter. I also read `docs/portability-contract.md` §3, `lint.py`, `docs/authoring-portable-skills.md`, `tests/test_lint.py`, the relevant cases in `tests/test_spec_close_log.py`, the frontmatter of all 11 skills, `/ship-spec`'s Tool-use notes, `/review-pr`'s Step 2, and the vigil-converter Hermes adapter (`src/converters/claude-to-hermes.ts`, `src/types/hermes.ts`, `HERMES-MAPPING.md`). `python lint.py` today prints `0 error(s), 2 warning(s)` (ship-spec, review-pr). The spec has no Deferred section, so there were no rows to check. The shared-memory namespace "skills" is ACL-denied, so I checked the VHS ticket list through the Plane tool instead.)

Things that already conform: the key order in both blocks (shell, filesystem, network, subagents, services) matches all 9 existing blocks. No other skill has an inline subagent fallback, so `subagents: true` on the others stays accurate. The fixture layout follows the existing split (a valid skill as `<name>/SKILL.md`, a malformed one as flat `<name>.md`). There is no premature abstraction and no backwards-compat shim. The Hermes adapter reads booleans with `value === true` (claude-to-hermes.ts:102-108), so `optional` is already not emitted as a requirement, as the new contract note says.

## Findings

### F-1: The rewritten promotion-path sentence claims the `--strict` hook blocks missing-requires regressions; it does not
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7 (spec.md:73); § Design / `docs/authoring-portable-skills.md` (spec.md:116)
**Convention violated:** `lint.py` docstring (lines 15-18) and `docs/authoring-portable-skills.md:27,31`: "`--strict` exits non-zero if any ERROR (WARNs never gate)". VHS-18 decision: "WARN = missing `requires:`".
**Evidence:** The new text is "Every shipped skill carries a block, so `--strict` is clean and the hook blocks regressions." `missing-requires` is a WARN, so a skill that loses its block, or a new skill without one, passes `--strict` and the hook. The only real guard against that regression is the new assertion in `test_shipped_skills_clean` (Decision 9). The spec's own Out of scope excludes "any `--strict` mode that treats WARN as an error", which agrees that the hook cannot catch it.
**Suggested fix:** Reword it as: "Every shipped skill carries a block. The hook blocks ERROR regressions; a missing block on a shipped skill is caught by `tests/test_lint.py::test_shipped_skills_clean`, since `--strict` never gates on WARNs."

### F-2: Decision 3 makes `shell: optional` legal, but the Hermes `shell` row is left unchanged and the note lands on a row that includes a non-boolean
**Severity:** P2
**Where:** spec § Design / `docs/portability-contract.md` §3, Hermes mapping bullet (spec.md:100); § Decision 3 (spec.md:55-57)
**Convention violated:** The cross-surface rule (lock the wire format), and the VHS-20 decision that "the §3 mapping is lossy-in-kind, and the gaps are documented, never silently dropped".
**Evidence:** In the contract's mapping table (portability-contract.md:97-101), `shell` has its own row: "a `terminal`-toolset requirement", with an empty Note. The spec adds "an `optional` boolean is not emitted as a requirement" only to the `network`, `subagents`, `filesystem` row. `filesystem` is a flow sequence, not a boolean, and the `shell` row, the one boolean whose mapping does emit a requirement, says nothing about `optional`. A reader of the table would map `shell: optional` to a terminal-toolset requirement, while the adapter does not.
**Suggested fix:** Put the note on the `shell` row as well ("`shell: optional` emits no terminal-toolset requirement"). Alternatively, state it once in the prose under the table: "An `optional` boolean (`shell`, `network`, `subagents`) is never emitted as a Hermes requirement or a pre-flight check."

### F-3: Out of scope names a "swappable reviewer" ticket that does not exist
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Out of scope, bullet 2 (spec.md:159); § Decision 4 (spec.md:61) relies on it
**Convention violated:** Wiki decision `2026-09-27-cross-codex-review-gate-replaces-coderabbit.md`: "`/review-pr` stays CodeRabbit-only. Making it reviewer-agnostic is unticketed VHS work". AGENTS.md § Plan & Spec Reviews says to verify load-bearing claims against current state.
**Evidence:** The VHS project in Plane tops out at VHS-51 (this ticket). No VHS item covers a swappable or reviewer-agnostic `/review-pr`; the only `/review-pr` items are VHS-3 and VHS-41, both unrelated. The spec says "its own ticket flips `code-review-bot` to `code-review-bot?`", but no such ticket exists. The claim comes from brief Out of scope bullet 2, so the spec inherits it rather than inventing it.
**Suggested fix:** Either file the ticket and cite its ID, or change the text to "unticketed (wiki decision 2026-09-27); whoever adds the fallback flips `code-review-bot` to `code-review-bot?`".

### F-4: The converter repo's mapping docs go stale and the spec does not say so
**Severity:** P3
**Where:** spec § Out of scope, last bullet (spec.md:163)
**Convention violated:** VHS-20 decision: mismatches go back through the contract, and gaps are "documented, never silently dropped".
**Evidence:** vigil-converter `HERMES-MAPPING.md:19` says "`shell` is a boolean, never optional", and `src/types/hermes.ts:46-47` says "Booleans ... are required-when-present; only services carry optionality". Both become false once the contract accepts `optional`. The adapter's behaviour is still correct (`value === true`).
**Suggested fix:** Change the Out-of-scope bullet to: "the adapter needs no code change (`value === true` already treats `optional` as not required); its `HERMES-MAPPING.md:19` and `types/hermes.ts:47` wording goes stale and is a follow-up in that repo."

### F-5: The comment on the strengthened shipped-skills test still says "zero ERRORs"
**Severity:** P3
**Where:** spec § Design / `tests/test_lint.py` (spec.md:110-111)
**Convention violated:** The repo pattern that every test case carries a `# Regression for VHS-<n>: <behaviour>` line describing what it pins.
**Evidence:** test_lint.py:49 reads "# Regression for VHS-18: lint runs clean (zero ERRORs) against the shipped skills." The spec requires a VHS-51 comment only on "each new case". The modified case would then pin zero WARNs while its comment still says zero ERRORs.
**Suggested fix:** Add a line to the Design bullet: the case's comment gains "...and zero WARNs (VHS-51)".

### F-6: The renamed backlog tripwire stays in the spec-close-named suite, against that file's own stated rule
**Severity:** P3
**Where:** spec § Decision 7 (spec.md:73); § Design / `tests/test_spec_close_log.py` (spec.md:120)
**Convention violated:** The comment at `tests/test_spec_close_log.py:1041-1044`: "a repo-wide ban asserted from a spec-close-named suite would fail pointing at the wrong subsystem."
**Evidence:** `test_missing_requires_backlog_is_clear` no longer checks anything about spec-close. It is a repo-wide assertion about the authoring doc. The brief's Done when names `tests/test_spec_close_log.py` explicitly, so moving it is not required. This is a P3 for the drift-check only.
**Suggested fix:** Add one sentence to Decision 7 saying the test stays in `TestNoStaleWording` because the brief's Done when names this file. Alternatively, raise moving it into `tests/test_lint.py` with the operator.

### F-7: The contract text in Decision 4 is a spec-level addition that cites brief decisions that do not authorize it
**Severity:** P3
**Where:** spec § Decision 4 (spec.md:59-61); Scope row for the contract (spec.md:13)
**Convention violated:** The silent-additions check: class (c), an addition with rationale but attributed to the brief.
**Evidence:** Brief decisions 4 and 5 settle that `vcs-host` and `code-review-bot` are required on the two skills. The brief's Scope row for the contract lists only the booleans sentence, the schema comment and the Hermes note. Adding `vcs-host` and `code-review-bot` meanings to the role-token sentence is reasonable and has a rationale ("gains the same for the two tokens entering use"), but the "(brief 4, 5)" label presents it as carried from the brief.
**Suggested fix:** Label Decision 4 as "(spec addition; supports brief 4, 5)" so the operator's drift-check sees it.

### F-8: The `/spec-close` `vcs-host?` follow-up has no ticket and no Deferred row
**Severity:** P3
**Where:** spec § Decision 8 (spec.md:77); § Out of scope bullet 4 (spec.md:161)
**Convention violated:** The repo practice from VHS-37: a valid, out-of-scope item gets a ticket plus a `## Deferred — follow-up required` row, not loose prose.
**Evidence:** "that is a one-line follow-up once the operator confirms it". No VHS ticket covers it, and the spec has no Deferred section. Once this ships, it is the one block that uses `gh` without declaring `vcs-host`, and nothing tracks it.
**Suggested fix:** Ask the operator to file a ticket and cite it in Decision 8. If they prefer not to, write "untracked; operator to decide" so the drift-check sees the gap.

### F-9: The contract's definition of "required" still keys on `?` alone
**Severity:** P3
**Where:** spec § Design / Availability bullet (spec.md:98)
**Convention violated:** The contract is meant to be quoted word for word downstream, by VHS-21 (conformance suite) and VHS-20 (Hermes adapter).
**Evidence:** portability-contract.md:78 reads "A harness MUST verify each **required** capability (no `?`) before any mutation". `subagents: optional` has no `?`, so under that parenthetical it reads as required. The appended sentence "An `optional` boolean is likewise never verified at pre-flight" fixes the meaning only for someone who reads further.
**Suggested fix:** Also change the parenthetical to "(no `?` on a service; not `optional` on a boolean)".

### F-10: The lint's `.lower()` disagrees with lexical rule 5's "exactly (lowercase)"
**Severity:** P4
**Where:** spec § Design / Lexical rules step 5 (spec.md:99) and § `lint.py` (spec.md:104)
**Convention violated:** Contract §3 step 5: "must match the controlled vocabulary **exactly** (lowercase, unquoted)".
**Evidence:** `lint.py:106` checks `val.lower()`, so `Optional` and `TRUE` pass. The mismatch already exists, but this spec edits both lines and makes step 5 list the boolean values outright.
**Suggested fix:** Optionally add a sentence noting the lint is case-insensitive for booleans, or leave it alone. This is not required for this ticket.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 6 | P4: 1

Files referenced:
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-51.spec.md
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-51.brief.md
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\portability-contract.md (lines 63, 78, 87, 97-101)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\authoring-portable-skills.md (lines 27-42)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\lint.py (lines 15-18, 103-108)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\tests\test_lint.py (lines 48-59)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\tests\test_spec_close_log.py (lines 1041-1066, 1196-1203)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-converter\HERMES-MAPPING.md (line 19), src\types\hermes.ts (lines 46-47), src\converters\claude-to-hermes.ts (lines 102-108)
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki\decisions\2026-09-27-cross-codex-review-gate-replaces-coderabbit.md
- C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki\decisions\2026-06-18-vhs-20-hermes-preflight-advisory.md

STATUS: GREEN
