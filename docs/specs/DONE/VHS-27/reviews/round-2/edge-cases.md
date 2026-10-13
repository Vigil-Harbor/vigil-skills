The round-1 fixes hold. Two code-drift inputs still drop a cited change, and an empty delta can still replace a red marker.

# Edge-Cases Review — round 2

## Closure of round 1 findings
| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | Reader state `changed` never selects a candidate round | CLOSED | spec § Decision 14 and § Mode lines 128–130, 157: candidate comes from `source: review` plus a positive `round`, including a fingerprint mismatch; scenario 2b |
| correctness | F-2 | Green-round `spec.copy.md` is taken before post-green polish | CLOSED | spec § Decision 2, § Artifacts line 214, § Two counters line 204: green path rewrites `spec.copy.md` after polish and before the green marker; scenario 2 |
| correctness | F-3 | Output-contract closure line stays on the round-1 rule | CLOSED | spec § Delta contract line 329 replaces the output-contract parenthetical in all four agents |
| correctness | F-4 | Ticket not cached | CLOSED | spec § Deferred (P2+) records no spec change; brief remains the source |
| edge-cases | F-1 | Ledger coverage is a substring test, so a dropped shorter id is invisible | CLOSED | spec § Delta contract lines 351–354: token regex, severity immediately after the id, title matches excluded; scenario 11 |
| edge-cases | F-2 | House-style `path:line` citations never count as code drift, so scenario 10 no-ops | CLOSED | spec § Changed regions lines 275–276 strip `:digits`, ranges, en dash, and `#Ldigits`; scenario 10 |
| edge-cases | F-3 | Any edit marks every ancestor section changed, so a delta pass may explore the whole spec | CLOSED | spec § Changed regions lines 261–263 and § Delta contract line 340: exclusive body; ancestors and unlisted descendants stay out |
| edge-cases | F-4 | A git error suppresses the no-op, then an empty delta may go green and replace the baseline | CLOSED | spec § Mode line 160, § No-op line 183, § Two counters line 202, scenario 12: classifying failure is `mode: full (code-drift unavailable)`; a pass-2 failure leaves the marker pending and deletes that pass's `baseline.commit` |
| edge-cases | F-5 | A review marker whose round is not a positive integer falls through to delta | CLOSED | spec § Mode rows 10–11 and line 132; marker writes use temp-then-rename (§ Artifacts line 223); scenario 13 |
| edge-cases | F-6 | `baseline.commit` and `ledger.md` treat a Windows newline as corrupt | CLOSED | spec § Mode lines 136–138: commit accepts LF or CRLF on read, raw LF on write; ledger header is tested after carriage returns are removed |
| edge-cases | F-7 | The no-op can report green for a red marker when reports are missing or headings do not parse | CLOSED | spec § No-op steps 2–3 and lines 176–181: a red marker and a missing standing report are not a no-op; the block prints the verdict on disk; line-only `Where` maps to a heading (§ Changed regions line 283). A later empty-scope green write is F-3 below |
| edge-cases | F-8 | Only the immediate next round directory is reserved, so a later pass can overwrite an existing round | CLOSED | spec § Decision 8, § Mode row 9 and line 162, § Artifacts line 227: both delta directories and the full `round_cap` span must be absent |
| conventions | F-1 | Output-contract closure line is not an edit site | CLOSED | spec § Delta contract line 329 names `# Output contract` in all four agents |
| conventions | F-2 | Correctness anchor replacement leaves the old P1 rule in place | CLOSED | spec § Decision 4 and § Delta contract lines 345–349: replace the **Stale anchors** bullet and numbered item 2; do not leave the old P1 sentence |
| conventions | F-3 | Decision 7 omits the Follow-up filter § Mode applies | CLOSED | spec § Decision 7 lines 67–68 uses the same carriage-return and `**Follow-up:**` filters as § Mode |
| conventions | F-4 | Single-counter write-points and closure prose are not named as edit sites | CLOSED | spec § Docs lines 373–386 names write points, the interrupted-run bullet, both workflow-reference closure/tier paragraphs, and the `AGENTS.md` spec-brief grill at cumulative `C` |
| conventions | F-5 | Invocation syntax is specified once and copied in three places | CLOSED | spec § Invocation lines 116–117 names the H1 `Invoked as` line, the attest usage halt, the workflow reference, and `AGENTS.md` |
| conventions | F-6 | Mode row 9 is a spec-level addition to the brief's mode list | CLOSED | spec § Decision 14 lines 94–96 carries the occupied span and the non-integer round as storage rows under Decision 8 |
| conventions | F-7 | § 2b's sample disposition still cites a skill line | CLOSED | spec § Ledger line 247 replaces the sample with `fixed: re-anchored to § Design` |

## Findings

### F-1: A renamed cited file never becomes a changed path, so the no-op sticks
**Severity:** P1
**Where:** spec § Changed regions, lines 265–270
**Edge case:** Since `baseline.commit`, a file the spec cites is renamed, or renamed and edited. Default `diff.renames` is on. The spec text and the brief still match the saved copies, the guarantee scan is clean, and there is no open P0 or P1. The same hole hits a path git quotes (`core.quotePath` defaults to true: space, quote, or a non-ASCII byte) and a `git diff --name-only` listing the host truncates.
**What happens:** `git diff --name-only` prints the rename destination only, not the old path. The citation does not match, so the changed-region set stays empty. § No-op leaves the green marker and does not dispatch, so the dead citation is never filed. The old `baseline.commit` is kept, and every later re-run no-ops the same way. The spec bytes did not change, so `/ship-spec` sees a matching fingerprint and will not ask. If some other edit makes this run a real delta and it goes green, the new `baseline.commit` is current `HEAD` (§ Artifacts line 216) while the drift list was taken earlier (§ Mode line 160, § No-op line 168). The rename is then gone from the next diff as well.
**Why the spec misses it:** The four commands are defined as the path list. Nothing disables rename detection, passes `--name-status` and keeps both sides, sets `core.quotePath=false` and `--no-color`, or treats a quoted or truncated line as failure. A non-zero exit is a failure (§ Mode line 160). A successful listing that drops the cited path is not. The SHA written at dispatch is a second `git rev-parse`, not the SHA the listing was computed against.
**Suggested fix:** Take one snapshot. `git rev-parse HEAD` first. Run the four listings against that SHA with `-c core.quotePath=false --no-color --no-renames` (or `--name-status` and union every old and new path). Unquote nothing by hand. A non-zero exit, a line that is not a raw path, or a short read is `mode: full (code-drift unavailable)` during classification, and the pass-2 pending stop if a delta was already dispatched. Write that same SHA as `baseline.commit`. If `HEAD` differs when the file is saved, do not treat the newer tree as reviewed.

### F-2: Two headings with the same line can hide an edit
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Changed regions, line 263
**Edge case:** The spec has two headings whose lines are identical, such as two `### Example` sections. Only the second exclusive body changes. Bytes before the first heading (a BOM or a leading line) are a smaller cousin: they are in the fingerprint and in no body.
**What happens:** "The baseline heading with the same heading line" does not say which one, or that both must be paired in order. A map keyed by that line keeps one body. The edited body is not a changed region. If nothing else changed, the no-op runs and leaves the old fingerprint (`/ship-spec` then confirms). If something else changed and the delta goes green, the unreviewed body is included in the new fingerprint and is not reviewed.
**Why the spec misses it:** Identity is only the heading line. Document order, the parent stack, and bytes outside any heading are not mentioned.
**Suggested fix:** Pair headings in order by the stack of heading lines from the root. An unpaired heading is an addition or a deletion. If the filtered file bytes differ and that pairing explains none of the difference, emit a changed region rather than a no-op.

### F-3: A red marker whose P0/P1 headings do not parse can be replaced with green
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § No-op steps 2–5 (lines 171–174); spec § Dispatch, lines 311–313
**Edge case:** The marker is `red`. Each standing report is readable and has a `STATUS:` line, but no `### F-<k>:` heading with severity P0 or P1 (STATUS counts are non-zero, or the finding lines were not saved). The filtered spec matches `spec.copy.md`, code drift is empty, and the guarantee scan is clean.
**What happens:** Step 2 correctly refuses the no-op and dispatches. § Dispatch adds `<lens>/STATUS` only when the STATUS line is missing or the file is missing. Here the open set is empty and the changed-region set is empty, so the delta contract forbids new critique. Closure has no heading to reopen. A clean STATUS writes `verdict: green` and a new `baseline.commit`. `/ship-spec` will pass. The round-1 failure mode was a no-op that only printed green; this path writes green.
**Why the spec misses it:** Open findings are defined only as parseable `### F-<k>:` headings. A red marker forces a dispatch, not a full review, and nothing forbids a green exit when both delta sets are empty.
**Suggested fix:** If a report's STATUS P0+P1 is greater than zero and that lens yielded no open heading, add `<lens>/STATUS (P0)` and do not call the open set empty. Do not write a new green marker for a delta whose changed-region set and open-finding set are both empty unless the marker on disk is already green; otherwise select `mode: full (open findings unreadable)`.

## Summary
P0: 0 | P1: 1 | P2: 2 | P3: 0 | P4: 0

STATUS: RED P0=0 P1=1 P2=2 P3=0 P4=0
