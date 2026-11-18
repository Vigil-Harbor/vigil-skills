#!/usr/bin/env python3
"""Gate one design-loop review round.

Reads the reviewer's JSON (the shape in reference/score-schema.json), prints
the scores, and answers one question with its exit code:

    0  every category on every surface reached the target
    1  at least one did not
    2  the review is malformed or incomplete; the round is void

Usage:
    score_gate.py <review.json> [--target 8] [--categories a,b,c] [--concerns]

--categories makes a surface that lacks one of the named categories a
malformed review, so a reviewer cannot pass the gate by leaving one out.
Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_VOID = 2

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Malformed(Exception):
    """The review cannot be gated as it stands."""


def _text(value, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Malformed(f"{what} must be a non-empty string")
    return value.strip()


def read_review(raw: object, required: list[str] | None = None) -> list[dict]:
    """Return [{surface, categories: [{category, score, rationale, concerns}]}].

    Raises Malformed on anything that would make the gate's answer unreliable.
    """
    if not isinstance(raw, dict):
        raise Malformed("the review must be a JSON object")
    surfaces = raw.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise Malformed("'surfaces' must be a non-empty list")

    out: list[dict] = []
    seen_surfaces: set[str] = set()
    for i, surface in enumerate(surfaces):
        if not isinstance(surface, dict):
            raise Malformed(f"surfaces[{i}] must be an object")
        name = _text(surface.get("surface"), f"surfaces[{i}].surface")
        if name in seen_surfaces:
            raise Malformed(f"surface '{name}' appears twice")
        seen_surfaces.add(name)

        categories = surface.get("categories")
        if not isinstance(categories, list) or not categories:
            raise Malformed(f"surface '{name}': 'categories' must be a non-empty list")

        cats: list[dict] = []
        seen: set[str] = set()
        for j, cat in enumerate(categories):
            if not isinstance(cat, dict):
                raise Malformed(f"surface '{name}': categories[{j}] must be an object")
            cat_name = _text(cat.get("category"), f"surface '{name}': categories[{j}].category")
            key = cat_name.lower()
            if key in seen:
                raise Malformed(f"surface '{name}': category '{cat_name}' appears twice")
            seen.add(key)

            score = cat.get("score")
            # bool is an int in Python; a score of true must not read as 1.
            if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 10:
                raise Malformed(f"surface '{name}', {cat_name}: score must be an integer from 1 to 10")

            concerns = cat.get("concerns", [])
            if not isinstance(concerns, list):
                raise Malformed(f"surface '{name}', {cat_name}: 'concerns' must be a list")
            cats.append({
                "category": cat_name,
                "score": score,
                "rationale": cat.get("rationale") if isinstance(cat.get("rationale"), str) else "",
                "concerns": [c for c in concerns if isinstance(c, dict)],
            })

        if required:
            missing = [r for r in required if r.lower() not in seen]
            if missing:
                raise Malformed(f"surface '{name}' has no score for: {', '.join(missing)}")
        out.append({"surface": name, "categories": cats})
    return out


def lowest(review: list[dict]) -> tuple[int, str, str]:
    """(score, surface, category) of the lowest score; first one wins a tie."""
    best: tuple[int, str, str] | None = None
    for surface in review:
        for cat in surface["categories"]:
            if best is None or cat["score"] < best[0]:
                best = (cat["score"], surface["surface"], cat["category"])
    assert best is not None  # read_review guarantees at least one category
    return best


def render(review: list[dict], target: int, show_concerns: bool) -> str:
    lines: list[str] = []
    width = max(len(s["surface"]) for s in review)
    for surface in review:
        cells = "  ".join(
            f"{c['category']} {c['score']}{'' if c['score'] >= target else ' <'}"
            for c in surface["categories"]
        )
        lines.append(f"{surface['surface'].ljust(width)}  {cells}")

    score, where, cat = lowest(review)
    lines.append(f"LOWEST: {score} ({where} / {cat})")
    lines.append(f"GATE: {'PASS' if score >= target else 'FAIL'} (target {target})")

    if show_concerns:
        for surface in review:
            for c in surface["categories"]:
                if not c["concerns"]:
                    continue
                lines.append("")
                lines.append(f"[{surface['surface']} / {c['category']}] {c['score']}")
                ordered = sorted(
                    c["concerns"],
                    key=lambda k: SEVERITY_ORDER.get(str(k.get("severity", "")).lower(), 3),
                )
                for k in ordered:
                    lines.append(
                        f"  - ({k.get('severity', '?')}) {k.get('where', '?')} :: "
                        f"{k.get('problem', '?')} => {k.get('suggestion', '?')}"
                    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gate one design-loop review round.")
    parser.add_argument("review", help="path to the reviewer's JSON")
    parser.add_argument("--target", type=int, default=8, help="score every category must reach (default 8)")
    parser.add_argument("--categories", default="", help="comma-separated categories every surface must carry")
    parser.add_argument("--concerns", action="store_true", help="also print every concern, most severe first")
    args = parser.parse_args(argv)

    if not 1 <= args.target <= 10:
        print("VOID: --target must be from 1 to 10", file=sys.stderr)
        return EXIT_VOID
    required = [c.strip() for c in args.categories.split(",") if c.strip()]

    path = Path(args.review)
    try:
        # utf-8-sig: a reviewer CLI on Windows may write a byte-order mark.
        text = path.read_text(encoding="utf-8-sig")
    except OSError as err:
        print(f"VOID: cannot read {path}: {err}", file=sys.stderr)
        return EXIT_VOID
    if not text.strip():
        print(f"VOID: {path} is empty (the reviewer did not finish)", file=sys.stderr)
        return EXIT_VOID
    try:
        review = read_review(json.loads(text), required)
    except json.JSONDecodeError as err:
        print(f"VOID: {path} is not JSON: {err}", file=sys.stderr)
        return EXIT_VOID
    except Malformed as err:
        print(f"VOID: {err}", file=sys.stderr)
        return EXIT_VOID

    print(render(review, args.target, args.concerns))
    return EXIT_PASS if lowest(review)[0] >= args.target else EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
