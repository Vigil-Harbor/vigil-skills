# Conventions Review — round 3

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | `sys.path` insertion vs talaria precedent | CLOSED | spec.md:147-155 — `spec_from_file_location` + "No `sys.path` mutation"; anchors `talaria_bridge.py:3-4`, `talaria_read.py:23-32` verified exact (see F-8 for the watch anchor) |
| conventions | F-2 | `create_handoff.py` omits the `_sections` import | CLOSED | spec.md:307 — "Imports `TEMPLATE_SECTIONS` from `_sections` by file path (D4); the section table is never restated in this file" |
| conventions | F-3 | `lint.py` citations describe behavior it doesn't implement; `lint.py:52` stale | CLOSED | spec.md:115 contrasts CommonMark pairing against `lint.py:211-213`'s toggle (verified: 211 `if _FENCE_RE.match`, 212 `in_fence = not in_fence`, 213 `continue`); spec.md:191 now `lint.py:60` (verified `_CASE2_TAG = "or the equivalent"`) |
| conventions | F-4 | AGENTS.md uninstall lacks harness qualifier, POSIX-only | CLOSED | spec.md:234-238 — harness-qualified dual-shell entry; AGENTS.md's own "for Claude Code: `~/.claude/skills/`" verified at AGENTS.md:9 |
| conventions | F-5 | Fixture lands flat in a lint-only corpus | CLOSED | spec.md:37-40 — both fixtures under `tests/fixtures/session-handoff/`; verified root `.gitattributes` is `*.md text eol=lf` and `tests/fixtures/.gitattributes` carries no `*.md` rule, so no `-text` entry is needed; verified no test globs `tests/fixtures/` |
| conventions | F-6 | Bare `python` vs pinned-interpreter guidance | CLOSED | spec.md:363 — pin-by-full-path requirement; verified `skills/talaria/scripts/__pycache__/` holds cpython-310/311/314 artifacts |
| conventions | F-7 | Drift roll-up of spec-level additions | CLOSED (carried) | spec.md:394 § Deferred — but see F-7 below: v3's own additions are not folded in |
| conventions | F-8 | D12's AGENTS.md rationale partly inaccurate | CLOSED | spec.md:262 — verified AGENTS.md:54 is the `skills/spec-close/SKILL.md` row, and `git show --stat` confirms a0ad847 / 386dc6c / 8946f58 touch no AGENTS.md |
| correctness | F-1 | CRLF `\r` captured into title | CLOSED | spec.md:83-85 normalization step, load-bearing rationale |
| correctness | F-2 | Own content measured on masked copy | CLOSED | spec.md:140 — measured on the original |
| correctness | F-3 | Thematic break left as prose | CLOSED | spec.md:95-98 `_THEMATIC_BREAK_RE` |
| correctness | F-4 | Setext contradicts the terminator rule | CLOSED | spec.md:108 |
| correctness | F-5 | Two different fence algorithms described | CLOSED | spec.md:115 |
| correctness | F-6 | Exit codes vs in-process `load_script` | CLOSED | spec.md:307, 324, 336 — `main(argv) -> int`; matches `tests/test_talaria_watch.py:21-30`'s `load_script` |
| correctness | F-7 | `create_handoff.py` import + `sys.path` | CLOSED | spec.md:307 (see conventions F-1/F-2) |
| correctness | F-8 | `TEMPLATE_SECTIONS` never enumerated | CLOSED | spec.md:161-177 table |
| correctness | F-9 | Bounded read names the wrong end | CLOSED | spec.md:193 — discard first line on non-zero offset |
| correctness | F-10 | Stale anchor `lint.py:52` | CLOSED | spec.md:191 → `lint.py:60`, verified |
| correctness | F-11 | D12's AGENTS.md claim inaccurate | CLOSED | spec.md:262 |
| correctness | F-12 | "before or alongside" reopens the scope boundary | CLOSED | spec.md:21, 390 — "merge … first, then cut"; "resolved *before* this work … not part of this spec's diff" |
| edge-cases | F-1 | `\r` + no newline normalization | CLOSED | spec.md:83-85 |
| edge-cases | F-2 | Masked measurement | CLOSED | spec.md:140 |
| edge-cases | F-3 | Fixture pins minority shape | CLOSED | spec.md:37-38, 157 — two fixtures + explicit depth-agnostic rule |
| edge-cases | F-4 | Unterminated/nested fence | CLOSED | spec.md:115-116 |
| edge-cases | F-5 | Thematic break as three literals | CLOSED | spec.md:96-98, 111 |
| edge-cases | F-6 | "Blanked" undefined / offset drift | CLOSED | spec.md:113 — length-preserving masking, newlines preserved |
| edge-cases | F-7 | `.claude/handoffs/` never created | CLOSED | spec.md:310 |
| edge-cases | F-8 | `Continues from` format unspecified | CLOSED | spec.md:315-318 pinned format |
| edge-cases | F-9 | RESUME on absent/empty directory | CLOSED | spec.md:289 |
| edge-cases | F-10 | `BLOCKED` from auto-generated metadata | **PARTIAL** | spec.md:217 adds the exemption, but its region is undefined and D1/D4 forbid keying on the only identifier — see F-1 below |
| edge-cases | F-11 | Preconditions' two divergent values | CLOSED | spec.md:21-23 single gate + verification step; verified HEAD now tracks 7 skills and `tests/test_lint.py:52` reads `len(skills), 7` |
| edge-cases | F-12 | Leaf invariant vs real documents | CLOSED | spec.md:183 subtree fallback |
| edge-cases | F-13 | Inline code spans unmasked | CLOSED | spec.md:117 |
| edge-cases | F-14 | `sys.path` persistence + `__pycache__` | CLOSED | `sys.path` gone; `__pycache__` at spec.md:51 and § Deferred:396 |
| edge-cases | F-15 | Chain cycle keys on filenames | CLOSED | spec.md:291 — `resolve()`d absolute paths, case-insensitive on Windows |
| edge-cases | F-16 | CommonMark divergences | CLOSED | spec.md:109 |

Every round-2 finding closed except edge-cases/F-10, whose fix introduced the P1 below.

## Findings

### F-1: D6's metadata-block exemption has no defined region, and D1/D4 explicitly forbid keying on the only thing that identifies it
**Severity:** P1
**Where:** spec.md:217 (D6), against spec.md:69 (D1), spec.md:159 + 163 (D4 table), spec.md:343 (test-plan item 6)
**Convention violated:** The lens's cross-surface rule — lock the boundary, don't leave it implied; and the spec's own single-source discipline. Also an internal contradiction between D1 and D6.
**Evidence:**
- D6, spec.md:217 — "**the generic assignment class is not applied to the auto-generated metadata block**".
- D1, spec.md:69 — "**Container heading names are *not* fixed** — they are never matched or validated, so the implementer chooses them freely."
- D4's table caption, spec.md:159 — "container names are the implementer's choice per D1" — yet the table at spec.md:163 names one: `| ## | Session Metadata | container/meta |`, a tenth name outside D1's stated nine-name (`REQUIRED ∪ RECOMMENDED`) carve-out.
- Test-plan item 6, spec.md:343, pins the behavior: "a scaffold whose HEAD commit subject contains `client_secret = <20 chars>` is not `BLOCKED`".
- § `validate_handoff.py`, spec.md:326, restates the exemption without a locating rule.

Given only a file path, `validate_handoff.py` must decide which byte range is exempt. Every available option is either foreclosed or unstated:
1. **Match the `Session Metadata` heading** — foreclosed by D1's "never matched or validated" and D4's caption, and it silently stops applying to any document whose metadata heading differs. Both legacy fixtures and all five real on-disk documents are outside the exemption under this reading, which reinstates the unremediable-`BLOCKED` failure D6 exists to remove — a silent-failure path behind a "by construction" claim.
2. **A marker emitted by `create_handoff.py`** — the natural resolution, and the only one that satisfies D1 and D6 simultaneously, but § `create_handoff.py` (spec.md:305-320) enumerates everything the writer emits and no marker is among them.
3. **A positional heuristic** (first section / everything above the first required section) — unstated.

This is a security-gate boundary being left to implementer invention, with the most obvious choice contradicted by a different decision in the same spec.
**Suggested fix:** Pick option 2 and write it down in three places: (a) add to § `create_handoff.py` that the generated metadata block is delimited by a fixed, machine-readable marker (e.g. `<!-- session-handoff:metadata -->` … `<!-- /session-handoff:metadata -->`), emitted verbatim and never escaped; (b) restate D6's exemption as "the generic assignment class is suppressed *between the metadata markers*, and nowhere else — a document without markers gets no exemption"; (c) amend D1/D4 so `Session Metadata` is either an explicitly fixed, matched name (moving it out of the "implementer's choice" carve-out and into the reused-verbatim list, making it ten names not nine) or is dropped from the table as `*(container)*` like the other four. Add a test-plan case: a legacy document with no markers and a `client_secret = …` line in its metadata section **is** `BLOCKED` — so the exemption's absence on legacy input is a pinned, intended outcome rather than a discovered one.

### F-2: D4's `importlib` snippet is truncated relative to the precedent it cites, and silently diverges from talaria's per-consumer module-naming convention
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:149-155 (D4)
**Convention violated:** `skills/talaria/scripts/talaria_read.py:23-32` / `talaria_watch.py:33-42` — the repo's only file-path-import precedent, which D4 names as the pattern being followed.
**Evidence:** The spec shows only:
```python
spec = importlib.util.spec_from_file_location(
    "_session_handoff_sections", Path(__file__).resolve().with_name("_sections.py")
)
```
The cited precedent (`talaria_read.py:23-32`) is five more lines and every one of them is load-bearing:
```python
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load talaria_bridge.py from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
```
`spec_from_file_location` alone loads nothing. Two further divergences go unstated:
- **Shared synthetic name.** Talaria deliberately gives each consumer its own (`talaria_bridge_runtime` at `talaria_read.py:25`, `talaria_bridge_watch_runtime` at `talaria_watch.py:35`); D4 uses one name for both entry points. That may well be the better choice here — one module object is what "single source" wants — but it is a departure from the precedent D4 says it follows, and it matters for the tests: `tests/test_talaria_watch.py:22` opens with `sys.modules.pop(module_name, None)`, so in a single test process `create_handoff`, `validate_handoff`, and the leaf-invariant test can each end up holding a *different* `_sections` object for the same file. `TEMPLATE_SECTIONS` comparisons must then be by value, never by identity.
- **`.resolve()`** is added where the precedent uses bare `.with_name()`. Benign, but unremarked.

**Suggested fix:** Replace the snippet with the full six-line loader shape (guard → `module_from_spec` → `sys.modules[name] = module` → `exec_module`), and add one sentence: "Both entry points use the same synthetic name `_session_handoff_sections` — deliberately unlike talaria's per-consumer names, so the module is shared where it can be; tests compare `TEMPLATE_SECTIONS` by value, never by identity."

### F-3: A region-scoped *suppression* in a secret scanner departs from the repo's advisory-finding precedent and the wiki's recorded detect-and-record posture
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:217 (D6), spec.md:326 (§ `validate_handoff.py`)
**Convention violated:** `lint.py`'s WARN/ERROR split (the in-repo precedent D6 itself invokes at spec.md:213), plus two recorded wiki positions.
**Evidence:**
- In-repo: `lint.py:158`, `lint.py:248`, `lint.py:252` emit `(WARN, …)` findings that are reported but never gate — the repo's established way to say "we saw this, it doesn't block." D6 already cites `lint.py`'s warn-only posture at spec.md:213 and then, for the metadata block, chooses *not to look* rather than *to look and not gate*.
- Wiki, `decisions/2026-08-06-pet-170-annotate-never-withhold.md` — "Nothing is withheld under any `fail_mode`… detect-and-record as a first-class outcome rather than deny-only"; the console "renders the row as neither blocked nor clean." The fleet's answer to "this finding shouldn't block" is a third state, not silence.
- Wiki, `decisions/2026-05-27-pet-22-secret-field-registry.md` — the option explicitly rejected there is the per-region exclusion, because it "fails silently when new secrets are added." D6's exemption is that shape: a region where a whole detector class stops running, with nothing printed to say so.

Concretely, a real `AWS_SECRET_ACCESS_KEY = …` pasted into a commit subject would be scanned, matched, and then silently dropped — the author never learns their commit message carries a credential.
**Suggested fix:** Change D6's exemption from "not applied" to "applied, but demoted": generic-class matches inside the metadata block print as an advisory finding with the same locus + redacted excerpt as every other finding, labelled `advisory (auto-generated metadata — not gating)`, and do not set exit `2`. Update the § `validate_handoff.py` bullet at spec.md:326 to match, and extend test-plan item 6 to assert the advisory line is present on the non-`BLOCKED` scaffold. This keeps the escape hatch, satisfies the report-everything discipline, and costs one line of output.

### F-4: D4 claims the leaf-invariant test structurally prevents `create_handoff.py` from inlining the section table; it only detects drift
**Severity:** P3
**Where:** spec.md:181 (D4)
**Convention violated:** Single-source-of-truth claims must be verified against what the test actually pins (my lens's "verify 'by construction' claims" rule).
**Evidence:** spec.md:181 — "A test asserts this against `TEMPLATE_SECTIONS` read from the loaded `_sections` module — **which also fails the suite if `create_handoff.py` inlines its own copy of the table.**" A test that reads `_sections.TEMPLATE_SECTIONS` and checks the leaf invariant never touches `create_handoff.py`. The only test that observes both sides is item 4 (spec.md:341), and it compares `REQUIRED ∪ RECOMMENDED` names against a generated scaffold — so an inlined copy that stays *in sync* passes every test in the plan. The pin is drift-detection, not structural prevention, and it covers names only, not depths or ordering.
**Suggested fix:** Reword to what is true: "…and item 4's round-trip fails if an inlined copy in `create_handoff.py` ever drifts from `_sections`. Structural prevention is the § `create_handoff.py` rule that the table is never restated (spec.md:307), not a test." Optionally add a cheap structural pin to item 4: assert the scaffold's heading sequence equals `[name for _, name in TEMPLATE_SECTIONS if name]` in order.

### F-5: D3 reimplements two `lint.py` matcher shapes without stating why `lint.py` cannot simply be imported
**Severity:** P3
**Where:** spec.md:90-98, spec.md:115 (D3)
**Convention violated:** Reuse-vs-duplicate — the spec duplicates repo helpers and explains *which* behavior it declines to reuse, but never why it can't reuse the module.
**Evidence:** D3 says "We reuse `lint.py:55`'s `_FENCE_RE` *shape*; we do not reuse its pairing" (spec.md:115), and `_HEADING_RE` (spec.md:90) covers ground `lint.py:58`'s `_HEADING_STRIP_RE` already partly covers. The real reason duplication is correct here is structural and is nowhere on the page: `sync.py`'s `SUBTREES = ("skills", "agents")` (AGENTS.md:79 restates this) means `lint.py` is *not* mirrored into the operator's harness dir, so a skill script importing it would work in-repo and `ImportError` on every install. Without that sentence the duplication reads as an unexamined copy, and it is the first thing a reviewer or CodeRabbit will ask.
**Suggested fix:** Add one sentence to D3: "`_sections.py` cannot import `lint.py`: `sync.py` mirrors only `skills/` and `agents/`, so `lint.py` does not exist beside the installed skill. The regex shapes are reproduced deliberately, not copied for convenience."

### F-6: D12 settles the AGENTS.md inventory question but is silent on `README.md`'s `### Skills` list — the repo's established home for discoverability pointers
**Severity:** P3
**Where:** spec.md:259-262 (D12), § Modified files spec.md:44-47
**Convention violated:** AGENTS.md § Conventions — "Anything that must ship in a PR … belongs in a **tracked** file (`AGENTS.md`, `README.md`, or `docs/`)"; and the VHS-17/VHS-18 precedent of landing discoverability pointers in `README.md`.
**Evidence:** `README.md:7` opens a `### Skills` section listing only `/spec-cycle`, `/ship-spec`, `/review-pr` (README.md:9-11) — `talaria`, `spec-close`, `bloat-check`, and `hermes-kanban-awareness` are all absent. D12's reasoning ("A new row would extend an inventory nothing keeps current") applies to README with equal force and better evidence (3 of 7 listed vs AGENTS.md's mixed rows), but D12 never names it. Meanwhile `README.md:47` and `README.md:51` are exactly where VHS-17 and VHS-18 put their pointers, per wiki `projects/vigil-skills/state.md`. A reader of D12 cannot tell whether README was considered and declined or simply missed — and `session-handoff` is the first *user-invocable, natural-language-triggered* skill since that list went stale, which is the strongest case yet for listing.
**Suggested fix:** Extend D12's second bullet by one clause: "…and no `README.md` § Skills entry either — that list is 3-of-7 stale and none of the last four skills added one." Or, if the intent is the opposite, add `README.md` to § Modified files with a one-line `/session-handoff` bullet. Either is defensible; the silence is not.

### F-7: Drift roll-up — v3's new spec-level additions are not carried into § Deferred
**Severity:** P3
**Where:** spec.md:394 (§ Deferred)
**Convention violated:** My lens's silent-additions classification (a)/(b)/(c)/(d); the roll-up bullet exists but was not refreshed for v3.
**Evidence:** § Deferred:394 still reads as the round-1/round-2 roll-up, naming only D12's `reference/` override of brief:30 as the item for the human drift-check. Three v3 additions belong in that list:
- **(c) D6's metadata exemption (spec.md:217)** — the brief's open question offered "pass/fail on required-sections-plus-**no secrets**" (brief:86); D6 answers it and then carves a region out of "no secrets." Rationale is explicit, so this is (c), not (d) — but it narrows an acceptance-shaped property and is precisely the kind of thing the drift-check exists to surface.
- **(c) D3's normalization + length-preserving masking (spec.md:83-85, 113)** — substantial new machinery the brief does not mention; rationale is explicit and measured, so (c).
- **(c) D4's `TEMPLATE_SECTIONS` (spec.md:161-177)** — the brief specifies `references/handoff-template.md` as the section structure's home (brief:30); v3 makes a Python table the source and the template a rendering of it. Sound, and stated, but a structural relocation the brief did not authorize.

No (d) items — every v3 addition carries rationale.
**Suggested fix:** Add a v3 line to § Deferred: "**conventions/F-7 (r3, P3)** — v3's (c)-class additions: D6's metadata-block exemption narrowing the brief's 'no secrets' gate; D3's normalization/masking machinery; D4's relocation of the section schema from `reference/handoff-template.md` (brief:30) to `_sections.TEMPLATE_SECTIONS`. All carry rationale; recorded for drift-check visibility, no edit required."

### F-8: Two anchors introduced by the round-2 fix are imprecise
**Severity:** P4
**Where:** spec.md:155 (D4)
**Convention violated:** AGENTS.md § Plan & Spec Reviews — "specific `file:line` references"; the same discipline round 2 applied to `lint.py:52`.
**Evidence:** D4 cites "`talaria_read.py:23-32`, `talaria_watch.py:35-45`". Verified: `talaria_read.py` — `def _load_bridge()` at 23, `return module` at 32, **exact**. `talaria_watch.py` — `def _load_bridge()` at **33**, `return module` at **42**; the cited range starts two lines inside the body (skipping the `path = Path(__file__).with_name(...)` line that is the whole point of the citation) and overruns into `_as_path`. Separately, `talaria_bridge.py:3-4` — line 3 is blank; the quoted sentence is line 4 and its full statement runs to line 7.
**Suggested fix:** `talaria_watch.py:35-45` → `talaria_watch.py:33-42`; `talaria_bridge.py:3-4` → `talaria_bridge.py:4-7`.

### F-9: `_HEADING_RE` still guards for `\r` that D3 guarantees cannot reach it
**Severity:** P4
**Where:** spec.md:91 (D3)
**Convention violated:** None — internal consistency nit.
**Evidence:** spec.md:83-85 makes newline normalization mandatory and load-bearing ("All matching, span arithmetic, offsets, and length measurement operate on a normalized string"), so no `\r` can survive into the matcher. Yet spec.md:91 is `r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t\r]*#*[ \t\r]*$"` — two `\r`s in the trailing classes, leftovers from the pre-normalization draft. Harmless, but an implementer reading the regex may reasonably infer normalization is belt-and-braces rather than required, which is the exact inference D3's paragraph works to prevent.
**Suggested fix:** Drop `\r` from both classes — `r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$"` — and add a half-sentence: "no `\r` appears in the matchers; normalization is a precondition, not a fallback."

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 4 | P4: 2

STATUS: RED P0=0 P1=1 P2=2 P3=4 P4=2
