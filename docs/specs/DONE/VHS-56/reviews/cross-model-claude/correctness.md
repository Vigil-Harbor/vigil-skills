# Correctness Review — round 4

> Cross-model round (Claude reviewer agents) over the round-3 green spec, run outside the `/spec-cycle` loop on 2026-10-13. Persisted by hand from the agent's hand-back text; not a `round-<C>/` directory.

## Closure of round 3 findings
N/A: no closure predecessor. This is the first pass of a full invocation, and no closure_manifest was supplied.

## Findings

### F-1: Reconciliation edits have no defined home, so re-rendering or a revise can silently drop folds and operator replacements
**Severity:** P1
**Where:** spec § Decision 1; § Design 2; § Design 5; § Design 6; and the interaction with § Decision 7 and § Decision 8
**Claim:** Decision 1: "Phase 3 renders the exact candidate brief that Phase 5 would write". Design 2: "Define a 'candidate brief renderer' … by pointing Phase 3 to Phase 5's mapping and Scale-emission rules … The candidate is re-rendered after every reconciliation edit". Design 5: "apply fact/anchor edits, run the operator contradiction batch … If cycle 1 changed the candidate, render it again". Decision 8 lets the operator "replace" an acceptance statement in `## Done when`.
**Why this is wrong:** The renderer is defined as Phase 5's mapping rules applied to the Grill summary, the ticket text and the grounding facts. Those mapping rules transcribe `## Problem`, `## Why it matters` and `## Done when` "from the ticket text … never inferred" (`skills/spec-brief/SKILL.md:224`). They also take Decisions and Risks from the summary's Settled and Open lists (`:227-228`). The spec never says where a reconciliation result is stored so that the next render keeps it. That covers a folded fact, an operator's keep/replace/reopen answer, and a premise moved into Risks. Three things follow:
1. If reconciliation edits only the rendered text, the "re-render" in Design 2 and Design 5 re-derives the draft from unchanged inputs and throws the edits away. Cycle 2 and Confirm then see the pre-fold draft, while the outcome still says "folded n".
2. An operator "replace" of a `## Done when` item (Decision 8), or a fold that corrects a false premise in `## Problem`, cannot survive a re-transcription from the ticket. It contradicts the `:224` mapping rule, and the spec does not amend that rule.
3. Confirm option 2 re-invokes `grilling` "with the Grill summary as `prior_summary`" (`:182`). Design 6 says revising invalidates the doubt result and reruns Phase 3 from cycle 1. It does not say whether the operator's earlier contradiction-batch answers are carried into that summary. If they are not, the operator's replacement of a settled decision is silently reverted in the written brief unless the fresh reviewer happens to raise it again. That is the inverse of the brief's Decision 4: an operator decision changed without the operator seeing it.

Design 6 says "Phase 5 adds the `## Doubt pass` emission … and keeps the existing atomic write". It does not say that Phase 5 writes the confirmed candidate verbatim rather than re-applying the mapping rules.
**Suggested fix:** Pin a single source of truth, either of these:
- **(a)** The held candidate text is authoritative after the first render. Reconciliation edits that text in place, "re-render" means re-checking consistency rather than re-deriving, and Phase 5 writes the confirmed candidate plus `## Doubt pass` without re-running the mapping.
- **(b)** Reconciliation writes into the renderer inputs: folds go to the facts and References inputs, and operator answers go to the held Settled and Open lists that are also passed as `prior_summary` on a revise.

Either way, state which sections a fold may edit. Add an explicit exception to the `:224` transcription rule for a verified fold or an operator replacement in `## Problem`, `## Why it matters` or `## Done when`, or route those to `## Risks / decisions`. Also state whether contradiction-batch answers survive Confirm option 2.

### F-2: The "host cannot wait" branches are unreachable because the tier gate already stops a non-waiting host
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3; § Decision 4 (normalized reasons); § Design 1 (`can_wait`); § Test plan items 3 and 4
**Claim:** Decision 3 says: "Use the same host-capability test as the existing tier gate, which stops when the host cannot wait". It goes on: "`small` … On a host that cannot wait, keep the skip without prompting." and "`big`: … on a host that cannot wait, announce and record `skipped — host cannot wait`."
**Why this is wrong:** The tier gate runs in every mode before the interview. On a host that cannot wait it prints `tier needs an operator — stopping` and writes nothing (`skills/spec-brief/SKILL.md:92`, `:94`). Confirm also waits (`:178`). So every run that reaches Phase 3 has already passed the same wait test with "can wait". No written brief can carry `host cannot wait`, and test plan item 3 ("headless … failures are announced and recorded") cannot be exercised. The irreversible no-wait halt in Done when is already met by the existing tier gate. This produces dead prose, not broken behavior. But it tells the implementer and the mirrored docs that a headless run writes a brief with a skip record, which it never does.
**Suggested fix:** State that `can_wait` is always true at Phase 3, because the tier gate already stopped any host that cannot wait. Then either drop the `host cannot wait` reason and its small/big branches, or keep them explicitly as defensive. Amend test plan items 3 and 4 so the no-wait case is checked at the tier gate.

### F-3: The reviewer payload omits `wiki_root`, yet the reviewer is told to verify anchors and may open wiki files
**Severity:** P2
**Where:** spec § Design 4
**Claim:** "Each dispatch prompt contains only: … `project_root` for live read-only verification …" and "It may open repository and wiki files for evidence".
**Why this is wrong:** Briefs routinely cite wiki paths outside `project_root`. This brief cites `vigil-harbor-wiki/overview/2026-10-11-skill-pack-distillation.md:45`, and grounding reads `<wiki_root>/projects/<slug>/state.md` (`skills/spec-brief/SKILL.md:76`). `wiki_root` is resolved in Phase 0 (`:34`), but the "contains only" list excludes it. A fresh reviewer therefore cannot reliably find the wiki to check the "stale or unsupported anchors" it is told to challenge.
**Suggested fix:** Add `wiki_root` (or `none`) to the Design 4 payload list.

### F-4: Which skip reason applies to `small` with no eligible reviewer is not pinned
**Severity:** P3
**Where:** spec § Decision 3; § Decision 12; § Design 3
**Claim:** Design 3 says the small override is "shown only when the host can wait and an eligible reviewer exists. Declining or being unable to wait keeps the normalized tier-small skip." Decision 12 says "`small` and `big` may record an announced skip when no eligible reviewer exists".
**Why this is wrong:** For `small` with no eligible reviewer, both `tier small; operator did not request the pass` and `no eligible cross-model reviewer` fit the text. Test plan item 9 only requires that some normalized reason appears.
**Suggested fix:** Name the reason for that case in Design 3.

### F-5: How outcome counts aggregate over two cycles, and the summary-line wording, are not stated
**Severity:** P3
**Where:** spec § Decision 4; § Design 6
**Claim:** The record says `**Outcome:** folded <n> …; operator resolved <n> …; rejected <n>; open <n>` with `**Status:** completed | …`. The Confirm line says `completed in N cycle(s)`.
**Why this is wrong:** The spec does not say whether the counts sum across cycles 1 and 2 or cover only the last cycle. The summary-line token `completed in N cycle(s)` also differs from the record's `completed`, so the two need an explicit mapping.
**Suggested fix:** State "counts are summed across all reconciled cycles". Note that the summary line's `completed in N cycle(s)` corresponds to `**Status:** completed` with `**Cycles:** N`.

### F-6: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Not applicable; this is a process note.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `["plane_work_item","VHS-56"]` returned `Access denied: agent 'claude' lacks 'read' on namespace 'skills'`. The review used the brief as the local source of truth, as instructed. The brief's Origin paragraph records the operator's split into VHS-56, VHS-66 and VHS-67.
**Suggested fix:** None for the spec.

## Grounding notes (no finding)
- Every `skills/spec-brief/SKILL.md` anchor in § Goal, § Current behavior, § Decisions and § Design resolves to the described text: `:5`, `:9`, `:90`, `:94`, `:160`, `:162`, `:166`, `:168`, `:170`, `:176`, `:180`, `:184`, `:186`, `:188`, `:202`, `:205`, `:218`, `:254`, `:256`.
- `skills/spec-cycle/SKILL.md:1065/1067/1070` is the heading-keyed brief parse. The tier reader's section body ends at the next heading (`:351`), so a new `## Doubt pass` after `## Tier`/`## Scale` does not disturb it.
- `README.md:9`, `:65` and `AGENTS.md:25` are as described.
- `lint.py:44` is the "Controlled vocabulary" comment, with `REQUIRES_KEYS` at `:45`. The citation pair still covers the symbol, so this is not drift.
- Nothing outside spec-brief and the three docs references spec-brief's phase numbers, so renumbering does not touch `grilling` or `spec-cycle`.
- Baseline commit (all rounds) equals HEAD `7c2dfa0`. The three 2026-10-13 commits touching README, AGENTS and the workflow reference (`33b9215`, `fad52c7`, `f64bebe`) predate the baseline, so there is no drift.
- Done-when mapping: item 1 maps to Decisions 3 and 4, item 2 to Decision 8, item 3 to Decisions 3 and 12 plus Design 6, and item 4 to § Test command. All are mapped.
- Ground-truth check: `docs/specs/TODO/VHS-56.reviews/round-3/ground-truth-ledger.md` has 4 rows, and all were checked. Each spec sentence carries its own anchor, and the live code at `:184`, `:170`/`:176`, `:184` and `:218` supports the claim. No runtime claim in the Design 2 or Design 6 bodies lacks a row.

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 3 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=3 P4=0
