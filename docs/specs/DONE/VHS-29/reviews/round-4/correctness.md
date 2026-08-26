# Correctness Review — round 4

**Grounding (all read fresh from disk this pass):** spec v4 (459 lines) and `VHS-29.brief.md`; `CLAUDE.md` → `AGENTS.md`; all three round-3 reports (`scale_lens: off` — no `scalability.md` in `round-3/`, nothing to ignore). Plane VHS-29 retrieved from namespace `skills` (tag-exact, 1 hit; description matches the brief's Why/Done-when).

**Every code claim in the spec re-verified against the live files.** `skills/spec-close/SKILL.md` is 400 lines; all ten cited sites (3, 26, 204, 309, 343, 365, 380, 381, 382, 396) confirmed at their stated numbers, and the 381-vs-382 off-by-one correction in § Scope is right (381 is the Write-targets bullet, 382 is the mutation boundary). `grep -in "append"` → exactly 4 (3, 309, 343, 365); `grep -n "grep -F"` → exactly 4 (204, 343, 380, 396) — the spec's 4/3/1/1 breakdown of the nine sites is correct. `AGENTS.md` `append` hits are exactly 29 and 100. `docs/authoring-portable-skills.md:41` is the three-skill backlog sentence. `sync.py:30` `SUBTREES = ("skills", "agents")`, `:36` `CLAUDE_CONFIG_DIR`, `iter_files` is an unfiltered `rglob`. `create_handoff.py:338` `write_atomically`, `:347` the `newline="\n"` open. `_sections.py:76` `normalize()`, `lint.py:63` `_read_lines` — both `errors="replace"`. `spec-cycle/SKILL.md:5-10` is the `requires:` block after `user_invocable:`; `portability-contract.md` "Uniqueness / position" confirms the rule. `SKILL.md:34`/`:74`/`:378`/`:379` back D10's `network`/`services` claims; `grep -in subagent` returns nothing. All three shipped scripts are git mode `100644`. `test_session_handoff.py:91` is `run_main`, `:471` is the in-test CRLF `write_bytes` — both anchors exact. `tests/test_lint.py:48-58` pins `len(skills) == 8` over `skills/*/SKILL.md`, so the new `scripts/` dir owes no tripwire bump.

**Measured on this machine:** `python -V` = 3.14.3; `sys.stdout.encoding`/`errors` = `cp1252`/`surrogateescape`; `python lint.py skills/spec-close/SKILL.md` → `0 error(s), 1 warning(s)` (`missing-requires`), and `missing-requires`/`unreadable` are the only WARN rules in `lint.py`, so D10 does clear it to zero. Live wiki `log.md` = 514 lines / 149,495 bytes / zero `\r`; every one of its 31 `close | ` occurrences is an entry heading, none body prose (D4's asymmetry rationale holds). `git check-attr -a tests/fixtures/spec-close/log-crlf.md` → `text: set`; `tests/fixtures/crlf-skill/SKILL.md` → `text: unset` — conventions/F-1's evidence reproduced exactly.

**`git log -10` on the touched files:** `skills/spec-close/SKILL.md` last moved `b9afacd` (2026-06-14) — nothing in 7 days. **`AGENTS.md` moved yesterday** (`40c4bb8`, 2026-08-24, VHS-28); both cited lines re-verified as current and still the file's only `append` occurrences. `docs/authoring-portable-skills.md` last moved `7ec40ca`. No spec-relevant code has shifted under the plan.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Four stale numeric test-case citations | CLOSED | Root-cause fix: title-based citations throughout + "Citation convention" note (spec:5). `grep -n "case [0-9]\|test [0-9]"` over the spec returns **zero** hits; all title citations resolve to real cases |
| correctness | F-2 (P2) | exit 127 wrong for an unresolved script path | CLOSED | D5:166 attributes 127 to a missing **interpreter** only, states CPython exits 2; D9:264 detects not-found via an explicit `test -f` pre-check |
| correctness | F-3 (P3) | Baseline from `stat(path)` after the read | CLOSED | D8:226 `os.fstat(handle.fileno())` with the inode-swap rationale at :240; § Design:326 matches |
| correctness | F-4 (P3) | Trailing-newline invariant unachievable | CLOSED | D7:214 scopes the tail rule to fresh-wiki/missing-file; `log-no-trailing-newline.md` (:45) makes the normal-outcome assertion non-vacuous |
| correctness | F-5 (P3) | `except BaseException` swallows `SystemExit` | CLOSED | D5:168 re-raises `KeyboardInterrupt` **and** `SystemExit`; § Design:328 states argparse's 0/2 pass through |
| correctness | F-6 (P4) | chmod between re-stat and swap | CLOSED | D8:231-233 — chmod now precedes the re-stat, annotation is literally true |
| correctness | F-7 (P4) | BOM/newline order stated both ways | CLOSED | D6:186, D7:209, § Design:326 all read normalize-newlines → strip-BOM → strip. (Residual nit on the precedent-parity claim → **F-6** below) |
| edge-cases | F-1 (P0) | Stale citations (reopen of correctness/F-2 r2) | CLOSED | as correctness F-1 |
| edge-cases | F-2 (P2) | Separator normalization falsifies D6's absolute claim | **PARTIAL** | CRLF half fully closed: D6:188 bounds the exception to the boundary line, and the newlines case (:405) asserts *that line's* terminator. The BOM half is stated but not implemented → **F-3** below (keeps P2) |
| edge-cases | F-3 (P2) | Baseline captured after the read | CLOSED | as correctness F-3 |
| edge-cases | F-4 (P2) | Three-way exit code never observable | CLOSED **for the Bash form** | D5:141 `echo "prepend_log_entry_exit=$?"` on its own line; D5:164 states the skill branches on the integer. The PowerShell form added in the same revision has no counterpart — raised as **NEW F-2**, not a partial |
| edge-cases | F-5 (P2) | Guard/path never shell-quoted | CLOSED | D5:136 shows both quotings; :144-147 "Both quotings are load-bearing" covers the `|`-pipeline and the Windows-backslash exit-0 case |
| edge-cases | F-6 (P2) | Missing script exits 2, not 127 | CLOSED | as correctness F-2 |
| edge-cases | F-7 (P2) | Test 10 precondition unreachable; Windows `NUL` | CLOSED | No-stdin case split into subprocess (union match, `NUL` comment) + in-process stub halves (:399); D5:151 carries the platform note |
| edge-cases | F-8 (P2) | Cases 12/13 need a forbidden in-process seam | CLOSED | § Test plan "Division of labour" (:373-376) names the in-process path, both required halves of the `sys.stdin` stub with the two traps, and a named monkeypatched seam |
| edge-cases | F-9 (P3) | Missing-file path inherits `mkstemp`'s 0600 | CLOSED | D8:243 covers both paths; the mode case (:403) asserts both. (Residual on the `~umask` primitive → **F-5**) |
| edge-cases | F-10 (P3) | Tail invariant / test 17 vacuous | CLOSED | as correctness F-4 |
| edge-cases | F-11 (P3) | Catch-all message shape unspecified | CLOSED | D5:170 gives the concrete format with the before-argparse carve-out |
| edge-cases | F-12 (P3) | Invocation Bash-only in a neutral repo | CLOSED | D9:266-274 adds the PowerShell here-string form as asked. Whether that form *works* is a new question → **F-1**, **F-2** |
| edge-cases | F-13 (P4) | `SystemExit` swallowed | CLOSED | as correctness F-5 |
| conventions | F-1 (P1) | CRLF fixture cannot survive its own commit | CLOSED | `log-crlf.md` dropped from § Files to create; § Scope:47 carries the full rationale incl. the verified `check-attr` output; both `.gitattributes` in § Files to leave alone (:52); § Out of scope:434 names it; the newlines case builds CRLF in-test per `test_session_handoff.py:471` |
| conventions | F-2 (P1) | v2→v3 renumbering left four pointers wrong | CLOSED | as correctness F-1 |
| conventions | F-3 (P3) | § Deferred doesn't apply its criteria to v3's additions | CLOSED | § Deferred now carries eleven items (:448-458) |
| conventions | F-4 (P3) | Blanket zero-`append` over `AGENTS.md` over-broad | CLOSED | The no-stale-wording case (:407) keeps whole-file counts for `SKILL.md`, asserts on **content** for `AGENTS.md` |
| conventions | F-5 (P3) | D6 re-implements `normalize()` silently | CLOSED | D6:192 "On re-implementing the normalizer"; strict decode stated as a deliberate choice at :179 |

26 of 27 closed, one PARTIAL. The root-cause fix on citations held: **zero numeric test-case references survive anywhere in the spec.**

## Findings

### F-1: D9's PowerShell here-string pipe destroys the em dash — the one byte D4, D6 and `SKILL.md:396` all call load-bearing
**Severity:** P1
**Where:** spec § D9 (spec.md:266-274); against D4 (spec.md:123), D6 hazard 1 (spec.md:178), § Design (spec.md:347)
**Claim:** D9 mandates a second invocation form for PowerShell hosts:

```powershell
@'
## [YYYY-MM-DD] close | <PROJECT> — <TICKET-ID>: <title>
…
'@ | python "<resolved-script-path>" "<log-path>" --guard 'close | <PROJECT> — <TICKET-ID>:'
```

D6 pins UTF-8 on all four of the script's own I/O surfaces and D4 states that "any tool that normalizes [the em dash] to `--` breaks dedup."

**Why this is wrong:** When PowerShell pipes a string into a native executable it encodes with `$OutputEncoding`, and in **Windows PowerShell 5.1 — this repo's primary shell — that defaults to `ASCIIEncoding`**. Measured:

```
$ powershell.exe -NoProfile -Command "$OutputEncoding.GetType().FullName; @'
## [2026-08-25] close | VHS — VHS-29: title
'@ | python -c 'import sys; print(repr(sys.stdin.buffer.read()))'"
System.Text.ASCIIEncoding
b'## [2026-08-25] close | VHS ? VHS-29: title\r\n'
```

The em dash arrives as `?` (0x3F). The `--guard` value travels through argv (UTF-16 command line) and keeps its em dash, so D5 validation step 3 — "it must appear in the entry's **first line**" — fails on **every** close run through this form, exiting 2 with a message that blames the guard rather than the shell. `SKILL.md:396`'s hazard, which the spec deliberately preserves and re-anchors, is realized by the spec's own new invocation form.

The configured case is also unremarked. On this machine (profile loaded) `$OutputEncoding` is `UTF8Encoding` **with preamble**, and the same pipe delivers:

```
b'\xef\xbb\xbf## [2026-08-25] close | VHS \xe2\x80\x94 VHS-29: title\r\n'
```

— a leading BOM and CRLF terminators. D6 handles both (BOM-on-entry strip at :190, newline normalization at :186), but the spec justifies that handling as a generic hazard; it is in fact the *required* path for the PowerShell form, and the spec never says so.

**Suggested fix:** In D9, show the encoding pin as part of the form, not as a footnote — e.g. prefix the block with `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)` (BOM-suppressing) and state that without it Windows PowerShell 5.1 pipes ASCII and silently replaces `—` with `?`, which D5 step 3 then reports as a guard mismatch. Add one sentence to D6 recording that the PowerShell path is why entry-side BOM stripping and CRLF normalization are load-bearing rather than defensive, and add the BOM+CRLF-prefixed stdin to the em-dash/BOM round-trip case as a named input.

---

### F-2: The PowerShell branch drops both mechanisms D5 and D9 declare mandatory for Phase 5 step 4 — the exit-code capture (`$?` is a Boolean in PowerShell) and the `test -f` pre-check
**Severity:** P1
**Where:** spec § D9 (spec.md:264, :266-274); against D5 (spec.md:141, :164), § Design (spec.md:345, :347)
**Claim:** D5:164 — "**The skill branches on the echoed integer, never on the harness's success/failure signal.** … Hence `echo "prepend_log_entry_exit=$?"` on its own line." D9:264 — "Phase 5 step 4 runs `test -f "<resolved-path>"` before invoking… The pre-check exists because a missing script and a refusing script both exit 2, so the actionable install hint cannot be inferred after the fact." § Design:347 lists "the invocation in both shell forms".

**Why this is wrong:** Both mechanisms are specified in Bash-only syntax and neither is given a PowerShell counterpart, so the branch the spec adds for PowerShell hosts cannot execute the step's own contract:

1. **`$?` is not the exit code in PowerShell.** It is a `[bool]` recording whether the last command succeeded. The literal port — `Write-Output "prepend_log_entry_exit=$?"` — emits `prepend_log_entry_exit=True`/`False`, which collapses the three-way branch back into the pass/fail signal D5:164 forbids, reproducing exactly the misreport round-3 edge-cases/F-4 was raised against: an idempotent skip (exit 1, an *expected* path per `SKILL.md`'s "Partial-then-full re-run" failure mode) reads as `log.md NOT written` with a spurious recovery hint. The correct variable for a native command is `$LASTEXITCODE`, which appears nowhere in the spec.
2. **`test -f` is not a PowerShell command.** It errors (`The term 'test' is not recognized`), the skill reads that as pre-check failure, and takes the not-found branch — the same silent-loss end state as edge-cases/F-1, on an installed script. `Test-Path` is likewise absent from the spec.

D9's stated warrant is `SKILL.md`'s paired-form convention — verified live at `SKILL.md:25` (`$env:USERNAME` / `$USER`) and `:26` (two config paths). Both of those precedents pair the *whole* mechanism, not one of its three parts.

**Suggested fix:** In D9, give the PowerShell branch all three lines, not one: `if (-not (Test-Path "<resolved-script-path>")) { … install hint … }` before the pipe, and `Write-Output "prepend_log_entry_exit=$LASTEXITCODE"` after it, with one sentence noting that `$?` is a Boolean and would silently collapse the three-way branch. Amend § Design:345 and :347 so the line-343 rewrite states the pre-check and the exit-code echo as shell-paired requirements rather than attributing the echo to the Bash form alone.

---

### F-3: D6 asserts the existing file's BOM is dropped "by the `lstrip("﻿")` in step 2" — step 2 operates on the entry, and no specified code path touches the file's BOM
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D6 "Preservation, stated exactly" (spec.md:188); against D5 validation step 2 (spec.md:152), D6 hazard 4 Read (spec.md:184), D6 "BOM on the entry" (spec.md:190), § Design `main()` (spec.md:326)
**Claim:** "The existing file's BOM, if any, is likewise dropped by the `lstrip("﻿")` in step 2 — also named, also bounded."
**Why this is wrong:** There is no such step. D5's numbered validation step 2 is *"**Empty entry** after decode, newline-normalize, BOM-strip, and `.strip()`"* — it operates on the stdin entry, and D6:190's BOM paragraph is titled "**BOM on the entry**" for the same reason. The *file* read is specified at D6:184 as `open(path, encoding="utf-8", newline="")` — `utf-8`, not `utf-8-sig`, and with no strip — and § Design's `main()` walkthrough reads "open the file with `newline=""`, read, `os.fstat` the handle" with no normalization of the existing text at all. As specified, a BOM-prefixed `log.md` **keeps** its BOM.

So the spec states a bounded deviation from its own preservation rule that its implementation does not perform, and attributes it to a mechanism that does not apply to that data. An implementer who follows :188 adds `existing.lstrip("﻿")` and rewrites a byte the same sentence says the script never authors (on the very file the header-corruption case guards — and that case asserts from `# Wiki Log` onward, so a dropped BOM slips past it); one who follows :184 and :326 does not. This is the residual half of round-3 edge-cases/F-2, whose ask was "state whether the existing file's BOM is preserved or dropped": the statement was added, but it contradicts the read path.

**Suggested fix:** Decide and say it once. Preserving is the choice consistent with the rest of D6 — replace the sentence with *"The existing file's BOM, if any, is **preserved**: the file is opened `utf-8`, not `utf-8-sig`, and nothing strips it. Only the **entry**'s BOM is stripped (below), because a BOM mid-file would break `ENTRY_RE`."* If dropping is intended instead, name the actual step, add it to § Design's `main()` walkthrough, and pin it with an assertion.

---

### F-4: The fresh-wiki outcome reports `Prepended: log.md` for an entry placed at the end of the file, and its stderr notice is never surfaced
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D7 outcome table (spec.md:200) vs § D5 exit-code table (spec.md:160) and § Design line-365 rewrite (spec.md:349)
**Claim:** D7: "**Fresh wiki** … Place the entry **after the existing content**; stderr notice `no dated entry found — entry placed at end of file` | 0". D5: "| 0 | Entry written | Report `Prepended: log.md` |".
**Why this is wrong:** Only the exit-2 row surfaces stderr. On the fresh-wiki path the script writes a deliberate operator notice to stderr, exits 0, and the skill — per the specified mapping — prints `Prepended: log.md` and discards the notice. The operator is told the entry was prepended when it was placed at the bottom, with no signal that the file's shape was unusual. That is a milder form of the report this ticket exists to eliminate: D7:203 argues at length that bottom-placement reported as `Prepended: log.md` "is the bug wearing a green success report", and then leaves the one remaining bottom-placement path reporting exactly that string.

The missing-file outcome has the same shape (exit 0, `Prepended: log.md`, over a file that was created rather than prepended to), though there the wording is merely imprecise rather than misleading. Test coverage does not catch it: the fresh-wiki case asserts "exit 0, notice on stderr" — the script side only. Nothing asserts what the skill does with the notice.

**Suggested fix:** Extend the exit-0 row of D5's table and § Design's line-365 rewrite to a two-line mapping: `Prepended: log.md` when the script is silent, and `log.md: <stderr notice>` appended beneath it when the script wrote one. Word the fresh-wiki completion line without "append" (D7's tripwire forbids it) — e.g. `log.md: no dated entry found — entry placed at end of file`.

---

### F-5: `0o666 & ~umask` names a value CPython has no read-only accessor for
**Severity:** P3
**Where:** spec § D8 mode bullet (spec.md:243); the mode case (spec.md:403)
**Claim:** "When it does not [exist], the temp is chmod'd to `0o666 & ~umask` so a created `log.md` matches what a plain `open(path, "w")` would have produced."
**Why this is wrong:** `os.umask()` is the only umask interface in the stdlib and it is a **setter that returns the previous value** — there is no query. Obtaining the value requires `old = os.umask(0); os.umask(old)`, which mutates process-global state for the duration and is not thread-safe. The spec states the target value without stating the primitive, and the obvious naive reading ("read the umask") has no implementation.
**Suggested fix:** Either name the primitive — *"read it with the standard `old = os.umask(0); os.umask(old)` set-and-restore; the script is single-threaded so the window is safe"* — or sidestep it: on the missing-file path, create the target with `os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o666)` (which the kernel masks correctly) and write through that descriptor, skipping `mkstemp` where there is no existing file to replace atomically anyway.

---

### F-6: D6's parity claim about `_sections.normalize()` is inverted on the one axis round-3 asked about
**Severity:** P4
**Where:** spec § D6 "On re-implementing the normalizer" (spec.md:192)
**Claim:** "Decode → normalize newlines → strip BOM is exactly `skills/session-handoff/scripts/_sections.py:76` `normalize()`…"
**Why this is wrong:** `_sections.py:76-87` decodes, strips the BOM, **then** folds newlines — the inverse of D6's order. Functionally identical (newline folding neither creates nor consumes U+FEFF), and v4's internal alignment on normalize-newlines → strip-BOM is the right call — it closed correctness/F-7. But round-3 conventions/F-5 flagged the order inversion specifically and asked for it to be aligned *or stated*; the paragraph does neither, and instead claims equivalence on the axis that differs. The strictness divergence, the other half of that finding, **is** stated (spec:179) and correct — both precedents verified as `errors="replace"`.
**Suggested fix:** "…is the same operation as `_sections.py:76` `normalize()` (which strips the BOM before folding newlines — the inverse order, immaterial since newline folding never touches U+FEFF), and `lint.py:63` `_read_lines` is a third instance of the decode-then-BOM-strip pair."

## Summary
P0: 0 | P1: 2 | P2: 2 | P3: 1 | P4: 1

STATUS: RED P0=0 P1=2 P2=2 P3=1 P4=1
