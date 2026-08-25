# Correctness Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Pinned chain block omits `Previous title` | **CLOSED** | spec:305-310 pins the two-line form incl. `- Previous title: <escaped, ≤80 chars>`, sources it from the previous doc's first `#` heading, re-anchors escaping/truncation and exempts filename+href; test item 8 (spec:336) asserts against that line |
| correctness | F-2 | Metadata exemption region undefined | **CLOSED** (by removal) | spec:207 "No metadata exemption… Nothing is exempt"; spec:317 "nothing exempt"; CREATE remedy at spec:277 |
| correctness | F-3 | Inline-code-span masking unspecified | **CLOSED** (by removal) | spec:20, 133 — masking cut entirely |
| correctness | F-4 | False corpus claim (`### Architecture Overview`) | **CLOSED** | Claim and the fallback it supported are absent from v4 (grep: no occurrence) |
| correctness | F-5 | RESUME assumes a markdown href | **CLOSED** | spec:281 adds the no-href branch (backticked/bare path, `.claude/`-relative rule, note-and-stop) |
| correctness | F-6 | "original" vs "normalized" | **CLOSED** | `grep -n "original"` over the spec returns zero hits; spec:317 reads "normalized" |
| correctness | F-7 | Stale talaria anchors | **CLOSED** | spec:139 `talaria_read.py:23-32` / `talaria_watch.py:33-42`; spec:152 `talaria_bridge.py:4-5` — all three re-verified on disk |
| correctness | F-8 | "the five real documents" | **CLOSED** | spec:127 scopes to `MCP Server/.claude/handoffs/`; spec:385 records the 23-doc corpus |
| edge-cases | F-1 | Subtree fallback has no terminator/API | **CLOSED** (by removal) | spec:179 "No leaf invariant… may nest freely"; spec:133 "No `section_span`" |
| edge-cases | F-2 | Metadata exemption undelimited | **CLOSED** (by removal) | spec:207 |
| edge-cases | F-3 | `--project-path` does not base git cwd | **CLOSED** | spec:298 adds `cwd=<resolved project path>` with the silently-wrong rationale; test item 7 (spec:335) restated |
| edge-cases | F-4 | Collision check undefined; `os.replace` clobbers | **CLOSED** | spec:301 — `open(path,"x")` + `-2`/`-3`, `tempfile.mkstemp`, `finally` cleanup, and the backwards claim corrected |
| edge-cases | F-5 | Inline spans, no pairing/ordering rule | **CLOSED** (by removal) | spec:20 |
| edge-cases | F-6 | Unterminated-fence advisory | **CLOSED** (by removal) | spec:20, 205 (no advisory of any kind remains) |
| edge-cases | F-7 | Redaction prints short credentials | **CLOSED** | spec:211 — fully masked at ≤12 chars; test item 4 (spec:332) pins it |
| edge-cases | F-8 | TODO-in-fence vs 50-char interaction | **CLOSED** | spec:24 records the surviving half as an accepted limit; test item 5 (spec:333) pins it |
| edge-cases | F-9 | `## ` vs `##` empty heading | **CLOSED** | spec:26 |
| conventions | F-1 | Metadata exemption vs D1 | **CLOSED** (by removal) | spec:207 |
| conventions | F-2 | Truncated `importlib` snippet | **CLOSED** | spec:142-149 full six-line loader; spec:154 shared synthetic name + compare-by-value note |
| conventions | F-3 | Region suppression in a secret scanner | **CLOSED** | spec:207 — no suppression exists |
| conventions | F-4 | "structurally prevents" overclaim | **CLOSED** | spec:181 reworded to detects-drift + the § create_handoff.py rule |
| conventions | F-5 | Why `_sections.py` can't import `lint.py` | **CLOSED** | spec:101 |
| conventions | F-6 | README § Skills silence | **CLOSED** | spec:252; verified `README.md:9-11` lists only 3 of 7 |
| conventions | F-7 | Drift roll-up not refreshed | **PARTIAL** | spec:383 refreshed for v4 and flags D0 — but its brief:44 entry quotes text the brief does not contain; see **F-1** below (original severity P3 retained by this lens; F-1 files the substance) |
| conventions | F-8 | Imprecise talaria anchors | **CLOSED** | spec:139, 152 |
| conventions | F-9 | `\r` in `_HEADING_RE` | **CLOSED** | spec:105 regex is `[ \t]*#*[ \t]*$`; spec:97 "No `\r` appears in any matcher" |

No REOPENED items. Every closure the manifest claimed is verifiable on disk; the one gap is conventions/F-7's roll-up content, filed below.

**Grounding notes.** Ticket VHS-28 retrieved (`skills` namespace, record `806902ac`); its description matches the brief with no conflict. `git log -10 -- tests/test_lint.py AGENTS.md`: `tests/test_lint.py` was last touched by `7a3a929` — the current HEAD, landed today — which is the tripwire bump the Preconditions section is built around, so the spec is planning against current code, not shifted code. All other anchors re-verified: `ship-spec/SKILL.md:76`, `lint.py:55/58/60/291`, `sync.py:30/45/81-84`, `talaria_read.py:23-32`, `talaria_watch.py:23/33-42/77`, `talaria_bridge.py:4-5`, `AGENTS.md:54`, `README.md:9-11/30`, `tests/test_lint.py:44-46`, `talaria/SKILL.md:126`, `.gitattributes`, `docs/portability-contract.md` §3 (confirmed: no schema key can declare a package dependency), `skills/hermes-kanban-awareness/reference/` (the only `reference*/` dir in the repo), `origin/main` = `a0ad847` with 5 skill dirs asserting `4`, branch with 7 asserting `7`, 8 commits ahead including `386dc6c`/`8946f58`/`7a3a929`. Corpus claims re-measured: in `MCP Server/.claude/handoffs/` exactly 3 of 5 carry all three required sections at `##` and 2 at `##`/`###`, so D3's "two required sections missing on 60%" is exact.

**On question (a): the scope-down holds.** I grepped the whole spec for `section_span`, `masked`, `subtree`, `leaf invariant`, `score`, `original`, `≥50` — every hit is either in D0's own account of what was removed, or in a "no X" sentence. No surviving check reads section content or section end position. Brief done-when #2 (brief:70) is purely a presence claim ("no section reported `missing`"), and spec test items 2 and 3 satisfy it. The presence half of the gate is sound. The **TODO half is not yet specified well enough to be a gate** — F-3 below.

**On question (b): the narrowing is defensible; the recording is not honest.** F-1.

## Findings

### F-1: § Deferred attributes to brief:44 a quotation the brief does not contain, and the requirement brief:44 actually states — plus the acceptance criterion that pins a test for it — is dropped unnamed while § Done when claims a 1:1 mapping

**Severity:** P1
**Where:** spec.md:383 (§ Deferred), spec.md:361 and spec.md:365 (§ Done when), against `docs/specs/TODO/VHS-28.brief.md:44` and `:71`

**Claim:** spec:383 — "D0's removal of the completeness-length check, which narrows the brief's *"required sections present **and populated**"* (brief:44) to presence-plus-no-placeholder."
spec:361 — "Mapped 1:1 to the brief's acceptance criteria."
spec:365 — "**(brief #3)** `tests/test_session_handoff.py` passes, covering depth-blind matching, the scaffold round-trip, and secret positives…"

**Why this is wrong:** The string "populated" does not occur anywhere in the brief (`grep -n "populated" VHS-28.brief.md` → no matches). brief:44 reads, verbatim:

> `- Preserve the three distinctions the vendor fix was smoke-tested against: level-3 section with real content → passes; genuinely absent section → still `missing`; level-3 section with 5 characters → still `incomplete`.`

That is not a soft "present and populated" phrasing — it is an imperative to **preserve** a named third verdict, `incomplete`. D0 deletes that verdict outright: the D6 table (spec:196-201) has three verdicts and none is `incomplete`. The drift entry paraphrases a weaker obligation than the brief imposes, which is precisely the failure mode the drift roll-up exists to prevent, on the item spec:383 itself nominates as "the one worth a human eye."

It also propagates into the acceptance mapping. brief:71 (done-when #3) is:

> `3. tests/test_session_handoff.py passes, covering the three heading distinctions, a scaffold round-trip, and a secret-pattern positive.`

"The three heading distinctions" is a back-reference to brief:44's three, reinforced by brief:48 ("Cover, at minimum: the three distinctions above"). spec:365 silently substitutes "depth-blind matching" for that phrase and spec:361 calls the result a 1:1 mapping. Test item 1 (spec:329) covers two of the three; the third cannot be written at all under D0. An explicit acceptance criterion is therefore restated rather than mapped, and a reader of § Done when cannot tell that anything was dropped.

Secondarily, spec:364 restates brief done-when #2 as "specified once in `_sections.py`" where brief:70 says "accepts `#` through `######` in **all three places**" (brief:42 names them: required match, terminator scan, recommended match). Collapsing three sites to one is a *stronger* outcome and I do not dispute it — but D0 also removes the terminator scan brief:42 explicitly demands, and the mapping does not say so.

**Suggested fix:** In § Deferred, replace the paraphrase with the brief's own text and the real consequence: "D0's removal of the completeness-length check. brief:44 requires preserving three distinctions, the third being *'level-3 section with 5 characters → still `incomplete`'*; D0 deletes the `incomplete` verdict, so that distinction and the terminator scan brief:42 names are dropped, and brief done-when #3's 'the three heading distinctions' becomes two. Rationale: D0. **This is the item requiring explicit human authorization at the drift-check.**" Then amend spec:365 to map honestly — "(brief #3, **narrowed**) … covering two of brief:44's three distinctions (depth-blind match, genuinely-absent → `missing`); the third (`incomplete`) is removed by D0" — and soften spec:361 from "Mapped 1:1" to "Mapped to the brief's acceptance criteria; #2 and #3 are narrowed by D0 as recorded in § Deferred."

---

### F-2: `TEMPLATE_SECTIONS` as specified cannot render the scaffold, and test item 2's equality assertion is unsatisfiable as written

**Severity:** P1
**Where:** spec.md:156-176 (D4 table), spec.md:296 (§ `create_handoff.py`), spec.md:330 (test item 2), spec.md:181, spec.md:310

**Claim:** spec:330 — "the scaffold's heading sequence **equals** `[name for _, name in TEMPLATE_SECTIONS if name]` in order (drift detection for an inlined table)."
spec:296 — "**Imports `TEMPLATE_SECTIONS` from `_sections` by file path (D4); the section table is never restated in this file.**"

**Why this is wrong:** Three concrete mismatches, each of which alone breaks the equality:

1. **The scaffold has an H1 that is not in the table.** spec:310 requires `Previous title` to be read from "the previous document's first `#` heading" — and the previous document is one this same script produced, so `create_handoff.py` must emit a depth-1 title line. All 23 corpus documents do (`# Handoff: …` at line 1, verified across every `*/.claude/handoffs/*.md`). `TEMPLATE_SECTIONS` (spec:158-176) has no `#` row. The scaffold's heading sequence therefore begins with a title the filtered list does not contain, and the `assertEqual` fails on the first element.
2. **The four unnamed container rows.** spec:165, 168, 171 are `| ## | *(container)* | — |`. The `if name` filter in the assertion only makes sense if those rows carry an empty name — in which case `create_handoff.py` cannot render those `##` headings from the table at all and needs a second, untabled source of container names, which weakens spec:296's "never restated" and spec:181's single-source claim to cover named rows only. If instead the implementer puts real names in those rows, `if name` filters nothing and the scaffold/table can agree — but then spec:85's "Container heading names are **not** fixed" sits against a table that fixes them, and D4 already names two containers itself (`Session Metadata` spec:163, `Pending Work` spec:169). The spec does not say which reading is intended, and the test's correctness depends on the answer.
3. **Body text has no declared home.** `TEMPLATE_SECTIONS` is "an ordered `(depth, name)` table" (spec:156). Rendering a scaffold also needs per-section guidance prose and the `[TODO: …]` markers. spec:323 puts those in `reference/handoff-template.md`, but nothing says `create_handoff.py` reads that file, and D4 says it imports the table from `_sections.py`. So the scaffold's actual content is sourced from a place the spec never names.

**Suggested fix:** (a) Add an explicit `#` title row to `TEMPLATE_SECTIONS` (or state that the H1 is emitted outside the table and is excluded from the assertion). (b) Settle the container question in one sentence in D4 — either "container rows carry `None` as their name; `create_handoff.py` supplies container titles from its own rendering constants, which nothing validates" (and then narrow spec:181's single-source claim to the named rows), or "container names live in the table and D1's 'not fixed' means *not matched by the validator*, not *absent from the schema*." (c) State where per-section guidance and `[TODO: …]` text lives — reading `reference/handoff-template.md` at render time is the option that keeps one source; a constants dict in `create_handoff.py` is fine too, but say which. (d) Restate the assertion so it is satisfiable: "the subsequence of scaffold headings whose titles appear in `TEMPLATE_SECTIONS` equals `[name for _, name in TEMPLATE_SECTIONS if name]` in order."

---

### F-3: The `[TODO: …]` emission rule — now the entire completeness gate — is unspecified, and one plausible reading makes an out-of-repo scaffold permanently un-`READY`

**Severity:** P1
**Where:** spec.md:18 and spec.md:323 (the marker), spec.md:302 (git "Placeholder text"), spec.md:158-176 (generated/fixed-format rows), spec.md:305-310 (pinned chain block), spec.md:330 and spec.md:335 (tests 2 and 7)

**Claim:** spec:18 — "`create_handoff.py` emits a `[TODO: …]` marker in **every section** it scaffolds, so *'did the author replace the placeholder'* already answers completeness."
spec:323 — "**every section** carrying a `[TODO: …]` marker (which is what completeness now rests on)."
spec:302 — "**Placeholder text** distinguishes not-a-repo / no-commits / git-unavailable-or-timed-out."

**Why this is wrong:** D0 promotes the TODO scan from a secondary check to the sole completeness mechanism, but the spec never states which sections carry a marker — and "every section" contradicts three of its own pinned blocks:

- `## Handoff Chain` is pinned to an exact two-line format (spec:305-310) with no room for a marker, and is classed "fixed-format" in the table (spec:175).
- `### Recent Commits` is classed "generated" (spec:159) and is auto-filled from `git log` (spec:302).
- `### Files Modified` (spec:170) is likewise auto-filled from git (spec:302-303), yet is classed "recommended", i.e. indistinguishable in the table from an author-filled section.

Worse, the word "placeholder" now carries two meanings that collide on the gate token. spec:18 and spec:383 use "placeholder" to mean `[TODO: …]`; spec:302 uses "Placeholder text" for the not-a-repo / no-commits / timeout strings, and its shape is not pinned. An implementer who writes the git-failure placeholder as `[TODO: not a git repository]` — the natural reading given spec:18 — produces a scaffold that **can never reach `READY`** outside a repo, because the author has nothing to replace. That is exactly the document test item 7 (spec:335) generates ("`--project-path <tmpdir>` outside any repository asserts the not-a-repo placeholder"), so tests 2 and 7 can be made to disagree by an implementation choice the spec does not constrain.

The gate's *coverage* is also unpinned in the other direction: nothing states that each of the three `REQUIRED_SECTIONS` must carry a marker. If one does not, the completeness gate is silently vacuous for that section, and no test in the plan would notice — test item 2 only replaces whatever markers happen to exist.

**Suggested fix:** Add one bullet to § `create_handoff.py`: "**`[TODO: …]` markers are emitted into exactly the author-filled sections** — every name in `REQUIRED_SECTIONS ∪ RECOMMENDED_SECTIONS`. The generated and fixed-format sections (`Session Metadata`, `Recent Commits`, `Files Modified`, `Handoff Chain`) never carry one; their git-failure strings are plain prose (e.g. `_not a git repository_`) and **must not** use the `[TODO: …]` shape, which is the completeness gate's token." Add to test item 2: "a fresh scaffold contains exactly one `[TODO: …]` per `REQUIRED ∪ RECOMMENDED` name and none elsewhere"; add to test item 7: "the not-a-repo scaffold, with its `[TODO: …]` markers replaced, validates `READY`."

---

### F-4: D0's "Accepted limits" list omits the two coverage holes the removal actually opens — including the one that applies to both legacy fixtures

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:22-26 (D0 § Accepted limits), spec.md:331 (test item 3), spec.md:315-318 (§ `validate_handoff.py`)

**Claim:** spec:22 — "**Accepted limits, recorded deliberately:**" followed by three bullets: TODO-in-a-code-block, a fenced line matching a required name, and the empty-heading whitespace boundary.

**Why this is wrong:** All three listed limits are properties of the *presence* check. The two limits that D0 actually creates — both properties of the *completeness* check it replaced — are absent:

1. **Deleting a placeholder is indistinguishable from filling it.** An author who deletes a `[TODO: …]` line rather than writing under it gets `READY` on an empty required section. Under the removed measurement that was `incomplete`. This is the direct cost of D0 and it is the strongest argument the human drift-check will weigh; it should be on the page next to the decision, not inferable from it.
2. **Any document not produced by this scaffold gets no completeness check whatsoever.** `validate_handoff.py <handoff-file>` (spec:315) takes any path. A hand-written, legacy, or vendor-produced document never contained `[TODO: …]` markers, so the TODO scan matches nothing and the gate degrades to "three headings exist." That is not hypothetical: test item 3 (spec:331) runs the validator on exactly two such documents, and D8 (spec:219) makes reading existing documents a design commitment. spec:18's claim that "the TODO scan was doing the real work all along" is true for generated documents and vacuous for every other input.

Neither is a design error — both are defensible given D0's reasoning — but D0's own framing is "recorded deliberately," and these are the recordings that matter.

**Suggested fix:** Append two bullets to spec:22-26: "— A placeholder that is **deleted** rather than filled reads as complete; an empty required section under a present heading returns `READY`. The removed ≥50-character check caught this; the TODO scan cannot. — A document **not generated by `create_handoff.py`** carries no markers, so completeness reduces to heading presence for it. This is the state of both legacy fixtures (test item 3) and of every document already on disk under D8."

---

### F-5: `_sections.py`'s public surface is stated two different ways, and the normalizer both entry points must call is never named

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:119-133 (D3), spec.md:137 (D4), spec.md:292 (§ Encoding discipline), spec.md:310 (§ `create_handoff.py`), spec.md:317 (§ `validate_handoff.py`)

**Claim:** spec:119 — "`_sections.py` exposes:" followed by `has_section` alone, closed by spec:133 — "That is the whole matcher surface."
spec:137 — "`_sections.py` declares `TEMPLATE_SECTIONS`, `REQUIRED_SECTIONS`, `RECOMMENDED_SECTIONS`, `_HEADING_RE`, **the normalizer**, and `has_section()`."

**Why this is wrong:** Three call sites need more than `has_section`, and the spec does not give them a callable name:

- `has_section(normalized, name)` takes already-normalized text (spec:122), so both entry points must call the normalizer first — spec:292 says "**Reads:** the D3 normalizer" without naming a function.
- spec:310 requires `create_handoff.py` to extract the previous document's first `#` heading title "via `_sections`' matcher on normalized text" — that needs `_HEADING_RE` directly plus the normalizer, and a rule for which heading counts (first depth-1 heading, or first heading of any depth — the spec says "`#` heading", which reads as depth-1, but does not say so).
- spec:133's "that is the whole matcher surface" reads, in isolation, as forbidding exactly the `_HEADING_RE` access spec:310 mandates. A careful reader resolves "matcher surface" ≠ "module surface", which is why this is P2 and not P1.

**Suggested fix:** Give the normalizer a name and a signature in D3 next to `has_section` — e.g. `def normalize(raw: bytes) -> str` (decode `utf-8` `errors="replace"`, strip leading BOM, `\r\n`/`\r` → `\n`) — and amend spec:133 to "No `section_span`, no terminator rule, no masking. The module's whole surface is `normalize`, `has_section`, `_HEADING_RE`, and the three name tables." Add half a sentence at spec:310 fixing the title rule: "the first heading at depth 1".

---

### F-6: `Previous title` has no defined behavior when the predecessor has no depth-1 heading

**Severity:** P3
**Where:** spec.md:310, spec.md:304

**Claim:** spec:310 — "`Previous title` is read from the previous document's first `#` heading via `_sections`' matcher on normalized text."

**Why this is wrong:** spec:304 accepts any `--continues-from` path that resolves inside `<project-path>/.claude/handoffs/` and exists — it does not require the target to be a handoff document this skill generated. A `.md` with no depth-1 heading yields no match and the spec states no fallback: the implementer emits `None`, an empty line, or raises. All 23 documents in the ecosystem corpus do carry an H1 (verified), so this does not bite today, which is why it is P3.

**Suggested fix:** Add to spec:310: "If the previous document has no depth-1 heading, emit the filename in place of the title; never fail the create."

---

### F-7: Two imprecise anchors

**Severity:** P3
**Where:** spec.md:228, spec.md:99

**Claim:** spec:228 — "matching `AGENTS.md:9`'s own 'for Claude Code: `~/.claude/skills/`'". spec:99 — "`lint._read_lines` (`lint.py:64-73`)".

**Why this is wrong:** The quoted AGENTS.md sentence is at **`AGENTS.md:7`** ("Cross-machine agent skills and subagents… (for Claude Code: `~/.claude/skills/` and `~/.claude/agents/`)"); line 9 is the `## Sync commands` heading. `lint.py:64-73` is the *body* of `_read_lines`; the `def` is at line 63, so the citation drops the signature it names. The quoted text and the described behavior are both correct in each case — only the offsets are off.

**Suggested fix:** `AGENTS.md:9` → `AGENTS.md:7`; `lint.py:64-73` → `lint.py:63-73`.

---

### F-8: `slug` is positional-required in one section and optional in another

**Severity:** P4
**Where:** spec.md:277 vs spec.md:296, spec.md:300

**Claim:** spec:277 (SKILL.md § CREATE) — `create_handoff.py <slug> [--continues-from <file>] [--project-path <dir>]`. spec:296 (§ `create_handoff.py`) — `create_handoff.py [slug] [--continues-from FILE] [--project-path PATH]`, with spec:300 "only *then* default to `handoff` if empty".

**Why this is wrong:** `<slug>` and `[slug]` are different argparse declarations (`nargs=None` vs `nargs="?"`), and spec:300's default only makes sense under the second. Trivially resolvable, but the two sections disagree.

**Suggested fix:** Make spec:277 read `create_handoff.py [slug] …` and add "(omitted or empty → `handoff`)".

## Summary
P0: 0 | P1: 3 | P2: 2 | P3: 2 | P4: 1

STATUS: RED P0=0 P1=3 P2=2 P3=2 P4=1
