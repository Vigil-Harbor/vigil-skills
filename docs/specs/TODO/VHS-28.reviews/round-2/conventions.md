# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | D4's "one module-level source" has no home in the file inventory | **CLOSED** | `_sections.py` added at spec.md:33 (Scope/New files); D4 spec.md:122-128 declares its contents; D2 renamed spec.md:69 + fence scoped to entry points spec.md:75 |
| conventions | F-2 | pytest gate vs stdlib-only convention | **CLOSED** | spec.md:304-310 stdlib `unittest discover` only; pytest demoted to operator-local at spec.md:310. Verified against `skills/talaria/SKILL.md:126` |
| conventions | F-3 | D5 notes-heading imperative / missing case-2 tag | **CLOSED** | spec.md:142 carries `or the equivalent in your host`; spec.md:143 is a verbless parenthetical. (Anchor stale — see new F-3) |
| conventions | F-4 | Exit code 2 overloaded | **CLOSED** | D6 table spec.md:162 adds exit `3`; rationale spec.md:164; lint.py divergence named spec.md:168 |
| conventions | F-5 | Name unresolved | **CLOSED** | D11 spec.md:212-218 |
| conventions | F-6 | D8/D5 path asymmetry unstated | **CLOSED** | D8 spec.md:183-186 states project-local-working-state vs harness-config; gitignore claim scoped to this repo |
| conventions | F-7 | AGENTS.md § File layout row departs from last three skills | **CLOSED** | Row dropped (spec.md:45); D12 spec.md:223. Verified: `a0ad847`/`386dc6c`/`8946f58` touch zero AGENTS.md lines. (Evidence sentence overstates — new F-8) |
| conventions | F-8 | peon-ping coexistence departure + `--prune` footgun | **CLOSED** | D9 spec.md:200-202. Both verified: `sync.py:81-84` prune loop; `comprehension/2026-05-06-custom-skills-personal-unlock.md` § Judgment Calls; `README.md:30` repeats the promise |
| conventions | F-9 | `references/` vs `reference/` | **CLOSED** | spec.md:36 + D12 spec.md:222. Precedent verified: `skills/hermes-kanban-awareness/reference/board-schema.md` is the repo's only one |
| conventions | F-10 | talaria convention overstated | **CLOSED** | spec.md:252 "following `skills/talaria/SKILL.md`". Verified `skills/talaria/SKILL.md:124-156` ships Test plan/command into installs |
| conventions | F-11 | Spec-level additions roll-up | **CLOSED** (as agreed: recorded, no edit) | spec.md:341 § Deferred (P2+). Re-walked for v2 — see new F-7 |
| correctness | F-1 | Tripwire + baseline true only on unmerged branch | **CLOSED** | § Preconditions spec.md:10-24; Modified-files row spec.md:44; test-plan 11 spec.md:300 |
| correctness | F-2 | "68 = untouched scaffold" misattribution | **CLOSED** | spec.md:153 now "a **fully-written** handoff, at the template's own heading depths" |
| correctness | F-3 | D9 puts operative `~/.claude/…` in SKILL.md | **CLOSED** | spec.md:194 operative sentence harness-neutral, literal path demoted to a note. (New F-4 covers the AGENTS.md half) |
| correctness | F-4 | Section vocabulary never enumerated | **CLOSED** | spec.md:130 enumerates REQUIRED (3) and RECOMMENDED (6) by name and depth |
| correctness | F-5 | Exit 2 overloaded | **CLOSED** | D6 spec.md:162-164 |
| correctness | F-6 | Span definition self-contradiction | **CLOSED** | D3 consequence 2, spec.md:119, deletes the clause explicitly |
| correctness | F-7 | Fenced blocks not excluded | **CLOSED** | D3 § Fence masking spec.md:97 |
| correctness | F-8 | `--project-path` purposeless | **CLOSED** | spec.md:266 states default, validation, and that it bases both output and `--continues-from` |
| correctness | F-9 | Score formula undefined | **CLOSED (deferred, rationalized)** | spec.md:166 monotonicity-only; recorded spec.md:342 |
| correctness | F-10 | Zero-WARN unverifiable from console | **CLOSED** | test-plan 10 spec.md:299 uses `lint.lint_path`. Verified `lint.py:291` returns non-zero only on ERROR; `tests/test_lint.py:44-46` is the cited shape |
| correctness | F-11 | `tests/fixtures/` never used | **CLOSED** | spec.md:38 + test-plan 5 spec.md:294. (Placement — new F-5) |
| correctness | F-12 | pytest not stdlib | **CLOSED** | spec.md:304-310 |
| correctness | F-13 | "~1,150 lines" is scripts only | **CLOSED** | spec.md:58 "1,147 lines of scripts; ≈1,570 including SKILL.md and references" |
| edge-cases | F-1 (P0) | `section_span` self-contradiction / second matcher | **CLOSED** | spec.md:119 |
| edge-cases | F-2 | No encoding specified (cp1252) | **CLOSED** | § Encoding discipline spec.md:254-260; reads follow `lint._read_lines` (verified `lint.py:63-73`) |
| edge-cases | F-3 | Tripwire anchored to unmerged branch | **CLOSED** | § Preconditions spec.md:10-24 |
| edge-cases | F-4 | Legacy corpus load-bearing but unpinned | **CLOSED** | `tests/fixtures/legacy-handoff.md` spec.md:38; test-plan 5 spec.md:294 |
| edge-cases | F-5 | Matcher unified on depth only | **CLOSED** | D3 spec.md:81-95 pins depth, indent, mandatory separator, closing sequence, case, setext |
| edge-cases | F-6 | Generic `KEY=value` secret class dropped | **CLOSED** | D1 spec.md:65 restores it as "the dominant real-world leak"; test-plan 6 spec.md:295 pins it |
| edge-cases | F-7 | Exit 2 overloaded | **CLOSED** | spec.md:162 |
| edge-cases | F-8 | BLOCKED names pattern but not locus | **CLOSED** | spec.md:170 `<file>:<line>` + redacted excerpt + no short-circuit |
| edge-cases | F-9 | Fences / inline code not excluded | **CLOSED** | spec.md:97; test-plan 2 spec.md:291 |
| edge-cases | F-10 | Last section swallows footer | **CLOSED** | D3 consequence 3 spec.md:120 (thematic-break termination); test-plan 3 spec.md:292 |
| edge-cases | F-11 | `--continues-from` silent degrade + Windows semantics | **CLOSED** | spec.md:270 hard error, `resolve()`d both sides, case-insensitive on Windows, "fresh start" only when flag absent |
| edge-cases | F-12 | No git subprocess timeout | **CLOSED** | spec.md:268 10s timeout, timeout == non-zero exit, three-case placeholder |
| edge-cases | F-13 | Long slug `OSError` | **CLOSED** | spec.md:267 60-char cap, sanitize-then-default ordering; test-plan 8 spec.md:297 |
| edge-cases | F-14 | `$` vs `fullmatch` | **CLOSED** | spec.md:147. Precedent verified: `skills/talaria/scripts/talaria_watch.py:77` `_WATCH_ID_RE.fullmatch` |
| edge-cases | F-15 | Fallback covers "not found" only | **CLOSED** | spec.md:145 arms on absent/unreadable/not-JSONL/too-large; states which case applied |
| edge-cases | F-16 | Non-atomic write + unbounded chain | **CLOSED** | spec.md:271 `os.replace`; spec.md:249 5-hop cap + visited-set |
| edge-cases | F-17 | `--since` on current branch reports "fresh" | **CLOSED** | spec.md:249 branch compare first, outranks commit count, `--all` |
| edge-cases | F-18 | `--project-path` unvalidated | **CLOSED** | spec.md:266 |
| edge-cases | F-19 | Git output unescaped into a table | **CLOSED** | spec.md:269 `-z`, `core.quotepath=false`, pipe/backtick escaping, 10-row cap |
| edge-cases | F-20 | Non-git temp dir shadowed by ancestor repo | **CLOSED** | test-plan 8 spec.md:297 `GIT_CEILING_DIRECTORIES` / scrubbed `GIT_DIR` |
| edge-cases | F-21 | Advisory score recreates threshold pressure | **PARTIAL** | spec.md:166 keeps the score but labels it a non-gate and instructs acting on the verdict/exit code; the finding's stronger option (drop it) was not taken. Rationalized, non-blocking, stays P3 |

No REOPENED items.

## Findings

### F-1: D4's `sys.path` insertion contradicts the repo's only shared-module precedent, which explicitly documents avoiding it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:124 (D4)
**Convention violated:** `skills/talaria/scripts/` — the repo's sole in-repo pattern for one script under `skills/*/scripts/` importing another
**Evidence:** `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/skills/talaria/scripts/talaria_bridge.py:3-4` states the choice as a design decision:

```
This file deliberately avoids HTTP and ``sys.path`` mutation. It locates a
Talaria checkout, verifies it is the Talaria plugin surface ... and imports
Talaria's state/connector modules by file path under synthetic module names.
```

Both consumers implement it the same way — `talaria_read.py:23-32` and `talaria_watch.py:35-45` each carry a `_load_bridge()` built on `importlib.util.spec_from_file_location(module_name, Path(__file__).with_name("talaria_bridge.py"))` with a distinct synthetic module name. The spec instead says "each entry point inserts its own directory on `sys.path` before importing."

Note the spec already knows the underlying constraint — test plan spec.md:288 says scripts load "via an `importlib` `load_script` helper because `skills/*/scripts/` is not an importable package." It solves the same problem two different ways in two places, and picks the non-precedented one for the shipped artifact. `sync.py` mirrors these files byte-for-byte into `~/.claude/skills/`, so the `sys.path[0]` mutation runs in the operator's harness process, not just in tests.
**Suggested fix:** Replace D4's parenthetical with the talaria mechanism — "each entry point loads `_sections.py` by file path via `importlib.util.spec_from_file_location(Path(__file__).with_name('_sections.py'))` under a distinct synthetic module name, following `skills/talaria/scripts/talaria_read.py:23-32`; no `sys.path` mutation, per `talaria_bridge.py:3-4`." If `sys.path` insertion is deliberately preferred, name the departure and why, the way D6 and D9 name theirs.

### F-2: `create_handoff.py`'s § Design entry omits the `_sections` import that `validate_handoff.py`'s carries — the single-source pin is asymmetric where it matters most
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:262-272 (§ Design → `scripts/create_handoff.py`) vs spec.md:276
**Convention violated:** single-source-of-truth — the exact drift class D3/D4 exist to eliminate, and the root cause the ticket was filed for
**Evidence:** spec.md:276 for the validator reads "CLI: `validate_handoff.py <handoff-file>`. Stdlib only. **Imports `_sections`.**" The create entry, spec.md:264, reads only "CLI: `create_handoff.py [slug] …`. Stdlib only." — no import statement. D4 spec.md:126 does say `TEMPLATE_SECTIONS` is "the ordered `(depth, name)` table `create_handoff.py` renders", so the intent is recorded; but § Design is what an implementer reads while writing the file, and there the one script that *renders* the vocabulary is the one whose sourcing is unstated. A hardcoded template table in `create_handoff.py` would satisfy every line of § Design and still fail D4's premise — and test-plan item 4's round-trip cannot see it, because both sides would drift together only if the drift is in the matcher, not in the table.
**Suggested fix:** Make spec.md:264 symmetric: "Stdlib only. **Imports `_sections`; renders `TEMPLATE_SECTIONS` — the section table is never restated in this file.**"

### F-3: D3's `lint.py` citations describe behavior `lint.py` does not implement, and one anchor is stale
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:97 (D3 § Fence masking), spec.md:142 (D5 step 1)
**Convention violated:** AGENTS.md § Plan & Spec Reviews — "Always verify load-bearing claims against the actual codebase … and current file state"; the same discipline applies to the spec's own citations, since an implementer will open the cited lines and copy what is there
**Evidence:** three separate problems, all in citations to `lint.py`:

1. spec.md:97 says fence masking blanks "lines between **matching** ``` / ~~~ fences … following `lint.py`'s `_FENCE_RE` handling (`lint.py:55, 209-215`)". `lint.py:211-213` is an unconditional toggle — `if _FENCE_RE.match(stripped): in_fence = not in_fence` — against `_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")` (`lint.py:55`). It pairs nothing: it does not track the opening fence's character, its length, or its indent. An implementer told to "follow lint.py's handling" gets a toggle, not matched fences — and the spec's own requirement is the stricter one.
2. spec.md:142 cites `lint.py:52` for `_CASE2_TAG = "or the equivalent"`. The actual line is **`lint.py:60`**.
3. Unstated but real: D3's matcher deliberately diverges from `lint.py`'s own heading handling in the opposite direction. `lint.py:58` is `_HEADING_STRIP_RE = re.compile(r"^#{1,6}\s*")` — no mandatory separator (so `##Foo` is a heading there) and no 0-3-space indent limit. D3 spends five bullets making both of those hard rules without noting it is intentionally stricter than the sibling file it otherwise cites as the pattern source.

**Suggested fix:** At spec.md:97, reword to "…**extending** `lint.py`'s fence toggle (`lint.py:55, 211-213`) to require a closer matching the opener's character and length, since a handoff body can legitimately nest one fence style inside another." Correct spec.md:142 to `lint.py:60`. Add one sentence to D3 noting the matcher is deliberately stricter than `lint.py:58`'s `_HEADING_STRIP_RE`, which serves a different purpose (prefix stripping, not span location).

### F-4: The AGENTS.md uninstall command drops the file's own harness qualifier and is POSIX-only on a PowerShell-primary machine
**Severity:** P3
**Where:** spec.md:195 (D9, recorded place 2)
**Convention violated:** `AGENTS.md` § header — "Harness-neutral by intent — written for Claude Code, Hermes, or any agent that reads an `AGENTS.md`" — and its established practice of qualifying Claude-Code-specific paths
**Evidence:** AGENTS.md § What this repo is writes the same directory as "installed into your agent's config dir (**for Claude Code:** `~/.claude/skills/` and `~/.claude/agents/`)". Every literal `~/.claude` in AGENTS.md today either sits behind that qualifier or inside a `sync.py` flag description. D9 prescribes the bare literal `rm -rf ~/.claude/skills/agentcraft-handoff/` with no qualifier. Separately, the operator machine's primary shell is PowerShell, where `rm -rf` is a parse error (`Remove-Item -Recurse -Force` is the equivalent) — and D9's own `--prune` warning exists precisely because a mis-executed removal here is destructive of 14 third-party skills.
**Suggested fix:** Specify the AGENTS.md entry as harness-qualified and dual-shell: "For Claude Code, remove the vendor copy from the skill dir — `rm -rf ~/.claude/skills/agentcraft-handoff/` (PowerShell: `Remove-Item -Recurse -Force ~/.claude/skills/agentcraft-handoff/`)." One line, and it keeps AGENTS.md's own stated neutrality intact.

### F-5: `tests/fixtures/` is a single-purpose lint corpus today; the new fixture lands flat inside it unnamespaced
**Severity:** P3
**Where:** spec.md:38 (Scope/New files), spec.md:294 (test-plan 5)
**Convention violated:** repo fixture organization; wiki `projects/vigil-skills/filemap.md:143` documents the directory as one unit — "`tests/test_lint.py` + `tests/fixtures/`"
**Evidence:** every current entry is a `lint.py` fixture — `bad-skill/`, `good-skill/`, `bom-skill/`, `crlf-skill/`, `indented-fence/`, `notes-bare-name/`, `split-marker/`, plus flat `comment-in-requires.md`, `tab-indent.md`, `empty.md`, `no-frontmatter.md`, `unterminated-frontmatter.md`, `inline-requires-mapping.md`. `legacy-handoff.md` sitting flat among them reads as a thirteenth lint fixture. Verified non-breaking: `tests/test_lint.py:63-77` enumerates fixture names explicitly rather than sweeping the directory, so an added file cannot be picked up by the lint suite — this is organizational, not a bug.
**Suggested fix:** Move it to `tests/fixtures/session-handoff/legacy-handoff.md` (matching the existing subdirectory grouping) and add one line to spec.md:38 noting that root `.gitattributes` (`*.md text eol=lf`) already normalizes it, so — unlike `tests/fixtures/.gitattributes`'s byte-exact `-text` entries for `crlf-skill/`, `bom-skill/`, `empty.md`, `tab-indent.md` — no `-text` entry is needed. That pre-empts the "DRIFT: 1 — fixtures `.gitattributes`" outcome VHS-18 hit (`state.md`, VHS-18 entry).

### F-6: § Test command uses bare `python` where spec-cycle's own authoring guidance asks for a pinned interpreter
**Severity:** P3
**Where:** spec.md:304-308
**Convention violated:** `skills/spec-cycle/SKILL.md` Phase 1 § Test command bullet, restated at `skills/ship-spec/SKILL.md:44`
**Evidence:** spec-cycle Phase 1 says "Pin the interpreter explicitly (e.g., `<full-path-to-python> -m pytest <files>`) when the project has multiple Python installs on PATH (common on Windows)." This repo has demonstrably run its suite under at least three: `skills/talaria/scripts/__pycache__/` holds `talaria_bridge.cpython-310.pyc`, `-311.pyc`, and `-314.pyc`. The talaria precedent the spec otherwise follows closely uses `${HERMES_PYTHON:-python}` rather than a bare `python` (`skills/talaria/SKILL.md:145-147`) — a pin with a default, not no pin.
**Suggested fix:** Either pin the interpreter, or add one sentence below spec.md:308: "`python` must be the same interpreter the rest of the suite runs under; pin it by full path if more than one is on PATH (see `skills/spec-cycle/SKILL.md` Phase 1)." Do not import `${HERMES_PYTHON:-python}` — that variable is talaria/Hermes-specific and would be its own drift here.

### F-7: Spec-level additions new in v2 that the brief and ticket do not explicitly authorize (drift-check visibility)
**Severity:** P3
**Where:** spec.md:10-24, spec.md:95, spec.md:218, spec.md:222, spec.md:337
**Convention violated:** none — this is the (c)-class roll-up the drift-check needs to see, the successor to round-1 conventions/F-11
**Evidence:** I walked v2's new material against `VHS-28.brief.md`. **No (d) items — nothing is a silent addition.** Every one carries explicit rationale:

- **§ Preconditions** (spec.md:10-24), including "Preferred resolution: land the three commits above on `main` first" — prescribes an action on `main` outside this spec's diff. Rationalized and fenced at spec.md:337. Structurally this has precedent: `docs/specs/DONE/VHS-19/spec.md:13` carries an analogous "## Repo topology & where the work lands (read this first)" implementer-orientation section, so a spec in this repo carrying a Preconditions section is squarely in convention. Note it is time-sensitive prose that goes stale the moment `386dc6c`/`8946f58`/`7a3a929` land — which is fine, since spec.md:23 already tells the implementer to read the file rather than trust the literal.
- **`reference/` singular** (spec.md:36, D12 spec.md:222) — this overrides a **literal brief line**: `VHS-28.brief.md:30` writes "**`references/handoff-template.md`**". D12 states the override with rationale and the precedent checks out, so it is (c) not (d) — but it is the one place v2 contradicts brief text rather than merely adding to it, and the drift-check should see it named.
- **Setext headings unsupported** (spec.md:95), **D11's coexistence tie-break** (spec.md:218), **the advisory score's monotonicity-only contract** (spec.md:166, recorded spec.md:342) — all (c), all rationalized.
- Everything else new in v2 (encoding discipline, atomic write, subprocess timeouts, `fullmatch`, 5-hop chain cap, `GIT_CEILING_DIRECTORIES`, exit `3`, 256 KB bound, 60-char slug cap) traces to a round-1 finding, i.e. authorized by review.

**Suggested fix:** None required — recorded for the Phase 3 drift-check. If anything is folded at 2g, the `reference/` singular override of brief:30 is the item worth a human eye.

### F-8: D12's stated rationale for dropping the § File layout row is partly inaccurate
**Severity:** P4
**Where:** spec.md:223
**Convention violated:** none — evidence accuracy only
**Evidence:** D12 says "the file adds per-skill rows only for unusual artifacts (`skills/ship-spec/states.json`)." AGENTS.md § File layout also carries a plain row for `skills/spec-close/SKILL.md` — an entirely ordinary artifact already covered by the generic `skills/<name>/SKILL.md` row above it. The *conclusion* is verified and correct: `git show --stat` for `a0ad847` (talaria), `386dc6c` (bloat-check), and `8946f58` (hermes-kanban-awareness) shows none of the three touched `AGENTS.md`.
**Suggested fix:** Trim to the verified claim: "the last three skills to ship each added a skill without touching `AGENTS.md`; the one per-skill row for an unusual artifact is `skills/ship-spec/states.json`, and `session-handoff` ships nothing unusual."

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 4 | P4: 1

STATUS: GREEN
