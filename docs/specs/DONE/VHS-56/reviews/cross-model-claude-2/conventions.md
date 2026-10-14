# Conventions Review — round 5

> Second cross-model round (Claude reviewer agents), delta over the Codex fold of the first Claude round, run outside the `/spec-cycle` loop on 2026-10-13. Persisted by hand from the agent's hand-back text; not a `round-<C>/` directory.

> A cross-model check (a Claude reviewer) of the Codex fold of the six P2s from the earlier Claude round. It also checks the round-4 post-green polish to Design 6 and Test plan 14, which no reviewer had seen. Mode: delta. The fold diff covers 15 hunks. I read the whole spec for context.

**What I read.** The spec at `docs/specs/TODO/VHS-56.spec.md` (318 lines), the fold diff, the brief, `AGENTS.md`, `docs/authoring-portable-skills.md`, `skills/spec-brief/SKILL.md`, `skills/grilling/SKILL.md` (lines 1–24 and 136–151), the spec-cycle § 2g rules, the reference (lines 1–30, 98–104, 144–154 and 244–248), README lines 7–11 and 60–68, and `lint.py:43-46`.

From the wiki I read the `state.md` header and these decisions: VHS-55 (stakes tier), VHS-26 (author-side ground-truth gate), PET-184 (cross-model checkpoint) and CROSS (Codex review gate).

I also read the installed `codex` skill, because it is the operator's real cross-model mechanism and the test case for fork (1).

**Anchors.** I re-checked every `path:line` in the spec against the live files. All of them resolve except one, `:182` (see F-7).

**Verdict file.** The fingerprint in `verdict.md` matches the current post-polish bytes.

**Deferred sections.** The spec has no `## Deferred — follow-up required` section, only `## Deferred (P2+)`, so the routing checks do not apply.

**Shared memory.** Shared memory was not used: access to namespace `skills` was denied, so the brief was the source.

## Closure of round 4 findings
Predecessor: `docs/specs/TODO/VHS-56.reviews/cross-model-claude/conventions.md`. Each row was checked against the current spec, not against what the fold author says.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions | F-1 | The "host cannot wait" branch is unreachable | CLOSED | Decision 3 now says the gate repeats no wait test and holds no `can_wait` (spec:55). The `host cannot wait` reason is gone from spec:86. Design 1 has no `can_wait` (spec:185-187). The failure-mode bullet is removed (spec:248-255). Done when no longer says "no-wait" (spec:296). Test plan 4 tests the halt at the existing tier gate (spec:270). |
| conventions | F-2 | A second invalid reply discards the interview | CLOSED | Decision 9 re-prints the offer as often as needed, and only option 3 aborts (spec:128). The Decision 8 batch keeps valid answers, and only an explicit abort ends it (spec:115). The Decision 12 menu re-prints (spec:175). The Design 7 bullet is at spec:255. |
| conventions | F-3 | `small` adds a blocking stop | CLOSED | `small` announces the skip without waiting. Confirm option 5 appears only when a reviewer is eligible (spec:57, :203, :234). Test plan 2 covers this (spec:268). |
| conventions | F-4 | Per-tier tables not updated | CLOSED | The Scope rows now name § Stakes tier and the AGENTS Stakes tier paragraph (spec:23, :25). Design 8 names `docs/spec-workflow-reference.md:147`–`:152` and `AGENTS.md:35` and gives clauses for each tier (spec:259). |
| conventions | F-5 | No conforming route for a host whose own subagents cannot change family | PARTIAL | A route now exists: native, skill or shell mechanisms count, under `shell: true` (spec:92, :98, :261). But the evidence it requires ("an explicit family field") is undefined, and the operator's own bridge does not carry one. The rest is filed below as F-1, still at P2. |
| conventions | F-6 | Spec-level additions not flagged | CLOSED | The Decisions preamble lists seven flagged additions with reasons (spec:31-39). Design 6 repeats the flag on the full preview (spec:234). Done when has a parenthetical for completed records (spec:294). Item (iv), the extra status and flag, is gone. |
| conventions | F-7 | Collapse cycle-2 failure into `completed at cap` | CLOSED | There is one furthest-completed rule (spec:175-177), and a tier-only upgrade keeps the at-cap record (spec:236, :270). The closing text keeps review-history wording as instructions; that is filed as F-2 below. |
| conventions | F-8 | Reviewer prompt has no wiki path | CLOSED | Design 4 adds `wiki_root` and `project_slug` (spec:212). |
| conventions | F-9 (P4) | `**Status:**` label collision | CLOSED | The label is now `**Result:**` (spec:72, :82). Test plan 17 covers it (spec:283). |

Codex's round-4 report, checked for the post-green polish:

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| conventions (R4) | F-1 | Keep resolutions without a Q id out of the Grill summary grammar | CLOSED | The `(Q<n>)` grammar is kept: only items with a Q id amend `prior_summary`, and items without one go to the candidate and to `seed` (spec:238, :280). A new problem in how the hand-off works is filed as F-4. |
| conventions (R4) | F-2 | Flagged additions need drift-check attention (P3) | CLOSED (informational) | The seven labels are still present (spec:33-39). |

**The four operator forks.**
- **Fork 1** (a CLI or skill reviewer counts when it states its family and runs read-only, with no vendor named): implemented, but more strictly than decided. See F-1.
- **Fork 2** (one retry): implemented as decided (spec:170-175). The retry belongs to its cycle and adds no cycle.
- **Fork 3** (`small` asks through a Confirm option): implemented as decided (spec:57, :203).
- **Fork 4** (full preview and completed-pass record): both are kept and flagged (spec:33-34, :234, :294).

**Portability.** No vendor, tool or model slug appears in normative text. The `requires` block is unchanged, and both dispatch routes rely on keys already declared. Tagging the operator's own route as a harness example would be acceptable.

## Findings

### F-1: Decision 5 asks for an "explicit family field" that is not defined, and no mechanism has one
**Severity:** P2
**Where:** spec § Decision 5 (spec:92); README requirement clause in Design 8 (spec:261); Test plan 15 (spec:281)
**Convention violated:** Operator fork (1), "counts when it **states** its model family and runs read-only". Portability habits 1 and 4 (`docs/authoring-portable-skills.md:9`, `:21`). The repo's terms for agent classes (`skills/spec-brief/SKILL.md:78`, `README.md:65`).
**Evidence:**
- Decision 5 requires "an explicit family field in the mechanism's declared configuration or runtime metadata/output". It also says "Tool presence, a model display name or a vendor inference is insufficient evidence". The spec never says what a family field looks like.
- No mechanism in this ecosystem declares one:
  - Skill frontmatter in this repo has `name`, `description`, `user_invocable` and `requires` (`AGENTS.md:107`); agents have `name` and `description`.
  - The operator's installed `codex` skill states its family only in prose ("Drive OpenAI Codex CLI (GPT 5.6 models)", line 3) and names model ids (`gpt-5.6-terra`, line 30). It declares `--sandbox read-only` (line 39). It has no field.
- Read strictly, the bridge that fork (1) was settled for is ineligible. Then every `big` run records `no eligible cross-model reviewer`, and every `irreversible` run halts right after the tier gate (Design 1, spec:189). Two implementers would disagree on whether "GPT 5.6 models" is a "display name" or a family statement.
- A smaller wording drift: the existing pattern calls the narrowest native class "read-restricted" and notes that such classes "keep shell access even when file-edit tools are withheld" (`SKILL.md:78`). Decision 5 and Design 1 require "read-only evidence". That reads as stricter than the convention the spec cites.

**Suggested fix:** In Decision 5, replace the family-field clause with: "the mechanism itself states the model family it runs — in its own instructions or configuration, or in its runtime output (for example a provider or model line it prints). A family the author infers from the tool's name, rather than one the mechanism states, is insufficient." Keep the same-family, unknown and write-only exclusions. Use "the narrowest read-restricted agent class or a read-only sandbox mode" so the wording matches `SKILL.md:78`. Mirror the change in the README clause and in Test plan 15. Decision 5 sits in § Decisions, which § 2g may not edit, so make this fold in a normal revision.

### F-2: Decision 12 states spec-revision history as an instruction
**Severity:** P2
**Where:** spec § Decision 12, paragraph 2 (spec:177); Decisions preamble (spec:37)
**Convention violated:** Specs state the end state and do not carry removal notes (AGENTS.md conventions; the reviewer rule against comments that describe removed code). `/spec-close` turns spec text into wiki decisions, so review-process ids leak into durable records.
**Evidence:**
- spec:177 says: "Delete the cycle-2-failure status and `dispatch_failed` flag. … Deliberately adopt conventions F-7's simpler furthest-completed-state rule … This supersedes the prior spec's special restart rule …"
- Neither the status nor the flag exists in `skills/spec-brief/SKILL.md`; they were only in an earlier draft of this spec. An implementer running `/ship-spec` will read "Delete" as an edit to the skill and find nothing to delete.
- "conventions F-7" means nothing once the reviews are archived.

**Suggested fix:** Rewrite as the end state: "There is no separate cycle-2-failure result and no failure flag. A completed record means at least one cycle was reconciled; `completed at cap` discloses unfinished review. A tier-only change keeps any completed record, including at cap; only a skip is re-evaluated, because brief Decision 6 requires that a pass ran, and a failure while `irreversible` is active still cannot skip. Confirm shows the disclosure after such an upgrade." In the preamble bullet at spec:37, drop "rather than a new status and flag". This text is in § Decisions, so fold it in a normal revision rather than in § 2g.

### F-3: Decision 11's strict report grammar departs from the VHS-55 rule for outside reviewers without saying so, and it is more machinery than the pass needs
**Severity:** P2
**Where:** spec § Decision 11 (spec:163); its consumers § Decision 12 (spec:175) and Design 5 (spec:222); Test plan 16 (spec:282)
**Convention violated:** Wiki decision `2026-10-11-vhs-55-ceremony-follows-an-operator-set-stakes-tier.md` §4. It classifies an outside reviewer's return leniently on purpose: "readable findings anywhere mean the review ran; an affirmative clean statement from the reviewer is success with zero counts; everything else, including empty output with exit 0, is `failed`."
**Evidence:**
- Decision 11 treats all of these as dispatch failure:
  - a missing one of five per-finding fields;
  - a summary count, status count and block count that do not all match;
  - a duplicate id;
  - any count above `question_cap`.
- It also specifies a fence parser in prose (backtick or tilde runs, same character, closing marker at least as long) for a report that is never stored and that the author reads directly.
- The reviewer this pass targets is a model from another family, often reached over a CLI. It has never seen this grammar.
- With one retry per cycle (spec:175), two format slips by such a reviewer under `irreversible` leave only Abort. That discards the interview, although the review did run and returned readable findings.
- The flagged-additions bullet (spec:36) justifies the grammar as protecting "the mutation boundary". A report grammar does not protect a mutation boundary; the read-only dispatch does.
- Decision 10 already says "the caller owns classification", so a malformed finding block can be classified by the author like any other.

**Suggested fix:** Align with VHS-55 §4, or say why the stricter rule is needed. The minimal version:
- A return counts as failure only when it is empty, when the host reports an error or timeout, or when it has no readable finding blocks and no `STATUS: READY`.
- A block with missing fields is classified by the author under Decision 10, usually as noise or contract misread.
- Blocks past `question_cap` are rejected as over the bound and not reconciled.
- Drop the fence-parsing sentence and the three-way count equality.
- Update Test plan 16 to match.

This changes behaviour, so it is not a § 2g candidate.

### F-4: The post-green polish was a change of mechanism, not a clarification, and it depends on `seed` meanings that grilling does not define
**Severity:** P2
**Where:** spec § Design 6, paragraphs 3–4 (spec:238, :240); Test plan 14 (spec:280); § Post-green polish (spec:318)
**Convention violated:** Callers keep the `grilling` hand-off contract as written (`skills/grilling/SKILL.md:18`, `:21`, `:23`). The § 2g bound: "Apply each candidate only if it is a clarification … no behavior reversals, no new scope" (`skills/spec-cycle/SKILL.md`, § 2g step 3).
**Evidence:**
- The polish moved resolutions without a Q id from amended Settled items into "separately labelled operator-settled constraints in the existing `seed` context". That changes the transport, so it is a change of mechanism. This round is the first review it has had.
- Grilling defines `seed` as "the problem statement and any grounding facts already established" (`grilling/SKILL.md:18`). It gives "operator-settled constraint" no meaning. Its resume contract rebuilds the tree "from the summary" (`:23`) and says nothing about seed items being binding. So the resumed interview may ask a question again, or settle it differently, without knowing it was fixed.
- The resume call spec-brief makes today passes only `prior_summary` and the caps (`skills/spec-brief/SKILL.md:182`). A seed is not currently sent on resume, so "existing" overstates the current hand-off.
- The spec's safeguard says "only an explicit operator revision that names an affected constraint may reopen or replace it" (spec:240). It does not say what happens when a returned Settled item conflicts with a retained constraint that nobody named. The candidate could then hold two contradictory statements.

**Suggested fix:** Keep the grilling grammar as it is (the right call) and close the gap on the caller side:
1. Say that option 2's resume passes `seed` again, with the constraints written as established facts the interview must not re-decide. That fits grilling's own wording for `seed`.
2. Say that after the interview returns, any revised decision that conflicts with a named constraint goes to the operator through the Decision 8 prompt before Phase 3 runs again. This reuses machinery that already exists rather than adding a rule.

Mirror both points in Test plan 14.

### F-5: The Decisions preamble leaves Decisions 4 and 6 out of the list that pins the brief's Risks
**Severity:** P3
**Where:** spec § Decisions preamble (spec:31)
**Convention violated:** Drift-check legibility, the (a)/(c) classification of the spec against the brief.
**Evidence:**
- spec:31 says "Decisions 1–3, 5, 7–10 and the Design pin the brief's Risks / decisions 1–10."
- Decision 4 pins Risks 4 (the skip record), and Decision 6 pins Risks 6 (the capabilities).
- Decision 6 is in neither the pin list nor the additions list. A drift-checker reading the preamble cannot place it.

**Suggested fix:** Write: "Decisions 1–10 pin the brief's Risks / decisions 1–10 in order. Decision 4's completed-pass record, Decisions 11–12 and the positions below are spec-level additions."

### F-6: Flagged spec-level additions, and where the fold's extra machinery could be smaller
**Severity:** P3
**Where:** spec:33-39; § Decision 4 count paragraph (spec:88); § Decision 5 tie-break (spec:94)
**Convention violated:** None. These are class (c) additions, surfaced for the human drift check. The VHS-46 lesson applies: adding a menu or rule tends to draw the next finding.
**Evidence:**
- All seven listed additions have stated reasons. The fold also clears my earlier F-6 item (iv).
- The spec grew from 279 to 318 lines, mostly at three points:
  - Decision 11's grammar (F-3).
  - Decision 4's paragraph on counting by distinct root, which sets six rules for audit metadata that "has no downstream gate".
  - Decision 5's deterministic tie-break ("lexically first declared mechanism/model identifier").
- F-1 and F-2 above are clarity problems, not added machinery.

**Suggested fix:** Optional. Keep the completed record, which is settled as fork 4. Consider shortening Decision 4's count rules to: "counts are per distinct finding root across both cycles; a root's last disposition wins". Consider replacing the lexical tie-break with "prefer the mechanism the operator has configured or used most recently; otherwise ask". Neither change is needed to close a finding.

### F-7: An anchor in Design 6's renumber list does not hold
**Severity:** P4
**Where:** spec § Design 6, last paragraph (spec:242)
**Convention violated:** Anchor accuracy.
**Evidence:** The renumber list names `skills/spec-brief/SKILL.md:182` as one of "spec-brief's own phase references". That line (option 2's resume text) has no phase number. The live references to the renumbered phases are `:124`, `:180` and `:216`, plus the headings at `:166` and `:186`.
**Suggested fix:** Drop `:182` from the list, or name the headings `:166` and `:186` in its place.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 2 | P4: 1

**Fold verdict.**
- The fold closes my earlier F-1 through F-4 and F-6 through F-9. F-5 is only partly closed, and the rest is F-1 above.
- Forks 2, 3 and 4 are implemented as decided. Fork 1 is implemented more strictly than decided (F-1).
- The post-green polish fixed the grammar problem Codex raised, but it opened a gap in the hand-off (F-4) and goes beyond the clarification-only bound of § 2g.

**Least-machinery judgment.** Most of the growth is warranted: the held candidate, read-only eligibility, retry, and the reply grammar for settled decisions. The parts that are more than needed are Decision 11's strict parser (F-3), Decision 12's history text (F-2), and Decision 4's counting rules (F-6).

**Folding.** F-1 and F-2 edit § Decisions, and F-3 changes behaviour, so § 2g cannot carry them. They need a normal revision and a delta pass.

STATUS: GREEN
