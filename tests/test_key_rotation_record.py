#!/usr/bin/env python3
"""Record lifecycle and read-only name, match, and hash tests.

Stdlib unittest. Builds a temporary git repository the way the session-handoff
tests do, and runs the script as a subprocess of sys.executable the way the
spec-close tests do.
"""

import hashlib
import importlib.util
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


B64_64 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def write_rel(root, rel, data):
    path = root.joinpath(*rel.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def assert_secrets(case, out, err, *secrets):
    for secret in secrets:
        case.assertNotIn(secret, out)
        case.assertNotIn(secret, err)


def armor_span(body_lines, tail):
    """Hashed armor bytes: header through END, no final line ending."""
    lines = ["-----BEGIN TEST-----"] + list(body_lines) + [tail, "-----END TEST-----"]
    return "\n".join(lines).encode("ascii")


def armor_file(body_lines, tail, ending=b"\n", final=True):
    text_lines = ["-----BEGIN TEST-----"] + list(body_lines) + [tail, "-----END TEST-----"]
    raw = [line.encode("ascii") for line in text_lines]
    body = ending.join(raw)
    if final:
        body += ending
    return body


def load_script():
    spec = importlib.util.spec_from_file_location("prepare_record_vhs78", str(SCRIPT))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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

    def test_09_quoted_sentinel_and_config_txt(self):
        root = self.make_repo()
        write_rel(root, ".env", b'NAME="VALUE-SENTINEL"\n')
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        assert_secrets(self, out, err, "VALUE-SENTINEL")

        root = self.make_repo()
        write_rel(root, "config.txt", b'NAME="VALUE-SENTINEL"\n')
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        assert_secrets(self, out, err, "VALUE-SENTINEL")

        code, out, err = run(root, ["--list-names", "--file", "config.txt"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        assert_secrets(self, out, err, "VALUE-SENTINEL")

    def test_09_app_env_unexplained(self):
        root = self.make_repo()
        write_rel(root, "app.env", b"NAME=1\nKEY = 2\n  # note\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        self.assertEqual(err, "prepare_record: unsupported syntax app.env:2\n")
        self.assertNotIn("KEY", out)
        self.assertNotIn("note", err)

    def test_09_secret_key_not_read(self):
        root = self.make_repo()
        first = b"A" * 43 + b"="
        second = b"B" * 43 + b"=="
        write_rel(root, "secret.key", first + b"\n")
        write_rel(root, "another.key", second + b"\n")
        write_rel(root, "keep.env", b"KEEPNAME=1\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEEPNAME\n")
        self.assertNotIn("secret.key", err)
        self.assertNotIn("another.key", err)
        self.assertNotIn("AAAA", out)
        self.assertNotIn("BBBB", out)

    def test_09_node_modules_skipped(self):
        root = self.make_repo()
        write_rel(root, "node_modules/pkg/.env", b"NAME=1\n")
        write_rel(root, "keep.env", b"KEEPNAME=1\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEEPNAME\n")

    def test_09_hash_quoted_endings(self):
        expect = sha256(b'"VALUE-SENTINEL"')
        fixtures = {
            "lf": b'NAME="VALUE-SENTINEL"\n',
            "crlf": b'NAME="VALUE-SENTINEL"\r\n',
            "no_final_newline": b'NAME="VALUE-SENTINEL"',
        }
        for label, data in fixtures.items():
            with self.subTest(fixture=label):
                root = self.make_repo()
                write_rel(root, ".env", data)
                code, out, err = run(root, ["--hash-name", "NAME", "--file", ".env"])
                self.assertEqual(code, 0, err)
                self.assertEqual(out, "NAME {}\n".format(expect))
                assert_secrets(self, out, err, "VALUE-SENTINEL")

    def test_09_hash_absent_empty(self):
        for label, data in (("lf", b"NAME=\n"), ("crlf", b"NAME=\r\n")):
            with self.subTest(fixture=label):
                root = self.make_repo()
                write_rel(root, ".env", data)
                code, out, err = run(root, ["--hash-name", "NAME", "--file", ".env"])
                self.assertEqual(code, 0, err)
                self.assertEqual(out, "NAME hash: absent\n")

    def test_09_export_and_withheld_other(self):
        root = self.make_repo()
        write_rel(root, ".env", b'export NAME="VALUE"\nOTHER=\n')
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        self.assertEqual(err, "prepare_record: withheld line .env:2\n")
        self.assertNotIn("OTHER", out)
        self.assertNotIn("VALUE", out)
        self.assertNotIn("VALUE", err)

        code, out, err = run(root, ["--hash-name", "NAME", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME {}\n".format(sha256(b'"VALUE"')))
        assert_secrets(self, out, err, "VALUE")

        code, out, err = run(root, ["--hash-name", "OTHER", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "OTHER hash: absent\n")

    def test_09_base64_value_then_empty_name(self):
        root = self.make_repo()
        write_rel(root, ".env", b"KEY=" + B64_64 + b"\nXYZ=\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY\n")
        self.assertEqual(err, "prepare_record: withheld line .env:2\n")
        self.assertNotIn("XYZ", out)
        self.assertNotIn("XYZ", err)
        assert_secrets(self, out, err, B64_64.decode("ascii"))

    def test_09_raw_base32_31(self):
        root = self.make_repo()
        name = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ23456"
        self.assertEqual(len(name), 31)
        write_rel(root, ".env", name + b"=\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        self.assertNotIn(name.decode("ascii"), out)
        self.assertNotIn(name.decode("ascii"), err)

    def test_09_last_assignment_wins(self):
        root = self.make_repo()
        write_rel(root, ".env", b"NAME=first\nNAME=second\n")
        code, out, err = run(root, ["--hash-name", "NAME", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME {}\n".format(sha256(b"second")))
        self.assertEqual(err, "prepare_record: duplicate assignment NAME .env\n")
        assert_secrets(self, out, err, "first", "second")

        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        self.assertEqual(err, "prepare_record: duplicate assignment .env:2\n")
        self.assertNotIn("NAME", err)

    def test_09_mixed_case(self):
        root = self.make_repo()
        write_rel(root, ".env", b"mixedCase=1\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        self.assertNotIn("mixedCase", out)
        self.assertNotIn("mixedCase", err)

    def test_09_mixed_case_43(self):
        root = self.make_repo()
        name = b"Aa" + (b"b" * 41)
        self.assertEqual(len(name), 43)
        write_rel(root, ".env", name + b"=\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        self.assertNotIn(name.decode("ascii"), out)
        self.assertNotIn(name.decode("ascii"), err)

    def test_09_unquoted_armor(self):
        expect = sha256(armor_span(["line-one", "line-two"], "AB=="))
        other = sha256(armor_span(["line-one", "line-zzz"], "AB=="))
        self.assertNotEqual(expect, other)

        root = self.make_repo()
        write_rel(root, ".env", b"KEY=" + armor_file(["line-one", "line-two"], "AB=="))
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY\n")
        self.assertEqual(err, "")
        assert_secrets(self, out, err, "line-one", "line-two", "AB==")

        variants = {
            "lf": b"KEY=" + armor_file(["line-one", "line-two"], "AB==", b"\n", True),
            "crlf": b"KEY=" + armor_file(["line-one", "line-two"], "AB==", b"\r\n", True),
            "no_final_newline": b"KEY=" + armor_file(
                ["line-one", "line-two"], "AB==", b"\n", False),
        }
        for label, data in variants.items():
            with self.subTest(fixture=label):
                root = self.make_repo()
                write_rel(root, ".env", data)
                code, out, err = run(root, ["--hash-name", "KEY", "--file", ".env"])
                self.assertEqual(code, 0, err)
                self.assertEqual(out, "KEY {}\n".format(expect))
                assert_secrets(self, out, err, "line-one", "line-two", "AB==")

        root = self.make_repo()
        write_rel(root, ".env", b"KEY=" + armor_file(["line-one", "line-zzz"], "AB=="))
        code, out, err = run(root, ["--hash-name", "KEY", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY {}\n".format(other))
        self.assertNotEqual(out, "KEY {}\n".format(expect))

    def test_09_private_key_then_armor(self):
        expect = sha256(armor_span(["line-one", "line-two"], "QK=="))
        root = self.make_repo()
        block = armor_file(["line-one", "line-two"], "QK==")
        write_rel(root, ".env", b"PRIVATE_KEY=\n" + block)
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        assert_secrets(self, out, err, "QK==", "line-one", "PRIVATE_KEY")

        code, out, err = run(root, ["--hash-name", "PRIVATE_KEY", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "PRIVATE_KEY {}\n".format(expect))
        self.assertNotIn("hash: absent", out)
        assert_secrets(self, out, err, "QK==", "line-one")

    def test_09_key_base64_xyz_cert(self):
        root = self.make_repo()
        data = (
            b"KEY=" + B64_64 + b"\nXYZ=\nCERT="
            + armor_file(["line-one"], "AB==")
        )
        write_rel(root, ".env", data)
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY\nCERT\n")
        self.assertEqual(err, "prepare_record: withheld line .env:2\n")
        self.assertNotIn("XYZ", out)
        self.assertNotIn("XYZ", err)
        assert_secrets(self, out, err, B64_64.decode("ascii"), "line-one", "AB==")

    def test_09_abcd_then_bare_header(self):
        root = self.make_repo()
        write_rel(root, ".env", b"ABCD==\n" + armor_file(["line-one"], "AB=="))
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        self.assertNotIn("unsupported", err)
        self.assertNotIn("ABCD", err)
        assert_secrets(self, out, err, "line-one", "AB==")

    def test_09_xyz_space_withheld(self):
        root = self.make_repo()
        write_rel(root, ".env", b"NAME=1\nXYZ= \n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        self.assertEqual(err, "prepare_record: withheld line .env:2\n")
        self.assertNotIn("XYZ", out)
        self.assertNotIn("XYZ", err)

    def test_09_blank_line_breaks_armor(self):
        root = self.make_repo()
        write_rel(root, ".env", b"NAME=\n\n" + armor_file(["line-one"], "AB=="))
        code, out, err = run(root, ["--hash-name", "NAME", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME hash: absent\n")
        assert_secrets(self, out, err, "line-one", "AB==")

    def test_09_same_name_two_env_files(self):
        root = self.make_repo()
        write_rel(root, ".env", b"NAME=1\n")
        write_rel(root, ".env.example", b"NAME=2\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")
        self.assertNotIn("duplicate assignment", err)

    def test_09_armor_space_before_header(self):
        expect = sha256(armor_span(["line-one", "line-two"], "AB=="))
        root = self.make_repo()
        write_rel(root, ".env", b"KEY= " + armor_file(["line-one", "line-two"], "AB=="))
        code, out, err = run(root, ["--hash-name", "KEY", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY {}\n".format(expect))
        assert_secrets(self, out, err, "line-one", "AB==")

    def test_09_private_key_space_then_armor(self):
        expect = sha256(armor_span(["line-one", "line-two"], "QK=="))
        root = self.make_repo()
        block = armor_file(["line-one", "line-two"], "QK==")
        write_rel(root, "nospace.env", b"PRIVATE_KEY=\n" + block)
        write_rel(root, "space.env", b"PRIVATE_KEY= \n" + block)
        code, out, err = run(root, ["--hash-name", "PRIVATE_KEY", "--file", "space.env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "PRIVATE_KEY {}\n".format(expect))
        code, out2, err2 = run(root, ["--hash-name", "PRIVATE_KEY", "--file", "nospace.env"])
        self.assertEqual(code, 0, err2)
        self.assertEqual(out2, out)
        assert_secrets(self, out, err, "QK==", "line-one")

    @unittest.skipIf(_skip_unreadable(), "unreadable files are POSIX-only")
    def test_09_unreadable_env(self):
        root = self.make_repo()
        env = write_rel(root, ".env", b"NAME=1\n")
        write_rel(root, "node_modules/names.txt", b"NAME\n")
        os.chmod(str(env), 0)
        try:
            code, _out, err = run(root, ["--list-names"])
            self.assertEqual(code, 0, err)
            self.assertIn("prepare_record: skipped unreadable .env", err)
            code, _out, err = run(
                root,
                ["--match-names", "--names-file", "node_modules/names.txt"],
            )
            self.assertEqual(code, 0, err)
            self.assertIn("prepare_record: skipped unreadable .env", err)
        finally:
            os.chmod(str(env), stat.S_IRUSR | stat.S_IWUSR)

    def test_09_cert_raw_body_unsupported(self):
        root = self.make_repo()
        body = b"B" * 64
        data = b"CERT=" + B64_64 + b"\n" + body + b"\n" + body + b"\nQUJD==\n"
        write_rel(root, ".env", data)
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "CERT\n")
        self.assertEqual(err, "prepare_record: unsupported syntax .env:2\n")
        self.assertNotIn("QUJD", out)
        self.assertNotIn("QUJD", err)
        self.assertNotIn("withheld", err)
        assert_secrets(self, out, err, B64_64.decode("ascii"))

    def test_09_raw_base32_28(self):
        root = self.make_repo()
        name = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ23"
        self.assertEqual(len(name), 28)
        write_rel(root, ".env", name + b"====\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        self.assertNotIn(name.decode("ascii"), out)
        self.assertNotIn(name.decode("ascii"), err)

    def test_09_backslash_continuation(self):
        root = self.make_repo()
        write_rel(root, ".env", b"TOKEN=prefix\\\nfragment=tail\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "TOKEN\n")
        assert_secrets(self, out, err, "prefix", "fragment", "tail")

        code, out, err = run(root, ["--hash-name", "TOKEN", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "TOKEN {}\n".format(sha256(b"prefix\\\nfragment=tail")))
        assert_secrets(self, out, err, "prefix", "fragment", "tail")

    def test_09_mixed_case_quoted_armor(self):
        root = self.make_repo()
        data = b'privateKey="-----BEGIN TEST-----\nline-one\nQQ==\n-----END TEST-----"\n'
        write_rel(root, ".env", data)
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: withheld line .env:1\n")
        self.assertNotIn("unsupported", err)
        self.assertNotIn("privateKey", err)
        assert_secrets(self, out, err, "QQ==", "line-one", "BEGIN")

    def test_09_pem_file_consumed(self):
        root = self.make_repo()
        body = "B" * 64
        write_rel(root, "key.pem", armor_file([body, body], "AB=="))
        code, out, err = run(root, ["--list-names", "--file", "key.pem"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "")
        self.assertNotIn("withheld", err)

    def test_09_match_high_bytes(self):
        root = self.make_repo()
        write_rel(root, "notes.txt", b"\xc3\x90\n")
        write_rel(root, "node_modules/names.txt", b"NAME\n")
        code, out, err = run(
            root,
            ["--match-names", "--names-file", "node_modules/names.txt"],
        )
        self.assertEqual(code, 0, err)
        self.assertNotIn("\xc3", out)
        self.assertEqual(out, "")

    def test_09_bom(self):
        root = self.make_repo()
        write_rel(root, ".env", b"\xef\xbb\xbfNAME=1\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME\n")

    def test_09_utf16_binary(self):
        root = self.make_repo()
        write_rel(root, ".env", "NAME=1\n".encode("utf-16"))
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: skipped binary .env\n")

    def test_09_missing_file(self):
        root = self.make_repo()
        code, out, err = run(root, ["--list-names", "--file", "missing.env"])
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "")
        self.assertIn("prepare_record: not a readable file missing.env", err)

    def test_09_long_value(self):
        root = self.make_repo()
        payload = b"a" * 4097
        write_rel(root, ".env", b"LONG=" + payload + b"\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "LONG\n")
        self.assertNotIn(payload.decode("ascii"), out)

        code, out, err = run(root, ["--hash-name", "LONG", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "LONG {}\n".format(sha256(payload)))
        self.assertNotIn("hash: absent", out)
        self.assertNotIn(payload.decode("ascii"), out)

    def test_09_quoted_multiline_pem(self):
        def file_bytes(middle, ending):
            parts = [
                b'KEY="-----BEGIN TEST-----',
                b"line-one",
                middle,
                b"BODY3==",
                b'-----END TEST-----"',
            ]
            return ending.join(parts) + ending

        def expect(middle):
            parts = [
                '"-----BEGIN TEST-----',
                "line-one",
                middle,
                "BODY3==",
                '-----END TEST-----"',
            ]
            return sha256("\n".join(parts).encode("ascii"))

        root = self.make_repo()
        write_rel(root, ".env", file_bytes(b"middle-line", b"\n"))
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY\n")
        self.assertEqual(err, "")
        assert_secrets(self, out, err, "middle-line", "BODY3", "line-one")

        code, out, err = run(root, ["--hash-name", "KEY", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY {}\n".format(expect("middle-line")))
        assert_secrets(self, out, err, "middle-line", "BODY3")

        root = self.make_repo()
        write_rel(root, ".env", file_bytes(b"other-middle", b"\n"))
        code, out, err = run(root, ["--hash-name", "KEY", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY {}\n".format(expect("other-middle")))
        self.assertNotEqual(expect("other-middle"), expect("middle-line"))

        root = self.make_repo()
        write_rel(root, ".env", file_bytes(b"middle-line", b"\r\n"))
        code, out, err = run(root, ["--hash-name", "KEY", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "KEY {}\n".format(expect("middle-line")))

    def test_09_escaped_quote_continues(self):
        root = self.make_repo()
        data = b'SA="{\\"a\\": 1,\n\\"b\\": 2}"\n'
        write_rel(root, ".env", data)
        expect = sha256(b'"{\\"a\\": 1,\n\\"b\\": 2}"')
        code, out, err = run(root, ["--hash-name", "SA", "--file", ".env"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "SA {}\n".format(expect))
        self.assertEqual(err, "")
        self.assertNotIn("unsupported", err)

    def test_09_unterminated_span(self):
        root = self.make_repo()
        data = (
            b"EARLY=x\n"
            b'KEY="-----BEGIN TEST-----\n'
            b"line-one\n"
            b"BODY3==\n"
            b"-----END TEST-----\n"
            b"LATER=x\n"
        )
        write_rel(root, ".env", data)
        write_rel(root, "names.txt", b"EARLY\nKEY\nLATER\n")
        code, out, err = run(
            root,
            ["--hash-names", "--names-file", "names.txt", "--file", ".env"],
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(
            out,
            "EARLY {}\nKEY hash: unterminated\nLATER hash: unread\n".format(sha256(b"x")),
        )
        self.assertEqual(err, "prepare_record: possibly reassigned EARLY .env\n")
        assert_secrets(self, out, err, "BEGIN", "BODY3", "line-one")
        self.assertNotIn("x", out)
        self.assertNotIn("x", err)

        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "EARLY\nKEY\n")
        self.assertEqual(err, "prepare_record: unterminated span .env:2\n")
        self.assertNotIn("LATER", out)
        assert_secrets(self, out, err, "BEGIN", "BODY3", "line-one")

    def test_09_nul_file(self):
        root = self.make_repo()
        write_rel(root, "blob.bin", b"\x00NULSENTINEL")
        code, out, err = run(root, ["--hash-name", "NAME", "--file", "blob.bin"])
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "")
        self.assertIn("prepare_record: not a readable file blob.bin", err)
        self.assertNotIn("hash: absent", out)
        self.assertNotIn("hash: absent", err)
        self.assertNotIn("NULSENTINEL", out)
        self.assertNotIn("NULSENTINEL", err)

    def test_09_match_line_boundaries(self):
        root = self.make_repo()
        write_rel(root, "once.txt", b"EDGE")
        long_line = (b"-" * 5000) + b"EDGE" + (b"-" * 100)
        self.assertGreater(len(long_line), 4096)
        write_rel(root, "long.txt", long_line)
        write_rel(root, "node_modules/names.txt", b"EDGE\n")
        code, out, err = run(
            root,
            ["--match-names", "--names-file", "node_modules/names.txt"],
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(out.splitlines()), ["EDGE long.txt", "EDGE once.txt"])

    def test_09_hash_names_two(self):
        root = self.make_repo()
        write_rel(root, ".env", b"ALPHA=alpha-secret\nBETA=beta-secret\n")
        write_rel(root, "names.txt", b"ALPHA\nBETA\n")
        code, out, err = run(
            root,
            ["--hash-names", "--names-file", "names.txt", "--file", ".env"],
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(
            out,
            "ALPHA {}\nBETA {}\n".format(sha256(b"alpha-secret"), sha256(b"beta-secret")),
        )
        self.assertEqual(len(out.splitlines()), 2)
        assert_secrets(self, out, err, "alpha-secret", "beta-secret")

    def test_09_directory_file(self):
        root = self.make_repo()
        (root / "subdir").mkdir()
        code, out, err = run(root, ["--hash-name", "NAME", "--file", "subdir"])
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "")
        self.assertIn("prepare_record: not a readable file subdir", err)
        self.assertNotIn("hash: absent", out)
        self.assertNotIn("hash: absent", err)

    def test_12_names_sidecar(self):
        root = self.make_repo()
        record = root / ".key-rotation" / "incident.md"
        record.parent.mkdir()
        body = b"Sign-off (close): open\nSIDECARTOKEN\n"
        record.write_bytes(body)
        write_rel(root, ".key-rotation/.names.tmp", b"SIDECARTOKEN\n")
        code, out, err = run(root, [])
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("reused: "), err)
        self.assertEqual(record.read_bytes(), body)
        self.assertEqual((root / ".gitignore").read_bytes(), b".key-rotation/\n")
        printed = path_from("reused: ", out)
        write_rel(root, "node_modules/names.txt", b"SIDECARTOKEN\n")
        code, out, err = run(
            root,
            [
                "--match-names",
                "--names-file",
                "node_modules/names.txt",
                "--record-path",
                printed,
            ],
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertNotIn(".names.tmp", out)
        self.assertNotIn("incident.md", out)
        self.assertNotIn("SIDECARTOKEN", out)

        root = self.make_repo()
        record = root / ".key-rotation" / "incident.md"
        record.parent.mkdir()
        body = b"Sign-off (close): open\n"
        record.write_bytes(body)
        write_rel(root, ".key-rotation/.env", b"NAME=x\n")
        printed = os.path.abspath(os.path.realpath(str(record)))
        write_rel(root, "node_modules/names.txt", b"NAME\n")
        code, out, err = run(
            root,
            [
                "--match-names",
                "--names-file",
                "node_modules/names.txt",
                "--record-path",
                printed,
            ],
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "NAME .key-rotation/.env\n")
        self.assertNotIn("incident.md", out)
        self.assertNotIn("x", out)
        self.assertNotIn("x", err)

        before = snapshot(root)
        code, _out, err = run(root, [])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: parent is not a record directory", err)
        self.assertFalse((root / ".gitignore").exists())
        self.assertEqual(record.read_bytes(), body)
        self.assertEqual(snapshot(root), before)

    def test_16_ignore_pattern_rejected(self):
        root = self.make_repo()
        before = snapshot(root)
        code, out, err = run(root, ["--record-path", "record.md"])
        self.assertEqual(code, 1, err)
        self.assertIn("prepare_record: ignore pattern rejected", err)
        self.assertEqual(out, "")
        self.assertEqual(snapshot(root), before)
        self.assertFalse((root / ".gitignore").exists())
        self.assertFalse((root / "record.md").exists())

    def test_16_outside_paths(self):
        root = self.make_repo()
        write_rel(root, ".env", b"LEAKNAME=INSIDE-VALUE-SENTINEL\n")
        write_rel(root, "names.txt", b"LEAKNAME\n")
        outside = Path(tempfile.mkdtemp(prefix="vhs78-out-"))
        self.addCleanup(shutil.rmtree, str(outside), True)
        outside_file = outside / "secret.env"
        outside_file.write_bytes(b"NAME=OUTSIDE-SENTINEL-VALUE\n")
        outside_names = outside / "names.txt"
        outside_names.write_bytes(b"OUTSIDE-SENTINEL-VALUE\n")
        cases = [
            ["--list-names", "--file", str(outside_file)],
            ["--match-names", "--names-file", str(outside_names)],
            ["--hash-name", "NAME", "--file", str(outside_file)],
            ["--hash-names", "--names-file", str(outside_names), "--file", ".env"],
            ["--hash-names", "--names-file", "names.txt", "--file", str(outside_file)],
        ]
        for args in cases:
            with self.subTest(args=args[:2]):
                code, out, err = run(root, args)
                self.assertEqual(code, 1, err)
                self.assertEqual(out, "")
                self.assertIn("prepare_record: path is outside the project", err)
                self.assertNotIn("OUTSIDE-SENTINEL-VALUE", out)
                self.assertNotIn("OUTSIDE-SENTINEL-VALUE", err)
                self.assertNotIn("INSIDE-VALUE-SENTINEL", out)
                self.assertNotIn("INSIDE-VALUE-SENTINEL", err)
                self.assertNotIn("LEAKNAME", out)

    def test_16_symlink(self):
        root = self.make_repo()
        outside = Path(tempfile.mkdtemp(prefix="vhs78-link-"))
        self.addCleanup(shutil.rmtree, str(outside), True)
        (outside / ".env").write_bytes(b"OUTSIDENAME=OUTSIDE-SENTINEL-VALUE\n")
        link = root / "escape"
        try:
            os.symlink(str(outside), str(link), target_is_directory=True)
        except OSError as exc:
            self.skipTest("symlink refused: {}".format(exc))
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertIn("prepare_record: skipped outside-root link escape", err)
        self.assertNotIn("OUTSIDENAME", out)
        self.assertNotIn("OUTSIDE-SENTINEL-VALUE", out)
        self.assertNotIn("OUTSIDE-SENTINEL-VALUE", err)

    def test_16_recheck_restore(self):
        module = load_script()
        real = module.ignore_checks

        def drive(append):
            root = self.make_repo()
            (root / ".gitignore").write_bytes(b"keep\n")
            calls = {"n": 0, "first_satisfied": None}

            def wrapped(root_arg, parent_rel, file_rel):
                calls["n"] += 1
                parent, file_check = real(root_arg, parent_rel, file_rel)
                if calls["n"] == 1:
                    calls["first_satisfied"] = parent.satisfied and file_check.satisfied
                    return parent, file_check
                if append:
                    path = Path(root_arg) / ".gitignore"
                    path.write_bytes(path.read_bytes() + b"extra/\n")
                parent.satisfied = False
                file_check.satisfied = False
                return parent, file_check

            module.ignore_checks = wrapped
            saved = {}
            for key in list(os.environ):
                if key.startswith("GIT_"):
                    saved[key] = os.environ.pop(key)
            try:
                try:
                    code = module.execute(["--project-root", str(root)])
                    err = ""
                except module.Stop as exc:
                    code = exc.code
                    err = exc.stderr
            finally:
                os.environ.update(saved)
                module.ignore_checks = real
            self.assertFalse(calls["first_satisfied"])
            self.assertGreaterEqual(calls["n"], 2)
            self.assertEqual(code, 1, err)
            self.assertIn("prepare_record: ignore check failed", err)
            self.assertEqual(list((root / ".key-rotation").glob("*.md")), [])
            return (root / ".gitignore").read_bytes()

        self.assertEqual(drive(False), b"keep\n")
        changed = drive(True)
        self.assertIn(b"extra/\n", changed)
        self.assertIn(b".key-rotation/\n", changed)
        self.assertNotEqual(changed, b"keep\n")

    def test_16_readonly_leaves_gitignore(self):
        root = self.make_repo()
        seeded = b"keep-me\n"
        (root / ".gitignore").write_bytes(seeded)
        write_rel(root, ".env", b"NAME=secret-ro\n")
        write_rel(root, "names.txt", b"NAME\n")
        modes = [
            ["--list-names"],
            ["--match-names", "--names-file", "names.txt"],
            ["--hash-name", "NAME", "--file", ".env"],
            ["--hash-names", "--names-file", "names.txt", "--file", ".env"],
        ]
        for args in modes:
            with self.subTest(args=args[0]):
                code, out, err = run(root, args)
                self.assertEqual(code, 0, err)
                self.assertEqual((root / ".gitignore").read_bytes(), seeded)
                self.assertFalse((root / ".key-rotation").exists())
                assert_secrets(self, out, err, "secret-ro")

    def test_16_heredoc_and_unexplained(self):
        root = self.make_repo()
        write_rel(root, ".env", b"KEY=$(cat <<END\nfragment=tail\nEND\n)\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "prepare_record: unsupported syntax .env:1\n")
        assert_secrets(self, out, err, "fragment", "tail", "KEY")

        root = self.make_repo()
        write_rel(root, ".env", b"ONE=1\nTWO=2\nnot an assignment\nTHREE=3\n")
        code, out, err = run(root, ["--list-names"])
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "ONE\nTWO\n")
        self.assertEqual(err, "prepare_record: unsupported syntax .env:3\n")
        self.assertNotIn("THREE", out)
        self.assertNotIn("not an assignment", err)


if __name__ == "__main__":
    unittest.main()
