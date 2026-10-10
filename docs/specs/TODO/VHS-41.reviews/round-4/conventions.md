# Conventions Review — round 4

## Closure of round 3 findings

| Lens | ID | Sev | Title | Status | Evidence |
|---|---|---|---|---|---|
| correctness | F-1 | P0 | Shipped strings say unfetchable is "excluded from the resume mark" | CLOSED | spec.md:1470 `Review <id> unfetchable (<code>) — counted as handled; not retried`; spec.md:1540 `not retried, counted as handled so the resume mark passes them` |
| correctness | F-2 | P1 | Decision 14 classifies `403` non-retryable | CLOSED | spec.md:679-680 `(Decision 12: a non-retryable 404/410/451 — 403 is retryable and floors)`; D9 bullet spec.md:1626-1628 agrees |
| correctness | F-3 | P1 | 2b step 2 sources rounds 2+ from the stale Step-2 fetch (b) | CLOSED | spec.md:924-931 makes the source per-invocation and names 6a's body-carrying poll |
| correctness | F-4 | P2 | Two two-arm restatements of 6f's post condition | CLOSED | Decision 3 spec.md:113-116 now "a bound, a failure, or an unfetchable review"; D1 spec.md:853-857 carries the three-armed gloss |
| correctness | F-5 | P2 | `HANDLED_THROUGH` circular ("in a posted comment") | CLOSED | spec.md:483-488 "…or in the comment this round is about to post — `R` is computed before the post" |
| correctness | F-6 | P3 | D7 asserted the superseded cleanup rule | CLOSED | spec.md:1455 "The directory is removed on every exit path (D1)." |
| edge-cases | F-1 | P1 | `test("\\S")` reaches gh as `\S` | CLOSED | `[^[:space:]]` at spec.md:909 and :1417; rationale spec.md:566-572; row 19 pins the `\\S` form out (spec.md:1763, :1787) |
| edge-cases | F-2 | P1 | Failed body fetch leaves error JSON that re-parses as zero items | CLOSED | spec.md:955 `rm -f` on non-zero exit; spec.md:960-966; step 4 spec.md:1003-1008 |
| edge-cases | F-3 | P2 | Session-condition rule evaluated where the information doesn't exist | CLOSED | 2b step 3 spec.md:968-980 makes classification provisional until the pass ends; Decision 12 spec.md:463-473 states the 404-masks-permission rationale and the single-member carve-out |
| edge-cases | F-4 | P2 | `new_body_items` counts bound-deferred backlog | **PARTIAL** | gate landed (spec.md:1282-1294, `submitted_at > PUSH_TIME`) and spec.md:938-942 fixes the same-harvest-set sentence — but the promised 6e backlog count is absent from D8's report block (F-3 below), and Decisions 2/4 were not reconciled with the gate (F-2 below) |
| edge-cases | F-5 | P2 | Partial-`--paginate` assumption never measured | CLOSED | spec.md:243-248 records the caveat and the "second detector" condition; test row 29(iv) spec.md:1856-1863 |
| edge-cases | F-6 | P2 | `<SCRATCH>` recovery adopts a concurrent run's directory | CLOSED | spec.md:773-782 refuses on ≠1 candidate; Decision 12 *Race* spec.md:596-598 |
| edge-cases | F-7 | P3 | `POSTED=` / `POST_FAILURE` unpinned | CLOSED | row 17 second command spec.md:1761, expected `1` (spec.md:1785) |
| edge-cases | F-8 | P3 | Row 20's `$TMPDIR/` guard unshippable | CLOSED | row 20 now `grep -cF '"$TMPDIR/'` (spec.md:1764); D1's caution uses backticked `` `$TMPDIR/…` `` (spec.md:749-753) — measured `0` on `main` and on the caution text |
| edge-cases | F-9 | P4 | Two factual slips in D1's rationale | CLOSED | spec.md:747-749 `mkdir: … File exists` diagnostic; spec.md:753 `/new-inline` |
| conventions | F-1 | P2 | Shipped-text rule omitted D7/D1/D8 | CLOSED | spec.md:715-721 now "every Design subsection that states text the skill carries — …D7's 6f section, D1's scratch-directory protocol, D8's 6e report lines…" |
| conventions | F-2 | P2 | Multi-hit override re-opens permanent blindness; D9's shipped bullet omits it | **PARTIAL** | Decision 12 scoped correctly (spec.md:463-473) — but D9's shipped bullet (spec.md:1620-1628) still states the unconditional form; see F-1 below |
| conventions | F-3 | P2 | Monotone-`R` rule vs. worked example | CLOSED | spec.md:494-499 "never decreases … re-posts the run's current `R`"; example spec.md:523 `r200:h300,400` now the named canonical form |
| conventions | F-4 | P3 | Post condition stated in three places, earliest missing an arm | CLOSED | Decision 2 spec.md:95-100 collapsed to a pointer |
| conventions | F-5 | P3 | `POSTED=`/`POST_FAILURE` ungated; Decision 7 missing the error-text field | CLOSED | spec.md:267-271; row 17 |
| conventions | F-6 | P4 | stderr-capture precedent not recorded | CLOSED | spec.md:248-251 |
| conventions | F-7 | P4 | D7 "mirrors 6c's" on the one rule it contradicts | CLOSED | spec.md:1493-1496 "follows 6c's log-and-continue discipline … with one deliberate difference" |

All round-3 P0/P1 items are CLOSED. Two P2s are PARTIAL and are re-stated below at their original severity.

## Findings

### F-1: D9's shipped unfetchable bullet still states the unconditional rule that 2b step 3 — also shipped — now qualifies
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D9 (spec.md:1620-1628) vs § 2b step 3 (spec.md:968-980) and § Decision 12 (spec.md:463-473)
**Convention violated:** the spec's own single-source discipline for load-bearing rules ("D6 holds the only statement of that rule", spec.md:82-83; "the single shared rule of D3 … not a second, body-only rule", spec.md:1121-1123), applied here to two regions that *both* ship into `skills/review-pr/SKILL.md`.
**Evidence:** this is the shipped half of my round-3 F-2, which the manifest reports folded. The spec half landed correctly — Decision 12 now reads *"if **every** attempted review in a set of two or more failed with the same non-retryable status, that is a session condition even when the status is `404` … so floor them all rather than writing them off"* — and 2b step 3 carries it (spec.md:973-979). But `grep -n 'session condition' VHS-41.spec.md` returns `453, 463, 975, 1627`, and `:1627` is the *`403`* sentence, not this rule. D9's bullet still reads, unconditionally: *"**A per-review body fetch returns a non-retryable status (404/410/451)** — the review is deleted, gone, or legally withheld, and no re-run will change that. It is recorded **unfetchable**."* Both 2b's steps and D9's edge cases are named in the shipped-text enumeration at spec.md:718-720, so the skill file will carry a procedure step and an edge-case bullet that disagree on the disposition of a whole-set `404` — exactly the token-scope-loss case the rule was written for, and the one where writing the reviews off costs the findings permanently.
**Suggested fix:** one clause on the D9 bullet, e.g. after "It is recorded **unfetchable**": *"— unless every review attempted in the round failed the same way, which is a session condition (GitHub masks permission failures as `404`) and floors them all instead."*

### F-2: D5's new `submitted_at > PUSH_TIME` gate is not reflected in Decision 2 or Decision 4, and Decision 4's exception list is explicitly closed
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D5 (spec.md:1282-1294) vs § Decision 2 (spec.md:59-64) and § Decision 4 (spec.md:130-142)
**Convention violated:** same single-source discipline (spec.md:82-83); and this is the drift pattern the spec has already corrected three times (the advance rule in round 1, the post condition in round 3, `R` in round 3).
**Evidence:** the round-3 fold added a real narrowing — spec.md:1283-1284: *"of the harvest set's parsed-and-deduped items, **only those from reviews with `submitted_at > PUSH_TIME` enter the count**"*. Neither upstream statement was updated. Decision 2 still says flatly *"6a's new-findings count includes parsed body items, so a review that carries body findings and no inline comments cannot read as 'nothing new'"* (spec.md:59-61) with *"Honored by: … 6a's amended poll (two summands)"* (spec.md:63-64). Decision 4 is worse, because its enumeration is closed by construction: *"One exception, **stated because it is a real asymmetry rather than a lapse**: 6d Phase 1 … Body findings therefore count **everywhere except** 6d Phase 1's short-circuit"* (spec.md:135-139). There are now two exceptions, and the sentence that promises to name the asymmetries names one. An implementer who writes 6a from Decisions 2/4 rather than from D5 reproduces the backlog-drain defect edge-cases a2r3-F-4 was filed against.
**Suggested fix:** in Decision 4, change *"Body findings therefore count everywhere except 6d Phase 1's short-circuit"* to *"Body findings therefore count everywhere except two scoped sites: 6d Phase 1's short-circuit (no thread) and 6a's `new_body_items`, which counts only post-push reviews so a bounded backlog cannot read as an incremental review (D5)."* In Decision 2, add *"— post-push reviews only; D5 holds the only statement of the count rule."*

### F-3: D5 promises a 6e backlog count that D8's report block — the single source for those lines — does not contain
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D5 (spec.md:1291-1294) vs § D8 6e report block (spec.md:1536-1545)
**Convention violated:** the spec's own shipped-text rule names *"D8's 6e report lines"* (spec.md:719-720) as the region the skill carries; a report field stated only in D5 has no shipped home.
**Evidence:** D5: *"6e's `Body-level findings` line reports items triaged from backlog **under their own count** so `new-findings` is never read as 'the incremental review found things' when it did not."* D8's block is the authoritative list, and its line is `- Body-level findings: B (outside-diff: b1, nitpick: b2) — dispositions posted in <comment-url> | …` — no backlog field, and no other line supplies one (`grep -n -i backlog VHS-41.spec.md` hits `:1292` and nothing in D8's range). `Body harvest bounded:` reports *deferred* reviews, which is the complement, not this. The half of edge-cases r3-F-4's fix that made the honesty visible to the operator is therefore unimplementable from the section that ships.
**Suggested fix:** extend D8's first line to `- Body-level findings: B (outside-diff: b1, nitpick: b2; from backlog reviews: bk) — dispositions posted in <comment-url> | …`, and reduce D5's sentence to a pointer at 6e.

### F-4: Decision 13 answers VHS-29 but never names VHS-28, whose Revisit trigger table lands on this design directly
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 13 (spec.md:600-636); wiki `decisions/2026-08-25-vhs-28-validator-does-not-parse-markdown.md`
**Convention violated:** "Contradicts a prior decision" — a decision page with an explicit revisit trigger naming this proposal class, fired without acknowledgment.
**Evidence:** Decision 13 handles VHS-29 correctly (I verified the quoted sentence: `2026-08-25-vhs-29-anchor-is-a-refusal-contract.md:39-41`, *"fence masking is the first step toward a markdown parser inside a skill script"*). But the closer prior decision is VHS-28, whose title *is* the objection — **"The Handoff Validator Does Not Parse Markdown"** — and whose `## Revisit trigger` table reads:

| Proposal | Why it lands here |
|---|---|
| "Just terminate sections at the next heading" | That is the vendor's bug, restated. It is wrong inside fenced blocks and wrong across depth changes |
| Extracting section *bodies* for any purpose (summarizing, diffing, linting prose) | Body extraction needs boundaries. Same parser, different justification |

2b steps 5–9 are section-boundary computation, body extraction, fence and inline-code masking, and a `<details>` depth walk — the enumerated trigger, three times over. VHS-28 closes with *"If a body-level feature genuinely earns its keep, the honest move is to reopen … deliberately — not to reintroduce a hand-rolled scan that is correct on the happy path and silently wrong on fenced code."* Decision 13's existing argument in fact *answers* this (read-only rather than write-placing, tripwires instead of silent wrongness, masking capped at two constructs, no AST) — the gap is that the reopening is not addressed to the decision that asked for it, so `/spec-close`'s wiki decomposition will have no supersession link and the next editor hitting VHS-28's table will find no prior answer. `grep -rn 'VHS-28' docs/specs/TODO/VHS-41.*` is empty across the spec and all three rounds of reviews.
**Suggested fix:** one paragraph in Decision 13, after the VHS-29 discussion: name VHS-28's revisit trigger ("extracting section bodies for any purpose"), state that this spec fires it deliberately, and give the two discriminators already argued — the consumer is an agent procedure rather than a stdlib-only script (so the stdlib-only contract VHS-28 protects is untouched), and the failure mode is a reported tripwire rather than a silently corrupted file. Add the page to the spec's reference set so the close carries the link.

### F-5: the test plan mandates pytest in a repo whose tests are stdlib `unittest` and whose AGENTS.md declares stdlib-only
**Severity:** P3
**Where:** spec § Test plan (spec.md:1722-1724, row 16 at spec.md:1760/:1784), § D10 (spec.md:1712-1716), § Scope (spec.md:29)
**Convention violated:** `AGENTS.md:7` — *"no dependencies beyond Python 3.8+ stdlib"* — the very line D10 edits; and the repo's own documented run form.
**Evidence:** the spec asserts *"The repo **does** have a pytest suite — `tests/test_lint.py`, …"* (spec.md:1722) and *"The repo ships five pytest modules"* (spec.md:1714). All five import `unittest` (`grep -l 'import unittest' tests/*.py` → all five), and `tests/test_lint.py:3-4` states *"Stdlib unittest. Run directly: `python tests/test_lint.py`."* There is no `pytest.ini`, `pyproject.toml`, `setup.cfg`, or requirements file in the repo root. Row 16's `python -m pytest tests/ -q` and the VHS-42 baseline string `1 failed, 158 passed, 3 skipped` are pytest-runner artifacts — reproducible here only because pytest 9.0.2 happens to be installed on this machine, not because the repo asks for it. The AGENTS.md edit itself is right and matches the wiki (`projects/vigil-skills/state.md:60` records `tests/test_lint.py` as *"the repo's **first test suite**"*); only the characterization and the runner drift.
**Suggested fix:** call them "five stdlib `unittest` modules" in both places, and give row 16 the stdlib form — `python -m unittest discover -s tests -q` — with the pytest invocation noted as an equivalent local convenience. Re-measure the baseline string in whichever runner the row names, so § Deferred and row 16 agree.

### F-6: `README.md:14` carries the same class of user-facing `/review-pr` description as `AGENTS.md:48`, and the spec excludes it without saying why
**Severity:** P3
**Where:** spec § Scope (spec.md:28-30), § Out of scope item 3 (spec.md:1918-1921) vs `README.md:14`
**Convention violated:** the spec's own r1-F-3 rationale for the `AGENTS.md` edit — *"The paragraph describes the skill's finding sources and write classes; body-level harvest and the PR-level disposition comment are both new and both externally visible."*
**Evidence:** `README.md:14` reads *"**`/review-pr [<num>]`** — Process one round of CodeRabbit review findings on a GitHub PR. Triages by severity, fixes real issues, pushes, resolves threads, and verifies the resolve actually took."* Same two properties: it names the finding source ("CodeRabbit review findings") and the write classes ("pushes, resolves threads"), and this change adds a third write class (a PR-level comment). Out of scope item 3 lists `README.md` in a flat enumeration with `sync.py`, `lint.py`, and `tests/`, none of which describe the skill's behavior. The exclusion is defensible — README's entry is a one-line index consistent with its neighbors, and it stays literally true — but the spec is otherwise meticulous about recording why a surface it could reasonably touch is left alone.
**Suggested fix:** one clause in Out of scope item 3: *"`README.md:14`'s one-line index entry stays true as written and is deliberately not extended — the write-class detail lives in `AGENTS.md:48`, which is where the r1-F-3 argument applies."*

### F-7: the Scope table calls a three-word strike "two words"
**Severity:** P4
**Where:** spec § Scope, `AGENTS.md:7` row (spec.md:29)
**Convention violated:** nothing structural — the Scope table is a load-bearing implementer instruction elsewhere in this spec (the `AGENTS.md:48` row says "one sentence" accurately).
**Evidence:** the row reads *"**Change — two words.** Strike 'no test suite'…"*. That is three words (plus the trailing comma). D10 (spec.md:1712-1716) quotes the before and after exactly, so no implementer is misled.
**Suggested fix:** *"**Change — three words.**"*

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 2 | P4: 1

Key paths:
- Spec: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.spec.md`
- Brief: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.brief.md`
- Subject: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\skills\review-pr\SKILL.md` (406 lines, unmodified on `main`)
- Conventions sources: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\AGENTS.md`, `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\CLAUDE.md`, `C:\Users\zioni\.claude\CLAUDE.md`
- Prior decisions read: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki\decisions\2026-08-25-vhs-28-validator-does-not-parse-markdown.md`, `…\2026-08-25-vhs-29-anchor-is-a-refusal-contract.md`, `…\2026-09-07-vhs-36-operator-claims-are-verified-not-trusted.md`, `…\2026-06-14-vhs-18-lint-warn-only-strict-gate.md`
- Wiki project pages: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-harbor-wiki\projects\vigil-skills\state.md`, `…\filemap.md` (no `architecture.md` for this project)
- Round-3 reports: `C:\Users\zioni\Documents\Vigil-Harbor\vigil-skills\docs\specs\TODO\VHS-41.reviews\round-3\` (no `scalability.md` present; `scale_lens: off` respected)

STATUS: GREEN
