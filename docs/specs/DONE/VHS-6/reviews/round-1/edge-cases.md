# VHS-6 Round 1 — Edge Cases Review

## Findings

### F-1 (P1): `git symbolic-ref --short` format bug (duplicate of correctness F-1)

**Location:** Design step 4b (line 99-102).

Same as correctness F-1. `git symbolic-ref --short refs/remotes/upstream/HEAD` returns `upstream/main`, not `main`. All downstream `upstream/<branch>` expansions would produce `upstream/upstream/main`.

### F-2 (P2): No timeout on `git fetch upstream`

**Location:** Design step 4c (line 105-108).

`git fetch upstream` could hang indefinitely on network issues (DNS resolution, unresponsive remote). The spec says "Network failure is non-fatal" but doesn't specify a timeout. Consider `timeout 30 git fetch upstream` or equivalent to bound wall-clock cost.

### F-3 (P2): `AskUserQuestion` tool does not exist

**Location:** Design step 4g (line 138).

`AskUserQuestion` is referenced as a tool call but is not a standard Claude Code tool. The LLM's standard interactive pattern is to present information and ask inline. The spec should describe the halt as a conversational prompt, not a tool invocation.

### F-4 (P2): BRE `\|` alternation in `--grep` is not portable

**Location:** Design step 4e (line 126).

`git log --grep="<term1>\|<term2>"` uses BRE alternation (`\|`), which is a GNU extension. For portability, use `--extended-regexp` (ERE) and plain `|`, or use multiple `--grep` flags (git OR's them by default).

### F-5 (P2): Single-tier query handling undefined

**Location:** Design step 4e (lines 118-128).

The spec says "Run two parallel git log queries" but step 4d may extract only file paths (no identifiers) or only identifiers (no paths). When one tier yields nothing, only one query should run. The spec should explicitly state: "If file paths were extracted, run the paths-based query. If code identifiers or title words were extracted, run the grep-based query. Run both in parallel only when both tiers have results."

### F-6 (P2): Windows path separators in regex

**Location:** Design step 4d (line 112).

The file-path regex `[A-Za-z0-9_./+-]+\.[a-z]{1,4}` uses `/` as path separator. On Windows, briefs may contain `\` separators. The regex won't match Windows-style paths. Since the check targets `git log` (which uses `/` internally), this is likely fine — but the brief content itself may use `\`. Consider normalizing.

### F-7 (P2): `git fetch` failure log says "using cached refs" but refs may not exist

**Location:** Design step 4c (line 108).

If `git fetch upstream` fails on a fresh clone that has never fetched upstream, there are no cached refs. The log line "using cached refs" is misleading. Better: "fetch failed (proceeding with available refs, if any)."

### F-8 (P2): Step 4f behind-count runs even when no commits found

**Location:** Design steps 4e-4f (lines 118-136).

Step 4e says "If both queries return empty: log and continue to step 5." Step 4f runs after 4e. If 4e already exited on empty results, 4f is unreachable. The flow is correct but could be stated more clearly — step 4f implicitly requires 4e to have found commits.

### F-9 (P3): Race between fetch and log

After `git fetch upstream` (step 4c), the upstream refs are updated. But if another process fetches concurrently (unlikely in a Claude Code session), the refs could change between fetch and log. Non-issue in practice.

### F-10 (P3): Search-term extraction on very short briefs

A brief with only a one-line heading and no body would yield only title-word fallback terms. These could be very broad (e.g., "upstream staleness check" → "upstream", "staleness", "check"). The 20-commit cap mitigates noise, but the user would see many false positives.

### F-11 (P3): `git rev-list HEAD..upstream/<branch>` counts all divergence, not just relevant

The behind-count includes ALL commits the fork is behind, not just the ones relevant to the brief's files. A fork 500 commits behind would show "500 commits behind" even if only 2 touch relevant files. This is by design (the check is "are you behind AND are there relevant commits") but could confuse users.

## Summary

The main edge-case concern is the symbolic-ref format bug (F-1, duplicate of correctness review). The remaining findings are robustness improvements: fetch timeout, BRE portability, single-tier query handling, and log message accuracy. None block shipping except F-1.

STATUS: RED P0=0 P1=1 P2=6 P3=3
