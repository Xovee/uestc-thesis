#!/usr/bin/env python3
"""Assert UESTC bibliography rules for ordinary and online entries."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader


def compact_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return "".join(text.split()).lower()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    arguments = parser.parse_args()

    text = compact_pdf_text(arguments.pdf)
    forbidden = {
        "ordinary-entry DOI": "10.1234/example.2026.123456",
        "ordinary-entry URL": "https://ordinary.example/reference",
        "ordinary-entry eprint": "2609.12345",
    }
    required = {
        "online-entry URL": "https://online.example/resource",
    }

    failures = []
    pages = [
        "".join((page.extract_text() or "").split()).lower()
        for page in PdfReader(arguments.pdf).pages
    ]
    if len(pages) != 2:
        failures.append(f"Pagination fixture has {len(pages)} pages, expected 2")
    else:
        if "paginationfillerreference28" not in pages[0]:
            failures.append("Page 1 no longer contains the final short entry")
        for fragment in (
            "adeliberatelylongbibliographyentry",
            "academictypesettinganddocumentengineering",
            "1201-1248",
        ):
            if fragment not in pages[1] or fragment in pages[0]:
                failures.append(f"Long entry is not wholly on page 2: {fragment}")
    for label, value in forbidden.items():
        if value.lower() in text:
            failures.append(f"{label} was printed")
    for label, value in required.items():
        if value.lower() not in text:
            failures.append(f"{label} was not printed")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: ordinary reference links are hidden and online URLs are retained.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
