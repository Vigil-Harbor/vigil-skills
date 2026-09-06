# Edge-Cases Review — round 4

Grounding complete. Read from disk: the v4 spec (all 562 lines), the brief, both `CLAUDE.md` files plus `AGENTS.md`'s pointers, all three round-3 reports, and re-verified the live anchors this round's closures depend on — `skills/spec-cycle/SKILL.md:466–485` (halt block is still exactly 3 options), `:573` (`mkdir` named among Bash uses), `:604–620` (the stale-`scalability.md` backstop, scoped to `round-<N-1>` closure reads), `:230–292` (Phase 0 step 7/8 + preflight summary — no timestamp emitted, confirming S8's honest rewrite), and `.gitignore` (still no `*.tmp`, matching the spec's corrected prose). `scale_lens: off`; no `scalability.md` exists in `round-3/`, so the stale-report guard is a no-op this run. Plane VHS-32 not re-queried — the brief carries the ticket body.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P1) | Post-cap revision round promised, granted by none | **CLOSED** | spec:157 (§1.1 carries the full resume contract: "If `rounds_used ≥ round_cap`, this invocation runs exactly one additional round and exits `revised-after-cap (+1 round)`; a further `prior_summary` … exits `round-cap` at once"), :181 (§1.4 cites it), :185 (§1.6 lists the single post-cap round among the bounds), :205 (bound now `(round_cap + 1) × question_cap`), :117/:313 ("the same `round_cap` / `question_cap` — the primitive owns the resume arithmetic"), :458 (checklist 4), :474 (Run D) |
| correctness | F-2 (P2) | 2c scalability stub missing from not-grillable | CLOSED | spec:405 ("any 2c dispatch-failure stub … `skills/spec-cycle/SKILL.md:404–409`") — verified against the live file |
| correctness | F-3 (P2) | No derivation rule for `## Out of scope` / `## Done when` | CLOSED | spec:338 (fence-shaped Settled → `## Out of scope`; Problem / Why it matters / Done when transcribed, never inferred) |
| correctness | F-4 (P2) | "Answer by number" omits the branch letter | CLOSED | spec:175 ("Answer by question number and branch letter (e.g. `Q3 B`); a plain answer is recorded as given.") |
| correctness | F-5 (P3) | `question_cap` "ignored" under `--no-grill` | CLOSED | spec:256 ("ignored for the interview; the default question cap (7) still bounds Phase 1's grounding batch") |
| correctness | F-6 (P3) | D8 seed drifts from Design 4 step 1 | CLOSED | spec:69 ("minus the not-grillable exclusions in Design 4 step 1") |
| correctness | F-7 (P3) | Runs A/B share `ZZZ-1` | CLOSED | spec:469 ("Run A uses `ZZZ-1` and Run B uses `ZZZ-2` (a shared id would trip Run B into the artifacts-exist halt…)") |
| correctness | F-8 (P3) | Local-only header fields unsourced | CLOSED | spec:338 (`**Status:** local-only · **Priority:** unset · **Assignee:** unassigned`) |
| correctness | F-9 (P3) | `sync.py:146` is `cmd_push`, not install | CLOSED | spec:447 ("`sync.py:96`, the install copy; `:146` is the symmetric push copy") |
| correctness | F-10 (P4) | Three residual label/bound nits | CLOSED | spec:463 ("four-case `## Scale` rule"), :205 (`(round_cap + 1) × question_cap`), :539 (`lint.py … :45–49`) |
| edge-cases | F-1 (P2) | Resume arithmetic absent from the primitive | **CLOSED** | Same root as correctness F-1. All three sub-facts pinned at :157 — prior Open stays Open unless downstream; Facts carry over and are not re-dispatched; Q/F numbering continues the prior series |
| edge-cases | F-2 (P2) | Settled-but-unapplicable at 2f-i; brief unprotected | CLOSED | spec:408 ("not applied: report it in step 5 as `deferred to option 3: <finding id>` … record it in `grill.md` as Settled-but-unapplied. 2f-i never edits the brief."), :411 (invariant added), :461 (checklist 7 greps both strings) |
| edge-cases | F-3 (P2) | Stale-`.tmp` cleanup never fires; gitignore rationale wrong | CLOSED | spec:262 (temp added to the step-2 *trigger*; "If only the stale temp exists, remove it, log …, and continue without halting"), :336 ("unlike the wiki this repo's `.gitignore` does not ignore `.*.tmp`, so the no-commit rule below is prose, not mechanism") — re-verified against `.gitignore`; :556 records the gitignore addition as deliberately not adopted |
| edge-cases | F-4 (P2) | S8's "durable backstop" needs a timestamp that doesn't exist | CLOSED | spec:123 ("held in context only: `/spec-cycle` records no preflight timestamp, so no on-disk signal distinguishes this invocation's grill from a prior one"), :529 (Risk 14). Verified: `spec-cycle:292` prints tokens only |
| edge-cases | F-5 (P3) | Concurrent `grill.md` appends lose a block; shared temp name | CLOSED | spec:123 ("a concurrent grill can be lost and nothing detects it; accepted"), :407 (`.grill.md.<random>.tmp`, "nothing detects this one by name") |
| edge-cases | F-6 (P3) | `--no-grill` grounding fan-out unbounded | CLOSED | spec:256 (same clause as correctness F-5) |
| edge-cases | F-7 (P3) | Resume / `--no-grill` / 2f-i paths untested | CLOSED | spec:467 (checklist 13), :474 (Run D) |
| conventions | F-1 (P2) | VHS-28 revisit trigger never engaged | CLOSED | spec:447 ("This is the second supersession … the revisit trigger in `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md`. A tracked uninstall manifest is still not warranted…"), :77 (D10 narrowed: "the *supersession* mechanism differs"), :548 (References) |
| conventions | F-2 (P2) | `AGENTS.md` edit had no defined slot | CLOSED | spec:425 ("one short paragraph (not a bullet) … appended after the closing 'If AgentCraft reinstalls its copy…' paragraph"), :466 (checklist 12 asserts the "Two warnings:" list still has exactly two bullets) |
| conventions | F-3 (P3) | README tagline / Requirements left pre-VHS-32 | CLOSED | spec:23 (Scope row now names `:3`), :439 (tagline rewrite + `/spec-close` Requirements) |
| conventions | F-4 (P3) | Two v3 emission rules outside the `:31` ledger | CLOSED | spec:31 ("…and the local-only header fields") — closes the class rather than re-enumerating |
| conventions | F-5 (P4) | `grilling` has no `## Failure modes` | CLOSED | spec:211 (§1.11), :458 (checklist 4: "`## Tool-use notes` and `## Failure modes` are real `##` headings") |

The round-3 P1 (correctness F-1, shared root with edge-cases F-1) is genuinely closed: the resume contract now lives in the primitive's own §1.1, is cross-referenced from §1.4/§1.6/§1.8, and is gated by checklist 4 and Run D. No REOPENED items, no PARTIALs.

## Findings

### F-1: A round-1 frontier emptied by the altitude fence exits `empty-frontier` — a zero-round interview that every caller reads as success
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § S9 (`:127`), § Design 1.2 (`:159`), § 1.7 (`:187`), § 1.8 header (`:192`); Design 4 step 5 (`:409`); Phase 4 References bullet (`:338`)
**Edge case:** A seed with a real root decision whose entire round-1 frontier is out of altitude. The commonest instance is 2f-i: findings whose honest dispositions are all implementation-level ("rename the variable", "fix the anchor"), which the 2f-i fence ("a decision that dispositions one of the listed findings") admits in principle but the brief-altitude reasoning in §1.6 trains the primitive to reject. A `/spec-brief` instance exists too — a ticket specified down to the file list.
**What happens:** S9 defines only two round-1 states: `empty-seed` = "no frontier at round 1 **because the tree has no root**", and `empty-frontier` = "tree **fully visited**". A frontier emptied by the fence is neither, so it falls through to `empty-frontier` — the success token. The primitive renders zero questions, exits at `rounds: 0/3`, and hands back an empty Settled list. `/spec-brief` then prints `Interview: 0 rounds, exit empty-frontier` in `## References` — a bullet that reads as a completed interview — while the empty-Settled sentinel and its warning (`:338`) are the only signals that nothing was asked. 2f-i prints `grill applied: 0 findings dispositioned` and re-renders with options 1–3, having burned the once-per-invocation option 4 on an interview that asked nothing. Neither caller can distinguish "the design was already settled" from "the fence rejected everything", which are opposite operator actions (write the brief vs. widen the altitude or pick option 3).
**Why the spec misses it:** S9 was written to separate the *no-seed* case from the *converged* case; the fence was designed independently as a per-question filter (S3/S4) and its aggregate effect on the round-1 frontier was never traced. §1.2's exit rule keys on "no root decision", not "no askable decision". Nothing in the spec asserts that at least one item is rendered before a non-`empty-seed` exit, and the §1.8 header (`rounds: <n>/<round_cap>`) has a well-formed rendering for `n = 0`.
**Suggested fix:** one clause in §1.2 and a matching line in §1.7 — *"`empty-frontier` is reachable only after at least one round was rendered. If the tree has a root but no round-1 candidate satisfies the altitude fence, exit `fence-empty` with the one-line reason 'every candidate decision is below the altitude fence'; callers treat it like `empty-seed` (nothing was asked) but the message names the fence, not the seed."* If a fifth token is unwanted, the cheaper edit is to keep `empty-frontier` and require the reason line to say which of the two states produced it, plus one sentence at `:409` telling 2f-i to re-offer option 4 when zero items were rendered.

---

### F-2: 2f-i inherits `/spec-cycle`'s round-4 scalability report without inheriting its stale-report guard
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 4 Edit 1 (`:389`), Edit 2 step 1 (`:405`)
**Edge case:** Configuration drift across invocations. Invocation 1 runs with `scale_lens == on`, reaches round 4, writes `round-4/scalability.md`, and halts at 2f. The operator picks option 1; the brief's `## Scale` (or the recorded spec Decision the Phase 0 step-8 re-run pin reads) is changed, and invocation 2 runs with `scale_lens == off`. Rounds 1–4 overwrite the three standing lenses' reports; nothing writes or deletes `round-4/scalability.md`, so invocation 1's file survives verbatim.
**What happens:** both new read sites are conditioned on the phrase "when the scale lens ran", which does not say *this invocation*. Read as "the file is present" — the natural reading when the instruction is "read the round-4 reports on disk" — the halt block prints phantom scalability P0/P1 titles from a lens that did not run, and 2f-i seeds the grill with them. The operator is then interviewed on findings that are not summands of `total_p0p1`, and step 5 reports them under `<s> findings dispositioned` — the audit line credits work against a gate that never counted them, and `grill.md` archives that to `DONE/` as the record of why the spec moved. `/spec-cycle` already solved exactly this hazard for its own closure read (`skills/spec-cycle/SKILL.md:611–620`, verified: "the generalized closure read ignores any `scalability.md` in `round-<N-1>/` when `scale_lens == off` — so a stale report from a prior on-run can never inject a phantom finding into an off-run's gate"), but that guard is scoped to `round-<N-1>/`; the halt print and 2f-i read `round-<4>/`, which the guard does not reach.
**Why the spec misses it:** the scalability line was added as a *closure* of a VHS-15 three-lens hardcode — a correctness fix to a print statement. The corresponding stale-file exposure at the same path had been solved elsewhere in the file, and the spec's References cite `:598–600` (the malformed-scale failure mode) but not `:604–620`, so the existing guard was never brought forward to the new read site.
**Suggested fix:** make the condition explicit at both sites — *"plus `scalability.md` **only when `scale_lens == on` for this invocation**; a `scalability.md` present in `round-4/` under `scale_lens == off` is stale from a prior on-run and is ignored, matching the closure-read guard at `skills/spec-cycle/SKILL.md:611–620`."* Add `scale_lens` to Design 4 step 1's inputs and cite `:604–620` in § References.

---

### F-3: Phase 4 writes into `docs/specs/TODO/` and forecloses creating it — first use in any repo without that directory fails after the whole interview
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 Phase 4 (`:336`), "What `/spec-brief` never does" (`:359`), Tool-use notes (`:363`)
**Edge case:** Missing precondition — the target directory does not exist. `/spec-brief` is the *first* stage of the lifecycle, so the first-ever run in a repo adopting this workflow is exactly the run where `docs/specs/TODO/` has never been created. `AGENTS.md:94` puts specs in the target project and Phase 0 step 1 sets `project_root = cwd`, so this is the normal adoption path, not an exotic one (Dynasty, petland, or any downstream consumer per `docs/customizing.md:3`).
**What happens:** Phase 0 step 2's collision check finds nothing (correctly — nothing exists), Phase 1 grounds, Phase 2 runs the full interview, Phase 3 confirms, and Phase 4 then writes `.<TICKET-ID>.brief.md.tmp` into a directory that isn't there. Depending on how the implementer realizes the write, that is either a hard error that discards a completed interview with no resume state by design (`:376`), or a silent success if the host's write tool happens to create parents — which is worse, because the behavior then differs by harness on the skill's very first use. The spec actively pushes toward the failing branch: `:363` calls the rename "the skill's lone filesystem mutation outside the brief" and `:359` says the skill never writes "anything other than the one brief file (and its transient `.tmp`)". By contrast the sibling skill declares directory creation openly — `skills/spec-cycle/SKILL.md:573` names "`mkdir` for review subdirs" among its Bash uses.
**Why the spec misses it:** every anchor and dry run is inside vigil-skills, where `docs/specs/TODO/` has existed since VHS-6; Runs A–D all execute in that tree, so no transcript can surface it. The "lone mutation" phrasing was introduced to satisfy conventions/F-2's atomic-write review and was scoped to *file* writes, never re-checked against the containing directory.
**Suggested fix:** one clause in Phase 4 — *"create `docs/specs/TODO/` if it does not exist (as `/spec-cycle` does for its review subdirs, `skills/spec-cycle/SKILL.md:573`); the directory creation and the temp rename are the skill's only filesystem mutations outside the brief itself"* — with matching wording at `:359` and `:363`, and `mkdir` added to the Tool-use-notes Bash list.

---

### F-4: The operator-facing round counter has no form for the granted post-cap round — it renders "Round 4 of 3"
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 1.3 literal round-end block (`:176`), § 1.8 hand-off header (`:192`), Phase 4 References bullet (`:338`), Run D (`:474`)
**Edge case:** The exact path this round's P1 fix created. `--rounds 3`, interview exits `round-cap`, operator picks option 2, §1.1 grants exactly one additional round.
**What happens:** §1.3 pins, verbatim, the line the operator reads at the bottom of every round: `Round <n> of <round_cap>.` On the granted round `n = round_cap + 1`, so the primitive prints `Round 4 of 3` — a bound the skill has just told the operator it is exceeding, on the interview's single most-repeated line and inside the fatigue mitigation the ticket exists to serve. The §1.8 header carries the same substitution (`rounds: 4/3`); there the `revised-after-cap (+1 round)` exit token partly explains it, but the per-round line has no such marker, and Phase 4's `Interview: 4 rounds, exit revised-after-cap (+1 round)` propagates `4` into the durable brief against a stated cap of 3. Checklist 4 asserts the round-end block is carried verbatim, and Run D asserts only the exit token — so the contradiction ships through the gate.
**Why the spec misses it:** the resume grant was written as budget arithmetic in §1.1 and §1.6 (both non-rendered sections); §1.3's literal block predates it and was last edited for a different reason (correctness/F-4's branch-letter fix at `:175`). No round-3 finding touched the two lines together.
**Suggested fix:** one substitution rule beside the literal block at `:176` — *"On the single post-cap resume round the last line reads `Round <round_cap>+1 of <round_cap> (post-cap revision round — the last).` instead."* — and one clause at §1.8 so the header renders `rounds: <n>/<round_cap>+1` on that exit. Add the substitution to checklist 4's verbatim list and one assertion to Run D.

---

### F-5: 2f-i's re-rendered red list is byte-identical to the pre-grill one — nothing marks which findings were just dispositioned
**Severity:** P3
**Where:** spec § Design 4 Edit 2 step 5 (`:409`), Edit 1 halt block (`:385–399`)
**Edge case:** Observability at the halt. The grill settles and applies decisions for, say, 3 of 6 remaining P0/P1s.
**What happens:** step 5 prints `grill applied: <s> findings dispositioned, <o> left open, <u> not grillable, <d> deferred to option 3` — counts only, no ids for the dispositioned set (the deferred set *does* get ids, and the not-grillable set gets a per-item line at step 1). Then it re-renders the 2f halt block, whose content is `<round 4 correctness P0/P1 titles>` read from reports the grill deliberately did not touch — so the operator sees the identical six titles they saw before running the grill, with a bare count above them. The one piece of state the operator needs to choose between option 1 (re-dispatch) and option 2 (ship by hand) is *which* findings are now addressed in the spec, and that is exactly what is withheld; recovering it means opening `grill.md`. Nothing breaks, which is why this is P3, but it undercuts the audit-trail rationale S8 gives for `grill.md` existing at all.
**Suggested fix:** name the ids in the summary line and mark the list — *"`grill applied: dispositioned <ids>; left open <ids>; not grillable <ids>; deferred to option 3 <ids>`, then the halt block with each dispositioned title suffixed ` — grilled (spec edited; not re-reviewed)`."* The suffix keeps the gate honest (the finding is still red) while showing what moved.

---

### F-6: Two concurrent `/spec-brief` runs on one ticket are undocumented, and the new unconditional stale-temp removal can delete a live run's in-flight write
**Severity:** P3
**Where:** spec § Design 3 Phase 0 step 2 (`:262`), Phase 4 (`:336`); § S8 (`:123`) by contrast
**Edge case:** Write-then-read race on the one persisted artifact this skill creates. Two sessions (parallel agents are normal in this ecosystem) run `/spec-brief VHS-40` against the same worktree.
**What happens:** two hazards, neither stated. (a) Both pass step 2's collision check (nothing exists yet), both interview, both write — last-writer-wins on the brief, with the losing operator's whole interview discarded and no signal. (b) The stale-temp removal added this round is unconditional on age: run B's step 2, arriving while run A is between temp-write and rename, sees "only the stale temp exists", deletes it, and continues without halting; run A's rename then fails and its own cleanup ("remove the temp file on any failure") finds nothing. The spec is scrupulous about this class elsewhere — S8 spells out `grill.md`'s last-writer-wins and declares two-session grilling out of the supported flow (Risk 14) — but the brief file, which is strictly more load-bearing, gets no such statement. My persistence checklist treats an undocumented concurrent-write outcome as a finding; the realistic probability here is low (both hazards need two humans answering two interviews for one ticket), which holds it at P3 rather than higher.
**Suggested fix:** one sentence beside Phase 4's atomic-write paragraph, mirroring S8's honesty — *"Two `/spec-brief` runs on the same ticket in one worktree are outside the supported flow: the collision check is not a lock, the brief is last-writer-wins, and step 2's stale-temp removal cannot distinguish an abandoned temp from a concurrent run's in-flight one."* — and add a Risk entry beside Risk 14.

---

### F-7: No gate row verifies the dry runs' emitted `ZZZ-1` / `ZZZ-2` artifacts were removed before commit
**Severity:** P3
**Where:** spec § Test plan procedure (`:469`), Runs A/B (`:471–472`), review checklist (`:455–467`)
**Edge case:** Test-fixture leakage. Runs A and B are authoring dry-runs executed inside the ship-spec worktree; each writes a real `docs/specs/TODO/ZZZ-<n>.brief.md` (plus, transiently, `.ZZZ-<n>.brief.md.tmp`).
**What happens:** the procedure states the intent — "the emitted briefs are deleted before commit and only the transcript is kept" — but the review checklist, which the spec itself calls "the gate for `/ship-spec`", has no row asserting it. Checklist 11 covers `agents/`, `skills/ship-spec/`, `skills/spec-close/`; nothing covers `docs/specs/TODO/`. Run C asserts `ZZZ-1.brief.md` does not exist, but only for the empty-seed run, which never writes one — so the assertion lands on the one run that cannot fail it while Runs A/B, which do write, are unasserted. A missed cleanup ships two throwaway briefs (and possibly a leaked dot-temp — precisely the artifact `:336` says must not be committed) into the lifecycle directory of a public repo.
**Suggested fix:** one checklist row — *"`git status --porcelain docs/specs/TODO/` shows no `ZZZ-*` path and no `.*.tmp`; `ls docs/specs/TODO/ZZZ-* .ZZZ-*` is empty."* — placed next to row 11.

---

### F-8: The `# Grill <k>` counter's operand is ambiguous against the `## Grill summary` line inside every appended block
**Severity:** P4
**Where:** spec § S8 (`:123`), § Design 4 Edit 2 step 3 (`:407`), § 1.8 (`:192`)
**Edge case:** Substring matching on the sole duplicate-detection mechanism. Each appended block contains both the caller's `# Grill <k> — …` header and, inside the verbatim summary, `## Grill summary — <seed title> …`.
**What happens:** the rule is "`<k>` = existing `# Grill` headers + 1". An implementer counting with an unanchored match (`grep -c '# Grill'`) counts both lines per block, so after one grill the next header is `# Grill 3`, then `# Grill 5`. Nothing breaks — the file is append-only and `/spec-close` copies it wholesale — but Risk 14 rests the entire after-the-fact duplicate story on this counter, and a sequence that skips numbers is exactly what an auditor would misread as a dropped block (the lost-update hazard S8 just accepted).
**Suggested fix:** pin the operand — *"`<k>` = the number of lines matching `^# Grill ` (anchored; the `## Grill summary` line inside each block is not one) + 1."*

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 3 | P4: 1

STATUS: GREEN
