# Spec: VHS-9 — spec-retire fast-path when wiki coverage already exists

## Goal

Add an early-exit fast-path to spec-retire Phase 2b that detects when `/wiki-after-merge` has already created wiki entries for the ticket. When coverage is complete, skip the full derivation pipeline and proceed directly to archive. When coverage is partial, derive proposals only for the missing categories. Secondary: make the untracked-spec status visible in Phase 0 with a notice.

## Scope

### Files to change

- `skills/spec-retire/SKILL.md` — Phase 0 (fallback notice), Phase 2b (fast-path logic), Phase 4 (narrow log.md idempotency guard)

### Files to leave alone

- `skills/spec-reconcile/SKILL.md` — no changes
- `skills/ship-spec/SKILL.md` — no changes
- `agents/*.md` — no changes
- `sync.py` — no changes

## Decisions

### Decision 1: Fast-path is a grep-based pre-check, not LLM analysis

The brief requires the check to be "lightweight (file greps, not LLM analysis)." Both the applicability determination (Stage 1) and the coverage check (Stage 2) use grep/sed. Stage 1 extracts the `## Wiki-ready` section via `sed` and greps for category markers within that section. Stage 2 greps wiki directories for the ticket ID.

**Rationale:** LLM-based comparison would defeat the purpose — the optimization saves token budget by avoiding unnecessary derivation. Grep/sed is deterministic, fast, and sufficient since both the reconciliation report template and wiki-after-merge entries use predictable markers.

### Decision 2: Three-category coverage model with conditional applicability

The fast-path checks three Phase 2b derivation categories — comprehension, decisions, and state.md — each with conditional applicability. Comprehension is only applicable when the reconciliation report flags an architectural change. Decisions are only applicable when the report flags extractable decisions. State.md is always applicable for full-retire. Log.md is excluded from the coverage model because it is not derived in Phase 2b — it is compiled by Phase 2c and written in Phase 4 with its own idempotency guard.

**Rationale:** A ticket that shipped a pure bug fix may have no wiki-worthy decisions or comprehension entries. Treating absent entries as "missing coverage" would force unnecessary derivation for categories that legitimately have no entries. Separating log.md from the derivation categories preserves the existing phase boundaries.

### Decision 3: Partial-coverage derives only missing categories

When some but not all applicable categories are present, Phase 2b derives proposals only for the gaps — not the full set. The existing duplicate-detection in Phase 2a remains as a safety net below this optimization layer.

**Rationale:** The brief explicitly requires this behavior (AC 3). The Phase 2a exclusion list still catches edge cases where the fast-path's grep missed a match (e.g., ticket ID referenced in a different format).

### Decision 4: Untracked-spec notice is placed in Phase 0, not Phase 1

The gitignored-spec detection happens at the point where the spec file is first resolved (Phase 0 step 2), keeping the notice co-located with the detection logic rather than deferred. The notice describes the actual consequence for spec-retire: the archive step will use `mv` + `git add` instead of `git mv` (not "recovered from git history" — that describes spec-reconcile's `git show` fallback, which is a different skill).

**Rationale:** Phase 0 is the preflight — the natural place for environment notices. Deferring the notice to a later phase would separate it from the detection, making the skill harder to follow.

### Decision 5: Phase 4 log.md idempotency guard narrowed to retirement-specific marker

The existing Phase 4 guard uses `grep -F "<TICKET-ID>"` which matches any log.md entry mentioning the ticket — including the merge-event entry written by wiki-after-merge. This broader match suppresses the retirement-event entry in exactly the scenario the fast-path optimizes for (wiki-after-merge has already run). The guard is narrowed to `grep -F "retire | <PROJECT> — <TICKET-ID>"` so the retirement entry is only suppressed by a prior retirement entry, not by a merge entry.

**Rationale:** Without this change, the fast-path's full-coverage branch is correct (it skips derivation) but Phase 4 would silently drop the retirement log entry because the merge-event entry already contains the ticket ID. This is a prerequisite for the fast-path to produce correct audit trails.

## Design

### Phase 0 change: gitignored-spec fallback notice

After Phase 0 step 2 ("Confirm the spec exists"), add a tracking-status check:

```
2a. Check tracking status: `git ls-files --error-unmatch <spec-path> 2>/dev/null`.
    If exit ≠ 0 (file is untracked/gitignored), print:
      `Note: Spec file is untracked (gitignored). Archive step will use mv + git add instead of git mv.`
    Continue regardless — the file exists on disk, which is sufficient.
```

This is informational only. It does not gate any behavior — the spec file's on-disk presence (verified in step 2) is what matters. The notice makes the tracking status visible when the spec directory is gitignored (as in vigil-skills), so the user understands why the archive step uses `mv` + `git add` rather than `git mv`.

### Phase 2b change: wiki coverage fast-path

Replace the current Phase 2b opening (which immediately begins reading the reconciliation report and drafting proposals) with a three-stage pre-check:

**Stage 1 — Determine applicable derivation categories.**

Extract the `## Wiki-ready` section from the reconciliation report, then grep for category markers within that section only. The markers must be scoped to Wiki-ready because "Decision" and "Comprehension" appear elsewhere in the report (the `## Decisions` table header and rows contain "Decision" in every well-formed report).

```bash
# Extract Wiki-ready section (from heading to next heading or RECONCILED line)
sed -n '/^## Wiki-ready/,/^##\|^RECONCILED/p' "<reconciliation_report_path>" > /tmp/wiki-ready-section.txt

# Check for category markers within that section
grep -c "Decision" /tmp/wiki-ready-section.txt
grep -c "Comprehension" /tmp/wiki-ready-section.txt
```

Classify applicability:

| Category | Applicable when |
|----------|----------------|
| `comprehension/` | Wiki-ready section contains "Comprehension" (grep count > 0) |
| `decisions/` | Wiki-ready section contains "Decision" (grep count > 0) |
| `state.md` "What's Shipped" | Always (evidence triple is mandatory for full-retire) |

If the reconciliation report has no `## Wiki-ready` section (sed produces empty output), treat all categories as applicable and fall through to normal derivation. This handles forward-compatibility if the reconciliation report template changes.

Note: `log.md` is not included in the coverage model. The retirement log entry is a distinct event from the merge log entry that wiki-after-merge writes. Phase 2c always compiles a retirement log entry, and Phase 4's narrowed idempotency guard (`grep -F "retire | <PROJECT> — <TICKET-ID>"`) prevents duplicates while allowing the retirement entry to coexist with wiki-after-merge's merge entry.

This deviates from brief AC 1, which lists four categories including log.md. The rationale: log.md is not a Phase 2b derivation target — it's a Phase 2c/4 artifact. Including it in the coverage model would conflate "was the merge logged?" with "were wiki proposals derived?" The retirement entry is always written regardless of fast-path result.

**Stage 2 — Check existing coverage.**

For each applicable category, run a targeted grep. Use echo delimiters between commands so per-category output is unambiguous:

```bash
echo "::COMP::"; grep -rl "<TICKET-ID>" "<wiki_root>/comprehension/" 2>/dev/null
echo "::DECI::"; grep -rl "<TICKET-ID>" "<wiki_root>/decisions/" 2>/dev/null
echo "::STATE::"; grep -rl --include="state.md" "<TICKET-ID>" "<wiki_root>/projects/" 2>/dev/null
```

The state.md grep uses `--include="state.md"` across all `projects/` subdirectories rather than targeting a specific project slug. This avoids requiring a mapping from Plane project prefix (e.g., `VHS`) to wiki project directory name (e.g., `vigil-skills`), which aren't the same and have no defined mapping in states.json. The `--include` flag is placed before the path for portability across grep implementations.

Run all applicable greps in a single Bash call (semicolon-separated). Classify each applicable category by checking the output between its delimiter and the next: non-empty output after the delimiter = `covered`, no output after the delimiter = `missing`. The echo delimiters ensure per-command classification is deterministic even when multiple greps return results.

**Stage 3 — Branch on coverage level.**

Three branches:

1. **Full coverage** (all applicable categories are `covered`):

   Print a summary of what was found. Only list applicable categories — omit not-applicable ones:
   ```text
   Wiki coverage already exists (likely created by /wiki-after-merge):
     [found] comprehension/ — <matched-filename>
     [found] decisions/ — <matched-filename>
     [found] state.md — entry found

   All derivation categories covered. Skip wiki proposal derivation? [y/N]
   ```

   Note: The brief specifies `[skip/edit]` as the prompt format. This spec uses `[y/N]` for consistency with existing skill prompt conventions (spec-retire Phase 0 step 4, Phase 3).

   - On `y`: set derivation proposals to empty (no decisions, no comprehension, no state.md edit). Proceed to Phase 2c, which still compiles the archive list and the retirement log entry. Phase 4's idempotency check handles log.md dedup.
   - On `N`: fall through to the normal derivation flow (existing Phase 2b logic).

2. **Partial coverage** (some applicable categories are `covered`, some are `missing`):

   Print what's covered and what's missing:
   ```text
   Partial wiki coverage found:
     [found]   comprehension/ — <matched-filename>
     [missing] decisions/ — not found
     [found]   state.md — entry found

   Deriving proposals for missing categories only.
   ```

   Then run the existing derivation logic, but scoped to only the `missing` categories. Read all necessary inputs (reconciliation report, spec) as usual — the shared-input read step is not optimized away. Only the drafting/proposal step is scoped: skip proposal drafting for `covered` categories, draft only for `missing` ones. The Phase 2a exclusion list still applies within the derivation scope.

3. **No coverage** (no applicable categories are `covered`):

   No output from the fast-path. Fall through to the existing Phase 2b derivation flow unchanged.

### Integration with existing flow

- **Phase 2a (duplicate detection)** remains unchanged. It runs before Phase 2b and feeds the exclusion list. The fast-path is an optimization layer above Phase 2a — it checks broader coverage (did wiki-after-merge run?), while Phase 2a catches per-entry duplicates. The comprehension/decisions greps in the fast-path overlap with Phase 2a's greps; this redundancy is intentional — the fast-path is self-contained, and Phase 2a remains as a safety net for the partial-coverage derivation path.
- **Phase 2c (compile proposals)** receives whatever Phase 2b produces. In the full-coverage-skip case, 2b produces no derivation proposals — 2c compiles the archive list and the retirement log entry (which is always included regardless of fast-path result).
- **Phase 4 (execute)** log.md idempotency guard is narrowed (see Decision 5). The current guard (`grep -F "<TICKET-ID>"`) is replaced with `grep -F "retire | <PROJECT> — <TICKET-ID>"` so it matches only prior retirement entries, not wiki-after-merge's merge-event entries. This is a behavioral change — without it, the merge-event entry would suppress the retirement log entry in exactly the scenario the fast-path handles.
- **Partial-retire mode** is unaffected. The fast-path only executes inside Phase 2b, which is already skipped entirely for partial-retire.

### Phase 4 change: narrow log.md idempotency guard

In Phase 4 step 4, replace:
```
Idempotency: grep -F "<TICKET-ID>" <wiki_root>/log.md first; skip if already present.
```

With:
```
Idempotency: grep -F "retire | <PROJECT> — <TICKET-ID>" <wiki_root>/log.md first; skip if already present.
```

This narrower match ensures that wiki-after-merge's merge-event entry (e.g., `## [YYYY-MM-DD] feat | VHS — VHS-8: ...`) does not suppress the retirement-event entry (e.g., `## [YYYY-MM-DD] retire | VHS — VHS-8: ...`). `<PROJECT>` is `project_prefix` from Phase 0 step 1 (the uppercase prefix extracted from the ticket ID, e.g., `VHS` from `VHS-9`).

### Amended SKILL.md structure

The Phase 2b section (currently lines 59–75 in SKILL.md) will be restructured as:

```
### 2b. Wiki decomposition (full-retire only)

Skip entirely for partial-retire. For full-retire:

#### Fast-path: check existing wiki coverage

<Stage 1-3 logic as described above>

#### Normal derivation (when fast-path does not fully exit)

<Existing Phase 2b derivation logic, with the addition that partial-coverage
mode scopes derivation to missing categories only>
```

## Test plan

This is a markdown-only skill file — no executable code to unit test. Verification is behavioral:

1. **Syntax validation:** `sync.py install --dry-run --verbose` succeeds (file copies without error, YAML frontmatter parses).
2. **Manual review:** Read the modified SKILL.md end-to-end and confirm:
   - Phase 0 step 2a is correctly placed after step 2 and before step 3
   - Phase 2b fast-path runs only in full-retire mode (partial-retire still skips 2b entirely)
   - The three coverage branches (full/partial/none) are unambiguous
   - Grep commands use quoted paths (Windows compatibility)
   - state.md grep uses `--include="state.md"` across `projects/`, not a specific slug
   - Phase 2a and Phase 2c references are consistent with the new flow
   - The `[y/N]` prompt only appears in the full-coverage branch
   - Retirement log entry is always compiled by Phase 2c (not skipped by fast-path)
   - Phase 4 idempotency guard uses the retirement-specific marker

## Test command

```
python sync.py install --dry-run --verbose
```

## Done when

1. Phase 2b starts with a grep-based coverage check across three derivation categories (comprehension, decisions, state.md), with comprehension and decisions conditionally applicable based on the reconciliation report's `## Wiki-ready` section.
2. Full-coverage case prints a summary and prompts `[y/N]` — `y` proceeds to Phase 2c with empty derivation proposals (archive + retirement log entry only), `N` falls through to normal derivation.
3. Partial-coverage case reports covered vs. missing categories and derives proposals only for missing ones (inputs are still read; only proposal drafting is scoped).
4. No-coverage case falls through to existing derivation unchanged.
5. Token savings in full-coverage case: Phase 2b completes in 1-2 tool calls (grep + user prompt) instead of 5-8.
6. Phase 0 prints a notice when spec file is untracked (gitignored), making the tracking status and its archive-step consequence explicit.
7. Partial-retire mode is unaffected — Phase 2b is still skipped entirely.
8. Retirement log entry is always compiled by Phase 2c regardless of fast-path result. Phase 4's idempotency guard uses the retirement-specific marker to distinguish from wiki-after-merge's merge-event entry.

## Out of scope

- Changing `/wiki-after-merge` behavior.
- Adding inter-skill communication or shared state beyond filesystem checks.
- Modifying Phase 2a duplicate detection (it still runs for the partial-coverage path).
- Any changes to spec-reconcile, ship-spec, or spec-cycle skills.
- Executable test suite — this is a markdown-only change.
