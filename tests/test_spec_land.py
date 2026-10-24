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
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
