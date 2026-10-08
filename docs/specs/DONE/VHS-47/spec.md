# VHS-47 — A spec verdict on disk that /spec-tickets and /ship-spec read

## Goal

`/spec-cycle` writes one small file, the verdict marker, that says whether a spec ended green or red, when, and for which exact text. `/ship-spec` and `/spec-tickets` read it in preflight: green passes, red halts, and anything else (no marker, a review that did not finish, a spec edited since) asks the operator to confirm. An operator can attest a spec green when the verdict was reached by hand. Neither downstream skill reads a reviewer report or recomputes the gate.

## Scope

| Path | Change |
|------|--------|
| `skills/spec-cycle/SKILL.md` | Invocation line gains `--attest`. New `## The verdict marker` section (format, fingerprint, write rule). Pending write at the start of Phase 2. Green write after 2g. Red write in 2f. One sentence in 2f-i. New `## Attest mode` section. Phase 3 output gains one line. Tool-use notes and Failure modes entries. |
| `skills/ship-spec/SKILL.md` | New Phase 0 step 1b (read the verdict). Preflight summary names it. Phase 5 PR body gains one line. The "Spec not green" failure mode is rewritten. Tool-use notes bullet. |
| `skills/spec-tickets/SKILL.md` | Phase 0 step 4 becomes the verdict read. Step 2 gains one clause. The preflight line and the approval block gain a verdict line. Phase 4 step 1 re-reads the marker. Failure modes entries. Step 3 relabelled; step 6's `reviews:` token removed. Tool-use notes bullet. |
| `docs/spec-workflow-reference.md` | The spec-cycle, spec-tickets and ship-spec entries each describe the marker; spec-cycle's describes attest mode. |
| `AGENTS.md`, `README.md` | The three stage descriptions each gain a clause; `/spec-cycle`'s invocation shows `[--attest "<reason>"]`. |
| `docs/customizing.md` | `## Spec & brief layout` gains the marker's path. Spec-level addition: the brief's Scope names three docs, and this is the list VHS-46 extended for the same reason. |

Leave alone: `skills/spec-close/`, `skills/spec-brief/`, `skills/review-pr/`, `agents/`, `sync.py`, `lint.py`, `skills/ship-spec/states.json`, `docs/portability-contract.md`, `docs/authoring-portable-skills.md`, every file under `tests/`, and every skill's `requires:` block.

## Decisions

Brief decision numbers are in parentheses.

### Decision 1 — The marker file (brief 1, 10, 11; Risk 1)

Path: `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`. One marker per spec. Each write replaces the whole file.

```markdown
# Spec verdict: <TICKET-ID>

verdict: green | red | pending
source: review | operator-attested
ticket: <TICKET-ID>
spec: docs/specs/TODO/<TICKET-ID>.spec.md
round: <1-4> | not reviewed | in progress
gate: <P0+P1 count> | not reviewed | in progress
date: <YYYY-MM-DD>
fingerprint: sha256-lf:<64 hex digits> | none
reason: <one line>
replaces: <verdict>, <source>, round <round>, gate <gate>, <date> | none | unreadable
```

- Fields are `key: value` lines, lower-case keys, one per line, with the key at the start of the line. The `# Spec verdict:` heading is not a field. A reader takes the first line for each key and ignores anything else in the file.
- `reason` and `replaces` appear only on an operator-attested marker.
- A review-produced marker has `source: review` and real numbers in `round` and `gate`. A green one always has `gate: 0`.
- A pending marker has `source: review`, `round: in progress`, `gate: in progress`, `fingerprint: none`.
- An attested marker has `verdict: green`, `source: operator-attested`, `round: not reviewed`, `gate: not reviewed`.

### Decision 2 — The fingerprint (brief 16; Risk 1)

The fingerprint is the SHA-256 of the spec file's bytes after every carriage-return byte is removed, written as `sha256-lf:` followed by the 64 lower-case hex digits. Removing carriage returns makes the value the same for a CRLF and an LF checkout.

Compute it with the host's shell *(e.g., `tr -d '\r' < <spec-path> | sha256sum` in a POSIX shell, `shasum -a 256` in place of `sha256sum` on macOS, or the equivalent in your host)*. `/spec-cycle` computes it when it writes a green or red marker. `/ship-spec` computes it again to compare. Both skills already use the shell. `/spec-tickets` does not compute it.

If a writer cannot compute it, it writes `fingerprint: none` and prints `verdict marker: fingerprint not computed (<reason>)`. A green marker with `fingerprint: none` reads downstream as the changed-spec case.

### Decision 3 — When /spec-cycle writes (brief 8, 13, 17; Risks 2, 3)

1. **Pending.** At the start of Phase 2, once per invocation and before round 1's reviewers are dispatched, create the reviews directory if absent and write a pending marker. This covers a first run and a re-run on an existing spec alike, and replaces whatever marker was there.
2. **Green.** After 2g has finished and before Phase 3 prints, write a green marker: the round that went green, `gate: 0`, today's date, and the fingerprint of the spec as polish left it.
3. **Red.** In 2f, after round 4's 2e edits and before the halt block prints, write a red marker: `round: 4`, the round-4 `total_p0p1`, today's date, and the fingerprint of the spec as it stands at the halt.
4. **After the halt.** Options 1 to 3 end the skill with the red marker in place. Option 4 (2f-i) edits the spec and leaves the marker untouched: it stays red.
5. **Interrupted run.** Nothing more is written. The pending marker stays.

A marker write that fails does not change the run's outcome (a spec-level rule; the brief does not state one). Print `verdict marker NOT written: <error> — the marker on disk says <its verdict, or none>` at once, where the write was attempted: before round 1 for the pending write, under the SPEC READY header for the green write, above the halt block for the red write. The marker on disk is then whatever the last successful write left.

Phase 3's output gains one line under `Rounds:`: `Verdict: green — docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`, or `Verdict: green — marker NOT written` when that write failed.

### Decision 4 — Attest mode (brief 5, 6, 11, 12; Risk 4)

Invocation, written the same way everywhere: `/spec-cycle <brief-path> [--attest "<reason>"]`. In attest mode the path may also be the spec path; only the ticket id is taken from it, by Phase 0 step 1's existing prefix match, and the brief need not exist. `--attest` with no reason, an empty reason, or any other flag halts with `Usage: /spec-cycle <brief-path> [--attest "<reason>"]`. The reason is stored as one line; line breaks in it become spaces.

Attest mode runs none of Phase 0 steps 2 to 8, Phase 1, Phase 2, or Phase 3. It dispatches no reviewer and edits no spec. Its steps:

1. Resolve the ticket id and the spec at `docs/specs/TODO/<TICKET-ID>.spec.md`. If the spec does not exist, halt.
2. If the spec lacks any of `## Goal`, `## Scope`, `## Design`, `## Test plan`, `## Test command`, `## Done when`, `## Out of scope`, halt: `cannot attest: <heading> is missing`.
3. Read the current marker and classify it by Decision 5, computing the fingerprint.
4. If it is green and the fingerprint matches, print `already green and unchanged — nothing to attest` and stop. Nothing is written.
5. Otherwise print the current state, the spec path, and the reason, then:

   ```text
   ATTEST: <TICKET-ID>
   Current verdict: <state line, or none>
   Spec: docs/specs/TODO/<TICKET-ID>.spec.md
   Reason: <reason>

   This records the spec as green without a review round.
   1. Attest green
   2. Abort — nothing written
   ```

   Wait for the operator. Any reply other than `1` is treated as 2. A host that cannot wait prints `attestation requires an operator — nothing written` and stops.
6. On 1, write an attested marker (Decision 1) with today's date, the spec's fingerprint, the reason, and `replaces:` set from the old marker's `verdict`, `source`, `round`, `gate` and `date`; `none` when there was no marker; `unreadable` when it could not be parsed. Create the reviews directory if it is absent. Print the marker path. If the write fails, print `attestation NOT written: <error>` and stop; the spec's verdict is unchanged.

Attestation is allowed over no marker, a pending marker, a red marker, a green marker whose spec changed, and an unreadable marker.

### Decision 5 — How a reader classifies the marker (brief 2, 3, 4, 13, 14)

A reader looks at `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md` and lands on exactly one state. The rows are tested top to bottom and the first that matches wins:

| State | When | What the reader does |
|-------|------|----------------------|
| `missing` | The file or its directory does not exist | Confirm |
| `unreadable` | The file has no `verdict:` line with one of the three values, or its `ticket:` line is absent or names another ticket | Confirm, naming the reason |
| `pending` | `verdict: pending` | Confirm: a review started and did not finish |
| `red` | `verdict: red` | Halt, whether or not the spec has changed |
| `green` | `verdict: green` and the reader computed a fingerprint equal to the marker's | Pass |
| `changed` | `verdict: green` and the computed fingerprint differs, or the marker's `fingerprint:` line is absent or `none`, or the reader could not compute one | Confirm: the spec is not the text that was judged |

`green` carries its kind: `review, round <n>` or `operator-attested`. Both pass the same way (brief 7).

Every confirm stops on a host that cannot wait.

### Decision 6 — /ship-spec (brief 2, 3, 4, 7, 9, 14, 16)

New Phase 0 step 1b, directly after the spec path is resolved. It classifies the marker by Decision 5, computing the fingerprint.

- `green`: continue. Keep `- [x] Spec verdict: green (<kind>, <date>)` for the PR body.
- `red`: halt with

  ```text
  SPEC VERDICT: red (round <round>, gate <gate>, <date>).
  /ship-spec does not implement a red spec.
  Get a green verdict first: re-run /spec-cycle, or record your own review with
    /spec-cycle <spec-path> --attest "<reason>"
  ```

- `missing`, `unreadable`, `pending`, `changed`: print

  ```text
  SPEC VERDICT: <state> — <one line: what that means for this spec>
  1. Proceed — I have reviewed this spec
  2. Stop
  ```

  and wait. Any reply other than `1` is treated as 2. A host that cannot wait prints `spec verdict needs an operator — stopping` and stops. On 1, keep `- [ ] Spec verdict: <state> — proceeded on operator confirmation` for the PR body and continue. On 2, stop.

The one-line preflight summary names the state. Phase 5's PR body Test plan block carries the kept line. The "Spec not green" failure mode is rewritten to describe this step; the heading check it described stays as a second sentence, because a spec with missing headings still cannot be implemented.

### Decision 7 — /spec-tickets (brief 9, 15, 16)

Phase 0 step 4 ("if the reviews directory is absent, warn once and continue") is replaced by the verdict read. `/spec-tickets` classifies by Decision 5 without computing a fingerprint, so a `verdict: green` marker is always `green` here and never `changed`, including one whose `fingerprint:` is `none`; its verdict line says the fingerprint was not checked either way.

- `red`: halt in preflight, before any draft, with Decision 6's red block, its second line reading `/spec-tickets does not file tickets for a red spec.`
- Anything else: keep a verdict line and continue. There is no separate prompt.

The verdict line is printed in the Phase 0 summary and in the approval block, directly under `Storage:`:

- `Verdict: green (<kind>, <date>) — fingerprint not checked on this host`
- `Verdict: missing — no recorded review for this spec`
- `Verdict: pending — a review started and did not finish`
- `Verdict: unreadable (<reason>) — treated as no recorded review`

`Approve and file` is the operator's confirmation of that line.

Phase 4 step 1 gains a second check: read the marker again; if the verdict line it would now print differs from the line that was printed, halt with no writes and ask for a new approval. A marker that turned red is caught here.

Phase 0 step 2's sentence that the reviews directory is not read for pieces gains a clause: the verdict marker is read for the verdict and for nothing else.

### Decision 8 — No backfill; /spec-close and /spec-brief unchanged (brief Out of scope)

Specs written before this change have no marker and meet the confirm. `/spec-close` archives `<TICKET-ID>.reviews/` whole, so the marker travels to `DONE/<TICKET-ID>/reviews/verdict.md` with no change to that skill. `/spec-brief`'s collision check already halts when a spec or a reviews directory exists; a marker inside that directory changes nothing there.

### Decision 9 — Scale is a non-factor

The brief's `## Scale` sets `**Factor:** no`. One file per spec, one read per run.

### Decision 10 — Capability blocks are untouched (Risk 5; brief Out of scope)

`/spec-cycle` already declares `shell: true` and `filesystem: [read, write]`, which cover the hash command and the marker write. `/spec-tickets` declares `filesystem: [read, write]`, which covers reading one more file; it gains no shell. `/ship-spec` has no `requires:` block and gains none here (VHS-51). The lint census stays 11.

### Decision 11 — Room for later work (Risk 6)

The marker is written at three named points and read through one classification table. A later change that adds another way to reach a verdict (VHS-27's delta rounds) writes through the same green or red step. Nothing here depends on there being exactly four rounds except the `round:` value's range, which is descriptive.

## Design

### `skills/spec-cycle/SKILL.md`

- **Invocation line.** `Invoked as: /spec-cycle <brief-path>` becomes `/spec-cycle <brief-path> [--attest "<reason>"]`, with one sentence: with `--attest` the path may be the spec path; see `## Attest mode`.
- **New `## The verdict marker`,** placed after `## Why split from /ship-spec`. It holds Decision 1's template and field rules, Decision 2, the failed-write rule from Decision 3, and, under a `### Reading the marker` sub-heading, Decision 5's table. That table is the canonical copy; `/ship-spec` and `/spec-tickets` each carry their own, because a skill is read alone. Decision 2's last sentence is written here as: a green marker with `fingerprint: none` reads as the changed-spec case in `/ship-spec`; `/spec-tickets` does not look at the fingerprint. The write steps below refer to this section.
- **Phase 2.** A new first paragraph before `### 2a`: the pending write (Decision 3 item 1).
- **2d.** The sentence that breaks the loop on green gains: the green marker is written after 2g, not here.
- **2f.** One sentence before the halt block: write the red marker (Decision 3 item 3).
- **2f-i.** The closing "2f-i never …" sentence gains the clause `never rewrites the verdict marker,` directly after `never edits the brief,`, so "and runs at most once per invocation" stays the last clause and the next sentence's "That last bound" still points at it.
- **Phase 3.** A new first sentence, before the output template: write the green marker (Decision 3 item 2). Every green run reaches Phase 3, whether 2g folded candidates or left by its no-candidate exit, so the write lives here and 2g is not edited. The output template gains the `Verdict:` line in one of three forms: `Verdict: green — <marker path>`; `Verdict: green — <marker path> (fingerprint not computed)`; `Verdict: green — marker NOT written`. The failed-write line from Decision 3 is printed directly under the SPEC READY header, above the template's `Path:` line.
- **New `## Attest mode`,** placed after Phase 3 and before Tool-use notes: Decision 4 in full.
- **Tool-use notes.** One bullet: a shell hash command for the fingerprint; Write for the marker.
- **Failure modes.** Three bullets: marker write fails; fingerprint cannot be computed; an interrupted run leaves pending.

### `skills/ship-spec/SKILL.md`

- **Phase 0 step 1b:** Decision 6 in full, carrying Decision 5's table, Decision 1's reading rule (key at the start of the line, first line per key, the `# Spec verdict:` heading is not a field), and Decision 2's fingerprint rule and tagged example, worded as in `/spec-cycle`. A green marker whose `source:` is absent or not one of the two values prints its kind as `source not recorded`; one with no `date:` prints `no date`.
- **Tool-use notes:** one bullet: a shell hash command to check the fingerprint.
- **Preflight summary sentence:** names the verdict state and, for green, its kind.
- **Phase 5:** the Test plan block gains the kept `Spec verdict:` line, placed directly above the `Review gate:` line. The test-command bullet stays first, so the existing `N/A` rule ("replace the first bullet") is unchanged.
- **Failure modes:** "Spec not green" rewritten as Decision 6 describes.

### `skills/spec-tickets/SKILL.md`

- **Phase 0 step 2:** the added clause.
- **Phase 0 step 3:** its label changes from "Green-lit check" to "Heading check", and the Failure modes entry "Spec not green-lit" becomes "Spec incomplete". The verdict read is now what "green-lit" means.
- **Phase 0 step 4:** replaced by Decision 7's read, carrying Decision 5's table adapted to this skill: no `changed` row; the `green` row has no fingerprint clause; the action column reads "shown in the approval block" where the canonical table says Confirm, and "halt" for red. It carries Decision 1's reading rule in the same words as the other two skills, and the same fallback for a green marker with no usable `source:` or `date:`.
- **Phase 0 step 6:** the printed line becomes `ticket: <PARENT-ID> · headings: ok`, followed on its own line by the verdict line from Decision 7. The `reviews: present | absent` token is removed, since the verdict line covers it.
- **Phase 3:** the approval block template gains the `Verdict:` line under `Storage:`. The "Option 1 is omitted" list is unchanged; red never reaches the block.
- **Phase 4 step 1:** the second check.
- **Failure modes:** two bullets: red verdict halts in preflight; verdict changed while approval waited.
- **Tool-use notes:** one bullet: reads the verdict marker; computes no hash.

### Docs

- `docs/spec-workflow-reference.md`: in the spec-cycle entry, its `**Invocation:**` line gains `[--attest "<reason>"]`, and a short `### Verdict marker` subsection is added (what it records, the three write points, attest mode in two sentences). In the spec-tickets entry, one bullet. In the ship-spec Phase 0 entry, one sentence.
- `AGENTS.md` items 2, 3 and 4 and `README.md`'s three stage bullets: one clause each. `/spec-cycle`'s invocation is shown as `/spec-cycle <brief-path> [--attest "<reason>"]` in both.
- `docs/customizing.md` § Spec & brief layout: add `docs/specs/TODO/<TICKET-ID>.reviews/verdict.md`, described as the spec's recorded verdict.

No new text contains an `mcp__` name. The only command shown is the tagged hash example.

## Test plan

Mechanical gate:

1. `python tests/test_lint.py` exits 0 with 11 skills and zero ERROR.
2. `python tests/test_spec_close_log.py` exits 0.
3. `python lint.py --strict` exits 0.
4. `skills/spec-cycle/SKILL.md` contains `## The verdict marker` and `## Attest mode` exactly once each.
5. `verdict.md` appears in each of the three skills.
6. `skills/ship-spec/SKILL.md` contains `SPEC VERDICT: red`.
7. The leave-alone paths have no diff against `origin/main`.
8. No `requires:` block changed: the frontmatter of the three skills is unchanged.

Review checklist for the skill text. The mechanical gate does not cover it:

- The marker template and field rules in `/spec-cycle` match Decision 1 exactly.
- Pending is written once, at the start of Phase 2, on a first run and on a re-run.
- Green is written at the top of Phase 3, so it is reached from both exits of 2g (candidates folded, and none tagged); red is written in 2f after round 4's edits; 2f-i writes nothing.
- A failed marker write prints its line and does not change the run's outcome.
- Attest mode: usage errors halt; an incomplete spec is refused; green-and-unchanged writes nothing; the prompt is shown and a host that cannot wait writes nothing; the written marker has `not reviewed` for round and gate, the reason, and `replaces`.
- Attest mode dispatches no reviewer and edits no spec.
- `/ship-spec` step 1b: green passes; red halts with the red block (four lines, ending in the `--attest` line); each other state prints the two-option prompt; a host that cannot wait stops; the PR body carries the right line.
- `/spec-tickets`: red halts before any draft; every other state reaches the approval block with its verdict line; no fingerprint is computed and the green line says so; Phase 4 re-reads the marker.
- Neither downstream skill reads a reviewer report or computes a gate.
- The fingerprint rule (carriage returns removed, `sha256-lf:` prefix) is stated once in `/spec-cycle` and restated identically in `/ship-spec`.
- The classification table's rows and order are the same in all three skills, apart from the `/spec-tickets` adaptations the Design names (no `changed` row, no fingerprint clause, its own action column).
- The reading rule is stated in all three skills.
- No `requires:` block changed.

Behavioural acceptance (brief Done-when bullets 1 and 2) is checked on the first runs after `python sync.py install`: a `/spec-cycle` run that ends green leaves a green marker that `/ship-spec` passes; an existing spec with no marker meets the confirm. This change's own `/ship-spec` run uses the installed pre-change skill and so performs no verdict check. The PR body lists both as unchecked post-merge steps, with a third: reply on the PR #31 CodeRabbit thread with this PR's link.

## Test command

Run from the repo root. It must exit 0.

```
python tests/test_lint.py && python tests/test_spec_close_log.py && python lint.py --strict && test "$(grep -c '^## The verdict marker$' skills/spec-cycle/SKILL.md)" = "1" && test "$(grep -c '^## Attest mode$' skills/spec-cycle/SKILL.md)" = "1" && grep -q 'verdict\.md' skills/spec-cycle/SKILL.md && grep -q 'verdict\.md' skills/ship-spec/SKILL.md && grep -q 'verdict\.md' skills/spec-tickets/SKILL.md && grep -q 'SPEC VERDICT: red' skills/ship-spec/SKILL.md && test -z "$(git diff --name-only origin/main -- skills/spec-close skills/spec-brief skills/review-pr agents sync.py lint.py skills/ship-spec/states.json docs/portability-contract.md docs/authoring-portable-skills.md tests)" && test -z "$(git diff origin/main -- skills/spec-cycle/SKILL.md skills/spec-tickets/SKILL.md skills/ship-spec/SKILL.md | grep -E '^[-+](requires:|  (shell|filesystem|network|subagents|services):)')"
```

## Done when

- /spec-cycle records its final verdict in a form another skill can read without parsing review reports. — Decisions 1 to 3 and the `## The verdict marker` section; checked by the review checklist now and by the first post-install run.
- /spec-tickets and /ship-spec check it in preflight and do not proceed silently on a spec that is red or was never reviewed. — Decisions 5 to 7; checked the same way.
- The CodeRabbit thread on PR #31 can be pointed at this ticket. — The PR body links PR #31, and replying on that thread is a listed post-merge step.

## Out of scope

- Backfilling markers for existing specs.
- `/spec-close` reading the marker.
- Delta-scoped review rounds (VHS-27) and VHS-43's work.
- Any change to the reviewer agents, the gate formula, or the routing rules.
- A `requires:` block for `/ship-spec`, and any change to an existing one (VHS-51).
- The executor that reads `/spec-tickets` children.
- Fingerprint checking in `/spec-tickets`.
- A marker for the brief, or any verdict on anything but the spec file.

## Deferred (P2+)

- edge-cases/R1/F-8 — Renaming a local-only ticket's artifacts makes a true green marker read `unreadable` (its `ticket:` no longer matches). Left: the operator meets one confirm, or re-attests.
- edge-cases/R1/F-9 — Attest mode does not say what it writes if the spec changes while its prompt waits, or if the hash cannot be computed. Decision 2's `fingerprint: none` rule applies; the marker then reads `changed` downstream.
- edge-cases/R1/F-10 — The hash example is POSIX. A host using another shell must produce lower-case hex over carriage-return-free bytes; Decision 2 states the rule, not every command.
- edge-cases/R1/F-11 — A re-run's pending write discards an attested marker's reason. Left: the reviews directory is in git once archived, and a re-run supersedes an attestation by design.
- conventions/R1/F-7 — Spec-level additions, for the drift check: `docs/customizing.md` in Scope; `replaces: unreadable`; the unknown-flag halt; removal of `/spec-tickets`' `reviews: present | absent` token; the failed-write rule.
- conventions/R1/F-8 — A headless `/ship-spec` now stops on every spec without a green marker. The brief decides this (Decisions 2 and 14). It differs from VHS-46's "a skip never blocks" because that was about an optional review and this is about whether the spec was reviewed at all.
- conventions/R1/F-10, F-11 — Attest mode restates the seven-heading list; the fingerprint is a prose shell command, not a tested script. Left as written.
- correctness/R1/F-10 — The usage line shows `<brief-path>`; attest mode also accepts the spec path, stated in Decision 4's first sentence.
- edge-cases/R2/F-5 to F-10; conventions/R2/F-7 to F-11; correctness/R1/F-9 — a run where every marker write fails leaves an earlier marker (each failure prints); a marker that errors on read, or carries trailing carriage returns, is treated as `unreadable` by a careful reader; filling in a `Follow-up:` value after green makes the spec read `changed`; the leave-alone check diffs against `origin/main` as it stands at ship time; `verdict.md` is the one file in the reviews tree that is rewritten in place, and round reports stay immutable; an attested green is an operator claim that is labelled, not verified, by the brief's decision. Round-2 spec-level additions for the drift check: the "Heading check" relabel, "any reply other than `1`", and `/spec-tickets` showing a `fingerprint: none` marker as green.

## Post-green polish

- correctness/R2/F-1, conventions/R2/F-1 — § Design: one spelling for the invocation line; the workflow reference's invocation line named.
- correctness/R2/F-2, conventions/R2/F-3, edge-cases/R2/F-3 — § Test plan: "three-line block" corrected; the green-write row now names both exits of 2g.
- correctness/R2/F-3, conventions/R2/F-4 — § Design: the verdict-marker section words the `fingerprint: none` rule per reader.
- correctness/R2/F-4, edge-cases/R2/F-2, conventions/R2/F-2 — § Design and § Test plan: the reading rule is carried into both readers, with a checklist row.
- edge-cases/R2/F-1 — § Design and § Test plan: the `/spec-tickets` copy of the table is an adaptation, named as such.
- edge-cases/R2/F-4, conventions/R2/F-6 — § Design: a green marker with no usable `source:` or `date:` has a stated kind to print.
- conventions/R2/F-5, correctness/R2/F-6 — § Design: Phase 3's `Verdict:` line has three forms and the failed-write line has one position; the preflight summary names the kind.
- correctness/R2/F-5 — § Scope: rows now list the Tool-use notes bullets and the `/spec-tickets` relabel.
