#!/usr/bin/env python3
"""Assert the stable PDF structure of a Chinese or English example PDF."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import ArrayObject, IndirectObject


A4_WIDTH = 595.28
A4_HEIGHT = 841.89
SIZE_TOLERANCE = 1.0
EXPECTED_EXTERNAL_LABELS = ["C1", "C2", "C3", "D1"]
PROFILES = {
    "chinese": {
        "metadata": {
            "/Title": "论文题目",
            "/Author": "作者姓名",
            "/Creator": "UESTC Thesis LaTeX Template by Xovee Xu",
        },
        "front_bookmark_order": [
            "摘要",
            "ABSTRACT",
            "目录",
            "图目录",
            "表目录",
            "主要符号表",
            "缩略词表",
        ],
        "main_bookmarks": {
            "模板使用示例",
            "致谢",
            "参考文献",
            "补充材料",
            "攻读硕士学位期间取得的成果",
        },
        "first_chapter": "模板使用示例",
    },
    "english": {
        "metadata": {
            "/Title": "English Thesis Title",
            "/Author": "Author Name",
            "/Creator": "UESTC Thesis LaTeX Template by Xovee Xu",
        },
        "front_bookmark_order": [
            "摘要",
            "ABSTRACT",
            "Contents",
            "Figures",
            "Tables",
            "Symbols",
            "Acronyms",
        ],
        "main_bookmarks": {
            "TemplateUsageExample",
            "Acknowledgements",
            "References",
            "SupplementaryMaterial",
            "ResearchResultsObtainedDuringtheStudyforMaster'sDegree",
        },
        "first_chapter": "TemplateUsageExample",
    },
}


def roman(number: int) -> str:
    values = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )
    result = []
    for value, numeral in values:
        count, number = divmod(number, value)
        result.append(numeral * count)
    return "".join(result)


def normalized_title(title: str) -> str:
    return "".join(title.split())


def collect_outline(reader: PdfReader) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []

    def visit(items: list[object], level: int = 0) -> None:
        for item in items:
            if isinstance(item, list):
                visit(item, level + 1)
                continue
            try:
                page = reader.get_destination_page_number(item) + 1
            except Exception:
                page = None
            entries.append(
                {
                    "level": level,
                    "title": normalized_title(getattr(item, "title", str(item))),
                    "page": page,
                }
            )

    visit(reader.outline)
    return entries


def page_object_map(reader: PdfReader) -> dict[tuple[int, int], int]:
    result = {}
    for index, page in enumerate(reader.pages, start=1):
        reference = page.indirect_reference
        if reference is not None:
            result[(reference.idnum, reference.generation)] = index
    return result


def destination_page(
    reader: PdfReader,
    destination: object,
    pages_by_object: dict[tuple[int, int], int],
) -> int | None:
    if isinstance(destination, str):
        named = reader.named_destinations.get(destination)
        return reader.get_destination_page_number(named) + 1 if named else None
    if isinstance(destination, ArrayObject) and destination:
        target = destination[0]
        if isinstance(target, IndirectObject):
            return pages_by_object.get((target.idnum, target.generation))
        try:
            return int(target) + 1
        except (TypeError, ValueError):
            return None
    try:
        return reader.get_destination_page_number(destination) + 1
    except Exception:
        return None


def internal_link_targets(reader: PdfReader) -> tuple[list[int], int]:
    pages_by_object = page_object_map(reader)
    targets = []
    unresolved = 0
    for page in reader.pages:
        for annotation_reference in page.get("/Annots", []):
            annotation = annotation_reference.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A")
            if isinstance(action, IndirectObject):
                action = action.get_object()
            destination = annotation.get("/Dest")
            if destination is None and action and action.get("/S") == "/GoTo":
                destination = action.get("/D")
            if destination is None:
                continue
            target = destination_page(reader, destination, pages_by_object)
            if target is None:
                unresolved += 1
            else:
                targets.append(target)
    return targets, unresolved


def check_pdf(pdf_path: Path, language: str) -> list[str]:
    errors = []
    profile = PROFILES[language]
    expected_metadata = profile["metadata"]
    front_bookmark_order = profile["front_bookmark_order"]
    main_bookmarks = profile["main_bookmarks"]
    required_top_level_bookmarks = set(front_bookmark_order) | set(main_bookmarks)
    first_chapter = profile["first_chapter"]
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exception:
        return [f"无法读取PDF：{exception}"]

    if reader.is_encrypted:
        errors.append("示例PDF不应加密")

    page_count = len(reader.pages)
    labels = reader.page_labels
    if len(labels) != page_count:
        errors.append(f"页码标签数量{len(labels)}与页面数量{page_count}不一致")
        return errors
    if len(set(labels)) != len(labels):
        errors.append("页码标签存在重复")
    if labels[:4] != EXPECTED_EXTERNAL_LABELS:
        errors.append(
            f"外部PDF页码标签应为{EXPECTED_EXTERNAL_LABELS}，实际为{labels[:4]}"
        )

    try:
        main_start = labels.index("1")
    except ValueError:
        errors.append("没有找到从1开始的正文页码标签")
        main_start = len(labels)

    front_labels = labels[4:main_start]
    expected_front_labels = [roman(index) for index in range(1, len(front_labels) + 1)]
    if front_labels != expected_front_labels:
        errors.append(
            f"前置部分页码标签应连续使用大写罗马数字，实际为{front_labels}"
        )

    main_labels = labels[main_start:]
    expected_main_labels = [str(index) for index in range(1, len(main_labels) + 1)]
    if main_labels != expected_main_labels:
        errors.append(f"正文页码标签应从1连续编号，实际为{main_labels}")

    for page_number, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - A4_WIDTH) > SIZE_TOLERANCE or abs(height - A4_HEIGHT) > SIZE_TOLERANCE:
            errors.append(
                f"第{page_number}页不是A4尺寸：{width:.2f} x {height:.2f} pt"
            )

    metadata = reader.metadata or {}
    for key, expected in expected_metadata.items():
        actual = metadata.get(key)
        if actual != expected:
            errors.append(f"元数据{key}应为`{expected}`，实际为`{actual}`")
    producer = str(metadata.get("/Producer", ""))
    if not producer.startswith("xdvipdfmx"):
        errors.append(f"PDF生成器应为xdvipdfmx，实际为`{producer}`")

    outline = collect_outline(reader)
    top_level = {entry["title"] for entry in outline if entry["level"] == 0}
    missing_bookmarks = sorted(required_top_level_bookmarks - top_level)
    if missing_bookmarks:
        errors.append(f"缺少顶层书签：{missing_bookmarks}")

    bookmark_pages = {}
    for entry in outline:
        page = entry["page"]
        if page is None or not 1 <= page <= page_count:
            errors.append(f"书签`{entry['title']}`没有有效目标页面")
            continue
        if page <= len(EXPECTED_EXTERNAL_LABELS):
            errors.append(f"书签`{entry['title']}`错误地指向外部封面或声明页面")
        if entry["level"] == 0:
            bookmark_pages[entry["title"]] = page

    abstract_page = bookmark_pages.get("摘要")
    abstract_label = labels[abstract_page - 1] if abstract_page else None
    if abstract_label != "I":
        errors.append(f"书签`摘要`应指向页码标签I，实际为{abstract_label}")

    front_pages = []
    for title in front_bookmark_order:
        page = bookmark_pages.get(title)
        if page is None:
            continue
        front_pages.append(page)
        actual_label = labels[page - 1]
        if actual_label not in front_labels:
            errors.append(
                f"前置部分书签`{title}`应指向大写罗马数字页码，实际为{actual_label}"
            )
    if front_pages != sorted(front_pages) or len(set(front_pages)) != len(front_pages):
        errors.append("前置部分书签目标页面没有按照文档顺序严格递增")

    for title in main_bookmarks:
        page = bookmark_pages.get(title)
        if page is None:
            continue
        actual_label = labels[page - 1]
        if not actual_label.isdigit():
            errors.append(
                f"正文书签`{title}`应指向阿拉伯数字页码，实际为{actual_label}"
            )

    first_chapter_page = bookmark_pages.get(first_chapter)
    first_chapter_label = labels[first_chapter_page - 1] if first_chapter_page else None
    if first_chapter_label != "1":
        errors.append(
            f"书签`{first_chapter}`应指向正文第1页，实际为{first_chapter_label}"
        )

    link_targets, unresolved_links = internal_link_targets(reader)
    if not link_targets:
        errors.append("没有检测到内部链接")
    if unresolved_links:
        errors.append(f"存在{unresolved_links}个无法解析的内部链接")
    invalid_targets = [target for target in link_targets if not 1 <= target <= page_count]
    if invalid_targets:
        errors.append(f"内部链接指向PDF范围之外的页面：{invalid_targets}")
    external_page_targets = [
        target for target in link_targets if target <= len(EXPECTED_EXTERNAL_LABELS)
    ]
    if external_page_targets:
        errors.append(f"内部链接错误地指向外部封面或声明页面：{external_page_targets}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="示例PDF的路径")
    parser.add_argument(
        "--language",
        choices=tuple(PROFILES),
        default="chinese",
        help="示例语言，默认为chinese",
    )
    arguments = parser.parse_args()

    if not arguments.pdf.is_file():
        print(f"FAIL: 找不到PDF：{arguments.pdf}", file=sys.stderr)
        return 1

    errors = check_pdf(arguments.pdf, arguments.language)
    if errors:
        print("PDF结构断言失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    reader = PdfReader(str(arguments.pdf))
    top_level_count = sum(
        entry["level"] == 0 for entry in collect_outline(reader)
    )
    print(
        f"PASS: {arguments.pdf}，{len(reader.pages)}页，"
        f"{top_level_count}个顶层书签，页码标签、书签、内部链接和元数据均正常。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
