# Correctness Review — round 1

## Closure of round 0 findings

N/A — no closure predecessor.

## Findings

### F-1: Cycle-2 failure has conflicting irreversible outcomes
**Severity:** P0
**Where:** docs/specs/TODO/VHS-56.spec.md:155
**Claim:** “`irreversible` stops and writes nothing for those cases,” followed by “A cycle-2 dispatch failure records the completed cycle-1 reconciliation plus an open count and uses `completed at cap`.”
**Why this is wrong:** The second rule is unconditional and permits a completed outcome after dispatch failure, whereas the preceding rule, Test plan item 4 at line 238, and Done when at line 260 require irreversible dispatch failures to halt. For example, an irreversible run folds a cycle-1 finding, then cycle 2 times out: the spec supplies both a halt and a completed result. Design 6 at line 209 also allows previously completed results to survive a tier change, so a failed-cycle result obtained under `big` could later bypass the irreversible failure posture.
**Suggested fix:** Restrict the cycle-2 failure continuation to `small` and `big`; explicitly halt irreversible runs on failure of either cycle. Define whether a result containing a failed dispatch qualifies for reuse when changing to irreversible, consistently with the stated failure rule.

### F-2: Adding a decision under no-grill leaves the previous review valid
**Severity:** P1
**Where:** docs/specs/TODO/VHS-56.spec.md:209
**Claim:** “Revising an interview answer invalidates the prior doubt result … after the resumed interview returns, Phase 3 runs again from cycle 1.”
**Why this is wrong:** The retained Confirm menu has another content-changing path: under `--no-grill`, option 2 appends an operator decision rather than resuming an interview (`skills/spec-brief/SKILL.md:184`). The spec only invalidates results after revising an interview answer. Following that rule permits a completed doubt pass, an added decision during Confirm, and a write carrying the earlier completed outcome without challenging the new decision. This misses the brief’s Decision 3 requirement that the challenged draft be the artifact presented for confirmation.
**Suggested fix:** Explicitly invalidate the result after `--no-grill` option 2 adds a decision. Re-render the candidate and return to Phase 3 from cycle 1, applying the tier policy before presenting Confirm again. Add this path to Test plan item 8.

### F-3: ground-truth ledger omits runtime claims
**Severity:** P2
**Where:** spec § 2. Render the candidate draft once the interview path ends; spec § 6. Renumber Confirm and Write and make the outcome visible
**Claim:** “Under `--no-grill`, it uses the existing ticket-only decision derivation”; “keeps the existing atomic write.”
**Why this is wrong:** The ledger declares `New spec: rows cover every section.`, but neither section has a row covering these existing-behavior claims. The underlying claims are supported by `skills/spec-brief/SKILL.md:184` and `skills/spec-brief/SKILL.md:218`; this is an evidence-ledger omission, not unsupported behavior. The atomic-write rows currently name Goal and Current behavior, while Design 6’s row covers only the menu.
**Suggested fix:** Add rows naming these sections and their live anchors.

### F-4: ticket not cached
**Severity:** P3
**Where:** spec § Done when
**Claim:** The spec implements the narrowed VHS-56 brief.
**Why this is wrong:** Canonical ticket verification could not be completed. The required shared-memory lookup with namespace `skills`, tags `plane_work_item` and `VHS-56`, and source system `plane` returned: `Access denied: agent 'codex' lacks 'read' on namespace 'skills'`. Review therefore used the brief, including its explicit split into VHS-56, VHS-66, and VHS-67.
**Suggested fix:** No speculative scope change. Verify against the ticket when an authorized read is available.

## Summary

P0: 1 | P1: 1 | P2: 1 | P3: 1 | P4: 0

Ground-truth rows 1, 2, 5, 9, and 10 were sampled against freshly opened sources; their claims are supported. No Deferred section is present. The cross-section walk found the conflicting failure transition and the omitted Confirm mutation path above.

The touched files changed within the last seven days, including `5f640d0` (stakes tiers, October 11) and `33b9215` (ground-truth gate, October 13). This review used their current on-disk state.

STATUS: RED P0=1 P1=1 P2=1 P3=1 P4=0
