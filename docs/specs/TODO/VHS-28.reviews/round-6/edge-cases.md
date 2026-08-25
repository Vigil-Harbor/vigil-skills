# Edge-Cases Review — round 6 (delta)

Scoped to the v5→v6 delta (7 hunks) plus untouched text the delta invalidates. Closure covers my own round-5 findings, matching round-5's scoping.

## Closure of round 5 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | `mkstemp` fd still open at `os.replace` (P1) | **CLOSED** | `spec.md:349` now requires `os.fdopen(fd, "w", encoding="utf-8", newline="\n")` in a `with` and states the source-handle rule with the `WinError 32` reproduction |
| edge-cases | F-2 | `try/finally` also fires on success (P2) | **CLOSED** | `spec.md:350` replaces the construct with the condition — "on any exception between the claim and the successful replace", flag cleared the instant `os.replace` returns. *Its rationale clause is now false for a different reason — see F-3* |
| edge-cases | F-3 | Hard kill strands a `.md` claim that RESUME offers (P2) | **CLOSED** | `spec.md:348` claims `<stem>.md.tmp` with `open(claim, "xb")`; RESUME's `*.tmp` exclusion (`spec.md:320`) makes an orphan invisible. **The fix introduces F-1 and F-3 below** |
| edge-cases | F-4 | Template specified as marker-in-every-section (P2) | **CLOSED** | `spec.md:373` now reads "Every `required`/`recommended` section carries a `[TODO: …]` marker and the `title`/`container`/`generated`/`chain` sections carry none — matching § `create_handoff.py` exactly" |
| edge-cases | F-5 | `None`-row rule swept in named containers; "four container rows" miscount (P2) | **CLOSED** | `spec.md:207-212` rewritten to key on **class**, not on name-presence; `spec.md:380` drops the count and uses `cls in ("required", "recommended")`. **Residual: `spec.md:183` still calls the table `(depth, name)` — see F-2** |
| edge-cases | F-6 | Test 8's "authored fixture" is an undeclared third fixture (P2) | **CLOSED** | `spec.md:386` now says the test **writes** the predecessor into the temp handoffs directory, and names both reasons (two declared fixtures; `--continues-from` hard-errors outside the handoffs dir); `spec.md:216` matches |
| edge-cases | F-7 | `first_heading_title` returns `""` for `# ` (P3) | **CLOSED** | `spec.md:143-151` normalizes the empty title to `None` inside the module; `spec.md:360` restates it; `spec.md:386` adds the `# `-H1 test case |
| edge-cases | F-8 | `GIT_*` scrub covered two variables (P3) | **CLOSED** | `spec.md:343` states it as a class — "every inherited `GIT_*` variable removed" — enumerates seven, and keeps the `GIT_INDEX_FILE` rationale |
| edge-cases | F-9 | "bounds what `Previous title` can escape" false for foreign predecessors (P3) | **CLOSED** | `spec.md:214` narrowed to a *generated* document (and the arithmetic corrected 60 → 69, which is right: `len("Handoff: ") + 60`); `spec.md:216` states the unconditional-escape rule; `spec.md:360` settles `\|` — "passes through unescaped: the chain block is a bullet, not a table cell" |
| edge-cases | F-10 | Git-derived text can carry the marker shape, unclearably (P3) | **PARTIAL** | `spec.md:353` adds the rule, but the escape *mechanism* the same sentence establishes does not defeat `TODO_MARKER_RE`, and the chain block is out of its scope. Severity retained at P3 — see F-4 |
| edge-cases | F-11 | Two nits: `D5`→`D3` attribution; `-2` appended to what (P4) | **CLOSED** | `spec.md:214` now reads "D3's `first_heading_title`"; `spec.md:348` now reads "to the filename stem, before the extension". *A residual ambiguity from the new double extension is at F-7* |

**Round-5 P4s the delta was asked about — all three addressed:** temp-file dot-prefix landed (`spec.md:349`, `prefix=".session-handoff."`, and the four cited precedents check out — `talaria_bridge.py:420`, `talaria_watch.py:123,140`, `talaria_read.py:174` all use `mkstemp(prefix=".…", suffix=".tmp", dir=…)`); the unencoded `open(path, "x")` became `open(claim, "xb")` with the reason stated (`spec.md:348`); the container-row miscount is gone (`spec.md:207-212`, `spec.md:380`). None was silently dropped.

**`todo_marker()` / `TODO_MARKER_RE` round-trip — verified, no finding.** `re.compile(r"\[TODO\b[^\]]*\]", re.IGNORECASE)` matches every plausible emission for all nine names (`[TODO: <name>]`, `[TODO: <name> — …]`, and bare `[TODO]`); no `required`/`recommended` name contains `]` or a regex-significant character, and `[^\]]*` crosses newlines, so a multi-line marker still round-trips. The one shape that would break it — a name whose text makes `TODO` word-adjacent, e.g. `[TODOS: …]` — is excluded by the pinned `[TODO: …]` form. The round-trip claim in the `todo_marker` docstring holds. (A related but distinct gap is at F-5.)

## Findings

### F-1: The claim moved to `<stem>.md.tmp` but the replace target stayed `<stem>.md` — collision safety now guards a path nothing is written to, and an existing handoff is silently clobbered
**Severity:** P1
**Where:** spec.md:348 (step 2), spec.md:349 (step 3), against spec.md:346 (the preamble) and spec.md:385 (test 7)
**Edge case:** `<stem>.md` exists and `<stem>.md.tmp` does not — a same-second, same-slug CREATE into a handoffs directory that came from anywhere other than a prior in-place successful run: a `.claude/handoffs/` tracked in git (spec.md:262 explicitly contemplates that `.claude/` may not be gitignored in the target project), a copied or restored directory, a `*.tmp` housekeeping sweep, or a fresh clone.
**What happens:** The exclusive create at step 2 tests `<stem>.md.tmp`, which is absent, so it succeeds and no `-2` suffix is taken. Step 3 then `os.replace`s the rendered scaffold onto `<stem>.md`, destroying the existing handoff with no message and exit `0`. Reproduced:

```
claim on .md.tmp succeeded even though the .md document already exists
document now reads: NEW SCAFFOLD
directory after a 'successful' create: ['2026-08-24-120000-slug.md', '2026-08-24-120000-slug.md.tmp']
```

**Why the spec misses it:** In v5 the claim path and the replace target were the same path, so one `open(..., "x")` bought both properties the preamble names. The round-5 F-3 fix moved the claim to `.md.tmp` to survive a hard kill and left the replace target where it was — but the preamble two lines above is unchanged and still states the invariant this mechanism exists to provide: "`os.replace` alone is atomic *replacement* — it would clobber an existing document silently, which is the opposite of collision safety." Nothing now tests `<stem>.md` for existence at any point. Worse, the design's remaining collision safety is *accidental and depends on litter*: because nothing removes the claim on success (F-3), a repeat CREATE in the same second happens to hit `FileExistsError` on the leftover `.md.tmp` — so test 7's "a same-second collision produces `-2` rather than clobbering" passes for the wrong reason and cannot fail when the real guard is missing. Fixing the litter in F-3 without fixing this silently removes collision safety altogether.
**Suggested fix:** Make the guard test the path that gets written. Step 2: "**Claim by creating both exclusively** — `open(f"{stem}.md", "x")` *and* `open(f"{stem}.md.tmp", "xb")`, closing each immediately; `FileExistsError` on **either** takes the next `-2` … `-9` stem. The `.md` claim is what makes collision safety real (the replace target is `<stem>.md`); the `.md.tmp` claim is what a hard kill leaves behind, and RESUME already ignores it." Alternatively keep the single `.md.tmp` claim and add an explicit `if (handoffs / f"{stem}.md").exists(): take the next suffix` check before the claim — but say so, because the exclusive create is currently the only stated mechanism. Either way, amend test 7 so the collision case is constructed with **only** `<stem>.md` present (no leftover `.tmp`), which is the state that actually exercises the guard.

### F-2: `TEMPLATE_SECTIONS` is still declared a `(depth, name)` table, but three delta sites now destructure three elements
**Severity:** P1
**Where:** spec.md:183, against spec.md:210, spec.md:352, spec.md:380
**Edge case:** The first data structure the implementer writes.
**What happens:** spec.md:183 reads "**`TEMPLATE_SECTIONS`** — an ordered `(depth, name)` table". Built that way, spec.md:210 and spec.md:380's `[name for _, name, cls in TEMPLATE_SECTIONS if cls in ("required", "recommended")]` raises `ValueError: not enough values to unpack (expected 3, got 2)` the moment test item 2 runs, and spec.md:352's marker rule — "markers go into exactly the rows classed `required` or `recommended`" — is unimplementable, because the class the rule keys on does not exist at runtime. Built as a 3-tuple, spec.md:183 is simply wrong about the single source of truth D3/D4 exist to pin.
**Why the spec misses it:** The Class column pre-dates v6 but was documentation-only — three rows carried `—`, and v5's rules keyed on name-presence (`if name`). Hunk 4 fills every row's class *and* promotes the class to the runtime discriminator for both the marker rule and the drift assertion, which makes the arity three. spec.md:183 is the one sentence that states the arity, and it was not touched. This is not the ambiguity of round-5 F-5 (which had a wrong reading and a right one, both of which produced running code); here one reading crashes the suite and cannot express the marker rule at all.
**Suggested fix:** spec.md:183 → "**`TEMPLATE_SECTIONS`** — an ordered `(depth, name, class)` table; **depth governs rendering only**, and `class` — one of `title`, `container`, `generated`, `required`, `recommended`, `chain` — is what the marker rule and the drift assertion key on. `name` is `None` on the title row and on the three anonymous `*(container)*` rows." Drop the trailing "Container names (marked `*(container)*`) are the implementer's choice per D1" from that line, since spec.md:212 now states the freedom more precisely and more broadly.

### F-3: Nothing removes the claim on the success path, and step 4's justification for the flag is false under the new claim path
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:350 (step 4), spec.md:348-349
**Edge case:** The success path of every CREATE.
**What happens:** Step 4 scopes cleanup to "any exception between the claim and the successful replace". `os.replace` moves the *mkstemp* temp onto `<stem>.md`; the claim `<stem>.md.tmp` is never mentioned again, so a zero-byte `.md.tmp` accumulates in `.claude/handoffs/` — one per handoff, forever, in every project. Reproduced above: the directory after a successful create holds both `2026-08-24-120000-slug.md` and `2026-08-24-120000-slug.md.tmp`. RESUME ignores `*.tmp` so it is invisible rather than harmful, but where the target project tracks `.claude/` (spec.md:262) the litter is committed, and F-1 shows the collision guard is silently leaning on it.
Compounding it, step 4's rationale — "once the replace succeeds the claim path *is* the document, and a `finally` would delete the handoff it just wrote" — was written for the v5 world where the claim was `<stem>.md`. Under v6 the claim path is `<stem>.md.tmp`, and after a successful replace it is **not** the document; it is an empty file. The sentence that explains why the mechanism must be a flag is now factually wrong about its own mechanism, which is exactly the kind of stale premise an implementer reasons forward from.
**Why the spec misses it:** Hunks 5 and 6 landed round-5 F-2 and F-3 independently. F-2 rewrote step 4 in v5's terms; F-3 changed what step 4's terms refer to. Neither pass re-read the other's rationale, and test 7's byte-identical assertion covers only the *failure* path, so no test observes the success path's residue.
**Suggested fix:** Step 4 → "**Remove the claim once the replace returns** — on success as well as on failure; under v6 the claim is `<stem>.md.tmp` and after the replace it is an empty leftover, not the document. On **any exception** between the claim and the successful replace, remove both the mkstemp temp and the claim, then re-raise. Track the claim in a flag so cleanup is ordered after the replace, never a bare `finally` around a path that may already be the document." Add to test 7: after a *successful* create the handoffs directory contains exactly one file. (Sequence this against F-1 — removing the claim on success is only safe once the collision guard tests `<stem>.md`.)

### F-4: The new "escape `[TODO…]`-shaped runs" rule does not work under the escape mechanism its own sentence establishes, and does not cover the chain block
**Severity:** P3 *(round-5 F-10 retained at its original severity — PARTIAL, not closed)*
**Where:** spec.md:353, spec.md:360, spec.md:164
**Edge case:** (a) a commit subject or modified path containing `[TODO] …`; (b) `--continues-from` a hand-authored predecessor whose H1 contains a `[TODO: …]` run.
**What happens:** (a) The clause reads "Any `[TODO…]`-shaped run in git-derived text is escaped too", in the same sentence that defines escaping for `|` and backticks — i.e. backslash escaping. Backslash escaping does not defeat `\[TODO\b[^\]]*\]`, because the regex never looks at what precedes the `[`. Measured against the pinned pattern:

```
raw commit subject           -> MATCHES (trips gate)   [TODO] wire up X
backslash-escaped brackets   -> MATCHES (trips gate)   \[TODO\] wire up X
backslash on open only       -> MATCHES (trips gate)   \[TODO] wire up X
backtick-wrapped             -> MATCHES (trips gate)   `[TODO] wire up X`
html entity open bracket     -> no match (safe)        &#91;TODO] wire up X
zero-width inserted          -> no match (safe)        [<U+200B>TODO] wire up X
space inserted               -> no match (safe)        [ TODO] wire up X
```

So the guard added this round leaves the failure it names in place: a repo with that commit convention produces handoffs stuck at `NEEDS WORK` that the author can only clear by hand-editing generated content, reproduced on every subsequent CREATE.
(b) The rule is scoped to *git-derived* text. `Previous title` at spec.md:360 is derived from the **predecessor's H1**, escapes backticks only, and passes `|` through deliberately — nothing neutralizes a `[TODO: …]` run there. A hand-authored predecessor titled `# [TODO] migrate auth` writes an unclearable marker into the new document's `Handoff Chain` block, which is class `chain` and carries no marker of its own, so the only way to reach `READY` is to delete the provenance line. Test 8 already builds a hand-written predecessor with a deliberately exotic H1; this is one character away from it.
**Why the spec misses it:** The clause states the right requirement and borrows a verb ("escaped") whose established meaning in that sentence is the wrong mechanism; and it was written against the git path round-5 F-10 raised, without asking what else can carry foreign text into the document.
**Suggested fix:** Say what neutralization means and widen the scope: "**Any `[TODO…]`-shaped run in text the tool did not author — git subjects and paths, and the `Previous title` drawn from a predecessor's H1 — is neutralized so `TODO_MARKER_RE` cannot match it.** Markdown backslash-escaping does **not** do this (`\[TODO\]` still matches `\[TODO\b[^\]]*\]`); break the token itself, e.g. render the opening bracket as `&#91;`. Pin it: assert `TODO_MARKER_RE.search(render(...)) is None` for a commit subject `[TODO] wire up X` and for a predecessor H1 `# [TODO] migrate auth`." Add that assertion to test 7 (git path) and test 8 (chain path), since nothing today would catch either.

### F-5: `todo_marker()`'s output shape is unspecified, and test item 2's per-row assertion cannot be written without it
**Severity:** P3
**Where:** spec.md:153-155 (D3), spec.md:380 (test 2)
**Edge case:** Writing the assertion that makes the completeness gate non-vacuous.
**What happens:** spec.md:153-155 says only that `todo_marker(name)` returns "the `[TODO: ...]` text for a section" and that `TODO_MARKER_RE` matches what it emits. Test 2 asserts "exactly one `[TODO: …]` per `required`/`recommended` row and none anywhere else". "Per row" requires mapping each marker back to its section — and D0 deliberately removed every mechanism for locating text under a heading (no `section_span`, no terminator rule), so the only way to write it is `todo_marker(name) in text` for each of the nine, which is well-defined **only if the returned string embeds `name` verbatim**. Nothing pins that. An implementer who returns a constant `"[TODO: fill this in]"` for every section satisfies the docstring, and the strongest available assertion collapses to "there are nine markers" — which no longer distinguishes nine markers in the right nine sections from nine in one.
**Why the spec misses it:** `todo_marker` was introduced as a *renderer* to kill the duplicated string; the test that consumes it was rewritten in the same round to key on class. The contract between them — that the marker is identifiable per section — was never stated.
**Suggested fix:** Pin the shape in the docstring: "Returns `f\"[TODO: {name} — …guidance…]\"`; the section name appears verbatim, so `todo_marker(name) in text` is how test item 2 locates a section's marker without any sectioning (D0)." And make test 2 explicit: "for each of the nine names, `todo_marker(name)` occurs exactly once, and `len(TODO_MARKER_RE.findall(text)) == 9`."

### F-6: Only one of the three git-failure placeholders is pinned as non-marker-shaped
**Severity:** P3
**Where:** spec.md:385 (test 7), against spec.md:351-352
**Edge case:** `git log` times out at the 10-second bound in a large repo, or the repo has no commits — both named at spec.md:351.
**What happens:** spec.md:352 requires all three placeholders (not-a-repo / no-commits / git-unavailable-or-timed-out) to be plain prose and forbids the marker shape, with the consequence spelled out: an accidentally marker-shaped placeholder makes those CREATEs permanently un-`READY` with nothing for the author to replace. Test 7 pins exactly one of the three — "the not-a-repo scaffold, with its markers replaced, validates `READY` (proving the git placeholder is not marker-shaped)". The timeout string is the one an implementer is most likely to phrase as an instruction to the reader, and it is also the hardest of the three to reach end-to-end, so it is the one that will ship unpinned.
**Why the spec misses it:** The assertion was attached to a scenario that already existed in test 7 for the `cwd=` fix; the other two placeholders have no scenario of their own.
**Suggested fix:** Make it a direct unit assertion rather than an end-to-end one — it needs no repository: "assert that **each** of the three git-failure placeholder strings the module defines is rejected by `TODO_MARKER_RE`, and that each renders as italic prose." That pins all three at once and does not depend on provoking a timeout.

### F-7: Two nits in new text
**Severity:** P4
**Where:** spec.md:348, spec.md:360
**What happens:** (a) spec.md:348's "append `-2` … `-9` **to the filename stem, before the extension**" was unambiguous when the claim was `<stem>.md`; the claim is now `<stem>.md.tmp`, which has two extensions, so "the extension" admits both `<stem>-2.md.tmp` and `<stem>.md-2.tmp`. Only the first is meant — the suffix has to land on the stem the `.md` document inherits. (b) spec.md:360 requires the title "escaped and truncated to 80 characters with an ellipsis" without fixing the order. Escape-then-truncate can cut a `` \` `` pair at the boundary; truncate-then-escape can exceed the 80 the pinned format states and test 8 asserts against.
**Suggested fix:** (a) "append `-2` … `-9` to the timestamp-and-slug stem — `<stem>-2.md` / `<stem>-2.md.tmp`, never after `.md`". (b) "truncate the raw title to 80 characters (ellipsis included), **then** escape — the escaped form may exceed 80; the 80 bounds the title, not the rendered line."

## Summary
P0: 0 | P1: 2 | P2: 1 | P3: 3 | P4: 1

STATUS: RED P0=0 P1=2 P2=1 P3=3 P4=1
