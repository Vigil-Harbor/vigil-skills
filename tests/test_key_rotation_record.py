#!/usr/bin/env python3
"""Record lifecycle tests for skills/key-rotation/scripts/prepare_record.py.

Stdlib unittest. Builds a temporary git repository the way the session-handoff
tests do, and runs the script as a subprocess of sys.executable the way the
spec-close tests do. Rows 9, 12, and 16 belong to later tickets.
"""

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "key-rotation" / "scripts" / "prepare_record.py"
TEMPLATE = REPO_ROOT / "skills" / "key-rotation" / "reference" / "record-template.md"


def _skip_unreadable():
    """POSIX-only case. Skip on Windows and when root can read mode 000."""
    if os.name != "posix":
        return True
    geteuid = getattr(os, "geteuid", None)
    if geteuid is None:
        return True
    return geteuid() == 0


def git_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root, *args, check=False):
    proc = subprocess.run(
        ["git"] + list(args),
        cwd=str(root),
        env=git_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    return proc


def init_repo(path):
    """A one-commit repository, with signing and hooks kept out of the way."""
    git(path, "init", "-q", check=True)
    git(path, "symbolic-ref", "HEAD", "refs/heads/main", check=True)
    git(path, "config", "user.email", "vhs75@example.invalid", check=True)
    git(path, "config", "user.name", "VHS-75 Test", check=True)
    git(path, "config", "commit.gpgsign", "false", check=True)
    (path / "README.md").write_bytes(b"seed\n")
    git(path, "add", "README.md", check=True)
    git(path, "commit", "-q", "--no-verify", "-m", "init", check=True)


def run(root, args):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--project-root", str(root)] + list(args),
        cwd=str(root),
        env=git_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8"),
        proc.stderr.decode("utf-8"),
    )


def today():
    return date.today().isoformat()


def expected_record(day):
    data = TEMPLATE.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data.replace(b"{{date}}", day.encode("ascii"))


def path_from(prefix, out):
    line = out.splitlines()[0]
    if not line.startswith(prefix):
        raise AssertionError(out)
    return line[len(prefix):]


def norm(path):
    return os.path.normcase(os.path.realpath(os.path.abspath(str(path))))


def rel_posix(root, path):
    rel = os.path.relpath(str(path), str(root))
    return Path(rel).as_posix()


def snapshot(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(str(root)):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), str(root))
            found.append(Path(rel).as_posix())
    return sorted(found)


class TestKeyRotationRecord(unittest.TestCase):
    maxDiff = None

    def make_repo(self):
        directory = tempfile.mkdtemp(prefix="vhs77-")
        self.addCleanup(shutil.rmtree, directory, True)
        root = Path(directory)
        init_repo(root)
        return root

    def test_01_create(self):
        root = self.make_repo()
        day = today()
        code, out, err = run(root, [])
        self.assertEqual(code, 0, err)
        self.assertEqual(out.splitlines()[0][:9], "created: ")
        created = Path(path_from("created: ", out))
        self.assertEqual(created.read_bytes(), expected_record(day))
        self.assertNotIn(b"\r", created.read_bytes())
        self.assertIn(day, created.name)
        self.assertEqual(git(root, "check-ignore", "-q", "--", ".key-rotation/").returncode, 0)
        self.assertEqual(
            git(root, "check-ignore", "-q", "--", rel_posix(root, created)).returncode,
            0,
        )
        lines = (root / ".gitignore").read_bytes().splitlines()
        self.assertEqual([line for line in lines if line == b".key-rotation/"], [b".key-rotation/"])

    def test_02_date_token(self):
        day = today()
        root = self.make_repo()
        code, out, err = run(root, ["--record-path", ".key-rotation/record-YYYY-MM-DD.md"])
        self.assertEqual(code, 0, err)
        created = Path(path_from("created: ", out))
        self.assertIn(day, created.name)
        self.assertNotIn("YYYY-MM-DD", created.name)
        self.assertEqual(created.parent.name, ".key-rotation")

        other = self.make_repo()
        code, out, err = run(other, ["--record-path", "kept/record-YYYY-MM-DD.md"])
        self.assertEqual(code, 0, err)
        created = Path(path_from("created: ", out))
        self.assertEqual(created.parent.name, "kept")
        self.assertIn(day, created.name)
        self.assertNotIn("YYYY-MM-DD", created.name)
        self.assertNotIn("YYYY-MM-DD", str(created.parent))

    def test_03_reuse(self):
        for value in (b"open", b"Open"):
            with self.subTest(value=value):
                root = self.make_repo()
                record = root / ".key-rotation" / "incident.md"
                record.parent.mkdir()
                body = b"Sign-off (close): " + value + b"\nMARKER-REUSE\n"
                record.write_bytes(body)
                code, out, err = run(root, [])
                self.assertEqual(code, 0, err)
                self.assertTrue(out.startswith("reused: "), out)
                self.assertEqual(norm(path_from("reused: ", out)), norm(record))
                self.assertEqual(record.read_bytes(), body)

    def test_04_ignore_repair(self):
        day_bodies = {
            "negated": b".key-rotation/\n!.key-rotation/\n",
            "whitelist": b"*\n!*/\n!*.md\n",
        }
        for name, seeded in day_bodies.items():
            with self.subTest(fixture=name):
                root = self.make_repo()
                record = root / ".key-rotation" / "open-record.md"
                record.parent.mkdir()
                body = b"Sign-off (close): open\nMARKER-REPAIR\n"
                record.write_bytes(body)
                (root / ".gitignore").write_bytes(seeded)
                file_rel = rel_posix(root, record)
                self.assertEqual(git(root, "check-ignore", "-q", "--", file_rel).returncode, 1)
                if name == "whitelist":
                    for operand in (".key-rotation/", file_rel):
                        quiet = git(root, "check-ignore", "-q", "--", operand)
                        verbose = git(root, "check-ignore", "-v", "--", operand)
                        self.assertEqual(quiet.returncode, 1, operand)
                        self.assertEqual(verbose.returncode, 0, verbose.stderr)
                        self.assertIn(b"!", verbose.stdout)
                before = record.read_bytes()
                code, out, err = run(root, [])
                self.assertEqual(code, 0, err)
                self.assertTrue(out.startswith("reused: "), err)
                self.assertEqual(git(root, "check-ignore", "-q", "--", ".key-rotation/").returncode, 0)
                self.assertEqual(git(root, "check-ignore", "-q", "--", file_rel).returncode, 0)
                after = (root / ".gitignore").read_bytes()
                self.assertTrue(after.startswith(seeded), after)
                self.assertEqual(after.splitlines()[-1], b".key-rotation/")
                dry = git(root, "add", "-A", "--dry-run")
                self.assertEqual(dry.returncode, 0, dry.stderr)
                self.assertNotIn("open-record.md", dry.stdout.decode("utf-8", "replace"))
                self.assertEqual(record.read_bytes(), before)

    def test_05_halt(self):
        root = self.make_repo()
        outside = Path(tempfile.mkdtemp(prefix="vhs77-out-"))
        self.addCleanup(shutil.rmtree, outside, True)
        outside_file = outside / "record.md"
        code, _out, err = run(root, ["--record-path", str(outside_file)])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: path is outside the project", err)
        self.assertFalse(outside_file.exists())
        self.assertFalse((root / ".key-rotation").exists())

        dirty = self.make_repo()
        parent = dirty / ".key-rotation"
        parent.mkdir()
        (parent / "notes.txt").write_bytes(b"not a record\n")
        code, _out, err = run(dirty, [])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: parent is not a record directory", err)
        self.assertFalse((dirty / ".gitignore").exists())
        self.assertEqual(list(parent.glob("*.md")), [])

        plain = Path(tempfile.mkdtemp(prefix="vhs77-plain-"))
        self.addCleanup(shutil.rmtree, plain, True)
        (plain / ".gitignore").write_bytes(b"keep\n")
        code, _out, err = run(plain, [])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: not a git work tree", err)
        self.assertEqual((plain / ".gitignore").read_bytes(), b"keep\n")

        tracked = self.make_repo()
        record = tracked / ".key-rotation" / "tracked.md"
        record.parent.mkdir()
        body = b"Sign-off (close): open\nMARKER-TRACKED\n"
        record.write_bytes(body)
        git(tracked, "add", "-f", "--", rel_posix(tracked, record), check=True)
        git(tracked, "commit", "-q", "--no-verify", "-m", "track", check=True)
        code, _out, err = run(tracked, [])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: record is tracked", err)
        self.assertEqual(record.read_bytes(), body)

        missing = self.make_repo()
        code, _out, err = run(missing, ["--template", str(missing / "no-such-template.md")])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: template missing", err)
        self.assertFalse((missing / ".key-rotation").exists())
        self.assertEqual([path for path in missing.rglob("*.md") if ".git" not in path.parts], [missing / "README.md"])

    def test_06_two_open_records(self):
        root = self.make_repo()
        first = root / ".key-rotation" / "a.md"
        second = root / ".key-rotation" / "b.md"
        first.parent.mkdir()
        body_a = b"Sign-off (close): open\nA\n"
        body_b = b"Sign-off (close): open\nB\n"
        first.write_bytes(body_a)
        second.write_bytes(body_b)
        expected = sorted([rel_posix(root, first), rel_posix(root, second)])
        for args in ([], ["--record-path", "other/record.md"]):
            with self.subTest(args=args):
                code, _out, err = run(root, args)
                self.assertEqual(code, 1, err)
                lines = err.splitlines()
                self.assertEqual(lines[0], "prepare_record: multiple open records")
                self.assertEqual(sorted(lines[1:]), expected)
                self.assertEqual(first.read_bytes(), body_a)
                self.assertEqual(second.read_bytes(), body_b)
        self.assertFalse((root / "other").exists())

    def test_07_second_record_and_choose(self):
        root = self.make_repo()
        code, out, err = run(root, [])
        self.assertEqual(code, 0, err)
        first = Path(path_from("created: ", out))
        first_bytes = first.read_bytes()
        code, out, err = run(root, ["--new"])
        self.assertEqual(code, 0, err)
        second = Path(path_from("created: ", out))
        self.assertNotEqual(norm(first), norm(second))
        self.assertEqual(first.read_bytes(), first_bytes)
        second_bytes = second.read_bytes()
        both = sorted([rel_posix(root, first), rel_posix(root, second)])

        def assert_tie(args):
            code, _out, err = run(root, args)
            self.assertEqual(code, 1, err)
            lines = err.splitlines()
            self.assertEqual(lines[0], "prepare_record: multiple open records")
            self.assertEqual(sorted(lines[1:]), both)
            self.assertEqual(first.read_bytes(), first_bytes)
            self.assertEqual(second.read_bytes(), second_bytes)

        assert_tie([])
        assert_tie(["--record-path", ".key-rotation/record-YYYY-MM-DD.md"])
        assert_tie(["--record-path", str(first)])

        code, out, err = run(root, ["--choose", str(second)])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("reused: "), err)
        self.assertEqual(norm(path_from("reused: ", out)), norm(second))
        self.assertEqual(first.read_bytes(), first_bytes)
        self.assertEqual(second.read_bytes(), second_bytes)

        code, _out, err = run(root, ["--choose", str(root / ".key-rotation" / "neither.md")])
        self.assertEqual(code, 1, err)
        lines = err.splitlines()
        self.assertTrue(lines[0].startswith("prepare_record: chosen record not open"))
        self.assertIn("neither.md", lines[0])
        self.assertEqual(sorted(lines[1:]), both)
        self.assertEqual(first.read_bytes(), first_bytes)
        self.assertEqual(second.read_bytes(), second_bytes)

        single = self.make_repo()
        opened = single / ".key-rotation" / "open.md"
        closed = single / ".key-rotation" / "closed.md"
        opened.parent.mkdir()
        opened.write_bytes(b"Sign-off (close): open\n")
        closed.write_bytes(b"Sign-off (close): closed: done\n")
        code, _out, err = run(single, ["--choose", str(closed)])
        self.assertEqual(code, 1, err)
        lines = err.splitlines()
        self.assertTrue(lines[0].startswith("prepare_record: chosen record not open"))
        self.assertEqual(lines[1:], [rel_posix(single, opened)])

        empty = self.make_repo()
        code, _out, err = run(
            empty,
            ["--choose", ".key-rotation/missing.md", "--reuse-only"],
        )
        self.assertEqual(code, 1, err)
        lines = [line for line in err.splitlines() if line]
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("prepare_record: chosen record not open"))
        self.assertNotIn("\n", err.strip())

    def test_08_claims(self):
        day = today()
        root = self.make_repo()
        record_dir = root / ".key-rotation"
        record_dir.mkdir()
        suffixes = [""] + ["-{}".format(n) for n in range(2, 10)]
        for suffix in suffixes:
            claim = record_dir / "record-{}{}.md.tmp".format(day, suffix)
            claim.write_bytes(b"held\n")
        code, _out, err = run(root, [])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: write failed", err)
        self.assertEqual(list(record_dir.glob("*.md")), [])

        reclaimed = self.make_repo()
        record_dir = reclaimed / ".key-rotation"
        record_dir.mkdir()
        claim = record_dir / "record-{}.md.tmp".format(day)
        claim.write_bytes(b"")
        code, out, err = run(reclaimed, [])
        self.assertEqual(code, 0, err)
        created = Path(path_from("created: ", out))
        self.assertEqual(created.name, "record-{}.md".format(day))
        self.assertFalse(claim.exists())
        self.assertTrue(created.is_file())
        self.assertGreater(created.stat().st_size, 0)

        moved = self.make_repo()
        (moved / ".gitignore").write_bytes(b".key-rotation/\n")
        record_dir = moved / ".key-rotation"
        record_dir.mkdir()
        marker = record_dir / "record-{}.md".format(day)
        marker_bytes = b"MARKER-RACE\n"
        (record_dir / "record-{}.md.tmp".format(day)).write_bytes(b"")
        marker.write_bytes(marker_bytes)
        code, out, err = run(moved, [])
        self.assertEqual(code, 0, err)
        created = Path(path_from("created: ", out))
        self.assertEqual(created.name, "record-{}-2.md".format(day))
        self.assertFalse(created.name.endswith(".md-2"))
        self.assertNotIn(".md.", created.name)
        self.assertEqual(marker.read_bytes(), marker_bytes)

        tracked = self.make_repo()
        record_dir = tracked / ".key-rotation"
        record_dir.mkdir()
        second = record_dir / "record-{}-2.md".format(day)
        second.write_bytes(b"tracked\n")
        git(tracked, "add", "--", rel_posix(tracked, second), check=True)
        git(tracked, "commit", "-q", "--no-verify", "-m", "track-stem", check=True)
        second.unlink()
        marker = record_dir / "record-{}.md".format(day)
        marker.write_bytes(marker_bytes)
        code, _out, err = run(tracked, [])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: record is tracked", err)
        self.assertEqual(marker.read_bytes(), marker_bytes)
        self.assertFalse(second.exists())
        self.assertEqual(list(record_dir.glob("*.md")), [marker])

        seeded = self.make_repo()
        record_dir = seeded / ".key-rotation"
        record_dir.mkdir()
        existing = record_dir / "record-{}-2.md".format(day)
        body = b"Sign-off (close): open\nMARKER-SECOND\n"
        existing.write_bytes(body)
        code, out, err = run(seeded, [])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("reused: "), err)
        self.assertEqual(norm(path_from("reused: ", out)), norm(existing))
        self.assertEqual(existing.read_bytes(), body)
        self.assertFalse((record_dir / "record-{}.md".format(day)).exists())

    def test_10_ignore_line_bytes(self):
        root = self.make_repo()
        (root / ".gitignore").write_bytes(b"node_modules")
        code, _out, err = run(root, [])
        self.assertEqual(code, 0, err)
        data = (root / ".gitignore").read_bytes()
        self.assertEqual(data, b"node_modules\n.key-rotation/\n")
        code, _out, err = run(root, [])
        self.assertEqual(code, 0, err)
        self.assertEqual((root / ".gitignore").read_bytes(), data)
        self.assertEqual((root / ".gitignore").read_bytes().splitlines()[0], b"node_modules")

    def test_11_ignore_source(self):
        root = self.make_repo()
        exclude = root / ".git" / "info" / "exclude"
        current = exclude.read_bytes()
        if current and not current.endswith(b"\n"):
            current += b"\n"
        exclude.write_bytes(current + b".key-rotation/\n")
        self.assertFalse((root / ".gitignore").exists())
        code, out, err = run(root, [])
        self.assertEqual(code, 0, err)
        created = Path(path_from("created: ", out))
        gitignore = (root / ".gitignore").read_bytes()
        self.assertIn(b".key-rotation/\n", gitignore)
        verbose = git(root, "check-ignore", "-v", "--", rel_posix(root, created))
        self.assertEqual(verbose.returncode, 0, verbose.stderr)
        source = verbose.stdout.split(b"\t", 1)[0]
        self.assertTrue(source.startswith(b".gitignore:"), verbose.stdout)

    def test_13_status_custom_path(self):
        root = self.make_repo()
        day = today()
        record = root / "incidents" / "record-{}.md".format(day)
        record.parent.mkdir()
        record.write_bytes(b"Sign-off (close): open\nMARKER-STATUS\n")
        self.assertFalse((root / ".key-rotation").exists())
        before = snapshot(root)
        code, out, err = run(root, ["--status", "--record-path", "incidents/record-YYYY-MM-DD.md"])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertEqual(norm(out.strip()), norm(record))
        self.assertEqual(len(out.splitlines()), 1)
        self.assertEqual(snapshot(root), before)
        code, out, err = run(root, ["--status"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "")
        self.assertEqual(snapshot(root), before)
        self.assertFalse((root / ".key-rotation").exists())
        self.assertFalse((root / ".gitignore").exists())

    def test_14_reuse_only(self):
        root = self.make_repo()
        closed = root / ".key-rotation" / "done.md"
        closed.parent.mkdir()
        closed.write_bytes(b"Sign-off (close): closed: done\n")
        before = snapshot(root)
        code, _out, err = run(root, ["--reuse-only"])
        self.assertEqual(code, 1, err)
        lines = err.splitlines()
        self.assertEqual(lines[0], "prepare_record: no open record")
        self.assertEqual(lines[1], rel_posix(root, closed))
        self.assertEqual(snapshot(root), before)
        self.assertFalse((root / ".gitignore").exists())

        empty = self.make_repo()
        code, _out, err = run(empty, ["--reuse-only"])
        self.assertEqual(code, 1, err)
        self.assertEqual([line for line in err.splitlines() if line], ["prepare_record: no open record"])
        self.assertFalse((empty / ".key-rotation").exists())

        opened = self.make_repo()
        record = opened / ".key-rotation" / "live.md"
        record.parent.mkdir()
        body = b"Sign-off (close): open\nMARKER-LIVE\n"
        record.write_bytes(body)
        code, out, err = run(opened, ["--reuse-only"])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("reused: "), err)
        self.assertEqual(norm(path_from("reused: ", out)), norm(record))
        self.assertEqual(record.read_bytes(), body)

        usage = self.make_repo()
        code, _out, err = run(usage, ["--reuse-only", "--new"])
        self.assertEqual(code, 2, err)
        self.assertNotIn("prepare_record:", err)
        self.assertIn("usage:", err.lower())

        indented = self.make_repo()
        record = indented / ".key-rotation" / "indented.md"
        record.parent.mkdir()
        body = b"  Sign-off (close): open\nMARKER-INDENT\n"
        record.write_bytes(body)
        code, out, err = run(indented, [])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("reused: "), err)
        self.assertEqual(record.read_bytes(), body)

        mixed = self.make_repo()
        record = mixed / ".key-rotation" / "mixed.md"
        record.parent.mkdir()
        body = b"Sign-off (close): closed: x\nSign-off (close): open\n"
        record.write_bytes(body)
        code, out, err = run(mixed, [])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("reused: "), err)
        self.assertEqual(norm(path_from("reused: ", out)), norm(record))
        self.assertEqual(record.read_bytes(), body)

        # Ignore is already satisfied: a non-record sibling blocks repair.
        beside = self.make_repo()
        (beside / ".gitignore").write_bytes(b".key-rotation/\n")
        notes = beside / ".key-rotation" / "notes.md"
        notes.parent.mkdir()
        notes_body = b"Follow-up: see Sign-off (close): open later\n"
        notes.write_bytes(notes_body)
        code, out, err = run(beside, [])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("created: "), err)
        created = Path(path_from("created: ", out))
        self.assertNotEqual(norm(created), norm(notes))
        self.assertEqual(notes.read_bytes(), notes_body)
        self.assertIn(b"Sign-off (close): open", created.read_bytes())

    @unittest.skipIf(
        _skip_unreadable(),
        "unreadable-file case is POSIX-only and skips as root",
    )
    def test_14_reuse_only_unreadable(self):
        root = self.make_repo()
        (root / ".gitignore").write_bytes(b".key-rotation/\n")
        hidden = root / ".key-rotation" / "notes.md"
        hidden.parent.mkdir()
        hidden.write_bytes(b"Sign-off (close): open\n")
        os.chmod(str(hidden), 0)
        rel = rel_posix(root, hidden)
        try:
            code, _out, err = run(root, ["--reuse-only"])
            self.assertEqual(code, 1, err)
            lines = err.splitlines()
            self.assertIn("prepare_record: skipped unreadable {}".format(rel), lines)
            self.assertIn("prepare_record: record unreadable {}".format(rel), lines)
            self.assertLess(
                lines.index("prepare_record: skipped unreadable {}".format(rel)),
                lines.index("prepare_record: record unreadable {}".format(rel)),
            )
            self.assertFalse((root / ".key-rotation" / "record-{}.md".format(today())).exists())

            code, _out, err = run(root, [])
            self.assertEqual(code, 1, err)
            self.assertIn("prepare_record: record unreadable {}".format(rel), err)
            self.assertFalse((root / ".key-rotation" / "record-{}.md".format(today())).exists())

            code, out, err = run(root, ["--new"])
            self.assertEqual(code, 0, err)
            created = Path(path_from("created: ", out))
            self.assertNotEqual(norm(created), norm(hidden))
            self.assertTrue(created.is_file())
            self.assertGreater(created.stat().st_size, 0)
        finally:
            os.chmod(str(hidden), stat.S_IRUSR | stat.S_IWUSR)

    def test_15_record_path_rejected(self):
        root = self.make_repo()
        before = snapshot(root)
        cases = [
            ["--record-path", "incidents/YYYY-MM-DD/record.md"],
            ["--record-path", ".key-rotation/record.txt"],
        ]
        for args in cases:
            with self.subTest(args=args):
                code, _out, err = run(root, args)
                self.assertEqual(code, 1, err)
                self.assertIn("prepare_record: record path rejected", err)
                self.assertEqual(snapshot(root), before)
                self.assertFalse((root / ".gitignore").exists())

        day = today()
        target = root / ".key-rotation" / "record-{}.md".format(day)
        target.mkdir(parents=True)
        before = snapshot(root)
        code, _out, err = run(root, ["--record-path", ".key-rotation/record-YYYY-MM-DD.md"])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: record path rejected", err)
        self.assertEqual(snapshot(root), before)
        self.assertFalse((root / ".gitignore").exists())
        self.assertTrue(target.is_dir())


if __name__ == "__main__":
    unittest.main()
