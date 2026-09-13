#!/usr/bin/env python3
"""Assert cross-reference values and distinct theorem-family PDF anchors."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LABEL_PATTERN = re.compile(
    r"\\newlabel\{(?P<label>[^}]+)\}"
    r"\{\{(?P<value>[^}]*)\}"
    r"\{[^}]*\}\{[^}]*\}"
    r"\{(?P<anchor>[^}]*)\}"
)

EXPECTED = {
    "chinese": {
        "xref:zh:chapter": ("第一章", "chapter.1"),
        "xref:zh:section": ("1.1", "section.1.1"),
        "xref:zh:subsection": ("1.1.1", "subsection.1.1.1"),
        "xref:zh:subsubsection": ("1.1.1.1", "subsubsection.1.1.1.1"),
        "xref:zh:definition": ("1.1", "definition.1.1"),
        "xref:zh:theorem": ("1.2", "theorem.1.2"),
        "xref:zh:lemma": ("1.3", "lemma.1.3"),
        "xref:zh:proposition": ("1.4", "proposition.1.4"),
        "xref:zh:corollary": ("1.5", "corollary.1.5"),
        "xref:zh:assumption": ("1.6", "assumption.1.6"),
        "xref:zh:remark": ("1.7", "remark.1.7"),
        "xref:zh:appendix": ("附录A", "appendix.A"),
        "xref:zh:appendix-definition": ("A.1", "definition.A.1"),
    },
    "english": {
        "xref:en:chapter": ("Chapter 1", "chapter.1"),
        "xref:en:section": ("1.1", "section.1.1"),
        "xref:en:subsection": ("1.1.1", "subsection.1.1.1"),
        "xref:en:subsubsection": ("1.1.1.1", "subsubsection.1.1.1.1"),
        "xref:en:definition": ("1.1", "definition.1.1"),
        "xref:en:theorem": ("1.2", "theorem.1.2"),
        "xref:en:lemma": ("1.3", "lemma.1.3"),
        "xref:en:proposition": ("1.4", "proposition.1.4"),
        "xref:en:corollary": ("1.5", "corollary.1.5"),
        "xref:en:assumption": ("1.6", "assumption.1.6"),
        "xref:en:remark": ("1.7", "remark.1.7"),
        "xref:en:appendix": ("Appendix A", "appendix.A"),
        "xref:en:appendix-definition": ("A.1", "definition.A.1"),
    },
}


def read_labels(path: Path) -> dict[str, tuple[str, str]]:
    labels: dict[str, tuple[str, str]] = {}
    for match in LABEL_PATTERN.finditer(path.read_text(encoding="utf-8")):
        labels[match.group("label")] = (
            match.group("value"),
            match.group("anchor"),
        )
    return labels


def check(path: Path, language: str) -> list[str]:
    labels = read_labels(path)
    errors: list[str] = []
    for label, expected in EXPECTED[language].items():
        actual = labels.get(label)
        if actual != expected:
            errors.append(f"{path.name}: {label} expected {expected}, got {actual}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chinese_aux", type=Path)
    parser.add_argument("english_aux", type=Path)
    arguments = parser.parse_args()

    errors = check(arguments.chinese_aux, "chinese")
    errors.extend(check(arguments.english_aux, "english"))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("PASS: 中英文章节、附录和定理类引用编号及PDF锚点均正确。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
