# Edge-Cases Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: `section_span` contract contradicts itself — the "own content" stripping clause is unreachable, and reintroduces a second matcher
**Severity:** P0
**Where:** `docs/specs/TODO/VHS-28.spec.md:67-76` (docstring) vs `:80` (last sentence of D3); premise at `:78`
**Edge case:** Any section with a nested subsection — i.e. the exact shape the fix targets.
**What happens:** The docstring defines `end` as "the offset of the next heading at ANY depth," so a returned span can never contain a heading line. Line 80 then says "Section content is measured after stripping the trailing/leading whitespace **and any nested heading lines the span does not own**." That clause describes stripping something the span definition guarantees is absent. An implementer reading D3 has two incompatible mental models — (a) span stops at the first child heading, or (b) span runs to the next *sibling-or-shallower* heading and child headings are stripped afterward — and they produce different `incomplete` verdicts for every parent section in the template. Model (b) requires a **second heading matcher** (to identify "lines the span does not own"), which is precisely the "second place to get it wrong" D3 claims at line 78 to have eliminated. This is load-bearing: the whole spec is justified as the *structural* fix for a three-call-site divergence.
**Why the spec misses it:** D3 was written to cover two separate improvements (opener depth, terminator depth) and the sentence at :80 is a leftover from the vendor's model where `##?` let child content bleed in. Nothing in the test plan (`:216-227`) distinguishes the two models — item 1's "a level-3 subsection **terminates** its parent's span" pins model (a), while :80 describes model (b).
**Suggested fix:** Delete the "and any nested heading lines the span does not own" clause from `:80`, and replace with an explicit statement: *"A parent heading's own content is only the text between it and its first child heading. Container headings that carry no prose of their own therefore always measure 0 characters and MUST NOT appear in `REQUIRED_SECTIONS` or `RECOMMENDED_SECTIONS`."* Add a test-plan bullet asserting that invariant against the generated scaffold, so a container heading added to either list fails the suite.

---

### F-2: No text encoding is specified anywhere — on the target machine the platform default is cp1252, so the scaffold write can crash and the validator read silently corrupts measurements
**Severity:** P1
**Where:** spec `:187-197` (`create_handoff.py` — "Writes the file"), `:199-206` (`validate_handoff.py` — "Unreadable/undecodable file")
**Edge case:** Any non-ASCII byte in git metadata, in the template, or in an authored handoff.
**What happens:** Measured on the operator machine: `locale.getpreferredencoding(False)` is **`cp1252`**, `sys.flags.utf8_mode == 0`, `PYTHONUTF8` unset (Python 3.14.3). So `Path.write_text(content)` / `read_text()` without an explicit `encoding=` use cp1252.
- **Write side (crash):** `create_handoff.py` embeds `git log --oneline -5` verbatim. `git log --oneline -60` in *this repo* currently contains `U+FEFF`, which cp1252 cannot encode — `UnicodeEncodeError`, uncaught traceback, **no handoff document produced**, at the exact moment the user is saving context before losing it. Emoji or CJK in a commit subject or a modified filename does the same. Spec `:192` says "**Every git call is wrapped**" — that guards the subprocess, not the write, so the stated defense does not cover this.
- **Read side (silent corruption):** a UTF-8 handoff containing `—`/`→` decoded as cp1252 becomes mojibake with ~3× the character count, which directly inflates the ≥50-character "own content" measurement — a thin section passes the gate. Bytes `0x81/0x8D/0x8F/0x90/0x9D` are undefined in cp1252, so some valid UTF-8 handoffs raise `UnicodeDecodeError` and get reported as "undecodable" (exit 2) when they are fine.
- **BOM:** an existing handoff with a UTF-8 BOM makes the leading `# Handoff: …` H1 unmatchable, so `--continues-from` chain-title extraction silently degrades.
**Why the spec misses it:** The spec inherits the vendor's bare `filepath.write_text(content)` / `path.read_text()` by omission, and the D1 clean-room framing (`:38-44`) only bounded the *secret pattern list*, not I/O discipline. The repo has already solved this: `lint.py:64-73` (`_read_lines`) does `read_bytes()` → `.decode("utf-8", errors="replace")` → BOM strip → `splitlines()`, and `tests/fixtures/bom-skill/`, `tests/fixtures/crlf-skill/` exist precisely to pin it.
**Suggested fix:** Add to the Design section for both scripts: *"All file I/O is explicitly UTF-8. Writes use `encoding='utf-8'`; reads follow `lint._read_lines`' discipline — `read_bytes()`, `decode('utf-8', errors='replace')`, strip a leading BOM — so no valid document is ever reported as undecodable and no locale setting changes the verdict. Git output is captured with `encoding='utf-8', errors='replace'`."* Add test-plan bullets: a scaffold generated in a repo whose HEAD commit subject contains an emoji, and validation of a BOM-prefixed and a CRLF handoff.

---

### F-3: The `tests/test_lint.py` "7 → 8" bump is anchored to an unmerged branch; in ship-spec's worktree the anchor is `4` and the suite is red before any VHS-28 code runs
**Severity:** P1
**Where:** spec `:27` (Modified files table), `:227` (test-plan item 7), `:234-237` (test command + "currently 44 passed")
**Edge case:** Configuration drift between the authoring working tree and the branch `/ship-spec` cuts from.
**What happens:** `skills/ship-spec/SKILL.md:76` cuts the implementation worktree as `git worktree add -b <branch> <path> origin/<default-branch>`. Verified:

| Ref | `skills/*/SKILL.md` on disk | `test_lint.py` assertion |
|---|---|---|
| `origin/main` (a0ad847) | **5** | **4** |
| `HEAD` (feat/tal-003-talaria-skill, 8 ahead) | 7 | 7 |

In the ship-spec worktree the literal `7` the spec tells the implementer to edit **does not exist in the file** (it reads `4`), and `test_shipped_skills_clean` is *already failing* there (5 ≠ 4) before session-handoff is added. Adding the skill makes 6, and the specified target of 8 is wrong by two. The implementer hits an unexplained red gate on the first test run and burns ship-spec's 5-iteration budget chasing a phantom — with an error message ("if you added a skill, bump this count") that actively points at the wrong cause.
**Why the spec misses it:** The spec was authored against the current working tree, where commits `386dc6c` (bloat-check), `8946f58` (hermes-kanban-awareness) and `7a3a929` (tripwire 4→7) are present but unmerged. Same root for the "currently `44 passed, 8 subtests passed`" baseline at `:237` — that is this branch's number, not the base branch's.
**Suggested fix:** Replace the row at `:27` with an order-independent instruction: *"Bump the shipped-skill inventory tripwire to `len(glob('skills/*/SKILL.md'))` **as observed in the implementation worktree** (currently `4` on `origin/main`, `7` on the unmerged feature branch — read the file, do not assume `7`)."* Add a Preconditions note stating whether VHS-28 stacks on `feat/tal-003-talaria-skill` or on `origin/main`, and drop or re-anchor the `44 passed` baseline.

---

### F-4: Existing vendor-generated handoff documents are declared load-bearing but nothing in the design or the test plan pins them
**Severity:** P1
**Where:** spec `:133-135` (D8, "Existing handoff documents on disk stay readable and listable"), brief `:61`, test plan `:216-227`
**Edge case:** Running the new validator against the corpus already on disk — including the very document that surfaced VHS-28.
**What happens:** D4 (`:82-93`) closes the loop between the *new* template and the *new* validator, but the section vocabulary is being re-derived clean-room (D1). If any name or depth shifts — "Immediate Next Steps" → "Next Steps", `### Important Context` promoted to `##`, "Potential Gotchas" renamed — every existing handoff (5 measured on this machine, in two projects) instantly reports required sections `missing` and the RESUME workflow's staleness assessment reads them as broken. There is no version marker in the documents, no compatibility statement, and **no test in items 1–7 that runs the validator against a legacy on-disk document**. The failure is silent in the worst way: a correct historical handoff is reported as `NEEDS WORK`, which is exactly the false signal the ticket was filed about.
**Why the spec misses it:** D4's round-trip test generates its own scaffold, so it is structurally incapable of catching template *drift away from the installed corpus* — it only catches drift between the two new files.
**Suggested fix:** Add to D4 or D8: *"`REQUIRED_SECTIONS` and `RECOMMENDED_SECTIONS` reuse the vendor template's section names and depths verbatim (they are the schema of documents already on disk, not authored expression)."* Add test-plan item: *"Legacy-corpus compatibility — a checked-in fixture under `tests/fixtures/` reproducing the on-disk vendor-generated handoff shape (`## Current State Summary`, `### Important Context`, `### Immediate Next Steps`, footer after `---`) validates with zero `missing`."* Note the fixture must be authored, not copied, per D1.

---

### F-5: D3 unifies the heading *depth* only — separator, end-anchor, leading indent, closing-`#` and case are still per-call-site, which is the same bug class the ticket filed
**Severity:** P1
**Where:** spec `:58-64` (`HEADING = r"#{1,6}"`), `:78` ("There is no second place to get it wrong"), Done-when `:248`
**Edge case:** Heading-shaped lines that are not headings, and headings that don't match the assumed shape.
**What happens:** The vendor's three sites diverged on **two** axes, not one: opener `#{1,6}\s*NAME` (zero-or-more space, IGNORECASE, no end anchor) vs terminator `\n#{1,6}\s+` (one-or-more space). Pinning `HEADING` fixes only the depth axis; every other axis is still decided independently at each call site. Concretely, all of these remain undefined and will diverge again:
- `#Important Context` (no space) — matches the opener under `\s*`, is **not** a heading in CommonMark, and does **not** terminate under `\s+`. A section can therefore open on a non-heading and never close.
- `   ## Immediate Next Steps` (1–3 leading spaces) — a valid ATX heading per CommonMark; `(?:^|\n)#` misses it, so the section reads `missing` on a hand-edited document.
- `## Important Context ##` (ATX closing sequence) — matched by a prefix pattern, but the *name* extraction and any end-anchored variant differ.
- `## Immediate Next Steps (deferred)` — passes a prefix match, fails an end-anchored one. Unspecified which is intended.
- Case: the vendor used `re.IGNORECASE` everywhere; the spec never states whether the rewrite does. `## important context` flipping between `missing` and present is a verdict flip.
- Substring collisions: with no end anchor, a section name that is a prefix of another resolves to whichever appears first, measuring the wrong span.
- Setext headings (`Title\n-----`) are not matched at all, so they neither open nor terminate — content bleeds across them into the parent's 50-char measurement.

Done-when #2 (`:248`) claims the fix is delivered "**structurally**, via the single `section_span` helper." One shared depth constant does not deliver that.
**Why the spec misses it:** The brief framed the bug as a regex-width bug ("`##?` → `#{1,6}`, three places"), and D3 inherited that framing. The second-order defect D3 *does* catch (terminator depth) shows the author saw the pattern but stopped at depth.
**Suggested fix:** Replace `HEADING = r"#{1,6}"` with a single fully-specified compiled matcher and state its semantics explicitly in D3 — e.g. *"`_HEADING_RE = re.compile(r'^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$', re.MULTILINE)`: 0–3 leading spaces, mandatory space after the hashes (so `#hashtag` is not a heading), optional ATX closing sequence stripped. Section names are compared case-insensitively against the captured title, after stripping — not by regex interpolation of the name. Setext headings are not supported; the template emits ATX only."* Extend test-plan item 1 with: `#hashtag` (not a heading), 3-space-indented heading (is one), 4-space-indented (is not), trailing `##`, mixed-case name, and a heading whose name is a prefix of another required section.

---

### F-6: D1 narrows the secret list to five branded shapes, dropping the generic `KEY = "value"` patterns — the highest-probability leak in a handoff now returns `READY`
**Severity:** P1
**Where:** spec `:44` (D1's bounded list), `:204` ("secret scan (D1's bounded pattern list)"), D6 `:116-121`
**Edge case:** The realistic secret: a value pasted from `.env`, a CI log, or a `docker run` line.
**What happens:** The vendor list carried six generic assignment patterns (`api_key`, `password`, `secret`, `token`, `private_key`, plus DSNs) *and* the branded prefixes. D1 keeps only `ghp_`, `sk-`, `xox[baprs]-`, PEM headers, and DSN-with-password. So `DATABASE_PASSWORD=hunter2patoot`, `ANTHROPIC_API_KEY=sk-ant-api03-…`, `AWS_SECRET_ACCESS_KEY="wJalr…"`, `client_secret: "…"` all pass the gate and the document is reported `READY` — the exact verdict that tells the author it is safe to hand over. This is a security regression against the artifact being superseded, delivered silently, and the template's own guidance ("List relevant env var NAMES only — NEVER include actual values") makes the scanner the only enforcement.
Two further false negatives inside the retained list, if it is transcribed at the vendor's widths: `sk-[a-zA-Z0-9]{48}` misses `sk-ant-api03-…` and `sk-proj-…` (both contain `-`/`_` and are far longer) — i.e. it misses **Anthropic keys specifically**, the most likely credential in a Vigil Harbor session; and `ghp_[a-zA-Z0-9]{36}` misses `gho_`/`ghu_`/`ghs_`/`ghr_` and `github_pat_…`.
**Why the spec misses it:** D1's rationale is about *provenance* — which patterns are "facts about credential formats" rather than authored expression. Generic `password\s*[:=]\s*"…"` is even more clearly a fact than a vendor prefix, so the provenance argument does not motivate dropping them; the narrowing looks incidental.
**Suggested fix:** Restore the generic assignment class in D1's enumeration: *"…plus the generic assignment shapes `(api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*<non-trivial value>` — the dominant real-world leak — with a minimum value length to keep prose out."* Widen the branded prefixes to `sk-[A-Za-z0-9_-]{20,}` (covers `sk-ant-`/`sk-proj-`) and `gh[pousr]_[A-Za-z0-9]{36,}` / `github_pat_[A-Za-z0-9_]{20,}`. Extend test-plan item 3 to require a positive for a bare `KEY=value` env-style line and for an `sk-ant-api03-…`-shaped string.

---

### F-7: Exit code `2` is overloaded — "secrets detected" and "I mistyped the path" are indistinguishable, contradicting D6's own rationale
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:121` ("Distinct exit codes let a caller tell 'unfinished' from 'dangerous'") vs `:206` ("Missing file → clear message, exit `2`. Unreadable/undecodable file → same")
**Edge case:** A typo'd path, a directory passed instead of a file, a file deleted between create and validate.
**What happens:** `validate_handoff.py .claude/handoff/foo.md` (singular typo) exits 2. SKILL.md's CREATE step (`:181`) says "Do not finalize on `BLOCKED`" — an agent gating on the exit code reports a secrets block on a document it never opened. The one distinction D6 pays for with a three-verdict design is destroyed by the error path. The no-argument case is also unspecified; the vendor exits 1, which collides with `NEEDS WORK`.
**Why the spec misses it:** D6's table (`:116-119`) covers only the three verdicts; the error exits were added later at `:206` and reuse "the non-zero one that isn't 1".
**Suggested fix:** Reserve `2` exclusively for `BLOCKED`. At `:206`: *"Missing / unreadable / undecodable file, or no argument → clear message on stderr naming the path and the reason, exit `3`. Exit `2` means secrets and nothing else."* Add the error exit to the test-plan item 3 matrix.

---

### F-8: A `BLOCKED` verdict names the pattern class but not where it matched — the author cannot clear it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:205` ("Report prints each check, the advisory score, and the verdict")
**Edge case:** A false positive, or any positive on a 300-line document (measured: real handoffs run 179–312 lines).
**What happens:** The vendor report prints `Token: Found 1 potential match(es)` — a class name and a count, no line number, no excerpt. On a false positive (the vendor's `Bearer\s+[a-zA-Z0-9_\-.]+` matches the literal prose "Bearer token"; D1's DSN forms match a documented example connection string) the workflow deadlocks: SKILL.md says do not finalize, and the author has no way to locate the offending text short of grepping by hand with a regex they don't have. Symmetrically, `incomplete` tells the author a section is thin but not *how* thin (27 of 50 characters vs 3 of 50 changes what they do). This is the debuggable-tripwire axis, and this repo already holds the higher bar: `lint.py` findings are `(severity, rule, file, line, message)` five-tuples.
**Why the spec misses it:** D6 focused on verdict semantics; report content is one clause at `:205`.
**Suggested fix:** At `:205`: *"Every finding carries a locus: `<file>:<line>` plus the matched pattern name and a redacted excerpt (first 4 and last 4 characters of the match, middle replaced), matching `lint.py`'s finding-tuple discipline. `incomplete` reports the measured length against the threshold (`27/50 chars`). All violations are reported before the verdict line — no short-circuit on the first match."*

---

### F-9: Fenced code blocks and inline code are not excluded — a `#` comment silently truncates a section, and a quoted `[TODO: …]` makes `READY` unreachable
**Severity:** P2
**Where:** spec `:54-80` (D3), `:204` ("Checks: unfilled `[TODO: …]`")
**Edge case:** A handoff containing a shell snippet, or one that documents this skill.
**What happens:** Two distinct effects, both from scanning the whole document as flat text:
1. **Span truncation.** D3 makes the terminator fire on *any* depth 1–6, and a shell comment inside a fence (` # run the tests`) is depth-1 heading-shaped. A section whose evidence is a fenced command block ends at the comment; everything after it stops counting toward the ≥50-character check, and a fully-written section reports `incomplete`. D3 explicitly advertises being "slightly **stricter** than the vendor's patched version" (`:80`) — this is where that strictness misfires. (Measured: the current 5-document corpus has zero heading-shaped lines inside fences, so this is latent, not observed — but the RESUME workflow at `:182` instructs agents to record `git log` / `git diff --stat` invocations, which is exactly where `#` comments appear.)
2. **Unclearable `NEEDS WORK`.** The `[TODO: …]` scan has no escape hatch, so any handoff that *quotes* the marker — a handoff about VHS-28 itself, or one pasting the template — can never reach `READY`. This spec quotes `[TODO: …]` five times; a handoff summarizing this session would be permanently `NEEDS WORK` with no remedy.
**Why the spec misses it:** The vendor scanned flat text and the spec inherited it; `lint.py` by contrast tracks fences (`_FENCE_RE`, `lint.py:55`), so the repo already has the pattern.
**Suggested fix:** In D3: *"`section_span` and the `[TODO: …]` scan operate on a fence-masked copy of the document — lines between matching ``` / ~~~ fences are blanked before matching, following `lint.py`'s `_FENCE_RE` handling. The secret scan deliberately does **not** mask fences: a credential inside a code block is still a credential."* Add test-plan bullets: a section containing a fenced block with a `# comment` line validates complete; a `[TODO: x]` inside a fence does not trip the TODO check; a `ghp_…` inside a fence still does trip the secret check.

---

### F-10: A required section placed last swallows the document footer and passes the 50-character gate on boilerplate alone
**Severity:** P2
**Where:** spec `:70-71` ("`end` is … the offset of the next heading at ANY depth, **or `len(content)`**"), test plan `:222`
**Edge case:** The last heading in the document, plus horizontal rules and trailing boilerplate.
**What happens:** Measured across the 5 real handoffs: after the final heading there are **588–875 characters** of trailing content (a `---` rule plus the "Security Reminder: before finalizing, run `validate_handoff.py`…" footer). Any section that ends up last therefore measures 10–17× the threshold before the author types anything — an empty required section returns `READY`. Today the last heading is always `## Related Resources` (not required), so this is latent; but the spec re-authors the ordered section table (`:197`) with no constraint pinning that, and D4's round-trip test fills *every* `[TODO:]` so it structurally cannot catch a false pass. `---` also reads as a setext underline / thematic break that nothing terminates on.
**Why the spec misses it:** `len(content)` is the obvious terminator and the footer is invisible in the abstract; the failure only appears when you measure the real artifact.
**Suggested fix:** In D3: *"The span also terminates at a thematic break (`---`/`***`/`___` on its own line) so the document footer is never counted as any section's content."* Add an ordering invariant to D4 and a test: *"a required section placed last in the document, left empty, is reported `incomplete`."*

---

### F-11: `--continues-from` — a missing target silently degrades to "fresh start", and the containment check's Windows semantics are unspecified
**Severity:** P2
**Where:** spec `:194`, `:224` (test-plan item 4)
**Edge case:** Wrong filename, symlinked/junctioned project path, non-existent target, `--project-path` in play.
**What happens:** Four gaps in one clause:
1. **Silent flag discard.** `:194` says "emits a chain block with the previous document's title; **absent → an explicit 'fresh start' block**." The vendor resolves a not-found `--continues-from` to `{"exists": False}`, which produces the *fresh-start* block. So `--continues-from 2026-08-22-mcp-52.md` (one character wrong) writes a document that asserts "Continues from: None (fresh start)" — the operator's explicit chaining intent is silently inverted, and the RESUME workflow (`:182`, "following any `Continues from` link") loses the thread. An explicitly-passed flag that fails should never be a no-op.
2. **Base directory undefined.** `:189` adds `--project-path PATH`, but `:194` says `--continues-from` "resolves against `.claude/handoffs/`" without saying whose — CWD's or `--project-path`'s. If they differ, the chain link points into a different tree.
3. **Symlink/junction false rejection.** `Path.resolve()` follows links. If the project lives under a junction (routine on Windows with redirected `Documents`/OneDrive), the resolved candidate and an unresolved base never compare equal and *every* `--continues-from` is rejected. Conversely `is_relative_to` is a case-sensitive string comparison, and `resolve(strict=False)` does not canonicalize case for a non-existent target, so a case-mismatched filename false-rejects.
4. **Rejection behavior unstated.** Escape → error and exit non-zero, or warn and fall back to fresh-start? Given (1), an implementer will plausibly pick fallback.
**Why the spec misses it:** `:194` compresses resolution, validation, and the absent-case into one sentence, and the absent-case wording conflates "flag not passed" with "flag passed, target not found."
**Suggested fix:** Rewrite `:194`: *"`--continues-from` is resolved against `<project-path>/.claude/handoffs/`. Both the base and the candidate are `resolve()`d before comparison, and the comparison is case-insensitive on Windows. A path that escapes the directory, or names a file that does not exist, is a **hard error**: a message naming the resolved path and the base, exit non-zero, no document written. 'Fresh start' is emitted only when the flag is not passed at all."* Extend test-plan item 4 with the not-found case and an absolute-path escape (`C:/Windows/win.ini`), asserting non-zero exit and no file created.

---

### F-12: No timeout on git subprocesses — "every git call is wrapped" covers exceptions, not hangs
**Severity:** P2
**Where:** spec `:192`
**Edge case:** A held `index.lock`, a repo on a slow/disconnected network share, a stalled fsmonitor or credential helper.
**What happens:** `create_handoff.py` blocks indefinitely with no output. The user invoked this *because* context was running out; a silent hang is the worst available failure. The vendor script has `timeout=10` on every call (`run_cmd`, `subprocess.run(..., timeout=10)`) and catches `subprocess.TimeoutExpired` — the spec's "wrapped" language covers `FileNotFoundError`/non-zero exit but says nothing about time, so a clean-room implementer working from the spec alone will drop the timeout.
**Why the spec misses it:** "Wrapped" reads as complete; the external-system-slow axis is not enumerated anywhere in the spec.
**Suggested fix:** At `:192`: *"…wrapped, with a per-call timeout (10s). A timeout is treated exactly like a non-zero exit — the placeholder line is emitted and generation continues. The placeholder text distinguishes the three cases (not a repo / no commits / git unavailable-or-timed-out) so the failure is diagnosable from the document itself."*

---

### F-13: A long slug crashes the write with an uncaught `OSError` — measured, even with long paths enabled
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:191` ("Slug sanitized to `[a-z0-9-]`, empty → `handoff`"), `:195`, test plan `:224` ("slug sanitizing")
**Edge case:** An agent passing the user's phrasing straight through as the slug.
**What happens:** Reproduced on this machine — `LongPathsEnabled = 1` in the registry, and a 316-character target path still fails:
```
OSError [Errno 22] Invalid argument: 'C:\Users\zioni\AppData\Local\Temp\hlp\.claude\handoffs\2026-08-23-221530-aaa….md'
```
Uncaught traceback, no document. No length cap is specified. The realistic trigger is benign — the vendor sanitizer maps spaces to hyphens, so `create_handoff.py "continue the session-handoff spec review and then ship it through ship-spec"` is already 70 characters of slug, and an agent that passes a whole user turn reaches 150+. Deep project paths (`…\Vigil-Harbor\MCP Server\.claude\handoffs\` is 65 characters before the 35-character timestamp prefix) cut the available budget roughly in half.
**Why the spec misses it:** "Sanitized to `[a-z0-9-]`" addresses the character set; length is a separate axis and no test-plan bullet covers it.
**Suggested fix:** At `:191`: *"Slug sanitized to `[a-z0-9-]`, collapsed runs of `-`, stripped of leading/trailing `-`, and **truncated to 60 characters**; empty after sanitizing → `handoff`."* Add to test-plan item 4: a 300-character slug produces a valid path and a written file. Also state the ordering explicitly — sanitize *then* default — otherwise an all-emoji slug sanitizes to empty and yields `2026-08-23-221530-.md`.

---

### F-14: D5's session-id check uses `$`, not `fullmatch` — the precedent it cites (`60303f9`) uses `fullmatch` for exactly this reason
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec `:105` ("matched against `^[0-9a-fA-F]{8}-…{12}$` before any filesystem lookup … the same posture as talaria's watch-id rejection (`60303f9`)")
**Edge case:** An argument with a trailing newline, e.g. from `$(cat id.txt)` or a copy-paste.
**What happens:** In Python, `$` matches at end-of-string **or immediately before a trailing newline**, so `"…-…-…-…-…\n"` passes validation and is then interpolated into the `~/.claude/projects/**/<id>.jsonl` glob (4,178 files across the store on this machine). The stated purpose of the check — "keeps a hostile or fat-fingered argument out of glob expansion" — is not delivered. The cited commit does it correctly: `skills/talaria/scripts/talaria_watch.py` uses `_WATCH_ID_RE = re.compile(r"^[0-9a-f]{16}$")` with `_WATCH_ID_RE.fullmatch(normalized)` — belt and braces, precisely because `$` alone is leaky.
**Why the spec misses it:** The regex was written from memory of the precedent rather than from the file.
**Suggested fix:** At `:105`: *"…matched with `re.fullmatch` against `^[0-9a-fA-F]{8}-…{12}$` (mirroring `talaria_watch.py`'s `_WATCH_ID_RE.fullmatch`, which is anchored twice deliberately: `$` alone admits a trailing newline)."* Extend test-plan item 5 with a trailing-newline id.

---

### F-15: SESSION TRANSFER's fallback covers "not found" but not "found and unusable" — transcripts here run to 39.6 MB
**Severity:** P2
**Where:** spec `:99-103` (D5, "read the tail"; "**Mandatory fallback:** if no transcript is found")
**Edge case:** The transcript exists and is enormous, truncated, or not valid JSONL.
**What happens:** Measured on this machine: 4,178 transcripts totalling 3.13 GB, largest **39.6 MB**, 27 over 10 MB. D5 says "read the tail" without quantifying it, and the fallback trigger is narrowly worded — "if no transcript is found — wrong harness, pruned history, malformed id." A 40 MB file *is* found, so the fallback does not arm; an agent that reads it whole either errors or consumes its entire context budget on the first action of a mode whose whole point is that context was scarce. A partially-written JSONL (the source session still running, or killed mid-write) is also "found" and yields a truncated final record.
**Why the spec misses it:** D5 was written to resolve the *portability* question; the size/corruption axis of the same lookup was not enumerated.
**Suggested fix:** At `:102-103`: *"…read the **last N kilobytes** (e.g. 256 KB), decoding from the last complete record boundary and discarding a truncated final line. The fallback arms whenever the transcript is missing **or unusable** — absent, unreadable, not valid JSONL, or too large to read within the budget — and in every case the summary states plainly which case applied."*

---

### F-16: Handoff writes are non-atomic and the chain is unbounded — a killed writer leaves a half-document that RESUME reads as authoritative, and a chain cycle loops the resuming agent
**Severity:** P2
**Where:** spec `:195` ("Writes the file … Refuses to overwrite"), `:182` (RESUME: "read the document fully, **following any `Continues from` link**"), D10 `:150-152`
**Edge case:** Ctrl-C or a context-limit kill during the write; a hand-edited or accidentally circular chain.
**What happens:** Two persistence-checklist items are unaddressed:
- **Atomicity.** A single non-atomic `write_text` means an interrupted create leaves a truncated `.md` in `.claude/handoffs/`. RESUME lists newest-first and reads it as the current handoff — a half-document is strictly worse than no document, because it looks complete enough to act on. There is no `status`/temp-and-rename discipline. The fix is free: write to `<name>.md.tmp` and `os.replace`, which also closes the TOCTOU window in the same-second collision check at `:195` (an `exists()`-then-`write` sequence; `open(path, 'x')` or `os.replace` removes it).
- **Chain re-entrancy.** Nothing bounds chain depth and nothing detects a cycle. `A --continues-from B` where `B` was later hand-edited to point at `A` makes RESUME's "following any `Continues from` link" loop until the agent's budget is gone. Chain depth is likewise unbounded across a long-running project.
Both are cheap and neither is scale machinery, so neither conflicts with D10 — worth stating explicitly so the drift-check does not flag the `os.replace` as unwarranted.
**Why the spec misses it:** D8 treats storage as unchanged from the vendor and therefore settled; the vendor's non-atomicity came along with it.
**Suggested fix:** At `:195`: *"The document is written atomically — `<name>.md.tmp` then `os.replace` — so an interrupted run leaves either no file or a complete one; this also makes the same-second collision check race-free. (Atomic replace is durability, not scale machinery — it is not the batching/concurrency D10 fences off.)"* At `:182`: *"…following the `Continues from` link, to a maximum of 5 hops, tracking visited filenames so a circular chain terminates with a note rather than a loop."*

---

### F-17: The staleness rubric reads `git log --since` on the current branch only, so a branch switch reports "fresh"
**Severity:** P2
**Where:** spec `:182` (RESUME rubric), D2 `:46-52` (justifying the removal of `check_staleness.py`)
**Edge case:** Handoff written on branch A, resumed on branch B (the normal case in this repo — every ship-spec run cuts a new worktree and branch).
**What happens:** `git log --oneline --since=<handoff timestamp>` is scoped to `HEAD`. Resume on a freshly cut branch and the answer is "no commits → **fresh**," the most permissive bucket in the rubric, on a document that may be describing an entirely different tree. The rubric only mentions branch divergence in its most severe bucket ("weeks plus branch divergence"), so the common case is unguarded. Secondarily, the handoff's own timestamp is a naive local-time string in a body line an author may edit, and `--since` will silently accept a garbled value.
**Why the spec misses it:** D2 argues correctly that an agent interprets staleness better than a fixed ladder, but the *commands* it hands the agent still encode the branch-local assumption from the deleted script.
**Suggested fix:** At `:182`: *"…compare the recorded branch against the current one **first** — a mismatch is itself a staleness signal and outranks the commit count. Assess commits with `git log --oneline --since=<ts> --all` (or against the merge-base with the handoff's branch), and prefer the timestamp parsed from the **filename** over the body line, which authors edit."*

---

### F-18: `--project-path` appears in the CLI but nowhere else in the spec, and is unvalidated
**Severity:** P3
**Where:** spec `:189` (`create_handoff.py [slug] [--continues-from FILE] [--project-path PATH]`) vs `:181` (SKILL.md CREATE: `create_handoff.py <slug> [--continues-from <file>]`)
**Edge case:** A path that does not exist, is a file, or is not writable.
**What happens:** The flag is new relative to the vendor (which uses `os.getcwd()`), is absent from the documented CREATE workflow, has no stated validation, and interacts undefined-ly with `--continues-from` (see F-11). `mkdir -p` on a non-existent path will happily create a `.claude/handoffs/` tree somewhere unintended; passing a file raises `NotADirectoryError`. This is also the one argument that *does* become a path fragment, which sits awkwardly against D5's "never as a path fragment" posture for the session id.
**Suggested fix:** Either drop `--project-path` (CWD is sufficient and matches SKILL.md), or add one line: *"`--project-path` defaults to CWD; it must be an existing directory or generation fails with a clear message. It is the base for both the output directory and `--continues-from` resolution."* Mirror it in the SKILL.md CREATE step at `:181`.

---

### F-19: Git output is interpolated into a markdown table with no escaping
**Severity:** P3
**Where:** spec `:193` ("Modified-file table capped at 10 rows"), `:194` (chain block carries "the previous document's title")
**Edge case:** A filename containing `|`, a non-ASCII filename, a previous-handoff H1 containing `]` or `|`.
**What happens:** `git diff --name-only` is line-split and each path becomes `| <path> | … | … |`. A path containing `|` adds a column and corrupts the table for every reader. Non-ASCII paths are octal-escaped by git's default `core.quotepath=true` and render as `"caf\303\251.txt"`. The chain block builds `[{title}](./{filename})`; a title containing `]` breaks the link. Nothing crashes and D7 drops the file-reference check, so there is no downstream consumer — this is cosmetic corruption of the artifact only.
**Suggested fix:** At `:193`: *"Paths are gathered with `-z` and `-c core.quotepath=false`, and `|` and backticks are escaped before being placed in a table cell; the chain-block title is escaped for markdown link text and truncated to 80 characters."*

---

### F-20: The "non-git temp directory" test can be shadowed by an ancestor repository
**Severity:** P3
**Where:** spec `:224` (test-plan item 4: "generation in a non-git temp directory succeeds with placeholder git lines")
**Edge case:** A developer whose `TMPDIR` sits inside a git working tree, or a test that uses `tempfile.mkdtemp(dir=REPO_ROOT)`.
**What happens:** `git rev-parse --git-dir` walks *upward*, so a "non-git" temp directory nested under any repository reports success and the test asserts a placeholder that never appears — a false failure that looks like a code bug. Conversely, a test written to assert real git metadata could pass for the wrong reason.
**Suggested fix:** At `:224`: *"…in a temp directory isolated from any ancestor repo (`GIT_CEILING_DIRECTORIES` set to the temp root, or `GIT_DIR`/`GIT_WORK_TREE` scrubbed), asserting the placeholder text is present."*

---

### F-21: The advisory score still prints, and re-creates the threshold pressure D6 exists to remove
**Severity:** P3
**Where:** spec `:121` ("The advisory **score is still printed** … but it gates nothing")
**Edge case:** A model that learned the vendor's "do not finalize below 70" instruction.
**What happens:** D6's rationale (`:109-112`) is that a visible number authors optimize against. Removing the *documented* threshold while keeping the number visible preserves most of the pull — an agent seeing `Score: 62/100` next to `Verdict: READY` will plausibly self-gate anyway, which is the flattening behavior the ticket observed.
**Suggested fix:** Print the score with an explicit non-gate label — e.g. `Score: 62/100 (advisory only — the verdict above is the gate; no score threshold exists)` — and state in SKILL.md that the agent acts on the verdict and exit code, never on the score.

## Summary
P0: 1 | P1: 5 | P2: 11 | P3: 4

STATUS: RED P0=1 P1=5 P2=11 P3=4
