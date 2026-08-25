# Conventions Review — round 6 (delta-scoped)

## Closure of round 5 findings

Scoped to my own lens per the delta brief; the other lenses verify theirs.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 (P0) | `Files Modified` marker rule vs. `RECOMMENDED_SECTIONS`; test 2 count unsatisfiable | **CLOSED** | v6 took the keep-it-recommended branch and propagated it everywhere. Table classes are now total — `title`/`container`/`generated`/`chain` replace the three `—` cells (spec.md:186-202), so `RECOMMENDED_SECTIONS` = "the six marked recommended" (spec.md:205) matches the six `recommended` rows exactly, and `REQUIRED ∪ RECOMMENDED` = the nine of spec.md:210/380. The marker rule is restated class-keyed with `Files Modified` explicitly included (spec.md:352), the template mirror agrees (spec.md:372), and test item 2's count is now "exactly one per `required`/`recommended` row" (spec.md:380) — satisfiable at 9. D6's "marker in a recommended section is `NEEDS WORK`" (spec.md:243) behaves sanely: the section's *why-changed* cells are author work, so the marker tracks something clearable. Residual placement ambiguity filed NEW as F-4 below, not as a reopen |
| conventions | F-2 (P2) | `TODO_MARKER_RE` private but shared; unnamed fourth callable | **CLOSED** | `TODO_MARKER_RE` is public with the reason stated (spec.md:158, 164); only `_HEADING_RE` stays private, and no consumer touches it (`create_handoff.py` takes `first_heading_title`, spec.md:341; `validate_handoff.py` takes `has_section`, spec.md:367). The helper is named `todo_marker()` and the count agrees in all four places that state it: D3 "four public callables" + the code block (spec.md:121, 153), D4's enumeration (spec.md:162), the import list (spec.md:341), and the render site (spec.md:352). No third private-name-across-modules instance was created |
| conventions | F-3 (P4) | temp file drops the dot-prefix precedent | **CLOSED** | spec.md:349 now `mkstemp(prefix=".session-handoff.", suffix=".md.tmp", dir=…)`. All four cited precedents verified on disk and all four dot-prefix: `talaria_bridge.py:420`, `talaria_watch.py:123`, `talaria_watch.py:140`, `talaria_read.py:174` |
| conventions | F-4 (P4) | `open(path, "x")` text-mode, no encoding | **CLOSED** | spec.md:348 is `with open(claim, "xb"): pass`, with "binary because nothing is written through it" — the absence of an encoding is now self-evidently correct against § Encoding discipline (spec.md:334) |
| conventions | F-5 (P4) | "the four container rows" matches no reading of the table | **CLOSED** | The phrase is gone; the rewritten item 2 keys on class instead of on name-presence (spec.md:380), and the explanatory paragraph now says "the three anonymous `*(container)*` rows" (spec.md:212), which matches the table |

Incidental: § Module conventions' PEP 604 correction (spec.md:326) is accurate — `str | None` is a `TypeError` on 3.8 without the future import, same as `list[str]`, and the six precedent scripts all carry it.

## Findings

### F-1: `TEMPLATE_SECTIONS` is declared a 2-tuple table and consumed as a 3-tuple
**Severity:** P0
**Where:** spec.md:183, contradicted by spec.md:210 and spec.md:380
**Convention violated:** internal consistency — D4 makes `_sections.py` the single declaration of the vocabulary, so its shape must be stated once and read the same way everywhere
**Evidence:** spec.md:183 (untouched by this delta) still reads: "**`TEMPLATE_SECTIONS`** — an ordered `(depth, name)` table". Both new v6 lines unpack three fields: spec.md:210 "compares against `[name for _, name, cls in TEMPLATE_SECTIONS if cls in ("required", "recommended")]`", repeated verbatim in test item 2 at spec.md:380. In v5 the `Class` column was documentation only and the assertion unpacked two (`[name for _, name in TEMPLATE_SECTIONS if name]`), which was consistent; v6 promoted class to a runtime field in the consumers without promoting it in the declaration. This is the delta making untouched text wrong. An implementer who builds the table from spec.md:183 gets `ValueError: not enough values to unpack (expected 3, got 2)` from the literal test code the spec prints, and D4's enumeration at spec.md:162 offers no second opinion — it names `TEMPLATE_SECTIONS` without a shape.
**Suggested fix:** At spec.md:183: "**`TEMPLATE_SECTIONS`** — an ordered `(depth, name, cls)` table where `cls` is one of `title` / `container` / `generated` / `required` / `recommended` / `chain`, exactly the table's third column; **depth governs rendering only, and `cls` governs behavior**. `name` is `None` on the title row and the three anonymous container rows." Mirror the tuple shape in D4's enumeration at spec.md:162.

### F-2: The claim moved to `<stem>.md.tmp`, but step 4's rationale and the collision guarantee still assume the claim *is* the document
**Severity:** P0
**Where:** spec.md:348 (step 2) vs. spec.md:346 (the preamble), spec.md:350 (step 4) and spec.md:385 (test item 7)
**Convention violated:** internal consistency; and the spec's own stated separation of the two mechanisms at spec.md:346
**Evidence:** v6 rewrote step 2 to claim `<stem>.md.tmp` and step 3 to `os.replace` the rendered temp "onto `<stem>.md`". The claim path and the document path are now **different files**. Step 4, also rewritten in this delta, still argues from the old identity: "a bare `finally` is wrong here, **because once the replace succeeds the claim path *is* the document**, and a `finally` would delete the handoff it just wrote" (spec.md:350). Under step 2 as now written that sentence is false — the claim is a `.tmp` that `os.replace` never touches. Three consequences follow, and the spec does not resolve any of them:

1. **Litter on every success.** Step 4's flag is "cleared the instant `os.replace` returns", so nothing ever removes the claim on the happy path. Every successful CREATE leaves a permanent zero-byte `YYYY-MM-DD-HHMMSS-<slug>.md.tmp` beside the document.
2. **The `.md` name is no longer reserved.** spec.md:346 opens the sequence with "`os.replace` alone is atomic *replacement* — it would clobber an existing document silently, which is the opposite of collision safety", which is precisely what step 2 existed to prevent. With the claim off the `.md` name, a same-second re-run whose predecessor's claim was cleaned up finds `<stem>.md.tmp` free, claims it, and `os.replace`s straight over the earlier `<stem>.md`.
3. **Test item 7's collision assertion now passes only by accident.** spec.md:385 asserts "a same-second collision produces `-2` rather than clobbering". That holds only if the previous run's orphan `.tmp` is still sitting there — i.e. only because of consequence 1. An implementer who cleans up the claim on success (the reading step 4's stale rationale actively discourages, but the obvious hygiene) breaks the test *and* loses a document.

**Suggested fix:** Say which file reserves the name, once. Simplest coherent version keeping both round-5 edge-case fixes: at spec.md:348, "**Claim `<stem>.md.tmp`** … The claim is the name reservation for `<stem>.md`: on `FileExistsError`, *or if `<stem>.md` already exists*, append `-2` … `-9` to the stem." At spec.md:349, end with "…then `os.replace` onto `<stem>.md` and **remove the claim**." At spec.md:350, drop the false rationale and state the real one: "On any exception between the claim and the successful replace, remove both the rendered temp and the claim, then re-raise. On success, remove the claim after the replace — it is a reservation, never the document." Then spec.md:385's collision assertion is satisfied deterministically rather than by leftover litter.

### F-3: "`[TODO…]`-shaped run … is escaped too" has no mechanism, and the escape used two clauses earlier does not defeat `TODO_MARKER_RE`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:353
**Convention violated:** the spec's prescriptive-mechanism discipline everywhere else in this sequence; and D4's rule that the marker matcher is the single authority on the token
**Evidence:** The new clause is appended to the markdown-safety bullet that immediately precedes it: "`|` and backticks escaped before entering a table cell. **Any `[TODO…]`-shaped run in git-derived text is escaped too**". The adjacency makes backslash escaping the obvious reading (and it is what round-5 edge-cases suggested, "a leading `[` … escaped"), but it does not work against the pattern D4 pins at spec.md:164, `re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)`: on `\[TODO\] wire up X` the engine matches `[TODO` at index 1, `\b` holds before the backslash, `[^\]]*` absorbs it, and `\]` closes the match. The escape renders correctly and still trips the gate — reproducing exactly the unclearable-`NEEDS WORK` failure the same bullet-pair is written to prevent, on generated content the author cannot edit away.
**Suggested fix:** Pin the transformation and tie it to the regex: "Any `[TODO…]`-shaped run in git-derived text has its opening bracket rewritten as the entity `&#91;` — a backslash escape renders correctly but leaves the literal `[TODO` in the bytes `TODO_MARKER_RE` scans, so it does not work here. `&#91;TODO] wire up X` displays as written and matches nothing." Add a one-line pin to test item 4 or 7: a commit subject containing `[TODO] x` produces a scaffold that validates `READY` once its own markers are filled.

### F-4: `Files Modified` is told to carry "exactly one" marker and to have its per-file cells filled — the two do not fit the same rendering
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:352 vs. spec.md:380
**Convention violated:** the class table is the single source of truth for marker placement (D4); ambiguity here lands directly on a pinned test assertion
**Evidence:** The v6 parenthetical that resolves round-5 F-1 reads: "(`Files Modified` *is* classed recommended and *does* carry one: git fills its path column, **the author fills the "describe changes / why changed" cells**…)" — plural cells, one per file row, in a table spec.md:353 caps at 10 rows. The same delta's test item 2 asserts "**exactly one `[TODO: …]` per `required`/`recommended` row and none anywhere else**" (spec.md:380). A per-cell rendering — the one the parenthetical describes — emits up to 10 markers in that section and fails the assertion; a single marker line under the heading satisfies the assertion but marks none of the cells it is justifying. `Files Modified` is the only row where a marker shares a section with generated table content, so this is the one place the rule needs saying.
**Suggested fix:** Pin the placement at spec.md:352: "`Files Modified` carries its single marker as a line **beneath the generated table**, not inside a cell — `[TODO: why did each of these change?]` — so the section's count stays one and the generated rows stay untouched." Optionally add to test item 2 that the marker in `Files Modified` is outside the table block.

### F-5: `REQUIRED_SECTIONS` / `RECOMMENDED_SECTIONS` are restated in prose now that the class column is authoritative
**Severity:** P3
**Where:** spec.md:205 against spec.md:207-210
**Convention violated:** single source of truth — the reason `_sections.py` exists at all (D4: "the section table is never restated")
**Evidence:** spec.md:207 now declares "**Every row carries a class, and the class — not the name — drives behavior.**" Two consumers key off class (the renderer and test item 2), but the validator keys off the two name lists (spec.md:367: "each name in `REQUIRED_SECTIONS` present via `has_section` … recommended sections present"). spec.md:205 defines those lists by prose enumeration — `RECOMMENDED_SECTIONS` = "the six marked recommended" — so the same fact is encoded twice inside one module, which is the "one matcher, several places, diverging" shape spec.md:164 invokes as VHS-28's reason for existing. Six is correct today; nothing keeps it correct after a table edit.
**Suggested fix:** One clause at spec.md:205: "`REQUIRED_SECTIONS` and `RECOMMENDED_SECTIONS` are **derived** from the class column — `tuple(n for _, n, c in TEMPLATE_SECTIONS if c == "required")` and the `recommended` equivalent — never written out a second time. They evaluate to `Current State Summary` / `Important Context` / `Immediate Next Steps`, and to the six rows marked recommended."

### F-6: D1's naming freedom is widened in a downstream paragraph without amending D1 or the table caption
**Severity:** P3
**Where:** spec.md:212 against spec.md:87 and spec.md:183
**Convention violated:** prior decisions are amended where they are stated, not silently broadened downstream (spec-level addition with rationale — the (c) class)
**Evidence:** Three different scopes are now on the page. spec.md:87 (D1, untouched): "**Container heading names are not fixed** — never matched or validated, so the implementer chooses them freely." spec.md:183 (untouched): "Container names (**marked `*(container)*`**) are the implementer's choice per D1" — narrower still, only the three anonymous rows. spec.md:212 (new): "the `title`, `container`, `generated` and `chain` rows are rendered from `create_handoff.py`'s own constants, are never matched by any validator check and are never pinned by any test — so an implementer really is free to name them, or to rename `Pending Work`". The v6 statement is the accurate one under the class-keyed rules and I verified nothing pins those headings (item 7 asserts placeholder *text*, item 8 asserts the chain *bullet* format, not its heading) — but it grants naming freedom over `Recent Commits` and `Handoff Chain` that D1 as written does not, and spec.md:183 flatly contradicts it for named container rows.
**Suggested fix:** Amend D1 at spec.md:87 to the class formulation ("every row not classed `required` or `recommended` is rendered from `create_handoff.py`'s constants and never matched — the implementer names them freely"), and cut the parenthetical scoping at spec.md:183 to match.

### F-7: Step 3 cites the four atomic-write precedents for the prefix and drops the rest of their shape
**Severity:** P4
**Where:** spec.md:349
**Convention violated:** the repo's four-instance atomic-write shape, which the same sentence cites by anchor
**Evidence:** All four cited sites do the same four things, verified on disk: `mkstemp(prefix=".…", suffix=".tmp", dir=…)`, then `fh.flush()` + `os.fsync(fh.fileno())` inside the `with`, then `os.replace`, and (three of four) `_fsync_dir(path.parent)` after — `talaria_bridge.py:418-432`, `talaria_watch.py:121-135` and `137-151`, `talaria_read.py:172-186`. spec.md:349 adopts the prefix and the `os.fdopen(fd, "w", encoding="utf-8", newline="\n")` wrapper (byte-for-byte `talaria_watch.py:141`) but stops before the durability half. Handoffs are project working state, so the fsync omission costs little — this is conformance to a precedent the spec itself invokes, not a bug.
**Suggested fix:** Extend step 3: "…in a `with`, **flushing and `os.fsync`ing before the block exits** as all four cited sites do, then `os.replace`."

## Summary
P0: 2 | P1: 0 | P2: 2 | P3: 2 | P4: 1

STATUS: RED P0=2 P1=0 P2=2 P3=2 P4=1
