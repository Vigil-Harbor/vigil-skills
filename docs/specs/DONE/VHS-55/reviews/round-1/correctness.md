# Correctness Review — round 1

## Closure of round 0 findings
N/A — round 1

## Findings

### F-1: Looser Tier heading rule halts every valid `## Tier` section
**Severity:** P0
**Where:** spec § Design, spec-cycle parse step 1 (spec.md:175)
**Claim:** "A heading that matches the looser `^#{1,6}\s+tier\b` and whose body contains a `**Level:**` line is malformed: halt."
**Why this is wrong:** `## Tier` matches both the strict pattern `^#{1,6}\s+tier\s*$` and the looser `\btier\b` pattern. The Level step on the next line accepts `small`, `big`, and `irreversible`. A literal reading of the halt sentence is true of every well-formed section the brief's Done when requires (`## Tier` plus `**Level:** small`). Scale's near-miss tripwire, which this parse is copying, is conditional: it fires only when no whole-word heading matched (`skills/spec-cycle/SKILL.md:299-304`). This sentence is not. The following sentence ("A looser heading with no `**Level:**` line is ignored") would also swallow a strict `## Tier` that step 2 is supposed to halt on for a missing level. `## Tiering` / `## Tier list` are the near-misses the strict pattern already excludes; they are the only headings the looser rule can mean.
**Suggested fix:** State that the looser rule applies only when no strict `^#{1,6}\s+tier\s*$` heading matched. A second strict `## Tier` stays on the warn-and-use-first path, Level line or not.

### F-2: Malformed-brief halt runs before the re-run pin
**Severity:** P0
**Where:** spec § Design, spec-cycle parse step 2 and Re-run pin (spec.md:176, spec.md:179); Decision 2
**Claim:** Step 2: "No Level line, an empty value, `tweak`, or any other token → halt `tier: malformed (<what was found>) — halting`. Write no marker." Re-run pin: the recorded spec line "is authoritative, including when the brief is absent, disagrees, or malformed."
**Why this is wrong:** The numbered parse halts and returns before the pin. A later brief edit that breaks `**Level:**` then blocks every re-run of a spec that already has a valid `**Tier:**` line, and the warning `tier: brief malformed — using recorded` is unreachable. That contradicts this spec's Decision 2 and brief Decision 2: once the spec exists, the recorded line is authoritative (the same pin Scale uses at `skills/spec-cycle/SKILL.md:330-340`). "Brief absent" cannot mean the file is missing either: Phase 0 step 2 already halts when the brief file is gone (`skills/spec-cycle/SKILL.md:109`). It has to mean the section is absent, which is the non-halting path and does not need the halt to be unconditional.
**Suggested fix:** Resolve a recorded spec line first. If its value is `small`, `big`, or `irreversible`, it wins and the run warns `tier: brief <absent|disagrees|malformed> — using recorded`. Halt on a malformed brief only when the spec has no valid recorded line. A recorded line whose own value is not one of the three still halts and does not fall through to the brief.

### F-3: A non-bare `**Tier:**` line is read as absent and becomes `big`
**Severity:** P1
**Where:** spec § Decision 12 (spec.md:76); reader rule (spec.md:183); ship-spec step 1b (spec.md:229)
**Claim:** "A candidate is a line matching `^[ \t]*\*\*Tier:\*\*\s*(\S+)\s*$`." No match means `big`. Decision 12: "a missing value on a present section or line halts the reader." Brief Decision 12, which this decision carries: a missing level "halts the reader rather than downgrading, so an intended `irreversible` is never silently read as `big`."
**Why this is wrong:** The candidate regex requires a token and end-of-line. `**Tier:**` with no value does not match, so it is not a "present line" and the invocation takes `big` with no warning. `**Tier:** irreversible — unskippable gate` does not match either, so an irreversible declaration written in this repo's usual `**Label:** value — note` shape is also absence, and ship-spec then allows the three Phase 3b skips. Unknown tokens and `tweak` halt only after the regex matches. Attest mode and the re-run pin use this same rule, so all three readers fail open together. The brief section does not have this hole: a present `## Tier` heading plus no Level line already halts.
**Suggested fix:** Keep fenced lines excluded. A line that matches `^[ \t]*\*\*Tier:\*\*` but not the bare-value pattern halts as `tier: malformed`. Default to `big` only when no such line exists. Apply that to spec-cycle, attest mode, and ship-spec.

### F-4: Irreversible "re-run /ship-spec" cannot resume the worktree it just created
**Severity:** P1
**Where:** spec § Decision 8 and Phase 3b irreversible halt (spec.md:60, spec.md:242-251)
**Claim:** "The halt names the case and tells the operator to declare or repair the command and re-run `/ship-spec`. The run does not commit." Brief Decision 8: "re-running ship-spec is the resume path."
**Why this is wrong:** Phase 3b runs after Phase 1 has already created the branch and `<project-root>/../<TICKET-ID>-worktree`. Those checks halt a second invocation: an existing worktree path is a hard stop, and an existing branch stops for reuse/delete/rename (`skills/ship-spec/SKILL.md:107-119`). The new halt text offers no in-place continue (unlike the existing Blocks halt at `:222-239`, whose option 1 resumes in the same worktree) and does not print the worktree path. Following the halt deletes the implementation or dead-ends. Nothing in this spec changes Phase 1.
**Suggested fix:** On the irreversible halt, print the worktree path and say the uncommitted tree is kept. Resume means repair the command and continue that worktree at Phase 3b, not re-enter Phase 0. If a full re-invocation is required, say that `git worktree remove` discards the implementation, and do not call that a resume.

### F-5: Post-cap Confirm still offers only options 1 and 3
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design, spec-brief Confirm (spec.md:159)
**Claim:** "Add option 4: `Change the tier — ask the tier gate again`. … Options 1 to 3 behave as they do now."
**Why this is wrong:** Today's Confirm, after a post-cap resume, "re-renders with options 1 and 3 only" (`skills/spec-brief/SKILL.md:105`). The spec never edits that sentence, and "behave as they do now" keeps it. That menu is still Phase 3, and brief Decision 6 says Confirm can change the tier, including to `tweak` before Phase 4. Option 4 also "shows the same prompt" as the tier gate, whose rule is that any reply other than `1`–`4` stops and writes nothing. After the interview, that discards the run on a typo, and the spec does not say whether the re-ask inherits that rule.
**Suggested fix:** Say the post-cap menu is options 1, 3, and 4 (option 2 stays omitted). On the re-ask, an invalid reply re-prints the tier prompt and does not discard the interview.

### F-6: Tweak-floor match mode and basis line are not pinned tightly enough to judge the examples
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 14 (spec.md:92-117)
**Claim:** "A path signal matches a path segment or a filename." Extension signals "match a named path as a substring." Basis template: `basis: <n> files (<paths>) | files: unknown, ~<m> lines | lines: unknown, surfaces: none | <surface> | surfaces: unknown`. Examples are "normative for that shape," including `1 file` and `surfaces: config`.
**Why this is wrong:** Built-in path signals do not say whether `auth` equals a segment, equals a filename, or is a substring. `authentication/foo.py` and `config.py` come out differently under those readings, and a substring miss recommends `tweak` for a change Decision 4 says is never `tweak`. Extension text says read `AGENTS.md`, then `CLAUDE.md` when it exists, and "no heading in either file" means the built-in four only — union versus first-heading-wins is not stated, so a signal that should block `tweak` can be dropped. The basis template and the normative examples disagree: example 1 uses `1 file` not `1 files`, and example 2 uses `surfaces: config` where the template's alternative is a bare `<surface>`. Two matching surfaces have no winner. Checklist item 1 cannot be applied until those are one grammar.
**Suggested fix:** Pin path signals as case-insensitive equality on a path segment or on the filename (state whether `config.py` matches filename `config`). Union `## Tweak surfaces` lines from both files. Make the basis grammar match the three examples, including singular `file` and `surfaces: <name>`, and name which surface wins when several match.

### F-7: `round_cap` rewrite leaves literal cap-of-4 sentences in force
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § `round_cap` substitution (spec.md:189-213); docs paragraph (spec.md:267); AGENTS.md paragraph (spec.md:269)
**Claim:** "rewrite these and no other numerals" in `skills/spec-cycle/SKILL.md`. In the workflow reference, rewrite only `:84-86` and `:246`. In `AGENTS.md`, edit the spec-cycle bullet at `:27`.
**Why this is wrong:** Those closed lists leave sentences that are false when `round_cap` is 2. `skills/spec-cycle/SKILL.md:672` still says 2f-i applies edits "under the 2e rounds-1–3 rules" (the table never names 672; "no other numerals" forbids fixing it). `docs/spec-workflow-reference.md:66` is still "up to 4 rounds", `:27` is still "post-round-4", and `:102` is still "red at the round-4 halt", beside steps that the spec does retarget at `round_cap`. `AGENTS.md:25` still says "post-round-4 option 4" next to the bullet the spec rewrites at `:27`. The lines the table does name (`:3`, `:17`, `:36`, `:369`, `:373`, `:495`, `:497`, `:507`, `:510`, `:525`, `:531`, `:548`, `:549`, `:551`, `:555`, `:560`, `:565`, `:581`, `:587`, `:589`, `:591-594`, `:620`, `:622`, `:656`, `:658`, `:676`, `:685`, `:688`) match the current skill text.
**Suggested fix:** Add `:672` to the spec-cycle table as `rounds 1 .. round_cap−1` (do not touch `routing steps 1–3` or menu `options 1–3`). Add workflow-reference `:66`, `:27`, and `:102`, and `AGENTS.md:25`, to the same substitution.

### F-8: Ship-spec's other copies of the gate contract stay unconditional
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § ship-spec (spec.md:240-253); spec-cycle canonical marker table
**Claim:** The Phase 3b opening at `:183` gains the irreversible exception. "`big`, and an absent spec line: the three skip cases stay skips, including the failure-mode wording at `:432-433`." Green and changed rows at `skills/ship-spec/SKILL.md:30-31` gain the tier clause. "`small` … Phase 3 still runs."
**Why this is wrong:** `:432-433` today say an unavailable or failed review command skips and "Never halt for it." The spec does not say those bullets gain the irreversible exception, so the failure-mode section contradicts the new halt. `skills/spec-cycle/SKILL.md:60-69` still calls its fingerprint-only table the canonical copy that ship-spec carries. This spec changes ship-spec's copy and leaves spec-tickets inert (Decision 13, and `skills/spec-tickets/SKILL.md:36-44` does only read `verdict:` and `ticket:`). Nothing tells the implementer to break that "identical copy" claim, so a later sync from the canonical table drops the tier check or pushes it into spec-tickets. "Phase 3 still runs" can also be read as overriding the existing `N/A` test-command skip (`skills/ship-spec/SKILL.md:60`, `:144`).
**Suggested fix:** Say the `:432-433` bullets halt for `irreversible` and still skip otherwise. Say spec-cycle's canonical table stays fingerprint-only, ship-spec's green/changed rows are the ones that add the tier clause, and spec-tickets does not. Say the `N/A` test-command skip is unchanged for every tier.

### F-9: ticket not cached
**Severity:** P3
**Where:** grounding step 3
**Claim:** Plane ticket VHS-55 is canonical where it conflicts with the brief.
**Why this is wrong:** `memory_search` on namespace `skills` with tags `plane_work_item` and `VHS-55` returned `Access denied: agent 'grok' lacks 'read' on namespace 'skills'`. The review used the brief. Anchors in the skill files were checked against the tree as of 2026-10-11; commits on those files since 2026-10-08 (`b1ab82b`, `8d404d0`, `aad9971`, `156d388`, `1bd3f29`) are already what the cited line numbers point at.
**Suggested fix:** Re-check the ticket text if a host with `skills` read access is available before ship.

## Summary
P0: 2 | P1: 2 | P2: 4 | P3: 1 | P4: 0

STATUS: RED P0=2 P1=2 P2=4 P3=1 P4=0
