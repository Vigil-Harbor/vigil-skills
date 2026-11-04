#!/usr/bin/env python3
"""Tests for spec-land's land_check.py (VHS-81).

Stdlib unittest. The script is loaded by file path, the same way
tests/test_spec_close_log.py loads prepend_log_entry.py, so it can stay a
portable script without package boilerplate.

Cases pass stdin strings, or subprocess bytes for the invalid-UTF-8 row.
They do not create a git repo and do not call GitHub.

The VHS-57 test plan's states.json Post-merge Checklists assertions are
TestCltPostMergeChecklists below.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "spec-land" / "scripts" / "land_check.py"

HEAD = "1" * 40
BASE = "2" * 40
PATCH = "3" * 40
RECORDED = "a" * 40
OTHER = "b" * 40
RANGE_OTHER = "c" * 40
REVIEW_TOKENS = ("passed", "skipped", "inconclusive", "not-run")


def load_script(path: Path, module_name: str):
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load script at {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class StdinStub:
    """sys.stdin stand-in with a binary buffer, so main() can decode bytes."""

    def __init__(self, data: bytes) -> None:
        self.buffer = io.BytesIO(data)


def run_main(module, argv, stdin: str = ""):
    out, err = io.StringIO(), io.StringIO()
    stub = StdinStub(stdin.encode("utf-8"))
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
            mock.patch.object(sys, "stdin", stub):
        code = module.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def marker(head=HEAD, base=BASE, patch=PATCH, review="passed", nl="\n",
           drop=None, trailer=""):
    rows = [
        "<!-- vigil-spec-land",
        "head: " + head,
        "base: " + base,
        "patch-id: " + patch,
        "review: " + review,
        "-->",
    ]
    if drop is not None:
        del rows[drop]
    body = nl.join(rows)
    if trailer:
        body = body + nl + trailer
    return body


def decide_argv(parents, commits, recorded, single, range_id=None):
    argv = [
        "decide",
        "--parents", str(parents),
        "--pr-commits", str(commits),
        "--recorded", recorded,
        "--single", single,
    ]
    if range_id is not None:
        argv.extend(["--range", range_id])
    return argv


class TestLandCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script(SCRIPT, "spec_land_check_under_test")

    def test_parse_well_formed_prints_four_fields(self):
        for token in REVIEW_TOKENS:
            with self.subTest(review=token):
                code, out, err = run_main(self.mod, ["parse"], marker(review=token))
                self.assertEqual(code, 0, err)
                self.assertEqual(
                    out,
                    f"head={HEAD} base={BASE} patch-id={PATCH} review={token}\n",
                )
                self.assertEqual(err, "")

    def test_parse_no_sentinel_exits_1(self):
        code, out, err = run_main(self.mod, ["parse"], "nothing to record here\n")
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_parse_prose_mention_exits_1(self):
        body = "see vigil-spec-land in the discussion\n" + marker()
        code, out, err = run_main(self.mod, ["parse"], body)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_parse_leading_bom_exits_0(self):
        code, out, err = run_main(self.mod, ["parse"], "\ufeff" + marker())
        self.assertEqual(code, 0, err)
        self.assertEqual(
            out, f"head={HEAD} base={BASE} patch-id={PATCH} review=passed\n")
        self.assertEqual(err, "")

    def test_parse_uppercase_sha_exits_2(self):
        code, out, err = run_main(self.mod, ["parse"], marker(head="A" * 40))
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")

    def test_parse_unknown_review_token_exits_2(self):
        code, out, err = run_main(self.mod, ["parse"], marker(review="approved"))
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")

    def test_parse_prose_after_close_exits_2(self):
        code, out, err = run_main(
            self.mod, ["parse"], marker(trailer="landed by hand"))
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")

    def test_parse_missing_field_exits_2(self):
        code, out, err = run_main(self.mod, ["parse"], marker(drop=2))
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")

    def test_parse_crlf_exits_0(self):
        code, out, err = run_main(self.mod, ["parse"], marker(nl="\r\n"))
        self.assertEqual(code, 0, err)
        self.assertEqual(
            out, f"head={HEAD} base={BASE} patch-id={PATCH} review=passed\n")
        self.assertEqual(err, "")

    def test_decide_squash_match_single(self):
        code, out, err = run_main(
            self.mod,
            decide_argv(1, 4, RECORDED, RECORDED),
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "match single\n")
        self.assertEqual(err, "")

    def test_decide_rebase_match_range(self):
        code, out, err = run_main(
            self.mod,
            decide_argv(1, 2, RECORDED, OTHER, RECORDED),
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "match range\n")
        self.assertEqual(err, "")

    def test_decide_merge_match_single(self):
        code, out, err = run_main(
            self.mod,
            decide_argv(2, 2, RECORDED, RECORDED, RANGE_OTHER),
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "match single\n")
        self.assertEqual(err, "")
        # Decision 3: parents >= 2 ignores range even when that id matches.
        code, out, err = run_main(
            self.mod,
            decide_argv(2, 2, RECORDED, OTHER, RECORDED),
        )
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "mismatch\n")

    def test_decide_range_not_consulted_when_single_matches(self):
        code, out, err = run_main(
            self.mod,
            decide_argv(1, 5, RECORDED, RECORDED, RANGE_OTHER),
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "match single\n")
        self.assertEqual(err, "")

    def test_decide_neither_id_mismatch(self):
        code, out, err = run_main(
            self.mod,
            decide_argv(1, 3, RECORDED, OTHER, RANGE_OTHER),
        )
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "mismatch\n")

    def test_decide_bad_arguments_exit_2(self):
        cases = (
            decide_argv(0, 1, RECORDED, RECORDED),
            decide_argv(1, 0, RECORDED, RECORDED),
            decide_argv(1, 1, "A" * 40, RECORDED),
        )
        for argv in cases:
            with self.subTest(argv=argv):
                code, out, err = run_main(self.mod, argv)
                self.assertEqual(code, 2, err)
                self.assertEqual(out, "")

    def test_decide_one_commit_compares_single_only(self):
        code, out, err = run_main(
            self.mod,
            decide_argv(1, 1, RECORDED, RECORDED, RANGE_OTHER),
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "match single\n")
        code, out, err = run_main(
            self.mod,
            decide_argv(1, 1, RECORDED, OTHER, RECORDED),
        )
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "mismatch\n")

    def test_invalid_utf8_exits_3_not_1(self):
        invocations = (
            ["parse"],
            decide_argv(1, 1, RECORDED, RECORDED),
            ["overlap"],
        )
        for argv in invocations:
            with self.subTest(argv=argv[0]):
                proc = subprocess.run(
                    [sys.executable, str(SCRIPT), *argv],
                    input=b"\xff",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.assertEqual(proc.returncode, 3)
                self.assertNotEqual(proc.returncode, 1)
                self.assertEqual(proc.stdout, b"")

    def test_overlap_one_shared_path(self):
        stdin = "alpha.py\nshared.py\nzebra.py\n--\nother.py\nshared.py\n"
        code, out, err = run_main(self.mod, ["overlap"], stdin)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "shared.py\n")

    def test_overlap_disjoint_paths(self):
        stdin = "Dir/A.py\n--\nDir/a.py\n"
        code, out, err = run_main(self.mod, ["overlap"], stdin)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "clear\n")
        self.assertEqual(err, "")

    def test_overlap_two_empty_lists(self):
        code, out, err = run_main(self.mod, ["overlap"], "--\n")
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "clear\n")
        self.assertEqual(err, "")

    def test_overlap_blank_lines_are_not_paths(self):
        code, out, err = run_main(self.mod, ["overlap"], "a.py\n\n--\nb.py\n\n")
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "clear\n")


CLT_CHECKLISTS_UUID = "5bbbab1a-bb0e-41b1-b40f-bdd761e0273b"


class TestCltPostMergeChecklists(unittest.TestCase):
    """Repo states.json: CLT gained Post-merge Checklists (VHS-83). No Plane call."""

    def test_clt_post_merge_checklists(self):
        path = REPO_ROOT / "skills" / "ship-spec" / "states.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        clt = data["CLT"]
        self.assertEqual(
            clt["states"]["Post-merge Checklists"], CLT_CHECKLISTS_UUID)
        self.assertIn("Post-merge Checklists", clt["state_groups"])
        self.assertEqual(clt["state_groups"]["Post-merge Checklists"], "started")
        for key in clt["states"]:
            self.assertIn(key, clt["state_groups"])


class TestMarkerReadCommand(unittest.TestCase):
    """gh rejects --slurp combined with --jq (VHS-84). No skill may print that command."""

    def test_no_gh_api_line_combines_slurp_and_jq(self):
        offenders = []
        for path in sorted((REPO_ROOT / "skills").rglob("SKILL.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            for number, line in enumerate(lines, 1):
                if "gh api" in line and "--slurp" in line and "--jq" in line:
                    offenders.append("{}:{}".format(path.relative_to(REPO_ROOT), number))
        self.assertEqual(offenders, [])

    def test_marker_readers_use_slurp(self):
        # VHS-91: the comment read lives in land_check.py, so the pin moves there.
        mod = load_script(SCRIPT, "spec_land_check_argv")
        argv = mod._comments_argv(7)
        self.assertEqual(
            argv, ["gh", "api", "--paginate", "--slurp", "repos/{owner}/{repo}/issues/7/comments"])
        self.assertNotIn("--jq", argv)

    def _skill_lines(self, predicate):
        offenders = []
        for path in sorted((REPO_ROOT / "skills").rglob("SKILL.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            for number, line in enumerate(lines, 1):
                if predicate(line):
                    offenders.append("{}:{}".format(path.relative_to(REPO_ROOT), number))
        return offenders

    def test_no_skill_carries_the_comment_read(self):
        # Regression for VHS-91: the marker mechanism is the script's, not prose.
        self.assertEqual(self._skill_lines(lambda l: "gh api --paginate --slurp" in l), [])

    def test_no_skill_carries_the_fingerprint_command(self):
        # Regression for VHS-91: verdict_marker.py fingerprint is the one copy.
        self.assertEqual(
            self._skill_lines(lambda l: "tr -d" in l and "Follow-up:" in l), [])


def comment(cid, body, created="2026-10-27T10:00:00Z"):
    return {"id": cid, "body": body, "created_at": created}


def pages(*comments):
    return json.dumps([list(comments)]).encode("utf-8")


class FakeCmd:
    """_cmd stand-in. Routes match an argv prefix; a list of responses is
    consumed in order and its last entry repeats. A response is
    (code, stdout, stderr) or a callable taking (argv, input)."""

    def __init__(self, **overrides):
        self.calls = []
        self.bodies = []
        self.routes = {
            ("gh", "pr", "view"): [(0, json.dumps(
                {"headRefOid": HEAD, "baseRefOid": BASE}).encode(), b"")],
            ("git", "rev-parse"): [(0, (HEAD + "\n").encode(), b"")],
            ("git", "cat-file"): [(0, b"", b"")],
            ("git", "fetch"): [(0, b"", b"")],
            ("git", "diff"): [(0, b"diff --git a/x b/x\n", b"")],
            ("git", "patch-id"): [(0, (PATCH + " " + "f" * 40 + "\n").encode(), b"")],
            ("gh", "api"): [(0, pages(), b"")],
            ("gh", "pr", "comment"): [self._comment_ok],
        }
        for key, value in overrides.items():
            self.routes[tuple(key.split())] = value if isinstance(value, list) else [value]

    def _comment_ok(self, argv, _input):
        self.bodies.append(Path(argv[argv.index("--body-file") + 1]).read_bytes())
        return 0, b"", b""

    def __call__(self, argv, input=None):
        self.calls.append((list(argv), input))
        for prefix, responses in self.routes.items():
            if tuple(argv[:len(prefix)]) == prefix:
                response = responses.pop(0) if len(responses) > 1 else responses[0]
                return response(argv, input) if callable(response) else response
        raise AssertionError("unexpected command {}".format(argv))

    def called(self, *prefix):
        return [call for call in self.calls if tuple(call[0][:len(prefix)]) == prefix]


class RaisingStdin:
    class _Buffer:
        def read(self, *_):
            raise AssertionError("stdin was read")

    buffer = _Buffer()

    def read(self, *_):
        raise AssertionError("stdin was read")


class TestLatestAndPost(unittest.TestCase):
    """VHS-91: land_check.py latest and post. _cmd and _sleep are patched."""

    @classmethod
    def setUpClass(cls):
        cls.mod = load_script(SCRIPT, "spec_land_check_post_under_test")

    def run_cmd(self, argv, fake, stdin=None):
        sleep = mock.Mock()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(self.mod, "_cmd", fake), \
                mock.patch.object(self.mod, "_sleep", sleep), \
                mock.patch.object(sys, "stdin", stdin or RaisingStdin()):
            code = self.mod.main(list(argv))
        return code, out.getvalue(), err.getvalue(), sleep

    def post(self, fake, *extra, review="passed"):
        return self.run_cmd(["post", "7", "--review", review, *extra], fake)

    # 1
    def test_latest_picks_the_latest_marker(self):
        older = comment(1, marker(head=OTHER), "2026-10-27T09:00:00Z")
        newer = comment(2, marker(), "2026-10-27T10:00:00Z")
        mention = comment(9, "see <!-- vigil-spec-land", "2026-10-27T11:00:00Z")
        fake = FakeCmd(**{"gh api": (0, pages(newer, older, mention), b"")})
        code, out, err, _ = self.run_cmd(["latest", "7"], fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "id=2 head={} base={} patch-id={} review=passed\n".format(
            HEAD, BASE, PATCH))
        tie_low = comment(3, marker(head=OTHER), "2026-10-27T10:00:00+00:00")
        tie_high = comment(4, marker(), "2026-10-27T10:00:00Z")
        fake = FakeCmd(**{"gh api": (0, json.dumps([[tie_high], [tie_low]]).encode(), b"")})
        code, out, err, _ = self.run_cmd(["latest", "7"], fake)
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("id=4 head=" + HEAD), out)

    # 2
    def test_latest_no_marker(self):
        for raw in (b"[]", b"[[]]", pages(comment(1, "LGTM"))):
            with self.subTest(raw=raw):
                code, out, err, _ = self.run_cmd(
                    ["latest", "7"], FakeCmd(**{"gh api": (0, raw, b"")}))
                self.assertEqual(code, 1, err)
                self.assertEqual(out, "no marker\n")

    # 3
    def test_latest_malformed(self):
        body = marker(review="maybe")
        fake = FakeCmd(**{"gh api": (0, pages(comment(5, body)), b"")})
        code, out, err, _ = self.run_cmd(["latest", "7"], fake)
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "malformed marker id=5\n" + body + "\n")

    # 4
    def test_latest_read_failures_exit_4(self):
        bad = {
            "gh exits non-zero": (1, b"", b"HTTP 502"),
            "not JSON": (0, b"<html>", b""),
            "non-array page": (0, b"[{}]", b""),
            "missing id": (0, json.dumps([[{"body": "x", "created_at": "t"}]]).encode(), b""),
            "missing body": (0, json.dumps([[{"id": 1, "created_at": "t"}]]).encode(), b""),
            "missing created_at": (0, json.dumps([[{"id": 1, "body": "x"}]]).encode(), b""),
            "element not object": (0, b"[[1]]", b""),
            "null body": (0, json.dumps([[{"id": 1, "body": None, "created_at": "t"}]]).encode(), b""),
            "string id": (0, pages(comment("1", "x")), b""),
            "bool id": (0, pages(comment(True, "x")), b""),
            "int created_at": (0, pages(comment(1, "x", 5)), b""),
            "bad timestamp": (0, pages(comment(1, marker(), "yesterday")), b""),
            "no timezone": (0, pages(comment(1, marker(), "2026-10-27T10:00:00")), b""),
            "not UTF-8": (0, b"[[\xff]]", b""),
        }
        for name, response in bad.items():
            with self.subTest(case=name):
                code, out, err, _ = self.run_cmd(
                    ["latest", "7"], FakeCmd(**{"gh api": response}))
                self.assertEqual(code, 4, err)
                self.assertEqual(out, "")

    # 5
    def test_post_happy_path(self):
        fake = FakeCmd()
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "SHA marker: posted (head {}, review passed)\n".format(HEAD))
        (argv, _), = fake.called("gh", "pr", "comment")
        self.assertEqual(argv[:4], ["gh", "pr", "comment", "7"])
        self.assertEqual(argv[4], "--body-file")
        self.assertFalse(Path(argv[5]).exists())
        body = fake.bodies[0]
        self.assertEqual(body, (marker() + "\n").encode("utf-8"))
        self.assertFalse(body.startswith(b"\xef\xbb\xbf"))
        self.assertEqual(self.mod._parse_marker(body.decode("utf-8")),
                         (0, "head={} base={} patch-id={} review=passed".format(HEAD, BASE, PATCH)))
        (diff_argv, _), = fake.called("git", "diff")
        self.assertEqual(diff_argv, ["git", "diff", "{}...{}".format(BASE, HEAD)])

    # 6
    def test_post_same_head_is_current(self):
        # Regression for VHS-96: a stronger token on the same head posts a new marker.
        fake = FakeCmd(**{"gh api": (0, pages(comment(1, marker(review="skipped"))), b"")})
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("SHA marker: posted"), out)
        self.assertEqual(len(fake.called("gh", "pr", "comment")), 1)
        self.assertIn(b"review: passed", fake.bodies[0])

    def test_post_same_head_equal_is_current(self):
        fake = FakeCmd(**{"gh api": (0, pages(comment(1, marker(review="passed"))), b"")})
        code, out, err, _ = self.post(fake, review="passed")
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "SHA marker: already current (head {})\n".format(HEAD))
        self.assertEqual(fake.called("gh", "pr", "comment"), [])

    def test_post_same_head_weaker_is_current(self):
        for review in ("not-run", "inconclusive"):
            with self.subTest(review=review):
                fake = FakeCmd(**{"gh api": (0, pages(comment(1, marker(review="passed"))), b"")})
                code, out, err, _ = self.post(fake, review=review)
                self.assertEqual(code, 0, err)
                self.assertEqual(out, "SHA marker: already current (head {})\n".format(HEAD))
                self.assertEqual(fake.called("gh", "pr", "comment"), [])

    def test_post_same_head_rank_order(self):
        steps = (("skipped", "not-run"), ("inconclusive", "skipped"), ("passed", "inconclusive"))
        for new, old in steps:
            with self.subTest(new=new, old=old):
                fake = FakeCmd(**{"gh api": (0, pages(comment(1, marker(review=old))), b"")})
                code, out, err, _ = self.post(fake, review=new)
                self.assertEqual(code, 0, err)
                self.assertTrue(out.startswith("SHA marker: posted"), out)
                self.assertEqual(len(fake.called("gh", "pr", "comment")), 1)
                self.assertIn(("review: " + new).encode("ascii"), fake.bodies[0])

    # 7
    def test_post_no_valid_head(self):
        old = marker(head="xyz")
        for no_push in (True, False):
            with self.subTest(no_push=no_push):
                fake = FakeCmd(**{"gh api": (0, pages(comment(8, old)), b"")})
                code, out, err, _ = self.post(fake, *(["--no-push"] if no_push else []))
                self.assertIn("latest marker id=8 (malformed):\n" + old, err)
                if no_push:
                    self.assertEqual(code, 1, err)
                    self.assertEqual(out.splitlines()[0],
                                     "SHA marker: NOT posted (latest marker has no valid head (no-push))")
                    self.assertEqual(fake.called("gh", "pr", "comment"), [])
                else:
                    self.assertEqual(code, 0, err)
                    self.assertTrue(out.startswith("SHA marker: posted"), out)

    # 8
    def test_post_head_mismatch(self):
        view_other = (0, json.dumps({"headRefOid": OTHER, "baseRefOid": BASE}).encode(), b"")
        fake = FakeCmd(**{"gh pr view": [view_other, view_other]})
        code, out, err, sleep = self.post(fake)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "SHA marker: NOT posted (head mismatch {} != {})\n".format(HEAD, OTHER))
        sleep.assert_called_once_with(5)
        self.assertEqual(fake.called("git", "diff"), [])
        self.assertEqual(fake.called("gh", "pr", "comment"), [])

        new_head = "4" * 40
        view_new = (0, json.dumps({"headRefOid": new_head, "baseRefOid": BASE}).encode(), b"")
        fake = FakeCmd(**{"gh pr view": [view_other, view_new],
                          "git rev-parse": (0, (new_head + "\n").encode(), b"")})
        code, out, err, sleep = self.post(fake)
        self.assertEqual(code, 0, err)
        (diff_argv, _), = fake.called("git", "diff")
        self.assertEqual(diff_argv[2], "{}...{}".format(BASE, new_head))
        self.assertIn(("head: " + new_head).encode(), fake.bodies[0])

        fake = FakeCmd(**{"gh pr view": [view_other, (1, b"", b"boom")]})
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "SHA marker: NOT posted (gh pr view failed)\n")

    # 9
    def test_post_base_missing(self):
        fake = FakeCmd(**{"git cat-file": [(1, b"", b""), (0, b"", b"")]})
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(len(fake.called("git", "fetch", "origin")), 1)
        fake = FakeCmd(**{"git cat-file": (1, b"", b"")})
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "SHA marker: NOT posted (base object missing)\n")

    # 10
    def test_post_bad_patch_id(self):
        cases = {
            "diff fails": {"git diff": (128, b"", b"bad revision")},
            "second line": {"git patch-id": (0, (PATCH + " x\n" + PATCH + " y\n").encode(), b"")},
            "missing field": {"git patch-id": (0, b"\n", b"")},
            "uppercase": {"git patch-id": (0, ("A" * 40 + " x\n").encode(), b"")},
        }
        for name, routes in cases.items():
            with self.subTest(case=name):
                fake = FakeCmd(**routes)
                code, out, err, _ = self.post(fake)
                self.assertEqual(code, 1, err)
                self.assertEqual(out, "SHA marker: NOT posted (bad patch-id)\n")
                self.assertEqual(fake.called("gh", "pr", "comment"), [])

    # 11
    def test_post_retries_once(self):
        fake = FakeCmd()
        fake.routes[("gh", "pr", "comment")] = [(1, b"", b"502"), fake._comment_ok]
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 0, err)
        self.assertEqual(len(fake.called("gh", "pr", "comment")), 2)

        fake = FakeCmd(**{"gh pr comment": (1, b"", b"502")})
        code, out, err, _ = self.post(fake)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "SHA marker: NOT posted (gh pr comment failed twice)\n" + marker() + "\n")
        calls = fake.called("gh", "pr", "comment")
        self.assertEqual(len(calls), 2)
        self.assertFalse(Path(calls[0][0][5]).exists())

    # 12
    def test_post_bad_review_token(self):
        with self.assertRaises(SystemExit) as caught:
            self.post(FakeCmd(), review="bogus")
        self.assertEqual(caught.exception.code, 2)

    # 13
    def test_latest_and_post_never_read_stdin(self):
        code, _, err, _ = self.run_cmd(["latest", "7"], FakeCmd(), RaisingStdin())
        self.assertEqual(code, 1, err)
        code, _, err, _ = self.run_cmd(["post", "7", "--review", "skipped"], FakeCmd(), RaisingStdin())
        self.assertEqual(code, 0, err)

    # 15
    def test_post_forwards_diff_bytes(self):
        raw = b"diff --git a/x b/x\r\n+caf\xe9\r\n"
        fake = FakeCmd(**{"git diff": (0, raw, b"")})
        code, _, err, _ = self.post(fake)
        self.assertEqual(code, 0, err)
        (_, forwarded), = fake.called("git", "patch-id")
        self.assertEqual(forwarded, raw)

    # 16
    def test_latest_non_ascii_bodies(self):
        chatter = comment(1, "Looks good \U0001f680 — merci, ça marche", "2026-10-27T11:00:00Z")
        fake = FakeCmd(**{"gh api": (0, pages(comment(2, marker()), chatter), b"")})
        code, out, err, _ = self.run_cmd(["latest", "7"], fake)
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("id=2 "), out)

    # 17
    def test_post_refusals_before_the_post(self):
        fake = FakeCmd(**{"gh pr view": (1, b"", b"no auth")})
        code, out, _, _ = self.post(fake)
        self.assertEqual((code, out), (1, "SHA marker: NOT posted (gh pr view failed)\n"))
        self.assertEqual(fake.called("gh", "pr", "comment"), [])
        fake = FakeCmd(**{"gh api": (1, b"", b"HTTP 500")})
        code, out, _, _ = self.post(fake)
        self.assertEqual(code, 1)
        self.assertEqual(out, "SHA marker: NOT posted (comment read failed)\n" + marker() + "\n")
        self.assertEqual(fake.called("gh", "pr", "comment"), [])

    # 18
    def test_post_malformed_same_head_posts(self):
        old = marker(review="maybe")
        for extra in ((), ("--no-push",)):
            with self.subTest(extra=extra):
                fake = FakeCmd(**{"gh api": (0, pages(comment(3, old)), b"")})
                code, out, err, _ = self.post(fake, *extra)
                self.assertEqual(code, 0, err)
                self.assertEqual(len(fake.called("gh", "pr", "comment")), 1)

    # 19
    def test_post_failed_temp_delete_warns(self):
        fake = FakeCmd()
        with mock.patch.object(self.mod.os, "remove", side_effect=OSError("locked")):
            code, out, err, _ = self.post(fake)
        (argv, _), = fake.called("gh", "pr", "comment")
        Path(argv[5]).unlink()
        self.assertEqual(code, 0, err)
        self.assertIn("warning: temp body file not removed", err)

    # 20
    def test_post_failed_rev_parse(self):
        fake = FakeCmd(**{"git rev-parse": (128, b"HEAD\n", b"fatal: not a git repository")})
        code, out, err, sleep = self.post(fake)
        self.assertEqual(code, 1, err)
        self.assertEqual(out, "SHA marker: NOT posted (head mismatch none != {})\n".format(HEAD))
        sleep.assert_not_called()

    def test_cmd_turns_spawn_oserror_into_nonzero(self):
        with mock.patch.object(self.mod.subprocess, "run", side_effect=FileNotFoundError("gh")):
            code, out, _ = self.mod._cmd(["gh", "pr", "view", "7"])
            self.assertNotEqual(code, 0)
            self.assertEqual(out, b"")
            buf_out, buf_err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                rc = self.mod.main(["post", "7", "--review", "passed"])
        self.assertEqual(rc, 1)
        self.assertEqual(buf_out.getvalue(), "SHA marker: NOT posted (gh pr view failed)\n")

    def test_cmd_real_bytes_round_trip(self):
        raw = b"a\r\nb\xff\n"
        code, out, _ = self.mod._cmd(
            [sys.executable, "-c", "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())"],
            input=raw)
        self.assertEqual((code, out), (0, raw))


# --- VHS-97: preflight, wiki, cleanup. Every command is stubbed. ----------

LANDED = "4" * 40
PARENT = "5" * 40
BRANCH = "feat/vhs-97-script"
AGENTS_TEXT = (
    "# Agents\n\n## Wiki\n\nSlug: proj\nLog: off\nFilemap file: elsewhere.md\n\n"
    "## Post-land command\n\npython sync.py install\n")
WRITE_PREFIXES = (("git", "push"), ("git", "branch"), ("git", "worktree", "remove"),
                  ("git", "merge", "--ff-only"), ("gh", "pr", "comment"))


def ok(text=""):
    return 0, text.encode("utf-8"), b""


class Router:
    """_cmd stand-in for the VHS-97 commands. `git -C <path>` is matched
    without the -C pair; the longest matching prefix wins."""

    def __init__(self, routes):
        self.calls = []
        self.routes = {key: value if isinstance(value, list) else [value]
                       for key, value in routes.items()}

    @staticmethod
    def norm(argv):
        argv = list(argv)
        return ["git"] + argv[3:] if argv[:2] == ["git", "-C"] else argv

    def __call__(self, argv, input=None):
        self.calls.append((list(argv), input))
        plain = self.norm(argv)
        for prefix in sorted(self.routes, key=len, reverse=True):
            if tuple(plain[:len(prefix)]) == prefix:
                responses = self.routes[prefix]
                response = responses.pop(0) if len(responses) > 1 else responses[0]
                return response(argv, input) if callable(response) else response
        raise AssertionError("unexpected command {}".format(argv))

    def ran(self, *prefix):
        return [argv for argv, _ in self.calls if tuple(self.norm(argv)[:len(prefix)]) == prefix]


class TestPreflightWikiCleanup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mod = load_script(SCRIPT, "spec_land_check_vhs97_under_test")

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).as_posix()
        self.main = self.tmp + "/main"
        self.linked = self.tmp + "/wt"
        self.wiki = self.tmp + "/wiki"
        self.config = self.tmp + "/config"
        for path in (self.main, self.wiki + "/projects/proj",
                     self.config + "/skills/ship-spec", self.config + "/skills/spec-close/scripts"):
            os.makedirs(path)
        Path(self.main, "CLAUDE.md").write_text(
            "- **Wiki:** `{}` (the wiki)\n".format(self.wiki), encoding="utf-8")
        Path(self.config, "skills/ship-spec/states.json").write_text(json.dumps({"VHS": {
            "project_id": "proj-uuid",
            "states": {"Done": "done-uuid", "Post-merge Checklists": "pmc-uuid"},
            "state_groups": {"Done": "completed", "Post-merge Checklists": "started"}}}),
            encoding="utf-8")
        Path(self.config, "skills/spec-close/scripts/prepend_log_entry.py").write_text("", encoding="utf-8")
        self.env = {"CLAUDE_CONFIG_DIR": self.config}

    def tearDown(self):
        self._tmp.cleanup()

    def pr_json(self, **over):
        data = {"state": "MERGED", "mergeCommit": {"oid": LANDED},
                "mergedAt": "2026-11-04T00:00:00Z", "baseRefOid": BASE, "headRefOid": HEAD,
                "headRefName": BRANCH, "title": "feat(vhs-97): script it",
                "body": "## Test plan\n- [x] tests\n- [ ] Spec verdict: green\n- [ ] Post-merge verification\n",
                "commits": [{}], "url": "https://github.com/o/r/pull/7"}
        data.update(over)
        return json.dumps(data)

    def porcelain(self, main_branch="main", linked=1):
        text = "worktree {}\nHEAD {}\nbranch refs/heads/{}\n\n".format(self.main, LANDED, main_branch)
        for index in range(linked):
            text += "worktree {}{}\nHEAD {}\nbranch refs/heads/{}\n\n".format(
                self.linked, index or "", HEAD, BRANCH)
        return text

    def routes(self, over=None):
        routes = {
            ("gh", "repo", "view"): ok(json.dumps({"owner": {"login": "o"}, "name": "r"})),
            ("gh", "pr", "view", "7"): ok(self.pr_json()),
            ("git", "fetch"): ok(),
            ("gh", "api"): (0, pages(comment(1, marker(patch=PATCH))), b""),
            ("git", "diff", LANDED + "^1", LANDED): ok("diff --git a/x b/x\n"),
            ("git", "patch-id"): ok(PATCH + " " + "f" * 40 + "\n"),
            ("git", "rev-list", "--parents"): ok(LANDED + " " + PARENT + "\n"),
            ("git", "cat-file"): ok(),
            ("git", "cat-file", "-e", LANDED + ":CLAUDE.md"): (128, b"", b"missing"),
            ("git", "show", LANDED + ":AGENTS.md"): ok(AGENTS_TEXT),
            ("git", "merge-base"): ok(),
            ("git", "rev-list", "--reverse"): ok(),
            ("git", "diff", "--name-only"): ok("skills/x.md\n"),
            ("git", "worktree", "list"): ok(self.porcelain()),
            ("git", "symbolic-ref"): ok("refs/remotes/origin/main\n"),
            ("git", "status"): ok(),
        }
        routes.update(over or {})
        return Router(routes)

    def run_main(self, argv, router, shell=None):
        out, err = io.StringIO(), io.StringIO()
        shell = shell or mock.Mock(return_value=0)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(self.mod, "_cmd", router), \
                mock.patch.object(self.mod, "_shell", shell), \
                mock.patch.dict(os.environ, self.env), \
                mock.patch.object(sys, "stdin", RaisingStdin()):
            code = self.mod.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def preflight(self, router, *argv):
        before = sorted(str(p) for p in Path(self.tmp).rglob("*"))
        code, out, err = self.run_main(["preflight", *argv], router)
        self.assertEqual(sorted(str(p) for p in Path(self.tmp).rglob("*")), before,
                         "preflight wrote a file")
        for prefix in WRITE_PREFIXES:
            self.assertEqual(router.ran(*prefix), [], prefix)
        state = None
        for line in out.splitlines():
            if line.startswith("spec_land_state="):
                state = json.loads(line[len("spec_land_state="):])
        return code, out, err, state

    def state_file(self, state):
        path = Path(self.tmp, "state.json")
        path.write_text(json.dumps(state), encoding="utf-8")
        return str(path)

    # Preflight -----------------------------------------------------------

    def test_preflight_clean_match(self):
        router = self.routes()
        code, out, err, state = self.preflight(router, "7")
        self.assertEqual(code, 0, out + err)
        self.assertIn("SHA: match (match single) review=passed", out)
        self.assertIn("Reply yes to land VHS-97.", out)
        self.assertEqual(len(router.ran("git", "fetch")), 2)
        self.assertEqual(state["version"], 1)
        self.assertEqual(state["verification"]["status"], "match")
        self.assertEqual(state["verification"]["diff_base"], LANDED + "^1")
        self.assertEqual(state["plane"]["target"], "Post-merge Checklists")
        self.assertEqual(state["checklist"], ["- [ ] Post-merge verification"])
        self.assertEqual(state["worktrees"], [self.linked])
        self.assertEqual(state["fast_forward"], "will run")

    def test_preflight_no_marker_skips_verification(self):
        router = self.routes({("gh", "api"): (0, pages(comment(1, "LGTM")), b"")})
        code, out, _, state = self.preflight(router, "7")
        self.assertEqual(code, 0)
        self.assertIn("no marker - verification skipped", out)
        self.assertEqual(state["verification"]["status"], "skipped")
        self.assertEqual(router.ran("git", "patch-id"), [])
        self.assertNotIn("may omit earlier rebased commits", out)

    def test_preflight_no_marker_multi_commit_shows_filemap_caveat(self):
        router = self.routes({("gh", "api"): (0, pages(comment(1, "LGTM")), b""),
                              ("gh", "pr", "view", "7"): ok(self.pr_json(commits=[{}, {}]))})
        code, out, _, _ = self.preflight(router, "7")
        self.assertEqual(code, 0)
        self.assertIn("may omit earlier rebased commits", out)

    def test_preflight_warnings_allow_land_anyway(self):
        overlap_walk = {
            ("git", "rev-list", "--reverse"): ok(PARENT + "\n"),
            ("git", "diff-tree"): ok("skills/x.md\n"),
            ("git", "log"): ok("other change\n"),
        }
        cases = {
            "malformed": {("gh", "api"): (0, pages(comment(1, marker(review="maybe"))), b"")},
            "head": {("gh", "api"): (0, pages(comment(1, marker(head=OTHER))), b"")},
            "patch-id": {("git", "patch-id"): ok(OTHER + "\n")},
            "overlap": overlap_walk,
        }
        for name, over in cases.items():
            with self.subTest(case=name):
                router = self.routes(over)
                code, out, _, state = self.preflight(router, "7")
                self.assertEqual(code, 0, out)
                self.assertIn("SHA: WARNING", out)
                self.assertIn("Reply land anyway to land VHS-97", out)
                self.assertEqual(state["verification"]["status"], "warning")
                self.assertEqual(state["verification"]["diff_base"], LANDED + "^1")
                if name in ("malformed", "head"):
                    self.assertEqual(router.ran("git", "patch-id"), [])

    def test_preflight_range_match_uses_range_base(self):
        pr = self.pr_json(commits=[{}, {}, {}])
        patches = [ok(OTHER + "\n"), ok(PATCH + "\n")]
        router = self.routes({("gh", "pr", "view", "7"): ok(pr), ("git", "patch-id"): patches,
                                ("git", "diff", LANDED + "~3", LANDED): ok("d\n")})
        code, out, _, state = self.preflight(router, "7")
        self.assertEqual(code, 0, out)
        self.assertEqual(state["verification"]["kind"], "match range")
        self.assertEqual(state["verification"]["diff_base"], LANDED + "~3")

    def test_preflight_policy_stops(self):
        cases = {
            "not merged": {("gh", "pr", "view", "7"): ok(self.pr_json(state="OPEN"))},
            "fetch": {("git", "fetch"): (128, b"", b"Permission denied (publickey).")},
            "comment read": {("gh", "api"): (1, b"", b"HTTP 502")},
            "ancestry": {("git", "merge-base"): (1, b"", b"")},
        }
        for name, over in cases.items():
            with self.subTest(case=name):
                code, out, _, state = self.preflight(self.routes(over), "7")
                self.assertEqual(code, 1, out)
                self.assertTrue(out.startswith("HALT: "), out)
                self.assertNotIn("no marker", out)
                self.assertIsNone(state)

    def test_preflight_pr_url_must_match_repo(self):
        code, out, _, _ = self.preflight(self.routes(), "https://github.com/x/y/pull/7")
        self.assertEqual(code, 1)
        self.assertIn("PR URL is not for o/r", out)
        code, out, _, state = self.preflight(self.routes(), "https://github.com/O/R/pull/7")
        self.assertEqual(code, 0, out)
        self.assertEqual(state["pr"]["number"], 7)

    def test_preflight_spec_path_pages_past_100(self):
        rows = [{"number": n, "title": "ABC-{}".format(n), "headRefName": "x"} for n in range(150)]
        rows.append({"number": 7, "title": "feat: thing", "headRefName": "feat/vhs-97-x"})
        router = self.routes({("gh", "pr", "view", "--json"): (1, b"", b"no pr"),
                                ("gh", "pr", "list"): ok(json.dumps(rows))})
        code, out, _, state = self.preflight(router, "/c/repo/docs/specs/TODO/VHS-97.spec.md")
        self.assertEqual(code, 0, out)
        self.assertEqual(state["ticket_source"], "spec path")
        self.assertIn("10000", router.ran("gh", "pr", "list")[0])
        router = self.routes({("gh", "pr", "view", "--json"): (1, b"", b"no pr"),
                                ("gh", "pr", "list"): ok("[]")})
        code, out, _, _ = self.preflight(router, "docs/specs/TODO/VHS-97.spec.md")
        self.assertEqual(code, 1)
        self.assertIn("pass the PR number", out)

    def test_preflight_ambiguous_ticket_then_retry(self):
        pr = self.pr_json(title="fix(vhs-12): other")
        code, out, _, state = self.preflight(self.routes({("gh", "pr", "view", "7"): ok(pr)}), "7")
        self.assertEqual(code, 4)
        self.assertIn("VHS-97, VHS-12", out)
        self.assertIsNone(state)
        code, out, _, state = self.preflight(
            self.routes({("gh", "pr", "view", "7"): ok(pr)}), "7", "--ticket", "vhs-12")
        self.assertEqual(code, 0, out)
        self.assertEqual((state["ticket"], state["ticket_source"]), ("VHS-12", "operator"))

    def test_preflight_instructions(self):
        # Removed keys are ignored; CLAUDE.md wins the wiki path; AGENTS.md supplies the rest.
        code, out, _, state = self.preflight(self.routes(), "7")
        self.assertEqual(code, 0, out)
        self.assertEqual(state["wiki"]["path"], self.wiki)
        self.assertEqual(state["wiki"]["slug"], "proj")
        self.assertEqual(state["post_land"]["command"], "python sync.py install")
        self.assertNotIn("elsewhere.md", out)
        two_lines = AGENTS_TEXT.replace("python sync.py install\n", "one\ntwo\n")
        router = self.routes({("git", "show", LANDED + ":AGENTS.md"): ok(two_lines)})
        _, out, _, state = self.preflight(router, "7")
        self.assertIsNone(state["post_land"]["command"])
        self.assertIn("2 non-blank lines - skipped", out)
        # Regression for VHS-97: cloud names its wiki only by Path: under ## Wiki.
        os.makedirs(self.tmp + "/notes")
        path_only = "## Wiki\n\nPath: {}/notes\n".format(self.tmp)
        self.assertEqual(self.mod._wiki_path(path_only), self.tmp + "/notes")

    def test_norm_path_accepts_both_forms(self):
        with mock.patch.object(self.mod.os, "name", "nt"):
            self.assertEqual(self.mod._norm_path("/c/Users/x"), "C:/Users/x")
            self.assertEqual(self.mod._norm_path("C:\\Users\\x"), "C:/Users/x")
            self.assertEqual(self.mod._norm_path("C:/Users/x"), "C:/Users/x")

    def test_checklist_and_hash(self):
        unchecked = self.mod._checklist(
            "## Test plan\r\n- [ ] Review gate: x\n- [ ] Post-merge verification\n## Next\n- [ ] no\n")
        self.assertEqual(unchecked, ["- [ ] Post-merge verification"])
        with mock.patch.dict(os.environ, self.env):
            plane = self.mod._plane("VHS-97", 7, unchecked)
        self.assertEqual(plane["state_id"], "pmc-uuid")
        self.assertTrue(plane["comment"].endswith(
            "spec-land:checklist PR #7 9c4b924006cf6d5f7ec1808f1347d5863786a708d1542a5cc5676b5240be80f9"))

    # Wiki ----------------------------------------------------------------

    def preflight_state(self, over=None):
        code, out, _, state = self.preflight(self.routes(over), "7")
        self.assertEqual(code, 0, out)
        return state

    def test_wiki_log_and_filemap(self):
        state = self.preflight_state()
        filemap = Path(self.wiki, "projects/proj/filemap.md")
        filemap.write_text(
            "# Filemap\n\n### `gone.py`\n- gone\n\n### `old.py`\n- body\n\n## Next\n", encoding="utf-8")
        Path(self.wiki, "log.md").write_text("## [2099-01-01] newer\n", encoding="utf-8")
        router = self.routes({
            (sys.executable,): ok("prepend_log_entry_outcome=prepended\n"),
            ("git", "diff", "--name-status"): ok(
                "D\tgone.py\nR100\told.py\tnew.py\nA\ttests/test_new.py\nM\tkeep.py\n")})
        code, out, _ = self.run_main(["wiki", "--state", self.state_file(state)], router)
        self.assertEqual(code, 0, out)
        self.assertIn("log.md: prepended", out)
        argv, entry = router.calls[0]
        self.assertEqual(argv[-2:], ["--guard", "merge | VHS \u2014 VHS-97 PR #7:"])
        self.assertTrue(entry.decode("utf-8").startswith("## [2099-01-01] merge | VHS \u2014 VHS-97 PR #7:"))
        text = filemap.read_text(encoding="utf-8")
        self.assertNotIn("gone.py", text)
        self.assertIn("### `new.py`\n- body", text)
        self.assertIn("### `tests/test_new.py`\n- **Purpose:** Test added in PR #7.", text)
        self.assertIn("filemap: M keep.py: not filemap-relevant", out)

    def test_wiki_failures_reported(self):
        state = self.preflight_state()
        Path(self.wiki, "projects/proj/filemap.md").write_text("# F\n", encoding="utf-8")
        router = self.routes({(sys.executable,): (1, b"", b""),
                                ("git", "diff", "--name-status"): (128, b"", b"bad revision")})
        code, out, _ = self.run_main(["wiki", "--state", self.state_file(state)], router)
        self.assertEqual(code, 1)
        self.assertIn("log.md: entry already present - skipped", out)
        self.assertIn("filemap: NOT written", out)

    def test_state_file_must_be_valid(self):
        for body in ("not json", json.dumps({"version": 2}), json.dumps({"version": 1})):
            with self.subTest(body=body):
                path = Path(self.tmp, "bad.json")
                path.write_text(body, encoding="utf-8")
                router = self.routes()
                code, out, _ = self.run_main(["cleanup", "--state", str(path)], router)
                self.assertEqual(code, 1)
                self.assertTrue(out.startswith("HALT: "), out)
                self.assertEqual(router.calls, [])

    # Cleanup -------------------------------------------------------------

    def cleanup_routes(self, over=None):
        routes = {
            ("git", "worktree", "list"): ok(self.porcelain()),
            ("git", "status"): ok(),
            ("git", "worktree", "remove"): ok(),
            ("git", "rev-parse", "--verify"): ok(HEAD + "\n"),
            ("git", "rev-list", "--count"): ok("0\n"),
            ("git", "branch", "-d"): (1, b"", b"not fully merged"),
            ("git", "branch", "-D"): ok(),
            ("git", "ls-remote"): ok("{}\trefs/heads/{}\n".format(HEAD, BRANCH)),
            ("git", "push"): ok(),
            ("git", "merge", "--ff-only"): ok(),
            ("git", "merge-base", "--is-ancestor"): ok(),
        }
        routes.update(over or {})
        return Router(routes)

    def test_cleanup_happy_path(self):
        state = self.preflight_state()
        shell = mock.Mock(return_value=0)
        router = self.cleanup_routes()
        code, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router, shell)
        self.assertEqual(code, 0, out)
        self.assertIn("local branch: deleted (-D", out)
        push = router.ran("git", "push")[0]
        self.assertIn("--force-with-lease=refs/heads/{}:{}".format(BRANCH, HEAD), push)
        self.assertNotIn("--force", [a for a in push if a == "--force"])
        self.assertNotIn("--force", router.ran("git", "worktree", "remove")[0])
        shell.assert_called_once_with("python sync.py install", self.main)

    def test_cleanup_dirty_worktree_keeps_branches(self):
        state = self.preflight_state()
        status = lambda argv, _: ok(" M x\n") if argv[2] == self.linked else ok()
        router = self.cleanup_routes({("git", "status"): status})
        code, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router)
        self.assertIn("worktree: dirty - kept", out)
        for prefix in (("git", "worktree", "remove"), ("git", "branch"), ("git", "push")):
            self.assertEqual(router.ran(*prefix), [], prefix)
        self.assertIn("fast-forward: done", out)

    def test_cleanup_several_checkouts_continue(self):
        state = self.preflight_state()
        router = self.cleanup_routes({("git", "worktree", "list"): ok(self.porcelain(linked=2))})
        code, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router)
        self.assertIn("2 linked checkouts kept", out)
        self.assertEqual(router.ran("git", "branch"), [])
        self.assertEqual(router.ran("git", "push"), [])
        self.assertEqual(len(router.ran("git", "merge", "--ff-only")), 1)

    def test_cleanup_force_delete_needs_match_and_tip(self):
        warned = self.preflight_state({("git", "patch-id"): ok(OTHER + "\n")})
        router = self.cleanup_routes()
        _, out, _ = self.run_main(["cleanup", "--state", self.state_file(warned)], router)
        self.assertEqual(router.ran("git", "branch", "-D"), [])
        self.assertIn("-D needs a SHA match", out)
        matched = self.preflight_state()
        for over, phrase in (({("git", "rev-list", "--count"): ok("2\n")}, "2 commits not in the PR head"),
                             ({("git", "rev-list", "--count"): (128, b"", b"bad")}, "rev-list failed")):
            with self.subTest(phrase=phrase):
                router = self.cleanup_routes(over)
                _, out, _ = self.run_main(["cleanup", "--state", self.state_file(matched)], router)
                self.assertEqual(router.ran("git", "branch"), [])
                self.assertIn(phrase, out)
        # A matched SHA with a local tip that is not the PR head never reaches -D.
        router = self.cleanup_routes({("git", "rev-parse", "--verify"): ok(OTHER + "\n")})
        _, out, _ = self.run_main(["cleanup", "--state", self.state_file(matched)], router)
        self.assertEqual(router.ran("git", "branch", "-D"), [])
        self.assertIn("-D needs a SHA match", out)

    def test_cleanup_failed_remove_or_push_deletes_nothing_more(self):
        state = self.preflight_state()
        router = self.cleanup_routes({("git", "worktree", "remove"): (1, b"", b"busy")})
        code, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router)
        self.assertEqual(code, 1)
        self.assertIn("worktree: NOT removed", out)
        self.assertEqual(router.ran("git", "branch"), [])
        self.assertEqual(router.ran("git", "push"), [])
        router = self.cleanup_routes({("git", "push"): (1, b"", b"stale info")})
        _, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router)
        self.assertIn("remote branch: skipped (lease rejected or push failed: stale info)", out)

    def test_cleanup_remote_delete_guards(self):
        state = self.preflight_state()
        cases = {
            "lookup failed": (128, b"", b"ssh: denied"),
            "different tip": ok("{}\trefs/heads/{}\n".format(OTHER, BRANCH)),
            "already deleted": ok(""),
        }
        for name, response in cases.items():
            with self.subTest(case=name):
                router = self.cleanup_routes({("git", "ls-remote"): response})
                _, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router)
                self.assertEqual(router.ran("git", "push"), [])
                self.assertIn("remote branch: " + {"lookup failed": "lookup failed",
                                                   "different tip": "skipped (tip",
                                                   "already deleted": "already deleted"}[name], out)

    def test_cleanup_default_branch_is_protected(self):
        state = self.preflight_state()
        state["pr"]["branch"] = "main"
        router = self.cleanup_routes()
        _, out, _ = self.run_main(["cleanup", "--state", self.state_file(state)], router)
        self.assertIn("branches: kept (main is the default branch)", out)
        self.assertEqual(router.ran("git", "branch"), [])
        self.assertEqual(router.ran("git", "push"), [])

    def test_cleanup_post_land_needs_fast_forward(self):
        state = self.preflight_state()
        cases = {
            "wrong branch": {("git", "worktree", "list"): ok(self.porcelain(main_branch="other"))},
            "dirty main": {("git", "status"): lambda argv, _: ok(" M k\n") if argv[2] == self.main else ok()},
            "ff failed": {("git", "merge", "--ff-only"): (128, b"", b"diverged")},
            "not contained": {("git", "merge-base", "--is-ancestor"): (1, b"", b"")},
        }
        for name, over in cases.items():
            with self.subTest(case=name):
                shell = mock.Mock(return_value=0)
                _, out, _ = self.run_main(
                    ["cleanup", "--state", self.state_file(state)], self.cleanup_routes(over), shell)
                shell.assert_not_called()
                self.assertIn("post-land command: skipped", out)


if __name__ == "__main__":
    unittest.main()
