# Edge-Cases Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | `_HEADING_RE` captures trailing `\r` | CLOSED | spec:83‑85 mandates the normalizer; spec:91 widens the trailing class; test item 7 (spec:344) asserts CRLF→`READY`, zero `missing`, and LF output |
| edge-cases | F-2 | Own content measured on masked copy | CLOSED | spec:113 length-preserving mask; spec:140 measures `len(original[start:end].strip())`; spec:326, test item 2 (spec:339) |
| edge-cases | F-3 | Fixture pins minority shape; depth-agnosticism unstated | CLOSED | spec:37‑38 two fixtures in `tests/fixtures/session-handoff/`; spec:157 "depth never participates"; test item 5 (spec:342) |
| edge-cases | F-4 | Unterminated/nested fence masks the rest of the document | CLOSED | spec:115 CommonMark pairing; spec:116 unterminated masks nothing + advisory. *(New consequences filed as F-6 below.)* |
| edge-cases | F-5 | Thematic break as three literal chars; setext contradiction | CLOSED | spec:95‑98 `_THEMATIC_BREAK_RE` (3-or-more, spaced forms); spec:108 setext `---` terminates, `===` does not; spec:111 |
| edge-cases | F-6 | "Blanked" undefined; masked/unmasked line numbers diverge | CLOSED | spec:113 — equal-length spaces, newlines kept, offsets identical between copies |
| edge-cases | F-7 | `.claude/handoffs/` never created | CLOSED | spec:310 `mkdir(parents=True, exist_ok=True)` + named-directory failure path |
| edge-cases | F-8 | `Continues from` representation unspecified | CLOSED | spec:315‑318 pinned format both sides; test item 9 (spec:346) round-trip incl. `|`/backtick/200-char title |
| edge-cases | F-9 | RESUME on absent/empty handoffs dir | CLOSED | spec:289 "say so plainly and offer CREATE — do not prompt" |
| edge-cases | F-10 | `BLOCKED` from auto-generated metadata has no escape hatch | **PARTIAL** | spec:217 adds the exemption but never delimits "the auto-generated metadata block" → new **F-2** (P1) below |
| edge-cases | F-11 | Preconditions: two paths, one line, no re-verification | CLOSED | spec:10‑23 hard gate + "Verification step, not a fallback"; git confirms 5/4 red on `origin/main`, 7/7 green locally |
| edge-cases | F-12 | Leaf invariant vs. real nested documents | **PARTIAL** | spec:181 scopes the invariant to `TEMPLATE_SECTIONS`; spec:183 adds a subtree fallback with no terminator and no API → new **F-1** (P1) below |
| edge-cases | F-13 | Inline code spans unmasked | **PARTIAL** | spec:117 masks them, but no pairing/ordering rule is given where fences got one → new **F-5** (P2) below |
| edge-cases | F-14 | `sys.path` mutation; `__pycache__` mirroring | CLOSED | spec:150 `importlib.util.spec_from_file_location`; spec:51 + spec:396 record `__pycache__` as pre-existing/deferred |
| edge-cases | F-15 | Chain cycle keyed on filenames | CLOSED | spec:291 `resolve()`d absolute paths, case-insensitive on Windows; cap/rubric untested by declared design (spec:351) |
| edge-cases | F-16 | Two CommonMark divergences | CLOSED | spec:109 records both as deliberate |
| correctness | F-1 | CRLF into title | CLOSED | same as edge-cases/F-1 |
| correctness | F-2 | Measurement on masked copy | CLOSED | same as edge-cases/F-2 |
| correctness | F-3 | Thematic break left as prose | CLOSED | spec:95‑98 pinned to the character |
| correctness | F-4 | Setext bullet contradicts terminator | CLOSED | spec:108 |
| correctness | F-5 | Two different fence algorithms described | CLOSED | spec:115 — reuses `lint.py:55`'s *shape*, explicitly not its pairing (verified: `lint.py:211‑213` is an unconditional toggle) |
| correctness | F-6 | Exit codes vs. in-process `load_script`; no `main` contract | CLOSED | spec:307/324 `main(argv) -> int`; spec:336 asserts on the returned int |
| correctness | F-7 | `create_handoff.py` omits the `_sections` import | CLOSED | spec:307 states it explicitly |
| correctness | F-8 | `TEMPLATE_SECTIONS` never enumerated | CLOSED | spec:159‑179 full table + `REQUIRED`/`RECOMMENDED` split |
| correctness | F-9 | Bounded read names the wrong end | CLOSED | spec:193 "discard the **first** line if the read did not start at byte 0" |
| correctness | F-10 | Stale `lint.py:52` anchor | CLOSED | spec:191 now cites `lint.py:60`; verified `_CASE2_TAG` is at line 60 |
| correctness | F-11 | D12's AGENTS.md claim inaccurate | CLOSED | spec:262 now concedes `skills/spec-close/SKILL.md` has an ordinary row; verified at `AGENTS.md:54` |
| correctness | F-12 | "before or alongside" reopens the scope boundary | CLOSED | spec:390 "resolved *before* this work… not part of this spec's diff" |
| conventions | F-1 | `sys.path` vs. talaria precedent | CLOSED | spec:147‑155 |
| conventions | F-2 | Asymmetric `_sections` pin | CLOSED | spec:307 |
| conventions | F-3 | `lint.py` citations describe behavior it lacks | CLOSED | spec:85/115/191/348 — all four anchors verified correct |
| conventions | F-4 | Uninstall command POSIX-only, unqualified | CLOSED | spec:234‑238 harness-qualified + dual-shell |
| conventions | F-5 | Fixture lands flat in the lint corpus | CLOSED | spec:37‑40 subdirectory + "no `-text` entry"; verified root `.gitattributes` is `*.md text eol=lf` |
| conventions | F-6 | Bare `python` | CLOSED | spec:363 pin-by-full-path rule |
| conventions | F-7 | Unauthorized spec-level additions | CLOSED | spec:394 recorded in § Deferred for drift-check |
| conventions | F-8 | D12 rationale partly inaccurate | CLOSED | spec:262 |

No REOPENED items. Two PARTIALs and one PARTIAL-adjacent carry their new defects as fresh findings below.

## Findings

### F-1: The nested-document subtree fallback has no terminator and no API to compute one — and the terminator it will most likely get re-admits the boilerplate bypass D3 exists to prevent
**Severity:** P1
**Where:** spec.md:183 (fallback rule); spec.md:145 (module exports); spec.md:157 (depth-blind rule); spec.md:123‑135 (`section_span` contract); spec.md:342 (test item 5)
**Edge case:** A required section with empty own content followed by a deeper heading — the case D4 says occurs in two of the five real documents.
**What happens:** The implementer cannot compute "the full subtree" from the declared API. `_sections.py` exports `section_span(masked, name)`, whose contract is explicitly name-keyed and depth-blind ("Lookup is BY NAME ONLY; depth never participates in matching", spec.md:126‑131) and which returns only `(start, end)` — no depth, no heading index. Determining where a subtree *ends* requires the matched heading's depth and the depth of every subsequent heading. Two consequences:
1. The call site re-derives heading structure with its own `_HEADING_RE.finditer` scan in `validate_handoff.py` — reinstating the "matcher re-decided per call site" pattern the entire spec exists to abolish, and directly against done-when #2's "every call site derives from them" (spec.md:376).
2. The natural terminator ("next heading of depth ≤ own") silently drops the thematic-break rule that `section_span` carries. spec.md:111 says a missing thematic-break terminator lets "the last section absorb the 588–875 characters of trailing boilerplate the corpus actually carries — an *empty* required section returning `READY`… A silent gate bypass is worse than a false `incomplete`." An empty required container that is the last `##` in a document with a `---` footer gets exactly that verdict through the fallback path.

Additionally undefined: whether "immediately followed by a deeper heading" is measured on the masked or original text (spec.md:113 masks only for *matching*, and the emptiness test at spec.md:140 is on the original — so a section whose body is a fenced block has non-empty own content and never triggers the fallback, which is right, but nothing says so); and what `incomplete` reports as its measured length when the fallback fires, given spec.md:215 pins the format to `27/50 chars`.
**Why the spec misses it:** The fallback was added at spec.md:183 to close round‑2 edge-cases/F-12, but D4's exports list (spec.md:145) and `section_span`'s docstring (spec.md:123‑135) were not revised alongside it. Test item 5 (spec.md:342) exercises only the positive direction — "a substantial subtree validates complete" — so no test would catch either the depth-blind re-derivation or the dropped thematic break.
**Suggested fix:** Add a `subtree_span(masked, name) -> (start, end) | None` to `_sections.py`'s declared exports and specify it in D3 alongside `section_span`: same masked input, `end` is the offset of the next heading **of depth ≤ the matched heading's depth**, the next thematic break, or `len(masked)` — whichever comes first. State that the fallback fires only when `original[start:end].strip()` is empty and the character immediately at `end` begins a deeper heading, that the fallback's length is measured on the original over the subtree span, and that an `incomplete` finding under the fallback reports `N/50 chars (subtree)` so the report distinguishes the two paths. Add to test item 3 or 5: an empty required container whose subtree is followed by a `---` footer plus 500 characters of boilerplate must still report `incomplete`.

### F-2: The `BLOCKED` metadata exemption is never delimited, so the generic secret class — the spec's own "dominant real-world leak" — can be disarmed by any author who writes one heading
**Severity:** P1
**Where:** spec.md:217 (D6 escape hatch); spec.md:326 (validator check order); spec.md:163 (`Session Metadata` row); spec.md:69 (container names are the implementer's choice); spec.md:343 (test item 6)
**Edge case:** A handoff document that contains a `## Session Metadata` heading written by the author rather than by `create_handoff.py` — or any credential pasted below whichever heading the implementer happened to pick for the metadata container.
**What happens:** `validate_handoff.py` reads a file off disk with no knowledge of what generated it (spec.md:324 — its only input is a path). "The auto-generated metadata block" therefore has to be recognized structurally, and the spec never says how. Every plausible delimitation is exploitable:
- **By section name** — the exemption region becomes `section_span(masked, "Session Metadata")`, and an author who pastes `.env` lines under that heading, or who adds such a heading anywhere in the document, gets the generic assignment class silently disarmed over that span. That is the class spec.md:67 calls "**the dominant real-world leak** — a line pasted from `.env`, a CI log, or a `docker run`". A security gate whose exemption region is authored content is not a gate.
- **The anchor is not even stable.** `Session Metadata` is classed `container/meta` (spec.md:163), and D1 says "**Container heading names are *not* fixed** — they are never matched or validated, so the implementer chooses them freely" (spec.md:69). The one name the security exemption must key on is a name D1 declares free-floating and explicitly never matched.
- **The region provably spans authored content.** spec.md:217 says the auto-generated material is "branch names, commit subjects, and file paths", but file paths land under `### Files Modified` (spec.md:170) — a *recommended, author-filled* section. Any region wide enough to cover the generated file table also covers text the author writes.
- **Absent-heading case:** a legacy or renamed document has no such heading, the exemption region is empty, and a scaffold whose HEAD subject carries `client_secret = …` is `BLOCKED` with the "no remedy" condition D6 was written to eliminate.

**Why the spec misses it:** The exemption was added to close round‑2 edge-cases/F-10, which asked for an escape hatch; the review did not ask for a region and the revision defined one only by adjective ("auto-generated"). Test item 6 (spec.md:343) tests the exemption's positive case and "the same string in authored body text is [BLOCKED]" — but "authored body text" is undefined, so a test placed in `## Current State Summary` passes while the smuggling path through the exempt heading stays untested.
**Suggested fix:** Replace the region-based exemption with a value-based one, which needs no delimiter and cannot be smuggled into: `create_handoff.py` records the exact generated metadata lines it emitted (or, simpler and stateless: `validate_handoff.py` exempts a generic-class match **only when the matched line is byte-identical to a line obtainable from `git log --format=%s -5` / `git status` output at validation time**). If a region-based rule is kept instead, D6 must (a) name `Session Metadata` a **fixed, matched** name and carve it out of D1's "container names are free" sentence, (b) state that the region is the `section_span` of that name and nothing else, (c) state that the generated file table must therefore live inside it, not under `Files Modified`, and (d) add a test-item-6 case: a `KEY=<20 chars>` line authored under `## Session Metadata` in a hand-written document **must still be `BLOCKED`**.

### F-3: `--project-path` is declared to base exactly two things, and the git invocation is not one of them — so the document's branch and commits come from the wrong repository, and test item 8 fails as written
**Severity:** P1
**Where:** spec.md:309 (`--project-path` bases "**both** the output directory and `--continues-from` resolution"); spec.md:312 (git metadata); spec.md:345 (test item 8); spec.md:290 (RESUME's branch-mismatch rule)
**Edge case:** `create_handoff.py --project-path <other-dir>` invoked from a process whose CWD is a different repository — which is precisely how test item 8 runs it, and the only reason the flag exists.
**What happens:** `subprocess.run(["git", ...])` inherits the process CWD. The document is written into `<other-dir>/.claude/handoffs/` but pre-filled with the *calling* repository's branch, last five commits, and modified files. Nothing errors; the artifact is silently wrong in its most load-bearing field. RESUME then reads it and applies spec.md:290 — "**Compare the recorded branch against the current one first** — a mismatch is itself a staleness signal and outranks commit count" — to a branch name from an unrelated repo, producing a confident wrong staleness verdict.

Test item 8's first case is unpassable as specified: "Generation in a temp dir **isolated from any ancestor repo** (`GIT_CEILING_DIRECTORIES` set, or `GIT_DIR`/`GIT_WORK_TREE` scrubbed) asserts placeholder text." Tests run in-process (spec.md:336) with CWD at the repo root, so git resolves `vigil-skills` itself and returns a real branch — `GIT_CEILING_DIRECTORIES` bounds git's *upward* walk and does not suppress a repository at the CWD. The assertion on placeholder text fails, and ship-spec's test loop burns iterations on it.
**Why the spec misses it:** The emphasis on "**both**" reads as an exhaustive enumeration, and § `create_handoff.py`'s git bullet (spec.md:312) specifies timeout and failure classification in detail while never naming a working directory. No round-2 finding touched the flag's scope.
**Suggested fix:** Amend spec.md:309 to "bases the output directory, `--continues-from` resolution, **and the working directory of every git subprocess** (`cwd=<resolved project path>`)" and add the same to spec.md:312's bullet. Amend test item 8 accordingly: the isolation case becomes "generation with `--project-path <tmpdir>` where `<tmpdir>` is not inside a repository asserts the not-a-repo placeholder, with the test process CWD left at the repo root" — which then tests the fix rather than the environment.

### F-4: The "same-second collision check" is required by the test plan and referenced by the design, but defined nowhere — and `os.replace` is the operation that clobbers, not the one that prevents it
**Severity:** P1
**Where:** spec.md:319 ("Atomic write… This also makes the same-second collision check race-free"); spec.md:345 (test item 8: "same-second collision does not clobber"); spec.md:223 (naming scheme)
**Edge case:** Two `create_handoff.py` runs producing the same `YYYY-MM-DD-HHMMSS-<slug>.md` — most realistically the same run retried, or a scripted create immediately following a failed one within the same second.
**What happens:** Three separate defects sit in one sentence:
1. **No collision policy exists anywhere in the spec.** spec.md:319 refers to "the same-second collision check" with a definite article, as though it were defined earlier; grep of the whole spec finds no other mention. The implementer has no rule for what to do when the target exists — overwrite, suffix, error, bump the timestamp.
2. **`os.replace` makes clobbering silent and unconditional.** It is atomic *replacement*: it destroys an existing same-named document with no error and no trace. Atomicity is orthogonal to collision safety — the claim at spec.md:319 is backwards, and an implementer who trusts it writes exactly the clobbering code test item 8 forbids.
3. **The temp path collides too.** `<name>.md.tmp` is derived from the same colliding name, so two concurrent runs write interleaved bytes into one temp file before both `replace` it — defeating the atomicity guarantee the bullet exists to provide. The spec also never specifies cleanup of a `<name>.md.tmp` left by an interrupted run; RESUME ignores them (spec.md:289), so they accumulate indefinitely.

**Why the spec misses it:** The atomic-write bullet was carried forward unchanged from v1/v2 and the collision clause reads as a corollary of atomicity rather than a separate mechanism. No round-2 lens probed it.
**Suggested fix:** Add an explicit bullet under § `create_handoff.py`: "**Collision:** the target name is claimed with `open(path, 'x')` (or `os.open(..., O_CREAT|O_EXCL)`) before rendering; on `FileExistsError`, append `-2`, `-3`, … up to a small cap, then fail non-zero. The temp file is created in the same directory with a unique suffix (`tempfile.mkstemp(dir=..., suffix='.md.tmp')`) so concurrent runs never share it, and is removed in a `finally` if the render fails." Then correct spec.md:319 to say atomicity and collision-safety are two mechanisms, not one.

### F-5: Inline-code-span masking was added with no pairing rule and no ordering relative to fence masking — the one matcher in `_sections.py` left for the call site to invent
**Severity:** P2
**Where:** spec.md:117 ("Inline code spans are masked too"); spec.md:113 (masking definition); spec.md:115‑116 (fence pairing and unterminated fence, both pinned)
**Edge case:** An unpaired backtick in prose — "don't use \`--prune" — or a document containing an odd number of backticks, or a double-backtick span, or a fenced block whose ``` delimiters are themselves backtick runs.
**What happens:** Depends entirely on the regex the implementer picks, and the spec constrains none of it:
- A pattern using `.` with `re.DOTALL`, or `` `[^`]*` `` against the whole normalized document, pairs a stray prose backtick with one hundreds of lines away and masks every heading in between. Those sections then report `missing` on a valid document — the exact ticket symptom VHS-28 was filed for, arriving through the fix meant to remove it.
- **Ordering is unspecified.** If inline masking runs before fence masking, a naive backtick pattern pairs an opening ``` fence's delimiters with the closing fence's and consumes the block, after which fence detection on the masked copy finds no fences at all and `lint.py`-style pairing (spec.md:115) never runs. If it runs after, a `~~~` block's contents are already spaces and the question is moot — but the spec does not say which.
- **Masking can manufacture structure.** Because the mask is length-preserving, a three-character span at line start becomes exactly three spaces: `` `x` ## Foo `` masks to `   ## Foo`, which `_HEADING_RE`'s `^ {0,3}` accepts as a real heading, and `` `x`--- `` masks to `   ---`, which `_THEMATIC_BREAK_RE` accepts as a terminator — truncating the enclosing section on a document that contains neither.

**Why the spec misses it:** spec.md:117 was added as a one-line answer to round‑2 edge-cases/F-13 (P3), while the fence rules beside it got a full paragraph each. D3's stated premise is that a matcher left unspecified is a matcher each call site re-decides (spec.md:81) — this is the only matcher in the module that v3 leaves that way.
**Suggested fix:** Add to D3, next to the fence bullets: "**Inline code spans** are matched per CommonMark run-length rules but bounded to a single line: an opening run of N backticks pairs with the next run of exactly N backticks **on the same line**; an unpaired run masks nothing. Masking is applied **fence-first, then inline spans on the already-masked copy**, so fence delimiters are never candidates for span pairing. Because masking is length-preserving, matching runs on the fully masked copy in one pass — no heading or thematic-break match may be produced by a span that was not one in the original; implementations must therefore mask spans to spaces only *within* the span's own byte range and never across a line boundary." Add to test item 2: a body line containing one unpaired backtick leaves all following sections findable, and a `` `x` ## Foo `` line is not treated as a heading.

### F-6: The unterminated-fence advisory silently changes verdicts, and its effect on the exit code is undefined
**Severity:** P2
**Where:** spec.md:116 (the rule); spec.md:205‑207 (verdict table); spec.md:215 ("All violations print before the verdict"); spec.md:339 (test item 2); spec.md:109 ("Two deliberate CommonMark simplifications")
**Edge case:** A handoff document that ends inside a code block — a pasted command sequence or stack trace as the final content, which is a common shape for a "here's where I left off" document.
**What happens:** Three unhandled consequences of "treat the document as unfenced from the opener onward":
1. **This is not a pathological input, it is valid CommonMark.** CommonMark closes an open fence at end of document; such a document is well-formed and its block content is code. Under spec.md:116 that content is un-masked, so a `# comment` inside a pasted shell block becomes a live heading that terminates the enclosing required section (false `incomplete`), a `---` inside a pasted diff becomes a thematic break with the same effect, and a `[TODO: …]` inside a pasted snippet trips the TODO check → `NEEDS WORK`. The remedy trades a silent blank-out for a noisy false negative, on a document class that is common rather than broken. D3 records exactly "two deliberate CommonMark simplifications" (spec.md:109) and this — the largest divergence of the three — is not among them.
2. **Verdict impact is undefined.** The verdict table (spec.md:205‑207) has three verdicts plus exit 3; an "advisory finding" is in none of them. spec.md:215 says "All violations print before the verdict", so an implementer who classes the advisory as a violation returns `1` on an otherwise clean document. Nothing in the spec says whether the advisory is gate-affecting.
3. **Scope of "masks nothing" is ambiguous.** The sentence opens with "masks nothing" (whole document?) and continues "from the opener onward" (only the tail?). Properly-paired fences earlier in the document should stay masked; the sentence permits reading it either way.

**Why the spec misses it:** The rule was written to close round‑2 edge-cases/F-4, framed around the *stray* fence. The legitimate document-ends-in-a-fence case was never separated from it, and test item 2 asserts only that "post-fence required sections are still found, with the advisory finding emitted" — never what verdict results.
**Suggested fix:** Split the two cases in D3: "A fence left open **at end of document** is closed at EOF per CommonMark and masks normally — no advisory. A fence opener followed by a closer of the wrong character or insufficient length is a genuine mismatch: mask nothing from that opener onward and emit the advisory." Add to D6: "The unterminated-fence advisory is **not gate-affecting** — it prints in the findings block, is excluded from the violation count, and never changes the verdict or the exit code." Add to test item 2: a document ending inside a fence containing a `# comment` and a `[TODO: x]` validates `READY`/`0` with no advisory.

### F-7: The redaction rule prints short credentials in full
**Severity:** P2
**Where:** spec.md:215 ("a **redacted** excerpt (first 4 and last 4 characters, middle masked)"); spec.md:67 (generic class, minimum value length ≥8)
**Edge case:** A generic-assignment match whose value is at or near the ≥8-character floor — `password: hunter22`, `api_key: sw0rdf1sh`.
**What happens:** "First 4 and last 4" applied to an 8-character value reproduces all 8 characters with nothing masked; at 9–11 characters it masks one to three. The `BLOCKED` report — the artifact whose entire purpose is to stop a credential propagating — prints the credential to stdout, where the agent reads it and may echo it into the handoff document, a PR body, or a chat transcript. Whether the excerpt is the whole matched line or just the captured value is also unstated; if it is the line, a `KEY=<8 chars>` line is `KEY=` … the value's tail, which is barely better.
**Why the spec misses it:** The rule was written for the branded-prefix class (`sk-ant-api03-…`, `ghp_…`), where 40+ characters make first-4/last-4 genuinely redacting. The generic class with its ≥8 floor was added in the same decision (spec.md:67) but the redaction arithmetic was not revisited against it.
**Suggested fix:** Amend spec.md:215: "the excerpt is the **matched value** (never the whole line), redacted as first 4 + last 4 with the middle masked **only when the value exceeds 12 characters**; at 12 or fewer, the excerpt is `<pattern-name>, N chars, fully masked` — the `<file>:<line>` locus already identifies the line for the author, so no plaintext is needed to act on the finding." Add to test item 6: a `BLOCKED` report for an 8-character generic value contains none of that value's characters.

### F-8: A `[TODO: …]` inside a fenced block both evades the TODO check and counts toward the 50-character completeness threshold
**Severity:** P3
**Where:** spec.md:326 (check order); spec.md:339 (test item 2); spec.md:140 (measure on original); spec.md:113 (TODO scan on masked)
**Edge case:** A required section whose entire body is a fenced block containing only unfilled placeholders.
**What happens:** The TODO scan runs on the masked copy, so the fenced marker is invisible (deliberate, spec.md:339). The completeness measurement runs on the original, so the marker's characters count toward ≥50 (deliberate, spec.md:140). Composed, an entirely unfilled required section reaches `READY`/`0`. Each half is a correct round‑2 fix; the interaction between them is new in v3 and unexamined.
**Why the spec misses it:** F-1 and F-2 were closed independently, in different paragraphs of D3, and neither closure considered the other's masking surface.
**Suggested fix:** Add to spec.md:140: "the completeness measurement subtracts masked characters — `len(original[start:end].strip())` counts only positions where the masked copy is not a substituted space — so a body consisting solely of code contributes zero own content." If that is judged too strict (it would reverse test item 2's first case), instead run the TODO scan **unmasked within a section already judged complete**, or state explicitly at spec.md:339 that a fully-fenced placeholder body is an accepted gate hole and why.

### F-9: `## ` (hashes plus trailing whitespace, no title) is a heading while `##` alone is not, so the recorded "empty heading" simplification has a whitespace-dependent boundary
**Severity:** P4
**Where:** spec.md:91 (`_HEADING_RE`); spec.md:109 ("an empty heading (`###` alone) is not recognized")
**Edge case:** A trailing space left after the hashes by an editor that does not strip them.
**What happens:** `^ {0,3}(#{1,6})[ \t]+(.*?)…$` matches `"## "` with an empty title group, so that line terminates the enclosing section; `"##"` does not match and so does not terminate it. Content therefore bleeds across one form and not the other, depending on invisible whitespace. Neither form ever matches a vocabulary name, so no section is misidentified — only the terminator behavior differs, and the ≥50 measurement can pick up borrowed text in the non-terminating case.
**Why the spec misses it:** spec.md:109 records the simplification in terms of `###` alone and does not consider the whitespace variant.
**Suggested fix:** Widen the recorded simplification at spec.md:109 to "an empty heading is recognized as a *terminator* when followed by whitespace (`## `) and not when bare (`##`); neither can match a vocabulary name, so no verdict depends on the distinction" — or make it uniform by allowing `[ \t]*$` after the hashes when the title is empty.

## Summary
P0: 0 | P1: 4 | P2: 3 | P3: 1 | P4: 1

STATUS: RED P0=0 P1=4 P2=3 P3=1 P4=1
