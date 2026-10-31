#!/usr/bin/env python3
"""Regression for VHS-103: live ticket reads, not the MCP mirror."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    REPO_ROOT / "skills" / "spec-brief" / "SKILL.md",
    REPO_ROOT / "skills" / "spec-cycle" / "SKILL.md",
    REPO_ROOT / "skills" / "spec-close" / "SKILL.md",
    REPO_ROOT / "skills" / "spec-land" / "SKILL.md",
]
AGENTS = [
    REPO_ROOT / "agents" / "spec-reviewer-{}.md".format(name)
    for name in ("correctness", "edge-cases", "conventions", "scalability")
]
LIVE_READ = SKILLS[:3] + AGENTS


def read(path):
    return path.read_text(encoding="utf-8")


class TestPlaneLiveRead(unittest.TestCase):

    def test_no_mirror_read(self):
        # Regression for VHS-103: no mirror tag and no memory search on these reads.
        for path in SKILLS + AGENTS:
            text = read(path)
            for phrase in ("plane_work_item", "memory_search"):
                with self.subTest(path=path.name, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_no_retired_names(self):
        for path in SKILLS + AGENTS:
            text = read(path)
            for phrase in ("plane-proxy", "mcp__plane__"):
                with self.subTest(path=str(path.relative_to(REPO_ROOT)), phrase=phrase):
                    self.assertNotIn(phrase, text)
        for rel in ("AGENTS.md", "README.md", "docs/customizing.md"):
            with self.subTest(path=rel):
                self.assertNotIn("plane-proxy", read(REPO_ROOT / rel))

    def test_live_read_named(self):
        for path in LIVE_READ:
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertIn("retrieve_by_identifier", read(path))

    def test_reviewers_report_unread_ticket(self):
        for path in AGENTS:
            text = read(path)
            with self.subTest(agent=path.name):
                self.assertIn("ticket not read", text)
                self.assertIn("ticket not found", text)
                for line in text.splitlines():
                    self.assertNotIn("`namespace`", line)

    def test_spec_brief_header_fields(self):
        text = read(REPO_ROOT / "skills" / "spec-brief" / "SKILL.md")
        self.assertIn(
            'fields: "id,name,state,description_stripped,priority,assignees,created_at"',
            text)

    def test_warning_names_reauth(self):
        for name in ("spec-brief", "spec-cycle", "spec-close"):
            with self.subTest(skill=name):
                self.assertIn(
                    "re-authenticate",
                    read(REPO_ROOT / "skills" / name / "SKILL.md"))

    def test_no_namespace_config(self):
        data = json.loads(
            (REPO_ROOT / "skills" / "ship-spec" / "states.json").read_text(encoding="utf-8"))
        for key, value in data.items():
            if isinstance(value, str):
                self.assertNotIn("namespace", value.lower(), key)
                continue
            if not isinstance(value, dict):
                continue
            self.assertNotIn("namespace", value, key)
            self.assertNotIn("namespace", value.get("_note", "").lower(), key)

    def test_no_shared_memory_service(self):
        for name in ("spec-brief", "spec-cycle", "spec-close"):
            block = read(REPO_ROOT / "skills" / name / "SKILL.md").split("---", 2)[1]
            with self.subTest(skill=name):
                self.assertNotIn("shared-memory", block)

    def test_close_gate_unchanged(self):
        text = read(REPO_ROOT / "skills" / "spec-close" / "SKILL.md")
        self.assertIn("Plane unreachable or ticket not found", text)
        self.assertIn("partial-or-abort", text)


if __name__ == "__main__":
    unittest.main()
