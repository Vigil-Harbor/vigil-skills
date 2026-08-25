# Conventions Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | D6 metadata exemption has no defined region | **CLOSED** | spec:207 "**Nothing is exempt.**"; the exempt-region concept is gone from D6 and from § `validate_handoff.py` (spec:317 "nothing exempt") |
| conventions | F-2 | truncated `importlib` snippet / naming divergence | **CLOSED** | spec:141-150 is the full six-line loader; spec:154 records the shared synthetic name as a deliberate divergence from talaria's per-consumer names and pins by-value comparison. Verified against `talaria_read.py:23-32` and `talaria_watch.py:33-42` |
| conventions | F-3 | region-scoped suppression vs advisory precedent | **CLOSED** | resolved by removal — no suppression remains to demote (spec:207) |
| conventions | F-4 | leaf-invariant test claimed to *prevent* inlining | **CLOSED** | spec:179-181; the invariant is gone and prevention is now attributed to the never-restate rule, not a test. (Its replacement sentence cites the wrong test number — filed as F-2 below, not a reopen) |
| conventions | F-5 | D3 reimplements `lint.py` shapes without saying why | **CLOSED** | spec:101; verified `sync.py` `SUBTREES = ("skills","agents")`, so `lint.py` is genuinely absent beside an installed skill |
| conventions | F-6 | D12 silent on `README.md` § Skills | **CLOSED** | spec:252; verified `README.md:9-11` lists 3 skills against 7 tracked `skills/*/SKILL.md` |
| conventions | F-7 | drift roll-up not refreshed | **CLOSED** (see F-1) | spec:383 refreshed and names D0 for the human check — but one of its four citations is inaccurate |
| conventions | F-8 | imprecise talaria anchors | **CLOSED** | `talaria_bridge.py:4` carries the `sys.path` sentence; `talaria_watch.py:33-42` is the loader; `talaria_watch.py:23` is `_WATCH_ID_RE` |
| conventions | F-9 | `\r` still in the matcher | **CLOSED** | spec:105 regex is `[ \t]`-only; spec:97 states normalization as a precondition |
| correctness | F-1 | chain block omits `Previous title:` | **CLOSED** | spec:305-310 pins both lines |
| correctness | F-2 | metadata exemption unimplementable | **CLOSED** | spec:207 |
| correctness | F-3 | inline-span masking unspecified | **CLOSED** | removed (spec:20, 373) |
| correctness | F-4 | nesting-fallback justification misdescribes the corpus | **CLOSED** | fallback removed; replacement claim at spec:127-130 **independently verified** — `MCP Server/.claude/handoffs/` is exactly 3 all-`##` and 2 `##`/`###`, so a `(depth,name)` key drops 2 required sections on 60% of the corpus |
| correctness | F-5 | bare backticked chain path | **CLOSED** | spec:281 |
| correctness | F-6 | "the original" ambiguous | **CLOSED** | spec:317 "all on the **normalized** text (D0: no masked copy exists)" |
| correctness | F-7 | stale talaria anchors | **CLOSED** | as F-8 above |
| correctness | F-8 | corpus scope overstated | **CLOSED** | spec:385 corpus-sampling note |
| edge-cases | F-1 | subtree fallback has no terminator | **CLOSED** | removed (spec:20, 179) |
| edge-cases | F-2 | exemption disarms the generic class | **CLOSED** | spec:207 |
| edge-cases | F-3 | `--project-path` doesn't base git `cwd` | **CLOSED** | spec:298 |
| edge-cases | F-4 | collision check undefined | **CLOSED** | spec:301 — `open(path,"x")` claim + `mkstemp`/`os.replace` render, stated as two mechanisms |
| edge-cases | F-5 | inline-span masking ordering | **CLOSED** | removed |
| edge-cases | F-6 | unterminated-fence advisory undefined | **CLOSED** | removed; zero residue (grep for fence/score/masking finds only D0's own removal prose) |
| edge-cases | F-7 | redaction prints short credentials | **CLOSED** | spec:211 fully-masked at ≤12 chars; pinned by test item 4 |
| edge-cases | F-8 | TODO in a fence evades the check | **CLOSED** | inverted and recorded as an accepted limit (spec:24), pinned by test item 5 |
| edge-cases | F-9 | `## ` vs `##` empty-heading boundary | **CLOSED** | spec:26 |

## Scope-down assessment (D0)

**(a) Conventional? Yes, and under-cited.** An explicit scope-down decision carrying its own rationale is the established shape here — `decisions/2026-08-07-pet-171-unreachable-state-needs-no-machinery.md` is the same move ("before building a discriminator for a feared failure state, check whether it can occur"), and D0's structural argument at spec:20 is precisely that form. The parser-rejection reasoning is **accurate**: no dependency manifest exists (no `requirements.txt`/`pyproject.toml`/`setup.py`/`Pipfile`), every import across `lint.py`, `sync.py`, and all four shipped script trees is stdlib, `sync.py` copies files with no install step, and `docs/portability-contract.md` §3 not only lacks a package key but states outright that the declaration is "**not** a sibling manifest file" and that the repo is stdlib-only because "stdlib has no YAML parser." See F-5 for the stronger citation available.

**(b) Wiki conflict: none.** No decision page governs handoff validation or completeness scoring. **Brief conflict: real, and mis-recorded** — see F-1.

**(c) New issues from the scope-down:** F-2 (stale cross-reference in the rewritten D4) and F-4 (the shrunken matcher surface no longer covers one caller's need). No removed machinery left residue.

## Findings

### F-1: § Deferred's D0 entry quotes brief text that does not exist, and understates what D0 drops relative to the brief
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:383 (§ Deferred), spec:365 (Done when #3), spec:251 (D12)
**Convention violated:** the spec-cycle drift-check contract — § Deferred is the artifact the human reads at the HARD STOP to see what the spec added or narrowed relative to the brief; and D12's own precedent of naming brief contradictions explicitly.
**Evidence:** spec:383 reads `D0's removal of the completeness-length check, which narrows the brief's "required sections present **and populated**" (brief:44) to presence-plus-no-placeholder`. The word "populated" appears nowhere in the brief (`grep -n "populated" VHS-28.brief.md` → no match). What brief:44 actually says is:
> `- Preserve the three distinctions the vendor fix was smoke-tested against: level-3 section with real content → passes; genuinely absent section → still `missing`; level-3 section with 5 characters → still `incomplete`.`

and brief:42 requires "the section-terminator scan." D0 removes both — the `incomplete` verdict no longer exists in D6's table (spec:196-201) and the terminator rule is explicitly cut (spec:133). Two knock-ons: spec:365 (Done when #3) claims a 1:1 map to brief done-when #3, but brief:71 requires tests covering "**the three** heading distinctions" while the spec's #3 quietly reads "depth-blind matching"; and D12 at spec:251 still asserts `reference/` is "**the one place** this spec contradicts brief text rather than extending it," which D0 has made false.
**Why not P1:** the *direction* is authorized — the brief's own § Open questions (brief:86-87) puts gate semantics up for redesign and offers "a pass/fail on required-sections-plus-no-secrets" as the alternative, which is exactly D6+D0. The completeness check is not in the brief's § Decisions carried forward. So this is a disclosure defect, not a violated carried-forward decision.
**Suggested fix:** in § Deferred, replace the quoted phrase with the real one — "narrows brief:42's section-terminator scan and brief:44's third distinction (`level-3 section with 5 characters → still incomplete`) to presence-plus-no-placeholder; the `incomplete` verdict is retired." Add a clause to Done when #3: "brief #3's third distinction is superseded by D0 — the verdict vocabulary no longer contains `incomplete`." Amend D12:251 to "one of two places" (or drop the uniqueness claim).

### F-2: D4 points at "Test item 4's round-trip"; the round-trip is test item 2 and item 4 is the verdict/exit matrix
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:181
**Convention violated:** AGENTS.md § Plan & Spec Reviews — findings and cross-references must resolve against current file state; this is a stale anchor introduced by the round-3 fix to my own F-4.
**Evidence:** spec:181 — "Test item 4's round-trip *detects drift* in an inlined copy". The round-trip with the heading-sequence assertion is **test item 2** (spec:330: "the scaffold's heading sequence equals `[name for _, name in TEMPLATE_SECTIONS if name]` in order (drift detection for an inlined table)"). Test item 4 (spec:332) is the verdict/exit matrix. Every other intra-spec test reference resolves correctly (spec:363 → item 10 Lint; spec:364 → items 2, 3; spec:375 → item 3), so this is the lone miss.
**Suggested fix:** spec:181 — "Test item 4's" → "Test item 2's".

### F-3: The script contract specifies PEP 585 annotations without the `from __future__ import annotations` line every shipped script in this repo carries, against an AGENTS.md-declared Python 3.8 floor
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec:296, spec:315 (`main(argv: list[str]) -> int`), § Encoding discipline
**Convention violated:** AGENTS.md § What this repo is — "no dependencies beyond Python 3.8+ stdlib"; and the uniform in-repo pattern for stdlib scripts.
**Evidence:** all six stdlib scripts in the tree open with `from __future__ import annotations` — `lint.py`, `sync.py`, `skills/talaria/scripts/talaria_{bridge,read,watch}.py`, `skills/hermes-kanban-awareness/scripts/read_board.py` — and the precedent signature is `def main(argv: list[str] | None = None) -> int` (`talaria_bridge.py:1070`, `talaria_read.py:289`, `talaria_watch.py:738`). On Python 3.8 an annotation of `list[str]` is evaluated at def time and raises `TypeError: 'type' object is not subscriptable`, so the spec as literally written does not import at the repo's own declared floor. The spec cites talaria's "return-an-int discipline" (spec:296) but not the header that makes the annotation legal.
**Suggested fix:** add to § Encoding discipline or § `scripts/create_handoff.py`: "All three modules open with `from __future__ import annotations`, following every stdlib script in this repo — AGENTS.md declares a 3.8 floor and the annotations used here are PEP 585." Optionally align the signature to `main(argv: list[str] | None = None) -> int`.

### F-4: `_sections` exports a module-private name across the module boundary, and D3's "whole matcher surface" doesn't cover the one thing `create_handoff.py` needs from it
**Severity:** P3
**Where:** spec:133 ("That is the whole matcher surface"), spec:137 (D4 export list), spec:310
**Convention violated:** repo precedent for the file-path-import seam — the only existing consumer pair reaches for public names only.
**Evidence:** spec:310 requires `create_handoff.py` to read "the previous document's first `#` heading via `_sections`' matcher on normalized text." `has_section(normalized, name) -> bool` (spec:122) cannot return a title, so the caller must consume `_sections._HEADING_RE` directly — a leading-underscore name, listed as an export at spec:137. Across the repo's only cross-module file-path import, `talaria_read.py` and `talaria_watch.py` consume exclusively public names from the loaded bridge (`bridge.read_operational`, `bridge.act`, `bridge.doctor`, `bridge.ensure_ready`, `bridge.evaluate_operational_selector`) — no `bridge._*` access anywhere. The gap is small but it is the second consumer inventing its own use of the shared regex, which is the shape D3 exists to prevent.
**Suggested fix:** add one public function to `_sections` — `first_heading_title(normalized) -> str | None` — and have `create_handoff.py` call it; then D3:133's "whole matcher surface" reads as `has_section` + `first_heading_title`, and `_HEADING_RE` stays private to the module.

### F-5: D0's parser rejection cites D1 where two recorded wiki decisions say it more directly
**Severity:** P4
**Where:** spec:14 ("Vendoring a parser into a public repo is what D1 refuses for the vendor skill.")
**Convention violated:** none — this strengthens an argument that is already correct.
**Evidence:** D1 refuses copying vendor *skill* code on provenance grounds, which is adjacent rather than on point. The recorded decision that refuses exactly this is `decisions/2026-06-15-vhs-19-fork-and-own-converter.md`: "**Carry the engine into vigil-skills.** Rejected: breaks the stdlib-only/no-build contract." And `docs/portability-contract.md` §3 states the no-manifest constraint normatively ("**not** a sibling manifest file"; "The repo is 'no dependencies beyond Python 3.8+ stdlib,' and stdlib has no YAML parser"). The shape of D0 itself has precedent in `decisions/2026-08-07-pet-171-unreachable-state-needs-no-machinery.md`.
**Suggested fix:** in D0 ¶2, swap the D1 sentence for "This is the same call `decisions/2026-06-15-vhs-19-fork-and-own-converter.md` made when it kept the Bun converter out of this tree, and `docs/portability-contract.md` §3 states the constraint normatively."

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 1

STATUS: GREEN
