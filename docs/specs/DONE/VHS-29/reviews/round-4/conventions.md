# Conventions Review — round 4

Grounding verified fresh from disk this pass: spec v4 and brief; `CLAUDE.md` → `AGENTS.md` (full); `skills/spec-close/SKILL.md` (all nine cited lines + 382 verified at their stated numbers, file is 400 lines); `skills/ship-spec/SKILL.md:41`, `skills/spec-cycle/SKILL.md:1-11,235`; `docs/portability-contract.md:35-103`, `docs/authoring-portable-skills.md:41`; `lint.py` (`_read_lines`, `_validate_requires_value`, `SERVICES_VOCAB`, `lint_path`), `sync.py:29-45`, `tests/test_lint.py:36-81`, `tests/test_session_handoff.py:91,471,567`; `skills/session-handoff/scripts/{_sections.py:76,create_handoff.py:338-357}`; root + `tests/fixtures/` `.gitattributes` plus live `git check-attr`; root `.gitignore`; `docs/specs/DONE/VHS-28/{spec.md,brief.md,reconciliation.md}`. Wiki: `projects/vigil-skills/{state,filemap}.md`, `decisions/` (VHS-18 lint-warn-only, both VHS-28 entries incl. the D0 Revisit-trigger table), live `log.md` (514 lines / 149,495 bytes / zero `\r`), `.gitignore:8`, `.claude/skills/wiki-after-merge/SKILL.md:35-42`. `scale_lens: off` — no `scalability.md` in `round-3/`; nothing to ignore.

Independent re-verification of the spec's load-bearing counts: `grep -in "append" skills/spec-close/SKILL.md` → 4 (3, 309, 343, 365); `grep -n "grep -F"` → 4 (204, 343, 380, 396); the 4/3/1/1 breakdown holds. A repo-wide `git grep -in append -- '*.md' ':!docs/specs' ':!tests'` confirms **no tenth site**. `grep -n "test case [0-9]"` over the spec → **zero hits**.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 (P1) | CRLF fixture cannot survive a checkout | **CLOSED** | § Files to create drops `log-crlf.md`; § Scope ¶ "No CRLF fixture is checked in" carries the `git check-attr` output (re-verified today: `text: set`, `eol: lf`); both `.gitattributes` named in § Files to leave alone; § Out of scope bullet; § Fixtures + the newlines case say "built in-test", matching `tests/test_session_handoff.py:471` |
| conventions | F-2 (P1) | Four stale numeric test pointers (3rd-round drift) | **CLOSED** | Fixed at the root, not patched: spec:5 Citation convention; every citation now by title. `grep -n "test case [0-9]"` → 0 hits. All 79 `D<n>` citations re-audited by grep, each resolves |
| conventions | F-3 (P3) | § Deferred not applied to v3's own additions | **CLOSED** | Grew 7 → 11; both named items (D5's never-abort rule at :451, `AGENTS.md:100` at :457) present. *A new variant appears in v4 — F-2 below* |
| conventions | F-4 (P3) | Test 18's blanket zero-append over `AGENTS.md` | **CLOSED** | Option (a) taken exactly: whole-file counts kept for `SKILL.md`, `AGENTS.md` asserted on **content** located by substring, never index, with the living-doc + wrong-subsystem rationale (:407) |
| conventions | F-5 (P3) | D6 re-implements `normalize()` without a duplication note; silent strictness divergence | **PARTIAL** | Duplication note + strict-decode rationale landed (:192). The BOM/newline **order** divergence is still neither aligned nor explained — and :192 now asserts an exactness the precedent does not have. See F-1 below |
| conventions | F-6 (P4) | Shebang / `requires:` position | CLOSED (r3) | :310, :288 unchanged |
| correctness | F-1 (P1) | Four stale test-case citations | **CLOSED** | as conventions F-2 |
| correctness | F-2 (P2) | `exit 127` wrong attribution | **CLOSED** | :166 attributes 127 to a missing interpreter only; :264 `test -f` pre-check emits the install hint |
| correctness | F-3 (P3) | Baseline taken after the read | **CLOSED** | :226 `os.fstat(handle.fileno())`; :240 states the rename/inode-swap reason |
| correctness | F-4 (P3) | Tail invariant unachievable on the normal outcome | **CLOSED** | :214 "Tail, scoped honestly" + `log-no-trailing-newline.md` fixture |
| correctness | F-5 (P3) | `SystemExit` swallowed | **CLOSED** | :168, :328 — re-raised alongside `KeyboardInterrupt`, argparse codes pass through |
| correctness | F-6 (P4) | `chmod` between re-stat and swap | **CLOSED** | :231-232 — `chmod` precedes the re-stat, which is now last before `os.replace` |
| correctness | F-7 (P4) | BOM/newline order stated both ways | **CLOSED** | :186, :209, :326 all state one order. *Internally consistent; diverges from precedent — F-1 below* |
| edge-cases | F-1 (P0) | Three stale test cross-refs | **CLOSED** | as conventions F-2 |
| edge-cases | F-2 (P2) | Boundary-line re-termination falsifies D6's absolute claim | **CLOSED** | :188 bounds the claim explicitly; the newlines case asserts *that line's* terminator rather than a self-immunizing blanket |
| edge-cases | F-3 (P2) | Concurrency baseline after the read | **CLOSED** | as correctness F-3 |
| edge-cases | F-4 (P2) | Three-way exit never observable | **CLOSED** | :141 `echo "prepend_log_entry_exit=$?"`; :164 states why the harness signal is insufficient |
| edge-cases | F-5 (P2) | Guard/path never shell-quoted | **CLOSED** | :144-147 — both quotings with the pipeline-split and backslash-eaten-path failure traces |
| edge-cases | F-6 (P2) | Missing script exits 2, not 127 | **CLOSED** | :166 + :264 |
| edge-cases | F-7 (P2) | Test 10 unreachable via `subprocess` | **CLOSED** | Split into (a) `subprocess` DEVNULL and (b) in-process stub, with the Windows-`NUL`-is-a-tty note |
| edge-cases | F-8 (P2) | In-process seam forbidden by the division of labour | **CLOSED** | :373-376 — the division of labour now names the seam, the `.buffer`-over-`BytesIO` stdin stub, and why the precedent helper is insufficient |
| edge-cases | F-9 (P3) | Created file inherits `mkstemp`'s 0600 | **CLOSED** | :243 "Mode is set on both paths" (`0o666 & ~umask`); the Mode case |
| edge-cases | F-10 (P3) | Tail invariant vacuous | **CLOSED** | as correctness F-4 |
| edge-cases | F-11 (P3) | Catch-all message shape unspecified | **CLOSED** | :170 gives the exact form plus the pre-argparse carve-out |
| edge-cases | F-12 (P3) | Bash-only invocation in a harness-neutral repo | **CLOSED** | D9 PowerShell here-string (:268-274) |
| edge-cases | F-13 (P4) | `--help` exits 2 | **CLOSED** | as correctness F-5 |

25 CLOSED, 1 PARTIAL. No REOPENED. The renumbering drift that ran for three consecutive rounds is fixed at the root rather than patched again — that was the right call.

## Findings

### F-1: D6's normalizer note claims the sequence "is exactly" `_sections.normalize()`, but the two run in different orders — the divergence round 3 asked about is still unrecorded
**Severity:** P3
**Where:** spec.md:192 (D6, "On re-implementing the normalizer"); spec.md:186, :209, :326 (the stated order)
**Convention violated:** Reuse-vs-duplicate / accuracy of a cited precedent. Round-3 conventions F-5 asked for three things; two landed, this one did not, and the fix introduced a false equality claim in the same sentence.
**Evidence:** The spec states its order three times consistently — decode → **normalize newlines** → **strip BOM** → `.strip()` (`:186`, `:209`, `:326`) — then at `:192` says:

> Decode → normalize newlines → strip BOM is exactly `skills/session-handoff/scripts/_sections.py:76` `normalize()`

The shipped function runs the opposite order:

```python
text = raw.decode("utf-8", errors="replace")
if text.startswith("﻿"):
    text = text[1:]
return text.replace("\r\n", "\n").replace("\r", "\n")
```

Decode → **strip BOM** → **normalize newlines**. Both orders are correct (U+FEFF is untouched by newline folding, and `\r\n` folding cannot manufacture a BOM), so nothing breaks. But round-3 F-5 named this exact divergence and asked to "align the BOM-strip/newline-fold order with the precedent unless there is a reason not to." v4 did neither, and the new paragraph now asserts an identity that a reviewer checking `_sections.py:76` will find is not one — in the one paragraph written to pre-empt a duplication finding. `lint.py:63` `_read_lines` follows the precedent's order too, so the spec's order is the outlier of three.
**Suggested fix:** One of two one-line edits. Either flip the spec's stated order to decode → strip BOM → normalize newlines in all three places (`:186`, `:209`, `:326`), which makes `:192`'s "exactly" true and matches both precedents; or keep the order and correct `:192` to *"the same three operations as `_sections.py:76` `normalize()` and the decode-then-BOM-strip pair in `lint.py:63`, in a different but equivalent order — U+FEFF is untouched by newline folding, so the sequence commutes."*

---

### F-2: § Deferred still omits one v4-introduced Phase-5 addition — D9's `test -f` pre-check and its install-hint failure line
**Severity:** P3
**Where:** spec.md:444-458 (§ Deferred); spec.md:264 (D9, "Not-found is detected by an explicit pre-check"); spec.md:345 (§ Design, Phase 5 step 4's contents)
**Convention violated:** The spec's own § Deferred inclusion criterion (`:446` — "Additions the brief does not explicitly authorize … Recorded here so the Phase 3 drift check surfaces them rather than a reader discovering them in the diff"), and the drift-check contract `/spec-cycle` Phase 3 renders from it. This is a new variant of round-3 conventions F-3, not a reopening — the two items that finding named are both present now.
**Evidence:** v4 added a new shell command and a new operator-facing failure message to Phase 5 step 4:

> Phase 5 step 4 runs `test -f "<resolved-path>"` before invoking. On failure it prints `log.md NOT written: prepend_log_entry.py not found at <path> — install with 'python sync.py install'` and, per D5, the close still runs step 5 and prints its completion block.

The brief discusses neither script resolution nor a not-found path — its § Open questions ask only about CLI surface, exit codes, in-place-vs-stdout, and guard placement. This is brief-unauthorized new Phase-5 failure-path behavior of exactly the shape § Deferred already lists twice: *"D5's never-abort-the-close rule — new Phase 5 failure-path behavior the brief does not discuss"* (`:451`) and *"D5's echoed exit code — Phase 5 step 4 branches on `prepend_log_entry_exit=$?`"* (`:452`). It has full rationale in D9, so it is class (c), not a silent addition — but § Deferred is where this spec has routed class-(c) items since round 1, and `:455` already lists the *smaller* half of the same decision (the PowerShell form) while leaving the larger half out.
**Suggested fix:** Add one bullet to § Deferred: *"**D9's not-found pre-check** — `test -f` before the invocation plus an install-hint failure line, new Phase 5 behavior the brief does not discuss; needed because a missing script and a refusing script both exit 2, so the actionable hint cannot be inferred after the fact."*

---

### F-3: Site 26 makes `spec-close` the only skill that honors `$CLAUDE_CONFIG_DIR` for `states.json` — the same file `ship-spec` and `spec-cycle` read under the old rule
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:20 (§ Scope, site 26); spec.md:262 (D9's rationale for bringing it along); spec.md:336 (§ Design); spec.md:456 (§ Deferred)
**Convention violated:** Single source of truth for a shared config-file resolution rule across the spec-lifecycle skill family. D9's own stated principle — *"Rather than ship one file with two different config-dir rules — the same class of drift this ticket exists to fix"* — applies one level up as well.
**Evidence:** `skills/ship-spec/states.json` is read by three skills, and today all three state the identical two-default rule:

- `skills/spec-close/SKILL.md:26` — `` Read `~/.claude/skills/ship-spec/states.json` (`~/.claude/` on Unix; `%USERPROFILE%\.claude\` on Windows) ``
- `skills/ship-spec/SKILL.md:41` — `` from `~/.claude/skills/ship-spec/states.json` — `~/.claude/` on Unix; `%USERPROFILE%\.claude\` on Windows — as installed by `sync.py` ``
- `skills/spec-cycle/SKILL.md:235` — `` Read `~/.claude/skills/ship-spec/states.json` (`~/.claude/` on Unix; `%USERPROFILE%\.claude\` on Windows) (installed by `sync.py`) ``

`grep -rn "CLAUDE_CONFIG_DIR"` over the repo returns only `sync.py:14,36,180` and `README.md:40` — **no skill mentions it today**. Site 26 makes `spec-close` the first and only one. On a machine with `$CLAUDE_CONFIG_DIR` set, `/spec-cycle` and `/ship-spec` would look for `states.json` at `~/.claude` (where `sync.py install` never wrote it) while `/spec-close` finds it — three consecutive phases of one lifecycle disagreeing about where their shared config lives. The spec trades a genuine intra-file inconsistency (which D9 itself creates) for a new cross-file one across three skills, and does not acknowledge the trade anywhere: § Deferred's bullet says only *"a nine-word edit outside the brief's site list, taken so the file does not ship two different config-dir rules."*

This is P2, not P1: the spec correctly notes the env var is unset on the operator machine, so nothing breaks today, and I verified nothing in the repo sets it.
**Suggested fix:** Either (a) keep site 26 and add one sentence to D9 acknowledging the consequence and its owner — *"This makes `spec-close` the only skill honoring `$CLAUDE_CONFIG_DIR`; `ship-spec:41` and `spec-cycle:235` read the same file under the two-default rule. Sweeping all three is a separate ticket, filed rather than done here, because the env var is unset today"* — or (b) drop site 26 and instead scope D9's env-var rule to script resolution only, noting that `states.json` resolution is a three-skill convention that a follow-up sweeps. (a) is the smaller edit and preserves D9's argument; (b) leaves the repo strictly consistent.

---

### F-4: The wiki's tracked "3 missing-`requires:` WARNs" count goes stale on merge, and § Design "Wiki-side step" — the spec's own vehicle for out-of-PR wiki edits — does not name it
**Severity:** P4
**Where:** spec.md:298 (D10's backlog clearing); spec.md:361-367 (§ Design "Wiki-side step")
**Convention violated:** Prior-decision hygiene. `decisions/2026-06-14-vhs-18-lint-warn-only-strict-gate.md` is `Status: active` and its promotion path is tracked in two places the spec does not touch.
**Evidence:** D10 correctly updates the in-repo backlog at `docs/authoring-portable-skills.md:41` from three skills to two. Two wiki mirrors of the same count will then be wrong:

- `projects/vigil-skills/filemap.md:164` — *"still exactly 3 tracked `missing-requires` WARNs (ship-spec/spec-close/review-pr)"*
- `decisions/2026-06-14-vhs-18-lint-warn-only-strict-gate.md` § Related — *"Tracked backlog: annotate ship-spec/spec-close/review-pr `requires:` blocks → `--strict` pre-commit hook."*

The spec already carries an out-of-PR wiki step with its destination named, so the pattern exists. Arguably `/spec-close`'s own wiki decomposition and `/wiki-after-merge`'s filemap delta catch both — which is why this is P4, not P3.
**Suggested fix:** Add one clause to § Design "Wiki-side step": *"Also stale after merge, and left to `/spec-close` / `/wiki-after-merge` rather than done here: `projects/vigil-skills/filemap.md:164` and the VHS-18 decision's Related line both say three tracked `missing-requires` WARNs; it becomes two."*

---

### F-5: The in-process interposition seam is described as "monkeypatched" without naming the repo's existing mechanism
**Severity:** P4
**Where:** spec.md:376 (§ Test plan, "a named monkeypatched seam")
**Convention violated:** The spec's own discipline of citing every precedent by `file:line` — it does so for the stdin stub (`tests/test_session_handoff.py:91`), the CRLF construction (`:471`), the atomic write (`create_handoff.py:338`), and `newline="\n"` (`:347`). This one seam is the exception.
**Evidence:** The repo already has the exact idiom, in the suite this spec follows: `tests/test_session_handoff.py:567` does `with mock.patch.object(self.C.os, "replace", side_effect=OSError("boom")):` — which is precisely the "forced mid-write failure" the atomic-write-and-temp-hygiene case needs, and `:599` patches a module attribute the same way. "Monkeypatched" leaves the implementer to reinvent it (`setattr` + `try/finally` is a plausible and worse reading).
**Suggested fix:** Change `:376` to *"a named seam patched with `unittest.mock.patch.object` over the module's `splice` (or `os.fsync`), matching `tests/test_session_handoff.py:567`, which patches `os.replace` with `side_effect=OSError` for the same purpose."*

---

### F-6: One case citation is not by title, against the citation convention the spec declares at line 5
**Severity:** P4
**Where:** spec.md:188 (D6, "Preservation, stated exactly")
**Convention violated:** spec.md:5 — *"Test cases are referred to by **title**, never by number."*
**Evidence:** `:188` says *"the CRLF test case asserts *that specific line's* terminator."* There is no case titled "CRLF"; the case is **Newlines, all three directions**. Every other case reference in the spec resolves to its title (`grep` over all of them: no-stale-wording, header-corruption, anchor unit test, read-side refusal, write-side heading validation, fresh wiki, missing file, `requires:`-matches-the-body, lint — all present, all bolded). This one is un-bolded and descriptive, so it reads as prose rather than a formal pointer, but it is the one place a reader has to hunt — and the convention was declared this round specifically to end hunting.
**Suggested fix:** `:188` → *"the **newlines** case asserts *that specific line's* terminator."*

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 2 | P4: 3

STATUS: GREEN
