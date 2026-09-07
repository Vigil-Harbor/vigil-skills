# Conventions Review — round 4

Grounded: spec and brief read fresh; `AGENTS.md` and both `CLAUDE.md` files read; all three round-3 reports read; every `grilling` / `spec-cycle` / `spec-brief` anchor the round-4 changes touch re-verified live at `7403cb5`. `scale_lens == off` and no `scalability.md` exists in `round-3/` — nothing to ignore.

## Closure of round 3 findings

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Design 4's post-cap rule amends `grilling:23` | CLOSED | Rule removed. spec:483–492; `:23`/`:57` listed unchanged in Scope (spec:28); row 8 (spec:843–845) asserts both byte-identical; § Deferred spec:1055–1061 + Risks 7 (spec:993–998). D9 (spec:157–165) keeps "the resume contract" in row 4's surviving list, now true again |
| correctness | F-2 (P1) | `:108` amended, `:151`/`:148` not | CLOSED | Design 2 spec:347–362; Scope cell spec:28 names all three bullets individually; rows 4 (spec:800–802) and 7 (spec:833–834) |
| correctness | F-3 (P2) | Precedence chain omits `fact not established`, ranks Q-only values | CLOSED | Two orders, one per shape, spec:308–338; row 4 spec:793–798 |
| correctness | F-4 (P4) | "eight-section" brief template | CLOSED | spec:883–885 reads "nine-header … one of them the conditional `## Scale`" |
| edge-cases | F-1 (P0) | No entry for `fact not established`; rule 3 self-contradicts | CLOSED | spec:304–338; rule 3 spec:442–448 now cites the F-item ranking |
| edge-cases | F-2 (P1) | `:151` restates the reversed rule | CLOSED | as correctness F-2 |
| edge-cases | F-3 (P2) | `## Out of scope` third empty header | CLOSED | spec:695–701; Risks 6 (spec:987–992) now names two headers; row 12 spec:879–882 |
| edge-cases | F-4 (P2) | Preserved post-cap round no caller can spend | CLOSED (deferred, accepted) | Rule dropped; two-file reason at spec:487–492 and spec:1055–1061 |
| edge-cases | F-5 (P2) | "Dispatched once" vs the resume contract | CLOSED | spec:433–437; row 7 spec:831–832 |
| edge-cases | F-6 (P2) | Demoted `deferred to option 3` invisible | CLOSED | `also settled (left open)` spec:613–622; row 10 spec:856–858 |
| edge-cases | F-7 (P2) | Roll-up narrowing vs conservative reporting | CLOSED (by removal) | spec:245–253; row 6 spec:817–819 asserts "no narrowing"; roll-up no longer lists it |
| edge-cases | F-8 (P2) | Preview shows two empty lists, Phase 4 writes an item | CLOSED | spec:679–683; row 12 spec:872–875 |
| edge-cases | F-9 (P3) | `revised-after-cap` absent from the chain | CLOSED | spec:317–318; row 4 spec:796–797 |
| edge-cases | F-10 (P3) | `:132` bound vs never-rendered overflow F-items | CLOSED | D13 spec:197–205; `:132` added to Scope cell and roll-up spec:66–67 |
| conventions | F-1 (P1) | `## Failure modes` `:148`/`:149`/`:151` unamended | CLOSED | Design 2 spec:347–362; Scope cell spec:28; rows 4 and 7; roll-up spec:62–65 |
| conventions | F-2 (P2) | All-or-none report renders outside the block `:116` pins | **PARTIAL** | Option (a) taken in Design 1 (spec:227–239) and Scope (spec:28), but not propagated to Design 2's authoritative block, Design 4's closing line, or row 6's stale clause → F-1 and F-2 below |
| conventions | F-3 (P2) | § Deferred's blanket coverage claim false for correctness R2 F-5 | CLOSED | spec:1065–1069 names it closed-not-deferred and gives the mechanism |
| conventions | F-4 (P3) | Two spec-level additions missing from the roll-up | CLOSED | spec:84–86, spec:90–92 |
| conventions | F-5 (P3) | Preamble's relation to `question_cap` unstated | **PARTIAL** | Design half closed (spec:540–544, correct against `grilling:85`). Row 9 (spec:846–850) still asserts only "the definition of the optional one-line round preamble" → F-3 below |
| conventions | F-6 (P4) | `:104`'s exit enumeration not gated | CLOSED | Row 8 spec:842–843; verified `grilling:104` lists five exits today |

## Findings

### F-1: The spec disagrees with itself about whether the hand-off header's `reason:` enumeration changes

**Severity:** P0
**Where:** spec.md:280 and spec.md:500–501, against spec.md:28, spec.md:232–233 and spec.md:820–821
**Convention violated:** the cross-surface rule — the wire format between the primitive and its callers must be locked, not implied; and the spec's own declaration at spec.md:275–277 that Design 2 is where every other design's change appears.
**Evidence:** Design 1 relocates the all-or-none violation report onto the header (spec.md:232–233): "**and on the hand-off header's `reason:` field** as `partially identified seed — ref: omitted` on every exit that renders the block." The Scope table agrees (spec.md:28) and checklist row 6 gates it (spec.md:820–821).

Two other places say the opposite:

- spec.md:275–277 calls Design 2 "the authoritative rendering. Everything the other designs change appears here in one place" — and its header line (spec.md:280) reproduces the live enumeration unchanged: `reason: tree fully visited | no candidate decision met the altitude fence | cap reached | operator stop | resume`. Verified byte-for-byte against `skills/grilling/SKILL.md:119`. The new value is absent.
- spec.md:500–501 (Design 4): "The header's exit enumeration gains `fence-empty`; **the reason enumeration is unchanged.**"

Checklist row 4 pins Design 2's block; row 6 pins the value Design 2's block omits. `## Test command` is `N/A`, so the checklist is the whole gate — it now asserts both sides of a contradiction without comparing them, the same failure class as edge-cases R3 F-1.

There is also no composition rule. `partially identified seed — ref: omitted` is required "on every exit that renders the block", but `reason:` is single-valued in the template. A partially identified seed on an `empty-frontier` exit has two reasons and no stated rendering.
**Suggested fix:** In Design 2's block, extend the header's reason enumeration to `… | resume | partially identified seed — ref: omitted`, and add one sentence stating the composition. Change Design 4's closing line, or delete the "unchanged" clause and defer to Design 2. Row 4 should assert the enumeration as a whole rather than only the exit list.

### F-2: Checklist row 6 still mandates the above-the-header rendering Design 1 explicitly rejects

**Severity:** P1
**Where:** spec.md:816–817 (row 6), against spec.md:234–239 (Design 1, Reporting)
**Convention violated:** the same `:116` wire-format lock the round-3 fix was taken for; the one-rule-one-place discipline conventions R3 F-1 was raised under.
**Evidence:** Design 1 now says, with its rationale: "**Not on a line above the header:** `skills/grilling/SKILL.md:116` says the block is rendered *exactly*, and 2f-i appends 'the returned Grill summary verbatim' starting at the `## Grill summary` header (`spec-cycle:523`), so a line above it never reaches `grill.md`." Verified live.

Row 6 was not updated with it:

```
the all-or-none rule **with both its consequences** — no `ref:` field at all for the
whole interview, and the report on the first rendered line (round preamble, or
immediately above the `## Grill summary` header when no round renders);
```

An implementer satisfying row 6 writes into `skills/grilling/SKILL.md` exactly the rule Design 1 forbids — and on the one path it matters (`fence-empty`, where no round renders and 2f-i is the only caller supplying ids), the report is then stripped by `spec-cycle:523`'s verbatim append, which is the failure round-3 F-2 was filed for. Row 6 carries both answers: the stale clause and the new `reason:`-field assertion four lines later.
**Suggested fix:** Replace the parenthetical with "(the round-1 preamble where a round renders, **and** the hand-off header's `reason:` field on every exit that renders the block; no line above the header — `:116` is unchanged)". Keep the existing final sentence.

### F-3: Row 9 does not gate the preamble's exemption from `question_cap`, so Out-of-scope fence 1 stays on inference at the gate

**Severity:** P3
**Where:** spec.md:846–850 (row 9), against spec.md:540–544 (Design 5)
**Convention violated:** with `## Test command` = `N/A`, a rule the checklist does not assert is not gated. Out-of-scope 1 (spec.md:932–933) bars "any change to the three bounds"; `grilling:85` defines bound 2 as "At most `question_cap` **rendered items** per round".
**Evidence:** Design 5 states it correctly: "**The preamble is not a rendered item.**" Row 9 asserts only "the definition of the optional one-line round preamble" — which a preamble defined as a rendered item would also satisfy.
**Suggested fix:** Row 9: "…and the definition of the optional one-line round preamble, **stated as not a rendered item — it does not count against `question_cap` and never appears in the hand-off block**."

### F-4: The resume rule for Open F-items carrying a claim qualifier is a spec-level addition absent from the drift-check roll-up

**Severity:** P3
**Where:** spec.md:433–437 (Design 3 rule 1), against spec.md:56–96 (roll-up)
**Convention violated:** the roll-up's stated purpose — `spec-cycle:636` renders the Phase 3 drift-check from the *brief's* decision list, so the roll-up is the only surface on which a spec-level addition reaches the HARD STOP.
**Evidence:** Rule 1's third paragraph adds a new rule governing resume behaviour. Neither brief decision 4/5 nor the ticket says anything about resumes, and the brief's `grilling` Scope row does not list the invocation contract's resume semantics as changing. The nearest roll-up bullet (spec.md:72–73) does not name it — and it is the one addition that qualifies the semantics of a line (`:23`) checklist rows 5 and 8 protect verbatim and D9's argument rests on. Row 7 does gate it, so this is disclosure, not a hole.
**Suggested fix:** Add one roll-up bullet naming it.

## Verified, not findings

- **The newly declared amendments stay inside the brief's fence, and are disclosed.** `:104` and `:132` sit inside the brief's own declared ranges (`:102–112`, `:114–135`) and are named in the Scope table; `:132` is additionally in the roll-up. `:148`/`:149`/`:151` sit outside the brief's enumerated "Current" ranges but are consequences of authorized changes under the file's own single-source-of-truth pattern (the one Design 2 already applies to `:74`/`:88`) — each is named individually in the Scope cell, `:151` in the roll-up's precedence bullet, `:148`/`:149` in their own bullet, and all three in rows 4 and 7. None touches the three bounds, the fork form or the advisory rule; the only fact-finding-dispatch contact is `:76`'s retry, whose narrowing Out-of-scope 9 discloses in terms.
- **§ Deferred and § Risks are truthful.** All five § Deferred entries check out against the reports they name; the closing sentence now says "round-1, round-2 **and round-3**" and its claim survives a walk of every round-3 P2+ finding. Risks 5, 6 and 7 correctly mirror the three accepted deferrals, and Risks 7's two-file reason (`grilling:23` + `spec-brief:105`) is verified against both live lines.
- **Both removals left the spec consistent.** The post-cap rule leaves no residue: Scope, row 5, row 8, § References, D9 and Risks 7 all agree that `:23` and `:57` are untouched, and D9's nine-leg "extends" argument is whole again. The dropped narrowing is likewise clean — no residual `also edited`, Design 1's inheritance and row 6 both say "no narrowing", and the roll-up no longer lists it.
- **No premature abstraction, no unneeded backwards-compat, no duplicate-vs-reuse drift.**
- **"Files to leave alone" still holds.**

## Summary
P0: 1 | P1: 1 | P2: 0 | P3: 2 | P4: 0

STATUS: RED P0=1 P1=1 P2=0 P3=2 P4=0
