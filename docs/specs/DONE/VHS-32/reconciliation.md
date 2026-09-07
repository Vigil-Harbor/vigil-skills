# Reconciliation Report: VHS-32

> Date: 2026-09-06
> Spec: docs/specs/TODO/VHS-32.spec.md
> Merge: PR #26 (d381f88)
> Plane state: Done (group: completed)

## Summary
PR #26 shipped every file the spec's Scope table names and nothing else; the three new skills carry the spec's verbatim contract lines, and the `/spec-cycle` edit is confined to the five expected hunks with 2e/2g byte-identical. The only departure from the spec is the corrected `/spec-cycle` Failure-modes text plus a step-3 guard (test-output DEVIATIONS 1b/1c, raised by CodeRabbit) — recorded against S8 as the sole drift; the extra `docs/spec-workflow-reference.md` step-8 edit (DEVIATIONS 1) and the scratch-dir `sync.py` run (DEVIATIONS 2) are stated and do not count.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/grilling/SKILL.md` (new) | Yes | 151 lines; `user_invocable: false`, `requires: subagents: true, filesystem: [read]` (`:4–7`). |
| `skills/grill-me/SKILL.md` (new) | Yes | 21 lines; `user_invocable: true`, `requires:` mirrors the primitive (`:4–7`). |
| `skills/spec-brief/SKILL.md` (new) | Yes | 189 lines; `requires: shell, filesystem [read, write], network, subagents, services: [issue-tracker?, shared-memory?]` (`:5–10`). |
| `skills/spec-cycle/SKILL.md` § 2f + new § 2f-i | Yes | Hunks at `:475`, `:484`, `:487–561`; 2e and 2g byte-identical vs e193b8e (re-verified this pass). 1b/1c corrections inside the pinned text — see S8. |
| `skills/spec-cycle/SKILL.md` § Tool-use notes / § Failure modes | Yes | One Tool-use bullet (`:652`); Failure-modes bullet split into two (`:698–708`) per DEVIATIONS 1b. |
| `AGENTS.md` § Workflow + § Superseded vendor skills | Yes | Four-item lifecycle (`:23–31`); collision paragraph, not a bullet (`:84–89`); "Two warnings:" list untouched (`:70`). |
| `docs/spec-workflow-reference.md` (`:3`, before `:7`, after `:161`) | Yes | Intro (`:3`), `## Skill 0: spec-brief` + `### The grilling contract` (`:7–35`), `## Skill 3: spec-close` (`:194`). **Added edit** at `:86` (Phase 2 step 8 now names the fourth option) = DEVIATIONS 1 — stated reason: the three-option menu would contradict the grilling-contract subsection two sections above it. |
| `README.md` tagline, § Skills, § Requirements | Yes | `:3`, `:9`, `:12`, `:13`, `:16`, `:63–64`. |
| `docs/specs/TODO/VHS-32.test-output.txt` | Yes | Spec-stated companion (spec `:470`: "captured into `docs/specs/TODO/VHS-32.test-output.txt`"); not unexpected. |

Unexpected files in diff (not in spec):
- none

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| D1 | Read-restricted exploration on the strongest model, never general-purpose | Confirmed | `skills/grilling/SKILL.md:70 — 'never a general-purpose agent, which inherits the full session tool set'`; `:142 — 'Claude Code: `Explore`, dispatched with an Opus model override) — the only dispatch this skill makes'` |
| D2 | Binding as portable intent; Claude Code form is a parenthetical | Confirmed | `skills/grilling/SKILL.md:70 — '(Claude Code: the `Explore` subagent type with an Opus model override, or the equivalent narrowest read-only agent class in your host)'`; echoed `skills/spec-brief/SKILL.md:78`; no `model:` in any new file (test-output `:53–57`) |
| D3 | Facts are the agent's job; decisions are the operator's | Confirmed | `skills/grilling/SKILL.md:74 — 'Questions downstream of a fact wait for it; the rest of the frontier is asked in the current round'`; `:138 — 'answers a decision on the operator's behalf'` (never-list) |
| D4 | Forks stated as weighed forks; recommendation advisory | Confirmed | `skills/grilling/SKILL.md:40–43 — '**A.** <branch> — *For:* <…>  *Against:* <…>' … '➡️ **Recommend B**'`; `:61 — 'The recommendation is advisory. It is never a default that carries by silence'` |
| D5 | Ask the whole frontier in one round, then wait | Confirmed | `skills/grilling/SKILL.md:29 — 'Each round asks the whole frontier, capped … never drip-feed one question at a time'` |
| D6 | Three bounds: round cap 3, question cap 7, altitude fence | Confirmed | `skills/grilling/SKILL.md:82–86 — 'Three bounds, and nothing else, end the interview: 1. **Round cap** — default 3 … 2. **Per-round question cap** — default 7 … 3. **Altitude fence**'`; `skills/spec-brief/SKILL.md:28 — '`--rounds N`: integer, `1 ≤ N ≤ 10`. `--questions N`: integer, `1 ≤ N ≤ 15`'` |
| D7 | Hitting a cap is a documented outcome, not a failure | Confirmed | `skills/grilling/SKILL.md:112 — 'Reaching a cap is a documented outcome, not a failure; the caller decides what to do with the open frontier.'`; `skills/spec-brief/SKILL.md:140 — 'Open frontier items → `## Risks / decisions`, numbered, each ending "spec author pins this"'` |
| D8 | 2f grill scoped to named findings; cannot patch; routes through 2e | Confirmed | `skills/spec-cycle/SKILL.md:484 — '4. Grill the remaining findings — a bounded interview scoped to the titles above; decisions route through 2e revise (see 2f-i)'`; `:539–540 — 'edit the spec in place under the 2e rounds-1–3 rules'`; `:556–557 — '2f-i never re-dispatches reviewers, never increments the round counter'`; `skills/grilling/SKILL.md:7 — 'filesystem: [read]'` |
| D9 | Grilling is never auto-invoked | Confirmed | `skills/grilling/SKILL.md:3 — 'Not a user-facing entry point — invoked only by /grill-me, /spec-brief, and /spec-cycle's post-round-4 halt (option 4)'`; `:4 — 'user_invocable: false'`; `:12 — 'This skill is invoked only by `/grill-me`, `/spec-brief`, or `/spec-cycle` 2f-i. If you reached it any other way, stop'`; `skills/spec-cycle/SKILL.md:652 — 'only from 2f-i, only after the operator picks option 4'` |
| D10 | Clean-room, not a port; idea attributed to mattpocock/skills | Confirmed | `skills/grilling/SKILL.md:27 — 'adapted from the `grilling` skill in `mattpocock/skills` (MIT); the text here is original'`; `AGENTS.md:85 — 'share directory names with `mattpocock/skills`'` |
| S1 | Question cap is a hard truncation; monotonic numbering | Confirmed | `skills/grilling/SKILL.md:85 — 'This is a hard truncation, not a soft target. **Ordering** when truncating: carried-over and re-asked items first, then shallowest tree depth'`; `:48 — '`Q1…Qn` never resets between rounds'` |
| S2 | `/spec-brief` confirms before writing, even on an empty frontier | Confirmed | `skills/spec-brief/SKILL.md:97–100 — 'Write the brief? 1. Write … 2. Revise an answer … 3. Abort'`; `:19 — '--no-grill  # skip the interview; still confirms before writing'`; Run A test-output `:379–384` |
| S3 | Test for "genuinely branches" (two or three candidates, (a)+(b)) | Confirmed | `skills/grilling/SKILL.md:90 — 'Render a question in fork form when **two or three** candidate answers each (a) are consistent with every decision already settled … and (b) would produce a *different* line'` |
| S4 | Altitude-fence worked examples verbatim | Confirmed | `skills/grilling/SKILL.md:94–98 — table row 1 'Should the origin-sync check offer a fast-forward, or only warn?'`; test-output `:72` (grep count 1) |
| S5 | Degrade to fact requests when no read-restricted class; fact requests share the cap | Confirmed | `skills/grilling/SKILL.md:72 — 'If none exists, do **not** dispatch a write-capable agent: render every fact need as a fact request'`; `:85 — 'questions and fact requests together'`; `:88 — 'A fact request the operator leaves unanswered twice becomes an Open item'` |
| S6 | `grill-me` mirrors the primitive's `requires:` | Confirmed | `skills/grill-me/SKILL.md:5–7 — 'requires: subagents: true / filesystem: [read]'`; `:16 — 'mirrors `grilling`'s: it declares what the delegate needs, so pre-flight is honest'` |
| S7 | defer / omitted / free-form / revise rules | Confirmed | `skills/grilling/SKILL.md:63–66 — '**`defer`** … **Omitted** … **Free-form** … **Revise**'`; `skills/spec-brief/SKILL.md:105 — 'offers option 2 at most once after a cap hit … re-renders with options 1 and 3 only'`; `:107 — '2. Add a decision (state it)'`; Run D test-output `:561–577` |
| S8 | 2f-i once per halt; `grill.md` append-only | Drifted | Core pin shipped: `skills/spec-cycle/SKILL.md:524–530 — 'preceded by `---` if the file already exists … Never overwrite an existing `grill.md`'`; `:558 — 'runs at most once per invocation'`; `:487 — 'then re-renders this menu without option 4'`. **Drift:** (a) Design 4 Edit 3's pinned Failure-modes bullet was replaced by two bullets (`:698–708`) because the spec's text claimed `grill.md` records not-grillable/never-started cases as Open, which steps 1–3 make impossible — DEVIATIONS 1b; (b) step 3 gained a guard the spec does not state — `:518–521 — 'If the primitive returned `empty-seed`, or returned without a `## Grill summary` block … write nothing to `grill.md`'` — DEVIATIONS 1c. Both strengthen the append-only/never-partial rule; both raised by CodeRabbit on PR #26 and re-verified (five hunks, 2e/2g identical, lint clean). |
| S9 | Empty seed is a halt, not an empty frontier | Confirmed | `skills/grilling/SKILL.md:31 — 'exit `empty-seed` at once, without rendering a round'`; `:110 — '`empty-seed` returns the token and a one-line reason, and nothing else'`; `skills/spec-brief/SKILL.md:88 — 're-prompt once, then halt … If the primitive itself returns `empty-seed`, halt the same way — nothing is written'`; `skills/grill-me/SKILL.md:21`; the 1c guard (`skills/spec-cycle/SKILL.md:518`) makes the "callers never write on `empty-seed`" clause hold for 2f-i; Run C test-output `:617–627` |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `grilling/SKILL.md` exists, `user_invocable: false`, with tree/frontier, one-round-per-frontier, D4 fork, D1–D2 dispatch, three D6 bounds | Met | `skills/grilling/SKILL.md:4 — 'user_invocable: false'`; `:25–29` tree/frontier; `:38–43` fork block; `:70` D2 sentence; `:82–86` three bounds; test-output row 4 `:59–83` PASS |
| 2 | `grill-me/SKILL.md` exists, `user_invocable: true`, delegating to `grilling` | Met | `skills/grill-me/SKILL.md:4 — 'user_invocable: true'`; `:14 — 'Run the `grilling` skill … with `seed` = the topic the user gave, brief altitude, and the default bounds (3 rounds, 7 questions)'` |
| 3 | `spec-brief/SKILL.md` exists; writes brief with eight sections, Settled → Decisions, Open → Risks | Met | `skills/spec-brief/SKILL.md:113–128` section skeleton; `:139–140` mapping; Run A test-output `:386–408` (eight sections, References bullet), Run B `:580–595` (3 Open → "spec author pins this" ×3) |
| 4 | Degrades to conversation-only without the tracker; both services optional | Met | `skills/spec-brief/SKILL.md:10 — 'services: [issue-tracker?, shared-memory?]'`; `:65 — 'On failure of both: **conversation-only mode.**'`; test-output `:262–279` (memory 0 results → tracker not found → local-only) |
| 5 | 2f offers option 4; text says no re-dispatch, no round increment, routes through 2e | Met | `skills/spec-cycle/SKILL.md:484` option 4; `:539–540` 2e rules; `:556–557 — 'never re-dispatches reviewers, never increments the round counter'`; test-output row 7 `:115–128` PASS |
| 6 | 2f-i persists to `reviews/round-4/grill.md`, append-only | Met | `skills/spec-cycle/SKILL.md:524 — '`docs/specs/TODO/<TICKET-ID>.reviews/round-4/grill.md`'`; `:530 — 'Never overwrite an existing `grill.md`'`; test-output `:126` (path count 2) |
| 7 | Valid `requires:` in all three; `lint.py --strict` zero ERROR, no new `missing-requires` WARN | Met | test-output row 1 `:17–25 — 'lint: 0 error(s), 2 warning(s)' … 'no new WARN was introduced' PASS` |
| 8 | No bare harness tool name as an operative imperative; `Explore`/Opus only inside the D2 parenthetical | Met | test-output row 2 `:27–49` (every hit is case-2 parenthetical, case-3 heading, or the prohibition) PASS; row 3 `:53–57` (`model:` count 0 each) PASS |
| 9 | `AGENTS.md`, reference, `README.md` describe the four-stage lifecycle incl. `/spec-close` | Met | `AGENTS.md:23 — 'Four skills form the spec lifecycle'` + items `:25–31`; `README.md:3 — 'brief → spec → review → ship → close'`, `:12` `/spec-close`; `docs/spec-workflow-reference.md:3 — 'Four AI-driven skills'`, `:7`, `:194`; test-output row 8 `:130–150` PASS |
| 10 | `sync.py status` clean; `push` round-trips byte-for-byte; Test command N/A; Test plan = checklist + dry runs | Met | test-output row 10 `:177–182 — '26 action(s) applied.' / 'In sync.' / 'No changes'` (run with `--claude-dir <scratch>` per DEVIATIONS 2 `:699–705`; round-trip property fully exercised); spec `:477–479` Test command N/A; spec `:453–475` checklist + Runs A–D |

## Test Plan
| Test | Exists? | Location |
|---|---|---|
| Row 1 — lint --strict, 0 ERROR, WARN count 2 | Yes, PASS | test-output `:14–25` |
| Row 2 — no bare harness tool name imperative | Yes, PASS | test-output `:27–49` |
| Row 3 — no `model:` frontmatter | Yes, PASS | test-output `:51–57` |
| Row 4 — grilling verbatim contract lines + real `##` headings | Yes, PASS | test-output `:59–83` |
| Row 5 — `user_invocable` values; description hygiene | Yes, PASS | test-output `:85–95` |
| Row 6 — spec-cycle diff confined to named sites; gate count; 2e/2g identical | Yes, PASS | test-output `:97–113` (five hunks; re-verified after 1b/1c at `:675–677`, `:695–697`) |
| Row 7 — 2f-i invariant strings + scalability halt line | Yes, PASS | test-output `:115–128` |
| Row 8 — three docs describe four stages; spec-close ≥1 in README/reference | Yes, PASS | test-output `:130–150` |
| Row 9 — spec-brief body assertions (ranges, no 0 alias, .tmp, rename, Scale rule) | Yes, PASS | test-output `:152–169` |
| Row 10 — sync.py install/status/push round trip; `/grilling` slash probe | Yes, PASS | test-output `:171–199` — round trip against a scratch `--claude-dir` (DEVIATIONS 2 `:699–705`); slash-command probe deferred to post-merge install, non-blocking per the row |
| Row 11 — agents/, ship-spec/, spec-close/ untouched | Yes, PASS | test-output `:201–207`; re-verified `git diff --name-only e193b8e d381f88` on those trees → empty |
| Row 12 — AGENTS.md collision paragraph; "Two warnings:" still 2 bullets | Yes, PASS | test-output `:209–217` |
| Row 13 — --no-grill and option-2 paths | Yes, PASS | test-output `:219–231` |
| Row 14 — no ZZZ-*/.*.tmp leakage after dry runs | Yes, PASS | test-output `:630–640` |
| Run A — empty frontier | Yes, PASS | test-output `:249–409` |
| Run B — round cap (`--rounds 1 --questions 3`) | Yes, PASS | test-output `:412–512`, write half `:580–595` |
| Run C — empty seed | Yes, PASS | test-output `:598–627` |
| Run D — revise after cap | Yes, PASS | test-output `:515–578`. Note: spec Test plan `:475` says the round-end line reads `Round 2 of 1 (…)` while Design 1.3 (`:179`) and `skills/grilling/SKILL.md:57` pin `Round <round_cap>+1 of <round_cap>`; the run rendered `Round 1+1 of 1` (`:541`), matching the Design — a stale line in the spec's Test plan, not a code drift. |

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision D9: a model-invocable primitive is fenced by a body guard sentence and a caller list in its description, not by `user_invocable: false` — the flag is advisory (informational on Hermes, dropped by the VHS-20 adapter). Reusable rule for any future non-user-facing skill.
- Decision S5 (with D1/D2): when a host has no read-restricted agent class, render a fact request to the operator rather than dispatch a write-capable agent; fact requests share the per-round cap. Constrains every future skill that fans out for facts; also records the contract gap that `requires.subagents` cannot be optional.
- Decision D7 + S1: a cap is a documented outcome — hard truncation with carried overflow, unresolved items surface as "spec author pins this". The pattern for bounding any interactive loop without deadlocking it.
- Decision S8: `grill.md` is append-only with an anchored `# Grill <k>` counter, and the once-per-invocation bound is context-held because `/spec-cycle` records no preflight timestamp. Second concrete instance of "audit trail over coordination" alongside VHS-29's log prepend.
- Decision D10 / Design 6: second supersession of a third-party skill (after VHS-28), dispositioned differently — same-name overwrite on `sync.py install` needs no removal step or uninstall manifest. Updates the revisit trigger in `decisions/2026-08-25-vhs-28-supersession-is-an-operator-step.md`.
- Decision S9: an empty seed is a distinct exit that callers treat as a halt and never write on; the shipped 2f-i step-3 guard (DEVIATIONS 1c) extends this to "no `## Grill summary` block → nothing persisted".
- Comprehension: the spec lifecycle is now four stages — `/spec-brief` → `/spec-cycle` → `/ship-spec` → `/spec-close` — with the brief produced by a bounded interview instead of an unbounded prompt, so the artifact every reviewer lens treats as authority has its forks settled before review context is spent. The interview is the shared model-invocable `grilling` primitive (`filesystem: [read]` only, `subagents: true`): it models the problem as a design tree, asks the whole settled frontier per round with weighed forks and an advisory recommendation, dispatches read-restricted exploration for facts, and stops on a round cap, a per-round item cap, or an altitude fence, handing back a Grill summary that the caller alone writes. The same primitive backs `/grill-me` (no artifact) and `/spec-cycle`'s new post-round-4 option 4 (2f-i), which grills only the remaining P0/P1 findings, routes decisions through the existing 2e revise path, appends to `round-4/grill.md`, and never re-dispatches reviewers or moves the round counter.

RECONCILED: yes DRIFT: 1
