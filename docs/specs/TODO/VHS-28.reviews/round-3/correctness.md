# Correctness Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `_HEADING_RE` captures CRLF `\r` | **CLOSED** | spec:83-86 normalizer; spec:91 `[ \t\r]` class; spec:107 `.strip()`; spec:301 `newline="\n"`; spec:344 test 7. Corpus claim verified: `MCP Server/.claude/handoffs/2026-08-15-060410-mcp-45-post-merge.md` is CRLF and all three required sections are `##` (lines 27/143/207) |
| correctness | F-2 | own content measured on masked copy | **CLOSED** | spec:113 length-preserving masking; spec:140 `len(original[start:end].strip())`; spec:339 test 2 |
| correctness | F-3 | thematic break left as prose | **CLOSED** | spec:95-98 `_THEMATIC_BREAK_RE`; spec:111 unconditional |
| correctness | F-4 | setext bullet contradicts terminator | **CLOSED** | spec:108 |
| correctness | F-5 | fence pairing / `lint.py` mischaracterized | **CLOSED** | spec:115-116. Verified `lint.py:55` `_FENCE_RE`, `lint.py:211-213` unconditional toggle |
| correctness | F-6 | no `main(argv) -> int` contract | **CLOSED** | spec:307, 324, 336 |
| correctness | F-7 | `create_handoff.py` omits `_sections` import; `sys.path` | **CLOSED** | spec:307, 147-155. Verified `talaria_read.py:23-32` implements exactly this |
| correctness | F-8 | `TEMPLATE_SECTIONS` never enumerated | **CLOSED** | spec:159-179. Leaf invariant re-walked below — holds for all 9 required/recommended names; `REQUIRED`=3, `RECOMMENDED`=6, D1's "nine names" consistent |
| correctness | F-9 | bounded read names wrong end | **CLOSED** | spec:193 "discard the first line" |
| correctness | F-10 | stale `lint.py:52` | **CLOSED** | spec:191 now `lint.py:60`; verified `_CASE2_TAG` is at `lint.py:60` |
| correctness | F-11 | D12 AGENTS.md claim inaccurate | **CLOSED** | spec:262; verified `AGENTS.md:54` is the `spec-close` row |
| correctness | F-12 | "before or alongside" reopens scope | **CLOSED** | spec:390 "resolved *before* this work" |
| edge-cases | F-1 | CRLF | **CLOSED** | as correctness/F-1 |
| edge-cases | F-2 | masked-copy measurement | **CLOSED** | as correctness/F-2 |
| edge-cases | F-3 | fixture pins minority shape | **CLOSED** | spec:37-38 two fixtures; spec:157 name-only. Verified 3 flat / 2 nested across the MCP Server five |
| edge-cases | F-4 | unterminated / nested fence | **CLOSED** | spec:115-116 |
| edge-cases | F-5 | three-literal-char break; setext | **CLOSED** | spec:95-98, 108 |
| edge-cases | F-6 | "blanked" undefined, offsets shift | **CLOSED** | spec:113 |
| edge-cases | F-7 | `.claude/handoffs/` never created | **CLOSED** | spec:310 |
| edge-cases | F-8 | `Continues from` representation unspecified | **PARTIAL** | spec:315-318 pins the link line but omits the `Previous title:` sub-line the corpus actually carries — see F-1 below (severity raised: the pinned block now contradicts its own escaping rule) |
| edge-cases | F-9 | RESUME empty directory | **CLOSED** | spec:289 |
| edge-cases | F-10 | `BLOCKED` on auto-generated metadata | **PARTIAL** | spec:217 declares the exemption but never defines the exempt region — see F-2 below |
| edge-cases | F-11 | Preconditions two paths | **CLOSED** | spec:10-23. Verified: `origin/main` = `a0ad847`, 5 skill dirs, `tests/test_lint.py:52` asserts `4`; branch has 7 dirs and asserts `7`, 8 commits ahead |
| edge-cases | F-12 | leaf invariant only vs scaffold | **CLOSED** (rationale wrong) | spec:183 adds the subtree fallback; its supporting corpus claim is false — see F-4 |
| edge-cases | F-13 | inline code spans unmasked | **PARTIAL** | spec:117 adds masking but leaves span pairing wholly unspecified — see F-3 |
| edge-cases | F-14 | `sys.path` persistence / `__pycache__` | **CLOSED** | spec:150-155, 51, 396 |
| edge-cases | F-15 | chain cycle keys on filenames | **CLOSED** | spec:291 `resolve()`d, case-insensitive |
| edge-cases | F-16 | two CommonMark divergences | **CLOSED** | spec:109 |
| conventions | F-1 | `sys.path` vs precedent | **CLOSED** | spec:147-155 |
| conventions | F-2 | asymmetric `_sections` import | **CLOSED** | spec:307 |
| conventions | F-3 | `lint.py` citations / stale anchor | **CLOSED** | spec:85, 115, 191 — all three re-verified |
| conventions | F-4 | uninstall command POSIX-only | **CLOSED** | spec:236 dual-shell, harness-qualified |
| conventions | F-5 | fixture lands flat | **CLOSED** | spec:40; verified `tests/fixtures/` is a pure lint corpus and root `.gitattributes` carries `*.md text eol=lf` |
| conventions | F-6 | bare `python` | **CLOSED** | spec:363 |
| conventions | F-7 | unauthorized additions roll-up | **CLOSED** | spec:394 (deferred, recorded) |
| conventions | F-8 | D12 rationale partly inaccurate | **CLOSED** | spec:262 |

## Findings

### F-1: The "pinned" chain-block format omits the `Previous title:` line that the very next bullet, the RESUME step, and test-plan item 9 all depend on

**Severity:** P0
**Where:** `docs/specs/TODO/VHS-28.spec.md:315-318` (§ `scripts/create_handoff.py`), cross-referenced at `:291` (§ SKILL.md, RESUME) and `:346` (test plan item 9)

**Claim:** spec:315-318 —

> **The chain block is a pinned format**, because RESUME parses it and the existing corpus already uses it:
> - `- **Continues from**: [<filename>](./<filename>)`
> - `- **Continues from**: None (fresh start)` …
> - Escaping and the 80-character truncation apply **only to the previous document's displayed title, never to the filename or the href.**

**Why this is wrong:** The pinned block has no title field at all — both link-text and href are `<filename>`. So the escaping/truncation bullet governs a field the format does not emit, and there is nothing for RESUME's parenthetical at spec:291 ("resolved relative to the handoffs directory, **not the displayed title**") to disambiguate against. Test-plan item 9 (spec:346) then asserts a case that is vacuous under the pinned format: "assert the emitted line matches the pinned format exactly … including when A's title contains `|`, backticks, and 200 characters" — A's title never appears in `[<filename>](./<filename>)`.

The on-disk corpus the spec says it is pinning to carries the title on a **separate continuation line** that the spec's block drops:

```
- **Continues from**: [2026-08-23-031109-mcp-49-50-53-54-high-priority-sprint.md](./2026-08-23-031109-mcp-49-50-53-54-high-priority-sprint.md)
  - Previous title: MCP-49/50/53/54 shipped — the high-priority board is clear; five PRs merged, wiki corruption fixed and repaired
- **Supersedes**: None
```

(`C:/Users/zioni/Documents/Vigil-Harbor/MCP Server/.claude/handoffs/2026-08-23-154211-mcp-51-spec-cycle-5-rounds.md:18-20`; same shape at `petland/.claude/handoffs/2026-08-11-020232-clt-91-closed-compliance-reconciled.md:18-19`.)

An implementer follows the code block, emits no title line, and test 9's title cases cannot be written. Related: spec:313 says `|` and backticks are "escaped before entering a table cell", but the title's actual home is a bullet continuation line, where `|` needs no escaping — so the escaping rule is also attached to the wrong construct.

**Suggested fix:** Extend the pinned block to the two-line form the corpus uses, and re-anchor the escaping rule to it:

```
- **Continues from**: [<filename>](./<filename>)
  - Previous title: <escaped, ≤80 chars>
- **Continues from**: None (fresh start)      # flag not passed at all
```

State that `Previous title` is read from the previous document's first `#` heading (via `_sections`' `_HEADING_RE` on the normalized text), that backticks are escaped and the title truncated to 80 characters with an ellipsis, and that the filename and href are never escaped or truncated. Then test 9's `|`/backtick/200-char case asserts against the `Previous title` line.

---

### F-2: D6's `BLOCKED` metadata exemption has no defined region, and `validate_handoff.py` cannot know which lines were auto-generated — test-plan item 6 pins an outcome that depends on the missing definition

**Severity:** P1
**Where:** spec:217 (D6), spec:326 (§ `scripts/validate_handoff.py`), spec:343 (test plan item 6), spec:159-177 (D4 `TEMPLATE_SECTIONS`)

**Claim:** spec:217 — "**the generic assignment class is not applied to the auto-generated metadata block**"; spec:326 — "secret scan (D1's list, unmasked, with D6's metadata-block exemption for the generic class)"; spec:343 — "**a scaffold whose HEAD commit subject contains `client_secret = <20 chars>` is not `BLOCKED`** (D6's metadata exemption), while the same string in authored body text is."

**Why this is wrong:** `validate_handoff.py <handoff-file>` receives only a file path (spec:324). It has no record of what `create_handoff.py` generated, so "the auto-generated metadata block" is not a property it can observe — it must use a structural proxy, and the spec names none. Worse, the two obvious proxies give different answers on exactly the motivating case:

- If the proxy is `section_span(masked, "Session Metadata")`, the commit list is **outside** it. Every document in the corpus nests commits one level deeper — `## Session Metadata` (line 3) → `### Recent Commits (for context)` (line 9) → `## Handoff Chain` (line 16) in `MCP Server/.claude/handoffs/2026-08-15-060410-mcp-45-post-merge.md`, and identically in all five. Since `section_span`'s `end` is "the next heading at ANY depth" (spec:128), `### Recent Commits` terminates the `Session Metadata` span, so the commit subject is *not* exempt and test 6 fails.
- If the proxy is "everything before the first required section", the exemption silently covers `## Handoff Chain` too.

D4's now-enumerated `TEMPLATE_SECTIONS` (spec:161-177) makes this sharper rather than softer: it has **no row for the commit list at all**, and `Files Modified` — which spec:312-313 says is auto-filled from `git` with paths in a table — is listed as an ordinary `###` **recommended** section, indistinguishable from authored content. So the spec's own single-source table does not tell the implementer where the auto-generated region begins or ends.

**Suggested fix:** Define the exempt region structurally in D3/D4 rather than by provenance. Concretely: add the commit list to `TEMPLATE_SECTIONS` as an explicit row (e.g. `###` under `Session Metadata`), and state in D6 that the generic-assignment class is skipped for the union of the `Session Metadata` subtree (its own span plus every deeper heading up to the next `##`) and the `Handoff Chain` span — naming "subtree", not "span", since `section_span` stops at the first child heading. Then restate test-plan item 6 in those terms ("a commit subject inside the Session Metadata subtree is exempt; the same string under `## Important Context` is not"), so the assertion is decidable from the spec.

---

### F-3: Inline-code-span masking is asserted but never specified — the one masker D3 leaves open on the axes it closes for fences

**Severity:** P2
**Where:** spec:113-118 (D3, § Fence masking, length-preserving)

**Claim:** spec:117 — "**Inline code spans are masked too**, so a handoff whose next step is literally 'remove the `[TODO: wire up auth]` marker' can still reach `READY`."

**Why this is wrong:** D3's stated thesis is that leaving *any* matcher axis unpinned is what produced the bug ("The vendor built its heading pattern in three places and they diverged on **two** axes … So every matcher is specified completely, once", spec:81). For fences the spec now pins the delimiter character, the minimum length, the same-character-and-at-least-as-long closer rule, the trailing-whitespace rule, and an explicit unterminated-opener rule with an advisory finding (spec:115-116). For inline spans it pins nothing:

- Whether a span may cross a newline. CommonMark says it may. A multiline `` `[^`]*` `` masker with an odd backtick count in one region will blank a heading between two distant backticks — the section then reports `missing` on a visibly present heading, the exact symptom class VHS-28 was filed for and brief done-when #2 forbids. A line-bounded `` `[^`\n]*` `` cannot.
- What an unterminated span does (fences get an explicit rule; spans get none).
- Whether spans use CommonMark's variable-length backtick-run pairing (`` `` a ` b `` `` is one span).
- Ordering relative to fence masking. If spans are masked first, a ` ``` ` fence delimiter's own backticks are seen as span delimiters.

I probed all 23 handoff documents on disk (`C:/Users/zioni/Documents/Vigil-Harbor/*/.claude/handoffs/*.md`): every one has an even non-fence backtick count, and none has an odd running count at a required heading — so this does not break today's corpus, which is why it is P2 and not P1. It is a latent reintroduction of the defect class on arbitrary input.

**Suggested fix:** Add one bullet under § Fence masking: "**Inline spans are line-bounded and non-nesting**: a span opens and closes on the same line, delimited by a run of N backticks closed by the next run of exactly N; an unclosed run on a line masks nothing on that line. Spans are masked **after** fenced regions, so fence delimiters never register as span delimiters." Add a test to item 2: a line carrying a single unpaired backtick before a required heading does not cause that heading to report `missing`.

---

### F-4: D4's justification for the nesting fallback misdescribes both nested documents — `### Architecture Overview` sits under a container, not under `## Current State Summary`

**Severity:** P2
**Where:** spec:183 (D4, "Arbitrary documents may nest, and that is not an error")

**Claim:** spec:183 — "Two of the five real documents already put `### Architecture Overview` directly under `## Current State Summary`."

**Why this is wrong:** Neither does. In both nested documents `### Architecture Overview` is the first child of a `## Codebase Understanding` container, and `## Current State Summary` is a `##` sibling several sections earlier with real prose of its own:

- `MCP Server/.claude/handoffs/2026-08-23-031109-mcp-49-50-53-54-high-priority-sprint.md` — `## Current State Summary` line 24, `## Codebase Understanding` line 32, `### Architecture Overview` line 34.
- `MCP Server/.claude/handoffs/2026-08-23-154211-mcp-51-spec-cycle-5-rounds.md` — line 24, line 41, line 43 respectively.

In both, `Current State Summary`'s span (lines 25-31 / 25-40) holds ordinary prose, so under D3's own rules it is a leaf with non-empty own content and the subtree fallback never fires. No document in the corpus — I checked all 23, across seven projects — makes a `REQUIRED ∪ RECOMMENDED` name a container. The fallback behavior itself is fine and is pinned by test-plan item 5 (spec:342), so this is a false supporting claim rather than a design error; but it is the only evidence offered for adding the fallback, and a future reader auditing the decision will not be able to reproduce it.

**Suggested fix:** Replace the sentence with what the corpus actually shows — "The corpus keeps every required name a leaf today, but nothing enforces that on inputs we do not generate (two of the five already nest `###` sections under `##` containers such as `Codebase Understanding`), so the fallback is defensive rather than corpus-driven" — and keep test item 5's synthetic subtree case, which is now the only thing pinning it.

---

### F-5: RESUME's chain-following assumes a markdown href; two on-disk documents record the predecessor as a bare backticked path with no link

**Severity:** P2
**Where:** spec:291 (§ SKILL.md, RESUME), spec:315 (§ `create_handoff.py`), spec:225 (D8)

**Claim:** spec:291 — "Read fully, **following the `Continues from` href** (resolved relative to the handoffs directory, not the displayed title)"; spec:315 — the format is pinned "because RESUME parses it and **the existing corpus already uses it**"; D8 (spec:225) — "Existing documents stay readable and listable".

**Why this is wrong:** The corpus is not uniform on this line. Of the documents that actually chain, ten use the `[file](./file)` link form, but two do not:

- `Primer/.claude/handoffs/2026-08-06-192609-pri4-royal-ink-shipped.md:21` — ``- **Continues from**: `.claude/handoffs/2026-08-05-181523-hub-completion-qa-night.md` (hub completion + QA night)``
- `Zoho inventory/.claude/handoffs/2026-08-22-infuzd-capability-menu-and-pricing.md:6` — ``- Continues from: `.claude/handoffs/2026-08-21-202109-infuzd-zoho-discovery-complete.md``` (no bold, outside a `Handoff Chain` heading)

Three more record `None` in prose forms the spec's two pinned `None` variants do not cover (`**None — this is a new thread.**`, `None. The scaffold auto-linked …`). An agent told to "follow the href" finds none in these documents and has no stated behavior; it will either stop silently or guess. Chain-following is not itself a Done-when, which is why this is P2 — but the spec asserts the corpus uses the pinned format, and it partially does not.

**Suggested fix:** Add one clause to RESUME: "if the line carries no markdown href, take the first backticked or bare path on the line and resolve it the same way (relative to the handoffs directory when it is bare, relative to `<project-path>` when it begins `.claude/`); if neither yields an existing file, note it and stop the chain rather than guessing." Soften spec:315 to "the majority of the existing corpus already uses it".

---

### F-6: "the original" is used for two different strings across D3, § Encoding discipline, and § `validate_handoff.py`

**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:83, spec:124, spec:140, spec:113, spec:326

**Claim:** spec:124 — "Return (start, end) into the **normalized text**"; spec:140 — "it is measured on the ***original***. `len(original[start:end].strip())`"; spec:113 — "Offsets … are therefore identical between the masked copy and **the original**"; spec:326 — "≥50 characters of own content **measured on the original** (D3 consequence 2)".

**Why this is wrong:** "Original" carries two possible referents — the raw decoded bytes, or the normalized-but-unmasked text — and the spec never defines it. The three sections were edited separately and the terminology did not converge: `section_span`'s docstring says spans index the *normalized* text, while the two consumers that slice with those spans say *original*. An implementer who reads "original" as pre-normalization applies normalized offsets to a longer CRLF string, and the resulting slice is misaligned by one character per preceding line — a wrong length measurement on exactly the CRLF documents D3 was rewritten to fix (`2026-08-15-060410-mcp-45-post-merge.md` has 143 lines before `## Immediate Next Steps`, so the slice would be off by 143 bytes). spec:83 does say "All matching, span arithmetic, offsets, and length measurement operate on a normalized string", so a careful reader unravels it — hence P2, not P1.

**Suggested fix:** Introduce two named terms once in D3, immediately after the normalization paragraph — `normalized` (decoded, BOM-stripped, LF-only) and `masked` (the length-preserving copy of `normalized`) — retire the word "original" throughout, and rewrite consequence 2 as `len(normalized[start:end].strip())` and spec:326 as "measured on `normalized`".

---

### F-7: Two stale anchors into `skills/talaria/scripts/`

**Severity:** P3
**Where:** spec:155 (D4)

**Claim:** "`skills/talaria/scripts/talaria_bridge.py:3-4` states the choice explicitly … and both consumers (`talaria_read.py:23-32`, `talaria_watch.py:35-45`) implement exactly this pattern."

**Why this is wrong:** `talaria_read.py:23-32` is exact (`def _load_bridge` at line 23, `return module` at 32). The other two are off:
- `talaria_bridge.py` — the sentence "This file deliberately avoids HTTP and ``sys.path`` mutation" spans **lines 4-5**, not 3-4 (line 3 is blank).
- `talaria_watch.py` — `def _load_bridge` is at **line 33**, ending at 42, not 35-45. (`talaria_watch.py:23,77`, cited at spec:196 for the `_WATCH_ID_RE`/`fullmatch` pair, is exact.)

**Suggested fix:** `talaria_bridge.py:4-5` and `talaria_watch.py:33-42`.

---

### F-8: "the five real documents" is one project's directory; the handoff corpus is 23 documents across seven projects

**Severity:** P3
**Where:** spec:85, spec:111, spec:157, spec:183, spec:342

**Claim:** spec:157 — "measured across the five real documents, three are fully flattened to `##` and two use `##`/`###`"; spec:37-38 — the two fixtures are labelled "3 of 5 real documents" and "2 of 5 real documents".

**Why this is wrong:** The five are `C:/Users/zioni/Documents/Vigil-Harbor/MCP Server/.claude/handoffs/`. Ecosystem-wide there are 23 handoff documents in seven `*/.claude/handoffs/` directories (Dynasty 1, MCP Server 5, Petasos 2, Primer 5, Zoho inventory 2, petland 7, vigil-harbor-wiki 1). Every measured property the spec derives from "the five" checks out for that directory — 3 flat / 2 nested is exact; `2026-08-15-060410-mcp-45-post-merge.md` is the only CRLF file and all three of its required sections are `##`; trailing content after the last heading is 590-877 chars against the quoted "588–875". But the wider corpus is what the fixtures claim coverage of, and it contains shapes the five do not (F-5's two link-less chain lines; a document whose last heading is `## Recommended next-session opener`; one whose last heading is `### Verify reports on disk`). Naming the sample keeps a later reader from over-reading the fixtures' representativeness.

**Suggested fix:** Write "the five documents in `MCP Server/.claude/handoffs/`" at spec:85/111/157/183 and in the § New files fixture rows, and note that the wider ecosystem corpus is 23 documents whose additional shapes are handled by the name-only rule rather than by fixture.

## Summary
P0: 1 | P1: 1 | P2: 4 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=1 P2=4 P3=2 P4=0
