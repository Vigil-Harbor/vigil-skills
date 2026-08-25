# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: The tripwire bump and the "44 passed" baseline are true only on an unmerged local branch, not at ship-spec's branch point
**Severity:** P1
**Where:** spec § Scope → Modified files (`docs/specs/TODO/VHS-28.spec.md:27`); spec § Test command (`:237`); test plan item 7 (`:227`)
**Claim:** "`tests/test_lint.py` | Bump the shipped-skill inventory tripwire 7 → 8" and "The third command is the full-suite regression gate (currently `44 passed, 8 subtests passed`)."
**Why this is wrong:** The `7` exists only on the current branch. It was set by `7a3a929 2026-08-23 test(lint): bump shipped-skill tripwire 4 -> 7`, which `git merge-base --is-ancestor 7a3a929 origin/main` reports as **NO**. `origin/main` is still `a0ad847` (2026-06-28), where:
- `tests/test_lint.py:52` reads `len(skills), 4` — not 7;
- `git ls-tree -r origin/main skills/ | grep SKILL.md` returns **5** files (review-pr, ship-spec, spec-close, spec-cycle, talaria).

So at `origin/main` the suite is **already red** (`test_shipped_skills_clean` asserts 4 == 5) before any VHS-28 work, and the baseline is not `44 passed` but 43 passed / 1 failed. `skills/ship-spec/SKILL.md:76` cuts the worktree with `git worktree add -b <branch> <worktree-path> origin/<default-branch>`, so the implementer lands in exactly that tree: the instructed `7 → 8` edit has no matching text, the correct value there would be `6`, and the "regression gate" the spec names cannot go green.
(The 44/8 numbers themselves are otherwise sound: `grep -c "def test_"` gives 6 + 19 + 19 = 44, and `tests/test_talaria_bridge.py:490-499` has exactly 8 `subTest` cases.)
**Suggested fix:** State the precondition explicitly — e.g. "This spec assumes commits `386dc6c`, `8946f58`, `7a3a929` (bloat-check, hermes-kanban-awareness, tripwire 4→7) have merged to `main`; if ship-spec's worktree still shows `len(skills), 4`, the bump is `N → N+1` against whatever is on the base branch, and the pre-existing 4-vs-5 failure must be fixed first." Replace the hardcoded "7 → 8" with "current value → current value + 1" and re-state the baseline as "the suite is green at the branch point" rather than a pinned count.

---

### F-2: D6 attributes the score 68 to "the untouched scaffold"; the ticket and the code say otherwise
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D6 (`:111`)
**Claim:** "The vendor gate was 'score ≥ 70 and no secrets,' on a 0–100 scale where the untouched scaffold scored 68."
**Why this is wrong:** The Plane ticket (record `806902ac-…`, chunk 2) says: "Measured on a **real, fully-written handoff**: score 68 → 80". Chunk 1 shows what the *untouched* scaffold actually produced — `Current State Summary (incomplete) <- correct, still has a TODO`, plus two `(missing)`. Running the vendor formula at `~/.claude/skills/agentcraft-handoff/scripts/validate_handoff.py:145-159` on an untouched scaffold: `-30` (TODOs present) `-10 × 3` (all three required in the missing list) `- 2 × 6` (all recommended at `###`) ⇒ ≤ 40, not 68. The gate claim itself (`score >= 70 and not secrets_found`) is verified at `validate_handoff.py:260`.
The *conclusion* D6 draws survives — a fully-filled document at the template's own depths scored 68 and could not clear 70, which the ticket calls "a false floor" — but the stated evidence is wrong, and the ticket is canonical.
**Suggested fix:** Rewrite as: "…on a 0–100 scale where a **fully-written** handoff at the template's own heading depths scored 68 — a floor the template's structure imposed, not its content (ticket VHS-28, measured 68 → 80 after the regex fix)."

---

### F-3: D9 puts an operative `~/.claude/…` path into SKILL.md, which is exactly what D5 refuses to do
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D9 (`:141-146`) vs § D5 (`:97-104`)
**Claim:** D5: "Baking that path in as the operative instruction would violate portability-contract §2 ('assumptions about a specific harness's filesystem layout')." D9: "It is recorded in two tracked places… 1. `skills/session-handoff/SKILL.md` § *Superseding the vendor skill* — the uninstall command and what to expect."
**Why this is wrong:** `docs/portability-contract.md:43` reads verbatim: "**Do not survive — avoid them:** …assumptions about a specific harness's filesystem layout or affordances beyond what `requires` declares." An uninstall command naming `~/.claude/skills/agentcraft-handoff/` is precisely such an assumption, sitting in the same portable `SKILL.md` body from which D5 carefully exiled `~/.claude/projects/**/<session-id>.jsonl`. `lint.py` will not catch it (`_MCP_RE` only flags `mcp__*` — see `lint.py:56, 202-240`), so the inconsistency ships silently. The brief carries "Portability contract applies (§2–§3)" as a decision (`VHS-28.brief.md:60`).
**Suggested fix:** Apply D5's own remedy to D9: keep the operative sentence harness-neutral ("remove any previously installed vendor handoff skill from this harness's skill directory") and put the literal `rm -rf ~/.claude/skills/agentcraft-handoff/` under the same clearly-marked, non-operative notes heading. Or drop it from SKILL.md entirely and keep the command only in `AGENTS.md`, which is machine-facing repo guidance rather than a portable artifact.

---

### F-4: The section vocabulary — the "single source" D4 pins — is never enumerated
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D4 (`:86-91`), § `create_handoff.py` (`:197`), § `validate_handoff.py` (`:203`), § D8 (`:133-135`)
**Claim:** "Both scripts import their section vocabulary from **one module-level source**… `validate_handoff.py` declares `REQUIRED_SECTIONS` and `RECOMMENDED_SECTIONS`." / "Section vocabulary is a module-level ordered table — the single source D4 pins."
**Why this is wrong:** The spec never says what is in that table. For a spec this specific elsewhere, that leaves the load-bearing artifact to the implementer, and two consequences follow that the spec does not address:

1. **A container section can never reach READY.** D3 (`:68-71`) defines `end` as "the offset of the next heading at ANY depth", and § validate (`:204`) requires "≥50 characters of *own* content". Any required section whose body is entirely subsections (the vendor's `## Context for Resuming Agent` at `create_handoff.py:298` is exactly this shape) has zero own content and is permanently `incomplete`. The invariant "every REQUIRED section must be a leaf in the template" is real and unstated. D4's round-trip test would eventually surface it, but as a mystery failure rather than a stated constraint.
2. **Existing documents.** The brief carries "Existing handoff documents on disk… must remain readable and listable by the new skill" (`VHS-28.brief.md:61`), and D8 restates it. Every such document uses the vendor's names (`Current State Summary`, `Important Context`, `Immediate Next Steps` — `validate_handoff.py:40-53`). D1's clean-room posture creates direct pressure to rename them, and nothing in the spec or test plan pins whether a vendor-era document still validates.

**Suggested fix:** Enumerate `REQUIRED_SECTIONS`, `RECOMMENDED_SECTIONS`, and the ordered template table (name + depth) in § Design. Add the sentence "every REQUIRED section is a leaf — no subsections beneath it — because D3's terminator gives a container zero own content." State whether section names carry over from the vendor's vocabulary, and if they do, add a fixture under `tests/fixtures/` holding a vendor-format document that must still validate.

---

### F-5: Exit code 2 is overloaded, contradicting D6's stated reason for distinct codes
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D6 verdict table (`:116-121`) vs § `validate_handoff.py` (`:206`)
**Claim:** D6: "Distinct exit codes let a caller tell 'unfinished' from 'dangerous.'" § validate: "Missing file → clear message, exit `2`. Unreadable/undecodable file → same."
**Why this is wrong:** `2` is `BLOCKED` — "any secret pattern matched". Assigning the same code to a usage/IO error means a caller acting on `2` cannot distinguish "this document contains a credential" from "you typed the wrong filename", which is the precise distinction D6 says the codes exist to preserve.
**Suggested fix:** Give the error path its own code (`3`, or the conventional `64`/`66`) and add the row to D6's table so the code set is declared in one place. If sharing `2` is deliberate, say so in D6 and drop the "dangerous vs unfinished" justification.

---

### F-6: D3's span definition contradicts itself one sentence later
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D3 (`:69-71` vs `:80`)
**Claim:** "`end` is the offset of the next heading at ANY depth, or len(content)." … "Section content is measured after stripping the trailing/leading whitespace and **any nested heading lines the span does not own**."
**Why this is wrong:** If the span terminates at the next heading of any depth, the span provably contains no heading lines at all — there is nothing to strip. The two sentences describe different designs (terminate-at-any-depth vs. include-subsections-then-filter), and they produce different verdicts for a container section (see F-4). An implementer following the second sentence would build the more permissive version the spec elsewhere says it is replacing.
**Suggested fix:** Delete the "any nested heading lines" clause; the stripping rule is whitespace only.

---

### F-7: Fenced code blocks are not excluded from heading detection, and D3 makes the exposure worse
**Severity:** P2
**Where:** spec § D3 (`:61-80`), § `validate_handoff.py` (`:203-204`)
**Claim:** "`end` is the offset of the next heading at ANY depth… Terminating at *any* depth 1–6 fixes the over-generous pass, which means the rewrite is slightly **stricter** than the vendor's patched version."
**Why this is wrong:** Handoff documents routinely embed shell blocks, and a line inside a fence that begins with `#` (a `# comment`, a `#!/usr/bin/env` shebang, a `#123` issue reference) is indistinguishable from an ATX heading to a bare `#{1,6}` regex. Under the vendor's `##?` this mostly did not bite; under "terminate at any depth" a single `# rebuild the index` line inside a fence truncates its section's span, and the ≥50-character own-content check can then report a fully-written required section as `incomplete`. That is the same user-visible symptom class VHS-28 was filed for. `lint.py:55, 209-215` shows this repo already tracks fence state (`_FENCE_RE`, `in_fence`) precisely for this reason, so the pattern is established here.
The spec is also silent on two CommonMark details the "per CommonMark" comment at `:61` implies: ATX headings require a space after the hashes (so `##Foo` is not a heading), and up to 3 leading spaces of indentation are permitted.
**Suggested fix:** Say in D3 that `section_span` scans with fence state (mirroring `lint.py`'s `_FENCE_RE` handling), require the space after the hashes, and add a test-plan case: "a `#`-leading line inside a fenced block does not terminate a section."

---

### F-8: `--project-path` appears in the CLI with no stated purpose
**Severity:** P3
**Where:** spec § `create_handoff.py` (`:189`)
**Claim:** "CLI: `create_handoff.py [slug] [--continues-from FILE] [--project-path PATH]`."
**Why this is wrong:** No other line in the spec reads this flag. In the vendor design the project root existed to resolve the file-reference check (`validate_handoff.py:94-134`, `base_path`), and D7 (`:123-129`) deletes that check. `--continues-from` resolves against `.claude/handoffs/` (`:194`) and git metadata comes from the cwd (`:192`), so the flag has no consumer.
**Suggested fix:** Either state what it does (e.g. "runs git discovery and writes `.claude/handoffs/` relative to PATH instead of cwd; defaults to cwd") or drop it from the CLI.

---

### F-9: The advisory score is promised but never defined
**Severity:** P3
**Where:** spec § D6 (`:121`), § `validate_handoff.py` (`:205`)
**Claim:** "The advisory **score is still printed** — it is genuinely useful for 'is this thin?' — but it gates nothing… Report prints each check, the advisory score, and the verdict."
**Why this is wrong:** The vendor formula (`validate_handoff.py:137-170`) cannot be carried: D1 forbids transcription, D7 removes one of its five terms (`files_missing`), and D6 changes the required-section semantics that drive another. So the implementer must invent a formula, and no test constrains it — a user-visible number with no specification.
**Suggested fix:** Give the formula in § `validate_handoff.py` (start, deductions, floor), or say plainly that the exact weights are implementer's choice and only monotonicity is required.

---

### F-10: Test-plan item 6 asserts zero warnings; the Test command cannot check that
**Severity:** P3
**Where:** spec test plan item 6 (`:226`) vs § Test command (`:233`)
**Claim:** "passes `lint.py --strict` with zero errors **and** zero warnings (it declares `requires:`, so the `missing-requires` WARN must not appear)."
**Why this is wrong:** The substantive claim is correct — I traced `_lint_requires` (`lint.py:145-199`) against the proposed frontmatter: `requires:` present (no `missing-requires` WARN at `:158`), block form, `shell: true` in `BOOL_KEYS` ✓, `filesystem: [read, write]` a flow sequence over `FILESYSTEM_VOCAB` ✓ ⇒ zero ERROR, zero WARN. But `lint.py:291` returns `1 if (strict and n_err > 0)` — "WARNs never affect exit" (`:17`). The console command in § Test command therefore cannot fail on a warning; only a programmatic assertion over `lint.lint_path(...)` can, as `tests/test_lint.py:44-46` already does.
**Suggested fix:** Note that item 6's zero-WARN half is asserted inside `tests/test_session_handoff.py` via `lint.lint_path`, not by the `--strict` exit code.

---

### F-11: The brief asks for fixtures under `tests/fixtures/`; the test plan never uses them
**Severity:** P3
**Where:** spec § Test plan (`:214-227`) vs `VHS-28.brief.md:48`
**Claim:** Brief: "Follows the existing `tests/test_lint.py` / `tests/test_talaria_*.py` shape (stdlib + pytest, **fixtures under `tests/fixtures/`**)."
**Why this is wrong:** Every case in the spec's plan is generated in-process or in a temp dir; `tests/fixtures/` is never mentioned. `tests/test_lint.py:18` (`FIX = … / "fixtures"`) is the shape the brief points at, and `tests/fixtures/` already holds 13 such files. This matters most for F-4's vendor-format regression, which is naturally a checked-in fixture. (The `load_script` helper claim at `:214` does check out — `tests/test_talaria_watch.py:21-32` defines exactly that helper, and `skills/*/scripts/` has no `__init__.py`.)
**Suggested fix:** Add one sentence saying which cases are fixtures on disk and which are generated, or state that this suite deliberately generates everything.

---

### F-12: The `pytest` gate is not a stdlib-only command
**Severity:** P3
**Where:** spec § Test command (`:234-237`)
**Claim:** "`python -m pytest tests/ -q` … the full-suite regression gate (currently `44 passed, 8 subtests passed`)."
**Why this is wrong:** `AGENTS.md` § "What this repo is" states "no build step, no test suite, no dependencies beyond Python 3.8+ stdlib." The `8 subtests passed` line is `pytest-subtests` output specifically; without that plugin the summary differs, and without pytest the command does not run at all. The spec offers no stdlib equivalent for the full suite.
**Suggested fix:** Add the stdlib fallback (`python -m unittest discover -s tests -v`) alongside, and note that pytest + pytest-subtests are operator-local tools, not repo dependencies.

---

### F-13: "~1,150 lines" is the scripts only
**Severity:** P4
**Where:** spec § D1 (`:42`)
**Claim:** "Importing ~1,150 lines of a vendor-managed third-party skill…"
**Why this is wrong:** `wc -l` over the vendor tree: scripts total 1,147; the whole tree (SKILL.md + references + scripts) is 1,569.
**Suggested fix:** "~1,150 lines of vendor scripts (≈1,570 including SKILL.md and references)."

---

## Verified without finding

- D3's account of the filed defect is accurate: the ticket records the three call sites as `##?` at lines 68, 90 and `\n##?\s+` at line 75; the installed copy now reads `#{1,6}` at all three (`validate_handoff.py:68, 75, 91`), and the spec correctly acknowledges it is comparing against "the vendor's patched version" (`:80`).
- Brief's heading-depth claims: `### Immediate Next Steps` is at `create_handoff.py:284`, `### Important Context` at `:300`. Exact.
- `sync.py` needs no change: `SUBTREES = ("skills", "agents")` (`sync.py:30`) and `iter_files` uses `rglob("*")` (`:41-45`), so `scripts/` and `references/` mirror automatically.
- `skills/talaria/SKILL.md` does carry § Test plan / § Test command / § Done-when (lines 124, 143, 159), so the convention the spec mirrors at `:185` exists.
- D5's contract citation is verbatim at `docs/portability-contract.md:43`; the commit it cites, `60303f9 fix(talaria): reject invalid watch ids`, resolves.
- `.claude/` is gitignored (`.gitignore:8`), so D8's parenthetical holds.
- Done-when mapping is genuinely 1:1 — brief #1–#6 ↔ spec #1–#6, and spec #6's re-mapping onto the Plane ticket's own criteria (regex depths, scaffold validates, adoption, smoke test) matches the ticket text.
- `git log` on the touched files: `tests/test_lint.py` last moved `7a3a929` (today — see F-1); `lint.py` and `sync.py` untouched since June and May respectively.

Files read for verification (absolute): `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/lint.py`, `.../sync.py`, `.../AGENTS.md`, `.../README.md`, `.../tests/test_lint.py`, `.../tests/test_talaria_watch.py`, `.../tests/test_talaria_bridge.py`, `.../skills/talaria/SKILL.md`, `.../skills/ship-spec/SKILL.md`, `.../docs/portability-contract.md`, `C:/Users/zioni/.claude/skills/agentcraft-handoff/scripts/validate_handoff.py`, `.../create_handoff.py`.

## Summary
P0: 0 | P1: 1 | P2: 6 | P3: 5 | P4: 1

STATUS: RED P0=0 P1=1 P2=6 P3=5 P4=1
