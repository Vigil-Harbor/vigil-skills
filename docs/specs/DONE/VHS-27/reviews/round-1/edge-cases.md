The ledger match, the citation rule, and the no-op path each fail open on inputs this repo already produces. The report follows.

# Edge-Cases Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: Ledger coverage is a substring test, so a dropped shorter id is invisible
**Severity:** P0
**Where:** VHS-27.spec.md:332 (§ Delta contract, ledger check)
**Edge case:** A predecessor report has both `correctness/F-1` (P1) and `correctness/F-10` (P1). The saved ledger omits the F-1 line and keeps the F-10 line. Same failure when any id is a digit-prefix of another id at the same severity (`F-2` vs `F-20`), or when the omitted id string appears inside another line's title.
**What happens:** The check marks the omitted finding covered and does not file `ledger omits a P0/P1 line`. The gate can go green. This is the dropped-P1 case Decision 3 and the third Done-when bullet exist to catch. PET-166-sized rounds (tens of P0/P1 lines) always have prefix ids.
**Why the spec misses it:** The prescribed test is "some line contains `<lens>/F-<k>` and the same severity." `correctness/F-10 (P1)` contains the character sequence `correctness/F-1` and the severity `P1`. There is no token boundary and the severity is not required to sit on that id. The same rule covers `<lens>/STATUS` by containment rather than by its own line.
**Suggested fix:** Cover a finding only when a line matches the id as a token: `(^|[^A-Za-z0-9])<lens>/F-<k>([^0-9]|$)`, with `(P0)` or `(P1)` as the severity on that same line immediately after the id, before the title. Do not treat a match inside the quoted title or inside a longer id as coverage. Add a scenario: ledger has `correctness/F-10 (P1)` and omits `correctness/F-1 (P1)`; the correctness lens files one P0 naming F-1.

### F-2: House-style `path:line` citations never count as code drift, so scenario 10 no-ops
**Severity:** P1
**Where:** VHS-27.spec.md:256-257 (§ Changed regions, path citation and Scope row); scenario 10 at VHS-27.spec.md:384
**Edge case:** The spec text and brief are unchanged, the guarantee scan is clean, open findings are empty, and a cited file differs from `baseline.commit`. The only citations are backtick spans in the form this repo already uses: `` `SKILL.md:386` ``, `` `AGENTS.md:46-48` ``, `` `SCHEMA.md:280–283` `` (en dash), or `` `skills/spec-cycle/SKILL.md:388` ``. Confirmed in `docs/specs/TODO/VHS-41.spec.md` and `VHS-13.spec.md`.
**What happens:** The span is not equal to the git path, is not a `/`-boundary suffix of it, and is not "only a filename," so neither the path test nor the Scope-row test fires. The changed-region set stays empty. § No-op step 4 prints the NO-OP block and leaves the green marker in place. Reviewers are not dispatched, so the delta contract's whole-spec vanished-reference check never runs. The merge Decision 5 exists to catch is recorded as "nothing changed."
**Why the spec misses it:** The matcher requires the backtick span to be exactly the path or exactly the filename. It never strips a `:line`, `:start-end`, en-dash range, or `#Lnn` suffix before comparing. Scenario 10 assumes "cited" means those tests succeed.
**Suggested fix:** Before comparing, strip one trailing locator from the span: `:digits`, `:digits-digits`, `:digits–digits` (en dash), or `#Ldigits`, including a leading `./`. Apply that normalized span to both the path test and the Scope-row path test. A span that still does not match stays a non-citation. Add a scenario-10 variant whose only citation is `` `skills/spec-cycle/SKILL.md:388` `` and whose outcome is still not a no-op.

### F-3: Any edit marks every ancestor section changed, so a delta pass may explore the whole spec
**Severity:** P1
**Where:** VHS-27.spec.md:241-243 (§ Changed regions); VHS-27.spec.md:318 (§ Delta contract)
**Edge case:** A one-line edit inside one leaf section, or a code-drift citation that sits in that leaf. The document's `# Title` heading has no later heading of equal or lesser depth.
**What happens:** A section body runs through the next heading of equal or lesser depth, so it includes every descendant. The leaf change makes the leaf, its parent, and the H1 all differ. All three are emitted as changed regions. The delta contract then allows new critique of every named section and forbids "any other region." The H1 region is the whole spec, so unchanged sibling subtrees are in scope. Every non-empty text delta is a full-spec exploration, which is the churn Decision 10 forbids. The same inclusion pulls a single code-drift citation up into every ancestor.
**Why the spec misses it:** Extent is defined once, inclusively, and "changed" is defined on that text. The contract limits exploration by section name, not by the diff hunk and not by the heading's exclusive intro.
**Suggested fix:** Give each heading an exclusive body: the lines after the heading and before the next heading of any depth. A section is text-changed only when that exclusive body differs. Code-drift and path citation run on that same exclusive body. Do not emit an ancestor solely because a descendant changed. The explorable region is the named heading's exclusive body plus that heading's own descendants only when those descendants are themselves listed.

### F-4: A git error suppresses the no-op, then an empty delta may go green and replace the baseline
**Severity:** P1
**Where:** VHS-27.spec.md:159 (§ No-op step 3); VHS-27.spec.md:251-252 (§ Changed regions); VHS-27.spec.md:202 and VHS-27.spec.md:267 (§ Artifacts, § Dispatch)
**Edge case:** Mode is already delta, spec and brief match the saved copies, open findings are empty, and the scan is clean, but `git diff` or `git ls-files` fails or the saved SHA does not resolve. Realistic triggers: `index.lock` held by another git process, a shallow clone or rebase that dropped the saved object, or a missing git directory.
**What happens:** Step 3 skips the no-op and dispatches delta with text-diff regions only. Those regions are empty, so the prompt carries an empty `changed_regions`. Critique is forbidden outside that list. Closure and vanished-reference checks still run, but they do not see a behavior change whose cited symbols still resolve — the PET-166 merge. A clean STATUS goes green. Dispatch already wrote a new `baseline.commit` of current `HEAD` before the reviewers ran. The next re-run diffs against that new SHA, so the unreviewed drift is gone and the no-op succeeds. Persisted baseline state now says the new tree was reviewed.
**Why the spec misses it:** It says not to flip the mode to full, and it allows a green pass whenever the gate is clean. It never says an empty region set produced by a skipped code-drift pass is forbidden from going green, and it never keeps the previous `baseline.commit` when the diff could not be computed. "Do not write `NONE`" covers only a bad `git rev-parse` at save time, which refuses dispatch; a later diff failure does not.
**Suggested fix:** If any code-drift command fails or the saved SHA does not resolve, do not dispatch a text-only delta. Select `mode: full (code-drift unavailable)` when still classifying. During a pass already dispatched, do not write a green marker and do not leave the new `baseline.commit` as the next baseline: print `code-drift: skipped (git error)`, leave the marker pending, and stop without Phase 3. A later run then takes the pending row and reviews the whole spec. Add that scenario next to scenario 10.

### F-5: A review marker whose round is not a positive integer falls through to delta
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** VHS-27.spec.md:126-145 (§ Mode, rows 3 and 10)
**Edge case:** `verdict:` is `green` or `red`, `ticket:` matches, `source:` is not `operator-attested`, and `round` is missing, `not reviewed`, `in progress`, or not a positive integer. The six-state reader still calls this `green`, `changed`, or `red`, not `unreadable` (that state is only "no verdict line" or a bad ticket). A crash mid-overwrite of `verdict.md` can leave this shape; the current skill replaces the marker in place and does not require temp-then-rename.
**What happens:** Rows 1–9 do not match. Row 7 requires a positive round. Row 10 selects `mode: delta (continuing round <candidate>)` even though § Mode never set `candidate`. `candidate + 1` is not executable. An implementer who substitutes 0 or 1 starts at `round-1/` and can overwrite an existing reviews tree.
**Why the spec misses it:** "Unreadable" is delegated to the six-state reader, which does not look at `round`. The catch-all row assumes a candidate exists.
**Suggested fix:** Add a row before row 10: review-green or review-red whose `round` is not a positive integer → `mode: full (round unreadable)`. Do not start a delta. Require the marker write itself to use the same temp-then-rename rule as the four round artifacts, so a crash cannot truncate `verdict.md`.

### F-6: `baseline.commit` and `ledger.md` treat a Windows newline as a corrupt artifact
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** VHS-27.spec.md:128 (§ Mode, baseline and ledger readable); VHS-27.spec.md:202 (§ Artifacts)
**Edge case:** The file is 40 lowercase hex digits plus CRLF, or the ledger header is the required sentence with a trailing `\r`. `git rev-parse HEAD` emits LF, but a text-mode write on Windows stores CRLF. The fingerprint path already strips carriage returns; these two new files do not.
**What happens:** `baseline.commit` fails the "single trailing newline" byte check, so every later re-run takes row 7 `mode: full (no baseline)` and delta never engages. A CRLF ledger fails the first-line equality check and takes row 8 forever. Both degrade to a full pass rather than corrupting the spec, but the feature this ticket adds does not run on the platform the skill already special-cases for CR.
**Why the spec misses it:** It pins "a single trailing newline" and an exact header line, and it never says to strip `\r` or to write those two files as raw LF bytes.
**Suggested fix:** Define `baseline.commit` as 40 lowercase hex bytes plus one `\n`, with no `\r` anywhere, written as raw bytes. When reading, accept either `\n` or `\r\n` and reject anything else. For `ledger.md`, strip `\r` before the header test, the same way § Mode strips carriage returns from briefs. A zero-byte ledger stays unreadable.

### F-7: The no-op can report green for a red marker when reports are missing or headings do not parse
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** VHS-27.spec.md:165-169 (§ No-op); VHS-27.spec.md:289 (§ Dispatch, open findings)
**Edge case:** Marker is `red`, baseline and ledger match, spec text is unchanged, the scan is clean, and either a standing-lens report is absent from `round-<candidate>/`, or the report's STATUS line parses as `RED` but no `### F-<k>:` heading carries severity P0 or P1 (truncated save after 2c). `**Where:** spec.md:410` with no section name is a related gap: the finding is open only if a heading parsed, and § Changed regions never maps a line-only `Where` onto a heading.
**What happens:** A missing file is not "a report with no parseable STATUS line," so no `<lens>/STATUS` open finding is added. The open set stays empty. Step 4 prints `Marker: left as written (green, round <candidate>)` and stops. The marker on disk stays red, so `/ship-spec` still halts, but the operator is told the run is green. The sentence "A red marker cannot reach this block" is not checked against `verdict:`.
**Why the spec misses it:** Open findings are defined only for a report that was read. Red is inferred from those findings plus the scan, never from the marker. The printed block hardcodes `green`.
**Suggested fix:** If the marker is `red`, do not take the no-op. If `correctness.md`, `edge-cases.md`, or `conventions.md` is missing or unreadable, add `<lens>/STATUS (P0)` the same way an unparseable STATUS does, and do not no-op. When an open finding's `Where` names a heading, emit that section; when it names only a line, emit the heading that contains that line, or the whole spec if the line cannot be placed. Keep the printed marker line equal to the verdict actually left on disk.

### F-8: Only the immediate next round directory is reserved, so a later pass can overwrite an existing round
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** VHS-27.spec.md:144-151 (§ Mode, row 9 and full start); VHS-27.spec.md:209 (§ Artifacts)
**Edge case:** A hole in the round directories. Delta: marker at round 4, `round-5/` absent, `round-6/` present (round-5 removed, or pass 2 of an earlier run created it and the marker never moved). Full: smallest missing directory is 3 while `round-4/` still holds reports. Also a partial artifact set written after the pending marker: § Artifacts says the later run "takes row 7 or row 8," but row 4 matches first whenever the pending write succeeded, and row 9 matches when the new directory exists and the marker is still the old green or red.
**What happens:** Row 9 only looks at `round-<candidate+1>/`. Delta pass 2 writes `round-<candidate+2>/` with no second check and replaces that round's reports, `spec.copy.md`, and `ledger.md`. A full invocation sets `C = start + P - 1` and likewise overwrites any later directory in the span. Decision 13's "interrupted reports are not overwritten" does not hold across a hole. The row 7/8 sentence is false for the pending and next-directory cases; following it instead of first-match would mis-route the recovery. The safe outcomes (row 4 full, or row 9 full) only happen when the implementer follows the table and ignores that sentence.
**Why the spec misses it:** The storage rule is stated as one directory check. "Smallest positive integer N such that `round-<N>/` does not exist" does not require `round-<N>` through `round-<N+round_cap-1>` to be free. Delta pass 2 never repeats the check.
**Suggested fix:** Before creating any round directory, require the whole span to be absent: for delta, both `candidate+1` and `candidate+2`; for full, `start` through `start+round_cap-1`. If any one exists, take full mode and choose the smallest `start` whose entire span is free. Replace the § Artifacts sentence with: a partial set under a pending marker takes row 4; a partial set whose directory is `round-<candidate+1>/` while the marker is still the previous green or red takes row 9; row 7 or 8 applies only when the candidate directory itself is missing a member.

## Summary
P0: 1 | P1: 3 | P2: 4 | P3: 0 | P4: 0

Persistence walk for `spec.copy.md`, `brief.copy.md`, `baseline.commit`, and `ledger.md`: per-file temp-then-rename is defined and a zero-byte ledger correctly forces a later full pass. The group of three dispatch files is not one atomic commit, but a partial set is recoverable. Those records are bounded by the spec, the brief, one SHA, and one line per P0/P1. The DONE archive is refused as a baseline. There is no schema version; a round without the three files takes full mode. The unchecked case is F-4: a green pass after a skipped code-drift computation persists a new SHA that hides the unreviewed tree. Concurrent invocations stay outside the flow the skill already documents.

STATUS: RED P0=1 P1=3 P2=4 P3=0 P4=0
