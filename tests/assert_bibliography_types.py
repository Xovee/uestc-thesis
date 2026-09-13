#!/usr/bin/env python3
"""Check rendered citations and bibliography fields; TeX checks list geometry."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    # Strict decoding also detects BibTeX truncating a raw Unicode name initial.
    bbl = args.pdf.with_suffix(".bbl").read_text(encoding="utf-8")
    parts = re.split(r"\\bibitem\[[\s\S]*?\]\{([^{}]+)\}\s*", bbl)
    entries = dict(zip(parts[1::2], parts[2::2]))
    failures = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(len(entries) == 23, f"Expected 23 records, found {len(entries)}")
    markers = {
        "cn-book": "M", "cn-standard": "S", "cn-journal": "J",
        "en-journal": "J", "en-conference": "C", "en-book": "M",
        "online-book": "M/OL", "cn-thesis": "D", "cn-newspaper": "N",
        "cn-report": "R", "cn-patent": "P", "generic-thesis": "D",
        "arxiv-as-article": "J", "legacy-online": "EB/OL",
        "conference-both-places": "C", "conference-location-only": "C",
        "conference-no-place": "C", "conference-empty-location": "C",
    }
    for key, marker in markers.items():
        check(f"[{marker}]" in entries.get(key, ""), f"{key}: wrong type marker")
    expected = {
        "en-journal": ("Hu J, Zhao R, Tian M, et~al.", "5344-5348"),
        "en-book": ("Harrington R~F.", "3rd ed.", "New York:", "76-112"),
        "en-conference": ("Recognition, Boston, USA, 2015: 3003-3012.",),
        "translated-book": ("等译. 2 版.", "15-16"),
        "cn-newspaper": ("2012-03-31", "(3)"),
        "cn-patent": ("ZL201120085830.0", "2012-04-25"),
        "online-book": ("(2013-11-15)", "[2014-06-24]", r"\url{https://"),
        "online-with-separate-doi": (r"\doi{10.0000/online-separate}",),
        "first-edition": ("{LaTeX} reference: A short companion",),
        "accented-initial": (r"Ar{\i}n {\.I}.",),
    }
    for key, fragments in expected.items():
        entry = " ".join(entries.get(key, "").split())
        for fragment in fragments:
            check(fragment in entry, f"{key}: missing {fragment}")
    for key in ("en-journal", "en-conference", "arxiv-as-article"):
        for forbidden in ("/OL", r"\url", r"\doi", "[A]"):
            check(forbidden not in entries.get(key, ""), f"{key}: printed {forbidden}")
    for key in ("online-book", "online-no-doi-repeat"):
        check(r"\doi" not in entries.get(key, ""), f"{key}: DOI duplicated")
    check("1st" not in entries.get("first-edition", ""), "First edition was printed")

    reader = PdfReader(args.pdf)
    rendered = " ".join(
        " ".join(page.extract_text() or "" for page in reader.pages).split()
    )
    conference_places = {
        "conference-both-places": "Test Conference, Meeting City, 2026: 1-2.",
        "conference-location-only": "Test Conference, Meeting City, 2026: 3-4.",
        "conference-no-place": "Test Conference, 2026: 5-6.",
        "conference-empty-location": "Test Conference, Fallback City, 2026: 7-8.",
    }
    for key, fragment in conference_places.items():
        check(fragment in " ".join(entries.get(key, "").split()),
              f"{key}: wrong location or punctuation in BBL")
        check(fragment in rendered, f"{key}: wrong location or punctuation in PDF")
    for forbidden in ("Publisher City", "Ignored Book Location"):
        check(forbidden not in bbl and forbidden not in rendered,
              f"Printed incorrect location: {forbidden}")
    first_page = reader.pages[0].extract_text() or ""
    compact = "".join(first_page.split())
    for citation in (
        "SINGLE[1]", "RANGE[2-4]", "MIXED[1,3,5]", "INLINE[5-6]",
        "REVERSE[2-4]", "AFTER[1]", "STAR[1]", "NOTES[see1]12",
    ):
        check(citation in compact, f"Missing rendered citation: {citation}")
    check(bool(re.search(r"MIXED\s*\[1, 3, 5\]", first_page)),
          "Citation commas lost their following spaces")
    for page in reader.pages[1:]:
        for annotation in page.get("/Annots", []):
            action = annotation.get_object().get("/A", {})
            if action.get("/S") == "/URI":
                check(str(action.get("/URI", "")).startswith("https://doi.org/"),
                      "Bibliography URL unexpectedly became clickable")
    for failure in failures:
        print(f"FAIL: {failure}")
    if not failures:
        print("PASS: 23 bibliography records, conference locations, and rendered citations verified.")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
