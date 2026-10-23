# Review gate: VHS-75

- Command: /ponytail-review
- Mode: subagent
- Compared against: origin/main
- Result: ran
- Blocks: 1 (1 fixed, 0 fixed by operator, 0 overridden, 0 unresolved)
- Fix or record: 2 (2 fixed, 0 recorded)
- Record only: 2

## Findings

1. [Blocks] `--hash-names` and `--hash-name` echo whatever they are given as a name, including a whole `KEY=value` line — `skills/key-rotation/scripts/prepare_record.py` `names_from_bytes`, `write_hash_lines`, `reject_readonly_usage`
   Problem: the names file was filtered only to non-blank ASCII lines and never checked against the name grammar every other mode enforces. Swapping the two project-relative flags (`--names-file .env --file names.txt`) printed every line of the value file on stdout as `<line> hash: absent`, exit 0. Reproduced by the reviewer. `--hash-name 'X=not_a_name'` echoed the same way.
   Disposition: fixed — added `is_name_text` (grammar plus `MAX_NAME_BYTES`), `names_from_bytes` keeps only grammar-valid lines after trimming spaces and tabs, `--hash-name` with a non-name is a parser usage error (exit 2, argument not echoed). New test `test_09_hash_names_non_name_lines_never_echo` covers the swapped-flag case, a mixed names file, and the bad `--hash-name`.
2. [Fix or record] `--match-names` slurps every text file in the project into memory and builds a per-file set of every identifier — `prepare_record.py` `read_regular_text`, `run_match_names`
   Problem: one large text artifact in the tree (CSV, SQL dump, log) means one giant bytes object plus a set of up to hundreds of millions of runs; a MemoryError surfaces as the misleading `prepare_record: write failed`. The spec describes streaming.
   Disposition: fixed — new `match_file` streams line by line after the 8192-byte NUL probe, intersects each line's identifier runs with the requested set, and stops early once every name has hit. Hit order per file is unchanged (names-file order). `read_regular_text` stays for the env-file modes, which read small files.
3. [Fix or record] Four redundant git calls when the ignore rule is already right — `prepare_record.py` `ensure_ignore`
   Problem: when both ignore checks passed, `recheck_ignore` ran the same two checks again before returning. Nothing changed between the rounds.
   Disposition: fixed — removed the redundant call on the satisfied path. The two meaningful rechecks (after the `.gitignore` publish, and before the record replace) stay.
4. [Record only] Rollback after a failed repair leaves an empty `.gitignore` when none existed before — `prepare_record.py` `rollback_gitignore`
   Problem: when the script created `.gitignore` from scratch and the post-publish recheck still failed, writing the previous bytes back wrote `b""`, leaving a zero-byte file the project did not have.
   Disposition: not acted on — harmless to git, rare failure path; a follow-up can unlink instead of publishing empty bytes.
5. [Record only] Two simultaneous creates can land on the same stem — `prepare_record.py` `remove_zero_byte_target`, `finish_create`
   Problem: between process A's exclusive create and its `os.replace`, process B can treat A's zero-byte target as a crash leftover, unlink it, and create its own. Both print the same `created:` line with identical blank content. The spec's step 11 claim that the loser skips to the next stem does not hold in that window.
   Disposition: not acted on — does not occur at the stated load (one operator; SKILL.md forbids a second concurrent editor). Spec step 11 text overstates the guarantee; noted for /spec-close reconciliation.

## Also checked, clean

Every stdout and stderr line SKILL.md quotes exists in the script with the same text and argument shape; `--status` and the read-only modes never call a writer; the only `os.replace` onto a record target is onto a file this process created exclusively; no traceback can reach stdout; frontmatter matches the spec's pinned block; no provider, company, person, project, or ticket is named in the skill, template, or customizing example; Python 3.8 syntax verified with `ast.parse(feature_version=(3, 8))` (no 3.8 interpreter on this host). The three POSIX-only tests skip on Windows.
