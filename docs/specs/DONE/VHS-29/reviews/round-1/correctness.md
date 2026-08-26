# Correctness Review — round 1

## Closure of round 0 findings

N/A — round 1

## Findings

### F-1: § Scope forbids the very edit § Design mandates (line 204)
**Severity:** P0
**Where:** spec § Scope → "Files to leave alone" (spec.md:24) vs. spec § Design → "What does not change" (spec.md:191)

**Claim:** § Scope, "Files to leave alone":

> Every other phase of `skills/spec-close/SKILL.md` — **Phases 0–4, the coverage model**, the Plane state gate, the archive step, the completion-output block apart from its one `Appended:` line.

§ Design, "What does not change":

> …the **coverage-model note at line 204** … keep their current wording, **except that line 204's parenthetical naming the idempotency guard now points at the script** rather than a bare `grep -F`.

**Why this is wrong:** These cannot both hold. `SKILL.md:204` is the coverage-model note, and it sits inside Phase 3 — both categories § Scope declares off-limits:

```
skills/spec-close/SKILL.md:204
Note: `log.md` is not included in the coverage model. … Phase 5's idempotency guard
(`grep -F "close | <PROJECT> — <TICKET-ID>:"`) prevents duplicates while allowing the
close entry to coexist with wiki-after-merge's merge entry.
```

Compounding it, § Scope's "Files to change" enumerates the edit set as "five wording sites (lines 3, 309, 343, 365, 382); Phase 5 step 4 rewritten…; frontmatter gains a `requires:` block" — line 204 is absent. An implementer working the Scope list (the normal reading order) edits five lines and ships a skill whose Phase 3 still advertises a `grep -F` guard that D4 retired. Done-when #1 and test case 14 both pass in that state, so nothing catches it.

**Suggested fix:** Add line 204 to § Scope's "Files to change" as a sixth site, and amend "Files to leave alone" to read "…Phases 0–4 **except line 204's guard parenthetical**, the coverage model **derivation table and stages**…". Extend done-when #1's enumeration accordingly.

---

### F-2: D4 retires the `grep -F` guard but leaves two SKILL.md sites naming it
**Severity:** P1
**Where:** spec § Decisions D4 (spec.md:73-83); spec § Design "the five sites" (spec.md:172-187)

**Claim:** D4: "Today the guard is a prompt-level `grep -F …` run before a separate write. Moving it into the script makes check-and-insert one operation." § Design then lists exactly five `SKILL.md` sites to touch.

**Why this is wrong:** `grep -F` appears at **four** places in the current file, and D4 invalidates two that the spec never mentions:

- `skills/spec-close/SKILL.md:380` — the Bash tool-use bullet: `` `grep -F` (idempotency check) ``. § Design says this bullet "gains the script invocation," but says nothing about removing the now-false `(idempotency check)` gloss. (It is also line 380, not the "line 382" the spec labels — see F-4.)
- `skills/spec-close/SKILL.md:396` — the failure-mode bullet:

  > **Log-guard encoding.** The `grep -F` idempotency pattern depends on the literal em dash (`—`) in the entry format; tools that normalize it to `--`/`-` will break dedup and produce duplicate entries on re-run.

  After D4 no `grep -F` runs for the log guard. The *hazard* survives (the script's `in` compare is equally em-dash-sensitive, which D6 acknowledges), so this bullet needs rewording, not deletion — but the spec's § Scope "Files to change" list does not include it, and § "Files to leave alone" does not exempt the failure-modes section either way. The spec is simply silent.

Shipping as written leaves the skill body self-contradictory: Phase 5 step 4 invokes a script that owns the guard, while two other sections tell the operator a shell grep performs it.

**Suggested fix:** Add lines 380 and 396 to § Scope's "Files to change" with the intended new text, e.g. line 380 → `grep -F` retained only for duplicate detection (`grep -rlw` / `grep -c`), with `python skills/spec-close/scripts/prepend_log_entry.py` added; line 396 → re-anchor the em-dash hazard onto the script's `--guard` substring compare. Note in § Design that this makes seven edit sites, not five, and reconcile done-when #1's parenthetical list.

---

### F-3: D8's `requires:` block under-declares spec-close's actual capabilities
**Severity:** P1
**Where:** spec § Decisions D8 (spec.md:135-145)

**Claim:**

> The skill now shells out to a script and reads/writes two repos, so the declaration is no longer merely missing paperwork — **it is newly accurate to state**:
> ```yaml
> requires:
>   shell: true
>   filesystem: [read, write]
> ```
> **No `network`, no `subagents`.**

**Why this is wrong:** "No `network`" is false against the file. `skills/spec-close/SKILL.md` makes outbound network calls in three places:

- `:34` — `timeout 30 git fetch origin 2>/dev/null` (Phase 0 origin-sync)
- `:74` — `gh pr view <N> --json files,additions,deletions`, then `gh pr diff <N>`
- `:377` — the tool-use note repeating `gh pr view` / `gh pr diff`

`docs/portability-contract.md:57` defines `network: true` as "makes outbound network requests of its own." The skill also depends on two contract-vocabulary services — Plane (`issue-tracker`) at `:379` and the shared-memory/MCP server (`shared-memory`) at `:378` — both warn-and-proceed per the failure-modes section, i.e. `?`-optional in the contract's terms (`docs/portability-contract.md:65`). The sibling lifecycle skill declares exactly that shape and the contract cites it as the worked reference (`docs/portability-contract.md:138`):

```yaml
# skills/spec-cycle/SKILL.md:5-10
requires:
  shell: true
  filesystem: [read, write]
  network: true
  subagents: true
  services: [issue-tracker?, shared-memory?]
```

This matters beyond paperwork: `docs/portability-contract.md:78` — "A harness MUST verify each **required** capability (no `?`) before any mutation and fail clearly." An undeclared `network` means a sandboxed harness pre-flights clean and then dies at Phase 2's `gh pr diff`, mid-close. The brief pins the portability contract as a decision carried forward (brief.md:103), so the drift is against a load-bearing brief decision, not merely a style preference. `lint.py` will not catch it — it validates vocabulary and syntax only, never under-declaration (verified: `_validate_requires_value`, `lint.py:103-141`), so done-when #5 stays green on a wrong declaration.

`subagents` is correctly omitted — `grep -in "subagent"` over `SKILL.md` returns nothing.

**Suggested fix:** Change D8's block to:
```yaml
requires:
  shell: true
  filesystem: [read, write]
  network: true
  services: [issue-tracker?, shared-memory?]
```
and replace the "No `network`, no `subagents`" sentence with the evidence (`git fetch` at :34, `gh pr view`/`gh pr diff` at :74, Plane + shared-memory at :378-379; `subagents` genuinely unused). Add a test-plan assertion that the declared set matches the tool-use notes, so the declaration cannot silently drift again.

---

### F-4: The mutation-boundary site is line 381, not 382
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Scope (spec.md:13), § Design (spec.md:187), § Done when #1 (spec.md:238)

**Claim:** "**Line 382 (mutation-boundary note).** `Write for the reconciliation report, wiki entries, and log.md` → Write for the reconciliation report and wiki entries…"

**Why this is wrong:** The quoted sentence is at `skills/spec-close/SKILL.md:381`. Line 382 is a different bullet:

```
381: - Write for the reconciliation report, wiki entries, and log.md. Edit for state.md updates (surgical line replacement).
382: - **Mutation boundary:** no file mutation before the Phase 4 confirmation except the reconciliation report … All other writes — wiki entries, state.md, archive moves, log.md — happen in Phase 5, after explicit user approval.
```

Both mention `log.md`, so an implementer editing by line number could touch the wrong one. The spec's own quoted text disambiguates, which keeps this below P1, but done-when #1 enumerates "(lines 3, 309, 343, 365, 382)" as the acceptance list — auditing against that list checks the wrong line. The Plane ticket carries the same off-by-one ("line 382 — mutation-boundary note listing log.md among Write targets"), so this is inherited, not introduced; the spec is the right place to correct it.

**Suggested fix:** Retitle the section "**Line 381 (Write-targets bullet)**" and note that line 382's mutation-boundary sentence keeps `log.md` in its "All other writes" list unchanged. Update the enumerations at spec.md:13 and spec.md:238 to `3, 309, 343, 365, 381`.

---

### F-5: D6 pins encoding on every path except the one `--dry-run` uses
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions D6 (spec.md:107-115); § Test plan case 12 (spec.md:222)

**Claim:** D6: "Three encoding hazards on this specific write, all on Windows, all silent… **These are pinned by tests, not left to the implementation's defaults.**" Test 12: "`--dry-run` prints the merged text and leaves the file byte-identical."

**Why this is wrong:** D6 covers `open(..., encoding="utf-8")`, `sys.stdin.buffer.read().decode("utf-8")`, and `newline=""` on writes. It does not cover `sys.stdout`, which is where `--dry-run` sends the merged text. Measured on this repo's interpreter (`Python 3.14.3`, Windows) with stdout piped — exactly how a `subprocess`-driven test and the Bash tool see it:

```
sys.stdout.encoding = 'cp1252'   sys.stdout.errors = 'surrogateescape'
subprocess.run([sys.executable, '-c', 'print("a—b")']) -> stdout == b'a\x97b\r\n'
```

So `print(merged)` emits **cp1252 bytes with CRLF line endings**, not the UTF-8/LF text the script just computed. A test that asserts `proc.stdout.decode("utf-8") == expected` fails on both axes. (It does not raise — 3.14's `surrogateescape` default and cp1252's own em dash at `\x97` keep it lossless-but-transcoded — so the failure is a confusing byte mismatch, not a clean traceback.) The same applies to any stderr message that echoes the `--guard` literal, which by construction contains an em dash. PEP 686's UTF-8-by-default lands in 3.15, not the pinned 3.14.

**Suggested fix:** Add a fourth bullet to D6: the script reconfigures its output streams (`sys.stdout.reconfigure(encoding="utf-8", newline="")`, same for stderr) before any print, or writes dry-run output via `sys.stdout.buffer.write(merged.encode("utf-8"))`. State in test case 12 which bytes are expected (UTF-8, LF) so the test pins the choice rather than inheriting it.

---

### F-6: Test case 14's allowlist names a survivor that does not exist, and D7's own wording would trip it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan case 14 (spec.md:224); § Design (spec.md:181); D7 table (spec.md:122)

**Claim:** "Grep `SKILL.md` for `append`/`Append` case-insensitively; **the only permitted survivor is prose that describes the *wiki's old* contract being retired.** Asserted as an explicit allowlist…"

**Why this is wrong:** Two problems.

1. No such prose exists. `grep -in "append" skills/spec-close/SKILL.md` returns exactly four hits — lines 3, 309, 343, 365 — all of them sites the spec is changing. The named "permitted survivor" is a category with zero current members, so the allowlist as described is either empty (making the assertion "zero occurrences", which the spec should just say) or an invitation to add an entry post-hoc when the grep fails.

2. § Design (spec.md:181) requires Phase 5 step 4 to state "the three cases of D7" as the script's contract. D7's fresh-wiki row is worded "**Append** after the existing content" and its blank-line rule says "existing content is right-stripped, then `\n\n<entry>\n` is **appended**." An implementer transcribing D7 into `SKILL.md` reintroduces the word the test forbids, and test 14 fails on a correct implementation.

**Suggested fix:** State the allowlist literally (e.g. "expected count: 0") and reword D7's fresh-wiki row and blank-line bullet to avoid `append` — "the entry lands after the existing content" / "the entry is placed at end of file." Add a sentence to § Design telling the implementer to use the non-`append` phrasing when transcribing D7 into Phase 5 step 4.

---

### F-7: Exit code 1 is ambiguous between "skipped" and "the script crashed"
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decisions D5, exit-code table (spec.md:99-103); § Design `main()` walkthrough (spec.md:168)

**Claim:**

| Code | Meaning | `SKILL.md` behavior |
|---|---|---|
| 1 | Skipped — the guard string is already present | Report `log.md: entry already present — skipped` |
| 2 | Usage or I/O error (no `--guard`, empty stdin, guard not in entry, **unreadable path**) | Surface stderr verbatim; do not retry |

**Why this is wrong:** Python exits **1** on any uncaught exception. The exit-2 row enumerates only *read*-side I/O failures ("unreadable path"); the write is the last step in the `main()` walkthrough and no error handling is specified for it. A `PermissionError` or `OSError` on the write therefore exits 1, and `SKILL.md` — following the table — reports `log.md: entry already present — skipped`. The close run then prints a successful-looking completion block while `log.md` was never written, and the re-run path ("Interrupted execute", `SKILL.md:392`) will skip it again on the next attempt for the same reason. This is precisely the "by construction" claim resting on a silent-failure path: D4's atomicity argument ("an interrupted run cannot land a duplicate") holds only if a failed write is distinguishable from a deliberate skip.

**Suggested fix:** Require `main()` to wrap the read *and* write in `try/except OSError` and return 2 with the message on stderr, and add a top-level guard so no exception escapes as a bare 1. Extend the exit-2 row to "…unreadable path, **unwritable path, or any unexpected error**". Add a test case: make the target read-only (or point at a directory), assert exit 2 and that nothing is reported as a skip.

---

### F-8: Blank-line discipline breaks on the two degenerate inputs
**Severity:** P3
**Where:** spec § Decisions D7, "Blank-line discipline" (spec.md:127-133)

**Claim:** "Normal case: the text preceding the anchor is normalized to end with exactly one blank line (`\n\n`)… Fresh-wiki case: existing content is right-stripped, then `\n\n<entry>\n` is appended… Every path leaves the file ending in exactly one `\n`."

**Why this is wrong:** Both rules produce leading blank lines when the "preceding"/"existing" text is empty:

- **Empty existing file** (a `touch`ed `log.md`, which D7 routes to the fresh-wiki branch since `ENTRY_RE` does not match): right-strip yields `""`, so the result is `"\n\n" + entry + "\n"` — the file opens with two blank lines.
- **Headerless file whose first line is the anchor** (an unlikely but reachable state, e.g. a hand-trimmed log): "normalize the preceding text to end with `\n\n`" applied to `""` gives the same two leading newlines.

Neither violates the trailing-`\n` invariant, but both violate the spec's stated "exactly one blank line above" outcome, and test case 10 ("Exactly one blank line above and below the inserted entry… Asserted for all three insertion cases") would fail against a literal implementation of the rule.

**Suggested fix:** Add to the blank-line bullets: "when the preceding/existing text is empty after stripping, no leading separator is emitted — the entry starts at byte 0." Add the empty-file case to test 10.

---

### F-9: D2's property count and its logic both contradict the paragraph above them
**Severity:** P3
**Where:** spec § Decisions D2 (spec.md:51-57)

**Claim:** "Three properties, each load-bearing: … — **Both properties must hold for a false match**, and the fixture in § Test plan pins the exact header text…"

**Why this is wrong:** Three properties are listed (`^` under `re.M`, the `\d{4}-\d{2}-\d{2}` class, the trailing space), then the closing sentence says "both." Worse, the logic is inverted: for a false match to occur, the exclusions would have to *fail*, not "hold." As written the sentence asserts the opposite of what D2 is arguing.

**Suggested fix:** "All three exclusions would have to fail simultaneously for the header's format sentence to match, and the fixture in § Test plan pins the exact header text that breaks the naive form."

---

### F-10: The fixture is described as reproducing a header the spec is simultaneously changing
**Severity:** P3
**Where:** spec § Test plan → Fixtures (spec.md:205); § Design → Wiki-side step (spec.md:195)

**Claim:** Fixtures: "`tests/fixtures/spec-close/log-with-entries.md` reproduces the real header **verbatim** — the `# Wiki Log` title, the `` Append-only record of wiki operations. Format: `## [YYYY-MM-DD] action | description` `` sentence, and the newest-first blockquote."

Wiki-side step: "`vigil-harbor-wiki/log.md`'s header opens `Append-only record of wiki operations.` … Reword to `Running record of wiki operations.`"

**Why this is wrong:** I verified the current header (`vigil-harbor-wiki/log.md:1-8`) matches the fixture description exactly, LF-terminated. But acceptance criterion 6 changes line 3's opening words, so the moment AC6 lands the fixture is no longer "verbatim," and a future reader comparing the two will suspect drift. The load-bearing half — `` Format: `## [YYYY-MM-DD] action | description` `` — is untouched by the reword, so nothing functional is at risk; the spec just doesn't say so.

**Suggested fix:** Add one sentence to § Fixtures: "AC6's reword touches only the sentence's opening words; the `Format:` clause — the part that breaks a naive `index(\"## [\")` — is unchanged, so the fixture stays valid either way. Keep the fixture on the pre-reword text and note it there."

---

### F-11: The wiki-side sibling carries the same stale wording in its step heading
**Severity:** P4
**Where:** spec § Scope → "Files to leave alone" (spec.md:26)

**Claim:** "`wiki-after-merge` and `wiki-state-update` (wiki repo) — both already prepend correctly."

**Why this is wrong:** Behaviorally accurate — `vigil-harbor-wiki/.claude/skills/wiki-after-merge/SKILL.md:39` reads "Otherwise, **prepend** a new entry under format `## [YYYY-MM-DD] <action> | <project> — …`". But its own step heading two lines up says the opposite:

```
:37   4. **Append log.md entry (idempotent).**
:38      - First, `grep -F "<short-sha>" log.md` — if found, skip the append
```

Same wording drift this ticket is fixing, in the file the brief cites as the correct precedent. The brief explicitly puts `wiki-after-merge` out of scope (brief.md:121), so this is not a scope change — just worth a line in § Wiki-side step so the operator can fix it in the same direct-on-master commit as the `log.md` header. Note also that the wiki skills live under `.claude/skills/`, not `skills/`, contra the brief's reference at brief.md:140.

**Suggested fix:** Add to § Wiki-side step: "While on wiki master, `.claude/skills/wiki-after-merge/SKILL.md:37-38`'s 'Append log.md entry' heading is the same stale wording over a correct prepend at :39 — optional to fix in the same commit; not an acceptance criterion."

## Summary
P0: 1 | P1: 2 | P2: 4 | P3: 3 | P4: 1

STATUS: RED P0=1 P1=2 P2=4 P3=3 P4=1
