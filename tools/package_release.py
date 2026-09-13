#!/usr/bin/env python3
"""Create a clean, deterministic release archive from an explicit allowlist."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from release_audit import inspect_payload, sha256


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "uestc-thesis-xovee-chinese.zip"
DEFAULT_SOURCE_ONLY_OUTPUT = ROOT / "dist" / "uestc-thesis-xovee-chinese-source-preview.zip"
LANGUAGES = ("chinese", "english")

ROOT_FILES = (
    ".vscode/settings.json",
    ".vscode/extensions.json",
    "README.md",
    "GUIDE.md",
    "LICENSE",
    "NOTICE.md",
    "cover.pdf",
    "declaration.pdf",
    "main.tex",
    "uestcthesis.cls",
    "uestcthesis.bst",
    "latexmkrc",
    "references.bib",
    "fonts/README.md",
    "fonts/simsun.ttc",
    "fonts/simhei.ttf",
    "fonts/times.ttf",
    "fonts/timesbd.ttf",
    "fonts/timesi.ttf",
    "fonts/timesbi.ttf",
    "chapters/README.md",
    "chapters/abstract.tex",
    "chapters/achievements.tex",
    "chapters/acronyms.tex",
    "chapters/appendix.tex",
    "chapters/chapter-1.tex",
    "chapters/acknowledgements.tex",
    "chapters/symbols.tex",
    "figures/README.md",
    "figures/uestc-logo.png",
)

# Package destinations stay identical in both languages; maintenance sources do not.
ENGLISH_SOURCES = {
    "README.md": "README-english.md",
    "GUIDE.md": "GUIDE-english.md",
    "main.tex": "main-english.tex",
    "chapters/README.md": "chapters/README-english.md",
    **{f"chapters/{name}.tex": f"chapters/{name}-english.tex" for name in (
        "achievements", "acronyms", "appendix", "chapter-1", "acknowledgements", "symbols")},
}


def archive_root(language: str) -> Path:
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported package language: {language}")
    return Path(f"uestc-thesis-xovee-{language}")


def package_payload(sources: dict[str, bytes], language: str) -> dict[str, bytes]:
    payload = dict(sources)
    if "README.md" in payload:
        # Each archive has one guide; cross-language navigation stays on GitHub.
        base = "https://github.com/Xovee/uestc-thesis/blob/main/"
        local_guide = "GUIDE-english.md" if language == "english" else "GUIDE.md"
        readme = payload["README.md"].decode("utf-8")
        def readme_target(match: re.Match[str]) -> str:
            target = match.group(1)
            if target == local_guide:
                return "](GUIDE.md)"
            if target.endswith(".png"):
                return "](https://raw.githubusercontent.com/Xovee/uestc-thesis/main/" + target + ")"
            return "](" + base + target + ")"
        readme = re.sub(
            r"\]\((README(?:-english)?\.md|GUIDE(?:-english)?\.md|docs/previews/(?:chinese|english)\.(?:png|pdf))\)",
            readme_target, readme)
        payload["README.md"] = readme.encode("utf-8")
    if language == "english":
        # Only rename the six explicit inputs; never rewrite arbitrary thesis text.
        for destination, source in ENGLISH_SOURCES.items():
            if destination.startswith("chapters/") and destination.endswith(".tex"):
                old = ("\\input{" + source.removesuffix(".tex") + "}").encode()
                new = ("\\input{" + destination.removesuffix(".tex") + "}").encode()
                payload["main.tex"] = payload["main.tex"].replace(old, new)
    return payload


def source_map(entries: list[tuple[Path, Path]]) -> dict[str, str]:
    return {name.as_posix(): path.relative_to(ROOT).as_posix() for path, name in entries}

APPROVED_ASSET_HASHES = {
    "fonts/simsun.ttc": "1526AC24375F51F6EB73BC2D3F8072DBE4A80A3A65217677C9D9A84F67DAB2AB",
    "fonts/simhei.ttf": "9B1959DB3B3ABEB7EFDAEC26EDF7DFE871A6039DE8D614AF7248575207BE629E",
    "fonts/times.ttf": "931C5DE5C70401D9324D5014C123802B4FB753000360CEB2F56C589403CD58C5",
    "fonts/timesbd.ttf": "54FBE2C70AF7C85A97BED0573227E3CCC4B2486012E3CA2A40C6BC77065846F5",
    "fonts/timesi.ttf": "E7F7A88B65188328AEA58670F955022E23C712F55679524729DA1E4E03C49D88",
    "fonts/timesbi.ttf": "3A29D114CB5229E8DBDA5BEF6C69BE4A210A13B7277DE4D66E9FC86963226F6C",
    "cover.pdf": "E61948A8BCF74661737F9959605BCD7E6035AC4DA3E174F3BDB2481ED1B59A15",
    "declaration.pdf": "1D9E0FF9B0F4550D8976275C798327E1E52F63DE1B83947ADFF65AF0340378E3",
    "figures/uestc-logo.png": "944831E558C5313185106D18242906D9FEE988303F65294B857E7432558EBE1D",
}

REVIEW_FIELDS = ("content_and_images", "all_pdf_pages", "non_official_wording")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package only the files intended for template users."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            f"final archive path (default: {DEFAULT_OUTPUT.relative_to(ROOT)}); "
            "preparation creates a separate -candidate.zip; source-only uses -source-preview.zip"
        ),
    )
    parser.add_argument(
        "--reviewed",
        type=Path,
        help="finalize the exact candidate after completing its .review.json checks",
    )
    parser.add_argument("--tex-bin", type=Path, help="TeX binary directory for this build only")
    parser.add_argument("--language", choices=LANGUAGES,
                        help="thesis package language (default: chinese, or the reviewed candidate's language)")
    parser.add_argument(
        "--source-only",
        action="store_true",
        help="create a draft source package with GUIDE.md but without the example PDF",
    )
    return parser.parse_args()


def resolve_input(path: Path) -> Path:
    return (path if path.is_absolute() else ROOT / path).resolve()


def collect_user_files(language: str = "chinese") -> list[tuple[Path, Path]]:
    entries: list[tuple[Path, Path]] = []
    archive_root(language)

    for relative_name in ROOT_FILES:
        source_name = ENGLISH_SOURCES.get(relative_name, relative_name) if language == "english" else relative_name
        source = ROOT / source_name
        if not source.is_file():
            raise FileNotFoundError(f"required release file is missing: {source_name}")
        if not source.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f"release file resolves outside the project: {relative_name}")
        expected_hash = APPROVED_ASSET_HASHES.get(relative_name)
        if expected_hash is not None:
            actual_hash = hashlib.sha256(source.read_bytes()).hexdigest().upper()
            if actual_hash != expected_hash:
                raise ValueError(
                    f"approved binary asset has changed: {relative_name}\n"
                    f"expected SHA-256: {expected_hash}\n"
                    f"actual SHA-256:   {actual_hash}"
                )
        entries.append((source, Path(relative_name)))

    return entries


def require_ready_guide() -> None:
    guide = ROOT / "GUIDE.md"
    states = re.findall(
        r"^\s*<!--\s*guide-status:\s*(\w+)\s*-->\s*$",
        guide.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    if states != ["ready"]:
        raise ValueError(
            "GUIDE.md is not approved for a formal release. Complete and review the "
            "manual before setting its single guide-status marker to ready, or use "
            "--source-only for a draft source package."
        )


def build_example(directory: Path) -> dict:
    """Build from the exact copied payload, without reusing any old PDF or aux file."""
    compiler = shutil.which("latexmk")
    locator = shutil.which("kpsewhich")
    if compiler is None or locator is None:
        raise ValueError("TeX Live is required to prepare a formal candidate; use --tex-bin or --source-only")
    output = directory / "build"
    result = subprocess.run(
        [compiler, "-norc", "-r", str(directory / "latexmkrc"), "-xelatex",
         "-outdir=" + str(output), "-jobname=uestc-thesis-example", "main.tex"],
        cwd=directory, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise ValueError("Fresh example build failed; no package was created.\n" + result.stdout[-4000:] + result.stderr[-1000:])
    tex_root = subprocess.run([locator, "-var-value=TEXMFROOT"], check=True,
                              capture_output=True, text=True).stdout.strip()
    if not tex_root:
        raise ValueError("Cannot verify TeX installation input paths")
    system_root = Path(tex_root).resolve()
    recorder = (output / "uestc-thesis-example.fls").read_text(encoding="utf-8")
    for line in recorder.splitlines():
        if line.startswith("INPUT "):
            path = (directory / line[6:]).resolve()
            if not path.is_relative_to(directory.resolve()) and not path.is_relative_to(system_root):
                raise ValueError(f"Example read a file outside the staged source and TeX installation: {path.name}")
    bibliography_log = (output / "uestc-thesis-example.blg").read_text(encoding="utf-8", errors="replace")
    for name in re.findall(r"^(?:The style file: |Database file #\d+: )(.+)$", bibliography_log, re.M):
        path = (directory / name.strip()).resolve()
        if not path.is_file() or not path.is_relative_to(directory.resolve()):
            raise ValueError(f"Example bibliography input is not in the staged source: {name}")
    version = subprocess.run([compiler, "-v"], check=True, capture_output=True, text=True).stdout.strip()
    return {"entry": "main.tex", "fresh_build": True, "latexmk_version": version}


def validate_entries(entries: list[tuple[Path, Path]], output: Path) -> None:
    archive_names: set[Path] = set()
    resolved_output = output.resolve()

    for source, archive_name in entries:
        resolved_source = source.resolve()
        if resolved_source == resolved_output:
            raise ValueError("the output archive cannot also be an input file")
        if archive_name.is_absolute() or ".." in archive_name.parts:
            raise ValueError(f"unsafe archive path: {archive_name}")
        if archive_name in archive_names:
            raise ValueError(f"duplicate archive path: {archive_name}")
        archive_names.add(archive_name)


def write_archive(entries: list[tuple[Path, Path]], output: Path, language: str = "chinese") -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")

    try:
        with zipfile.ZipFile(
            temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for source, relative_name in sorted(entries, key=lambda item: item[1].as_posix()):
                archive_name = (archive_root(language) / relative_name).as_posix()
                info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100644 & 0xFFFF) << 16
                with source.open("rb") as handle:
                    archive.writestr(info, handle.read(), compresslevel=9)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()


def source_records(payload: dict[str, bytes]) -> list[dict]:
    return [{"path": name, "size": len(data), "sha256": sha256(data)}
            for name, data in sorted(payload.items())]


def snapshot_sources(entries: list[tuple[Path, Path]]) -> dict[str, bytes]:
    payload = {name.as_posix(): path.read_bytes() for path, name in entries}
    for name, expected in APPROVED_ASSET_HASHES.items():
        if sha256(payload[name]).upper() != expected:
            raise ValueError(f"Approved binary asset changed while reading it: {name}")
    return payload


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_package(entries: list[tuple[Path, Path]], output: Path, source_only: bool, language: str = "chinese") -> Path:
    raw_sources = snapshot_sources(entries)
    sources = source_records(raw_sources)
    payload = package_payload(raw_sources, language)
    candidate = output if source_only else output.with_name(output.stem + "-candidate.zip")
    report_path = candidate.with_suffix(".review.json")
    extra = sorted(path.relative_to(ROOT).as_posix() for folder in ("chapters", "figures")
                   for path in (ROOT / folder).rglob("*")
                   if path.is_file() and path.relative_to(ROOT).as_posix() not in source_map(entries).values())
    initial = inspect_payload(payload, language)
    if initial["findings"]:
        write_json(report_path, {"kind": "blocked", "audit": initial, "excluded_files": extra})
        raise ValueError(f"Release content checks failed; inspect {report_path}")
    with tempfile.TemporaryDirectory(prefix="uestc-release-") as temporary:
        stage = Path(temporary)
        for name, data in payload.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        build = None
        if not source_only:
            build = build_example(stage)
            if any((stage / name).read_bytes() != data for name, data in payload.items()):
                raise ValueError("Example build modified a staged source file")
            payload["uestc-thesis-example.pdf"] = (stage / "build/uestc-thesis-example.pdf").read_bytes()
        audit = inspect_payload(payload, language)
        if audit["findings"]:
            write_json(report_path, {"kind": "blocked", "audit": audit, "excluded_files": extra})
            raise ValueError(f"Release content checks failed; inspect {report_path}")
        if sources != source_records({name.as_posix(): path.read_bytes() for path, name in entries}):
            raise ValueError("Source changed during preparation; rerun with a stable source tree")
        staged_entries = []
        for name, data in payload.items():
            path = stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            staged_entries.append((path, Path(name)))
        validate_entries(staged_entries, candidate)
        write_archive(staged_entries, candidate, language)
    report = {"schema": 2, "language": language, "source_map": source_map(entries),
              "kind": "source-preview" if source_only else "formal-candidate",
              "candidate": candidate.name, "archive_sha256": sha256(candidate.read_bytes()),
              "sources": sources, "audit": audit, "excluded_files": extra, "build": build,
              "review": {key: False for key in REVIEW_FIELDS}}
    if not source_only:
        preview = candidate.with_suffix(".example.pdf")
        preview.write_bytes(payload["uestc-thesis-example.pdf"])
        report["example_preview"] = preview.name
    write_json(report_path, report)
    print(f"PASS: prepared {'draft source package' if source_only else 'candidate for review'}: {candidate}")
    print(f"PASS: archive contains {len(payload)} exact-listed files; review record: {report_path}")
    return report_path


def finalize_package(entries: list[tuple[Path, Path]], report_path: Path, output: Path, language: str = "chinese") -> None:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, dict) or report.get("schema") != 2 or report.get("kind") != "formal-candidate":
        raise ValueError("A formal candidate review record is required")
    if report.get("language") != language or report.get("source_map") != source_map(entries):
        raise ValueError("Candidate language or source mapping differs; prepare a new candidate")
    if any(report.get("review", {}).get(key) is not True for key in REVIEW_FIELDS):
        raise ValueError("Complete the content, PDF-page and non-official-wording review checks first")
    payload = snapshot_sources(entries)
    if report.get("sources") != source_records(payload):
        raise ValueError("Source changed since review; prepare and review a new candidate")
    payload = package_payload(payload, language)
    prefix = archive_root(language).as_posix()
    candidate_name = report.get("candidate", "")
    if not candidate_name or Path(candidate_name).name != candidate_name:
        raise ValueError("Candidate filename must stay beside its review record")
    candidate = report_path.parent / candidate_name
    archive_bytes = candidate.read_bytes()
    if sha256(archive_bytes) != report.get("archive_sha256"):
        raise ValueError("Candidate archive changed since review")
    with zipfile.ZipFile(candidate) as archive:
        expected = {f"{prefix}/{name}" for name in payload} | {f"{prefix}/uestc-thesis-example.pdf"}
        if len(archive.namelist()) != len(expected) or set(archive.namelist()) != expected or archive.testzip():
            raise ValueError("Candidate archive member list is invalid")
        for name, data in payload.items():
            if archive.read(f"{prefix}/{name}") != data:
                raise ValueError(f"Candidate source differs from the current source: {name}")
        payload["uestc-thesis-example.pdf"] = archive.read(f"{prefix}/uestc-thesis-example.pdf")
    audit = inspect_payload(payload, language)
    if audit != report.get("audit") or audit["findings"]:
        raise ValueError("Candidate inspection no longer matches the reviewed record")
    preview_name = report.get("example_preview", "")
    if not preview_name or Path(preview_name).name != preview_name or (report_path.parent / preview_name).read_bytes() != payload["uestc-thesis-example.pdf"]:
        raise ValueError("Reviewed PDF preview no longer matches the candidate PDF")
    if not isinstance(report.get("build"), dict) or report["build"].get("fresh_build") is not True:
        raise ValueError("Candidate does not have a fresh example build record")
    protected = {report_path.resolve(), candidate.resolve(), (report_path.parent / preview_name).resolve()}
    if output.resolve() in protected or output.with_suffix('.manifest.json').resolve() in protected:
        raise ValueError("Formal output must not overwrite review artifacts")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    try:
        temporary.write_bytes(archive_bytes)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    write_json(output.with_suffix(".manifest.json"), report)
    print(f"PASS: finalized reviewed formal release: {output}")


def main() -> int:
    args = parse_args()
    try:
        if args.source_only and args.reviewed:
            raise ValueError("--source-only cannot finalize a formal release")
        language = args.language
        if args.reviewed and language is None:
            report = json.loads(resolve_input(args.reviewed).read_text(encoding="utf-8"))
            if not isinstance(report, dict) or report.get("language") not in LANGUAGES:
                raise ValueError("A formal candidate review record with a package language is required")
            language = report["language"]
        language = language or "chinese"
        default_output = DEFAULT_SOURCE_ONLY_OUTPUT if args.source_only else DEFAULT_OUTPUT
        if language == "english":
            suffix = "-source-preview.zip" if args.source_only else ".zip"
            default_output = ROOT / "dist" / (archive_root(language).name + suffix)
        output = resolve_input(args.output or default_output)
        if args.tex_bin:
            os.environ["PATH"] = str(args.tex_bin.resolve()) + os.pathsep + os.environ.get("PATH", "")
        entries = collect_user_files(language)
        validate_entries(entries, output)
        if not args.source_only:
            require_ready_guide()
        if args.reviewed:
            finalize_package(entries, resolve_input(args.reviewed), output, language)
        else:
            prepare_package(entries, output, args.source_only, language)
    except (FileNotFoundError, OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
