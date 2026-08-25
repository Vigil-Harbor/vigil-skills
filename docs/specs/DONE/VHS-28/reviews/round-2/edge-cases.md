# Edge-Cases Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | `section_span` self-contradiction (P0) | CLOSED | spec:119 — stripping is whitespace only, clause explicitly deleted; leaf invariant spec:132 + test item 3 spec:292 |
| edge-cases | F-2 | No text encoding specified (P1) | **PARTIAL** | spec:254-260 adds UTF-8 write/read/subprocess + BOM strip, but says nothing about newlines — see F-1 below |
| edge-cases | F-3 | Tripwire anchored to unmerged branch (P1) | CLOSED | spec:10-24; table verified against disk (`origin/main`=`a0ad847`, 5 `SKILL.md`, asserts `4`; local HEAD `7a3a929`, 7, asserts `7`, 8 ahead) — new variant at F-11 |
| edge-cases | F-4 | Legacy corpus unpinned (P1) | **PARTIAL** | spec:38 + item 5 spec:294 add a fixture, but it pins the shape used by only 2 of the 5 real documents — see F-3 below |
| edge-cases | F-5 | Matcher unifies depth only (P1) | CLOSED | spec:82-95 — full `_HEADING_RE` + six stated semantics (residual `\r` gap is F-1) |
| edge-cases | F-6 | Secret list narrowed (P1) | CLOSED | spec:65-66 restores the generic assignment class with length floors; widened branded prefixes |
| edge-cases | F-7 | Exit `2` overloaded (P2) | CLOSED | spec:162 exit `3` for operator errors |
| edge-cases | F-8 | `BLOCKED` carries no locus (P2) | CLOSED | spec:170 — `<file>:<line>`, pattern name, redacted excerpt, report-all-then-verdict (offset caveat at F-6) |
| edge-cases | F-9 | Fences / inline code not excluded (P2) | **PARTIAL** | spec:97 masks fences; inline code spans still unmasked — F-13 |
| edge-cases | F-10 | Last section swallows footer (P2) | **PARTIAL** | spec:107-109 adds thematic-break termination, but the rule is literal-3-char only — F-5 |
| edge-cases | F-11 | `--continues-from` silent degrade (P2) | **PARTIAL** | spec:270 makes not-found a hard error (write side); the read side has no parse rule — F-8 |
| edge-cases | F-12 | No git subprocess timeout (P2) | CLOSED | spec:268 — 10s, timeout treated as non-zero exit |
| edge-cases | F-13 | Long slug crashes write (P2) | CLOSED | spec:267 — 60-char cap, truncate-then-default ordering |
| edge-cases | F-14 | `$` vs `fullmatch` on session id (P2) | CLOSED | spec:147 |
| edge-cases | F-15 | Fallback covers not-found only (P2) | CLOSED | spec:145 — "missing **or unusable**", four named cases |
| edge-cases | F-16 | Non-atomic write, unbounded chain (P2) | CLOSED | spec:271 `os.replace`; spec:249 5-hop cap (residuals at F-15) |
| edge-cases | F-17 | Staleness reads current branch only (P2) | CLOSED | spec:249 — branch comparison first, outranks commit count |
| edge-cases | F-18 | `--project-path` unvalidated (P3) | CLOSED | spec:266 |
| edge-cases | F-19 | Git output unescaped in table (P3) | CLOSED | spec:269 |
| edge-cases | F-20 | Temp dir shadowed by ancestor repo (P3) | CLOSED | test item 8, spec:297 |
| edge-cases | F-21 | Advisory score recreates threshold (P3) | CLOSED | spec:166 — labelled non-gate, verdict-only instruction |
| correctness | F-1 | Tripwire/baseline (P1) | CLOSED | same as edge/F-3 |
| correctness | F-2 | "68 on the untouched scaffold" (P2) | CLOSED | spec:153 now says "a **fully-written** handoff, at the template's own heading depths" |
| correctness | F-3 | Operative `~/.claude/…` in SKILL.md (P2) | CLOSED | spec:194 — harness-neutral operative sentence, literal path as non-operative note |
| correctness | F-4 | Vocabulary never enumerated (P2) | **PARTIAL** | spec:130 enumerates required (with depths) + recommended (names); `TEMPLATE_SECTIONS`, the ordered `(depth, name)` table the leaf invariant is asserted against, is still never shown — F-3 |
| correctness | F-5 | Exit `2` overloaded (P2) | CLOSED | spec:162 |
| correctness | F-6 | Span contradicts itself (P2) | CLOSED | spec:119 |
| correctness | F-7 | Fenced blocks not excluded (P2) | **PARTIAL** | spec:97; new failure modes at F-2, F-4, F-6 |
| correctness | F-8 | `--project-path` purposeless (P3) | CLOSED | spec:266 |
| correctness | F-9 | Score never defined (P3) | CLOSED | accepted as Deferred, spec:342 |
| correctness | F-10 | Zero-WARN uncheckable by the command (P3) | CLOSED | item 10, spec:299 — programmatic via `lint.lint_path` (verified: `lint.py:291` returns non-zero on ERRORs only) |
| correctness | F-11 | `tests/fixtures/` unused (P3) | CLOSED | spec:38 |
| correctness | F-12 | pytest gate not stdlib (P3) | CLOSED | spec:310 |
| correctness | F-13 | "~1,150 lines" is scripts only (P4) | CLOSED | spec:58 |
| conventions | F-1 | `_sections` has no home (P1) | CLOSED | spec:33 file-inventory row |
| conventions | F-2 | pytest vs stdlib convention (P2) | CLOSED | spec:310 |
| conventions | F-3 | Case-2 tag missing in D5 (P2) | CLOSED | spec:142-143 |
| conventions | F-4 | Exit `2` overloaded (P2) | CLOSED | spec:162 |
| conventions | F-5 | Name open question unresolved (P2) | CLOSED | D11, spec:212-218 |
| conventions | F-6 | D8/D5 asymmetry unstated (P3) | CLOSED | spec:184 |
| conventions | F-7 | AGENTS.md File layout row (P3) | CLOSED | D12, spec:223 |
| conventions | F-8 | `--prune` footgun / posture (P3) | CLOSED | spec:201-202 (verified: `sync.py:81` prune, `iter_files` unfiltered `rglob`) |
| conventions | F-9 | `references/` vs `reference/` (P4) | CLOSED | D12, spec:222 |
| conventions | F-10 | "talaria convention" overstated (P4) | CLOSED | spec:252 now a plain citation |
| conventions | F-11 | Unauthorized spec-level additions (P3) | CLOSED | Deferred, spec:341 |

No REOPENED items. Five PARTIALs, each carried forward below as a concrete new finding.

## Findings

### F-1: The new `_HEADING_RE` captures a trailing `\r`, and the new Encoding discipline never normalizes newlines — measured on a real legacy handoff
**Severity:** P1
**Where:** spec.md:82-86 (`_HEADING_RE`), spec.md:254-260 (§ Encoding discipline), spec.md:258 (Writes)
**Edge case:** CRLF line endings — both in the existing corpus and in the documents this skill will itself write.
**What happens:** `r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$"` with `re.MULTILINE`: `$` matches only *before* `\n`, and `\r` is in neither `[ \t]` nor `#*`, so the non-greedy title group is forced to absorb it. I ran the spec's exact regex against the corpus:

```
== 2026-08-15-060410-mcp-45-post-merge.md   (file(1): "with CRLF line terminators")
   Current State Summary    d=2 own=818   raw_title='Current State Summary\r'
   Immediate Next Steps     d=2 own=2233  raw_title='Immediate Next Steps\r'
   Important Context        d=2 own=1398  raw_title='Important Context\r'
```

D3 says names are compared "case-insensitively against the captured title **after stripping**", where "stripping" is defined only as the ATX closing sequence. An implementer who writes `title.casefold() == name.casefold()` — the literal reading — reports **all three required sections `missing`** on that document. That is the ticket's headline symptom, reproduced by the very regex introduced to eliminate it.

The write side compounds it: spec:258 specifies `encoding="utf-8"` but no `newline=`, so on the target platform (`cp1252` locale, per spec:256) Python's text mode translates `\n` → `\r\n` and **every scaffold this skill generates is CRLF** — i.e. the skill would fail to validate its own output.
**Why the spec misses it:** § Encoding discipline cites `lint._read_lines` (`lint.py:64-73`) as the read discipline, but `_read_lines` ends in `splitlines()`, which *is* CRLF/CR-safe. `section_span` needs a whole string, not lines, so it inherits the citation without inheriting the newline safety. The BOM is handled explicitly; `\r` is not mentioned anywhere in the spec.
**Suggested fix:** In § Encoding discipline, extend the read discipline in `_sections.py` to: `read_bytes()` → `decode("utf-8", errors="replace")` → strip BOM → **`text.replace("\r\n", "\n").replace("\r", "\n")`**, and state that all matching, span, offset and length arithmetic operates on that normalized string. Add `newline="\n"` to the write in § `create_handoff.py`. Belt-and-braces: make the title group `(.*?)[ \t\r]*#*[ \t\r]*$`. Test item 7 already names a CRLF case — restate it as "a CRLF handoff validates with zero `missing`", so it pins the failure rather than a vague "correctly".

### F-2: "Own content" is measured on the fence-masked copy, so a required section whose body is a code block measures zero characters and is permanently `incomplete`
**Severity:** P1
**Where:** spec.md:97 (fence masking), spec.md:102 (`def section_span(masked, section)`), spec.md:119 (consequence 2), spec.md:278
**Edge case:** A required section whose content is mostly or entirely a fenced block — a pasted stack trace, a failing test excerpt, a command sequence under `Immediate Next Steps`, an error under `Important Context`.
**What happens:** `section_span`'s signature takes `masked` and returns offsets into `masked`. Consequence 2 defines own content as that span "after stripping leading/trailing whitespace — **nothing else**". Fenced lines are blanked in `masked`, so the natural implementation measures blanked whitespace: a section holding a 40-line code block strips to `0 chars`, reports `incomplete (0/50 chars)`, verdict `NEEDS WORK`, exit `1` — on a document that is visibly fully written. The author's only remedy is to pad with prose. This is the same symptom class the spec cites at spec:97 as the reason fence masking exists in the first place; masking cures the truncation half and creates the measurement half.
**Why the spec misses it:** spec:97 scopes masking to "before **matching**" (headings, `[TODO:]`), but the span function it names is also the source of the length measurement, and the signature makes the masked string the only thing in scope. Nothing in the spec tells the implementer to slice the *original*. No test-plan item measures a fence-only section: item 2 asserts a fenced `# comment` "validates complete", which is satisfied by an ordinary section that merely *contains* a fence alongside prose.
**Suggested fix:** In D3, state that masking preserves offsets (see F-6) and that **length is measured on the original text sliced at the masked span's offsets** — `len(original[start:end].strip())` — while heading detection and the `[TODO:]` scan use `masked`. Add to test item 2: "a required section whose entire body is a fenced code block of ≥50 characters validates **complete**."

### F-3: The legacy fixture pins the minority on-disk shape; three of the five real documents use a different heading depth, and the spec never states that matching is depth-agnostic
**Severity:** P2
**Where:** spec.md:38, spec.md:126-130 (D4), test item 5 spec.md:294
**Edge case:** The actual corpus the brief declares load-bearing ("existing handoff documents on disk … must remain readable", brief:61).
**What happens:** I read all five documents in `C:/Users/zioni/Documents/Vigil-Harbor/MCP Server/.claude/handoffs/`. The depths are **not** what D4 declares:

| Document | Current State Summary | Important Context | Immediate Next Steps | Recommended set |
|---|---|---|---|---|
| `2026-08-15-…-mcp-45` | `##` | `##` | `##` | all `##` |
| `2026-08-22-…-halted-red` | `##` | `##` | `##` | all `##` |
| `2026-08-22-…-gpu-cutover` | `##` | `##` | `##` | all `##` |
| `2026-08-23-…-sprint` | `##` | `###` | `###` | all `###` |
| `2026-08-23-…-5-rounds` | `##` | `###` | `###` | all `###` |

Three of five are fully flattened to `##`; the container headings (`## Codebase Understanding`, `## Context for Resuming Agent`) are absent entirely from all five. Test item 5's fixture is specified as `## Current State Summary`, `### Important Context`, `### Immediate Next Steps` — the vendor *template* shape, which matches only the two newest documents. The regression test that exists to "catch drift away from the documents already installed" therefore covers 40% of them.

Separately, whether matching is by name or by `(depth, name)` is left ambiguous: spec:127 says `REQUIRED_SECTIONS` is a subset "**by name**", but spec:130 annotates each with a depth and spec:126 makes `TEMPLATE_SECTIONS` an ordered `(depth, name)` table. An implementer who keys the lookup on the tuple reports `Important Context` and `Immediate Next Steps` `missing` on three of five real documents — a depth bug, which is the exact defect VHS-28 was filed for.
**Why the spec misses it:** D4 reasons from the vendor's `create_handoff.py` template (which does emit `###`), not from the documents the authoring agent actually produced. The agent flattened the headings — the behavior D6:153 itself predicts ("teaches authors to flatten headings until the number moves").
**Suggested fix:** In D4, state explicitly: **section lookup is by name only; the depth in `TEMPLATE_SECTIONS` governs rendering, never matching.** Change test item 5 to two fixtures (or one fixture with both shapes): `tests/fixtures/legacy-handoff.md` (all-`##` flattened) and `tests/fixtures/legacy-handoff-nested.md` (`##`/`###`/`###`), both asserting zero `missing`. Add a one-line assertion that the same name matches at every depth 1-6.

### F-4: An unterminated or nested code fence masks the remainder of the document, so present sections report `missing` and the TODO scan goes blind
**Severity:** P2
**Where:** spec.md:97 ("lines between **matching** ``` / ~~~ fences are blanked")
**Edge case:** A fence opened and never closed; or — far more likely here — a fenced block that itself contains a ``` line, which is routine in a handoff about skill/spec work in this repo.
**What happens:** The inner ``` toggles masking off, the outer closer toggles it back on, and everything from there to EOF is blanked. Every heading after that point vanishes: required sections report `missing`, `[TODO: …]` markers become invisible, and the document reports `NEEDS WORK` naming sections the author can see with their own eyes. The secret scan (unmasked) still runs, so the two halves of the report disagree about what the document contains, with no diagnostic explaining why. `lint.py`'s own toggle (`lint.py:205-215`) has the same property, but lint is advisory — here it flips a gate.
**Why the spec misses it:** "matching" is stated as a property of well-formed input; the malformed case has no defined behavior. Test item 2 covers only a well-formed fence. Note the current corpus contains **zero** fenced blocks, so this is entirely a forward-looking risk that no existing document would surface.
**Suggested fix:** In D3, specify: fence tracking uses CommonMark closing rules (closer is the same character, at least as long as the opener, nothing but whitespace after); **an opening fence with no closer masks nothing** — treat the document as unfenced from that point and emit a distinct advisory finding, `unterminated code fence at <file>:<line>`, so the mismatch is diagnosable from the report rather than presenting as phantom missing sections. Add a test case: a document with an unterminated fence still reports its post-fence required sections as present.

### F-5: Thematic-break termination is specified as three literal characters — a `----` footer silently defeats it, and D3's setext bullet contradicts the span rule
**Severity:** P2
**Where:** spec.md:95 (setext bullet), spec.md:107-109 (span docstring), spec.md:120 (consequence 3)
**Edge case:** A footer rule written as `----` / `-----` / `* * *`, or a setext-style `Title` + `---`.
**What happens two ways:**
1. `section_span` says the span ends at "the next thematic break (`---`/`***`/`___` **alone on a line**)". Read literally that is `line.strip() in ("---", "***", "___")`. CommonMark thematic breaks are *three or more* of the character, optionally space-separated. A handoff whose footer rule is `----` is not terminated, the last required section absorbs the 588-875 characters of boilerplate consequence 3 warns about, and an **empty required section returns `READY` with exit `0`** — a silent gate bypass, which is the failure consequence 3 exists to prevent. (All three separators in the current corpus happen to be exactly `---`, so today's documents are safe and the gap is invisible to test item 3.)
2. spec:95 asserts a setext heading "neither opens nor terminates a section". But a setext H2 underline *is* a line of three-or-more `-`, so under the span rule it **does** terminate the enclosing section. Two adjacent normative statements about the same input disagree, and an implementer who honors the bullet by suppressing `---` after a non-blank line re-breaks consequence 3.
**Why the spec misses it:** The rule was derived from the one shape observed in the corpus rather than from the markdown grammar, and the setext bullet was written about `_HEADING_RE` (where it is true) but phrased as a claim about section behavior (where it is not).
**Suggested fix:** Restate the terminator as: a line matching `^ {0,3}((-[ \t]*){3,}|(\*[ \t]*){3,}|(_[ \t]*){3,})$` on the fence-masked copy, **unconditionally** — no setext exception. Amend spec:95 to "…a setext heading does not *open* a section; its `---` underline terminates the enclosing span like any other thematic break." Extend test item 3 with a `-----` footer and a setext-underline case.

### F-6: "Blanked" is undefined — if masking shifts offsets, every `<file>:<line>` locus D6 promises is wrong, and the masked and unmasked scans report line numbers from different strings
**Severity:** P2
**Where:** spec.md:97, spec.md:170 (D6 finding locus)
**Edge case:** Any document containing a fence, once a finding is reported after it.
**What happens:** D6 makes the locus load-bearing: "Without this, a `BLOCKED` verdict on a 300-line document is unclearable." But the report is assembled from two different strings — `incomplete` findings from the masked copy, secret findings from the raw text — and the spec never says whether "blanked" means *replaced with equal-length whitespace* (offsets and line count preserved) or *removed* (offsets shift by the length of every fenced block above). Under the second reading every `incomplete` locus after the first fence points at the wrong line, and the author is sent to a line that has nothing to do with the finding. Silent, and there is no test that asserts a line number at all — items 2, 3, 4, 6 assert verdicts and counts only.
**Why the spec misses it:** The masking rule and the locus rule were added in response to two different round-1 findings (F-9 and F-8) and never reconciled.
**Suggested fix:** In D3, state: masking replaces each fenced line's characters with spaces of equal length and preserves all newlines, so offsets, line numbers and length arithmetic are identical between the masked copy and the original. Add one assertion to test item 2 that an `incomplete` finding **after** a fenced block reports the correct 1-based line number.

### F-7: `.claude/handoffs/` is never created — first run in any project that has never held a handoff raises an uncaught `FileNotFoundError`
**Severity:** P2
**Where:** spec.md:264-272 (§ `create_handoff.py`), spec.md:266, spec.md:271
**Edge case:** The empty-state path — the very first CREATE in a fresh project, and the state test item 8's isolated temp dir is in.
**What happens:** spec:266 validates that `--project-path` exists and spec:271 writes `<name>.md.tmp` then `os.replace`, but nothing creates `<project-path>/.claude/handoffs/`. The `open()` on the temp file raises `FileNotFoundError`, uncaught — a traceback instead of the "clear message, non-zero exit" the spec specifies for every other operator error, at the moment the user is running this *because context is running out*.
**Why the spec misses it:** § `create_handoff.py` enumerates validation, slug handling, git metadata, escaping and atomicity in detail, which makes the omission read as deliberate. The vendor script does create it (`create_handoff.py:183`, `# Create handoffs directory`), so the behavioral reference covers it — it just didn't survive into the spec.
**Suggested fix:** Add a bullet: "Create `<project-path>/.claude/handoffs/` with `mkdir(parents=True, exist_ok=True)` before rendering; a failure (permission, path-is-a-file) exits non-zero with a message naming the resolved directory." Add to test item 8: "generation into a project directory with no `.claude/` writes successfully and creates the directory."

### F-8: The `Continues from` on-disk representation is unspecified — the writer escapes and truncates it, the reader has no parse rule, and the corpus already has a fixed format
**Severity:** P2
**Where:** spec.md:269 ("chain-block title escaped for link text and truncated to 80 characters"), spec.md:249 (RESUME: "following any `Continues from` link")
**Edge case:** RESUME on a document written by the vendor tool, or by ours after title escaping/truncation.
**What happens:** RESUME is instructed to follow the link, but the spec never states what shape it has. The existing corpus uses a fixed one — `2026-08-15-…-mcp-45.md:20` opens `## Handoff Chain` with `- **Continues from**: [<filename>](./<filename>)` and the no-parent form `- **Continues from**: None (fresh start)`. If our writer emits a different shape, RESUME silently finds nothing on legacy documents and reports a chain of length 1; if the reader keys on the *displayed title* rather than the href, spec:269's 80-character truncation and markdown escaping break the resolution. No test-plan item creates a chain and then follows it — item 8 covers only the two `--continues-from` **failure** paths.
**Why the spec misses it:** The chain was hardened on the write side in response to round-1 F-11 and F-19; the read side stayed as prose in the SKILL.md workflow, so the two halves were never specified as one contract.
**Suggested fix:** In § `create_handoff.py`, pin the emitted block verbatim (`- **Continues from**: [<filename>](./<filename>)`, plus `- **Continues from**: None (fresh start)` when the flag is absent), and state that escaping/truncation applies **only to the previous document's title line, never to the filename or the href**. In RESUME, state that the link is resolved from the href relative to the handoffs directory. Add a test: create A, create B `--continues-from A`, assert the emitted line matches the pinned shape and that the href round-trips to A's path — including when A's title contains `|`, backticks and 200 characters.

### F-9: RESUME has no behavior for an absent or empty `.claude/handoffs/`
**Severity:** P2
**Where:** spec.md:249 ("list `.claude/handoffs/` newest-first")
**Edge case:** No handoff directory, or a directory holding no `.md` files — the state of every project before its first CREATE, and the state after F-7's crash.
**What happens:** The workflow's first step yields nothing and the spec gives no next instruction. The agent improvises: most likely it asks the user what to do — which is precisely what D5 forbids for SESSION TRANSFER ("Never fail; never interrogate the user"), and the two sibling modes now behave inconsistently on the same class of empty input. A non-`.md` file (a stray `.tmp` from an interrupted write — note spec:271 leaves `<name>.md.tmp` behind on a crash) could also be picked up as "newest" if the listing isn't extension-filtered.
**Why the spec misses it:** D5's fallback was hardened in round 1 (F-15); RESUME's empty case was never on the list.
**Suggested fix:** Add to RESUME: "If the directory does not exist or contains no `*.md`, say so plainly and offer CREATE — do not prompt for a path. List `*.md` only; ignore `*.tmp`."

### F-10: A `BLOCKED` verdict triggered by auto-generated git metadata has no escape hatch
**Severity:** P2
**Where:** spec.md:65 (generic assignment class), spec.md:161 (`BLOCKED` outranks everything), spec.md:248 ("Do not finalize on `BLOCKED`")
**Edge case:** A commit subject, branch name, or modified-file path that matches the generic class — e.g. `fix(auth): rotate client_secret = <20 chars>`, or a branch named `token-rotation-<hash>`. `create_handoff.py` embeds branch, last 5 commits, and modified + staged files into the scaffold (spec:268).
**What happens:** The freshly generated, entirely unedited scaffold validates as `BLOCKED`/exit `2`. CREATE says do not finalize; there is no `--allow`, no acknowledgement path, and re-running regenerates the same metadata. The author's only route is hand-editing auto-generated content out of the document — clearable, but undocumented and indistinguishable from a genuine leak until they read the redacted excerpt. D6 deliberately made `BLOCKED` the hardest verdict in the design and gave it no relief valve.
**Why the spec misses it:** D1's length floors are justified as keeping *prose* out (spec:65); the spec never considers that the scan's input is partly machine-generated by the same script.
**Suggested fix:** Either (a) exempt the generated metadata block from the generic assignment class while keeping branded prefixes and PEM/DSN patterns active over it, or (b) document the manual remedy in CREATE ("if the match is in auto-generated metadata, edit the offending line out and re-validate — the redacted excerpt and locus identify it"). Add a test to item 6: a scaffold generated where the HEAD commit subject contains `client_secret = <20 chars>` produces the documented outcome rather than an unexplained `BLOCKED`.

### F-11: The Preconditions' two paths write different values to the same `test_lint.py` line, with no re-verification step after the pending commits land
**Severity:** P2
**Where:** spec.md:23-24 (consequences 1 and 2), spec.md:44
**Edge case:** VHS-28 is implemented on an unfixed `origin/main` base while `7a3a929` is still unmerged, then both land.
**What happens:** I verified the refs: `origin/main` is `a0ad847` with 5 `SKILL.md` and `len(skills), 4`; `7a3a929` (local, unmerged) bumps that literal `4 → 7`. Consequence 1 instructs the implementer to set the assertion to `6` on the unfixed base. That single line then has three candidate values in flight — `4` (origin), `6` (VHS-28's branch), `7` (`7a3a929`) — and the correct post-merge value is `8`. Git will conflict on it, which is the good case; the bad case is a resolution that takes one side wholesale and lands `6` or `7` while eight `SKILL.md` files exist, leaving `main` red again — the exact condition Preconditions exists to prevent. Note also that consequence 1's `6` **silently absorbs** the `4 → 6` half of `7a3a929`'s fix into VHS-28's diff, so the two changes are no longer independent.
**Why the spec misses it:** Preconditions correctly diagnoses the *baseline* problem and offers the right preferred resolution (spec:24), but then supplies a fallback path whose merge consequences aren't traced. "Preferred" is not a gate.
**Suggested fix:** Make landing `386dc6c` / `8946f58` / `7a3a929` on `main` a **hard precondition** — "cut the worktree only after these are merged; the tripwire edit is then `7 → 8`" — and demote consequence 1 to a verification instruction ("confirm the observed count is 7 before adding this skill; if it is not, stop and resolve the baseline"). If the fallback path is kept, add: "after merge, re-run `python -m unittest tests.test_lint` on `main` and correct the literal to the observed count."

### F-12: The leaf invariant is enforced only against the generated scaffold; two of five real documents already make a required section a container
**Severity:** P3
**Where:** spec.md:132 (D4 leaf invariant), test item 3 spec.md:292
**Edge case:** A hand-edited or differently-flattened document where a required section has a child heading directly beneath it.
**What happens:** I verified the invariant holds against the vendor's template — every name in both lists is followed by a sibling or a shallower heading, so no contradiction with "reuse the vendor's names and depths verbatim". But in the two `###`-shaped corpus documents, `## Current State Summary` is immediately followed by `### Architecture Overview`, making a **required** section a container in production. Own content measures 985 and 1,166 characters in those two files, so they pass today — but any document where the author writes straight into the subsections and leaves the parent bare gets `incomplete` on a section that is visibly complete, and D4's rationale ("would be permanently `incomplete`") says exactly that. The invariant test cannot see it, because it asserts against `TEMPLATE_SECTIONS`, which the validator's real inputs do not obey.
**Why the spec misses it:** The invariant was designed as a *template-authoring* constraint (its stated purpose is to fail the suite when someone adds a container to a list) and is being read as a property of documents.
**Suggested fix:** Say so explicitly in D4: "the leaf invariant constrains `TEMPLATE_SECTIONS` only; arbitrary documents may nest." Then define the fallback for the arbitrary case — the simplest is: when a section's own content is empty **and** the span is immediately followed by a deeper heading, measure the full subtree instead, and report `incomplete` only when the subtree is also short. Add a fixture case.

### F-13: Inline code spans are still unmasked, so a `[TODO: …]` written in backticks is unclearable
**Severity:** P3
**Where:** spec.md:97, spec.md:278
**Edge case:** A handoff whose next step is literally "remove the `[TODO: wire up auth]` marker in `foo.py`" — a natural sentence in the Immediate Next Steps of a handoff about unfinished work.
**What happens:** The TODO check fires forever. `READY` is unreachable without rewording prose that is correct as written. Round-1 F-9 raised inline code alongside fences; fence masking closed the heading half completely and the TODO half only for *fenced* content. (The heading half of the inline-code risk is genuinely closed — an inline span cannot begin a line-anchored heading.)
**Why the spec misses it:** The remedy adopted for F-9 was fence masking, and inline spans were not separately carried forward.
**Suggested fix:** Mask single- and multi-backtick inline code spans on the same masked copy (same equal-length-space rule), or explicitly scope the TODO regex to markers at line start / list-item position. Add the case to test item 2.

### F-14: `sys.path` insertion persists for the whole test process, and `__pycache__` mirrors through `sync.py`
**Severity:** P3
**Where:** spec.md:124 ("each entry point inserts its own directory on `sys.path`"), spec.md:49 (§ Left alone — `sync.py`), spec.md:288
**Edge case:** The full-suite command (`python -m unittest discover -s tests -p 'test_*.py'`) runs every test module in **one** interpreter.
**What happens:** Two effects, both minor but both real. (1) `skills/session-handoff/scripts/` is inserted at `sys.path[0]` and never removed, ahead of the repo root that `tests/test_lint.py:14` inserts, for every subsequent test module in the same process; today nothing collides (`_sections`, `create_handoff`, `validate_handoff` are unique names), but the shadowing is silent if that ever changes, and repeated loads grow `sys.path` unboundedly. (2) Importing `_sections` writes `skills/session-handoff/scripts/__pycache__/`, and `sync.py`'s `iter_files` is an unfiltered `rglob("*")` (`sync.py:42-45`), so `.pyc` files mirror into the harness skill directory — where they then appear as `dst_files - src_files` entries that `--prune` (`sync.py:81`) would queue for deletion, feeding directly into D9's `--prune` warning. This is pre-existing (`skills/talaria/scripts/__pycache__` already exists) and not VHS-28's regression, but spec:49 asserts clean automatic mirroring without noting it.
**Suggested fix:** In D4, prefer a guarded insert with a stable position and a de-dup check (`if d not in sys.path`), or have the test helper inject `_sections` into `sys.modules` once rather than each entry point mutating global state. Add one sentence to spec:49 acknowledging that `__pycache__` mirrors and is harmless but interacts with `--prune`.

### F-15: Chain-cycle detection keys on filenames rather than resolved paths, and neither the cap nor the cycle rule is tested
**Severity:** P3
**Where:** spec.md:249 ("a maximum of 5 hops, tracking visited filenames")
**Edge case:** A chain crossing project roots via `--project-path`, or a case-differing filename on Windows.
**What happens:** Two same-named documents in different handoff directories are treated as a cycle and the chain stops early with a spurious note; conversely `Foo.md` vs `foo.md` on a case-insensitive filesystem is the same file but two distinct "visited" entries — the 5-hop cap is what actually saves that case, making the cycle set redundant belt-and-braces rather than the stated mechanism. Neither the cap nor the cycle behavior appears in the test plan (item 8 covers only `--continues-from`'s two failure paths), and both are agent-executed prose, not code, so nothing enforces them.
**Suggested fix:** Change to "tracking `resolve()`d absolute paths, compared case-insensitively on Windows" — matching the containment-check discipline already specified at spec:270 — and state that the 5-hop cap applies regardless. Optionally note in the test plan that the cap is prose-enforced and deliberately untested.

### F-16: Two small `_HEADING_RE` divergences from CommonMark
**Severity:** P4
**Where:** spec.md:82-86
**Edge case:** (a) An empty ATX heading — `###` alone on a line. (b) A title ending in `#` with no preceding space, e.g. `## Interop with C#`.
**What happens:** (a) The mandatory `[ \t]+` means `###` alone is not a heading, so it neither opens nor **terminates** a span; content bleeds past it. CommonMark treats it as a valid empty heading. (b) `[ \t]*#*[ \t]*$` strips the trailing `#` from `C#`, yielding the title `Interop with C`. CommonMark requires a closing sequence to be preceded by a space, so the correct title keeps it. Neither name is in the vocabulary, so neither affects a verdict today; both are latent divergences in a matcher whose whole purpose is to be the one authoritative definition.
**Suggested fix:** Optional. If tightening: allow `^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$` for the empty case, and require `[ \t]` before the closing run (`(?:[ \t]+#+)?`). Otherwise, record both as deliberate simplifications in D3's semantics list so a future reader does not treat them as bugs.

## Summary
P0: 0 | P1: 2 | P2: 9 | P3: 4 | P4: 1

Key files:
- `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/docs/specs/TODO/VHS-28.spec.md`
- `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/docs/specs/TODO/VHS-28.brief.md`
- `C:/Users/zioni/Documents/Vigil-Harbor/MCP Server/.claude/handoffs/` — the five-document corpus F-1 and F-3 were measured against
- `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/lint.py` (`_read_lines` 63-73, fence toggle 205-215, exit 291)
- `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/tests/test_lint.py:48-59` (the tripwire)
- `C:/Users/zioni/Documents/Vigil-Harbor/vigil-skills/sync.py:42-45, 81` (`iter_files`, `--prune`)

STATUS: RED P0=0 P1=2 P2=8 P3=4 P4=1
