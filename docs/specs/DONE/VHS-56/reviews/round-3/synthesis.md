# Synthesis — round 3

Lenses: correctness, edge-cases, conventions
Empty review: conventions

## Act on
(none)

## Consider
(none)

## Noted
- correctness/F-1 (P3) "ticket not cached" — shared-memory permission degradation already recorded; no speculative scope edit.
- edge-cases/F-1 (P2) "Ticket grounding remains blocked by namespace permissions" — same environment limitation; the existing `## Deferred (P2+)` entry carries it.
- conventions — no findings

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| Ticket/shared-memory access degradation | correctness/F-1; edge-cases/F-1 | correctness; edge-cases | P3; P2 | Noted |
