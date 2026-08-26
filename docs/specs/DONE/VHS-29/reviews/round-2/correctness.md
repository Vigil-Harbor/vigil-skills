# Correctness Review — round 2

Grounding: read fresh from disk — `docs/specs/TODO/VHS-29.spec.md` (v2), `VHS-29.brief.md`, all three round-1 reviews, `CLAUDE.md` → `AGENTS.md`, `skills/spec-close/SKILL.md` (all eight cited lines verified at their stated numbers), `skills/spec-cycle/SKILL.md:5-10`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md:41`, `skills/session-handoff/SKILL.md` + `scripts/create_handoff.py:325-358`, `tests/test_lint.py`, `tests/test_session_handoff.py`, `lint.py`, `sync.py`, and `vigil-harbor-wiki/log.md` + `.claude/skills/wiki-after-merge/SKILL.md:37-39`. Plane VHS-29 retrieved from namespace `skills` (tag-exact, 1 hit; MCP 502'd once, succeeded on retry). Ran `python lint.py skills/spec-close/SKILL.md` → `0 error(s), 1 warning(s)`, and measured `python -V` = 3.14.3, `sys.stdout.encoding` = cp1252/surrogateescape when piped, `reconfigure(encoding="utf-8", newline="\n")` → UTF-8 + LF, uncaught `KeyboardInterrupt` → exit 130 (not 1). `git log` shows no commit to `skills/spec-close/SKILL.md` in the last 7 days (`b9afacd`, VHS-14); `AGENTS.md` last moved 2026-08-24 (`40c4bb8`) and both cited lines are current.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | § Scope forbids the edit § Design mandates (line 204) | CLOSED | spec:18 (Scope table row 204), :43 ("Phase 3 apart from line 204's guard parenthetical"), :249 (Design bullet), :324 (Done-when #1 enumerates eight) |
| correctness | F-2 | D4 retires `grep -F` but two SKILL.md sites still name it | CLOSED | spec:22, :24 (Scope rows 380/396), :108 (D4 em-dash paragraph), :262, :266 |
| correctness | F-3 | `requires:` under-declares | CLOSED | D10 spec:197-211 declares `network: true` + `services: [issue-tracker?, shared-memory?]`; evidence lines verified (`SKILL.md:34`, `:74`, `:378-379`); new test 16 |
| correctness | F-4 | Write-targets site is 381, not 382 | CLOSED | spec:23, :26, :264, :324 — verified 381 is the Write bullet, 382 the mutation boundary |
| correctness | F-5 | stdout/stderr encoding unpinned | CLOSED | D6 item 3 (spec:144); `--dry-run` dropped (spec:116). Measured claim is accurate |
| correctness | F-6 | Test allowlist names a nonexistent survivor; D7 trips it | CLOSED | test 15 now "expected count: 0" (spec:308); D7 reworded ("placed at end of file"); spec:175, :257 |
| correctness | F-7 | Exit 1 ambiguous | CLOSED | D5 exit table + reservation rationale (spec:126-136); test 9 |
| correctness | F-8 | Blank-line discipline on degenerate inputs | CLOSED | spec:172 ("no leading separator is emitted"); test 14 |
| correctness | F-9 | D2 "both properties" miscount + inverted logic | CLOSED | spec:76 "All three exclusions would have to fail simultaneously" |
| correctness | F-10 | Fixture "verbatim" vs AC6 reword | CLOSED | spec:288 |
| correctness | F-11 | `wiki-after-merge:37-38` heading drift | CLOSED | spec:276; verified `:37` reads "**Append log.md entry (idempotent).**" over a correct prepend at `:39` |
| edge-cases | F-1 | Exit 1 overloaded | CLOSED | D5 (spec:126-136); measured: uncaught `KeyboardInterrupt` exits 130, so the re-raise carve-out cannot collide with the reserved 1 |
| edge-cases | F-2 | Fresh wiki ≡ anchor-not-found | CLOSED | D7 Refuse row (spec:158) + `HEADINGISH_RE`; fixture `log-h3-entries.md`; test 3; Done-when #3 restated |
| edge-cases | F-3 | Script path *and interpreter* unresolved | PARTIAL | Path half fully CLOSED by D9 (spec:185-191). Interpreter still unnamed — see F-5 below. Downgraded from P1 to P2 because the spec adopts `session-handoff`'s documented harness-resolves precedent, verified at `skills/session-handoff/SKILL.md:44,50` (bare `create_handoff.py`, no interpreter) |
| edge-cases | F-4 | No atomic replace | CLOSED | D8 (spec:177-183); `create_handoff.py:338` `write_atomically` and `:347` `newline="\n"` both verified at the cited lines |
| edge-cases | F-5 | Blank line at offset 0 / empty file | CLOSED | spec:172; test 14 incl. second-close-on-created-file |
| edge-cases | F-6 | stdout encoding → UnicodeEncodeError | CLOSED | D6 item 3; `--dry-run` dropped |
| edge-cases | F-7 | Stale `grep -F` at 380/394/396 | CLOSED | 380 and 396 in Scope; 394 explicitly retained as still-accurate (spec:270) — verified `:394` says "the log idempotency guard", mechanism-neutral |
| edge-cases | F-8 | Concurrent writers undocumented | CLOSED | D8 concurrency paragraph (spec:183) + § Out of scope "Locking `log.md`" |
| edge-cases | F-9 | BOM survives `.strip()` | CLOSED | D6 BOM paragraph (spec:147); test 12 |
| edge-cases | F-10 | `__pycache__` mirrors via `sync.py` | CLOSED | spec:44 + § Out of scope; `SUBTREES`/`iter_files` verified at `sync.py:30,42-46` |
| edge-cases | F-11 | `AGENTS.md:29` out of scope | CLOSED | spec:30; test 15 |
| edge-cases | F-12 | Guard tripwire weaker than claimed | CLOSED | D4 first-line rule (spec:106); test 8 |
| conventions | F-1 | `AGENTS.md:29` sixth site | CLOSED | spec:30 (both :29 and :100) |
| conventions | F-2 | Off-by-one at 381 + missing 380 | CLOSED | spec:22-26 |
| conventions | F-3 | `requires:` under-declares vs contract §3 | CLOSED | D10; matches `spec-cycle:5-10` minus `subagents` |
| conventions | F-4 | `authoring-portable-skills.md:41` backlog | CLOSED | spec:31, :213; line 41 verified to name the three skills |
| conventions | F-5 | Script path form unspecified | CLOSED | D9 (spec:185-191) |
| conventions | F-6 | `--dry-run` has no caller | CLOSED | spec:116 drops it |
| conventions | F-7 | Unauthorized additions | CLOSED | § Deferred (spec:346) carries all three to the Phase 3 drift check |
| conventions | F-8 | `--strict` cannot enforce zero WARN | CLOSED | test 17 (spec:310) uses `lint.lint_path`; spec:320 restates `--strict` as ERROR-only. Verified `lint.py:243` `lint_path` exists and `tests/test_lint.py` uses it |

*(`scale_lens: off` — no `scalability.md` present in `round-1/`; nothing to ignore.)*

## Findings

### F-1: Two live references to "D8" now point at the wrong decision
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:17 (§ Scope table, line-3 row); spec.md:31 (§ Scope, other tracked files)

**Claim:**
> `| 3 | Frontmatter description | "and append to wiki log.md" → prepend wording; requires: block added to the frontmatter **(D8)** |`

> "…the tracked missing-`requires:` backlog names three skills … **D8** removes `spec-close` from that list…"

**Why this is wrong:** The `requires:` decision was renumbered D8 → D10 for v2 (the closure manifest says so, and spec.md:193 is `### D10 — requires: block added to the frontmatter`). D8 in v2 is `### D8 — The write is atomic, and a concurrent change is detected` (spec.md:177). Both pointers now land on the atomic-write decision, which says nothing about frontmatter or the lint backlog. The rest of the spec is consistent (spec.md:247 correctly says "The `requires:` block of D10"; spec.md:328 and :340 both cite D10).

**Suggested fix:** Change both occurrences to `D10`.

---

### F-2: D10 cites test case 14; the assertion it describes is test case 16
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:211 (§ Decisions, D10, closing sentence)

**Claim:**
> "`lint.py` validates the vocabulary but never under-declaration, so the fuller block lints identically to the thin one — which is why **test case 14** asserts the declared set against the tool-use notes rather than trusting the lint."

**Why this is wrong:** Test case 14 (spec.md:307) is "**Whitespace discipline** — One blank line above and below the inserted entry…". The requires-vs-body assertion is case **16** (spec.md:309, "`requires:` matches the body"). Done-when #5 (spec.md:328) already cites "test cases 16, 17" correctly, so D10 is the lone straggler — same v1→v2 renumbering that produced F-1. Verified independently that adding the block breaks no existing test: `tests/test_lint.py:48-53` pins only `len(skills) == 8` over `skills/*/SKILL.md` (a new `scripts/` subdirectory does not change that count) and zero ERROR, never the WARN set.

**Suggested fix:** Change "test case 14" to "test case 16".

---

### F-3: D8 and § Design disagree on where the concurrency re-check happens, and the abort path's temp-file cleanup is unspecified
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:183 (D8, "Concurrency") vs. spec.md:241 (§ Design, `main()` walkthrough)

**Claim:** D8:
> "The script captures `os.stat()` (`st_mtime_ns`, `st_size`) immediately after reading and **re-checks it immediately before `os.replace`**; a mismatch exits 2 with `log.md changed under us — re-run`."

§ Design:
> "…→ `splice()` → **re-`stat` and compare → write atomically (D8)** → exit 0."

**Why this is wrong:** These place the re-check on opposite sides of the temp-file write. D8's placement is the one its own rationale demands ("it closes the multi-second window this script actually opens"); § Design's places the check *before* the whole `mkstemp` → write → `fsync` → `close` sequence, leaving that window open again after the check has passed.

The two orderings also have different cleanup obligations, and neither is specified. Under D8's ordering the mismatch is detected with a fully-written temp file on disk, and the abort is a plain `return 2`, not an exception — so `create_handoff.py:352`'s `except BaseException: temp_path.unlink(missing_ok=True)` (the shape spec.md:181 says to reuse) never fires. Test case 11 (spec.md:304) asserts only "exit 2 and unchanged content"; it does not assert the temp file is gone, unlike test case 10 which does for the success and mid-write-failure paths.

The litter would land in the wiki working tree, which `SKILL.md:370` tells the operator to commit with `git add -A`. That is mitigated *only* if the implementer carries over `create_handoff.py:341`'s leading-dot prefix (`prefix=".session-handoff."`), because `vigil-harbor-wiki/.gitignore` ignores `.*.tmp` (added for INFRA-27's plane-sync atomic-write residue) — but the spec never states the dot prefix as load-bearing, only "reusing the shape of".

Both readings ship working code, which is why this sits below the gate rather than at P1.

**Suggested fix:** Make § Design's walkthrough match D8 — "→ `splice()` → write atomically (D8: mkstemp → fsync → close → **re-`stat` and compare** → `os.replace`)". Add one sentence to D8: the mismatch abort unlinks the temp file before returning 2, and the temp name carries a leading dot so any residue is covered by the wiki's `.*.tmp` ignore. Extend test case 11 to assert no temp file remains.

---

### F-4: Done-when #1 cites test case 15 as its evidence, but test 15 cannot see three of the eight sites
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:324 (Done when #1); spec.md:308 (test case 15)

**Claim:**
> "1. `/spec-close` prepends, and **all eight** `SKILL.md` sites (lines 3, 204, 309, 343, 365, 380, 381, 396) plus `AGENTS.md:29`/`:100` … read consistently. — § Scope; § Design "the eight sites"; **test case 15**."

> "15. **No append wording survives.** `grep -in "append"` over `skills/spec-close/SKILL.md` — **expected count: 0**."

**Why this is wrong:** `grep -in "append"` over the current file returns exactly four hits — lines 3, 309, 343, 365 (verified). Sites **204, 380, and 396** carry no "append" wording at all; what makes them in-scope is the retired `grep -F` guard:

```
204: … Phase 5's idempotency guard (`grep -F "close | <PROJECT> — <TICKET-ID>:"`) prevents duplicates …
380: - Bash for … `grep -F` (idempotency check), `grep -rlw` / `grep -c` …
396: - **Log-guard encoding.** The `grep -F` idempotency pattern depends on the literal em dash (`—`) …
```

A shipped `SKILL.md` that reworded the four append sites and left all three `grep -F` sites untouched passes test 15 at count 0 and satisfies every other cited test. That is exactly the drift round-1 correctness F-1/F-2 and edge-cases F-7 were about — the *edits* are now correctly scoped, but the standing tripwire the spec cites as their acceptance evidence covers only half of them. Edge-cases F-7's suggested fix explicitly asked for the `grep -F` half ("Widen test case 14's grep to also assert that `grep -F` no longer appears in `SKILL.md` in an idempotency context"); the spec closed the scope half and dropped the test half.

**Suggested fix:** Extend test case 15 with a second count assertion — `grep -n 'grep -F' skills/spec-close/SKILL.md` expected count **0** (all four current occurrences are in the edit set, so zero is achievable and is the correct target once the guard moves into the script). Or, if line 380's bullet is meant to retain a `grep -F` mention for some other use, state the expected count explicitly rather than leaving it uncovered.

---

### F-5: The invocation's interpreter is never named (residual of round-1 edge-cases F-3)
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:185-191 (D9); spec.md:258, :262 (§ Design, lines 343 and 380)

**Claim:** D9 resolves *where* the script lives — "`~/.claude/skills/spec-close/scripts/prepend_log_entry.py`, honoring `$CLAUDE_CONFIG_DIR`, `%USERPROFILE%\.claude\…` on Windows" — and § Design says Phase 5 step 4 carries "the invocation, shown with a quoted heredoc".

**Why this is wrong:** Nothing in the spec says whether the invocation is `python <path>`, `python3 <path>`, or a bare `<path>`. D9's own worked counter-example is written `python skills/spec-close/scripts/prepend_log_entry.py …`, and § Test command (spec.md:320) says "Pin `python` by full path if more than one interpreter is on `PATH`" — but that clause is scoped to running the tests, not to the runtime call. A bare `scripts/prepend_log_entry.py` is not directly executable from Git Bash on Windows (no shebang dispatch), which is the shell the tool-use notes at `SKILL.md:380` assume.

This is a partial closure, not a reopening: D9 fully closes the P1-driving half of edge-cases F-3 (cwd is the target repo, so a repo-relative path silently fails everywhere but vigil-skills), and the omission mirrors shipped precedent — `skills/session-handoff/SKILL.md:44,50` invoke `create_handoff.py` / `validate_handoff.py` by bare name with no interpreter. That precedent is what D9 cites, and it is accurate, which is why this is P2 rather than P1.

**Suggested fix:** One clause in D9: the invocation is written `python <resolved-path>` (Windows) / `python3 <resolved-path>` (Unix), or state that the interpreter prefix is deliberately left to the harness, matching `session-handoff`, and that the not-found halt message at spec.md:191 covers a failed resolution either way.

---

### F-6: Test case 9's read-only-target assertion is Windows-only
**Severity:** P3
**Where:** spec.md:302 (test case 9)

**Claim:**
> "9. **Exit 1 is reserved.** A **read-only target** (and, separately, a directory as `<log-path>`) exits **2**, not 1…"

**Why this is wrong:** D8 makes the write a temp-file-plus-`os.replace`, and on POSIX `os.replace` is governed by the *directory's* write permission, not the target file's mode bits. `chmod 0444 log.md` followed by `os.replace(tmp, log.md)` **succeeds** on Linux/macOS — the test would fail there by writing the file and exiting 0. On Windows the target's read-only attribute does make `os.replace` raise `PermissionError`, which is presumably where the case was drafted. The directory-as-`<log-path>` half is portable (`PermissionError` on Windows, `IsADirectoryError` on POSIX, both → exit 2).

**Suggested fix:** Either make the *parent directory* read-only (portable on POSIX; note it is a no-op on Windows), or keep the read-only-file case and skip it off Windows, or lean on the directory-as-target case alone, which already proves the property test 9 exists to prove.

---

### F-7: Test case 15's `AGENTS.md` half is stated two ways at once
**Severity:** P3
**Where:** spec.md:308 (test case 15)

**Claim:**
> "…**expected count: 0**. Same assertion over `AGENTS.md` **lines 29 and 100 specifically**. **Stated as a count, not an allowlist**, so a future edit reintroducing "append the entry" fails the suite."

**Why this is wrong:** "A count, not an allowlist" and "lines 29 and 100 specifically" are different assertions. A whole-file count over `AGENTS.md` is achievable — `grep -in "append" AGENTS.md` returns exactly lines 29 and 100 today, both in the edit set — and is what the stated rationale ("a future edit reintroducing…fails the suite") requires. A line-pinned assertion delivers the opposite: it goes stale the moment anything above line 29 shifts, and it would not catch a reintroduction elsewhere in the file.

**Suggested fix:** Pick the whole-file count for `AGENTS.md` too, and drop "lines 29 and 100 specifically" (keep them as the § Scope pointer, where they belong).

---

### F-8: "Files to leave alone" carves line 204 out of Phase 3 but leaves Phase 4 flat, while line 309 sits inside Phase 4
**Severity:** P3
**Where:** spec.md:43 (§ Scope, "Files to leave alone")

**Claim:**
> "`skills/spec-close/SKILL.md` outside the eight sites above — Phases 0–2, **Phase 4**, the Plane state gate, the archive step, and **Phase 3 apart from line 204's guard parenthetical**."

**Why this is wrong:** `SKILL.md`'s `## Phase 4 — Consolidated confirmation` spans lines 282–317 (verified against the heading map), so site 309 — the close-plan template, one of the eight — is inside Phase 4. The umbrella clause "outside the eight sites above" does resolve it, which is why this is not the P0 round-1 F-1 raised. But the sentence then carves 204 out of Phase 3 explicitly, which signals that the umbrella clause is *not* being relied on — and an implementer who reads the asymmetry as meaningful concludes Phase 4 is fully off-limits and skips 309. (Similarly, "the archive step" is Phase 5 step 3, while sites 343 and 365 are Phase 5.)

**Suggested fix:** Drop the redundant "apart from line 204's guard parenthetical" carve-out (the umbrella clause covers it), or add the matching one for Phase 4/309 so the treatment is uniform.

---

### F-9: D8's concurrency detection has no baseline on the missing-file path
**Severity:** P3
**Where:** spec.md:183 (D8, "Concurrency"); spec.md:160 (D7, Missing-file row)

**Claim:**
> "The script captures `os.stat()` … immediately after reading and re-checks it immediately before `os.replace`; a mismatch exits 2."

**Why this is wrong:** When `log.md` is absent there is nothing to `stat`, so the missing-file outcome has no baseline to compare against. A concurrent writer that creates `log.md` between this script's existence check and its `os.replace` is clobbered silently — the same lost-write D8 exists to detect, on the one path where the detection does not apply. Narrow (it requires a fresh wiki plus a concurrent writer), and D8 is explicit that this is detection rather than locking, so this is a completeness note, not a design objection.

**Suggested fix:** One clause in D8: on the missing-file outcome the script asserts non-existence again immediately before `os.replace` (or uses `os.link`/`O_EXCL` to reserve the name, matching `create_handoff.py:330`'s `open(claim, "xb")` reservation), and exits 2 with the same `changed under us` message if the path has appeared.

## Summary
P0: 0 | P1: 0 | P2: 5 | P3: 4 | P4: 0

STATUS: GREEN
