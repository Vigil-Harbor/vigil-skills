#!/usr/bin/env python3
"""Read, write, and fingerprint the spec verdict marker (VHS-91).

Usage:
    verdict_marker.py fingerprint <spec-path>
    verdict_marker.py read --ticket ID --marker PATH (--spec PATH | --no-fingerprint)
                           [--spec-tier small|big|irreversible]
    verdict_marker.py write --marker PATH --ticket ID --spec REL-PATH
                            --verdict green|red|pending --source review|operator-attested
                            --round R --gate G --tier small|big|irreversible
                            [--fingerprint-of PATH] [--reason TEXT] [--replaces auto]
                            [--date YYYY-MM-DD]

This docstring is the one statement of the marker format. spec-cycle writes
the marker at docs/specs/TODO/<TICKET-ID>.reviews/verdict.md; ship-spec and
spec-tickets read it. Each write replaces the whole file:

    # Spec verdict: <TICKET-ID>

    verdict: green | red | pending
    source: review | operator-attested
    ticket: <TICKET-ID>
    spec: docs/specs/TODO/<TICKET-ID>.spec.md
    round: <positive integer> | not reviewed | in progress
    gate: <P0+P1 count> | not reviewed | in progress
    tier: small | big | irreversible
    date: <YYYY-MM-DD>
    fingerprint: sha256-lf:<64 hex digits> | none
    reason: <one line>
    replaces: <verdict>, <source>, round <round>, gate <gate>, <date> | none | unreadable

Field rules. A field is a line that starts with a lower-case key, a colon,
then the value. The first line for each key wins. One trailing CR is removed
and the value is trimmed. Any other line, the heading included, is ignored.
reason and replaces appear only on an operator-attested marker.

Fingerprint. SHA-256 of the spec's bytes with every CR byte removed, then with
every line dropped whose first non-blank characters are **Follow-up:**, every
other byte kept (a final line with no LF does not gain one). Non-blank means
anything other than space, tab, VT or FF. Written as sha256-lf:<64 hex>.
Follow-up lines are excluded so a ticket id filed after green does not read as
a changed spec.

States, tested in order, first match wins:
    missing     the marker file (or its directory) does not exist
    unreadable  not a regular file, cannot be read, not UTF-8, no verdict: line
                with green/red/pending, or a ticket: line absent or naming
                another ticket
    pending     verdict: pending
    red         verdict: red
    green       verdict: green, and the fingerprint and tier tests pass
    changed     verdict: green, and either test fails

fingerprint
    0  stdout sha256-lf:<64 hex>
    1  stderr "fingerprint not computed (<reason>)"

read prints one JSON object on one line and exits 0 whenever it classified
the marker. Keys: state, reason, cause, kind, date, round, gate, verdict,
marker_tier.

write
    0  stdout "verdict marker written: <path>"
    1  stdout "verdict marker NOT written: <error> — the marker on disk says <v>"
    2  usage error

main() reconfigures stdout and stderr to UTF-8. Any other failure exits 3.
SystemExit and KeyboardInterrupt propagate: argparse usage errors stay exit 2.

Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

_FIELD = re.compile(r"^([a-z]+):(.*)$")
_TICKET = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")
_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
_VERDICTS = ("green", "red", "pending")
_SOURCES = ("review", "operator-attested")
_TIERS = ("small", "big", "irreversible")
_FOLLOW_UP = b"**Follow-up:**"
# sed's [[:space:]] in the C locale, less LF (the separator) and CR (removed).
_BLANK = b" \t\x0b\x0c"


class _NotWritten(Exception):
    pass


def fingerprint(path: str) -> str:
    """Raise OSError when the spec cannot be read."""
    with open(path, "rb") as handle:
        data = handle.read()
    # CR is the only line boundary bytes.splitlines() knows besides LF, and it
    # is gone, so keepends splits on LF alone and keeps a missing final LF.
    kept = [line for line in data.replace(b"\r", b"").splitlines(keepends=True)
            if not line.lstrip(_BLANK).startswith(_FOLLOW_UP)]
    return "sha256-lf:" + hashlib.sha256(b"".join(kept)).hexdigest()


def _fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.split("\n"):
        if line.endswith("\r"):
            line = line[:-1]
        match = _FIELD.match(line)
        if match and match.group(1) not in fields:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def _load(marker: str) -> tuple[str, dict[str, str] | None, str | None]:
    """Return (status, fields, reason); status is missing, unreadable or ok."""
    if not os.path.exists(marker):
        return "missing", None, None
    if not os.path.isfile(marker):
        return "unreadable", None, "not a regular file"
    try:
        with open(marker, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return "unreadable", None, "cannot be read ({})".format(exc)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return "unreadable", None, "not UTF-8"
    return "ok", _fields(text), None


def _on_disk(marker: str) -> str:
    """The verdict a failed write reports: one definition (spec Decision 4)."""
    status, fields, _ = _load(marker)
    if status == "missing":
        return "none"
    if status == "ok" and fields.get("verdict") in _VERDICTS:
        return fields["verdict"]
    return "unreadable"


def classify(ticket: str, marker: str, spec: str | None,
             spec_tier: str | None) -> dict:
    """spec None means --no-fingerprint."""
    result = {"state": None, "reason": None, "cause": None, "kind": None,
              "date": None, "round": None, "gate": None, "verdict": None,
              "marker_tier": None}
    status, fields, reason = _load(marker)
    if status != "ok":
        result["state"] = status
        result["reason"] = reason
        return result
    source = fields.get("source")
    if source == "review":
        kind = "review, round {}".format(fields.get("round", "not recorded"))
    elif source == "operator-attested":
        kind = "operator-attested"
    else:
        kind = "source not recorded"
    result.update(kind=kind, date=fields.get("date", "no date"),
                  round=fields.get("round"), gate=fields.get("gate"),
                  verdict=fields.get("verdict"), marker_tier=fields.get("tier"))
    verdict = fields.get("verdict")
    if verdict not in _VERDICTS:
        result["state"] = "unreadable"
        result["reason"] = ("no verdict: line" if verdict is None
                            else "verdict: {} is not green, red or pending".format(verdict))
        return result
    if fields.get("ticket") != ticket:
        result["state"] = "unreadable"
        result["reason"] = ("no ticket: line" if "ticket" not in fields
                            else "ticket: {} is not {}".format(fields["ticket"], ticket))
        return result
    if verdict != "green":
        result["state"] = verdict
        return result

    cause = reason = None
    if spec is not None:
        recorded = fields.get("fingerprint")
        if recorded is None or recorded == "none":
            cause, reason = "fingerprint-none", "the marker records no fingerprint"
        else:
            try:
                computed = fingerprint(spec)
            except OSError as exc:
                cause, reason = "fingerprint-not-computed", "fingerprint not computed ({})".format(exc)
            else:
                if computed != recorded:
                    cause, reason = "fingerprint-differs", "the spec is not the text that was judged"
    marker_tier = fields.get("tier")
    # The fingerprint cause wins when both tests fail.
    if cause is None and spec_tier is not None and marker_tier is not None \
            and (marker_tier not in _TIERS or marker_tier != spec_tier):
        cause = "tier"
        reason = "marker tier {}, spec tier {}".format(marker_tier, spec_tier)
    result["state"] = "green" if cause is None else "changed"
    result["cause"], result["reason"] = cause, reason
    return result


def _replaces(ticket: str, marker: str) -> str:
    current = classify(ticket, marker, None, None)
    if current["state"] == "missing":
        return "none"
    if current["state"] == "unreadable":
        return "unreadable"
    _, fields, _ = _load(marker)
    absent = "not recorded"
    return "{}, {}, round {}, gate {}, {}".format(
        fields["verdict"], fields.get("source", absent), fields.get("round", absent),
        fields.get("gate", absent), fields.get("date", absent))


def render(args, fp: str, replaces: str | None) -> str:
    lines = [
        "# Spec verdict: " + args.ticket,
        "",
        "verdict: " + args.verdict,
        "source: " + args.source,
        "ticket: " + args.ticket,
        "spec: " + args.spec,
        "round: " + args.round,
        "gate: " + args.gate,
        "tier: " + args.tier,
        "date: " + args.date,
        "fingerprint: " + fp,
    ]
    if args.reason is not None:
        lines.append("reason: " + re.sub(r"\r\n|\r|\n", " ", args.reason))
    if replaces is not None:
        lines.append("replaces: " + replaces)
    return "\n".join(lines) + "\n"


def write_atomically(marker: Path, text: str) -> None:
    """Raise _NotWritten or OSError. Shape of prepend_log_entry.write_atomically."""
    leaf = marker.parent
    if not leaf.is_dir():
        # Only the <ID>.reviews/ leaf is created, so a wrong working directory
        # cannot plant a stray marker tree.
        if not leaf.parent.is_dir():
            raise _NotWritten("{} does not exist".format(leaf.parent))
        leaf.mkdir(exist_ok=True)
    try:
        mode = stat.S_IMODE(os.stat(str(marker)).st_mode)
    except FileNotFoundError:
        mode = 0o644
    fd, temp_name = tempfile.mkstemp(prefix=".verdict.md.", suffix=".tmp", dir=str(leaf))
    temp_path = Path(temp_name)
    try:
        # Close before the rename: on Windows an open source handle blocks
        # os.replace.
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp creates at 0600; os.replace would carry that onto the marker.
        os.chmod(str(temp_path), mode)
        os.replace(str(temp_path), str(marker))
    finally:
        temp_path.unlink(missing_ok=True)


def _round(value: str) -> str:
    if value in ("not reviewed", "in progress") or re.fullmatch(r"[1-9][0-9]*", value):
        return value
    raise argparse.ArgumentTypeError("not a positive integer, 'not reviewed' or 'in progress'")


def _gate(value: str) -> str:
    if value in ("not reviewed", "in progress") or re.fullmatch(r"0|[1-9][0-9]*", value):
        return value
    raise argparse.ArgumentTypeError("not a non-negative integer, 'not reviewed' or 'in progress'")


def _ticket(value: str) -> str:
    if _TICKET.fullmatch(value):
        return value
    raise argparse.ArgumentTypeError("not a ticket id")


def _date(value: str) -> str:
    if _DATE.fullmatch(value):
        return value
    raise argparse.ArgumentTypeError("not YYYY-MM-DD")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="verdict_marker.py")
    sub = parser.add_subparsers(dest="command", required=True)
    fp = sub.add_parser("fingerprint")
    fp.add_argument("spec")
    read = sub.add_parser("read")
    read.add_argument("--ticket", required=True)
    read.add_argument("--marker", required=True)
    group = read.add_mutually_exclusive_group(required=True)
    group.add_argument("--spec")
    group.add_argument("--no-fingerprint", action="store_true")
    read.add_argument("--spec-tier", choices=_TIERS)
    write = sub.add_parser("write")
    write.add_argument("--marker", required=True)
    write.add_argument("--ticket", required=True, type=_ticket)
    write.add_argument("--spec", required=True)
    write.add_argument("--verdict", required=True, choices=_VERDICTS)
    write.add_argument("--source", required=True, choices=_SOURCES)
    write.add_argument("--round", required=True, type=_round)
    write.add_argument("--gate", required=True, type=_gate)
    write.add_argument("--tier", required=True, choices=_TIERS)
    write.add_argument("--fingerprint-of")
    write.add_argument("--reason")
    write.add_argument("--replaces", choices=("auto",))
    write.add_argument("--date", type=_date,
                       default=datetime.date.today().isoformat())
    return parser


def _run(argv: list[str]) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "fingerprint":
        try:
            print(fingerprint(args.spec))
        except OSError as exc:
            print("fingerprint not computed ({})".format(exc), file=sys.stderr)
            return 1
        return 0
    if args.command == "read":
        spec = None if args.no_fingerprint else args.spec
        print(json.dumps(classify(args.ticket, args.marker, spec, args.spec_tier)))
        return 0

    if args.source != "operator-attested" and (args.reason is not None or args.replaces):
        parser.error("--reason and --replaces need --source operator-attested")
    fp = "none"
    if args.fingerprint_of is not None:
        try:
            fp = fingerprint(args.fingerprint_of)
        except OSError as exc:
            print("verdict marker: fingerprint not computed ({})".format(exc))
    try:
        replaces = _replaces(args.ticket, args.marker) if args.replaces else None
        write_atomically(Path(args.marker), render(args, fp, replaces))
    except (OSError, _NotWritten) as exc:
        print("verdict marker NOT written: {} — the marker on disk says {}".format(
            exc, _on_disk(args.marker)))
        return 1
    print("verdict marker written: " + args.marker)
    return 0


def main(argv: list[str]) -> int:
    # Windows stdout is cp1252 when piped. Reconfigure before any write so the
    # em dash in the NOT-written line cannot escape as a crash (exit 1).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass
    try:
        return _run(argv)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # noqa: BLE001 - exit 1 is a documented outcome
        sys.stderr.write(
            "unexpected failure: {}: {}\n".format(type(exc).__name__, exc))
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
