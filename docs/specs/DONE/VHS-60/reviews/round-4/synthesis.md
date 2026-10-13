# Synthesis — round 4

Lenses: correctness, edge-cases, conventions
Empty review: none

## Act on
(none)

## Consider
(none)

## Noted
- correctness/F-1 (P3) ticket not cached.
- correctness/F-2 (P3) a phrase made only of stripped marker characters is not skipped.
- correctness/F-3 (P3) whole-path-token rule stated beside the locator grammar but relied on for the file decision.
- correctness/F-4 (P4) deletion gate's "every removed line" test does not fit sentence-level replacements.
- edge-cases/F-1 (P3) phrase empty only after marker deletion counts as a miss.
- edge-cases/F-2 (P3) a word-form line belonging to another file is placed in this spec.
- edge-cases/F-3 (P3) parenthesis cut lets an exact match pre-empt a longer heading.
- edge-cases/F-4 (P3) deletion gate diffs against a fixed SHA.
- edge-cases/F-5 (P3) ticket grounding unavailable.
- edge-cases/F-6 (P4) Decision 7 no longer says "current" heading text.
- edge-cases/F-7 (P4) artifact-exception heading omits `:445`.
- conventions/F-1 (P3) the `/spec-close` note names the wrong wiki file.
- conventions/F-2 (P3) spec-level additions beyond the brief, for the human drift check.
- conventions/F-3 (P4) artifact-exception heading omits `:445`.

## Dismissed
(none)

## Agreement Map
| Root | Findings | Lenses | Severities | Bucket |
|---|---|---|---|---|
| `:492` replacement — emptiness tested before marker deletion | correctness/F-2, edge-cases/F-1 | correctness, edge-cases | P3, P3 | Noted |
| artifact-exception heading omits `:445` | edge-cases/F-7, conventions/F-3 | edge-cases, conventions | P4, P4 | Noted |
| Test plan deletion gate wording | correctness/F-4, edge-cases/F-4 | correctness, edge-cases | P4, P3 | Noted |
| ticket grounding unavailable (memory server 502) | correctness/F-1, edge-cases/F-5 | correctness, edge-cases | P3, P3 | Noted |
