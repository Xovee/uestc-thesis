#!/usr/bin/env python3
"""Run the complete maintainer regression suite from one stable entry point."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BUILD_DIR = PROJECT_ROOT / "build" / "regression"


@dataclass(frozen=True)
class LatexCase:
    jobname: str
    source: str
    quick: bool = False


CASES = (
    LatexCase("r01-reference-boundaries", "tests/r01-reference-boundaries.tex", quick=True),
    LatexCase("r01-reference-boundaries-english", "tests/r01-reference-boundaries-english.tex", quick=True),
    LatexCase("f05-editions", "tests/f05-editions.tex", quick=True),
    LatexCase("f05-editions-english", "tests/f05-editions-english.tex", quick=True),
    LatexCase("f04-subfigures", "tests/f04-subfigures.tex", quick=True),
    LatexCase("f04-subfigures-english", "tests/f04-subfigures-english.tex", quick=True),
    LatexCase("f03-table-spacing", "tests/f03-table-spacing.tex", quick=True),
    LatexCase("f03-table-spacing-english", "tests/f03-table-spacing-english.tex", quick=True),
    LatexCase("f02-appendix-fonts", "tests/f02-appendix-fonts.tex", quick=True),
    LatexCase("f02-appendix-fonts-english", "tests/f02-appendix-fonts-english.tex", quick=True),
    LatexCase("f02-appendix-fonts-doctor", "tests/f02-appendix-fonts-doctor.tex"),
    LatexCase("f02-appendix-fonts-doctor-english", "tests/f02-appendix-fonts-doctor-english.tex"),
    LatexCase("f01-original", "tests/f01-original.tex", quick=True),
    LatexCase("f01-boundaries", "tests/f01-boundaries.tex"),
    LatexCase("f01-boundaries-english", "tests/f01-boundaries-english.tex"),
    LatexCase("layout-contract", "tests/layout-contract.tex", quick=True),
    LatexCase("master-chinese", "tests/smoke.tex", quick=True),
    LatexCase("doctor-chinese", "tests/smoke-doctor.tex", quick=True),
    LatexCase("master-english", "tests/smoke-english.tex", quick=True),
    LatexCase("doctor-english", "tests/smoke-doctor-english.tex", quick=True),
    LatexCase(
        "full-example-english",
        "tests/full-example-english.tex",
        quick=True,
    ),
    LatexCase("cross-references", "tests/cross-references.tex", quick=True),
    LatexCase(
        "cross-references-english",
        "tests/cross-references-english.tex",
        quick=True,
    ),
    LatexCase("bibliography-pagination", "tests/bibliography-pagination.tex"),
    LatexCase("bibliography-types", "tests/bibliography-types.tex"),
    LatexCase("caption-citations", "tests/caption-citations.tex"),
    LatexCase("caption-citations-english", "tests/caption-citations-english.tex"),
    LatexCase("appendix-numbering", "tests/appendix-numbering.tex"),
    LatexCase(
        "appendix-numbering-english",
        "tests/appendix-numbering-english.tex",
    ),
    LatexCase("numbering-boundaries", "tests/numbering-boundaries.tex"),
    LatexCase(
        "numbering-boundaries-english",
        "tests/numbering-boundaries-english.tex",
    ),
    LatexCase("heading-pagination", "tests/heading-pagination.tex"),
    LatexCase(
        "heading-pagination-english",
        "tests/heading-pagination-english.tex",
    ),
    LatexCase("notation-lists", "tests/notation-lists.tex"),
    LatexCase("notation-lists-english", "tests/notation-lists-english.tex"),
)


def display_command(command: list[str]) -> str:
    return " ".join(f'"{part}"' if " " in part else part for part in command)


def normalized_tools(tools: dict) -> dict:
    # Windows latexmk prints console code-page diagnostics before its version.
    # A different terminal encoding does not mean a different TeX installation.
    result = {name: dict(details) for name, details in tools.items()}
    if "latexmk" in result:
        result["latexmk"]["version"] = re.sub(
            r"\A.*?(?=Latexmk,)", "", result["latexmk"]["version"], flags=re.S
        )
    return result


def run(command: list[str]) -> None:
    print(f"\n>>> {display_command(command)}", flush=True)
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    if result.returncode:
        raise RuntimeError(
            f"命令以状态码{result.returncode}失败：{display_command(command)}"
        )


def compile_case(case: LatexCase, build_dir: Path) -> None:
    run(
        [
            "latexmk",
            "-xelatex",
            f"-outdir={build_dir}",
            f"-jobname={case.jobname}",
            case.source,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tex-bin", type=Path,
        help="本次测试使用的TeX发行版bin目录；不更改系统PATH",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="只运行四种硕博、中英文组合和默认完整示例",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=DEFAULT_BUILD_DIR,
        help="回归测试输出目录，默认为build/regression",
    )
    arguments = parser.parse_args()

    if arguments.tex_bin:
        tex_bin = arguments.tex_bin.resolve()
        for tool in ("latexmk", "xelatex", "bibtex"):
            if shutil.which(tool, path=str(tex_bin)) is None:
                parser.error(f"指定目录中找不到{tool}：{tex_bin}")
        os.environ["PATH"] = str(tex_bin) + os.pathsep + os.environ.get("PATH", "")

    if shutil.which("latexmk") is None:
        print("FAIL: 找不到latexmk，请先安装受支持的TeX发行版。", file=sys.stderr)
        return 1

    build_dir = arguments.build_dir
    if not build_dir.is_absolute():
        build_dir = PROJECT_ROOT / build_dir
    build_dir.mkdir(parents=True, exist_ok=True)
    environment = {"platform": platform.platform(), "python": sys.version, "tools": {}}
    for tool, flag in (("latexmk", "-v"), ("xelatex", "--version"), ("bibtex", "--version")):
        executable = shutil.which(tool)
        if executable is None:
            parser.error(f"找不到{tool}")
        version = subprocess.run([executable, flag], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", check=True)
        environment["tools"][tool] = {"path": executable, "version": version.stdout.strip()}
    environment_file = build_dir / "environment.json"
    if environment_file.exists():
        previous = json.loads(environment_file.read_text(encoding="utf-8"))
        if normalized_tools(previous.get("tools", {})) != normalized_tools(environment["tools"]):
            parser.error("输出目录包含其他工具版本的结果，请使用不同的--build-dir。")
    environment_file.write_text(json.dumps(environment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    selected_cases = [case for case in CASES if case.quick or not arguments.quick]

    try:
        run([sys.executable, "tests/assert_external_pdfs.py"])
        run([sys.executable, "tests/prepare_subfigure_example.py", "GUIDE.md",
             str(build_dir / "f04-guide-example.tex")])
        for case in selected_cases:
            compile_case(case, build_dir)
        for case in selected_cases:
            if case.jobname.startswith("r01-reference-boundaries"):
                run([sys.executable, "tests/assert_reference_boundaries.py",
                     str(build_dir / f"{case.jobname}.pdf")])
            if case.jobname.startswith("f05-editions"):
                run([sys.executable, "tests/assert_editions.py",
                     str(build_dir / f"{case.jobname}.pdf")])
            if case.jobname.startswith("f04-subfigures"):
                command = [sys.executable, "tests/assert_subfigures.py",
                           str(build_dir / f"{case.jobname}.pdf")]
                if case.jobname.endswith("-english"):
                    command.append("--english")
                run(command)
            if case.jobname.startswith("f03-table-spacing"):
                run([sys.executable, "tests/assert_table_spacing.py",
                     str(build_dir / f"{case.jobname}.pdf")])
            if case.jobname.startswith("f02-appendix-fonts"):
                command = [sys.executable, "tests/assert_appendix_fonts.py",
                           str(build_dir / f"{case.jobname}.pdf")]
                if case.jobname.endswith("-english"):
                    command.append("--english")
                run(command)
        run([sys.executable, "tests/assert_layout_contract.py", str(build_dir / "layout-contract.pdf")])
        run([sys.executable, "tests/assert_toc_page_columns.py",
             str(build_dir / "f01-original.pdf"), "--pages", "1", "--entries", "2"])
        if not arguments.quick:
            for jobname in ("f01-boundaries", "f01-boundaries-english"):
                run([sys.executable, "tests/assert_toc_page_columns.py",
                     str(build_dir / f"{jobname}.pdf"), "--pages", "2", "3", "4",
                     "--entries", "12"])

        run(
            [
                sys.executable,
                "tests/assert_cross_reference_anchors.py",
                str(build_dir / "cross-references.aux"),
                str(build_dir / "cross-references-english.aux"),
            ]
        )
        if not arguments.quick:
            for jobname in ("caption-citations", "caption-citations-english"):
                run(
                    [
                        sys.executable,
                        "tests/assert_caption_citation_order.py",
                        str(build_dir / f"{jobname}.pdf"),
                    ]
                )
            run(
                [
                    sys.executable,
                    "tests/assert_bibliography_types.py",
                    str(build_dir / "bibliography-types.pdf"),
                ]
            )
            run(
                [
                    sys.executable,
                    "tests/assert_bibliography_fields.py",
                    str(build_dir / "bibliography-pagination.pdf"),
                ]
            )

        example = LatexCase("uestc-thesis-template-preview", "main.tex")
        compile_case(example, build_dir)
        run(
            [
                sys.executable,
                "tests/assert_pdf_structure.py",
                str(build_dir / "uestc-thesis-template-preview.pdf"),
            ]
        )
        run(
            [
                sys.executable,
                "tests/assert_pdf_structure.py",
                str(build_dir / "full-example-english.pdf"),
                "--language",
                "english",
            ]
        )
    except RuntimeError as exception:
        print(f"\nFAIL: {exception}", file=sys.stderr)
        return 1

    log = (build_dir / "uestc-thesis-template-preview.log").read_text(encoding="utf-8", errors="replace")
    environment["loaded_versions"] = [line.strip() for line in log.splitlines()
                                      if re.match(r"(?:LaTeX2e|L3 programming layer|Package:|Document Class:)", line)]
    environment_file.write_text(json.dumps(environment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mode = "快速" if arguments.quick else "完整"
    print(
        f"\nPASS: {mode}回归测试通过，共编译{len(selected_cases) + 1}份文档。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
