# VHS-28 — `session-handoff` skill (clean-room), superseding `agentcraft-handoff`

**Brief:** `docs/specs/TODO/VHS-28.brief.md` · **Plane:** VHS-28 · **Namespace:** `skills`
**Spec round:** v7 (delta patch of round-6 findings) · **Authored:** 2026-08-23 · **Revised:** 2026-08-24

## Goal

Ship a tracked, portable **`session-handoff`** skill under `skills/session-handoff/` that fully replaces the AgentCraft-managed `agentcraft-handoff`. The skill scaffolds, validates, resumes, and chains session handoff documents. It is written clean-room, declares `requires:` per the portability contract, is covered by `tests/test_session_handoff.py`, and installs through `sync.py` like every other skill here. The validator bug VHS-28 was filed for — heading patterns capped at `##`, so no `###` section could ever be seen — is eliminated structurally: one heading matcher in one shared module, matching **by name at any depth**, pinned by tests against a generated scaffold and both shapes of legacy on-disk document.

## D0 — Scope-down: the validator does not parse markdown *(new in v4; read this first)*

Rounds 1–3 converged on a design that needed a CommonMark-subset parser — fence pairing, inline-span backtick runs, thematic breaks, setext underlines, length-preserving masking, a masked-vs-normalized string split. Three review rounds produced 19 blocking findings, most of them in that machinery rather than in the feature. v4 removes the machinery instead of specifying it further.

**Why a parser is not an option here.** The repo has no dependency manifest, every import in every shipped script is stdlib, and `sync.py` distributes skills by copying files into the harness skill dir with no install step — so a third-party parser would `ImportError` on every operator machine, and the `requires:` schema (`docs/portability-contract.md` §3) has no key to declare one. Vendoring one into this tree is the same call `decisions/2026-06-15-vhs-19-fork-and-own-converter.md` already made — "**Carry the engine into vigil-skills.** Rejected: breaks the stdlib-only/no-build contract" — and `docs/portability-contract.md` §3 states the constraint normatively.

**Why a parser is not needed.** Every piece of that machinery existed to protect **one** check: the ≥50-character completeness measurement. Fence masking existed so code blocks would not truncate a section's measured length. The subtree fallback existed so container sections measured something. The masked/normalized split existed so the arithmetic landed on the right string.

**So the ≥50-character check is removed.** `create_handoff.py` emits a `[TODO: …]` marker into exactly the sections classed `required` or `recommended` in D4's table — including `Files Modified`, whose paths git fills but whose commentary the author writes — and into no others (see § `create_handoff.py`), so *"did the author replace the placeholder"* answers completeness for a scaffolded document — better than a character count, which a padded sentence satisfies and a terse-but-complete section fails.

**What that buys, structurally:** with no length measurement, section *content* is never measured, so nothing downstream depends on where a section ends. The validator asks only whether each required heading is **present**. A `#` line inside a fenced block therefore cannot shorten, truncate, or hide anything — the worst it can do is invent a heading that no required name matches. Fence masking, inline-span masking, thematic-break termination, the leaf invariant, and the subtree fallback all become unreachable code, and are cut.

**Accepted limits, recorded deliberately:**

- A `[TODO: …]` quoted inside a code block or inline span still trips the TODO check. Visible, clearable by rewording, and rare — the marker shape is distinctive. This is the one place masking bought something real, and it is not worth a parser.
- **A required section name on any line starting with 1–6 `#` satisfies that presence check** — including inside a fenced block, an indented block, or an HTML comment. A handoff that quotes another handoff will hit this, which is not exotic in a skill whose subject *is* handoffs. It is a false *pass*, never a false fail, and the author is the person reading the verdict.
- **Completeness is checked only where a marker survives.** A section whose placeholder was *deleted* rather than replaced, or left empty under a present heading, validates `READY`. The removed ≥50-character check caught that; the marker scan cannot.
- **A document this skill did not scaffold gets presence checking only.** All 23 documents in the on-disk corpus carry zero `[TODO:` markers, so for every one of them — and for both legacy fixtures in test item 3 — the completeness half is a no-op. The marker scan answers completeness for the window between generation and first edit, on documents `create_handoff.py` produced; it is an author's checklist, not an adversarial validator, and D8's commitment to reading existing documents is what makes that acceptable.
- An empty heading is a heading when followed by whitespace (`## `) and not when bare (`##`). Neither can match a vocabulary name, so no verdict depends on it.

## Preconditions

**Hard gate — do not cut the implementation worktree until this is satisfied.** `/ship-spec` cuts from `origin/<default-branch>` (`skills/ship-spec/SKILL.md:76`), which is not the tree this spec was authored against.

| Ref | `skills/*/SKILL.md` present | `tests/test_lint.py` asserts | Suite state |
|---|---|---|---|
| `origin/main` (`a0ad847`, 2026-06-28) | 5 | `len(skills), 4` | **red** — fails 5 ≠ 4 |
| `feat/tal-003-talaria-skill` (local, 8 ahead) | 7 | `len(skills), 7` | green |

`main` has been red since talaria merged. The fix lives in `386dc6c`, `8946f58` and `7a3a929`, interleaved with five other commits on `feat/tal-003-talaria-skill` — not independently cherry-pickable.

**The gate:** merge that branch's PR to `main` first, then cut the worktree. The tripwire edit is then a clean `7 → 8`.

**Verification, not a fallback:** on entering the worktree, confirm `tests/test_lint.py` reads `len(skills), 7` and that `skills/*/SKILL.md` numbers 7. If not, **stop and resolve the baseline** — do not compute a local value. Proceeding on the unfixed base would put three candidate values (`4`, `6`, `7`) in flight on one line and absorb half of `7a3a929`'s fix into this diff.

## Scope

### New files

| Path | Purpose |
|---|---|
| `skills/session-handoff/SKILL.md` | Skill definition: frontmatter + the three mode workflows |
| `skills/session-handoff/scripts/_sections.py` | **Shared** vocabulary, heading matcher, normalizer — the single source D3/D4 pin |
| `skills/session-handoff/scripts/create_handoff.py` | Scaffold a pre-filled handoff document |
| `skills/session-handoff/scripts/validate_handoff.py` | Presence + TODO + secret gate |
| `skills/session-handoff/reference/handoff-template.md` | Section structure, annotated (singular `reference/` — D12) |
| `tests/test_session_handoff.py` | Regression suite (repo root `tests/`, **not** inside the skill dir) |
| `tests/fixtures/session-handoff/legacy-flat.md` | Authored fixture, all-`##` shape |
| `tests/fixtures/session-handoff/legacy-nested.md` | Authored fixture, `##`/`###` shape |

Both fixtures go in a `session-handoff/` subdirectory: `tests/fixtures/` is otherwise entirely a `lint.py` corpus. Root `.gitattributes` (`*.md text eol=lf`) already normalizes them, so **no `-text` entry is needed** and none should be added.

### Modified files

| Path | Change |
|---|---|
| `tests/test_lint.py` | Bump the shipped-skill tripwire `7 → 8` (verify, don't assume — see Preconditions) |
| `AGENTS.md` | A § Superseded vendor skills note carrying the uninstall step (D9). **No § File layout row** — D12 |

### Left alone

- `sync.py` — `SUBTREES = ("skills", "agents")`, `iter_files` uses `rglob("*")`, so `scripts/` and `reference/` mirror automatically. *(That `rglob` is unfiltered, so `scripts/__pycache__/*.pyc` also mirrors and then reads as a `dst_files - src_files` entry `--prune` would delete. Pre-existing — `skills/talaria/scripts/__pycache__/` already does this — and part of why D9 warns off `--prune`.)*
- `lint.py`, `README.md`, `~/.claude/skills/agentcraft-handoff/` (deleted wholesale per D9, never edited), every other skill.

## Decisions

### D1 — Clean-room rewrite, not a port

No file, function body, docstring, or template prose is copied from `~/.claude/skills/agentcraft-handoff/` (1,147 lines of scripts; ≈1,570 including SKILL.md and references). That tree is a *behavioral* reference.

**Rationale.** `vigil-skills` is public; importing a vendor-managed skill wholesale is redistribution with unclear provenance.

**Two bounded carry-forwards, both schema rather than expression:**

1. **Secret-detection patterns** — credential *formats* are facts, not authored expression:
   - **Generic assignment shapes** — `(api[_-]?key|secret|password|passwd|token|private[_-]?key|client[_-]?secret)\s*[:=]\s*<value>`, minimum value length ≥8 (≥20 for `token`) to keep prose out. **The dominant real-world leak.**
   - **Branded prefixes at current widths** — `sk-[A-Za-z0-9_-]{20,}` (covers `sk-ant-api03-…`/`sk-proj-…`; a `{48}` alphanumeric-only pattern misses Anthropic keys), `gh[pousr]_[A-Za-z0-9]{36,}`, `github_pat_[A-Za-z0-9_]{20,}`, `xox[baprs]-[A-Za-z0-9-]+`, PEM `-----BEGIN … PRIVATE KEY-----`, DSN-with-password forms.
2. **Section names (D4)** — the nine `REQUIRED ∪ RECOMMENDED` names are the schema of documents already on disk. **Every row not classed `required` or `recommended` is rendered from `create_handoff.py`'s own constants and never matched or validated** — so the implementer names those headings freely, whether the table shows a title for them or leaves them anonymous.

### D2 — Two entry points, not four scripts

`create_handoff.py` and `validate_handoff.py` are the executable entry points. `list_handoffs.py` and `check_staleness.py` do not ship; listing and staleness are prompt-driven steps in RESUME, because "show me the handoffs and how stale this one is" is a directory listing plus `git log`, which an agent interprets better than a fixed ladder.

The fence counts **entry points**, not modules. `_sections.py` is a shared module, not a third command.

### D3 — One heading matcher, in one shared module (the actual fix)

The vendor built its heading pattern in three places and they diverged on **two** axes — depth (`##?`) and separator (opener `\s*`, terminator `\s+`). So the matcher is specified once, in `_sections.py`.

**Text normalization is a precondition, not a fallback.** All matching operates on: `read_bytes()` → `decode("utf-8", errors="replace")` → strip leading BOM → `text.replace("\r\n", "\n").replace("\r", "\n")`. No `\r` appears in any matcher, because none can reach one.

The newline step is load-bearing. Under `re.MULTILINE`, `$` matches only before `\n`, so on `"## Current State Summary\r\n"` the `\r` is absorbed into the title group, the name comparison fails, and the section reports **`missing`** — the ticket's headline symptom, reproduced by the fix meant to remove it. Measured: `MCP Server/.claude/handoffs/2026-08-15-060410-mcp-45-post-merge.md` is CRLF and all three of its required sections fail that way. `lint._read_lines` (`lint.py:63-73`) is CRLF-safe only because it ends in `.splitlines()`; a whole-document matcher inherits none of that.

**Why `_sections.py` cannot import `lint.py`:** `sync.py` mirrors only `skills/` and `agents/`, so `lint.py` does not exist beside the installed skill. Regex shapes are reproduced deliberately, not copied for convenience.

```python
_HEADING_RE = re.compile(
    r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$",   # depth, title
    re.MULTILINE,
)
```

Semantics, stated so no call site re-decides them:

- **Depths 1–6.** Seven or more `#` is not a heading.
- **0–3 leading spaces** permitted (CommonMark); 4+ is an indented code block.
- **A space or tab after the hashes is mandatory** — `#hashtag` and `##Foo` are not headings. This closes the vendor's "opens on a non-heading, never closes" hole.
- **An optional ATX closing sequence** (`## Title ##`) is stripped from the captured title. (A title genuinely ending in `#`, e.g. `Interop with C#`, would lose it — recorded as a deliberate simplification; no vocabulary name is affected.)
- **The captured title is `.strip()`ed, then compared case-insensitively by name** — never by interpolating the name into a regex, which is what created the substring-collision failure.
- **Setext headings are not recognized.** The template emits ATX only.

**Presence is the only question asked.** Per D0 there is no content measurement, so `_sections.py` exposes four public callables:

```python
def normalize(raw: bytes) -> str:
    r"""Decode utf-8 with errors='replace', strip a leading BOM, and fold
    \r\n and lone \r to \n. Every other function here takes this output.

    Raw string deliberately: this docstring *documents* the escapes, so it
    must not contain them — in a module whose thesis is that a stray \r
    breaks matching, shipping one inside its own normalizer would be poor.
    """

def has_section(normalized: str, name: str) -> bool:
    """True if any ATX heading at ANY depth 1-6 has this title.

    Lookup is BY NAME ONLY; depth never participates. Measured across the five
    documents in MCP Server/.claude/handoffs/, three are fully flattened to `##`
    and two use `##`/`###` — so a lookup keyed on (depth, name) would report two
    required sections `missing` on 60% of that corpus, which is a depth bug, i.e.
    precisely the defect VHS-28 was filed for.
    """

def first_heading_title(normalized: str) -> str | None:
    """The first depth-1 heading's title, or None.

    None covers BOTH "no depth-1 heading" and "the heading is empty" — `# `
    alone is a heading per D0's accepted limits and its title group captures
    '', so the empty title is normalized to None here rather than leaving
    callers to discover that '' is not None.
    Public so `create_handoff.py` never touches `_HEADING_RE` itself (D4).
    """

def todo_marker(name: str) -> str:
    """The `[TODO: ...]` text for a section. `TODO_MARKER_RE` matches exactly
    what this emits — one producer, one matcher, one module.

    Returns `f"[TODO: {name} — <guidance>]"`. **The section name appears
    verbatim**, which is what makes `todo_marker(name) in text` a valid way to
    locate one section's marker: D0 removed every sectioning mechanism, so a
    constant marker string would collapse test item 2's per-row assertion into
    a bare count of nine that cannot tell nine right sections from one.
    """
```

No `section_span`, no terminator rule, no masking. `normalize`, `has_section`, `first_heading_title`, `todo_marker`, `TODO_MARKER_RE` and the name tables are the module's whole public surface; only `_HEADING_RE` stays private to it.

### D4 — One vocabulary, shared by file-path import

`_sections.py` declares `TEMPLATE_SECTIONS` (an ordered table of `(depth, name, cls)` triples), `REQUIRED_SECTIONS` and `RECOMMENDED_SECTIONS` (both **derived** from `cls`, not written out), the shared `TODO_MARKER_RE`, the private `_HEADING_RE`, and the four public callables `normalize()`, `has_section()`, `first_heading_title()`, `todo_marker()`.

**`TODO_MARKER_RE` lives here, not in either entry point.** Since D0 makes the placeholder scan the *whole* completeness gate, the marker is now a load-bearing shared string — exactly the "one matcher, several places, diverging" shape VHS-28 was filed for. It is `re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)`, and it is **public, because both entry points use it**: `create_handoff.py` renders through `todo_marker()` and `validate_handoff.py` scans with this same object. Declaring it private while two modules share it would push the validator into either reaching past an underscore or re-declaring the pattern — and the second is "one matcher, two places, diverging" on the single token D0 made the entire completeness gate.

**Both entry points load it by file path**, following the repo's only precedent (`talaria_read.py:23-32`; `talaria_watch.py:33-42`), which is the full loader shape — `spec_from_file_location` alone loads nothing:

```python
spec = importlib.util.spec_from_file_location(
    "_session_handoff_sections", Path(__file__).resolve().with_name("_sections.py")
)
if spec is None or spec.loader is None:
    raise ImportError("cannot load _sections.py")
module = importlib.util.module_from_spec(spec)
sys.modules["_session_handoff_sections"] = module
spec.loader.exec_module(module)
```

**No `sys.path` mutation** — `talaria_bridge.py:4-5` states that choice explicitly, and `sync.py` mirrors these files into the operator's harness dir, where a module-level insert would run in their process and persist.

Both entry points use the **same** synthetic name — deliberately unlike talaria's per-consumer names, so the module is shared where it can be. Tests compare `TEMPLATE_SECTIONS` **by value, never by identity**, since `load_script` pops `sys.modules` between loads.

**`TEMPLATE_SECTIONS`** — an ordered `(depth, name, cls)` table, where `cls` is exactly the table's third column: one of `title` / `container` / `generated` / `required` / `recommended` / `chain`. **Depth governs rendering only; `cls` governs behavior.** `name` is `None` on the title row and on the three anonymous `*(container)*` rows — every heading whose row is not classed `required` or `recommended` is the implementer's choice per D1, named or anonymous alike:

| Depth | Name | Class |
|---|---|---|
| `#` | *(document title)* | title |
| `##` | Session Metadata | container |
| `###` | Recent Commits | generated |
| `##` | Current State Summary | **required** |
| `##` | *(container)* | container |
| `###` | Architecture Overview | recommended |
| `###` | Critical Files | recommended |
| `##` | *(container)* | container |
| `###` | Files Modified | recommended |
| `###` | Decisions Made | recommended |
| `##` | Pending Work | container |
| `###` | Immediate Next Steps | **required** |
| `##` | *(container)* | container |
| `###` | Important Context | **required** |
| `###` | Assumptions Made | recommended |
| `###` | Potential Gotchas | recommended |
| `##` | Handoff Chain | chain |

`REQUIRED_SECTIONS` and `RECOMMENDED_SECTIONS` are **derived from the class column, never written out a second time** — `tuple(n for _, n, c in TEMPLATE_SECTIONS if c == "required")` and the `recommended` equivalent. Restating them by hand would encode the same fact twice inside the one module whose thesis is that duplicated schema diverges. They evaluate to `Current State Summary` / `Important Context` / `Immediate Next Steps`, and to the six rows marked recommended.

**Every row carries a class, and the class — not the name — drives behavior.** Two rules key off it, and nothing keys off whether a name is present:

- **Markers** go into exactly the rows classed `required` or `recommended` (§ `create_handoff.py`).
- **Test item 2's drift assertion** compares against `[name for _, name, cls in TEMPLATE_SECTIONS if cls in ("required", "recommended")]` — the nine matched names, in order.

That keeps D1's promise intact: the `title`, `container`, `generated` and `chain` rows are rendered from `create_handoff.py`'s own constants, are never matched by any validator check and are never pinned by any test — so an implementer really is free to name them, or to rename `Pending Work`, without failing their own suite. The three anonymous `*(container)*` rows are anonymous *because* nothing depends on their titles, not because a named container row is somehow different.

**The title row is filled as `# Handoff: <slug, hyphens replaced by spaces>`.** No `--title` argument is added — the slug is the title, which keeps the CLI at three arguments and means a *generated* document's title is always ASCII, drawn from `Handoff: ` plus `[a-z0-9 ]`, and ≤69 characters — inside the 80-character truncation below, and containing neither `|` nor a backtick. D3's `first_heading_title` reads exactly this line.

**That bounds generated predecessors only.** `--continues-from` may point at a legacy or hand-authored document, whose H1 can carry anything — so the chain block escapes **unconditionally**, and test item 8's `|`/backtick/200-character case uses a hand-written predecessor the test writes into the temp handoffs directory, which a generated document could never be.

**No leaf invariant.** It existed to protect the length measurement; with D0 there is nothing to protect, and arbitrary documents may nest freely.

**Structural prevention of a duplicated table** is the § `create_handoff.py` rule that the table is never restated — not a test. Test item 2's round-trip *detects drift* in an inlined copy; it does not prevent one.

### D5 — Session transfer: declared, portable, bounded, degradable

1. **Operative imperative (the only executed instruction):** "Locate the transcript for the given session id in this harness's session store, or the equivalent in your host." — the repo's canonical §4 case-2 tag (`lint.py:60`).
2. **Non-operative example, no imperative verb:** *(e.g. Claude Code keeps session transcripts under `~/.claude/projects/**/<session-id>.jsonl`.)*
3. **Bounded read.** Seek to `max(0, size - 256*1024)`, read to EOF, decode with `errors="replace"`; **discard the first line if the read did not start at byte 0** — in a tail read the partial record is the *first* line; and discard the final line if it does not parse as JSON, since a live writer may be mid-append. Measured: 4,178 transcripts, 3.13 GB, largest 39.6 MB.
4. **Mandatory fallback, widely armed.** Triggers when the transcript is missing **or unusable** — absent, unreadable, not valid JSONL, or too large. Fall back to `git status`, `git log --oneline -10`, newest document in `.claude/handoffs/`; summarize; **state plainly which case applied**. Never fail; never interrogate the user.

**Input validation.** `re.fullmatch` against `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` **before any filesystem lookup**. `fullmatch`, not `$`: `$` also matches before a trailing newline, so `"<uuid>\n"` from `$(cat id.txt)` would reach glob expansion. Mirrors `talaria_watch.py:23,77`. A non-matching argument is a task slug for CREATE, never a path fragment.

### D6 — The gate is a verdict, not a score threshold

The vendor gate was "score ≥ 70 and no secrets". The ticket measured a **fully-written** handoff at the template's own depths scoring **68** — unclearable regardless of content, rising to 80 once the regex was fixed. A threshold nobody can clear teaches authors to flatten headings until the number moves.

| Verdict | Condition | Exit |
|---|---|---|
| `READY` | all three required headings present, no `[TODO: …]` remains, no secret matched | `0` |
| `NEEDS WORK` | a required heading absent, or a `[TODO: …]` remains | `1` |
| `BLOCKED` | any secret pattern matched (outranks the above) | `2` |
| *(not a verdict)* | missing / unreadable file, or no argument — message on **stderr** | `3` |

**Exit `2` means secrets and nothing else** — otherwise a caller cannot tell "this contains a credential" from "you typed the wrong filename".

**No advisory score.** It existed to summarize the length measurement D0 removed. Recommended-section gaps print as informational lines and change nothing.

**The TODO scan is whole-document, and a marker left in a *recommended* section is therefore `NEEDS WORK` too.** That is deliberate, and it is stated here so authors learn the rule rather than discover it: a *missing* recommended section is informational, but a recommended section still holding its placeholder is unfinished work. The asymmetry does create one perverse incentive — deleting `### Potential Gotchas` outright ships green where leaving an honest empty one does not — and scoping the scan per-section would need the sectioning D0 refuses. Accepted, and recorded next to the incentive it creates.

**No metadata exemption.** v3 carved the generic assignment class out of an "auto-generated metadata block"; two lenses independently rated that a P1, because `validate_handoff.py` receives only a file path and cannot observe provenance, so the region had to be a structural proxy an author could write themselves — a security gate whose exemption region is authored content. **Nothing is exempt.** If a commit subject carries `client_secret = <20 chars>`, that is a real credential in real git history and blocking is the correct outcome, not a false positive. The remedy is documented in CREATE: the locus and redacted excerpt identify the line; edit it and re-validate.

**Deliberate divergence from `lint.py`.** `lint.py` is warn-only by default and gates only under `--strict`, because it carries a `missing-requires` migration backlog to grandfather. `validate_handoff.py` is greenfield, so it gates on first run.

**Report content — every finding carries a locus:** `<file>:<line>`, the matched pattern name, and a **redacted excerpt of the matched value** (never the whole line). Redaction is first-4 + last-4 with the middle masked **only when the value exceeds 12 characters**; at 12 or fewer the excerpt is `<pattern-name>, N chars, fully masked` — first-4/last-4 on an 8-character value reproduces it in full, and the locus already tells the author where to look. All violations print before the verdict; no short-circuit.

### D7 — The file-reference check is dropped, deliberately

Bounded by the brief's fence, which permits dropping and forbids *solving*. On the document that surfaced VHS-28 it produced five warnings, all false — noise that trains the reader to skim the block where secret findings also live. No path-classification logic is written.

### D8 — Storage location and naming unchanged

`<project-path>/.claude/handoffs/YYYY-MM-DD-HHMMSS-<slug>.md`. Existing documents stay readable (pinned by both fixtures).

**The §2 asymmetry, stated.** D5 keeps `~/.claude/projects/` non-operative, so making `.claude/handoffs/` operative needs a distinction: **this path is project-local working state, not harness config.** A harness needing to relocate it uses `--project-path`, not a fork. `.claude/` is gitignored **in this repo**; the skill writes into whatever project it runs in, where that may not hold.

### D9 — Supersession is an operator step, recorded in tracked files

`ship-spec` PRs this repo; it cannot touch `~/.claude/`.

1. `skills/session-handoff/SKILL.md` § *Superseding a previously installed handoff skill* — operative sentence **harness-neutral** ("remove any previously installed vendor handoff skill from this harness's skill directory"), literal path as a non-operative note. D5 exiles `~/.claude/projects/**` from this same portable body; an uninstall command naming `~/.claude/skills/agentcraft-handoff/` is the same §2 violation, and `lint.py` would not catch it.
2. `AGENTS.md` § *Superseded vendor skills* — machine-facing, **harness-qualified and dual-shell**, matching AGENTS.md:7's own "for Claude Code: `~/.claude/skills/`":

   > For Claude Code, remove the vendor copy from the skill dir — `rm -rf ~/.claude/skills/agentcraft-handoff/` (PowerShell: `Remove-Item -Recurse -Force ~/.claude/skills/agentcraft-handoff/`).

**Not `CLAUDE.md`** (gitignored, ships in no PR) and not the PR description (not tracked).

**Two warnings the AGENTS.md entry must carry:**

- **Targeted removal only.** Not `python sync.py install --prune`: it queues a delete for every `dst_files - src_files` path under `skills/` (`sync.py:81-84`), and `~/.claude/skills/` holds 14 third-party skills.
- **This departs from recorded practice, deliberately.** The wiki records that third-party skills coexist preserved (`comprehension/2026-05-06-custom-skills-personal-unlock.md`), a promise `README.md:30` repeats. Deleting is right *here* because this copy is broken and superseded, unlike functioning software like peon-ping — the departure is named, not silent.

**If AgentCraft restores its copy.** Expected, non-fatal; re-run the targeted removal. We do not fight the vendor's installer and do not edit vendor-managed files.

### D10 — Scale is a recorded non-factor

The brief declares `**Factor:** no`. **No batching, pagination, caching, or concurrency machinery.** Four things are **durability, not scale**: atomic write, the 10-second git timeout, D5's 256 KB bounded read, and the 5-hop chain cap. Each bounds one operation's failure mode.

### D11 — Name: `session-handoff`

Harness-neutral, describes the artifact rather than a UI. The `description` **deliberately claims all five trigger phrasings** the vendor advertised, because after the uninstall they must route somewhere. During coexistence the host picks by description match; ours is the more specific. The hard remedy is D9's removal, not a naming trick.

### D12 — In-repo consistency calls

- **`reference/`, singular.** The repo's only precedent is `skills/hermes-kanban-awareness/reference/`. This **overrides the brief**, which writes `references/` at brief:30 — one of two places this spec contradicts brief text rather than extending it (the other, larger one is D0; see § Deferred).
- **No `AGENTS.md` § File layout row.** The file's rows are inconsistent — `skills/spec-close/SKILL.md` has an ordinary one (`AGENTS.md:54`) while the last three skills to ship added none (`a0ad847`, `386dc6c`, `8946f58`). **And no `README.md` § Skills entry either** — that list is 3-of-7 stale (`README.md:9-11` names only `/spec-cycle`, `/ship-spec`, `/review-pr`) and none of the last four skills added one. The § Superseded vendor skills entry stays: genuinely new information, required by brief done-when #5.

## Design

### `SKILL.md`

```yaml
---
name: session-handoff
description: >
  Save and restore working context across sessions. Creates a validated handoff
  document capturing state, decisions, and next steps; resumes from one; or picks
  up directly from a prior session id. Use when the user says "create handoff",
  "save state", "load handoff", "resume from", "continue where we left off", or
  when context is filling up and work must survive the session boundary.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
---
```

Body sections:

1. **Mode selection** — UUID argument (D5's `fullmatch`) → SESSION TRANSFER; save/pause intent → CREATE; resume/load intent → RESUME.
2. **CREATE** — `create_handoff.py [slug] [--continues-from <file>] [--project-path <dir>]` (slug omitted or empty → `handoff`), fill every `[TODO: …]`, `validate_handoff.py <file>`, report path + verdict + first next action. **Act on the verdict and exit code.** Do not finalize on `BLOCKED`; the locus and redacted excerpt identify the line — edit it and re-validate, including when the match is in a generated commit subject (a credential in git history is a real finding).
3. **RESUME** —
   - List `*.md` in `<project-path>/.claude/handoffs/`, newest first; **ignore `*.tmp`**. **If the directory is absent or holds no `*.md`, say so plainly and offer CREATE — do not prompt for a path**, matching D5's never-interrogate posture.
   - **Compare the recorded branch against the current one first** — a mismatch outranks commit count, and is the common case since every ship-spec run cuts a new branch. Then `git log --oneline --since=<ts> --all`, preferring the timestamp from the **filename** over the body line. Rubric: no commits, same branch → fresh; few, unrelated → review then resume; many, or touching Critical Files, or branch mismatch → verify carefully; weeks plus divergence → consider a fresh handoff.
   - Read fully, **following the `Continues from` link to a maximum of 5 hops, tracking `resolve()`d absolute paths compared case-insensitively on Windows.** Prefer the markdown href, resolved relative to the handoffs directory. **If the line carries no href** — two on-disk documents record a bare backticked path instead — take the first backticked or bare path on the line, resolving it relative to the handoffs directory when bare and to `<project-path>` when it begins `.claude/` — **unless the text before it on that line contains `None` or `new thread`.** Three corpus documents record a *rejected* auto-link in exactly that shape (`- **Continues from**: None. The scaffold auto-linked \`…\``), and following it resumes from an unrelated session while presenting the result as chain context. If neither yields an existing file, note it and stop the chain rather than guessing. A cycle terminates with a note.
   - Verify branch/blockers/assumptions; begin at Immediate Next Steps #1.
4. **SESSION TRANSFER** — per D5.
5. **Superseding a previously installed handoff skill** — per D9, harness-neutral.
6. **Test plan / Test command / Done-when** — following `skills/talaria/SKILL.md`. These ship into operator installs (`sync.py` mirrors byte-for-byte); intentional, as it is for talaria.

### Module conventions (all three files)

Each of `_sections.py`, `create_handoff.py` and `validate_handoff.py` opens with `from __future__ import annotations`, as every stdlib script in this repo does (`lint.py`, `sync.py`, the three `talaria_*.py`, `read_board.py`). This is load-bearing, not cosmetic: `AGENTS.md` declares a Python 3.8 floor, and the PEP 585 / PEP 604 annotations used here `list[str]` and `str | None` are evaluated at def time without it and raise `TypeError` on 3.8 — `'type' object is not subscriptable` for `list[str]`, `unsupported operand type(s) for |: 'type' and 'NoneType'` for `str | None`. The precedent signature is `def main(argv: list[str] | None = None) -> int` (`talaria_bridge.py:1070`, `talaria_read.py:289`, `talaria_watch.py:738`).

### Encoding discipline (both entry points)

**All file I/O is explicitly UTF-8**, reads normalized per D3. Measured on the operator machine: `locale.getpreferredencoding(False)` is **`cp1252`**, `sys.flags.utf8_mode == 0`. A bare `write_text`/`read_text` uses cp1252 — a `UnicodeEncodeError` crash on git metadata it cannot encode (this repo's `git log` contains `U+FEFF`), and valid UTF-8 documents reported undecodable.

- **Writes:** `encoding="utf-8", newline="\n"`. The `newline` argument is required — without it Python translates `\n` → `\r\n` on Windows and **every scaffold would be CRLF**, i.e. the skill would fail to validate its own output.
- **Reads:** the D3 normalizer. **Subprocess output:** `encoding="utf-8", errors="replace"`.

### `scripts/create_handoff.py`

CLI: `create_handoff.py [slug] [--continues-from FILE] [--project-path PATH]`. Stdlib only. **Imports `TEMPLATE_SECTIONS`, `normalize`, `first_heading_title`, `todo_marker` and `TODO_MARKER_RE` from `_sections` by file path (D4); the section table, the marker text and the marker pattern are never restated in this file.** `TODO_MARKER_RE` is what the `&#91;` rewrite below matches against — without it this script would re-derive the marker shape, which is the divergence D4 exists to prevent. Exposes `main(argv: list[str]) -> int`; the `__main__` guard is `sys.exit(main(sys.argv[1:]))`, following `talaria_bridge.py`'s return-an-int discipline so tests assert on a returned value, not `SystemExit`.

- **`--project-path`** defaults to CWD, must be an existing directory (else clear message, non-zero exit), and bases the output directory, `--continues-from` resolution, **and the working directory of every git subprocess** (`cwd=<resolved project path>`, **with every inherited `GIT_*` variable removed from the child environment** — `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_CEILING_DIRECTORIES`, `GIT_PREFIX`, … — so `cwd` alone decides the repository. Scrubbing only the first two is not enough: git resolves all of them ahead of discovery and a hook exports the lot, so with `GIT_INDEX_FILE` still set `git status` reads the *other* repository's index). Without this, a document written into another repo is pre-filled with the *calling* repo's branch and commits — silently wrong in the field RESUME's staleness check trusts most, and it fails silently because git succeeds, just against the wrong repository.
- **Create the output directory** — `mkdir(parents=True, exist_ok=True)` on `<project-path>/.claude/handoffs/`. Without it the first CREATE in any project raises an uncaught `FileNotFoundError`. Failure exits non-zero naming the resolved directory.
- **Slug:** sanitize to `[a-z0-9-]`, collapse runs of `-`, strip leading/trailing `-`, **truncate to 60 characters**, and only *then* default to `handoff` if empty. Reproduced with `LongPathsEnabled=1`, a 316-character target path still raises `OSError [Errno 22]`.
- **Collision and atomicity are two mechanisms, not one.** (`os.replace` alone is atomic *replacement* — it would clobber an existing document silently, which is the opposite of collision safety.) In order:
  1. **Validate everything first** — `--project-path`, the slug, and `--continues-from` — *before* claiming a name. The `--continues-from` hard-error path promises "no document written", which only holds if no name has been claimed yet.
  2. **Claim `<stem>.md.tmp`**, not `<stem>.md`, with `with open(claim, "xb"): pass` — binary because nothing is written through it, and closed immediately because on Windows `os.replace` fails with `PermissionError` while a handle on the target is open. Claiming a `.tmp` is what makes a **hard kill** survivable: the four git subprocesses below can run for ~40s after the claim, and a `taskkill` or a closed terminal in that window bypasses any `try` block — but RESUME already lists `*.md` and ignores `*.tmp`, so an orphaned claim is invisible rather than offered as the newest handoff.

     **The claim is a name reservation for `<stem>.md`, and it is not the document.** Because the claim and the eventual document are different paths, the exclusive create alone does not guard the `.md` name — so a stem is taken **if `<stem>.md.tmp` raises `FileExistsError` *or* `<stem>.md` already exists**. Both conditions must be tested, or step 3's `os.replace` silently clobbers a handoff whose claim was already cleaned up. On a taken stem, append `-2` … `-9` **to the timestamp-and-slug stem** — `<stem>-2.md` with claim `<stem>-2.md.tmp`, never after `.md` — then fail non-zero past `-9`.
  3. **Render** via `tempfile.mkstemp(prefix=".session-handoff.", suffix=".md.tmp", dir=<handoffs dir>)` — dot-prefixed to match the repo's four existing atomic writes (`talaria_bridge.py:420`, `talaria_watch.py:123,140`, `talaria_read.py:174`) — and **close the descriptor before renaming**: `mkstemp` hands back an *open* fd, and on Windows an open **source** handle blocks `os.replace` exactly as an open target handle does (reproduced: `WinError 32`). Wrap it as `os.fdopen(fd, "w", encoding="utf-8", newline="\n")` in a `with`, **flushing and `os.fsync`ing before the block exits** as all four cited sites do, then `os.replace` onto `<stem>.md` and **remove the claim**.
  4. **On any exception between the claim and the successful replace**, remove both the rendered temp and the claim, then re-raise. **On success, remove the claim after the replace returns** — it is a reservation, never the document, so nothing is lost by deleting it and a `CREATE` that leaves it behind litters a permanent zero-byte `<stem>.md.tmp` beside every handoff. Do not let the reservation survive as a de-facto collision marker: step 2 tests `<stem>.md` directly, which is what makes the guarantee hold whether or not a previous claim was cleaned up.
- **Git metadata** — branch, last 5 commits, modified + staged files — **every call wrapped with a 10-second timeout**, a timeout treated exactly like a non-zero exit. Placeholder text distinguishes not-a-repo / no-commits / git-unavailable-or-timed-out so the failure is diagnosable from the document. A silent indefinite hang is the worst failure here.
- **`[TODO: …]` markers go into exactly the rows classed `required` or `recommended`** — rendered through `_sections.todo_marker()`, one per such section and nowhere else. The `title`, `container`, `generated` and `chain` rows never carry one. (`Files Modified` *is* classed recommended and *does* carry one: git fills its path column, the author explains why those files changed, which is exactly the work a marker tracks. **Its single marker is a line beneath the generated table, never inside a cell** — `[TODO: Files Modified — why did each of these change?]` — so the section's count stays one no matter how many rows git emits, and the generated rows stay untouched. A per-cell marker would emit up to ten and fail test item 2.) Critically, the git-failure strings above are diagnostics, not author work: they are plain prose (`_not a git repository_`) and **must not** use the marker shape. A git placeholder written as `[TODO: not a git repository]` would make every CREATE outside a repo permanently un-`READY`, with nothing for the author to replace.
- **Markdown safety:** paths gathered with `-z` and `-c core.quotepath=false`; `|` and backticks escaped before entering a table cell; table capped at 10 rows with `… and N more`. **Any `[TODO…]`-shaped run in text this script did not author has its opening bracket rewritten as the HTML entity `&#91;`** — a commit subject like `[TODO] wire up X` is a real convention, and unescaped it would trip the whole-document marker scan on a fully written handoff. Unlike the tool's own placeholders the author cannot clear that without editing generated content, which is the same unclearable-gate failure the marker bullet prevents for our diagnostics.

  **The entity is load-bearing — a backslash escape does not work here.** `TODO_MARKER_RE` is `\[TODO\b[^\]]*\]`, and against `\[TODO\] wire up X` the engine matches `[TODO` at index 1, `\b` holds before the backslash, `[^\]]*` absorbs it and `\]` closes the match: the run renders correctly and still trips the gate. `&#91;TODO] wire up X` displays as written and matches nothing. This is why the rule cannot ride along with the `|`-and-backtick escaping in the same sentence — that mechanism is backslashes, and it is exactly the one that fails.

  **Scope is every string the author cannot edit**, not only git output: the four git-metadata fields, the three git-failure placeholders, and the chain block's `Previous title` — which is drawn from another document's H1 and so can carry anything at all. `create_handoff.py` therefore imports `TODO_MARKER_RE` alongside its other `_sections` names, and applies the rewrite through it rather than by re-deriving the marker shape.
- **`--continues-from`:** resolved against `<project-path>/.claude/handoffs/`; base and candidate both `resolve()`d; comparison case-insensitive on Windows. A path that escapes the directory **or names a file that does not exist is a hard error** — message naming the resolved path and base, non-zero exit, no document written.
- **The chain block is a pinned two-line format**, matching what the corpus actually carries:
  ```
  - **Continues from**: [<filename>](./<filename>)
    - Previous title: <escaped, ≤80 chars>
  ```
  with `- **Continues from**: None (fresh start)` emitted **only when the flag is not passed at all**. `Previous title` comes from `_sections.first_heading_title(normalize(...))` — the previous document's first **depth-1** heading; the raw title is **truncated to 80 characters first (ellipsis included), and escaped after** — escaping first can cut a `` \` `` pair at the boundary, and the escaped form may exceed 80 because the 80 bounds the title, not the rendered line. If it returns `None` — no depth-1 heading, or an empty one; the target need not be a document this skill generated — emit the filename in place of the title, and never fail the create. `|` passes through unescaped: the chain block is a bullet, not a table cell. **The filename and href are never escaped or truncated.**
- Prints the resulting path to stdout.

### `scripts/validate_handoff.py`

CLI: `validate_handoff.py <handoff-file>`. Stdlib only. Imports `_sections` by file path. Exposes `main(argv: list[str]) -> int` with the same guard.

- Checks, in order, all on `_sections.normalize()`d text (D0: no masked copy exists): each name in `REQUIRED_SECTIONS` present via `has_section`; no `TODO_MARKER_RE` match anywhere in the document; recommended sections present (informational only); secret scan (D1's list, nothing exempt).
- Report per D6; exits `0`/`1`/`2`/`3`.
- No `--json`; nothing consumes it yet.

### `reference/handoff-template.md`

The annotated section structure with per-section guidance and depths matching `TEMPLATE_SECTIONS`. **Every `required`/`recommended` section carries a `[TODO: …]` marker and the `title`/`container`/`generated`/`chain` sections carry none** — matching § `create_handoff.py` exactly, because this document is the annotated mirror of what the scaffold emits and it ships into operator installs.

## Test plan

Run from the repo root. Stdlib `unittest`, matching `tests/test_lint.py` and `tests/test_talaria_*.py`; scripts load via an `importlib` `load_script` helper. Exit codes are asserted on the **returned int** from `main(argv)`, never via `SystemExit`. Cases are generated in temp dirs except the two fixtures.

1. **Heading matcher — the filed bug.** A `###` required section is found (proves depth-blindness); a genuinely absent one reports `missing`; **the same name matches at every depth 1–6**. Plus: 7 `#` is not a heading; `#hashtag` and `##Foo` are not headings; 3-space indent is a heading, 4-space is not; a trailing `##` closing run is stripped; a mixed-case name matches; a name that prefixes another required name resolves correctly.
2. **Template round-trip.** Generate a scaffold → replace every `[TODO: …]` → validate → `READY`, exit `0`, zero `missing`. Every name in `REQUIRED ∪ RECOMMENDED` appears as a heading in a fresh scaffold, and the **subsequence** of scaffold headings matching those nine names equals `[name for _, name, cls in TEMPLATE_SECTIONS if cls in ("required", "recommended")]` in order — keyed on **class**, so the title/container/generated/chain headings stay free to be named anything (D4) and no test pins them. Also: a fresh scaffold contains **exactly one `[TODO: …]` per `required`/`recommended` row and none anywhere else** — asserted per name, not just by count: for each of the nine, `todo_marker(name)` occurs exactly once in the document, **and** `len(TODO_MARKER_RE.findall(text)) == 9`. The count alone cannot tell nine markers in the right nine sections from nine in one, which is what makes the completeness gate non-vacuous. `Files Modified`'s marker is asserted to sit outside its generated table block.
3. **Legacy-corpus compatibility — both shapes.** `legacy-flat.md` (all-`##`) and `legacy-nested.md` (`##`/`###`), both **authored, not copied**, validating with zero `missing`.
4. **Verdict / exit matrix.** Clean → `READY`/`0`; unfilled TODO → `NEEDS WORK`/`1`; absent required heading → `NEEDS WORK`/`1`; planted fake credential → `BLOCKED`/`2`; secrets **and** TODOs → `BLOCKED`; missing file and no-argument → `3`. Secret positives must include a bare `KEY=value` env-style line and an `sk-ant-api03-…`-shaped string; a near-miss negative ("token" in prose) must not trip; **a `BLOCKED` report for an 8-character generic value contains none of that value's characters** (D6 redaction).
5. **Accepted limits (D0), pinned so they are decisions not surprises.** A `[TODO: x]` inside a fenced block **does** trip the TODO check; a fenced line reading exactly `# Current State Summary` **does** satisfy that presence check. A required heading quoted inside a fenced block from another handoff **does** satisfy that presence check. All three assert documented behavior rather than aspiration.
6. **Encoding.** A scaffold generated where the HEAD commit subject contains an emoji writes successfully; the generated scaffold is **LF, not CRLF**; a **CRLF** handoff validates `READY` with **zero `missing`**; a BOM-prefixed handoff validates correctly.
7. **Scaffold robustness.** `--project-path <tmpdir>` outside any repository asserts the not-a-repo placeholder **with the test process CWD left at the repo root** (this tests the `cwd=` fix rather than the environment); generation into a project with no `.claude/` creates the directory; slug sanitizing and the 60-char cap (a 300-char slug still writes a valid file); `--continues-from` not-found and absolute-path escape both exit non-zero with **no file created**; and after a **forced rendering failure** the handoffs directory is byte-identical to its pre-call state — no orphaned claim file, no orphaned `.tmp`.

   **Collision, asserted both ways.** A same-second collision produces `-2` rather than clobbering — *and* the same assertion holds **with the first run's claim file removed**, which is the case that fails if step 2 tests only `FileExistsError` on the `.tmp` and not `<stem>.md` itself. Also assert a successful CREATE leaves **no `.tmp` behind**: the litter and the clobber are the same defect seen from two sides, so a test that pins only one of them lets the other ship.

   **Git-failure placeholders, all three.** A direct unit assertion, needing no repository: each of the three placeholder strings the module defines (not-a-repo / no-commits / git-unavailable-or-timed-out) is **rejected by `TODO_MARKER_RE`** and renders as italic prose. The end-to-end not-a-repo scaffold, with its markers replaced, still validates `READY`. The timeout string is the hardest of the three to provoke and the most tempting to phrase as an instruction to the reader, so it is the one that ships unpinned if the assertion stays end-to-end.

   **The `&#91;` rewrite.** A commit subject containing `[TODO] wire up X`, and a `--continues-from` predecessor whose H1 contains one, both produce a scaffold that validates `READY` once its own nine markers are filled.
8. **Chain round-trip.** Create A, then B `--continues-from A`; assert both emitted lines match the pinned format and the href resolves back to A. The escaping case chains from a predecessor the test **writes into the temp handoffs directory** — not a tracked fixture, since § New files declares exactly two and `--continues-from` hard-errors on anything outside `<project-path>/.claude/handoffs/` — with an H1 containing `|`, backticks and 200 characters, which a *generated* document could never carry (D4 derives its title from the sanitized 60-char slug). Also assert that a predecessor with **no depth-1 heading, and one whose H1 is empty (`# `)**, both yield the filename rather than an empty `Previous title:` line.
9. **Session-id validation.** Malformed, traversal-shaped, and **trailing-newline** ids are rejected before any filesystem lookup.
10. **Lint.** `skills/session-handoff/SKILL.md` yields zero ERROR and zero WARN, asserted **programmatically** via `lint.lint_path(...)` (as `tests/test_lint.py:44-46` does) — `lint.py --strict` exits non-zero only on ERRORs (`lint.py:291`), so the console command cannot check the WARN half.
11. **Inventory tripwire.** `tests/test_lint.py` bumped `7 → 8`, and the per-skill zero-ERROR loop passes for all 8.

The 5-hop chain cap and the RESUME staleness rubric are agent-executed prose, not code; deliberately untested.

## Test command

```console
python -m unittest discover -s tests -p 'test_session_handoff.py' -v
python lint.py --strict skills/session-handoff/SKILL.md
python -m unittest discover -s tests -p 'test_*.py' -v
```

Stdlib only — `AGENTS.md` § What this repo is declares "no dependencies beyond Python 3.8+ stdlib", and `skills/talaria/SKILL.md:126` states "Use stdlib unittest; no pytest/node gate is required." The third command is the full-suite gate; it must be green at the branch point (see Preconditions).

`python` must be the same interpreter the rest of the suite runs under — **pin it by full path if more than one is on PATH** (`skills/talaria/scripts/__pycache__/` holds `cpython-310`, `-311` and `-314` artifacts). Do not adopt talaria's `${HERMES_PYTHON:-python}`; that variable is Hermes-specific. `pytest` is an operator-local convenience, not a repo dependency.

```console
env -u PYTHONHOME -u PYTHONPATH -u UV_INTERNAL__PYTHONHOME python -m unittest discover -s tests -p 'test_session_handoff.py' -v
```

## Done when

Mapped to the brief's acceptance criteria. **#2 and #3 are narrowed by D0**, as recorded in § Deferred — this is not a 1:1 map and should not be read as one.

1. **(brief #1)** `skills/session-handoff/` exists, `python sync.py install` places it under the harness skill dir, and `lint.py` reports no ERROR and no WARN for it (test item 10).
2. **(brief #2, narrowed)** brief:42 names three call sites including a section-terminator scan; D0 removes the terminator, so the matcher is specified once in `_sections.py` — depth, indent, mandatory separator, closing sequence, case, newline normalization — matching **by name at any depth**, with every call site deriving from it. A freshly generated scaffold with placeholders replaced validates with **no section reported `missing`**, and so do both legacy on-disk shapes (test items 2, 3).
3. **(brief #3, narrowed)** `tests/test_session_handoff.py` passes, covering **two of brief:44's three distinctions** — a `###` section is found, a genuinely absent one reports `missing` — plus the scaffold round-trip and secret positives including the generic `KEY=value` class. The third distinction (`5 characters → still incomplete`) cannot be written: D0 retires the `incomplete` verdict.
4. **(brief #4)** All three modes work with `agentcraft-handoff` uninstalled: CREATE produces a `READY` document, RESUME loads and assesses one (degrading gracefully on an empty directory), SESSION TRANSFER either reads a real transcript within the 256 KB bound or degrades per D5 with the applicable case stated.
5. **(brief #5)** `~/.claude/skills/agentcraft-handoff/` is removed on the operator machine, and the uninstall step (dual-shell), the `--prune` warning, and the AgentCraft-may-restore-it caveat are recorded in tracked files (`SKILL.md` harness-neutral + `AGENTS.md` literal), not in gitignored `CLAUDE.md`.
6. **(brief #6)** VHS-28's own done-when #1, #2, #4 are satisfied by items 1–3; its #3 is satisfied by adoption-via-rewrite, recorded as D1 and reflected in the AGENTS.md entry.

## Out of scope

- **Solving the "referenced file(s) not found" false positive.** No path-classification logic (D7).
- **Parsing markdown** (D0). No fence/inline-span/thematic-break/setext handling, no third-party or vendored parser.
- **The `incomplete` verdict and any content-length measurement** (D0). The verdict vocabulary is `READY` / `NEEDS WORK` / `BLOCKED` only.
- **Generating a Hermes (or other harness) adapter** — the VHS-16 line.
- **Migrating or rewriting existing handoff documents.** They must remain readable (test item 3); they are not touched.
- **Preventing AgentCraft from reinstalling its managed skill.** No vendor-managed file is edited.
- **Any change to `sync.py`, `lint.py`, `README.md`, or the spec-lifecycle skills.**
- **Any scale machinery** (D10).
- **Fixing `main`'s pre-existing red suite** — a hard precondition resolved *before* this work, not part of this diff.

## Deferred (P2+)

- **Drift roll-up for the human check.** (c)-class additions carrying rationale but not authorized by the brief: D12's `reference/` singular overriding brief:30's literal `references/`; D3's newline-normalization requirement; D4's relocation of the section schema from `reference/handoff-template.md` (brief:30) to `_sections.TEMPLATE_SECTIONS`; and **D0's removal of the completeness-length check**. No (d) items — nothing is a silent addition.

  **D0 is the item requiring explicit human authorization, and here is exactly what it costs against the brief.** brief:44 does not say "present and populated" (an earlier draft of this entry quoted that phrase; it appears nowhere in the brief). It says: *"Preserve the three distinctions the vendor fix was smoke-tested against: level-3 section with real content → passes; genuinely absent section → still `missing`; level-3 section with 5 characters → still `incomplete`."* D0 deletes the third distinction and the `incomplete` verdict with it, so brief done-when #3's "the three heading distinctions" becomes two (found / missing). D0 also supersedes brief:42's section-terminator-scan requirement and brief:29's `score`. The *direction* is authorized — the brief's own § Open questions asks whether to keep the numeric threshold "or replace it with a pass/fail on required-sections-plus-no-secrets", which is precisely D6+D0, and none of this sits in § Decisions carried forward — but the narrowing is real and is yours to accept.
- **edge-cases/F-14 (r2, P3)** — `__pycache__` mirroring through `sync.py` is pre-existing; noted in § Left alone because it interacts with D9's `--prune` warning.
- **Corpus sampling note.** Measurements cited as "the five documents" are `MCP Server/.claude/handoffs/`. The wider ecosystem corpus is 23 documents across seven projects; its additional shapes are handled by the name-only rule rather than by fixture.
