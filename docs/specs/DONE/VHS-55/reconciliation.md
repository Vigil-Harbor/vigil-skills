# Reconciliation Report: VHS-55

> Date: 2026-10-11
> Spec: docs/specs/TODO/VHS-55.spec.md
> Merge: PR #38 (squash `5f640d0`; CodeRabbit fix folded pre-merge as `d738797` on the branch)
> Plane state: Done (group: completed)

## Summary
Every Scope row shipped and every Done-when bullet is met. One decision drifted on purpose: the irreversible-tier return classification was hardened after CodeRabbit's review (command-level errors are now judged before the "readable findings" test, where the spec had them inside test 3). The suite does not execute skills, so the spec's seven-item reading checklist is the real gate; two items were walked (2 and 4), one was exercised by the CodeRabbit finding (7), and four remain reading-only.

## Scope
| Spec file | In diff? | Notes |
|---|---|---|
| `skills/spec-brief/SKILL.md` | Yes | +93/−5: seed gate hoisted to every mode (`:86`), tier gate (`:90-124`), heuristic + basis line + four examples (`:130-158`), Confirm option 4 (`:175-180`), `## Tier` emission (`:202-216`) |
| `skills/spec-cycle/SKILL.md` | Yes | +57/−41: Phase 0 step 9 tier/`round_cap` parse with re-run pin and reader rule (`:343-353`), `**Tier:**` Decision line (`:380`), `tier:` on every marker incl. attested (`:38,50,51`), loop cap → `round_cap` (`:384,513,576`), tier on every reviewer prompt (`:420`) |
| `skills/ship-spec/SKILL.md` | Yes | +47/−12: spec-line reader, never the brief (`:24`), `tier:` clause of `green`/`changed` (`:34-35,59`), `small` skip (`:197`), `irreversible` halt + three tests + options (`:199-214`), `Halted passes:` (`:293`) |
| `agents/spec-reviewer-{correctness,edge-cases,conventions,scalability}.md` | Yes | +1 each: `tier` input line (`:20`, `:20`, `:22`, `:21`) |
| `docs/spec-workflow-reference.md` | Yes | +73/−12: tier gate and headless stop (`:19`), Confirm shows tier + basis (`:23`), `round_cap` loop (`:70-92`) |
| `AGENTS.md` | Yes | +6/−4: "Stakes tier" paragraph (`:35`), severity scale unchanged by tier (`:107`) |

Leave-alone list honoured: `git diff --stat 95b7ac0 5f640d0 -- skills/spec-tickets tests/` is empty; `README.md`, `docs/customizing.md`, `docs/portability-contract.md`, `sync.py`, `states.json` untouched.

Unexpected files in diff (not in spec):
- `docs/specs/TODO/VHS-55.review.md` — ship-spec review-gate record (expected audit artifact, not drift; VHS-53 precedent)
- `docs/specs/TODO/VHS-55.test-output.txt` — ship-spec test capture (expected audit artifact, not drift)

## Decisions
| # | Decision | Status | Evidence |
|---|---|---|---|
| 1 | Four tiers; `irreversible` adds no lens; scale stays its own declaration | Confirmed | `skills/spec-cycle/SKILL.md:343` — 'Do not change the scale parse above, and do not set `scale_lens` from the tier'; `AGENTS.md:35` |
| 2 | Carrier: brief `## Tier` → spec `**Tier:**` Decision → marker `tier:`; spec line authoritative; ship-spec never reads the brief | Confirmed | `skills/spec-brief/SKILL.md:211-213`; `skills/spec-cycle/SKILL.md:380`, `:51` (attested marker carries `tier:`); `skills/ship-spec/SKILL.md:24` — 'read the spec's recorded tier. Never read the brief for this'; `:35` (`changed` on malformed/disagreeing `tier:`) |
| 3 | The operator sets the tier; no `--tier` flag, no silent default | Confirmed | `skills/spec-brief/SKILL.md:92` — 'Nothing in any mode writes a tier the operator did not choose. There is no `--tier` flag' |
| 4 | Tweak floor: ≤2 files, <50 lines, none of auth/payments/data/config | Confirmed | `skills/spec-brief/SKILL.md:130-158` heuristic, taxonomy table, basis line (`:151`) |
| 5 | A tweak writes nothing; collision case names stale paths, deletes nothing | Confirmed | `skills/spec-brief/SKILL.md:108,112,120,124` — 'The tweak path creates no brief temp and deletes nothing' |
| 6 | Seed gate, then tier gate, then interview, in every mode; Confirm can change the tier | Confirmed | `skills/spec-brief/SKILL.md:86` — 'in every mode, including `--no-grill`'; `:92`; `:175-180` (Confirm option 4) |
| 7 | `small`: same three lenses, `round_cap = 2`, review gate skipped, test gate kept; grilling keeps its own cap of 3 | Confirmed | `skills/spec-cycle/SKILL.md:343` — '`small` sets it to 2'; `:384,513,576`; `:662` — 'interview cap 3 … This cap is the interview's, not the review loop's `round_cap`'; `skills/ship-spec/SKILL.md:197` |
| 8 | `irreversible`: three skip cases halt and wait; option 1 re-runs the gate in-run; three ordered return tests; supersedes VHS-46's skip rule for this tier only | Drifted | `skills/ship-spec/SKILL.md:199-214` implements the halt, options 1/2, `Command from:` line, worktree-kept text, `(no output, exit <code>)` and the `echo "no findings"` remedy (`:209`), `Halted passes:` (`:293`). **Drift:** `d738797` (CodeRabbit Major) moved "an error about the command itself on either stream" from inside test (3) to a check that runs *before* test (1), because a tool error carrying a location plus a problem would otherwise pass test (1). Behaviour is stricter than the spec, in the spec's own direction; the spec text was not updated. |
| 9 | Absence is `big` with no warning; present-but-malformed halts | Confirmed | `skills/spec-cycle/SKILL.md:351` — 'No strict match → `tier = big`, `round_cap = 4`, no warning'; `:352` — '`tweak`, a trailing note … halts `tier: malformed (<line>) — halting`' |
| 10 | Every reviewer prompt carries `tier`; each agent lists it | Confirmed | `skills/spec-cycle/SKILL.md:420` — 'Passed to every dispatched reviewer, including scalability'; four agent files `:20-22` |
| 11 | A host that cannot wait stops at the tier gate | Confirmed | `skills/spec-brief/SKILL.md:94` — 'print `tier needs an operator — stopping` and stop. Write nothing.' |
| 12 | Grammar: strict whole-word heading, `**Level:**` line, fences ignored, first wins / second warns | Confirmed | `skills/spec-cycle/SKILL.md:347` (reader rule), `:351-353` (heading, level, siblings ignored) |
| 13 | `spec-tickets` ignores `tier:`; no edit | Confirmed | `git diff --stat 95b7ac0 5f640d0 -- skills/spec-tickets` is empty |
| 14 | Tweak heuristic: unknown → `big`; never recommends `small`/`irreversible`; `## Tweak surfaces` extension | Confirmed | `skills/spec-brief/SKILL.md:149` (extension), `:151` (basis line), `:155-158` (four examples) |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | spec-brief: `## Tier` + `**Level:**` on non-tweak briefs; tweak writes nothing / names stale artifacts; seed gate before tier gate in every mode; headless stops at the tier gate | Met | `skills/spec-brief/SKILL.md:86,92,94,108,112,211-216` |
| 2 | spec-cycle: `**Tier:**` Decision line; `tier:` on every marker incl. attest; `small` runs `round_cap = 2`; tier on every reviewer prompt | Met | `skills/spec-cycle/SKILL.md:380,38,50,51,343,384,420` |
| 3 | ship-spec: reads the spec line; malformed/disagreeing marker `tier:` is `changed`; `small` skips the gate; `irreversible` halts on missing/unavailable/failed in every marker state, keeps the worktree, offers in-run re-run; clean statement or non-zero-with-findings is success, empty output is failed | Met | `skills/ship-spec/SKILL.md:24,34-35,59,197,199-214` |
| 4 | No `## Tier` / no `**Tier:**` behaves as today; malformed brief halts only when the spec has no valid line; recorded line wins with a warning; recorded line outside the three halts without falling through | Met | `skills/spec-cycle/SKILL.md:345` — 'A valid line … wins over an absent, disagreeing, or malformed brief. Warn … and do not halt'; '… halts `tier: malformed (<line>) — halting` … and does not fall through to the brief'; `:351` |
| 5 | `docs/spec-workflow-reference.md` and `AGENTS.md` describe the ladder | Met | `docs/spec-workflow-reference.md:19,23,70-92`; `AGENTS.md:35` |
| 6 | Lint and tests pass | Met | On `5f640d0`: `python lint.py --strict` over the three skills → 0 errors, 0 warnings; `python -m unittest discover -s tests -p "test_*.py"` → Ran 164, OK (skipped=3) |

## Test Plan
No new tests by design (the suite does not execute skills). The spec's seven-item review checklist:

| Test | Exists? | Location |
|---|---|---|
| 1. Decision 14 examples reproduce their basis lines | Reading-only, not walked at close | `skills/spec-brief/SKILL.md:155-158` carry the four examples verbatim |
| 2. `skills/spec-tickets/SKILL.md` has no diff | Walked — holds | `git diff --stat 95b7ac0 5f640d0 -- skills/spec-tickets` empty |
| 3. `round_cap = 2` / `= 4` predicate reading | Reading-only, not walked at close | `skills/spec-cycle/SKILL.md:513,576`; `docs/spec-workflow-reference.md:72,90-92` |
| 4. Grilling keeps its own cap of 3 | Walked — holds | `skills/spec-cycle/SKILL.md:662` |
| 5. Fenced / mid-line tier tokens are not the recorded tier | Reading-only, not walked at close | `skills/spec-cycle/SKILL.md:347`; `skills/ship-spec/SKILL.md:24` |
| 6. Absence → `big`; recorded line wins over malformed brief; out-of-set line halts | Reading-only, not walked at close | `skills/spec-cycle/SKILL.md:345,351-352` |
| 7. Irreversible Phase 3b reading (halt cases, three tests, options, `Halted passes:`) | Exercised by review — one gap found and fixed | CodeRabbit PR #38 Major on `:199`; fixed in `d738797` (see Decision 8) |
| Existing suite + lint | Yes | `tests/` (164 tests), `lint.py --strict` |

## Wiki-ready
Decisions and comprehension worth extracting to the wiki:
- Decision (multi-judgment): ceremony follows an operator-set stakes tier — four tiers, the brief→spec→marker carrier with the spec line authoritative, `small` = same lenses at `round_cap 2` with the review gate skipped, `irreversible` = halt-not-skip with three ordered return tests (refines VHS-46's "a skip never blocks the commit" for that tier only), absent = `big`, malformed halts, no override flags, headless stops rather than defaulting.
- Decision (within the same page): the tweak-floor heuristic recommends only `tweak` or `big`; unknown blocks `tweak`; `## Tweak surfaces` is the project extension point.
- Comprehension: how the tier flows through spec-brief (gate + emission), spec-cycle (parse, Decision line, marker, `round_cap`, reviewer prompts), ship-spec (reader, `changed` clause, skip/halt), the four reviewer agents, and what breaks if any one link is removed; plus the post-merge ordering fix.

RECONCILED: yes DRIFT: 1
