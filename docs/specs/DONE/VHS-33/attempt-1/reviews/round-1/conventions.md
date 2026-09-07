# Conventions Review — round 1

Grounding: the spec and brief read fresh, `AGENTS.md`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, the wiki (`projects/vigil-skills/`, `decisions/2026-09-06-vhs-32-…`, `decisions/2026-08-09-review-round-artifacts-are-immutable.md`), the archived `docs/specs/DONE/VHS-32/spec.md`, and the four live skill files plus `ship-spec/SKILL.md`. Checklist rows 1–3 were executed against the tree at `7403cb5`.

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: Checklist row 2 and row 10 are mutually unsatisfiable — the grep fails on pre-existing `spec-cycle` text that row 10 forbids editing
**Severity:** P0
**Where:** `docs/specs/TODO/VHS-33.spec.md:384-387` (row 2) vs `:425-428` (row 10) and `:29` (Scope)
**Convention violated:** `docs/portability-contract.md` §4 case-1/case-3 classification; the VHS-32 precedent for this exact row (`docs/specs/DONE/VHS-32/spec.md:456`), which scoped the grep to the three **new** files it created.
**Evidence:** VHS-33 adds `skills/spec-cycle/SKILL.md` to the row-2 file list and asserts *"every hit is inside a parenthetical carrying 'or the equivalent', or under a `## Tool-use notes` heading, or is the prohibition itself."* Running it:

```
327:Single message, the reviewer Agent tool calls (three, or four when scale is declared) …
330:Agent(subagent_type="spec-reviewer-correctness", prompt=<context>)
331:Agent(subagent_type="spec-reviewer-edge-cases",  prompt=<context>)
332:Agent(subagent_type="spec-reviewer-conventions", prompt=<context>)
338:Agent(subagent_type="spec-reviewer-scalability", prompt=<context>)
341:When `scale_lens != on`, no fourth `Agent` call is emitted …
650:- Agent calls (parallel) for the reviewers …      ← under ## Tool-use notes (exempt)
652:- Skill invocation of `grilling` …                 ← under ## Tool-use notes (exempt)
```

Lines 327 and 330–341 sit under `### 2b. Dispatch the reviewers in parallel` — operative dispatch instructions, matching none of the three exemptions. So row 2 fails as written. Making it pass requires editing 2b, which row 10 forbids (*"hunks only inside the `### 2f-i` subsection and the one `## Failure modes` bullet — no hunk in 2a–2e"*) and which the Scope table also excludes. Because `## Test command` is `N/A`, this checklist **is** the ship gate, so the implementer hits a gate that cannot pass without violating another gate row.
**Suggested fix:** Scope row 2 to the diff, matching its own trailing sentence. E.g.: *"…for `skills/spec-cycle/SKILL.md`, evaluate only lines this change adds (`git diff -U0`); its pre-existing `Agent(...)` dispatch block in 2b is out of scope and unchanged. No new bare harness-tool call is introduced."*

---

### F-2: `## Test command` carries prose and two runnable commands under `N/A` — ship-spec's documented `N/A` parse will not fire
**Severity:** P1
**Where:** `docs/specs/TODO/VHS-33.spec.md:447-460`
**Convention violated:** `skills/ship-spec/SKILL.md:20` (the `N/A` exception), `skills/spec-cycle/SKILL.md:305`, and the VHS-32 precedent (`docs/specs/DONE/VHS-32/spec.md:477-479` — the section is the two characters `N/A` and nothing else).
**Evidence:** `skills/ship-spec/SKILL.md:20`: *"extract its raw text content (strip markdown code fences if present, trim leading/trailing whitespace). If the resulting string matches `N/A` (case-insensitive), record the resolved test command as `N/A` and do not fall through to step 4.2 or 4.3."* The extracted content here is not `N/A` — it is `N/A` plus three prose paragraphs plus a fenced block containing `python lint.py --strict` / `python sync.py status`. A literal implementer therefore falls through to 4.2 (`CLAUDE.md` "Build & Run" — this repo has none; `AGENTS.md` says "no build step, no test suite") and then to 4.3, which **halts loudly**. The alternative failure is worse: an implementer reads the fenced block as the test command and runs the Phase 3 test-gate loop, which the spec explicitly says will not happen (`:459-460`).

The two commands are also pure duplication — they are already checklist rows 1 and 15 (`:381-383`, `:444-445`), so removing them costs nothing and restores single-source-of-truth.
**Suggested fix:** Make the section body exactly `N/A`. Move the surrounding sentences into the `## Test plan` preamble (`:374-378`), where the "checklist is the gate" framing already lives — VHS-32 did precisely this.

---

### F-3: `## Out of scope` says "Carried from the brief" but one fence is widened and one is a spec-author addition
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:483-502` (header `:485`, item 1 `:488-489`, item 9 `:500-502`)
**Convention violated:** VHS-32's Out-of-scope shape (`docs/specs/DONE/VHS-32/spec.md:496-514`), which splits the section into **"Carried verbatim from the brief:"** and a separately labelled **"Spec-author additions to the fence (each a consequence of a Decision above, not new scope):"**.
**Evidence:** Two divergences under a flat "Carried from the brief." header:

1. Brief `:61` reads *"Any change to the three bounds, the fork form, the advisory-recommendation rule, or the fact-finding dispatch rules (ticket)."* The spec renders it as *"…or the fact-finding dispatch rules — **except the claim-verification path Design 3 adds, which the brief scopes in explicitly**."* The brief's fence carries no such exception; only brief decision 4 authorizes the path, and the two are in tension. The spec resolves that tension correctly but attributes the resolution to the brief. It matters because Design 3 (`:206-219`) does more than add a path: departure 1 carves an exception into the existing failed-dispatch rule at `skills/grilling/SKILL.md:76`, and departure 2 makes verification consume `question_cap` — both are edits to rules the brief fenced.
2. Item 9 (`:500-502`, no mechanical assertion in `lint.py` / `sync.py` / `tests/`) appears in no form in the brief's `## Out of scope` (`:59-68`). It is a spec-author fence.

**Suggested fix:** Split the section as VHS-32 did. Keep the brief's eight items verbatim under "Carried verbatim from the brief:", then a second list — "Spec-author additions to the fence" — holding item 9 and the claim-verification carve-out, with the honest one-liner: *"the brief's fence and its Decision 4 conflict; this spec narrows the fence to the claim-verification path Decision 4 authorizes, and to nothing else."*

---

### F-4: No roll-up of the spec-level Design additions for the drift-check
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** `docs/specs/TODO/VHS-33.spec.md:49` (the `## Decisions` preamble)
**Convention violated:** VHS-32's `## Decisions` preamble (`docs/specs/DONE/VHS-32/spec.md:31`), which classifies every decision and then explicitly enumerates the ones recorded at point of use.
**Evidence:** VHS-32: *"S6–S9 are spec-level additions with rationale, authorized by neither brief nor ticket… Five further reviewer-driven additions are recorded at their point of use rather than as S-items, and **are listed here so the drift check sees them**: …"* VHS-33's preamble is one line — *"Carried from the brief's `## Decisions carried forward`, in its numbering."* — which is true of D1–D12 but leaves at least seven load-bearing spec-level additions buried in Design prose with no index:

- `blocked-on: F<n>` as new Q-item reason vocabulary, and the narrowing of the Q-item reason set (`:182-185`) — brief decision 3 authorizes an *added* F-shape, not a removal from the Q set.
- The two Design-3 departures from the existing dispatch rules (`:206-219`).
- The `empty-frontier` boundary sentence for later fence-blocked rounds (`:234-237`).
- `_(none)_` as the empty-section rendering (`:239-241`).
- Lens-qualified seed ids `<lens>/<finding-id>` (`:279-284`).
- The four-way precedence rule and seed-order dedup (`:296-315`).
- `unknown ref ignored: <id>` (`:316-319`) and `; unreferenced decisions applied: <n>` (`:302-309`).

Each is individually reasonable and rationalized in place — this is a visibility gap, not a substance objection. But `/spec-cycle`'s Phase 3 drift-check is a *structural* checklist, and VHS-32 established that unindexed additions are what it misses.
**Suggested fix:** Add one paragraph after `:49`: *"D1–D12 are carried from the brief; D13 records the brief's `## Scale` non-factor per `/spec-cycle` Phase 1. The following are spec-level additions with rationale, recorded at their point of use and listed here so the drift check sees them: …"* with the seven bullets above.

---

### F-5: The absent-`ref:` rule is justified by a parser-compat concern the brief says does not exist
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:155-157` (Design 1, "Rendering — the absent/none rule")
**Convention violated:** the repo's general "no unneeded backwards-compat" posture (`AGENTS.md` Git Hygiene / the VHS-28 delete-cleanly precedent); brief F1.
**Evidence:** The spec's stated reason for the absent state is *"The block is byte-identical to v1 in this respect, so those two callers' parsers are unaffected."* But brief `:83` (F1) records: *"nothing mechanical asserts the hand-off block's shape: `lint.py`, `sync.py`, `tests/` contain no reference to `skills/grilling`"* — and the spec repeats this at `:42-43`. `/spec-brief` and `/grill-me` are model consumers, not parsers; nothing breaks if `ref: none` were always emitted. The rule is still the right call, but for a different reason: `/spec-brief` transcribes Settled items into the brief, and a `ref: none` on every item would be noise in an artifact every downstream lens treats as authority.
**Suggested fix:** Replace the compat rationale with the artifact-cleanliness one, e.g.: *"Absent, not `none`, when no ids were supplied — `/spec-brief` transcribes Settled items into the brief, and a universal `ref: none` would be noise in the artifact every downstream lens reads. Nothing mechanical parses the block (brief F1), so this is a legibility rule, not a compatibility one."*

---

### F-6: No `## Risks` and no `## References` section
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md` (whole document)
**Convention violated:** VHS-32's spec shape (`docs/specs/DONE/VHS-32/spec.md:516-551` Risks; `:534-551` References). Not in `/spec-cycle`'s minimum template (`skills/spec-cycle/SKILL.md:300-307`), but it is the established shape for this surface.
**Evidence:** There is real residual risk to record, and nowhere records it: (a) the v2 contract remains a prose contract with no mechanical assertion, and the spec's own Out-of-scope item 9 fences creating one — so after this ships, *nothing* asserts the block's shape (the archived VHS-32 row 4 is superseded); (b) VHS-32 Risks 9 (`requires:` has no token for nested skill invocation) and 11 (`user_invocable: false` is advisory) are unchanged by this ticket and should be carried as "unchanged, not fixed here"; (c) the `ref:` echo is model-rendered, so a mis-echoed id is possible — which is exactly why `unknown ref ignored:` exists, but that tripwire is a mitigation, not a risk record. The anchors are currently scattered inline with only the header line `**Anchors verified against:** vigil-skills 7403cb5` (`:5`) tying them together.
**Suggested fix:** Add a `## Risks` section carrying (a)–(c) plus the VHS-32 Risk 9/11/14 status, and a `## References` section consolidating the anchors already cited inline.

---

### F-7: The VHS-32 wiki decision's "Revisit when" trigger fires on this ticket and is not recorded
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:102-107` (D9) and `:483-502`
**Convention violated:** `vigil-harbor-wiki/decisions/2026-05-01-wiki-maintenance-redesign.md` supersede-and-link; the VHS-32 spec's own precedent of dispositioning a wiki revisit trigger in-spec (`docs/specs/DONE/VHS-32/spec.md:549`).
**Evidence:** `vigil-harbor-wiki/decisions/2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` header: *"Revisit when: VHS-33 lands the hand-off contract v2 (caller IDs, fact-item shapes, `fence-empty` token)"*. This spec lands exactly that. D9 handles the archived-spec side of supersession correctly, but says nothing about the live wiki decision whose stated trigger it fires, and the wiki is `/spec-close`'s job — which reads the spec.
**Suggested fix:** One line in D9 or Out of scope: *"The wiki decision `2026-09-06-vhs-32-the-interview-is-bounded-and-cannot-write.md` names this ticket as its revisit trigger; updating it is `/spec-close`'s decomposition step, not this spec's."*

---

### F-8: `; unreferenced decisions applied: <n>` is conditionally omitted on a line whose other four clauses are unconditional
**Severity:** P3
**Where:** `docs/specs/TODO/VHS-33.spec.md:302-309` (Design 6, step 5)
**Convention violated:** the existing step-5 line shape (`skills/spec-cycle/SKILL.md:549`), whose four id-set clauses always render.
**Evidence:** The spec adds a fifth clause "omitted entirely when `n` is 0" while leaving the other four unconditional — and the spec never says what an *empty* id-set renders as in the four existing clauses, so a reader can't tell whether the asymmetry is deliberate or an oversight. A variable-arity report line is also harder to eyeball for the operator this line exists to serve.
**Suggested fix:** Either render the clause unconditionally (`unreferenced decisions applied: 0`), or state the omission rule alongside a matching statement of how an empty id-set renders in the four existing clauses (e.g. `dispositioned (none)`).

---

### F-9: Three spellings of "empty" now coexist in one contract
**Severity:** P4
**Where:** `docs/specs/TODO/VHS-33.spec.md:239-241` (`_(none)_`), `:158-160` (`ref: none`), vs `skills/grilling/SKILL.md:122` (`Facts relied on: <F-ids or "none">`)
**Convention violated:** the spec's own D12 rule — *"One meaning per term: the same thing keeps the same name"* (`:121-125`).
**Evidence:** After this change the block carries `none` (bare, in `Facts relied on:`), `ref: none`, and `_(none)_` (section-empty), while `/spec-brief` separately writes `_(none settled — see Risks / decisions)_` (`skills/spec-brief/SKILL.md:139`). The first two are consistent; `_(none)_` is a fourth shape for a related idea, introduced by a design whose headline rule is one-meaning-per-term.
**Suggested fix:** Add one sentence to Design 4 noting that `_(none)_` is the section-empty sentinel and `none` the field-empty one, so the two are not confusable — or reuse `none` for both.

---

## Verified, not findings

- **Superseding the archived VHS-32 checklist row 4 by carrying a forward-facing row (D9, Test plan row 4, `:389-398`) is the right convention.** It matches `vigil-harbor-wiki/decisions/2026-08-09-review-round-artifacts-are-immutable.md` — *"never edited after their round closes. Closures are recorded **forward**"* — and the spec's Scope fence at `:40`, reinforced by checklist row 14. No finding.
- **D13 matches the brief's `## Scale` → `**Factor:** no`** and satisfies `skills/spec-cycle/SKILL.md:313`. It also correctly states why (Phase 3 drift-check anchor + the Phase 0 re-run pin at `:280-290`). No finding.
- **Portability (§4) holds in the spec's own prose.** Every dispatch is intent-phrased; no bare harness tool call is added as an operative imperative. The public-repo constraint is respected.
- **Checklist rows 1 and 3 pass today**: `python lint.py --strict` → `0 error(s), 2 warning(s)` (`review-pr`, `ship-spec` — exactly the stated baseline); `grep -c 'model:'` → 0 for all three files.
- **Scope-table and Design anchors spot-check clean** against `7403cb5`: `grilling` `:14-23`, `:33-57`, `:68-78`, `:74`, `:76`, `:88`, `:102-112`, `:108`, `:114-134`, `:136-138`, `:146-151`; `spec-brief` `:139` and `:141` are exactly what Design 7 claims.
- **No premature abstraction.** `ref:` serves three callers with one supplier today, and the two-state rendering rule is the minimum shape, not a registry.

## Summary
P0: 1 | P1: 1 | P2: 2 | P3: 4 | P4: 1

STATUS: RED P0=1 P1=1 P2=2 P3=4 P4=1
