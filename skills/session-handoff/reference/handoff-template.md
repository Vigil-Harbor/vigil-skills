# Handoff document structure

The annotated mirror of what `scripts/create_handoff.py` emits. Depths match the
section table in `scripts/_sections.py`; the guidance under each heading is what
the generated `[TODO: ...]` marker asks for.

Three rules govern the whole document:

- **Only the required and recommended sections carry a marker.** The title, the
  metadata container, the generated commit list and the chain block never do —
  they are filled by the tool, and a marker there would be unclearable.
- **Presence is matched by name at any depth.** `## Important Context` and
  `### Important Context` are the same section to the validator. Nest however
  the document reads best.
- **Nothing is exempt from the secret scan**, including the generated commit
  list. A credential in git history is a real finding.

---

## `#` — document title *(generated, no marker)*

`# Handoff: <slug with hyphens replaced by spaces>`. The validator reads this
line when another document chains to this one.

## `##` Session Metadata *(container, no marker)*

Created timestamp, project path, current branch. Generated.

### `###` Recent Commits *(generated, no marker)*

The last five commits, `<short sha> <subject>`, one per bullet. When git cannot
answer, this reads as plain italic prose — `_not a git repository_`,
`_no commits yet_`, or `_git unavailable or timed out_` — deliberately *not* the
marker shape, so a handoff written outside a repository can still reach `READY`.

## `##` Current State Summary *(required)*

`[TODO: Current State Summary — what is the state of this work right now?]`

Where the work actually stands: what is done, what is half-done, what is
blocked. Write it for someone with no memory of the session.

## `##` Codebase Orientation *(container, no marker)*

### `###` Architecture Overview *(recommended)*

`[TODO: Architecture Overview — how do the moving parts fit together?]`

### `###` Critical Files *(recommended)*

`[TODO: Critical Files — which files must the next session read first?]`

Paths with a sentence each on why they matter. RESUME's staleness check looks at
whether later commits touched these.

## `##` Work Completed *(container, no marker)*

### `###` Files Modified *(recommended)*

A generated `| Status | File |` table of modified and staged paths, capped at ten
rows with `… and N more`. Beneath the table — never inside a cell — one marker:

`[TODO: Files Modified — why did each of these change?]`

Git supplies the paths; you supply the reason.

### `###` Decisions Made *(recommended)*

`[TODO: Decisions Made — what was decided, and what was rejected?]`

Record the rejected option too. A decision without its alternatives gets
relitigated.

## `##` Pending Work *(container, no marker)*

### `###` Immediate Next Steps *(required)*

`[TODO: Immediate Next Steps — what is the very next action, in order?]`

An ordered list. RESUME starts at #1, so #1 must be executable without further
inference.

## `##` Context and Risks *(container, no marker)*

### `###` Important Context *(required)*

`[TODO: Important Context — what would the next session get wrong without this?]`

### `###` Assumptions Made *(recommended)*

`[TODO: Assumptions Made — what is assumed but not verified?]`

### `###` Potential Gotchas *(recommended)*

`[TODO: Potential Gotchas — what is likely to bite the next session?]`

## `##` Handoff Chain *(generated, no marker)*

Two pinned lines when the document continues from another:

```
- **Continues from**: [<filename>](./<filename>)
  - Previous title: <the predecessor's H1, truncated to 80 characters>
```

and a single line when it does not:

```
- **Continues from**: None (fresh start)
```

A predecessor with no depth-1 heading, or an empty one, records its filename in
place of the title rather than an empty line.
