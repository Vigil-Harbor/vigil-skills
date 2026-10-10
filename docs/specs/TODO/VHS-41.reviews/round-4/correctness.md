# Correctness Review — round 4

## Closure of round 3 findings

Grounding note: `AGENTS.md` was last touched **2026-09-06** (`d381f88`, VHS-32) — inside the 7-day window. I re-verified both anchors the spec edits: `AGENTS.md:7` still reads `no build step, no test suite, no dependencies…` and `:46` is the `### /review-pr` heading with the paragraph at `:48`. No drift. `skills/review-pr/SKILL.md` last changed 2026-08-18 (`5b3da4c`); it is 406 lines, as the spec states, and every anchor the spec cites (`:11 :61 :68 :69 :75 :76 :79 :81 :83 :85 :95 :96-107 :109-114 :120 :125 :127 :131-138 :140-144 :152-158 :162 :172 :174-175 :180 :186 :194-195 :198 :200 :209 :215 :217 :224-226 :233 :234 :241 :243 :245 :252 :262 :273 :277 :279 :281 :283 :290 :316 :331 :341-342 :345 :351-368 :362 :370-377 :379-406`) resolves to what the spec says it does. All 20 measurable "Pre" values in the test plan reproduce exactly (rows 4–22, incl. pytest `1 failed, 158 passed, 3 skipped` and `0 error(s), 1/2 warning(s)`). `gh api --jq --arg self x '…'` → `accepts 1 arg(s), received 3` ✓; `gh` is 2.87.3 ✓; `mkdir -p` precedent in `spec-close/SKILL.md:333` ✓; no `date +%s` precedent ✓; four `scripts/` subtrees ✓; `docs/portability-contract.md` §4 case 1 ✓; `docs/authoring-portable-skills.md:41` ✓; `sync.py:155 cmd_status` returns `None` ✓. `lint.py`'s only ERROR rule is `operative-tool-call` on `mcp__*` plus `requires-malformed`, so the new prose cannot introduce an ERROR — gate rows 1–2 hold.

| Lens | ID | Title | Status | Evidence |
|---|---|---|---|---|
| correctness | F-1 (P0) | Unfetchable strings say "excluded from the resume mark" | CLOSED | spec.md:1470 (`counted as handled; not retried`), spec.md:1540 (`counted as handled so the resume mark passes them`) |
| correctness | F-2 (P1) | Decision 14 classifies `403` non-retryable | CLOSED | spec.md:679-680; matches Decision 12 (spec.md:456) and D9 (spec.md:1626-1628) |
| correctness | F-3 (P1) | 2b step 2 sources candidates from stale fetch (b) in rounds 2+ | CLOSED | spec.md:924-931 — source is now per-invocation |
| correctness | F-4 (P2) | 6f post condition restated with two arms | CLOSED | spec.md:113-116, 852-856 both now three-armed / defer to Decision 12 |
| correctness | F-5 (P2) | `HANDLED_THROUGH` circular on "a posted comment" | CLOSED | spec.md:486-489 — "or in the comment this round is about to post" |
| correctness | F-6 (P3) | D7 asserts the narrow cleanup rule | CLOSED | spec.md:1455 defers to D1 |
| edge-cases | F-1 (P1) | `test("\\S")` aborts both comment queries | CLOSED | spec.md:909, 1417 use `[^[:space:]]`; rationale 566-572; row 19 pins the `\\S` form out |
| edge-cases | F-2 (P1) | Error JSON re-parsed as a clean zero-item body | CLOSED | spec.md:955 (`rm -f` on non-zero exit), 1003-1008 (missing capture ⇒ fetch failure) |
| edge-cases | F-3 (P2) | Session-condition rule evaluated where info doesn't exist; `404` not `403` | CLOSED | spec.md:968-980 ("provisional until every fetch … has returned"); Decision 12 spec.md:462-468 |
| edge-cases | F-4 (P2) | `new_body_items` counts bound-deferred backlog | CLOSED | spec.md:1282-1294 — `submitted_at > PUSH_TIME` gate added (see F-1 below for the residue) |
| edge-cases | F-5 (P2) | Partial-`--paginate` assumption never verified | CLOSED | spec.md:243-248 + test row 29(iv) |
| edge-cases | F-6 (P2) | `<SCRATCH>` recovery adopts a concurrent run's dir | CLOSED | spec.md:773-782 — exactly-one-or-refuse |
| edge-cases | F-7 (P3) | `POSTED=`/`POST_FAILURE` unpinned | CLOSED | row 17 second command, expected `1`; spec.md:1427-1429 |
| edge-cases | F-8 (P3) | Row 20's `$TMPDIR/` guard makes D1's caution unshippable | CLOSED | row 20 now pins the quoted form `'"$TMPDIR/'`; D1's caution (spec.md:752-754) writes it unquoted — verified non-matching |
| edge-cases | F-9 (P4) | Two factual slips in D1's rationale | CLOSED | spec.md:756-758 — `mkdir -p` precedent named, `date +%s` correctly stated as precedent-free (both verified) |
| conventions | F-1 (P2) | Shipped-text rule omits D7 | CLOSED | spec.md:719-721 now names D7, D1 and D8 |
| conventions | F-2 (P2) | Multi-hit non-retryable override re-opens permanent blindness; D9 bullet lacks it | **PARTIAL** | Semantics fixed and bounded (spec.md:462-468, 968-980: "every attempted review in a set of two or more"). D9's shipped bullet (spec.md:1620-1628) still omits the exception; the rule does ship via 2b step 3, so this is redundancy, not loss. Stays P2 |
| conventions | F-3 (P2) | Monotone-`R` rule vs. worked example disagree | CLOSED | spec.md:494-499 names the worked example canonical; round 2's `r200:h300,400` now derives from the stated rule |
| conventions | F-4 (P3) | Post condition stated in three places, earliest missing an arm | CLOSED | spec.md:96-98 defers to Decision 12 as sole statement |
| conventions | F-5 (P3) | `POSTED=`/`POST_FAILURE` ungated, Decision 7 states token without field | CLOSED | spec.md:267-271 + row 17 |
| conventions | F-6 (P4) | stderr-capture precedent not recorded | CLOSED | spec.md:248-251 (verified: `2>/dev/null` is the only stderr idiom in shipped skills) |
| conventions | F-7 (P4) | D7 claims to mirror `:279` on the rule it contradicts | CLOSED | spec.md:1493-1496 states the deliberate difference |

No REOPENED items. The one PARTIAL is P2 and does not gate.

## Findings

### F-1: The oldest-first bound deferres the run's *own* incremental review, so `new_body_items` is 0 by construction on a bounded round
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D2 2b step 2 (spec.md:924-942), § D5 (spec.md:1274-1294)
**Claim:** "The round's **harvest set** is the **10 oldest** candidates … **The bound applies to every invocation of 2b** — Step 2's harvest, 6a's counting pass, and 6b's triage pass" (spec.md:932-940), and `new_body_items` counts "only those from reviews with `submitted_at > PUSH_TIME`" (spec.md:1283-1285).
**Why this is wrong:** Compose the two. On a first run against a mature PR (>10 unhandled body-carrying reviews), 6a's candidate set is `{40 backlog reviews} ∪ {the incremental review this run's push just triggered}`. The bound takes the ten **oldest**, so the incremental review — the highest id — is deferred out of the harvest set entirely. It is therefore never fetched, never parsed, and cannot contribute to `new_body_items`, which is 0 for structural reasons rather than because nothing new arrived. That defeats the brief's stated rationale for Decision 2 verbatim: "the PR #28 finding lived in the *incremental* review; a fix confined to Step 2 would not have caught it" (brief.md:27, spec.md:66-67). Worse, 6a spends the round parsing ten pre-push backlog bodies — exactly the "backlog drain" the a2r3-F-4 fold says must not happen (spec.md:1288-1291) — while blind to the review it was waiting for. The degradation is bounded (each run advances the marker by ten and the bound line tells the operator to re-run) and loudly reported, so it is not a ship blocker; but it is an unstated consequence of a spec-author bound overriding a brief decision, and the drift-check should see it as a decision, not a lapse.
**Suggested fix:** Add one sentence to 2b step 2 after the oldest-first paragraph: *"A consequence: when the bound binds, the newest review — including the incremental review this run's own push triggered — is among the deferred, so `new_body_items` is 0 for that round by construction and 6a cannot observe it. Contiguity requires oldest-first; the re-run the bound line prescribes is what reaches the newest review."* Optionally cross-reference it from D5's `new_body_items` paragraph.

### F-2: Step 2 now reaches 6a with no verdict review at all, leaving `PREV_REVIEW_ID` undefined
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D1 (spec.md:834-839), § D5 (spec.md:1230-1236, 1240-1249, 1314-1316)
**Claim:** "**If (a) yields no record** … If (b) also yields nothing, fall through to `:83`'s no-reviews report; if (b) yielded bodies, **proceed to the harvest with no verdict**." (spec.md:834-839)
**Why this is wrong:** That sentence opens a run path that `SKILL.md:83` previously closed. Downstream, `SKILL.md:174-178` says "Capture that review's `id` as `PREV_REVIEW_ID`", and D5's converted `:174` query carries the same `select(.state != "COMMENTED")` filter as (a) — so if (a) found nothing, the 6a query finds nothing either and there is no id to capture. Every 6a/6b query is then unsubstitutable: `select(.pull_request_review_id > <PREV_REVIEW_ID>)` at spec.md:1246 and `SKILL.md:225`. The spec shows it is alert to this class of hazard one paragraph earlier — "Do not call (a2) with an unbound `<VERDICT_ID>`: under Decision 14 that errored fetch would be classified as a harvest failure and force `inconclusive`" (spec.md:836-838) — but does not extend the rule to `PREV_REVIEW_ID`. Reaching the state requires the inference Decision 8 flags as unobserved (a body-carrying `COMMENTED` review on a PR with *zero* non-`COMMENTED` CodeRabbit reviews — spec.md:308-312), and the failure degrades safely to `inconclusive` rather than silently, which is why this is P2 and not P1.
**Suggested fix:** Extend spec.md:838-839 to: *"…if (b) yielded bodies, proceed to the harvest with no verdict. In that state `PREV_REVIEW_ID` has no value; substitute `0` in 6a's and 6b's inline queries (every review id exceeds it, so the round triages the full inline set once) rather than leaving the placeholder unbound."*

### F-3: Decision 12's "a re-run over the identical set … is exactly the duplicate the guard exists to suppress" is false whenever the earlier run posted a non-zero `R` for that set
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § Decision 12 (spec.md:427-433, 491-499, 548-560), § D9 edge cases (spec.md:1682-1691)
**Claim:** "A re-run over the identical set with the identical outcome is exactly the duplicate the guard exists to suppress." (spec.md:431-433)
**Why this is wrong:** The guard matches on the full `r<R>:h<IDS>` line (spec.md:548-550, 1417-1418), and `R` is not a function of the harvest set alone — it is `HANDLED_THROUGH` measured over `(PRIOR_MARK, id]`, which differs between a run and its re-run. Worked case: run 1 round 1 harvests `[100, 200, 300]`, 300 fails retryably → floor 300, `HANDLED_THROUGH` 200 → posts `r200:h100,200,300`. Round 2's set is `[300]`; 300 fails again; the monotone rule re-posts `R = 200` → `r200:h300`. Now re-run. `PRIOR_MARK` is 200 (the resume query takes the highest `r`), so the candidate set is `(200, ∞) = [300]` — the *identical* set with the *identical* outcome. But `HANDLED_THROUGH` is now measured over `(200, id]`, where 300 failed, so no id qualifies and, per spec.md:492-494, "`R` is `0`". The marker is `r0:h300`, which does not equal the standing `r200:h300`, so the guard misses and a duplicate posts. (It is self-limiting — the second re-run matches `r0:h300` and is suppressed — which is why this is one spurious comment, not spam.) The shipped D9 bullet at spec.md:1686-1690 ("A **re-run** that hits the same retryable failure recomputes the same set and the same id list and is suppressed … and 6e says so (`dispositions not posted — guard-skipped`)") is *correct within its own scenario* (`PRIOR_MARK = 0` throughout), but Decision 12's generalized sentence is not.
**Suggested fix:** Qualify spec.md:431-433: *"A re-run over the identical set with the identical outcome reproduces the same marker — and is suppressed — whenever `PRIOR_MARK` is unchanged. When the earlier run advanced `PRIOR_MARK` above the failed id, the re-run's `R` falls to the `0` sentinel and the marker differs, so one duplicate posts before the pair converges; tolerated for the same reason the concurrency race is."* Leave D9's bullet as-is (it is scoped correctly).

### F-4: 2b step 2's shipped bound report promises a marker the round may not post
**Severity:** P2
**Pre-ship recommended:** yes
**Where:** spec § D2 2b step 2 (spec.md:936-937)
**Claim:** The shipped report line reads `body harvest bounded: parsed the 10 oldest of <M> unhandled body-carrying reviews; deferred <id, id, …> — this round posts a marker through <R> so a re-run resumes at the deferred ones`.
**Why this is wrong:** Two problems, both in text the skill carries. (i) `<R>` is not known when this line is emitted — Decision 12 computes it at post time, after the fetch pass classifies failures and the floor is recomputed (spec.md:443-449, 491-494). (ii) The promise can be false. 6f's post condition requires `R` to advance past `PRIOR_MARK` (spec.md:1389-1392); if the *lowest* id of the ten fails retryably, the floor drops to it, `HANDLED_THROUGH` yields nothing above `PRIOR_MARK`, `R` stays at the sentinel and does not advance — so no comment posts, no marker lands, and "a re-run resumes at the deferred ones" is exactly what does *not* happen: the re-run recomputes the same set. An operator acting on that line would stop re-reading the harvest report.
**Suggested fix:** Reword to state the condition rather than the outcome: `body harvest bounded: parsed the 10 oldest of <M> unhandled body-carrying reviews; deferred <id, id, …> — re-run to pick them up; the deferred ids are reachable once this run posts a marker (6f)`. Drop `<R>` from the line.

### F-5: `HARVEST_FLOOR` clears on "parsed", while `HANDLED_THROUGH` requires "dispositioned" — the two conditions should agree
**Severity:** P3
**Where:** spec § Decision 12 (spec.md:443-449 vs. 486-489)
**Claim:** A floor cause is "a review deferred by 2b step 2's bound **and not since parsed**" and clears when "a later round … **parses** what an earlier one deferred" (spec.md:443-447); `HANDLED_THROUGH` requires the review to have been "fetched, parsed, **and had all its surviving items dispositioned**" (spec.md:486-488).
**Why this is wrong:** A round can parse a deferred review without triaging it — 6a parses the harvest set to compute a count (spec.md:1274-1277), and if `NEW_INLINE + new_body_items == 0` the cycle goes to 6d and 6b never runs, so those items reach no disposition. Under the current wording that clears the floor for that id while `HANDLED_THROUGH` still excludes it. No harm follows — `R = min(HANDLED_THROUGH, floor − 1)` and `HANDLED_THROUGH` is the binding constraint, so the invariant at spec.md:501-504 holds — but a future editor who reasons from the floor alone (as Decision 12 invites, spec.md:517-523) will conclude the review is handled when it is not.
**Suggested fix:** Change "and not since parsed" / "parses what an earlier one deferred" to "and not since **handled**" / "**handles** what an earlier one deferred", with "handled" defined as `HANDLED_THROUGH`'s three-part test. One word in two places.

### F-6: The `:81` and `:381` exits post a 6f comment but never reach 6e, so nothing reports the comment URL, the unfetchable row, or the harvest-size row
**Severity:** P3
**Where:** spec § D1 (spec.md:846-865), § D7 (spec.md:1381-1387), § D8 (spec.md:1536-1545)
**Claim:** `:81` and `:381` "gain the sentence *'Before exiting, post the progress marker if 6f's post condition holds (6f).'*" (spec.md:1381-1382); 6e's report carries `Body-level findings: … dispositions posted in <comment-url>`, `Body reviews unfetchable: …`, `Body harvest size: …` (spec.md:1537-1541).
**Why this is wrong:** Both exits stop the run — `SKILL.md:81` reports "Nothing to review — PR is approved" and `:381` reports "Nothing to review" — long before 6e. So on the very paths that D7 added a post for, the operator sees a terminal line that says nothing happened, while a PR-level comment was in fact written and (per D7's third arm, spec.md:1392-1396) a review was written off as unfetchable. 2b steps 2 and 3 emit their own inline lines, so the *bound* and the *size* are visible, but the unfetchable classification and the posted comment URL have no reporting site on these paths. `:81` is the modal outcome of a re-run on a healthy PR, which the spec itself notes (spec.md:768-769).
**Suggested fix:** In D1's `:81` clause and D9's `:381` rewrite, add: *"When the marker was posted, append `— body-level progress marker posted in <comment-url>` (and, when a review was written off, `; review <id> unfetchable (<code>)`) to the exit line before stopping."*

### F-7: Plane ticket VHS-41 is not in the memory mirror
**Severity:** P3
**Where:** grounding step 3
**Claim:** n/a — grounding.
**Why this is wrong:** `memory_search` with `namespace: "plane"`, `tags: ["plane_work_item", "VHS-41"]`, `source_system: "plane"` returned `Results: 0 of 1 requested` (confidence 0.00). The ticket's canonical description and acceptance criteria could not be cross-checked against the brief. I proceeded from `docs/specs/TODO/VHS-41.brief.md`, whose header carries the ticket UUID `80abb94f-6cd5-44a7-84f1-716b17704947` and whose "Done when" clauses both map cleanly onto spec § Done when 1–2. This is the fourth round in which the ticket has not been reachable; the risk is that a Plane-side edit since 2026-09-08 is invisible to every lens.
**Suggested fix:** No spec edit. Before `/ship-spec`, re-mirror VHS-41 into the `plane` namespace (or confirm the Plane description matches the brief by hand) so the drift-check has the canonical source.

## Summary
P0: 0 | P1: 0 | P2: 4 | P3: 3 | P4: 0

STATUS: GREEN
