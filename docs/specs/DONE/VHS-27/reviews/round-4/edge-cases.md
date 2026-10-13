The round-3 folds are in the spec. One open-finding form still drops the section a red re-run has to re-check.

# Edge-Cases Review — round 4

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | A late full upgrade keeps the two-directory delta start | CLOSED | spec § Decision 8 line 72 and § Decision 14 line 96 discard `candidate + 1` and recompute `start`; § Mode lines 160–164 and § No-op step 4 line 173 stop with the marker unchanged when no span of `round_cap` is free; scenario 16 line 436 starts at 8 and does not overwrite `round-7/`; test plan lines 448 and 455 |
| edge-cases | F-2 | A line-only Where is placed in the spec after the revision, so the open section drops out | CLOSED | spec § Decision 15 line 100, § Changed regions line 289, and § Dispatch line 319 resolve a line-only Where in the predecessor `spec.copy.md` and emit that heading's pair; scenario 17 line 438; test plan line 455. The suffixed house form is a new finding below, not this defect |
| edge-cases | F-3 | Code-drift commands have no deadline, so a hung git never becomes the failure token | CLOSED | spec § Changed regions lines 269–275 wrap every listing and the snapshot in `timeout 30 git --no-pager`; expiry is a failure; § Docs line 396, scenario 12 line 428, test plan lines 447 and 456 |
| correctness | F-1 | A green marker with a non-empty delta has no classified exit | CLOSED | spec § No-op step 7 line 177 continues to the pending write and keeps `candidate + 1`; scenario 2b line 408 |
| correctness | F-2 | The empty-pair Done-when sentence covers only the green no-op | CLOSED | spec § Done when line 470: the no-op is scenario 2; a red marker with both sets empty is scenario 15 |
| correctness | F-3 | ticket not cached | CLOSED | spec § Deferred (P2+) line 493 records no spec change. Re-filed below; this run was also told not to call shared memory |
| conventions | F-1 | Ledger sample still teaches the old header while mode requires the word `next` | CLOSED | spec § Ledger lines 250–251: the § 2b sample header becomes `closure_manifest (round <N-1> → next):`; `round 4 → 5` is row 8; test plan line 455 |
| conventions | F-2 | The workflow-reference edit list never states the delta mode | CLOSED | spec § Docs line 394 states the two-pass re-run, the clean no-op, and `--full`; test plan line 453 |
| conventions | F-3 | Delta pass 2 keeps an out-of-scope recount fold | CLOSED | spec § Decision 8 line 72 and § Two counters line 204: pass 2 keeps the fold and does not revert, including when the original finding is out-of-scope |

Round-qualified folds named in the manifest are still present: locator strip at § Changed regions lines 281–284 and scenario 10; exclusive-body pairing at lines 265 and 280 and § Delta contract line 346; git failure selects full mode before the pending write (§ Mode line 160) or the pass-2 pending stop (§ Two counters line 204, scenario 12); a review-green fingerprint mismatch still sets the candidate (§ Mode lines 130–132, scenario 2b). No `## Deferred — follow-up required` section is present. `## Deferred (P2+)` is not that section.

## Findings

### F-1: A suffixed `§` phrase suppresses the line and names no heading
**Severity:** P1
**Where:** spec § Changed regions, line 289; spec § Decision 15, line 100; spec § Scenarios, scenario 17
**Edge case:** An unresolved P0 or P1 uses the Where form this repo already writes: `spec § No-op step 4, line 173; spec § Mode lines 162–164` (round-3 edge-cases F-1) or `spec § Changed regions, line 288` (round-3 edge-cases F-2). The heading texts are `No-op`, `Mode`, and `Changed regions`. The cited exclusive bodies are unchanged, so the text diff does not name them. Delta pass 2, or a re-run after a red halt.
**What happens:** Line 289 has two arms. A title (`§ Mode`, `### Mode`, or the heading line's text) wins and does not use the line. A line is used only when Where names only a line. `§ No-op step 4` is not the heading `### No-op`, and `§ Mode lines 162–164` is not `### Mode`. The phrase-before-comma form that does match `Changed regions` does not match `No-op step 4`. Neither arm fires, and the spec never says to split on `;`. No heading is emitted for that finding. The delta contract then limits new critique to headings that were named. The pass can go green, and the next `spec.copy.md` and `baseline.commit` record the unreviewed section as reviewed. Decision 15 says an open finding's heading stays in scope when its text did not change.
**Why the spec misses it:** Scenario 17 only shows a bare `§ Mode` and a pure line-only Where. The rule that a title does not use the line was added so a moved line cannot override a real title. It also drops the locator on a title that matches no heading. `spec.md:173`, the other form in the reviewer output contract, is unspecified: the full path is the spec, but the token `spec.md` is not defined, so a path-is-not-the-spec reading explodes to every heading and a neither-arm reading emits nothing.
**Suggested fix:** Split Where on `;` and resolve each clause. Treat `spec.md`, the ticket's `*.spec.md` filename, and the full repo-relative spec path as the spec. After `§` or a heading marker, select every current heading whose text equals the phrase or is the longest heading-text prefix of it (`No-op` matches `No-op step 4`; `Changed regions` matches `Changed regions, line 288`). If more than one heading matches, emit all of them. If none match, use the line against the predecessor copy as line 289 already specifies. If a clause has neither a matching heading nor a placeable line, emit every current heading. Do not let a non-matching `§` phrase discard the line. Add those three Wheres to scenario 17.

### F-2: An untracked brief is code drift, so the clean no-op never fires
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Changed regions, lines 269–284; spec § No-op steps 3 and 6
**Edge case:** Marker `green`, filtered spec equal to `spec.copy.md`, filtered brief equal to `brief.copy.md`, scan clean, no open P0 or P1, and no implementation file changed. The brief and the spec are still untracked, which is the normal tree: spec-cycle does not commit, and `git status` shows `docs/specs/TODO/VHS-27.brief.md` as `??`. The H1 exclusive body backticks that brief path, as this spec does at line 3 and `VHS-41.spec.md` does at line 4.
**What happens:** `git ls-files --others --exclude-standard` lists the brief on every run until it is committed. The listing does not consult `baseline.commit`, so a green pass that saves today's HEAD does not clear it. The H1 body matches the path, step 6 does not fire, and a delta pass is dispatched. The same filename rule hits `verdict.md`, `spec.copy.md`, and `ledger.md` once this skill has written them under `<TICKET-ID>.reviews/`, for any spec that backticks those names. Decision 7 already treats a byte-identical brief as unchanged. Decision 11's clean no-op does not run on that tree, and each green delta can edit the spec and restart the churn the no-op exists to stop.
**Why the spec misses it:** Code drift is the union of the four listings with no exclusion for the two files the text diff and the brief filter already compared, or for the reviews tree this skill writes. Scenario 2's "no cited file changed" is false for the ordinary uncommitted brief.
**Suggested fix:** Before the citation tests, drop the resolved brief path, the spec path, and any path under `docs/specs/TODO/<TICKET-ID>.reviews/` from the changed-path set. A filename-only match must not see a dropped path. Add a scenario: green marker, both copies byte-identical, brief and spec untracked, no other cited path changed, and the result is the no-op.

### F-3: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Edge case:** Ticket lookup was not available.
**What happens:** No Plane record was retrieved. Done when and Decisions 1–16 were taken from the brief. The spec already records that under `## Deferred (P2+)`.
**Why the spec misses it:** This run was instructed not to call shared memory or the tracker.
**Suggested fix:** None for the spec. Re-check the Plane ticket when the mirror is reachable if its wording differs from the brief.

## Summary
P0: 0 | P1: 1 | P2: 1 | P3: 1 | P4: 0

STATUS: RED P0=0 P1=1 P2=1 P3=1 P4=0
