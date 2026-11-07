#!/usr/bin/env python3
"""Tests for skills/spec-close/scripts/archive_spec.py, plus spec-close SKILL.md pins (VHS-98).

Stdlib unittest. Each case builds a throwaway git repository and runs the
script as a subprocess of sys.executable with cwd at that repository, the way
tests/test_key_rotation_record.py does.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "spec-close" / "scripts" / "archive_spec.py"
SKILL = REPO_ROOT / "skills" / "spec-close" / "SKILL.md"
TODO = Path("docs") / "specs" / "TODO"
DONE = Path("docs") / "specs" / "DONE"


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    # Keep a global excludes file from changing what counts as ignored.
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def git(root, *args):
    proc = subprocess.run(["git"] + list(args), cwd=str(root), env=git_env(),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8")


def init_repo(path):
    git(path, "init", "-q")
    git(path, "symbolic-ref", "HEAD", "refs/heads/main")
    git(path, "config", "user.email", "vhs98@example.invalid")
    git(path, "config", "user.name", "VHS-98 Test")
    git(path, "config", "commit.gpgsign", "false")
    git(path, "config", "core.hooksPath", os.devnull)
    (path / "README.md").write_bytes(b"seed\n")
    git(path, "add", "README.md")
    git(path, "commit", "-q", "--no-verify", "-m", "init")


@unittest.skipUnless(shutil.which("git"), "git not on PATH")
class ArchiveCase(unittest.TestCase):

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="vhs98-"))
        self.addCleanup(shutil.rmtree, str(self.root), True)
        init_repo(self.root)
        (self.root / TODO).mkdir(parents=True)

    def write(self, rel, text="x\n"):
        path = self.root / TODO / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def commit(self, *rels):
        git(self.root, "add", "--", *rels)
        git(self.root, "commit", "-q", "--no-verify", "-m", "add")

    def ignore(self, pattern):
        (self.root / ".gitignore").write_text(pattern + "\n", encoding="utf-8")
        self.commit(".gitignore")

    def run_script(self, *args, cwd=None):
        proc = subprocess.run([sys.executable, str(SCRIPT)] + list(args),
                              cwd=str(cwd or self.root), env=git_env(),
                              stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.returncode, proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8")

    def staged(self):
        return git(self.root, "diff", "--cached", "--name-status")

    def done(self, rel):
        return self.root / DONE / "X-1" / rel


class TestStates(ArchiveCase):

    def test_tracked(self):
        self.write("X-1.spec.md")
        self.commit("docs/specs/TODO/X-1.spec.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.done("spec.md").is_file())
        self.assertIn("- tracked: moved", out)
        self.assertIn("staged: docs/specs/DONE/X-1/spec.md", out)
        self.assertIn("docs/specs/DONE/X-1/spec.md", self.staged())

    def test_tracked_with_untracked_files(self):
        self.write("X-1.reviews/a.md")
        self.commit("docs/specs/TODO/X-1.reviews/a.md")
        self.write("X-1.reviews/b.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertIn("tracked, with untracked files: moved", out)
        staged = self.staged()
        self.assertIn("docs/specs/DONE/X-1/reviews/a.md", staged)
        self.assertIn("docs/specs/DONE/X-1/reviews/b.md", staged)

    def test_tracked_onto_ignored_destination(self):
        self.write("X-1.spec.md")
        self.commit("docs/specs/TODO/X-1.spec.md")
        self.ignore("docs/specs/DONE/")
        # Positive control: the rule really matches the destination.
        git(self.root, "check-ignore", "--no-index", "-q", "--", "docs/specs/DONE/X-1/spec.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.done("spec.md").is_file())
        self.assertIn("docs/specs/DONE/X-1/spec.md", self.staged())

    def test_tracked_with_untracked_onto_ignored_destination(self):
        self.write("X-1.reviews/a.md")
        self.commit("docs/specs/TODO/X-1.reviews/a.md")
        self.write("X-1.reviews/b.md")
        self.ignore("docs/specs/DONE/")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.done("reviews/a.md").is_file())
        self.assertTrue(self.done("reviews/b.md").is_file())
        staged = self.staged()
        self.assertIn("docs/specs/DONE/X-1/reviews/a.md", staged)
        self.assertNotIn("reviews/b.md", staged)
        self.assertNotIn("NOT", out)

    def test_untracked_destination_not_ignored(self):
        self.write("X-1.brief.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertIn("untracked, destination not ignored: moved", out)
        self.assertIn("docs/specs/DONE/X-1/brief.md", self.staged())

    def test_untracked_destination_ignored(self):
        self.ignore("docs/specs/")
        self.write("X-1.spec.md")
        self.write("X-1.reviews/r.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.done("spec.md").is_file())
        self.assertTrue(self.done("reviews/r.md").is_file())
        self.assertIn("untracked, destination ignored: moved (local only)", out)
        self.assertIn("staged: none", out)
        self.assertEqual(self.staged(), "")


class TestSafety(ArchiveCase):

    def test_destination_exists(self):
        self.write("X-1.reviews/a.md")
        self.done("reviews").mkdir(parents=True)
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 1, out)
        self.assertIn("destination exists: skipped", out)
        self.assertTrue((self.root / TODO / "X-1.reviews" / "a.md").is_file())
        self.assertFalse(self.done("reviews/X-1.reviews").exists())
        self.assertFalse(self.done("reviews/a.md").exists())

    def test_rerun_has_nothing_to_archive(self):
        self.write("X-1.spec.md")
        self.assertEqual(self.run_script("X-1")[0], 0)
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertIn("nothing to archive for X-1", out)

    def test_prefix_collision(self):
        self.write("X-1.spec.md")
        self.write("X-11.spec.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue((self.root / TODO / "X-11.spec.md").is_file())
        self.assertFalse((self.root / DONE / "X-11").exists())

    def test_prefix_stripping(self):
        self.write("X-1.test-output.txt")
        self.write("X-1.attempt-1/spec.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.done("test-output.txt").is_file())
        self.assertTrue(self.done("attempt-1/spec.md").is_file())


class TestFolder(ArchiveCase):

    def test_folder_only(self):
        self.write("X-1/a.md")
        self.write("X-1/sub/b.md")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 0, out)
        self.assertTrue(self.done("a.md").is_file())
        self.assertTrue(self.done("sub/b.md").is_file())
        self.assertFalse((self.root / TODO / "X-1").exists())

    def test_folder_and_dotted_clash(self):
        self.write("X-1.spec.md", "dotted\n")
        self.write("X-1/spec.md", "folder\n")
        code, out, _ = self.run_script("X-1")
        self.assertEqual(code, 1, out)
        self.assertEqual(self.done("spec.md").read_text(encoding="utf-8"), "dotted\n")
        self.assertTrue((self.root / TODO / "X-1" / "spec.md").is_file())
        self.assertIn("docs/specs/TODO/X-1/spec.md -> docs/specs/DONE/X-1/spec.md"
                      " - destination exists: skipped", out)


class TestDryRun(ArchiveCase):

    def test_dry_run_changes_nothing(self):
        self.write("X-1.spec.md")
        self.commit("docs/specs/TODO/X-1.spec.md")
        before = git(self.root, "status", "--porcelain", "-uall")
        code, out, _ = self.run_script("X-1", "--dry-run")
        self.assertEqual(code, 0, out)
        self.assertIn("tracked: would move", out)
        self.assertIn("staged: (dry run)", out)
        self.assertEqual(git(self.root, "status", "--porcelain", "-uall"), before)
        self.assertFalse((self.root / DONE).exists())

    def test_dry_run_reports_the_clash(self):
        self.write("X-1.spec.md")
        self.write("X-1/spec.md")
        code, out, _ = self.run_script("X-1", "--dry-run")
        self.assertEqual(code, 1, out)
        self.assertIn("destination exists: would skip", out)
        self.assertTrue((self.root / TODO / "X-1.spec.md").is_file())
        self.assertFalse((self.root / DONE).exists())


class TestUsage(ArchiveCase):

    def test_bad_ticket_and_missing_argument(self):
        for args in (("x-1",), ()):
            with self.subTest(args=args):
                code, _, err = self.run_script(*args)
                self.assertEqual(code, 2)
                self.assertIn("usage:", err)
        self.assertFalse((self.root / DONE).exists())

    def test_outside_a_repo(self):
        outside = Path(tempfile.mkdtemp(prefix="vhs98-out-"))
        self.addCleanup(shutil.rmtree, str(outside), True)
        env = git_env()
        env["GIT_CEILING_DIRECTORIES"] = str(outside.parent)
        proc = subprocess.run([sys.executable, str(SCRIPT), "X-1"], cwd=str(outside), env=env,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("not inside a git work tree", proc.stderr.decode("utf-8"))

    def test_repo_without_docs_specs(self):
        shutil.rmtree(str(self.root / "docs"))
        code, _, err = self.run_script("X-1")
        self.assertEqual(code, 2)
        self.assertIn("no docs/specs/", err)
        self.assertFalse((self.root / "docs").exists())


class TestSkillPins(unittest.TestCase):

    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")

    def test_word_ceiling(self):
        # Target about 2,200 words; this is the tripwire.
        self.assertLessEqual(len(self.text.split()), 2600)

    def test_archive_lives_in_the_script(self):
        self.assertIn("archive_spec.py", self.text)
        self.assertNotIn("git check-ignore", self.text)

    def test_merge_line_lookup_named(self):
        self.assertIn("merge | <PREFIX> — <TICKET-ID> PR #", self.text)


if __name__ == "__main__":
    unittest.main()
