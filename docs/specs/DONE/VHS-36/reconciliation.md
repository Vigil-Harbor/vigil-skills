# Reconciliation Report: VHS-36

> Date: 2026-09-07
> Spec: docs/specs/TODO/VHS-36.spec.md
> Merge: PR #28, commit ea5c2b0
> Plane state: Done (group: completed)

## Summary

All four spec-scoped files changed as specified. Every decision confirmed in shipped code. No unexpected files, no dropped files. The spec's one stated departure from the brief (D4's batch-cap bound replacing the brief's per-round-rendered bound) ships as designed.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/grilling/SKILL.md` | Yes | 8 bold-lead paragraphs in § Fact-finding (Designs 1–6); § Termination stop exception (D7); F-item hand-off line qualifier + `claim:` (D8); § What this skill never does (D9); § Failure modes 5th bullet + stop amendment (D10). 25+/4−. |
| `skills/spec-brief/SKILL.md` | Yes | `:140` gains the unverified-claim qualifier form (D11). 2+/1−. |
| `skills/grill-me/SKILL.md` | Yes | Fourth failure-mode bullet naming the degradation (D12). 1+. |
| `docs/spec-workflow-reference.md` | Yes | `:31` claim rule; `:35` labelled-claim paraphrase (D13). 4+/2−. |

Unexpected files in diff (not in spec):
- _(none)_

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| D1 | Operator-supplied fact is a claim to check | Confirmed | `skills/grilling/SKILL.md:80` — 'the answer is a **claim**, not an established fact' |
| D2 | Unverifiable claims stay open; `source: operator` never legal | Confirmed | `skills/grilling/SKILL.md:159` — 'records an operator's claim as an established fact; writes `source: operator`' in § Never does |
| D3 | Non-repo-checkable claims stay Open; no new source class | Confirmed | `skills/grilling/SKILL.md:89` — 'no check is dispatched, and the claim is Open' for no-repo-footprint; `skills/grill-me/SKILL.md:23` — fourth bullet |
| D4 | Check runs at once; batch-cap bound (spec departs from brief's per-round-rendered bound) | Confirmed | `skills/grilling/SKILL.md:82` — 'one parallel batch, capped at `question_cap` dispatches' with hard truncation |
| D5 | Failed check never retried; operator never re-asked | Confirmed | `skills/grilling/SKILL.md:87` — 'A failed check is not retried and the operator is not re-asked' |
| D6 | Two outcomes (confirmed / not confirmed) | Confirmed | `skills/grilling/SKILL.md:84` — 'A check confirms the claim or it does not'; contrary evidence gets a fresh `F<n>` |
| D7 | Third reason value; precedence over `stopped` | Confirmed | `skills/grilling/SKILL.md:141` — reason set `<fact not established \| fact not established (operator claim, unverified) \| stopped>`; `:123` — stop exception and precedence sentence |
| D8 | Brief carries claim text, labelled | Confirmed | `skills/spec-brief/SKILL.md:140` — `operator claims "<answer>", unverified; spec author pins this` |
| D9 | Open claims carry over un-redispatched | Confirmed | `skills/grilling/SKILL.md:91` — 'every Open `F<n>` item carries over as Open … and is not re-dispatched' |
| D10 | Blocked question renders anyway once claim resolves | Confirmed | `skills/grilling/SKILL.md:90` — 'the question waiting on it enters the next round's frontier' |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Primitive states verification rule, unverifiable-claim rule, dispatch rules | Met | `skills/grilling/SKILL.md:80–91` — 8 paragraphs cover all three |
| 2 | `/spec-brief` Phase 4 maps; `/grill-me` names degradation | Met | `skills/spec-brief/SKILL.md:140`; `skills/grill-me/SKILL.md:23` |
| 3 | `lint.py --strict` 0 ERROR; `sync.py` clean/round-trips | Unverifiable | PR-time gate; commit message records 17-row checklist green |
| 4 | PR #26 thread 3945500860 closable | Unverifiable | External GitHub thread status |

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| 17-row review checklist (prose-only spec) | Yes | Recorded in PR #28 body; no automated test file (N/A — doc-only) |

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- **Decision: operator claims are verified read-only, never trusted** — the core trust-boundary principle: an operator's answer is a claim checked by a read-only exploration, never an established fact; `source: operator` is prohibited. This adopts what VHS-33's wiki decision recorded as rejected-for-now (§ 3 "a cause qualifier on the F-item text"), and narrows the VHS-33 invariant that "no dispatch is ever active at `stop`" (a check fired on the stopping round's answer *is* active). Three revisit-worthy items from one decision entry.
- **Comprehension: grilling gains claim-verification rules** — 8 paragraphs in § Fact-finding plus changes to § Termination, the hand-off block, § What this skill never does, § Failure modes; three consumer files updated. The trust model for operator-supplied information changes from "carried through unverified" to "checked read-only before it counts".

RECONCILED: yes DRIFT: 0
