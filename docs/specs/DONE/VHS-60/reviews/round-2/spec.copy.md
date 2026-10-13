# VHS-60 — tighten spec-cycle delta scope and full-pass recovery

## Goal

Make `/spec-cycle` delta re-runs select exactly the spec regions named by unresolved findings, ignore unrelated tickets' review/attempt archives during code-drift matching, and keep first/full reviews usable when `HEAD` cannot be snapshotted. The change also closes the adjacent mode-reporting, deleted-spec, reviewer-contract, raw-path wording, usage, and workflow-reference gaps carried by the brief, without changing delta pass 2 or the review gate.

## Scope

| Path | Region | Change |
|---|---|---|
| `skills/spec-cycle/SKILL.md` | Phase 0 step 10 mode table | Add the absent-spec full-mode row with the brief's precedence and token. |
| `skills/spec-cycle/SKILL.md` | `### Delta no-op` | Print the replacement mode token when step 4 overrides delta mode. |
| `skills/spec-cycle/SKILL.md` | `### Round artifacts` and Phase 2 dispatch precondition | Add the full-pass, snapshot-command-failure-only two-file exception; keep every delta pass and every other incomplete-set failure unchanged. |
| `skills/spec-cycle/SKILL.md` | `### Changed regions` | Restore the four-clause raw-path wording, widen the archive-path drop, and replace open-finding heading/line resolution with the ordered, boundary-aware union rule. |
| `agents/spec-reviewer-correctness.md` | `# Delta scope` | Remove the stale `<lens>/STATUS` paragraph. |
| `agents/spec-reviewer-edge-cases.md` | `# Delta scope` | Apply the same byte-identical replacement block. |
| `agents/spec-reviewer-conventions.md` | `# Delta scope` | Apply the same byte-identical replacement block. |
| `agents/spec-reviewer-scalability.md` | `# Delta scope` | Apply the same byte-identical replacement block. |
| `README.md` | `/spec-cycle` usage line | Add `--full` to the bracketed alternatives. |
| `docs/spec-workflow-reference.md` | Phase 2 delta/full-mode and per-round artifact description | Document the absent-spec fallback and full-pass two-file exception. |

No new files are created. Do not edit `docs/specs/DONE/VHS-27/`, `AGENTS.md`, `sync.py`, `lint.py`, tests, ship-spec, spec-tickets, spec-close, or the verdict-marker schema.

## Decisions

### Decision 1 — print a late mode override

When delta no-op step 4 replaces the held token, print exactly `mode: full (open findings unreadable)` before reserving and running the full span. The preflight summary remains an honest record of the earlier held token; the second line records the later classification. No other late override or summary format changes.

### Decision 2 — a failed full-pass snapshot has one two-file exception

A full pass whose single `timeout 30 git --no-pager rev-parse HEAD` call times out, exits non-zero, or returns anything other than exactly 40 lower-case hexadecimal digits prints `baseline.commit NOT written: full-pass snapshot unavailable (<reason>) — dispatching with spec.copy.md and brief.copy.md only`. `<reason>` is `timeout`, `git error`, or `invalid SHA`.

For that named failure only, write both copy temps and rename `spec.copy.md` then `brief.copy.md` using the existing same-directory temp protocol. Dispatch only after both renames succeed. Do not create a `baseline.commit` temp or destination. The round counts normally and may end green or red. Because its round directory lacks `baseline.commit`, a later reviewed-marker re-run takes `mode: full (no baseline)`.

If the snapshot was valid but creating, writing, or renaming `baseline.commit` fails, the exception does not apply: use the existing incomplete-set stop. Every delta pass still requires all three files and a held snapshot. Copy-temp and copy-rename failures also stop before dispatch.

### Decision 3 — a deleted spec forces full mode

Add `Spec file does not exist` immediately after the operator-attested row and before the changed-brief row, with token `mode: full (no spec)`. Rows above it keep precedence, so the ordinary first invocation still reports `mode: full (marker missing)`. A reviewed green/red marker cannot carry its old baseline or ledger into a freshly authored spec.

### Decision 4 — delta pass 2's unreadable-status stop is unchanged

Keep the current pending-marker stop before delta pass 2. Do not dispatch that pass as full and do not add a third control branch.

### Decision 5 — ignore every open ticket's review and attempt archives

Before citation matching, drop every changed path whose first directory below `docs/specs/TODO/` matches either `<ticket>.reviews/` or `<ticket>.attempt-<n>/`, where `<ticket>` is a non-empty directory-name prefix and `<n>` is one or more ASCII digits. Drop all descendants, including attempt-held `spec.md` and `brief.md`. Keep another ticket's canonical `docs/specs/TODO/<ID>.brief.md` and `<ID>.spec.md` visible. Do not widen the rule to `docs/specs/DONE/` or to similarly named directories outside `docs/specs/TODO/`.

### Decision 6 — remove the stale status paragraph from all four agents

Replace the complete `# Delta scope` block in each reviewer with the byte-identical block in § Exact prose replacements. Only the `<lens>/STATUS` paragraph disappears. The replacement text names no skill line, repo-local skill/agent path, or implementation source.

### Decision 7 — ordered boundary-aware heading matching always unions cited lines

For each heading phrase, compare current heading text case-sensitively after removing the Markdown hash marker and its following whitespace. Run these arms in order; the first non-empty arm wins and emits every tie:

1. exact heading-text equality;
2. headings whose text begins with the phrase and whose next character is absent or non-alphanumeric;
3. the longest heading text that prefixes the phrase and whose next phrase character is absent or non-alphanumeric.

“Alphanumeric” means an ASCII letter or digit (`[A-Za-z0-9]`). This makes `Decision 8` select `Decision 8 — Two counters` but not `Decision 80`, while retaining the current long-heading-prefix fallback for phrases such as `No-op step 4`.

The heading result never suppresses a cited line. Resolve every line locator independently in the predecessor `spec.copy.md`, map its innermost owning predecessor heading through the existing stack pairing, and union that current/deleted heading with all text-match results. Thus `§ Design, line 289` includes both the `Design` heading and the heading that owns line 289.

### Decision 8 — segment multiple references and expand line ranges

Within each semicolon-delimited `Where` clause, treat every literal `§` reference and every Markdown heading-marker reference (`#{1,6}` followed by whitespace) as a separate segment; the segment ends immediately before the next such marker or at the clause end. Before heading matching, trim surrounding whitespace, then remove one terminal standalone connector `and` or `or` (case-insensitive) and its surrounding whitespace, then trim one run of trailing comma, semicolon, or colon characters plus surrounding whitespace. These are the complete joining-word and punctuation lists.

Within a segment, first try the phrase cut at its first comma. If all three Decision 7 arms are empty, retry all three arms against the uncut segment. This retry never crosses the segment boundary.

Recognize every positive decimal `line <n>` and inclusive `lines <start>-<end>` or `lines <start>–<end>` locator in the clause, case-insensitively. A range with `start <= end` places every line in the predecessor copy and unions the innermost owning headings, so a range crossing a heading includes each crossed owner. An invalid, reversed, zero, or out-of-file locator is unplaceable. If neither any heading arm nor any locator can be placed for a spec clause, retain the conservative fallback that emits every current heading. Existing rules for non-spec paths, deleted pairs, and unchanged-heading hunks remain.

### Decision 9 — state raw-path constraints as four separate clauses

The raw-path rule says: after removing one trailing carriage return, the line is non-empty and project-relative with forward slashes; it has no leading double quote; it contains no `=>` anywhere; it contains no tab anywhere; and it contains no backslash anywhere. This restores the VHS-27 wording without changing behavior.

### Decision 10 — pre-merge evidence uses this spec's real re-run

After this first invocation reaches a review-produced green, run `/spec-cycle docs/specs/TODO/VHS-60.brief.md` once with no intentional spec edit and once after one small, reviewable spec edit. Record the printed mode line, emitted changed-region list, and outcome of both runs in the PR. This evidence uses the currently installed rules, so the unchanged re-run may dispatch because the existing VHS-41 review/attempt trees match a bare citation; that is accepted evidence. The fixed-rule no-op is verified by the scenario walk before merge. Do not attest this spec, because an operator-attested marker forces full mode and cannot supply the required delta evidence.

### Decision 11 — stakes tier

**Tier:** big

The review loop has four full-pass opportunities. Tier does not enable the scale lens, and this brief has no scale declaration.

## Design

### Mode-table and reporting edits

Keep first-match semantics. Renumber the later rows after inserting the absent-spec row; no consumer parses the display number. Phase 1 still authors a missing spec after mode resolution, but the held full token prevents delta classification and the delta no-op. Delta no-op step 4 prints its replacement token before full-span reservation; a span-reservation failure therefore still has a visible final mode.

### Round-artifact state machine

Treat snapshot acquisition separately from writing a known SHA:

1. A delta pass uses its already-held valid snapshot and follows the existing three-temp/three-rename path.
2. A full pass calls `rev-parse` once.
3. On a valid SHA, follow the existing three-temp/three-rename path. Any artifact failure stops dispatch.
4. On snapshot timeout, git error, or invalid SHA, print Decision 2's line, prepare the two copy temps, rename them in the existing order, and dispatch only when both destinations exist. Do not invent or leave an empty `baseline.commit`.

The exception changes only dispatch eligibility. It does not synthesize a code baseline, extend the round budget, alter the marker, or make the round eligible for a later delta. Phase 2's general “complete set” sentence explicitly names this exception so it does not contradict `### Round artifacts`.

### Changed-path filtering

Apply the new all-ticket archive drop after collecting and validating raw git-listing lines and before stripping citation locators or matching filenames. The current-ticket brief/spec/reviews exclusions remain. A direct child such as `docs/specs/TODO/VHS-41.reviews/round-1/correctness.md` or `docs/specs/TODO/VHS-41.attempt-1/spec.md` is dropped; `docs/specs/TODO/VHS-41.spec.md`, `docs/specs/TODO/VHS-41.brief.md`, and `docs/specs/DONE/VHS-41/reviews/correctness.md` are not.

### Open-finding resolver

Preserve the existing top-level split on semicolons and the rule that a non-spec path emits every current heading. For a clause about this spec:

1. Discover all `§` and Markdown heading-marker segments in source order.
2. Normalize only each segment's terminal connector/punctuation as Decision 8 defines.
3. Run Decision 7's three heading arms on the comma-cut phrase, retrying the uncut segment only when all arms are empty.
4. Independently extract every line/line-range locator from the whole clause, place it in the predecessor copy, and stack-pair each distinct owning heading into the current spec.
5. Union and de-duplicate heading results without changing source order. A deleted pair stays `deleted: true`; an unchanged current heading uses the existing open-finding hunk.
6. Emit every current heading only when the clause concerns this spec and neither heading matching nor line placement produced a result.

This makes widening the safe failure mode: ambiguous ties and cross-heading ranges include more regions, never fewer. It does not introduce fuzzy similarity or heading-rename detection.

### Reviewer contract synchronization

The four agent edits are mechanical replacements of the full `# Delta scope` block. After editing, compare the extracted bytes from `# Delta scope` through the line immediately before each lens's `# Critique lens` heading. All four must be identical. Do not copy any spec/skill file citations into those agent blocks.

### Documentation synchronization

Update README's invocation grammar. In the workflow reference, extend the delta/full-mode paragraph to name an absent spec as a full-mode reason, and extend the per-round dispatch description to say a full pass may dispatch with only the two copies when snapshot acquisition itself fails. The reference must also state that such a round is not a delta baseline and a later reviewed-marker run takes `mode: full (no baseline)`.

## Exact prose replacements

These are the implementation text, not paraphrases. Line anchors refer to commit `0158267f681386d7b51c3239ec2bc0b13c45ba25`; locate by the quoted current text if lines move.

### `skills/spec-cycle/SKILL.md:363-375` — mode table

Current:

```markdown
| # | Condition | Token |
|---|---|---|
| 1 | `--full` was given | `mode: full (--full)` |
| 2 | Marker missing | `mode: full (marker missing)` |
| 3 | Marker has no valid `verdict:` or has no matching `ticket:` | `mode: full (marker unreadable)` |
| 4 | `verdict:` is `pending` | `mode: full (pending)` |
| 5 | `source:` is `operator-attested` | `mode: full (attested)` |
| 6 | Candidate set, saved brief present, and filtered brief differs | `mode: full (brief changed)` |
| 7 | Candidate set, review green or red, and baseline does not match | `mode: full (no baseline)` |
| 8 | Candidate set, baseline matches, and ledger is missing or unreadable | `mode: full (ledger unreadable)` |
| 9 | Candidate set, and `round-<candidate+1>/` or `round-<candidate+2>/` exists | `mode: full (round span occupied)` |
| 10 | Candidate unset after rows 1–5 | `mode: full (round unreadable)` |
| 11 | Otherwise | `mode: delta (continuing round <candidate>)` |
```

Replacement:

```markdown
| # | Condition | Token |
|---|---|---|
| 1 | `--full` was given | `mode: full (--full)` |
| 2 | Marker missing | `mode: full (marker missing)` |
| 3 | Marker has no valid `verdict:` or has no matching `ticket:` | `mode: full (marker unreadable)` |
| 4 | `verdict:` is `pending` | `mode: full (pending)` |
| 5 | `source:` is `operator-attested` | `mode: full (attested)` |
| 6 | Spec file does not exist | `mode: full (no spec)` |
| 7 | Candidate set, saved brief present, and filtered brief differs | `mode: full (brief changed)` |
| 8 | Candidate set, review green or red, and baseline does not match | `mode: full (no baseline)` |
| 9 | Candidate set, baseline matches, and ledger is missing or unreadable | `mode: full (ledger unreadable)` |
| 10 | Candidate set, and `round-<candidate+1>/` or `round-<candidate+2>/` exists | `mode: full (round span occupied)` |
| 11 | Candidate unset after rows 1–5 | `mode: full (round unreadable)` |
| 12 | Otherwise | `mode: delta (continuing round <candidate>)` |
```

### `skills/spec-cycle/SKILL.md:417` — late override

Current:

```text
4. If any `<lens>/STATUS` line exists, or the marker is red and both sets are empty, replace the token with `mode: full (open findings unreadable)`. Discard the delta start, reserve the smallest free full span, and run full. If no full span exists, stop with the marker unchanged. Do not print the no-op block or dispatch delta.
```

Replacement:

```text
4. If any `<lens>/STATUS` line exists, or the marker is red and both sets are empty, replace the token with `mode: full (open findings unreadable)` and print that replacement token. Discard the delta start, reserve the smallest free full span, and run full. If no full span exists, stop with the marker unchanged. Do not print the no-op block or dispatch delta.
```

### `skills/spec-cycle/SKILL.md:453` and `:506` — artifact exception

Current artifact paragraph:

```text
Write every round file by a dot-prefixed same-directory temp named `.<filename>.<random>.tmp`, then rename over the destination. Write all three temps first, then rename spec, brief, commit in that order. If any rename fails, print `<filename> NOT written: <error>`, delete an unrenamed temp, do not dispatch, do not write a ledger, and do not start another pass. Already renamed files remain and pending remains pending. Do not take a second snapshot for a delta pass. If HEAD moves after the listing snapshot, save the held snapshot; the newer tree is not treated as reviewed. A full pass takes one `timeout 30 git --no-pager rev-parse HEAD` at the start of this set; invalid or timed-out output fails the commit write rather than inventing a SHA.
```

Replacement artifact paragraphs:

```text
Write every round file by a dot-prefixed same-directory temp named `.<filename>.<random>.tmp`, then rename over the destination. Except for the named full-pass snapshot failure below, write all three temps first, then rename spec, brief, commit in that order. If creating, writing, or renaming an artifact fails, print `<filename> NOT written: <error>`, delete every unrenamed temp created by this artifact-write attempt, do not dispatch, do not write a ledger, and do not start another pass. Already renamed files remain and pending remains pending. A valid snapshot followed by a `baseline.commit` write or rename failure is not the exception.

Do not take a second snapshot for a delta pass. If HEAD moves after the listing snapshot, save the held snapshot; the newer tree is not treated as reviewed. A full pass takes one `timeout 30 git --no-pager rev-parse HEAD` at the start of this set. When that command times out, exits non-zero, or does not return exactly 40 lower-case hexadecimal digits, print `baseline.commit NOT written: full-pass snapshot unavailable (<reason>) — dispatching with spec.copy.md and brief.copy.md only`, where `<reason>` is `timeout`, `git error`, or `invalid SHA`. For that failure only, create both copy temps, then rename `spec.copy.md` and `brief.copy.md` in that order. Dispatch only if both renames succeed; do not create `baseline.commit`. The round counts as reviewed but cannot be a delta baseline, so a later reviewed-marker run takes `mode: full (no baseline)`. Every delta pass and every other incomplete artifact set still does not dispatch.
```

Current Phase 2 precondition:

```text
Before dispatch, atomically save the three-file set in `### Round artifacts`. Do not dispatch if the set is incomplete.
```

Replacement Phase 2 precondition:

```text
Before dispatch, atomically save the artifact set in `### Round artifacts`. Do not dispatch if the set is incomplete, except for that section's named full-pass snapshot-command failure: after both copy renames succeed, that full pass dispatches without `baseline.commit`.
```

### `skills/spec-cycle/SKILL.md:488` — raw path

Current:

```text
A raw path is a non-empty project-relative forward-slash line after removing one trailing CR, with no leading `"`, `=>`, tab, or backslash. Do not repair or unquote output. A non-zero exit, timeout, unresolved SHA, or non-raw line is failure. `--no-renames` makes a rename list both old and new paths.
```

Replacement:

```text
A raw path is a non-empty project-relative forward-slash line after removing one trailing CR. It has no leading `"`; it contains no `=>` anywhere, no tab anywhere, and no backslash anywhere. Do not repair or unquote output. A non-zero exit, timeout, unresolved SHA, or non-raw line is failure. `--no-renames` makes a rename list both old and new paths.
```

### `skills/spec-cycle/SKILL.md:490` — changed-path drop

Current:

```text
Before matching citations, drop the resolved brief path, `docs/specs/TODO/<TICKET-ID>.spec.md`, and every path under `docs/specs/TODO/<TICKET-ID>.reviews/`. Strip one trailing locator (`:digits`, `:digits-digits`, `:digits–digits`, or `#Ldigits`) and one leading `./` from each backtick span. In a heading's exclusive body, a citation matches a changed path by exact value, slash-boundary suffix, or filename-only equality. Matching is case-sensitive. Also inspect `## Scope` rows/list items: a changed backtick path with `§` references adds every named section; with no section it adds only `## Scope`. A code-only hit's hunk is `(no text change — cited file <path> changed since <sha>)`.
```

Replacement:

```text
Before matching citations, drop the resolved brief path, `docs/specs/TODO/<TICKET-ID>.spec.md`, and every path under `docs/specs/TODO/<TICKET-ID>.reviews/`. Also drop every path whose first directory below `docs/specs/TODO/` is `<ticket>.reviews/` or `<ticket>.attempt-<n>/`, where `<ticket>` is non-empty and `<n>` is one or more ASCII digits; this drops every descendant, including an attempt's `spec.md` and `brief.md`, but does not drop another ticket's canonical brief or spec. Strip one trailing locator (`:digits`, `:digits-digits`, `:digits–digits`, or `#Ldigits`) and one leading `./` from each backtick span. In a heading's exclusive body, a citation matches a changed path by exact value, slash-boundary suffix, or filename-only equality. Matching is case-sensitive. Also inspect `## Scope` rows/list items: a changed backtick path with `§` references adds every named section; with no section it adds only `## Scope`. A code-only hit's hunk is `(no text change — cited file <path> changed since <sha>)`.
```

### `skills/spec-cycle/SKILL.md:492` — open-finding resolver

Current:

```text
For each open finding, split `Where` on `;`. `spec.md`, the ticket spec filename, and its repo-relative path mean this spec; another path emits every current heading. After `§` or a heading marker, take text through the next comma and match heading text by equality or the longest heading-text prefix; emit every tie and do not then use the line. Otherwise place its line in the predecessor `spec.copy.md`, take the innermost owning heading there, and stack-pair it into the current spec. A deleted pair is emitted as deleted. A non-matching `§` phrase does not discard a line. With no heading match or placeable line, emit every current heading. An unchanged heading selected by an open finding gets `(open finding <lens>/<id> — no text hunk)`.
```

Replacement:

```text
For each open finding, split `Where` on `;`. `spec.md`, the ticket spec filename, and its repo-relative path mean this spec; another path emits every current heading. Within a clause about this spec, every literal `§` and every Markdown heading marker of one to six `#` followed by whitespace opens a separate segment ending before the next such marker or at the clause end. For each segment, trim surrounding whitespace; remove one terminal standalone `and` or `or`, case-insensitively, and its surrounding whitespace; then trim one run of trailing comma, semicolon, or colon characters and surrounding whitespace. First take the phrase through the first comma and run these case-sensitive heading-text arms in order, stopping at the first non-empty arm and emitting every tie: exact equality; every heading whose text begins with the phrase and is followed by a non-ASCII-alphanumeric character or end of text; otherwise the longest heading text that prefixes the phrase and ends before a non-ASCII-alphanumeric character or end of phrase. If all arms are empty, retry all three against the uncut segment. Heading text excludes the Markdown marker and following whitespace. ASCII alphanumeric means `[A-Za-z0-9]`.

Independently of every heading match, resolve every positive decimal `line <n>` and inclusive `lines <start>-<end>` or `lines <start>–<end>` locator in the clause, case-insensitively, against the predecessor `spec.copy.md`. A valid range has `start <= end`; place every line in it. For each placeable line, take the innermost owning predecessor heading and stack-pair it into the current spec. Union and de-duplicate those results with all segment heading matches in source order. A deleted pair is emitted as deleted. A non-matching heading phrase does not discard a line. An invalid, reversed, zero, or out-of-file locator is unplaceable. With no heading match and no placeable line in a clause about this spec, emit every current heading. An unchanged heading selected by an open finding gets `(open finding <lens>/<id> — no text hunk)`.
```

### Four reviewer agents — complete `# Delta scope` block

Current in `agents/spec-reviewer-correctness.md:90-100`, `agents/spec-reviewer-edge-cases.md:88-98`, `agents/spec-reviewer-conventions.md:93-103`, and `agents/spec-reviewer-scalability.md:77-87`:

```markdown
# Delta scope

Apply this only when `review_mode` is `delta`. When it is `full` or absent, skip this section.

Read the spec (grounding step 1), run the Deferred-findings block, verify closures, check vanished references, and record process failures exactly as you do on a full pass. Those checks are not limited to `changed_regions`.

Apply your critique-lens questions only to headings named in `changed_regions` or in `open_findings`. A named heading covers its exclusive body only: the lines after that heading and before the next heading of any depth. A descendant heading is in scope only when it is itself named. A `deleted: true` entry has no body in the current spec: read that heading's body in `spec.copy.md` in the prior round's reviews directory, and assess what the removal drops. Do not explore any other region. Do not file a finding whose claim is that a Decision outside that scope should be a different decision. A changed section that contradicts a Decision outside the scope is in scope: file it against the changed section.

A line whose id is `<lens>/STATUS` names no heading. It is not a changed region and not an open-finding heading. Ignore it as scope.

A P0 you meet while doing a check this section still requires (you were not hunting an unchanged region for it) may be filed. Cite the evidence. It counts in the gate. Do not open an unchanged section to look for one.
```

Replacement in all four files, byte-for-byte:

```markdown
# Delta scope

Apply this only when `review_mode` is `delta`. When it is `full` or absent, skip this section.

Read the spec (grounding step 1), run the Deferred-findings block, verify closures, check vanished references, and record process failures exactly as you do on a full pass. Those checks are not limited to `changed_regions`.

Apply your critique-lens questions only to headings named in `changed_regions` or in `open_findings`. A named heading covers its exclusive body only: the lines after that heading and before the next heading of any depth. A descendant heading is in scope only when it is itself named. A `deleted: true` entry has no body in the current spec: read that heading's body in `spec.copy.md` in the prior round's reviews directory, and assess what the removal drops. Do not explore any other region. Do not file a finding whose claim is that a Decision outside that scope should be a different decision. A changed section that contradicts a Decision outside the scope is in scope: file it against the changed section.

A P0 you meet while doing a check this section still requires (you were not hunting an unchanged region for it) may be filed. Cite the evidence. It counts in the gate. Do not open an unchanged section to look for one.
```

### `README.md:10` — usage

Current:

```markdown
- **`/spec-cycle <brief-path> [--attest "<reason>"]`** — Author a spec from a brief, then run a parallel review loop (correctness / edge-cases / repo-conventions, plus an optional scalability lens) until findings clean or 4 passes complete. Halts at a session boundary with a structural drift-check checklist before any implementation. Records its verdict at `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`; `--attest` records a green verdict reached by hand. Pair with `/ship-spec`.
```

Replacement:

```markdown
- **`/spec-cycle <brief-path> [--attest "<reason>" | --full]`** — Author a spec from a brief, then run a parallel review loop (correctness / edge-cases / repo-conventions, plus an optional scalability lens) until findings clean or 4 passes complete. Halts at a session boundary with a structural drift-check checklist before any implementation. Records its verdict at `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`; `--attest` records a green verdict reached by hand. Pair with `/ship-spec`.
```

### `docs/spec-workflow-reference.md:74` and `:81` — workflow summary

Current delta/full paragraph:

```text
On a re-run after a reviewed green or red halt, spec-cycle uses at most two delta passes when the saved baseline is readable: each lens newly explores only changed heading bodies and prior-round open P0/P1 findings, while closure, grounding, process, vanished-reference, and Deferred-row checks remain active. Delta pass 1 revises normally. Delta pass 2 folds without FROZEN/REWRITE, then halts if still red. A clean green re-run with nothing changed and nothing open is a no-op that leaves the marker as written. `--full`, or any full-mode row such as a missing marker/baseline, changed brief, pending marker, occupied round span, unreadable ledger, or unavailable code drift, forces a full invocation. The first invocation remains a full review.
```

Replacement delta/full paragraph:

```text
On a re-run after a reviewed green or red halt, spec-cycle uses at most two delta passes when the saved baseline is readable: each lens newly explores only changed heading bodies and prior-round open P0/P1 findings, while closure, grounding, process, vanished-reference, and Deferred-row checks remain active. Delta pass 1 revises normally. Delta pass 2 folds without FROZEN/REWRITE, then halts if still red. A clean green re-run with nothing changed and nothing open is a no-op that leaves the marker as written. `--full`, or any full-mode row such as a missing marker/baseline/spec, changed brief, pending marker, occupied round span, unreadable ledger, or unavailable code drift, forces a full invocation. The missing-spec row follows the attested row, so a first invocation with no marker still reports `mode: full (marker missing)`; a reviewed marker whose spec was deleted reports `mode: full (no spec)`. The first invocation remains a full review.
```

Current dispatch item:

```text
2. **Dispatch the reviewer agents in parallel** (one message, multiple agent calls — three by default; a fourth, scalability, when the brief declares scale). Each reviews through a different lens:
```

Replacement dispatch item:

```text
2. **Save the round artifacts, then dispatch the reviewer agents in parallel** (one message, multiple agent calls — three by default; a fourth, scalability, when the brief declares scale). Normally the saved set is `spec.copy.md`, `brief.copy.md`, and a valid `baseline.commit`. If and only if a full pass cannot acquire its commit snapshot, it prints the named failure, saves both copies atomically, and dispatches without `baseline.commit`; that reviewed round cannot become a delta baseline, so a later reviewed-marker run selects `mode: full (no baseline)`. Every delta pass and every other incomplete set stops before dispatch. Each reviewer uses a different lens:
```

## Scenarios

1. **First invocation precedence.** No marker and no spec: row 2 wins, prints `mode: full (marker missing)`, Phase 1 authors the spec, and the first full pass runs.
2. **Reviewed marker, deleted spec.** Review-produced green/red marker with a valid candidate baseline and unchanged brief, but no spec: the new row prints `mode: full (no spec)`; Phase 1 authors a fresh spec and no old ledger enters its first full dispatch.
3. **Late unreadable-open override.** Preflight prints delta; no-op step 4 finds `<lens>/STATUS` or a red marker with both sets empty: it then prints `mode: full (open findings unreadable)`, recomputes the full span, and never dispatches delta.
4. **Full snapshot command fails.** `rev-parse HEAD` times out, errors, or emits an invalid SHA: the named line prints, both copies rename successfully, no `baseline.commit` exists, and the full reviewers dispatch. If the round completes, the next reviewed-marker invocation selects `mode: full (no baseline)`.
5. **Artifact failure after a valid snapshot.** `rev-parse` yields a valid SHA but a temp create/write or any rename fails: print the ordinary failure, delete every unrenamed temp created by that attempt, and do not dispatch. Exercise failures before the first rename and at each rename position. The two-file exception does not apply.
6. **Delta snapshot requirement.** A delta pass lacks or cannot validate its held snapshot: retain the current full override/pass-2 stop. It never takes the two-file exception.
7. **All-ticket archive noise.** The only changed paths are `docs/specs/TODO/VHS-41.reviews/round-1/correctness.md` and `docs/specs/TODO/VHS-41.attempt-1/spec.md`; both are dropped, so a bare `correctness.md` or `spec.md` citation cannot make a changed region and an otherwise clean green re-run reaches the no-op.
8. **Canonical cross-ticket dependency.** `docs/specs/TODO/VHS-41.spec.md` or `VHS-41.brief.md` changes and a heading cites its bare filename: it remains in the set and selects that heading.
9. **Raw-path tripwires.** A line with a leading quote, or with `=>`, a tab, or a backslash at any later position, is non-raw and triggers the existing failure path. A normal forward-slash project path remains valid.
10. **Equality plus cited line.** `spec § Design, line 289` matches `Design` exactly and independently places line 289 in a child heading; both headings are unioned, so the child remains explorable.
11. **Abbreviated numbered decision.** `spec § Decision 8` selects `Decision 8 — Two counters, at most two delta passes on every tier`; it does not select `Decision 80` and does not emit every heading.
12. **Wrong shorter prefix loses to starts-with.** With headings `Decision` and `Decision 8 — Two counters`, phrase `Decision 8` uses arm 2 and selects the latter; arm 3 never runs.
13. **Two section references.** `spec § Decision 8 and § Decision 14` becomes two segments, strips the terminal `and` from the first, and unions both selected headings.
14. **Comma-cut retry.** If the comma-cut phrase yields no heading but the uncut segment does, the resolver retries all arms against the uncut segment without crossing into another `§` reference.
15. **Cross-heading range.** A `lines 120-135` locator whose predecessor lines occupy two exclusive bodies selects both innermost owning headings, mapped through stack pairing.
16. **Conservative fallback.** A spec clause with no match and no placeable valid line still emits every current heading; an invalid/reversed range alone cannot narrow the pass.
17. **Agent synchronization.** Extracting the four replacement Delta scope blocks yields byte-identical bytes, and none contains `<lens>/STATUS`, a skill line number, or a repo-local skill/agent path.
18. **Real pre-merge delta evidence.** The review-produced green from this run is re-run unchanged and after a small spec edit; both mode/scope/outcome records go into the PR even if the unchanged current-rule run dispatches because of VHS-41 archive noise.

## Test plan

No new automated test module is added because this repository's suite does not execute prose skills. Review the implementation diff against every exact replacement and walk all 18 scenarios against the edited prose.

The implementation review must additionally verify:

- the four `# Delta scope` blocks are byte-identical after the deletion;
- no dot-prefixed temp remains after any exercised artifact write;
- current-ticket copy exclusions and other-ticket canonical spec/brief visibility remain intact;
- mode-table precedence is first-match and the candidate/unset row still refers to rows 1–5;
- the full-pass two-file exception cannot be reached after a valid snapshot or on a delta pass;
- the README and workflow reference match the skill's final tokens and exception;
- no file under `docs/specs/DONE/VHS-27/` changes;
- the real pre-merge reruns from Decision 10 are recorded in the PR.

## Test command

Run from the repository root:

```text
python lint.py --strict
python -m unittest discover -s tests -p "test_*.py"
```

Both commands must pass. They guard repository portability and regression behavior; the scenario walk is the behavioral oracle for these prose-only control-flow changes.

## Done when

- The three briefed `Where` forms resolve without an every-heading fallback: abbreviated `Decision 8`, equality-plus-line `Design, line 289`, and the wrong-parent/prefix case all select the finding's owning heading. — Decisions 7–8; scenarios 10–12.
- A bare review-artifact filename does not block the no-op when only another ticket's untracked review/attempt archives changed. — Decision 5; scenario 7.
- This spec contains one scenario per changed behavior, and `docs/specs/DONE/VHS-27/spec.md` is unchanged. — § Scenarios; Test plan.
- Delta no-op step 4 prints `mode: full (open findings unreadable)` when it replaces the held token. — Decision 1; scenario 3.
- README's `/spec-cycle` usage line contains `[--attest "<reason>" | --full]`. — Exact README replacement.
- A full pass whose commit snapshot cannot be acquired prints the named line, saves the two copies, and dispatches; its next reviewed-marker run selects `mode: full (no baseline)`. — Decision 2; scenario 4.
- A reviewed marker with the spec deleted prints `mode: full (no spec)`, while a first invocation still prints `mode: full (marker missing)`. — Decision 3; scenarios 1–2.
- All four reviewer agents omit the `<lens>/STATUS` scope paragraph and retain byte-identical Delta scope blocks. — Decision 6; scenario 17.
- The raw-path sentence separately bans a leading quote and any `=>`, tab, or backslash anywhere. — Decision 9; scenario 9.
- One real unchanged and one small-edit delta re-run on this review-produced-green VHS-60 spec are recorded in the PR as Decision 10 requires. — Decision 10; scenario 18.

## Out of scope

- Dispatching delta pass 2 as a full review when a status line is unreadable; keep the current pending-marker stop.
- Dropping other tickets' canonical briefs or specs from code drift.
- A post-merge/install real delta run under the fixed rules.
- Detecting deliberate citations into another ticket's `.reviews/` or `.attempt-<n>/` directory, or suppressing changed tracked files under `docs/specs/DONE/<ID>/reviews/`.
- Editing the archived VHS-27 spec or its review evidence.
- Adding an author-side executable checker; VHS-26 owns that work.
- Fuzzy heading similarity, heading-rename detection, gate arithmetic, reviewer severity rules, round budgets, verdict-marker fields, tier/scale pins, or any ship-spec/spec-tickets/spec-close behavior.
- Concurrent `/spec-cycle` invocations over one spec. The installed skill already declares them outside the supported flow; VHS-60 adds no lock, ownership claim, or stale-owner recovery.

## Deferred (P2+)

- correctness/F-1 and edge-cases/F-3 (P3) ticket grounding was unavailable — no spec change; the run took the documented brief-only degrade path.
- correctness/F-2 (P3) touched workflow files changed recently — no spec change; all quoted current blocks were verified at `0158267f681386d7b51c3239ec2bc0b13c45ba25` and must be rechecked immediately before implementation.
