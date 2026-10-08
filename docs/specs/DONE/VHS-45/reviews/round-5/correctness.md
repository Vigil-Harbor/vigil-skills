# Correctness Review — round 5

Delta-scoped: Decision 3, Decision 12, the Skill outline, Phases 0, 1, 3 and 4, the tracker-mode and filing checklist bullets, the two new Out of scope bullets, the Deferred (P2+) row, and Decision 11's removed sentence. Kept sections were checked only for cross-references into the rewrite.

The read-back and resume protocol is gone, and both round-4 correctness P0/P1 findings close with it. The rewrite leaves no P0 or P1. Three P2 cross-reference corrections remain.

## Closure of round 4 findings

Grounding: no commit in the last 7 days touches the files this spec edits (newest is `d4db373`, 2026-09-08). `skills/*/SKILL.md` is 11 files, so 12 after `spec-tickets`; `tests/test_lint.py` still asserts 8 (lines 50-55). `skills/spec-close/SKILL.md` line 340 carries the companion rule Phase 4 cites. The reference `to-tickets` skill was read: blockers first, native link else "Blocked by", no read-back, no resume, parent untouched. The spec has no `## Deferred — follow-up required` section, so there are no deferred rows to validate. `scale_lens` is off.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Slug identity still matches the raw fenced title, so text mode never keeps a child | CLOSED (by removal) | No slug match against stored titles remains. spec § Decision 12 lines 139-145: create-only, no find or compare of earlier children. § Skill outline line 157: no tracker response field is named. |
| correctness | F-2 (P1) | Native read-back takes `object.id`, but the relations list identifies the work item as `issue_id` | CLOSED (by removal) | spec § Decision 12 line 133: the skill does not read its writes back. Success is the write's own return (line 143, § Phase 4 line 214). |
| correctness | F-3 (P3) | ticket not cached | CLOSED | Not a spec defect. Re-filed as F-4 below. |
| edge-cases | F-1 (P0) | A fenced child title is "some other piece", so text mode creates another child | CLOSED (by removal) | Same root as correctness F-1. |
| edge-cases | F-2 (P1) | The official relation list has no top-level `blocked_by` | CLOSED (by removal) | Same root as correctness F-2. No relation read remains. |
| edge-cases | F-3 (P2) | A finished plane-proxy page still carries a cursor | CLOSED (by removal) | No paged match loop remains. The existing-work count is "a notice, not a census" and may be `unknown` (line 145). |
| edge-cases | F-4 (P4) | Plane ticket text was not readable | CLOSED | Not a spec defect. See F-4 below. |
| conventions | F-1 (P2) | The mode table still keys `text` off "not advertised" | CLOSED | spec § Decision 3 lines 42-43: `native` when it "offers an operation that creates a blocked-by relation"; `text` when "it offers no such relation operation". |
| conventions | F-2 (P3) | Drift-check — round-4 pins with rationale | CLOSED | Informational. The pinned response shapes are removed. |

## Findings

### F-1: Done when cites a Decision 3 rule that now lives in Decision 12, under a mechanism that no longer exists
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:264 | spec § Done when, third bullet
**Claim:** "The approval block's unblocked set, and Decision 3's rule that create-before-edge is not a build order."
**Why this is wrong:** Decision 3 (lines 36-59) no longer states that rule. Its only sentence on order is line 55, "Filing blockers first (Decision 12) is what makes those identifiers exist." The rule is in Decision 12, line 139: "This order exists so that identifiers exist. It is not a build order, it is not written into any ticket". "Create-before-edge" also names the old shape (all children, then all edges). The rewrite files one piece at a time, each with its own relations. The Done-when bullet is still satisfied; only its pointer is stale.
**Suggested fix:** Change the clause to "Decision 12's rule that the blockers-first filing order is not a build order."

### F-2: Phase 1 limits the existing-work read to tracker modes, but Decision 12 and the approval block need it on `local`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:167 | spec § Phase 1 — Storage probe
**Claim:** "On a tracker mode it also resolves the parent and makes the one existing-work read (Decision 12)."
**Why this is wrong:** Decision 12 line 145 gives the read a `local` form: "the parent's children when the integration can list them, or the files matching `docs/specs/TODO/<PARENT-ID>.ticket-*.md`". The approval block (line 184) prints "n local ticket files", and the checklist (line 245) expects "the count of existing children or local ticket files". An implementer who writes Phase 1 from line 167 alone skips the read on `local` and has nothing to print. Decision 12 settles it for a careful reader, so this is a clarity fix.
**Suggested fix:** Split the sentence: "On a tracker mode it also resolves the parent. On every mode except `halt` it makes the one existing-work read (Decision 12)."

### F-3: Decision 10's AGENTS.md sentence says the skill "otherwise writes local files", which Decision 3 forbids
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:107 | spec § Decision 10, first bullet (kept section; cross-reference into rewritten Decision 3)
**Claim:** "It uses the tracker when the Decision 3 probe succeeds, and otherwise writes local files."
**Why this is wrong:** Decision 3 line 47 says "`halt` is not `local`", and line 59 says a tracker error "does not fall back to local files". A probe that fails on a connected tracker halts. Local files are written only when no integration is connected (line 44). The sentence as written would put a false description into `AGENTS.md`. The README bullet on line 108 already has the right wording.
**Suggested fix:** Replace with: "It uses the tracker when one is connected and the Decision 3 probe succeeds, writes local files only when no issue-tracker integration is connected, and halts otherwise."

### F-4: ticket not cached
**Severity:** P3
**Where:** spec § Goal
**Claim:** The spec implements Plane ticket VHS-45.
**Why this is wrong:** `memory_search` on namespace `plane` with tags `plane_work_item`, `VHS-45` returned "Access denied: agent 'claude' lacks 'read' on namespace 'plane'". The review used the brief, which says its Done when is transcribed from the ticket.
**Suggested fix:** None in the spec.

## Checked and clean

- Done when, all four bullets, still map: Phases 0-4 (line 262); `native`/`text` children with relations or a `Blocked by` relation list (263); the unblocked set (264, pointer per F-1); Decision 4 plus the Assembly paragraph (265).
- No residue of the removed protocol in any section: no read-back, unwrap, slug match, temp file, or atomic rename. `states.json` appears only as a leave-alone path and as "does not read" (line 137).
- Option-1 omission agrees across Decision 5, Decision 12 line 147, Phase 3 line 202, and checklist line 246.
- The Storage grammar agrees between Decision 3 line 51 and the Phase 3 block line 182.
- The failure stop agrees across Decision 12 line 143, Phase 4 lines 210 and 214, checklist line 244, and the Deferred (P2+) row.
- The never-does list (line 159) matches Decision 12's create-only and no-resume rules and the two new Out of scope bullets (lines 275-276).
- Brief constraints hold: no edit to `skills/ship-spec/SKILL.md`, no plane-proxy relation tool (line 149).

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 1 | P4: 0

STATUS: GREEN
