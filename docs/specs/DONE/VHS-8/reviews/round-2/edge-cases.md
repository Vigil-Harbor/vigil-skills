# Edge Cases Review — VHS-8 Round 2

## Closure Table

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | R1/F-1 | Large PR diff pre-fetch guard | CLOSED | Lines 123-124: `gh pr view --json` before full diff |
| edge-cases | R1/F-2 | `--force` flag no phase handling | CLOSED | Flag removed entirely |
| edge-cases | R1/F-3 | Plane not found defaults to full-retire | CLOSED | Line 381: defaults to partial-retire |
| edge-cases | R1/F-4 | Mixed tracked/untracked in reviews dir | CLOSED | Line 384: `git ls-files --error-unmatch` detection |
| edge-cases | R1/F-5 | DONE/ dir exists on retry | DEFERRED | Line 453 |
| edge-cases | R1/F-6 | Last-line parsing last non-blank | CLOSED | Line 227 |
| edge-cases | R1/F-7 | Concurrent wiki edits | CLOSED | Accepted risk |
| edge-cases | R1/F-8 | grep false positives | DEFERRED | Line 454 |

## Findings

### F-1 (P2): spec-reconcile allows `cancelled` but reconciliation needs shipped code

A cancelled ticket has no shipped code. Reconciliation will find nothing and produce a meaningless report. Should halt for cancelled tickets or produce an N/A report.

### F-2 (P2): spec-reconcile has no Plane-down fallback

If `list_states` or `retrieve_work_item_by_identifier` fails (network, Plane down), Phase 0 step 5 has no escape path. Should offer user override since reconciliation is read-only.

### F-3 (P2): `--partial` + completed ticket silently downgrades

User running `--partial` on a completed ticket loses full-retire functionality with no warning. Should warn when `--partial` overrides auto-detected full-retire.

### F-4 (P2): Companion file discovery unspecified for archive

Phase 4 says "any companions" but no glob pattern or discovery mechanism is defined. Suggest `<TICKET-ID>.*` glob.

### F-5 (P2): Reconciliation report lookup error message hardcodes TODO path

Phase 0 step 3 error message says "Run /spec-reconcile docs/specs/TODO/..." even when input was a DONE/ path. Should use actual `<spec-path>`.

### F-6 (P2): log.md idempotency grep too broad

`grep -F "<TICKET-ID>"` matches any mention. Should narrow to `grep -F "retire | <PROJECT> -- <TICKET-ID>:"`.

### F-7 (P2): Project prefix not in states.json leaves project_id undefined for step 5

Step 4 fallback only covers namespace. Without project_id, list_states cannot be called. Should skip step 5 entirely.

### F-8 (P2): issue_number should be parsed as integer

Plane API expects integer for `issue_identifier`. Spec extracts a string. Should specify type conversion.

### F-9 (P2): Archive step assumes spec in TODO/ but Phase 0 accepts DONE/

If spec is already in DONE/, `git mv` from TODO/ fails. Should detect and skip archive when already at destination.

STATUS: GREEN
