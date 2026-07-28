# Edge Cases Review — VHS-8 Round 1

## Findings

### F-1 (P2): Large PR diff pre-fetch guard

spec-reconcile Phase 1 step 2 mentions ">500 lines" threshold for diff summarization but doesn't specify how to detect line count before reading the full diff. `gh pr diff` streams the entire content. Suggest: use `gh pr view --json additions,deletions` first, sum them, and skip full diff read if total exceeds threshold.

### F-2 (P1): `--force` flag in Decision 4 has no phase-level handling

Same root issue as correctness F-1. Decision 4 declares `--force` for forcing full-retire on non-completed tickets, but no phase references it. If kept, it needs: Phase 0 arg parsing, Phase 1 mode override, and an explicit user confirmation gate (since --force bypasses the safety check).

### F-3 (P1): Plane ticket not found defaults to full-retire (risky)

spec-retire failure modes say: "Default to full-retire if the ticket can't be looked up." Full-retire writes wiki entries and updates state.md — the higher-blast-radius path. If Plane is unreachable, the safer default is partial-retire (archive only), since the user can always re-run with explicit mode once Plane is available.

### F-4 (P2): Mixed tracked/untracked files in reviews directory

Decision 5 handles tracked vs. untracked for spec files, but the `reviews/` directory is always untracked (created by spec-cycle, never committed). `git mv` on untracked directories fails silently or errors. Phase 4 step 3 should check `git ls-files --error-unmatch` on the reviews directory too, not just individual files.

### F-5 (P2): DONE/ directory already exists on retry

If spec-retire is interrupted after `mkdir -p DONE/<TICKET-ID>/` but before completing the moves, a retry will find the directory already exists with partial contents. `mkdir -p` is fine (idempotent), but `git mv` will fail if the destination file already exists. Add `--force` to `git mv` or check for existing files.

### F-6 (P2): Last-line parsing should be "last non-blank line"

spec-retire Phase 0 step 4 says "Read the reconciliation report's last line." If the file has trailing newlines (common), parsing fails. Should be "last non-blank line" — match the pattern used by spec-cycle for reviewer STATUS lines.

### F-7 (P2): Concurrent wiki edits during log.md append

log.md is append-only, but if another process (e.g., /wiki-after-merge) appends simultaneously, the idempotency grep may race. Low probability but worth noting. Mitigation: the grep + append is a single Bash call, and the user is unlikely to run both skills concurrently.

### F-8 (P2): `grep -rl` may match false positives in duplicate detection

Phase 2a uses `grep -rl "<TICKET-ID>"` which matches anywhere in a file — including references, related-links sections, or changelog entries that mention the ticket without being *about* it. Could produce false-positive duplicate warnings.

### F-9 (P3): No timeout on `gh pr diff` for very large PRs

Some PRs have thousands of lines. `gh pr diff` with no pagination or timeout could hang or produce massive output. Consider a timeout or `--patch` flag.

### F-10 (P3): Wiki path with spaces

Windows paths may contain spaces (e.g., "My Documents"). grep commands in Phase 2a need proper quoting.

### F-11 (P3): Empty "Wiki-ready" section in reconciliation report

If spec-reconcile produces a reconciliation report with an empty Wiki-ready section (no decisions or comprehension worth extracting), spec-retire Phase 2b should handle this gracefully — propose zero wiki entries rather than erroring.

## Closure Table

(Round 1 — no prior findings to close.)

STATUS: RED P0=0 P1=2 P2=6 P3=3
