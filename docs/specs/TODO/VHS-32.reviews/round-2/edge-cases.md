# Edge-Cases Review — round 2

Grounding complete. Read on disk: the v2 spec, the brief, both CLAUDE.md files, `AGENTS.md`, all three round-1 reports, `skills/spec-cycle/SKILL.md` (2e `:426`, 2f `:466–485`, 2g `:487`, 2c `:390–410`, gate `:415`, Phase 3 parser `:553–563`, Tool-use notes `:570`, Failure modes `:578`, stale-report backstop `:612–620`), `skills/spec-close/SKILL.md:28–45, :308–345`, `skills/ship-spec/SKILL.md:20,197,241`, `lint.py`, `docs/portability-contract.md`, `README.md`, `docs/spec-workflow-reference.md`. Plane VHS-32 not re-queried (brief carries the ticket body; namespace `skills`). All line anchors cited in § References verify.

## Closure of round 1 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 | docs cannot satisfy four-stage lifecycle (P0) | CLOSED | § Scope README/reference rows + Scope note; § Design 5 adds `## Skill 3: spec-close` and the README bullet; checklist 8 `grep -c 'spec-close'` ≥ 1. Verified both files are 0 today. |
| correctness | F-2 | D8 seed excludes scalability (P1) | CLOSED | § D8 "every remaining P0/P1 finding in the round-4 reports on disk … plus `scalability.md`"; § Design 4 Edit 1 adds the 4th `Remaining P0/P1` line. |
| correctness | F-3 | `--rounds 0` contradictory (P1) | CLOSED | § Design 3 Invocation: `1 ≤ N ≤ 10` / `1 ≤ N ≤ 15`, "there is no `0` alias"; Failure modes no longer lists it. |
| correctness | F-4 | "read-only by construction" over-claims `Explore` (P2) | CLOSED | § D1 Honesty note; § Risks 10. |
| correctness | F-5 | `user_invocable: false` asserted to suppress the slash command (P2) | CLOSED | § D9 "advisory"; § Design 1 frontmatter note; checklist 10 treats a visible `/grilling` as documented, not a blocker. |
| correctness | F-6 | Tool-use notes bold vs heading (P2) | CLOSED | § Design 3 "(A real `## Tool-use notes` heading…)"; § Design 6 bullet keyed to `lint.py:57,216–217`; checklist 9. Verified `_NOTES_HEADING_RE` matches. |
| correctness | F-7 | `facts_policy` dead parameter (P2) | CLOSED | Removed from § 1.1 inputs; S5 states "There is no caller-side `facts_policy` switch". |
| correctness | F-8 | three stale line anchors (P2) | CLOSED | Re-verified on disk: 2f `:466–485`, Tool-use notes `:570`, Failure modes `:578`, 2e `:426`, 2g `:487`, gate `:415`, AGENTS.md `:23–29`, swr `:162`, README `:7–11`/`:54–59` all correct. |
| correctness | F-9 | transcripts unproducible as described (P2) | CLOSED | § Test plan "Procedure" (authoring dry-run, `ZZZ-1`, delete before commit); § Deferred records the manual PR-body link. |
| correctness | F-10 | `subagents: true` forecloses S5 degradation (P2) | CLOSED (accepted) | S5 "Contract limitation, recorded not fixed"; § Risks 9. Deliberate direction with rationale. |
| correctness | F-11 | explicit "scale not a factor" discarded (P3) | CLOSED | § Design 3 Phase 4 three-state rule, state 3 emits `**Factor:** no`. |
| correctness | F-12 | under-specified argument/confirm branches (P3) | CLOSED | § Design 3 Invocation usage halt; Phase 3 option-2 and `--no-grill` variants. |
| edge-cases | F-1 | same root as correctness/F-1 (P0) | CLOSED | as above. |
| edge-cases | F-2 | empty seed writes hollow brief (P1) | CLOSED | § S9; Phase 0 step 5c; Phase 1 step 1; Phase 2 halt; § 1.2 / 1.7 `empty-seed`; Run C. |
| edge-cases | F-3 | exploration hang/crash stalls the interview (P1) | **PARTIAL** | § 1.5 adds the dispatch cap and the error/empty/no-fact rule, but the hang case is qualified "(where the host reports it) times out" while the same sentence asserts "a failed exploration never blocks a round". No host-independent bound and no accepted-limitation record. See F-2 below. |
| edge-cases | F-4 | fact requests uncapped (P1) | CLOSED | § S5 "Fact requests count against the per-round cap"; § D6 and § 1.6 restate it. |
| edge-cases | F-5 | revise: no invalidation / budget / addressing (P1) | CLOSED | § S7 revise bullet (downstream return to frontier, `revised-after-cap`); § S1 monotonic `Q1…Qn`; Phase 3 option 2. (New residual: re-selection is unbounded — F-6 below.) |
| edge-cases | F-6 | overwrite guard + non-atomic write (P1) | CLOSED | Phase 0 step 2 fenced halt over brief/spec/reviews with git-status column; Phase 4 tmp-then-rename. |
| edge-cases | F-7 | scale factor without target (P1) | CLOSED | Phase 4 "## Scale emission" three-state rule incl. the Risks item and the `warning:` line. |
| edge-cases | F-8 | host cannot invoke nested skill (P1) | CLOSED | Point-of-use halts in § Design 2, § Design 3 Phase 2 + Failure modes, § Design 4 step 2; § Design 6 bullet; § Risks 9. |
| edge-cases | F-9 | flag validation / `--no-grill` interaction (P2) | CLOSED | § Design 3 Invocation ranges, usage halt, `--no-grill` wins + warn. |
| edge-cases | F-10 | 2f-i missing report / synthetic P0 (P2) | CLOSED | § Design 4 Edit 2 step 1 "Not grillable" rule + step 5 line. (Exposes a new empty-seed hole — F-1 below.) |
| edge-cases | F-11 | `grill.md` overwritten (P2) | CLOSED | § S8 append-only with `---` separator and dated header; step 3 "Never overwrite". |
| edge-cases | F-12 | `--no-grill` derivation unruled (P2) | CLOSED | Phase 3 `--no-grill` paragraph (explicit-statement-only + quote/`path:line`, fence applies); `Interview: skipped (--no-grill)`. |
| edge-cases | F-13 | defer expands Open by an unshown subtree (P2) | CLOSED | § S7 rolled-up item; § 1.8 by-construction bound `round_cap × question_cap`. |
| edge-cases | F-14 | `subagents: true` unconditional (P2) | CLOSED (accepted) | S5 contract-limitation note; § Risks 9; README Requirements now names the real capability. |
| edge-cases | F-15 | free-form / partial / `stop`-in-flight (P2) | CLOSED | § S7 free-form + omitted bullets; § 1.7 `stop` rule (settle answered, abandon in-flight, `unresolved because: stopped`). |
| edge-cases | F-16 | `user_invocable: false` unprecedented (P3) | CLOSED | § Design 1.0 guard sentence; § Risks 11; checklist 5. Verified: all eight shipped skills are `true`. |
| conventions | F-1 | same root as correctness/F-1 (P0) | CLOSED | as above. |
| conventions | F-2 | halt hardcodes three lenses (P2) | CLOSED | § Design 4 Edit 1 scalability line. |
| conventions | F-3 | `states.json` path (P2) | CLOSED | Phase 0 step 3 uses the `<config-dir>` / `$CLAUDE_CONFIG_DIR` resolution, cited to `spec-close:31`. |
| conventions | F-4 | Phase 0 reads `AGENTS.md` first (P2) | CLOSED | Phase 0 step 1 reads `<project_root>/CLAUDE.md` with the `AGENTS.md` pointer parenthetical. |
| conventions | F-5 | no origin-sync preflight (P2) | CLOSED | Phase 0 step 4, warn-only, `spec-close:37–42` shape. (Residual: the durable Scope claim — F-7 below.) |
| conventions | F-6 | `user_invocable` informational on Hermes (P2) | CLOSED | § D9, § Design 1 note, § Risks 11. |
| conventions | F-7 | description trigger competition (P2) | CLOSED | § Design 1 "carries **no** user-phrase triggers"; checklist 5 greps for the three phrases. |
| conventions | F-8 | `--rounds 0` dual meaning (P2) | CLOSED | as correctness/F-3. |
| conventions | F-9 | S6–S8 mislabelled as brief-deferred forks (P3) | CLOSED | § Decisions preamble now splits S1–S5 (brief-deferred) from S6–S9 (spec additions). |
| conventions | F-10 | `·`-separated inline menu idiom (P3) | CLOSED | Phase 0 step 2 and Phase 3 both use fenced one-per-line menus + "Wait for the user's response." |
| conventions | F-11 | `AGENTS.md` anchor overshoot (P4) | CLOSED | § Scope now `:23–29`; verified line 29 is the `/spec-close` item. |
| conventions | F-12 | README Requirements implies Python dependency (P4) | CLOSED | § Design 5 line now reads "no external services required … a harness that can dispatch a read-restricted subagent". |

Eleven of twelve round-1 P0/P1s close cleanly; the manifest's claim for edge-cases/F-3 is only partly borne out.

## Findings

### F-1: `empty-seed` has no branch at two of the three call sites, and 2f-i's write instruction directly contradicts S9 on a path 2f-i exists to serve
**Severity:** P1
**Where:** spec § S9 (`:125–127`), § Design 4 Edit 2 steps 1–3 (`:397–399`), § Design 2 (`:225`)
**Edge case:** Empty input to the primitive, produced by the spec's *own* new exclusion rule. Step 1 excludes from the seed "a report that is missing or unparseable, and any synthetic `missing STATUS line` P0". Reaching the 2f halt with *only* those is a documented `/spec-cycle` state: a crashed standing lens is scored `STATUS: RED P0=1 P1=0` (`spec-cycle:578`) and a vanished scalability reviewer gets a stub with the same shape (`:402–410`). If both remaining P0s are dispatch failures, the exclusion empties the seed.
**What happens:** Step 2 invokes `grilling` with an empty seed. Per § 1.2 and § S9 the primitive exits `empty-seed` at once and returns "the token and a one-line reason" — explicitly *not* the § 1.8 Grill summary block. Step 3 then says, unconditionally, "Append the returned Grill summary verbatim to … `round-4/grill.md`, preceded by `---` … and by a header line". S9 says the opposite: "callers treat `empty-seed` as a halt and **never write on it**." The implementer has two contradictory instructions on the same reachable path. Either outcome is bad: a `# Grill — … findings: <ids>` header with no body is appended into the append-only audit file `/spec-close` archives to `DONE/` (an audit record asserting a grill happened when none did), or the run stalls with no defined next step. Step 5's counters (`<s>/<o>/<u>`) are also undefined for this shape.

Same gap, harmless variant, at the third call site: `/grill-me` (§ Design 2) says "the Grill summary is the deliverable" with no `empty-seed` branch — a user who types `/grill-me` with no topic gets an undefined response. Only `/spec-brief` Phase 2 handles the token.
**Why the spec misses it:** S9 was written for the `/spec-brief` seed gate and generalized to "callers" in one clause; § Design 4 was written before S9 existed and step 1's exclusion rule (added this round to close edge-cases/F-10) is precisely what makes an empty 2f-i seed reachable. The two new rules were not composed. Checklist 7 greps 2f-i for five strings, none of which is `empty-seed`.
**Suggested fix:** Add to § Design 4 Edit 2 step 1: *"If the seed is empty after exclusions, do not invoke the grill: print `nothing grillable — <lens>/<id> …; option 1 re-dispatches those lenses.` and re-render the menu with options 1–3. Nothing is appended to `grill.md`, and option 4 is not consumed."* Add one sentence to § Design 2: *"On `empty-seed`, report the primitive's one-line reason and stop — there is no summary to deliver."* Add `empty-seed` to checklist 7's grep list.

---

### F-2: An exploration that never returns still blocks the round on any host that reports no timeout — including the reference host — while § 1.5 asserts it cannot
**Severity:** P1
**Where:** spec § Design 1.5 (`:182`), § Design 3 Phase 1 step 4 (`:290`) and § Failure modes (`:367`), § Risks
**Edge case:** External-system failure — a dispatched read-restricted exploration hangs (a runaway repo-wide search, a wedged shell, a model stall) rather than erroring or returning empty. Round-1 edge-cases/F-3, re-verified against v2.
**What happens:** § 1.5 now reads: "A dispatch that errors, returns empty, returns without the fact, or **(where the host reports it)** times out is a **failed dispatch** … the round renders without it — a failed exploration never blocks a round." The parenthetical narrows the *hang* trigger to hosts that surface a timeout; the closing clause then asserts the guarantee unconditionally. On Claude Code — the host every binding in this spec is written against — a pending subagent call does not surface a timeout to the orchestrating model, so a hung dispatch is never classified as failed. Because § 1.5 also requires the batch to complete "**before** rendering the round", the operator sees no questions, no `ℹ️` line, and no error; and because § Out of scope pins "no resume state is kept", killing the session at round 3 of 3 discards every settled decision. The spec's own preflight observability line (`grounding: <n> files read, <m> explorations dispatched (<f> failed)`) is printed *after* the batch, so it cannot fire either.
**Why the spec misses it:** v2 closed the two failure shapes a returning agent can have (error, empty/no-fact) and the fan-out width (`capped at question_cap dispatches`), but treated "does not return" as the same class rather than as the one shape a prompt-level skill genuinely cannot recover from. `/spec-cycle` faces the identical exposure and handles it honestly at `:402–410` by writing a stub so the gate still has a summand; the new primitive states a stronger guarantee than its mechanism delivers, and § Risks — which records four other accepted limitations of exactly this kind (Risks 8–11) — has no entry for it.
**Suggested fix:** Two cheap edits, no new machinery. (1) Soften § 1.5's guarantee to what the mechanism supports: *"A dispatch that errors, returns empty, or returns without the fact is a failed dispatch … Where the host reports a timeout, treat it identically. Where it does not, a hung dispatch blocks the round — see § Risks."* (2) Add § Risks 12: *"A hung exploration blocks the round it belongs to, and no resume state exists to recover the interview behind it. Accepted: no prompt-level construct can cancel a pending dispatch. Mitigations: the per-round dispatch cap bounds how many can hang, and every dispatch prompt bounds its own work — 'answer from the paths named in the question; return `not found` rather than searching exhaustively.'"* Add that bounding clause to the D2 sentence so it ships in the skill body, and a matching `## Failure modes` bullet in `/spec-brief`.

---

### F-3: `--no-grill` can never emit `## Scale`, so a brief written on that path silently disables the scalability lens even when the ticket declares a target
**Severity:** P2
**Where:** spec § Design 3 Phase 4 "`## Scale` emission" (`:335–339`), Phase 3 `--no-grill` paragraph (`:309`)
**Edge case:** Configuration flag interacts with a conditional emission rule. Operator runs `/spec-brief VHS-40 --no-grill` on a ticket whose text says "must hold at 10k tenants".
**What happens:** All three emitting states are conditioned on "a settled decision" from the interview; the fourth state is "Never asked → no section." Under `--no-grill` the interview is "Skipped entirely" (Phase 2), so nothing is ever settled and nothing is ever asked — the fourth state always applies. The ticket's scale statement is instead derived by Phase 3's `--no-grill` rule into `## Decisions carried forward` as prose. `/spec-cycle` Phase 0 step 8 detects scale *only* via the `^#{1,6}\s+scal(e|ing)\s*$` heading (verified `:238–250`); prose in Decisions is invisible to it. The scalability reviewer never runs, `scale_lens` resolves `off`, and Phase 3's drift check renders no Scale block — the fourth lens is dropped with no warning anywhere. This is the same silent-drop class the spec just closed for the target-less case (edge-cases/F-7), reached through the other door.
**Why the spec misses it:** the three-state rule was written as a fix to the *interview* path and the `--no-grill` derivation rule was written separately in Phase 3; neither section mentions the other, and § Test plan has no `--no-grill` run.
**Suggested fix:** Add a fifth line to the `## Scale` emission rule: *"Under `--no-grill`, apply the same three states to a scale declaration stated explicitly in the ticket text (factor + target → emit; factor without target → no section, Risks item, warning). If the ticket says nothing about scale, emit no section."* Optionally add a `--no-grill` row to the checklist.

---

### F-4: A grounding exploration that fails under `--no-grill` has nowhere to land — the fact is dropped silently
**Severity:** P2
**Where:** spec § Design 3 Phase 1 step 4 (`:290`), § Failure modes (`:367`), Phase 2 (`:296`)
**Edge case:** External-system failure combined with the skip flag. Phase 1 grounding is not gated on `--no-grill`, so dispatches still happen; Phase 2 is.
**What happens:** Step 4's rule is "A failed dispatch (error, empty, no fact) becomes a fact request in **the interview's first round**", and § Failure modes repeats "Exploration dispatch fails → fact request in round 1; never blocks." Under `--no-grill` there is no round 1. The fact need is simply lost: it does not reach `## Risks / decisions`, it is not named in `## References`, and the only trace is the `(<f> failed)` counter in a transient console line. The brief is then written carrying a `## Scope (verified against current files, <date>)` header over a gap the skill knew about. Every downstream lens reads that brief as authority.
**Why the spec misses it:** the failed-dispatch rule was added this round to close edge-cases/F-3 and routes to the interview by construction; `--no-grill`'s Phase-2 skip was pinned in D9 long before. The two paths never meet in the text.
**Suggested fix:** Extend step 4 and the Failure-modes bullet: *"…becomes a fact request in the interview's first round. Under `--no-grill`, it becomes a `## Risks / decisions` item instead — `<fact needed> — not established (exploration failed); spec author pins this`."*

---

### F-5: The per-round fact-*dispatch* cap has no overflow rule, unlike the rendered-item cap it mirrors
**Severity:** P2
**Where:** spec § Design 1.5 (`:182`), § S1 (`:81`), § 1.8 (`:197`)
**Edge case:** Size limit. A round's frontier needs more facts than `question_cap` — e.g. `--questions 3` with five frontier questions each needing a repo fact.
**What happens:** S1 gives the *rendered* cap an explicit overflow rule ("overflow is carried to the next round") and an ordering. § 1.5 gives the dispatch batch a cap — "one parallel batch, capped at `question_cap` dispatches" — and no overflow rule, no ordering, and no disposition for the fact needs that do not fit. Their dependent questions are, per D3, "downstream of a fact" and therefore wait; with nothing that ever re-dispatches them, they wait forever and reach § 1.8's Open frontier with no matching `unresolved because:` value (the enumerated set is `round-cap | deferred | stopped | fact not established | blocked-on: Q<m>`, none of which describes "never dispatched"). Either the implementer invents a value or the questions vanish from the hand-off — and the hand-off is what becomes `## Risks / decisions`, the record of what the brief does *not* settle.
**Why the spec misses it:** the dispatch cap was added this round as fix (b) of edge-cases/F-3 and borrowed `question_cap`'s number without borrowing S1's overflow discipline, which is written one section away and scoped explicitly to "rendered items".
**Suggested fix:** One sentence in § 1.5: *"Fact needs beyond the dispatch cap carry to the next round's batch by the S1 ordering; if the interview ends first, they reach the hand-off as Open with `unresolved because: fact not established`."*

---

### F-6: Phase 3 option 2 can be re-selected without limit after `revised-after-cap`, so the round cap is defeatable at the confirm prompt
**Severity:** P2
**Where:** spec § S7 revise bullet (`:117`), § Design 3 Phase 3 (`:305`), § S8 (`:121–123`)
**Edge case:** Re-entrancy at the confirm loop. The operator picks option 2 repeatedly.
**What happens:** S7 states "If the round budget is exhausted, exactly one revision round is granted and the exit token becomes `revised-after-cap`" — unconditionally, with no per-invocation limit. After that round the budget is exhausted again, the operator is returned to the same confirm prompt, and picking 2 again satisfies the rule again. Nothing in S7, Phase 3, or § 1.6 says the grant is single-use. Rounds accumulate past `round_cap` one at a time, defeating the bound that is the ticket's entire premise (brief Risk 1: "Interview fatigue is the failure mode that kills this") — and the recorded exit token stays `revised-after-cap`, so the brief's `Interview: <n> rounds, exit <token>` References bullet cannot distinguish one extra round from six. The author already had the idiom for this: S8 pins 2f-i's option 4 to "once per `/spec-cycle` invocation" and re-renders the menu without it.
**Why the spec misses it:** S7's revise bullet was added this round to close edge-cases/F-5, which asked about *invalidation* and *addressing*; the budget clause was written as the answer to "does a revision have any budget at all", not as a bound on repetition.
**Suggested fix:** Mirror S8: *"The post-cap revision round is granted at most once per invocation. After it, option 2 is no longer offered and the confirm re-renders with options 1 and 3 only."* State the count in the exit record — `exit revised-after-cap (+1 round)`.

---

### F-7: The origin-behind warning is transient, but Phase 4 still writes the durable "verified against current files" claim unqualified
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 Phase 0 step 4 (`:275`), Phase 4 section list (`:323`)
**Edge case:** Runtime precondition violation the skill already detects. Local `main` is 12 commits behind `origin/main`; grounding reads the stale tree.
**What happens:** Step 4 prints, correctly, `ORIGIN SYNC: local <branch> is <N> commits behind … the brief's "verified against current files" claim may be stale.` Then Phase 4 writes the header `## Scope (verified against current files, <date>)` with today's date and no qualification. The warning lives in console scrollback that ends with the session; the false claim lives in the artifact that every reviewer lens, `/spec-cycle`'s drift check, and `/spec-close`'s reconciliation treat as authority — and `/spec-close`'s own origin check (`spec-close:37–42`) exists precisely because stale-tree reads produce wrong conclusions. The skill knows the claim is suspect at the moment it writes it and records nothing.
**Why the spec misses it:** the origin check was added this round from conventions/F-5, whose ask was "add a preflight". The interaction with the Scope header's verification claim — the reason conventions/F-5 raised it — was not carried into Phase 4's mapping rules.
**Suggested fix:** In Phase 4, one line: *"When the preflight logged `origin: behind-N`, the Scope header reads `## Scope (verified against current files, <date>; local tree <N> commits behind origin/<cmp>)` and a `## References` bullet records the same."* Pure annotation — inside 2g's clarification limits.

---

### F-8: `grill.md` is append-only with no atomicity, no dedup key, and no durable record of the "once per invocation" bound
**Severity:** P2
**Where:** spec § Design 4 Edit 2 step 3 (`:399`), § S8 (`:121–123`), § Done when 6
**Edge case:** Persistence checklist — a new persisted artifact that survives process restart and is archived to `DONE/` by `/spec-close` (`spec-close:339–340`, verified).
**What happens:** Walking the checklist against step 3: (1) **Atomicity** — Phase 4 of `/spec-brief` earned a tmp-then-rename discipline this round; the `grill.md` append got none, so a kill mid-append leaves a truncated Grill summary inside the audit file, and there is no `status`/completeness marker for a reader to tell a truncated block from a complete one. (2) **Idempotency on retry** — the header `# Grill — <TICKET-ID> round 4 — <date> — findings: <ids>` is the only discriminator; a second grill on the same day over the same finding set produces a byte-identical header, so a retry after a partial append is indistinguishable from a legitimate second grill, and neither the implementer nor `/spec-close` can dedup. (3) **Concurrency** — `/spec-cycle` explicitly supports "separate invocations sharing a reviews tree" (`:612–620`, verified), so two sessions on the same ticket can interleave appends to one file with last-writer-wins undocumented. (4) **The bound is not durable** — S8's "once per `/spec-cycle` invocation" lives only in model context; after a compaction or a session boundary at the halt, nothing on disk says option 4 was already used, while `grill.md`'s presence is exactly the signal that would.
**Why the spec misses it:** S8 was written this round to close edge-cases/F-11, whose ask was "never overwrite". Append-only fixed the overwrite; the write discipline around the append was not revisited, and the atomicity rule added for the brief in the same revision was not generalized.
**Suggested fix:** In step 3: append via read-modify-tmp-rename (the same discipline Phase 4 uses), give the header a unique suffix (`— grill <k>` where `k` counts existing `# Grill —` headers in the file), and state last-writer-wins for the concurrent case. In S8, key the "once" bound to a durable signal: *"If `grill.md` already contains a `# Grill —` header for this round dated today, option 4 has run in this session — re-render with 1–3."*

---

### F-9: `## Scale` has no defined position in Phase 4's otherwise-exact section order
**Severity:** P3
**Where:** spec § Design 3 Phase 4 (`:313–329`, `:335–339`)
**Edge case:** Malformed-artifact adjacency. Phase 4 gives a fenced list of eight headers "in this order and with these headers (the `/spec-cycle` Phase 3 parser keys on three of them)" — verified accurate: `Decisions carried forward`, `Done when`, `Out of scope` (`spec-cycle:553–557`). The conditional `## Scale` section appears in a separate rule two paragraphs later with no stated position.
**What happens:** No functional break today — `/spec-cycle` Phase 0 step 8 matches the first line satisfying `^#{1,6}\s+scal(e|ing)\s*$` anywhere in the file. But an implementer following "in this order and with these headers" literally has no slot for it, and two `/spec-brief` runs can legitimately place it differently, which then diverges from every hand-written brief in `DONE/`.
**Suggested fix:** Name the slot in the fenced list: `## Out of scope` / `## Scale` *(conditional — see below)* / `## Risks / decisions` / `## References`.

---

### F-10: S9's "re-prompt once" is mechanized only for conversation-only mode; Phase 1 step 1 invokes it with no defined prompt
**Severity:** P3
**Where:** spec § S9 (`:125–127`), § Design 3 Phase 0 step 5c (`:279`), Phase 1 step 1 (`:287`)
**Edge case:** A ticket resolves successfully from memory or the tracker but its body is a bare title ("Fix the brief thing") — the common shape for a ticket filed from a phone.
**What happens:** Phase 1 step 1 says "Apply the S9 seed gate here too when the ticket text itself is empty or a bare title." S9's mechanism is "it re-prompts once, then halts", written for step 5c where there is a paragraph to re-request. In tracker mode there is nothing to re-prompt *for*: the ticket text will not change on a second read. The implementer must invent either a no-op re-prompt (halt immediately, contradicting "re-prompts once") or an ad-hoc "describe the problem" prompt — which is step 5c's conversation-only prompt, whose downstream consequence is a header line (`**Plane:** <ID> (<uuid>, <state>)` vs `unresolved (local-only)`) the spec does not address for the mixed case.
**Suggested fix:** State it once in S9: *"In ticket mode the re-prompt is step 5c's: print `Ticket <ID> states no problem — describe it in a paragraph and I will proceed from that.` and wait. The brief header keeps the resolved ticket line; the paragraph becomes the seed. A second empty answer halts."*

---

### F-11: A leaked `<TICKET-ID>.brief.md.tmp` is invisible to the artifacts-exist check and would be archived by `/spec-close` as a companion
**Severity:** P3
**Where:** spec § Design 3 Phase 4 (`:331`), Phase 0 step 2 (`:259`)
**Edge case:** Partial failure of the new atomic-write discipline. Phase 4 writes to a temp sibling and renames, and says "remove the temp file on any failure" — but a kill between create and cleanup leaves it.
**What happens:** Phase 0 step 2's collision check inspects `<TICKET-ID>.brief.md`, `<TICKET-ID>.spec.md`, `<TICKET-ID>.reviews/` — not the `.tmp`. A re-run therefore never reports it and silently overwrites it. If the ticket later closes, `/spec-close`'s archive rule "any other companion `<TICKET-ID>.<rest>` → `<rest>`" (verified `skills/spec-close/SKILL.md:340`) sweeps `VHS-40.brief.md.tmp` into `DONE/VHS-40/brief.md.tmp` — a half-written brief permanently filed next to the real one.
**Suggested fix:** In Phase 4, name the temp file outside the archived pattern (a dotfile, `.<TICKET-ID>.brief.md.tmp`), and add to Phase 0 step 2: *"A stale `<TICKET-ID>.brief.md.tmp` from an interrupted run is reported in the halt block and removed on option 1."*

---

### F-12: The artifacts-exist halt's option 1 is worded for a branch that may not hold
**Severity:** P3
**Where:** spec § Design 3 Phase 0 step 2 (`:259–273`)
**Edge case:** The block's own `<path | none>` placeholders admit `brief: none` with `spec:` and `reviews:` present — reachable when a brief was deleted, was never committed, or the spec was hand-written.
**What happens:** The halt fires (correctly — the spec and reviews are the thing at risk), but option 1 reads "Overwrite the brief (**the existing brief is read as grounding first**)" when there is no existing brief to read. The operator is offered a guarantee the skill cannot honor, and the implementer has no rule for grounding on that branch — the natural fallback (ground on the *spec* instead) is not stated and would quietly invert the lifecycle's authority direction.
**Suggested fix:** Make the option conditional: *"1. Write the brief (if one exists, it is read as grounding first; if only a spec and reviews exist, the brief is written fresh — the spec is **not** read as grounding, or the brief would inherit the artifact it is meant to authorize)."*

---

### F-13: An interview that settles nothing writes an empty `## Decisions carried forward`, which `/spec-cycle`'s drift check treats as present-and-satisfied
**Severity:** P3
**Where:** spec § Design 3 Phase 4 mapping rules (`:333`), § S2 (`:83–85`)
**Edge case:** Every rendered question is deferred, or `--questions 1 --rounds 1` with one `defer`. The seed gate passes (the seed was fine); the *outcome* is empty.
**What happens:** Phase 4 writes the header with no items. `/spec-cycle` Phase 3's parser (verified `:558–560`) renders its "Did the spec address everything in the brief?" fallback bullet **only when the header is missing** — a present-but-empty header enumerates nothing and prints a bare `Decisions carried in brief:` label. The drift check that exists to catch exactly this silently passes. S2's confirm is a real guard (the operator sees the empty preview and chose it), which is why this is P3 rather than higher — but the artifact carries no marker distinguishing "no decisions were settled" from "no decisions were needed".
**Suggested fix:** In Phase 4: *"If Settled is empty, write `_(none settled — see `## Risks / decisions`)_` under the header rather than leaving it blank, and print `warning: interview settled no decisions — the brief pins everything to the spec author`."*

## Summary
P0: 0 | P1: 2 | P2: 6 | P3: 5 | P4: 0

STATUS: RED P0=0 P1=2 P2=6 P3=5 P4=0
