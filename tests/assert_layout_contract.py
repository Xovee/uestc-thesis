#!/usr/bin/env python3
"""Measure edition-independent layout rules in the actual PDF output."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber


TEX_PT_TO_PDF_PT = 72 / 72.27
MM_TO_PDF_PT = 72 / 25.4


def inspect(pdf_path: Path) -> dict:
    failures: list[str] = []
    measurements: dict[str, float | list[float]] = {}

    def close(name: str, actual: float, expected: float, tolerance: float = 0.1):
        measurements[name] = round(actual, 4)
        if abs(actual - expected) > tolerance:
            failures.append(f"{name}: {actual:.4f}, expected {expected:.4f} +/- {tolerance}")

    with pdfplumber.open(pdf_path) as pdf:
        pages = list(pdf.pages)
        for number, page in enumerate(pages, 1):
            close(f"page_{number}_width", page.width, 210 * MM_TO_PDF_PT)
            close(f"page_{number}_height", page.height, 297 * MM_TO_PDF_PT)

        def locate(label: str):
            for page in pages:
                text = "".join(char["text"] for char in page.chars)
                index = text.find(label)
                if index >= 0:
                    return page, page.chars[index:index + len(label)]
            raise ValueError(f"Missing probe: {label}")

        def baseline(char):
            return float(char["matrix"][5])

        def baseline_gap(first: str, second: str):
            first_page, first_chars = locate(first)
            second_page, second_chars = locate(second)
            if first_page.page_number != second_page.page_number:
                raise ValueError(f"Baseline probes split across pages: {first}, {second}")
            return baseline(first_chars[0]) - baseline(second_chars[0])

        for first, second in (("BaselineA", "BaselineB"), ("BaselineB", "BaselineC"),
                              ("AfterDisplay", "AfterBaseline")):
            close(f"baseline_{first}_{second}", baseline_gap(first, second), 20 * TEX_PT_TO_PDF_PT)

        _, latin = locate("BaselineA")
        close("body_font_size", latin[0]["size"], 12 * TEX_PT_TO_PDF_PT)
        if "TimesNewRoman" not in latin[0]["fontname"]:
            failures.append(f"Unexpected Latin body font: {latin[0]['fontname']}")
        _, chinese = locate("中文正文第一行")
        close("chinese_font_size", chinese[0]["size"], 12 * TEX_PT_TO_PDF_PT)
        if "SimSun" not in chinese[0]["fontname"]:
            failures.append(f"Unexpected Chinese body font: {chinese[0]['fontname']}")
        _, indented = locate("IndentProbe")
        _, unindented = locate("NoIndentProbe")
        close("first_line_indent", indented[0]["x0"] - unindented[0]["x0"], 24 * TEX_PT_TO_PDF_PT)
        close("left_margin", unindented[0]["x0"], 30 * MM_TO_PDF_PT)
        close("paragraph_baseline_gap", baseline_gap("IndentProbe", "NoIndentProbe"), 20 * TEX_PT_TO_PDF_PT)

        # In an unexpanded hbox, automatic CJK/Latin and CJK/digit gaps must
        # have the declared natural width. Source spaces remain ordinary spaces.
        for label, symbol in (("LatinAuto", "A"), ("LatinSpace", "A"),
                              ("NumberAuto", "1"), ("NumberSpace", "1")):
            page, marker = locate(label)
            row = [c for c in page.chars if c["x0"] > marker[-1]["x1"] + 2
                   and abs(baseline(c) - baseline(marker[0])) < 0.1]
            row = [c for c in row if c["text"].strip()]
            if "".join(c["text"] for c in row) != f"中{symbol}文":
                raise ValueError(f"Unexpected mixed-script probe content: {label}")
            close(f"{label}_left_gap", row[1]["x0"] - row[0]["x1"], 3 * TEX_PT_TO_PDF_PT)
            close(f"{label}_right_gap", row[2]["x0"] - row[1]["x1"], 3 * TEX_PT_TO_PDF_PT)

        before_page, before = locate("BeforeDisplay")
        after_page, after = locate("AfterDisplay")
        if before_page.page_number != after_page.page_number:
            raise ValueError("Short display and surrounding text split across pages")
        display = [c for c in before_page.chars
                   if baseline(after[0]) + 1 < baseline(c) < baseline(before[0]) - 1
                   and c["text"].strip()]
        formula = [c for c in display if c["x0"] < 450]
        tag = [c for c in display if c["x0"] >= 450]
        if "".join(c["text"] for c in formula) != "a=b" or "".join(c["text"] for c in tag) != "(1-1)":
            raise ValueError("Formula content or chapter-based equation number changed")
        close("display_center", (min(c["x0"] for c in formula) + max(c["x1"] for c in formula)) / 2,
              before_page.width / 2, 0.2)
        close("equation_number_right", max(c["x1"] for c in tag), before_page.width - 30 * MM_TO_PDF_PT)
        close("equation_font_size", formula[0]["size"], 12 * TEX_PT_TO_PDF_PT)
        for heading, points in (("二级标题", 14), ("三级标题", 14), ("四级标题", 12)):
            _, chars = locate(heading)
            close(f"heading_{heading}_size", chars[0]["size"], points * TEX_PT_TO_PDF_PT)
        # These simple consecutive headings use a 20pt line box plus 6pt
        # after-skip; the following heading must not add its own before-skip.
        close("consecutive_heading_gap", baseline_gap("二级标题", "三级标题"), 26 * TEX_PT_TO_PDF_PT)

    log = pdf_path.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
    if "UESTC-DISPLAY-SKIPS: PASS" not in log:
        failures.append("Display-skip runtime assertion did not run")
    for pattern in (r"Overfull \\[hv]box", r"Missing character:"):
        if re.search(pattern, log):
            failures.append(f"Typesetting log contains {pattern}")
    return {"pdf": str(pdf_path), "measurements_pdf_points": measurements, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    arguments = parser.parse_args()
    try:
        report = inspect(arguments.pdf)
    except (ValueError, KeyError) as error:
        print(f"FAIL: {error}")
        return 1
    arguments.pdf.with_suffix(".layout.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if report["failures"]:
        for failure in report["failures"]:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: PDF font sizes, 20pt baselines, indentation, mixed-script spacing, headings and equation alignment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
