# Conventions Review — round 1

## Closure of round <N-1> findings
N/A — round 1

## Findings

### F-1: Output-contract closure line is not an edit site
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Delta contract (the `closure_manifest` guard), and `# Output contract` in all four agents
**Convention violated:** Heading-scoped edits, and one closure rule. The spec changes when step 7 runs, but the agents' required report shape still keys off `round_number`.
**Evidence:** The spec says step 7 runs only when a `closure_manifest` was provided, and otherwise the section is `N/A — no closure predecessor`, including when `round_number` is greater than 1. Each agent's output contract still says `(Required for round_number ≥ 2; "N/A — round 1" otherwise.)` and calls that the exact shape. A full invocation whose first cumulative round is greater than 1 has no closure predecessor (Decision 13). The template would still require a closure table.
**Suggested fix:** Name `# Output contract` in all four agents as an edit site. Replace that parenthetical with: required when a `closure_manifest` was provided; otherwise `N/A — no closure predecessor`.

### F-2: Correctness anchor replacement leaves the old P1 rule in place
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Delta contract, anchor paragraph; `agents/spec-reviewer-correctness.md` critique lens
**Convention violated:** Decision 4's replacement of "every stale file:line anchor is a P1" is scoped to one sentence. The correctness lens states that rule twice, and the procedure around it still checks the cited line.
**Evidence:** The spec says to replace "the sentence that says stale file:line anchors are P1." In the correctness agent the critique lens has a **Stale anchors** bullet, then numbered item 2: "For every file:line anchor in the spec: re-grep the current code at that line and verify the symbol the spec references is actually there. Stale anchors are P1 (not P3 — they mislead the implementer)." Replacing only the last sentence leaves "re-grep at that line" and the bullet, so a moved line can still be filed as a P1. The other three agents only gain the new paragraph, so the four lenses would not apply one rule.
**Suggested fix:** In the correctness agent, replace both the **Stale anchors** bullet and numbered item 2 with the anchor paragraph. Do not leave a sentence that says every stale anchor is a P1.

### F-3: Decision 7 omits the Follow-up filter § Mode applies
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 7 and spec § Mode
**Convention violated:** The fingerprint rule already drops `**Follow-up:**` lines (`skills/spec-cycle/SKILL.md`, **The fingerprint**). Decision 7 states a narrower comparison than the design that "honors" it.
**Evidence:** Decision 7 says any difference after carriage-return removal selects full mode. § Mode also drops every line whose first non-blank characters are `**Follow-up:**`, and § Changed regions uses that same filter so a follow-up ticket id is not a spec change. A brief or spec that differs only on those lines is full under Decision 7 and not full under § Mode.
**Suggested fix:** In Decision 7, state the same two filters as § Mode: carriage-return removal and the `**Follow-up:**` line drop, and no other byte.

### F-4: Single-counter write-points and closure prose are not named as edit sites
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Two counters, spec § Docs; `skills/spec-cycle/SKILL.md` **Write points** and **Failure modes**; `docs/spec-workflow-reference.md` Phase 2 and Stakes tier
**Convention violated:** Heading-scoped edits. VHS-47's marker is "written at three points" (pending before round 1, red at the round-cap halt, green after polish), and the workflow reference still describes one `round` counter. The spec changes those facts but lists only the `round` token and a short Phase 2 insert.
**Evidence:** The skill's write-points paragraph says the marker is written pending at the start of Phase 2, red in 2f, green at the top of Phase 3, and "an interrupted run writes nothing more." The interrupted-run failure mode says nothing after the pending write is written. The workflow reference says "Round 2+ closure tracking" and, under Stakes tier, that `round == round_cap` is always the FROZEN/REWRITE rewrite. This spec skips the pending write on a no-op, writes round artifacts after pending, writes red at cumulative `C`, and gives a full invocation's first pass no closure predecessor even when `C > 1`. `AGENTS.md`'s spec-brief bullet still says the grill is "the halt that follows `round_cap` rounds"; § Docs only names the `/spec-cycle` lifecycle item.
**Suggested fix:** Name those headings. Write points: pending once per invocation before the first dispatch, not on a no-op; red at the halting pass's cumulative round; green after polish. Interrupted run: a partial `spec.copy.md` / `brief.copy.md` / `baseline.commit` set may remain, and the marker stays pending. In the workflow reference, say the Stakes-tier `round == round_cap` paragraph and the round-2+ closure paragraph describe the first invocation's pass index. In the `AGENTS.md` spec-brief bullet, say the grill also follows a delta halt at cumulative `C`.

### F-5: Invocation syntax is specified once and copied in three places
**Severity:** P3
**Where:** spec § Invocation; `skills/spec-cycle/SKILL.md` "Invoked as" and `## Attest mode`
**Convention violated:** The skill already keeps the usage line in more than one heading. § Invocation names "the invocation line" once.
**Evidence:** The H1 says `Invoked as: /spec-cycle <brief-path> [--attest "<reason>"]`. Attest mode halts with `Usage: /spec-cycle <brief-path> [--attest "<reason>"]`. § Docs already names the workflow-reference invocation and the `AGENTS.md` lifecycle item. The new exclusive `--full` form has to land on both skill copies or the attest halt still rejects a legal flag.
**Suggested fix:** Name both skill sites in § Invocation: the "Invoked as" line and the usage halt in `## Attest mode`.

### F-6: Mode row 9 is a spec-level addition to the brief's mode list
**Severity:** P3
**Where:** spec § Mode, row 9
**Convention violated:** Silent-addition axis, class (c). Brief Decision 14 lists the full-mode conditions and then says otherwise the mode is delta. It does not list "the next round directory already exists."
**Evidence:** The brief's list is `--full`, missing, unreadable, pending, attested green, brief changed, no baseline, ledger missing or unreadable. The spec adds row 9, `round-<candidate+1>/` already exists → `mode: full (round <candidate+1> already exists)`, and explains it as Decision 8's rule that a delta pass never overwrites an existing round directory.
**Suggested fix:** In Decision 14, add this row to the carried-forward list and point at Decision 8, so the mode table is not an unlisted extra.

### F-7: § 2b's sample disposition still cites a skill line
**Severity:** P3
**Where:** spec § Ledger; `skills/spec-cycle/SKILL.md` § 2b sample manifest
**Convention violated:** Decision 10 and the brief's portability pin: text that reaches the four agents, which install into other repos, must not cite a skill line. The ledger says its line shape is the shape § 2b already uses.
**Evidence:** The § 2b sample is `correctness/F-2 (P1) "stale anchor in § Design" — fixed: re-anchored to SKILL.md:142`. That block is what a later round receives as `closure_manifest`. The spec's own ledger example (`fixed: edited § Design`) does not use a line number, but it tells the implementer to keep § 2b's shape, sample included.
**Suggested fix:** When § 2b is edited for the saved ledger, change that sample to a section anchor (`fixed: re-anchored to § Design`) so the saved manifest does not teach a `SKILL.md` line citation.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 3 | P4: 0

STATUS: GREEN
