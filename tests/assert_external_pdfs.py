#!/usr/bin/env python3
"""Assert the release properties of the default external PDF materials."""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


A4_WIDTH = 595.28
A4_HEIGHT = 841.89
SIZE_TOLERANCE = 1.0


@dataclass(frozen=True)
class ExpectedPdf:
    name: str
    pages: int
    sha256: str


EXPECTED_PDFS = (
    ExpectedPdf(
        name="cover.pdf",
        pages=3,
        sha256="E61948A8BCF74661737F9959605BCD7E6035AC4DA3E174F3BDB2481ED1B59A15",
    ),
    ExpectedPdf(
        name="declaration.pdf",
        pages=1,
        sha256="1D9E0FF9B0F4550D8976275C798327E1E52F63DE1B83947ADFF65AF0340378E3",
    ),
)


def resolved_object(value: object) -> object:
    getter = getattr(value, "get_object", None)
    return getter() if getter else value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def check_pdf(path: Path, expected: ExpectedPdf) -> list[str]:
    errors: list[str] = []
    try:
        reader = PdfReader(str(path))
    except Exception as exception:
        return [f"无法读取{path.name}：{exception}"]

    actual_hash = sha256(path)
    if actual_hash != expected.sha256:
        errors.append(
            f"{path.name}的SHA-256已变化：{actual_hash}；"
            "替换官方材料后应人工复核并更新断言"
        )

    if reader.is_encrypted:
        errors.append(f"{path.name}不应加密")

    if len(reader.pages) != expected.pages:
        errors.append(
            f"{path.name}应为{expected.pages}页，实际为{len(reader.pages)}页"
        )

    for page_number, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if (
            abs(width - A4_WIDTH) > SIZE_TOLERANCE
            or abs(height - A4_HEIGHT) > SIZE_TOLERANCE
        ):
            errors.append(
                f"{path.name}第{page_number}页不是A4尺寸："
                f"{width:.2f} x {height:.2f} pt"
            )
        if page.get("/Annots"):
            errors.append(f"{path.name}第{page_number}页不应包含批注或交互对象")

    metadata = reader.metadata
    if metadata and any(value not in (None, "") for value in metadata.values()):
        errors.append(f"{path.name}仍包含PDF文档元数据：{dict(metadata)}")
    if reader.xmp_metadata is not None:
        errors.append(f"{path.name}仍包含XMP元数据")

    catalog = resolved_object(reader.trailer["/Root"])
    if catalog.get("/AcroForm"):
        errors.append(f"{path.name}不应包含PDF表单")
    if catalog.get("/OpenAction") or catalog.get("/AA"):
        errors.append(f"{path.name}不应包含自动执行动作")

    names = catalog.get("/Names")
    if names:
        names = resolved_object(names)
        if names.get("/EmbeddedFiles"):
            errors.append(f"{path.name}不应包含附件")
        if names.get("/JavaScript"):
            errors.append(f"{path.name}不应包含JavaScript")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "project_root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="包含cover.pdf和declaration.pdf的项目根目录，默认为当前目录",
    )
    arguments = parser.parse_args()

    errors: list[str] = []
    for expected in EXPECTED_PDFS:
        path = arguments.project_root / expected.name
        if not path.is_file():
            errors.append(f"找不到{path}")
            continue
        errors.extend(check_pdf(path, expected))

    if errors:
        print("外部PDF断言失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PASS: cover.pdf为3页、declaration.pdf为1页；"
        "文件哈希、A4页面、空元数据和非交互结构均正常。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
