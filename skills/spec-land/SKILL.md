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

User-invoked after a pull request is already merged and before `/spec-close`. On one confirmation it checks the landed tree against the head, base, and patch-id last recorded on the PR, moves the issue-tracker ticket to Done or to Post-merge Checklists, writes the wiki merge line and the filemap delta when a wiki is configured, then removes the worktree and the local and remote feature branch and runs the project's post-land command.

The working directory is the target repo. Steps 1–8 have no side effects except the step 3 fetch, which updates remote-tracking refs and `FETCH_HEAD`. A halt in those steps writes nothing else, moves nothing, and deletes nothing. "No side effects" below means the same.

**Shell note.** Command examples use bash (single quotes, `$()`). Use your host's shell. Write `$HOME` and `$CLAUDE_CONFIG_DIR`, never a tilde inside double quotes: bash does not expand a tilde there, and the pre-checks below then report a file that is installed as missing. `<branch>` is PR metadata and may contain `$` or parentheses: set it from `gh` output (`branch=$(gh pr view <N> --json headRefName --jq .headRefName)`) and pass `"$branch"`. Never paste a branch name into command text.

## What this skill must not do

- Run `gh pr merge`. The operator merges (Decision 4).
- Run `git commit` or `git add`. The wiki suggestion in step 10 is text. Do not execute it (Decision 12).
- Run `git push` except the leased remote branch delete in step 9.5. No other `--force`. No content push.
- Stash, or run a merge that is not `git merge --ff-only`.
- Fetch again after the one fetch window in step 3 (Decision 3).
- Post or edit the SHA marker. This skill only reads it.
- Call `prepend_merge_entry.py`. Do not copy a wiki-repo script into this repo (Decision 2).
- Write `state.md`, a comprehension stub, a sibling ticket, or a wiki commit.
- Invent a state UUID. UUIDs come from the installed `states.json` (Decision 7).
- Reimplement marker parsing, the patch-id decision, or path overlap. `land_check.py` classifies (Decision 16).

## Step 1 — Input and PR selection (Decision 11)

Invocation: `/spec-land <PR-number | PR-URL | spec-path>`. No argument: `gh pr view --json number` for the current branch. A non-zero exit, or `gh` missing from `PATH`, halts. That halt is Decision 10: no wiki write, no Plane write, no cleanup. Do not guess.

Resolve owner and repo the way `/review-pr` does:

```bash
gh repo view --json owner,name --jq '.owner.login + "/" + .name'
```

A non-zero exit is the same halt.

Classify the argument:

- No argument: the number from `gh pr view --json number`.
- An argument that is only digits: that PR number.
- An argument that contains `/pull/<digits>`: that number. This is the GitHub PR URL form `/review-pr` accepts. The `<owner>/<repo>` before `/pull/` must equal the resolved owner and repo, compared case-insensitively. A URL for another repository halts. Do not look up its number here.
- Anything else is a spec path. The ticket id is the anchored filename prefix `^[A-Z][A-Z0-9]*-[0-9]+` on the last path segment (`VHS-57.spec.md` yields `VHS-57`). A filename that does not start with that prefix halts. Print the invocation. Do not select a PR.

Selecting the PR is not the ticket search. A PR number selects that number. A PR URL selects the number in the URL. A spec path sets the ticket from the filename, then selects the PR. Do not clean up a PR this rule did not select.

Spec-path selection, in order:

1. `gh pr view --json number,headRefName,title` for the current branch is that PR only when it exits 0 and the unanchored id on `headRefName` or on the title equals the filename id. Otherwise do not bind that PR. A branch id and a title id that both differ from the filename id are not a match.
2. Otherwise `gh pr list --state merged --search <filename-id> --json number,title,headRefName --limit 100`. A non-zero exit halts. A result of 100 rows halts with `merged-PR list hit the limit — not searching further`. Do not read a short page as zero matches. Keep a row when the unanchored id on its `headRefName` or its title equals the filename id. One kept row is the PR. Zero kept rows, or more than one, halts and prints the numbers. The operator then passes the PR number.

Unanchored id, on a branch name or a title: search case-insensitively for `(?<![A-Za-z0-9])[A-Za-z][A-Za-z0-9]*-[0-9]+`, take the first match in that field, and uppercase it. Do not scan commit messages.

`<N>` below is the selected number. Step 2 uses that number.

## Step 2 — Merged state (Decision 4, Decision 10)

```bash
gh pr view <N> --json state,mergeCommit,mergedAt,baseRefOid,headRefOid,headRefName,body,commits,title,url,isDraft
```

If `gh` fails before merged state is known (not on `PATH`, auth, network, 5xx, missing PR, missing API key), halt with no wiki write, no Plane write, and no cleanup. Do not guess.

Require `state` equal to `MERGED`. Anything else halts:

```text
HALT: PR #<N> is <state>, not MERGED. /spec-land does not merge.
```

A draft, an open PR, and a closed-unmerged PR all halt. `mergedAt` alone is not the test. `isDraft` does not override a `state` other than `MERGED`. Never run `gh pr merge`.

`<landed>` is `mergeCommit.oid`. Hold `mergedAt`, `baseRefOid`, `headRefOid`, `headRefName`, `body` (JSON null is the empty body), `commits`, `title`, and `url`. `<n>` is the length of the `commits` array. A `commits` value that is not an array is not a count: step 5 treats it as a failed candidate and does not call `decide`.

## Step 3 — Fetch once (Decision 3)

Before the SHA check, in one window:

```bash
git fetch origin
git fetch origin pull/<N>/head
```

Do not fetch again after confirmation. Later steps use these refs. A non-zero fetch does not by itself halt. A missing object halts at the check that required it. Do not describe that missing object as "not an ancestor."

## Step 4 — Marker read (Decision 10, Decision 16)

Resolve the classifier before parsing. The script is the installed file, never a path in the target repo:

```bash
SCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-land/scripts/land_check.py"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
test -f "$SCRIPT" || echo "land_check.py not found — install with 'python sync.py install'"
```

The interpreter probe tests executability, not presence. All three assignments are required. If the pre-check prints not-found, halt. Do not run the script. A missing script is not a malformed marker. No side effects.

Read issue comments only. Same command `/ship-spec` and `/review-pr` use:

```bash
gh api --paginate --slurp repos/{owner}/{repo}/issues/<N>/comments
```

`--paginate` requests every page. `--slurp` wraps those pages in one array. Do not add `--jq`: gh rejects `--slurp` combined with `--jq` and exits 1. Flatten the pages one level to get the comments. Do not assume oldest-first. Do not parse `gh pr view --json comments`. A successful read is a JSON array whose every element is a JSON array, including `[]` and `[[]]`. Every object must have `id`, `body`, and `created_at`. A non-zero exit, a result that is not that array, or a missing `id`, `body`, or `created_at` on any object is a hard halt: no wiki write, no Plane write, and no cleanup. Do not treat a failed or truncated read as an absent marker. This halt still applies after `state` is `MERGED`.

A marker comment is one whose body, after stripping one leading U+FEFF and then surrounding whitespace, starts with `<!-- vigil-spec-land`. A comment that only mentions the token elsewhere is not a marker and is ignored, not malformed. The latest record is the marker with the greatest `created_at`, compared as a timestamp. Ties break by the greatest integer `id`.

Only a successful full read with zero marker comments sets verification skipped. Print a note. The confirmation says `SHA record: none — verification skipped`. Plane, wiki, and cleanup still run after confirmation. Do not compute a patch-id on this path.

When a latest marker exists, pass its raw body to `parse` on stdin:

```bash
printf '%s' "$BODY" | "$PY" "$SCRIPT" parse
```

- Exit 0, one stdout line: `head=<40> base=<40> patch-id=<40> review=<token>`. Hold those four fields. The review token is `passed`, `skipped`, `inconclusive`, or `not-run`. Show it. Do not halt on `skipped`, `inconclusive`, or `not-run`. A match means the landed code is the recorded code, not that it was reviewed.
- Exit 1, empty stdout: not a marker. This skill already selected the body by the prefix rule, so exit 1 is a contradiction. Halt. No side effects.
- Exit 2: malformed. Print the comment `id` and the raw body. Do not compare. The operator fixes or deletes the comment. Halt. No side effects.
- Any other exit, including 3: halt. No side effects. Exit 3 is an unexpected failure. It is not "no marker."

An argparse usage error exits 2. Every other uncaught exception from the script exits 3. An exit a subcommand does not list halts with no side effects.

## Step 5 — SHA verification (Decision 3, Decision 16)

Skip this step when step 4 set verification skipped.

Every id the script prints is 40 lowercase hex. Head equality is a string compare of `headRefOid` to the recorded head. It does not compare `mergeCommit.oid` to the recorded head. A squash or rebase landed commit is a new object.

**Head first.** On inequality, halt with no side effects. A patch-id match does not override a head mismatch.

```text
HALT: PR head <headRefOid> != recorded head <recorded-head>
```

Then `git log --oneline <recorded-head>..<headRefOid>`. Do not run `decide`.

**Candidates.** The skill computes them. `decide` classifies them. Do not reimplement the parent/commit table.

Single candidate, always:

```bash
git diff <landed>^1 <landed> | git patch-id --stable
```

Use the first whitespace-separated field of the single stdout line. A second field on that line is not a second id. The field must be 40 lowercase hex. A non-zero exit from `git diff` or `git patch-id --stable`, a second line, a missing field, or a field that is not 40 lowercase hex is the patch-id halt below. Do not pass that output to `decide`.

Parent count is the number of parent SHAs on `git rev-list --parents -n 1 <landed>` (one SHA plus N parent SHAs). The range candidate is computed only when that count is 1, `<n>` is greater than 1, and the single id differs from the recorded patch-id:

```bash
git diff <landed>~<n> <landed> | git patch-id --stable
```

The same one-id rule applies. `<landed>~<n>` is not used on any other path. When the range is not computed, call `decide` without `--range`. When the parent count is 2 or more, do not pass `--range`.

`decide` reads stdin and blocks on a terminal. Give it empty stdin:

```bash
"$PY" "$SCRIPT" decide --parents <P> --pr-commits <N> --recorded <recorded-patch-id> --single <single-id> [--range <range-id>] < /dev/null
```

Exit 0 prints `match single` or `match range`. Exit 1 prints `mismatch`. Exit 2 is bad arguments. Any exit other than 0 is the patch-id halt. Do not continue.

Patch-id halt, no side effects and no override flag. Print the recorded id, the single id, and the range id or `n/a`. Print this sentence: the hunks that landed are not the hunks recorded (conflict resolution, or nearby context from a base edit on a file the PR also touches). Then `git diff --stat <recorded-base>...<recorded-head>` and `git diff --stat` of the candidate that was compared (`<landed>^1 <landed>`, or `<landed>~<n> <landed>` when the range was computed). When the range candidate was computed, also run `git range-diff <recorded-base>...<recorded-head> <candidate-base>...<landed>`. A non-zero `git range-diff` is printed under the halt. It does not replace the halt. Recovery, verbatim in substance:

```text
This halt is terminal for v1. The resolved tree is mergeCommit.oid, not the PR head. There is no override flag. Do not push.
```

Do not tell the operator to push. `/review-pr` pushes the PR branch and cannot re-record a merged PR whose head branch is gone.

**Base drift**, only after a match. Merge-time base is `<landed>^1` when the result is `match single` (or single was the only candidate), and `<landed>~<n>` when the result is `match range`.

Before the walk:

```bash
git cat-file -e <recorded-base>
git cat-file -e <recorded-head>
git cat-file -e <landed>
```

Any missing object halts: `HALT: missing object <recorded base|recorded head|landed> <oid>`. Do not report it as "not an ancestor."

If `git merge-base --is-ancestor <recorded-base> <merge-time-base>` fails and all three objects exist, halt with `recorded base is not an ancestor of the merge-time base`. Do not print a range.

Commits in the walk: `git rev-list --reverse <recorded-base>..<merge-time-base>`. An empty list is no drift. Continue.

For each commit, `git diff-tree --first-parent -m --no-commit-id --name-only -r <commit>`. Exit 0 with no names means that commit has no first-parent file changes. It does not mean a merge was skipped. The PR path list is `git diff --name-only <recorded-base>...<recorded-head>`. A non-zero `git diff --name-only` or a non-zero `git diff-tree` is a halt, not an empty path list. Do not call `overlap` with an empty list that came from a failed command.

Normalize every path to forward slashes, then one `overlap` call. Stdin is two LF-delimited lists separated by a line that is exactly `--`:

```bash
"$PY" "$SCRIPT" overlap <<'EOF'
<walk paths, one per line>
--
<PR paths, one per line>
EOF
```

Two empty lists that came from successful commands are a valid call. Exit 0 prints `clear`. Exit 1 prints the shared paths, one per line. Exit 2 means the separator was missing: halt, no side effects. Any other exit halts, no side effects.

A non-empty intersection halts even when the patch-ids match:

```text
HALT: base moved and these commits touch files the PR touches:
<sha> <subject>
  <path>
```

For each walked commit whose own paths share a line with that output, print its sha, `git log -1 --format=%s <sha>`, and those paths. No side effects.

An empty intersection with a non-empty commit list is reported (subjects) and the run continues. Hold those subjects for the confirmation.

## Step 6 — Ticket (Decision 11)

A spec path already set the ticket id in step 1. The confirmation source is `spec path`. If that PR's branch or title also has an unanchored id and the uppercased id differs, the confirmation notes the disagreement. Do not halt. Do not switch to a different PR.

A PR number or a PR URL uses the branch search, then the title search, with the unanchored pattern from step 1.

- Both match and differ, and there is no spec path: halt and prompt, showing both ids. Do not guess. The operator types one id. Uppercase it. It must match `^[A-Z][A-Z0-9]*-[0-9]+`. A reply that does not match stops with no side effects. The confirmation then shows source `operator`.
- One match, or both agree: source is `branch`, `title`, or `branch and title`.
- Neither matches: prompt for the id. The same pattern applies. Source is `operator`. No side effects until the confirmation in step 8.

A host that cannot wait stops with no side effects.

`<PROJECT>` is the ticket prefix, the text before the first hyphen. The issue number is the integer after the hyphen.

## Step 7 — Checklist, instructions, worktrees (Decisions 7, 9, and 5)

A missing landed commit halts here, before confirmation, when step 5 did not already halt. `git cat-file -e <landed>` must succeed. A `mergeCommit.oid` that is missing or not 40 lowercase hex is that same halt. The confirmation is not reached. A missing instructions file does not halt.

**Checklist (Decision 7).** Strip one trailing CR from each line of the PR body before matching. The test-plan section runs from a line `## Test plan` to the next line matching `^## `, or to the end of the body. An unchecked box is a line matching `^\s*[-*] \[ \]\s+\S`. Drop lines inside that section that contain `Spec verdict:` or `Review gate:`. Boxes outside the section are not read. An empty body, a missing test plan, or a section whose only boxes are those audit lines means no unchecked boxes, so the target is Done. The line `- [ ] Post-merge verification` counts. It is not an audit line.

**states.json.** Read `<config-dir>/skills/ship-spec/states.json`. `<config-dir>` is `$CLAUDE_CONFIG_DIR` when set, otherwise `~/.claude` on Unix and `%USERPROFILE%\.claude` on Windows. In bash that is `"${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/ship-spec/states.json"`. Do not read the copy in the target repo. The declared post-land command installs into the directory this lookup reads. The first land of the PR that adds a key still sees the previously installed file, which may lack that key. Do not special-case the repo file.

For a prefix whose `states` map contains `Post-merge Checklists` and whose `state_groups` entry for that key is present, any remaining unchecked box selects Post-merge Checklists. Hold those unchecked lines verbatim, in order. Otherwise the target is Done, and unchecked boxes on a project with no such key are ignored. State UUIDs come only from that file's `states` map.

The Plane comment, posted only on the Post-merge Checklists path, is:

```text
Post-merge checklists for PR #<N>:
<unchecked lines, verbatim, in order>
spec-land:checklist PR #<N> <sha256>
```

`<sha256>` is the SHA-256 of the unchecked lines joined by `\n` (LF), UTF-8, lowercase hex, with no extra LF after the last line. The marker is visible text, not an HTML comment: Plane strips HTML comments from a comment body, so a hidden marker never persists. Skip the post only when an existing comment's text contains `spec-land:checklist PR #<N> <sha256>` for this PR number and this hash. A different PR number posts a new comment even when the lines match. A different set of lines posts a new comment and does not edit the old one. The state move recomputes the target from the current boxes on every run. Already in the target state: skip the move. In Done, with boxes now unchecked, and the Checklists key present: the target is Post-merge Checklists.

**Instructions (Decision 9).** Resolve these before confirmation. Do not re-read them after the fast-forward. Wiki writes, the slug, and the post-land command are these held values. The fast-forward is not what makes them readable.

The `CLAUDE.md` source is `git show <landed>:CLAUDE.md` when `git cat-file -e <landed>:CLAUDE.md` succeeds, and otherwise `CLAUDE.md` on disk in the main checkout (the first porcelain worktree) when that file exists. Do not read `CLAUDE.md` from a linked worktree. A file absent from the landed commit is normal. Halt only when `git cat-file -e <landed>` fails, or when `git show` fails on a file `cat-file -e` reported present.

Landed `AGENTS.md` is `git show <landed>:AGENTS.md` only when `git cat-file -e <landed>:AGENTS.md` succeeds.

No instructions file at all means no wiki configured and no post-land command declared. The run reports that and, after confirmation, continues to Plane and cleanup.

`wiki_root` uses the Path and wiki-bullet rule on the `CLAUDE.md` source, then on the landed `AGENTS.md`. "No wiki configured" means those files produced no wiki path.

Path rule, on one file: `Path:` under `## Wiki`. If that path does not exist, replace the username segment the way `/spec-brief` does (Windows: `$env:USERNAME`; Unix: `$USER`) and re-check. If no `Path:` line exists, take the first absolute path or `~/` path on a line that contains `wiki`. Expand `~/` before the existence check. Apply the username replacement to that path too when it does not exist. The first file that yields a path that exists wins.

Keys, first file that has the key wins, `CLAUDE.md` source then landed `AGENTS.md`. A section runs from its heading through the line before the next `^#{1,6} ` heading. Record which file each value came from.

| Key | Meaning |
|---|---|
| `Slug:` | Under `## Wiki`. No slug: skip the filemap write and say so. |
| `Log:` | `on` or `off`. Absent: `on` when `wiki_root` resolved, otherwise off. Any other value: warn and treat as off. |
| `Filemap:` | `on` or `off`. Absent: `on` when both `wiki_root` and the slug resolved, otherwise off. Any other value: warn and treat as off. `on` with no slug still skips the filemap write. |
| `Log file:` | Replaces `<wiki_root>/log.md`. |
| `Filemap file:` | Replaces `<wiki_root>/projects/<project_slug>/filemap.md`. |
| `## Post-land command` | The body must be one non-blank line, the same one-line rule as a `## Review command` section. Empty, or more than one non-blank line: warn, name the file, and skip. A missing section skips and says no command was declared. |

A `Log file:` or `Filemap file:` value that is absolute, or starts with `~/`, is used as that path (`~/` expanded). Any other value is relative to `wiki_root`. A missing filemap file is skipped and not created. The skill does not create a filemap. A missing log file is left to `prepend_log_entry.py`, which may create it.

**Worktrees (Decision 5).** The main checkout is the first `worktree` record in `git worktree list --porcelain`. The path is the text after `worktree ` on that line. Never remove it. Discover linked checkouts by exact branch match of `refs/heads/<headRefName>`, the same match `/review-pr` uses. Also accept the sibling path `<main>/../<TICKET-ID>-worktree` when its porcelain branch is that ref. Count a path once. The confirmation's fast-forward line uses this main checkout. Several linked checkouts: the confirmation says so. After `yes`, actions 1 and 2 still run, then steps 3–7 of the cleanup halt and the paths are listed. None: the confirmation says `no worktree`.

Default branch, for the fast-forward preview and for step 9.6, discovered the way `/ship-spec` Phase 0 step 5 does, against the main checkout:

```bash
git -C <main> symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|^refs/remotes/origin/||'
git -C <main> remote show origin | sed -n '/HEAD branch/s/.*: //p'
```

Do not use `git branch --show-current` from the directory the skill was started in.

## Step 8 — Confirmation (Decision 11)

One prompt, after every read above and before any write. Print:

```text
PR: #<N> <url>
State: MERGED
mergedAt: <mergedAt>
Ticket: <TICKET-ID> (<source>)
<disagreement note, only when a spec path and the PR id differ>
SHA: match head=<recorded-head> patch-id=<match single|match range> review=<token>
SHA record: none — verification skipped
A match means the landed code is the recorded code, not that it was reviewed.
Base drift: <subjects, only when the walk was clear and non-empty>
Plane: <Done|Post-merge Checklists>
Unchecked:
<verbatim lines, or none>
Wiki: log <on|off> filemap <on|off>
Slug: <slug or none> from <file or none>
Log switch: <on|off> from <file or default>
Filemap switch: <on|off> from <file or default>
Post-land command: <text or none> from <file or none>
Worktree: <path, or no worktree, or the list>
Local branch: <headRefName>
Remote branch: <headRefName>
Fast-forward: will run | skipped (<reason>)
Post-land command: will run | skipped (<reason>)
Reply yes to land <TICKET-ID>.
```

Print one SHA line, the match line or the skipped line. The sentence under it is always printed.

The operator replies `yes` or `y` to that id, after surrounding whitespace is stripped. Any other reply aborts with no side effects. A host that cannot wait prints the confirmation and stops with no side effects.

The fast-forward and post-land lines are a preview. Step 9 checks the conditions again.

## Step 9 — Actions after yes (Decision 5)

Each action is independent. A failure is reported. Earlier actions are not rolled back. A re-run resumes the unfinished ones (Decision 14). A halt in action 3 is the exception: it stops actions 4 through 7. That halt does not undo actions 1 and 2, and it does not continue into the remote delete.

Change directory to the main checkout before `git worktree remove`, the local branch delete, and the fast-forward. Do not run those from inside the worktree that is about to be removed.

### 9.1 Wiki log and filemap, when configured

No wiki configured: say so. Log off: say so. Filemap off, or no slug: say so and skip that write.

Log, when on. The installed spec-close script owns the byte write. This skill does not edit `prepend_log_entry.py` and does not hand-edit `log.md`.

```bash
LOGSCRIPT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spec-close/scripts/prepend_log_entry.py"
LOGPATH="<log file>"
command -v python3 >/dev/null 2>&1 && python3 -c '' >/dev/null 2>&1 && PY=python3 || PY=python
test -f "$LOGSCRIPT" || echo "log.md NOT written: prepend_log_entry.py not found at $LOGSCRIPT — install with 'python sync.py install'"
```

If that check reports not-found, skip the invocation. Recovery: re-run `/spec-land` on this PR. Do not hand-edit `log.md`.

The guard is `merge | <PROJECT> — <TICKET-ID> PR #<N>:` with the em dash U+2014. A rewrite of that character to `--` or `-` breaks the guard. `<PROJECT>` is the ticket prefix. The guard contains the PR number so two PRs for one ticket each get a line, and a re-run of the same PR hits exit 1. It does not collide with spec-close's `close |` guard.

The heading date is the later of this run's UTC date and the newest `## [YYYY-MM-DD]` date already in the file, so the date passed in satisfies `entry_date >= newest_date`. A missing log file uses this run's UTC date. The heading stays one line. `<one-line>` is the PR title with line breaks removed, or the ticket id when the title is empty. `<short-sha>` is `mergeCommit.oid` abbreviated to 12 hex characters. The body contains `mergedAt` and the landed sha and no line that starts with `## [`.

```bash
if "$PY" "$LOGSCRIPT" "$LOGPATH" --guard 'merge | <PROJECT> — <TICKET-ID> PR #<N>:' <<'PREPEND_LOG_ENTRY_EOF'
## [YYYY-MM-DD] merge | <PROJECT> — <TICKET-ID> PR #<N>: <one-line> (`<short-sha>`)

Merged at: <mergedAt>
Landed: <mergeCommit.oid>
PREPEND_LOG_ENTRY_EOF
then rc=0; else rc=$?; fi
echo "prepend_log_entry_exit=$rc"
```

Single-quote the guard. Double-quote both paths. Keep the delimiter. Branch on the echoed integer, not on the host's pass/fail signal.

| Exit | Report |
|---|---|
| 0 | The outcome token on stdout: `prepended`, `fresh`, or `created` |
| 1 | `log.md: entry already present — skipped` |
| 2, or any other non-zero, or the not-found pre-check | `log.md NOT written` |

On exit 2, also surface stderr. Do not hand-edit `log.md`. Continue the other actions.

Filemap, from the diff the patch-id step accepted. `gh pr view --json files` is not the source. The status letter is the first character of `git diff --name-status`:

- `match single`, or a landed commit with two or more parents: `git diff --name-status <landed>^1 <landed>`.
- `match range`: `git diff --name-status <landed>~<n> <landed>`. Use `~<n>` only when `decide` returned `match range`.
- No marker: `git diff --name-status <landed>^1 <landed>`, and the report says verification was skipped. Do not use `~<n>`. That walk includes foreign base commits on a squash.

A non-zero `git diff --name-status` is a failed filemap write. Report it. Do not treat it as an empty diff and do not delete sections.

Apply each line to the filemap file, paths in forward slashes. A status whose first character is not `D`, `R`, `A`, or `M` is listed and not edited. `R` lines are `<status><tab><old><tab><new>`.

- `D`: delete the section whose heading line is `###` + space + backtick + path + backtick, from that heading through the line before the next markdown heading of any level, or through EOF. A missing heading is reported skipped. A re-run does not repair a partial cut: once the heading is gone, the missing-heading rule skips it.
- `R`: rename that heading from the old path to the new path. Leave the section body. Old heading missing and new heading present: skip. Both missing: skip and report. Both present: skip and report.
- `A` whose final path component matches `test_*.py`, `*.test.ts`, or `*.test.js`: if the heading is absent, add a heading line of that same shape and one bullet `- **Purpose:** Test added in PR #<N>.`
- `A` of any other path: if the heading is absent, add the same heading and `- **Purpose:** Added in PR #<N>.` Do not invent exports or dependencies. Do not ask.
- `M`: do not edit the filemap. List those paths as not filemap-relevant.

A missing filemap file is skipped. Do not create it.

### 9.2 Plane comment and state move (Decisions 6 and 7)

This is the only Plane write for this stage. A Plane failure does not block cleanup.

Look up the prefix in the installed `states.json` from step 7. A missing file, an unreadable file, invalid JSON, or a missing prefix: skip Plane, print the manual steps, and continue. When Plane is unreachable, or the ticket lookup fails, skip Plane, print the same manual steps, and continue. When the target key (`Done` or `Post-merge Checklists`) is absent from the prefix's `states` map, skip Plane, print the state names that are present, and continue.

Manual steps, the unreachable-tracker shape:

```text
Plane unreachable — skipping state update and checklist comment.
To complete manually:
  1. Move <TICKET-ID> to <target state name> in Plane
  2. Comment on the ticket with the checklist body when the target is Post-merge Checklists:
<checklist body, or "no checklist comment" when the target is Done>
```

When the prefix is missing, name that instead of "unreachable", and say the operator chooses Done, or Post-merge Checklists when that state exists and unchecked boxes remain.

On the checklist path, list existing comments with the issue tracker's work-item comment-list capability, or the equivalent in your host. If the list cannot be read, do not post. Report `checklist comment: NOT posted (comments unreadable)`, print the body, and still attempt the state move. Skip the post only when an existing comment contains this PR's hash marker from step 7. Post with the work-item comment capability, or the equivalent in your host. A failed post does not skip the state move and does not roll back the log.

State move: the work-item state-update capability, or the equivalent in your host, to the UUID in the installed `states` map. Read the ticket's current state UUID with the work-item lookup capability, or the equivalent in your host. Already equal to the target UUID: skip the move. Do not invent a UUID.

### 9.3 Worktree remove

Several linked checkouts of `headRefName`: halt actions 4 through 7 and list them. Do not remove one of them.

Otherwise `git worktree remove <path>` without `--force`, from the main checkout. Skip remove when `git -C <worktree> status --porcelain` is non-empty, when the path is missing, or when the branch is checked out only in the main checkout. None of those is a failure. A missing path reports `no worktree` when no linked checkout was found.

A dirty linked worktree skips the local branch delete and the remote branch delete, and the run says so. The fast-forward and the post-land command still run. They do not run when this action halted.

If the branch is checked out only in the main checkout, skip remove and skip the local branch delete. The remote-tip check in 9.5 still applies.

### 9.4 Local branch delete

Skip when this action was skipped above, or when the branch is already gone (report it as skipped, not as a failure). Skip when `git rev-list --count <headRefOid>..<local-tip>` is greater than 0. Those are commits on the local branch that are not in the merged PR head. A failed `rev-list` skips the delete and is reported. Do not use `-D` on that failure.

Otherwise `git branch -d "$branch"`. A squash or rebase leaves the original commits unmerged into the landed commit, so `-d` refuses even when the tip equals `headRefOid`. When the SHA check passed and the tip equals `headRefOid`, retry `git branch -D` and report `local branch deleted (-D; squash or rebase, tip matched the recorded head)`. When the SHA check was skipped because no marker existed, do not use `-D`. If `-d` refuses, skip and report.

### 9.5 Remote branch delete

`git push --force-with-lease="refs/heads/$branch:<headRefOid>" origin --delete "$branch"` only when `git ls-remote --heads origin "$branch"` prints a tip equal to `headRefOid`, or the ref is already gone (report `already deleted`). Empty output means gone only when `ls-remote` exited 0. A non-zero `ls-remote` skips the delete and is reported as a lookup failure. The lease refuses the delete if the tip moved after that check; report a lease rejection as skipped. A different remote tip is skipped and reported. Extra local-only commits do not block the remote delete when the remote tip equals the merged PR head. The local branch stays in that case. No other `--force`. A failed remote delete does not skip the fast-forward. A re-run retries the delete.

This is the only remote git mutation.

### 9.6 Fast-forward the main checkout (Decision 13)

`git -C <main> merge --ff-only origin/<default>` only when that checkout's current branch is the default branch and `git -C <main> status --porcelain` is empty. The default branch is the one step 7 discovered. The origin ref is the one step 3 fetched. Do not fetch again.

Otherwise skip this action and action 9.7 and say why. A non-zero `git merge --ff-only` also skips 9.7, is reported with the git error, and is not "already up to date." `--ff-only` does not start a merge on that failure. Do not retry the merge in this run. A later run may try again when the conditions hold. Do not stash.

"Already up to date" is exit 0. After an exit of 0, including that message, `git -C <main> merge-base --is-ancestor <landed> HEAD` must exit 0 before the post-land command runs. A non-zero exit skips the post-land command, and the summary says the main checkout does not contain the landed commit.

### 9.7 Post-land command

Runs only when 9.6 exited 0, including "Already up to date," and the ancestor check passed. A non-zero merge is not that case. It also does not run when no command was declared, or when the section was empty or had more than one non-blank line. Say which.

Run the held command in the main checkout. A non-zero exit of the command is reported, not retried in this run, and does not roll back earlier steps. A re-run tries again when the fast-forward conditions hold.

## Step 10 — Summary (Decision 12)

```text
=== LANDED: <TICKET-ID> ===
PR: <url>
SHA: match | skipped
Plane: <from> → <to> | skipped
Wiki: log <outcome> filemap <outcome>
Next: /spec-close <spec-path>
Suggested wiki commit: <names of files this run wrote, or none>
```

`SHA` is `match` or `skipped`. `Plane` is `skipped` when Plane was not written. When the ticket was already in the target state, print `<name> → <name>`. `Wiki` outcomes are the log token or `log.md: entry already present — skipped` or `NOT written` or `off` or `no wiki`, and for the filemap `written`, `skipped`, `off`, `no slug`, `missing file`, or `NOT written`.

Omit the spec path on the Next line when the run had no spec path. That line is then `Next: /spec-close`.

The suggested commit names only the files this run wrote. It is text for the operator. Do not run it. Do not print `git add`, `git commit`, or `git add -A`. When the run wrote no wiki file, the value is `none`.

## Re-run (Decision 14)

A second run on the same merged PR resumes unfinished actions and reports each one. It does not duplicate a merge log entry (guard exit 1), a filemap section (heading already present), or a Plane checklist comment (same PR number and same hash). Plane state is recomputed from the current boxes. A missing worktree, an already-deleted local branch, and an already-deleted remote ref are reported as skipped, not as failures. Concurrent runs are last-writer-wins. There is no lock.

## Tool-use notes

- Your host's shell for `git`, `gh`, and the two installed Python scripts. `vcs-host` is required. A missing `gh` before merged state is known is the step 2 halt.
- Your host's file read and write for the wiki filemap and for instruction files. `log.md` is not a direct write: `prepend_log_entry.py` owns it.
- Issue-tracker state-update and work-item comment capabilities (for example, `mcp__plane__update_work_item` and `mcp__plane__create_work_item_comment` in Claude Code, or the equivalent in your host). Listing comments for the hash check uses the same integration's comment-list capability, or the equivalent in your host. `issue-tracker` is optional: a missing tracker skips Plane and continues.
- Work-item lookup for the current state UUID, for example `mcp__plane__retrieve_work_item_by_identifier` in Claude Code, or the equivalent in your host.
- No shared-memory call. The ticket id comes from the spec path, the branch, the title, or the operator.

## Failure modes

- **PR not merged.** The step 2 halt. This skill does not merge.
- **`gh` failed before merged state is known, or the comment read failed.** Hard halt. No wiki, no Plane, no cleanup. Do not treat a truncated comment read as an absent marker.
- **No marker, on a successful full read.** Verification skipped. Confirmation, then Plane, wiki, and cleanup still run.
- **Malformed marker.** Print `id` and raw body. The operator fixes or deletes the comment. Do not compare.
- **Head, patch-id, or overlap halt.** No side effects and no override. The patch-id recovery says not to push.
- **Missing object.** Name the object. Do not call it a failed ancestor check.
- **Recorded base is not an ancestor.** That sentence only, no commit range.
- **Several worktrees.** Actions 1 and 2 stay. Actions 4–7 do not run.
- **Dirty linked worktree.** Remove, local delete, and remote delete are skipped. Fast-forward and the post-land command still run.
- **Plane skipped.** Manual steps. Cleanup continues.
- **Log script missing or exit 2.** `log.md NOT written`. Do not hand-edit the file. Re-run `/spec-land`.
- **Fast-forward refused or the main checkout does not contain `<landed>`.** The post-land command does not run. A later run may try again.
- **Host cannot wait.** The id prompt or the confirmation stops the run. Nothing is written.
