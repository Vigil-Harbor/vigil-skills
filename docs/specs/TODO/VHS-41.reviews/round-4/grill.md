# Grill 1 — VHS-41 round 4 — 2026-09-08T10:16:17-06:00 — findings: edge-cases/F-1, edge-cases/F-2, edge-cases/F-3

## Grill summary — VHS-41 round-4 remaining P0/P1 findings (rounds: 3/3, exit: empty-frontier; reason: tree fully visited)

### Settled
1. **The harvest cap yields to post-push reviews** (Q1) — chose A: in the post-push poll the harvest set is the 10 oldest pre-push candidates **plus every** candidate newer than the push, so the incremental review is always read; operator's rationale — "the cap is arbitrary". Facts relied on: none. ref: edge-cases/F-1
2. **An unfetchable review counts as handled for the in-run pointer** (Q2) — chose A: D6's "lowest failed" reads as "lowest *retryably* failed"; the pointer steps over a hard 404/410/451 exactly as the posted marker does. Operator's rationale — a failed fetch here is something the agent cannot fix, so handle it and do not spend cycles chasing it. Facts relied on: none. ref: edge-cases/F-2
3. **A fired drift detector blocks the affirmative exit** (Q3) — chose C: the round may not report "Nothing to review"; it exits `inconclusive`, prints the harvest summary, and does not advance the marker past unparsed reviews. Facts relied on: none. ref: edge-cases/F-3
4. **Both detectors block, not just the phrase detector** (Q5) — chose A: an incomplete pull is not trusted; the named real causes are CodeRabbit paused, rate limited, or approving the diff while posting outside-diff findings. Facts relied on: none. ref: edge-cases/F-3
5. **Fail closed on drift** (Q6) — chose A: a fired detector makes that review *unread*, so it floors the marker and a later run re-parses it. Operator's rationale — if the detectors fire the pipeline is broken; stop and fix the root cause rather than let a format change degrade the signal the skill exists to harvest. Facts relied on: none. ref: edge-cases/F-3
6. **The marker names out-of-order handled ids; the deterministic state helper is its own ticket** (Q4) — chose B: add the second id field so a post-push review read above a contiguity gap is not re-dispositioned, and file the state-owning helper script separately rather than redesigning Decisions 12–13 mid-spec. Facts relied on: F1. ref: edge-cases/F-1
7. **Auto-filing deferred findings is out of scope for VHS-41** (Q7) — chose A, with the operator's framing recorded: in a role-based task-router architecture, ticket-filing is a **hand-off to another agent**, not work done inside the skill; the receiver is not built yet, and any such hand-off is config-driven, never a hardcoded harness path. Facts relied on: none. ref: edge-cases/F-3

### Open frontier

*(none — every seeded finding is dispositioned)*

### Facts established
- F1 — Nothing in the repo forbids a skill shipping a helper script: 4 of 11 shipped skills already do, the only rules are stdlib-Python/no-build-step, a `requires:` declaration, and no hardcoded harness paths; Decision 13 fences only the *parse* (a refusing script would turn every CodeRabbit cosmetic tweak into a hard failure), wiki VHS-28 fences markdown *body* parsing in one validator rather than scripts generally, and wiki VHS-29 is *pro*-script for state exactly like this — it moved the idempotency guard into a script so check-and-insert is one operation "rather than a prompt-level `grep -F` the model could skip" (source: `docs/specs/TODO/VHS-41.spec.md:31,600-636`; `vigil-harbor-wiki/decisions/2026-08-25-vhs-28-validator-does-not-parse-markdown.md:45-47,122-135`; `vigil-harbor-wiki/decisions/2026-08-25-vhs-29-anchor-is-a-refusal-contract.md:39-43,77-79`; `AGENTS.md:7`; `docs/portability-contract.md:49-65`; `docs/authoring-portable-skills.md:21,41`; `skills/{spec-close,session-handoff,talaria,hermes-kanban-awareness}/scripts/`)

### Operator framing recorded alongside the decisions
Scope and sectioning across this architecture need not be monolithic or contained in one ticket. Each piece earns its place and its scrutiny before implementation — the goal is fewer agent-inference-filled gaps and more explicit bridges. The follow-up state helper is therefore filed as its own bridge with its own brief, not as a phase of VHS-41.
