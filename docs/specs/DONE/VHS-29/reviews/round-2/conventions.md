# Conventions Review — round 2

Grounding: spec, brief, `AGENTS.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, `lint.py` + `tests/test_lint.py`, `tests/test_session_handoff.py`, `skills/session-handoff/` scripts, `sync.py`, `.gitattributes`/`.gitignore`, the live `skills/spec-close/SKILL.md` (all eight cited lines verified at their stated numbers), wiki `projects/vigil-skills/{state,filemap}.md`, wiki `decisions/` (both VHS-28 entries), and the live `vigil-harbor-wiki/log.md` header. All three round-1 reports read from disk.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | `AGENTS.md:29` sixth append site | CLOSED | spec § Scope line 30 puts `AGENTS.md:29` **and** `:100` in files-to-change; test case 15 asserts over both. Verified live: those are the only two `append` hits in `AGENTS.md` |
| conventions | F-2 | Five-site inventory off by one; misses `grep -F` at 380 | CLOSED | spec § Scope lines 13–26: eight-site table (3, 204, 309, 343, 365, 380, 381, 396), line 382 named unchanged. All eight verified against the live file; 381 is indeed the Write-targets bullet |
| conventions | F-3 | `requires:` under-declares vs contract §3 | CLOSED | D10 (spec:193–213). Evidence re-verified: `git fetch` at `SKILL.md:34`, `gh pr view/diff` at `:74`, shared-memory at `:378`, Plane at `:379`; `grep -in subagent` → 0 hits |
| conventions | F-4 | Backlog sentence in `docs/authoring-portable-skills.md` | CLOSED | spec § Scope line 31; live `:41` confirmed to name the three skills |
| conventions | F-5 | Script path reference form unspecified | CLOSED | D9 (spec:185–191); matches `skills/session-handoff/SKILL.md:23-24`'s skill-relative form |
| conventions | F-6 | `--dry-run` is unused surface | CLOSED | spec:116 drops it, citing VHS-28's principle; old test case 12 gone |
| conventions | F-7 | Unauthorized additions → drift check | **PARTIAL** | § Deferred (spec:344–346) added, but it still lists only v1's three items; v2's own brief-unauthorized additions (D7 refusal, D8 atomicity + concurrency) are not carried there — see F-2 below |
| conventions | F-8 | `lint --strict` cannot enforce zero WARN | CLOSED | test case 17 uses `lint.lint_path()` in-process (same API as `tests/test_lint.py:36`); § Test command labels `--strict` an ERROR gate only |
| correctness | F-1 | § Scope forbids the line-204 edit § Design mandates | CLOSED | line 204 now a scope row; "Files to leave alone" reads "Phase 3 apart from line 204's guard parenthetical" |
| correctness | F-2 | `grep -F` survivors at 380 / 396 | CLOSED | both are scope rows with intended new text (spec:22, 24, 262, 266) |
| correctness | F-3 | `requires:` under-declaration | CLOSED | D10, as above |
| correctness | F-4 | Site is 381, not 382 | CLOSED | spec:23 + 26, with the inherited off-by-one called out |
| correctness | F-5 | Encoding unpinned on the `--dry-run` path | CLOSED | `--dry-run` dropped; D6 item 3 reconfigures both streams |
| correctness | F-6 | Test-14 allowlist names a nonexistent survivor | CLOSED | now "expected count: 0" (test 15); D7's table and § Design:257 use non-`append` phrasing |
| correctness | F-7 | Exit 1 ambiguous | CLOSED | D5 exit table + `try/except BaseException` → 2, `KeyboardInterrupt` re-raised (spec:126–136) |
| correctness | F-8 | Blank-line discipline on degenerate inputs | CLOSED | D7 "Degenerate inputs" bullet (spec:172) + test case 14 |
| correctness | F-9 | D2 "both properties" contradiction | CLOSED | spec:76 now "All three exclusions would have to fail simultaneously" |
| correctness | F-10 | Fixture "verbatim" vs AC6 | CLOSED | § Fixtures paragraph (spec:288) |
| correctness | F-11 | `wiki-after-merge:37-38` stale heading | CLOSED | § Wiki-side step (spec:276), explicitly optional and not an AC |
| edge-cases | F-1 | Exit 1 overloaded | CLOSED | D5, as above |
| edge-cases | F-2 | Fresh-wiki indistinguishable from missed anchor | CLOSED | D7 refusal row + `HEADINGISH_RE`; fixture `log-h3-entries.md`; test case 3 |
| edge-cases | F-3 | Script path / cwd in another repo | CLOSED | D9 + the not-found halt message; interpreter left to the harness, matching `session-handoff`'s shipped precedent, and any 127 is failure per D5 |
| edge-cases | F-4 | No atomic write | CLOSED | D8 reuses `create_handoff.py:338 write_atomically()`'s shape — verified: mkstemp-in-dir → `os.fdopen(..., encoding="utf-8", newline="\n")` → flush/fsync → close → `os.replace`, `unlink(missing_ok=True)` on `BaseException` |
| edge-cases | F-5 | Blank line at offset 0 / empty file | CLOSED | D7 degenerate-inputs bullet + test 14 |
| edge-cases | F-6 | stdout/stderr encoding | CLOSED | D6 item 3 |
| edge-cases | F-7 | Stale `grep -F` at 380 / 394 / 396 | CLOSED | 380 + 396 in scope; 394 verified to contain no `grep -F` and its "log idempotency guard" phrase stays accurate (spec:270) |
| edge-cases | F-8 | Concurrent writers undocumented | CLOSED | D8 concurrency paragraph (stat before/after, exit 2 `changed under us`) |
| edge-cases | F-9 | BOM survives `.strip()` | CLOSED | D6 BOM paragraph; `tests/fixtures/bom-skill/` precedent verified |
| edge-cases | F-10 | `__pycache__` mirrors into config dir | CLOSED | § Scope:44 + § Out of scope:339 |
| edge-cases | F-11 | `AGENTS.md:29` | CLOSED | as conventions F-1 |
| edge-cases | F-12 | Guard tripwire weaker than claimed | CLOSED | D4 "Consistency tripwire" — first line, not whole text (spec:106) |

## Findings

### F-1: Two stale `D8` cross-references survive the v2 renumbering — both should read `D10`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:17 (§ Scope table, line-3 row); spec.md:31 (§ Scope, "Other tracked files")
**Convention violated:** Internal cross-reference integrity — the spec makes its Decision IDs load-bearing pointers (§ Scope, § Design, § Done when, § Out of scope all cite them), and `AGENTS.md` § Plan & Spec Reviews requires reviews and specs to carry precise references.
**Evidence:** In v1 the `requires:` decision was D8. v2 inserted the atomic-write decision as D8 and moved `requires:` to D10, but two call sites were not renumbered:

- spec.md:17 — "`requires:` block added to the frontmatter **(D8)**"
- spec.md:31 — "**D8** removes `spec-close` from that list"

`D8` now reads "The write is atomic, and a concurrent change is detected" (spec.md:177), which says nothing about `requires:`. § Design:247 and test case 16 and Done-when #5 all correctly say D10, so the two stragglers point at the wrong decision. An implementer working the Scope list — the normal reading order — follows `D8` and lands on the atomicity decision.
**Suggested fix:** Change both to `D10`. While there, a quick pass over the remaining `D<n>` citations confirms the rest are correct (D2/D3/D4/D5/D6/D7/D9/D11 all resolve to their intended decisions).

### F-2: § Deferred was not extended to v2's own brief-unauthorized additions
**Severity:** P3
**Where:** spec § Deferred (spec.md:344–346); D7 (spec.md:153–175); D8 (spec.md:177–183)
**Convention violated:** The drift-check contract — `/spec-cycle` Phase 3 renders the spec's deferred/unauthorized items so a human sees additions *before* implementation rather than discovering them in the diff. Round-1 conventions F-7 established that this spec routes such items through § Deferred; the section now under-reports.
**Evidence:** § Deferred lists exactly three items (D10's `requires:` block, D4's first-line tripwire, test 15's standing wording assertion) — the v1 set. v2 added two load-bearing positions the brief does not authorize:

- **D7's refusal path.** The brief's § Scope reads "**Fresh wiki (no dated entries)** — append after the header block" and its Done-when #3 asks only that fresh-wiki and missing-file "are both specified." The spec introduces a third, *refusing* branch (exit 2 on a populated file the anchor misses) and rewrites its own Done-when #3 to require it. Correct and well-argued (spec.md:162) — but it is a spec-level change of direction against a brief-stated behavior, i.e. class (c).
- **D8's atomicity + concurrency detection.** The brief's open question asked only "in place or emit to stdout." Temp-file-plus-`os.replace` and a stat-based `log.md changed under us — re-run` refusal are new operator-visible behavior with no brief or ticket authorization.

Both carry explicit rationale, so neither is a silent addition — but neither reaches the Phase 3 drift check as currently written.
**Suggested fix:** Add two bullets to § Deferred naming D7's refusal branch (as narrowing the brief's fresh-wiki wording) and D8's atomicity/concurrency behavior, each with its one-line rationale, so the drift-check surfaces all five additions rather than three.

### F-3: Test case 15 pins its `AGENTS.md` assertion to line numbers, against the repo's content-based test convention
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan, case 15 (spec.md:308)
**Convention violated:** Repo test precedent — every doc assertion in the existing suite matches on *content*, never on line index, precisely so unrelated doc edits neither break the test nor make it silently check the wrong text.
**Evidence:** The spec says: "Same assertion over `AGENTS.md` **lines 29 and 100 specifically**." The shipped precedent (`tests/test_session_handoff.py:737-739`) reads the whole file and regex-searches it:

```python
body = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
found = ...search(body)
self.assertIsNotNone(found, "SKILL.md must declare the session-id pattern")
```

`tests/test_lint.py` is the same shape (content and rule names, no offsets). `AGENTS.md` is a living doc — 108 lines today, edited by most feature PRs — so a line-pinned assertion drifts to the wrong lines on the next unrelated edit and then passes vacuously. Verified that both `append` occurrences in `AGENTS.md` are the two the spec is fixing (`grep -in append AGENTS.md` → lines 29 and 100 only), so a content-based form is available and unambiguous.
**Suggested fix:** Restate case 15's `AGENTS.md` half as content: assert that the `/spec-close` bullet and the `/wiki-after-merge` paragraph each contain `prepend`, and that `grep -in "append" AGENTS.md` returns zero — or, if a blanket zero is too broad for a doc that may legitimately use the word later, assert on the two sentences located by substring, never by index.

### F-4: D9 claims parity with Phase 0 step 4 on `$CLAUDE_CONFIG_DIR`, which that step does not honor
**Severity:** P3
**Where:** spec § Decisions D9 (spec.md:189)
**Convention violated:** Accuracy of the cited in-file precedent; and, secondarily, the portability contract's case-2 tagging idiom for harness-specific concretions (`docs/portability-contract.md:107-117`).
**Evidence:** D9: "Phase 5 step 4 gives the concrete Claude Code form (`~/.claude/skills/spec-close/scripts/prepend_log_entry.py`, honoring `$CLAUDE_CONFIG_DIR`, `%USERPROFILE%\.claude\` on Windows) **the same way Phase 0 step 4 already spells out `states.json`'s location with both variants**." The live step reads:

```
skills/spec-close/SKILL.md:26
4. Read `~/.claude/skills/ship-spec/states.json` (`~/.claude/` on Unix; `%USERPROFILE%\.claude\` on Windows).
```

No `$CLAUDE_CONFIG_DIR`. Honoring the env var is the *better* rule — `sync.py:36` resolves the install dir as `--claude-dir` → `$CLAUDE_CONFIG_DIR` → `~/.claude`, so a script path that ignores it can point at a directory `sync.py install` never wrote to — but shipping it at only one of the two config-dir sites leaves the same file with two different resolution rules, which is the kind of drift this ticket exists to fix.
**Suggested fix:** Reword D9 to state the divergence rather than claim parity ("Phase 0 step 4 names only the two default locations; the script's rule additionally honors `$CLAUDE_CONFIG_DIR`, matching `sync.py`'s resolution order at `sync.py:36`"), and either bring `states.json`'s line along in the same edit — a nine-word change, and it would make the file self-consistent — or record in § Out of scope that it is deliberately left.

### F-5: D8 copies `write_atomically()` into a second skill without saying why it isn't shared
**Severity:** P3
**Where:** spec § Decisions D8 (spec.md:181)
**Convention violated:** Single-source-of-truth / reuse-vs-duplicate. The repo runs a `bloat-check` skill and CodeRabbit over every PR, and both are built to flag exactly this shape: a near-verbatim second copy of a named helper.
**Evidence:** D8 says the write "goes through a temp file … **reusing the shape of** `skills/session-handoff/scripts/create_handoff.py:338` `write_atomically()`" and then re-specifies the whole sequence. Verified: the two will be materially the same eight lines. The duplication is almost certainly *correct* here — skills install independently under `~/.claude/skills/<name>/`, `sync.py`'s `SUBTREES` mirrors per-skill trees with no shared module path, and `create_handoff.py`'s signature `(handoffs_dir, target, claim, text)` is welded to its claim-file reservation protocol, which `prepend_log_entry.py` has no use for. But the spec never says any of that, so the first reviewer of the diff re-derives it, or files it as duplication.
**Suggested fix:** One sentence in D8: skills are installed independently and share no importable module, and `create_handoff.py`'s claim-file parameters do not apply here, so the sequence is re-implemented deliberately rather than extracted — with the pointer kept so the two stay comparable.

### F-6: Two file-shape conventions left unpinned — the script's shebang and the `requires:` block's position
**Severity:** P4
**Where:** spec § Design, script shape (spec.md:225); § Design line 3 (spec.md:247)
**Convention violated:** `docs/portability-contract.md:91-93` ("Exactly one `requires:` key per skill, **placed after the existing scalar frontmatter keys** and before the closing `---`"), and the shipped script shape in `skills/session-handoff/scripts/`.
**Evidence:** § Design enumerates the script's shape — "module docstring stating usage, outcomes, and exit codes; `from __future__ import annotations`; a `main(argv)` returning an int; `if __name__ == "__main__"`" — but omits the `#!/usr/bin/env python3` line that all three shipped scripts carry (`create_handoff.py:1`; note git mode `100644`, i.e. shebang without an exec bit). Separately, neither § Scope's line-3 row nor § Design says where in the frontmatter the `requires:` block goes; `lint.py` validates the block's content but not its position (`_lint_requires`, `lint.py:145`), so the contract's placement rule is unenforced. `skills/spec-cycle/SKILL.md:5-10` puts it after `user_invocable:`.
**Suggested fix:** Add "shebang `#!/usr/bin/env python3`, mode 644" to the script-shape sentence, and "placed after `user_invocable:`, per `docs/portability-contract.md` § Uniqueness / position" to the line-3 description.

## Summary
P0: 0 | P1: 0 | P2: 2 | P3: 3 | P4: 1

STATUS: GREEN
