"""Inspect the exact release payload; human review still covers names and images."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
import re
from urllib.parse import urlsplit

from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, TextStringObject


PUBLIC_EMAILS = {"xovee.xu@gmail.com"}
# Reviewed embedded-font XMP: only xmpRights:Marked=True; retain the copyright mark.
APPROVED_RIGHTS_XMP = {"dcbea084ecf33e2871392e1f3d8ae2c4b4c9c2f42d5b99acf819e38fc688aaa4"}
TEXT_SUFFIXES = {".tex", ".cls", ".bst", ".bib", ".md", ".json"}
PATTERNS = {
    "email": re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I),
    "phone": re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d[- ]?\d{4}[- ]?\d{4}(?!\d)|(?:电话|phone|tel)\s*[:：]\s*\+?\d[\d ()-]{6,}\d", re.I),
    "identity_number": re.compile(r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?!\d)"),
    "student_number": re.compile(r"(?:学\s*号|student\s*(?:id|number))\s*[:：=]?\s*\d{8,}(?![\dXx])", re.I),
    "local_path": re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|file://|(?<![A-Za-z0-9/])/(?:Users|home)/[^/\s]+|\\\\[^\\\s]+\\[^\\\s]+", re.I),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan_text(text: str, location: str) -> list[dict]:
    findings = []
    for kind, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            if kind == "email" and match.group().lower() in PUBLIC_EMAILS:
                continue
            findings.append({"location": location, "kind": kind,
                             "line": text.count("\n", 0, match.start()) + 1})
    return findings


def inspect_pdf(name: str, data: bytes, language: str = "chinese") -> tuple[dict, list[dict]]:
    placeholders = {"chinese": ("论文题目", "作者姓名"), "english": ("English Thesis Title", "Author Name")}
    if language not in placeholders:
        raise ValueError(f"Unsupported package language: {language}")
    findings = []

    def flag(kind, location=name):
        findings.append({"location": location, "kind": kind})

    try:
        reader = PdfReader(io.BytesIO(data), strict=True)
        if reader.is_encrypted:
            flag("encrypted_pdf")
            return {"path": name, "encrypted": True}, findings
        metadata = {str(k): str(v) for k, v in (reader.metadata or {}).items()}
        summary = {"path": name, "pages": len(reader.pages), "metadata": metadata,
                   "page_sizes": [], "annotation_types": [], "uri_targets": [], "xmp_sha256": []}
        if not reader.pages:
            flag("empty_pdf")
        for key, value in metadata.items():
            findings.extend(scan_text(value, f"{name}:metadata{key}"))
        if name in {"cover.pdf", "declaration.pdf"}:
            if any(metadata.values()):
                flag("personalized_external_pdf_metadata")
            if len(reader.pages) != (3 if name == "cover.pdf" else 1):
                flag("external_pdf_page_count")
        if name == "uestc-thesis-example.pdf":
            title, author = placeholders[language]
            expected = {"/Title": title, "/Author": author,
                        "/Creator": "UESTC Thesis LaTeX Template by Xovee Xu"}
            if any(metadata.get(key) != value for key, value in expected.items()):
                flag("example_metadata_must_use_placeholders")
            allowed = set(expected) | {"/Producer", "/CreationDate", "/ModDate", "/Subject", "/Keywords", "/Trapped"}
            if set(metadata) - allowed or metadata.get("/Subject") or metadata.get("/Keywords"):
                flag("unexpected_example_metadata")
        for number, page in enumerate(reader.pages, 1):
            location = f"{name}:page {number}"
            width, height = float(page.mediabox.width), float(page.mediabox.height)
            summary["page_sizes"].append([round(width, 3), round(height, 3)])
            if name in {"cover.pdf", "declaration.pdf", "uestc-thesis-example.pdf"} and (
                    abs(width - 595.28) > 1 or abs(height - 841.89) > 1):
                flag("expected_a4_page", location)
            findings.extend(scan_text(page.extract_text() or "", location))
            for reference in page.get("/Annots", []):
                kind = str(reference.get_object().get("/Subtype", "unknown"))
                summary["annotation_types"].append(kind)
                if kind != "/Link" or name in {"cover.pdf", "declaration.pdf"}:
                    flag("unexpected_pdf_annotation", location)

        # Walk referenced objects once, including metadata, actions, names and forms.
        visited = set()

        def walk(value, action_context=False):
            if isinstance(value, IndirectObject):
                identity = (value.idnum, value.generation, action_context)
                if identity in visited:
                    return
                visited.add(identity)
                value = value.get_object()
            if isinstance(value, DictionaryObject):
                if any(key in value for key in ("/EmbeddedFiles", "/EF", "/AF", "/AcroForm", "/JavaScript", "/JS", "/AA")):
                    flag("attachments_forms_or_active_content")
                if "/Metadata" in value:
                    xmp = value["/Metadata"].get_object().get_data()
                    digest = sha256(xmp)
                    summary["xmp_sha256"].append(digest)
                    findings.extend(scan_text(xmp.decode("utf-8", errors="replace"), f"{name}:XMP"))
                    if digest not in APPROVED_RIGHTS_XMP:
                        flag("unreviewed_xmp_metadata")
                action = value.get("/S")
                is_action = (action_context and "/S" in value) or value.get("/Type") == "/Action"
                if is_action and str(action) not in {"/GoTo", "/URI"}:
                    flag("unsafe_pdf_action")
                if "/URI" in value:
                    uri = str(value["/URI"])
                    summary["uri_targets"].append(uri)
                    if urlsplit(uri).scheme.lower() not in {"https", "http", "mailto"}:
                        flag("unsafe_pdf_uri")
                for key, child in value.items():
                    walk(child, key in {"/A", "/OpenAction"} or (key == "/Next" and is_action))
            elif isinstance(value, (ArrayObject, list)):
                for child in value:
                    walk(child, action_context)
            elif isinstance(value, TextStringObject):
                findings.extend(scan_text(str(value), f"{name}:PDF string"))

        walk(reader.trailer)
        summary["annotation_types"] = sorted(set(summary["annotation_types"]))
        summary["uri_targets"] = sorted(set(summary["uri_targets"]))
        summary["xmp_sha256"] = sorted(set(summary["xmp_sha256"]))
        return summary, findings
    except Exception as error:
        flag("unreadable_pdf")
        return {"path": name, "error_type": type(error).__name__}, findings


def inspect_payload(payload: dict[str, bytes], language: str = "chinese") -> dict:
    files, pdfs, findings = [], [], []
    for name, data in sorted(payload.items()):
        files.append({"path": name, "size": len(data), "sha256": sha256(data)})
        if name.lower().endswith(".pdf"):
            summary, issues = inspect_pdf(name, data, language)
            pdfs.append(summary)
            findings.extend(issues)
        elif Path(name).suffix.lower() in TEXT_SUFFIXES or name in {"LICENSE", "latexmkrc"}:
            findings.extend(scan_text(data.decode("utf-8"), name))
    unique = {tuple(sorted(item.items())): item for item in findings}
    return {"files": files, "pdfs": pdfs, "findings": list(unique.values())}
