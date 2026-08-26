# VHS-29 — `/spec-close` appends to a newest-first `log.md`; make it prepend, safely

**Status:** Backlog · **Priority:** Medium · **Assignee:** Unassigned
**Created:** 2026-08-25 · **Plane:** VHS-29
**Origin:** Hit live during the VHS-28 `/spec-close` run (2026-08-25).

## Why

`skills/spec-close/SKILL.md` Phase 5 step 4 instructs: *"**Append** the approved entry to `<wiki_root>/log.md`."* The wiki's `log.md` header declares the opposite and names the violation explicitly:

> **Newest first.** `/wiki-after-merge` prepends here; if a tool appends at the
> bottom instead, the entry is out of contract — re-sort rather than leaving it.

So every `/spec-close` run drops its entry at the bottom of a newest-first file and an operator re-sorts by hand. The wiki-side sibling `wiki-after-merge/SKILL.md:39` already does it right ("prepend a new entry under format `## [YYYY-MM-DD] {action} | {project} — {summary}`"), so the fleet's two `log.md` writers disagree with each other.

**Not a regression — a drift.** The two sides were never in sync:

- `spec-close` was created 2026-06-14 (`aeecc86`, VHS-12) already saying "Append the approved entry"; `git log -S` shows that wording has never changed.
- The wiki's newest-first contract landed 2026-08-20 (`87e58b2`, "re-sort log.md newest-first and run the third rotation").

The wiki was fixed; the skill that writes into it was not. Everything closed since 2026-08-20 has needed the manual re-sort.

## The sharper bug the naive fix hides

Following the wiki's contract instead of the skill's wording surfaced a second defect — the part actually worth pinning.

**Prepending by seeking the first `## [` in the file corrupts the header.** Line 3 of `log.md` is the format description:

```markdown
Append-only record of wiki operations. Format: `## [YYYY-MM-DD] action | description`
```

A plain `text.index("## [")` matches *inside that sentence*, splits it, and inserts the close entry mid-header. Observed live and reverted with `git checkout -- log.md`. The insertion anchor must be line-anchored on a real date:

```python
re.search(r"^## \[\d{4}-\d{2}-\d{2}\] ", text, re.M)
```

Note the header sentence still calls the file "Append-only", which is stale in exactly the same way and reads as license for this bug. That line lives in the wiki repo.

## Goal

`/spec-close` prepends its entry above the newest existing dated entry, using an anchor that provably cannot match the header's format sentence — and a test pins the header-corruption case, since a naive fix passes every test that does not run against a real `log.md` header.

## Scope

### 1. `skills/spec-close/SKILL.md` — the append wording

Four sites carry literal append wording, plus one tool-note site that lists `log.md` among Write targets:

| Line | Site | Load-bearing? |
|---|---|---|
| 343 | Phase 5 step 4 — the actual instruction | **yes** |
| 309 | Close-plan template — `Log.md append:` | no (operator-facing) |
| 365 | Completion output — `Appended: log.md` | no (operator-facing) |
| 3 | Frontmatter `description` — "…and append to wiki log.md" | no (discovery text) |
| 382 | Mutation-boundary note — lists `log.md` among Write targets | wording only |

All five must read consistently after the change. Line 3 is the skill's `description`, which is what fires the skill — reword without breaking its trigger phrasing.

Phase 5 step 4 must specify the full insertion contract:

- **Normal case** — prepend above the first *line-anchored dated* heading.
- **Fresh wiki (no dated entries)** — append after the header block.
- **Missing `log.md`** — create the file.

### 2. Insertion mechanics — a script

**Decision (Devin, 2026-08-25): ship a script.** `skills/spec-close/` currently ships `SKILL.md` and nothing else, so this is the skill's first script. The reason is done-when #4: a prose instruction is not directly testable — the strongest a doc-only fix can pin is its own wording, not its behavior against a real header, and the whole point of this ticket is that a naive fix passes every test that does not run against a real header.

`skills/spec-close/scripts/prepend_log_entry.py` — stdlib only, following `skills/session-handoff/scripts/` as the shape precedent — owns the deterministic part: locate the anchor, handle the three cases above, write. Phase 5 step 4 invokes it instead of describing byte surgery in prose. This matches the repo's stated principle that only deterministic gates earn a script; a regex that must not match one specific sentence in one specific file is exactly that.

The spec still decides whether the **idempotency guard** moves into the script alongside the insert (making check-and-insert one operation) or stays as the prompt-level `grep -F` it is today, and settles the script's CLI surface, exit codes, and whether it writes in place or emits to stdout.

### 3. Idempotency guard — unchanged in substance

The existing guard greps for the literal `close | <PROJECT> — <TICKET-ID>:` before writing and skips if present. Placement does not affect it, so the matching rule needs no change. The trailing colon stays load-bearing (without it, closing `<PROJECT>-1` after `<PROJECT>-11` false-matches). If the guard moves into the script, its behavior must be identical, including the `close |` prefix that distinguishes close entries from `wiki-after-merge`'s merge entries.

### 4. Test — pin the header-corruption case

At minimum, against a fixture that reproduces a **real `log.md` header** (title line, the "Append-only … Format: `## [YYYY-MM-DD] action | description`" sentence, the newest-first blockquote):

1. **Header corruption** — insertion lands above the first real dated entry and leaves the header byte-identical. A naive `index("## [")` implementation must fail this test.
2. **Fresh wiki** — header block present, zero dated entries: entry lands after the header, header intact.
3. **Missing file** — `log.md` absent: file created with the entry.
4. **Idempotency** — running twice produces one entry (wherever the guard ends up).

Follows the existing `tests/test_lint.py` / `tests/test_session_handoff.py` shape (stdlib + pytest, fixtures under `tests/fixtures/`).

### 5. Wiki-side — outside this PR

`log.md`'s header still opens "Append-only record of wiki operations", which contradicts the newest-first rule three lines below it and reads as license for the bug. Reconcile that sentence in `vigil-harbor-wiki`. Per repo convention this **merges direct on wiki master and is not part of the vigil-skills PR** — the spec must say so explicitly so the step is not lost.

## Scope note

`spec-close` is the only skill in `vigil-skills` that writes `log.md` — verified by `grep -rln "log\.md" skills/`, which returns `skills/spec-close/SKILL.md` alone. `wiki-after-merge` and `wiki-state-update` live in the wiki repo and are already correct. No other caller needs changing.

## Decisions carried forward

- **Ship a script, not prose** (Devin, 2026-08-25). §2. Done-when #4 is behavioral, so the insertion needs a testable surface.
- **Spec-lifecycle process.** Brief → `/spec-cycle` → `/ship-spec` → `/spec-close`, per repo convention.
- **Wiki-side change merges direct on master** (§5), not through the vigil-skills PR.
- **Portability contract applies** (`docs/portability-contract.md`) — the new script is stdlib-only Python, and `python lint.py` must stay clean for `spec-close`.

## Scale

**Factor:** no — one insertion, one file, one entry per close. The scalability lens stays off.

## Done when

1. `/spec-close` prepends, and all five sites in `SKILL.md` read consistently.
2. The insertion anchor is line-anchored on a real date and provably cannot match the header's format sentence.
3. Fresh-wiki (no dated entries) and missing-`log.md` cases are both specified.
4. A test pins the header-corruption case, and it fails against a naive `index("## [")` implementation.
5. `python lint.py` reports no ERROR for `spec-close`; the test suite passes.
6. The wiki-side "Append-only record" reconciliation is recorded as an out-of-PR step with its destination named.

## Out of scope

- Re-sorting historical `log.md` entries — the file is currently in contract (the VHS-28 entry was prepended by hand). This ticket is about the next close and every one after it.
- Any change to `wiki-after-merge` or `wiki-state-update` — both already prepend correctly.
- The log-rotation boundary (`log-archive.md`, "entries dated 2026-08-01 and later") — `spec-close` writes one entry at the top and never rotates.
- Any other Phase 5 step, the coverage model, or the Plane state gate.

## Open questions for the spec

- **Script surface.** CLI shape, exit codes, and whether `prepend_log_entry.py` writes `log.md` in place or emits the merged text to stdout for the skill to Write. In-place keeps Phase 5 simple; stdout keeps the mutation boundary visible in the skill body, which §5's tool-note (line 382) currently describes as a Write.
- **Guard placement.** Does the script own the idempotency grep (atomic check-and-insert) or does the prompt keep it? If the script owns it, Phase 5 step 4's prose guard collapses into the invocation and the "already present → skip" path needs a distinct exit code.
- **Blank-line discipline.** Exact separator handling between the header block, the inserted entry, and the previously-newest entry — the fixture tests must pin whatever the spec chooses, since "one blank line" vs "two" is the kind of thing that silently drifts.

## Filing note (carried from the ticket)

Two plane-proxy artifacts worth knowing about: (1) `description_html` is now HTML-escaped, so markup stores as literal visible source — the VHS-29 description is plain text for that reason; (2) angle-bracket placeholders are stripped as unknown tags, which silently ate several placeholders from an earlier revision, so brace placeholders were used instead. Worth checking whether other tooling that writes Plane descriptions is affected — **not part of this spec.**

## References

- **Plane VHS-29** — the source card.
- `skills/spec-close/SKILL.md` lines 3, 309, 343, 365, 382 — the five sites.
- `vigil-harbor-wiki/log.md` — header block, newest-first contract, and the stale "Append-only" sentence.
- `vigil-harbor-wiki/skills/wiki-after-merge/SKILL.md:39` — the correct prepend wording, already shipped.
- `aeecc86` (2026-06-14, VHS-12) — where the append wording entered.
- `87e58b2` (2026-08-20) — where the newest-first contract landed on the wiki side.
- `skills/session-handoff/scripts/` + `tests/test_session_handoff.py` — script and test shape precedent (VHS-28).
