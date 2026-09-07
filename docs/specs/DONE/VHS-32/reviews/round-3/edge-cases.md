# Edge-Cases Review — round 3

Grounding complete. Read from disk: the v3 spec (all 556 lines), the brief, both `CLAUDE.md` files, all three round-2 reports, and re-verified every anchor the closure manifest touches against `skills/spec-cycle/SKILL.md` (step 5 origin at `:133`, step 6 at `:234`, step 8 scale at `:237`, synthetic missing-STATUS P0 at `:371–375`, 2f at `:466–485`, Tool-use notes `:570`, Failure modes `:578`, stale-report backstop `:604–620`), plus `.gitignore`. Plane VHS-32 not re-queried (the brief carries the ticket body).

## Closure of round 2 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| edge-cases | F-1 | `empty-seed` unhandled at 2f-i and `/grill-me` (P1) | CLOSED | spec:403 (2f-i step 1 guard, "do not invoke `grilling`… write nothing to `grill.md`… re-render 1–3"), :226 (Design 2 `empty-seed` line), :127 (S9 names all three callers), :459 (checklist 7 greps "nothing grillable") |
| edge-cases | F-2 | Hung exploration blocks the round while §1.5 claims it cannot (P1) | CLOSED | spec:183 ("Where it does not, a dispatch that never returns blocks the round it belongs to… §Risks 12"); the unconditional "never blocks a round" clause is gone; :43 (D2 gains "answer from the paths named… return `not found`"), :523 (Risk 12), :373 (Failure-modes bullet) |
| edge-cases | F-3 | `--no-grill` can never emit `## Scale` (P2) | CLOSED | spec:343 (fifth bullet: same cases applied to an explicit ticket-text declaration) |
| edge-cases | F-4 | Failed grounding dispatch under `--no-grill` dropped (P2) | CLOSED | spec:292 ("under `--no-grill` it becomes a `## Risks / decisions` item… spec author pins this") |
| edge-cases | F-5 | Fact-dispatch cap had no overflow rule (P2) | CLOSED | spec:183 (carry by S1 ordering; else Open with `fact not established`) |
| edge-cases | F-6 | Option 2 re-selectable without limit (P2) | CLOSED at the caller | spec:117, :311 ("one post-cap revision round… after it, option 2 is no longer offered"). Residual: the *primitive* side of the grant is unstated — new F-1 |
| edge-cases | F-7 | Origin-behind warning not carried into the durable Scope claim (P2) | CLOSED | spec:336 (annotated `## Scope` heading + matching References bullet) |
| edge-cases | F-8 | `grill.md`: atomicity, dedup, concurrency, durable once-signal (P2) | **PARTIAL** | Atomicity/counter/last-writer closed: spec:123, :405 (read-modify-tmp-rename, `# Grill <k>`). The "durable backstop" keyed to "this invocation's Phase 0 preflight" datetime is circular — `/spec-cycle` records no preflight timestamp (`:292` prints tokens only) and Phase 0 is declared untouched (spec:25). New F-4; concurrency residual in F-5 |
| edge-cases | F-9 | `## Scale` had no slot in the section order (P3) | CLOSED | spec:329 (`## Scale  (conditional — see the emission rule below)`) |
| edge-cases | F-10 | S9 re-prompt undefined in ticket mode (P3) | CLOSED | spec:127 (ticket-mode re-prompt verbatim; header keeps the resolved ticket line) |
| edge-cases | F-11 | Leaked `.tmp` invisible / archived by `/spec-close` (P3) | **PARTIAL** | Dot prefix + halt row landed: spec:334, :265, :271. But step 2's *trigger* is still brief/spec/reviews only, so the one state that creates an orphan tmp never fires the halt — new F-3 |
| edge-cases | F-12 | Option 1 wording assumed a brief exists (P3) | CLOSED | spec:271 (conditional wording, spec explicitly not read as grounding) |
| edge-cases | F-13 | Empty Settled writes a bare header (P3) | CLOSED | spec:336 (`_(none settled — see Risks / decisions)_` + warning line) |
| correctness | F-1 | Three wrong `spec-cycle` anchors (P2) | CLOSED | spec:529 now `:133–233` / `:237` / `:371–375` — all three re-verified on disk |
| correctness | F-2 | `##` headings closed `## Design` (P2) | CLOSED | spec:359, :363 are `####`; Design 4/5/6 nest correctly again |
| correctness | F-3 | §1.3 block lacked the round-cost line (P2) | CLOSED | spec:176 ("a partly answered round still uses one of your `<round_cap>` rounds") |
| correctness | F-4 | Revise had no re-entry into the primitive (P2) | PARTIAL→ see F-1 | `prior_summary` input added (spec:157) and Phase 3 re-invokes with it (:311); the budget arithmetic it must drive is still caller-only |
| correctness | F-5 | Empty 2f-i seed (same root as edge F-1) (P2) | CLOSED | spec:403 |
| correctness | F-6 | Scope table had no derivation rule (P2) | CLOSED | spec:336 (one row per named path, `Current` from a fact `path:line`, `Change` from the settled decision, no-evidence paths → Risks) |
| correctness | F-7 | Factor/target dependency inverted (P3) | CLOSED | spec:339 ("one question, not two") |
| correctness | F-8 | "three states" over four bullets (P4) | CLOSED | spec:338 ("four input cases, three emitted shapes") |
| conventions | F-1 | Spec-additions ledger incomplete (P2) | CLOSED | spec:31 enumerates the five point-of-use additions |
| conventions | F-2 | Undotted temp name (P2) | CLOSED | spec:334 (dot-prefixed, cited to `prepend_log_entry.py:370–375`), :361 (Tool-use notes names the lone mutation) |
| conventions | F-3 | Upstream name collision undocumented (P2) | CLOSED | spec:423 (`AGENTS.md` bullet), :445, :524 (Risk 13), :464 (checklist 12) |
| conventions | F-4 | "Deferred" section mislabelled (P4) | CLOSED | spec:548 ("folded in a different shape than proposed, or deliberately not folded") |

Both round-2 P1s are genuinely closed. Two P2s are PARTIAL; neither blocks the gate.

## Findings

### F-1: The post-cap `+1` round exists only in the caller's section — the primitive's own contract, rebuilt from `prior_summary`, would exit `round-cap` with zero questions asked
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1.1 `prior_summary` bullet (`:157`), § 1.4 (`:181`), § 1.6 (`:185`), § 1.7 (`:187`) vs § S7 revise bullet (`:117`) and Phase 3 (`:311`); checklist 4 (`:456`)
**Edge case:** Re-entry with an exhausted budget — the exact state option 2 was added for. Operator runs `--rounds 3`, the interview exits `round-cap`, and at the confirm they pick "2. Revise an answer".
**What happens:** Phase 3 re-invokes `grilling` with `prior_summary` "and the same bounds". §1.1 says `rounds_used` carries over — so the primitive starts at `rounds_used == round_cap == 3`. Nothing in Design 1 (the section that *is* the authoring spec for `skills/grilling/SKILL.md`) says a round may be granted past the cap: §1.6 pins "the three bounds with defaults", and §1.7 merely lists `revised-after-cap` among the exit tokens without saying what produces it. A faithful implementer's primitive therefore terminates immediately on re-entry, and because the named decision "and everything settled downstream of it return to the frontier" happens *before* that check, the operator ends up strictly worse off than before: the decision they wanted to revise is now an unanswered Open item written into `## Risks / decisions` as "spec author pins this", and option 2 is no longer offered. Three further re-entry facts are unstated and each has a concrete wrong branch: (a) prior **Open** items — if they re-enter as "carried-over", S1's ordering ("carried-over and re-asked items first") renders them ahead of the revised subtree and can consume the entire single granted round; (b) prior **Facts established** — if not carried, the +1 round re-dispatches explorations already answered, re-incurring the §Risks-12 hang exposure; (c) **Q numbering** — S1 pins monotonic numbers "across the whole interview", but a second invocation rebuilding from a summary has no stated rule to continue the series, and if it restarts at `Q1` the confirm prompt's "name the Q number" becomes ambiguous against the summary the operator is reading.
**Why the spec misses it:** `prior_summary` was added this round to close correctness/F-4 (an *input* gap) and the once-only bound to close edge-cases/F-6 (a *repetition* gap). Both fixes were written into the caller's sections — S7 and Phase 3 — while §1.1's bullet describes only tree reconstruction. §1.4 explicitly enumerates which S7 rules the body carries ("S7's omitted / defer / free-form rules") and revise is not among them; checklist 4's verbatim-content list omits it too, so nothing catches the omission at ship time. Also note S7's "granted per invocation" does not say *whose* invocation — read as the primitive's, each re-entry grants its own round and the bound is back to caller-only enforcement.
**Suggested fix:** extend §1.1's `prior_summary` bullet to be the whole resume contract: *"…`rounds_used` carries over. If `rounds_used ≥ round_cap`, exactly one additional round is granted for this resume and the exit token is `revised-after-cap (+1 round)`; the caller decides whether to offer another resume. Open items from the prior summary stay Open (they are not re-asked) unless downstream of the revised decision; Facts established carry over and are not re-dispatched; Q/F numbering continues the prior series."* Add "revise/resume" to §1.4's list and one bullet to checklist 4. Add a checklist row (or a Run D transcript stub) exercising option 2 after a `round-cap` exit — the revise path currently has no coverage in either transcript.

---

### F-2: 2f-i has no disposition for a Settled decision that cannot be executed as an in-place spec edit, and its invariant list does not forbid touching the brief
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 4 Edit 2 step 4 (`:406`), step 5 (`:407`), invariants (`:409`); § D8 (`:69`)
**Edge case:** Runtime precondition violation — the grill settles a disposition the caller cannot apply. At the round-4 halt the commonest honest disposition for a stuck P0/P1 is "the brief is wrong / this is out of scope", which is precisely what menu option 3 ("Treat as scoped-down — narrow the brief") exists for. The 2f-i altitude ("a decision that dispositions one of the listed findings") admits such an answer; nothing filters it out.
**What happens:** Step 4 says, unconditionally, "For each **Settled** item, edit the spec in place under the 2e rounds-1–3 rules." A decision like "drop this from scope — the brief overreaches" has no in-place spec edit that honestly discharges it. The implementer has two bad branches: edit the *brief* (a write to the one artifact every reviewer lens, every closure table and `/spec-close` reconciliation treats as authority, from a stage that declares elsewhere it never does so — §D8 says the primitive "cannot patch", but says nothing about the caller's reach), or paper it over with a spec edit that asserts a scope narrowing the brief does not carry — which the next `/spec-cycle` run's conventions lens scores as a silent addition. Step 5's counters make either invisible: the item was Settled, so it is counted in `<s> findings dispositioned` and disappears from the red list, while `total_p0p1` is deliberately unchanged — so the audit line says the finding was handled and the gate says it was not, with no third category.
**Why the spec misses it:** D8 was written as a constraint on the *primitive* ("it never re-dispatches reviewers… and the primitive itself has no write capability"), and step 4 was written for the applicable case. The invariants sentence enumerates five nevers, all about the round counter, the gate, reviewers, and `grill.md` — none about the brief, the one file 2f-i sits closest to and the one whose mutation is unrecoverable for prior rounds' closure tables.
**Suggested fix:** one sentence in step 4 — *"A Settled decision that cannot be discharged by an in-place spec edit (e.g., 'narrow the brief') is not applied: report it in step 5 as `deferred to option 3: <finding id>`, leave the finding P0/P1, and record it in `grill.md` as Settled-but-unapplied."* — and add `never edits the brief` to the invariants list at `:409` (and to checklist 7's grep list, which already asserts four of the five nevers).

---

### F-3: The stale-`.tmp` cleanup never fires on the only run shape that leaves one, and the dot prefix does not make it uncommittable in this repo
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 Phase 0 step 2 (`:260–275`), Phase 4 (`:334`), § Decisions preamble (`:31`)
**Edge case:** Partial failure of the new atomic write. The operator kills the first `/spec-brief VHS-40` between temp-create and rename — or, more likely, aborts at the Phase 3 confirm / hits the S9 halt *after* a partial write attempt. No brief, no spec, no reviews dir exists; only `.VHS-40.brief.md.tmp` remains.
**What happens:** step 2's trigger is stated as "Check `docs/specs/TODO/<TICKET-ID>.brief.md`, `<TICKET-ID>.spec.md`, and `<TICKET-ID>.reviews/`. **If any exists**, halt" — the temp is only a *row inside* the halt block and option 1's cleanup ("a stale `.tmp` is removed") only runs if the halt fires. In the orphan-tmp state none of the three triggers exist, so the halt is skipped, the stale row never prints, and the file is reported and removed by nothing. It survives every subsequent aborted run. Phase 4's claim at `:334` — "is reported and removed by Phase 0 step 2 on the next run" — is therefore false on exactly the path it describes. Second, the dot prefix is cited to `skills/spec-close/scripts/prepend_log_entry.py:370–375`, whose stated rationale is that *the wiki's* `.gitignore` carries `.*.tmp`; I checked this repo's `.gitignore` — `__pycache__/`, `*.pyc`, `.DS_Store`, `*.swp`, `.idea/`, `.vscode/`, `CLAUDE.md`, `.claude/`, `.hermes/`, `.talaria-review-hermes/` — no `*.tmp` or `.*.tmp` entry, and dotfiles are not ignored by git by default. So in vigil-skills (and in any target repo that copies this shape) a leaked `.VHS-40.brief.md.tmp` under `docs/specs/TODO/` is a staging candidate for a plain `git add -A`; the spec's protection reduces to the prose "must not be committed". The dot prefix still earns its place by dodging `/spec-close`'s `<TICKET-ID>.<rest>` glob (verified `spec-close:340`) — that half of round-2/F-11 is genuinely closed.
**Why the spec misses it:** the stale row and option-1 cleanup were added as a *display* fix to edge-cases/F-11; the trigger list one sentence above was written earlier for the artifact-collision case and was not extended. And the precedent citation was carried across repos without re-checking that the ignore rule came with it.
**Suggested fix:** add the temp to the trigger — *"Check `…brief.md`, `…spec.md`, `…reviews/`, and `.<TICKET-ID>.brief.md.tmp`. If only the stale temp exists, remove it, log `stale temp removed: .<TICKET-ID>.brief.md.tmp`, and continue without halting; if any artifact exists, halt with the block below."* And either drop the `prepend_log_entry.py` rationale (keep the citation for the *shape* only, since the archive-glob reason is the one that holds here) or add `.*.tmp` to `.gitignore` as a one-line scope addition with rationale.

---

### F-4: S8's "durable backstop" for the once-per-invocation bound depends on a timestamp `/spec-cycle` never records and this spec may not add
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § S8 (`:123`), § Scope "Files explicitly untouched" (`:25`)
**Edge case:** Context loss at the halt — the state the backstop exists for. The 2f halt says "Wait for the user"; a session can be compacted or resumed there.
**What happens:** S8 reads: *"The once-per-invocation bound is held in context; as a durable backstop, a `# Grill` header whose datetime is later than this invocation's Phase 0 preflight means option 4 already ran."* The comparison needs "this invocation's Phase 0 preflight" datetime, which is not written anywhere: `/spec-cycle` Phase 0's one-line preflight summary (`:292`, verified) prints only result tokens — upstream, origin, scale-lens — and no time; nothing else in the file emits a timestamp; and this spec's Scope explicitly declares "every line of `skills/spec-cycle/SKILL.md` outside the three named edit sites (in particular Phase 0)" untouched, so the backstop cannot be given its input without breaking the fence. The check therefore rests on the model recalling its own start time — the same context the bound already lives in, so it backs up nothing. The consequence is mild in both directions (a second grill block appended in one invocation, visible via the `<k>` counter; or a legitimate option 4 wrongly withheld, recoverable by re-running), which is why this is P2 and not higher — but the spec states a durability guarantee its mechanism does not deliver, the same shape as the "never blocks a round" claim that was a P1 last round.
**Why the spec misses it:** the datetime form was chosen this round specifically to avoid the same-day false positive my round-2 F-8 would have caused (correctly — see § Deferred `:550`); the substitution was checked for correctness of the *predicate* but not for availability of its operand.
**Suggested fix:** state the bound honestly rather than inventing durability — *"The once-per-invocation bound is held in context; `/spec-cycle` records no preflight timestamp, so there is no on-disk signal that distinguishes this invocation's grill from a prior one. An existing `# Grill` header that this session did not write does not withhold option 4; the `<k>` counter makes any duplicate visible in the audit trail after the fact."* Record it beside Risks 12 as an accepted limitation.

---

### F-5: Concurrent appends to `grill.md` lose a whole block, and the `<k>` counter cannot make that visible; the shared fixed temp name can also interleave
**Severity:** P3
**Where:** spec § S8 (`:123`), § Design 4 Edit 2 step 3 (`:405`)
**Edge case:** Write-then-read race on new persisted state. `/spec-cycle` documents separate invocations sharing one reviews tree (`:604–620`, verified), so two sessions at the same ticket's round-4 halt can both run option 4.
**What happens:** the append is read-modify-tmp-rename, so two writers that both read a file containing `# Grill 1` both emit `# Grill 2` and the second rename discards the first's block entirely — a lost update, not a duplicate. S8's claim, "last writer wins and **the counter makes any duplicate visible**", describes the wrong hazard: nothing in the surviving file records that a grill was dropped, and `/spec-close` archives the truncated history to `DONE/` as the audit trail of why the spec moved after the halt. Second, both step 3 and Phase 4 pin a *fixed* dot-prefixed temp name in the target directory (Phase 4's is fixed by necessity, since Phase 0 step 2 detects it by name); the repo's two shipped atomic writers instead use `tempfile.mkstemp` for unique names (`prepend_log_entry.py:374–375`, `create_handoff.py:340–341`). Two concurrent writers sharing one temp path can rename a half-written file into place, which is worse than the lost update the discipline was adopted to prevent.
**Why the spec misses it:** round-2/F-8 asked for atomicity and got the single-writer discipline; the concurrency clause was written as a disposition sentence rather than derived from the read-modify-write shape.
**Suggested fix:** reword S8 — *"Under concurrent invocations sharing the reviews tree, the append is last-writer-wins over the whole file: a concurrent grill can be lost, and neither the counter nor `/spec-close` can detect it. Accepted; grilling the same ticket's round-4 from two sessions is out of the supported flow."* And give the append's temp a unique suffix (`.grill.md.<random>.tmp`), which costs nothing because — unlike Phase 4's — no other step detects it by name.

---

### F-6: Under `--no-grill` the Phase 1 grounding fan-out is bounded by a value the Invocation section has just declared ignored
**Severity:** P3
**Where:** spec § Design 3 Invocation (`:254`), Phase 1 step 4 (`:292`)
**Edge case:** Configuration interaction. `/spec-brief VHS-40 --no-grill --questions 15`.
**What happens:** Invocation says "`--no-grill` wins over any cap flag; if both are given, warn `--rounds/--questions ignored under --no-grill` and continue." Phase 1 step 4 — which runs *before* the `--no-grill` skip and is not gated on it — bounds the exploration batch at "at most `question_cap` dispatches". An implementer who reads the warning as "there is no question cap on this run" has no bound for the grounding fan-out at all, on the one path where a hung dispatch has no interview round to degrade into (Risks 12) and the failed-fact rule routes to `## Risks / decisions` instead. The likelier reading (flags ignored → defaults 3/7 stand → cap 7) is fine, but the text does not say which.
**Suggested fix:** one clause at `:254` — *"…ignored **for the interview**; the default question cap (7) still bounds Phase 1's grounding batch."*

---

### F-7: Neither transcript nor checklist exercises the three paths this round's fixes created
**Severity:** P3
**Where:** spec § Test plan (`:466–470`), checklist rows 7 and 9 (`:459`, `:461`)
**Edge case:** Test-coverage gap. Runs A/B/C cover empty-frontier, round-cap, and empty-seed. The three behaviors added in v2→v3 with the most branching — Phase 3 option 2 / `prior_summary` (F-1 above), `--no-grill` (which now carries its own `## Scale` derivation at `:343`, its own failed-dispatch rule at `:292`, and its own option-2 wording at `:311`), and 2f-i end-to-end — have no transcript and no checklist assertion beyond string greps.
**What happens:** nothing at runtime; but the review checklist is explicitly "the gate for `/ship-spec`", so a `grilling` body that silently omits the resume arithmetic, or a `--no-grill` path that emits no `## Scale` for a ticket that declares a target, ships green. Checklist 9 asserts Phase 4 "states the tmp-then-rename write and the three-state `## Scale` rule" — worth updating to the four-case wording now at `:338` as well.
**Suggested fix:** add one checklist row — *"`spec-brief` body: the `--no-grill` path states its own `## Scale` derivation, its failed-dispatch → Risks rule, and its option-2 wording; the Phase 3 option-2 path states re-invocation with `prior_summary`, the single post-cap round, and the fallback to options 1 and 3"* — and, if a fourth transcript is too costly, a Run D checklist row for option 2 after a `round-cap` exit.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 3 | P4: 0

STATUS: GREEN
