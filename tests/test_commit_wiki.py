#!/usr/bin/env python3
"""Tests for skills/spec-close/scripts/commit_wiki.py (VHS-122).

Stdlib unittest. Cases build a throwaway git repository. The P8 probe runs
the private-index sequence by hand and does not call the script.
"""

import contextlib
import importlib.util
import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def run_git(root, args, env=None, input_bytes=None, check=True):
    proc = subprocess.run(
        ["git", *args], cwd=str(root), env=env if env is not None else git_env(),
        input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise AssertionError("{} in {} failed: exit {} stdout={} stderr={}".format(
            args, root, proc.returncode, proc.stdout, proc.stderr))
    return proc


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "spec-close" / "scripts" / "commit_wiki.py"
PREPEND = REPO_ROOT / "skills" / "spec-close" / "scripts" / "prepend_log_entry.py"
DASH = "\u2014"
HEADER = (
    "# Wiki Log\n"
    "\n"
    "Append-only record of wiki operations. Format: `## [YYYY-MM-DD] action | description`\n"
    "\n"
)


def init_repo(path):
    run_git(path, ["init", "-q"])
    run_git(path, ["symbolic-ref", "HEAD", "refs/heads/main"])
    run_git(path, ["config", "user.email", "vhs122@example.invalid"])
    run_git(path, ["config", "user.name", "VHS-122 Test"])
    run_git(path, ["config", "commit.gpgsign", "false"])


def close_block(date, prefix, ticket, title, body, trailing_blank=True):
    text = "## [{}] close | {} {} {}: {}\n\n{}\n".format(
        date, prefix, DASH, ticket, title, body)
    if trailing_blank:
        text += "\n"
    return text


def merge_block(date, prefix, ticket, number, title, body, trailing_blank=True):
    text = "## [{}] merge | {} {} {} PR #{}: {}\n\n{}\n".format(
        date, prefix, DASH, ticket, number, title, body)
    if trailing_blank:
        text += "\n"
    return text


HEAD_LOG = (
    HEADER
    + merge_block("2026-11-01", "VHS", "VHS-100", 4, "old", "old body")
    + close_block("2026-10-01", "CLT", "CLT-2", "earlier", "earlier body", False)
).encode("utf-8")


@unittest.skipUnless(shutil.which("git"), "git not on PATH")
class TestGitPremiseP8(unittest.TestCase):
    """P8: a private index commit leaves the working tree and real index alone."""

    def test_private_index_commit_leaves_the_working_tree_alone(self):
        root = Path(tempfile.mkdtemp(prefix="vhs122-p8-"))
        self.addCleanup(shutil.rmtree, str(root), True)
        env = git_env()
        init_repo(root)
        (root / "log.md").write_bytes(b"seed\n")
        (root / "notes.md").write_bytes(b"notes\n")
        run_git(root, ["add", "--", "log.md", "notes.md"], env)
        run_git(root, ["commit", "-q", "-m", "init"], env)
        committed = (root / "log.md").read_bytes()
        work = committed + b"ours\ntheirs\n"
        (root / "log.md").write_bytes(work)
        saved = (root / "log.md").read_bytes()
        blob = committed + b"ours\n"

        hashed = run_git(root, ["hash-object", "-w", "--stdin"], env, blob)
        sha = hashed.stdout.decode().strip()
        listed = run_git(root, ["ls-tree", "HEAD", "--", "log.md"], env)
        mode = listed.stdout.decode().split()[0]

        index_dir = Path(tempfile.mkdtemp(prefix="vhs122-p8-index-"))
        self.addCleanup(shutil.rmtree, str(index_dir), True)
        private = dict(env)
        private["GIT_INDEX_FILE"] = str(index_dir / "index")
        run_git(root, ["read-tree", "HEAD"], private)
        run_git(root, ["update-index", "--cacheinfo", "{},{},log.md".format(mode, sha)], private)
        committed_proc = run_git(root, ["commit", "-q", "-m", "probe"], private)
        self.assertEqual(committed_proc.returncode, 0, committed_proc.stderr)

        shown = run_git(root, ["show", "HEAD:log.md"], env)
        self.assertIn(b"ours", shown.stdout)
        self.assertNotIn(b"theirs", shown.stdout)
        self.assertEqual((root / "log.md").read_bytes(), saved)

        listed_z = run_git(root, ["ls-tree", "-z", "HEAD", "--", "log.md"], env)
        refreshed = run_git(
            root, ["update-index", "-z", "--index-info"], env, listed_z.stdout)
        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)

        cached = run_git(root, ["diff", "--cached", "--quiet"], env, check=False)
        self.assertEqual(
            cached.returncode, 0,
            "stdout={} stderr={}".format(cached.stdout, cached.stderr))
        status = run_git(root, ["status", "--porcelain"], env)
        self.assertEqual(status.stdout.replace(b"\r\n", b"\n"), b" M log.md\n")


@unittest.skipUnless(shutil.which("git"), "git not on PATH")
class TestCommitWiki(unittest.TestCase):

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="vhs122-wiki-"))
        self.addCleanup(shutil.rmtree, str(self.root), True)
        init_repo(self.root)
        (self.root / "log.md").write_bytes(HEAD_LOG)
        (self.root / "projects" / "p").mkdir(parents=True)
        (self.root / "projects" / "p" / "state.md").write_bytes(b"# State\n")
        (self.root / "notes.md").write_bytes(b"notes\n")
        run_git(self.root, ["add", "--", "log.md", "projects/p/state.md", "notes.md"])
        run_git(self.root, ["commit", "-q", "-m", "seed"])

    def run_script(self, *args, root=None):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(root or self.root), *args],
            env=git_env(), stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.stdout.decode("utf-8")
        err = proc.stderr.decode("utf-8")
        return proc.returncode, out, err

    def show_log(self):
        return run_git(self.root, ["show", "HEAD:log.md"]).stdout

    def head(self):
        return run_git(self.root, ["rev-parse", "HEAD"]).stdout.decode().strip()

    def test_commits_only_this_tickets_entries(self):
        work = (
            HEADER
            + close_block("2026-11-22", "CLT", "CLT-9", "other", "other body")
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + merge_block("2026-11-21", "VHS", "VHS-122", 9, "landed", "merge body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log()
        close_at = shown.find("VHS-122: harvest".encode())
        merge_at = shown.find("VHS-122 PR #9".encode())
        self.assertGreaterEqual(close_at, 0)
        self.assertGreater(merge_at, close_at)
        self.assertNotIn(b"CLT-9", shown)
        self.assertEqual((self.root / "log.md").read_bytes(), work)
        self.assertEqual(run_git(self.root, ["diff", "--cached", "--quiet"], check=False).returncode, 0)
        status = run_git(self.root, ["status", "--porcelain"]).stdout.replace(b"\r\n", b"\n")
        self.assertEqual(status, b" M log.md\n")
        self.assertIn("log.md (2 entries)", out)
        self.assertEqual(len([line for line in out.splitlines() if line.startswith("wiki commit:")]), 1)

    def test_staged_bytes_equal_git_add(self):
        (self.root / ".gitattributes").write_bytes(b"* text=auto eol=lf\n")
        run_git(self.root, ["add", "--", ".gitattributes"])
        run_git(self.root, ["commit", "-q", "-m", "attrs"])
        run_git(self.root, ["config", "core.autocrlf", "true"])
        entry = "## [2026-11-22] close | VHS \u2014 VHS-122: harvest\n\nclose body"
        proc = subprocess.run(
            [sys.executable, str(PREPEND), str(self.root / "log.md"),
             "--guard", "close | VHS \u2014 VHS-122:"],
            input=entry.encode("utf-8"), env=git_env(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8"))
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        status = run_git(self.root, ["status", "--porcelain"]).stdout
        self.assertEqual(status, b"", out + err + status.decode("utf-8", "replace"))

    def test_crlf_working_tree(self):
        run_git(self.root, ["config", "core.autocrlf", "true"])
        work = (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).replace("\n", "\r\n").encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        status = run_git(self.root, ["status", "--porcelain"]).stdout
        self.assertEqual(status, b"", out + err)
        blob = run_git(self.root, ["cat-file", "blob", "HEAD:log.md"]).stdout
        self.assertNotIn(b"\r", blob)

    def test_named_files_are_committed_whole(self):
        (self.root / "projects" / "p" / "state.md").write_bytes(b"# State\nchanged\n")
        (self.root / "decisions").mkdir()
        (self.root / "decisions" / "new.md").write_bytes(b"new\n")
        (self.root / "notes.md").write_bytes(b"notes changed\n")
        code, out, err = self.run_script(
            "--ticket", "VHS-122", "--file", "projects/p/state.md", "--file", "decisions/new.md")
        self.assertEqual(code, 0, out + err)
        names = run_git(self.root, ["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"])
        committed = names.stdout.decode().splitlines()
        self.assertIn("projects/p/state.md", committed)
        self.assertIn("decisions/new.md", committed)
        self.assertNotIn("notes.md", committed)
        status = run_git(self.root, ["status", "--porcelain"]).stdout.decode()
        self.assertIn("notes.md", status)
        self.assertNotIn("state.md", status)
        self.assertNotIn("new.md", status)

    def test_other_sessions_staged_file_is_left_alone(self):
        (self.root / "extra.md").write_bytes(b"extra\n")
        run_git(self.root, ["add", "--", "extra.md"])
        work = (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        before = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        self.assertNotEqual(self.head(), before)
        names = run_git(
            self.root, ["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"]).stdout.decode()
        self.assertNotIn("extra.md", names)
        cached = run_git(self.root, ["diff", "--cached", "--name-only"]).stdout.decode().splitlines()
        self.assertIn("extra.md", cached)

    def test_own_path_already_staged_skips(self):
        (self.root / "log.md").write_bytes(HEAD_LOG + b"\nstaged\n")
        run_git(self.root, ["add", "--", "log.md"])
        index = run_git(self.root, ["write-tree"]).stdout
        before = self.head()
        code, out, err = self.run_script(
            "--ticket", "VHS-122", "--file", "projects/p/state.md")
        self.assertEqual(code, 1, out + err)
        self.assertIn("wiki commit: not made - already staged in the wiki: log.md", out)
        self.assertEqual(self.head(), before)
        self.assertEqual(run_git(self.root, ["write-tree"]).stdout, index)
        self.assertIn("--ticket VHS-122", out)
        self.assertIn("--file \"projects/p/state.md\"", out.replace("\\", "/"))

    def test_hook_rejection_leaves_nothing_behind(self):
        hooks = self.root / "hooks"
        hooks.mkdir()
        hook = hooks / "pre-commit"
        hook.write_bytes(b"#!/bin/sh\nprintf ran > hook-ran\nexit 1\n")
        os.chmod(str(hook), stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
        run_git(self.root, ["config", "core.hooksPath", str(hooks)])
        (self.root / "probe.txt").write_bytes(b"probe\n")
        run_git(self.root, ["add", "--", "probe.txt"])
        probe = run_git(self.root, ["commit", "-q", "-m", "probe"], check=False)
        if probe.returncode == 0 or not (self.root / "hook-ran").exists():
            self.skipTest("platform did not run the sh hook")
        run_git(self.root, ["reset", "-q", "HEAD", "--", "probe.txt"])
        (self.root / "probe.txt").unlink()
        (self.root / "hook-ran").unlink()
        work = (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        saved = (self.root / "log.md").read_bytes()
        before = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn("wiki commit: not made - ", out)
        self.assertEqual(self.head(), before)
        self.assertEqual(run_git(self.root, ["diff", "--cached", "--quiet"], check=False).returncode, 0)
        self.assertEqual((self.root / "log.md").read_bytes(), saved)
        self.assertIn("To retry:", out)

    def test_ticket_1_does_not_take_ticket_11(self):
        work = (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-1", "one", "one body")
            + close_block("2026-11-22", "VHS", "VHS-11", "eleven", "eleven body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-1")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log()
        self.assertIn("VHS-1: one".encode(), shown)
        self.assertNotIn(b"VHS-11", shown)
        self.assertIn(b"VHS-11", (self.root / "log.md").read_bytes())

    def test_older_entry_keeps_its_place(self):
        newer = merge_block("2026-12-01", "VHS", "VHS-200", 8, "newer", "newer body")
        ticket = merge_block("2026-11-20", "VHS", "VHS-122", 9, "landed", "merge body")
        older = close_block("2026-10-01", "CLT", "CLT-2", "earlier", "earlier body", False)
        (self.root / "log.md").write_bytes((HEADER + newer + older).encode("utf-8"))
        run_git(self.root, ["add", "--", "log.md"])
        run_git(self.root, ["commit", "-q", "-m", "newer anchor"])
        (self.root / "log.md").write_bytes((HEADER + newer + ticket + older).encode("utf-8"))
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log().decode("utf-8")
        newer_at = shown.find("VHS-200")
        ticket_at = shown.find("VHS-122 PR #9")
        older_at = shown.find("CLT-2")
        self.assertGreaterEqual(newer_at, 0)
        self.assertGreaterEqual(ticket_at, 0)
        self.assertGreaterEqual(older_at, 0)
        self.assertLess(newer_at, ticket_at)
        self.assertLess(ticket_at, older_at)

    def test_second_run_has_nothing_to_commit(self):
        work = (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        after = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        self.assertIn("wiki commit: nothing to commit", out)
        self.assertEqual(self.head(), after)

    def test_not_a_repository_and_detached_head(self):
        empty = Path(tempfile.mkdtemp(prefix="vhs122-not-a-repo-"))
        self.addCleanup(shutil.rmtree, str(empty), True)
        code, out, err = self.run_script("--ticket", "VHS-122", root=empty)
        self.assertEqual(code, 1, out + err)
        self.assertIn("wiki commit: not made - ", out)
        self.assertEqual(os.listdir(str(empty)), [])
        saved = (self.root / "log.md").read_bytes()
        run_git(self.root, ["checkout", "--detach"])
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn("wiki commit: not made - ", out)
        self.assertEqual((self.root / "log.md").read_bytes(), saved)

    def test_file_log_md_is_ignored(self):
        work = (
            HEADER
            + close_block("2026-11-22", "CLT", "CLT-9", "other", "other body")
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-122", "--file", "log.md")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log()
        self.assertNotIn(b"CLT-9", shown)
        self.assertIn(b"VHS-122", shown)

    def test_edit_to_an_old_entry_stays_out(self):
        old = HEAD_LOG.decode("utf-8")
        edited = old.replace("old body", "tampered body")
        work = (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + edited[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log()
        self.assertIn(b"old body", shown)
        self.assertNotIn(b"tampered body", shown)

    def test_bad_ticket_is_a_usage_error(self):
        code, out, err = self.run_script("--ticket", "vhs-1")
        self.assertEqual(code, 2, out + err)
        self.assertNotIn("wiki commit:", out)
        self.assertNotIn("wiki commit:", err)

    def test_merge_in_progress_is_not_made(self):
        run_git(self.root, ["checkout", "-b", "other"])
        (self.root / "notes.md").write_bytes(b"other\n")
        run_git(self.root, ["add", "--", "notes.md"])
        run_git(self.root, ["commit", "-q", "-m", "other"])
        run_git(self.root, ["checkout", "main"])
        (self.root / "notes.md").write_bytes(b"main side\n")
        run_git(self.root, ["add", "--", "notes.md"])
        run_git(self.root, ["commit", "-q", "-m", "main side"])
        merged = run_git(self.root, ["merge", "other"], check=False)
        self.assertNotEqual(merged.returncode, 0, merged.stderr)
        before = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn(
            "wiki commit: not made - the wiki has a merge, cherry-pick or revert in progress", out)
        self.assertEqual(self.head(), before)
        self.assertEqual(run_git(self.root, ["rev-parse", "-q", "--verify", "MERGE_HEAD"]).returncode, 0)

    def _our_log(self):
        return (
            HEADER
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")

    def _load(self):
        name = "commit_wiki_under_test"
        sys.modules.pop(name, None)
        spec = importlib.util.spec_from_file_location(name, SCRIPT)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    def _call(self, module, fn):
        with mock.patch.dict(os.environ, git_env(), clear=True):
            return fn()

    def _require_hook(self):
        hooks = self.root / "hooks"
        hooks.mkdir(exist_ok=True)
        hook = hooks / "pre-commit"
        hook.write_bytes(b"#!/bin/sh\nprintf ran > hook-ran\nexit 0\n")
        os.chmod(str(hook), stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
        run_git(self.root, ["config", "core.hooksPath", str(hooks)])
        marker = self.root / "hook-ran"
        if marker.exists():
            marker.unlink()
        proc = run_git(self.root, ["hook", "run", "--ignore-missing", "pre-commit"], check=False)
        if proc.returncode != 0 or not marker.exists():
            self.skipTest("platform did not run the sh hook")
        marker.unlink()
        return hook

    def test_peer_commit_between_build_and_update_is_not_published(self):
        module = self._load()
        (self.root / "log.md").write_bytes(self._our_log())
        candidate = self._call(module, lambda: module._build(str(self.root), "VHS-122", []))
        self.assertIsNotNone(candidate)
        (self.root / "notes.md").write_bytes(b"peer\n")
        run_git(self.root, ["add", "--", "notes.md"])
        run_git(self.root, ["commit", "-q", "-m", "peer"])
        peer = self.head()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                code = self._call(module, lambda: module._publish(str(self.root), "VHS-122", candidate))
            except module.NotMade as exc:
                code = 1
                module._not_made(str(self.root), "VHS-122", [], exc.reason)
        text = out.getvalue()
        self.assertEqual(code, 1, text)
        self.assertIn("not made", text)
        self.assertEqual(self.head(), peer)
        self.assertEqual(run_git(self.root, ["show", "HEAD:notes.md"]).stdout, b"peer\n")
        self.assertNotIn(b"VHS-122: harvest", run_git(self.root, ["show", "HEAD:log.md"]).stdout)

    def test_refresh_leaves_a_path_staged_after_the_check(self):
        hook = self._require_hook()
        hook.write_bytes(
            b"#!/bin/sh\nunset GIT_INDEX_FILE\nprintf 'PEER STAGED\\n' >> log.md\n"
            b"git add -- log.md\nexit 0\n")
        (self.root / "log.md").write_bytes(self._our_log())
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn("index not refreshed for log.md", out)
        self.assertNotIn("not made", out)
        self.assertIn(b"PEER STAGED", run_git(self.root, ["show", ":log.md"]).stdout)
        self.assertNotIn(b"PEER STAGED", self.show_log())

    def test_hook_cannot_replace_the_composed_log(self):
        hook = self._require_hook()
        hook.write_bytes(b"#!/bin/sh\ngit add -- log.md\nexit 0\n")
        work = (
            HEADER
            + close_block("2026-11-22", "CLT", "CLT-9", "other", "other body")
            + close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
            + HEAD_LOG.decode("utf-8")[len(HEADER):]
        ).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        before = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn("unexpected path: log.md", out)
        self.assertEqual(self.head(), before)
        self.assertNotIn(b"CLT-9", self.show_log())

    def test_directory_replaced_by_a_file_is_refused(self):
        state = self.root / "projects" / "p" / "state.md"
        state.unlink()
        (self.root / "projects" / "p").rmdir()
        (self.root / "projects" / "p").write_bytes(b"now a file\n")
        before = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122", "--file", "projects/p")
        self.assertEqual(code, 1, out + err)
        self.assertIn("unexpected path: projects/p/state.md", out)
        self.assertEqual(self.head(), before)

    def test_ticket_match_uses_heading_fields_not_the_title(self):
        quoted = close_block(
            "2026-11-22", "CLT", "CLT-9",
            "] close | VHS \u2014 VHS-122: quoted", "other body")
        ours = close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body")
        work = (HEADER + quoted + ours + HEAD_LOG.decode("utf-8")[len(HEADER):]).encode("utf-8")
        (self.root / "log.md").write_bytes(work)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log()
        needle = "close | VHS {} VHS-122:".format(DASH).encode("utf-8")
        self.assertIn(b"VHS-122: harvest", shown)
        self.assertNotIn(b"CLT-9", shown)
        self.assertEqual(shown.count(needle), 1)
        retitled = close_block("2026-11-23", "VHS", "VHS-122", "renamed", "close body")
        (self.root / "log.md").write_bytes(
            (HEADER + retitled + HEAD_LOG.decode("utf-8")[len(HEADER):]).encode("utf-8"))
        after = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        self.assertIn("nothing to commit", out)
        self.assertEqual(self.head(), after)
        self.assertEqual(self.show_log().count(needle), 1)

    def test_unmerged_index_or_sequencer_is_not_made(self):
        (self.root / "log.md").write_bytes(self._our_log())
        before = self.head()
        git_dir = Path(run_git(
            self.root, ["rev-parse", "--absolute-git-dir"]).stdout.decode().strip())
        sequencer = git_dir / "sequencer"
        sequencer.mkdir()
        try:
            code, out, err = self.run_script("--ticket", "VHS-122")
        finally:
            sequencer.rmdir()
        self.assertEqual(code, 1, out + err)
        self.assertIn("sequencer or rebase", out)
        self.assertEqual(self.head(), before)
        sha = run_git(
            self.root, ["hash-object", "-w", "--stdin"], input_bytes=b"side\n").stdout.decode().strip()
        info = "100644 {0} 1\tnotes.md\n100644 {0} 2\tnotes.md\n100644 {0} 3\tnotes.md\n".format(sha)
        run_git(self.root, ["update-index", "--index-info"], input_bytes=info.encode("utf-8"))
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn("unmerged entries", out)
        self.assertEqual(self.head(), before)

    def test_symlink_log_is_not_committed(self):
        outside = Path(tempfile.mkdtemp(prefix="vhs122-log-link-"))
        self.addCleanup(shutil.rmtree, str(outside), True)
        target = outside / "elsewhere.md"
        target.write_bytes(self._our_log())
        log_path = self.root / "log.md"
        log_path.unlink()
        try:
            os.symlink(str(target), str(log_path))
        except OSError as exc:
            self.skipTest("platform refuses symbolic links: {}".format(exc))
        before = self.head()
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 1, out + err)
        self.assertIn("not a regular file", out)
        self.assertEqual(self.head(), before)
        self.assertNotIn(b"close body", self.show_log())

    def test_new_log_is_committed_from_an_empty_base(self):
        run_git(self.root, ["rm", "-q", "--", "log.md"])
        run_git(self.root, ["commit", "-q", "-m", "drop log"])
        (self.root / "log.md").write_bytes(self._our_log())
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        self.assertNotIn("nothing to commit", out)
        self.assertIn(b"VHS-122: harvest", self.show_log())

    def test_bom_stays_a_prefix_and_an_empty_log_has_no_leading_blank(self):
        (self.root / "log.md").write_bytes(b"")
        run_git(self.root, ["add", "--", "log.md"])
        run_git(self.root, ["commit", "-q", "-m", "empty log"])
        entry = close_block("2026-11-22", "VHS", "VHS-122", "harvest", "close body").encode("utf-8")
        (self.root / "log.md").write_bytes(entry)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        blob = self.show_log()
        self.assertTrue(blob.startswith(b"## ["), blob[:20])
        old = b"## [2026-11-01] merge | VHS \u2014 VHS-100 PR #4: old\n\nold body\n"
        (self.root / "log.md").write_bytes(b"\xef\xbb\xbf" + old)
        run_git(self.root, ["add", "--", "log.md"])
        run_git(self.root, ["commit", "-q", "-m", "bom log"])
        (self.root / "log.md").write_bytes(b"\xef\xbb\xbf" + entry + old)
        code, out, err = self.run_script("--ticket", "VHS-122")
        self.assertEqual(code, 0, out + err)
        shown = self.show_log()
        self.assertTrue(shown.startswith(b"\xef\xbb\xbf## [2026-11-22]"), shown[:40])
        self.assertEqual(shown.count(b"\xef\xbb\xbf"), 1)
        self.assertLess(shown.find(b"VHS-122"), shown.find(b"VHS-100"))

    def test_literal_pathspec_does_not_match_a_different_staged_file(self):
        (self.root / "abcp.md").write_bytes(b"abcp\n")
        run_git(self.root, ["add", "--", "abcp.md"])
        run_git(self.root, ["commit", "-q", "-m", "abcp"])
        (self.root / "abcp.md").write_bytes(b"abcp changed\n")
        run_git(self.root, ["add", "--", "abcp.md"])
        bracket = self.root / "abc[p].md"
        bracket.write_bytes(b"bracket\n")
        code, out, err = self.run_script("--ticket", "VHS-122", "--file", "abc[p].md")
        self.assertEqual(code, 0, out + err)
        names = run_git(
            self.root, ["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"]).stdout.decode()
        self.assertIn("abc[p].md", names.splitlines())
        self.assertNotIn("abcp.md", names.splitlines())
        cached = run_git(self.root, ["diff", "--cached", "--name-only"]).stdout.decode().splitlines()
        self.assertIn("abcp.md", cached)

    def test_recovery_command_quotes_each_path(self):
        spaced = self.root / "release notes.md"
        spaced.write_bytes(b"v1\n")
        run_git(self.root, ["add", "--", "release notes.md"])
        run_git(self.root, ["commit", "-q", "-m", "spaced"])
        spaced.write_bytes(b"v2\n")
        module = self._load()
        original = module._git

        def wrapped(root, args, env, input_bytes=None):
            if args[:2] == ["update-index", "-z"] and "GIT_INDEX_FILE" not in env:
                return subprocess.CompletedProcess(args, 1, b"", b"refresh failed")
            return original(root, args, env, input_bytes)

        module._git = wrapped
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                    mock.patch.dict(os.environ, git_env(), clear=True):
                code = module.main([str(self.root), "--ticket", "VHS-122", "--file", "release notes.md"])
        finally:
            module._git = original
        text = out.getvalue()
        self.assertEqual(code, 1, text + err.getvalue())
        self.assertIn("made", text)
        self.assertNotIn("not made", text)
        self.assertIn('":(literal)release notes.md"', text.replace("\\", "/"))
        self.assertIn("release notes.md", run_git(
            self.root, ["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"]).stdout.decode())

    def test_short_hash_failure_still_reports_the_commit(self):
        module = self._load()
        (self.root / "log.md").write_bytes(self._our_log())
        before = self.head()
        original = module._git

        def wrapped(root, args, env, input_bytes=None):
            if args[:2] == ["rev-parse", "--short"]:
                return subprocess.CompletedProcess(args, 1, b"", b"short failed")
            return original(root, args, env, input_bytes)

        module._git = wrapped
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                    mock.patch.dict(os.environ, git_env(), clear=True):
                code = module.main([str(self.root), "--ticket", "VHS-122"])
        finally:
            module._git = original
        text = out.getvalue()
        head = self.head()
        self.assertNotEqual(head, before)
        self.assertEqual(code, 1, text + err.getvalue())
        self.assertIn(head, text)
        self.assertIn("made", text)
        self.assertNotIn("not made", text)


if __name__ == "__main__":
    unittest.main()
