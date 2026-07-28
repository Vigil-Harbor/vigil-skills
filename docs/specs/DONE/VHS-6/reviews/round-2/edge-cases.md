# VHS-6 Round 2 — Edge Cases Review

## Closure of round 1 findings

All prior P0 and P1 findings CLOSED. All P2 findings either CLOSED or explicitly deferred to P2+ with rationale.

(See correctness round-2 closure table for full cross-lens closure.)

## Findings

### F-1 (P2): Done-when #1 parenthetical lists 8 items for 7 sub-steps

Same as correctness F-1. Cosmetic mismatch between sub-step count (a–g = 7) and parenthetical activity count (8). "clean/skip logging" is not a distinct sub-step.

### F-2 (P3): File-path regex matches the brief's own filename

The regex includes `.md` as a known extension. Brief self-references (`docs/specs/TODO/VHS-6.brief.md`) will match and could consume path slots. Mitigated by 20-commit cap and user gate.

### F-3 (P3): `timeout` kill signal indistinguishable from network error in log

When `timeout 30` kills `git fetch` (exit 124), the log says the same "fetch failed" as a network error. No functional issue — all paths proceed correctly.

### F-4 (P3): `git rev-list` argument ordering

`git rev-list HEAD..upstream/<default-branch> --count` places `--count` after the ref range. Canonical form puts flags first. Works on modern git; purely style.

### F-5 (P3): No stopword list defined for fallback tier

Step 4d priority 3 says "non-stopword tokens" but doesn't define which words are stopwords. Low impact since fallback tier rarely fires.

### F-6 (P4): Test plan static verification test 3 uses BRE `\|`

The verification grep command uses BRE alternation, same portability concern the spec fixed for runtime. Acceptable since these are one-shot developer checks.

STATUS: GREEN
