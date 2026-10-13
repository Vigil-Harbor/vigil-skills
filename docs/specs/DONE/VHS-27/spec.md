# VHS-27 — Delta-scoped review passes for spec-cycle

**Ticket:** VHS-27
**Brief:** `docs/specs/TODO/VHS-27.brief.md`
**Namespace:** `skills` (states.json prefix `VHS`)

## Goal

A re-run of `/spec-cycle` over a spec that already has a reviewed green or a red halt reviews only what changed, plus open P0/P1 findings, for at most two passes. The first invocation's loop is unchanged. The skill saves the spec, the brief, the HEAD commit, and the P0/P1 disposition ledger beside each round so a later run can see hand edits and dropped findings. Nothing changed and nothing open is a no-op that leaves the green marker as it is. The work is skill and agent prose. No check script ships with it.

## Scope

Files to change. `sync.py` mirrors `skills/` and `agents/` into the install dir; `docs/` and `AGENTS.md` are not installed.

| Path | Change |
|---|---|
| `skills/spec-cycle/SKILL.md` | Add `--full`, exclusive with `--attest`. Resolve review mode from the marker fields and print it. Classify the clean no-op before the pending write. Run delta passes under two counters. Save the per-round copies, the commit, and the ledger. Pass changed regions and open findings. Warn on both stop screens. |
| `agents/spec-reviewer-correctness.md` | Accept the delta inputs. Apply the delta contract below. Compare the saved ledger with the prior round's reports and file one P0 when a P0 or P1 line is missing. Split anchor drift by cause. |
| `agents/spec-reviewer-edge-cases.md` | Accept the delta inputs. Apply the same delta contract. Split anchor drift by cause. |
| `agents/spec-reviewer-conventions.md` | Same as edge-cases. |
| `agents/spec-reviewer-scalability.md` | Same as edge-cases. The lens is still dispatched only when scale is on. |
| `docs/spec-workflow-reference.md` | Describe delta mode, `--full`, and the verdict `round` range. State the rationale with the PET-166 numbers. Say which paragraphs describe the first invocation's pass index. |
| `AGENTS.md` | In the `/spec-cycle` lifecycle item, state delta mode and `--full`. In the `/spec-brief` lifecycle item, state that the grill also follows a delta halt. |

Every edit site is a heading, a named step, or a named input bullet. Do not target a line number. The brief's line anchors are true at commit `c01286d` only. VHS-26 edits these same sections of `skills/spec-cycle/SKILL.md` next. Re-find the heading if the file has moved. Do not leave a line-number citation in any of the four agent files.

Files to leave alone:

- `skills/ship-spec/SKILL.md` and `skills/spec-tickets/SKILL.md`. Both print `round` as an opaque token. Neither checks a 1..4 range. Widening the token needs no edit there.
- `skills/spec-close/SKILL.md`. It already moves `<TICKET-ID>.reviews/` to `docs/specs/DONE/<TICKET-ID>/reviews/`. This spec only refuses to read that archive as a baseline.
- The Deferred-findings block in all four agents. It stays byte-identical, including across the four files. Do not insert the delta contract or the anchor rule into that block.
- `skills/spec-brief/SKILL.md`, `sync.py`, `lint.py`, `skills/ship-spec/states.json`, and `tests/`. No new test module. VHS-26 is the check script, and it is not this spec.

## Decisions

### Decision — Stakes tier

**Tier:** big

`round_cap` stays 4 for this tier. The two-pass delta budget in Decision 8 is the same on `small`, `big`, and `irreversible`. The scale re-run pin and the tier re-run pin are unchanged. This brief has no `## Scale` section, so the spec records none.

### Decision 1 — Delta passes run on re-runs only

The first invocation's loop stays the loop the skill has today: passes `1 .. round_cap`, revise while the pass index is below `round_cap`, FROZEN/REWRITE on the pass whose index equals `round_cap`, halt after that pass if still loop-red. A re-run is the only place a delta pass attaches. Honored by § Mode and § Two counters.

### Decision 2 — A copy of the spec and of the brief, every round

Before each dispatch, including every pass of a full invocation, the skill writes `spec.copy.md` and `brief.copy.md` into that round's directory. Changed regions are a diff against a baseline copy, not an author-stated list. Preflight reads the marker's round and selects that round's copy before the pending write replaces the marker. The selection is held for the invocation. Delta pass 2's text baseline is the copy delta pass 1 saved before its own dispatch. On a green round only, after post-green polish and before the green marker, rewrite that round's `spec.copy.md` to the post-polish bytes. A loop-red round keeps the pre-dispatch copy. Polish does not touch the brief, so `brief.copy.md` is not rewritten. Honored by § Artifacts, § Ledger, and § Changed regions.

### Decision 3 — The ledger is a saved file, P0 and P1 only

After every red round's revision, the final round included, the skill writes `ledger.md`. The next round, in this invocation or a later one, reads that file back and passes those bytes as `closure_manifest`. A green round writes an explicit empty ledger before the green marker. A required ledger that is missing or unreadable selects full mode. An earlier round's ledger is never used in its place. The correctness lens alone compares the manifest with the prior round's reports and files one blocking P0 when a P0 or P1 line is missing. Coverage is a token match on that line, not a substring of a longer id. P2 and lower never enter the ledger. Honored by § Artifacts, § Ledger, and the correctness paragraph of § Delta contract.

### Decision 4 — Anchor drift splits by cause

A citation whose symbol still resolves and whose line number moved is one combined P4 per reviewer report. A citation whose symbol is gone stays a P1, one finding per dead citation. In the correctness agent this replaces both the **Stale anchors** bullet and numbered item 2 of the cross-section walk. Do not leave either, and do not leave a sentence that every stale anchor is a P1 or that the check re-greps the cited line. The other three agents gain the same paragraph. It applies in full mode and in delta mode. Honored by § Delta contract (anchor paragraph).

### Decision 5 — Code drift uses the saved commit

`baseline.commit` is the one `timeout 30 git --no-pager rev-parse HEAD` snapshot the path listing was computed against, saved beside each round's copies. It is not a verdict-marker field, and it is not a second rev-parse taken later. On a re-run, a spec section that cites a file changed since that commit is a changed region. A rename lists both the old path and the new path. A quoted path is not repaired. While the mode table would select delta, a code-drift command that fails, a command that does not finish within the `timeout 30` bound, a saved SHA that does not resolve, or a listing line that is not a raw path selects `mode: full (code-drift unavailable)` before the pending write. A text-only delta is not dispatched. After a delta pass was already dispatched, the same failure does not go green and does not leave that pass's new `baseline.commit` as the next baseline. If HEAD moves after the snapshot, the saved SHA stays the snapshot, so the newer tree is not treated as reviewed. The spec path, the brief path, and any path under that ticket's `reviews/` directory are not code drift. Both the halt screen and the Phase 3 screen carry the drift warning. Honored by § Artifacts, § Mode, § Changed regions, and § Stop screens.

### Decision 6 — `--full` requests a full pass

`--full` is exclusive with `--attest`. It does not override the tier pin or the scale pin recorded in the spec. It forces full mode, which also suppresses the no-op. Honored by § Invocation and § Mode.

### Decision 7 — A changed brief forces a full pass

The skill compares the brief with the saved `brief.copy.md`. The comparison removes every carriage-return byte and drops every line whose first non-blank characters are `**Follow-up:**`. No other byte is dropped. Any remaining difference selects full mode. A delta pass never runs against a changed brief. Honored by § Mode.

### Decision 8 — Two counters, at most two delta passes on every tier

The cumulative review round names `round-<N>/` and the marker's `round`. It is any positive integer. The per-invocation pass index drives revise, fold, and halt. Delta pass 1 revises under the ordinary revision rules. Delta pass 2 routes and folds without FROZEN/REWRITE and, if still loop-red, halts with the existing halt menu. The grill option uses the final cumulative round's directory. A green delta pass runs post-green polish and Phase 3. Before any round directory is created, the whole span must be absent: delta needs both `candidate+1` and `candidate+2` absent; a full invocation needs `start` through `start+round_cap-1` absent. If any one of those directories exists, the mode is full and `start` is the smallest positive integer whose span is entirely free. A later step that replaces a delta token with a full token discards `candidate + 1` and computes `start` with that same rule before any directory is created. If no free span of `round_cap` directories exists, the run stops and the marker is unchanged. Delta pass 2 uses the final-round recount rule: it may keep a fold and may not revert, including when the original finding is out-of-scope, because there is no third pass. Honored by § Two counters and § Mode.

### Decision 9 — A non-empty delta pass dispatches every lens the run would normally dispatch

Three lenses, or four when this invocation's scale lens is on. The saving is the narrower scope, not a dropped lens. Honored by § Dispatch.

### Decision 10 — The delta restriction covers new exploration only

Reviewers do not explore unchanged regions and do not re-litigate a settled decision. A named heading covers its exclusive body only. A descendant heading is in scope only when it is itself named. Closure verification, the Deferred-findings block, grounding, process failures, and vanished-reference checks run as today at their existing severities. A P0 met incidentally outside the changed regions may be reported, with evidence, and it counts in the gate. Reviewers do not read an unchanged region to look for one. Honored by § Delta contract. The contract text stands alone: the four agents run installed in other repos, so that text cites no skill line and no path in this repo.

### Decision 11 — Nothing changed and nothing open is a no-op

The skill classifies the no-op before the pending write. The guarantee scan runs first. If the scan withholds, the run is not a no-op and goes on to dispatch. A `red` marker is not a no-op. A missing or unreadable standing-lens report is not a no-op. A `red` marker whose changed-region set and open-finding set are both empty is not dispatched as an empty delta. It selects `mode: full (open findings unreadable)` before the pending write. That full pass discards the delta start and uses Decision 8's full-invocation span. An open set that contains a `<lens>/STATUS` line takes that same full pass. The line names no heading and is not dispatched as delta. A green marker whose changed-region set or open-finding set is non-empty is not a no-op. It dispatches delta. A no-op takes no round number, saves no copy, dispatches no reviewer, runs no polish and no synthesis, and does not rewrite the marker. It reports the verdict already on disk by leaving that marker in place. The clean path is a green marker with both sets empty. Honored by § No-op.

### Decision 12 — No saved copy means a full pass

That run saves the first copy and prints `mode: full (no baseline)`. A delta pass never runs without a baseline. The archive under `docs/specs/DONE/<TICKET-ID>/reviews/` is never a baseline. Honored by § Mode and § Artifacts.

### Decision 13 — A pending marker means a full pass

The full pass takes the smallest `start` whose span of `round_cap` directories is free, so an interrupted run's reports stay as audit evidence. Round numbers are storage, not closure ancestry. The first pass of any full invocation has no closure predecessor and needs no ledger. Later passes of that same invocation close the completed pass before them. Honored by § Mode and § Two counters.

### Decision 14 — Mode table

The mode is resolved from the marker fields `verdict:`, `source:`, and `round:`. It is not resolved from the six-state reader's `green` or `changed` state. A fingerprint mismatch is not a row. The mode is full, with its reason printed, when any row in § Mode matches. The carried-forward rows are `--full`, marker missing, marker unreadable, pending, attested (whether or not the fingerprint matches), brief changed, no baseline, and ledger missing or unreadable. Two further rows are this spec's storage rules, pointing at Decision 8: the delta span is occupied, and a review green or red whose `round` is not a positive integer. When the table would select delta and code drift cannot be computed, including a listing line that is not a raw path, Decision 5 replaces the token with `mode: full (code-drift unavailable)` before the pending write. When the table would select delta and the open set contains a `<lens>/STATUS` line, or the marker is `red` and both sets are empty, the token is `mode: full (open findings unreadable)` before the pending write, and `start` is recomputed by Decision 8. Otherwise the mode is delta. An attested green has no reviewed round to continue from. Honored by § Mode.

### Decision 15 — Delta inputs

Changed regions are Markdown headings together with the diff hunk of each heading's exclusive body. An ancestor is not emitted because a descendant changed. Identical heading lines pair in document order by the stack of ancestor heading lines. That pairing is not a similarity guess. A renamed heading is a deleted heading plus a new heading. Bytes before the first heading are their own region. Open findings are the prior round's unresolved P0 and P1 only. A `Where` is split on `;`. Each clause matches a heading by equality or by the longest heading-text prefix, and a match does not use the line. A clause with no matching heading uses its line number against the predecessor `spec.copy.md`, then stack-pairs into the current spec. A non-matching `§` phrase does not discard that line. `spec.md`, the ticket's spec filename, and the repo-relative spec path are the spec. Any other path emits every heading. Honored by § Changed regions and § Dispatch.

### Decision 16 — The rationale lives in the workflow reference

`docs/spec-workflow-reference.md` states the delta mode and the PET-166 numbers. `AGENTS.md` states the mode and `--full` in the `/spec-cycle` lifecycle item and does not repeat the numbers. Honored by § Docs.

## Design

### Invocation

The invocation line becomes:

```text
/spec-cycle <brief-path> [--attest "<reason>" | --full]
```

That line is written in both places the skill already states it: the H1 `Invoked as` line, and the usage halt in `## Attest mode`. The same line is also the workflow-reference invocation and the `AGENTS.md` lifecycle item, which § Docs names.

`--attest "<reason>"` is unchanged, including attest mode's refusal to run any other phase. `--full` takes no value. Both flags together, `--attest` with no reason or an empty reason, `--full` with a value, or any other flag halts with:

```text
Usage: /spec-cycle <brief-path> [--attest "<reason>" | --full]
```

Nothing is written on that halt. Attest mode does not resolve a review mode and does not read a baseline.

### Mode

Resolve the mode once, after the tier step, and hold it for the invocation. Read `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md` before the pending write replaces it. Take each field as the text after the first `key:` line, trimmed, with one trailing carriage return removed if present.

The six-state reader is not the mode key. Its `missing`, `unreadable`, and `pending` states are rows 2–4 only. `unreadable` in row 3 is that reader's state: no `verdict:` line with one of `green`, `red`, or `pending`, or a `ticket:` line that is absent or names another ticket. A fingerprint that differs, a `fingerprint:` line that is absent or `none`, and a fingerprint that cannot be computed are the reader's `changed` state when `verdict:` is `green`. None of those is a mode row. Text diff and code drift record the byte change. Do not halt for confirmation on `changed`.

Set the candidate round when `source:` is `review` and `round:` matches `^[1-9][0-9]*$`. The candidate is that integer. This includes a marker the reader would call `changed`. When `source:` is not `review`, or `round:` is not that pattern, the candidate is unset. `0`, a leading zero, and an empty value are unset.

Select files only from `docs/specs/TODO/<TICKET-ID>.reviews/round-<candidate>/`. Do not search other rounds. Do not open `docs/specs/DONE/`. A row that names the candidate does not match when the candidate is unset.

A baseline matches only when all three exist in that directory. `spec.copy.md` and `brief.copy.md` are present at any size, including empty. `baseline.commit` is 40 lowercase hex digits followed by one newline, and nothing else. On read, accept either `\n` or `\r\n`. Reject a missing newline, a second line, any other byte, and a `\r` that is not the one carriage return in that `\r\n`.

A ledger is readable only when `ledger.md` exists, is non-empty, and, after every carriage-return byte is removed, its first non-blank line is `closure_manifest (round <digits> → next):` with the same digits as the candidate round. A zero-byte file stays unreadable.

Compare briefs only when `brief.copy.md` is present. Strip every carriage-return byte from both sides. Also drop every line whose first non-blank characters are `**Follow-up:**`, the same line filter the fingerprint uses, so replacing `unfiled` with a ticket id is not a brief change and not a spec change. No other byte is dropped. A missing final newline is a difference.

First match wins:

| # | Condition | Token |
|---|---|---|
| 1 | `--full` was given | `mode: full (--full)` |
| 2 | Marker missing | `mode: full (marker missing)` |
| 3 | Marker unreadable, as defined above | `mode: full (marker unreadable)` |
| 4 | `verdict:` is `pending` | `mode: full (pending)` |
| 5 | `source:` is `operator-attested` | `mode: full (attested)` |
| 6 | Candidate is set, that round's `brief.copy.md` exists, and the filtered brief differs | `mode: full (brief changed)` |
| 7 | Candidate is set, `verdict:` is `green` or `red`, `source:` is `review`, and the baseline does not match | `mode: full (no baseline)` |
| 8 | Candidate is set, the baseline matches, and `ledger.md` is missing or unreadable | `mode: full (ledger unreadable)` |
| 9 | Candidate is set, and `round-<candidate+1>/` or `round-<candidate+2>/` exists | `mode: full (round span occupied)` |
| 10 | Candidate is unset, and rows 1–5 did not match | `mode: full (round unreadable)` |
| 11 | Otherwise | `mode: delta (continuing round <candidate>)` |

Row 5 matches an attested marker whether or not the fingerprint matches the spec. Row 7 matches a review green or review red whose fingerprint would make the reader return `changed`. Row 9 is Decision 8: a delta pass never overwrites an existing round directory, and it reserves both passes. Row 10 includes a review green or red whose `round` is not a positive integer. Row 11 matches only when the candidate is set.

When row 11 matched, compute code drift against the candidate round's `baseline.commit`, as § Changed regions defines it, before printing the preflight token and before the pending write. If any code-drift command fails, a command does not finish, the saved SHA does not resolve, or any listing line is not a raw path, replace the token with `mode: full (code-drift unavailable)`. Do not dispatch a text-only delta. Do not run the no-op. Discard the delta start and compute `start` with the full-invocation rule below before creating any directory. If no free span of `round_cap` directories exists, stop with the marker unchanged and create no directory. Otherwise run the full loop from that `start`. A full pass from this override does not reuse that snapshot; § Artifacts takes a new one at the three-file write. When the token stays delta, hold the snapshot SHA from this computation for the dispatch-time `baseline.commit`. Print whichever token won, in the existing one-line preflight summary, after the tier token.

A full invocation starts at the smallest positive integer `start` such that every directory `round-<start>/` through `round-<start+round_cap-1>/` is absent. Its first pass receives no `closure_manifest` and writes the closure section as `N/A — no closure predecessor`. Its later passes close `round-<previous>/` and take `closure_manifest` from that round's `ledger.md`.

A delta invocation starts at `candidate + 1` only while the token stays delta. It runs only when row 11 matched and neither the code-drift override nor § No-op step 4 replaced the token. Both `round-<candidate+1>/` and `round-<candidate+2>/` are absent on that path. On `small`, `round_cap` is 2, so that pair is the whole full span and this late upgrade does not reach a third directory.

### No-op

Run this only when the held token is `mode: delta (continuing round <candidate>)`. Run it after Phase 1 and before the pending write. Phase 1 on a re-run does not edit the spec, so the code drift computed in § Mode is the result this classification uses. Do not compute it a second time. Steps 1, 2, and 3 always run, in that order. They do not end the classification. Steps 4, 5, 6, and 7 are then tested in order, and the first of them that matches ends the classification.

1. Run the guarantee scan already defined for the green break, against the current spec. If it withholds, this is not a no-op. Print `green withheld: <D-ids> — undischarged in-scope P0/P1` (or the malformed-row line the scan already prints). Do not dispatch from this step. Each withholding row is an open finding on the delta prompt (`guarantee/D-<n>`, or `guarantee/D-?` when the id does not parse). The delta scope includes `## Deferred — follow-up required`.
2. If `correctness.md`, `edge-cases.md`, or `conventions.md` in the candidate round is missing or unreadable, add `<lens>/STATUS (P0)`. When this invocation's scale lens is on, a missing or unreadable `scalability.md` is the same. A stale `scalability.md` while scale is off stays ignored.
3. Changed regions are the § Mode code-drift result unioned with the text diff against the candidate round's `spec.copy.md`. Open findings are the candidate round's unresolved P0 and P1, defined in § Dispatch. `**Follow-up:**` lines are ignored by the same filter as § Mode. A report whose STATUS P0+P1 is greater than zero and that yielded no open heading adds `<lens>/STATUS (P0)`.
4. If the open set contains any `<lens>/STATUS` line, or `verdict:` is `red` and both sets are empty: replace the token with `mode: full (open findings unreadable)`. Discard the delta start. Compute `start` with the full-invocation rule in § Mode before creating any directory. If no free span of `round_cap` directories exists, stop with the marker unchanged and create no directory. Do not print the no-op block. Do not dispatch delta. A `<lens>/STATUS` line names no heading and is not a delta scope. Run the full loop from that `start`. This happens before the pending write.
5. If `verdict:` is `red` and either set is non-empty and the open set contains no `<lens>/STATUS` line: this is not a no-op. Continue to the pending write and dispatch delta. Do not infer redness only from the open-finding set, and do not skip the extraction in steps 2 and 3.
6. If `verdict:` is `green` and the changed-region set is empty and the open-finding set is empty and the scan was clean: print the NO-OP block in this section and stop. Do not write the pending marker. Do not write a copy, a ledger, a synthesis, or a polish section.
7. If `verdict:` is `green` and either set is non-empty and the open set contains no `<lens>/STATUS` line: this is not a no-op. Continue to the pending write and dispatch delta. The delta start stays `candidate + 1`. Scenarios 2b and 10 take this step.

```text
=== NO-OP: <TICKET-ID> ===
Mode: delta (nothing changed, nothing open)
Marker: left as written (<verdict>, round <candidate>)
Spec: docs/specs/TODO/<TICKET-ID>.spec.md
```

`<verdict>` and `<candidate>` are the values left on disk. `--full` and every full-mode token, including `mode: full (code-drift unavailable)` and `mode: full (open findings unreadable)`, skip this classification.

### Two counters

**Cumulative round `C`.** The directory is `round-<C>/`. The marker's `round`, when a pass completes, is `C`. In `## The verdict marker`, replace the `round` value `<1..round_cap>` with `<positive integer>`. The other two tokens, `not reviewed` and `in progress`, stay. Add no field.

**Pass index `P`.** It starts at 1 for each invocation. Reviewers are not told `P`. They are told `round_number: C`.

Full invocation, every tier:

- `P` runs from 1 through `round_cap`. `C = start + P - 1`, where `start` is the span start from § Mode.
- While `P < round_cap`, revise with the ordinary revision rules (route, fold, defer, reject, re-fold recount).
- When `P == round_cap`, run FROZEN/REWRITE as today, then the halt if still loop-red. The FROZEN window is the earlier passes of this invocation, addressed by their cumulative directories. Do not treat a directory left by an older invocation as part of that window.
- The recount reverts an original fold only when `2 ≤ P < round_cap`. It does not revert on the final full pass.
- When `start` is 1, `C` equals `P` and the halt directory is `round-<round_cap>/`, which is today's behavior.

Delta invocation, every tier, at most two passes:

- Pass 1 (`P = 1`): ordinary revision, the rules the full loop uses while `P < round_cap`. This includes a `small` tier, whose `round_cap` is 2. Do not run FROZEN/REWRITE. The recount does not revert on pass 1. Code drift for this pass is the computation § Mode already made.
- Pass 2 (`P = 2`): route every P0 and P1 and fold where the ceiling says fold. Do not classify FROZEN or REWRITE. Do not build a closed-issues rewrite manifest. Before this pass is dispatched, if pass 1's open set contains a `<lens>/STATUS` line, do not dispatch, do not write a green marker, leave the marker pending, print `open findings unreadable: <lens>/STATUS — pass 2 not dispatched; marker left pending`, and stop without Phase 3. A later run takes row 4. The recount may append `(recount: <k> sites, fold kept)` and may not revert, including when the original finding is out-of-scope, because there is no third pass. Text baseline is pass 1's pre-dispatch `spec.copy.md`. Code drift uses pass 1's `baseline.commit`. If that computation fails, a command does not finish, the saved SHA does not resolve, or a listing line is not a raw path, this pass does not go green: print `code-drift: skipped (git error)`, leave the marker pending, delete this pass's `baseline.commit` if it was written, and stop without Phase 3. A later run takes row 4. If the computation succeeds and the pass is still loop-red after the fold, write the red marker at this `C` and print the existing halt menu. Grill reads and writes `round-<C>/`, not `round-<round_cap>/`.
- The pass-2 rule is explicit because `P = 2` is still below `round_cap` on `big` and `irreversible`. Substituting `P` into `P < round_cap` would open a third delta pass. Do not.
- A dispatched pass that returns green, on either counter, breaks the loop, runs post-green polish, rewrites that round's `spec.copy.md` to the post-polish bytes, writes the empty ledger, then Phase 3. It does not rewrite `brief.copy.md`. It does not start the other pass. The code-drift failure in the pass-2 bullet is not a green pass.

The gate formula is unchanged. Loop-red is still `total_p0p1 > 0` or the guarantee scan withheld. Synthesis is still written every dispatched round and is not written on a no-op.

### Artifacts

All four files live in `docs/specs/TODO/<TICKET-ID>.reviews/round-<C>/`. Create the directory before writing. Names:

| File | When | Bytes |
|---|---|---|
| `spec.copy.md` | Immediately before this round's reviewers are dispatched. On the green path only, rewritten after post-green polish and before the green marker. | At dispatch: exact bytes of the spec the reviewers see. After the green rewrite: exact post-polish bytes. A loop-red round is not rewritten. |
| `brief.copy.md` | Immediately before dispatch. Not rewritten. | Exact bytes of the brief file at dispatch. |
| `baseline.commit` | Immediately before dispatch. | The snapshot SHA from § Changed regions: 40 lowercase hex digits and one `\n`. No `\r` anywhere. Not a second `git rev-parse`. |
| `ledger.md` | After this round's revision when the round is loop-red, including the final pass; before the green marker when the round goes green, after the `spec.copy.md` rewrite. | The manifest block in § Ledger. |

`spec.copy.md` at dispatch is the spec the reviewers of this round see. It is written before they are dispatched and before this round's revision. Delta pass 2 diffs against pass 1's pre-dispatch `spec.copy.md`. The green rewrite happens only when that round is going green, so there is no pass 2 on that path. Code drift on a delta pass 1 uses the candidate round's `baseline.commit`. Code drift on pass 2 uses pass 1's `baseline.commit`, so a merge during pass 1 is visible. The brief is compared once, at mode resolution, not again between passes.

Write each round file by temp-then-rename in the round directory. The temp name is `.<filename>.<random>.tmp`. Write the temp, then rename it over the destination. A failed rename leaves an existing destination untouched. Print `<filename> NOT written: <error>` and delete a temp that was not renamed. `baseline.commit` is written as raw bytes, not as a text-mode write that inserts `\r`.

The marker writes use the same temp-then-rename. Pending, red, and green each write `docs/specs/TODO/<TICKET-ID>.reviews/.verdict.md.<random>.tmp` and rename it over `verdict.md`. Do not truncate `verdict.md` in place. A failed rename leaves the previous marker and prints the skill's existing failed-write line. The heading that owns those writes is `## The verdict marker`.

The three dispatch files are one set. Write all three temps first. Rename `spec.copy.md`, then `brief.copy.md`, then `baseline.commit`. If a rename fails, do not dispatch that round, do not write the ledger, and do not start the next pass. Files already renamed stay. The pending marker, if it was written, stays pending.

A later run routes a partial set by the mode table, not by a special case that jumps to row 7 or row 8. A partial set under a pending marker takes row 4. A partial set whose directory is `round-<candidate+1>/` or `round-<candidate+2>/`, while the marker is still the previous green or red, takes row 9. Row 7 or row 8 applies only when the candidate directory itself is missing a member.

On a delta pass, `baseline.commit` is the snapshot SHA § Changed regions already took for that pass's listing. Do not run `git rev-parse HEAD` again at the rename. If HEAD has moved since the snapshot, still write the snapshot. The newer tree is not treated as reviewed. On a full pass, which does not list paths, the snapshot is one `timeout 30 git --no-pager rev-parse HEAD` taken at the start of this three-file write, and that same SHA is what is written. If that command does not finish, or does not print 40 lowercase hex digits, do not write `NONE` and do not invent a SHA. The commit rename fails with `baseline.commit NOT written: <error>`, and the set rule above fires.

`ledger.md` is its own write, after the spec edits of that round. A failed ledger write does not roll back the spec. Print `ledger NOT written: <error>`. The next pass of this invocation reads the file from disk. If that read fails, dispatch that pass as `review_mode: full` with no `closure_manifest`, print `ledger: missing — pass <P> dispatched full`, and do not read an older ledger. The pass budget does not grow. A later invocation sees the missing ledger and takes row 8.

On the pass-2 code-drift failure in § Two counters, delete that pass's `baseline.commit` if the rename already happened. Leave `spec.copy.md` and `brief.copy.md`. Leave the marker pending.

A no-op writes none of the four files and does not write the marker.

### Ledger

The file is the manifest block and nothing else. No title line.

After a loop-red revision, one line per P0/P1 disposition the revision rules already require, including a `guarantee/D-<n>` line and a round-qualified revert line:

```text
closure_manifest (round <C> → next):
  - correctness/F-1 (P1) "title" — fixed: edited § Design
```

The line shape is the shape § 2b already uses, with two edits to that section's sample. The sample header becomes `closure_manifest (round <N-1> → next):`, with `next` the literal word. The sample that re-anchors a finding to a skill file and a line number becomes `fixed: re-anchored to § Design`. The mode check and the on-disk ledger use that same header. A ledger whose first non-blank line says `closure_manifest (round 4 → 5):` is unreadable and takes row 8. A ledger whose first non-blank line says `closure_manifest (round 4 → next):` is readable. The block passed to the next round is the bytes read back from `ledger.md`, not a second in-memory copy and not a block that still teaches a skill-line citation. Build the block from the revision just done, write it, then read `ledger.md` back. The next round's prompt carries the bytes that were read back.

Before the green marker, after post-green polish and after the `spec.copy.md` rewrite:

```text
closure_manifest (round <C> → next):
  (empty — round <C> closed green)
```

That sentence is not a finding line. A zero-byte file is unreadable and selects full mode next time. Polish does not change the ledger: a green round has no P0/P1 dispositions to record. Write the empty ledger even when polish edits the spec.

### Changed regions

**Text.** Strip carriage returns. Drop `**Follow-up:**` lines, same filter as § Mode. Split both texts into headings. A heading is a line that, outside a fence and not prefixed `> `, matches `^#{1,6}\s` (one or more spaces or tabs after the hashes, applied per line, not across a line break). That is the same boundary the skill uses for a tier or scale section. Fences are the ones the Deferred section already defines.

Each heading has an exclusive body: the lines after the heading and before the next heading of any depth. Pair headings in document order by the stack of heading lines from the document title down. The nth heading with a given stack in the current spec pairs with the nth heading with that stack in the baseline. An unpaired heading is an addition or a deletion. Do not key a map by the heading line alone. Do not pair by similarity. A heading is text-changed when its exclusive body, filtered, differs from its paired baseline heading. A heading only in the baseline is emitted as deleted. A heading only in the current spec is emitted with its exclusive body as its hunk. Do not emit an ancestor because a descendant's exclusive body changed.

Bytes before the first heading are a region whose heading is `(before first heading)`. If those filtered bytes differ, emit that region. If the filtered file bytes differ and the pairing, the exclusive bodies, and that leading region still leave the changed-region set empty, emit every heading rather than a no-op.

**Code drift.** Take one snapshot first: `timeout 30 git --no-pager rev-parse HEAD`. Call it `snapshot`. It must be 40 lowercase hex digits. If that command does not finish, the snapshot failed. Changed paths are project-root-relative, forward slashes, the union of these four listings. Each listing is `git --no-pager` wrapped in the same `timeout 30` the skill uses for `git fetch`. `--no-color` does not disable the pager. `--no-pager` does. Each diff command uses `-c core.quotePath=false --no-color --no-renames`. The untracked listing uses `-c core.quotePath=false`. Do not unquote a line by hand. `--no-renames` lists a rename as the old path and the new path.

- `timeout 30 git --no-pager -c core.quotePath=false diff --no-color --no-renames --name-only <saved-baseline-sha> <snapshot>`
- `timeout 30 git --no-pager -c core.quotePath=false diff --no-color --no-renames --name-only`
- `timeout 30 git --no-pager -c core.quotePath=false diff --no-color --no-renames --name-only --cached`
- `timeout 30 git --no-pager -c core.quotePath=false ls-files --others --exclude-standard`

A raw path is one non-empty line, after a trailing carriage return is removed: no leading `"`, no `=>`, no tab, and no backslash. Anything else is not a raw path. Do not unquote it and do not rewrite `\` to `/`. A non-zero exit, a command that does not finish, expiry of `timeout 30`, and any line that is not a raw path are failures. A clean exit whose every line is a raw path is the complete listing. There is no second parser for a truncated or quoted listing.

These failure rules apply only to a delta pass. A full pass does not compute code drift and does not stop because a diff command failed. When row 11 matched and classification is still in progress, a failed command, a saved SHA that does not resolve, or a line that is not a raw path is the § Mode override: the token becomes `mode: full (code-drift unavailable)` and no text-only delta is dispatched. When a delta pass was already dispatched, the same failure is the pass-2 stop in § Two counters: print `code-drift: skipped (git error)`, add no code-drift regions, do not write a green marker, delete this pass's `baseline.commit` if written, leave the marker pending, and stop without Phase 3.

**Which section cites a changed path.** Both tests apply to the heading's exclusive body. Union them with the text-diff headings. Do not pull an ancestor in because the citation sits in a descendant.

Before the citation tests, drop the resolved brief path, the spec path `docs/specs/TODO/<TICKET-ID>.spec.md`, and every path under `docs/specs/TODO/<TICKET-ID>.reviews/` from the changed-path set. A filename-only match does not see a dropped path.

Before either test, strip one trailing locator from a backtick span's inner text. The locator is a suffix matching `:digits`, `:digits-digits`, `:digits–digits` (en dash), or `#Ldigits`. Also remove one leading `./`. A span that still does not match a path after that strip is not a citation. Apply the stripped span to both tests below.

1. **Path citation.** A backtick span whose stripped inner text equals a changed path, or is a suffix of it that begins at a `/` boundary. A span that is only a filename matches a changed path with that filename. A span that contains a directory matches only as that suffix. The match is case-sensitive.
2. **Scope row.** Only inside the exclusive body of `## Scope`. A table row or list item that contains a backtick path, compared after the same strip, and a `§` reference links that path to each section the `§` names. When the path is changed, those sections are changed regions. A row that names a changed path and names no section adds `## Scope` only. It does not pull in the rest of the spec.

A code-drift hit whose exclusive body did not change still counts. Its hunk is the single line `(no text change — cited file <path> changed since <sha>)`. The explorable region for that heading is its exclusive body. A descendant is explorable only when that descendant is itself listed.

**Open-finding sections.** A heading named by an open finding's `Where` is in the delta scope even when its exclusive body is unchanged. Emit it with the hunk `(open finding <lens>/<id> — no text hunk)`. Split `Where` on `;` and resolve each clause on its own. A clause that cites `spec.md`, the ticket's `*.spec.md` filename, or the repo-relative spec path cites this spec. Any other path emits every current heading for that clause rather than mapping that file's line number into the spec. After `§` or a heading marker, take the phrase up to a comma. Select every current heading whose text equals that phrase, or whose text is the longest heading-text prefix of that phrase (`No-op` matches `No-op step 4`; `Mode` matches `Mode lines 162–164`). If more than one heading matches, emit all of them. A matching heading does not also use the line. If no heading matches and the clause has a line number, resolve that line against the predecessor `spec.copy.md`: the candidate round's copy on delta pass 1, and pass 1's pre-dispatch copy on delta pass 2. Take the innermost heading in that copy whose heading line is that line or whose exclusive body contains it. Emit that heading's pair in the current spec, using the stack pairing above. A paired heading that was deleted is emitted as a deletion. If a clause has neither a matching heading nor a placeable line, emit every current heading. Do not let a non-matching `§` phrase discard the line. Emitting the document title's exclusive body is not a substitute for that every-heading case.

### Dispatch

The pending write is unchanged in contents and still happens once per invocation, immediately before the first dispatch. It does not happen on a no-op. It still replaces whatever marker was there. It uses the temp-then-rename in § Artifacts.

Before every dispatch, full or delta, save the three-file set in § Artifacts. Then dispatch the lenses this invocation already resolved: the three standing lenses, plus scalability when `scale_lens` is on. One parallel message.

Every reviewer prompt gains:

- `review_mode: full` or `review_mode: delta`
- `round_number: <C>` — a positive integer, not capped at 4

When `review_mode` is `delta`, the prompt also carries `changed_regions` and `open_findings` in this shape:

```text
changed_regions:
  - heading: "## Design"
    hunk: |
      <the exclusive body's diff hunk, or the code-drift line, or the open-finding line>
  - heading: "### Old name"
    deleted: true
open_findings:
  - correctness/F-2 (P1) "title" — § Design
```

`closure_manifest` is present only when this pass has a closure predecessor. It is the bytes of the previous round's `ledger.md`. The first pass of a full invocation omits it. A delta pass 1 includes it: the candidate round's ledger. A later pass includes the ledger written for `C - 1`.

**Open findings, extracted, not recalled.** From each lens report in the predecessor round (`correctness.md`, `edge-cases.md`, `conventions.md`, plus `scalability.md` only when this invocation's `scale_lens` is on). Ignore `synthesis.md`. Ignore a stale `scalability.md` when scale is off. A finding is open when it is a `### F-<k>:` heading in that report whose severity is P0 or P1. The predecessor round is the last completed round, so no later review has closed them. Do not drop one because that report's own closure table mentions it. Do not include P2 or lower. A report with no parseable `STATUS:` line adds `<lens>/STATUS (P0) "missing STATUS line"`. A standing-lens report that is missing or unreadable adds the same `<lens>/STATUS (P0)` line. A report whose STATUS P0+P1 is greater than zero, and that yielded no `### F-<k>:` heading of severity P0 or P1, adds `<lens>/STATUS (P0) "STATUS count without a finding heading"`. A `<lens>/STATUS` line names no heading. It does not select delta. § No-op step 4 takes `mode: full (open findings unreadable)` when any such line is present. When the predecessor went green, every standing report exists and parses, and none of those reports contains a P0 or P1 heading, the set is empty.

Delta pass 2 uses pass 1's reports as the predecessor, and pass 1's pre-dispatch `spec.copy.md` as the text baseline. Each `Where` clause is resolved as § Changed regions defines, against that same copy when the clause uses a line, and the prompt receives the paired heading in the current spec.

A full pass omits `changed_regions` and `open_findings`. The reviewer treats a missing `review_mode` as `full`.

### Delta contract

Insert the following into all four agents, after the `tier` input bullet. Insert the behavior section after grounding step 7, before the critique lens. Do not place either inside the Deferred-findings block. Do not add a line number, a `SKILL.md` path, or any path under this repo's `skills/`, `agents/`, or `docs/` trees. The target project's `docs/specs/TODO/<TICKET-ID>.reviews/` path, which step 7 already uses, may stay.

Input bullets, all four agents. Replace the `round_number` parenthetical `(1–4)` with `(a positive integer, the cumulative review round)`:

```text
- `review_mode` — `full` or `delta`. Absent means `full`. When `full`, review the whole spec. When `delta`, new critique is limited to `changed_regions` and `open_findings`.
- `changed_regions` — present only for `delta`. Each entry is a Markdown heading plus a diff hunk, or `deleted: true` for a heading that was removed. A heading covers its exclusive body only. This is the only list of sections you may newly explore.
- `open_findings` — present only for `delta`. The prior round's unresolved P0 and P1 findings. Their headings are in scope even when the hunk says the text did not change.
```

`closure_manifest` stays, with one change to its guard: it is present when this pass has a closure predecessor, not merely when `round_number` is at least 2. In all four agents, replace step 7's condition `If round_number ≥ 2` with `If a closure_manifest was provided`. Under `# Output contract` in all four agents, replace the parenthetical `(Required for round_number ≥ 2; "N/A — round 1" otherwise.)` with `(Required when a closure_manifest was provided; "N/A — no closure predecessor" otherwise.)`. When none was provided, the closure section body is `N/A — no closure predecessor`, including when `round_number` is greater than 1.

Behavior section, all four agents, verbatim:

```text
# Delta scope

Apply this only when `review_mode` is `delta`. When it is `full` or absent, skip this section.

Read the spec (grounding step 1), run the Deferred-findings block, verify closures, check vanished references, and record process failures exactly as you do on a full pass. Those checks are not limited to `changed_regions`.

Apply your critique-lens questions only to headings named in `changed_regions` or in `open_findings`. A named heading covers its exclusive body only: the lines after that heading and before the next heading of any depth. A descendant heading is in scope only when it is itself named. Do not explore any other region. Do not file a finding whose claim is that a Decision outside that scope should be a different decision. A changed section that contradicts a Decision outside the scope is in scope: file it against the changed section.

A line whose id is `<lens>/STATUS` names no heading. It is not a changed region and not an open-finding heading. Ignore it as scope.

A P0 you meet while doing a check this section still requires (you were not hunting an unchanged region for it) may be filed. Cite the evidence. It counts in the gate. Do not open an unchanged section to look for one.
```

Anchor paragraph, all four agents, in the critique lens, not in the Deferred-findings block. In the correctness agent, replace both the **Stale anchors** bullet and numbered item 2 of the cross-section walk with this paragraph. Do not leave a sentence that every stale anchor is a P1, and do not leave the instruction to re-grep the cited line. In the other three agents, add the paragraph. It applies in both modes:

```text
Anchor drift. For a file:line citation, re-check the symbol at the current file. If the symbol is gone, file a P1, one finding per dead citation. If the symbol still resolves and only the line number moved, do not file a P1. File those moved citations once per report, as one combined P4, listing each of them in that finding. Do not file one finding per moved line.
```

Correctness only, immediately after step 7 has read the predecessor reports. Skip it when no `closure_manifest` was provided:

```text
Ledger check. Compare `closure_manifest` with the P0 and P1 findings in the predecessor reports you just read for the closure table. A report finding counts when it has a `### F-<k>:` heading and severity P0 or P1. The manifest covers it when a line matches the id as a token, `(^|[^A-Za-z0-9])<lens>/F-<k>([^0-9]|$)`, and the severity `(P0)` or `(P1)` sits on that same line immediately after the id and before the title. A match inside a quoted title, or inside a longer id, is not coverage. A report with no parseable STATUS line is covered only when a line matches `<lens>/STATUS` as a token, `(^|[^A-Za-z0-9])<lens>/STATUS([^A-Za-z0-9]|$)`. A `guarantee/D-<n>` line and a round-qualified `<lens>/R<m>/F-<k>` line are legal extras; do not flag them as unknown. P2 and lower findings are not required. If one or more required lines are missing, file one P0 titled `ledger omits a P0/P1 line`. Name every missing id in that finding. Do not file one P0 per missing line.
```

The four Deferred-findings blocks stay byte-identical to each other and byte-identical to their text before this change.

### Stop screens

Append this paragraph to the halt block, above `What would you like to do?`, and to the Phase 3 block, above `=== NEXT ===`. Same words on both screens:

```text
DRIFT: a merge into a file this spec cites, while this review is open, restarts the churn a delta pass exists to stop. If those files change, re-run /spec-cycle before the next pass.
```

The halt menu's options, the GREEN WITHHELD case, the follow-up report, and the grill's one-shot rule are unchanged. The round number printed in `SPEC NOT GREEN AFTER <N> ROUNDS` is the cumulative `C` of the pass that halted. Remaining titles come from that round's reports. Grill persists to `round-<C>/grill.md`.

In `### 2f-i`, the seed read, the `grill.md` persist, and the re-render path use `round-<C>` on every halt. The row templates that step writes do too: `Deferred in: round <C> (grill)` and `Scope: operator — round-<C> grill`, in the revise step and in the deferred-row template. That equals `round-<round_cap>` only when the full invocation started at round 1. A delta halt uses the same heading.

The no-op block does not carry this warning. The no-op is not a stop screen. The pass-2 code-drift stop is not this halt menu: it leaves the marker pending and prints `code-drift: skipped (git error)`. The pass-2 `<lens>/STATUS` stop is not this halt menu either: it leaves the marker pending and prints `open findings unreadable: <lens>/STATUS — pass 2 not dispatched; marker left pending`.

### Docs

In `skills/spec-cycle/SKILL.md`:

- `## The verdict marker`, paragraph `**Write points.**`: pending is written once per invocation, immediately before the first dispatch, and is not written on a no-op. Red is written at the halting pass's cumulative round. Green is written after post-green polish. All three use the temp-then-rename in § Artifacts.
- `## Failure modes to watch for`, bullet `**Interrupted run.**`: a partial `spec.copy.md` / `brief.copy.md` / `baseline.commit` set may remain, and the marker stays pending. Re-run takes row 4 when the marker is pending.

In `docs/spec-workflow-reference.md`, in **Skill 1: spec-cycle**:

- The invocation line gains `[--full]`, exclusive with `--attest`.
- `### Phase 2`, the paragraph `**Round 2+ closure tracking:**`, describes the first invocation's pass index. A full invocation's first pass has no closure predecessor even when its cumulative round is greater than 1. A delta pass 1 closes the candidate round. The same sentence is applied to the adapting bullet `**Round 2+ closure tracking.**` so the two copies do not disagree.
- `### Verdict marker`: `round` is any positive completed review round, or `not reviewed`, or `in progress`. Pending is once per invocation before the first dispatch, not on a no-op, and not tied to the label "round 1". Red is the halting pass's cumulative round, which is `round_cap` only when the full invocation started at round 1. Green is after polish. No new field.
- `### Stakes tier`, the paragraph that says `round == round_cap` is the FROZEN/REWRITE rewrite: that sentence describes the first invocation's pass index `P`, not the cumulative round. A delta pass whose cumulative round equals `round_cap` does not run FROZEN/REWRITE.
- The same pass-index reading applies to the remaining single-counter sentences: `### The grilling contract` under Skill 0 (the grill follows `round_cap` rounds, and it also follows a delta halt at cumulative `C`); the Phase 2 introduction that calls the final round, `round == round_cap`, the rewrite, including its steps that halt and rewrite there with a FROZEN window of rounds `1 .. round_cap-1`; and the adapting bullet `**Targeted rewrite at round round_cap**`. A full invocation whose start is not 1 rewrites and grills at cumulative `C`.
- A rationale paragraph states these PET-166 numbers, transcribed from the ticket, and no others: 58% of findings in rounds 2–5 and 54% in rounds 6–10 targeted text added to satisfy earlier findings; genuine misses dried up after round 2 (about 12%); 3 of the 5 P0-class defects were manufactured by earlier remediations; the round-11 delta close-out verified 26 closures and surfaced 2 findings, both P2s, against about 30 findings per full-lens round in rounds 7–10.
- Skill 1 states the delta mode itself. A re-run is at most two delta passes over changed regions and open P0/P1s. A clean no-op leaves the marker as written. `--full` or a mode-table row forces a full pass. That sentence is the re-run reading of the Phase 2 introduction, which today says each lens reviews the spec with revision while `round < round_cap`. The first invocation's loop stays the full review.

In `skills/spec-cycle/SKILL.md`, `## Tool-use notes` gains the read-only code-drift commands beside `git rev-parse`, each as `git --no-pager` wrapped in the same `timeout 30` as `git fetch`: `git diff --name-only` with `-c core.quotePath=false --no-color --no-renames`, the same command with `--cached`, and `git ls-files --others --exclude-standard` with `-c core.quotePath=false`. The snapshot `git rev-parse HEAD` uses the same `timeout 30` and `--no-pager`. The sentence that calls `git merge --ff-only` the lone git-level mutation of tracked files stays. These commands do not change tracked files.

In `AGENTS.md`, the `/spec-cycle` lifecycle item states that a re-run runs at most two delta passes unless `--full` is given or the mode table forces a full pass, and that the first invocation is unchanged. It names `--full`. It does not carry the PET-166 numbers. The `/spec-brief` lifecycle item's grill clause states that the grill also follows a delta halt at cumulative round `C`, not only the halt after `round_cap` rounds. The `AGENTS.md` row in § Scope is the whole file, so that adjacent bullet is in scope.

### Scenarios

Each row is the outcome this design produces. `round_cap` is 4 except in the small-tier row. A review-green marker whose fingerprint does not match the spec still sets the candidate when `source:` is `review` and `round:` is a positive integer.

**1. First delta pass after a red halt.** Marker `red`, `source: review`, `round: 4`, baseline matches, ledger readable, brief unchanged, `round-5/` and `round-6/` both absent, scan clean, at least one open P0/P1. Mode `delta (continuing round 4)`. Pass 1 is cumulative round 5 and revises. The pending marker is written before that dispatch. If pass 1 goes green: `spec.copy.md` rewritten to the post-polish bytes, empty ledger, marker `green`, `round: 5`, `gate: 0`, no halt. If pass 1 stays loop-red: the pre-dispatch copy stays, ledger written, pass 2 is cumulative round 6, folds without FROZEN/REWRITE. If pass 2 goes green: marker `green`, `round: 6`. If pass 2 stays loop-red: marker `red`, `round: 6`, `gate` equal to that round's P0+P1 sum, halt menu, grill directory `round-6/`.

**2. First delta pass after a green, nothing changed.** Marker `green`, `source: review`, `round: 2`, empty ledger readable, filtered spec equal to the saved `spec.copy.md` (the post-polish bytes, because the green path rewrote it), filtered brief equal, no cited file changed, code drift succeeds, scan clean, the three standing reports exist and parse, no open P0/P1. Mode resolves to delta, then the no-op fires. No round is taken. Marker stays `green`, `round: 2`. The printed marker line says `green`. No halt. Output is the NO-OP block.

**2b. After a green, the spec text changed.** Same marker, including when the fingerprint no longer matches and the six-state reader would return `changed`. The filtered spec differs from `spec.copy.md`. Candidate is 2. Not a no-op. Pass 1 is cumulative round 3, delta scope is the changed exclusive bodies. A green pass writes marker `green`, `round: 3`, and rewrites `spec.copy.md` to the post-polish bytes. A red pass continues under the delta pass-2 rule: cumulative round 4, fold, no FROZEN/REWRITE, halt if still red.

**3. Small-tier continuation.** `round_cap` is 2. The first invocation is unchanged: pass 1 revises at round 1, pass 2 is FROZEN/REWRITE at round 2, and a red result halts at round 2. A re-run after that red halt, baseline and ledger good, brief unchanged, `round-3/` and `round-4/` both absent: mode delta. Pass 1 is cumulative round 3 and uses ordinary revision, not FROZEN/REWRITE. Pass 2 is cumulative round 4, folds without FROZEN/REWRITE, and halts if still loop-red. Grill directory is `round-4/`. `P = 2` is not treated as `P < round_cap`.

**4. Delta pass 2 still red, then the grill.** Continuation of scenario 1's pass 2. After the fold the round is still loop-red. Marker `red`, `round: 6`, `gate` equal to the STATUS sum, which is 0 when only the scan withheld. The halt menu is the existing one. When reviewer P0/P1 titles remain, options 1–4 are offered and option 4 reads and writes `round-6/`. When no reviewer P0/P1 remains, Remaining is `GREEN WITHHELD: <D-ids>` and option 4 is not offered.

**5. Attested green.** Marker `green`, `source: operator-attested`, `round: not reviewed`. Mode `full (attested)` whether or not the fingerprint matches. The candidate is unset. Start at the smallest span of `round_cap` free directories (1 through `round_cap` when none exist). First pass has no closure predecessor. Pending replaces the attested marker at dispatch. A green result writes `green` at that cumulative round. A run that stays red halts when the pass index equals `round_cap`, with FROZEN/REWRITE on that pass. No delta pass runs.

**6. Changed brief.** A review marker with a matching baseline whose filtered `brief.copy.md` differs from the current brief. Mode `full (brief changed)`, even if the spec is unchanged. Start at the smallest free span. No closure predecessor. Not a no-op. The full loop's halt applies if it stays red through `round_cap` passes.

**7. Absent baseline.** Marker `green` or `red`, `source: review`, `round: 3`, and `round-3/` is missing `spec.copy.md` or `brief.copy.md` or a valid `baseline.commit`. Mode `full (no baseline)`. Do not read `round-2/`. Do not read `docs/specs/DONE/`. Start at the smallest free span. That run writes the first copy before its first dispatch and prints `mode: full (no baseline)`. A `baseline.commit` of 40 hex digits plus `\r\n` is valid on read and does not take this row. A zero-byte ledger is not this row; it is row 8.

**8. Pending marker.** Marker `pending`, `round: in progress`, and `round-1/` plus `round-2/` exist. Mode `full (pending)`. Start at the smallest `start` whose span `start` through `start+round_cap-1` is entirely free. When `round-3/` through `round-6/` are all absent, start is 3. When any of that span exists, start is the next integer whose whole span is free. Do not overwrite `round-2/` or any directory already present. First pass has no closure predecessor. Later passes of this invocation close the pass before them, starting with that start, not round 2.

**9. After spec-close archived the spec.** spec-close moves `docs/specs/TODO/<TICKET-ID>.reviews/` to `docs/specs/DONE/<TICKET-ID>/reviews/` and the spec to `docs/specs/DONE/<TICKET-ID>/spec.md`. A later `/spec-cycle` sees no marker in `docs/specs/TODO/`. Mode `full (marker missing)`. The DONE tree is not a baseline, including when its `round-<N>/spec.copy.md` is intact. If the operator left a marker in TODO without the three-file set, row 7 applies instead (`no baseline`). Phase 1 authors a TODO spec when one is not already there. The run starts at round 1 when no TODO round directory exists.

**10. Code changed, spec and brief unchanged.** Marker `green`, empty ledger, filtered spec equal to the post-polish `spec.copy.md`, filtered brief equal, scan clean, standing reports present, and at least one cited file differs from `baseline.commit`. Not a no-op. Mode `delta (continuing round <R>)`. Open findings are empty. Changed regions are the citing headings' exclusive bodies and any Scope row that names both that path and a section. A citation whose only form is a backtick span `` `skills/spec-cycle/SKILL.md:388` `` still matches, after the locator strip, and the outcome is still not a no-op. The same strip covers `:digits-digits`, an en-dash range, and `#Ldigits`. Pass 1 is cumulative round `R+1`. The closure manifest is the empty ledger. The correctness ledger check finds no omitted P0 or P1. A green pass writes marker `green` at `R+1` and rewrites `spec.copy.md` to the post-polish bytes.

**11. Ledger keeps a longer id and drops the shorter one.** Predecessor reports contain `correctness/F-1` (P1) and `correctness/F-10` (P1). The saved ledger has a line `correctness/F-10 (P1) "..."` and no line whose token is `correctness/F-1`. The correctness lens files one P0 titled `ledger omits a P0/P1 line`, and that finding names F-1. It does not treat the F-10 line as coverage for F-1. The same holds when the omitted id appears only inside another line's quoted title.

**12. Code drift cannot be computed.** Spec and brief match the saved copies, open findings are empty, scan clean, and `git diff` or `git ls-files` fails, a command does not finish within `timeout 30`, or the saved SHA does not resolve. While classifying, the token is `mode: full (code-drift unavailable)`. The run is the full loop, not a text-only delta, and not a no-op. `start` is recomputed by § Mode, and the failed snapshot is not reused. Separately, if delta pass 1 was already dispatched and pass 2's code-drift computation then fails, including by `timeout 30`: print `code-drift: skipped (git error)`, do not write a green marker, delete that pass's `baseline.commit` if written, leave the marker pending, and stop without Phase 3. The next run takes row 4.

**13. Occupied span, and a round that is not a positive integer.** Marker `green` or `red`, `source: review`, `round: 4`, baseline and ledger good, `round-5/` absent, `round-6/` present. Mode `full (round span occupied)`. Start at the smallest free span of `round_cap` directories, which is not 5. A review marker whose `verdict:` is `green` or `red` and whose `round:` is missing, `not reviewed`, `in progress`, or not a positive integer takes `mode: full (round unreadable)` and does not start a delta.

**14. A cited file was renamed.** Marker `green`, filtered spec and brief equal the saved copies, scan clean, no open P0/P1, and a file cited in an exclusive body was renamed since `baseline.commit`. The listing uses `--no-renames`, so both the old path and the new path are changed paths. The old path matches the citation. Not a no-op. Mode stays `delta (continuing round <R>)`. Pass 1 is cumulative round `R+1`. `baseline.commit` for that pass is the snapshot the listing used. If HEAD moves after the snapshot and before the file is saved, the saved SHA is still the snapshot.

**15. Red marker, no parseable P0/P1 heading, nothing else changed.** The filtered spec matches, code drift is empty, and the scan is clean. Either (a) a standing report is missing, has no STATUS line, or has STATUS P0+P1 greater than zero with no `### F-<k>:` heading of that severity, so the open set contains `<lens>/STATUS (P0)`, a line that names no heading; or (b) the changed-region set and the open-finding set are both empty. In both arms the run is `mode: full (open findings unreadable)`: not a delta, not an empty delta dispatch, and not a green write over the red marker. `start` is recomputed by § Mode. Scenario 16 is the case where that start is not `candidate + 1`. The same `<lens>/STATUS` line met after delta pass 1 does not dispatch pass 2: the run prints `open findings unreadable: <lens>/STATUS — pass 2 not dispatched; marker left pending` and stops with the marker pending.

**16. Red marker, both sets empty, a later round directory exists.** Marker `red`, `source: review`, `round: 4`. `round-1/` through `round-4/` exist. `round-5/` and `round-6/` are absent. `round-7/` exists. No other round directory exists. Filtered spec and brief match, code drift is empty and finishes, the scan is clean, and both finding sets are empty. Row 11 matches. § No-op step 4 replaces the token with `mode: full (open findings unreadable)` and discards the delta start 5. The span 5 through 8 contains `round-7/`, so `start` is not 5. The smallest free span of 4 directories is 8 (`round-8/` through `round-11/`). `round-7/` is not overwritten. If no span of `round_cap` directories is free anywhere, the run stops and the marker stays `red` at round 4.

**17. A line-only Where moved.** Delta pass 2, or a re-run after a red halt. An unresolved P0 or P1 has a line-only `Where` and no heading title. That line falls in `### Mode` of the predecessor `spec.copy.md`. The current spec inserted lines above that section, so the same line number now falls in a different heading, and `### Mode`'s exclusive body is unchanged. The open-finding section is the current `### Mode`, the pair of the predecessor heading, not the heading that now contains the old line number. A `Where` of `§ Mode` matches by title and does not use the line. A `Where` whose path is not the spec emits every current heading. A line that cannot be placed in the predecessor copy emits every current heading. `spec § No-op step 4, line 173` matches the heading `No-op` by prefix and does not use the line. `spec § Mode lines 162–164` matches `Mode`. `spec § Changed regions, line 288` matches `Changed regions`. `spec.md:173` cites the spec; with no heading phrase it uses the line in the predecessor copy.

**18. Untracked brief and spec, nothing else changed.** Marker `green`, filtered spec equal to `spec.copy.md`, filtered brief equal to `brief.copy.md`, scan clean, no open P0 or P1, and no cited implementation file changed. The brief and the spec are untracked, so `git ls-files --others --exclude-standard` lists them. Those paths, and any path under `<TICKET-ID>.reviews/`, are dropped before the citation tests. The H1 citation of the brief does not count. The result is the no-op.

## Test plan

No new test module. The behavioral oracle is the scenario list above, checked by reading the edited skill. The automated gate is the repo's lint and unit suite, which must stay green because this change does not alter `lint.py` or `tests/`.

Review checklist, after the edits:

- Invocation accepts `--full` and rejects it together with `--attest`. Both the H1 `Invoked as` line and the `## Attest mode` usage halt carry the usage line in § Invocation.
- Mode rows 1–11 print the tokens in § Mode. A fingerprint mismatch does not by itself select a row. Row 9 does not overwrite a directory in the reserved span. A delta classification whose code drift fails, including a command that does not finish within `timeout 30`, prints `mode: full (code-drift unavailable)` and recomputes `start`.
- The no-op block matches § No-op, the marker is untouched, the printed verdict is the one on disk, and a withheld guarantee scan, a red marker with a non-empty set, a green marker with a non-empty set, or a red or green marker whose open headings are real findings still dispatches. A missing standing-lens report, a `<lens>/STATUS` line, or a red marker with both sets empty recomputes `start`, does not dispatch delta, and does not overwrite a later round directory. A `<lens>/STATUS` line in delta pass 1's open set stops before pass 2 with its printed line and a pending marker.
- `round-<C>/` contains `spec.copy.md`, `brief.copy.md`, and `baseline.commit` written before dispatch. On green, `spec.copy.md` is rewritten to the post-polish bytes before the green marker. `ledger.md` is written after a red revision or, empty, before a green marker. Marker writes use temp-then-rename. `baseline.commit` is raw LF on write and accepts LF or CRLF on read.
- A delta pass 2 folds without a FROZEN/REWRITE manifest. A full invocation whose start round is 1 still runs FROZEN/REWRITE on the pass whose index equals `round_cap`. The whole span is free before the first directory is created.
- The four agents contain the delta input bullets, the delta-scope section with the exclusive-body rule, the anchor paragraph, and the output-contract parenthetical from § Delta contract. The correctness agent contains the token ledger check, and neither the **Stale anchors** bullet nor numbered item 2 remains. None of those insertions cite a skill line or a path in this repo.
- The four Deferred-findings blocks are unchanged and still byte-identical to each other.
- `docs/spec-workflow-reference.md` carries the PET-166 numbers from § Docs, states that a re-run is at most two delta passes, that a clean no-op leaves the marker, and that `--full` or a mode-table row forces a full pass, and its Stakes-tier and Round 2+ closure paragraphs describe the pass index. `AGENTS.md` names delta mode and `--full`, names the delta halt in the spec-brief item, and does not carry those numbers.
- The halt screen and the Phase 3 screen both contain the DRIFT paragraph.
- Scenario 11's ledger, with F-10 present and F-1 absent, is one P0 naming F-1. A ledger headed `round 4 → 5` is row 8 unreadable. A ledger headed `round 4 → next` is readable. Scenario 10's locator-only citation is not a no-op. Scenario 14's rename lists both paths and is not a no-op. Scenario 15 does not write green over a red marker from an empty delta or from a `<lens>/STATUS` line; that line is a full pass. Scenario 16 does not start at 5 and does not overwrite `round-7/`. Scenario 17 keeps the heading for a suffixed `§` phrase. Scenario 18's untracked brief and spec are a no-op.
- `## Tool-use notes` lists the code-drift commands as `git --no-pager` with `timeout 30`. `### 2f-i` uses `round-<C>`. The workflow-reference sentences named in § Docs describe pass index `P`.

## Test command

```text
python lint.py --strict
python -m unittest discover -s tests -p "test_*.py"
```

Run both from the repo root. `lint.py --strict` must report 0 errors. The unit suite must pass. Neither command executes the scenarios. The checklist above is the check for those.

## Done when

- `skills/spec-cycle/SKILL.md` encodes the delta trigger (§ Mode, § No-op), the delta pass contract (§ Two counters, § Dispatch, § Delta contract), and the ledger rule (§ Ledger). The four reviewer agents accept `review_mode`, `changed_regions`, and `open_findings`, and they verify closures when a manifest is provided. — § Scope, § Delta contract
- A delta pass on a spec with zero changed regions and zero open P0/P1 findings is a no-op that reports green and does not run a full pass. — § No-op, scenario 2 (the no-op is the green marker in scenario 2; a red marker with both sets empty is the full pass in scenario 15)
- A synthetic prior-round P0 or P1 omitted from the saved ledger is one blocking P0 from the correctness reviewer, titled `ledger omits a P0/P1 line`. A longer id does not cover a shorter one. — § Delta contract, ledger check, scenario 11
- `docs/spec-workflow-reference.md` states the rationale with the PET-166 numbers. — § Docs
- The spec walks the first delta pass after a red halt (scenario 1) and after a green (scenarios 2 and 2b).
- The spec walks a `small`-tier continuation, whose review limit is 2 (scenario 3).
- The spec walks delta pass 2 still red, then the grill option (scenario 4).
- The spec walks an attested green (scenario 5), a changed brief (scenario 6), an absent baseline (scenario 7), a pending marker (scenario 8), and a run after spec-close archived the spec (scenario 9).
- The spec walks code that changed since the saved commit while the spec and the brief did not (scenario 10), including a locator-only citation.

## Out of scope

- FROZEN/REWRITE in a full invocation. It does not run in a delta pass. Making it run there is a change this spec does not make.
- The routing rules and the gate formula. A delta pass uses them as they are, except delta pass 2 keeps a recount fold and does not revert, including when the original finding is out-of-scope, as Decision 8 states. Synthesis still does not change the STATUS sum.
- An author-side check script. That is VHS-26.
- A new verdict-marker field. Only the `round` value's range widens.
- P2 and lower findings in the closure manifest or the saved ledger.
- The tier re-run pin and the scale re-run pin. Changing either still means editing the spec.
- Reading `docs/specs/DONE/` as a baseline, and any edit to spec-close's archive move.
- Edits to ship-spec or spec-tickets. They already treat `round` as opaque.
- A fuzzy heading-rename detector. A rename is recorded as a deletion plus an addition.

## Deferred (P2+)

- correctness/F-4 (P3) ticket not cached — no spec change. Shared memory and the tracker were unavailable; the brief is the source for Decisions 1–16 and Done when. Round 2 re-filed the same grounding note. Round 3 re-filed it again. Round 4 re-filed it again. Still no spec change.
- round 5 (delta) correctness/F-2 and edge-cases/F-2 (P2) a prefix match on a parent or wrong heading discards the cited line — changes the match rule, so not polish. Suggested: when a clause has both a matching heading and a line, resolve the line too and emit the union; require the prefix to end at a non-alphanumeric boundary.
- round 5 (delta) edge-cases/F-1 (P2, pre-ship recommended) an abbreviated heading title with no line (`spec § Decision 8`) matches nothing and emits every heading — changes the match rule, so not polish. Suggested: a third arm that selects headings whose text begins with the phrase at a non-alphanumeric boundary.
- round 5 (delta) edge-cases/F-3 (P2, pre-ship recommended) and correctness/F-4 (P3) other tickets' untracked `*.reviews/` trees and `*.attempt-*/` archives still count as code drift for a filename-only citation, so the no-op does not fire for a spec that backticks such a filename — changes the drop rule, so not polish. Suggested: drop every path under `docs/specs/TODO/` matching `*.reviews/` or `*.attempt-*/`.
- round 5 (delta) edge-cases/F-4 (P2), second half: dispatching pass 2 as a full review instead of stopping on a `<lens>/STATUS` line — a behavior change, so not polish. The printed line was folded; see Post-green polish.
- round 5 (delta) edge-cases/F-5 (P3) a clause with two `§` references or a line range is unspecified.
- round 5 (delta) conventions/F-2 (P3) the `<lens>/STATUS` paragraph in the agents' `# Delta scope` block covers a case the skill no longer sends; keep as a version-skew guard or drop.

## Post-green polish

Applied after the round-5 delta pass (gate 0), clarifications only:

- correctness/F-1, edge-cases/F-4, conventions/F-1 (round 5) — the pass-2 `<lens>/STATUS` stop now prints a named line; added to § Two counters, § Stop screens, scenario 15 and the test plan. Decision 8 was not edited.
- correctness/F-3, edge-cases/F-6, conventions/F-3 (round 5) — scenario 15 rewritten as two arms with one outcome sentence.
- conventions/F-4 (round 5) — the prefix example now exercises the prefix arm; two leftover rationale clauses removed from § No-op step 3 and § Dispatch.
