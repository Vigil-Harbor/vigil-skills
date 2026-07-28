# VHS-6 Round 2 — Conventions Review

## Closure of round 1 findings

All round 1 findings resolved. See correctness round-2 closure table for full cross-lens closure.

## Findings

### F-1 (P2): Done-when #1 parenthetical lists 8 items for 7 sub-steps

Same as correctness F-1 and edge-cases F-1. Cosmetic mismatch.

### F-2 (P4): `sed` added to Tool-use notes without CLAUDE.md external dependencies note

Ship-spec already uses `sed` and CLAUDE.md doesn't list it because it's a POSIX standard utility. Consistent behavior — no action needed.

### F-3 (P3): D4 drops "error strings" extraction tier from brief without explicit rationale

Brief mentions "error strings (heuristic: ALL-CAPS_WITH_UNDERSCORES)" as an extraction tier. Spec's code-identifiers tier partially subsumes this (ALL_CAPS tokens in backtick spans match the 4+ char regex) but the departure is not called out. Reasonable simplification — spec says "Spec author pins extraction regex; recommend keeping it small."

### F-4 (P3): `timeout` command is not a Windows-native command

Works via Git Bash on all current target machines. Ship-spec doesn't use `timeout` for git commands — a pure-git alternative exists (`git -c http.lowSpeedTime=30`). Not a functional issue since Bash tool is the execution path.

### F-5 (P3): Brief `[y/N]` → spec conversational prompt departure is well-handled

D6 explicitly maps the brief's stdin metaphor to the LLM's interactive pause with rationale. Correct as written.

STATUS: GREEN
