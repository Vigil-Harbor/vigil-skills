---
name: session-handoff
description: >
  Save and restore working context across sessions. Creates a validated handoff
  document capturing state, decisions, and next steps; resumes from one; or picks
  up directly from a prior session id. Use when the user says "create handoff",
  "save state", "load handoff", "resume from", "continue where we left off", or
  when context is filling up and work must survive the session boundary.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
---

# /session-handoff

Work outlives sessions; context does not. This skill writes the bridge: a handoff
document that states where the work stands, what was decided, and what the next
session should do first — then validates it before you rely on it.

Two scripts do the mechanical parts. Everything else is your judgement.

- `scripts/create_handoff.py` — scaffold a document, pre-filled with git metadata.
- `scripts/validate_handoff.py` — presence, placeholder and secret gate.

Documents live at `<project-path>/.claude/handoffs/YYYY-MM-DD-HHMMSS-<slug>.md`.
That path is project-local working state, not harness config; a harness that must
relocate it passes `--project-path` rather than forking this skill.

## Mode selection

Pick one mode from the argument and the user's intent:

1. The argument is a session id — a canonical UUID (8-4-4-4-12 hexadecimal
   groups) — → **SESSION TRANSFER**.
2. The user wants to save, pause, park or hand off the current work →
   **CREATE**.
3. The user wants to resume, load, or continue from earlier work → **RESUME**.

A non-UUID argument is a task slug for CREATE. It is never a path fragment.

## CREATE

1. Run `create_handoff.py [slug] [--continues-from <file>] [--project-path <dir>]`.
   An omitted or empty slug becomes `handoff`. The script prints the path it wrote.
2. Read the scaffold. Replace **every** `[TODO: ...]` marker with real content —
   the marker names the section and asks what it needs. Markers sit in the
   sections a human must write; the metadata, commit list and file table are
   already filled.
3. Run `validate_handoff.py <file>`.
4. **Act on the verdict and the exit code.** Report the path, the verdict, and
   the first next action to the user.

| Verdict | Exit | What to do |
|---------|------|------------|
| `READY` | 0 | Finalize. Tell the user the path. |
| `NEEDS WORK` | 1 | A required section is absent, or a placeholder remains. Fix and re-validate. |
| `BLOCKED` | 2 | A credential matched. **Do not finalize.** |
| *(none)* | 3 | The file is missing or unreadable — a usage error, not a verdict. |

On `BLOCKED`, the report gives the locus (`<file>:<line>`), the pattern name and
a redacted excerpt. Edit that line and re-validate. This holds **including** when
the match sits in a generated commit subject: a credential in git history is a
real finding, not a false positive.

A placeholder left in a *recommended* section is `NEEDS WORK` too. A recommended
section that is genuinely absent is only informational.

## RESUME

1. List `*.md` in `<project-path>/.claude/handoffs/`, newest first. **Ignore
   `*.tmp`** — those are abandoned name reservations, not documents. If the
   directory is absent or holds no `*.md`, say so plainly and offer CREATE. Do
   not prompt the user for a path.
2. **Assess staleness before trusting the document.**
   - **Compare the recorded branch against the current one first.** A mismatch
     outranks commit count, and it is the common case, since branch-per-change
     workflows cut a new branch for every unit of work.
   - Then count what has landed since: `git log --oneline --since=<ts> --all`,
     preferring the timestamp from the **filename** over the body line.
   - Rubric: no commits and the same branch → fresh, resume directly; a few
     unrelated commits → review them, then resume; many commits, or commits
     touching the Critical Files, or a branch mismatch → verify carefully before
     acting; weeks old plus real divergence → consider writing a fresh handoff
     instead of resuming this one.
3. **Read the document fully, then follow its chain.** Follow the
   `Continues from` link to a maximum of **5 hops**, tracking resolved absolute
   paths (compared case-insensitively on Windows) so a cycle terminates with a
   note rather than looping.
   - Prefer the markdown href, resolved relative to the handoffs directory.
   - **If the line carries no href**, take the first backticked or bare path on
     the line — resolving it relative to the handoffs directory when bare, and
     relative to `<project-path>` when it begins `.claude/`.
   - **Unless the text before that path contains `None` or `new thread`.** Some
     documents record a *rejected* auto-link in exactly that shape; following it
     resumes from an unrelated session while presenting the result as chain
     context.
   - If neither yields an existing file, note it and stop the chain. Do not guess.
4. Verify the recorded branch, blockers and assumptions against the current tree,
   then begin at **Immediate Next Steps #1**.

## SESSION TRANSFER

Given a session id, pick up where that session stopped.

1. **Validate the id first.** It must match the canonical UUID shape —
   `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`
   as a *full* match, so a trailing newline from a shell substitution is
   rejected — **before any filesystem lookup**. A non-matching argument is a task
   slug for CREATE.
2. **Locate the transcript for the given session id in this harness's session
   store, or the equivalent in your host.**
   *(e.g. Claude Code keeps session transcripts under
   `~/.claude/projects/**/<session-id>.jsonl`.)*
3. **Read it bounded.** Seek to `max(0, size - 256*1024)` and read to EOF,
   decoding with `errors="replace"`. Discard the first line if the read did not
   start at byte 0 — in a tail read the partial record is the *first* line — and
   discard the final line if it does not parse as JSON, since a live writer may
   be mid-append.
4. Summarize the recovered state and continue the work.

**Fallback — mandatory, and widely armed.** If the transcript is missing *or
unusable* (absent, unreadable, not valid JSONL, or too large to read usefully),
reconstruct from what is on disk: `git status`, `git log --oneline -10`, and the
newest document in `<project-path>/.claude/handoffs/`. Summarize that instead and
**state plainly which case applied**. Never fail the mode, and never interrogate
the user for a path.

## Superseding a previously installed handoff skill

This skill replaces earlier vendor-managed handoff skills. While both are
installed, the host picks between them by description match, which is not a
guarantee.

**Remove any previously installed vendor handoff skill from this harness's skill
directory.** Remove that one directory by name — do not run a prune or sync
operation that deletes everything the source tree does not contain, because a
skill directory normally holds third-party skills this repo knows nothing about.

If the vendor's installer restores its copy later, that is expected and not
fatal: repeat the targeted removal. Do not edit vendor-managed files.

## Test plan

Run from the vigil-skills repo root. Stdlib `unittest`; no pytest or node gate.

1. Heading matcher — the filed bug: a required section is found at `###`, an
   absent one reports `missing`, and the same name matches at every depth 1–6.
2. Template round-trip: a fresh scaffold carries exactly one placeholder per
   required/recommended section and none elsewhere; filling them all validates
   `READY`.
3. Legacy compatibility: both on-disk shapes (all-`##`, and `##`/`###`) validate
   with zero missing sections.
4. Verdict/exit matrix, including secret positives and a prose near-miss.
5. Accepted limits, pinned: a placeholder inside a fenced block still trips the
   scan; a heading inside a fenced block still satisfies presence.
6. Encoding: LF output, CRLF input, BOM input, non-ASCII git metadata.
7. Scaffold robustness: not-a-repo placeholders, slug sanitizing, collision
   suffixes, atomic-write cleanup, `--continues-from` hard errors.
8. Chain round-trip, including a predecessor whose title needs escaping.
9. Session-id validation rejects malformed, traversal-shaped and
   trailing-newline ids.
10. Portability lint reports zero ERROR and zero WARN for this skill.

## Test command

```console
python -m unittest discover -s tests -p 'test_session_handoff.py' -v
python lint.py --strict skills/session-handoff/SKILL.md
python -m unittest discover -s tests -p 'test_*.py' -v
```

Pin `python` by full path if more than one interpreter is on `PATH`.

## Done-when

- A scaffolded document, with every placeholder replaced, validates `READY`.
- Existing handoff documents at either heading shape still validate.
- A required section is found by name at any depth, which is the defect this
  skill was written to eliminate structurally.
- All three modes work with no vendor handoff skill installed.

## Tool-use notes

- `Read`, `Edit`, `Write` for filling in and reading handoff documents.
- `Bash` (or your host's shell capability) for the two scripts and for `git`.
- No network access, no subagents, no external services.
