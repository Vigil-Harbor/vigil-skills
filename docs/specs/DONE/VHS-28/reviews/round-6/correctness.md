# Correctness Review — round 6 (delta)

Scope: the 7 hunks in `docs/specs/TODO/VHS-28.reviews/round-6/v5-to-v6.diff` and the sections they land in, plus untouched text those hunks make wrong. D0 (removal of the ≥50-char check and the `incomplete` verdict) is operator-authorized and not re-litigated.

*Grounding note:* the Plane mirror no longer returns VHS-28 — `memory_search(namespace="plane", tags=["plane_work_item","VHS-28"], source_system="plane")` returns 0 results, and a semantic probe surfaces only GAV items. Round-1's report quotes the ticket verbatim (record `806902ac-…`) and this delta touches no done-when mapping, so the brief plus round-1's transcription were used. Not filed as a numbered finding.

## Closure of round 5 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Public surface closed at 3 callables vs. a 4th + shared `TODO_MARKER_RE` | **CLOSED** | spec:121 "four public callables"; `todo_marker(name: str) -> str` declared spec:153-155; spec:158 lists all four plus `TODO_MARKER_RE` as public, "only `_HEADING_RE` stays private"; D4 spec:162 restated; spec:164 "It is **public, because both entry points use it**"; spec:341 import list widened. (That import list is still one name short — see F-3, a *new* defect on the new :353 rule, not this one.) |
| correctness | F-2 (P1) | `handoff-template.md` "every section carrying a marker" | **CLOSED** | spec:373 now "Every `required`/`recommended` section carries a `[TODO: …]` marker and the `title`/`container`/`generated`/`chain` sections carry none — matching § `create_handoff.py` exactly" |
| correctness | F-3 (P2) | Test item 8's "authored fixture" is a third fixture | **CLOSED** | spec:386 "a predecessor the test **writes into the temp handoffs directory** — not a tracked fixture, since § New files declares exactly two" |
| correctness | F-4 (P3) | D4 attributes `first_heading_title` to D5 | **CLOSED** | spec:214 "D3's `first_heading_title` reads exactly this line" |
| correctness | F-5 (P3) | Title bound measured on the slug, not the heading | **CLOSED** | spec:214 "drawn from `Handoff: ` plus `[a-z0-9 ]`, and ≤69 characters — inside the 80-character truncation below, and containing neither a pipe nor a backtick". 9 + 60 = 69, arithmetic checks |
| correctness | F-6 (P4) | `str \| None` called PEP 585 | **PARTIAL** | spec:330 now cites "PEP 585 / PEP 604", but the same sentence still says both "raise `TypeError: 'type' object is not subscriptable` on 3.8". See F-7 |
| correctness | F-7 (P4) | `normalize` docstring ships literal CRs | **CLOSED** | spec:125 is now `r"""…"""`, with the reason recorded inside it |
| edge-cases | F-1 (P1) | `mkstemp` fd still open at `os.replace` | **CLOSED** | spec:349 "**close the descriptor before renaming** … Wrap it as `os.fdopen(fd, "w", encoding="utf-8", newline="\n")` in a `with`, then `os.replace`" |
| edge-cases | F-2 (P2) | `try/finally` also runs on success | **CLOSED** — but the fix does not compose with edge-cases/F-3's; see F-2 below | spec:350 "On any exception between the claim and the successful replace … Track the claim in a flag cleared the instant `os.replace` returns" |
| edge-cases | F-3 (P2) | Claim is a `.md`, so a hard kill strands it | **CLOSED** — but the fix does not compose with edge-cases/F-2's; see F-2 below | spec:348 "**Claim `<stem>.md.tmp`**, not `<stem>.md`, with `with open(claim, "xb"): pass`" |
| edge-cases | F-4 (P2) | Template marker in *every* section | **CLOSED** | spec:373, as correctness/F-2 |
| edge-cases | F-5 (P2) | `None`-row rule sweeps named containers; "four container rows" | **CLOSED** | spec:207-212 rewritten to key on **class**; spec:380's assertion is now `[name for _, name, cls in TEMPLATE_SECTIONS if cls in ("required","recommended")]`; the "four container rows" phrase is gone. (The rewrite left the canonical tuple shape behind — F-1) |
| edge-cases | F-6 (P2) | Test 8's third fixture | **CLOSED** | spec:386, as correctness/F-3 |
| edge-cases | F-7 (P3) | `first_heading_title` returns `""` for `# ` | **CLOSED** | spec:144-151 docstring normalizes `''` to `None`; spec:360 "no depth-1 heading, or an empty one"; spec:386 asserts both cases |
| edge-cases | F-8 (P3) | `GIT_*` scrub covers only two variables | **CLOSED** | spec:343 enumerates `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR`, `GIT_CEILING_DIRECTORIES`, `GIT_PREFIX`, "every inherited `GIT_*` variable" |
| edge-cases | F-9 (P3) | "bounds what `Previous title` can ever have to escape" false for foreign predecessors | **CLOSED** | spec:216 "**That bounds generated predecessors only** … the chain block escapes **unconditionally**" |
| edge-cases | F-10 (P3) | Git-derived text can carry the marker shape | **PARTIAL** | spec:353 adds the rule, but the escaping mechanism it names does not defeat `TODO_MARKER_RE` and the matcher is not in create_handoff's import list. Superseded by F-3 (P1) below |
| edge-cases | F-11 (P4) | D-number slip; "append `-2`…`-9`" to what | **CLOSED** | spec:214 "D3's"; spec:348 "append `-2` … `-9` **to the filename stem, before the extension**" |
| conventions | F-1 (P0) | `Files Modified` recommended vs. marker-excluded; item 2 unsatisfiable | **CLOSED** | Resolved on the opposite branch, and consistently: the table keeps it `recommended` (spec:195); spec:205's "the six marked recommended" matches the table exactly — Architecture Overview, Critical Files, Files Modified, Decisions Made, Assumptions Made, Potential Gotchas; spec:209 and spec:352 put a marker in every `required`/`recommended` row and name `Files Modified` explicitly; spec:373 mirrors it in the template; D6 spec:246 ("a marker in a recommended section is `NEEDS WORK`") stays consistent — a fresh scaffold is *meant* to be `NEEDS WORK`; test item 2's count is "per `required`/`recommended` row" = 9 = 3 + 6. **Where that marker physically goes is now unspecified — see F-5** |
| conventions | F-2 (P2) | `TODO_MARKER_RE` declared private, then shared | **CLOSED** | spec:158, spec:162, spec:164 |
| conventions | F-3 (P4) | Temp naming drops the dot-prefix precedent | **CLOSED** | spec:349 `prefix=".session-handoff."`; all four cited anchors verified on disk — `talaria_bridge.py:420`, `talaria_watch.py:123`, `talaria_watch.py:140`, `talaria_read.py:174` are each `tempfile.mkstemp(prefix=".…", suffix=".tmp", dir=…)` |
| conventions | F-4 (P4) | Claim opens text mode with no encoding | **CLOSED** | spec:348 `open(claim, "xb")`, with the reason stated |
| conventions | F-5 (P4) | "the four container rows" | **CLOSED** | phrase removed; spec:212 now says "The three anonymous `*(container)*` rows", which matches the table |

**Git-failure placeholder compliance (asked for explicitly).** The only literal placeholder string anywhere in the spec is `_not a git repository_` (spec:352). spec:351 names the other two categories (no-commits, git-unavailable-or-timed-out) without pinning strings, and no other section introduces one. `_not a git repository_` returns no match against `re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)` — verified by execution. Test item 7 pins the tested one ("the not-a-repo scaffold, with its markers replaced, validates `READY`"). **Compliant**, with the caveat that the two unpinned strings rely on the implementer honouring the explicit prohibition at :352.

**`todo_marker()` surface agreement (asked for explicitly).** spec:121 ("four public callables"), the D3 code block (spec:124/133/143/153), spec:158 (public-surface sentence), spec:162 (D4 declaration list) and spec:341 (create_handoff import list) all agree on four callables and on `TODO_MARKER_RE` being public. The one call site, spec:352, writes `_sections.todo_marker()` with no argument shown against a declared `todo_marker(name: str) -> str`; read as prose shorthand rather than a signature claim. No finding.

## Findings

### F-1: `TEMPLATE_SECTIONS` is declared as a 2-tuple table while both of the delta's new consumers unpack three elements

**Severity:** P0
**Where:** spec.md:183 (untouched) vs spec.md:210 and spec.md:380 (both new in v6)

**Claim:**
- spec:183 — "**`TEMPLATE_SECTIONS`** — an ordered `(depth, name)` table; **depth governs rendering only**."
- spec:210 — "compares against `[name for _, name, cls in TEMPLATE_SECTIONS if cls in ("required", "recommended")]`"
- spec:380 — the same expression, in test item 2.

**Why this is wrong:** `for _, name, cls in …` requires a 3-tuple; `(depth, name)` is a 2-tuple. An implementer who writes the module from its canonical declaration at :183 — `TEMPLATE_SECTIONS = [("#", None), ("##", "Session Metadata"), …]` — gets `ValueError: not enough values to unpack (expected 3, got 2)` the first time test item 2 runs, and has no declared home for the class column at all, even though the class is now the *only* thing driving marker placement (:209) and the drift assertion (:210).

This is precisely the recurrence pattern round 6 was asked to hunt. In v5 the table's third column existed but nothing consumed it, and test item 2 read `[name for _, name in TEMPLATE_SECTIONS if name]` — a 2-tuple, consistent with :183. The v6 hunk rewrote **both** consumers to a class-keyed 3-tuple (correctly closing conventions/F-5 and edge-cases/F-5) and left the declaration sentence at its v5 arity. Same shape as round-4's `_HEADING_RE` and round-5's `TODO_MARKER_RE`: the fix landed everywhere except the line that declares the thing.

Secondary, same line: :183 says "Container names (marked `*(container)*`) are the implementer's choice per D1", granting the naming freedom only to the three anonymous rows — while :212 (new) extends it to every non-`required`/`recommended` row, explicitly including "or to rename `Pending Work`", and by implication `Session Metadata`, `Recent Commits` and `Handoff Chain`. :183 is now the narrower of two statements of one rule.

**Suggested fix:** spec:183 → "**`TEMPLATE_SECTIONS`** — an ordered `(depth, name, class)` table, one entry per row below; **depth governs rendering only, and `class` governs everything else** (the two rules under the table). `name` is `None` for the anonymous rows. Every row whose class is not `required` or `recommended` is free-named per D1:"

---

### F-2: The claim moved to `<stem>.md.tmp` but step 4 still reasons as though the claim path becomes the document — so the claim leaks on every success, and `<stem>.md` is no longer guarded against clobber

**Severity:** P0
**Where:** spec.md:348 (step 2, new in v6) vs spec.md:350 (step 4, new in v6) and spec.md:346 (the section's stated invariant, untouched)

**Claim:**
- spec:348 — "**Claim `<stem>.md.tmp`**, not `<stem>.md`, with `with open(claim, "xb"): pass` … On `FileExistsError` append `-2` … `-9`"
- spec:349 — "then `os.replace` onto `<stem>.md`"
- spec:350 — "On any exception between the claim and the successful replace, remove both the temp file and the claim, then re-raise. Track the claim in a flag cleared the instant `os.replace` returns — a bare `finally` is wrong here, **because once the replace succeeds the claim path *is* the document**, and a `finally` would delete the handoff it just wrote."
- spec:346 — "**Collision and atomicity are two mechanisms, not one.** (`os.replace` alone is atomic *replacement* — it would clobber an existing document silently, which is the opposite of collision safety.)"

**Why this is wrong:** these are two v6 fixes — edge-cases/F-3 rewrote step 2, edge-cases/F-2 rewrote step 4 — written against different pictures of the same file. Under v5 the claim *was* `<stem>.md`, so step 4's premise held. Under v6 the claim is `<stem>.md.tmp` and the replace target is `<stem>.md`: two different paths. "Once the replace succeeds the claim path *is* the document" is now false, and three things follow.

1. **The claim leaks on every successful CREATE.** Step 4 removes the claim only on the exception path; on success the flag is cleared and nothing deletes `<stem>.md.tmp`. The handoffs directory accumulates one orphaned `.md.tmp` per handoff, permanently. Nothing in the test plan catches it — test item 7 asserts a byte-identical directory only "after a **forced rendering failure**".
2. **Collision safety now depends on that leak.** The exclusive create is on `<stem>.md.tmp`, which says nothing about whether `<stem>.md` exists. Test item 7's "a same-second collision produces `-2` rather than clobbering" passes only because the first run's claim was never cleaned up. Apply the obvious fix for (1) — delete the claim after a successful replace — and `os.replace` silently clobbers the existing document, which is exactly what :346's parenthetical says the design must never do. The two properties are coupled, and the spec states neither.
3. **A pre-existing `<stem>.md` with no `.tmp` sibling is clobbered today.** Any document written by an earlier build, restored from backup, copied in by hand, or surviving a `*.tmp` sweep of a directory whose `.tmp` files the spec itself calls "invisible" (:348) is overwritten with no warning and no `-2` suffix.

**Suggested fix:** make the claim an explicit lock with an existence check under it, and correct step 4's rationale. Step 2: "Claim `<stem>.md.tmp` … Then, **while holding the claim**, check `<stem>.md`; if it exists, release the claim and retry the whole step with `-2` … `-9` appended to the stem. Holding the lock serializes every creator of this stem, so the check is not racy." Step 4: "On any exception between the claim and the successful replace, remove both the temp file and the claim, then re-raise. **On success, remove the claim once the replace returns** — unlike v5's design the claim path is *not* the document, so removing it is correct; the flag exists only so a run that never took a claim does not delete someone else's." Test item 7: add "after a **successful** create the handoffs directory contains exactly one new file, the `.md`."

---

### F-3: The new "escape `[TODO…]`-shaped runs in git-derived text" rule does not work as written — backslash escaping still matches `TODO_MARKER_RE`, and create_handoff is not given the matcher

**Severity:** P1
**Where:** spec.md:353 (new in v6), against spec.md:164 and spec.md:341 (also new in v6)

**Claim:** spec:353 — "**Markdown safety:** … `|` and backticks escaped before entering a table cell … **Any `[TODO…]`-shaped run in git-derived text is escaped too** — a commit subject like `[TODO] wire up X` is a real convention, and unescaped it would trip the whole-document marker scan on a fully written handoff."

**Why this is wrong:** three ways, all introduced by this one new sentence.

1. **The escaping mechanism the bullet names does not defeat the pattern.** "Escaped" in this bullet's own context is markdown escaping — the `\|` / backslash-backtick treatment named a clause earlier. `TODO_MARKER_RE` is `re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)` (spec:164), unanchored, so it matches from the `[` and a preceding backslash is irrelevant. Executed against the spec's own pattern:

   ```
   '\[TODO] wire up X'    -> ['[TODO]']         # backslash escape: STILL MATCHES
   'a \[TODO: fix\] b'    -> ['[TODO: fix\]']   # escaping both brackets: STILL MATCHES
   '&#91;TODO] x'         -> []                 # entity: does not match
   ```

   An implementer who reads ":353 says escape it" and reaches for the same escaping as `|` ships exactly the unclearable gate the sentence exists to prevent: a fully written handoff in a repo with a `[TODO] …` commit subject reports `NEEDS WORK`/exit 1 forever, and the author cannot clear it without editing generated content.

2. **create_handoff has no sanctioned way to *find* the shape.** spec:341 enumerates the imports as "`TEMPLATE_SECTIONS`, `normalize`, `first_heading_title` and `todo_marker` from `_sections` … the section table and **the marker text are never restated in this file**". `TODO_MARKER_RE` is not in that list. Detecting a `[TODO…]`-shaped run needs the pattern, so the implementer either re-declares it in `create_handoff.py` — "one matcher, two places, diverging" on the single token D0 made the entire completeness gate, which spec:164 spends a paragraph forbidding — or reaches for a name :341 says the file does not import. Round-5 correctness/F-1, re-created one bullet further down.

3. **No test pins it.** Test item 7 pins only that *our own* git placeholder is not marker-shaped. Nothing generates a commit subject containing `[TODO]` and asserts the resulting scaffold, markers replaced, validates `READY` — so neither (1) nor (2) would be caught by the suite.

**Suggested fix:** (a) spec:353 → "… **and any `[TODO…]`-shaped run in git-derived text has its opening bracket replaced with `&#91;`** — a backslash does not help, since `TODO_MARKER_RE` is unanchored and matches from the `[` regardless of what precedes it. Implemented as `TODO_MARKER_RE.sub(lambda m: "&#91;" + m.group(0)[1:], text)`, so the one matcher stays the one matcher." (b) spec:341 → add `TODO_MARKER_RE` to the import list. (c) Test item 6 or 7 → add: "a scaffold generated where the HEAD commit subject is `[TODO] wire up X`, with all nine markers replaced, validates `READY`."

---

### F-4: D0's marker rule still uses the pre-class vocabulary, and now excludes a section v6 includes

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:18 (untouched) vs spec.md:207-209 and spec.md:352 (new in v6)

**Claim:** spec:18 — "`create_handoff.py` emits a `[TODO: …]` marker into every **authored** section it scaffolds (**not the generated or fixed-format ones** — see § `create_handoff.py`)".

**Why this is wrong:** v6 made the row *class* the sole driver (:207 — "the class — not the name — drives behavior") and settled `Files Modified` as recommended-and-marker-carrying (:352). But `Files Modified` is git-filled — :351 lists "modified + staged files" among the git metadata — so under :18's plain-language split it reads as a "generated" section and takes no marker. Follow :18 and a fresh scaffold carries eight markers, one short of test item 2's "exactly one `[TODO: …]` per `required`/`recommended` row" (:380). Separately, "fixed-format" is no longer a class anywhere: the v6 hunk renamed that table cell from "fixed-format (§ `create_handoff.py`)" to `chain` (:203), so :18 now cites vocabulary the schema dropped.

D0 is labelled "*read this first*", and its cross-reference to § `create_handoff.py` is the only thing keeping a reader out of the ditch. P2 rather than P1 because that cross-reference does resolve it and :352 calls `Files Modified` out by name.

**Suggested fix:** spec:18 → "`create_handoff.py` emits a `[TODO: …]` marker into exactly the sections classed `required` or `recommended` in D4's table — including `Files Modified`, whose paths git fills but whose commentary the author writes — and into no others (see § `create_handoff.py`), so …"

---

### F-5: `Files Modified` now carries a marker with no specified locus — the empty-table and N-row readings both break test item 2's count

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:352 (new in v6) vs spec.md:380 and spec.md:353

**Claim:** spec:352 — "one per such section and nowhere else … (`Files Modified` *is* classed recommended and *does* carry one: **git fills its path column, the author fills the "describe changes / why changed" cells**, which is exactly the work a marker tracks.)"

**Why this is wrong:** `Files Modified` is the one marker-carrying section whose body is a generated table (pipe-escaped cells, capped at 10 rows — :353). The justification places the author's work in *per-row cells*, the rule says *one marker per section*, and nothing says where the single marker sits. Two readings, both breaking the new count assertion at :380:

- **Marker in the per-file cells** — a 10-file working tree emits ten markers, and "exactly one `[TODO: …]` per `required`/`recommended` row" fails.
- **Marker only where a row exists** — the scaffolds test items 2 and 7 actually generate live in fresh temp directories with zero modified files, or with `_not a git repository_` prose in place of the table. No row, no marker, count one short. That is conventions/F-1's unsatisfiable-count defect re-created on the branch chosen to close it.

Making the marker section-level and unconditional also matters for `reference/handoff-template.md` (:373), which must mirror the scaffold exactly and has no git output at all.

**Suggested fix:** append to spec:352 — "The marker is **section-level and unconditional**: one line in the section body, above or below the table, never inside a table cell and never contingent on git having produced rows. Otherwise a zero-row table emits none and a ten-row table emits ten, and test item 2's count fails either way."

---

### F-6: `RECOMMENDED_SECTIONS` is still defined by a hand-maintained row count rather than by class

**Severity:** P3
**Where:** spec.md:205 (untouched) vs spec.md:207-210 (new in v6)

**Claim:** spec:205 — "`RECOMMENDED_SECTIONS` = the six marked recommended."

**Why this is wrong:** the count is correct today — the table has exactly six: Architecture Overview, Critical Files, Files Modified, Decisions Made, Assumptions Made, Potential Gotchas. But v6's thesis two lines below is that the class column is the machine-readable driver and prose counts are not, and this is the last hand-maintained row count left in the section — the same shape as the "four container rows" phrase v6 just deleted. It also makes `REQUIRED_SECTIONS`/`RECOMMENDED_SECTIONS` look like hand-written literals when they are derivable, which invites exactly the drift D4 exists to prevent.

**Suggested fix:** spec:205 → "`REQUIRED_SECTIONS` and `RECOMMENDED_SECTIONS` are **derived from the table, not written out**: `[n for _, n, c in TEMPLATE_SECTIONS if c == "required"]` (three: `Current State Summary`, `Immediate Next Steps`, `Important Context`) and the same with `"recommended"` (six)."

---

### F-7: § Module conventions still attributes the subscript `TypeError` to `str | None`

**Severity:** P4
**Where:** spec.md:330 (rewritten in v6)

**Claim:** "the PEP 585 / PEP 604 annotations used here (`list[str]` and `str | None` respectively — both a `TypeError` on 3.8 without it) **are evaluated at def time without it and raise `TypeError: 'type' object is not subscriptable` on 3.8**."

**Why this is wrong:** the v6 edit added the correct parenthetical and left the original clause standing behind it, so the sentence still says both forms raise the *subscript* error. `str | None` on 3.8 raises `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`. The parenthetical and the main clause now also say the same thing twice.

**Suggested fix:** "… are evaluated at def time without it and raise `TypeError` on 3.8 — `'type' object is not subscriptable` for `list[str]`, `unsupported operand type(s) for |: 'type' and 'NoneType'` for `str | None`." (Drop the now-redundant parenthetical.)

---

### F-8: Mid-sentence capital in the rewritten D4 paragraph

**Severity:** P4
**Where:** spec.md:164 (new in v6)

**Claim:** "It is `re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)`; **It** is **public, because both entry points use it**: …"

**Why this is wrong:** splice artifact from the patch — capital `It` after a semicolon, and two consecutive sentences opening "It is".

**Suggested fix:** "… `re.IGNORECASE)`, and it is **public, because both entry points use it**: …"

## Summary
P0: 2 | P1: 1 | P2: 2 | P3: 1 | P4: 2

Every round-5 finding across all three lenses is closed or carries a named residue, including the conventions P0: the `Files Modified` resolution holds at the table (:195), the six-row count (:205), the class rule (:209), § `create_handoff.py` (:352), the template mirror (:373), D6's recommended-marker rule (:246) and test item 2's nine-name count (:380). The two P0s and the P1 are all one failure mode, the same one as rounds 4 and 5: a v6 hunk rewrote the consumers of a rule and left the declaration, the rationale, or the enabling import pointing at the prior design.

STATUS: RED P0=2 P1=1 P2=2 P3=1 P4=2
