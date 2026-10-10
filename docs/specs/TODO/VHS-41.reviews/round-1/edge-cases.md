# Edge-Cases Review — round 1

## Closure of round <N-1> findings

Round 1 of attempt 2 — no prior round in this run. Verifying the operator-supplied closure manifest (attempt-1 round 4 → attempt-2 round 1) against the current spec:

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | `r0` sentinel makes the 6f guard a constant key | CLOSED | spec:355-362 (marker `r<R>:h<HEX>`), :421-433 (guard reads both parts), :1059 (digest recipe), :1263-1271 (D9 "Two `r0` rounds"), test row 25 (:1338/:1357). Digest is a genuine harvest identity. See new F-2 — the digest's *computation* introduces a defect of its own |
| edge-cases | F-1 | `; rc=$?` makes a failed fetch indistinguishable from a small one | PARTIAL | Token protocol present and correct at spec:215-219, :586-590, :913-915, D9 bullet :1237-1240, test row 24. But it is applied to **2 of the ~13 fetches Decision 14 says it governs** — see new F-5 |
| edge-cases | F-2 | `export SELF` → `env.SELF` resolves to `null` | CLOSED (with a gate conflict) | Literal `"<SELF>"` at spec:651 and :1042; Decision 14 bullet :519-521; rows 13/26. Verified: `gh api user --jq .login` → `ziomancer`, and the literal-substituted author filter runs clean against `issues/<N>/comments`. The *rationale comments* the fix shipped now collide with row 26 — new F-6 |
| edge-cases | F-3 | `r0` constant key suppresses a later round's disposition list | CLOSED | Same digest change; plus 6e now names this round's comment or `dispositions not posted — <guard-skipped\|post failed>` (spec:1149, :1160-1163) |
| edge-cases | F-4 | D6's advance rule states two incompatible values | CLOSED | spec:967-975 — one contiguous-prefix rule, worked example `[100 ok, 200 failed, 300 ok] → 100`, plus the D5 cached-parse/dedup absorption note |
| edge-cases | F-8 (known open) | CRLF / whitespace defeats the exact-match guard | REOPENED as F-7 | Still `. != ""` + `==` at spec:652 and :1039-1042 |
| edge-cases | F-10 (known open) | Row 14 cannot see the multi-line antipattern | REOPENED as F-13 | Row 14 unchanged at spec:1335 |
| edge-cases | F-12 (known open) | `$TMPDIR` never established | REOPENED as F-1, **re-ranked P3 → P1** | Now load-bearing: verified below that it aborts the fetch and trips Decision 14 |
| edge-cases | F-9 (known open) | Decision 14 misses fast-path / pre-existing-approval | REOPENED as F-14 | Decision 14 :536-542 still enumerates only the three Step 2 exits |
| edge-cases | F-5 (known open) | Phrase tripwire false alarm on the shipping PR | PARTIAL → F-16 | Masking added (spec:755-759), but a blockquoted *unfenced* mention still leaks |

## Findings

### F-1: `$TMPDIR` is used by every capture-and-count block but never established — verified to abort the fetch outright
**Severity:** P1
**Where:** spec:216-219 (Decision 7 canonical block), :588-590 (D1 fetch (c)), :679 (2b step 3), :913-915 (D5 inline poll); the claim it is established is at :679 ("the temp/scratch directory D7 establishes") but D7 (:1071-1076) establishes no variable — it only says "system temp directory (or the harness scratch directory)".
**Edge case:** `TMPDIR` unset — the default on most Linux distributions and container CI images, and not guaranteed by POSIX.
**What happens:** the redirection, not the fetch, fails. Verified in this environment:

```
$ env -u TMPDIR bash -c 'gh --version > "$TMPDIR/new_inline"; rc=$?; ...'
bash: line 1: /new_inline: Permission denied
HARVEST_FAILURE rc=1
```

`gh` never runs. The block emits a well-formed `HARVEST_FAILURE rc=1`, so Decision 14 (:528-542) fires: `REVIEW_SIGNAL` can never be `verdict-landed`, and `:81`, `:83` and `:381` are all blocked from reporting a clean result. Every run on such a machine ends `inconclusive` and tells the operator to re-run, forever, with an error code that points at GitHub rather than at an unset variable. Where `/` *is* writable (root in a container) it silently writes count files to the filesystem root instead.
**Why the spec misses it:** round 4 ranked this P3 when `$TMPDIR` was cosmetic. The stdout-token protocol added this round made the redirect the first thing that can fail, and Decision 14 turned any such failure into a run-wide gate — so an undefined variable is now a total functional failure, not a tidy-up.
**Suggested fix:** in D7, replace "system temp directory (or the harness scratch directory)" with an explicit establishment line the other blocks reference, e.g. `TMPDIR_RUN="${TMPDIR:-/tmp}/review-pr-<N>-$$"; mkdir -p "$TMPDIR_RUN"`, and note it is conversational state substituted literally (the `:180` pattern) since Bash calls do not share variables — the same discipline `<SELF>` now gets. Add a grep row pinning that no block references a bare `$TMPDIR`.

### F-2: The harvest digest interpolates CodeRabbit-supplied title text into a single-quoted shell string — quoting break and command execution
**Severity:** P1
**Where:** spec:1059 (`printf '%s' '<id>,<id>,…|<key>,<key>,…' | sha1sum | cut -c1-8`), with the key definition at :269-283 (Decision 9) and the digest input definition at :355-362.
**Edge case:** a body item with **no `cr-comment` marker** — Decision 9's fallback key is the tuple `(path, line-range, title)`, and D9's edge-case list (:1197-1199) confirms this path is expected. The title is untrusted reviewer text derived from the PR diff.
**What happens:** an apostrophe closes the shell literal. Verified:

```
$ printf '%s' '100,200|(src/a.py, 12-30, Don't use $(id) here)' | sha1sum | cut -c1-8
bash: syntax error near unexpected token `)'
```

and the escape is exploitable, not merely fatal — a title containing `Avoid '$(echo PWNED)' here` produced:

```
$ printf '%s' '100|(a.py, 1-2, Avoid '$(echo PWNED)' here)'
100|(a.py, 1-2, Avoid PWNED here)
```

The command substitution ran. That is arbitrary command execution from review text, in the one place the spec hands untrusted content to the shell instead of to a file. The benign outcome (syntax error) is also bad: the digest is unavailable, so 6f cannot compute its marker and the round posts nothing or posts an improvised key.
**Why the spec misses it:** Decision 10 and Decision 12 both establish that harvested text is untrusted, but the neutralization rule (:449-453, :1066-1069) is scoped to *the marker literal inside the 6f comment body*. The digest was added this round and inherited no such rule. `--body-file` protects the comment; nothing protects the digest.
**Suggested fix:** never put key text on a command line. Write the canonical string to a file with the same mechanism `<BODY_FILE>` uses and digest the file: `sha1sum < "$TMPDIR_RUN/digest_input"`. Additionally define the tuple key's **serialization** (it is currently undefined — `(path, line-range, title)` with no stated separator or escaping, so two runs can serialize the same finding differently and produce different digests, defeating the re-run suppression the digest exists for). Recommend hashing the tuple's parts joined by a character that cannot occur in a path or title (e.g. `\x1f`), or keying the fallback on `sha1(path|lines|title)` so only hex ever reaches the canonical string.

### F-3: 6f is unreachable on the three Step 2 exits, so a bounded first run on a mature PR posts no marker and re-harvests the same 10 reviews forever
**Severity:** P1
**Where:** post condition spec:1014-1019 (D7) vs. the enumerated invocation sites at :110-113 (Decision 3 *Honored by*) and :1046-1054 (D7's "two edits make it reachable on every path"); the exits are `:81` (D1, spec:616-622), `:83` (same), and `:381` (D9, spec:1166-1170).
**Edge case:** first run on a long-lived PR with more than 10 body-carrying reviews whose parsed prefix yields **zero** findings, no unresolved inline threads, and an `APPROVED` (or no-new-comment) state.
**What happens:** 2b step 2 parses the 10 oldest, defers the rest, and sets `HARVEST_FLOOR` (:666-676). Control returns to Step 2, and `:81` fires — D1 explicitly permits it: "the finding condition is on *findings*, not on harvest-set size — a mature PR whose historical bodies parse to zero items still short-circuits" (:619-621). The run exits before Step 3, before `:245`, before any 6b branch, i.e. before every one of the four sites that invoke 6f. No comment, no marker, `PRIOR_MARK` stays `0`. The next run recomputes the identical harvest set and does the same thing. **The deferred reviews are permanently unharvestable** — which is verbatim the failure Decision 12's "Progress does not depend on findings" rule (:409-415) and correctness r3-F-3 declared closed. `:381`'s rewrite has the same shape: it exits on "no inline comments *and* no body-level items after a completed harvest", and a bounded harvest counts as completed.
**Why the spec misses it:** D7's post condition is stated as a *predicate* ("when `R` would advance past `PRIOR_MARK` and a `HARVEST_FLOOR` exists"), while reachability is stated as a *list of call sites* that was written before the findings-free form existed. The two were never reconciled; nothing in D1 or D9 mentions 6f.
**Suggested fix:** in D1, make both `:81` and `:83` conditional on "6f has posted this round's marker if D7's post condition holds", and add the same clause to D9's `:381` rewrite; list all three as 6f invocation sites in Decision 3's *Honored by* and in D7's reachability paragraph. Add a test row asserting the skill names 6f on the `:81`/`:381` paths.

### F-4: A persistently failing review body sets a floor with no escape, permanently blinding the skill to every newer body finding on that PR — and "failed parse" is undefined
**Severity:** P1
**Where:** `HARVEST_FLOOR` definition spec:369-371, the `R` rule :376-382, the invariant :384-387, D6's advance rule :967-975, Decision 14 :528-531.
**Edge case:** one review whose per-review body fetch (2b step 3) fails *every* time — a deleted or hidden review, a 403/451 on a review from a fork, a repo transfer, or simply a review whose parse the agent judges failed.
**What happens:** within the run, `LAST_BODY_REVIEW_ID` may not advance past it (D6), so 6b never reaches newer reviews. Across runs, `HANDLED_THROUGH` can never exceed it, so `R` stays at the last good id below the failure — or `0` if the failure is the oldest — and every future run recomputes the same harvest set, hits the same failure, computes the same digest, and is **suppressed by its own guard** (:1263-1271 explicitly blesses this: "a re-run that reproduces the identical harvest … is suppressed"). Meanwhile Decision 14 forces `inconclusive` and blocks `:81`/`:83`/`:381` on every run. Net effect: `/review-pr` can never again report a clean result on that PR, and every body-level finding in every newer review is invisible — the exact blindness this ticket exists to remove, now permanent and silent apart from one report line. Decision 14's stated remedy ("degrades to `inconclusive`, re-run") is the same hollow remedy Decision 12 called out for the v1 draft; it does not converge here.
**Why the spec misses it:** Decision 12 reasons entirely about *transient* failures ("so a re-run can reach them"). It never asks what happens when the retry does not help, and the digest suppression added this round converts a repeating failure from noisy into silent.
**Suggested fix:** bound the floor. Add a rule: after N consecutive runs (or a stated retry count within a run) in which the same review id fails to fetch or parse, record it as **unfetchable**, exclude it from the floor computation, and report it as a standing line in 6e (`body harvest: review <id> unfetchable after <n> attempts — excluded from the resume floor`). Persisting that across runs needs a place to record it — the natural one is the 6f marker comment, which is already the design's durable store. Separately, **define "a failed parse"**: Decision 12 makes it a floor-setting event, but 2b's tripwires (Decision 11, :340-342) explicitly "continue with whatever parsed", so no stated condition in 2b ever produces a failed parse. As written the floor predicate is undecidable.

### F-5: The observable-outcome protocol covers 2 of the ~13 fetches Decision 14 says it governs; the harvest fetch itself can still return a silent partial
**Severity:** P1
**Where:** Decision 14 bullet 1 (spec:502-512) enumerates the governed fetches — `(a)`, `(b)`, `(c)`, `(a2)`, the 2b resume query, each per-review body fetch, D5's three polls, D6's and D8's conversions, D7's guard. Decision 7 (:231) says the block shape "is used at D1 fetch (c) and D5's inline poll" — and only those two carry it (:588-590, :913-915).
**Edge case:** a `--paginate` stream on fetch **(a)** or **(b)** that dies on page 3 of 5.
**What happens:** Decision 7's own argument (:206-213, :221-231) is that a partial page set "looks well-formed", so the outcome must be *printed* to be observable. Fetches (a) and (b) print their records straight to stdout with no token, no capture and no status check. When the pages an agent already received look like a valid record stream, nothing in the prescribed procedure distinguishes "5 pages" from "3 pages then an error". Fetch (b) is the **body-harvest set itself**: a truncated (b) silently shrinks the harvest, the missing reviews are treated as non-existent rather than deferred, no floor is set, and `R` advances past them — re-creating precisely the "permanently unharvestable" defect Decision 12's invariant exists to prevent, this time with no failure recorded anywhere. D1 compounds it by presenting (a), (a2), (b) and (c) in one fenced block: run as one Bash call, only (c)'s status survives.
**Why the spec misses it:** Decision 14 was written as a *policy* ("any non-zero exit … is recorded"), Decision 7 as a *mechanism* for two named sites. Nothing states how the policy is discharged for the other eleven, and Decision 14 bullet 4 (:522-527) even says "Decision 7's file-capture shape is what makes that exit status observable" — which is true only where the shape is applied.
**Suggested fix:** state a single rule: **every** governed fetch is issued in its own Bash call ending with the token block, and where the records themselves are needed the block prints `COUNT=<n>` after the file, with the file then read. At minimum apply the capture-and-token shape to (a), (b), the 2b resume query, and the per-review body fetch, and raise test row 24's expectation from `≥ 3` to a number that pins them. Also split D1's single fenced block into per-fetch blocks so the "one Bash invocation" rule is visible at the call site.

### F-6: The prescribed command blocks carry spec-side annotations — including `env.SELF`, `export SELF` and review-finding IDs — that gate row 26 forbids in the shipped file
**Severity:** P1
**Where:** spec:638-654 (D2 step 1 block) and :1021-1045 (D7 guard block) vs. test row 26 (:1337 command, :1358 expectation).
**Edge case:** an implementer follows the spec literally and copies the fenced blocks, comments included — which every other block in the design intends (D1's `# (a) VERDICT determination…` comments mirror the existing `:64-67` style, and row 8's rationale counts "three prose mentions" as shipped text).
**What happens:** the shipped `SKILL.md` then contains `env.SELF` twice and `export SELF` once, and row 26 (`grep -cF 'env.SELF' $S ; grep -cF 'export SELF' $S`, expected `0`, `0`) fails on a **correct** implementation. This is the failure mode correctness r3-F-2 named: the cheapest way to pass the gate is to delete the very rationale that keeps a future editor from reintroducing the bug. Worse, those same blocks embed `(correctness r3-F-1 …)` and `(edge-cases r4-F-2)` — internal review-round citations — which would ship into a public repo's skill file and mean nothing to any reader.
**Why the spec misses it:** the blocks accreted their rationale as round-over-round rebuttals, and nothing in the spec distinguishes "text to place in the skill" from "note to the implementer". Row 26 was written assuming the former, the blocks were written as the latter.
**Suggested fix:** either (a) mark annotation lines explicitly — e.g. a `# [spec note, do not ship]` convention, with a gate row asserting none appear in `$S` — or (b) rewrite the two blocks' comments in ship-ready form ("resolve the login once and substitute it literally; individual Bash calls do not share shell variables") and move the round citations into the surrounding prose. Then re-verify row 26 against the rewritten text, and add a row asserting `grep -cE 'r[0-9]-F-[0-9]' $S` is `0`.

### F-7: The idempotency guard's exact match is defeated by a `\r` or whitespace-only trailing line
**Severity:** P1 → reported as P2 (see below)
**Severity:** P2
**Where:** spec:652 (resume, `split("\n") | map(select(. != "")) | last`) and :1039-1042 (guard, the same expression compared with `==` against the literal marker).
**Edge case:** the posted comment body ends `…-->\r\n`, or carries a trailing whitespace-only line.
**What happens:** `. != ""` treats `"\r"` and `"   "` as non-blank, so `last` returns `"<!-- … -->\r"` or a blank-looking line, and the `==` comparison never matches. The guard silently matches nothing — the identical failure mode `env.SELF` was rejected for last round — and every re-run posts another duplicate disposition comment. The resume `capture` still matches (unanchored, verified), so the two halves disagree about the same comment. Measured on live data: CodeRabbit and API-posted comments on this repo come back LF-only (`.body|split("\r")|length-1` is `0` on PR #27 and #28), so this is not the default path — but `<BODY_FILE>` is written on Windows here, where the file-writing path can emit CRLF, and any comment a human edits in the GitHub web UI comes back CRLF.
**Why the spec misses it:** "last non-blank line" was specified as prose and then encoded as `. != ""`, which is a different predicate.
**Suggested fix:** normalize before comparing in both queries: `(.body // "") | gsub("\r"; "") | split("\n") | map(select(test("\\S"))) | last // ""`, and say in Decision 12 that the marker comparison is on the trimmed line.

### F-8: Fixed-name temp files collide under the concurrency the spec explicitly tolerates
**Severity:** P2
**Where:** spec:588 (`$TMPDIR/inline_findings`), :913 (`$TMPDIR/new_inline`), :679 (`$TMPDIR/body-<REVIEW_ID>.md`); concurrency tolerated at :455-457 and D9 :1272-1274.
**Edge case:** two `/review-pr` runs at once (the spec's own tolerated case), or one run polling 6a while another agent writes.
**What happens:** both runs write `$TMPDIR/new_inline`. A `wc -l` taken while the other process is mid-write returns a partial count with exit 0 — a silently wrong finding count, which with a landed verdict yields `verdict-landed` and licenses "no new findings". That is the PR #51 false negative the whole capture-and-count mechanism exists to prevent, arriving through the mechanism. The spec's tolerance statement covers only duplicate comments, which are "recognizable"; a wrong count is not.
**Suggested fix:** scope the filenames to the run — `"$TMPDIR_RUN/new_inline"` where `TMPDIR_RUN` includes the PR number and a per-run token (see F-1's fix), and state that the directory is removed at the end of the run.

### F-9: `sha1sum` is not available on macOS, so the digest step fails on a common host for a public skill
**Severity:** P2
**Where:** spec:1059.
**Edge case:** the skill runs on macOS (or any BSD userland), where coreutils' `sha1sum` is absent and the equivalent is `shasum` / `openssl dgst -sha1`. Verified present here (Git Bash `/usr/bin/sha1sum`), and there is **no precedent** in the repo — `grep -rn 'sha1sum\|shasum\|md5sum' skills/` returns nothing.
**What happens:** `command not found`, the digest is empty, and the guard is keyed on `r<R>:h` with a blank hex — an exact-match string no comment carries, so the guard is inert and every round posts. Loud in the transcript, silent in effect.
**Why the spec misses it:** the digest was introduced this round as a shell one-liner; `sha1sum` was not checked against the portability contract, and `skills/review-pr/SKILL.md` declares no `requires:` block (brief Q6, out of scope) so nothing else flags the new dependency.
**Suggested fix:** state the fallback in D7 — `sha1sum || shasum -a 1` — or, better, drop the external binary: any stable 8-char function of the canonical string works (the spec only needs determinism within and across runs), and the harvest ids alone plus a count would do. Whatever is chosen, name it in the Out-of-scope note about review-pr's undeclared surface (:585-589).

### F-10: No rule for a body item whose path or line no longer exists — now the common case, because the harvest reaches back over the PR's whole body history
**Severity:** P2
**Where:** D3's per-finding loop (spec:865-869 / tail of the file): "read the file at the referenced line", "verify against current code", using "path and line range from the file group and item header".
**Edge case:** a first run on a mature PR harvests review bodies from weeks ago (Decision 2, 2b step 2). The file was renamed, deleted, or shortened since; or the item's `lines` field is the non-numeric form 2b step 9 deliberately records verbatim (`L12-L20`, a file-scoped range).
**What happens:** step 2 of the triage loop has nothing to read. The spec assigns no category for it, so the agent improvises per item — and the improvised disposition is what lands in the 6f comment and in the digest's key list, which needs to be deterministic across runs (F-2).
**Why the spec misses it:** for inline findings this is rare (a comment's thread is anchored to a live diff) and pre-existing. Widening the finding source to the PR's whole body history changes the frequency by an order of magnitude, and the spec inherits the gap without noticing it moved.
**Suggested fix:** add a named triage outcome in D3 — "path or line range no longer resolves → categorize `already-fixed` with reason `file/line no longer present`" — and add it to D9's edge-case list next to "Body item's line range points outside the PR diff".

### F-11: The 64 KB rule reports but does not bound, and the "read it in slices" procedure is undefined
**Severity:** P2
**Where:** spec:678-689 (2b step 3), against Decision 6's claim (:174-179) that the three bounds exist so "a pathological input degrades loudly and visibly instead of exhausting the round mid-triage".
**Edge case:** a review body of several megabytes (a full-repo review, a walkthrough with dozens of nitpick groups).
**What happens:** the review-count bound (10) and the item bound (20/50) are real caps; the size rule is only a *report*. A 5 MB body is still parsed in full, "in slices", and the round's context is exhausted mid-triage — the exact outcome the bound was written to prevent. And "reading it in slices" is not a procedure: 2b's section location (step 5) requires scanning to find the summary lines, and nothing says how to locate them without reading the file.
**Suggested fix:** make the size rule a bound with a stated ceiling, and state the slicing mechanism: locate candidate section lines with a line-numbered search over the file (which is a search, not a trim, and so consistent with Decision 5), then read only those line ranges. Above the ceiling, defer the review and set `HARVEST_FLOOR` so it is reported and retried rather than half-parsed.

### F-12: Within-round dedup is specified two different ways
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** Decision 9 (spec:281-283) "deduplicated on this key across all rounds of one run" vs. 2b step 10 (:799-801) "drop any whose key was already triaged in an **earlier round** of this run".
**Edge case:** a first run whose single Step 2 harvest set contains ten historical review bodies restating the same nitpick.
**What happens:** under step 10's wording nothing is deduped within the round — ten triage passes, ten lines in the 6f comment, and ten copies of one key in the digest's canonical string (which the spec says is "sorted and joined", not deduplicated). Under Decision 9's wording, one.
**Suggested fix:** align step 10 to Decision 9 — "already triaged in this run, including earlier in this round's harvest set" — and state that the digest's key list is deduplicated before sorting.

### F-13: Test row 14's guard cannot see the antipattern in the only shape this file writes
**Severity:** P2 (re-raise of attempt-1 edge-cases F-10, unfixed)
**Where:** spec:1335 (`grep -cE 'gh api --paginate.*\| *(wc|jq)' $S`), row expectation at :1345.
**Edge case:** the realistic wrong implementation, which is the file's own house style: `gh api --paginate repos/… \` on one line, `--jq '…' | wc -l` on the next.
**What happens:** `grep -E` is line-oriented, so the guard matches nothing whether or not the antipattern is present — the same class of un-failable guard correctness r3-F-8 caught in the `[^\n]` form. The row's own rationale calls this "Decision 7's most load-bearing rule", and it is unguarded. A secondary risk in the other direction: D9's edge-case prose is *supposed* to name the antipattern, and one natural phrasing (`gh api --paginate … | wc -l`, as Decision 7 itself writes it at :208) would trip the guard as a false positive.
**Suggested fix:** make the row multi-line — `grep -Pzo` is not portable, so use `python - <<'EOF'` reading the file and joining backslash continuations, or `grep -A1 -E 'gh api --paginate' $S | grep -cE '\| *(wc|jq)'`. Whatever the form, pin it with a demonstration that it *fails* on a two-line specimen, and exempt fenced prose that names the antipattern.

### F-14: Decision 14 blocks three affirmative exits and misses two more
**Severity:** P2 (re-raise of attempt-1 edge-cases F-9, unfixed)
**Where:** Decision 14 :536-542 ("All **three** Step 2 exits are covered"), vs. `REVIEW_SIGNAL=pre-existing-approval` (`:182`, D5's conversion at spec:895-902) and `REVIEW_SIGNAL=fast-path` (`:166`).
**Edge case:** Step 2's harvest fails, the round pushes a fix, and 6a finds a post-push `APPROVED`.
**What happens:** `pre-existing-approval` jumps straight to 6e and reports an affirmative "CodeRabbit approved" with a standing harvest failure. 6e does print `Body harvest failures: H` on its own line (D8), so it is not fully silent — but `Review completion signal: pre-existing-approval` is a confident line, and the honesty rule at `:370-377` is scoped to `inconclusive`. Same for `fast-path`, which by construction runs on a round that harvested.
**Suggested fix:** generalize the clause — "while any harvest failure stands, no affirmative `REVIEW_SIGNAL` (`verdict-landed`, `pre-existing-approval`, `fast-path`) may be reported without the failure named on the same line; the completion signal degrades to `inconclusive`" — and state which exits that covers rather than counting them.

### F-15: The resume mark is compared as a jq string, not a number
**Severity:** P3
**Where:** spec:653 (`capture(...) | .r`) and :655 ("Take the numerically highest value").
**Edge case:** markers `r9` and `r5135914911` on one PR (rare, but review ids of different lengths across a repo's history are not).
**What happens:** `capture` yields a **string**; if the agent compares lexically, `"9" > "5135914911"`, and the resume window closes at the wrong place — silently, since neither tripwire runs on the resume path (:439-441). The prose says "numerically", so a careful agent is fine; the query hands it the wrong type.
**Suggested fix:** append `| tonumber` to the resume filter.

### F-16: The phrase tripwire still fires on an unfenced quotation of the phrase inside a blockquote
**Severity:** P3 (residue of attempt-1 edge-cases F-5)
**Where:** spec:319-337 (Decision 11 phrase tripwire), :755-759 (2b step 6's phrase-scan view).
**Edge case:** CodeRabbit reviews the PR that ships this change and mentions "outside diff range comments" in a finding's **prose** inside a `> [!CAUTION]` callout — not inside a fence — while its own Outside-diff section is absent.
**What happens:** the phrase-scan view strips the `>` markers per line (making the phrase *more* visible) and masks only fences and inline-code spans, so an unfenced blockquoted mention survives and the tripwire fires. Decision 11's own justification assumes the quoted markdown is fenced inside the callout; when it is not, the detector is noise from day one — which is what test row 19 exists to prevent for a neighbouring case.
**Suggested fix:** narrow the trigger to structural context: fire only when the phrase appears on a line containing `<summary>` (i.e. a section header that failed to match the full pattern), which is the only shape the drift the detector targets can take. That also removes the need for the phrase-scan view to be body-wide.

## Summary
P0: 0 | P1: 6 | P2: 8 | P3: 2

Key files:
- Spec: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.spec.md`
- Brief: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.brief.md`
- Subject: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\skills\review-pr\SKILL.md` (406 lines, all cited anchors verified against `main`)
- Prior reviews: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.attempt-1\reviews\round-4\`

Verified empirically (gh 2.87.3, Git Bash): `--slurp` is rejected with `--jq`; `gh api --jq` emits one compact JSON object per line (so `wc -l` is a valid record count); `capture("…r(?<r>[0-9]+)")` works in gojq and emits an empty stream on non-match; the literal-`"<SELF>"` author-filtered comment query runs clean; `sha1sum` exists here but has no precedent in `skills/`; unset `TMPDIR` aborts the canonical block before the fetch; and an apostrophe or `'$(…)'` in a harvested title breaks out of the digest command's quoting.

STATUS: RED P0=0 P1=6 P2=8 P3=2
