# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: "No helper script" rests on a false claim about `sync.py`, and contradicts the shipped `skills/<name>/scripts/` precedent
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope (row 3, "new files — **None.**"); D2 (the 7-step parse procedure)
**Convention violated:** repo precedent set by VHS-29 (deterministic work moves out of prose into a stdlib script under the skill's own dir) + accurate statements about `sync.py`
**Evidence:**
- Spec: *"no helper script, no new subtree (adding a top-level subtree would require editing `sync.py`'s `SUBTREES`, which this spec does not do)"*. That is a non-sequitur: a helper at `skills/review-pr/scripts/…` is **not** a new top-level subtree. `sync.py:30` — `SUBTREES = ("skills", "agents")`; `iter_files()` walks `root.rglob("*")`, so anything under `skills/review-pr/` mirrors with **zero** `sync.py` change.
- Two shipped skills already carry script subdirs: `skills/spec-close/scripts/` and `skills/session-handoff/scripts/`.
- Wiki `projects/vigil-skills/state.md` (VHS-29): *"The deterministic part moved out of prose into `skills/spec-close/scripts/prepend_log_entry.py` — the skill's **first script** — stdlib-only … Every shape the anchor cannot describe is a refusal (exit 2), never a silent bottom-append."* VHS-41's D2 is exactly that shape: an anchored regex parse, a depth-counted `<details>` scan, a dedup key, and a declared-vs-parsed count check (Decision 11 is literally a refusal/tripwire contract) — expressed as prose.
**Suggested fix:** Correct the Scope cell (drop the `SUBTREES` reasoning — it doesn't apply), and promote "the parse is prose, not a script" to a numbered `## Decisions` entry with the real tradeoff (an LLM parse tolerates CodeRabbit's format drift where a regex script would refuse; the tripwire is the mitigation). Load-bearing design choices belong in `## Decisions` per the VHS-32/33/36 spec shape, not in a Scope-table parenthetical.

### F-2: Two different severity-matching rules for the same labels, in one triage table
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D3 (Step 3 severity table) vs § D2 step 5
**Convention violated:** single source of truth — a new check that mirrors an existing check should extract the shared definition, not restate it differently
**Evidence:** D3 keeps/extends the **emoji-keyed** table (`skills/review-pr/SKILL.md:89-94`: `_🔴 Critical_`, `_🟠 Major_`, `_🟡 Minor_`; D3 adds `_🔵 Trivial_`). D2 step 5 defines body-item severity **by word**: *"the label span whose text contains one of `Critical`, `Major`, `Minor`, `Trivial`"* — and D2 step 2 argues the principle explicitly: *"Matching is on the section **phrase**, never the emoji, so an emoji change does not break the parse."* D3's own heading is *"one triage table, two origins"*, so one table now carries two incompatible matching disciplines: a CodeRabbit emoji change silently breaks inline triage while body triage keeps working.
Secondary: the table's "Pattern in body" column now gets an `Unlabeled` row with no pattern, and still carries `Nitpick` — a *section* name, not a severity — which D3 itself calls out as wrong yet keeps as a "note" row.
**Suggested fix:** State one severity rule for both origins (word-contains on the `_…_` label span, emoji shown as illustration only), and move `Nitpick` out of the severity table into the § Important triage rules block where D3 already rewrites the section rules.

### F-3: `AGENTS.md` § /review-pr goes stale, and the spec forbids touching it
**Severity:** P2
**Where:** spec § Scope ("everything else in the repo — **Leave alone.** No … `AGENTS.md` …"), § Out of scope 3
**Convention violated:** `AGENTS.md` is the repo's canonical, tracked project instruction file (project `CLAUDE.md`: *"The canonical, portable project instructions … live in **`AGENTS.md`**"*); shipped precedent updates it in the same PR when a skill's documented behavior changes
**Evidence:** `AGENTS.md:46` § /review-pr currently reads: *"Reads findings, verifies against current code, fixes real issues, pushes, posts per-thread commit-hash replies, conditionally waits … Non-fix threads (skip/duplicate/already-fixed) are left open…"*. After this spec the skill also harvests review-**body** findings and posts a PR-level disposition comment per round — a new externally-visible write class that this paragraph does not describe. Precedent: wiki `state.md` VHS-29 — *"Nine `SKILL.md` sites plus `AGENTS.md:29`/`:100` and `docs/authoring-portable-skills.md:41` reworded"*.
**Suggested fix:** Add `AGENTS.md:46` to the Scope table as a one-sentence amendment ("…also reads the review body's Outside-diff and Nitpick sections and posts their dispositions as one PR-level comment per round"), or record in § Out of scope why the paragraph is left stale.

### F-4: Test plan drops the repo's established prose-spec gate shape
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan, "Reviewer checklist" items 7–11; § Test command
**Convention violated:** the doc-only-spec gate convention set by VHS-32/33/36 — a checklist of copy-pasteable greps/diffs, not prose judgments
**Evidence:** `docs/specs/DONE/VHS-36/spec.md` § Test plan: *"Every row is a grep or a diff against the worktree … Where an asserted phrase contains a backtick, the row gives a backtick-free substring so the command is copy-pasteable"*, and its row 1 pins the exact WARN count (*"`missing-requires` WARN count is 2 (unchanged: `review-pr`, `ship-spec`)"*). VHS-41's items 7–11 are assertions a human must eyeball (*"no `--jq` program in the file still contains `last`, `| length`, or a `[...]` array-wrap"*, *"the two filters … are not unified"*) with no command given, and items 1–2 do not pin the WARN count.
**Suggested fix:** Convert 7–11 to greps against the worktree — e.g. `grep -c 'gh api' vs 'gh api --paginate'`, `grep -nF 'sort_by(.submitted_at)'` → 0, `grep -cF 'select((.body // "") != "")'` → expected N, `grep -cF 'Guard for body-level findings'` → 0, `git diff --name-only` → exactly one path — and pin `missing-requires` at 2 in item 2.

### F-5: `python sync.py status` is not a gate, and "status clean" reads against the spec's own test plan
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test command; § Done when 2; § Test plan item 3
**Convention violated:** `## Test command` is `/ship-spec`'s pass/fail gate; an acceptance criterion must be checkable as stated
**Evidence:** `sync.py:155` `cmd_status()` prints diffs and returns `None` — it **always** exits 0, so appending it to `python lint.py … --strict && python lint.py --strict && python sync.py status` adds no gate. It also compares the *worktree* against the live `~/.claude/` (`resolve_claude_dir`), which `/ship-spec` cannot control — the installed copy legitimately lags `main`, so unrelated files can show as differing. Meanwhile Done-when 2 says *"`sync.py status` clean"* while test-plan item 3 says it *"must show `skills/review-pr/SKILL.md` as the only difference"* — the criterion is met by a *non*-clean status.
*(Deliberately not escalated to P0: Done-when 2 points at test-plan items 1–3, which define the intended meaning. It is wording, not a genuine contradiction.)*
**Suggested fix:** Restate Done-when 2 as "`lint.py --strict` zero ERROR; `sync.py status` shows `skills/review-pr/SKILL.md` as the only repo↔config difference (observational, machine-dependent)", and move `sync.py status` out of `## Test command` into the manual reviewer checklist alongside items 4–11.

### F-6: The spec asserts the repo has no test suite; it has five pytest modules
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan, first line
**Convention violated:** verify load-bearing claims against current file state (`AGENTS.md` § Plan & Spec Reviews: *"Always verify load-bearing claims against the actual codebase … never review from memory"*)
**Evidence:** Spec: *"The repo has no test suite (`AGENTS.md`: 'no build step, no test suite')"*. `AGENTS.md:7` does say that, but it is stale: `tests/` holds `test_lint.py`, `test_session_handoff.py`, `test_spec_close_log.py`, `test_talaria_bridge.py`, `test_talaria_watch.py`. Wiki `state.md` VHS-18: *"`tests/test_lint.py` + `tests/fixtures/` are the repo's **first test suite**"*; VHS-29: *"suite 159 passed (57 new)"*. `tests/test_lint.py:50-53` also carries an inventory tripwire asserting exactly 8 shipped skills — unaffected here, which is worth *stating* rather than leaving implied.
**Suggested fix:** Replace the claim with the accurate one: the repo has a pytest suite, but this change touches no Python and no skill count, so the gate is `lint.py --strict` plus the checklist (the VHS-32/33/36 precedent). Optionally add `python -m pytest tests/ -q` as a no-regression row.

### F-7: New section naming breaks the skill file's own numbering convention
**Severity:** P3
**Where:** spec § D2 (`## Step 2b: Extract body-level findings`), § D7 (`6c-body`)
**Convention violated:** `skills/review-pr/SKILL.md`'s heading pattern — numbered steps are `##` (`## Step 1`, `## Step 2`, `## Step 6`), letter-suffixed sub-steps are `###` (`### 1b. Check CodeRabbit config`, `### 6a.`–`### 6e.`)
**Evidence:** `skills/review-pr/SKILL.md:48` `### 1b. Check CodeRabbit config`; `:162` `### 6a.`; `:243` `### 6c.`. The spec proposes a letter-suffixed `Step 2b` at `##` level, and a sub-step named `6c-body` — a hyphenated shape the file uses nowhere.
**Suggested fix:** Either `### 2b. Extract body-level findings` (matching `1b`), or promote it to a full `## Step 3` with renumbering (heavier — probably not worth it). Rename `6c-body` to `6f.` or state it as a labelled sub-heading *inside* 6c rather than a new step id, and use that name consistently in D4/D5/D6/D8.

### F-8: Spec-level additions the human drift-check should see
**Severity:** P3
**Where:** spec § Decisions 7–12; § D3
**Convention violated:** none — recorded so the drift-check has the list (all are category (c): spec-level additions carrying explicit rationale, none silent)
**Evidence:** The brief carries five decisions. The spec adds six more, each labelled `*(spec-author)*` with rationale: D7 streaming-jq conversion (which also **changes existing working logic** — verdict determination moves from `sort_by(.submitted_at) | last` to "the agent takes the record with the highest `id`", i.e. a jq aggregate becomes an LLM judgment, on the strength of an uncited "review ids are monotonically increasing" claim), D8 split filters, D9 finding key, D10 nested-`<details>` stripping, D11 tripwire, D12 idempotency marker. D3 additionally adds `Trivial` and `Unlabeled` severity rows, which the brief does not mention. No category-(d) silent additions found.
**Suggested fix:** No spec change required. If anything, add one sentence under D7 grounding the monotonic-id claim (GitHub review ids are globally increasing) so a later editor doesn't re-litigate it.

### F-9: The `--body-file` path is unspecified, inside a git worktree
**Severity:** P3
**Where:** spec § D7 (`gh pr comment <N> --body-file <path-to-body-file>`)
**Convention violated:** `AGENTS.md` § Git Hygiene — *"Before committing, audit staged paths for stale skill copies, backup files, and large binaries"*
**Evidence:** The skill runs in the PR's worktree (Step 1 resolves `WORKTREE_PATH`), and 6b/Step 5 push in the same round. The spec never says where the body file lives, so the natural reading is "in the repo". Step 5's *"Stage only the changed files by name (never use `git add -A`)"* contains the risk but does not remove the untracked-file litter.
**Suggested fix:** Say the body file is written to the system temp dir (or the harness scratch dir), never inside the worktree, and is removed after the post.

### F-10: The `requires:` deferral doesn't cite the tracked backlog it belongs to
**Severity:** P3
**Where:** spec § Out of scope 2
**Convention violated:** none broken — this is brief-authorized (Q6) — but the deferral is recorded in two places the spec doesn't name
**Evidence:** `docs/authoring-portable-skills.md:41`: *"Today two shipped skills (`ship-spec`, `review-pr`) have no `requires:` block … **This is the tracked backlog item.**"*, and the item notes spec-close *"was annotated by VHS-29, when it grew a script and the shell dependency became load-bearing"*. Wiki `decisions/2026-06-14-vhs-18-lint-warn-only-strict-gate.md`: *"Tracked backlog: annotate ship-spec/spec-close/review-pr `requires:` blocks → `--strict` pre-commit hook."* This spec materially deepens review-pr's `shell` / `network` / `vcs-host` surface (six more `gh` fetches plus a PR write).
**Suggested fix:** One clause in Out of scope 2: "…the tracked backlog item at `docs/authoring-portable-skills.md:41` / VHS-18's decision; this change deepens the shell+network surface without declaring it."

### F-11: Keep the new operative prose intent-phrased — don't extend the file's existing §4 drift
**Severity:** P3
**Where:** spec § D2, § D3, § D7 (all new operative prose)
**Convention violated:** `docs/portability-contract.md` §4 case 1 — an operative imperative must not name a harness tool
**Evidence:** `review-pr` already violates this in prose `lint.py` cannot see (it flags `mcp__*` only, per the VHS-18 decision): `skills/review-pr/SKILL.md:11` *"Use the **Bash tool** for these commands"*, `:99` *"using the Read tool"*, `:120` *"using Edit tool"*, `:200` *"individual Bash tool calls"*. The spec adds a large new operative section (2b) plus edits to `:96-107` and 6a/6c without stating the discipline, so an implementer copying the neighbouring style will add more.
**Suggested fix:** Add one line to the Design preamble: the new prose names capabilities, not harness tools (e.g. "read the file at the referenced line" rather than "use the Read tool"); the existing bare names stay untouched (out of scope) but are not extended.

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 5 | P4: 0

STATUS: GREEN
