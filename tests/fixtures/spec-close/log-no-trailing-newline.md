<!-- VHS-29 fixture: `log-with-entries.md` with the final newline removed.
     Makes the tail invariant non-vacuous — the normal outcome splices at the
     top and must leave the tail byte-identical, including a MISSING trailing
     newline, because rewriting bytes it did not author is exactly what the
     encoding decision forbids. -->
# Wiki Log

Append-only record of wiki operations. Format: `## [YYYY-MM-DD] action | description`

> **Newest first.** `/wiki-after-merge` prepends here; if a tool appends at the
> bottom instead, the entry is out of contract — re-sort rather than leaving it.
> Older entries rotate into [`log-archive.md`](log-archive.md). This file holds
> entries dated **2026-08-01 and later**.

## [2026-08-24] merge | VHS — VHS-28: `session-handoff` skill, superseding the vendor copy

`40c4bb8` (PR #24). Body prose for the previously-newest entry, carrying an em
dash — and a `|` pipe — so the guard compare has neighbours that look like it.

## [2026-08-20] close | VHS — VHS-27: an earlier close entry (archived from TODO/)

Body prose for the older entry.