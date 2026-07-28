# Edge-Cases Review — round 1

**Grounding notes:** Spec and brief read fresh, Plane ticket VHS-11 retrieved from MCP memory (confidence 0.82), CLAUDE.md in context, and all four target files verified — every line anchor in the spec checks out (`SKILL.md:23/96/99/101/107/142–152/144/147/172–181/264–273/277–293`; agent `**Severity:**` lines at correctness:146, edge-cases:141, conventions:135). External failure axes for this doc-only spec: git (local state + network fetch), conversational user prompts, subagent prompt contents, and the sync.py round-trip. Persistence checklist: no runtime persisted state is introduced; the only durable artifacts are spec-file sections, covered in F-2 below.

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: `<branch>` variable binding breaks on the default-branch fallback path in step 5c→5d/5e
**Severity:** P1
**Where:** spec.md:93–146 (D1, sub-steps 5c, 5d, 5e)
**Edge case:** current branch has no origin counterpart (e.g., a local topic branch never pushed) and the fallback chain resolves a default branch.
**What happens:** 5c captures the *current* branch as `<branch>` and, on fallback, resolves a *default* branch — but never names a variable for it. 5d (`git rev-list --count HEAD..origin/<branch>`), 5e (`git merge-base --is-ancestor HEAD origin/<branch>`), the prompt text ("local `<branch>` is `<N>` commits behind origin/`<branch>`"), and the merge command (`git merge --ff-only origin/<branch>`) all interpolate `<branch>` — which on the fallback path is precisely the branch with **no** `origin/<branch>` ref. Followed literally, 5d runs `git rev-list --count HEAD..origin/feature-x` → `fatal: bad revision`, a failure mode with no defined token; the step's behavior past that point is undefined.
**Why the spec misses it:** D1 reuses step 4's single-variable idiom, but step 4 only ever compares against `upstream/<default-branch>` — one variable suffices there. The brief's Risks §6 explicitly delegated this path ("fall back to the default branch") to the spec author; the spec resolves the *branch* but not the *binding* used by every downstream command.
**Suggested fix:** Introduce `<compare-branch>` in 5c: set to `<branch>` when `origin/<branch>` verifies, else to the resolved default branch. Use `origin/<compare-branch>` in 5d, 5e, the prompt text, the merge command, and the log tokens. The interpolated prompt then reads naturally on the fallback path ("local feature-x is 5 commits behind origin/main … `git merge --ff-only origin/main`"), which also makes the user-visible consequence (the topic branch is advanced onto origin/main's tip) explicit before confirmation.

### F-2: 2g steps 3–4 assume folded P2s live in `## Deferred (P2+)` — false for the primary case
**Severity:** P1
**Where:** spec.md:165–188 (D2, § 2g steps 3 and 4); interacts with SKILL.md:172–181 (2d/2e)
**Edge case:** spec goes green — the normal, intended trigger for 2g.
**What happens:** The loop is 2a→2b→2c→2d(gate)→2e(revise, *only if still red*). When the gate breaks green at round N, 2e never runs for round N, so the final round's P2s are **never written to `## Deferred (P2+)`** — and for green-at-round-1, the section doesn't exist at all. Yet 2g step 4 says "Move each folded P2 **out of** `## Deferred (P2+)`," and step 3 says an over-limit candidate "**stays in** `## Deferred (P2+)` untouched, with a one-line reason" — an entry that was never created cannot stay, and a one-line reason cannot be appended to a nonexistent row. The instruction's precondition is false for exactly the candidates step 1 defines (final-round report findings). Followed literally, the operator either silently no-ops the bookkeeping (folded/rejected P2s leave no trace) or improvises — the PET-86 undocumented-discretion problem the step exists to eliminate, reproduced inside the step itself.
**Why the spec misses it:** It inherits 2d's pre-existing loose phrasing (SKILL.md:174 says P2+ "are carried forward … in the `## Deferred (P2+)` section" without saying any step does that on the green round) and builds a move-out-of mechanic on top of it.
**Suggested fix:** Rewrite 2g steps 3–4 to be source-agnostic: step 3 — "a candidate that exceeds these limits is recorded in `## Deferred (P2+)` (creating the section/entry if absent) with a one-line reason"; step 4 — "record each folded P2 in `## Post-green polish` (finding ID + what changed); if it has an entry in `## Deferred (P2+)`, remove that entry." Optionally add one sentence to 2g step 1 making explicit that final-round P2s arrive via reports, not via Deferred.

### F-3: ff update mutates the tree after steps 2–4 already read from it — no post-update re-validation
**Severity:** P2
**Where:** spec.md:63–147 (D1 placement: step 5, after steps 2–4)
**Edge case:** user confirms the ff update, and the pulled commits touch preflight inputs — the brief itself (moved to `DONE/`, renamed, edited), `CLAUDE.md` (test commands changed), or a `docs/specs/TODO/<TICKET-ID>.spec.md` that a teammate already merged.
**What happens:** Step 2 confirmed brief existence, step 3 extracted CLAUDE.md test commands, and step 4d extracted search terms — all against the pre-update tree. After the update: a moved/deleted brief makes Phase 1's read fail at a point with no defined handling (step 2's halt message is preflight-only); stale CLAUDE.md test commands flow into the spec's `## Test command`; and a pre-existing merged spec file is silently overwritten by Phase 1 (Phase 1 writes the output path with no exists-check). Silent overwrite of a merged spec is the worst of these — exactly the half-state class the origin check is meant to prevent.
**Why the spec misses it:** The brief pins insertion "after step 4 (`:96`)," and the spec treats the mutation as terminal to step 5 ("continue to step 6") without considering that steps 1–4's reads are now stale.
**Suggested fix:** Add one sentence to 5e's on-update branch: "After a successful update, re-confirm the brief exists at the resolved path and re-read CLAUDE.md (steps 2–3); if `docs/specs/TODO/<TICKET-ID>.spec.md` now exists in the tree, halt and ask before overwriting in Phase 1."

### F-4: Pre-ship-tagged P2s from non-final rounds silently drop out of the polish step
**Severity:** P2
**Where:** spec.md:172–176 (D2, 2g step 1: "the final round's three reports")
**Edge case:** green at round ≥ 2, with a `**Pre-ship recommended:** yes` P2 tagged in round N−1 that the author deferred in 2e (didn't fix) and that the final round's reviewers did not re-emit (their closure tables track prior P0/P1 only — P2s are not re-raised).
**What happens:** 2g collects candidates only from the final round's reports, so the earlier-round tagged P2 is silently excluded — no log line distinguishes "none tagged" from "tagged earlier, not collected." The exact reviewer-recommended clarifications the feature exists to capture fall through whenever tagging and green happen in different rounds.
**Why the spec misses it:** PET-86's trigger case happened to have the tags appear in the green round itself, so the single-round collection looked sufficient.
**Suggested fix:** Either widen step 1 to also scan prior rounds' reports (or the spec's `## Deferred (P2+)` entries) for the marker, or state the limitation explicitly in 2g ("only final-round tags are honored; earlier tagged P2s remain in Deferred") so the drop is documented rather than silent.

### F-5: Closure manifest is undefined for the synthetic missing-STATUS P0
**Severity:** P2
**Where:** spec.md:236–252 (D4 closure-manifest block); interacts with SKILL.md:288 (failure mode: unparseable STATUS → "treat as `STATUS: RED P0=1`")
**Edge case:** a round-(N−1) reviewer report lacked a parseable STATUS line, so the orchestrator counted a synthetic P0 that exists in no report — no finding ID, no title, no `**Where:**`.
**What happens:** The manifest mandates one line per round-(N−1) P0/P1 in the shape `<lens>/<finding-id> (P<sev>) "<title>" — <how addressed, with spec § anchor>`. The synthetic P0 has none of these fields and no spec edit can "address" it. The author either omits it (manifest disagrees with the round-(N−1) gate arithmetic) or invents a line (agents' step-7 disk-read finds no matching finding and may emit a spurious mismatch finding). Either way the manifest's claim-verification value degrades exactly when reviewer output was already malformed.
**Why the spec misses it:** D4 assumes every gate-counted P0/P1 corresponds to a report finding; the synthetic-P0 rule at SKILL.md:288 breaks that assumption.
**Suggested fix:** One sentence in the D4 block: "A synthetic missing-STATUS P0 (per `## Failure modes`) appears in the manifest as `<lens>/STATUS (P0) "missing STATUS line" — report regenerated in round <N>` (or is exempted with that notation)."

### F-6: Exit-code conflation in 5e and undefined failure token for 5d
**Severity:** P3
**Where:** spec.md:109–146 (D1 sub-steps 5d, 5e)
**Edge case:** `git merge-base --is-ancestor` exits >1 on error (bad ref, or a shallow clone whose merge base lies below the shallow boundary); `git rev-list --count` fails on an unborn HEAD or truncated history.
**What happens:** 5e treats all non-zero exits as "histories have diverged" — a shallow clone is misreported as diverged (wrong cause in the warning and audit token, though it degrades safely: no mutation, proceed). 5d has no token for command failure at all; a rev-list error leaves the step's outcome unlogged.
**Why the spec misses it:** Mirrors step 4's pattern, which never runs merge-base and so never had the exit>1 ambiguity.
**Suggested fix:** Add a catch-all to D1: "any git command failure inside step 5 not otherwise handled → log `origin: skipped (git error)` and continue to step 6"; optionally note shallow clones in the diverged warning.

### F-7: Ticket-ID regex rejects digit-bearing Plane project prefixes
**Severity:** P3
**Where:** spec.md:207–210 (D3, `^[A-Z]+-[0-9]+`)
**Edge case:** Plane project identifiers may contain digits (e.g., `WEB3-12`); `[A-Z]+` stops at the digit and the match fails.
**What happens:** Degrades gracefully — the skill asks the user for the ticket ID — but the "tolerant resolution" feature mis-fires for an entire valid identifier class, every invocation, on such projects.
**Why the spec misses it:** All current vigil projects (VHS, PET, MCP, CAL) use pure-alpha prefixes.
**Suggested fix:** `^[A-Z][A-Z0-9]*-[0-9]+` (still anchored; still resolves the PET-86/MCP-33 example identically since matching starts at the prefix).

### F-8: Dry-run transcript covers only the happy ff path — diverged and ff-abort paths untested
**Severity:** P3
**Where:** spec.md:312 (Test plan item 9)
**Edge case:** the two risk-bearing branches of the skill's only mutation — diverged histories (no offer) and a git-aborted ff (uncommitted changes in the way) — are exercised by no transcript; only `git reset --hard HEAD~2` → ff-success is.
**What happens:** A wording bug in the never-retry branches (the ones Decision 1 calls load-bearing) would ship unexercised; checklist item 1 verifies the text exists, not that an operator following it behaves correctly.
**Suggested fix:** Extend item 9: in the same scratch repo, (a) add a local commit after the reset → verify the diverged warning and that no update is offered; (b) dirty a tracked file that the incoming commits touch, confirm the update, and verify git's abort is printed and the skill proceeds without retry.

### F-9: D1's enumeration of step-4 "continue to step 5" sub-steps omits 4e and 4g
**Severity:** P4
**Where:** spec.md:65 (D1: "the 'continue to step 5' lines inside step 4 (a/b/d/f sub-steps)")
**Edge case:** N/A — documentation accuracy. Grep shows six occurrences: SKILL.md:36 (4a), :42 (4b), :56 (4d), :70 (4e), :76 (4f), :95 (4g).
**What happens:** The no-text-change claim holds for all six, so no behavioral effect — but an implementer cross-checking the enumeration against Test-plan item 2's grep will hit two "unaccounted" lines and burn time reconciling.
**Suggested fix:** Change the parenthetical to "(all six occurrences: 4a/4b/4d/4e/4f/4g)".

### F-10: "Verbatim" brief_path in the 2b prompt — normalization unstated for agent cwd resets
**Severity:** P3
**Where:** spec.md:229–232 (D4 edit 1: "verbatim, not the canonical template")
**Edge case:** user-typed path forms the tolerance newly admits — Windows backslashes (`docs\briefs\X.md`), `./`-prefixed, or absolute paths — passed verbatim to subagents whose cwd resets between calls and who join relative paths against `project_root` only by convention.
**What happens:** Agents whose Read of `brief_path` fails record a blocked grounding step as a finding and continue — three degraded reviews in one round, polluting the convergence signal the spec's items 1 and 4 exist to protect.
**Why the spec misses it:** Step 1 says "Resolve `<brief-path>`" but never defines resolution to a normalized form; "verbatim" then propagates whatever the user typed.
**Suggested fix:** In D4 edit 1, replace "verbatim" with "the resolved path, normalized to absolute (or project_root-relative with forward slashes)".

## Summary
P0: 0 | P1: 2 | P2: 3 | P3: 4 | P4: 1

STATUS: RED P0=0 P1=2 P2=3 P3=4 P4=1
