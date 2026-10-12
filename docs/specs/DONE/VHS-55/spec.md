# VHS-55 — Stakes tier at preflight

**Brief:** `docs/specs/TODO/VHS-55.brief.md` · **Plane:** VHS-55 (Todo) · **Date:** 2026-10-11

## Goal

Ceremony follows a tier the operator sets in `/spec-brief`. `tweak` writes no brief. `small` keeps the three standing lenses, caps the review loop at 2 rounds, and skips `/ship-spec`'s review gate while keeping the test gate. `big` is today's loop. `irreversible` is `big` plus the tier on every reviewer prompt plus a review gate that halts instead of skipping. A brief with no `## Tier` section, and a spec with no recorded tier line, stay on today's path. Scale stays its own declaration and never follows from the tier.

## Scope

| Path | Change |
|---|---|
| `skills/spec-brief/SKILL.md` | Hoist the seed gate so it runs in every mode, including `--no-grill`. Add the tier gate after it and before the interview. Confirm can change the tier. A `tweak` choice writes nothing. Phase 4 emits `## Tier` on every brief it writes. |
| `skills/spec-cycle/SKILL.md` | Parse `## Tier` once per invocation beside the Scale parse. Record a `**Tier:**` line in Phase 1. Write `tier:` on every verdict marker, including attest mode. Replace the hard-coded review-loop cap of 4 with `round_cap` (2 for `small`, 4 otherwise). Pass `tier` on every reviewer prompt. |
| `skills/ship-spec/SKILL.md` | Read the spec's recorded tier. Treat a malformed or disagreeing marker `tier:` as the `changed` state. `small` skips the review gate. `irreversible` turns the three Phase 3b skip cases into a halt before the commit. |
| `agents/spec-reviewer-correctness.md`, `agents/spec-reviewer-edge-cases.md`, `agents/spec-reviewer-conventions.md`, `agents/spec-reviewer-scalability.md` | Add `tier` to each enumerated input list, with one sentence on how that lens consumes it. |
| `docs/spec-workflow-reference.md` | Document the ladder, the `## Tier` grammar, the tweak-floor heuristic, the headless stop, and the `round_cap` substitution. Rewrite the four loop-cap sentences so they follow `round_cap`. |
| `AGENTS.md` | Describe which tier changes which skill, that an absent tier is `big`, and that the severity scale does not change with tier. Name the optional `## Tweak surfaces` extension. |

Leave alone:

- `skills/spec-tickets/SKILL.md` — verified inert to a `tier:` line (Decision 13). No edit.
- `skills/spec-close/SKILL.md`, `skills/grilling/SKILL.md`, `skills/ship-spec/states.json`, `sync.py`
- `README.md`. `README.md:10` stays the big-tier maximum ("4 passes complete") and is not updated. Historical notes under `docs/` other than `docs/spec-workflow-reference.md`
- `docs/portability-contract.md`, `docs/customizing.md` (`docs/customizing.md:40` stays today's skip for `big` and an absent tier and is not updated for the irreversible halt), `docs/authoring-portable-skills.md`
- Every file under `tests/`. No new test module and no new drift test.

## Decisions

### Decision 1 — Four tiers

Brief Decision 1. The tiers are `tweak`, `small`, `big`, and `irreversible`. `irreversible` adds reviewer context and an unskippable ship-spec review gate on top of `big`. It does not add a lens. `scale_lens` is still decided only by `## Scale`. Design § spec-cycle sets `round_cap` from the tier and does not touch step 8's scale parse.

### Decision 2 — Carrier

Brief Decision 2. spec-brief writes `## Tier`. spec-cycle records the tier as a carried-forward Decision whose recognition line is a whole line `**Tier:**` plus `small`, `big`, or `irreversible`, and writes `tier:` on every marker, including attest mode. Attest mode reads that line from the spec because it does not run Phase 0 steps 2 to 8. Once a spec exists, a recorded line is authoritative over a later brief edit. ship-spec reads the spec line every time and uses the marker's `tier:` only as a consistency check. It does not read the brief for the tier. Step 2 still only checks that the brief file exists. A marker `tier:` that is missing is not a disagreement. A marker `tier:` that is malformed or differs from the spec puts a green marker in the `changed` state; the spec's value still governs after the operator confirms. An absent spec line means `big`. `irreversible` does not proceed past a skipped review gate in any marker state.

### Decision 3 — The operator sets the tier

Brief Decision 3. spec-brief recommends and asks. Nothing in any mode writes a tier the operator did not choose. There is no `--tier` flag and no default that skips the question.

### Decision 4 — Tweak floor

Brief Decision 4. The recommendation is `tweak` only when the estimate is known, the change is at most 2 files and under 50 lines, and it touches none of auth, payments, data, or config. Any of those four surfaces blocks `tweak` at any size. The estimate and the surface lists are Decision 14.

### Decision 5 — A tweak writes nothing

Brief Decision 5. `tweak` prints a NEXT block and stops, or, when the collision gate found a brief, spec, or reviews tree and the operator chose to proceed, stops by naming those paths. spec-brief does not delete them. `tweak` is never written into a brief, a spec, or a marker.

### Decision 6 — When the tier is asked

Brief Decision 6. The seed gate runs, then the tier gate, then the interview. Both gates run under `--no-grill`. An empty seed halts before the tier question. Confirm can change the tier. A change to `tweak` at Confirm takes the Decision 5 exit and does not reach Phase 4.

### Decision 7 — Small

Brief Decision 7. `small` dispatches the same three standing lenses, sets `round_cap` to 2, and makes ship-spec skip the review gate and keep the test gate. `round_cap` is the review-loop cap only. The grilling interview inside 2f-i keeps its own cap of 3 (`skills/spec-cycle/SKILL.md:646`). With `round_cap = 2`, round 1 is ordinary revision (`round < round_cap`), round 2 is the FROZEN/REWRITE rewrite (`round == round_cap`), and the recount's revert path (`2 ≤ round < round_cap`) does not run.

### Decision 8 — Irreversible review gate

Brief Decision 8. For `irreversible`, each of the three Phase 3b skip cases (no command declared, command not available, command failed — `skills/ship-spec/SKILL.md:187-195`) is a halt before Phase 4 that names the case, keeps the worktree, and waits. Option 1 re-resolves the review command through Phase 0 step 4b's three sources and runs Phase 3b again in the same run, so the implementation in the worktree is kept and the resume is the same invocation, not a new one. Option 2 stops with the worktree kept and the removal warning. A host that cannot wait takes option 2. For `irreversible` the return is classified by three tests in order, which replace today's untied "failed" and "found nothing" phrases (`:195`): (1) readable findings (a location plus a problem) anywhere in stdout or stderr mean the review ran, so continue into steps 4 to 8 whatever the exit code; (2) otherwise an affirmative clean statement from the reviewer itself (the clean-result text the reviewer's own definition documents, or an explicit "no findings" or "no issues" sentence) is success (step 8, zero counts, `None.`); (3) otherwise the return is `<command> failed`: empty output, an error about the command itself (not found, crash, traceback, usage or auth error) on either stream, or an error string with exit 0. In subagent mode the subagent's prompt also requires a first line `ran: yes | no — <why>` followed by the reviewer's output verbatim; `ran: no`, or a missing `ran:` line, is `failed`, and a subagent's own summary never counts as the reviewer's clean statement. A reviewer that is silent on success therefore cannot pass this tier as declared; the halt says so and names the remedy (declare `<command> && echo "no findings"`). `big` keeps today's looser reading. The once-per-run rule (`:185`) counts only passes that ran, meaning they reached steps 4 to 8; an irreversible halt pass did not run the review, and option 1 is the only route to another pass, uncapped because each pass needs an operator action. The run does not commit until the gate has run. (Folded after the round-3 green from D-1 and D-2 under the operator's standing ruling that in-scope P1s fold, then hardened by a two-lens delta pass; the brief's D8 carries the same text; the resume mechanism is this run's own halt-and-wait, the pattern the Phase 3 test-gate halt already uses.) The spec's tier applies after every marker state, including one the operator confirmed through. This supersedes the VHS-46 rule that a skipped review never blocks the commit, for `irreversible` only (`decisions/2026-10-08-vhs-46-ship-spec-review-gate-declared-one-pass.md`). `small`, `big`, and an absent line keep that rule.

### Decision 9 — Absence is big

Brief Decision 9. No `## Tier` heading in the brief, and no `**Tier:**` line in the spec, means `big`, with no warning. A present section or line whose value is missing, unknown, or `tweak` halts. It does not become `big`.

### Decision 10 — Reviewer prompts carry the tier

Brief Decision 10. Every dispatched reviewer, including the scalability reviewer when it runs, receives `tier: small | big | irreversible`. Each agent file lists that input. The shared P0/P1 definitions in `AGENTS.md` § Conventions stay as they are.

### Decision 11 — A host that cannot wait stops

Brief Decision 11. At the tier gate, a host that cannot wait prints `tier needs an operator — stopping` and stops. Nothing is written. The tier is not filled in.

### Decision 12 — Grammar

Brief Decision 12. In the brief, a whole-word `## Tier` heading, then a `**Level:** small | big | irreversible` line. Sibling lines are allowed and ignored, so VHS-54 can add one later. In the spec, the first whole line that is the tier line is the recorded Decision, wherever it sits. In both files the first match wins and a second match warns. `tweak`, an unknown token, or a missing value on a present section or line halts the reader.

### Decision 13 — spec-tickets ignores `tier:`

Risk 1, pinned here. `skills/spec-tickets/SKILL.md` reads the marker for the verdict only. Fields are `key: value` lines; the reader takes the first line for each key and ignores anything else (`:34-36`). The state table matches `verdict:` and `ticket:` (`:38-44`). The skill computes no fingerprint (`:198`). A `tier:` line is not a key that table reads, so it cannot change `missing`, `unreadable`, `pending`, `red`, or `green`. No edit to that skill.

### Decision 14 — Tweak heuristic

Risk 2, pinned here. The estimate comes from the ticket text (or the local-only paragraph) and the Phase 1 grounding facts. Scope rows do not exist yet. There is no diff.

A check that cannot be answered is unknown. Any unknown check, or any failed check, recommends `big`. The heuristic never recommends `small` or `irreversible` (spec pin beyond Risk 2). Those are choices on the prompt.

- **Files.** Distinct file paths the change names. A directory does not count. A wiki `state.md` or `filemap.md` that grounding opened does not count. No file path named for the change → unknown. Example 1 still recommends `tweak` when those wiki reads are present and the change names only `README.md`.
- **Lines.** An integer the texts tie to a line count or a diff size; a range uses its top; if several qualify, use the greatest. A ticket id, a date, a file count, or an item number does not qualify. "Under 50" means 49 or fewer. A single typo, a single wording replacement, or a single identifier rename, in one named file, with no other change described, estimates at 1 line (spec pin beyond Risk 2). If no qualifying number is stated, that 1-line estimate applies only to that single-edit case; any other change is unknown. A qualifying number wins over the 1-line estimate.
- **Surfaces.** `none` only when at least one file path is named and every named path and the described change were checked and none matched. No named path → unknown, which blocks `tweak`.

Built-in taxonomy. Matching is case-insensitive. A path signal equals one path segment, or equals the whole filename. `config.py` does not match the filename `config`. A directory segment `config` does. A one-word subject signal matches a whole word in the change description. A quoted multi-word signal matches that phrase with a word boundary at each end. The bare word "data" is not a signal.

| Surface | Path signal | Subject signal |
|---|---|---|
| auth | `auth`, `login`, `session`, `oauth`, `credential`, `secret`, `permission`, `rbac` | password, token, credential, secret, login, session, oauth, permission |
| payments | `billing`, `payment`, `invoice`, `subscription`, `checkout`, `payout`, `stripe` | charge, invoice, refund, payout, subscription |
| data | `migration`, `migrations`, `schema` | migration, schema, "drop table", "delete rows" |
| config | a segment or filename `config`; a filename `.env`; a filename `states.json`; a path under `.github/workflows/` | "environment variable", "feature flag" |

A `SKILL.md` file and a docs markdown file are not config unless a signal above matches. `AGENTS.md` and `CLAUDE.md` are not config unless a signal above matches.

**Extension.** Spec pin beyond Risk 2: an extension signal matches a named path as a substring on purpose, and is not the built-in segment rule. Read the target project's `AGENTS.md` and `CLAUDE.md` when each file is present. This is not the review-command order (`skills/ship-spec/SKILL.md:71-73` takes the first source). Each whole-word `## Tweak surfaces` heading contributes. Its body runs to the next `^#{1,6}` heading, the same rule as `## Tier` and `## Scale`. Each non-blank line is one extra signal. Strip one leading list marker (`-`, `*`, or `N.`) and then trim. A line that is empty after that is ignored. A remaining one-word line matches as a one-word signal. A remaining quoted phrase uses the phrase rule above. Any other remaining line is an unknown surface and recommends `big`. Its basis slot is `surfaces: unknown`, with the `never tweak` suffix and a short quote of the line. It is not `surfaces: none`. Signals union. Neither heading hides the other. A one-word signal matches a named path as a substring or the change description as a whole word. A quoted multi-word line uses the phrase rule above. A match blocks `tweak`. No heading in either file means the built-in four only. Extra signals only add surfaces.

**Basis line.** One line, three comma-separated slots, then the suffix. Files: `<n> file` or `<n> files` (singular when `n` is 1) plus ` (<paths>)`, or `files: unknown`. Lines: `~<m> line` or `~<m> lines` (singular when `m` is 1), or `lines: unknown`. Surfaces: `surfaces: none`, `surfaces: unknown`, or `surfaces: <name>`. When more than one surface matches, name every match, built-in order auth then payments then data then config, then extension lines in file order, joined by `+`. The suffix is `ticket text + grounding` when the recommendation is `tweak`, and `never tweak` otherwise.

Worked examples, normative for that shape:

1. Ticket "fix the typo recieve in README.md". Grounding also opened wiki `state.md` and `filemap.md`. Those do not count. The change names `README.md` only. Recommendation `tweak`. `basis: 1 file (README.md), ~1 line, surfaces: none — ticket text + grounding`
2. Ticket "add a state UUID to skills/ship-spec/states.json". Recommendation `big`. `basis: 1 file (skills/ship-spec/states.json), lines: unknown, surfaces: config — never tweak`
3. Ticket "make the gate stricter" and grounding names no path. Recommendation `big`. `basis: files: unknown, lines: unknown, surfaces: unknown — never tweak`
4. Ticket "drop table users in scripts/cleanup.sql". Grounding names that file and states 10 lines. The phrase "drop table" matches data. Recommendation `big`. `basis: 1 file (scripts/cleanup.sql), ~10 lines, surfaces: data — never tweak`

## Design

### spec-brief

**Seed gate.** Lift the seed-gate paragraph out of Phase 2 (`skills/spec-brief/SKILL.md:88`) so the sentence "Skipped entirely under `--no-grill`" (`:86`) no longer covers it. Place it after Phase 1 and before the tier gate. The rule text stays: a ticket or local-only paragraph that states no problem (under two sentences, or nothing a design decision could hang on) re-prompts once, then halts, and nothing is written. Phase 0 step 5c (`:65`) points at this step instead of "§ Phase 2". The interview's `empty-seed` return still halts with nothing written; that sentence stays with the rule.

**Tier gate.** Runs after the seed gate passes, in every mode, before the interview and before Confirm.

If the host cannot wait, print `tier needs an operator — stopping` and stop. Write nothing.

Otherwise compute Decision 14 and print:

```text
Tier: recommended <tweak|big>
<basis line>

1. tweak
2. small
3. big
4. irreversible
```

The recommended row carries ` (recommended)`. A reply of `1`, `2`, `3`, or `4` after trimming sets the tier. Any other reply stops and writes nothing.

`tweak` exits as Decision 5:

- Collision case: Phase 0 step 2 showed its halt and the operator chose option 1. Print the paths of the brief, the spec, and the reviews tree that exist, state that they stay actionable by `/ship-spec` and `/spec-close` until the operator removes or archives them and re-runs `/spec-brief` clean, and state that spec-brief deletes nothing. Do not print the NEXT block. A stale temp that step 2 already removed is not this case.
- Otherwise print:

```text
=== NO BRIEF WRITTEN: <TICKET-ID> ===
Tier: tweak
<basis line>

=== NEXT ===
No lifecycle — ship as a chore PR citing the ticket; the ticket's state and closing comment are yours to set, since no lifecycle stage will touch it.
```

The tweak path creates no brief temp and deletes nothing. `small`, `big`, or `irreversible` continues to the interview, or under `--no-grill` to Confirm. The chosen tier is kept for Confirm and Phase 4.

**Confirm.** The preview shows `Tier: <level>` and the basis line. Add option 4: `Change the tier — ask the tier gate again`. Option 4 shows the same prompt. A non-tweak choice returns to the preview with the new tier. A `tweak` choice takes the Decision 5 exit before Phase 4. Options 1 to 3 behave as they do now, except the post-cap menu. After a post-cap resume, Confirm re-renders with options 1, 3, and 4 (`skills/spec-brief/SKILL.md:105` today omits option 2, and option 4 joins that menu). Option 2 stays omitted there. On option 4's re-ask, a reply other than `1`–`4` re-prints the tier prompt and does not discard the interview. The first tier-gate ask, before any interview, still stops and writes nothing on any other reply. A revision (option 2) does not clear the tier.

**Phase 4.** On the write path the tier is `small`, `big`, or `irreversible`. Insert `## Tier` in the section list immediately before the conditional `## Scale` (`:125`). Emit exactly:

```markdown
## Tier

**Level:** small
```

with the chosen level. Emit no second `**Level:**` line and no sibling line. The rest of Phase 4, including Scale's four cases, is unchanged.

### spec-cycle

**Parse, beside step 8.** Resolve `tier` and `round_cap` once and hold them for the invocation. Do not change the scale parse, and do not set `scale_lens` from the tier. Apply the re-run pin before this parse can halt.

**Re-run pin.** If `docs/specs/TODO/<TICKET-ID>.spec.md` already exists, resolve its recorded line with the reader rule before judging the brief. A valid line (`small`, `big`, or `irreversible`) wins over an absent, disagreeing, or malformed brief. Warn `tier: brief <absent|disagrees|malformed> — using recorded` and do not halt. "Brief absent" means no `## Tier` section. A missing brief file already halts in Phase 0 step 2 (`skills/spec-cycle/SKILL.md:109`). A recorded label line that is not exactly one of the three halts `tier: malformed (<line>) — halting`, writes no marker, leaves an existing marker untouched, and does not fall through to the brief. If the spec has no label line, the brief governs this invocation and Phase 1 does not insert a line, because a re-run does not re-author. ship-spec then reads the spec as `big`. The marker for this invocation still carries the tier the invocation used, so a brief-driven `small` or `irreversible` against a spec with no line is ship-spec's `changed` state. The operator adds the line, or deletes the spec to re-author, the same remedy as the scale pin (`skills/spec-cycle/SKILL.md:330-340`).

**Brief parse.** Runs only when the pin did not already take a valid recorded line.

1. Heading. The first brief line matching `^#{1,6}\s+tier\s*$`, case-insensitive, is the section. The body runs to the next `^#{1,6}\s` heading or EOF. `## Tiering` and `## Tier list` do not match. No strict match → `tier = big`, `round_cap = 4`, no warning, and only then does the looser rule apply. More than one strict match → the first is authoritative and the run warns `tier: multiple Tier sections — using first`. A second strict heading is not a near-miss. The looser rule applies only when no strict heading matched, and it is case-insensitive, the same flag as the strict match: a heading that matches `^#{1,6}\s+tier\b` and whose body contains an unfenced `**Level:**` line is malformed: halt. A looser heading with no `**Level:**` line is ignored. This halt is stricter than Scale's warn-and-continue on purpose (Decision 12). Absence is `big`, so a near-miss that carries a Level line must not be read as absent. Do not warn-and-continue.
2. Level. Inside the section, ignore lines inside a fenced code block, the same fences as the spec reader. A Level line is an unfenced line that, after removing leading indentation, starts with the label `**Level:**` compared case-insensitively. The value is the text after the label, trimmed, then lowercased. Exactly `small`, `big`, or `irreversible` is the level: `small` → `round_cap = 2`; `big` or `irreversible` → `round_cap = 4`. Any other value, including empty, `tweak`, a trailing note, or punctuation stuck to the token, halts `tier: malformed (<line>) — halting`. Write no marker. Leave an existing marker as it is. The first Level line wins. A second warns `tier: multiple Level lines — using first` and is ignored. If the strict section contains no unfenced Level line, halt `tier: malformed (no Level line) — halting`. Write no marker. Leave an existing marker as it is. Do not treat that section as absence. A fenced example, and a mid-line mention that does not start the line, does not set `round_cap` and does not count as the Level line. The looser heading's "no Level line → ignore" rule stays as it is.
3. Sibling lines in the section are ignored.

**Phase 1.** When the spec is created, write one Decision whose recorded line is a whole line of the form `**Tier:** small` (or `big`, or `irreversible`) matching the resolved tier. Do not write a second one. The scale Decision, when step 8 requires one, stays a separate Decision.

**Reader rule for the spec line.** Ignore lines inside a fenced code block. Fences are the ones the deferred-section rules already define: a marker of three or more backticks or tildes. Outside a fence, a present declaration is a line that, after removing leading indentation, starts with the label `**Tier:**` compared case-insensitively. The first such line wins. A second warns `tier: multiple Tier lines in the spec — using first`. The value is the text after the label, trimmed, then lowercased. Exactly `small`, `big`, or `irreversible` is the recorded tier. Any other value, including empty, `tweak`, a trailing note, or punctuation stuck to the token, halts `tier: malformed (<line>) — halting`. That line is not absence and is not `big`. Absence, which is `big` with no warning, means no label line at all. Where this spec says "no line", it means no label line. A sentence that uses the token without that label is not a declaration. Attest mode, the re-run pin, and ship-spec use this rule and no other.

**Preflight summary.** Add `tier: <level> (round_cap=<n>)` to the one-line summary.

**`round_cap` substitution.** `small` is 2. `big` and `irreversible` are 4. Ordinary revision runs while `round < round_cap`. The recount reverts an original fold only when `2 ≤ round < round_cap`. The final round, `round == round_cap`, is the FROZEN/REWRITE rewrite, and the recount does not revert there. The closed-issues manifest and the FROZEN test cover rounds `1 .. round_cap − 1` and no other window. The FROZEN test does not also count `round == round_cap`. That is Decision 7. 2f halts after round `round_cap`. The red marker's `round:` field, the halt text, the report directory `round-<round_cap>/`, and 2f-i all use that parameter. Grilling's own cap of 3 is not this parameter. Neither is a step number, menu option 4, or the phrase "2f-i step 4".

In `skills/spec-cycle/SKILL.md`, rewrite these and no other numerals:

| Line | Today | Replacement |
|---|---|---|
| 3, 17 | `4 passes complete` | `round_cap passes complete` |
| 36 | `round: <1-4>` | `round: <1..round_cap>` |
| 369 | `≤4 passes` | `≤ round_cap passes` |
| 373 | `For each round 1..4` | `For each round 1..round_cap` |
| 495 | `rounds 1–3` / `round 4` | `rounds 1 .. round_cap−1` / `round == round_cap` |
| 497 | `round < 4` | `round < round_cap` |
| 507 | `after round 4` | `after round round_cap` |
| 510, 525 | `round 4 (grill)` | `round <round_cap> (grill)` |
| 510, 531 | `round-4 grill` | `round-<round_cap> grill` |
| 548 | `round 2 or 3`; `at round 4` | `2 ≤ round < round_cap`; `at round round_cap` |
| 549 | `round 4` in the otherwise-list | `round == round_cap` |
| 551 | `round == 4` | `round == round_cap` |
| 555, 565 | `rounds 1–3` | `rounds 1 .. round_cap−1`. This is the only FROZEN window. Do not also count `round == round_cap`. |
| 672 | `under the 2e rounds-1–3 rules` | `under the round < round_cap revise rules`, and do not re-run FROZEN. Do not change `routing steps 1–3` or menu `options 1–3`. |
| 560 | `round 4`, and `rounds 1–3 half` | `round round_cap`, and `round < round_cap half` |
| 581 | `at round 4` | `at round round_cap` |
| 587 | `after round 4`; `round: 4`; `round-4 total` | `after round round_cap`; `round: <round_cap>`; `round-<round_cap> total` |
| 589 | `AFTER 4 ROUNDS` | `AFTER <round_cap> ROUNDS` |
| 591–594 | `round 4` on each lens bullet | `round <round_cap>` |
| 620, 622, 656, 676, 685 | `round-4` paths and "round-4 reports" / "round-4 FROZEN" | `round-<round_cap>` |
| 658 | header `round 4` | `round <round_cap>` |
| 688 | `The round counter is still 4` | `The round counter is still round_cap` |

At line 646 the grilling call passes the literal 3. Name that bound the interview cap, not the review-loop variable `round_cap`. Do not change the value 3. Add one clause that this cap is the interview's, not the review loop's.

**Marker.** In the template (`:29-42`), after the `gate:` line, add:

```text
tier: small | big | irreversible
```

The pending write (`:371`), the red write (`:587`), the green write (`:757`, which follows the template), and the attest write (`:839`) each include `tier:` set to the invocation's tier. Attest mode, after the heading check (`:822`) and before the marker is classified (`:823`), reads the spec with the reader rule above. No line → `big`. A line outside the three values → halt `tier: malformed (<value>) — halting` and write nothing. A second line warns and is ignored. The already-green early return (`:824`) stays: a matching green marker is not rewritten just to add `tier:`. A marker attest does write includes `tier:`.

**Reviewer prompts.** The 2b list (`:397-404`) gains `tier: <small|big|irreversible>`, passed to every dispatched reviewer, including scalability when `scale_lens == on`.

### ship-spec

In step 1b, before the state table is acted on, read the spec with the reader rule above. Never read the brief for this. No line → `big`, no warning. A value outside the three, including `tweak`, → halt `tier: malformed (<value>) — halting`. No confirm-through and no write. A second line warns and is ignored.

Then classify the marker. Extend the `green` and `changed` rows (`skills/ship-spec/SKILL.md:30-31`) without reordering the table:

- `green` when `verdict: green`, the fingerprint matches, and either there is no `tier:` line or the first `tier:` line is exactly `small`, `big`, or `irreversible` and equals the spec tier.
- `changed` also when `verdict: green`, the fingerprint matches, and a `tier:` line is present but is not one of those three tokens or differs from the spec tier. The confirm names the marker value and the spec tier, and says the gate follows the spec tier. When the spec has no label line, the confirm says the spec tier is `big` because no line was recorded, and that a different marker `tier:`, including `irreversible`, will not be enforced.

spec-cycle's canonical marker table (`skills/spec-cycle/SKILL.md:60-69`) stays fingerprint-only. ship-spec's `green` and `changed` rows are the copy that adds the tier clause. spec-tickets is not that copy and is not edited (Decision 13).

`red`, `pending`, `missing`, and `unreadable` keep their current rows and still win when they match first. After the operator confirms a non-red state, Phase 3b uses the spec tier, not the marker's `tier:`. Attest's already-green early return is unchanged: a fingerprint match does not rewrite `tier:`.

The preflight summary names the tier next to the verdict state.

**Phase 3b.** The opening claim that a skip never blocks the commit (`:183`) gains the irreversible exception. The once-per-run sentence (`:185`) gains the same exception: it counts passes that ran (reached steps 4 to 8); an irreversible halt pass did not run the review, and option 1 below is the only route to another pass, available after every halt. "Not run again after fixes, a test-loop re-entry, or an operator fix" still holds once the review has run.

- `small`: before the three skip cases, print `review gate: skipped (small tier)`, keep `- [ ] Review gate: skipped — small tier` for the PR body, write no review file, and go to Phase 4. `small` does not skip Phase 3. The existing `Test command: N/A` skip (`skills/ship-spec/SKILL.md:60`, `:144`) still applies to every tier: do not run the command `N/A`. A doc-only `small` change whose test command is `N/A` commits with both the test loop and the review gate skipped, after the verdict check. Do the review-gate skip even when a review command is declared.
- `irreversible`: do not skip. For no command, the case is `no review command declared` and no review file is written, which is today's no-command case. For an unavailable command (including step 3's "command not found" come-back to step 2), the case is `<command> not available`. For a command that errors or returns nothing readable as findings, the case is `<command> failed` and the halt includes the first 20 lines of the error text. Classify the return by Decision 8's three ordered tests: readable findings anywhere in stdout or stderr mean the review ran, continue into steps 4 to 8 whatever the exit code; otherwise an affirmative clean statement from the reviewer itself (its documented clean-result text, or an explicit "no findings" or "no issues" sentence) goes straight to step 8 with zero counts and `None.`; otherwise `<command> failed`, which covers empty output, an error about the command itself on either stream, and an error string with exit 0. In subagent mode (step 3), the prompt also requires a first line `ran: yes | no — <why>` followed by the reviewer's output verbatim; `ran: no` or a missing line is `failed`, and the subagent's own summary is never the clean statement. On the unavailable and failed halts, write today's skipped-form review file (command, case, first 20 lines of the error) before waiting; a halted pass keeps no PR-body line; a later pass that runs replaces the review file whole in step 8 and sets the only `Review gate:` PR-body line. Every review file written after the first halt of a run, skipped-form or full, carries `- Halted passes: <n> (<case> | <case>)` directly after `- Result:`, so a run that stops after several halts keeps its history. Halt text:

```text
REVIEW GATE: irreversible tier — <case>.
<first 20 lines of the error text — failed case only; when the return was empty: (no output, exit <code>)>
Nothing is committed. The worktree is kept.
Worktree: <worktree-path>
Branch: <branch>
Command from: <absolute path of the source that step 4b took, and its section> | none — checked <project-root>/<spec-path> § Review command, <project-root>/CLAUDE.md § Review command, <project-root>/AGENTS.md § Review command
Repair or declare the command in the primary checkout, not in the worktree: step 4b reads only the primary checkout, and a worktree copy of CLAUDE.md or AGENTS.md would be committed with the change. Editing the spec's § Review command changes its fingerprint, so later readers see the verdict as changed.
<empty-return case only:> A command that prints nothing on a clean run cannot pass the irreversible tier. Declare one that states its clean result, e.g. <command> && echo "no findings".
1. Re-run the review gate — re-resolve the command (Phase 0 step 4b) and run Phase 3b again in this run
2. Stop — the worktree stays; `git worktree remove` refuses a dirty worktree and `git worktree remove --force` discards the uncommitted implementation
```

Wait for the operator. Trim the reply: `1` re-runs, `2` stops, and any other non-empty reply re-prints the halt and waits again, because the only in-run resume must not be lost to a typo. An empty reply or end-of-input is a host that cannot wait: print the halt once and take 2. On 1: when the test command is not `N/A`, re-enter Phase 3 with a fresh iteration count first, unconditionally, so edits made during the wait are tested (a status comparison cannot see a second edit to an already-modified file, and one test run per operator action is cheap); when that Phase 3 exits green, go to step 4b and then Phase 3b from step 1, not into Phase 3's normal flow. This loop has no cap because each pass needs an operator action, and the `Command from:` line makes a repeated identical halt self-explaining. On 2, print `review gate: irreversible halt — stopped, worktree kept at <worktree-path>` and stop. A host that cannot wait prints the halt and takes 2. There is no proceed-without-review option. When the command returns readable findings, steps 4 to 8 run as they do today.

- `big`, and an absent spec line: the three skip cases stay skips. The failure-mode bullets at `:432-433` gain an `irreversible` exception: those two cases halt with the Phase 3b case text and do not commit. `big` and an absent line keep today's skip. The bullets are not an unconditional "Never halt."

### Reviewer agents

In each of the four agent files, add this bullet to the orchestrator-input list, after the scale bullet already there (`agents/spec-reviewer-correctness.md:19`, `agents/spec-reviewer-edge-cases.md:19`, `agents/spec-reviewer-conventions.md:21`, `agents/spec-reviewer-scalability.md:20`):

```text
- `tier` — `small`, `big`, or `irreversible`, as passed by spec-cycle. Context for judging blast radius and reversibility in this lens's own reasoning. The shared P0/P1 definitions do not change with tier.
```

The scalability file gets the bullet even though it is dispatched only when scale is on. Do not change the `round_number` range comment. Do not change severity rules.

### Docs and AGENTS.md

`docs/spec-workflow-reference.md`, beside § Optional scalability lens (`:104`): add a section that states the four tiers and which skill each one changes, the `## Tier` / `**Level:**` grammar, Decision 14's heuristic with the four worked examples, the headless line `tier needs an operator — stopping`, absence meaning `big` with no warning, a malformed section halting, and `round_cap` of 2 for `small` and 4 otherwise. Rewrite the loop-cap sentences at `:84-86` and `:246`, and the leftover cap sentences at `:66` ("up to 4 rounds"), `:27` ("post-round-4"), and `:102` ("red at the round-4 halt"), so revision, rewrite, and halt follow `round_cap` rather than the literal 4. At `:11` and `:17`, the seed gate runs before the tier gate in every mode, including `--no-grill`, and is not part of the interview that flag skips. At `:21`, name `## Tier` on every brief Phase 4 writes. At `:187`, `irreversible` halts on the three skip cases and does not commit; `big` and an absent tier keep the skip. The review gate still runs for `big`, `irreversible`, and an absent tier when the test command is `N/A`. `small` skips it. Leave the grilling cap described as its own cap of 3 where this file mentions the post-halt interview.

`AGENTS.md`: in the spec-cycle bullet (`:27`), and in the post-round-4 mention at `:25`, say the loop runs up to `round_cap` rounds (2 when the tier is `small`, 4 otherwise) and the halt follows that cap. Grilling's own cap of 3 stays where `:25` is the interview. After the five-skill list, add a short stakes-tier paragraph: `tweak` stops in spec-brief with nothing written; `small` is three lenses, `round_cap` 2, and ship-spec skips the review gate while keeping the test gate; `big` is today's behaviour and is what an absent tier means; `irreversible` is `big` plus the tier on reviewer prompts plus a review gate that halts on the three skip cases; scale stays its own `## Scale` declaration. On the severity bullet (`:105`), add that those definitions do not change with tier. Next to the Scale bullet (`:108`), point at `## Tier` and at an optional `## Tweak surfaces` section a project may add, one signal per line, as Decision 14 describes. Do not add a populated `## Tweak surfaces` section to this repo.

## Test plan

The suite does not execute these skills. The check that can fail in CI is the existing unittest run, which includes `tests/test_lint.py` over skill frontmatter. No new test file, no new assertion, and no grep gate.

Review checklist for the PR:

1. The four Decision 14 examples produce the recommendation and the basis line written there when read against the heuristic text.
2. `skills/spec-tickets/SKILL.md` has no diff.
3. Reading the rewritten spec-cycle ranges with `round_cap = 2` gives revision in round 1 only, rewrite in round 2, and an empty revert condition. Reading them with `round_cap = 4` matches today's revision, rewrite, and revert predicates. The FROZEN window stays `1 .. round_cap−1` and does not include the final round.
4. `skills/spec-cycle/SKILL.md` still invokes grilling with its own cap of 3.
5. A spec line inside a fenced block, and a sentence that mentions the tier token mid-line, are not the recorded tier. A bare whole line is.
6. Absence of a brief section and absence of a spec line take the `big` path with no warning. A valid recorded spec line wins over a malformed brief, with the warning, and does not halt. A recorded line outside `small`, `big`, or `irreversible` halts and does not fall through to the brief. A present `tweak`, unknown, or empty value halts in spec-cycle, in attest mode, and in ship-spec. A strict `## Tier` section with no unfenced Level line halts and is not `big`.
7. Reading the rewritten ship-spec Phase 3b with tier `irreversible`: each of the three cases (no command, not available including the step-3 come-back, failed) halts before Phase 4 with its case text, the `Command from:` line, and the worktree kept; the three ordered tests classify the return (findings anywhere continue whatever the exit code; a reviewer's own affirmative clean statement reaches step 8 with zero counts; everything else is `failed`, including an exit-0 empty-output linter, which halts with the `(no output, exit 0)` line and the `echo "no findings"` remedy); in subagent mode `ran: no` or a missing `ran:` line is `failed` and the subagent's summary is never the clean statement; option 1 re-enters Phase 3 with a fresh count whenever the test command is not `N/A`, then step 4b, then Phase 3b from step 1, never Phase 1; `2`, an empty reply, and a host that cannot wait stop with the worktree kept; any other reply re-prints the halt; a `changed` marker the operator confirmed through still halts; a halted pass leaves no PR-body line, a later pass that runs sets the only one, and every review file after the first halt carries `- Halted passes:` after `- Result:`. Reading the same text with `big` or an absent tier gives today's three skips and the `:185` once-per-run rule unchanged.

## Test command

```text
python -m unittest discover -s tests -p "test_*.py"
```

## Done when

- spec-brief: a non-tweak brief carries `## Tier` with a `**Level:**` line; a `tweak`, chosen at the tier gate or at Confirm, writes nothing and prints the NEXT block, or stops naming the stale artifacts when the collision gate found any; the seed gate runs before the tier gate in every mode; a host that cannot wait stops at the tier gate.
- spec-cycle: records the Tier Decision as a `**Tier:**` line, writes `tier:` on every marker write including attest mode, runs `small` with `round_cap = 2` (revision in round 1, rewrite in round 2, no fold reversion in round 2), and passes `tier` to every reviewer prompt.
- ship-spec: reads the spec's `**Tier:**` line as the tier and treats a malformed or disagreeing marker `tier:` as the `changed` state; `small` skips the review gate; `irreversible` halts on a missing, unavailable, or failed review command in every marker state, keeps the worktree, and offers to re-run the gate in the same run; a review that affirmatively states no findings, or a non-zero exit with readable findings, is success, and empty output is `failed`.
- A brief with no `## Tier` section, and a spec with no `**Tier:**` line, behave exactly as today. A malformed `## Tier` halts only when the spec has no valid recorded line. A valid recorded line wins and the run warns. A recorded line outside `small`, `big`, or `irreversible` halts and does not fall through to the brief.
- `docs/spec-workflow-reference.md` and `AGENTS.md` describe the ladder.
- Lint and tests pass.

## Out of scope

- `--tier` override flags on `/spec-cycle` or `/ship-spec`. The brief is the only initial source, and the spec's recorded line is the only source after authorship.
- Which executor runs each stage (VHS-54). The `## Tier` section leaves room for sibling lines and this spec does not define any.
- spec-close. A tweak writes no artifact. Every other tier closes as today.
- Changing which lenses run per tier. The lens set is fixed.
- Changing the shared P0/P1 severity definitions by tier.
- The brief doubt pass (VHS-56) and delta-scoped passes (VHS-27).

## Deferred (P2+)

- edge-cases/R1/F-11, attest half: not folded. Attest's already-green early return stays, so a fingerprint match does not rewrite `tier:`. Rewriting it would change the pin that a pre-VHS-55 green marker with no `tier:` line is left as it is. The confirm sentence in § ship-spec is the folded half.
- correctness/R1/F-9 and edge-cases/R1/F-12: no spec change. The Plane ticket body was not readable (`memory_search` access denied on namespace `skills`). The brief is the record.

## Deferred — follow-up required

> Known, unfixed P0/P1 findings. Not part of this spec's implementation: `/ship-spec` must not implement anything in this section. Each row becomes a follow-up ticket filed by the operator.

### D-1: Irreversible "re-run /ship-spec" cannot resume the worktree it just created
**Finding:** correctness/R1/F-4 (P1)
**Deferred in:** round 1
**Where:** spec § Decision 8 and Phase 3b irreversible halt (spec.md:60, spec.md:242-251)
**Suggested fix:**
> On the irreversible halt, print the worktree path and say the uncommitted tree is kept. Resume means repair the command and continue that worktree at Phase 3b, not re-enter Phase 0. If a full re-invocation is required, say that `git worktree remove` discards the implementation, and do not call that a resume.

**Propagation sites:** § Decision 8; § Design, ship-spec Phase 3b
**Scope:** in-scope — `skills/ship-spec/SKILL.md` Phase 1 pre-create checks and Phase 3b; brief Scope row `skills/ship-spec/SKILL.md`
**Follow-up:** none needed
**Discharged:** folded round 3 — § Decision 8; § Design, ship-spec Phase 3b; § Done when; § Test plan

### D-2: A clean irreversible review is specified as the failed halt
**Finding:** edge-cases/R1/F-3 (P1)
**Deferred in:** round 1
**Where:** spec § ship-spec, Decision 8 and Phase 3b, lines 60–61 and 243–251; `skills/ship-spec/SKILL.md:195`
**Suggested fix:**
> For `irreversible`, keep both carve-outs: a non-zero exit that still returns readable findings continues into steps 4–8, and a review that ran and found nothing is success (step 8, zero counts, `None.`), not `<command> failed`. Halt only for no command, command not available (including the step-3 "command not found" come-back), or a return that is an error or not a findings report.

**Propagation sites:** § Decision 8; § Design, ship-spec Phase 3b
**Scope:** in-scope — `skills/ship-spec/SKILL.md` Phase 3b; brief Scope row `skills/ship-spec/SKILL.md`
**Follow-up:** none needed
**Discharged:** folded round 3 — § Decision 8; § Design, ship-spec Phase 3b; § Done when; § Test plan

## Post-green polish

- correctness/R3/F-1 and edge-cases/R3/F-1: brief parse step 2 halts when a strict `## Tier` section has no unfenced Level line. Test plan item 6 names that case.
- correctness/R3/F-2: the irreversible halt says `git worktree remove` refuses a dirty worktree and `git worktree remove --force` discards it.
- correctness/R3/F-3: the `:187` sentence says the review gate still runs for `big`, `irreversible`, and an absent tier when the test command is `N/A`, and that `small` skips it.
- edge-cases/R3/F-2: an unknown tweak-surface line prints `surfaces: unknown` with the `never tweak` suffix and a short quote of the line.
