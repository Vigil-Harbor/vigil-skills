# Round 5 — delta-only review

The user scoped this round explicitly: **"Review the deltas only."**

Two lenses were dispatched (correctness, edge-cases) — the two that were RED at round 4.
Conventions was GREEN at round 4 and was not re-run; re-scanning unchanged sections was the
churn the scoping decision was meant to avoid.

Both reviewers were given the v4->v5 delta list by section and instructed to report findings
outside it only where a delta made something wrong.

## Gate

| Lens | Round 4 | Round 5 (deltas) |
|---|---|---|
| correctness | RED P0=0 P1=2 | RED P0=1 P1=1 |
| edge-cases | RED P0=0 P1=2 | RED P0=1 P1=1 |
| conventions | GREEN | not run (scoped out) |

Both lenses independently found the same P0. Every round-5 blocking finding was introduced by
the v5 deltas themselves - none was pre-existing. That is the delta review working as intended.

## What the P0 was

v5 fixed the `set -e` exit-capture problem in D5's code block (`if ...; then rc=0; else rc=$?; fi`)
but left two prose sites still prescribing `echo "prepend_log_entry_exit=$?"`. After `fi`, `$?` is
the status of the last command in the taken branch - an assignment - so it is **always 0**.

Reproduced in this repo's Git Bash before accepting:

    if python -c 'import sys; sys.exit(2)'; then rc=0; else rc=$?; fi
    rc=2   $?=0

Transcribed into SKILL.md, that form would report `Prepended: log.md` for refusals, skips and
PermissionErrors alike - the silent-green class this ticket exists to remove.

## Folded into v6 / v7

v6: the P0 (both prose sites), the `python` vs `python3` contradiction (resolved into `$PY`),
the self-rejecting placeholder template, the missing placeholder-guard test, the notice-text
divergence, and the over-general BOM claim.

v7: the BOM handled at the root - matching runs against the text with a leading BOM removed and
offsets shifted, so the BOM is preserved in output and invisible to the anchor; D7's list no
longer claims the refusal row catches it; `prepend_log_entry_outcome=` on stdout as the carrier
for the three-way exit-0 split (stream-emptiness was not a value the caller holds); notices carry
the resolved path; new **BOM on the existing file** case.

BOM behaviour was measured directly rather than taken on trust. The reviewer's framing was
directionally right but imprecise: a BOM only defeats the anchor when it immediately precedes an
entry heading (a headerless file). With log.md's real `# Wiki Log` first line the BOM is inert.
Both broken shapes are silent, so v7 removes the class rather than documenting which shapes are safe.
