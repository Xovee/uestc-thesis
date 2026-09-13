#!/usr/bin/env python3
"""Check body-first citation numbering and intact front-matter lists."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    expected = [
        "lecun2015deep", "vaswani2017attention", "kingma2014adam",
        "lamport1994latex", "zhang2020third",
    ]
    bbl = args.pdf.with_suffix(".bbl").read_text(encoding="utf-8")
    order = re.findall(r"\\bibitem\[[\s\S]*?\]\{([^{}]+)\}", bbl)
    failures = []
    if order != expected:
        failures.append(f"Bibliography order is {order}; expected {expected}")

    reader = PdfReader(args.pdf)
    pages = ["".join((page.extract_text() or "").split()) for page in reader.pages]
    body_pages = [index for index, text in enumerate(pages) if "BODYFIRST" in text]
    if len(body_pages) != 1:
        failures.append(f"Expected one fixture body page, found {len(body_pages)}")
    else:
        body_index = body_pages[0]
        compact = pages[body_index]
        for marker in (
            "BODYFIRST[1]", "TABLESOURCE[2]", "BODYMIDDLE[3]",
            "FIGURESOURCE[4]", "BODYLAST[5]",
        ):
            if marker not in compact:
                failures.append(f"Missing correct rendered citation: {marker}")

        front = pages[:body_index]
        for marker in ("Captioncitationorder", "FIGURESOURCE[4]", "TABLESOURCE[2]"):
            if sum(marker in text for text in front) != 1:
                failures.append(f"Expected one front-matter entry: {marker}")

    # The fix must preserve the output streams, not merely suppress the lists.
    for suffix, marker in (
        (".toc", "Caption citation order"),
        (".lof", "FIGURESOURCE"),
        (".lot", "TABLESOURCE"),
    ):
        path = args.pdf.with_suffix(suffix)
        content = path.read_text(encoding="utf-8") if path.exists() else ""
        if r"\contentsline" not in content or marker not in content:
            failures.append(f"Missing regenerated list entry in {path.name}")

    destinations = reader.named_destinations
    named_links = 0
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A")
            action = action.get_object() if action else {}
            target = annotation.get("/Dest")
            if target is None and action.get("/S") == "/GoTo":
                target = action.get("/D")
            if isinstance(target, str):
                named_links += 1
                if target not in destinations:
                    failures.append(f"Unresolved internal link: {target}")
                elif reader.get_destination_page_number(destinations[target]) is None:
                    failures.append(f"Internal link has no page: {target}")
    if not named_links:
        failures.append("No named internal links found")

    for failure in failures:
        print(f"FAIL: {args.pdf.stem}: {failure}")
    if not failures:
        print(
            f"PASS: {args.pdf.stem}: five body citations in order; "
            f"three front-matter lists intact; {named_links} internal links resolved."
        )
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
