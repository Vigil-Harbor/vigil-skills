# Conventions Review — VHS-8 Round 1

## Findings

### F-1 (P2): `--force` flag is a silent addition not in the brief

Decision 4 adds `--force` which the brief doesn't mention. The brief specifies `--partial` as the only flag. Adding user-facing CLI flags beyond the brief's scope should be called out as a Decision departure, or removed.

### F-2 (P2): Runtime `list_states` calls vs. VHS-1 caching approach

VHS-1 introduced `states.json` to cache Plane state data and reduce runtime API calls. This spec adds runtime `list_states` calls in both skills. While the brief explicitly requests this approach ("Both skills call `list_states`..."), it's worth noting the tension with the caching direction. `states.json` already has state name→UUID mappings but lacks explicit group fields.

### F-3 (P3): Missing "Invoked as:" convention line in both skills

Existing skills (spec-cycle, ship-spec, review-pr) begin with "Invoked as: `/skill-name <args>`" after the frontmatter. Both new skill designs omit this convention.

### F-4 (P3): No mention of SCHEMA.md version or anchor convention

The spec references SCHEMA.md for wiki entry formats but doesn't cite specific template names. If SCHEMA.md templates change, the skill's assumptions may drift. Pin to current template names (e.g., "standard decision template", "comprehension template").

### F-5 (P3): Reconciliation report format not anchored to a schema

The reconciliation report has a defined structure in Phase 3 but no versioning or schema marker. If the format changes in a future version, spec-retire's parser may break. Consider adding a format version line (e.g., `Format: reconciliation-v1`).

### F-6 (P3): `retire` action tag not yet in wiki conventions

Decision 8 introduces a `retire` action tag for log.md. Existing tags are `feat`, `fix`, `refactor`. The new tag should be documented in SCHEMA.md or at minimum noted as an addition to the convention. The spec doesn't include a SCHEMA.md update in scope.

### F-7 (P4): Test command is minimal

`python sync.py install --dry-run --verbose` only tests file discovery, not structural validity of the SKILL.md files. Acceptable for a markdown-only repo but worth noting.

### F-8 (P4): No explicit mention of Windows path handling

The spec uses Unix path conventions (`mkdir -p`, forward slashes). On Windows, PowerShell equivalents or Git Bash would be needed. Since the skills are markdown instructions (not executable scripts), this is fine — the agent interprets them — but cross-platform notes could help.

## Closure Table

(Round 1 — no prior findings to close.)

STATUS: GREEN
