# VHS-109: separate simplification from behavior changes

Decision recorded 2026-11-03. Owner: Devin, repository operator. Scope: the VHS-96 / PR #66 design follow-up; no helper implementation is planned by this decision.

## Decision and effective scope

Retain the corrected prose for review selection and body extraction in the local PR #66 candidate, `13d60fdd9854f95da9489bf5070ce1182c70dbba`. Keep the existing tested marker helper. The evidence supports the bounded corrections; it does not establish autonomous reliability or that every source of review churn has disappeared.

VHS-90 prescribed a small-tier cut list and restricted review-driven regrowth. VHS-96's brief deliberately absorbed VHS-41 body findings, VHS-89 marker reporting, and VHS-102 same-head upgrades. Its decisions raised the target to about 2,400 words with a 2,800-word guardrail, and explicitly excluded `cr_poll.py` and scripted queries. The November 2 handoff records those choices as settled with Devin. Its `big` tier is explicit in the brief, spec, and verdict. The inspected ticket, brief, review snapshots, handoffs, and wiki decisions contain no explicit rationale reconciling that tier with the parent's `small` direction.

Treat VHS-96 as the recorded mixed-scope, big-tier task. Preserve its accepted additions and word budget; do not retroactively call them unauthorized or rewrite the historical tier. The missing reconciliation is a decision-record gap. A larger tier changes ceremony, not permission to add unrelated rules. The parent's anti-regrowth intent remains: preserve earned contracts, fix demonstrated harm, and defer speculative additions. Future exceptions should name the parent constraint and explain the scope, tier, and validation budget in the brief.

## What each kind of change must prove

| Classification | VHS-96 changes | Validation owed |
|---|---|---|
| Behavior-preserving compression | Remove repeated edge-case and polling explanations, consolidate CodeRabbit facts, remove harness-specific wording while preserving operations. | Compare old and new actions on representative inputs, including waits, stops, replies, and side effects; check cited cross-skill contracts. Word and phrase tests are structural checks only. |
| Existing-defect repair | Correct approved-HEAD reporting (VHS-89), old-head approval stops, acknowledgement versus verdict versus infrastructure selection, pagination, and later repairs to trusted dispositions, source ranges, pending requests, and inspection prerequisites. Some repair defects introduced by the new feature. | A reproducer showing the wrong prior outcome, the intended result, and neighboring cases that must stay unchanged. Exercise real helper/query code where available; label manual traces honestly. |
| New capability or intentional behavior change | Harvest body findings including nonempty COMMENTED reviews; persist keyed dispositions across runs; upgrade same-head marker tokens (VHS-102); move marker posting to the end/early stops; merge duplicate/already-fixed report categories into skip reasons. | Explicit acceptance criteria and validation budget, including supported layouts, trust, reruns, failed pushes, crashes, and report changes. New marker ranking needs executable upgrade/equal/weaker tests. These changes cannot claim equivalence merely because prose shrank. |

VHS-89 repairs an existing report; VHS-102 adds the persistence behavior needed to make that repair visible. Keep those obligations separate. Follow-up layout and author-filter fixes repair the added body/disposition capability rather than count as further compression.

The original spec's test plan had word/phrase checks, real marker tests, and manual body examples. It did not execute the prose workflow. VHS-106/107 and the combined pass supplied broader behavioral evidence: baseline scenarios, neighboring cases, and an integration case where moving a pending stop left an earlier recovery request unguarded. The final record has 35 current manual cases and four historical controls. Its comparator checks recorded judgments and fixture integrity, not an executing agent. Do not describe it as an autonomous success rate.

## Why keep prose now

The demonstrated selector ambiguity was treating several meanings of “latest review” as interchangeable. The candidate distinguishes finding sources, verdicts, infrastructure status, and completion of a pending request. Body failures involved omitted Follow-up layouts and source ranges; the current extraction rule names both. The recorded cases are consistent with these rules after correction.

A bounded pure helper could accept captured review/request JSON and return role-specific review IDs and pending status. If separately justified, a body extractor could return item keys, locations, and text for documented layouts. These would make selection/extraction executable against fixtures, but would not fix authorization, severity, request ordering, or push-before-disposition sequencing on their own.

Retaining prose has ongoing costs: manual scenario checks, layout updates, and interpretation variance across models. A helper adds a maintained input/output contract, parsing code, failure handling, fixture updates, installation and cross-platform checks, and integration prose that must remain consistent. Shorter instructions alone do not establish lower total cost. The current evidence does not justify that implementation cost for this patch.

Devin owns reconsideration when a concrete case shows ambiguity or repeated execution divergence that a bounded helper would remove. Keep rationale and owner in the existing review summary; create a ticket when separate work is planned. No speculative helper ticket or extra review gate is required now.

Any future helper proposal must amend the brief's explicit prose-query exclusion and obtain scope approval. Keep it Python 3.8+ stdlib under the existing `skills/review-pr/` folder, with no hardcoded machine paths or new service. `sync.py` already mirrors files recursively there; verify adapter packaging and invocation on supported harnesses rather than infer parity from sync. Promote relevant sanitized fixtures into tracked executable tests: acknowledgements, empty approvals, ordering/ties, pagination, pending requests, legacy/Follow-up bodies, ranges, fallback keys, and repeated prompt blocks. Test the actual helper and its integration; expected/observed records alone are insufficient. No general polling or parser framework follows from this decision.

## Evidence boundary

Live Plane VHS-90, VHS-96, and VHS-109 were read on 2026-11-03. Local/gitignored evidence in the primary checkout: `docs/specs/TODO/VHS-96.brief.md` (Decisions, Tier, Out of scope); `VHS-96.spec.md` (Test plan); `VHS-106.replay/README.md`; and `VHS-96.unified/{assessment.md,validation.json,check.py}`. Historical operator decisions: `.claude/handoffs/2026-11-02-201032-vhs-96-pr66-in-review.md`. Wiki context: the VHS-94 fold-policy and VHS-95 word-floor decisions dated October 30–31. These are bounded inspected sources, not a claim to have searched every private transcript.

The decision evaluates the local candidate above, not a newly published or approved PR head. VHS-109 changes documentation only. Its reusable rule is in [Authoring Portable Skills](authoring-portable-skills.md#simplifying-an-existing-skill).
