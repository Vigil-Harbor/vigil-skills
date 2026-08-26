# Reconciliation Report: VHS-29

> Date: 2026-08-25
> Spec: docs/specs/TODO/VHS-29.spec.md
> Merge: PR #25 — 7db7289 (squash; review commits 538d804, 03f24a3, 64a58e4, ecb07b6)
> Plane state: Done (group: completed)

## Summary

The spec shipped essentially as written: every file it named to change or create is in
the diff, all eleven decisions are reflected in the shipped code, and all six acceptance
criteria are Met. Two informational drift items, both additive and both originating in
the CodeRabbit review rounds rather than in implementation shortcuts.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-close/SKILL.md` | Yes | All nine sites reworded; `append` count 0, `grep -F` count 0 |
| `AGENTS.md` | Yes | `:29` prepend wording; `:100` wiki-after-merge "appends" → "prepends" |
| `docs/authoring-portable-skills.md` | Yes | `:41` backlog narrowed to `ship-spec`, `review-pr` |
| `skills/spec-close/scripts/prepend_log_entry.py` | Yes | Created, 599 lines |
| `tests/test_spec_close_log.py` | Yes | Created, 1207 lines |
| `tests/fixtures/spec-close/log-with-entries.md` | Yes | Created |
| `tests/fixtures/spec-close/log-fresh.md` | Yes | Created |
| `tests/fixtures/spec-close/log-h3-entries.md` | Yes | Created |
| `tests/fixtures/spec-close/log-no-trailing-newline.md` | Yes | Created |

Files the spec named to leave alone, confirmed untouched in the diff: `sync.py`, `lint.py`,
root `.gitattributes`, `tests/fixtures/.gitattributes`. No CRLF fixture was checked in, per
the spec's § Scope reasoning — CRLF is constructed in-test.

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-29.test-output.txt` — the `/ship-spec` test-capture audit artifact.
  Expected by the workflow, absent from the spec's declared file list. Counted as drift for
  bookkeeping; benign.

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| D1 | Ship a script, not prose | Confirmed | `skills/spec-close/scripts/prepend_log_entry.py` exists, stdlib-only, 599 lines |
| D2 | Anchor line-anchored on a real date | Confirmed | `prepend_log_entry.py:77` — `ENTRY_RE = re.compile(r"^## \[(\d{4})-(\d{2})-(\d{2})\] ", re.M)` |
| D3 | No markdown parsing | Confirmed | `prepend_log_entry.py:59-60` — fence masking explicitly declined, rationale recorded |
| D4 | Idempotency guard moves into the script | Confirmed | `--guard` flag; `SKILL.md:209` re-points the coverage note at the script; repo-wide `grep -F` count 0 |
| D5 | Entry text arrives on stdin | Confirmed | `prepend_log_entry.py:7`, `:441-444` — no-stdin case handled distinctly from empty-stdin |
| D6 | Encoding, newlines, BOM pinned | Confirmed | `prepend_log_entry.py:256-282` — strict UTF-8 decode, CRLF/lone-CR folding, BOM detach/re-attach |
| D7 | Four outcomes; unmatched anchor is a refusal | Drifted | Outcomes `prepended`/`fresh`/`created` plus exit 1 present as specified, but the shipped script adds a second refusal class beyond the spec — see Drift 2 |
| D8 | Atomic write, concurrent change detected | Confirmed | `prepend_log_entry.py:374-385` — `tempfile.mkstemp` + `os.replace`, 0600 mode corrected |
| D9 | Script resolves from the skill dir, never `project_root` | Confirmed | `SKILL.md:360` — `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-close/scripts/...`; `SKILL.md:31` states the one config-dir rule |
| D10 | `requires:` block added to frontmatter | Confirmed | `SKILL.md:4-9` — `shell: true`, `filesystem: [read, write]`, `network: true`, `services: [issue-tracker?, shared-memory?]` |
| D11 | Scale is a non-factor | Confirmed | No batching or rotation logic; the script writes one entry and never rotates |

**Drift 2 — D7 expanded during review.** The shipped script carries a `NotNewestFirst`
exception class (`prepend_log_entry.py:139`, raised at `:217` and `:246`) that the spec's D7
does not describe. It refuses three additional cases: an entry heading whose date is not a
real calendar day, an anchor whose date is not a real calendar day, and an entry strictly
older than the entry already at the anchor. This landed in review commits `64a58e4` and
`ecb07b6` answering a CodeRabbit finding — `ENTRY_RE`'s `\d{2}` fields constrain width, not
range, so `## [2026-13-45]` cleared every check the spec described and would have landed
permanently in the wiki's operations log. Additive and strictly safety-increasing; the spec
was not amended to match, which is the drift.

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Prepends; all nine SKILL.md sites plus AGENTS.md and the authoring doc read consistently | Met | `grep -ci append skills/spec-close/SKILL.md` → 0; `grep -c 'grep -F'` → 0; `AGENTS.md:29`/`:100` and `docs/authoring-portable-skills.md:41` all reworded |
| 2 | Anchor line-anchored on a real date, provably cannot match the header sentence | Met | `prepend_log_entry.py:77`; `tests/test_spec_close_log.py:189` asserts the naive `index("## [")` lands *inside* the format sentence |
| 3 | Fresh-wiki, missing-file, and refusal cases all specified | Met | Outcomes `fresh` (`:342-343`), `created` (`:294`), `AnchorMissing` (`:97`, `:304`), `NotNewestFirst` (`:139`) |
| 4 | A test pins header-corruption and fails against a naive implementation | Met | `tests/test_spec_close_log.py:187-198` — `test_naive_index_would_split_the_header` |
| 5 | `lint.py` no ERROR for spec-close; full suite passes | Met | `lint.py --strict` → 0 errors, 2 warnings (`ship-spec`, `review-pr` only); suite 159 passed, 3 skipped (POSIX-only), 44 subtests |
| 6 | Wiki-side reconciliation recorded as an out-of-PR step with destination named | Met | Spec § Wiki-side step names `vigil-harbor-wiki/log.md` and the exact reword (`Append-only record` → `Running record`). **The step itself is still outstanding** — see Left standing |

RECONCILED: yes DRIFT: 2

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| Header-corruption regression | Yes | `tests/test_spec_close_log.py:187` |
| Anchor unit test | Yes | `tests/test_spec_close_log.py` (ENTRY_RE cases) |
| Read-side refusal (`log-h3-entries.md`) | Yes | fixture plus cases present |
| Write-side heading validation | Yes | `prepend_log_entry.py:224` `ENTRY_RE.match(entry)` plus cases |
| Fresh wiki / missing file | Yes | `log-fresh.md` fixture; `created` outcome cases |
| Tail invariant (no trailing newline) | Yes | `log-no-trailing-newline.md` fixture |
| `requires:`-matches-the-body plus lint | Yes | `tests/test_lint.py` |

Suite result: **159 passed, 3 skipped, 44 subtests** (`python -m pytest tests/ -q`). The 3
skips are POSIX directory-permission and mode-bit cases, correctly skipped on Windows.

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:

- **Decision — the insertion anchor is a refusal contract, not a best-effort placement.**
  Non-obvious and constraining: the script's answer to every shape it cannot describe is
  exit 2, never a silent bottom-append, because a silent misplacement *is* the original
  VHS-29 bug. Reusable for any tool writing into an ordered wiki file.
- **Comprehension — `/spec-close` grew its first script, and the skill/config-dir split
  became load-bearing.** The skill now depends on an installed artifact, which introduces a
  failure mode the skill did not previously have (see Left standing).

## Left standing

1. **The wiki-side header reword is not done.** `vigil-harbor-wiki/log.md` still opens
   `Append-only record of wiki operations.`, contradicting the newest-first rule three lines
   below it. Criterion 6 required only that it be *recorded*; the operator step itself is
   still pending, direct on wiki master.
2. **`state.md:41` carries a now-stale verification line.** VHS-12's evidence line greps for
   `grep -F "close | <PROJECT> — <TICKET-ID>:"` in `skills/spec-close/SKILL.md`. VHS-29
   retired that guard into the script, so that grep now returns nothing. Historical record,
   but it no longer verifies.
3. **The fix was inert until installed.** Discovered during this close: the merged SKILL.md
   and script were absent from `~/.claude/skills/spec-close/` until `python sync.py install`
   was run. See the comprehension entry.
