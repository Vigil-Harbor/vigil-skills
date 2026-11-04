---
name: spec-land
description: After a PR is merged, confirm the landed code matches the recorded head and patch-id, move the Plane ticket to Done or Post-merge Checklists, write the wiki merge line and filemap delta, and clean up the worktree and branch. Never merges and never commits.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: true
  services: [vcs-host, issue-tracker?]
---

# /spec-land

Run after a pull request is merged and before `/spec-close`. One script call reads everything and prints a confirmation block. After one operator agreement, the script writes the wiki, you move the issue-tracker ticket, and the script cleans up and runs the project's post-land command.

`land_check.py` owns every check and every write except the tracker. Do not re-derive its mechanics by hand.

## What this skill must not do

- Run `gh pr merge`. The operator merges.
- Run `git commit` or `git add`, push content, stash, or force anything. The only remote change is the script's leased branch delete.
- Write anything before the operator agrees to the confirmation block.
- Hand-edit `log.md`. The script calls the installed `prepend_log_entry.py`.
- Write `state.md`, comprehension pages, or sibling tickets. `/spec-close` does the rest of the wiki.
- Invent a state UUID. Use the one the script prints from the installed `states.json`.

## Script

Resolve the installed script and an interpreter in the same shell call as each command:

```bash
SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-land/scripts/land_check.py"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
test -f "$SCRIPT" || echo "land_check.py not found — install with 'python sync.py install'"
```

A missing script stops the run. Every subcommand reads no stdin; give it `< /dev/null`. The script accepts both `C:/` and `/c/` path forms.

## Step 1 — Preflight

```bash
"$PY" "$SCRIPT" preflight <PR-number | PR-URL | spec-path> < /dev/null
```

No argument uses the current branch's PR. Run it from the repository's main checkout. It fetches once and writes nothing.

- **Exit 0.** Stdout is the confirmation block, then one line that starts with `spec_land_state=`. Hold that line exactly as printed. Do not edit it.
- **Exit 1.** The first line is `HALT: <reason>`. Show it and stop. Nothing was written. The script halts only when the PR is not merged, a PR or comment read fails, the fetch fails, a PR URL names another repository, no single PR matches, or a git command fails.
- **Exit 4.** `NEEDS TICKET`: the branch and title disagree on the ticket id, or name none. Ask the operator for the id, then rerun with `--ticket <ID>` on the same PR number.
- **Any other exit.** Show stderr and stop.

A failed comment read is never "no marker". A marker that is absent after a full read means verification is skipped, and the run continues.

## Step 2 — Confirm once

Show the confirmation block verbatim, except the `spec_land_state=` line. Then wait. The SHA line is one of:

- `match`: the landed code is the recorded code. It is not a statement that the code was reviewed. The review token is shown, never a gate.
- `no marker`: verification skipped.
- `WARNING`: a head mismatch, a patch-id mismatch, a malformed marker, or base drift onto PR files. The operator may still land. Say what the warning means in plain words.

Read the reply for intent. A clear yes for this ticket lands. On a `WARNING`, the reply must say to land despite the warning; a plain yes gets one question back naming the warning. Silence, an empty reply, or anything unclear is not yes; ask once, naming what is unclear. A reply that declines stops with nothing written. A host that cannot wait prints the block and stops.

Before you act, print `Reading: <what you will do>.`

## Step 3 — Save the state

After the operator agrees, write the held `spec_land_state=` line to a new temporary file outside the repository, with your file-write tool. Pass that path to the next two commands. Delete the file at the end of the run.

## Step 4 — Wiki

```bash
"$PY" "$SCRIPT" wiki --state <state-file> < /dev/null
```

It prepends the merge line to the wiki `log.md` with a guard, so a rerun does not duplicate it. Then it applies the filemap delta for added, deleted and renamed files. No wiki configured, no slug, or a missing filemap file is reported and skipped. Exit 1 means a write failed; report it and continue. Never hand-edit `log.md` to recover; rerun `/spec-land`.

## Step 5 — Issue tracker

Plane is optional. Take the prefix, target state, state UUID, project UUID and checklist comment from the state.

1. Read the ticket's current state with the tracker's retrieve-by-identifier capability (for example `mcp__claude_ai_Plane__workitem` with `action: retrieve_by_identifier`, `workitem_identifier: "<TICKET-ID>"` and `fields: "id,state"` in Claude Code, or the equivalent in your host; load the tool first if your host defers tool schemas). Do not pass `expand`, so `state` stays a UUID.
2. On the Post-merge Checklists path only, list the ticket's comments (for example `mcp__claude_ai_Plane__workitem_comment` with `action: list` in Claude Code, or the equivalent in your host). Skip the post when a comment already contains the last line of the checklist comment. If the list cannot be read, post anyway; a duplicate comment does no harm. Post the comment body exactly as printed. Its last line is visible text, because Plane strips HTML comments.
3. Move the ticket to the target UUID with the state-update capability (for example `mcp__claude_ai_Plane__workitem` with `action: update` in Claude Code, or the equivalent in your host). Skip the move when the ticket is already there.

A failed post does not skip the move. When the tracker is unreachable, the lookup fails, or the state reports a Plane problem, skip the tracker and print:

```text
Issue tracker skipped — <reason>.
To complete manually:
  1. Move <TICKET-ID> to <target state> in Plane
  2. Comment on the ticket with the checklist body when the target is Post-merge Checklists:
<checklist comment, or "no checklist comment" when the target is Done>
```

## Step 6 — Cleanup

```bash
"$PY" "$SCRIPT" cleanup --state <state-file> < /dev/null
```

Run it from the main checkout (the `main` path in the state), never from inside the worktree it removes. It rechecks the checkouts before it acts, then prints one line per action. The safety rules it holds:

- A dirty worktree is kept, and so are its local and remote branches.
- Several checkouts of the branch are kept with their branches. The run continues.
- `git branch -D` runs only after a SHA match with the local tip equal to the PR head. Never on the no-marker or warning path.
- The remote branch is deleted only with a lease on the PR head. Already gone is normal, because GitHub often deletes it.
- The default branch is never deleted.
- The main checkout fast-forwards only when it is on the default branch and clean.
- The post-land command runs once, in the main checkout, only when that fast-forward left it holding the landed commit.

Exit 1 means an action failed. Report it. Earlier actions are not rolled back.

## Step 7 — Summary

```text
=== LANDED: <TICKET-ID> ===
PR: <url>
SHA: match | skipped | warning — landed anyway
Plane: <from> → <to> | skipped
Wiki: <log outcome>; <filemap outcome>
Cleanup: <one line per action>
Next: /spec-close <spec-path>
Suggested wiki commit: <files the wiki step wrote, or none>
```

Omit the spec path on the Next line when the run had none. The suggested commit is text for the operator. Do not run it.

## Rerun

Rerunning on the same PR is safe. Start again at Step 1 with a fresh confirmation; do not reuse an old state file or an old agreement. Guards skip what is done: the log guard, existing filemap headings, the checklist marker, a ticket already in its target state, and branches already gone.

## Tool-use notes

- Shell for `land_check.py`; `vcs-host` is required. File write for the temporary state file.
- The tracker capabilities in Step 5. `issue-tracker` is optional: without it, print the manual steps and continue.
