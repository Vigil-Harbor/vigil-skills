# Edge-Cases Review — round 5 (delta)

## Closure of round 4 findings

Scoped per the delta brief to my own round-4 findings. Other lenses' round-4 items were not re-verified this pass.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | Scaffold has no document title; `Previous title` has no source (P0) | **CLOSED** | Title row `spec.md:172`; fill rule `spec.md:194`; `first_heading_title` made public `spec.md:138-140,143,147`; `None` fallback `spec.md:338`; test 2 restated as a subsequence `spec.md:358`; test 8 rechained to an authored fixture `spec.md:364`. Residual riders below (F-5, F-6, F-7, F-9) |
| edge-cases | F-2 | `open(path,"x")` strands a zero-byte `.md` (P1) | **CLOSED** for the exception paths | Four-step sequence `spec.md:324-328`; validate-before-claim `spec.md:325`; closed-handle claim `spec.md:326`; both-file cleanup `spec.md:328`; cap `-2`…`-9`; test 7 byte-identical assertion `spec.md:363`. Riders below (F-1, F-2, F-3) |
| edge-cases | F-3 | `[TODO: …]` marker unpinned (P2) | **PARTIAL** | `TODO_MARKER_RE` declared and made private `spec.md:147,149`; validator uses the same object `spec.md:345`; git-placeholder guard `spec.md:330`. **But `spec.md:351` still says the reference template carries a marker in "every section"** — the half of the round-4 fix that was not applied. See F-4 |
| edge-cases | F-4 | Fail-open coverage holes (P2) | **CLOSED** | Two new accepted-limit bullets `spec.md:26-27` |
| edge-cases | F-5 | TODO in a recommended section (P2) | **CLOSED** | `spec.md:224` states the whole-document scan is deliberate and names the perverse incentive |
| edge-cases | F-6 | Bare-path chain rule follows disclaimed links (P2) | **CLOSED — verified against the corpus** | `spec.md:300` guard. I re-ran the corpus: all 23 `Continues from` lines fall into four shapes; the three disclaimer shapes (`MCP…halted-red.md:18`, `Petasos…pet-176-spec-cycle.md:18`, `Primer…renderer-spike.md:18`) are now excluded, and the two genuine bare paths (`Primer…pri4-royal-ink-shipped.md:21`, `Zoho inventory…capability-menu.md:6`) are still followed. **No corpus document pairs a disclaimer with an href**, so the guard's no-href scoping leaves no hole |
| edge-cases | F-8 | Accepted limit mischaracterized (P3) | **CLOSED** | `spec.md:25` restated; third case added to test 5 `spec.md:361` |
| edge-cases | F-9 | `GIT_DIR`/`GIT_WORK_TREE` (P3) | **PARTIAL** | `spec.md:321` scrubs those two; the remaining discovery/index variables still redirect. See F-8 |

Anchor spot-checks on lines the diff corrected: `AGENTS.md:7` is indeed the `for Claude Code: ~/.claude/skills/` line; `lint.py:63-73` is indeed `_read_lines`. Both now correct. The new § Module conventions claim is also true — `from __future__ import annotations` is present in all six named scripts.

## Findings

### F-1: New step 3 renames a file whose `mkstemp` handle is still open — `os.replace` fails deterministically on Windows
**Severity:** P1
**Where:** spec.md:327 (§ `create_handoff.py`, collision/atomicity step 3)
**Edge case:** Every CREATE, on the operator's own platform.
**What happens:** `PermissionError [WinError 32]`, caught by the new step-4 `try/finally`, which removes both files and exits non-zero. CREATE never produces a document. Reproduced on this machine:

```
replace-with-open-fd: FAIL -> PermissionError [WinError 32] The process cannot access
  the file because it is being used by another process: '...tmp.md.tmp' -> '...a.md'
replace-after-close: OK
```

**Why the spec misses it:** Step 2 was written with exactly this hazard in mind for the *target* — "the handle is closed immediately, because on Windows `os.replace` fails with `PermissionError` while a handle on the target is open" — and the mirror-image rule for the *source* is not stated. `tempfile.mkstemp` returns an **open** OS-level fd by contract (unlike `NamedTemporaryFile`, it hands you a raw descriptor), and CPython opens it without `FILE_SHARE_DELETE`, so the rename is blocked. Step 3 as written is "Render via `tempfile.mkstemp(...)`, then `os.replace` onto the claimed name" — no close. The graceful reading exists (`os.fdopen(fd, "w", encoding="utf-8", newline="\n")` in a `with`, which the encoding-discipline bullet at spec.md:314 effectively forces), but the spec is prescriptive code-shaped text everywhere else in this sequence, and it spelled out the weaker half of the same rule two lines above.
**Suggested fix:** Extend step 3: "…then **close the descriptor** — wrap it as `os.fdopen(fd, "w", encoding="utf-8", newline="\n")` in a `with` — and only then `os.replace` onto the claimed name. On Windows the *source* handle blocks the rename exactly as the target handle does (reproduced: `WinError 32`)."

### F-2: Step 4 names `try/finally`, which also runs on success — and after the replace the claim path *is* the document
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:328 (collision/atomicity step 4)
**Edge case:** The success path of every CREATE.
**What happens:** Under a literal reading — "`try/finally` spans the claim through the replace, removing both the temp file and the claim file" — the `finally` fires after a *successful* `os.replace` and deletes the freshly written handoff. CREATE prints a path to stdout (spec.md:339) for a file that no longer exists, and the very next `validate_handoff.py <file>` exits `3`. The trap is that once `os.replace` succeeds, "the claim file" and "the document" are the same path, and nothing in step 4 says the claim stops being a claim at that moment.
**Why the spec misses it:** The bullet states the right *condition* ("on any failure") but names the one construct that ignores conditions. The two halves contradict each other. Test item 2's round-trip would catch a literal implementation immediately, which is why this is P2 and not P1 — but the spec should not require the test to disambiguate its own prose.
**Suggested fix:** Replace the construct with the condition: "Track the claim in a flag cleared the instant `os.replace` returns. On **any exception** between the claim and that point, remove both the temp file and the claim file, then re-raise — `finally` alone is wrong here, because after a successful replace the claim path is the document."

### F-3: The claim file is a `.md`, so a hard kill (not an exception) still strands it — and RESUME offers it as the newest handoff
**Severity:** P2
**Where:** spec.md:326 (step 2), spec.md:328 (step 4), spec.md:298 (RESUME listing)
**Edge case:** The process is killed — `taskkill`, an IDE stop button, a terminal close, a power loss — during the up-to-four 10-second git subprocesses that run *after* the claim (spec.md:329).
**What happens:** Step 4's cleanup is exception-scoped, so a hard kill bypasses it entirely and leaves a zero-byte `YYYY-MM-DD-HHMMSS-<slug>.md` dated now. RESUME lists `*.md` newest-first and ignores only `*.tmp` (spec.md:298), so the orphan is the *first* candidate offered; it validates `NEEDS WORK` with all three sections missing. The window is real — up to ~40 seconds of git subprocess time with the claim already on disk.
**Why the spec misses it:** The round-4 fix correctly widened the cleanup to cover raised exceptions and stopped there; the persistence checklist's atomicity item is about the writer being *killed*, which no `try` block covers. Note that the spec already owns the mechanism that solves this — RESUME's `*.tmp` exclusion.
**Suggested fix:** Claim under a name RESUME already ignores: "Claim `<stem>.md.tmp` with `open(..., "x")`, and `os.replace` the rendered temp onto `<stem>.md` as the final step. A claim that outlives the process is then a `.tmp`, which RESUME already skips, so a hard kill leaves no candidate document." If the `.md` claim is kept deliberately, record the hard-kill orphan as an accepted limit next to D0's list.

### F-4: `reference/handoff-template.md` is still specified as carrying a marker in *every* section — contradicting the new spec.md:330 and the new test item 2
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:351 (§ `reference/handoff-template.md`), against spec.md:330 and spec.md:358
**Edge case:** The shipped reference document, and any implementer who builds the scaffold from it.
**What happens:** spec.md:351 reads "every section carrying a `[TODO: …]` marker (which is what completeness now rests on)". spec.md:330 — new this round — says `Session Metadata`, `Recent Commits`, `Files Modified` and `Handoff Chain` **never** carry one, and test item 2 — also new — asserts "exactly one `[TODO: …]` per `REQUIRED ∪ RECOMMENDED` name and **none anywhere else**". Three statements, two answers. An implementer following spec.md:351 writes markers into the generated sections of the reference doc, and the reference doc then no longer describes what `create_handoff.py` emits — which matters, because the reference is the annotated mirror of the scaffold and ships into operator installs.
**Why the spec misses it:** Round-4 F-3's suggested fix had two edits — pin `TODO_MARKER_RE` in `_sections.py`, and amend the template section to "every *authored* section". The first landed; the second did not.
**Suggested fix:** spec.md:351 → "…depths matching `TEMPLATE_SECTIONS`, every **authored** section (`REQUIRED ∪ RECOMMENDED`) carrying a `[TODO: …]` marker and the generated/fixed-format sections carrying none, matching spec.md:330."

### F-5: The `None`-row rule sweeps in two *named* container rows, and test item 2's "four container rows" does not match the table's three
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:192 (D4), spec.md:358 (test item 2), against the table at spec.md:170-188 and D1 at spec.md:87
**Edge case:** Building `TEMPLATE_SECTIONS` — i.e. the first thing the implementer writes.
**What happens:** spec.md:192 says "**The title row and the container rows carry `None` as their name**", but the table gives *names* to two container-class rows (`Session Metadata`, `Pending Work`) and only three rows are anonymous `*(container)*` (spec.md:176, 179, 184). spec.md:358 then says "the title row and the **four** container rows carry `None`" — which matches neither three anonymous rows nor five container-class rows. The consequence is not cosmetic: `[name for _, name in TEMPLATE_SECTIONS if name]` is a different list under each reading, and under the coherent one it *includes* `Session Metadata` and `Pending Work`, so test item 2 pins those two container titles exactly — directly contradicting D1 at spec.md:87 ("Container heading names are not fixed … the implementer chooses them freely") and spec.md:192's own restatement of it. An implementer who exercises that freedom fails their own drift test.
**Why the spec misses it:** The title row was added to the table, and the two prose sites that describe the `None` rows were written from the *class* column ("container") rather than from the Name column.
**Suggested fix:** State it by count and by row: "Four rows carry `None` as their name — the title row and the three anonymous `*(container)*` rows. `Session Metadata`, `Pending Work`, `Recent Commits`, `Files Modified` and `Handoff Chain` **are** named in the table and **are** pinned by test item 2's drift assertion; D1's 'container names are not fixed' applies only to the three anonymous rows." Correct "four container rows" at spec.md:358 to match.

### F-6: Test item 8's "authored fixture" is a third fixture that § New files does not declare, spec.md:355 says there are exactly two, and it cannot be a `--continues-from` target from `tests/fixtures/`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:364 (test item 8), against spec.md:57-58 (§ New files), spec.md:355, spec.md:332, spec.md:359
**Edge case:** Writing the test the round-4 F-1 fix promised.
**What happens:** Item 8 now chains "from an **authored fixture** whose H1 contains `|`, backticks and 200 characters". Only two fixtures are declared — `legacy-flat.md`, described as **all-`##`** (so it has no H1 at all) and `legacy-nested.md` (`##`/`###`). Neither can serve, and spec.md:355 states flatly that cases "are generated in temp dirs **except the two fixtures**". Separately, spec.md:332 makes any `--continues-from` path that resolves outside `<project-path>/.claude/handoffs/` a **hard error** — so a file living at `tests/fixtures/session-handoff/` cannot be passed to `create_handoff.py` at all; the test must copy it into the temp handoffs directory first, which is nowhere stated.
**Why the spec misses it:** The fix moved the escaping case off a generated document (correctly — spec.md:194 now bounds generated titles to `[a-z0-9 ]`) without asking where the replacement input lives or whether the CLI will accept it.
**Suggested fix:** Either add the third fixture to § New files (`tests/fixtures/session-handoff/exotic-title.md`) and say the test copies it into the temp handoffs dir before chaining, or — simpler — reword to "chains from a **hand-written predecessor the test writes into the temp handoffs directory**", and drop the word "fixture" so it does not collide with spec.md:355's count of two.

### F-7: `first_heading_title` returns `""`, not `None`, for an empty depth-1 heading — the new `None` fallback misses it
**Severity:** P3
**Where:** spec.md:138-140 (D3), spec.md:338 (chain block), against spec.md:28 and spec.md:107
**Edge case:** A predecessor document whose first depth-1 heading is `# ` — a heading the spec explicitly says is a heading (spec.md:28: "An empty heading is a heading when followed by whitespace").
**What happens:** `_HEADING_RE`'s title group is `(.*?)`, so on `"# "` it captures the empty string. `first_heading_title` returns `""`, which is not `None`, so spec.md:338's guard ("If it returns `None` … emit the filename") does not fire, and the pinned two-line format emits `  - Previous title: ` with nothing after it. Test item 8 asserts "both emitted lines match the pinned format", so this is a silent format break rather than a crash.
**Why the spec misses it:** The docstring says "or `None` if the document has none", conflating "no depth-1 heading" with "no title text".
**Suggested fix:** Either make the docstring explicit — "returns `None` when there is no depth-1 heading; may return `''` when the heading is empty" — and change spec.md:338's guard to "if it returns `None` **or an empty string**", or specify that `first_heading_title` normalizes an empty title to `None`.

### F-8: The `GIT_*` scrub covers two variables; `GIT_INDEX_FILE` and the other discovery variables still redirect the child
**Severity:** P3
**Where:** spec.md:321 (§ `create_handoff.py`, `--project-path`)
**Edge case:** `create_handoff.py` invoked from a git hook — the case the bullet itself names.
**What happens:** A hook exports far more than the two scrubbed names: `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_PREFIX`, and (for worktrees) `GIT_COMMON_DIR`; `GIT_CEILING_DIRECTORIES` and `GIT_DISCOVERY_ACROSS_FILESYSTEM` also alter discovery. With `GIT_DIR` and `GIT_WORK_TREE` removed but `GIT_INDEX_FILE` still set, `git status --porcelain` reads the *other* repository's index, so the document's "modified + staged files" table is silently wrong — the exact silent-wrong-data outcome the bullet's own rationale describes ("it fails silently because git succeeds, just against the wrong repository"), narrowed rather than eliminated.
**Why the spec misses it:** The fix enumerated the two best-known variables. The failure class is "any inherited `GIT_*`", not those two.
**Suggested fix:** State it as a class rather than a list: "…with **every inherited `GIT_*` variable removed from the child environment** (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_CEILING_DIRECTORIES`, … — a hook exports all of these), so `cwd` alone decides the repository."

### F-9: spec.md:194's "bounds what `Previous title` can ever have to escape" is false for a predecessor this skill did not generate — which spec.md:338 explicitly allows
**Severity:** P3
**Where:** spec.md:194 (D4), against spec.md:338 and spec.md:364
**Edge case:** `--continues-from` pointed at a legacy or hand-authored document — the ordinary case for the first chained handoff in any project, and the case test item 8 now builds on purpose.
**What happens:** spec.md:194 argues that because a generated title is always `[a-z0-9 ]` and ≤60 chars, the escaping surface is bounded. spec.md:338 says the opposite in the same breath — "the target need not be a document this skill generated" — and test item 8 chains from a title with `|`, backticks and 200 characters. The escaping requirement at spec.md:338 survives, so nothing breaks; but an implementer who reads spec.md:194 as a licence to skip escaping produces a `Previous title` line that can carry arbitrary markdown. Related gap: spec.md:338 specifies **backtick** escaping and 80-char truncation only, while test item 8 asserts against a `|`-bearing title — and the `|`/backtick escaping rule at spec.md:331 is scoped to *table cells*, which the chain block is not. What the test should assert about `|` is undefined.
**Suggested fix:** Narrow the claim at spec.md:194 to what it actually buys ("a *generated* predecessor's title needs no escaping; an arbitrary one still does, which is why spec.md:338 escapes unconditionally"), and settle `|` at spec.md:338: "`|` passes through unescaped — the chain block is a bullet, not a table cell."

### F-10: Git-derived content can carry the marker shape, and unlike the tool's own placeholders it is not clearable
**Severity:** P3
**Where:** spec.md:330 (marker placement), spec.md:149 (`TODO_MARKER_RE`), spec.md:345 (whole-document scan)
**Edge case:** One of the last 5 commit subjects, or a modified file path, contains `[TODO…]` — e.g. a `[TODO] wire up X` subject, a convention some repos use.
**What happens:** `create_handoff.py` injects it into `### Recent Commits` or `### Files Modified`; the whole-document `TODO_MARKER_RE` scan then reports `NEEDS WORK`/exit 1 on a fully written handoff. The author must hand-edit generated content, and the next CREATE in that repo reproduces it — a gate nobody can clear, which is the failure class D6 was rewritten to eliminate. spec.md:330 anticipates precisely this shape for the tool's *own* diagnostic strings ("A git placeholder written as `[TODO: not a git repository]` would make every CREATE outside a repo permanently un-`READY`") but not for the git *data* passing through the same blocks.
**Why the spec misses it:** The guard was written for strings the implementer controls. The injected path was not considered.
**Suggested fix:** One clause on the markdown-safety bullet at spec.md:331, mirroring the escaping already there: "`|`, backticks, **and a leading `[` of any `[TODO…]`-shaped run** are escaped before git-derived text enters the document, so generated content can never trip the completeness scan." *(Verified as a non-issue for the corpus itself: I re-scanned all 23 on-disk documents with the broader `\[TODO\b[^\]]*\]`/IGNORECASE pattern and with the narrow `[TODO:` literal — both return zero, so spec.md:27's measurement holds under the new regex.)*

### F-11: Two nits in new text
**Severity:** P4
**Where:** spec.md:194, spec.md:326
**What happens:** (a) spec.md:194 attributes `first_heading_title` to **D5** ("D5's `first_heading_title` reads exactly this line"); it is declared in D3 (spec.md:138) and D4 (spec.md:147). D5 is session transfer. (b) spec.md:326's "append `-2` … `-9`" does not say *to what*: appending to the full path yields `…-slug.md-2`, which RESUME's `*.md` listing would never show. The stem is obviously meant; say so.
**Suggested fix:** Fix the D-number; write "append `-2` … `-9` **to the filename stem**, before `.md`".

## Summary
P0: 0 | P1: 1 | P2: 5 | P3: 4 | P4: 1

STATUS: RED P0=0 P1=1 P2=5 P3=4 P4=1
