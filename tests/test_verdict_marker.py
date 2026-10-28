#!/usr/bin/env python3
"""Tests for spec-cycle's verdict_marker.py (VHS-91).

Stdlib unittest. The script is loaded by file path, the same way
tests/test_spec_land.py loads land_check.py. Fixtures live in a temp dir;
expected fingerprints are hashlib over hand-filtered bytes, so no sed runs.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "spec-cycle" / "scripts" / "verdict_marker.py"
TICKET = "VHS-91"
SPEC_REL = "docs/specs/TODO/VHS-91.spec.md"


def load_script(path: Path, module_name: str):
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load script at {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def sha(data: bytes) -> str:
    return "sha256-lf:" + hashlib.sha256(data).hexdigest()


def marker_text(verdict="green", source="review", ticket=TICKET, round_="3", gate="0",
                tier="big", date="2026-10-27", fingerprint="none", extra=(), drop=()):
    rows = [
        ("verdict", verdict), ("source", source), ("ticket", ticket), ("spec", SPEC_REL),
        ("round", round_), ("gate", gate), ("tier", tier), ("date", date),
        ("fingerprint", fingerprint),
    ]
    lines = ["# Spec verdict: " + TICKET, ""]
    lines += ["{}: {}".format(k, v) for k, v in rows if k not in drop]
    lines += list(extra)
    return "\n".join(lines) + "\n"


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script(SCRIPT, "verdict_marker_under_test")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.reviews = self.root / "VHS-91.reviews"
        self.reviews.mkdir()
        self.marker = self.reviews / "verdict.md"
        self.spec = self.root / "VHS-91.spec.md"
        self.spec.write_bytes(b"# Spec\n\nbody\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = self.mod.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def read(self, *flags, marker=None):
        argv = ["read", "--ticket", TICKET, "--marker", marker or self.marker, *flags]
        code, out, err = self.run_main(argv)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def read_fp(self, *flags, marker=None):
        return self.read("--spec", self.spec, *flags, marker=marker)

    def write_marker(self, text):
        self.marker.write_text(text, encoding="utf-8", newline="")

    def good_fp(self):
        return self.mod.fingerprint(str(self.spec))


class TestFingerprint(Base):
    def fp_of(self, data: bytes) -> str:
        self.spec.write_bytes(data)
        return self.mod.fingerprint(str(self.spec))

    def test_lf_and_crlf_agree(self):
        self.assertEqual(self.fp_of(b"a\nb\n"), self.fp_of(b"a\r\nb\r\n"))
        self.assertEqual(self.fp_of(b"a\nb\n"), sha(b"a\nb\n"))

    def test_follow_up_lines_are_dropped(self):
        data = b"a\n**Follow-up:** VHS-1\n  **Follow-up:** x\n\t**Follow-up:** y\nsee Follow-up: z\nb\n"
        self.assertEqual(self.fp_of(data), sha(b"a\nsee Follow-up: z\nb\n"))
        self.assertEqual(self.fp_of(b"a\n- x **Follow-up:** y\n"), sha(b"a\n- x **Follow-up:** y\n"))

    def test_no_final_lf_is_kept(self):
        self.assertEqual(self.fp_of(b"a\nb"), sha(b"a\nb"))
        self.assertEqual(self.fp_of(b"a\n**Follow-up:** x"), sha(b"a\n"))

    def test_empty_file(self):
        self.assertEqual(self.fp_of(b""), sha(b""))

    def test_cli(self):
        code, out, _ = self.run_main(["fingerprint", self.spec])
        self.assertEqual((code, out), (0, sha(b"# Spec\n\nbody\n") + "\n"))

    def test_unreadable_spec_exits_1(self):
        code, out, err = self.run_main(["fingerprint", self.root / "absent.md"])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("fingerprint not computed (", err)


class TestReadStates(Base):
    def test_missing(self):
        self.assertEqual(self.read_fp()["state"], "missing")
        absent = self.root / "nope.reviews" / "verdict.md"
        self.assertEqual(self.read_fp(marker=absent)["state"], "missing")

    def test_unreadable(self):
        cases = {
            "no verdict line": marker_text(drop=("verdict",)),
            "bad verdict value": marker_text(verdict="amber"),
            "no ticket line": marker_text(drop=("ticket",)),
            "another ticket": marker_text(ticket="VHS-9"),
        }
        for name, text in cases.items():
            with self.subTest(case=name):
                self.write_marker(text)
                result = self.read_fp()
                self.assertEqual(result["state"], "unreadable")
                self.assertTrue(result["reason"])
        self.marker.unlink()
        self.marker.mkdir()
        self.assertEqual(self.read_fp()["reason"], "not a regular file")
        self.marker.rmdir()
        self.marker.write_bytes(b"verdict: green\nticket: VHS-91\n\xff\n")
        self.assertEqual(self.read_fp()["reason"], "not UTF-8")

    def test_pending_and_red(self):
        self.write_marker(marker_text(verdict="pending", round_="in progress", gate="in progress"))
        self.assertEqual(self.read_fp()["state"], "pending")
        self.write_marker(marker_text(verdict="red", gate="2", fingerprint=self.good_fp()))
        self.assertEqual(self.read_fp()["state"], "red")
        self.spec.write_bytes(b"changed\n")
        self.assertEqual(self.read_fp()["state"], "red")

    def test_green(self):
        self.write_marker(marker_text(fingerprint=self.good_fp()))
        result = self.read_fp()
        self.assertEqual((result["state"], result["cause"], result["reason"]), ("green", None, None))

    def test_changed_causes(self):
        self.write_marker(marker_text(fingerprint=sha(b"other")))
        self.assertEqual(self.read_fp()["cause"], "fingerprint-differs")
        self.write_marker(marker_text(drop=("fingerprint",)))
        self.assertEqual(self.read_fp()["cause"], "fingerprint-none")
        self.write_marker(marker_text(fingerprint="none"))
        self.assertEqual(self.read_fp()["cause"], "fingerprint-none")
        self.write_marker(marker_text(fingerprint=self.good_fp()))
        self.spec.unlink()
        result = self.read_fp()
        self.assertEqual((result["state"], result["cause"]), ("changed", "fingerprint-not-computed"))


class TestFieldRules(Base):
    def test_first_verdict_wins(self):
        self.write_marker(marker_text(verdict="red", extra=("verdict: green",)))
        self.assertEqual(self.read_fp()["state"], "red")

    def test_trailing_cr_removed(self):
        self.write_marker(marker_text(fingerprint=self.good_fp()).replace("\n", "\r\n"))
        self.assertEqual(self.read_fp()["state"], "green")

    def test_indented_verdict_is_not_a_field(self):
        text = marker_text().replace("verdict: green", "  verdict: green")
        self.write_marker(text)
        self.assertEqual(self.read_fp()["state"], "unreadable")

    def test_heading_is_not_a_field(self):
        self.write_marker("# Spec verdict: red\n\nticket: VHS-91\n")
        self.assertEqual(self.read_fp()["state"], "unreadable")


class TestReadFlags(Base):
    def test_no_fingerprint_passes_none(self):
        self.write_marker(marker_text(fingerprint="none"))
        self.assertEqual(self.read("--no-fingerprint")["state"], "green")

    def test_spec_tier(self):
        self.write_marker(marker_text(tier="small", fingerprint=self.good_fp()))
        result = self.read_fp("--spec-tier", "big")
        self.assertEqual((result["state"], result["cause"], result["marker_tier"]),
                         ("changed", "tier", "small"))
        self.assertEqual(self.read_fp()["state"], "green")
        self.write_marker(marker_text(drop=("tier",), fingerprint=self.good_fp()))
        self.assertEqual(self.read_fp("--spec-tier", "big")["state"], "green")
        self.write_marker(marker_text(tier="tweak", fingerprint=self.good_fp()))
        self.assertEqual(self.read_fp("--spec-tier", "big")["cause"], "tier")

    def test_fingerprint_cause_wins(self):
        self.write_marker(marker_text(tier="small", fingerprint=sha(b"other")))
        self.assertEqual(self.read_fp("--spec-tier", "big")["cause"], "fingerprint-differs")

    def test_spec_and_no_fingerprint_are_exclusive(self):
        for flags in (["--spec", self.spec, "--no-fingerprint"], []):
            with self.subTest(flags=flags):
                with self.assertRaises(SystemExit) as caught:
                    self.run_main(["read", "--ticket", TICKET, "--marker", self.marker, *flags])
                self.assertEqual(caught.exception.code, 2)


class TestKindAndDate(Base):
    def test_kinds(self):
        self.write_marker(marker_text())
        self.assertEqual(self.read("--no-fingerprint")["kind"], "review, round 3")
        self.write_marker(marker_text(source="operator-attested"))
        self.assertEqual(self.read("--no-fingerprint")["kind"], "operator-attested")
        self.write_marker(marker_text(drop=("source", "date")))
        result = self.read("--no-fingerprint")
        self.assertEqual((result["kind"], result["date"]), ("source not recorded", "no date"))


class TestWrite(Base):
    def write(self, *flags, verdict="green", source="review", round_="3", gate="0",
              marker=None):
        argv = ["write", "--marker", marker or self.marker, "--ticket", TICKET,
                "--spec", SPEC_REL, "--verdict", verdict, "--source", source,
                "--round", round_, "--gate", gate, "--tier", "big",
                "--date", "2026-10-27", *flags]
        return self.run_main(argv)

    def test_rendered_bytes(self):
        fp = self.good_fp()
        cases = (
            ({"verdict": "pending", "round_": "in progress", "gate": "in progress"}, (),
             marker_text(verdict="pending", round_="in progress", gate="in progress")),
            ({"verdict": "red", "gate": "2"}, ("--fingerprint-of", self.spec),
             marker_text(verdict="red", gate="2", fingerprint=fp)),
            ({}, ("--fingerprint-of", self.spec), marker_text(fingerprint=fp)),
        )
        for kwargs, flags, expected in cases:
            with self.subTest(kwargs=kwargs):
                code, out, err = self.write(*flags, **kwargs)
                self.assertEqual(code, 0, err)
                self.assertEqual(out, "verdict marker written: {}\n".format(self.marker))
                self.assertEqual(self.marker.read_bytes(), expected.encode("utf-8"))

    def test_attested_replaces(self):
        attest = ("--fingerprint-of", self.spec, "--reason", "hand review", "--replaces", "auto")

        def expected(replaces):
            return marker_text(source="operator-attested", round_="not reviewed",
                               gate="not reviewed", fingerprint=self.good_fp(),
                               extra=("reason: hand review", "replaces: " + replaces))

        priors = (
            (None, "none"),
            ("garbage\n", "unreadable"),
            (marker_text(verdict="red", gate="2", date="2026-10-20"),
             "red, review, round 3, gate 2, 2026-10-20"),
            (marker_text(verdict="pending", drop=("source", "round", "date")),
             "pending, not recorded, round not recorded, gate 0, not recorded"),
        )
        for prior, replaces in priors:
            with self.subTest(prior=replaces):
                if prior is None:
                    self.marker.unlink(missing_ok=True)
                else:
                    self.write_marker(prior)
                code, _, err = self.write(*attest, source="operator-attested",
                                          round_="not reviewed", gate="not reviewed")
                self.assertEqual(code, 0, err)
                self.assertEqual(self.marker.read_text(encoding="utf-8"), expected(replaces))

    def test_creates_leaf_directory(self):
        self.reviews.rmdir()
        code, _, err = self.write()
        self.assertEqual(code, 0, err)
        self.assertTrue(self.marker.is_file())

    def test_no_temp_left(self):
        self.write()
        self.write_marker(marker_text(fingerprint="none"))
        with mock.patch.object(self.mod.os, "replace", side_effect=OSError("locked")):
            code, out, _ = self.write()
        self.assertEqual(code, 1)
        self.assertEqual(out, "verdict marker NOT written: locked — the marker on disk says green\n")
        self.assertEqual([p.name for p in self.reviews.iterdir()], ["verdict.md"])

    def test_failed_write_reports_on_disk_verdict(self):
        priors = (
            (None, "none"),
            ("garbage\n", "unreadable"),
            (marker_text(ticket="VHS-1"), "green"),
        )
        for prior, said in priors:
            with self.subTest(said=said):
                if prior is None:
                    self.marker.unlink(missing_ok=True)
                else:
                    self.write_marker(prior)
                with mock.patch.object(self.mod.os, "replace", side_effect=OSError("locked")):
                    code, out, _ = self.write()
                self.assertEqual(code, 1)
                self.assertTrue(out.endswith("— the marker on disk says {}\n".format(said)), out)

    def test_usage_errors(self):
        for flags, kwargs in ((("--reason", "x"), {}), ((), {"round_": "0"}),
                              (("--replaces", "auto"), {})):
            with self.subTest(flags=flags, kwargs=kwargs):
                with self.assertRaises(SystemExit) as caught:
                    self.write(*flags, **kwargs)
                self.assertEqual(caught.exception.code, 2)
        with self.assertRaises(SystemExit) as caught:
            self.run_main(["write", "--marker", self.marker, "--ticket", "vhs-91", "--spec",
                           SPEC_REL, "--verdict", "green", "--source", "review", "--round", "1",
                           "--gate", "0", "--tier", "big"])
        self.assertEqual(caught.exception.code, 2)

    def test_reason_line_breaks_become_spaces(self):
        code, _, err = self.write("--reason", "one\ntwo\r\nthree", source="operator-attested",
                                  round_="not reviewed", gate="not reviewed")
        self.assertEqual(code, 0, err)
        self.assertIn("reason: one two three\n", self.marker.read_text(encoding="utf-8"))

    def test_written_marker_reads_back(self):
        for verdict, gate, state in (("pending", "in progress", "pending"), ("red", "2", "red"),
                                     ("green", "0", "green")):
            with self.subTest(verdict=verdict):
                flags = () if verdict == "pending" else ("--fingerprint-of", self.spec)
                round_ = "in progress" if verdict == "pending" else "3"
                self.write(*flags, verdict=verdict, gate=gate, round_=round_)
                self.assertEqual(self.read_fp("--spec-tier", "big")["state"], state)
        self.write("--fingerprint-of", self.spec, "--reason", "r", "--replaces", "auto",
                   source="operator-attested", round_="not reviewed", gate="not reviewed")
        self.assertEqual(self.read_fp()["kind"], "operator-attested")

    def test_unreadable_spec_writes_none(self):
        code, out, err = self.write("--fingerprint-of", self.root / "absent.md")
        self.assertEqual(code, 0, err)
        self.assertTrue(out.startswith("verdict marker: fingerprint not computed ("), out)
        self.assertIn("fingerprint: none\n", self.marker.read_text(encoding="utf-8"))

    def test_missing_leaf_parent_creates_nothing(self):
        marker = self.root / "wrong" / "VHS-91.reviews" / "verdict.md"
        code, out, _ = self.write(marker=marker)
        self.assertEqual(code, 1)
        self.assertTrue(out.endswith("— the marker on disk says none\n"), out)
        self.assertFalse((self.root / "wrong").exists())

    @unittest.skipIf(os.name == "nt", "POSIX mode bits")
    def test_mode(self):
        self.write()
        self.assertEqual(stat.S_IMODE(self.marker.stat().st_mode), 0o644)
        os.chmod(str(self.marker), 0o600)
        self.write()
        self.assertEqual(stat.S_IMODE(self.marker.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
