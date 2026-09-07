# Conventions Review — round 1

## Closure of round 0 findings

N/A — round 1.

## Findings

### F-1: Checklist row 3 asserts `grep -c '^###'` → 0, which is false today and contradicts row 10
**Severity:** P0
**Where:** spec.md:449 (`## Test plan` row 3); contradicts spec.md:157–159 and spec.md:496
**Convention violated:** Repo convention that the review checklist *is* the `/ship-spec` gate when `## Test command` is `N/A` (spec.md:425–426; VHS-33 spec `## Test plan` preamble). A gate row that cannot pass by construction blocks the ship.
**Evidence:** `skills/grilling/SKILL.md` currently has three `^###` markers — `:123 ### Settled`, `:126 ### Open frontier`, `:131 ### Facts established`. `grep -c '^###' skills/grilling/SKILL.md` → **3**, and grep does not skip fenced blocks. The spec's own Design preamble says so: *"the file's only `###` markers are inside the fenced hand-off block"* (spec.md:157–158). Checklist row 10 (spec.md:497) simultaneously requires `### Settled` / `### Open frontier` / `### Facts established` to still be present verbatim, re-asserting VHS-33 row 5 / VHS-32 row 4. So row 3 contradicts row 10, the file, and the spec's own rationale.
**Suggested fix:** Replace the assertion in row 3 with one that expresses the actual intent (no *new* heading outside the fence). Either `grep -c '^###' skills/grilling/SKILL.md` → **3** (unchanged: the three hand-off subsections), or better, `git diff -U0 -- skills/grilling/SKILL.md | grep '^+' | grep -v '^+++' | grep -c '^+###'` → 0.

---

### F-2: Design 6's resume rule contradicts the unedited resume contract at `:23`, and the "silence" rationale misreads it
**Severity:** P1
**Where:** spec § Design 6 (spec.md:291–305); D9 (spec.md:124–128)
**Convention violated:** The spec's own displacement idiom — when a new rule overrides an existing unedited sentence, the *shipped* text says so (Design 4, spec.md:252–255: *"For checks alone this displaces the failed-dispatch rule above…"*). Design 6 omits that and instead justifies itself with a claim about `:23` that the file does not support.
**Evidence:** `skills/grilling/SKILL.md:23` reads, in full:

> **Resume contract.** Rebuild the tree from the summary. Settled items stay settled except the named one and everything downstream of it, which re-enter the frontier. **Prior Open items stay Open and are not re-asked unless they are downstream of the revised decision.** Facts established carry over and are not re-dispatched.

The spec asserts (spec.md:296, 299–300) *"The resume contract's silence on Open F-items"* and *"says nothing about Open F-items"*. That is not silence: since VHS-33, an F-item **is** an Open item (`skills/grilling/SKILL.md:128`), fact requests are rendered items the operator answers by number (`:53` — `F1 <answer>`), and `:90` already routes a twice-unanswered fact request into an Open item. So `:23`'s "unless they are downstream of the revised decision" reaches Open F-items on its face — and Design 6's shipped text says the opposite ("including an Open item that is downstream of the revised decision"). Two rules in one prompt file, in direct conflict on a load-bearing behavior, in a contract three callers parse. The reader is left to infer that the more specific rule wins; the primitive's other overrides never rely on that inference.
**Suggested fix:** Make the shipped paragraph carry the displacement explicitly, in the Design 4 idiom — e.g. *"For `F<n>` items this displaces the resume contract's 'unless they are downstream of the revised decision' clause: every Open `F<n>` carries over as Open and is not re-dispatched, downstream or not."* Then drop the false "silence" claim from Design 6's "Why not edit `:23`" note and from D9, and add a checklist row asserting the displacement phrase is present. (Editing `:23` is the alternative — see F-3/F-4 on whether that is actually fenced.)

---

### F-3: The spec supersedes a recorded wiki decision without naming it
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Design 11 (spec.md:372–388) and § Design 8 (spec.md:328–344); the spec cites no `decisions/` page anywhere
**Convention violated:** Repo practice that a spec names the prior decision it supersedes or narrows. VHS-33 did exactly this ("Supersedes VHS-32 checklist row 4/7"), and its wiki page records the narrowing of VHS-32 § 5 in both directions. VHS-36 supersedes VHS-33's wiki decision § 3 and moots its Revisit-when trigger, silently.
**Evidence:** `vigil-harbor-wiki/decisions/2026-09-07-vhs-33-the-hand-off-carries-ids-and-a-hollow-brief-is-a-success.md` § 3 records:

> **Rejected — a cause qualifier on the F-item text** (`stopped` vs `fact not established` mapped to different Risks wording). Fenced by brief decision 12; two words if wanted later.

Design 11 adopts precisely that rejected shape: a cause qualifier on the F-item mapped to different `## Risks / decisions` wording in `/spec-brief` Phase 4. Separately, the same page's header reads:

> Revisit when: VHS-36 lands operator-supplied facts (**a `source: operator` shape**, claims-to-verify)

— and this spec *forbids* `source: operator` outright (Design 9, spec.md:348–353). Both are fine outcomes and both are brief-authorized; neither is acknowledged. The spec's meticulous supersede bookkeeping stops at the VHS-33 *spec* checklist and never reaches the wiki decision layer, which is the layer `/spec-close` harvests.
**Suggested fix:** Add one line under D7 or Design 11 — e.g. *"This adopts the qualifier VHS-33 wiki decision § 3 recorded as Rejected-for-now, and settles that decision's Revisit-when trigger against `source: operator`: it is prohibited, not shaped."* — so `/spec-close` decomposes it rather than inferring it.

---

### F-4: "The VHS-33 fence over `:19–32`" is a prior spec's diff-scope assertion, not a standing fence
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec.md:127–128 (D9) and spec.md:301 (Design 6, "Why not edit `:23`")
**Convention violated:** Distinguishing a carried fence (binding on this spec) from a prior spec's assertion about *its own* diff. The spec's carried fences come from the brief's `## Out of scope`, which does not list the resume contract.
**Evidence:** VHS-33's checklist row 9 reads *"`git diff -U0 -- skills/grilling/SKILL.md` shows **no hunks** in `:1–17`, `:19–32`, …"* — a statement scoped to VHS-33's own diff, framed as "invocation apart from the seed bullet, resume contract, …". The VHS-36 brief's carried-fence list (brief.md:52) is: *"the three bounds, the fork form, the advisory-recommendation rule; the size-bound sentence `skills/grilling/SKILL.md:137` byte-identical; `docs/specs/DONE/` never edited."* The resume contract is not among them, and the VHS-33 wiki decision's "Not changed, on purpose" list does not name it either. So editing `:23` is available to this spec — it is a design choice, not a constraint — and treating it as a fence is what forces the F-2 contradiction.
**Suggested fix:** Reword both places to state the choice honestly: *"`:23` is left unedited by choice — the rule lives beside the dispatch rules it bounds — not because VHS-33 fences it."* Combined with F-2's explicit displacement sentence, this closes the loop.

---

### F-5: The no-hunk fence skips `:18`, and VHS-33 checklist row 7 (the `ref:` machinery) is never re-asserted
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Test plan rows 9 and 10 (spec.md:482–500)
**Convention violated:** The re-assert discipline this spec sets for itself (spec.md:337–338: *"the Test plan below re-asserts every other clause of that row unchanged, as VHS-33 did for VHS-32 row 4"*) and applies to VHS-33 rows 4, 5, 6, 9, 11, 12, 13, 16 — but not row 7.
**Evidence:** Row 9's fenced ranges are `:1–17`, `:19–32`, `:33–68`, `:70–78`, `:82–108`, `:111–127`, `:129–142`, `:144–150`. The gap at `:18` is the `seed` bullet — the line VHS-33 edited to add `id` / `ref:` — and it is the one non-blank content line in the file that neither the fence nor any positive assertion covers. (`:69`, `:79`, `:81`, `:109` are blank; the rest are the edited lines.) The ranges look copied from VHS-33 row 9, where `:18` was excluded *because VHS-33 changed it*; here it has no reason to move. VHS-33 row 7 also pinned `grep -c 'ref:' skills/grilling/SKILL.md` ≥ 7 and the callers-map sentence — row 9's `:129–142` covers `:135`/`:139` as a diff fence, but the file-level count assertion is dropped.
**Suggested fix:** Change row 9's first range to `:1–32` (dropping the now-redundant `:19–32`), and add to row 10: *"Re-asserts VHS-33 checklist row 7: the `seed` bullet (`:18`) contains `id`, `ref:`, and 'no `ref:` field is rendered at all'; `grep -c 'ref:' skills/grilling/SKILL.md` ≥ 7."*

---

### F-6: The deferred size-bound item names no ticket ID
**Severity:** P3
**Where:** spec § Out of scope (spec.md:579–581)
**Convention violated:** The repo's defer convention — a valid, out-of-scope, non-trivial finding gets a filed ticket cited by ID, not a prose "its own ticket". Every other cross-reference in this spec and brief carries an ID (VHS-33, VHS-34, VHS-36, VHS-37, PR #26 thread 3945500860).
**Evidence:** The spec says *"(CodeRabbit PR #27 round 3, declined on the VHS-33 fence and still open as its own ticket)"*. The VHS-33 wiki decision says only *"a tighter bound is its own ticket"* — also unnamed. A search of the Plane mirror (namespace `skills`) for the Open-frontier size bound returns only VHS-33 and VHS-36; the brief's follow-up list names VHS-34 and VHS-37 for unrelated work. If the ticket exists it is uncited; if it does not, "still open as its own ticket" overstates the disposition.
**Suggested fix:** Cite the ticket ID, or change the wording to *"to be filed as its own ticket"* and file it before `/ship-spec`.

---

### F-7: Design 3 introduces the first bullet list inside § Fact-finding, and row 3's "eight paragraphs" miscounts the run
**Severity:** P3
**Where:** spec § Design 3 (spec.md:218–229); checklist row 3 (spec.md:442–449)
**Convention violated:** § Fact-finding's established idiom — bare bold-lead paragraphs, no sub-lists. `skills/grilling/SKILL.md:72`, `:74`, `:76`, `:78`, `:80` are five plain paragraphs; the section contains no bullet today. (Bullets exist elsewhere in the file — `:65–68`, `:153–156` — but never nested under a bold lead.)
**Evidence:** Design 3 renders as a bold-lead paragraph plus a two-item bulleted list, making the inserted run ten markdown blocks, not the "eight paragraphs" row 3 asserts (it counts bold leads). With the unwrapped rule (spec.md:149–152), each bullet must ship as one long line; nothing in the test plan asserts that.
**Suggested fix:** Either fold the two outcomes into the paragraph like every other bold lead in the section, or keep the bullets and (a) say in the Design preamble that the sub-list is a deliberate first for this section, and (b) reword row 3 to "eight bold-lead blocks" and add *"each of the two `**Two outcomes.**` bullets is one line."*

---

### F-8: Row 6's grep pattern is broken by a markdown backtick escape
**Severity:** P4
**Where:** spec § Test plan row 6 (spec.md:465)
**Convention violated:** Checklist rows are copy-pasteable commands (rows 1, 2, 7, 14 all are).
**Evidence:** The row reads `` grep -c 'stopped\` is reserved' skills/grilling/SKILL.md ``. A backslash does not escape a backtick inside a markdown code span, so the span terminates after `stopped\` and the rest renders as prose; copied into a shell, the single-quoted pattern contains a literal backslash and matches nothing.
**Suggested fix:** Use a double-backtick span with padding, or drop the backtick from the pattern: `grep -c 'is reserved for a fact need nobody answered'`.

---

### F-9: The `:143` prohibition list mixes semicolon and comma separators
**Severity:** P4
**Where:** spec § Design 9 (spec.md:350–353)
**Convention violated:** `skills/grilling/SKILL.md:143` is a semicolon-separated list of prohibitions ending in a period.
**Evidence:** The proposed replacement ends *"…answers a decision on the operator's behalf; records an operator's claim as an established fact, **or** writes `source: operator`."* — the final item switches to a comma-plus-`or`, so "records … or writes …" reads as one prohibition where the spec means two.
**Suggested fix:** *"…answers a decision on the operator's behalf; records an operator's claim as an established fact; writes `source: operator`."*

---

## Notes on things that check out

- **Silent-addition scan (category d): none.** Every load-bearing Design item traces to a brief decision, and the three items the brief explicitly left to the spec author (verification-prompt bound, fresh-`F<n>` numbering, precedence sentence — brief.md:61) are each flagged as such in the spec (spec.md:180–182, 261–264, 323–326). That is category (c) done correctly.
- **No premature abstraction.** The spec actively declines a new source class, a new hand-off section, a `refuted` reason value, and an evidence-carrying reason value (§ Out of scope). It adds exactly one value to one existing enum.
- **No backwards-compat shims.** Nothing renamed, re-exported, or flag-gated.
- **Public-repo / harness-neutrality holds.** No proposed shipped line names `Explore`, `Agent`, `Skill`, or a model; Design 1's *"the same agent class … as any other fact dispatch"* correctly inherits `:72`'s parenthetical rather than restating a harness binding. `lint.py`'s R2 only fires on `mcp__*` names, so row 2's broader grep is a manual convention check — inherited unchanged from VHS-33 row 2, which is right.
- **Reviewer agents untouched;** `agents/` is fenced by row 15. No `model:` / effort proposal anywhere.
- **Anchor line numbers verified at `f4d9290`** (HEAD): `skills/grilling/SKILL.md` `:23`, `:53`, `:72`, `:74`, `:78`, `:80`, `:110`, `:128`, `:137`, `:143`, `:153–156`; `skills/spec-brief/SKILL.md` `:140`/`:141`/`:142`; `docs/spec-workflow-reference.md` `:31`/`:35`. All correct. The claim that `docs/spec-workflow-reference.md` is unwrapped is also correct.
- **The VHS-33 row-4 supersede/re-assert split is accurate** — VHS-36 row 4 reproduces every clause of VHS-33 row 4 except the F-line reason set, which is the one line it changes.

## Summary
P0: 1 | P1: 1 | P2: 3 | P3: 2 | P4: 2

STATUS: RED P0=1 P1=1 P2=3 P3=2 P4=2
