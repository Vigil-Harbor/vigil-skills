# Edge-Cases Review — round 2

## Closure of round 1 findings
All nine round-1 edge findings verified **CLOSED** (independently simulated against the live wiki: 0 new INDEX info, exit 0). F-1 anchor (header in old_string) — verified H2 headers unique. F-2 (date-descending + max). F-3 (status line). F-4 (table-shape guard). F-5 (partial-run self-heal). F-6 (best-effort note). F-7 (advisory uses token rule). F-8 (try/catch). F-9 (sequential inserts). No REOPENED.

## Findings

### F-1: `max(existing, merge-date)` and "merge-date" underspecified — string-vs-Date comparison + date-source split + malformed/absent existing date
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** § D11; Part A steps 4–6
Two dates are used without pinning equality or comparison domain: the **row date** ("date from the entry" = slug `YYYY-MM-DD`, derived from commit message, `SKILL.md:52`) and the **`Last updated`** bump using `max(existing, merge-date)` where "merge-date" is never defined and appears nowhere in the skill. Failure paths: (a) `> Last updated:` is a bare `YYYY-MM-DD` string — `max()` is correct only lexically; an agent could parse to `Date` and re-serialize (timezone drift) — the lint itself uses `new Date(match[1])` (`wiki-lint.mjs:138`), a tempting mirror. (b) Missing/malformed existing date (`prime-radiant-hub.md:3`/`dynasty-hub.md:3` are stale `2026-05-17`, so the first insert exercises the `existing < new` branch) has no defined behavior.
**Fix:** state row date and `Last updated` are the **same** `YYYY-MM-DD` slug date; compare/store as zero-padded `YYYY-MM-DD` **strings** (lexical = chronological; no `Date`, no `Math.max`); malformed/absent existing → treat as empty (new wins) + emit a status line. Replace "merge-date" with "the entry's slug date" throughout.

### F-2: Date-descending insert undefined when the first data row's date is malformed/non-`YYYY-MM-DD`
**Severity:** P3
**Where:** § D11; Part A step 5
Table-shape guard checks header+separator, not per-row date well-formedness. A `| 2026-05-XX |` placeholder row (the wiki uses `-XX` slugs, `prime-radiant-hub.md:33`), empty first cell, or prose row makes the `≤` comparison undefined → possible newest-first violation (no crash).
**Fix:** skip rows whose first cell isn't `YYYY-MM-DD`-shaped when scanning; if none well-formed, insert below the separator + note in status line.

### F-3: AC-3's "wrong single project hub" case is silently un-caught by the "any project hub → silent" escape — confirm intended scope
**Severity:** P2  **Pre-ship recommended:** yes
**Where:** § D7; Part E; Done-when AC-3
The escape silences an entry in ANY project hub, including a non-prefix one. This preserves the legitimate DYN-under-RAD lineage (verified: all 10 such live entries are intended lineage, no false-negative today) but also silences a hypothetical misfile (PET entry only in `dynasty-hub.md`). The original motivating gap (PET-111 in NO project hub) is still caught, so AC-3's literal "any project hub" text holds; the brief's prose says "its **own** project hub" (`brief:31,45`), which is narrower. Conscious, documented trade — scope-confirmation, not a contradiction.
**Fix:** add one sentence to AC-3/D7 making the residual explicit (cross-lineage silence is intentional; the skill-time advisory is the misfiling backstop). Confirm at drift-check that "any project hub" is the accepted AC-3 reading.

### F-4: "insert failed → hard stop" leaves Step 7c Plane writes committed + earlier sequential inserts in the working tree
**Severity:** P3
**Where:** § D11; Part A step 8; interaction with `SKILL.md:90` (7c.6)
Step 7c Plane writes precede Step 8 and aren't rolled back; a hub-insert failure aborts the wiki commit after siblings transitioned, and a multi-entry run can leave entry 1's `Edit` in the working tree. Recoverable (git atomicity + grep-skip self-heal) and observable via the status line, but the "nothing commits" framing doesn't acknowledge the residue.
**Fix:** note the 7c-precedes-8 window + `git checkout -- <hub>` before re-running.

### F-5: `projectHubTexts` re-reads every hub a second time after `hubPrefixMap` — minor
**Severity:** P4
Up to 4 reads of each hub per run; a concurrent edit between reads could flip one entry to a spurious `info` (sub-ms window, exit unaffected). Optional: hoist a single `hub → text` map.

## Summary
P0: 0 | P1: 0 | P2: 3 | P3: 2 | P4: 1
All round-1 findings genuinely closed (verified live). Substring-collision risk the prompt flagged is NOT real (0 proper-substring containments among 233 full paths; `.includes(c)` uses full paths). Remaining items are precision gaps the revision introduced — none block shipping.

STATUS: GREEN
