# Edge-Cases Review — round 1

Spec: `docs/specs/TODO/VHS-47.spec.md` · Brief: `docs/specs/TODO/VHS-47.brief.md`

Grounding: spec and brief read from disk; `AGENTS.md` and the machine-local `CLAUDE.md` read; `skills/spec-cycle/SKILL.md` (Phase 0 step 1–2, Phase 1 re-run rule, 2c–2g, Phase 3, Tool-use notes, Failure modes), `skills/ship-spec/SKILL.md` (Phase 0, Phase 5 PR body, Failure modes), `skills/spec-tickets/SKILL.md` (whole file) and `skills/spec-brief/SKILL.md` (collision check) read. Ticket lookup in shared memory skipped per orchestrator note (ACL); the brief is the ticket text. The spec has no `## Deferred — follow-up required` section, so there are no rows to validate.

## Closure of round 0 findings

N/A — round 1

## Findings

No P0 or P1. Walking every state of the marker against both readers, I found no path on which the text, followed as written, lets a red or never-reviewed spec through `/ship-spec` without a prompt, and no write step that records a verdict the run did not reach. The findings below are places where a failure path has no stated outcome or where a reader rule has a gap that a careful agent would resolve, but that the skill text should pin.

### F-1: A failed pending write is silent on the interrupted path and leaves the previous verdict standing
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3, lines 59 and 65
**Edge case:** Partial failure. A re-run of `/spec-cycle` on a spec whose marker is green; the pending write fails (on Windows, `verdict.md` open in an editor that holds a lock is the realistic cause); the run is then interrupted, or stops mid-loop at 2e's "stop and tell the operator".
**What happens:** Line 65 places the `verdict marker NOT written` line "directly under the SPEC READY header or above the halt block". A run that never reaches either prints nothing about the failed pending write. The marker on disk is the earlier green one. If no 2e edit landed before the stop, the fingerprint still matches and `/ship-spec` reads `green` with no prompt, although the newest review found blocking findings and did not finish. If edits did land, `/ship-spec` reads `changed` and confirms, but `/spec-tickets` shows `Verdict: green`. Line 65's "normally pending" is also wrong for this case: the last successful write was the earlier run's.
**Why the spec misses it:** The failed-write rule was written for the green and red writes and names only their two print positions.
**Suggested fix:** In Decision 3, add: "If the pending write fails, print `verdict marker NOT written: <error>` at once, before round 1 is dispatched, and name the marker that is still on disk (`previous marker still in place: <state line>`). Repeat the line under the SPEC READY header or above the halt block." Change "normally pending" to "pending, or the previous run's marker when the pending write was the one that failed". Add the same sentence to the Failure-modes bullet for a failed marker write.

### F-2: Attest mode has no stated outcome when its own write fails, and does not say to create the reviews directory
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 4 step 6, line 93; § Decision 3, line 65
**Edge case:** Partial failure. Attesting a hand-written spec that has never been reviewed, so `<TICKET-ID>.reviews/` does not exist; or a write that errors.
**What happens:** Step 6 says "write an attested marker … Print the marker path." The only failed-write rule (line 65) is worded for a review run and names positions that do not exist in attest mode. An agent following step 6 literally prints the marker path after a write that failed, which tells the operator the spec is attested when it is not. Downstream stays safe (the marker is still missing, pending or red), so this is a misleading message, not a false verdict on disk. Decision 3 item 1 creates the directory for the pending write; step 6 does not say so for the one case where attest is the first writer.
**Why the spec misses it:** Decision 4 reuses Decision 1's write without restating Decision 3's directory and failure handling.
**Suggested fix:** Step 6: "Create the reviews directory if absent. If the write fails, print `verdict marker NOT written: <error> — the spec is not attested` and stop; do not print the marker path."

### F-3: Phase 3 still prints `Verdict: green — <marker path>` when the green write failed
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 3, lines 65 and 67
**Edge case:** Partial failure of the green write.
**What happens:** Line 65 prints `verdict marker NOT written` under the SPEC READY header; line 67 adds an unconditional `Verdict: green — docs/specs/TODO/<TICKET-ID>.reviews/verdict.md` to the same block. The operator sees both, and the second points at a file that says pending. The same applies when the fingerprint could not be computed: the line reads green while `/ship-spec` will read `changed`.
**Why the spec misses it:** The Phase 3 line has one form.
**Suggested fix:** Give the line three forms: `Verdict: green — <path>`; `Verdict: green — NOT recorded (<error>); the marker on disk reads <state>`; `Verdict: green — <path> (fingerprint not computed; /ship-spec will ask to confirm)`.

### F-4: The two new prompts do not say what a reply other than `1` or `2` does
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 4 step 5–6, lines 88–93; § Decision 6, lines 132–136
**Edge case:** Malformed input: an empty reply, end of input, a timeout, `yes`, `ok`, or a longer line beginning with `1` ("1, but check the scope table first").
**What happens:** Both prompts define "On 1" and "On 2" only. `/spec-tickets` already pins this class for its own block (lines 122–125 of that skill: exactly `1` after trimming; a longer line starting with `1` is not approval; empty reply or timeout writes nothing). Without the same rule here, a loose reply can be taken as consent. In attest mode that is the one place in this change where a loose reading writes a green verdict.
**Why the spec misses it:** The prompts were written as two-option menus without a reply grammar.
**Suggested fix:** Add to both: "Exactly `1`, after trimming, proceeds. Any other reply, an empty reply, end of input, or a timeout is treated as `2`." For attest: "…and nothing is written."

### F-5: Decision 5 does not say which row wins when two match, or how a green marker with no usable `fingerprint:` line reads
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 5, lines 101–108; § Decision 1, line 43
**Edge case:** Malformed marker: (a) `verdict: red` with a `ticket:` value for another ticket matches both `unreadable` and `red`; (b) a `verdict: green` marker whose `fingerprint:` line is absent (a write cut short, or a hand edit) or whose value is not `sha256-lf:` plus 64 hex digits; (c) a `verdict: green` marker whose `source:` is absent or neither of the two values, so the kind in `green (<kind>, <date>)` has nothing to print.
**What happens:** The sentence "lands on exactly one state" is not true for (a) as written. For (b) the `changed` row lists "differs, or the marker's is `none`, or the reader could not compute one"; an absent line is none of the three by the letter. A careful agent lands on `unreadable` for (a) and `changed` for (b), which are the safe readings, but the table should say so. In `/spec-tickets`, (b) reads plain `green`.
**Why the spec misses it:** The table lists conditions per state without an evaluation order.
**Suggested fix:** State under the table: "Test the rows top to bottom and take the first that matches." Widen `changed` to "the marker's fingerprint is `none`, absent, or not in the `sha256-lf:` form". Add: "A green marker whose `source:` is absent or unrecognised is `unreadable`."

### F-6: `/spec-tickets` prints plain green for a marker whose fingerprint is `none`
**Severity:** P2
**Where:** spec § Decision 7, lines 142 and 149; § Decision 2, line 55
**Edge case:** `/spec-cycle` could not compute the hash and wrote `verdict: green`, `fingerprint: none`.
**What happens:** Decision 2 says such a marker "reads downstream as the changed-spec case". Decision 7 says a `verdict: green` marker "is always `green` here and never `changed`". The two sentences disagree for this one marker. Seeing `none` needs no hash and no shell, so this is not fingerprint verification; the approval line `green … — fingerprint not checked on this host` describes a check that could never have passed anywhere.
**Why the spec misses it:** Decision 7 treats every fingerprint value as opaque.
**Suggested fix:** Either scope Decision 2's sentence to `/ship-spec`, or add a fifth verdict line to Decision 7: `Verdict: green (<kind>, <date>) — no fingerprint recorded; the spec text cannot be matched to the verdict`. The second is one line and keeps the two decisions consistent.

### F-7: The test command's leave-alone check compares against a moving `origin/main`
**Severity:** P3
**Where:** spec § Test command, line 250; § Test plan items 7 and 8
**Edge case:** `origin/main` advances (another PR merges and a fetch runs) between the worktree cut and a later test run, for example during `/review-pr` fix rounds. `git diff --name-only origin/main -- tests …` then lists files this change never touched and the gate fails for a reason unrelated to the change. VHS-46 used the same form, so this is inherited. Separately, item 8 says "the frontmatter of the three skills is unchanged" but the command greps only two files; a `requires:` block added to `skills/ship-spec/SKILL.md`, which Decision 10 forbids, would pass.
**What happens:** A false red in the test gate (up to five wasted iterations); and one unguarded fence.
**Suggested fix:** Diff against `$(git merge-base origin/main HEAD)` in both clauses, and add `skills/ship-spec/SKILL.md` to the last clause's path list.

### F-8: Renaming a local-only ticket's artifacts makes a true green marker read `unreadable`
**Severity:** P3
**Where:** spec § Decision 1 (`ticket:`, `spec:` fields); `skills/spec-cycle/SKILL.md:60`
**Edge case:** Phase 0 step 2's local-only path tells the operator to rename every `<TICKET-ID>.*` artifact, the reviews directory included, once the real ticket exists. The marker inside keeps the old `ticket:` and `spec:` values.
**What happens:** Both readers classify it `unreadable` (ticket mismatch) and confirm. Safe, but a reviewed verdict is lost without the operator having edited the spec.
**Suggested fix:** One sentence in `## The verdict marker`: after a ticket rename the marker reads as unreadable; re-run or attest to record the verdict under the new id.

### F-9: Attest mode does not say which fingerprint it writes when the spec changes while the prompt waits, or when the hash cannot be computed
**Severity:** P3
**Where:** spec § Decision 4 steps 3 and 6, lines 77 and 93
**Edge case:** The operator makes one more edit while the ATTEST prompt is open, then answers `1`. Or the host cannot compute the hash.
**What happens:** Step 3 computes a fingerprint; step 6 writes "the spec's fingerprint" without saying whether it is recomputed. Either reading is safe (a stale one reads `changed` downstream). With no hash available, Decision 2 makes the attested marker `fingerprint: none`, which can never pass `/ship-spec`; the operator is told only `fingerprint not computed`.
**Suggested fix:** Step 6: "Compute the fingerprint again at write time." Add: "If it cannot be computed, say before the prompt that the attested marker will still meet the confirm in `/ship-spec`."

### F-10: The hash example is POSIX only; a PowerShell host can produce a different string for the same bytes
**Severity:** P3
**Where:** spec § Decision 2, lines 51–53
**Edge case:** `/spec-cycle` runs under a POSIX shell and `/ship-spec` under PowerShell, or the reverse. `Get-FileHash` prints upper-case hex and hashes the raw bytes, carriage returns included; reading the file as text and re-encoding it changes the bytes.
**What happens:** A spurious `changed` and one extra confirm. It degrades safely.
**Suggested fix:** Add to Decision 2: "Compare case-insensitively after trimming; the hash is over bytes, so remove carriage returns from the bytes, not from a decoded string."

### F-11: A re-run's pending write discards an attested marker's reason with no record
**Severity:** P4
**Where:** spec § Decision 3 item 1, line 59
**Edge case:** `/spec-cycle` is started on an attested spec and interrupted at once.
**What happens:** The reason and `replaces:` line are gone; only version control, if the marker is tracked, has them. `replaces:` exists only on an attested marker.
**Suggested fix:** None required. If wanted, let a review-produced marker carry `replaces:` too.

## Persistence checklist (the marker is new persisted state)

1. **Atomicity.** Whole-file replace with no temp-and-rename. A write cut short leaves either no `verdict:` line (unreadable, confirm) or a green line without a fingerprint (F-5). `verdict:` is the first field, so a truncated file never shows a verdict the writer did not intend. CHECKED, with F-5.
2. **Size bound.** Ten single-line fields; `reason` is one line of operator text with no length cap. CHECKED; not a finding at this scale.
3. **Idempotency on retry.** One path per spec, whole-file replace. CHECKED.
4. **Read-side filtering.** The `ticket:` comparison rejects a marker copied from another spec. CHECKED; see F-8 for the rename case.
5. **Forward-compat.** No version field, but a reader takes the first line per key and ignores the rest, an unknown verdict value is `unreadable`, and the `sha256-lf:` prefix names the algorithm. CHECKED once F-5 pins the non-matching-prefix case.
6. **Write-then-read race.** Concurrent runs over one spec are outside the supported flow by the brief. `/spec-tickets` Phase 4 re-reads the marker. CHECKED.

## Summary
P0: 0 | P1: 0 | P2: 6 | P3: 4 | P4: 1

STATUS: GREEN
