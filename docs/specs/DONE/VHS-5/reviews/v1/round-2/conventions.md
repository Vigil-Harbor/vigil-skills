# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | Test command shape drift (uses `test "$(...)" =` instead of bare `grep -c`) | PARTIAL | Spec line 159 now uses `-ge "1"` / `= "0"` / `-ge "3"` (no magic-number `= "6"`) so the brittleness concern is resolved. Shape still differs from VHS-3/4/6 (which use bare `grep -c` chained via `&&`), but the difference is technically necessary: the P1 assertion `--stat` count must be **zero** — bare `grep -c '--stat' file` would exit 1 on zero matches and break the `&&` chain, which is the opposite of the desired semantics. The `test "$(...)"` wrapper is required for the "must be absent" clause. Convergence with prior VHS pattern is not possible without changing what the spec asserts. |
| conventions | F-2 | Comment text at line 241 verbose vs. surrounding `#`-line note style | PARTIAL | The 36-word `Note:` block (spec lines 75-77) is unchanged. Round 1 explicitly concluded "the comment does meet the 'WHY non-obvious' bar". The user's round-2 framing cites a `CLAUDE.md` rule "Default to writing no comments. Only add one when the WHY is non-obvious" — that exact text is NOT in this repo's CLAUDE.md (verified by grep across 78 lines; the repo's CLAUDE.md has no comment-style section at all). The WHY is genuinely non-obvious (REST vs GraphQL bot-login parity is the exact failure mode that produced this bug); a future reader "fixing" the filter back is the precise regression this comment prevents. Keeping the verbose form is the right call. No drift. |
| conventions | F-3 | "Cargo-cult code" editorializing | CLOSED-AS-WONTFIX | Spec Decision 1 line 29 still uses "would be cargo-cult code". This was P4 (pure tone nit). Round-2 changeset did not touch it, and the user's round-2 brief does not ask about it. Acceptable to leave; the reasoning is sound. |
| conventions | F-4 | Exact-count assertions not authorized by brief | CLOSED | Test command (line 159) no longer asserts any exact count — switched to `-ge "1"` (P0 fix presence), `= "0"` (P1 absence), `-ge "1"` (P1 replacement presence), `-ge "3"` (P2 wording presence). The brittle `= "6"` assertion is gone. The brief's Done-when remains structural (presence checks), which the new shape honors. |
| conventions | F-5 | "Three similar lines" attribution implied to be CLAUDE.md | CLOSED | Spec line 135 now reads: "the principle 'three similar lines is better than a premature abstraction' comes from this repo's `spec-reviewer-conventions` prompt, not from `CLAUDE.md`." Attribution explicit and correct. |
| conventions | F-6 | Wiki state.md doesn't track VHS-5 | CLOSED-NON-DEFECT | Not a spec defect; `/wiki-after-merge` handles state.md post-merge. Round-2 changes don't affect this. |
| correctness | (n/a) | round-1 correctness | Not in scope of this lens. |
| edge-cases | (n/a) | round-1 edge-cases | Not in scope of this lens. |

## Findings

### F-1: Test command shape diverges from VHS-3/4/6 convention but the divergence is structurally required

**Severity:** P3
**Where:** spec.md line 159 (Test command)
**Convention violated:** Prior VHS test-command pattern. VHS-3 line 253, VHS-4 line 270, VHS-6 line 227 all use `python sync.py status && grep -c <pattern> <file>` — bare `grep -c` chained with `&&`, where each grep's non-zero count passes the `&&` step.
**Evidence:** VHS-5 spec line 159 uses `test "$(grep -c <pat> <file>)" -ge "1"` (and `= "0"` for the absence assertion). The structural divergence is forced by the P1 assertion `--stat must be absent`: a bare `grep -c '--stat' file` exits 1 on zero matches, which would fail the `&&` chain when zero is what the assertion wants. The spec also explicitly documents (lines 147-148) why `python sync.py status &&` is dropped: it prints drift information but doesn't exit non-zero, and pre-existing peon-ping / states.json drift would clutter the report.
**Suggested fix:** None required. The spec's deviation is justified in-text. Optional: add one sentence to the Test command block making the "absence-assertion forces `test "$(...)"`" point explicit, so future readers don't try to "converge" the shape with VHS-3/4/6 without realizing the asymmetry.

### F-2: `Note:` comment at lines 75-77 explaining REST vs GraphQL login is justified, but is the only comment of its kind in the SKILL.md being edited

**Severity:** P4
**Where:** spec.md lines 75-77 (P0 edit Design section), proposing a `Note:` block immediately above the jq fence at SKILL.md:~241
**Convention violated:** None established in this repo's CLAUDE.md. The user's round-2 framing references a "Default to writing no comments. Only add one when the WHY is non-obvious" rule "per CLAUDE.md" — that exact phrasing does NOT appear in `vigil-skills/CLAUDE.md` (the file has no comment-style section across all 78 lines). The convention exists informally in some Claude system prompts and downstream projects, but is not a rule of THIS repo.
**Evidence:** Grep of `vigil-skills/CLAUDE.md` for "no comments", "non-obvious", "WHY" returns no matches. CLAUDE.md content stops at line 78 and covers sync commands, architecture, file layout, and conventions for skills/agents — but says nothing about prose comment style inside SKILL.md.
**Suggested fix:** None required. The WHY is genuinely non-obvious — REST/GraphQL bot-login parity is the exact bug being fixed, and a future "helpful" edit that adds the suffix back is the precise regression this `Note:` prevents. Round 1 conventions lens already evaluated this and concluded the comment "does meet the 'WHY non-obvious' bar." Round-2 disposition is the same. Optional micro-edit if the spec author wants to be more terse: shorten to one line per Round 1's F-2 suggested fix — but the longer form is also fine.

### F-3: Spec retains "cargo-cult code" phrase at Decision 1 — round-1 F-3 not addressed

**Severity:** P4
**Where:** spec.md line 29 (Decision 1)
**Convention violated:** Tone nit only. CLAUDE.md does not prohibit the phrase. Round-1 review flagged it as personal style; round-2 did not touch it.
**Evidence:** Spec line 29 still reads "adding `or "coderabbitai[bot]"` would be cargo-cult code".
**Suggested fix:** Optional. P4 nit; non-blocking. The decision itself is sound regardless of phrasing.

### F-4: No contradiction with prior wiki decisions

**Severity:** Informational
**Where:** N/A
**Convention violated:** None.
**Evidence:** Scanned `vigil-harbor-wiki/decisions/`. None of the 47 decision files reference `/review-pr`, GraphQL author filtering, polling cadence, or any pattern this spec touches. The closest related entries are about Plane MCP and wiki maintenance, both orthogonal. No supersession is being claimed or required.

### F-5: Silent spec additions check — clean

**Severity:** Informational
**Where:** Spec Decisions 1-4
**Convention violated:** None.
**Evidence:** Walking the four Decisions:
- Decision 1 (drop `[bot]` suffix, don't accept both forms): brief Decision 1 says "whether to also drop the suffix check entirely vs. accept both forms is the spec author's call" — category (c) spec-level addition with rationale, explicit. Authorized.
- Decision 2 (`--name-only` over `diffstat`): brief Decision 2 says "Spec author picks one with one-line rationale" — category (a) authorized by brief.
- Decision 3 (P2 doc rewrite, no sleeps): brief Decision 3 says "Pick the option that's cheaper to maintain — both are acceptable" — category (a) authorized by brief.
- Decision 4 (no restructuring): brief Decision 4 states the same. Category (a) authorized.
No silent (d)-category drift.

## Summary

P0: 0 | P1: 0 | P2: 0 | P3: 1 | P4: 2

## Closure table

| ID | Severity | Status | Evidence |
|----|----------|--------|----------|
| F-1 (R1) | P2 | PARTIAL → effectively closed | Spec line 159 dropped magic-number `= "6"`; remaining shape divergence (`test "$(...)"` wrapper) is structurally required for the `--stat = 0` absence assertion. Convergence with bare `grep -c` not possible. |
| F-2 (R1) | P3 | OPEN-as-acceptable | Comment text unchanged at spec 75-77; round-1 concluded the WHY-non-obvious bar is met. User's round-2 framing references a CLAUDE.md rule that does not exist in this repo's CLAUDE.md. Comment retained intentionally. |
| F-3 (R1) | P4 | OPEN | "cargo-cult code" phrase still at spec line 29. Pure tone nit, non-blocking. |
| F-4 (R1) | P4 | CLOSED | Test command (line 159) now uses `-ge` / `= "0"` form; no exact-count assertions. |
| F-5 (R1) | P4 | CLOSED | Spec line 135 now attributes "three similar lines" to `spec-reviewer-conventions` prompt, not CLAUDE.md. |
| F-6 (R1) | P4 | CLOSED (non-defect) | Wiki state.md update is post-merge `/wiki-after-merge` work, not in spec scope. |

STATUS: GREEN
