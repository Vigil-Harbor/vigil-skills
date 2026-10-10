Grounding done: spec re-read fresh from disk (1703 lines); `AGENTS.md` end to end; global + project `CLAUDE.md`; `docs/portability-contract.md` §1–§5; current `skills/review-pr/SKILL.md` (406 lines — anchors `:11`, `:81`, `:83`, `:99`, `:245`, `:277`, `:362`, `:381`, `:397`, `:404` re-verified); all eleven shipped `skills/*/SKILL.md`; wiki `projects/vigil-skills/{state,filemap}.md` and `decisions/` (nothing new since `2026-09-07-vhs-36-…`); the brief; round-1 `correctness.md` / `edge-cases.md` / `conventions.md`.

**Every `Pre` value in the test plan re-measured against the working tree — all 22 match**: row 4 `0`, 5 `7`, 6 `3`, 7 `0`, 8 `0`, 9 `1`/`2`, 10 `0`, 11 `1`, 12 no match, 13 `0`, 14 `0`, 15 `0`/`1`, 17 `0`, 18 `0`, 19 `0`/`0`, 20 `0`/`0`, 21 `0`, 22 `0`. Row 14's new `-A2` form was executed and hand-checked against every fenced block in the spec: the `wc` in the `if` line sits at +3/+4 from the `gh api --paginate` line in the multi-line shape (out of `-A2` range), and no `--jq` program pipes into an alternation member — so the guard neither false-positives nor is unfailable. `<SCRATCH>` blocks were checked against `grep -F '$TMPDIR/'` — `${TMPDIR:-/tmp}/` does not contain the literal, so row 20's guard half holds.

**Fenced-block audit (requested):** a script-extracted scan of all 13 fenced blocks for `r<n>-F-<n>`, `a2r<n>-F-<n>`, `Decision <n>`, `D<n>`, and `v<n> draft` returns **zero hits**. Placeholder style (`<SCRATCH>`, `<SELF>`, `<IDS>`, `<R>`, `<REVIEW_ID>`) matches the file's existing `<N>` / `<OWNER>` / `<VERDICT_ID>` / `{owner}/{repo}` idiom, and the `#` comments explain the rule in plain words exactly as `:64-67` does today. `a2r1-` is used consistently for this attempt's round 1 and never mixed with the bare `r1-` form (which denotes attempt 1); spot-checked citations resolve to the right lens and number.

---

# Conventions Review — round 2

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Decision 2 / D1 state a different advance rule than D6 | CLOSED | spec.md:77-84 now defers "per D6's advance rule and no other"; spec.md:736-741 same in D1, with the `[100 ok, 200 failed, 300 ok] → 100` counter-example; D6 (§ spec.md:1115+) holds the sole statement |
| correctness | F-2 (P1) | findings-free 6f has no Step 2 call site | CLOSED | § Decision 3 spec.md:118-121; D1 spec.md:723-733; D7 spec.md:1201-1209; D9 `:381` spec.md:1338-1345; test row 22 (`post the progress marker` → 2, Pre `0` verified) |
| correctness | F-3 (P2) | Decision 2 carries the pre-digest marker literal | CLOSED | spec.md:57-58 now cites "`review-pr:body-dispositions` marker (Decision 12 gives the full shape)" |
| correctness | F-4 (P2) | row 14 regex cannot match the multi-line shape | CLOSED | row 14 is now `grep -A2 -E …`; executed against the working tree (Pre `0`) and hand-checked against every block shape in the spec |
| correctness | F-5 (P2) | test row attributes body text to the wrong review | CLOSED | now row 25, spec.md:1580-1582 explicitly corrects the attribution to `5135914911` (row 23) |
| correctness | F-6 (P3) | `$TMPDIR` never established | CLOSED | § D1 spec.md:635-654 resolves `<SCRATCH>` once |
| correctness | F-7 (P3) | guard byte-exact vs web-UI CRLF | CLOSED | `gsub("\r"; "")` + `map(select(test("\\S")))` in both queries (spec.md:774, 1229-1230); rule stated at spec.md:485-489 |
| correctness | F-8 (P4) | quoted `gh api --arg` error count wrong | CLOSED | spec.md:754-756 now reads "received 3" |
| edge-cases | F-1 (P1) | `$TMPDIR` never established | CLOSED | § D1 spec.md:635-654; every block uses `<SCRATCH>`; § Decision 7 spec.md:249-251; test row 20 |
| edge-cases | F-2 (P1) | digest interpolates title text into a shell string | CLOSED | § Decision 12 spec.md:388-398 — `h<IDS>` is the literal `[0-9,]` id list; no digest, no `sha1sum`; § Decision 9 spec.md:302-305 keeps the tuple out of any command line |
| edge-cases | F-3 (P1) | 6f unreachable on Step 2 exits | CLOSED | same evidence as correctness F-2 |
| edge-cases | F-4 (P1) | persistently failing body pins the floor | CLOSED | § Decision 12 spec.md:404-421 (retryable vs non-retryable, **unfetchable**, failed-parse defined); § Decision 14 spec.md:590-594; 2b step 3 spec.md:809-812; D8 spec.md:1316; D9 spec.md:1394-1399; test row 29(ii) |
| edge-cases | F-5 (P1) | token protocol covers 2 of ~13 fetches | CLOSED | § Decision 7 spec.md:240-243 ("Every fetch Decision 14 governs … as its own Bash call"); all twelve sites written in shape; test row 17 enumerates all twelve |
| edge-cases | F-6 (P1) | blocks carry spec-side annotations row 26 forbids | CLOSED | § Design preamble spec.md:623-631; verified mechanically — zero citations / `Decision <n>` / `D<n>` in all 13 fenced blocks; rows 19 and 21 |
| edge-cases | F-7 (P2) | guard defeated by `\r` / whitespace-only line | CLOSED | as correctness F-7 |
| edge-cases | F-8 (P2) | fixed-name temp files collide | CLOSED | per-run `<SCRATCH>` keyed on PR number + epoch (spec.md:643), removed at end of run. Residue: second granularity, so two runs launched in the same second on one PR still share a directory — narrow enough that I do not re-raise it |
| edge-cases | F-9 (P2) | `sha1sum` absent on macOS | CLOSED | the digest is gone entirely (§ Decision 12 spec.md:388-398) |
| edge-cases | F-10 (P2) | no rule for a path/line that no longer resolves | CLOSED | § D3 spec.md:1184-1190 (`already-fixed`, reason `file/line no longer present`); D9 spec.md:1375-1378 |
| edge-cases | F-11 (P2) | 64 KB rule reports but does not bound | CLOSED | 2b step 3 spec.md:812-825 — 256 KB ceiling → unfetchable; 64 KB–ceiling → line-numbered search then range reads; 6e size row spec.md:1317 |
| edge-cases | F-12 (P2) | within-round dedup specified two ways | CLOSED | § Decision 9 spec.md:305-307 and 2b step 10 spec.md:1101-1104 now both say "this run — an earlier round, or earlier in this round's own harvest set" |
| edge-cases | F-13 (P2) | row 14 guard blind to the real shape | CLOSED | as correctness F-4 |
| edge-cases | F-14 (P2) | Decision 14 misses two affirmative signals | CLOSED | § Decision 14 spec.md:586-589 names `verdict-landed`, `pre-existing-approval`, `fast-path` |
| edge-cases | F-15 (P3) | resume mark compared as a string | CLOSED | `| .r | tonumber` (spec.md:775) plus the prose at spec.md:781-782 |
| edge-cases | F-16 (P3) | phrase tripwire fires on unfenced blockquote | DEFERRED (accepted) | § Deferred spec.md:1694-1702, with rationale that the narrowing is a design change — see F-4 below for the one procedural gap |
| conventions | F-1 (P1) | same defect as correctness F-1 | CLOSED | as correctness F-1 |
| conventions | F-2 (P2) | `sha1sum` has no repo precedent | CLOSED | removed entirely |
| conventions | F-3 (P2) | `$TMPDIR` hardcoded, no idiom | CLOSED | `<SCRATCH>` resolved once in D1; test row 20 pins both halves |
| conventions | F-4 (P2) | VHS-42 edit routed to `/ship-spec` | CLOSED | § Deferred spec.md:1686-1693 now names an explicit operator step via the plane-proxy work-item update capability, plain text, and states that `/ship-spec` Phase 6 has no description-edit capability |
| conventions | F-5 (P2) | row pinned `≥ 3` naming two sites | CLOSED | now row 17, `≥ 10` with all twelve sites enumerated and the two legitimate merges named |
| conventions | F-6 (P3) | Decision 3 one-armed; 6e missing size row | CLOSED | Decision 3 spec.md:112-114 gains the findings-free clause; D8's 6e block spec.md:1317 gains `Body harvest size` |
| conventions | F-7 (P3) | Decision 2 mis-tagged | CLOSED | spec.md:53 retagged *(carried from brief; the cross-run resume marker and the advance rule are spec-author)* |
| conventions | F-8 (P3) | bare-tool fence omits `:99` | CLOSED | Design preamble spec.md:617-621 now lists `:99` inside D3's region; D3 bullet spec.md:1180-1181 carries "the sub-step's existing wording at `:99` is carried through unchanged" |
| conventions | F-9 (P3) | no spec-only fence for review archaeology | PARTIAL | fenced blocks are fenced and clean, and test row 21 gates the whole file — but the *stated* rule (spec.md:623-631) is scoped to fenced blocks only, while ~66 citations and ~51 `Decision <n>`/`D<n>` refs sit in prose that ships (2b, D3, D9) → **F-1 below** |
| conventions | F-10 (P3) | test-row numbering non-contiguous | CLOSED | rows 3–22 automated, 23–29 manual, document order contiguous; § Test command spec.md:1626 updated to match |

All nine manifest P0/P1 items CLOSED. One P3 (conventions F-9) is PARTIAL and re-raised below at P2 because the round-1 fix moved the same defect from fenced blocks into prose without extending the rule.

## Findings

### F-1: The ship-ready rule is scoped to fenced blocks, but the prose that ships carries ~51 `Decision <n>` / `D<n>` references and ~66 lens citations — a vocabulary no shipped skill uses
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:623-631 (§ Design preamble); § D2 2b steps 1–12 (spec.md:745-1130); § D9 Added bullets (spec.md:1334-1471); § D3 (spec.md:979-1023); test row 21 (spec.md:1556)
**Convention violated:** repo practice — `grep -rncE '\bDecision [0-9]|\bD[0-9]+\b' skills/*/SKILL.md` returns **`0` for all eleven shipped skills**, and `grep -rn 'r[0-9]-F-[0-9]' skills/` returns zero. The file's own idiom cross-references by *step name* ("per the guard in 6c" `:382`, "see the honesty rule in 6e" `:406`, "report count in 6e" `:391`), never by a spec artifact. Also the spec's own preamble rule, applied unevenly across its own edit regions.
**Evidence:** the preamble's headline is *"Fenced blocks are ship-ready text; everything else is spec-internal"* and its rule reads *"…carry no lens citations (`r<n>-F-<n>`), no draft history, and no `Decision <n>` / `D<n>` references — those live in the prose around the block **and stop at the spec**."* Both halves are wrong for this document. (1) "Everything else is spec-internal" is contradicted four lines later by *"Worked specimens (kept in the skill so a future editor can re-verify…)"* (spec.md:1071) and by D2 itself, whose numbered steps **are** the skill's new `### 2b.` section, and by D9's Added bullets, which **are** the skill's new edge-case list. (2) That prose does not stop at the spec: a mechanical count over 2b's region (spec.md:745-1130) gives **36** `Decision <n>`/`D<n>` refs and **30** lens citations; over D9's region (spec.md:1334-1471), **15** and **5**. Concretely, the shipped edge-case bullet at spec.md:1394-1397 reads *"…counted as handled for contiguity, excluded from the floor, not retried (Decision 12)"* — a dangling pointer once it lands in a file that has no Decision 12. The citation half is at least gated (row 21 is whole-file, `[guard] 0`), so a literal implementation **fails its own gate** and the cheapest way to pass is deletion — precisely the dynamic the preamble names for the fenced blocks (spec.md:629-631). The `Decision <n>`/`D<n>` half is gated nowhere, so it ships silently.
**Suggested fix:** two edits. (a) Restate the preamble as a rule about *shipped text* rather than about fences: *"Wherever this Design section states text the skill carries — 2b's steps, D3's triage rules, D9's edge cases, the fenced blocks — that text carries no lens citations (`r<n>-F-<n>`), no draft history, and no `Decision <n>` / `D<n>` references. Cross-reference by the skill's own step names (`2b`, `6f`, `6e`) instead; the Decision-number rationale is spec-internal and stops here."* Drop the "everything else is spec-internal" clause, which the Worked-specimens paragraph already falsifies. (b) Add one guard row to the checklist: `grep -cE '\bDecision [0-9]|\bD[0-9]+\b' $S` → `[guard]` `0`, Pre `0` (measured), so the `D<n>` half is gated the way row 21 gates the citation half.

### F-2: `rm -rf` and `date +%s` enter a shipped skill with no repo precedent, and the cleanup they belong to is unreachable on the run's most common exits
**Severity:** P3
**Where:** spec.md:643 (§ D1 scratch block), spec.md:1327 (§ D8, "6e's last act is `rm -rf \"<SCRATCH>\"`"), spec.md:653 ("6e removes the directory at the end of the run")
**Convention violated:** repo practice — `grep -rn 'rm -rf' skills/` returns **zero** across all eleven skills; the repo's only `rm -rf` is an *operator* instruction in `AGENTS.md:68`, and even there it is paired with a PowerShell equivalent (`Remove-Item -Recurse -Force`) precisely because the repo is harness-neutral (`AGENTS.md:3`, `docs/portability-contract.md` §5). `date +%s` likewise returns zero hits anywhere outside this spec. By contrast the two other new primitives *do* have precedent and are fine as written: `mkdir -p` (`spec-close/SKILL.md:333`) and writing under a temp path (`spec-close/SKILL.md:194`, bare `/tmp/wiki-ready-section.txt`).
**Evidence:** D8 makes an unconditional destructive command the skill's last act, in a file whose only other deletions are `git`-mediated. Separately, the cleanup is stated only for 6e, but D1 creates the directory at the top of **Step 2** and three Step 2 exits (`:81` `APPROVED`, `:83` no-reviews, `:381` nothing-to-review) end the run before 6a, let alone 6e — and `:81` is the modal outcome of a re-run on a healthy PR. So the common path always leaks a directory and the uncommon path is the only one that cleans up. Harm is small (the directory is outside the worktree by design, spec.md:1327), which is why this is P3 and not higher — but the asymmetry reads as an oversight rather than a decision.
**Suggested fix:** (a) state the removal as a capability with the harness-neutral phrasing the repo uses — *"remove the scratch directory (`rm -rf "<SCRATCH>"` in bash; the equivalent in your host)"* — or lean on `:11`'s existing bash-only Shell note explicitly, so the choice is recorded rather than implied; (b) add one clause to D1: *"Every exit path removes `<SCRATCH>`, including Step 2's `:81`, `:83` and `:381` exits — 6e is where the normal run does it."* (c) Optional: note that `date +%s` is the chosen uniqueness token and that second granularity is the accepted bound (this also disposes of the edge-cases F-8 residue).

### F-3: Decision 7's capture-and-token block is written out verbatim twelve times in the shipped file with no stated reason
**Severity:** P3
**Where:** § Decision 7 spec.md:224-243; the twelve sites enumerated in test row 17 (spec.md:1552)
**Convention violated:** reuse-vs-duplicate — the repo ships a `bloat-check` skill whose stated purpose is "duplicated blocks, copy-paste epilogues, provable shrinks", and this change lands twelve copies of `rc=$?` + the `if … HARVEST_FAILURE … COUNT …` line into one file. The spec never says why, so the next reader (or the next `/review-pr` round on this very PR) sees only the duplication.
**Evidence:** the duplication is in fact **forced** and correct — the spec's own D2 step 1 argument establishes it (*"individual Bash tool calls do not share shell variables (`:180`)"*), so a shell function or an `emit_count()` helper defined once would be null in every later call, reproducing exactly the `env.SELF` failure the design already rejected. But that reasoning lives in D2 as an argument about `SELF`, not in Decision 7 as an argument about the block, and Decision 7's requirement (*"as its own Bash call"*, spec.md:240-241) is stated without it. An implementer or a reviewer looking for a shrink will try to factor it, and the design has no recorded answer.
**Suggested fix:** one sentence in Decision 7 after "as its own Bash call": *"The block is repeated verbatim at each site rather than factored into a shell function: shell state does not survive between Bash calls (`:180`), so a helper defined in one call is undefined in the next — the same failure mode `env.SELF` was rejected for. The repetition is deliberate, not copy-paste."*

### F-4: § Deferred's second bullet departs from the section's own filed-a-ticket rule, and from the rule the first bullet follows
**Severity:** P3
**Where:** spec.md:1672-1675 (§ Deferred preamble), spec.md:1694-1702 (phrase-tripwire bullet) vs spec.md:1677-1693 (VHS-42 bullet) and § Decision 11 spec.md:358-362
**Convention violated:** the section's own stated rule — *"Filed as tickets where a future run could hit them; recorded here where the trigger is remote enough that a ticket would only age"* — plus recorded practice (VHS-42 filed with ID + date + state; wiki `decisions/2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md` on claims being checkable).
**Evidence:** the bullet defers edge-cases F-16 as a design change, which is a sound call in itself. What is inconsistent is the *triage*: Decision 11 argues four lines of its own case on the premise that the trigger is immediate — *"Masking matters immediately: this change puts both phrases into `skills/review-pr/SKILL.md` and CodeRabbit quotes changed Markdown back, inside `> [!CAUTION]` callouts"* — and the deferred bullet is the same scenario minus the fence. So the spec simultaneously argues the trigger is day-one (Decision 11) and remote enough not to warrant a ticket (§ Deferred), and the reader cannot tell which the author believes. The first bullet, on a comparably-scoped item, got a ticket.
**Suggested fix:** either file it (a one-line VHS ticket, matching the VHS-42 bullet's shape: ID + date + state), or add the missing half-sentence that resolves the tension — *"Unlike Decision 11's fenced case, CodeRabbit's quoted Markdown is fenced in every observed specimen; the unfenced-prose variant has not been seen, so this is recorded rather than filed."*

### F-5: Test row 14's no-false-positive argument enumerates the jq pipe-followers incompletely
**Severity:** P4
**Where:** spec.md:1549 (test-plan row 14)
**Convention violated:** the spec's own test-plan discipline that each row's rationale is checkable as written
**Evidence:** the row argues *"The `--jq` programs' own pipes are followed by `select`, `{`, `map`, `last`, `capture`, `tonumber`, never by an aggregate, so the row does not false-positive on them."* The actual pipe-followers across the blocks also include `gsub`, `split`, `test`, `.r`, `.id` and `.[]`. The conclusion is still correct — I ran the row against every block shape in the spec and none of `wc|jq|head|tail|sed|cut` follows a `|` — but the enumeration offered as proof is not the enumeration in the file.
**Suggested fix:** replace the list with the property: *"no `|` in any `--jq` program is followed by `wc`, `jq`, `head`, `tail`, `sed`, or `cut`, so the row cannot false-positive on the filters themselves."*

## Summary
P0: 0 | P1: 0 | P2: 1 | P3: 3 | P4: 1

Relevant paths:
- Spec: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.spec.md`
- Brief: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.brief.md`
- Subject: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\skills\review-pr\SKILL.md`
- Conventions checked: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\AGENTS.md`, `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\portability-contract.md`
- Round-1 reports: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.reviews\round-1\`

STATUS: GREEN
