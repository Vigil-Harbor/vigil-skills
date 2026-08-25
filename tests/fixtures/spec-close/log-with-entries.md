<!-- VHS-29 fixture. Reproduces vigil-harbor-wiki/log.md's real header as it
     stands BEFORE the wiki-side "Append-only record" reword (AC6), which is
     shipped separately, direct on wiki master. Pinned on the pre-reword text
     deliberately: that reword touches only the sentence's opening words, and
     the `Format:` clause below — the half that breaks a naive first-hit scan
     for a bracketed h2 — is unchanged either way, so this fixture stays valid
     before and after it. THIS FIXTURE IS THE TEST: without the format
     sentence, a naive implementation passes everything below it. This note is
     deliberately free of any bracketed-h2 literal of its own, so the first
     naive hit in the file is the format sentence, exactly as in the live
     log.md, which carries no such note. -->
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
