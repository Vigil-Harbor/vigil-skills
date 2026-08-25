# Handoff: importer schema migration

Authored fixture (VHS-28). The nested on-disk shape: containers at `##`, the
sections themselves at `###`. This is the shape the original validator could
never see, because its heading pattern was capped at `##`. Written by hand for
this suite — not copied from any real handoff.

## Session Metadata

- **Created**: 2026-05-19 16:40:02
- **Project**: /srv/example/importer
- **Branch**: feat/schema-v3

### Recent Commits

- 7c02f11 feat(importer): read v3 column names
- 33ad8b4 chore(importer): pin the sample corpus

## Current State Summary

The importer reads both v2 and v3 column names. The v2 branch is scheduled for
removal once the last publisher upgrades, which has not happened yet.

## Orientation

### Architecture Overview

`columns.py` normalizes header names, `rows.py` coerces values, `load.py`
drives both. The dual-schema logic is entirely inside `columns.py`.

### Critical Files

- `importer/columns.py` — the v2/v3 mapping table.
- `importer/load.py` — chooses the mapping from the header row.

## Completed

### Files Modified

| Status | File |
|--------|------|
| M | importer/columns.py |
| A | tests/fixtures/v3-sample.csv |

`columns.py` gained the v3 names; the sample is the smallest file that exercises
both header shapes.

### Decisions Made

Detect the schema from the header row rather than from a per-publisher config.
Rejected the config approach: it would need a migration for every publisher, and
the header is already authoritative.

## Pending Work

### Immediate Next Steps

1. Check whether publisher `north-star` has upgraded to v3 headers.
2. If every publisher has, delete the v2 mapping and its tests.
3. Re-run the importer suite against the pinned corpus.

## Context and Risks

### Important Context

The v2 mapping is not dead code — two publishers still send v2 headers. Deleting
it early silently drops columns instead of failing.

### Assumptions Made

Assumed the header row is always the first non-empty line. One publisher sends a
preamble comment; that path is handled but only lightly tested.

### Potential Gotchas

The sample corpus is pinned by content hash. Editing the CSV by hand, even to
fix whitespace, fails the pin check with a message that does not mention
whitespace.

## Handoff Chain

- **Continues from**: `.claude/handoffs/2026-05-12-101500-importer-audit.md`
