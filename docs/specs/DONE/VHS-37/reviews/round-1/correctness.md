# Correctness Review — round 1

Anchor verification summary (all against `main` @ `124700b`): Phase 1 `:294-296` ✓ (and its seven required sections match R4's halt list exactly), 2b example `:365-368` ✓, 2b prose `:378-383` ✓, 2d `:411-424` ✓, 2e `:426-464` with `:428-432` / `:430` / `:431` / `:432` / `:435-441` ✓, 2f `:466-487` ✓, 2f-i step 5 `:555-557` ✓, 2g `:593-624` ✓, Phase 3 `:626-659` ✓, Failure modes `:685-` ✓; agents `correctness:18/38-39`, `edge-cases:18/38-39`, `conventions:20/43-44`, `scalability:18/30/40` ✓; output contracts `138/133/127/76` ✓; `docs/spec-workflow-reference.md:77,84,88` ✓. Baseline grep counts asserted by the test plan check out (`Address every P0 and P1 finding` = 1, `Deferred (P2+)` = 7, `DEFERRED` = 0 in all four agents, `Deferred` = 0 in ship-spec/spec-close, `including round 1` = 0 in the reference doc). `lint.py` only ERRORs on `mcp__*` operative calls and `requires:` malformation — the new prose trips neither. `sync.py push --dry-run` exists on the subparser. Two commits from 2026-09-07 (`ecdfefe`, `c97d4ad`) touched the 2f-i region; the spec already surfaces them.

## Closure of round 0 findings
N/A — round 1.

## Findings

### F-1: A deferred in-scope P0 row is detected as a routing violation but has no permitted remedy — the gate can never clear
**Severity:** P1
**Where:** spec § Design 2 rule R2 (spec.md:99) vs. § Design 7 block (spec.md:148) and § Design 1 step 3 (spec.md:67)
**Claim:** Design 7: "A row whose `Finding` severity is `P0` and whose `Scope` is `in-scope` is itself a routing violation **whatever else it satisfies** — the ceiling forbids deferring an in-scope P0; file it once, as a P0 titled `routing violation: D-<n>`, naming the ceiling." R2: "`/spec-cycle` never deletes a row and never overwrites `Follow-up:` … The only edits the skill makes to an existing row are (a) repairing the field a `routing violation: D-<n>` finding names, or inserting a missing preamble, and (b) re-anchoring an entry … The finding record — `Finding`, `Deferred in`, `Suggested fix` — is never rewritten."
**Why this is wrong:** Every other violation class the block can file has a matching author-side remedy in R2/R6 — missing preamble → "inserting a missing preamble"; duplicate section → R6 merge; malformed row → "repairing the field … names". The in-scope-P0 violation has none. It names no field (it names "the ceiling"), so R2(a) does not apply; `Finding` (which carries the severity) is explicitly never rewritten; the row is never deleted by the skill. Folding the finding at every site does not help either: R5 says the row stays after a fold, and the block's test is unconditional ("whatever else it satisfies"), so the same P0 re-fires every round. The gate sums P0/P1 from the `STATUS` lines (`skills/spec-cycle/SKILL.md:415-418`), so `total_p0p1` can never reach 0 for that invocation — a single mis-routing burns all four rounds and halts red, which is precisely the failure mode the brief was filed to stop (brief § Why it matters). The second entrance into the same trap: the block also says a `Scope` "wrong in a way that changes the routing (an in-scope P0 recorded as out-of-scope)" is a violation naming the failing field; repairing that field per R2(a) converts the row into an in-scope-P0 row, i.e. into the permanent violation. The only exit the spec names is outside the loop — the minor-additions bullet's "the operator is the GC … may be dropped by hand" (spec.md:51) and 2f option 1, both reachable only after round 4 (`SKILL.md:468`).
**Suggested fix:** Give R2 a third permitted edit and teach the block to honor it. In R2: "(c) discharging a row the reviewers filed a ceiling-class `routing violation: D-<n>` against: fold the finding at every site on its `Propagation sites` list and append one field, `**Discharged:** folded round <n> — § <a>; § <b>`. The finding record is still not rewritten and the row is still not deleted." In the Design 7 block, qualify the ceiling test: "…is itself a routing violation whatever else it satisfies **unless the row carries a `Discharged:` field naming the sections the fold touched, which the lens verifies like any `fixed:` disposition**". Add the field to Design 5's render (or state it is not rendered) and to the well-formedness enumeration as an optional eighth field, and add a checklist row greping `Discharged:` once in SKILL.md and once per agent.

### F-2: The section-extent grammar ("to the next `##` heading") is terminated by the row headings it is supposed to contain
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 2 (spec.md:78), § Design 5 (spec.md:133), § Design 7 block (spec.md:148)
**Claim:** All three state the section "runs from its heading to the next `##` heading that is not inside a blockquote, or to end of file", and Design 5 then says "the render treats every `###`-or-deeper heading in that span … as a row".
**Why this is wrong:** Rows are `### D-<n>:` headings (spec.md:85). A consumer that reads "the next `##` heading" as "the next line beginning `##`" — which is how the sentence is literally written, and these consumers are LLMs following prose, not a CommonMark parser — terminates the span at the first row, so the span contains zero rows, the render always prints `(none)`, and the reviewers see no rows to suppress against. That failure is silent, and Design 6 (spec.md:140) actively mis-attributes it: "A spec that carried rows in a prior round and renders `(none)` now is the signature of a truncated write." The spec is otherwise precise about this grammar (it pins the blockquote exclusion and the `> `-prefix rule), so the imprecision here stands out.
**Suggested fix:** In all three places write "to the next level-2 heading (exactly two `#`) that is not inside a blockquote, or to end of file; a `###`-or-deeper heading does not end the section." Add to test row 6 a per-agent `grep -cF 'exactly two'` ≥ 1 and to row 8 the same for SKILL.md.

### F-3: Design 3's revert is not reconciled with the untouched "Do not delete history" bullet at `:432`
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 3 (spec.md:110); § Design 1 closing note (spec.md:72) and § Scope "Left alone" (spec.md:23)
**Claim:** Design 3: "**revert the original fold** (remove the edit from every site it touched)". Design 1: "The existing P2 bullet (`:431`) and the 'Do not delete history' bullet (`:432`) are unchanged."
**Why this is wrong:** `skills/spec-cycle/SKILL.md:432` reads "Do not delete history of what changed; if a section is rewritten, that's fine, but the spec at end of round must stand on its own." The revert is the one operation in the whole design that deletes a prior round's recorded change, and it sits ~40 lines above that bullet in the same section. The spec reconciles every other tension of this kind explicitly (the `:446-462` closed-issues supersession, R3 vs 2g, the 2f-i step-4 carve-out) but leaves this one silent, so the author executing 2e in round 3 is reading two instructions that appear to conflict with no stated precedence.
**Suggested fix:** Add one clause to Design 3's revert bullet, landing in the same 2e insertion: "This is the one sanctioned removal of a prior round's edit; the history the `:432` bullet protects is preserved by the deferral row (which carries the finding record verbatim) plus the extra round-qualified manifest line, so the bullet is satisfied without editing it."

### F-4: D13 and R6 give conflicting matching rules, and the rule R6 relies on never reaches the reviewer
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D13 (spec.md:46), § Design 2 rule R6 (spec.md:103), § Design 7 step 3 (spec.md:150)
**Claim:** D13: "Reviewers match on `D-<n>` and the row title, **never on the finding id**." R6: "a manifest line citing a renumbered `D-<n>` is verified against the row's `Finding:` field, **not its id**."
**Why this is wrong:** The two sentences prescribe opposite matching keys for the same act, and R6's is written in the passive with no actor. If the actor is the reviewer, the instruction is unimplementable: D11 forbids agents from reading SKILL.md ("Agents have no include mechanism and must not read the skill file by an install-specific path"), R6 lands only in SKILL.md, and the agent-facing text (Design 7 item 2, spec.md:148) contains nothing about renumbering — while Design 7 step 3 says flatly "If no row `D-<n>` exists, mark the finding REOPENED", producing a false P0 for exactly the renumbered row R6 was written to protect. If the actor is the author (writing the manifest in 2b), R6 is fine but D13's "never on the finding id" reads as forbidding it.
**Suggested fix:** Make R6 author-side and explicit: "…when the author builds the next manifest, a line citing a renumbered row is written with the row's **new** `D-<n>`, verified against the row's `Finding:` field; the reviewer is never shown a stale id." Then D13 needs no change and Design 7 needs no renumbering clause.

### F-5: D16's re-run sentence over-states and contradicts Design 3's per-invocation scoping
**Severity:** P2
**Where:** spec § D16 (spec.md:49) vs. § Design 3 (spec.md:107)
**Claim:** D16: "On a re-run there is no in-context fold record, so the recount does not run at all and the new finding is routed by Design 1 with no recount suffix."
**Why this is wrong:** Design 3 scopes the recount to "the manifests built earlier in **this invocation**". A re-run is an invocation: its rounds 2 and 3 build manifests and therefore do have in-context fold records, so the recount does run for folds made during the re-run. Read literally, D16 disables the recount for the entire re-run — and re-runs are the specimen scenario the brief names (VHS-33 attempt 1, VHS-41 attempt 1). Only round 1 of a re-run is recount-free, and for the same reason round 1 of any invocation is.
**Suggested fix:** "On a re-run, a fold made in a **prior** invocation leaves no in-context record and is never recounted; the re-run's own rounds 2–3 recount their own folds exactly as any invocation does. No round directory is scanned."

### F-6: One root is filed twice per lens when a row records an in-scope P0
**Severity:** P3
**Where:** spec § Design 7 block (spec.md:148), § Decisions 1 (spec.md:31)
**Claim:** The block files `routing violation: D-<n>` for an in-scope-P0 row, and D14's exception says an in-scope P0 candidate "is always filed with the row cited as context".
**Why this is wrong:** Both fire on the same row in the same round, so one defect contributes 2 to `total_p0p1` per lens (up to 8 with four lenses). Decision 1's stated property is that "the number the operator reads is the number of live findings that are not deliberately deferred"; a 2× (or 8×) multiplier on one root works against that reading, and the block's own "file it once" only dedupes within a violation class.
**Suggested fix:** Add to the block: "When you file the underlying in-scope P0 under the D14 exception, do not also file the ceiling `routing violation` for that row — the P0 finding cites the row and names the ceiling in its `Why this is wrong`." (This also pairs cleanly with F-1's discharge path.)

### F-7: Three off-by-one line anchors
**Severity:** P3
**Where:** spec.md:101 (`:288`), spec.md:101 (`:599-601`), spec.md:23/49/74 (`:446-462`)
**Claim:** R4 cites "the escape Phase 0's re-run pin already names (`:288`)"; R4 cites 2g's idiom "at `:599-601`"; three places cite the closed-issues manifest as `:446-462`.
**Why this is wrong:** `SKILL.md:288` reads "prior on-run, edit or remove the recorded scale Decision in the spec (or" — the delete-the-spec escape is on `:289`. 2g's "If a `## Post-green polish` section already exists" idiom spans `:600-601`; `:599` is the tail of the preceding sentence. The closed-issues manifest bullet is `:446-461`; `:462` is the first line of the "Blank-slate rewrites are forbidden" bullet (the byte-identical assertion still holds, since `:462` is also unchanged).
**Suggested fix:** `:288-289`, `:600-601`, `:446-461`. The Scope preamble's re-verify instruction covers the risk, but the citations are cheap to correct.

## Summary
P0: 0 | P1: 1 | P2: 4 | P3: 2 | P4: 0

STATUS: RED P0=0 P1=1 P2=4 P3=2 P4=0
