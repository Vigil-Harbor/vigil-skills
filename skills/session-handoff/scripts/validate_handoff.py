#!/usr/bin/env python3
"""Validate a session handoff document.

Usage:
    validate_handoff.py <handoff-file>

Three checks, in order, all on normalized text: every required section heading
is present (by name, at any depth); no `[TODO: ...]` placeholder remains
anywhere in the document; no secret pattern matched. Recommended-section gaps
are informational and change nothing.

Verdicts and exit codes (VHS-28 D6):
    READY        0    all required headings present, no placeholder, no secret
    NEEDS WORK   1    a required heading absent, or a placeholder remains
    BLOCKED      2    a secret matched (outranks the above)
    (no verdict) 3    missing/unreadable file, or no argument - stderr

Exit 2 means secrets and nothing else, so a caller can tell "this contains a
credential" from "you typed the wrong filename". Stdlib only.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REDACTION_FLOOR = 12


def _load_sections():
    """Load the shared section module by file path (D4)."""
    path = Path(__file__).resolve().with_name("_sections.py")
    spec = importlib.util.spec_from_file_location("_session_handoff_sections", path)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load _sections.py from {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["_session_handoff_sections"] = module
    spec.loader.exec_module(module)
    return module


S = _load_sections()


# --- Secret patterns (D1 carry-forward: credential formats are facts) --------

# The dominant real-world leak: a generic assignment. Longer alternatives come
# first so `client_secret` is not reported as `secret`. A minimum value length
# keeps prose out; `token` carries a higher floor because it is a common word.
_GENERIC_SECRET_RE = re.compile(
    r"""\b(client[_-]?secret|private[_-]?key|api[_-]?key|passwd|password|secret|token)\b"""
    r"""\s*[:=]\s*["']?([^\s"'`,;]{8,})""",
    re.IGNORECASE,
)
_GENERIC_MIN = 8
_TOKEN_MIN = 20

# Branded prefixes at current widths.
_BRANDED_PATTERNS = (
    ("openai/anthropic-style key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("github token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("github fine-grained pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]+")),
    ("pem private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("dsn with password",
     re.compile(r"\b[a-zA-Z][a-zA-Z0-9+.-]*://[^\s:/@]+:[^\s:/@]+@[^\s/]+")),
)


def redact(pattern_name: str, value: str) -> str:
    """First-4 + last-4 with the middle masked, but only above 12 characters.

    At 12 or fewer, first-4/last-4 reproduces too much of the value (on an
    8-character value, all of it), so the excerpt names the pattern and the
    length instead. The locus already tells the author where to look.
    """
    if len(value) > REDACTION_FLOOR:
        return value[:4] + "*" * (len(value) - 8) + value[-4:]
    return "<{}, {} chars, fully masked>".format(pattern_name, len(value))


def scan_secrets(lines: list[str]) -> list[tuple[int, str, str]]:
    """Return (line_number, pattern_name, redacted_excerpt) for every match.

    Nothing is exempt. `validate_handoff.py` receives only a file path and
    cannot observe provenance, so any exemption region would have to be a
    structural proxy an author could write themselves.
    """
    findings: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(lines, start=1):
        for match in _GENERIC_SECRET_RE.finditer(line):
            key, value = match.group(1), match.group(2)
            floor = _TOKEN_MIN if key.lower() == "token" else _GENERIC_MIN
            if len(value) < floor:
                continue
            name = "generic assignment ({})".format(key.lower())
            findings.append((lineno, name, redact(name, value)))
        for name, pattern in _BRANDED_PATTERNS:
            for match in pattern.finditer(line):
                findings.append((lineno, name, redact(name, match.group(0))))
    return findings


def scan_placeholders(lines: list[str]) -> list[tuple[int, str]]:
    """Return (line_number, matched_text) for every remaining placeholder.

    The scan is whole-document, so a marker left in a *recommended* section is
    NEEDS WORK too: a missing recommended section is informational, but a
    recommended section still holding its placeholder is unfinished work.
    """
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        for match in S.TODO_MARKER_RE.finditer(line):
            findings.append((lineno, match.group(0)))
    return findings


def _report(path: Path, missing_required, placeholders, missing_recommended,
            secrets, verdict, out) -> None:
    print("handoff: {}".format(path), file=out)
    print("", file=out)

    print("Required sections:", file=out)
    if missing_required:
        for name in missing_required:
            print("  MISSING: {}".format(name), file=out)
    else:
        print("  all present", file=out)

    print("Placeholders remaining:", file=out)
    if placeholders:
        for lineno, text in placeholders:
            print("  {}:{}: {}".format(path, lineno, text), file=out)
    else:
        print("  none", file=out)

    print("Recommended sections (informational):", file=out)
    if missing_recommended:
        for name in missing_recommended:
            print("  missing: {}".format(name), file=out)
    else:
        print("  all present", file=out)

    print("Secrets:", file=out)
    if secrets:
        for lineno, name, excerpt in secrets:
            print("  {}:{}: {} - {}".format(path, lineno, name, excerpt), file=out)
    else:
        print("  none", file=out)

    print("", file=out)
    print("VERDICT: {}".format(verdict), file=out)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: validate_handoff.py <handoff-file>", file=sys.stderr)
        return 3
    path = Path(args[0]).expanduser()
    try:
        raw = path.read_bytes()
    except OSError as exc:
        print("cannot read {}: {}".format(path, exc), file=sys.stderr)
        return 3

    text = S.normalize(raw)
    lines = text.split("\n")

    missing_required = [n for n in S.REQUIRED_SECTIONS if not S.has_section(text, n)]
    placeholders = scan_placeholders(lines)
    missing_recommended = [n for n in S.RECOMMENDED_SECTIONS
                           if not S.has_section(text, n)]
    secrets = scan_secrets(lines)

    if secrets:
        verdict, code = "BLOCKED", 2
    elif missing_required or placeholders:
        verdict, code = "NEEDS WORK", 1
    else:
        verdict, code = "READY", 0

    # All violations print before the verdict; no short-circuit.
    _report(path, missing_required, placeholders, missing_recommended,
            secrets, verdict, sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
