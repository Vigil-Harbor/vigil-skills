# Handoff: retry backoff rewrite

Authored fixture (VHS-28). The fully flattened on-disk shape: every section is
`##`, including the ones the template nests at `###`. Written by hand for this
suite — not copied from any real handoff.

## Session Metadata

- **Created**: 2026-03-04 09:12:44
- **Project**: /srv/example/queue-runner
- **Branch**: fix/retry-backoff

## Recent Commits

- 4a1c9de fix(queue): cap the retry ceiling at 30s
- 91be207 test(queue): cover the jitter bounds

## Current State Summary

The exponential backoff now caps at 30 seconds instead of growing without
bound. The jitter fraction is still hardcoded; making it configurable is the
next piece of work.

## Architecture Overview

`runner.py` pulls jobs, `backoff.py` decides the delay, `store.py` persists the
attempt count. Only `backoff.py` changed.

## Critical Files

- `queue/backoff.py` — the ceiling and the jitter live here.
- `queue/runner.py` — calls into it once per failed attempt.

## Files Modified

| Status | File |
|--------|------|
| M | queue/backoff.py |
| M | tests/test_backoff.py |

`backoff.py` gained the ceiling; the test file gained bounds assertions.

## Decisions Made

Capped at 30s rather than 60s: the upstream timeout is 45s, so a 60s ceiling
would have guaranteed a timeout on the last retry. Rejected making the ceiling
configurable in this change — nobody has asked for it.

## Immediate Next Steps

1. Read `queue/backoff.py` and confirm the jitter fraction is still 0.2.
2. Decide whether the fraction becomes a constructor argument.
3. Run the queue suite before touching the runner.

## Important Context

The staging queue has a stuck job from before the cap landed. It will retry
forever until someone drains it; that is expected and not a regression.

## Assumptions Made

Assumed the upstream timeout stays at 45s. Not verified against the vendor's
current documentation.

## Potential Gotchas

`test_backoff.py` seeds the random module directly. Reordering the tests changes
the jitter values and the bounds assertions fail for reasons unrelated to the
code under test.

## Handoff Chain

- **Continues from**: None (fresh start)
