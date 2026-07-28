# Correctness Review — VHS-8 Round 1

## Findings

### F-1 (P0): `--force` flag declared but not implemented in phases

Decision 4 introduces a `--force` flag ("force full-retire even when ticket isn't completed") but neither Phase 0 step 7 nor Phase 1 step 4 of spec-retire reference or handle it. The flag is also not in the brief — it's a silent addition.

**Fix:** Either implement `--force` in the Phase descriptions (step 7 parse, step 4 mode logic) or remove it from Decision 4 entirely. Since it's not in the brief and adds complexity, removal is cleaner.

### F-2 (P1): spec-reconcile warn-and-proceed contradicts brief's warn-and-halt

Brief says: "Warn-and-halt if ticket is not in a completed state." Spec Phase 0 step 5 says: "Proceed anyway — reconciliation is read-only, so running it on an in-progress ticket is safe (just unusual)." This directly contradicts the brief without a Decision justifying the departure.

**Fix:** Either implement halt (matching the brief) or add a Decision explaining why proceed is better. The brief is explicit — a Decision is needed to override it.

### F-3 (P2): Reconciliation filename mismatch with brief

Brief's Risks section recommends `<TICKET-ID>.reconciliation.md`. Spec uses `<TICKET-ID>.reconcile.md` throughout. Minor inconsistency but could confuse users referencing the brief.

### F-4 (P1): CLAUDE.md update doesn't address stale heading and intro

The spec says to extend "Workflow: spec-cycle -> ship-spec" but doesn't rename the heading or update the intro paragraph that says "The two main skills form a split pipeline." With 4 skills, both the heading and intro text become inaccurate.

**Fix:** Update the CLAUDE.md change instructions to rename the heading (e.g., "Workflow: spec lifecycle") and fix the intro paragraph.

### F-5 (P2): `completed_at` field not guaranteed on Plane tickets

Phase 2b step 4 says "The ship date comes from the Plane ticket's `completed_at`." This field may be null or missing for tickets completed before Plane tracked it. No fallback specified.

### F-6 (P2): Reconciliation report path assumes TODO/ location

Phase 3 writes to `docs/specs/TODO/<TICKET-ID>.reconcile.md` but Phase 0 step 1 accepts specs from `docs/specs/DONE/<TICKET-ID>/spec.md`. If input is a DONE/ spec, the report path should be `DONE/<TICKET-ID>/reconciliation.md`, not `TODO/`.

### F-7 (P2): "Wait -- actually" stream-of-consciousness in Phase 4

Phase 4 contains "Wait — actually, this creates a cross-repo problem..." This reads as authoring process rather than spec content. The cross-repo handling is good but should be presented as a clean design decision.

### F-8 (P2): ship-spec comparison claim in Phase 4

Phase 4 says "This matches ship-spec's approach where the skill makes changes but the user controls the commit." ship-spec actually does commit and create PRs. Inaccurate comparison.

### F-9 (P3): Missing "Invoked as:" convention line

Existing skills (spec-cycle, ship-spec) begin with an "Invoked as:" line showing usage syntax. Both new skills omit this.

### F-10 (P3): Ticket ID parsing rule not specified

Both skills extract `ticket_id` from the spec path but don't specify the parsing rule (e.g., filename stem before `.spec.md`, uppercase). Edge cases: nested paths, lowercase input.

## Closure Table

(Round 1 — no prior findings to close.)

STATUS: RED P0=1 P1=2 P2=5 P3=2
