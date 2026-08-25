# Reconciliation Report: VHS-28

> Date: 2026-08-25
> Spec: docs/specs/TODO/VHS-28.spec.md
> Merge: PR #24, squash commit `40c4bb8` (2026-08-24)
> Plane state: Done (group: completed)

## Summary

The spec shipped essentially as written. All 8 new files and both modified files
in § Scope appear in the diff; every one of D0–D12 is confirmed in code. One real
divergence: the shipped `chain_lines()` neutralizes the predecessor filename and
percent-encodes its href, which contradicts the spec's own literal sentence that
"the filename and href are never escaped or truncated" (spec:373). The deviation
is deliberate, carries an in-code rationale, and resolves a tension inside the
spec rather than departing from its intent.

## Scope

| Spec file | In diff? | Notes |
|---|---|---|
| `skills/session-handoff/SKILL.md` | Yes | As specified |
| `skills/session-handoff/scripts/_sections.py` | Yes | As specified |
| `skills/session-handoff/scripts/create_handoff.py` | Yes | As specified |
| `skills/session-handoff/scripts/validate_handoff.py` | Yes | As specified |
| `skills/session-handoff/reference/handoff-template.md` | Yes | Singular `reference/` per D12 |
| `tests/test_session_handoff.py` | Yes | Repo-root `tests/`, not inside the skill dir |
| `tests/fixtures/session-handoff/legacy-flat.md` | Yes | As specified |
| `tests/fixtures/session-handoff/legacy-nested.md` | Yes | As specified |
| `tests/test_lint.py` | Yes | Tripwire `7 → 8`, exactly as § Modified files predicted |
| `AGENTS.md` | Yes | § Superseded vendor skills added; no § File layout row, per D12 |

Unexpected files in diff (not in spec):

- `docs/specs/TODO/VHS-28.test-output.txt` (177 lines) — the ship-spec test-output
  capture for the PR audit trail. Benign process artifact, not product code;
  `VHS-13.test-output.txt` is already on `main` under the same convention.
  CodeRabbit asked for it to be relocated and the directory gitignored; that was
  **declined**, not deferred — vigil-skills is the target repo for VHS tickets,
  the spec and brief are already tracked at that path, and gitignoring
  `docs/specs/TODO/` would break `/spec-close`.

No spec-named file was dropped.

## Decisions

| # | Decision | Status | Evidence |
|---|---|---|---|
| D0 | Validator does not parse markdown; no completeness length check | Confirmed | `validate_handoff.py:13-15` — verdict table is `READY`/`NEEDS WORK`/`BLOCKED` only; zero occurrences of `incomplete` as a verdict, no length measurement |
| D1 | Clean-room rewrite, not a port | Unverifiable | Structural check cannot prove provenance; no vendor product nouns ("hero", "AgentCraft") appear in the skill body |
| D2 | Two entry points, not four scripts | Confirmed | `scripts/` holds exactly `_sections.py`, `create_handoff.py`, `validate_handoff.py`; no `list_handoffs.py` / `check_staleness.py` |
| D3 | One heading matcher, in one shared module | Confirmed | `_sections.py:70-71` — `_HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")`, the single definition; `has_section()` and `first_heading_title()` both derive from it |
| D4 | One vocabulary, shared by file-path import | Confirmed | `create_handoff.py:53-57` and `validate_handoff.py:32-35` both use `spec_from_file_location`; comment states "No `sys.path` mutation: sync.py mirrors these files" |
| D5 | Session transfer: declared, portable, bounded, degradable | Confirmed | `SKILL.md:114-125` — harness layout given as an *example*, read bounded to `max(0, size - 256*1024)`, mandatory fallback |
| D6 | The gate is a verdict, not a score threshold | Confirmed | `validate_handoff.py:179-183` — verdict/code pairs `BLOCKED`/2, `NEEDS WORK`/1, `READY`/0; no numeric score |
| D7 | The file-reference check is dropped | Confirmed | Zero matches for `referenced file` / `not found` in `validate_handoff.py` |
| D8 | Storage location and naming unchanged | Confirmed | `create_handoff.py:7,411` — `.claude/handoffs/`, stem `%Y-%m-%d-%H%M%S-<slug>` |
| D9 | Supersession is an operator step, recorded in tracked files | Confirmed | `AGENTS.md:59-81` — dual-shell uninstall line, `--prune` warning, AgentCraft-may-restore caveat |
| D10 | Scale is a recorded non-factor | Confirmed | Brief § Scale declares "no"; no scale machinery in the diff |
| D11 | Name: `session-handoff` | Confirmed | `SKILL.md:4` frontmatter `name: session-handoff`; description fires on all five vendor phrasings |
| D12 | In-repo consistency calls | Confirmed | `reference/` singular on disk; no § File layout row added to AGENTS.md |

### Deviation — predecessor filename escaping (the one real drift)

**Spec (line 373):** "**The filename and href are never escaped or truncated.**"

**Shipped (`create_handoff.py:256-265`):**

```python
return [
    "- **Continues from**: [{}](./{})".format(
        neutralize_todo(filename), quote(filename)),
    "  - Previous title: {}".format(shown),
]
```

The label is passed through `neutralize_todo()` and the href through `quote()`.
The filename is still never *truncated* — the drift is on "escaped" only.

**Why it is right.** A hand-created predecessor named `[TODO] notes.md` would
trip the whole-document marker scan on an otherwise-complete handoff, and the
author cannot clear it because the chain block is generated content. The spec's
own broader rule — that the `&#91;` rewrite covers every string the author
cannot edit — already implied this; line 373 states the narrower promise and the
two sit in tension. Shipping resolved the tension toward the broader rule.
Percent-encoding the href breaks the marker shape *and* keeps the link
resolvable; both operations are no-ops for a generated filename, whose slug is
already `[a-z0-9-]`. The rationale is recorded in-code at `create_handoff.py:257-262`.

Rejected alternative: neutralizing the label only, which left the href still
matching the marker pattern.

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Skill exists, installs via `sync.py`, lint reports no ERROR **and no WARN** for it | Met | `~/.claude/skills/session-handoff/` present; `python lint.py --strict` → `0 error(s), 3 warning(s)`, all three on `review-pr`/`ship-spec`/`spec-close`, none on `session-handoff` |
| 2 | Matcher specified once, matching by name at any depth; scaffold and both legacy shapes validate with no section `missing` | Met | `_sections.py:70-71` single `#{1,6}` matcher; `tests/fixtures/session-handoff/legacy-{flat,nested}.md` exercised by the suite |
| 3 | `tests/test_session_handoff.py` passes — two heading distinctions, scaffold round-trip, secret positives incl. generic `KEY=value` | Met | `python -m pytest tests/ -q` → **102 passed, 37 subtests passed** in 5.99s |
| 4 | All three modes work with `agentcraft-handoff` uninstalled | Met | `~/.claude/skills/agentcraft-handoff/` absent; installed copy smoke-tested through the full verdict matrix — unfilled scaffold → 1, filled → 0, planted credential → 2, missing file → 3 |
| 5 | Vendor copy removed on the operator machine; uninstall step + `--prune` warning + restore caveat in tracked files | Met | Vendor dir absent; `AGENTS.md:59-81` carries all three, in a tracked file (not gitignored `CLAUDE.md`) |
| 6 | VHS-28's own done-when #1/#2/#4 satisfied by items 1–3; #3 by adoption-via-rewrite | Met | Items 1–3 above; D1 recorded and reflected in the AGENTS.md entry |

Zero Unmet.

## Test Plan

| Test | Exists? | Location |
|---|---|---|
| Heading distinctions (found / missing) | Yes | `tests/test_session_handoff.py` |
| Legacy on-disk shapes, flat and nested | Yes | `tests/fixtures/session-handoff/legacy-flat.md`, `legacy-nested.md` |
| Scaffold round-trip (create → fill → validate clean) | Yes | `tests/test_session_handoff.py` |
| Secret positives incl. generic `KEY=value` | Yes | `tests/test_session_handoff.py` |
| Shipped-skill inventory tripwire | Yes | `tests/test_lint.py:49-56` (`7 → 8`) |

Suite total: 102 passed, 37 subtests. 778 lines of new test code.

## Wiki-ready

Decisions and comprehension worth extracting to the wiki:

- **Decision D0 — a validator that does not parse markdown.** The reusable
  judgment: dropping the ≥50-character completeness check dropped everything
  that needed a parser (fence masking, thematic-break termination, subtree
  fallback) and replaced it with a placeholder scan. Constrains future validator
  work in this repo and reinforces the stdlib-only contract that
  `2026-06-15-vhs-19-fork-and-own-converter.md` already defended once.
- **Decision D9 — supersession as a recorded operator step.** `sync.py` installs
  but cannot remove a vendor copy it never installed, so the uninstall lives in
  `AGENTS.md` rather than in code. Non-obvious and constraining: it departs from
  `README.md`'s promise to preserve separately-installed skills, deliberately and
  narrowly, and it carries the `--prune` landmine.
- **Comprehension — the session-handoff skill.** What changed (a tracked,
  clean-room skill superseding an untracked vendor copy), why (the fix existed on
  one machine with no history), what would break (behavior keys off the *class*
  column in `TEMPLATE_SECTIONS`, never the name — renaming a `required`/
  `recommended` row changes the gate; file-path import is load-bearing because
  `lint.py` does not exist beside an installed skill).

RECONCILED: yes DRIFT: 2
