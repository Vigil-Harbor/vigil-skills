---
name: key-rotation
description: >
  Guide an operator through a credential-exposure response for credentials
  of every kind: confirm the notice, inventory names, contain, audit use,
  rotate per provider role, verify, and write a record. The operator
  performs every provider action. The skill never prints, stores, or
  moves a secret value.
user_invocable: true
requires:
  shell: true
  filesystem: [read, write]
  network: false
  subagents: false
---

# /key-rotation

This skill is a process guide for a credential-exposure response. The operator performs every action at a provider. The skill asks, explains, and records. It never prints, stores, or moves a secret value, a last-N fragment, or a masked value. It never calls a provider, never revokes, and never takes a service down.

One gitignored record in the target project is the only output. The record carries variable names and, only after permission in this run, SHA-256 fingerprints. `scripts/prepare_record.py` does preflight and the read-only helpers. The skill does not open a file that holds a value. The script reads those files and does not print the value.

The blank record shape is `reference/record-template.md`. The script reads that file only on the create path. This skill does not paste it.

No mode and no step depends on a tracker or on another skill. Follow-ups stay in the record. The skill does not post or file them, and it does not send the notify list.

## What this skill must not do

- Call a provider, revoke a credential, or take a service down.
- Print, store, or move a secret value, a last-N fragment, or a masked value. Refuse a fragment or a masked value if one is offered. Do not place either in the record or the conversation.
- Open a file that holds a value. Helpers read those files.
- Treat silence, or this skill's own recommendation, as a sign-off.
- Start containment before the confirm sign-off, or when the operator says the channel is not the provider's own.
- Rotate first for a resident package or tooling compromise. Do not sweep or clean. The order there is sweep, then clean, then rotate, and this skill does not perform it.
- Post to a tracker or send the notify list.
- Run a helper or a hash without that run's permission.
- Overwrite or truncate an existing record. Do not remove a `Sign-off (close):` line.
- Name a project, a client, a person, a company or vendor, a ticket, or a variable from an incident record. Providers appear as roles.
- Describe how to obtain, forge, or misuse a credential. Wording stays defensive: response and prevention.

Patching, trust-store work, and forensics are not steps. A resident package or tooling compromise is not this flow.

## Eleven-item process

Decisions already applied: the skill makes no provider call, patching and forensics are not steps, and nothing is filed. Each item names the phase step that carries it.

| # | Item | Phase step |
|---|---|---|
| 1 | Confirm the notice on the provider's own channel, and do not sign off on a no | Phase 0, first step |
| 2 | Record the notice link and the stated exposure window | Phase 0, before containment |
| 3 | Inventory variable names, from a candidate list the operator confirms | Phase 1 |
| 4 | Containment the operator carries out, grouped by role | Phase 2, and only after item 1 is signed |
| 5 | Usage audit of each confirmed name | Phase 3 |
| 6 | Hidden-consumer sweep of the project tree | Phase 3, one script walk |
| 7 | Rotation per provider role, done by the operator | Phase 4 |
| 8 | Same-or-different comparison by hash, after permission, via the script | Phase 3, optional step |
| 9 | Verification that the replacement works and the old credential does not | Phase 5 |
| 10 | A disposition for every name | Phase 6, the body of that phase, before its sign-off |
| 11 | A record of role, consumers, scopes, time, verification, and follow-up lines | Phase 6, written in the record and not filed |

## Blocking gates

1. Helpers run only after the operator grants permission in this run.
2. A phase closes only when the operator's sign-off and its evidence are written in the record.
3. Containment guidance starts only after the operator affirms that the channel is the provider's own and the link and the exposure window are recorded.

The phase that a sentence binds repeats that sentence.

## Project section

The optional project section heading is exactly `## Key rotation`. No other heading matches. Keys:

```text
Providers:
Shared accounts:
Notify:
Record path:
```

`Providers:` is the roster of roles. `Shared accounts:` notes when one credential covers two roles. `Notify:` is the operator's notify list. `Record path:` is a project-relative pattern.

Use project-instructions text the harness already supplied. When the harness supplied none, read `CLAUDE.md` and then `AGENTS.md` at the project root, each only when that file can be read, and use the first `## Key rotation` section. A missing or unreadable file is an absent section. Ask. Do not stop. A missing section or a missing key is asked the same way.

Every run that calls the script, including `status`, resolves `Record path` before the script searches. Do not run the script until that resolution is done.

- A present `Record path:` key is passed as `--record-path`.
- When the key is absent, offer the default `.key-rotation/record-YYYY-MM-DD.md` under the project root. The operator accepts it or supplies a project-relative path.
- Pass no `--record-path` only when the operator accepted the default.
- A supplied path is passed as `--record-path` for this run. Show this line for the operator to add to the project section, with their path in place of the default:

```text
Record path: .key-rotation/record-YYYY-MM-DD.md
```

Until that line is added, each run asks again. The token `YYYY-MM-DD` may appear only in the final path component. The path must end in `.md` and must not name an existing directory. The script rejects anything else with `prepare_record: record path rejected` and creates nothing. The script, not the model, replaces `YYYY-MM-DD` in the final component with the local calendar date of the creating run.

A changed `Record path` does not move an open record. The script still reuses the single open record it finds under `.key-rotation/` or under the resolved parent. Until that record is closed, the operator passes its path with `--record-path` or restores the key. Do not move the file.

Ask for each still-missing key other than `Record path` during Phase 0. Preflight already needed `Record path`.

## Modes and resume

Check the argument before any script run.

- No mode argument is the no-argument run: resolve the record path, run preflight, then continue at the first open sign-off.
- A mode argument is one of `inventory`, `contain`, `audit`, `rotate`, `verify`, `close`, `status`.
- Any other token: name those seven modes and write nothing. Do not run the script. Hardening is not a mode.

Permission is per run. A note in an old sign-off that helpers were allowed is evidence, not a grant for this run.

A mode does not reopen a closed record. Mode runs pass `--reuse-only`. A new record starts from a no-argument run when no open record exists, or from an explicit operator instruction that passes `--new`. While another record is open, the file `--new` creates is resumed only when the operator picks it with `--choose`. A later run without `--choose` does not make that choice, whatever `--record-path` holds. Pass `--choose` only with a path the operator picked from the script's list. A single open record is reused without `--choose`. The script does not pick the earliest name.

Do not start a second editor while one run is in progress. Two sessions on one record are last-writer-wins. There is no lock.

### No-argument run

Resolve the record path, then run:

```text
scripts/prepare_record.py --project-root <dir> [--record-path <path>]
```

Add `--choose <path>` only when the operator picked one path from a previous open list. Add `--new` only when the operator explicitly instructs a new record. Do not pass `--template`.

On exit 0, stdout is one line, `created: <absolute path>` or `reused: <absolute path>`. Keep that path. Continue at the first open sign-off in this order: confirm, inventory, contain, audit, rotate, verify, hardening, close. A no-argument resume that stops on `Sign-off (hardening)` performs Hardening there. `close` only checks that the hardening sign-off is already closed.

On a non-zero exit, show the script's stderr and do not enter a phase. A stop after preflight has succeeded names the path from the `created:` or `reused:` line.

### Mode run

Resolve the record path, then run preflight with `--reuse-only`:

```text
scripts/prepare_record.py --project-root <dir> [--record-path <path>] --reuse-only
```

Add `--choose <path>` beside `--record-path` when more than one record is open and the operator has picked one. Do not omit `--choose` while more than one record is open. Do not pass `--new` on a mode run.

If the first stderr line is `prepare_record: no open record`, the following lines that do not start with `prepare_record:` are closed records, possibly none. When that list is non-empty, say the incident is closed. When it is empty, say that no record exists. Stop. Do not create a record.

Then check the prerequisite. If a prerequisite sign-off is open or missing, stop and name it. Do not perform the earlier phase inside the later mode.

| Mode | Prerequisite |
|---|---|
| `inventory` | confirm closed |
| `contain` | confirm closed |
| `audit` | confirm closed and inventory closed |
| `rotate` | confirm closed and contain closed |
| `verify` | confirm closed, and each role to be verified has a rotate log entry |
| `close` | inventory, contain, audit, rotate, verify, and hardening all closed |
| `status` | none |

### Status

`status` runs this and nothing else:

```text
scripts/prepare_record.py --project-root <dir> [--record-path <path>] --status
```

It prints every open record as an absolute path, one per line, and writes nothing. It does not create a record and does not modify `.gitignore`. Zero open records prints no path and exits 0. More than one open record is still exit 0.

- One path: report the state of each sign-off line, the count of confirmed names, the count of blank Role cells, and the follow-up lines. List names with an empty or invalid Disposition only when every sign-off before close is closed. Before Phase 6 every Disposition cell is empty by rule.
- More than one path: list them and do not pick one.
- No path: say so and stop.

A `prepare_record: skipped unreadable <path>` line means a record could not be read. Say that. Delete nothing.

### Preflight failures

Exit 0 on create, reuse, or a read-only mode that ran, including when advisories were printed. Exit 1 on every `prepare_record:` failure. Exit 2 is argparse only: the parser's own message, no `prepare_record:` prefix. On exit 2, show that message and write nothing.

These three failures are a block. The first stderr line is the header. The relative paths are the following lines that do not start with `prepare_record:`. Advisory lines, if any, follow the paths.

- `prepare_record: multiple open records` — show the list and stop. The next run passes the path the operator picks, as printed, as `--choose`, beside the usual `--record-path`.
- `prepare_record: no open record` — see Mode run.
- `prepare_record: chosen record not open <path>` — say the chosen record is no longer open, show the open list, and stop. The next run passes the path the operator picks from that list as `--choose`, or omits `--choose` only when the operator says to continue the one listed record. When the list is empty, say the chosen record is closed and stop.

`prepare_record: record unreadable <path>` is not one of those three blocks. A `prepare_record: skipped unreadable <path>` line precedes it. Show the path and stop. The operator restores the file, picks a readable open record with `--choose`, or instructs a new record with `--new`.

Other exit-1 lines, shown as the script prints them:

- `prepare_record: not a git work tree`
- `prepare_record: not a git work tree <operand> <exit code>`
- `prepare_record: path is outside the project`
- `prepare_record: path is outside the project <raw argument>`
- `prepare_record: parent is not a record directory`
- `prepare_record: record is tracked`
- `prepare_record: ignore pattern rejected`
- `prepare_record: ignore check failed`
- `prepare_record: record path rejected`
- `prepare_record: template missing <path>`
- `prepare_record: write failed`
- `prepare_record: gitignore changed`
- `prepare_record: not a readable file <path>`

Show the line and stop. Do not create or edit a record by hand to get past a failure. A hard kill during the ignore publish can leave a root-level `.key-rotation.<random>` file that holds only ignore-file bytes. The operator deletes it. This skill does not.

On POSIX the record directory is mode `0700` and the record is mode `0600`. On Windows those bits are advisory and the files inherit the project's access control list. Do not add access-control-list code.

## Permissions

Compare the reply case-insensitively after stripping surrounding whitespace. Only the single word `yes` grants. Anything else, including silence, refuses.

Helpers run only after the operator grants permission in this run.

Permission A, asked once in a run before any helper. It allows `--list-names` and `--match-names` for this run only. It does not allow hashing.

> May this run list variable names and search this project's files for those names? It will not copy values into the record or the conversation. Reply yes to allow it for this run only. Any other reply skips the helpers and you do those steps by hand.

Permission B, asked only when the operator wants a same-or-different check. Never treat permission A as permission B. It allows `--hash-name` and `--hash-names` for this run only.

> May this run compute a SHA-256 fingerprint of each value, for a same-or-different comparison? Only the fingerprint can go in the record. A hash of a short or guessable value is weak. Reply yes to allow it for this run only. Any other reply skips hashing.

The value must not appear on the process command line, in the record, or in the conversation. Pass names in the names file. `--hash-name` takes a name, never a value.

A hash compares stored bytes. Quotes and spaces stay, so an unquoted stored form and a quoted stored form of the same characters read as different, and a trailing comment reads as different. State that beside the hashing step. State again that a hash of a short or guessable value is weak. No fragment and no masked value.

## Sign-offs

A new record carries these lines, each exactly `open`:

```text
Sign-off (confirm): open
Sign-off (inventory): open
Sign-off (contain): open
Sign-off (audit): open
Sign-off (rotate): open
Sign-off (verify): open
Sign-off (hardening): open
Sign-off (close): open
```

A sign-off is closed only when that line exists and the text after the colon, stripped, starts with `closed:` using a case-insensitive comparison, and at least one non-whitespace character follows that prefix. Write `closed: ` plus one paragraph of the operator's decision and the evidence. Anything else stays open, including `open`, `Open`, `open.`, `still open`, and `left open`. Do not close a sign-off from silence.

A phase closes only when the operator's sign-off and its evidence are written in the record.

Inside a file that is already a record, a missing phase line means that phase is open. Append that line as `open`. Do not rewrite a line that is already closed, except the reset below.

A file is a record only when it contains a line that, after optional leading whitespace, starts with `Sign-off (close):`. A mention of that text inside another line is not that line. The file is open when that line exists and is not closed. It is closed when that line is closed. When more than one such line exists, the file is open unless every copy is closed. A file without that line is not a record. Do not reuse it and do not append a sign-off there.

One close is allowed without the earlier phases. When Phase 0 ends on a negative channel answer or on the resident-compromise stop, ask whether to close this record. Only the single word `yes` accepts. On yes, write this line and nothing else, so a false alarm does not leave an open record for the next incident:

```text
Sign-off (close): closed: not confirmed — <one-line reason>
```

Leave the other sign-off lines as they are. Write no disposition sweep. On any other reply, leave the record unchanged and stop.

### Reset on a real change

On a real change to the set of names or roles, or to a role's log entry, set the re-entered phase's own sign-off and every later sign-off back to open before continuing. Rewrite each as `open (was: <previous value>)`. That reads as open and keeps the earlier evidence. The operator signs that phase off again with fresh evidence. A closed sign-off must not carry evidence for a set it did not cover.

Later means later in the sign-off order above. Do not append a duplicate row, role subsection, or follow-up line.

### How to edit the record

Change only the lines that phase touches. Apply one targeted edit per contiguous run of changed lines, or one write spanning the batch when the edit takes one region only. Never re-emit the whole file for a partial batch. Never re-emit the whole table to change one cell. Never remove the `Sign-off (close):` line.

Upsert disposition rows by name and `### Role:` subsections by role. Collect a phase's row changes and apply them in one record write per operator batch. Do not write the record once per name. A `### Role:` subsection write may be one per role.

The skill has no fsync or replace primitive. The script's create path and its ignore-file write do. Do not invent a second writer.

Confirmed rows use the disposition table. Columns are Name, Role, Disposition, Evidence. Evidence holds consumers for that name, one line, no value. There is no value column. Leave Role empty until Phase 2. Leave Disposition empty until Phase 6. Do not fill a Disposition cell before Phase 6.

The provider log is one `### Role: <role>` subsection per role, with consumers, scopes, verification, and time. Do not append a second subsection for the same role.

Follow-up lines under `## Follow-ups` are `Follow-up: <one sentence>` or `Blocker: <one sentence>`. Do not append a follow-up whose sentence is already present.

At the design target the record holds about 100 names and 12 role subsections. That is a shape, not a cap. Do not paste the table into the conversation when the phase does not need it. Do not open a second project. Do not spawn a helper per name or per role.

## Script

Run this skill's `scripts/prepare_record.py` with the host Python. Stdlib only. The forms below are the script's usage. Do not invent flags. Do not pass `--template`.

```text
prepare_record.py --project-root <dir> [--record-path <path>] [--choose <path> [--reuse-only] | --new | --reuse-only] [--template <path>]
prepare_record.py --project-root <dir> [--record-path <path>] --status
prepare_record.py --project-root <dir> [--record-path <path>] --list-names [--file <project-relative>]...
prepare_record.py --project-root <dir> [--record-path <path>] --match-names --names-file <project-relative>
prepare_record.py --project-root <dir> --hash-name <name> --file <project-relative>
prepare_record.py --project-root <dir> --hash-names --names-file <project-relative> --file <project-relative>
```

`--project-root` is the target project. `--record-path` and `--choose` accept a project-relative path or an absolute path, including a `created:` or `reused:` path as printed. Hash modes do not take `--record-path`; the script ignores it. Do not pass it on a hash invocation.

Read-only modes do not create a record, do not truncate one, and do not modify `.gitignore`. They are mutually exclusive with each other and with `--status`, `--new`, `--choose`, `--reuse-only`, and `--template`. `--new` and `--reuse-only` are mutually exclusive. `--choose` may be combined with `--reuse-only`.

`--list-names` prints one distinct name per line, the first time it is a candidate, with a trailing newline, and no other byte. It reads env files only, by name: a regular file named `.env`, `.env.*`, or `*.env`, plus each file named with `--file`. A name is printed only when it matches the assignment grammar and passes the three withhold rules. Quoted spans, armored spans, and backslash-continued lines are value bytes and are never printed. A line whose only `=` bytes are trailing padding is never printed. The three withhold rules are: a mixed-case left-hand side; an armored span; a value that, once trailing spaces and tabs are removed, is empty or made only of `=` bytes. The last assignment of a name in one file wins. The operator confirms the candidate list before any name enters the record.

`--list-names` stderr, path and line only, never content:

- `prepare_record: withheld line <path>:<line>`
- `prepare_record: unterminated span <path>:<line>`
- `prepare_record: unsupported syntax <path>:<line>`
- `prepare_record: duplicate assignment <path>:<line>` (no name; the name is already on the candidate list, so it needs no hand listing)
- `prepare_record: skipped binary <path>` (env-named file or `--file`; exit 0)
- `prepare_record: skipped unreadable <path>`
- `prepare_record: skipped outside-root link <path>`

A `--file` named `.envrc` or ending in `.sh` is not read and prints no stderr line. The operator lists those names by hand. The operator names files that hold assignment lines, never a key or certificate file. When the withheld report covers most lines of a file, that file is an empty-value template or the project uses mixed-case names: the operator reads that file's names in one pass and adds only names not already on the candidate list. A withheld line directly after a long unquoted value, or a line whose value is only `=` bytes, is a wrapped tail, not a name. The operator does not list it. This skill does not open the file.

`--list-names --file` on a missing or non-regular file exits 1 with `prepare_record: not a readable file <path>`.

`--match-names` prints `<name> <path>`, one hit per name per file. The name is the first token. It prints paths, not lines. It skips a binary file with no `skipped binary` line. It reports `prepare_record: skipped unreadable <path>` and `prepare_record: skipped outside-root link <path>`. Pass the record's own path from the `created:` or `reused:` line as `--record-path` so the walk skips the record itself and the temps beside it, not the directory that holds them.

`--hash-name` and `--hash-names` print one line per requested name, in names-file order for `--hash-names`:

- `<name> <64 lowercase hex>`
- `<name> hash: absent`
- `<name> hash: unterminated`
- `<name> hash: unread`

`hash: absent` is an empty stored value, or a name with no assignment in a file that was read. `hash: unread` is only for a name with no assignment before an unterminated span. On `prepare_record: unsupported syntax <path>:<line>` during a hash, names already assigned keep their digest, and names not yet seen stay `hash: absent`, not `unread`. A name assigned before an unterminated span keeps that result, and the script prints `prepare_record: possibly reassigned <name> <path>`. Hash modes report a duplicate as `prepare_record: duplicate assignment <name> <path>` with no line number. The record stores the fingerprint or the `hash:` token, never a value.

A hash `--file` that is missing, non-regular, unreadable, or whose first 8192 bytes contain a NUL byte exits 1 with `prepare_record: not a readable file <path>`. Do not treat that as `hash: absent`. No `hash: absent` line is printed for that path.

A path whose real path is outside the project exits 1 with `prepare_record: path is outside the project <raw argument>` and prints no file bytes.

## Phase 0 — Confirm

Preflight has already run. On a non-zero exit this phase was not entered.

If the operator describes a resident package or tooling compromise rather than a provider that may have read stored secrets, stop. Say this skill does not rotate first, and that the other order is sweep, then clean, then rotate. Do not perform that sweep. Ask whether to close this record as not confirmed, as Sign-offs allows.

### First step — confirm the channel (item 1)

Ask for the notice link, the channel, and the exposure window as the notice states it. The operator says whether the channel is the provider's own. Do not fetch the link. A negative answer stops the run before containment and is not evidence. Ask whether to close this record as not confirmed. The confirm sign-off stays `open` until the operator says the channel is the provider's own.

### Notice link and exposure window, before containment (item 2)

Record the notice link and the stated exposure window. Ask for each project-section key that is still missing, other than `Record path`. Show the notify list and record one evidence line: the operator notified them, or the operator skipped them. Do not send a message.

Containment guidance starts only after the operator affirms that the channel is the provider's own and the link and the exposure window are recorded.

Do not start containment. Sign off only when the link and the window are non-empty and the operator has affirmed the channel. Evidence is the link, the window, the affirmative answer, and the roster.

A phase closes only when the operator's sign-off and its evidence are written in the record.

## Phase 1 — Inventory

Item 3. Gate: helpers run only after the operator grants permission in this run.

Ask permission A. If allowed, run `--list-names`, and add `--file` for each further env-style file the operator names. Pass `--record-path` when the open record's path is known, using the `created:` or `reused:` path as printed:

```text
scripts/prepare_record.py --project-root <dir> [--record-path <path>] --list-names [--file <project-relative>]...
```

Show the candidate list from stdout. Show each stderr advisory by path and line only. The operator lists by hand the names behind a withheld line, an unterminated span, an unsupported-syntax stop, a skipped binary, a skipped unreadable file, an outside-root link, or a shell file the script did not read. A duplicate-assignment line needs no hand listing. The operator confirms which names belong in this incident. Only then write one disposition row per confirmed name, in one edit.

If permission A is refused, the operator lists the names. The same confirmation is required before any name enters the record.

Upsert by name. A second run updates the existing row and does not append a duplicate. Leave Role empty until Phase 2. Leave Disposition empty until Phase 6.

A phase closes only when the operator's sign-off and its evidence are written in the record. Evidence is the count of confirmed names and whether helpers ran in this run.

## Phase 2 — Contain

Item 4, and only after item 1 is signed. If the confirm sign-off is open or missing, stop.

Containment guidance starts only after the operator affirms that the channel is the provider's own and the link and the exposure window are recorded.

Group the names the operator marks exposed by provider role, and emit one containment note per role. When shared-account notes say one credential covers two roles, one note names both. Say which role the operator should disable, and stop there. The operator writes what they did. No values.

When the operator assigns a role to a confirmed name, upsert that row's Role cell. Do not set Disposition in this phase. A confirmed row whose Role cell is blank blocks the rotate sign-off until the operator fills that cell or writes one `Follow-up:` for that name.

A phase closes only when the operator's sign-off and its evidence are written in the record. Evidence is those roles.

## Phase 3 — Audit

Items 5, 6, and 8. Prerequisites: confirm and inventory are closed.

Helpers run only after the operator grants permission in this run.

### Usage audit (item 5)

For each confirmed name, record where it is used. A consumer that is not in the tree is a question to the operator. An unanswered question becomes one `Follow-up:` line. Do not append a follow-up whose sentence is already present. Per-name consumers stay on the disposition row (one line, no value) or on that role's subsection.

### Hidden-consumer sweep, one script walk (item 6)

If helpers are allowed in this run, write the confirmed names, one per line and with no values, into a dot-prefixed `*.tmp` in the record directory. Pass the record's own path from the `created:` or `reused:` line as `--record-path`. Run `--match-names` once on that file. Do not start one walk per name.

```text
scripts/prepare_record.py --project-root <dir> --record-path <path> --match-names --names-file <project-relative>
```

The script prints paths, not lines. Do not open the files the script names. Keep the names file for the hash calls below, and delete it after the last helper call of this phase. A leftover dot-prefixed sidecar is a temp. Do not report it as a hit.

### Same-or-different comparison, optional (item 8)

This step waits on permission B. After that permission, one `--hash-names` call per value file compares the hex strings. The value files are the paths `--match-names` printed, or a file the operator names. The record stores fingerprints only. `--hash-name` is a single-name spot check. A missing name or an empty value is `hash: absent`.

```text
scripts/prepare_record.py --project-root <dir> --hash-names --names-file <project-relative> --file <project-relative>
scripts/prepare_record.py --project-root <dir> --hash-name <name> --file <project-relative>
```

Do not pass `--record-path` on these two forms. State the stored-form note and the weak-hash note from Permissions beside this step, outside the permission prompt. Delete the names file after the last of these calls. If permission B is refused, skip hashing and delete the names file after the sweep.

A phase closes only when the operator's sign-off and its evidence are written in the record. Evidence is the name count, whether helpers ran in this run, and the follow-ups opened here. It is not the consumer list.

## Phase 4 — Rotate

Item 7. Prerequisites: confirm and contain are closed. The operator rotates at the provider. This skill records.

The rotate set is the roster plus every distinct non-blank Role on a confirmed row. Take one role in that set at a time. When shared-account notes say two roles share a credential, one operator action covers both, and both log entries say so. Upsert one `### Role:` subsection per role. Do not append a second subsection for the same role.

Record the role, the consumer names, the scope names granted, the verification word the operator supplies, and the time the operator states. No values.

The phase sign-off waits until every role in the rotate set has one log entry or one `Follow-up:` line. A blank Role on a confirmed row blocks that sign-off, as Phase 2 says.

A phase closes only when the operator's sign-off and its evidence are written in the record.

## Phase 5 — Verify

Item 9. For each role in the rotate set that has a log entry, the operator checks that the replacement works and the previous credential does not. Record the operator's result on that log entry, updating it in place. The phase sign-off waits until every such role has a result or one `Follow-up:` line. A mode re-entry may update one role before the phase sign-off.

A phase closes only when the operator's sign-off and its evidence are written in the record.

## Hardening

This section runs when no-argument resume stops on `Sign-off (hardening)`. It does not run inside `close`.

Runtime secret fetch is one identity held by the host, a short-lived token, and any secret the application must not see kept out of the injected environment.

Three leakage checks:

- argument visibility
- debug logging of the injected environment
- a token readable from a parent process

The operator sets the evidence to `adopt`, `defer`, or `not applicable`, plus a one-line reason. The line value is `closed: adopt — <reason>`, or the same shape for `defer` and `not applicable`. `defer` also writes one `Follow-up:` line.

A phase closes only when the operator's sign-off and its evidence are written in the record. The record line is `Sign-off (hardening)`.

## Phase 6 — Close

Entry requires the inventory, contain, audit, rotate, verify, and hardening sign-offs to be closed. Do not require filled disposition cells for entry. `close` does not perform hardening. If hardening is open, stop and name it.

### Disposition for every name, before the close sign-off (item 10)

The operator sets each Disposition cell to one of these five words, compared after stripping whitespace and folding case. Do not fill a Disposition cell before this phase.

- `rotated` — replaced, and the previous credential is no longer accepted.
- `revoked` — previous credential killed, no replacement.
- `dead` — nothing accepts it, nothing to rotate.
- `identifier` — not a secret. Recorded so the sweep is complete.
- `config` — not a secret. Recorded, not rotated.

`Rotated` is `rotated`. `Open` is not one of the five words, so that cell stays unfilled. An empty Disposition cell, or a cell that is not one of those words, blocks the close sign-off and leaves this phase open. It does not block entry.

### Record of the response, written and not filed (item 11)

The record holds one provider-log subsection per role: role, consumers, scopes, time, and verification, with no values. Every role in the rotate set still has one log entry or one `Follow-up:` line. Leftovers are `Follow-up:` or `Blocker:` lines, and a line already present is not appended again. Do not post or file them.

Then the close sign-off. A phase closes only when the operator's sign-off and its evidence are written in the record. After `Sign-off (close)` is closed, this record is closed.

A record closed as not confirmed in Phase 0 is the exception: that close writes no disposition sweep.

## Tool-use notes

- `Read` and `Edit` for the record and for project instructions. Read the record. Do not open a file that holds a value.
- `Bash` (or your host's shell capability) for `scripts/prepare_record.py`.
- No network access, no subagents, no external services.

## Failure modes

- **Unknown token.** Name the seven modes and write nothing.
- **Record path not resolved.** Do not run the script. An operator's answer must not be discarded, and a record must not be created at a path the operator did not choose.
- **Exit 2.** The invocation does not match the usage block. Show the parser message. Write nothing.
- **Exit 1 from preflight.** Show stderr. Do not enter the phase. Do not hand-write a record to bypass the failure.
- **Several open records.** Show the script's list. Do not pick one. Wait for the operator and pass that path as `--choose`.
- **Mode with no open record.** Say the incident is closed, or that no record exists, and stop.
- **Helpers refused.** The operator does inventory and the sweep by hand. Do not open value files to replace the script.
- **Hash file unreadable.** `prepare_record: not a readable file <path>` is a failure. It is not `hash: absent`.
- **Silence.** Not a grant and not a sign-off. The phase stays open.
- **Value offered.** Do not copy it into the record or the conversation. Ask for a name, a role, a disposition word, or a fingerprint the script printed.
- **Second editor.** Do not start one while a run is in progress.
