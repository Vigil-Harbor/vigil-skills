# Round 6 — narrow delta check (v5 -> v7)

Two lenses (correctness, edge-cases), scoped to the v5->v7 deltas only.

## Gate

| Lens | Round 5 | Round 6 |
|---|---|---|
| correctness | RED P0=1 P1=1 | RED P0=1 P1=0 P2=1 P3=2 |
| edge-cases  | RED P0=1 P1=1 | RED P0=1 P1=0 P2=3 P3=1 |

Both lenses independently found the SAME P0, and it was the same *class* as round 5's:
a decision was updated and its § Design mirror was not.

- Round 5 P0: D5's code block got the `$rc` fix; two prose sites kept `$?`.
- Round 6 P0: D5's exit table got the `prepend_log_entry_outcome=` carrier; § Design's
  "Line 365 (completion output)" bullet - the site that dictates what SKILL.md:365 actually
  says - still branched on "exits 0 silently vs with a stderr notice", the discriminator
  D5 rejects by name one paragraph earlier.

## Root-cause action

Rather than fix the third instance and hope, v8 adds a mechanical cross-check: every mechanism
the Decisions introduce is greped against § Design and § Test plan. That sweep found a fourth,
unreported instance - `prepend_log_entry_exit` appeared 3x in Decisions and 0x in § Design - which
is now closed. The sweep currently reports no Decisions-only mechanisms.

## Findings folded into v8

P0 (both lenses): § Design's completion-output bullet now keys on the outcome token; the `main()`
walkthrough prints it after a successful `os.replace`; the step-4 contents bullet names both the
exit capture and the outcome token.

P2 (edge-cases F-3): the interpreter probe tests executability, not presence. Measured on the
operator machine: `python3` is the WindowsApps App Execution Alias at 3.13.14 while `python` is
3.14.3 - a presence-only probe selects a different interpreter than the test command uses, and on
a host without Store Python it selects a stub that exits 9009 without reading stdin.

P2 (both lenses): the BOM fix and D7's degenerate no-leading-separator rule did not compose -
a BOM is not whitespace, so `.strip()` keeps it and the rule never fired on a BOM'd file.
v8 detaches the BOM, splices in stripped coordinates, and re-attaches, so the two rules compose
with no extra clause. `splice()`'s contract and the Whitespace case now say so.

P2/P3: `$PY` added to the step-4 enumeration; D5's "every message names path and guard" narrowed
to failure messages, since D7's two exit-0 notices carry the path only.

## Status

v8 folds every round-6 finding. v8 itself has NOT been reviewed.
